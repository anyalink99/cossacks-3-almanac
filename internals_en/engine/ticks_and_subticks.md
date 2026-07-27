<a id="recon-тики-сабтики-время"></a>
# Recon: Ticks, Sub-Tick State, and Time

This document describes Cossacks 3's time model: the main progress loop,
state-machine intervals, variable time steps, and adaptive game speed. These
mechanisms explain why a simulation may not replay identically after save/load,
even on the same host, and why different machines can diverge. Code references
and Pascal excerpts are collected in [Sources](#sources).

**Related documents:**

- [determinism_audit.md](determinism_audit.md) — RNG sites in resource gathering and
  battle; this document describes **when** they are called.
- [server_sync_architecture.md](server_sync_architecture.md) — how
  server-authoritative architecture is related to ticks; sync packages in
  real-time versus game-time logic.

## TL;DR

- **Three time scales** coexist in the code: real time (wall-clock seconds),
  game time (logical simulation time, scaled by `TimeSpeedFactor`)
  and frames (animation frames; 32 frames = 1 game-second).
- The main progress loop targets one tick every **20 ms** of real time
  (`gc_progress_Interval = 0.02`). It distributes pathfinding requests,
  processes periodic events and the economy, and adapts game speed.
- Units do **not** tick every frame. Each class has its own interval: military —
  100 ms, peasants - 135 ms (`gc_statemachine_interval_*`).
- During save/load, some `gProgress.last*time` timestamps may not resume at an
  identical phase. A subsystem can miss a tick or run twice in quick
  succession, contributing to non-reproducibility.

---

<a id="1-три-временных-шкалы"></a>
## 1. Three Time Scales

Three different “times” coexist in the code:

| Scale | Meaning | API / representation |
|---|---|---|
| **Real time** | Wall seconds | `_misc_GetRealTime`, `GetCurrentTime` |
| **Game time** | Logical simulation time, scaled by `TimeSpeedFactor` | `GetGameTime`, designated `gametime` |
| **Frames** | Discrete frames of animations and timings in scripts | `gc_time_to_frames = 32` |

**Key relationships:**
```
1 game-second  =  32 frames                      (gc_time_to_frames)
1 game-second  =  1 / (TimeSpeedFactor/10)  real-seconds
                = 1.43 real-sec @ slow (factor 7)
                = 1.00 real-sec @ normal (factor 10)
                = 0.71 real-sec @ fast (factor 14)
```
Game-speed presets [^1]:

- `gc_settings_gamespeed_0 = 7` (slow)
- `gc_settings_gamespeed_1 = 10` (normal)
- `gc_settings_gamespeed_2 = 14` (fast)

This is the lobby's `gMap.settings.additional.gamespeed` option. For all speed
values, see
[`reports/map/lobby_settings.md`](../../docs_en/reports/map/lobby_settings.md#gamespeed--скорость-партии);
behavior decoding - [`game_settings.md`](../../docs_en/recon/world/map/game_settings.md) §3.6.

Script durations such as animations, `buildtime`, and `attackpause` are
expressed in **frames**. Convert them to game seconds with `frames / 32`, then
to real seconds by additionally dividing by `TimeSpeedFactor / 10`.

---

<a id="2-главный-progress-loop"></a>
## 2. Main progress-loop

The simulation's central loop is in `progress/progress.inc/nothing.inc` (745
lines). The `progress` state machine is represented as a separate player-like
object and ticks whenever the engine invokes its `Nothing` state.

<a id="21-структура-одного-тика"></a>
### 2.1 Single tick structure

During each tick, the progress loop reads `gametime`, calculates `deltatime`
from the previous tick, and, if the game is not paused, runs the relevant
subsystems. These include economy accrual through
`_res_ProcessEconomy(deltatime)`, distribution of pathfinding requests from
`gWaterPathList` and `gGOPathList`, timestamp-driven events, and game-speed
adaptation based on real FPS. At the end of the tick,
`gProgress.progresstick` is incremented and
`gProgress.lastprogresstime` is updated to the current `gametime` [^2].

<a id="22-что-progress-loop-не-делает"></a>
### 2.2 Work not performed directly by the progress loop

It does **not tick every unit directly**. Units have their own state machines
and `Nothing` cycles. The progress loop:

- starts the economy (`_res_ProcessEconomy(deltatime)`);
- distributes pathfinding requests;
- pushes periodic events;
- manages progress sections (see §3), determining how many units may tick in
  the current frame.

The engine invokes each unit's state machine **at an interval determined by its
class** (see §3).

---

<a id="3-state-machine-intervals--сабтики-на-классах-юнитов"></a>
## 3. State-Machine Intervals: Sub-Ticks by Unit Class

This is the main source of sub-tick behavior.

<a id="31-базовые-интервалы"></a>
### 3.1 Basic intervals

The constants `gc_statemachine_interval_units = 100` and
`gc_statemachine_interval_peasants = 135` set the real-time interval, in
milliseconds, between state-machine ticks for each class [^3]:

- military units tick **~10 Hz** (10 times per second);
- peasants tick **~7.4 Hz** (about 7 times per second).

A peasant's state machine is therefore updated **less often** than a soldier's,
reducing the cost of simulating a large economy.

### 3.2 Progress sections

Units are divided into progress “sections,” and the engine processes up to
`secmax` objects per tick [^4]. A section is a batch of same-class units that
must be updated within `interval` milliseconds. `cycles` is the number of
progress-loop ticks available before the section's next mandatory update.
These values adapt to current load.

<a id="33-импликации-сабтиков"></a>
### 3.3 Subtik implications

1. **Peasants make decisions less often than soldiers.** Their response to
   finding or losing a resource target is approximately 135 ms, which becomes
   noticeable at high game speed.

2. **Unit order within a section is deterministic** because it follows the
   list, but section boundaries can shift between frames with FPS. At high FPS,
   the engine may process the whole section at once; at low FPS, it divides the
   section into smaller batches.

3. **Under load, different hosts may process different portions of a section
   during one tick.** This can contribute to cross-host divergence, although
   the multiplayer synchronization layer must compensate for it (see §5).

---

<a id="4-периодические-события-mod-n--timed"></a>
## 4. Periodic events (mod-N + timed)
The progress loop triggers subsystems in two ways.

<a id="41-по-счётчику-тиков-progresstick-mod-n"></a>
### 4.1 By tick counter (`progresstick mod N`)

Water pathfinding runs every second tick when
`gProgress.progresstick mod 2 = 0`, if there are water requests [^5]. Network
synchronization of unit parameters via `_misc_SyncUnitsParams` is triggered every
53rd tick [^6].

<a id="42-по-таймштампам-gametime--lasttime"></a>
### 4.2 By time stamps (`gametime > last*time`)

Most periodic subsystems follow this pattern: if game time has passed the
stored timestamp, run the subsystem and advance the timestamp into the future.
All intervals are multiples of `gc_progress_Interval = 0.02` game seconds [^7]:

- `gc_progress_TimeMiscPlSecMax = 200 × 0.02 = 4.0` game-sec
- `gc_progress_TimePoolPlSecMax = 70 × 0.02 = 1.4` game-sec
- `gc_progress_TimeSearchEnemyCounter = 5 × 0.02 = 0.1` game-sec
- `gc_progress_TimeSearchEnemyCountSum = 10 × 0.02 = 0.2` game-sec
- `gc_progress_TimeSearchEnemyCountMid = 50 × 0.02 = 1.0` game-sec
- `gc_progress_TimeProgressStatistics = 10 × 0.02 = 0.2` game-sec
- `gc_progress_TimeProgressTopZones = gc_top_GlobalTick × 0.02`
- `gc_progress_TimeSoundProgressFreq = 0.02`

These `gProgress.last*time` timestamps **are stored in saves** and initialized
through `random` [^8]. Their randomized phase offsets prevent every subsystem
from running in the same frame and causing a CPU spike. Initialization happens
once; afterward the timestamps behave like ordinary state.

---

<a id="5-variable-timestep--адаптивная-скорость"></a>
## 5. Variable timestep + adaptive speed

<a id="51-deltatime--переменный"></a>
### 5.1 Variable `deltatime`

`deltatime` is the amount of game time elapsed since the previous progress-loop
tick and is **not fixed** [^2]:

- at high FPS: `deltatime ~16` ms, each tick is small;
- at low FPS: `deltatime ~30+` ms, each tick is large.

The economy advances through `_res_ProcessEconomy(deltatime)`, so **mine income
per tick is proportional to `deltatime`**. Over the same amount of game time,
mines accumulate the same income regardless of FPS.

<a id="52-адаптивная-скорость-главное"></a>
### 5.2 Adaptive speed (main)

When the CPU cannot process all units in real time, the adaptive-speed
mechanism activates [^9]:

1. Engine calculates real FPS (`realfps`) and performance metrics (`pr`, `pp`,
   `pt`).
2. If `realfps < 20`, `secmax` (the maximum units per tick) decreases.
3. In parallel, `SetTimeSpeedFactor(newspeed)` **reduces game speed
   dynamically**.

The minimum value is `5`, below even `gc_settings_gamespeed_0 = 7`. Under peak
load, the game can therefore slow to 50% of normal speed. Here, `speed` is the
user-selected preset (`gamespeed_0/1/2`), while `newfactor` is a 0–1
coefficient based on how far the simulation falls behind. `cSpeedStepUp` and
`cSpeedStepDown` limit the change to at most 0.667 per pass.

In multiplayer, the server broadcasts the change through
`LanSendParser(gc_LAN_GAME_SYNC_GAMETIME, ...)`, and clients adjust to it.

<a id="53-импликации-для-детерминизма"></a>
### 5.3 Implications for determinism

**In single player:**

- Adaptive speed means that the same minute of real time can contain
  **different amounts of game time** on different machines, producing
  different amounts of wood and mine income.
- This explains why resource output can vary between hosts even with a fixed
  save: host A with a fast CPU might simulate seven game minutes in five real
  minutes, while host B simulates only 6.5. The difference in game time changes
  the amount gathered.

**In multiplayer:**

- The server broadcasts `SetTimeSpeedFactor`, giving all hosts the same
  game-time-to-real-time ratio.
- But the “section” (which units are processed in which tick) on different hosts can
  vary because `secmax` is also adjusted locally.

**Same host, different launches of the same save:**

- Adaptive speed depends on current system load, including background
  processes and GPU activity. Even on the same machine,
  `SetTimeSpeedFactor` can therefore change at different moments in separate
  runs, producing different amounts of game time over the same real-time
  interval.

---

<a id="6-save--load--что-нормализуется-что-теряется"></a>
## 6. Save/Load: Preserved and Lost State

<a id="61-хуки"></a>
### 6.1 Hooks

| State machine | OnBeforeSave | OnAfterLoad |
|---|---|---|
| Progress | `SwitchTo('Nothing')` | `SwitchTo('Nothing')` |
| Unit (peasant) | `SwitchTo('Nothing')` | `SwitchTo('Nothing')` (+ ship children for water units) |
| Environment resource | — (default) | `ExecuteState('Initial'); SwitchTo('Nothing')` |

The corresponding hook files are [^10].

<a id="62-что-точно-сохраняется"></a>
### 6.2 State that is saved

From the network sync format (aka save) [^11]:

- `posx`, `posz` (`Float` sub-cell position);
- `upx, upy, upz, dirx, diry, dirz` (orientation);
- `statestag` (state-tag bitmask);
- `sto` (target handle);
- `stpx, stpz, sta` (state target position and arrow angle);
- `cid, id, pl, hp, bbuilt, bdead, buildprogress`;
- **`uniqrnd`** (per-unit nonce, see [determinism_audit.md](determinism_audit.md)).

From `gProgress` (type `TProgress`) [^12]:

- `lastprogresstime`, `progresstick` — tick counter and last tick time;
- all `last*time` for periodic events.

From per-unit `TObj` [^13]:

- `lastprogresstime`, `progresstick`, `soundlastprogresstime`,
  `soundprogresstick`, `soundcounterlastprogresstime`,
  `soundcounterprogresstick` — progress counters for the unit itself.

<a id="63-что-не-сохраняется-или-сбрасывается"></a>
### 6.3 State that is not saved or is reset

- **Current animation phase** — `OnBeforeSave` calls `SwitchTo('Nothing')`,
  which breaks the current animation loop. After loading, the peasant begins
  animation from the zero phase (or from the one selected by the engine).
- **In-flight pathfinding state** — the current position in the track-point list
  and interpolation phase between points. After loading, the peasant is placed
  at the saved position and receives a new path.
- **Global `random` state** — almost certainly absent from the save format.
  After loading, `random` resumes from a different state.
- **Position within progress-section traversal** — the section restarts after
  loading.
- **Current load and FPS history** (`garrfloat_perf_progress`) — a global array
  of recent performance metrics. It is filled again after loading, so adaptive
  speed can begin from a different `TimeSpeedFactor`.

<a id="64-каскад-на-load"></a>
### 6.4 Cascade on Load

1. Engine reads fields `gProgress` (including `lastprogresstime`, `progresstick`).
2. A hook resets all units to `'Nothing'`, losing the animation phase.
3. All resources are reset `Initial → Nothing` through the hook.
4. `garrfloat_perf_progress` is reset to zero, so adaptive speed starts from its
   default state.
5. Global `random` starts from whatever state the engine considers
   appropriate; there is no indication that it is serialized.
6. On the first tick after loading, `deltatime = 0` because
   `lastprogresstime = gametime`. The `if deltatime > 0` branch therefore does
   not run. Normal processing begins on the
   second tick.

---

<a id="7-sub-tick-state--что-это-и-почему-важно"></a>
## 7. Sub-Tick State: Definition and Significance

“Sub-tick state” is state that **changes within one logical tick** or between
ticks of a unit's state machine, but is not preserved at save/load granularity.

<a id="71-примеры-sub-tick-state-у-крестьянина"></a>
### 7.1 Examples of sub-tick state of a peasant

| State | Stored in | Restored on load? |
|---|---|---|
| Animation phase `workwood` / `workfood` / `walkwood` | engine animation system | NO - `SwitchTo('Nothing')` resets |
| Sub-tile position interpolation when walking | engine track-point system | Partially—the position is saved, but the interpolation phase is lost |
| Current unit `progresstick` | `TObj.progresstick` | YES—the field is saved |
| `lastprogresstime` unit | `TObj.lastprogresstime` | YES |
| `standtime` (time spent idle) | `TObj.standtime` | YES (probably in `TObj`) [^13] |
| Active order (target, type) | `TObj.orders[]` | YES |
| `restype`, `resamount` (what it carries now) | `TObj.*` | YES |
| Current resource target | `TObj.sto` | YES (the handle is saved) |

<a id="72-где-sub-tick-state-создаёт-расхождение"></a>
### 7.2 How sub-tick state creates divergence

After loading, every sub-tick field is **either restored** or **reset to a
neutral value**. That still creates timing differences:

1. Resetting the animation makes the peasant begin a **new work cycle at phase
   0**, even if the pre-save phase was 0.7. The **first strike after loading
   therefore occurs later** than it would have in an uninterrupted simulation.

2. The offset cascades: a later first delivery leads to a later target search,
   a different `progresstick mod 53` synchronization phase, and potentially a
   different tree selected through `random` (see
   [determinism_audit.md](determinism_audit.md) §3).

3. Reset pathfinding creates a new topology request. Pathfinder tie-breaking
   may then choose a different route to the same tree.

Each of the discrepancies is small in itself, but they accumulate over the course of
minutes of simulation until the production difference becomes noticeable.

---

<a id="8-сводная-картина-почему-симуляция-расходится"></a>
## 8. Why the Simulation Diverges

<a id="81-причины-на-одном-хосте-разные-запуски-одного-сейва"></a>
### 8.1 Reasons **on the same host**, different launches of the same save

| Source | Influence |
|---|---|
| Animation phases reset, shifting the first strike | Cascading timing changes |
| Pathfinding tie-breaking gives different paths to the same tree | Different arrival times |
| Global `random` state varies between runs | Different outcomes at seven RNG sites in resource gathering ([determinism_audit.md](determinism_audit.md) §3) |
| Adaptive speed depends on current system load | Different amounts of game time over the same real-time interval |
| Progress-section traversal restarts | Units begin with a fresh batch boundary |

<a id="82-дополнительные-причины-между-хостами"></a>
### 8.2 Additional reasons **between hosts**

| Source | Influence |
|---|---|
| Different CPU → different `realfps` → different `TimeSpeedFactor` (single-player) | Different amounts of game time per minute of real time |
| Different Float serialization between x87/SSE/FMA | Micro-discrepancies in physics and geometry |
| Different initialization `random` for `gProgress.last*time`, if the game starts from scratch (not Load) | Different phase of periodic events |

<a id="83-что-детерминировано-при-save--load"></a>
### 8.3 Deterministic state across save/load

- HP of all resources and units (integers).
- Integer player resources.
- `uniqrnd`, `progresstick`, and all `last*time` fields.
- Mine income: `produce_rate × N_workers × deltatime`. If accumulated
  `deltatime` is the same between runs—as it approximately is with stable
  FPS—the result is the same.

---

<a id="9-связь-с-моделью-добычи"></a>
## 9. Relationship to the Resource-Gathering Model

**The analytical model** in
[peasant_extraction.md](../../docs_en/recon/world/economy/peasant_extraction.md)
uses **game time**, not real time. This is appropriate because its formulas are
invariant under game-speed changes.

**Players**, however, usually compare resource totals over a **real-time
window**, such as five minutes. The relationship is:
```
real_time × (TimeSpeedFactor / 10) = game_time
```
If host A maintains `TimeSpeedFactor = 14` throughout a fast-speed test, five
real minutes equal seven game minutes. If adaptive speed reduces the factor to
12, five real minutes equal six game minutes, yielding **15% less production**
from otherwise identical simulation logic.

**Implication:** When calibrating a model empirically, you need to either:

- (a) measure game time, perhaps through a replay with a known duration;
- (b) measure FPS through a game profiler and calculate the effective speed factor;
- (c) run short tests of roughly one minute on a lightweight map with few
  units, so adaptive slowdown does not activate.

---

## 10. Cross-references

- [determinism_audit.md](determinism_audit.md) — RNG sites in resource gathering and combat.
  This document refers to §6 (save/load) and §5 (adaptive speed) for
  explanations of the mechanism of nondeterminism.
- [peasant_extraction.md](../../docs_en/recon/world/economy/peasant_extraction.md)
  models gathering in game time; §1 of this document converts between game time
  and real time while accounting for adaptive speed.
- [building_mechanics.md](../../docs_en/recon/world/economy/building_mechanics.md) — `buildtime` in
  frames, `deltatime` for construction.

---

<a id="источники"></a>
## Sources

All links are relative to `data/scripts/` in the Cossacks 3 installation.

[^1]: Game-speed presets — `dmscript.global:1027-1029`:
    ```pascal
    gc_settings_gamespeed_0 = 7;     // slow
    gc_settings_gamespeed_1 = 10;    // normal
    gc_settings_gamespeed_2 = 14;    // fast
    ```
[^2]: Structure of one progress-loop tick - `progress/progress.inc/nothing.inc:71-759`:
    ```pascal
    var lastprogresstime : Float = gProgress.lastprogresstime;
    var gametime : Float = GetGameTime;
    var deltatime : Float = gametime - lastprogresstime;

    if (lastprogresstime>0) and (deltatime>0) then  // not on pause
    begin
       var perffps : Float = GetProgressPlayersPerformance;
       perffps := MinFloat(perffps, 1/FramesPerSecond);
       var cycletime : Float = perffps*(GetTimeSpeedFactor/10);

       _res_ProcessEconomy(deltatime);  // mines, fields regeneration

       // ... pathfinding for all units in gWaterPathList / gGOPathList ...
       // ... periodic events by timeouts (see section 4) ...
       // ... game-speed adaptation by real FPS (see section 5) ...
    end;

    if (lastprogresstime>0) and (deltatime>0) then
       gProgress.progresstick := gProgress.progresstick + 1;
    gProgress.lastprogresstime := gametime;
    ```
[^3]: State machine basic intervals - `dmscript.global:1458-1459`:
    ```pascal
    gc_statemachine_interval_units = 100;       // ms — military units
    gc_statemachine_interval_peasants = 135;    // ms — peasants
    ```

[^4]: Progress sections — `progress/progress.inc/nothing.inc:475-498`:
    ```pascal
    var psind : Integer = GetPlayerProgressSectionIndexByInterval(plHnd, gc_statemachine_interval_peasants);
    peacount := GetPlayerProgressSectionCountGOByIndex(plHnd, psind);
    // ...
    psind := GetPlayerProgressSectionIndexByInterval(plHnd, gc_statemachine_interval_units);
    warcount := GetPlayerProgressSectionCountGOByIndex(plHnd, psind);

    psgocount := Max(peacount, warcount);
    secmax := _misc_RoundUp(psgocount/cycles);    // target: process all in `cycles` ticks
    secmax := Max(50, Min(psgocount, secmax));
    ```
[^5]: Pathfinding for water every second tick - `progress/progress.inc/nothing.inc:117`:
    ```pascal
    if (gWaterPathList.GetCount>0) and ((gGOPathList.GetCount=0) or (gProgress.progresstick mod 2=0)) then
    ```
[^6]: Network synchronization of unit parameters every 53rd tick - `progress/progress.inc/nothing.inc:405`:
    ```pascal
    if ((gProgress.progresstick mod 53)=0) and ... then
       _misc_SyncUnitsParams;
    ```
[^7]: Base step and periodic event intervals - `dmscript.global:1489-1498`:
    ```pascal
    gc_progress_Interval               = 0.02;       // base step (50 Hz)
    gc_progress_TimeMiscPlSecMax       = 200 * 0.02;
    gc_progress_TimePoolPlSecMax       = 70  * 0.02;
    gc_progress_TimeSearchEnemyCounter = 5   * 0.02;
    gc_progress_TimeSearchEnemyCountSum= 10  * 0.02;
    gc_progress_TimeSearchEnemyCountMid= 50  * 0.02;
    gc_progress_TimeProgressStatistics = 10  * 0.02;
    gc_progress_TimeProgressTopZones   = (gc_top_GlobalTick * 0.02);
    gc_progress_TimeSoundProgressFreq  = 0.02;
    ```
Example of applying an interval to `lastmiscplsecmaxtime`:
    ```pascal
    if gametime > gProgress.lastmiscplsecmaxtime then
    begin
       gProgress.lastmiscplsecmaxtime := gametime + gc_progress_TimeMiscPlSecMax;
       // ... subsystem code ...
    end;
    ```
[^8]: Initializing timestamps via `random` - `miscext.script:1891-1898`:
    ```pascal
    gProgress.lastprogresshistorytime := random;
    gProgress.lastmiscplsecmaxtime := random*gc_progress_TimeMiscPlSecMax;
    // ...
    ```
[^9]: Adaptive speed - `progress/progress.inc/nothing.inc:510-628`:
    ```pascal
    var newspeed : Float = speed*(1-newfactor);
    newspeed := Clamp(newspeed, 5, gc_settings_gamespeed_2);
    // ...
    SetTimeSpeedFactor(newspeed);
    ```
[^10]: Save/Load hooks - `progress/progress.inc/{onbeforesave,onafterload,initial}.inc`, `units/unit.inc/{onbeforesave,onafterload}.inc`, `env/env.inc/onafterload.inc`.

[^11]: Network sync format (aka save) - `miscext2.script:4002-4027`. Includes `posx`, `posz`, orientation, `statestag`, `sto`, `stpx`, `stpz`, `sta`, `cid`, `id`, `pl`, `hp`, `bbuilt`, `bdead`, `buildprogress`, `uniqrnd`.

[^12]: Structure `TProgress` - `classes.script:6011`. Contains `lastprogresstime`, `progresstick` and all `last*time` for periodic events.

[^13]: Unit progress fields in `TObj` - `classes.script:36-41, 3704+`. Includes `lastprogresstime`, `progresstick`, `soundlastprogresstime`, `soundprogresstick`, `soundcounterlastprogresstime`, `soundcounterprogresstick`.
