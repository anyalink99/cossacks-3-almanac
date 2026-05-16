# Cossacks 3 — каталог артефактов

_Extracted **2026-05-05 16:33:56** (local) from game files (unit.script mtime: 2026-04-28 03:32:28)._

Все сгенерированные файлы для справочника по игре. Главная точка входа.

## Начни здесь

**[reference/README.md](reference/README.md)** — структурированный справочник по игре: формулы, главы по темам, 21 нация, 16 сравнений.

**[architecture.md](architecture.md)** — поток данных в проекте: что откуда берётся, кто что генерирует. Читать **перед** тем как добавлять новый отчёт или править генератор.

**[known_issues.md](known_issues.md)** — парсерные пробелы, расхождения с внешними гайдами, open empirical questions. Закрытые проблемы — в [known_issues_archive.md](known_issues_archive.md). Читать **перед** тем как писать инструмент поверх `data.json`.

## Структура `docs/`

Сам каталог `docs/` содержит только человеко-читаемые материалы для игрока. Машинные дампы и техническая документация лежат на верхнем уровне репозитория ([`../data.json`](../data.json), [`../derived/`](../derived/), [`../internals/`](../internals/)).

```
docs/
├── README.md              ← этот файл (каталог)
│
├── reference/             ← каноническая справка по игре (генерируется)
│   ├── README.md          ← TL;DR + index + glossary
│   ├── 01_economy/README.md … 07_naval/README.md  ← 7 глав по темам
│   ├── nations/           ← 21 cheatsheet по нациям
│   └── compare/           ← side-by-side сравнения юнитов / зданий
│
├── recon/                 ← глубокие исследования механик (handwritten)
│   ├── README.md          ← индекс + «когда что читать»
│   ├── world/
│   │   ├── economy/       добыча, постройка, захват, голод, очередь, апгрейды
│   │   ├── combat/        урон, формации, target_selection, башни, стены,
│   │   │                  артиллерия, флот, обзор, поведение стрелков
│   │   └── map/           map_generation_pipeline, game_settings
│   └── systems/           ai_behavior, mercenaries_diplomacy, victory_conditions,
│                          scenarios_and_triggers, ui_input_and_feedback
│
└── reports/               ← производные расчёты, сгруппированы по теме
    ├── README.md
    ├── combat/            DPS, counter matrix, attack rates, vision, artillery
    ├── economy/           scaling, builder_slots, construction, production, efficiency
    ├── tech/              tech tree
    ├── map/               map resources, starting layout, replay validation
    └── nations/           overview, deviations
```

## Reference — каноническая справка

