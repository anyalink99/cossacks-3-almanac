<a id="recon-конвейер-урона"></a>
<a id="как-рассчитывается-урон"></a>
# How Damage Is Calculated

[← How the game works](../../README.md)

Detailed analysis: what exactly happens between the moment when the unit
fires a projectile, and the moment when the target's health decreases.
Six successive steps of the formula, edge cases (peacetime,
scenario invulnerability, friendly fire), and interaction points
with adjacent systems (formations, capture, and healing).

> **Basic tables** (weapon types, `protection[kind]` scale, numbers according
> each unit) are in [`reference/02_combat/README.md`](../../../reference/02_combat/README.md).
> This document explains the **process**, not the numbers.

<a id="кратко"></a>
## TL;DR

- Entry point - `_misc_DoDamage(goHnd, trgHnd, indamage, weapind, weapkind)` [^1].
  It is called whenever a projectile reaches its target or a melee
  unit completes its attack animation. The exact impact frame is defined
  in the unit's `.acl` file through the `OnAclAnimationReachedAttack` callback;
  see [`internals/engine/animation_system.md` §5](../../../../internals_en/engine/animation_system.md).
- Six consecutive modifiers: fast-cavalry reduction → shield →
  formation bonus → protection by weapon type → Priest healing →
  minimum damage.
- Headshot (`+floor(uniqrnd × 500)`) is applied in a separate branch,
  only for `bullet`/`arrow` and only for non-buildings.
- At least one health point is always removed, even if all
  modifiers pushed damage into a negative value.
- Peacetime (`gbool_peacemode`) and scenarios with
  `hp >= gc_gameplay_infinitehp` are processed **before** the formula and
  may skip the calculation completely.

---

<a id="1-точка-входа-и-предусловия"></a>
## 1. Entry point and preconditions

`_misc_DoDamage` takes five arguments:

| Parameter | What |
|---|---|
| `goHnd` | Handle of the attacker (can be `0` - for example, natural damage, AoE without a source). |
| `trgHnd` | Target handle. If it is `0`, the function exits immediately. |
| `indamage` | Raw weapon damage, equivalent to `weapon.damage` in `data.json`. |
| `weapind` | Index of the particular weapon slot (primary or secondary). |
| `weapkind` | Weapon type from `gc_obj_weapon_kind_*`: Pike Attack (`pike`), Sword Attack (`sword`), Fire Power (`bullet`), Arrow Attack (`arrow`), Cannonball Damage (`cannonball`), Grapeshot Damage (`cannister`), or grenade (`grenade`). |

Exit preconditions **before** formula:

1. `pobj2 = nil` (target not found in `gPlayer[*].objbase[*][*]`) → exit.
2. The target is already dead (`bdead`) → exit.
3. Scenario invulnerability: `gScenario.bactive AND (hp >= gc_gameplay_infinitehp)` or
   `not GetGameObjectPlayableObjectByHandle(trgHnd)` → exit [^2].
4. Peacetime (`gbool_peacemode`) - processing in a separate branch, see §6.

---

<a id="2-шаги-формулы"></a>
## 2. Formula steps

After these checks, the main calculation begins. At each step the
`damage` variable (initially `damage := indamage`) is adjusted.

<a id="шаг-1-пирс-быстрой-конницы"></a>
<a id="шаг-1-снижение-урона-по-быстрой-коннице"></a>
### Step 1. Fast-cavalry damage reduction

If the target is light cavalry on the move (`usage = gc_obj_usage_fasthorse`,
`statestag` contains `gc_statetag_move_walk`) and the projectile is a bullet or
arrow, the script **subtracts 5 points** before all other
calculations [^1]. This represents a glancing hit.

`bCanHeadShot` is true only for `bullet` or `arrow` and only if
the target is not a building (`not bbuilding`). For spear/sword/cannonball
this step is skipped.

<a id="шаг-2-щит-цели"></a>
### Step 2: Target Shield

If the building is completed (`bbuilt = True`), the full
target's `shield` is subtracted; if it is still under construction
(`bbuilt = False`), only one third, `shield DIV 3`, is subtracted [^7].
`shield` is taken from `data.json` [^3].

This makes it worthwhile to attack an enemy Tower **before it is
completed**, while most of its protection is not yet active.

