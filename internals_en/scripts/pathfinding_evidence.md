<a id="recon-pathfinding-и-движение-юнитов"></a>
<a id="поиск-пути-и-движение-юнитов"></a>
<a id="технический-разбор-поиска-пути-и-движения"></a>
# Technical Evidence for Pathfinding and Movement

[← Scripts and Scenarios](structure.md)

[Reader guide to unit movement](../../docs_en/recon/world/combat/pathfinding.md)

This article explains how units choose a route, avoid neighbors and
obstacles, move in formation, and react when blocked. The exact native
algorithm is unknown, so observed game behavior is separated from
[Technical Details](#technical-details).

**Related documents:**

- [Ticks and subticks](../engine/ticks_and_subticks.md)
  — timing of the main simulation loops.
- [Server architecture and network synchronization](../engine/server_sync_architecture.md)
  — movement-order transfer between server and clients.
- [Building construction, repair, and destruction](../../docs_en/recon/world/economy/building_mechanics.md)
  — building footprints.

<a id="коротко"></a>
## At a Glance

- The game first plans a route around map obstacles, then locally pushes
  neighboring objects apart every frame.
- Route requests are batched and processed every 20 ms.
- The collision map uses 0.5-cell subdivisions of the game grid.
- **Friendly pushing** is silent: allied units push one another apart
  without triggering an animation.
- **An enemy in the forward 90° sector** makes a unit switch to attack,
  even when it was moving toward another destination.
- A **formation** gives each unit its own destination with a small random
  offset; units do not follow a single squad leader. This is why a moving
  formation spreads slightly.
- If no route is found, the unit stops. There is no universal stuck-unit
  teleport or pathfinding timeout.

<a id="движение-для-игрока"></a>
<a id="как-движение-выглядит-для-игрока"></a>
## How Movement Behaves in Play

<a id="маршрут-и-препятствия"></a>
### Routes and Obstacles

A movement order specifies the destination, and the game returns a chain of
intermediate route points. A unit may skip unnecessary bends when the next
section is clear in a straight line. Land and water routes are calculated
separately, with land requests receiving higher priority.

If no route is found, the unit stops. A new calculation begins after a new
movement order, a target change, or a special attempt to leave a dense crowd.
Routes are not universally recalculated every frame.

<a id="обход-соседей"></a>
### Avoiding Neighbors

Local pushing is applied on top of the planned route:

- allies gently push one another apart without a separate reaction;
- an enemy in the forward 90° sector may cause a unit to attack;
- buildings remain immovable while units flow around them;
- ships are much heavier than land units and push their neighbors harder.

<a id="что-происходит-в-толпе"></a>
### Dense Crowds

When more than three nearby objects are standing and at least four have
remained still for three game seconds, a unit searches for a free position
in a six-cell spiral roughly once every 3.075 game seconds. This disperses
many crowds but does not guarantee escape from every dead end.

<a id="движение-построения"></a>
### Formation Movement

A formation has no single route that every member follows blindly. The game
computes each unit's grid position, adds a small random offset, and issues a
separate movement order. A wide formation may therefore stretch through a
narrow passage and assemble again after stopping.

<a id="нагрузка-при-массовом-приказе"></a>
### Cost of Mass Movement

No script-side limit on the route queue was found. Every unit requesting a
route during one tick is passed to the native engine in one batch. This
supports mass orders, but the practical performance limit depends on the
hidden engine implementation.

---

<a id="технические-подробности"></a>
## Technical Details

<a id="1-архитектура-две-независимые-подсистемы"></a>
<a id="архитектура-две-независимые-подсистемы"></a>
### Architecture: Two Independent Subsystems

The engine divides unit navigation into two loosely coupled subsystems:

| Subsystem | Purpose | Implementation |
|---|---|---|
| **Topology and obstacle map** (`Topology`, `QuadTree`) | Global A → B routing through traversable zones; returns an array of route points (`TrackPoint`). | Native functions `Topology*` / `TraceLine*`. |
| **Collision avoidance** (`CollisionInertia`, CI) | Per-frame avoidance and pushing along an existing route, with mass and inertia. | Native functions `*CI*`. |

Scripts access both through `Set*ByHandle` and `Get*ByHandle` functions.
Their native implementations are not visible to script code.

The script-side entry point is `_init_InitializeTopology` [^1]. It sets the
main topology constants: `gc_top_TopologyPriority = 90`,
`gc_top_PathPriority = 70`, `gc_top_WallPriority = 95`,
`gc_top_EffectDist = 3`, and others [^2].

This is a **`QuadTree`-based collision world** with two priority layers.
The first includes all static obstacles; the second includes only terrain
and walls. Requests that allow a unit to leave a building use the lower
priority layer so that a route can be found as if the building were absent.

---

<a id="2-pathfinding-где-и-как"></a>
<a id="2-где-и-как-рассчитывается-путь"></a>
<a id="где-и-как-рассчитывается-путь"></a>
### Where and How Routes Are Calculated

<a id="21-очередь-и-батчевание"></a>
<a id="21-очередь-и-пакетная-обработка"></a>
<a id="очередь-и-пакетная-обработка"></a>
#### Queue and Batching

**Queue:** `_unit_PathListAdd` uses two global lists [^3]. A unit is added
to `gGOPathList` (land) or `gWaterPathList` (water) **once** when it enters
`gc_statetag_execute_move` [^4]. The Boolean `bpathrequested` flag prevents
duplicate entries [^5].

Both lists are serialized as part of the save and replay world state [^6].

<a id="22-главный-батч-раз-в-progress-tick--20ms"></a>
<a id="22-главный-пакет-запросов-раз-в-20-мс"></a>
<a id="главный-пакет-запросов-раз-в-20-мс"></a>
#### Main Batch (Once Every 20 ms)

The pathfinding batch is processed in
`progress/progress.inc/nothing.inc` [^7]:

1. One queue is selected: `gWaterPathList` or `gGOPathList`. Land receives
   2:1 priority; water is processed only when the
   land queue is empty or `progresstick mod 2 == 0`).
