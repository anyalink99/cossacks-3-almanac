<a id="cossacks-3--темпы-производства"></a>
<a id="скорость-производства-юнитов"></a>
# Cossacks 3 - Production Rate

[← Tables and calculations](../README.md)

How many units per minute does **one building** provide, with an uninterrupted queue and without farm/resource restrictions.

**Mechanics** [^1]:
- The building has ONE queue (`orders[0]`). There is **no parallel construction**.
- Progress: `progress += deltatime / unit.buildtime`. When `progress ≥ 1` the unit spawns, progress is reset.
- The cost is written off **immediately (upfront)** at the start of each unit.
- If you hit the farm cap or unit cap, production **stops**, there is no progress.

**Formula:**
- `rate_per_g_sec = 1 / unit.buildtime_sec`
- `rate_per_real_sec_fast = rate_per_g_sec × 1.4`
- `units_per_real_min_fast = rate_per_real_sec_fast × 60`

Grouped by nations. For each building there is a list of units that it can produce.

<a id="содержание"></a>
## Contents

- **[ALG - Algeria](#alg--algeria-алжир)** - [`algart`](#algart--артиллерийское-депо), [`algbar`](#algbar--казарма), [`algcen`](#algcen--городской-центр), [`algdip`](#algdip--дипломатический-центр), [`algsta`](#algsta--конюшня), [`algtem`](#algtem--мечеть), [`turmil`](#turmil--мельница), [`turpor`](#turpor--порт)
- **[AUS - Austria](#aus--austria-австрия)** - [`ausart`](#ausart--артиллерийское-депо), [`ausba2`](#ausba2--казарма-18в), [`ausbar`](#ausbar--казарма-17в), [`auscen`](#auscen--городской-центр), [`ausdip`](#ausdip--дипломатический-центр), [`aussta`](#aussta--конюшня), [`austem`](#austem--собор), [`eurmil`](#eurmil--мельница), [`eurpor`](#eurpor--порт)
- **[BAV - Bavaria](#bav--bavaria-бавария)** - [`bavart`](#bavart--артиллерийское-депо), [`bavba2`](#bavba2--казарма-18в), [`bavbar`](#bavbar--казарма-17в), [`bavcen`](#bavcen--городской-центр), [`bavdip`](#bavdip--дипломатический-центр), [`bavsta`](#bavsta--конюшня), [`bavtem`](#bavtem--собор), [`eurmil`](#eurmil--мельница), [`eurpor`](#eurpor--порт)
- **[DEN - Denmark](#den--denmark-дания)** - [`denart`](#denart--артиллерийское-депо), [`denba2`](#denba2--казарма-18в), [`denbar`](#denbar--казарма-17в), [`dencen`](#dencen--городской-центр), [`dendip`](#dendip--дипломатический-центр), [`densta`](#densta--конюшня), [`dentem`](#dentem--собор), [`eurmil`](#eurmil--мельница), [`eurpor`](#eurpor--порт)
- **[ENG - England](#eng--england-англия)** - [`engart`](#engart--артиллерийское-депо), [`engba2`](#engba2--казарма-18в), [`engbar`](#engbar--казарма-17в), [`engcen`](#engcen--городской-центр), [`engdip`](#engdip--дипломатический-центр), [`engsta`](#engsta--конюшня), [`engtem`](#engtem--собор), [`eurmil`](#eurmil--мельница), [`eurpor`](#eurpor--порт)
- **[FRA - France](#fra--france-франция)** - [`eurmil`](#eurmil--мельница), [`eurpor`](#eurpor--порт), [`fraart`](#fraart--артиллерийское-депо), [`fraba2`](#fraba2--казарма-18в), [`frabar`](#frabar--казарма-17в), [`fracen`](#fracen--городской-центр), [`fradip`](#fradip--дипломатический-центр), [`frasta`](#frasta--конюшня), [`fratem`](#fratem--собор)
- **[HUN - Hungary](#hun--hungary-венгрия)** - [`eurmil`](#eurmil--мельница), [`eurpor`](#eurpor--порт), [`hunart`](#hunart--артиллерийское-депо), [`hunba2`](#hunba2--казарма-18в), [`hunbar`](#hunbar--казарма-17в), [`huncen`](#huncen--городской-центр), [`hundip`](#hundip--дипломатический-центр), [`hunsta`](#hunsta--конюшня), [`huntem`](#huntem--собор)
- **[NET — Netherlands](#net--netherlands-нидерланды)** — [`eurmil`](#eurmil--мельница), [`eurpor`](#eurpor--порт), [`netart`](#netart--артиллерийское-депо), [`netba2`](#netba2--казарма-18в), [`netbar`](#netbar--казарма-17в), [`netcen`](#netcen--городской-центр), [`netdip`](#netdip--дипломатический-центр), [`netsta`](#netsta--конюшня), [`nettem`](#nettem--собор)
- **[PIE — Piedmont](#pie--piedmont-пьемонт)** — [`eurmil`](#eurmil--мельница), [`eurpor`](#eurpor--порт), [`pieart`](#pieart--артиллерийское-депо), [`pieba2`](#pieba2--казарма-18в), [`piebar`](#piebar--казарма-17в), [`piecen`](#piecen--городской-центр), [`piedip`](#piedip--дипломатический-центр), [`piesta`](#piesta--конюшня), [`pietem`](#pietem--собор)
- **[POL — Poland](#pol--poland-польша)** — [`eurmil`](#eurmil--мельница), [`eurpor`](#eurpor--порт), [`polart`](#polart--артиллерийское-депо), [`polba2`](#polba2--казарма-18в), [`polbar`](#polbar--казарма-17в), [`polcen`](#polcen--городской-центр), [`poldip`](#poldip--дипломатический-центр), [`polsta`](#polsta--конюшня), [`poltem`](#poltem--собор)
- **[POR — Portugal](#por--portugal-португалия)** — [`eurmil`](#eurmil--мельница), [`porart`](#porart--артиллерийское-депо), [`porba2`](#porba2--казарма-18в), [`porbar`](#porbar--казарма-17в), [`porcen`](#porcen--городской-центр), [`pordip`](#pordip--дипломатический-центр), [`porpor`](#porpor--порт), [`porsta`](#porsta--конюшня), [`portem`](#portem--собор)
- **[PRU — Prussia](#pru--prussia-пруссия)** — [`eurmil`](#eurmil--мельница), [`eurpor`](#eurpor--порт), [`pruart`](#pruart--артиллерийское-депо), [`pruba2`](#pruba2--казарма-18в), [`prubar`](#prubar--казарма-17в), [`prucen`](#prucen--городской-центр), [`prudip`](#prudip--дипломатический-центр), [`prusta`](#prusta--конюшня), [`prutem`](#prutem--собор)
- **[RUS — Russia](#rus--russia-россия)** — [`rusart`](#rusart--артиллерийское-депо), [`rusba2`](#rusba2--казарма-18в), [`rusbar`](#rusbar--стрелецкая-казарма), [`ruscen`](#ruscen--городской-центр), [`rusdip`](#rusdip--дипломатический-центр), [`rusmil`](#rusmil--мельница), [`ruspor`](#ruspor--порт), [`russta`](#russta--конюшня), [`rustem`](#rustem--православная-церковь)
- **[SAX — Saxony](#sax--saxony-саксония)** — [`eurmil`](#eurmil--мельница), [`eurpor`](#eurpor--порт), [`saxart`](#saxart--артиллерийское-депо), [`saxba2`](#saxba2--казарма-18в), [`saxbar`](#saxbar--казарма-17в), [`saxcen`](#saxcen--городской-центр), [`saxdip`](#saxdip--дипломатический-центр), [`saxsta`](#saxsta--конюшня), [`saxtem`](#saxtem--собор)
- **[SCO — Scotland](#sco--scotland-шотландия)** — [`eurmil`](#eurmil--мельница), [`eurpor`](#eurpor--порт), [`scoart`](#scoart--артиллерийское-депо), [`scoba2`](#scoba2--замок), [`scobar`](#scobar--казарма-17в), [`scocen`](#scocen--городской-центр), [`scodip`](#scodip--дипломатический-центр), [`scosta`](#scosta--конюшня), [`scotem`](#scotem--собор)
- **[SPA — Spain](#spa--spain-испания)** — [`eurmil`](#eurmil--мельница), [`eurpor`](#eurpor--порт), [`spaart`](#spaart--артиллерийское-депо), [`spaba2`](#spaba2--казарма-18в), [`spabar`](#spabar--казарма-17в), [`spacen`](#spacen--городской-центр), [`spadip`](#spadip--дипломатический-центр), [`spasta`](#spasta--конюшня), [`spatem`](#spatem--собор)
- **[SWE - Sweden](#swe--sweden-швеция)** - [`eurmil`](#eurmil--мельница), [`eurpor`](#eurpor--порт), [`sweart`](#sweart--артиллерийское-депо), [`sweba2`](#sweba2--казарма-18в), [`swebar`](#swebar--казарма-17в), [`swecen`](#swecen--городской-центр), [`swedip`](#swedip--дипломатический-центр), [`swesta`](#swesta--конюшня), [`swetem`](#swetem--собор)
- **[SWI - Switzerland](#swi--switzerland-швейцария)** - [`eurmil`](#eurmil--мельница), [`eurpor`](#eurpor--порт), [`swiart`](#swiart--артиллерийское-депо), [`swiba2`](#swiba2--казарма-18в), [`swibar`](#swibar--казарма-17в), [`swicen`](#swicen--городской-центр), [`swidip`](#swidip--дипломатический-центр), [`swista`](#swista--конюшня), [`switem`](#switem--собор)
- **[TUR - Turkey](#tur--turkey-турция)** - [`turart`](#turart--артиллерийское-депо), [`turbar`](#turbar--казарма), [`turcen`](#turcen--городской-центр), [`turdip`](#turdip--дипломатический-центр), [`turmil`](#turmil--мельница), [`turpor`](#turpor--порт), [`tursta`](#tursta--конюшня), [`turtem`](#turtem--мечеть)
- **[UKR - Ukraine](#ukr--ukraine-украина)** - [`rusmil`](#rusmil--мельница), [`ukrart`](#ukrart--артиллерийское-депо), [`ukrbar`](#ukrbar--козацкий-дом), [`ukrcen`](#ukrcen--городской-центр), [`ukrdip`](#ukrdip--дипломатический-центр), [`ukrpor`](#ukrpor--порт), [`ukrsta`](#ukrsta--конюшня), [`ukrtem`](#ukrtem--православная-церковь)
- **[VEN - Venice](#ven--venice-венеция)** - [`eurmil`](#eurmil--мельница), [`eurpor`](#eurpor--порт), [`venart`](#venart--артиллерийское-депо), [`venba2`](#venba2--казарма-18в), [`venbar`](#venbar--казарма-17в), [`vencen`](#vencen--городской-центр), [`vendip`](#vendip--дипломатический-центр), [`vensta`](#vensta--конюшня), [`ventem`](#ventem--собор)

<a id="alg--algeria-алжир"></a>
<a id="алжир"></a>
## Algeria (`alg`)
<a id="algart--артиллерийское-депо"></a>
<a id="артиллерийское-депо--algart"></a>
### `algart` — Artillery Depot

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cannon` | Cannon | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| `howitzer` | Howitzer | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| `mortar` | Bombard | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |

<a id="algbar--казарма"></a>
<a id="казарма--algbar"></a>
### `algbar` — Barracks

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `archer` | Archer | 1.50 | 40.0 | **56.0** | 20 | 1 | 0 | 1 | — |
| `drummertur` | Drummer, 17th century | 4.00 | 15.0 | **21.0** | 30 | 15 | 0 | 1 | — |
| `lightinfantry` | Light Infantryman | 1.00 | 60.0 | **84.0** | 25 | 0 | 1 | 1 | — |
| `officertur` | Officer | 7.50 | 8.0 | **11.2** | 50 | 100 | 0 | 1 | — |
| `pikemantur` | Ottoman Pikeman | 5.50 | 10.9 | **15.3** | 55 | 5 | 0 | 1 | — |

<a id="algcen--городской-центр"></a>
<a id="городской-центр--algcen"></a>
### `algcen` — Town Hall

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `peatur` | Peasant | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 28 |

<a id="algdip--дипломатический-центр"></a>
<a id="дипломатический-центр--algdip"></a>
### `algdip` — Diplomatic Center

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `archerdip` | Archer (mercenary) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| `archerturdip` | Turkish archer (mercenary) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| `cossacksichdip` | Sich Cossack (mercenary) | 2.50 | 24.0 | **33.6** | 0 | 60 | 0 | 1 | 60 |
| `dragoon18dip` | Dragoon, 18th century (mercenary) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| `grenadierdip` | Grenadier (mercenary) | 1.50 | 40.0 | **56.0** | 0 | 25 | 0 | 1 | 36 |
| `lightcavalrydip` | Light cavalry (mercenary) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| `lightinfantrydip` | Light Infantryman (mercenary) | 1.25 | 48.0 | **67.2** | 0 | 4 | 0 | 1 | — |
| `roundshierdip` | Roundshier (mercenary) | 1.50 | 40.0 | **56.0** | 0 | 12 | 0 | 1 | — |

<a id="algsta--конюшня"></a>
<a id="конюшня--algsta"></a>
### `algsta` — Stable

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `mameluke` | Mameluke | 12.00 | 5.0 | **7.0** | 100 | 8 | 0 | 1 | 60 |

<a id="algtem--мечеть"></a>
<a id="мечеть--algtem"></a>
### `algtem` — Mosque

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `mullah` | Mullah | 15.00 | 4.0 | **5.6** | 30 | 10 | 0 | 1 | — |

<a id="мельница--turmil"></a>
### `turmil` — Mill

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

<a id="порт--turpor"></a>
### `turpor` — Shipyard

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `battleship` | Ship of the Line | 390.00 | 0.2 | **0.2** | 0 | 3200 | 700 | 1 | — |
| `ferry` | Ferry | 56.00 | 1.1 | **1.5** | 0 | 50 | 100 | 1 | — |
| `fishboat` | Boat | 40.00 | 1.5 | **2.1** | 0 | 0 | 0 | 1 | — |
| `galley` | Galley | 50.00 | 1.2 | **1.7** | 0 | 900 | 800 | 1 | — |
| `xebec` | Xebec | 230.00 | 0.3 | **0.4** | 0 | 1600 | 320 | 1 | — |

[↑ to contents](#содержание)

<a id="aus--austria-австрия"></a>
<a id="австрия"></a>
## Austria (`aus`)
<a id="ausart--артиллерийское-депо"></a>
<a id="артиллерийское-депо--ausart"></a>
### `ausart` — Artillery Depot

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cannon` | Cannon | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| `howitzer` | Howitzer | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| `mortar` | Bombard | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| `multicannon` | Multi-barrelled Cannon | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

<a id="ausba2--казарма-18в"></a>
<a id="казарма-18в--ausba2"></a>
### `ausba2` — Barracks, 18th century

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer18` | Drummer, 18th century | 6.00 | 10.0 | **14.0** | 50 | 30 | 0 | 1 | — |
| `grenadier` | Grenadier | 6.00 | 10.0 | **14.0** | 80 | 60 | 40 | 1 | 36 |
| `musketeer18` | Musketeer, 18th century | 4.50 | 13.3 | **18.7** | 50 | 40 | 40 | 1 | — |
| `officer18` | Officer, 18th century | 6.00 | 10.0 | **14.0** | 50 | 200 | 10 | 1 | — |
| `pandur` | Pandur | 5.50 | 10.9 | **15.3** | 40 | 15 | 10 | 1 | — |
| `pikeman18` | Pikeman, 18th century | 1.25 | 48.0 | **67.2** | 30 | 2 | 0 | 1 | — |

<a id="ausbar--казарма-17в"></a>
<a id="казарма-17в--ausbar"></a>
### `ausbar` — Barracks, 17th century

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer` | Drummer, 17th century | 5.00 | 12.0 | **16.8** | 60 | 20 | 0 | 1 | — |
| `musketeeraus` | Musketeer, 17th century | 6.50 | 9.2 | **12.9** | 35 | 9 | 15 | 1 | — |
| `officer` | Officer, 17th century | 10.00 | 6.0 | **8.4** | 50 | 150 | 30 | 1 | — |
| `pikeman` | Pikeman, 17th century | 4.50 | 13.3 | **18.7** | 25 | 3 | 20 | 1 | — |
| `roundshier` | Roundshier | 4.00 | 15.0 | **21.0** | 20 | 3 | 25 | 1 | — |
<a id="auscen--городской-центр"></a>
<a id="городской-центр--auscen"></a>
### `auscen` — Town Hall

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `peaaus` | Peasant | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

<a id="ausdip--дипломатический-центр"></a>
<a id="дипломатический-центр--ausdip"></a>
### `ausdip` — Diplomatic Center

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `archerdip` | Archer (mercenary) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| `archerturdip` | Turkish archer (mercenary) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| `cossacksichdip` | Sich Cossack (mercenary) | 2.50 | 24.0 | **33.6** | 0 | 60 | 0 | 1 | 60 |
| `dragoon18dip` | Dragoon, 18th century (mercenary) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| `grenadierdip` | Grenadier (mercenary) | 1.50 | 40.0 | **56.0** | 0 | 25 | 0 | 1 | 36 |
| `lightcavalrydip` | Light cavalry (mercenary) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| `lightinfantrydip` | Light Infantryman (mercenary) | 1.25 | 48.0 | **67.2** | 0 | 4 | 0 | 1 | — |
| `roundshierdip` | Roundshier (mercenary) | 1.50 | 40.0 | **56.0** | 0 | 12 | 0 | 1 | — |

<a id="aussta--конюшня"></a>
<a id="конюшня--aussta"></a>
### `aussta` — Stable

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `croat` | Croat | 15.75 | 3.8 | **5.3** | 80 | 6 | 2 | 1 | 60 |
| `cuirassier` | Cuirassier | 22.50 | 2.7 | **3.7** | 120 | 35 | 25 | 1 | 75 |
| `dragoon` | Dragoon, 17th century | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | 60 |
| `dragoon18` | Dragoon, 18th century | 22.50 | 2.7 | **3.7** | 70 | 60 | 7 | 1 | 60 |
| `hussar` | Hussar | 15.00 | 4.0 | **5.6** | 70 | 20 | 2 | 1 | 60 |
| `reiter` | Reiter | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | 75 |

<a id="austem--собор"></a>
<a id="собор--austem"></a>
### `austem` — Cathedral

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `priest` | Priest | 20.00 | 3.0 | **4.2** | 60 | 25 | 0 | 1 | — |

<a id="мельница--eurmil"></a>
### `eurmil` — Mill

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

<a id="порт--eurpor"></a>
### `eurpor` — Shipyard

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `battleship` | Ship of the Line | 390.00 | 0.2 | **0.2** | 0 | 3200 | 700 | 1 | — |
| `ferry` | Ferry | 56.00 | 1.1 | **1.5** | 0 | 50 | 100 | 1 | — |
| `fishboat` | Boat | 40.00 | 1.5 | **2.1** | 0 | 0 | 0 | 1 | — |
| `frigate` | Frigate | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| `galley` | Galley | 50.00 | 1.2 | **1.7** | 0 | 900 | 800 | 1 | — |
| `yacht` | Yacht | 48.00 | 1.2 | **1.8** | 0 | 450 | 150 | 1 | — |

[↑ to contents](#содержание)

<a id="bav--bavaria-бавария"></a>
<a id="бавария"></a>
## Bavaria (`bav`)
<a id="bavart--артиллерийское-депо"></a>
<a id="артиллерийское-депо--bavart"></a>
### `bavart` — Artillery Depot

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cannon` | Cannon | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| `howitzer` | Howitzer | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| `mortar` | Bombard | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| `multicannon` | Multi-barrelled Cannon | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

<a id="bavba2--казарма-18в"></a>
<a id="казарма-18в--bavba2"></a>
### `bavba2` — Barracks, 18th century
| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer18` | Drummer, 18th century | 6.00 | 10.0 | **14.0** | 50 | 30 | 0 | 1 | — |
| `grenadierbav` | Grenadier | 6.00 | 10.0 | **14.0** | 95 | 70 | 40 | 1 | 36 |
| `musketeer18bav` | Musketeer, 18th century | 5.00 | 12.0 | **16.8** | 60 | 55 | 35 | 1 | — |
| `officer18` | Officer, 18th century | 6.00 | 10.0 | **14.0** | 50 | 200 | 10 | 1 | — |
| `pikeman18` | Pikeman, 18th century | 1.25 | 48.0 | **67.2** | 30 | 2 | 0 | 1 | — |

<a id="bavbar--казарма-17в"></a>
<a id="казарма-17в--bavbar"></a>
### `bavbar` — Barracks, 17th century

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer` | Drummer, 17th century | 5.00 | 12.0 | **16.8** | 60 | 20 | 0 | 1 | — |
| `musketeer` | Musketeer, 17th century | 6.00 | 10.0 | **14.0** | 45 | 6 | 5 | 1 | — |
| `officer` | Officer, 17th century | 10.00 | 6.0 | **8.4** | 50 | 150 | 30 | 1 | — |
| `pikeman` | Pikeman, 17th century | 4.50 | 13.3 | **18.7** | 25 | 3 | 20 | 1 | — |

<a id="bavcen--городской-центр"></a>
<a id="городской-центр--bavcen"></a>
### `bavcen` — Town Hall

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `peaaus` | Peasant | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

<a id="bavdip--дипломатический-центр"></a>
<a id="дипломатический-центр--bavdip"></a>
### `bavdip` — Diplomatic Center

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `archerdip` | Archer (mercenary) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| `archerturdip` | Turkish archer (mercenary) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| `cossacksichdip` | Sich Cossack (mercenary) | 2.50 | 24.0 | **33.6** | 0 | 60 | 0 | 1 | 60 |
| `dragoon18dip` | Dragoon, 18th century (mercenary) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| `grenadierdip` | Grenadier (mercenary) | 1.50 | 40.0 | **56.0** | 0 | 25 | 0 | 1 | 36 |
| `lightcavalrydip` | Light cavalry (mercenary) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| `lightinfantrydip` | Light Infantryman (mercenary) | 1.25 | 48.0 | **67.2** | 0 | 4 | 0 | 1 | — |
| `roundshierdip` | Roundshier (mercenary) | 1.50 | 40.0 | **56.0** | 0 | 12 | 0 | 1 | — |

<a id="bavsta--конюшня"></a>
<a id="конюшня--bavsta"></a>
### `bavsta` — Stable

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cuirassier` | Cuirassier | 22.50 | 2.7 | **3.7** | 120 | 35 | 25 | 1 | 75 |
| `dragoon` | Dragoon, 17th century | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | 60 |
| `dragoon18` | Dragoon, 18th century | 22.50 | 2.7 | **3.7** | 70 | 60 | 7 | 1 | 60 |
| `hussar` | Hussar | 15.00 | 4.0 | **5.6** | 70 | 20 | 2 | 1 | 60 |
| `reiter` | Reiter | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | 75 |

<a id="bavtem--собор"></a>
<a id="собор--bavtem"></a>
### `bavtem` — Cathedral

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `priest` | Priest | 20.00 | 3.0 | **4.2** | 60 | 25 | 0 | 1 | — |

<a id="eurmil--мельница"></a>
### `eurmil` — Mill

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

<a id="eurpor--порт"></a>
### `eurpor` — Shipyard

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `battleship` | Ship of the Line | 390.00 | 0.2 | **0.2** | 0 | 3200 | 700 | 1 | — |
| `ferry` | Ferry | 56.00 | 1.1 | **1.5** | 0 | 50 | 100 | 1 | — |
| `fishboat` | Boat | 40.00 | 1.5 | **2.1** | 0 | 0 | 0 | 1 | — |
| `frigate` | Frigate | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| `galley` | Galley | 50.00 | 1.2 | **1.7** | 0 | 900 | 800 | 1 | — |
| `yacht` | Yacht | 48.00 | 1.2 | **1.8** | 0 | 450 | 150 | 1 | — |

[↑ to contents](#содержание)

<a id="den--denmark-дания"></a>
<a id="дания"></a>
## Denmark (`den`)
<a id="denart--артиллерийское-депо"></a>
<a id="артиллерийское-депо--denart"></a>
### `denart` — Artillery Depot

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cannon` | Cannon | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| `howitzer` | Howitzer | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| `mortar` | Bombard | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| `multicannon` | Multi-barrelled Cannon | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

<a id="denba2--казарма-18в"></a>
<a id="казарма-18в--denba2"></a>
### `denba2` — Barracks, 18th century

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer18` | Drummer, 18th century | 6.00 | 10.0 | **14.0** | 50 | 30 | 0 | 1 | — |
| `grenadierden` | Grenadier | 6.50 | 9.2 | **12.9** | 100 | 90 | 40 | 1 | 36 |
| `musketeer18den` | Musketeer, 18th century | 5.50 | 10.9 | **15.3** | 50 | 80 | 40 | 1 | — |
| `officer18` | Officer, 18th century | 6.00 | 10.0 | **14.0** | 50 | 200 | 10 | 1 | — |
| `pikeman18` | Pikeman, 18th century | 1.25 | 48.0 | **67.2** | 30 | 2 | 0 | 1 | — |

<a id="denbar--казарма-17в"></a>
<a id="казарма-17в--denbar"></a>
### `denbar` — Barracks, 17th century

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer` | Drummer, 17th century | 5.00 | 12.0 | **16.8** | 60 | 20 | 0 | 1 | — |
| `musketeer` | Musketeer, 17th century | 6.00 | 10.0 | **14.0** | 45 | 6 | 5 | 1 | — |
| `officer` | Officer, 17th century | 10.00 | 6.0 | **8.4** | 50 | 150 | 30 | 1 | — |
| `pikeman` | Pikeman, 17th century | 4.50 | 13.3 | **18.7** | 25 | 3 | 20 | 1 | — |

<a id="dencen--городской-центр"></a>
<a id="городской-центр--dencen"></a>
### `dencen` — Town Hall

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `peaeng` | Peasant | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

<a id="dendip--дипломатический-центр"></a>
<a id="дипломатический-центр--dendip"></a>
### `dendip` — Diplomatic Center

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `archerdip` | Archer (mercenary) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| `archerturdip` | Turkish archer (mercenary) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| `cossacksichdip` | Sich Cossack (mercenary) | 2.50 | 24.0 | **33.6** | 0 | 60 | 0 | 1 | 60 |
| `dragoon18dip` | Dragoon, 18th century (mercenary) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| `grenadierdip` | Grenadier (mercenary) | 1.50 | 40.0 | **56.0** | 0 | 25 | 0 | 1 | 36 |
| `lightcavalrydip` | Light cavalry (mercenary) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| `lightinfantrydip` | Light Infantryman (mercenary) | 1.25 | 48.0 | **67.2** | 0 | 4 | 0 | 1 | — |
| `roundshierdip` | Roundshier (mercenary) | 1.50 | 40.0 | **56.0** | 0 | 12 | 0 | 1 | — |

<a id="densta--конюшня"></a>
<a id="конюшня--densta"></a>
### `densta` — Stable

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cuirassier` | Cuirassier | 22.50 | 2.7 | **3.7** | 120 | 35 | 25 | 1 | 75 |
| `dragoon` | Dragoon, 17th century | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | 60 |
| `dragoon18` | Dragoon, 18th century | 22.50 | 2.7 | **3.7** | 70 | 60 | 7 | 1 | 60 |
| `hussar` | Hussar | 15.00 | 4.0 | **5.6** | 70 | 20 | 2 | 1 | 60 |
| `reiter` | Reiter | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | 75 |

<a id="dentem--собор"></a>
<a id="собор--dentem"></a>
### `dentem` — Cathedral

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `priest` | Priest | 20.00 | 3.0 | **4.2** | 60 | 25 | 0 | 1 | — |

<a id="eurmil--мельница"></a>
### `eurmil` — Mill

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

<a id="eurpor--порт"></a>
### `eurpor` — Shipyard

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `battleship` | Ship of the Line | 390.00 | 0.2 | **0.2** | 0 | 3200 | 700 | 1 | — |
| `ferry` | Ferry | 56.00 | 1.1 | **1.5** | 0 | 50 | 100 | 1 | — |
| `fishboat` | Boat | 40.00 | 1.5 | **2.1** | 0 | 0 | 0 | 1 | — |
| `frigate` | Frigate | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| `galley` | Galley | 50.00 | 1.2 | **1.7** | 0 | 900 | 800 | 1 | — |
| `yacht` | Yacht | 48.00 | 1.2 | **1.8** | 0 | 450 | 150 | 1 | — |

[↑ to contents](#содержание)

<a id="eng--england-англия"></a>
<a id="англия"></a>
## England (`eng`)
<a id="engart--артиллерийское-депо"></a>
<a id="артиллерийское-депо--engart"></a>
### `engart` — Artillery Depot

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cannon` | Cannon | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| `howitzer` | Howitzer | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| `mortar` | Bombard | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| `multicannon` | Multi-barrelled Cannon | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

<a id="engba2--казарма-18в"></a>
<a id="казарма-18в--engba2"></a>
### `engba2` — Barracks, 18th century

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `bagpiper` | Bagpiper | 7.00 | 8.6 | **12.0** | 120 | 20 | 0 | 1 | — |
| `grenadier` | Grenadier | 6.00 | 10.0 | **14.0** | 80 | 60 | 40 | 1 | 36 |
| `highlander` | Highlander | 6.50 | 9.2 | **12.9** | 90 | 25 | 10 | 1 | 39 |
| `musketeer18` | Musketeer, 18th century | 4.50 | 13.3 | **18.7** | 50 | 40 | 40 | 1 | — |
| `officer18` | Officer, 18th century | 6.00 | 10.0 | **14.0** | 50 | 200 | 10 | 1 | — |
| `pikeman18` | Pikeman, 18th century | 1.25 | 48.0 | **67.2** | 30 | 2 | 0 | 1 | — |

<a id="engbar--казарма-17в"></a>
<a id="казарма-17в--engbar"></a>
### `engbar` — Barracks, 17th century

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer` | Drummer, 17th century | 5.00 | 12.0 | **16.8** | 60 | 20 | 0 | 1 | — |
| `musketeer` | Musketeer, 17th century | 6.00 | 10.0 | **14.0** | 45 | 6 | 5 | 1 | — |
| `officer` | Officer, 17th century | 10.00 | 6.0 | **8.4** | 50 | 150 | 30 | 1 | — |
| `pikeman` | Pikeman, 17th century | 4.50 | 13.3 | **18.7** | 25 | 3 | 20 | 1 | — |

<a id="engcen--городской-центр"></a>
<a id="городской-центр--engcen"></a>
### `engcen` — Town Hall

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `peaeng` | Peasant | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

<a id="engdip--дипломатический-центр"></a>
<a id="дипломатический-центр--engdip"></a>
### `engdip` — Diplomatic Center

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `archerdip` | Archer (mercenary) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| `archerturdip` | Turkish archer (mercenary) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| `cossacksichdip` | Sich Cossack (mercenary) | 2.50 | 24.0 | **33.6** | 0 | 60 | 0 | 1 | 60 |
| `dragoon18dip` | Dragoon, 18th century (mercenary) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| `grenadierdip` | Grenadier (mercenary) | 1.50 | 40.0 | **56.0** | 0 | 25 | 0 | 1 | 36 |
| `lightcavalrydip` | Light cavalry (mercenary) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| `lightinfantrydip` | Light Infantryman (mercenary) | 1.25 | 48.0 | **67.2** | 0 | 4 | 0 | 1 | — |
| `roundshierdip` | Roundshier (mercenary) | 1.50 | 40.0 | **56.0** | 0 | 12 | 0 | 1 | — |

<a id="engsta--конюшня"></a>
<a id="конюшня--engsta"></a>
### `engsta` — Stable

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cuirassier` | Cuirassier | 22.50 | 2.7 | **3.7** | 120 | 35 | 25 | 1 | 75 |
| `dragoon` | Dragoon, 17th century | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | 60 |
| `dragoon18` | Dragoon, 18th century | 22.50 | 2.7 | **3.7** | 70 | 60 | 7 | 1 | 60 |
| `hussar` | Hussar | 15.00 | 4.0 | **5.6** | 70 | 20 | 2 | 1 | 60 |
| `reiter` | Reiter | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | 75 |

<a id="engtem--собор"></a>
<a id="собор--engtem"></a>
### `engtem` — Cathedral

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `priest` | Priest | 20.00 | 3.0 | **4.2** | 60 | 25 | 0 | 1 | — |

<a id="eurmil--мельница"></a>
### `eurmil` — Mill

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

<a id="eurpor--порт"></a>
### `eurpor` — Shipyard

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `battleship` | Ship of the Line | 390.00 | 0.2 | **0.2** | 0 | 3200 | 700 | 1 | — |
| `ferry` | Ferry | 56.00 | 1.1 | **1.5** | 0 | 50 | 100 | 1 | — |
| `fishboat` | Boat | 40.00 | 1.5 | **2.1** | 0 | 0 | 0 | 1 | — |
| `frigate` | Frigate | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| `galley` | Galley | 50.00 | 1.2 | **1.7** | 0 | 900 | 800 | 1 | — |
| `yacht` | Yacht | 48.00 | 1.2 | **1.8** | 0 | 450 | 150 | 1 | — |

[↑ to contents](#содержание)

<a id="fra--france-франция"></a>
<a id="франция"></a>
## France (`fra`)
<a id="eurmil--мельница"></a>
### `eurmil` — Mill

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

<a id="eurpor--порт"></a>
### `eurpor` — Shipyard

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `battleship` | Ship of the Line | 390.00 | 0.2 | **0.2** | 0 | 3200 | 700 | 1 | — |
| `ferry` | Ferry | 56.00 | 1.1 | **1.5** | 0 | 50 | 100 | 1 | — |
| `fishboat` | Boat | 40.00 | 1.5 | **2.1** | 0 | 0 | 0 | 1 | — |
| `frigate` | Frigate | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| `galley` | Galley | 50.00 | 1.2 | **1.7** | 0 | 900 | 800 | 1 | — |
| `yacht` | Yacht | 48.00 | 1.2 | **1.8** | 0 | 450 | 150 | 1 | — |

<a id="fraart--артиллерийское-депо"></a>
<a id="артиллерийское-депо--fraart"></a>
### `fraart` — Artillery Depot

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cannon` | Cannon | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| `howitzer` | Howitzer | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| `mortar` | Bombard | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| `multicannon` | Multi-barrelled Cannon | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

<a id="fraba2--казарма-18в"></a>
<a id="казарма-18в--fraba2"></a>
### `fraba2` — Barracks, 18th century

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `chasseur` | Chasseur | 7.50 | 8.0 | **11.2** | 50 | 45 | 15 | 1 | — |
| `drummer18` | Drummer, 18th century | 6.00 | 10.0 | **14.0** | 50 | 30 | 0 | 1 | — |
| `grenadier` | Grenadier | 6.00 | 10.0 | **14.0** | 80 | 60 | 40 | 1 | 36 |
| `musketeer18` | Musketeer, 18th century | 4.50 | 13.3 | **18.7** | 50 | 40 | 40 | 1 | — |
| `officer18` | Officer, 18th century | 6.00 | 10.0 | **14.0** | 50 | 200 | 10 | 1 | — |
| `pikeman18` | Pikeman, 18th century | 1.25 | 48.0 | **67.2** | 30 | 2 | 0 | 1 | — |

<a id="frabar--казарма-17в"></a>
<a id="казарма-17в--frabar"></a>
### `frabar` — Barracks, 17th century

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer` | Drummer, 17th century | 5.00 | 12.0 | **16.8** | 60 | 20 | 0 | 1 | — |
| `musketeer` | Musketeer, 17th century | 6.00 | 10.0 | **14.0** | 45 | 6 | 5 | 1 | — |
| `officer` | Officer, 17th century | 10.00 | 6.0 | **8.4** | 50 | 150 | 30 | 1 | — |
| `pikeman` | Pikeman, 17th century | 4.50 | 13.3 | **18.7** | 25 | 3 | 20 | 1 | — |

<a id="fracen--городской-центр"></a>
<a id="городской-центр--fracen"></a>
### `fracen` — Town Hall

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `peaeng` | Peasant | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

<a id="fradip--дипломатический-центр"></a>
<a id="дипломатический-центр--fradip"></a>
### `fradip` — Diplomatic Center

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `archerdip` | Archer (mercenary) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| `archerturdip` | Turkish archer (mercenary) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| `cossacksichdip` | Sich Cossack (mercenary) | 2.50 | 24.0 | **33.6** | 0 | 60 | 0 | 1 | 60 |
| `dragoon18dip` | Dragoon, 18th century (mercenary) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| `grenadierdip` | Grenadier (mercenary) | 1.50 | 40.0 | **56.0** | 0 | 25 | 0 | 1 | 36 |
| `lightcavalrydip` | Light cavalry (mercenary) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| `lightinfantrydip` | Light Infantryman (mercenary) | 1.25 | 48.0 | **67.2** | 0 | 4 | 0 | 1 | — |
| `roundshierdip` | Roundshier (mercenary) | 1.50 | 40.0 | **56.0** | 0 | 12 | 0 | 1 | — |

<a id="frasta--конюшня"></a>
<a id="конюшня--frasta"></a>
### `frasta` — Stable

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cuirassier` | Cuirassier | 22.50 | 2.7 | **3.7** | 120 | 35 | 25 | 1 | 75 |
| `dragoon` | Dragoon, 17th century | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | 60 |
| `dragoon18fra` | Dragoon, 18th century | 15.00 | 4.0 | **5.6** | 50 | 30 | 6 | 1 | 45 |
| `hussar` | Hussar | 15.00 | 4.0 | **5.6** | 70 | 20 | 2 | 1 | 60 |
| `kingmusketeer` | King's Musketeer | 27.00 | 2.2 | **3.1** | 100 | 100 | 8 | 1 | 75 |
| `reiter` | Reiter | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | 75 |

<a id="fratem--собор"></a>
<a id="собор--fratem"></a>
### `fratem` — Cathedral

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `priest` | Priest | 20.00 | 3.0 | **4.2** | 60 | 25 | 0 | 1 | — |

[↑ to contents](#содержание)

<a id="hun--hungary-венгрия"></a>
<a id="венгрия"></a>
## Hungary (`hun`)
### `eurmil` — Mill

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

### `eurpor` — Shipyard

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `battleship` | Ship of the Line | 390.00 | 0.2 | **0.2** | 0 | 3200 | 700 | 1 | — |
| `ferry` | Ferry | 56.00 | 1.1 | **1.5** | 0 | 50 | 100 | 1 | — |
| `fishboat` | Boat | 40.00 | 1.5 | **2.1** | 0 | 0 | 0 | 1 | — |
| `frigate` | Frigate | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| `galley` | Galley | 50.00 | 1.2 | **1.7** | 0 | 900 | 800 | 1 | — |
| `yacht` | Yacht | 48.00 | 1.2 | **1.8** | 0 | 450 | 150 | 1 | — |

<a id="hunart--артиллерийское-депо"></a>
<a id="артиллерийское-депо--hunart"></a>
### `hunart` — Artillery Depot

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cannon` | Cannon | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| `howitzer` | Howitzer | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| `mortar` | Bombard | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| `multicannon` | Multi-barrelled Cannon | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

<a id="hunba2--казарма-18в"></a>
<a id="казарма-18в--hunba2"></a>
### `hunba2` — Barracks, 18th century

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer18` | Drummer, 18th century | 6.00 | 10.0 | **14.0** | 50 | 30 | 0 | 1 | — |
| `grenadierhun` | Grenadier | 6.50 | 9.2 | **12.9** | 90 | 80 | 40 | 1 | 36 |
| `musketeer18` | Musketeer, 18th century | 4.50 | 13.3 | **18.7** | 50 | 40 | 40 | 1 | — |
| `officer18` | Officer, 18th century | 6.00 | 10.0 | **14.0** | 50 | 200 | 10 | 1 | — |
| `pandurhun` | Szekely | 6.50 | 9.2 | **12.9** | 30 | 25 | 10 | 1 | — |
| `pikeman18` | Pikeman, 18th century | 1.25 | 48.0 | **67.2** | 30 | 2 | 0 | 1 | — |

<a id="hunbar--казарма-17в"></a>
<a id="казарма-17в--hunbar"></a>
### `hunbar` — Barracks, 17th century

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer` | Drummer, 17th century | 5.00 | 12.0 | **16.8** | 60 | 20 | 0 | 1 | — |
| `gauduk` | Hajduk | 4.50 | 13.3 | **18.7** | 35 | 4 | 4 | 1 | — |
| `officer` | Officer, 17th century | 10.00 | 6.0 | **8.4** | 50 | 150 | 30 | 1 | — |
| `pikeman` | Pikeman, 17th century | 4.50 | 13.3 | **18.7** | 25 | 3 | 20 | 1 | — |

<a id="huncen--городской-центр"></a>
<a id="городской-центр--huncen"></a>
### `huncen` — Town Hall

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `peapol` | Peasant | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

<a id="hundip--дипломатический-центр"></a>
<a id="дипломатический-центр--hundip"></a>
### `hundip` — Diplomatic Center

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `archerdip` | Archer (mercenary) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| `archerturdip` | Turkish archer (mercenary) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| `cossacksichdip` | Sich Cossack (mercenary) | 2.50 | 24.0 | **33.6** | 0 | 60 | 0 | 1 | 60 |
| `dragoon18dip` | Dragoon, 18th century (mercenary) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| `grenadierdip` | Grenadier (mercenary) | 1.50 | 40.0 | **56.0** | 0 | 25 | 0 | 1 | 36 |
| `lightcavalrydip` | Light cavalry (mercenary) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| `lightinfantrydip` | Light Infantryman (mercenary) | 1.25 | 48.0 | **67.2** | 0 | 4 | 0 | 1 | — |
| `roundshierdip` | Roundshier (mercenary) | 1.50 | 40.0 | **56.0** | 0 | 12 | 0 | 1 | — |

<a id="hunsta--конюшня"></a>
<a id="конюшня--hunsta"></a>
### `hunsta` — Stable

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cuirassier` | Cuirassier | 22.50 | 2.7 | **3.7** | 120 | 35 | 25 | 1 | 75 |
| `dragoon` | Dragoon, 17th century | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | 60 |
| `hussarhun` | Hussar | 21.00 | 2.9 | **4.0** | 100 | 30 | 2 | 1 | 60 |
| `lightcavalry` | Light cavalry | 21.00 | 2.9 | **4.0** | 90 | 50 | 6 | 1 | 60 |
| `reiter` | Reiter | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | 75 |

<a id="huntem--собор"></a>
<a id="собор--huntem"></a>
### `huntem` — Cathedral

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `priest` | Priest | 20.00 | 3.0 | **4.2** | 60 | 25 | 0 | 1 | — |

[↑ to contents](#содержание)

<a id="net--netherlands-нидерланды"></a>
<a id="нидерланды"></a>
## Netherlands (`net`)
### `eurmil` — Mill

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

### `eurpor` — Shipyard

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `battleship` | Ship of the Line | 390.00 | 0.2 | **0.2** | 0 | 3200 | 700 | 1 | — |
| `ferry` | Ferry | 56.00 | 1.1 | **1.5** | 0 | 50 | 100 | 1 | — |
| `fishboat` | Boat | 40.00 | 1.5 | **2.1** | 0 | 0 | 0 | 1 | — |
| `frigate` | Frigate | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| `galley` | Galley | 50.00 | 1.2 | **1.7** | 0 | 900 | 800 | 1 | — |
| `yacht` | Yacht | 48.00 | 1.2 | **1.8** | 0 | 450 | 150 | 1 | — |

<a id="netart--артиллерийское-депо"></a>
<a id="артиллерийское-депо--netart"></a>
### `netart` — Artillery Depot

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cannon` | Cannon | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| `howitzer` | Howitzer | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| `mortar` | Bombard | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| `multicannon` | Multi-barrelled Cannon | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

<a id="netba2--казарма-18в"></a>
<a id="казарма-18в--netba2"></a>
### `netba2` — Barracks, 18th century

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer18` | Drummer, 18th century | 6.00 | 10.0 | **14.0** | 50 | 30 | 0 | 1 | — |
| `grenadier` | Grenadier | 6.00 | 10.0 | **14.0** | 80 | 60 | 40 | 1 | 36 |
| `musketeer18` | Musketeer, 18th century | 4.50 | 13.3 | **18.7** | 50 | 40 | 40 | 1 | — |
| `officer18` | Officer, 18th century | 6.00 | 10.0 | **14.0** | 50 | 200 | 10 | 1 | — |
| `pikeman18` | Pikeman, 18th century | 1.25 | 48.0 | **67.2** | 30 | 2 | 0 | 1 | — |

<a id="netbar--казарма-17в"></a>
<a id="казарма-17в--netbar"></a>
### `netbar` — Barracks, 17th century

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer` | Drummer, 17th century | 5.00 | 12.0 | **16.8** | 60 | 20 | 0 | 1 | — |
| `musketeernet` | Musketeer, 17th century | 5.00 | 12.0 | **16.8** | 50 | 8 | 4 | 1 | — |
| `officer` | Officer, 17th century | 10.00 | 6.0 | **8.4** | 50 | 150 | 30 | 1 | — |
| `pikeman` | Pikeman, 17th century | 4.50 | 13.3 | **18.7** | 25 | 3 | 20 | 1 | — |

<a id="netcen--городской-центр"></a>
<a id="городской-центр--netcen"></a>
### `netcen` — Town Hall
| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `peaeng` | Peasant | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

<a id="netdip--дипломатический-центр"></a>
<a id="дипломатический-центр--netdip"></a>
### `netdip` — Diplomatic Center

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `archerdip` | Archer (mercenary) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| `archerturdip` | Turkish archer (mercenary) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| `cossacksichdip` | Sich Cossack (mercenary) | 2.50 | 24.0 | **33.6** | 0 | 60 | 0 | 1 | 60 |
| `dragoon18dip` | Dragoon, 18th century (mercenary) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| `grenadierdip` | Grenadier (mercenary) | 1.50 | 40.0 | **56.0** | 0 | 25 | 0 | 1 | 36 |
| `lightcavalrydip` | Light cavalry (mercenary) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| `lightinfantrydip` | Light Infantryman (mercenary) | 1.25 | 48.0 | **67.2** | 0 | 4 | 0 | 1 | — |
| `roundshierdip` | Roundshier (mercenary) | 1.50 | 40.0 | **56.0** | 0 | 12 | 0 | 1 | — |

<a id="netsta--конюшня"></a>
<a id="конюшня--netsta"></a>
### `netsta` — Stable

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cuirassier` | Cuirassier | 22.50 | 2.7 | **3.7** | 120 | 35 | 25 | 1 | 75 |
| `dragoon` | Dragoon, 17th century | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | 60 |
| `dragoon18net` | Dragoon, 18th century | 24.00 | 2.5 | **3.5** | 100 | 70 | 7 | 1 | 75 |
| `hussar` | Hussar | 15.00 | 4.0 | **5.6** | 70 | 20 | 2 | 1 | 60 |
| `reiter` | Reiter | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | 75 |

<a id="nettem--собор"></a>
<a id="собор--nettem"></a>
### `nettem` — Cathedral

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `priest` | Priest | 20.00 | 3.0 | **4.2** | 60 | 25 | 0 | 1 | — |

[↑ to contents](#содержание)

<a id="pie--piedmont-пьемонт"></a>
<a id="пьемонт"></a>
## Piedmont (`pie`)
<a id="eurmil--мельница"></a>
### `eurmil` — Mill

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

<a id="eurpor--порт"></a>
### `eurpor` — Shipyard

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `battleship` | Ship of the Line | 390.00 | 0.2 | **0.2** | 0 | 3200 | 700 | 1 | — |
| `ferry` | Ferry | 56.00 | 1.1 | **1.5** | 0 | 50 | 100 | 1 | — |
| `fishboat` | Boat | 40.00 | 1.5 | **2.1** | 0 | 0 | 0 | 1 | — |
| `frigate` | Frigate | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| `galley` | Galley | 50.00 | 1.2 | **1.7** | 0 | 900 | 800 | 1 | — |
| `yacht` | Yacht | 48.00 | 1.2 | **1.8** | 0 | 450 | 150 | 1 | — |

<a id="pieart--артиллерийское-депо"></a>
<a id="артиллерийское-депо--pieart"></a>
### `pieart` — Artillery Depot

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cannon` | Cannon | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| `howitzer` | Howitzer | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| `mortar` | Bombard | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| `multicannon` | Multi-barrelled Cannon | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

<a id="pieba2--казарма-18в"></a>
<a id="казарма-18в--pieba2"></a>
### `pieba2` — Barracks, 18th century

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer18` | Drummer, 18th century | 6.00 | 10.0 | **14.0** | 50 | 30 | 0 | 1 | — |
| `grenadier` | Grenadier | 6.00 | 10.0 | **14.0** | 80 | 60 | 40 | 1 | 36 |
| `musketeer18` | Musketeer, 18th century | 4.50 | 13.3 | **18.7** | 50 | 40 | 40 | 1 | — |
| `officer18` | Officer, 18th century | 6.00 | 10.0 | **14.0** | 50 | 200 | 10 | 1 | — |
| `pikeman18` | Pikeman, 18th century | 1.25 | 48.0 | **67.2** | 30 | 2 | 0 | 1 | — |

<a id="piebar--казарма-17в"></a>
<a id="казарма-17в--piebar"></a>
### `piebar` — Barracks, 17th century

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer` | Drummer, 17th century | 5.00 | 12.0 | **16.8** | 60 | 20 | 0 | 1 | — |
| `musketeer` | Musketeer, 17th century | 6.00 | 10.0 | **14.0** | 45 | 6 | 5 | 1 | — |
| `officer` | Officer, 17th century | 10.00 | 6.0 | **8.4** | 50 | 150 | 30 | 1 | — |
| `pikeman` | Pikeman, 17th century | 4.50 | 13.3 | **18.7** | 25 | 3 | 20 | 1 | — |

<a id="piecen--городской-центр"></a>
<a id="городской-центр--piecen"></a>
### `piecen` — Town Hall

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `peaspa` | Peasant | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

<a id="piedip--дипломатический-центр"></a>
<a id="дипломатический-центр--piedip"></a>
### `piedip` — Diplomatic Center

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `archerdip` | Archer (mercenary) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| `archerturdip` | Turkish archer (mercenary) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| `cossacksichdip` | Sich Cossack (mercenary) | 2.50 | 24.0 | **33.6** | 0 | 60 | 0 | 1 | 60 |
| `dragoon18dip` | Dragoon, 18th century (mercenary) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| `grenadierdip` | Grenadier (mercenary) | 1.50 | 40.0 | **56.0** | 0 | 25 | 0 | 1 | 36 |
| `lightcavalrydip` | Light cavalry (mercenary) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| `lightinfantrydip` | Light Infantryman (mercenary) | 1.25 | 48.0 | **67.2** | 0 | 4 | 0 | 1 | — |
| `roundshierdip` | Roundshier (mercenary) | 1.50 | 40.0 | **56.0** | 0 | 12 | 0 | 1 | — |

<a id="piesta--конюшня"></a>
<a id="конюшня--piesta"></a>
### `piesta` — Stable

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cuirassier` | Cuirassier | 22.50 | 2.7 | **3.7** | 120 | 35 | 25 | 1 | 75 |
| `dragoon` | Dragoon, 17th century | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | 60 |
| `dragoon18pie` | Dragoon, 18th century | 20.25 | 3.0 | **4.1** | 60 | 65 | 7 | 1 | 60 |
| `hussar` | Hussar | 15.00 | 4.0 | **5.6** | 70 | 20 | 2 | 1 | 60 |
| `reiter` | Reiter | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | 75 |

<a id="pietem--собор"></a>
<a id="собор--pietem"></a>
### `pietem` — Cathedral

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `padre` | Padre | 25.00 | 2.4 | **3.4** | 50 | 40 | 0 | 1 | — |

[↑ to contents](#содержание)

<a id="pol--poland-польша"></a>
<a id="польша"></a>
## Poland (`pol`)
<a id="eurmil--мельница"></a>
### `eurmil` — Mill

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

<a id="eurpor--порт"></a>
### `eurpor` — Shipyard

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `battleship` | Ship of the Line | 390.00 | 0.2 | **0.2** | 0 | 3200 | 700 | 1 | — |
| `ferry` | Ferry | 56.00 | 1.1 | **1.5** | 0 | 50 | 100 | 1 | — |
| `fishboat` | Boat | 40.00 | 1.5 | **2.1** | 0 | 0 | 0 | 1 | — |
| `frigate` | Frigate | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| `galley` | Galley | 50.00 | 1.2 | **1.7** | 0 | 900 | 800 | 1 | — |
| `yacht` | Yacht | 48.00 | 1.2 | **1.8** | 0 | 450 | 150 | 1 | — |

<a id="polart--артиллерийское-депо"></a>
<a id="артиллерийское-депо--polart"></a>
### `polart` — Artillery Depot

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cannon` | Cannon | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| `howitzer` | Howitzer | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| `mortar` | Bombard | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| `multicannon` | Multi-barrelled Cannon | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

<a id="polba2--казарма-18в"></a>
<a id="казарма-18в--polba2"></a>
### `polba2` — Barracks, 18th century

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer18` | Drummer, 18th century | 6.00 | 10.0 | **14.0** | 50 | 30 | 0 | 1 | — |
| `grenadier` | Grenadier | 6.00 | 10.0 | **14.0** | 80 | 60 | 40 | 1 | 36 |
| `musketeer18` | Musketeer, 18th century | 4.50 | 13.3 | **18.7** | 50 | 40 | 40 | 1 | — |
| `officer18` | Officer, 18th century | 6.00 | 10.0 | **14.0** | 50 | 200 | 10 | 1 | — |
| `pikeman18` | Pikeman, 18th century | 1.25 | 48.0 | **67.2** | 30 | 2 | 0 | 1 | — |

<a id="polbar--казарма-17в"></a>
<a id="казарма-17в--polbar"></a>
### `polbar` — Barracks, 17th century

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer` | Drummer, 17th century | 5.00 | 12.0 | **16.8** | 60 | 20 | 0 | 1 | — |
| `musketeerpol` | Musketeer, 17th century | 4.50 | 13.3 | **18.7** | 40 | 3 | 3 | 1 | — |
| `officer` | Officer, 17th century | 10.00 | 6.0 | **8.4** | 50 | 150 | 30 | 1 | — |
| `pikemanpol` | Pikeman, 17th century | 3.00 | 20.0 | **28.0** | 25 | 1 | 0 | 1 | — |

<a id="polcen--городской-центр"></a>
<a id="городской-центр--polcen"></a>
### `polcen` — Town Hall

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `peapol` | Peasant | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

<a id="poldip--дипломатический-центр"></a>
<a id="дипломатический-центр--poldip"></a>
### `poldip` — Diplomatic Center

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `archerdip` | Archer (mercenary) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| `archerturdip` | Turkish archer (mercenary) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| `cossacksichdip` | Sich Cossack (mercenary) | 2.50 | 24.0 | **33.6** | 0 | 60 | 0 | 1 | 60 |
| `dragoon18dip` | Dragoon, 18th century (mercenary) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| `grenadierdip` | Grenadier (mercenary) | 1.50 | 40.0 | **56.0** | 0 | 25 | 0 | 1 | 36 |
| `lightcavalrydip` | Light cavalry (mercenary) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| `lightinfantrydip` | Light Infantryman (mercenary) | 1.25 | 48.0 | **67.2** | 0 | 4 | 0 | 1 | — |
| `roundshierdip` | Roundshier (mercenary) | 1.50 | 40.0 | **56.0** | 0 | 12 | 0 | 1 | — |

<a id="polsta--конюшня"></a>
<a id="конюшня--polsta"></a>
### `polsta` — Stable

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cuirassier` | Cuirassier | 22.50 | 2.7 | **3.7** | 120 | 35 | 25 | 1 | 75 |
| `dragoon` | Dragoon, 17th century | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | 60 |
| `dragoon18` | Dragoon, 18th century | 22.50 | 2.7 | **3.7** | 70 | 60 | 7 | 1 | 60 |
| `dragoonpol` | Pospolite ruszenie | 13.50 | 4.4 | **6.2** | 70 | 5 | 4 | 1 | 60 |
| `hussar` | Hussar | 15.00 | 4.0 | **5.6** | 70 | 20 | 2 | 1 | 60 |
| `reiterpol` | Light Reiter | 8.25 | 7.3 | **10.2** | 60 | 5 | 2 | 1 | 45 |
| `wingedhussar` | Winged Hussar | 26.00 | 2.3 | **3.2** | 130 | 30 | 25 | 1 | 75 |

<a id="poltem--собор"></a>
<a id="собор--poltem"></a>
### `poltem` — Cathedral

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `priest` | Priest | 20.00 | 3.0 | **4.2** | 60 | 25 | 0 | 1 | — |

[↑ to contents](#содержание)

<a id="por--portugal-португалия"></a>
<a id="португалия"></a>
## Portugal (`por`)
<a id="eurmil--мельница"></a>
### `eurmil` — Mill

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

<a id="porart--артиллерийское-депо"></a>
<a id="артиллерийское-депо--porart"></a>
### `porart` — Artillery Depot

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cannon` | Cannon | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| `howitzer` | Howitzer | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| `mortar` | Bombard | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| `multicannon` | Multi-barrelled Cannon | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

<a id="porba2--казарма-18в"></a>
<a id="казарма-18в--porba2"></a>
### `porba2` — Barracks, 18th century

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer18` | Drummer, 18th century | 6.00 | 10.0 | **14.0** | 50 | 30 | 0 | 1 | — |
| `grenadier` | Grenadier | 6.00 | 10.0 | **14.0** | 80 | 60 | 40 | 1 | 36 |
| `jagerpor` | Volunteer | 2.25 | 26.7 | **37.3** | 30 | 2 | 5 | 1 | — |
| `musketeer18` | Musketeer, 18th century | 4.50 | 13.3 | **18.7** | 50 | 40 | 40 | 1 | — |
| `officer18` | Officer, 18th century | 6.00 | 10.0 | **14.0** | 50 | 200 | 10 | 1 | — |
| `pikeman18` | Pikeman, 18th century | 1.25 | 48.0 | **67.2** | 30 | 2 | 0 | 1 | — |

<a id="porbar--казарма-17в"></a>
<a id="казарма-17в--porbar"></a>
### `porbar` — Barracks, 17th century

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer` | Drummer, 17th century | 5.00 | 12.0 | **16.8** | 60 | 20 | 0 | 1 | — |
| `musketeer` | Musketeer, 17th century | 6.00 | 10.0 | **14.0** | 45 | 6 | 5 | 1 | — |
| `officer` | Officer, 17th century | 10.00 | 6.0 | **8.4** | 50 | 150 | 30 | 1 | — |
| `pikemanpor` | Pikeman, 17th century | 4.00 | 15.0 | **21.0** | 40 | 4 | 5 | 1 | — |

<a id="porcen--городской-центр"></a>
<a id="городской-центр--porcen"></a>
### `porcen` — Town Hall

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `peaspa` | Peasant | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

<a id="pordip--дипломатический-центр"></a>
<a id="дипломатический-центр--pordip"></a>
### `pordip` — Diplomatic Center

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `archerdip` | Archer (mercenary) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| `archerturdip` | Turkish archer (mercenary) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| `cossacksichdip` | Sich Cossack (mercenary) | 2.50 | 24.0 | **33.6** | 0 | 60 | 0 | 1 | 60 |
| `dragoon18dip` | Dragoon, 18th century (mercenary) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| `grenadierdip` | Grenadier (mercenary) | 1.50 | 40.0 | **56.0** | 0 | 25 | 0 | 1 | 36 |
| `lightcavalrydip` | Light cavalry (mercenary) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| `lightinfantrydip` | Light Infantryman (mercenary) | 1.25 | 48.0 | **67.2** | 0 | 4 | 0 | 1 | — |
| `roundshierdip` | Roundshier (mercenary) | 1.50 | 40.0 | **56.0** | 0 | 12 | 0 | 1 | — |

<a id="porpor--порт"></a>
<a id="порт--porpor"></a>
### `porpor` — Shipyard

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `battleship` | Ship of the Line | 390.00 | 0.2 | **0.2** | 0 | 3200 | 700 | 1 | — |
| `ferry` | Ferry | 56.00 | 1.1 | **1.5** | 0 | 50 | 100 | 1 | — |
| `fishboat` | Boat | 40.00 | 1.5 | **2.1** | 0 | 0 | 0 | 1 | — |
| `frigate` | Frigate | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| `galley` | Galley | 50.00 | 1.2 | **1.7** | 0 | 900 | 800 | 1 | — |
| `yacht` | Yacht | 48.00 | 1.2 | **1.8** | 0 | 450 | 150 | 1 | — |

<a id="porsta--конюшня"></a>
<a id="конюшня--porsta"></a>
### `porsta` — Stable

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cuirassier` | Cuirassier | 22.50 | 2.7 | **3.7** | 120 | 35 | 25 | 1 | 75 |
| `dragoon` | Dragoon, 17th century | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | 60 |
| `dragoon18` | Dragoon, 18th century | 22.50 | 2.7 | **3.7** | 70 | 60 | 7 | 1 | 60 |
| `hussar` | Hussar | 15.00 | 4.0 | **5.6** | 70 | 20 | 2 | 1 | 60 |
| `reiter` | Reiter | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | 75 |

<a id="portem--собор"></a>
<a id="собор--portem"></a>
### `portem` — Cathedral

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `priest` | Priest | 20.00 | 3.0 | **4.2** | 60 | 25 | 0 | 1 | — |

[↑ to contents](#содержание)

<a id="pru--prussia-пруссия"></a>
<a id="пруссия"></a>
## Prussia (`pru`)
<a id="eurmil--мельница"></a>
### `eurmil` — Mill

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

<a id="eurpor--порт"></a>
### `eurpor` — Shipyard

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `battleship` | Ship of the Line | 390.00 | 0.2 | **0.2** | 0 | 3200 | 700 | 1 | — |
| `ferry` | Ferry | 56.00 | 1.1 | **1.5** | 0 | 50 | 100 | 1 | — |
| `fishboat` | Boat | 40.00 | 1.5 | **2.1** | 0 | 0 | 0 | 1 | — |
| `frigate` | Frigate | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| `galley` | Galley | 50.00 | 1.2 | **1.7** | 0 | 900 | 800 | 1 | — |
| `yacht` | Yacht | 48.00 | 1.2 | **1.8** | 0 | 450 | 150 | 1 | — |

<a id="pruart--артиллерийское-депо"></a>
<a id="артиллерийское-депо--pruart"></a>
### `pruart` — Artillery Depot

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cannon` | Cannon | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| `howitzer` | Howitzer | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| `mortar` | Bombard | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| `multicannon` | Multi-barrelled Cannon | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

<a id="pruba2--казарма-18в"></a>
<a id="казарма-18в--pruba2"></a>
### `pruba2` — Barracks, 18th century

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer18` | Drummer, 18th century | 6.00 | 10.0 | **14.0** | 50 | 30 | 0 | 1 | — |
| `grenadier` | Grenadier | 6.00 | 10.0 | **14.0** | 80 | 60 | 40 | 1 | 36 |
| `grenadierpru` | Grenadier | 7.00 | 8.6 | **12.0** | 90 | 100 | 45 | 1 | 36 |
| `musketeer18pru` | Musketeer, 18th century | 6.00 | 10.0 | **14.0** | 70 | 80 | 40 | 1 | — |
| `officer18` | Officer, 18th century | 6.00 | 10.0 | **14.0** | 50 | 200 | 10 | 1 | — |
| `pikeman18` | Pikeman, 18th century | 1.25 | 48.0 | **67.2** | 30 | 2 | 0 | 1 | — |

<a id="prubar--казарма-17в"></a>
<a id="казарма-17в--prubar"></a>
### `prubar` — Barracks, 17th century

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer` | Drummer, 17th century | 5.00 | 12.0 | **16.8** | 60 | 20 | 0 | 1 | — |
| `musketeer` | Musketeer, 17th century | 6.00 | 10.0 | **14.0** | 45 | 6 | 5 | 1 | — |
| `officer` | Officer, 17th century | 10.00 | 6.0 | **8.4** | 50 | 150 | 30 | 1 | — |
| `pikeman` | Pikeman, 17th century | 4.50 | 13.3 | **18.7** | 25 | 3 | 20 | 1 | — |

<a id="prucen--городской-центр"></a>
<a id="городской-центр--prucen"></a>
### `prucen` — Town Hall

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `peaaus` | Peasant | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

<a id="prudip--дипломатический-центр"></a>
<a id="дипломатический-центр--prudip"></a>
### `prudip` — Diplomatic Center

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `archerdip` | Archer (mercenary) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| `archerturdip` | Turkish archer (mercenary) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| `cossacksichdip` | Sich Cossack (mercenary) | 2.50 | 24.0 | **33.6** | 0 | 60 | 0 | 1 | 60 |
| `dragoon18dip` | Dragoon, 18th century (mercenary) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| `grenadierdip` | Grenadier (mercenary) | 1.50 | 40.0 | **56.0** | 0 | 25 | 0 | 1 | 36 |
| `lightcavalrydip` | Light cavalry (mercenary) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| `lightinfantrydip` | Light Infantryman (mercenary) | 1.25 | 48.0 | **67.2** | 0 | 4 | 0 | 1 | — |
| `roundshierdip` | Roundshier (mercenary) | 1.50 | 40.0 | **56.0** | 0 | 12 | 0 | 1 | — |

<a id="prusta--конюшня"></a>
<a id="конюшня--prusta"></a>
### `prusta` — Stable

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cuirassier` | Cuirassier | 22.50 | 2.7 | **3.7** | 120 | 35 | 25 | 1 | 75 |
| `dragoon` | Dragoon, 17th century | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | 60 |
| `dragoon18` | Dragoon, 18th century | 22.50 | 2.7 | **3.7** | 70 | 60 | 7 | 1 | 60 |
| `hussarpru` | Hussar | 11.25 | 5.3 | **7.5** | 80 | 15 | 2 | 1 | 60 |
| `reiter` | Reiter | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | 75 |

<a id="prutem--собор"></a>
<a id="собор--prutem"></a>
### `prutem` — Cathedral

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `priest` | Priest | 20.00 | 3.0 | **4.2** | 60 | 25 | 0 | 1 | — |

[↑ to contents](#содержание)

<a id="rus--russia-россия"></a>
<a id="россия"></a>
## Russia (`rus`)
<a id="rusart--артиллерийское-депо"></a>
<a id="артиллерийское-депо--rusart"></a>
### `rusart` — Artillery Depot

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cannon` | Cannon | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| `howitzer` | Howitzer | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| `mortar` | Bombard | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| `multicannon` | Multi-barrelled Cannon | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

<a id="rusba2--казарма-18в"></a>
<a id="казарма-18в--rusba2"></a>
### `rusba2` — Barracks, 18th century

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer18` | Drummer, 18th century | 6.00 | 10.0 | **14.0** | 90 | 15 | 0 | 1 | — |
| `grenadier` | Grenadier | 6.00 | 10.0 | **14.0** | 80 | 60 | 40 | 1 | 36 |
| `musketeer18` | Musketeer, 18th century | 4.50 | 13.3 | **18.7** | 50 | 40 | 40 | 1 | — |
| `officer18` | Officer, 18th century | 6.00 | 10.0 | **14.0** | 50 | 200 | 10 | 1 | — |
| `pikeman18` | Pikeman, 18th century | 1.25 | 48.0 | **67.2** | 30 | 2 | 0 | 1 | — |

<a id="rusbar--стрелецкая-казарма"></a>
<a id="стрелецкая-казарма--rusbar"></a>
### `rusbar` — Strelets Barracks

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummerrus` | Drummer, 17th century | 6.00 | 10.0 | **14.0** | 90 | 15 | 0 | 1 | — |
| `officerrus` | Commander | 12.50 | 4.8 | **6.7** | 100 | 125 | 5 | 1 | — |
| `pikemanrus` | Spearman | 5.50 | 10.9 | **15.3** | 45 | 4 | 15 | 1 | — |
| `strelet` | Strelets | 8.50 | 7.1 | **9.9** | 70 | 7 | 9 | 1 | — |

<a id="ruscen--городской-центр"></a>
<a id="городской-центр--ruscen"></a>
### `ruscen` — Town Hall

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `pearus` | Serf | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 26 |

<a id="rusdip--дипломатический-центр"></a>
<a id="дипломатический-центр--rusdip"></a>
### `rusdip` — Diplomatic Center

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `archerdip` | Archer (mercenary) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| `archerturdip` | Turkish archer (mercenary) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| `cossacksichdip` | Sich Cossack (mercenary) | 2.50 | 24.0 | **33.6** | 0 | 60 | 0 | 1 | 60 |
| `dragoon18dip` | Dragoon, 18th century (mercenary) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| `grenadierdip` | Grenadier (mercenary) | 1.50 | 40.0 | **56.0** | 0 | 25 | 0 | 1 | 36 |
| `lightcavalrydip` | Light cavalry (mercenary) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| `lightinfantrydip` | Light Infantryman (mercenary) | 1.25 | 48.0 | **67.2** | 0 | 4 | 0 | 1 | — |
| `roundshierdip` | Roundshier (mercenary) | 1.50 | 40.0 | **56.0** | 0 | 12 | 0 | 1 | — |

<a id="rusmil--мельница"></a>
<a id="мельница--rusmil"></a>
### `rusmil` — Mill

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

<a id="ruspor--порт"></a>
<a id="порт--ruspor"></a>
### `ruspor` — Shipyard

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `battleship` | Ship of the Line | 390.00 | 0.2 | **0.2** | 0 | 3200 | 700 | 1 | — |
| `ferry` | Ferry | 56.00 | 1.1 | **1.5** | 0 | 50 | 100 | 1 | — |
| `fishboat` | Boat | 40.00 | 1.5 | **2.1** | 0 | 0 | 0 | 1 | — |
| `frigate` | Frigate | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| `galley` | Galley | 50.00 | 1.2 | **1.7** | 0 | 900 | 800 | 1 | — |
| `yacht` | Yacht | 48.00 | 1.2 | **1.8** | 0 | 450 | 150 | 1 | — |

<a id="russta--конюшня"></a>
<a id="конюшня--russta"></a>
### `russta` — Stable

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cossackdon` | Don Cossack | 13.50 | 4.4 | **6.2** | 100 | 0 | 0 | 1 | 60 |
| `cuirassier` | Cuirassier | 22.50 | 2.7 | **3.7** | 120 | 35 | 25 | 1 | 75 |
| `dragoon18` | Dragoon, 18th century | 22.50 | 2.7 | **3.7** | 70 | 60 | 7 | 1 | 60 |
| `hussar` | Hussar | 15.00 | 4.0 | **5.6** | 70 | 20 | 2 | 1 | 60 |
| `vityaz` | Vityaz | 25.50 | 2.4 | **3.3** | 160 | 13 | 25 | 1 | 75 |

<a id="rustem--православная-церковь"></a>
<a id="православная-церковь--rustem"></a>
### `rustem` — Orthodox Cathedral

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `pope` | Pope | 20.00 | 3.0 | **4.2** | 40 | 20 | 0 | 1 | — |

[↑ to contents](#содержание)

<a id="sax--saxony-саксония"></a>
<a id="саксония"></a>
## Saxony (`sax`)
<a id="eurmil--мельница"></a>
### `eurmil` — Mill

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

<a id="eurpor--порт"></a>
### `eurpor` — Shipyard

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `battleship` | Ship of the Line | 390.00 | 0.2 | **0.2** | 0 | 3200 | 700 | 1 | — |
| `ferry` | Ferry | 56.00 | 1.1 | **1.5** | 0 | 50 | 100 | 1 | — |
| `fishboat` | Boat | 40.00 | 1.5 | **2.1** | 0 | 0 | 0 | 1 | — |
| `frigate` | Frigate | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| `galley` | Galley | 50.00 | 1.2 | **1.7** | 0 | 900 | 800 | 1 | — |
| `yacht` | Yacht | 48.00 | 1.2 | **1.8** | 0 | 450 | 150 | 1 | — |

<a id="saxart--артиллерийское-депо"></a>
<a id="артиллерийское-депо--saxart"></a>
### `saxart` — Artillery Depot

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cannon` | Cannon | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| `howitzer` | Howitzer | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| `mortar` | Bombard | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| `multicannon` | Multi-barrelled Cannon | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

<a id="saxba2--казарма-18в"></a>
<a id="казарма-18в--saxba2"></a>
### `saxba2` — Barracks, 18th century

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer18` | Drummer, 18th century | 6.00 | 10.0 | **14.0** | 50 | 30 | 0 | 1 | — |
| `grenadiersax` | Grenadier | 6.00 | 10.0 | **14.0** | 50 | 60 | 40 | 1 | 30 |
| `musketeer18sax` | Musketeer, 18th century | 4.50 | 13.3 | **18.7** | 40 | 45 | 40 | 1 | — |
| `officer18` | Officer, 18th century | 6.00 | 10.0 | **14.0** | 50 | 200 | 10 | 1 | — |
| `pikeman18` | Pikeman, 18th century | 1.25 | 48.0 | **67.2** | 30 | 2 | 0 | 1 | — |

<a id="saxbar--казарма-17в"></a>
<a id="казарма-17в--saxbar"></a>
### `saxbar` — Barracks, 17th century

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer` | Drummer, 17th century | 5.00 | 12.0 | **16.8** | 60 | 20 | 0 | 1 | — |
| `musketeer` | Musketeer, 17th century | 6.00 | 10.0 | **14.0** | 45 | 6 | 5 | 1 | — |
| `officer` | Officer, 17th century | 10.00 | 6.0 | **8.4** | 50 | 150 | 30 | 1 | — |
| `pikeman` | Pikeman, 17th century | 4.50 | 13.3 | **18.7** | 25 | 3 | 20 | 1 | — |

<a id="saxcen--городской-центр"></a>
<a id="городской-центр--saxcen"></a>
### `saxcen` — Town Hall

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `peaaus` | Peasant | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

<a id="saxdip--дипломатический-центр"></a>
<a id="дипломатический-центр--saxdip"></a>
### `saxdip` — Diplomatic Center

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `archerdip` | Archer (mercenary) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| `archerturdip` | Turkish archer (mercenary) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| `cossacksichdip` | Sich Cossack (mercenary) | 2.50 | 24.0 | **33.6** | 0 | 60 | 0 | 1 | 60 |
| `dragoon18dip` | Dragoon, 18th century (mercenary) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| `grenadierdip` | Grenadier (mercenary) | 1.50 | 40.0 | **56.0** | 0 | 25 | 0 | 1 | 36 |
| `lightcavalrydip` | Light cavalry (mercenary) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| `lightinfantrydip` | Light Infantryman (mercenary) | 1.25 | 48.0 | **67.2** | 0 | 4 | 0 | 1 | — |
| `roundshierdip` | Roundshier (mercenary) | 1.50 | 40.0 | **56.0** | 0 | 12 | 0 | 1 | — |

<a id="saxsta--конюшня"></a>
<a id="конюшня--saxsta"></a>
### `saxsta` — Stable

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cuirassier` | Cuirassier | 22.50 | 2.7 | **3.7** | 120 | 35 | 25 | 1 | 75 |
| `dragoon` | Dragoon, 17th century | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | 60 |
| `dragoon18` | Dragoon, 18th century | 22.50 | 2.7 | **3.7** | 70 | 60 | 7 | 1 | 60 |
| `guardcavalrysax` | Cavalry Guard | 24.00 | 2.5 | **3.5** | 140 | 50 | 20 | 1 | 75 |
| `hussar` | Hussar | 15.00 | 4.0 | **5.6** | 70 | 20 | 2 | 1 | 60 |
| `reiter` | Reiter | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | 75 |

<a id="saxtem--собор"></a>
<a id="собор--saxtem"></a>
### `saxtem` — Cathedral

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `priest` | Priest | 20.00 | 3.0 | **4.2** | 60 | 25 | 0 | 1 | — |

[↑ to contents](#содержание)

<a id="sco--scotland-шотландия"></a>
<a id="шотландия"></a>
## Scotland (`sco`)
<a id="eurmil--мельница"></a>
### `eurmil` — Mill

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

<a id="eurpor--порт"></a>
### `eurpor` — Shipyard

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `battleship` | Ship of the Line | 390.00 | 0.2 | **0.2** | 0 | 3200 | 700 | 1 | — |
| `ferry` | Ferry | 56.00 | 1.1 | **1.5** | 0 | 50 | 100 | 1 | — |
| `fishboat` | Boat | 40.00 | 1.5 | **2.1** | 0 | 0 | 0 | 1 | — |
| `frigate` | Frigate | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| `yacht` | Yacht | 48.00 | 1.2 | **1.8** | 0 | 450 | 150 | 1 | — |

<a id="scoart--артиллерийское-депо"></a>
<a id="артиллерийское-депо--scoart"></a>
### `scoart` — Artillery Depot

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cannon` | Cannon | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| `framegun` | Frame gun | 50.00 | 1.2 | **1.7** | 0 | 300 | 150 | 1 | — |
| `howitzer` | Howitzer | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| `mortar` | Bombard | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |

<a id="scoba2--замок"></a>
<a id="замок--scoba2"></a>
### `scoba2` — Castle

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `archersco` | Bow Clansman | 6.00 | 10.0 | **14.0** | 80 | 7 | 0 | 1 | 39 |
| `swordsmansco` | Sword Clansman | 7.00 | 8.6 | **12.0** | 110 | 10 | 0 | 1 | 45 |

<a id="scobar--казарма-17в"></a>
<a id="казарма-17в--scobar"></a>
### `scobar` — Barracks, 17th century

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `bagpiper` | Bagpiper | 7.00 | 8.6 | **12.0** | 120 | 20 | 0 | 1 | — |
| `musketeersco` | Covenanter musketeer | 7.00 | 8.6 | **12.0** | 55 | 8 | 7 | 1 | — |
| `officersco` | Officer | 10.00 | 6.0 | **8.4** | 130 | 130 | 10 | 1 | — |
| `pikemansco` | Covenanter pikeman | 4.00 | 15.0 | **21.0** | 35 | 2 | 0 | 1 | — |

<a id="scocen--городской-центр"></a>
<a id="городской-центр--scocen"></a>
### `scocen` — Town Hall

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `peasco` | Peasant | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

<a id="scodip--дипломатический-центр"></a>
<a id="дипломатический-центр--scodip"></a>
### `scodip` — Diplomatic Center

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `archerdip` | Archer (mercenary) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | 39 |
| `archerturdip` | Turkish archer (mercenary) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | 39 |
| `cossacksichdip` | Sich Cossack (mercenary) | 2.50 | 24.0 | **33.6** | 0 | 60 | 0 | 1 | 60 |
| `dragoon18dip` | Dragoon, 18th century (mercenary) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| `grenadierdip` | Grenadier (mercenary) | 1.50 | 40.0 | **56.0** | 0 | 25 | 0 | 1 | 36 |
| `lightcavalrydip` | Light cavalry (mercenary) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| `lightinfantrydip` | Light Infantryman (mercenary) | 1.25 | 48.0 | **67.2** | 0 | 4 | 0 | 1 | — |
| `roundshierdip` | Roundshier (mercenary) | 1.50 | 40.0 | **56.0** | 0 | 12 | 0 | 1 | 45 |

<a id="scosta--конюшня"></a>
<a id="конюшня--scosta"></a>
### `scosta` — Stable

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `lancersco` | Lancer | 21.00 | 2.9 | **4.0** | 120 | 6 | 0 | 1 | 60 |
| `raidersco` | Raider | 22.50 | 2.7 | **3.7** | 130 | 8 | 2 | 1 | 75 |

<a id="scotem--собор"></a>
<a id="собор--scotem"></a>
### `scotem` — Cathedral

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `priest` | Priest | 20.00 | 3.0 | **4.2** | 60 | 25 | 0 | 1 | — |

[↑ to contents](#содержание)

<a id="spa--spain-испания"></a>
<a id="испания"></a>
## Spain (`spa`)
<a id="eurmil--мельница"></a>
### `eurmil` — Mill

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

<a id="eurpor--порт"></a>
### `eurpor` — Shipyard

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `battleship` | Ship of the Line | 390.00 | 0.2 | **0.2** | 0 | 3200 | 700 | 1 | — |
| `ferry` | Ferry | 56.00 | 1.1 | **1.5** | 0 | 50 | 100 | 1 | — |
| `fishboat` | Boat | 40.00 | 1.5 | **2.1** | 0 | 0 | 0 | 1 | — |
| `frigate` | Frigate | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| `galley` | Galley | 50.00 | 1.2 | **1.7** | 0 | 900 | 800 | 1 | — |
| `yacht` | Yacht | 48.00 | 1.2 | **1.8** | 0 | 450 | 150 | 1 | — |

<a id="spaart--артиллерийское-депо"></a>
<a id="артиллерийское-депо--spaart"></a>
### `spaart` — Artillery Depot

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cannon` | Cannon | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| `howitzer` | Howitzer | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| `mortar` | Bombard | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| `multicannon` | Multi-barrelled Cannon | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

<a id="spaba2--казарма-18в"></a>
<a id="казарма-18в--spaba2"></a>
### `spaba2` — Barracks, 18th century

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer18` | Drummer, 18th century | 6.00 | 10.0 | **14.0** | 50 | 30 | 0 | 1 | — |
| `grenadier` | Grenadier | 6.00 | 10.0 | **14.0** | 80 | 60 | 40 | 1 | 36 |
| `musketeer18` | Musketeer, 18th century | 4.50 | 13.3 | **18.7** | 50 | 40 | 40 | 1 | — |
| `officer18` | Officer, 18th century | 6.00 | 10.0 | **14.0** | 50 | 200 | 10 | 1 | — |
| `pikeman18` | Pikeman, 18th century | 1.25 | 48.0 | **67.2** | 30 | 2 | 0 | 1 | — |

<a id="spabar--казарма-17в"></a>
<a id="казарма-17в--spabar"></a>
### `spabar` — Barracks, 17th century

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer` | Drummer, 17th century | 5.00 | 12.0 | **16.8** | 60 | 20 | 0 | 1 | — |
| `musketeerspa` | Musketeer, 17th century | 7.50 | 8.0 | **11.2** | 40 | 12 | 20 | 1 | — |
| `officer` | Officer, 17th century | 10.00 | 6.0 | **8.4** | 50 | 150 | 30 | 1 | — |
| `pikeman` | Pikeman, 17th century | 5.50 | 10.9 | **15.3** | 35 | 7 | 30 | 1 | — |
| `pikemanspa` | Coselete | 5.50 | 10.9 | **15.3** | 35 | 7 | 30 | 1 | — |

<a id="spacen--городской-центр"></a>
<a id="городской-центр--spacen"></a>
### `spacen` — Town Hall

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `peaspa` | Peasant | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

<a id="spadip--дипломатический-центр"></a>
<a id="дипломатический-центр--spadip"></a>
### `spadip` — Diplomatic Center

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `archerdip` | Archer (mercenary) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| `archerturdip` | Turkish archer (mercenary) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| `cossacksichdip` | Sich Cossack (mercenary) | 2.50 | 24.0 | **33.6** | 0 | 60 | 0 | 1 | 60 |
| `dragoon18dip` | Dragoon, 18th century (mercenary) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| `grenadierdip` | Grenadier (mercenary) | 1.50 | 40.0 | **56.0** | 0 | 25 | 0 | 1 | 36 |
| `lightcavalrydip` | Light cavalry (mercenary) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| `lightinfantrydip` | Light Infantryman (mercenary) | 1.25 | 48.0 | **67.2** | 0 | 4 | 0 | 1 | — |
| `roundshierdip` | Roundshier (mercenary) | 1.50 | 40.0 | **56.0** | 0 | 12 | 0 | 1 | — |

<a id="spasta--конюшня"></a>
<a id="конюшня--spasta"></a>
### `spasta` — Stable

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cuirassier` | Cuirassier | 22.50 | 2.7 | **3.7** | 120 | 35 | 25 | 1 | 75 |
| `dragoon` | Dragoon, 17th century | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | 60 |
| `dragoon18` | Dragoon, 18th century | 22.50 | 2.7 | **3.7** | 70 | 60 | 7 | 1 | 60 |
| `hussar` | Hussar | 15.00 | 4.0 | **5.6** | 70 | 20 | 2 | 1 | 60 |
| `reiter` | Reiter | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | 75 |

<a id="spatem--собор"></a>
<a id="собор--spatem"></a>
### `spatem` — Cathedral

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `priest` | Priest | 20.00 | 3.0 | **4.2** | 60 | 25 | 0 | 1 | — |

[↑ to contents](#содержание)

<a id="swe--sweden-швеция"></a>
<a id="швеция"></a>
## Sweden (`swe`)
### `eurmil` — Mill

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

### `eurpor` — Shipyard

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `battleship` | Ship of the Line | 390.00 | 0.2 | **0.2** | 0 | 3200 | 700 | 1 | — |
| `ferry` | Ferry | 56.00 | 1.1 | **1.5** | 0 | 50 | 100 | 1 | — |
| `fishboat` | Boat | 40.00 | 1.5 | **2.1** | 0 | 0 | 0 | 1 | — |
| `frigate` | Frigate | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| `galley` | Galley | 50.00 | 1.2 | **1.7** | 0 | 900 | 800 | 1 | — |
| `yacht` | Yacht | 48.00 | 1.2 | **1.8** | 0 | 450 | 150 | 1 | — |
<a id="sweart--артиллерийское-депо"></a>
<a id="артиллерийское-депо--sweart"></a>
### `sweart` — Artillery Depot

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cannon` | Cannon | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| `howitzer` | Howitzer | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| `mortar` | Bombard | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| `multicannon` | Multi-barrelled Cannon | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

<a id="sweba2--казарма-18в"></a>
<a id="казарма-18в--sweba2"></a>
### `sweba2` — Barracks, 18th century

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer18` | Drummer, 18th century | 6.00 | 10.0 | **14.0** | 50 | 30 | 0 | 1 | — |
| `grenadier` | Grenadier | 6.00 | 10.0 | **14.0** | 80 | 60 | 40 | 1 | 36 |
| `musketeer18` | Musketeer, 18th century | 4.50 | 13.3 | **18.7** | 50 | 40 | 40 | 1 | — |
| `officer18` | Officer, 18th century | 6.00 | 10.0 | **14.0** | 50 | 200 | 10 | 1 | — |
| `pikeman18swe` | Pikeman, 18th century | 1.50 | 40.0 | **56.0** | 40 | 3 | 0 | 1 | — |

<a id="swebar--казарма-17в"></a>
<a id="казарма-17в--swebar"></a>
### `swebar` — Barracks, 17th century

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer` | Drummer, 17th century | 5.00 | 12.0 | **16.8** | 60 | 20 | 0 | 1 | — |
| `musketeer` | Musketeer, 17th century | 6.00 | 10.0 | **14.0** | 45 | 6 | 5 | 1 | — |
| `officer` | Officer, 17th century | 10.00 | 6.0 | **8.4** | 50 | 150 | 30 | 1 | — |
| `pikeman` | Pikeman, 17th century | 4.50 | 13.3 | **18.7** | 25 | 3 | 20 | 1 | — |

<a id="swecen--городской-центр"></a>
<a id="городской-центр--swecen"></a>
### `swecen` — Town Hall

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `peaeng` | Peasant | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

<a id="swedip--дипломатический-центр"></a>
<a id="дипломатический-центр--swedip"></a>
### `swedip` — Diplomatic Center

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `archerdip` | Archer (mercenary) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| `archerturdip` | Turkish archer (mercenary) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| `cossacksichdip` | Sich Cossack (mercenary) | 2.50 | 24.0 | **33.6** | 0 | 60 | 0 | 1 | 60 |
| `dragoon18dip` | Dragoon, 18th century (mercenary) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| `grenadierdip` | Grenadier (mercenary) | 1.50 | 40.0 | **56.0** | 0 | 25 | 0 | 1 | 36 |
| `lightcavalrydip` | Light cavalry (mercenary) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| `lightinfantrydip` | Light Infantryman (mercenary) | 1.25 | 48.0 | **67.2** | 0 | 4 | 0 | 1 | — |
| `roundshierdip` | Roundshier (mercenary) | 1.50 | 40.0 | **56.0** | 0 | 12 | 0 | 1 | — |

<a id="swesta--конюшня"></a>
<a id="конюшня--swesta"></a>
### `swesta` — Stable

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cuirassier` | Cuirassier | 22.50 | 2.7 | **3.7** | 120 | 35 | 25 | 1 | 75 |
| `dragoon` | Dragoon, 17th century | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | 60 |
| `dragoon18` | Dragoon, 18th century | 22.50 | 2.7 | **3.7** | 70 | 60 | 7 | 1 | 60 |
| `hackapell` | Hakkapeliitta | 18.00 | 3.3 | **4.7** | 80 | 7 | 2 | 1 | 60 |
| `hussar` | Hussar | 15.00 | 4.0 | **5.6** | 70 | 20 | 2 | 1 | 60 |
| `reiterswe` | Swedish Reiter | 22.50 | 2.7 | **3.7** | 130 | 7 | 20 | 1 | 75 |

<a id="swetem--собор"></a>
<a id="собор--swetem"></a>
### `swetem` — Cathedral
| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `priest` | Priest | 20.00 | 3.0 | **4.2** | 60 | 25 | 0 | 1 | — |

[↑ to contents](#содержание)

<a id="swi--switzerland-швейцария"></a>
<a id="швейцария"></a>
## Switzerland (`swi`)
<a id="eurmil--мельница"></a>
### `eurmil` — Mill

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

<a id="eurpor--порт"></a>
### `eurpor` — Shipyard

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `battleship` | Ship of the Line | 390.00 | 0.2 | **0.2** | 0 | 3200 | 700 | 1 | — |
| `ferry` | Ferry | 56.00 | 1.1 | **1.5** | 0 | 50 | 100 | 1 | — |
| `fishboat` | Boat | 40.00 | 1.5 | **2.1** | 0 | 0 | 0 | 1 | — |
| `frigate` | Frigate | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| `galley` | Galley | 50.00 | 1.2 | **1.7** | 0 | 900 | 800 | 1 | — |
| `yacht` | Yacht | 48.00 | 1.2 | **1.8** | 0 | 450 | 150 | 1 | — |

<a id="swiart--артиллерийское-депо"></a>
<a id="артиллерийское-депо--swiart"></a>
### `swiart` — Artillery Depot

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cannon` | Cannon | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| `howitzer` | Howitzer | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| `mortar` | Bombard | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| `multicannon` | Multi-barrelled Cannon | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

<a id="swiba2--казарма-18в"></a>
<a id="казарма-18в--swiba2"></a>
### `swiba2` — Barracks, 18th century

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer18` | Drummer, 18th century | 6.00 | 10.0 | **14.0** | 50 | 30 | 0 | 1 | — |
| `grenadier` | Grenadier | 6.00 | 10.0 | **14.0** | 80 | 60 | 40 | 1 | 36 |
| `jagerswi` | Chasseur | 8.50 | 7.1 | **9.9** | 40 | 70 | 20 | 1 | — |
| `musketeer18` | Musketeer, 18th century | 4.50 | 13.3 | **18.7** | 50 | 40 | 40 | 1 | — |
| `officer18` | Officer, 18th century | 6.00 | 10.0 | **14.0** | 50 | 200 | 10 | 1 | — |
| `pikeman18` | Pikeman, 18th century | 1.25 | 48.0 | **67.2** | 30 | 2 | 0 | 1 | — |

<a id="swibar--казарма-17в"></a>
<a id="казарма-17в--swibar"></a>
### `swibar` — Barracks, 17th century

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer` | Drummer, 17th century | 5.00 | 12.0 | **16.8** | 60 | 20 | 0 | 1 | — |
| `musketeer` | Musketeer, 17th century | 6.00 | 10.0 | **14.0** | 45 | 6 | 5 | 1 | — |
| `officer` | Officer, 17th century | 10.00 | 6.0 | **8.4** | 50 | 150 | 30 | 1 | — |
| `pikemanswi` | Pikeman, 17th century | 5.00 | 12.0 | **16.8** | 40 | 6 | 20 | 1 | — |

<a id="swicen--городской-центр"></a>
<a id="городской-центр--swicen"></a>
### `swicen` — Town Hall

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `peaaus` | Peasant | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

<a id="swidip--дипломатический-центр"></a>
<a id="дипломатический-центр--swidip"></a>
### `swidip` — Diplomatic Center

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `archerdip` | Archer (mercenary) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| `archerturdip` | Turkish archer (mercenary) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| `cossacksichdip` | Sich Cossack (mercenary) | 2.50 | 24.0 | **33.6** | 0 | 60 | 0 | 1 | 60 |
| `dragoon18dip` | Dragoon, 18th century (mercenary) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| `grenadierdip` | Grenadier (mercenary) | 1.50 | 40.0 | **56.0** | 0 | 25 | 0 | 1 | 36 |
| `lightcavalrydip` | Light cavalry (mercenary) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| `lightinfantrydip` | Light Infantryman (mercenary) | 1.25 | 48.0 | **67.2** | 0 | 4 | 0 | 1 | — |
| `roundshierdip` | Roundshier (mercenary) | 1.50 | 40.0 | **56.0** | 0 | 12 | 0 | 1 | — |

<a id="swista--конюшня"></a>
<a id="конюшня--swista"></a>
### `swista` — Stable

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cuirassier` | Cuirassier | 22.50 | 2.7 | **3.7** | 120 | 35 | 25 | 1 | 75 |
| `dragoon` | Dragoon, 17th century | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | 60 |
| `dragoon18` | Dragoon, 18th century | 22.50 | 2.7 | **3.7** | 70 | 60 | 7 | 1 | 60 |
| `hussarswi` | Mounted Jaeger | 19.50 | 3.1 | **4.3** | 120 | 30 | 2 | 1 | 60 |
| `reiter` | Reiter | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | 75 |

<a id="switem--собор"></a>
<a id="собор--switem"></a>
### `switem` — Cathedral

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `priest` | Priest | 20.00 | 3.0 | **4.2** | 60 | 25 | 0 | 1 | — |

[↑ to contents](#содержание)

<a id="tur--turkey-турция"></a>
<a id="турция"></a>
## Turkey (`tur`)
<a id="turart--артиллерийское-депо"></a>
<a id="артиллерийское-депо--turart"></a>
### `turart` — Artillery Depot

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cannon` | Cannon | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| `howitzer` | Howitzer | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| `mortar` | Bombard | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |

<a id="turbar--казарма"></a>
<a id="казарма--turbar"></a>
### `turbar` — Barracks

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `archertur` | Turkish archer | 3.00 | 20.0 | **28.0** | 45 | 4 | 0 | 1 | — |
| `drummertur` | Drummer, 17th century | 4.00 | 15.0 | **21.0** | 30 | 15 | 0 | 1 | — |
| `jannisary` | Janissary | 8.00 | 7.5 | **10.5** | 55 | 13 | 5 | 1 | — |
| `lightinfantry` | Light Infantryman | 1.00 | 60.0 | **84.0** | 25 | 0 | 1 | 1 | — |
| `officertur` | Officer | 7.50 | 8.0 | **11.2** | 50 | 100 | 0 | 1 | — |
| `pikemantur` | Ottoman Pikeman | 5.50 | 10.9 | **15.3** | 55 | 5 | 0 | 1 | — |

<a id="turcen--городской-центр"></a>
<a id="городской-центр--turcen"></a>
### `turcen` — Town Hall

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `peatur` | Peasant | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 28 |

<a id="turdip--дипломатический-центр"></a>
<a id="дипломатический-центр--turdip"></a>
### `turdip` — Diplomatic Center

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `archerdip` | Archer (mercenary) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| `archerturdip` | Turkish archer (mercenary) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| `cossacksichdip` | Sich Cossack (mercenary) | 2.50 | 24.0 | **33.6** | 0 | 60 | 0 | 1 | 60 |
| `dragoon18dip` | Dragoon, 18th century (mercenary) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| `grenadierdip` | Grenadier (mercenary) | 1.50 | 40.0 | **56.0** | 0 | 25 | 0 | 1 | 36 |
| `lightcavalrydip` | Light cavalry (mercenary) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| `lightinfantrydip` | Light Infantryman (mercenary) | 1.25 | 48.0 | **67.2** | 0 | 4 | 0 | 1 | — |
| `roundshierdip` | Roundshier (mercenary) | 1.50 | 40.0 | **56.0** | 0 | 12 | 0 | 1 | — |

<a id="turmil--мельница"></a>
### `turmil` — Mill

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

<a id="turpor--порт"></a>
### `turpor` — Shipyard

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `battleship` | Ship of the Line | 390.00 | 0.2 | **0.2** | 0 | 3200 | 700 | 1 | — |
| `ferry` | Ferry | 56.00 | 1.1 | **1.5** | 0 | 50 | 100 | 1 | — |
| `fishboat` | Boat | 40.00 | 1.5 | **2.1** | 0 | 0 | 0 | 1 | — |
| `galley` | Galley | 50.00 | 1.2 | **1.7** | 0 | 900 | 800 | 1 | — |
| `xebec` | Xebec | 230.00 | 0.3 | **0.4** | 0 | 1600 | 320 | 1 | — |
| `yachttur` | Yacht | 48.00 | 1.2 | **1.8** | 0 | 450 | 150 | 1 | — |

<a id="tursta--конюшня"></a>
<a id="конюшня--tursta"></a>
### `tursta` — Stable

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `sipahi` | Heavy Sipahi | 18.00 | 3.3 | **4.7** | 130 | 20 | 70 | 1 | 75 |
| `spakh` | Light Sipahi | 9.00 | 6.7 | **9.3** | 80 | 6 | 5 | 1 | 60 |
| `tatar` | Tatar | 11.25 | 5.3 | **7.5** | 70 | 6 | 0 | 1 | 60 |

<a id="turtem--мечеть"></a>
<a id="мечеть--turtem"></a>
### `turtem` — Mosque

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `mullah` | Mullah | 15.00 | 4.0 | **5.6** | 30 | 10 | 0 | 1 | — |

[↑ to contents](#содержание)

<a id="ukr--ukraine-украина"></a>
<a id="украина"></a>
## Ukraine (`ukr`)
<a id="rusmil--мельница"></a>
### `rusmil` — Mill

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

<a id="ukrart--артиллерийское-депо"></a>
<a id="артиллерийское-депо--ukrart"></a>
### `ukrart` — Artillery Depot

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cannon` | Cannon | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| `howitzer` | Howitzer | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| `mortar` | Bombard | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |

<a id="ukrbar--козацкий-дом"></a>
<a id="козацкий-дом--ukrbar"></a>
### `ukrbar` — Cossack House

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `serdiuk` | Serdiuk | 11.00 | 5.5 | **7.6** | 60 | 11 | 5 | 1 | — |

<a id="ukrcen--городской-центр"></a>
<a id="городской-центр--ukrcen"></a>
### `ukrcen` — Town Hall

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `peaukr` | Peasant | 11.25 | 5.3 | **7.5** | 100 | 0 | 0 | 1 | 32 |

<a id="ukrdip--дипломатический-центр"></a>
<a id="дипломатический-центр--ukrdip"></a>
### `ukrdip` — Diplomatic Center

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `archerdip` | Archer (mercenary) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| `archerturdip` | Turkish archer (mercenary) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| `cossacksichdip` | Sich Cossack (mercenary) | 2.50 | 24.0 | **33.6** | 0 | 60 | 0 | 1 | 60 |
| `dragoon18dip` | Dragoon, 18th century (mercenary) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| `grenadierdip` | Grenadier (mercenary) | 1.50 | 40.0 | **56.0** | 0 | 25 | 0 | 1 | 36 |
| `lightcavalrydip` | Light cavalry (mercenary) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| `lightinfantrydip` | Light Infantryman (mercenary) | 1.25 | 48.0 | **67.2** | 0 | 4 | 0 | 1 | — |
| `roundshierdip` | Roundshier (mercenary) | 1.50 | 40.0 | **56.0** | 0 | 12 | 0 | 1 | — |

<a id="ukrpor--порт"></a>
<a id="порт--ukrpor"></a>
### `ukrpor` — Shipyard

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `chaika` | — | 40.00 | 1.5 | **2.1** | 0 | 600 | 200 | 1 | — |
| `ferry` | Ferry | 56.00 | 1.1 | **1.5** | 0 | 50 | 100 | 1 | — |
| `fishboat` | Boat | 40.00 | 1.5 | **2.1** | 0 | 0 | 0 | 1 | — |
| `galley` | Galley | 50.00 | 1.2 | **1.7** | 0 | 900 | 800 | 1 | — |

<a id="ukrsta--конюшня"></a>
<a id="конюшня--ukrsta"></a>
### `ukrsta` — Stable

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cossackregister` | Register Cossack | 10.50 | 5.7 | **8.0** | 70 | 15 | 0 | 1 | 60 |
| `cossacksich` | Sich Cossack | 13.50 | 4.4 | **6.2** | 130 | 0 | 2 | 1 | 60 |
| `hetman` | Hetman | 16.50 | 3.6 | **5.1** | 150 | 150 | 10 | 1 | 90 |

<a id="ukrtem--православная-церковь"></a>
<a id="православная-церковь--ukrtem"></a>
### `ukrtem` — Orthodox Cathedral

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `pope` | Pope | 20.00 | 3.0 | **4.2** | 40 | 20 | 0 | 1 | — |

[↑ to contents](#содержание)

<a id="ven--venice-венеция"></a>
<a id="венеция"></a>
## Venice (`ven`)
<a id="eurmil--мельница"></a>
### `eurmil` — Mill

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

<a id="eurpor--порт"></a>
### `eurpor` — Shipyard

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `battleship` | Ship of the Line | 390.00 | 0.2 | **0.2** | 0 | 3200 | 700 | 1 | — |
| `ferry` | Ferry | 56.00 | 1.1 | **1.5** | 0 | 50 | 100 | 1 | — |
| `fishboat` | Boat | 40.00 | 1.5 | **2.1** | 0 | 0 | 0 | 1 | — |
| `frigate` | Frigate | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| `galley` | Galley | 50.00 | 1.2 | **1.7** | 0 | 900 | 800 | 1 | — |
| `yacht` | Yacht | 48.00 | 1.2 | **1.8** | 0 | 450 | 150 | 1 | — |

<a id="venart--артиллерийское-депо"></a>
<a id="артиллерийское-депо--venart"></a>
### `venart` — Artillery Depot

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cannon` | Cannon | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| `howitzer` | Howitzer | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| `mortar` | Bombard | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| `multicannon` | Multi-barrelled Cannon | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

<a id="venba2--казарма-18в"></a>
<a id="казарма-18в--venba2"></a>
### `venba2` — Barracks, 18th century

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer18` | Drummer, 18th century | 6.00 | 10.0 | **14.0** | 50 | 30 | 0 | 1 | — |
| `grenadier` | Grenadier | 6.00 | 10.0 | **14.0** | 80 | 60 | 40 | 1 | 36 |
| `musketeer18` | Musketeer, 18th century | 4.50 | 13.3 | **18.7** | 50 | 40 | 40 | 1 | — |
| `officer18` | Officer, 18th century | 6.00 | 10.0 | **14.0** | 50 | 200 | 10 | 1 | — |
| `pikeman18` | Pikeman, 18th century | 1.25 | 48.0 | **67.2** | 30 | 2 | 0 | 1 | — |

<a id="venbar--казарма-17в"></a>
<a id="казарма-17в--venbar"></a>
### `venbar` — Barracks, 17th century

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer` | Drummer, 17th century | 5.00 | 12.0 | **16.8** | 60 | 20 | 0 | 1 | — |
| `musketeer` | Musketeer, 17th century | 6.00 | 10.0 | **14.0** | 45 | 6 | 5 | 1 | — |
| `officer` | Officer, 17th century | 10.00 | 6.0 | **8.4** | 50 | 150 | 30 | 1 | — |
| `pikeman` | Pikeman, 17th century | 4.50 | 13.3 | **18.7** | 25 | 3 | 20 | 1 | — |

<a id="vencen--городской-центр"></a>
<a id="городской-центр--vencen"></a>
### `vencen` — Town Hall

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `peaspa` | Peasant | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

<a id="vendip--дипломатический-центр"></a>
<a id="дипломатический-центр--vendip"></a>
### `vendip` — Diplomatic Center

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `archerdip` | Archer (mercenary) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| `archerturdip` | Turkish archer (mercenary) | 1.25 | 48.0 | **67.2** | 0 | 15 | 0 | 1 | — |
| `cossacksichdip` | Sich Cossack (mercenary) | 2.50 | 24.0 | **33.6** | 0 | 60 | 0 | 1 | 60 |
| `dragoon18dip` | Dragoon, 18th century (mercenary) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| `grenadierdip` | Grenadier (mercenary) | 1.50 | 40.0 | **56.0** | 0 | 25 | 0 | 1 | 36 |
| `lightcavalrydip` | Light cavalry (mercenary) | 2.00 | 30.0 | **42.0** | 0 | 120 | 0 | 1 | 60 |
| `lightinfantrydip` | Light Infantryman (mercenary) | 1.25 | 48.0 | **67.2** | 0 | 4 | 0 | 1 | — |
| `roundshierdip` | Roundshier (mercenary) | 1.50 | 40.0 | **56.0** | 0 | 12 | 0 | 1 | — |

<a id="vensta--конюшня"></a>
<a id="конюшня--vensta"></a>
### `vensta` — Stable

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cuirassier` | Cuirassier | 22.50 | 2.7 | **3.7** | 120 | 35 | 25 | 1 | 75 |
| `dragoon` | Dragoon, 17th century | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | 60 |
| `dragoon18` | Dragoon, 18th century | 22.50 | 2.7 | **3.7** | 70 | 60 | 7 | 1 | 60 |
| `hussar` | Hussar | 15.00 | 4.0 | **5.6** | 70 | 20 | 2 | 1 | 60 |
| `reiter` | Reiter | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | 75 |

<a id="ventem--собор"></a>
<a id="собор--ventem"></a>
### `ventem` — Cathedral

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `priest` | Priest | 20.00 | 3.0 | **4.2** | 60 | 25 | 0 | 1 | — |

[↑ to contents](#содержание)

---

<a id="замечания"></a>
## Notes

1. **farm = 1 for each unit** - each unit occupies 1 population slot (controlled by `gPlayer.farm`). Buildings that increase the limit - `cen = +100`, `hou = +25`, `bar = +150`, `ba2 = +250`, etc.
2. **Food consumption** - food consumption per in-game second is divided by 32 (see `gc_obj_foodperunit`). Standard - 32 for infantry, 26 for Russian peasants, 40+ for heavy cavalry.
3. **If there is a shortage of farm, production stops** - the building will try to write off the resource, but the unit will not come out, progress is frozen.
4. **N buildings = N × rate.** 5 infantry barracks = 5 × ~13 musketeers/min @ fast = ~65 musketeers/min.

<a id="источники"></a>
## Sources

All links are relative to `data/scripts/` in the Cossacks 3 installation.

[^1]: `DoProgressOrders` for buildings - production queue processing - `units/building.inc/doprogressorders.inc:120-373`.
