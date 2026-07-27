<a id="known-issues-и-оговорки"></a>
<a id="известные-ограничения-и-оговорки"></a>
# Known Issues and Caveats

**English** · [Русский](../../internals/project/known_issues.md)

This page collects three kinds of limitation:

- **Parser gaps:** places where `data.json` does not yet reproduce the game
  files completely.
- **Disagreements with external sources:** values that differ from popular
  guides or calculators. The game scripts remain the source of truth.
- **Edge cases:** verified behavior that is easy to overlook.

The list changes as the parser and the research improve. Resolved entries move
to the [archive](known_issues_archive.md), which preserves the technical
history of each correction.

---

<a id="парсерные-пробелы-datajson"></a>
## Parser gaps in `data.json`

<a id="weapons-у-зданий-пока-не-извлекаются-полностью"></a>
<a id="оружие-зданий-пока-извлекается-не-полностью"></a>
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

The reference also documents several familiar RTS mechanics that Cossacks 3
does **not** implement: a charge bonus, a universal anti-cavalry multiplier, a
drummer aura, a special grenade trajectory, and stealth. See
[Combat and movement](../../docs_en/reference/02_combat/README.md) for the
verified combat rules.

---

<a id="edge-cases--что-легко-проглядеть"></a>
<a id="особые-случаи-которые-легко-проглядеть"></a>
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
  `Nothing` service check. On Easy and Normal, the corresponding chances are
  only 0.305% and 0.610%.
- **`farmused` counts non-building units and serves as occupied population;
  it is not housing capacity.**
  In an ordinary non-battle match, a value from 1 through 99 makes the
  player-existence check additionally require a live eligible Peasant or a
  completed Town Hall. At
  `farmused = 0`, the player loses even if buildings remain. A single Peasant
  and a Mill are enough to continue playing. See
  [Victory and defeat](../../docs_en/recon/systems/victory_conditions.md).
- **The sight-radius formula is `20 + 4 × vision` cells.** Even `vision = 0`
  therefore gives a radius of 20 cells rather than no vision.
- **Housing capacity is
  `cen × 100 + bar × 150 + ba2 × 250 + hou × 25`,** but the map also imposes a
  global limit between 500 and 8,000 according to the selected match setting.
  Once that cap is reached, additional Houses no longer increase usable
  capacity.
- **The generator forces `foreststype = 0` on Land maps.** Even when another
  forest type is selected in the match room, `dogenerate.inc:6` replaces it
  with zero. Other terrain types still require separate verification.
- **Score does not decide victory or rating.** It is used for statistics.
  Standard matches end when only one player or allied team remains. Cossacks 3
  has no Wonder victory condition.

---

<a id="исследовательские-планы"></a>
## Research Backlogs

Detailed hypotheses and reproducible experiments live on separate pages:

- [combat mechanics](research_backlog_combat.md), including pathfinding;
- [game systems](research_backlog_systems.md), including the economy, object
  capture, artificial intelligence, determinism, and map generation.

This page remains the single source for current parser limitations, data
discrepancies, and verified caveats. The research backlogs are the single
source for questions that do not yet have a verified answer.

---

<a id="где-жалуются-на-ошибки"></a>
<a id="как-сообщить-об-ошибке"></a>
## Reporting an error

If the encyclopedia disagrees with what you observe in the game, open an issue
or pull request and include:

- what you observed;
- the game version used for the test;
- the game-script revision represented by the repository, shown in the output
  of `parser/build_data.py`.

Record an unverified observation as a reproducible experiment in the relevant
research backlog before treating it as a limitation.
