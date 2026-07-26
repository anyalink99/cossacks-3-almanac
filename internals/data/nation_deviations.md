# Национальные отклонения — здания и юниты

**Производный** файл (расчётный, не извлечение). Считается из [`data.json`](../../data.json) скриптом [`compute/compute_nation_deviations.py`](../../compute/compute_nation_deviations.py).

Цель — собрать в одном месте ВСЕ места, где у конкретной нации значение стата здания или общего юнита отличается от того, что у большинства. Источник дельт — `case i of nation:` ветки в `unit.script`, которые перезаписывают `SetObjBuildingProperties` / `SetObjBaseWeapon` для отдельных наций.

Формат: для каждого семейства (например, `<nat>cen` — Городской центр) 21 нация группируется по «отпечатку» — кортежу значимых статов. Мажоритарная группа считается базовым вариантом; меньшие группы перечисляются как отклонения с явным указанием того, чем именно они отличаются.

Этот отчёт **не дублирует**, а дополняет [сравнением наций](../../docs/reports/nations/overview.md). Оно даёт обзор «у кого что есть» (roster size, building coverage, рынок-кластеры) и top-10 stat-anomalies по HP-разбросу. Здесь же перечисляются полные стат-отпечатки.

Содержание:

- [§1. Здания общего класса (Городской центр, Казармы, Академия и т. д.)](#1-здания-общего-класса)
- [§2. Юниты, общие для нескольких наций](#2-юниты-общие-для-нескольких-наций)

## §1. Здания общего класса

Для каждого семейства зданий — `<nat>` + суффикс — собираются записи всех наций, у которых это здание есть. Затем нации группируются по идентичности стат-отпечатка: значения, которые в скрипте читаются через `SetObjBuildingProperties` / `SetObjBuildingExtProperties`. Если у нации этого здания нет (например, Украина без Башни и каменных стен — см. [сравнении наций](../../docs/reports/nations/overview.md), она в данной группе не появляется.

Тип «отпечатка»: HP · buildtime · costpercent · цена · score · vision · farm · peasantabsorber · consume · weapon (damage/pause/radiusmax) · produces.

### `<nat>cen` — Городской центр

- **Базовый вариант** (7/21): **bav** Бавария, **hun** Венгрия, **pie** Пьемонт, **por** Португалия, **sax** Саксония … (+2)
  - HP **4000**, buildtime **156.25** g-сек, costpercent **300**
  - цена: 700 W · 700 S
  - score=1000, farm=100
  - produces: peaaus, peaeng, peapol, pearus, peasco, peaspa, peatur, peaukr

- **Отклонение 1** (2/21): **den** Дания, **eng** Англия
  - HP **4030**, buildtime **156.25** g-сек, costpercent **300**
  - цена: 700 W · 700 S
  - score=1000, farm=100
  - produces: peaaus, peaeng, peapol, pearus, peasco, peaspa, peatur, peaukr

- **Отклонение 2** (1/21): **aus** Австрия
  - HP **4000**, buildtime **46.88** g-сек, costpercent **300**
  - цена: 700 W · 700 S
  - score=1000, farm=100
  - produces: peaaus, peaeng, peapol, pearus, peasco, peaspa, peatur, peaukr

- **Отклонение 3** (1/21): **fra** Франция
  - HP **4500**, buildtime **156.25** g-сек, costpercent **300**
  - цена: 700 W · 700 S
  - score=1000, farm=100
  - produces: peaaus, peaeng, peapol, pearus, peasco, peaspa, peatur, peaukr

- **Отклонение 4** (1/21): **spa** Испания
  - HP **4250**, buildtime **156.25** g-сек, costpercent **300**
  - цена: 700 W · 700 S
  - score=1000, farm=100
  - produces: peaaus, peaeng, peapol, pearus, peasco, peaspa, peatur, peaukr

- **Отклонение 5** (1/21): **rus** Россия
  - HP **4050**, buildtime **156.25** g-сек, costpercent **300**
  - цена: 680 W · 700 S
  - score=1000, farm=75
  - produces: peaaus, peaeng, peapol, pearus, peasco, peaspa, peatur, peaukr

- **Отклонение 6** (1/21): **ukr** Украина
  - HP **5300**, buildtime **156.25** g-сек, costpercent **400**
  - цена: 700 W
  - score=1000, farm=200
  - produces: peaaus, peaeng, peapol, pearus, peasco, peaspa, peatur, peaukr

- **Отклонение 7** (1/21): **pol** Польша
  - HP **4300**, buildtime **156.25** g-сек, costpercent **300**
  - цена: 700 W · 700 S
  - score=1000, farm=100
  - produces: peaaus, peaeng, peapol, pearus, peasco, peaspa, peatur, peaukr

- **Отклонение 8** (1/21): **swe** Швеция
  - HP **5000**, buildtime **156.25** g-сек, costpercent **300**
  - цена: 700 W · 700 S
  - score=1000, farm=100
  - produces: peaaus, peaeng, peapol, pearus, peasco, peaspa, peatur, peaukr

- **Отклонение 9** (1/21): **pru** Пруссия
  - HP **4200**, buildtime **156.25** g-сек, costpercent **300**
  - цена: 700 W · 700 S
  - score=1000, farm=100
  - produces: peaaus, peaeng, peapol, pearus, peasco, peaspa, peatur, peaukr

- **Отклонение 10** (1/21): **ven** Венеция
  - HP **5100**, buildtime **156.25** g-сек, costpercent **300**
  - цена: 700 W · 700 S
  - score=1000, farm=100
  - produces: peaaus, peaeng, peapol, pearus, peasco, peaspa, peatur, peaukr

- **Отклонение 11** (1/21): **tur** Турция
  - HP **4000**, buildtime **156.25** g-сек, costpercent **300**
  - цена: 600 W · 500 S
  - score=1000, farm=100
  - produces: peaaus, peaeng, peapol, pearus, peasco, peaspa, peatur, peaukr

- **Отклонение 12** (1/21): **alg** Алжир
  - HP **5500**, buildtime **156.25** g-сек, costpercent **300**
  - цена: 450 W · 700 S
  - score=1000, farm=50
  - produces: peaaus, peaeng, peapol, pearus, peasco, peaspa, peatur, peaukr

- **Отклонение 13** (1/21): **net** Нидерланды
  - HP **4950**, buildtime **156.25** g-сек, costpercent **300**
  - цена: 700 W · 700 S
  - score=1000, farm=100
  - produces: peaaus, peaeng, peapol, pearus, peasco, peaspa, peatur, peaukr


### `<nat>hou` — Дом / ферма

- **Базовый вариант** (10/21): **aus** Австрия, **bav** Бавария, **den** Дания, **fra** Франция, **hun** Венгрия … (+5)
  - HP **4000**, buildtime **31.25** g-сек, costpercent **104**
  - цена: 100 W · 100 S
  - score=100, farm=25
  - produces: —

- **Отклонение 1** (3/21): **eng** Англия, **swe** Швеция, **ven** Венеция
  - HP **5000**, buildtime **31.25** g-сек, costpercent **104**
  - цена: 100 W · 100 S
  - score=100, farm=25
  - produces: —

- **Отклонение 2** (2/21): **net** Нидерланды, **pru** Пруссия
  - HP **4500**, buildtime **31.25** g-сек, costpercent **104**
  - цена: 100 W · 100 S
  - score=100, farm=25
  - produces: —

- **Отклонение 3** (1/21): **spa** Испания
  - HP **4200**, buildtime **31.25** g-сек, costpercent **104**
  - цена: 100 W · 100 S
  - score=100, farm=25
  - produces: —

- **Отклонение 4** (1/21): **rus** Россия
  - HP **5000**, buildtime **31.25** g-сек, costpercent **104**
  - цена: 120 W
  - score=100, farm=25
  - produces: —

- **Отклонение 5** (1/21): **ukr** Украина
  - HP **4150**, buildtime **31.25** g-сек, costpercent **105**
  - цена: 120 W
  - score=100, farm=25
  - produces: —

- **Отклонение 6** (1/21): **pol** Польша
  - HP **4100**, buildtime **31.25** g-сек, costpercent **104**
  - цена: 100 W · 100 S
  - score=100, farm=25
  - produces: —

- **Отклонение 7** (1/21): **tur** Турция
  - HP **4000**, buildtime **31.25** g-сек, costpercent **106**
  - цена: 100 W · 100 S
  - score=100, farm=25
  - produces: —

- **Отклонение 8** (1/21): **alg** Алжир
  - HP **4300**, buildtime **31.25** g-сек, costpercent **104**
  - цена: 100 W · 100 S
  - score=100, farm=25
  - produces: —


### `<nat>bar` — Казарма XVII в.

- **Базовый вариант** (16/21): **aus** Австрия, **bav** Бавария, **den** Дания, **eng** Англия, **fra** Франция … (+11)
  - HP **40000**, buildtime **93.75** g-сек, costpercent **500**
  - цена: 100 W · 100 S · 500 G
  - score=500, farm=150
  - produces: archer, archertur, drummer, drummerrus, drummertur, gauduk, jannisary, lightinfantry, musketeer, musketeeraus, musketeernet, musketeerpol, musketeersco, musketeerspa, officer, officerrus, officersco, officertur, pikeman, pikemanpol, pikemanpor, pikemanrus, pikemansco, pikemanspa, pikemanswi, pikemantur, roundshier, serdiuk, strelet

- **Отклонение 1** (2/21): **alg** Алжир, **tur** Турция
  - HP **35000**, buildtime **93.75** g-сек, costpercent **500**
  - цена: 400 W · 400 S
  - score=500, farm=50
  - produces: archer, archertur, drummer, drummerrus, drummertur, gauduk, jannisary, lightinfantry, musketeer, musketeeraus, musketeernet, musketeerpol, musketeersco, musketeerspa, officer, officerrus, officersco, officertur, pikeman, pikemanpol, pikemanpor, pikemanrus, pikemansco, pikemanspa, pikemanswi, pikemantur, roundshier, serdiuk, strelet

- **Отклонение 2** (1/21): **rus** Россия
  - HP **25000**, buildtime **78.12** g-сек, costpercent **300**
  - цена: 200 W · 20 S
  - score=500, farm=25
  - produces: archer, archertur, drummer, drummerrus, drummertur, gauduk, jannisary, lightinfantry, musketeer, musketeeraus, musketeernet, musketeerpol, musketeersco, musketeerspa, officer, officerrus, officersco, officertur, pikeman, pikemanpol, pikemanpor, pikemanrus, pikemansco, pikemanspa, pikemanswi, pikemantur, roundshier, serdiuk, strelet

- **Отклонение 3** (1/21): **ukr** Украина
  - HP **20000**, buildtime **93.75** g-сек, costpercent **300**
  - цена: 150 W · 150 S
  - score=500, farm=75
  - produces: archer, archertur, drummer, drummerrus, drummertur, gauduk, jannisary, lightinfantry, musketeer, musketeeraus, musketeernet, musketeerpol, musketeersco, musketeerspa, officer, officerrus, officersco, officertur, pikeman, pikemanpol, pikemanpor, pikemanrus, pikemansco, pikemanspa, pikemanswi, pikemantur, roundshier, serdiuk, strelet

- **Отклонение 4** (1/21): **sco** Шотландия
  - HP **30000**, buildtime **93.75** g-сек, costpercent **500**
  - цена: 100 W · 100 S · 500 G
  - score=500, farm=150
  - produces: archer, archertur, bagpiper, drummer, drummerrus, drummertur, gauduk, jannisary, lightinfantry, musketeer, musketeeraus, musketeernet, musketeerpol, musketeersco, musketeerspa, officer, officerrus, officersco, officertur, pikeman, pikemanpol, pikemanpor, pikemanrus, pikemansco, pikemanspa, pikemanswi, pikemantur, roundshier, serdiuk, strelet


### `<nat>ba2` — Казарма XVIII в.

- **Базовый вариант** (17/21): **aus** Австрия, **bav** Бавария, **den** Дания, **eng** Англия, **fra** Франция … (+12)
  - HP **55000**, buildtime **5625.0** g-сек, costpercent **200**
  - цена: 1700 W · 2950 S · 4000 G
  - score=500, farm=250
  - produces: archersco, bagpiper, chasseur, drummer18, grenadier, grenadierbav, grenadierden, grenadierhun, grenadierpru, grenadiersax, highlander, jagerpor, jagerswi, musketeer18, musketeer18bav, musketeer18den, musketeer18pru, musketeer18sax, officer18, pandur, pandurhun, pikeman18, pikeman18swe, swordsmansco

- **Отклонение 1** (1/21): **sco** Шотландия
  - HP **40000**, buildtime **625.0** g-сек, costpercent **250**
  - цена: 640 W · 2400 S · 2400 G
  - score=500, farm=150
  - produces: archersco, chasseur, drummer18, grenadier, grenadierbav, grenadierden, grenadierhun, grenadierpru, grenadiersax, highlander, jagerpor, jagerswi, musketeer18, musketeer18bav, musketeer18den, musketeer18pru, musketeer18sax, officer18, pandur, pandurhun, pikeman18, pikeman18swe, swordsmansco


### `<nat>sta` — Конюшня

- **Базовый вариант** (14/21): **aus** Австрия, **bav** Бавария, **den** Дания, **fra** Франция, **net** Нидерланды … (+9)
  - HP **20000**, buildtime **625.0** g-сек, costpercent **200**
  - цена: 2500 W · 100 S · 600 G
  - score=500
  - produces: cossackdon, cossackregister, cossacksich, croat, cuirassier, dragoon, dragoon18, dragoon18fra, dragoon18net, dragoon18pie, dragoonpol, guardcavalrysax, hackapell, hetman, hussar, hussarhun, hussarpru, hussarswi, kingmusketeer, lancersco, mameluke, raidersco, reiter, reiterpol, reiterswe, sipahi, spakh, tatar, vityaz, wingedhussar

- **Отклонение 1** (2/21): **eng** Англия, **sco** Шотландия
  - HP **25000**, buildtime **375.0** g-сек, costpercent **200**
  - цена: 2350 W · 800 G
  - score=500
  - produces: cossackdon, cossackregister, cossacksich, croat, cuirassier, dragoon, dragoon18, dragoon18fra, dragoon18net, dragoon18pie, dragoonpol, guardcavalrysax, hackapell, hetman, hussar, hussarhun, hussarpru, hussarswi, kingmusketeer, lancersco, mameluke, raidersco, reiter, reiterpol, reiterswe, sipahi, spakh, tatar, vityaz, wingedhussar

- **Отклонение 2** (1/21): **rus** Россия
  - HP **25000**, buildtime **375.0** g-сек, costpercent **200**
  - цена: 7950 W · 550 G
  - score=500
  - produces: cossackdon, cossackregister, cossacksich, croat, cuirassier, dragoon, dragoon18, dragoon18fra, dragoon18net, dragoon18pie, dragoonpol, guardcavalrysax, hackapell, hetman, hussar, hussarhun, hussarpru, hussarswi, kingmusketeer, lancersco, mameluke, raidersco, reiter, reiterpol, reiterswe, sipahi, spakh, tatar, vityaz, wingedhussar

- **Отклонение 3** (1/21): **ukr** Украина
  - HP **10000**, buildtime **156.25** g-сек, costpercent **300**
  - цена: 3200 W · 850 S · 850 G
  - score=500
  - produces: cossackdon, cossackregister, cossacksich, croat, cuirassier, dragoon, dragoon18, dragoon18fra, dragoon18net, dragoon18pie, dragoonpol, guardcavalrysax, hackapell, hetman, hussar, hussarhun, hussarpru, hussarswi, kingmusketeer, lancersco, mameluke, raidersco, reiter, reiterpol, reiterswe, sipahi, spakh, tatar, vityaz, wingedhussar

- **Отклонение 4** (1/21): **tur** Турция
  - HP **55000**, buildtime **156.25** g-сек, costpercent **700**
  - цена: 1000 W · 2600 S
  - score=500
  - produces: cossackdon, cossackregister, cossacksich, croat, cuirassier, dragoon, dragoon18, dragoon18fra, dragoon18net, dragoon18pie, dragoonpol, guardcavalrysax, hackapell, hetman, hussar, hussarhun, hussarpru, hussarswi, kingmusketeer, lancersco, mameluke, raidersco, reiter, reiterpol, reiterswe, sipahi, spakh, tatar, vityaz, wingedhussar

- **Отклонение 5** (1/21): **alg** Алжир
  - HP **55000**, buildtime **156.25** g-сек, costpercent **700**
  - цена: 1000 W · 2200 S
  - score=500
  - produces: cossackdon, cossackregister, cossacksich, croat, cuirassier, dragoon, dragoon18, dragoon18fra, dragoon18net, dragoon18pie, dragoonpol, guardcavalrysax, hackapell, hetman, hussar, hussarhun, hussarpru, hussarswi, kingmusketeer, lancersco, mameluke, raidersco, reiter, reiterpol, reiterswe, sipahi, spakh, tatar, vityaz, wingedhussar

- **Отклонение 6** (1/21): **hun** Венгрия
  - HP **20000**, buildtime **625.0** g-сек, costpercent **200**
  - цена: 2500 W · 100 S · 600 G
  - score=500
  - produces: cossackdon, cossackregister, cossacksich, croat, cuirassier, dragoon, dragoon18, dragoon18fra, dragoon18net, dragoon18pie, dragoonpol, guardcavalrysax, hackapell, hetman, hussar, hussarhun, hussarpru, hussarswi, kingmusketeer, lancersco, lightcavalry, mameluke, raidersco, reiter, reiterpol, reiterswe, sipahi, spakh, tatar, vityaz, wingedhussar


### `<nat>aca` — Академия

- **Базовый вариант** (8/21): **bav** Бавария, **fra** Франция, **hun** Венгрия, **pie** Пьемонт, **por** Португалия … (+3)
  - HP **63000**, buildtime **625.0** g-сек, costpercent **300**
  - цена: 1250 W · 1100 S
  - score=500
  - produces: —

- **Отклонение 1** (2/21): **spa** Испания, **swe** Швеция
  - HP **63000**, buildtime **625.0** g-сек, costpercent **300**
  - цена: 1350 W · 1000 S
  - score=500
  - produces: —

- **Отклонение 2** (2/21): **alg** Алжир, **tur** Турция
  - HP **65000**, buildtime **156.25** g-сек, costpercent **300**
  - цена: 1450 W · 1100 S
  - score=500
  - produces: —

- **Отклонение 3** (1/21): **aus** Австрия
  - HP **65000**, buildtime **625.0** g-сек, costpercent **300**
  - цена: 1250 W · 1100 S
  - score=500
  - produces: —

- **Отклонение 4** (1/21): **eng** Англия
  - HP **63000**, buildtime **625.0** g-сек, costpercent **300**
  - цена: 1150 W · 1200 S
  - score=500
  - produces: —

- **Отклонение 5** (1/21): **rus** Россия
  - HP **65000**, buildtime **843.75** g-сек, costpercent **300**
  - цена: 1250 W · 1300 S
  - score=500
  - produces: —

- **Отклонение 6** (1/21): **ukr** Украина
  - HP **65000**, buildtime **46.88** g-сек, costpercent **300**
  - цена: 1350 W · 1200 S
  - score=500
  - produces: —

- **Отклонение 7** (1/21): **pol** Польша
  - HP **63000**, buildtime **625.0** g-сек, costpercent **300**
  - цена: 950 W · 800 S
  - score=500
  - produces: —

- **Отклонение 8** (1/21): **pru** Пруссия
  - HP **63000**, buildtime **625.0** g-сек, costpercent **300**
  - цена: 1200 W · 1150 S
  - score=500
  - produces: —

- **Отклонение 9** (1/21): **ven** Венеция
  - HP **63000**, buildtime **625.0** g-сек, costpercent **300**
  - цена: 1090 W · 1260 S
  - score=500
  - produces: —

- **Отклонение 10** (1/21): **net** Нидерланды
  - HP **63000**, buildtime **625.0** g-сек, costpercent **300**
  - цена: 1050 W · 1230 S
  - score=500
  - produces: —

- **Отклонение 11** (1/21): **den** Дания
  - HP **63000**, buildtime **625.0** g-сек, costpercent **300**
  - цена: 1450 W · 900 S
  - score=500
  - produces: —


### `<nat>bla` — Кузница

- **Базовый вариант** (17/21): **aus** Австрия, **bav** Бавария, **den** Дания, **eng** Англия, **hun** Венгрия … (+12)
  - HP **5500**, buildtime **93.75** g-сек, costpercent **400**
  - цена: 100 W · 30 S · 640 I
  - score=500
  - produces: —

- **Отклонение 1** (2/21): **alg** Алжир, **tur** Турция
  - HP **6500**, buildtime **109.38** g-сек, costpercent **400**
  - цена: 100 W · 30 S · 640 I
  - score=500
  - produces: —

- **Отклонение 2** (1/21): **fra** Франция
  - HP **5500**, buildtime **93.75** g-сек, costpercent **600**
  - цена: 100 W · 30 S · 640 I
  - score=500
  - produces: —

- **Отклонение 3** (1/21): **ukr** Украина
  - HP **4500**, buildtime **62.5** g-сек, costpercent **400**
  - цена: 100 W · 30 S · 640 I
  - score=500
  - produces: —


### `<nat>art` — Артиллерийское депо

- **Базовый вариант** (19/21): **alg** Алжир, **aus** Австрия, **bav** Бавария, **den** Дания, **eng** Англия … (+14)
  - HP **40000**, buildtime **245.94** g-сек, costpercent **200**
  - цена: 100 W · 1000 S · 1400 C
  - score=500
  - produces: cannon, framegun, howitzer, mortar, multicannon

- **Отклонение 1** (1/21): **ukr** Украина
  - HP **40000**, buildtime **245.94** g-сек, costpercent **200**
  - цена: 4250 W · 4400 S · 100 G · 1400 C
  - score=500
  - produces: cannon, framegun, howitzer, mortar, multicannon

- **Отклонение 2** (1/21): **tur** Турция
  - HP **40000**, buildtime **245.94** g-сек, costpercent **200**
  - цена: 500 W · 1200 S · 1400 C
  - score=500
  - produces: cannon, framegun, howitzer, mortar, multicannon


### `<nat>dip` — Дипломатический центр

- **Базовый вариант** (17/21): **aus** Австрия, **bav** Бавария, **den** Дания, **eng** Англия, **fra** Франция … (+12)
  - HP **4500**, buildtime **312.5** g-сек, costpercent **100**
  - цена: 4900 W · 1700 S
  - score=500
  - produces: archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip, lightcavalrydip, lightinfantrydip, roundshierdip

- **Отклонение 1** (2/21): **alg** Алжир, **tur** Турция
  - HP **5500**, buildtime **312.5** g-сек, costpercent **100**
  - цена: 4600 W · 2020 S
  - score=500
  - produces: archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip, lightcavalrydip, lightinfantrydip, roundshierdip

- **Отклонение 2** (1/21): **rus** Россия
  - HP **6500**, buildtime **312.5** g-сек, costpercent **100**
  - цена: 7900 W · 3700 S
  - score=500
  - produces: archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip, lightcavalrydip, lightinfantrydip, roundshierdip

- **Отклонение 3** (1/21): **ukr** Украина
  - HP **5000**, buildtime **312.5** g-сек, costpercent **100**
  - цена: 3900 W · 2700 S
  - score=500
  - produces: archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip, lightcavalrydip, lightinfantrydip, roundshierdip


### `<nat>tem` — Храм

- **Базовый вариант** (16/21): **aus** Австрия, **bav** Бавария, **den** Дания, **eng** Англия, **hun** Венгрия … (+11)
  - HP **4200**, buildtime **156.25** g-сек, costpercent **300**
  - цена: 1000 W · 1200 S · 500 I
  - score=500
  - produces: mullah, padre, pope, priest

- **Отклонение 1** (2/21): **alg** Алжир, **tur** Турция
  - HP **5000**, buildtime **93.75** g-сек, costpercent **300**
  - цена: 1000 W · 1200 S · 500 I
  - score=500
  - produces: mullah, padre, pope, priest

- **Отклонение 2** (1/21): **fra** Франция
  - HP **6000**, buildtime **312.5** g-сек, costpercent **300**
  - цена: 1100 W · 2000 S · 600 I
  - score=500
  - produces: mullah, padre, pope, priest

- **Отклонение 3** (1/21): **rus** Россия
  - HP **4500**, buildtime **156.25** g-сек, costpercent **300**
  - цена: 1150 W · 1650 S · 100 G · 500 I
  - score=500
  - produces: mullah, padre, pope, priest

- **Отклонение 4** (1/21): **ukr** Украина
  - HP **5300**, buildtime **156.25** g-сек, costpercent **300**
  - цена: 1100 W · 1400 S · 300 I
  - score=500
  - produces: mullah, padre, pope, priest


## §2. Юниты, общие для нескольких наций

Берётся каждый sid юнита, у которого есть запись хотя бы у двух наций (если у одной — это уникальный юнит, описывается в [сравнении наций](../../docs/reports/nations/overview.md). Записи группируются по стат-отпечатку (HP / buildtime / цена / щит / скорость / защиты / consume / weapon-набор). Юниты с одинаковым отпечатком сливаются в одну группу.

Если у sid'а одна группа на все доступные нации — отклонений нет, и он здесь не показывается. Если разные — перечисляются базовый вариант (мажоритарный) и отклонения.

### `archerdip` — Лучник

- **Базовый вариант** (20 наций): **alg** Алжир, **aus** Австрия, **bav** Бавария, **den** Дания, **eng** Англия … (+15)
  - HP **20**, цена: 15 G, buildtime **1.25** g-сек, speed 32
  - score=1, costpercent=100.5
  - consume: 16 G/тик
  - weapon[0]: 25 dmg · pause 2.5 s · range 13.13 t · arrow, disp 3.75t
  - weapon[1]: 100 dmg · pause 0.78 s · range 14.06 t · firearrow, disp 3.75t

- **Отклонение 1** (1 нация): **sco** Шотландия
  - HP **20**, цена: 15 G, buildtime **1.25** g-сек, speed 32
  - score=1, costpercent=100.5
  - consume: 39 F/тик · 16 G/тик
  - weapon[0]: 25 dmg · pause 2.5 s · range 13.13 t · arrow, disp 3.75t
  - weapon[1]: 100 dmg · pause 0.78 s · range 14.06 t · firearrow, disp 3.75t

### `archerturdip` — Лучник

- **Базовый вариант** (20 наций): **alg** Алжир, **aus** Австрия, **bav** Бавария, **den** Дания, **eng** Англия … (+15)
  - HP **20**, цена: 15 G, buildtime **1.25** g-сек, speed 32
  - score=1, costpercent=100.5
  - consume: 16 G/тик
  - weapon[0]: 25 dmg · pause 2.5 s · range 13.13 t · arrow, disp 3.75t
  - weapon[1]: 100 dmg · pause 0.78 s · range 14.06 t · firearrow, disp 3.75t

- **Отклонение 1** (1 нация): **sco** Шотландия
  - HP **20**, цена: 15 G, buildtime **1.25** g-сек, speed 32
  - score=1, costpercent=100.5
  - consume: 39 F/тик · 16 G/тик
  - weapon[0]: 25 dmg · pause 2.5 s · range 13.13 t · arrow, disp 3.75t
  - weapon[1]: 100 dmg · pause 0.78 s · range 14.06 t · firearrow, disp 3.75t

### `drummer18` — Лёгкая пехота

- **Базовый вариант** (15 наций): **aus** Австрия, **bav** Бавария, **den** Дания, **fra** Франция, **hun** Венгрия … (+10)
  - HP **100**, цена: 50 F · 30 G, buildtime **6.0** g-сек, speed 32
  - score=10

- **Отклонение 1** (1 нация): **rus** Россия
  - HP **100**, цена: 90 F · 15 G, buildtime **6.0** g-сек, speed 32
  - score=10

### `pikeman` — Лёгкая пехота

- **Базовый вариант** (12 наций): **aus** Австрия, **bav** Бавария, **den** Дания, **eng** Англия, **fra** Франция … (+7)
  - HP **90**, цена: 25 F · 3 G · 20 I, buildtime **4.5** g-сек, speed 32
  - score=10
  - prot: pike=3, sword=2, bullet=4, cannister=210, arrow=6, cannonball=40
  - weapon[0]: 8 dmg · pause 0.0 s · range 1.88 t · pike

- **Отклонение 1** (1 нация): **spa** Испания
  - HP **100**, цена: 35 F · 7 G · 30 I, buildtime **5.5** g-сек, speed 32
  - score=10
  - prot: pike=3, sword=4, bullet=6, cannister=240, arrow=12, cannonball=50
  - weapon[0]: 10 dmg · pause 0.0 s · range 1.88 t · pike

### `roundshierdip` — Лёгкая пехота

- **Базовый вариант** (20 наций): **alg** Алжир, **aus** Австрия, **bav** Бавария, **den** Дания, **eng** Англия … (+15)
  - HP **75**, цена: 12 G, buildtime **1.5** g-сек, speed 32
  - score=1
  - prot: pike=5, sword=3, bullet=8, cannister=225, arrow=17, cannonball=80
  - consume: 20 G/тик
  - weapon[0]: 6 dmg · pause 0.0 s · range 1.13 t · sword

- **Отклонение 1** (1 нация): **sco** Шотландия
  - HP **75**, цена: 12 G, buildtime **1.5** g-сек, speed 32
  - score=1
  - prot: pike=5, sword=3, bullet=8, cannister=225, arrow=17, cannonball=80
  - consume: 45 F/тик · 20 G/тик
  - weapon[0]: 6 dmg · pause 0.0 s · range 1.13 t · sword


Всего юнитов с межнациональными отклонениями: **5**.
