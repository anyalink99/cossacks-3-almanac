<a id="здания"></a>
# Buildings

[← Quick reference](../README.md)

Some buildings have a separate national variant; others use an architectural
set shared by several nations. The canonical localized name is shown first.
The internal code beside it is only for exact identification.

Prices below are for the **first** copy. Each additional building of the same
type may cost more. The first six prices are listed in
[Scaling building prices](../../reports/economy/scaling_prices.md).

<a id="расшифровка-колонок"></a>
## Column guide

| Column | Meaning |
|---|---|
| **Building** | Canonical name and internal code |
| **Nation / Nations** | Nations that can build this variant |
| **Health** | Health of the completed building |
| **Construction time** | Game seconds with one builder. Additional peasants reduce it; see [Construction and repair](../../recon/world/economy/building_mechanics.md). |
| **Price growth** | How much each additional copy costs. 100% means the same price; 300% means three times the previous price. |
| **Food / Wood / Stone / Gold / Iron / Coal** | Cost of the first copy |
| **Population** | Amount added to the population limit |
| **Produces** | Canonical names of units created by the building |
| **Notes** | Weapons, capacity, gathering, and other special properties |

Bold values differ from the most common value in that column.

<a id="строительство-и-ремонт"></a>
## Construction and repair

The full mechanics are covered in
[Building construction, repair, and destruction](../../recon/world/economy/building_mechanics.md).

- Additional builders speed up construction almost proportionally, but only a
  limited number can stand around each building.
- An unfinished building has only one third of its normal protection.
- Any building under construction can be captured, including a Tower.
- One peasant repairs about 29 health per game second.
- Canceling construction or an order refunds its full paid cost.
- Destroying a working building refunds paid orders still in its queue.

<a id="переход-в-xviii-век"></a>
## Advancing to the 18th century

The advance is researched in the Town Hall after building an Academy, a
Cathedral, and an Artillery Depot.

<a id="цена-перехода"></a>
### Cost of the advance

| Nation | Food | Gold | Iron | Coal | Required buildings |
|---|---:|---:|---:|---:|---|
| Most nations | 30,000 | 5,000 | 2,000 | 2,000 | Academy, Cathedral, Artillery Depot |
| France | 40,000 | 3,500 | 4,000 | 2,000 | Academy, Cathedral, Artillery Depot |
| England | 25,000 | 5,000 | 5,500 | 2,000 | Academy, Cathedral, Artillery Depot |
| Poland | 30,000 | 4,800 | 2,200 | 2,000 | Academy, Cathedral, Artillery Depot |
| Ukraine, Turkey, Algeria | — | — | — | — | Advance unavailable |

The research itself takes 9.38 game seconds. Ukraine, Turkey, and Algeria
remain in the 17th century and compensate with unique troops.

<a id="содержание"></a>
## Contents

