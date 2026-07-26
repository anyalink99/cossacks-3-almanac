#02. Combat and movement

[← Index](README.md)

<a id="о-чём-эта-глава"></a>
## What is this chapter about?

Summary **tables** for combat and movement: types of weapons, unit speeds,
counter-effectiveness matrix, cross-tabulation “upgrades ×
characteristics", cost of one shot. Numbers extracted from
scripts and generated automatically from [`data.json`](../../../data.json).

**Detailed analysis of mechanics** - in `recon/world/combat/`:

- [combat_damage_pipeline.md](../../recon/world/combat/combat_damage_pipeline.md)
  — damage pipeline: 6 steps of the formula, headshot, AoE cap, friendly
  fire, peace-mode, simplification.
- [formations.md](../../recon/world/combat/formations.md) - LINE /
  SQUARE / KARE: 149 formations, formation bonuses, hold-mode FSM, threshold
  disbandment.
- [ranged_units_behavior.md](../../recon/world/combat/ranged_units_behavior.md)
  — shooter behavior: standground, bartprepare, RunAway, penalty to
  range when moving, multi-weapon, high ground.
- [target_selection.md](../../recon/world/combat/target_selection.md)
  — target selection algorithm via scan-grid, attack-move, treatment
  priests, the squad's reaction to a strike, the dispersion of shots.
- [unit_commands.md](../../recon/world/combat/unit_commands.md) —
  queue of orders, attack modes, hold-fire, rally points.
- [vision_and_fow.md](../../recon/world/combat/vision_and_fow.md) —
  fog of war and viewing radius formula `20 + 4 × vision`.
- [pathfinding.md](../../recon/world/combat/pathfinding.md) —
  movement and push.
- [artillery_specifics.md](../../recon/world/combat/artillery_specifics.md)
  — artillery: `bartprepare`, `attackpoint`, limits through the art depot.
- [towers.md](../../recon/world/combat/towers.md)
  - towers and garrison.
- [naval_combat.md](../../recon/world/combat/naval_combat.md) —
  sea battle.
- [walls_and_gates.md](../../recon/world/combat/walls_and_gates.md)
  - walls and gates.

<a id="типы-оружия-gcobjweaponkind"></a>
## Weapon types (`gc_obj_weapon_kind_*`)

| Kind | Description | Media |
|---|---|---|
| `pike` | Long Spear/Pike | Pikemen 17th/18th century. |
| `sword` | Sword/saber | Light infantry, swordsmen, cavalry in close combat |
| `bullet` | Gunshot bullet | Musketeer, archer, janissary, dragoon, etc. |
| `arrow` | Boom/bolt | Archer (`SHOTLU`-ammo) |
| `cannonball` | Cannonball | Cannon, tower, frigate (single shot) |
| `cannister` | Buckshot | Cannon melee, multi-barreled gun |

Each `kind` has its own `protection[kind]` column for targets. See
damage formula in
[`recon/world/combat/combat_damage_pipeline.md` §2](../../recon/world/combat/combat_damage_pipeline.md).

Details - in
[`recon/world/combat/combat_damage_pipeline.md`](../../recon/world/combat/combat_damage_pipeline.md)
and [`ranged_units_behavior.md`](../../recon/world/combat/ranged_units_behavior.md).

<a id="uniqrnd--индивидуальное-случайное-число-юнита"></a>
## `uniqrnd` - individual random unit number

When spawning, each unit receives `uniqrnd ∈ [0, 1)` - fixed
a random number that remains unchanged until death (see
[`internals/engine/rng_implementation.md`](../../../internals_en/engine/rng_implementation.md)).
Used in **four** mechanics simultaneously:

| # | Where is it used | Effect |
|---:|---|---|
| 1 | Headshot Bonus | `+floor(uniqrnd × 500)` extra damage on crit |
| 2 | Effective max-range | `radiusmax −= uniqrnd × 3` tile during `standtime < 0.25` g-sec |
| 3 | Search timing | `nextSearch = now + uniqrnd × 0.15 + 0.3` sec - units do not scan synchronously |
| 4 | Multiplayer sync seed | `SetRandomKey(floor(uniqrnd × MaxInt))` for synchronizing solutions between clients |

Details - in
[`recon/world/combat/combat_damage_pipeline.md`](../../recon/world/combat/combat_damage_pipeline.md)
and [`ranged_units_behavior.md`](../../recon/world/combat/ranged_units_behavior.md).
<a id="скорости-юнитов"></a>
## Unit speeds

