# Cossacks 3 — DPS / EHP / armor metrics

**Производный** файл (расчётный, не извлечение). Считается из `docs/data.json` скриптом [`compute/compute_combat_stats.py`](../../compute/compute_combat_stats.py).

## Формула урона

Источник: [`miscext2.script:380`, `434`](<C:/Program Files (x86)/Steam/steamapps/common/Cossacks 3/data/scripts/lib/miscext2.script>) (damage application).

```
applied_damage = max(1, base_damage + squad_bonus - target.protection[weapon_kind])
target.hp     -= applied_damage
```

`gc_settings_gamespeed_2 = 14` (fast). Game-time → real-time: `×1.4`. 
Реальный DPS = game-DPS × game_speed.

## §1. Сводная таблица боевых юнитов

Группировка: одна строка на каждый уникальный набор статов. Колонка **nations** — нации, в которых этот юнит с этими статами доступен (`all` = все 21). Если у юнита разные значения у разных наций (например `pikeman/pol` имеет половину брони от стандарта) — это разные строки.

Колонки: HP, скорость (px/g-sec; 32 = крестьянин), основное оружие (урон / пауза / дальность / тип), DPS @ game-sec, DPS @ real-sec (×1.4 fast), protections (только ненулевые), shield. Юнит может иметь ≥1 оружия — показано **сильнейшее по соотношению урон/пауза**.

