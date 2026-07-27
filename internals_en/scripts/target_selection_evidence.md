<a id="recon-выбор-цели-и-attack-move"></a>
<a id="выбор-цели-и-атака-с-движением"></a>
<a id="технический-разбор-выбора-цели-и-атаки-с-движением"></a>
# Technical Evidence for Target Selection and Attack-Move

[← Scripts and Scenarios](structure.md)

[Reader guide to target selection](../../docs_en/recon/world/combat/target_selection.md)

This article explains why a formation does not always attack the nearest
enemy, how melee units spread across several targets, and how ordinary
movement differs from attack-move. The main rules use player-facing terms;
function, mode, and field names are collected under
[Technical details and implementation](#technical-details-and-implementation)
and [Sources](#sources).

<a id="кратко"></a>
## At a Glance

- Search uses a **grid** [^1]. The map is divided into fixed cells, each
  holding units by player. The game checks a rectangle around the searching
  unit, keeps one candidate from each cell, then compares them.
- Traversal within a cell begins at a random position; the first candidate
  that passes every filter is retained [^2].
- For **melee units**, a target becomes 12.5% less attractive for every ally
  already heading toward it. This spreads a line across the enemy front
  instead of piling everyone onto one opponent [^3].
- **Ranged units** do not use that balancing and favor the nearest target
  within range.
- During the first 0.25 game second after moving, a ranged unit loses up to
  three cells of effective detection radius. Full range returns at rest [^4].
- **Attack-move** makes infantry and cavalry search in every direction every
  100 ms. Ordinary movement limits automatic reaction to a 30° forward cone
  [^5].
- **Artillery** fires at fixed coordinates rather than following a selected
  unit. The point does not move with the enemy [^6].

---

<a id="как-игра-выбирает-цель"></a>
## How the Game Chooses a Target

1. The game takes a rectangle of grid cells around the unit.
2. It starts at a random position inside each cell and retains one valid
   candidate.
3. A ranged unit compares candidates by distance. A melee unit also counts
   how many allies already chose each enemy.
4. Targets outside the minimum and maximum range are discarded.
5. Healing, capture, and special computer-player tasks use separate filters.

As a result, neighboring units in one formation may choose different
opponents even when one enemy looks slightly closer on screen.

<a id="что-важно-для-управления"></a>
## What Matters for Unit Control

| Situation | Result |
|---|---|
| Melee units enter a dense line | They spread across the front because an already selected target becomes less attractive. |
| Ranged units see several enemies | Each chooses independently; there is no shared automatic focus fire. |
| Ordinary movement passes an enemy | The unit mainly reacts to enemies inside a 30° forward cone. |
| Attack-move | Search covers every direction and updates regularly. |
| Artillery fires at a point | It keeps firing at the coordinates even after the enemy leaves. |

<a id="технические-подробности-и-реализация"></a>
## Technical Details and Implementation

<a id="1-точки-входа"></a>
<a id="точки-входа"></a>
### Entry Points

Four functions drive the target-selection process:

| Function | When it is called | Role |
|---|---|---|
| `_unit_SearchVictim` [^7] | one-off search, such as a ranged unit retreating or reassessing manually | requests a target within the ring `[r0..r1]` around a point |
| `_unit_SearchVictimOnProgress` [^8] | each unit-progress tick, roughly every 100 ms | handles automatic attacks and reactions while moving |
| `_unit_SearchEnemyScanCells` [^1] | called by both functions above | scans grid cells and selects the best available target |
| `_unit_SearchEnemyInCell` [^9] | called from `_unit_SearchEnemyScanCells` | inspects the units stored in one cell |

`_unit_SearchVictimOnProgress` derives the search mode (`scanmode`) and
radii from `objprop`, then calls `_unit_SearchEnemyScanCells`. Each cell
contributes a candidate from `_unit_SearchEnemyInCell`; the outer scan
returns the candidate with the smallest adjusted distance.

The scan grid (`gScanGrid`, `gScanGridUnits`) partitions the map into
fixed-size cells and tracks each player separately. Every cell stores a list
of present units and player bitmasks (`fplmask`, `myplmask`,
`enemyplmask`). Cells that contain no relevant player can therefore be
discarded without inspecting their unit lists [^10].

---

<a id="2-unitsearchenemyincell--выбор-внутри-одной-ячейки"></a>
<a id="выбор-внутри-одной-ячейки"></a>
### Selection Within One Cell

The function returns one object handle, `goHnd`, or 0 when no candidate
qualifies [^9].

<a id="21-какие-игроки-рассматриваются"></a>
<a id="какие-игроки-рассматриваются"></a>
#### Which Players Are Considered

The loop checks up to `gc_MaxPlayerCount` players represented in the cell,
then filters by friend-or-enemy affiliation. Normal combat considers enemies
only; healing (`scanmode = 1`) does the opposite and considers allies only
[^11].

<a id="22-случайный-стартовый-индекс-и-циклический-проход"></a>
<a id="случайный-стартовый-индекс-и-циклический-проход"></a>
#### Random Starting Index and Cyclic Scan

The starting index is `floor(random × count)`, where `count` is the number
of that player's units in the cell. The function then visits all `count`
entries cyclically from that index. The first candidate to pass every check
is selected, and the branch exits through `break(MAIN)` [^2].

This means: **within one cell the choice is statistically uniform**
among eligible candidates. If a cell contains four eligible enemy
Musketeers, each has the same chance of being selected.

<a id="23-фильтры-на-кандидата"></a>
<a id="фильтры-на-кандидата"></a>
#### Candidate Filters

The basic filters are:

- `trgHnd <> 0`,
- `trgHnd <> goHnd` (not the searching unit itself),
- visual state is not `gc_statetag_visual_hide`,
- essential state includes `gc_statetag_essential_none` (the unit is neither
  dying nor being created).

Range is calculated differently for melee and ranged combat. The `bmelee`
flag is true when the maximum attack radius does not exceed
`gc_unit_meleeattackradius`. Ranged units lose
`gc_obj_maxattackradiusdisp × uniqrnd` from their search radius; melee units
do not [^12].

The constants are `gc_unit_meleeattackradius = 0.5` cell and
`gc_obj_maxattackradiusdisp = 3` cells [^13]. A ranged unit loses up to
`3 × uniqrnd` cells of effective radius during the scan.
This penalty applies to target selection. The firing-range penalty at
`standtime < 0.25` is a separate mechanic described in
[Ranged-Unit Behavior §4](../../docs_en/recon/world/combat/ranged_units_behavior.md#4-штраф-к-дальности-при-движении-standtime).

The topology check accepts a target in the same connected area. For ranged
combat, it can also accept a target whose Euclidean distance does not exceed
`maxRad + max((goY - trgY) × 2, 0)`, including the high-ground bonus [^14].
Melee therefore requires a shared land area or island; ranged combat has an
additional direct-distance path.

<a id="24-диспетчер-по-scanmode"></a>
<a id="режимы-отбора-кандидата"></a>
#### Candidate-Selection Modes

This block determines which valid candidate is selected. Modes 0–3 leave
through `break(MAIN)` after finding the first compatible target [^15]:

| `scanmode` | Used for | Selection rule |
|---:|---|---|
| 0 (default) | ordinary combat | first enemy with `material ∈ {body, iron}`, or `material = wood` when the attacker is a building; `bcankill` is also checked through `kmask AND mmask`. |
| 1 (healer) | a unit with `objprop.bpriest = True` | first allied unit with `hp < maxhp`; if the first candidate is already at full health, this pass returns no result. |
| 2 (capture fallback) | most land units during periodic updates | first searches for a killable target as in mode 0; if none is found, makes another pass for `bcapture && _unit_TestCapture(trgHnd)`. |
| 3 (capture only) | specialized capture tasks | returns the first candidate that passes `bcapture` and `_unit_TestCapture`; other objects are ignored. |
| 4 (special sabotage) | special computer-controlled tasks | examines all candidates and selects the highest `weapon[0].damage`, choosing the most dangerous target rather than the nearest. |

“First” in modes 0, 1, 2, and 3 means the first candidate encountered by the
randomized traversal from the previous section. Mode 4 does not exit early:
it updates `Result` until the highest `damage` value has been found.

---

<a id="3-unitsearchenemyscancells--обход-ячеек"></a>
<a id="обход-ячеек"></a>
### Scanning Cells

The scan returns one object handle, `goHnd`, or 0 [^1].

<a id="31-прямоугольник-ячеек"></a>
<a id="прямоугольник-ячеек"></a>
#### Scan Rectangle

`_misc_CalcScanCellsMinMax` calculates the cell boundaries around the unit,
after which a nested `i × j` loop visits the rectangle. `x1` and `y1` are the
unit's own cell; `rx1` is the cell radius,
`floor(maxsearchdist / gc_scangrid_size) + 1`. The scan therefore covers a
square of `(2 × rx1 + 1)²` cells, usually 3×3 or 5×5 [^16].

<a id="32-цикл-и-две-метрики"></a>
<a id="цикл-и-две-метрики"></a>
#### Two Distance Metrics

For each cell, `_unit_SearchEnemyInCell` returns one candidate. The outer
scan checks whether that candidate lies within the permitted range ring
(`minsearchdistSqr < distSqr < maxsearchdistSqr`) and updates **two
metrics**: the absolute nearest target, `minTrgHnd`, and the nearest target
after load adjustment, `minRelativeTrgHnd`. The function returns
`minRelativeTrgHnd` [^17].

Important details:

- **Range ring.** `minsearchdist` is the inner dead zone and
  `maxsearchdist` is the outer limit. A moving ranged unit uses
  `Sqr(maxsearchdist - 3 × uniqrnd)`; a stationary ranged unit or any melee
  unit uses `maxsearchdist²` [^4].
- **Two parallel metrics.** `minTrgHnd` is the physically nearest target.
  `minRelativeTrgHnd` is the nearest candidate after target-load adjustment
  (see §3.3).
- The function returns `minRelativeTrgHnd`, so load balancing always affects
  the result. The unadjusted `minTrgHnd` is calculated but not returned. A
  source comment explains why the absolute-distance shortcut is not useful
  when only one unit is sampled from each cell [^18].

<a id="33-балансировка-нагрузки-для-рукопашников"></a>
<a id="балансировка-нагрузки-для-рукопашников"></a>
#### Melee Target-Load Balancing

`stolist` contains units whose current state already targets this opponent.
It therefore measures how many units are moving toward or attacking that
target, not merely how many happen to stand within attack range. For melee
selection, the adjusted distance is
`distSqr × (1 + stolist.GetCount × 0.125)`, which makes a heavily contested
target appear farther away [^3].

Effect of target load on melee distance:

| `STO_count` | Multiplier for `distSqr` | On the square of the distance |
|---:|---:|---|
| 0 | ×1.000 | real distance |
| 1 | ×1.125 | +6.1% linear distance |
| 4 | ×1.500 | +22.5% |
| 8 | ×2.000 | +41.4% |
| 16 | ×3.000 | +73.2% |

If eight allies are already heading toward a target, that target effectively
moves 41% farther away. The next Pikeman is therefore likely to choose
another enemy in the same cell, spreading the formation across the front.

Ranged units do not use this balancing. Their target distribution comes from
projectile dispersion and cell traversal, not an explicit load metric.

<a id="34-ранний-выход-для-рукопашников"></a>
<a id="ранний-выход-для-рукопашников"></a>
#### Early Exit for Melee Combat

If a melee unit finds an improved target **inside half a scan cell** (about
four cells), the scan stops. Continuing to seek a better-balanced opponent
would add little because the current target is already very close. The
threshold is `cOkDist = (gc_scangrid_size / 2)²` [^19].

Ranged units have no equivalent early exit and always scan the full
rectangle.

---

<a id="4-unitsearchvictimonprogress--периодический-поиск"></a>
<a id="периодический-поиск"></a>
### Periodic Search

The unit's state logic refreshes target search roughly every 100 ms. This
update decides whom to attack at that moment [^8].

<a id="41-радиусы"></a>
<a id="радиусы"></a>
#### Radii

Base values come from `objprop`: `searchdist = objprop.searchradius` and
`minsearchdist = objprop.minattackradius`. A ranged unit on high ground gains
`searchdist += goHeight × 2` when `goHeight > 0`. A melee unit on guard has
its search distance capped by `gc_gameplay_meleeguardmaxsearchdist`, so it
does not chase too far [^20].

For more about the high-ground bonus, see
[Ranged-Unit Behavior §7](../../docs_en/recon/world/combat/ranged_units_behavior.md#7-high-ground--бонус-с-возвышенности).

<a id="42-выбор-scanmode"></a>
<a id="42-выбор-режима-поиска-scanmode"></a>
<a id="выбор-режима-поиска"></a>
#### Choosing the Search Mode

Religious healers use `scanmode = 1`. Capturable units such as artillery,
along with ships and buildings, use mode 0 and search only for attack
targets. Other land units such as infantry and cavalry use mode 2: attack
first and try capture only when no killable target exists [^21].

An infantry unit will therefore **try to capture** a defenseless gun or
Storehouse when there is nothing nearby to attack.

<a id="43-диспетчер-обхода"></a>
<a id="выбор-способа-обхода"></a>
#### Choosing the Scanning Method

The game chooses one of three scanning procedures. Ships use
`_unit_SearchEnemyScanCellsShips`; long-range units or large radii use
`_unit_SearchEnemyScanCellsLongRange`; ordinary units use
`_unit_SearchEnemyScanCells` [^22].

The long-range scan checks up to 18 cells (`cLongRangeTryNum = 18`) and
returns **the first valid target**, rather than searching for the nearest.

---

<a id="5-атака-с-движением"></a>
## 5. Attack-Move

Attack-move looks like one action to the player, but its implementation
depends on the unit type and on what the player aimed at.

<a id="51-для-пехоты-и-кавалерии--gcobjordertypemove-с-подрежимами"></a>
<a id="51-пехота-и-кавалерия"></a>
### 5.1. Infantry and Cavalry

An order's `progress` field stores its movement submode [^5]:

| Submode | Constant | Behavior |
|---|---|---|
| `move_mode_default` | 0 | normal movement to the point |
| `move_mode_attack` | 1 | attack-move: every periodic update calls `_unit_SearchVictimOnProgress` and, if it finds a target, issues `_unit_OrderAttack` |

The profile flag `gProfile.bsearchenemyinfront`, enabled by default [^23],
adds a forward search to ordinary movement. If the angle between movement
and a potential target is at most `cMinAngle = 30°`, the unit turns to
attack [^24].

Ordinary right-click movement can therefore trigger combat, but **only for
enemies inside a 30° forward cone**. Enemies to the side or rear are ignored.
Attack-move has no such restriction and can select a nearby enemy in any
direction.

<a id="52-для-артиллерии--gcobjordertypeattackpoint"></a>
<a id="52-артиллерия"></a>
### 5.2. Artillery

`_player_OrderUnitsToAttackPoint` only processes units with
`objprop.bartprepare = True`. For each matching unit, it clears
`bstandground`, enables `bsearchenemy`, optionally removes previous orders,
and issues `_unit_OrderAttackPoint` with the chosen coordinates [^6].

`bartprepare = True` is set for the Cannon (`cannon`), Howitzer
(`howitzer`), and Frame gun (`framegun`; see [^25] for the exact script
branches). These units:

1. Receive `gc_obj_order_type_attackpoint` with the chosen coordinates.
2. At each update, `_unit_TryAttackPoint` [^26] checks whether the point is
   in range and fires. The point is fixed and belongs to no unit.
3. Area damage affects everyone inside the blast radius (see
   [How Damage Is Calculated §6.5](../../docs_en/recon/world/combat/combat_damage_pipeline.md)).
4. Because `bsearchenemy := True`, artillery may also notice an enemy inside
   its ordinary radius, but the current `attackpoint` order remains until the
   shot is completed.

Unlike attack-move, artillery **fires at the coordinate** even after the
target leaves. This supports area denial and indirect fire, but it also means
the gun may keep shelling empty ground until given a new order.

<a id="53-через-gui"></a>
<a id="53-через-интерфейс"></a>
### 5.3. Interface Orders

The interface sends an order packet processed by
`units/global.inc/readorder.inc`. Three branches set
`bsearchenemy := True` [^27], all for orders that should allow automatic
enemy acquisition:

- normal movement `move`,
- `move_mode_attack`,
- `attackpoint` (artillery).

Automatic target acquisition therefore remains active unless
`bstandground` is set while `standtime > 0`. The behavior is described in
[Ranged-Unit Behavior §1-2](../../docs_en/recon/world/combat/ranged_units_behavior.md#1-standground-vs-обычный-режим).

---

<a id="6-что-отсюда-следует-для-микроконтроля"></a>
## 6. Practical Implications for Unit Control

- **Ranged units do not focus fire automatically.** Units in the same squad
  choose independently rather than coordinating a shared target. To make all
  36 Musketeers fire at one enemy, issue an explicit attack order. After that
  target dies or leaves range, every Musketeer evaluates the battlefield
  independently again.
- **Melee units spread along the front.** Each additional Pikeman considers
  how many allies already chose a candidate and is more likely to take
  another at a similar distance.
- **Ordinary movement watches a 30° forward cone.** Cavalry approaching from
  the rear or flank may not trigger a Musketeer's automatic attack. Use
  attack-move or stop the unit explicitly.
- **Fire at a point creates zone denial.** Artillery keeps shelling the
  chosen coordinates with its normal dispersion instead of following an
  enemy.
- **A recently moving ranged unit loses up to three cells of detection
  radius.** A unit with `uniqrnd ≈ 0.9` loses 2.7 cells, while one with
  `≈ 0.1` loses 0.3. Parts of one line may therefore notice the same target
  at different times.
- **Special computer-controlled sabotage chooses the highest-damage enemy**, not
  the nearest one. This is not ordinary combat behavior; see
  [computer-player behavior](../../docs_en/recon/systems/ai_behavior.md).

---

<a id="7-лечение-священниками--bpriest"></a>
<a id="7-лечение-духовными-лицами-bpriest"></a>
<a id="7-как-духовные-лица-выбирают-раненых"></a>
## 7. How Religious Units Choose Wounded Allies

The Priest (`priest`), Pope (`pope`), Mullah (`mullah`), and Padre (`padre`)
form a special class. They scan
**friendly units only** and choose the first wounded ally encountered. If the
first candidate is already at full health, the search returns no result.

Healing uses a separate branch of the calculation (see
[How Damage Is Calculated §5](../../docs_en/recon/world/combat/combat_damage_pipeline.md)) [^32]:
```
target.hp += weapon.damage              # WITHOUT shield or protection
target.hp := min(target.hp, target.maxhp)
```
The healing delay is zero (`heal pause = 0`), so the healer restores health
every animation cycle, roughly every 0.7 game second, until the target is
fully healed.

| Unit | Healing per hit | Range (pixels / cells) | Availability |
|---|---:|---|---|
| Priest (`priest`) | 20 | 0–400 / 7.5 | most European nations |
| Pope (`pope`) | 25 | 0–350 / 6.6 | Papal States / Venice |
| Mullah (`mullah`) | 15 | 0–500 / **9.4** | Turkey / Algeria (longest range) |
| Padre (`padre`) | 30 | 0–400 / 7.5 | Spain / Portugal (strongest healing) |

<a id="71-стратегические-свойства"></a>
### 7.1. Strategic Properties

- **Healing ignores armor and shield** and restores the full weapon value.
- **Several Priests can heal one target in parallel.** Four Priests restore
  80 health per cycle, about 115 per game second, to a 282-health Reiter.
- **The Mullah has the longest range** and can heal from the second line.
- **The Padre has the strongest heal**, 30 health per hit.
- Religious healers have little health and no armor, making them priority
  raid targets.

<a id="72-конверсии-нет"></a>
### 7.2. No Conversion

Unlike missionaries in Age of Empires II, religious units in Cossacks 3 are
**healers only**. They cannot convert enemy units. See also
[building capture](../../docs_en/recon/world/economy/capture_mechanics.md)
§7.

---

<a id="8-реакция-отряда-на-полученный-удар"></a>
## 8. How a Squad Reacts to Damage

When a non-artillery unit takes damage in `_misc_DoDamage`, the script sets
its squad's `TSquad.fAgressive := True` and updates `fLastBattleTime` [^33].
In effect, **one damaging hit wakes the whole squad**, which then searches
for the attacker and counterattacks.

<a id="81-стратегические-следствия"></a>
### 8.1. Strategic Implications

- **One Archer can activate an entire computer-controlled squad.** This can
  be used as a distraction while another force attacks the flank.
- **Computer-controlled artillery is an exception:** taking a hit does not
  switch it into the aggressive state, so it continues its current order.
- A covert Peasant raid should avoid unnecessary attacks, which can alert
  the whole enemy squad.

See also [How Damage Is Calculated §8](../../docs_en/recon/world/combat/combat_damage_pipeline.md)
about the same effect from the damage formula.

---

<a id="scattering-and-shot-accuracy"></a>
<a id="9-рассеяние-и-точность-выстрела"></a>
## 9. Dispersion and Shot Accuracy

Each projectile is displaced from the intended target by
`_weapon_CalcShotDispertion` [^34]:
```
maxdisp = dist × disp × 0.0267         # in cells
shot_x  = target_x + (1 − random × 2) × maxdisp
shot_z  = target_z + (1 − random × 2) × maxdisp
```
`dist` is the distance to the target in cells; `disp` is
`weapon.dispertion`, also converted to cells. Dispersion grows linearly with
distance.

<a id="91-базовые-значения-dispertion"></a>
<a id="91-базовые-значения-разброса-dispertion"></a>
<a id="91-базовые-значения-разброса"></a>
### 9.1. Basic Dispersion Values

| Weapon | Dispersion (pixels / cells) | Deviation at 15 cells |
|---|---:|---:|
| Streltsy (`SHOTMUSKET`, base) | 200 / 3.75 | ±1.50 cells |
| Archer (`STRELA`) | 175 / 3.28 | ±1.31 cells |
| Archer (`OSTRELA`, fire arrow) | 200 / 3.75 | ±1.50 cells |
| Musketeer, base | 250 / 4.69 | ±1.88 cells |
| Cannon (`PPOINTT`) | ~250 / 4.69 | ±1.88 cells |
| Tower (`PPOINTTTOW`) | ~100 / 1.88 | ±0.75 cells |
| Yacht or Galley (`PPOINTTKOR`) | 25 / 0.47 | ±0.19 cells |

<a id="92-шанс-попасть-в-юнит-размером-11-тайл-на-дистанции-d"></a>
<a id="chance-to-hit-a-1x1-tile-unit-at-a-distance-d"></a>
<a id="92-шанс-попасть-в-юнит-размером-11-клетка-на-дистанции-d"></a>
### 9.2. Chance to Hit a 1×1-Cell Unit at Distance `d`

- If `2 × maxdisp ≤ 1` → ~100% hit.
- If `2 × maxdisp > 1` → the approximate chance of landing inside the
  target square is `1 / (2 × maxdisp)`.

Example: a Musketeer with `disp = 3.75` at 15 cells gives
`maxdisp = 1.50`, window ±1.50 = 3.00 → chance of hitting the target 1×1 ≈
**1/3 = 33%** in one shot. Idealized calculations that ignore dispersion can
therefore underestimate the time needed to kill a target by about threefold.

<a id="93-апгрейды-на-dispertion"></a>
<a id="93-улучшения-разброса-dispertion"></a>
<a id="93-улучшения-точности"></a>
### 9.3. Accuracy Upgrades

Only for **artillery**:
- `aca.20` (“Research new sighting devices for artillery”):
  **−35% dispersion**.
- `aca.27` (“Develop mathematics”): **−35%**, stacking with `aca.20`.

For musketeers and archers there is **no direct** dispersion upgrade.

---

<a id="10-открытые-вопросы"></a>
## 10. Open Questions

| # | Question | How to verify it |
|---:|---|---|
| 1 | The exact condition under which the interface sends `move_mode_default` instead of `move_mode_attack`: presumably right-click means movement, while A + click means attack-move. The scripts do not expose this decision. | Test it in the editor or inspect the interface calls in native code. |
| 2 | Was the 0.125 weight in `stolist` target-load balancing derived analytically or tuned empirically? | Compare with Cossacks 1 or measure the target distribution of 36 Pikemen against 36 Musketeers. |
| 3 | Which units satisfy `_misc_GetShotPointsCount(goHnd) > 0` and therefore use `_unit_SearchEnemyScanCellsLongRange`? Artillery certainly does and Towers probably do; the full list must be extracted from `objprop.shotpoints`. | Run `parse_animations.py` or search directly for `shotpoints`. |
| 4 | The long-range scan always returns the first match. Does that make long-range units less selective, or is the behavior overridden in native code? | Profile an AI scenario with one Mortar against several targets. |

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
[^3]: `stolist` target-load balancing for melee — `lib/unit.script:5188-5198`:
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
[^13]: Radius constants — `dmscript.global:113-116` (`gc_unit_meleeattackradius = 0.5` cell, `gc_obj_maxattackradiusdisp = 3` cells).

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
[^22]: Scan dispatcher (water, long-range, or regular) —
         `lib/unit.script:5494-5503`:
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

[^26]: `_unit_TryAttackPoint` — `lib/unit.script:7512` onward.

[^27]: Order processor with `bsearchenemy := True` - `units/global.inc/readorder.inc:63, 88, 97`.

[^32]: Healing formula via `gc_obj_weapon_kind_heal` -
       `lib/miscext2.script:371-398`. Description of the priests and their
       parameters (heal/impact, range) - `lib/unit.script:1151-1188`.

[^33]: The squad's reaction to damage received is `lib/miscext2.script:406-417`.
       Update `TSquad.fAgressive := True` and `fLastBattleTime`
       upon the first successful hit on any unit of the squad.

[^34]: Shot dispersion — `_weapon_CalcShotDispertion` in
       `lib/weapon.script:625`. The coefficient `0.0267` is hard-coded;
       `weapon.dispertion` comes from the weapon definitions in
       `lib/weapon.script` after `_misc_PixelsToTiles`.
