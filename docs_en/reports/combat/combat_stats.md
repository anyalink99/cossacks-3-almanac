# Cossacks 3 – DPS / EHP / armor metrics

**Derived** file (calculated, not extracted). Considered from `data.json` script [`compute/compute_combat_stats.py`](../../../compute/compute_combat_stats.py).

## Damage formula

Damage calculation is done in `_misc_DoDamage` [^1]. Briefly:
```
applied_damage = max(1, base_damage + squad_bonus - target.protection[weapon_kind])
target.hp     -= applied_damage
```
`gc_settings_gamespeed_2 = 14` (fast). Game-time → real-time: `×1.4`. 
Real DPS = game-DPS × game_speed.

## §1. Summary table of combat units

Grouping: one line for each unique set of stats. Column **Nations** - where this unit with these stats is available (`all 21` = in all). If a unit has different values ​​for different nations (for example, `pikemanpol` has half the armor of the standard) - these are different lines.

Columns: HP, speed (px per game second; 32 = peasant), main weapon (damage / pause / range / type), DPS in game secondss, DPS in real seconds (×1.4 at fast speed), defense (non-zero only) and shield. A unit can have several weapons - the **strongest in terms of damage/pause ratio** is shown.

| `sid` | Nations | Class | HP | Speed ​​| Primary Weapon | DPS, g-sec | DPS, real (fast) | Protection |
| --- | --- | --- | ---: | ---: | --- | ---: | ---: | --- |
| `tatar` | **tur** Turkey | Archer | 185 | 32 | 140d / 4.69s / 20.63t [firearrow] | 29.85 | 41.79 | — |
| `archersco` | **sco** Scotland | Archer | 150 | 32 | 150d / 4.38s / 18.75t [firearrow] | 34.25 | 47.95 | — |
| `archertur` | **tur** Turkey | Archer | 65 | 32 | 150d / 4.38s / 16.88t [firearrow] | 34.25 | 47.95 | — |
| `archer` | **alg** Algeria | Archer | 40 | 32 | 150d / 3.91s / 11.25t [firearrow] | 38.36 | 53.7 | — |
| `archerdip` | all 21 | Archer | 20 | 32 | 100d / 0.78s / 14.06t [firearrow] | 128.21 | 179.49 | — |
| `archerturdip` | all 21 | Archer | 20 | 32 | 100d / 0.78s / 14.06t [firearrow] | 128.21 | 179.49 | — |
| `cannon` | all 21 | Cannon | 9000 | 20 | 1800d / 10.94s / 40.5t [cannonball] | 164.53 | 230.34 | shield=75 |
| `framegun` | **sco** Scotland | Cannon | 3000 | 20 | 500d / 2.81s / 33.75t [cannonball] | 177.94 | 249.12 | shield=50 |
| `grenadierbav` | **bav** Bavaria | Grenadier | 125 | 32 | 110d / 2.34s / 9.38t [mortarball] | 47.01 | 65.81 | — |
| `grenadierden` | **den** Denmark | Grenadier | 125 | 32 | 110d / 2.34s / 9.38t [mortarball] | 47.01 | 65.81 | — |
| `grenadierhun` | **hun** Hungary | Grenadier | 125 | 32 | 110d / 2.81s / 11.25t [mortarball] | 39.15 | 54.81 | — |
| `grenadierpru` | **pru** Prussia | Grenadier | 125 | 32 | 110d / 2.34s / 9.38t [mortarball] | 47.01 | 65.81 | — |
| `grenadier` | **aus** Austria, **eng** England, **fra** France, **net** Netherlands, **pie** Piedmont … (+8) | Grenadier | 120 | 32 | 110d / 2.34s / 9.38t [mortarball] | 47.01 | 65.81 | — |
| `grenadiersax` | **sax** Saxony | Grenadier | 100 | 32 | 110d / 2.34s / 9.38t [mortarball] | 47.01 | 65.81 | — |
| `grenadierdip` | all 21 | Grenadier | 30 | 32 | 200d / 3.12s / 7.5t [mortarball] | 64.1 | 89.74 | — |
| `vityaz` | **eng** Russia | Heavy Cavalry | 380 | 56 | 14d / 0 (melee) / 1.22t [pike] | — | — | pike=2, sword=4, bullet=3, cannister=160, arrow=17, cannonball=40 |
| `sipahi` | **tur** Turkey | Heavy Cavalry | 360 | 56 | 15d / 0 (melee) / 1.22t [sword] | — | — | pike=3, sword=7, bullet=4, cannister=225, arrow=24, cannonball=60 |
| `guardcavalrysax` | **sax** Saxony | Heavy Cavalry | 320 | 56 | 15d / 0 (melee) / 1.22t [pike] | — | — | pike=2, sword=5, bullet=9, cannister=150, arrow=9, cannonball=70 |
| `hetman` | **ukr** Ukraine | Heavy Cavalry | 320 | 56 | 70d / 0 (melee) / 1.22t [pike] | — | — | sword=1, bullet=3, cannister=75, arrow=3, cannonball=15 |
| `lancersco` | **sco** Scotland | Heavy Cavalry | 320 | 56 | 11d / 0 (melee) / 1.88t [pike] | — | — | — |
| `cuirassier` | **aus** Austria, **bav** Bavaria, **den** Denmark, **eng** England, **fra** France … (+12) | Heavy Cavalry | 300 | 56 | 14d / 0 (melee) / 1.22t [pike] | — | — | pike=2, sword=4, bullet=10, cannister=160, arrow=5, cannonball=80 |
| `reiter` | **aus** Austria, **bav** Bavaria, **den** Denmark, **eng** England, **fra** France … (+9) | Heavy Cavalry | 300 | 56 | 15d / 0 (melee) / 1.22t [pike] | — | — | pike=2, sword=6, bullet=6, cannister=190, arrow=15, cannonball=40 |
| `reiterswe` | **swe** Sweden | Heavy Cavalry | 300 | 56 | 14d / 0 (melee) / 1.22t [pike] | — | — | pike=2, sword=3, bullet=7, cannister=140, arrow=7, cannonball=35 |
| `mameluke` | **alg** Algeria | Heavy Cavalry | 280 | 56 | 16d / 0 (melee) / 1.88t [pike] | — | — | pike=1, sword=3, bullet=1, cannister=75, arrow=8 |
| `cossackregister` | **ukr** Ukraine | Heavy Cavalry | 250 | 56 | 12d / 0 (melee) / 1.88t [pike] | — | — | — |
| `spakh` | **tur** Turkey | Heavy Cavalry | 230 | 56 | 15d / 0 (melee) / 1.88t [pike] | — | — | sword=1, cannister=10, arrow=2 |
| `cossackdon` | **eng** Russia | Heavy Cavalry | 220 | 56 | 13d / 0 (melee) / 1.88t [pike] | — | — | — |
| `reiterpol` | **pol** Poland | Heavy Cavalry | 190 | 56 | 9d / 0 (melee) / 1.22t [sword] | — | — | — |
| `raidersco` | **sco** Scotland | Light Cavalry | 280 | 96 | 11d / 0 (melee) / 1.22t [sword] | — | — | — |
| `hussarswi` | **swi** Switzerland | Light Cavalry | 265 | 96 | 14d / 0 (melee) / 1.22t [sword] | — | — | — |
| `croat` | **aus** Austria | Light Cavalry | 260 | 96 | 9d / 0 (melee) / 1.22t [sword] | — | — | — |
| `cossacksich` | **ukr** Ukraine | Light Cavalry | 250 | 96 | 13d / 0 (melee) / 1.22t [sword] | — | — | — |
| `hussarhun` | **hun** Hungary | Light Cavalry | 250 | 96 | 10d / 0 (melee) / 1.22t [sword] | — | — | — |
| `hackapell` | **swe** Sweden | Light Cavalry | 245 | 96 | 12d / 0 (melee) / 1.22t [pike] | — | — | — |
| `hussarpru` | **pru** Prussia | Light Cavalry | 240 | 96 | 9d / 0 (melee) / 1.22t [sword] | — | — | — |
| `hussar` | **aus** Austria, **bav** Bavaria, **den** Denmark, **eng** England, **fra** France … (+9) | Light Cavalry | 230 | 96 | 12d / 0 (melee) / 1.22t [sword] | — | — | — |
| `wingedhussar` | **pol** Poland | Light Cavalry | 225 | 96 | 14d / 0 (melee) / 1.88t [pike] | — | — | pike=1, sword=2, bullet=5, cannister=160, arrow=10, cannonball=30 |
| `cossacksichdip` | all 21 | Light Cavalry | 150 | 96 | 8d / 0 (melee) / 1.22t [sword] | — | — | — |
| `swordsmansco` | **sco** Scotland | Light Infantry | 180 | 32 | 10d / 0 (melee) / 1.13t [sword] | — | — | pike=1, sword=2, bullet=2, cannister=110, arrow=6, cannonball=10 |
| `bagpiper` | **eng** England, **sco** Scotland | Light Infantry | 150 | 32 | — | — | — | — |
| `officersco` | **sco** Scotland | Light Infantry | 150 | 32 | 40d / 0 (melee) / 1.22t [pike] | — | — | — |
| `officer` | **aus** Austria, **bav** Bavaria, **den** Denmark, **eng** England, **fra** France … (+11) | Light Infantry | 125 | 32 | 30d / 0 (melee) / 1.22t [pike] | — | — | pike=2, sword=2, bullet=5, cannister=200, arrow=10, cannonball=30 |
| `officer18` | **aus** Austria, **bav** Bavaria, **den** Denmark, **eng** England, **fra** France … (+12) | Light Infantry | 125 | 32 | 50d / 0 (melee) / 1.22t [pike] | — | — | — |
| `officerrus` | **eng** Russia | Light Infantry | 125 | 32 | 40d / 0 (melee) / 1.22t [pike] | — | — | — |
| `officertur` | **alg** Algeria, **tur** Turkey | Light Infantry | 125 | 32 | 30d / 0 (melee) / 1.22t [pike] | — | — | — |
| `pikeman18swe` | **swe** Sweden | Light Infantry | 110 | 32 | 11d / 0 (melee) / 1.88t [pike] | — | — | — |
| `drummer18` | **aus** Austria, **bav** Bavaria, **den** Denmark, **fra** France, **hun** Hungary … (+11) | Light Infantry | 100 | 32 | — | — | — | — |
| `drummerrus` | **eng** Russia | Light Infantry | 100 | 32 | — | — | — | — |
| `pikeman` | **spa** Spain | Light Infantry | 100 | 32 | 10d / 0 (melee) / 1.88t [pike] | — | — | pike=3, sword=4, bullet=6, cannister=240, arrow=12, cannonball=50 |
| `pikemanpor` | **por** Portugal | Light Infantry | 100 | 32 | 9d / 0 (melee) / 1.88t [pike] | — | — | sword=1, bullet=1, cannister=25, arrow=4 |
| `pikemansco` | **sco** Scotland | Light Infantry | 100 | 32 | 9d / 0 (melee) / 1.88t [pike] | — | — | — |
| `pikemanspa` | **spa** Spain | Light Infantry | 100 | 32 | 10d / 0 (melee) / 1.88t [pike] | — | — | pike=3, sword=4, bullet=6, cannister=240, arrow=12, cannonball=50 |
| `priest` | **aus** Austria, **bav** Bavaria, **den** Denmark, **eng** England, **fra** France … (+11) | Light Infantry | 100 | 32 | — | — | — | — |
| `roundshier` | **aus** Austria | Light Infantry | 100 | 32 | 6d / 0 (melee) / 1.13t [sword] | — | — | pike=3, sword=3, bullet=7, cannister=225, arrow=16, cannonball=80 |
| `pikemantur` | **alg** Algeria, **tur** Turkey | Light Infantry | 95 | 32 | 9d / 0 (melee) / 2.06t [pike] | — | — | — |
| `padre` | **pie** Piedmont | Light Infantry | 90 | 32 | — | — | — | — |
| `pikeman` | **aus** Austria, **bav** Bavaria, **den** Denmark, **eng** England, **fra** France … (+7) | Light Infantry | 90 | 32 | 8d / 0 (melee) / 1.88t [pike] | — | — | pike=3, sword=2, bullet=4, cannister=210, arrow=6, cannonball=40 |
| `pikemanpol` | **pol** Poland | Light Infantry | 90 | 32 | 8d / 0 (melee) / 2.06t [pike] | — | — | — |
| `pikemanswi` | **swi** Switzerland | Light Infantry | 90 | 32 | 10d / 0 (melee) / 1.88t [pike] | — | — | pike=3, sword=3, bullet=6, cannister=220, arrow=6, cannonball=45 |
| `pikeman18` | **aus** Austria, **bav** Bavaria, **den** Denmark, **eng** England, **fra** France … (+11) | Light Infantry | 85 | 32 | 9d / 0 (melee) / 1.88t [pike] | — | — | — |
| `pikemanrus` | **eng** Russia | Light Infantry | 85 | 32 | 8d / 0 (melee) / 1.69t [pike] | — | — | pike=2, sword=1, bullet=4, cannister=140, arrow=4, cannonball=25 |
| `drummer` | **aus** Austria, **bav** Bavaria, **den** Denmark, **eng** England, **fra** France … (+11) | Light Infantry | 75 | 32 | — | — | — | — |
| `mullah` | **alg** Algeria, **tur** Turkey | Light Infantry | 75 | 32 | — | — | — | — |
| `pope` | **rus** Russia, **ukr** Ukraine | Light Infantry | 75 | 32 | — | — | — | — |
| `roundshierdip` | all 21 | Light Infantry | 75 | 32 | 6d / 0 (melee) / 1.13t [sword] | — | — | pike=5, sword=3, bullet=8, cannister=225, arrow=17, cannonball=80 |
| `lightinfantry` | **alg** Algeria, **tur** Turkey | Light Infantry | 55 | 32 | 5d / 0 (melee) / 0.94t [sword] | — | — | — |
| `drummertur` | **alg** Algeria, **tur** Turkey | Light Infantry | 50 | 32 | — | — | — | — |
| `lightinfantrydip` | all 21 | Light Infantry | 50 | 32 | 16d / 0 (melee) / 0.94t [sword] | — | — | — |
| `howitzer` | all 21 | Bombard | 3000 | 20 | 4000d / 18.75s / 26.25t [cannonball] | 213.33 | 298.66 | shield=75 |
| `dragoon18net` | **net** Netherlands | Horse Rifleman | 320 | 56 | 17d / 5.0s / 15.94t [bullet] | 3.4 | 4.76 | — |
| `kingmusketeer` | **fra** France | Horse Rifleman | 280 | 56 | 43d / 6.88s / 13.13t [bullet] | 6.25 | 8.75 | — |
| `dragoon18` | **aus** Austria, **bav** Bavaria, **den** Denmark, **eng** England, **pol** Poland … (+8) | Horse Rifleman | 225 | 56 | 19d / 5.31s / 16.88t [bullet] | 3.58 | 5.01 | — |
| `dragoon` | **aus** Austria, **bav** Bavaria, **den** Denmark, **eng** England, **fra** France … (+11) | Horse Rifleman | 220 | 56 | 15d / 5.62s / 15.0t [bullet] | 2.67 | 3.74 | — |
| `dragoon18pie` | **pie** Piedmont | Horse Rifleman | 200 | 56 | 19d / 5.0s / 16.88t [bullet] | 3.8 | 5.32 | — |
| `dragoonpol` | **pol** Poland | Horse Rifleman | 185 | 56 | 13d / 5.0s / 15.94t [bullet] | 2.6 | 3.64 | — |
| `lightcavalry` | **hun** Hungary | Horse Rifleman | 175 | 56 | 14d / 5.31s / 18.75t [bullet] | 2.64 | 3.7 | — |
| `dragoon18fra` | **fra** France | Horse Rifleman | 140 | 56 | 10d / 4.69s / 15.0t [bullet] | 2.13 | 2.98 | — |
| `multicannon` | **aus** Austria, **bav** Bavaria, **den** Denmark, **eng** England, **fra** France … (+12) | Richbarreled gun | 2000 | 16 | 500d / 1.88s / 13.13t [cannister] | 265.96 | 372.34 | shield=50 |
| `highlander` | **eng** England | Shooter | 130 | 32 | 16d / 5.0s / 15.94t [bullet] | 3.2 | 4.48 | — |
| `dragoon18dip` | all 21 | Shooter | 100 | 56 | 18d / 2.25s / 15.0t [bullet] | 8.0 | 11.2 | — |
| `lightcavalrydip` | all 21 | Shooter | 100 | 56 | 18d / 2.25s / 15.0t [bullet] | 8.0 | 11.2 | — |
| `musketeer18` | **aus** Austria, **eng** England, **fra** France, **hun** Hungary, **net** Netherlands … (+8) | Shooter | 100 | 32 | 16d / 4.69s / 16.88t [bullet] | 3.41 | 4.77 | — |
| `musketeer18bav` | **bav** Bavaria | Shooter | 100 | 32 | 22d / 5.94s / 17.81t [bullet] | 3.7 | 5.18 | — |
| `musketeer18den` | **den** Denmark | Shooter | 100 | 32 | 29d / 5.94s / 16.88t [bullet] | 4.88 | 6.83 | — |
| `musketeer18pru` | **pru** Prussia | Shooter | 100 | 32 | 22d / 4.69s / 17.81t [bullet] | 4.69 | 6.57 | — |
| `musketeer18sax` | **sax** Saxony | Shooter | 90 | 32 | 19d / 4.38s / 16.88t [bullet] | 4.34 | 6.08 | — |
| `musketeersco` | **sco** Scotland | Shooter | 90 | 32 | 12d / 4.69s / 15.94t [bullet] | 2.56 | 3.58 | — |
| `musketeerspa` | **spa** Spain | Shooter | 85 | 32 | 15d / 5.94s / 15.94t [bullet] | 2.53 | 3.54 | pike=3, sword=2, bullet=5, cannister=210, arrow=7, cannonball=40 |
| `pandur` | **aus** Austria | Shooter | 85 | 32 | 17d / 4.69s / 16.88t [bullet] | 3.62 | 5.07 | — |
| `serdiuk` | **ukr** Ukraine | Shooter | 85 | 32 | 12d / 4.06s / 16.88t [bullet] | 2.96 | 4.14 | — |
| `strelet` | **eng** Russia | Shooter | 85 | 32 | 12d / 4.69s / 13.13t [bullet] | 2.56 | 3.58 | — |
| `chasseur` | **fra** France | Shooter | 75 | 32 | 20d / 5.94s / 19.69t [bullet] | 3.37 | 4.72 | — |
| `pandurhun` | **hun** Hungary | Shooter | 75 | 32 | 19d / 5.0s / 18.75t [bullet] | 3.8 | 5.32 | — |
| `musketeer` | **bav** Bavaria, **den** Denmark, **eng** England, **fra** France, **pie** Piedmont … (+6) | Shooter | 70 | 32 | 12d / 4.69s / 15.0t [bullet] | 2.56 | 3.58 | — |
| `musketeerpol` | **pol** Poland | Shooter | 70 | 32 | 9d / 3.12s / 13.13t [bullet] | 2.88 | 4.03 | — |
| `jagerswi` | **swi** Switzerland | Shooter | 65 | 32 | 20d / 6.88s / 22.5t [bullet] | 2.91 | 4.07 | — |
| `jannisary` | **tur** Turkey | Shooter | 65 | 32 | 12d / 4.69s / 15.94t [bullet] | 2.56 | 3.58 | — |
| `musketeernet` | **net** Netherlands | Shooter | 65 | 32 | 10d / 3.75s / 15.0t [bullet] | 2.67 | 3.74 | — |
| `gauduk` | **hun** Hungary | Shooter | 60 | 32 | 9d/3.12s/14.06t [bullet] | 2.88 | 4.03 | — |
| `musketeeraus` | **aus** Austria | Shooter | 55 | 32 | 12d / 5.0s / 15.0t [bullet] | 2.4 | 3.36 | pike=2, sword=2, bullet=5, cannister=165, arrow=5, cannonball=35 |
| `jagerpor` | **por** Portugal | Shooter | 50 | 32 | 10d / 5.94s / 15.0t [bullet] | 1.68 | 2.35 | — |
| `mortar` | all 21 | Supermortar | 400 | 24 | 200d / 7.81s / 48.75t [mortarball] | 25.61 | 35.85 | shield=25 |

