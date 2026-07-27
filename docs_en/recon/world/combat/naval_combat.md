<a id="recon-морской-бой"></a>
<a id="как-устроен-морской-бой"></a>
# How Naval Combat Works

[← How the game works](../../README.md)

Water forms a separate movement area in Cossacks 3. This article explains
how ships choose targets, why they cannot travel over land, how troops cross
water, and how warships differ from fishing vessels. Exact fields, functions,
and internal codes are collected under
[Technical details](#technical-details) and [Sources](#sources).

<a id="кратко"></a>
## TL;DR

- Naval units move over the water network and do not find paths over land
  [^1].
- Only a **Shipyard** produces ships. A nation's
  roster may include light vessels, Frigates, Ships of the Line, transports,
  and Boats.
- A **Ferry** carries infantry, cavalry, and artillery, then unloads
  them near another shore.
- A **Ship of the Line** consumes gold upkeep but is not affected by food
  shortages.
- **Naval formations** are mainly for squadron movement; see
  [Formations and Their Combat Bonuses §7](formations.md).
- Target selection respects connected water areas, preventing shots across
  an unrelated stretch of shoreline.

---

<a id="1-что-делает-юнит-морским"></a>
<a id="1-какие-юниты-относятся-к-флоту"></a>
## 1. Which units belong to the fleet

The game distinguishes four overlapping categories [^1]:

| Category | What it includes |
|---|---|
| Ships | All vessels that move over water. |
| Ships of the Line | Heavy warships with powerful weapons. |
| Ferry | A vessel that carries land units. |
| Boats | Economic vessels that gather food. |

These categories affect pathfinding, target selection, upkeep, and available
orders. Their internal flags are listed under
[Technical details](#technical-details).

---

<a id="2-регионы-и-pathfinding"></a>
<a id="2-водные-области-и-поиск-пути"></a>
## 2. Regions and pathfinding

The map is divided into connected **movement areas** [^2]. Naval units
occupy water areas and land units occupy land areas. This matters because:

1. A ship does not fire at a land enemy in a disconnected movement area.
   This prevents shots across an unrelated stretch of shoreline.
2. Ships use a separate water pathfinding grid.
3. A Ferry is a special case: while infantry is on board, it
   is counted inside the ship and occupies no land cell.

<a id="21-связность-через-транспорт"></a>
### 2.1. Connectivity through transport

An extended check accounts for **connections through transport**. A ship and
an infantry unit may occupy different areas yet remain reachable through
boarding and unloading.

---

<a id="3-порт-port"></a>
<a id="3-порт-sid-por"></a>
<a id="3-порт-por"></a>
<a id="3-порт"></a>
## 3. Shipyard

The Shipyard produces the fleet. Its main features are:

1. **Must be near water.** During placement, neighbouring cells are checked
   for water.
2. **Produces** ships of all nation types (light to heavy).
3. **Has a rally point**, normally placed on nearby water.
4. May have **built-in weapons**: some Shipyards fire on approaching enemy
   ships.

Price and properties are listed in the
[building guide](../../../reference/03_buildings/README.md).

---

<a id="4-транспортный-корабль"></a>
<a id="4-транспорт"></a>
## 4. Ferry

Transport takes place in four stages:

1. Infantry, cavalry, or artillery receive an order to board.
2. Units come within four cells, disappear from the map, and are counted
   inside the Ferry.
3. The ship receives an ordinary movement order toward the landing site.
4. On the unload command, units appear beside the ship on shore.

<a id="41-емкость-транспорта"></a>
<a id="41-вместимость-транспорта"></a>
### 4.1. Ferry capacity

A Ferry holds **120 population units**. Most infantry occupies one space,
cavalry two or three, and artillery five or more. That is roughly 100
Musketeers or 40 Reiters. The [navy guide](../../../reference/07_naval/README.md)
gives the full rule; the interface blocks boarding once the hold is full.

<a id="42-уязвимость"></a>
### 4.2. Vulnerability

If a Ferry sinks at sea with troops on board, **all units inside die**.
The vessel itself is nevertheless durable: it has 62,000 health, while
1,800 raw Cannon damage works out to about 35 direct hits even before
protection and misses are considered. The real danger is concentrated fire,
which can destroy both the ship and its entire embarked force at once.

Practical protection includes:

- a warship escort;
- a landing site outside enemy Tower range;
- an approach concealed by the enemy's fog of war.

---

<a id="5-линейный-корабль-battleship-и-dps-анализ-кораблей"></a>
<a id="5-линейный-корабль-battleship-и-урон-кораблей-в-секунду"></a>
<a id="5-линейный-корабль-и-урон-кораблей-в-секунду"></a>
## 5. Ship of the Line and damage per second

The Ship of the Line is the heaviest class. Its main features are:

1. **Multiple weapons:** broadsides and the bow gun may have different
   characteristics, so the ship's real firepower depends on all installed
   weapons rather than on a single salvo.
2. It requires **gold upkeep** but does not suffer from food shortages.
3. **Area-damage salvos:** cannonballs with a large blast radius
   can destroy an entire concentration of infantry on the shore.

<a id="51-real-dps--fast-по-основным-классам"></a>
<a id="51-реальный-урон-в-секунду-при-быстрой-скорости-игры"></a>
### 5.1. Actual damage per second at Fast game speed

The calculation divides damage by the pause between shots and multiplies
the result by 1.4. See
[Attack speed](../../../reports/combat/attack_rates.md) for the complete
tables.

| Class | Damage | Pause | Damage/s at Fast speed | Note |
|---|---:|---:|---:|---|
| Ship of the Line | 1800 | 0.62 | **≈ 4063** | highest damage per second in the game |
| Frigate | 1800 | 2.34 | ≈ 1077 | main combat ship |
| Galley, mortar shell | 1000 | 1.56 | ≈ 897 | **58-cell** range, bombards the shore from afar |
| Chaika (Ukraine) | 1000 | 2.34 | ≈ 599 | **fastest ranged ship** (speed 55) |
| Yacht | 1000 | 10.94 | ≈ 128 | weak but cheap scout |

<a id="52-уязвимости-линкора"></a>
### 5.2. Ship of the Line vulnerabilities

- **Shore artillery** can exploit its range and area damage.
- **Bombards on shore** can engage it from long range.

<a id="53-особые--dlc"></a>
<a id="53-особые-корабли-и-дополнительный-контент"></a>
### 5.3. Special ships and additional content

| Unit | Nation | What's special |
|---|---|---|
| Chaika | Ukraine | Fastest ranged ship (speed 55). Health 25,000 versus 31,000 for a regular Yacht. Vision 4. |
| Xebec | Algeria, Turkey | Eastern counterpart of the Frigate. Health 65,000 (+30%). Speed 28 (−2). |
| Yacht | Turkey | 35,000 health, speed 70, and two weapon slots. It is the fastest ship in a standard national roster. |

---

<a id="6-рыболовное-судно-fishboat"></a>
<a id="6-рыбацкая-лодка-fishboat"></a>
<a id="6-рыбацкая-лодка"></a>
## 6. Boat

The Boat is an economic unit. Its work cycle is:

1. Travels to a fishing area selected by the engine.
2. Remains at the fishing point and gathers
   **`32 / 12 ≈ 2.67` food per game second**, about 160 per game minute.
   This is slightly slower than an ideal Peasant at about 2.97.
3. Once its 1,000-unit hold is full, it goes to the Shipyard and unloads food.
4. Returns to the fishing point, much as a Peasant returns to a resource
   after delivering a load.

Each fishing point has a finite stock. Once every available point is
depleted, fishing stops.

<a id="61-уязвимость"></a>
### 6.1. Vulnerability

With only 300 health, Boats are extremely vulnerable to a Frigate's
1,800-damage salvo. They need safe waters or a Galley escort.

<a id="62-апгрейды"></a>
<a id="62-улучшения"></a>
### 6.2. Upgrades

Fishing upgrades (see
[Upgrades](../../../reference/05_upgrades/README.md))
increase Boat capacity rather than speeding up each gathering step.
**Design new tackle and fishing nets** (+100% Boat efficiency) doubles
cargo capacity to 2,000 food per trip. This reduces the number of journeys
to the Shipyard without changing the rate at which food accumulates at the
fishing point.

<a id="63-где-живёт-рыбная-ловля"></a>
<a id="63-как-устроен-промысел"></a>
### 6.3. How fishing works

The cycle resembles Peasant food gathering: select a source, accumulate a
load, deliver it to a receiving building, and return.

---

<a id="7-морские-формации"></a>
## 7. Sea formations

Naval units have four formation families (see
[Formations and Their Combat Bonuses §1.1](formations.md)):

| Formation | Description |
|---|---|
| Standard ship formation | An ordinary squadron layout. |
| Naval-only formation | Cannot be mixed with land units. |
| Spaced line | Wider intervals between ships. |
| Pack | A loose formation for light ships. |

Bonuses are usually zero or `+1`. Sea formations work for
positioning and pathfinding, not for
a significant bonus in battle.

---

<a id="8-атака-с-воды-по-берегу"></a>
## 8. Attacking the shore

A ship can fire at land units near the water's edge if the target is treated
as reachable within the connected area. In practice:

- Ships can shoot infantry directly on a pier or beach.
- Ships **cannot reach** infantry deep inland because it belongs to a land
  area.
- Artillery on shore can hit ships if its range reaches the water's edge.

---

<a id="85-стратегические-выводы"></a>
## 8.5. Strategic Conclusions

- **The Shipyard is a major mid-game investment.** For 1,600 wood,
  800 stone, 400 iron, and 1,562 game seconds of construction, it opens
  access to the fleet. Blacksmith upgrades for land units do not provide
  long-range ships with protection from cannonballs.
- **A Galley with a mortar shell** is the main naval siege weapon: its
  58-cell range lets it bombard the shore beyond the 28-cell range of an
  ordinary Tower.
- **The Ship of the Line dominates direct naval combat:** 90,000 health and
  roughly 4,063 damage per second. One can withstand pressure from three
  Frigates or 6–8 Galleys. It costs about as much as seven Frigates, so it
  must be protected rather than treated as disposable.
- **Ferries need redundancy.** Build three or four Ferries and keep them behind a
  Frigate escort.
- **Boat-based fishing is a niche economy for maritime nations.** On
  Tiny maps without a water front, a Boat is useless. On
  water-heavy maps it can be a main source of food for Turkey,
  Algeria, and Ukraine, compensating for their weaker
  17th-century economy.
- **Turkey's Yacht is the fastest standard ship.** Its speed of 70 lets it
  choose engagements, scout, and disengage from heavier vessels.

---

<a id="9-связь-со-скирмиш-картами"></a>
<a id="9-interaction-with-skirmish-maps"></a>
<a id="9-морской-бой-на-случайных-картах"></a>
## 9. Naval combat on random maps

Most Land Maps have **no water** (or very little). Therefore
sea battle is important only for:

- **Random maps with a large water area**.
- **Smooth and Hills** with a large water area.
- **Campaign** and Historical Battles (specially designed
  missions).

On a regular four-player Highlands land map there is usually no usable
water, so Shipyards and ships are unavailable.

---

<a id="технические-подробности"></a>
## Technical details

| Game concept | Internal representation |
|---|---|
| ship, Ship of the Line, transport, Boat | `bship`, `bbattleship`, `btransport`, `bfishboat` |
| naval-class checks | `_unit_IsShip`, `_unit_IsBattleShip`, `_unit_IsWaterUnit` |
| water region and extended connectivity | `_unit_GetRegion`, `_unit_SameRegion`, `_unit_SameRegionExt` |
| Shipyard | `por`; rally point `rallypoint` |
| boarding, contents, and unloading | `garrison`, `inside[]`, `ungarrison`; radius `captureradius = 4` |
| transport capacity | `garrison_capacity` |
| Ship of the Line and upkeep | `battleship`, `bmercenary`, `bnohungry` |
| Boat and full hold | `fishboat`, `fishingmax = 1000` |
| fishing speed and upgrades | `fishingspeed`, `fishingperc` |
| naval formation families | `SHIPS`, `SHIPSN`, `LINEMORB`, `PACK` |
| internal codes for special ships | `chaika`, `xebec`, `yachttur` |
| multiple ship weapons | several `weapon_*` fields |
| **Design new tackle and fishing nets** upgrade | `aca.5` |
| cannonball and mortar shell | `cannonball`, `mortarball` |

<a id="источники"></a>
## Sources

[^1]: `data.json` — fields `unit.bship`, `bbattleship`, `btransport`,
      `bfishboat`. See also `data/scripts/lib/unit.script:82-100` —
      functions `_unit_IsWaterUnit`, `_unit_IsShip`, `_unit_IsBattleShip`.

[^2]: `data/scripts/lib/unit.script:74` — `_unit_GetRegion(goHnd)`;
      `_unit_SameRegion` and `_unit_SameRegionExt` compare the regions of
      two units.
