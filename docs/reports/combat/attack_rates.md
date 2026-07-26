# Cossacks 3 — Скорость атаки (per-unit)

**Производный** отчёт. Считается из `data.json` + `derived/animations.json` скриптом [`compute/compute_attack_rates.py`](../../../compute/compute_attack_rates.py).

## Модель

Cossacks 3 не использует общую систему «атаки в секунду». Вместо неё:

```
ranged (weapon.pause_sec > 0):   cycle = pause_sec
melee  (weapon.pause_sec = 0):   cycle = duration of attack0 animation
attacks_per_g_sec = 1 / cycle
attacks_per_real_sec @ fast = 1 / cycle × 1.4
```

Для melee длительность `attack0` варьируется 11..33 кадра между юнитами (median 15). Источник: `data/animations/aaf/<sid>.aaf` → `derived/animations.json`.

## §1. Скорость атаки по юнитам

Одна строка на уникальный набор статов (юнит может присутствовать в нескольких нациях с одинаковыми параметрами — тогда `nations` = список).

**Колонки:**
- **cycle_g** — длительность одного полного цикла атаки в **игровых** секундах. Для ranged = `weapon.pause_sec`. Для melee = длительность анимации `attack0` из `data/animations/aaf/<sid>.aaf`.
- **src** — откуда взято: `pause` (поле оружия), `anim` (анимация), `fallback` (нет .aaf — взят медианный 15-frame swing).
- **att/g-sec** — атак в игровую секунду = `1 / cycle_g`.
- **att/real-sec @ fast** — то же × 1.4 (gc_settings_gamespeed_2).

Сортировка: ranged → melee, внутри — по убыванию частоты атаки.