2. For each unit in the queue, call
   `TopologyAddPathGameObjectByHandle`, and the unit is assigned
   a numeric squad tag for land units, or `-1` for water units.
3. One batch call—`TopologyGetPath` for land or `TopologyGetPathExt` for
   water—calculates paths for the entire queue.
4. For each unit, the script checks `noPath`, sets the current route-point
   indices, and finally clears the queue.

**What is important:**

1. **One batch per progress tick.** `progresstick` advances every 20 ms
   (`gc_progress_Interval = 0.02`). A tick handles either land or water,
   never both.
2. **Land has 2:1 priority.** The water queue is processed only when the
   land queue is empty or `progresstick mod 2 == 0`.
3. **The whole list is submitted in one call** to `TopologyGetPath` or
   `TopologyGetPathExt`. Native code receives an array of units and their
   start and end points, calculates each route, and fills the `TrackPoint`
   arrays. The algorithm itself is not visible to scripts.
4. **`squad` is passed as a numeric tag** before the request. The engine
   may use it to coordinate routes for units in one squad or to share a
   movement-cost map. Confirming this without decompilation is impossible.
5. **`noPath` is determined by `TrackPointCount == 0`**: when the engine
   finds no route, the route-point array is empty.
6. After the batch, the script inserts building exit points (for leaving a
   barracks or transport) and resets `bpathrequested`.

<a id="23-что-делает-topologygetpath-наблюдаемо"></a>
<a id="наблюдаемая-роль-topologygetpath"></a>
#### Observable Role of `TopologyGetPath`

From the usage context and class name:

- **`QuadTree`** is a spatial obstacle index that divides the world into
  cells.
- **Topology** is a higher-level graph of **zones**
  (`TopologyGetZoneIndex(x, z)`). `_unit_TopologyAdd`,
  `_unit_TopologyRemove`, and `_unit_TopologyProgress` [^8] track the zone
  occupied by each unit for quick distance checks.
- **`TopologyGetPathDistance(x1,z1,x2,z2,bIncludeBuildings)`** [^9] —
  a synchronous function that returns path length along the topology graph.
  It is used by computer-player logic, not to move units.
- **`TopologyGetPathToZone(zoneInd)`** [^10] requests a route to a zone for
  computer-player combat logic.

