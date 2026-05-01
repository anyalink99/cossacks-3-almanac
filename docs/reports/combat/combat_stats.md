# Cossacks 3 — DPS / EHP / armor metrics

**Производный** файл (расчётный, не извлечение). Считается из `docs/data.json` скриптом [`compute/compute_combat_stats.py`](../../compute/compute_combat_stats.py).

## Формула урона

Расчёт урона делается в `_misc_DoDamage` [^1]. Кратко:

```
applied_damage = max(1, base_damage + squad_bonus - target.protection[weapon_kind])
target.hp     -= applied_damage
```

`gc_settings_gamespeed_2 = 14` (fast). Game-time → real-time: `×1.4`. 
Реальный DPS = game-DPS × game_speed.

## §1. Сводная таблица боевых юнитов

Группировка: одна строка на каждый уникальный набор статов. Колонка **Нации** — где этот юнит с этими статами доступен (`все 21` = во всех). Если у юнита разные значения у разных наций (например `pikemanpol` имеет половину брони от стандарта) — это разные строки.

Колонки: HP, скорость (px на игровую секунду; 32 = крестьянин), основное оружие (урон / пауза / дальность / тип), DPS в игровых секундах, DPS в реальных секундах (×1.4 на скорости fast), защиты (только ненулевые) и щит. У юнита может быть несколько оружий — показано **сильнейшее по соотношению урон/пауза**.