| sid | usage | weapon | dmg | range_t | cycle_g | src | att/g-sec | att/real @ fast | nations |
| --- | --- | --- | ---: | ---: | ---: | --- | ---: | ---: | --- |
| `battleship` | Battleship | cannonball #0 | 1800 | 36.56 | 0.62 | pause | 1.61 | 2.26 | alg, aus, bav, den … (+16) |
| `archerdip` | Archer | firearrow #1 | 100 | 14.06 | 0.78 | pause | 1.28 | 1.79 | all |
| `archerturdip` | Archer | firearrow #1 | 100 | 14.06 | 0.78 | pause | 1.28 | 1.79 | all |
| `galley` | Galley | mortarball #1 | 1000 | 58.13 | 1.56 | pause | 0.64 | 0.90 | alg, aus, bav, den … (+16) |
| `tatar` | Archer | arrow #0 | 15 | 20.63 | 1.56 | pause | 0.64 | 0.90 | tur |
| `xebec` | Frigate | cannonball #0 | 1800 | 31.88 | 1.56 | pause | 0.64 | 0.90 | alg, tur |
| `multicannon` | Multi-cannon | cannister #0 | 500 | 13.13 | 1.88 | pause | 0.53 | 0.74 | aus, bav, den, eng … (+13) |
| `dragoon18dip` | Shooter | bullet #0 | 18 | 15.0 | 2.25 | pause | 0.44 | 0.62 | all |
| `lightcavalrydip` | Shooter | bullet #0 | 18 | 15.0 | 2.25 | pause | 0.44 | 0.62 | all |
| `archer` | Archer | arrow #0 | 15 | 15.0 | 2.34 | pause | 0.43 | 0.60 | alg |
| `chaika` | Yacht | cannonball #0 | 1000 | 20.63 | 2.34 | pause | 0.43 | 0.60 | ukr |
| `frigate` | Frigate | cannonball #0 | 1800 | 30.94 | 2.34 | pause | 0.43 | 0.60 | aus, bav, den, eng … (+14) |
| `grenadier` | Grenadier | mortarball #2 | 110 | 9.38 | 2.34 | pause | 0.43 | 0.60 | aus, eng, fra, net … (+9) |
| `grenadierbav` | Grenadier | mortarball #2 | 110 | 9.38 | 2.34 | pause | 0.43 | 0.60 | bav |
| `grenadierden` | Grenadier | mortarball #2 | 110 | 9.38 | 2.34 | pause | 0.43 | 0.60 | den |
| `grenadierpru` | Grenadier | mortarball #2 | 110 | 9.38 | 2.34 | pause | 0.43 | 0.60 | pru |
| `grenadiersax` | Grenadier | mortarball #2 | 110 | 9.38 | 2.34 | pause | 0.43 | 0.60 | sax |
| `archerdip` | Archer | arrow #0 | 25 | 13.13 | 2.50 | pause | 0.40 | 0.56 | all |
| `archerturdip` | Archer | arrow #0 | 25 | 13.13 | 2.50 | pause | 0.40 | 0.56 | all |
| `archertur` | Archer | arrow #0 | 20 | 16.88 | 2.66 | pause | 0.38 | 0.53 | tur |
| `framegun` | Cannon | cannonball #0 | 500 | 33.75 | 2.81 | pause | 0.36 | 0.50 | sco |
| `grenadierhun` | Grenadier | mortarball #2 | 110 | 11.25 | 2.81 | pause | 0.36 | 0.50 | hun |
| `archersco` | Archer | arrow #0 | 20 | 18.75 | 3.12 | pause | 0.32 | 0.45 | sco |
| `gauduk` | Shooter | bullet #1 | 9 | 14.06 | 3.12 | pause | 0.32 | 0.45 | hun |
| `grenadierdip` | Grenadier | mortarball #2 | 200 | 7.5 | 3.12 | pause | 0.32 | 0.45 | all |
| `musketeerpol` | Shooter | bullet #1 | 9 | 13.13 | 3.12 | pause | 0.32 | 0.45 | pol |
| `musketeernet` | Shooter | bullet #1 | 10 | 15.0 | 3.75 | pause | 0.27 | 0.37 | net |
| `archer` | Archer | firearrow #1 | 150 | 11.25 | 3.91 | pause | 0.26 | 0.36 | alg |
| `serdiuk` | Shooter | bullet #1 | 12 | 16.88 | 4.06 | pause | 0.25 | 0.34 | ukr |
| `archersco` | Archer | firearrow #1 | 150 | 18.75 | 4.38 | pause | 0.23 | 0.32 | sco |
| `archertur` | Archer | firearrow #1 | 150 | 16.88 | 4.38 | pause | 0.23 | 0.32 | tur |
| `grenadierpru` | Grenadier | bullet #1 | 16 | 16.88 | 4.38 | pause | 0.23 | 0.32 | pru |
| `musketeer18sax` | Shooter | bullet #1 | 19 | 16.88 | 4.38 | pause | 0.23 | 0.32 | sax |
| `dragoon18fra` | Mounted Shooter | bullet #0 | 10 | 15.0 | 4.69 | pause | 0.21 | 0.30 | fra |
| `galley` | Galley | cannonball #0 | 100 | 22.5 | 4.69 | pause | 0.21 | 0.30 | alg, aus, bav, den … (+16) |
| `grenadierdip` | Grenadier | bullet #1 | 16 | 15.0 | 4.69 | pause | 0.21 | 0.30 | all |
| `jannisary` | Shooter | bullet #1 | 12 | 15.94 | 4.69 | pause | 0.21 | 0.30 | tur |
| `musketeer` | Shooter | bullet #1 | 12 | 15.0 | 4.69 | pause | 0.21 | 0.30 | bav, den, eng, fra … (+7) |
| `musketeer18` | Shooter | bullet #1 | 16 | 16.88 | 4.69 | pause | 0.21 | 0.30 | aus, eng, fra, hun … (+9) |
| `musketeer18pru` | Shooter | bullet #1 | 22 | 17.81 | 4.69 | pause | 0.21 | 0.30 | pru |
| `musketeersco` | Shooter | bullet #1 | 12 | 15.94 | 4.69 | pause | 0.21 | 0.30 | sco |
| `pandur` | Shooter | bullet #1 | 17 | 16.88 | 4.69 | pause | 0.21 | 0.30 | aus |
| `strelet` | Shooter | bullet #0 | 12 | 13.13 | 4.69 | pause | 0.21 | 0.30 | rus |
| `tatar` | Archer | firearrow #1 | 140 | 20.63 | 4.69 | pause | 0.21 | 0.30 | tur |
| `dragoon18net` | Mounted Shooter | bullet #0 | 17 | 15.94 | 5.00 | pause | 0.20 | 0.28 | net |
| `dragoon18pie` | Mounted Shooter | bullet #0 | 19 | 16.88 | 5.00 | pause | 0.20 | 0.28 | pie |
| `dragoonpol` | Mounted Shooter | bullet #0 | 13 | 15.94 | 5.00 | pause | 0.20 | 0.28 | pol |
| `highlander` | Shooter | bullet #1 | 16 | 15.94 | 5.00 | pause | 0.20 | 0.28 | eng |
| `musketeeraus` | Shooter | bullet #0 | 12 | 15.0 | 5.00 | pause | 0.20 | 0.28 | aus |
| `pandurhun` | Shooter | bullet #1 | 19 | 18.75 | 5.00 | pause | 0.20 | 0.28 | hun |
| `dragoon18` | Mounted Shooter | bullet #0 | 19 | 16.88 | 5.31 | pause | 0.19 | 0.26 | aus, bav, den, eng … (+9) |
| `grenadier` | Grenadier | bullet #1 | 16 | 16.88 | 5.31 | pause | 0.19 | 0.26 | aus, eng, fra, net … (+9) |
| `grenadierbav` | Grenadier | bullet #1 | 19 | 16.88 | 5.31 | pause | 0.19 | 0.26 | bav |
| `grenadierhun` | Grenadier | bullet #1 | 16 | 16.88 | 5.31 | pause | 0.19 | 0.26 | hun |
| `grenadiersax` | Grenadier | bullet #1 | 19 | 17.81 | 5.31 | pause | 0.19 | 0.26 | sax |
| `lightcavalry` | Mounted Shooter | bullet #0 | 14 | 18.75 | 5.31 | pause | 0.19 | 0.26 | hun |
| `dragoon` | Mounted Shooter | bullet #0 | 15 | 15.0 | 5.62 | pause | 0.18 | 0.25 | aus, bav, den, eng … (+12) |
| `chasseur` | Shooter | bullet #1 | 20 | 19.69 | 5.94 | pause | 0.17 | 0.24 | fra |
| `grenadierden` | Grenadier | bullet #1 | 19 | 16.88 | 5.94 | pause | 0.17 | 0.24 | den |
| `jagerpor` | Shooter | bullet #1 | 10 | 15.0 | 5.94 | pause | 0.17 | 0.24 | por |
| `musketeer18bav` | Shooter | bullet #1 | 22 | 17.81 | 5.94 | pause | 0.17 | 0.24 | bav |
| `musketeer18den` | Shooter | bullet #1 | 29 | 16.88 | 5.94 | pause | 0.17 | 0.24 | den |
| `musketeerspa` | Shooter | bullet #0 | 15 | 15.94 | 5.94 | pause | 0.17 | 0.24 | spa |
| `jagerswi` | Shooter | bullet #1 | 20 | 22.5 | 6.88 | pause | 0.15 | 0.20 | swi |
| `kingmusketeer` | Mounted Shooter | bullet #0 | 43 | 13.13 | 6.88 | pause | 0.15 | 0.20 | fra |
| `mortar` | Super Mortar | mortarball #0 | 200 | 48.75 | 7.81 | pause | 0.13 | 0.18 | all |
| `cannon` | Cannon | cannonball #0 | 1800 | 40.5 | 10.94 | pause | 0.09 | 0.13 | all |
| `yacht` | Yacht | cannonball #0 | 1000 | 20.63 | 10.94 | pause | 0.09 | 0.13 | aus, bav, den, eng … (+14) |
| `yachttur` | Yacht | cannonball #0 | 30 | 18.75 | 12.50 | pause | 0.08 | 0.11 | tur |
| `howitzer` | Mortar | cannonball #0 | 4000 | 26.25 | 18.75 | pause | 0.05 | 0.07 | all |
| `pikeman18` | Light Infantry | pike #0 | 9 | 1.88 | 0.28 | anim | 3.56 | 4.98 | aus, bav, den, eng … (+12) |
| `pikemanrus` | Light Infantry | pike #0 | 8 | 1.69 | 0.31 | anim | 3.20 | 4.48 | rus |
| `pikeman18swe` | Light Infantry | pike #0 | 11 | 1.88 | 0.38 | anim | 2.67 | 3.73 | swe |
| `pikemanpol` | Light Infantry | pike #0 | 8 | 2.06 | 0.38 | anim | 2.67 | 3.73 | pol |
| `pikemanpor` | Light Infantry | pike #0 | 9 | 1.88 | 0.38 | anim | 2.67 | 3.73 | por |
| `pikemantur` | Light Infantry | pike #0 | 9 | 2.06 | 0.38 | anim | 2.67 | 3.73 | alg, tur |
| `roundshier` | Light Infantry | sword #0 | 6 | 1.13 | 0.38 | anim | 2.67 | 3.73 | aus |
| `sipahi` | Heavy Cavalry | sword #0 | 15 | 1.22 | 0.38 | anim | 2.67 | 3.73 | tur |
| `vityaz` | Heavy Cavalry | pike #0 | 14 | 1.22 | 0.38 | anim | 2.67 | 3.73 | rus |
| `wingedhussar` | Light Cavalry | pike #0 | 14 | 1.88 | 0.38 | anim | 2.67 | 3.73 | pol |
| `cossacksich` | Light Cavalry | sword #0 | 13 | 1.22 | 0.41 | anim | 2.46 | 3.45 | ukr |
| `swordsmansco` | Light Infantry | sword #0 | 10 | 1.13 | 0.41 | anim | 2.46 | 3.45 | sco |
| `cossackdon` | Heavy Cavalry | pike #0 | 13 | 1.88 | 0.44 | anim | 2.29 | 3.20 | rus |
| `cossackregister` | Heavy Cavalry | pike #0 | 12 | 1.88 | 0.44 | anim | 2.29 | 3.20 | ukr |
| `croat` | Light Cavalry | sword #0 | 9 | 1.22 | 0.44 | anim | 2.29 | 3.20 | aus |
| `cuirassier` | Heavy Cavalry | pike #0 | 14 | 1.22 | 0.44 | anim | 2.29 | 3.20 | aus, bav, den, eng … (+13) |
| `guardcavalrysax` | Heavy Cavalry | pike #0 | 15 | 1.22 | 0.44 | anim | 2.29 | 3.20 | sax |
| `hackapell` | Light Cavalry | pike #0 | 12 | 1.22 | 0.44 | anim | 2.29 | 3.20 | swe |
| `hussar` | Light Cavalry | sword #0 | 12 | 1.22 | 0.44 | anim | 2.29 | 3.20 | aus, bav, den, eng … (+10) |
| `hussarhun` | Light Cavalry | sword #0 | 10 | 1.22 | 0.44 | anim | 2.29 | 3.20 | hun |
| `hussarpru` | Light Cavalry | sword #0 | 9 | 1.22 | 0.44 | anim | 2.29 | 3.20 | pru |
| `hussarswi` | Light Cavalry | sword #0 | 14 | 1.22 | 0.44 | anim | 2.29 | 3.20 | swi |
| `lancersco` | Heavy Cavalry | pike #0 | 11 | 1.88 | 0.44 | anim | 2.29 | 3.20 | sco |
| `lightinfantry` | Light Infantry | sword #0 | 5 | 0.94 | 0.44 | anim | 2.29 | 3.20 | alg, tur |
| `mameluke` | Heavy Cavalry | pike #0 | 16 | 1.88 | 0.44 | anim | 2.29 | 3.20 | alg |
| `musketeer18` | Shooter | pike #0 | 10 | 1.22 | 0.44 | anim | 2.29 | 3.20 | aus, eng, fra, hun … (+9) |
| `officer` | Light Infantry | pike #0 | 30 | 1.22 | 0.44 | anim | 2.29 | 3.20 | aus, bav, den, eng … (+12) |
| `officerrus` | Light Infantry | pike #0 | 40 | 1.22 | 0.44 | anim | 2.29 | 3.20 | rus |
| `raidersco` | Light Cavalry | sword #0 | 11 | 1.22 | 0.44 | anim | 2.29 | 3.20 | sco |
| `reiter` | Heavy Cavalry | pike #0 | 15 | 1.22 | 0.44 | anim | 2.29 | 3.20 | aus, bav, den, eng … (+10) |
| `reiterpol` | Heavy Cavalry | sword #0 | 9 | 1.22 | 0.44 | anim | 2.29 | 3.20 | pol |
| `reiterswe` | Heavy Cavalry | pike #0 | 14 | 1.22 | 0.44 | anim | 2.29 | 3.20 | swe |
| `spakh` | Heavy Cavalry | pike #0 | 15 | 1.88 | 0.44 | anim | 2.29 | 3.20 | tur |
| `cossacksichdip` | Light Cavalry | sword #0 | 8 | 1.22 | 0.47 | fallback | 2.13 | 2.99 | all |
| `grenadierdip` | Grenadier | pike #0 | 30 | 1.5 | 0.47 | fallback | 2.13 | 2.99 | all |
| `hetman` | Heavy Cavalry | pike #0 | 70 | 1.22 | 0.47 | anim | 2.13 | 2.99 | ukr |
| `lightinfantrydip` | Light Infantry | sword #0 | 16 | 0.94 | 0.47 | fallback | 2.13 | 2.99 | all |
| `pikeman` | Light Infantry | pike #0 | 8 | 1.88 | 0.47 | anim | 2.13 | 2.99 | aus, bav, den, eng … (+8) |
| `pikeman` | Light Infantry | pike #0 | 10 | 1.88 | 0.47 | anim | 2.13 | 2.99 | spa |
| `pikemansco` | Light Infantry | pike #0 | 9 | 1.88 | 0.47 | anim | 2.13 | 2.99 | sco |
| `pikemanspa` | Light Infantry | pike #0 | 10 | 1.88 | 0.47 | anim | 2.13 | 2.99 | spa |
| `pikemanswi` | Light Infantry | pike #0 | 10 | 1.88 | 0.47 | anim | 2.13 | 2.99 | swi |
| `roundshierdip` | Light Infantry | sword #0 | 6 | 1.13 | 0.47 | fallback | 2.13 | 2.99 | all |
| `grenadier` | Grenadier | pike #0 | 18 | 1.5 | 0.50 | anim | 2.00 | 2.80 | aus, eng, fra, net … (+9) |
| `grenadierbav` | Grenadier | pike #0 | 14 | 1.5 | 0.50 | anim | 2.00 | 2.80 | bav |
| `grenadierden` | Grenadier | pike #0 | 22 | 1.5 | 0.50 | anim | 2.00 | 2.80 | den |
| `grenadierhun` | Grenadier | pike #0 | 30 | 1.5 | 0.50 | anim | 2.00 | 2.80 | hun |
| `grenadierpru` | Grenadier | pike #0 | 18 | 1.5 | 0.50 | anim | 2.00 | 2.80 | pru |
| `grenadiersax` | Grenadier | pike #0 | 22 | 1.5 | 0.50 | anim | 2.00 | 2.80 | sax |
| `musketeer18bav` | Shooter | pike #0 | 5 | 1.59 | 0.53 | anim | 1.88 | 2.64 | bav |
| `musketeer18den` | Shooter | pike #0 | 8 | 1.59 | 0.53 | anim | 1.88 | 2.64 | den |
| `musketeer18pru` | Shooter | pike #0 | 10 | 1.59 | 0.53 | anim | 1.88 | 2.64 | pru |
| `musketeer18sax` | Shooter | pike #0 | 7 | 1.22 | 0.53 | anim | 1.88 | 2.64 | sax |
| `officer18` | Light Infantry | pike #0 | 50 | 1.22 | 0.56 | anim | 1.78 | 2.49 | aus, bav, den, eng … (+13) |
| `officersco` | Light Infantry | pike #0 | 40 | 1.22 | 0.56 | anim | 1.78 | 2.49 | sco |
| `officertur` | Light Infantry | pike #0 | 30 | 1.22 | 0.56 | anim | 1.78 | 2.49 | alg, tur |
| `peaaus` | Peasant | sword #0 | 20 | 1.22 | 0.56 | anim | 1.78 | 2.49 | aus, bav, pru, sax, swi |
| `peaeng` | Peasant | sword #0 | 20 | 1.22 | 0.56 | anim | 1.78 | 2.49 | den, eng, fra, net, swe |
| `peapol` | Peasant | sword #0 | 20 | 1.22 | 0.56 | anim | 1.78 | 2.49 | hun, pol |
| `pearus` | Peasant | sword #0 | 20 | 1.22 | 0.56 | anim | 1.78 | 2.49 | rus |
| `peasco` | Peasant | sword #0 | 20 | 1.22 | 0.56 | anim | 1.78 | 2.49 | sco |
| `peaspa` | Peasant | sword #0 | 20 | 1.22 | 0.56 | anim | 1.78 | 2.49 | pie, por, spa, ven |
| `peatur` | Peasant | sword #0 | 20 | 1.22 | 0.56 | anim | 1.78 | 2.49 | alg, tur |
| `peaukr` | Peasant | sword #0 | 20 | 1.22 | 0.56 | anim | 1.78 | 2.49 | ukr |

