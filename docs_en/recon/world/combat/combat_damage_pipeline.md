<a id="recon-конвейер-урона"></a>
<a id="как-рассчитывается-урон"></a>
# How Damage Is Calculated

[← How the game works](../../README.md)

This article answers a practical question: why the same shot removes
different amounts of health from different targets. It covers the six
successive damage modifiers, peacetime, scenario invulnerability, friendly
fire, and the links to formations, capture, and healing.

> **Basic tables** (weapon types, `protection[kind]` scale, numbers according
> each unit) are in [Combat and Movement](../../../reference/02_combat/README.md).
> This document explains the **process**, not the numbers.

<a id="кратко"></a>
## TL;DR

- Calculation begins when a projectile reaches its target or a melee unit
  completes its strike.
- Six consecutive modifiers: fast-cavalry reduction → shield →
  formation bonus → protection by weapon type → Priest healing →
  minimum damage.
- A headshot is a rare separate bonus for bullets and arrows; buildings
  cannot receive it.
- At least one health point is always removed, even if all
  modifiers pushed damage into a negative value.
- Peacetime and scenario invulnerability are checked **before** the formula
  and may cancel damage completely.

Readers who only need the practical result can stop at this list. The
sections below document each step with formulas, internal fields, and source
references.

---

<a id="1-точка-входа-и-предусловия"></a>
<a id="1-когда-начинается-расчёт"></a>
## 1. When damage is calculated

Calculation starts on impact. The unit animation determines the exact impact
frame; the technical chain is documented under
[animation timing §5](../../../../internals_en/engine/animation_system.md).

