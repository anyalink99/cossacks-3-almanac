<a id="cossacks-3--темпы-производства"></a>
<a id="скорость-производства-юнитов"></a>
# Unit Production Rates

[← Tables and calculations](../README.md)

These tables show how many units one building can train per minute when its
queue runs continuously and sufficient resources and population capacity
are available.

**How production works** [^1]:

- Every building has one queue and trains only one unit at a time.
- The unit appears when its training progress reaches 100%.
- Its cost is paid in full when training begins.
- Training pauses when the population limit has been reached.

**Formula:**
- `rate_per_g_sec = 1 / unit.buildtime_sec`
- `rate_per_real_sec_fast = rate_per_g_sec × 1.4`
- `units_per_real_min_fast = rate_per_real_sec_fast × 60`

Entries are grouped by nation and then by production building.

<a id="содержание"></a>
## Contents

- **[Algeria](#alg--algeria-алжир)**
- **[Austria](#aus--austria-австрия)**
- **[Bavaria](#bav--bavaria-бавария)**
- **[Denmark](#den--denmark-дания)**
- **[England](#eng--england-англия)**
- **[France](#fra--france-франция)**
- **[Hungary](#hun--hungary-венгрия)**
- **[Netherlands](#net--netherlands-нидерланды)**
- **[Piedmont](#pie--piedmont-пьемонт)**
- **[Poland](#pol--poland-польша)**
- **[Portugal](#por--portugal-португалия)**
- **[Prussia](#pru--prussia-пруссия)**
- **[Russia](#rus--russia-россия)**
- **[Saxony](#sax--saxony-саксония)**
- **[Scotland](#sco--scotland-шотландия)**
- **[Spain](#spa--spain-испания)**
- **[Sweden](#swe--sweden-швеция)**
- **[Switzerland](#swi--switzerland-швейцария)**
- **[Turkey](#tur--turkey-турция)**
- **[Ukraine](#ukr--ukraine-украина)**
- **[Venice](#ven--venice-венеция)**

<a id="alg--algeria-алжир"></a>
<a id="алжир"></a>
## Algeria (`alg`)
<a id="algart--артиллерийское-депо"></a>
<a id="production-alg-algart"></a>
<a id="артиллерийское-депо--algart"></a>
### Artillery Depot — `algart`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Cannon** (`cannon`) | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| **Howitzer** (`howitzer`) | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| **Bombard** (`mortar`) | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |

<a id="algbar--казарма"></a>
<a id="production-alg-algbar"></a>
<a id="казарма--algbar"></a>
### Barracks — `algbar`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Archer** (`archer`) | 1.50 | 40.0 | **56.0** | 20 | 1 | 0 | 1 | — |
| **Drummer, 17th century** (`drummertur`) | 4.00 | 15.0 | **21.0** | 30 | 15 | 0 | 1 | — |
| **Light Infantryman** (`lightinfantry`) | 1.00 | 60.0 | **84.0** | 25 | 0 | 1 | 1 | — |
| **Officer** (`officertur`) | 7.50 | 8.0 | **11.2** | 50 | 100 | 0 | 1 | — |
| **Ottoman Pikeman** (`pikemantur`) | 5.50 | 10.9 | **15.3** | 55 | 5 | 0 | 1 | — |

<a id="algcen--городской-центр"></a>
<a id="production-alg-algcen"></a>
<a id="городской-центр--algcen"></a>
### Town Hall — `algcen`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Peasant** (`peatur`) | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 28 |

<a id="algdip--дипломатический-центр"></a>
<a id="production-alg-algdip"></a>
<a id="дипломатический-центр--algdip"></a>
### Diplomatic Center — `algdip`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Archer (mercenary)** (`archerdip`) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| **Turkish archer (mercenary)** (`archerturdip`) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| **Sich Cossack (mercenary)** (`cossacksichdip`) | 2.50 | 24.0 | **33.6** | 0 | 60 | 0 | 1 | 60 |
| **Dragoon, 18th century (mercenary)** (`dragoon18dip`) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| **Grenadier (mercenary)** (`grenadierdip`) | 1.50 | 40.0 | **56.0** | 0 | 25 | 0 | 1 | 36 |
| **Light cavalry (mercenary)** (`lightcavalrydip`) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| **Light Infantryman (mercenary)** (`lightinfantrydip`) | 1.25 | 48.0 | **67.2** | 0 | 4 | 0 | 1 | — |
| **Roundshier (mercenary)** (`roundshierdip`) | 1.50 | 40.0 | **56.0** | 0 | 12 | 0 | 1 | — |

<a id="algsta--конюшня"></a>
<a id="production-alg-algsta"></a>
<a id="конюшня--algsta"></a>
### Stable — `algsta`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Mameluke** (`mameluke`) | 12.00 | 5.0 | **7.0** | 100 | 8 | 0 | 1 | 60 |

<a id="algtem--мечеть"></a>
<a id="production-alg-algtem"></a>
<a id="мечеть--algtem"></a>
### Mosque — `algtem`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Mullah** (`mullah`) | 15.00 | 4.0 | **5.6** | 30 | 10 | 0 | 1 | — |

<a id="production-alg-turmil"></a>
<a id="мельница--turmil"></a>
### Mill — `turmil`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |

<a id="production-alg-turpor"></a>
<a id="порт--turpor"></a>
### Shipyard — `turpor`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Ship of the Line** (`battleship`) | 390.00 | 0.2 | **0.2** | 0 | 3200 | 700 | 1 | — |
| **Ferry** (`ferry`) | 56.00 | 1.1 | **1.5** | 0 | 50 | 100 | 1 | — |
| **Boat** (`fishboat`) | 40.00 | 1.5 | **2.1** | 0 | 0 | 0 | 1 | — |
| **Galley** (`galley`) | 50.00 | 1.2 | **1.7** | 0 | 900 | 800 | 1 | — |
| **Xebec** (`xebec`) | 230.00 | 0.3 | **0.4** | 0 | 1600 | 320 | 1 | — |

[↑ to contents](#содержание)

<a id="aus--austria-австрия"></a>
<a id="австрия"></a>
## Austria (`aus`)
<a id="ausart--артиллерийское-депо"></a>
<a id="production-aus-ausart"></a>
<a id="артиллерийское-депо--ausart"></a>
### Artillery Depot — `ausart`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Cannon** (`cannon`) | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| **Howitzer** (`howitzer`) | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| **Bombard** (`mortar`) | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| **Multi-barrelled Cannon** (`multicannon`) | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

<a id="ausba2--казарма-18в"></a>
<a id="production-aus-ausba2"></a>
<a id="казарма-18в--ausba2"></a>
### Barracks, 18th century — `ausba2`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Drummer, 18th century** (`drummer18`) | 6.00 | 10.0 | **14.0** | 50 | 30 | 0 | 1 | — |
| **Grenadier** (`grenadier`) | 6.00 | 10.0 | **14.0** | 80 | 60 | 40 | 1 | 36 |
| **Musketeer, 18th century** (`musketeer18`) | 4.50 | 13.3 | **18.7** | 50 | 40 | 40 | 1 | — |
| **Officer, 18th century** (`officer18`) | 6.00 | 10.0 | **14.0** | 50 | 200 | 10 | 1 | — |
| **Pandur** (`pandur`) | 5.50 | 10.9 | **15.3** | 40 | 15 | 10 | 1 | — |
| **Pikeman, 18th century** (`pikeman18`) | 1.25 | 48.0 | **67.2** | 30 | 2 | 0 | 1 | — |

<a id="ausbar--казарма-17в"></a>
<a id="production-aus-ausbar"></a>
<a id="казарма-17в--ausbar"></a>
### Barracks, 17th century — `ausbar`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Drummer, 17th century** (`drummer`) | 5.00 | 12.0 | **16.8** | 60 | 20 | 0 | 1 | — |
| **Musketeer, 17th century** (`musketeeraus`) | 6.50 | 9.2 | **12.9** | 35 | 9 | 15 | 1 | — |
| **Officer, 17th century** (`officer`) | 10.00 | 6.0 | **8.4** | 50 | 150 | 30 | 1 | — |
| **Pikeman, 17th century** (`pikeman`) | 4.50 | 13.3 | **18.7** | 25 | 3 | 20 | 1 | — |
| **Roundshier** (`roundshier`) | 4.00 | 15.0 | **21.0** | 20 | 3 | 25 | 1 | — |
<a id="auscen--городской-центр"></a>
<a id="production-aus-auscen"></a>
<a id="городской-центр--auscen"></a>
### Town Hall — `auscen`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Peasant** (`peaaus`) | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

<a id="ausdip--дипломатический-центр"></a>
<a id="production-aus-ausdip"></a>
<a id="дипломатический-центр--ausdip"></a>
### Diplomatic Center — `ausdip`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Archer (mercenary)** (`archerdip`) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| **Turkish archer (mercenary)** (`archerturdip`) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| **Sich Cossack (mercenary)** (`cossacksichdip`) | 2.50 | 24.0 | **33.6** | 0 | 60 | 0 | 1 | 60 |
| **Dragoon, 18th century (mercenary)** (`dragoon18dip`) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| **Grenadier (mercenary)** (`grenadierdip`) | 1.50 | 40.0 | **56.0** | 0 | 25 | 0 | 1 | 36 |
| **Light cavalry (mercenary)** (`lightcavalrydip`) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| **Light Infantryman (mercenary)** (`lightinfantrydip`) | 1.25 | 48.0 | **67.2** | 0 | 4 | 0 | 1 | — |
| **Roundshier (mercenary)** (`roundshierdip`) | 1.50 | 40.0 | **56.0** | 0 | 12 | 0 | 1 | — |

<a id="aussta--конюшня"></a>
<a id="production-aus-aussta"></a>
<a id="конюшня--aussta"></a>
### Stable — `aussta`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Croat** (`croat`) | 15.75 | 3.8 | **5.3** | 80 | 6 | 2 | 1 | 60 |
| **Cuirassier** (`cuirassier`) | 22.50 | 2.7 | **3.7** | 120 | 35 | 25 | 1 | 75 |
| **Dragoon, 17th century** (`dragoon`) | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | 60 |
| **Dragoon, 18th century** (`dragoon18`) | 22.50 | 2.7 | **3.7** | 70 | 60 | 7 | 1 | 60 |
| **Hussar** (`hussar`) | 15.00 | 4.0 | **5.6** | 70 | 20 | 2 | 1 | 60 |
| **Reiter** (`reiter`) | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | 75 |

<a id="austem--собор"></a>
<a id="production-aus-austem"></a>
<a id="собор--austem"></a>
### Cathedral — `austem`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Priest** (`priest`) | 20.00 | 3.0 | **4.2** | 60 | 25 | 0 | 1 | — |

<a id="production-aus-eurmil"></a>
<a id="мельница--eurmil"></a>
### Mill — `eurmil`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |

<a id="production-aus-eurpor"></a>
<a id="порт--eurpor"></a>
### Shipyard — `eurpor`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Ship of the Line** (`battleship`) | 390.00 | 0.2 | **0.2** | 0 | 3200 | 700 | 1 | — |
| **Ferry** (`ferry`) | 56.00 | 1.1 | **1.5** | 0 | 50 | 100 | 1 | — |
| **Boat** (`fishboat`) | 40.00 | 1.5 | **2.1** | 0 | 0 | 0 | 1 | — |
| **Frigate** (`frigate`) | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| **Galley** (`galley`) | 50.00 | 1.2 | **1.7** | 0 | 900 | 800 | 1 | — |
| **Yacht** (`yacht`) | 48.00 | 1.2 | **1.8** | 0 | 450 | 150 | 1 | — |

[↑ to contents](#содержание)

<a id="bav--bavaria-бавария"></a>
<a id="бавария"></a>
## Bavaria (`bav`)
<a id="bavart--артиллерийское-депо"></a>
<a id="production-bav-bavart"></a>
<a id="артиллерийское-депо--bavart"></a>
### Artillery Depot — `bavart`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Cannon** (`cannon`) | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| **Howitzer** (`howitzer`) | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| **Bombard** (`mortar`) | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| **Multi-barrelled Cannon** (`multicannon`) | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

<a id="bavba2--казарма-18в"></a>
<a id="production-bav-bavba2"></a>
<a id="казарма-18в--bavba2"></a>
### Barracks, 18th century — `bavba2`
| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Drummer, 18th century** (`drummer18`) | 6.00 | 10.0 | **14.0** | 50 | 30 | 0 | 1 | — |
| **Grenadier** (`grenadierbav`) | 6.00 | 10.0 | **14.0** | 95 | 70 | 40 | 1 | 36 |
| **Musketeer, 18th century** (`musketeer18bav`) | 5.00 | 12.0 | **16.8** | 60 | 55 | 35 | 1 | — |
| **Officer, 18th century** (`officer18`) | 6.00 | 10.0 | **14.0** | 50 | 200 | 10 | 1 | — |
| **Pikeman, 18th century** (`pikeman18`) | 1.25 | 48.0 | **67.2** | 30 | 2 | 0 | 1 | — |

<a id="bavbar--казарма-17в"></a>
<a id="production-bav-bavbar"></a>
<a id="казарма-17в--bavbar"></a>
### Barracks, 17th century — `bavbar`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Drummer, 17th century** (`drummer`) | 5.00 | 12.0 | **16.8** | 60 | 20 | 0 | 1 | — |
| **Musketeer, 17th century** (`musketeer`) | 6.00 | 10.0 | **14.0** | 45 | 6 | 5 | 1 | — |
| **Officer, 17th century** (`officer`) | 10.00 | 6.0 | **8.4** | 50 | 150 | 30 | 1 | — |
| **Pikeman, 17th century** (`pikeman`) | 4.50 | 13.3 | **18.7** | 25 | 3 | 20 | 1 | — |

<a id="bavcen--городской-центр"></a>
<a id="production-bav-bavcen"></a>
<a id="городской-центр--bavcen"></a>
### Town Hall — `bavcen`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Peasant** (`peaaus`) | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

<a id="bavdip--дипломатический-центр"></a>
<a id="production-bav-bavdip"></a>
<a id="дипломатический-центр--bavdip"></a>
### Diplomatic Center — `bavdip`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Archer (mercenary)** (`archerdip`) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| **Turkish archer (mercenary)** (`archerturdip`) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| **Sich Cossack (mercenary)** (`cossacksichdip`) | 2.50 | 24.0 | **33.6** | 0 | 60 | 0 | 1 | 60 |
| **Dragoon, 18th century (mercenary)** (`dragoon18dip`) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| **Grenadier (mercenary)** (`grenadierdip`) | 1.50 | 40.0 | **56.0** | 0 | 25 | 0 | 1 | 36 |
| **Light cavalry (mercenary)** (`lightcavalrydip`) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| **Light Infantryman (mercenary)** (`lightinfantrydip`) | 1.25 | 48.0 | **67.2** | 0 | 4 | 0 | 1 | — |
| **Roundshier (mercenary)** (`roundshierdip`) | 1.50 | 40.0 | **56.0** | 0 | 12 | 0 | 1 | — |

<a id="bavsta--конюшня"></a>
<a id="production-bav-bavsta"></a>
<a id="конюшня--bavsta"></a>
### Stable — `bavsta`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Cuirassier** (`cuirassier`) | 22.50 | 2.7 | **3.7** | 120 | 35 | 25 | 1 | 75 |
| **Dragoon, 17th century** (`dragoon`) | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | 60 |
| **Dragoon, 18th century** (`dragoon18`) | 22.50 | 2.7 | **3.7** | 70 | 60 | 7 | 1 | 60 |
| **Hussar** (`hussar`) | 15.00 | 4.0 | **5.6** | 70 | 20 | 2 | 1 | 60 |
| **Reiter** (`reiter`) | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | 75 |

<a id="bavtem--собор"></a>
<a id="production-bav-bavtem"></a>
<a id="собор--bavtem"></a>
### Cathedral — `bavtem`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Priest** (`priest`) | 20.00 | 3.0 | **4.2** | 60 | 25 | 0 | 1 | — |

<a id="eurmil--мельница"></a>
<a id="production-bav-eurmil"></a>
<a id="мельница--eurmil-1"></a>
### Mill — `eurmil`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |

<a id="eurpor--порт"></a>
<a id="production-bav-eurpor"></a>
<a id="порт--eurpor-1"></a>
### Shipyard — `eurpor`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Ship of the Line** (`battleship`) | 390.00 | 0.2 | **0.2** | 0 | 3200 | 700 | 1 | — |
| **Ferry** (`ferry`) | 56.00 | 1.1 | **1.5** | 0 | 50 | 100 | 1 | — |
| **Boat** (`fishboat`) | 40.00 | 1.5 | **2.1** | 0 | 0 | 0 | 1 | — |
| **Frigate** (`frigate`) | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| **Galley** (`galley`) | 50.00 | 1.2 | **1.7** | 0 | 900 | 800 | 1 | — |
| **Yacht** (`yacht`) | 48.00 | 1.2 | **1.8** | 0 | 450 | 150 | 1 | — |

[↑ to contents](#содержание)

<a id="den--denmark-дания"></a>
<a id="дания"></a>
## Denmark (`den`)
<a id="denart--артиллерийское-депо"></a>
<a id="production-den-denart"></a>
<a id="артиллерийское-депо--denart"></a>
### Artillery Depot — `denart`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Cannon** (`cannon`) | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| **Howitzer** (`howitzer`) | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| **Bombard** (`mortar`) | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| **Multi-barrelled Cannon** (`multicannon`) | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

<a id="denba2--казарма-18в"></a>
<a id="production-den-denba2"></a>
<a id="казарма-18в--denba2"></a>
### Barracks, 18th century — `denba2`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Drummer, 18th century** (`drummer18`) | 6.00 | 10.0 | **14.0** | 50 | 30 | 0 | 1 | — |
| **Grenadier** (`grenadierden`) | 6.50 | 9.2 | **12.9** | 100 | 90 | 40 | 1 | 36 |
| **Musketeer, 18th century** (`musketeer18den`) | 5.50 | 10.9 | **15.3** | 50 | 80 | 40 | 1 | — |
| **Officer, 18th century** (`officer18`) | 6.00 | 10.0 | **14.0** | 50 | 200 | 10 | 1 | — |
| **Pikeman, 18th century** (`pikeman18`) | 1.25 | 48.0 | **67.2** | 30 | 2 | 0 | 1 | — |

<a id="denbar--казарма-17в"></a>
<a id="production-den-denbar"></a>
<a id="казарма-17в--denbar"></a>
### Barracks, 17th century — `denbar`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Drummer, 17th century** (`drummer`) | 5.00 | 12.0 | **16.8** | 60 | 20 | 0 | 1 | — |
| **Musketeer, 17th century** (`musketeer`) | 6.00 | 10.0 | **14.0** | 45 | 6 | 5 | 1 | — |
| **Officer, 17th century** (`officer`) | 10.00 | 6.0 | **8.4** | 50 | 150 | 30 | 1 | — |
| **Pikeman, 17th century** (`pikeman`) | 4.50 | 13.3 | **18.7** | 25 | 3 | 20 | 1 | — |

<a id="dencen--городской-центр"></a>
<a id="production-den-dencen"></a>
<a id="городской-центр--dencen"></a>
### Town Hall — `dencen`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Peasant** (`peaeng`) | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

<a id="dendip--дипломатический-центр"></a>
<a id="production-den-dendip"></a>
<a id="дипломатический-центр--dendip"></a>
### Diplomatic Center — `dendip`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Archer (mercenary)** (`archerdip`) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| **Turkish archer (mercenary)** (`archerturdip`) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| **Sich Cossack (mercenary)** (`cossacksichdip`) | 2.50 | 24.0 | **33.6** | 0 | 60 | 0 | 1 | 60 |
| **Dragoon, 18th century (mercenary)** (`dragoon18dip`) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| **Grenadier (mercenary)** (`grenadierdip`) | 1.50 | 40.0 | **56.0** | 0 | 25 | 0 | 1 | 36 |
| **Light cavalry (mercenary)** (`lightcavalrydip`) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| **Light Infantryman (mercenary)** (`lightinfantrydip`) | 1.25 | 48.0 | **67.2** | 0 | 4 | 0 | 1 | — |
| **Roundshier (mercenary)** (`roundshierdip`) | 1.50 | 40.0 | **56.0** | 0 | 12 | 0 | 1 | — |

<a id="densta--конюшня"></a>
<a id="production-den-densta"></a>
<a id="конюшня--densta"></a>
### Stable — `densta`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Cuirassier** (`cuirassier`) | 22.50 | 2.7 | **3.7** | 120 | 35 | 25 | 1 | 75 |
| **Dragoon, 17th century** (`dragoon`) | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | 60 |
| **Dragoon, 18th century** (`dragoon18`) | 22.50 | 2.7 | **3.7** | 70 | 60 | 7 | 1 | 60 |
| **Hussar** (`hussar`) | 15.00 | 4.0 | **5.6** | 70 | 20 | 2 | 1 | 60 |
| **Reiter** (`reiter`) | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | 75 |

<a id="dentem--собор"></a>
<a id="production-den-dentem"></a>
<a id="собор--dentem"></a>
### Cathedral — `dentem`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Priest** (`priest`) | 20.00 | 3.0 | **4.2** | 60 | 25 | 0 | 1 | — |

<a id="eurmil--мельница-1"></a>
<a id="production-den-eurmil"></a>
<a id="мельница--eurmil-2"></a>
### Mill — `eurmil`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |

<a id="eurpor--порт-1"></a>
<a id="production-den-eurpor"></a>
<a id="порт--eurpor-2"></a>
### Shipyard — `eurpor`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Ship of the Line** (`battleship`) | 390.00 | 0.2 | **0.2** | 0 | 3200 | 700 | 1 | — |
| **Ferry** (`ferry`) | 56.00 | 1.1 | **1.5** | 0 | 50 | 100 | 1 | — |
| **Boat** (`fishboat`) | 40.00 | 1.5 | **2.1** | 0 | 0 | 0 | 1 | — |
| **Frigate** (`frigate`) | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| **Galley** (`galley`) | 50.00 | 1.2 | **1.7** | 0 | 900 | 800 | 1 | — |
| **Yacht** (`yacht`) | 48.00 | 1.2 | **1.8** | 0 | 450 | 150 | 1 | — |

[↑ to contents](#содержание)

<a id="eng--england-англия"></a>
<a id="англия"></a>
## England (`eng`)
<a id="engart--артиллерийское-депо"></a>
<a id="production-eng-engart"></a>
<a id="артиллерийское-депо--engart"></a>
### Artillery Depot — `engart`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Cannon** (`cannon`) | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| **Howitzer** (`howitzer`) | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| **Bombard** (`mortar`) | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| **Multi-barrelled Cannon** (`multicannon`) | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

<a id="engba2--казарма-18в"></a>
<a id="production-eng-engba2"></a>
<a id="казарма-18в--engba2"></a>
### Barracks, 18th century — `engba2`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Bagpiper** (`bagpiper`) | 7.00 | 8.6 | **12.0** | 120 | 20 | 0 | 1 | — |
| **Grenadier** (`grenadier`) | 6.00 | 10.0 | **14.0** | 80 | 60 | 40 | 1 | 36 |
| **Highlander** (`highlander`) | 6.50 | 9.2 | **12.9** | 90 | 25 | 10 | 1 | 39 |
| **Musketeer, 18th century** (`musketeer18`) | 4.50 | 13.3 | **18.7** | 50 | 40 | 40 | 1 | — |
| **Officer, 18th century** (`officer18`) | 6.00 | 10.0 | **14.0** | 50 | 200 | 10 | 1 | — |
| **Pikeman, 18th century** (`pikeman18`) | 1.25 | 48.0 | **67.2** | 30 | 2 | 0 | 1 | — |

<a id="engbar--казарма-17в"></a>
<a id="production-eng-engbar"></a>
<a id="казарма-17в--engbar"></a>
### Barracks, 17th century — `engbar`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Drummer, 17th century** (`drummer`) | 5.00 | 12.0 | **16.8** | 60 | 20 | 0 | 1 | — |
| **Musketeer, 17th century** (`musketeer`) | 6.00 | 10.0 | **14.0** | 45 | 6 | 5 | 1 | — |
| **Officer, 17th century** (`officer`) | 10.00 | 6.0 | **8.4** | 50 | 150 | 30 | 1 | — |
| **Pikeman, 17th century** (`pikeman`) | 4.50 | 13.3 | **18.7** | 25 | 3 | 20 | 1 | — |

<a id="engcen--городской-центр"></a>
<a id="production-eng-engcen"></a>
<a id="городской-центр--engcen"></a>
### Town Hall — `engcen`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Peasant** (`peaeng`) | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

<a id="engdip--дипломатический-центр"></a>
<a id="production-eng-engdip"></a>
<a id="дипломатический-центр--engdip"></a>
### Diplomatic Center — `engdip`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Archer (mercenary)** (`archerdip`) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| **Turkish archer (mercenary)** (`archerturdip`) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| **Sich Cossack (mercenary)** (`cossacksichdip`) | 2.50 | 24.0 | **33.6** | 0 | 60 | 0 | 1 | 60 |
| **Dragoon, 18th century (mercenary)** (`dragoon18dip`) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| **Grenadier (mercenary)** (`grenadierdip`) | 1.50 | 40.0 | **56.0** | 0 | 25 | 0 | 1 | 36 |
| **Light cavalry (mercenary)** (`lightcavalrydip`) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| **Light Infantryman (mercenary)** (`lightinfantrydip`) | 1.25 | 48.0 | **67.2** | 0 | 4 | 0 | 1 | — |
| **Roundshier (mercenary)** (`roundshierdip`) | 1.50 | 40.0 | **56.0** | 0 | 12 | 0 | 1 | — |

<a id="engsta--конюшня"></a>
<a id="production-eng-engsta"></a>
<a id="конюшня--engsta"></a>
### Stable — `engsta`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Cuirassier** (`cuirassier`) | 22.50 | 2.7 | **3.7** | 120 | 35 | 25 | 1 | 75 |
| **Dragoon, 17th century** (`dragoon`) | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | 60 |
| **Dragoon, 18th century** (`dragoon18`) | 22.50 | 2.7 | **3.7** | 70 | 60 | 7 | 1 | 60 |
| **Hussar** (`hussar`) | 15.00 | 4.0 | **5.6** | 70 | 20 | 2 | 1 | 60 |
| **Reiter** (`reiter`) | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | 75 |

<a id="engtem--собор"></a>
<a id="production-eng-engtem"></a>
<a id="собор--engtem"></a>
### Cathedral — `engtem`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Priest** (`priest`) | 20.00 | 3.0 | **4.2** | 60 | 25 | 0 | 1 | — |

<a id="eurmil--мельница-2"></a>
<a id="production-eng-eurmil"></a>
<a id="мельница--eurmil-3"></a>
### Mill — `eurmil`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |

<a id="eurpor--порт-2"></a>
<a id="production-eng-eurpor"></a>
<a id="порт--eurpor-3"></a>
### Shipyard — `eurpor`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Ship of the Line** (`battleship`) | 390.00 | 0.2 | **0.2** | 0 | 3200 | 700 | 1 | — |
| **Ferry** (`ferry`) | 56.00 | 1.1 | **1.5** | 0 | 50 | 100 | 1 | — |
| **Boat** (`fishboat`) | 40.00 | 1.5 | **2.1** | 0 | 0 | 0 | 1 | — |
| **Frigate** (`frigate`) | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| **Galley** (`galley`) | 50.00 | 1.2 | **1.7** | 0 | 900 | 800 | 1 | — |
| **Yacht** (`yacht`) | 48.00 | 1.2 | **1.8** | 0 | 450 | 150 | 1 | — |

[↑ to contents](#содержание)

<a id="fra--france-франция"></a>
<a id="франция"></a>
## France (`fra`)
<a id="eurmil--мельница-3"></a>
<a id="production-fra-eurmil"></a>
<a id="мельница--eurmil-4"></a>
### Mill — `eurmil`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |

<a id="eurpor--порт-3"></a>
<a id="production-fra-eurpor"></a>
<a id="порт--eurpor-4"></a>
### Shipyard — `eurpor`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Ship of the Line** (`battleship`) | 390.00 | 0.2 | **0.2** | 0 | 3200 | 700 | 1 | — |
| **Ferry** (`ferry`) | 56.00 | 1.1 | **1.5** | 0 | 50 | 100 | 1 | — |
| **Boat** (`fishboat`) | 40.00 | 1.5 | **2.1** | 0 | 0 | 0 | 1 | — |
| **Frigate** (`frigate`) | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| **Galley** (`galley`) | 50.00 | 1.2 | **1.7** | 0 | 900 | 800 | 1 | — |
| **Yacht** (`yacht`) | 48.00 | 1.2 | **1.8** | 0 | 450 | 150 | 1 | — |

<a id="fraart--артиллерийское-депо"></a>
<a id="production-fra-fraart"></a>
<a id="артиллерийское-депо--fraart"></a>
### Artillery Depot — `fraart`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Cannon** (`cannon`) | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| **Howitzer** (`howitzer`) | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| **Bombard** (`mortar`) | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| **Multi-barrelled Cannon** (`multicannon`) | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

<a id="fraba2--казарма-18в"></a>
<a id="production-fra-fraba2"></a>
<a id="казарма-18в--fraba2"></a>
### Barracks, 18th century — `fraba2`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Chasseur** (`chasseur`) | 7.50 | 8.0 | **11.2** | 50 | 45 | 15 | 1 | — |
| **Drummer, 18th century** (`drummer18`) | 6.00 | 10.0 | **14.0** | 50 | 30 | 0 | 1 | — |
| **Grenadier** (`grenadier`) | 6.00 | 10.0 | **14.0** | 80 | 60 | 40 | 1 | 36 |
| **Musketeer, 18th century** (`musketeer18`) | 4.50 | 13.3 | **18.7** | 50 | 40 | 40 | 1 | — |
| **Officer, 18th century** (`officer18`) | 6.00 | 10.0 | **14.0** | 50 | 200 | 10 | 1 | — |
| **Pikeman, 18th century** (`pikeman18`) | 1.25 | 48.0 | **67.2** | 30 | 2 | 0 | 1 | — |

<a id="frabar--казарма-17в"></a>
<a id="production-fra-frabar"></a>
<a id="казарма-17в--frabar"></a>
### Barracks, 17th century — `frabar`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Drummer, 17th century** (`drummer`) | 5.00 | 12.0 | **16.8** | 60 | 20 | 0 | 1 | — |
| **Musketeer, 17th century** (`musketeer`) | 6.00 | 10.0 | **14.0** | 45 | 6 | 5 | 1 | — |
| **Officer, 17th century** (`officer`) | 10.00 | 6.0 | **8.4** | 50 | 150 | 30 | 1 | — |
| **Pikeman, 17th century** (`pikeman`) | 4.50 | 13.3 | **18.7** | 25 | 3 | 20 | 1 | — |

<a id="fracen--городской-центр"></a>
<a id="production-fra-fracen"></a>
<a id="городской-центр--fracen"></a>
### Town Hall — `fracen`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Peasant** (`peaeng`) | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

<a id="fradip--дипломатический-центр"></a>
<a id="production-fra-fradip"></a>
<a id="дипломатический-центр--fradip"></a>
### Diplomatic Center — `fradip`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Archer (mercenary)** (`archerdip`) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| **Turkish archer (mercenary)** (`archerturdip`) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| **Sich Cossack (mercenary)** (`cossacksichdip`) | 2.50 | 24.0 | **33.6** | 0 | 60 | 0 | 1 | 60 |
| **Dragoon, 18th century (mercenary)** (`dragoon18dip`) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| **Grenadier (mercenary)** (`grenadierdip`) | 1.50 | 40.0 | **56.0** | 0 | 25 | 0 | 1 | 36 |
| **Light cavalry (mercenary)** (`lightcavalrydip`) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| **Light Infantryman (mercenary)** (`lightinfantrydip`) | 1.25 | 48.0 | **67.2** | 0 | 4 | 0 | 1 | — |
| **Roundshier (mercenary)** (`roundshierdip`) | 1.50 | 40.0 | **56.0** | 0 | 12 | 0 | 1 | — |

<a id="frasta--конюшня"></a>
<a id="production-fra-frasta"></a>
<a id="конюшня--frasta"></a>
### Stable — `frasta`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Cuirassier** (`cuirassier`) | 22.50 | 2.7 | **3.7** | 120 | 35 | 25 | 1 | 75 |
| **Dragoon, 17th century** (`dragoon`) | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | 60 |
| **Dragoon, 18th century** (`dragoon18fra`) | 15.00 | 4.0 | **5.6** | 50 | 30 | 6 | 1 | 45 |
| **Hussar** (`hussar`) | 15.00 | 4.0 | **5.6** | 70 | 20 | 2 | 1 | 60 |
| **King's Musketeer** (`kingmusketeer`) | 27.00 | 2.2 | **3.1** | 100 | 100 | 8 | 1 | 75 |
| **Reiter** (`reiter`) | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | 75 |

<a id="fratem--собор"></a>
<a id="production-fra-fratem"></a>
<a id="собор--fratem"></a>
### Cathedral — `fratem`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Priest** (`priest`) | 20.00 | 3.0 | **4.2** | 60 | 25 | 0 | 1 | — |

[↑ to contents](#содержание)

<a id="hun--hungary-венгрия"></a>
<a id="венгрия"></a>
## Hungary (`hun`)
<a id="production-hun-eurmil"></a>
<a id="мельница--eurmil-5"></a>
### Mill — `eurmil`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |

<a id="production-hun-eurpor"></a>
<a id="порт--eurpor-5"></a>
### Shipyard — `eurpor`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Ship of the Line** (`battleship`) | 390.00 | 0.2 | **0.2** | 0 | 3200 | 700 | 1 | — |
| **Ferry** (`ferry`) | 56.00 | 1.1 | **1.5** | 0 | 50 | 100 | 1 | — |
| **Boat** (`fishboat`) | 40.00 | 1.5 | **2.1** | 0 | 0 | 0 | 1 | — |
| **Frigate** (`frigate`) | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| **Galley** (`galley`) | 50.00 | 1.2 | **1.7** | 0 | 900 | 800 | 1 | — |
| **Yacht** (`yacht`) | 48.00 | 1.2 | **1.8** | 0 | 450 | 150 | 1 | — |

<a id="hunart--артиллерийское-депо"></a>
<a id="production-hun-hunart"></a>
<a id="артиллерийское-депо--hunart"></a>
### Artillery Depot — `hunart`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Cannon** (`cannon`) | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| **Howitzer** (`howitzer`) | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| **Bombard** (`mortar`) | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| **Multi-barrelled Cannon** (`multicannon`) | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

<a id="hunba2--казарма-18в"></a>
<a id="production-hun-hunba2"></a>
<a id="казарма-18в--hunba2"></a>
### Barracks, 18th century — `hunba2`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Drummer, 18th century** (`drummer18`) | 6.00 | 10.0 | **14.0** | 50 | 30 | 0 | 1 | — |
| **Grenadier** (`grenadierhun`) | 6.50 | 9.2 | **12.9** | 90 | 80 | 40 | 1 | 36 |
| **Musketeer, 18th century** (`musketeer18`) | 4.50 | 13.3 | **18.7** | 50 | 40 | 40 | 1 | — |
| **Officer, 18th century** (`officer18`) | 6.00 | 10.0 | **14.0** | 50 | 200 | 10 | 1 | — |
| **Szekely** (`pandurhun`) | 6.50 | 9.2 | **12.9** | 30 | 25 | 10 | 1 | — |
| **Pikeman, 18th century** (`pikeman18`) | 1.25 | 48.0 | **67.2** | 30 | 2 | 0 | 1 | — |

<a id="hunbar--казарма-17в"></a>
<a id="production-hun-hunbar"></a>
<a id="казарма-17в--hunbar"></a>
### Barracks, 17th century — `hunbar`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Drummer, 17th century** (`drummer`) | 5.00 | 12.0 | **16.8** | 60 | 20 | 0 | 1 | — |
| **Hajduk** (`gauduk`) | 4.50 | 13.3 | **18.7** | 35 | 4 | 4 | 1 | — |
| **Officer, 17th century** (`officer`) | 10.00 | 6.0 | **8.4** | 50 | 150 | 30 | 1 | — |
| **Pikeman, 17th century** (`pikeman`) | 4.50 | 13.3 | **18.7** | 25 | 3 | 20 | 1 | — |

<a id="huncen--городской-центр"></a>
<a id="production-hun-huncen"></a>
<a id="городской-центр--huncen"></a>
### Town Hall — `huncen`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Peasant** (`peapol`) | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

<a id="hundip--дипломатический-центр"></a>
<a id="production-hun-hundip"></a>
<a id="дипломатический-центр--hundip"></a>
### Diplomatic Center — `hundip`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Archer (mercenary)** (`archerdip`) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| **Turkish archer (mercenary)** (`archerturdip`) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| **Sich Cossack (mercenary)** (`cossacksichdip`) | 2.50 | 24.0 | **33.6** | 0 | 60 | 0 | 1 | 60 |
| **Dragoon, 18th century (mercenary)** (`dragoon18dip`) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| **Grenadier (mercenary)** (`grenadierdip`) | 1.50 | 40.0 | **56.0** | 0 | 25 | 0 | 1 | 36 |
| **Light cavalry (mercenary)** (`lightcavalrydip`) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| **Light Infantryman (mercenary)** (`lightinfantrydip`) | 1.25 | 48.0 | **67.2** | 0 | 4 | 0 | 1 | — |
| **Roundshier (mercenary)** (`roundshierdip`) | 1.50 | 40.0 | **56.0** | 0 | 12 | 0 | 1 | — |

<a id="hunsta--конюшня"></a>
<a id="production-hun-hunsta"></a>
<a id="конюшня--hunsta"></a>
### Stable — `hunsta`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Cuirassier** (`cuirassier`) | 22.50 | 2.7 | **3.7** | 120 | 35 | 25 | 1 | 75 |
| **Dragoon, 17th century** (`dragoon`) | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | 60 |
| **Hussar** (`hussarhun`) | 21.00 | 2.9 | **4.0** | 100 | 30 | 2 | 1 | 60 |
| **Light cavalry** (`lightcavalry`) | 21.00 | 2.9 | **4.0** | 90 | 50 | 6 | 1 | 60 |
| **Reiter** (`reiter`) | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | 75 |

<a id="huntem--собор"></a>
<a id="production-hun-huntem"></a>
<a id="собор--huntem"></a>
### Cathedral — `huntem`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Priest** (`priest`) | 20.00 | 3.0 | **4.2** | 60 | 25 | 0 | 1 | — |

[↑ to contents](#содержание)

<a id="net--netherlands-нидерланды"></a>
<a id="нидерланды"></a>
## Netherlands (`net`)
<a id="production-net-eurmil"></a>
<a id="мельница--eurmil-6"></a>
### Mill — `eurmil`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |

<a id="production-net-eurpor"></a>
<a id="порт--eurpor-6"></a>
### Shipyard — `eurpor`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Ship of the Line** (`battleship`) | 390.00 | 0.2 | **0.2** | 0 | 3200 | 700 | 1 | — |
| **Ferry** (`ferry`) | 56.00 | 1.1 | **1.5** | 0 | 50 | 100 | 1 | — |
| **Boat** (`fishboat`) | 40.00 | 1.5 | **2.1** | 0 | 0 | 0 | 1 | — |
| **Frigate** (`frigate`) | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| **Galley** (`galley`) | 50.00 | 1.2 | **1.7** | 0 | 900 | 800 | 1 | — |
| **Yacht** (`yacht`) | 48.00 | 1.2 | **1.8** | 0 | 450 | 150 | 1 | — |

<a id="netart--артиллерийское-депо"></a>
<a id="production-net-netart"></a>
<a id="артиллерийское-депо--netart"></a>
### Artillery Depot — `netart`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Cannon** (`cannon`) | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| **Howitzer** (`howitzer`) | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| **Bombard** (`mortar`) | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| **Multi-barrelled Cannon** (`multicannon`) | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

<a id="netba2--казарма-18в"></a>
<a id="production-net-netba2"></a>
<a id="казарма-18в--netba2"></a>
### Barracks, 18th century — `netba2`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Drummer, 18th century** (`drummer18`) | 6.00 | 10.0 | **14.0** | 50 | 30 | 0 | 1 | — |
| **Grenadier** (`grenadier`) | 6.00 | 10.0 | **14.0** | 80 | 60 | 40 | 1 | 36 |
| **Musketeer, 18th century** (`musketeer18`) | 4.50 | 13.3 | **18.7** | 50 | 40 | 40 | 1 | — |
| **Officer, 18th century** (`officer18`) | 6.00 | 10.0 | **14.0** | 50 | 200 | 10 | 1 | — |
| **Pikeman, 18th century** (`pikeman18`) | 1.25 | 48.0 | **67.2** | 30 | 2 | 0 | 1 | — |

<a id="netbar--казарма-17в"></a>
<a id="production-net-netbar"></a>
<a id="казарма-17в--netbar"></a>
### Barracks, 17th century — `netbar`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Drummer, 17th century** (`drummer`) | 5.00 | 12.0 | **16.8** | 60 | 20 | 0 | 1 | — |
| **Musketeer, 17th century** (`musketeernet`) | 5.00 | 12.0 | **16.8** | 50 | 8 | 4 | 1 | — |
| **Officer, 17th century** (`officer`) | 10.00 | 6.0 | **8.4** | 50 | 150 | 30 | 1 | — |
| **Pikeman, 17th century** (`pikeman`) | 4.50 | 13.3 | **18.7** | 25 | 3 | 20 | 1 | — |

<a id="netcen--городской-центр"></a>
<a id="production-net-netcen"></a>
<a id="городской-центр--netcen"></a>
### Town Hall — `netcen`
| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Peasant** (`peaeng`) | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

<a id="netdip--дипломатический-центр"></a>
<a id="production-net-netdip"></a>
<a id="дипломатический-центр--netdip"></a>
### Diplomatic Center — `netdip`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Archer (mercenary)** (`archerdip`) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| **Turkish archer (mercenary)** (`archerturdip`) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| **Sich Cossack (mercenary)** (`cossacksichdip`) | 2.50 | 24.0 | **33.6** | 0 | 60 | 0 | 1 | 60 |
| **Dragoon, 18th century (mercenary)** (`dragoon18dip`) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| **Grenadier (mercenary)** (`grenadierdip`) | 1.50 | 40.0 | **56.0** | 0 | 25 | 0 | 1 | 36 |
| **Light cavalry (mercenary)** (`lightcavalrydip`) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| **Light Infantryman (mercenary)** (`lightinfantrydip`) | 1.25 | 48.0 | **67.2** | 0 | 4 | 0 | 1 | — |
| **Roundshier (mercenary)** (`roundshierdip`) | 1.50 | 40.0 | **56.0** | 0 | 12 | 0 | 1 | — |

<a id="netsta--конюшня"></a>
<a id="production-net-netsta"></a>
<a id="конюшня--netsta"></a>
### Stable — `netsta`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Cuirassier** (`cuirassier`) | 22.50 | 2.7 | **3.7** | 120 | 35 | 25 | 1 | 75 |
| **Dragoon, 17th century** (`dragoon`) | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | 60 |
| **Dragoon, 18th century** (`dragoon18net`) | 24.00 | 2.5 | **3.5** | 100 | 70 | 7 | 1 | 75 |
| **Hussar** (`hussar`) | 15.00 | 4.0 | **5.6** | 70 | 20 | 2 | 1 | 60 |
| **Reiter** (`reiter`) | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | 75 |

<a id="nettem--собор"></a>
<a id="production-net-nettem"></a>
<a id="собор--nettem"></a>
### Cathedral — `nettem`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Priest** (`priest`) | 20.00 | 3.0 | **4.2** | 60 | 25 | 0 | 1 | — |

[↑ to contents](#содержание)

<a id="pie--piedmont-пьемонт"></a>
<a id="пьемонт"></a>
## Piedmont (`pie`)
<a id="eurmil--мельница-4"></a>
<a id="production-pie-eurmil"></a>
<a id="мельница--eurmil-7"></a>
### Mill — `eurmil`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |

<a id="eurpor--порт-4"></a>
<a id="production-pie-eurpor"></a>
<a id="порт--eurpor-7"></a>
### Shipyard — `eurpor`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Ship of the Line** (`battleship`) | 390.00 | 0.2 | **0.2** | 0 | 3200 | 700 | 1 | — |
| **Ferry** (`ferry`) | 56.00 | 1.1 | **1.5** | 0 | 50 | 100 | 1 | — |
| **Boat** (`fishboat`) | 40.00 | 1.5 | **2.1** | 0 | 0 | 0 | 1 | — |
| **Frigate** (`frigate`) | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| **Galley** (`galley`) | 50.00 | 1.2 | **1.7** | 0 | 900 | 800 | 1 | — |
| **Yacht** (`yacht`) | 48.00 | 1.2 | **1.8** | 0 | 450 | 150 | 1 | — |

<a id="pieart--артиллерийское-депо"></a>
<a id="production-pie-pieart"></a>
<a id="артиллерийское-депо--pieart"></a>
### Artillery Depot — `pieart`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Cannon** (`cannon`) | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| **Howitzer** (`howitzer`) | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| **Bombard** (`mortar`) | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| **Multi-barrelled Cannon** (`multicannon`) | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

<a id="pieba2--казарма-18в"></a>
<a id="production-pie-pieba2"></a>
<a id="казарма-18в--pieba2"></a>
### Barracks, 18th century — `pieba2`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Drummer, 18th century** (`drummer18`) | 6.00 | 10.0 | **14.0** | 50 | 30 | 0 | 1 | — |
| **Grenadier** (`grenadier`) | 6.00 | 10.0 | **14.0** | 80 | 60 | 40 | 1 | 36 |
| **Musketeer, 18th century** (`musketeer18`) | 4.50 | 13.3 | **18.7** | 50 | 40 | 40 | 1 | — |
| **Officer, 18th century** (`officer18`) | 6.00 | 10.0 | **14.0** | 50 | 200 | 10 | 1 | — |
| **Pikeman, 18th century** (`pikeman18`) | 1.25 | 48.0 | **67.2** | 30 | 2 | 0 | 1 | — |

<a id="piebar--казарма-17в"></a>
<a id="production-pie-piebar"></a>
<a id="казарма-17в--piebar"></a>
### Barracks, 17th century — `piebar`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Drummer, 17th century** (`drummer`) | 5.00 | 12.0 | **16.8** | 60 | 20 | 0 | 1 | — |
| **Musketeer, 17th century** (`musketeer`) | 6.00 | 10.0 | **14.0** | 45 | 6 | 5 | 1 | — |
| **Officer, 17th century** (`officer`) | 10.00 | 6.0 | **8.4** | 50 | 150 | 30 | 1 | — |
| **Pikeman, 17th century** (`pikeman`) | 4.50 | 13.3 | **18.7** | 25 | 3 | 20 | 1 | — |

<a id="piecen--городской-центр"></a>
<a id="production-pie-piecen"></a>
<a id="городской-центр--piecen"></a>
### Town Hall — `piecen`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Peasant** (`peaspa`) | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

<a id="piedip--дипломатический-центр"></a>
<a id="production-pie-piedip"></a>
<a id="дипломатический-центр--piedip"></a>
### Diplomatic Center — `piedip`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Archer (mercenary)** (`archerdip`) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| **Turkish archer (mercenary)** (`archerturdip`) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| **Sich Cossack (mercenary)** (`cossacksichdip`) | 2.50 | 24.0 | **33.6** | 0 | 60 | 0 | 1 | 60 |
| **Dragoon, 18th century (mercenary)** (`dragoon18dip`) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| **Grenadier (mercenary)** (`grenadierdip`) | 1.50 | 40.0 | **56.0** | 0 | 25 | 0 | 1 | 36 |
| **Light cavalry (mercenary)** (`lightcavalrydip`) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| **Light Infantryman (mercenary)** (`lightinfantrydip`) | 1.25 | 48.0 | **67.2** | 0 | 4 | 0 | 1 | — |
| **Roundshier (mercenary)** (`roundshierdip`) | 1.50 | 40.0 | **56.0** | 0 | 12 | 0 | 1 | — |

<a id="piesta--конюшня"></a>
<a id="production-pie-piesta"></a>
<a id="конюшня--piesta"></a>
### Stable — `piesta`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Cuirassier** (`cuirassier`) | 22.50 | 2.7 | **3.7** | 120 | 35 | 25 | 1 | 75 |
| **Dragoon, 17th century** (`dragoon`) | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | 60 |
| **Dragoon, 18th century** (`dragoon18pie`) | 20.25 | 3.0 | **4.1** | 60 | 65 | 7 | 1 | 60 |
| **Hussar** (`hussar`) | 15.00 | 4.0 | **5.6** | 70 | 20 | 2 | 1 | 60 |
| **Reiter** (`reiter`) | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | 75 |

<a id="pietem--собор"></a>
<a id="production-pie-pietem"></a>
<a id="собор--pietem"></a>
### Cathedral — `pietem`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Padre** (`padre`) | 25.00 | 2.4 | **3.4** | 50 | 40 | 0 | 1 | — |

[↑ to contents](#содержание)

<a id="pol--poland-польша"></a>
<a id="польша"></a>
## Poland (`pol`)
<a id="eurmil--мельница-5"></a>
<a id="production-pol-eurmil"></a>
<a id="мельница--eurmil-8"></a>
### Mill — `eurmil`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |

<a id="eurpor--порт-5"></a>
<a id="production-pol-eurpor"></a>
<a id="порт--eurpor-8"></a>
### Shipyard — `eurpor`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Ship of the Line** (`battleship`) | 390.00 | 0.2 | **0.2** | 0 | 3200 | 700 | 1 | — |
| **Ferry** (`ferry`) | 56.00 | 1.1 | **1.5** | 0 | 50 | 100 | 1 | — |
| **Boat** (`fishboat`) | 40.00 | 1.5 | **2.1** | 0 | 0 | 0 | 1 | — |
| **Frigate** (`frigate`) | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| **Galley** (`galley`) | 50.00 | 1.2 | **1.7** | 0 | 900 | 800 | 1 | — |
| **Yacht** (`yacht`) | 48.00 | 1.2 | **1.8** | 0 | 450 | 150 | 1 | — |

<a id="polart--артиллерийское-депо"></a>
<a id="production-pol-polart"></a>
<a id="артиллерийское-депо--polart"></a>
### Artillery Depot — `polart`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Cannon** (`cannon`) | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| **Howitzer** (`howitzer`) | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| **Bombard** (`mortar`) | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| **Multi-barrelled Cannon** (`multicannon`) | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

<a id="polba2--казарма-18в"></a>
<a id="production-pol-polba2"></a>
<a id="казарма-18в--polba2"></a>
### Barracks, 18th century — `polba2`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Drummer, 18th century** (`drummer18`) | 6.00 | 10.0 | **14.0** | 50 | 30 | 0 | 1 | — |
| **Grenadier** (`grenadier`) | 6.00 | 10.0 | **14.0** | 80 | 60 | 40 | 1 | 36 |
| **Musketeer, 18th century** (`musketeer18`) | 4.50 | 13.3 | **18.7** | 50 | 40 | 40 | 1 | — |
| **Officer, 18th century** (`officer18`) | 6.00 | 10.0 | **14.0** | 50 | 200 | 10 | 1 | — |
| **Pikeman, 18th century** (`pikeman18`) | 1.25 | 48.0 | **67.2** | 30 | 2 | 0 | 1 | — |

<a id="polbar--казарма-17в"></a>
<a id="production-pol-polbar"></a>
<a id="казарма-17в--polbar"></a>
### Barracks, 17th century — `polbar`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Drummer, 17th century** (`drummer`) | 5.00 | 12.0 | **16.8** | 60 | 20 | 0 | 1 | — |
| **Musketeer, 17th century** (`musketeerpol`) | 4.50 | 13.3 | **18.7** | 40 | 3 | 3 | 1 | — |
| **Officer, 17th century** (`officer`) | 10.00 | 6.0 | **8.4** | 50 | 150 | 30 | 1 | — |
| **Pikeman, 17th century** (`pikemanpol`) | 3.00 | 20.0 | **28.0** | 25 | 1 | 0 | 1 | — |

<a id="polcen--городской-центр"></a>
<a id="production-pol-polcen"></a>
<a id="городской-центр--polcen"></a>
### Town Hall — `polcen`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Peasant** (`peapol`) | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

<a id="poldip--дипломатический-центр"></a>
<a id="production-pol-poldip"></a>
<a id="дипломатический-центр--poldip"></a>
### Diplomatic Center — `poldip`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Archer (mercenary)** (`archerdip`) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| **Turkish archer (mercenary)** (`archerturdip`) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| **Sich Cossack (mercenary)** (`cossacksichdip`) | 2.50 | 24.0 | **33.6** | 0 | 60 | 0 | 1 | 60 |
| **Dragoon, 18th century (mercenary)** (`dragoon18dip`) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| **Grenadier (mercenary)** (`grenadierdip`) | 1.50 | 40.0 | **56.0** | 0 | 25 | 0 | 1 | 36 |
| **Light cavalry (mercenary)** (`lightcavalrydip`) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| **Light Infantryman (mercenary)** (`lightinfantrydip`) | 1.25 | 48.0 | **67.2** | 0 | 4 | 0 | 1 | — |
| **Roundshier (mercenary)** (`roundshierdip`) | 1.50 | 40.0 | **56.0** | 0 | 12 | 0 | 1 | — |

<a id="polsta--конюшня"></a>
<a id="production-pol-polsta"></a>
<a id="конюшня--polsta"></a>
### Stable — `polsta`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Cuirassier** (`cuirassier`) | 22.50 | 2.7 | **3.7** | 120 | 35 | 25 | 1 | 75 |
| **Dragoon, 17th century** (`dragoon`) | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | 60 |
| **Dragoon, 18th century** (`dragoon18`) | 22.50 | 2.7 | **3.7** | 70 | 60 | 7 | 1 | 60 |
| **Pospolite ruszenie** (`dragoonpol`) | 13.50 | 4.4 | **6.2** | 70 | 5 | 4 | 1 | 60 |
| **Hussar** (`hussar`) | 15.00 | 4.0 | **5.6** | 70 | 20 | 2 | 1 | 60 |
| **Light Reiter** (`reiterpol`) | 8.25 | 7.3 | **10.2** | 60 | 5 | 2 | 1 | 45 |
| **Winged Hussar** (`wingedhussar`) | 26.00 | 2.3 | **3.2** | 130 | 30 | 25 | 1 | 75 |

<a id="poltem--собор"></a>
<a id="production-pol-poltem"></a>
<a id="собор--poltem"></a>
### Cathedral — `poltem`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Priest** (`priest`) | 20.00 | 3.0 | **4.2** | 60 | 25 | 0 | 1 | — |

[↑ to contents](#содержание)

<a id="por--portugal-португалия"></a>
<a id="португалия"></a>
## Portugal (`por`)
<a id="eurmil--мельница-6"></a>
<a id="production-por-eurmil"></a>
<a id="мельница--eurmil-9"></a>
### Mill — `eurmil`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |

<a id="porart--артиллерийское-депо"></a>
<a id="production-por-porart"></a>
<a id="артиллерийское-депо--porart"></a>
### Artillery Depot — `porart`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Cannon** (`cannon`) | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| **Howitzer** (`howitzer`) | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| **Bombard** (`mortar`) | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| **Multi-barrelled Cannon** (`multicannon`) | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

<a id="porba2--казарма-18в"></a>
<a id="production-por-porba2"></a>
<a id="казарма-18в--porba2"></a>
### Barracks, 18th century — `porba2`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Drummer, 18th century** (`drummer18`) | 6.00 | 10.0 | **14.0** | 50 | 30 | 0 | 1 | — |
| **Grenadier** (`grenadier`) | 6.00 | 10.0 | **14.0** | 80 | 60 | 40 | 1 | 36 |
| **Volunteer** (`jagerpor`) | 2.25 | 26.7 | **37.3** | 30 | 2 | 5 | 1 | — |
| **Musketeer, 18th century** (`musketeer18`) | 4.50 | 13.3 | **18.7** | 50 | 40 | 40 | 1 | — |
| **Officer, 18th century** (`officer18`) | 6.00 | 10.0 | **14.0** | 50 | 200 | 10 | 1 | — |
| **Pikeman, 18th century** (`pikeman18`) | 1.25 | 48.0 | **67.2** | 30 | 2 | 0 | 1 | — |

<a id="porbar--казарма-17в"></a>
<a id="production-por-porbar"></a>
<a id="казарма-17в--porbar"></a>
### Barracks, 17th century — `porbar`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Drummer, 17th century** (`drummer`) | 5.00 | 12.0 | **16.8** | 60 | 20 | 0 | 1 | — |
| **Musketeer, 17th century** (`musketeer`) | 6.00 | 10.0 | **14.0** | 45 | 6 | 5 | 1 | — |
| **Officer, 17th century** (`officer`) | 10.00 | 6.0 | **8.4** | 50 | 150 | 30 | 1 | — |
| **Pikeman, 17th century** (`pikemanpor`) | 4.00 | 15.0 | **21.0** | 40 | 4 | 5 | 1 | — |

<a id="porcen--городской-центр"></a>
<a id="production-por-porcen"></a>
<a id="городской-центр--porcen"></a>
### Town Hall — `porcen`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Peasant** (`peaspa`) | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

<a id="pordip--дипломатический-центр"></a>
<a id="production-por-pordip"></a>
<a id="дипломатический-центр--pordip"></a>
### Diplomatic Center — `pordip`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Archer (mercenary)** (`archerdip`) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| **Turkish archer (mercenary)** (`archerturdip`) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| **Sich Cossack (mercenary)** (`cossacksichdip`) | 2.50 | 24.0 | **33.6** | 0 | 60 | 0 | 1 | 60 |
| **Dragoon, 18th century (mercenary)** (`dragoon18dip`) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| **Grenadier (mercenary)** (`grenadierdip`) | 1.50 | 40.0 | **56.0** | 0 | 25 | 0 | 1 | 36 |
| **Light cavalry (mercenary)** (`lightcavalrydip`) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| **Light Infantryman (mercenary)** (`lightinfantrydip`) | 1.25 | 48.0 | **67.2** | 0 | 4 | 0 | 1 | — |
| **Roundshier (mercenary)** (`roundshierdip`) | 1.50 | 40.0 | **56.0** | 0 | 12 | 0 | 1 | — |

<a id="porpor--порт"></a>
<a id="production-por-porpor"></a>
<a id="порт--porpor"></a>
### Shipyard — `porpor`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Ship of the Line** (`battleship`) | 390.00 | 0.2 | **0.2** | 0 | 3200 | 700 | 1 | — |
| **Ferry** (`ferry`) | 56.00 | 1.1 | **1.5** | 0 | 50 | 100 | 1 | — |
| **Boat** (`fishboat`) | 40.00 | 1.5 | **2.1** | 0 | 0 | 0 | 1 | — |
| **Frigate** (`frigate`) | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| **Galley** (`galley`) | 50.00 | 1.2 | **1.7** | 0 | 900 | 800 | 1 | — |
| **Yacht** (`yacht`) | 48.00 | 1.2 | **1.8** | 0 | 450 | 150 | 1 | — |

<a id="porsta--конюшня"></a>
<a id="production-por-porsta"></a>
<a id="конюшня--porsta"></a>
### Stable — `porsta`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Cuirassier** (`cuirassier`) | 22.50 | 2.7 | **3.7** | 120 | 35 | 25 | 1 | 75 |
| **Dragoon, 17th century** (`dragoon`) | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | 60 |
| **Dragoon, 18th century** (`dragoon18`) | 22.50 | 2.7 | **3.7** | 70 | 60 | 7 | 1 | 60 |
| **Hussar** (`hussar`) | 15.00 | 4.0 | **5.6** | 70 | 20 | 2 | 1 | 60 |
| **Reiter** (`reiter`) | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | 75 |

<a id="portem--собор"></a>
<a id="production-por-portem"></a>
<a id="собор--portem"></a>
### Cathedral — `portem`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Priest** (`priest`) | 20.00 | 3.0 | **4.2** | 60 | 25 | 0 | 1 | — |

[↑ to contents](#содержание)

<a id="pru--prussia-пруссия"></a>
<a id="пруссия"></a>
## Prussia (`pru`)
<a id="eurmil--мельница-7"></a>
<a id="production-pru-eurmil"></a>
<a id="мельница--eurmil-10"></a>
### Mill — `eurmil`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |

<a id="eurpor--порт-6"></a>
<a id="production-pru-eurpor"></a>
<a id="порт--eurpor-9"></a>
### Shipyard — `eurpor`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Ship of the Line** (`battleship`) | 390.00 | 0.2 | **0.2** | 0 | 3200 | 700 | 1 | — |
| **Ferry** (`ferry`) | 56.00 | 1.1 | **1.5** | 0 | 50 | 100 | 1 | — |
| **Boat** (`fishboat`) | 40.00 | 1.5 | **2.1** | 0 | 0 | 0 | 1 | — |
| **Frigate** (`frigate`) | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| **Galley** (`galley`) | 50.00 | 1.2 | **1.7** | 0 | 900 | 800 | 1 | — |
| **Yacht** (`yacht`) | 48.00 | 1.2 | **1.8** | 0 | 450 | 150 | 1 | — |

<a id="pruart--артиллерийское-депо"></a>
<a id="production-pru-pruart"></a>
<a id="артиллерийское-депо--pruart"></a>
### Artillery Depot — `pruart`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Cannon** (`cannon`) | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| **Howitzer** (`howitzer`) | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| **Bombard** (`mortar`) | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| **Multi-barrelled Cannon** (`multicannon`) | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

<a id="pruba2--казарма-18в"></a>
<a id="production-pru-pruba2"></a>
<a id="казарма-18в--pruba2"></a>
### Barracks, 18th century — `pruba2`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Drummer, 18th century** (`drummer18`) | 6.00 | 10.0 | **14.0** | 50 | 30 | 0 | 1 | — |
| **Grenadier** (`grenadier`) | 6.00 | 10.0 | **14.0** | 80 | 60 | 40 | 1 | 36 |
| **Grenadier** (`grenadierpru`) | 7.00 | 8.6 | **12.0** | 90 | 100 | 45 | 1 | 36 |
| **Musketeer, 18th century** (`musketeer18pru`) | 6.00 | 10.0 | **14.0** | 70 | 80 | 40 | 1 | — |
| **Officer, 18th century** (`officer18`) | 6.00 | 10.0 | **14.0** | 50 | 200 | 10 | 1 | — |
| **Pikeman, 18th century** (`pikeman18`) | 1.25 | 48.0 | **67.2** | 30 | 2 | 0 | 1 | — |

<a id="prubar--казарма-17в"></a>
<a id="production-pru-prubar"></a>
<a id="казарма-17в--prubar"></a>
### Barracks, 17th century — `prubar`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Drummer, 17th century** (`drummer`) | 5.00 | 12.0 | **16.8** | 60 | 20 | 0 | 1 | — |
| **Musketeer, 17th century** (`musketeer`) | 6.00 | 10.0 | **14.0** | 45 | 6 | 5 | 1 | — |
| **Officer, 17th century** (`officer`) | 10.00 | 6.0 | **8.4** | 50 | 150 | 30 | 1 | — |
| **Pikeman, 17th century** (`pikeman`) | 4.50 | 13.3 | **18.7** | 25 | 3 | 20 | 1 | — |

<a id="prucen--городской-центр"></a>
<a id="production-pru-prucen"></a>
<a id="городской-центр--prucen"></a>
### Town Hall — `prucen`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Peasant** (`peaaus`) | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

<a id="prudip--дипломатический-центр"></a>
<a id="production-pru-prudip"></a>
<a id="дипломатический-центр--prudip"></a>
### Diplomatic Center — `prudip`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Archer (mercenary)** (`archerdip`) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| **Turkish archer (mercenary)** (`archerturdip`) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| **Sich Cossack (mercenary)** (`cossacksichdip`) | 2.50 | 24.0 | **33.6** | 0 | 60 | 0 | 1 | 60 |
| **Dragoon, 18th century (mercenary)** (`dragoon18dip`) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| **Grenadier (mercenary)** (`grenadierdip`) | 1.50 | 40.0 | **56.0** | 0 | 25 | 0 | 1 | 36 |
| **Light cavalry (mercenary)** (`lightcavalrydip`) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| **Light Infantryman (mercenary)** (`lightinfantrydip`) | 1.25 | 48.0 | **67.2** | 0 | 4 | 0 | 1 | — |
| **Roundshier (mercenary)** (`roundshierdip`) | 1.50 | 40.0 | **56.0** | 0 | 12 | 0 | 1 | — |

<a id="prusta--конюшня"></a>
<a id="production-pru-prusta"></a>
<a id="конюшня--prusta"></a>
### Stable — `prusta`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Cuirassier** (`cuirassier`) | 22.50 | 2.7 | **3.7** | 120 | 35 | 25 | 1 | 75 |
| **Dragoon, 17th century** (`dragoon`) | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | 60 |
| **Dragoon, 18th century** (`dragoon18`) | 22.50 | 2.7 | **3.7** | 70 | 60 | 7 | 1 | 60 |
| **Hussar** (`hussarpru`) | 11.25 | 5.3 | **7.5** | 80 | 15 | 2 | 1 | 60 |
| **Reiter** (`reiter`) | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | 75 |

<a id="prutem--собор"></a>
<a id="production-pru-prutem"></a>
<a id="собор--prutem"></a>
### Cathedral — `prutem`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Priest** (`priest`) | 20.00 | 3.0 | **4.2** | 60 | 25 | 0 | 1 | — |

[↑ to contents](#содержание)

<a id="rus--russia-россия"></a>
<a id="россия"></a>
## Russia (`rus`)
<a id="rusart--артиллерийское-депо"></a>
<a id="production-rus-rusart"></a>
<a id="артиллерийское-депо--rusart"></a>
### Artillery Depot — `rusart`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Cannon** (`cannon`) | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| **Howitzer** (`howitzer`) | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| **Bombard** (`mortar`) | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| **Multi-barrelled Cannon** (`multicannon`) | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

<a id="rusba2--казарма-18в"></a>
<a id="production-rus-rusba2"></a>
<a id="казарма-18в--rusba2"></a>
### Barracks, 18th century — `rusba2`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Drummer, 18th century** (`drummer18`) | 6.00 | 10.0 | **14.0** | 90 | 15 | 0 | 1 | — |
| **Grenadier** (`grenadier`) | 6.00 | 10.0 | **14.0** | 80 | 60 | 40 | 1 | 36 |
| **Musketeer, 18th century** (`musketeer18`) | 4.50 | 13.3 | **18.7** | 50 | 40 | 40 | 1 | — |
| **Officer, 18th century** (`officer18`) | 6.00 | 10.0 | **14.0** | 50 | 200 | 10 | 1 | — |
| **Pikeman, 18th century** (`pikeman18`) | 1.25 | 48.0 | **67.2** | 30 | 2 | 0 | 1 | — |

<a id="rusbar--стрелецкая-казарма"></a>
<a id="production-rus-rusbar"></a>
<a id="стрелецкая-казарма--rusbar"></a>
### Strelets Barracks — `rusbar`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Drummer, 17th century** (`drummerrus`) | 6.00 | 10.0 | **14.0** | 90 | 15 | 0 | 1 | — |
| **Commander** (`officerrus`) | 12.50 | 4.8 | **6.7** | 100 | 125 | 5 | 1 | — |
| **Spearman** (`pikemanrus`) | 5.50 | 10.9 | **15.3** | 45 | 4 | 15 | 1 | — |
| **Strelets** (`strelet`) | 8.50 | 7.1 | **9.9** | 70 | 7 | 9 | 1 | — |

<a id="ruscen--городской-центр"></a>
<a id="production-rus-ruscen"></a>
<a id="городской-центр--ruscen"></a>
### Town Hall — `ruscen`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Serf** (`pearus`) | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 26 |

<a id="rusdip--дипломатический-центр"></a>
<a id="production-rus-rusdip"></a>
<a id="дипломатический-центр--rusdip"></a>
### Diplomatic Center — `rusdip`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Archer (mercenary)** (`archerdip`) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| **Turkish archer (mercenary)** (`archerturdip`) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| **Sich Cossack (mercenary)** (`cossacksichdip`) | 2.50 | 24.0 | **33.6** | 0 | 60 | 0 | 1 | 60 |
| **Dragoon, 18th century (mercenary)** (`dragoon18dip`) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| **Grenadier (mercenary)** (`grenadierdip`) | 1.50 | 40.0 | **56.0** | 0 | 25 | 0 | 1 | 36 |
| **Light cavalry (mercenary)** (`lightcavalrydip`) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| **Light Infantryman (mercenary)** (`lightinfantrydip`) | 1.25 | 48.0 | **67.2** | 0 | 4 | 0 | 1 | — |
| **Roundshier (mercenary)** (`roundshierdip`) | 1.50 | 40.0 | **56.0** | 0 | 12 | 0 | 1 | — |

<a id="rusmil--мельница"></a>
<a id="production-rus-rusmil"></a>
<a id="мельница--rusmil"></a>
### Mill — `rusmil`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |

<a id="ruspor--порт"></a>
<a id="production-rus-ruspor"></a>
<a id="порт--ruspor"></a>
### Shipyard — `ruspor`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Ship of the Line** (`battleship`) | 390.00 | 0.2 | **0.2** | 0 | 3200 | 700 | 1 | — |
| **Ferry** (`ferry`) | 56.00 | 1.1 | **1.5** | 0 | 50 | 100 | 1 | — |
| **Boat** (`fishboat`) | 40.00 | 1.5 | **2.1** | 0 | 0 | 0 | 1 | — |
| **Frigate** (`frigate`) | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| **Galley** (`galley`) | 50.00 | 1.2 | **1.7** | 0 | 900 | 800 | 1 | — |
| **Yacht** (`yacht`) | 48.00 | 1.2 | **1.8** | 0 | 450 | 150 | 1 | — |

<a id="russta--конюшня"></a>
<a id="production-rus-russta"></a>
<a id="конюшня--russta"></a>
### Stable — `russta`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Don Cossack** (`cossackdon`) | 13.50 | 4.4 | **6.2** | 100 | 0 | 0 | 1 | 60 |
| **Cuirassier** (`cuirassier`) | 22.50 | 2.7 | **3.7** | 120 | 35 | 25 | 1 | 75 |
| **Dragoon, 18th century** (`dragoon18`) | 22.50 | 2.7 | **3.7** | 70 | 60 | 7 | 1 | 60 |
| **Hussar** (`hussar`) | 15.00 | 4.0 | **5.6** | 70 | 20 | 2 | 1 | 60 |
| **Vityaz** (`vityaz`) | 25.50 | 2.4 | **3.3** | 160 | 13 | 25 | 1 | 75 |

<a id="rustem--православная-церковь"></a>
<a id="production-rus-rustem"></a>
<a id="православная-церковь--rustem"></a>
### Orthodox Cathedral — `rustem`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Pope** (`pope`) | 20.00 | 3.0 | **4.2** | 40 | 20 | 0 | 1 | — |

[↑ to contents](#содержание)

<a id="sax--saxony-саксония"></a>
<a id="саксония"></a>
## Saxony (`sax`)
<a id="eurmil--мельница-8"></a>
<a id="production-sax-eurmil"></a>
<a id="мельница--eurmil-11"></a>
### Mill — `eurmil`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |

<a id="eurpor--порт-7"></a>
<a id="production-sax-eurpor"></a>
<a id="порт--eurpor-10"></a>
### Shipyard — `eurpor`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Ship of the Line** (`battleship`) | 390.00 | 0.2 | **0.2** | 0 | 3200 | 700 | 1 | — |
| **Ferry** (`ferry`) | 56.00 | 1.1 | **1.5** | 0 | 50 | 100 | 1 | — |
| **Boat** (`fishboat`) | 40.00 | 1.5 | **2.1** | 0 | 0 | 0 | 1 | — |
| **Frigate** (`frigate`) | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| **Galley** (`galley`) | 50.00 | 1.2 | **1.7** | 0 | 900 | 800 | 1 | — |
| **Yacht** (`yacht`) | 48.00 | 1.2 | **1.8** | 0 | 450 | 150 | 1 | — |

<a id="saxart--артиллерийское-депо"></a>
<a id="production-sax-saxart"></a>
<a id="артиллерийское-депо--saxart"></a>
### Artillery Depot — `saxart`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Cannon** (`cannon`) | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| **Howitzer** (`howitzer`) | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| **Bombard** (`mortar`) | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| **Multi-barrelled Cannon** (`multicannon`) | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

<a id="saxba2--казарма-18в"></a>
<a id="production-sax-saxba2"></a>
<a id="казарма-18в--saxba2"></a>
### Barracks, 18th century — `saxba2`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Drummer, 18th century** (`drummer18`) | 6.00 | 10.0 | **14.0** | 50 | 30 | 0 | 1 | — |
| **Grenadier** (`grenadiersax`) | 6.00 | 10.0 | **14.0** | 50 | 60 | 40 | 1 | 30 |
| **Musketeer, 18th century** (`musketeer18sax`) | 4.50 | 13.3 | **18.7** | 40 | 45 | 40 | 1 | — |
| **Officer, 18th century** (`officer18`) | 6.00 | 10.0 | **14.0** | 50 | 200 | 10 | 1 | — |
| **Pikeman, 18th century** (`pikeman18`) | 1.25 | 48.0 | **67.2** | 30 | 2 | 0 | 1 | — |

<a id="saxbar--казарма-17в"></a>
<a id="production-sax-saxbar"></a>
<a id="казарма-17в--saxbar"></a>
### Barracks, 17th century — `saxbar`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Drummer, 17th century** (`drummer`) | 5.00 | 12.0 | **16.8** | 60 | 20 | 0 | 1 | — |
| **Musketeer, 17th century** (`musketeer`) | 6.00 | 10.0 | **14.0** | 45 | 6 | 5 | 1 | — |
| **Officer, 17th century** (`officer`) | 10.00 | 6.0 | **8.4** | 50 | 150 | 30 | 1 | — |
| **Pikeman, 17th century** (`pikeman`) | 4.50 | 13.3 | **18.7** | 25 | 3 | 20 | 1 | — |

<a id="saxcen--городской-центр"></a>
<a id="production-sax-saxcen"></a>
<a id="городской-центр--saxcen"></a>
### Town Hall — `saxcen`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Peasant** (`peaaus`) | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

<a id="saxdip--дипломатический-центр"></a>
<a id="production-sax-saxdip"></a>
<a id="дипломатический-центр--saxdip"></a>
### Diplomatic Center — `saxdip`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Archer (mercenary)** (`archerdip`) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| **Turkish archer (mercenary)** (`archerturdip`) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| **Sich Cossack (mercenary)** (`cossacksichdip`) | 2.50 | 24.0 | **33.6** | 0 | 60 | 0 | 1 | 60 |
| **Dragoon, 18th century (mercenary)** (`dragoon18dip`) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| **Grenadier (mercenary)** (`grenadierdip`) | 1.50 | 40.0 | **56.0** | 0 | 25 | 0 | 1 | 36 |
| **Light cavalry (mercenary)** (`lightcavalrydip`) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| **Light Infantryman (mercenary)** (`lightinfantrydip`) | 1.25 | 48.0 | **67.2** | 0 | 4 | 0 | 1 | — |
| **Roundshier (mercenary)** (`roundshierdip`) | 1.50 | 40.0 | **56.0** | 0 | 12 | 0 | 1 | — |

<a id="saxsta--конюшня"></a>
<a id="production-sax-saxsta"></a>
<a id="конюшня--saxsta"></a>
### Stable — `saxsta`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Cuirassier** (`cuirassier`) | 22.50 | 2.7 | **3.7** | 120 | 35 | 25 | 1 | 75 |
| **Dragoon, 17th century** (`dragoon`) | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | 60 |
| **Dragoon, 18th century** (`dragoon18`) | 22.50 | 2.7 | **3.7** | 70 | 60 | 7 | 1 | 60 |
| **Cavalry Guard** (`guardcavalrysax`) | 24.00 | 2.5 | **3.5** | 140 | 50 | 20 | 1 | 75 |
| **Hussar** (`hussar`) | 15.00 | 4.0 | **5.6** | 70 | 20 | 2 | 1 | 60 |
| **Reiter** (`reiter`) | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | 75 |

<a id="saxtem--собор"></a>
<a id="production-sax-saxtem"></a>
<a id="собор--saxtem"></a>
### Cathedral — `saxtem`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Priest** (`priest`) | 20.00 | 3.0 | **4.2** | 60 | 25 | 0 | 1 | — |

[↑ to contents](#содержание)

<a id="sco--scotland-шотландия"></a>
<a id="шотландия"></a>
## Scotland (`sco`)
<a id="eurmil--мельница-9"></a>
<a id="production-sco-eurmil"></a>
<a id="мельница--eurmil-12"></a>
### Mill — `eurmil`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |

<a id="eurpor--порт-8"></a>
<a id="production-sco-eurpor"></a>
<a id="порт--eurpor-11"></a>
### Shipyard — `eurpor`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Ship of the Line** (`battleship`) | 390.00 | 0.2 | **0.2** | 0 | 3200 | 700 | 1 | — |
| **Ferry** (`ferry`) | 56.00 | 1.1 | **1.5** | 0 | 50 | 100 | 1 | — |
| **Boat** (`fishboat`) | 40.00 | 1.5 | **2.1** | 0 | 0 | 0 | 1 | — |
| **Frigate** (`frigate`) | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| **Yacht** (`yacht`) | 48.00 | 1.2 | **1.8** | 0 | 450 | 150 | 1 | — |

<a id="scoart--артиллерийское-депо"></a>
<a id="production-sco-scoart"></a>
<a id="артиллерийское-депо--scoart"></a>
### Artillery Depot — `scoart`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Cannon** (`cannon`) | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| **Frame gun** (`framegun`) | 50.00 | 1.2 | **1.7** | 0 | 300 | 150 | 1 | — |
| **Howitzer** (`howitzer`) | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| **Bombard** (`mortar`) | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |

<a id="scoba2--замок"></a>
<a id="production-sco-scoba2"></a>
<a id="замок--scoba2"></a>
### Castle — `scoba2`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Bow Clansman** (`archersco`) | 6.00 | 10.0 | **14.0** | 80 | 7 | 0 | 1 | 39 |
| **Sword Clansman** (`swordsmansco`) | 7.00 | 8.6 | **12.0** | 110 | 10 | 0 | 1 | 45 |

<a id="scobar--казарма-17в"></a>
<a id="production-sco-scobar"></a>
<a id="казарма-17в--scobar"></a>
### Barracks, 17th century — `scobar`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Bagpiper** (`bagpiper`) | 7.00 | 8.6 | **12.0** | 120 | 20 | 0 | 1 | — |
| **Covenanter musketeer** (`musketeersco`) | 7.00 | 8.6 | **12.0** | 55 | 8 | 7 | 1 | — |
| **Officer** (`officersco`) | 10.00 | 6.0 | **8.4** | 130 | 130 | 10 | 1 | — |
| **Covenanter pikeman** (`pikemansco`) | 4.00 | 15.0 | **21.0** | 35 | 2 | 0 | 1 | — |

<a id="scocen--городской-центр"></a>
<a id="production-sco-scocen"></a>
<a id="городской-центр--scocen"></a>
### Town Hall — `scocen`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Peasant** (`peasco`) | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

<a id="scodip--дипломатический-центр"></a>
<a id="production-sco-scodip"></a>
<a id="дипломатический-центр--scodip"></a>
### Diplomatic Center — `scodip`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Archer (mercenary)** (`archerdip`) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | 39 |
| **Turkish archer (mercenary)** (`archerturdip`) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | 39 |
| **Sich Cossack (mercenary)** (`cossacksichdip`) | 2.50 | 24.0 | **33.6** | 0 | 60 | 0 | 1 | 60 |
| **Dragoon, 18th century (mercenary)** (`dragoon18dip`) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| **Grenadier (mercenary)** (`grenadierdip`) | 1.50 | 40.0 | **56.0** | 0 | 25 | 0 | 1 | 36 |
| **Light cavalry (mercenary)** (`lightcavalrydip`) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| **Light Infantryman (mercenary)** (`lightinfantrydip`) | 1.25 | 48.0 | **67.2** | 0 | 4 | 0 | 1 | — |
| **Roundshier (mercenary)** (`roundshierdip`) | 1.50 | 40.0 | **56.0** | 0 | 12 | 0 | 1 | 45 |

<a id="scosta--конюшня"></a>
<a id="production-sco-scosta"></a>
<a id="конюшня--scosta"></a>
### Stable — `scosta`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Lancer** (`lancersco`) | 21.00 | 2.9 | **4.0** | 120 | 6 | 0 | 1 | 60 |
| **Raider** (`raidersco`) | 22.50 | 2.7 | **3.7** | 130 | 8 | 2 | 1 | 75 |

<a id="scotem--собор"></a>
<a id="production-sco-scotem"></a>
<a id="собор--scotem"></a>
### Cathedral — `scotem`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Priest** (`priest`) | 20.00 | 3.0 | **4.2** | 60 | 25 | 0 | 1 | — |

[↑ to contents](#содержание)

<a id="spa--spain-испания"></a>
<a id="испания"></a>
## Spain (`spa`)
<a id="eurmil--мельница-10"></a>
<a id="production-spa-eurmil"></a>
<a id="мельница--eurmil-13"></a>
### Mill — `eurmil`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |

<a id="eurpor--порт-9"></a>
<a id="production-spa-eurpor"></a>
<a id="порт--eurpor-12"></a>
### Shipyard — `eurpor`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Ship of the Line** (`battleship`) | 390.00 | 0.2 | **0.2** | 0 | 3200 | 700 | 1 | — |
| **Ferry** (`ferry`) | 56.00 | 1.1 | **1.5** | 0 | 50 | 100 | 1 | — |
| **Boat** (`fishboat`) | 40.00 | 1.5 | **2.1** | 0 | 0 | 0 | 1 | — |
| **Frigate** (`frigate`) | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| **Galley** (`galley`) | 50.00 | 1.2 | **1.7** | 0 | 900 | 800 | 1 | — |
| **Yacht** (`yacht`) | 48.00 | 1.2 | **1.8** | 0 | 450 | 150 | 1 | — |

<a id="spaart--артиллерийское-депо"></a>
<a id="production-spa-spaart"></a>
<a id="артиллерийское-депо--spaart"></a>
### Artillery Depot — `spaart`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Cannon** (`cannon`) | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| **Howitzer** (`howitzer`) | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| **Bombard** (`mortar`) | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| **Multi-barrelled Cannon** (`multicannon`) | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

<a id="spaba2--казарма-18в"></a>
<a id="production-spa-spaba2"></a>
<a id="казарма-18в--spaba2"></a>
### Barracks, 18th century — `spaba2`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Drummer, 18th century** (`drummer18`) | 6.00 | 10.0 | **14.0** | 50 | 30 | 0 | 1 | — |
| **Grenadier** (`grenadier`) | 6.00 | 10.0 | **14.0** | 80 | 60 | 40 | 1 | 36 |
| **Musketeer, 18th century** (`musketeer18`) | 4.50 | 13.3 | **18.7** | 50 | 40 | 40 | 1 | — |
| **Officer, 18th century** (`officer18`) | 6.00 | 10.0 | **14.0** | 50 | 200 | 10 | 1 | — |
| **Pikeman, 18th century** (`pikeman18`) | 1.25 | 48.0 | **67.2** | 30 | 2 | 0 | 1 | — |

<a id="spabar--казарма-17в"></a>
<a id="production-spa-spabar"></a>
<a id="казарма-17в--spabar"></a>
### Barracks, 17th century — `spabar`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Drummer, 17th century** (`drummer`) | 5.00 | 12.0 | **16.8** | 60 | 20 | 0 | 1 | — |
| **Musketeer, 17th century** (`musketeerspa`) | 7.50 | 8.0 | **11.2** | 40 | 12 | 20 | 1 | — |
| **Officer, 17th century** (`officer`) | 10.00 | 6.0 | **8.4** | 50 | 150 | 30 | 1 | — |
| **Pikeman, 17th century** (`pikeman`) | 5.50 | 10.9 | **15.3** | 35 | 7 | 30 | 1 | — |
| **Coselete** (`pikemanspa`) | 5.50 | 10.9 | **15.3** | 35 | 7 | 30 | 1 | — |

<a id="spacen--городской-центр"></a>
<a id="production-spa-spacen"></a>
<a id="городской-центр--spacen"></a>
### Town Hall — `spacen`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Peasant** (`peaspa`) | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

<a id="spadip--дипломатический-центр"></a>
<a id="production-spa-spadip"></a>
<a id="дипломатический-центр--spadip"></a>
### Diplomatic Center — `spadip`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Archer (mercenary)** (`archerdip`) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| **Turkish archer (mercenary)** (`archerturdip`) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| **Sich Cossack (mercenary)** (`cossacksichdip`) | 2.50 | 24.0 | **33.6** | 0 | 60 | 0 | 1 | 60 |
| **Dragoon, 18th century (mercenary)** (`dragoon18dip`) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| **Grenadier (mercenary)** (`grenadierdip`) | 1.50 | 40.0 | **56.0** | 0 | 25 | 0 | 1 | 36 |
| **Light cavalry (mercenary)** (`lightcavalrydip`) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| **Light Infantryman (mercenary)** (`lightinfantrydip`) | 1.25 | 48.0 | **67.2** | 0 | 4 | 0 | 1 | — |
| **Roundshier (mercenary)** (`roundshierdip`) | 1.50 | 40.0 | **56.0** | 0 | 12 | 0 | 1 | — |

<a id="spasta--конюшня"></a>
<a id="production-spa-spasta"></a>
<a id="конюшня--spasta"></a>
### Stable — `spasta`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Cuirassier** (`cuirassier`) | 22.50 | 2.7 | **3.7** | 120 | 35 | 25 | 1 | 75 |
| **Dragoon, 17th century** (`dragoon`) | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | 60 |
| **Dragoon, 18th century** (`dragoon18`) | 22.50 | 2.7 | **3.7** | 70 | 60 | 7 | 1 | 60 |
| **Hussar** (`hussar`) | 15.00 | 4.0 | **5.6** | 70 | 20 | 2 | 1 | 60 |
| **Reiter** (`reiter`) | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | 75 |

<a id="spatem--собор"></a>
<a id="production-spa-spatem"></a>
<a id="собор--spatem"></a>
### Cathedral — `spatem`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Priest** (`priest`) | 20.00 | 3.0 | **4.2** | 60 | 25 | 0 | 1 | — |

[↑ to contents](#содержание)

<a id="swe--sweden-швеция"></a>
<a id="швеция"></a>
## Sweden (`swe`)
<a id="production-swe-eurmil"></a>
<a id="мельница--eurmil-14"></a>
### Mill — `eurmil`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |

<a id="production-swe-eurpor"></a>
<a id="порт--eurpor-13"></a>
### Shipyard — `eurpor`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Ship of the Line** (`battleship`) | 390.00 | 0.2 | **0.2** | 0 | 3200 | 700 | 1 | — |
| **Ferry** (`ferry`) | 56.00 | 1.1 | **1.5** | 0 | 50 | 100 | 1 | — |
| **Boat** (`fishboat`) | 40.00 | 1.5 | **2.1** | 0 | 0 | 0 | 1 | — |
| **Frigate** (`frigate`) | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| **Galley** (`galley`) | 50.00 | 1.2 | **1.7** | 0 | 900 | 800 | 1 | — |
| **Yacht** (`yacht`) | 48.00 | 1.2 | **1.8** | 0 | 450 | 150 | 1 | — |
<a id="sweart--артиллерийское-депо"></a>
<a id="production-swe-sweart"></a>
<a id="артиллерийское-депо--sweart"></a>
### Artillery Depot — `sweart`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Cannon** (`cannon`) | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| **Howitzer** (`howitzer`) | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| **Bombard** (`mortar`) | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| **Multi-barrelled Cannon** (`multicannon`) | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

<a id="sweba2--казарма-18в"></a>
<a id="production-swe-sweba2"></a>
<a id="казарма-18в--sweba2"></a>
### Barracks, 18th century — `sweba2`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Drummer, 18th century** (`drummer18`) | 6.00 | 10.0 | **14.0** | 50 | 30 | 0 | 1 | — |
| **Grenadier** (`grenadier`) | 6.00 | 10.0 | **14.0** | 80 | 60 | 40 | 1 | 36 |
| **Musketeer, 18th century** (`musketeer18`) | 4.50 | 13.3 | **18.7** | 50 | 40 | 40 | 1 | — |
| **Officer, 18th century** (`officer18`) | 6.00 | 10.0 | **14.0** | 50 | 200 | 10 | 1 | — |
| **Pikeman, 18th century** (`pikeman18swe`) | 1.50 | 40.0 | **56.0** | 40 | 3 | 0 | 1 | — |

<a id="swebar--казарма-17в"></a>
<a id="production-swe-swebar"></a>
<a id="казарма-17в--swebar"></a>
### Barracks, 17th century — `swebar`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Drummer, 17th century** (`drummer`) | 5.00 | 12.0 | **16.8** | 60 | 20 | 0 | 1 | — |
| **Musketeer, 17th century** (`musketeer`) | 6.00 | 10.0 | **14.0** | 45 | 6 | 5 | 1 | — |
| **Officer, 17th century** (`officer`) | 10.00 | 6.0 | **8.4** | 50 | 150 | 30 | 1 | — |
| **Pikeman, 17th century** (`pikeman`) | 4.50 | 13.3 | **18.7** | 25 | 3 | 20 | 1 | — |

<a id="swecen--городской-центр"></a>
<a id="production-swe-swecen"></a>
<a id="городской-центр--swecen"></a>
### Town Hall — `swecen`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Peasant** (`peaeng`) | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

<a id="swedip--дипломатический-центр"></a>
<a id="production-swe-swedip"></a>
<a id="дипломатический-центр--swedip"></a>
### Diplomatic Center — `swedip`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Archer (mercenary)** (`archerdip`) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| **Turkish archer (mercenary)** (`archerturdip`) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| **Sich Cossack (mercenary)** (`cossacksichdip`) | 2.50 | 24.0 | **33.6** | 0 | 60 | 0 | 1 | 60 |
| **Dragoon, 18th century (mercenary)** (`dragoon18dip`) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| **Grenadier (mercenary)** (`grenadierdip`) | 1.50 | 40.0 | **56.0** | 0 | 25 | 0 | 1 | 36 |
| **Light cavalry (mercenary)** (`lightcavalrydip`) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| **Light Infantryman (mercenary)** (`lightinfantrydip`) | 1.25 | 48.0 | **67.2** | 0 | 4 | 0 | 1 | — |
| **Roundshier (mercenary)** (`roundshierdip`) | 1.50 | 40.0 | **56.0** | 0 | 12 | 0 | 1 | — |

<a id="swesta--конюшня"></a>
<a id="production-swe-swesta"></a>
<a id="конюшня--swesta"></a>
### Stable — `swesta`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Cuirassier** (`cuirassier`) | 22.50 | 2.7 | **3.7** | 120 | 35 | 25 | 1 | 75 |
| **Dragoon, 17th century** (`dragoon`) | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | 60 |
| **Dragoon, 18th century** (`dragoon18`) | 22.50 | 2.7 | **3.7** | 70 | 60 | 7 | 1 | 60 |
| **Hakkapeliitta** (`hackapell`) | 18.00 | 3.3 | **4.7** | 80 | 7 | 2 | 1 | 60 |
| **Hussar** (`hussar`) | 15.00 | 4.0 | **5.6** | 70 | 20 | 2 | 1 | 60 |
| **Swedish Reiter** (`reiterswe`) | 22.50 | 2.7 | **3.7** | 130 | 7 | 20 | 1 | 75 |

<a id="swetem--собор"></a>
<a id="production-swe-swetem"></a>
<a id="собор--swetem"></a>
### Cathedral — `swetem`
| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Priest** (`priest`) | 20.00 | 3.0 | **4.2** | 60 | 25 | 0 | 1 | — |

[↑ to contents](#содержание)

<a id="swi--switzerland-швейцария"></a>
<a id="швейцария"></a>
## Switzerland (`swi`)
<a id="eurmil--мельница-11"></a>
<a id="production-swi-eurmil"></a>
<a id="мельница--eurmil-15"></a>
### Mill — `eurmil`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |

<a id="eurpor--порт-10"></a>
<a id="production-swi-eurpor"></a>
<a id="порт--eurpor-14"></a>
### Shipyard — `eurpor`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Ship of the Line** (`battleship`) | 390.00 | 0.2 | **0.2** | 0 | 3200 | 700 | 1 | — |
| **Ferry** (`ferry`) | 56.00 | 1.1 | **1.5** | 0 | 50 | 100 | 1 | — |
| **Boat** (`fishboat`) | 40.00 | 1.5 | **2.1** | 0 | 0 | 0 | 1 | — |
| **Frigate** (`frigate`) | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| **Galley** (`galley`) | 50.00 | 1.2 | **1.7** | 0 | 900 | 800 | 1 | — |
| **Yacht** (`yacht`) | 48.00 | 1.2 | **1.8** | 0 | 450 | 150 | 1 | — |

<a id="swiart--артиллерийское-депо"></a>
<a id="production-swi-swiart"></a>
<a id="артиллерийское-депо--swiart"></a>
### Artillery Depot — `swiart`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Cannon** (`cannon`) | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| **Howitzer** (`howitzer`) | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| **Bombard** (`mortar`) | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| **Multi-barrelled Cannon** (`multicannon`) | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

<a id="swiba2--казарма-18в"></a>
<a id="production-swi-swiba2"></a>
<a id="казарма-18в--swiba2"></a>
### Barracks, 18th century — `swiba2`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Drummer, 18th century** (`drummer18`) | 6.00 | 10.0 | **14.0** | 50 | 30 | 0 | 1 | — |
| **Grenadier** (`grenadier`) | 6.00 | 10.0 | **14.0** | 80 | 60 | 40 | 1 | 36 |
| **Jaeger** (`jagerswi`) | 8.50 | 7.1 | **9.9** | 40 | 70 | 20 | 1 | — |
| **Musketeer, 18th century** (`musketeer18`) | 4.50 | 13.3 | **18.7** | 50 | 40 | 40 | 1 | — |
| **Officer, 18th century** (`officer18`) | 6.00 | 10.0 | **14.0** | 50 | 200 | 10 | 1 | — |
| **Pikeman, 18th century** (`pikeman18`) | 1.25 | 48.0 | **67.2** | 30 | 2 | 0 | 1 | — |

<a id="swibar--казарма-17в"></a>
<a id="production-swi-swibar"></a>
<a id="казарма-17в--swibar"></a>
### Barracks, 17th century — `swibar`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Drummer, 17th century** (`drummer`) | 5.00 | 12.0 | **16.8** | 60 | 20 | 0 | 1 | — |
| **Musketeer, 17th century** (`musketeer`) | 6.00 | 10.0 | **14.0** | 45 | 6 | 5 | 1 | — |
| **Officer, 17th century** (`officer`) | 10.00 | 6.0 | **8.4** | 50 | 150 | 30 | 1 | — |
| **Pikeman, 17th century** (`pikemanswi`) | 5.00 | 12.0 | **16.8** | 40 | 6 | 20 | 1 | — |

<a id="swicen--городской-центр"></a>
<a id="production-swi-swicen"></a>
<a id="городской-центр--swicen"></a>
### Town Hall — `swicen`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Peasant** (`peaaus`) | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

<a id="swidip--дипломатический-центр"></a>
<a id="production-swi-swidip"></a>
<a id="дипломатический-центр--swidip"></a>
### Diplomatic Center — `swidip`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Archer (mercenary)** (`archerdip`) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| **Turkish archer (mercenary)** (`archerturdip`) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| **Sich Cossack (mercenary)** (`cossacksichdip`) | 2.50 | 24.0 | **33.6** | 0 | 60 | 0 | 1 | 60 |
| **Dragoon, 18th century (mercenary)** (`dragoon18dip`) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| **Grenadier (mercenary)** (`grenadierdip`) | 1.50 | 40.0 | **56.0** | 0 | 25 | 0 | 1 | 36 |
| **Light cavalry (mercenary)** (`lightcavalrydip`) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| **Light Infantryman (mercenary)** (`lightinfantrydip`) | 1.25 | 48.0 | **67.2** | 0 | 4 | 0 | 1 | — |
| **Roundshier (mercenary)** (`roundshierdip`) | 1.50 | 40.0 | **56.0** | 0 | 12 | 0 | 1 | — |

<a id="swista--конюшня"></a>
<a id="production-swi-swista"></a>
<a id="конюшня--swista"></a>
### Stable — `swista`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Cuirassier** (`cuirassier`) | 22.50 | 2.7 | **3.7** | 120 | 35 | 25 | 1 | 75 |
| **Dragoon, 17th century** (`dragoon`) | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | 60 |
| **Dragoon, 18th century** (`dragoon18`) | 22.50 | 2.7 | **3.7** | 70 | 60 | 7 | 1 | 60 |
| **Mounted Jaeger** (`hussarswi`) | 19.50 | 3.1 | **4.3** | 120 | 30 | 2 | 1 | 60 |
| **Reiter** (`reiter`) | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | 75 |

<a id="switem--собор"></a>
<a id="production-swi-switem"></a>
<a id="собор--switem"></a>
### Cathedral — `switem`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Priest** (`priest`) | 20.00 | 3.0 | **4.2** | 60 | 25 | 0 | 1 | — |

[↑ to contents](#содержание)

<a id="tur--turkey-турция"></a>
<a id="турция"></a>
## Turkey (`tur`)
<a id="turart--артиллерийское-депо"></a>
<a id="production-tur-turart"></a>
<a id="артиллерийское-депо--turart"></a>
### Artillery Depot — `turart`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Cannon** (`cannon`) | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| **Howitzer** (`howitzer`) | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| **Bombard** (`mortar`) | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |

<a id="turbar--казарма"></a>
<a id="production-tur-turbar"></a>
<a id="казарма--turbar"></a>
### Barracks — `turbar`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Turkish archer** (`archertur`) | 3.00 | 20.0 | **28.0** | 45 | 4 | 0 | 1 | — |
| **Drummer, 17th century** (`drummertur`) | 4.00 | 15.0 | **21.0** | 30 | 15 | 0 | 1 | — |
| **Janissary** (`jannisary`) | 8.00 | 7.5 | **10.5** | 55 | 13 | 5 | 1 | — |
| **Light Infantryman** (`lightinfantry`) | 1.00 | 60.0 | **84.0** | 25 | 0 | 1 | 1 | — |
| **Officer** (`officertur`) | 7.50 | 8.0 | **11.2** | 50 | 100 | 0 | 1 | — |
| **Ottoman Pikeman** (`pikemantur`) | 5.50 | 10.9 | **15.3** | 55 | 5 | 0 | 1 | — |

<a id="turcen--городской-центр"></a>
<a id="production-tur-turcen"></a>
<a id="городской-центр--turcen"></a>
### Town Hall — `turcen`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Peasant** (`peatur`) | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 28 |

<a id="turdip--дипломатический-центр"></a>
<a id="production-tur-turdip"></a>
<a id="дипломатический-центр--turdip"></a>
### Diplomatic Center — `turdip`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Archer (mercenary)** (`archerdip`) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| **Turkish archer (mercenary)** (`archerturdip`) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| **Sich Cossack (mercenary)** (`cossacksichdip`) | 2.50 | 24.0 | **33.6** | 0 | 60 | 0 | 1 | 60 |
| **Dragoon, 18th century (mercenary)** (`dragoon18dip`) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| **Grenadier (mercenary)** (`grenadierdip`) | 1.50 | 40.0 | **56.0** | 0 | 25 | 0 | 1 | 36 |
| **Light cavalry (mercenary)** (`lightcavalrydip`) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| **Light Infantryman (mercenary)** (`lightinfantrydip`) | 1.25 | 48.0 | **67.2** | 0 | 4 | 0 | 1 | — |
| **Roundshier (mercenary)** (`roundshierdip`) | 1.50 | 40.0 | **56.0** | 0 | 12 | 0 | 1 | — |

<a id="turmil--мельница"></a>
<a id="production-tur-turmil"></a>
<a id="мельница--turmil-1"></a>
### Mill — `turmil`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |

<a id="turpor--порт"></a>
<a id="production-tur-turpor"></a>
<a id="порт--turpor-1"></a>
### Shipyard — `turpor`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Ship of the Line** (`battleship`) | 390.00 | 0.2 | **0.2** | 0 | 3200 | 700 | 1 | — |
| **Ferry** (`ferry`) | 56.00 | 1.1 | **1.5** | 0 | 50 | 100 | 1 | — |
| **Boat** (`fishboat`) | 40.00 | 1.5 | **2.1** | 0 | 0 | 0 | 1 | — |
| **Galley** (`galley`) | 50.00 | 1.2 | **1.7** | 0 | 900 | 800 | 1 | — |
| **Xebec** (`xebec`) | 230.00 | 0.3 | **0.4** | 0 | 1600 | 320 | 1 | — |
| **Yacht** (`yachttur`) | 48.00 | 1.2 | **1.8** | 0 | 450 | 150 | 1 | — |

<a id="tursta--конюшня"></a>
<a id="production-tur-tursta"></a>
<a id="конюшня--tursta"></a>
### Stable — `tursta`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Heavy Sipahi** (`sipahi`) | 18.00 | 3.3 | **4.7** | 130 | 20 | 70 | 1 | 75 |
| **Light Sipahi** (`spakh`) | 9.00 | 6.7 | **9.3** | 80 | 6 | 5 | 1 | 60 |
| **Tatar** (`tatar`) | 11.25 | 5.3 | **7.5** | 70 | 6 | 0 | 1 | 60 |

<a id="turtem--мечеть"></a>
<a id="production-tur-turtem"></a>
<a id="мечеть--turtem"></a>
### Mosque — `turtem`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Mullah** (`mullah`) | 15.00 | 4.0 | **5.6** | 30 | 10 | 0 | 1 | — |

[↑ to contents](#содержание)

<a id="ukr--ukraine-украина"></a>
<a id="украина"></a>
## Ukraine (`ukr`)
<a id="rusmil--мельница-1"></a>
<a id="production-ukr-rusmil"></a>
<a id="мельница--rusmil-1"></a>
### Mill — `rusmil`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |

<a id="ukrart--артиллерийское-депо"></a>
<a id="production-ukr-ukrart"></a>
<a id="артиллерийское-депо--ukrart"></a>
### Artillery Depot — `ukrart`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Cannon** (`cannon`) | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| **Howitzer** (`howitzer`) | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| **Bombard** (`mortar`) | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |

<a id="ukrbar--козацкий-дом"></a>
<a id="production-ukr-ukrbar"></a>
<a id="козацкий-дом--ukrbar"></a>
### Cossack House — `ukrbar`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Serdiuk** (`serdiuk`) | 11.00 | 5.5 | **7.6** | 60 | 11 | 5 | 1 | — |

<a id="ukrcen--городской-центр"></a>
<a id="production-ukr-ukrcen"></a>
<a id="городской-центр--ukrcen"></a>
### Town Hall — `ukrcen`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Peasant** (`peaukr`) | 11.25 | 5.3 | **7.5** | 100 | 0 | 0 | 1 | 32 |

<a id="ukrdip--дипломатический-центр"></a>
<a id="production-ukr-ukrdip"></a>
<a id="дипломатический-центр--ukrdip"></a>
### Diplomatic Center — `ukrdip`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Archer (mercenary)** (`archerdip`) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| **Turkish archer (mercenary)** (`archerturdip`) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| **Sich Cossack (mercenary)** (`cossacksichdip`) | 2.50 | 24.0 | **33.6** | 0 | 60 | 0 | 1 | 60 |
| **Dragoon, 18th century (mercenary)** (`dragoon18dip`) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| **Grenadier (mercenary)** (`grenadierdip`) | 1.50 | 40.0 | **56.0** | 0 | 25 | 0 | 1 | 36 |
| **Light cavalry (mercenary)** (`lightcavalrydip`) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| **Light Infantryman (mercenary)** (`lightinfantrydip`) | 1.25 | 48.0 | **67.2** | 0 | 4 | 0 | 1 | — |
| **Roundshier (mercenary)** (`roundshierdip`) | 1.50 | 40.0 | **56.0** | 0 | 12 | 0 | 1 | — |

<a id="ukrpor--порт"></a>
<a id="production-ukr-ukrpor"></a>
<a id="порт--ukrpor"></a>
### Shipyard — `ukrpor`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Chaika** (`chaika`) | 40.00 | 1.5 | **2.1** | 0 | 600 | 200 | 1 | — |
| **Ferry** (`ferry`) | 56.00 | 1.1 | **1.5** | 0 | 50 | 100 | 1 | — |
| **Boat** (`fishboat`) | 40.00 | 1.5 | **2.1** | 0 | 0 | 0 | 1 | — |
| **Galley** (`galley`) | 50.00 | 1.2 | **1.7** | 0 | 900 | 800 | 1 | — |

<a id="ukrsta--конюшня"></a>
<a id="production-ukr-ukrsta"></a>
<a id="конюшня--ukrsta"></a>
### Stable — `ukrsta`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Register Cossack** (`cossackregister`) | 10.50 | 5.7 | **8.0** | 70 | 15 | 0 | 1 | 60 |
| **Sich Cossack** (`cossacksich`) | 13.50 | 4.4 | **6.2** | 130 | 0 | 2 | 1 | 60 |
| **Hetman** (`hetman`) | 16.50 | 3.6 | **5.1** | 150 | 150 | 10 | 1 | 90 |

<a id="ukrtem--православная-церковь"></a>
<a id="production-ukr-ukrtem"></a>
<a id="православная-церковь--ukrtem"></a>
### Orthodox Cathedral — `ukrtem`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Pope** (`pope`) | 20.00 | 3.0 | **4.2** | 40 | 20 | 0 | 1 | — |

[↑ to contents](#содержание)

<a id="ven--venice-венеция"></a>
<a id="венеция"></a>
## Venice (`ven`)
<a id="eurmil--мельница-12"></a>
<a id="production-ven-eurmil"></a>
<a id="мельница--eurmil-16"></a>
### Mill — `eurmil`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |

<a id="eurpor--порт-11"></a>
<a id="production-ven-eurpor"></a>
<a id="порт--eurpor-15"></a>
### Shipyard — `eurpor`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Ship of the Line** (`battleship`) | 390.00 | 0.2 | **0.2** | 0 | 3200 | 700 | 1 | — |
| **Ferry** (`ferry`) | 56.00 | 1.1 | **1.5** | 0 | 50 | 100 | 1 | — |
| **Boat** (`fishboat`) | 40.00 | 1.5 | **2.1** | 0 | 0 | 0 | 1 | — |
| **Frigate** (`frigate`) | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| **Galley** (`galley`) | 50.00 | 1.2 | **1.7** | 0 | 900 | 800 | 1 | — |
| **Yacht** (`yacht`) | 48.00 | 1.2 | **1.8** | 0 | 450 | 150 | 1 | — |

<a id="venart--артиллерийское-депо"></a>
<a id="production-ven-venart"></a>
<a id="артиллерийское-депо--venart"></a>
### Artillery Depot — `venart`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Cannon** (`cannon`) | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| **Howitzer** (`howitzer`) | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| **Bombard** (`mortar`) | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| **Multi-barrelled Cannon** (`multicannon`) | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

<a id="venba2--казарма-18в"></a>
<a id="production-ven-venba2"></a>
<a id="казарма-18в--venba2"></a>
### Barracks, 18th century — `venba2`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Drummer, 18th century** (`drummer18`) | 6.00 | 10.0 | **14.0** | 50 | 30 | 0 | 1 | — |
| **Grenadier** (`grenadier`) | 6.00 | 10.0 | **14.0** | 80 | 60 | 40 | 1 | 36 |
| **Musketeer, 18th century** (`musketeer18`) | 4.50 | 13.3 | **18.7** | 50 | 40 | 40 | 1 | — |
| **Officer, 18th century** (`officer18`) | 6.00 | 10.0 | **14.0** | 50 | 200 | 10 | 1 | — |
| **Pikeman, 18th century** (`pikeman18`) | 1.25 | 48.0 | **67.2** | 30 | 2 | 0 | 1 | — |

<a id="venbar--казарма-17в"></a>
<a id="production-ven-venbar"></a>
<a id="казарма-17в--venbar"></a>
### Barracks, 17th century — `venbar`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Drummer, 17th century** (`drummer`) | 5.00 | 12.0 | **16.8** | 60 | 20 | 0 | 1 | — |
| **Musketeer, 17th century** (`musketeer`) | 6.00 | 10.0 | **14.0** | 45 | 6 | 5 | 1 | — |
| **Officer, 17th century** (`officer`) | 10.00 | 6.0 | **8.4** | 50 | 150 | 30 | 1 | — |
| **Pikeman, 17th century** (`pikeman`) | 4.50 | 13.3 | **18.7** | 25 | 3 | 20 | 1 | — |

<a id="vencen--городской-центр"></a>
<a id="production-ven-vencen"></a>
<a id="городской-центр--vencen"></a>
### Town Hall — `vencen`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Peasant** (`peaspa`) | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

<a id="vendip--дипломатический-центр"></a>
<a id="production-ven-vendip"></a>
<a id="дипломатический-центр--vendip"></a>
### Diplomatic Center — `vendip`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Archer (mercenary)** (`archerdip`) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| **Turkish archer (mercenary)** (`archerturdip`) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| **Sich Cossack (mercenary)** (`cossacksichdip`) | 2.50 | 24.0 | **33.6** | 0 | 60 | 0 | 1 | 60 |
| **Dragoon, 18th century (mercenary)** (`dragoon18dip`) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| **Grenadier (mercenary)** (`grenadierdip`) | 1.50 | 40.0 | **56.0** | 0 | 25 | 0 | 1 | 36 |
| **Light cavalry (mercenary)** (`lightcavalrydip`) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| **Light Infantryman (mercenary)** (`lightinfantrydip`) | 1.25 | 48.0 | **67.2** | 0 | 4 | 0 | 1 | — |
| **Roundshier (mercenary)** (`roundshierdip`) | 1.50 | 40.0 | **56.0** | 0 | 12 | 0 | 1 | — |

<a id="vensta--конюшня"></a>
<a id="production-ven-vensta"></a>
<a id="конюшня--vensta"></a>
### Stable — `vensta`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Cuirassier** (`cuirassier`) | 22.50 | 2.7 | **3.7** | 120 | 35 | 25 | 1 | 75 |
| **Dragoon, 17th century** (`dragoon`) | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | 60 |
| **Dragoon, 18th century** (`dragoon18`) | 22.50 | 2.7 | **3.7** | 70 | 60 | 7 | 1 | 60 |
| **Hussar** (`hussar`) | 15.00 | 4.0 | **5.6** | 70 | 20 | 2 | 1 | 60 |
| **Reiter** (`reiter`) | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | 75 |

<a id="ventem--собор"></a>
<a id="production-ven-ventem"></a>
<a id="собор--ventem"></a>
### Cathedral — `ventem`

| Unit | Training time (game s) | Units/game min | Units/real min at Fast | Food | Gold | Iron | Population | Food upkeep |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Priest** (`priest`) | 20.00 | 3.0 | **4.2** | 60 | 25 | 0 | 1 | — |

[↑ to contents](#содержание)

---

<a id="замечания"></a>
## Notes

1. **Each unit uses one population slot.** Town Halls, Houses, and Barracks
   increase the available capacity.
2. **Food upkeep** is consumed continuously in game time. Heavy cavalry
   generally requires more food than infantry.
3. **Production pauses at the population limit.** Progress resumes when
   capacity becomes available.
4. **Several buildings add their rates together.** For example, five
   identical Barracks train units five times as quickly as one.

<a id="источники"></a>
## Sources

All links are relative to `data/scripts/` in the Cossacks 3 installation.

[^1]: `DoProgressOrders` — production-queue processing —
      `units/building.inc/doprogressorders.inc:120-373`.
