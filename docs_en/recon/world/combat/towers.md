<a id="recon-башни"></a>
<a id="как-работают-башни"></a>
# How Towers Work

[← How the game works](../../README.md)

How a Tower chooses targets, what each shot costs, which upgrades affect
it, and when it can be captured or destroyed. Script references are
collected in [Sources](#sources).

> **Tower garrison is not implemented in Cossacks 3.** In scripts
> `peasantabsorber` is assigned **only** to Coal, Gold, and Iron Mines
> (internal branches `coa`, `gol`, and `iro` in `unit.script`). Towers
> (internal type `tow`), Town Halls, Houses, and Barracks cannot accept
> infantry; the familiar “put Musketeers in the tower” mechanic from
> other strategy games does not exist here.
> Garrison via `inside[]` exists, but is only used for
> **transport ships** (`btransport = True`); see
> [`naval_combat.md` §4](naval_combat.md).

<a id="коротко"></a>
## TL;DR

- A Tower has a built-in Cannonball weapon (`cannonball`) dealing 1,000
  damage and a 32-tile vision radius (`vision = 3`).
- Firing is automatic (`bartprepare = True`): the Tower searches for
  targets within 26.25 tiles (`searchradius`) and fires.
- Each European Tower shot costs **10 iron and 30 coal**; the Ottoman
  version costs more. Continuous upkeep is `consume[gold] = 500`,
  which according to the formula `× 32 / 20000` gives **0.8 gold per
  game second, or 48 gold per game minute**. When a required resource runs out, the
  Tower silently stops firing.
- Five European Tower upgrades (`eurtow.1..5`) raise the rate of fire by
  **2.14×** in total.
- **Capture is only possible while the tower is under construction.** In `unit.script`
  for `<prefix>tow`, `bcapture = False` is explicitly set (via
  `SetObjBuildingBaseSettings(objprop, False, ...)`), the flag is not
  change with `bbuilt`. A completed Tower never reaches
  `_misc_CheckCapture`: the `nothing` state handler calls `CheckCapture`
  only with `bbuilt=False` (any building under construction) or with
  `bcapture=True` (completed building). Therefore a completed Tower
  cannot be captured and must be destroyed. A Tower under construction
  can be captured because the `not bbuilt` branch calls
  `_misc_CheckCapture` regardless of `bcapture`, and infantry
  changes ownership through `_misc_ChangePlayer` when enemy infantry are
  within four tiles and no defenders are present.
- **There is no garrison in the tower** (see quote block above).

---

<a id="1-что-делает-здание-башней"></a>
## 1. What Makes a Building a Tower

The `'tow'` branch in `unit.script` assigns the key fields [^1]:

| Game property | Internal value | Meaning |
|---|---|---|
| `usage` | `gc_obj_usage_tower` | Tower type. |
| Weapon (`weapon[0]`) | `cannonball`, `damage = 1000` | Built-in Cannonball dealing 1,000 damage. |
| `weapon[0].weaponsid` | `'PPOINTTTOW'` | Specific projectile (see `weapon.script`). |
| `weapon[0].cost[iron]` | 10 | For the shot. |
| `weapon[0].cost[coal]` | 30 | For the shot. |
| `weapon[0].fxshot` | `'shottower'` | Flash effect. |
| `weapon[0].dispertion` | `_misc_PixelsToTiles(100) = 1.88 t` | Scatter. |
| Search radius (`searchradius`) | `_misc_PixelsToTiles(1400) = 26.25 t` | Automatic target-acquisition radius. |
| Gold upkeep (`consume[gold]`) | 500 | Continuous upkeep: **0.8 gold per game second**. |
| Vision (`vision`) | 3 | 32 tiles in the fog of war. |
| `peasantabsorber` | (not specified) | **Garrison not supported.** |
| `bgarrison` | (not specified) | Same. |

Parameters `SetObjBuildingProperties(20000, 3937, 120)`:
- HP = 20,000.
- `buildtime` = 3937 frames × 10 / 32 = **1,230 game seconds**.
- 120 — `costpercent` (each next tower is 20% more expensive).

Price: 0 food / 100 wood / 100 stone / 150 gold / 0 iron / 0 coal.

---

<a id="2-числовые-параметры-базовой-европейской-башни-eurtow"></a>
<a id="2-параметры-европейской-башни-eurtow"></a>
## 2. European Tower Parameters (`eurtow`)

| Parameter | Meaning | Note |
|---|---:|---|
| Hit points | 20,000 | Russian: 21,000; Ottoman: 22,500 |
| Vision (`vision`) | 3 → 32 tiles | less than an average Hussar |
| Search radius (`searchradius`) | 1,400 px = **26.25 tiles** | automatic target-acquisition radius |
| Damage | **1,000** | Cannonball (`cannonball`) uses `prot_cannonball` protection |
| Reload (`weapon_pause`) | 400 frames = **12.5 game seconds** | one shot every 12.5 game seconds |
| Shot range | 1500 px = **28.13 t** | tur 30 t |
| Scatter | 100 px = **1.88 t** | rus 125; a projectile may miss a single unit |
| Shot cost | **10 iron and 30 coal** | Ottoman: 15 iron and 40 coal |
| Upkeep | `consume[gold] = 500` → **0.8 gold per game second** (48 per game minute) | formula `consume × 32 / 20000`, the same as for food (see [`../economy/hunger_and_rebellion.md` §2.3](../economy/hunger_and_rebellion.md)) |
| Capture | `bcapture = False` (after construction) | the tower is **never** captured when completed |

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

The Tower is a regular armed building and therefore uses the common
`_unit_SearchEnemyScanCells` algorithm (see
[`target_selection.md` §3](target_selection.md)). Features:

| Parameter | Tower | Infantry |
|---|---|---|
| `scanmode` | `priest_or_tower` (no load balancing) | `default` for melee, `default` for marksman |
| Search cone | 360° (unrestricted) | 360° while idle, 30° while attack-moving |
| Accounting `STO_count` | No | Yes for melee |
| Impact reaction | Shoots at the source if in radius | Same |

The Tower therefore fires at the **nearest** enemy in range, regardless
of how many other units are already targeting it.

<a id="31-дальность-и-обзор"></a>
### 3.1. Range and view

With a 32-tile vision radius (`vision = 3`), the Tower **sees farther**
than either its 26.25-tile search radius or its 28.13-tile firing range.
It can begin tracking an enemy in sight and fire as soon as the target
enters range.

<a id="32-тонкости-поведения"></a>
### 3.2. Subtleties of behavior

- **Each shot costs resources.** With no iron or coal, the Tower
  **does not fire**. During a rebellion (`gold = 0`) it stops consuming
  gold, but a shortage of iron or coal still disables its firepower. See
  [`../../../internals/engine/animation_system.md` §7](../../../../internals_en/engine/animation_system.md)
  how resources are deducted at the moment of an attack.
- **`bturnoff = True`** means the Tower can be **manually disabled** in
  the interface. A disabled Tower spends no iron, coal, or gold and does not fire.
  Used to save money in peacetime.
- **`bartprepare = True`** - the tower itself searches for targets in `searchradius`
  and fires without an explicit order, like an infantryman holding position.

---

<a id="4-апгрейды-башни"></a>
<a id="4-улучшения-башни"></a>
## 4. Tower Upgrades

5 levels `eurtow.1..5`, each one reduces `weapon_pause`
by −20% / −20% / −10% / −10% / −10% (multipliers accumulate,
total ≈ 0.8 × 0.8 × 0.9³ ≈ 0.467 → **fire frequency × 2.14**). Full
list - in [`05_upgrades/README.md` → `tow`](../../../reference/05_upgrades/README.md).

The cost of leveling up increases with level: level 1 - several hundred
resources; level 5 – several thousand. See numerical data there.

---

<a id="5-время-постройки-и-время-сноса"></a>
## 5. Construction time and demolition time

`buildtime = 3937 × 10 / 32 = 1,230 game seconds`
for one peasant. With 6 builders (see
[`../../reports/economy/builder_slots.md`](../../../reports/economy/builder_slots.md))
- about `1230 / 6 × 1.13 ≈ 232 game seconds`, or roughly four game minutes.

Demolition: `20 000 HP / 1800 dmg cannonball ≈ 11 hits` → about 2 minutes
shelling with one cannon in the absence of repairs.

---
<a id="6-захват--только-во-время-постройки"></a>
## 6. Capture - only during construction

From [`../economy/capture_mechanics.md`](../economy/capture_mechanics.md):

- Completed Towers (`bbuilt = True`) **cannot be captured**:
  `bcapture` is `False` from initialization. Capture checks still run
  for every unfinished building, so a Tower can change ownership only
  while it is under construction [^2].
- Towers in construction are captured according to the usual rules
  capturing buildings: infantryman approaches `captureradius = 4`
  tile, there are no defenders in the radius - instant capture.

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
- **Modest vision (`vision = 3`)** means the Tower needs nearby scouts
  to cover its flanks.
- **Spread 1.88 t** - the tower **misses** single targets.
  It is effective against concentrations of infantry or cavalry, but
  less reliable against a single Hetman.
- **A completed Tower cannot be captured, only destroyed.** Building
  one on contested ground is risky because the unfinished structure can
  be seized.
- **An unfinished Tower is the better target:** while under construction
  it has `shield / 3` (see [`combat_damage_pipeline.md` §2](combat_damage_pipeline.md)),
  plus the ability to capture.

---

<a id="8-открытые-эмпирические-вопросы"></a>
<a id="8-что-ещё-требует-проверки"></a>
## 8. Questions Requiring Further Testing

1. **Exact formula for disp when firing.** `dispertion = 1.88 t` -
   This is a basic value, but does distance make a difference? It looks like
   `maxdisp = dist × disp × 0.0267` (as for regular ranged units; see
   [`target_selection.md` §9](target_selection.md)) - measurement needed.
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

[^2]: See [`../economy/capture_mechanics.md`](../economy/capture_mechanics.md) -
      a Tower has `bcapture = False` from initialization, but the
      `not bbuilt` branch still calls `_misc_CheckCapture` for every
      unfinished building.
