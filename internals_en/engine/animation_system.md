<a id="animation-system-тайминги-циклы-точка-удара"></a>
# Animation system: timings, cycles, impact point

What are `.aaf` and `.acl` files, how are frames converted to g-seconds,
where does the “swing point” and the “shot moment” live?
(projectile spawn), where the movement speed of each class is set
units. All links to the code are in [Sources](#sources).

> **Related documents:**
> [`../../docs/recon/world/combat/combat_damage_pipeline.md`](../../docs_en/recon/world/combat/combat_damage_pipeline.md)
> - damage formula; [`../../docs/recon/world/economy/building_mechanics.md`](../../docs_en/recon/world/economy/building_mechanics.md)
> - construction through animation `construct`; [`../../docs/recon/world/combat/ranged_units_behavior.md`](../../docs_en/recon/world/combat/ranged_units_behavior.md)
> - shooting and projectile properties.

## TL;DR

- **`gc_time_to_frames = 32`** - 32 frames in one game second.
  Units use this multiplier directly. For **buildings** yes
  additional `gc_buildtime_modifier = 10`: their `buildtime`
  stored in frames with a multiplier of 10, real construction time =
  `frames × 10 / 32` g-sec.
- **`.aaf`-files** (`data/animations/aaf/<sid>.aaf`) - text
  track table with `(name, start_frame, end_frame)`. 1,382 tracks
  from 194 files (see `derived/animations.json`).
- **`.acl`-files** (`data/animations/acl/<class>.acl`) — Animation
  Cycles List: FSM graph of transitions between animations. Inside -
  `actAnimation`, `actExecuteState`, `actTrackPoint` steps.
- **`refspeed.acl`** - global config of movement speeds and
  rotation for each class (`peasantwalk`, `infantrywalk`,
  `fasthorsewalk`, `cannonwalk`, …). Options
  `TrackPointMoveStep` / `TrackPointTurnStep`.
- **Moment of impact/shot** is callback `OnAclAnimationReachedAttack`
  (`units/unit.inc/onaclanimationreachedattack.inc`). It's built in
  `.acl` attack animation chain between `actAnimation` and
  `actExecuteState 'OnAclAnimationReachedAttackEnd'` - that is
  fires at the **exact frame** specified by the file for each
  weapon/class.
- **`gWeapons[].propagation`** defines: apply damage immediately
  (`immediate` - for melee, buckshot, beam) or spawn
  a projectile that will fly and hit the target later.
- **Gunshot sounds** in large battles are filtered by RNG through
  `gWeapons[].volumeclippedfreq`, so as not to clip - details §6.

---

<a id="1-frame-time-и-gctimetoframes--32"></a>
## 1. Frame-time and `gc_time_to_frames = 32`

`gc_time_to_frames = 32` is the fundamental time constant in
engine. Each game event that is described in frames
(animations, weapon pauses, timers), converted to g-seconds as
`frames / 32`.

**Exception - buildings.** `gc_buildtime_modifier = 10` - field
`buildtime` for buildings is stored in **frames × 10**. That is real
build time = `buildtime_frames × 10 / 32` g-sec. In units
There is no such multiplier, they have `buildtime / 32` - that’s all.

| Object | `buildtime` is stored as | g-sec formula |
|---|---|---|
| Unit (peasant/pikeman/cannon) | frames | `buildtime / 32` |
| Building (cen/bar/aca) | frames × 10 | `buildtime × 10 / 32` |

See also
[`../../docs/recon/world/economy/building_mechanics.md`](../../docs_en/recon/world/economy/building_mechanics.md).

---

<a id="2-файлы-и-форматы"></a>
## 2. Files and formats

### 2.1. `.aaf` – Actor Animation File

Text file (cp1251 format) in `data/animations/aaf/`:
```
AAF
18
"idle",64,113,morph
"walk",1,20,morph
"attack0",237,254,morph
"workfood",278,299,morph
"workwood",237,254,morph
"workstone",217,234,morph
"construct",186,198,morph
"reaction",456,481,morph
"prepare0",64,65,morph
...
```
Header `AAF` + number of records, then one line per track:
`"name", start_frame, end_frame, mode` (mode usually `morph`).

**Inclusion format:** `start` and `end` - both inclusive.
Duration = `end − start + 1` frames = `(end − start + 1) / 32`
g-sec.

Examples from `peaaus.aaf`:

| Track | start–end | Duration |
|---|---:|---:|
| `walk` | 1–20 | 20 frames = 0.625 g-sec |
| `attack0` | 237–254 | 18 frames = 0.5625 g-sec |
| `construct` | 186–198 | **13 frames = 0.4063 g-sec** |
| `workfood` | 278–299 | 22 frames = 0.6875 g-sec |
| `workstone` | 217–234 | 18 frames = 0.5625 g-sec |

**Key Track Names:**

- `idle`, `idle0`, `idle1`, ... - standing without action.
- `walk` - main movement. `walkfood/wood/stone` - with cargo.
- `attack0`, `attack1`, `attack2` - three weapon slots (see §5).
- `workfood/wood/stone` - collective work.
- `construct` - construction / renovation of a building.
- `death` - death.
- `prepare0`, `prepareN` / `unprepareN` - preparation / packaging
  (for `bartprepare` units: artillery, towers).
- `reaction` - reaction to a close enemy (readiness for battle).
- `idlefood/wood/stone` — standing with a load (intermediate state).

**Summary of our parser:** `parser/parse_animations.py` extracts
all tracks in [`derived/animations.json`](../../derived/animations.json).
Average `attack0` for all melee units - **15 frames (0.469 g-sec)**.
This is sewn into `parser/config.py` as `MELEE_SWING_FALLBACK_FRAMES = 15`
for cases when a unit does not have its own `.aaf`.

### 2.2. `.acl` – Animation Cycles List

Text `.parser` format in `data/animations/acl/`. Describes
**FSM transition graph** between animations. Each entry is
named loop with a list of actions.

Example from `cannon.acl` (cannon attack):
```
[*] : struct.begin
   Name = attack0
   From = attack0
   CyclesList = False
   Options : struct.begin
      acoSmoothAnimation = True
      acoRandomFrame = False
      acoRandomCycle = False
      acoSkipActions = False
   struct.end
   global : struct.begin {refurl=.\data\animations\ref\refspeed.acl; refkey=.cannonidle}
      Action = actTrackPoint
      TrackPointIdleName = 
      TrackPointMode = mmNone
      TrackPointPreset = 
   struct.end
   items : struct.begin
      [*] : struct.begin
         Action = actExecuteState
         ExecuteStateName = OnAclAnimationReachedAttack
      struct.end
      [*] : struct.begin
         Action = actAnimation
         AnimationName = attack0
         NumberCycle = 1
      struct.end
      [*] : struct.begin
         Action = actExecuteState
         ExecuteStateName = OnAclAnimationReachedAttackEnd
      struct.end
   struct.end
struct.end
```
**Key fields:**

| Field | What |
|---|---|
| `Name` | Loop name (inside .acl-FSM). |
| `From` | The state from which we come. |
| `CyclesList` | Is it possible to play a loop in a list? |
| `Options.acoSmoothAnimation` | Transition smoothing (blend). |
| `Options.acoRandomFrame` | Start with a random frame (for variety in a group of units). |
| `Options.acoRandomCycle` | Randomly select a cycle option. |
| `Options.acoSkipActions` | Skip `items[]` (only animation without callbacks). |
| `global` | Global setting via `refurl`-include from `refspeed.acl`. |
| `items[]` | Sequence of actions (see §2.3). |

**`refurl` / `refkey`:** include mechanism. `refurl=.\data\animations\
ref\refspeed.acl; refkey=.cannonidle` means “insert here
entry `cannonidle` from `refspeed.acl`." Analogue of `#include` in C.

<a id="23-action-типы-в-acl"></a>
### 2.3. Action types in `.acl`

| Action | What does |
|---|---|
| `actAnimation` | Play animation (by track name from `.aaf`); parameter `NumberCycle` - how many repetitions. |
| `actExecuteState` | Go to the FSM state of the unit (by name) - calls the `units/unit.inc/<state>.inc` handler. |
| `actTrackPoint` | Change the unit's trackpoint (to move along a pre-recorded trajectory). Parameters `TrackPointMode = mmNone / mmRelative / mmAbsolute`. |

Main `ExecuteStateName`:

- `OnAclAnimationReachedAttack` - **moment of impact / shot** (§5).
- `OnAclAnimationReachedAttackEnd` - end of attack animation.
- `OnAclAnimationStarted`, `OnAclAnimationFinished` - start / end.

<a id="24-refspeedacl--таблица-скоростей-движения"></a>
### 2.4. `refspeed.acl` - table of movement speeds

In `data/animations/ref/refspeed.acl` - general config with steps
movement and rotation for each class of units. Each class has
two modes: `…idle` (in place) and `…walk` (in motion).

| Class | `walk.TrackPointMoveStep` | `walk.TrackPointTurnStep` |
|---|---:|---:|
| infantry | 0.03 | 11.125 |
| peasant | **0.0375** | 11.125 |
| hardhorse | 0.0525 | 11.125 |
| fasthorse | **0.09** | 11.125 |
| cannon | 0.020625 | 2.225 |
| mortar | 0.0225 | 8.9 |
| howitzer | 0.020625 | 8.9 |
| multicannon | 0.018 | 11.125 |
| fishboat | 0.015 | 1.1125 |
| ferry | (see file) | (see file) |

`TrackPointMoveStep` - how many tiles the unit moves by **one
walk animation frame** (that is, for `1/32` g-sec). `TrackPointTurnStep`
— rotation angle per frame (in degrees).

Speed in tiles per second:
```
tiles_per_g_sec = TrackPointMoveStep × 32
```
| Class | Speed (tiles/g-sec) |
|---|---:|
| infantry | 0.96 |
| peasant | 1.20 |
| hardhorse | 1.68 |
| fasthorse | **2.88** (×3 from infantry) |
| cannon | 0.66 |
| mortar | 0.72 |
| howitzer | 0.66 |
| fishboat | 0.48 |

See also `gc_obj_speed_*` constants in `dmscript.global`
(`peasant = 40`, `fasthorse = 96`, etc.) is an abstract
scale, **proportional** `TrackPointMoveStep`, but not
identical. For exact values in tiles take from here
(`refspeed.acl`).

### 2.5. `refunit.acl`

General config of basic cycles `idle / walk / death` - reused
via `refurl`-include from specific `<class>.acl`-files.
Reduces duplication: a typical link is “the gun `idle` has this
the same as for infantry, but `walk` is special.”

---

<a id="3-native-api-для-анимаций"></a>
## 3. Native API for animations

`derived/dws_native_signatures.json` contains **600+ functions**
working with animations. Key groups:

### 3.1. Frame-data

| Function | What |
|---|---|
| `GetGameObjectFrameAnimationDataByHandle(gohnd, animname, var sf, ef): Boolean` | Get start/end animation frames `animname` for an object. Used in `_unit_ApplyAttackPause` to calculate pauses. |
| `GetGameObjectDeferredFramesByHandle(gohnd, var defcurrentframe, defframes)` | The current frame and the total number of frames of the deferred loop. |

<a id="32-switch--blend"></a>
### 3.2. Switch/blend

| Function | What |
|---|---|
| `GameObjectSetFrameAnimationByHandle(gohnd, frameanimationname, randomoffsetframeanimation)` | Direct installation of animation. |
| `GameObjectSwitchToAnimationCyclesBlendByHandle(gohnd, name, ...)` | Smooth blend between current and new loop. |
| `GameObjectMySwitchToFrameAnimationBlend(name, randomframe, smooth, ...)` | The same blend for “your” (current-actor) context. |

### 3.3. TrackPoint

| Function | What |
|---|---|
| `GameObjectMyTrackPointAdd(x, y, z)` | Add a point to move along the path. |
| `GameObjectMyTrackPointInsert(ind, x, y, z)` | Insert into position `ind`. |
| `GameObjectMyTrackPointClear()` | Clear all track points. |
| `GameObjectGetTrackPointMoveDistanceToEndByHandle(gohnd)` | Distance from the current position to the end of the path. |
| `GameObjectGetTrackPointMoveDistanceToAlignByHandle(gohnd)` | Distance to alignment point (formation). |

---

<a id="4-fsm-юнита-и-её-связь-с-анимациями"></a>
## 4. Unit FSM and its connection with animations

Each unit is an FSM, states are stored as a bitmask
`gc_statetag_*` to `TObj.statestag` (see table in
`dmscript.global`). Main groups:

| Group | Bits |
|---|---|
| Essential | `essential_none`, `essential_birth`, `essential_death` |
| Move | `move_idle`, `move_walk`, `move_turn` |
| Action | `action_none`, `action_attack`, `action_build`, `action_extract` |
| Execute | `execute_none`, `execute_move` |
| Weapon | `weapon_none`, `weapon_0`, `weapon_1`, `weapon_2` |
| Resource | `resource_none`, `resource_food`, `resource_wood`, `resource_stone` |
| Visual | `visual_none`, `visual_stage_0..3`, `visual_hide` |

When changing states, `.acl`-FSM selects the appropriate animation
(for example, `walkfood` if `state = move_walk + resource_food`).

Specific FSM transition handlers - in
`data/scripts/units/unit.inc/<state>.inc`. For example:
`onaclanimationreachedattack.inc` triggers on event
“the attack animation has reached swing-point” (§5).

---

<a id="5-onaclanimationreachedattack--момент-удара--выстрела"></a>
## 5. `OnAclAnimationReachedAttack` - moment of impact / shot

This is the **main callback** of the animal system: the moment in the frame when
damage is applied to the target or a projectile is fired. Fully described in
`data/scripts/units/unit.inc/onaclanimationreachedattack.inc`.

<a id="51-где-задаётся-точный-кадр"></a>
### 5.1. Where is the exact frame set?

In the `.acl` attack file (`attack0` / `attack1` / `attack2`)
the order `items[]` determines **at what point** the animation
callback will work. Standard structure:
```
items:
  [0] actExecuteState 'OnAclAnimationReachedAttack'    ← swing point
  [1] actAnimation 'attack0' (NumberCycle = 1)         ← complete animation
  [2] actExecuteState 'OnAclAnimationReachedAttackEnd' ← completion
```
`actExecuteState` is triggered when `actAnimation`
will reach the corresponding mark. That is, `swing-point` is built in
**into the animation itself** via `.acl`-config - for different units it
may be at the beginning, middle or end of the attack cycle.

<a id="52-что-callback-делает"></a>
### 5.2. What does callback do?

Pseudocode (`onaclanimationreachedattack.inc`):
```
1. If the unit is dead, exit.
2. weapind := weapon index from statetag (gc_statetag_weapon_0/1/2 → 0/1/2).
3. _unit_ApplyWeaponCost(myHnd, weapind)        ← deduct iron/coal/gold for the shot
4. _unit_ApplyAttackPause(myHnd, weapind)        ← pause until the next cycle
5. weaponid := objprop.weapon[weapind].weaponid
   trgHnd := GetGameObjectSTOHandleByHandle(myHnd)  ← cached target
6. If trgHnd ≠ 0:
   a) weaponid == 0 (melee):
      - Play the impact sound (sword/sabre/pike) via _unit_RequestPlaySound
      - _misc_DoDamage(myHnd, trgHnd, damage, weapind, kind) ← immediate damage
   b) propagation == immediate (canister, lightning):
      - Apply _misc_DoDamage immediately
      - Play the shot sound
      - Spawn the fxshot effect (flash, smoke)
   c) normal projectile:
      - Spawn a projectile via CreatePlayerGameObjectHandleByHandle
      - A separate projectile FSM handles its flight
      - _misc_DoDamage runs on the '_OnTargetReached' event
```
<a id="53-семантика-для-разных-типов-оружия"></a>
### 5.3. Semantics for different types of weapons

| Type `weaponid` | What's at the moment of swing |
|---|---|
| Melee (`weaponid = 0`) | Damage immediately. Sound - `sabre`/`pike`/`sword` (by `kind`). |
| Rifle with `propagation = immediate` (buckshot, lightning) | Immediate damage + sound + fxshot. The AoE radius is applied here too. |
| Regular projectile (arrow, bullet, cannonball) | A `projectile` object spawns and flies towards the target. Damage is applied at the moment the projectile **arrives** (event `_OnTargetReached`), and not at the moment of swing. This gives "flight time" for arrows and cannonballs. |

<a id="54-rng-фильтр-звуков-выстрела"></a>
### 5.4. RNG filter for gunshot sounds

If the object is **not in frustum** of the camera and
`gWeapons[weaponid].volumeclippedfreq > 0`, RNG check is done:
`if vcf < random` - sound **skips**. That is, on large
battles, where 100 musketeers fire in a volley, part of the sounds
accidentally discarded so that the mixer does not clip.

If `volumeclippedfreq <= 0` - the sound is always played (musket in
frustum, artillery). If `volumeclippedfreq` is high (≈ 0.9) -
sound is skipped often (background gunfire out of sight).

---

<a id="6-unitapplyattackpause--следующий-цикл"></a>
## 6. `_unit_ApplyAttackPause` - next cycle

After each swing there is a pause until the next one
attack cycle [^2]:
```
attpause := objbase.weapon[weapind].pause
if individual.benabled and attpause > 0:
    attpause *= individual.attackrate    ← percentage upgrades
```
The specific number `pause` is stored in the unit data. For the musketeer
17th century — `pause ≈ 150` frames = 4.69 g-sec. With upgrades
`aca.31`+`aca.33` (60% cumulative reduction) — `≈ 1.88 g-sec`.

The code has a **commented out** branch checking “whether
pause for animation length": if `attpause - frames/30 < 1/60`,
no pause is needed (the animation is already long). Currently this
branch **disabled** - pause is always applied, even if it
shorter animation (this is not critical: the next swing point is not
will fire before the next cycle `.acl`).

---

<a id="7-unitapplyweaponcost--стоимость-выстрела"></a>
## 7. `_unit_ApplyWeaponCost` - cost of a shot

With each swing, `weapon[weapind].cost[restype]` is debited for
shot [^3]:
```
for i := 0 to gc_ResCount-1:
   if weapon[weapind].cost[i] > 0:
      if gPlayer[plInd].res[i] >= weapon[weapind].cost[i]:
         res[i] -= weapon[weapind].cost[i]
      else:
         res[i] := 0  ← if the player has less, deduct the remainder
```
That is, if the player runs out of `iron` or `coal`, tower/cannon
**still shoots** (writes off the remainder to zero), but then without
resource ceases. If a shot is not blocked by a resource, it is written off
upon the impact. This is the key mechanism: **check at the time of swing
there is no resource**, the check occurs earlier - at the stage of target selection.

Full table of shot prices for each unit - in
[`../../docs/reference/02_combat/README.md` → “Cost of one shot”](../../docs_en/reference/02_combat/README.md).

---

<a id="8-ключевые-тайминги-сводка"></a>
## 8. Key timings (summary)

From 1,382 tracks in `derived/animations.json`:

| Class | `attack0` (frames) | `attack0` (g-sec) | `walk` (frames) | Real-DPS @ fast (if known) |
|---|---:|---:|---:|---:|
| Peasant (peaaus) | 18 | 0.563 | 20 | — |
| Pikeman 17th century | 14 | 0.438 | 20 | ~7-8 |
| Musketeer 17th century | 18 | 0.563 | 22 | ~6-7 (via `weapon.pause`) |
| Cavalryman | 18 | 0.563 | 26 | — |
| Cannon | 14-16 | 0.5 | (see §2.4) | by `weapon.pause = 350 frames` |
| Tower | 14 | 0.438 | (idle) | by `weapon.pause = 400 frames` |

`attack0` - duration of the strike animation. Real attack tempo
is defined by `weapon.pause` (see §6), which is usually **greater**
`attack0` (due to built-in rest between swings). For
melee `weapon.pause = 0` - they hit every animation cycle,
that is, **`attack0`-duration is the DPS cycle**.

See function `melee_swing_sec(sid)` in
[`parser/config.py`](../../parser/config.py) - takes real
`attack0` from `derived/animations.json` or fallback to median 15
frames (0.469 g-sec).

---

<a id="9-открытые-вопросы"></a>
## 9. Open questions

1. **Exact refspeed values for all classes.** I have listed
   main (infantry / peasant / hardhorse / fasthorse / cannon /
   mortar / howitzer / multicannon / fishboat / ferry), but in
   `refspeed.acl` There are also more exotic ones (`balloondock`,
   `ducha`-marine classes, etc.). Full dump - open the file.
2. **How does `gc_obj_speed_*` relate to `TrackPointMoveStep`.**
   It looks like these are two **different** scales: `gc_obj_speed_*` —
   abstract for AI calculations, `TrackPointMoveStep` - real
   for rendering. The connection has not been read.
3. **`actTrackPoint` with mode `mmRelative` vs `mmAbsolute`** —
   exactly how it is used when moving in formation.
4. **`acoRandomFrame` behavior.** If enabled, units in the group
   walk animation starts from different frames - but how is it chosen?
   starting frame? Via `random()` or `uniqrnd`?

---

<a id="источники"></a>
## Sources

[^1]: `data/scripts/units/unit.inc/onaclanimationreachedattack.inc`
      - the main handler of the moment of impact. Parameters: `arg_obj : TObj`.
      Inside checks `bdead`, `attackdelay`, selects weapons
      via `statetag`, applies `_unit_ApplyWeaponCost` /
      `_unit_ApplyAttackPause`, delegates damage to `_misc_DoDamage`
      (for melee / immediate) or spawns `projectile` object
      (for ranged attack).

[^2]: `_unit_ApplyAttackPause` - `lib/unit.script` (search
      `procedure _unit_ApplyAttackPause`). Counts the final pause
      as `attpause * individual.attackrate` (if custom
      upgrades are active).

[^3]: `_unit_ApplyWeaponCost` - `lib/unit.script` (search
      `procedure _unit_ApplyWeaponCost`). Cheats
      `weapon[weapind].cost[i]` for all 7 resources (food / wood /
      stone / gold / iron / coal / +1).
