<a id="recon-конвейер-урона"></a>
<a id="как-рассчитывается-урон"></a>
# How Damage Is Calculated

[← How the game works](../../README.md)

This article answers a practical question: why the same shot removes
different amounts of health from different targets. It covers the six
successive damage modifiers, peacetime, scenario invulnerability, friendly
fire, and the links to formations, capture, and healing.

> **Basic tables** (weapon types, protection against each type, and values for
> individual units) are in
> [Combat and Movement](../../../reference/02_combat/README.md).
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

<a id="практическая-схема"></a>
## Practical Sequence

An ordinary hit follows a straightforward sequence:

1. The game checks whether scenario rules and peace time allow damage.
2. A bullet or arrow loses 5 damage against moving light cavalry.
3. The target's general armor is subtracted. A building under construction
   receives only one third of its finished armor.
4. A formation defense bonus is subtracted when the target belongs to a
   squad.
5. Protection against the particular weapon type—such as bullet, arrow,
   pike, or sword—is subtracted.
6. If the result falls below one, the target still loses one health point.

The attacker's formation adds its own damage bonus separately. A Priest
uses the same interaction point to heal an ally up to maximum health instead
of causing damage.

Bullets and arrows have a 5% chance to receive a large headshot bonus.
Buildings and moving light cavalry are excluded. The trigger comes from
the shared `random` stream, while the bonus amount comes from the target's
persistent individual value.

Area-damage projectiles lose power with distance from the center and may hit
allies. One explosion can affect only a limited number of targets, so a dense
group does not take full damage on every unit.

<a id="техническое-приложение"></a>
## Technical Appendix

The sections below preserve the exact calculation order, internal fields,
and exceptions. The player-facing sequence is summarized above.

<a id="1-точка-входа-и-предусловия"></a>
<a id="1-когда-начинается-расчёт"></a>
<a id="1-when-damage-is-calculated"></a>
<a id="когда-начинается-расчёт"></a>
### When damage is calculated

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
<a id="2-formula-steps"></a>
<a id="шаги-формулы"></a>
### Formula steps

After these checks, the main calculation begins. At each step the
`damage` variable (initially `damage := indamage`) is adjusted.

<a id="шаг-1-пирс-быстрой-конницы"></a>
<a id="шаг-1-снижение-урона-по-быстрой-коннице"></a>
#### Step 1. Fast-cavalry damage reduction

If the target is light cavalry on the move (`usage = gc_obj_usage_fasthorse`,
`statestag` contains `gc_statetag_move_walk`) and the projectile is a bullet or
arrow, the script **subtracts 5 points** before all other
calculations [^1]. This represents a glancing hit.

`bCanHeadShot` is true only for `bullet` or `arrow` and only if
the target is not a building (`not bbuilding`). For spear/sword/cannonball
this step is skipped.

<a id="шаг-2-щит-цели"></a>
#### Step 2. Target shield

If the building is completed (`bbuilt = True`), the full
target `shield` is subtracted; if it is still under construction
(`bbuilt = False`), only one third, `shield DIV 3`, is subtracted [^7].
`shield` is taken from `data.json` [^3].

This makes it worthwhile to attack an enemy Tower **before it is
completed**, while most of its protection is not yet active.

<a id="шаг-3-бонус-строя-цели"></a>
#### Step 3. Target's formation bonus

If the target belongs to a formation (`squad >= 0`), the script
pulls `pSquad2` from `gPlayer[target.pl].squads` and applies
formation shield bonus: `fAddShieldHold` when `fHoldMode = True`,
otherwise `fAddShield`. The result is subtracted from damage
(usually `+2` while moving and `+7` while holding position). See
[Formations and Their Combat Bonuses §3](formations.md). If the target is not in a formation
(`squad = -1`), step is skipped.

<a id="шаг-4-защита-по-типу-оружия"></a>
#### Step 4. Protection by weapon type

