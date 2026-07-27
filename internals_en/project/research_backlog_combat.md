<a id="план-исследований-боевые-механики"></a>
# Research Backlog: Combat Mechanics

[Русский](../../internals/project/research_backlog_combat.md) · **English**

[← Project architecture and maintenance](README.md)

This document tracks questions for which the available scripts, data, and
observations do not yet support a reliable player-facing rule. It is a
technical experiment plan, not part of the encyclopedia.

Every result should record the game version, match settings, initial objects,
number of repetitions, and raw observations. Once a conclusion is confirmed,
it belongs in the relevant encyclopedia article and the completed item should
be removed from this list.

<a id="артиллерия"></a>
## Artillery

Related article:
[Artillery](../../docs_en/recon/world/combat/artillery_specifics.md).

1. **Minimum range by artillery type.** `data.json` contains both
   `radiusmin = 0`, which permits point-blank fire, and values of five cells
   or more. Controlled measurements are needed to establish how each value
   behaves in play.
2. **Total area-damage cap.** The current estimate is the equivalent of
   damaging three to five units. Compare one salvo against groups of 1, 5,
   10, and 30 units.

<a id="расчёт-урона"></a>
## Damage Calculation

Related article:
[How the Game Calculates Damage](../../docs_en/recon/world/combat/combat_damage_pipeline.md).

1. **Exact area-damage cap.** The limiting coefficient in
   `_misc_DoRoundDamage` remains unknown. Fire a series of grenades at groups
   of 1, 5, 10, 20, and 50 units and record the total damage.
2. **The fourth peacetime case.** Test the combination in which the attacker
   stands on friendly territory, the target stands on foreign territory, and
   the script branch indicates that both objects die. If the test confirms a
   defect, record it under [known limitations](known_issues.md).
3. **Headshots after negative intermediate damage.** Determine whether the
   bonus is added directly to the negative value or after damage is clamped
   to a minimum of one: `damage = 200` versus
   `damage = max(1, ...) + 200`. This requires either a complete analysis of
   the `_misc_DoDamage` branch or a controlled in-game test.

<a id="построения"></a>
## Formations

Related article:
[Formations](../../docs_en/recon/world/combat/formations.md).

1. **Overlapping formation bonuses.** Test whether one unit can receive
   bonuses from two formations simultaneously. The structure of `TSquad`
   suggests that it stores only one set of bonuses, but this needs a
   controlled measurement.
2. **The effect of `symmetry = 3`.** Use the editor to record the position of
   right-flank cavalry after the squad turns 180° and its layout is mirrored
   on both axes.
3. **Time required to change formation.** A full rearrangement currently
   appears to take 0.4–0.6 game seconds. Measure how squad size and
   pathfinding complexity affect that time.

<a id="морской-бой"></a>
## Naval Combat

Related article:
[Naval Combat](../../docs_en/recon/world/combat/naval_combat.md).

1. **How far inland a ship can fire.** The boundary depends on the movement
   region assigned to the shoreline; measure it on several maps.
2. **Regeneration of fish sources.** Run a long controlled match after
   fully depleting a source and search `lib/res.script` for the handler that
   would restore it.

<a id="стрелковые-юниты"></a>
## Ranged Units

Related article:
[Ranged-Unit Behavior](../../docs_en/recon/world/combat/ranged_units_behavior.md).

1. **Retreat direction.** Determine whether a ranged unit retreats directly
   away from its enemy or whether `RunAway` follows a more complex
   path-selection rule. Record trajectories from a set of identical scenes.
2. **Canister range after movement.** Current evidence indicates that canister
   does not receive the movement penalty, while its minimum range is normally
   zero. Verify that its maximum range, `radiusmax`, also remains unchanged.
3. **Archer elevation and area damage.** Test whether the `goHeight × 2`
   adjustment affects the search for a building hit by a Fire Arrow from
   high ground, or only the search for units.

<a id="башни-и-форты"></a>
## Towers and Forts

Related article: [Towers](../../docs_en/recon/world/combat/towers.md).

1. **Garrison fire from forts.** Forts in Historical Battles and campaigns
   can accept infantry but are not the standard Tower type `tow`. Their
   behavior requires a separate review of scenario scripts.

<a id="приказы-юнитов"></a>
## Unit Orders

Related article:
[Unit Orders](../../docs_en/recon/world/combat/unit_commands.md).

1. **The two order-queue limits.** The shared object-order list has 12 slots,
   while the lower-level unit queue is described as having 32. Determine
   which limit applies to a sequence of player commands and where the other
   limit is used.
2. **Resetting `STO` and `STP` on a new order.** Determine whether these
   caches survive between orders and how long a unit remembers its previous
   enemy after receiving a new command.

<a id="поиск-пути"></a>
## Pathfinding

Related article:
[Pathfinding](../../docs_en/recon/world/combat/pathfinding.md).

1. **Native search algorithm.** The scripts do not reveal whether the engine
   uses A*, a flow field, wave propagation, or another graph-search method.
   Analyze the relevant `TOSWPath*` functions or compare their behavior on
   controlled maps.
2. **Effect of the squad tag.** Test whether the floating-point `squad-tag`
   passed by the scripts changes the route returned for units in one
   formation.
3. **Repathing after a new obstacle appears.** No explicit repath request has
   been found in the scripts. Place a building on an active route and record
   whether the unit stops or finds a new path.

<a id="обзор-и-туман-войны"></a>
## Vision and Fog of War

Related article:
[Vision and Fog of War](../../docs_en/recon/world/combat/vision_and_fow.md).

1. **How the radius maps to game cells.** The script returns a value in the
   fog-of-war system's internal unit. Reading it as a number of cells matches
   observation but still needs a controlled measurement.
2. **Vision update rate.** Determine whether the visible area is recalculated
   every frame or at a fixed interval. Fast cavalry should make any delay
   easiest to detect.
3. **Fog-of-war memory.** Establish which object information remains in an
   explored area after it leaves current vision. The working hypothesis is
   that terrain persists while units and buildings require current vision.

<a id="стены-и-ворота"></a>
## Walls and Gates

Related article:
[Walls and Gates](../../docs_en/recon/world/combat/walls_and_gates.md).

1. **Cost of a long Wall.** Determine whether `costpercent` applies to every
   segment separately or once to the entire drawn line.
2. **Segment construction rate.** `wallvariation = 0` uses the ordinary
   formula, while the other variations use explicit `builderPoints`.
   Measure every variation with different numbers of Peasants.
3. **Breaking the Wall while a segment becomes a Gate.** Test whether the
   Gate remains in the Wall cluster when neighboring segments are destroyed
   before the upgrade completes, or becomes a detached building.
