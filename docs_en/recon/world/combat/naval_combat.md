<a id="recon-морской-бой"></a>
<a id="как-устроен-морской-бой"></a>
# How Naval Combat Works

[← How the game works](../../README.md)

In-depth analysis: how do naval units differ from land units, how
boarding works, how transport ships behave, what it means
port All links to the code are in [Sources](#sources).

<a id="кратко"></a>
## TL;DR

- Naval units have the flag `bship = True`, and `_unit_IsShip` /
  `_unit_IsBattleShip` / `_unit_IsWaterUnit` distinguish between vessels [^1].
- Only **port** (`port`-building) produces ships. Every nation
  has its own set of ships: light boat, frigate, line
  ship, merchant ship, fisherman.
- **Transport ships** (`btransport = True`) carry units:
  infantry/cavalry/artillery board through
  `garrison`, the ship takes them to shore.
- **Battleships** (`battleship`) are often marked
  `bmercenary = True` - they are “mercenary” relatively
  ordinary units: they require gold upkeep but do not suffer from
  food shortages.
- **Naval formations** use separate families (`SHIPS`, `SHIPSN`,
  `LINEMORB`); see [Formations and Their Combat Bonuses §7](formations.md).
- The target `_unit_SearchEnemy*` for a naval unit takes into account `same_region`
  - the ship does not shoot at ground units (they are in a different
  pathfinding-region).

---

<a id="1-что-делает-юнит-морским"></a>
## 1. What makes a unit “sea”

Several related flags in `data.json` [^1]:

| Field | What |
|---|---|
| `bship` | Ship (any type). |
| `bbattleship` | Ship of the Line (heavy, powerful weapon). |
| `btransport` | Transport ship for infantry, cavalry, and artillery. |
| `bfishboat` | Fishing vessel. |

Also `_unit_IsWaterUnit(handle)` is a function that returns
true for all naval units. Used when selecting a target and in
pathfinding so that the ship does not try to go on land.

---

<a id="2-регионы-и-pathfinding"></a>
<a id="2-водные-области-и-поиск-пути"></a>
## 2. Regions and pathfinding

The map in C3 is divided into **regions** via
`_unit_GetRegion(goHnd)` [^2]. Naval units are in
“water” regions, land ones - in “earth” regions. This is important because:

1. The ship **does not shoot** at a land enemy (if they are in different
   regions). Check `_unit_SameRegion(hnd1, hnd2)`. This
   standard protection against buggy shots across the shore.
2. Pathfinding for the ship - on the water-grid, separately from
   land.
3. A transport ship is a special case: while infantry is on board, it
   lives in `inside[]` (as a garrison, see
   [tower and garrison mechanics](towers.md)), and her
   the region is changing.

### 2.1. `_unit_SameRegionExt`

Advanced region check option (`_unit_SameRegionExt`)
takes into account **public accessibility** via transport. That is, “the ship and
the infantry are not in the same region, but are connected through a transport route.”

---

<a id="3-порт-port"></a>
<a id="3-порт-sid-por"></a>
<a id="3-порт-por"></a>
## 3. Shipyard (SID `por`)

Shipyard - ship factory building. Features:

1. **Must be near water.** When building, the script checks that
   neighboring cells are water tiles.
2. **Produces** ships of all nation types (light to heavy).
3. Has `rallypoint` - collection point, usually placed on the water
   near the port.
4. May have **built-in weapons** - some ports shoot
   on approaching enemy ships.

Prices and port properties are listed in the
[building guide](../../../reference/03_buildings/README.md) (the `port` row).

---

<a id="4-транспортный-корабль"></a>
## 4. Transport ship

Transport ships have `btransport = True`. Behaviour:

1. Infantry/cavalry/artillery receive orders
   `garrison(transport_handle)`.
2. Units go to the transport, enter through the entry (`captureradius = 4`
   tiles), disappear from the map, end up in `inside[]`.
3. The transport receives a movement order, `move(x, z)`.
4. When the transport has arrived, the player clicks “unload”
   (`ungarrison`). Units climb out next to the ship on the shore.

<a id="41-емкость-транспорта"></a>
### 4.1. Transport capacity

`garrison_capacity` for transports is usually 10–20; exact values are in the
[navy guide](../../../reference/07_naval/README.md). If you try to load more,
the interface blocks the command.

<a id="42-уязвимость"></a>
### 4.2. Vulnerability

The transport is a soft target. If it sinks at sea with infantry on
board, **all units inside die**. This is critical: one Cannon on
the coast can sink 15-20 pikemen in a couple of salvos.

Transport protection:
- Convoy of warships.
- Landing in a safe zone (outside the area of enemy towers).
- Hidden landing in FOW (fog of war on the enemy side).

---

<a id="5-линейный-корабль-battleship-и-dps-анализ-кораблей"></a>
<a id="5-линейный-корабль-battleship-и-урон-кораблей-в-секунду"></a>
## 5. Ship of the Line (`battleship`) and damage per second

`battleship` is the heaviest class. Features:

1. **Multiple weapons**: broadsides, bow gun.
   In the code this is represented through several `weapon_*` fields in
   `data.json`. Our parser extracts only the first one (see.
   [known limitations](../../../../internals_en/project/known_issues.md) — open issue
   about multi-weapon buildings).
2. **`bmercenary = True`** - the battleship is marked as
   "mercenary" among Diplomatic Centre units. This means it requires
   **gold upkeep** but does not suffer from food shortages
   (`bnohungry = True` through `bmercenary`).
3. **AoE salvos**: `cannonball` projectiles with a large burst radius
   can destroy an entire concentration of infantry on the shore.

<a id="51-real-dps--fast-по-основным-классам"></a>
<a id="51-реальный-урон-в-секунду-при-быстрой-скорости-игры"></a>
### 5.1. Actual damage per second at Fast game speed

Formula: `damage / pause × 1.4`. Full attack speed tables -
to [Attack speed](../../../reports/combat/attack_rates.md).

| Class | Damage | Pause | Damage/s at Fast speed | Note |
|---|---:|---:|---:|---|
| Ship of the Line (`battleship`) | 1800 | 0.62 | **≈ 4063** | highest damage per second in the game |
| Frigate (`frigate`) | 1800 | 2.34 | ≈ 1077 | main combat ship |
| Galley (mortarball) | 1000 | 1.56 | ≈ 897 | range **58 t**, hits the shore from a long distance |
| Chaika (`chaika`, Ukraine) | 1000 | 2.34 | ≈ 599 | **fastest ranged ship** (speed 55) |
| Ottoman Yacht (`yachttur`) | 1000 | 2.34 | ≈ 599 | damage per second 4.7× higher than a regular Yacht at the same price |
| Yacht (`yacht`) | 1000 | 10.94 | ≈ 128 | weak but cheap scout |

<a id="52-уязвимости-линкора"></a>
### 5.2. Battleship vulnerabilities

- **Artillery from the shore** - large radius, AoE.
- **Fireship** (if the nation has one) is a self-detonating ship.
- **Bombards** - naval artillery type (if available in the nation).

<a id="53-особые--dlc"></a>
<a id="53-особые-корабли-и-дополнительный-контент"></a>
### 5.3. Special ships and additional content

| Unit | Nation | What's special |
|---|---|---|
| Chaika (`chaika`) | Ukraine | Fastest ranged ship (speed 55). Health 25,000 versus 31,000 for a regular Yacht. Vision 4. |
| Xebec (`xebec`) | Algeria, Turkey | Eastern counterpart of the Frigate. Health 65,000 (+30%). Speed 28 (−2). |
| Ottoman Yacht (`yachttur`) | Turkey | Health 31,000, like a regular Yacht, but `pause = 2.34` instead of `10.94`: **4.7× the damage per second**. |

---

<a id="6-рыболовное-судно-fishboat"></a>
<a id="6-рыбацкая-лодка-fishboat"></a>
## 6. Fishing boat (`fishboat`)

`fishboat` - economic unit. Cycle:

1. Goes to the water in the area with fish (controlled by the native engine).
2. Stands and accumulates food at the speed of **`32 / 12 ≈ 2.67 food / game sec`**
   ≈ 115 per game minute - somewhat slower than the ideal peasant
   (≈ 2.97/g-sec).
3. Once `fishingmax = 1000` is filled, it goes to Shipyard and unloads food.
4. Returns to the same point (like a peasant with a resource in a warehouse).

Limited: fish points **not infinite** (unlike
tree stumps). If all points are caught, fishing stops until
respawn

<a id="61-уязвимость"></a>
### 6.1. Vulnerability

Health 300: one Frigate salvo (1800 Cannonball Damage) can kill
several Boats in one wave. Protection requires either no enemies at
sea or an escort of Galleys.

<a id="62-апгрейды"></a>
### 6.2. Upgrades

Upgrades `fishingperc` (`mil` / `bla` / `aca` - see.
[upgrades](../../../reference/05_upgrades/README.md))
reduce `fishingspeed` (fewer frames per unit), which directly
increases production. Also `aca.5` (+100% boat efficiency)
doubles cargo capacity to 2000 food per trip.

<a id="63-где-живёт-рыбная-ловля"></a>
### 6.3. Where does fishing live?

Script logic - in `lib/unit.script`, branch
`_unit_DoExtractFish` or similar (similar to `_unit_DoExtract`).
The load is identical to the food production by peasants, but through `bfishboat`
instead of `bpeasant`.

---

<a id="7-морские-формации"></a>
## 7. Sea formations

Families `SHIPS`, `SHIPSN`, `LINEMORB`, `PACK` (see
[Formations and Their Combat Bonuses §1.1](formations.md)) - for naval units:

| Family | Description |
|---|---|
| `SHIPS` | Standard ship formations. |
| `SHIPSN` | Purely naval, without land units. |
| `LINEMORB` | Line with extended interval (for squadron). |
| `PACK` | Flock (for light ships). |

Bonuses are usually zero or `+1`. Sea formations work for
positioning and pathfinding, not for
a significant bonus in battle.

---

<a id="8-атака-с-воды-по-берегу"></a>
## 8. Attack from the water along the shore

The ship can fire at ground units in the zone `radiusmax` from
edges of the water, but **only if they are in the same `region`** through
`_unit_SameRegionExt`. In practice this means:

- Ships can shoot infantry directly on the pier/beach.
- The ships **will not reach** the infantry deep on the mainland (it is in
  land region).
- Artillery from the shore can hit the sea if it
  `radiusmax` reaches the water's edge.

---

<a id="85-стратегические-выводы"></a>
## 8.5. Strategic Conclusions

- **The Shipyard is a major mid-game turning point.** For 1600 wood,
  800 stone, 400 iron, and 1562 game seconds of construction, the
  player gains access to
  the most durable army in the game, resistant to land upgrades
  18th century: for cannonball defense on long-range ships
  There are no upgrades from the forge.
- **A Galley with mortarball** is the main “siege weapon of the sea”:
  its 58-tile range lets it bombard the shore without a response from
  ordinary Towers with a 28-tile range.
- **The Ship of the Line is an “aircraft carrier”:** 90,000 health
  and roughly 4063 damage per second.
  One ship can hold three frigates or 6–8 galleys. Costs like
  7 frigates, but the combat value is non-linear.
- **Transport ships are expendable.** Build 3–4 at a time and keep
  them behind a Frigate escort.
- **The fishing boat economy is a niche for maritime nations.** On
  Tiny maps and without a water front a fishing boat is useless. On
  water-heavy maps it can be a main source of food for Turkey,
  Algeria, and Ukraine, compensating for their weaker
  17th-century economy.
- **The Ottoman Yacht (`yachttur`) is unexpectedly strong.** Its
  damage per second is 4.7
  times higher than a regular yacht at the same price makes it one of
  the best units in terms of price/damage ratio in the game. If you play
  Turkey, mass-producing Ottoman Yachts in the Shipyard can decide a
  naval map on its own.

---

<a id="9-связь-со-скирмиш-картами"></a>
## 9. Connection with skirmish cards

Most Land Maps have **no water** (or very little). Therefore
sea battle is important only for:

- **Naval Skirmish maps** (special water maps).
- **Smooth and Hills** with a large water area.
- **Campaign** and Historical Battles (specially designed
  missions).

On a regular 4-player Land map Highlands there is usually no water type,
ports and ships are inaccessible.

---

<a id="10-открытые-эмпирические-вопросы"></a>
## 10. Open empirical questions

1. **Exact transport capacity** for each nation. B `data.json`
   `garrison_capacity` for transport ships - find the exact numbers.
2. **Radius of the “shore”** for firing a ship on land. Accurate
   the distance from the water at which the ship still falls into the infantry,
   depends on layer `region`. Measure it.
3. **Replenishment of fish points**. Will fish spots respawn in
   Is it game time, or after everything is exhausted, is food from the sea closed?
Find `_res_RegenFish` or a similar procedure in `lib/res.script`.

---

<a id="источники"></a>
## Sources

[^1]: `data.json` - fields `unit.bship`, `bbattleship`, `btransport`,
      `bfishboat`. Also `data/scripts/lib/unit.script:82-100` -
      functions `_unit_IsWaterUnit`, `_unit_IsShip`, `_unit_IsBattleShip`.

[^2]: `data/scripts/lib/unit.script:74` - `_unit_GetRegion(goHnd)`.
      Also `_unit_SameRegion`, `_unit_SameRegionExt` -
      checking one region for two units.
