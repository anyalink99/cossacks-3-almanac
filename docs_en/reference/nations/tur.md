<a id="турция"></a>
# Turkey (`tur`)



[← All nations](README.md) · [← Quick reference](../README.md)

<a id="кластер"></a>
<a id="общие-особенности"></a>
## Shared features

- **Base peasant:** **Peasant** (`peatur`).
- The Mill, Storehouse, Market, and Tower use one of the game's shared architectural sets (internal group `tur`).

<a id="уникальные-юниты-6"></a>
## Unique units (6)

| Unit | Role | Health | Damage | Reload, game s | Range, tiles |
|---|---|---:|---:|---:|---:|
| **Turkish archer** `archertur` | Archer | 65 | 150 | 4.38 | 16.88 |
| **Janissary** `jannisary` | Shooter | 65 | 12 | 4.69 | 15.94 |
| **Heavy Sipahi** `sipahi` | Heavy Cavalry | 360 | 15 | 0.0 | 1.22 |
| **Light Sipahi** `spakh` | Heavy Cavalry | 230 | 15 | 0.0 | 1.88 |
| **Tatar** `tatar` | Archer | 185 | 140 | 4.69 | 20.63 |
| **Yacht** `yachttur` | Yacht | 35000 | 0 | 21.88 | 30.94 |

<a id="здания"></a>
## Buildings

<a id="уникальные-для-нации-9"></a>
### Unique to the nation (9)

> **Bold** marks values that differ from the most common version of the same building.

| Building | Health | Build time, game s | Price growth, % | Food | Wood | Stone | Gold | Iron | Coal | Population | Produces |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Minaret** `turaca` | **65000** | **156.25** | 300 | 0 | **1450** | 1100 | 0 | 0 | 0 | 0 | — |
| **Artillery Depot** `turart` | 40000 | 245.94 | 200 | 0 | **500** | **1200** | 0 | 0 | 1400 | 0 | Cannon, Frame gun, Howitzer, Bombard, Multi-barrelled Cannon |
| **Barracks** `turbar` | **35000** | 93.75 | 500 | 0 | **400** | **400** | **0** | 0 | 0 | **50** | Archer, Turkish archer, Drummer, 17th century, Drummer, 17th century, Drummer, 17th century (+24) |
| **Blacksmith** `turbla` | **6500** | **109.38** | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| **Town Hall** `turcen` | 4000 | 156.25 | 300 | 0 | **600** | **500** | 0 | 0 | 0 | 100 | Peasant, Peasant, Peasant, Serf, Peasant (+3) |
| **Diplomatic Center** `turdip` | **5500** | 312.5 | 100 | 0 | **4600** | **2020** | 0 | 0 | 0 | 0 | Archer (mercenary), Turkish archer (mercenary), Sich Cossack (mercenary), Dragoon, 18th century (mercenary), Grenadier (mercenary) (+3) |
| **Housing** `turhou` | 4000 | 31.25 | **106** | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| **Stable** `tursta` | **55000** | **156.25** | **700** | 0 | **1000** | **2600** | **0** | 0 | 0 | 0 | Don Cossack, Register Cossack, Sich Cossack, Croat, Cuirassier (+25) |
| **Mosque** `turtem` | **5000** | **93.75** | 300 | 0 | 1000 | 1200 | 0 | 500 | 0 | 0 | Mullah, Padre, Pope, Priest |

<a id="общий-кластер-12"></a>
<a id="общие-здания-архитектурной-группы-12"></a>
### Shared buildings (12)

| Building | HP | Time (g-sec) | cost% | F | W | S | G | I | C | Add. |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Mine** `eurcoa` | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | produces {"coal": 13}; +5 workers |
| **Mine** `eurgol` | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | produces {"gold": 13}; +5 workers |
| **Mine** `euriro` | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | produces {"iron": 13}; +5 workers |
| **Bazaar** `turmar` | 4500 | 234.38 | 1500 | 0 | 450 | 150 | 0 | 0 | 0 | — |
| **Mill** `turmil` | 20000 | 93.75 | 200 | 0 | 30 | 150 | 0 | 0 | 0 | — |
| **Shipyard** `turpor` | 40000 | 1562.5 | 150 | 0 | 800 | 800 | 0 | 400 | 0 | — |
| **Gate** `tursga` | 32000 | 120.0 | 0 | 0 | 0 | 60 | 0 | 0 | 0 | content {"stone": 150} |
| **Storehouse** `tursto` | 10000 | 31.25 | 200 | 0 | 30 | 10 | 0 | 0 | 0 | — |
| **Wall** `turswa` | 50000 | 120.0 | 0 | 0 | 0 | 60 | 0 | 0 | 0 | content {"stone": 150} |
| **Tower** `turtow` | 22500 | 984.38 | 125 | 0 | 150 | 90 | 100 | 0 | 0 | damage 1200; content {"gold": 500} |
| **Gate** `ukrwga` | 1500 | 5.62 | 0 | 0 | 10 | 0 | 0 | 0 | 0 | content {"wood": 32} |
| **Palisade** `ukrwwa` | 1500 | 5.62 | 0 | 0 | 10 | 0 | 0 | 0 | 0 | content {"wood": 32} |