<a id="шаг-3-бонус-строя-цели"></a>
### Step 3. Target's formation bonus

If the target belongs to a formation (`squad >= 0`), the script
pulls `pSquad2` from `gPlayer[target.pl].squads` and applies
formation shield bonus: `fAddShieldHold` when `fHoldMode = True`,
otherwise `fAddShield`. The result is subtracted from damage
(usually `+2` on the go and `+7` in hold mode). See
[`formations.md` §3](formations.md). If the target is not in a formation
(`squad = -1`), step is skipped.

<a id="шаг-4-защита-по-типу-оружия"></a>
### Step 4. Protection by weapon type

`target.protection[weapkind]` is subtracted from damage - an array of 7
values according to `gc_obj_weapon_kind_*` [^4]. For example, an infantryman with
light protection `protection[bullet] = 1`, `protection[arrow] = 2`,
`protection[pike] = 0`. For heavy cavalry `protection[bullet] = 1`,
but `protection[sword] = 4`, so a sabre strike must first overcome
four points of armour.

<a id="шаг-5-лечение-священника-исключение"></a>
<a id="шаг-5-лечение-капелланом-исключение"></a>
### Step 5. Priest healing (exception)

If **attacker** is a priest (`bpriest = True`), all steps 1-4
are skipped. Instead `target.hp := target.hp + indamage`,
limited to `maxhp` [^8]. In other words, the Priest **adds**
target's health instead of dealing damage. See
[`target_selection.md` §7](target_selection.md) for target selection.

<a id="шаг-6-клик-минимума"></a>
<a id="шаг-6-минимальный-урон"></a>
### Step 6. Minimum damage

If `damage < 1` after steps 1–4, it is raised to 1; then
`target.hp := target.hp − damage` [^9]. At least **one health point**
is always removed, even if the modifiers reduced damage to zero or
below. This guarantees non-zero damage even for a lone veteran melee
unit attacking heavily protected infantry in a holding formation.

After decreasing `hp`, the script checks for death. If `hp <= 0`, it
sets `bdead := True` and calls `_misc_OnDeath`, which:
- `+kill` is counted to the attacker,
- score points are awarded (`kill = +2 × cost`),
- death animation starts,
- a slot in the formation is freed,
- `bfamine` is checked because a food consumer has been removed (see
  [hunger and rebellion](../economy/hunger_and_rebellion.md)).

---

<a id="3-хедшот-отдельная-ветка-flooruniqrnd--500"></a>
## 3. Headshot: separate branch `+floor(uniqrnd × 500)`

The headshot branch runs **before** step 4 but does not replace it. Conditions [^5]:

1. Weapon type: `bullet` or `arrow`.
2. The target is not a building (`not bbuilding`).
3. The target is **not fast cavalry on the move** (it already receives the
   −5, see §2 step 1).
4. RNG condition: `random < 0.05` (5% chance).

If all four are true - `damage := damage + floor(target.uniqrnd × 500)` [^10].

`uniqrnd` ∈ `[0, 1)` is fixed when the unit spawns and does not change
(see [`internals/engine/rng_implementation.md`](../../../../internals_en/engine/rng_implementation.md)).
The same target therefore **always** contributes the same headshot bonus;
this is part of the deterministic synchronization model.

Then the formula continues with the usual step 4 (subtraction `protection`).
Headshot can push a weak hit (1-2 damage after shield) into
lethal (200–500 damage), instantly killing a normal infantryman
or peasant.

<a id="31-замечание-про-random"></a>
### 3.1. Note about `random`

Before checking the 5% chance, `unit.script` calls
`SetRandomKey(floor(uniqrnd × gc_MaxInt))` - reseeding global
RNG from the attacker's `uniqrnd`. This is a
**per-decision deterministic seed** (see
[`internals/engine/rng_implementation.md` §5](../../../../internals_en/engine/rng_implementation.md)),
which guarantees that the same hit produces the same result on every client.

---

<a id="4-дружественный-огонь"></a>
## 4. Friendly fire

Directly targeting an ally in Cossacks 3 is impossible: target selection
(`_unit_SearchEnemyInCell`) filters friends/allies through
`enemyplmask` even before the candidate stage, and the projectile simply
is never launched. You therefore cannot manually fire at friendly units.

