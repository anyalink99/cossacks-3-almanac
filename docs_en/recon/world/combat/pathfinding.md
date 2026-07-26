<a id="recon-pathfinding-и-движение-юнитов"></a>
<a id="поиск-пути-и-движение-юнитов"></a>
# Pathfinding and Unit Movement

[← How the game works](../../README.md)

How do units in Cossacks 3 find a way, bypass each other and buildings, and what
occurs when blocked. **The main conclusion right away:** the algorithm itself
`pathfinding` lives in the native engine (C++); scripts only place units
into the queue, transmit the target point and read the result. The algorithm is not visible -
only the frame around it is visible. All links to the code and the Pascal blocks themselves
collected in the [Sources](#sources) section at the end of the document.

**Related documents:**

- [ticks_and_subticks.md](../../../../internals_en/engine/ticks_and_subticks.md) - main progress-loop
  (`gc_progress_Interval = 0.02 s`), unit-tick = 100 ms.
- [server_sync_architecture.md](../../../../internals_en/engine/server_sync_architecture.md) —
  `WriteMove` / `ReadMove`, server-authoritative model, serialization
  queue in save.
- [building_mechanics.md](../economy/building_mechanics.md) – footprint and `CIMass`
  near buildings (massive “anchors” for collisions).

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
- **Friendly push** - silent: their units push each other apart,
  no animation.
- **Enemy at 90° in front** - the unit automatically switches to attack,
  even if he was going to another goal.
- **Formation** is a jittered offset for each unit, rather than following
  squad-leader. That’s why it moves “blurring”.

<a id="1-архитектура-две-независимые-подсистемы"></a>
## 1. Architecture: two independent subsystems

The engine divides unit navigation into two loosely coupled subsystems:

| Subsystem | What does | Where does he live |
|---|---|---|
| **Topology + QuadTree path-search** | Global search for path A → B through traffic zones; returns an array of `TrackPoint`'s. | Native APIs `Topology*` / `TraceLine*`. |
| **CollisionInertia (CI)** | Per-frame local bypass of neighbors along an already laid path (push / avoid with masses and inertia). | Native API `*CI*`. |

Scripts access both via `Set / Get*ByHandle` - **details
implementations in native code are not visible to scripts**.

Entry point to scripts: `_init_InitializeTopology` [^1]. Inside are set
key topology constants: `gc_top_TopologyPriority = 90`,
`gc_top_PathPriority = 70`, `gc_top_WallPriority = 95`,
`gc_top_EffectDist = 3` and others [^2]

This is **`QuadTree`-based collision world** with two priority layers: first
includes all static obstacles, the second - only terrain and walls.
Queries “a unit is passing through a building” have a lower priority so that `pathfinding`
could find his way “as if the building were not there.”

---

<a id="2-pathfinding-где-и-как"></a>
## 2. Pathfinding: where and how

<a id="21-очередь-и-батчевание"></a>
### 2.1 Queue and batching

**Queue:** two global lists in `_unit_PathListAdd` [^3]. Unit
added to `gGOPathList` (earth) or `gWaterPathList` (water) **exactly
once** when transitioning to state `gc_statetag_execute_move` [^4].
The `bpathrequested : Boolean` flag protects against duplication of [^5].

**Lists are serialized** in save/replay [^6] is part of the world state.

<a id="22-главный-батч-раз-в-progress-tick--20ms"></a>
### 2.2 Main batch (once per progress-tick = 20ms)

The entire batch of `pathfinding` is in `progress/progress.inc/nothing.inc` [^7].
Key steps:

1. One queue is selected - `gWaterPathList` or `gGOPathList` -
with priority 2:1 in favor of land (aquatic is processed only if
   earthly is empty OR `progresstick mod 2 == 0`).
2. For each unit in the queue, call
   `TopologyAddPathGameObjectByHandle`, and the unit is assigned
   float-tag — squad-id (for ground units) or -1 (for water units).
3. One batch call - `TopologyGetPath` (ground) or `TopologyGetPathExt`
   (water) - calculates paths for the entire queue at once.
4. For each unit, `noPath` is checked (there are no TrackPoints) and
   current-point indices are set; at the end the list is cleared.

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
4. **`squad` is passed as float-tag** before the request. Apparently, kernel
   uses it for group-routing (units of the same squad can receive
   agreed paths or common cost-map). Confirm empirically without
   decompilation is not possible.
5. **`noPath` is determined by `TrackPointCount == 0`**: if the kernel is not
   found the way, no TrackPoints.
6. After the batch, the script itself inserts building-exit-points (exit from
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
## 3. TrackPoints - pathfinding output

After `TopologyGetPath` each unit receives an array of **TrackPoints**
(waypoints) that the engine reads on each frame for interpolation
movements:
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

## 4. Collision avoidance (CI = CollisionInertia)

The main mechanism that forces units to **bypass each other**.
Essentially - local physical pushing (push with masses and inertia),
superimposed on top of an already laid path.

### 4.1 Per-unit init

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
### 4.2 Ships get huge CI

Ships summon `SetCustomCollisionInertia` with large [^17] multipliers:
`ferry` and `battleship` - `radius x11, mass x32`; `frigate`, `xebec` —
`9, 16`; `galley` - `7, 12`; `chaika`, `yacht`, `yachttur` - `6, 8`;
`fishboat` - `3, 1`.

This explains why ships **push** each other and **not themselves
shift** under the pressure of infantry: mass 32 versus 1 for infantry.

<a id="43-здания--неподвижные-тяжёлые-блокеры"></a>
### 4.3 Buildings - stationary heavy blockers

Buildings are initialized with `CollisionInertia=true`,
`CIIntersectRadius=0.35` tile, `CIMovable=false`, `CIMass=10000`,
`CIStuckAngle=5` (for units - 0), `CIAvoidPointMaxAngle=120`,
`CIMaxCollideCounter=7` [^18].

**Conclusion:** buildings are massive immovable blockers with a radius of 0.35
(plus a separate footprint-mask on the cell-grid; see
[building_mechanics.md](../economy/building_mechanics.md)). Global way around
buildings are being built by `pathfinding`; local collision (CI) only insures that
The unit did not hit the wall closely.

<a id="44-push-mechanic-между-юнитами-правило-передний--90-fov"></a>
### 4.4 Push-mechanic between units: “front + 90° FOV” rule

CI rules are set for three categories - `Fr` (friendly), `En` (enemy),
`Nl` (neutral) - via `SetGameObjectMyRuleCollidedExec*` [^19]:

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

1. **Union → Union:** pure physics CI (`mass` / `intersect` /
   `inertia`), without events. Units “stick together” and smoothly push apart -
   the front one pushes the rear one in the direction of movement.
2. **Enemy → enemy (90° front):** called by `_misc_Collided`, which
   automatically initiates an attack.
3. **Unit → building / building → unit:** building `bMovable=False` +
   `mass=10000` - push-physics does not move the building, the unit flows around.
4. **Projectiles and pedestrian markers:**
   `SetGameObjectMyCollisionDetection(False)` - ignore CI.

---

## 5. Stuck handling

### 5.1 Per-frame: “no path → stop”

In `pathfinding`'s batch [^21] after calling `TopologyGetPath` for each
unit is calculated by `noPath` through `TrackPointCount = 0`. If TrackPoints
yes - `current-point` indices and motion animation are set.
If not - and the unit was in `gc_statetag_move_walk` - it is called
`_unit_Stop`.

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

### 5.4 Hard “hang fix”

`unit.inc/nothing.inc` has a watchdog for invisible units in the state
“I’m born, but I don’t see myself” (left the barracks, but didn’t show up) [^24]:
after 1 s `standtime` is forced to be entered
`gc_statetag_essential_none`. This is not an ordinary stuck, but glitch protection
transport / leave-building.

<a id="55-loader-pass-на-старте-два-юнита-в-одной-точке"></a>
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
## 6. Formation movement: each unit moves on its own

Main insight: **formation does not move as a unit**.
There is no squad-leader as such - **each unit gets its own
individual target**.

<a id="61-writemove--рассыпать-squad-на-per-unit-ордера"></a>
### 6.1 `WriteMove` - scatter the squad into per-unit orders

`WriteMove` [^26] walks the formation grid and for each unit:

1. Calculates the target cell of the formation in world coordinates.
2. Adds random variance (jitter) within
   `unitradius * 1.1` through the turn to `random*360`.
3. Calls `_unit_OrderMove(gohnd, x_personal, y_personal, ...)` -
   personal order for your cell with jitter.

Then the unit goes **independently**, through the standard chain
`_unit_PathListAdd` → `TopologyGetPath`. None
“leader-leads-the-rest” is not.

`gPathTag` (rolling 1..255) is written as `info.amount` - **does not apply to
`pathfinding`**, this is an order-cookie for server↔client sync.

<a id="62-грид-формации"></a>
### 6.2 Formation Grid

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
### 6.4 Squad-id as hint for kernel

Remember from §2.2: before `TopologyGetPath`, each unit receives
`SetGameObjectTagFloatByHandle(goHnd, TObj(pObj).squad)`. What kernel with
does this - **not visible from the scripts**. Hypothesis: consistent routing
for one unit (units do not cross paths with each other in chess
okay). But this is **not confirmed**; need decompilation or
empirical test with two squads in a narrow passage.

<a id="65-orphan-константа"></a>
### 6.5 Orphan constant

`gc_player_SquadMoveTick = 10` [^31] - **defined, but not found anywhere
used** (Grep for all `.script` files only gives a definition).
Possibly reserved for squad-level repath, but not
implemented.

---

## 7. Repath frequency

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

- **Queue `pathfinding` - without cap** in scripts. How many units
  hit `gGOPathList` in a tick (20 ms), that's how much it will be processed in one
  call `TopologyGetPath`.
- **TrackPoint smoothing**: `SkipFactor=1`, `SkipEpsilon=0.1`,
  `SkipPoints=true` [^12] - the unit can cut off intermediate points if
  there is a clear line of sight ahead.
- **CI per-unit budget** [^15]:
  - `MaxCollideCounter = 7*3 = 21` (number of collisions per tick before lights out);
  - `MaxProcessObject = 4*3 = 12` (number of objects in the vicinity,
    processed by CI).

<a id="82-профайлер-встроен"></a>
### 8.2 Profiler built-in

The script wraps `TopologyGetPath` in calls
`_misc_ProfilerBegin('progress.GetPath')` and `_misc_ProfilerEnd` [^34].
There is no profiler data in the scripts, but the engine can measure the cost.

<a id="83-глобальный-progress-cap"></a>
### 8.3 Global progress-cap

In `progress.inc` [^35] for misc/pool players there is a dynamic `secmax`
(adaptive processing slicing): with `count > 700` the step increases as
`count div 20`, with `count < 2000` - `count div 15`, otherwise -
`count div 10`. For `gGOPathList` itself **there is no such thing**, queue
processed completely.

---

<a id="9-открытые-вопросы-для-эмпирических-замеров"></a>
## 9. Open questions (for empirical measurements)

1. **Path-search algorithm** - A*, flow-field or wave? Decompilation
   native `TopologyGetPath` or empirical test: long way with
   several equally long alternatives and seeing which one is chosen.
   Hypothesis: A* with heuristic = euclidean.
2. **Impact of squad-id float-tag**: is it really transmitted to the kernel as
   group-routing hint? Empirically: move two squads in parallel across
   narrow passage (1 tile) and see if the paths conflict.
3. **path-list-burst boundary**: how many units start move at the same time
   without FPS drop - 200, 500, 1000? The script does not limit, kernel -
   perhaps.
4. **Repath to a new obstacle**: build a building exactly on the path
   walking squad. Will there be an automatic repath or units
   will they resist and stop?
5. **`CIStuckAngle = 0` for units vs. `= 5` for buildings**: what does this mean
   behaviorally? For buildings, the “consider stuck” threshold is 5°, for units it is 0°.
   Most likely related to rotation-snapping CI-physics.
6. **Ships + dummy frigate**: `bIsShipDummy` [^36] - separate
   collision entity? Does it affect `pathfinding`?
7. **Relationship between footprint-mask of building (cell=0.5) and `CIIntersectRadius=0.35`**:
   `0.35 < 0.5`, which means the CI radius is **smaller** than the blocking grid. Units
   can “scratch” on the corners of buildings - this geometry is hidden. Worth it
   check empirically.

---

<a id="10-резюме"></a>
## 10. Summary

- **`pathfinding`'s algorithm is in the native engine.** Scripts only: (a)
  add units to `gGOPathList` or `gWaterPathList` when starting move,
  (b) call `TopologyGetPath` or `TopologyGetPathExt` once every 20 ms,
  (c) interpret the returned TrackPoints. The search itself (A* / flow /
  wave) **not visible**; indirectly - this is `QuadTree`-collision-world + graph
  `TTopZone` with connectivity at radius 3 + path-priority/topology-priority
  layers + `TraceLineQuadTree` for LoS-checks.
- **Collision avoidance is `CollisionInertia` (CI):** per-unit mass
  and radius, push-physics. Buildings - `mass=10000, movable=False`, ships
  get increased mass and radius. The push unit is silent; enemy in
  front 90° - automatic attack-event.
- **Stuck handling — minimal.** If the path is not found, the unit just
  worth it (no timeout, no teleport). With more than 3 standing neighbors and
  `standtime >= 3 s` - `FindBestPosition` spirally looking for a free
  cell within a radius of 6. At the start
  `_misc_FixCollisionInertiaObjectsInOnePoint` removes overlapping
  environment objects so that path-trace does not get stuck.
- **Formation movement is NOT squad-leader.** `WriteMove` scatters
  group: each unit gets its own
  `_unit_OrderMove(personal_x, personal_y)` with jitter within
  unit-radius. There are no single squad paths in the scripts; squad-id
  is passed to the kernel as a float-tag, but the effect is not visible from the code.
  `gc_player_SquadMoveTick = 10` is an orphan constant.
- **Repath:** only when changing order or new move command. Periodic
  repath is missing.
- **There are no limits in scripts:** the queue is processed in one batch. If
  500 units start simultaneously - all in one call
  `TopologyGetPath`. The cost is measured by the built-in `_misc_Profiler`,
  but scripts do not use it for throttling.

**All calls from the script go to native code, the path-search algorithm is not
visible.** Further investigation requires decompiling Cossacks 3 EXE or
empirical tests with target scenarios (see §9).

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