| sid | нации | usage | HP | speed | primary weapon | DPS g-s | DPS real | protections |
| --- | --- | --- | ---: | ---: | --- | ---: | ---: | --- |
| `tatar` | tur | Archer | 185 | 32 | 140d / 4.69s / 20.63t [firearrow] | 29.85 | 41.79 | — |
| `archersco` | sco | Archer | 150 | 32 | 150d / 4.38s / 18.75t [firearrow] | 34.25 | 47.95 | — |
| `archertur` | tur | Archer | 65 | 32 | 150d / 4.38s / 16.88t [firearrow] | 34.25 | 47.95 | — |
| `archer` | alg | Archer | 40 | 32 | 150d / 3.91s / 11.25t [firearrow] | 38.36 | 53.7 | — |
| `archerdip` | all | Archer | 20 | 32 | 100d / 0.78s / 14.06t [firearrow] | 128.21 | 179.49 | — |
| `archerturdip` | all | Archer | 20 | 32 | 100d / 0.78s / 14.06t [firearrow] | 128.21 | 179.49 | — |
| `cannon` | all | Cannon | 9000 | 20 | 1800d / 10.94s / 40.5t [cannonball] | 164.53 | 230.34 | shield=75 |
| `framegun` | sco | Cannon | 3000 | 20 | 500d / 2.81s / 33.75t [cannonball] | 177.94 | 249.12 | shield=50 |
| `grenadierbav` | bav | Grenadier | 125 | 32 | 110d / 2.34s / 9.38t [mortarball] | 47.01 | 65.81 | — |
| `grenadierden` | den | Grenadier | 125 | 32 | 110d / 2.34s / 9.38t [mortarball] | 47.01 | 65.81 | — |
| `grenadierhun` | hun | Grenadier | 125 | 32 | 110d / 2.81s / 11.25t [mortarball] | 39.15 | 54.81 | — |
| `grenadierpru` | pru | Grenadier | 125 | 32 | 110d / 2.34s / 9.38t [mortarball] | 47.01 | 65.81 | — |
| `grenadier` | aus, eng, fra, net, pie … (+8 more) | Grenadier | 120 | 32 | 110d / 2.34s / 9.38t [mortarball] | 47.01 | 65.81 | — |
| `grenadiersax` | sax | Grenadier | 100 | 32 | 110d / 2.34s / 9.38t [mortarball] | 47.01 | 65.81 | — |
| `grenadierdip` | all | Grenadier | 30 | 32 | 200d / 3.12s / 7.5t [mortarball] | 64.1 | 89.74 | — |
| `vityaz` | rus | Heavy Cavalry | 380 | 56 | 14d / 0 (melee) / 1.22t [pike] | — | — | pike=2, sword=4, bullet=3, cannister=160, arrow=17, cannonball=40 |
| `sipahi` | tur | Heavy Cavalry | 360 | 56 | 15d / 0 (melee) / 1.22t [sword] | — | — | pike=3, sword=7, bullet=4, cannister=225, arrow=24, cannonball=60 |
| `guardcavalrysax` | sax | Heavy Cavalry | 320 | 56 | 15d / 0 (melee) / 1.22t [pike] | — | — | pike=2, sword=5, bullet=9, cannister=150, arrow=9, cannonball=70 |
| `hetman` | ukr | Heavy Cavalry | 320 | 56 | 70d / 0 (melee) / 1.22t [pike] | — | — | sword=1, bullet=3, cannister=75, arrow=3, cannonball=15 |
| `lancersco` | sco | Heavy Cavalry | 320 | 56 | 11d / 0 (melee) / 1.88t [pike] | — | — | — |
| `cuirassier` | aus, bav, den, eng, fra … (+12 more) | Heavy Cavalry | 300 | 56 | 14d / 0 (melee) / 1.22t [pike] | — | — | pike=2, sword=4, bullet=10, cannister=160, arrow=5, cannonball=80 |
| `reiter` | aus, bav, den, eng, fra … (+9 more) | Heavy Cavalry | 300 | 56 | 15d / 0 (melee) / 1.22t [pike] | — | — | pike=2, sword=6, bullet=6, cannister=190, arrow=15, cannonball=40 |
| `reiterswe` | swe | Heavy Cavalry | 300 | 56 | 14d / 0 (melee) / 1.22t [pike] | — | — | pike=2, sword=3, bullet=7, cannister=140, arrow=7, cannonball=35 |
| `mameluke` | alg | Heavy Cavalry | 280 | 56 | 16d / 0 (melee) / 1.88t [pike] | — | — | pike=1, sword=3, bullet=1, cannister=75, arrow=8 |
| `cossackregister` | ukr | Heavy Cavalry | 250 | 56 | 12d / 0 (melee) / 1.88t [pike] | — | — | — |
| `spakh` | tur | Heavy Cavalry | 230 | 56 | 15d / 0 (melee) / 1.88t [pike] | — | — | sword=1, cannister=10, arrow=2 |
| `cossackdon` | rus | Heavy Cavalry | 220 | 56 | 13d / 0 (melee) / 1.88t [pike] | — | — | — |
| `reiterpol` | pol | Heavy Cavalry | 190 | 56 | 9d / 0 (melee) / 1.22t [sword] | — | — | — |
| `raidersco` | sco | Light Cavalry | 280 | 96 | 11d / 0 (melee) / 1.22t [sword] | — | — | — |
| `hussarswi` | swi | Light Cavalry | 265 | 96 | 14d / 0 (melee) / 1.22t [sword] | — | — | — |
| `croat` | aus | Light Cavalry | 260 | 96 | 9d / 0 (melee) / 1.22t [sword] | — | — | — |
| `cossacksich` | ukr | Light Cavalry | 250 | 96 | 13d / 0 (melee) / 1.22t [sword] | — | — | — |
| `hussarhun` | hun | Light Cavalry | 250 | 96 | 10d / 0 (melee) / 1.22t [sword] | — | — | — |
| `hackapell` | swe | Light Cavalry | 245 | 96 | 12d / 0 (melee) / 1.22t [pike] | — | — | — |
| `hussarpru` | pru | Light Cavalry | 240 | 96 | 9d / 0 (melee) / 1.22t [sword] | — | — | — |
| `hussar` | aus, bav, den, eng, fra … (+9 more) | Light Cavalry | 230 | 96 | 12d / 0 (melee) / 1.22t [sword] | — | — | — |
| `wingedhussar` | pol | Light Cavalry | 225 | 96 | 14d / 0 (melee) / 1.88t [pike] | — | — | pike=1, sword=2, bullet=5, cannister=160, arrow=10, cannonball=30 |
| `cossacksichdip` | all | Light Cavalry | 150 | 96 | 8d / 0 (melee) / 1.22t [sword] | — | — | — |
| `swordsmansco` | sco | Light Infantry | 180 | 32 | 10d / 0 (melee) / 1.13t [sword] | — | — | pike=1, sword=2, bullet=2, cannister=110, arrow=6, cannonball=10 |
| `officersco` | sco | Light Infantry | 150 | 32 | 40d / 0 (melee) / 1.22t [pike] | — | — | — |
| `officer` | aus, bav, den, eng, fra … (+11 more) | Light Infantry | 125 | 32 | 30d / 0 (melee) / 1.22t [pike] | — | — | pike=2, sword=2, bullet=5, cannister=200, arrow=10, cannonball=30 |
| `officer18` | aus, bav, den, eng, fra … (+12 more) | Light Infantry | 125 | 32 | 50d / 0 (melee) / 1.22t [pike] | — | — | — |
| `officerrus` | rus | Light Infantry | 125 | 32 | 40d / 0 (melee) / 1.22t [pike] | — | — | — |
| `officertur` | alg, tur | Light Infantry | 125 | 32 | 30d / 0 (melee) / 1.22t [pike] | — | — | — |
| `pikeman18swe` | swe | Light Infantry | 110 | 32 | 11d / 0 (melee) / 1.88t [pike] | — | — | — |
| `drummer18` | rus | Light Infantry | 100 | 32 | — | — | — | — |
| `drummerrus` | rus | Light Infantry | 100 | 32 | — | — | — | — |
| `mullah` | alg, tur | Light Infantry | 100 | 32 | — | — | — | — |
| `padre` | pie | Light Infantry | 100 | 32 | — | — | — | — |
| `pikeman` | spa | Light Infantry | 100 | 32 | 10d / 0 (melee) / 1.88t [pike] | — | — | pike=3, sword=4, bullet=6, cannister=240, arrow=12, cannonball=50 |
| `pikemanpor` | por | Light Infantry | 100 | 32 | 9d / 0 (melee) / 1.88t [pike] | — | — | sword=1, bullet=1, cannister=25, arrow=4 |
| `pikemansco` | sco | Light Infantry | 100 | 32 | 9d / 0 (melee) / 1.88t [pike] | — | — | — |
| `pikemanspa` | spa | Light Infantry | 100 | 32 | 10d / 0 (melee) / 1.88t [pike] | — | — | pike=3, sword=4, bullet=6, cannister=240, arrow=12, cannonball=50 |
| `pope` | rus, ukr | Light Infantry | 100 | 32 | — | — | — | — |
| `priest` | aus, bav, den, eng, fra … (+11 more) | Light Infantry | 100 | 32 | — | — | — | — |
| `roundshier` | aus | Light Infantry | 100 | 32 | 6d / 0 (melee) / 1.13t [sword] | — | — | pike=3, sword=3, bullet=7, cannister=225, arrow=16, cannonball=80 |
| `pikemantur` | alg, tur | Light Infantry | 95 | 32 | 9d / 0 (melee) / 2.06t [pike] | — | — | — |
| `pikeman` | aus, bav, den, eng, fra … (+7 more) | Light Infantry | 90 | 32 | 8d / 0 (melee) / 1.88t [pike] | — | — | pike=3, sword=2, bullet=4, cannister=210, arrow=6, cannonball=40 |
| `pikemanpol` | pol | Light Infantry | 90 | 32 | 8d / 0 (melee) / 2.06t [pike] | — | — | — |
| `pikemanswi` | swi | Light Infantry | 90 | 32 | 10d / 0 (melee) / 1.88t [pike] | — | — | pike=3, sword=3, bullet=6, cannister=220, arrow=6, cannonball=45 |
| `pikeman18` | aus, bav, den, eng, fra … (+11 more) | Light Infantry | 85 | 32 | 9d / 0 (melee) / 1.88t [pike] | — | — | — |
| `pikemanrus` | rus | Light Infantry | 85 | 32 | 8d / 0 (melee) / 1.69t [pike] | — | — | pike=2, sword=1, bullet=4, cannister=140, arrow=4, cannonball=25 |
| `bagpiper` | eng, sco | Light Infantry | 75 | 32 | — | — | — | — |
| `drummer` | aus, bav, den, eng, fra … (+11 more) | Light Infantry | 75 | 32 | — | — | — | — |
| `drummer18` | aus, bav, den, fra, hun … (+10 more) | Light Infantry | 75 | 32 | — | — | — | — |
| `roundshierdip` | all | Light Infantry | 75 | 32 | 6d / 0 (melee) / 1.13t [sword] | — | — | pike=5, sword=3, bullet=8, cannister=225, arrow=17, cannonball=80 |
| `lightinfantry` | alg, tur | Light Infantry | 55 | 32 | 5d / 0 (melee) / 0.94t [sword] | — | — | — |
| `drummertur` | alg, tur | Light Infantry | 50 | 32 | — | — | — | — |
| `lightinfantrydip` | all | Light Infantry | 50 | 32 | 16d / 0 (melee) / 0.94t [sword] | — | — | — |
| `howitzer` | all | Mortar | 3000 | 20 | 4000d / 18.75s / 26.25t [cannonball] | 213.33 | 298.66 | shield=75 |
| `dragoon18net` | net | Mounted Shooter | 320 | 56 | 17d / 5.0s / 15.94t [bullet] | 3.4 | 4.76 | — |
| `kingmusketeer` | fra | Mounted Shooter | 280 | 56 | 43d / 6.88s / 13.13t [bullet] | 6.25 | 8.75 | — |
| `dragoon18` | aus, bav, den, eng, pol … (+8 more) | Mounted Shooter | 225 | 56 | 19d / 5.31s / 16.88t [bullet] | 3.58 | 5.01 | — |
| `dragoon` | aus, bav, den, eng, fra … (+11 more) | Mounted Shooter | 220 | 56 | 15d / 5.62s / 15.0t [bullet] | 2.67 | 3.74 | — |
| `dragoon18pie` | pie | Mounted Shooter | 200 | 56 | 19d / 5.0s / 16.88t [bullet] | 3.8 | 5.32 | — |
| `dragoonpol` | pol | Mounted Shooter | 185 | 56 | 13d / 5.0s / 15.94t [bullet] | 2.6 | 3.64 | — |
| `lightcavalry` | hun | Mounted Shooter | 175 | 56 | 14d / 5.31s / 18.75t [bullet] | 2.64 | 3.7 | — |
| `dragoon18fra` | fra | Mounted Shooter | 140 | 56 | 10d / 4.69s / 15.0t [bullet] | 2.13 | 2.98 | — |
| `multicannon` | aus, bav, den, eng, fra … (+12 more) | Multi-cannon | 2000 | 16 | 500d / 1.88s / 13.13t [cannister] | 265.96 | 372.34 | shield=50 |
| `highlander` | eng | Shooter | 130 | 32 | 16d / 5.0s / 15.94t [bullet] | 3.2 | 4.48 | — |
| `dragoon18dip` | all | Shooter | 100 | 56 | 18d / 2.25s / 15.0t [bullet] | 8.0 | 11.2 | — |
| `lightcavalrydip` | all | Shooter | 100 | 56 | 18d / 2.25s / 15.0t [bullet] | 8.0 | 11.2 | — |
| `musketeer18` | aus, eng, fra, hun, net … (+8 more) | Shooter | 100 | 32 | 16d / 4.69s / 16.88t [bullet] | 3.41 | 4.77 | — |
| `musketeer18bav` | bav | Shooter | 100 | 32 | 22d / 5.94s / 17.81t [bullet] | 3.7 | 5.18 | — |
| `musketeer18den` | den | Shooter | 100 | 32 | 29d / 5.94s / 16.88t [bullet] | 4.88 | 6.83 | — |
| `musketeer18pru` | pru | Shooter | 100 | 32 | 22d / 4.69s / 17.81t [bullet] | 4.69 | 6.57 | — |
| `musketeer18sax` | sax | Shooter | 90 | 32 | 19d / 4.38s / 16.88t [bullet] | 4.34 | 6.08 | — |
| `musketeersco` | sco | Shooter | 90 | 32 | 12d / 4.69s / 15.94t [bullet] | 2.56 | 3.58 | — |
| `musketeerspa` | spa | Shooter | 85 | 32 | 15d / 5.94s / 15.94t [bullet] | 2.53 | 3.54 | pike=3, sword=2, bullet=5, cannister=210, arrow=7, cannonball=40 |
| `pandur` | aus | Shooter | 85 | 32 | 17d / 4.69s / 16.88t [bullet] | 3.62 | 5.07 | — |
| `serdiuk` | ukr | Shooter | 85 | 32 | 12d / 4.06s / 16.88t [bullet] | 2.96 | 4.14 | — |
| `strelet` | rus | Shooter | 85 | 32 | 12d / 4.69s / 13.13t [bullet] | 2.56 | 3.58 | — |
| `chasseur` | fra | Shooter | 75 | 32 | 20d / 5.94s / 19.69t [bullet] | 3.37 | 4.72 | — |
| `pandurhun` | hun | Shooter | 75 | 32 | 19d / 5.0s / 18.75t [bullet] | 3.8 | 5.32 | — |
| `musketeer` | bav, den, eng, fra, pie … (+6 more) | Shooter | 70 | 32 | 12d / 4.69s / 15.0t [bullet] | 2.56 | 3.58 | — |
| `musketeerpol` | pol | Shooter | 70 | 32 | 9d / 3.12s / 13.13t [bullet] | 2.88 | 4.03 | — |
| `jagerswi` | swi | Shooter | 65 | 32 | 20d / 6.88s / 22.5t [bullet] | 2.91 | 4.07 | — |
| `jannisary` | tur | Shooter | 65 | 32 | 12d / 4.69s / 15.94t [bullet] | 2.56 | 3.58 | — |
| `musketeernet` | net | Shooter | 65 | 32 | 10d / 3.75s / 15.0t [bullet] | 2.67 | 3.74 | — |
| `gauduk` | hun | Shooter | 60 | 32 | 9d / 3.12s / 14.06t [bullet] | 2.88 | 4.03 | — |
| `musketeeraus` | aus | Shooter | 55 | 32 | 12d / 5.0s / 15.0t [bullet] | 2.4 | 3.36 | pike=2, sword=2, bullet=5, cannister=165, arrow=5, cannonball=35 |
| `jagerpor` | por | Shooter | 50 | 32 | 10d / 5.94s / 15.0t [bullet] | 1.68 | 2.35 | — |
| `mortar` | all | Super Mortar | 400 | 24 | 200d / 7.81s / 48.75t [mortarball] | 25.61 | 35.85 | shield=25 |

