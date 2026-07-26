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

- **[ALG - Algeria](#alg--algeria-алжир)** - [`algart`](#production-alg-algart), [`algbar`](#production-alg-algbar), [`algcen`](#production-alg-algcen), [`algdip`](#production-alg-algdip), [`algsta`](#production-alg-algsta), [`algtem`](#production-alg-algtem), [`turmil`](#production-alg-turmil), [`turpor`](#production-alg-turpor)
- **[AUS - Austria](#aus--austria-австрия)** - [`ausart`](#production-aus-ausart), [`ausba2`](#production-aus-ausba2), [`ausbar`](#production-aus-ausbar), [`auscen`](#production-aus-auscen), [`ausdip`](#production-aus-ausdip), [`aussta`](#production-aus-aussta), [`austem`](#production-aus-austem), [`eurmil`](#production-aus-eurmil), [`eurpor`](#production-aus-eurpor)
- **[BAV - Bavaria](#bav--bavaria-бавария)** - [`bavart`](#production-bav-bavart), [`bavba2`](#production-bav-bavba2), [`bavbar`](#production-bav-bavbar), [`bavcen`](#production-bav-bavcen), [`bavdip`](#production-bav-bavdip), [`bavsta`](#production-bav-bavsta), [`bavtem`](#production-bav-bavtem), [`eurmil`](#production-bav-eurmil), [`eurpor`](#production-bav-eurpor)
- **[DEN - Denmark](#den--denmark-дания)** - [`denart`](#production-den-denart), [`denba2`](#production-den-denba2), [`denbar`](#production-den-denbar), [`dencen`](#production-den-dencen), [`dendip`](#production-den-dendip), [`densta`](#production-den-densta), [`dentem`](#production-den-dentem), [`eurmil`](#production-den-eurmil), [`eurpor`](#production-den-eurpor)
- **[ENG - England](#eng--england-англия)** - [`engart`](#production-eng-engart), [`engba2`](#production-eng-engba2), [`engbar`](#production-eng-engbar), [`engcen`](#production-eng-engcen), [`engdip`](#production-eng-engdip), [`engsta`](#production-eng-engsta), [`engtem`](#production-eng-engtem), [`eurmil`](#production-eng-eurmil), [`eurpor`](#production-eng-eurpor)
- **[FRA - France](#fra--france-франция)** - [`eurmil`](#production-fra-eurmil), [`eurpor`](#production-fra-eurpor), [`fraart`](#production-fra-fraart), [`fraba2`](#production-fra-fraba2), [`frabar`](#production-fra-frabar), [`fracen`](#production-fra-fracen), [`fradip`](#production-fra-fradip), [`frasta`](#production-fra-frasta), [`fratem`](#production-fra-fratem)
- **[HUN - Hungary](#hun--hungary-венгрия)** - [`eurmil`](#production-hun-eurmil), [`eurpor`](#production-hun-eurpor), [`hunart`](#production-hun-hunart), [`hunba2`](#production-hun-hunba2), [`hunbar`](#production-hun-hunbar), [`huncen`](#production-hun-huncen), [`hundip`](#production-hun-hundip), [`hunsta`](#production-hun-hunsta), [`huntem`](#production-hun-huntem)
- **[NET — Netherlands](#net--netherlands-нидерланды)** — [`eurmil`](#production-net-eurmil), [`eurpor`](#production-net-eurpor), [`netart`](#production-net-netart), [`netba2`](#production-net-netba2), [`netbar`](#production-net-netbar), [`netcen`](#production-net-netcen), [`netdip`](#production-net-netdip), [`netsta`](#production-net-netsta), [`nettem`](#production-net-nettem)
- **[PIE — Piedmont](#pie--piedmont-пьемонт)** — [`eurmil`](#production-pie-eurmil), [`eurpor`](#production-pie-eurpor), [`pieart`](#production-pie-pieart), [`pieba2`](#production-pie-pieba2), [`piebar`](#production-pie-piebar), [`piecen`](#production-pie-piecen), [`piedip`](#production-pie-piedip), [`piesta`](#production-pie-piesta), [`pietem`](#production-pie-pietem)
- **[POL — Poland](#pol--poland-польша)** — [`eurmil`](#production-pol-eurmil), [`eurpor`](#production-pol-eurpor), [`polart`](#production-pol-polart), [`polba2`](#production-pol-polba2), [`polbar`](#production-pol-polbar), [`polcen`](#production-pol-polcen), [`poldip`](#production-pol-poldip), [`polsta`](#production-pol-polsta), [`poltem`](#production-pol-poltem)
- **[POR — Portugal](#por--portugal-португалия)** — [`eurmil`](#production-por-eurmil), [`porart`](#production-por-porart), [`porba2`](#production-por-porba2), [`porbar`](#production-por-porbar), [`porcen`](#production-por-porcen), [`pordip`](#production-por-pordip), [`porpor`](#production-por-porpor), [`porsta`](#production-por-porsta), [`portem`](#production-por-portem)
- **[PRU — Prussia](#pru--prussia-пруссия)** — [`eurmil`](#production-pru-eurmil), [`eurpor`](#production-pru-eurpor), [`pruart`](#production-pru-pruart), [`pruba2`](#production-pru-pruba2), [`prubar`](#production-pru-prubar), [`prucen`](#production-pru-prucen), [`prudip`](#production-pru-prudip), [`prusta`](#production-pru-prusta), [`prutem`](#production-pru-prutem)
- **[RUS — Russia](#rus--russia-россия)** — [`rusart`](#production-rus-rusart), [`rusba2`](#production-rus-rusba2), [`rusbar`](#production-rus-rusbar), [`ruscen`](#production-rus-ruscen), [`rusdip`](#production-rus-rusdip), [`rusmil`](#production-rus-rusmil), [`ruspor`](#production-rus-ruspor), [`russta`](#production-rus-russta), [`rustem`](#production-rus-rustem)
- **[SAX — Saxony](#sax--saxony-саксония)** — [`eurmil`](#production-sax-eurmil), [`eurpor`](#production-sax-eurpor), [`saxart`](#production-sax-saxart), [`saxba2`](#production-sax-saxba2), [`saxbar`](#production-sax-saxbar), [`saxcen`](#production-sax-saxcen), [`saxdip`](#production-sax-saxdip), [`saxsta`](#production-sax-saxsta), [`saxtem`](#production-sax-saxtem)
- **[SCO — Scotland](#sco--scotland-шотландия)** — [`eurmil`](#production-sco-eurmil), [`eurpor`](#production-sco-eurpor), [`scoart`](#production-sco-scoart), [`scoba2`](#production-sco-scoba2), [`scobar`](#production-sco-scobar), [`scocen`](#production-sco-scocen), [`scodip`](#production-sco-scodip), [`scosta`](#production-sco-scosta), [`scotem`](#production-sco-scotem)
- **[SPA — Spain](#spa--spain-испания)** — [`eurmil`](#production-spa-eurmil), [`eurpor`](#production-spa-eurpor), [`spaart`](#production-spa-spaart), [`spaba2`](#production-spa-spaba2), [`spabar`](#production-spa-spabar), [`spacen`](#production-spa-spacen), [`spadip`](#production-spa-spadip), [`spasta`](#production-spa-spasta), [`spatem`](#production-spa-spatem)
- **[SWE - Sweden](#swe--sweden-швеция)** - [`eurmil`](#production-swe-eurmil), [`eurpor`](#production-swe-eurpor), [`sweart`](#production-swe-sweart), [`sweba2`](#production-swe-sweba2), [`swebar`](#production-swe-swebar), [`swecen`](#production-swe-swecen), [`swedip`](#production-swe-swedip), [`swesta`](#production-swe-swesta), [`swetem`](#production-swe-swetem)
- **[SWI - Switzerland](#swi--switzerland-швейцария)** - [`eurmil`](#production-swi-eurmil), [`eurpor`](#production-swi-eurpor), [`swiart`](#production-swi-swiart), [`swiba2`](#production-swi-swiba2), [`swibar`](#production-swi-swibar), [`swicen`](#production-swi-swicen), [`swidip`](#production-swi-swidip), [`swista`](#production-swi-swista), [`switem`](#production-swi-switem)
- **[TUR - Turkey](#tur--turkey-турция)** - [`turart`](#production-tur-turart), [`turbar`](#production-tur-turbar), [`turcen`](#production-tur-turcen), [`turdip`](#production-tur-turdip), [`turmil`](#production-tur-turmil), [`turpor`](#production-tur-turpor), [`tursta`](#production-tur-tursta), [`turtem`](#production-tur-turtem)
- **[UKR - Ukraine](#ukr--ukraine-украина)** - [`rusmil`](#production-ukr-rusmil), [`ukrart`](#production-ukr-ukrart), [`ukrbar`](#production-ukr-ukrbar), [`ukrcen`](#production-ukr-ukrcen), [`ukrdip`](#production-ukr-ukrdip), [`ukrpor`](#production-ukr-ukrpor), [`ukrsta`](#production-ukr-ukrsta), [`ukrtem`](#production-ukr-ukrtem)
- **[VEN - Venice](#ven--venice-венеция)** - [`eurmil`](#production-ven-eurmil), [`eurpor`](#production-ven-eurpor), [`venart`](#production-ven-venart), [`venba2`](#production-ven-venba2), [`venbar`](#production-ven-venbar), [`vencen`](#production-ven-vencen), [`vendip`](#production-ven-vendip), [`vensta`](#production-ven-vensta), [`ventem`](#production-ven-ventem)

<a id="alg--algeria-алжир"></a>
<a id="алжир"></a>
## Algeria (`alg`)
<a id="algart--артиллерийское-депо"></a>
<a id="production-alg-algart"></a>
<a id="артиллерийское-депо--algart"></a>
### `algart` — Artillery Depot

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cannon` | Cannon | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| `howitzer` | Howitzer | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| `mortar` | Bombard | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |

<a id="algbar--казарма"></a>
<a id="production-alg-algbar"></a>
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
<a id="production-alg-algcen"></a>
<a id="городской-центр--algcen"></a>
### `algcen` — Town Hall

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `peatur` | Peasant | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 28 |

<a id="algdip--дипломатический-центр"></a>
<a id="production-alg-algdip"></a>
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
<a id="production-alg-algsta"></a>
<a id="конюшня--algsta"></a>
### `algsta` — Stable

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `mameluke` | Mameluke | 12.00 | 5.0 | **7.0** | 100 | 8 | 0 | 1 | 60 |

<a id="algtem--мечеть"></a>
<a id="production-alg-algtem"></a>
<a id="мечеть--algtem"></a>
### `algtem` — Mosque

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `mullah` | Mullah | 15.00 | 4.0 | **5.6** | 30 | 10 | 0 | 1 | — |

<a id="production-alg-turmil"></a>
<a id="мельница--turmil"></a>
### `turmil` — Mill

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

<a id="production-alg-turpor"></a>
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
<a id="production-aus-ausart"></a>
<a id="артиллерийское-депо--ausart"></a>
### `ausart` — Artillery Depot

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cannon` | Cannon | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| `howitzer` | Howitzer | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| `mortar` | Bombard | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| `multicannon` | Multi-barrelled Cannon | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

<a id="ausba2--казарма-18в"></a>
<a id="production-aus-ausba2"></a>
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
<a id="production-aus-ausbar"></a>
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
<a id="production-aus-auscen"></a>
<a id="городской-центр--auscen"></a>
### `auscen` — Town Hall

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `peaaus` | Peasant | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

<a id="ausdip--дипломатический-центр"></a>
<a id="production-aus-ausdip"></a>
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
<a id="production-aus-aussta"></a>
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
<a id="production-aus-austem"></a>
<a id="собор--austem"></a>
### `austem` — Cathedral

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `priest` | Priest | 20.00 | 3.0 | **4.2** | 60 | 25 | 0 | 1 | — |

<a id="production-aus-eurmil"></a>
<a id="мельница--eurmil"></a>
### `eurmil` — Mill

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

<a id="production-aus-eurpor"></a>
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
<a id="production-bav-bavart"></a>
<a id="артиллерийское-депо--bavart"></a>
### `bavart` — Artillery Depot

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cannon` | Cannon | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| `howitzer` | Howitzer | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| `mortar` | Bombard | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| `multicannon` | Multi-barrelled Cannon | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

<a id="bavba2--казарма-18в"></a>
<a id="production-bav-bavba2"></a>
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
<a id="production-bav-bavbar"></a>
<a id="казарма-17в--bavbar"></a>
### `bavbar` — Barracks, 17th century

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer` | Drummer, 17th century | 5.00 | 12.0 | **16.8** | 60 | 20 | 0 | 1 | — |
| `musketeer` | Musketeer, 17th century | 6.00 | 10.0 | **14.0** | 45 | 6 | 5 | 1 | — |
| `officer` | Officer, 17th century | 10.00 | 6.0 | **8.4** | 50 | 150 | 30 | 1 | — |
| `pikeman` | Pikeman, 17th century | 4.50 | 13.3 | **18.7** | 25 | 3 | 20 | 1 | — |

<a id="bavcen--городской-центр"></a>
<a id="production-bav-bavcen"></a>
<a id="городской-центр--bavcen"></a>
### `bavcen` — Town Hall

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `peaaus` | Peasant | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

<a id="bavdip--дипломатический-центр"></a>
<a id="production-bav-bavdip"></a>
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
<a id="production-bav-bavsta"></a>
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
<a id="production-bav-bavtem"></a>
<a id="собор--bavtem"></a>
### `bavtem` — Cathedral

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `priest` | Priest | 20.00 | 3.0 | **4.2** | 60 | 25 | 0 | 1 | — |

<a id="eurmil--мельница"></a>
<a id="production-bav-eurmil"></a>
<a id="мельница--eurmil-1"></a>
### `eurmil` — Mill

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

<a id="eurpor--порт"></a>
<a id="production-bav-eurpor"></a>
<a id="порт--eurpor-1"></a>
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
<a id="production-den-denart"></a>
<a id="артиллерийское-депо--denart"></a>
### `denart` — Artillery Depot

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cannon` | Cannon | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| `howitzer` | Howitzer | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| `mortar` | Bombard | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| `multicannon` | Multi-barrelled Cannon | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

<a id="denba2--казарма-18в"></a>
<a id="production-den-denba2"></a>
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
<a id="production-den-denbar"></a>
<a id="казарма-17в--denbar"></a>
### `denbar` — Barracks, 17th century

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer` | Drummer, 17th century | 5.00 | 12.0 | **16.8** | 60 | 20 | 0 | 1 | — |
| `musketeer` | Musketeer, 17th century | 6.00 | 10.0 | **14.0** | 45 | 6 | 5 | 1 | — |
| `officer` | Officer, 17th century | 10.00 | 6.0 | **8.4** | 50 | 150 | 30 | 1 | — |
| `pikeman` | Pikeman, 17th century | 4.50 | 13.3 | **18.7** | 25 | 3 | 20 | 1 | — |

<a id="dencen--городской-центр"></a>
<a id="production-den-dencen"></a>
<a id="городской-центр--dencen"></a>
### `dencen` — Town Hall

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `peaeng` | Peasant | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

<a id="dendip--дипломатический-центр"></a>
<a id="production-den-dendip"></a>
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
<a id="production-den-densta"></a>
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
<a id="production-den-dentem"></a>
<a id="собор--dentem"></a>
### `dentem` — Cathedral

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `priest` | Priest | 20.00 | 3.0 | **4.2** | 60 | 25 | 0 | 1 | — |

<a id="eurmil--мельница-1"></a>
<a id="production-den-eurmil"></a>
<a id="мельница--eurmil-2"></a>
### `eurmil` — Mill

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

<a id="eurpor--порт-1"></a>
<a id="production-den-eurpor"></a>
<a id="порт--eurpor-2"></a>
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
<a id="production-eng-engart"></a>
<a id="артиллерийское-депо--engart"></a>
### `engart` — Artillery Depot

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cannon` | Cannon | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| `howitzer` | Howitzer | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| `mortar` | Bombard | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| `multicannon` | Multi-barrelled Cannon | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

<a id="engba2--казарма-18в"></a>
<a id="production-eng-engba2"></a>
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
<a id="production-eng-engbar"></a>
<a id="казарма-17в--engbar"></a>
### `engbar` — Barracks, 17th century

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer` | Drummer, 17th century | 5.00 | 12.0 | **16.8** | 60 | 20 | 0 | 1 | — |
| `musketeer` | Musketeer, 17th century | 6.00 | 10.0 | **14.0** | 45 | 6 | 5 | 1 | — |
| `officer` | Officer, 17th century | 10.00 | 6.0 | **8.4** | 50 | 150 | 30 | 1 | — |
| `pikeman` | Pikeman, 17th century | 4.50 | 13.3 | **18.7** | 25 | 3 | 20 | 1 | — |

<a id="engcen--городской-центр"></a>
<a id="production-eng-engcen"></a>
<a id="городской-центр--engcen"></a>
### `engcen` — Town Hall

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `peaeng` | Peasant | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

<a id="engdip--дипломатический-центр"></a>
<a id="production-eng-engdip"></a>
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
<a id="production-eng-engsta"></a>
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
<a id="production-eng-engtem"></a>
<a id="собор--engtem"></a>
### `engtem` — Cathedral

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `priest` | Priest | 20.00 | 3.0 | **4.2** | 60 | 25 | 0 | 1 | — |

<a id="eurmil--мельница-2"></a>
<a id="production-eng-eurmil"></a>
<a id="мельница--eurmil-3"></a>
### `eurmil` — Mill

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

<a id="eurpor--порт-2"></a>
<a id="production-eng-eurpor"></a>
<a id="порт--eurpor-3"></a>
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
<a id="eurmil--мельница-3"></a>
<a id="production-fra-eurmil"></a>
<a id="мельница--eurmil-4"></a>
### `eurmil` — Mill

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

<a id="eurpor--порт-3"></a>
<a id="production-fra-eurpor"></a>
<a id="порт--eurpor-4"></a>
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
<a id="production-fra-fraart"></a>
<a id="артиллерийское-депо--fraart"></a>
### `fraart` — Artillery Depot

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cannon` | Cannon | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| `howitzer` | Howitzer | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| `mortar` | Bombard | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| `multicannon` | Multi-barrelled Cannon | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

<a id="fraba2--казарма-18в"></a>
<a id="production-fra-fraba2"></a>
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
<a id="production-fra-frabar"></a>
<a id="казарма-17в--frabar"></a>
### `frabar` — Barracks, 17th century

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer` | Drummer, 17th century | 5.00 | 12.0 | **16.8** | 60 | 20 | 0 | 1 | — |
| `musketeer` | Musketeer, 17th century | 6.00 | 10.0 | **14.0** | 45 | 6 | 5 | 1 | — |
| `officer` | Officer, 17th century | 10.00 | 6.0 | **8.4** | 50 | 150 | 30 | 1 | — |
| `pikeman` | Pikeman, 17th century | 4.50 | 13.3 | **18.7** | 25 | 3 | 20 | 1 | — |

<a id="fracen--городской-центр"></a>
<a id="production-fra-fracen"></a>
<a id="городской-центр--fracen"></a>
### `fracen` — Town Hall

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `peaeng` | Peasant | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

<a id="fradip--дипломатический-центр"></a>
<a id="production-fra-fradip"></a>
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
<a id="production-fra-frasta"></a>
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
<a id="production-fra-fratem"></a>
<a id="собор--fratem"></a>
### `fratem` — Cathedral

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `priest` | Priest | 20.00 | 3.0 | **4.2** | 60 | 25 | 0 | 1 | — |

[↑ to contents](#содержание)

<a id="hun--hungary-венгрия"></a>
<a id="венгрия"></a>
## Hungary (`hun`)
<a id="production-hun-eurmil"></a>
<a id="мельница--eurmil-5"></a>
### `eurmil` — Mill

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

<a id="production-hun-eurpor"></a>
<a id="порт--eurpor-5"></a>
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
<a id="production-hun-hunart"></a>
<a id="артиллерийское-депо--hunart"></a>
### `hunart` — Artillery Depot

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cannon` | Cannon | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| `howitzer` | Howitzer | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| `mortar` | Bombard | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| `multicannon` | Multi-barrelled Cannon | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

<a id="hunba2--казарма-18в"></a>
<a id="production-hun-hunba2"></a>
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
<a id="production-hun-hunbar"></a>
<a id="казарма-17в--hunbar"></a>
### `hunbar` — Barracks, 17th century

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer` | Drummer, 17th century | 5.00 | 12.0 | **16.8** | 60 | 20 | 0 | 1 | — |
| `gauduk` | Hajduk | 4.50 | 13.3 | **18.7** | 35 | 4 | 4 | 1 | — |
| `officer` | Officer, 17th century | 10.00 | 6.0 | **8.4** | 50 | 150 | 30 | 1 | — |
| `pikeman` | Pikeman, 17th century | 4.50 | 13.3 | **18.7** | 25 | 3 | 20 | 1 | — |

<a id="huncen--городской-центр"></a>
<a id="production-hun-huncen"></a>
<a id="городской-центр--huncen"></a>
### `huncen` — Town Hall

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `peapol` | Peasant | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

<a id="hundip--дипломатический-центр"></a>
<a id="production-hun-hundip"></a>
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
<a id="production-hun-hunsta"></a>
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
<a id="production-hun-huntem"></a>
<a id="собор--huntem"></a>
### `huntem` — Cathedral

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `priest` | Priest | 20.00 | 3.0 | **4.2** | 60 | 25 | 0 | 1 | — |

[↑ to contents](#содержание)

<a id="net--netherlands-нидерланды"></a>
<a id="нидерланды"></a>
## Netherlands (`net`)
<a id="production-net-eurmil"></a>
<a id="мельница--eurmil-6"></a>
### `eurmil` — Mill

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

<a id="production-net-eurpor"></a>
<a id="порт--eurpor-6"></a>
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
<a id="production-net-netart"></a>
<a id="артиллерийское-депо--netart"></a>
### `netart` — Artillery Depot

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cannon` | Cannon | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| `howitzer` | Howitzer | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| `mortar` | Bombard | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| `multicannon` | Multi-barrelled Cannon | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

<a id="netba2--казарма-18в"></a>
<a id="production-net-netba2"></a>
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
<a id="production-net-netbar"></a>
<a id="казарма-17в--netbar"></a>
### `netbar` — Barracks, 17th century

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer` | Drummer, 17th century | 5.00 | 12.0 | **16.8** | 60 | 20 | 0 | 1 | — |
| `musketeernet` | Musketeer, 17th century | 5.00 | 12.0 | **16.8** | 50 | 8 | 4 | 1 | — |
| `officer` | Officer, 17th century | 10.00 | 6.0 | **8.4** | 50 | 150 | 30 | 1 | — |
| `pikeman` | Pikeman, 17th century | 4.50 | 13.3 | **18.7** | 25 | 3 | 20 | 1 | — |

<a id="netcen--городской-центр"></a>
<a id="production-net-netcen"></a>
<a id="городской-центр--netcen"></a>
### `netcen` — Town Hall
| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `peaeng` | Peasant | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

<a id="netdip--дипломатический-центр"></a>
<a id="production-net-netdip"></a>
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
<a id="production-net-netsta"></a>
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
<a id="production-net-nettem"></a>
<a id="собор--nettem"></a>
### `nettem` — Cathedral

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `priest` | Priest | 20.00 | 3.0 | **4.2** | 60 | 25 | 0 | 1 | — |

[↑ to contents](#содержание)

<a id="pie--piedmont-пьемонт"></a>
<a id="пьемонт"></a>
## Piedmont (`pie`)
<a id="eurmil--мельница-4"></a>
<a id="production-pie-eurmil"></a>
<a id="мельница--eurmil-7"></a>
### `eurmil` — Mill

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

<a id="eurpor--порт-4"></a>
<a id="production-pie-eurpor"></a>
<a id="порт--eurpor-7"></a>
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
<a id="production-pie-pieart"></a>
<a id="артиллерийское-депо--pieart"></a>
### `pieart` — Artillery Depot

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cannon` | Cannon | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| `howitzer` | Howitzer | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| `mortar` | Bombard | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| `multicannon` | Multi-barrelled Cannon | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

<a id="pieba2--казарма-18в"></a>
<a id="production-pie-pieba2"></a>
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
<a id="production-pie-piebar"></a>
<a id="казарма-17в--piebar"></a>
### `piebar` — Barracks, 17th century

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer` | Drummer, 17th century | 5.00 | 12.0 | **16.8** | 60 | 20 | 0 | 1 | — |
| `musketeer` | Musketeer, 17th century | 6.00 | 10.0 | **14.0** | 45 | 6 | 5 | 1 | — |
| `officer` | Officer, 17th century | 10.00 | 6.0 | **8.4** | 50 | 150 | 30 | 1 | — |
| `pikeman` | Pikeman, 17th century | 4.50 | 13.3 | **18.7** | 25 | 3 | 20 | 1 | — |

<a id="piecen--городской-центр"></a>
<a id="production-pie-piecen"></a>
<a id="городской-центр--piecen"></a>
### `piecen` — Town Hall

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `peaspa` | Peasant | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

<a id="piedip--дипломатический-центр"></a>
<a id="production-pie-piedip"></a>
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
<a id="production-pie-piesta"></a>
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
<a id="production-pie-pietem"></a>
<a id="собор--pietem"></a>
### `pietem` — Cathedral

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `padre` | Padre | 25.00 | 2.4 | **3.4** | 50 | 40 | 0 | 1 | — |

[↑ to contents](#содержание)

<a id="pol--poland-польша"></a>
<a id="польша"></a>
## Poland (`pol`)
<a id="eurmil--мельница-5"></a>
<a id="production-pol-eurmil"></a>
<a id="мельница--eurmil-8"></a>
### `eurmil` — Mill

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

<a id="eurpor--порт-5"></a>
<a id="production-pol-eurpor"></a>
<a id="порт--eurpor-8"></a>
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
<a id="production-pol-polart"></a>
<a id="артиллерийское-депо--polart"></a>
### `polart` — Artillery Depot

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cannon` | Cannon | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| `howitzer` | Howitzer | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| `mortar` | Bombard | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| `multicannon` | Multi-barrelled Cannon | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

<a id="polba2--казарма-18в"></a>
<a id="production-pol-polba2"></a>
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
<a id="production-pol-polbar"></a>
<a id="казарма-17в--polbar"></a>
### `polbar` — Barracks, 17th century

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer` | Drummer, 17th century | 5.00 | 12.0 | **16.8** | 60 | 20 | 0 | 1 | — |
| `musketeerpol` | Musketeer, 17th century | 4.50 | 13.3 | **18.7** | 40 | 3 | 3 | 1 | — |
| `officer` | Officer, 17th century | 10.00 | 6.0 | **8.4** | 50 | 150 | 30 | 1 | — |
| `pikemanpol` | Pikeman, 17th century | 3.00 | 20.0 | **28.0** | 25 | 1 | 0 | 1 | — |

<a id="polcen--городской-центр"></a>
<a id="production-pol-polcen"></a>
<a id="городской-центр--polcen"></a>
### `polcen` — Town Hall

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `peapol` | Peasant | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

<a id="poldip--дипломатический-центр"></a>
<a id="production-pol-poldip"></a>
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
<a id="production-pol-polsta"></a>
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
<a id="production-pol-poltem"></a>
<a id="собор--poltem"></a>
### `poltem` — Cathedral

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `priest` | Priest | 20.00 | 3.0 | **4.2** | 60 | 25 | 0 | 1 | — |

[↑ to contents](#содержание)

<a id="por--portugal-португалия"></a>
<a id="португалия"></a>
## Portugal (`por`)
<a id="eurmil--мельница-6"></a>
<a id="production-por-eurmil"></a>
<a id="мельница--eurmil-9"></a>
### `eurmil` — Mill

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

<a id="porart--артиллерийское-депо"></a>
<a id="production-por-porart"></a>
<a id="артиллерийское-депо--porart"></a>
### `porart` — Artillery Depot

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cannon` | Cannon | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| `howitzer` | Howitzer | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| `mortar` | Bombard | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| `multicannon` | Multi-barrelled Cannon | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

<a id="porba2--казарма-18в"></a>
<a id="production-por-porba2"></a>
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
<a id="production-por-porbar"></a>
<a id="казарма-17в--porbar"></a>
### `porbar` — Barracks, 17th century

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer` | Drummer, 17th century | 5.00 | 12.0 | **16.8** | 60 | 20 | 0 | 1 | — |
| `musketeer` | Musketeer, 17th century | 6.00 | 10.0 | **14.0** | 45 | 6 | 5 | 1 | — |
| `officer` | Officer, 17th century | 10.00 | 6.0 | **8.4** | 50 | 150 | 30 | 1 | — |
| `pikemanpor` | Pikeman, 17th century | 4.00 | 15.0 | **21.0** | 40 | 4 | 5 | 1 | — |

<a id="porcen--городской-центр"></a>
<a id="production-por-porcen"></a>
<a id="городской-центр--porcen"></a>
### `porcen` — Town Hall

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `peaspa` | Peasant | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

<a id="pordip--дипломатический-центр"></a>
<a id="production-por-pordip"></a>
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
<a id="production-por-porpor"></a>
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
<a id="production-por-porsta"></a>
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
<a id="production-por-portem"></a>
<a id="собор--portem"></a>
### `portem` — Cathedral

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `priest` | Priest | 20.00 | 3.0 | **4.2** | 60 | 25 | 0 | 1 | — |

[↑ to contents](#содержание)

<a id="pru--prussia-пруссия"></a>
<a id="пруссия"></a>
## Prussia (`pru`)
<a id="eurmil--мельница-7"></a>
<a id="production-pru-eurmil"></a>
<a id="мельница--eurmil-10"></a>
### `eurmil` — Mill

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

<a id="eurpor--порт-6"></a>
<a id="production-pru-eurpor"></a>
<a id="порт--eurpor-9"></a>
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
<a id="production-pru-pruart"></a>
<a id="артиллерийское-депо--pruart"></a>
### `pruart` — Artillery Depot

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cannon` | Cannon | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| `howitzer` | Howitzer | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| `mortar` | Bombard | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| `multicannon` | Multi-barrelled Cannon | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

<a id="pruba2--казарма-18в"></a>
<a id="production-pru-pruba2"></a>
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
<a id="production-pru-prubar"></a>
<a id="казарма-17в--prubar"></a>
### `prubar` — Barracks, 17th century

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer` | Drummer, 17th century | 5.00 | 12.0 | **16.8** | 60 | 20 | 0 | 1 | — |
| `musketeer` | Musketeer, 17th century | 6.00 | 10.0 | **14.0** | 45 | 6 | 5 | 1 | — |
| `officer` | Officer, 17th century | 10.00 | 6.0 | **8.4** | 50 | 150 | 30 | 1 | — |
| `pikeman` | Pikeman, 17th century | 4.50 | 13.3 | **18.7** | 25 | 3 | 20 | 1 | — |

<a id="prucen--городской-центр"></a>
<a id="production-pru-prucen"></a>
<a id="городской-центр--prucen"></a>
### `prucen` — Town Hall

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `peaaus` | Peasant | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

<a id="prudip--дипломатический-центр"></a>
<a id="production-pru-prudip"></a>
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
<a id="production-pru-prusta"></a>
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
<a id="production-pru-prutem"></a>
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
<a id="production-rus-rusart"></a>
<a id="артиллерийское-депо--rusart"></a>
### `rusart` — Artillery Depot

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cannon` | Cannon | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| `howitzer` | Howitzer | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| `mortar` | Bombard | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| `multicannon` | Multi-barrelled Cannon | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

<a id="rusba2--казарма-18в"></a>
<a id="production-rus-rusba2"></a>
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
<a id="production-rus-rusbar"></a>
<a id="стрелецкая-казарма--rusbar"></a>
### `rusbar` — Strelets Barracks

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummerrus` | Drummer, 17th century | 6.00 | 10.0 | **14.0** | 90 | 15 | 0 | 1 | — |
| `officerrus` | Commander | 12.50 | 4.8 | **6.7** | 100 | 125 | 5 | 1 | — |
| `pikemanrus` | Spearman | 5.50 | 10.9 | **15.3** | 45 | 4 | 15 | 1 | — |
| `strelet` | Strelets | 8.50 | 7.1 | **9.9** | 70 | 7 | 9 | 1 | — |

<a id="ruscen--городской-центр"></a>
<a id="production-rus-ruscen"></a>
<a id="городской-центр--ruscen"></a>
### `ruscen` — Town Hall

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `pearus` | Serf | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 26 |

<a id="rusdip--дипломатический-центр"></a>
<a id="production-rus-rusdip"></a>
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
<a id="production-rus-rusmil"></a>
<a id="мельница--rusmil"></a>
### `rusmil` — Mill

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

<a id="ruspor--порт"></a>
<a id="production-rus-ruspor"></a>
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
<a id="production-rus-russta"></a>
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
<a id="production-rus-rustem"></a>
<a id="православная-церковь--rustem"></a>
### `rustem` — Orthodox Cathedral

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `pope` | Pope | 20.00 | 3.0 | **4.2** | 40 | 20 | 0 | 1 | — |

[↑ to contents](#содержание)

<a id="sax--saxony-саксония"></a>
<a id="саксония"></a>
## Saxony (`sax`)
<a id="eurmil--мельница-8"></a>
<a id="production-sax-eurmil"></a>
<a id="мельница--eurmil-11"></a>
### `eurmil` — Mill

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

<a id="eurpor--порт-7"></a>
<a id="production-sax-eurpor"></a>
<a id="порт--eurpor-10"></a>
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
<a id="production-sax-saxart"></a>
<a id="артиллерийское-депо--saxart"></a>
### `saxart` — Artillery Depot

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cannon` | Cannon | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| `howitzer` | Howitzer | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| `mortar` | Bombard | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| `multicannon` | Multi-barrelled Cannon | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

<a id="saxba2--казарма-18в"></a>
<a id="production-sax-saxba2"></a>
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
<a id="production-sax-saxbar"></a>
<a id="казарма-17в--saxbar"></a>
### `saxbar` — Barracks, 17th century

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer` | Drummer, 17th century | 5.00 | 12.0 | **16.8** | 60 | 20 | 0 | 1 | — |
| `musketeer` | Musketeer, 17th century | 6.00 | 10.0 | **14.0** | 45 | 6 | 5 | 1 | — |
| `officer` | Officer, 17th century | 10.00 | 6.0 | **8.4** | 50 | 150 | 30 | 1 | — |
| `pikeman` | Pikeman, 17th century | 4.50 | 13.3 | **18.7** | 25 | 3 | 20 | 1 | — |

<a id="saxcen--городской-центр"></a>
<a id="production-sax-saxcen"></a>
<a id="городской-центр--saxcen"></a>
### `saxcen` — Town Hall

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `peaaus` | Peasant | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

<a id="saxdip--дипломатический-центр"></a>
<a id="production-sax-saxdip"></a>
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
<a id="production-sax-saxsta"></a>
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
<a id="production-sax-saxtem"></a>
<a id="собор--saxtem"></a>
### `saxtem` — Cathedral

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `priest` | Priest | 20.00 | 3.0 | **4.2** | 60 | 25 | 0 | 1 | — |

[↑ to contents](#содержание)

<a id="sco--scotland-шотландия"></a>
<a id="шотландия"></a>
## Scotland (`sco`)
<a id="eurmil--мельница-9"></a>
<a id="production-sco-eurmil"></a>
<a id="мельница--eurmil-12"></a>
### `eurmil` — Mill

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

<a id="eurpor--порт-8"></a>
<a id="production-sco-eurpor"></a>
<a id="порт--eurpor-11"></a>
### `eurpor` — Shipyard

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `battleship` | Ship of the Line | 390.00 | 0.2 | **0.2** | 0 | 3200 | 700 | 1 | — |
| `ferry` | Ferry | 56.00 | 1.1 | **1.5** | 0 | 50 | 100 | 1 | — |
| `fishboat` | Boat | 40.00 | 1.5 | **2.1** | 0 | 0 | 0 | 1 | — |
| `frigate` | Frigate | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| `yacht` | Yacht | 48.00 | 1.2 | **1.8** | 0 | 450 | 150 | 1 | — |

<a id="scoart--артиллерийское-депо"></a>
<a id="production-sco-scoart"></a>
<a id="артиллерийское-депо--scoart"></a>
### `scoart` — Artillery Depot

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cannon` | Cannon | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| `framegun` | Frame gun | 50.00 | 1.2 | **1.7** | 0 | 300 | 150 | 1 | — |
| `howitzer` | Howitzer | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| `mortar` | Bombard | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |

<a id="scoba2--замок"></a>
<a id="production-sco-scoba2"></a>
<a id="замок--scoba2"></a>
### `scoba2` — Castle

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `archersco` | Bow Clansman | 6.00 | 10.0 | **14.0** | 80 | 7 | 0 | 1 | 39 |
| `swordsmansco` | Sword Clansman | 7.00 | 8.6 | **12.0** | 110 | 10 | 0 | 1 | 45 |

<a id="scobar--казарма-17в"></a>
<a id="production-sco-scobar"></a>
<a id="казарма-17в--scobar"></a>
### `scobar` — Barracks, 17th century

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `bagpiper` | Bagpiper | 7.00 | 8.6 | **12.0** | 120 | 20 | 0 | 1 | — |
| `musketeersco` | Covenanter musketeer | 7.00 | 8.6 | **12.0** | 55 | 8 | 7 | 1 | — |
| `officersco` | Officer | 10.00 | 6.0 | **8.4** | 130 | 130 | 10 | 1 | — |
| `pikemansco` | Covenanter pikeman | 4.00 | 15.0 | **21.0** | 35 | 2 | 0 | 1 | — |

<a id="scocen--городской-центр"></a>
<a id="production-sco-scocen"></a>
<a id="городской-центр--scocen"></a>
### `scocen` — Town Hall

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `peasco` | Peasant | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

<a id="scodip--дипломатический-центр"></a>
<a id="production-sco-scodip"></a>
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
<a id="production-sco-scosta"></a>
<a id="конюшня--scosta"></a>
### `scosta` — Stable

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `lancersco` | Lancer | 21.00 | 2.9 | **4.0** | 120 | 6 | 0 | 1 | 60 |
| `raidersco` | Raider | 22.50 | 2.7 | **3.7** | 130 | 8 | 2 | 1 | 75 |

<a id="scotem--собор"></a>
<a id="production-sco-scotem"></a>
<a id="собор--scotem"></a>
### `scotem` — Cathedral

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `priest` | Priest | 20.00 | 3.0 | **4.2** | 60 | 25 | 0 | 1 | — |

[↑ to contents](#содержание)

<a id="spa--spain-испания"></a>
<a id="испания"></a>
## Spain (`spa`)
<a id="eurmil--мельница-10"></a>
<a id="production-spa-eurmil"></a>
<a id="мельница--eurmil-13"></a>
### `eurmil` — Mill

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

<a id="eurpor--порт-9"></a>
<a id="production-spa-eurpor"></a>
<a id="порт--eurpor-12"></a>
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
<a id="production-spa-spaart"></a>
<a id="артиллерийское-депо--spaart"></a>
### `spaart` — Artillery Depot

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cannon` | Cannon | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| `howitzer` | Howitzer | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| `mortar` | Bombard | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| `multicannon` | Multi-barrelled Cannon | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

<a id="spaba2--казарма-18в"></a>
<a id="production-spa-spaba2"></a>
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
<a id="production-spa-spabar"></a>
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
<a id="production-spa-spacen"></a>
<a id="городской-центр--spacen"></a>
### `spacen` — Town Hall

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `peaspa` | Peasant | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

<a id="spadip--дипломатический-центр"></a>
<a id="production-spa-spadip"></a>
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
<a id="production-spa-spasta"></a>
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
<a id="production-spa-spatem"></a>
<a id="собор--spatem"></a>
### `spatem` — Cathedral

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `priest` | Priest | 20.00 | 3.0 | **4.2** | 60 | 25 | 0 | 1 | — |

[↑ to contents](#содержание)

<a id="swe--sweden-швеция"></a>
<a id="швеция"></a>
## Sweden (`swe`)
<a id="production-swe-eurmil"></a>
<a id="мельница--eurmil-14"></a>
### `eurmil` — Mill

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

<a id="production-swe-eurpor"></a>
<a id="порт--eurpor-13"></a>
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
<a id="production-swe-sweart"></a>
<a id="артиллерийское-депо--sweart"></a>
### `sweart` — Artillery Depot

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cannon` | Cannon | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| `howitzer` | Howitzer | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| `mortar` | Bombard | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| `multicannon` | Multi-barrelled Cannon | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

<a id="sweba2--казарма-18в"></a>
<a id="production-swe-sweba2"></a>
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
<a id="production-swe-swebar"></a>
<a id="казарма-17в--swebar"></a>
### `swebar` — Barracks, 17th century

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer` | Drummer, 17th century | 5.00 | 12.0 | **16.8** | 60 | 20 | 0 | 1 | — |
| `musketeer` | Musketeer, 17th century | 6.00 | 10.0 | **14.0** | 45 | 6 | 5 | 1 | — |
| `officer` | Officer, 17th century | 10.00 | 6.0 | **8.4** | 50 | 150 | 30 | 1 | — |
| `pikeman` | Pikeman, 17th century | 4.50 | 13.3 | **18.7** | 25 | 3 | 20 | 1 | — |

<a id="swecen--городской-центр"></a>
<a id="production-swe-swecen"></a>
<a id="городской-центр--swecen"></a>
### `swecen` — Town Hall

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `peaeng` | Peasant | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

<a id="swedip--дипломатический-центр"></a>
<a id="production-swe-swedip"></a>
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
<a id="production-swe-swesta"></a>
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
<a id="production-swe-swetem"></a>
<a id="собор--swetem"></a>
### `swetem` — Cathedral
| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `priest` | Priest | 20.00 | 3.0 | **4.2** | 60 | 25 | 0 | 1 | — |

[↑ to contents](#содержание)

<a id="swi--switzerland-швейцария"></a>
<a id="швейцария"></a>
## Switzerland (`swi`)
<a id="eurmil--мельница-11"></a>
<a id="production-swi-eurmil"></a>
<a id="мельница--eurmil-15"></a>
### `eurmil` — Mill

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

<a id="eurpor--порт-10"></a>
<a id="production-swi-eurpor"></a>
<a id="порт--eurpor-14"></a>
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
<a id="production-swi-swiart"></a>
<a id="артиллерийское-депо--swiart"></a>
### `swiart` — Artillery Depot

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cannon` | Cannon | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| `howitzer` | Howitzer | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| `mortar` | Bombard | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| `multicannon` | Multi-barrelled Cannon | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

<a id="swiba2--казарма-18в"></a>
<a id="production-swi-swiba2"></a>
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
<a id="production-swi-swibar"></a>
<a id="казарма-17в--swibar"></a>
### `swibar` — Barracks, 17th century

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer` | Drummer, 17th century | 5.00 | 12.0 | **16.8** | 60 | 20 | 0 | 1 | — |
| `musketeer` | Musketeer, 17th century | 6.00 | 10.0 | **14.0** | 45 | 6 | 5 | 1 | — |
| `officer` | Officer, 17th century | 10.00 | 6.0 | **8.4** | 50 | 150 | 30 | 1 | — |
| `pikemanswi` | Pikeman, 17th century | 5.00 | 12.0 | **16.8** | 40 | 6 | 20 | 1 | — |

<a id="swicen--городской-центр"></a>
<a id="production-swi-swicen"></a>
<a id="городской-центр--swicen"></a>
### `swicen` — Town Hall

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `peaaus` | Peasant | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

<a id="swidip--дипломатический-центр"></a>
<a id="production-swi-swidip"></a>
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
<a id="production-swi-swista"></a>
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
<a id="production-swi-switem"></a>
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
<a id="production-tur-turart"></a>
<a id="артиллерийское-депо--turart"></a>
### `turart` — Artillery Depot

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cannon` | Cannon | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| `howitzer` | Howitzer | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| `mortar` | Bombard | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |

<a id="turbar--казарма"></a>
<a id="production-tur-turbar"></a>
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
<a id="production-tur-turcen"></a>
<a id="городской-центр--turcen"></a>
### `turcen` — Town Hall

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `peatur` | Peasant | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 28 |

<a id="turdip--дипломатический-центр"></a>
<a id="production-tur-turdip"></a>
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
<a id="production-tur-turmil"></a>
<a id="мельница--turmil-1"></a>
### `turmil` — Mill

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

<a id="turpor--порт"></a>
<a id="production-tur-turpor"></a>
<a id="порт--turpor-1"></a>
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
<a id="production-tur-tursta"></a>
<a id="конюшня--tursta"></a>
### `tursta` — Stable

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `sipahi` | Heavy Sipahi | 18.00 | 3.3 | **4.7** | 130 | 20 | 70 | 1 | 75 |
| `spakh` | Light Sipahi | 9.00 | 6.7 | **9.3** | 80 | 6 | 5 | 1 | 60 |
| `tatar` | Tatar | 11.25 | 5.3 | **7.5** | 70 | 6 | 0 | 1 | 60 |

<a id="turtem--мечеть"></a>
<a id="production-tur-turtem"></a>
<a id="мечеть--turtem"></a>
### `turtem` — Mosque

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `mullah` | Mullah | 15.00 | 4.0 | **5.6** | 30 | 10 | 0 | 1 | — |

[↑ to contents](#содержание)

<a id="ukr--ukraine-украина"></a>
<a id="украина"></a>
## Ukraine (`ukr`)
<a id="rusmil--мельница-1"></a>
<a id="production-ukr-rusmil"></a>
<a id="мельница--rusmil-1"></a>
### `rusmil` — Mill

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

<a id="ukrart--артиллерийское-депо"></a>
<a id="production-ukr-ukrart"></a>
<a id="артиллерийское-депо--ukrart"></a>
### `ukrart` — Artillery Depot

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cannon` | Cannon | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| `howitzer` | Howitzer | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| `mortar` | Bombard | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |

<a id="ukrbar--козацкий-дом"></a>
<a id="production-ukr-ukrbar"></a>
<a id="козацкий-дом--ukrbar"></a>
### `ukrbar` — Cossack House

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `serdiuk` | Serdiuk | 11.00 | 5.5 | **7.6** | 60 | 11 | 5 | 1 | — |

<a id="ukrcen--городской-центр"></a>
<a id="production-ukr-ukrcen"></a>
<a id="городской-центр--ukrcen"></a>
### `ukrcen` — Town Hall

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `peaukr` | Peasant | 11.25 | 5.3 | **7.5** | 100 | 0 | 0 | 1 | 32 |

<a id="ukrdip--дипломатический-центр"></a>
<a id="production-ukr-ukrdip"></a>
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
<a id="production-ukr-ukrpor"></a>
<a id="порт--ukrpor"></a>
### `ukrpor` — Shipyard

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `chaika` | — | 40.00 | 1.5 | **2.1** | 0 | 600 | 200 | 1 | — |
| `ferry` | Ferry | 56.00 | 1.1 | **1.5** | 0 | 50 | 100 | 1 | — |
| `fishboat` | Boat | 40.00 | 1.5 | **2.1** | 0 | 0 | 0 | 1 | — |
| `galley` | Galley | 50.00 | 1.2 | **1.7** | 0 | 900 | 800 | 1 | — |

<a id="ukrsta--конюшня"></a>
<a id="production-ukr-ukrsta"></a>
<a id="конюшня--ukrsta"></a>
### `ukrsta` — Stable

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cossackregister` | Register Cossack | 10.50 | 5.7 | **8.0** | 70 | 15 | 0 | 1 | 60 |
| `cossacksich` | Sich Cossack | 13.50 | 4.4 | **6.2** | 130 | 0 | 2 | 1 | 60 |
| `hetman` | Hetman | 16.50 | 3.6 | **5.1** | 150 | 150 | 10 | 1 | 90 |

<a id="ukrtem--православная-церковь"></a>
<a id="production-ukr-ukrtem"></a>
<a id="православная-церковь--ukrtem"></a>
### `ukrtem` — Orthodox Cathedral

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `pope` | Pope | 20.00 | 3.0 | **4.2** | 40 | 20 | 0 | 1 | — |

[↑ to contents](#содержание)

<a id="ven--venice-венеция"></a>
<a id="венеция"></a>
## Venice (`ven`)
<a id="eurmil--мельница-12"></a>
<a id="production-ven-eurmil"></a>
<a id="мельница--eurmil-16"></a>
### `eurmil` — Mill

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

<a id="eurpor--порт-11"></a>
<a id="production-ven-eurpor"></a>
<a id="порт--eurpor-15"></a>
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
<a id="production-ven-venart"></a>
<a id="артиллерийское-депо--venart"></a>
### `venart` — Artillery Depot

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cannon` | Cannon | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| `howitzer` | Howitzer | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| `mortar` | Bombard | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| `multicannon` | Multi-barrelled Cannon | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

<a id="venba2--казарма-18в"></a>
<a id="production-ven-venba2"></a>
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
<a id="production-ven-venbar"></a>
<a id="казарма-17в--venbar"></a>
### `venbar` — Barracks, 17th century

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer` | Drummer, 17th century | 5.00 | 12.0 | **16.8** | 60 | 20 | 0 | 1 | — |
| `musketeer` | Musketeer, 17th century | 6.00 | 10.0 | **14.0** | 45 | 6 | 5 | 1 | — |
| `officer` | Officer, 17th century | 10.00 | 6.0 | **8.4** | 50 | 150 | 30 | 1 | — |
| `pikeman` | Pikeman, 17th century | 4.50 | 13.3 | **18.7** | 25 | 3 | 20 | 1 | — |

<a id="vencen--городской-центр"></a>
<a id="production-ven-vencen"></a>
<a id="городской-центр--vencen"></a>
### `vencen` — Town Hall

| Unit | name | Time (g-sec) | temp (units/g-min) | tempo (units/real-min@fast) | F | G | I | farm | food consumption |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `peaspa` | Peasant | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

<a id="vendip--дипломатический-центр"></a>
<a id="production-ven-vendip"></a>
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
<a id="production-ven-vensta"></a>
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
<a id="production-ven-ventem"></a>
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
