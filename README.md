# Cossacks 3 Almanac

Полный справочник по экономике, юнитам, зданиям и апгрейдам игры **Cossacks 3 — Back to War**, извлечённый напрямую из игровых скриптов (`unit.script`, `country.script`, `dmscript.global`, locale-файлы). В репозитории: парсер игровых файлов, набор производных расчётов, writers для markdown/xlsx, симулятор экономики и накопленные исследования механик.

> Источник всех чисел — файлы установленной игры. Если что-то расходится с внешними калькуляторами или гайдами — доверяй репозиторию (расхождения задокументированы). Скрипты идемпотентны: после игрового патча перегенерируешь pipeline, и все артефакты обновляются.

## Что внутри

📖 **Готовый справочник** — открывай прямо на GitHub, ничего запускать не надо:
- [`output/reference/`](output/reference/) — каноническая справка: главы по темам, 21 нация, 16 сравнений
- [`output/reports/`](output/reports/) — все производные расчёты: DPS/EHP, контр-матрица, scaling, tech tree, production rates, builder slots, construction times, map resources, starting layout
- [`output/simulations/`](output/simulations/) — выходы симулятора экономики (build orders → таймлайн)
- [`recon/`](recon/) — глубокие исследования механик (добыча, строительство, эмпирика, детерминизм/синк)

🔧 **Pipeline** — для регенерации после патча игры:
- [`parser/`](parser/) — извлечение данных из `.script` (Pascal-парсер с символьным исполнением)
- [`compute/`](compute/) — производные расчёты (scaling, map gen, tech tree, construction times)
- [`writers/`](writers/) — генерация markdown / xlsx / diff между снапшотами
- [`simulator/`](simulator/) — timeline-симулятор экономики + примеры build orders

🛠 **Моды** — изменения игровой логики через C3 mod-loader:
- [`mods/`](mods/) — каждый мод как подпапка с `build.py` (патчер) и собранным результатом. См. [`mods/README.md`](mods/README.md) для конвенции.

## Структура репозитория

```
.
├── parser/                      ← парсеры игровых .script-файлов → output/data.json
│   ├── config.py                ← пути, константы, табличные маппинги
│   ├── build_data.py            ← orchestrator (запускать первым)
│   ├── extract_constants.py
│   ├── parse_locale.py
│   ├── parse_country.py
│   ├── parse_units.py
│   ├── simulate_upgrades.py
│   └── debug/                   ← вспомогательные dev-скрипты для парсера
├── compute/                     ← производные расчёты от data.json (всё пишет в output/reports/)
│   ├── compute_scaling.py             → scaling_prices.md
│   ├── compute_map_resources.py       → map_resources.md
│   ├── compute_construction_times.py  → construction_times.md
│   ├── compute_builder_slots.py       → builder_slots.md (+derived/builder_slots.json)
│   ├── compute_efficiency_upgrades.py → efficiency_upgrades.md
│   ├── compute_combat_stats.py        → combat_stats.md (DPS / EHP / armor)
│   ├── compute_counter_matrix.py      → counter_matrix.md (TTK matrix)
│   ├── extract_starting_layout.py     → starting_layout.md
│   └── build_tech_tree.py             → tech_tree.md, production_rates.md (+derived/tech_tree.json)
├── writers/                     ← форматирование data.json в человеко-читаемые формы
│   ├── write_md_tree.py         ← основной writer (output/reference/ дерево)
│   ├── write_md.py              ← (legacy) монолитный md
│   ├── write_xlsx.py            ← xlsx со sanity-проверками
│   └── diff_snapshots.py        ← diff двух снапшотов data.json (после патча)
├── simulator/                   ← timeline-симулятор экономики → output/simulations/
│   ├── simulate_economy.py
│   └── build_orders/            ← примеры входных build orders (.json)
├── recon/                       ← research notes (механики добычи, строительства, эмпирика, детерминизм/синк)
├── mods/                        ← моды для игры (каждый — подпапка с build.py + src/ + build/)
│   └── Deterministic Extraction/  ← воспроизводимая добыча через SetRandomKey+RandomExt
└── output/                      ← сгенерированные артефакты (всё это уже в репо)
    ├── data.json                ← единый источник правды (~4.7 MB)
    ├── cossacks3_reference.{md,xlsx}  ← (legacy) монолитная версия
    ├── reference/               ← каноническая справка (главы 01-06, nations/, compare/)
    ├── reports/                 ← все производные расчёты (.md), индекс — reports/README.md
    ├── simulations/             ← выходы симулятора (sim_*.{csv,md})
    └── derived/                 ← машинно-читаемые JSON-датасеты
```

## Быстрый старт

### Просто почитать справочник

GitHub рендерит markdown — открывай нужный файл. Точки входа:

- [output/reference/README.md](output/reference/README.md) — TL;DR + index + glossary
- [output/reports/README.md](output/reports/README.md) — индекс всех производных расчётов
- [output/simulations/README.md](output/simulations/README.md) — как запустить симулятор и формат build order
- [recon/README.md](recon/README.md) — research notes по конкретным механикам

### Регенерировать после патча игры

Требования: Python 3.11+ и установленный Cossacks 3 (Steam). По умолчанию ищется в `C:\Program Files (x86)\Steam\steamapps\common\Cossacks 3` — для другого пути установи env-переменную:

```bash
# Linux/macOS
export COSSACKS3_PATH="/path/to/Cossacks 3"

# Windows (PowerShell)
$env:COSSACKS3_PATH = "D:\Games\Cossacks 3"
```

Затем из корня репозитория:

```bash
python -m pip install openpyxl                       # для writers/write_xlsx.py

python parser/build_data.py                          # → output/data.json
python writers/write_md_tree.py                      # → output/reference/ + output/README.md
python compute/compute_scaling.py                    # → output/reports/scaling_prices.md
python compute/compute_map_resources.py              # → output/reports/map_resources.md
python compute/compute_construction_times.py         # → output/reports/construction_times.md
python compute/compute_efficiency_upgrades.py        # → output/reports/efficiency_upgrades.md
python compute/compute_combat_stats.py               # → output/reports/combat_stats.md
python compute/compute_counter_matrix.py             # → output/reports/counter_matrix.md
python compute/extract_starting_layout.py            # → output/reports/starting_layout.md
python compute/build_tech_tree.py                    # → output/reports/tech_tree.md + production_rates.md + output/derived/tech_tree.json
python compute/compute_animations.py                 # → output/derived/animations.json
python compute/compute_builder_slots.py              # → output/reports/builder_slots.md + output/derived/builder_slots.json
python parser/parse_generator_cfg.py                 # → output/derived/pattern_types.json
python compute/compute_pattern_inventory.py          # → output/derived/pattern_{inventory,type_stats}.json
python simulator/simulate_economy.py simulator/build_orders/bav_basic_5min.json   # → output/simulations/
```

`parser/build_data.py` — единственный скрипт, который читает игровые файлы. Все остальные потребляют `output/data.json` и работают за <30 сек суммарно.

### Diff снапшотов после патча

```bash
python parser/build_data.py
cp output/data.json /tmp/data_old.json
# … обновляешь игру …
python parser/build_data.py
python writers/diff_snapshots.py /tmp/data_old.json output/data.json --out diff.md
```

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
