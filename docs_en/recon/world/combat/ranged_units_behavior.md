<a id="recon-поведение-стрелковых-юнитов"></a>
<a id="как-ведут-себя-стрелковые-юниты"></a>
# Ranged-Unit Behavior

[← How the game works](../../README.md)

This article explains why two identical ranged units may behave differently:
one opens fire at long range, another waits until the enemy is close, a third
backs away, and a Cannon switches from round shot to grapeshot. It begins
with what the player sees; exact field and handler names are collected under
[Technical details](#technical-details) and [Sources](#sources).

> **Related documents:** [damage calculation](combat_damage_pipeline.md) —
> damage formula; [target selection](target_selection.md) —
> target selection algorithm; [Unit Orders](unit_commands.md) —
> order queue; [How Artillery Works](artillery_specifics.md)
> — artillery mechanics.

<a id="кратко"></a>
## TL;DR

- **Hold position** gives a ranged unit its full detection radius, usually
  28–45 cells. In normal mode it may not react until the enemy is almost in
  melee range.
- **Artillery fire at a point** disables Hold Position and enables active
  target search around the selected location.
- **Retreat from the dead zone** makes a ranged unit step back 3.5 cells when
  an enemy comes too close. It does not happen while holding position.
- **Immediately after moving**, a ranged unit loses up to 3 cells of
  effective range; artillery loses up to 1.5 cells.
- **A stationary unit** gains about 0.6 cells of range.
- Units with multiple weapons switch by distance: the Cannon uses
  cannonballs at range and grapeshot nearby; the Musketeer,
  18th century uses a musket at range and a bayonet up close.
- **High ground** increases the detection radius by twice the position's
  height.

---

<a id="1-standground-vs-обычный-режим"></a>
<a id="1-удержание-позиции-standground-и-обычный-режим"></a>
<a id="1-удержание-позиции-и-обычный-режим"></a>
## 1. Hold Position versus normal mode

The central difference is the radius in which the unit begins reacting to an
enemy [^1].

While **holding position**, a unit reacts throughout its full weapon range,
usually about 28–45 cells.

In **normal mode** and while moving, the reaction radius falls almost to the
minimum firing distance. The unit may therefore notice an enemy only after
it has come very close. The exact formula is given under
[Technical details](#technical-details).

<a id="11-что-это-значит-на-практике"></a>
### 1.1. What does this mean in practice?

| Mode | Behavior |
|---|---|
| Hold position | The Musketeer on the hill fires 5–10 shots before close combat. |
| Normal behavior | The same Musketeer fires only 1–2 shots before the enemy closes. |
| Movement order | Temporarily removes the benefit of hold position. |

**Use hold position when defending.** Without it, ranged units may
appear unresponsive and wait until enemies are only 1–2 cells away.

<a id="2-bartprepare--режим-артиллерии"></a>
<a id="2-допуск-артиллерии-к-стрельбе-по-точке-bartprepare"></a>
<a id="2-стрельба-артиллерии-по-точке"></a>
## 2. Firing artillery at a point

The Cannon, Howitzer, and Frame gun can bombard a location even when no unit
is selected there. The game forcibly changes their behavior for this order
[^2].

| Behavior | Change |
|---|---|
| Hold position | disabled |
| Independent enemy search | enabled |
| Current order | bombard the selected location after the normal delay |

Artillery ordered to fire at a point therefore searches around the selected
point and fires at enemies found there.

For units without this mode, such as the Multi-barrelled Cannon or a
Musketeer, the same command becomes an ordinary movement order.

See also [How Artillery Works](artillery_specifics.md) §3
about firing at a point and preparing the shot.

<a id="3-runaway--отход-стрелка-из-мёртвой-зоны"></a>
<a id="3-отход-стрелка-из-мёртвой-зоны-runaway"></a>
<a id="3-отход-стрелка-из-мёртвой-зоны"></a>
## 3. Retreating from the dead zone

If an enemy enters a ranged unit's **dead zone**—closer than its minimum
firing distance—the unit retreats by **3.5 cells** unless it is holding
position [^3].

<a id="31-условия-запуска"></a>
### 3.1. Conditions

All three must be true:

1. The unit is **not** holding position.
2. The enemy is closer than the minimum firing distance.
3. Starting condition (one of):
   - the unit has just approached or completed a shot;
   - the unit has stood still for more than **1.3 game seconds**;
   - a human player on Easy or Normal difficulty, which skips
     this timing check.

<a id="32-сложность-и-поведение"></a>
### 3.2. Difficulty and behavior

| Controller | Difficulty | When the unit retreats |
|---|---|---|
| Human | Easy / Normal | At every update while the enemy remains in the dead zone. |
| Human | Hard / Very Hard / Impossible | Immediately after approaching or firing, or after 1.3 seconds at rest; in between, the unit gets time to fire. |
| AI | Any | Same timing as Hard and above for a human. |

<a id="33-стратегические-выводы"></a>
### 3.3. Strategic implications

- **Holding a hill** requires hold position, or ranged units will
  scatter when enemies close in.
- For **fighting retreats**, disable hold position: the unit retreats
  3.5 cells, turns, fires, and retreats again.
- **Light cavalry** can catch retreating ranged units because fast cavalry
  moves about three times as quickly as an ordinary unit.

<a id="4-штраф-к-дальности-при-движении-standtime"></a>
<a id="4-почему-движение-сокращает-дальность"></a>
## 4. Why movement reduces range

The game tracks how long the unit has remained still. Movement resets the
counter; after the unit stops, it begins to increase.

For the first **0.25 game second** after stopping, the unit loses part of
its effective maximum range [^4]. The penalty is specific to the unit:
between 0 and 3 cells for infantry, or between 0 and 1.5 cells for
artillery. Its chosen value remains constant.

<a id="41-эффект"></a>
### 4.1. Effect

- **A moving unit cannot immediately fire at full range**; it must
  stand for about 0.25 game second.
- **Grapeshot is exempt.**
- **Artillery receives half the penalty**: a Bombard or Cannon can
  fire near full range shortly after moving.
- Together with the retreat mechanic, this produces the sequence **retreat →
  pause 0.25 → fire → retreat**.

<a id="5-бонус-к-дальности-в-покое-addradius"></a>
<a id="5-бонус-к-дальности-бездействующего-юнита-addradius"></a>
<a id="5-почему-неподвижный-юнит-стреляет-дальше"></a>
## 5. Why a stationary unit fires farther

An idle unit receives the range bonus assigned to its weapon [^5].
Musketeers, Archers, and Cannons normally gain 32 pixels, or about
**0.6 cells**. When firing at a Palisade, another **0.36 cells** is added.

<a id="51-эффект"></a>
### 5.1. Effect

A stationary defense, such as a group holding position on a hill,
fires about **0.6 cells farther** than the same units while moving.
Combined with high ground and removal of the post-movement penalty,
this noticeably increases the defensive range.

<a id="6-переключение-оружия-по-дистанции-multi-weapon"></a>
<a id="6-переключение-нескольких-видов-оружия-по-дистанции"></a>
## 6. Switching between multiple weapons by distance

Many units have **multiple weapons**. The game automatically selects one
that suits the target's distance and type [^6]: a melee weapon nearby and
a ranged weapon farther away. Fire arrows receive priority against
buildings, wooden objects, and Palisades.

<a id="61-пары-multi-weapon-юнитов"></a>
<a id="61-пары-оружия"></a>
### 6.1. Weapon pairs

<a id="пушка--ядро-против-картечи"></a>
#### Cannon — cannonball versus grapeshot

| Weapon | Damage | Pause | Range (pixels) | When |
|---|---:|---:|---|---|
| Cannonball | 1,800 | 350 | 550–2,160 | distance is at least 550 pixels (~10.3 cells) |
| Grapeshot | area damage | 350 | 0–450 | enemy is within 450 pixels (~8.4 cells) |

Infantry that comes within about eight cells of a Cannon is automatically
engaged with **grapeshot**, which deals heavy area damage. An extended line
helps keep each explosion from hitting more than nine targets; see
[How Damage Is Calculated §5](combat_damage_pipeline.md) for the
area-damage limit.

<a id="мушкетёр-18-в--пуля-против-штыка"></a>
<a id="мушкетер-18в--пуля-против-штыка"></a>
#### Musketeer, 18th century — musket shot versus bayonet

| Weapon | Damage | Pause | Range (pixels) | When |
|---|---:|---:|---|---|
| Bayonet | 5–10 (by nation) | **0** (no pause between hits) | 35–65 (~0.66–1.22 cells) | point blank |
| Musket | 16–29 (by nation) | 140–190 | 400–900 (~7.5–16.9 cells) | beyond 7.5 cells |

A Musketeer is **not helpless** in close combat: the bayonet has no pause
and attacks on every animation cycle. Cavalry charging
reloading Musketeers will still face their bayonets.

Fire Power upgrades increase musket damage but leave the bayonet at its
base value.

<a id="лучник--обычная-стрела-против-огненной"></a>
#### Archer — regular arrow versus fire arrow

| Weapon | Damage | Pause | Range (pixels) | Dispersion | Features |
|---|---:|---:|---|---:|---|
| Regular arrow | 15 | 75 | 400–800 | 175 pixels | main attack |
| Fire arrow | **150** | 125 | 400–600 | 200 pixels | used against buildings, wooden objects, and Palisades |

The Fire Arrow is the **Archer's weapon against buildings**. It deals 150
damage—ten times the normal arrow's value—but fires 40% more slowly, and
its dispersion value is 14.3% larger. That does not directly mean 14.3%
lower accuracy. It receives **no formation damage bonus**. The game
automatically switches the Archer to fire arrows when the target is a
building, wooden object, or Palisade.

<a id="прочие"></a>
#### Other

- **Janissary** — bullet and sabre.
- **Strelets** — arquebus and berdiche.
- **Chasseur and Dragoon** — bullet and sabre.
- **Mounted ranged units**, such as the Drabant and Mounted Archer — ranged
  weapon and sabre.

The rule is the same throughout: use the melee weapon up close and the
ranged weapon at a distance.

<a id="7-high-ground--бонус-с-возвышенности"></a>
<a id="7-бонус-с-возвышенности"></a>
## 7. High-ground bonus

If a ranged unit stands on high ground, its **search distance** increases
by two cells for every cell of height [^7]. The bonus applies **only to
detection**, not to the weapon's true firing range. If the enemy is detected
before entering range, the unit begins acting and fires as soon as the target
enters weapon range. In practice, Musketeers on a hill begin responding
earlier and gain more shots before melee begins.

Hills are controlled by the map's relief setting; Highlands gives the
strongest opportunities to use this bonus.

<a id="71-не-работает-на"></a>
### 7.1. Units that do not benefit

- Melee units: a Pikeman still has to close to melee range.
- Units with no independent target-search radius, such as the Bombard and
  Drummer.

<a id="технические-подробности"></a>
## Technical details

These internal names are useful when checking the scripts, but they are not
separate commands shown in the interface.

| Game concept | Internal name |
|---|---|
| hold position | `standground`, field `bstandground` |
| fire at a point | order `attackpoint`, permission `bartprepare` |
| retreat from the dead zone | handler `RunAway` |
| time since stopping | `standtime` |
| stationary range bonus | `addradius` |
| per-unit fixed random value | `uniqrnd` |
| minimum and maximum weapon range | `radiusmin`, `radiusmax` |
| target types accepted by a weapon | `attmask` |

<a id="формулы-дальности-и-отхода"></a>
### Range and retreat formulas

- Hold Position:
  `maxsearchdist = MIN(searchradius, GetMaxAttackRadius)`.
- Normal mode or movement:
  `maxsearchdist = minsearchdist + 0.375`.
- Retreat is available to a ranged unit with `minsearchdist > 0` when the
  target lies in `[0, minsearchdist]`. Its distance is
  `gc_unit_runawaydist = 3.5`, and its repeated-trigger delay is
  `gc_unit_runawaydelay = 1.3`.
- Fast cavalry uses `fasthorse = 96`, compared with the ordinary
  `default = 32`.

The post-movement penalty is calculated as follows:

```
if (standtime < 0.25) AND (weapon.kind ≠ cannister):
    if (NOT bArtillery):
        radiusmax −= 3 × uniqrnd
    else:
        radiusmax −= 3 × uniqrnd × 0.5
```

The `gc_obj_maxattackradiusdisp` constant is 3. The `uniqrnd` value lies in
`[0, 1)` and is fixed when the unit is created.

While idle, the game adds `weapon[i].addradius`, usually 32 pixels.
Idle state is identified through `statestag` and
`gc_statetag_move_idle`; `gc_obj_usage_weakwall` receives another
0.36 cells.

<a id="внутренние-параметры-нескольких-видов-оружия"></a>
### Internal parameters for multiple weapons

| Unit and weapon | Slot and internal type | Damage | Pause | Range |
|---|---|---:|---:|---|
| Cannon, cannonball | `weapon[0]`, `PPOINTT`, `cannonball` | 1,800 | 350 | 550–2,160 |
| Cannon, grapeshot | `weapon[1]`, `PSMPOINTTPUS`, `cannister` | area damage | 350 | 0–450 |
| Musketeer, 18th century, bayonet | `weapon[0]`, `pike` | 5–10 | 0 | 35–65 |
| Musketeer, 18th century, musket | `weapon[1]`, `SHOTMUSKET`, `bullet` | 16–29 | 140–190 | 400–900 |
| Archer, regular arrow | `weapon[0]`, `STRELA`, `arrow` | 15 | 75 | 400–800 |
| Archer, fire arrow | `weapon[1]`, `OSTRELA`, `firearrow` | 150 | 125 | 400–600 |

Selection considers the `radiusmin..radiusmax` interval and the match
between `weapon[i].attmask` and the target's `mmask`. The fire arrow uses
`building + wood + woodwall`. The `bla.musketeer18.1.X` upgrade series
raises `bullet` damage but not bayonet damage.

The high-ground bonus is
`searchdist += goHeight × 2`. It applies to ranged units whose
`minsearchdist > melee_radius`. Units with `searchradius = 0`, including
the Bombard and Drummer, do not benefit. The map's relief setting is stored
as `relief`.

<a id="источники"></a>
## Sources

[^1]: `data/scripts/lib/unit.script:7259-7286` —
      `_unit_SearchTarget`, calculation `maxsearchdist`. Condition:
      `if (bstandground AND order ≠ move) then maxsearchdist :=
      MIN(searchradius, GetMaxAttackRadius) else maxsearchdist :=
      minsearchdist + 0.375;`.

[^2]: `data/scripts/lib/player.script:2456-2463` — handler for
      `bartprepare` with `attackpoint` order:
      forced reset `bstandground := False`,
      `bsearchenemy := True`, issuing the order `attackpoint(trgx,
      trgz)` with a preparation delay.

[^3]: `data/scripts/lib/unit.script:7363-7369` — `RunAway` mechanics.
      Parameters: `gc_unit_runawaydelay = 1.3` game seconds,
      `gc_unit_runawaydist = 3.5` cells. The condition uses
      `bstandground`, `standtime`, and `bai`; Easy and Normal human players
      receive the more forgiving branch.

[^4]: `data/scripts/lib/unit.script:8011-8023` — reduces `radiusmax`
      while `standtime < 0.25` game second. Constant
      `gc_obj_maxattackradiusdisp = 3` (`dmscript.global:116`).

[^5]: `data/scripts/lib/unit.script:8026-8028` — applies
      `weapon.addradius` to an idle unit, usually 32 px or 0.6 cells.
      `gc_obj_usage_weakwall` receives another 0.36 cells.

[^6]: `data/scripts/lib/unit.script:6376-6451` —
      `_unit_GetWeaponToAttackIndex`, which selects a weapon slot by
      distance and target `attmask`.

[^7]: `data/scripts/lib/unit.script:5469, 7272` — high-ground search-distance
      bonus. It applies only to ranged units, where
      `minsearchdist > melee_radius`.
