<a id="recon-pipeline-генерации-карты"></a>
<a id="как-создаётся-случайная-карта"></a>
<a id="технический-разбор-генерации-случайной-карты"></a>
# Technical Evidence for Random-Map Generation

[← Scripts and Scenarios](structure.md)

[Reader guide to random-map generation](../../docs_en/recon/world/map/map_generation_pipeline.md)

The game assembles a random map in five stages: preparation, terrain,
starting positions and nearby resources, remaining resources, and
finalization. Identical lobby options do not necessarily mean identical
terrain: the result also depends on the base mask and two generation keys.
Internal functions and Pascal excerpts are collected near the end under
[Technical details](#technical-details) and [Sources](#sources).

**Related documents:**

- [Resource gathering, §8](../../docs_en/recon/world/economy/peasant_extraction.md) — densities
  (`frs_big`, `mnt`, ...) and distances from the center for mines.
- [Resource gathering, §8.4](../../docs_en/recon/world/economy/peasant_extraction.md) — what a
  `.pattern` file is and how mask cells become environment objects.

<a id="коротко"></a>
## At a Glance

- The map is built in **five stages**: preparation → terrain → starting
  positions and nearby resources → remaining resources → finalization.
- The base mask and two generation keys **fully determine the map**, which
  is why a replay reproduces the same terrain and object placement.
- Three elliptical zones of different sizes are reserved around each
  starting position. The inner zone remains clear for the starting army;
  the next zones reserve room for nearby stone and forests.
- On Land maps, the generator uses mixed conifer forests; the Desert season
  replaces them with separate desert environment sets [^2].
- With the Default starting-army setting, the final stage creates
  **18 Peasants** in a 6 × 3 grid. A special preset replaces them with a
  national force.

<a id="1-глобальные-константы-объявлены-до-процедур"></a>
<a id="от-чего-зависит-результат"></a>
## What Determines the Result

| Choice | What changes |
|---|---|
| Terrain type | The base shape of land, water, and available starting points. |
| Relief | The share of plains, hills, mountains, and buildable ground. |
| Deposit richness | The number of mineral-placement passes near players and farther from the base. |
| Season | Textures and environment sets; Desert uses separate variants. |
| Map size | Available area and the density adjustment for placed objects. |
| Teams | Whether allies are placed together or positions are distributed normally. |
| Base mask and keys | The exact reproducible map variant. |

---

<a id="2-pipeline-хронологический-порядок-файлы-от-вершины-dogenerate-вниз"></a>
<a id="2-порядок-генерации-карты"></a>
<a id="порядок-генерации-карты"></a>
## Map-Generation Sequence

| Stage | Result |
|---|---|
| Preparation | Service masks are cleared and environment templates are loaded. |
| Relief | The surface, elevations, coasts, and water are created. |
| Starting positions | Players receive positions; the first resources and deposits are placed nearby. |
| Rest of the map | Distant deposits, forests, stone, swamps, lakes, and decoration are added. |
| Finalization | Starting units appear, territory ownership is calculated, and peace-time borders are added when needed. |

The individual stages are detailed below.

<a id="phase-0--подготовка"></a>
<a id="этап-0--подготовка"></a>
### Stage 0 — Preparation

1. Helper procedures for masks (`FillPatternMaskElipse/Circle/Rectangle/MapBorder`) [^4].
2. Helper procedures for units and `UniqueStartingUnits`: nation-specific
   officers and drummers for a non-default starting army (`startingunits > default`) [^5].
3. `ClearMapMaskAndObjects` clears `gPatternMask` (640×640),
   `arrStartPos[0..7]`, and `arrStartPosBusy[i] := -1` [^6].
4. `_gui_ProcessProgressBar('progressbar.loadingenvironment')` calls
   `LoadPatterns(True, False)` and `LoadPatterns(True, True)`, loading all
   `.pattern` files from `data/gen/patterns/*` [^7].

<a id="этап-1--рельеф-и-базовая-поверхность"></a>
### Stage 1 — Terrain and Base Surface

5. Existing non-spectator players are counted in `plcount` [^8].
6. `SetupTiledPatterns('tiles')` — or `desert_tiles` in the desert — places
   background details such as dirt and cracks on a 25 × 25-cell grid. A
   256 × 256 map receives about **100 placements** [^9].
7. `SetRandomKey(randkey1)` sets the generator key, making all subsequent
   `RandomExt` calls reproducible [^10].
8. Relief (`relieftype`), terrain type (`terraintype`), and mine richness
   (`minesdensity`) are validated; invalid values are randomized. The built-in
   `ExecuteState('GenerateMap')` then creates a heightmap from the selected
   `inputbitmap.tga` and fills the map cells [^11].
9. Shore and water cells with `height < -0.1` are blocked in
   `gPatternMask` [^12].
10. The Random mine setting (`minesdensity > 2`) is replaced with
    `floor(RandomExt*3)` [^13].
11. `_misc_SetDesert(False, False)` if `bDesert` [^14].

<a id="phase-1--terrain"></a>
<a id="этап-2--стартовые-позиции-и-ближайшие-ресурсы"></a>
### Stage 2 — Starting Positions and Nearby Resources

12. The C++ engine extracts starting positions from special markers in
    `inputbitmap.tga`. The script copies valid `gMap.players[i].startx/y`
    coordinates to `arrStartPos`; their number is stored in `spcount` [^15].
13. `_misc_FillPatternMaskMapBorder(3)` blocks the outer frame, three cells wide [^16].
14. **`RandomStartingPoints(spcount, minesdensity)`** [^17] assigns positions
    according to the team setting (see §3). For each player,
    `CreateStartPoint(...)`:
    - closes the inner zone with `_misc_FillPatternMaskElipse(...)`;
    - places the first round of nearby deposits with `SetupMines(...)`;
    - `SetupStartingResources(pointx, pointy)` — places ~5–6 clusters around (see §4).
15. A second `SetRandomKey(randkey1)` resets the generator so that details of
    the previous placement do not affect later stages [^18].

<a id="phase-2--старт-поинты"></a>
<a id="этап-3--рельеф-и-остальные-ресурсы"></a>
### Stage 3 — Relief and Remaining Resources

16. The `relieftype` branch selects `plt`, `mnt`, and `hil`. For Highlands
    (`relieftype = 3`), the values are `plt=0.000055`, `mnt=0.000120`, and
    `hil=0.000050` [^19].
17. Base densities are set to `frs_big=0.0009`, `frs_mid=0.0009`,
    `frs_small=0.00054`, `dcr=0.0005`, `stn1=0.00016`, and
    `stn2=0.00012` [^20].
18. `_misc_GetFreePatternMaskModifier(...)` estimates the proportion of free
    cells through random sampling (a Monte Carlo estimate). The result is
    multiplied by the map-size adjustment
    `640/((mapW+mapH)/2)`; for Tiny maps this is ×2.5 [^21].
19. `problarge` adjusts the final densities for
    `pln_small/_mid/_large/_huge`, `swamp_*`, `lake_*`, and
    `mnt/plt/hil` [^22].
20. `_misc_SetupPatternsByType(...)` places mountains, three-part plateaus,
    ravines, and hills [^23].
21. **Remaining deposits:** `SetupMines(...)` runs rounds `1..rounds-1`,
    creating the outer rings. Here `maxround = 0` means that no additional
    limit is imposed [^24].
22. The generator key is reset again with `SetRandomKey(randkey1)` [^25].
23. `_misc_SetupPatternsByType` places forests, stone, plains, swamps, and
    lakes. On Land maps, `foreststype` is forced to 0, so only the `pine`,
    `spruce`, `pinefir`, and mixed `pine_big_2` sets are used [^26].

<a id="phase-4--старт-юниты--финализация"></a>
<a id="phase-3--relief-densities--phase-2-mines"></a>
<a id="этап-4--стартовые-юниты-и-завершение"></a>
### Stage 4 — Starting Units and Finalization

24. **`for i:=0 to gc_MaxPlayerCount-1 do CreateStartPointPeasants(i, startx, starty)`** (or `CreateUniqueStartingUnits` if `startingunits>default`) [^27].
25. `_misc_PreloadTextures(True, True, True)` [^28].
26. `gbool_gui_mapgenerationfinished := True` [^29].
27. Environment objects are normalized for the season: `leaftree*` is
    removed in winter, and scale is clamped to `[scaleMin, scaleMax]` [^30].
28. Processing ticks are distributed among computer-controlled players
    (`gPlayer[i].progressTick := ...`) [^31].
29. `_player_SetupTeams(true)` [^32].
30. `gfloat_peacetime := _misc_GetPeaceTime(...)`; `gbool_peacemode := (peacetime <> default)` [^33].
31. **`FillOwnerMap(spcount)`** (see §5) [^34].
32. `if gbool_peacemode then SetupBorderObjects` (see §6) [^35].
33. `_misc_SetShoresCollision` [^36].
34. The season selects a color table: winter=6, desert=7, default=0; the
    internal `PHDR` flag is set to `1` only in winter [^37].
35. `TimeLog('Generation finished. relieftype=... minesdensity=...')` [^38].

---

<a id="3-randomstartingpointsplcount-minesdensity--раздача-игроков"></a>
<a id="3-как-игрокам-назначаются-стартовые-позиции"></a>
## 3. How Starting Positions Are Assigned

`RandomStartingPoints(plcount, minesdensity)` has two branches, selected by
the team setting (`gMap.settings.additional.teams`) [^17].

<a id="31-teams--nearby-союзники-рядом"></a>
<a id="31-союзники-рядом-teams--nearby"></a>
### 3.1. Allies Nearby (`teams = nearby`)

1. Players are grouped by `team`: `0` means solo players and `1..4` are teams.
2. A team with only one member is moved into the solo group (`team[0]`).
3. For every multi-player team:
   - the generator is reset with `SetRandomKey(randkey1)` and advanced by the
     required number of steps;
   - the next team is selected randomly from `teamlist`;
   - `GenerateTeamStartingPoints(...)` chooses neighboring positions with a
     greedy algorithm [^39]. The first position is random; every later
     position should be close to most of the existing ones, with total
     distance used as the tie-breaker;
   - the selected positions (`points`) are randomly assigned to team members.

<a id="32-teams--default-по-разным-углам"></a>
<a id="32-обычная-расстановка-teams--default"></a>
### 3.2. Standard Placement (`teams = default`)

- All players belong to `team[0]`. For each one, the generator is reset with
  `SetRandomKey(randkey1)`, advanced by `i + 8` steps, and used to choose a
  random remaining position (`pointindex`).

In both cases, `CreateStartPoint(...)` is called for every player. It places
the first round of deposits and the nearby starting resources.

**Where `arrStartPos[].x/y` comes from.** The C++ engine reads
`inputbitmap.tga` and finds special-color pixels that mark starting positions.
The script receives their coordinates through `gMap.players[i].startx/starty`
and can only reassign players among those positions.

---

<a id="4-setupstartingresourcespointx-pointy--что-спавнится-возле-города"></a>
<a id="4-какие-ресурсы-появляются-возле-стартового-города"></a>
## 4. Resources Near the Starting Town Hall

`SetupStartingResources(pointx, pointy)` performs six placement stages. Each
tests up to 128 × 3 = 384 positions by varying angle and distance. It is
called from `CreateStartPoint` **after** the inner `cCircle1` zone is filled
[^40].

| # | Object | Minimum distance, cells | Distance formula | Zone blocked afterward |
|--:|---|---:|---|---|
| 1 | Mixed stone-and-forest area (`stoneforests`; `desert_stoneforests` or `desert_forests_big` in desert) | `min(5,7) = 5` | `5 + RandomExt*3 + (i+j)*0.5` | — |
| 2 | `_FillPatternMaskElipse(cCircle2=12,15)` | — | — | Middle zone |
| 3 | Stones (`stones`) | `min(12,15) = 12` | `12 + RandomExt*3 + (i+j)*0.5` | — |
| 4 | Medium or large forest (`forests_pinefir/spruce/pine_*_medium/big`), twice | 12 | Same | — |
| 5 | Stones (`stones`) | `min(12,15) + 4 = 16` | `16 + RandomExt*2 + (i+j)*0.5` | — |
| 6 | One more medium or large forest (`forests_*_medium/big`) | 16 | Same | — |
| 7 | `_FillPatternMaskElipse(cCircle3=22,18)` | — | — | Outer zone |

**What this means for the starting base:** within **5–22 cells** of the
Town Hall, the generator guarantees:

- one `stoneforests` pattern containing both Wood and Stone, with a mask of
  roughly 152 cells;
- two `stones` patterns, roughly 138 mask cells each;
- three `forests_*_big/medium` patterns, from 148 to 1,631 mask cells
  depending on the type.

Afterward, the area within 22 cells is fully masked and the third stage cannot
place anything else there. **This is why the starting area reliably contains
enough wood for a Town Hall (`ratuse`) and the first Mill (`mill`).**

Desert maps substitute `desert_stoneforests`, `desert_forests_big`,
`desert_stones`, and `desert_forests_medium/big`.

---

<a id="5-fillownermapspcount--кому-какая-клетка-принадлежит"></a>
<a id="5-как-карта-делится-между-игроками"></a>
## 5. How the Map Is Divided Among Players

`FillOwnerMap(spCount)` uses breadth-first search (`BFS`) [^41]:

1. Initialize `gScanGrid[i,j]` (size
   `gc_scangrid_countx × gc_scangrid_county`) with `owner=-1`, `dist=-1`,
   and `fChecked=False`.
2. For each starting position: `_misc_PosToScanGridIndices(arrStartPos[i].x, .y, gridX, gridY)` → `gScanGrid[gridX,gridY].owner := arrStartPosBusy[i]` (player ID), `dist := 0`.
3. BFS: while there are unprocessed cells on the current `dist` → distribute to 4 neighbors (i±1, j±1) the same owner with `dist+1`.

The result assigns every scan-grid cell to the nearest player by Manhattan
distance.

---

<a id="6-границы-во-время-мира"></a>
## 6. Peace-Time Borders

`SetupBorderObjects` runs **only while peace time is enabled**
(`gbool_peacemode`, or `peacetime ≠ 0`) [^42]. See
[Game Settings](../../docs_en/recon/world/map/game_settings.md#peacetime--как-устроен-мир) for the full mechanic.

For each horizontal or vertical pair of neighboring cells:

- if `owner` differs, draw a chain of border objects between the cell
  centers;
- Step: `cBorderObjDist = 1` cell.
- On water: `gc_basename_ptborderwater`, on land: `gc_basename_ptborder`.
- The engine's miscellaneous-object player slot (`gc_playerind_misc`) owns
  the objects; `GameObjectMakeUniqId` assigns unique identifiers.

Our calculation model ignores peace-time borders. With peace time disabled,
they do not exist and cannot affect resource calculations.

---

<a id="7-createstartpointpeasantsplind-pointx-pointy--стартовые-крестьяне"></a>
<a id="7-как-размещаются-стартовые-крестьяне"></a>
## 7. How Starting Peasants Are Placed

Algorithm [^43]:

- `count = 18`: one call to this procedure always creates 18 Peasants.
- `cUnitR = 0.75` — grid step.
- For `i` from 0 to 17:
  - `px = pointx + (i div 3) * 0.75 + (0.5 - RandomExt) * 0.25 - (6 * 0.75)/2`
  - `pz = pointy + (i mod 3) * 0.75 + (0.5 - RandomExt) * 0.25 - (0 * 0.75)/2`
  - creates a Peasant at `(px, py, pz)`, facing downward (`SetGameObjectRollAngleByHandle = 180`).

**Grid:** 6 columns × 3 rows, 0.75 cells apart, with random jitter of ±0.125.
Because `count mod 3 = 18 mod 3 = 0`, the Z-centering offset is zero. The
Z coordinates run from `pointy + 0` to `pointy + 1.5`, so the grid is shifted
downward rather than centered. X is centered correctly, from
`pointx - 2.25` to `pointx + 1.5`.

This matches the observed **18 idle Peasants**: 18 × (32 + 30) Food per game second × 32/20000 × 120 game seconds ≈ 214 Food. See also the [economy guide](../../docs_en/reference/01_economy/README.md).
If `gMap.settings.additional.startingunits > 0` (not “Default”), `CreateUniqueStartingUnits` replaces the 18 Peasants with a nation-specific force: an Officer, a Drummer, and several infantrymen. All 14 presets appear in the [lobby-settings reference](../../docs_en/reports/map/lobby_settings.md#startingunits--стартовая-армия); their behavior is described under [Game Settings](../../docs_en/recon/world/map/game_settings.md).

---

<a id="8-что-значит-phase-1-vs-phase-2-mines"></a>
<a id="8-как-размещаются-месторождения"></a>
## 8. How Mineral Deposits Are Placed

`SetupMines(pointx, pointy, minround, maxround, minesdensity, spcount)` is
called twice:

| Stage | `minround` | `maxround` | Rounds performed | Source |
|---|---:|---:|---|---|
| First call inside `CreateStartPoint` | 0 | 1 | `i := 0..0`, round 0 only | [^44] |
| Second call after terrain generation | 1 | 0 | `i := 1..rounds-1`, skipping round 0 | [^24] |

`if (maxround>0) and (rounds>maxround) then rounds := maxround` limits the
first call to one round. In the second call, `maxround=0` imposes no
override, so `minesdensity` determines the full number of rounds.

For **Rich (`minesdensity=2`) on Tiny (`mapsize>2`)** [version ≥80]:

- Phase 1: one round × three resources = three nearby deposits (gold, iron,
  and coal) at a distance of 14–22 cells.
- Phase 2 runs rounds 1–4, but round 4 is skipped on Tiny maps, leaving
  three outer rounds × three resources = nine outer deposits.
- **Twelve deposits per player is an upper bound on attempts.** Each deposit
  receives up to 256 candidate positions. If none avoids `cCircle`, other
  mines, and a neighbor's starting position, the deposit is omitted. In
  practice a Tiny Rich map produces 9–12 deposits, depending on its generation
  key.

In generator version 90 or later, round 2 on a Tiny map with
`spcount ≤ 4` snaps the farthest deposits toward map corners through
`newpointx/y = ±maphW ∓ 24, ±maphH ∓ 24` [^45]. These become neutral,
contested deposits near the edge.

---

<a id="9-версионные-различия-grecordgeneratorversion"></a>
## 9. Version Differences (`gRecordGeneratorVersion`)

The code contains many `if (gRecordGeneratorVersion < N) then …` branches.
The DLC5-era game client uses a generator version of at least 90, which
includes:

- DLC5 terrain types [^46].
- Distance table v90+ (mines round 2 = 70..82 on tiny, snap to corner).
- `gRecordGeneratorVersion < 53` → player handle 8 is deleted.
- `< 89` → 9, 10, 11 are deleted.

A mod developer can check `gRecordGeneratorVersion` via `data/game/var/data.cfg` or via git log of this file.

---

<a id="10-что-наша-симуляция-в-parser-и-compute-модулирует--упрощает"></a>
<a id="10-что-упрощает-наша-расчётная-модель"></a>
## 10. Simplifications in the Calculation Model

The following table records which parts of `dogenerate.inc` the calculation
model reproduces, approximates, or omits:

| Reality | Our simulation | Status |
|---|---|---|
| Engine reads starting positions (`arrStartPos`) from `inputbitmap.tga` | We set one position explicitly | Sufficient for one-player scenarios |
| Six `SetupStartingResources` stages with specific patterns | We use aggregate forest and stone density | **Rough:** starting resources are undercounted, but totals have been checked against replays |
| Blocked `cCircle1/2/3` zones | Not modeled explicitly | Their effect is partly absorbed by the measured placement rates (§14) |
| Nearby deposits, round 0 at 14–22 cells | Modeled through `predicted_mines_per_type` | Validated: actual-to-predicted ratio is 1.00 |
| Second-round corner snapping on Tiny maps | Not modeled; distance remains 70–82 | Minor difference |
| On Land maps, forest type is forced to `0` | Land mixture assumed | Matches |
| Territory ownership and peace-time borders | Ignored | Harmless with the standard no-peace-time setting |
| Default starting army: 18 Peasants in a 6 × 3 grid | Fixed at 18 for Default | Matches |
| Placement probability by pattern type | Measured per-type values replace the former universal 0.65 | Validated on ten homogeneous Tiny + Land + Highlands replays; ratios 0.96–1.04 |
| Desert patterns for `season = 3` | Not implemented | Needed for desert maps; 1 of 20 sample replays |
| Plains, mountains, swamps, hills, plateaus, and stone forests | Not predicted by `compute_counts` | **Open gap:** about 50% of clusters are outside the model |
| Deposit formula outside Land | Calculated as Land | **Open gap:** such replays yield an invalid player count |
| Allies-nearby placement | Not implemented | Sufficient for one-player scenarios |

---

<a id="14-проверка-расчётной-модели-по-реплеям"></a>
## 14. Validating the Calculation Model Against Replays

Since 29 April 2026, the model can be checked against real save and replay
files. This turns §10 from a list of hypotheses into measured results.

<a id="141-стек"></a>
### 14.1. Tools

| Script | Purpose |
|---|---|
| [`parser/parse_replay.py`](../../parser/parse_replay.py) | Reads OSWMap13 settings, the BMP preview, and occurrences of `.pattern` names |
| [`parser/parse_replay_aggregates.py`](../../parser/parse_replay_aggregates.py) | Aggregates a folder of `.rep`/`.map` files into `derived/replay_ground_truth.json` with per-replay and per-type cluster counts |
| [`compute/validate_map_predictions.py`](../../compute/validate_map_predictions.py) | Runs `compute_counts(...)` for every replay, compares prediction with reality, and writes the grouped [calibration table](../data/map_predictions_validation.md) |

Sections 14.2–14.5 describe the OSWMap13 format, grouping method, and
calibration results.

<a id="142-формат-oswmap13-карты"></a>
### 14.2. OSWMap13 Map Format

`.rep` and `.map` files contain a binary snapshot:

- The header contains length-prefixed strings such as
  `"OSWMap13.Map.Ver[0.0]..."`, `"UID..."`, `"GameMapSnapShotBegin"`, a BMP
  image, `"GameMapSnapShotEnd"`, and `"GameMapRecordBegin"`.
- The body contains pairs of unsigned 32-bit lengths and ASCII strings:
  `(u32 keylen, ASCII key, u32 vallen, ASCII value)`. Numbers are serialized
  as ASCII strings.
- Placed `.pattern` filenames appear as printable strings, for example `mng_3`
  and `forests_pine_big_1`. **Each occurrence represents one cluster actually
  placed by the engine** and therefore provides the observed, ground-truth
  count.

The headers do not include `playerscount` or `startid`; these values must be
derived from the deposit formula in §14.4.

<a id="143-почему-выборку-нужно-делить-на-группы"></a>
### 14.3. Why the Sample Must Be Split into Groups

⚠ A combined actual-to-predicted ratio can accidentally approach 1.0. Tiny
maps have a higher placement rate and were underpredicted; Huge maps have a
lower rate and were overpredicted. The errors cancel out. Validation must
therefore group data by `(mapsize, relieftype, terraintype, mask_kind)` and
report the combined result separately.

<a id="144-как-вывести-число-игроков-на-карте-суша"></a>
### 14.4. Inferring the Player Count on Land

For Land terrain, total mines per type encode the player count `P`:
```
mines_per_type = P × (1 + n_after) + (spcount - P) × n_after
              = P + spcount × n_after

⇒ P = mng_count - spcount × n_after
```
Here `n_after` is the number of rounds after round 0, excluding round 4 on
Tiny maps. With Tiny, Rich or Medium deposits, and four starting positions,
values 14, 15, and 16 mean two, three, and four players respectively. A
two-player replay with `mng_count = 14` validates the formula.

For **non-Land** terrain (`terraintype != 0`), the formula does not work.
The engine follows a different branch; `CreateStartPoint` may skip round 0.
See question 6 in §13.

<a id="145-измеренные-вероятности-размещения"></a>
### 14.5. Measured Placement Rates

The values are stored in
[`PER_TYPE_PLACEMENT_TINY_HIGHLANDS_LAND`](../../compute/compute_map_resources.py).
The sample contains ten Tiny + Land + Highlands replays with four starting
positions and a no-water mask (`Tiny+Land+Highlands+4pl_nowater`).

| Pattern type | Placement rate | Actual / predicted |
|---|---:|---:|
| `forests_pine_big` | 0.81 | 0.98 |
| `forests_pine_big_2` | 0.74 | 1.00 |
| `forests_pinefir_big` | 0.07 | 1.10 |
| `forests_spruce_big` | 0.20 | 1.00 |
| `forests_pine_medium` | 0.76 | 1.04 |
| `forests_pinefir_medium` | 0.09 | 0.75 (rounding error by 1.5→2) |
| `forests_spruce_medium` | 0.04 | 0.70 (rounding) |
| `forests_pine_small` | 0.64 | 0.96 |
| `forests_pinefir_small` | 0.03 | 0.80 |
| `stones` | 0.58 | 1.01 |
| Gold, iron, and coal (`mng/mni/mnc`) | Formula | 1.00 |

The large variation follows from pattern footprint size:

- `pine_big` uses 148 mask cells, fits almost anywhere, and succeeds about
  80% of the time.
- `pinefir_big` uses roughly 920 cells, six times as many, and succeeds only
  about 7% of the time.
- `spruce_big` lies between them at about 20%.

These values apply only to **Tiny + Land + Highlands**. Larger maps provide
more free space, so the rates for `pinefir` and `spruce` should differ. Do
not extrapolate without additional replay data.

---

<a id="11-ключевые-файлы-pipeline"></a>
<a id="технические-подробности"></a>
## Technical Details

`DoGenerate`, launched through `ExecuteState('DoGenerate')`, runs the stage
sequence [^1]. The horizontal and vertical radii (semiaxes) of the three
starting zones are
`5 × 7`, `12 × 15`, and `22 × 18`
(`cCircle1Mask*`, `cCircle2Mask*`, and `cCircle3Mask*`) [^3].
`cBorderObjDist = 1` is the spacing of peace-time border objects.

The zones are marked in `gPatternMask`: an occupied cell can no longer
receive a forest, stone, or environment-player object.
`_misc_FillPatternMaskElipse(pointx, pointy+2, rx, ry)` offsets the ellipse
center by two cells vertically from the starting point.

In the Land-map generator, `foreststype` first receives
`floor(RandomExt*3)` and is then immediately overwritten with `0` [^2].
Branch 0 uses the `pinefir`, `spruce`, `pine`,
and `pine_big_2` sets. Desert is selected by
`bDesert := (gMap.settings.gen.season = 3)`, which switches to `desert_*`
sets. Half the map width (`maphW := mapW div 2`) is used by the second
`SetupMines` pass to anchor distant deposits to corners on Tiny maps.

<a id="11-ключевые-файлы-алгоритма"></a>
## 11. Key Algorithm Files

| Purpose | File | Lines |
|---|---|---|
| Main orchestrator | `data/scripts/common.inc/dogenerate.inc` | 1-2103 |
| Entry point | `data/scripts/common.inc/initmapgen.inc` | 232 |
| Mission map option | `data/scripts/common.inc/dogeneratemissionmap.inc` | — |
| Engine RNG seed setup | `data/scripts/lib/map.script` | 322 (`GenerateMapRandKey`) |
| InputBitmap selection | `data/scripts/common.inc/generatemap.inc` | 179-216 |
| StandPattern (C++ inside) | `data/scripts/lib/misc.script` | 3390 (declaration only) |
| GenerateMap state | engine-builtin | called line 1565 |

---

<a id="12-seed-space--что-определяет-уникальную-карту"></a>
<a id="12-seed-space"></a>
<a id="12-что-определяет-уникальную-карту"></a>
## 12. What Determines a Unique Map

With terrain type, map size, relief, mine richness, and player count fixed, a
map is uniquely specified by its base mask (`inputbitmap`) and generation keys
(`randkey0`, `randkey1`):

- `inputbitmap` is a file from
  `data/gen/terrainmasks/<terrain>/<N>pl_*.tga`, selected through the random
  index `floor(RandomExt*count)` [^47]. The engine reads the TGA image and
  derives starting positions from special markers in the mask, exposing the
  coordinates through `gMap.players[i].startx/y`.
- `randkey0, randkey1` form a 64-bit pair of random number generator (RNG)
  seeds (`SetRandomExtKey64`) [^48]. The pair determines every subsequent
  `RandomExt` call, including forest, stone, and deposit placement and the
  selection of a bitmap from the list.

For four players, the base-mask counts are:

| Terrain folder | Files |
|---|---:|
| `continent/` | 121 |
| `continents/` | 187 |
| `islands/` | 320 |
| `land/` | **230** |
| `mediterranean/` | 122 |
| `nowater/` | 42 |
| `nowater2/` | 33 |
| `peninsulas/` | 280 |

Land therefore has **230 base map shapes** for four players.

This has three practical consequences:

1. **Bounded enumeration.** For Land + Tiny + four players + Highlands +
   Rich, the number of maps is 230 base shapes multiplied by the number of
   key variants. The exact key range exposed by the interface is not yet
   known. Its four-byte field is unlikely to expose more than `10⁹` values,
   and user-entered keys probably occupy a smaller range.
2. **Deterministic replay.** Given `inputbitmap`, `randkey0`, and `randkey1`,
   the map can be reproduced bit for bit if the engine generator is
   deterministic; see
   [the determinism audit](../engine/determinism_audit.md).
   Save filenames contain `randkey1`:
   `'game_v'+gSerialVersion+'k'+randkey1+'.map'` [^49].

3. **Precise tree-count calibration.** Repeating a generation five to ten
   times with identical settings, then parsing environment objects from the
   save, can measure the relationship between mask size and tree count. This
   would replace the current `0.30 × mask_cells` approximation.

**Limitations.** `GenerateMapRandKey` is built into the engine and its body is
not available [^50]. The exact range of `randkey0` and `randkey1` remains
unconfirmed.

---

<a id="13-открытые-вопросы-для-следующих-сессий"></a>
## 13. Open Questions

1. **Exact starting positions (`arrStartPos`) in `inputbitmap.tga`.** The
   engine probably reads special RGB pixel codes. Manually decoding
   `data/gen/terrainmasks/land/4pl_*.tga` would reveal the exact positions for
   every mask and improve editor tooling and resource-distance predictions.

2. **Exact free-space adjustments for Tiny maps and Highlands.** The internal
   values have not been measured. Effective per-type placement rates have
   been calibrated from ten replays (§14.5), so practical calculations are
   already possible without reconstructing the Monte Carlo implementation.

3. **Does `SetupTiledPatterns` affect later object placement?** Roughly one
   hundred tiled patterns on a 256 × 256 map provide ground decorations such
   as cracks and mud. They may also block `gPatternMask`; this must be checked
   through `_misc_CheckStandPatternExt`.

4. **C++ functions `StandPatternWithAngle` and `_misc_FillPatternMaskBy*`.**
   Only declarations are available. Without disassembling the executable, a
   mask cell cannot be mapped exactly to an environment-object class such as
   `oak`, `leaftree`, or `decortree`.

5. **The live `gRecordGeneratorVersion` value.** This determines which branch
   of the deposit-distance table is used. It is probably at least 90 because
   second-round corner snapping matches sample replays, but this has not been
   confirmed. The extracted replay header `Build.Ver[X.Y.Z.NNNN]` may provide
   the answer.

6. **Deposit formula outside Land.** For Continents, Mediterranean, Coastal,
   Peninsulas, and Lakes (`terraintype != 0`), the number of gold deposits
   (`mng`) implies an impossible player count of zero or less (§14.4).
   `CreateStartPoint` may skip round 0, or the number of later rounds may
   differ. The relevant `dogenerate.inc` branches or `ExecuteState` code must
   be examined.

7. **Add plains, mountains, swamps, hills, plateaus, stone forests, and desert
   areas to `compute_counts`.** Their technical types (`plain`, `mountains`,
   `swamps`, `hills`, `plateaus`, `stoneforests`, `desert_*`) are placed
   outside the `foreststype` block and account for about half of the clusters
   found in replays.

8. **Dozens of `randkey0` and `randkey1` values for Land + Tiny + Highlands.**
   At least fifty replays with identical settings and only the key changed are
   needed to confirm that a key always produces the same cluster count, or to
   measure the variance. The ten current replays are not enough.

---

<a id="источники"></a>
## Sources

All links are relative to `data/scripts/` in the Cossacks 3 installation.

[^1]: `DoGenerate` entry point is `common.inc/initmapgen.inc:232`, main script is `common.inc/dogenerate.inc:1-2103` (2103 lines).
[^2]: `foreststype` initialization and forced override — `common.inc/dogenerate.inc:5-6`:
    ```pascal
    var foreststype : Integer = floor(RandomExt*3);
    foreststype := 0;
    ```
[^3]: Global constants `cCircle*`, `cBorderObjDist` - `common.inc/dogenerate.inc:407-416`.

[^4]: Helper-procedures for masks (`FillPatternMaskElipse/Circle/Rectangle/MapBorder`) - `common.inc/dogenerate.inc:1-78`.

[^5]: Helper-procedures for units and `UniqueStartingUnits` - `common.inc/dogenerate.inc:80-419`.

[^6]: `ClearMapMaskAndObjects` - `common.inc/dogenerate.inc:444-497`.

[^7]: `LoadPatterns` after the progress bar - `common.inc/dogenerate.inc:1284-1289`.

[^8]: Counting `plcount` non-spectator - `common.inc/dogenerate.inc:1291-1296`.

[^9]: `SetupTiledPatterns('tiles')` - `common.inc/dogenerate.inc:1535`.

[^10]: `SetRandomKey(randkey1)` (first seed) - `common.inc/dogenerate.inc:1538`.

[^11]: Resolve `relieftype/terraintype/minesdensity` + `ExecuteState('GenerateMap')` - `common.inc/dogenerate.inc:1542-1565`.

[^12]: Water shore mask (`height < -0.1`) — `common.inc/dogenerate.inc:1568-1581`.

[^13]: Random `minesdensity` if > 2 - `common.inc/dogenerate.inc:1585-1587`.

[^14]: `_misc_SetDesert(False, False)` - `common.inc/dogenerate.inc:1590`.

[^15]: Filling `arrStartPos` from `gMap.players[i].startx/y` - `common.inc/dogenerate.inc:1596-1611`.

[^16]: `_misc_FillPatternMaskMapBorder(3)` - `common.inc/dogenerate.inc:1613`.

[^17]: `RandomStartingPoints` - `common.inc/dogenerate.inc:1090-1229` (call to `1615`).

[^18]: Re-seed after `RandomStartingPoints` - `common.inc/dogenerate.inc:1616`.

[^19]: `relieftype` densities (`plt/mnt/hil`) - `common.inc/dogenerate.inc:1621-1650`.

[^20]: Basic density constants (`frs_big`, `dcr`, `stn1`, ...) - `common.inc/dogenerate.inc:1688-1693`.

[^21]: `_misc_GetFreePatternMaskModifier(...)` + map-size modifier - `common.inc/dogenerate.inc:1715-1725`.

[^22]: Final densities (`pln_*`, `swamp_*`, `lake_*`) - `common.inc/dogenerate.inc:1727-1739`.

[^23]: `_misc_SetupPatternsByType` for mountains/plateau/ravine/hills - `common.inc/dogenerate.inc:1745-1766`.

[^24]: Phase-2 mines cycle - `common.inc/dogenerate.inc:1768-1771`:
    ```pascal
    for i := 0 to spcount-1 do
       SetupMines(arrStartPos[i].x, arrStartPos[i].y, 1, 0, minesdensity, spcount);
    ```
[^25]: Re-seed after Phase-2 mines - `common.inc/dogenerate.inc:1772`.

[^26]: `_misc_SetupPatternsByType` for forests/stones/plain/swamp/lake - `common.inc/dogenerate.inc:1774-1908`.

[^27]: Cycle `CreateStartPointPeasants` / `CreateUniqueStartingUnits` - `common.inc/dogenerate.inc:1914-1923`.

[^28]: `_misc_PreloadTextures(True, True, True)` - `common.inc/dogenerate.inc:1925`.

[^29]: `gbool_gui_mapgenerationfinished := True` - `common.inc/dogenerate.inc:1939`.

[^30]: Seasonal normalization of env-objects - `common.inc/dogenerate.inc:1971-2027`.

[^31]: AI `progressTick` setup - `common.inc/dogenerate.inc:2031-2050`.

[^32]: `_player_SetupTeams(true)` - `common.inc/dogenerate.inc:2052`.

[^33]: `gfloat_peacetime` / `gbool_peacemode` - `common.inc/dogenerate.inc:2059`.

[^34]: `FillOwnerMap(spcount)` - `common.inc/dogenerate.inc:2062`.

[^35]: `SetupBorderObjects` (under `gbool_peacemode`) - `common.inc/dogenerate.inc:2064-2065`.

[^36]: `_misc_SetShoresCollision` - `common.inc/dogenerate.inc:2068`.

[^37]: Color table per season (winter=6, desert=7, default=0; PHDR=1 for winter) — `common.inc/dogenerate.inc:2075-2084`.

[^38]: Final `TimeLog('Generation finished. ...')` - `common.inc/dogenerate.inc:2100`.

[^39]: `GenerateTeamStartingPoints(teamcount, pointsbusy, points)` - `common.inc/dogenerate.inc:999-1088`.

[^40]: `SetupStartingResources(pointx, pointy)` - `common.inc/dogenerate.inc:720-978`.

[^41]: `FillOwnerMap(spCount)` - `common.inc/dogenerate.inc:1370-1428`.

[^42]: `SetupBorderObjects` - `common.inc/dogenerate.inc:1430-1527`.

[^43]: `CreateStartPointPeasants(plInd, pointx, pointy)` — `common.inc/dogenerate.inc:1231-1281`:
    ```pascal
    count := 18;
    cUnitR := 0.75;
    for i := 0 to count-1 do
    begin
       px := pointx + (i div 3) * cUnitR + (0.5 - RandomExt) * 0.25 - (6 * cUnitR)/2;
       pz := pointy + (i mod 3) * cUnitR + (0.5 - RandomExt) * 0.25 - (0 * cUnitR)/2;
       ...
       SetGameObjectRollAngleByHandle(goHnd, 180);
    end;
    ```
[^44]: Phase-1 mines inside `CreateStartPoint` - `common.inc/dogenerate.inc:985`.

[^45]: Tiny corner-snap for round 2 - `common.inc/dogenerate.inc:658-696` (version ≥ 90).

[^46]: DLC5 terrain types - `common.inc/dogenerate.inc:1555`.

[^47]: Select `inputbitmap` through `floor(RandomExt*count)` - `common.inc/generatemap.inc:179-191`.

[^48]: `SetRandomExtKey64(randkey0, randkey1)` - `common.inc/generatemap.inc:216`.

[^49]: The name of the save file with `randkey1` is `lib/miscext2.script:15` (`'game_v'+gSerialVersion+'k'+randkey1+'.map'`).

[^50]: `GenerateMapRandKey` - `lib/map.script:322` (engine-builtin, body unavailable).
