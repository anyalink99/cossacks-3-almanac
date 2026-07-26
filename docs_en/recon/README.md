<a id="recon-notes--глубокие-исследования-механик"></a>
# Recon notes - deep research into mechanics

This is a **handwritten** analysis of what is not in `data.json` and what will not be pulled out
autoparser: engine behavior, hidden formulas, edge cases, RNG sites,
network model. All numbers in [`../reference/`](../reference/) are based on
on these documents - “why” lives here, and “how much” lives there.

Documents are divided into three subfolders depending on what **
Exactly** understands. Each file is self-contained; cross references -
obviously via markdown links. The data pipeline in which these are embedded
documents - in [`../architecture.md`](../architecture.md).

<a id="мир-и-карта-что-видит-игрок--worldworld"></a>
## World and map (what the player sees) - [`world/`](world/)

Detailed analyzes of what is happening in the active party: production,
combat, movement, formations, capture, map generation, lobby options.

<a id="экономика"></a>
### Economy

| File | What's inside |
|---|---|
| [world/economy/peasant_extraction.md](world/economy/peasant_extraction.md) | Resource extraction: peasant cycle, formulas, mines (up to 95 absorber), fields, efficiency upgrades, guaranteed starting resources, hemp = endless wood pool. |
| [world/economy/building_mechanics.md](world/economy/building_mechanics.md) | Buildings: footprint mask, repair, construction, builder slots, walls, garrison, captureradius. |
| [world/economy/capture_mechanics.md](world/economy/capture_mechanics.md) | Capture buildings and units - pure geometry. Some are captured, some are not. |
| [world/economy/upgrades_application.md](world/economy/upgrades_application.md) | How the upgrade is applied: to existing units and future ones, additive composition `eff`, `priceperc` / `buildtimeperc`, interruption of research. |
| [world/economy/hunger_and_rebellion.md](world/economy/hunger_and_rebellion.md) | Famine (`bfamine`) and riot (`brebellion`): when the flags are raised, who dies and in what order, protection. |
| [world/economy/production_queue.md](world/economy/production_queue.md) | Production queue: 12 slots, infinite mode, merging orders via `costpercent`, refund when canceled and captured, interrupted by invaders. |
| (Market) | A detailed analysis of the mechanics and exchange formula is for now only in [`../reference/06_market/README.md`](../reference/06_market/README.md). |

<a id="бой-и-команды"></a>
### Combat and teams

| File | What's inside |
|---|---|
| [world/combat/combat_damage_pipeline.md](world/combat/combat_damage_pipeline.md) | Damage pipeline: 6 steps of the formula, headshot, AoE, friendly fire, peace-mode, scenario invulnerability. |
| [world/combat/formations.md](world/combat/formations.md) | LINE / SQUARE / KARE: 149 formations, formation bonuses, hold-mode, mask and symmetry. |
| [world/combat/target_selection.md](world/combat/target_selection.md) | Target selection algorithm via scan-grid: 5 modes, attack-move, 30° cone. |
| [world/combat/unit_commands.md](world/combat/unit_commands.md) | Order queue, modes (move, attack, attack-move, garrison, patrol, guard), hold-mode, hold-fire, rally point, STO/STP. |
| [world/combat/pathfinding.md](world/combat/pathfinding.md) | Pathfinding: A\*-like via `TopologyGetPath`, two-level, collision grid, formations. |
| [world/combat/towers.md](world/combat/towers.md) | Towers: target designation, shot cost, upgrades, capture only during construction. **There is no garrison in the tower in C3** - `peasantabsorber` is placed only at the mines. |
| [world/combat/walls_and_gates.md](world/combat/walls_and_gates.md) | Walls and gates: segments, construction by peasants, builder slots by `wallvariation`, gates as an upgrade `buildgate`, demolition of a segment when attempting to capture. |
| [world/combat/artillery_specifics.md](world/combat/artillery_specifics.md) | Artillery: types (`artind`), `bartprepare`, `attackpoint`, limits through art depot, AoE. |
| [world/combat/naval_combat.md](world/combat/naval_combat.md) | Naval units: port, transport, battleship, fisherman, sea formations, combat from the shore. |
| [world/combat/vision_and_fow.md](world/combat/vision_and_fow.md) | Vision radius (`20 + 4 × vision`), fog of war, allied vision, `fogreveal`-shells. |
| [world/combat/ranged_units_behavior.md](world/combat/ranged_units_behavior.md) | Shooter behavior: standground, bartprepare, RunAway, range penalty, multi-weapon, high ground. |

<a id="карта-и-генерация"></a>
### Map and generation

| File | What's inside |
|---|---|
| [world/map/map_generation_pipeline.md](world/map/map_generation_pipeline.md) | Timeline `DoGenerate`: forbidden zones, `SetupStartingResources`, mines phase-1/2, `FillOwnerMap`, peacetime boundaries, seed space. |
| [world/map/game_settings.md](world/map/game_settings.md) | Lobby options: `gen.*` and `additional.*`, peace-time, century18, balloon. |