<a id="2-рейтинг-dps--боевые-юниты"></a>
## §2. DPS Rating - Combat Units

All combat units with `pause > 0` (melee with `pause = 0` are excluded - their damage is tied to the animation cycle, see §4). DPS is calculated in game-sec; column "DPS real (fast)" - ×1.4 for easy comparison with what is visible in real time.

| # | sid | nations | usage | HP | weapon kind | damage | pause, s | far., tile. | DPS g-s | DPS real |
| ---: | --- | --- | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | `multicannon` | **aus** Austria, **bav** Bavaria, **den** Denmark, **eng** England, **fra** France … (+12) | Multi-cannon | 2000 | canister | 500 | 1.88 | 13.13 | 265.96 | 372.34 |
| 2 | `howitzer` | all 21 | Mortar | 3000 | cannonball | 4000 | 18.75 | 26.25 | 213.33 | 298.66 |
| 3 | `framegun` | **sco** Scotland | Cannon | 3000 | cannonball | 500 | 2.81 | 33.75 | 177.94 | 249.12 |
| 4 | `cannon` | all 21 | Cannon | 9000 | cannonball | 1800 | 10.94 | 40.5 | 164.53 | 230.34 |
| 5 | `archerdip` | all 21 | Archer | 20 | firearrow | 100 | 0.78 | 14.06 | 128.21 | 179.49 |
| 6 | `archerturdip` | all 21 | Archer | 20 | firearrow | 100 | 0.78 | 14.06 | 128.21 | 179.49 |
| 7 | `grenadierdip` | all 21 | Grenadier | 30 | mortarball | 200 | 3.12 | 7.5 | 64.1 | 89.74 |
| 8 | `grenadier` | **aus** Austria, **eng** England, **fra** France, **net** Netherlands, **pie** Piedmont … (+8) | Grenadier | 120 | mortarball | 110 | 2.34 | 9.38 | 47.01 | 65.81 |
| 9 | `grenadierpru` | **pru** Prussia | Grenadier | 125 | mortarball | 110 | 2.34 | 9.38 | 47.01 | 65.81 |
| 10 | `grenadierden` | **den** Denmark | Grenadier | 125 | mortarball | 110 | 2.34 | 9.38 | 47.01 | 65.81 |
| 11 | `grenadiersax` | **sax** Saxony | Grenadier | 100 | mortarball | 110 | 2.34 | 9.38 | 47.01 | 65.81 |
| 12 | `grenadierbav` | **bav** Bavaria | Grenadier | 125 | mortarball | 110 | 2.34 | 9.38 | 47.01 | 65.81 |
| 13 | `grenadierhun` | **hun** Hungary | Grenadier | 125 | mortarball | 110 | 2.81 | 11.25 | 39.15 | 54.81 |
| 14 | `archer` | **alg** Algeria | Archer | 40 | firearrow | 150 | 3.91 | 11.25 | 38.36 | 53.7 |
| 15 | `archertur` | **tur** Turkey | Archer | 65 | firearrow | 150 | 4.38 | 16.88 | 34.25 | 47.95 |
| 16 | `archersco` | **sco** Scotland | Archer | 150 | firearrow | 150 | 4.38 | 18.75 | 34.25 | 47.95 |
| 17 | `tatar` | **tur** Turkey | Archer | 185 | firearrow | 140 | 4.69 | 20.63 | 29.85 | 41.79 |
| 18 | `mortar` | all 21 | Super Mortar | 400 | mortarball | 200 | 7.81 | 48.75 | 25.61 | 35.85 |
| 19 | `dragoon18dip` | all 21 | Shooter | 100 | bullet | 18 | 2.25 | 15.0 | 8.0 | 11.2 |
| 20 | `lightcavalrydip` | all 21 | Shooter | 100 | bullet | 18 | 2.25 | 15.0 | 8.0 | 11.2 |
| 21 | `kingmusketeer` | **fra** France | Mounted Shooter | 280 | bullet | 43 | 6.88 | 13.13 | 6.25 | 8.75 |
| 22 | `musketeer18den` | **den** Denmark | Shooter | 100 | bullet | 29 | 5.94 | 16.88 | 4.88 | 6.83 |
| 23 | `musketeer18pru` | **pru** Prussia | Shooter | 100 | bullet | 22 | 4.69 | 17.81 | 4.69 | 6.57 |
| 24 | `musketeer18sax` | **sax** Saxony | Shooter | 90 | bullet | 19 | 4.38 | 16.88 | 4.34 | 6.08 |
| 25 | `dragoon18pie` | **pie** Piedmont | Mounted Shooter | 200 | bullet | 19 | 5.0 | 16.88 | 3.8 | 5.32 |
| 26 | `pandurhun` | **hun** Hungary | Shooter | 75 | bullet | 19 | 5.0 | 18.75 | 3.8 | 5.32 |
| 27 | `musketeer18bav` | **bav** Bavaria | Shooter | 100 | bullet | 22 | 5.94 | 17.81 | 3.7 | 5.18 |
| 28 | `pandur` | **aus** Austria | Shooter | 85 | bullet | 17 | 4.69 | 16.88 | 3.62 | 5.07 |
| 29 | `dragoon18` | **aus** Austria, **bav** Bavaria, **den** Denmark, **eng** England, **pol** Poland … (+8) | Mounted Shooter | 225 | bullet | 19 | 5.31 | 16.88 | 3.58 | 5.01 |
| 30 | `musketeer18` | **aus** Austria, **eng** England, **fra** France, **hun** Hungary, **net** Netherlands … (+8) | Shooter | 100 | bullet | 16 | 4.69 | 16.88 | 3.41 | 4.77 |
| 31 | `dragoon18net` | **net** Netherlands | Mounted Shooter | 320 | bullet | 17 | 5.0 | 15.94 | 3.4 | 4.76 |
| 32 | `chasseur` | **fra** France | Shooter | 75 | bullet | 20 | 5.94 | 19.69 | 3.37 | 4.72 |
| 33 | `highlander` | **eng** England | Shooter | 130 | bullet | 16 | 5.0 | 15.94 | 3.2 | 4.48 |
| 34 | `serdiuk` | **ukr** Ukraine | Shooter | 85 | bullet | 12 | 4.06 | 16.88 | 2.96 | 4.14 |
| 35 | `jagerswi` | **swi** Switzerland | Shooter | 65 | bullet | 20 | 6.88 | 22.5 | 2.91 | 4.07 |
| 36 | `musketeerpol` | **pol** Poland | Shooter | 70 | bullet | 9 | 3.12 | 13.13 | 2.88 | 4.03 |
| 37 | `gauduk` | **hun** Hungary | Shooter | 60 | bullet | 9 | 3.12 | 14.06 | 2.88 | 4.03 |
| 38 | `dragoon` | **aus** Austria, **bav** Bavaria, **den** Denmark, **eng** England, **fra** France … (+11) | Mounted Shooter | 220 | bullet | 15 | 5.62 | 15.0 | 2.67 | 3.74 |
| 39 | `musketeernet` | **net** Netherlands | Shooter | 65 | bullet | 10 | 3.75 | 15.0 | 2.67 | 3.74 |
| 40 | `lightcavalry` | **hun** Hungary | Mounted Shooter | 175 | bullet | 14 | 5.31 | 18.75 | 2.64 | 3.7 |
| 41 | `dragoonpol` | **pol** Poland | Mounted Shooter | 185 | bullet | 13 | 5.0 | 15.94 | 2.6 | 3.64 |
| 42 | `musketeer` | **bav** Bavaria, **den** Denmark, **eng** England, **fra** France, **pie** Piedmont … (+6) | Shooter | 70 | bullet | 12 | 4.69 | 15.0 | 2.56 | 3.58 |
| 43 | `strelet` | **eng** Russia | Shooter | 85 | bullet | 12 | 4.69 | 13.13 | 2.56 | 3.58 |
| 44 | `jannisary` | **tur** Turkey | Shooter | 65 | bullet | 12 | 4.69 | 15.94 | 2.56 | 3.58 |
| 45 | `musketeersco` | **sco** Scotland | Shooter | 90 | bullet | 12 | 4.69 | 15.94 | 2.56 | 3.58 |
| 46 | `musketeerspa` | **spa** Spain | Shooter | 85 | bullet | 15 | 5.94 | 15.94 | 2.53 | 3.54 |
| 47 | `musketeeraus` | **aus** Austria | Shooter | 55 | bullet | 12 | 5.0 | 15.0 | 2.4 | 3.36 |
| 48 | `dragoon18fra` | **fra** France | Mounted Shooter | 140 | bullet | 10 | 4.69 | 15.0 | 2.13 | 2.98 |
| 49 | `jagerpor` | **por** Portugal | Shooter | 50 | bullet | 10 | 5.94 | 15.0 | 1.68 | 2.35 |