`target.protection[weapkind]` is then subtracted. This is one of seven values
indexed by `gc_obj_weapon_kind_*` [^4]. For example, an infantryman with
light protection `protection[bullet] = 1`, `protection[arrow] = 2`,
`protection[pike] = 0`. For heavy cavalry `protection[bullet] = 1`,
but `protection[sword] = 4`, so a sabre strike must first overcome
four points of armor.

<a id="шаг-5-лечение-священника-исключение"></a>
<a id="шаг-5-лечение-капелланом-исключение"></a>
#### Step 5. Priest healing (exception)

If the **attacker** is a Priest (`bpriest = True`), steps 1–4
are skipped. Instead `target.hp := target.hp + indamage`,
limited to `maxhp` [^8]. In other words, the Priest **adds**
health to the target instead of dealing damage. See
[Target Selection and Attack-Move §7](target_selection.md) for target selection.

<a id="шаг-6-клик-минимума"></a>
<a id="шаг-6-минимальный-урон"></a>
#### Step 6. Minimum damage

If `damage < 1` after steps 1–4, it is raised to 1; then
`target.hp := target.hp − damage` [^9]. At least **one health point**
is always removed, even if the modifiers reduced damage to zero or
below. This guarantees non-zero damage even for a lone veteran melee
unit attacking heavily protected infantry in a holding formation.

After decreasing `hp`, the script checks for death. If `hp <= 0`, it
sets `bdead := True` and calls `_misc_OnDeath`, which:

- credits the attacker with a kill;
- awards score (`+2 × the target's base point value`);
- starts the death animation;
- frees the unit's formation slot;
- checks `bfamine` because one food consumer has been removed (see
  [hunger and rebellion](../economy/hunger_and_rebellion.md)).

---

<a id="3-хедшот-отдельная-ветка-flooruniqrnd--500"></a>
<a id="3-попадание-в-голову"></a>
<a id="3-headshots"></a>
<a id="попадание-в-голову"></a>
### Headshots

The headshot bonus uses a separate `+floor(uniqrnd × 500)` branch. It is
added **after** weapon-type protection but before the minimum-damage clamp.
Conditions [^5]:

1. Weapon type: `bullet` or `arrow`.
2. The target is not a building (`not bbuilding`).
3. The target is **not fast cavalry on the move** (it already receives the
   −5; see “Fast-cavalry damage reduction” above).
4. RNG condition: `random < 0.05` (5% chance).

If all four conditions are true,
`damage := damage + floor(target.uniqrnd × 500)` [^10].

`uniqrnd` ∈ `[0, 1)` is fixed when the unit spawns and does not change
(see [Implementation of RNG in Cossacks 3](../../../../internals_en/engine/rng_implementation.md)).
The same target therefore **always** contributes the same headshot bonus;
the amount is fixed, but the outcome of the 5% check is not.

The bonus is added after `shield`, formation modifiers, and `protection`.
A headshot can therefore turn a weak hit—only one or two points after
protection—into 200–500 damage, enough to kill ordinary infantry or a
Peasant instantly.

<a id="31-замечание-про-random"></a>
<a id="31-почему-случайный-результат-остаётся-одинаковым-у-всех-игроков"></a>
<a id="почему-случайный-результат-остаётся-одинаковым-у-всех-игроков"></a>
<a id="31-why-every-player-sees-the-same-random-result"></a>
<a id="что-случайно-а-что-фиксировано"></a>
#### What is random and what stays fixed

The trigger and the bonus amount come from different sources. The 5% check
reads the shared `random` stream without a preceding `SetRandomKey`. If it
succeeds, the added amount is determined by the target's stored `uniqrnd`.

The trigger therefore depends on the full preceding history of `random`
calls. Stored `uniqrnd` alone cannot reproduce it: a separate reload or
replay does not have to produce a headshot at the same moment. See
[Implementation of RNG in Cossacks 3 §5](../../../../internals_en/engine/rng_implementation.md)
for details.

---

