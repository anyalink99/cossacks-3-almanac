<a id="национальные-отклонения--здания-и-юниты"></a>
# National deviations - buildings and units

**Derived** file (calculated, not extracted). Counted from [`data.json`](../../../data.json) as script [`compute/compute_nation_deviations.py`](../../../compute/compute_nation_deviations.py).

The goal is to collect in one place ALL the places where a particular nation has a stat value for a building or a general unit that differs from what the majority have. The source of the deltas is `case i of nation:` branches in `unit.script`, which overwrite `SetObjBuildingProperties` / `SetObjBaseWeapon` for individual nations.

Format: for each family (for example, `<nat>cen` - Town Hall) 21 nations are grouped by “fingerprint” - a tuple of significant stats. The majority group is considered the base case; smaller groups are listed as outliers, with an explicit indication of how exactly they differ.

This report **does not duplicate**, but complements [`reports/nations/overview.md`](overview.md). overview gives an overview of “who has what” (roster size, building coverage, market clusters) and top-10 stat-anomalies by HP spread. Full stat fingerprints are also listed here.

Contents:

- [§1. General class buildings (Town Hall, Barracks, Academy, etc.)](#1-здания-общего-класса)
- [§2. Units common to several nations](#2-юниты-общие-для-нескольких-наций)

<a id="1-здания-общего-класса"></a>
## §1. General class buildings

For each building family - `<nat>` + suffix - records of all nations that have that building are collected. Nations are then grouped by stat fingerprint identity: values ​​that are read in the script by `SetObjBuildingProperties` / `SetObjBuildingExtProperties`. If a nation does not have this building (for example, Ukraine without Towers and stone walls - see [`overview.md` §2](overview.md)), it does not appear in this group.

Fingerprint type: HP · buildtime · costpercent · price · score · vision · farm · peasantabsorber · consume · weapon (damage/pause/radiusmax) · produces.

<a id="cen--городской-центр"></a>
### `<nat>cen` — Town Hall

- **Basic option** (7/21): **bav** Bavaria, **hun** Hungary, **pie** Piedmont, **por** Portugal, **sax** Saxony … (+2)
  - HP **4000**, buildtime **156.25** g-sec, costpercent **300**
  - price: 700 W · 700 S
  - score=1000, farm=100
  - produces: peaaus, peaeng, peapol, pearus, peasco, peaspa, peatur, peaukr

- **Deviation 1** (2/21): **den** Denmark, **eng** England
  - HP **4030**, buildtime **156.25** g-sec, costpercent **300**
  - price: 700 W · 700 S
  - score=1000, farm=100
  - produces: peaaus, peaeng, peapol, pearus, peasco, peaspa, peatur, peaukr

- **Deviation 2** (1/21): **aus** Austria
  - HP **4000**, buildtime **46.88** g-sec, costpercent **300**
  - price: 700 W · 700 S
  - score=1000, farm=100
  - produces: peaaus, peaeng, peapol, pearus, peasco, peaspa, peatur, peaukr

- **Deviation 3** (1/21): **fra** France
  - HP **4500**, buildtime **156.25** g-sec, costpercent **300**
  - price: 700 W · 700 S
  - score=1000, farm=100
  - produces: peaaus, peaeng, peapol, pearus, peasco, peaspa, peatur, peaukr

- **Deviation 4** (1/21): **spa** Spain
  - HP **4250**, buildtime **156.25** g-sec, costpercent **300**
  - price: 700 W · 700 S
  - score=1000, farm=100
  - produces: peaaus, peaeng, peapol, pearus, peasco, peaspa, peatur, peaukr

- **Deviation 5** (1/21): **rus** Russia
  - HP **4050**, buildtime **156.25** g-sec, costpercent **300**
  - price: 680 W · 700 S
  - score=1000, farm=75
  - produces: peaaus, peaeng, peapol, pearus, peasco, peaspa, peatur, peaukr

- **Deviation 6** (1/21): **ukr** Ukraine
  - HP **5300**, buildtime **156.25** g-sec, costpercent **400**
  - price: 700 W
  - score=1000, farm=200
- produces: peaaus, peaeng, peapol, pearus, peasco, peaspa, peatur, peaukr

- **Deviation 7** (1/21): **pol** Poland
  - HP **4300**, buildtime **156.25** g-sec, costpercent **300**
  - price: 700 W · 700 S
  - score=1000, farm=100
  - produces: peaaus, peaeng, peapol, pearus, peasco, peaspa, peatur, peaukr

- **Deviation 8** (1/21): **swe** Sweden
  - HP **5000**, buildtime **156.25** g-sec, costpercent **300**
  - price: 700 W · 700 S
  - score=1000, farm=100
  - produces: peaaus, peaeng, peapol, pearus, peasco, peaspa, peatur, peaukr

- **Deviation 9** (1/21): **pru** Prussia
  - HP **4200**, buildtime **156.25** g-sec, costpercent **300**
  - price: 700 W · 700 S
  - score=1000, farm=100
  - produces: peaaus, peaeng, peapol, pearus, peasco, peaspa, peatur, peaukr

- **Deviation 10** (1/21): **ven** Venice
  - HP **5100**, buildtime **156.25** g-sec, costpercent **300**
  - price: 700 W · 700 S
  - score=1000, farm=100
  - produces: peaaus, peaeng, peapol, pearus, peasco, peaspa, peatur, peaukr

- **Deviation 11** (1/21): **tur** Turkey
  - HP **4000**, buildtime **156.25** g-sec, costpercent **300**
  - price: 600 W · 500 S
  - score=1000, farm=100
  - produces: peaaus, peaeng, peapol, pearus, peasco, peaspa, peatur, peaukr

- **Deviation 12** (1/21): **alg** Algeria
  - HP **5500**, buildtime **156.25** g-sec, costpercent **300**
  - price: 450 W · 700 S
  - score=1000, farm=50
  - produces: peaaus, peaeng, peapol, pearus, peasco, peaspa, peatur, peaukr

- **Deviation 13** (1/21): **net** Netherlands
  - HP **4950**, buildtime **156.25** g-sec, costpercent **300**
  - price: 700 W · 700 S
  - score=1000, farm=100
  - produces: peaaus, peaeng, peapol, pearus, peasco, peaspa, peatur, peaukr


<a id="hou--дом--ферма"></a>
### `<nat>hou` - Housing / farm

- **Basic option** (10/21): **aus** Austria, **bav** Bavaria, **den** Denmark, **fra** France, **hun** Hungary … (+5)
  - HP **4000**, buildtime **31.25** g-sec, costpercent **104**
  - price: 100 W · 100 S
  - score=100, farm=25
  - produces: —

- **Deviation 1** (3/21): **eng** England, **swe** Sweden, **ven** Venice
  - HP **5000**, buildtime **31.25** g-sec, costpercent **104**
  - price: 100 W · 100 S
  - score=100, farm=25
  - produces: —

- **Deviation 2** (2/21): **net** Netherlands, **pru** Prussia
  - HP **4500**, buildtime **31.25** g-sec, costpercent **104**
  - price: 100 W · 100 S
  - score=100, farm=25
  - produces: —

- **Deviation 3** (1/21): **spa** Spain
  - HP **4200**, buildtime **31.25** g-sec, costpercent **104**
  - price: 100 W · 100 S
  - score=100, farm=25
  - produces: —

- **Deviation 4** (1/21): **rus** Russia
  - HP **5000**, buildtime **31.25** g-sec, costpercent **104**
  - price: 120 W
  - score=100, farm=25
  - produces: —

- **Deviation 5** (1/21): **ukr** Ukraine
  - HP **4150**, buildtime **31.25** g-sec, costpercent **105**
  - price: 120 W
  - score=100, farm=25
  - produces: —

- **Deviation 6** (1/21): **pol** Poland
  - HP **4100**, buildtime **31.25** g-sec, costpercent **104**
  - price: 100 W · 100 S
  - score=100, farm=25
  - produces: —

- **Deviation 7** (1/21): **tur** Turkey
  - HP **4000**, buildtime **31.25** g-sec, costpercent **106**
  - price: 100 W · 100 S
  - score=100, farm=25
  - produces: —

- **Deviation 8** (1/21): **alg** Algeria
  - HP **4300**, buildtime **31.25** g-sec, costpercent **104**
  - price: 100 W · 100 S
  - score=100, farm=25
  - produces: —


<a id="bar--казарма-xvii-в"></a>
### `<nat>bar` — Barracks XVII century.

- **Basic option** (16/21): **aus** Austria, **bav** Bavaria, **den** Denmark, **eng** England, **fra** France … (+11)
- HP **40000**, buildtime **93.75** g-sec, costpercent **500**
  - price: 100 W · 100 S · 500 G
  - score=500, farm=150
  - produces: archer, archertur, drummer, drummerrus, drummertur, gauduk, jannisary, lightinfantry, musketeer, musketeeraus, musketeernet, musketeerpol, musketeersco, musketeerspa, officer, officerrus, officersco, officertur, pikeman, pikemanpol, pikemanpor, pikemanrus, pikemansco, pikemanspa, pikemanswi, pikemantur, roundshier, serdiuk, strelet

- **Deviation 1** (2/21): **alg** Algeria, **tur** Turkey
  - HP **35000**, buildtime **93.75** g-sec, costpercent **500**
  - price: 400 W · 400 S
  - score=500, farm=50
  - produces: archer, archertur, drummer, drummerrus, drummertur, gauduk, jannisary, lightinfantry, musketeer, musketeeraus, musketeernet, musketeerpol, musketeersco, musketeerspa, officer, officerrus, officersco, officertur, pikeman, pikemanpol, pikemanpor, pikemanrus, pikemansco, pikemanspa, pikemanswi, pikemantur, roundshier, serdiuk, strelet

- **Deviation 2** (1/21): **rus** Russia
  - HP **25000**, buildtime **78.12** g-sec, costpercent **300**
  - price: 200 W 20 S
  - score=500, farm=25
  - produces: archer, archertur, drummer, drummerrus, drummertur, gauduk, jannisary, lightinfantry, musketeer, musketeeraus, musketeernet, musketeerpol, musketeersco, musketeerspa, officer, officerrus, officersco, officertur, pikeman, pikemanpol, pikemanpor, pikemanrus, pikemansco, pikemanspa, pikemanswi, pikemantur, roundshier, serdiuk, strelet

- **Deviation 3** (1/21): **ukr** Ukraine
  - HP **20000**, buildtime **93.75** g-sec, costpercent **300**
  - price: 150 W · 150 S
  - score=500, farm=75
  - produces: archer, archertur, drummer, drummerrus, drummertur, gauduk, jannisary, lightinfantry, musketeer, musketeeraus, musketeernet, musketeerpol, musketeersco, musketeerspa, officer, officerrus, officersco, officertur, pikeman, pikemanpol, pikemanpor, pikemanrus, pikemansco, pikemanspa, pikemanswi, pikemantur, roundshier, serdiuk, strelet

- **Deviation 4** (1/21): **sco** Scotland
  - HP **30000**, buildtime **93.75** g-sec, costpercent **500**
  - price: 100 W · 100 S · 500 G
  - score=500, farm=150
  - produces: archer, archertur, bagpiper, drummer, drummerrus, drummertur, gauduk, jannisary, lightinfantry, musketeer, musketeeraus, musketeernet, musketeerpol, musketeersco, musketeerspa, officer, officerrus, officersco, officertur, pikeman, pikemanpol, pikemanpor, pikemanrus, pikemansco, pikemanspa, pikemanswi, pikemantur, roundshier, serdiuk, strelet


### `<nat>ba2` — Barracks XVIII century.

- **Basic option** (17/21): **aus** Austria, **bav** Bavaria, **den** Denmark, **eng** England, **fra** France … (+12)
  - HP **55000**, buildtime **5625.0** g-sec, costpercent **200**
  - price: 1700 W · 2950 S · 4000 G
  - score=500, farm=250
  - produces: archersco, bagpiper, chasseur, drummer18, grenadier, grenadierbav, grenadierden, grenadierhun, grenadierpru, grenadiersax, highlander, jagerpor, jagerswi, musketeer18, musketeer18bav, musketeer18den, musketeer18pru, musketeer18sax, officer18, pandur, pandurhun, pikeman18, pikeman18swe, swordsmansco

- **Deviation 1** (1/21): **sco** Scotland
  - HP **40000**, buildtime **625.0** g-sec, costpercent **250**
  - price: 640 W · 2400 S · 2400 G
  - score=500, farm=150
  - produces: archersco, chasseur, drummer18, grenadier, grenadierbav, grenadierden, grenadierhun, grenadierpru, grenadiersax, highlander, jagerpor, jagerswi, musketeer18, musketeer18bav, musketeer18den, musketeer18pru, musketeer18sax, officer18, pandur, pandurhun, pikeman18, pikeman18swe, swordsmansco
<a id="sta--конюшня"></a>
### `<nat>sta` — Stable

- **Basic option** (14/21): **aus** Austria, **bav** Bavaria, **den** Denmark, **fra** France, **net** Netherlands … (+9)
  - HP **20000**, buildtime **625.0** g-sec, costpercent **200**
  - price: 2500 W · 100 S · 600 G
  - score=500
  - produces: cossackdon, cossackregister, cossacksich, croat, cuirassier, dragoon, dragoon18, dragoon18fra, dragoon18net, dragoon18pie, dragoonpol, guardcavalrysax, hackapell, hetman, hussar, hussarhun, hussarpru, hussarswi, kingmusketeer, lancersco, mameluke, raidersco, reiter, reiterpol, reiterswe, sipahi, spakh, tatar, vityaz, wingedhussar

- **Deviation 1** (2/21): **eng** England, **sco** Scotland
  - HP **25000**, buildtime **375.0** g-sec, costpercent **200**
  - price: 2350 W 800 G
  - score=500
  - produces: cossackdon, cossackregister, cossacksich, croat, cuirassier, dragoon, dragoon18, dragoon18fra, dragoon18net, dragoon18pie, dragoonpol, guardcavalrysax, hackapell, hetman, hussar, hussarhun, hussarpru, hussarswi, kingmusketeer, lancersco, mameluke, raidersco, reiter, reiterpol, reiterswe, sipahi, spakh, tatar, vityaz, wingedhussar

- **Deviation 2** (1/21): **rus** Russia
  - HP **25000**, buildtime **375.0** g-sec, costpercent **200**
  - price: 7950 W 550 G
  - score=500
  - produces: cossackdon, cossackregister, cossacksich, croat, cuirassier, dragoon, dragoon18, dragoon18fra, dragoon18net, dragoon18pie, dragoonpol, guardcavalrysax, hackapell, hetman, hussar, hussarhun, hussarpru, hussarswi, kingmusketeer, lancersco, mameluke, raidersco, reiter, reiterpol, reiterswe, sipahi, spakh, tatar, vityaz, wingedhussar

- **Deviation 3** (1/21): **ukr** Ukraine
  - HP **10000**, buildtime **156.25** g-sec, costpercent **300**
  - price: 3200 W 850 S 850 G
  - score=500
  - produces: cossackdon, cossackregister, cossacksich, croat, cuirassier, dragoon, dragoon18, dragoon18fra, dragoon18net, dragoon18pie, dragoonpol, guardcavalrysax, hackapell, hetman, hussar, hussarhun, hussarpru, hussarswi, kingmusketeer, lancersco, mameluke, raidersco, reiter, reiterpol, reiterswe, sipahi, spakh, tatar, vityaz, wingedhussar

- **Deviation 4** (1/21): **tur** Turkey
  - HP **55000**, buildtime **156.25** g-sec, costpercent **700**
  - price: 1000 W · 2600 S
  - score=500
  - produces: cossackdon, cossackregister, cossacksich, croat, cuirassier, dragoon, dragoon18, dragoon18fra, dragoon18net, dragoon18pie, dragoonpol, guardcavalrysax, hackapell, hetman, hussar, hussarhun, hussarpru, hussarswi, kingmusketeer, lancersco, mameluke, raidersco, reiter, reiterpol, reiterswe, sipahi, spakh, tatar, vityaz, wingedhussar

- **Deviation 5** (1/21): **alg** Algeria
  - HP **55000**, buildtime **156.25** g-sec, costpercent **700**
  - price: 1000 W · 2200 S
  - score=500
  - produces: cossackdon, cossackregister, cossacksich, croat, cuirassier, dragoon, dragoon18, dragoon18fra, dragoon18net, dragoon18pie, dragoonpol, guardcavalrysax, hackapell, hetman, hussar, hussarhun, hussarpru, hussarswi, kingmusketeer, lancersco, mameluke, raidersco, reiter, reiterpol, reiterswe, sipahi, spakh, tatar, vityaz, wingedhussar

- **Deviation 6** (1/21): **hun** Hungary
  - HP **20000**, buildtime **625.0** g-sec, costpercent **200**
  - price: 2500 W · 100 S · 600 G
  - score=500
- produces: cossackdon, cossackregister, cossacksich, croat, cuirassier, dragoon, dragoon18, dragoon18fra, dragoon18net, dragoon18pie, dragoonpol, guardcavalrysax, hackapell, hetman, hussar, hussarhun, hussarpru, hussarswi, kingmusketeer, lancersco, lightcavalry, mameluke, raidersco, reiter, reiterpol, reiterswe, sipahi, spakh, tatar, vityaz, wingedhussar


<a id="aca--академия"></a>
### `<nat>aca` — Academy

- **Basic option** (8/21): **bav** Bavaria, **fra** France, **hun** Hungary, **pie** Piedmont, **por** Portugal … (+3)
  - HP **63000**, buildtime **625.0** g-sec, costpercent **300**
  - price: 1250 W 1100 S
  - score=500
  - produces: —

- **Deviation 1** (2/21): **spa** Spain, **swe** Sweden
  - HP **63000**, buildtime **625.0** g-sec, costpercent **300**
  - price: 1350 W 1000 S
  - score=500
  - produces: —

- **Deviation 2** (2/21): **alg** Algeria, **tur** Turkey
  - HP **65000**, buildtime **156.25** g-sec, costpercent **300**
  - price: 1450 W 1100 S
  - score=500
  - produces: —

- **Deviation 3** (1/21): **aus** Austria
  - HP **65000**, buildtime **625.0** g-sec, costpercent **300**
  - price: 1250 W 1100 S
  - score=500
  - produces: —

- **Deviation 4** (1/21): **eng** England
  - HP **63000**, buildtime **625.0** g-sec, costpercent **300**
  - price: 1150 W · 1200 S
  - score=500
  - produces: —

- **Deviation 5** (1/21): **rus** Russia
  - HP **65000**, buildtime **843.75** g-sec, costpercent **300**
  - price: 1250 W 1300 S
  - score=500
  - produces: —

- **Deviation 6** (1/21): **ukr** Ukraine
  - HP **65000**, buildtime **46.88** g-sec, costpercent **300**
  - price: 1350 W 1200 S
  - score=500
  - produces: —

- **Deviation 7** (1/21): **pol** Poland
  - HP **63000**, buildtime **625.0** g-sec, costpercent **300**
  - price: 950 W 800 S
  - score=500
  - produces: —

- **Deviation 8** (1/21): **pru** Prussia
  - HP **63000**, buildtime **625.0** g-sec, costpercent **300**
  - price: 1200 W 1150 S
  - score=500
  - produces: —

- **Deviation 9** (1/21): **ven** Venice
  - HP **63000**, buildtime **625.0** g-sec, costpercent **300**
  - price: 1090 W 1260 S
  - score=500
  - produces: —

- **Deviation 10** (1/21): **net** Netherlands
  - HP **63000**, buildtime **625.0** g-sec, costpercent **300**
  - price: 1050 W 1230 S
  - score=500
  - produces: —

- **Deviation 11** (1/21): **den** Denmark
  - HP **63000**, buildtime **625.0** g-sec, costpercent **300**
  - price: 1450 W 900 S
  - score=500
  - produces: —


<a id="bla--кузница"></a>
### `<nat>bla` — Blacksmith

- **Basic option** (17/21): **aus** Austria, **bav** Bavaria, **den** Denmark, **eng** England, **hun** Hungary … (+12)
  - HP **5500**, buildtime **93.75** g-sec, costpercent **400**
  - price: 100 W 30 S 640 I
  - score=500
  - produces: —

- **Deviation 1** (2/21): **alg** Algeria, **tur** Turkey
  - HP **6500**, buildtime **109.38** g-sec, costpercent **400**
  - price: 100 W 30 S 640 I
  - score=500
  - produces: —

- **Deviation 2** (1/21): **fra** France
  - HP **5500**, buildtime **93.75** g-sec, costpercent **600**
  - price: 100 W 30 S 640 I
  - score=500
  - produces: —

- **Deviation 3** (1/21): **ukr** Ukraine
  - HP **4500**, buildtime **62.5** g-sec, costpercent **400**
  - price: 100 W 30 S 640 I
  - score=500
  - produces: —


<a id="art--артиллерийское-депо"></a>
### `<nat>art` — Artillery Depot

- **Basic option** (19/21): **alg** Algeria, **aus** Austria, **bav** Bavaria, **den** Denmark, **eng** England … (+14)
  - HP **40000**, buildtime **245.94** g-sec, costpercent **200**
  - price: 100 W · 1000 S · 1400 C
  - score=500
- produces: cannon, framegun, howitzer, mortar, multicannon

- **Deviation 1** (1/21): **ukr** Ukraine
  - HP **40000**, buildtime **245.94** g-sec, costpercent **200**
  - price: 4250 W · 4400 S · 100 G · 1400 C
  - score=500
  - produces: cannon, framegun, howitzer, mortar, multicannon

- **Deviation 2** (1/21): **tur** Turkey
  - HP **40000**, buildtime **245.94** g-sec, costpercent **200**
  - price: 500 W · 1200 S · 1400 C
  - score=500
  - produces: cannon, framegun, howitzer, mortar, multicannon


<a id="dip--дипломатический-центр"></a>
### `<nat>dip` — Diplomatic Center

- **Basic option** (17/21): **aus** Austria, **bav** Bavaria, **den** Denmark, **eng** England, **fra** France … (+12)
  - HP **4500**, buildtime **312.5** g-sec, costpercent **100**
  - price: 4900 W 1700 S
  - score=500
  - produces: archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip, lightcavalrydip, lightinfantrydip, roundshierdip

- **Deviation 1** (2/21): **alg** Algeria, **tur** Turkey
  - HP **5500**, buildtime **312.5** g-sec, costpercent **100**
  - price: 4600 W 2020 S
  - score=500
  - produces: archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip, lightcavalrydip, lightinfantrydip, roundshierdip

- **Deviation 2** (1/21): **rus** Russia
  - HP **6500**, buildtime **312.5** g-sec, costpercent **100**
  - price: 7900 W 3700 S
  - score=500
  - produces: archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip, lightcavalrydip, lightinfantrydip, roundshierdip

- **Deviation 3** (1/21): **ukr** Ukraine
  - HP **5000**, buildtime **312.5** g-sec, costpercent **100**
  - price: 3900 W 2700 S
  - score=500
  - produces: archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip, lightcavalrydip, lightinfantrydip, roundshierdip


<a id="tem--храм"></a>
### `<nat>tem` – Temple

- **Basic option** (16/21): **aus** Austria, **bav** Bavaria, **den** Denmark, **eng** England, **hun** Hungary … (+11)
  - HP **4200**, buildtime **156.25** g-sec, costpercent **300**
  - price: 1000 W · 1200 S · 500 I
  - score=500
  - produces: mullah, padre, pope, priest

- **Deviation 1** (2/21): **alg** Algeria, **tur** Turkey
  - HP **5000**, buildtime **93.75** g-sec, costpercent **300**
  - price: 1000 W · 1200 S · 500 I
  - score=500
  - produces: mullah, padre, pope, priest

- **Deviation 2** (1/21): **fra** France
  - HP **6000**, buildtime **312.5** g-sec, costpercent **300**
  - price: 1100 W · 2000 S · 600 I
  - score=500
  - produces: mullah, padre, pope, priest

- **Deviation 3** (1/21): **rus** Russia
  - HP **4500**, buildtime **156.25** g-sec, costpercent **300**
  - price: 1150 W · 1650 S · 100 G · 500 I
  - score=500
  - produces: mullah, padre, pope, priest

- **Deviation 4** (1/21): **ukr** Ukraine
  - HP **5300**, buildtime **156.25** g-sec, costpercent **300**
  - price: 1100 W · 1400 S · 300 I
  - score=500
  - produces: mullah, padre, pope, priest


<a id="2-юниты-общие-для-нескольких-наций"></a>
## §2. Units common to several nations

Each sid of a unit is taken that has a record in at least two nations (if one has a unique unit, it is described in [`reports/nations/overview.md`](overview.md) §3). Entries are grouped by stat fingerprint (HP / buildtime / price / shield / speed / defense / consume / weapon set). Units with the same fingerprint merge into one group.

If a sid has one group for all available nations, there are no deviations, and he is not shown here. If different, the base option (majority) and deviations are listed.

<a id="archerdip--лучник"></a>
### `archerdip` — Archer

- **Basic option** (20 nations): **alg** Algeria, **aus** Austria, **bav** Bavaria, **den** Denmark, **eng** England … (+15)
- HP **20**, price: 15 G, buildtime **1.25** g-sec, speed 32
  - score=1, costpercent=100.5
  - consume: 16 G/tick
  - weapon[0]: 25 dmg pause 2.5 s range 13.13 t arrow, disp 3.75t
  - weapon[1]: 100 dmg pause 0.78 s range 14.06 t firearrow, disp 3.75t

- **Deviation 1** (1 nation): **sco** Scotland
  - HP **20**, price: 15 G, buildtime **1.25** g-sec, speed 32
  - score=1, costpercent=100.5
  - consume: 39 F/tick · 16 G/tick
  - weapon[0]: 25 dmg pause 2.5 s range 13.13 t arrow, disp 3.75t
  - weapon[1]: 100 dmg pause 0.78 s range 14.06 t firearrow, disp 3.75t

<a id="archerturdip--лучник"></a>
### `archerturdip` — Archer

- **Basic option** (20 nations): **alg** Algeria, **aus** Austria, **bav** Bavaria, **den** Denmark, **eng** England … (+15)
  - HP **20**, price: 15 G, buildtime **1.25** g-sec, speed 32
  - score=1, costpercent=100.5
  - consume: 16 G/tick
  - weapon[0]: 25 dmg pause 2.5 s range 13.13 t arrow, disp 3.75t
  - weapon[1]: 100 dmg pause 0.78 s range 14.06 t firearrow, disp 3.75t

- **Deviation 1** (1 nation): **sco** Scotland
  - HP **20**, price: 15 G, buildtime **1.25** g-sec, speed 32
  - score=1, costpercent=100.5
  - consume: 39 F/tick · 16 G/tick
  - weapon[0]: 25 dmg pause 2.5 s range 13.13 t arrow, disp 3.75t
  - weapon[1]: 100 dmg pause 0.78 s range 14.06 t firearrow, disp 3.75t

<a id="drummer18--лёгкая-пехота"></a>
### `drummer18` - Light Infantry

- **Basic option** (15 nations): **aus** Austria, **bav** Bavaria, **den** Denmark, **fra** France, **hun** Hungary … (+10)
  - HP **100**, price: 50 F · 30 G, buildtime **6.0** g-sec, speed 32
  - score=10

- **Deviation 1** (1 nation): **rus** Russia
  - HP **100**, price: 90 F · 15 G, buildtime **6.0** g-sec, speed 32
  - score=10

<a id="pikeman--лёгкая-пехота"></a>
### `pikeman` - Light Infantry

- **Basic option** (12 nations): **aus** Austria, **bav** Bavaria, **den** Denmark, **eng** England, **fra** France … (+7)
  - HP **90**, price: 25 F · 3 G · 20 I, buildtime **4.5** g-sec, speed 32
  - score=10
  - prot: pike=3, sword=2, bullet=4, cannister=210, arrow=6, cannonball=40
  - weapon[0]: 8 dmg pause 0.0 s range 1.88 t pike

- **Deviation 1** (1 nation): **spa** Spain
  - HP **100**, price: 35 F · 7 G · 30 I, buildtime **5.5** g-sec, speed 32
  - score=10
  - prot: pike=3, sword=4, bullet=6, cannister=240, arrow=12, cannonball=50
  - weapon[0]: 10 dmg pause 0.0 s range 1.88 t pike

<a id="roundshierdip--лёгкая-пехота"></a>
### `roundshierdip` - Light Infantry

- **Basic option** (20 nations): **alg** Algeria, **aus** Austria, **bav** Bavaria, **den** Denmark, **eng** England … (+15)
  - HP **75**, price: 12 G, buildtime **1.5** g-sec, speed 32
  - score=1
  - prot: pike=5, sword=3, bullet=8, cannister=225, arrow=17, cannonball=80
  - consume: 20 G/tick
  - weapon[0]: 6 dmg pause 0.0 s range 1.13 t sword

- **Deviation 1** (1 nation): **sco** Scotland
  - HP **75**, price: 12 G, buildtime **1.5** g-sec, speed 32
  - score=1
  - prot: pike=5, sword=3, bullet=8, cannister=225, arrow=17, cannonball=80
  - consume: 45 F/tick · 20 G/tick
  - weapon[0]: 6 dmg pause 0.0 s range 1.13 t sword


Total units with interethnic deviations: **5**.
