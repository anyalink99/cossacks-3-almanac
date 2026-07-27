<a id="recon-детерминизм-добычи-и-боя-rng-audit"></a>
# Recon: determinism of loot and combat (RNG audit)

All sources of non-determinism in the hot path of mining and combat: where is RNG in
scripts (can be modified), and where in the engine (not possible). Needed for
scatter estimates in the simulator and for a potential mod-fix. All
links to the code and the Pascal blocks themselves are collected in the section
[Sources](#sources) at the end of the document.

**Related documents:**

- [ticks_and_subticks.md](ticks_and_subticks.md) - time model,
  sub-tick state, adaptive speed.
- [server_sync_architecture.md](server_sync_architecture.md) —
  server-authoritative architecture C3, net modes, why `random`
  valid in server-only logic.

**Empirical context (player observations):**

- Loading the same save with a fixed arrangement of peasants
  → for an equal interval of real time, resource extraction **varies
  between runs** (same host).
- Between different hosts the discrepancy is even greater.
- **Mines are stable** between launches, their behavior is completely
  reproducible.

All script paths below are relative to `data/` in the Cossacks 3 installation.

---

<a id="1-как-устроен-rng-в-dmscript"></a>
## 1. How RNG works in DMscript

The scripting environment exposes two main sources of randomness and one control function:

| ID | What does | Where is defined |
|---|---|---|
| `random` | Float ∈ [0,1) from global PRNG | engine builtin |
| `RandomExt` | Float ∈ [0,1) from the “extended” PRNG | engine builtin |
| `SetRandomKey(seed : Integer)` | Reseeding Global PRNG | engine builtin |

**Key semantics:** both generators are **global**, but are used differently:

- `random` is a consumable thread whose state is advanced by each call and is not reinitialized between them.
- `RandomExt` - used explicitly after `SetRandomKey(...)` to obtain a **seed-determined** sequence.

> **Important (RE-validated):** generators use **different**
> seed cells. `random` - a wrapper over `System._Random`, which mutates
> standard Delphi `System.RandSeed` (32 bit). `RandomExt` - 64-bit
> LCG over a **individual** cell controlled by `SetRandomKey` and
> `SetRandomExtKey64`. So calling `random` does not shift the seed
> `RandomExt`, and vice versa. A curious subtlety of naming: `SetRandomKey`
> actually controls the seed `RandomExt`, not `Random` - details in
> [`rng_implementation.md` §3](rng_implementation.md). Parsing by binary -
> in private `cossacks-deep/findings/rng_implementation.md`.

There is a conscious pattern in the code: before a series of calls `RandomExt` is placed
`SetRandomKey(floor(uniqrnd × gc_MaxInt))`, after which the sequence
becomes reproducible with the same `uniqrnd` [^1].

The author's comments directly confirm this: one is marked as
`sync multiplayer` (where `RandomExt` is needed synchronous between hosts) [^2],
another - `I use general random, cause no need to sync it and randomext
may change planned results on dif PCs` [^3]. That is, `random` and
`RandomExt` differ in inter-host synchronization guarantees.

**Conclusion 1.** Conscious pattern: `random` - one-time, `RandomExt` -
synchronized via an explicit seed. Using `random` without
preliminary `SetRandomKey` creates a history dependency
global PRNG state.

---

<a id="2-что-переживает-saveload"></a>
## 2. What Save/Load experiences

<a id="21-uniqrnd--детерминированный-per-unit-nonce"></a>
### 2.1 `uniqrnd` - deterministic per-unit nonce

Each unit receives `uniqrnd : Float ∈ [0,1)` when creating [^4], and
**this float is explicitly serialized** in network sync/save: separately
write [^5] and read [^6].

Also saved `progresstick : Integer = floor(RandomExt × 32)` [^7]
and a number of per-unit float fields - `lasttimecheckcapture`, `lasttimeidlegrid`,
`lasttimescangrid`, `lasttimetopology`, `lasttimebestposition`,
`lastsearchenemy` [^8]. They are all initialized via `random` once
at startup and then saved as a normal state.

### 2.2 OnBeforeSave / OnAfterLoad

The engine exposes save and load hooks to scripts. For the peasant
`OnBeforeSave` calls `SwitchTo('Nothing')` [^9], and `OnAfterLoad` calls
for water units it recreates ship childs, for all - again
`SwitchTo('Nothing')` [^10]. For resource `OnAfterLoad` executes
`Initial`-state and goes to `'Nothing'` [^11].

**Conclusion 2.** Developers **know about the instability of sub-tick state** and
forcibly reset the state machine of the peasant in `'Nothing'` and when
saving, and when loading. This normalizes the animation phase and current
action, but **does not normalize**: position (sub-cell), target (sto handle),
direction and state of global PRNG.

<a id="23-что-не-сохраняется-или-ресетится"></a>
### 2.3 What is not saved (or reset)

- Global state `random` (units are clearly not in the save format; probably reseeded to load or not saved at all).
- The current phase of the animation work cycle (reset via `SwitchTo('Nothing')`).
- In-flight pathfinding state (waypoint queue, partial step interpolation) - almost exactly reset.

---

<a id="3-rng-в-добыче"></a>
## 3. RNG in production

<a id="31-site-map-полный"></a>
### 3.1 Site map (full)

All calls to `random` in the resource extraction hot path:

| What to choose | Influence | Level |
|---|---|---|
| `rndind := floor(random × count)` - starting index when scanning the selected cell `gResGrid` to `_misc_FindResourceToExtract` [^12] | **Which tree/stone** will the peasant choose in the found cell | script |
| `if (random < (testW / (testW + testS)))` - choice of wood vs stone when `filterres = none` [^13] | **What resource** is extracted (only with auto-selection of type) | script |
| `if (random < waitrnd)` to `_unit_SearchResourceInRadius` - standtime gate [^14] | **Will the search start** on this tick (if standtime > 0.1) | script |
| `bskipcheck := (random > 0.75)` [^15] | **Should I skip some checks** when selecting a target | script |
| `rndind := floor(random × count)` — starting index in `gIntegerList` [^16] | **Which candidate** is selected from among equally suitable resources in the radius | script |
| `rmax := gc_obj_extract_food_radiusmaxSqr × random` (food only, with move_walk) [^17] | **Radius around the field** in which it is considered “hittable” | script |
| `if (TObj(pobj).standtime >= 9) or (random > 0.9)` [^18] | **Triggering advanced search** of a neighboring resource | script |

Also inside `_unit_SearchResourceInRadius` there are several more
`floor(random × count)` for other search cases [^19].

<a id="32-алгоритм-поиска-по-miscfindresourcetoextract"></a>
### 3.2 Search algorithm (according to `_misc_FindResourceToExtract`)

Logic [^20]:

1. Enumerate all cells `gResGrid[i,j]` (deterministic traversal - the order of cells is fixed).
2. For each, `reldst = (2 + dst) / (1 + (freewood + freestone/2)/40)` is calculated - a deterministic metric of “profitability”.
3. The cell with the minimum `reldst` (`mingridx`, `mingridy`) is remembered.
4. **Inside the found cell** the starting index `rndind := floor(random × count)` is selected, and a linear search is carried out from it.
5. If `filterres = none`, the wood/stone selection is made via `if (random < (testW / (testW + testS)))`.

**Steps 1-3 are completely deterministic**. Steps 4-5 - two calls to `random`.
This explains why, between launches of the same save, peasants
start choosing different trees/stones within one zone.

<a id="33-цепная-реакция"></a>
### 3.3 Chain reaction

Low HP of a single tree (8000-16000 for a stump, with `gc_resource_type_wood`
HP decreases by 1 per hit) and frequent trips to the warehouse create **a lot
decision points** per minute of real time. Each point is
Branch point via `random`. This is the accumulation mechanism
variances.

---

<a id="4-rng-в-бою"></a>
## 4. RNG in battle

### 4.1 Site map

| What to choose | Is it seeded by uniqrnd? | Level |
|---|---|---|
| `bHeadShot := bCanHeadShot and (random < 0.05) and (not bFastHorseBullet)` [^21] | **No** - raw `random` | script |
| `damage := damage + floor(TObj(pobj).uniqrnd × 500)` (headshot bonus) [^22] | **Yes** - fixed per-unit | determined |
| `SetRandomKey(floor(TObj(pobj).uniqrnd × gc_MaxInt))` before debris spawns when a building is destroyed [^23] | **Yes, obviously seeded** | determined |
| `SetRandomKey(floor(random × gc_MaxInt))` before network synchronization of the projectile [^24] | **No** - `random` for seeding | script |
| `(random < 0.05)` - kill-check (probably for NPC env) [^25] | **No** | script |
| `SetGameObjectIntervalFactorByHandle(hnd, 0.7 + random × 0.6)` - Desync death animation **intentionally** [^26] | No | visual, not gameplay |
| `GameObjectRollByHandle(hnd, -cDeathRollAngle + random × cDeathRollAngle × 2)` - angle of incidence of the corpse [^27] | No | visual |
| `SetRandomKey(floor(newuniqrnd × gc_MaxInt))` for calculating the projectile trajectory [^1] | **Yes** | determined |

<a id="42-урон"></a>
### 4.2 Damage

Base damage is calculated completely deterministically:
`damage = weapon.damage + squad.bonus - target.protection[weapkind]`.

Headshot:

- Trigger: `bHeadShot = (random < 0.05)` - **source of dispersion**.
- Bonus if triggered: `+ floor(uniqrnd × 500)` - **deterministic**
  (`uniqrnd` persists).

That is, **in ~95% of shots the damage is completely deterministic**. B ~5%
the damage is devaried through the headshot trigger, which depends on
global state `random` at the time of the shot.

<a id="43-снаряды-и-дисперсия"></a>
### 4.3 Projectiles and dispersion

The `_unit_DoProjectile` pattern is structured like this: first the global PRNG
seeded with the current value `random`, then the variance is calculated
via `RandomExt` (now reproducible from seed), and at the end seed
saved in `TPlayerArgs(parg).frnd` for server replication [^28].

This is a **semi-deterministic** pattern: the seed itself (`random`) is random,
but after installing the seed, further calculations are reproducible. Between
hosts **status `random` is synchronized** via lockstep, so
all hosts receive the same seed → the same `RandomExt` →
the same shot dispersion.

**However** this same pattern explains why `random` is critical for
Sync: if on one of the hosts the global PRNG has advanced too much
call due to some script, *the entire subsequent fight* will be received by others
seeds.

<a id="44-что-детерминировано-в-бою"></a>
### 4.4 What is determined in battle

- Damage without headshot (95% of cases)
- Headshot Bonus (via `uniqrnd`)
- Projectile dispersion (via `SetRandomKey + RandomExt`)
- Projectile flight time, lead, hit/miss in general
- Animations are marked with author's commentary
  `units die at different animation speed, to desyncronise visual part` [^26] —
  This is an intentional desync of only the visual.

**Conclusion 3.** Combat is much more deterministic than mining. Chief
the source of variance is the 5% headshot trigger on raw `random`.
The remaining `random` in the combat code are visual.

---

<a id="5-rng-в-init-и-ai"></a>
## 5. RNG in init and AI

For completeness:

| What | When |
|---|---|
| `obj.progresstick := floor(RandomExt × 32)` — unit progress phase of tick [^7] | init-only, **saved as state** |
| `obj.uniqrnd := RandomExt` - per-unit nonce [^4] | init-only, **saved** |
| Init `gProgress.last*time` via `random` - global timers [^29] | init-only |
| Per-unit `lasttime*` via `random` [^8] | init-only, then saved |
| AI decisions via `RandomExt < _misc_RandToRandom(N)` [^30] | every AI tick affects the player's AI behavior |
| `SetRandomKey(floor(random × gc_MaxInt))` - synchronization for some process [^31] | hot-path |

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
- Income = `produce_rate × N_workers × dt` - pure arithmetic
- No target search, no pathfinding, no queue (slots are fixed)

This matches the empirical result: mines produce the same amount on every run.

---

<a id="7-механизм-недетерминизма-синтез"></a>
## 7. The mechanism of nondeterminism (synthesis)

> For an understanding of tick-loop, sub-tick state and adaptive game speed, see
> [ticks_and_subticks.md](ticks_and_subticks.md). Here we give a short
> RNG-focused summary.

<a id="71-один-хост-разные-запуски-одного-сейва"></a>
### 7.1 One host, different launches of one save

Scenario: load a save with 10 peasants on the forest, wait 5 minutes real-time,
We count the tree.

**What is the same after Load:**

- Positions of peasants and warehouses (integer/tile components - exactly; sub-cell - probably saved as float).
- `uniqrnd` of every peasant (obviously persistent).
- HP of all trees and fields.
- The current goal (`sto`) of each peasant is to handle the resource.
- `progresstick`, all `lasttime*` - persist.

**What's different:**

1. **Global state PRNG** (`random`-cursor) - almost certainly NOT saved in save format and is initialized according to the system start time or in another way that varies from launch to launch.
2. The peasant’s state machine is forcibly reset to `'Nothing'` (see §2.2), but this means that after Load the peasants **look for the target again** through `_misc_FindResourceToExtract` / `_unit_SearchResourceInRadius`, getting into the RNG-dependent steps §3.1.
3. In-flight pathfinding state - lost when `SwitchTo('Nothing')`.

**Cascade:** Load → reset state in `Nothing` → each peasant again
calls search → 5 calls `random` on each peasant affect the choice
starting index in resgrid → different trees → different paths → different
arrival times → different competition for resource → further feedback
no, but there is a multiplier: each Save/Load multiplies the variance.

<a id="72-между-хостами"></a>
### 7.2 Between hosts

In addition to §7.1, the following are added:

- **Floating-point** differences (especially if the CPU supports different extensions).
- Possible lockstep desynchronization during single-player save (it is not network-based and does not have to be strictly deterministic).
- Different init seed `gProgress.last*time` - it is executed once at startup, each host has its own `random` [^29].

<a id="73-ранг-источников-по-влиянию"></a>
### 7.3 Rank of sources by influence

For mining, in descending order of contribution to variance (according to hot-path frequency):

1. **Random selections within `_misc_FindResourceToExtract`** [^12][^13] - Called every time a peasant returns a resource to the warehouse and looks for the next one.
2. **Random selections in `_unit_SearchResourceInRadius`** [^14][^15][^16] - repeated search if the target is lost.
3. **Pathfinding tie-breaking** (engine, not available to the script) - when several paths are of the same length, the choice depends on the internal order of traversing the graph.
4. **Sub-tick state is not normalized to Save/Load** (engine, partially mitigated via `SwitchTo('Nothing')`).
5. **Variable timestep** (engine, if available).

---

<a id="8-что-детерминировано-by-design"></a>
## 8. What is determined by-design

- **Mines**: pure tick arithmetic, no RNG.
- **Per-unit characteristics**: `uniqrnd`, `progresstick`, all `lasttime*` - persist.
- **Damage without headshot** (95% of combat cases).
- **Projectile dispersion** (via `SetRandomKey + RandomExt` from per-unit nonce).
- **Headshot Bonus** (via `uniqrnd`).
- **Profitability metric for cell `gResGrid`** (`reldst` in `_misc_FindResourceToExtract` is a pure function of coordinates and counters).
- **Damage calculation in `OnAclAnimationReachedWork`** [^32] - completely deterministic, no `random`.

---

<a id="9-что-в-движке-вне-досягаемости-скрипта"></a>
## 9. What's in the engine (outside the script's reach)

- **Save/load format** - which fields of `TObj` are saved, which are not (but the list from network sync is exactly saved: `pos`, `dir`, `statestag`, `sto`, `hp`, `uniqrnd` [^33]). Can be partially mitigated via `OnBeforeSave` (as `SwitchTo('Nothing')` already does).
- **Pathfinding** and its tie-breaking at equal distances.
- **Resource grid iteration** — the order of objects in `gResGrid[i,j]` depends on the history of insertions/deletions into the array, which in turn depends on the history of spawning and killing resources.
- **Variable logical tick** — `deltatime` depends on FPS, see [ticks_and_subticks.md](ticks_and_subticks.md) §5.
- **Adaptive game speed** — engine dynamically reduces `TimeSpeedFactor` under load, see [ticks_and_subticks.md](ticks_and_subticks.md) §5.2. This is the **main** source of inter-host desync in single player.
- **Floating-point accuracy between different CPUs**.
- **Global device `random`** - PRNG algorithm, initial seed.

---

<a id="10-импликации-для-модели-добычи"></a>
## 10. Implications for the mining model

Specific assumptions for the model emerge from this audit:

1. **Analytical ceiling** (best-case rate with ideal distribution) - we calculate strictly deterministically using the formulas from [`peasant_extraction.md`](../../docs_en/recon/world/economy/peasant_extraction.md). RNG is not taken into account. Time - in **game-time**, not real-time (see [ticks_and_subticks.md](ticks_and_subticks.md) §1, 9).

2. **Real production in the game** = `theoretical × (1 - loss_factor)`, where `loss_factor` is an empirically calibrated loss coefficient from:
   - Competition for a tree (several peasants per tree).
   - Pathfinding overhead (choosing a non-optimal tree).
   - Micro-delays in searching for a target after returning to the warehouse.

3. **Expected spread between runs of one save** (gut-feel forecast before empirical measurement): σ/μ ≈ 5-15% on a 5-minute window for forest/stone. For mines σ/μ ≈ 0.

4. **Model validation**: run the save ≥ 3 times, take the average, more than one run.

5. **Calibration `loss_factor`**: can potentially be approximated via the RNG fix mod (see §11), which should significantly compress the dispersion and bring it closer to the theoretical ceiling.

---

<a id="11-указатель-на-потенциальный-мод-фикс"></a>
## 11. Pointer to a potential mod fix

Full picture of what is being modded**:

- `_misc_FindResourceToExtract` [^20] - rewrite `random` → deterministic hash from `uniqrnd + GetGameTime + goHnd`.
- `_unit_SearchResourceInRadius` [^34] - the same.
- 7 RNG sites in production (see §3.1) - all script-level.
- Headshot triggering [^21] is optional, for complete determinism of the battle.

**What the mod can NOT fix:**

- Pathfinding tie-breaking.
- Save format extension (requires DLL injection or hex patch exe).
- Traversal order in `gResGrid` (insertion order).
- Inter-launch stability of the PRNG global state (you need to patch the engine initialization).

**Deploy:** via the game mod system (`mods/<modname>/data/scripts/lib/...`
overrides files from the game). Mod manager - `modman.exe`, config -
`mods/mods.ini`. Existing workshop mods (for example, `1585067167` -
Back to War OST) confirm this format.

**Minus:** override for entire files (not for functions) - necessary
copy `misc.script` (256 KB) and `unit.script` (560 KB) completely and
support diff after game patches.

**Test protocol:** save with a fixed arrangement → 5 starts without
fashion (write σ/μ) → 5 runs with mod → comparison. If σ/μ fell
from > 5% to < 2% - RNG sources dominated and the fix works. If
≈ 5% left - engine sources dominate (pathfinding,
sub-tick state).

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
[^10]: `OnAfterLoad` for the peasant (water units reassemble ship childs, the rest - `SwitchTo('Nothing')`) - `units/unit.inc/onafterload.inc`.

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
