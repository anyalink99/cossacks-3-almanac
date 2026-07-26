<a id="cossacks-3--скорость-атаки-per-unit"></a>
<a id="скорость-атаки"></a>
# Attack speed

[← Tables and calculations](../README.md)

<a id="модель"></a>
## Model

Cossacks 3 does not use a single “attacks per second” system. Instead:

- For ranged weapons, the cycle equals the reload time.
- For melee attacks, the cycle equals the attack-animation duration.
- Attacks per game second equal `1 / cycle duration`.
- On Fast, the real attack rate is 1.4 times higher.

A melee attack animation lasts between 11 and 33 frames depending on the
unit; the median is 15 frames.

<a id="1-скорость-атаки-по-юнитам"></a>
## §1. Unit attack speed

Each row represents one weapon used by a unit. Identical national variants are
grouped together.

**Cycle duration** is the time between attacks in game seconds. It is the
reload time for ranged weapons and the attack-animation duration for melee
weapons. A source marked **estimate** means that no readable animation was
available, so the median duration was used.
- **att/g-sec** — attacks per game second = `1 / cycle_g`.
- **att/real-sec @ fast** - the same × 1.4 (gc_settings_gamespeed_2).

Sorting: ranged → melee, inside - in descending order of attack frequency.

| sid | usage | weapon | dmg | range_t | cycle_g | src | att/g-sec | att/real@fast | nations |
| --- | --- | --- | ---: | ---: | ---: | --- | ---: | ---: | --- |
| `battleship` | Battleship | cannonball #0 | 1800 | 36.56 | 0.62 | pause | 1.61 | 2.26 | alg, aus, bav, den… (+16) |
| `archerdip` | Archer | firearrow #1 | 100 | 14.06 | 0.78 | pause | 1.28 | 1.79 | all |
| `archerturdip` | Archer | firearrow #1 | 100 | 14.06 | 0.78 | pause | 1.28 | 1.79 | all |
| `galley` | Galley | mortarball #1 | 1000 | 58.13 | 1.56 | pause | 0.64 | 0.90 | alg, aus, bav, den… (+16) |
| `tatar` | Archer | arrow #0 | 15 | 20.63 | 1.56 | pause | 0.64 | 0.90 | Turkey |
| `xebec` | Frigate | cannonball #0 | 1800 | 31.88 | 1.56 | pause | 0.64 | 0.90 | Algeria, Turkey |
| `multicannon` | Multi-cannon | cannister #0 | 500 | 13.13 | 1.88 | pause | 0.53 | 0.74 | aus, bav, den, eng… (+13) |
| `dragoon18dip` | Shooter | bullet #0 | 18 | 15.0 | 2.25 | pause | 0.44 | 0.62 | all |
| `lightcavalrydip` | Shooter | bullet #0 | 18 | 15.0 | 2.25 | pause | 0.44 | 0.62 | all |
| `archer` | Archer | arrow #0 | 15 | 15.0 | 2.34 | pause | 0.43 | 0.60 | Algeria |
| **Chaika** `chaika` | Yacht | cannonball #0 | 1000 | 20.63 | 2.34 | pause | 0.43 | 0.60 | Ukraine |
| `frigate` | Frigate | cannonball #0 | 1800 | 30.94 | 2.34 | pause | 0.43 | 0.60 | aus, bav, den, eng… (+14) |
| `grenadier` | Grenadier | mortarball #2 | 110 | 9.38 | 2.34 | pause | 0.43 | 0.60 | aus, eng, fra, net… (+9) |
| `grenadierbav` | Grenadier | mortarball #2 | 110 | 9.38 | 2.34 | pause | 0.43 | 0.60 | Bavaria |
| `grenadierden` | Grenadier | mortarball #2 | 110 | 9.38 | 2.34 | pause | 0.43 | 0.60 | Denmark |
| `grenadierpru` | Grenadier | mortarball #2 | 110 | 9.38 | 2.34 | pause | 0.43 | 0.60 | Prussia |
| `grenadiersax` | Grenadier | mortarball #2 | 110 | 9.38 | 2.34 | pause | 0.43 | 0.60 | Saxony |
| `archerdip` | Archer | arrow #0 | 25 | 13.13 | 2.50 | pause | 0.40 | 0.56 | all |
| `archerturdip` | Archer | arrow #0 | 25 | 13.13 | 2.50 | pause | 0.40 | 0.56 | all |
| `archertur` | Archer | arrow #0 | 20 | 16.88 | 2.66 | pause | 0.38 | 0.53 | Turkey |
| `framegun` | Cannon | cannonball #0 | 500 | 33.75 | 2.81 | pause | 0.36 | 0.50 | Scotland |
| `grenadierhun` | Grenadier | mortarball #2 | 110 | 11.25 | 2.81 | pause | 0.36 | 0.50 | Hungary |
| `archersco` | Archer | arrow #0 | 20 | 18.75 | 3.12 | pause | 0.32 | 0.45 | Scotland |
| `gauduk` | Shooter | bullet #1 | 9 | 14.06 | 3.12 | pause | 0.32 | 0.45 | Hungary |
| `grenadierdip` | Grenadier | mortarball #2 | 200 | 7.5 | 3.12 | pause | 0.32 | 0.45 | all |
| `musketeerpol` | Shooter | bullet #1 | 9 | 13.13 | 3.12 | pause | 0.32 | 0.45 | Poland |
| `musketeernet` | Shooter | bullet #1 | 10 | 15.0 | 3.75 | pause | 0.27 | 0.37 | Netherlands |
| `archer` | Archer | firearrow #1 | 150 | 11.25 | 3.91 | pause | 0.26 | 0.36 | Algeria |
| `serdiuk` | Shooter | bullet #1 | 12 | 16.88 | 4.06 | pause | 0.25 | 0.34 | Ukraine |
| `archersco` | Archer | firearrow #1 | 150 | 18.75 | 4.38 | pause | 0.23 | 0.32 | Scotland |
| `archertur` | Archer | firearrow #1 | 150 | 16.88 | 4.38 | pause | 0.23 | 0.32 | Turkey |
| `grenadierpru` | Grenadier | bullet #1 | 16 | 16.88 | 4.38 | pause | 0.23 | 0.32 | Prussia |
| `musketeer18sax` | Shooter | bullet #1 | 19 | 16.88 | 4.38 | pause | 0.23 | 0.32 | Saxony |
| `dragoon18fra` | Mounted Shooter | bullet #0 | 10 | 15.0 | 4.69 | pause | 0.21 | 0.30 | France |
| `galley` | Galley | cannonball #0 | 100 | 22.5 | 4.69 | pause | 0.21 | 0.30 | alg, aus, bav, den … (+16) |
| `grenadierdip` | Grenadier | bullet #1 | 16 | 15.0 | 4.69 | pause | 0.21 | 0.30 | all |
| `jannisary` | Shooter | bullet #1 | 12 | 15.94 | 4.69 | pause | 0.21 | 0.30 | Turkey |
| `musketeer` | Shooter | bullet #1 | 12 | 15.0 | 4.69 | pause | 0.21 | 0.30 | bav, den, eng, fra … (+7) |
| `musketeer18` | Shooter | bullet #1 | 16 | 16.88 | 4.69 | pause | 0.21 | 0.30 | aus, eng, fra, hun … (+9) |
| `musketeer18pru` | Shooter | bullet #1 | 22 | 17.81 | 4.69 | pause | 0.21 | 0.30 | Prussia |
| `musketeersco` | Shooter | bullet #1 | 12 | 15.94 | 4.69 | pause | 0.21 | 0.30 | Scotland |
| `pandur` | Shooter | bullet #1 | 17 | 16.88 | 4.69 | pause | 0.21 | 0.30 | Austria |
| `strelet` | Shooter | bullet #0 | 12 | 13.13 | 4.69 | pause | 0.21 | 0.30 | Russia |
| `tatar` | Archer | firearrow #1 | 140 | 20.63 | 4.69 | pause | 0.21 | 0.30 | Turkey |
| `dragoon18net` | Mounted Shooter | bullet #0 | 17 | 15.94 | 5.00 | pause | 0.20 | 0.28 | Netherlands |
| `dragoon18pie` | Mounted Shooter | bullet #0 | 19 | 16.88 | 5.00 | pause | 0.20 | 0.28 | Piedmont |
| `dragoonpol` | Mounted Shooter | bullet #0 | 13 | 15.94 | 5.00 | pause | 0.20 | 0.28 | Poland |
| `highlander` | Shooter | bullet #1 | 16 | 15.94 | 5.00 | pause | 0.20 | 0.28 | England |
| `musketeeraus` | Shooter | bullet #0 | 12 | 15.0 | 5.00 | pause | 0.20 | 0.28 | Austria |
| `pandurhun` | Shooter | bullet #1 | 19 | 18.75 | 5.00 | pause | 0.20 | 0.28 | Hungary |
| `dragoon18` | Mounted Shooter | bullet #0 | 19 | 16.88 | 5.31 | pause | 0.19 | 0.26 | aus, bav, den, eng … (+9) |
| `grenadier` | Grenadier | bullet #1 | 16 | 16.88 | 5.31 | pause | 0.19 | 0.26 | aus, eng, fra, net … (+9) |
| `grenadierbav` | Grenadier | bullet #1 | 19 | 16.88 | 5.31 | pause | 0.19 | 0.26 | Bavaria |
| `grenadierhun` | Grenadier | bullet #1 | 16 | 16.88 | 5.31 | pause | 0.19 | 0.26 | Hungary |
| `grenadiersax` | Grenadier | bullet #1 | 19 | 17.81 | 5.31 | pause | 0.19 | 0.26 | Saxony |
| `lightcavalry` | Mounted Shooter | bullet #0 | 14 | 18.75 | 5.31 | pause | 0.19 | 0.26 | Hungary |
| `dragoon` | Mounted Shooter | bullet #0 | 15 | 15.0 | 5.62 | pause | 0.18 | 0.25 | aus, bav, den, eng … (+12) |
| `chasseur` | Shooter | bullet #1 | 20 | 19.69 | 5.94 | pause | 0.17 | 0.24 | France |
| `grenadierden` | Grenadier | bullet #1 | 19 | 16.88 | 5.94 | pause | 0.17 | 0.24 | Denmark |
| `jagerpor` | Shooter | bullet #1 | 10 | 15.0 | 5.94 | pause | 0.17 | 0.24 | Portugal |
| `musketeer18bav` | Shooter | bullet #1 | 22 | 17.81 | 5.94 | pause | 0.17 | 0.24 | Bavaria |
| `musketeer18den` | Shooter | bullet #1 | 29 | 16.88 | 5.94 | pause | 0.17 | 0.24 | Denmark |
| `musketeerspa` | Shooter | bullet #0 | 15 | 15.94 | 5.94 | pause | 0.17 | 0.24 | Spain |
| `jagerswi` | Shooter | bullet #1 | 20 | 22.5 | 6.88 | pause | 0.15 | 0.20 | Switzerland |
| `kingmusketeer` | Mounted Shooter | bullet #0 | 43 | 13.13 | 6.88 | pause | 0.15 | 0.20 | France |
| `mortar` | Super Mortar | mortarball #0 | 200 | 48.75 | 7.81 | pause | 0.13 | 0.18 | all |
| `cannon` | Cannon | cannonball #0 | 1800 | 40.5 | 10.94 | pause | 0.09 | 0.13 | all |
| `yacht` | Yacht | cannonball #0 | 1000 | 20.63 | 10.94 | pause | 0.09 | 0.13 | aus, bav, den, eng … (+14) |
| `yachttur` | Yacht | cannonball #0 | 30 | 18.75 | 12.50 | pause | 0.08 | 0.11 | Turkey |
| `howitzer` | Mortar | cannonball #0 | 4000 | 26.25 | 18.75 | pause | 0.05 | 0.07 | all |
| `pikeman18` | Light Infantry | pike #0 | 9 | 1.88 | 0.28 | anim | 3.56 | 4.98 | aus, bav, den, eng … (+12) |
| `pikemanrus` | Light Infantry | pike #0 | 8 | 1.69 | 0.31 | anim | 3.20 | 4.48 | Russia |
| `pikeman18swe` | Light Infantry | pike #0 | 11 | 1.88 | 0.38 | anim | 2.67 | 3.73 | Sweden |
| `pikemanpol` | Light Infantry | pike #0 | 8 | 2.06 | 0.38 | anim | 2.67 | 3.73 | Poland |
| `pikemanpor` | Light Infantry | pike #0 | 9 | 1.88 | 0.38 | anim | 2.67 | 3.73 | Portugal |
| `pikemantur` | Light Infantry | pike #0 | 9 | 2.06 | 0.38 | anim | 2.67 | 3.73 | Algeria, Turkey |
| `roundshier` | Light Infantry | sword #0 | 6 | 1.13 | 0.38 | anim | 2.67 | 3.73 | Austria |
| `sipahi` | Heavy Cavalry | sword #0 | 15 | 1.22 | 0.38 | anim | 2.67 | 3.73 | Turkey |
| `vityaz` | Heavy Cavalry | pike #0 | 14 | 1.22 | 0.38 | anim | 2.67 | 3.73 | Russia |
| `wingedhussar` | Light Cavalry | pike #0 | 14 | 1.88 | 0.38 | anim | 2.67 | 3.73 | Poland |
| `cossacksich` | Light Cavalry | sword #0 | 13 | 1.22 | 0.41 | anim | 2.46 | 3.45 | Ukraine |
| `swordsmansco` | Light Infantry | sword #0 | 10 | 1.13 | 0.41 | anim | 2.46 | 3.45 | Scotland |
| `cossackdon` | Heavy Cavalry | pike #0 | 13 | 1.88 | 0.44 | anim | 2.29 | 3.20 | Russia |
| `cossackregister` | Heavy Cavalry | pike #0 | 12 | 1.88 | 0.44 | anim | 2.29 | 3.20 | Ukraine |
| `croat` | Light Cavalry | sword #0 | 9 | 1.22 | 0.44 | anim | 2.29 | 3.20 | Austria |
| `cuirassier` | Heavy Cavalry | pike #0 | 14 | 1.22 | 0.44 | anim | 2.29 | 3.20 | aus, bav, den, eng … (+13) |
| `guardcavalrysax` | Heavy Cavalry | pike #0 | 15 | 1.22 | 0.44 | anim | 2.29 | 3.20 | Saxony |
| `hackapell` | Light Cavalry | pike #0 | 12 | 1.22 | 0.44 | anim | 2.29 | 3.20 | Sweden |
| `hussar` | Light Cavalry | sword #0 | 12 | 1.22 | 0.44 | anim | 2.29 | 3.20 | aus, bav, den, eng … (+10) |
| `hussarhun` | Light Cavalry | sword #0 | 10 | 1.22 | 0.44 | anim | 2.29 | 3.20 | Hungary |
| `hussarpru` | Light Cavalry | sword #0 | 9 | 1.22 | 0.44 | anim | 2.29 | 3.20 | Prussia |
| `hussarswi` | Light Cavalry | sword #0 | 14 | 1.22 | 0.44 | anim | 2.29 | 3.20 | Switzerland |
| `lancersco` | Heavy Cavalry | pike #0 | 11 | 1.88 | 0.44 | anim | 2.29 | 3.20 | Scotland |
| `lightinfantry` | Light Infantry | sword #0 | 5 | 0.94 | 0.44 | anim | 2.29 | 3.20 | Algeria, Turkey |
| `mameluke` | Heavy Cavalry | pike #0 | 16 | 1.88 | 0.44 | anim | 2.29 | 3.20 | Algeria |
| `musketeer18` | Shooter | pike #0 | 10 | 1.22 | 0.44 | anim | 2.29 | 3.20 | aus, eng, fra, hun … (+9) |
| `officer` | Light Infantry | pike #0 | 30 | 1.22 | 0.44 | anim | 2.29 | 3.20 | aus, bav, den, eng … (+12) |
| `officerrus` | Light Infantry | pike #0 | 40 | 1.22 | 0.44 | anim | 2.29 | 3.20 | Russia |
| `raidersco` | Light Cavalry | sword #0 | 11 | 1.22 | 0.44 | anim | 2.29 | 3.20 | Scotland |
| `reiter` | Heavy Cavalry | pike #0 | 15 | 1.22 | 0.44 | anim | 2.29 | 3.20 | aus, bav, den, eng … (+10) |
| `reiterpol` | Heavy Cavalry | sword #0 | 9 | 1.22 | 0.44 | anim | 2.29 | 3.20 | Poland |
| `reiterswe` | Heavy Cavalry | pike #0 | 14 | 1.22 | 0.44 | anim | 2.29 | 3.20 | Sweden |
| `spakh` | Heavy Cavalry | pike #0 | 15 | 1.88 | 0.44 | anim | 2.29 | 3.20 | Turkey |
| `cossacksichdip` | Light Cavalry | sword #0 | 8 | 1.22 | 0.47 | fallback | 2.13 | 2.99 | all |
| `grenadierdip` | Grenadier | pike #0 | 30 | 1.5 | 0.47 | fallback | 2.13 | 2.99 | all |
| `hetman` | Heavy Cavalry | pike #0 | 70 | 1.22 | 0.47 | anim | 2.13 | 2.99 | Ukraine |
| `lightinfantrydip` | Light Infantry | sword #0 | 16 | 0.94 | 0.47 | fallback | 2.13 | 2.99 | all |
| `pikeman` | Light Infantry | pike #0 | 8 | 1.88 | 0.47 | anim | 2.13 | 2.99 | aus, bav, den, eng… (+8) |
| `pikeman` | Light Infantry | pike #0 | 10 | 1.88 | 0.47 | anim | 2.13 | 2.99 | Spain |
| `pikemansco` | Light Infantry | pike #0 | 9 | 1.88 | 0.47 | anim | 2.13 | 2.99 | Scotland |
| `pikemanspa` | Light Infantry | pike #0 | 10 | 1.88 | 0.47 | anim | 2.13 | 2.99 | Spain |
| `pikemanswi` | Light Infantry | pike #0 | 10 | 1.88 | 0.47 | anim | 2.13 | 2.99 | Switzerland |
| `roundshierdip` | Light Infantry | sword #0 | 6 | 1.13 | 0.47 | fallback | 2.13 | 2.99 | all |
| `grenadier` | Grenadier | pike #0 | 18 | 1.5 | 0.50 | anim | 2.00 | 2.80 | aus, eng, fra, net… (+9) |
| `grenadierbav` | Grenadier | pike #0 | 14 | 1.5 | 0.50 | anim | 2.00 | 2.80 | Bavaria |
| `grenadierden` | Grenadier | pike #0 | 22 | 1.5 | 0.50 | anim | 2.00 | 2.80 | Denmark |
| `grenadierhun` | Grenadier | pike #0 | 30 | 1.5 | 0.50 | anim | 2.00 | 2.80 | Hungary |
| `grenadierpru` | Grenadier | pike #0 | 18 | 1.5 | 0.50 | anim | 2.00 | 2.80 | Prussia |
| `grenadiersax` | Grenadier | pike #0 | 22 | 1.5 | 0.50 | anim | 2.00 | 2.80 | Saxony |
| `musketeer18bav` | Shooter | pike #0 | 5 | 1.59 | 0.53 | anim | 1.88 | 2.64 | Bavaria |
| `musketeer18den` | Shooter | pike #0 | 8 | 1.59 | 0.53 | anim | 1.88 | 2.64 | Denmark |
| `musketeer18pru` | Shooter | pike #0 | 10 | 1.59 | 0.53 | anim | 1.88 | 2.64 | Prussia |
| `musketeer18sax` | Shooter | pike #0 | 7 | 1.22 | 0.53 | anim | 1.88 | 2.64 | Saxony |
| `officer18` | Light Infantry | pike #0 | 50 | 1.22 | 0.56 | anim | 1.78 | 2.49 | aus, bav, den, eng… (+13) |
| `officersco` | Light Infantry | pike #0 | 40 | 1.22 | 0.56 | anim | 1.78 | 2.49 | Scotland |
| `officertur` | Light Infantry | pike #0 | 30 | 1.22 | 0.56 | anim | 1.78 | 2.49 | Algeria, Turkey |
| `peaaus` | Peasant | sword #0 | 20 | 1.22 | 0.56 | anim | 1.78 | 2.49 | Austria, Bavaria, Prussia, Saxony, Switzerland |
| `peaeng` | Peasant | sword #0 | 20 | 1.22 | 0.56 | anim | 1.78 | 2.49 | Denmark, England, France, Netherlands, Sweden |
| `peapol` | Peasant | sword #0 | 20 | 1.22 | 0.56 | anim | 1.78 | 2.49 | Hungary, Poland |
| `pearus` | Peasant | sword #0 | 20 | 1.22 | 0.56 | anim | 1.78 | 2.49 | Russia |
| `peasco` | Peasant | sword #0 | 20 | 1.22 | 0.56 | anim | 1.78 | 2.49 | Scotland |
| `peaspa` | Peasant | sword #0 | 20 | 1.22 | 0.56 | anim | 1.78 | 2.49 | Piedmont, Portugal, Spain, Venice |
| `peatur` | Peasant | sword #0 | 20 | 1.22 | 0.56 | anim | 1.78 | 2.49 | Algeria, Turkey |
| `peaukr` | Peasant | sword #0 | 20 | 1.22 | 0.56 | anim | 1.78 | 2.49 | Ukraine |

