<a id="шотландия"></a>
# Scotland (`sco`)



[← All nations](README.md) · [← Quick reference](../README.md)

<a id="кластер"></a>
<a id="общие-особенности"></a>
## Shared features

- **Base peasant:** **Peasant** (`peasco`).
- The Mill, Storehouse, Market, and Tower use one of the game's shared architectural sets (internal group `eur`).

<a id="уникальные-юниты-9"></a>
## Unique units (9)

| Unit | Role | Health | Damage | Reload, game s | Range, tiles |
|---|---|---:|---:|---:|---:|
| **Bow Clansman** `archersco` | Archer | 150 | 150 | 4.38 | 18.75 |
| **Frame gun** `framegun` | Cannon | 3000 | 500 | 2.81 | 33.75 |
| **Lancer** `lancersco` | Heavy Cavalry | 320 | 11 | 0.0 | 1.88 |
| **Covenanter musketeer** `musketeersco` | Shooter | 90 | 12 | 4.69 | 15.94 |
| **Officer** `officersco` | Light Infantry | 150 | 40 | 0.0 | 1.22 |
| **Peasant** `peasco` | Peasant | 60 | 20 | 0.0 | 1.22 |
| **Covenanter pikeman** `pikemansco` | Light Infantry | 100 | 9 | 0.0 | 1.88 |
| **Raider** `raidersco` | Light Cavalry | 280 | 11 | 0.0 | 1.22 |
| **Sword Clansman** `swordsmansco` | Light Infantry | 180 | 10 | 0.0 | 1.13 |

<a id="здания"></a>
## Buildings

<a id="уникальные-для-нации-10"></a>
### Unique to the nation (10)

> **Bold** marks values that differ from the most common version of the same building.

| Building | Health | Build time, game s | Price growth, % | Food | Wood | Stone | Gold | Iron | Coal | Population | Produces |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Academy** `scoaca` | 63000 | 625.0 | 300 | 0 | 1250 | 1100 | 0 | 0 | 0 | 0 | — |
| **Artillery Depot** `scoart` | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | Cannon, Frame gun, Howitzer, Bombard, Multi-barrelled Cannon |
| **Castle** `scoba2` | **40000** | **625.0** | **250** | 0 | **640** | **2400** | **2400** | 0 | 0 | **150** | Bow Clansman, Chasseur, Drummer, 18th century, Grenadier, Grenadier (+18) |
| **Barracks, 17th century** `scobar` | **30000** | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | Archer, Turkish archer, Bagpiper, Drummer, 17th century, Drummer, 17th century (+25) |
| **Blacksmith** `scobla` | 5500 | 93.75 | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| **Town Hall** `scocen` | 4000 | 156.25 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | Peasant, Peasant, Peasant, Serf, Peasant (+3) |
| **Diplomatic Center** `scodip` | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | Archer (mercenary), Turkish archer (mercenary), Sich Cossack (mercenary), Dragoon, 18th century (mercenary), Grenadier (mercenary) (+3) |
| **Housing** `scohou` | 4000 | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| **Stable** `scosta` | **25000** | **375.0** | 200 | 0 | **2350** | **0** | **800** | 0 | 0 | 0 | Don Cossack, Register Cossack, Sich Cossack, Croat, Cuirassier (+25) |
| **Cathedral** `scotem` | 4200 | 156.25 | 300 | 0 | 1000 | 1200 | 0 | 500 | 0 | 0 | Mullah, Padre, Pope, Priest |

<a id="общий-кластер-12"></a>
<a id="общие-здания-архитектурной-группы-12"></a>
### Shared buildings (12)

