<a id="known-issues-и-оговорки"></a>
# Known Issues and Caveats

This page collects four kinds of limitation:

- **Parser gaps:** places where `data.json` does not yet reproduce the game
  files completely.
- **Disagreements with external sources:** values that differ from popular
  guides or calculators. The game scripts remain the source of truth.
- **Open empirical questions:** formulas or interpretations that still require
  an in-game measurement.
- **Edge cases:** verified behavior that is easy to overlook.

The list changes as the parser and the research improve. Resolved entries move
to the [archive](known_issues_archive.md), where the original problem and its
correction remain available for reference.

---

<a id="парсерные-пробелы-datajson"></a>
## Parser gaps in `data.json`

<a id="weapons-у-зданий-пока-не-извлекаются-полностью"></a>
### Multiple building weapons are not fully extracted

Building rows in `data.json` contain the scalar fields `weapon_damage`,
`weapon_pause_frames`, `weapon_radiusmax`, `weapon_kind`, and `weapon_cost`.
If a mod gives one building multiple weapons, the parser currently records only
the first.

All combat-capable buildings in the unmodified game, including towers and the
shipyard, use a single weapon. The limitation therefore does not affect the
current reference, but it remains relevant to modded data.

<a id="сценарные-триггеры-не-парсятся"></a>
### Scenario triggers are not parsed

The pipeline does not parse `data/scripts/lib/scenario.script`, which defines
triggers used by scenarios, campaigns, and historical battles. Conclusions
about scenario actions and victory conditions were extracted manually.

See [Victory and defeat](../../docs_en/recon/systems/victory_conditions.md)
for the reader-facing explanation.

---

<a id="расхождения-с-внешними-источниками"></a>
## Discrepancies with external sources

Several values in this encyclopedia differ from values quoted by older guides
and calculators. When they disagree, this project follows the scripts from the
installed game version.

| Fact | Value found elsewhere | Value in the game files | Source | Conclusion |
|---|---|---|---|---|
| `hits_needed` for food | 30 | **22** | `dmscript.global:799`, `gc_resource_hitsneeded_food` | A peasant performs 22 work cycles before returning to a storehouse, not 30. The shorter cycle raises the practical gathering rate. |
| Cost of `aca.4` (Field Melioration) | W1400/G522 | **W1000/G475** for every nation | `country.script:3490`, `_country_AddUpgrade('aca.4', ..., wood=1000, gold=475)` | All 21 nations use the same price. The external value probably belongs to an older game version. |
| Cost of “Manufacture Agricultural Equipment” at the Blacksmith | W400/G100 | **Not present at the Blacksmith** | `country.script` | The current Blacksmith offers unit damage and protection upgrades. The named upgrade may come from an earlier Cossacks title; related economic upgrades are researched at the Academy in Cossacks 3. |

The reference also documents several familiar RTS mechanics that Cossacks 3
does **not** implement: a charge bonus, a universal anti-cavalry multiplier, a
drummer aura, a special grenade trajectory, and stealth. See
[Combat and movement](../../docs_en/reference/02_combat/README.md) for the
verified combat rules.

---

<a id="edge-cases--что-легко-проглядеть"></a>
## Edge cases that are easy to overlook

- **Builder limits for the four storehouse variants.** The European Storehouse
  (`eursto`) uses a special union of linear support masks rather than the usual
  perimeter calculation. Its limit is eight builders; a plain perimeter model
  would incorrectly predict nine. Gates cannot be built by peasants at all.
  See `compute/compute_builder_slots.py`.
- **Building `buildtime` uses an additional multiplier.**
  `gc_buildtime_modifier = 10`, so the duration in game seconds is
  `frames × 10 / 32`, not `frames / 32` as it is for units. The normalized
  value is already stored in `data.json` as `buildtime_sec`; the warning
  applies when reading raw frames.
- **Mercenary rebellion accelerates sharply on Hard and above.** The condition
  `_misc_RandomInt < 6000` gives an 18.31% chance of desertion on each
  `Nothing` tick, roughly every 0.625 game seconds. With `brebellion = True`,
  a force of 50 mercenaries can disappear almost completely within 5–10 game
  seconds. On Easy and Normal, the corresponding chances are only 0.305% and
  0.610%.
- **`farmused` does not fall to zero while the player owns either a peasant or
  a Town Hall.** A player can survive with a single peasant and a Mill without
  being eliminated. See
  [Victory and defeat](../../docs_en/recon/systems/victory_conditions.md).
- **The sight-radius formula is `20 + 4 × vision` cells.** Even `vision = 0`
  therefore gives a radius of 20 cells rather than no vision.
- **Population capacity is
  `cen × 100 + bar × 150 + ba2 × 250 + hou × 25`,** but the map also imposes a
  global limit between 500 and 8,000 according to map size. Once that cap is
  reached, additional houses no longer increase usable capacity.