AoE projectiles are a different story. Grenade, cannonball, mortar bomb and
buckshot land at a coordinate (or at an already selected enemy
target), after which the script finds **all** objects within the radius through
`GetGameObjectsInArea` and applies `_misc_DoDamage` to each. On
At this stage the `enemyplmask` filter no longer applies, so friendly
units can also be hit. Details are in §5 and §6.6 below. Friendly fire
in Cossacks 3 is therefore a side effect of area damage and occurs
only for artillery and grenade launchers.

Priest healing, by contrast, only affects friendly units: `bpriest`
uses `scanmode = 1` (see
[`target_selection.md` §7](target_selection.md)),
which requires a `myplmask` match.

Capturing an enemy unit (`bcapture`) is a separate mechanic and is
not based on damage. See
[building capture](../economy/capture_mechanics.md).

---

<a id="5-aoe--взрывная-волна"></a>
<a id="5-урон-по-области--взрывная-волна"></a>
## 5. AoE - blast wave

Shells with `gc_aoe_radius > 0` (grenade, cannonball, buckshot) hit
not one target, but a zone. After landing:

1. The script finds **all** objects within the AoE radius (via native
   `GetGameObjectsInArea`, see
   [`internals/engine/native_api.md` §2.1](../../../../internals_en/engine/native_api.md)).
2. For every affected object, the same function is called:
   `_misc_DoDamage`, but `indamage` decreases by distance:
   ```
   damage_at_d = indamage × (1 − d / radius)
   ```
   where `d` is the Euclidean distance to the epicentre. Total damage
   across all affected targets is limited (see §6.5 below).
3. Friendly fire from AoE is **possible**: if your own infantry is standing
   next to an enemy, the grenade will hit both.

AoE damage cap is a limit on the total damage to a bunch of targets: even
if 30 units are within the radius, the total damage cannot exceed
`damage × cap` (typically `cap = 3..5` equivalent units). This
prevents one grenade from instantly destroying a dense group.

---

<a id="6-мирное-время-gboolpeacemode"></a>
## 6. Peacetime (`gbool_peacemode`)

If the global flag `gbool_peacemode = True` (peace-time is on
at the start of the game), the formula is skipped by a special branch [^6]. Behavior:

| Attacker on foreign territory? | Target on foreign territory? | What |
|---|---|---|
| No | No | The attacker dies instantly (`hp := 0`). |
| Yes | Yes | The blow goes through as usual. |
| Yes | No | The attacker dies instantly; the target takes no damage. |
| No | Yes | The attacker dies instantly; the target **also** instantly dies (weird engine). |

“Foreign territory” is determined via `_unit_IsOnEnemyTerritory(handle)`
- this checks `OwnerMap`, filled during map generation
(see [map generation](../map/map_generation_pipeline.md) about
`FillOwnerMap`).

Peace time ends when `peacetime`-seconds have elapsed in
lobby (`gbool_peacemode := False`), and the formula returns to
the usual six-step scheme.

---

<a id="65-aoe-damage-cap--как-кучкование-защищает"></a>
<a id="65-ограничение-урона-по-области"></a>
## 6.5. Area-damage limit

Explosions (cannon ball, mortar bomb, grenade, buckshot) hit
all units within the radius of `r` through `_misc_DoRoundDamage`, **but only
first N take damage** [^11]:
```
count = floor(1 + (r / 0.35)²)
```
| Weapon | Radius | Maximum units hit |
|---|---:|---:|
| Cannon, cannonball | ~1 tile | **9** |
| Bombard, bomb | ~2 tiles | **33** |
| Howitzer | ~1 tile | **9** |
| Grenade | ~0.5 tile | **3** |

**Strategic conclusion:** a dense group is protected: of 50 units at
one point, at most 9 are hit by a cannonball; the rest remain untouched.
A stretched line suffers much more.

Fire Arrow Attack (`barrow`) uses another branch: `(listcount
> 300) or (dist < r)` [^12]. If in the list collected by area
**more than 300** units - the entire list is hit without
distance checks. If **300 or less** - you need `dist < r`.
The cap `count` is not used in this thread.

