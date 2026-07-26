<a id="cossacks-3--каталог-артефактов"></a>
# Cossacks 3 — documentation catalog

**English** · [Русский](../docs/README.md)

_Extracted **2026-05-17 12:33:30** (local) from game files (unit.script mtime: 2026-04-28 03:32:28)._

All generated files for the game reference. Main entry point.

<a id="начни-здесь"></a>
## Start here

**[reference/README.md](reference/README.md)** — structured game reference: formulas, topical chapters, 21 nations, and 16 comparisons.

**[architecture.md](architecture.md)** — project data flow: where each dataset comes from and which script generates it. Read this **before** adding a report or editing a generator.

**[known_issues.md](known_issues.md)** — parser gaps, discrepancies with external guides, and open empirical questions. Resolved issues are archived in [known_issues_archive.md](known_issues_archive.md). Read this **before** building a tool on top of `data.json`.

<a id="структура-docs"></a>
## `docs_en/` structure

This catalog contains player-facing, human-readable material. Machine dumps and developer documentation live at the repository root ([`../data.json`](../data.json), [`../derived/`](../derived/), and [`../internals_en/`](../internals_en/)).

```
docs_en/
├── README.md              ← this catalog
│
├── reference/             ← generated canonical game reference
│   ├── README.md          ← overview, index, and glossary
│   ├── 01_economy/README.md … 07_naval/README.md  ← 7 topical chapters
│   ├── nations/           ← 21 nation cheat sheets
│   └── compare/           ← side-by-side unit and building comparisons
│
├── recon/                 ← in-depth, handwritten mechanics research
│   ├── README.md          ← index and reading guide
│   ├── world/
│   │   ├── economy/       gathering, construction, capture, famine, queues, upgrades
│   │   ├── combat/        damage, formations, target selection, towers, walls,
│   │   │                  artillery, naval combat, vision, ranged-unit behavior
│   │   └── map/           map generation and game settings
│   └── systems/           ai_behavior, mercenaries_diplomacy, victory_conditions,
│                          scenarios_and_triggers, ui_input_and_feedback
│
└── reports/               ← derived calculations grouped by topic
    ├── README.md
    ├── combat/            DPS, counter matrix, attack rates, vision, artillery
    ├── economy/           scaling, builder_slots, construction, production, efficiency
    ├── tech/              tech tree
    ├── map/               map resources, starting layout, replay validation
    └── nations/           overview, deviations
```
<a id="reference--каноническая-справка"></a>
## Reference — canonical game data