<a id="юниты-по-классам"></a>
## Units by class

<a id="крестьяне"></a>
### Peasants

| Unit | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Peasant** `peatur` | 50 | 12.5 | 100 | 0 | 0 | 20 | 1.22 | 0.0 | semi-unique (2n) |

<a id="пикинёры-17-в"></a>
### Pikemen (17th century)

| Unit | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Ottoman Pikeman** `pikemantur` | 95 | 5.5 | 55 | 5 | 0 | 9 | 2.06 | 0.0 | semi-unique (2n) |

<a id="лёгкая-пехота"></a>
### Light Infantry

| Unit | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Light Infantryman** `lightinfantry` | 55 | 1.0 | 25 | 0 | 1 | 5 | 0.94 | 0.0 | semi-unique (2n) |
| **Light Infantryman (mercenary)** `lightinfantrydip` | 50 | 1.25 | 0 | 4 | 0 | 16 | 0.94 | 0.0 | common |
| **Roundshier (mercenary)** `roundshierdip` | 75 | 1.5 | 0 | 12 | 0 | 6 | 1.13 | 0.0 | common |

<a id="мушкетёры-17-в"></a>
### Musketeers (17th century)

| Unit | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Janissary** `jannisary` | 65 | 8.0 | 55 | 13 | 5 | 12 | 15.94 | 4.69 | unique |

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
| **Turkish archer** `archertur` | 65 | 3.0 | 45 | 4 | 0 | 150 | 16.88 | 4.38 | unique |
| **Turkish archer (mercenary)** `archerturdip` | 20 | 1.25 | 0 | 15 | 0 | 100 | 14.06 | 0.78 | common |

<a id="лёгкая-кавалерия"></a>
### Light Cavalry

| Unit | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Light cavalry (mercenary)** `lightcavalrydip` | 100 | 2.0 | 0 | 120 | 0 | 18 | 15.0 | 2.25 | common |

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
| **Heavy Sipahi** `sipahi` | 360 | 18.0 | 130 | 20 | 70 | 15 | 1.22 | 0.0 | unique |
| **Light Sipahi** `spakh` | 230 | 9.0 | 80 | 6 | 5 | 15 | 1.88 | 0.0 | unique |
| **Tatar** `tatar` | 185 | 11.25 | 70 | 6 | 0 | 140 | 20.63 | 4.69 | unique |

<a id="пушки"></a>
### Cannons

| Unit | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Cannon** `cannon` | 9000 | 75.0 | 0 | 400 | 400 | 1800 | 40.5 | 10.94 | common |

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
| **Galley** `galley` | 35000 | 50.0 | 0 | 900 | 800 | 1000 | 58.13 | 1.56 | common |
| **Xebec** `xebec` | 65000 | 230.0 | 0 | 1600 | 320 | 1800 | 31.88 | 1.56 | semi-unique (2n) |
| **Yacht** `yachttur` | 35000 | 48.0 | 0 | 450 | 150 | 0 | 30.94 | 21.88 | unique |

<a id="офицеры"></a>
### Officers

| Unit | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Officer** `officertur` | 125 | 7.5 | 50 | 100 | 0 | 30 | 1.22 | 0.0 | semi-unique (2n) |

<a id="барабанщики-и-волынщики"></a>
### Drummers and pipers

| Unit | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Drummer, 17th century** `drummertur` | 50 | 4.0 | 30 | 15 | 0 | — | — | — | semi-unique (2n) |

<a id="священники"></a>
### Priests

| Unit | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Mullah** `mullah` | 75 | 15.0 | 30 | 10 | 0 | 15 | 9.38 | 0.0 | semi-unique (2n) |

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

<a id="апгрейды-181"></a>
<a id="улучшения-181"></a>
## Upgrades (181)

The full list is in the [chapter “Upgrades”](../05_upgrades/README.md).

By buildings:

- **aca** (aca): 36
- **mil** (mil): 1
- **bla** (bla): 6
- **sta** (sta): 36
- **bar** (bar): 51
- **art** (art): 24
- **cen** (cen): 1
- **mines** (Mine): 18
