<a id="национальные-отклонения--здания-и-юниты"></a>
# National Variants of Buildings and Units

[← Technical documentation](../README.md)

This calculated report is built from [`data.json`](../../data.json) by
[`compute/compute_nation_deviations.py`](../../compute/compute_nation_deviations.py).

This report collects every building or shared-unit statistic that differs
from the most common value across nations. The differences originate in
`case i of nation:` branches in `unit.script`, which override
`SetObjBuildingProperties` or `SetObjBaseWeapon` for individual nations.

For each family—for example, `<nat>cen` for the Town Hall—the 21 nations
are grouped by a fingerprint of significant statistics. The largest group
defines the baseline; smaller groups are listed as variants with their
differences shown explicitly.

This report complements the reader-facing
[nation comparison](../../docs_en/reports/nations/overview.md), which summarizes
roster size, building coverage, market groups, and the largest stat differences.
The full stat fingerprints are listed here.

Contents:

- [§1. Shared building families (Town Hall, Barracks, Academy, etc.)](#1-здания-общего-класса)
- [§2. Units common to several nations](#2-юниты-общие-для-нескольких-наций)

<a id="1-здания-общего-класса"></a>
## §1. Shared Building Families

For each `<nat>`-plus-suffix building family, the report collects every
nation that has the building and groups identical fingerprints together.
The values come from `SetObjBuildingProperties` and
`SetObjBuildingExtProperties`. A nation without that building does not
appear in the group; for example, Ukraine has no towers or stone walls.
See the [nation comparison](../../docs_en/reports/nations/overview.md).

Fingerprint fields: HP · buildtime · costpercent · price · score · vision ·
farm · peasantabsorber · consume · weapon (damage/pause/radiusmax) · production
roster.

<a id="natcen--городской-центр"></a>
### `<nat>cen` — Town Hall

- **Baseline** (7/21): **bav** Bavaria, **hun** Hungary, **pie** Piedmont, **por** Portugal, **sax** Saxony … (+2)
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


<a id="nathou--дом--ферма"></a>
### `<nat>hou` — House

- **Baseline** (10/21): **aus** Austria, **bav** Bavaria, **den** Denmark, **fra** France, **hun** Hungary … (+5)
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


<a id="natbar--казарма-xvii-в"></a>
### `<nat>bar` — Barracks, 17th century

- **Baseline** (16/21): **aus** Austria, **bav** Bavaria, **den** Denmark, **eng** England, **fra** France … (+11)
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


<a id="natba2--казарма-xviii-в"></a>
### `<nat>ba2` — Barracks, 18th century

- **Baseline** (17/21): **aus** Austria, **bav** Bavaria, **den** Denmark, **eng** England, **fra** France … (+12)
  - HP **55000**, buildtime **5625.0** g-sec, costpercent **200**
  - price: 1700 W · 2950 S · 4000 G
  - score=500, farm=250
  - produces: archersco, bagpiper, chasseur, drummer18, grenadier, grenadierbav, grenadierden, grenadierhun, grenadierpru, grenadiersax, highlander, jagerpor, jagerswi, musketeer18, musketeer18bav, musketeer18den, musketeer18pru, musketeer18sax, officer18, pandur, pandurhun, pikeman18, pikeman18swe, swordsmansco

- **Deviation 1** (1/21): **sco** Scotland
  - HP **40000**, buildtime **625.0** g-sec, costpercent **250**
  - price: 640 W · 2400 S · 2400 G
  - score=500, farm=150
  - produces: archersco, chasseur, drummer18, grenadier, grenadierbav, grenadierden, grenadierhun, grenadierpru, grenadiersax, highlander, jagerpor, jagerswi, musketeer18, musketeer18bav, musketeer18den, musketeer18pru, musketeer18sax, officer18, pandur, pandurhun, pikeman18, pikeman18swe, swordsmansco
<a id="natsta--конюшня"></a>
### `<nat>sta` — Stable

- **Baseline** (14/21): **aus** Austria, **bav** Bavaria, **den** Denmark, **fra** France, **net** Netherlands … (+9)
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


<a id="nataca--академия"></a>
### `<nat>aca` — Academy

- **Baseline** (8/21): **bav** Bavaria, **fra** France, **hun** Hungary, **pie** Piedmont, **por** Portugal … (+3)
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


<a id="natbla--кузница"></a>
### `<nat>bla` — Blacksmith

- **Baseline** (17/21): **aus** Austria, **bav** Bavaria, **den** Denmark, **eng** England, **hun** Hungary … (+12)
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


<a id="natart--артиллерийское-депо"></a>
### `<nat>art` — Artillery Depot

- **Baseline** (19/21): **alg** Algeria, **aus** Austria, **bav** Bavaria, **den** Denmark, **eng** England … (+14)
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


<a id="natdip--дипломатический-центр"></a>
### `<nat>dip` — Diplomatic Center

- **Baseline** (17/21): **aus** Austria, **bav** Bavaria, **den** Denmark, **eng** England, **fra** France … (+12)
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


<a id="nattem--храм"></a>
### `<nat>tem` – Temple

- **Baseline** (16/21): **aus** Austria, **bav** Bavaria, **den** Denmark, **eng** England, **hun** Hungary … (+11)
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

Each unit `sid` with records in at least two nations is included; units unique to one nation are covered by the [nation comparison](../../docs_en/reports/nations/overview.md). Entries are grouped by stat fingerprint (HP / build time / price / armor / speed / defense / upkeep / weapon set). Units with the same fingerprint are merged into one group.

If a SID has the same fingerprint in every available nation, it has no
variant and is omitted. Otherwise, the majority fingerprint and all
deviations are listed.

<a id="archerdip--лучник"></a>
### `archerdip` — Archer (mercenary)

- **Baseline** (20 nations): **alg** Algeria, **aus** Austria, **bav** Bavaria, **den** Denmark, **eng** England … (+15)
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
### `archerturdip` — Turkish archer (mercenary)

- **Baseline** (20 nations): **alg** Algeria, **aus** Austria, **bav** Bavaria, **den** Denmark, **eng** England … (+15)
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
### `drummer18` — Drummer, 18th century

- **Baseline** (15 nations): **aus** Austria, **bav** Bavaria, **den** Denmark, **fra** France, **hun** Hungary … (+10)
  - HP **100**, price: 50 F · 30 G, buildtime **6.0** g-sec, speed 32
  - score=10

- **Deviation 1** (1 nation): **rus** Russia
  - HP **100**, price: 90 F · 15 G, buildtime **6.0** g-sec, speed 32
  - score=10

<a id="pikeman--лёгкая-пехота"></a>
### `pikeman` — Pikeman, 17th century

- **Baseline** (12 nations): **aus** Austria, **bav** Bavaria, **den** Denmark, **eng** England, **fra** France … (+7)
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
### `roundshierdip` — Roundshier (mercenary)

- **Baseline** (20 nations): **alg** Algeria, **aus** Austria, **bav** Bavaria, **den** Denmark, **eng** England … (+15)
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


Total shared units with national deviations: **5**.