## §2. Рейтинг DPS — боевые юниты

Все combat-юниты с `pause > 0` (melee с `pause = 0` исключены — урон у них привязан к анимационному циклу, см. §4). DPS считается в game-sec; колонка "DPS real (fast)" — ×1.4 для удобства сравнения с тем, что видно в реальном времени.

| # | sid | нации | usage | HP | weapon kind | урон | пауза, с | дальн., тайл. | DPS g-s | DPS real |
| ---: | --- | --- | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | `multicannon` | aus, bav, den, eng, fra … (+12 more) | Multi-cannon | 2000 | cannister | 500 | 1.88 | 13.13 | 265.96 | 372.34 |
| 2 | `howitzer` | all | Mortar | 3000 | cannonball | 4000 | 18.75 | 26.25 | 213.33 | 298.66 |
| 3 | `framegun` | sco | Cannon | 3000 | cannonball | 500 | 2.81 | 33.75 | 177.94 | 249.12 |
| 4 | `cannon` | all | Cannon | 9000 | cannonball | 1800 | 10.94 | 40.5 | 164.53 | 230.34 |
| 5 | `archerdip` | all | Archer | 20 | firearrow | 100 | 0.78 | 14.06 | 128.21 | 179.49 |
| 6 | `archerturdip` | all | Archer | 20 | firearrow | 100 | 0.78 | 14.06 | 128.21 | 179.49 |
| 7 | `grenadierdip` | all | Grenadier | 30 | mortarball | 200 | 3.12 | 7.5 | 64.1 | 89.74 |
| 8 | `grenadier` | aus, eng, fra, net, pie … (+8 more) | Grenadier | 120 | mortarball | 110 | 2.34 | 9.38 | 47.01 | 65.81 |
| 9 | `grenadierpru` | pru | Grenadier | 125 | mortarball | 110 | 2.34 | 9.38 | 47.01 | 65.81 |
| 10 | `grenadierden` | den | Grenadier | 125 | mortarball | 110 | 2.34 | 9.38 | 47.01 | 65.81 |
| 11 | `grenadiersax` | sax | Grenadier | 100 | mortarball | 110 | 2.34 | 9.38 | 47.01 | 65.81 |
| 12 | `grenadierbav` | bav | Grenadier | 125 | mortarball | 110 | 2.34 | 9.38 | 47.01 | 65.81 |
| 13 | `grenadierhun` | hun | Grenadier | 125 | mortarball | 110 | 2.81 | 11.25 | 39.15 | 54.81 |
| 14 | `archer` | alg | Archer | 40 | firearrow | 150 | 3.91 | 11.25 | 38.36 | 53.7 |
| 15 | `archertur` | tur | Archer | 65 | firearrow | 150 | 4.38 | 16.88 | 34.25 | 47.95 |
| 16 | `archersco` | sco | Archer | 150 | firearrow | 150 | 4.38 | 18.75 | 34.25 | 47.95 |
| 17 | `tatar` | tur | Archer | 185 | firearrow | 140 | 4.69 | 20.63 | 29.85 | 41.79 |
| 18 | `mortar` | all | Super Mortar | 400 | mortarball | 200 | 7.81 | 48.75 | 25.61 | 35.85 |
| 19 | `dragoon18dip` | all | Shooter | 100 | bullet | 18 | 2.25 | 15.0 | 8.0 | 11.2 |
| 20 | `lightcavalrydip` | all | Shooter | 100 | bullet | 18 | 2.25 | 15.0 | 8.0 | 11.2 |
| 21 | `kingmusketeer` | fra | Mounted Shooter | 280 | bullet | 43 | 6.88 | 13.13 | 6.25 | 8.75 |
| 22 | `musketeer18den` | den | Shooter | 100 | bullet | 29 | 5.94 | 16.88 | 4.88 | 6.83 |
| 23 | `musketeer18pru` | pru | Shooter | 100 | bullet | 22 | 4.69 | 17.81 | 4.69 | 6.57 |
| 24 | `musketeer18sax` | sax | Shooter | 90 | bullet | 19 | 4.38 | 16.88 | 4.34 | 6.08 |
| 25 | `dragoon18pie` | pie | Mounted Shooter | 200 | bullet | 19 | 5.0 | 16.88 | 3.8 | 5.32 |
| 26 | `pandurhun` | hun | Shooter | 75 | bullet | 19 | 5.0 | 18.75 | 3.8 | 5.32 |
| 27 | `musketeer18bav` | bav | Shooter | 100 | bullet | 22 | 5.94 | 17.81 | 3.7 | 5.18 |
| 28 | `pandur` | aus | Shooter | 85 | bullet | 17 | 4.69 | 16.88 | 3.62 | 5.07 |
| 29 | `dragoon18` | aus, bav, den, eng, pol … (+8 more) | Mounted Shooter | 225 | bullet | 19 | 5.31 | 16.88 | 3.58 | 5.01 |
| 30 | `musketeer18` | aus, eng, fra, hun, net … (+8 more) | Shooter | 100 | bullet | 16 | 4.69 | 16.88 | 3.41 | 4.77 |
| 31 | `dragoon18net` | net | Mounted Shooter | 320 | bullet | 17 | 5.0 | 15.94 | 3.4 | 4.76 |
| 32 | `chasseur` | fra | Shooter | 75 | bullet | 20 | 5.94 | 19.69 | 3.37 | 4.72 |
| 33 | `highlander` | eng | Shooter | 130 | bullet | 16 | 5.0 | 15.94 | 3.2 | 4.48 |
| 34 | `serdiuk` | ukr | Shooter | 85 | bullet | 12 | 4.06 | 16.88 | 2.96 | 4.14 |
| 35 | `jagerswi` | swi | Shooter | 65 | bullet | 20 | 6.88 | 22.5 | 2.91 | 4.07 |
| 36 | `musketeerpol` | pol | Shooter | 70 | bullet | 9 | 3.12 | 13.13 | 2.88 | 4.03 |
| 37 | `gauduk` | hun | Shooter | 60 | bullet | 9 | 3.12 | 14.06 | 2.88 | 4.03 |
| 38 | `dragoon` | aus, bav, den, eng, fra … (+11 more) | Mounted Shooter | 220 | bullet | 15 | 5.62 | 15.0 | 2.67 | 3.74 |
| 39 | `musketeernet` | net | Shooter | 65 | bullet | 10 | 3.75 | 15.0 | 2.67 | 3.74 |
| 40 | `lightcavalry` | hun | Mounted Shooter | 175 | bullet | 14 | 5.31 | 18.75 | 2.64 | 3.7 |
| 41 | `dragoonpol` | pol | Mounted Shooter | 185 | bullet | 13 | 5.0 | 15.94 | 2.6 | 3.64 |
| 42 | `musketeer` | bav, den, eng, fra, pie … (+6 more) | Shooter | 70 | bullet | 12 | 4.69 | 15.0 | 2.56 | 3.58 |
| 43 | `strelet` | rus | Shooter | 85 | bullet | 12 | 4.69 | 13.13 | 2.56 | 3.58 |
| 44 | `jannisary` | tur | Shooter | 65 | bullet | 12 | 4.69 | 15.94 | 2.56 | 3.58 |
| 45 | `musketeersco` | sco | Shooter | 90 | bullet | 12 | 4.69 | 15.94 | 2.56 | 3.58 |
| 46 | `musketeerspa` | spa | Shooter | 85 | bullet | 15 | 5.94 | 15.94 | 2.53 | 3.54 |
| 47 | `musketeeraus` | aus | Shooter | 55 | bullet | 12 | 5.0 | 15.0 | 2.4 | 3.36 |
| 48 | `dragoon18fra` | fra | Mounted Shooter | 140 | bullet | 10 | 4.69 | 15.0 | 2.13 | 2.98 |
| 49 | `jagerpor` | por | Shooter | 50 | bullet | 10 | 5.94 | 15.0 | 1.68 | 2.35 |