<a id="3-effective-hp--против-эталонной-атаки-10-единиц-урона-по-типу"></a>
## §3. Effective HP - against standard attack 10 units of damage by type

`EHP_vs_X = HP / max(1, 10 - prot[X])` - how many hits will a unit withstand if it is hit by a weapon of type X with a base damage of 10. For attacks with higher/lower damage, divide/multiply proportionally (the formula is linear if damage > prot). If `damage <= prot`, the engine guarantees at least 1 damage/hit [^2] - therefore EHP is not infinite against the pike of a pikeman with prot_pike=3, but exactly `HP / max(1, dmg-prot)`.

Only units that have at least one protection value ≠ 0 are included (the filter excludes typical “naked” units like archers/musketeers without armor).

| sid | nations | usage | HP | shield | EHP pike | sword | bullet | canister | arrow | cannonball |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `vityaz` | **eng** Russia | Heavy Cavalry | 380 | — | 47.5 | 63.3 | 54.3 | 380.0 | 380.0 | 380.0 |
| `sipahi` | **tur** Turkey | Heavy Cavalry | 360 | — | 51.4 | 120.0 | 60.0 | 360.0 | 360.0 | 360.0 |
| `guardcavalrysax` | **sax** Saxony | Heavy Cavalry | 320 | — | 40.0 | 64.0 | 320.0 | 320.0 | 320.0 | 320.0 |
| `hetman` | **ukr** Ukraine | Heavy Cavalry | 320 | — | 32.0 | 35.6 | 45.7 | 320.0 | 45.7 | 320.0 |
| `cuirassier` | **aus** Austria, **bav** Bavaria, **den** Denmark, **eng** England, **fra** France … (+12) | Heavy Cavalry | 300 | — | 37.5 | 50.0 | 300.0 | 300.0 | 60.0 | 300.0 |
| `reiter` | **aus** Austria, **bav** Bavaria, **den** Denmark, **eng** England, **fra** France … (+9) | Heavy Cavalry | 300 | — | 37.5 | 75.0 | 75.0 | 300.0 | 300.0 | 300.0 |
| `reiterswe` | **swe** Sweden | Heavy Cavalry | 300 | — | 37.5 | 42.9 | 100.0 | 300.0 | 100.0 | 300.0 |
| `mameluke` | **alg** Algeria | Heavy Cavalry | 280 | — | 31.1 | 40.0 | 31.1 | 280.0 | 140.0 | 28.0 |
| `spakh` | **tur** Turkey | Heavy Cavalry | 230 | — | 23.0 | 25.6 | 23.0 | 230.0 | 28.8 | 23.0 |
| `wingedhussar` | **pol** Poland | Light Cavalry | 225 | — | 25.0 | 28.1 | 45.0 | 225.0 | 225.0 | 225.0 |
| `swordsmansco` | **sco** Scotland | Light Infantry | 180 | — | 20.0 | 22.5 | 22.5 | 180.0 | 45.0 | 180.0 |
| `officer` | **aus** Austria, **bav** Bavaria, **den** Denmark, **eng** England, **fra** France … (+11) | Light Infantry | 125 | — | 15.6 | 15.6 | 25.0 | 125.0 | 125.0 | 125.0 |
| `pikeman` | **spa** Spain | Light Infantry | 100 | — | 14.3 | 16.7 | 25.0 | 100.0 | 100.0 | 100.0 |
| `pikemanpor` | **por** Portugal | Light Infantry | 100 | — | 10.0 | 11.1 | 11.1 | 100.0 | 16.7 | 10.0 |
| `pikemanspa` | **spa** Spain | Light Infantry | 100 | — | 14.3 | 16.7 | 25.0 | 100.0 | 100.0 | 100.0 |
| `roundshier` | **aus** Austria | Light Infantry | 100 | — | 14.3 | 14.3 | 33.3 | 100.0 | 100.0 | 100.0 |
| `pikeman` | **aus** Austria, **bav** Bavaria, **den** Denmark, **eng** England, **fra** France … (+7) | Light Infantry | 90 | — | 12.9 | 11.2 | 15.0 | 90.0 | 22.5 | 90.0 |
| `pikemanswi` | **swi** Switzerland | Light Infantry | 90 | — | 12.9 | 12.9 | 22.5 | 90.0 | 22.5 | 90.0 |
| `pikemanrus` | **eng** Russia | Light Infantry | 85 | — | 10.6 | 9.4 | 14.2 | 85.0 | 14.2 | 85.0 |
| `roundshierdip` | all 21 | Light Infantry | 75 | — | 15.0 | 10.7 | 37.5 | 75.0 | 75.0 | 75.0 |
| `musketeerspa` | **spa** Spain | Shooter | 85 | — | 12.1 | 10.6 | 17.0 | 85.0 | 28.3 | 85.0 |
| `musketeeraus` | **aus** Austria | Shooter | 55 | — | 6.9 | 6.9 | 11.0 | 55.0 | 11.0 | 55.0 |