| Building | HP | Time (g-sec) | cost% | F | W | S | G | I | C | Add. |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Mine** `eurcoa` | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | produces {"coal": 13}; +5 workers |
| **Mine** `eurgol` | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | produces {"gold": 13}; +5 workers |
| **Mine** `euriro` | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | produces {"iron": 13}; +5 workers |
| **Market** `eurmar` | 4000 | 234.38 | 2000 | 0 | 450 | 0 | 0 | 0 | 0 | — |
| **Mill** `eurmil` | 20000 | 93.75 | 200 | 0 | 30 | 150 | 0 | 0 | 0 | — |
| **Shipyard** `eurpor` | 50000 | 1562.5 | 150 | 0 | 1600 | 800 | 0 | 400 | 0 | — |
| **Gate** `eursga` | 32000 | 90.0 | 0 | 0 | 0 | 50 | 0 | 0 | 0 | content {"stone": 250} |
| **Storehouse** `eursto` | 10000 | 31.25 | 150 | 0 | 50 | 20 | 0 | 0 | 0 | — |
| **Wall** `eurswa` | 50000 | 90.0 | 0 | 0 | 0 | 50 | 0 | 0 | 0 | content {"stone": 250} |
| **Tower** `eurtow` | 20000 | 1230.31 | 120 | 0 | 100 | 100 | 150 | 0 | 0 | damage 1000; content {"gold": 500} |
| **Gate** `ukrwga` | 1500 | 5.62 | 0 | 0 | 10 | 0 | 0 | 0 | 0 | content {"wood": 32} |
| **Palisade** `ukrwwa` | 1500 | 5.62 | 0 | 0 | 10 | 0 | 0 | 0 | 0 | content {"wood": 32} |

<a id="юниты-по-классам"></a>
## Units by class

<a id="крестьяне"></a>
### Peasants

| Unit | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Peasant** `peasco` | 60 | 12.5 | 100 | 0 | 0 | 20 | 1.22 | 0.0 | unique |

<a id="пикинёры-17-в"></a>
### Pikemen (17th century)

| Unit | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Covenanter pikeman** `pikemansco` | 100 | 4.0 | 35 | 2 | 0 | 9 | 1.88 | 0.0 | unique |

<a id="лёгкая-пехота"></a>
### Light Infantry

| Unit | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Light Infantryman (mercenary)** `lightinfantrydip` | 50 | 1.25 | 0 | 4 | 0 | 16 | 0.94 | 0.0 | common |
| **Roundshier (mercenary)** `roundshierdip` | 75 | 1.5 | 0 | 12 | 0 | 6 | 1.13 | 0.0 | common |
| **Sword Clansman** `swordsmansco` | 180 | 7.0 | 110 | 10 | 0 | 10 | 1.13 | 0.0 | unique |

<a id="мушкетёры-17-в"></a>
### Musketeers (17th century)

| Unit | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Covenanter musketeer** `musketeersco` | 90 | 7.0 | 55 | 8 | 7 | 12 | 15.94 | 4.69 | unique |

<a id="гренадёры"></a>
### Grenadiers

| Unit | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Grenadier (mercenary)** `grenadierdip` | 30 | 1.5 | 0 | 25 | 0 | 16 | 15.0 | 4.69 | common |

<a id="лучники"></a>
### Archers

| Unit | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Archer (mercenary)** `archerdip` | 20 | 1.25 | 0 | 15 | 0 | 100 | 14.06 | 0.78 | common |
| **Bow Clansman** `archersco` | 150 | 6.0 | 80 | 7 | 0 | 150 | 18.75 | 4.38 | unique |
| **Turkish archer (mercenary)** `archerturdip` | 20 | 1.25 | 0 | 15 | 0 | 100 | 14.06 | 0.78 | common |

<a id="лёгкая-кавалерия"></a>
### Light Cavalry

| Unit | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Lancer** `lancersco` | 320 | 21.0 | 120 | 6 | 0 | 11 | 1.88 | 0.0 | unique |
| **Light cavalry (mercenary)** `lightcavalrydip` | 100 | 2.0 | 0 | 120 | 0 | 18 | 15.0 | 2.25 | common |
| **Raider** `raidersco` | 280 | 22.5 | 130 | 8 | 2 | 11 | 1.22 | 0.0 | unique |

<a id="драгуны"></a>
### Dragoons

| Unit | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Dragoon, 18th century (mercenary)** `dragoon18dip` | 100 | 2.0 | 0 | 120 | 0 | 18 | 15.0 | 2.25 | common |

<a id="тяжёлая-кавалерия"></a>
### Heavy Cavalry

| Unit | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Sich Cossack (mercenary)** `cossacksichdip` | 150 | 2.5 | 0 | 60 | 0 | 8 | 1.22 | 0.0 | common |

