<a id="recon-поведение-стрелковых-юнитов"></a>
<a id="как-ведут-себя-стрелковые-юниты"></a>
# Ranged-Unit Behavior

[← How the game works](../../README.md)

An in-depth look at hold-position behaviour, artillery fire-at-point
orders, retreating from a dead zone, movement penalties, idle range
bonuses, weapon switching, and the high-ground bonus. Code references
are collected under [Sources](#sources).

> **Related documents:** [damage calculation](combat_damage_pipeline.md) -
> damage formula; [target selection](target_selection.md) —
> target selection algorithm; [`unit_commands.md`](unit_commands.md) —
> order queue; [`artillery_specifics.md`](artillery_specifics.md)
> — artillery mechanics.

<a id="кратко"></a>
## TL;DR

- **Hold position** (`standground`) lets a ranged unit search to its
  full `searchradius` of roughly 28–45 tiles. Without it, the search
  distance is only about `minsearchdist + 0.375`.
- **Fire-at-point permission** (`bartprepare`) lets artillery, Towers,
  and Shipyards accept `attackpoint`; the order disables hold position
  and starts searching around the selected point.
- **Dead-zone retreat** (`RunAway`) moves a ranged unit 3.5 tiles
  away when an enemy comes inside `minsearchdist`. It is disabled
  while holding position.
- A unit that moved within the last 0.25 game second loses up to
  3 tiles of effective maximum range; artillery loses up to 1.5.
- An **idle unit** gains about 0.6 tile from `addradius`.
- Units with multiple weapons switch by distance: the Cannon uses
  cannonballs at range and grapeshot nearby; the Musketeer,
  18th century uses a musket at range and a bayonet up close.
- **High ground** increases the search distance:
  `searchdist += goHeight × 2`.

---

<a id="1-standground-vs-обычный-режим"></a>
<a id="1-удержание-позиции-standground-и-обычный-режим"></a>
## 1. Hold position (`standground`) versus normal mode

The target-search distance, `maxsearchdist`, is calculated differently
for hold position and normal movement [^1].

While **holding position** (`bstandground = True` and the order is not
`move`):
```
maxsearchdist = MIN(searchradius, GetMaxAttackRadius)
```
That is, the full range of the weapon (~28-45 tiles).

In **normal** mode (without hold position, or with `move`):
```
maxsearchdist = minsearchdist + 0.375
```
This is almost melee distance: the unit detects the enemy only after
it comes very close.

<a id="11-что-это-значит-на-практике"></a>
### 1.1. What does this mean in practice?

| Mode | Behaviour |
|---|---|
| Hold position (`standground`) | The Musketeer on the hill fires 5–10 shots before close combat. |
| Regular (`move`/`attack`) | The same Musketeer fires only 1–2 shots before the enemy closes. |
| Movement order | Disables hold position: `if (order = move)` blocks the branch. |

**Use hold position when defending.** Without it, ranged units may
appear unresponsive and wait until enemies are only 1–2 tiles away.

<a id="2-bartprepare--режим-артиллерии"></a>
<a id="2-допуск-артиллерии-к-стрельбе-по-точке-bartprepare"></a>
## 2. Permission for artillery to fire at a point (`bartprepare`)

`bartprepare = True` is set for artillery, Towers (`tow`), and
Shipyards (`port`). When one receives `attackpoint(trgx, trgz)`,
the script switches its modes [^2]:

| Field | Change |
|---|---|
| `bstandground` | forced to False |
| `bsearchenemy` | forced to True (active search) |
| Receives an order | `attackpoint` with delay `attackdelay`/`attackmaxdelay` |

Artillery with `attackpoint` therefore searches around the selected
point and fires at enemies found there.

Without `bartprepare` (for example, a mobile grapeshot unit or
Musketeer), the order
`attackpoint` behaves like `move(x, z)` without active search.

See also [`artillery_specifics.md`](artillery_specifics.md) §3
about the order `attackpoint` and the preparation of the shot.

<a id="3-runaway--отход-стрелка-из-мёртвой-зоны"></a>
<a id="3-отход-стрелка-из-мёртвой-зоны-runaway"></a>
## 3. Retreating from the dead zone (`RunAway`)

If an enemy enters a ranged unit's **dead zone**, between `0` and
`minsearchdist`, and the unit is not holding position, it retreats
by `gc_unit_runawaydist = 3.5` tiles [^3].

<a id="31-условия-запуска"></a>
### 3.1. Conditions

All three must be true:

1. The unit is **not** in standground.
2. The enemy is in the zone `[0, minsearchdist]`.
3. Starting condition (one of):
   - `standtime = 0` (just approached / completed the shot);
   - `standtime > gc_unit_runawaydelay = 1.3` g-sec (stood
     long enough);
   - or a human player on Easy or Normal difficulty, which skips
     this timing check.

<a id="32-сложность-и-поведение"></a>
### 3.2. Difficulty and behaviour

| Controller | Difficulty | When the unit retreats |
|---|---|---|
| Human | Easy / Normal | At every update while the enemy is inside `minsearchdist`. |
| Human | Hard / Very Hard / Impossible | Only when `standtime = 0` or `> 1.3`; in between, the unit gets time to fire. |
| AI | Any | Same timing as Hard and above for a human. |

<a id="33-стратегические-выводы"></a>
### 3.3. Strategic implications

- **Holding a hill** requires hold position, or ranged units will
  scatter when enemies close in.
- For **fighting retreats**, disable hold position: the unit retreats
  3.5 tiles, turns, fires, and retreats again.
- **Light cavalry** can catch retreating ranged units:
  `fasthorse = 96` versus the usual `default = 32`.

<a id="4-штраф-к-дальности-при-движении-standtime"></a>
## 4. Range penalty when moving (`standtime`)

`standtime` records how long the unit has remained still. Movement
resets it to 0; after stopping, it begins to increase.

If `standtime < 0.25` game second, the unit loses effective maximum
range [^4]:
```
if (standtime < 0.25) AND (weapon.kind ≠ cannister):
    if (NOT bArtillery):
        radiusmax −= 3 × uniqrnd            # infantry: up to −3 tiles
    else:
        radiusmax −= 3 × uniqrnd × 0.5      # artillery: up to −1.5 tiles
```
Here `gc_obj_maxattackradiusdisp = 3` comes from `dmscript.global`,
and `uniqrnd` ∈ `[0, 1)` is fixed when the unit is created.

<a id="41-эффект"></a>
### 4.1. Effect

- **A moving unit cannot immediately fire at full range**; it must
  stand for about 0.25 game second.
- **Grapeshot is exempt** (`kind = cannister`).
- **Artillery receives half the penalty**: a Bombard or Cannon can
  fire near full range shortly after moving.
- Together with `RunAway`, this produces the sequence **retreat →
  pause 0.25 → fire → retreat**.

<a id="5-бонус-к-дальности-в-покое-addradius"></a>
<a id="5-бонус-к-дальности-бездействующего-юнита-addradius"></a>
## 5. Range bonus while idle (`addradius`)

If the unit is idle (`statestag` contains
`gc_statetag_move_idle`), it receives a bonus to
`weapon.radiusmax` [^5]:
```
rbonus += weapon[i].addradius     # normally 32 px = ~0.6 tiles
```
Musketeers, Archers, and Cannons normally have
`addradius = 32 px = 0.6 tile`. Weak walls
(`gc_obj_usage_weakwall`) gain an additional **+0.36 tile**.

<a id="51-эффект"></a>
### 5.1. Effect

A stationary defence, such as a group holding position on a hill,
fires about **0.6 tile farther** than the same units while moving.
Combined with high ground and removal of the `standtime` penalty,
this noticeably increases the defensive range.

<a id="6-переключение-оружия-по-дистанции-multi-weapon"></a>
<a id="6-переключение-нескольких-видов-оружия-по-дистанции"></a>
## 6. Switching between multiple weapons by distance

Many units have **multiple weapon slots** (`weapon[0]`,
`weapon[1]`, ...). The game automatically selects the desired one
distance to the target - each weapon has
`radiusmin..radiusmax` [^6]. If the enemy is in close range -
a weapon with a small `radiusmin` is selected; otherwise - distant.

Additionally, `attmask` is taken into account: if the target has `mmask`
matches `weapon[i].attmask` (armor material), this is a weapon
priority. Therefore, **fire arrows** are chosen for
buildings (their `attmask` contains `gc_obj_material_building`).

<a id="61-пары-multi-weapon-юнитов"></a>
<a id="61-пары-оружия"></a>
### 6.1. Weapon pairs

<a id="пушка--ядро-против-картечи"></a>
#### Cannon — cannonball versus grapeshot

| Slot | Type | Damage | Pause | Range (pixels) | When |
|---|---|---:|---:|---|---|
| `weapon[0]`, `PPOINTT` | Cannonball Damage (`cannonball`) | 1800 | 350 | 550–2160 | distance ≥ 550 pixels (~10.3 tiles) |
| `weapon[1]`, `PSMPOINTTPUS` | Grapeshot Damage (`cannister`) | area damage | 350 | 0–450 | enemy is within 450 pixels (~8.4 tiles) |

Infantry that comes within ~8 tiles of a cannon is automatically hit
under **grapeshot**—heavy area damage. Therefore, rushing infantry into a
Cannon means taking grapeshot at point-blank range. **It is better to attack a Cannon in an extended
line** so that there are no more than 9 units under the explosion (see.
[`combat_damage_pipeline.md` §5](combat_damage_pipeline.md) about AoE
damage limit).

<a id="мушкетёр-18-в--пуля-против-штыка"></a>
<a id="мушкетер-18в--пуля-против-штыка"></a>
#### Musketeer, 18th century — musket shot versus bayonet

| Slot | Type | Damage | Pause | Range (pixels) | When |
|---|---|---:|---:|---|---|
| `weapon[0]` (bayonet) | Pike Attack (`pike`) | 5–10 (by nation) | **0** (no pause between hits) | 35–65 (~0.66–1.22 tiles) | point blank |
| `weapon[1]`, `SHOTMUSKET` | Fire Power (`bullet`) | 16–29 (by nation) | 140–190 | 400–900 (~7.5–16.9 tiles) | beyond 7.5 tiles |

A Musketeer is **not helpless** in close combat: his bayonet has
`pause = 0` and attacks on every animation cycle. Cavalry charging
reloading Musketeers will still face their bayonets.

Bayonet upgrades are separate from bullet upgrades
(`bla.musketeer18.1.X` increases bullet damage, bayonet remains
basic).

<a id="лучник--обычная-стрела-против-огненной"></a>
#### Archer — regular arrow versus fire arrow

| Slot | Type | Damage | Pause | Range (pixels) | Dispersion | Features |
|---|---|---:|---:|---|---:|---|
| `weapon[0]`, `STRELA` | Arrow Attack (`arrow`) | 15 | 75 | 400–800 | 175 pixels | main attack |
| `weapon[1]`, `OSTRELA` | Fire Arrow Attack (`firearrow`) | **150** | 125 | 400–600 | 200 pixels | `attmask = building + wood + woodwall` |

Fire Arrow Attack is the **Archer's weapon against buildings**: damage 150
(10 times more than usual), but the rate of fire is 40% worse,
accuracy is 14% worse, and the **formation damage bonus does not
apply**. The game automatically switches the Archer to `OSTRELA`
when the target is a building, wooden object, or palisade.

<a id="прочие"></a>
#### Other

- **Janissary** - bullet + saber.
- **Strelets** - arquebus + reed.
- **Chasseur / dragoon** - bullet + saber.
- **Mounted archers** (drabant, mounted archer) - bullet + saber
  on horseback.

Everywhere the logic is the same: close - a melee weapon, far -
small arms

<a id="7-high-ground--бонус-с-возвышенности"></a>
<a id="7-бонус-с-возвышенности"></a>
## 7. High-ground bonus

If a shooting unit is on high ground (`Y > 0`), it
**search distance** increases in proportion to the height of [^7]:
```
searchdist += goHeight × 2     # ranged units only: minsearchdist > melee_radius
```
`goHeight` — Y-coordinate of the unit in tiles. Bonus **only to radius
detection**, not to the shot itself. But if the enemy is not yet in the zone
attacks, the unit starts moving and will fire as soon as the target
will go into `radiusmax`. In practice, musketeers shoot from a hill at
advancing **earlier** = more shots before close combat.

Low Mountains are created by the `relief` parameter when generating a map
(Highlands gives the maximum).

<a id="71-не-работает-на"></a>
### 7.1. Units that do not benefit

- Melee units (a pikeman on a hill has no advantages
  receives - he is in close combat).
- Units with `searchradius = 0` (mortar, drummer, etc.).

<a id="8-открытые-эмпирические-вопросы"></a>
## 8. Open empirical questions

1. **Exact formula for RunAway direction.** In which direction
   shooter retreating? “From the enemy in a straight line” or something more
   smart pathfinding selection. Measure through screenshots.
2. **Penalty to range when `cannister`.** The entry says “not
   fined", but `radiusmin` for cannister is usually zero -
   you need to check that `radiusmax` really does not tremble.
3. **High ground for archers against AoE.** If the archer is standing
   on the hill and shoots a fire arrow at the building - taken into account
   whether the amendment `goHeight × 2` is in the detection of the building, or only
   when searching for units?

<a id="источники"></a>
## Sources

[^1]: `data/scripts/lib/unit.script:7259-7286` —
      `_unit_SearchTarget`, calculation `maxsearchdist`. Condition:
      `if (bstandground AND order ≠ move) then maxsearchdist :=
      MIN(searchradius, GetMaxAttackRadius) else maxsearchdist :=
      minsearchdist + 0.375;`.

[^2]: `data/scripts/lib/player.script:2456-2463` - handler
      `bartprepare` with `attackpoint` order:
      forced reset `bstandground := False`,
      `bsearchenemy := True`, issuing the order `attackpoint(trgx,
      trgz)` with a preparation delay.

[^3]: `data/scripts/lib/unit.script:7363-7369` - RunAway mechanics.
      Parameters: `gc_unit_runawaydelay = 1.3` g-sec,
      `gc_unit_runawaydist = 3.5` tile. The inclusion condition takes into account
      `bstandground`, `standtime`, flag `bai` (for
      normal human indulgence).

[^4]: `data/scripts/lib/unit.script:8011-8023` - fine `radiusmax`
      at `standtime < 0.25` g-sec. Constant
      `gc_obj_maxattackradiusdisp = 3` (`dmscript.global:116`).

[^5]: `data/scripts/lib/unit.script:8026-8028` - bonus
      `addradius` for idle unit. Field `weapon.addradius`,
      usually 32 px = 0.6 t. For `gc_obj_usage_weakwall` -
      additional +0.36 tiles.

[^6]: `data/scripts/lib/unit.script:6376-6451` —
      `_unit_GetWeaponToAttackIndex`. Selecting a weapon slot by
      distances and `attmask` targets.

[^7]: `data/scripts/lib/unit.script:5469, 7272` – search bonus
      distance from a hill. Applies only to ranged
      units (where `minsearchdist > melee_radius`).
