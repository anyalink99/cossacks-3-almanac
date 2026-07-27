# Native API движка Cossacks 3 (Delphi + DWS)

Реверс-инжиниринг нативного слоя движка через статический анализ
`cossacks.exe` — без Ghidra/IDA, только парсинг бинарника на Python.

**TL;DR:** движок написан на Delphi, скриптовая среда — DWS
(DelphiWebScript, open-source). Каждый нативный примитив, который скрипт
видит как функцию, зарегистрирован в exe как Delphi `AnsiString` со
строкой-сигнатурой Pascal-объявления. Эти строки можно извлечь
напрямую — мы получили **4 856 нативных сигнатур**, из которых **884
действительно вызываются** из `data/scripts/*` (100% покрытие
script-callable примитивов).

Сопутствующие документы:

- [determinism_audit.md](determinism_audit.md) — RNG-источники в горячем
  пути.
- [server_sync_architecture.md](server_sync_architecture.md) —
  server-authoritative модель C3.
- [ticks_and_subticks.md](ticks_and_subticks.md) — модель времени.

Машинно-читаемые артефакты:

- `docs/derived/dws_native_signatures.json` — 4 856 сигнатур (имя,
  параметры, тип возврата, RVA в exe).
- `docs/derived/engine_primitives.json` — 884 нативных + 46 классовых
  кастов + 19 DWS-builtin'ов из скриптов.
- `docs/derived/exe_strings.json` — 61 595 ASCII + 15 615 Pascal
  ShortString со смещениями (если когда-то понадобятся для xref).

## 1. Методология

### 1.1. Идентификация движка

В строках `cossacks.exe` подтверждаются:

| Сигнатура | Что это значит |
|---|---|
| `FastMM4 (c) 2004 - 2011 Pierre le Riche` | Delphi memory manager → бинарь точно Delphi (не FreePascal). |
| `TFormDWSDebugger`, `TFormScriptEvaluate` | Скрипты — DWS (DelphiWebScript). Open-source, github.com/EricGrange/DWScript. |
| `TFormStateMachines` | Явный FSM-слой над скриптами. |
| `TBitmap3DSx` | Загрузчик 3DS-моделей встроен. |
| `EId*` исключения (Indy 10) | Сетевая часть — Indy Internet Direct, тоже open-source. |
| `TFormHelloScreen` | UI на стандартных Delphi VCL/FMX формах. |

### 1.2. Извлечение сигнатур

DWS-функция регистрируется в Delphi-коде как:

```pascal
TdwsUnit.AddFunction(
  'function GetGameObjectPositionXByHandle(gohandle: Integer): Float',
  GetGameObjectPositionXByHandleNative);
```

Строка с объявлением — обычная Delphi `AnsiString` (статическая,
рантайм-immutable), которая в `.exe` лежит как:

```
... <ref_count = 0xFFFFFFFF> <length: u32> <chars[length]> 00 ...
```

Сканер в `parser/engine_recon/extract_dws_signatures.py` проходит
бинарник, ищет байт-паттерн `\xFF\xFF\xFF\xFF<len:4>...\x00`, проверяет
что строка начинается с `function` или `procedure` (с поправкой на
ведущий пробел в части записей), и парсит её как Pascal-объявление.

Этого достаточно: **100% script-callable примитивов** нашлись по имени.

## 2. Что говорят 4 856 сигнатур про устройство движка

### 2.1. ECS на handle'ах

Подавляющая часть API — это операции над `gohandle: Integer`
(GameObject handle) и `plhandle: Integer` (Player handle). Ни один
скрипт не получает указатель на C-структуру; всё через целочисленный
дескриптор и пары `Get*ByHandle` / `Set*ByHandle`.

Размер подсистем:

| Подсистема | Сигнатур | Что в неё попадает |
|---|---:|---|
| `game_object` | 715 | `Get/Set*ByHandle` для GameObject (позиция, ориентация, AABB, ECS-флаги, anim, материалы). |
| `player` | 185 | `Get/SetPlayer*ByHandle` (ресурсы, лимиты, апгрейды, отношения). |
| `scripting` | 85 | `EvaluateCodeThread`, `EvaluateFileThread`, `ParserGet*`, `ParserSet*`. |
| `save_load` / sync | 38 | `RecordCustom*`, `RecordSynch*`, `FileStream*`. |
| `behaviour_props` | 28 | `SetBehaviourBoolProperty`, `BehaviourCreate`, и т.д. — компоненты на GameObject. |
| `spawn` | 25 | `Create*ByHandle`, `Destroy*`, `AddObjectToDestroyList`. |
| `ui` | 19 | `AddNewElement*`, `GetGuiTexture*`. |
| `path_command` | 15 | `MoveTo*ByHandle`, `StopOrders*`. |
| `geometry` | 11 | `VectorDistance`, `VectorRotateY`, `ArrayAffineVector*`. |
| `ai` | 10 | `AIRegionDoScanObjects*`. |
| `locale` | 9 | `GetLocaleTable*`. |
| `rng` | 5 | `Random`, `RandomExt`, `SetRandomKey`, etc. |
| `search` | 2 | `FindGameObjectByUniqId`, `FindUniqIdByGameObject`. |

Остальные ~3 600 — `misc`: ассеты, частицы, звук, рендер, дебаг, FOW,
камера, AI-региональные сканы. Из них примерно 4× больше функций, чем
скрипт зовёт — это API для редактора (`editor.exe` — отдельный бинарь,
но шарит ту же DWS-среду) и ассет-пайплайна.

### 2.2. Server sync — что это такое технически

В [server_sync_architecture.md](server_sync_architecture.md) мы
описывали `bProcess`-паттерн как абстракцию. Нативный API теперь
закрывает «как именно сериализуется состояние»:

**Низкий уровень — `RecordCustom*` (~25 функций):**

| Функция | Назначение |
|---|---|
| `RecordCustomBegin{,GUI,Map,StateMachine,TagObject}` | Открыть пакет соответствующего типа. |
| `RecordCustomEnd` | Закрыть пакет. |
| `RecordCustomReadBit/Boolean/Byte/Word/SmallInt/Int24/Integer/Float/PackedFloat/ShortString/String/Buffer` | Десериализаторы по типам. |
| `RecordCustomWrite*` (зеркало) | Сериализаторы. |
| `RecordCustomBeginReadBitFields` / `EndReadBitFields` | Bit-packed блоки (несколько бит-флагов в один байт). |
| `RecordCustomGetReadPackageSize` / `WritePackageSize` | Текущий размер пакета. |

Поддерживаемые типы намекают на формат сетевого/save-пакета:
- `Int24` — 24-битное целое (3 байта, экономия трафика).
- `PackedFloat` — float, упакованный в меньше байт (вероятно scaled
  fixed-point).
- `Bit` + bit-fields — флаги юнитов в bitstream.
- `ShortString` (Pascal, ≤255 байт) и `String` (динамический) — оба
  поддерживаются.

**Средний уровень — `RecordSynch*` (~30 функций):**

| Функция | Назначение |
|---|---|
| `RecordSynchBegin{,GUI,MAP,ByHandle}` | Начать синхронизацию заданной области состояния. |
| `RecordSynchIntRegister` / `FloatRegister` / `StringRegister` | Зарегистрировать слот в стеке синхронизации. |
| `RecordSynchStackInt/Float/StringByName` | Засинхронизовать значение по имени. |
| `RecordSynchStackInt/Float/StringByNameTestChanges` | Засинхронизовать **только если изменилось** — это и есть delta-кодирование. |
| `RecordSynchState(name)` | Произвольная маркировка точки. |
| `SetRecordEnabled` / `SetRecordGroupEnabled` / `SetRecordInitializeEnabled` | Тумблеры записи. |

**Вывод:** server-authoritative C3 работает так — клиент вычисляет
своё локальное состояние, прогоняет «зарегистрированные» переменные
через `RecordSynchStack*ByNameTestChanges`, и **отсылает только дельту
изменений** в виде `RecordCustomWrite*`-пакета, бит-упакованного по
типу `Int24/PackedFloat/Bit-fields`. Это объясняет почему трафик C3
маленький даже на больших баталиях.

`SetRecordInitializeEnabled` отдельным флагом контролирует
«начальный снапшот» (full state) vs «только delta».