| `sid` | Нации | Класс | HP | Скорость | Основное оружие | DPS, g-сек | DPS, real (fast) | Защиты |
| --- | --- | --- | ---: | ---: | --- | ---: | ---: | --- |
| `tatar` | **tur** Турция | Лучник | 185 | 32 | 140d / 4.69s / 20.63t [firearrow] | 29.85 | 41.79 | — |
| `archersco` | **sco** Шотландия | Лучник | 150 | 32 | 150d / 4.38s / 18.75t [firearrow] | 34.25 | 47.95 | — |
| `archertur` | **tur** Турция | Лучник | 65 | 32 | 150d / 4.38s / 16.88t [firearrow] | 34.25 | 47.95 | — |
| `archer` | **alg** Алжир | Лучник | 40 | 32 | 150d / 3.91s / 11.25t [firearrow] | 38.36 | 53.7 | — |
| `archerdip` | все 21 | Лучник | 20 | 32 | 100d / 0.78s / 14.06t [firearrow] | 128.21 | 179.49 | — |
| `archerturdip` | все 21 | Лучник | 20 | 32 | 100d / 0.78s / 14.06t [firearrow] | 128.21 | 179.49 | — |
| `cannon` | все 21 | Пушка | 9000 | 20 | 1800d / 10.94s / 40.5t [cannonball] | 164.53 | 230.34 | shield=75 |
| `framegun` | **sco** Шотландия | Пушка | 3000 | 20 | 500d / 2.81s / 33.75t [cannonball] | 177.94 | 249.12 | shield=50 |
| `grenadierbav` | **bav** Бавария | Гренадёр | 125 | 32 | 110d / 2.34s / 9.38t [mortarball] | 47.01 | 65.81 | — |
| `grenadierden` | **den** Дания | Гренадёр | 125 | 32 | 110d / 2.34s / 9.38t [mortarball] | 47.01 | 65.81 | — |
| `grenadierhun` | **hun** Венгрия | Гренадёр | 125 | 32 | 110d / 2.81s / 11.25t [mortarball] | 39.15 | 54.81 | — |
| `grenadierpru` | **pru** Пруссия | Гренадёр | 125 | 32 | 110d / 2.34s / 9.38t [mortarball] | 47.01 | 65.81 | — |
| `grenadier` | **aus** Австрия, **eng** Англия, **fra** Франция, **net** Нидерланды, **pie** Пьемонт … (+8) | Гренадёр | 120 | 32 | 110d / 2.34s / 9.38t [mortarball] | 47.01 | 65.81 | — |
| `grenadiersax` | **sax** Саксония | Гренадёр | 100 | 32 | 110d / 2.34s / 9.38t [mortarball] | 47.01 | 65.81 | — |
| `grenadierdip` | все 21 | Гренадёр | 30 | 32 | 200d / 3.12s / 7.5t [mortarball] | 64.1 | 89.74 | — |
| `vityaz` | **rus** Россия | Тяжёлая кавалерия | 380 | 56 | 14d / 0 (melee) / 1.22t [pike] | — | — | pike=2, sword=4, bullet=3, cannister=160, arrow=17, cannonball=40 |
| `sipahi` | **tur** Турция | Тяжёлая кавалерия | 360 | 56 | 15d / 0 (melee) / 1.22t [sword] | — | — | pike=3, sword=7, bullet=4, cannister=225, arrow=24, cannonball=60 |
| `guardcavalrysax` | **sax** Саксония | Тяжёлая кавалерия | 320 | 56 | 15d / 0 (melee) / 1.22t [pike] | — | — | pike=2, sword=5, bullet=9, cannister=150, arrow=9, cannonball=70 |
| `hetman` | **ukr** Украина | Тяжёлая кавалерия | 320 | 56 | 70d / 0 (melee) / 1.22t [pike] | — | — | sword=1, bullet=3, cannister=75, arrow=3, cannonball=15 |
| `lancersco` | **sco** Шотландия | Тяжёлая кавалерия | 320 | 56 | 11d / 0 (melee) / 1.88t [pike] | — | — | — |
| `cuirassier` | **aus** Австрия, **bav** Бавария, **den** Дания, **eng** Англия, **fra** Франция … (+12) | Тяжёлая кавалерия | 300 | 56 | 14d / 0 (melee) / 1.22t [pike] | — | — | pike=2, sword=4, bullet=10, cannister=160, arrow=5, cannonball=80 |
| `reiter` | **aus** Австрия, **bav** Бавария, **den** Дания, **eng** Англия, **fra** Франция … (+9) | Тяжёлая кавалерия | 300 | 56 | 15d / 0 (melee) / 1.22t [pike] | — | — | pike=2, sword=6, bullet=6, cannister=190, arrow=15, cannonball=40 |
| `reiterswe` | **swe** Швеция | Тяжёлая кавалерия | 300 | 56 | 14d / 0 (melee) / 1.22t [pike] | — | — | pike=2, sword=3, bullet=7, cannister=140, arrow=7, cannonball=35 |
| `mameluke` | **alg** Алжир | Тяжёлая кавалерия | 280 | 56 | 16d / 0 (melee) / 1.88t [pike] | — | — | pike=1, sword=3, bullet=1, cannister=75, arrow=8 |
| `cossackregister` | **ukr** Украина | Тяжёлая кавалерия | 250 | 56 | 12d / 0 (melee) / 1.88t [pike] | — | — | — |
| `spakh` | **tur** Турция | Тяжёлая кавалерия | 230 | 56 | 15d / 0 (melee) / 1.88t [pike] | — | — | sword=1, cannister=10, arrow=2 |
| `cossackdon` | **rus** Россия | Тяжёлая кавалерия | 220 | 56 | 13d / 0 (melee) / 1.88t [pike] | — | — | — |
| `reiterpol` | **pol** Польша | Тяжёлая кавалерия | 190 | 56 | 9d / 0 (melee) / 1.22t [sword] | — | — | — |
| `raidersco` | **sco** Шотландия | Лёгкая кавалерия | 280 | 96 | 11d / 0 (melee) / 1.22t [sword] | — | — | — |
| `hussarswi` | **swi** Швейцария | Лёгкая кавалерия | 265 | 96 | 14d / 0 (melee) / 1.22t [sword] | — | — | — |
| `croat` | **aus** Австрия | Лёгкая кавалерия | 260 | 96 | 9d / 0 (melee) / 1.22t [sword] | — | — | — |
| `cossacksich` | **ukr** Украина | Лёгкая кавалерия | 250 | 96 | 13d / 0 (melee) / 1.22t [sword] | — | — | — |
| `hussarhun` | **hun** Венгрия | Лёгкая кавалерия | 250 | 96 | 10d / 0 (melee) / 1.22t [sword] | — | — | — |
| `hackapell` | **swe** Швеция | Лёгкая кавалерия | 245 | 96 | 12d / 0 (melee) / 1.22t [pike] | — | — | — |
| `hussarpru` | **pru** Пруссия | Лёгкая кавалерия | 240 | 96 | 9d / 0 (melee) / 1.22t [sword] | — | — | — |
| `hussar` | **aus** Австрия, **bav** Бавария, **den** Дания, **eng** Англия, **fra** Франция … (+9) | Лёгкая кавалерия | 230 | 96 | 12d / 0 (melee) / 1.22t [sword] | — | — | — |
| `wingedhussar` | **pol** Польша | Лёгкая кавалерия | 225 | 96 | 14d / 0 (melee) / 1.88t [pike] | — | — | pike=1, sword=2, bullet=5, cannister=160, arrow=10, cannonball=30 |
| `cossacksichdip` | все 21 | Лёгкая кавалерия | 150 | 96 | 8d / 0 (melee) / 1.22t [sword] | — | — | — |
| `swordsmansco` | **sco** Шотландия | Лёгкая пехота | 180 | 32 | 10d / 0 (melee) / 1.13t [sword] | — | — | pike=1, sword=2, bullet=2, cannister=110, arrow=6, cannonball=10 |
| `officersco` | **sco** Шотландия | Лёгкая пехота | 150 | 32 | 40d / 0 (melee) / 1.22t [pike] | — | — | — |
| `officer` | **aus** Австрия, **bav** Бавария, **den** Дания, **eng** Англия, **fra** Франция … (+11) | Лёгкая пехота | 125 | 32 | 30d / 0 (melee) / 1.22t [pike] | — | — | pike=2, sword=2, bullet=5, cannister=200, arrow=10, cannonball=30 |
| `officer18` | **aus** Австрия, **bav** Бавария, **den** Дания, **eng** Англия, **fra** Франция … (+12) | Лёгкая пехота | 125 | 32 | 50d / 0 (melee) / 1.22t [pike] | — | — | — |
| `officerrus` | **rus** Россия | Лёгкая пехота | 125 | 32 | 40d / 0 (melee) / 1.22t [pike] | — | — | — |
| `officertur` | **alg** Алжир, **tur** Турция | Лёгкая пехота | 125 | 32 | 30d / 0 (melee) / 1.22t [pike] | — | — | — |
| `pikeman18swe` | **swe** Швеция | Лёгкая пехота | 110 | 32 | 11d / 0 (melee) / 1.88t [pike] | — | — | — |
| `drummer18` | **rus** Россия | Лёгкая пехота | 100 | 32 | — | — | — | — |
| `drummerrus` | **rus** Россия | Лёгкая пехота | 100 | 32 | — | — | — | — |
| `mullah` | **alg** Алжир, **tur** Турция | Лёгкая пехота | 100 | 32 | — | — | — | — |
| `padre` | **pie** Пьемонт | Лёгкая пехота | 100 | 32 | — | — | — | — |
| `pikeman` | **spa** Испания | Лёгкая пехота | 100 | 32 | 10d / 0 (melee) / 1.88t [pike] | — | — | pike=3, sword=4, bullet=6, cannister=240, arrow=12, cannonball=50 |
| `pikemanpor` | **por** Португалия | Лёгкая пехота | 100 | 32 | 9d / 0 (melee) / 1.88t [pike] | — | — | sword=1, bullet=1, cannister=25, arrow=4 |
| `pikemansco` | **sco** Шотландия | Лёгкая пехота | 100 | 32 | 9d / 0 (melee) / 1.88t [pike] | — | — | — |
| `pikemanspa` | **spa** Испания | Лёгкая пехота | 100 | 32 | 10d / 0 (melee) / 1.88t [pike] | — | — | pike=3, sword=4, bullet=6, cannister=240, arrow=12, cannonball=50 |
| `pope` | **rus** Россия, **ukr** Украина | Лёгкая пехота | 100 | 32 | — | — | — | — |
| `priest` | **aus** Австрия, **bav** Бавария, **den** Дания, **eng** Англия, **fra** Франция … (+11) | Лёгкая пехота | 100 | 32 | — | — | — | — |
| `roundshier` | **aus** Австрия | Лёгкая пехота | 100 | 32 | 6d / 0 (melee) / 1.13t [sword] | — | — | pike=3, sword=3, bullet=7, cannister=225, arrow=16, cannonball=80 |
| `pikemantur` | **alg** Алжир, **tur** Турция | Лёгкая пехота | 95 | 32 | 9d / 0 (melee) / 2.06t [pike] | — | — | — |
| `pikeman` | **aus** Австрия, **bav** Бавария, **den** Дания, **eng** Англия, **fra** Франция … (+7) | Лёгкая пехота | 90 | 32 | 8d / 0 (melee) / 1.88t [pike] | — | — | pike=3, sword=2, bullet=4, cannister=210, arrow=6, cannonball=40 |
| `pikemanpol` | **pol** Польша | Лёгкая пехота | 90 | 32 | 8d / 0 (melee) / 2.06t [pike] | — | — | — |
| `pikemanswi` | **swi** Швейцария | Лёгкая пехота | 90 | 32 | 10d / 0 (melee) / 1.88t [pike] | — | — | pike=3, sword=3, bullet=6, cannister=220, arrow=6, cannonball=45 |
| `pikeman18` | **aus** Австрия, **bav** Бавария, **den** Дания, **eng** Англия, **fra** Франция … (+11) | Лёгкая пехота | 85 | 32 | 9d / 0 (melee) / 1.88t [pike] | — | — | — |
| `pikemanrus` | **rus** Россия | Лёгкая пехота | 85 | 32 | 8d / 0 (melee) / 1.69t [pike] | — | — | pike=2, sword=1, bullet=4, cannister=140, arrow=4, cannonball=25 |
| `bagpiper` | **eng** Англия, **sco** Шотландия | Лёгкая пехота | 75 | 32 | — | — | — | — |
| `drummer` | **aus** Австрия, **bav** Бавария, **den** Дания, **eng** Англия, **fra** Франция … (+11) | Лёгкая пехота | 75 | 32 | — | — | — | — |
| `drummer18` | **aus** Австрия, **bav** Бавария, **den** Дания, **fra** Франция, **hun** Венгрия … (+10) | Лёгкая пехота | 75 | 32 | — | — | — | — |
| `roundshierdip` | все 21 | Лёгкая пехота | 75 | 32 | 6d / 0 (melee) / 1.13t [sword] | — | — | pike=5, sword=3, bullet=8, cannister=225, arrow=17, cannonball=80 |
| `lightinfantry` | **alg** Алжир, **tur** Турция | Лёгкая пехота | 55 | 32 | 5d / 0 (melee) / 0.94t [sword] | — | — | — |
| `drummertur` | **alg** Алжир, **tur** Турция | Лёгкая пехота | 50 | 32 | — | — | — | — |
| `lightinfantrydip` | все 21 | Лёгкая пехота | 50 | 32 | 16d / 0 (melee) / 0.94t [sword] | — | — | — |
| `howitzer` | все 21 | Мортира | 3000 | 20 | 4000d / 18.75s / 26.25t [cannonball] | 213.33 | 298.66 | shield=75 |
| `dragoon18net` | **net** Нидерланды | Конный стрелок | 320 | 56 | 17d / 5.0s / 15.94t [bullet] | 3.4 | 4.76 | — |
| `kingmusketeer` | **fra** Франция | Конный стрелок | 280 | 56 | 43d / 6.88s / 13.13t [bullet] | 6.25 | 8.75 | — |
| `dragoon18` | **aus** Австрия, **bav** Бавария, **den** Дания, **eng** Англия, **pol** Польша … (+8) | Конный стрелок | 225 | 56 | 19d / 5.31s / 16.88t [bullet] | 3.58 | 5.01 | — |
| `dragoon` | **aus** Австрия, **bav** Бавария, **den** Дания, **eng** Англия, **fra** Франция … (+11) | Конный стрелок | 220 | 56 | 15d / 5.62s / 15.0t [bullet] | 2.67 | 3.74 | — |
| `dragoon18pie` | **pie** Пьемонт | Конный стрелок | 200 | 56 | 19d / 5.0s / 16.88t [bullet] | 3.8 | 5.32 | — |
| `dragoonpol` | **pol** Польша | Конный стрелок | 185 | 56 | 13d / 5.0s / 15.94t [bullet] | 2.6 | 3.64 | — |
| `lightcavalry` | **hun** Венгрия | Конный стрелок | 175 | 56 | 14d / 5.31s / 18.75t [bullet] | 2.64 | 3.7 | — |
| `dragoon18fra` | **fra** Франция | Конный стрелок | 140 | 56 | 10d / 4.69s / 15.0t [bullet] | 2.13 | 2.98 | — |
| `multicannon` | **aus** Австрия, **bav** Бавария, **den** Дания, **eng** Англия, **fra** Франция … (+12) | Многоствольная пушка | 2000 | 16 | 500d / 1.88s / 13.13t [cannister] | 265.96 | 372.34 | shield=50 |
| `highlander` | **eng** Англия | Стрелок | 130 | 32 | 16d / 5.0s / 15.94t [bullet] | 3.2 | 4.48 | — |
| `dragoon18dip` | все 21 | Стрелок | 100 | 56 | 18d / 2.25s / 15.0t [bullet] | 8.0 | 11.2 | — |
| `lightcavalrydip` | все 21 | Стрелок | 100 | 56 | 18d / 2.25s / 15.0t [bullet] | 8.0 | 11.2 | — |
| `musketeer18` | **aus** Австрия, **eng** Англия, **fra** Франция, **hun** Венгрия, **net** Нидерланды … (+8) | Стрелок | 100 | 32 | 16d / 4.69s / 16.88t [bullet] | 3.41 | 4.77 | — |
| `musketeer18bav` | **bav** Бавария | Стрелок | 100 | 32 | 22d / 5.94s / 17.81t [bullet] | 3.7 | 5.18 | — |
| `musketeer18den` | **den** Дания | Стрелок | 100 | 32 | 29d / 5.94s / 16.88t [bullet] | 4.88 | 6.83 | — |
| `musketeer18pru` | **pru** Пруссия | Стрелок | 100 | 32 | 22d / 4.69s / 17.81t [bullet] | 4.69 | 6.57 | — |
| `musketeer18sax` | **sax** Саксония | Стрелок | 90 | 32 | 19d / 4.38s / 16.88t [bullet] | 4.34 | 6.08 | — |
| `musketeersco` | **sco** Шотландия | Стрелок | 90 | 32 | 12d / 4.69s / 15.94t [bullet] | 2.56 | 3.58 | — |
| `musketeerspa` | **spa** Испания | Стрелок | 85 | 32 | 15d / 5.94s / 15.94t [bullet] | 2.53 | 3.54 | pike=3, sword=2, bullet=5, cannister=210, arrow=7, cannonball=40 |
| `pandur` | **aus** Австрия | Стрелок | 85 | 32 | 17d / 4.69s / 16.88t [bullet] | 3.62 | 5.07 | — |
| `serdiuk` | **ukr** Украина | Стрелок | 85 | 32 | 12d / 4.06s / 16.88t [bullet] | 2.96 | 4.14 | — |
| `strelet` | **rus** Россия | Стрелок | 85 | 32 | 12d / 4.69s / 13.13t [bullet] | 2.56 | 3.58 | — |
| `chasseur` | **fra** Франция | Стрелок | 75 | 32 | 20d / 5.94s / 19.69t [bullet] | 3.37 | 4.72 | — |
| `pandurhun` | **hun** Венгрия | Стрелок | 75 | 32 | 19d / 5.0s / 18.75t [bullet] | 3.8 | 5.32 | — |
| `musketeer` | **bav** Бавария, **den** Дания, **eng** Англия, **fra** Франция, **pie** Пьемонт … (+6) | Стрелок | 70 | 32 | 12d / 4.69s / 15.0t [bullet] | 2.56 | 3.58 | — |
| `musketeerpol` | **pol** Польша | Стрелок | 70 | 32 | 9d / 3.12s / 13.13t [bullet] | 2.88 | 4.03 | — |
| `jagerswi` | **swi** Швейцария | Стрелок | 65 | 32 | 20d / 6.88s / 22.5t [bullet] | 2.91 | 4.07 | — |
| `jannisary` | **tur** Турция | Стрелок | 65 | 32 | 12d / 4.69s / 15.94t [bullet] | 2.56 | 3.58 | — |
| `musketeernet` | **net** Нидерланды | Стрелок | 65 | 32 | 10d / 3.75s / 15.0t [bullet] | 2.67 | 3.74 | — |
| `gauduk` | **hun** Венгрия | Стрелок | 60 | 32 | 9d / 3.12s / 14.06t [bullet] | 2.88 | 4.03 | — |
| `musketeeraus` | **aus** Австрия | Стрелок | 55 | 32 | 12d / 5.0s / 15.0t [bullet] | 2.4 | 3.36 | pike=2, sword=2, bullet=5, cannister=165, arrow=5, cannonball=35 |
| `jagerpor` | **por** Португалия | Стрелок | 50 | 32 | 10d / 5.94s / 15.0t [bullet] | 1.68 | 2.35 | — |
| `mortar` | все 21 | Сверхмортира | 400 | 24 | 200d / 7.81s / 48.75t [mortarball] | 25.61 | 35.85 | shield=25 |

