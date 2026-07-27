<a id="recon-механика-зданий"></a>
<a id="строительство-ремонт-и-разрушение-зданий"></a>
# Building Construction, Repair, and Destruction

[← How the game works](../../README.md)

Deep analysis: footprint, construction and repair by peasants, walls, garrison
towers, capture, destruction. All links to code and Pascal blocks are collected in the section
[Sources](#sources) at the end of the document. All paths there are relative to `data/` in
installing Cossacks 3.

> **Technical details of animation `construct` and frame-accurate timings** —
> to [`internals/engine/animation_system.md`](../../../../internals_en/engine/animation_system.md).

<a id="коротко-о-главном"></a>
## TL;DR

- **Buildtime** for buildings is stored with an additional multiplier
  `gc_buildtime_modifier = 10` [^1]. Units have a multiplier = 1. Real time
  buildings = `frames × 10 / 32`, not `frames / 32`. In `docs/data.json` field
  `building.buildtime_sec` already takes into account ×10.
- **Footprint = collision mask** in file `<sid>.prop`. Cell size -
  0.5 tiles (`gc_collision_size = 0.5`).
- **Repair is free**, +20 HP per peasant hit (`gc_gameplay_repairhp`).
- **Build**: `delta = 0.359 / buildtime` per hit. Animation
  `construct` = 13 frames = 0.406 g-sec.
- **Builder slots** = `bbox_cols + bbox_rows` (Manhattan-perimeter) for
  convex shapes. The hard limit of the engine is 30. Walls are 4 slots per segment.
- **Captureradius** = 4 tiles (see [capture_mechanics.md](capture_mechanics.md)).

---

<a id="1-building-footprint-форма-и-размер"></a>
<a id="1-форма-и-занимаемая-площадь-здания"></a>
## 1. Building shape and footprint

**Source:** `collisionmaskproperty.Mask` in `.prop` building file [^2].

**Unit:** 1 mask cell = **0.5 tiles** (`cellSize := 0.5` [^3]).

**Mask = 2D ASCII grid of 0/1**, where 1 = occupied cell. bavcen example:
```
000110000000          12 cols × 11 rows = 6×5.5 tiles
001111000000          ↓ filled diamond
011111100000
111111110000
011111111000
001111111110
000111111110
000011111100
000001111000
000000110000
000000000000
```
Occupied ≈ 57 cells × 0.5² = 14.25 tiles². Visually - a diagonal square.

**CustomBoundingAABB** (for rendering/clicking) - separate from the collision mask, usually smaller, in tiles: for bavcen X=4.45, Z=2.70.

**ScaleFactor for mask:** 1 [^4] - mask cells are not scaled. `DefaultScale=0.662` (visual) ≠ collision.

**Where is it stored with us:** nowhere yet, you need to extract the footprint mask from the .prop files in JSON.

---

<a id="2-repair-починка--бесплатно"></a>
<a id="2-бесплатный-ремонт"></a>
## 2. Free repairs

**Source:** the construct animation end handler checks the order type and
adds a fixed amount of HP, limited by `maxhp` [^5].

**Constant:** `gc_gameplay_repairhp = 20` [^6].

**Mechanic:**

- Each completed “construct” animation cycle of the peasant → +20 HP to the building.
- **No resources are wasted.** Repairs are absolutely free.
- Capped at maxhp.
- Several peasants are repairing in parallel (see §3 builder slots).

**Construct animation:** 13 frames (186..198 in AAF). Assuming 32 fps = 0.406 g-sec per cycle.

**Calculation of repair speed:**

- 1 peasant: 20 HP / 0.406 g-sec = **49.3 HP/g-sec**
- N peasant: 49.3 × N (up to cap builder slots)
- Bavcen with HP=4000, repair from 0 to full: 4000 / 49.3 = **81 g-sec** by one peasant (~58).
- With 12 builders (typical limit for a center): 81/12 = **6.75 g-sec**.

⚠ Repair works only when the building is **already completed** (`bbuilt = True`). Until the construction is completed, another mechanism operates (see §3).

---

<a id="3-construction-постройка-крестьянами"></a>
<a id="3-постройка-крестьянами"></a>
## 3. Construction by Peasants

<a id="31-прогресс-за-один-удар-молотком"></a>
### 3.1 Progress in one “hammer blow”

Calculation of `delta`, `buildprogress` and HP increase - at each completion
construct animation [^7]:

- `delta := gc_buildtime_progressperhit / buildtime`
- `buildprogress += delta`
- `hp += round(maxhp × delta)` (capped at `maxhp`)

Where is `gc_buildtime_progressperhit = 10 × 1/32 × 1.15 = 0.359375`.

<a id="32-время-постройки-vs-число-строителей--важно"></a>
<a id="32-время-постройки-и-число-строителей"></a>
### 3.2 Construction time and builder count

**Each peasant builder** independently plays a construct animation (13 frames @ 32 fps = 0.406 g-sec per cycle) and at the end of the cycle gives +1 hit. With N builders in parallel - N hits / 0.406 g-sec.

**Formula for N builders:**
```
hits_total = buildtime_g_sec / 0.359375
T_with_N(g-sec) = hits_total / (N / 0.406)
                = buildtime_g_sec × (0.406 / 0.359)/ N
                = buildtime_g_sec × 1.13 / N
```
**Practical rule:** `time = buildtime × 1.13 / N`. You double the peasants → halve the time.

**Cap:** N is limited by the number of builder slots (see §3.3). Engine hard cap: 30.

**Example bavba2 (Barracks 18 century, `buildtime = 5625 game sec`)**:

| N builders | g-sec | min g-sec |
|---:|---:|---:|
| 1 | 6,356 | 105.9 |
| 2 | 3 178 | 53.0 |
| 5 | 1,271 | 21.2 |
| 10 | 636 | 10.6 |
| 16 (slot cap for large building) | 397 | 284 | **4.7 min** ← realistic |

**No one builds a building with ONE peasant in a real game.** When placing a foundation, all idle peasants in the vicinity immediately come running, filling all builder slots.

The complete table of “time with N peasants” for all buildings of all nations is in [`docs/reports/economy/construction_times.md`](../../../reports/economy/construction_times.md) (generator: [`compute/compute_construction_times.py`](../../../../compute/compute_construction_times.py)).

**What's in our JSON:** field `building.buildtime_sec` = `frames × 10/32` is **normalized buildtime** from formula (`objbase.buildtime`). Time-s-1-builder ≈ `buildtime_sec × 1.13`. That is, **the field is NOT equal to the real construction time - it always requires division by N**.

To avoid confusion: you can interpret `buildtime_sec` as “seconds of work for 1 builder, to accumulate full progress” - at the moment when there are N builders, divide by N.

<a id="33-builder-slots-сколько-крестьян-могут-одновременно-строить"></a>
<a id="33-сколько-крестьян-могут-строить-одновременно"></a>
### 3.3 How many Peasants can build at once

**Cap:** `gc_MaxBuilderCount = 30` [^8].
**Min spacing:** `gc_BuilderDist = 1.0` tile [^9].

**Builder points** - specific positions around the building where the peasant stands and works.

**Source of positions:**

1. For most buildings - **dynamically calculated** from collision mask via `_unit_CalcBuilderPoints` [^10]. Algorithm: walks the perimeter of the mask with a step of 0.5 tiles (1 cell), places a dot every `dist=1.0` tile, after the cycle adds another one if `dLen > dist/2`.
2. For walls - from `data/game/var/wallcustom.cfg` (BuilderPoints per wall variation, up to 16).
3. (Optional) Override per-building in `data/game/var/objcustom.cfg` - in the current file there are only ExitPoints/SmokePoints/Decal, no BuilderPoints.

**Exact values for each building:** [`docs/reports/economy/builder_slots.md`](../../../reports/economy/builder_slots.md) and [`derived/builder_slots.json`](../../../../derived/builder_slots.json) - generated by [`compute/compute_builder_slots.py`](../../../../compute/compute_builder_slots.py).

**Geometric insight.** For any convex shape (disc, rhombus, rounded rectangle, diagonal slab - that is, for the vast majority of buildings) Manhattan perimeter = `bbox_cols + bbox_rows`. Walker and `bbox_cols+bbox_rows` give the same result for convex.

**Non-convex buildings** - there are, but not many (5 out of ~350): `scocen` (two “legs” on top, walker=28 vs bbox 24), `swecen` (arch with two legs at the bottom, walker=27 vs bbox 24), `portem` (ledge at the bottom right, +2), `bavhou` (two legs, +1), `ukrtem` (cross-shaped, +1). Walker correctly bypasses internal dents and counts additional slots - **empirically confirmed on swecen=27** (engine actually places peasants inside the arch).

**Full table of empirical points** (9 out of 10 match prediction):

- Convex: polcen=18, ruscen=24, eurmil=10, rusmil=7, polbla=18, polba2=25 ✓
- Non-convex: swecen=27 ✓
- Sparse storehouses: tursto=8 (walker on a large component), spasto=7 (walker on a large one, orphan ignored), russto=8 (bbox_union for linear supports) ✓
- Known discrepancy: eursto prediction 9, empirics 8 (off by 1, reason not identified).
**Strong dependence on the nation.** The size of the mask (and therefore the perimeter) for the same category of building can vary by multiples. Example for 18c barracks (`*ba2`):

| nation | mask | cells | perim (tiles) | slots |
|---|---|---:|---:|---:|
| Venice | 12x9 | 58 | 19 | **19** |
| Saxony | 12x9 | 59 | 20 | **20** |
| Netherlands | 12x10 | 69 | 21 | **21** |
| swi/pie/pru/den | 12x12 | 63-91 | 22 | **22** |
| bav/eng | 12x11 | 65-73 | 23 | **23** |
| Portugal | 12x14 | 86 | 24 | **24** |
| Poland | 14x14 | 87 | 25 | **25** |
| spa/hun | 14x13 | 101-103 | 26 | **26** |
| Sweden | 14x13 | 108 | 27 | **27** |
| aus/fra | 16×15-17 | 112-129 | 29 | **29** |
| sco/rus | 16×15-18 | 123-133 | 30+ | **30** (cap'd) |

**Engine quirk - warehouse sparse masks.** For 4 warehouses (`russto`, `eursto`, `spasto`, `tursto`) the mask is not convex. `tursto` still has one big component - walker gives 8 = fact. `spasto` has a large blot + 1 small orphan in the corner; walker walks correctly most of the time and ignores orphan → 7 = fact (with the empty left side of the building building, as seen in the game). For `russto` and `eursto`, the mask degenerates to **two linear “support” bars** (1×2 and 1×3) with a void between them - a walker on one bar gives 3-4 slots, but in the game the peasants bypass the bbox entirely: 8 vs the result predicted by the walker. Empirically: the rule “if all components are linear → use `bbox_cols + bbox_rows` union” reproduces russto exactly (8=8) and eursto with a known discrepancy of −1 (prediction 9, fact 8). Implemented as fallback `method=bbox_union` in [`compute_builder_slots.py`](../../../../compute/compute_builder_slots.py).

**The gate is an instant custom upgrade on an existing wall segment** (`gc_upg_type_single_buildgate`), rather than a separate building built by peasants. The player selects a completed section of a straight wall from at least three identical segments and clicks “build gate”. In place of the central segment, a new gate object (`*sga` / `*wga`) with `individual.upglevel = 1` is created; the nearest call to `_unit_ControlBuildProgress` through a special branch `if (bwall) and (upglevel>0) then hp := maxhp` immediately sets full HP, after which OnTagStates transfers the object to `bbuilt = True`. No construction is taking place by peasants. More details in [`../combat/walls_and_gates.md`](../combat/walls_and_gates.md).

**Sim vs in-game ±1.** In addition to the described ±1 for eursto, the simulation predicts 23 for bavba2, and the user observed 22 (this is a historical measurement, not rechecked with the new formula - for now we interpret it as a pathing failure for one point or edge of the map).

<a id="34-алгоритм-назначения-крестьянина-на-стройку"></a>
### 3.4 Algorithm for assigning a peasant to a construction site

`_unit_OrderBuild` [^11]:

1. Gets builder slots for the target.
2. For each slot, checks: is it occupied (is someone already building/renovating on it)? If yes, pass.
3. From the free ones, he selects the **closest in Euclidean distance** to the peasant.
4. Assigns a peasant to this slot and sends it there with the move command.
5. Having reached Peasant, the `construct` animation begins to play.
6. Each animation cycle → +HP / +progress (see §2/§3.1).

**Cost:** paid **upfront when setting the foundation** (when you gave the command to build and the peasant came up). After this, no resources are wasted.

---

<a id="4-walls-и-gates-строительство-стен"></a>
<a id="4-стены-и-ворота"></a>
## 4. Walls and Gates

**Type:** `gc_obj_usage_hardwall` / `gc_obj_usage_weakwall` (palisade, woodgate, stonegate, stonewall).

Each **Wall segment** occupies **2×2 tiles**. Builder-point
coordinates in `wallcustom.cfg` range from −1 to +1 around its centre.

**Builder slots per wall variation:**

| Variation | Geometry | Slots |
|---:|---|---:|
| 1 | vertical wall | 4 (2 dots on the left + 2 on the right) |
| 2 | horizontal | 4 (2 top + 2 bottom) |
| 3 | angle/diagonal | 4 |
| 4 | angle/diagonal (mirrored) | 4 |
| 5 | intersection or gate | **12** (12 points around the perimeter of 2x2) |
| 6+ | other | 4-8 |

Cap from the engine: `gc_MaxWallBuilderPointsCount = 16` [^12].

**Wall parameters** (`buildtime_g_sec = frames × 10/32`):

| Wall or Gate | Internal ID | Durability | Frames | Game seconds | Price | Stone consumption |
|---|---|---:|---:|---:|---|---:|
| Wall | `eurswa` | 50,000 | 288 | **90** | 50 Stone | 250 |
| Gate | `eursga` | 32,000 | 288 | **90** | 50 Stone | 250 |
| Russian Wall | `russwa` | 50,000 | 640 | **200** | 60 Stone | 200 |
| Russian Gate | `russga` | 32,000 | 640 | **200** | 60 Stone | 200 |
| Turkish/Algerian Wall | `turswa` | 50,000 | 384 | **120** | 60 Stone | 150 |
| Turkish/Algerian Gate | `tursga` | 32,000 | 384 | **120** | 60 Stone | 150 |
| Palisade | `ukrwwa` | 1,500 | 18 | **5.6** | 10 Wood | 32 |
| Ukrainian Palisade | `ukrwwa` | 2,500 | 26 | **8.1** | 12 Wood | 40 |
| Wooden Gate | `ukrwga` | 1,000 | 18 | **5.6** | 10 Wood | 32 |
| Ukrainian Wooden Gate | `ukrwga` | 1,500 | 26 | **8.1** | 12 Wood | 40 |

`costpercent = 0` - all segments at the same price, without scaling. The walls have `consume.stone` or `consume.wood` - constant consumption while the segment is standing (see artillery in [`../combat/artillery_specifics.md`](../combat/artillery_specifics.md) about the consume mechanics).

Construction time for one segment with N builders: `bt × 1.13 / N` according to the usual building formula - but for walls N is limited to `gCustomBuildPointsWall[wallvariation].builderCount` (see §4 below).

---

<a id="5-garrison--inside-units-объекты-внутри-зданий"></a>
<a id="5-юниты-внутри-зданий"></a>
## 5. Units inside buildings

<a id="51-peasantabsorber--для-шахт"></a>
<a id="51-места-для-крестьян-в-шахтах-peasantabsorber"></a>
### 5.1 Mine capacity for Peasants (`peasantabsorber`)

Mines with SIDs `eurgol`, `euriro`, and `eurcoa` hold five Peasants
by default (`peasantabsorber=5`) and up to 95 after upgrades. See
[Peasant gathering](peasant_extraction.md#5-шахты-золото-железо-и-уголь).

<a id="52-transport--для-транспорта"></a>
<a id="52-вместимость-транспорта-transport"></a>
### 5.2 Transport capacity (`transport`)

Carrying capacity for transport units:

- Ferry (`ferry`): `transport = 80+40 = 120` slots [^13].
- Other transport ships still require separate verification.

<a id="53-tower--built-in-cannon"></a>
<a id="53-башня-как-самостоятельное-орудие"></a>
### 5.3 Tower as a self-contained weapon

A Tower has no garrison (`peasantabsorber=0`, `transport=0`). It is
a stationary artillery building with its own weapon. Basic parameters
for the European version [^14]:

| Parameter | Value |
|---|---|
| weapon[0].kind | `gc_obj_weapon_kind_cannonball` |
| weapon[0].damage | 1000 |
| weapon[0].pause | 400 frames = 12.5 g-sec |
| weapon[0].radiusmin / radiusmax (px) | 550 / 1500 |
| weapon[0].radiusmax (tiles) | ≈ 28.1 |
| weapon[0].detectradiusmin / detectradiusmax (px) | 550 / 50000 |
| weapon[0].cost / shot | iron=10, coal=30 |
| weapon[0].dispersion | 100px |
| Search radius (`searchradius`) | 1400 px ≈ 26.25 tiles |
| Gold consumption (`consume.gold`) | **500 per tick = 0.8 Gold per game second** [^16] |
| Durability | 20,000 |
| Construction time | 3,937 frames ≈ 123 game seconds |
| Cost scaling (`costpercent`) | 120 |
| `bturnoff=True` | The Tower can be disabled to stop consuming Gold |

**Russian version** [^17]: durability 21,000, `buildtime=4725`,
`costpercent=125`, defence 5, and dispersion 125 px. Only the firing
pause is replaced: 300 frames or 9.375 game seconds.

**Turkish version** [^19]: durability 22,500, `buildtime=3150`,
`costpercent=125`, and a price of 150 Stone, 90 Wood, and 100 Gold.
Damage is 1,200; firing pause 500 frames; ammunition costs 40 Coal
and 15 Iron.

**Upgrades:** `gc_ach_upgrade_towerattspeed` (achievement-related, attack speed).

⚠ Infantry **cannot** garrison a Tower. In Cossacks 3, the Tower
fires by itself.

**Parser gap:** weapons for buildings are not yet extracted into `data.json` entirely - there are only scalar fields (`weapon_damage`, `weapon_pause_frames`, `weapon_radiusmax`, `weapon_kind`, `weapon_cost`); If a building has two weapons, only the first one hits. More details are in the [known limitations](../../../../internals_en/project/known_issues.md).

<a id="54-другие-проверки-внутренних-мест"></a>
### 5.4 Other checks for internal capacity

- `bcapture=True` indicates that the object **may be captured** by the enemy (see §7).
- `gc_obj_usage_tower` - special case: captured even without bcapture [^20].

---

<a id="6-ветшание-и-разрушение-зданий"></a>
## 6. Building decay and destruction

<a id="61-decay-ветшание"></a>
<a id="61-ветшание"></a>
### 6.1 Decay

**Not found** in the code. Buildings **do not lose HP** over time on their own. HP changes only from:

- Damage by enemy
- Capture (?) - need to check

<a id="62-destruction-разрушение"></a>
<a id="62-разрушение"></a>
### 6.2 Destruction

HP=0 → state-machine transition via `gc_statetag_essential_death`. Buildings have `bavcen_death1a/death2a` meshes (visualis) - ruins after death.

**Is it possible to rebuild?** - needs to be checked specifically (presumably: no, just build a new building).

<a id="timeline-разрушения"></a>
<a id="последовательность-разрушения"></a>
#### Destruction sequence

With `hp ≤ 0` or `bDie := True`, the building enters
`essential_death`. The state machine [^27] sets the first
`DelayExecuteState` timer:

- if the building was in `essential_birth`, `DeathStage2` runs after
  30 game seconds;
- otherwise `DeathStage1` runs after 30 seconds, changes the model to
  `<sid>_death1`, and schedules `DeathStage2` after another 30 seconds.
  Both delays double for a Mine (`usage = mine`).

**The body** remains on the map in this interval: visually - mesh `<sid>_death1.mesh`, in state `essential_death`, material `'debris'` [^29], collision - the same. The construction of a new building on these squares is impossible until the building disappears.

**Cage reset.** In `DeathStage2` [^30] for non-walls with `gc_collisiontag_terrain` is called `_unit_SetTerrainCollision(myHnd, gc_collisiontag_none)` + `_misc_UnitTopologyUpdate`, then `GameObjectRequestToDestroyByHandle`. After this, the cell is freed, and a new building can be placed on it.

**Garrison inside** (if the building has `peasantabsorber > 0` or `transport > 0`). `_unit_DestroyObj` [^31] collects `gc_argunit_inside` and calls `_unit_DoUnitsGoOutside(list, bDead=True, ...)`. This procedure [^32] gives each unit in the list `essential_death`, meaning the contents die along with the building.

<a id="ondeath-возврат-ресурсов-из-очереди"></a>
<a id="возврат-ресурсов-из-очереди-при-уничтожении"></a>
#### Returning queued resources on destruction

Just before deleting `OnDeath`, the [^33] hook scrolls through the building's order queue:

- `produce` orders are processed through `_unit_ProduceUnit(... bState=False, ...)` [^34] - internally leads to `_unit_CancelUnitProduction` and the return of resources.
- `performupgrade` orders - via `_unit_CancelUpgradePerform`, refund of the base upgrade cost.

That is, when a working barracks or academy is demolished, resources for already paid units and upgrades are **returned** to the player and not burned.

<a id="score-штраф"></a>
<a id="штраф-к-счёту"></a>
#### Score penalty

Upon destruction, to the owner: `−2 × building.score` (or `−5×`, if the building has already been captured - see [`../systems/victory_conditions.md`](../../systems/victory_conditions.md)).

<a id="63-refund-при-отмене-заказов"></a>
<a id="63-возврат-ресурсов-при-отмене-заказов"></a>
### 6.3 Resource refunds after cancellation

| Action | Return | Source |
|---|---|---|
| Cancel an unfinished building (Foundation, GUI button) | **100%** resources spent | GUI-handler `_misc_GUICancelBuilding` [^25] calls `GameObjectDestroyByHandle`; there is no mirror `_res_AddResToPlayerByIndex` for foundation cost in the scripts - refund 100%, apparently processed on the C++ side (behavior in the game is confirmed). |
| Canceling an order for a unit in queue | **100%** of what was written off at the time of order | `_unit_CancelUnitProduction` [^24] returns `price[k] × costmodifier`, where `costmodifier = pow(costpercent/100, restype)` and `restype` are the built-copy counter saved in `OrderInfo` at the time of order. Tech. price is not taken into account. |
| Cancel upgrade | **100%** base price | `_unit_CancelUpgradePerform` [^35] returns the base from `_country_GetUpgradeCostBySID`. Upgrades do not have costpercent scaling. |
| Capture | All canceled orders are interrupted and the resources are returned to the **previous** owner. | See `_misc_ChangePlayer` cleanup thread in [`capture_mechanics.md`](capture_mechanics.md). |

<a id="64-производство-при-низкой-прочности"></a>
<a id="64-производство-при-низком-hp"></a>
### 6.4 Production at low durability

`doprogressorders.inc`: no check for HP. The building produces units while it is alive. **Incomplete building (bbuilt=False) - does not produce.**

---

<a id="7-capture-захват-зданий"></a>
<a id="7-захват-зданий"></a>
## 7. Capturing buildings

**Trigger:** `objprop.bcapture = True` in code or `gc_obj_usage_tower`.

**Mechanic** [^21]:

- Radius: `gc_gameplay_captureradius = 214/53.33 = 4.0 tiles` [^22].
- Block radius: `gc_gameplay_captureblockshotradius = 3.0 tiles`.
- If enemy infantry is within the radius of capturing the building and the owner player is **not** in this radius → the building goes to the enemy.
- **Capture is instantaneous**, verified in-game on April 29, 2026.
  One check satisfying `enemy_in_radius && owner_not_in_radius`
  changes ownership.

**Which buildings can be captured:** Mines, Town Halls, and many
other buildings marked `bcapture=True`.

**Walls and gates are a separate branch.** For segments `bcapture = False`, but in `_misc_CheckCapture` for all `bwall` `bDie := True` is forced - an enemy infantryman within a radius of 4 tiles without defenders **destroys** the segment without transferring it to the owner. When HP < 1/3 of max, the branch is skipped altogether (the wall is already being eaten up with weapons). Details - [`../combat/walls_and_gates.md` §4](../combat/walls_and_gates.md).

When captured:

- HP is saved
- Player ownership → new
- Score for the “invader” with a multiplier of 5 [^23]

⚠ Subtleties: when capturing, `counter.all` is incremented, but `counter.built` is not. This affects price scaling (if a center is captured, your next center will be ×3 as usual - but the captured one is counted in the counter).

---

<a id="8-резюме-механик-быстрый-ответ-на-частые-вопросы"></a>
## 8. Mechanic's resume (quick answer to frequently asked questions)

| Question | Answer |
|---|---|
| Length of one wall segment | 2×2 tiles, 4-12 builder slots depending on variation (§4) |
| objcustom.cfg BuilderPoints override? | There is only `ExitPoints/SmokePoints/Decal` in the file - **all buildings** are counted through dynamic `_unit_CalcBuilderPoints` (bypassing the perimeter mask). Walls are the only exception, they have explicit BuilderPoints in `wallcustom.cfg`. |
| Decay HP | **No.** Buildings only lose HP from damage. Neither the constant `gc_decay` nor calls to `_hp_decay` exist in scripts. |
| Disappearance of debris | **Yes, ~60 seconds** after the building dies. Handlers chain: `OnTagStates.essential_death` → `GameObjectMyDelayExecuteState('DeathStage1', gc_building_deathtime_0=30)` → `DeathStage1` → `GameObjectMyDelayExecuteState('DeathStage2', gc_building_deathtime_1=30)` → `DeathStage2` → `GameObjectRequestToDestroyByHandle`. Mines go 2x slower (`deathtime := deathtime*2`). See `units/building.inc/{settagstates,deathstage1,deathstage2}.inc`. |
| Is it possible to restore a building after HP=0 | **No.** `OnDeath` calls `_unit_DestroyObj` - the building is deleted. Mash `<sid>_death1a/2a` is a visual ruin, not a game object. Only new foundation. |
| Is Capture radius universal? | Yes. `gc_gameplay_captureradius = 4.0 tiles` [^22]. Per-building override not found. |
| Refund if construction is canceled | **Unit queue:** `_unit_CancelUnitProduction` [^24] returns `price[k] × costmodifier`, where `costmodifier = pow(costpercent/100, restype)` and `restype` are the counter of built copies saved at the time of order. That is, exactly as much as was written off is returned. **Foundation (cancel by button):** The GUI handler `_misc_GUICancelBuilding` [^25] calls only `GameObjectDestroyByHandle`. There is no mirror `_res_AddResToPlayerByIndex` for foundation cost in the scripts - processing the return of 100% of spent resources is apparently done on the C++ side (behavior in the game has been confirmed). |

<a id="9-открытые-вопросы"></a>
## 9. Open questions

| # | Question | How to solve |
|---:|---|---|
| 1 | FPS construct animations (= 32 or another?) | Empirical: time one hammer cycle on a building under construction |
| 2 | The exact cost of one wall segment (50 stone - per segment or for the entire drawing?) | Empirical: put 1 segment in the editor, view decommissioned resources |

---

<a id="источники"></a>
## Sources

All links are relative to `data/scripts/` in the Cossacks 3 installation.

[^1]: `gc_buildtime_modifier = 10` for buildings - `lib/misc.script:478-482`.

[^2]: The collision mask is stored in the `collisionmaskproperty.Mask` of each `data/objects/buildings/<sid>.prop`.

[^3]: Mask cell size - `lib/unit.script:8712`:
    ```pascal
    cellSize := 0.5;
    ```
[^4]: Mask ScaleFactor = 1 - `data/objects/buildings/refbuilding.prop:45`.

[^5]: HP increase during repair - `units/unit.inc/onaclanimationreachedconstruct.inc:40-41`:
    ```pascal
    if (arg_obj.orders[0].itype = gc_obj_order_type_repair) then
       TObj(pobj).hp := Min(TObj(pobj).hp + gc_gameplay_repairhp, TObjBase(pobjbase).maxhp);
    ```
[^6]: `gc_gameplay_repairhp = 20` - `dmscript.global:211`.

[^7]: Progress per hit during construction - `units/unit.inc/onaclanimationreachedconstruct.inc:25-37`:
    ```pascal
    delta := (gc_buildtime_progressperhit / TObjBase(pobjbase).buildtime)
    buildprogress += delta
    deltahp := round(maxhp * delta)
    hp += deltahp   // capped at maxhp
    ```
[^8]: `gc_MaxBuilderCount = 30` - `dmscript.global:159`.

[^9]: `gc_BuilderDist = 1.0` - `dmscript.global:160`.

[^10]: `_unit_CalcBuilderPoints` - `lib/unit.script:8702-9006`.

[^11]: `_unit_OrderBuild` - `lib/unit.script:9285-9378`.

[^12]: `gc_MaxWallBuilderPointsCount = 16` - `dmscript.global:137`.

[^13]: The carrying capacity of the ferry is `lib/unit.script:2043` (`transport = 80 + 40 = 120`).

[^14]: Basic European tower - `lib/unit.script:2223-2240`:
    ```pascal
    SetObjBaseWeapon(objprop, objbase, 0, 1000, 400, 550, 1500, 550, 50000, gc_obj_weapon_kind_cannonball, True);
    ```
[^15]: Signature `SetObjBaseWeapon` - `lib/unit.script:520`.

[^16]: `consume.gold = 500/tick` for the tower - `lib/unit.script:2235`.

[^17]: Russian version of the tower - `lib/unit.script:2241-2247` (branch `commonrus`).

[^18]: Conditions for skipping `default = -1` in `SetObjBaseWeapon` - `lib/unit.script:523-538` (`if (damage<>-1)`, etc.).

[^19]: Turkish version of the tower - `lib/unit.script:2248-2256` (branch `commontur`).

[^20]: Special case for `gc_obj_usage_tower` - `lib/unit.script:178`.

[^21]: Grab mechanic - `lib/miscext.script:1018-1030`.

[^22]: `gc_gameplay_captureradius = 214/53.33 = 4.0` - `dmscript.global:208` (see also `lib/miscext.script:1018`).

[^23]: The score multiplier for a capture is `lib/unit.script:3837-3841`.

[^24]: `_unit_CancelUnitProduction` - `lib/unit.script:5891-5977`.

[^25]: `_misc_GUICancelBuilding` - `lib/miscext2.script:3898-3953`.

[^27]: State-death machine of the building - `data/scripts/units/building.inc/settagstates.inc:32-53`.

[^28]: `DeathStage1` - `data/scripts/units/building.inc/deathstage1.inc:5-11`. `DeathStage2` is defined in `deathstage2.inc`.

[^29]: Installing material `'debris'` for the corpse of the building - `data/scripts/units/building.inc/ontagstates.inc:286`.

[^30]: `DeathStage2` - cell release and final removal - `data/scripts/units/building.inc/deathstage2.inc:8-15`.

[^31]: `_unit_DestroyObj` - `lib/miscext2.script:4232-4242`.

[^32]: `_unit_DoUnitsGoOutside` - `lib/unit.script:4559-4564`.

[^33]: OnDeath hook of the building - `data/scripts/units/building.inc/ondeath.inc:11-25`.

[^34]: `_unit_ProduceUnit` - `lib/unit.script:10351`.

[^35]: `_unit_CancelUpgradePerform` - `lib/unit.script:5837-5889`.