Before applying the formula, the game verifies that the target exists, is
still alive, and accepts normal damage [^1]. Scenario invulnerability and
peacetime are checked separately [^2]. Only then do the base damage, weapon
type, and chosen target enter the calculation. The function and all five
arguments are listed under [Technical details](#technical-details).

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
(usually `+2` while moving and `+7` while holding position). See
[Formations and Their Combat Bonuses §3](formations.md). If the target is not in a formation
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
[Target Selection and Attack-Move §7](target_selection.md) for target selection.

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
<a id="3-попадание-в-голову"></a>
## 3. Headshots

The headshot bonus uses a separate `+floor(uniqrnd × 500)` branch. It runs
**before** step 4 but does not replace it. Conditions [^5]:

1. Weapon type: `bullet` or `arrow`.
2. The target is not a building (`not bbuilding`).
3. The target is **not fast cavalry on the move** (it already receives the
   −5, see §2 step 1).
4. RNG condition: `random < 0.05` (5% chance).

If all four are true - `damage := damage + floor(target.uniqrnd × 500)` [^10].

`uniqrnd` ∈ `[0, 1)` is fixed when the unit spawns and does not change
(see [Implementation of RNG in Cossacks 3](../../../../internals_en/engine/rng_implementation.md)).
The same target therefore **always** contributes the same headshot bonus;
this is part of the deterministic synchronization model.

Then the formula continues with the usual step 4 (subtraction `protection`).
Headshot can push a weak hit (1-2 damage after shield) into
lethal (200–500 damage), instantly killing a normal infantryman
or peasant.

<a id="31-замечание-про-random"></a>
<a id="31-почему-случайный-результат-остаётся-одинаковым-у-всех-игроков"></a>
### 3.1. Why every player sees the same random result

Before checking the 5% chance, `unit.script` calls
`SetRandomKey(floor(uniqrnd × gc_MaxInt))` - reseeding global
RNG from the attacker's `uniqrnd`. This is a
**per-decision deterministic seed** (see
[Implementation of RNG in Cossacks 3 §5](../../../../internals_en/engine/rng_implementation.md)),
which guarantees that the same hit produces the same result on every client.

---

<a id="4-дружественный-огонь"></a>
## 4. Friendly fire

You cannot deliberately select an ally as a target: both automatic search
and manual attacks reject friendly units. A projectile already in flight may
still hit an ally on its path, however, and an explosion can affect anyone
inside its radius. Preventing friendly targeting is therefore not the same
as complete protection from friendly fire.

AoE projectiles are a different story. Grenade, cannonball, mortar bomb and
buckshot land at a coordinate (or at an already selected enemy target), then
affect **all** objects within the radius. Details are in §5 and §6.6 below.

Priest healing, by contrast, selects only friendly units (see
[Target Selection and Attack-Move](target_selection.md)).

Capturing an enemy object is a separate mechanic and is not based on damage. See
[building capture](../economy/capture_mechanics.md).

---

<a id="5-aoe--взрывная-волна"></a>
<a id="5-урон-по-области--взрывная-волна"></a>
## 5. AoE - blast wave

Grenades, cannonballs, and grapeshot hit a zone rather than one target. After
landing:

1. The game finds **all** objects inside the blast radius.
2. Damage to each object decreases with distance:
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
<a id="6-мирное-время"></a>
## 6. Peacetime

During the period of peace selected in the lobby, a special branch bypasses
the normal formula [^6]:

| Attacker on foreign territory? | Target on foreign territory? | What |
|---|---|---|
| No | No | The attacker dies instantly. |
| Yes | Yes | The blow goes through as usual. |
| Yes | No | The attacker dies instantly; the target takes no damage. |
| No | Yes | The attacker dies instantly; the target **also** instantly dies (weird engine). |

“Foreign territory” is determined from the ownership map created during
map generation (see [map generation](../map/map_generation_pipeline.md)).

When the lobby timer expires, the game returns to the usual six-step formula.

---

<a id="65-aoe-damage-cap--как-кучкование-защищает"></a>
<a id="65-ограничение-урона-по-области"></a>
## 6.5. Area-damage limit

Explosions from cannonballs, mortar shells, grenades, and grapeshot cover all
units within radius `r`, **but only the first N take damage** [^11]:
```
count = floor(1 + (r / 0.35)²)
```
| Weapon | Radius | Maximum units hit |
|---|---:|---:|
| Cannon, cannonball | ~1 cell | **9** |
| Bombard, bomb | ~2 cells | **33** |
| Howitzer | ~1 cell | **9** |
| Grenade | ~0.5 cell | **3** |

**Strategic conclusion:** a dense group is protected: of 50 units at
one point, at most 9 are hit by a cannonball; the rest remain untouched.
A stretched line suffers much more.

Fire arrows use another branch [^12]. If the area query returns **more than
300** units, the entire list is hit without a distance check. With **300 or
fewer**, a target must be inside radius `r`. The target-count limit does not
apply in this branch.

<a id="66-дружественный-огонь"></a>
## 6.6. Friendly fire

The damage-application stage has **no general side or owner check** [^13],
so any object on the trajectory may be affected.

**What can hit friendly units:**
- regular and fire arrows;
- musket bullets;
- grenades;
- artillery projectiles;
- AoE explosions (buckshot, cannonballs, bombs) - hit everything in a radius,
  including friendly units.

**Exceptions:**
- **Ships** have a separate safeguard [^14]: merchant ships and warships
  belonging to one player do not sink each other.
- **Towers and guns** normally do not fire if a friendly building is in the
  line of fire [^15]. This blocks the shot
  rather than preventing damage after the projectile is in flight.

The exact projectile list for which the line-of-fire check is disabled is
given under [Technical details](#technical-details).

<a id="67-подтверждённые-упрощения-формулы"></a>
## 6.7. Confirmed formula simplifications

Several mechanics familiar from other real-time strategy games are
**not implemented** in Cossacks 3. Each item is based on a direct
search of the scripts:

- **There is no cavalry charge bonus.** Cavalry deals its weapon's base
  damage.
- **There is no separate type of damage against horses.** The pikeman does not
  “×N against cavalry” multiplier. A Pikeman is effective against a Reiter
  because pikes deal ordinary damage against cavalry's usually low
  protection from that weapon type.
- **There is no Drummer aura.** The Drummer, 17th century occupies a
  formation slot but grants no damage, speed, or morale bonuses.
- **The grenadier has no special trajectory.** The grenadier uses
  the common area-damage path (the `cannonball` type with a blast radius).
- **There is no stealth or invisibility.** All units are visible inside the
  enemy's vision radius.

Consequently, formation is the only way to multiply damage. There are
no hidden positional bonuses apart from high ground (see
[Ranged-Unit Behavior §7](ranged_units_behavior.md)) and hold position.
Upgrades, formation, and the match between weapon type
and protection type make up the entire combat calculation.

---

<a id="7-сценарная-неуязвимость"></a>
## 7. Scenario invulnerability

Units with infinite health, decorative characters, and scenario helper
objects bypass the entire calculation [^2]. Campaigns and Historical Battles
use this for:

- Bosses that cannot be killed through damage (only through a trigger).
- Decorative civilians (peasants running around the map in
  missions that the player should not accidentally kill).
- Scenario “beacons” - invisible trigger objects.

This protection is active only in scenarios. It does not apply in Skirmish
or Multiplayer.

---
<a id="8-реакция-ai-отряда-на-удар"></a>
<a id="8-реакция-отряда-под-управлением-ии-на-удар"></a>
## 8. AI squad reaction to a strike

After the target loses health, the game checks whether it belongs to a squad.
If the squad
is in "idle/hold" mode, puts the entire squad into
“attack whoever hit us” mode. In effect, **one hit
wakes up the entire squad** - this is part of the “realistic” mechanics of Cossacks,
when a salvo on one unit immediately triggers the response of all
neighbors. See details in
[Target Selection and Attack-Move §6](target_selection.md).

---

<a id="технические-подробности"></a>
## Technical details

The main handler is `_misc_DoDamage(goHnd, trgHnd, indamage, weapind,
weapkind)` [^1].

| Argument or field | Meaning |
|---|---|
| `goHnd` | attacker handle; may be `0` for damage without a source |
| `trgHnd` | target handle; the handler exits when it is `0` |
| `indamage` | base weapon damage |
| `weapind` | weapon-slot index |
| `weapkind` | weapon type from `gc_obj_weapon_kind_*` |
| `pobj2`, `bdead` | target existence and death state |
| `gbool_peacemode` | active peacetime |
| `gc_gameplay_infinitehp`, `gScenario.bactive` | scenario invulnerability |
| `_unit_IsOnEnemyTerritory`, `OwnerMap`, `FillOwnerMap` | foreign-territory check |
| `_misc_DoRoundDamage` | area damage |
| `bcheckfriendonline`, `_misc_IsBuildingInRay` | friendly-building line-of-fire check |
| `bcharging`, `firsthit`, `chargebonus`, `bstealth` | charge and stealth flags absent from the scripts |

The friendly-building line-of-fire check is explicitly disabled for
`STRELA`, `OSTRELA`, `SHOTMUSKET`, `SHOTBLOCKHOUSE`, `NUCLGRE`,
`PSMPOINTTPUS`, `DIMMORT1`, `DIMMORT2NEW`, `PSMPOINTT`, and `DIMMORT2KOR`.

<a id="9-открытые-эмпирические-вопросы"></a>
<a id="открытые-эмпирические-вопросы"></a>
## Open empirical questions

1. **Exact formula for the area-damage cap.** The current evidence suggests
   `cap = 3..5` unit-equivalents. Verify it with grenade shots against groups
   of 1, 5, 10, 20, and 50 units.
2. **The fourth peacetime case** (attacker on friendly territory, target on
   foreign territory, both die) looks like a script defect and needs an
   in-game test. If confirmed, add it to
   [known limitations](../../../../internals_en/project/known_issues.md).
3. **Headshots after negative intermediate damage.** If steps 1–4 reduce
   `damage` below zero and the headshot branch adds `+200`, determine whether
   the result is `200` or `max(1, ...) + 200`. The available script fragment
   does not make the exact order unambiguous.

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
      [Combat and Movement § Damage calculation](../../../reference/02_combat/README.md#как-считается-урон)).

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
