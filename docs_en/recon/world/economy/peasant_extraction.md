<a id="recon-добыча-ресурсов-крестьянами"></a>
<a id="как-крестьяне-добывают-ресурсы"></a>
# How Peasants Gather Resources

[← How the game works](../../README.md)

A complete model of the extraction rate of all resources: formulas, mines, fields,
efficiency upgrades, map influence. The simulator is built on these numbers
economics and calculations in [`docs/reference/01_economy/README.md`](../../../reference/01_economy/README.md).
All links to the code and the Pascal blocks themselves are collected in the section
[Sources](#sources) at the end of the document.

**Default context (unless otherwise stated in the text):**

- Party speed - **fast** (`gamespeed = 2`, multiplier ×1.4 to normal; see §1).
- Map - `terraintype = 0` (Land), `relieftype = 3` (Highlands),
  `resourcemines = 2` (Rich), `mapsize = 3` (Small, 256 × 256).
- All paths to scripts in [Sources](#sources) are relative to `data/` in the Cossacks 3 installation.

> **Related documents:**
>
> - [determinism_audit.md](../../../../internals_en/engine/determinism_audit.md) - RNG sites in hot
> production paths and expected variation between runs.
> - [ticks_and_subticks.md](../../../../internals_en/engine/ticks_and_subticks.md) - time model,
> sub-tick state-machine, adaptive speed. Needed for correct
> interpretations of real-time versus game-time when taking measurements.
> - [server_sync_architecture.md](../../../../internals_en/engine/server_sync_architecture.md) —
> server-authoritative architecture C3 (important for multiplayer measurements).
> - [map_generation_pipeline.md](../map/map_generation_pipeline.md) — timeline
> `DoGenerate`, starting positions, placement of scaffolding / rocks / mines.

> **TL;DR.** The analytical production ceiling (formulas below) is calculated in
> **game time**. Actual in-game loot will be lower due to
> RNG target selections in `_misc_FindResourceToExtract` (see.
> [determinism_audit.md](../../../../internals_en/engine/determinism_audit.md) §3). Scatter between
> launches of one save in a 5-minute window - 5–15% for forest and stone,
> ≈ 0% for mines.

---

<a id="1-игровая-скорость-и-время"></a>
## 1. Game speed and time

**Basic tick:** `gc_time_to_frames = 32` - 32 frames in one game
second [^1]. All durations in scripts in "frames" must be divided by 32 for
translation to **game seconds (game-time)**.

**Game speeds** (`gc_settings_gamespeed_*`) [^2]:

| Mode | Tag | speedfactor |
|---|---:|---:|
| 0 (slow) | 7 | 0.7× |
| 1 (normal) | 10 | 1.0× |
| **2 (fast)** | **14** | **1.4×** |

**Conclusion for calculations:** all formulas below are given in **game secondsakh**.

<a id="2-цикл-добычи-поведение"></a>
## 2. Mining cycle (behavior)

One peasant's pipeline:

1. **Work tick.** When working, animation `workfood`/`workwood`/`workstone`
   cycle = N frames. Upon reaching the end of the cycle:
    - `OnAclAnimationReachedWork` [^3] is triggered.
    - `arg_obj.resamount += 1` - the “hit” counter in the inventory increases.
    - Resource HP decreases:
      - food: `-= Max(1, floor(100/(1+fieldlife/100)))`. Default fieldlife=0 → 100 HP/hit.
      - wood: `-= 1`. At HP=0 → the tree becomes a stump (see §4.2).
      - stone: `-= 1`. Stone HP = 10,000,000, virtually infinite.

2. **Return to warehouse.** When `resamount >= hitsneeded` [^4]:
    - food: 22, wood: 14, stone: 20 hits.
    - `_unit_GetNearestStorehouse` starts - search the list
      `gPlayer[pl].lists.storehouses` [^5]. Buildings with
      `usage=storage/mill/center` and `resourcebase[restype]=True`.
    - Target - `resourcePoint` warehouse (delivery point in tile coordinates
      from the position of the building; tables for all types - in §3 “Resource delivery points”).

3. **Surrender.** When entering the radius of `gc_gameplay_resourceDropRadiusSqr = 0.5` (≈0.707 tiles):
    - `_unit_PeasantAddResToPlayerByIndex` → `delivered = (portion × eff) / 100` [^6].
- Basic portions (`gc_obj_resource_portion_*`): food=**45**, wood=**28**,
      stone=**40**, other=**20** [^7].
    - `eff` - `gPlayer[pl].resefficiency[cid][restype]`, starts from 100,
      upgrades are added (see §7).
    - `restype := none`, `resamount := 0`, search for a new resource.

4. **Re-acquire.** `_unit_SearchResourceInRadius` near the **starting point of the task**
   (`TOrderInfo.x/y`) [^8]:
    - Standard radius: `gc_obj_res_searchradius = 6` tiles.
    - If `standtime>9` or `random>0.9` → expansion to `2× = 12` tiles [^9].
    - Candidate scoring: `score = (1+myDst/5) × (1+resDst/4) × (1+stoFactor) × (1+attFactor)`.
      `attFactor`/`stoFactor` fine a resource that others are already accessing.
    - Only `brised=True`. Limit of competitive miners per resource:
      food=**3**, wood=**2**, stone=**3**.

<a id="3-константы-extracted"></a>
<a id="3-извлечённые-константы"></a>
## 3. Extracted constants

<a id="анимация--кадры-одного-work-цикла"></a>
<a id="анимация--кадры-одного-рабочего-цикла"></a>
### Animation frames in one work cycle

From `data/animations/aaf/peaaus.aaf` (same for all nations except `pearus`):

| cycle | Frames | g-sec |
|---|---:|---:|
| workfood (aus,fra,eng,...) | 22 | 0.6875 |
| workfood (rus) | 23 | 0.7188 |
| workwood | 18 | 0.5625 |
| workstone | 18 | 0.5625 |
| walk | 20 | 0.625 |
| walkfood | 20 | 0.625 |
| walkwood | 20 | 0.625 |
| walkstone | 20 | 0.625 |

Animation frame rate matches `gc_time_to_frames = 32` (32
frame/g-sec) - confirmed via `parser/parse_animations.py`
and is consistent with the `refspeed.acl` table `TrackPointMoveStep`. See
[`internals/engine/animation_system.md`](../../../../internals_en/engine/animation_system.md).

<a id="базовые-числа-добычи"></a>
### Base loot numbers

| Parameter | Meaning | Source |
|---|---:|---|
| `gc_obj_resource_portion_food` | 45 | [^7] |
| `gc_obj_resource_portion_wood` | 28 | [^7] |
| `gc_obj_resource_portion_stone` | 40 | [^7] |
| `gc_obj_resource_portion_others` | 20 | [^6] |
| `gc_resource_hitsneeded_food` | 22 | [^4] |
| `gc_resource_hitsneeded_wood` | 14 | [^4] |
| `gc_resource_hitsneeded_stone` | 20 | [^4] |
| Default `eff` | 100 | [^10] |
| `gc_FieldMaxHP` | 25,000 | [^11] |

<a id="радиусы-и-расстояния"></a>
### Radii and distances

| Parameter | Value (tiles) | Destination |
|---|---:|---|
| `gc_obj_res_searchradius` | 6 | base search radius after passing |
| (expansion during standtime) | up to 12 (2×) | [^9] |
| `gc_obj_extract_food_radiusmax` | 1.5 (=80×0.01875) | field "impact" range |
| `gc_obj_extract_wood_radiusmax` | 0.75 (=40×0.01875) | tree "impact" range |
| `gc_obj_extract_stone_radiusmax` | 0.9375 (=50×0.01875) | stone "impact" range |
| `gc_gameplay_resourceDropRadiusSqr` | 0.5 (sqrt≈0.707) | delivery radius at the warehouse |

<a id="точки-сдачи-ресурсов-resourcepoint"></a>
### Resource delivery points (resourcePoint)

Each building that receives resources has a fixed point in `data/game/var/objcustom.cfg`
`ResourcePoint {x, z}` — offset in **tile coordinates** from the world position of the building.
It is to her that the peasant goes; it is also used in `_unit_GetNearestStorehouse`
to rank the nearest warehouse. Buildings with `usage = storage / mill / center` and
`resourcebase[restype] = True` are included in the candidate list [^5].

In C3, negative z = north = top of screen. All values with large negative z
are located on the **north (upper) side** of the building.

**Storehouses** (`gc_obj_usage_storage`):

| Building | Internal ID | Nations | `x` | `z` | Position |
|---|---|---|---:|---:|---|
| Storehouse | `eursto` | Austria, Bavaria, Denmark, England, France, Hungary, Netherlands, Piedmont, Prussia, Saxony, Scotland, Sweden, Switzerland, Venice | +0.20 | −1.69 | north corner |
| Storehouse | `russto` | Poland, Russia, Ukraine | +0.19 | −1.50 | north corner |
| Storehouse | `tursto` | Algeria, Turkey | +0.17 | −1.67 | north corner |
| Storehouse | `spasto` | Portugal, Spain | — | — | building centre (0, 0); not specified |

**Mills** (`gc_obj_usage_mill`):
| Building | Internal ID | `x` | `z` | Position |
|---|---|---:|---:|---|
| Mill | `eurmil` | −0.02 | −1.61 | north side |
| Mill | `rusmil` | +0.04 | −1.09 | north side |
| Mill | `turmil` | −0.44 | −2.56 | north side |

**City centers** (`gc_obj_usage_center`):

| Building | Internal ID | `x` | `z` |
|---|---|---:|---:|
| Town Hall | `vencen` | +0.07 | −3.86 |
| Town Hall | `swecen` | +0.02 | −3.68 |
| Town Hall | `engcen` | −0.50 | −3.67 |
| Town Hall | `turcen` | +0.49 | −3.41 |
| Town Hall | `auscen` | −0.11 | −3.34 |
| Town Hall | `spacen` | +0.10 | −3.35 |
| Town Hall | `saxcen` | +0.24 | −3.25 |
| Town Hall | `porcen` | +0.30 | −3.17 |
| Town Hall | `ukrcen` | −1.30 | −3.16 |
| Town Hall | `algcen` | +0.80 | −3.20 |
| Town Hall | `ruscen` | −0.28 | −3.22 |
| Town Hall | `fracen` | +0.01 | −3.12 |
| Town Hall | `prucen` | −0.06 | −3.07 |
| Town Hall | `bavcen` | −1.45 | −3.07 |
| Town Hall | `polcen` | −0.06 | −2.63 |
| Town Hall | `swicen` | −1.82 | −2.51 |
| Town Hall | `huncen` | +1.39 | −2.25 |
| Town Hall | `piecen` | −0.25 | −2.42 |
| Town Hall | `dencen` | −0.10 | −2.20 |
| Town Hall | `netcen` | +0.43 | −2.23 |
| Town Hall | `scocen` | 0 | **−0.72** ⚠ anomalously close to the building centre |

Source: `data/game/var/objcustom.cfg` (`_country_initobjcustom` is parsed at startup).

<a id="скорости-движения"></a>
### Travel speeds

The actual speed is set in `data/animations/ref/refspeed.acl`
through the parameter `TrackPointMoveStep` (tiles per frame of walk animation).
Speed in tiles per game second = `TrackPointMoveStep × 32`:

| Class | `TrackPointMoveStep` | Tiles per game second |
|---|---:|---:|
| Infantry (`infantry`) | 0.03 | **0.96** |
| **Peasant (`peasant`)** | **0.0375** | **1.20** |
| Heavy cavalry (`hardhorse`) | 0.0525 | 1.68 |
| Fast cavalry (`fasthorse`) | 0.09 | 2.88 |
| Cannon (`cannon`) | 0.020625 | 0.66 |

Abstract scale `gc_obj_speed_*` (default = 32, peasant = 40,
hardhorse = 56, fasthorse = 96, cannon = 20, mortar = 24) [^12]
**proportional** `TrackPointMoveStep`, but used
scripts for AI calculations and simplified relative comparisons. For
exact real speeds in tiles are taken from here (`refspeed.acl`).
Details are in [`internals/engine/animation_system.md` §2.4](../../../../internals_en/engine/animation_system.md).

<a id="конкурентные-добытчики-на-одном-ресурсе"></a>
### Competitive miners on one resource

`gc_gameplay_resource_maxattackers_*`:

- food = 3, wood = **2**, stone = 3, none = 4

<a id="4-per-resource-математика"></a>
<a id="4-расчёты-по-каждому-ресурсу"></a>
## 4. Calculations by resource

<a id="41-идеальный-rate-без-хождения"></a>
<a id="41-идеальная-скорость-добычи-без-учёта-пути"></a>
### 4.1 Ideal gathering rate without travel

For one peasant, excluding the road to the warehouse, with `eff=100`, `fieldlife=0`:
```
rate_per_trip = portion × eff / 100             # resource per trip
time_per_trip_game = hitsneeded × t_hit_game    # game seconds
rate = rate_per_trip / time_per_trip_game       # resource per game second
```
| Resource | portion | hitneeded | t_hit_game | rate (units/g-sec) | units/g-min |
|---|---:|---:|---:|---:|---:|
| food (default eff) | 45 | 22 | 0.6875 | **2.975** | **178** |
| wood | 28 | 14 | 0.5625 | **3.556** | **213** |
| stone | 40 | 20 | 0.5625 | **3.556** | **213** |

⚠ This is the **upper limit** - the actual rate is lower due to the road to the warehouse.

<a id="42-wood--большиесредниемелкие-деревья"></a>
<a id="42-дерево-большие-средние-и-малые-деревья"></a>
### 4.2 Wood: large, medium, and small trees

When spawning randomly [^14]:

| Chance | HP | Type | Wood from tree |
|---:|---|---|---:|
| 20% | `floor(8000×(1+random)) = 8000..16000` | **giant** | ≈ 16k..32k wood (HP × 2) |
| 15% | `floor(125×(1+random×4)) = 125..624` | average | ≈ 250..1248 wood |
| 45% | `floor(10+rnd×(0.5+random×0.5)×100)`, `rnd∈[0.2,0.65]` → **20..75** | small | ≈ 40..150 wood |
| 20% | 10 | "stump" | ≈ 20 wood |

Calculation: `gc_resource_hitsneeded_wood = 14`, `gc_obj_resource_portion_wood = 28`, that is, **2 wood per hit** (28/14). Therefore `wood ≈ HP × 2`. This is without upgrades (`eff = 100`); `mill.X` / `aca.X` / `bla.X` is multiplied by `eff`.

**Mediume waiting for HP** (roughly):

- 0.2 × 12000 + 0.15 × 375 + 0.45 × 47 + 0.2 × 10 ≈ **2480 HP** per tree
- With 14 hits/trip ≈ 177 trips per “average” tree, ≈ **4956 wood/tree**.

**Transition tree→stump** [^15]:

- When HP=0 → `gc_statetag_essential_death` → mesh changes to `pinestump1..4`
  (distribution 70/20/5/5%), `collisioninertia=False`.
- `brised` for wood **is never set to False** in the code (unlike
  from food, where flag is used to slow growth). The stump remains
  a valid resource in `gResGrid`, search sees it, and type=wood is saved.

**Preference for whole trees - emergent through penalty queuing.** B
candidate scoring [^16]:
```
score = (1 + dstMy/5) × (1 + dstRes/4) × (1 + stoFactor) × (1 + attFactor)
attFactor = 1 + attcount × 1.5    if attcount ≥ 1, else 0
stoFactor = 1 + stocount × 1.5    if stocount ≥ 1, else 0
```
`attcount` = now they are cutting, `stocount` = now they are coming towards him. `dstMy` —
distance from the peasant, `dstRes` - distance from the starting point
assignments. **Minimum score wins.**

Effect: a resource with 1 active cutter receives a multiplier ×(1+2.5) = **×3.5**
to soon. A whole tree with no cutters nearby always wins over a stump with a cutter
in 2-3 tiles. This is how the observed preference arises - **not because
that this is a stump, but because they are already working on the stump**.

**None stump vs whole tree, both without cutters** - the neighbor wins
distance, without penalty. When the forest is cut down (everything has become stumps), the peasants
work on them evenly, without avoidance.

**Cross-over distances** (approximately): stump with 1 chopper on 2 tiles
loses to the whole tree on ≤8 tiles. But search radius = 6 tiles, so
that the effective zone is ~3-5 tiles of “handicap” to the whole tree above an occupied stump.

**Hard cap:** with `attcount ≥ maxattackers=2` for wood the resource is completely
filtered (75% of the time, 25% chance of bypass via `bskipcheck = random>0.75`).

<a id="43-stone--фактически-бесконечный"></a>
<a id="43-камень-практически-не-истощается"></a>
### 4.3 Stone is effectively inexhaustible

HP = 10,000,000 [^17]. One stone holds 10M hits = 500k runs = 20M
stone Infinite for practical purposes. All calculations for stone - without
accounting for depletion.

<a id="44-food--поле-с-регенерацией"></a>
<a id="44-еда-поле-с-регенерацией"></a>
### 4.4 Food: regenerating Fields

**HP fields:** start = 0, with `essential_birth → essential_none`
set = `gc_FieldMaxHP = 25000` [^18].

**Damage to field per hit:** `resdec = Max(1, floor(100/(1+fieldlife/100)))`.

| fieldlife | resdec/strike | max hits to 0 HP | max food (at eff=100) |
|---:|---:|---:|---:|
| 0 | 100 | 250 | 250 × 45/22 = **511** |
| 100 | 50 | 500 | 1023 |
| 200 | 33 | ~757 | 1549 |
| 300 | 25 | 1000 | 2045 |
| 500 | 16 | 1562 | 3196 |

(Every 22 hits - 1 flight with 45 food; formula: hits × portion / hitsneeded.)

**Field regeneration** [^19]:

- When HP < FieldMaxHP **AND** `visualstage=0` (HP ≥ 13000): every
  `cFieldRestartTime = 31.25` game seconds → `HP += floor(25000 × random × 0.1)`
  (that is, 0..2500 is random).
- At stages <stage_0 (HP<13000) - DOES NOT regenerate.

**Restart field** [^20]:

- HP=0 → `essential_death` → 21.875 game seconds → `essential_birth+visual_stage_0`.
- Then `cFieldGrowTime = 4×21.875 = 87.5` game seconds growth (4 visual
  stages: 0→1→2→3). At this time, `brised=False` cannot be mined.
- Full downtime: 21.875 + 87.5 = **109.375 game seconds**.

<a id="5-шахты-goldironcoal"></a>
<a id="5-шахты-золото-железо-и-уголь"></a>
## 5. Mines: Gold, Iron, and Coal

**Building:** Mine. Most European nations use SIDs `eurgol`,
`euriro`, and `eurcoa`; Russia and Ukraine use the corresponding
`rus*` variants, while Turkey and Algeria use `tur*` [^21].

| Parameter | Meaning |
|---|---:|
| Durability | 2500 |
| Construction time | 300 frames = 9.375 game seconds |
| Price | 100 Wood, 100 Stone (`costpercent=0`; no scaling) |
| `peasantabsorber` | **5** (max 5 peasants inside) |
| `produce[gold/iron/coal]` | **13** |

**Mechanics:** peasant enters → `_unit_AddInside` [^22]:
```
gPlayer[pl].counter.resincome[i] += produce[i]   # +13 for each worker who entered
```
Upon exit/death - corresponding reduction.

**Income tick** [^23]:
```
const mult  = 100
const speed = 256/1.024 = 250
resincome_eff = resincome × gc_time_to_frames        # =13×32=416 per peasant
bank        += resincome_eff × deltatime
realbank     = bank / speed
delivered    = floor(realbank)                        # to the player
```
**Speed per 1 peasant in the mine:**

- For 1 g-sec: bank gain = 13 × 32 × 1.0 = 416. realbank = 416/250 = **1.664** resource/g-sec ≈ **99.8/g-min**

**Full mine (5 peasants, no upgrades):**

- 5 × 1.664 = **8.32 resources/g-sec** ≈ **499/g-min**

<a id="51-mine-upgrades--расширение-вместимости"></a>
<a id="51-улучшения-вместимости-шахты"></a>
### 5.1 Mine-capacity upgrades

Each mine has 6 individual upgrades (`<commonName><res>.1`..`.6`,
`bindividual=True` - needs to be researched at each mine separately). Type:
`gc_upg_type_single_inside_mine`. Effect: `addpeasantabsorber += value`.
Time: 300 frames = 9.375 game-sec each [^24].

| Level | Added capacity | Total capacity | Price | Requirement |
|---|---:|---:|---|---|
| `.1` | +5 | 10 | 1,000 Food, 1,250 Gold | — |
| `.2` | +8 | 18 | 5,250 Food, 4,950 Gold | — |
| `.3` | +10 | 28 | 12,500 Food, 9,250 Gold | — |
| `.4` | +12 | 40 | 15,800 Food, 18,500 Gold | 18th century |
| `.5` | +15 | 55 | 19,800 Food, 21,050 Gold | 18th century |
| `.6` | +40 | **95** | 50,200 Food, 25,950 Gold | 18th century |

**One mine fully upgraded (95 peasants):**

- resincome += 95 × 13 = 1235
- 1235 × 32 / 250 = **158.08 resource/g-sec** ≈ **9,485/g-min**

Total cost full upgrade of one mine: **F104 550, G80 950** (plus 6 × 9.375 = **56.25 g-sec** while the peasants are not working).

⚠ These upgrades are per Mine, not global. Twelve Mines must be
upgraded separately.

<a id="6-поля-и-fieldlife--апгрейды"></a>
<a id="6-улучшения-долговечности-полей"></a>
## 6. Field-durability upgrades

Technical type `gc_upg_type_fieldlifeperc` (ID 23) applies
`gPlayer.fieldlife += value`; the values are additive [^25].

Two upgrades are present for a standard European nation:

| Canonical name | Internal ID | Researched at | Bonus | Price | Source |
|---|---|---|---:|---|---|
| Carry out field melioration | `<csid>aca.4` | Academy | +200 | 1,000 Wood, 475 Gold | [^26] |
| Manufacture agricultural equipment | `<csid>bla.1` | Blacksmith | +100 | 400 Wood, 90 Gold | [^27] |

Total for both: fieldlife = **300** → resdec=25 → 1000 hits/field → 2045 food/field.

⚠ For non-Latin nations (`rus`, `ukr`, `tur`, `alg`, etc.) there may be
nuances need to be double-checked (but the basic formula is general).

<a id="7-апгрейды-efficiency-resefficiency"></a>
<a id="7-улучшения-эффективности-добычи"></a>
## 7. Gathering-efficiency upgrades

All efficiency upgrades are additively added to
`gPlayer.resefficiency[cid][restype]` (default 100):

| Technical type | Resource |
|---|---|
| `gc_upg_type_effectfood` | Food (`food`) |
| `gc_upg_type_effectfoodperc` | Food (`food`) |
| `gc_upg_type_effectwood`/`perc` | Wood (`wood`) |
| `gc_upg_type_effectstone`/`perc` | Stone (`stone`) |

Observed in `country.script` (mill upgrades - `<csid>mil.X` or `<commonName>mil.X`):

- mill `.1`: +40% food
- mill `.2`: +50% food
- mill `.3`: +50% food (requires level 2)
- aca `.8`: +100% wood (mill+blacksmith chain)
- aca `.23`: +100% stone, `.24`: +200% stone

⚠ A complete list of 21 nations must be obtained through an existing
`parser/simulate_upgrades.py`. See §9.

<a id="8-карта-как-вход-для-модели"></a>
## 8. Map as input for the model

Complete procedure `DoGenerate` (cCircle1/2/3, SetupStartingResources, phases
mines, FillOwnerMap, peacetime borders) - in
[map_generation_pipeline.md](../map/map_generation_pipeline.md). Below is only
what is needed for extraction formulas.

<a id="81-игровые-параметры-наш-контекст"></a>
### 8.1 Game parameters (our context)

| UI label | Code field | Tag | Meaning |
|---|---|---:|---|
| Map Shape | `terraintype` | 0 | Land |
| Terrain Type | `relieftype` | 3 | Highlands |
| Minerals | `resourcemines` | 2 | Rich |
| Map Size | `mapsize` | 3 | Tiny (256×256) |

Sources: `data/gui/menu.inc/showcustomgame.inc`, labels in
`data/locale/{en,ru}/{gui,new}.txt`.

**Important detail of Highlands**: density of mountains (`mnt = 0.000120`) - maximum
among all reliefs [^28]. Less flat areas for farms/warehouses, more
Placement attempts fail.

<a id="82-терминология-месторождение-vs-шахта"></a>
<a id="82-терминология-месторождение-и-шахта"></a>
### 8.2 Terminology: deposit vs mine

*Deposit* - geological deposit placed by the generator (patterns
`mng`/`mni`/`mnc`, basenames `minegold`/`mineiron`/`minecoal`).
*Mine* - building `eurgol`/`euriro`/`eurcoa`, built by a peasant on
field (`peasantabsorber=5`, up to 95 with upgrades).

<a id="83-сколько-ресурсов-на-старте"></a>
### 8.3 How many resources are there at the start?

**Deposits.** On Tiny + Rich → 4 rounds × 3 types = **12 deposits
per player** (round 4 skipped on tiny). Distances from start: round 0 =
14-22 tiles (Phase 1, in `CreateStartPoint`), 1 = 32-42, 2 = 70-82, 3 =
22-38 (all Phase 2). Details -
[map_generation_pipeline.md §8](../map/map_generation_pipeline.md#8-что-значит-phase-1-vs-phase-2-mines).

**Starting resources outside mines.** Within a 5-22 tile radius from the city center
always available: **1× stoneforest, 2× stones, 3× forests** (medium/big,
foreststype=0 mix) via `SetupStartingResources`
([map_generation_pipeline.md §4](../map/map_generation_pipeline.md#4-setupstartingresourcespointx-pointy--что-спавнится-возле-города)).
This explains why at the beginning of the game there is always enough wood for ratuse +
the first mill BEFORE the general forest spawn.

<a id="84-леса-и-камни--densities--калибровка-trees-per-pattern"></a>
<a id="84-леса-и-камни-плотность-и-число-деревьев-в-шаблоне"></a>
### 8.4 Forests and Stone: density and trees per pattern

> **`foreststype` always = 0 for Land.** Random initialization
> `floor(RandomExt*3)` immediately overwritten by zero [^29]. `foreststype=1`
> (leaf-only) and =2 (mixed-only) on Land **not activated**. Used
> `foreststype=0` mix: pinefir/spruce/pine/pine_big_2 (big),
> pinefir/spruce/pine (mid), pinefir/pine (small).

Densities [^30]:

- `frs_big = 0.0009`, `frs_mid = 0.0009`, `frs_small = 0.00054`
- `stn1 = 0.00016`, `stn2 = 0.00012`
- `dcr = 0.0005` (decor)

The final density is applied via `_misc_SetupPatternsByType` [^31] with
three factors:

1. `prob*` modifiers [^32] - Monte Carlo on 32000×4 samples in 12/16/24/29-tile
   squares. Shows “how much free space” is left after the terrain
   placement
2. Tiny modifier ×2.5 (`640/256`) for all `prob*`.
3. Per-call splits: `frs_big/8` for 4 types of forest, `frs_mid/6` for 3 types,
   `frs_small/4` into 2 types.

**Numbers for Tiny + Highlands + Land** (source:
[`compute/compute_map_resources.py`](../../../../compute/compute_map_resources.py),
report in [`docs/reports/map/map_resources.md`](../../../reports/map/map_resources.md)):

| Parameter | Meaning |
|---|---:|
| Card size | 65536 tiles (256x256) |
| `prob*` (after ×2.5 modifier) | ≈1.85-2.06 (depending on the pattern size) |
| Big forest clusters (placed, 65% success) | ~34 |
| Mid forest clusters | ~37 |
| Small forest clusters | ~23 |
| Stone clusters | ~21 |
| **Mask cell sum** (placement slots all types) | ~**27,000** per card |
| **Calibrated chopable trees** (mask × 0.30) | ~**8 200** per card |
| Total stones on the map (calibrated) | ~**861** (mask × 0.30) |
| **Initial wood pool** (sum of HP of all trees) | ~**40M wood units** |
| **Efficient wood pool** | **∞** — the stumps are infinite (see §8.5) |
| **Deposits** per player (Rich + Tiny) | **4 gold + 4 iron + 4 coal = 12** (4 rounds × 3 resources; round 4 skipped by tiny) |

<a id="число-деревьев-по-типам-шаблонов"></a>
### Tree counts by pattern type

After decrypting `data/game/var/generator.cfg` section `PatternList`
match the pattern type (for example, `forests_pine_big`) with the list
specific `.pattern` files. Parser -
[`parser/parse_generator_cfg.py`](../../../../parser/parse_generator_cfg.py) →
`docs/derived/pattern_types.json`.

Cross-tabulating with `pattern_inventory.json` (mask cell counts) →
`docs/derived/pattern_type_stats.json`:

| pattern type | n_files | min | **median** | max | example |
|---|---:|---:|---:|---:|---|
| forests_pine_big | 8 | 71 | **148** | 304 | `frt_b_p_1` |
| forests_pine_big_2 | 3 | 155 | **185** | 204 | `b_frt_b_p_1` |
| forests_pine_medium | 10 | 49 | **59** | 97 | `frt_m_p_1` |
| forests_pine_small | 6 | 21 | **44** | 46 | `frt_s_p_1` |
| forests_pinefir_big | 6 | 613 | **920** | 1494 | `d_frt_big_1` |
| forests_pinefir_medium | 6 | 218 | **311** | 383 | `d_frt_mid_1` |
| forests_pinefir_small | 6 | 80 | **172** | 200 | `d_frt_small_1` |
| forests_pinedrygreen_small | 4 | 367 | **629** | 638 | `d_frt_pinedry_*` |
| forests_spruce_big | 4 | 498 | **571** | 576 | spruce variants |
| forests_spruce_medium | 4 | 368 | **469** | 549 | |
| forests_leaf_big | 2 | 574 | **695** | 695 | `g_frt_big_1` |
| forests_leaf_medium | 2 | 388 | **514** | 514 | |
| forests_leaf_small | 6 | 122 | **250** | 450 | |
| forests_mixed_big | 3 | 1111 | **1631** | 2906 | `e_frt_big_1` |
| forests_mixed_medium | 5 | 656 | **895** | 1034 | |
| stoneforests | 8 | 121 | **152** | 164 | forest+stones |
| stones | 7 | 108 | **138** | 193 | `d_stn_*` |
| desert_stones | 12 | 53 | **74** | 101 | desert stone |
| **mng / mni / mnc** (mines) | 6 each | 32 | **32** | 32 | `mng_1` etc. — **= 1 deposit, not 32 objects** |

<a id="что-значит-mask1-решение-через-empirical-calibration"></a>
<a id="что-означает-mask1-проверка-по-игровым-измерениям"></a>
### What `mask=1` means: in-game calibration

`mask=1` cells = **placement slots for env objects**, spawned by C++
function `StandPatternWithAngle` (code not available).

**Mask cells contain:** chopable trees (oak/pine/leaftree/...) + ground
decoration (drytree, decortree*, fallen logs, grass tufts, stumps). Engine
assigns variant_id → specific env-object class - but we don't see it
mapping.

**Empirical calibration (source - user, 2026-04-29):**

- Small forest (`forests_pine_small`, mask median 44): visible chopable trees ≈ **10** → ratio = 0.23
- Large forest (`forests_pine_big`, mask median 148): visible chopable trees ≈ **50** → ratio = 0.34
- Average: **TREE_CHOPABLE_RATIO ≈ 0.30**

**Counter-examples (mask ≠ objects):**

- `mng/mni/mnc` (mines): all 18 files have exactly 32 mask cells, but this
  **1 deposit per pattern** (mask = collision footprint). Not 32 mines.
- `brush_plt_1x1` (4×4, 8 mask=1): = **8 visible bushes** in the game - here
  1:1 (splits are dense).

**Conclusion:** for mines `mask = footprint`, for gaps `mask = 1:1`, for
forests `mask × 0.30 ≈ chopable trees`. This ratio is hardwired into
[`compute/compute_map_resources.py`](../../../../compute/compute_map_resources.py)
as `TREE_CHOPABLE_RATIO`. Refine when more empirical data is available.

<a id="соответствие-типа-шаблона-файлу"></a>
### Pattern type to file mapping

When calling `_misc_PlacePatternByType('forests_pine_big', envHnd, x, y)` [^33]
the engine searches in `gPatternList`, selects one file by `Freq` weight and tries
post via `_misc_CheckStandPatternExt`. After success is called
C++ `StandPatternWithAngle` - it will spawn env objects (the body is not available).

For `foreststype=0` (default mix) the card calls 4 different big types
(pinefir/spruce/pine/pine_big_2), 3 mid-types, 2 small-types. Everyone has
your median tree count → the final sample is weighted by freq and mask-density.

<a id="85-пеньки--бесконечный-wood-pool-критично-для-симуляции"></a>
<a id="85-пеньки-как-неисчерпаемый-источник-дерева"></a>
### 8.5 Stumps as an inexhaustible source of Wood

Behavior source - `OnAclAnimationReachedWork` plus ontagstates
wood-death-handler [^3] [^15].

Life cycle of a tree:

1. **Spawn** [^14]: `brised := True`, HP is assigned randomly by distribution
   (giant 8000-16000 / medium 125-624 / small 10-60 / stub 10).
2. **Every hit** peasant: `hp -= 1, peasant.resamount += 1`.
3. **At hp = 0**: `_unit_SetTagStates(trgHnd, gc_statetag_essential_death)`.
   This is the ontagstates wood-death-handler trigger:
   - mesh changes to `pinestump<1..4>` (random)
   - `SetGameObjectCollisionInertiaByHandle(myHnd, False)`
- **`brised` remains True** (no one resets it to death)
4. **The stump continues to live as a valid goal** for
   `_unit_SearchResourceInRadius` [^34] - check only `brised`, checks
   No HP.
5. The impacts continue: `hp -= 1` goes into negative values (-1, -2, -3, ...).
   Condition `if hp = 0` is triggered only once (at exactly 0), because
   there is no re-transition to death.
6. `peasant.resamount` increments each hit → **tree gives wood indefinitely**.

**Behavioural consequence:** wood “end-game” no. Wood is always available;
the only limitation is the bandwidth of peasants (1 hit/0.5625
g-sec = 3.56 wood/g-sec/peasant) and capacity (2 attackers/tree through
`gc_gameplay_resource_maxattackers_wood`).

**Why do peasants still prefer whole trees?** Not because
HP filter - due to `attFactor` in score:
`tmpRDist = (1+dst/5)*(1+resdst/4)*(1+stoFactor)*(1+attFactor)`, where
`attFactor = 1+attcount*1.5` if ≥1 is already cutting. Therefore fresh
an uncut tree is always closer in “scoring distance” than a popular one
stump. But if all the trees are occupied, the peasants go to the stumps.

**For simulation:** wood pool = effectively infinite. We only consider rate
(peasants × 3.56 wood/g-sec × eff/100) minus walk_overhead to the warehouse.

<a id="9-открытые-вопросы"></a>
## 9. Open questions

| # | Question | How to solve |
|---:|---|---|
| 1 | ~~Peasant's Exact Speed~~ | ✅ **Closed:** `TrackPointMoveStep = 0.0375` × 32 frames / g-sec = **1.20 tiles / g-sec** (see §3 “Movement Speeds” and [`internals/engine/animation_system.md` §2.4](../../../../internals_en/engine/animation_system.md)). |
| 2 | Full list of efficiency upgrades for 21 nations | Use `parser/simulate_upgrades.py` (already inlines SetUpgStruct and iterates over `case cid`). |
| 3 | The real cost of going to the warehouse | Speed is now known (see question 1) → distance × 1/1.20 g-sec/tile. |
| 4 | Accounting `ferry` (delivery from isolated forest islands) | Not critical for tiny+land, put it aside. |
| 5 | `walkintervalfactor` - how it affects walking animation | It looks like the animation speed is scaling relative to the physical speed. Set aside (see also [`internals/engine/animation_system.md` §9](../../../../internals_en/engine/animation_system.md)). |

**What you need for Level B (formulas):** §3-§7 cover everything.
The main parameter - the peasant's speed - is closed through
`TrackPointMoveStep`.

**What is needed for level C (simulator):** additional step 2 (full
list of efficiency upgrades).

---

<a id="источники"></a>
## Sources

All links are relative to `data/` in the Cossacks 3 installation.

[^1]: `gc_time_to_frames = 32` - `scripts/dmscript.global`.

[^2]: `gc_settings_gamespeed_*` - `scripts/dmscript.global:1027-1029`.

[^3]: `OnAclAnimationReachedWork` - `scripts/units/unit.inc/onaclanimationreachedwork.inc`.

[^4]: `gc_resource_hitsneeded_*` (food=22, wood=14, stone=20) and checking `resamount >= hitsneeded` - `scripts/dmscript.global:799-801` and `scripts/lib/res.script:346-358`.

[^5]: `_unit_GetNearestStorehouse` - `scripts/lib/unit.script:9572-9604`.

[^6]: `_unit_PeasantAddResToPlayerByIndex` - `scripts/lib/unit.script:9544-9569`.

[^7]: Basic portions `gc_obj_resource_portion_*` - `scripts/dmscript.global:803-806`.

[^8]: `_unit_SearchResourceInRadius` - `scripts/lib/unit.script:4041-4181`.

[^9]: Search radius extension for `standtime>9` or `random>0.9` is `scripts/lib/unit.script:9824-9826`.

[^10]: Default `eff = 100` - `scripts/lib/player.script:109`.

[^11]: `gc_FieldMaxHP = 25000` - `scripts/dmscript.global:128`.

[^12]: `gc_obj_speed_*` - `scripts/dmscript.global:603-620`.
[^13]: `objbase.speed := gc_obj_speed_peasant` commented out in `scripts/lib/unit.script:1192`; global `objbase.speed := 1` - `scripts/lib/unit.script:618`.

[^14]: HP distribution of trees at spawn - `scripts/env/env.inc/initial.inc:79-89`.

[^15]: Transition tree→stump - `scripts/env/env.inc/ontagstates.inc:50-78`.

[^16]: Resource candidate scoring - `scripts/lib/unit.script:4141-4145`.

[^17]: HP of stone `10 000 000` - `scripts/env/env.inc/initial.inc:96`.

[^18]: HP fields are set = `gc_FieldMaxHP` when `essential_birth → essential_none` - `scripts/env/env.inc/ontagstates.inc:119`.

[^19]: Field regeneration (`cFieldRestartTime = 31.25`) - `scripts/env/env.inc/nothing.inc:78-87`.

[^20]: Restarting the field and `cFieldGrowTime = 87.5` - `scripts/env/env.inc/nothing.inc:31-34`.

[^21]: Building parameters `eurgol`/`euriro`/`eurcoa` - `scripts/lib/unit.script:2311-2323`.

[^22]: `_unit_AddInside` - `scripts/lib/unit.script:3016-3032`.

[^23]: Income tick - `scripts/lib/player.script:240-266`.

[^24]: Mine upgrades (`gc_upg_type_single_inside_mine`, addpeasantabsorber) - `scripts/lib/country.script:3871-3897`.

[^25]: `gc_upg_type_fieldlifeperc` (ID 23), `gPlayer.fieldlife += value` - `scripts/lib/player.script:1830-1832`.

[^26]: Upgrade `<csid>aca.4` (academy, +200 fieldlife) - `scripts/lib/country.script:3490`.

[^27]: Upgrade `<csid>bla.1` (blacksmith, +100 fieldlife) - `scripts/lib/country.script:3714`.

[^28]: Density of the Highlands `mnt = 0.000120` - `scripts/lib/dogenerate.inc:1640-1644`.

[^29]: `foreststype` always = 0 on Land - `scripts/lib/dogenerate.inc:5-6`.

[^30]: Densities (frs_big/mid/small, stn1/2, dcr) - `scripts/lib/dogenerate.inc:1688-1693`.

[^31]: `_misc_SetupPatternsByType` - `scripts/lib/misc.script:3681-3737`.

[^32]: `prob*` Monte Carlo modifiers - `scripts/lib/misc.script:3929-3941`.

[^33]: `_misc_PlacePatternByType` - `scripts/lib/misc.script:3655`.

[^34]: Resource lookup only checks `brised` (no HP check) - `scripts/lib/unit.script:4148`.