[**reference/**](reference/) — главы по темам, cheatsheet на каждую нацию, side-by-side сравнения. Старт — [reference/README.md](reference/README.md).

- **Главы:** [01_economy](reference/01_economy/README.md), [02_combat](reference/02_combat/README.md), [03_buildings](reference/03_buildings/README.md), [04_units](reference/04_units/README.md), [05_upgrades](reference/05_upgrades/README.md), [06_market](reference/06_market/README.md), [07_naval](reference/07_naval/README.md)
- **Нации:** [reference/nations/](reference/nations/README.md) — 21 нация, по одному cheatsheet
- **Сравнения:** [reference/compare/](reference/compare/README.md) — пикинеры / мушкетеры / кавалерия / корабли / оружие и др.

## Recon — глубокие исследования

[**recon/**](recon/README.md) — Reverse-engineering ключевых механик. Каждый документ автономен и ссылается на конкретные строки игровых скриптов.

- **Логика мира — экономика:** [peasant_extraction](recon/world/economy/peasant_extraction.md), [building_mechanics](recon/world/economy/building_mechanics.md), [capture_mechanics](recon/world/economy/capture_mechanics.md), [hunger_and_rebellion](recon/world/economy/hunger_and_rebellion.md), [production_queue](recon/world/economy/production_queue.md), [upgrades_application](recon/world/economy/upgrades_application.md)
- **Логика мира — бой:** [combat_damage_pipeline](recon/world/combat/combat_damage_pipeline.md), [target_selection](recon/world/combat/target_selection.md), [formations](recon/world/combat/formations.md), [pathfinding](recon/world/combat/pathfinding.md), [unit_commands](recon/world/combat/unit_commands.md), [ranged_units_behavior](recon/world/combat/ranged_units_behavior.md), [vision_and_fow](recon/world/combat/vision_and_fow.md), [towers](recon/world/combat/towers.md), [walls_and_gates](recon/world/combat/walls_and_gates.md), [artillery_specifics](recon/world/combat/artillery_specifics.md), [naval_combat](recon/world/combat/naval_combat.md)
- **Логика мира — карта:** [map_generation_pipeline](recon/world/map/map_generation_pipeline.md), [game_settings](recon/world/map/game_settings.md)
- **Игровые системы:** [ai_behavior](recon/systems/ai_behavior.md), [mercenaries_diplomacy](recon/systems/mercenaries_diplomacy.md), [victory_conditions](recon/systems/victory_conditions.md), [scenarios_and_triggers](recon/systems/scenarios_and_triggers.md), [ui_input_and_feedback](recon/systems/ui_input_and_feedback.md)
- **Engine internals (выделены в [`../internals/`](../internals/)):** [ticks_and_subticks](../internals/engine/ticks_and_subticks.md), [determinism_audit](../internals/engine/determinism_audit.md), [server_sync_architecture](../internals/engine/server_sync_architecture.md), [native_api](../internals/engine/native_api.md), [rng_implementation](../internals/engine/rng_implementation.md), [animation_system](../internals/engine/animation_system.md), [rtti_class_map](../internals/engine/rtti_class_map.md)

## Reports — производные расчёты

Всё, что считается из `data.json`: бой, экономика, тех-дерево, карта, нации. Индекс — [reports/README.md](reports/README.md).

- **Бой:** [combat_stats](reports/combat/combat_stats.md), [counter_matrix](reports/combat/counter_matrix.md), [attack_rates](reports/combat/attack_rates.md), [vision_radii](reports/combat/vision_radii.md), [artillery](reports/combat/artillery.md)
- **Экономика:** [scaling_prices](reports/economy/scaling_prices.md), [efficiency_upgrades](reports/economy/efficiency_upgrades.md), [production_rates](reports/economy/production_rates.md), [construction_times](reports/economy/construction_times.md), [builder_slots](reports/economy/builder_slots.md)
- **Тех-дерево:** [tech_tree](reports/tech/tech_tree.md)
- **Карта:** [lobby_settings](reports/map/lobby_settings.md), [map_resources](reports/map/map_resources.md), [starting_layout](reports/map/starting_layout.md), [map_predictions_validation](reports/map/map_predictions_validation.md)
- **Нации:** [overview](reports/nations/overview.md), [deviations](reports/nations/deviations.md) — side-by-side сравнения всех 21

## Сырой JSON и engine-дампы

- [`../data.json`](../data.json) — мастер-данные (~4.7 МБ), выход `parser/build_data.py`. Все writer-скрипты читают отсюда.
- [`../derived/`](../derived/) — специализированные JSON-датасеты ([README](../derived/README.md)): tech_tree, builder_slots, animations, game_settings, canonical_terms, pattern_*, replay_ground_truth, плюс engine-RE дампы (4856 native сигнатур, exe_strings, primitives).

## Регенерация

После патча игры или изменений в скриптах — `python scripts/regen.py all` (полный круг, ~4 мин). Точечно:

```
python scripts/regen.py reference        # только writers/
python scripts/regen.py reports-economy  # только economy-отчёты
python scripts/regen.py sanity           # parser + 112 авто-проверок
python scripts/regen.py help             # все targets
```

Полный список команд для регенерации — в `README.md` корня репо.

## Стат

- Нации: **21**
- Здания: **456** строк (sid×nation)
- Юниты: **714** строк
- Апгрейды: **4429** строк (с полными cost/value/itype)
- Офицеры: **231** групп
- Sanity checks: **112/112** PASS