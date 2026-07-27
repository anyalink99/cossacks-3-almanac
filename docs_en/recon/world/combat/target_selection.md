<a id="recon-выбор-цели-и-attack-move"></a>
<a id="выбор-цели-и-атака-с-движением"></a>
# Target Selection and Attack-Move

[← How the game works](../../README.md)

Reverse engineering the target search functions and how the order "attack to the point"
diverges into different processing branches depending on the type of unit. All
links to the code and the Pascal blocks themselves are collected in the [Sources](#sources) section
at the end of the document.

<a id="кратко"></a>
## TL;DR

- The search is carried out through **scan-grid** [^1] - the map is divided into fixed cells
  size, each stores its own list of units by player. The scanner bypasses
  a rectangle of cells around the finder, in each cell selects one
  candidate and in the end takes the closest one.
- Inside the cell, the order of traversal is **randomized**: the starting index is specified
  as `floor(random × count)`, and the first candidate that passes all filters,
  becomes the choice [^2].
- For **melee units** load balancing works between cells:
  the distance to the target is multiplied by `1 + STO_count × 0.125`, where `STO_count` is
  how many allied units are already heading towards this target. The more people are already hitting -
  then the target cell is considered “further”, and the second pikeman will prefer
  another enemy. This distributes the line along the front, rather than dumping it
  for one enemy [^3].
- For **shooting units** there is no balancing - the closest one is simply selected
  within radius.
- The shooter in motion (when `standtime ≤ 0.25` game seconds) loses up to
  three tiles of effective detection radius according to the formula
  `maxRad -= 3 × uniqrnd`. When standing, the full radius returns [^4].
- **Attack-move** for infantry and cavalry is order `gc_obj_order_type_move`
  with submode `move_mode_attack`. The unit goes to the point and every 100 ms
  searches for a target in full `searchradius`. With normal `move_mode_default`
  search limited to 30° front cone [^5].
- **Artillery** with flag `bartprepare` goes along a separate branch through
  `_player_OrderUnitsToAttackPoint` and receives `gc_obj_order_type_attackpoint` -
  shooting at a coordinate, not at a specific target. The point does not move
  enemy [^6].

---

<a id="1-точки-входа"></a>
## 1. Entry points

Four functions through which the entire target selection process goes:

| Function | When is it called | What answers |
|---|---|---|
| `_unit_SearchVictim` [^7] | one-time search (shooter withdrawal, manual reassessment) | direct request “find me a target in the ring `[r0..r1]` from the point” |
| `_unit_SearchVictimOnProgress` [^8] | each unit progress tick (~100 ms) | auto-attack and react to enemies while moving |
| `_unit_SearchEnemyScanCells` [^1] | called by both above | traversing scan-grid cells and selecting the minimally relevant target |
| `_unit_SearchEnemyInCell` [^9] | called from `_unit_SearchEnemyScanCells` | one pass through the list of units in one cell |

The cycle is like this: `_unit_SearchVictimOnProgress` determines the mode
(`scanmode`) and radii from `objprop`, then calls
`_unit_SearchEnemyScanCells`. That for each cell gets a candidate
from `_unit_SearchEnemyInCell` and at the end chooses the one who has
minimum relative distance.

scan-grid itself (`gScanGrid`, `gScanGridUnits`) is a partition of the map by
cells of a fixed size, separate for each player. In each
the cell stores a list of present units and a bitmask
(`fplmask`, `myplmask`, `enemyplmask`). This allows you to immediately filter
cells in which there is no enemy, and do not open them at all [^10].

---

<a id="2-unitsearchenemyincell--выбор-внутри-одной-ячейки"></a>
## 2. `_unit_SearchEnemyInCell` - selection within one cell

Returns one handle `goHnd` (or 0 if there is no candidate) [^9].

<a id="21-какие-игроки-рассматриваются"></a>
### 2.1 Which players are being considered

Loop through all `gc_MaxPlayerCount` players, filter by bit mask
presence in the cell and by affiliation (friend/enemy). Normal mode
Only enemy players are bypassed. At the priest's (`scanmode = 1`) -
on the contrary, only your own [^11].

<a id="22-случайный-стартовый-индекс-и-циклический-проход"></a>
### 2.2 Random starting index and looping

The starting index is specified as `floor(random × count)`, where `count` is
the number of player units in the cell. Next comes a cyclic pass through all
`count` elements starting from this random index (modulo
`count`). The first candidate who passes all checks is announced
selected - the corresponding branch makes `break(MAIN)` [^2].

This means: **within one cell the choice is statistically uniform**
among suitable candidates. If there are four enemy musketeers in a cell,
everyone has an equal chance of becoming a target.

<a id="23-фильтры-на-кандидата"></a>
### 2.3 Candidate filters

Minimum:

- `trgHnd <> 0`,
- `trgHnd <> goHnd` (not the searching unit itself),
- visual state is not `gc_statetag_visual_hide`,
- essential state includes `gc_statetag_essential_none` (the unit is not in its death
  and not at birth).

Radius - calculated differently for melee and ranged combat. First
The unit type is determined by the flag `bmelee` (it is true if the maximum
attack radius does not exceed `gc_unit_meleeattackradius`). For shooters from
radius, a random penalty is subtracted `gc_obj_maxattackradiusdisp × uniqrnd`,
for melee combat - no [^12].

Constants: `gc_unit_meleeattackradius = 0.5` tile,
`gc_obj_maxattackradiusdisp = 3` tile [^13]. Rifle unit
loses up to `3 × uniqrnd` effective radius tiles at the time of scanning.
This penalty applies specifically to target selection; range penalty
shot at `standtime < 0.25` - a separate story, described in
[`ranged_units_behavior.md` §4](ranged_units_behavior.md#4-штраф-к-дальности-при-движении-standtime).

Topological check: the target is valid if it is in the same topology zone,
the same as the attacker, or (for ranged combat) if the distance is in the Euclidean norm
does not exceed `maxRad + max((goY - trgY) × 2, 0)` (with bonus for
elevation) [^14]. That is, melee requires a common area (one land,
one island), and the shooter can penetrate either the general zone, or simply
line of sight within a radius.

<a id="24-диспетчер-по-scanmode"></a>
### 2.4 Dispatcher by `scanmode`

This block determines which valid candidate is selected.
All branches use early exit `break(MAIN)` after finding the first
compatible target [^15]:

| `scanmode` | Where does it turn on | Whom does he choose |
|---:|---|---|
| 0 (default) | regular unit | the first enemy with `material ∈ {body, iron}` or (if the attacker is a building) `material = wood`. Additional filter `bcankill` via `kmask AND mmask`. |
| 1 (priest) | at unit `objprop.bpriest = True` | first **own** unit with `hp < maxhp`. If the first candidate is at full HP, the function exits the loop without a result. |
| 2 (capture fallback) | default for most units without `bcapture` during periodic updates | first looks for a killable target (as mode 0); if none is found, makes a separate pass for `bcapture && _unit_TestCapture(trgHnd)` and returns a capturable target. |
| 3 (capture-only) | specialized search (for example, AI on capture tasks) | returns the first valid `bcapture` + `_unit_TestCapture`, does not consider anything else. |
| 4 (AI sabotage) | special AI tasks | examines **all** candidates and selects the one with the greatest `weapon[0].damage`: the most dangerous target, not the nearest one. |

“First” in modes 0, 1, 2, 3 is the first according to that very random
bypass from §2.2. In mode 4, the cycle is not terminated by an early exit -
`Result` is updated to the maximum `damage`.

---

<a id="3-unitsearchenemyscancells--обход-ячеек"></a>
## 3. `_unit_SearchEnemyScanCells` — scanning cells

Returns one handle `goHnd` or 0 [^1].

<a id="31-прямоугольник-ячеек"></a>
### 3.1 Cell rectangle

Using `_misc_CalcScanCellsMinMax`, cell boundary indices are calculated
around the seeker's position; then double loop `i × j` on this
rectangle. `x1`, `y1` — index of the finder’s own cell in
scan-grid; `rx1` — radius in cells, considered at the top level
as `floor(maxsearchdist / gc_scangrid_size) + 1`. That is, it is covered
square `(2 × rx1 + 1)²` cells - usually 3x3 or 5x5 [^16].

<a id="32-цикл-и-две-метрики"></a>
### 3.2 The cycle and two metrics

For each cell, `_unit_SearchEnemyInCell` returns one candidate.
Then it is checked to see if it belongs to the ring of radii
(`minsearchdistSqr < distSqr < maxsearchdistSqr`) and update immediately
**two metrics**: absolute minimum distance `minTrgHnd` and
relative minimum `minRelativeTrgHnd` (taking into account the load on
target). What is returned is `minRelativeTrgHnd` [^17].

Notable points:

- **Ring of radii.** Both boundaries - `minsearchdist` (dead zone
  for shooters, the enemy hits it closely) and `maxsearchdist`
  (outer radius of the aimed shot). Shooter in motion counts
  by `Sqr(maxsearchdist - 3 × uniqrnd)`. Standing shooter and any
  melee - according to `maxsearchdist²` [^4].
- **Two parallel metrics.** `minTrgHnd` - simply absolutely
  nearest target. `minRelativeTrgHnd` - closest adjusted for
  “load” (see §3.3).
- **Returns `minRelativeTrgHnd`** - that is, it’s always an option
  with balancing; absolute `minTrgHnd` is calculated, but in
  as a result is not used. The author's comment is straight
  stipulates: *no help from relative dist cause we choose 1 unit
  from each cell* [^18].

<a id="33-балансировка-нагрузки-для-рукопашников"></a>
### 3.3 Load Balancing for Melee

`stolist` is a list of units whose state-target points to this goal.
That is, these are not “current within the attack radius”, but **how long are they going in principle?
or they are going to beat** this particular opponent. For melee combat
the relative distance is calculated as `distSqr × (1 + stolist.GetCount × 0.125)`,
that is, the "loaded" target is effectively pushed back [^3].

Melee effect when selected:

| `STO_count` | Multiplier for `distSqr` | On the square of the distance |
|---:|---:|---|
| 0 | ×1.000 | real distance |
| 1 | ×1.125 | +6.1% linear distance |
| 4 | ×1.500 | +22.5% |
| 8 | ×2.000 | +41.4% |
| 16 | ×3.000 | +73.2% |

The target, towards which eight of yours are already running, is effectively “moved away”
by 41% - and the second pikeman will most likely choose another enemy in the same
cell. This makes the formation more spread out along the front.

There is no balancing for shooters. All musketeers of one squad usually
knock down one nearby target; the distribution turns out naturally -
through the scattering of shots and the order of traversal of cells, and not through explicit
metric.

<a id="34-ранний-выход-для-рукопашников"></a>
### 3.4 Early exit for melee combat

If the melee finds the target **inside half of the scan-cell** (~4 tiles)
and improved `relativeDist`, the cycle through cells ends. Continue searching
a “more balancing suitable” opponent does not make sense -
the current one is already very close. Constant `cOkDist = (gc_scangrid_size / 2)²`
is calculated inside the function [^19].

There is no such option for shooters - they always go around the entire rectangle.

---

<a id="4-unitsearchvictimonprogress--периодический-поиск"></a>
## 4. `_unit_SearchVictimOnProgress` - periodic search

The unit's state machine calls this function roughly every 100 ms
(`gc_global_TimeProgressUnit`). She decides who to auto-attack
currently [^8].

<a id="41-радиусы"></a>
### 4.1 Radii

Basic values are taken from `objprop`: `searchdist = objprop.searchradius`,
`minsearchdist = objprop.minattackradius`. To the shooter (when
`minsearchdist > gc_unit_meleeattackradius`) a bonus is added with
hills - `searchdist += goHeight × 2`, if `goHeight > 0`.
For melee in Guard mode `searchdist` is limited from above
constant `gc_gameplay_meleeguardmaxsearchdist` - the guard does not leave
far [^20].

Bonus from higher ground - more details in
[`ranged_units_behavior.md` §7](ranged_units_behavior.md#7-high-ground--бонус-с-возвышенности).

<a id="42-выбор-scanmode"></a>
<a id="42-выбор-режима-поиска-scanmode"></a>
### 4.2 Selecting the search mode (`scanmode`)

The priest goes to `scanmode = 1`. All units that themselves are captured
(`bcapture` - for example, artillery), as well as water and buildings - in
`scanmode = 0` (kill only). All others are non-capturable
ground units (infantry, cavalry) - in `scanmode = 2`: priority to kill,
if you fail, capture [^21].

That is, an infantry unit **by default tries to capture** a defenseless
a gun or a warehouse, if there is nothing nearby to kill.

<a id="43-диспетчер-обхода"></a>
### 4.3 Scan dispatcher

Depending on the environment and the number of cells, one of three procedures is selected
bypass: for water units - `_unit_SearchEnemyScanCellsShips`, for
long-range (`_misc_GetShotPointsCount > 0`, artillery and turrets) or
large radius - `_unit_SearchEnemyScanCellsLongRange`, for
regular - `_unit_SearchEnemyScanCells` [^22].

The long-range scan traverses up to 18 cells (`cLongRangeTryNum = 18`) and selects
**the first valid goal that comes across** - he is not looking for the minimum.

---

<a id="5-атака-с-движением"></a>
## 5. Attack-move

In Cossacks 3, attack-move looks like one action to the player, but
in the code these are **several different orders** depending on the type of unit
and how the player aimed the sight.

<a id="51-для-пехоты-и-кавалерии--gcobjordertypemove-с-подрежимами"></a>
### 5.1 For infantry and cavalry - `gc_obj_order_type_move` with submodes

`progress` orders are stored in submode [^5]:

| Submode | Constant | Behavior |
|---|---|---|
| `move_mode_default` | 0 | normal movement to the point |
| `move_mode_attack` | 1 | attack-move: every periodic update calls `_unit_SearchVictimOnProgress` and, if it finds a target, issues `_unit_OrderAttack` |

Additionally there is a global profile flag
`gProfile.bsearchenemyinfront` (default `True` [^23]). He adds
**smart search** for `move_mode_default`: if a potential
the target and the angle between the direction of movement and the direction towards it are not
exceeds `cMinAngle = 30°`, the unit is automatically deployed to
attack [^24].

That is, when smart search is turned on, normal movement (right click)
also catches enemies, but **only those who are in a 30° cone in front**. Enemies
on the sides and back are ignored. When moving aggressively
(`move_mode_attack`) there is no such limitation - the closest enemy is taken
anywhere.

<a id="52-для-артиллерии--gcobjordertypeattackpoint"></a>
### 5.2 For artillery - `gc_obj_order_type_attackpoint`

`_player_OrderUnitsToAttackPoint` only processes units with
`objprop.bartprepare = True`. For each such unit it is removed
`bstandground`, set to `bsearchenemy`, optionally cleared
previous orders and issued `_unit_OrderAttackPoint` with coordinates [^6].

`bartprepare = True` is set for the Cannon (`cannon`), Howitzer
(`howitzer`), and Frame gun (`framegun`; exact
branches in the script - see [^25]). These units:

1. Get `gc_obj_order_type_attackpoint` with the coordinates of the point.
2. At each progress tick in `_unit_TryAttackPoint` [^26] check
   whether the point is within the radius, and shoot at it. Point from no one
   doesn't depend - it's just a coordinate.
3. AoE damage catches everyone who is in the explosion radius (see.
   [`combat_damage_pipeline.md` §6.5](combat_damage_pipeline.md)).
4. Because of `bsearchenemy := True`, the artillery itself selects in parallel
   target through `_unit_SearchVictimOnProgress`, if within its normal radius
   an enemy has appeared, but the current `attackpoint` order will not change,
   until it shoots back.

Difference from move-attack: artillery **fires at the coordinate**, even
if the target is gone. This is convenient for suppression and mortar support behind
line of sight. But if the enemy ran away, ordinary artillery with the order
attack-point hammers on an empty space until a new command.

<a id="53-через-gui"></a>
<a id="53-через-интерфейс"></a>
### 5.3 Via GUI

The GUI sends a packet that processes `units/global.inc/readorder.inc`.
It has three dots that indicate `bsearchenemy := True` [^27],
and they all correspond to orders, after which the unit must search for itself
enemy:

- normal movement `move`,
- `move_mode_attack`,
- `attackpoint` (artillery).

That is, “found an enemy - switched” works **always**, except
cases when `bstandground` clearly stands for `standtime > 0`. This behavior
described in
[`ranged_units_behavior.md` §1-2](ranged_units_behavior.md#1-standground-vs-обычный-режим).

---

<a id="6-что-отсюда-следует-для-микроконтроля"></a>
## 6. Practical implications for unit control

- **Ranged units do not focus fire automatically.** Units in the same squad
  select targets individually - random inside the cell plus
  `minRelativeTrgHnd` by cells - rather than coordinating a common goal.
  In order for all 36 musketeers to shoot at one enemy, you need to explicitly give
  `OrderAttack` (right click on target) and even that is held
  not hard: after killing or leaving the enemy from the radius, each unit
  will re-evaluate on its own.
- **Melee is distributed** along the front through STO balancing:
  Each next pikeman in the ranks takes into account how many he has already hit
  the current candidate, and given equal distances is more likely to choose
  another. Therefore, the formation of pikemen naturally covers the line
  enemies, rather than falling to one point.
- **Firing with retreat** is limited to the angle `cMinAngle = 30°`. If
  The shooter moves with a normal move (not aggressive) - he notices
  enemies only in the front cone. Cavalryman entering from the rear or
  flank, does not activate an auto attack for a musketeer moving forward along
  right click. You need either `move_mode_attack` or an explicit stop.
- **Artillery on a point is useful as a zone denial.** Placed on
  attack-point gun does not recalculate the target - it will shoot at
  coordinate with the assigned `dispertion`, covering the AoE of everyone who goes there
  comes in.
- **The shooter in motion is effectively “lower” by 3 tiles** in radius
  detection: `maxRad -= 3 × uniqrnd` while `standtime < 0.25`.
  A unit with a high `uniqrnd ≈ 0.9` immediately loses 2.7 tiles, a low
  `≈ 0.1` - 0.3 tiles. That is, in one line there are part of the musketeers
  will “see” the target earlier, the rest - later.
- **AI saboteur aims for maximum damage.** In `scanmode = 4` mode
  (special AI tasks for sabotage operations) the unit chooses
  not the closest, but the most dangerous enemy according to `weapon[0].damage`. This
  not “regular” AI; see [computer-player behavior](../../systems/ai_behavior.md), section
  "Open questions."

---

<a id="7-лечение-священниками--bpriest"></a>
<a id="7-лечение-духовными-лицами-bpriest"></a>
## 7. Healing by religious units (`bpriest`)

The Priest (`priest`), Pope (`pope`), Mullah (`mullah`), and Padre
(`padre`) form a special class
units with `bpriest = True`. Target selection algorithm - mode
`scanmode = 1` (see §2.1): **only own** players are scanned, and
the unit is selected according to the rule “the first one encountered with `hp < maxhp`”;
if the first candidate is already at full HP - exit without result.

The priest's "attack" is handled in a separate branch
`_misc_DoDamage` (see [`combat_damage_pipeline.md` §5](combat_damage_pipeline.md))
with `weapon.kind = gc_obj_weapon_kind_heal` [^32]. Formula:
```
target.hp += weapon.damage              # WITHOUT shield or protection
target.hp := min(target.hp, target.maxhp)
```
`heal pause = 0` - the priest heals every animation cycle
(~0.7 g-sec) until the target reaches full HP.

| Unit | Healing per hit | Range (pixels / tiles) | Availability |
|---|---:|---|---|
| Priest | 20 | 0–400 / 7.5 | most European nations |
| Pope | 25 | 0–350 / 6.6 | Papal States / Venice |
| Mullah | 15 | 0–500 / **9.4** | Turkey / Algeria (longest range) |
| Padre | 30 | 0–400 / 7.5 | Spain / Portugal (strongest healing) |

<a id="71-стратегические-свойства"></a>
### 7.1. Strategic properties

- **Healing ignores armor and shield** - restores HP by
  full `weapon.damage` regardless of target protection.
- **Several priests heal one target in parallel** —
  rater with 282 HP healed by 4 priests = +80 HP/cycle ≈ 115
  HP/real second.
- **Mullah has the longest range** - heals from the second
  line, inaccessible for melee combat.
- **Padre most effective** (30 / hit) - Spanish-Portuguese
  the army is very tenacious.
- Priests themselves are vulnerable (low HP, no armor) - priority
  target for raids.

<a id="72-конверсии-нет"></a>
### 7.2. No conversion

Unlike missionaries in Age of Empires II, religious units in Cossacks 3 are
**healer only**. No conversion of enemy units to friendly units
no scripts. See also [building capture](../economy/capture_mechanics.md)
§7.

---

<a id="8-реакция-отряда-на-полученный-удар"></a>
## 8. The squad's reaction to the blow received

Any non-artillery unit that takes damage in `_misc_DoDamage`,
switches its `TSquad.fAgressive := True` and updates
`fLastBattleTime` [^33]. Effect: **one damaging shot/hit
for any unit in the squad, switches the entire squad to combat mode** -
all units begin to actively search for the enemy and counterattack.

<a id="81-стратегические-следствия"></a>
### 8.1. Strategic Implications

- **AI peck by one archer** activates **entire** squad
  AI. Can be used as a distraction: one scout teases
  army, the rest are flanked.
- **AI Artillery is an exception** (special case in code): not
  switches to `fAgressive` from impact, continues to work in
  his order.
- **Hidden gathering activity** (raid by peasants in
  rear) - **do not attack** at all, otherwise the whole army will move.

See also [`combat_damage_pipeline.md` §8](combat_damage_pipeline.md)
about the same effect from the damage formula.

---

<a id="9-рассеяние-и-точность-выстрела"></a>
## 9. Scattering and shot accuracy

Each projectile shot is scattered relative to the target along
formula in `_weapon_CalcShotDispertion` [^34]:
```
maxdisp = dist × disp × 0.0267         # in tiles
shot_x  = target_x + (1 − random × 2) × maxdisp
shot_z  = target_z + (1 − random × 2) × maxdisp
```
`dist` — distance to target (tiles), `disp` — `weapon.dispertion`
(tiles, after `_misc_PixelsToTiles`). **The farther, the more
scattering**, linear.

<a id="91-базовые-значения-dispertion"></a>
<a id="91-базовые-значения-разброса-dispertion"></a>
### 9.1. Basic dispersion values

| Weapon | Dispersion (pixels / tiles) | Deviation at 15 tiles |
|---|---:|---:|
| Strelets (SHOTMUSKET, base) | 200 / 3.75 | ±1.50 t |
| Archer (STRELA) | 175 / 3.28 | ±1.31 t |
| Archer (OSTRELA fire) | 200 / 3.75 | ±1.50 t |
| Musketeer base | 250 / 4.69 | ±1.88 t |
| Cannon (PPOINTT) | ~250 / 4.69 | ±1.88 t |
| Tower (PPOINTTTOW) | ~100 / 1.88 | ±0.75 t |
| Yacht / galley (PPOINTTKOR) | 25 / 0.47 | ±0.19 t |

<a id="92-шанс-попасть-в-юнит-размером-11-тайл-на-дистанции-d"></a>
### 9.2. Chance to hit a 1x1 tile unit at a distance `d`

- If `2 × maxdisp ≤ 1` → ~100% hit.
- If `2 × maxdisp > 1` → chance ≈ `1 / (2 × maxdisp)` to get into
  the desired square.

Example: musketeer (`disp = 3.75`) on 15 tiles →
`maxdisp = 1.50`, window ±1.50 = 3.00 → chance of hitting the target 1×1 ≈
**1/3 = 33%** in one shot. That is, **TTK for long-range bullets and
arrows in idealized matrices is underestimated by 3 times**.

<a id="93-апгрейды-на-dispertion"></a>
<a id="93-улучшения-разброса-dispertion"></a>
### 9.3. Upgrades to dispersion

Only for **artillery**:
- `aca.20` (“Research new sighting devices for artillery”):
  **−35% dispersion**.
- `aca.27` (“Develop mathematics”): **−35%** (accumulates from
  `aca.20`).

For musketeers and archers there is **no direct** dispersion upgrade.

---

<a id="10-открытые-вопросы"></a>
## 10. Open questions

| # | Question | Where to dig |
|---:|---|---|
| 1 | The exact condition under which the interface sends `move_mode_default` instead of `move_mode_attack`: presumably right-click means movement, while A + click means attack-move. The scripts do not expose this decision. | Test it in the editor or inspect the interface calls in native code. |
| 2 | Weight 0.125 in STO balancing - chosen empirically or selected? | Compare with C1 or experimentally measure the spread of targets for 36 pikemen versus 36 musketeers. |
| 3 | `_misc_GetShotPointsCount(goHnd) > 0` as a condition for selecting `_unit_SearchEnemyScanCellsLongRange`: which units have this True? Artillery - definitely, towers - probably; the full list needs to be extracted from the definitions `objprop.shotpoints`. | `parse_animations.py` or direct grep using `shotpoints`. |
| 4 | The long-range scan always returns the first match. Does that make long-range units less selective, or is the behavior overridden in native code? | Profile an AI scenario with one Bombard against several targets. |

---

<a id="источники"></a>
## Sources

All links are relative to `data/scripts/` in the Cossacks 3 installation.

[^1]: `_unit_SearchEnemyScanCells` - `lib/unit.script:5142-5212`.

[^2]: Random starting index and cycling through the list of units in a cell - `lib/unit.script:4872-4877`:
    ```pascal
    var count : Integer = gScanGrid[cellx, celly].fPlCount[plind];
    rndind := floor(random * count);
    for i := 0 to count - 1 do
    begin
       newind := (rndind + i) mod count;
       trgHnd := gScanGridUnits[plind, cellx, celly].Get(newind);
       ...
    end;
    ```
[^3]: STO balancing for melee - `lib/unit.script:5188-5198`:
    ```pascal
    var pstolist : Pointer = _misc_GetObjectArgData(trgHnd, gc_argunit_stolist);
    relativeDist := distSqr * (1 + TIntegerList(pstolist).GetCount * 0.125);
    ```
[^4]: Calculation of `maxsearchdistSqr` (radius penalty for a moving shooter) - `lib/unit.script:5151-5156`:
    ```pascal
    var bmelee : Boolean = ...;
    if bmelee or (TObj(pobj).standtime > 0.25) then
       maxsearchdistSqr := maxsearchdist * maxsearchdist
    else
       maxsearchdistSqr := Sqr(maxsearchdist - gc_obj_maxattackradiusdisp * TObj(pObj).uniqrnd);
    ```
[^5]: Motion submode constants - `dmscript.global:715-718`.

[^6]: `_player_OrderUnitsToAttackPoint` — `lib/player.script:2447-2481`:
    ```pascal
    if (gObjProp[TObj(pobj).cid][TObj(pobj).id].bartprepare) then
    begin
       TObj(pobj).bstandground := False;
       TObj(pobj).bsearchenemy := True;
       if (bClearOrders) then _unit_ClearOrders(goHnd);
       _unit_OrderAttackPoint(goHnd, trgx, trgz, False, bClearOrders);
    end;
    ```
[^7]: `_unit_SearchVictim` - `lib/unit.script:5214-5262`.

[^8]: `_unit_SearchVictimOnProgress` - `lib/unit.script:5443-5520`.

[^9]: `_unit_SearchEnemyInCell` - `lib/unit.script:4832-4961`.

[^10]: Bit masks of players on the cell (`fplmask`, `myplmask`, `enemyplmask`) - `lib/unit.script:4842-4852`:
    ```pascal
    for plind := 0 to gc_MaxPlayerCount-1 do
    begin
       var enemyplmask : Integer = gPlayer[TObj(pObj).pl].enemyplmask;
       if scanmode <> 1 then
       begin
          if (gScanGrid[cellx, celly].fplmask and enemyplmask and (1 shl plind)) = 0 then
             continue;
       end
       else
       begin
          if (gScanGrid[cellx, celly].fplmask and gPlayer[TObj(pObj).pl].myplmask and (1 shl plind)) = 0 then
             continue;
       end;
       ...
    end;
    ```
[^11]: Same thread, see [^10].

[^12]: Radius calculation taking into account melee/ranged combat - `lib/unit.script:4867-4870`:
    ```pascal
    var maxRad : Float = _unit_GetMaxAttackRadius(goHnd);
    var bmelee : Boolean = maxRad <= gc_unit_meleeattackradius;
    if not bmelee then
       maxRad := maxRad - gc_obj_maxattackradiusdisp * TObj(pobj).uniqRnd;
    ```
[^13]: Radius constants - `dmscript.global:113-116` (`gc_unit_meleeattackradius = 0.5 t`, `gc_obj_maxattackradiusdisp = 3 t`).

[^14]: Topological target check - `lib/unit.script:4882-4889`:
    ```pascal
    if not bmelee then
    begin
       var trgX, trgY, trgZ : Float;
       GetGameObjectAbsolutePositionByHandle(trgHnd, trgX, trgY, trgZ);
       bFlag := (VectorDistance(goX, 0, goZ, trgx, 0, trgZ)) <= (maxRad + MaxFloat((goY - trgY) * 2, 0));
    end;

    if (_unit_GetRegion(trgHnd) = myRegion) or (bFlag) then ...
    ```
[^15]: Dispatcher for `scanmode` (select first compatible target) - `lib/unit.script:4894-4961`. All branches 0/1/2/3 use early exit `break(MAIN)`; branch 4 (`AI sabotage`) updates `Result` to the maximum `weapon[0].damage` and does not break.

[^16]: Counting a rectangle of cells - `lib/unit.script:5164-5170`:
    ```pascal
    var cellx, celly, cellxmax, cellymax : Integer;
    _misc_CalcScanCellsMinMax(x1, y1, rx1, cellx, celly, cellxmax, cellymax);
    var i, j : Integer;
    for [MAIN]i := cellx to (cellxmax) do
    for j := celly to (cellymax) do
       ...
    ```
[^17]: Main loop `_unit_SearchEnemyScanCells` - `lib/unit.script:5167-5210`:
    ```pascal
    for [MAIN]i := cellx to cellxmax do
    for j := celly to cellymax do
    begin
       trgHnd := _unit_SearchEnemyInCell(goHnd, i, j, scanmode);
       _misc_ScanGridCellDataUpdateResult(gScanGrid[i,j], trgHnd <> 0);
       if (trgHnd <> 0) then
       begin
          distSqr := Sqr(pX - GetGameObjectPositionXByHandle(trgHnd))
                   + Sqr(pZ - GetGameObjectPositionZByHandle(trgHnd));
          if (distSqr > minsearchdistSqr) and (distSqr < maxsearchdistSqr) then
          begin
             if (distSqr < mindist) then begin
                mindist := distSqr;
                minTrgHnd := trgHnd;
             end;
             if bmelee then
                relativeDist := distSqr * (1 + TIntegerList(pstolist).GetCount * 0.125)
             else
                relativeDist := distSqr;
             if (relativeDist < minRelativeDist) then
             begin
                minRelativeDist := relativeDist;
                minRelativeTrgHnd := trgHnd;
                if bmelee and (mindist < cOkDist) then break(MAIN);
             end;
          end;
       end;
    end;
    Result := minRelativeTrgHnd;
    ```
[^18]: Return `minRelativeTrgHnd` and author's comment - `lib/unit.script:5210`.

[^19]: Early exit for melee - `lib/unit.script:5200-5202`:
    ```pascal
    const cOkDist = (gc_scangrid_size / 2) * (gc_scangrid_size / 2);
    if bmelee and (mindist < cOkDist) then
       break(MAIN);
    ```
[^20]: Calculation of radii in `_unit_SearchVictimOnProgress` - `lib/unit.script:5456-5475`:
    ```pascal
    var pobjprop : Pointer = gObjProp[TObj(pobj).cid][TObj(pobj).id];
    var searchdist : Float = TObjProp(pobjprop).searchradius;
    var minsearchdist : Float = TObjProp(pobjprop).minattackradius;

    if (minsearchdist > gc_unit_meleeattackradius) then
    begin
       var goHeight : Float = GetGameObjectPositionYByHandle(goHnd);
       if (goHeight < 0) then goHeight := 0;
       searchdist := searchdist + goHeight * 2;     // high-ground bonus
    end
    else
    begin
       if (TObj(pobj).orders[0].itype = gc_obj_order_type_guard) then
          searchdist := MinFloat(searchdist, gc_gameplay_meleeguardmaxsearchdist);
    end;
    ```
[^21]: Selecting `scanmode` to `_unit_SearchVictimOnProgress` - `lib/unit.script:5487-5492`:
    ```pascal
    var scanmode : Integer;
    if (TObjProp(pobjprop).bpriest) then
       scanmode := 1
    else if (not ((TObjProp(pobjprop).bcapture) or (TObjProp(pobjprop).media = gc_obj_media_water) or (TObjProp(pobjprop).bbuilding))) then
       scanmode := 2;
    ```
[^22]: Bypass Manager (water/long-range/regular) - `lib/unit.script:5494-5503`:
    ```pascal
    if (TObjProp(pobjprop).media = gc_obj_media_water) then
       trgHnd := _unit_SearchEnemyScanCellsShips(goHnd, posX, posZ, minsearchdist, scangridx, scangridy, rx1, scanmode)
    else
    begin
       if (_misc_GetShotPointsCount(goHnd) > 0) then
          trgHnd := _unit_SearchEnemyScanCellsLongRange(goHnd, posX, posZ, minsearchdist, scangridx, scangridy, rx1, cLongRangeTryNum, scanmode)
       else
       if (rx1 <= 5) and (scanmode <> 1) then
          trgHnd := _unit_SearchEnemyScanCells(goHnd, posX, posZ, minsearchdist, searchdist, scangridx, scangridy, rx1, scanmode)
       ...
    end;
    ```
[^23]: Defaulted flag `bsearchenemyinfront = True` - `lib/profile.script:30`.

[^24]: Smart search (30° front cone) - `lib/unit.script:7334-7359`:
    ```pascal
    var bSmartSearch : Boolean = (gProfile.bsearchenemyinfront)
                              and (TObj(pobj).orders[0].itype = gc_obj_order_type_move)
                              and (TObj(pobj).orders[0].info.progress = gc_obj_order_move_mode_default);
    if bSmartSearch and (trgHnd <> 0) and (TObj(pobj).orders[0].bexecute) then
    begin
       ...
       const cMinAngle = 30;
       var dirx : Float = tpx - GetGameObjectPositionXByHandle(goHnd);
       var dirz : Float = tpz - GetGameObjectPositionZByHandle(goHnd);
       var dirx2 : Float = GetGameObjectPositionXByHandle(trgHnd) - GetGameObjectPositionXByHandle(goHnd);
       var dirz2 : Float = GetGameObjectPositionZByHandle(trgHnd) - GetGameObjectPositionZByHandle(goHnd);
       var angle : Float = VectorAngle(dirx, 0, dirz, dirx2, 0, dirz2);
       if (angle < cMinAngle) then
          _unit_OrderAttack(goHnd, trgHnd, True, False, False);
    end;
    ```
[^25]: `objprop.bartprepare := True` - `lib/unit.script:1724, 1756, 1846, 2240` (cannon, howitzer projective, framegun, tower built-in cannon).

[^26]: `_unit_TryAttackPoint` - `lib/unit.script:7512` and onwards.

[^27]: Order processor with `bsearchenemy := True` - `units/global.inc/readorder.inc:63, 88, 97`.

[^32]: Healing formula via `gc_obj_weapon_kind_heal` -
       `lib/miscext2.script:371-398`. Description of the priests and their
       parameters (heal/impact, range) - `lib/unit.script:1151-1188`.

[^33]: The squad's reaction to damage received is `lib/miscext2.script:406-417`.
       Update `TSquad.fAgressive := True` and `fLastBattleTime`
       upon the first successful hit on any unit of the squad.

[^34]: Scattering of shots - `_weapon_CalcShotDispertion` in
       `lib/weapon.script:625`. Coefficient `0.0267` —
       hard-coded; `weapon.dispertion` comes from the definition
       weapons in `lib/weapon.script` (after `_misc_PixelsToTiles`).