**Layer Hypothesis:**

- At a high level, the engine may use A* across the zone graph, with
  `TTopZone` nodes and connections defined by `gc_top_EffectDist = 3`.
- At a low level, grid or quadtree collision tests may place `TrackPoint`
  entries between graph nodes.

This interpretation is consistent with `TopologySetPosSearchRadius(7)`,
which controls how far the engine searches for a nearby passable point.

**Grid:** `gc_collision_size = 0.5` [^11] means one collision cell spans
half of one game cell, about 26 pixels. `gc_MaxColMapWidth =
2*gc_MaxMapWidth` likewise shows that the collision grid has twice as many
cells per side as the main map grid, for example 1,280 versus 640.

> **The algorithm is not visible:** `TopologyGetPath` and
> `TopologyGetPathExt` enter native code. Scripts do not reveal whether the
> implementation uses A*, a flow field, wave propagation, or another
> method. Indirect evidence includes batched unit requests, a squad ID
> passed as a hint, a separate zone graph plus `QuadTree`, and the
> `TraceLineQuadTree` ray-casting function.

---

<a id="3-trackpointы--выход-pathfindingа"></a>
<a id="3-маршрутные-точки"></a>
<a id="маршрутные-точки"></a>
### Route Points

After `TopologyGetPath`, each unit receives an array of **route points**
(`TrackPoint`) that the engine reads every frame to interpolate movement:
- `GameObjectTrackPointAddByHandle(hnd, x, y, z)` — append.
- `GameObjectTrackPointInsertByHandle(hnd, ind, x, y, z)` – insert
  (used to insert the exit-point of the building **at the beginning**).
- `SetGameObjectTrackPointCurrentPointIndexByHandle(hnd, idx)` — set
  current.
- `GetGameObjectTrackPointCountByHandle(hnd)` — list length.
- `SetGameObjectTrackPointSkipPointsByHandle(hnd, true)` — allow
  skip intermediate points (if there is visibility until the next one).
- `SetGameObjectTrackPointSkipQuadTree(quadTree)` / `SkipFactor(1)` /
  `SkipEpsilon(0.1)` [^12] — path smoothing parameters.

Each unit selects a quadtree for route smoothing:
`gc_obj_media_land` uses `TopologyGetPathQuadTree`, while
`gc_obj_media_water` uses `TopologyGetTopologyQuadTree` [^12].

Reaching the end of the path triggers `OnEndPointReached` [^13], which
switches the unit to `move_idle` and deletes the order.

When completing a turn, `OnDirectionReached` [^14] is triggered.

---

<a id="4-предотвращение-столкновений-collisioninertia-ci"></a>
<a id="предотвращение-столкновений-collisioninertia-ci"></a>
### Collision Avoidance (`CollisionInertia`, CI)

This is the main mechanism that makes units **avoid one another**:
local physical pushing with mass and inertia, applied on top of an
already calculated route.

<a id="41-параметры-отдельного-юнита"></a>
<a id="параметры-отдельного-юнита"></a>
#### Per-Unit Parameters

CI parameters are set in `SetCustomCollisionInertia` [^15]: `CIMass`,
`CIIntersectRadius`, `CIDeltaStep`, `CIRotationSpeed`, `CIStuckAngle`,
`CIEpsilonAngle`, `CIEpsilonShift`, `CIEpsilonMove`,
`CIDistExtPointEpsilon`, `CIMaxCollideCounter`, `CIMaxProcessObject`.

Constants:

- `gc_collision_radius_default = 0.16` [^16].
- `gc_collision_radius_stand = 0.1`.
- `gc_collision_radius_attack = 0.1`.

Formation spacing values used by `WriteMove`:

- `gc_obj_radius_default = 10`, `gc_obj_radius_horse = 15`.
- `gc_obj_radius_formation_default = 8`, `gc_obj_radius_formation_horse = 12`.

The intersection radius of an infantry unit is about 0.16 game cells, so
units can stand close together. Cavalry uses `unitradius = 15` for formation
spacing.