- **`foreststype = 0` on Land maps.** Even when Random Forests is selected in
  the lobby, `dogenerate.inc:6` forces zero for the Land map type. Other map
  types interpret the setting differently.
- **Score does not decide victory.** It is used for statistics and rating.
  Standard matches end when only one player or allied team remains. Cossacks 3
  has no Wonder victory condition.

---

## Open empirical questions

The script code does not answer every question below. Each item names the
article that explains what is known and what an in-game experiment still needs
to measure.

<a id="добыча-и-экономика--reconworldeconomypeasantextractionmdreconworldeconomypeasantextractionmd-9"></a>
<a id="добыча-и-экономика--reconworldeconomypeasantextractionmddocsreconworldeconomypeasantextractionmd-9"></a>
### Resource gathering — [Peasant resource gathering](../../docs_en/recon/world/economy/peasant_extraction.md)

- The exact `loss_factor`: the share of working time lost while walking to a
  storehouse under different map layouts.
- The practical gathering rate after the peasant's random target selection.
  Across repeated five-minute runs from one save, the observed coefficient of
  variation is about 5–15% for wood and stone and approximately zero for
  mines.
- The exact `K` coefficient for trees per map pattern. The current value,
  0.30, is calibrated against Small = 10 and Large = 50; a stronger estimate
  requires repeated map generation and environment parsing.

<a id="ии--reconsystemsaibehaviormdreconsystemsaibehaviormd-открытые-вопросы"></a>
<a id="ии--reconsystemsaibehaviormddocsreconsystemsaibehaviormd-открытые-вопросы"></a>
### Computer player — [How the Computer Player Works](../../docs_en/recon/systems/ai_behavior.md)

- Where and how the aggressor pool is replenished through
  `aiData.agressors.Add`.
- What activates `bhumanai`; no setter has been found in the scripts, so it may
  be controlled by the engine or interface.
- The exact meaning of `gc_ai_max_guards = 120`, which appears to be headroom
  above a pikeman threshold.
- The condition that changes `centerfound` to `True`.
- Whether difficulty affects attack frequency beyond construction and
  recruitment speed. Aggressor and sabotage triggers use the same constants,
  so this requires an in-game comparison.

<a id="захват--reconworldeconomycapturemechanicsmdreconworldeconomycapturemechanicsmd-9"></a>
<a id="захват--reconworldeconomycapturemechanicsmddocsreconworldeconomycapturemechanicsmd-9"></a>
### Capture — [Capturing objects](../../docs_en/recon/world/economy/capture_mechanics.md)

- Which point `(px, py)` represents a building during the distance check: the
  model center, bounding-box center, or anchor point.
- Whether `bAutoKill` is legacy code. It is declared but never assigned in
  `_misc_CheckCapture`.
- Why `_unit_SearchCapturersForWall` does not require `bcancapture`, and
  whether peasants or artillery can therefore destroy a wall through the
  capture path.

<a id="pathfinding--reconworldcombatpathfindingmddocsreconworldcombatpathfindingmd-9"></a>
### Pathfinding — [Pathfinding](../../docs_en/recon/world/combat/pathfinding.md)

- Which native search algorithm is used: A*, a flow field, wave propagation,
  or another graph method.
- Whether the floating-point squad tag changes the route returned for units in
  the same formation.
- What happens when a new obstacle appears on an active route. No explicit
  repath request has been found in the scripts.

<a id="rng--детерминизм--internalsenginedeterminismauditmdinternalsenginedeterminismauditmd"></a>
<a id="генератор-случайных-чисел-и-детерминизм--determinismauditmdenginedeterminismauditmd"></a>
### Random-number generation and determinism — [Determinism audit](../engine/determinism_audit.md)

- Whether the global `random` cursor is stored in a saved game. Current
  evidence suggests that it is not.
- Native pathfinding tie-breaking.
- The effect of the engine's variable time step.

<a id="генерация-карты--reconworldmapmapgenerationpipelinemddocsreconworldmapmapgenerationpipelinemd-13"></a>
### Map generation — [Random-map generation](../../docs_en/recon/world/map/map_generation_pipeline.md)

- The number of distinct random maps: 230 base pattern layouts multiplied by
  an unknown range of random-key variations.
- How `arrStartPos` is encoded in `inputbitmap.tga`; the engine reads starting
  markers from special RGB values.
- Desert pattern types for `season = 3`, which
  `compute_map_resources.py` does not yet model. They appeared in one of 20
  sampled replays.

---

<a id="где-жалуются-на-ошибки"></a>
## Reporting an error

If the encyclopedia disagrees with what you observe in the game, open an issue
or pull request and include:

- what you observed;
- the game version used for the test;
- the game-script revision represented by the repository, shown in the output
  of `parser/build_data.py`.

This list is intentionally incomplete. Several open questions require direct
measurement in a running game rather than further static analysis.