Basic `gc_obj_speed_*` from `dmscript.global:603-620`. **Abstract units** (not tiles/sec). The actual speed in tiles/sec depends on animation `walkInterval`, `walkintervalfactor` and game speed. Translation requires empirical measurement.

| Class | Speed ​​| Note |
|---|---:|---|
| default | 32 | infantry, artillery and many default units |
| peasant | 40 | peasant - faster than ordinary infantry |
| hardhorse | 56 | heavy cavalry (Reiter, Cuirassier, Vityaz) |
| fasthorse | 96 | light cavalry (Hussar, Lancer, Cossack) - the fastest |
| cannon | 20 | gun - slow |
| mortar | 24 | mortar - a little faster than a cannon |
| howitzer | 20 |  |
| multicannon | 16 |  |
| fishboat | 16 | fishing boat |
| ferry | 28 | ferry (transport) |
| yacht | 40 | yacht (shooting ship) |
| yachttur | 70 | Turkish yacht (faster than standard) |
| chaika | 55 | Ukrainian seagull - mobile |
| galley | 40 |  |
| frigate | 30 | frigate |
| xebec | 28 |  |
| battleship | 16 | battleship - the slowest warship |

**Law:** relative values. fasthorse(96) ≈ ×3 from cannon(20). peasant(40) in the middle. The slowest are battleship/multicannon (16).

<a id="офицеры-и-формации"></a>
## Officers and formations

Each nation has N groups of officers. One officer leads the **formation** of certain units (usually infantry/cavalry of the same class). Formations are standard for everyone:

**LINE / SQUARE / KARE × 15 / 36 / 72 / 120 / 196 / 400 units.**

The larger the formation, the stronger the bonuses (attack, defense, morale).

Full tables of officers → sections in [nations/](../nations/README.md) for each nation.

<a id="матрица-контр-эффективности-приближённый-ttk"></a>
## Counter-effectiveness matrix (approximate TTK)

For each pair (attacking class, defending class) - **approximate time to kill** (time-to-kill, TTK) in **game seconds** at 1v1, excluding formations, movement, misses and shield bonuses of units.

Calculation: for the attacker we take **representative class unit** (median in damage); for a defender - median by HP. The damage formula applies:
```
applied = max(1, weapon.dmg - target.shield - target.protection[weapon.kind])
DPS = applied / weapon.pause_sec
TTK = target.HP / DPS
```
⚠ The numbers are approximate. The actual TTK will be higher due to: road to target, shot preparation (`bartprepare`), formation bonuses (squad shield, LINE/SQUARE/KARE formation), movement penalty to accuracy, fast-cavalry headshot bonus.

**Median class representatives** (used for calculation):

| Class | Representational Attacker | damage | recharge (s) | type | Representative Defender | HP | shield |
|---|---|---:|---:|---|---|---:|---:|
| Peasant | `peatur` (Peasant) | 20 | 0.5625 | sword | `peatur` (Peasant) | 50 | 0 |
| Pikemen 17c | `pikeman` (Pikeman, 17th century) | 8 | 0.4688 | pike | `pikeman` (Pikeman, 17th century) | 90 | 0 |
| Pikemen 18c | `pikeman18` (Pikeman, 18th century) | 9 | 0.2812 | pike | `pikeman18` (Pikeman, 18th century) | 85 | 0 |
| Light Infantry | `roundshierdip` (Roundshier (mercenary)) | 6 | 0.4688 | sword | `roundshierdip` (Roundshier (mercenary)) | 75 | 0 |
| Musketeers 17c | `musketeer` (Musketeer, 17th century) | 12 | 4.69 | bullet | `musketeer` (Musketeer, 17th century) | 70 | 0 |
| Musketeers 18c | `musketeer18` (Musketeer, 18th century) | 16 | 4.69 | bullet | `musketeer18pru` (Musketeer, 18th century) | 100 | 0 |
| Grenadiers | `grenadierdip` (Grenadier (mercenary)) | 16 | 4.69 | bullet | `grenadierdip` (Grenadier (mercenary)) | 30 | 0 |
| Archers | `archerturdip` (Turkish archer (mercenary)) | 100 | 0.78 | firearrow | `archerdip` (Archer (mercenary)) | 20 | 0 |
| Light Cavalry | `lightcavalrydip` (Light cavalry (mercenary)) | 18 | 2.25 | bullet | `lightcavalry` (Light cavalry) | 175 | 0 |
| Dragoons | `dragoon18dip` (Dragoon, 18th century (mercenary)) | 18 | 2.25 | bullet | `dragoon` (Dragoon, 17th century) | 220 | 0 |
| Heavy Cavalry | `wingedhussar` (Winged Hussar) | 14 | 0.375 | pike | `cuirassier` (Cuirassier) | 300 | 0 |
| Cannons | `cannon` (Cannon) | 1800 | 10.94 | cannonball | `cannon` (Cannon) | 9000 | 75 |
| Mortars | `howitzer` (Howitzer) | 4000 | 18.75 | cannonball | `howitzer` (Howitzer) | 3000 | 75 |