## §2. Рейтинг DPS — боевые юниты

Все combat-юниты с `pause > 0` (melee с `pause = 0` исключены — урон у них привязан к анимационному циклу, см. §4). DPS считается в game-sec; колонка "DPS real (fast)" — ×1.4 для удобства сравнения с тем, что видно в реальном времени.

| # | sid | нации | usage | HP | weapon kind | урон | пауза, с | дальн., тайл. | DPS g-s | DPS real |
| ---: | --- | --- | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | `multicannon` | **aus** Австрия, **bav** Бавария, **den** Дания, **eng** Англия, **fra** Франция … (+12) | Multi-cannon | 2000 | cannister | 500 | 1.88 | 13.13 | 265.96 | 372.34 |
| 2 | `howitzer` | все 21 | Mortar | 3000 | cannonball | 4000 | 18.75 | 26.25 | 213.33 | 298.66 |
| 3 | `framegun` | **sco** Шотландия | Cannon | 3000 | cannonball | 500 | 2.81 | 33.75 | 177.94 | 249.12 |
| 4 | `cannon` | все 21 | Cannon | 9000 | cannonball | 1800 | 10.94 | 40.5 | 164.53 | 230.34 |
| 5 | `archerdip` | все 21 | Archer | 20 | firearrow | 100 | 0.78 | 14.06 | 128.21 | 179.49 |
| 6 | `archerturdip` | все 21 | Archer | 20 | firearrow | 100 | 0.78 | 14.06 | 128.21 | 179.49 |
| 7 | `grenadierdip` | все 21 | Grenadier | 30 | mortarball | 200 | 3.12 | 7.5 | 64.1 | 89.74 |
| 8 | `grenadier` | **aus** Австрия, **eng** Англия, **fra** Франция, **net** Нидерланды, **pie** Пьемонт … (+8) | Grenadier | 120 | mortarball | 110 | 2.34 | 9.38 | 47.01 | 65.81 |
| 9 | `grenadierpru` | **pru** Пруссия | Grenadier | 125 | mortarball | 110 | 2.34 | 9.38 | 47.01 | 65.81 |
| 10 | `grenadierden` | **den** Дания | Grenadier | 125 | mortarball | 110 | 2.34 | 9.38 | 47.01 | 65.81 |
| 11 | `grenadiersax` | **sax** Саксония | Grenadier | 100 | mortarball | 110 | 2.34 | 9.38 | 47.01 | 65.81 |
| 12 | `grenadierbav` | **bav** Бавария | Grenadier | 125 | mortarball | 110 | 2.34 | 9.38 | 47.01 | 65.81 |
| 13 | `grenadierhun` | **hun** Венгрия | Grenadier | 125 | mortarball | 110 | 2.81 | 11.25 | 39.15 | 54.81 |
| 14 | `archer` | **alg** Алжир | Archer | 40 | firearrow | 150 | 3.91 | 11.25 | 38.36 | 53.7 |
| 15 | `archertur` | **tur** Турция | Archer | 65 | firearrow | 150 | 4.38 | 16.88 | 34.25 | 47.95 |
| 16 | `archersco` | **sco** Шотландия | Archer | 150 | firearrow | 150 | 4.38 | 18.75 | 34.25 | 47.95 |
| 17 | `tatar` | **tur** Турция | Archer | 185 | firearrow | 140 | 4.69 | 20.63 | 29.85 | 41.79 |
| 18 | `mortar` | все 21 | Super Mortar | 400 | mortarball | 200 | 7.81 | 48.75 | 25.61 | 35.85 |
| 19 | `dragoon18dip` | все 21 | Shooter | 100 | bullet | 18 | 2.25 | 15.0 | 8.0 | 11.2 |
| 20 | `lightcavalrydip` | все 21 | Shooter | 100 | bullet | 18 | 2.25 | 15.0 | 8.0 | 11.2 |
| 21 | `kingmusketeer` | **fra** Франция | Mounted Shooter | 280 | bullet | 43 | 6.88 | 13.13 | 6.25 | 8.75 |
| 22 | `musketeer18den` | **den** Дания | Shooter | 100 | bullet | 29 | 5.94 | 16.88 | 4.88 | 6.83 |
| 23 | `musketeer18pru` | **pru** Пруссия | Shooter | 100 | bullet | 22 | 4.69 | 17.81 | 4.69 | 6.57 |
| 24 | `musketeer18sax` | **sax** Саксония | Shooter | 90 | bullet | 19 | 4.38 | 16.88 | 4.34 | 6.08 |
| 25 | `dragoon18pie` | **pie** Пьемонт | Mounted Shooter | 200 | bullet | 19 | 5.0 | 16.88 | 3.8 | 5.32 |
| 26 | `pandurhun` | **hun** Венгрия | Shooter | 75 | bullet | 19 | 5.0 | 18.75 | 3.8 | 5.32 |
| 27 | `musketeer18bav` | **bav** Бавария | Shooter | 100 | bullet | 22 | 5.94 | 17.81 | 3.7 | 5.18 |
| 28 | `pandur` | **aus** Австрия | Shooter | 85 | bullet | 17 | 4.69 | 16.88 | 3.62 | 5.07 |
| 29 | `dragoon18` | **aus** Австрия, **bav** Бавария, **den** Дания, **eng** Англия, **pol** Польша … (+8) | Mounted Shooter | 225 | bullet | 19 | 5.31 | 16.88 | 3.58 | 5.01 |
| 30 | `musketeer18` | **aus** Австрия, **eng** Англия, **fra** Франция, **hun** Венгрия, **net** Нидерланды … (+8) | Shooter | 100 | bullet | 16 | 4.69 | 16.88 | 3.41 | 4.77 |
| 31 | `dragoon18net` | **net** Нидерланды | Mounted Shooter | 320 | bullet | 17 | 5.0 | 15.94 | 3.4 | 4.76 |
| 32 | `chasseur` | **fra** Франция | Shooter | 75 | bullet | 20 | 5.94 | 19.69 | 3.37 | 4.72 |
| 33 | `highlander` | **eng** Англия | Shooter | 130 | bullet | 16 | 5.0 | 15.94 | 3.2 | 4.48 |
| 34 | `serdiuk` | **ukr** Украина | Shooter | 85 | bullet | 12 | 4.06 | 16.88 | 2.96 | 4.14 |
| 35 | `jagerswi` | **swi** Швейцария | Shooter | 65 | bullet | 20 | 6.88 | 22.5 | 2.91 | 4.07 |
| 36 | `musketeerpol` | **pol** Польша | Shooter | 70 | bullet | 9 | 3.12 | 13.13 | 2.88 | 4.03 |
| 37 | `gauduk` | **hun** Венгрия | Shooter | 60 | bullet | 9 | 3.12 | 14.06 | 2.88 | 4.03 |
| 38 | `dragoon` | **aus** Австрия, **bav** Бавария, **den** Дания, **eng** Англия, **fra** Франция … (+11) | Mounted Shooter | 220 | bullet | 15 | 5.62 | 15.0 | 2.67 | 3.74 |
| 39 | `musketeernet` | **net** Нидерланды | Shooter | 65 | bullet | 10 | 3.75 | 15.0 | 2.67 | 3.74 |
| 40 | `lightcavalry` | **hun** Венгрия | Mounted Shooter | 175 | bullet | 14 | 5.31 | 18.75 | 2.64 | 3.7 |
| 41 | `dragoonpol` | **pol** Польша | Mounted Shooter | 185 | bullet | 13 | 5.0 | 15.94 | 2.6 | 3.64 |
| 42 | `musketeer` | **bav** Бавария, **den** Дания, **eng** Англия, **fra** Франция, **pie** Пьемонт … (+6) | Shooter | 70 | bullet | 12 | 4.69 | 15.0 | 2.56 | 3.58 |
| 43 | `strelet` | **rus** Россия | Shooter | 85 | bullet | 12 | 4.69 | 13.13 | 2.56 | 3.58 |
| 44 | `jannisary` | **tur** Турция | Shooter | 65 | bullet | 12 | 4.69 | 15.94 | 2.56 | 3.58 |
| 45 | `musketeersco` | **sco** Шотландия | Shooter | 90 | bullet | 12 | 4.69 | 15.94 | 2.56 | 3.58 |
| 46 | `musketeerspa` | **spa** Испания | Shooter | 85 | bullet | 15 | 5.94 | 15.94 | 2.53 | 3.54 |
| 47 | `musketeeraus` | **aus** Австрия | Shooter | 55 | bullet | 12 | 5.0 | 15.0 | 2.4 | 3.36 |
| 48 | `dragoon18fra` | **fra** Франция | Mounted Shooter | 140 | bullet | 10 | 4.69 | 15.0 | 2.13 | 2.98 |
| 49 | `jagerpor` | **por** Португалия | Shooter | 50 | bullet | 10 | 5.94 | 15.0 | 1.68 | 2.35 |