## §3. Effective HP — против эталонной атаки 10 единиц урона по типу

`EHP_vs_X = HP / max(1, 10 - prot[X])` — сколько ударов выдержит юнит если по нему бьёт оружие типа X с базовым уроном 10. Для атак с бо́льшим/меньшим уроном делите/умножайте пропорционально (формула линейна если урон > prot). Если `damage <= prot`, движок гарантирует минимум 1 урон/удар (`miscext2.script:381`) — поэтому EHP не бесконечный против пик у пикинёра с prot_pike=3, а ровно `HP / max(1, dmg-prot)`.

Включены только юниты, у которых хоть одно значение protection ≠ 0 (фильтр исключает типичных «голых» юнитов вроде стрельцов/мушкетёров без брони).

| sid | нации | usage | HP | shield | EHP pike | sword | bullet | cannister | arrow | cannonball |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `vityaz` | rus | Heavy Cavalry | 380 | — | 47.5 | 63.3 | 54.3 | 380.0 | 380.0 | 380.0 |
| `sipahi` | tur | Heavy Cavalry | 360 | — | 51.4 | 120.0 | 60.0 | 360.0 | 360.0 | 360.0 |
| `guardcavalrysax` | sax | Heavy Cavalry | 320 | — | 40.0 | 64.0 | 320.0 | 320.0 | 320.0 | 320.0 |
| `hetman` | ukr | Heavy Cavalry | 320 | — | 32.0 | 35.6 | 45.7 | 320.0 | 45.7 | 320.0 |
| `cuirassier` | aus, bav, den, eng, fra … (+12 more) | Heavy Cavalry | 300 | — | 37.5 | 50.0 | 300.0 | 300.0 | 60.0 | 300.0 |
| `reiter` | aus, bav, den, eng, fra … (+9 more) | Heavy Cavalry | 300 | — | 37.5 | 75.0 | 75.0 | 300.0 | 300.0 | 300.0 |
| `reiterswe` | swe | Heavy Cavalry | 300 | — | 37.5 | 42.9 | 100.0 | 300.0 | 100.0 | 300.0 |
| `mameluke` | alg | Heavy Cavalry | 280 | — | 31.1 | 40.0 | 31.1 | 280.0 | 140.0 | 28.0 |
| `spakh` | tur | Heavy Cavalry | 230 | — | 23.0 | 25.6 | 23.0 | 230.0 | 28.8 | 23.0 |
| `wingedhussar` | pol | Light Cavalry | 225 | — | 25.0 | 28.1 | 45.0 | 225.0 | 225.0 | 225.0 |
| `swordsmansco` | sco | Light Infantry | 180 | — | 20.0 | 22.5 | 22.5 | 180.0 | 45.0 | 180.0 |
| `officer` | aus, bav, den, eng, fra … (+11 more) | Light Infantry | 125 | — | 15.6 | 15.6 | 25.0 | 125.0 | 125.0 | 125.0 |
| `pikeman` | spa | Light Infantry | 100 | — | 14.3 | 16.7 | 25.0 | 100.0 | 100.0 | 100.0 |
| `pikemanpor` | por | Light Infantry | 100 | — | 10.0 | 11.1 | 11.1 | 100.0 | 16.7 | 10.0 |
| `pikemanspa` | spa | Light Infantry | 100 | — | 14.3 | 16.7 | 25.0 | 100.0 | 100.0 | 100.0 |
| `roundshier` | aus | Light Infantry | 100 | — | 14.3 | 14.3 | 33.3 | 100.0 | 100.0 | 100.0 |
| `pikeman` | aus, bav, den, eng, fra … (+7 more) | Light Infantry | 90 | — | 12.9 | 11.2 | 15.0 | 90.0 | 22.5 | 90.0 |
| `pikemanswi` | swi | Light Infantry | 90 | — | 12.9 | 12.9 | 22.5 | 90.0 | 22.5 | 90.0 |
| `pikemanrus` | rus | Light Infantry | 85 | — | 10.6 | 9.4 | 14.2 | 85.0 | 14.2 | 85.0 |
| `roundshierdip` | all | Light Infantry | 75 | — | 15.0 | 10.7 | 37.5 | 75.0 | 75.0 | 75.0 |
| `musketeerspa` | spa | Shooter | 85 | — | 12.1 | 10.6 | 17.0 | 85.0 | 28.3 | 85.0 |
| `musketeeraus` | aus | Shooter | 55 | — | 6.9 | 6.9 | 11.0 | 55.0 | 11.0 | 55.0 |

