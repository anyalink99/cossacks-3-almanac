<a id="улучшения"></a>
# Upgrades

[← Quick reference](../README.md)

Upgrades are grouped by the building where they are researched: Academy,
Blacksmith, Mill, Stable, Barracks, Mine, Tower, Wall, and Shipyard.
The canonical localized name is shown first; the internal code is secondary.

<a id="выберите-место-исследования"></a>
## Choose a research location

| Article | What it contains |
|---|---|
| [Mines](mines.md) | Six capacity levels for Gold, Iron, and Coal Mines |
| [Academy](academy.md) | Gathering, construction, artillery, and other general research |
| [Mill](mill.md) | Food-gathering upgrades |
| [Blacksmith](blacksmith.md) | General military and economic upgrades |
| [Stable](stable.md) | Cavalry damage and protection |
| [17th-Century Barracks](barracks_17.md) | Damage and protection for 17th-century infantry |
| [18th-Century Barracks](barracks_18.md) | Damage and protection for 18th-century infantry |
| [Artillery Depot](artillery_depot.md) | Cannon upgrades |
| [Town Hall](town_hall.md) | Advancing to the 18th century |
| [Tower](tower.md) | Five reload-speed levels |
| [Walls and Palisades](walls_and_gates.md) | Converting a fortification section into a gate |
| [Shipyard and Ferry](shipyard.md) | Ship healing and Ferry capacity |


<a id="расшифровка-колонок"></a>
## Column guide

| Column | Meaning |
|---|---|
| **Upgrade** | Canonical name and internal code |
| **Nations** | Nations that can research it. A national variant with a different value appears in its own row. |
| **Effect** | What changes: damage, protection, gathering, construction time, and so on |
| **Value** | Size of the effect. For percentage effects, 50 means +50%. |
| **Food / Wood / Stone / Gold / Iron / Coal** | Research cost |
| **Time** | Research time in game seconds; the building is occupied during this period |

> One row represents one upgrade for one nation or a group of nations. When
> all nations share the same value, they are combined into one row.


<a id="математика-применения-апгрейдов"></a>
<a id="математика-применения-порядок-и-комбинирование"></a>
<a id="как-складываются-улучшения"></a>
## How upgrades combine

In almost every case, research order **does not affect** a unit’s or
building’s final characteristics. The game stores bonuses separately and
recalculates the result from the same base value.

Rounding can occasionally change price, health, Fishing Boat capacity, or
speed by one point. See [How upgrades are applied](../../recon/world/economy/upgrades_application.md)
for the technical details. In ordinary play, upgrades can be researched in
any convenient order without changing the final damage or protection.