<a id="матрица-контр-эффективности--ttk-в-g-сек"></a>
### Counter-effectiveness matrix - TTK in g-sec

Strings = **attacker**. Columns = **defending**. Cell = TTK (game-sec). Green/low = attacker kills quickly; red/high = defender stands for a long time.

| Atk\Def | Pea | Pik17 | Pik18 | LtInf | Mus17 ​​| Mus18 | Green | Arch | LtCav | Drag | HvCav | CNN | Mor |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Pea** (Peasant) | 1.4 | 2.8 | 2.4 | 2.5 | 2.0 | 2.8 | **0.8** | **0.6** | 4.9 | 6.2 | 11 | _5062_ | _1688_ |
| **Pik17** (Pikemen 17c) | 2.9 | 8.4 | 5.0 | 12 | 4.1 | 5.9 | 1.8 | 1.2 | 10 | 13 | 23 | _4219_ | _1406_ |
| **Pik18** (Pikemen 18c) | 1.6 | 4.2 | 2.7 | 5.3 | 2.2 | 3.1 | **0.9** | **0.6** | 5.5 | 6.9 | 12 | _2531_ | _844_ |
| **LtInf** (Light Infantry) | 3.9 | 11 | 6.6 | 12 | 5.5 | 7.8 | 2.3 | 1.6 | 14 | 17 | 70 | _4219_ | _1406_ |
| **Mus17** (Musketeers 17c) | 20 | 53 | 33 | 88 | 27 | 39 | 12 | 7.8 | 68 | 86 | _704_ | _42210_ | _14070_ |
| **Mus18** (Musketeers 18c) | 15 | 35 | 25 | 44 | 21 | 29 | 8.8 | 5.9 | 51 | 64 | _235_ | _42210_ | _14070_ |
| **Gren** (Grenadiers) | 15 | 35 | 25 | 44 | 21 | 29 | 8.8 | 5.9 | 51 | 64 | _235_ | _42210_ | _14070_ |
| **Arch** (Archers) | **0.4** | **0.7** | **0.7** | **0.6** | **0.5** | **0.8** | **0.2** | **0.2** | 1.4 | 1.7 | 2.3 | _281_ | 94 |
| **LtCav** (Light Cavalry) | 6.2 | 14 | 11 | 17 | 8.8 | 12 | 3.8 | 2.5 | 22 | 28 | 84 | _20250_ | _6750_ |
| **Drag** (Dragoons) | 6.2 | 14 | 11 | 17 | 8.8 | 12 | 3.8 | 2.5 | 22 | 28 | 84 | _20250_ | _6750_ |
| **HvCav** (Heavy Cavalry) | 1.3 | 3.1 | 2.3 | 3.1 | 1.9 | 2.7 | **0.8** | **0.5** | 4.7 | 5.9 | 9.4 | _3375_ | _1125_ |
| **Cnn** (Cannons) | **0.3** | **0.6** | **0.5** | **0.5** | **0.4** | **0.6** | **0.2** | **0.1** | 1.1 | 1.3 | 1.9 | 57 | 19 |
| **Mor** (Mortars) | **0.2** | **0.4** | **0.4** | **0.4** | **0.3** | **0.5** | **0.1** | **0.1** | **0.8** | 1.0 | 1.4 | 43 | 14 |

**Reading:** bold means a quick kill (TTK <1 sec); italics means almost no damage (TTK >100 sec).

<a id="матрица-контр-эффективности-с-поправкой-на-промахи-пулистрелы"></a>
### Counter-effectiveness matrix adjusted for misses (bullets/arrows)

For bullet/arrow attackers, the TTK is higher due to **scatter**: at a distance of 15 t, the musketeer hits only ~33% of shots (see section Scatter). Here TTK is multiplied by the miss rate:
```
hit_chance(dist) = min(1.0, 1 / (2 × maxdisp))
                 = min(1.0, 1 / (2 × dist × disp × 0.0267))
real_TTK = ideal_TTK / hit_chance
```
I count at a distance of 12 t (typical range of shooters), with base dispersion = 200 px/3.75 t. For close combat (cannon/mortar in close combat?) the distance is 6 t as a fallback value. Below is the relative TTK for shooters (lines only: Mus17, Mus18, Arch, Drag, LtCav (if shooting)):

