<a id="animation-system-тайминги-циклы-точка-удара"></a>
# Animation System: Timing, Cycles, and Impact Frames

This document explains the `.aaf` and `.acl` formats, conversion from animation
frames to game seconds, the exact frame at which a strike or shot occurs, and
the movement-speed settings for each unit class. Code references are collected
in [Sources](#sources).

> **Related documents:**
> [`../../docs/recon/world/combat/combat_damage_pipeline.md`](../../docs_en/recon/world/combat/combat_damage_pipeline.md)
> - damage formula; [`../../docs/recon/world/economy/building_mechanics.md`](../../docs_en/recon/world/economy/building_mechanics.md)
> - construction through animation `construct`; [`../../docs/recon/world/combat/ranged_units_behavior.md`](../../docs_en/recon/world/combat/ranged_units_behavior.md)
> - shooting and projectile properties.

## TL;DR

- **`gc_time_to_frames = 32`** — one game second contains 32 frames.
  Units use this conversion directly. **Buildings** have an additional
  `gc_buildtime_modifier = 10`: their `buildtime` is stored in frames with a
  factor of 10, so actual construction time is
  `frames × 10 / 32` g-sec.
- **`.aaf` files** (`data/animations/aaf/<sid>.aaf`) — text tables of tracks
  with `(name, start_frame, end_frame)`. The catalog contains 1,382 tracks
  from 194 files (see `derived/animations.json`).
- **`.acl` files** (`data/animations/acl/<class>.acl`) — animation-cycle lists,
  represented as FSM graphs of transitions between animations. They contain
  `actAnimation`, `actExecuteState`, `actTrackPoint` steps.
- **`refspeed.acl`** — global configuration of movement speeds and
  rotation for each class (`peasantwalk`, `infantrywalk`,
  `fasthorsewalk`, `cannonwalk`, …). Options
  `TrackPointMoveStep` / `TrackPointTurnStep`.
- The **moment of impact or shot** is the
  `OnAclAnimationReachedAttack` callback
  (`units/unit.inc/onaclanimationreachedattack.inc`). It is embedded in the
  `.acl` attack-animation chain and fires at the **exact frame** specified for
  each weapon and class.
- **`gWeapons[].propagation`** defines: apply damage immediately
  (`immediate` - for melee, buckshot, beam) or spawn
  a projectile that travels and hits the target later.
- **Gunshot sounds** in large battles are filtered by RNG through
  `gWeapons[].volumeclippedfreq` to avoid clipping; see §6.

---

<a id="1-frame-time-и-gc_time_to_frames--32"></a>
## 1. Frame-time and `gc_time_to_frames = 32`

`gc_time_to_frames = 32` is the engine's fundamental time conversion. Every
event expressed in frames—animations, weapon pauses, and some timers—is
converted to game seconds as
`frames / 32`.

**Exception: buildings.** Because `gc_buildtime_modifier = 10`, a building's
`buildtime` is stored in **frames × 10**. Its actual construction time is
`buildtime_frames × 10 / 32` game seconds. Units have no such multiplier and
use `buildtime / 32`.

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

These are CP1251 text files in `data/animations/aaf/`:
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

Both `start` and `end` are inclusive.
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

**Key track names:**

- `idle`, `idle0`, `idle1`, ... — standing without action.
- `walk` — normal movement; `walkfood/wood/stone` — movement with cargo.
- `attack0`, `attack1`, `attack2` — three weapon slots (see §5).
- `workfood/wood/stone` — resource-gathering work.
- `construct` — building construction or repair.
- `death` — death.
- `prepare0`, `prepareN` / `unprepareN` — deployment and packing
  (for `bartprepare` units: artillery, towers).
- `reaction` — response to a nearby enemy (combat readiness).
- `idlefood/wood/stone` — standing with a load (intermediate state).

**Summary of our parser:** `parser/parse_animations.py` extracts
all tracks in [`derived/animations.json`](../../derived/animations.json).
The average `attack0` track among melee units is **15 frames (0.469 game
seconds)**. This value appears in `parser/config.py` as
`MELEE_SWING_FALLBACK_FRAMES = 15`
for cases when a unit does not have its own `.aaf`.

### 2.2. `.acl` – Animation Cycles List

These `.parser`-format text files in `data/animations/acl/` describe an
**FSM transition graph** between animations. Each entry is a named cycle with
a list of actions.

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

| Field | Meaning |
|---|---|
| `Name` | Cycle name within the `.acl` FSM. |
| `From` | Source state for the transition. |
| `CyclesList` | Whether the cycle can be played as part of a list. |
| `Options.acoSmoothAnimation` | Transition smoothing (blend). |
| `Options.acoRandomFrame` | Start with a random frame (for variety in a group of units). |
| `Options.acoRandomCycle` | Randomly select a cycle option. |
| `Options.acoSkipActions` | Skip `items[]`, playing the animation without callbacks. |
| `global` | Shared settings included from `refspeed.acl` through `refurl`. |
| `items[]` | Sequence of actions (see §2.3). |

**`refurl` / `refkey`:** an inclusion mechanism.
`refurl=.\data\animations\ref\refspeed.acl; refkey=.cannonidle` means “insert
the `cannonidle` entry from `refspeed.acl` here.” It is analogous to C's
`#include`.

<a id="23-action-типы-в-acl"></a>
### 2.3. Action types in `.acl`

| Action | Purpose |
|---|---|
| `actAnimation` | Play an animation by its `.aaf` track name; `NumberCycle` sets the number of repetitions. |
| `actExecuteState` | Enter a named unit FSM state and invoke its `units/unit.inc/<state>.inc` handler. |
| `actTrackPoint` | Change the unit's track point for movement along a predefined trajectory. Modes: `mmNone`, `mmRelative`, and `mmAbsolute`. |

Main `ExecuteStateName` values:

- `OnAclAnimationReachedAttack` - **moment of impact / shot** (§5).
- `OnAclAnimationReachedAttackEnd` - end of attack animation.
- `OnAclAnimationStarted`, `OnAclAnimationFinished` - start / end.

<a id="24-refspeedacl--таблица-скоростей-движения"></a>
### 2.4. `refspeed.acl`: movement-speed table

`data/animations/ref/refspeed.acl` contains the common movement and rotation
steps for each unit class. Each class has
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

`TrackPointMoveStep` is the distance, in tiles, that the unit moves during
**one walk-animation frame** (`1/32` of a game second).
`TrackPointTurnStep` is the rotation angle per frame, in degrees.

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

The `gc_obj_speed_*` constants in `dmscript.global` (`peasant = 40`,
`fasthorse = 96`, and so on) use an abstract scale that is **proportional to**
but not identical with `TrackPointMoveStep`. Use `refspeed.acl` for exact
tile-based values.

### 2.5. `refunit.acl`

The common `idle`, `walk`, and `death` cycles are reused through `refurl`
inclusions from class-specific `.acl` files. This reduces duplication: a class
can share an infantry idle cycle while defining its own walk cycle.

---

<a id="3-native-api-для-анимаций"></a>
## 3. Native API for animations

`derived/dws_native_signatures.json` contains **600+ functions**
working with animations. Key groups:

### 3.1. Frame data

| Function | Purpose |
|---|---|
| `GetGameObjectFrameAnimationDataByHandle(gohnd, animname, var sf, ef): Boolean` | Get an object's start and end frames for `animname`. `_unit_ApplyAttackPause` uses them to calculate delays. |
| `GetGameObjectDeferredFramesByHandle(gohnd, var defcurrentframe, defframes)` | The current frame and the total number of frames of the deferred loop. |

<a id="32-switch--blend"></a>
### 3.2. Switch/blend

| Function | Purpose |
|---|---|
| `GameObjectSetFrameAnimationByHandle(gohnd, frameanimationname, randomoffsetframeanimation)` | Set an animation directly. |
| `GameObjectSwitchToAnimationCyclesBlendByHandle(gohnd, name, ...)` | Smooth blend between current and new loop. |
| `GameObjectMySwitchToFrameAnimationBlend(name, randomframe, smooth, ...)` | Perform the same blend for the current actor context. |

### 3.3. TrackPoint

| Function | Purpose |
|---|---|
| `GameObjectMyTrackPointAdd(x, y, z)` | Add a point to move along the path. |
| `GameObjectMyTrackPointInsert(ind, x, y, z)` | Insert a point at index `ind`. |
| `GameObjectMyTrackPointClear()` | Clear all track points. |
| `GameObjectGetTrackPointMoveDistanceToEndByHandle(gohnd)` | Distance from the current position to the end of the path. |
| `GameObjectGetTrackPointMoveDistanceToAlignByHandle(gohnd)` | Distance to alignment point (formation). |

---

<a id="4-fsm-юнита-и-её-связь-с-анимациями"></a>
## 4. Unit FSM and Animation Integration

Each unit is an FSM whose states are stored in `TObj.statestag` as a
`gc_statetag_*` bitmask (see the table in
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

Specific FSM transition handlers live in
`data/scripts/units/unit.inc/<state>.inc`. For example,
`onaclanimationreachedattack.inc` handles the event in which the attack
animation reaches its swing point (§5).

---

<a id="5-onaclanimationreachedattack--момент-удара--выстрела"></a>
## 5. `OnAclAnimationReachedAttack`: Moment of Impact or Shot

This is the **main callback** of the animation system: the point in the cycle when
damage is applied to the target or a projectile is fired. Fully described in
`data/scripts/units/unit.inc/onaclanimationreachedattack.inc`.

<a id="51-где-задаётся-точный-кадр"></a>
### 5.1. Where the exact frame is set

In the `.acl` attack file (`attack0` / `attack1` / `attack2`)
the order of `items[]` determines **when** the callback fires. The standard
structure is:
```
items:
  [0] actExecuteState 'OnAclAnimationReachedAttack'    ← swing point
  [1] actAnimation 'attack0' (NumberCycle = 1)         ← complete animation
  [2] actExecuteState 'OnAclAnimationReachedAttackEnd' ← completion
```
`actExecuteState` fires when `actAnimation` reaches the corresponding marker.
The swing point is therefore embedded **in the animation itself** through the
`.acl` configuration; depending on the unit, it may occur near the beginning,
middle, or end of the attack cycle.

<a id="52-что-callback-делает"></a>
### 5.2. What the callback does

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

| `weaponid` type | What happens at the swing point |
|---|---|
| Melee (`weaponid = 0`) | Damage is applied immediately. Sound: `sabre`, `pike`, or `sword`, selected by `kind`. |
| Rifle with `propagation = immediate` (buckshot, lightning) | Immediate damage + sound + fxshot. The AoE radius is applied here too. |
| Regular projectile (arrow, bullet, cannonball) | A `projectile` object spawns and flies towards the target. Damage is applied at the moment the projectile **arrives** (event `_OnTargetReached`), and not at the moment of swing. This gives "flight time" for arrows and cannonballs. |

<a id="54-rng-фильтр-звуков-выстрела"></a>
### 5.4. RNG filter for gunshot sounds

If the object is **outside the camera frustum** and
`gWeapons[weaponid].volumeclippedfreq > 0`, the game performs an RNG check:
`if vcf < random` causes the sound to be **skipped**. During large battles,
such as a volley from 100 musketeers, this randomly discards some off-screen
sounds to prevent audio clipping.

If `volumeclippedfreq <= 0`, the sound always plays. If it is high
(approximately 0.9), unseen background gunfire is skipped frequently.

---

<a id="6-_unit_applyattackpause--следующий-цикл"></a>
## 6. `_unit_ApplyAttackPause`: Delay Before the Next Cycle

After each swing, the game applies a delay before the next attack cycle [^2]:
```
attpause := objbase.weapon[weapind].pause
if individual.benabled and attpause > 0:
    attpause *= individual.attackrate    ← percentage upgrades
```
The specific number `pause` is stored in the unit data. For the musketeer
17th century — `pause ≈ 150` frames = 4.69 g-sec. With upgrades
`aca.31`+`aca.33` (60% cumulative reduction) — `≈ 1.88 g-sec`.

The code contains a **commented-out** branch that would compare the pause with
the animation length: if `attpause - frames/30 < 1/60`, no extra delay would
be needed because the animation is already long enough. That branch is
currently **disabled**, so the pause is always applied even when it is shorter
than the animation. This does not allow the next swing point to fire before the
next `.acl` cycle.

---

<a id="7-_unit_applyweaponcost--стоимость-выстрела"></a>
## 7. `_unit_ApplyWeaponCost`: Cost per Shot

Each attack consumes the resources listed in
`weapon[weapind].cost[restype]` [^3]:
```
for i := 0 to gc_ResCount-1:
   if weapon[weapind].cost[i] > 0:
      if gPlayer[plInd].res[i] >= weapon[weapind].cost[i]:
         res[i] -= weapon[weapind].cost[i]
      else:
         res[i] := 0  ← if the player has less, deduct the remainder
```
A tower or cannon can therefore **complete the current shot** even when the
player has less iron or coal than its full cost: the remaining amount is
reduced to zero. Further attacks stop once the missing resource is checked
during target selection. Resource payment itself occurs at the attack impact,
not during that earlier availability check.

The complete table of per-shot costs is in
[`../../docs/reference/02_combat/README.md` → “Cost of one shot”](../../docs_en/reference/02_combat/README.md).

---

<a id="8-ключевые-тайминги-сводка"></a>
## 8. Timing Summary

From 1,382 tracks in `derived/animations.json`:

| Class | `attack0` (frames) | `attack0` (g-sec) | `walk` (frames) | Real-DPS @ fast (if known) |
|---|---:|---:|---:|---:|
| Peasant (peaaus) | 18 | 0.563 | 20 | — |
| Pikeman 17th century | 14 | 0.438 | 20 | ~7-8 |
| Musketeer 17th century | 18 | 0.563 | 22 | ~6-7 (via `weapon.pause`) |
| Cavalryman | 18 | 0.563 | 26 | — |
| Cannon | 14-16 | 0.5 | (see §2.4) | by `weapon.pause = 350 frames` |
| Tower | 14 | 0.438 | (idle) | by `weapon.pause = 400 frames` |

`attack0` is the strike-animation duration. Actual attack tempo is determined
by `weapon.pause` (see §6), which is usually **longer than** `attack0` because
it includes the rest between attacks. Melee units have `weapon.pause = 0` and
strike once per animation cycle, so **the `attack0` duration is their DPS
cycle**.

The `melee_swing_sec(sid)` function in
[`parser/config.py`](../../parser/config.py) reads the actual `attack0` value
from `derived/animations.json` or falls back to the 15-frame median
(0.469 game seconds).

---

<a id="9-открытые-вопросы"></a>
## 9. Open Questions

1. **Exact `refspeed` values for every class.** The main classes are listed
   here (infantry, peasant, hardhorse, fasthorse, cannon, mortar, howitzer,
   multicannon, fishboat, ferry), but `refspeed.acl` also contains less common
   entries such as `balloondock` and the `ducha` naval classes.
2. **How does `gc_obj_speed_*` relate to `TrackPointMoveStep`.**
   These appear to be two **different** scales: `gc_obj_speed_*` is
   abstract for AI calculations, `TrackPointMoveStep` - real
   used by rendering. Their exact relationship is still unknown.
3. **`actTrackPoint` with mode `mmRelative` vs `mmAbsolute`** —
   exactly how it is used when moving in formation.
4. **`acoRandomFrame` behavior.** When enabled, units in a group begin their
   walk animations on different frames. It is not yet known whether the
   starting frame comes from `random()` or `uniqrnd`.

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