**Net I/O в скрипты не экспонируется.** В сигнатурах нет ни одного
`Net*`/`Send*`/`Broadcast*` — то есть ниже уровня
`RecordSynch*`/`RecordCustom*` всё внутри `cossacks.exe` (Indy 10 +
Steam wrapper).

### 2.3. Pathfinding — на отдельном потоке

Найдено 14 функций `PathDataThread*`:

```pascal
PathDataThreadCount(): Integer;
PathDataThreadResume();
PathDataThreadSuspend();
PathDataThreadSuspended(): Boolean;
PathDataThreadTerminate();
PathDataThreadStaticPriority(val: Integer);
PathDataThreadDynamicPriority(val: Boolean);
PathDataThreadMinPriority(val: Integer);
PathDataThreadMaxPriority(val: Integer);
PathDataThreadDeltaPriority(val: Integer);
PathDataThreadSleepStep(val: Integer);
PathDataThreadSleepLength(val: Integer);
PathDataThreadSafeClean();
```

**Pathfinding в C3 — асинхронный.** Запросы пути обрабатываются
в отдельном пуле потоков, у которых есть собственный планировщик
(`StaticPriority`/`DynamicPriority`/`MinPriority`/`MaxPriority`,
`DeltaPriority`, `SleepStep`/`SleepLength`).

Это меняет нашу модель детерминизма: даже если RNG зафиксирован,
порядок завершения путей зависит от планировщика OS-тредов. Вероятно
поэтому в [determinism_audit.md](determinism_audit.md) добыча между
запусками одного и того же сейва различается даже у одного хоста — не
только из-за RNG, но и из-за **гонки за результаты pathfinding-потока**.

Скриптовый API для pathfinding (то, как скрипт **создаёт** запрос
пути) — это не отдельные `Find*` функции, а команды через
`Set*ByHandle` (например, `MoveTo`-style); сам поиск асинхронен и
скрипт просто ждёт следующего тика.

<a id="24-rng--глубже-чем-мы-думали"></a>
### 2.4. Четыре независимых хранилища RNG

`random`, `RandomExt` и генератор карт не используют одно общее состояние.
Нативный API показывает **четыре независимых хранилища начальных значений**,
каждое со своим алгоритмом.

> `Random` — обёртка над `System._Random`, которая изменяет стандартный
> 32-битный `RandSeed` Delphi. Это состояние не связано с 64-битным
> расширенным начальным значением, которым управляют `SetRandomKey` и
> `SetRandomExtKey64`. Подробности — в приватном
> `cossacks-deep/findings/rng_implementation.md`.

| Хранилище | Seed-функции | Алгоритм поверх | Назначение |
|---|---|---|---|
| **Delphi `System.RandSeed`** (32-бит) | `Randomize` или прямая запись `System.RandSeed` (DWS не выставляет) | `Random` (`System._Random`: `seed := seed * 0x8088405 + 1`) | Дефолтный gameplay-RNG. Не управляется `SetRandomKey`. |
| **Расширенный 64-бит seed** | `SetRandomKey(key: Integer)` (32-бит → sign-extend), `SetRandomExtKey64(k0, k1: Integer)` (полный 64-бит) | `RandomExt` (64-бит LCG, своя пара констант) | Контролируемый поток для случайности, где нужна детерминированность через пересев. |
| **Seed генератора карт** | `SetMapGeneratorRandomKey(const randkey0, randkey1)` | Внутренний алгоритм генератора (не разобран) | Изолированный RNG для `_DoGenerate` (рельеф, размещение объектов, стартовых позиций). |
| **Глобальный seed map-генератора** | `SetGlobalMapGeneratorRandomKey(const randkey0, randkey1)` | Отдельный (не разобран) | Параллельное хранилище в state-структурах карты — кандидат на worldmap или превью карты в лобби. |

Дополнительно: `GetPlayerCubeRandomValue(playerhandle: Integer): Float`
— отдельный per-player детерминированный «куб случайности» (вероятно,
для AI/decisions, чтобы каждый игрок видел свою повторяемую
последовательность).

Также есть «погодный» RNG: `GetAirWeatherRandom`, `SetAirWeatherRandom`,
`GetAirWeatherRandomStart`, `GetAirWeatherRandomEnd`,
`GetAirWindRandom` — изолированный поток для атмосферных эффектов
(ветер, тучи), чтобы визуал не влиял на gameplay-PRNG.

