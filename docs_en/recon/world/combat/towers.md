<a id="recon-башни"></a>
# Recon: towers

In-depth analysis: how the turret fires, target designation, resources for
shot, upgrades, capture and demolition. All links to the code are in
[Sources](#sources).

> **Tower garrison is not implemented in Cossacks 3.** In scripts
> `peasantabsorber` is installed **only** for mines (`coa` /
> `gol` / `iro` branches in `unit.script`). Towers (`tow`),
> City centers, Housing and Barracks do not accept infantry inside -
> the “drive the musketeers into the tower” mechanic from other RTS games is missing.
> Garrison via `inside[]` exists, but is only used for
> **transport ships** (`btransport = True`) - see.
> [`naval_combat.md` §4](naval_combat.md). This fixes it
> a common misconception that was previously present in this
> document.

## TL;DR

- Tower - building with built-in `weapon` (cannonball, 1000 damage) and
  review `vision = 3` (32 FOW tiles).
- Automatic shooting via `bartprepare = True`: the tower itself
  looks for targets in the `searchradius = 26.25` tile and shoots.
- Each shot costs **10 iron + 30 coal** (for European) or
  more in Turkish; permanent content - `consume[gold] = 500`,
  which according to the formula `× 32 / 20000` gives **0.8 gold / g-sec =
  48 gold/g-minute**. If there is a shortage of resources, the tower is silent
  stops shooting.
- 5 upgrade levels `eurtow.1..5` speed up reload time to **×2.14**.
- **Capture is only possible while the tower is under construction.** In `unit.script`
  for `<prefix>tow`, `bcapture = False` is explicitly set (via
  `SetObjBuildingBaseSettings(objprop, False, ...)`), the flag is not
  changes according to `bbuilt`. The finished tower in `_misc_CheckCapture` is not
  hits: handler `nothing` for buildings calls `CheckCapture`
  only with `bbuilt=False` (any building under construction) or with
  `bcapture=True` (ready). Therefore, capture the completed tower
  It’s impossible - it can only be destroyed with weapons. Tower under construction -
  you can: `not bbuilt` handler branch `Nothing` is calling
  `_misc_CheckCapture` regardless of `bcapture`, and infantry
  enemy in a 4-tile radius without defenders changes
  owner via `_misc_ChangePlayer`.
- **There is no garrison in the tower** (see quote block above).

---

<a id="1-что-делает-здание-башней"></a>
## 1. What makes a building a “tower”

In `unit.script` in the `'tow'` branch the key
fields [^1]:

| Field | Meaning | What |
|---|---|---|
| `usage` | `gc_obj_usage_tower` | Tower type. |
| `weapon[0]` | `cannonball`, damage 1000 | Built-in weapons. |
| `weapon[0].weaponsid` | `'PPOINTTTOW'` | Specific projectile (see `weapon.script`). |
| `weapon[0].cost[iron]` | 10 | For the shot. |
| `weapon[0].cost[coal]` | 30 | For the shot. |
| `weapon[0].fxshot` | `'shottower'` | Flash effect. |
| `weapon[0].dispertion` | `_misc_PixelsToTiles(100) = 1.88 t` | Scatter. |
| `searchradius` | `_misc_PixelsToTiles(1400) = 26.25 t` | Target auto-lock radius. |
| `consume[gold]` | 500 | Constant upkeep (by formula: 500 × 32 / 20000 = **0.8 gold / g-sec**). |
| `vision` | 3 | → 32 FOW tiles. |
| `peasantabsorber` | (not specified) | **Garrison not supported.** |
| `bgarrison` | (not specified) | Same. |

Parameters `SetObjBuildingProperties(20000, 3937, 120)`:
- HP = 20,000.
- `buildtime` = 3937 frames × 10 / 32 = **1230 g-sec**.
- 120 — `costpercent` (each next tower is 20% more expensive).

Price: 0 food / 100 wood / 100 stone / 150 gold / 0 iron / 0 coal.

---

<a id="2-числовые-параметры-базовой-европейской-башни-eurtow"></a>
## 2. Numerical parameters of the basic European tower (`eurtow`)

| Parameter | Meaning | Note |
|---|---:|---|
| HP | 20,000 | rus 21 000, tur 22 500 |
| `vision` | 3 → 32 FOW tiles | less than the average hussar |
| `searchradius` | 1400 px = **26.25 t** | target auto-lock radius |
| Damage | **1000** | `cannonball` - penetrates armor by `prot_cannonball` |
| `weapon_pause` | 400 frames = **12.5 g-sec** | one shot every 12.5 g-sec |
| Shot range | 1500 px = **28.13 t** | tur 30 t |
| Scatter | 100 px = **1.88 t** | rus 125; a projectile may miss a single unit |
| Shot cost | **10 iron + 30 coal** | tur: 15 iron + 40 coal |
| Contents | `consume[gold] = 500` → **0.8 gold / g-sec** (48 / g-min) | formula `consume × 32 / 20000`, the same as for food (see [`../economy/hunger_and_rebellion.md` §2.3](../economy/hunger_and_rebellion.md)) |
| Capture | `bcapture = False` (after construction) | the tower is **never** captured when completed |

### 2.1. Variations by nation

- **Russian Tower** (`rustow`) reloads faster: `pause = 300`
  frames = 9.4 g-sec (versus 12.5 for the European one), with HP +5%.
- **Turkish Tower** (`turtow`) hits harder, but less often: `damage = 1200`
  (+20%), `pause = 500` (−25% to the rate of fire), `range = 30 t`. And
  costs more: 40 coal + 15 iron versus 30/10.

---

## 3. Tower targeting

Tower is a normal building with weapons, so **uses a common one
algorithm** `_unit_SearchEnemyScanCells` (see
[`target_selection.md` §3](target_selection.md)). Features:

| Parameter | At the tower | At the infantry |
|---|---|---|
| `scanmode` | `priest_or_tower` (no load balancing) | `default` for melee, `default` for marksman |
| Search Cone | 360° (no limit) | 360° for idle, 30° for attack-move |
| Accounting `STO_count` | No | Yes for melee |
| Impact reaction | Shoots at the source if in radius | Same |

That is, the tower always fires at the **nearest** enemy in radius,
no matter how many other units are already firing at him.

### 3.1. Range and view

With vision `vision = 3` (32 FOW tiles), the tower **sees further** than
its `searchradius = 26.25` or firing range `28.13 t`. This
it is necessary that the tower can “start aiming” as soon as the enemy
will appear in the viewing area, and open fire as soon as it enters
shooting zone.

### 3.2. Subtleties of behavior

- **Each shot costs resources.** With zero `iron` or `coal`
  the turret **doesn't fire**. During Rebellion (`gold = 0`) she
  stops consuming gold, but also when there is a shortage of iron/coal
  silently loses firepower. See
  [`../../../internals/engine/animation_system.md` §7](../../../../internals_en/engine/animation_system.md)
  about how exactly resources are written off at the time of a swing.
- **`bturnoff = True`** - the tower can be **manually disabled** through it
  UI A disabled tower does not spend iron / coal / gold and does not fire.
  Used to save money in peacetime.
- **`bartprepare = True`** - the tower itself searches for targets in `searchradius`
  and shoots without the player's command, like an infantryman in standground mode.

---

## 4. Tower upgrades

5 levels `eurtow.1..5`, each one reduces `weapon_pause`
by −20% / −20% / −10% / −10% / −10% (multipliers accumulate,
total ≈ 0.8 × 0.8 × 0.9³ ≈ 0.467 → **fire frequency × 2.14**). Full
list - in [`05_upgrades/README.md` → `tow`](../../../reference/05_upgrades/README.md).

The cost of leveling up increases with level: level 1 - several hundred
resources; level 5 – several thousand. See numerical data there.

---

## 5. Construction time and demolition time

`buildtime = 3937 × 10 / 32 = 1230 g-sec`
for one peasant. With 6 builders (see
[`../../reports/economy/builder_slots.md`](../../../reports/economy/builder_slots.md))
- about `1230 / 6 × 1.13 ≈ 232 g-sec ≈ 4 game minutes`.

Demolition: `20 000 HP / 1800 dmg cannonball ≈ 11 hits` → about 2 minutes
shelling with one cannon in the absence of repairs.

---
<a id="6-захват--только-во-время-постройки"></a>
## 6. Capture - only during construction

From [`../economy/capture_mechanics.md`](../economy/capture_mechanics.md):

- Completed towers (`bbuilt = True`) **not captured** - from
  they are available `bcapture = True` only while they are being built. After
  completion of construction `bcapture` is removed [^2].
- Towers in construction are captured according to the usual rules
  capturing buildings: infantryman approaches `captureradius = 4`
  tile, there are no defenders in the radius - instant capture.

Therefore, the counter-strategy against the enemy tower is to attack **in
time of construction**: either demolish or capture. After completion
Only heavy artillery has a chance.

---

<a id="7-стратегические-выводы"></a>
## 7. Strategic conclusions

- **Tower is a worthwhile investment, but not free.** Contents
  ≈ 0.8 gold / g-sec × 10 towers = 8 gold / g-sec = **480 gold per
  game minute** only for the “tax”, plus 30 coal + 10 iron for
  each shot (1 time per 12.5 g-sec). On a long game 10
  towers significantly drag on the economy.
- **Low `vision = 3`** - the tower does not see the flanks well. Don't put
  her alone on the hill: scouts are needed nearby.
- **Spread 1.88 t** - the tower **misses** single targets.
  Effective against concentrations of infantry or cavalry, but not against
  single Hetman.
- **The tower cannot be captured - only demolished.** Therefore, economically
  it is unprofitable to put it under construction “on the disputed territory” - it
  easily intercepted.
- **It is more important to attack a tower under construction than a completed one:** c
  construction `shield / 3` (see [`combat_damage_pipeline.md` §2](combat_damage_pipeline.md)),
  plus the ability to capture.

---

<a id="8-открытые-эмпирические-вопросы"></a>
## 8. Open empirical questions

1. **Exact formula for disp when firing.** `dispertion = 1.88 t` -
   This is a basic value, but does distance make a difference? It looks like
   `maxdisp = dist × disp × 0.0267` (same as for regular shooters, see
   [`target_selection.md` §9](target_selection.md)) - measurement needed.
2. **Garrison shooting for forts.** In the campaign / Historical
   Battle has "forts" that can accept infantry. This
   **not** standard tower (`tow`-sid) - needs to be checked separately
   on campaign scripts.

---

<a id="источники"></a>
## Sources

[^1]: `data/scripts/lib/unit.script` - branch `'tow'`. Basic
      parameters via `SetObjBuildingBaseSettings`,
      `SetObjBuildingProperties(20000, 3937, 120)`,
      `SetObjBaseWeapon(...damage=1000, pause=400, range=550-1500...)`.
      Price via `SetObjBasePrice(0, 100, 100, 150, 0, 0)`.

[^2]: See [`../economy/capture_mechanics.md`](../economy/capture_mechanics.md) -
      `bcapture` for the tower is reset when construction is completed.
