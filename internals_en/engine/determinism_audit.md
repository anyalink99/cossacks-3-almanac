<a id="recon-детерминизм-добычи-и-боя-rng-audit"></a>
# Recon: Determinism in Resource Gathering and Combat (RNG Audit)

This audit traces every known source of nondeterminism in the hot paths of
resource gathering and combat. It distinguishes script-level RNG, which a mod
can change, from engine-level behavior outside the scripts' reach. The results
support variance estimates in the simulator and a possible deterministic mod.
All links to the code and the relevant Pascal excerpts are collected in
[Sources](#sources) at the end of the document.

**Related documents:**

- [ticks_and_subticks.md](ticks_and_subticks.md) — time model,
  sub-tick state, adaptive speed.
- [server_sync_architecture.md](server_sync_architecture.md) —
  C3's server-authoritative architecture, network modes, and why `random`
  is valid in server-only logic.

**Empirical context (player observations):**

- Loading the same save with a fixed arrangement of peasants
  → for an equal interval of real time, resource extraction **varies
  between runs** (same host).
- Between different hosts the discrepancy is even greater.
- **Mines are stable** between launches; their behavior is completely
  reproducible.

All script paths below are relative to `data/` in the Cossacks 3 installation.

---

<a id="1-как-устроен-rng-в-dmscript"></a>
## 1. How RNG works in DMscript

The scripting environment exposes two main sources of randomness and one control function:

| ID | Purpose | Defined in |
|---|---|---|
| `random` | Float ∈ [0,1) from global PRNG | engine builtin |
| `RandomExt` | Float ∈ [0,1) from the “extended” PRNG | engine builtin |
| `SetRandomKey(seed : Integer)` | Reseeds the extended PRNG | engine builtin |

**Key semantics:** both generators are **global**, but are used differently:

- `random` draws from a continuous sequence whose state advances on every call.
- `RandomExt` is used after `SetRandomKey(...)` to obtain a sequence
  **determined by an explicit seed**.

> **Important (RE-validated):** generators use **different**
> seed cells. `random` is a wrapper over `System._Random`, which mutates
> standard Delphi `System.RandSeed` (32 bit). `RandomExt` is a 64-bit
> LCG with its **own** state, controlled by `SetRandomKey` and
> `SetRandomExtKey64`. So calling `random` does not shift the seed
> `RandomExt`, and vice versa. A curious subtlety of naming: `SetRandomKey`
> actually controls the `RandomExt` seed, not `Random`; see
> [`rng_implementation.md` §3](rng_implementation.md). The binary analysis is
> documented in the private file `cossacks-deep/findings/rng_implementation.md`.

The code follows a deliberate pattern: before a sequence of `RandomExt` calls,
it invokes `SetRandomKey(floor(uniqrnd × gc_MaxInt))`. The resulting sequence
is reproducible for the same `uniqrnd` [^1].

The source comments confirm this distinction. One call is marked
`sync multiplayer`, where `RandomExt` must stay synchronized between hosts [^2].
Another says that the general RNG needs no synchronization and that
`RandomExt` may change planned results on different PCs [^3]. In other words,
`random` and `RandomExt` provide different cross-host guarantees.

**Conclusion 1.** The code uses `random` for unsynchronized draws and
`RandomExt` for sequences synchronized by an explicit seed. A result from
`random` depends on the entire history of the global PRNG state.

---

<a id="2-что-переживает-saveload"></a>
## 2. What Survives Save/Load

<a id="21-uniqrnd--детерминированный-per-unit-nonce"></a>
### 2.1 `uniqrnd`: deterministic per-unit nonce

Each unit receives `uniqrnd : Float ∈ [0,1)` when it is created [^4], and
**this value is explicitly serialized** in network synchronization and save
data: it is written in one handler [^5] and read back in another [^6].

The save also contains `progresstick : Integer = floor(RandomExt × 32)` [^7]
and several per-unit floating-point fields: `lasttimecheckcapture`, `lasttimeidlegrid`,
`lasttimescangrid`, `lasttimetopology`, `lasttimebestposition`,
`lastsearchenemy` [^8]. They are all initialized via `random` once
at startup and later stored as ordinary state.

### 2.2 OnBeforeSave / OnAfterLoad

The engine exposes save and load hooks to scripts. A peasant's
`OnBeforeSave` calls `SwitchTo('Nothing')` [^9]. In `OnAfterLoad`, water units
recreate their ship children, and all units again call
`SwitchTo('Nothing')` [^10]. A resource object's `OnAfterLoad` executes the
`Initial` state and then switches to `'Nothing'` [^11].

**Conclusion 2.** Developers **know about the instability of sub-tick state** and
force the peasant's state machine to `'Nothing'` both when saving and when
loading. This normalizes the animation phase and current action, but it does
**not** normalize the sub-cell position, target (`sto` handle), direction, or
global PRNG state.

<a id="23-что-не-сохраняется-или-ресетится"></a>
### 2.3 What is not saved (or reset)

- The global `random` state (it does not appear in the known save fields and is
  probably reseeded on load or not saved at all).
- The current phase of the animation work cycle (reset via `SwitchTo('Nothing')`).
- In-flight pathfinding state (the waypoint queue and partial-step
  interpolation) is almost certainly reset.

---

<a id="3-rng-в-добыче"></a>
## 3. RNG in Resource Gathering

<a id="31-site-map-полный"></a>
### 3.1 Complete list of RNG sites

All calls to `random` in the resource extraction hot path:

| RNG-dependent choice | Effect | Level |
|---|---|---|
| `rndind := floor(random × count)` — starting index when `_misc_FindResourceToExtract` scans the selected `gResGrid` cell [^12] | **Which tree or stone deposit** the peasant chooses in that cell | script |
| `if (random < (testW / (testW + testS)))` - choice of wood vs stone when `filterres = none` [^13] | **What resource** is extracted (only with auto-selection of type) | script |
| `if (random < waitrnd)` in `_unit_SearchResourceInRadius` — `standtime` gate [^14] | **Whether the search starts** on this tick (if `standtime > 0.1`) | script |
| `bskipcheck := (random > 0.75)` [^15] | **Should I skip some checks** when selecting a target | script |
| `rndind := floor(random × count)` — starting index in `gIntegerList` [^16] | **Which candidate** is selected among equally suitable resources in range | script |
| `rmax := gc_obj_extract_food_radiusmaxSqr × random` (food only, with `move_walk`) [^17] | **Radius around the field** within which it counts as reachable | script |
| `if (TObj(pobj).standtime >= 9) or (random > 0.9)` [^18] | **Whether to start an extended search** for a neighboring resource | script |

Also inside `_unit_SearchResourceInRadius` there are several more
`floor(random × count)` for other search cases [^19].

<a id="32-алгоритм-поиска-по-_misc_findresourcetoextract"></a>
### 3.2 Search algorithm in `_misc_FindResourceToExtract`

Logic [^20]:

1. Enumerate all `gResGrid[i,j]` cells in a fixed, deterministic order.
2. For each cell, calculate
   `reldst = (2 + dst) / (1 + (freewood + freestone/2)/40)`, a deterministic
   measure of its attractiveness.
3. Retain the cell with the minimum `reldst` (`mingridx`, `mingridy`).
4. **Within the selected cell**, choose the starting index
   `rndind := floor(random × count)` and scan linearly from there.
5. If `filterres = none`, the wood/stone selection is made via `if (random < (testW / (testW + testS)))`.

**Steps 1–3 are completely deterministic**. Steps 4–5 make two `random` calls.
This explains why, between launches of the same save, peasants
start choosing different trees/stones within one zone.

<a id="33-цепная-реакция"></a>
### 3.3 Chain reaction

A single tree has limited HP (8,000–16,000 for a stump, with
`gc_resource_type_wood` HP decreasing by one per hit), and peasants make
frequent trips to the storehouse. This creates **many decision points** per
minute of real time. Each `random` branch adds another opportunity for runs to
diverge, so small differences accumulate.

---

<a id="4-rng-в-бою"></a>
## 4. RNG in Combat

<a id="41-site-map"></a>
### 4.1 RNG sites

| RNG-dependent choice | Seeded by `uniqrnd`? | Level |
|---|---|---|
| `bHeadShot := bCanHeadShot and (random < 0.05) and (not bFastHorseBullet)` [^21] | **No** - raw `random` | script |
| `damage := damage + floor(TObj(pobj).uniqrnd × 500)` (headshot bonus) [^22] | **Yes** — fixed per unit | deterministic |
| `SetRandomKey(floor(TObj(pobj).uniqrnd × gc_MaxInt))` before debris spawns when a building is destroyed [^23] | **Yes** — explicitly seeded | deterministic |
| `SetRandomKey(floor(random × gc_MaxInt))` before network synchronization of the projectile [^24] | **No** - `random` for seeding | script |
| `(random < 0.05)` - kill-check (probably for NPC env) [^25] | **No** | script |
| `SetGameObjectIntervalFactorByHandle(hnd, 0.7 + random × 0.6)` — **intentional** variation in death-animation timing [^26] | No | visual, not gameplay |
| `GameObjectRollByHandle(hnd, -cDeathRollAngle + random × cDeathRollAngle × 2)` — corpse fall angle [^27] | No | visual |
| `SetRandomKey(floor(newuniqrnd × gc_MaxInt))` for calculating the projectile trajectory [^1] | **Yes** | determined |

<a id="42-урон"></a>
### 4.2 Damage

Base damage is calculated completely deterministically:
`damage = weapon.damage + squad.bonus - target.protection[weapkind]`.

Headshot:

- Trigger: `bHeadShot = (random < 0.05)` - **source of dispersion**.
- Bonus if triggered: `+ floor(uniqrnd × 500)` - **deterministic**
  (`uniqrnd` persists).

Thus, **damage is completely deterministic for roughly 95% of shots**. The
remaining roughly 5% depend on the headshot trigger and therefore on the global
`random` state at the moment of the shot.

<a id="43-снаряды-и-дисперсия"></a>
### 4.3 Projectiles and dispersion

The `_unit_DoProjectile` pattern works as follows: first, it seeds the extended
PRNG from the current `random` value. It then calculates dispersion through
`RandomExt`, which is reproducible from that seed, and finally stores a
`RandomExt` value in `TPlayerArgs(parg).frnd` for server replication [^28].

This is a **semi-deterministic** pattern: the seed itself (`random`) is random,
but after installing the seed, further calculations are reproducible. Between
hosts, the **`random` state is synchronized** through the existing network
mechanism, so
all hosts receive the same seed → the same `RandomExt` →
the same shot dispersion.

**However**, this same pattern makes `random` critical to synchronization. If
an extra script call advances the global PRNG on one host, subsequent combat
events receive different seeds.

<a id="44-что-детерминировано-в-бою"></a>
### 4.4 Deterministic parts of combat

- Damage without headshot (95% of cases)
- Headshot bonus (via `uniqrnd`)
- Projectile dispersion (via `SetRandomKey + RandomExt`)
- Projectile flight time, lead, hit/miss in general
- Death-animation timing carries the source comment
  `units die at different animation speed, to desyncronise visual part` [^26] —
  This intentionally varies only the visual presentation.

**Conclusion 3.** Combat is much more deterministic than resource gathering.
Its main gameplay source of variance is the 5% headshot trigger on raw
`random`; the remaining combat-side `random` calls are visual.

---

<a id="5-rng-в-init-и-ai"></a>
## 5. RNG in init and AI

For completeness:

| What | When |
|---|---|
| `obj.progresstick := floor(RandomExt × 32)` — unit progress phase of tick [^7] | init-only, **saved as state** |
| `obj.uniqrnd := RandomExt` - per-unit nonce [^4] | init-only, **saved** |
| Initialize global `gProgress.last*time` timers via `random` [^29] | init-only |
| Per-unit `lasttime*` via `random` [^8] | init-only, then saved |
| AI decisions via `RandomExt < _misc_RandToRandom(N)` [^30] | every AI tick affects the player's AI behavior |
| `SetRandomKey(floor(random × gc_MaxInt))` — synchronization for another process [^31] | hot path |

AI is heavily dependent on `random` and `RandomExt`. This explains why
AI games are even less deterministic than PvP.

---

<a id="6-почему-шахты-воспроизводимы"></a>
## 6. Why mines are reproducible

This section checks the observation against the game logic. A mine is a unit
with `produce[gc_resource_type_*]`; its income is applied in
`_player_ProcessResourceIncome` (see
[peasant_extraction.md](../../docs_en/recon/world/economy/peasant_extraction.md)).

The mine's hot path makes **no calls to `random`**:

- Peasant enters the shaft → `_unit_AddInside` → state “inside”
- Income = `produce_rate × N_workers × dt` — pure arithmetic
- No target search, no pathfinding, no queue (slots are fixed)

This matches the empirical result: mines produce the same amount on every run.

---

<a id="7-механизм-недетерминизма-синтез"></a>
## 7. How Nondeterminism Accumulates

> For the tick loop, sub-tick state, and adaptive game speed, see
> [ticks_and_subticks.md](ticks_and_subticks.md). This section gives a short
> RNG-focused summary.

<a id="71-один-хост-разные-запуски-одного-сейва"></a>
### 7.1 One host, different launches of one save

Scenario: load a save with ten peasants working in a forest, wait five minutes
of real time, then measure the wood gathered.

**State preserved after loading:**

- Positions of peasants and storehouses (integer/tile components definitely;
  sub-cell coordinates probably as floating-point values).
- `uniqrnd` of every peasant.
- HP of all trees and fields.
- Each peasant's current resource target (`sto` handle).
- `progresstick` and all `lasttime*` fields.

**State that can differ:**

1. The **global PRNG state** (`random` cursor) is almost certainly not stored in
   the save and is initialized from system time or another value that varies
   between launches.
2. The peasant's state machine is forcibly reset to `'Nothing'` (see §2.2).
   After loading, peasants therefore **search for a target again** through
   `_misc_FindResourceToExtract` / `_unit_SearchResourceInRadius`, entering
   the RNG-dependent steps described in §3.1.
3. In-flight pathfinding state is lost when `SwitchTo('Nothing')` runs.

**Cascade:** load → reset state to `Nothing` → each peasant searches again →
five `random` calls per peasant affect the starting index in the resource grid
→ different trees → different paths → different arrival times → different
competition for resources. Each save/load cycle can therefore amplify the
variance.

<a id="72-между-хостами"></a>
### 7.2 Between hosts

Cross-host comparisons add three more sources:

- **Floating-point** differences (especially if the CPU supports different extensions).
- A single-player simulation is not network-synchronized and does not have to
  remain strictly deterministic.
- Different initial `gProgress.last*time` values: initialization runs once at
  startup, using each host's own `random` state [^29].

<a id="73-ранг-источников-по-влиянию"></a>
### 7.3 Sources ranked by impact

For resource gathering, the sources rank as follows by hot-path frequency:

1. **Random choices in `_misc_FindResourceToExtract`** [^12][^13] — called
   whenever a peasant deposits resources at the storehouse and searches for a
   new target.
2. **Random choices in `_unit_SearchResourceInRadius`** [^14][^15][^16] —
   repeated whenever the current target is lost.
3. **Pathfinding tie-breaking** (engine-level) — when several paths have equal
   length, the result depends on the graph's internal traversal order.
4. **Sub-tick state is not normalized to Save/Load** (engine, partially mitigated via `SwitchTo('Nothing')`).
5. **Variable timestep** (engine, if available).

---

<a id="8-что-детерминировано-by-design"></a>
## 8. What Is Deterministic by Design

- **Mines**: pure tick arithmetic, no RNG.
- **Per-unit state**: `uniqrnd`, `progresstick`, and all `lasttime*` fields persist.
- **Damage without headshot** (95% of combat cases).
- **Projectile dispersion** (via `SetRandomKey + RandomExt` from per-unit nonce).
- **Headshot bonus** (via `uniqrnd`).
- **Profitability metric for cell `gResGrid`** (`reldst` in `_misc_FindResourceToExtract` is a pure function of coordinates and counters).
- **Damage calculation in `OnAclAnimationReachedWork`** [^32] — completely deterministic, with no `random` calls.

---

<a id="9-что-в-движке-вне-досягаемости-скрипта"></a>
## 9. Engine Behavior Outside the Scripts' Reach

- **Save/load format** - which fields of `TObj` are saved, which are not (but the list from network sync is exactly saved: `pos`, `dir`, `statestag`, `sto`, `hp`, `uniqrnd` [^33]). Can be partially mitigated via `OnBeforeSave` (as `SwitchTo('Nothing')` already does).
- **Pathfinding** and its tie-breaking at equal distances.
- **Resource grid iteration** — the order of objects in `gResGrid[i,j]` depends on the history of insertions/deletions into the array, which in turn depends on the history of spawning and killing resources.
- **Variable logical tick** — `deltatime` depends on FPS, see [ticks_and_subticks.md](ticks_and_subticks.md) §5.
- **Adaptive game speed** — engine dynamically reduces `TimeSpeedFactor` under load, see [ticks_and_subticks.md](ticks_and_subticks.md) §5.2. This is the **main** source of inter-host desync in single player.
- **Floating-point accuracy between different CPUs**.
- **Global `random` generator** — its PRNG algorithm and initial seed.

---

<a id="10-импликации-для-модели-добычи"></a>
## 10. Implications for the Resource-Gathering Model

Specific assumptions for the model emerge from this audit:

1. **Analytical ceiling** (best-case rate with ideal distribution): calculate it
   deterministically from the formulas in
   [`peasant_extraction.md`](../../docs_en/recon/world/economy/peasant_extraction.md),
   without RNG. Measure time in **game time**, not real time (see
   [ticks_and_subticks.md](ticks_and_subticks.md) §§1 and 9).

2. **Actual in-game production** = `theoretical × (1 - loss_factor)`, where
   `loss_factor` is an empirically calibrated coefficient covering:
   - Competition for a tree (several peasants per tree).
   - Pathfinding overhead (choosing a non-optimal tree).
   - Brief delays while searching for a target after returning to the storehouse.

3. **Expected spread between runs of one save** (a preliminary estimate before
   empirical measurement): σ/μ ≈ 5–15% over a five-minute window for wood and
   stone. For mines, σ/μ ≈ 0.

4. **Model validation**: run the same save at least three times and use the
   average rather than a single result.

5. **Calibration `loss_factor`**: can potentially be approximated via the RNG fix mod (see §11), which should significantly compress the dispersion and bring it closer to the theoretical ceiling.

---

<a id="11-указатель-на-потенциальный-мод-фикс"></a>
## 11. Outline of a Potential Mod Fix

**Script changes:**

- `_misc_FindResourceToExtract` [^20] — replace `random` with a deterministic
  hash derived from `uniqrnd + GetGameTime + goHnd`.
- `_unit_SearchResourceInRadius` [^34] — apply the same change.
- All seven resource-gathering RNG sites in §3.1 are script-level.
- The headshot trigger [^21] is optional if complete combat determinism is
  required.

**What the mod cannot fix:**

- Pathfinding tie-breaking.
- Save format extension (requires DLL injection or hex patch exe).
- Traversal order in `gResGrid` (insertion order).
- Inter-launch stability of the PRNG global state (you need to patch the engine initialization).

**Deployment:** use the game's mod system. Files under
`mods/<modname>/data/scripts/lib/...` override the corresponding game files.
The mod manager is `modman.exe`, and its configuration is `mods/mods.ini`.
Existing Workshop mods, such as `1585067167` (Back to War OST), confirm this
layout.

**Drawback:** the mod system overrides whole files, not individual functions.
The mod must therefore copy all of `misc.script` (256 KB) and `unit.script`
(560 KB) and keep those copies in sync with future game patches.

**Test protocol:** fixed-layout save → five runs without the mod (record σ/μ)
→ five runs with the mod → compare. If σ/μ falls from >5% to <2%, script RNG
was the dominant source and the fix works. If roughly 5% remains, engine-level
sources such as pathfinding and sub-tick state dominate.

See separate mod plan document (TBD).

---

<a id="источники"></a>
## Sources

All links are relative to `data/scripts/` in the Cossacks 3 installation.

[^1]: Seed PRNG with the value `uniqrnd` to calculate the projectile trajectory - `lib/weapon.script:1051`:
    ```pascal
    SetRandomKey(floor(newuniqrnd * gc_MaxInt)); // sync multiplayer
    ```
[^2]: Author's comment “sync multiplayer” (ibid.) - `lib/weapon.script:1051`.

[^3]: Author's comment on the difference between `random` and `RandomExt` - `lib/weapon.script:1011`:
    ```pascal
    // I use general random, cause no need to sync it and randomext may change planned results on dif PCs
    ```
[^4]: Initializing `obj.uniqrnd := RandomExt` - `lib/unit.script:2726`.

[^5]: Entry `uniqrnd` in network sync - `lib/miscext2.script:4027`:
    ```pascal
    ParserSetFloatValueByKeyByHandle(pSync, 'uniqrnd', uniqrnd);
    ```
[^6]: Reading `uniqrnd` from network sync - `lib/miscext2.script:4120, 4152`:
    ```pascal
    TObj(pobj).uniqrnd := uniqrnd;
    ```
[^7]: Initializing `obj.progresstick := floor(RandomExt * 32)` - `lib/unit.script:2707`.

[^8]: Per-unit `lasttime*` fields (`lasttimecheckcapture`, `lasttimeidlegrid`, `lasttimescangrid`, `lasttimetopology`, `lasttimebestposition`, `lastsearchenemy`) - `lib/miscext.script:2757-2762`.

[^9]: `OnBeforeSave` for the peasant - `units/unit.inc/onbeforesave.inc`:
    ```pascal
    SwitchTo('Nothing');
    ```
[^10]: `OnAfterLoad` for the peasant (water units reassemble ship children;
    the rest call `SwitchTo('Nothing')`) —
    `units/unit.inc/onafterload.inc`.

[^11]: `OnAfterLoad` for resource - `env/env.inc/onafterload.inc`:
    ```pascal
    ExecuteState('Initial');
    SwitchTo('Nothing');
    ```
[^12]: Starting index when scanning cell `gResGrid` to `_misc_FindResourceToExtract` - `lib/misc.script:2790`:
    ```pascal
    rndind := floor(random * count);
    ```
[^13]: Choosing wood vs stone when `filterres = none` - `lib/misc.script:2801`:
    ```pascal
    if (random < (testW / (testW + testS))) then ...
    ```
[^14]: Gate on standtime in `_unit_SearchResourceInRadius` - `lib/unit.script:4055`:
    ```pascal
    if (random < waitrnd) then ...
    ```
[^15]: Skipping some checks when selecting a target - `lib/unit.script:4114`:
    ```pascal
    bskipcheck := (random > 0.75);
    ```
[^16]: Starting index in `gIntegerList` for selecting a candidate among suitable resources - `lib/unit.script:4120`:
    ```pascal
    rndind := floor(random * count);
    ```
[^17]: Radius around the field for food production with `move_walk` - `lib/unit.script:9790`:
    ```pascal
    rmax := gc_obj_extract_food_radiusmaxSqr * random;
    ```
[^18]: Extended search for neighboring resource triggered - `lib/unit.script:9822`:
    ```pascal
    if (TObj(pobj).standtime >= 9) or (random > 0.9) then ...
    ```
[^19]: Additional `floor(random * count)` in `_unit_SearchResourceInRadius` for other search cases - `lib/unit.script:4623, 4647, 4674, 4796, 4872`.

[^20]: Body `_misc_FindResourceToExtract` - `lib/misc.script:2730-2823`.

[^21]: Headshot triggered - `lib/miscext2.script:420`:
    ```pascal
    bHeadShot := bCanHeadShot and (random < 0.05) and (not bFastHorseBullet);
    ```
[^22]: Headshot damage bonus - `lib/miscext2.script:437`:
    ```pascal
    damage := damage + floor(TObj(pobj).uniqrnd * 500);
    ```
[^23]: Seed PRNG with the value `uniqrnd` before debris spawns when a building is destroyed - `lib/unit.script:11453`:
    ```pascal
    SetRandomKey(floor(TObj(pobj).uniqrnd * gc_MaxInt));
    ```
[^24]: PRNG seeding with `random` value before network synchronization of the projectile - `lib/unit.script:11528`:
    ```pascal
    SetRandomKey(floor(random * gc_MaxInt)); // needed to sync multiplayer arg.frnd
    ```
[^25]: Kill-check for NPC env - `lib/unit.script:7289`:
    ```pascal
    if (random < 0.05) then ...
    ```
[^26]: Intentional desynchronization of death animation speed - `lib/unit.script:11103`:
    ```pascal
    SetGameObjectIntervalFactorByHandle(hnd, 0.7 + random * 0.6);
    // units die at different animation speed, to desyncronise visual part
    ```
[^27]: Angle of incidence of the corpse - `lib/unit.script:10824`:
    ```pascal
    GameObjectRollByHandle(hnd, -cDeathRollAngle + random * cDeathRollAngle * 2);
    ```
[^28]: Body `_unit_DoProjectile` (seeding `random` → calculation `RandomExt` → saving seed in `frnd`) - `lib/unit.script:11518-11554`:
    ```pascal
    SetRandomKey(floor(random * gc_MaxInt)); // line 11528 — seed the PRNG with random
    if (disp > 0) then
       _weapon_CalcShotDispertion(...);   // uses RandomExt, now reproducible from the seed
    TPlayerArgs(parg).frnd := RandomExt; // line 11554 — save seed for server replication
    ```
[^29]: Init global timers `gProgress.last*time` via `random` - `lib/miscext.script:1891-1898`.

[^30]: AI decisions via `RandomExt < _misc_RandToRandom(N)` - `lib/unit.script:3644-3665`.

[^31]: `SetRandomKey(floor(random * gc_MaxInt))` for synchronization - `lib/unit.script:5301`.

[^32]: Deterministic calculation of damage per hit - `units/unit.inc/onaclanimationreachedwork.inc`.

[^33]: List of `TObj` fields guaranteed to be saved in network sync (`pos`, `dir`, `statestag`, `sto`, `hp`, `uniqrnd`) - `lib/miscext2.script:4002-4027`.

[^34]: Body `_unit_SearchResourceInRadius` - `lib/unit.script:4043+`.