<a id="игровые-системы-правила-ai-наёмники-сценарии--systemssystems"></a>
## Game systems (rules, AI, mercenaries, scenarios) - [`systems/`](systems/)

| File | What's inside |
|---|---|
| [systems/ai_behavior.md](systems/ai_behavior.md) | AI: tick 2.4 g-sec, difficulty (from 30% to 125%), build order rule-based, aggressive waves of 5 units. |
| [systems/mercenaries_diplomacy.md](systems/mercenaries_diplomacy.md) | Deep center and mercenaries: 21 nations, 8 types of mercenaries, gold-upkeep, Rebellion 18.31% on hard+. |
| [systems/victory_conditions.md](systems/victory_conditions.md) | Victory and defeat: last-team-standing, defeat by `farmused = 0`, scoreboard for statistics. |
| [systems/scenarios_and_triggers.md](systems/scenarios_and_triggers.md) | Scenarios (`TScenarioTrigger` / `Condition` / `Action` / FSM) - campaign, Historical Battles, peace-mode for the hero. |
| [systems/ui_input_and_feedback.md](systems/ui_input_and_feedback.md) | Interface and input: selection, mouse / keyboard / scroll, cursor, camera, listener for sound. **Sounds and FOW are independent systems** (a unit in the enemy FOW can be heard). Alarm notifications (`_misc_DoAlarm`) are triggered only outside the frustum camera. |

<a id="engine-internals--переехало"></a>
## Engine internals - moved

Documents about the engine design (time model, RNG, network
model, native API DWS) - now in a separate top-level folder
[`../../internals/engine/`](../../internals/engine/). They are too
technical for the average reader of the reference book. If needed:

- [`internals/engine/ticks_and_subticks.md`](../../internals_en/engine/ticks_and_subticks.md) - time model.
- [`internals/engine/determinism_audit.md`](../../internals_en/engine/determinism_audit.md) - RNG audit.
- [`internals/engine/server_sync_architecture.md`](../../internals_en/engine/server_sync_architecture.md) - server-authoritative.
- [`internals/engine/native_api.md`](../../internals_en/engine/native_api.md) - 4,856 native DWS functions.

<a id="когда-что-читать"></a>
## When to read what

- **“Why does this unit extract so much wood?”** → [world/economy/peasant_extraction.md](world/economy/peasant_extraction.md).
- **“How many peasants can build building X at the same time?”** → [world/economy/building_mechanics.md](world/economy/building_mechanics.md) §3.
- **“How many mines will I have at the start?”** → [world/economy/peasant_extraction.md §8.3](world/economy/peasant_extraction.md) or [world/map/map_generation_pipeline.md §8](world/map/map_generation_pipeline.md).
- **“Why does the same save give different loot when rebooting?”** → [internals/engine/determinism_audit.md](../../internals_en/engine/determinism_audit.md) §7.
- **“Why is `random` used in one place and `RandomExt` in another?”** → [internals/engine/server_sync_architecture.md](../../internals_en/engine/server_sync_architecture.md) §1.3 + [internals/engine/determinism_audit.md](../../internals_en/engine/determinism_audit.md) §1.
- **“The map is the same - what does this mean formally?”** → [world/map/map_generation_pipeline.md §12](world/map/map_generation_pipeline.md) (seed space).
- **“When does AI attack me?”** → [systems/ai_behavior.md](systems/ai_behavior.md) §“Aggression / attack triggers”.
- **“Is it possible to capture the tower?”** → [world/economy/capture_mechanics.md](world/economy/capture_mechanics.md) §6.
- **“How to win a game?”** → [systems/victory_conditions.md](systems/victory_conditions.md) §3.
- **“How do mercenaries / Rebellion work?”** → [systems/mercenaries_diplomacy.md](systems/mercenaries_diplomacy.md) §§3-4.
- **“How do units move in formation?”** → [world/combat/pathfinding.md](world/combat/pathfinding.md) §6.
- **“Who will my musketeer shoot at if there are three enemies in a radius?”** → [world/combat/target_selection.md](world/combat/target_selection.md) §3.
- **“How does `attack-move` differ from normal movement?”** → [world/combat/target_selection.md](world/combat/target_selection.md) §5.
- **“What options are there in the lobby and what do they give?”** → tables in [`../reports/map/lobby_settings.md`](../reports/map/lobby_settings.md), engine behavior in [world/map/game_settings.md](world/map/game_settings.md). Native JSON for editors is [`../../derived/game_settings.json`](../../derived/game_settings.json).

<a id="что-не-в-этой-папке"></a>
## What is NOT in this folder

- Ready price / HP / damage tables - in [`../reference/`](../reference/).
- Derivative calculations (DPS, EHP, scaling, tech tree, vision, etc.) - in [`../reports/`](../reports/README.md).
- Open empirical questions for in-game measurements - built into §9 of each profile document.