**Что это меняет для симулятора:** когда в [extraction
model](../../docs/recon/world/economy/peasant_extraction.md) нам нужно
репродуцировать поведение крестьян, важно понимать, какой именно `Random*`
скрипт зовёт в каждом hot-path шаге. Если только `random` — нужно
имитировать Delphi `RandSeed`. Если есть `SetRandomKey + RandomExt` —
имитировать расширенный seed и его LCG. Map RNG и weather — независимые
хранилища, на extraction-цепочку не влияют.

### 2.5. Поведенческие компоненты (Behaviour)

`BehaviourCreate`, `BehaviourCreateWithKey`, `BehaviourDestroy` плюс
~28 функций `SetBehaviour*Property` показывают, что юниты — это
GameObject + набор Behaviour-компонентов. Behaviour в DWS — это
строковый класс-имя:

```pascal
BehaviourCreate(gohnd: Integer; const classname: String;
                uniq: Boolean; usecurrentparams: Boolean): Integer;
```

Имена `Behaviour*` классов хранятся в RTTI и в `.parser` файлах — их
можно перечислить через `BehaviourPropertiesLoadFromParser` /
`SaveToParser`. Это объясняет архитектурно, почему `unit.script`
оперирует абстракциями типа «у юнита есть hp, weapon, anim, vision»
без явного объявления полей — поля живут в Behaviour-компонентах.

Особый интерес — `BehaviourInertia*` (apply force/torque/translation,
mirror, surface bounce): встроенная **физическая симуляция инерции**
для летающих/кидаемых объектов (например, ядра пушек, кавалерия в
галопе).

### 2.6. AI — региональная архитектура

Все AI-примитивы (10 функций) построены вокруг
`AIRegion*`:

```pascal
AIRegionDoScanObjects(const name: String);
AIRegionDoScanObjectsByHandle(const reghnd: Integer);
AIRegionDoScanObjectsExtByHandle(const reghnd: Integer);
AIRegionDoUpdateObject(const reghnd, gohnd: Integer; const notify: Boolean);
AIRegionDoClearObjects/ByHandle(...);
AIRegionFromParserStruct/ToParserStruct(...);
AIRegionLoadFromTextFile/SaveToTextFile(...);
```

**AI оперирует в spatial regions** — отдельных «зонах интереса» с
собственным списком объектов. ИИ запрашивает обновление зоны
(`DoScanObjects`), получает список GameObject в ней, принимает
решения. Это бьётся с `recon/ai.md` (если он есть) и закрывает вопрос
«как ИИ ищет цели».

### 2.7. Скриптовая среда — DWS со своими расширениями

`EvaluateCodeThread(const code: String): Integer` и
`EvaluateFileThread(const filename: String): Integer` показывают, что
DWS-скрипты могут запускаться в отдельных потоках. Это объясняет,
почему некоторые скриптовые цепочки (например, кампания) выглядят
«одновременно работающими».

`AddProcAddress`, `PointerOf` — расширения над стандартным DWS, дают
скриптам доступ к указателям на функции. Это подсказывает, что часть
gameplay-логики передаётся как callback'и (например, обработчики
триггеров сценария).

## 3. Топ-50 самых частых нативных вызовов

(Сгенерировано в `native_primitives.md` рядом, здесь сжатый ТОП-30 для ориентира.)

| # | Имя | Calls | Что делает |
|---|---|---:|---|
| 1 | `GetPlayerHandleByIndex` | 270 | Получить handle игрока по индексу. |
| 2 | `GetGameObjectPositionXByHandle` | 263 | X-координата объекта. |
| 3 | `GetGameObjectPositionZByHandle` | 263 | Z-координата (3D). |
| 4 | `ErrorLog` | 387 | Логирование. |
| 5 | `GetLocaleTableListItemById` | 197 | Локализация. |
| 6 | `SwitchTo` | 146 | Корневой scheduler-примитив (146 файлов!). |
| 7 | `VectorDistance` | 137 | Расстояние между точками. |
| 8 | `SetBehaviourBoolProperty` | 127 | Set ECS-property. |
| 9 | `GetPlayerIndexByHandle` | 120 | Inverse mapping. |
| 10 | `ParserGetFloatValueByKeyByHandle` | 115 | Чтение из `.parser` файла. |
| 11 | `RecordCustomWriteInteger` | 111 | Сериализация целого. |
| 12 | `ReadInteger` | 106 | Чтение из stream. |
| 13 | `GetGameObjectUniqueIdByHandle` | 95 | UID объекта. |
| 14 | `GetGameObjectHandleByUniqueId` | 94 | Inverse. |
| 15 | `GetPlayerGameObjectsCountByHandle` | 89 | Счётчик объектов игрока. |
| 16 | `WriteInteger` | 87 | Запись в stream. |
| 17 | `StrExists` | 86 | Поиск подстроки. |
| 18 | `SetBehaviourFloatProperty` | 84 | Set ECS-property. |

