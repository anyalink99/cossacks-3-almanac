<a id="known-issues-и-оговорки"></a>
# Known issues and disclaimers

What to keep in mind when using this guide. Here
converge:

- **Parser spaces** - places where `../data.json` does not reflect game
  files exactly.
- **Differences with external sources** - where our numbers differ from
  popular guides and calculators (the source of truth is game scripts).
- **Open empirical questions** - guesses and formulas marked “not verified”
  in recon documents; waiting for measurements in the game.
- **Edge cases** are known features that are easy to overlook.

The file is alive: when the game is patched or empirical verification is updated manually.
Closed issues move to [`known_issues_archive.md`](known_issues_archive.md) -
if anything below looks "weird for the current version" it may already be
corrected and archived.

---

<a id="парсерные-пробелы-datajson"></a>
## Parser spaces (`../data.json`)

<a id="weapons-у-зданий-пока-не-извлекаются-полностью"></a>
### Weapons from buildings have not yet been completely removed

**What:** for buildings in `../data.json` there are scalar `weapon_damage`,
`weapon_pause_frames`, `weapon_radiusmax`, `weapon_kind`, `weapon_cost`. If
the building has two weapons (theoretically possible for future mods), will be removed
only the first one.

**In the real game:** all combat buildings (Towers, Shipyard) have one weapon - so
that right now this gap is not showing up. Comment left as
reminder for parser.

<a id="сценарные-триггеры-не-парсятся"></a>
### Script triggers are not parsed

**What:** `data/scripts/lib/scenario.script` (triggers, campaigns, historical
battles) - not included in the pipeline. All the facts about Wonder, `endgame_win`,
scenario-actions were extracted manually.

**Where to look with your hands:** [`docs/recon/systems/victory_conditions.md`](recon/systems/victory_conditions.md) §3.

---

<a id="расхождения-с-внешними-источниками"></a>
## Discrepancies with external sources

Several numbers in this reference differ from those found in
other people's guides and calculators. The source of truth is game scripts; if anything
does not match external material - we trust the files in this repo.

| Fact | Where seen outside | In the game file | Source | Verdict |
|---|---|---|---|---|
| `hits_needed` for food | 30 | **22** | `dmscript.global:799 gc_resource_hitsneeded_food` | We trust the file: the peasant makes 22 blows with a hoe before returning to the warehouse, not 30. This shortens the trip and raises the actual rate. |
| Cost `aca.4` (Field melioration) | W1400/G522 | **W1000 / G475** (any nation) | `country.script:3490 _country_AddUpgrade('aca.4', ..., wood=1000, gold=475)` | All 21 nations have the same price. Perhaps in external guides there are numbers from the old version. |
| Cost `Manufacture agricultural equipment` (blacksmith) | W400/G100 | **not found in blacksmith** | `country.script` | In the current forge - only per-unit damage / protection. Perhaps there was such an upgrade in Cossacks 1, and in C3 it moved to the academy (`aca.X`). |

