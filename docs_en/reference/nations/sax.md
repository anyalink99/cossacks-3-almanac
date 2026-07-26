# Saxony (`sax`)
_Saxony_

[← Index](../README.md) · [← All nations](README.md)

<a id="кластер"></a>
## Cluster

- **Shared cluster:** `eur` (mill/sto/mar/tow use the suffix `eur+`)
- **Peasant:** `peaaus`
- **Cluster infantry:** cluster `eur`

<a id="уникальные-юниты-3"></a>
## Unique units (3)

| Unit | role | HP | damage | recharge | far (tile) |
|---|---|---:|---:|---:|---:|
| **Grenadier** `grenadiersax` | Grenadier | 100 | 19 | 5.31 | 17.81 |
| **Cavalry Guard** `guardcavalrysax` | Heavy Cavalry | 320 | 15 | 0.0 | 1.22 |
| **Musketeer, 18th century** `musketeer18sax` | Shooter | 90 | 19 | 4.38 | 16.88 |

<a id="здания"></a>
## Buildings

<a id="уникальные-для-нации-10"></a>
### Unique to the nation (10)

> **Bold** - values that differ from the basic ones (fashion for all nations) for the same type of building.

| Building | HP | Time (g-sec) | cost% | F | W | S | G | I | C | farm | produces |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Academy** `saxaca` | 63000 | 625.0 | 300 | 0 | 1250 | 1100 | 0 | 0 | 0 | 0 | — |
| **Artillery Depot** `saxart` | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |
| **Barracks, 18th century** `saxba2` | 55000 | 5625.0 | 200 | 0 | 1700 | 2950 | 4000 | 0 | 0 | 250 | archersco, bagpiper, chasseur, drummer18, grenadier (+19) |
| **Barracks, 17th century** `saxbar` | 40000 | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | archer, archertur, drummer, drummerrus, drummertur (+24) |
| **Blacksmith** `saxbla` | 5500 | 93.75 | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| **Town Hall** `saxcen` | 4000 | 156.25 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | peaaus, peaeng, peapol, pearus, peasco (+3) |
| **Diplomatic Center** `saxdip` | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip (+3) |
| **Housing** `saxhou` | 4000 | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| **Stable** `saxsta` | 20000 | 625.0 | 200 | 0 | 2500 | 100 | 600 | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier (+25) |
| **Cathedral** `saxtem` | 4200 | 156.25 | 300 | 0 | 1000 | 1200 | 0 | 500 | 0 | 0 | mullah, padre, pope, priest |

<a id="общий-кластер-12"></a>
### Shared cluster (12)

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
| **Peasant** `peaaus` | 50 | 12.5 | 100 | 0 | 0 | 20 | 1.22 | 0.0 | shared(5n) |

<a id="пикинёры-17-в"></a>
### Pikemen (17th century)

| Unit | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Pikeman, 17th century** `pikeman` | 90 | 4.5 | 25 | 3 | 20 | 8 | 1.88 | 0.0 | shared(13n) |

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
| **Musketeer, 17th century** `musketeer` | 70 | 6.0 | 45 | 6 | 5 | 12 | 15.0 | 4.69 | shared(11n) |

<a id="мушкетёры-18-в"></a>
### Musketeers (18th century)

| Unit | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Musketeer, 18th century** `musketeer18sax` | 90 | 4.5 | 40 | 45 | 40 | 19 | 16.88 | 4.38 | unique |

<a id="гренадёры"></a>
### Grenadiers

| Unit | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Grenadier (mercenary)** `grenadierdip` | 30 | 1.5 | 0 | 25 | 0 | 16 | 15.0 | 4.69 | common |
| **Grenadier** `grenadiersax` | 100 | 6.0 | 50 | 60 | 40 | 19 | 17.81 | 5.31 | unique |

<a id="лучники"></a>
### Archerand

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
| **Dragoon, 17th century** `dragoon` | 220 | 15.0 | 90 | 7 | 5 | 15 | 15.0 | 5.62 | shared(16n) |
| **Dragoon, 18th century** `dragoon18` | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | shared(13n) |
| **Dragoon, 18th century (mercenary)** `dragoon18dip` | 100 | 2.0 | 0 | 120 | 0 | 18 | 15.0 | 2.25 | common |

<a id="тяжёлая-кавалерия"></a>
### Heavy Cavalry

| Unit | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Sich Cossack (mercenary)** `cossacksichdip` | 150 | 2.5 | 0 | 60 | 0 | 8 | 1.22 | 0.0 | common |
| **Cuirassier** `cuirassier` | 300 | 22.5 | 120 | 35 | 25 | 14 | 1.22 | 0.0 | shared(17n) |
| **Cavalry Guard** `guardcavalrysax` | 320 | 24.0 | 140 | 50 | 20 | 15 | 1.22 | 0.0 | unique |
| **Reiter** `reiter` | 300 | 24.0 | 120 | 10 | 40 | 15 | 1.22 | 0.0 | shared(14n) |

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
| **Officer, 17th century** `officer` | 125 | 10.0 | 50 | 150 | 30 | 30 | 1.22 | 0.0 | shared(16n) |
| **Officer, 18th century** `officer18` | 125 | 6.0 | 50 | 200 | 10 | 50 | 1.22 | 0.0 | shared(17n) |

<a id="барабанщики-и-волынщики"></a>
### Drummer, 17th centuryand pipers

| Unit | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Drummer, 17th century** `drummer` | 75 | 5.0 | 60 | 20 | 0 | — | — | — | shared(16n) |
| **Drummer, 18th century** `drummer18` | 100 | 6.0 | 50 | 30 | 0 | — | — | — | shared(16n) |

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

<a id="апгрейды-219"></a>
## Upgrades (219)

The full list is in the [chapter “Upgrades”](../05_upgrades/README.md).

By buildings:

- **aca** (aca): 36
- **bla** (bla): 6
- **sta** (sta): 60
- **bar** (bar): 24
- **ba2** (ba2): 39
- **art** (art): 24
- **cen** (cen): 1
- **mines** (Mine): 18