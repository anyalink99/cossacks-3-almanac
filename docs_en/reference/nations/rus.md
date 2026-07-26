<a id="россия"></a>
# Russia (`rus`)



[← All nations](README.md) · [← Quick reference](../README.md)

<a id="кластер"></a>
<a id="общие-особенности"></a>
## Shared features

- **Base peasant:** **Serf** (`pearus`).
- The Mill, Storehouse, Market, and Tower use one of the game's shared architectural sets (internal group `rus`).

<a id="уникальные-юниты-7"></a>
## Unique units (7)

| Unit | Role | Health | Damage | Reload, game s | Range, tiles |
|---|---|---:|---:|---:|---:|
| **Don Cossack** `cossackdon` | Heavy Cavalry | 220 | 13 | 0.0 | 1.88 |
| **Drummer, 17th century** `drummerrus` | Light Infantry | 100 | — | — | — |
| **Commander** `officerrus` | Light Infantry | 125 | 40 | 0.0 | 1.22 |
| **Serf** `pearus` | Peasant | 50 | 20 | 0.0 | 1.22 |
| **Spearman** `pikemanrus` | Light Infantry | 85 | 8 | 0.0 | 1.69 |
| **Strelets** `strelet` | Shooter | 85 | 12 | 4.69 | 13.13 |
| **Vityaz** `vityaz` | Heavy Cavalry | 380 | 14 | 0.0 | 1.22 |

<a id="здания"></a>
## Buildings

<a id="уникальные-для-нации-10"></a>
### Unique to the nation (10)

> **Bold** marks values that differ from the most common version of the same building.

| Building | Health | Build time, game s | Price growth, % | Food | Wood | Stone | Gold | Iron | Coal | Population | Produces |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Academy** `rusaca` | **65000** | **843.75** | 300 | 0 | 1250 | **1300** | 0 | 0 | 0 | 0 | — |
| **Artillery Depot** `rusart` | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | Cannon, Frame gun, Howitzer, Bombard, Multi-barrelled Cannon |
| **Barracks, 18th century** `rusba2` | 55000 | 5625.0 | 200 | 0 | 1700 | 2950 | 4000 | 0 | 0 | 250 | Bow Clansman, Bagpiper, Chasseur, Drummer, 18th century, Grenadier (+19) |
| **Strelets Barracks** `rusbar` | **25000** | **78.12** | **300** | 0 | **200** | **20** | **0** | 0 | 0 | **25** | Archer, Turkish archer, Drummer, 17th century, Drummer, 17th century, Drummer, 17th century (+24) |
| **Blacksmith** `rusbla` | 5500 | 93.75 | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| **Town Hall** `ruscen` | **4050** | 156.25 | 300 | 0 | **680** | 700 | 0 | 0 | 0 | **75** | Peasant, Peasant, Peasant, Serf, Peasant (+3) |
| **Diplomatic Center** `rusdip` | **6500** | 312.5 | 100 | 0 | **7900** | **3700** | 0 | 0 | 0 | 0 | Archer (mercenary), Turkish archer (mercenary), Sich Cossack (mercenary), Dragoon, 18th century (mercenary), Grenadier (mercenary) (+3) |
| **Izba** `rushou` | **5000** | 31.25 | 104 | 0 | **120** | **0** | 0 | 0 | 0 | 25 | — |
| **Stable** `russta` | **25000** | **375.0** | 200 | 0 | **7950** | **0** | **550** | 0 | 0 | 0 | Don Cossack, Register Cossack, Sich Cossack, Croat, Cuirassier (+25) |
| **Orthodox Cathedral** `rustem` | **4500** | 156.25 | 300 | 0 | **1150** | **1650** | **100** | 500 | 0 | 0 | Mullah, Padre, Pope, Priest |

<a id="общий-кластер-12"></a>
<a id="общие-здания-архитектурной-группы-12"></a>
### Shared buildings (12)

| Building | HP | Time (g-sec) | cost% | F | W | S | G | I | C | Add. |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Mine** `eurcoa` | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | produces {"coal": 13}; +5 workers |
| **Mine** `eurgol` | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | produces {"gold": 13}; +5 workers |
| **Mine** `euriro` | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | produces {"iron": 13}; +5 workers |
| **Market** `rusmar` | 4000 | 234.38 | 2000 | 0 | 450 | 0 | 0 | 0 | 0 | — |
| **Mill** `rusmil` | 15000 | 93.75 | 200 | 0 | 210 | 0 | 0 | 0 | 0 | — |
| **Shipyard** `ruspor` | 45000 | 1562.5 | 150 | 0 | 1200 | 800 | 0 | 400 | 0 | — |
| **Gate** `russga` | 32000 | 200.0 | 0 | 0 | 0 | 60 | 0 | 0 | 0 | content {"stone": 200} |
| **Storehouse** `russto` | 10000 | 31.25 | 200 | 0 | 50 | 20 | 0 | 0 | 0 | — |
| **Wall** `russwa` | 50000 | 200.0 | 0 | 0 | 0 | 60 | 0 | 0 | 0 | content {"stone": 200} |
| **Tower** `rustow` | 21000 | 1476.56 | 125 | 0 | 100 | 100 | 150 | 0 | 0 | damage 1000; content {"gold": 500} |
| **Gate** `ukrwga` | 1500 | 5.62 | 0 | 0 | 10 | 0 | 0 | 0 | 0 | content {"wood": 32} |
| **Palisade** `ukrwwa` | 1500 | 5.62 | 0 | 0 | 10 | 0 | 0 | 0 | 0 | content {"wood": 32} |

<a id="юниты-по-классам"></a>
## Units by class

<a id="крестьяне"></a>
### Peasants