<a id="пушки"></a>
### Cannons

| Unit | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Cannon** `cannon` | 9000 | 75.0 | 0 | 400 | 400 | 1800 | 40.5 | 10.94 | common |
| **Frame gun** `framegun` | 3000 | 50.0 | 0 | 300 | 150 | 500 | 33.75 | 2.81 | unique |

<a id="мортиры"></a>
### Mortars

| Unit | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Howitzer** `howitzer` | 3000 | 94.0 | 0 | 350 | 300 | 4000 | 26.25 | 18.75 | common |
| **Bombard** `mortar` | 400 | 25.0 | 0 | 75 | 200 | 200 | 48.75 | 7.81 | common |

<a id="рыбацкие-лодки"></a>
### Fishing boats

| Unit | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Boat** `fishboat` | 300 | 40.0 | 0 | 0 | 0 | — | — | — | common |

<a id="военные-корабли"></a>
### Warships

| Unit | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Ship of the Line** `battleship` | 90000 | 390.0 | 0 | 3200 | 700 | 1800 | 36.56 | 0.62 | common |
| **Ferry** `ferry` | 62000 | 56.0 | 0 | 50 | 100 | — | — | — | common |
| **Frigate** `frigate` | 50000 | 230.0 | 0 | 1100 | 600 | 1800 | 30.94 | 2.34 | common |
| **Yacht** `yacht` | 31000 | 48.0 | 0 | 450 | 150 | 1000 | 20.63 | 10.94 | common |

<a id="офицеры"></a>
### Officers

| Unit | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Officer** `officersco` | 150 | 10.0 | 130 | 130 | 10 | 40 | 1.22 | 0.0 | unique |

<a id="барабанщики-и-волынщики"></a>
### Drummers and pipers

| Unit | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Bagpiper** `bagpiper` | 150 | 7.0 | 120 | 20 | 0 | — | — | — | semi-unique (2n) |

<a id="священники"></a>
### Priests

| Unit | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Priest** `priest` | 100 | 20.0 | 60 | 25 | 0 | 20 | 7.5 | 0.0 | shared(16n) |

<a id="разное-и-миссии"></a>
### Miscellaneous and missions

| Unit | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `unitbox` | 100 | 3.12 | 100 | 0 | 0 | — | — | — | common |

<a id="офицеры-11-групп"></a>
## Officers (11 groups)

Each officer leads the formation of his units. Standard formations: **LINE / SQUARE / KARE × 15/36/72/120/196/400**.

| officer | drummer | units |
|---|---|---|
| `roundshierdip` | `roundshierdip` | roundshierdip |
| `grenadierdip` | `grenadierdip` | grenadierdip |
| `officer` | `drummer` | pikemanpol, roundshier, musketeer, musketeeraus, musketeerpol, musketeerspa, grenadierdip, roundshierdip (+5) |
| `officerrus` | `drummerrus` | pikemanrus, strelet, grenadierdip, roundshierdip |
| `officertur` | `drummertur` | pikemantur, lightinfantry, archer, archertur, jannisary, grenadierdip, roundshierdip |
| `officer18` | `drummer18` | pikeman18, pikeman18swe, pandur, chasseur, highlander, musketeer18, musketeer18pru, grenadier (+11) |
| `officer18` | `bagpiper` | pikeman18, pikeman18swe, pandur, chasseur, highlander, musketeer18, musketeer18pru, grenadier (+7) |
| `officersco` | `bagpiper` | pikemansco, musketeersco, grenadierdip, roundshierdip |
| `serdiuk` | `serdiuk` | serdiuk |
| `archersco` | `archersco` | archersco |
| `swordsmansco` | `swordsmansco` | swordsmansco |

<a id="апгрейды-168"></a>
<a id="улучшения-168"></a>
## Upgrades (168)

The full list is in the [chapter “Upgrades”](../05_upgrades/README.md).

By buildings:

- **aca** (aca): 36
- **bla** (bla): 6
- **sta** (sta): 24
- **bar** (bar): 24
- **ba2** (ba2): 24
- **art** (art): 24
- **cen** (cen): 1
- **mines** (Mine): 18