<a id="4-дружественный-огонь"></a>
<a id="66-дружественный-огонь"></a>
<a id="4-friendly-fire"></a>
<a id="66-friendly-fire"></a>
<a id="дружественный-огонь"></a>
### Friendly fire

You cannot deliberately select an ally as a target: both automatic search
and manual attacks reject friendly units. A projectile already in flight may
still hit an ally on its path, however, and an explosion can affect anyone
inside its radius. Preventing friendly targeting is therefore not the same
as complete protection from friendly fire.

The damage-application stage has **no general side or owner check** [^13].
Friendly units can be hit by:

- regular and fire arrows;
- musket bullets;
- grenades;
- artillery projectiles;
- area-damage explosions—grapeshot, cannonballs, and bombs affect everything
  inside their radius.

There are two important exceptions:

- **Ships** have a separate safeguard [^14]: merchant ships and warships
  belonging to one player do not sink each other.
- **Towers and guns** normally do not fire if a friendly building is in the
  line of fire [^15]. This blocks the shot itself, but does not cancel damage
  from a projectile that is already in flight.

AoE projectiles are a different story. Grenade, cannonball, mortar bomb and
buckshot land at a coordinate (or at an already selected enemy target), then
affect **all** objects within the radius. See
[Area damage and blast waves](#area-damage-and-blast-waves).

The exact projectile list for which the line-of-fire check is disabled is
given under [Technical details](#technical-details).

Priest healing, by contrast, selects only friendly units (see
[Target Selection and Attack-Move](target_selection.md)).

Capturing an enemy object is a separate mechanic and is not based on damage. See
[building capture](../economy/capture_mechanics.md).

---

<a id="5-aoe--взрывная-волна"></a>
<a id="5-урон-по-области--взрывная-волна"></a>
<a id="5-area-damage-and-blast-waves"></a>
<a id="урон-по-области--взрывная-волна"></a>
### Area damage and blast waves

Grenades, cannonballs, and grapeshot hit a zone rather than one target. After
landing:

1. The game finds **all** objects inside the blast radius.
2. Damage to each object decreases with distance:
   ```
   damage_at_d = indamage × (1 − d / radius)
   ```
   where `d` is the Euclidean distance to the epicentre. The number of
   objects that receive this damage is limited (see
   [Area-damage limit](#area-damage-limit)).
3. Friendly fire from AoE is **possible**: if your own infantry is standing
   next to an enemy, the grenade will hit both.

---

<a id="6-мирное-время-gboolpeacemode"></a>
<a id="6-мирное-время"></a>
<a id="6-peacetime"></a>
<a id="мирное-время"></a>
### Peacetime

During the period of peace selected in the lobby, a special branch bypasses
the normal formula [^6]:

| Attacker on foreign territory? | Target on foreign territory? | Result |
|---|---|---|
| No | No | The attacker dies instantly. |
| Yes | Yes | The blow goes through as usual. |
| Yes | No | The attacker dies instantly; the target takes no damage. |

“Foreign territory” is determined from the ownership map created during
map generation (see [map generation](../map/map_generation_pipeline.md)).

When the lobby timer expires, the game returns to the usual six-step formula.

---

<a id="65-aoe-damage-cap--как-кучкование-защищает"></a>
<a id="65-ограничение-урона-по-области"></a>
<a id="65-area-damage-limit"></a>
<a id="ограничение-урона-по-области"></a>
### Area-damage limit

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

<a id="67-подтверждённые-упрощения-формулы"></a>
<a id="67-чего-в-боевой-формуле-нет"></a>
<a id="67-mechanics-absent-from-the-combat-formula"></a>
<a id="чего-в-боевой-формуле-нет"></a>
### Mechanics absent from the combat formula

Several mechanics familiar from other real-time strategy games are
**not implemented** in Cossacks 3:

- **There is no cavalry charge bonus.** Cavalry deals its weapon's base
  damage.
- **There is no separate type of damage against horses.** A Pikeman has no
  “×N against cavalry” multiplier. It is effective against a Reiter
  because pikes deal ordinary damage against cavalry's usually low
  protection from that weapon type.
- **There is no Drummer aura.** The Drummer, 17th century occupies a
  formation slot but grants no damage, speed, or morale bonuses.
- **The Grenadier has no special trajectory.** The Grenadier uses
  the common area-damage path (the `cannonball` type with a blast radius).
- **There is no stealth or invisibility.** All units are visible inside the
  enemy's vision radius.

Consequently, formation is the only squad-wide way to modify damage. There
are no hidden positional bonuses apart from high ground (see
[Ranged-Unit Behavior §7](ranged_units_behavior.md)) and hold position.
Upgrades, formation, and the match between weapon type
and protection type make up the entire combat calculation.

---

<a id="7-сценарная-неуязвимость"></a>
<a id="7-scenario-invulnerability"></a>
<a id="сценарная-неуязвимость"></a>
### Scenario invulnerability

Units with infinite health, decorative characters, and scenario helper
objects bypass the entire calculation [^2]. Campaigns and Historical Battles
use this for:

- bosses that cannot be killed through damage and instead require a trigger;
- decorative civilians that the player should not accidentally kill;
- scenario “beacons”—invisible trigger objects.

This protection is active only in scenarios. It does not apply in random-map
or multiplayer matches.

---
<a id="8-реакция-ai-отряда-на-удар"></a>
<a id="8-реакция-отряда-под-управлением-ии-на-удар"></a>
<a id="8-ai-squad-reaction-to-a-strike"></a>
<a id="реакция-отряда-под-управлением-ии-на-удар"></a>
### AI squad reaction to a strike

After the target loses health, the game checks whether it belongs to a squad.
If the squad is idle or holding position, the attack puts the entire squad
into a retaliatory state. In effect, **one hit wakes up the whole squad**:
a salvo against one member immediately provokes the others. See
[Target Selection and Attack-Move §6](target_selection.md).

---

<a id="technical-details"></a>
<a id="технические-подробности"></a>
<a id="внутренняя-функция-и-поля"></a>
### Internal function and fields

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

<a id="источники"></a>
## Sources

[^1]: `data/scripts/lib/miscext2.script:_misc_DoDamage` — the main
      damage-calculation function, about 250 lines long. It accepts five
      arguments and applies the modifiers in sequence.

[^2]: `_misc_DoDamage`, start of procedure:
      `if (gScenario.bactive) and ((target.hp >= gc_gameplay_infinitehp)
       or (not GetGameObjectPlayableObjectByHandle(trgHnd))) then exit;`

[^3]: `data.json`, field `unit.shield` or `building.shield`. Values range
      from 0–4 for units and 0–6 for buildings.

[^4]: `data.json`, array `unit.protection[7]` or
      `building.protection[7]` by indexes
      `gc_obj_weapon_kind_*` (see also
      [Combat and Movement § Damage calculation](../../../reference/02_combat/README.md#как-считается-урон)).

[^5]: `data/scripts/lib/miscext2.script:_misc_DoDamage`, branch
      `if (bCanHeadShot) and (random < 0.05) then ...`.
      `bCanHeadShot` is true for `arrow` or `bullet` against
      non-buildings.

[^6]: `data/scripts/lib/miscext2.script:_misc_DoDamage`, branch
      `if gbool_peacemode then ...`. Uses
      `_unit_IsOnEnemyTerritory(handle, pobj)` for the territory check.

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

[^12]: `data/scripts/lib/miscext2.script:589` — branch for
       fire arrows (`barrow`): `(listcount > 300) or (dist < r)`.

[^13]: `data/scripts/lib/miscext2.script:274` — `_misc_DoDamage`
       begins without checking the target's side, so friendly fire is
       possible.

[^14]: `data/scripts/lib/weapon.script:482-492` — comment
       `// prevent ships from friendly fire`.

[^15]: `data/scripts/lib/unit.script:7686-7714` —
       `_misc_IsBuildingInRay`.