<a id="42-корабли-получают-огромную-ci"></a>
<a id="42-корабли-получают-большую-инерцию-столкновений"></a>
<a id="корабли-получают-большую-инерцию-столкновений"></a>
#### Ships Receive Much Greater Mass and Radius

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
<a id="здания--тяжёлые-неподвижные-препятствия"></a>
#### Buildings Are Heavy, Immovable Obstacles

Buildings are initialized with `CollisionInertia=true`,
`CIIntersectRadius=0.35` game cell, `CIMovable=false`, `CIMass=10000`,
`CIStuckAngle=5` (for units - 0), `CIAvoidPointMaxAngle=120`,
`CIMaxCollideCounter=7` [^18].

**Conclusion:** buildings are massive immovable obstacles with a radius
of 0.35 (plus a separate footprint mask on the cell grid; see
[construction and repair](../../docs_en/recon/world/economy/building_mechanics.md)). Pathfinding
calculates the global route around them; local collision avoidance only
keeps a unit from pressing directly into a wall.

<a id="44-push-mechanic-между-юнитами-правило-передний--90-fov"></a>
<a id="44-расталкивание-юнитов-и-передний-сектор-в-90"></a>
<a id="расталкивание-юнитов-и-передний-сектор-в-90"></a>
#### Unit Pushing and the Forward 90° Sector

Collision rules distinguish allies (`Fr`), enemies (`En`), and neutral
objects (`Nl`) through `SetGameObjectMyRuleCollidedExec*` [^19]:

- `Fr` (friendly): no event is generated. CI still pushes the objects
  physically, but script logic does not intervene.
- `En` (enemy): `_misc_Collided` is generated only when the enemy lies
  within the forward 90° sector. A unit may therefore attack an enemy it
  meets head-on without reacting to contact from behind.
- `Nl` (neutral): handled like a friendly object, without an event.
The `_misc_Collided` [^20] handler itself checks that both objects are
`gc_obj_material_body`, then tries to attack through `_unit_TryAttack`. If
the target is out of range and the unit is not retreating, the current order
is replaced with an attack order.

**Push mechanics summary:**

1. **Ally → ally:** CI physics only (`mass`, intersection radius, and
   inertia), without events. Units remain packed together while pushing one
   another apart smoothly.
2. **Unit → enemy (90° front):** `_misc_Collided` is called and
   automatically initiates an attack.
3. **Unit → building:** with `bMovable=False` and `mass=10000`, collision
   physics leaves the building fixed and redirects the unit around it.
4. **Projectiles and path markers:**
   `SetGameObjectMyCollisionDetection(False)` - ignore CI.

---

<a id="5-обработка-застревания"></a>
<a id="обработка-застревания"></a>
### Handling Stuck Units

<a id="51-проверка-каждый-кадр-нет-пути--остановиться"></a>
<a id="проверка-каждый-кадр-нет-пути--остановиться"></a>
#### Per-Frame Check: “No Route Means Stop”

After `TopologyGetPath`, the batch sets `noPath` from
`TrackPointCount = 0` [^21]. When route points exist, it initializes the
current-point indices and movement animation. When the array is empty and
the unit is in `gc_statetag_move_walk`, it calls `_unit_Stop`.

If no route is found, the unit stops without a dedicated timeout or
immediate retry. The order remains when `bRemove=False`, so another
transition to `execute_move` can request a fresh route.

<a id="52-сжатая-толпа--findbestposition"></a>
<a id="сжатая-толпа--findbestposition"></a>
#### Dense Crowd: `FindBestPosition`

`FindBestPosition` [^22] is called from `nothing.inc` when an idle unit has
`standtime > 1`. If more than `maxdensity = 3` neighbors overlap it and at
least four of those neighbors have `standtime >= 3`, the function performs
a spiral search for a free idle-grid cell within radius 6 and issues a move
order to that position. The check is rate-limited through
`lasttimebestposition` to
`gc_unit_TimeFindBestPosition = 0.1*31 - 0.025 ≈ 3.075` game seconds.

<a id="53-топология-обновляется-по-таймеру"></a>
<a id="топология-обновляется-по-таймеру"></a>
#### Timed Topology Update

In `unit.inc/nothing.inc` `_unit_TopologyProgress` is periodically called
at intervals `gc_unit_TimeTopology = 0.1*50 - 0.025 ≈ 4.975 s` [^23].
This is not a route recalculation. It refreshes the unit's topology zone for
computer-player distance queries.

