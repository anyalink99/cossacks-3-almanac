<a id="recon-башни"></a>
<a id="как-работают-башни"></a>
# How Towers Work

[← How the game works](../../README.md)

How a Tower chooses targets, what each shot costs, which upgrades affect
it, and when it can be captured or destroyed. Script references are
collected in [Sources](#sources).

> **Tower garrison is not implemented in Cossacks 3.** Mines and Transport
> Ships can accept infantry, but Towers, Town Halls, Houses, and Barracks
> cannot. The familiar “put Musketeers in the tower” mechanic from other
> strategy games does not exist here. Troops are carried by
> **Transport Ships** instead; see [How Naval Combat Works §4](naval_combat.md).
> The script-level evidence is collected under
> [Technical details](#technical-details).

<a id="коротко"></a>
## TL;DR

- A Tower has a built-in Cannonball weapon dealing 1,000 damage and a
  32-cell vision radius.
- Firing is automatic: the Tower searches for targets within 26.25 cells.
- Each European Tower shot costs **10 iron and 30 coal**; the Ottoman
  version costs more. Continuous upkeep is **0.8 gold per
  game second, or 48 gold per game minute**. When a required resource runs out, the
  Tower silently stops firing.
- Five European Tower upgrades raise the rate of fire by
  **2.14×** in total.
- **Capture is only possible while the Tower is under construction.** A
  completed Tower cannot change ownership and must be destroyed. Enemy
  infantry can capture an unfinished Tower from within four cells if no
  defenders are nearby [^2].
- **There is no garrison in the tower** (see quote block above).

---

<a id="1-что-делает-здание-башней"></a>
## 1. What Makes a Building a Tower

The Tower is defined by its weapon, range, and operating costs [^1]:

| Game property | Value |
|---|---|
| Weapon | Cannonball, 1,000 damage. |
| Shot cost | 10 iron and 30 coal. |
| Dispersion | 1.88 cells. |
| Automatic target-acquisition radius | 26.25 cells. |
| Gold upkeep | 0.8 gold per game second. |
| Vision | 32 cells in the fog of war. |
| Garrison | Not supported. |

Additional properties:
- health: 20,000;
- construction time: 3,937 frames × 10 / 32 =
  **1,230 game seconds**;
- each subsequent Tower costs 20% more.

Price: 0 food / 100 wood / 100 stone / 150 gold / 0 iron / 0 coal.

---

<a id="2-числовые-параметры-базовой-европейской-башни-eurtow"></a>
<a id="2-параметры-европейской-башни-eurtow"></a>
<a id="2-параметры-европейской-башни"></a>
## 2. European Tower parameters

| Parameter | Meaning | Note |
|---|---:|---|
| Hit points | 20,000 | Russian: 21,000; Ottoman: 22,500 |
| Vision | 32 cells | less than an average Hussar |
| Search radius | 1,400 px = **26.25 cells** | automatic target-acquisition radius |
| Damage | **1,000** | Cannonball damage is reduced by protection against cannonballs |
| Reload | 400 frames = **12.5 game seconds** | one shot every 12.5 game seconds |
| Shot range | 1500 px = **28.13 t** | tur 30 t |
| Scatter | 100 px = **1.88 t** | rus 125; a projectile may miss a single unit |
| Shot cost | **10 iron and 30 coal** | Ottoman: 15 iron and 40 coal |
| Upkeep | **0.8 gold per game second** (48 per game minute) | deducted at the same rate as food (see [Famine and Mercenary Rebellion §2.3](../economy/hunger_and_rebellion.md)) |
| Capture | only while under construction | a completed Tower cannot be captured |

<a id="21-вариации-по-нациям"></a>
### 2.1. Variations by nation

- **Russian Tower** (`rustow`) reloads faster: `pause = 300`
  frames = 9.4 game seconds (versus 12.5 for the European one), with 5% more hit points.
- **Ottoman Tower** (`turtow`) hits harder but less often: `damage = 1200`
  (+20%), `pause = 500` (−25% to the rate of fire), `range = 30 t`. And
  costs more: 40 coal + 15 iron versus 30/10.

---

<a id="3-целеуказание-башни"></a>
## 3. Tower targeting

The Tower uses the same general target search as armed units (see
[Target Selection and Attack-Move](target_selection.md)). Its important
differences are:

| Rule | Tower | Infantry |
|---|---|---|
| Choice among targets | no load balancing | load balancing applies to melee units |
| Search cone | 360° (unrestricted) | 360° while idle, 30° while attack-moving |
| Impact reaction | Shoots at the source if in radius | Same |

The Tower therefore fires at the **nearest** enemy in range, regardless
of how many other units are already targeting it.

<a id="31-дальность-и-обзор"></a>
### 3.1. Range and view

With a 32-cell vision radius, the Tower **sees farther**
than either its 26.25-cell search radius or its 28.13-cell firing range.
It can begin tracking an enemy in sight and fire as soon as the target
enters range.

<a id="32-тонкости-поведения"></a>
### 3.2. Subtleties of behavior

- **Each shot costs resources.** With no iron or coal, the Tower
  **does not fire**. During a rebellion (`gold = 0`) it stops consuming
  gold, but a shortage of iron or coal still disables its firepower. See
  [Animation system: timings, cycles, impact point §7](../../../../internals_en/engine/animation_system.md)
  how resources are deducted at the moment of an attack.
- The Tower can be **manually disabled** in
  the interface. A disabled Tower spends no iron, coal, or gold and does not fire.
  Used to save money in peacetime.
- The Tower searches within its radius and fires without an explicit order.

---

<a id="4-апгрейды-башни"></a>
<a id="4-улучшения-башни"></a>
## 4. Tower Upgrades

Five levels reduce reload time by
−20% / −20% / −10% / −10% / −10% (multipliers accumulate,
total ≈ 0.8 × 0.8 × 0.9³ ≈ 0.467 → **fire frequency × 2.14**). Full
list - in [upgrades](../../../reference/05_upgrades/README.md).

The cost of leveling up increases with level: level 1 - several hundred
resources; level 5 – several thousand. See numerical data there.

---

<a id="5-время-постройки-и-время-сноса"></a>
## 5. Construction time and demolition time

One Peasant needs 1,230 game seconds to build a Tower. With six builders (see
[builder limits](../../../reports/economy/builder_slots.md))
- about `1230 / 6 × 1.13 ≈ 232 game seconds`, or roughly four game minutes.

Demolition: `20 000 HP / 1800 dmg cannonball ≈ 11 hits` → about 2 minutes
shelling with one cannon in the absence of repairs.

---
<a id="6-захват--только-во-время-постройки"></a>
## 6. Capture - only during construction

From [How Buildings and Units Are Captured](../economy/capture_mechanics.md):

- Completed Towers **cannot be captured**. Capture checks still run for every
  unfinished building, so a Tower can change ownership only while it is
  under construction [^2].
- Towers in construction are captured according to the usual rules
  for buildings: infantry comes within four cells, no defenders are in
  range, and ownership changes immediately.

Therefore, attack an enemy Tower **while it is being built**: destroy or
capture it before completion. Once it is complete, heavy artillery is
the practical answer.

---

<a id="7-стратегические-выводы"></a>
## 7. Strategic conclusions

- **A Tower can pay off, but it is not free.** Upkeep is
  0.8 gold per game second × 10 Towers = **480 gold per
  game minute** only for the “tax”, plus 30 coal + 10 iron for
  each shot (once every 12.5 game seconds). In a long match, 10
  Towers place a noticeable burden on the economy.
- **Modest vision** means the Tower needs nearby scouts
  to cover its flanks.
- **Spread 1.88 t** - the tower **misses** single targets.
  It is effective against concentrations of infantry or cavalry, but
  less reliable against a single Hetman.
- **A completed Tower cannot be captured, only destroyed.** Building
  one on contested ground is risky because the unfinished structure can
  be seized.
- **An unfinished Tower is the better target:** while under construction
  only one third of its shield applies (see [How Damage Is Calculated §2](combat_damage_pipeline.md)),
  plus the ability to capture.

---

<a id="8-что-ещё-требует-проверки"></a>
<a id="технические-подробности"></a>
## Technical details

| Game concept | Internal representation |
|---|---|
| Tower type | branch `tow`, value `gc_obj_usage_tower` |
| European, Russian, and Ottoman Towers | `eurtow`, `rustow`, `turtow` |
| projectile and firing effect | `weapon[0].weaponsid = PPOINTTTOW`, `fxshot = shottower` |
| shot cost and dispersion | `weapon[0].cost[iron/coal]`, `weapon[0].dispertion` |
| target search, vision, and reload | `searchradius`, `vision`, `weapon_pause` |
| upkeep | `consume[gold] = 500`; formula `consume × 32 / 20000` |
| manual shutdown | `bturnoff = True` |
| construction state | `bbuilt` |
| capturability after completion | `bcapture = False` |
| capture check | `_misc_CheckCapture`, radius `captureradius = 4` |
| absence of garrison | `peasantabsorber` and `bgarrison` are unset; `inside[]` is used by transports |
| base properties | `SetObjBuildingProperties(20000, 3937, 120)` |

<a id="8-открытые-эмпирические-вопросы"></a>
<a id="что-ещё-требует-проверки"></a>
## 8. Questions Requiring Further Testing

1. **Exact formula for disp when firing.** `dispertion = 1.88 t` -
   This is a basic value, but does distance make a difference? It looks like
   `maxdisp = dist × disp × 0.0267` (as for regular ranged units; see
   [Target Selection and Attack-Move §9](target_selection.md)) - measurement needed.
2. **Garrison fire from forts.** Campaigns and Historical Battles contain
   forts that can accept infantry. These are **not** standard Towers
   (internal type `tow`) and require a separate examination of campaign scripts.

---

<a id="источники"></a>
## Sources

[^1]: `data/scripts/lib/unit.script` - branch `'tow'`. Basic
      parameters via `SetObjBuildingBaseSettings`,
      `SetObjBuildingProperties(20000, 3937, 120)`,
      `SetObjBaseWeapon(...damage=1000, pause=400, range=550-1500...)`.
      Price via `SetObjBasePrice(0, 100, 100, 150, 0, 0)`.

[^2]: See [How Buildings and Units Are Captured](../economy/capture_mechanics.md) -
      a Tower has `bcapture = False` from initialization, but the
      `not bbuilt` branch still calls `_misc_CheckCapture` for every
      unfinished building.
