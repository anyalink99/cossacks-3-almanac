<a id="как-устроена-игра"></a>
# How the Game Works

[← Encyclopedia home](../README.md)

This section explains not only **how much**, but also **why**. It covers the
hidden rules of Cossacks 3: a peasant’s trip to the storehouse, target
selection, formations, building capture, order queues, map generation, and
computer-player behavior.

Articles can be read independently. Canonical names are used in the main text;
internal identifiers and function names remain in notes where they are useful
for verification.

<a id="экономика-и-строительство"></a>
## Economy and construction

| Article | What it explains |
|---|---|
| [Peasant resource gathering](world/economy/peasant_extraction.md) | The full work cycle, delivery, mines, fields, and gathering upgrades. |
| [Construction and repair](world/economy/building_mechanics.md) | Building placement, builder limits, construction time, repair, and destruction. |
| [Capturing objects](world/economy/capture_mechanics.md) | Which buildings and units can be captured and how defenders are checked. |
| [Applying upgrades](world/economy/upgrades_application.md) | How bonuses affect existing and future units and how multiple upgrades combine. |
| [Famine and mercenary rebellion](world/economy/hunger_and_rebellion.md) | When shortages of food or gold begin to destroy an army. |
| [Production queues](world/economy/production_queue.md) | Orders, infinite production, payment, cancellation, and refunds. |
| [Market](../reference/06_market/README.md) | Exchange formulas, rate changes, and practical conclusions. |

<a id="бой-движение-и-приказы"></a>
## Combat, movement, and orders

| Article | What it explains |
|---|---|
| [Damage calculation](world/combat/combat_damage_pipeline.md) | Base damage, armor, weapon-type protection, formation bonuses, and critical hits. |
| [Formations](world/combat/formations.md) | Line and square formations, valid group sizes, and combat bonuses. |
| [Target selection](world/combat/target_selection.md) | Which enemy a unit attacks first and how attack-move works. |
| [Unit orders](world/combat/unit_commands.md) | Move, attack, patrol, guard, garrison, and command queues. |
| [Pathfinding](world/combat/pathfinding.md) | How individual units and formations navigate around obstacles. |
| [Ranged-unit behavior](world/combat/ranged_units_behavior.md) | Shot preparation, retreat, multiple weapons, and elevation bonuses. |
| [Towers](world/combat/towers.md) | Target selection, shot cost, upgrades, and capture while under construction. |
| [Walls and gates](world/combat/walls_and_gates.md) | Wall segments, construction, converting a wall segment into a gate, and demolition. |
| [Artillery](world/combat/artillery_specifics.md) | Shot preparation, area damage, and artillery limits. |
| [Naval combat](world/combat/naval_combat.md) | Sea combat, transports, fishing, and special ships. |
| [Vision and fog of war](world/combat/vision_and_fow.md) | Sight radius, shared allied vision, and temporary projectile vision. |

<a id="карта-и-правила-матча"></a>
## Map and match rules

| Article | What it explains |
|---|---|
| [Random-map generation](world/map/map_generation_pipeline.md) | Terrain, water, forests, stone, mines, and starting-position placement. |
| [Match settings](world/map/game_settings.md) | How lobby options change map generation and the rules of a match. |

<a id="игровые-системы"></a>
## Game systems

| Article | What it explains |
|---|---|
| [Computer-player behavior](systems/ai_behavior.md) | Economy, construction, army recruitment, and military target selection. |
| [Mercenaries and the Diplomatic Center](systems/mercenaries_diplomacy.md) | Recruitment, rising prices, and rebellion when gold runs out. |
| [Victory and defeat](systems/victory_conditions.md) | Player elimination, surrender, team play, and scenario conditions. |
| [Scenarios and event rules](systems/scenarios_and_triggers.md) | Conditions and actions used to build missions. |
| [Controls and feedback](systems/ui_input_and_feedback.md) | How clicks, hotkeys, and interface commands become game orders. |

---

Project architecture, network protocols, file formats, and extraction
limitations are documented in [Technical documentation](../../internals_en/README.md).
