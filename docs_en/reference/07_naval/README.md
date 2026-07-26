<a id="флот"></a>
# Navy

[← Quick reference](../README.md)

> **The essentials:**
>
> - **One Shipyard unlocks the whole navy.** It produces six classes of
>   warship, the Ferry, and the Fishing Boat.
> - **Ships cost much more than land units**, but are also far tougher:
>   25,000–90,000 health versus roughly 50–380 for infantry and cavalry.
> - The **Ferry** is the only way to carry land units across water. Its
>   capacity is 120 population slots.
> - The **Fishing Boat** is the only naval source of food and can replace
>   fields and hunting on water-heavy maps.

See [How naval combat works](../../recon/world/combat/naval_combat.md) for
water regions, transports, Battleships, real damage per second at Fast speed,
and national ship variants.

<a id="содержание"></a>
## Contents

- [Shipyard](#shipyard)
- [Ships](#ships)
- [Combat statistics](#combat-statistics)
- [Ferry](#ferry)
- [Fishing Boat](#fishing-boat)

<a id="порт"></a>
## Shipyard

Shipyard parameters are the same for every architectural set.

| Parameter | Value |
|---|---:|
| Health | **50,000** |
| Construction time | **1,562.5 game seconds**—about 18.6 real minutes at Fast speed with one builder |
| Price growth | **150%**—each additional Shipyard costs 50% more |
| Cost | 1,600 wood / 800 stone / 400 iron |
| Requirement | Market |
| Capture | Cannot be captured; can only be destroyed |
| Vision | 32 tiles |

**Produces:** Ship of the Line; Chaika, Yacht, or Ottoman Yacht depending on
the nation; Ferry; Fishing Boat; Frigate or Xebec; and Galley.

The second Shipyard costs 2,400 wood, 1,200 stone, and 600 iron. The third
costs 3,600 wood, 1,800 stone, and 900 iron. See [Economy](../01_economy/README.md)
for the general scaling rule.

<a id="корабли"></a>
## Ships

The game has seven main naval units plus Ukrainian, Ottoman, and Algerian
variants. Names use the English game localization where available.

| Ship | Role | Health | Speed | Vision, tiles | Target acquisition, tiles | Cost | Build time, game seconds |
|---|---|---:|---:|---:|---:|---|---:|
| **Fishing Boat** `fishboat` | Fishing Boat | 300 | 16 | 24 | — | 600 wood | 40.0 |
| **Ferry** `ferry` | Transport | 62,000 | 28 | 24 | — | 300 wood / 50 gold / 100 iron | 56.0 |
| **Yacht** `yacht` | Light warship | 31,000 | 40 | 32 | 19.69 | 900 wood / 450 gold / 150 iron / 200 coal | 48.0 |
| **Chaika** `chaika` | Ukrainian light warship | 25,000 | 55 | 36 | 19.69 | 1,050 wood / 600 gold / 200 iron / 400 coal | 40.0 |
| **Ottoman Yacht** `yachttur` | Ottoman light warship | 35,000 | 70 | 32 | 19.69 | 900 wood / 450 gold / 150 iron / 200 coal | 48.0 |
| **Galley** `galley` | Artillery ship | 35,000 | 40 | 28 | 20.63 | 9,500 wood / 900 gold / 800 iron | 50.0 |
| **Frigate** `frigate` | Heavy warship | 50,000 | 30 | 52 | 33.75 | 5,000 wood / 1,100 gold / 600 iron / 800 coal | 230.0 |
| **Xebec** `xebec` | Algerian and Ottoman heavy warship | 65,000 | 28 | 52 | 33.75 | 7,000 wood / 1,600 gold / 320 iron / 960 coal | 230.0 |
| **Ship of the Line** `battleship` | Ship of the Line | 90,000 | 16 | 52 | 31.5 | 9,000 wood / 3,200 gold / 700 iron / 6,500 coal | 390.0 |

For scale, a Peasant or Light Infantry unit has speed 32, a mounted warrior
usually has 80–96, and ships range from 16 to 55.

<a id="боевые-характеристики"></a>
## Combat statistics

Iron and coal are deducted when a ship fires.

| Ship | Weapon | Damage | Reload, game seconds | Range, tiles | Damage type | Shot cost |
|---|:---:|---:|---:|---:|---|---|
| **Yacht** `yacht` | 0 | 1,000 | 10.94 | 20.63 | cannonball | 4 iron + 9 coal |
| **Chaika** `chaika` | 0 | 1,000 | 2.34 | 20.63 | cannonball | 4 iron + 9 coal |
| **Ottoman Yacht** `yachttur` | 0 | 30 | 12.5 | 18.75 | cannonball | 5 iron + 15 coal |
|  | 1 | 0 | 21.88 | 30.94 | — | 5 iron + 15 coal |
| **Galley** `galley` | 0 | 100 | 4.69 | 22.5 | cannonball | 4 iron + 9 coal |
|  | 1 | 1,000 | 1.56 | 58.13 | mortar blast | 4 iron + 9 coal |
| **Frigate** `frigate` | 0 | 1,800 | 2.34 | 30.94 | cannonball | 25 iron + 35 coal |
| **Xebec** `xebec` | 0 | 1,800 | 1.56 | 31.88 | cannonball | 25 iron + 35 coal |
| **Ship of the Line** `battleship` | 0 | 1,800 | 0.62 | 36.56 | cannonball | 5 iron + 15 coal |

Real damage per second at Fast speed is discussed in
[How naval combat works](../../recon/world/combat/naval_combat.md). See
[Attack rates](../../reports/combat/attack_rates.md) for the full tables.

<a id="транспорт"></a>
## Ferry

| Parameter | Value |
|---|---:|
| Health | 62,000 |
| Speed | 28 |
| Capacity | 120 |
| Build time | 56.0 game seconds; 40.0 real seconds at Fast speed |
| Cost | 300 wood / 50 gold / 100 iron |
| Weapon | none |
| Vision | 24 tiles |

A capacity of 120 means one Ferry holds up to **120 population slots**.
Most infantry use one slot, cavalry two or three, and artillery five or more.
The Ferry therefore carries roughly 100 Musketeers or 40 Reiters.

Loading, vulnerability, and escort behavior are covered in
[How naval combat works](../../recon/world/combat/naval_combat.md).

<a id="рыбачья-лодка"></a>
## Fishing Boat

| Parameter | Value |
|---|---:|
| Health | 300 |
| Speed | 16 |
| Food per trip | 1,000 |
| Gathering interval | 12 frames per food unit |
| Build time | 40.0 game seconds |
| Cost | 600 wood |

The fishing cycle, upgrades, vulnerability, and strategy are covered in
[How naval combat works](../../recon/world/combat/naval_combat.md).

<a id="источники"></a>
## Technical source

Shipyard parameters: `lib/unit.script:2148-2206`, including common,
Russian, Ottoman, Portuguese, and Ukrainian overrides.