## §4. Notes and Disclaimers

- **Melee weapons (pause = 0)** - DPS does not count. In the code, melee damage is dealt by an animation frame trigger (`onaclanimationreachedwork`), cycle ~25-32 frames ≈ 1 hit/g-sec. The exact value requires empirical measurement (FPS of animations has not been empirically confirmed).
- **Squad bonuses** ignored. `fAddDamage` (offensive) and `fAddShield`/`fAddShieldHold` (wall mode) can add up to +50% damage and up to +50 EHP - but they are formation/condition dependent, not unit specific. The comparison in this table is base vs base stats.
- **`mortarball` / `firearrow`** - individual kind values, without a corresponding protection field. Included in DPS, but not shown in §3 EHP (no protection).
- **Weapon `heal`** for the priest is excluded from all calculations - this is a non-aggressive ability.
- **Speed ​​= 32** on infantry is `gc_obj_speed_default`. Real Peasant Speed ​​(`gc_obj_speed_peasant=40`) **commented out** [^3], defaults to `objbase.speed:=1`. The numbers in the speed column are a table of constants [^4], that is, _declared_ values ​​that have not been verified empirically.
- **Real time.** If you play at fast speed (×1.4) - multiply all DPS from the g-sec column by 1.4. By default (×1.0) - do not multiply.

---

Generated from `data.json`. For regeneration:
```
python compute/compute_combat_stats.py
```
## Sources

All links are relative to `data/scripts/` in the Cossacks 3 installation.

[^1]: `_misc_DoDamage` - subtracts protection and triggers a headshot - `lib/miscext2.script:380, 434`.

[^2]: rule min damage = 1 - `lib/miscext2.script:381`.

[^3]: commented out `objbase.speed := gc_obj_speed_peasant` - `lib/unit.script:1192`.

[^4]: table `gc_obj_speed_*` - `dmscript.global:603-620`.