## §3. Effective HP — против эталонной атаки 10 единиц урона по типу

`EHP_vs_X = HP / max(1, 10 - prot[X])` — сколько ударов выдержит юнит если по нему бьёт оружие типа X с базовым уроном 10. Для атак с бо́льшим/меньшим уроном делите/умножайте пропорционально (формула линейна если урон > prot). Если `damage <= prot`, движок гарантирует минимум 1 урон/удар [^2] — поэтому EHP не бесконечный против пик у пикинёра с prot_pike=3, а ровно `HP / max(1, dmg-prot)`.

Включены только юниты, у которых хоть одно значение protection ≠ 0 (фильтр исключает типичных «голых» юнитов вроде стрельцов/мушкетёров без брони).

| sid | нации | usage | HP | shield | EHP pike | sword | bullet | cannister | arrow | cannonball |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `vityaz` | **rus** Россия | Heavy Cavalry | 380 | — | 47.5 | 63.3 | 54.3 | 380.0 | 380.0 | 380.0 |
| `sipahi` | **tur** Турция | Heavy Cavalry | 360 | — | 51.4 | 120.0 | 60.0 | 360.0 | 360.0 | 360.0 |
| `guardcavalrysax` | **sax** Саксония | Heavy Cavalry | 320 | — | 40.0 | 64.0 | 320.0 | 320.0 | 320.0 | 320.0 |
| `hetman` | **ukr** Украина | Heavy Cavalry | 320 | — | 32.0 | 35.6 | 45.7 | 320.0 | 45.7 | 320.0 |
| `cuirassier` | **aus** Австрия, **bav** Бавария, **den** Дания, **eng** Англия, **fra** Франция … (+12) | Heavy Cavalry | 300 | — | 37.5 | 50.0 | 300.0 | 300.0 | 60.0 | 300.0 |
| `reiter` | **aus** Австрия, **bav** Бавария, **den** Дания, **eng** Англия, **fra** Франция … (+9) | Heavy Cavalry | 300 | — | 37.5 | 75.0 | 75.0 | 300.0 | 300.0 | 300.0 |
| `reiterswe` | **swe** Швеция | Heavy Cavalry | 300 | — | 37.5 | 42.9 | 100.0 | 300.0 | 100.0 | 300.0 |
| `mameluke` | **alg** Алжир | Heavy Cavalry | 280 | — | 31.1 | 40.0 | 31.1 | 280.0 | 140.0 | 28.0 |
| `spakh` | **tur** Турция | Heavy Cavalry | 230 | — | 23.0 | 25.6 | 23.0 | 230.0 | 28.8 | 23.0 |
| `wingedhussar` | **pol** Польша | Light Cavalry | 225 | — | 25.0 | 28.1 | 45.0 | 225.0 | 225.0 | 225.0 |
| `swordsmansco` | **sco** Шотландия | Light Infantry | 180 | — | 20.0 | 22.5 | 22.5 | 180.0 | 45.0 | 180.0 |
| `officer` | **aus** Австрия, **bav** Бавария, **den** Дания, **eng** Англия, **fra** Франция … (+11) | Light Infantry | 125 | — | 15.6 | 15.6 | 25.0 | 125.0 | 125.0 | 125.0 |
| `pikeman` | **spa** Испания | Light Infantry | 100 | — | 14.3 | 16.7 | 25.0 | 100.0 | 100.0 | 100.0 |
| `pikemanpor` | **por** Португалия | Light Infantry | 100 | — | 10.0 | 11.1 | 11.1 | 100.0 | 16.7 | 10.0 |
| `pikemanspa` | **spa** Испания | Light Infantry | 100 | — | 14.3 | 16.7 | 25.0 | 100.0 | 100.0 | 100.0 |
| `roundshier` | **aus** Австрия | Light Infantry | 100 | — | 14.3 | 14.3 | 33.3 | 100.0 | 100.0 | 100.0 |
| `pikeman` | **aus** Австрия, **bav** Бавария, **den** Дания, **eng** Англия, **fra** Франция … (+7) | Light Infantry | 90 | — | 12.9 | 11.2 | 15.0 | 90.0 | 22.5 | 90.0 |
| `pikemanswi` | **swi** Швейцария | Light Infantry | 90 | — | 12.9 | 12.9 | 22.5 | 90.0 | 22.5 | 90.0 |
| `pikemanrus` | **rus** Россия | Light Infantry | 85 | — | 10.6 | 9.4 | 14.2 | 85.0 | 14.2 | 85.0 |
| `roundshierdip` | все 21 | Light Infantry | 75 | — | 15.0 | 10.7 | 37.5 | 75.0 | 75.0 | 75.0 |
| `musketeerspa` | **spa** Испания | Shooter | 85 | — | 12.1 | 10.6 | 17.0 | 85.0 | 28.3 | 85.0 |
| `musketeeraus` | **aus** Австрия | Shooter | 55 | — | 6.9 | 6.9 | 11.0 | 55.0 | 11.0 | 55.0 |

