<a id="здания"></a>
# Buildings

[← Quick reference](../README.md)

Some buildings have a separate national variant; others use an architectural
set shared by several nations. The canonical localized name is shown first.
The internal code beside it is only for exact identification.

Prices below are for the **first** copy. Each additional building of the same
type may cost more. The first six prices are listed in
[Scaling building prices](../../reports/economy/scaling_prices.md).

<a id="выберите-здание"></a>
## Choose a building

<a id="экономика-и-развитие"></a>
### Economy and development

| Article | What it contains |
|---|---|
| [Town Hall](town_hall.md) | National variants, cost, health, population, and available peasants |
| [Housing](housing.md) | Cost, health, construction time, and population |
| [Mill](mill.md) | Architectural variants and cost |
| [Storehouse](storehouse.md) | Architectural variants and cost |
| [Market](market.md) | Architectural variants; trading mechanics are covered separately |
| [Mines](mines.md) | Gold, Iron, and Coal Mines, capacity, and expansion levels |

<a id="войска-и-исследования"></a>
### Troops and research

| Article | What it contains |
|---|---|
| [Barracks, 17th Century](barracks_17.md) | National variants and trained troops |
| [Barracks, 18th Century](barracks_18.md) | National variants and trained troops |
| [Blacksmith](blacksmith.md) | Cost, health, and national variants |
| [Stable](stable.md) | National variants and available cavalry |
| [Cathedral](cathedral.md) | National variants and clergy |
| [Academy](academy.md) | Cost, health, and national variants |
| [Artillery Depot](artillery_depot.md) | National variants and available artillery |
| [Diplomatic Center](diplomatic_center.md) | Cost, health, and available mercenaries |

<a id="оборона-и-флот"></a>
### Defense and navy

| Article | What it contains |
|---|---|
| [Shipyard](shipyard.md) | National Shipyard variants |
| [Tower](tower.md) | Firing characteristics, upkeep, and national differences |
| [Walls, Gates, and Palisades](walls_and_gates.md) | Stone and wooden fortifications |


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
- One Peasant restores about 49.3 durability per game second.
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