<a id="2-сводка-по-типу-оружия"></a>
## §2. Weapon Type Summary

Min / median / max cycle duration for each `kind`. Helps to see “how much slower one crossbow attack is than another” within a class and understand where `attpauseperc` upgrades give the most profit.

| kind | n | min cycle (g-sec) | median | max | min att/real@fast |
| --- | ---: | ---: | ---: | ---: | ---: |
| arrow | 6 | 1.56 | 2.50 | 3.12 | 0.90 |
| bullet | 38 | 2.25 | 5.00 | 6.88 | 0.62 |
| canister | 1 | 1.88 | 1.88 | 1.88 | 0.74 |
| cannonball | 10 | 0.62 | 4.69 | 18.75 | 2.26 |
| firearrow | 6 | 0.78 | 4.38 | 4.69 | 1.79 |
| mortarball | 9 | 1.56 | 2.34 | 7.81 | 0.90 |
| pike | 41 | 0.28 | 0.44 | 0.56 | 4.98 |
| sword | 23 | 0.38 | 0.44 | 0.56 | 3.73 |

<a id="3-замечания"></a>
## §3. Notes
- **Pause vs swing.** In Cossacks 3 for remote weapons `pause` is a full cycle (shot animation inside pause). For melee `pause=0` and the cycle is equal to the length of the animation itself `attack0`.
- **Fallback** for melee = 15 frames (≈ 0.4688 g-sec, median over all units with .aaf). Applies if for a specific `sid` there is no file in `data/animations/aaf/` or there is no track `attack0`.
- **Multi-weapon units.** Musketeer18 (bayonet + musket), archer with flaming arrows, etc. — in their table there is a line for weapons, the column `weapon` shows `#index`.
- **`heal` excluded.** Priest = non-aggressive, not included in combat DPS calculation.
- **Real vs game.** All game logic (animations, pause) is in **game** seconds. To get real time at fast speed, divide g-sec by 1.4 (or multiply rate by 1.4).
- **Cooldown upgrades.** `attpauseperc` (see [`reference/05_upgrades/README.md`](../../reference/05_upgrades/README.md)) only reduces pause in ranged. Melee swing is not upgradeable - it is tied to animation.
