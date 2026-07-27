<a id="recon-добыча-ресурсов-крестьянами"></a>
<a id="как-крестьяне-добывают-ресурсы"></a>
<a id="техническая-модель-добычи-ресурсов-крестьянами"></a>
# Technical Model of Peasant Resource Gathering

[← Scripts and Scenarios](structure.md)

[Reader-facing resource gathering article](../../docs_en/recon/world/economy/peasant_extraction.md)

A technical model of resource gathering: formulas, Mines, Fields, efficiency
upgrades, and map influence. These values support the economy simulator and
the calculations in the
[economy guide](../../docs_en/reference/01_economy/README.md). Code references
and Pascal excerpts are collected under [Sources](#sources).

**Default context (unless otherwise stated in the text):**

- Game speed — **Fast** (`gamespeed = 2`, ×1.4 relative to Normal; see §1).
- Map — `terraintype = 0` (Land), `relieftype = 3` (Highlands),
  `resourcemines = 2` (Rich), `mapsize = 3` (Tiny, 256 × 256).
- All paths to scripts in [Sources](#sources) are relative to `data/` in the Cossacks 3 installation.

> **Related documents:**
>
> - [Determinism and RNG audit](../engine/determinism_audit.md) — random
>   branches in gathering paths and the expected variation between runs.
> - [Ticks and subticks](../engine/ticks_and_subticks.md) — time model,
>   sub-tick state machine, and adaptive speed. Needed for correct
>   interpretation of real time and game time in measurements.
> - [Server architecture and network synchronization](../engine/server_sync_architecture.md)
>   — the server-authoritative model used in multiplayer measurements.
> - [Map generation](../../docs_en/recon/world/map/map_generation_pipeline.md)
>   — `DoGenerate`, starting positions, and the placement of forests, Stone,
>   and deposits.

> **TL;DR.** The analytical ceilings below use **game time**. Actual gathering
> is lower because workers travel and target selection includes random
> branches in `_misc_FindResourceToExtract`; see the
> [RNG audit](../engine/determinism_audit.md) §3. Repeated five-minute runs
> from the same save vary by about 5–15% for wood and Stone, and negligibly
> for Mines.

---

<a id="1-игровая-скорость-и-время"></a>
## 1. Game speed and time

**Basic tick:** `gc_time_to_frames = 32`, so one game second contains 32
frames [^1]. Divide script durations expressed in frames by 32 to convert them
to **game seconds**.

**Game speeds** (`gc_settings_gamespeed_*`) [^2]:

| Mode | Tag | speedfactor |
|---|---:|---:|
| 0 (slow) | 7 | 0.7× |
| 1 (normal) | 10 | 1.0× |
| **2 (fast)** | **14** | **1.4×** |

All formulas below use **game seconds**.

<a id="2-цикл-добычи-поведение"></a>
## 2. Gathering cycle

One Peasant follows this cycle:

1. **Work tick.** When working, animation `workfood`/`workwood`/`workstone`
   cycle = N frames. Upon reaching the end of the cycle:
    - `OnAclAnimationReachedWork` [^3] is triggered.
    - `arg_obj.resamount += 1` increments the carried hit counter.
    - The source loses durability:
      - food: `-= Max(1, floor(100/(1+fieldlife/100)))`. Default fieldlife=0 → 100 HP/hit.
      - wood: `-= 1`. At HP=0 → the tree becomes a stump (see §4.2).
      - stone: `-= 1`. Stone HP = 10,000,000, virtually infinite.

2. **Travel to a drop-off building.** When `resamount >= hitsneeded` [^4]:
    - food: 22, wood: 14, stone: 20 hits.
    - `_unit_GetNearestStorehouse` searches
      `gPlayer[pl].lists.storehouses` [^5] for a building with
      `usage=storage/mill/center` and `resourcebase[restype]=True`.
    - The destination is the building's `resourcePoint`, an offset in map-cell
      coordinates. §3 lists the known values.

3. **Delivery.** Within
   `gc_gameplay_resourceDropRadiusSqr = 0.5` (about 0.707 map cells):
    - `_unit_PeasantAddResToPlayerByIndex` → `delivered = (portion × eff) / 100` [^6].
    - Base portions (`gc_obj_resource_portion_*`): Food=**45**, Wood=**28**,
      stone=**40**, other=**20** [^7].
    - `eff` is `gPlayer[pl].resefficiency[cid][restype]`; it starts at 100
      and receives additive upgrade bonuses (see §7).
    - `restype := none`, `resamount := 0`, search for a new resource.

4. **Find another source.** `_unit_SearchResourceInRadius` searches near the
   **original order point**
   (`TOrderInfo.x/y`) [^8]:
    - Standard radius: `gc_obj_res_searchradius = 6` map cells.
    - If `standtime>9` or `random>0.9` → expansion to `2× = 12` map cells [^9].
    - Candidate scoring:
      `score = (1+myDst/5) × (1+resDst/4) × (1+stoFactor) × (1+attFactor)`.
      `attFactor` and `stoFactor` penalize sources already being worked or
      approached.
    - Only `brised=True`. Limit of competitive miners per resource:
      food=**3**, wood=**2**, stone=**3**.

<a id="3-константы-extracted"></a>
<a id="3-извлечённые-константы"></a>
## 3. Extracted constants

<a id="анимация--кадры-одного-work-цикла"></a>
<a id="анимация--кадры-одного-рабочего-цикла"></a>
### Animation frames in one work cycle

From `data/animations/aaf/peaaus.aaf` (shared by every nation except the
Russian Peasant, `pearus`):

| Cycle | Frames | Game seconds |
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
frames per game second), confirmed through `parser/parse_animations.py`,
and is consistent with the `refspeed.acl` table `TrackPointMoveStep`. See
[Animation system: timings, cycles, impact point](../engine/animation_system.md).

<a id="базовые-числа-добычи"></a>
### Base gathering values

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

| Parameter | Value (map cells) | Destination |
|---|---:|---|
| `gc_obj_res_searchradius` | 6 | base search radius after delivery |
| expansion after a long idle period | up to 12 (2×) | [^9] |
| `gc_obj_extract_food_radiusmax` | 1.5 (=80×0.01875) | Field work range |
| `gc_obj_extract_wood_radiusmax` | 0.75 (=40×0.01875) | tree work range |
| `gc_obj_extract_stone_radiusmax` | 0.9375 (=50×0.01875) | Stone work range |
| `gc_gameplay_resourceDropRadiusSqr` | 0.5 (√≈0.707) | delivery radius at the drop-off point |

<a id="точки-сдачи-ресурсов-resourcepoint"></a>
### Resource delivery points (resourcePoint)

Each resource-accepting building may define a fixed
`ResourcePoint {x, z}` in `data/game/var/objcustom.cfg`. The coordinates are
offsets in **map cells** from the building's world position. A Peasant walks to
this point, and `_unit_GetNearestStorehouse` uses it when ranking candidate
drop-off buildings. Eligible buildings have
`usage = storage / mill / center` and `resourcebase[restype] = True` [^5].

In C3, negative z = north = top of screen. All values with large negative z
are located on the **north (upper) side** of the building.

**Storehouses** (`gc_obj_usage_storage`):

| Building | Internal ID | Nations | `x` | `z` | Position |
|---|---|---|---:|---:|---|
| Storehouse | `eursto` | Austria, Bavaria, Denmark, England, France, Hungary, Netherlands, Piedmont, Prussia, Saxony, Scotland, Sweden, Switzerland, Venice | +0.20 | −1.69 | north corner |
| Storehouse | `russto` | Poland, Russia, Ukraine | +0.19 | −1.50 | north corner |
| Storehouse | `tursto` | Algeria, Turkey | +0.17 | −1.67 | north corner |
| Storehouse | `spasto` | Portugal, Spain | — | — | building center (0, 0); not specified |

**Mills** (`gc_obj_usage_mill`):
| Building | Internal ID | `x` | `z` | Position |
|---|---|---:|---:|---|
| Mill | `eurmil` | −0.02 | −1.61 | north side |
| Mill | `rusmil` | +0.04 | −1.09 | north side |
| Mill | `turmil` | −0.44 | −2.56 | north side |

**Town Halls** (`gc_obj_usage_center`):

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
| Town Hall | `scocen` | 0 | **−0.72** ⚠ anomalously close to the building center |

Source: `data/game/var/objcustom.cfg` (`_country_initobjcustom` is parsed at startup).

<a id="скорости-движения"></a>
### Travel speeds

The actual speed is set in `data/animations/ref/refspeed.acl`
through `TrackPointMoveStep` (map cells per frame of walk animation).
Speed in map cells per game second = `TrackPointMoveStep × 32`:

| Class | `TrackPointMoveStep` | Map cells per game second |
|---|---:|---:|
| Infantry (`infantry`) | 0.03 | **0.96** |
| **Peasant (`peasant`)** | **0.0375** | **1.20** |
| Heavy cavalry (`hardhorse`) | 0.0525 | 1.68 |
| Fast cavalry (`fasthorse`) | 0.09 | 2.88 |
| Cannon (`cannon`) | 0.020625 | 0.66 |

The abstract `gc_obj_speed_*` scale (default = 32, Peasant = 40,
hardhorse = 56, fasthorse = 96, cannon = 20, mortar = 24) [^12]
is proportional to `TrackPointMoveStep`, but scripts use it mainly for AI
calculations and relative comparisons. Exact movement speeds in map cells come
from `refspeed.acl`.
Details are in [Animation system: timings, cycles, impact point §2.4](../engine/animation_system.md).

<a id="конкурентные-добытчики-на-одном-ресурсе"></a>
### Workers competing for one source

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
| Resource | portion | hitneeded | t_hit_game | rate (units/game s) | units/game min |
|---|---:|---:|---:|---:|---:|
| food (default eff) | 45 | 22 | 0.6875 | **2.975** | **178** |
| wood | 28 | 14 | 0.5625 | **3.556** | **213** |
| stone | 40 | 20 | 0.5625 | **3.556** | **213** |

This is the **travel-free ceiling**. Actual gathering is lower because the
Peasant must reach a drop-off building.

<a id="42-wood--большиесредниемелкие-деревья"></a>
<a id="42-дерево-большие-средние-и-малые-деревья"></a>
### 4.2 Wood: large, medium, and small trees

When spawning randomly [^14]:

| Chance | HP | Type | Wood from tree |
|---:|---|---|---:|
| 20% | `floor(8000×(1+random)) = 8000..15999` | **giant** | ≈ 16,000..31,998 Wood (HP × 2) |
| 15% | `floor(125×(1+random×4)) = 125..624` | medium | ≈ 250..1248 wood |
| 45% | `floor(10+rnd×(0.5+random×0.5)×100)`, `rnd∈[0.2,0.65]` → **20..74** | small | ≈ 40..148 Wood |
| 20% | 10 | "stump" | ≈ 20 wood |

Because `gc_resource_hitsneeded_wood = 14` and
`gc_obj_resource_portion_wood = 28`, each hit is worth **two Wood** at
`eff = 100`. The pre-upgrade reserve is therefore approximately
`durability × 2`; gathering-efficiency upgrades scale the delivered amount.

**Expected durability** of a random tree:

- 0.2 × 12000 + 0.15 × 375 + 0.45 × 47 + 0.2 × 10 ≈ **2480 HP** per tree
- At 14 hits per trip, this is about 177 trips and **4,956 Wood per tree**.

**Transition tree→stump** [^15]:

- When HP=0 → `gc_statetag_essential_death` → mesh changes to `pinestump1..4`
  (distribution 70/20/5/5%), `collisioninertia=False`.
- `brised` for wood **is never set to False** in the code (unlike
  from food, where flag is used to slow growth). The stump remains
  a valid resource in `gResGrid`, search sees it, and type=wood is saved.

**Preference for intact trees emerges from worker penalties.** Candidate
scoring [^16]:
```
score = (1 + dstMy/5) × (1 + dstRes/4) × (1 + stoFactor) × (1 + attFactor)
attFactor = 1 + attcount × 1.5    if attcount ≥ 1, else 0
stoFactor = 1 + stocount × 1.5    if stocount ≥ 1, else 0
```
`attcount` is the number already cutting the source, `stocount` the number
approaching it, `dstMy` the distance from this Peasant, and `dstRes` the
distance from the original order point. **The lowest score wins.**

One active worker gives a source a ×3.5 penalty. An unused intact tree can
therefore outrank a nearby stump that is already being worked. The preference
comes from congestion, **not from an explicit stump penalty**.

When an intact tree and a stump are both unused, distance decides. After an
entire forest has become stumps, Peasants distribute among them normally.

**Approximate crossover:** a stump two map cells away with one worker loses to
an unused intact tree up to about eight cells away. Because the ordinary
search radius is six cells, the practical advantage is roughly three to five
cells.

**Worker cap:** once `attcount ≥ maxattackers=2` for Wood, the source is
normally filtered out. `bskipcheck = random>0.75` bypasses this check in
25% of searches.

<a id="43-stone--фактически-бесконечный"></a>
<a id="43-камень-практически-не-истощается"></a>
### 4.3 Stone is effectively inexhaustible

Durability is 10,000,000 [^17]. One Stone object therefore supports ten
million hits, 500,000 full trips, and about 20 million Stone. Depletion can
be ignored in an ordinary match.

<a id="44-food--поле-с-регенерацией"></a>
<a id="44-еда-поле-с-регенерацией"></a>
### 4.4 Food: regenerating Fields

**Field durability:** a new Field starts at zero and receives
`gc_FieldMaxHP = 25,000` during the
`essential_birth → essential_none` transition [^18].

**Damage to field per hit:** `resdec = Max(1, floor(100/(1+fieldlife/100)))`.

| fieldlife | resdec/strike | max hits to 0 HP | max food (at eff=100) |
|---:|---:|---:|---:|
| 0 | 100 | 250 | 250 × 45/22 = **511** |
| 100 | 50 | 500 | 1023 |
| 200 | 33 | ~757 | 1549 |
| 300 | 25 | 1000 | 2045 |
| 500 | 16 | 1562 | 3196 |

(Every 22 hits produce one 45-Food delivery; the formula is
`hits × portion / hitsneeded`.)

**Field regeneration** [^19]:

- When HP < FieldMaxHP **AND** `visualstage=0` (HP ≥ 13000): every
  `cFieldRestartTime = 31.25` game seconds → `HP += floor(25000 × random × 0.1)`
  (that is, 0..2500 is random).
- Below visual stage 0 (`hp < 13,000`), regeneration stops.

**Restart field** [^20]:

- HP=0 → `essential_death` → 21.875 game seconds → `essential_birth+visual_stage_0`.
- The four growth stages then take
  `cFieldGrowTime = 4×21.875 = 87.5` game seconds. During growth,
  `brised=False`, so the Field cannot be harvested.
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
| Base construction time | 300 frames × 10 / 32 = 93.75 game seconds |
| Price | 100 Wood, 100 Stone (`costpercent=0`; no scaling) |
| `peasantabsorber` | **5** (max 5 peasants inside) |
| `produce[gold/iron/coal]` | **13** |

**Mechanic:** when a Peasant enters, `_unit_AddInside` [^22] adds the
Mine's production value to the player's income:
```
gPlayer[pl].counter.resincome[i] += produce[i]   # +13 for each worker who entered
```
Leaving or dying subtracts the same value.

**Income tick** [^23]:
```
const mult  = 100
const speed = 256/1.024 = 250
resincome_eff = resincome × gc_time_to_frames        # =13×32=416 per peasant
bank        += resincome_eff × deltatime
realbank     = bank / speed
delivered    = floor(realbank)                        # to the player
```
**Income from one Peasant:**

- For one game second: bank gain = 13 × 32 × 1.0 = 416. `realbank = 416/250`,
  or **1.664 resources per game second** and about **99.8 per game minute**.

**Full mine (5 peasants, no upgrades):**

- 5 × 1.664 = **8.32 resources per game second**, or about **499 per game minute**.

<a id="51-mine-upgrades--расширение-вместимости"></a>
<a id="51-улучшения-вместимости-шахты"></a>
### 5.1 Mine-capacity upgrades

Each mine has 6 individual upgrades (`<commonName><res>.1`..`.6`,
`bindividual=True`, so each Mine researches them separately). Type:
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
- 1235 × 32 / 250 = **158.08 resources per game second**, or about
  **9,485 per game minute**.

Fully upgrading one Mine costs **104,550 Food and 80,950 Gold**. The six
research steps occupy the Mine for `6 × 9.375 = 56.25` game seconds.

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

National upgrade sets vary, although the underlying formula is universal.

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

Observed in `country.script`:

- Mill `mil.1`: +140% Food
- Mill `mil.2`: +180% Food; absent for Turkey and Algeria
- Academy `aca.1`: +40% Food, `aca.2`: +50%, `aca.3`: +50%
- Academy `aca.8`: +100% Wood (Mill + Blacksmith chain)
- Academy `aca.23`: +100% Stone, `aca.24`: +200% Stone

`parser/simulate_upgrades.py` already expands all 21 national upgrade sets
into `data.json`. Exact nation-specific values are available in the
[upgrade reference](../../docs_en/reference/05_upgrades/README.md).

<a id="8-карта-как-вход-для-модели"></a>
## 8. Map as input for the model

The complete `DoGenerate` pipeline—start circles, `SetupStartingResources`,
deposit phases, `FillOwnerMap`, and peacetime borders—is documented in
[map generation](../../docs_en/recon/world/map/map_generation_pipeline.md).
This section retains only the inputs needed by the gathering model.

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

Highlands has the highest mountain density (`mnt = 0.000120`) of the
available terrain types [^28]. Less flat ground remains for Fields and
drop-off buildings, and more placement attempts fail.

<a id="82-терминология-месторождение-vs-шахта"></a>
<a id="82-терминология-месторождение-и-шахта"></a>
### 8.2 Terminology: deposit vs mine

*Deposit* is a geological site placed by the generator (patterns
`mng`/`mni`/`mnc`, basenames `minegold`/`mineiron`/`minecoal`).
*Mine* is the building placed on that site (`eurgol`/`euriro`/`eurcoa`),
with capacity for five Peasants initially and 95 after all upgrades.

<a id="83-сколько-ресурсов-на-старте"></a>
### 8.3 How many resources are there at the start?

**Deposits.** On Tiny + Rich, four rounds across three resource types create
**12 deposits per player**; the fifth round is skipped. Distances from start:
round 0 =
14–22 map cells (Phase 1, in `CreateStartPoint`), 1 = 32–42, 2 = 70–82, 3 =
22-38 (all Phase 2). Details -
[How a Random Map Is Generated §8](../../docs_en/recon/world/map/map_generation_pipeline.md#8-что-значит-phase-1-vs-phase-2-mines).

**Starting resources outside deposits.** Within 5–22 map cells of the Town Hall,
`SetupStartingResources` places **one mixed Stone-and-forest group, two Stone
groups, and three forest groups**
([How a Random Map Is Generated §4](../../docs_en/recon/world/map/map_generation_pipeline.md#4-setupstartingresourcespointx-pointy--что-спавнится-возле-города)).
before the general environment pass.

<a id="84-леса-и-камни--densities--калибровка-trees-per-pattern"></a>
<a id="84-леса-и-камни-плотность-и-число-деревьев-в-шаблоне"></a>
### 8.4 Forests and Stone: density and trees per pattern

> **`foreststype` is always 0 on Land.** The random initialization
> `floor(RandomExt*3)` is immediately overwritten with zero [^29].
> Leaf-only and mixed-only modes are therefore inactive. The default mix uses
> pinefir/spruce/pine/pine_big_2 (large),
> pinefir/spruce/pine (mid), pinefir/pine (small).

Densities [^30]:

- `frs_big = 0.0009`, `frs_mid = 0.0009`, `frs_small = 0.00054`
- `stn1 = 0.00016`, `stn2 = 0.00012`
- `dcr = 0.0005` (decor)

The final density is applied via `_misc_SetupPatternsByType` [^31] with
three factors:

1. `prob*` modifiers [^32], estimated by Monte Carlo sampling in
   12/16/24/29-cell squares, represent the free space left after terrain
   placement.
2. Tiny modifier ×2.5 (`640/256`) for all `prob*`.
3. Per-call splits: `frs_big/8` for 4 types of forest, `frs_mid/6` for 3 types,
   `frs_small/4` into 2 types.

**Numbers for Tiny + Highlands + Land** (source:
[`compute/compute_map_resources.py`](../../compute/compute_map_resources.py),
report in [map resource estimates](../../docs_en/reports/map/map_resources.md)):

| Parameter | Meaning |
|---|---:|
| Map size | 65,536 cells (256×256) |
| `prob*` (after ×2.5 modifier) | ≈1.85-2.06 (depending on the pattern size) |
| Big forest clusters (placed, 65% success) | ~34 |
| Mid forest clusters | ~37 |
| Small forest clusters | ~23 |
| Stone clusters | ~21 |
| **Total mask cells** (placement slots of all types) | about **27,000** per map |
| **Estimated harvestable trees** (mask × 0.30) | about **8,200** per map |
| Total stones on the map (calibrated) | ~**861** (mask × 0.30) |
| **Initial wood pool** (sum of HP of all trees) | ~**40M wood units** |
| **Efficient wood pool** | **∞** — the stumps are infinite (see §8.5) |
| **Deposits** per player (Rich + Tiny) | **4 Gold + 4 Iron + 4 Coal = 12** (four rounds × three resources; the fifth round is skipped) |

<a id="число-деревьев-по-типам-шаблонов"></a>
### Tree counts by pattern type

After decoding the `PatternList` section of
`data/game/var/generator.cfg`, the parser maps each pattern type, such as
`forests_pine_big`, to its `.pattern` files:
[`parser/parse_generator_cfg.py`](../../parser/parse_generator_cfg.py) →
`derived/pattern_types.json`.

Cross-tabulating with `pattern_inventory.json` (mask cell counts) →
`derived/pattern_type_stats.json`:

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

**Mask cells may contain** harvestable trees
(`oak`/`pine`/`leaftree`/...) or scenery such as dead trees, fallen logs,
grass, and stumps. The native engine maps `variant_id` to a specific
environment-object class; that mapping is not exposed to scripts.

**Empirical calibration (user measurements, 29 April 2026):**

- Small forest (`forests_pine_small`, mask median 44): visible harvestable trees ≈ **10** → ratio = 0.23
- Large forest (`forests_pine_big`, mask median 148): visible harvestable trees ≈ **50** → ratio = 0.34
- Average: **TREE_CHOPABLE_RATIO ≈ 0.30**

**Counter-examples (mask ≠ objects):**

- `mng/mni/mnc` deposit patterns: all 18 files have 32 mask cells, but each
  pattern creates **one deposit**, not 32.
- `brush_plt_1x1` has eight occupied mask cells and produces eight visible
  bushes, a one-to-one case.

**Conclusion:** for deposits the mask is a footprint; for dense decoration
it may be one-to-one; for forests, `mask × 0.30 ≈ harvestable trees`.
This ratio is stored in
[`compute/compute_map_resources.py`](../../compute/compute_map_resources.py)
as `TREE_CHOPABLE_RATIO`. Refine when more empirical data is available.

<a id="соответствие-типа-шаблона-файлу"></a>
### Pattern type to file mapping

When `_misc_PlacePatternByType('forests_pine_big', envHnd, x, y)` is called
[^33], the engine searches `gPatternList`, chooses a file according to its
`Freq` weight, and validates the placement with
`_misc_CheckStandPatternExt`. A successful check calls the native
`StandPatternWithAngle` function, which spawns the environment objects; its
implementation is not available to the scripts.

With `foreststype = 0` (the default mix), the map draws from four large forest
types (`pinefir`, `spruce`, `pine`, and `pine_big_2`), three medium types, and
two small types. Each type has its own median tree count, so the final estimate
is weighted by file frequency and mask density.

<a id="85-пеньки--бесконечный-wood-pool-критично-для-симуляции"></a>
<a id="85-пеньки-как-неисчерпаемый-источник-дерева"></a>
### 8.5 Stumps as an inexhaustible source of wood

The behavior comes from `OnAclAnimationReachedWork` and the wood-death handler
in `ontagstates` [^3] [^15].

Tree life cycle:

1. **Spawn** [^14]: `brised := True`, HP is assigned randomly by distribution
   (giant 8,000–15,999; medium 125–624; small 20–74; spawned stump 10).
2. **Every hit:** `hp -= 1, peasant.resamount += 1`.
3. **At hp = 0**: `_unit_SetTagStates(trgHnd, gc_statetag_essential_death)`.
   This is the ontagstates wood-death-handler trigger:
   - mesh changes to `pinestump<1..4>` (random)
   - `SetGameObjectCollisionInertiaByHandle(myHnd, False)`
- **`brised` remains True** because the death handler never resets it.
4. **The stump remains a valid target** for
   `_unit_SearchResourceInRadius` [^34], which checks `brised` but not
   durability.
5. Further hits drive durability into negative values. The `if hp = 0`
   branch ran only once, at exactly zero.
6. `peasant.resamount` still increments, so the source yields Wood
   indefinitely.

**Consequence:** Wood cannot be exhausted completely. The limits are worker
throughput—one hit per 0.5625 game seconds, or 3.56 Wood per game second at
base efficiency—and the two-worker limit per tree or stump.

**Why do Peasants still prefer intact trees?** Candidate scoring includes the
`attFactor` congestion penalty:
`tmpRDist = (1+dst/5)*(1+resdst/4)*(1+stoFactor)*(1+attFactor)`, where
`attFactor = 1+attcount*1.5` when at least one worker is already cutting.
An unused intact tree can therefore beat a nearer, occupied stump. Once
intact trees are unavailable, Peasants work the stumps.

**Simulation rule:** treat the Wood pool as infinite and model throughput as
`Peasants × 3.56 Wood/game-second × eff/100`, reduced by travel overhead.

<a id="9-открытые-вопросы"></a>
## 9. Open questions

| # | Question | How to solve |
|---:|---|---|
| 1 | Ferry (`ferry`) use for isolated forest islands | Test a route that includes embarkation, crossing, and disembarkation on a divided-island map. |
| 2 | Effect of `walkintervalfactor` on walking | Compare animation speed and physical movement at several values. |
| 3 | Share of working time lost to obstacle avoidance | Record movement traces on several representative layouts and compare them with straight-line travel. |
| 4 | Exact ratio between forest-pattern mask cells and harvestable trees | Expand the in-game sample for every forest-pattern type and recalculate `TREE_CHOPABLE_RATIO`. |

**Level B (formulas):** §3–§7 contain the required values. Physical Peasant
speed is already included as `TrackPointMoveStep × 32 = 1.20` map cells per
game second.

**Level C (simulator):** read the extracted nation-specific efficiency
upgrades from `data.json` and model the remaining overhead listed above.

---

<a id="источники"></a>
## Sources

All links are relative to `data/` in the Cossacks 3 installation.

[^1]: `gc_time_to_frames = 32` — `scripts/dmscript.global`.

[^2]: `gc_settings_gamespeed_*` — `scripts/dmscript.global:1027-1029`.

[^3]: `OnAclAnimationReachedWork` —
      `scripts/units/unit.inc/onaclanimationreachedwork.inc`.

[^4]: `gc_resource_hitsneeded_*` (Food=22, Wood=14, Stone=20) and the
      `resamount >= hitsneeded` check — `scripts/dmscript.global:799-801`
      and `scripts/lib/res.script:346-358`.

[^5]: `_unit_GetNearestStorehouse` — `scripts/lib/unit.script:9572-9604`.

[^6]: `_unit_PeasantAddResToPlayerByIndex` —
      `scripts/lib/unit.script:9544-9569`.

[^7]: Base portions `gc_obj_resource_portion_*` —
      `scripts/dmscript.global:803-806`.

[^8]: `_unit_SearchResourceInRadius` — `scripts/lib/unit.script:4041-4181`.

[^9]: Search radius extension for `standtime>9` or `random>0.9` is `scripts/lib/unit.script:9824-9826`.

[^10]: Default `eff = 100` — `scripts/lib/player.script:109`.

[^11]: `gc_FieldMaxHP = 25000` — `scripts/dmscript.global:128`.

[^12]: `gc_obj_speed_*` — `scripts/dmscript.global:603-620`.
[^13]: `objbase.speed := gc_obj_speed_peasant` is commented out in
       `scripts/lib/unit.script:1192`; the global `objbase.speed := 1` is
       set in `scripts/lib/unit.script:618`.

[^14]: Tree-durability distribution at spawn —
       `scripts/env/env.inc/initial.inc:79-89`.

[^15]: Tree-to-stump transition —
       `scripts/env/env.inc/ontagstates.inc:50-78`.

[^16]: Resource-candidate scoring — `scripts/lib/unit.script:4141-4145`.

[^17]: Stone durability `10,000,000` —
       `scripts/env/env.inc/initial.inc:96`.

[^18]: Field durability becomes `gc_FieldMaxHP` during
       `essential_birth → essential_none` —
       `scripts/env/env.inc/ontagstates.inc:119`.

[^19]: Field regeneration (`cFieldRestartTime = 31.25`) —
       `scripts/env/env.inc/nothing.inc:78-87`.

[^20]: Field restart and `cFieldGrowTime = 87.5` —
       `scripts/env/env.inc/nothing.inc:31-34`.

[^21]: Mine parameters `eurgol`/`euriro`/`eurcoa` —
       `scripts/lib/unit.script:2311-2323`.

[^22]: `_unit_AddInside` — `scripts/lib/unit.script:3016-3032`.

[^23]: Income update — `scripts/lib/player.script:240-266`.

[^24]: Mine upgrades (`gc_upg_type_single_inside_mine`,
       `addpeasantabsorber`) — `scripts/lib/country.script:3871-3897`.

[^25]: `gc_upg_type_fieldlifeperc` (ID 23),
       `gPlayer.fieldlife += value` — `scripts/lib/player.script:1830-1832`.

[^26]: Upgrade `<csid>aca.4` (Academy, +200 `fieldlife`) —
       `scripts/lib/country.script:3490`.

[^27]: Upgrade `<csid>bla.1` (Blacksmith, +100 `fieldlife`) —
       `scripts/lib/country.script:3714`.

[^28]: Highlands density `mnt = 0.000120` —
       `scripts/lib/dogenerate.inc:1640-1644`.

[^29]: `foreststype` is always 0 on Land —
       `scripts/lib/dogenerate.inc:5-6`.

[^30]: Density values (`frs_big/mid/small`, `stn1/2`, `dcr`) —
       `scripts/lib/dogenerate.inc:1688-1693`.

[^31]: `_misc_SetupPatternsByType` — `scripts/lib/misc.script:3681-3737`.

[^32]: `prob*` Monte Carlo modifiers — `scripts/lib/misc.script:3929-3941`.

[^33]: `_misc_PlacePatternByType` — `scripts/lib/misc.script:3655`.

[^34]: Resource lookup checks `brised`, not durability —
       `scripts/lib/unit.script:4148`.
