# Cossacks 3 Almanac

[English](README.en.md) · **Русский**

Полный справочник по экономике, юнитам, зданиям и апгрейдам игры **Cossacks 3 — Back to War**, извлечённый напрямую из игровых скриптов (`unit.script`, `country.script`, `dmscript.global`, locale-файлы). В репозитории: парсер игровых файлов, набор производных расчётов, writers для markdown/xlsx, симулятор экономики и накопленные исследования механик.

> Источник всех чисел — файлы установленной игры. Если что-то расходится с внешними калькуляторами или гайдами — доверяй репозиторию (расхождения задокументированы). Скрипты идемпотентны: после игрового патча перегенерируешь pipeline, и все артефакты обновляются.

## Что внутри

**Готовый справочник для игроков** — открывай прямо на GitHub, ничего запускать не надо. Всё лежит в [`docs/`](docs/):

- [`docs/reference/`](docs/reference/) — каноническая справка: 7 глав по темам,
  21 нация и 33 сравнительные таблицы
- [`docs/recon/`](docs/recon/) — handwritten reverse-engineering механик игры, разбито по темам:
  `world/economy/` (добыча, постройка, захват, голод, очередь, апгрейды), `world/combat/` (урон, формации, выбор цели, башни, стены, артиллерия, флот, обзор), `world/map/` (генерация карты, опции лобби), `systems/` (AI, наёмники, условия победы, сценарии, UI/ввод)
- [`docs/reports/`](docs/reports/) — производные расчёты, сгруппированные по теме:
  `combat/` (боевые показатели, матрица противодействия, темп атак, обзор,
  артиллерия), `economy/` (рост цен, места строителей, время строительства,
  производство, эффективность), `tech/` (дерево развития), `map/` (ресурсы,
  стартовая раскладка, настройки матча), `nations/` (обзор и национальные
  отличия)

**Техническая документация (для разработчиков / моддеров)** — отдельно от `docs/` в [`internals/`](internals/):

- [`internals/engine/`](internals/engine/) — устройство движка (Delphi + DWS): native API (4856 функций), RTTI, RNG, animation system, сетевые пакеты, тики
- [`internals/scripts/`](internals/scripts/) — структура `data/scripts/*` (load order, точки входа)
- [`internals/data/`](internals/data/) — `data/`-каталог игры: подпапки и форматы файлов (`.parser`, `.pattern`, `.aaf`)

**Машинно-читаемые JSON-датасеты** — для редактора билдов, симулятора, внешних анализаторов:

- [`data.json`](data.json) — мастер-структура (~5.7 МБ): 21 нация, 456 зданий, 714 юнитов, 4483 апгрейда
- [`derived/`](derived/) — специализированные срезы: `tech_tree.json`, `builder_slots.json`, `animations.json`, `game_settings.json`, `canonical_terms.json`, `pattern_*.json`, `replay_ground_truth.json`, плюс engine-RE дампы (`dws_native_signatures.json`, `engine_primitives.json`, `exe_strings.json`)

**Pipeline — для регенерации после патча игры:**

- [`parser/`](parser/) — извлечение данных из `.script` (Pascal-парсер с символьным исполнением); подпапка [`engine_recon/`](parser/engine_recon/) — экстракторы из бинаря `cossacks.exe`
- [`compute/`](compute/) — производные расчёты (scaling, map gen, tech tree, construction times и т. д.)
- [`writers/`](writers/) — генерация markdown-справочника + diff между снапшотами
- [`simulator/`](simulator/) — timeline-симулятор экономики (backend для browser-редактора через Pyodide)
- [`editor/`](editor/) — браузерный редактор билдов (HTML + JS + Pyodide), запускает симулятор прямо в браузере
- [`scripts/regen.py`](scripts/regen.py) + [`Makefile`](Makefile) — единый runner для всего pipeline'а

**Перед началом работы с `data.json`:** [`internals/project/known_issues.md`](internals/project/known_issues.md) — список актуальных парсерных пробелов, расхождений с внешними гайдами и открытых эмпирических вопросов. Закрытые проблемы, включая прежнюю ошибку со статами наёмников, перенесены в [`internals/project/known_issues_archive.md`](internals/project/known_issues_archive.md).

**Моды** — изменения игровой логики через C3 mod-loader:

- [`mods/`](mods/) — каждый мод как подпапка с `build.py` (патчер) и собранным результатом. См. [`mods/README.md`](mods/README.md) для конвенции.

## Структура репозитория

```
.
├── data.json                мастер-данные (~5.7 МБ, источник правды для всего downstream)
├── derived/                 машинно-читаемые JSON (tech_tree, builder_slots, animations, game_settings, engine RE-дампы)
├── parser/                  парсеры игровых .script-файлов → data.json
│   └── engine_recon/        экстракторы из cossacks.exe (DWS native API, RTTI, primitives)
├── compute/                 производные расчёты от data.json → docs/reports/<topic>/
├── writers/                 рендер data.json в markdown + шаблоны прозы
├── simulator/               timeline-симулятор экономики (backend редактора через Pyodide)
├── editor/                  браузерный редактор билд-ордеров
├── mods/                    моды (каждый — build.py + src/ + build/)
├── scripts/                 pipeline-runner (regen.py)
│
├── docs/                    справочник для игрока
│   ├── reference/           каноническая справка (01_economy/README.md … 07_naval/README.md, nations/, compare/)
│   ├── recon/               глубокие исследования механик (handwritten)
│   │   ├── world/{economy,combat,map}/   логика мира
│   │   └── systems/         правила, AI, наёмники, сценарии, UI
│   └── reports/             производные отчёты, по темам:
│       ├── combat/          DPS / EHP / counter matrix / attack rates / vision / artillery
│       ├── economy/         scaling / builder_slots / construction / production / efficiency
│       ├── tech/            tech tree
│       ├── map/             ресурсы карты / стартовая раскладка / настройки матча
│       └── nations/         cross-nation overview / deviations
│
└── internals/               техническое устройство движка и скриптов
    ├── engine/              cossacks.exe, DWS, RNG, sync, тики, animation system
    ├── scripts/             структура data/scripts/* (load order, точки входа)
    └── data/                структура data/-каталога и форматы файлов
```