<a id="54-аварийное-исправление-зависания"></a>
<a id="аварийное-исправление-зависания"></a>
#### Emergency Recovery from an Invalid State

`unit.inc/nothing.inc` contains a watchdog for a unit that remains in its
birth state while its visual state is still `visual_none`, for example after
leaving a Barracks without appearing correctly [^24]. After one game second,
or for a relevant leave-building or leave-transport order, the code forces
`gc_statetag_essential_none`. This protects transport and building-exit
transitions; it is not ordinary pathfinding recovery.

<a id="55-loader-pass-на-старте-два-юнита-в-одной-точке"></a>
<a id="55-проверка-при-загрузке-два-юнита-в-одной-точке"></a>
<a id="проверка-при-загрузке-два-юнита-в-одной-точке"></a>
#### Load-Time Check for Two Objects at One Point

Map generation calls `_misc_FixCollisionInertiaObjectsInOnePoint` [^25].
It makes three passes and destroys duplicate environment objects occupying
the same point, preventing an infinite loop during route tracing. The call
originates in `common.inc/dogenerate.inc:2070`.

<a id="56-чего-не-найдено"></a>
<a id="чего-не-найдено"></a>
#### What Was Not Found

- **No per-route timeout.** A unit can wait with `bpathrequested=True`,
  receive an empty route, and stop.
- **No stuck-unit teleport.** The `essential_none` watchdog described above
  resets a state flag; it does not move the unit.
- **No `gGOPathList` length cap.** Script code submits the entire queue as
  one batch.

---

<a id="6-formation-movement-каждый-юнит-идёт-сам"></a>
<a id="6-движение-построения-каждый-юнит-идёт-сам"></a>
<a id="движение-построения-каждый-юнит-идёт-сам"></a>
### Formation Movement: Each Unit Moves Independently

The key point is that a **formation does not move as one object**.
There is no single squad leader to follow: **each unit receives its own
destination**.

<a id="61-writemove--рассыпать-squad-на-per-unit-ордера"></a>
<a id="61-writemove--выдать-каждому-юниту-отдельный-приказ"></a>
<a id="writemove-отдельный-приказ-каждому-юниту"></a>
#### `WriteMove` Issues a Separate Order to Each Unit

`WriteMove` [^26] walks the formation grid and for each unit:

1. Calculates the target cell of the formation in world coordinates.
2. Adds a small random offset within `unitradius * 1.1`, rotated by
   `random*360`.
3. Calls `_unit_OrderMove(gohnd, x_personal, y_personal, ...)`, giving that
   soldier an individual destination.

Every unit then follows the standard
`_unit_PathListAdd` → `TopologyGetPath` chain independently. There is no
leader-following movement model.

`gPathTag`, a rolling value from 1 to 255, is written to `info.amount`. It
acts as an order token for server–client synchronization rather than a route
parameter.

<a id="62-грид-формации"></a>
<a id="62-сетка-построения"></a>
<a id="сетка-построения"></a>
#### Formation Grid

`_squad_FullRebuildGrid` [^27] maintains the per-squad `arGrid[i,j]`
mapping from formation cells to units. A turn or mode change rebuilds the
grid according to the new direction.

Constants [^28]: `gc_formation_maxcount = 160` (max units in squad),
`gc_formation_maskmaxwidth = 54`, `gc_formation_maskmaxheight = 24`.

<a id="63-fmovecount--простой-счётчик"></a>
<a id="fmovecount-простой-счётчик"></a>
#### `fMoveCount`: Simple Counter

`_player_CalcSquadsMoveCount` [^29] recounts the units in
`gc_statetag_move_walk` for each squad. It runs every
`gc_global_TimeCalcSquadsMoveCount = 0.03*10 = 0.3` game seconds and is used
only by squad aggression and hold-mode checks [^30], not by pathfinding.

<a id="64-squad-id-как-hint-для-kernel"></a>
<a id="64-номер-отряда-как-подсказка-движку"></a>
<a id="номер-отряда-как-подсказка-движку"></a>
#### Squad ID as a Hint to the Engine

