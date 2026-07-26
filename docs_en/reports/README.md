<a id="расчётные-отчёты-derived-reports"></a>
# Derived reports

Derivative calculations based on [`../../data.json`](../../data.json) - something that cannot be read directly from game scripts and needs to be calculated. Grouped by topic; index below.

<a id="бой-combatcombat"></a>
## Fight ([`combat/`](combat/))

| File | What's inside | Generator |
|---|---|---|
| [combat/combat_stats.md](combat/combat_stats.md) | DPS and effective HP (EHP) by weapon type for all combat units. | `compute/compute_combat_stats.py` |
| [combat/counter_matrix.md](combat/counter_matrix.md) | Approximate TTK (time-to-kill) between unit classes, taking into account defense and hit. | `compute/compute_counter_matrix.py` |
| [combat/attack_rates.md](combat/attack_rates.md) | Unit attack speed: cycle duration (pause or attack0 animation), attacks/g-sec, attacks/real @ fast. | `compute/compute_attack_rates.py` |
| [combat/vision_radii.md](combat/vision_radii.md) | Vision (FOW) and searchradius for all units. Formula `floor(20 + 4×vision)` tiles. The best scouts (Drummer, 17th century, Hetman, ships). | `compute/compute_vision.py` |
| [combat/artillery.md](combat/artillery.md) | Land Artillery Summary (`bartillery = True`): damage, pause, dispertion, cost per shot, fleet limit from the Artillery Depot, unit economics and national differences. | `compute/compute_artillery.py` |

<a id="экономика-economyeconomy"></a>
## Economy ([`economy/`](economy/))

| File | What's inside | Generator |
|---|---|---|
| [economy/scaling_prices.md](economy/scaling_prices.md) | Price of the Nth building instance: `cost(N) = floor(base × (costpercent/100)^(N-1))`. Tables N=1..6. | `compute/compute_scaling.py` |
| [economy/efficiency_upgrades.md](economy/efficiency_upgrades.md) | Summary of `gc_upg_type_effect*` - which upgrades add what (food/wood/stone/damage/protection/range). | `compute/compute_efficiency_upgrades.py` |
| [economy/production_rates.md](economy/production_rates.md) | For each nation × building × unit: `buildtime`, `units/g-min`, `units/real-min @ fast`, price and upkeep. | `compute/compute_tech_tree.py` |
| [economy/construction_times.md](economy/construction_times.md) | Construction time of each building with 1, 2, 5, 10 builders and at maximum slots. | `compute/compute_construction_times.py` |
| [economy/builder_slots.md](economy/builder_slots.md) | How many peasants can build a building at the same time (calculated by walking around the mask perimeter in steps of `gc_BuilderDist=1.0`). | `compute/compute_builder_slots.py` |

<a id="тех-дерево-techtech"></a>
## Tech tree ([`tech/`](tech/))

| File | What's inside | Generator |
|---|---|---|
| [tech/tech_tree.md](tech/tech_tree.md) | Wood dependencies: for each building/unit/upgrade - a list of prerequisites (`[B]` building, `[U]` unit, `[T]` upgrade). Machine version - `../../derived/tech_tree.json`. | `compute/compute_tech_tree.py` |

<a id="карта-mapmap"></a>
## Map ([`map/`](map/))

| File | What's inside | Generator |
|---|---|---|
| [map/lobby_settings.md](map/lobby_settings.md) | All lobby options with canonical Russian names from the game locale (terrain, resources, peace time, population limit, AI difficulty - 95 values ​​in 18 categories). | `compute/compute_game_settings.py` |
| [map/map_resources.md](map/map_resources.md) | Counting forests, stones and mines on the standard map Small + Highlands + Rich. About 109 large trees, 33 stones, up to 12 deposits per player. | `compute/compute_map_resources.py` |
| [map/starting_layout.md](map/starting_layout.md) | Starting layout: 18 peasants in a 6x3 grid near the City Center, location `cen` / `sto` / mines. | `compute/compute_starting_layout.py` |
| [map/map_predictions_validation.md](map/map_predictions_validation.md) | Validation of the `compute_map_resources` model against the ground truth replay (10 homogeneous replays Small + Land + Highlands). | `compute/validate_map_predictions.py` |

## Nations ([`nations/`](nations/))

| File | What's inside | Generator |
|---|---|---|
| [nations/overview.md](nations/overview.md) | Side-by-side comparison of all 21 nations: roster size, access to the 18th century, unique units, stat anomalies, mercenaries, market cluster. | `compute/compute_nations_overview.py` |
| [nations/deviations.md](nations/deviations.md) | Full stat fingerprints of common buildings (`<nat>cen`, `<nat>aca`, `<nat>art`, etc.) and common units: which nations deviate from the base case and in what ways. Complements overview.md in detail. | `compute/compute_nation_deviations.py` |

## Linked data

- [`../reference/`](../reference/README.md) - canonical help (chapters 01–07, `nations/`, `compare/`). The reports above are built on top of it.
- [`../recon/`](../recon/README.md) - deep research into the mechanics on which these reports are based.
- [`../../derived/`](../../derived/) - machine-readable JSON datasets (`tech_tree.json`, `builder_slots.json`, `pattern_*.json`, `animations.json`).

## Regeneration

After updating `data.json`:
```bash
python compute/compute_combat_stats.py        # → reports/combat/combat_stats.md
python compute/compute_counter_matrix.py      # → reports/combat/counter_matrix.md
python compute/compute_attack_rates.py        # → reports/combat/attack_rates.md
python compute/compute_vision.py              # → reports/combat/vision_radii.md
python compute/compute_artillery.py           # → reports/combat/artillery.md
python compute/compute_scaling.py             # → reports/economy/scaling_prices.md
python compute/compute_efficiency_upgrades.py # → reports/economy/efficiency_upgrades.md
python compute/compute_builder_slots.py       # → reports/economy/builder_slots.md (+derived/builder_slots.json)
python compute/compute_construction_times.py  # → reports/economy/construction_times.md
python parser/build_tech_graph.py             # → derived/tech_tree.json
python compute/compute_tech_tree.py           # → reports/tech/tech_tree.md, reports/economy/production_rates.md
python compute/compute_game_settings.py        # → reports/map/lobby_settings.md (+derived/game_settings.json)
python compute/compute_map_resources.py        # → reports/map/map_resources.md
python compute/compute_starting_layout.py     # → reports/map/starting_layout.md
python compute/validate_map_predictions.py     # → reports/map/map_predictions_validation.md
python compute/compute_nations_overview.py     # → reports/nations/overview.md
python compute/compute_nation_deviations.py    # → reports/nations/deviations.md
```
