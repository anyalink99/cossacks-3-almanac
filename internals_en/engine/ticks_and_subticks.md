# Recon: ticks, subtics, time

Time model in Cossacks 3: main progress-loop, sub-tick intervals
state-machine, variable time step, adaptive game speed. This is the base
to understand why the simulation doesn't play even on the same host after
Save/Load and why different machines diverge. All links to the code themselves
Pascal blocks are collected in the [Sources](#sources) section at the end of the document.

**Related documents:**

- [determinism_audit.md](determinism_audit.md) - RNG sites in mining and
  battle; this document describes **when** they are called.
- [server_sync_architecture.md](server_sync_architecture.md) - how
  server-authoritative architecture is related to ticks; sync packages in
  real-time versus game-time logic.

## TL;DR

- **three time scales** coexist in the code: real time (wall seconds),
  game time (logical simulation time, scaled by `TimeSpeedFactor`)
  and frames (animation frames; 32 frames = 1 game-second).
- Main progress-loop ticks every **20ms** real time
  (`gc_progress_Interval = 0.02`). Inside - distribution of pathfinding requests,
  periodic events, economics, game speed adaptation.
- Units tick **not every frame**, but once at their own interval: military -
  100 ms, peasants - 135 ms (`gc_statemachine_interval_*`).
- On Save / Load, some of the timestamps `gProgress.last*time` ** are not
  is restored accurately** - subsystems may miss a tick or
  get two in a row. This is one source of non-recursivity.

---

## 1. Three time scales

Three different “times” coexist in the code:

| Scale | What | Where |
|---|---|---|
| **Real time** | Wall seconds | `_misc_GetRealTime`, `GetCurrentTime` |
| **Game time** | Logical simulation time, scaled by `TimeSpeedFactor` | `GetGameTime`, designated `gametime` |
| **Frames** | Discrete frames of animations and timings in scripts | `gc_time_to_frames = 32` |

**Key Relationships:**
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

This is the lobby option `gMap.settings.additional.gamespeed`. Table of all speeds -
[`reports/map/lobby_settings.md`](../../docs_en/reports/map/lobby_settings.md#gamespeed--скорость-партии);
behavior decoding - [`game_settings.md`](../../docs_en/recon/world/map/game_settings.md) §3.6.

All durations in scripts (animations, `buildtime`, `attackpause`) - in
**frames**. Translation into game-seconds: `frames / 32`. Conversion to real-seconds:
additionally divide by `TimeSpeedFactor/10`.

---

## 2. Main progress-loop

The heart of the simulation lives in `progress/progress.inc/nothing.inc` (745 lines). This
The “progress” state machine is a separate “player” in the Cossacks 3 architecture, which
ticks every time the engine calls state `Nothing`.

### 2.1 Single tick structure

In one tick progress-loop reads `gametime`, considers `deltatime` relative
last tick and, if the game is not paused, executes a full set of subsystems:
economy accrual via `_res_ProcessEconomy(deltatime)`, distribution
pathfinding queries from `gWaterPathList` and `gGOPathList`, processing
periodic events according to timestamps and adaptation of game speed according to real
FPS At the end of the tick, `gProgress.progresstick` is incremented and
`gProgress.lastprogresstime` is updated to the current `gametime` [^2].

### 2.2 What progress-loop does NOT do

It **doesn't tick every unit** directly. Units are separate state machines with
own cycles `Nothing`. Progress-loop:

- starts the economy (`_res_ProcessEconomy(deltatime)`);
- distributes pathfinding requests;
- pushes periodic events;
- manages progress sections (see §3) - determines how many units *has
  right* to tick in this frame.

Units tick themselves when the engine calls them through the state machine, **at intervals,
depending on their class** (see §3).

---

## 3. State-machine intervals - subtics on unit classes

Here is the main mechanism of sub-tick behavior.

### 3.1 Basic intervals

Constants `gc_statemachine_interval_units = 100` and
`gc_statemachine_interval_peasants = 135` set real milliseconds
time between state machine ticks for a unit of this class [^3]:

- military units tick **~10 Hz** (10 times per second);
- peasants tick **~7.4 Hz** (about 7 times per second).

That is, the peasant receives an update to his state machine **less often** than
soldier. This is the economy of massive economic simulations.

### 3.2 Progress sections

Not all units tick every frame - they are broken up into "sections" and the engine goes through
by `secmax` objects per tick [^4]. Section - a batch of units of the same class, which
must be "updated" within `interval` ms. `cycles` — how many ticks
progress-loop will be in time before the next mandatory section update. These numbers
adapt to actual load.

### 3.3 Subtik implications

1. **Peasants make decisions less often than soldiers.** Reaction time to “found /
   lost resource" is about 135 ms, which is noticeable at high speed
   games.

2. **The order of ticks of units in a section is deterministic** (by list), but the boundaries
   sections can be shifted between frames depending on FPS. At high FPS
   all units tick every time, on low - the section is cut into pieces.

3. **Under load (thousands of units), different hosts with different FPS receive different
   "chunks" of a section in one tick.** This is a potential source of inter-host
   out of sync, but in lockstep multiplayer it must be compensated (see §5).

---

## 4. Periodic events (mod-N + timed)
Inside the progress-loop, different subsystems are triggered according to two patterns.

<a id="41-по-счётчику-тиков-progresstick-mod-n"></a>
### 4.1 By tick counter (`progresstick mod N`)

Pathfinding for water is executed every second tick: the condition is checked
`gProgress.progresstick mod 2 = 0`, if there are water requests [^5]. Network
synchronization of unit parameters via `_misc_SyncUnitsParams` is triggered every
53rd tick [^6].

<a id="42-по-таймштампам-gametime--lasttime"></a>
### 4.2 By time stamps (`gametime > last*time`)

Most periodic subsystems work according to the scheme “if the game time
exceeded the last time stamp - execute and reset the time stamp to
the future." All intervals are specified as multipliers from `gc_progress_Interval = 0.02`
game-sec [^7]:

- `gc_progress_TimeMiscPlSecMax = 200 × 0.02 = 4.0` game-sec
- `gc_progress_TimePoolPlSecMax = 70 × 0.02 = 1.4` game-sec
- `gc_progress_TimeSearchEnemyCounter = 5 × 0.02 = 0.1` game-sec
- `gc_progress_TimeSearchEnemyCountSum = 10 × 0.02 = 0.2` game-sec
- `gc_progress_TimeSearchEnemyCountMid = 50 × 0.02 = 1.0` game-sec
- `gc_progress_TimeProgressStatistics = 10 × 0.02 = 0.2` game-sec
- `gc_progress_TimeProgressTopZones = gc_top_GlobalTick × 0.02`
- `gc_progress_TimeSoundProgressFreq = 0.02`

These timestamps (`gProgress.last*time`) **are saved in save** and
are initialized via `random` [^8] - to **separate in phase** different
subsystems and avoid a CPU spike if they all ticked in the same frame.
`random` is used (not `RandomExt`), but these initializations occur alone
once and then they simply experience it as a normal state.

---

<a id="5-variable-timestep--адаптивная-скорость"></a>
## 5. Variable timestep + adaptive speed

<a id="51-deltatime--переменный"></a>
### 5.1 deltatime - variable

The variable `deltatime` is equal to the real game time elapsed since
past progress-loop tick, and **not fixed** [^2]:

- at high FPS: `deltatime ~16` ms, each tick is small;
- at low FPS: `deltatime ~30+` ms, each tick is large.

The economy is ticking through `_res_ProcessEconomy(deltatime)` - that is, **income
mines per tick is proportional to `deltatime`**. The mines give the same
accumulated income in game-seconds regardless of FPS, because the total
`gametime` is deterministic for game speed × wall time.

<a id="52-адаптивная-скорость-главное"></a>
### 5.2 Adaptive speed (main)

When the CPU does not have time to process all units in real time, it triggers
key mechanism [^9]:

1. Engine calculates real FPS (`realfps`) and performance metrics (`pr`, `pp`,
   `pt`).
2. If `realfps < 20`, `secmax` (max. units per tick) decreases.
3. In parallel, `SetTimeSpeedFactor(newspeed)` is called - **decrease in game
   speed dynamic**.

The minimum limit is `5` (even lower than `gc_settings_gamespeed_0 = 7`). That is
under peak load the game **slows down to 50% of slow**. Here `speed`
— user-set speed (`gamespeed_0/1/2`), `newfactor` —
coefficient 0..1 depending on how much the simulation “falls short”.
The change step is limited by the constants `cSpeedStepUp` and `cSpeedStepDown` (together
no more than 0.667 per pass).

In multiplayer, the server sends out the change via
`LanSendParser(gc_LAN_GAME_SYNC_GAMETIME, ...)` - all clients are adjusted.

<a id="53-импликации-для-детерминизма"></a>
### 5.3 Implications for determinism

**In single player:**

- Adaptive speed means that on different machines the same real
  minute gives **different past game-time**. Different trees were cut down, different
  the mines have been dug.
- This explains the observation “the production varies between hosts”: even with a fixed
  save, host A with a fast CPU passed the conditional 7 game-min in 5 real-min,
  host B with slow - 6.5 game-min. The difference in game-time gives different loot.

**In multiplayer:**

- Server sends out `SetTimeSpeedFactor` - all hosts receive the same
game-time-per-real-time.
- But the “section” (which units are processed in which tick) on different hosts can
  vary because `secmax` is also adjusted locally.

**Same host, different launches of the same save:**

- Adaptive speed depends on the current system load (background
  processes, GPU, etc.). This means that even on the same machine between two
  launches `SetTimeSpeedFactor` can work at different moments, giving
  different amount of game-time for equal real-time.

---

<a id="6-save--load--что-нормализуется-что-теряется"></a>
## 6. Save / Load - what is normalized, what is lost

<a id="61-хуки"></a>
### 6.1 Hooks

| State machine | OnBeforeSave | OnAfterLoad |
|---|---|---|
| Progress | `SwitchTo('Nothing')` | `SwitchTo('Nothing')` |
| Unit (peasant) | `SwitchTo('Nothing')` | `SwitchTo('Nothing')` (+ ship childs if aquatic) |
| Env(resource) | — (default) | `ExecuteState('Initial'); SwitchTo('Nothing')` |

The corresponding hook files are [^10].

<a id="62-что-точно-сохраняется"></a>
### 6.2 What exactly is saved

From the network sync format (aka save) [^11]:

- `posx`, `posz` (Float - sub-cell position);
- `upx, upy, upz, dirx, diry, dirz` (orientation);
- `statestag` (bit status of tags);
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
### 6.3 What is NOT saved (or reset)

- **Current animation phase** - `OnBeforeSave` calls `SwitchTo('Nothing')`,
  which breaks the current animation loop. After Load the peasant begins
  animation from the zero phase (or from the one selected by the engine).
- **In-flight pathfinding state** — current position in the track-point list, phase
  interpolation between trackpoints. After Load the peasant stands in a position from
  save and it is given a new path.
- **Global state `random`** - almost certainly NOT saved in save
  format. After Load `random` starts “from a new place”.
- **Position in the progress section bypass** - after Load, the section starts anew.
- **Current load / FPS history** (`garrfloat_perf_progress`) - global
  an array of current perf metrics. After Load is filled again, and adaptive
  speed can start from another `TimeSpeedFactor`.

<a id="64-каскад-на-load"></a>
### 6.4 Cascade on Load

1. Engine reads fields `gProgress` (including `lastprogresstime`, `progresstick`).
2. All units are reset to `'Nothing'` via a hook - the animation phase is lost.
3. All resources are reset `Initial → Nothing` through the hook.
4. `garrfloat_perf_progress` is reset to zero - adaptive speed starts from default.
5. Global `random` starts from the state that the engine considers
   appropriate (no indication that it is being serialized).
6. First tick after Load: `deltatime = 0` (because
   `lastprogresstime = gametime` immediately after Load), which means a cycle
   `if deltatime > 0` will not work; transition to the second tick with standard
   `deltatime`.

---

<a id="7-sub-tick-state--что-это-и-почему-важно"></a>
## 7. Sub-tick state - what is it and why is it important

“Sub-tick state” is a state that **changes within one logical
tick** or between ticks of the state machine of a specific unit, but does not persist
on save/load granularity.

<a id="71-примеры-sub-tick-state-у-крестьянина"></a>
### 7.1 Examples of sub-tick state of a peasant

| State | Where does he live | Recovered on Load? |
|---|---|---|
| Animation phase `workwood` / `workfood` / `walkwood` | engine animation system | NO - `SwitchTo('Nothing')` resets |
| Sub-tile position interpolation when walking | engine track-point system | Partially - the position is saved, but the interpolation phase is lost |
| Current unit `progresstick` | `TObj.progresstick` | YES - the field is saved |
| `lastprogresstime` unit | `TObj.lastprogresstime` | YES |
| `standtime` (how much does it cost without work) | `TObj.standtime` | YES (probably in `TObj`) [^13] |
| Active order (target, type) | `TObj.orders[]` | YES |
| `restype`, `resamount` (what it carries now) | `TObj.*` | YES |
| Current Resource Purpose | `TObj.sto` | YES (handle is saved) |

### 7.2 Where sub-tick state creates divergence

After Load, all sub-tick fields are **either restored** or **reset to
neutral**. Everything seems to be fine. But:

1. The animation is reset - the peasant begins a **new work-cycle with phase 0**,
   whereas before the save he could have had a phase of 0.7. So, **the first blow after
   Load occurs later than it would have in that simulation**.

2. This offset cascades: first resource delivery later - next search
   tree at a different game-time - ends up in a different phase
   `progresstick mod 53`-synchronization - another tree selection is possible via
   `random` (see [determinism_audit.md](determinism_audit.md) §3).

3. Pathfinding reset - new request to topology - tie-breaking in pathfinder
   - perhaps another path to the same tree.

Each of the discrepancies is small in itself, but they accumulate over the course of
minutes of simulation** until there is a noticeable difference in production.

---

## 8. The big picture: why the simulation diverges

### 8.1 Reasons **on the same host**, different launches of the same save

| Source | Influence |
|---|---|
| Animation phases are reset - first hit is phase shifted | Cascade in timing |
| Pathfinding tie-breaking gives different paths to the same tree | Different arrival times |
| Global status `random` varies between runs | Different outcomes of 7 RNG sites in mining ([determinism_audit.md](determinism_audit.md) §3) |
| Adaptive speed depends on the current system load | Different real game-time for equal real-time |
| Progress section batch boundary starts from scratch | Units first tick with a “fresh pack” |

### 8.2 Additional reasons **between hosts**

| Source | Influence |
|---|---|
| Different CPU - different `realfps` - different `TimeSpeedFactor` (single player) | Miscellaneous game-time per minute real-time |
| Different Float serialization between x87/SSE/FMA | Micro-discrepancies in physics and geometry |
| Different initialization `random` for `gProgress.last*time`, if the game starts from scratch (not Load) | Different phase of periodic events |

### 8.3 What is deterministic during Save / Load

- HP of all resources and units (integers).
- Integer player resources.
- `uniqrnd`, `progresstick`, all `last*time` (obviously persistent).
- Mine: `produce_rate × N_workers × deltatime` - arithmetic. If the amount
  `deltatime` per window is the same between runs (and it is approximately the same
  with stable FPS), the result is the same.

---

## 9. Link to the mining model

**In the analytical model** (see.
[peasant_extraction.md](../../docs_en/recon/world/economy/peasant_extraction.md)) we consider **in
game-time**, not real-time. This is the correct approach - the formulas are invariant to
game speed.

**But** the real player compares the loot **in a real-time window** (for example,
"5 real-min") Connection:
```
real_time × (TimeSpeedFactor / 10) = game_time
```
If on host A `TimeSpeedFactor = 14` (declared fast) **supported
strictly**, then 5 real-min = 7 game-min. If adaptive speed has reduced it to 12,
then 5 real-min = 6 game-min - **15% less production** with identical
simulations.

**Implication:** When calibrating a model empirically, you need to either:

- (a) use game-time for measurements (but the game shows real-time in
  UI; perhaps through replay with a known duration);
- (b) measure FPS through a game profiler and calculate the effective speed factor;
- (c) run short tests (a minute) on a light card with a small number
  units so that adaptive speed does not work.

---

## 10. Cross-references

- [determinism_audit.md](determinism_audit.md) - RNG sites in mining and combat.
  This document refers to §6 (save/load) and §5 (adaptive speed) for
  explanations of the mechanism of nondeterminism.
- [peasant_extraction.md](../../docs_en/recon/world/economy/peasant_extraction.md) - extraction model in
  game-time §1 of this document is supplemented by the translation game-time ↔ real-time with
  taking into account adaptive speed.
- [building_mechanics.md](../../docs_en/recon/world/economy/building_mechanics.md) — `buildtime` in
  frames, `deltatime` for construction.

---

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
Template for applying intervals - for example, for `lastmiscplsecmaxtime`:
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