## §4. Замечания и оговорки

- **Оружие ближнего боя (pause = 0)** — DPS не считается. В коде урон melee наносится по триггеру анимационного кадра (`onaclanimationreachedwork`), цикл ~25-32 кадра ≈ 1 удар/g-sec. Точное значение требует эмпирического замера (FPS анимаций не подтверждён эмпирически).
- **Бонусы отряда** проигнорированы. `fAddDamage` (наступательный) и `fAddShield`/`fAddShieldHold` (стеновой режим) могут добавлять до +50% к damage и до +50 EHP — но они зависят от формации/состояния, а не от юнита. Сравнение в этой таблице — базовые статы против базовых.
- **`mortarball` / `firearrow`** — отдельные значения kind, без соответствующего поля protection. Входят в DPS, но в §3 EHP не показаны (защиты нет).
- **Оружие `heal`** у священника исключено из всех расчётов — это неагрессивная способность.
- **Speed = 32** на пехоте — это `gc_obj_speed_default`. Реальная скорость крестьянина (`gc_obj_speed_peasant=40`) **закомментирована** [^3], по умолчанию применяется `objbase.speed:=1`. Числа в столбце speed — таблица констант [^4], то есть _декларированные_ значения, не верифицированные эмпирически.
- **Реальное время.** Если играете на скорости fast (×1.4) — умножьте все DPS из колонки g-sec на 1.4. На default (×1.0) — не умножайте.

---

Сгенерировано из `docs/data.json`. Для перегенерации:

```
python compute/compute_combat_stats.py
```

## Источники

Все ссылки относительно `data/scripts/` в установке Cossacks 3.

[^1]: `_misc_DoDamage` — вычитание защиты и срабатывание хедшота — `lib/miscext2.script:380, 434`.

[^2]: правило min damage = 1 — `lib/miscext2.script:381`.

[^3]: закомментированное `objbase.speed := gc_obj_speed_peasant` — `lib/unit.script:1192`.

[^4]: таблица `gc_obj_speed_*` — `dmscript.global:603-620`.
