## Начни здесь

**[reference/README.md](reference/README.md)** — структурированный справочник по игре: формулы, главы, 21 нация, 16 сравнений.

## Структура `output/`

```
output/
├── README.md              ← этот файл (каталог)
├── data.json              ← сырой источник правды (~4.7 MB)
├── reference/             ← каноническая справка по игре
│   ├── README.md          ← TL;DR + index + glossary
│   ├── 01_economy.md … 06_market.md  ← главы по темам
│   ├── nations/           ← 21 cheatsheet по нациям
│   └── compare/           ← side-by-side сравнения юнитов / зданий
├── reports/               ← все производные расчёты (.md)
│   ├── README.md          ← индекс отчётов
│   ├── combat_stats.md    ← DPS / EHP
│   ├── counter_matrix.md  ← TTK между классами юнитов
│   ├── scaling_prices.md  ← цена N-го экземпляра здания
│   ├── efficiency_upgrades.md
│   ├── tech_tree.md       ← граф зависимостей
│   ├── production_rates.md ← units / min
│   ├── construction_times.md ← время постройки с N строителями
│   ├── builder_slots.md   ← макс. число строителей на здание
│   ├── map_resources.md   ← подсчёт на стандартной карте
│   └── starting_layout.md ← стартовая раскладка
├── simulations/           ← выходы симулятора экономики
│   ├── README.md          ← как запустить, формат build order
│   └── sim_*.{csv,md}     ← результаты прогонов
└── derived/               ← машинно-читаемые JSON-датасеты
    ├── tech_tree.json
    ├── animations.json
    ├── builder_slots.json
    └── pattern_*.json
```

## Reference — каноническая справка

[**reference/**](reference/) — главы по темам, по одному cheatsheet на нацию, side-by-side сравнения. Старт — [reference/README.md](reference/README.md):

- **Главы:** [01_economy](reference/01_economy.md), [02_combat](reference/02_combat.md), [03_buildings](reference/03_buildings.md), [04_units](reference/04_units.md), [05_upgrades](reference/05_upgrades.md), [06_market](reference/06_market.md)
- **Нации:** [reference/nations/](reference/nations/README.md) — 21 нация
- **Сравнения:** [reference/compare/](reference/compare/README.md) — pikemen / musketeers / cavalry / ships / weapons и др.

## Reports — производные расчёты

Всё, что считается из `data.json`: бой (DPS / EHP, контр-матрица), цены и масштабирование, темпы и тайминги, ресурсы карты. Индекс — [reports/README.md](reports/README.md).

- **Бой:** [combat_stats](reports/combat_stats.md), [counter_matrix](reports/counter_matrix.md)
- **Цены:** [scaling_prices](reports/scaling_prices.md), [efficiency_upgrades](reports/efficiency_upgrades.md)
- **Темп:** [tech_tree](reports/tech_tree.md), [production_rates](reports/production_rates.md), [construction_times](reports/construction_times.md), [builder_slots](reports/builder_slots.md)
- **Карта:** [map_resources](reports/map_resources.md), [starting_layout](reports/starting_layout.md)

## Simulations — выходы симулятора

[**simulations/**](simulations/README.md) — таймлайны экономики по конкретным build order'ам (скрипт `simulator/simulate_economy.py`). Build orders (вход) — в [`../simulator/build_orders/`](../simulator/build_orders/).

## Сырой JSON

[`data.json`](data.json) — единый источник правды, выход `parser/build_data.py`. Все writer-скрипты читают отсюда. После патча игры регенерируется.

## Глубокие исследования (`../recon/`)

Research notes по конкретным механикам ([`../recon/README.md`](../recon/) — индекс):

- [`../recon/peasant_extraction.md`](../recon/peasant_extraction.md) — добыча: цикл крестьянина, формулы, шахты, поля, апгрейды
- [`../recon/building_mechanics.md`](../recon/building_mechanics.md) — постройка / починка, builder slots, стены, гарнизон, захват
- [`../recon/map_generation_pipeline.md`](../recon/map_generation_pipeline.md) — DoGenerate timeline + seed space
- [`../recon/determinism_audit.md`](../recon/determinism_audit.md) — RNG-сайты, save / load, мод-фикс
- [`../recon/ticks_and_subticks.md`](../recon/ticks_and_subticks.md) — модель времени, adaptive game speed
- [`../recon/server_sync_architecture.md`](../recon/server_sync_architecture.md) — server-authoritative модель C3

## Регенерация

После патча игры или изменений в скриптах:

```
python parser/build_data.py                 # → output/data.json (источник правды)
python writers/write_md_tree.py             # → output/reference/ + output/README.md
python compute/compute_scaling.py           # → output/reports/scaling_prices.md
python compute/compute_map_resources.py     # → output/reports/map_resources.md
python compute/build_tech_tree.py           # → output/reports/tech_tree.md + production_rates.md + derived/tech_tree.json
python simulator/simulate_economy.py <build_order.json>  # → output/simulations/sim_<name>.{csv,md}
```

Все writer-скрипты читают только из `data.json` — кроме `build_data.py`, который читает напрямую из файлов игры.