<a id="66-дружественный-огонь"></a>
## 6.6. Friendly fire

In `_misc_DoDamage` **no check for side/owner** [^13] -
damage is applied to any object along the trajectory.

**What can hit friendly units:**
- Arrows (`STRELA`) and fire arrows (`OSTRELA`).
- Musket bullets (`SHOTMUSKET`).
- Grenades (`NUCLGRE`).
- Artillery (`PSMPOINTTPUS`, `DIMMORT1`, `DIMMORT2NEW`,
  `PSMPOINTT`, `DIMMORT2KOR`).
- AoE explosions (buckshot, cannonballs, bombs) - hit everything in a radius,
  including our own.

**Exceptions:**
- **Ships**: separate protection `// prevent ships from friendly
  fire` [^14] - merchants and warships of one player do not sink
  each other.
- **Towers and guns** with `bcheckfriendonline = True` (default)
  do not fire if there is a friendly building in the line of fire -
  via `_misc_IsBuildingInRay` [^15]. But it blocks the shot
  rather than preventing damage after the projectile is in flight.

**List of weapons with checks explicitly DISABLED
`bcheckfriendonline`** (they shoot through their buildings):
`STRELA`, `OSTRELA`, `SHOTMUSKET`, `SHOTBLOCKHOUSE`, `NUCLGRE`,
`PSMPOINTTPUS`, `DIMMORT1`, `DIMMORT2NEW`, `PSMPOINTT`,
`DIMMORT2KOR` - that is, all arrows, musket bullets and almost all
artillery.

<a id="67-подтверждённые-упрощения-формулы"></a>
## 6.7. Confirmed formula simplifications

Several mechanics familiar from other real-time strategy games are
**not implemented** in Cossacks 3. Each item is based on a direct
search of the scripts:

- **There is no bonus for cavalry charge.** Search `bcharging` /
  `firsthit` / `chargebonus` doesn't find anything. Cavalry Damage =
  its weapon's base damage.
- **There is no separate type of damage against horses.** The pikeman does not
  multiplier "×N against cavalry". Pikeman effectiveness against
  a Reiter is simply `weapon.damage(pike)` against
  `target.protection[pike]`; cavalry usually have low protection.
- **There is no Drummer aura.** The Drummer, 17th century occupies a
  formation slot but grants no damage, speed, or morale bonuses.
- **The grenadier has no special trajectory.** The grenadier uses
  the common area-damage path (the `cannonball` type with a blast radius).
- **No stealth or invisibility.** All units are visible in the zone
  of sight. There is no `bstealth` flag in the code.

Consequently, formation is the only way to multiply damage. There are
no hidden positional bonuses apart from high ground (see
[`ranged_units_behavior.md` §7](ranged_units_behavior.md)) and
`standground`. Upgrades, formation, and the match between weapon type
and protection type make up the entire combat calculation.

---

<a id="7-сценарная-неуязвимость"></a>
## 7. Scenario invulnerability

Units with `hp >= gc_gameplay_infinitehp` (∞ HP) or with
`not GetGameObjectPlayableObjectByHandle()` (decorative NPCs,
trigger objects) - skip the entire [^2] pipeline. This
used in Campaign and Historical Battles for:

- Bosses that cannot be killed through damage (only through a trigger).
- Decorative civilians (peasants running around the map in
  missions that the player should not accidentally kill).
- Scenario “beacons” - invisible trigger objects.

Active only with `gScenario.bactive` - that is, in skirmish and
this mechanism does not operate in Multiplayer.

---
<a id="8-реакция-ai-отряда-на-удар"></a>
<a id="8-реакция-отряда-под-управлением-ии-на-удар"></a>
## 8. AI squad reaction to a strike

After `_misc_DoDamage` has reduced the target's health, a separate
branch checks whether the target belongs to a squad, and if the squad
is in "idle/hold" mode, puts the entire squad into
“I attack the one who hits” (`_squad_*`-function). Effect: **one hit
wakes up the entire squad** - this is part of the “realistic” mechanics of Cossacks,
when a salvo on one unit immediately triggers the response of all
neighbors. See details in
[`target_selection.md` §6](target_selection.md).

---

<a id="9-открытые-эмпирические-вопросы"></a>
## 9. Open empirical questions

