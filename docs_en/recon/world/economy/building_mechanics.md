<a id="recon-механика-зданий"></a>
<a id="строительство-ремонт-и-разрушение-зданий"></a>
# Building Construction, Repair, and Destruction

[← How the game works](../../README.md)

An examination of building footprints, construction and repair by Peasants,
walls, internal capacity, capture, and destruction. Code references and Pascal
excerpts are collected in [Sources](#sources) at the end of the article. All
paths there are relative to `data/` in the Cossacks 3 installation.

> **Frame-accurate details of the `construct` animation** are documented in
> [Animation system: timings, cycles, impact point](../../../../internals_en/engine/animation_system.md).

<a id="коротко-о-главном"></a>
## TL;DR

- **Construction time** (`buildtime`) for buildings carries an additional
  `gc_buildtime_modifier = 10` multiplier [^1]. Units use a multiplier of 1.
  The actual building time is therefore `frames × 10 / 32`, not
  `frames / 32`. The `building.buildtime_sec` field in `docs/data.json`
  already includes the ×10 multiplier.
- **Footprint:** the collision mask in `<sid>.prop`; each mask cell spans
  0.5 tiles (`gc_collision_size = 0.5`).
- **Repair is free** and restores 20 durability per Peasant hammer strike
  (`gc_gameplay_repairhp`).
- **Construction progress:** `delta = 0.359 / buildtime` per strike. One
  `construct` cycle lasts 13 frames, or 0.406 game seconds.
- **Builder positions:** for a convex footprint, their number equals
  `bbox_cols + bbox_rows`. The engine-wide limit is 30; an ordinary wall
  segment has four positions.
- **Capture radius:** four tiles (see [building capture](capture_mechanics.md)).

---

<a id="1-building-footprint-форма-и-размер"></a>
<a id="1-форма-и-занимаемая-площадь-здания"></a>
## 1. Building shape and footprint

**Source:** `collisionmaskproperty.Mask` in `.prop` building file [^2].

**Unit:** 1 mask cell = **0.5 tiles** (`cellSize := 0.5` [^3]).

**The mask is a two-dimensional text grid of zeroes and ones**, where 1
marks an occupied cell. This is the Bavaria Town Hall (`bavcen`):

```
000110000000          12 columns × 11 rows = 6×5.5 tiles
001111000000          ↓ filled diamond shape
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

Approximately 57 cells are occupied: `57 × 0.5² = 14.25` square tiles.
The resulting footprint is a diamond-shaped square.

**The model bounds** (`CustomBoundingAABB`) used for rendering and
selection are separate from the collision mask and usually smaller. For the
Bavaria Town Hall, they are `X = 4.45` and `Z = 2.70` tiles.

**Mask scale:** `ScaleFactor = 1` [^4], so the mask cells are not scaled.
The visual `DefaultScale = 0.662` does not affect collision.

**Project data:** these masks are not extracted yet; exporting the `.prop`
footprints to `JSON` remains future work.

---

<a id="2-repair-починка--бесплатно"></a>
<a id="2-бесплатный-ремонт"></a>
## 2. Free repairs

**Source:** the `construct` animation completion handler checks the order
type and adds a fixed amount of durability, capped at `maxhp` [^5].

**Constant:** `gc_gameplay_repairhp = 20` [^6].

**Mechanic:**

- Every completed Peasant `construct` cycle restores 20 durability.
- **No resources are spent:** repairs are completely free.
- Durability cannot exceed `maxhp`.
- Several Peasants can repair in parallel, using the positions described
  in §3.3.

**Construction animation:** 13 frames (186–198 in `AAF`). At 32 frames
per second, one cycle lasts 0.406 game seconds.

**Calculation of repair speed:**

- One Peasant: `20 / 0.406` = **49.3 durability per game second**.
- N Peasants: `49.3 × N`, until every available position is occupied.
- A Bavaria Town Hall (`bavcen`) with 4,000 durability takes about
  **81 game seconds** to repair from zero with one Peasant.
- Twelve builders complete the same repair in about **6.75 game seconds**.

⚠ Repair applies only to an **already completed** building
(`bbuilt = True`). Before construction finishes, the progress mechanism
described in §3 applies instead.

---

<a id="3-construction-постройка-крестьянами"></a>
<a id="3-постройка-крестьянами"></a>
## 3. Construction by Peasants

<a id="31-прогресс-за-один-удар-молотком"></a>
### 3.1 Progress in one “hammer blow”

The game calculates `delta`, `buildprogress`, and the durability increase
whenever a `construct` animation finishes [^7]:

- `delta := gc_buildtime_progressperhit / buildtime`
- `buildprogress += delta`
- `hp += round(maxhp × delta)`, capped at `maxhp`

Here, `gc_buildtime_progressperhit = 10 × 1/32 × 1.15 = 0.359375`.

<a id="32-время-постройки-vs-число-строителей--важно"></a>
<a id="32-время-постройки-и-число-строителей"></a>
### 3.2 Construction time and builder count

**Each Peasant builder** independently plays the `construct` animation:
13 frames at 32 frames per second, or 0.406 game seconds per cycle.
Completing a cycle counts as one hammer strike.

**Formula for N builders:**

```
hits_total = buildtime_g_sec / 0.359375
T_with_N(g-sec) = hits_total / (N / 0.406)
                = buildtime_g_sec × (0.406 / 0.359)/ N
                = buildtime_g_sec × 1.13 / N
```

**Practical rule:** `time = buildtime × 1.13 / N`. Doubling the number
of Peasants approximately halves the construction time.

**Limit:** N cannot exceed the number of available builder positions
(§3.3), and the engine never allows more than 30.

**Example: the Bavaria 18th-century Barracks (`bavba2`), with
`buildtime = 5625` game seconds:**

| Builders | Game seconds | Game minutes |
|---:|---:|---:|
| 1 | 6,356 | 105.9 |
| 2 | 3,178 | 53.0 |
| 5 | 1,271 | 21.2 |
| 10 | 636 | 10.6 |
| 16 | 397 | **6.6** |

In practice, a large building is rarely constructed by a single Peasant.
After the foundation is placed, nearby idle Peasants occupy the available
positions around it.

The complete table for all nations and buildings is in the
[construction-time report](../../../reports/economy/construction_times.md)
(generated by [`compute/compute_construction_times.py`](../../../../compute/compute_construction_times.py)).

**Value stored in `JSON`:** `building.buildtime_sec = frames × 10/32`
is the normalized `objbase.buildtime`. The actual time for one builder is
approximately `buildtime_sec × 1.13`; for N builders, divide that result
by N.

<a id="33-builder-slots-сколько-крестьян-могут-одновременно-строить"></a>
<a id="33-сколько-крестьян-могут-строить-одновременно"></a>
### 3.3 How many Peasants can build at once

**Limit:** `gc_MaxBuilderCount = 30` [^8].
**Minimum spacing:** `gc_BuilderDist = 1.0` tile [^9].

**Builder positions** are the exact places around a building where a
Peasant can stand and work.

**Source of positions:**

1. For most buildings, `_unit_CalcBuilderPoints` [^10] calculates them
   **dynamically** from the collision mask. It walks the perimeter in
   0.5-tile steps and places a point every `dist = 1.0` tile.
2. Walls use the explicit `BuilderPoints` for each wall variation in
   `data/game/var/wallcustom.cfg`, with at most 16 positions.
3. `data/game/var/objcustom.cfg` allows a per-building override, but the
   current file contains only `ExitPoints`, `SmokePoints`, and `Decal`.

**Exact values for each building:** see the
[builder-position report](../../../reports/economy/builder_slots.md) and
[`derived/builder_slots.json`](../../../../derived/builder_slots.json),
generated by [`compute/compute_builder_slots.py`](../../../../compute/compute_builder_slots.py).

**Geometric rule.** For a convex footprint—a disc, diamond, or rounded
rectangle—the Manhattan perimeter equals `bbox_cols + bbox_rows`. The mask
walker produces the same result.

Only five of roughly 350 buildings are **non-convex**: the Scotland
Town Hall (`scocen`), Sweden Town Hall (`swecen`), Portugal Cathedral
(`portem`), Ukraine Cathedral (`ukrtem`), and Bavaria House (`bavhou`).
The walker follows their recesses and therefore finds additional positions.
The result of 27 positions for the Sweden Town Hall has been confirmed
in-game.

**Empirical checks** agree with the calculation in 9 of 10 cases:

- Convex buildings: Poland Town Hall (`polcen`) = 18, Russia Town Hall
  (`ruscen`) = 24, European Mill (`eurmil`) = 10, Russia Mill
  (`rusmil`) = 7, Poland Blacksmith (`polbla`) = 18, and Poland
  18th-century Barracks (`polba2`) = 25. ✓
- Non-convex Sweden Town Hall (`swecen`) = 27. ✓
- Sparse Storehouses: Turkey (`tursto`) = 8, Spain (`spasto`) = 7,
  and Russia (`russto`) = 8. ✓
- Known discrepancy: the calculation gives 9 for the European Storehouse
  (`eursto`), while the in-game measurement is 8.

**The nation matters.** Footprint size, and therefore perimeter, can vary
considerably within one building category. The 18th-century Barracks
(`*ba2`) is a useful example:

| Nation | Mask | Occupied cells | Perimeter, tiles | Positions |
|---|---|---:|---:|---:|
| Venice (`ven`) | 12×9 | 58 | 19 | **19** |
| Saxony (`sax`) | 12×9 | 59 | 20 | **20** |
| Netherlands (`net`) | 12×10 | 69 | 21 | **21** |
| Switzerland, Piedmont, Prussia, Denmark | 12×12 | 63–91 | 22 | **22** |
| Bavaria, England | 12×11 | 65–73 | 23 | **23** |
| Portugal (`por`) | 12×14 | 86 | 24 | **24** |
| Poland (`pol`) | 14×14 | 87 | 25 | **25** |
| Spain, Hungary | 14×13 | 101–103 | 26 | **26** |
| Sweden (`swe`) | 14×13 | 108 | 27 | **27** |
| Austria, France | 16×15–17 | 112–129 | 29 | **29** |
| Scotland, Russia | 16×15–18 | 123–133 | 30+ | **30** |

**Sparse Storehouse masks.** The Russia (`russto`), European (`eursto`),
Spain (`spasto`), and Turkey (`tursto`) Storehouses have non-convex
footprints. The ordinary walk correctly finds 8 positions for Turkey and
7 for Spain. The Russia and European masks reduce to two separate linear
supports, so the game follows their combined bounding box. The rule
“use the union's `bbox_cols + bbox_rows` when every component is linear”
reproduces Russia exactly and differs by one for the European Storehouse.
The calculator implements this fallback as `method=bbox_union`.

**A Gate is an instantaneous individual upgrade to an existing Wall
segment** (`gc_upg_type_single_buildgate`), not a separate building that
Peasants construct. The player selects a straight, completed run of at
least three segments. The central segment is replaced with a Gate
(`*sga` or `*wga`) at `individual.upglevel = 1`;
`_unit_ControlBuildProgress` immediately assigns full durability, and
`OnTagStates` sets `bbuilt = True`. See [Walls and Gates](../combat/walls_and_gates.md).

**One-position discrepancies.** Besides the European Storehouse result,
the calculator gives 23 positions for the Bavaria 18th-century Barracks
(`bavba2`), while an older in-game measurement found 22. That measurement
has not yet been repeated; one inaccessible point or proximity to the map
edge may explain it.

<a id="34-алгоритм-назначения-крестьянина-на-стройку"></a>
### 3.4 Algorithm for assigning a peasant to a construction site

`_unit_OrderBuild` [^11]:

1. Obtain the target's builder positions.
2. Skip each position already occupied by a builder or repairer.
3. Choose the free position **closest to the Peasant by Euclidean distance**.
4. Assign the Peasant to that position and issue the internal `move` command.
5. Once the Peasant arrives, begin the `construct` animation.
6. Each completed cycle adds durability and construction progress.

**The entire cost is charged when the foundation is placed**, once the
Peasant reaches the construction site. No further resources are spent.

---

<a id="4-walls-и-gates-строительство-стен"></a>
<a id="4-стены-и-ворота"></a>
## 4. Walls and Gates

**Internal roles:** `gc_obj_usage_hardwall` and
`gc_obj_usage_weakwall`, covering the Palisade, Wooden Gate, Stone Gate,
and Stone Wall.

Each **Wall segment** occupies **2×2 tiles**. Builder-position
coordinates in `wallcustom.cfg` range from −1 to +1 around its centre.

**Builder slots per wall variation:**

| Variation | Geometry | Positions |
|---:|---|---:|
| 1 | vertical wall | 4 (2 dots on the left + 2 on the right) |
| 2 | horizontal | 4 (2 top + 2 bottom) |
| 3 | angle/diagonal | 4 |
| 4 | angle/diagonal (mirrored) | 4 |
| 5 | intersection or gate | **12** (around the 2×2 perimeter) |
| 6+ | other | 4-8 |

The engine limit is `gc_MaxWallBuilderPointsCount = 16` [^12].

**Wall parameters** (`buildtime_g_sec = frames × 10/32`):

| Wall or Gate | Internal ID | Durability | Frames | Game seconds | Price | Stone consumption |
|---|---|---:|---:|---:|---|---:|
| Stone Wall | `eurswa` | 50,000 | 288 | **90** | 50 Stone | 250 |
| Stone Gate | `eursga` | 32,000 | 288 | **90** | 50 Stone | 250 |
| Russia Stone Wall | `russwa` | 50,000 | 640 | **200** | 60 Stone | 200 |
| Russia Stone Gate | `russga` | 32,000 | 640 | **200** | 60 Stone | 200 |
| Turkey/Algeria Stone Wall | `turswa` | 50,000 | 384 | **120** | 60 Stone | 150 |
| Turkey/Algeria Stone Gate | `tursga` | 32,000 | 384 | **120** | 60 Stone | 150 |
| Palisade | `ukrwwa` | 1,500 | 18 | **5.6** | 10 Wood | 32 |
| Ukrainian Palisade | `ukrwwa` | 2,500 | 26 | **8.1** | 12 Wood | 40 |
| Wooden Gate | `ukrwga` | 1,000 | 18 | **5.6** | 10 Wood | 32 |
| Ukrainian Wooden Gate | `ukrwga` | 1,500 | 26 | **8.1** | 12 Wood | 40 |

With `costpercent = 0`, every segment has the same price. The
`consume.stone` and `consume.wood` fields define continuing resource
consumption while the segment exists.

Construction time for one segment with N builders follows the ordinary
formula, `bt × 1.13 / N`, but N is limited by
`gCustomBuildPointsWall[wallvariation].builderCount`.

---

<a id="5-garrison--inside-units-объекты-внутри-зданий"></a>
<a id="5-юниты-внутри-зданий"></a>
## 5. Units inside buildings

<a id="51-peasantabsorber--для-шахт"></a>
<a id="51-места-для-крестьян-в-шахтах-peasantabsorber"></a>
### 5.1 Mine capacity for Peasants (`peasantabsorber`)

Gold Mine (`eurgol`), Iron Mine (`euriro`), and Coal Mine (`eurcoa`)
hold five Peasants by default (`peasantabsorber = 5`) and up to 95 after
upgrades. See
[Peasant gathering](peasant_extraction.md#5-шахты-золото-железо-и-уголь).

<a id="52-transport--для-транспорта"></a>
<a id="52-вместимость-транспорта-transport"></a>
### 5.2 Transport capacity (`transport`)

Capacity for transport units:

- Ferry (`ferry`): `transport = 80 + 40 = 120` places [^13].
- Other transport ships still require separate verification.

<a id="53-tower--built-in-cannon"></a>
<a id="53-башня-как-самостоятельное-орудие"></a>
### 5.3 Tower as a self-contained weapon

A Tower has no garrison (`peasantabsorber = 0`, `transport = 0`). It is
a stationary artillery building with its own weapon. The basic European
version has the following parameters [^14]:

| Parameter | Value |
|---|---|
| Projectile type (`weapon[0].kind`) | `gc_obj_weapon_kind_cannonball` |
| Damage (`weapon[0].damage`) | 1,000 |
| Reload time (`weapon[0].pause`) | 400 frames = 12.5 game seconds |
| Minimum / maximum range (`radiusmin`, `radiusmax`) | 550 / 1,500 pixels |
| Maximum range in tiles | ≈ 28.1 |
| Detection radius (`detectradiusmin`, `detectradiusmax`) | 550 / 50,000 pixels |
| Shot cost (`weapon[0].cost`) | 10 Iron, 30 Coal |
| Dispersion (`weapon[0].dispertion`) | 100 pixels |
| Search radius (`searchradius`) | 1,400 pixels ≈ 26.25 tiles |
| Gold consumption (`consume.gold`) | **500 per tick = 0.8 Gold per game second** [^16] |
| Durability | 20,000 |
| Construction time | 3,937 frames ≈ 123 game seconds |
| Price growth (`costpercent`) | 120 |
| `bturnoff = True` | The Tower can be disabled to stop consuming Gold |

**Russia version** [^17]: 21,000 durability, `buildtime = 4725`,
`costpercent = 125`, defence 5, and dispersion 125 pixels. Its reload
time is 300 frames, or 9.375 game seconds.

**Turkey version** [^19]: 22,500 durability, `buildtime = 3150`,
`costpercent = 125`, and a price of 150 Stone, 90 Wood, and 100 Gold.
It deals 1,200 damage, reloads in 500 frames, reaches 1,600 pixels, and
spends 40 Coal and 15 Iron per shot.

**Upgrade:** `gc_ach_upgrade_towerattspeed` increases the rate of fire
and is tied to an achievement.

⚠ Infantry **cannot** garrison a Tower. In Cossacks 3, the Tower
fires by itself.

**Data limitation:** building weapons are not yet extracted completely.
If a building has two weapons, only the first appears in the summary.
Technical details are listed under
[known limitations](../../../../internals_en/project/known_issues.md).

<a id="54-другие-проверки-внутренних-мест"></a>
### 5.4 Other checks for internal capacity

- `bcapture = True` marks an object that **can be captured** by an enemy
  (see §7).
- `gc_obj_usage_tower` is a special case: the capture check runs even
  without `bcapture` [^20].

---

<a id="6-ветшание-и-разрушение-зданий"></a>
## 6. Building decay and destruction

<a id="61-decay-ветшание"></a>
<a id="61-ветшание"></a>
### 6.1 Decay

No decay mechanic was found in the scripts. Buildings **do not lose
durability over time** on their own. It changes only through:

- enemy damage;
- capture, which still requires a dedicated check.

<a id="62-destruction-разрушение"></a>
<a id="62-разрушение"></a>
### 6.2 Destruction

At zero durability, a building enters `gc_statetag_essential_death`.
Models such as `bavcen_death1a` and `bavcen_death2a` depict the ruins,
but they are not separate game objects.

**Can it be rebuilt?** This still needs a direct test; the likely answer
is no, and the player must place a new building.

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

**The remains** stay on the map during this interval as
`<sid>_death1.mesh`, in the `essential_death` state, with the `debris`
material [^29] and the original collision footprint. No new building can
be placed on those tiles until the remains disappear.

**Releasing the footprint.** In `DeathStage2` [^30], a non-wall with
`gc_collisiontag_terrain` calls
`_unit_SetTerrainCollision(myHnd, gc_collisiontag_none)` and
`_misc_UnitTopologyUpdate`, followed by
`GameObjectRequestToDestroyByHandle`. The occupied tiles then become
available for construction.

**Units inside** a building with `peasantabsorber > 0` or
`transport > 0` die with it. `_unit_DestroyObj` [^31] collects
`gc_argunit_inside` and calls `_unit_DoUnitsGoOutside(list, bDead=True,
...)`; that procedure assigns `essential_death` to every contained unit
[^32].

<a id="ondeath-возврат-ресурсов-из-очереди"></a>
<a id="возврат-ресурсов-из-очереди-при-уничтожении"></a>
#### Returning queued resources on destruction

Immediately before deletion, the `OnDeath` handler [^33] processes the
building's order queue:

- `produce` orders pass through
  `_unit_ProduceUnit(... bState=False, ...)` [^34], which ultimately calls
  `_unit_CancelUnitProduction` and refunds their resources.
- `performupgrade` orders pass through `_unit_CancelUpgradePerform`,
  refunding the base upgrade cost.

If a working Barracks or Academy is destroyed, the resources already
paid for queued units and upgrades are therefore **returned** to the
player.

<a id="score-штраф"></a>
<a id="штраф-к-счёту"></a>
#### Score penalty

Destruction subtracts `2 × building.score` from the owner's score, or
`5 × building.score` if the building has previously been captured. See
[Victory, Defeat, and the End of a Match](../../systems/victory_conditions.md).

<a id="63-refund-при-отмене-заказов"></a>
<a id="63-возврат-ресурсов-при-отмене-заказов"></a>
### 6.3 Resource refunds after cancellation

| Action | Return | Source |
|---|---|---|
| Cancel an unfinished building through the interface | **100%** of the resources spent | `_misc_GUICancelBuilding` [^25] calls `GameObjectDestroyByHandle`. The scripts do not contain a matching `_res_AddResToPlayerByIndex`, so the engine probably handles the refund; the in-game result has been confirmed. |
| Cancel a queued unit | **100%** of the amount charged when it was ordered | `_unit_CancelUnitProduction` [^24] returns `price[k] × costmodifier`. The saved `restype` value records the number of completed copies at ordering time, so later price changes do not affect the refund. |
| Cancel an upgrade | **100%** of its base price | `_unit_CancelUpgradePerform` [^35] returns the base price from `_country_GetUpgradeCostBySID`; upgrades do not use `costpercent` scaling. |
| Capture | Cancelled orders are interrupted and their resources return to the **previous** owner. | See the `_misc_ChangePlayer` cleanup path in [building capture](capture_mechanics.md). |

<a id="64-производство-при-низкой-прочности"></a>
<a id="64-производство-при-низком-hp"></a>
### 6.4 Production at low durability

`doprogressorders.inc` contains no durability check. A building continues
producing units while it remains alive, but an unfinished building
(`bbuilt = False`) cannot produce.

---

<a id="7-capture-захват-зданий"></a>
<a id="7-захват-зданий"></a>
## 7. Capturing buildings

**Eligibility:** `objprop.bcapture = True`, or the special
`gc_obj_usage_tower` role.

**Mechanic** [^21]:

- Capture radius: `gc_gameplay_captureradius = 214/53.33 = 4.0` tiles
  [^22].
- Fire-blocking radius: `gc_gameplay_captureblockshotradius = 3.0` tiles.
- If enemy infantry is inside the capture radius and the owning player
  has no unit there, the building changes hands.
- **Capture is instantaneous.** An in-game test on 29 April 2026
  confirmed that one check satisfying
  `enemy_in_radius && owner_not_in_radius` changes ownership.

**Which buildings can be captured:** Mines, Town Halls, and many
other buildings marked `bcapture=True`.

**Walls and Gates use a separate path.** Their segments have
`bcapture = False`, but `_misc_CheckCapture` forces `bDie := True` for
every `bwall`: undefended enemy infantry within four tiles **destroys**
the segment instead of taking ownership. The branch is skipped below
one-third durability. See [Walls and Gates §4](../combat/walls_and_gates.md).

When captured:

- Durability is preserved.
- Ownership changes to the capturing player.
- The capturing player receives score with a ×5 multiplier [^23].

⚠ On capture, `counter.all` increases but `counter.built` does not. This
still affects price scaling: a captured Town Hall counts toward the price
of the next one, which can therefore cost three times as much.

---

<a id="8-резюме-механик-быстрый-ответ-на-частые-вопросы"></a>
## 8. Mechanics summary

| Question | Answer |
|---|---|
| Size of one Wall segment | 2×2 tiles, with 4–12 builder positions depending on its variation (§4) |
| Can `objcustom.cfg` override builder positions? | The current file contains only `ExitPoints`, `SmokePoints`, and `Decal`. `_unit_CalcBuilderPoints` calculates positions dynamically for buildings; Walls alone have explicit `BuilderPoints` in `wallcustom.cfg`. |
| Does durability decay? | **No.** Buildings lose durability only through damage. Neither `gc_decay` nor calls to `_hp_decay` appear in the scripts. |
| When do the remains disappear? | **About 60 seconds after destruction.** The state sequence is `OnTagStates.essential_death` → `DeathStage1` → `DeathStage2` → `GameObjectRequestToDestroyByHandle`. Mines take twice as long. |
| Can a building be restored after reaching zero durability? | **No.** `OnDeath` calls `_unit_DestroyObj`; `<sid>_death1a/2a` is only the ruin model. A new foundation must be placed. |
| Is the capture radius universal? | Yes. `gc_gameplay_captureradius = 4.0` tiles [^22]; no per-building override was found. |
| What is refunded when construction is cancelled? | Cancelling a queued unit returns exactly the amount charged through `_unit_CancelUnitProduction` [^24]. Cancelling a foundation through `_misc_GUICancelBuilding` [^25] returns 100% of the cost, probably through engine-side handling. |

<a id="9-открытые-вопросы"></a>
## 9. Open questions

| # | Question | How to solve |
|---:|---|---|
| 1 | Does the `construct` animation run at 32 frames per second? | Time one hammer cycle on a building under construction |
| 2 | Is 50 Stone the cost of one Wall segment or the whole drawn section? | Place a single segment in the editor and measure the deduction |

---

<a id="источники"></a>
## Sources

All links are relative to `data/scripts/` in the Cossacks 3 installation.

[^1]: `gc_buildtime_modifier = 10` for buildings —
      `lib/misc.script:478-482`.

[^2]: Each `data/objects/buildings/<sid>.prop` stores its collision mask
      in `collisionmaskproperty.Mask`.

[^3]: Collision-mask cell size — `lib/unit.script:8712`:
    ```pascal
    cellSize := 0.5;
    ```
[^4]: The mask `ScaleFactor` is 1 —
      `data/objects/buildings/refbuilding.prop:45`.

[^5]: Durability restored during repairs —
      `units/unit.inc/onaclanimationreachedconstruct.inc:40-41`:
    ```pascal
    if (arg_obj.orders[0].itype = gc_obj_order_type_repair) then
       TObj(pobj).hp := Min(TObj(pobj).hp + gc_gameplay_repairhp, TObjBase(pobjbase).maxhp);
    ```
[^6]: `gc_gameplay_repairhp = 20` — `dmscript.global:211`.

[^7]: Construction progress per hammer strike —
      `units/unit.inc/onaclanimationreachedconstruct.inc:25-37`:
    ```pascal
    delta := (gc_buildtime_progressperhit / TObjBase(pobjbase).buildtime)
    buildprogress += delta
    deltahp := round(maxhp * delta)
    hp += deltahp   // capped at maxhp
    ```
[^8]: `gc_MaxBuilderCount = 30` — `dmscript.global:159`.

[^9]: `gc_BuilderDist = 1.0` — `dmscript.global:160`.

[^10]: `_unit_CalcBuilderPoints` — `lib/unit.script:8702-9006`.

[^11]: `_unit_OrderBuild` — `lib/unit.script:9285-9378`.

[^12]: `gc_MaxWallBuilderPointsCount = 16` — `dmscript.global:137`.

[^13]: Ferry capacity — `lib/unit.script:2043`
       (`transport = 80 + 40 = 120`).

[^14]: Basic European Tower — `lib/unit.script:2223-2240`:
    ```pascal
    SetObjBaseWeapon(objprop, objbase, 0, 1000, 400, 550, 1500, 550, 50000, gc_obj_weapon_kind_cannonball, True);
    ```
[^15]: `SetObjBaseWeapon` signature — `lib/unit.script:520`.

[^16]: Tower `consume.gold = 500/tick` — `lib/unit.script:2235`.

[^17]: Russia Tower variant — `lib/unit.script:2241-2247`
       (`commonrus` branch).

[^18]: Conditions for leaving `default = -1` unchanged in
       `SetObjBaseWeapon` — `lib/unit.script:523-538`
       (`if (damage<>-1)`, and similar checks).

[^19]: Turkey Tower variant — `lib/unit.script:2248-2256`
       (`commontur` branch).

[^20]: Special handling for `gc_obj_usage_tower` — `lib/unit.script:178`.

[^21]: Capture mechanic — `lib/miscext.script:1018-1030`.

[^22]: `gc_gameplay_captureradius = 214/53.33 = 4.0` —
       `dmscript.global:208` (see also `lib/miscext.script:1018`).

[^23]: Capture score multiplier — `lib/unit.script:3837-3841`.

[^24]: `_unit_CancelUnitProduction` — `lib/unit.script:5891-5977`.

[^25]: `_misc_GUICancelBuilding` — `lib/miscext2.script:3898-3953`.

[^27]: Building destruction state machine —
       `data/scripts/units/building.inc/settagstates.inc:32-53`.

[^28]: `DeathStage1` —
       `data/scripts/units/building.inc/deathstage1.inc:5-11`.
       `DeathStage2` is defined in `deathstage2.inc`.

[^29]: Applying the `debris` material to a destroyed building —
       `data/scripts/units/building.inc/ontagstates.inc:286`.

[^30]: `DeathStage2`, which releases the footprint and removes the object —
       `data/scripts/units/building.inc/deathstage2.inc:8-15`.

[^31]: `_unit_DestroyObj` — `lib/miscext2.script:4232-4242`.

[^32]: `_unit_DoUnitsGoOutside` — `lib/unit.script:4559-4564`.

[^33]: Building `OnDeath` handler —
       `data/scripts/units/building.inc/ondeath.inc:11-25`.

[^34]: `_unit_ProduceUnit` — `lib/unit.script:10351`.

[^35]: `_unit_CancelUpgradePerform` — `lib/unit.script:5837-5889`.