[**reference/**](reference/) contains topical chapters, a cheat sheet for every nation, and side-by-side comparisons. Start with [reference/README.md](reference/README.md).

- **Chapters:** [01_economy](reference/01_economy/README.md), [02_combat](reference/02_combat/README.md), [03_buildings](reference/03_buildings/README.md), [04_units](reference/04_units/README.md), [05_upgrades](reference/05_upgrades/README.md), [06_market](reference/06_market/README.md), [07_naval](reference/07_naval/README.md)
- **Nations:** [reference/nations/](reference/nations/README.md) — 21 nations, one cheat sheet each
- **Comparisons:** [reference/compare/](reference/compare/README.md) — pikemen, musketeers, cavalry, ships, artillery, and more

<a id="recon--глубокие-исследования"></a>
## Recon — in-depth research

[**recon/**](recon/README.md) reverse-engineers key mechanics. Each document is self-contained and cites specific lines from the game scripts.

- **Logic of the world - economics:** [peasant_extraction](recon/world/economy/peasant_extraction.md), [building_mechanics](recon/world/economy/building_mechanics.md), [capture_mechanics](recon/world/economy/capture_mechanics.md), [hunger_and_rebellion](recon/world/economy/hunger_and_rebellion.md), [production_queue](recon/world/economy/production_queue.md), [upgrades_application](recon/world/economy/upgrades_application.md)
- **World logic - combat:** [combat_damage_pipeline](recon/world/combat/combat_damage_pipeline.md), [target_selection](recon/world/combat/target_selection.md), [formations](recon/world/combat/formations.md), [pathfinding](recon/world/combat/pathfinding.md), [unit_commands](recon/world/combat/unit_commands.md), [ranged_units_behavior](recon/world/combat/ranged_units_behavior.md), [vision_and_fow](recon/world/combat/vision_and_fow.md), [towers](recon/world/combat/towers.md), [walls_and_gates](recon/world/combat/walls_and_gates.md), [artillery_specifics](recon/world/combat/artillery_specifics.md), [naval_combat](recon/world/combat/naval_combat.md)
- **Logic of the world - map:** [map_generation_pipeline](recon/world/map/map_generation_pipeline.md), [game_settings](recon/world/map/game_settings.md)
- **Game systems:** [ai_behavior](recon/systems/ai_behavior.md), [mercenaries_diplomacy](recon/systems/mercenaries_diplomacy.md), [victory_conditions](recon/systems/victory_conditions.md), [scenarios_and_triggers](recon/systems/scenarios_and_triggers.md), [ui_input_and_feedback](recon/systems/ui_input_and_feedback.md)
- **Engine internals (highlighted in [`../internals/`](../internals_en/)):** [ticks_and_subticks](../internals_en/engine/ticks_and_subticks.md), [determinism_audit](../internals_en/engine/determinism_audit.md), [server_sync_architecture](../internals_en/engine/server_sync_architecture.md), [native_api](../internals_en/engine/native_api.md), [rng_implementation](../internals_en/engine/rng_implementation.md), [animation_system](../internals_en/engine/animation_system.md), [rtti_class_map](../internals_en/engine/rtti_class_map.md)

<a id="reports--производные-расчёты"></a>
## Reports — derived calculations

Calculations based on `data.json`, covering combat, economy, the technology tree, maps, and nations. See the [report index](reports/README.md).

- **Combat:** [combat_stats](reports/combat/combat_stats.md), [counter_matrix](reports/combat/counter_matrix.md), [attack_rates](reports/combat/attack_rates.md), [vision_radii](reports/combat/vision_radii.md), [artillery](reports/combat/artillery.md)
- **Economy:** [scaling_prices](reports/economy/scaling_prices.md), [efficiency_upgrades](reports/economy/efficiency_upgrades.md), [production_rates](reports/economy/production_rates.md), [construction_times](reports/economy/construction_times.md), [builder_slots](reports/economy/builder_slots.md)
- **Tech tree:** [tech_tree](reports/tech/tech_tree.md)
- **Map:** [lobby_settings](reports/map/lobby_settings.md), [map_resources](reports/map/map_resources.md), [starting_layout](reports/map/starting_layout.md), [map_predictions_validation](reports/map/map_predictions_validation.md)
- **Nations:** [overview](reports/nations/overview.md), [deviations](reports/nations/deviations.md) - side-by-side comparisons of all 21

<a id="сырой-json-и-engine-дампы"></a>
## Raw JSON and engine dumps

- [`../data.json`](../data.json) — master dataset (~5.7 MB), generated by `parser/build_data.py`. All reference writers read from it.
- [`../derived/`](../derived/) — specialized JSON datasets ([README](../derived/README.en.md)): `tech_tree`, `builder_slots`, animations, game settings, canonical terms, `pattern_*`, replay ground truth, and engine reverse-engineering dumps (4,856 native signatures, executable strings, and primitives).

<a id="регенерация"></a>
## Regeneration

After a game patch or a script change, run `python scripts/regen.py all` for a full rebuild (about four minutes). For targeted regeneration:

```
python scripts/regen.py reference        # writers only
python scripts/regen.py reports-economy  # economy reports only
python scripts/regen.py sanity           # parser + 112 automatic checks
python scripts/regen.py help             # list all targets
```
The repository root `README.md` contains the complete command list.

<a id="стат"></a>
## Statistics

- Nations: **21**
- Buildings: **456** lines (sid×nation)
- Units: **714** lines
- Upgrades: **4483** lines (with full cost/value/itype)
- Officers: **231** groups
- Sanity checks: **112/112** PASS