1. **Exact formula for AoE damage cap**: it looks like `cap = 3..5`
   units equivalent to total damage, but the coefficient is in the code
   not proofread. Measure through a series of grenade shots at a group
   from 1, 5, 10, 20, 50 units and check.
2. **Clear conditions `peacemode` type 4** (attacking on his own,
   target on someone else → both die): this looks like a bug in the script,
   needs to be confirmed. If so, it’s worth adding to `known_issues.md`.
3. **Taking into account headshots with negative base damage.** If step 1–4
   already reduced `damage` to `< 0`, and then headshot added `+200`,
   will it be `damage = 200` or `damage = max(1, ...) + 200`?
   The order of steps is unreadable in the code without complete disassembly
   branches `_misc_DoDamage`.

---

<a id="источники"></a>
## Sources

[^1]: `data/scripts/lib/miscext2.script:_misc_DoDamage`. Home
      damage calculation function, ~250 lines. Accepts 5 parameters,
      goes through all the steps sequentially.

[^2]: `_misc_DoDamage`, start of procedure:
      `if (gScenario.bactive) and ((target.hp >= gc_gameplay_infinitehp)
       or (not GetGameObjectPlayableObjectByHandle(trgHnd))) then exit;`

[^3]: `data.json`, field `unit.shield` or `building.shield`. For
      for units the range is 0–4, for buildings – 0–6.

[^4]: `data.json`, array `unit.protection[7]` or
      `building.protection[7]` by indexes
      `gc_obj_weapon_kind_*` (see also
      [`reference/02_combat/README.md` § Damage calculation](../../../reference/02_combat/README.md#как-считается-урон)).

[^5]: `data/scripts/lib/miscext2.script:_misc_DoDamage`, branch
      `if (bCanHeadShot) and (random < 0.05) then ...`.
      Validation `bCanHeadShot` is true for `arrow`/`bullet` against
      non-buildings.

[^6]: `data/scripts/lib/miscext2.script:_misc_DoDamage`, branch
      `if gbool_peacemode then ...`. Uses
      `_unit_IsOnEnemyTerritory(handle, pobj)` for verification.

[^7]: `data/scripts/lib/miscext2.script:_misc_DoDamage`, step 2:
      ```pascal
      if (TObj(pobj2).bbuilt) then
         damage := damage − TObjBase(pobjbase2).shield
      else
         damage := damage − TObjBase(pobjbase2).shield DIV 3;
      ```
[^8]: `data/scripts/lib/miscext2.script:_misc_DoDamage`, branch
      `bpriest`:
      ```pascal
      if (TObjProp(pobjprop).bpriest) then
      begin
         damage := indamage;
         TObj(pobj2).hp := TObj(pobj2).hp + damage;
         if (TObj(pobj2).hp >= TObjBase(pobjbase2).maxhp) then
            TObj(pobj2).hp := TObjBase(pobjbase2).maxhp;
      end;
      ```
[^9]: `data/scripts/lib/miscext2.script:_misc_DoDamage`, step 6:
      ```pascal
      if (damage < 1) then damage := 1;
      TObj(pobj2).hp := TObj(pobj2).hp − damage;
      if (TObj(pobj2).hp <= 0) then ... // OnDeath
      ```
[^10]: `data/scripts/lib/miscext2.script:_misc_DoDamage`,
       headshot branch: `damage := damage + floor(TObj(pobj2).uniqrnd
       × 500)`. Probability check: `random < 0.05`
       (5% chance).

[^11]: `data/scripts/lib/miscext2.script:576` —
       `_misc_DoRoundDamage`. Cap formula: `count = floor(1 +
       (radius / 0.35)²)`.

[^12]: `data/scripts/lib/miscext2.script:589` - branch for
       fire arrows (`barrow`): `(listcount > 300) or (dist < r)`.

[^13]: `data/scripts/lib/miscext2.script:274` - function
       `_misc_DoDamage` starts without side check;
       Friendly shooting is possible.

[^14]: `data/scripts/lib/weapon.script:482-492` - comment
       `// prevent ships from friendly fire`.

[^15]: `data/scripts/lib/unit.script:7686-7714` —
       `_misc_IsBuildingInRay`.
