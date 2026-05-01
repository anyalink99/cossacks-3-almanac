# Cossacks 3 — каталог артефактов

_Extracted **2026-05-01 04:53:43** (local) from game files (unit.script mtime: 2026-04-28 03:32:28)._

Все сгенерированные файлы для справочника по игре. Главная точка входа.

## Начни здесь

**[reference/README.md](reference/README.md)** — структурированный справочник по игре: формулы, главы по темам, 21 нация, 16 сравнений.

**[architecture.md](architecture.md)** — поток данных в проекте: что откуда берётся, кто что генерирует. Читать **перед** тем как добавлять новый отчёт или править генератор.

**[known_issues.md](known_issues.md)** — парсерные пробелы, расхождения с внешними гайдами, open empirical questions. Закрытые проблемы — в [known_issues_archive.md](known_issues_archive.md). Читать **перед** тем как писать инструмент поверх `data.json`.

## Структура `docs/`

```
docs/
├── README.md              ← этот файл (каталог)
├── data.json              ← мастер-данные (~4.7 МБ, источник правды)
│
├── reference/             ← каноническая справка по игре (генерируется)
│   ├── README.md          ← TL;DR + index + glossary
│   ├── 01_economy.md … 07_naval.md  ← 7 глав по темам
│   ├── nations/           ← 21 cheatsheet по нациям
│   └── compare/           ← side-by-side сравнения юнитов / зданий
│
├── recon/                 ← глубокие исследования механик (handwritten)
│   ├── README.md          ← индекс + «когда что читать»
│   ├── peasant_extraction.md, building_mechanics.md, capture_mechanics.md,
│   ├── ai_behavior.md, mercenaries_diplomacy.md, pathfinding.md,
│   ├── victory_conditions.md, map_generation_pipeline.md,
│   ├── determinism_audit.md, ticks_and_subticks.md, server_sync_architecture.md
│
├── reports/               ← производные расчёты, сгруппированы по теме
│   ├── README.md
│   ├── combat/            DPS, counter matrix, attack rates, vision
│   ├── economy/           scaling, builder_slots, construction, production, efficiency
│   ├── tech/              tech tree
│   ├── map/               map resources, starting layout, replay validation
│   └── nations/           cross-nation overview
│
├── simulations/           ← выходы симулятора экономики
│   ├── README.md
│   └── sim_*.{csv,md}
│
└── derived/               ← машинно-читаемые JSON-датасеты
    ├── README.md          ← каталог всех JSON
    ├── animations.json, builder_slots.json, tech_tree.json,
    ├── canonical_terms.json, game_settings.json,
    ├── pattern_*.json, replay_ground_truth.json
```

## Reference — каноническая справка

[**reference/**](reference/) — главы по темам, cheatsheet на каждую нацию, side-by-side сравнения. Старт — [reference/README.md](reference/README.md).

- **Главы:** [01_economy](reference/01_economy.md), [02_combat](reference/02_combat.md), [03_buildings](reference/03_buildings.md), [04_units](reference/04_units.md), [05_upgrades](reference/05_upgrades.md), [06_market](reference/06_market.md), [07_naval](reference/07_naval.md)
- **Нации:** [reference/nations/](reference/nations/README.md) — 21 нация, по одному cheatsheet
- **Сравнения:** [reference/compare/](reference/compare/README.md) — пикинеры / мушкетеры / кавалерия / корабли / оружие и др.

## Recon — глубокие исследования

[**recon/**](recon/README.md) — Reverse-engineering ключевых механик. Каждый документ автономен и ссылается на конкретные строки игровых скриптов.

- **Логика мира:** [peasant_extraction](recon/world/peasant_extraction.md), [building_mechanics](recon/world/building_mechanics.md), [capture_mechanics](recon/world/capture_mechanics.md), [pathfinding](recon/world/pathfinding.md), [map_generation_pipeline](recon/world/map_generation_pipeline.md)
- **Игровые системы:** [ai_behavior](recon/systems/ai_behavior.md), [mercenaries_diplomacy](recon/systems/mercenaries_diplomacy.md), [victory_conditions](recon/systems/victory_conditions.md)
- **Engine internals:** [ticks_and_subticks](recon/engine/ticks_and_subticks.md), [determinism_audit](recon/engine/determinism_audit.md), [server_sync_architecture](recon/engine/server_sync_architecture.md)

## Reports — производные расчёты

Всё, что считается из `data.json`: бой, экономика, тех-дерево, карта, нации. Индекс — [reports/README.md](reports/README.md).

- **Бой:** [combat_stats](reports/combat/combat_stats.md), [counter_matrix](reports/combat/counter_matrix.md), [attack_rates](reports/combat/attack_rates.md), [vision_radii](reports/combat/vision_radii.md)
- **Экономика:** [scaling_prices](reports/economy/scaling_prices.md), [efficiency_upgrades](reports/economy/efficiency_upgrades.md), [production_rates](reports/economy/production_rates.md), [construction_times](reports/economy/construction_times.md), [builder_slots](reports/economy/builder_slots.md)
- **Тех-дерево:** [tech_tree](reports/tech/tech_tree.md)
- **Карта:** [lobby_settings](reports/map/lobby_settings.md), [map_resources](reports/map/map_resources.md), [starting_layout](reports/map/starting_layout.md), [map_predictions_validation](reports/map/map_predictions_validation.md)
- **Нации:** [overview](reports/nations/overview.md) — side-by-side сравнение всех 21

## Simulations — выходы симулятора

[**simulations/**](simulations/README.md) — таймлайны экономики по конкретным build order'ам (скрипт `simulator/simulate_economy.py`). Build orders (вход) — в [`../simulator/build_orders/`](../simulator/build_orders/).

## Сырой JSON

[`data.json`](data.json) — мастер-данные, выход `parser/build_data.py`. Все writer-скрипты читают отсюда. После патча игры регенерируется.

## Регенерация

После патча игры или изменений в скриптах:

```
python parser/build_data.py                 # → docs/data.json (источник правды)
python parser/build_canonical_terms.py      # → docs/derived/canonical_terms.json
python writers/write_md_tree.py             # → docs/reference/ + docs/README.md
python compute/compute_scaling.py           # → docs/reports/economy/scaling_prices.md
python compute/compute_game_settings.py     # → docs/reports/map/lobby_settings.md (+derived/game_settings.json)
python compute/compute_map_resources.py     # → docs/reports/map/map_resources.md
python parser/build_tech_graph.py           # → docs/derived/tech_tree.json
python compute/compute_tech_tree.py         # → docs/reports/tech/tech_tree.md + reports/economy/production_rates.md
python simulator/simulate_economy.py <build_order.json>  # → docs/simulations/sim_<name>.{csv,md}
```

Полный список команд для регенерации — в `README.md` корня репо.

## Стат

- Нации: **21**
- Здания: **414** строк (sid×nation)
- Юниты: **714** строк
- Апгрейды: **4429** строк (с полными cost/value/itype)
- Офицеры: **231** групп
- Sanity checks: **112/112** PASS