Additionally: in the new chapter [02_combat → “Confirmed simplifications of combat
formulas"](reference/02_combat/README.md) describes five mechanics from other RTS, which
in C3 **no** (charge bonus, anti-cavalry multiplier, drummer aura, special
grenade trajectory, stealth). These are also forms of divergence - players often expect
these effects are similar to AoE/Total War.

---

<a id="edge-cases--что-легко-проглядеть"></a>
## Edge cases - what is easy to overlook

- **Builder slots for 4 warehouses.** One nation (`eursto`) is calculated via
  special `bbox_union` for linear “supports” instead of a regular walker;
  result `eursto = 8` (perimeter would give 9, off by 1 - accepted).
  Details - `compute/compute_builder_slots.py`. Gates are not being built at all
  peasants.
- **`buildtime` for buildings** is stored with an additional multiplier
  `gc_buildtime_modifier = 10`. Real time in game secondsakh =
`frames × 10 / 32`, and not just `frames / 32` like units. This is reflected in
  `data.json: buildings[*].buildtime_sec` - but if you read raw `frames`, don’t
  forget it.
- **Mercenary mass-defection on hard+.** Threshold `_misc_RandomInt < 6000` gives
  18.31% chance of transition on each Nothing-tick (~0.625 game seconds). Army
  50 mercenaries are lost almost completely in 5–10 game seconds with
  `brebellion = True`. On easy / normal - 0.305% / 0.610%, almost a riot
  decorative
- **`farmused` for defeat does not fall to 0** while there is a peasant **or**
  Town Hall. You can live with one peasant and one mill and not
  lose. Details -
  [`docs/recon/systems/victory_conditions.md`](recon/systems/victory_conditions.md) §4.
- **Vision formula 20 + 4 × vision (tiles)** gives a minimum of 20 t even with
  `vision = 0`. Default The unit does not have “0 review”, but 20 tiles.
- **Pop cap = `cen × 100 + bar × 150 + ba2 × 250 + hou × 25`** - but always
  limited by a global map cap of 500..8000 depending on the map size.
  Without a map-limit, it’s easy to not understand why houses no longer provide population.
- **Foreststype = 0 on Land always.** Even if “Random” is selected in the lobby
  forests", engine forces 0 for Land maps (`dogenerate.inc:6`). On non-Land
  other meanings apply.
- **Score does not determine victory.** Accumulates only for statistics and ELO. Victory
  - last-team-standing only. Wonder of the World is not in C3.

---

## Open empirical questions

These are questions for which the answer from the code is incomplete or cannot be extracted without
in-game measurements. Listed by recon documents - each section indicates where
you can actually dig.

<a id="добыча-и-экономика--reconworldeconomypeasantextractionmdreconworldeconomypeasantextractionmd-9"></a>
### Mining and economics - [`recon/world/economy/peasant_extraction.md`](recon/world/economy/peasant_extraction.md) §9

- Exact `loss_factor` (proportion of time lost on walking to the warehouse) at different
  map layouts.
- Real rate taking into account the RNG choice of target by the peasant (between launches
  one save σ/μ ≈ 5–15% on a 5-minute window for forest and stone; for mines
  ≈ 0).
- Empirical `K` (trees-per-pattern coefficient) - now 0.30
  calibrated to small = 10 / big = 50, but exact coefficient requires
  5–10 runs of map gen + env parsing.

<a id="ии--reconsystemsaibehaviormdreconsystemsaibehaviormd-открытые-вопросы"></a>
### AI - [`recon/systems/ai_behavior.md`](recon/systems/ai_behavior.md) §“Open questions”

- Replenishment rate of the agressor pool (`aiData.agressors.Add` - where?).
- Activation of the `bhumanai` flag - the setter was not found in the scripts. Perhaps
  set from the engine or UI side.
- `gc_ai_max_guards = 120` - buffer above the pike threshold, but semantics
  incomprehensible.
- Logic `centerfound` - when switches to `True`.
- Impact of difficulty on attack frequency: agressor/sabotage triggers use
  identical constants; The only difference is the speed of construction. Worth it
  verify in game.

<a id="захват--reconworldeconomycapturemechanicsmdreconworldeconomycapturemechanicsmd-9"></a>
### Capture — [`recon/world/economy/capture_mechanics.md`](recon/world/economy/capture_mechanics.md) §9

- Exact position of `(px, py)` at the building when checking: model center, bbox center
  or anchor-point? Empirically measured: build a barracks, bring
  peasant to the edge, measure the min-distance.
- `bAutoKill` is declared in code, but is never assigned in
  `_misc_CheckCapture`. Possibly legacy from C1.
- Walls: `_unit_SearchCapturersForWall` does NOT require `bcancapture` - this means
  peasants and art can “break” the wall through the capture mechanism. Check
  empirically.

### Pathfinding — [`recon/world/combat/pathfinding.md`](recon/world/combat/pathfinding.md) §9

- The pathfinding algorithm itself lives in the native engine (C++): A*? Flow
  field? Wave propagation? Not visible to scripts.
- Squad-tag effect (transmitted as float-tag from the script): does the engine change
  path result for units of the same squad?
- Behavior when a new obstacle appears on the route: no challenge found
  repath. Does the unit stop silently?

<a id="rng--детерминизм--internalsenginedeterminismauditmdinternalsenginedeterminismauditmd"></a>
### RNG / determinism - [`../internals/engine/determinism_audit.md`](../internals_en/engine/determinism_audit.md)

- Global state PRNG (`random`-cursor) - is it saved in save? Rather
  everything, no.
- Pathfinding tie-breaking (engine, not available to the script).
- Variable timestep (engine).

### Map generation — [`recon/world/map/map_generation_pipeline.md`](recon/world/map/map_generation_pipeline.md) §13

- Bounded enumeration of unique cards: 230 basic forms × K randkey variations.
  K unknown (probably ≤ 10⁹, but actual range of user seeds
  less).
- Exact position of `arrStartPos` in `inputbitmap.tga` - engine reads markers
  according to special RGB pixel codes. Decode manually.
- `season = 3` → desert pattern types - not implemented in
  `compute_map_resources` (1 / 20 sample replays).

---

<a id="где-жалуются-на-ошибки"></a>
## Where they complain about errors

If something does not coincide with your observations in the game, open an issue or
pull request with description:

- what was observed,
- what version of the game did you use,
- which branch of scripts is currently in the repo (see date in `parser/build_data.py` output).

This file is deliberately incomplete: empirical measurements are needed, which are more convenient
everything to do while sitting at the game.