**[Buildings by nation](#постройки-по-нациям)**
  - [Town Hall (`cen`)](#cen--городской-центр)
  - [Housing (`hou`)](#hou--дом)
  - [Barracks, 17th century (`bar`)](#bar--казарма-17-в)
  - [Barracks, 18th century (`ba2`)](#ba2--казарма-18-в)
  - [Blacksmith (`bla`)](#bla--кузница)
  - [Stable (`sta`)](#sta--конюшня)
  - [Cathedral (`tem`)](#tem--собор)
  - [Academy (`aca`)](#aca--академия)
  - [Artillery Depot (`art`)](#art--артиллерийское-депо)
  - [Diplomatic Center (`dip`)](#dip--дипломатический-центр)
**[General buildings (by clusters)](#общие-постройки-по-кластерам)**
  - [mil - Mill](#mil--мельница)
  - [sto — Storehouse](#sto--склад)
  - [mar — Market](#mar--рынок)
  - [por — Shipyard](#por--порт)
  - [tow - Tower](#tow--башня)
  - [gol - Gold Mine](#gol--золотая-шахта)
  - [iro - Iron Mine](#iro--железная-шахта)
  - [coa - Coal mine](#coa--угольная-шахта)
  - [swa - Stone wall](#swa--каменная-стена)
  - [sga - Gate](#sga--каменные-ворота)
  - [wga - Gate](#wga--деревянные-ворота)
  - [wwa - Palisade](#wwa--палисад)
**[Mines - upgrades (gol/iro/coa)](#шахты--апгрейды-golirocoa)**

<a id="постройки-по-нациям"></a>
## Buildings by nation

Summary: for each type of building - parameters for all nations (where they exist). **Bold**—deviations from the base value (column mode).

<a id="cen--городской-центр"></a>
<a id="городской-центр-cen"></a>
### Town Hall (`cen`)

| Building | Nation | Health | Construction time | Price growth | Food | Wood | Stone | Gold | Iron | Coal | Population | Produces |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Town Hall** `algcen` | Algeria | **5500** | 156.25 | 300 | 0 | **450** | 700 | 0 | 0 | 0 | **50** | Peasant (`peaaus`), Peasant (`peaeng`), Peasant (`peapol`), Serf (`pearus`), Peasant (`peasco`), +3 more |
| **Town Hall** `auscen` | Austria | 4000 | **46.88** | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | Peasant (`peaaus`), Peasant (`peaeng`), Peasant (`peapol`), Serf (`pearus`), Peasant (`peasco`), +3 more |
| **Town Hall** `bavcen` | Bavaria | 4000 | 156.25 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | Peasant (`peaaus`), Peasant (`peaeng`), Peasant (`peapol`), Serf (`pearus`), Peasant (`peasco`), +3 more |
| **Town Hall** `dencen` | Denmark | **4030** | 156.25 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | Peasant (`peaaus`), Peasant (`peaeng`), Peasant (`peapol`), Serf (`pearus`), Peasant (`peasco`), +3 more |
| **Town Hall** `engcen` | England | **4030** | 156.25 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | Peasant (`peaaus`), Peasant (`peaeng`), Peasant (`peapol`), Serf (`pearus`), Peasant (`peasco`), +3 more |
| **Town Hall** `fracen` | France | **4500** | 156.25 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | Peasant (`peaaus`), Peasant (`peaeng`), Peasant (`peapol`), Serf (`pearus`), Peasant (`peasco`), +3 more |
| **Town Hall** `huncen` | Hungary | 4000 | 156.25 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | Peasant (`peaaus`), Peasant (`peaeng`), Peasant (`peapol`), Serf (`pearus`), Peasant (`peasco`), +3 more |
| **Town Hall** `netcen` | Netherlands | **4950** | 156.25 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | Peasant (`peaaus`), Peasant (`peaeng`), Peasant (`peapol`), Serf (`pearus`), Peasant (`peasco`), +3 more |
| **Town Hall** `piecen` | Piedmont | 4000 | 156.25 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | Peasant (`peaaus`), Peasant (`peaeng`), Peasant (`peapol`), Serf (`pearus`), Peasant (`peasco`), +3 more |
| **Town Hall** `polcen` | Poland | **4300** | 156.25 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | Peasant (`peaaus`), Peasant (`peaeng`), Peasant (`peapol`), Serf (`pearus`), Peasant (`peasco`), +3 more |
| **Town Hall** `porcen` | Portugal | 4000 | 156.25 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | Peasant (`peaaus`), Peasant (`peaeng`), Peasant (`peapol`), Serf (`pearus`), Peasant (`peasco`), +3 more |
| **Town Hall** `prucen` | Prussia | **4200** | 156.25 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | Peasant (`peaaus`), Peasant (`peaeng`), Peasant (`peapol`), Serf (`pearus`), Peasant (`peasco`), +3 more |
| **Town Hall** `ruscen` | Russia | **4050** | 156.25 | 300 | 0 | **680** | 700 | 0 | 0 | 0 | **75** | Peasant (`peaaus`), Peasant (`peaeng`), Peasant (`peapol`), Serf (`pearus`), Peasant (`peasco`), +3 more |
| **Town Hall** `saxcen` | Saxony | 4000 | 156.25 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | Peasant (`peaaus`), Peasant (`peaeng`), Peasant (`peapol`), Serf (`pearus`), Peasant (`peasco`), +3 more |
| **Town Hall** `scocen` | Scotland | 4000 | 156.25 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | Peasant (`peaaus`), Peasant (`peaeng`), Peasant (`peapol`), Serf (`pearus`), Peasant (`peasco`), +3 more |
| **Town Hall** `spacen` | Spain | **4250** | 156.25 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | Peasant (`peaaus`), Peasant (`peaeng`), Peasant (`peapol`), Serf (`pearus`), Peasant (`peasco`), +3 more |
| **Town Hall** `swecen` | Sweden | **5000** | 156.25 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | Peasant (`peaaus`), Peasant (`peaeng`), Peasant (`peapol`), Serf (`pearus`), Peasant (`peasco`), +3 more |
| **Town Hall** `swicen` | Switzerland | 4000 | 156.25 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | Peasant (`peaaus`), Peasant (`peaeng`), Peasant (`peapol`), Serf (`pearus`), Peasant (`peasco`), +3 more |
| **Town Hall** `turcen` | Turkey | 4000 | 156.25 | 300 | 0 | **600** | **500** | 0 | 0 | 0 | 100 | Peasant (`peaaus`), Peasant (`peaeng`), Peasant (`peapol`), Serf (`pearus`), Peasant (`peasco`), +3 more |
| **Town Hall** `ukrcen` | Ukraine | **5300** | 156.25 | **400** | 0 | 700 | **0** | 0 | 0 | 0 | **200** | Peasant (`peaaus`), Peasant (`peaeng`), Peasant (`peapol`), Serf (`pearus`), Peasant (`peasco`), +3 more |
| **Town Hall** `vencen` | Venice | **5100** | 156.25 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | Peasant (`peaaus`), Peasant (`peaeng`), Peasant (`peapol`), Serf (`pearus`), Peasant (`peasco`), +3 more |

<a id="hou--дом"></a>
<a id="дом-hou"></a>
### Housing (`hou`)

| Building | Nation | Health | Construction time | Price growth | Food | Wood | Stone | Gold | Iron | Coal | Population | Produces |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Housing** `alghou` | Algeria | **4300** | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| **Housing** `aushou` | Austria | 4000 | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| **Housing** `bavhou` | Bavaria | 4000 | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| **Housing** `denhou` | Denmark | 4000 | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| **Housing** `enghou` | England | **5000** | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| **Housing** `frahou` | France | 4000 | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| **Housing** `hunhou` | Hungary | 4000 | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| **Housing** `nethou` | Netherlands | **4500** | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| **Housing** `piehou` | Piedmont | 4000 | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| **Housing** `polhou` | Poland | **4100** | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| **Housing** `porhou` | Portugal | 4000 | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| **Housing** `pruhou` | Prussia | **4500** | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| **Izba** `rushou` | Russia | **5000** | 31.25 | 104 | 0 | **120** | **0** | 0 | 0 | 0 | 25 | — |
| **Housing** `saxhou` | Saxony | 4000 | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| **Housing** `scohou` | Scotland | 4000 | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| **Housing** `spahou` | Spain | **4200** | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| **Housing** `swehou` | Sweden | **5000** | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| **Housing** `swihou` | Switzerland | 4000 | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| **Housing** `turhou` | Turkey | 4000 | 31.25 | **106** | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| **Hut** `ukrhou` | Ukraine | **4150** | 31.25 | **105** | 0 | **120** | **0** | 0 | 0 | 0 | 25 | — |
| **Housing** `venhou` | Venice | **5000** | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |

<a id="bar--казарма-17-в"></a>
<a id="казарма-17-в-bar"></a>
### Barracks, 17th century (`bar`)

| Building | Nation | Health | Construction time | Price growth | Food | Wood | Stone | Gold | Iron | Coal | Population | Produces |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Barracks** `algbar` | Algeria | **35000** | 93.75 | 500 | 0 | **400** | **400** | **0** | 0 | 0 | **50** | Archer (`archer`), Turkish archer (`archertur`), Drummer, 17th century (`drummer`), Drummer, 17th century (`drummerrus`), Drummer, 17th century (`drummertur`), +24 more |
| **Barracks, 17th century** `ausbar` | Austria | 40000 | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | Archer (`archer`), Turkish archer (`archertur`), Drummer, 17th century (`drummer`), Drummer, 17th century (`drummerrus`), Drummer, 17th century (`drummertur`), +24 more |
| **Barracks, 17th century** `bavbar` | Bavaria | 40000 | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | Archer (`archer`), Turkish archer (`archertur`), Drummer, 17th century (`drummer`), Drummer, 17th century (`drummerrus`), Drummer, 17th century (`drummertur`), +24 more |
| **Barracks, 17th century** `denbar` | Denmark | 40000 | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | Archer (`archer`), Turkish archer (`archertur`), Drummer, 17th century (`drummer`), Drummer, 17th century (`drummerrus`), Drummer, 17th century (`drummertur`), +24 more |
| **Barracks, 17th century** `engbar` | England | 40000 | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | Archer (`archer`), Turkish archer (`archertur`), Drummer, 17th century (`drummer`), Drummer, 17th century (`drummerrus`), Drummer, 17th century (`drummertur`), +24 more |
| **Barracks, 17th century** `frabar` | France | 40000 | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | Archer (`archer`), Turkish archer (`archertur`), Drummer, 17th century (`drummer`), Drummer, 17th century (`drummerrus`), Drummer, 17th century (`drummertur`), +24 more |
| **Barracks, 17th century** `hunbar` | Hungary | 40000 | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | Archer (`archer`), Turkish archer (`archertur`), Drummer, 17th century (`drummer`), Drummer, 17th century (`drummerrus`), Drummer, 17th century (`drummertur`), +24 more |
| **Barracks, 17th century** `netbar` | Netherlands | 40000 | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | Archer (`archer`), Turkish archer (`archertur`), Drummer, 17th century (`drummer`), Drummer, 17th century (`drummerrus`), Drummer, 17th century (`drummertur`), +24 more |
| **Barracks, 17th century** `piebar` | Piedmont | 40000 | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | Archer (`archer`), Turkish archer (`archertur`), Drummer, 17th century (`drummer`), Drummer, 17th century (`drummerrus`), Drummer, 17th century (`drummertur`), +24 more |
| **Barracks, 17th century** `polbar` | Poland | 40000 | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | Archer (`archer`), Turkish archer (`archertur`), Drummer, 17th century (`drummer`), Drummer, 17th century (`drummerrus`), Drummer, 17th century (`drummertur`), +24 more |
| **Barracks, 17th century** `porbar` | Portugal | 40000 | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | Archer (`archer`), Turkish archer (`archertur`), Drummer, 17th century (`drummer`), Drummer, 17th century (`drummerrus`), Drummer, 17th century (`drummertur`), +24 more |
| **Barracks, 17th century** `prubar` | Prussia | 40000 | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | Archer (`archer`), Turkish archer (`archertur`), Drummer, 17th century (`drummer`), Drummer, 17th century (`drummerrus`), Drummer, 17th century (`drummertur`), +24 more |
| **Strelets Barracks** `rusbar` | Russia | **25000** | **78.12** | **300** | 0 | **200** | **20** | **0** | 0 | 0 | **25** | Archer (`archer`), Turkish archer (`archertur`), Drummer, 17th century (`drummer`), Drummer, 17th century (`drummerrus`), Drummer, 17th century (`drummertur`), +24 more |
| **Barracks, 17th century** `saxbar` | Saxony | 40000 | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | Archer (`archer`), Turkish archer (`archertur`), Drummer, 17th century (`drummer`), Drummer, 17th century (`drummerrus`), Drummer, 17th century (`drummertur`), +24 more |
| **Barracks, 17th century** `scobar` | Scotland | **30000** | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | Archer (`archer`), Turkish archer (`archertur`), Bagpiper (`bagpiper`), Drummer, 17th century (`drummer`), Drummer, 17th century (`drummerrus`), +25 more |
| **Barracks, 17th century** `spabar` | Spain | 40000 | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | Archer (`archer`), Turkish archer (`archertur`), Drummer, 17th century (`drummer`), Drummer, 17th century (`drummerrus`), Drummer, 17th century (`drummertur`), +24 more |
| **Barracks, 17th century** `swebar` | Sweden | 40000 | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | Archer (`archer`), Turkish archer (`archertur`), Drummer, 17th century (`drummer`), Drummer, 17th century (`drummerrus`), Drummer, 17th century (`drummertur`), +24 more |
| **Barracks, 17th century** `swibar` | Switzerland | 40000 | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | Archer (`archer`), Turkish archer (`archertur`), Drummer, 17th century (`drummer`), Drummer, 17th century (`drummerrus`), Drummer, 17th century (`drummertur`), +24 more |
| **Barracks** `turbar` | Turkey | **35000** | 93.75 | 500 | 0 | **400** | **400** | **0** | 0 | 0 | **50** | Archer (`archer`), Turkish archer (`archertur`), Drummer, 17th century (`drummer`), Drummer, 17th century (`drummerrus`), Drummer, 17th century (`drummertur`), +24 more |
| **Cossack House** `ukrbar` | Ukraine | **20000** | 93.75 | **300** | 0 | **150** | **150** | **0** | 0 | 0 | **75** | Archer (`archer`), Turkish archer (`archertur`), Drummer, 17th century (`drummer`), Drummer, 17th century (`drummerrus`), Drummer, 17th century (`drummertur`), +24 more |
| **Barracks, 17th century** `venbar` | Venice | 40000 | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | Archer (`archer`), Turkish archer (`archertur`), Drummer, 17th century (`drummer`), Drummer, 17th century (`drummerrus`), Drummer, 17th century (`drummertur`), +24 more |

<a id="ba2--казарма-18-в"></a>
<a id="казарма-18-в-ba2"></a>
### Barracks, 18th century (`ba2`)

| Building | Nation | Health | Construction time | Price growth | Food | Wood | Stone | Gold | Iron | Coal | Population | Produces |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Barracks, 18th century** `ausba2` | Austria | 55000 | 5625.0 | 200 | 0 | 1700 | 2950 | 4000 | 0 | 0 | 250 | Bow Clansman (`archersco`), Bagpiper (`bagpiper`), Chasseur (`chasseur`), Drummer, 18th century (`drummer18`), Grenadier (`grenadier`), +19 more |
| **Bar…5522 tokens truncated…megun`), Howitzer (`howitzer`), Bombard (`mortar`), Multi-barrelled Cannon (`multicannon`) |
| **Artillery Depot** `saxart` | Saxony | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | Cannon (`cannon`), Frame gun (`framegun`), Howitzer (`howitzer`), Bombard (`mortar`), Multi-barrelled Cannon (`multicannon`) |
| **Artillery Depot** `scoart` | Scotland | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | Cannon (`cannon`), Frame gun (`framegun`), Howitzer (`howitzer`), Bombard (`mortar`), Multi-barrelled Cannon (`multicannon`) |
| **Artillery Depot** `spaart` | Spain | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | Cannon (`cannon`), Frame gun (`framegun`), Howitzer (`howitzer`), Bombard (`mortar`), Multi-barrelled Cannon (`multicannon`) |
| **Artillery Depot** `sweart` | Sweden | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | Cannon (`cannon`), Frame gun (`framegun`), Howitzer (`howitzer`), Bombard (`mortar`), Multi-barrelled Cannon (`multicannon`) |
| **Artillery Depot** `swiart` | Switzerland | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | Cannon (`cannon`), Frame gun (`framegun`), Howitzer (`howitzer`), Bombard (`mortar`), Multi-barrelled Cannon (`multicannon`) |
| **Artillery Depot** `turart` | Turkey | 40000 | 245.94 | 200 | 0 | **500** | **1200** | 0 | 0 | 1400 | 0 | Cannon (`cannon`), Frame gun (`framegun`), Howitzer (`howitzer`), Bombard (`mortar`), Multi-barrelled Cannon (`multicannon`) |
| **Artillery Depot** `ukrart` | Ukraine | 40000 | 245.94 | 200 | 0 | **4250** | **4400** | **100** | 0 | 1400 | 0 | Cannon (`cannon`), Frame gun (`framegun`), Howitzer (`howitzer`), Bombard (`mortar`), Multi-barrelled Cannon (`multicannon`) |
| **Artillery Depot** `venart` | Venice | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | Cannon (`cannon`), Frame gun (`framegun`), Howitzer (`howitzer`), Bombard (`mortar`), Multi-barrelled Cannon (`multicannon`) |

<a id="dip--дипломатический-центр"></a>
<a id="кузница-bla"></a>
### Diplomatic Center (`dip`)

| Building | Nation | Health | Construction time | Price growth | Food | Wood | Stone | Gold | Iron | Coal | Population | Produces |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Diplomatic Center** `algdip` | Algeria | **5500** | 312.5 | 100 | 0 | **4600** | **2020** | 0 | 0 | 0 | 0 | Archer (mercenary) (`archerdip`), Turkish archer (mercenary) (`archerturdip`), Sich Cossack (mercenary) (`cossacksichdip`), Dragoon, 18th century (mercenary) (`dragoon18dip`), Grenadier (mercenary) (`grenadierdip`), +3 more |
| **Diplomatic Center** `ausdip` | Austria | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | Archer (mercenary) (`archerdip`), Turkish archer (mercenary) (`archerturdip`), Sich Cossack (mercenary) (`cossacksichdip`), Dragoon, 18th century (mercenary) (`dragoon18dip`), Grenadier (mercenary) (`grenadierdip`), +3 more |
| **Diplomatic Center** `bavdip` | Bavaria | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | Archer (mercenary) (`archerdip`), Turkish archer (mercenary) (`archerturdip`), Sich Cossack (mercenary) (`cossacksichdip`), Dragoon, 18th century (mercenary) (`dragoon18dip`), Grenadier (mercenary) (`grenadierdip`), +3 more |
| **Diplomatic Center** `dendip` | Denmark | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | Archer (mercenary) (`archerdip`), Turkish archer (mercenary) (`archerturdip`), Sich Cossack (mercenary) (`cossacksichdip`), Dragoon, 18th century (mercenary) (`dragoon18dip`), Grenadier (mercenary) (`grenadierdip`), +3 more |
| **Diplomatic Center** `engdip` | England | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | Archer (mercenary) (`archerdip`), Turkish archer (mercenary) (`archerturdip`), Sich Cossack (mercenary) (`cossacksichdip`), Dragoon, 18th century (mercenary) (`dragoon18dip`), Grenadier (mercenary) (`grenadierdip`), +3 more |
| **Diplomatic Center** `fradip` | France | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | Archer (mercenary) (`archerdip`), Turkish archer (mercenary) (`archerturdip`), Sich Cossack (mercenary) (`cossacksichdip`), Dragoon, 18th century (mercenary) (`dragoon18dip`), Grenadier (mercenary) (`grenadierdip`), +3 more |
| **Diplomatic Center** `hundip` | Hungary | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | Archer (mercenary) (`archerdip`), Turkish archer (mercenary) (`archerturdip`), Sich Cossack (mercenary) (`cossacksichdip`), Dragoon, 18th century (mercenary) (`dragoon18dip`), Grenadier (mercenary) (`grenadierdip`), +3 more |
| **Diplomatic Center** `netdip` | Netherlands | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | Archer (mercenary) (`archerdip`), Turkish archer (mercenary) (`archerturdip`), Sich Cossack (mercenary) (`cossacksichdip`), Dragoon, 18th century (mercenary) (`dragoon18dip`), Grenadier (mercenary) (`grenadierdip`), +3 more |
| **Diplomatic Center** `piedip` | Piedmont | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | Archer (mercenary) (`archerdip`), Turkish archer (mercenary) (`archerturdip`), Sich Cossack (mercenary) (`cossacksichdip`), Dragoon, 18th century (mercenary) (`dragoon18dip`), Grenadier (mercenary) (`grenadierdip`), +3 more |
| **Diplomatic Center** `poldip` | Poland | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | Archer (mercenary) (`archerdip`), Turkish archer (mercenary) (`archerturdip`), Sich Cossack (mercenary) (`cossacksichdip`), Dragoon, 18th century (mercenary) (`dragoon18dip`), Grenadier (mercenary) (`grenadierdip`), +3 more |
| **Diplomatic Center** `pordip` | Portugal | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | Archer (mercenary) (`archerdip`), Turkish archer (mercenary) (`archerturdip`), Sich Cossack (mercenary) (`cossacksichdip`), Dragoon, 18th century (mercenary) (`dragoon18dip`), Grenadier (mercenary) (`grenadierdip`), +3 more |
| **Diplomatic Center** `prudip` | Prussia | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | Archer (mercenary) (`archerdip`), Turkish archer (mercenary) (`archerturdip`), Sich Cossack (mercenary) (`cossacksichdip`), Dragoon, 18th century (mercenary) (`dragoon18dip`), Grenadier (mercenary) (`grenadierdip`), +3 more |
| **Diplomatic Center** `rusdip` | Russia | **6500** | 312.5 | 100 | 0 | **7900** | **3700** | 0 | 0 | 0 | 0 | Archer (mercenary) (`archerdip`), Turkish archer (mercenary) (`archerturdip`), Sich Cossack (mercenary) (`cossacksichdip`), Dragoon, 18th century (mercenary) (`dragoon18dip`), Grenadier (mercenary) (`grenadierdip`), +3 more |
| **Diplomatic Center** `saxdip` | Saxony | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | Archer (mercenary) (`archerdip`), Turkish archer (mercenary) (`archerturdip`), Sich Cossack (mercenary) (`cossacksichdip`), Dragoon, 18th century (mercenary) (`dragoon18dip`), Grenadier (mercenary) (`grenadierdip`), +3 more |
| **Diplomatic Center** `scodip` | Scotland | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | Archer (mercenary) (`archerdip`), Turkish archer (mercenary) (`archerturdip`), Sich Cossack (mercenary) (`cossacksichdip`), Dragoon, 18th century (mercenary) (`dragoon18dip`), Grenadier (mercenary) (`grenadierdip`), +3 more |
| **Diplomatic Center** `spadip` | Spain | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | Archer (mercenary) (`archerdip`), Turkish archer (mercenary) (`archerturdip`), Sich Cossack (mercenary) (`cossacksichdip`), Dragoon, 18th century (mercenary) (`dragoon18dip`), Grenadier (mercenary) (`grenadierdip`), +3 more |
| **Diplomatic Center** `swedip` | Sweden | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | Archer (mercenary) (`archerdip`), Turkish archer (mercenary) (`archerturdip`), Sich Cossack (mercenary) (`cossacksichdip`), Dragoon, 18th century (mercenary) (`dragoon18dip`), Grenadier (mercenary) (`grenadierdip`), +3 more |
| **Diplomatic Center** `swidip` | Switzerland | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | Archer (mercenary) (`archerdip`), Turkish archer (mercenary) (`archerturdip`), Sich Cossack (mercenary) (`cossacksichdip`), Dragoon, 18th century (mercenary) (`dragoon18dip`), Grenadier (mercenary) (`grenadierdip`), +3 more |
| **Diplomatic Center** `turdip` | Turkey | **5500** | 312.5 | 100 | 0 | **4600** | **2020** | 0 | 0 | 0 | 0 | Archer (mercenary) (`archerdip`), Turkish archer (mercenary) (`archerturdip`), Sich Cossack (mercenary) (`cossacksichdip`), Dragoon, 18th century (mercenary) (`dragoon18dip`), Grenadier (mercenary) (`grenadierdip`), +3 more |
| **Diplomatic Center** `ukrdip` | Ukraine | **5000** | 312.5 | 100 | 0 | **3900** | **2700** | 0 | 0 | 0 | 0 | Archer (mercenary) (`archerdip`), Turkish archer (mercenary) (`archerturdip`), Sich Cossack (mercenary) (`cossacksichdip`), Dragoon, 18th century (mercenary) (`dragoon18dip`), Grenadier (mercenary) (`grenadierdip`), +3 more |
| **Diplomatic Center** `vendip` | Venice | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | Archer (mercenary) (`archerdip`), Turkish archer (mercenary) (`archerturdip`), Sich Cossack (mercenary) (`cossacksichdip`), Dragoon, 18th century (mercenary) (`dragoon18dip`), Grenadier (mercenary) (`grenadierdip`), +3 more |

<a id="общие-постройки-по-кластерам"></a>
<a id="общие-постройки-по-архитектурным-группам"></a>
## Common buildings (by cluster)

<a id="mil--мельница"></a>
<a id="мельница-mil"></a>
### Mill (`mil`)
| Building | Nations | Health | Construction time | Price growth | Food | Wood | Stone | Gold | Iron | Coal | Notes |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Mill** `eurmil` | Austria, Bavaria, Denmark, England, France, Hungary, Netherlands, Piedmont, Poland, Portugal, Prussia, Saxony, Scotland, Spain, Sweden, Switzerland, Venice | 20000 | 93.75 | 200 | 0 | 30 | 150 | 0 | 0 | 0 | — |
| **Mill** `rusmil` | Russia, Ukraine | 15000 | 93.75 | 200 | 0 | 210 | 0 | 0 | 0 | 0 | — |
| **Mill** `turmil` | Algeria, Turkey | 20000 | 93.75 | 200 | 0 | 30 | 150 | 0 | 0 | 0 | — |

<a id="sto--склад"></a>
<a id="склад-sto"></a>
### Storehouse (`sto`)

| Building | Nations | Health | Construction time | Price growth | Food | Wood | Stone | Gold | Iron | Coal | Notes |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Storehouse** `eursto` | Austria, Bavaria, Denmark, England, France, Hungary, Netherlands, Piedmont, Prussia, Saxony, Scotland, Sweden, Switzerland, Venice | 10000 | 31.25 | 150 | 0 | 50 | 20 | 0 | 0 | 0 | — |
| **Storehouse** `russto` | Poland, Russia, Ukraine | 10000 | 31.25 | 200 | 0 | 50 | 20 | 0 | 0 | 0 | — |
| **Storehouse** `spasto` | Portugal, Spain | 10000 | 31.25 | 150 | 0 | 20 | 20 | 0 | 0 | 0 | — |
| **Storehouse** `tursto` | Algeria, Turkey | 10000 | 31.25 | 200 | 0 | 30 | 10 | 0 | 0 | 0 | — |

<a id="mar--рынок"></a>
<a id="рынок-mar"></a>
### Market (`mar`)

| Building | Nations | Health | Construction time | Price growth | Food | Wood | Stone | Gold | Iron | Coal | Notes |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Market** `eurmar` | Austria, Bavaria, Denmark, England, France, Hungary, Netherlands, Piedmont, Poland, Prussia, Saxony, Scotland, Sweden, Switzerland, Venice | 4000 | 234.38 | 2000 | 0 | 450 | 0 | 0 | 0 | 0 | — |
| **Market** `rusmar` | Russia, Ukraine | 4000 | 234.38 | 2000 | 0 | 450 | 0 | 0 | 0 | 0 | — |
| **Market** `spamar` | Portugal, Spain | 4000 | 156.25 | 2000 | 0 | 450 | 0 | 0 | 0 | 0 | — |
| **Bazaar** `turmar` | Algeria, Turkey | 4500 | 234.38 | 1500 | 0 | 450 | 150 | 0 | 0 | 0 | — |

<a id="por--порт"></a>
<a id="порт-por"></a>
### Shipyard (`por`)

| Building | Nations | Health | Construction time | Price growth | Food | Wood | Stone | Gold | Iron | Coal | Notes |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Shipyard** `eurpor` | Austria, Bavaria, Denmark, England, France, Hungary, Netherlands, Piedmont, Poland, Prussia, Saxony, Scotland, Spain, Sweden, Switzerland, Venice | 50000 | 1562.5 | 150 | 0 | 1600 | 800 | 0 | 400 | 0 | — |
| **Shipyard** `porpor` | Portugal | 50000 | 1562.5 | 150 | 0 | 1600 | 800 | 0 | 400 | 0 | damage 1000; range 28.1t; gold upkeep 250 |
| **Shipyard** `ruspor` | Russia | 45000 | 1562.5 | 150 | 0 | 1200 | 800 | 0 | 400 | 0 | — |
| **Shipyard** `turpor` | Algeria, Turkey | 40000 | 1562.5 | 150 | 0 | 800 | 800 | 0 | 400 | 0 | — |
| **Shipyard** `ukrpor` | Ukraine | 45000 | 1562.5 | 150 | 0 | 2000 | 0 | 0 | 0 | 0 | — |

<a id="tow--башня"></a>
<a id="башня-tow"></a>
### Tower (`tow`)

| Building | Nations | Health | Construction time | Price growth | Food | Wood | Stone | Gold | Iron | Coal | Notes |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Tower** `eurtow` | Austria, Bavaria, Denmark, England, France, Hungary, Netherlands, Piedmont, Poland, Portugal, Prussia, Saxony, Scotland, Spain, Sweden, Switzerland, Venice | 20000 | 1230.31 | 120 | 0 | 100 | 100 | 150 | 0 | 0 | damage 1000; range 28.1t; gold upkeep 500 |
| **Tower** `rustow` | Russia | 21000 | 1476.56 | 125 | 0 | 100 | 100 | 150 | 0 | 0 | damage 1000; range 28.1t; gold upkeep 500 |
| **Tower** `turtow` | Algeria, Turkey | 22500 | 984.38 | 125 | 0 | 150 | 90 | 100 | 0 | 0 | damage 1200; range 30.0t; gold upkeep 500 |

<a id="башня--кратко"></a>
#### Tower summary

A complete analysis of shooting, review, garrison and strategy - in
[`../../recon/world/combat/towers.md`](../../recon/world/combat/towers.md).
Brief parameters of the basic European tower (`eurtow`):

| Parameter | Meaning | Note |
|---|---:|---|
| HP | 20,000 | rus 21 000, tur 22 500 |
| `vision` | 3 → 32 FOW tiles | less than the average hussar |
| `searchradius` | 1400 px = 26.25 t | target auto-lock radius |
| Damage | 1000 | `cannonball` |
| `weapon_pause` | 400 frames = 12.5 g-sec | rus 9.4 g-sec, tur 15.6 g-sec |
| Shot range | 1500 px = 28.13 t | tur 30 t |
| Scatter | 100 px = 1.88 t | rus 125 |
| Shot cost | 10 iron + 30 coal | tur: 15 iron + 40 coal |
| Contents | `consume[gold] = 500` → **0.8 gold / g-sec** (≈ 67 / real-min @ fast) | formula `× 32 / 20000`, with `gold = 0` the turret silently stops firing |
| Capture | `bcapture = False` | the tower is **never** captured after construction |

5 upgrade levels `eurtow.1..5` reduce `weapon_pause` to
× 0.467 from base → fire frequency **× 2.14**. The full list is in
[05_upgrades/README.md → tow](../05_upgrades/README.md#tow--башня-скорость-перезарядки).
<a id="gol--золотая-шахта"></a>
<a id="золотая-шахта-gol"></a>
### Gold Mine (`gol`)

| Building | Nations | Health | Construction time | Price growth | Food | Wood | Stone | Gold | Iron | Coal | Notes |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Mine** `eurgol` | Algeria, Austria, Bavaria, Denmark, England, France, Hungary, Netherlands, Piedmont, Poland, Portugal, Prussia, Russia, Saxony, Scotland, Spain, Sweden, Switzerland, Turkey, Ukraine, Venice | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | produces gold; capacity 5 peasants |

<a id="iro--железная-шахта"></a>
<a id="железная-шахта-iro"></a>
### Iron Mine (`iro`)

| Building | Nations | Health | Construction time | Price growth | Food | Wood | Stone | Gold | Iron | Coal | Notes |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Mine** `euriro` | Algeria, Austria, Bavaria, Denmark, England, France, Hungary, Netherlands, Piedmont, Poland, Portugal, Prussia, Russia, Saxony, Scotland, Spain, Sweden, Switzerland, Turkey, Ukraine, Venice | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | produces iron; capacity 5 peasants |

<a id="coa--угольная-шахта"></a>
<a id="угольная-шахта-coa"></a>
### Coal Mine (`coa`)

| Building | Nations | Health | Construction time | Price growth | Food | Wood | Stone | Gold | Iron | Coal | Notes |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Mine** `eurcoa` | Algeria, Austria, Bavaria, Denmark, England, France, Hungary, Netherlands, Piedmont, Poland, Portugal, Prussia, Russia, Saxony, Scotland, Spain, Sweden, Switzerland, Turkey, Ukraine, Venice | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | produces coal; capacity 5 peasants |

<a id="swa--каменная-стена"></a>
<a id="каменная-стена-swa"></a>
### Stone Wall (`swa`)

| Building | Nations | Health | Construction time | Price growth | Food | Wood | Stone | Gold | Iron | Coal | Notes |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Wall** `eurswa` | Austria, Bavaria, Denmark, England, France, Hungary, Netherlands, Piedmont, Poland, Portugal, Prussia, Saxony, Scotland, Spain, Sweden, Switzerland, Venice | 50000 | 90.0 | 0 | 0 | 0 | 50 | 0 | 0 | 0 | stone upkeep 250 |
| **Wall** `russwa` | Russia | 50000 | 200.0 | 0 | 0 | 0 | 60 | 0 | 0 | 0 | stone upkeep 200 |
| **Wall** `turswa` | Algeria, Turkey | 50000 | 120.0 | 0 | 0 | 0 | 60 | 0 | 0 | 0 | stone upkeep 150 |

<a id="sga--каменные-ворота"></a>
<a id="каменные-ворота-sga"></a>
### Stone Gate (`sga`)

| Building | Nations | Health | Construction time | Price growth | Food | Wood | Stone | Gold | Iron | Coal | Notes |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Gate** `eursga` | Austria, Bavaria, Denmark, England, France, Hungary, Netherlands, Piedmont, Poland, Portugal, Prussia, Saxony, Scotland, Spain, Sweden, Switzerland, Venice | 32000 | 90.0 | 0 | 0 | 0 | 50 | 0 | 0 | 0 | stone upkeep 250 |
| **Gate** `russga` | Russia | 32000 | 200.0 | 0 | 0 | 0 | 60 | 0 | 0 | 0 | stone upkeep 200 |
| **Gate** `tursga` | Algeria, Turkey | 32000 | 120.0 | 0 | 0 | 0 | 60 | 0 | 0 | 0 | stone upkeep 150 |

<a id="wga--деревянные-ворота"></a>
<a id="деревянные-ворота-wga"></a>
### Wooden Gate (`wga`)

| Building | Nations | Health | Construction time | Price growth | Food | Wood | Stone | Gold | Iron | Coal | Notes |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Gate** `ukrwga` | Algeria, Austria, Bavaria, Denmark, England, France, Hungary, Netherlands, Piedmont, Poland, Portugal, Prussia, Russia, Saxony, Scotland, Spain, Sweden, Switzerland, Turkey, Ukraine, Venice | 1500 | 5.62 | 0 | 0 | 10 | 0 | 0 | 0 | 0 | wood upkeep 32 |

<a id="wwa--палисад"></a>
<a id="палисад-wwa"></a>
### Palisade (`wwa`)

| Building | Nations | Health | Construction time | Price growth | Food | Wood | Stone | Gold | Iron | Coal | Notes |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Palisade** `ukrwwa` | Algeria, Austria, Bavaria, Denmark, England, France, Hungary, Netherlands, Piedmont, Poland, Portugal, Prussia, Russia, Saxony, Scotland, Spain, Sweden, Switzerland, Turkey, Ukraine, Venice | 1500 | 5.62 | 0 | 0 | 10 | 0 | 0 | 0 | 0 | wood upkeep 32 |

<a id="шахты--апгрейды-golirocoa"></a>
<a id="улучшения-шахт"></a>
## Mines - upgrades (gol/iro/coa)

Each mine starts with `peasantabsorber=5`. 6 upgrades cumulatively bring up to **95 peasants** per mine.

| Level | +workers | Food | Gold | Cumulatively |
|---|---:|---:|---:|---:|
| `eurgol.1` | +5 | 1000 | 1250 | 10 |
| `eurgol.2` | +8 | 5250 | 4950 | 18 |
| `eurgol.3` | +10 | 12500 | 9250 | 28 |
| `eurgol.4` | +12 | 15800 | 18500 | 40 |
| `eurgol.5` | +15 | 19800 | 21050 | 55 |
| `eurgol.6` | +40 | 50200 | 25950 | 95 |
