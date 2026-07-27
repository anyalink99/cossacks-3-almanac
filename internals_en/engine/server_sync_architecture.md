<a id="recon-серверная-архитектура-и-сетевая-синхронизация"></a>
# Recon: Server Architecture and Network Synchronization

This document describes C3's network synchronization model: which host runs the
simulation, what data travels over the network and when, and how synchronization
interacts with ticks and `random`. It complements
[determinism_audit.md](determinism_audit.md) (RNG sites) and
[ticks_and_subticks.md](ticks_and_subticks.md) (time model). This layer explains
why synchronizing adaptive speed across hosts still does not make separate
simulations reproducible.

All script paths below are relative to `data/` in the Cossacks 3 installation.
Code references and Pascal excerpts are collected in [Sources](#sources).

## TL;DR

- **C3 is server-authoritative, not lockstep.** One host (the server) runs
  all game logic; clients and replay playback merely display the result.
- Throughout the code, the pattern
  `if not (_net_IsClient or _net_IsReplay) then …` keeps game logic on the
  server [^1].
- Synchronization packets are sent either per event (for example, one trade or
  one capture) or periodically (`_misc_SyncUnitsParams` runs once every 53
  progress ticks).
- Hosts therefore do **not** need to run deterministic simulations. Unlike a
  lockstep model, C3 does not try to keep every host's `random()` sequence in
  sync with a shared seed.

---

<a id="1-главное-c3--server-authoritative-не-lockstep"></a>
## 1. Core Model: C3 Is Server-Authoritative, **Not** Lockstep

<a id="11-что-это-значит"></a>
### 1.1 What this means

In a classic lockstep RTS (such as StarCraft or Age of Empires II), **all hosts
run an identical simulation** from the same PRNG seed and synchronize
only player commands. Every RNG call produces the same result on every host
because the input states are identical.

C3 works **differently**: one host (the server) runs the simulation, while the
others (clients) **only display** the state sent to them. This is visible in
a fundamental pattern that occurs dozens of times in the code:
game-logic blocks use `if (bProcess) then …`, where `bProcess` is
defined as `not (_net_IsClient or _net_IsReplay)` [^1].

Clients and replay playback **do not run game logic**. They receive packets from
the server or replay stream and apply the changes locally. This pattern occurs in
handlers for resource extraction, damage, construction progress and
in many other hooks [^2].

### 1.2 Net modes

Five network modes [^3]:

| Mode | Condition | Role |
|---|---|---|
| `_net_IsOffline` | `GetLanMode = 0` (single player) | Local simulation (effectively its own server) |
| `_net_IsServer` | `GetLanMode > gc_lanmode_client` | This host |
| `_net_IsClient` | `GetLanMode = gc_lanmode_client` | Receives from the server |
| `_net_IsRecord` | `GetRecordManagerGameMode = 2` | Runs locally and records a replay |
| `_net_IsReplay` | `GetRecordManagerGameMode = 1` | Receives events from a replay file |

In single-player, `_net_IsOffline` makes the local process its own server, so
`bProcess` is always true.

<a id="13-архитектурные-следствия"></a>
### 1.3 Architectural implications

- **Why `random` is seeded through `SetRandomKey(uniqrnd*MaxInt)`** [^4]:
  so that the client can **reproduce** projectile dispersion from the same seed.
  The server sends `frnd : Float = RandomExt` → the client applies
  `SetRandomKey` with the value restored from this `frnd`, and
  gets identical variance.

- **Why `random` without `SetRandomKey` is not critical for inter-host
  synchronization**: its result is used only on the server (under
  `bProcess`). Clients do not execute this branch. The source comment says that
  the general RNG does not need synchronization, while `RandomExt` could change
  the intended result on different PCs [^5]. The developers therefore use the
  non-reproducible general RNG only where cross-host synchronization is
  unnecessary.

---

<a id="2-что-синхронизируется-и-как"></a>
## 2. What Is Synchronized and How
<a id="21-per-event-пакеты-отправляются-по-факту-события"></a>
### 2.1 Per-event packages (sent upon event)

Each player game object (the player state machine) has paired
`WriteX` / `ReadX` for each event type. In the global catalog
there are more than thirty such handler pairs:

| Event | Write* | Read* | Payload |
|---|---|---|---|
| Unit creation | writenew.inc | readnew.inc | uid, race/base, pos, cid |
| Destruction | writefree.inc | readfree.inc | uid |
| Death | writedeath.inc | readdeath.inc | uid |
| Move command | writemove.inc | readmove.inc | uid, target pos |
| Order | writeorder.inc | readorder.inc | uid, order type, target |
| Search for a resource | writesearch.inc | readsearch.inc | — |
| Projectile | writeproj.inc | readproj.inc | uid, weapon, **frnd** for variance sync |
| Apply an upgrade | writeapply.inc | readapply.inc | uid, upgrade |
| Construction progress | writeconstruct.inc | readconstruct.inc | uid, hp delta |
| ...~25 more events | | | |

The creation-handler template works as follows [^6]: the server creates the
object locally through `CreatePlayerGameObjectHandleByHandle`, obtains its
local uid, and sends that uid to clients in a packet. Clients create local
objects with **the same uid** (using the uid-to-handle table) and apply the
received parameters.
This preserves the consistency of links between hosts.

<a id="22-periodic-пакеты-по-таймауту"></a>
### 2.2 Periodic packets (by timeout)

The main progress loop checks three timers on every tick [^7]:

| What | Period | Scale |
|---|---|---|
| `WriteRes` (player's current resource supply) | 0.1 sec | **real time** |
| `WriteLanSyncData` (general sync block) | 0.1 sec | **real time** |
| `WriteStats` (counters) | 20 sec | **real time** |

**Important:** these periods use **real time**. This means:
- At fast (×1.4) speed, the 0.1 real seconds between two `WriteRes` calls
  contain approximately 0.14 game seconds.
- At slow (×0.7) speed, they contain 0.07 game seconds.
- At an adaptive slowdown to 5/10 = 0.5× — 0.05 game seconds.

Accordingly, **packet frequency remains constant in real time at different
speeds**, which is good for network throughput, but bad for
reproducibility of game logic.

<a id="23-sync-unit-params-mod-53"></a>
### 2.3 Sync unit parameters (mod 53)

Once every 53 progress ticks, the server calls `_misc_SyncUnitsParams` [^8].
It takes units from `gLanSyncUnitsParamsUIDList` (objects that the server
marked as "needing sync", usually after non-trivial changes)
and sends their status via `WriteSyncUnitsParams` [^9].

**Period:** every 53rd progress tick. Tick frequency depends on FPS (see
[ticks_and_subticks.md](ticks_and_subticks.md) §5). At 50 Hz tick this
is approximately 1.06 seconds of real time. Unit-parameter synchronization can
therefore lag by about one second.

### 2.4 GameTime/speed sync

**Server only** (external condition `_net_IsServer`) changes
`TimeSpeedFactor`. The server sends a packet with a pair (`GetGameTime`,
`newspeed`) via `LanSendParser(gc_LAN_GAME_SYNC_GAMETIME, …)` [^10].
Clients use this to synchronize **game time progression**.

A packet is sent only when `newspeed <> GetTimeSpeedFactor`, that is, when the
speed actually changes. No packets are sent between changes; clients continue
ticking at the last received speed.

### 2.5 On-demand full sync

When the game suspects a desynchronization, it performs an expensive full-state
synchronization:

1. The client sends `gc_LAN_GAME_SYNC_REQUEST` with three `(cuid, nuid, envc)`
   (uid counters) [^11].
2. The server runs `_misc_WriteSyncServer` and sends the **full state of every
   unit** [^12]: for each uid, `bexists`, and (if the object
   exists) `racename`, `basename`, `posx/z`, `scale`, orientation,
   `statestag`, `sto`, `stp`, `sta`, `cid`, `id`, `pl`, `hp`, `bbuilt`,
   `bdead`, `buildprogress`, **`uniqrnd`**.
3. In `_misc_ReadSyncClient`, the client recreates missing objects or restores
   the state of existing ones [^13].

This is a “hard reset”: an expensive operation used only when consistency is
lost, not during normal ticks.

---

<a id="3-почему-поведение-расходится-даже-при-синхронизации"></a>
## 3. Why Behavior Diverges Even When Synchronized

The central question is: if adaptive speed is synchronized, why can behavior
still diverge? The following sections cover the known causes.

<a id="31-real-time-driven-sync-конфликтует-с-game-time-driven-логикой"></a>
### 3.1 Real-time-driven sync conflicts with game-time-driven logic

Sync packets are sent in **real time** (see §2.2). Game logic ticks in
**game time** (see [ticks_and_subticks.md](ticks_and_subticks.md) §1).
When the server changes `TimeSpeedFactor`:

1. On the server, `gametime` now advances faster or slower.
2. `WriteRes` continues to send every 0.1 real-sec.
3. Between two `WriteRes` calls, the server accumulates
   `0.1 × speedfactor/10` game seconds of resource gathering.
4. The client applies the received values after 0.1 real-sec.

**But the client's progress loop also continues ticking during this time**:
the client runs `_res_ProcessEconomy(deltatime)` at the same shared progress
points. On the client, `deltatime` is calculated as
`GetGameTime - lastprogresstime`, and `GetGameTime` goes at a speed
specified by the last received `gc_LAN_GAME_SYNC_GAMETIME`.

**Problem:** between the moment when the server changes speed and the moment
when the client receives the packet, there is a network lag (~5-100 ms). In this
window:
- The server has already moved ahead in game-time with a new speed.
- The client is still ticking at the old speed.
- After `SYNC_GAMETIME` arrives, the client must either jump to the server's
  game time or, more likely, accept the new speed and continue from its current
  game time.

A difference in game time between server and client produces different
`deltatime` values at different sub-phases, so the client may briefly display
a "phantom" resource value.

For the question at hand, this is secondary: if the server's resource gathering
were reproducible, client-side display differences would not affect gameplay.
It does explain why different hosts may momentarily show different states:
network latency gives them different effective game-time intervals over the
same span of real time.

<a id="32-adaptive-speed-основан-на-локальных-perf-метриках-сервера"></a>
### 3.2 Adaptive speed is based on **local** server perf metrics

The server averages **its own** `GetPerfRender` (rendering FPS) over 16 frames
and `garrfloat_perf_progress` (simulation FPS) over
`gc_perf_progresshistory` frames [^14]. These metrics are
**local** and depend on the process's current environment: Windows background
tasks, antivirus updates, GPU spikes, and so on.

For example:
- Server A at moment T₁ has realfps=30 → speed remains maximum.
- Server B at the same moment T₁ has realfps=18 → speed is reduced to
  8/14 = ~57%.
- With **the same save** on A and B, a five-minute real-time test can cover
  different amounts of game time.

Different amounts of game time produce different numbers of gathering cycles
and therefore different resource totals.

<a id="33-init-random-и-randomext-различаются-между-хостами"></a>
### 3.3 Init `random` and `RandomExt` vary between hosts

C3 makes many `random` and `RandomExt` calls when starting a new game (as
opposed to loading one), including:
- `gProgress.last*time := random*X` [^15];
- `obj.uniqrnd := RandomExt` for **each** unit and resource [^16];
- `obj.progresstick := floor(RandomExt*32)` [^17];
- `lasttime*` per-unit [^18];
- Initial tree positions on the map via `RandomExt` [^19].

In multiplayer, **only the server** performs initialization and sends the result through
`WriteNew`/`WriteSyncServer`. Clients receive `uniqrnd`, `pos` and
other fields from the server and apply them. Multiplayer initialization is
therefore consistent between hosts.

In **single-player**, host A and host B receive different initialization values
(the random seed depends on the system time at startup). If the player
copies the same save to both hosts, the save format
**must** contain `uniqrnd` of all objects (see
[determinism_audit.md](determinism_audit.md) §2.1), so those values will be
identical. The **global `random` state and adaptive-speed phase**, however, will
still differ.

<a id="34-saveload-чтобы-гарантировать-консистентность-нужны-вещи-которых-в-save-нет"></a>
### 3.4 Save/Load: some state required for consistency is not saved

From the save format audit ([determinism_audit.md](determinism_audit.md) §2
+ [ticks_and_subticks.md](ticks_and_subticks.md) §6):

**Save contains:**
- All per-unit `uniqrnd`, `progresstick`, `lasttime*`, `hp`, pos,
  `statestag`, `sto`.
- `gProgress.lastprogresstime`, `progresstick`, `last*time`.

**Save does NOT contain:**
- State of global `random` PRNG cursor.
- Current `garrfloat_perf_progress` history (refilled after
  Load).
- A peasant's sub-tick animation phase (reset by
  `SwitchTo('Nothing')` in `OnAfterLoad`).
- In-flight pathfinding state.

When we load a save on the same host, the second time:
1. PRNG `random` starts from some new state (depending on
   game history since the application was launched).
2. `garrfloat_perf_progress` is empty → adaptive speed reacts differently
   during the first five seconds.
3. All peasants are reset to `'Nothing'` → their next action is a new
   resource search via `_misc_FindResourceToExtract`
   ([determinism_audit.md](determinism_audit.md) §3.1) → two `random` calls
   give **different** results because the global PRNG is in
   a different state.

This explains how the same save can produce different resource-gathering
behavior after separate launches.

<a id="35-между-хостами-в-single-player"></a>
### 3.5 Between hosts in single player

In addition to §3.3 and §3.4:
- Floating-point results from x87, SSE, and FMA may differ in the final bit,
  with discrepancies accumulating over minutes of simulation.
- Adaptive speed differs between hosts (§3.2).
- If the player does not transfer the exact save (for example, starts a “new game”
  with the same settings), the map is generated again with a **different** seed
  → completely different tree positions.

---

<a id="4-сводная-таблица-что-синхронно-что-нет"></a>
## 4. Summary: What Is Synchronized and What Is Not

| State | Single-player Load → Load on one host | Multiplayer between hosts | Single-player on two hosts |
|---|---|---|---|
| Per-unit `uniqrnd` | ✓ persists in save | ✓ via `WriteNew` | ✓ if the save is the same |
| Per-unit `hp`, pos | ✓ | ✓ via periodic sync | ✓ |
| Per-unit `progresstick` | ✓ | ✓ | ✓ |
| Global `random` cursor | ✗ — divergence after Load | ✓ still not needed (server-only) | ✗ — divergence |
| `gProgress.last*time` | ✓ | ✓ | ✓ |
| Animation phase | ✗ — reset by `OnAfterLoad` | n/a — clients do not simulate it | ✗ |
| In-flight pathfinding | ✗ — lost | ✗ — the client catches up via `WriteMove` | ✗ |
| Adaptive speed phase | ✗ — performance history is empty | ✗ — calculated only by the server | ✗ |
| Resource-grid order | ✓ persists with the unit list | ✓ | potentially ✓ when only one map is loaded |
| Position in progress section | ✗ — the section restarts | ✗ — irrelevant to the client | ✗ |
| Map-generation RNG seed | n/a (map stored in save) | ✓ with a shared seed | ✗ — if new games start independently |

---

<a id="5-чем-server-authoritative-помогает-в-добыче"></a>
## 5. How the Server-Authoritative Model Affects Resource Gathering

In multiplayer, the server-authoritative model means that **a peasant's
behavior is determined entirely by the server**. The client sees only the result:
- The server called `_misc_FindResourceToExtract`, made two `random` calls,
  and selected tree No. 142.
- The server sent `WriteOrder` or `WriteSearch` to the client with handle No. 142.
- The client sees a peasant walking towards tree No. 142.

Therefore, **all hosts in a multiplayer game see the same gathering result**:
the server decides, and the clients receive that decision.
**Desync starts** when:
- Network latency causes a player command, such as sending a peasant to work,
  to reach the server later than expected, delaying its execution.
- Delayed adaptive-speed changes can appear as jerky movement on clients.
- A lost UDP packet leaves the client with stale state until the next
  synchronization.

These network effects do not apply in single-player: the local `bProcess` is
always true and there is no synchronization delay. The separate save/load
problem described in §3.4 still applies.

---

<a id="6-импликации-для-мод-фикса"></a>
## 6. Implications for a Mod Fix

For **single-player determinism**:

- Network synchronization can be ignored because `bProcess` is always true.
- Random state after save/load must be handled separately; see
  [determinism_audit.md §3.1](determinism_audit.md). One possible mod strategy
  is to remove `random` from the affected hot path and derive a deterministic
  value from saved fields such as `uniqrnd`, `progresstick`, and `goHnd`.
- Adaptive speed is a separate issue. A mod would need either to disable its
  trigger, if the scripts expose a suitable hook, or to measure behavior in
  game time as described in [ticks_and_subticks.md §9](ticks_and_subticks.md).

For a future **multiplayer** mod:
- Do not alter the structure of `WriteNew`/`ReadNew` or the other paired
  handlers; their synchronization mechanism is sound.
- When patching `_misc_FindResourceToExtract`, be sure to take into account
  `bProcess`. The tree selection logic occurs **only** on the server, so
  the new deterministic hash must use fields available **on the server**
  (`uniqrnd` and `gametime`, both synchronized).
- Do not include anything that may differ between server and client in the
  hash, such as local performance history.

The planned single-player fix satisfies these restrictions automatically.

---

## 7. Cross-references

- [determinism_audit.md](determinism_audit.md) §1 describes `random` vs
  `RandomExt` vs `SetRandomKey`. This document §1.3 explains **why**
  the developers separated these mechanisms (server-authoritative
  architecture).
- [determinism_audit.md](determinism_audit.md) §2 describes what
  persists in save format. This document §2.5 shows that **that
  The same** format is used for on-demand network resync.
- [ticks_and_subticks.md](ticks_and_subticks.md) §5.2 describes adaptive
  speed. This document §3.2 explains why adaptive speed does not help
  consistency between hosts.
- [ticks_and_subticks.md](ticks_and_subticks.md) §6 describes save/load
  hooks. This document §3.4 explains why even these hooks are not
  sufficient.
- [peasant_extraction.md](../../docs_en/recon/world/economy/peasant_extraction.md)
  describes the resource-gathering model and should be read together with the
  RNG-loss analysis in `determinism_audit.md` (§3).

---

<a id="источники"></a>
## Sources

All links are relative to `data/scripts/` in the Cossacks 3 installation.

[^1]: Basic pattern `bProcess` - example of use:
    ```pascal
    var bProcess : Boolean = not (_net_IsClient or _net_IsReplay);
    if (bProcess) then
    begin
       // ... reduce resource HP
       // ... credit the resource to the player
       // ... calculate and apply damage
    end;
    ```
[^2]: Examples of handlers with verification `bProcess`:
    `units/unit.inc/onaclanimationreachedwork.inc:8` (resource extraction),
    `units/unit.inc/onaclanimationreachedattack.inc:8` (application
    damage), `units/unit.inc/onaclanimationreachedconstruct.inc:8`
    (construction progress), `units/unit.inc/ontagstates.inc:720` and
    others.

[^3]: Definitions `_net_IsOffline`, `_net_IsServer`, `_net_IsClient`,
    `_net_IsRecord`, `_net_IsReplay` - `lib/net.script:39-67`.
    Constants `gc_LAN_GAME_*` - `lib/classes.script:7560-7591`.

[^4]: PRNG seeding for projectile dispersion -
    `weapon.script:1051`, `unit.script:11453`. Transfer `frnd` from
    server to client - `unit.script:11554`.

[^5]: Author's comment on the choice of general random -
    `weapon.script:1011`:
    ```pascal
    // I use general random, cause no need to sync it
    // and randomext may change planned results on dif PCs
    ```
[^6]: Template `WriteNew` - `units/global.inc/writenew.inc:15-71`:
    ```pascal
    if _net_IsServer or _net_IsOffline then begin
       // ... locally create unit ...
       gohnd := CreatePlayerGameObjectHandleByHandle(plhnd, race, base, posx, 0, posz);
    end;

    if _net_IsOnline or _net_IsRecord then begin
       RecordCustomBegin('ReadNew');
       // ... write fields to package ...
       var gouid: Integer;
       if _net_IsServer or _net_IsRecord then
          gouid := GetGameObjectUniqueIdByHandle(gohnd);
       RecordCustomWriteString(race);
       // ...
       RecordCustomEnd;
    end;
    ```
[^7]: Periodic timers in the main progress loop -
    `progress/progress.inc/nothing.inc:697-713`:
    ```pascal
    var curtime : Float = GetCurrentTime;   // <-- REAL TIME, not game time!
    if (curtime - gfloat_lan_lastsyncrestime) > 0.1 then
    begin
       gfloat_lan_lastsyncrestime := curtime;
       ExecuteState('WriteRes');
    end;
    if (curtime - gfloat_lan_lastsyncstatstime) > 20 then
    begin
       gfloat_lan_lastsyncstatstime := curtime;
       ExecuteState('WriteStats');
    end;
    if (curtime - gfloat_lan_lastsyncdatatime) > 0.1 then
    begin
       gfloat_lan_lastsyncdatatime := curtime;
       gbool_net_forcesyncdata := true;
       ExecuteState('WriteLanSyncData');
    end;
    ```
[^8]: Trigger `_misc_SyncUnitsParams` mod 53 —
    `progress/progress.inc/nothing.inc:405-406`:
    ```pascal
    if ((gProgress.progresstick mod 53)=0) and (gLanSyncUnitsParamsUIDList.GetCount>0) and ((_net_IsOnline and _net_IsServer) or (_net_IsRecord)) then
       _misc_SyncUnitsParams;
    ```
[^9]: Implementation of `_misc_SyncUnitsParams` -
    `miscext2.script:4301-4338`.

[^10]: Sending gameTime/speed synchronization packet -
    `progress/progress.inc/nothing.inc:617-622`:
    ```pascal
    SetTimeSpeedFactor(newspeed);
    var pLan : Integer = _parser_ParserTemporary(True);
    ParserSetFloatValueByKeyByHandle(pLan, 't', GetGameTime);
    ParserSetFloatValueByKeyByHandle(pLan, 's', newspeed);
    LanSendParser(gc_LAN_GAME_SYNC_GAMETIME, pLan);
    ```
[^11]: `_misc_WriteSyncClient` (resync request) -
    `miscext2.script:3955-3963`.

[^12]: `_misc_WriteSyncServer` (full state of all units) -
    `miscext2.script:3965-4072`.

[^13]: `_misc_ReadSyncClient` - `miscext2.script:4083+`.

[^14]: Local adaptive speed perf metrics -
    `progress/progress.inc/nothing.inc:563-578`:
    ```pascal
    var pr, pp : Float;
    const cCheckFrames = 16;
    for i:=0 to cCheckFrames-1 do
       pr := pr+GetPerfRender(i);
    pr := (pr/cCheckFrames);

    var progfps : Float;
    for i:=0 to gc_perf_progresshistory-1 do
       progfps := progfps+garrfloat_perf_progress[i];
    progfps := progfps/gc_perf_progresshistory;
    ```
[^15]: Init `gProgress.last*time` via `random` —
    `miscext.script:1891-1898`.

[^16]: `obj.uniqrnd := RandomExt` for each unit/resource -
    `unit.script:2726`.

[^17]: Init `obj.progresstick := floor(RandomExt*32)` —
    `unit.script:2707`.

[^18]: Per-unit `lasttime*` initialization - `miscext.script:2757-2762`.

[^19]: Init tree positions via `RandomExt` —
    `misc.script:3714-3715`, `misc.script:3906-3907`.
