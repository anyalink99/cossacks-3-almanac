<a id="recon-pathfinding-и-движение-юнитов"></a>
<a id="поиск-пути-и-движение-юнитов"></a>
# Pathfinding and Unit Movement

[← How the game works](../../README.md)

This article explains how Cossacks 3 units find routes, avoid one another
and buildings, and react when blocked. **The key point:** the pathfinding
algorithm itself lives in the native C++ engine. Scripts only queue units,
submit destinations, and read the resulting routes. Script references and
Pascal excerpts are collected in [Sources](#sources).

**Related documents:**

- [ticks_and_subticks.md](../../../../internals_en/engine/ticks_and_subticks.md) - main progress-loop
  (`gc_progress_Interval = 0.02 s`), unit-tick = 100 ms.
- [server_sync_architecture.md](../../../../internals_en/engine/server_sync_architecture.md) —
  `WriteMove` / `ReadMove`, server-authoritative model, serialization
  queue in save.
- [building_mechanics.md](../economy/building_mechanics.md) – footprint and `CIMass`
  near buildings (massive “anchors” for collisions).

<a id="коротко"></a>
## TL;DR

- Unit movement is **two independent subsystems**: global
  `pathfinding` (search for path A → B via `QuadTree` obstacle map) and
  local collision/push (`CollisionInertia`). Both live in
  native engine; in scripts - only requests to them.
- `Pathfinding` **batch** once every 20 ms (`progress`-tick): the engine takes all
  a queue of units waiting for a route, and considers the paths to be one pass.
  Local collision - every frame.
- The size of the collision cell is `0.5` tile (`gc_BuilderDist = 1.0` for
  placement of construction workers around the building).
- **Friendly pushing** is silent: allied units push one another apart
  without triggering an animation.
- **An enemy in the forward 90° sector** makes a unit switch to attack,
  even when it was moving toward another destination.
- A **formation** gives each unit its own destination with a small random
  offset; units do not follow a single squad leader. This is why a moving
  formation spreads slightly.

<a id="1-архитектура-две-независимые-подсистемы"></a>
## 1. Architecture: two independent subsystems

The engine divides unit navigation into two loosely coupled subsystems:

| Subsystem | Purpose | Implementation |
|---|---|---|
| **Topology and obstacle map** (`Topology`, `QuadTree`) | Global A → B routing through traversable zones; returns an array of route points (`TrackPoint`). | Native functions `Topology*` / `TraceLine*`. |
| **Collision avoidance** (`CollisionInertia`, CI) | Per-frame avoidance and pushing along an existing route, with mass and inertia. | Native functions `*CI*`. |

Scripts access both via `Set / Get*ByHandle` - **details
implementations in native code are not visible to scripts**.

Entry point to scripts: `_init_InitializeTopology` [^1]. Inside are set
key topology constants: `gc_top_TopologyPriority = 90`,
`gc_top_PathPriority = 70`, `gc_top_WallPriority = 95`,
`gc_top_EffectDist = 3` and others [^2]

This is a **`QuadTree`-based collision world** with two priority layers.
The first includes all static obstacles; the second includes only terrain
and walls. Requests that allow a unit to leave a building use the lower
priority layer so that a route can be found as if the building were absent.

---

<a id="2-pathfinding-где-и-как"></a>
<a id="2-где-и-как-рассчитывается-путь"></a>
## 2. Where and How Routes Are Calculated

<a id="21-очередь-и-батчевание"></a>
<a id="21-очередь-и-пакетная-обработка"></a>
### 2.1 Queue and batching

**Queue:** two global lists in `_unit_PathListAdd` [^3]. Unit
added to `gGOPathList` (earth) or `gWaterPathList` (water) **exactly
once** when transitioning to state `gc_statetag_execute_move` [^4].
The `bpathrequested : Boolean` flag protects against duplication of [^5].

**Lists are serialized** in save/replay [^6] is part of the world state.

<a id="22-главный-батч-раз-в-progress-tick--20ms"></a>
<a id="22-главный-пакет-запросов-раз-в-20-мс"></a>
### 2.2 Main batch (once every 20 ms)

The entire batch of `pathfinding` is in `progress/progress.inc/nothing.inc` [^7].
Key steps:

1. One queue is selected - `gWaterPathList` or `gGOPathList` -
with a 2:1 priority in favor of land (water is processed only when the
   land queue is empty or `progresstick mod 2 == 0`).
2. For each unit in the queue, call
   `TopologyAddPathGameObjectByHandle`, and the unit is assigned
   a numeric squad tag for land units, or `-1` for water units.
3. One batch call—`TopologyGetPath` (land) or `TopologyGetPathExt`
   (water) - calculates paths for the entire queue at once.
4. For each unit, the script checks `noPath`, sets the current route-point
   indices, and finally clears the queue.

**What is important:**

1. **One batch per progress-tick.** `progresstick` is incremented every
   20 ms (`gc_progress_Interval = 0.02`). In one tick, **one** is solved
   turn - water or land - never both.
2. **Land queue is priority (2:1).** Water queue is processed
   only if the earth one is empty OR `progresstick mod 2 == 0`.
3. **The entire list is considered a single call** `TopologyGetPath` /
   `TopologyGetPathExt`. This is a **batch request to native code**: kernel
   gets an array of units with their (start, end), performs path-search for
   each, fills out TrackPoints. Algorithm inside - **not visible from
   scripts**.
4. **`squad` is passed as a numeric tag** before the request. The engine
   may use it to coordinate routes for units in one squad or to share a
   movement-cost map. Confirming this without decompilation is impossible.
5. **`noPath` is determined by `TrackPointCount == 0`**: when the engine
   finds no route, the route-point array is empty.
6. After the batch, the script inserts building exit points (for leaving a
   barracks or transport) and resets `bpathrequested`.

<a id="23-что-делает-topologygetpath-наблюдаемо"></a>
### 2.3 What `TopologyGetPath` does (observable)

From the usage context and class name:

- **`QuadTree`** - spatial index of obstacles, divides the world into
  cells.
- **Topology** is a superstructure graph of **zones**
  (`TopologyGetZoneIndex(x, z)`); set `_unit_TopologyAdd` /
  `_unit_TopologyRemove` / `_unit_TopologyProgress` [^8] supports
  “what zone is this unit currently in” for a quick distance-check.
- **`TopologyGetPathDistance(x1,z1,x2,z2,bIncludeBuildings)`** [^9] —
  a synchronous function that returns the path length along a topological graph.
  Used AI, not motion.
- **`TopologyGetPathToZone(zoneInd)`** [^10] - request “route to zone”,
  AI war-logic.

**Layer Hypothesis:**

- High level - A* according to the zone graph (nodes - `TTopZone`, edges -
  connections via `gc_top_EffectDist=3`).
- Low level - inside the grid- or quadtree-collision-test zone to
  insert TrackPoints between nodes.

This is compatible with the constant `TopologySetPosSearchRadius(7)` (how far
look for the “nearest passable point”).

**Grid:** `gc_collision_size = 0.5` [^11] is the size
base-collision-cell **in tiles** (i.e. 1 “collision cell” =
0.5 tiles ≈ 26 pixels). Also `gc_MaxColMapWidth = 2*gc_MaxMapWidth`
confirms: the collision map is 2 times smaller than the map (640 → 1280
cells/side).

> **Algorithm not visible**: calls `TopologyGetPath` / `TopologyGetPathExt`
> lead to native code. It is impossible to determine from the scripts whether it is A*,
> flow-field, wave-propagation or something else. Documented
> indirect signs: batch processing of the list of units, transfer of squad-id
> as a hint, the presence of a separate zone structure + `QuadTree`, raycast function
> `TraceLineQuadTree` (which means there are LoS-checks inside path-search).

---

<a id="3-trackpointы--выход-pathfindingа"></a>
<a id="3-маршрутные-точки"></a>
## 3. Route Points

After `TopologyGetPath`, each unit receives an array of **route points**
(`TrackPoint`) that the engine reads every frame to interpolate movement:
- `GameObjectTrackPointAddByHandle(hnd, x, y, z)` - append.
- `GameObjectTrackPointInsertByHandle(hnd, ind, x, y, z)` – insert
  (used to insert the exit-point of the building **at the beginning**).
- `SetGameObjectTrackPointCurrentPointIndexByHandle(hnd, idx)` — set
  current.
- `GetGameObjectTrackPointCountByHandle(hnd)` — list length.
- `SetGameObjectTrackPointSkipPointsByHandle(hnd, true)` - allow
  skip intermediate points (if there is visibility until the next one).
- `SetGameObjectTrackPointSkipQuadTree(quadTree)` / `SkipFactor(1)` /
  `SkipEpsilon(0.1)` [^12] — path smoothing parameters.

Each unit object initializes skip-quadtree by selecting: for
`gc_obj_media_land` is taken from `TopologyGetPathQuadTree` (path-mode), for
`gc_obj_media_water` — `TopologyGetTopologyQuadTree` (full-mode) [^12].

When reaching the end of the path, `OnEndPointReached` [^13] is triggered -
switching to `move_idle`, deleting the order.

When completing a turn, `OnDirectionReached` [^14] is triggered.

---

<a id="4-предотвращение-столкновений-collisioninertia-ci"></a>
## 4. Collision Avoidance (`CollisionInertia`, CI)

This is the main mechanism that makes units **avoid one another**:
local physical pushing with mass and inertia, applied on top of an
already calculated route.

<a id="41-параметры-отдельного-юнита"></a>
### 4.1 Per-unit parameters

CI parameters are set in `SetCustomCollisionInertia` [^15]: `CIMass`,
`CIIntersectRadius`, `CIDeltaStep`, `CIRotationSpeed`, `CIStuckAngle`,
`CIEpsilonAngle`, `CIEpsilonShift`, `CIEpsilonMove`,
`CIDistExtPointEpsilon`, `CIMaxCollideCounter`, `CIMaxProcessObject`.

Constants:

- `gc_collision_radius_default = 0.16` [^16].
- `gc_collision_radius_stand = 0.1`.
- `gc_collision_radius_attack = 0.1`.

Behavioral radii (uses `WriteMove` for variance):

- `gc_obj_radius_default = 10`, `gc_obj_radius_horse = 15`.
- `gc_obj_radius_formation_default = 8`, `gc_obj_radius_formation_horse = 12`.

**Conclusion:** intersect-radius for a foot unit is ≈ 0.16 tiles - very
small, units can stand tightly together. Horses receive `unitradius=15`
(display-radius).

<a id="42-корабли-получают-огромную-ci"></a>
<a id="42-корабли-получают-большую-инерцию-столкновений"></a>
### 4.2 Ships receive much greater mass and radius

Ships call `SetCustomCollisionInertia` with large multipliers [^17].
The Ferry (`ferry`) and Ship of the Line (`battleship`) use
`radius × 11, mass × 32`; the Frigate (`frigate`) and Xebec (`xebec`)
use `9, 16`; the Galley (`galley`) uses `7, 12`; the Chaika (`chaika`)
and both Yacht variants (`yacht`, `yachttur`) use `6, 8`; and the
Boat (`fishboat`) uses `3, 1`.

This explains why ships **push** one another yet barely move under
pressure from infantry: their mass can be 32 instead of 1.

<a id="43-здания--неподвижные-тяжёлые-блокеры"></a>
<a id="43-здания--тяжёлые-неподвижные-препятствия"></a>
### 4.3 Buildings are heavy, immovable obstacles

Buildings are initialized with `CollisionInertia=true`,
`CIIntersectRadius=0.35` tile, `CIMovable=false`, `CIMass=10000`,
`CIStuckAngle=5` (for units - 0), `CIAvoidPointMaxAngle=120`,
`CIMaxCollideCounter=7` [^18].

**Conclusion:** buildings are massive immovable obstacles with a radius
of 0.35 (plus a separate footprint mask on the cell grid; see
[building_mechanics.md](../economy/building_mechanics.md)). Pathfinding
calculates the global route around them; local collision avoidance only
keeps a unit from pressing directly into a wall.

<a id="44-push-mechanic-между-юнитами-правило-передний--90-fov"></a>
<a id="44-расталкивание-юнитов-и-передний-сектор-в-90"></a>
### 4.4 Unit pushing and the forward 90° sector

Collision rules distinguish allies (`Fr`), enemies (`En`), and neutral
objects (`Nl`) through `SetGameObjectMyRuleCollidedExec*` [^19]:

- `Fr` (friendly): event **not** generated. CI is still physical
  pushes, but the script does not interfere.
- `En` (enemy): event is generated **only if the enemy is in front 90°**
  (`_misc_Collided`). This explains why the unit starts attacking the enemy
  “face to face”, but not if you hit me from behind.
- `Nl` (neutral): like friendly - without event.
The `_misc_Collided` [^20] handler itself checks that both objects are
`gc_obj_material_body`, and when hit, tries to attack through
`_unit_TryAttack`; if the target is out of range and the unit does not run away -
switches the current order to attack.

**Push mechanics summary:**

1. **Ally → ally:** only CI physics (`mass` / `intersect` /
   `inertia`), without events. Units “stick together” and smoothly push apart -
   the front one pushes the rear one in the direction of movement.
2. **Enemy → enemy (90° front):** called by `_misc_Collided`, which
   automatically initiates an attack.
3. **Unit → building / building → unit:** building `bMovable=False` +
   `mass=10000` - push-physics does not move the building, the unit flows around.
4. **Projectiles and pedestrian markers:**
   `SetGameObjectMyCollisionDetection(False)` - ignore CI.

---

<a id="5-обработка-застревания"></a>
## 5. Handling Stuck Units

<a id="51-проверка-каждый-кадр-нет-пути--остановиться"></a>
### 5.1 Per-frame check: “no route means stop”

In `pathfinding`'s batch [^21] after calling `TopologyGetPath` for each
unit is calculated by `noPath` through `TrackPointCount = 0`. If TrackPoints
yes - `current-point` indices and motion animation are set.
If no points exist and the unit was in `gc_statetag_move_walk`,
`_unit_Stop` is called.

**If the path is not found** - the unit **simply stops**, without timeout
and retry. The Order remains (if `bRemove=False`), and the unit will “try again”
at the next transition to `execute_move`.

<a id="52-сжатая-толпа--findbestposition"></a>
### 5.2 Compressed crowd - `FindBestPosition`

`FindBestPosition` [^22] is called from `nothing.inc` when the unit is idle and
`standtime > 1` - trying to get out of the dense crowd. Conditions: number of neighbors
according to conflict there are more `maxdensity = 3`, and of them they cost at least the same
`standtime >= 3 s`. Then - **spiral search** within a radius of 6 idle-grid-
cells around the current position, and order to move to a free cell.
Not every tick-period is triggered
`gc_unit_TimeFindBestPosition = 0.1*31 - 0.025 ≈ 3.075 s` controlled
via `lasttimebestposition`.

<a id="53-топология-обновляется-по-таймеру"></a>
### 5.3 Topology is updated by timer

In `unit.inc/nothing.inc` `_unit_TopologyProgress` is periodically called
at intervals `gc_unit_TimeTopology = 0.1*50 - 0.025 ≈ 4.975 s` [^23].
This is **not a repath**, but a re-evaluation of “what topo-zone am I in” (for AI
distance-queries).

<a id="54-аварийное-исправление-зависания"></a>
### 5.4 Hard “hang fix”

`unit.inc/nothing.inc` has a watchdog for invisible units in the state
“I’m born, but I don’t see myself” (left the barracks, but didn’t show up) [^24]:
after 1 s `standtime` is forced to be entered
`gc_statetag_essential_none`. This is not an ordinary stuck, but glitch protection
transport / leave-building.

<a id="55-loader-pass-на-старте-два-юнита-в-одной-точке"></a>
<a id="55-проверка-при-загрузке-два-юнита-в-одной-точке"></a>
### 5.5 Loader-pass at the start: “two units at one point”

When generating a map, it is called
`_misc_FixCollisionInertiaObjectsInOnePoint` [^25]: in three passes
**destroyed** environment objects superimposed at one point -
otherwise path-trace would loop. Runs from
`common.inc/dogenerate.inc:2070`.

<a id="56-чего-не-найдено"></a>
### 5.6 What was NOT found

- **No timeout per path.** The unit can hang “indefinitely” from
  `bpathrequested=True`, then get an empty path and stop.
- **No teleport when stuck.** Watchdog `essential_none` (§5.4) not
  teleports, but only resets the flag.
- **No cap on queue length** `gGOPathList`. The script code is not
  limits; everything in the queue is considered one batch.

---

<a id="6-formation-movement-каждый-юнит-идёт-сам"></a>
<a id="6-движение-построения-каждый-юнит-идёт-сам"></a>
## 6. Formation Movement: Each Unit Moves Independently

The key point is that a **formation does not move as one object**.
There is no single squad leader to follow: **each unit receives its own
destination**.

<a id="61-writemove--рассыпать-squad-на-per-unit-ордера"></a>
<a id="61-writemove--выдать-каждому-юниту-отдельный-приказ"></a>
### 6.1 `WriteMove` issues a separate order to each unit

`WriteMove` [^26] walks the formation grid and for each unit:

1. Calculates the target cell of the formation in world coordinates.
2. Adds a small random offset within
   `unitradius * 1.1` through the turn to `random*360`.
3. Calls `_unit_OrderMove(gohnd, x_personal, y_personal, ...)` -
   personal order for your cell with jitter.

Then the unit goes **independently**, through the standard chain
`_unit_PathListAdd` → `TopologyGetPath`. None
“leader-leads-the-rest” is not.

`gPathTag` (rolling 1..255) is written as `info.amount` - **does not apply to
`pathfinding`**, this is an order-cookie for server↔client sync.

<a id="62-грид-формации"></a>
<a id="62-сетка-построения"></a>
### 6.2 Formation grid

`_squad_FullRebuildGrid` [^27] holds per-squad `arGrid[i,j]` - which unit
in which cell of the formation. When changing lanes (turn, attack-mode, etc.)
re-sorts by direction.

Constants [^28]: `gc_formation_maxcount = 160` (max units in squad),
`gc_formation_maskmaxwidth = 54`, `gc_formation_maskmaxheight = 24`.

<a id="63-fmovecount--простой-счётчик"></a>
### 6.3 `fMoveCount` - simple counter

`_player_CalcSquadsMoveCount` [^29] simply recalculates for each squad
number of units in `gc_statetag_move_walk` state. Runs with period
`gc_global_TimeCalcSquadsMoveCount = 0.03*10 = 0.3 s`. Only used
squad-aggressive logic and hold-mode check [^30]. To `pathfinding`'u
has no relation.

<a id="64-squad-id-как-hint-для-kernel"></a>
<a id="64-номер-отряда-как-подсказка-движку"></a>
### 6.4 Squad ID as a hint to the engine

Remember from §2.2: before `TopologyGetPath`, each unit receives
`SetGameObjectTagFloatByHandle(goHnd, TObj(pObj).squad)`. What kernel with
does this - **not visible from the scripts**. Hypothesis: consistent routing
for one unit (units do not cross paths with each other in chess
okay). But this is **not confirmed**; need decompilation or
empirical test with two squads in a narrow passage.

<a id="65-orphan-константа"></a>
<a id="65-неиспользуемая-константа"></a>
### 6.5 Unused constant

`gc_player_SquadMoveTick = 10` [^31] - **defined, but not found anywhere
used** (Grep for all `.script` files only gives a definition).
Possibly reserved for squad-level repath, but not
implemented.

---

<a id="7-когда-путь-рассчитывается-заново"></a>
## 7. When Routes Are Recalculated

| When a unit requests a new path | Why |
|---|---|
| Go to `gc_statetag_execute_move` | `_unit_PathListAdd` is explicitly called from `ontagstates.inc` |
| Resetting or changing the order - `_unit_ClearOrders` → new `_unit_OrderMove` | `_unit_OrderMove` creates a new Order of type `gc_obj_order_type_move`, which places `bDoPosition := True` in `_misc_DoProgressOrders` [^32] → `gc_statetag_execute_move` → `_unit_PathListAdd` |
| The compressed crowd - `FindBestPosition` found a free cell | See §5.2 - once every 3.075 s maximum |

**Scenarios in which repath does NOT work** (confirmed by `Grep` by
`unit.inc` and `miscext.script`):

- **Periodic repath while moving towards the goal.** Not implemented - not
  There was no timer, no call. If the target moves, a new order is placed
  The attack itself is logic.
- **Repath when colliding with an enemy.** `_misc_Collided` does not cause repath,
  and `_unit_TryAttack` / `_unit_OrderAttack`. The attack itself will already give a new
  move-order if needed.
- **Repath when a new obstacle appears on the path.** Not found. If
  the building was placed directly on the route of the moving unit, it would run into
  `OnEndPointReached` and through `_unit_RemoveOrder` [^33] will stop.
  Further behavior depends on the order type: `move` without `bRemove` will be included
  to `move_walk` again and will give a new `PathListAdd`.

---

<a id="8-производительность-и-лимиты"></a>
## 8. Performance and limits

<a id="81-лимиты-в-скриптах"></a>
### 8.1 Limits in scripts

- **The pathfinding queue has no script-side limit.** Every unit added
  to `gGOPathList` during a 20 ms tick is processed in the next
  `TopologyGetPath` call.
- **Route-point smoothing:** `SkipFactor=1`, `SkipEpsilon=0.1`, and
  `SkipPoints=true` [^12] let a unit skip intermediate points when
  there is a clear line of sight ahead.
- **Per-unit collision budget** [^15]:
  - `MaxCollideCounter = 7*3 = 21` (collisions processed per tick);
  - `MaxProcessObject = 4*3 = 12` (number of objects in the vicinity,
    processed by CI).

<a id="82-профайлер-встроен"></a>
### 8.2 Profiler built-in

The script wraps `TopologyGetPath` in calls
`_misc_ProfilerBegin('progress.GetPath')` and `_misc_ProfilerEnd` [^34].
There is no profiler data in the scripts, but the engine can measure the cost.

<a id="83-глобальный-progress-cap"></a>
<a id="83-глобальное-ограничение-цикла-расчёта"></a>
### 8.3 Global progress-cap

In `progress.inc` [^35] for misc/pool players there is a dynamic `secmax`
(adaptive processing slicing): with `count > 700` the step increases as
`count div 20`, with `count < 2000` - `count div 15`, otherwise -
`count div 10`. For `gGOPathList` itself **there is no such thing**, queue
processed completely.

---

<a id="9-открытые-вопросы-для-эмпирических-замеров"></a>
<a id="9-что-ещё-требует-проверки"></a>
## 9. Questions Requiring Further Testing

1. **Pathfinding algorithm:** A*, a flow field, or a wave search? This
   requires decompiling native `TopologyGetPath` or testing several
   equally long routes. The working hypothesis is A* with a Euclidean
   heuristic.
2. **Effect of the numeric squad tag:** does the engine actually use it
   to coordinate group routes? Move two squads through a one-tile
   passage and compare their paths.
3. **Simultaneous-request limit:** how many units can begin moving
   without a frame-rate drop—200, 500, or 1,000? Scripts impose no
   limit; the native engine may do so internally.
4. **A new obstacle:** place a building directly on a squad's route.
   Does the engine recalculate the path or do the units stop?
5. **`CIStuckAngle = 0` for units and `= 5` for buildings:** what is the
   visible effect? The value may relate to rotation snapping.
6. **Ships and the dummy Frigate:** is `bIsShipDummy` [^36] a separate
   collision object, and does it affect pathfinding?
7. **Building footprint versus collision radius:** with a 0.5-tile cell
   and `CIIntersectRadius=0.35`, the collision radius is smaller than the
   blocking grid. Test whether units catch on building corners.

---

<a id="10-резюме"></a>
## 10. Summary

- **The pathfinding algorithm lives in the native engine.** Scripts add
  units to `gGOPathList` or `gWaterPathList`, call
  `TopologyGetPath` / `TopologyGetPathExt` every 20 ms, and interpret
  the returned route points. `QuadTree`, the `TTopZone` graph, and
  `TraceLineQuadTree` provide indirect clues, but the exact algorithm
  is not visible.
- **`CollisionInertia` (CI) handles local avoidance.** Each unit has a
  mass and radius. Buildings use `mass=10000, movable=False`, while
  ships receive much larger values. Allies push silently; an enemy in
  the forward 90° sector can trigger an automatic attack.
- **Stuck-unit recovery is minimal.** A unit stops when no route is
  found; there is no timeout or teleport. `FindBestPosition` searches
  nearby cells when a stationary crowd becomes too dense.
- **A formation has no common leader path.** `WriteMove` gives every
  unit an individual `_unit_OrderMove(personal_x, personal_y)` target
  with a small random offset. The squad ID is passed to the engine as a
  numeric tag, but its effect is unknown.
- **Routes are recalculated only after an order change or a new movement
  command.** No periodic recalculation was found.
- **Scripts do not cap the queue.** If 500 units begin moving together,
  all 500 are submitted in one `TopologyGetPath` call. `_misc_Profiler`
  measures the cost, but scripts do not use it to throttle work.

**The route algorithm itself remains hidden in native code.** Further
investigation requires decompiling the Cossacks 3 executable or running
targeted experiments (see §9).

---

<a id="источники"></a>
## Sources

All paths are relative to `data/scripts/` in a Cossacks 3 installation.

[^1]: `_init_InitializeTopology` — `lib/init.script:85-93`:
    ```pascal
    procedure _init_InitializeTopology();
    begin
       TopologyCreate;
       TopologySetTopologyPriority(gc_top_TopologyPriority);  // = 90
       TopologySetPathPriority(gc_top_PathPriority);          // = 70
       TopologySetPosSearchRadius(7);
       TopologySetBufferSize(SizeOf(TTopZone));
       TopologySetConnectionRadius(gc_top_EffectDist);        // = 3
    end;
    ```
[^2]: Topology constants - `dmscript.global:140-153`:
    ```pascal
    gc_top_TopologyPriority = 90;   // QuadTree priority for blockers (buildings, terrain)
    gc_top_PathPriority     = 70;   // QuadTree priority for path search (without buildings, or fewer)
    gc_top_WallPriority     = 95;   // dedicated wall priority
    gc_top_WallQuadTree     = 2;
    gc_top_UnitTick         = 50;   // used in gc_unit_TimeTopology
    gc_top_GlobalTick       = 100;
    gc_top_EffectDist       = 3;
    gc_top_MaxUpdateAreas   = 500;
    ```

[^3]: `_unit_PathListAdd` — `lib/unit.script:3324-3363`:
    ```pascal
    procedure _unit_PathListAdd(const goHnd : Integer);
    begin
       var pobj : Pointer = _unit_GetTObj(goHnd);
       if (pobj<>nil) then
       begin
          if (not TObj(pobj).bpathrequested) then
          begin
             if _unit_IsWaterUnit(goHnd) then
             gWaterPathList.Add(goHnd)
             else
             gGOPathList.Add(goHnd);
             TObj(pobj).bpathrequested := True;
          end;
       end;
    end;
    ```
[^4]: Call from `units/unit.inc/ontagstates.inc:692`:
    ```pascal
    if (switchExecute=gc_statetag_execute_move) then
    begin
       ...
       _unit_PathListAdd(myHnd);
       ...
    end
    ```
[^5]: Flag `bpathrequested : Boolean` - `dmscript.global:1747`.

[^6]: Serialization of lists `gGOPathList` and `gWaterPathList` -
    `dmscript.source:340-341`.

[^7]: Main batch of `pathfinding` - `progress/progress.inc/nothing.inc:115-323`:
    ```pascal
    117: if (gWaterPathList.GetCount>0) and ((gGOPathList.GetCount=0) or (gProgress.progresstick mod 2=0)) then
    118:    pList := gWaterPathList; landPath := false;
    123: else
    124:    pList := gGOPathList; landPath := true;
    128:
    129: var count : Integer = TIntegerList(pList).GetCount;
    130: if (count>0) then begin
    131:    TopologyClearPathGameObjects;
    132:    for i := 0 to count-1 do begin
    135:       var goHnd : Integer = TIntegerList(pList).Get(i);
    144:       TopologyAddPathGameObjectByHandle(goHnd);
    149:       if TObjProp(pObjProp).media = gc_obj_media_land then
    150:          SetGameObjectTagFloatByHandle(goHnd, TObj(pObj).squad)   // squad id for group cost
    151:       else
    152:          SetGameObjectTagFloatByHandle(goHnd, -1);
    153:    end;
    155:    _misc_ProfilerBegin('progress.GetPath');
    157:    if landPath then
    158:       TopologyGetPath
    159:    else begin
    161:       var quadTree : Integer = TopologyGetTopologyQuadTree;
    162:       TopologyGetPathExt(quadTree, gc_collisiontag_water, gc_TestPriorityOption_Water);
    163:    end;
    165:    _misc_ProfilerEnd('progress.GetPath');
    167:    for i:=0 to count-1 do begin
    169:       var goHnd : Integer = TIntegerList(pList).Get(i);
    171:       var noPath : Boolean = (GetGameObjectTrackPointCountByHandle(goHnd) = 0);
    177:       TObj(pobj).bpathrequested := False;
           ...     // insert building exit points, turn transport ramps away, etc.
    307:       DoSetupMoveAnimation(goHnd);
    308:       SetGameObjectTrackPointCurrentPointIndexByHandle(goHnd, 0);
    309:       SetGameObjectTrackPointCurrentPointIndexByHandle(goHnd, 1);
           ...
    322:    TIntegerList(pList).Clear;
    323: end;
    ```
[^8]: Unit topo-zone support - `lib/unit.script:3248-3287, 6957-6977`
    (`_unit_TopologyAdd`, `_unit_TopologyRemove`, `_unit_TopologyProgress`).

[^9]: `TopologyGetPathDistance` - `lib/unit.script:6142, 6150`.

[^10]: `TopologyGetPathToZone` - `lib/misc.script:3231, 3255, 5241` and
    `progresswarai.inc`.

[^11]: `gc_collision_size = 0.5`, `gc_MaxColMapWidth = 2*gc_MaxMapWidth` —
    `dmscript.global:178`.

[^12]: TrackPoint smoothing parameters - `units/unit.inc/initial.inc:280-287`:
    ```pascal
    gc_obj_media_land  : quadTree := TopologyGetPathQuadTree;     // 70 (path mode, without buildings?)
    gc_obj_media_water : quadTree := TopologyGetTopologyQuadTree; // 90 (full-mode)
    ```

[^13]: `OnEndPointReached` — `units/unit.inc/onendpointreached.inc`.

[^14]: `OnDirectionReached` — `units/unit.inc/ondirectionreached.inc`.

[^15]: Per-unit init CI — `units/unit.inc/initial.inc:21-56`:
    ```pascal
    procedure SetCustomCollisionInertia(hnd : Integer; IntersectRadiusFactor, MassFactor, DeltaStepFactor : Float; bMovable : Boolean);
    begin
       SetGameObjectCollisionInertiaByHandle(hnd, IntersectRadiusFactor>0);
       if (IntersectRadiusFactor<=0) then exit;
       SetGameObjectCIAvoidPointMaxAngleByHandle(hnd, 180);
       SetGameObjectCIMassByHandle(hnd, 1*massFactor);
       SetGameObjectCIIntersectRadiusByHandle(hnd, gc_collision_radius_default*IntersectRadiusFactor);
       SetGameObjectCIMaxDistKoefByHandle(hnd, 2);
       SetGameObjectCIDeltaStepByHandle(hnd, 0.005/DeltaStepFactor);
       SetGameObjectCIRotationSpeedByHandle(hnd, 5);
       SetGameObjectCIStuckAngleByHandle(hnd, 0); // 0.5 in rw2to
       SetGameObjectCIEpsilonAngleByHandle(hnd, 4);
       SetGameObjectCIEpsilonShiftByHandle(hnd, 0.001);
       SetGameObjectCIEpsilonMoveByHandle(hnd, 0.02);
       SetGameObjectCIDistExtPointEpsilonByHandle(hnd, 0.005);
       SetGameObjectCIMovableByHandle(hnd, bMovable);
       SetGameObjectCIBuildExtPointsByHandle(hnd, True);
       SetGameObjectCIMaxCollideCounterByHandle(hnd, 7*3);
       SetGameObjectCIMaxProcessObjectByHandle(hnd, 4*3);
       ...
    end;
    ```
[^16]: Collision radius constants - `dmscript.global:972`
    (`gc_collision_radius_default = 0.16`, `gc_collision_radius_stand = 0.1`,
    `gc_collision_radius_attack = 0.1`).

[^17]: CI parameters of ships - `units/unit.inc/initial.inc`:
    ```pascal
    'ferry'              : SetCustomCollisionInertia(myHnd, 11, 32, 0.1, ...);   // radius x11, mass x32
    'battleship'         : ...                                                    11, 32
    'frigate', 'xebec'   : ...                                                     9, 16
    'galley'             : ...                                                     7, 12
    'chaika'             : ...                                                     6,  8
    'yacht', 'yachttur'  : ...                                                     6,  8
    'fishboat'           : ...                                                     3,  1
    ```
[^18]: CI parameters of buildings - `units/building.inc/initial.inc:59-72`:
    ```pascal
    SetGameObjectCollisionInertiaByHandle(colHnd, true);   // CI enabled
    SetGameObjectCIIntersectRadiusByHandle(colHnd, 0.35);  // 0.35 tiles
    SetGameObjectCIMovableByHandle(colHnd, false);         // immovable
    SetGameObjectCIMassByHandle(colHnd, 10000);            // 10000 — effectively infinite
    SetGameObjectCIMaxDistKoefByHandle(colHnd, 2);
    SetGameObjectCIDeltaStepByHandle(colHnd, 0.005);
    SetGameObjectCIRotationSpeedByHandle(colHnd, 5);
    SetGameObjectCIStuckAngleByHandle(colHnd, 5);          // buildings → 5°, units → 0
    SetGameObjectCIEpsilonAngleByHandle(colHnd, 4);
    SetGameObjectCIEpsilonShiftByHandle(colHnd, 0.001);
    SetGameObjectCIEpsilonMoveByHandle(colHnd, 0.02);
    SetGameObjectCIDistExtPointEpsilonByHandle(colHnd, 0.005);
    SetGameObjectCIAvoidPointMaxAngleByHandle(colHnd, 120);
    SetGameObjectCIMaxCollideCounterByHandle(colHnd, 7);
    ```
[^19]: Friendly/Enemy/Neutral push rules - `units/unit.inc/initial.inc:303-318`:
    ```pascal
    SetGameObjectMyCollisionExecAsFunc(true);
    SetGameObjectMyRuleCollidedExecFr(4, 35.0, False);   // friendly:  flags=4, fov=35° → no collide event
    SetGameObjectMyRuleCollidedExecEn(2, 90.0, False);   // enemy:     flags=2, fov=90° → fire event
    SetGameObjectMyRuleCollidedExecNl(4, 35.0, False);   // neutral:   flags=4, fov=35° → no collide event
    if gbool_use_collision then SetGameObjectMyCollidedStateName('_misc_Collided');
    ```

[^20]: `_misc_Collided` — `lib/miscext.script:1235-1289`:
    ```pascal
    procedure _misc_Collided(const hnd: Integer);
    begin
       if (_net_IsOffline or _net_IsServer) and not _net_IsReplay
           and (GetGameObjectPlayableObjectByHandle(hnd)) then begin
          var trg: integer = GetGameObjectStateCollisionObjectByHandle(hnd);
          ...
          if (gObjProp[TObj(pobj).cid][TObj(pobj).id].material = gc_obj_material_body)
             and (gObjProp[TObj(pobj2).cid][TObj(pobj2).id].material = gc_obj_material_body) then
          begin
             if (GetGameObjectTrackPointMovementModeIntByHandle(hnd) <> 0) then
             begin
                var res : Integer = _unit_TryAttack(hnd, trg, false);
                if (res<=gc_result_tryattack_outofrange) then begin
                   if not isrunaway then begin
                      if (orders[0].itype=attackobj) and (orders[0].info.trg<>trg) then
                         _unit_SetOrderTrg(hnd, 0, trg, True)
                      else
                         _unit_OrderAttack(hnd, trg, True, False, False);
                   end;
                end;
             end;
             // and symmetrically for trg → hnd (if trg was also moving)
          end;
       end;
    end;
    ```
[^21]: Processing `noPath` - `progress/progress.inc/nothing.inc:171-316`:
    ```pascal
    171: var noPath : Boolean = (GetGameObjectTrackPointCountByHandle(goHnd) = 0);
    ...
    301: var tpCount : Integer = GetGameObjectTrackPointCountByHandle(goHnd);
    302: if tpCount > 0 then begin
           SetGameObjectTargetRotatingModeByHandle(goHnd, 'trmNone');
           DoSetupMoveAnimation(goHnd);
           SetGameObjectTrackPointCurrentPointIndexByHandle(goHnd, 0);
           SetGameObjectTrackPointCurrentPointIndexByHandle(goHnd, 1);
    312: end else begin
    313:    if _unit_GetTagStateByType(goHnd, gc_statetag_move) = gc_statetag_move_walk then
    314:       _unit_Stop(goHnd);
    315: end;
    ```
[^22]: `FindBestPosition` - `lib/miscext.script:190-252`, call from
    `nothing.inc`/`miscext.script:654-658`:
    ```pascal
    function FindBestPosition(goHnd : Integer; var px, pz : Float) : Boolean;
    begin
       const maxdensity = 3;
       var count : Integer = GetGameObjectCountCollidedObjectsByHandle(goHnd);
       if (count>maxdensity) then begin
          var standcount : Integer;
          for i:=0 to count-1 do begin
             trgHnd := GetGameObjectCollidedGOHandleByHandle(goHnd, i);
             ptrgobj := _unit_GetTObj(trgHnd);
             if (ptrgobj<>nil) and (TObj(ptrgobj).standtime>=3) then
                standcount := standcount+1;
          end;
          if (standcount>maxdensity) then begin
             var radius : Integer = 6;
             var minind : Integer = 8+floor(random*16);
             var maxind : Integer = GetSpiralStepsByRadius(radius)-1;
             if (ProcessSpiralIdleGridSearch(goX, goZ, 1, minind, maxind, radius, x, y)) then
                ...
                _unit_OrderMove(goHnd, goX, goZ, vecx, vecz, gc_obj_order_move_mode_default, False);
          end;
       end;
    end;
    ```
[^23]: Periodic topology update - `units/unit.inc/nothing.inc:128-132`:
    ```pascal
    if gametime>arg_obj.lasttimetopology then begin
       arg_obj.lasttimetopology := gametimewithrnd+gc_unit_TimeTopology;
       _unit_TopologyProgress(myHnd);
    end;
    ```

[^24]: Hard «hang fix» — `units/unit.inc/nothing.inc:148-154`:
    ```pascal
    else if (statetag and gc_statetag_essential_birth<>0)
           and (statetag and gc_statetag_visual_none<>0) then
    if ((arg_obj.orders[0].itype<gc_obj_order_type_leavetransport)
        and (arg_obj.orders[0].itype>gc_obj_order_type_leavebuilding))
        or (arg_obj.standtime>1) then
    begin
       _unit_SetTagStates(myHnd, gc_statetag_essential_none);
       ErrorLog('unit:nothing: Possible hang unit was fixed to essential_none');
    end;
    ```

[^25]: `_misc_FixCollisionInertiaObjectsInOnePoint` —
    `lib/misc.script:3739-3780`:
    ```pascal
    // fix issue when game may stuck on path trace
    var tries : Integer;
    for [MAIN]tries:=0 to 2 do
    if (GetCountOfPlayers>gc_playerind_env) then begin
       const epsilon = 0.001;
       ...
       for i:=GetPlayerGameObjectsCountByHandle(plhnd)-1 downto 0 do begin
          ...
          if (...VectorDistance < epsilon) then begin
             GameObjectDestroyByHandle(goHnd);
             break;
          end;
       end;
    end;
    ```
[^26]: `WriteMove` (distribution of personal move orders to squad) —
    `units/global.inc/writemove.inc:79-138`:
    ```pascal
    for j:=rows-1 downto 0 do
    for i:=cols-1 downto 0 do begin
       var gohnd : Integer = GetGroupGameObjectHandleByGridColRow(grhnd, i, j);
       if gohnd <> 0 then begin
          // calculate the formation's target cell in world coordinates
          x := posx + (i-cols/2+0.5) * minx * hdirx - (j+0.5) * miny * dirx;
          y := posz + (i-cols/2+0.5) * minx * hdirz - (j+0.5) * miny * dirz;

          // random dispersion within the unit radius (jitter)
          var unitradius : Float = gObjProp[...].radius;
          var dispradius : Float = unitradius*1.1;
          var dispx : Float = (0.5-random)*dispradius;
          VectorRotateY(dispx, dispy, dispz, random*360);
          x := x+dispx;
          y := y+dispz;

          if not addord then _unit_ClearOrders(gohnd);
          var pOrder : Pointer = _unit_OrderMove(gohnd, x, y, dirX, dirZ, mode, dofirst);
          if (pOrder<>nil) then TOrder(pOrder).info.amount := gPathTag;
       end;
    end;
    ```
[^27]: `_squad_FullRebuildGrid` - `lib/squad.script:199-263`.

[^28]: Formation constants - `dmscript.global:166-168`:
    ```pascal
    gc_formation_maxcount      = 160;   // maximum units per squad
    gc_formation_maskmaxwidth  = 54;
    gc_formation_maskmaxheight = 24;
    ```

[^29]: `_player_CalcSquadsMoveCount` — `lib/player.script:2591-2607`:
    ```pascal
    procedure _player_CalcSquadsMoveCount(plInd : Integer);
    begin
       for i := gPlayer[plInd].squads.GetCount-1 downto 0 do begin
          var pSquad : Pointer = gPlayer[plInd].squads.Get(i);
          TSquad(pSquad).fMoveCount := 0;
          for j := TSquad(pSquad).GetCount-1 downto 0 do begin
             var goHnd : Integer = TSquad(pSquad).Get(j);
             if ((GetGameObjectStatesTagByHandle(goHnd) and gc_statetag_move_walk)<>0) then
                TSquad(pSquad).fMoveCount := TSquad(pSquad).fMoveCount + 1;
          end;
       end;
    end;
    ```
[^30]: Using `fMoveCount` - `progress.inc:152, 160`,
    `lib/miscext.script:20`.

[^31]: `gc_player_SquadMoveTick = 10` - `dmscript.global:155`.

[^32]: `_misc_DoProgressOrders` (setting `bDoPosition := True` for
    move orders) - `lib/miscext.script:317-330, 613-633`.

[^33]: `_unit_RemoveOrder` with upath-collision —
    `units/unit.inc/onendpointreached.inc:54-58`. Author's comment:
    *should be logged only if unit stop cause of new unpathable
    collision on his way*.

[^34]: Profiler around `TopologyGetPath` -
    `progress/progress.inc/nothing.inc:155, 165`:
    ```pascal
    _misc_ProfilerBegin('progress.GetPath');
    ... TopologyGetPath / TopologyGetPathExt ...
    _misc_ProfilerEnd('progress.GetPath');
    ```
[^35]: Adaptive `secmax` - `progress/progress.inc:325-346`:
    ```pascal
    if (count>700) then secmax := secmax+(count div 20)
    else if (count<2000) then secmax := secmax+(count div 15)
    else secmax := secmax+(count div 10);
    ```

[^36]: `bIsShipDummy` — `units/unit.inc/initial.inc:200-256`.
