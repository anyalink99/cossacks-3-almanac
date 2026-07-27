<a id="recon-формации"></a>
<a id="построения-и-их-боевые-бонусы"></a>
# Formations and Their Combat Bonuses

[← How the game works](../../README.md)

This article explains which formations exist, what combat bonuses they
provide, and when Hold Position is worthwhile. The squad's internal
representation and script references are collected under
[Technical Details](#technical-details) and [Sources](#sources).

<a id="коротко"></a>
## At a Glance

- The game defines **149** formation variants: lines, squares, triangles,
  Prussian and historical arrangements, and naval formations [^1].
- Each formation defines positions for rank-and-file units and officers,
  plus one pair of bonuses while moving and another while holding.
- Bonuses are additive, not percentage: `+2` to damage = simple
  `damage += 2` after all other modifiers [^2].
- Standard 15–196-unit combat formations give **+2 damage and +2 defence**
  while moving and **+7 damage and +7 defence** after entering Hold Position.
- Attacker and defender bonuses are applied independently on every hit.
- A normal large formation holds up to 196 units; special variants hold 400.

---

<a id="1-каталог-формаций"></a>
<a id="1-какие-построения-есть"></a>
## 1. Available Formations

The game uses several formation families. Variants within one family differ
in size, unit placement, and sometimes combat bonuses. Internal family names
are included only to make the table verifiable against the game files.

<a id="11-семейства"></a>
### 1.1. Families

| Formation | Internal family | Variants | Description |
|---|---|---:|---|
| Line | `LINE` | 61 | From 3–10 units without a bonus to 15 / 36 / 72 / 120 / 196 / 400 units with bonuses. |
| Extended line | `LINEMORB` | 19 | Wide-spacing variants, including layouts for naval squads. |
| Full square | `SQUARE` | 12 | Square layouts for 15 / 36 / 72 / 120 / 196 / 400 units, including no-bonus variants. |
| Hollow square | `KARE` | 12 | Melee units around the perimeter and ranged units inside. |
| Triangle | `TRI` | 12 | A historical layout, primarily for cavalry. |
| Prussian formation | `PRUS` | 12 | Prussia's national formation family. |
| Rank | `SHER` | 12 | A historical linear arrangement. |
| Naval formations | `SHIPS`, `SHIPSN`, `PACK` | 6 | Ship formations. |
| Single unit | `ALONE`, `ODIN` | 2 | A one-unit layout. |
| No formation | `none` | 1 | The empty entry. |

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

<a id="3-применение-бонуса-в-формуле-урона"></a>
<a id="2-как-прибавки-влияют-на-урон"></a>
## 2. How Bonuses Affect Damage

The attacker and target may belong to different squads. A defence bonus
reduces damage received by the target, while a damage bonus strengthens the
attacker's hit. Moving and holding squads use different values [^4].

This happens **after** subtracting `shield` and `protection[kind]`, but
before checking `damage < 1 → damage := 1`. Therefore, formational
the boost **can push a weak hit out of the "1 HP minimum"
back to operating range**.

Conversely, if the defender holds formation (`+7` defence), a small hit
of 4–6 damage can fall below one and be clamped to the minimum of 1 HP.
Holding formation is therefore especially effective against light hits.

<a id="31-числовые-примеры"></a>
<a id="21-числовые-примеры"></a>
### 2.1. Numerical Examples

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
<a id="3-режим-стоять-насмерть"></a>
## 3. Hold Position

When the mode is active:

1. The stronger bonuses are used—usually `+7/+7` instead of `+2/+2`
   while moving.
2. Units do not lose formation because of the path of their own comrades.
3. The unit **does not move** voluntarily: even when ordered to “attack”
   The units will first deploy into formation and only then move.

Preventing units from firing without an explicit order is a separate mode.
Players often enable it together with Hold Position, but one does not imply
the other.

<a id="41-когда-выгоден-hold"></a>
<a id="41-когда-выгодно-удерживать-строй"></a>
<a id="31-когда-выгодно-удерживать-строй"></a>
### 3.1. When Holding Formation Helps

- **Defence.** Ranged units in the 15-unit square (`SQUARE15`) gain
  `+7` defence and survive a volley
  better than no formation. In numbers: 14 musket damage → 14 − 1 −
  1 − 7 = **5** versus 12 without formation.
- **18th-century line infantry.** `LINE` formations are quick to assume,
  making a held line a common defensive tactic.

<a id="42-когда-невыгоден-hold"></a>
<a id="42-когда-удержание-строя-мешает"></a>
<a id="32-когда-удержание-строя-мешает"></a>
### 3.2. When Holding Formation Gets in the Way

- **Cavalry attack.** For an immediate strike, disable hold position;
  otherwise the riders first take their assigned places.
- **Pursuit.** A squad holding position will not catch a retreating enemy.

---

<a id="5-mask-как-юниты-раскладываются-по-строю"></a>
<a id="5-схема-мест-в-строю"></a>
<a id="4-как-бойцы-располагаются-в-строю"></a>
## 4. How Units Are Placed

Each formation has one grid for rank-and-file units and another for officers.
For example, a five-unit line uses double spacing:
```
*..*..*..*..*
```
A full 36-unit square uses a 6×6 grid:
```
*.*.*.*.*.*
.*.*.*.*.*.
*.*.*.*.*.*
.*.*.*.*.*.
*.*.*.*.*.*
.*.*.*.*.*.
```
A 15-unit hollow square places melee units around the perimeter:
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

When direction changes, the grid may be mirrored horizontally, vertically,
or across both axes. The Officer, Drummer, and Standard Bearer use reserved
positions, usually central or protected by rank-and-file units.

---

<a id="6-когда-меняется-формация"></a>
<a id="5-когда-меняется-построение"></a>
## 5. When the Formation Changes

| Trigger | Result |
|---|---|
| The player selects a formation | The squad immediately receives a new placement grid and its bonuses. |
| The squad receives reinforcements or takes losses | It may switch to a larger or smaller size variant. |
| Hold Position is enabled or disabled | The formation shape stays the same; the active bonus set changes. |
| The squad is disbanded | Its formation bonuses disappear. |

Formation size is **selected automatically** from the unit count. If a
15-unit line loses five units, it changes to a ten- or nine-position line,
depending on when the formation is cleaned up.

---

<a id="7-морские-формации"></a>
<a id="8-морские-построения"></a>
<a id="6-морские-построения"></a>
## 6. Naval Formations

Separate families are intended for ships. Their combat bonuses are either
similar to land formations or zero, but their placement grids account for a
much larger ship radius—64 pixels or more.

For the ships themselves, see [How Naval Combat Works](naval_combat.md).

<a id="8-влияние-формации-на-pathfinding"></a>
<a id="8-влияние-построения-на-движение"></a>
<a id="9-влияние-построения-на-движение"></a>
<a id="7-влияние-построения-на-движение"></a>
## 7. How Formations Affect Movement

Within one squad:

- each unit knows its assigned position relative to the leader;
- the squad moves as a loose group, then units take their places with a
  small random offset after stopping; see
  [Pathfinding and Unit Movement](pathfinding.md);
- if a unit is knocked out of place, the squad does not wait for it to
  return, leaving a gap.

Squads on the same side pass through one another more gently than scattered
units. Alignment on the Standard Bearer reduces pushing within the formation.

---

<a id="technical-details"></a>
<a id="технические-подробности"></a>
<a id="8-технические-подробности"></a>
## 8. Technical Details

<a id="81-хранение-построения-и-прибавок"></a>
### 8.1. Formation and Bonus Storage

The global `gFormation[160]` array contains 149 loaded records. Each stores
`id`, `sid`, `symmetry`, the `bonusdamage` / `bonusshield` and
`bonusdamagehold` / `bonusshieldhold` pairs, grid dimensions, and the
`mask` and `maskofficers` arrays [^7].
`data/game/var/formations.cfg` is loaded at startup by
`_init_InitializeFormations` [^3].

The `TSquad` record stores `fAddDamage`, `fAddShield`, `fAddDamageHold`,
`fAddShieldHold`, and `fHoldMode` [^8]. These values come from the selected
`gFormation[i]` entry and are replaced whenever the formation changes.

The grid is limited to `gc_formation_maskmaxwidth = 54` ×
`gc_formation_maskmaxheight = 24`. `symmetry` controls mirroring:
0 means none, 1 horizontal, 2 vertical, and 3 both axes. Cell size is
`gc_obj_radius_formation_default = 8` pixels, or
`gc_obj_radius_formation_horse = 12` for cavalry [^5].

<a id="7-создание-и-расформирование-tsquad"></a>
<a id="82-создание-и-расформирование-отряда"></a>
### 8.2. Creating and Disbanding a Squad

<a id="71-создание"></a>
<a id="создание"></a>
#### Creation

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
<a id="расформирование"></a>
#### Disbanding

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
<a id="переход-в-режим-удержания-после-простоя"></a>
#### Entering Hold Position After an Idle Period

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

<a id="9-открытые-эмпирические-вопросы"></a>
<a id="10-что-ещё-требует-проверки"></a>
<a id="9-что-ещё-требует-проверки"></a>
## 9. Questions Requiring Further Testing

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