| Atk\Def | Pea | Pik17 | LtInf | Mus17 ​​| Green | Arch | LtCav | HvCav |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **Mus17** (Musketeers 17c, hit≈41%) | 47 | _127_ | _211_ | _66_ | 28 | 19 | _164_ | _1691_ |
| **Mus18** (Musketeers 18c, hit≈41%) | 35 | _85_ | _106_ | 49 | 21 | 14 | _123_ | _564_ |
| **Gren** (Grenadiers, hit≈41%) | 35 | _85_ | _106_ | 49 | 21 | 14 | _123_ | _564_ |
| **Arch** (Archers, hit≈100%) | 0.4 | 0.7 | 0.6 | 0.5 | 0.2 | 0.2 | 1.4 | 2.3 |
| **LtCav** (Light Cavalry, hit≈41%) | 15 | 35 | 41 | 21 | 9 | 6 | 53 | _203_ |
| **Drag** (Dragoons, hit≈41%) | 15 | 35 | 41 | 21 | 9 | 6 | 53 | _203_ |

**What has been added** regarding the ideal TTK:
- Shooters at a distance of 12 t **hit ~50%** of shots → TTK ×2.
- Archer and with disp 175 px (a little better) - hit a little more often.
- At a long distance (15-17 t for a musket) - TTK another +30-50%.
- In **hold-mode formation** damage +7 (from 6 to 13) → TTK drops by ~2 times. Taking into account misses, the formation compensates for the scattering approximately just right.
- **On the hill** the musketeers start shooting 2-4 t further → +1-2 shots before the enemy approaches. Effective TTK is reduced by ~10-30% due to extra salvos.

**Examples of conclusions** (based on standard protection data):
- **Cannons / mortars** against infantry - TTK <1 (complete kill with one shot per shot).
- **Pikemen** vs heavy cavalry - TTK is high because cavalry has prot_pike. But in a formation, a pikeman gives significantly more DPS.
- **Musketeers** against infantry with prot_bullet=4-6 - TTK ~10-15 sec, realistic.
- **Light cavalry** against cannons - low TTK (cannon without armor, easy to kill).

<a id="перекрёстная-таблица-апгрейды--характеристики"></a>
## Cross table: upgrades × characteristics

Which upgrade affects what. Summary of `itype` (deciphered in [chapter “Upgrades”](../05_upgrades/README.md)). Prices are given for the base nation (varies by nation - see [chapter “Upgrades”](../05_upgrades/README.md)).

**Notation Hints:** `aca.X` = academy.X, `bla.<unit>.1.X` = X-level blacksmith damage for the unit. `mil.X` = mill.X. The names are from the locale (en).

<a id="глобальные-апгрейды-academy-mill"></a>
### Global upgrades (academy, mill)

