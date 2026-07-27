# Internals — техническое устройство Cossacks 3

[English](../internals_en/README.md) · **Русский**

Эта папка — **не справочник для игрока**. Здесь описано внутреннее устройство
игры: исполняемый файл, скриптовая среда DWS, структура каталога `data/` и
форматы файлов. Игровые характеристики, сравнения и объяснения механик
находятся в [энциклопедии](../docs/README.md).

Сюда попадает всё, что:

- описывает исполняемый файл (`cossacks.exe`) и используемые в нём
  Delphi, DWS, Indy и FastMM4;
- описывает структуру скриптов (`data/scripts/*`), порядок их загрузки и связи;
- описывает форматы и расположение файлов в `data/` (`.parser`,
  `.pattern`, `.aaf`, локали, генерация карт);
- дополняет читательские статьи из `docs/recon/` точными путями, внутренними
  полями и фрагментами исходных скриптов.

## Структура

| Раздел | Что внутри |
|---|---|
| [engine/](engine/) | Исполняемый файл, виртуальная машина DWS, сетевая модель, время и генераторы случайных чисел. |
| [scripts/](scripts/) | Структура `data/scripts/*`, порядок загрузки, точки входа и технические приложения к статьям о механиках. |
| [data/](data/) | Структура `data/`: подпапки, форматы файлов (`.parser`, `.pattern`, `.aaf`). |
| [project/](project/) | Архитектура репозитория, правила документации, планы исследований и известные ограничения. |

## engine/

Документы основаны на статическом анализе `cossacks.exe`. Скрипты Python
извлекают сведения непосредственно из исполняемого файла; проекты Ghidra или
IDA для воспроизведения результатов не требуются.

| Файл | Что внутри |
|---|---|
| [engine/native_api.md](engine/native_api.md) | **4 856 сигнатур встроенных функций DWS**: имена, типы аргументов и RVA, извлечённые из исполняемого файла по шаблону `AnsiString`. Покрыты все 884 примитива, которые вызывают игровые скрипты; функции сгруппированы по подсистемам. |
| [engine/native_primitives.md](engine/native_primitives.md) | Машинно-сгенерированный указатель: 50 самых часто используемых примитивов и по 10 примеров на подсистему. |
| [engine/rtti_class_map.md](engine/rtti_class_map.md) | Карта **1 779 классов Delphi** по подсистемам: игровые объекты, поведение, поиск пути, триггеры, сеть, генерация карт, редактор `.aix` и другие группы. |
| [engine/determinism_audit.md](engine/determinism_audit.md) | Какие генераторы случайных чисел участвуют в добыче и бою, какие состояния сохраняются и что можно изменить модификацией. |
| [engine/rng_implementation.md](engine/rng_implementation.md) | Реализация `Random` и `RandomExt`, их отдельные начальные состояния и приём с детерминированным ключом для каждого решения. |
| [engine/server_sync_architecture.md](engine/server_sync_architecture.md) | Серверная модель синхронизации, сетевые режимы, интервалы обновлений и назначение `bProcess`. |
| [engine/server_sync_packet_format.md](engine/server_sync_packet_format.md) | Битовая раскладка сетевых пакетов: двоичные записи `EconomyPackage` и текстовые снимки состояния юнитов. |
| [engine/ticks_and_subticks.md](engine/ticks_and_subticks.md) | Реальное и игровое время, кадры, основной цикл обновления и интервалы внутренних автоматов состояния. |
| [engine/animation_system.md](engine/animation_system.md) | Форматы анимации `.aaf` и `.acl`, скорости движения, момент нанесения удара, стоимость оружия и выбор звука выстрела. |
| [engine/script_modding_constraints.md](engine/script_modding_constraints.md) | Практические ограничения скриптовых модификаций: что можно изменить через DWS-скрипты, где нужны данные игры, а где возможности упираются в движок. |

## scripts/