| Unit | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Serf** `pearus` | 50 | 12.5 | 100 | 0 | 0 | 20 | 1.22 | 0.0 | unique |

<a id="пикинёры-17-в"></a>
### Pikemen (17th century)

| Unit | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Spearman** `pikemanrus` | 85 | 5.5 | 45 | 4 | 15 | 8 | 1.69 | 0.0 | unique |

<a id="пикинёры-18-в"></a>
### Pikemen (18th century)

| Unit | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Pikeman, 18th century** `pikeman18` | 85 | 1.25 | 30 | 2 | 0 | 9 | 1.88 | 0.0 | shared(16n) |

<a id="лёгкая-пехота"></a>
### Light Infantry

| Unit | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Light Infantryman (mercenary)** `lightinfantrydip` | 50 | 1.25 | 0 | 4 | 0 | 16 | 0.94 | 0.0 | common |
| **Roundshier (mercenary)** `roundshierdip` | 75 | 1.5 | 0 | 12 | 0 | 6 | 1.13 | 0.0 | common |

<a id="мушкетёры-17-в"></a>
### Musketeers (17th century)

| Unit | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Strelets** `strelet` | 85 | 8.5 | 70 | 7 | 9 | 12 | 13.13 | 4.69 | unique |

<a id="мушкетёры-18-в"></a>
### Musketeers (18th century)

| Unit | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Musketeer, 18th century** `musketeer18` | 100 | 4.5 | 50 | 40 | 40 | 16 | 16.88 | 4.69 | shared(13n) |

<a id="гренадёры"></a>
### Grenadiers

| Unit | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Grenadier** `grenadier` | 120 | 6.0 | 80 | 60 | 40 | 16 | 16.88 | 5.31 | shared(13n) |
| **Grenadier (mercenary)** `grenadierdip` | 30 | 1.5 | 0 | 25 | 0 | 16 | 15.0 | 4.69 | common |

<a id="лучники"></a>
### Archers

| Unit | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Archer (mercenary)** `archerdip` | 20 | 1.25 | 0 | 15 | 0 | 100 | 14.06 | 0.78 | common |
| **Turkish archer (mercenary)** `archerturdip` | 20 | 1.25 | 0 | 15 | 0 | 100 | 14.06 | 0.78 | common |

<a id="лёгкая-кавалерия"></a>
### Light Cavalry

| Unit | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Hussar** `hussar` | 230 | 15.0 | 70 | 20 | 2 | 12 | 1.22 | 0.0 | shared(14n) |
| **Light cavalry (mercenary)** `lightcavalrydip` | 100 | 2.0 | 0 | 120 | 0 | 18 | 15.0 | 2.25 | common |

<a id="драгуны"></a>
### Dragoons

| Unit | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Dragoon, 18th century** `dragoon18` | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | shared(13n) |
| **Dragoon, 18th century (mercenary)** `dragoon18dip` | 100 | 2.0 | 0 | 120 | 0 | 18 | 15.0 | 2.25 | common |

<a id="тяжёлая-кавалерия"></a>
### Heavy Cavalry

| Unit | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Don Cossack** `cossackdon` | 220 | 13.5 | 100 | 0 | 0 | 13 | 1.88 | 0.0 | unique |
| **Sich Cossack (mercenary)** `cossacksichdip` | 150 | 2.5 | 0 | 60 | 0 | 8 | 1.22 | 0.0 | common |
| **Cuirassier** `cuirassier` | 300 | 22.5 | 120 | 35 | 25 | 14 | 1.22 | 0.0 | shared(17n) |
| **Vityaz** `vityaz` | 380 | 25.5 | 160 | 13 | 25 | 14 | 1.22 | 0.0 | unique |

<a id="пушки"></a>
### Cannons

| Unit | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Cannon** `cannon` | 9000 | 75.0 | 0 | 400 | 400 | 1800 | 40.5 | 10.94 | common |
| **Multi-barrelled Cannon** `multicannon` | 2000 | 50.0 | 0 | 400 | 250 | 500 | 13.13 | 1.88 | shared(17n) |

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
| **Galley** `galley` | 35000 | 50.0 | 0 | 900 | 800 | 1000 | 58.13 | 1.56 | common |
| **Yacht** `yacht` | 31000 | 48.0 | 0 | 450 | 150 | 1000 | 20.63 | 10.94 | common |

<a id="офицеры"></a>
### Officers

| Unit | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Officer, 18th century** `officer18` | 125 | 6.0 | 50 | 200 | 10 | 50 | 1.22 | 0.0 | shared(17n) |
| **Commander** `officerrus` | 125 | 12.5 | 100 | 125 | 5 | 40 | 1.22 | 0.0 | unique |

<a id="барабанщики-и-волынщики"></a>
### Drummers and pipers

| Unit | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Drummer, 18th century** `drummer18` | 100 | 6.0 | 90 | 15 | 0 | — | — | — | shared(16n) |
| **Drummer, 17th century** `drummerrus` | 100 | 6.0 | 90 | 15 | 0 | — | — | — | unique |

<a id="священники"></a>
### Priests
| Unit | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Pope** `pope` | 75 | 20.0 | 40 | 20 | 0 | 25 | 6.56 | 0.0 | semi-unique (2n) |

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

<a id="апгрейды-219"></a>
<a id="улучшения-219"></a>
## Upgrades (219)

The full list is in the [chapter “Upgrades”](../05_upgrades/README.md).

By buildings:

- **aca** (aca): 36
- **mil** (mil): 2
- **bla** (bla): 6
- **sta** (sta): 60
- **bar** (bar): 24
- **ba2** (ba2): 39
- **art** (art): 24
- **cen** (cen): 1
- **mines** (Mine): 18
