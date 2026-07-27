<a id="recon-формации"></a>
<a id="построения-и-их-боевые-бонусы"></a>
# Formations and Their Combat Bonuses

[← How the game works](../../README.md)

This article explains the available formations, their combat bonuses, and
the difference between moving normally and holding position (the internal
`fHoldMode` flag). Script references and Pascal excerpts are collected in
[Sources](#sources).

<a id="коротко"></a>
## TL;DR

- Formations are stored in the text config `data/game/var/formations.cfg`,
  total **149** records; indexed by numbers `0..159`
  (`gc_formation_maxcount = 160`) [^1].
- Each formation specifies an internal number (`id`), a mask-reflection mode
  (`symmetry`), two sets of bonuses
  (`bonusdamage` / `bonusshield` for movement and `bonusdamagehold` /
  `bonusshieldhold` while holding), and a **position mask** (`mask`) for
  rank-and-file units and officers.
- Bonuses are additive, not percentage: `+2` to damage = simple
  `damage += 2` after all other modifiers [^2].
- Standard combat formations (from `LINE15` and larger) give
  **+2 attack / +2 shield** while moving and **+7 / +7** while standing
  to death" (`fHoldMode = True`).
- The engine represents a squad with `TSquad`. Its formation bonus is applied
  through the fields
  `fAddDamage`, `fAddShield`, `fAddDamageHold`, `fAddShieldHold` —
  they are cumulative with each hit to/from a squad unit.
- The mask size is limited by `gc_formation_maskmaxwidth = 54` × 
  `gc_formation_maskmaxheight = 24`. One squad contains up to 196
  units in normal mode and up to 400 in `*400` mode.

---

<a id="1-каталог-формаций"></a>
## 1. Formation Catalog

`gFormation[160]` is a global array of records. Each entry stores
string identifier `sid` (`LINE15`, `SQUARE36`, ...), parameter
`symmetry` (0 - asymmetrical, 1 - horizontal reflection, 2 - horizontal
vertical, 3 - on both axes), two pairs of bonuses
(`bonusdamage` / `bonusshield` for movement and
`bonusdamagehold` / `bonusshieldhold` for holding), grid dimensions,
and two Boolean matrices: `mask` for rank-and-file positions and
`maskofficers` for Officer positions [^7].

The config is read once when the game starts by the procedure
`_init_InitializeFormations()` [^3].

<a id="11-семейства"></a>
### 1.1. Families

| Prefix | Count | Purpose |
|---|---:|---|
| `LINE` | 61 | Line 3–10 units (without bonus), then 15 / 36 / 72 / 120 / 196 / 400 (with bonus). |
| `LINEMORB` | 19 | "Line with Curb" - expanded options for naval units. |
| `SQUARE` | 12 | Full square square: 15 / 36 / 72 / 120 / 196 / 400 + options `*NB` without bonus. |
| `KARE` | 12 | Hollow square (melee on the perimeter, arrows inside): dimensions are similar to `SQUARE`. |
| `TRI` | 12 | Triangular formation (historical, for cavalry). |
| `PRUS` | 12 | Prussian system (national version for Prussia). |
| `SHER` | 12 | Ranks (historical). |
| `SHIPS` / `SHIPSN` / `PACK` | 6 | Naval formations. |
| `ALONE` / `ODIN` | 2 | Single unit. |
| `none` | 1 | Without formation (zero entry). |

<a id="12-бонусы-по-размерам"></a>
### 1.2. Bonuses by size

Standard values that a squad receives *in formation*:

| Size | Internal variant | Moving damage | Moving defence | Holding damage | Holding defence |
|---|---|---:|---:|---:|---:|
| 3–10 | `LINE3..LINE10` | 0 | 0 | 0 | 0 |
| 15 | `LINE15`, `SQUARE15`, `KARE15` | 2 | 2 | 7 | 7 |
| 36, 72, 120, 196 | `LINE36..196`, `SQUARE36..196`, `KARE36..196` | 2 | 2 | 7 | 7 |
| 400 | `LINE400`, `SQUARE400`, `KARE400` | 3 | 3 | 7 | 7 |
| 15+ `*NB` | `SQUARE15NB`, `KARE36NB` ... | 0 | 0 | 0 | 0 |
| historical | `TRI`, `PRUS`, `SHER` (without `_OLD`) | 1 | 1 | 1 | 1 |
| `*_OLD` | `TRI_OLD`, `PRUS_OLD` | −10..+5 | −5..+9 | −27..+95 | −19..+80 |

Variants ending in `_OLD` are remnants of early game versions and are
rarely used in the current rosters.

The `NB` suffix means “No Bonus”: the formation keeps its layout without
granting a combat advantage. This is useful in scenarios or AI behavior
where the shape itself matters.
<a id="13-лимиты-на-нацию-и-отряд"></a>
### 1.3. Limits per nation and squad

- Per nation - `gc_country_maxformationcount = 3` available
  formational sets (for example, in Prussia it is `LINE`/`SQUARE`/`PRUS`).
- In one formation - no more than `gc_country_maxformationunitcount = 12`
  units of **different types** (that is, mask marks the positions of 12 different
  unit classes).
- Officer mask - up to `gc_country_maxofficersformationmask = 50`
  marked “officer here.”

---

<a id="2-где-живёт-бонус-tsquad"></a>
## 2. Where the Bonus Lives: `TSquad`

The entry `TSquad` (defined in `lib/classes.script`) stores four
formation bonus numeric fields - `fAddDamage` / `fAddShield` for
movement, `fAddDamageHold` / `fAddShieldHold` for holding - and
boolean flag `fHoldMode` [^8].

These fields are **taken directly** from the selected `gFormation[i]` and
are rewritten whenever the formation changes. Thus, saying that a squad
uses the 15-unit line (internal variant `LINE15`) does not mean that the
script contains a line such as
`squad.formationId = LINE15` - there are four numbers in `TSquad` and
name (`fSid`) for UI.

---

<a id="3-применение-бонуса-в-формуле-урона"></a>
## 3. Applying the Bonus in the Damage Formula

Source: `lib/miscext2.script:_misc_DoDamage` [^4].

Both the attacker and the target can belong to a squad. The formation's
**defence bonus** applies to the **target**: if the defender
`fHoldMode` is enabled, `fAddShieldHold` is taken, otherwise `fAddShield`;
the total is subtracted from the damage. Bonus **damage** added
**attacker**: symmetrically via `fAddDamageHold` / `fAddDamage`,
but is added to damage.

This happens **after** subtracting `shield` and `protection[kind]`, but
before checking `damage < 1 → damage := 1`. Therefore, formational
the boost **can push a weak hit out of the "1 HP minimum"
back to operating range**.

Conversely, if the defender holds formation (`+7` defence), a small hit
of 4–6 damage can fall below one and be clamped to the minimum of 1 HP.
Holding formation is therefore especially effective against light hits.

<a id="31-числовые-примеры"></a>
### 3.1. Numerical examples

A Musketeer, 18th century, with 14 base damage (`damage = 14`) fires at
an 18th-century infantryman with one point of general defence
(`shield = 1`) and one point of bullet protection
(`protection[bullet] = 1`):

| Target's position | Holding formation | Final damage |
|---|---|---:|
| No | — | `14 − 1 − 1 = 12` |
| `LINE15` | no | `14 − 1 − 1 − 2 = 10` |
| `LINE15` | yes | `14 − 1 − 1 − 7 = 5` |
| `SQUARE400` | yes | `14 − 1 − 1 − 7 = 5` |

Now the same Musketeer attacks from a 15-unit line (`LINE15`) while the
target is outside a squad:

| Attacker's position | Holding formation | Final damage |
|---|---|---:|
| No | — | 12 |
| `LINE15` | no | `12 + 2 = 14` |
| `LINE15` | yes | `12 + 7 = 19` |

If both are in formations, the bonuses are summed up: `+attacker` and
`−target` are independent.

---

<a id="4-hold-mode-fholdmode--стоять-насмерть"></a>
<a id="4-режим-стоять-насмерть-fholdmode"></a>
## 4. Hold Position (`fHoldMode`)

`fHoldMode` - squad flag, which is switched by the interface or
script. When enabled:

1. The pair `fAddDamageHold` / `fAddShieldHold` is used (usually `+7`
   against `+2` on the move) - **greatly** increases survivability and attack.
2. Units do not lose formation because of the path of their own comrades.
3. The unit **does not move** voluntarily: even when ordered to “attack”
   The units will first deploy into formation and only then move.

The associated flag is `fHoldFire`: “do not open fire until explicitly ordered.”
This is a separate mechanism not related to `fHoldMode`, although it is usually
turn on together.

<a id="41-когда-выгоден-hold"></a>
<a id="41-когда-выгодно-удерживать-строй"></a>
### 4.1. When holding formation helps

- **Defence.** Ranged units in the 15-unit square (`SQUARE15`) gain
  `+7` defence and survive a volley
  better than no formation. In numbers: 14 musket damage → 14 − 1 −
  1 − 7 = **5** versus 12 without formation.
- **18th-century line infantry.** `LINE` formations are quick to assume,
  making a held line a common defensive tactic.

<a id="42-когда-невыгоден-hold"></a>
<a id="42-когда-удержание-строя-мешает"></a>
### 4.2. When holding formation gets in the way

- **Cavalry attack.** For an immediate strike, disable hold position;
  otherwise the riders first take their assigned places.
- **Pursuit.** A squad holding position will not catch a retreating enemy.

---

<a id="5-mask-как-юниты-раскладываются-по-строю"></a>
<a id="5-схема-мест-в-строю"></a>
## 5. Position Masks

In `mask : struct.begin` of each formation there is an ASCII map of positions.
For example, `LINE5` - five units with double spacing:
```
*..*..*..*..*
```
`SQUARE36` - 6x6 square:
```
*.*.*.*.*.*
.*.*.*.*.*.
*.*.*.*.*.*
.*.*.*.*.*.
*.*.*.*.*.*
.*.*.*.*.*.
```
`KARE15` - hollow square (melee around the perimeter):
```
*****
*...*
*...*
*...*
*****
```
Cell size - `gc_obj_radius_formation_default = 8` pixels (for
cavalry - `gc_obj_radius_formation_horse = 12`) [^5]. That is
`LINE5` has a width of `5 × 8 = 40` pixels × visual scale.

The `symmetry` parameter affects **how** melee mask unfolds
when moving: 0 - without mirroring; 1 — reflected horizontally;
2 - vertically; 3 - on both axes.

`maskofficers` is a parallel mask that marks the cells into which
you need to appoint officers (drummer, standard bearer). Their positions are often
central or dedicated so that the officer is protected by the rank and file.

---

<a id="6-когда-меняется-формация"></a>
## 6. When the formation changes

Formation changes are implemented in `lib/squad.script`, primarily by
functions prefixed `_squad_*`. The triggers are:

| Trigger | Result |
|---|---|
| The player selects a formation in the interface | Recalculates `gFormation[i]` for the squad immediately. |
| The squad receives reinforcements or takes losses | May switch to a smaller formation (`LINE36 → LINE15`) when 15 or fewer units remain. |
| Hold position is enabled or disabled | Changes only `fHoldMode`, not the formation ID. |
| The squad is disbanded | Sets `fSid := ''` and clears the bonuses. |

The size of the formation is **selected automatically** according to the number of units:
if in `LINE15` 5 units died and 10 remained, `_squad_*`-function
will switch to `LINE10` (or `LINE9`, depending on the cleanup logic).

---

<a id="7-создание-и-расформирование-tsquad"></a>
## 7. Creating and Disbanding `TSquad`

<a id="71-создание"></a>
### 7.1. Creation

`_player_CreateSquad` assembles a formation only if
`_unit_IsOfficer(officerHnd) = True` [^9]. The assembly entry point,
`_unit_MakeSquadList` [^10] accepts `officerHnd`, searches around the
Officer for a Drummer and suitable rank-and-file units, then
`_player_SetSquadFormation` places units in the grid and records
`fAddDamage / fAddShield` from `gFormation[formInd]` [^11]. Therefore,
a new `TSquad` with recorded bonuses can appear only under a
**living Officer**.

After assembly, `_player_SetSquadFormation` places the Officer and
Drummer in cells from `maskOfficers`, and rank-and-file units in `mask`.
If the Officer is no longer present when the grid is rebuilt, that cell
remains `0`, but the fields `fAddDamage / fAddShield` were written
earlier and **do not depend on the composition of the grid**.

<a id="72-расформирование-disband"></a>
<a id="72-расформирование-отряда"></a>
### 7.2. Disbanding a squad

On every `Progress` tick, `CheckSquadsDisband` runs for each active
player [^12]:

| Condition | Result |
|---|---|
| `count(non-officer) < gc_player_SquadDismissPercent × fBaseCount` | `_misc_DisbandSquad` removes `TSquad`. After this, the `if (pSquad2 ≠ nil)` branch in the damage formula is skipped, and the bonus for the remaining units is not found. |

Parameters:
- `gc_player_SquadDismissPercent = 0.25` [^13] — threshold share.
- `_squad_GetBaseUnitCount(pSquad)` equals
  `TSquad.GetCount − 1 − 1` (minus officer, minus drummer, if
  present). **Only rank-and-file units** count toward the threshold.

Formation bonuses therefore disappear **not when the Officer dies**, but
when the rank-and-file count drops below 25% of the original `fBaseCount`.

<a id="73-hold-mode-fsm-порог-простоя"></a>
<a id="73-переход-в-режим-удержания-после-простоя"></a>
### 7.3. Entering hold mode after an idle period

The stronger hold bonus (for `LINE`, `SQUARE`, and `KARE`: `+7` damage
and defence at sizes 15–196, or a change from `+3/+3` to `+7/+7` at
size 400) is active while
`TSquad.fHoldMode = True`. State machine [^14]:

| State | Transition conditions |
|---|---|
| `fHoldMode := True` | `fStandGround = True`, `fHoldMode = False`, `fAgressive = False`, `fMoveCount = 0`, and the accumulated `fHoldModeProgress` (growing at the rate of `deltatime / gc_squad_holdmode_time` per tick) reached 1.0. |
| `fHoldMode := False` | The squad receives a movement order [^15]. |

Parameters: `gc_squad_holdmode_time = 150 × 8 × gc_frames_to_time =
37.5` game seconds of idleness in Hold Position [^16];
`gc_frames_to_time = 0.03125`.

Thus, **the stronger bonus activates after 37.5 game seconds** of
continuous idleness without aggression or movement.
As soon as you move the unit, `fHoldMode` is reset, and the accumulation
starts again.

---

<a id="7-морские-формации"></a>
<a id="8-морские-построения"></a>
## 8. Naval Formations

The `SHIPS`, `SHIPSN`, and `LINEMORB` families are intended for ship
squads. Their bonuses are similar or zero, while their position masks
account for much larger ship radii
(`gc_obj_radius_formation_default × 8`, or 64+ pixels).

Sea battle has its own characteristics (see.
[`naval_combat.md`](naval_combat.md)).

---

<a id="8-влияние-формации-на-pathfinding"></a>
<a id="8-влияние-построения-на-движение"></a>
<a id="9-влияние-построения-на-движение"></a>
## 9. How Formations Affect Movement

Within one squad:
- Each unit knows its “target cell” in mask relative
  leader.
- While moving, the squad travels as a loose group; once it stops, its
  units take their assigned places with a small random offset (see
  [`pathfinding.md` §6](pathfinding.md)).
- If a unit is knocked out of place, for example by cavalry, the squad
  **does not wait** for it to return; a gap remains in the formation.

Between squads - different squads of the same side pass through
each other softer than scattered units, thanks
`SetGameObjectAlignmentToFlagman` - squad flag “align with
standard bearer" reduces the pushing force inside the formation.

---

<a id="9-открытые-эмпирические-вопросы"></a>
<a id="10-что-ещё-требует-проверки"></a>
## 10. Questions Requiring Further Testing

1. **Do two formation bonuses apply simultaneously** if
   the same unit falls under several formations (for example,
   18th century infantry in the formation of a regiment under the common “banner of the commander”)?
   Apparently not - `TSquad` only stores one set of bonuses.
   Confirm with measurements.
2. **Exact meaning of `symmetry = 3`.** When a squad turns 180° and its
   mask is mirrored on both axes, where does the right-flank cavalry
   move? This requires an editor test or screenshots.
3. **Formation switching speed.** A full rearrangement appears to take
   0.4–0.6 game seconds, depending on unit count and pathfinding. This
   estimate needs measurement.

---

<a id="источники"></a>
## Sources

[^1]: `data/scripts/dmscript.global` — `gc_formation_maxcount = 160`,
      `gc_formation_maskmaxwidth = 54`, `gc_formation_maskmaxheight = 24`.

[^2]: `data/scripts/lib/miscext2.script:_misc_DoDamage`. Bonus
      added as `damage := damage − bonus` (for target) or
      `damage := damage + bonus` (for attacker) after `shield`,
      `protection[kind]`, before checking `damage < 1 → 1`.

[^3]: `data/scripts/lib/init.script:_init_InitializeFormations`.
      Loads `gc_filepath_formations = './data/game/var/formations.cfg'`
      via `ParserLoadFromFileByHandle`, parses 149 records and
      fills in the global `gFormation[160]`.

[^4]: `data/scripts/lib/miscext2.script:_misc_DoDamage` —
      lines `if (TSquad(pSquad2).fHoldMode) then bonus :=
      TSquad(pSquad2).fAddShieldHold else bonus :=
      TSquad(pSquad2).fAddShield;`.

[^5]: `data/scripts/dmscript.global` —
      `gc_obj_radius_formation_default = 8`,
      `gc_obj_radius_formation_horse = 12`. Used in
      pathfinding to determine the width of the formation.

[^7]: Record `gFormation[i]` stores:
      ```pascal
      record
         id : Integer;
         sid : String;
         symmetry : Integer;
         bonusdamage, bonusshield : Integer;
         bonusdamagehold, bonusshieldhold : Integer;
         width, height : Integer;
         countunits, countofficers : Integer;
         mask : array [0..23, 0..53] of Boolean;
         maskofficers : array [0..23, 0..53] of Boolean;
      end
      ```
The dimensions of the mask are `gc_formation_maskmaxheight` × `gc_formation_maskmaxwidth`.

[^8]: `data/scripts/lib/classes.script` - definition of `TSquad`.
      Fields `fAddDamage`, `fAddShield`, `fAddDamageHold`,
      `fAddShieldHold` and `fHoldMode` live on each unit and
      are rewritten by the formation change procedure.

[^9]: `data/scripts/lib/player.script:914` - tuning assembly only
      under a living officer: `if _unit_IsOfficer(officerHnd) then ...`.

[^10]: `data/scripts/lib/unit.script:6280-6315` —
       `_unit_MakeSquadList(officerHnd)`. Looking for a drummer and
       suitable rank-and-file units around the Officer.

[^11]: `data/scripts/lib/player.script:809-812` - record bonuses
       in `TSquad`:
       ```pascal
       TSquad(pSquad).fAddDamage     := gFormation[formInd].bonusdamage;
       TSquad(pSquad).fAddShield     := gFormation[formInd].bonusshield;
       TSquad(pSquad).fAddDamageHold := gFormation[formInd].bonusdamagehold;
       TSquad(pSquad).fAddShieldHold := gFormation[formInd].bonusshieldhold;
       ```
[^12]: `data/scripts/units/global.inc/progress.inc:5-35, 174-175` —
       `CheckSquadsDisband` every tick:
       ```pascal
       basecount := TSquad(pSquad).fBaseCount;
       count     := _squad_GetBaseUnitCount(pSquad);
       if count < basecount * gc_player_SquadDismissPercent then
           _misc_DisbandSquad(plHnd, i, true);
       ```
`_misc_DisbandSquad` - `data/scripts/lib/misc.script:2893-2935`.

[^13]: `data/scripts/dmscript.global:156` —
       `gc_player_SquadDismissPercent = 0.25`.
       `_squad_GetBaseUnitCount` - `data/scripts/lib/squad.script:98-107`.

[^14]: `data/scripts/units/global.inc/progress.inc:160-172` —
       Hold-mode state machine.

[^15]: `data/scripts/units/global.inc/writemove.inc:42-44`,
       `data/scripts/lib/player.script:1453-1455` - reset
       `fHoldMode := False` when ordering movement.

[^16]: `data/scripts/dmscript.global:174, 180` - parameters
       Hold-mode: `gc_squad_holdmode_time = 150 × 8 × gc_frames_to_time
       = 37.5` game seconds.