| Upgrade | Effect | val | Cost (F/W/S/G/I/C) | What improves |
|---|---|---:|---|---|
| `aca.1` (Academy) | **+food eff %** | 40 | F0/W200/S0/G325/I0/C0 | Cultivate new cultures of wheat (harvesting +40%) |
| `aca.2` (Academy) | **+food eff %** | 50 | F0/W2400/S0/G625/I0/C0 | Cultivate new cultures of rye (harvesting +50%) |
| `aca.3` (Academy) | **+food eff %** | 50 | F0/W3600/S0/G850/I0/C0 | Raise agriculturists' salary (harvesting +50%) |
| `aca.4` (Academy) | **+field HP %** | 200 | F0/W1000/S0/G475/I0/C0 | Carry out field melioration (field capacity +200%) |
| `aca.5` (Academy) | **+fish eff %** | 100 | F0/W12400/S0/G2520/I0/C0 | Design new tackle and fishing nets (boat efficiency +100%) |
| `aca.6` (Academy) | **enable unit** | 0 | F0/W12400/S0/G7040/I0/C0 | Develop new woodworking methods (frigate building) |
| `aca.7` (Academy) | **price%** | 0 | F0/W7300/S0/G1220/I0/C0 | Build new shipyards for fishing boats (fishing boat cost -85 |
| `aca.8` (Academy) | **+wood eff %** | 100 | F5500/W0/S0/G550/I0/C0 | Design new woodworking tools (woodcutting efficiency +100%) |
| `aca.9` (Academy) | **+shield** | 85 | F0/W9400/S7850/G1150/I0/C0 | Use new construction materials (durability of buildings +85) |
| `aca.10` (Academy) | **build time %** | -7500000 | F0/W0/S0/G6950/I0/C0 | Raise builders' salary (building construction time -75%) |
| `aca.11` (Academy) | **+shield** | 80 | F0/W0/S16200/G1500/I0/C0 | Research new fortification grades (durability of walls and t |
| `aca.12` (Academy) | **+damage %** | 10 | F0/W0/S0/G0/I5000/C0 | Improve firearms: rifled barrel (fire power +10%) |
| `aca.13` (Academy) | **+damage %** | 10 | F0/W0/S0/G4000/I0/C0 | Research granular gunpowder (fire power +10%) |
| `aca.14` (Academy) | **+damage %** | 15 | F0/W0/S0/G7000/I0/C0 | Research new sulfur purification methods (fire power +15%) |
| `aca.15` (Academy) | **+damage %** | 25 | F0/W0/S0/G0/I0/C11000 | Research new nitre purification methods (fire power +25%) |
| `aca.16` (Academy) | **range %** | 5 | F0/W0/S0/G2000/I12150/C0 | Research improved additions to gunpowder formula (artillery |
| `aca.17` (Academy) | **range %** | 10 | F0/W0/S3000/G4550/I19200/C0 | Design new barrel types: unicorn, carronade (artillery range |
| `aca.18` (Academy) | **HP %** | 50 | F0/W0/S0/G500/I3830/C1500 | Design more durable gun carriage: Gribovalle system (artille |
| `aca.19` (Academy) | **enable unit** | 0 | F0/W0/S0/G1500/I0/C2500 | Design multi-barrel cannon |
| `aca.20` (Academy) | **accuracy %** | -35 | F0/W3540/S0/G2000/I0/C7250 | Research new sighting devices for artillery (artillery accur |
| `aca.21` (Academy) | **healing** | 25 | F0/W350/S0/G100/I0/C250 | Finance artillery repair shops (repair all artillery) |
| `aca.22` (Academy) | **geology** | 0 | F0/W0/S0/G250/I0/C0 | Develop geology (previously hidden deposits appear on the ma |
| `aca.23` (Academy) | **+stone eff %** | 100 | F0/W0/S0/G1550/I3000/C0 | Develop mining (stone excavation efficiency +100%) |
| `aca.24` (Academy) | **+stone eff %** | 200 | F4200/W0/S0/G1550/I0/C12520 | Raise miners' salary (stone excavation efficiency +200%) |
| `aca.25` (Academy) | **balloon** | 0 | F0/W0/S0/G5750/I0/C0 | Design Montgolfier (reveals the whole map) |
| `aca.26` (Academy) | **healing** | 50 | F0/W0/S0/G200/I0/C200 | Develop medical science (heals all living units) |
| `aca.27` (Academy) | **accuracy %** | -35 | F0/W9540/S0/G12000/I0/C65200 | Develop mathematics (artillery accuracy +35%) |
| `aca.28` (Academy) | **speed %** | 40 | F0/W65400/S0/G24050/I0/C0 | Design new rigging types (ship speed +40%) |
| `aca.29` (Academy) | **enable unit** | 0 | F0/W32300/S0/G6800/I9000/C12800 | Design new rib system and new hulls (battleship construction |
| `aca.30` (Academy) | **build time %** | -5000000 | F0/W2300/S42700/G1150/I0/C0 | Train carpenters (shipbuilding speed x10) |
| `aca.31` (Academy) | **reload %** | -30 | F0/W0/S6000/G5500/I4200/C0 | Design wheellock (rate of fire +30%) |
| `aca.32` (Academy) | **price%** | 0 | F0/W0/S0/G6050/I0/C7750 | Design flintlock (musket cost -50%) |
| `aca.33` (Academy) | **reload %** | -30 | F0/W5000/S0/G5500/I0/C15200 | Design paper cartridge and iron ramrod (rate of fire +30%) |
| `aca.34` (Academy) | **+shield** | 2 | F0/W0/S0/G9750/I0/C0 | Research improved steel grades for cuirasses (armoured soldi |
| `aca.35` (Academy) | **+damage** | 5 | F0/W0/S0/G11500/I0/C0 | Design bayonet: barrel-inserted, bayonet with a tube (cold s |
| `aca.36` (Academy) | **+damage %** | 25 | F0/W0/S0/G19500/I0/C0 | Research new steel grades (18c musketeer/grenadier melee att |

**Stack of upgrades by effects** (cumulative):
- **+food extraction**: `mil.1` (+140%? note: mill upgrade values ​​vary) + `aca.1` (+40%) + `aca.2` (+50%) + `aca.3` (+50%). Eff can reach 100+140+40+50+50 = **380%**.
- **+wood extraction**: `aca.8` (+100%). Doubles wood/trip.
- **+stone extraction**: `aca.23` (+100%) + `aca.24` (+200%). Up to 100+100+200 = **400% eff**.
- **+fishing**: `aca.5` (+100%). Doubles `fishingmax` boats → 1000→2000.
- **+field HP** (`fieldlife`): `aca.4` (+200) + `bla.1` (+100). Changes field damage from 100/hit to 25/hit → +4× food per field.
- **+firearm damage %**: `aca.12` (+10) + `aca.13` (+10) + `aca.14` (+15) + `aca.15` (+25) = **+60% damage** for all bullet/arrow units.
- **+artillery range %**: `aca.16` (+5) + `aca.17` (+10) = **+15% range**.
- **+artillery accuracy %**: `aca.20` (-35%) + `aca.27` (-35%) = **-70% dispersion** (almost accurate shots).
- **+artillery durability %**: `aca.18` (+50%).
- **+firearm reload %**: `aca.31` (-30%) + `aca.33` (-30%) = **-60% reload** (fire rate +250%). Applies to **ALL shooters with bullet weapons** - musketeers, archers, janissaries, dragoons, etc. (via `garr_UnitsShooters` / `garr_UnitsBayonet`), not just artillery.
- **+building shield**: `aca.9` (+85, all buildings) + `aca.11` (+80, walls/towers).
- **+building speed**: `aca.10` (-75% buildtime).
- **+ship speed**: `aca.28` (+40%).
- **One-time effects**: `aca.21` (heals artillery), `aca.22` (geology - opens mines), `aca.25` (Hot Air Balloon - opens map), `aca.26` (heals all units), `aca.30` (×10 construction speed ships), `aca.32` (-50% cost of muskets).
- **Unlock units**: `aca.6` (frigate), `aca.19` (multi-barrel cannon), `aca.29` (battleship).

<a id="поюнитные-апгрейды-blacksmith--barracks--stable"></a>
### Unit upgrades (blacksmith / barracks / stable)

Blacksmith (`bla`), barracks (`bar`/`ba2`), stable (`sta`) contain **unit damage and defense upgrades** (5 levels + special 7th level). Format sid: `<nat><place>.<unit>.<itype>.<level>` where itype=1 (damage) or 2 (protection).

Full stack example for **rusbar.pikemanrus** (Russian Spearman):
- 5 levels of damage (`.1.1` … `.1.5`): +1, +2, +2, +1, +2 = **+8 damage**
- 5 levels of protection (`.2.1` … `.2.5`): +1, +1, +2, +1, +1 = **+6 to protection** (pike, sword, arrow)
- Level 7 unique (`.1.6` / `.2.6`): +2 damage / +2 defense (override for rus)
- **Full stack: +10 damage / +8 defense** on a fully upgraded Russian pikeman.

The full list is in the [chapter “Upgrades”](../05_upgrades/README.md) (~4500 lines, by location).

<a id="стоимость-одного-выстрела"></a>
## Cost of one shot

Many gun units, towers and ships cost `iron` / `coal` / `gold` for each shot (regardless of the cost of building the unit itself). This is a separate tax, in addition to `consume[gold]` and `food upkeep`.

Rows are grouped by `(sid, weapon)`: if the values ​​are the same for all nations, shown in one row with `nation = all`. If a nation has its own meaning, it is in a separate line.

| Unit | Nations | weapon | damage | recharge (s) | shots/min | iron / shot | coal/shot | gold/shot |
|---|---|---|---:|---:|---:|---:|---:|---:|
| **Archer** `archer` | alg | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| **Archer** `archer` | alg | `STRELA` | 15 | 2.34 | 25.6 | — | — | — |
| **Archer (mercenary)** `archerdip` | all | `OSTRELA` | 100 | 0.78 | 76.9 | — | — | — |
| **Archer (mercenary)** `archerdip` | all | `STRELA` | 25 | 2.5 | 24.0 | — | — | — |
| **Bow Clansman** `archersco` | sco | `OSTRELA` | 150 | 4.38 | 13.7 | — | — | — |
| **Bow Clansman** `archersco` | sco | `STRELA` | 20 | 3.12 | 19.2 | — | — | — |
| **Turkish archer** `archertur` | tur | `OSTRELA` | 150 | 4.38 | 13.7 | — | — | — |
| **Turkish archer** `archertur` | tur | `STRELA` | 20 | 2.66 | 22.6 | — | — | — |
| **Turkish archer (mercenary)** `archerturdip` | all | `OSTRELA` | 100 | 0.78 | 76.9 | — | — | — |
| **Turkish archer (mercenary)** `archerturdip` | all | `STRELA` | 25 | 2.5 | 24.0 | — | — | — |
| **Ship of the Line** `battleship` | all | `PPOINTTKOR` | 1800 | 0.62 | 96.8 | 5 | 15 | — |
| **Cannon** `cannon` | all | `PPOINTT` | 1800 | 10.94 | 5.5 | 20 | 40 | — |
| **Cannon** `cannon` | all | `PSMPOINTTPUS` | 0 | 10.94 | 5.5 | 24 | 21 | — |
| `chaika` | ukr | `PPOINTTKOR` | 1000 | 2.34 | 25.6 | 4 | 9 | — |
| **Chasseur** `chasseur` | fra | `SHOTMUSKET` | 20 | 5.94 | 10.1 | 4 | 8 | — |
| **Dragoon, 17th century** `dragoon` | aus, bav, den, eng, fra, hun, net, pie, pol, por, pru, sax, spa, swe, swi, ven | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| **Dragoon, 18th century** `dragoon18` | aus, bav, den, eng, pol, por, pru, rus, sax, spa, swe, swi, ven | `SHOTMUSKET` | 19 | 5.31 | 11.3 | 4 | 5 | — |
| **Dragoon, 18th century (mercenary)** `dragoon18dip` | all | `SHOTMUSKET` | 18 | 2.25 | 26.7 | 5 | 8 | — |
| **Dragoon, 18th century** `dragoon18fra` | fra | `SHOTMUSKET` | 10 | 4.69 | 12.8 | 3 | 3 | — |
| **Dragoon, 18th century** `dragoon18net` | net | `SHOTMUSKET` | 17 | 5.0 | 12.0 | 3 | 4 | — |
| **Dragoon, 18th century** `dragoon18pie` | pie | `SHOTMUSKET` | 19 | 5.0 | 12.0 | 4 | 5 | — |
| **Pospolite ruszenie** `dragoonpol` | pol | `SHOTMUSKET` | 13 | 5.0 | 12.0 | 2 | 3 | — |
| **Tower** `eurtow` | aus, bav, den, eng, fra, hun, net, pie, pol, por, pru, sax, sco, spa, swe, swi, ven | `cannonball` | 1000 | 12.5 | 4.8 | 10 | 30 | — |
| **Frame gun** `framegun` | sco | `PPOINTTFRAME` | 500 | 2.81 | 21.4 | 30 | 40 | — |
| **Frigate** `frigate` | all | `PPOINTTKOR` | 1800 | 2.34 | 25.6 | 25 | 35 | — |
| **Galley** `galley` | all | `DIMMORT2KOR` | 1000 | 1.56 | 38.5 | 4 | 9 | — |
| **Galley** `galley` | all | `PPOINTTKOR` | 100 | 4.69 | 12.8 | 4 | 9 | — |
| **Hajduk** `gauduk` | hun | `SHOTMUSKET` | 9 | 3.12 | 19.2 | 1 | 2 | — |
| **Grenadier** `grenadier` | aus, eng, fra, net, pie, pol, por, pru, rus, spa, swe, swi, ven | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| **Grenadier** `grenadierbav` | bav | `SHOTMUSKET` | 19 | 5.31 | 11.3 | 3 | 3 | — |
| **Grenadier** `grenadierden` | den | `SHOTMUSKET` | 19 | 5.94 | 10.1 | 3 | 3 | — |
| **Grenadier (mercenary)** `grenadierdip` | all | `SHOTMUSKET` | 16 | 4.69 | 12.8 | 2 | 5 | — |
| **Grenadier** `grenadierhun` | hun | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| **Grenadier** `grenadierpru` | pru | `SHOTMUSKET` | 16 | 4.38 | 13.7 | 2 | 3 | — |
| **Grenadier** `grenadiersax` | sax | `SHOTMUSKET` | 19 | 5.31 | 11.3 | 3 | 3 | — |
| **Highlander** `highlander` | eng | `SHOTMUSKET` | 16 | 5.0 | 12.0 | 3 | 4 | — |
| **Howitzer** `howitzer` | all | `DIMMORT1` | 4000 | 18.75 | 3.2 | 20 | 100 | — |
| **Volunteer** `jagerpor` | por | `SHOTMUSKET` | 10 | 5.94 | 10.1 | 2 | 4 | — |
| **Chasseur** `jagerswi` | swi | `SHOTMUSKET` | 20 | 6.88 | 8.7 | 4 | 9 | — |
| **Janissary** `jannisary` | tur | `SHOTMUSKET` | 12 | 4.69 | 12.8 | 3 | 5 | — |
| **King's Musketeer** `kingmusketeer` | fra | `SHOTMUSKET` | 43 | 6.88 | 8.7 | 6 | 10 | — |
| **Light cavalry** `lightcavalry` | hun | `SHOTMUSKET` | 14 | 5.31 | 11.3 | 2 | 3 | — |
| **Light cavalry (mercenary)** `lightcavalrydip` | all | `SHOTMUSKET` | 18 | 2.25 | 26.7 | 5 | 8 | — |
| **Bombard** `mortar` | all | `DIMMORT2` | 200 | 7.81 | 7.7 | 20 | 30 | — |
| **Multi-barrelled Cannon** `multicannon` | aus, bav, den, eng, fra, hun, net, pie, pol, por, pru, rus, sax, spa, swe, swi, ven | `PSMPOINTT` | 500 | 1.88 | 31.9 | 40 | 30 | — |
| **Musketeer, 17th century** `musketeer` | bav, den, eng, fra, pie, por, pru, sax, swe, swi, ven | `SHOTMUSKET` | 12 | 4.69 | 12.8 | 2 | 4 | — |
| **Musketeer, 18th century** `musketeer18` | aus, eng, fra, hun, net, pie, pol, por, rus, spa, swe, swi, ven | `SHOTMUSKET` | 16 | 4.69 | 12.8 | 2 | 3 | — |
| **Musketeer, 18th century** `musketeer18bav` | bav | `SHOTMUSKET` | 22 | 5.94 | 10.1 | 3 | 4 | — |
| **Musketeer, 18th century** `musketeer18den` | den | `SHOTMUSKET` | 29 | 5.94 | 10.1 | 4 | 5 | — |
| **Musketeer, 18th century** `musketeer18pru` | pru | `SHOTMUSKET` | 22 | 4.69 | 12.8 | 3 | 4 | — |
| **Musketeer, 18th century** `musketeer18sax` | sax | `SHOTMUSKET` | 19 | 4.38 | 13.7 | 3 | 3 | — |
| **Musketeer, 17th century** `musketeeraus` | aus | `SHOTMUSKET` | 12 | 5.0 | 12.0 | 2 | 4 | — |
| **Musketeer, 17th century** `musketeernet` | net | `SHOTMUSKET` | 10 | 3.75 | 16.0 | 1 | 3 | — |
| **Musketeer, 17th century** `musketeerpol` | pol | `SHOTMUSKET` | 9 | 3.12 | 19.2 | 1 | 2 | — |
| **Covenanter musketeer** `musketeersco` | sco | `SHOTMUSKET` | 12 | 4.69 | 12.8 | 2 | 5 | — |
| **Musketeer, 17th century** `musketeerspa` | spa | `SHOTMUSKET` | 15 | 5.94 | 10.1 | 3 | 6 | — |
| **Pandur** `pandur` | aus | `SHOTMUSKET` | 17 | 4.69 | 12.8 | 3 | 6 | — |
| **Szekely** `pandurhun` | hun | `SHOTMUSKET` | 19 | 5.0 | 12.0 | 3 | 7 | — |
| **Shipyard** `porpor` | por | `cannonball` | 1000 | 8.75 | 6.9 | 10 | 30 | — |
| **Tower** `rustow` | rus | `cannonball` | 1000 | 9.38 | 6.4 | 10 | 30 | — |
| **Serdiuk** `serdiuk` | ukr | `SHOTMUSKET` | 12 | 4.06 | 14.8 | 3 | 6 | — |
| **Strelets** `strelet` | rus | `SHOTMUSKET` | 12 | 4.69 | 12.8 | 2 | 4 | — |
| **Tatar** `tatar` | tur | `STRELA` | 15 | 1.56 | 38.5 | — | — | — |
| **Tower** `turtow` | alg, tur | `cannonball` | 1200 | 15.62 | 3.8 | 15 | 40 | — |
| **Xebec** `xebec` | alg, tur | `PPOINTTKOR` | 1800 | 1.56 | 38.5 | 25 | 35 | — |
| **Yacht** `yacht` | all | `PPOINTTKOR` | 1000 | 10.94 | 5.5 | 4 | 9 | — |
| **Yacht** `yachttur` | tur | `PPOINTTKOR` | 30 | 12.5 | 4.8 | 5 | 15 | — |
| **Yacht** `yachttur` | tur | `PPOINTTKOR` | 0 | 21.88 | 2.7 | 5 | 15 | — |