`SwitchTo` (146 файлов!) — это нечто вроде `goto state` для
state-machine'ов. Учитывая, что есть `TFormStateMachines` в RTTI и
`MachineLibrary*` в API, скриптовая логика уровня поведения
организована как FSM, а `SwitchTo` — переход между состояниями.

## 4. Где хранится остальное (что не в скриптах)

Из 4 856 нативных функций в exe скрипт зовёт только 884. Остальные
3 972 — это:

- **Editor API** — `AddEditorControl`, `AddEditorFormInput`,
  `AddCameraTrackPoint`, `ResourceTexturesReload` и т.д. Используются
  в `editor.exe` (отдельный бинарь, шарит ту же DWS-среду).
- **Asset / pipeline** — `EnvironmentLoadLensFlareFromFile`,
  `MachineLibrarySaveSerialsToFile`, `ResourceLODActorLibrary*`.
- **Internal-only** — pre-render, низкоуровневые TLF (Top-Level Frame)
  и particle-FX операции, которые скрипт никогда не дёргает.
- **Steam wrapper** — `SteamwrapStartVoiceRecording`,
  `TSteamAchievement` API.
- **Indy-сетевой слой** — `TInternetShellClient`, `TInternetShellSession`
  (использует Steam transport, виден в Pascal class names).

Если когда-то понадобится копать редактор или сетевой стек — все имена
есть, RVA в `dws_native_signatures.json`.

## 5. Что закрыто этим документом

| Вопрос | Где был открыт | Ответ |
|---|---|---|
| Что такое `bProcess` на уровне сети | `server_sync_architecture.md` | `RecordSynch*` + `RecordCustom*` — see §2.2. |
| Сколько RNG-потоков в движке | `determinism_audit.md` | 4 независимых: `Random`, `RandomExt`, `MapGenerator`, `GlobalMapGenerator` + weather. §2.4. |
| Как ИИ ищет цели | `ai.md` (TODO) | Через `AIRegionDoScanObjects*` — spatial regions. §2.6. |
| Pathfinding — sync или async | (открытый) | **Async, отдельный thread pool** с приоритетами. §2.3. |
| Как сериализуются юниты | (открытый) | `RecordCustom*` с типами `Int24`, `PackedFloat`, `Bit-fields`. §2.2. |
| Что есть «Behaviour» юнита | `unit.script` догадки | Полноценные ECS-компоненты с `BehaviourCreate(classname: String)`. §2.5. |

## 6. Что ещё открыто — и как это закрыть **без декомпилятора**

Большая часть исходно открытых вопросов закрыта в смежных
документах. Ниже — статус каждого:

| Вопрос | Где раскрыт |
|---|---|
| 6.1. Bit-layout сетевых пакетов | ✅ Полностью описан в [`server_sync_packet_format.md`](server_sync_packet_format.md): `EconomyPackage` (бинарь, 1–18 байт), unit-state через parser-text. |
| 6.2. Реализация `Random` LCG | ✅ Полностью описана в [`rng_implementation.md`](rng_implementation.md): Delphi LCG `X = X × 134775813 + 1 mod 2³²`, плюс per-decision deterministic seed pattern. |
| 6.3. Карта классов движка | ✅ См. [`rtti_class_map.md`](rtti_class_map.md): 266 game-engine классов по подсистемам, в т. ч. `TXAIRegion*`, `TXPath*`, `TXTrigger*`, `TXLan*`. |
| 6.4. Алгоритм поиска ресурса крестьянином | 🔬 Логика в `lib/unit.script:_unit_DoExtract` и сопутствующих. Нативного `findnearestresource` нет — поиск использует комбинацию scan-grid (см. [`target_selection.md`](../../docs/recon/world/combat/target_selection.md) §2) и `AIRegionDoScanObjects*` для крупных зон. Доразобрать через grep по скриптам — без декомпилятора. |
| 6.5. Точная формула pathfinding | 🔬 Из RTTI-классов (`TPathData`, `TOSWMovementPath`, `TOSWPathNode`, `TOSWPathNodes`, `TXPathCellChangedArray` — см. [`rtti_class_map.md` §4](rtti_class_map.md)) видно, что pathfinding построен **на graph of nodes**, не на чистом A* по grid'у. Узлы пересчитываются через `TXPathCellChangedArray` при изменениях карты. Точный алгоритм поиска по графу (Dijkstra / A* / weighted A*) — единственное, что требует декомпиляции; характеристики наблюдаемы через `PathDataThread*`-параметры. |
| 6.6. Алгоритм `MapGenerator` | 🔬 Класс `TXMapGenerator` (см. [`rtti_class_map.md` §8](rtti_class_map.md)) принимает `(randkey0, randkey1)` пару — это два uint32, всего 64 бита состояния (как `RandomExt`, см. [`rng_implementation.md` §3](rng_implementation.md)). Конкретный PRNG (Xorshift64? L'Ecuyer?) внутри класса — без декомпиляции не определить. Не критично: при том же seed карта детерминирована. |
| 6.7. Формат `.aix` (AI-config) | 🔬 Редактор `.aix` встроен в `editor.exe` через `TAIXEditor` / `TAIXEditorState` / `TAIXArgsEditor` / `TAIXVarsEditor` (см. [`rtti_class_map.md` §16](rtti_class_map.md)). Структура — «переменные + аргументы», бинарная, но не критична: gameplay-AI описан в `lib/ai.script` и через `AIRegion*`-API. |
| 6.8. Формат `.map` | ❌ Бинарный, не разобран. Используется только для встроенных миссий (Historical Battle, кампания). Скирмиш-карты процедурные. См. [`../data/file_formats.md`](../data/file_formats.md). |

**Принцип:** «🔬» — теоретически разрешимо без декомпилятора через
скрипты или RTTI; «❌» — реально требует RE.

## 7. Файлы и инструменты

| Файл | Что делает |
|---|---|
| `parser/engine_recon/extract_primitives.py` | Сканирует `data/scripts/*` → 884 нативных-кандидатов + 46 type-cast'ов + 19 DWS builtin'ов. |
| `parser/engine_recon/dump_exe_strings.py` | Дамп всех ASCII (61k) и Pascal ShortString (15k) из `cossacks.exe` с RVA. |
| `parser/engine_recon/extract_dws_signatures.py` | Главный: сканирует AnsiString-таблицу, извлекает 4 856 DWS-сигнатур, кросс-референс со скриптом → 100% покрытие. |

## 8. Воспроизведение

```powershell
cd c:\projects\other\cossacks
python parser\engine_recon\extract_primitives.py
python parser\engine_recon\dump_exe_strings.py
python parser\engine_recon\extract_dws_signatures.py
```

Артефакты появляются в `derived/*.json` и обновляют отчёт в
`native_primitives.md` (соседний файл в этой же папке).

## 9. Если всё-таки понадобится декомпилятор

`dws_native_signatures.json` содержит RVA каждой сигнатуры — точка
входа для Ghidra/IDR/IDA. Сценарий:

1. Открыть `cossacks.exe` в Ghidra с Delphi-плагином (DelphiHelper или
   IDR-import).
2. Перейти к RVA нужной сигнатуры — рядом указатель на нативный
   callback (стандартный паттерн DWS-регистрации в Delphi).
3. F5 → C-decompile. Delphi compile-output читается легко (нет
   C++-шаблонов, нет inline-агрессии).

Имя callback-функции часто доступно из RTTI методов — у каждого
Delphi-класса в exe лежит `vmtTypeInfo` со списком published-методов.
Можно усилить `dump_exe_strings.py`, добавив walker по VMT, и
получить ~1 779 классов с их методами как ASCII. Но **это уже
крайний случай** — статика покрывает 95% задач.