Структура `data/scripts/*` — где какая логика лежит, как файлы
загружаются, какие точки входа.

| Файл | Что внутри |
|---|---|
| [scripts/structure.md](scripts/structure.md) | Порядок загрузки, основные файлы `.script`, их назначение и точки входа в скриптовую среду. |

### Технические приложения к игровым механикам

| Тема | Приложения |
|---|---|
| Экономика и строительство | [Добыча ресурсов](scripts/peasant_extraction_evidence.md), [строительство и ремонт](scripts/building_mechanics_evidence.md), [захват](scripts/capture_mechanics_evidence.md), [улучшения](scripts/upgrades_application_evidence.md), [голод и бунт](scripts/hunger_and_rebellion_evidence.md), [очередь производства](scripts/production_queue_evidence.md) |
| Бой и движение | [Выбор цели](scripts/target_selection_evidence.md), [поиск пути](scripts/pathfinding_evidence.md) |
| Карта | [Генерация случайной карты](scripts/map_generation_evidence.md) |

## data/

Что лежит в `data/` — каталоги, форматы, как парсятся.

| Файл | Что внутри |
|---|---|
| [data/layout.md](data/layout.md) | Полный обзор `data/`: 26 подпапок и что в каждой. |
| [data/file_formats.md](data/file_formats.md) | Форматы файлов: `.parser` (текстовые конфиги), `.pattern` (карты-кисти), `.aaf` (анимации), `.tga`/`.dds` (текстуры). |
| [data/game_fields_glossary.md](data/game_fields_glossary.md) | Глоссарий технических полей из `data.json` и скриптов игры. |
| [data/nation_deviations.md](data/nation_deviations.md) | Технические отпечатки национальных вариантов зданий и юнитов. |
| [data/map_predictions_validation.md](data/map_predictions_validation.md) | Калибровка расчётной модели ресурсов карты по данным реплеев. |
| [data/replay_format.md](data/replay_format.md) | Устройство файлов реплеев и сохранений `OSWMap13`: заголовок, записи, пакеты команд и синхронизация состояния. |

## Чем это отличается от `docs/recon/`

| `docs/recon/` (для игрока) | `internals/` (для разработчика/моддера) |
|---|---|
| «Сколько шахт у меня будет на старте?» | «В каком порядке `dmscript.source` инициализирует глобальное состояние?» |
| «Почему один сейв даёт разную добычу?» | «Какой именно LCG использует Delphi `Random`, и что зависит от какого RNG-потока?» |
| «Как ходят юниты в формации?» | «Как pathfinding-thread-pool взаимодействует с скриптовым тиком?» |

Граница проста: имена встроенных функций, форматы на уровне байтов и анализ
исполняемого файла относятся сюда. Игровые числа и наблюдаемое в партии
поведение относятся к [энциклопедии](../docs/README.md).

## Связанные машинные дампы

Все JSON-датасеты, генерируемые из этих документов или из бинаря, — в
[`../derived/`](../derived/):

- `dws_native_signatures.json` — 4 856 сигнатур встроенных функций (см. [engine/native_api.md](engine/native_api.md)).
- `engine_primitives.json` — 884 встроенных примитива и 46 приведений типов из скриптов.
- `exe_strings.json` — 61 000 ASCII-строк и 15 000 значений Pascal
  `ShortString` из исполняемого файла.
- Другие наборы (`game_settings`, `tech_tree`, `builder_slots` и прочие)
  используются в игровой энциклопедии.

## Инструменты

Все экстракторы — в [`../parser/engine_recon/`](../parser/engine_recon/):

```powershell
python parser\engine_recon\extract_primitives.py     # → derived/engine_primitives.json
python parser\engine_recon\dump_exe_strings.py       # → derived/exe_strings.json
python parser\engine_recon\extract_dws_signatures.py # → derived/dws_native_signatures.json
                                                     # + internals/engine/native_primitives.md
```
