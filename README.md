# Cossacks 3 Almanac

Полный справочник по экономике, юнитам, зданиям и апгрейдам игры **Cossacks 3 — Back to War**, извлечённый напрямую из игровых скриптов (`unit.script`, `country.script`, `dmscript.global`, locale-файлы). В репозитории: парсер игровых файлов, набор производных расчётов, writers для markdown/xlsx, симулятор экономики и накопленные исследования механик.

> Источник всех чисел — файлы установленной игры. Если что-то расходится с внешними калькуляторами или гайдами — доверяй репозиторию (расхождения задокументированы). Скрипты идемпотентны: после игрового патча перегенерируешь pipeline, и все артефакты обновляются.

## Что внутри

**Готовый справочник** — открывай прямо на GitHub, ничего запускать не надо. Всё лежит в [`docs/`](docs/):

- [`docs/reference/`](docs/reference/) — каноническая справка: 7 глав по темам, 21 нация, 15 side-by-side сравнений
- [`docs/recon/`](docs/recon/) — глубокие исследования механик (захват, путь, ИИ, наёмники, сетевая модель, RNG, генерация карт)
- [`docs/reports/`](docs/reports/) — производные расчёты, сгруппированные по теме:
  `combat/` (DPS, контр-матрица, скорость атаки, vision), `economy/` (scaling, builder slots, construction, production, efficiency), `tech/` (tech tree), `map/` (ресурсы, стартовая раскладка, валидация по реплеям), `nations/` (overview)
- [`docs/simulations/`](docs/simulations/) — выходы симулятора экономики (build orders → таймлайн)

**Pipeline** — для регенерации после патча игры:

- [`parser/`](parser/) — извлечение данных из `.script` (Pascal-парсер с символьным исполнением)
- [`compute/`](compute/) — производные расчёты (scaling, map gen, tech tree, construction times, и т. д.)
- [`writers/`](writers/) — генерация markdown-справочника + diff между снапшотами
- [`simulator/`](simulator/) — timeline-симулятор экономики + примеры build orders
- [`scripts/regen.py`](scripts/regen.py) + [`Makefile`](Makefile) — единый runner для всего pipeline'а

**Перед началом работы с `data.json`:** [`docs/known_issues.md`](docs/known_issues.md) — список парсерных пробелов, расхождений с внешними гайдами, open empirical questions. Самый известный кейс: для 168 dip-юнитов в `data.json` лежат не наёмничьи статы; правильные числа — в `docs/recon/mercenaries_diplomacy.md`.

**Моды** — изменения игровой логики через C3 mod-loader:

- [`mods/`](mods/) — каждый мод как подпапка с `build.py` (патчер) и собранным результатом. См. [`mods/README.md`](mods/README.md) для конвенции.

## Структура репозитория

```
.
├── parser/                  парсеры игровых .script-файлов → docs/data.json
├── compute/                 производные расчёты от data.json → docs/reports/<topic>/
├── writers/                 рендер data.json в markdown/xlsx + шаблоны прозы
├── simulator/               timeline-симулятор экономики → docs/simulations/
├── mods/                    моды (каждый — build.py + src/ + build/)
└── docs/                    единая база человеко-читаемых артефактов
    ├── data.json            мастер-данные (~4.7 МБ, источник правды)
    ├── derived/             машинно-читаемые JSON (animations, tech_tree, builder_slots, …)
    ├── reference/           каноническая справка (01_economy.md … 07_naval.md, nations/, compare/)
    ├── recon/               глубокие исследования механик (handwritten)
    ├── reports/             производные отчёты, по темам:
    │   ├── combat/          DPS / EHP / counter matrix / attack rates / vision
    │   ├── economy/         scaling / builder_slots / construction / production / efficiency
    │   ├── tech/            tech tree
    │   ├── map/             map resources / starting layout / replay validation
    │   └── nations/         cross-nation overview
    └── simulations/         выходы симулятора экономики
```

## Быстрый старт

### Просто почитать

GitHub рендерит markdown — открывай нужный файл. Точки входа:

- [`docs/reference/README.md`](docs/reference/README.md) — оглавление справочника + краткая выжимка
- [`docs/recon/README.md`](docs/recon/README.md) — индекс глубоких исследований
- [`docs/reports/README.md`](docs/reports/README.md) — индекс производных отчётов
- [`docs/simulations/README.md`](docs/simulations/README.md) — как запустить симулятор и формат build order

### Регенерировать после патча игры

Требования: Python 3.11+ и установленный Cossacks 3 (Steam). По умолчанию ищется в `C:\Program Files (x86)\Steam\steamapps\common\Cossacks 3` — для другого пути установи env-переменную:

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
python parser/build_data.py                     # → docs/data.json (мастер-данные)
python parser/build_canonical_terms.py          # → docs/derived/canonical_terms.json
python writers/write_md_tree.py                 # → docs/reference/ + docs/README.md
python compute/compute_combat_stats.py          # → docs/reports/combat/combat_stats.md
python compute/compute_counter_matrix.py        # → docs/reports/combat/counter_matrix.md
python compute/compute_attack_rates.py          # → docs/reports/combat/attack_rates.md
python compute/compute_vision.py                # → docs/reports/combat/vision_radii.md
python compute/compute_scaling.py               # → docs/reports/economy/scaling_prices.md
python compute/compute_efficiency_upgrades.py   # → docs/reports/economy/efficiency_upgrades.md
python compute/compute_construction_times.py    # → docs/reports/economy/construction_times.md
python compute/compute_builder_slots.py         # → docs/reports/economy/builder_slots.md (+derived/builder_slots.json)
python compute/build_tech_tree.py               # → docs/reports/tech/tech_tree.md + economy/production_rates.md + derived/tech_tree.json
python compute/compute_game_settings.py         # → docs/reports/map/lobby_settings.md (+derived/game_settings.json)
python compute/compute_map_resources.py         # → docs/reports/map/map_resources.md
python compute/extract_starting_layout.py       # → docs/reports/map/starting_layout.md
python compute/validate_map_predictions.py      # → docs/reports/map/map_predictions_validation.md
python compute/compute_nations_overview.py      # → docs/reports/nations/overview.md
python parser/parse_animations.py               # → docs/derived/animations.json
python parser/parse_generator_cfg.py            # → docs/derived/pattern_types.json
python parser/parse_pattern_inventory.py        # → docs/derived/pattern_{inventory,type_stats}.json
python simulator/simulate_economy.py simulator/build_orders/bav_basic_5min.json   # → docs/simulations/
```

`parser/build_data.py` — единственный скрипт, который читает игровые файлы. Все остальные потребляют `docs/data.json` и работают за <30 сек суммарно.

### Diff снапшотов после патча

Один шаг через make (или ручной — три команды ниже):

```bash
make diff   # снапшотит docs/data.json, regen, diff в diff.md
```

Или вручную:

```bash
python parser/build_data.py
cp docs/data.json /tmp/data_old.json
# … обновляешь игру …
python parser/build_data.py
python writers/diff_snapshots.py /tmp/data_old.json docs/data.json --out diff.md
```

После регенерации в `diff.md` видны все изменения статов между версиями игры.

## Sanity checks

`parser/build_data.py` гоняет **112 автопроверок** на каждом запуске и фейлится, если игра поменяла что-то ключевое (константы времени, базовые порции, известные числа конкретных юнитов, mine upgrade chain, market rates). Покрытие — `parser/README.md` содержит список категорий.

## Что сейчас в данных

- **Нации:** 21 (играбельные; mis/tat/lit исключены)
- **Здания:** 414 строк (sid×nation)
- **Юниты:** 714 строк
- **Апгрейды:** 4429 строк (с полностью разрешёнными cost / value / itype / prereqs)
- **Офицеры/формации:** 231 групп

## Лицензия и атрибуция

Этот репозиторий содержит **только производные данные** из публично распространяемых игровых файлов Cossacks 3 (GSC Game World). Игровые ресурсы и торговые марки принадлежат их владельцам. Скрипты в этом репозитории — отдельная работа, распространяются без специальной лицензии (используй на свой страх и риск).