## §2. Сводка по типу оружия

Min / median / max длительности цикла для каждого `kind`. Помогает увидеть «насколько медленнее одна арбалетная атака другой» внутри класса и понять, где апгрейды `attpauseperc` дают больше всего профита.

| kind | n | min cycle (g-sec) | median | max | min att/real @ fast |
| --- | ---: | ---: | ---: | ---: | ---: |
| arrow | 6 | 1.56 | 2.50 | 3.12 | 0.90 |
| bullet | 38 | 2.25 | 5.00 | 6.88 | 0.62 |
| cannister | 1 | 1.88 | 1.88 | 1.88 | 0.74 |
| cannonball | 10 | 0.62 | 4.69 | 18.75 | 2.26 |
| firearrow | 6 | 0.78 | 4.38 | 4.69 | 1.79 |
| mortarball | 9 | 1.56 | 2.34 | 7.81 | 0.90 |
| pike | 41 | 0.28 | 0.44 | 0.56 | 4.98 |
| sword | 23 | 0.38 | 0.44 | 0.56 | 3.73 |

## §3. Замечания

- **Pause vs swing.** В Cossacks 3 для дистанционного оружия `pause` — это полный цикл (анимация выстрела внутри pause). Для melee `pause=0` и цикл равен длине самой анимации `attack0`.
- **Fallback** для melee = 15 кадров (≈ 0.4688 g-sec, медиана по всем юнитам с .aaf). Применяется если для конкретного `sid` в `data/animations/aaf/` нет файла или нет трека `attack0`.
- **Multi-weapon юниты.** Musketeer18 (bayonet + musket), архер с горящими стрелами и т.п. — у них в таблице по строке на оружие, колонка `weapon` показывает `#index`.
- **`heal` исключён.** Священник = неагрессивный, не входит в боевой DPS-расчёт.
- **Real vs game.** Вся игровая логика (анимации, pause) — в **игровых** секундах. Чтобы получить реальное время на скорости fast, делите g-sec на 1.4 (или умножайте rate на 1.4).
- **Cooldown апгрейды.** `attpauseperc` (см. [`reference/05_upgrades/README.md`](../../reference/05_upgrades/README.md)) уменьшает только pause у ranged. Melee swing не апгрейдится — он привязан к анимации.

---

Перегенерация: `python compute/compute_attack_rates.py`