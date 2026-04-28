# Cossacks 3 — каталог артефактов

_Extracted **2026-04-28 09:52:20** (local) from game files (unit.script mtime: 2026-04-28 03:32:28)._

Все сгенерированные файлы для справочника по игре. Главная точка входа.

## Начни здесь

**[reference/README.md](reference/README.md)** — структурированный справочник: формулы, главы, 21 нация, 16 сравнений, derived-расчёты.

## Структура `output/`

```
output/
├── README.md              ← этот файл (каталог)
├── data.json              ← сырой источник правды (~4.7 MB)
├── reference/             ← справочник по игре (~50 файлов)
│   ├── README.md          ← TL;DR + index по справочнику
│   ├── 01_economy.md … 06_market.md  ← главы по темам
│   ├── nations/           ← 21 cheatsheet по нациям
│   ├── compare/           ← 16 side-by-side сравнений
│   └── derived/           ← расчётные файлы
│       ├── scaling_prices.md      ← цены N-го здания
│       └── map_resources.md       ← ресурсы на карте
└── strategy/              ← strategy stack (планирование экономики)
    ├── README.md          ← вход в strategy: что есть, как использовать
    ├── tech_tree.{md,json}        ← граф зависимостей
    ├── production_rates.md        ← units/min для каждого здания
    └── sim/                       ← output симулятора (sim_*.csv/md)
```

## Reference (главное)

[**reference/**](reference/) — структурированный справочник по игре. Открывай нужный файл напрямую, или начни с [reference/README.md](reference/README.md):

- **Главы:** [01_economy](reference/01_economy.md), [02_combat](reference/02_combat.md), [03_buildings](reference/03_buildings.md), [04_units](reference/04_units.md), [05_upgrades](reference/05_upgrades.md), [06_market](reference/06_market.md)
- **Нации:** [reference/nations/](reference/nations/README.md) — по одному cheatsheet на нацию
- **Сравнения:** [reference/compare/](reference/compare/README.md) — pikemen/musketeers/cavalry/ships/weapons и др. side-by-side
- **Derived:** [reference/derived/](reference/reports/) — scaling_prices (цена N-го здания) и map_resources (подсчёт на карте)

## Strategy stack

Файлы для планирования и симуляции экономики — в подкаталоге [`strategy/`](strategy/):

| Файл | Что внутри | Скрипт |
|---|---|---|
| [strategy/README.md](strategy/README.md) | **Точка входа в strategy**: как использовать | — |
| [strategy/tech_tree.md](strategy/tech_tree.md) / [.json](derived/tech_tree.json) | Граф зависимостей зданий/юнитов/апгрейдов | `parser/build_tech_tree.py` |
| [strategy/production_rates.md](strategy/production_rates.md) | units/min для каждого здания × юнита | то же |
| [strategy/sim/](strategy/sim/) | Output симулятора (`sim_*.csv/md`) | `parser/simulate_economy.py` |

Build orders (вход для симулятора): [`../build_orders/`](../build_orders/)

## Сырой JSON

[`data.json`](data.json) — единый источник правды, выход `parser/build_data.py`. Все writer-скрипты читают отсюда. После патча игры регенерируется.

## Глубокие исследования (`../recon/`)

Не справочник, а research notes и черновики:

- [`../recon/peasant_extraction.md`](../recon/peasant_extraction.md) — полный разбор механики добычи
- [`../recon/extraction_formulas.md`](../recon/extraction_formulas.md) — формульная сводка
- [`../recon/empirical_tests.md`](../recon/empirical_tests.md) — открытые вопросы для in-game замеров
- [`../recon/step1_findings.md`](../recon/step1_findings.md) — исторический recon файлов игры
- [`../recon/visual_editor_roadmap.md`](../recon/visual_editor_roadmap.md) — план визуального редактора стратегий

## Регенерация

После патча игры или изменений в скриптах:

```
python parser/build_data.py                 # → output/data.json (источник правды)
python writers/write_md_tree.py             # → output/reference/ + output/README.md
python compute/compute_scaling.py           # → output/reference/reports/scaling_prices.md
python compute/compute_map_resources.py     # → output/reference/reports/map_resources.md
python compute/build_tech_tree.py           # → output/strategy/tech_tree.{md,json}, production_rates.md
python simulator/simulate_economy.py <build_order.json>  # → output/strategy/sim/sim_<name>.{csv,md}
```
Все writer-скрипты читают только из `data.json` — кроме `build_data.py`, который читает напрямую из файлов игры.

## Стат

- Нации: **21**
- Здания: **414** строк (sid×nation)
- Юниты: **714** строк
- Апгрейды: **4429** строк (с полными cost/value/itype)
- Офицеры: **231** групп
- Sanity checks: **112/112** PASS