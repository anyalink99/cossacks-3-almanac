# Recon: server architecture and network synchronization

Network synchronization model in C3 - who simulates what is transmitted and when
over the network, how it is related to ticks and `random`. The third document in connection with
[determinism_audit.md](determinism_audit.md) (RNG sites) and
[ticks_and_subticks.md](ticks_and_subticks.md) (time model). Without this
layer cannot be explained why even adaptive speed synchronization between
hosts does not make the behavior reproducible.

All script paths below are relative to `data/` in the Cossacks 3 installation.
All links to the code and the Pascal blocks themselves are collected in the section
[Sources](#sources) at the end of the document.

## TL;DR

- **C3 — server-authoritative, not lockstep.** One host (server) counts
  all game logic; the rest (clients, replays) only display.
- In the code this is the pattern `if not (_net_IsClient or _net_IsReplay) then …` everywhere
  — game logic is executed only on the server [^1].
- Sync packages come in two ways: per-event (one deal, one capture) and
  periodically (once every 53 progress ticks - `_misc_SyncUnitsParams`).
- Because of this, determinism between hosts **does not** have to hold - in
  unlike lockstep, the discrepancy in `random()` cannot be corrected by general
  seed.

---

## 1. Main thing: C3 - server-authoritative, **not** lockstep

### 1.1 What does this mean?

In classic lockstep RTS (StarCraft, Age of Empires II) **all hosts
run an identical simulation** from one seed PRNG, synchronizing
only by player teams. Any rng call is identical on all hosts,
because the input states are identical.

C3 is done **differently**: one host (server) simulates, the rest
(clients) **only display** what is sent to them. This can be seen from
a fundamental pattern that occurs dozens of times in the code:
the game logic block turns into `if (bProcess) then …`, where `bProcess`
defined as `not (_net_IsClient or _net_IsReplay)` [^1].

Clients and replays **do not perform game logic**. They listen for packets from
server and apply the changes locally. This pattern occurs in
handlers for resource extraction, damage, construction progress and
in many other hooks [^2].

### 1.2 Net modes

Five network modes [^3]:

| Mode | Condition | Who is pretending |
|---|---|---|
| `_net_IsOffline` | `GetLanMode = 0` (single player) | Locally (= server for yourself) |
| `_net_IsServer` | `GetLanMode > gc_lanmode_client` | This host |
| `_net_IsClient` | `GetLanMode = gc_lanmode_client` | Receives from the server |
| `_net_IsRecord` | `GetRecordManagerGameMode = 2` | Locally, plus it says replay |
| `_net_IsReplay` | `GetRecordManagerGameMode = 1` | Receives from a record file |

Single-player = `_net_IsOffline` = client-yourself-server. `bProcess`
always true.

### 1.3 Architectural implications

- **Why is `random` seeded via `SetRandomKey(uniqrnd*MaxInt)`** [^4]:
  so that the client can **reproduce** projectile dispersion from the same seed.
  The server sends `frnd : Float = RandomExt` → the client applies
  `SetRandomKey` with the value restored from this `frnd`, and
  gets identical variance.

- **Why `random` (without `SetRandomKey`) is not critical for inter-host
  synchronization**: its result is used only on the server (under
  `bProcess`). Clients do not call this branch. The author's comment is
  directly confirms: “I’m using general random, synchronize it
  not necessary, and randomext can change the intended results to
  different PCs" [^5]. The developers **know** that `random` is not reproducible
  between hosts, and use it only where it is not needed for
  synchronization

---

## 2. What is synchronized and how
<a id="21-per-event-пакеты-отправляются-по-факту-события"></a>
### 2.1 Per-event packages (sent upon event)

Each game object “player” (player state machine) has pairs
`WriteX` / `ReadX` for each event type. In the global catalog
there are more than thirty processors of such pairs:

| Event | Write* | Read* | What does it carry |
|---|---|---|---|
| Unit Creation | writenew.inc | readnew.inc | uid, race/base, pos, cid |
| Destruction | writefree.inc | readfree.inc | uid |
| Death | writedeath.inc | readdeath.inc | uid |
| Command move | writemove.inc | readmove.inc | uid, target pos |
| Order | writeorder.inc | readorder.inc | uid, order type, target |
| Search/find a resource | writesearch.inc | readsearch.inc | — |
| Projectile | writeproj.inc | readproj.inc | uid, weapon, **frnd** for variance sync |
| Apply upgrade | writeapply.inc | readapply.inc | uid, upgrade |
| Construct progress | writeconstruct.inc | readconstruct.inc | uid, hp delta |
| ...~25 more events | | | |

The creation handler template is [^6]: the server creates the object locally
via `CreatePlayerGameObjectHandleByHandle`, **gets local uid**,
and sends this uid to clients in a packet. Clients create local
objects with **same uid** (uid table → handle) and apply parameters.
This preserves the consistency of links between hosts.

<a id="22-periodic-пакеты-по-таймауту"></a>
### 2.2 Periodic packets (by timeout)

The main progress loop checks three timers every tick [^7]:

| What | Period | Scale |
|---|---|---|
| `WriteRes` (player's current resource supply) | 0.1 sec | **real time** |
| `WriteLanSyncData` (general sync block) | 0.1 sec | **real time** |
| `WriteStats` (counters) | 20 sec | **real time** |

**Important:** periods in **real time**. This means:
- At fast (×1.4) game speed, 0.1 real-sec passes between two `WriteRes`
  ≈ 0.14 game-sec.
- On slow (×0.7) — 0.07 game-sec.
- On adaptively-slowed down to 5/10 = 0.5× - 0.05 game-sec.

Accordingly, **packet frequency is the same in real-time on different
speeds**, which is good for network throughput, but bad for
reproducibility of game logic.

<a id="23-sync-unit-params-mod-53"></a>
### 2.3 Sync unit parameters (mod 53)

Once every 53 progress ticks the server calls `_misc_SyncUnitsParams` [^8]: that
takes units from `gLanSyncUnitsParamsUIDList` (units that the server
marked as "needing sync", usually after non-trivial changes)
and sends their status via `WriteSyncUnitsParams` [^9].

**Period:** every 53rd tick of progress. Tick depends on FPS (see.
[ticks_and_subticks.md](ticks_and_subticks.md) §5). At 50 Hz tick this
~1.06 sec real-time. That is, unit param sync lags by ~1 on average
second real-time.

### 2.4 GameTime/speed sync

**Server only** (external condition `_net_IsServer`) changes
`TimeSpeedFactor`. The server sends a packet with a pair (`GetGameTime`,
`newspeed`) via `LanSendParser(gc_LAN_GAME_SYNC_GAMETIME, …)` [^10].
Clients use this to synchronize **game time progression**.

Sending condition: only when `newspeed <> GetTimeSpeedFactor`
(actual change). Between changes - no messages; clients
they just keep ticking at the last set speed.

### 2.5 On-demand full sync

If desync is suspected, heavy synchronization of everything is performed
states:

1. The client sends `gc_LAN_GAME_SYNC_REQUEST` with three `(cuid, nuid, envc)`
   (uid counters) [^11].
2. The server starts `_misc_WriteSyncServer` and sends **full status
   all units** [^12]: for each uid - `bexists`, and (if the object
   exists) `racename`, `basename`, `posx/z`, `scale`, orientation,
   `statestag`, `sto`, `stp`, `sta`, `cid`, `id`, `pl`, `hp`, `bbuilt`,
   `bdead`, `buildprogress`, **`uniqrnd`**.
3. The client in `_misc_ReadSyncClient` recreates the missing objects or
   restores the state of existing [^13].

This is a “hard reset” - an expensive operation, not used in a normal tick,
only when consistency is lost.

---

<a id="3-почему-поведение-расходится-даже-при-синхронизации"></a>
## 3. Why behavior diverges even when synchronized

The main question: “adaptive speed synchronizes on everyone, why is everything
diverges equally? Here's a complete list of reasons.

<a id="31-real-time-driven-sync-конфликтует-с-game-time-driven-логикой"></a>
### 3.1 Real-time-driven sync conflicts with game-time-driven logic

Sync packets are sent in **real time** (see §2.2). Game logic ticks in
**game time** (see [ticks_and_subticks.md](ticks_and_subticks.md) §1).
When the server changes `TimeSpeedFactor`:

1. On the server `gametime` it is now faster/slower.
2. `WriteRes` continues to send every 0.1 real-sec.
3. Between two `WriteRes`, `0.1 × speedfactor/10` has accumulated on the server
   game-time mining.
4. The client applies the received values ​​after 0.1 real-sec.

**But the client is also ticking its progress-loop at this time**:
`_res_ProcessEconomy(deltatime)` is launched on the client from the same shared
progress points. For the client, `deltatime` is calculated as
`GetGameTime - lastprogresstime`, and `GetGameTime` goes at a speed
specified by the last received `gc_LAN_GAME_SYNC_GAMETIME`.

**Problem:** between the moment when the server changes speed and the moment
when the client receives the packet, there is a network lag (~5-100 ms). In this
window:
- The server has already moved ahead in game-time with a new speed.
- The client is still ticking at the old speed.
- After `SYNC_GAMETIME` arrives, the client must **leap** catch up
  game-time of the server, or - which is likely - simply accept the new speed
  and continue with your current gametime.

Difference in gametime between server and client → different `deltatime`
fall on different mini-phases → client display of resources can
display a "phantom" value.

In our specific task, this is not the main thing (if mining on the server
was reproducible, client differences would not matter to
gameplay). But this explains why “different hosts see different things” - they
different effective game-time passed for equal real-time due to lags
sync packages.

<a id="32-adaptive-speed-основан-на-локальных-perf-метриках-сервера"></a>
### 3.2 Adaptive speed is based on **local** server perf metrics

The server averages **its own** `GetPerfRender` (FPS render) and
`garrfloat_perf_progress` (sim FPS) on windows 16 and
`gc_perf_progresshistory` frames respectively [^14]. These metrics
**local** and depend on the state of the process at the moment: background tasks
Windows, antivirus update, GPU spikes and so on.

That is:
- Server A at moment T₁ has realfps=30 → speed remains maximum.
- Server B at the same moment T₁ has realfps=18 → speed is reduced to
  8/14 = ~57%.
- With **the same save** on A and B, different things happened in 5 real-min
  game-time

Different game-time → different number of mining cycles → different amounts of resources.

<a id="33-init-random-и-randomext-различаются-между-хостами"></a>
### 3.3 Init `random` and `RandomExt` vary between hosts

C3 when starting a new game (not Load) causes a lot of `random` and
`RandomExt` for:
- `gProgress.last*time := random*X` [^15];
- `obj.uniqrnd := RandomExt` for **each** unit and resource [^16];
- `obj.progresstick := floor(RandomExt*32)` [^17];
- `lasttime*` per-unit [^18];
- Init tree positions on the map via `RandomExt` [^19].

In multiplayer **only the server** does init and sends the result via
`WriteNew`/`WriteSyncServer`. Clients receive `uniqrnd`, `pos` and
other from the server and apply. Therefore, in multiplayer init is consistent
between hosts.

In **single-player** on host A, initialization gives single values (random
seed = system time on startup A), on host B - others. If the player
copies the same save to both hosts - Load in save format
**must** contain `uniqrnd` of all objects (see
[determinism_audit.md](determinism_audit.md) §2.1), and they will
are the same. But **global state `random` and adaptive speed phase
vary**.

### 3.4 Save/Load: to guarantee consistency you need things that are not in save

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
- Sub-tick animation phase of the peasant (resets after
  `SwitchTo('Nothing')` to `OnAfterLoad`).
- In-flight pathfinding state.

When we load a save on the same host, the second time:
1. PRNG `random` starts from some new state (depending on
   game history since the application was launched).
2. `garrfloat_perf_progress` empty → adaptive speed reacts with another
   Lag for the first 5 seconds.
3. All peasants are reset to `'Nothing'` → their next action = new
   resource search via `_misc_FindResourceToExtract`
   ([determinism_audit.md](determinism_audit.md) §3.1) → 2 calls
   `random` give **different** results because the global PRNG is in
   different condition.

This is the final explanation of “one save, different launches - different
prey."

### 3.5 Between hosts in single player

In addition to §3.3 and §3.4:
- Floating-point behavior between x87/SSE/FMA may differ in
  last bit. Accumulates over minutes of simulation.
- Adaptive speed on different hosts is out of sync (§3.2).
- If the player does not transfer the save exactly (for example, selects “new game”
  with the same settings), the map is generated again with a **different** seed
  → completely different tree positions.

---

## 4. Pivot table: what is synchronous and what is not

| State | Single-player Load → Load on one host | Multiplayer between hosts | Single-player on two hosts |
|---|---|---|---|
| Per-unit `uniqrnd` | ✓ persists in save | ✓ via `WriteNew` | ✓ if the save is the same |
| Per-unit `hp`, pos | ✓ | ✓ via periodic sync | ✓ |
| Per-unit `progresstick` | ✓ | ✓ | ✓ |
| Global `random` cursor | ✗ — divergence after Load | ✓ still not needed (server-only) | ✗ — divergence |
| `gProgress.last*time` | ✓ | ✓ | ✓ |
| Animation phase | ✗ — reset `OnAfterLoad` | n/a - clients do not pretend | ✗ |
| In-flight pathfinding | ✗ — lost | ✗ - but the client catches up via `WriteMove` | ✗ |
| Adaptive speed phase | ✗ — perf history is empty | ✗ - server-only solution | ✗ |
| Resource grid order | ✓ persists with unit list | ✓ | potentially ✓ if there is only one card |
| Position in progress section | ✗ — section starts again | ✗ - but the client doesn’t care | ✗ |
| Map gen RNG seed | n/a (map in save) | ✓ if you use single seed | ✗ — if new games start independently |

---

## 5. How server-authoritative helps in mining

In multiplayer with a server-authoritative model **behavior of a peasant
determined entirely by the server**. The client sees the result:
- The server called `_misc_FindResourceToExtract` with two `random` -
  I chose tree No. 142.
- The server sent `WriteOrder` or `WriteSearch` to the client with handle No. 142.
- The client sees a peasant walking towards tree No. 142.

Therefore **in multiplayer the loot on different hosts is the same** - this is seen
server, the rest are synchronized results.
**Desync starts** when:
- Network lag causes the player's command (for example, send
  peasant) arrives on the server later than estimated → delay
  applications.
- Adaptive speed changed with a lag → clients see jerky movements.
- Network packet lost (UDP) → state on the client is stale before
  next sync.

Single-player has none of this - **your own `bProcess`
always true, no sync lags**. But problems appear 3.4 (save/load).

---

## 6. Implications for mod fix

In the context of **single-player determinism** (our task):
- Network sync can be ignored - `bProcess` is always true.
- **It is necessary to solve the problem `random` after Save/Load** (see.
  [determinism_audit.md](determinism_audit.md) §3.1) - remove `random`
  from hot-path mining, replace with deterministic hash from
  saved fields (`uniqrnd`, `progresstick`, `goHnd`).
- Adaptive speed is a separate problem, requires:
  - or disabling via mod (if there is a script hook on it
    trigger),
  - or measurements in game-time (see.
    [ticks_and_subticks.md](ticks_and_subticks.md) §9).

In the context of **multiplayer** (if you ever want to make an MP mod):
- Do not touch the structure of `WriteNew`/`ReadNew` and other paired ones
  handlers - everything works correctly there.
- When patching `_misc_FindResourceToExtract`, be sure to take into account
  `bProcess`. The tree selection logic occurs **only** on the server, so
  the new deterministic hash must use fields **that**
  is on the server (`uniqrnd`, `gametime` - both are synchronized).
- Do not use anything in hash that may differ between servers
  and by the client (for example, local perf history).

Since the planned single-player mod-fix, these restrictions
are respected automatically.

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
- [peasant_extraction.md](../../docs_en/recon/world/economy/peasant_extraction.md) – model
  production **Must be updated** with reference to determinism_audit.md (§3)
  to account for losses through RNG.

---

## Sources

All links are relative to `data/scripts/` in the Cossacks 3 installation.

[^1]: Basic pattern `bProcess` - example of use:
    ```pascal
    var bProcess : Boolean = not (_net_IsClient or _net_IsReplay);
    if (bProcess) then
    begin
       // ... уменьшаем HP ресурса
       // ... начисляем ресурс игроку
       // ... вычисляем урон и применяем
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
    var curtime : Float = GetCurrentTime;   // <-- REAL TIME, не game time!
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
