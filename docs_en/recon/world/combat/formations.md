# Recon: formations

In-depth analysis: what formations are there, where bonuses are set, how
it is the squad that receives an increase in damage and shield, what is the difference between
normal and held formation (`hold`). All links to code and blocks
Pascal - in the [Sources](#sources) section at the end of the document.

## TL;DR

- Formations are stored in the text config `data/game/var/formations.cfg`,
  total **149** records; indexed by numbers `0..159`
  (`gc_formation_maxcount = 160`) [^1].
- Each formation specifies: `id`, `symmetry`, two sets of bonuses
  (`bonusdamage` / `bonusshield` for movement and `bonusdamagehold` /
  `bonusshieldhold` for holding), as well as **mask** - location
  units and officers in the ranks.
- Bonuses are additive, not percentage: `+2` to damage = simple
  `damage += 2` after all other modifiers [^2].
- Standard combat formations (from `LINE15` and larger) give
  **+2 attack / +2 shield** while moving and **+7 / +7** while standing
  to death" (`fHoldMode = True`).
- The squad is `TSquad`. Formation bonus is applied via fields
  `fAddDamage`, `fAddShield`, `fAddDamageHold`, `fAddShieldHold` —
  they are cumulative with each hit to/from a squad unit.
- The mask size is limited by `gc_formation_maskmaxwidth = 54` × 
  `gc_formation_maskmaxheight = 24`. One squad holds up to 196
  units in normal mode and up to 400 in `*400` mode.

---

## 1. Formation catalog

`gFormation[160]` is a global array of records. Each entry stores
string identifier `sid` (`LINE15`, `SQUARE36`, ...), parameter
`symmetry` (0 - asymmetrical, 1 - horizontal reflection, 2 - horizontal
vertical, 3 - on both axes), two pairs of bonuses
(`bonusdamage` / `bonusshield` for movement and
`bonusdamagehold` / `bonusshieldhold` for holding), mesh dimensions
and two Boolean matrices - `mask` for the positions of ordinary units and
`maskofficers` for officers [^7].

The config is read once when the game starts by the procedure
`_init_InitializeFormations()` [^3].

### 1.1. Families

| Prefix | How much | What is this |
|---|---:|---|
| `LINE` | 61 | Line 3–10 units (without bonus), then 15 / 36 / 72 / 120 / 196 / 400 (with bonus). |
| `LINEMORB` | 19 | "Line with Curb" - expanded options for naval units. |
| `SQUARE` | 12 | Full square square: 15 / 36 / 72 / 120 / 196 / 400 + options `*NB` without bonus. |
| `KARE` | 12 | Hollow square (melee on the perimeter, arrows inside): dimensions are similar to `SQUARE`. |
| `TRI` | 12 | Triangular formation (historical, for cavalry). |
| `PRUS` | 12 | Prussian system (national version for Prussia). |
| `SHER` | 12 | Ranks (historical). |
| `SHIPS` / `SHIPSN` / `PACK` | 6 | Marine formations. |
| `ALONE` / `ODIN` | 2 | Single unit. |
| `none` | 1 | Without formation (zero entry). |

### 1.2. Bonuses by size

Standard values that a unit receives *in formation*:

| Size | id | `+dmg` | `+shd` | `+dmg hold` | `+shd hold` |
|---|---|---:|---:|---:|---:|
| 3–10 | `LINE3..LINE10` | 0 | 0 | 0 | 0 |
| 15 | `LINE15`, `SQUARE15`, `KARE15` | 2 | 2 | 7 | 7 |
| 36, 72, 120, 196 | `LINE36..196`, `SQUARE36..196`, `KARE36..196` | 2 | 2 | 7 | 7 |
| 400 | `LINE400`, `SQUARE400`, `KARE400` | 3 | 3 | 7 | 7 |
| 15+ `*NB` | `SQUARE15NB`, `KARE36NB` ... | 0 | 0 | 0 | 0 |
| historical | `TRI`, `PRUS`, `SHER` (without `_OLD`) | 1 | 1 | 1 | 1 |
| `*_OLD` | `TRI_OLD`, `PRUS_OLD` | −10..+5 | −5..+9 | −27..+95 | −19..+80 |

`*_OLD` - these are legacy options from the time of early patches; in current
They are almost never used on rosters (a legacy from beta versions).

`*NB` - “No Bonus”: visual formation without advantages. Useful,
if you want to keep the formation for the sake of aesthetics or for an AI trigger, but
do not receive an increase in damage.
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
## 2. Where does the bonus live: `TSquad`

The entry `TSquad` (defined in `lib/classes.script`) stores four
formation bonus numeric fields - `fAddDamage` / `fAddShield` for
movement, `fAddDamageHold` / `fAddShieldHold` for holding - and
boolean flag `fHoldMode` [^8].

These fields are **taken directly** from the selected `gFormation[i]` and
are rewritten at each change of formation. That is, “the detachment has a formation
LINE15" does not mean that the script contains a line like
`squad.formationId = LINE15` - there are four numbers in `TSquad` and
name (`fSid`) for UI.

---

<a id="3-применение-бонуса-в-формуле-урона"></a>
## 3. Using the bonus in the damage formula

Source: `lib/miscext2.script:_misc_DoDamage` [^4].

The attacker and the target can both belong to a unit. Bonus
formation **shield** is added **targets**: if the defender
`fHoldMode` is enabled, `fAddShieldHold` is taken, otherwise `fAddShield`;
the total is subtracted from the damage. Bonus **damage** added
**attacker**: symmetrically via `fAddDamageHold` / `fAddDamage`,
but is added to damage.

This happens **after** subtracting `shield` and `protection[kind]`, but
before checking `damage < 1 → damage := 1`. Therefore, formational
the boost **can push a weak hit out of the "1 HP minimum"
back to operating range**.

The opposite is true: if the defender is in a hold formation (`+7 armor`),
a small blow (4-6 damage) can go to `damage < 1 → 1` - that is
reduced to a minimum of 1 HP. This is the “hold formation is tanking”
light blows."

<a id="31-числовые-примеры"></a>
### 3.1. Numerical examples

Musket 18 (damage = 14) vs infantry 18 (`shield = 1`,
`protection[bullet] = 1`):

| Target in formation | Target in hold | Damage |
|---|---|---:|
| No | — | `14 − 1 − 1 = 12` |
| `LINE15` | no | `14 − 1 − 1 − 2 = 10` |
| `LINE15` | yes | `14 − 1 − 1 − 7 = 5` |
| `SQUARE400` | yes | `14 − 1 − 1 − 7 = 5` |

Attack Musket 18 in `LINE15` (on the move) against a target outside the formation:

| Attacker in formation | Attacker in hold | Damage |
|---|---|---:|
| No | — | 12 |
| `LINE15` | no | `12 + 2 = 14` |
| `LINE15` | yes | `12 + 7 = 19` |

If both are in formations, the bonuses are summed up: `+attacker` and
`−target` are independent.

---

<a id="4-hold-mode-fholdmode--стоять-насмерть"></a>
## 4. Hold mode (`fHoldMode`) - stand to death

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
### 4.1. When is holding beneficial?

- **Defense.** Shooters in SQUARE15-hold survive a volley at `+7 armor`
  better than no formation. In numbers: 14 musket damage → 14 − 1 −
  1 − 7 = **5** versus 12 without formation.
- **Line infantry of the 18th century** `LINE` usually cheap in terms of formation costs
  (units quickly line up), so “we always keep
  hold-LINE" is a typical tactic.

<a id="42-когда-невыгоден-hold"></a>
### 4.2. When holding is not profitable

- **Cavalry attack.** If you want an instant strike, formation in
  hold will force the horses to get into line first. It's better to turn it off
hold for cavalry.
- **Pursuit.** A detachment in hold will not catch up with the retreating enemy.

---

## 5. Mask: how units are arranged in formation

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

## 6. When the formation changes

The script logic for changing the system is in `lib/squad.script` (functions with
prefix `_squad_*`). Triggers:

| Trigger | What's changing |
|---|---|
| The player pressed the “build XX” button in the UI | Immediately recalculates `gFormation[i]` for the unit. |
| The squad received reinforcements / losses | Can "move" into a smaller formation (`LINE36 → LINE15`) if there are ≤15 units left. |
| Hold mode disabled/enabled | Does not change the formation id, only `fHoldMode`. |
| The squad has been disbanded | `fSid := ''`, bonuses are nullified. |

The size of the formation is **selected automatically** according to the number of units:
if in `LINE15` 5 units died and 10 remained, `_squad_*`-function
will switch to `LINE10` (or `LINE9`, depending on the cleanup logic).

---

## 7. Creation and disbandment of `TSquad`

### 7.1. Creation

`_player_CreateSquad` assembles the system only if
`_unit_IsOfficer(officerHnd) = True` [^9]. Assembly entry point -
`_unit_MakeSquadList` [^10]: function accepts `officerHnd`, searches
around him a drummer and suitable privates, then
`_player_SetSquadFormation` places units in the grid and records
`fAddDamage / fAddShield` from `gFormation[formInd]` [^11]. Therefore
new `TSquad` with recorded bonuses appear only under
**living** officer.

After assembly `_player_SetSquadFormation` plants the officer and
drummer in cells `maskOfficers`; privates - in cells `mask`.
If at the time of re-arranging the grid there is no longer an officer in `TSquad`,
his cell remains `0`, but the fields `fAddDamage / fAddShield` are written
earlier and **do not depend on the composition of the grid**.

### 7.2. Disbandment (`disband`)

On every tick `Progress` is called for every living player
`CheckSquadsDisband` [^12]:

| Condition | What's going on |
|---|---|
| `count(non-officer) < gc_player_SquadDismissPercent × fBaseCount` | `_misc_DisbandSquad` removes `TSquad`. After this, the `if (pSquad2 ≠ nil)` branch in the damage formula is skipped, and the bonus for the remaining units is not found. |

Parameters:
- `gc_player_SquadDismissPercent = 0.25` [^13] — threshold share.
- `_squad_GetBaseUnitCount(pSquad)` is equal to
  `TSquad.GetCount − 1 − 1` (minus officer, minus drummer, if
  yes). **only privates** enter the threshold.

That is, formation bonuses disappear **not from the death of an officer**, but from
a drop in the number of rank and file below 25% of the original `fBaseCount`.

### 7.3. Hold-mode FSM (idle threshold)

Hold Multiplier (for LINE/SQUARE/KARE: `+7 dmg / +7 shield` on
sizes 15-196 and `+3/+3 → +7/+7` for 400) is active until
`TSquad.fHoldMode = True`. State machine [^14]:

| State | Transition conditions |
|---|---|
| `fHoldMode := True` | `fStandGround = True`, `fHoldMode = False`, `fAgressive = False`, `fMoveCount = 0`, and the accumulated `fHoldModeProgress` (growing at the rate of `deltatime / gc_squad_holdmode_time` per tick) reached 1.0. |
| `fHoldMode := False` | The unit receives movement order [^15]. |

Parameters: `gc_squad_holdmode_time = 150 × 8 × gc_frames_to_time =
37.5` g-sec idle time in Stand Ground [^16];
`gc_frames_to_time = 0.03125`.

That is, **“reaching the hold-bonus” takes 37.5 g-seconds**
continuous standing in Stand Ground without aggression and without movement.
As soon as you move the unit, `fHoldMode` is reset, and the accumulation
starts again.

---

<a id="7-морские-формации"></a>
## 7. Sea formations

Separate families `SHIPS`, `SHIPSN`, `LINEMORB` - for squads
ships. Bonuses are similar (or zero), but mask and others -
take into account the radius of the ship (large `gc_obj_radius_formation_default`
× 8 = 64+ pixels).

Sea battle has its own characteristics (see.
[`naval_combat.md`](naval_combat.md)).

---

<a id="8-влияние-формации-на-pathfinding"></a>
## 8. Influence of formation on pathfinding

Within one squad:
- Each unit knows its “target cell” in mask relative
  leader.
- When moving, the unit moves in a “crowd”, but when the unit stops
  occupy their cells in formation (`jittered`-movement, see
  [`pathfinding.md` §6](pathfinding.md)).
- If a unit is knocked out of the mask (for example, shot down by cavalry), the squad
  **does not expect** return - he remains in the new hole.

Between squads - different squads of the same side pass through
each other softer than scattered units, thanks
`SetGameObjectAlignmentToFlagman` - squad flag “align with
standard bearer" reduces the pushing force inside the formation.

---

<a id="9-открытые-эмпирические-вопросы"></a>
## 9. Open empirical questions

1. **Do two formation bonuses apply simultaneously** if
   the same unit falls under several formations (for example,
   18th century infantry in the formation of a regiment under the common “banner of the commander”)?
   Apparently not - `TSquad` only stores one set of bonuses.
   Confirm with measurements.
2. **Exact semantics symmetry = 3.** When a unit turns to
   180° and mask is mirrored by both axes - where does the right one go?
   flank cavalry? Need a screenshot/test in the editor.
3. **Formation switching speed.** Looks like 0.4–0.6 g-sec
   complete rearrangement, but it depends on the number of units and
   pathfinding. Measure it.

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
       suitable privates around the officer.

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
       = 37.5` g-sec.