## Быстрый старт

### Просто почитать

GitHub рендерит markdown — открывай нужный файл. Точки входа:

- [`docs/reference/README.md`](docs/reference/README.md) — оглавление справочника + краткая выжимка
- [`docs/recon/README.md`](docs/recon/README.md) — индекс глубоких исследований
- [`docs/reports/README.md`](docs/reports/README.md) — индекс производных отчётов

### Регенерировать после патча игры

Требования: Python 3.11+ и установленный Cossacks 3 (Steam). Основной
конвейер использует стандартную библиотеку Python. Для извлечения иконок и
анализа исполняемого файла установите дополнительные зависимости:

```bash
python -m pip install -r requirements.txt
```

По умолчанию игра ищется в `C:\Program Files (x86)\Steam\steamapps\common\Cossacks 3`
— для другого пути установите переменную окружения:

```bash
# Linux/macOS
export COSSACKS3_PATH="/path/to/Cossacks 3"

# Windows (PowerShell)
$env:COSSACKS3_PATH = "D:\Games\Cossacks 3"
```

Затем из корня репозитория один из вариантов:

```bash
# Вариант 1 — Python-runner (работает на любой ОС):
python scripts/regen.py                         # full regen, всё что ниже разом
python scripts/regen.py reference               # только writers/
python scripts/regen.py reports-combat          # только docs/reports/combat/
python scripts/regen.py help                    # все targets

# Вариант 2 — make (где есть `make`):
make all          # = python scripts/regen.py all
make reference
make reports
make sanity       # parser + проверка 112 sanity-чеков
make help
```

Что внутри (для пошагового вызова без runner'а):

```bash
python parser/build_data.py                     # → data.json (мастер-данные)
python parser/build_canonical_terms.py          # → derived/canonical_terms.json
python writers/write_md_tree.py                 # → docs/reference/ + docs/README.md
python compute/compute_combat_stats.py          # → docs/reports/combat/combat_stats.md
python compute/compute_counter_matrix.py        # → docs/reports/combat/counter_matrix.md
python compute/compute_attack_rates.py          # → docs/reports/combat/attack_rates.md
python compute/compute_vision.py                # → docs/reports/combat/vision_radii.md
python compute/compute_scaling.py               # → docs/reports/economy/scaling_prices.md
python compute/compute_efficiency_upgrades.py   # → docs/reports/economy/efficiency_upgrades.md
python compute/compute_construction_times.py    # → docs/reports/economy/construction_times.md
python compute/compute_builder_slots.py         # → docs/reports/economy/builder_slots.md (+derived/builder_slots.json)
python parser/build_tech_graph.py               # → derived/tech_tree.json
python compute/compute_tech_tree.py             # → docs/reports/tech/tech_tree.md + economy/production_rates.md
python compute/compute_game_settings.py         # → docs/reports/map/lobby_settings.md (+derived/game_settings.json)
python compute/compute_map_resources.py         # → docs/reports/map/map_resources.md
python compute/compute_starting_layout.py       # → docs/reports/map/starting_layout.md
python compute/validate_map_predictions.py      # → internals{_en}/data/map_predictions_validation.md
python compute/compute_nations_overview.py      # → docs/reports/nations/overview.md
python parser/parse_animations.py               # → derived/animations.json
python parser/parse_generator_cfg.py            # → derived/pattern_types.json
python parser/parse_pattern_inventory.py        # → derived/pattern_{inventory,type_stats}.json
python scripts/build_entity_catalog.py           # → assets/data/entity-catalog.json + игровые UI-иконки
```

`parser/build_data.py` читает игровые данные, а `scripts/build_entity_catalog.py` —
таблицу материалов и UI-атласы. Остальные генераторы потребляют `data.json` и
работают без повторного разбора установки игры.

### Diff снапшотов после патча

Один шаг через make (или ручной — три команды ниже):

```bash
make diff   # снапшотит data.json, regen, diff в diff.md
```

Или вручную:

```bash
python parser/build_data.py
cp data.json /tmp/data_old.json
# … обновляешь игру …
python parser/build_data.py
python writers/diff_snapshots.py /tmp/data_old.json data.json --out diff.md
```

После регенерации в `diff.md` видны все изменения статов между версиями игры.

## Sanity checks

`make sanity` или `python scripts/regen.py sanity` пересобирает данные и
проверяет **112 инвариантов**. Команда завершится с ошибкой, если игра
поменяла что-то ключевое: константы времени, базовые порции, известные числа
конкретных юнитов, цепочку улучшений шахт или курсы рынка. Список категорий
приведён в [`parser/README.md`](parser/README.md).

## Что сейчас в данных

- **Нации:** 21 (играбельные; mis/tat/lit исключены)
- **Здания:** 456 строк (sid×nation)
- **Юниты:** 714 строк
- **Апгрейды:** 4483 строки (с полностью разрешёнными cost / value / itype / prereqs)
- **Офицеры/формации:** 231 групп

## Лицензия и атрибуция

Оригинальный код и авторская документация распространяются по
[лицензии MIT](LICENSE). Производные игровые данные, интерфейсные иконки,
названия и торговые марки этой лицензией не покрываются и принадлежат их
правообладателям. Подробности и лицензии браузерных библиотек приведены в
[уведомлении о сторонних материалах](THIRD_PARTY_NOTICES.md).
