# Internals — техническое устройство Cossacks 3

Эта папка — **не справочник для игрока**. Здесь живут документы про
то, как игра устроена изнутри: бинарь движка, скриптовая среда DWS,
структура `data/` каталога, форматы файлов. Если ты пришёл узнать
«сколько HP у мушкетёра» — это не сюда; это в [`docs/`](../docs/).

Сюда попадает всё, что:

- описывает движок (`cossacks.exe`) — Delphi/DWS/Indy/FastMM4;
- описывает структуру скриптов (`data/scripts/*`) — какой файл за
  что отвечает, как они вызывают друг друга;
- описывает форматы и расположение файлов в `data/` (`.parser`,
  `.pattern`, `.aaf`, локали, генерация карт);
- закрывает «как именно» работают вещи, у которых в `docs/recon/`
  описан только «что».

## Структура

| Раздел | Что внутри |
|---|---|
| [engine/](engine/) | Бинарь, скриптовый VM, сетевая модель, тики, RNG. |
| [scripts/](scripts/) | Структура `data/scripts/*` — load order, точки входа, что в каждом файле. |
| [data/](data/) | Структура `data/`: подпапки, форматы файлов (`.parser`, `.pattern`, `.aaf`). |

## engine/

Реверс-инжиниринг через статический анализ `cossacks.exe` — без
Ghidra/IDA, только через парсинг бинарника на Python.

| Файл | Что внутри |
|---|---|
| [engine/native_api.md](engine/native_api.md) | Главный документ. **4 856 native DWS-сигнатур** (имя, типы аргументов, RVA), извлечены прямо из exe через AnsiString-паттерн `\xFF\xFF\xFF\xFF<len><chars>\x00`. 100 % покрытие 884 примитивов, которые скрипт реально вызывает. Подсистемы (`game_object`, `player`, `save_load`, `path_command`, …). |
| [engine/native_primitives.md](engine/native_primitives.md) | Машинно-сгенерированный быстрый поиск: топ-50 + 10 примеров на подсистему. |
| [engine/rtti_class_map.md](engine/rtti_class_map.md) | Карта **1 779 Delphi-классов** в exe по подсистемам: `TXGameObject`, `TXBehaviour*` (22 класса), `TXAIRegion*` (5), `TXPath*` / `TPathData` (6), `TXTrigger*` (8), `TXStateMachine*` (9), `TXLan*` (8 — multiplayer), `TXMapGenerator`, `TXPattern*` (25), `TAIX*` (4 — редактор `.aix`) и т. д. |
| [engine/determinism_audit.md](engine/determinism_audit.md) | RNG-аудит: какие RNG-функции используются в горячем пути добычи и боя, что персистится, мод-loader готовность. |
| [engine/rng_implementation.md](engine/rng_implementation.md) | Реализация `Random` (Delphi LCG `X = X × 134775813 + 1 mod 2³²`) и `RandomExt` (64-бит LCG поверх **общего с `Random`** глобального seed'а). Главный паттерн: per-decision deterministic seed. RE-валидировано через приватный `cossacks-deep`. |
| [engine/server_sync_architecture.md](engine/server_sync_architecture.md) | C3 — server-authoritative (не lockstep). Net modes, sync-периоды, паттерн `bProcess`. |
| [engine/server_sync_packet_format.md](engine/server_sync_packet_format.md) | Bit-layout сетевых пакетов: `EconomyPackage` (бинарь 1–18 байт) + parser-text для unit-state. |
| [engine/ticks_and_subticks.md](engine/ticks_and_subticks.md) | Модель времени: real / game / frames. Главный progress-loop. Sub-tick state-machine intervals (135 мс у крестьян, 100 мс у юнитов). |
| [engine/animation_system.md](engine/animation_system.md) | Animation system: формат `.aaf` (1 382 трека) и `.acl` (FSM-граф циклов), `refspeed.acl` (скорости движения по классам), `OnAclAnimationReachedAttack` callback (момент удара), `_unit_ApplyWeaponCost` / `ApplyAttackPause`, RNG-фильтр звуков выстрела. |

## scripts/

Структура `data/scripts/*` — где какая логика лежит, как файлы
загружаются, какие точки входа.

| Файл | Что внутри |
|---|---|
| [scripts/structure.md](scripts/structure.md) | Load order, главные `.script` файлы и их назначение, точки входа в скриптовую среду. |

## data/

Что лежит в `data/` — каталоги, форматы, как парсятся.

| Файл | Что внутри |
|---|---|
| [data/layout.md](data/layout.md) | Полный обзор `data/`: 26 подпапок и что в каждой. |
| [data/file_formats.md](data/file_formats.md) | Форматы файлов: `.parser` (текстовые конфиги), `.pattern` (карты-кисти), `.aaf` (анимации), `.tga`/`.dds` (текстуры). |

## Чем это отличается от `docs/recon/`

| `docs/recon/` (для игрока) | `internals/` (для разработчика/моддера) |
|---|---|
| «Сколько шахт у меня будет на старте?» | «В каком порядке `dmscript.source` инициализирует глобальное состояние?» |
| «Почему один сейв даёт разную добычу?» | «Какой именно LCG использует Delphi `Random`, и что зависит от какого RNG-потока?» |
| «Как ходят юниты в формации?» | «Как pathfinding-thread-pool взаимодействует с скриптовым тиком?» |

Граница: если для понимания нужны имена нативных функций / форматы
байт-уровня / бинарь exe — это сюда. Если нужны игровые числа /
поведение в активной партии — это в `docs/`.

## Связанные машинные дампы

Все JSON-датасеты, генерируемые из этих документов или из бинаря, — в
[`../derived/`](../derived/):

- `dws_native_signatures.json` — 4 856 native сигнатур (см. [engine/native_api.md](engine/native_api.md)).
- `engine_primitives.json` — 884 native + 46 type-cast'ов из скриптов.
- `exe_strings.json` — 61k ASCII + 15k Pascal ShortString из exe.
- Прочие (game_settings, tech_tree, builder_slots, ...) — для игровой стороны.

## Инструменты

Все экстракторы — в [`../parser/engine_recon/`](../parser/engine_recon/):

```powershell
python parser\engine_recon\extract_primitives.py     # → derived/engine_primitives.json
python parser\engine_recon\dump_exe_strings.py       # → derived/exe_strings.json
python parser\engine_recon\extract_dws_signatures.py # → derived/dws_native_signatures.json
                                                     # + internals/engine/native_primitives.md
```