## §4. Замечания и оговорки

- **Оружие ближнего боя (pause = 0)** — DPS не считается. В коде урон melee наносится по триггеру анимационного кадра (`onaclanimationreachedwork`), цикл ~25-32 кадра ≈ 1 удар/g-sec. Точное значение требует эмпирического замера (FPS анимаций не подтверждён эмпирически).
- **Бонусы отряда** проигнорированы. `fAddDamage` (наступательный) и `fAddShield`/`fAddShieldHold` (стеновой режим) могут добавлять до +50% к damage и до +50 EHP — но они зависят от формации/состояния, а не от юнита. Сравнение в этой таблице — базовые статы против базовых.
- **`mortarball` / `firearrow`** — отдельные kind'ы, без соответствующего поля protection. Входят в DPS, но в §3 EHP не показаны (защиты нет).
- **Оружие `heal`** у priest'а исключено из всех расчётов — это неагрессивная способность.
- **Speed = 32** на пехоте — это `gc_obj_speed_default`. Реальная скорость крестьянина (`gc_obj_speed_peasant=40`) **закомментирована** в `unit.script:1192`, по умолчанию применяется `objbase.speed:=1`. Числа в столбце speed — таблица из `dmscript.global:603-620`, то есть _декларированные_ значения, не верифицированные эмпирически.
- **Реальное время.** Если играете на скорости fast (×1.4) — умножьте все DPS из колонки g-sec на 1.4. На default (×1.0) — не умножайте.

---

Сгенерировано из `docs/data.json`. Для перегенерации:

```
python compute/compute_combat_stats.py
```