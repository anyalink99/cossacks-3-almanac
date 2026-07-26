# Recon: behavior of shooting units

In-depth analysis: shooter attack modes (standground, bartprepare,
RunAway), range penalty when moving, range bonus when
rest, switching weapons at a distance, bonus from high
positions. All links to the code are in [Sources](#sources).

> **Related documents:** [`combat_damage_pipeline.md`](combat_damage_pipeline.md) -
> damage formula; [`target_selection.md`](target_selection.md) —
> target selection algorithm; [`unit_commands.md`](unit_commands.md) —
> queue of orders; [`artillery_specifics.md`](artillery_specifics.md)
> - separately about artillery.

## TL;DR

- **Standground** - flag of the “stand” squad. Shooter in standground
  scans enemies to the full `searchradius` (28-45 tiles), without -
  only on ~`minsearchdist + 0.375` tiles (almost close combat).
- **Bartprepare** - flag for artillery, towers and ports: when
  upon receipt of a `attackpoint` order, it forcibly disables
  standground and activates the search for targets around the point.
- **RunAway** - the shooter retreats 3.5 tiles if the enemy enters
  its “dead zone” (`< minsearchdist`). Doesn't work in standground.
- **Standtime < 0.25 g-sec** - the shooter has just moved, loses
  up to 3 effective max-range tiles (`uniqrnd × 3`); artillery -
  up to 1.5 tiles.
- **Idle-state** adds `addradius` to range (~0.6 tiles).
- **Multi-weapon** units automatically switch weapons according to
  distances: cannon → cannonball on the far side / buckshot on the near side;
  musketeer 18th century → bullet at long range / bayonet at point blank range.
- **High ground**: on a hill (Y > 0) the shooter sees further:
  `searchdist += goHeight × 2`.

---

## 1. Standground vs normal mode

The main mechanism for determining target visibility is different
`maxsearchdist` in standground and in normal mode [^1].

In **standground** (flag `bstandground = True` plus order - not
`move`):
```
maxsearchdist = MIN(searchradius, GetMaxAttackRadius)
```
That is, the full range of the weapon (~28-45 tiles).

In **normal** mode (without standground or order `move`):
```
maxsearchdist = minsearchdist + 0.375
```
That is, **almost melee** - the shooter detects the enemy only when
he came close.

### 1.1. What does this mean in practice?

| Mode | What's going on |
|---|---|
| Standground (`hold position`) | The musketeer on the hill fires 5–10 shots before close combat. |
| Regular (`move`/`attack`) | The same musketeer manages 1-2 shots, then the enemy runs up. |
| Movement order | Erases standground: `if (order = move)` blocks the branch. |

**Defense = standground required.** Without it, shooting units
look “deaf”: they stand and do not react to the enemy in the far zone,
open fire only on 1-2 tiles.

## 2. Bartprepare - artillery mode

`bartprepare = True` - flag for artillery, towers (`tow`) and
ports (`port`). When such a unit receives an order
`attackpoint(trgx, trgz)` (by area), forced script
switches modes [^2]:

| What's changing | How |
|---|---|
| `bstandground` | forced to False |
| `bsearchenemy` | forced to True (active scanner) |
| Receives an order | `attackpoint` with delay `attackdelay`/`attackmaxdelay` |

That is, artillery in `attackpoint` mode **does not stand on one
location**, but actively scans the area around the target and fires
anyone who happens to be there.

Without `bartprepare` (mobile card shooter, musketeer) team
`attackpoint` works like `move(x, z)` - without active search.

See also [`artillery_specifics.md`](artillery_specifics.md) §3
about the order `attackpoint` and the preparation of the shot.

## 3. RunAway - the shooter’s departure from the dead zone

If a shooting unit (`minsearchdist > 0`) has an enemy enter
**dead zone** (between `0` and `minsearchdist`, that is, too
close to shoot), and the unit is **not in standground** - it retreats
on `gc_unit_runawaydist = 3.5` tile back [^3].

### 3.1. Launch conditions

All three must be true:

1. The unit is **not** in standground.
2. The enemy is in the zone `[0, minsearchdist]`.
3. Starting condition (one of):
   - `standtime = 0` (just approached / completed the shot);
   - `standtime > gc_unit_runawaydelay = 1.3` g-sec (stood
     long enough);
   - **Or** human player on easy / normal difficulty - then
     this gate is skipped.

### 3.2. Complexity and behavior

| Who's playing | Difficulty | When retreats |
|---|---|---|
| Human Player | easy/normal | Every tick until the enemy is in `minsearchdist` (indulgence for beginners). |
| Human Player | hard / very hard / impossible | Only at moments `standtime = 0` or `> 1.3` (the intermediate “manages to shoot”). |
| AI | any | Just like hard+ for a person - without concessions. |

### 3.3. Strategic Conclusions

- **Hold the hill** - `standground` is required, otherwise arrows
  will scatter when approaching.
- **Retreat tactics** (withdrawal with shelling) - **remove**
  standground; the shooter will run back 3.5 t, turn, shoot,
  will run back again.
- **Light Cavalry** catches up with retreating riflemen
  (fasthorse=96 vs default=32 - 3 times faster).

## 4. Range penalty when moving (`standtime`)

`standtime` — counter “how long the unit stands still.” When
movement is reset to 0; when it stops it starts to grow.

If `standtime < 0.25` g-sec, the shooter “shakes” - loses
effective max-range [^4]:
```
if (standtime < 0.25) AND (weapon.kind ≠ cannister):
    if (NOT bArtillery):
        radiusmax −= 3 × uniqrnd            # пехота: до −3 tiles
    else:
        radiusmax −= 3 × uniqrnd × 0.5      # артиллерия: до −1.5 tiles
```
Where is `gc_obj_maxattackradiusdisp = 3` (from `dmscript.global`), and
`uniqrnd` ∈ `[0, 1)` - the number of each fixed at spawn
unit.

### 4.1. Effect

- **A shooter in motion will not shoot at full range** —
  you need to stand for ~0.25 g-sec. This explains the “misses” in long-range
  targets when approaching.
- **Buckshot is not penalized** (`kind = cannister` is an exception).
- **Artillery is penalized 2x less** - mortar / cannon after
  short movement ready to shoot almost at full capacity.
- In combination with RunAway creates the pattern **walk away → pause 0.25 →
  shot → retreat**.

## 5. Bonus to range at rest (`addradius`)

If the unit is in idle state (`statestag` contains
`gc_statetag_move_idle`), he receives a bonus to
`weapon.radiusmax` [^5]:
```
rbonus += weapon[i].addradius     # обычно 32 px = ~0.6 tiles
```
To whom it is given: musketeers, archers, cannons - everyone
`addradius = 32 px = 0.6 t`. For weak walls
(`gc_obj_usage_weakwall`) additional **+0.36 tiles** rbonus.

### 5.1. Effect

Stationary defense (for example, a garrison on a hill in a standground)
shoots **~0.6 t further** than the same unit on the move. B
combination with high-ground (see §7) and elimination of the `standtime` penalty
This results in a noticeable increase in the defense radius.

## 6. Switching weapons by distance (multi-weapon)

Many units have **multiple weapon slots** (`weapon[0]`,
`weapon[1]`, ...). The game automatically selects the desired one
distance to the target - each weapon has
`radiusmin..radiusmax` [^6]. If the enemy is in close range -
a weapon with a small `radiusmin` is selected; otherwise - distant.

Additionally, `attmask` is taken into account: if the target has `mmask`
matches `weapon[i].attmask` (armor material), this is a weapon
priority. Therefore, **fire arrows** are chosen for
buildings (their `attmask` contains `gc_obj_material_building`).

### 6.1. Pairs of multi-weapon units

#### Cannon - cannonball against buckshot

| Slot | Type | dmg | pause | range (px) | When |
|---|---|---:|---:|---|---|
| `weapon[0]` PPOINTT | cannonball | 1800 | 350 | 550–2160 | distance ≥ 550 px (~10.3 t) |
| `weapon[1]` PSMPOINTTPUS | canister | AoE | 350 | 0–450 | enemy is closer 450 px (~8.4 t) |

Infantry that comes within ~8 tiles of a cannon is automatically hit
under **buckshot** - massive AoE damage. Therefore, “a rush of infantry on
cannon" = buckshot at point-blank range. **It’s better to attack a cannon with a stretched one
line** so that there are no more than 9 units under the explosion (see.
[`combat_damage_pipeline.md` §5](combat_damage_pipeline.md) about AoE
damage cap).

#### Musketeer 18th century. - bullet against bayonet

| Slot | Type | dmg | pause | range (px) | When |
|---|---|---:|---:|---|---|
| `weapon[0]` (bayonet) | pike | 5–10 (by nation) | **0** (no cooldown between hits) | 35–65 (~0.66–1.22 t) | point-blank |
| `weapon[1]` SHOTMUSKET | bullet | 16–29 (by nation) | 140–190 | 400–900 (~7.5–16.9 t) | further 7.5 t |

After being shot, a musketeer is **not helpless** in close combat - he has
**bayonet** with pause = 0 (beats every animation cycle). Attack
reloading musketeers with cavalry = get a bayonet fight.

Bayonet upgrades are separate from bullet upgrades
(`bla.musketeer18.1.X` increases bullet damage, bayonet remains
basic).

#### Archer - regular arrow versus fire arrow

| Slot | Type | dmg | pause | range (px) | dispersion | Features |
|---|---|---:|---:|---|---:|---|
| `weapon[0]` STRELA | arrow | 15 | 75 | 400–800 | 175 px | main shooting |
| `weapon[1]` OSTRELA | firearrow | **150** | 125 | 400–600 | 200px | `attmask` = building+wood+woodwall |

Fire Arrow Attack - **archer weapons against buildings**: damage 150
(10 times more than usual), but the rate of fire is 40% worse,
accuracy is 14% worse, and **squad damage bonus is not
applies**. The game automatically switches the archer to
OSTRELA, when the target is a building / wood / palisade.

#### Other

- **Janissary** - bullet + saber.
- **Strelets** - arquebus + reed.
- **Chasseur / dragoon** - bullet + saber.
- **Mounted archers** (drabant, mounted archer) - bullet + saber
  on horseback.

Everywhere the logic is the same: close - a melee weapon, far -
small arms

## 7. High ground - bonus from a hill

If a shooting unit is on high ground (`Y > 0`), it
**search distance** increases in proportion to the height of [^7]:
```
searchdist += goHeight × 2     # только для ranged юнитов: minsearchdist > melee_radius
```
`goHeight` — Y-coordinate of the unit in tiles. Bonus **only to radius
detection**, not to the shot itself. But if the enemy is not yet in the zone
attacks, the unit starts moving and will fire as soon as the target
will go into `radiusmax`. In practice, musketeers shoot from a hill at
advancing **earlier** = more shots before close combat.

Low Mountains are created by the `relief` parameter when generating a map
(Highlands gives the maximum).

### 7.1. Doesn't work on

- Melee units (a pikeman on a hill has no advantages
  receives - he is in close combat).
- Units with `searchradius = 0` (mortar, drummer, etc.).

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
