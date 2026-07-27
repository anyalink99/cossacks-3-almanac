# Структура скриптовой среды Cossacks 3

Где какая логика лежит в `data/scripts/`, как файлы попадают в
скриптовый VM, какие у них точки входа.

## 1. Что такое «скрипт» в C3

Cossacks 3 использует **DWS** (DelphiWebScript, open-source:
[github.com/EricGrange/DWScript](https://github.com/EricGrange/DWScript))
как встроенный скриптовый язык. Синтаксис — Object Pascal:

```pascal
function _unit_GetTObj(handle : Integer) : TObj;
begin
   Result := TObj(GetGameObjectTagByHandle(handle));
end;
```

Игра предоставляет скриптам **4 856 нативных функций** — готовый API
к движку (см. [`../engine/native_api.md`](../engine/native_api.md)).
Скрипты их вызывают, передают handle'ы объектов, читают и пишут
свойства. Сама же gameplay-логика (что делать с этими handle'ами) —
живёт в `.script`-файлах.

Это значит: **большая часть «правил игры» — в скриптах**, а движок
предоставляет ECS-runtime, render, pathfinding, sync и I/O. Это
делает игру очень моддабельной (mod loader `modman.exe`).

## 2. Файлы и форматы в `data/scripts/`

```
data/scripts/
├── dmscript.global           Глобальные константы (.parser-формат)
├── dmscript.source           Начальное состояние глобальных vars
├── common.aix                AI-константы (бинарный)
├── common.inc                ?
├── resource.script           Top-level: загрузка локали
├── env/env.inc               Environment variables
├── lib/                      29 .script-файлов — библиотеки логики
│   ├── unit.script           (534 KB) — поведение юнитов и зданий
│   ├── country.script        (342 KB) — нации, апгрейды, ростер
│   ├── classes.script        (242 KB) — record-типы и helpers
│   ├── miscext2.script       (198 KB) — продвинутый misc
│   ├── misc.script           (237 KB) — общие helpers
│   ├── gui.script            (162 KB) — UI-логика
│   ├── player.script         (138 KB) — состояние игрока
│   ├── ai.script             ( 90 KB) — поведение ИИ
│   ├── serial.script         ( 91 KB) — сериализация
│   ├── weapon.script         ( 66 KB) — оружие/снаряды
│   ├── miscext.script        ( 70 KB)
│   ├── movie.script          ( 45 KB) — кат-сцены
│   ├── scenario.script       (200 KB) — сценарии и кампания
│   ├── control.script        ( 27 KB) — выделение/команды
│   ├── steam.script          ( 27 KB) — Steam wrapper
│   ├── sound.script          ( 26 KB)
│   ├── profile.script        ( 26 KB)
│   ├── squad.script          ( 23 KB) — отряды
│   ├── ui.script             ( 22 KB)
│   ├── pfx.script            ( 17 KB) — particles
│   ├── res.script            ( 12 KB) — ресурсы
│   ├── map.script            ( 11 KB)
│   ├── miscext3.script       ( 10 KB)
│   ├── init.script           ( 10 KB) — инициализация
│   ├── scenarioeditor.script ( 10 KB)
│   ├── net.script            (  6 KB) — multiplayer state
│   ├── group.script          (  5 KB)
│   ├── parser.script         (  2 KB) — обёртка над DWS Parser
├── misc/                     Дополнительные .inc
├── progress/progress.inc
├── units/<sid>/              Per-unit `.parser` configs
├── user/user.inc
└── env/env.inc
```

**Расширения и формат:**

- `.script` — DWS source. Object Pascal с расширениями DWS.
  Кодировка `cp1251` (русский комментарий обычное дело).
- `.global`, `.source`, `.inc` — `.parser`-формат (текстовый
  иерархический конфиг с `section.begin / struct.begin / [*] = ;...`).
  Парсится не DWS, а нативным `Parser*` API.
- `.aix` — бинарный AI-конфиг.

## 3. Как скрипты попадают в VM

В отличие от Lua/Python с явным `require/import`, у DWS в C3 **нет
`uses`-директив в файлах библиотек**. Загрузка идёт через **конфиги
сущностей** (`.parser`-файлы) и движок:

| Поле в .parser | Что делает |
|---|---|
| `DMScriptGlobalFileName` | Глобальные константы (`dmscript.global`). Грузится один раз при старте. |
| `OnLoadScriptFileName` | Скрипт, который вызывается когда сущность создаётся / загружается. |
| `startscript` | Скрипт, исполняемый сразу при инициализации игры. |
| `ScenarioStateName` | Имя скрипта для конкретного состояния FSM сценария. |
| `OnLoadScript` (inline) | Inline-DWS-код в .parser. |

Все эти поля найдены в `cossacks.exe` как RTTI-свойства DWS-классов
сценариев (RVA `0x34fc84` для `DMScriptGlobalFileName` и т.д., см.
[`derived/exe_strings.json`](../../derived/exe_strings.json) если
нужны точные адреса).

**Практический эффект:** все `lib/*.script` загружаются неявно — они
ссылаются друг на друга через имена функций (`_unit_*`, `_misc_*`),
и DWS-компилятор разрешает ссылки в момент компиляции всего набора.
Каждый `.script` — это **unit-библиотека функций без явных импортов**.

## 4. Namespacing-конвенция

C3 использует Pascal-style namespace через подчёркивания:

| Префикс | Файл | Содержимое |
|---|---|---|
| `_unit_*` | `unit.script` | Логика юнитов и зданий: `_unit_DoExtract`, `_unit_SearchEnemy`, `_unit_GetTObj`. |
| `_misc_*` | `misc.script`, `miscext.script`, `miscext2.script` | Общие helpers: `_misc_DoDamage`, `_misc_GetPickedUnitHandle`. |
| `_country_*` | `country.script` | Нации, апгрейды: `_country_GetSIDByID`, `_country_DoUpgrade`. |
| `_player_*` | `player.script` | Состояние игрока: `_player_GetTPlayerArgs`, `_player_DoStartingResources`. |
| `_ai_*` | `ai.script` | ИИ-логика: `_ai_IsEnemiesExists`, `_ai_DoTickAggressive`. |
| `_net_*` | `net.script` | Multiplayer flags: `_net_IsClient`, `_net_IsServer`. |
| `_parser_*` | `parser.script` | Обёртка над DWS-Parser API. |
| `_gui_*` | `gui.script` | UI: `_gui_GetTop`, `_gui_OnElementClick`. |
| `_squad_*` | `squad.script` | Отряды: `_squad_GetOfficer`, `_squad_DoFormation`. |
| `_weapon_*` | `weapon.script` | Оружие/снаряды: `_weapon_GetTProj`. |
| `_res_*` | `res.script` | Ресурсы: `_res_GetTRes`. |
| `_init_*` | `init.script` | Инициализация при старте игры. |
| `_map_*` | `map.script`, `miscext2.script` | Логика карты: `_map_Init`, `_map_RestoreSettings`. |
| `_control_*` | `control.script` | Команды юнитам: `_control_DeselectAllUnits`. |
| `_movie_*` | `movie.script` | Кат-сцены: `_movie_SaveCamera`, `_movie_DoPlay`. |
| `_pfx_*` | `pfx.script` | Particles. |
| `_sound_*` | `sound.script` | Звук: `_sound_GetIndexesByTag`. |
| `_profile_*` | `profile.script` | Профиль игрока. |
| `_group_*` | `group.script` | Группы (брандеры). |

В сумме ~1 600 функций определены в скриптах (см.
`derived/engine_primitives.json` поле `defined`).

## 5. Что в каждом главном файле

### `lib/unit.script` (534 KB, 250 функций) — главный

Поведение всех юнитов и зданий. Содержит огромный `case sid of`
блок: для каждого сидевого ID юнита/здания — соответствующая
ветка с настройкой свойств (HP, weapon, animations, behaviors).

**Ключевые точки:**

- `_unit_GetTObj(handle) : TObj` — получить record-обёртку из handle.
- `_unit_DoExtract` — крестьянская добыча, FSM walk → work → return.
- `_unit_SearchEnemy*` — поиск цели в scan-grid (см.
  [`docs/recon/world/target_selection.md`](../../docs/recon/world/combat/target_selection.md)).
- `_unit_DoDamage` — применение урона.
- `_unit_OnTickXxx` — per-tick обработчики FSM-состояний.

### `lib/country.script` (342 KB, 64 функции) — нации

Большой `case cid of`-блок для 21 нации. Для каждой:

- Список доступных юнитов (`AddCountryUnit`).
- Список зданий (`AddCountryBuilding`).
- Дерево апгрейдов (`SetUpgStruct`, `AddUpgradePack`).
- Особенности (например, у Pol — пехотный пикинёр, у Ven — лёгкая кавалерия).

Парсится автоматически в `parser/parse_country.py` и
`parser/simulate_upgrades.py`.

### `lib/classes.script` (242 KB, 438 функций) — типы

Record-определения и их helpers. Содержит обёртки `TObj`, `TSquad`,
`TArmy`, `TWeapon`, `TPlayerArgs`, `TIntegerList`, etc. — всё, что
скрипты используют как типы. Эти record'ы не настоящие Delphi-classes
(это «тонкие» wrapper'ы вокруг `Integer` handle), но через DWS они
ведут себя как объекты.

### `lib/player.script` (138 KB) — игрок

Состояние одного из 12 игроков. Стартовые ресурсы, лимиты населения,
потребление food/gold, отношения с другими игроками, флаги
`bfamine`/`brebellion`.

### `lib/ai.script` (90 KB) — ИИ

ИИ-противник: тик каждые 2.4 g-сек, build order, выбор цели для
агрессии. Использует `AIRegion*` (см.
[`docs/recon/systems/ai_behavior.md`](../../docs/recon/systems/ai_behavior.md)
и [`../engine/native_api.md` §2.6](../engine/native_api.md)).

### `lib/serial.script` (91 KB) — сериализация

Сохранение и загрузка состояния. 108 процедур типа
`DoSerializeUnit`, `DoSerializePlayer`. Использует нативные
`RecordCustomWrite*`/`RecordSynch*` (см.
[`../engine/native_api.md` §2.2](../engine/native_api.md)).

### `lib/scenario.script` (200 KB) — сценарии

Кампания и Historical Battles. Триггеры (`TScenarioTrigger`),
условия (`TScenarioCondition`), действия (`TScenarioAction`),
результаты (`TScenarioResult`).

### `resource.script` (top-level) — точка входа локали

Не в `lib/`. Не библиотека, а **исполняемый скрипт** (без `function/
procedure`-deflarations, прямой код). При старте грузит
`data/locale/lang.loc`, выбирает язык через Steam (`SteamwrapGetSteamUILanguage`),
заполняет `resource.lib` парсер. См. сам файл — он короткий (~2 KB).

## 6. Точки входа в скриптовый VM

Из exe-анализа найдены три класса entry point'ов:

1. **`startscript`** — скрипт, исполняемый при создании сессии.
   Используется для одноразовой инициализации.
2. **`OnLoadScriptFileName`** — скрипт, привязанный к классу
   сущности. Вызывается каждый раз при создании / десериализации
   объекта этого класса.
3. **`ScenarioStateName`** — скрипт-обработчик одного состояния FSM.
   Сценарий = граф из таких состояний.

Кроме того, `lib/*.script`-функции вызываются:

- Из других скриптов через DWS function-call (compile-time linking).
- Из движка через **callback-имена**: например,
  `BehaviourCreate(gohnd, 'WoodChopperBehaviour')` ссылается на
  Behaviour-класс, у которого есть скриптовый callback с таким
  именем (через RTTI Delphi-класса в exe).

## 7. Глобальные константы и состояние

### `dmscript.global` (86 KB, 2 400 строк)

В формате `.parser` (не DWS!). Содержит ВСЕ `gc_*`-константы:
- `gc_statetag_*` — биты FSM-состояния (см. файл).
- `gc_obj_usage_*` — типы юнитов (`lightinfantry`, `cavalry`, ...).
- `gc_obj_weapon_kind_*` — типы оружия (`pike`, `sword`, `bullet`, ...).
- `gc_resource_type_*` — типы ресурсов.
- `gc_time_to_frames = 32` — кадров в игровой секунде.
- `gc_pixels_to_tile = 53.3333` — конверсия дальности.
- И сотни других.

Загружается один раз при старте через
`DMScriptGlobalFileName`-поле. После этого `gc_*`-имена доступны как
именованные DWS-константы во всех скриптах.

### `dmscript.source`

Тоже `.parser`-формат. Содержит **начальное состояние всех
глобальных vars** (имена начинаются на `g`: `gint_*`, `gbool_*`,
`gstring_*`). При старте новой игры всё инициализируется отсюда.

## 8. Кодировка и язык

- `.script` — `cp1251` (Windows-1251). Комментарии часто на русском
  (русским разработчиком GSC).
- `.parser` (`.global`, `.source`, `.inc`) — тоже `cp1251`.
- DWS case-insensitive: `_unit_GetTObj` и `_UNIT_gettobj`
  эквивалентны (важно для нашего парсинга — мы лоуэркейсим всё).

## 9. Полезные срезы

Все эти данные доступны машинно в [`derived/`](../../derived/):

| Файл | Что содержит |
|---|---|
| `engine_primitives.json` | 884 native-вызова из скриптов + 46 type-cast'ов + 19 DWS builtin'ов с частотами и списками файлов. |
| `dws_native_signatures.json` | 4 856 native-сигнатур из exe (имя, типы, RVA). |
| `tech_tree.json` | Граф `nation × upgrade × prerequisite`, выжатый из `country.script` через `parser/build_tech_graph.py`. |
| `canonical_terms.json` | Канонические русские названия из `data/locale/`. |

## 10. Как читать скрипт без знания Pascal

Шорткат для чтения C3-скриптов:

| DWS / Pascal | Эквивалент в C-style |
|---|---|
| `:=` | `=` |
| `=` | `==` |
| `<>` | `!=` |
| `var x : Integer = 0;` | `int x = 0;` |
| `begin ... end;` | `{ ... }` |
| `if cond then begin ... end else begin ... end;` | `if (cond) { ... } else { ... }` |
| `for i := 0 to N-1 do begin ... end;` | `for (int i=0; i<N; i++) { ... }` |
| `case x of 1: ... ; 2: ... ; else ... end;` | `switch (x) { case 1: ... break; case 2: ... break; default: ... }` |
| `function F(a : Integer) : Boolean;` | `bool F(int a)` |
| `procedure P(a : Integer);` | `void P(int a)` |
| `Result := value;` | `return value;` (но без явного return) |
| `TObj(handle).hp` | `((TObj*)handle)->hp` (тонкий type-cast) |

**Тонкости C3-скриптов:**

- `TObj`/`TSquad`/`TArmy` — это НЕ настоящие классы, а type-cast'ы
  над `Integer` handle. Все «методы» — нативные функции
  `Get*ByHandle(int)`/`Set*ByHandle(int, ...)`.
- Нет ООП-наследования. Есть только records и handle'ы.
- `random` и `RandomExt` — глобальные RNG-функции, не методы.
- Нет автоматической памяти — все «объекты» живут в движке,
  скрипт держит только Integer-handle'ы.

## Дальнейшее чтение

- [Технический разбор захвата](capture_mechanics_evidence.md) — полный
  пример проверки одной игровой механики по скриптам, включая псевдокод и
  ссылки на строки источников.
- [Технический разбор очереди производства](production_queue_evidence.md) —
  внутренние типы приказов, формула возврата и точки вызова.
- [Технический разбор голода и бунта](hunger_and_rebellion_evidence.md) —
  пороги состояний, вероятности и формула потребления.
- [Техническая модель добычи ресурсов](peasant_extraction_evidence.md) —
  формулы рабочего цикла, точки сдачи и расчёты шаблонов карты.
- [Технический разбор улучшений](upgrades_application_evidence.md) —
  внутренние типы эффектов, порядок применения и формулы.
- [Технический разбор зданий](building_mechanics_evidence.md) — маски
  столкновений, рабочие точки, разрушение и возврат ресурсов.
- [`../engine/native_api.md`](../engine/native_api.md) — что движок предоставляет скриптам (4 856 native-функций, разбитых по подсистемам).
- [`../data/layout.md`](../data/layout.md) — что лежит в `data/`, рядом со скриптами.
- [DWS на GitHub](https://github.com/EricGrange/DWScript) — open-source реализация языка, можно читать как референс.