Before the batched `TopologyGetPath` call, each unit receives
`SetGameObjectTagFloatByHandle(goHnd, TObj(pObj).squad)`. Scripts do not
reveal how native code uses this value. It may help coordinate routes within
one squad, but confirming that requires decompilation or a controlled test
with two squads in a narrow passage.

<a id="65-orphan-константа"></a>
<a id="65-неиспользуемая-константа"></a>
<a id="неиспользуемая-константа"></a>
#### Unused Constant

`gc_player_SquadMoveTick = 10` [^31] is defined but never referenced by
other `.script` files. It may have been reserved for squad-level route
updates.

---

<a id="7-когда-путь-рассчитывается-заново"></a>
<a id="когда-путь-рассчитывается-заново"></a>
### When Routes Are Recalculated

| When a unit requests a new path | Why |
|---|---|
| Entering `gc_statetag_execute_move` | `_unit_PathListAdd` is called explicitly from `ontagstates.inc`. |
| Clearing or replacing an order: `_unit_ClearOrders` → new `_unit_OrderMove` | `_unit_OrderMove` creates `gc_obj_order_type_move`; `_misc_DoProgressOrders` sets `bDoPosition := True` [^32], leading to `gc_statetag_execute_move` and `_unit_PathListAdd`. |
| `FindBestPosition` finding a free cell in a dense crowd | At most once every 3.075 game seconds. |

No script-side route recalculation was found in these situations:

- **Periodic recalculation while moving.** No timer or direct call performs
  it. A moving combat target instead causes attack logic to issue another
  order.
- **Collision with an enemy.** `_misc_Collided` calls `_unit_TryAttack` or
  `_unit_OrderAttack`; the resulting attack may issue movement as needed.
- **A new obstacle appearing on the route.** No immediate recalculation call
  was found. A blocked unit can reach `OnEndPointReached`, remove the
  unusable route through `_unit_RemoveOrder` [^33], and stop. Whether it
  requests another route then depends on the active order.

---

<a id="8-производительность-и-лимиты"></a>
<a id="производительность-и-лимиты"></a>
### Performance and Limits

<a id="81-лимиты-в-скриптах"></a>
<a id="лимиты-в-скриптах"></a>
#### Limits in Scripts

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
<a id="встроенный-профайлер"></a>
#### Built-In Profiler

The script wraps `TopologyGetPath` in calls
`_misc_ProfilerBegin('progress.GetPath')` and `_misc_ProfilerEnd` [^34].
There is no profiler data in the scripts, but the engine can measure the cost.

<a id="83-глобальный-progress-cap"></a>
<a id="83-глобальное-ограничение-цикла-расчёта"></a>
<a id="глобальное-ограничение-цикла-расчёта"></a>
#### Global Progress Cap

`progress.inc` uses a dynamic `secmax` for the internal `misc` and `pool`
players to divide processing adaptively [^35]. When `count > 700`, the
increment is `count div 20`. Otherwise, `count < 2000` is always true for an
ordinary nonnegative counter, so the increment is `count div 15`. The final
`count div 10` branch is effectively unreachable, probably because the
conditions are ordered incorrectly. `gGOPathList` has no equivalent slice:
the whole route queue is processed.

---

<a id="9-открытые-вопросы-для-эмпирических-замеров"></a>
<a id="9-что-ещё-требует-проверки"></a>
## 9. Questions Requiring Further Testing

1. **Pathfinding algorithm:** A*, a flow field, or a wave search? This
   requires decompiling native `TopologyGetPath` or testing several
   equally long routes. The working hypothesis is A* with a Euclidean
   heuristic.
2. **Effect of the numeric squad tag:** does the engine actually use it
   to coordinate group routes? Move two squads through a one-cell
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
7. **Building footprint versus collision radius:** with a 0.5-cell collision
   and `CIIntersectRadius=0.35`, the collision radius is smaller than the
   blocking grid. Test whether units catch on building corners.

---

<a id="10-резюме"></a>
<a id="сводка-технических-выводов"></a>
## Summary of Technical Findings

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
    SetGameObjectCIIntersectRadiusByHandle(colHnd, 0.35);  // 0.35 cells
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
