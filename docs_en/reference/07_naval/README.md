#07. Navy

[← Index](README.md)

> **Main points:**
>
> - **One Shipyard = the whole sea.** Construction of Shipyard (`<cluster>por`) unlocks the entire sea roster: 6 types of ships + Ferry + Fishing boat. There are no other buildings that produce ships in the game.
> - **Ships are noticeably more expensive than land units**, but also much stronger (HP 25,000–90,000 versus ~50–380 for infantry and cavalry). Ship of the Line is a floating bunker with the highest DPS in the game.
> - **Ferry** is the only way to transport infantry across water. Capacity - 120 “slots”.
> - **Fishing boat is the only sea source of food.** An alternative to fields and hunting at an early stage among sea nations.

**In-depth analysis of mechanics:**

- [`../../recon/world/combat/naval_combat.md`](../../recon/world/combat/naval_combat.md) - sea battle, regions, transport, battleship, real-DPS @ fast by class, special units (`chaika` / `xebec` / `yachttur`), strategic conclusions.

<a id="содержание"></a>
## Contents

- [Shipyard](#порт-clusterpor)
- [Ship Catalog](#каталог-кораблей)
- [Combat stats](#боевые-статы)
- [Ferry](#транспорт-ferry)
- [Fishing Boat](#рыбачья-лодка-fishboat)

<a id="порт-por"></a>
## Shipyard (`<cluster>por`)

The Shipyard parameters are defined in one branch of the `commonsid+'por'` parsing of [^n1].

| Parameter | Meaning |
|---|---:|
| HP | **50,000** |
| `buildtime` | 5000 frames = **1562.5 g-sec** (≈ 1116 real-sec @ fast = 18.6 min for one builder) |
| `costpercent` | **150** (each next +50%) |
| Price | 1600 W / 800 S / 400 I |
| Prereq | `<cluster>mar` (market) |
| `bcapture` | `False` - cannot be captured, only destroyed |
| `vision` | 3 (32 t FOW) |

**Produces:** `battleship`, `chaika` / `yacht` / `yachttur`, `ferry`, `fishboat`, `frigate` / `xebec`, `galley`. All nations have the same Shipyard - there are no nation-specific Shipyards with different rosters (only `chaika` ↔ `yacht` ↔ `yachttur` replace each other by nation).

**Cost of the second Shipyard:** `1600 × 1.5 = 2400 W` + `800 × 1.5 = 1200 S` + `400 × 1.5 = 600 I` (rule `costpercent` see [01_economy/README.md](../01_economy/README.md)). Third: 3600 / 1800 / 900.

<a id="каталог-кораблей"></a>
## Ship catalog

7 naval units + 2 ukr/tur variants. Names are from the game locale; parameters extracted from [`data.json`](../../../data.json).

| Ship | Class | HP | Speed ​​| Vision (t) | Search(t) | Price | Buildtime g-sec |
| --- | --- | ---: | ---: | ---: | ---: | --- | ---: |
| **Boat** `fishboat` | Fishing boat | 300 | 16 | 24 | — | 600 W | 40.0 |
| **Ferry** `ferry` | Ferry | 62000 | 28 | 24 | — | 300 W / 50 G / 100 I | 56.0 |
| **Yacht** `yacht` | Light Gunner | 31000 | 40 | 32 | 19.69 | 900 W / 450 G / 150 I / 200 C | 48.0 |
| `chaika` | Light shooter (ukr) | 25000 | 55 | 36 | 19.69 | 1050 W / 600 G / 200 I / 400 C | 40.0 |
| **Yacht** `yachttur` | Light marksman (tur) | 35000 | 70 | 32 | 19.69 | 900 W / 450 G / 150 I / 200 C | 48.0 |
| **Galley** `galley` | Artillery | 35000 | 40 | 28 | 20.63 | 9500 W / 900 G / 800 I | 50.0 |
| **Frigate** `frigate` | Heavy Gunner | 50000 | 30 | 52 | 33.75 | 5000 W / 1100 G / 600 I / 800 C | 230.0 |
| **Xebec** `xebec` | Heavy Gunner (alg/tur) | 65000 | 28 | 52 | 33.75 | 7000 W / 1600 G / 320 I / 960 C | 230.0 |
| **Ship of the Line** `battleship` | Ship of the Line | 90000 | 16 | 52 | 31.5 | 9000 W / 3200 G / 700 I / 6500 C | 390.0 |

**Speed scale** for understanding the numbers: peasant = 32, mounted warrior = 80–96, light infantry = 32. Ships — from 16 to 55.

<a id="боевые-статы"></a>
## Combat stats

The cost of one shot (`weapon[i].cost`) is written off at the moment of the salvo: with each shot, `iron + coal` leaves the treasury.
| Ship | No. | dmg | pause (g-sec) | range(t) | kind | cost/shot |
| --- | :---: | ---: | ---: | ---: | --- | --- |
| **Yacht** `yacht` | 0 | 1000 | 10.94 | 20.63 | cannonball | 4 I + 9 C |
| `chaika` | 0 | 1000 | 2.34 | 20.63 | cannonball | 4 I + 9 C |
| **Yacht** `yachttur` | 0 | 30 | 12.5 | 18.75 | cannonball | 5 I + 15 C |
|   | 1 | 0 | 21.88 | 30.94 | — | 5 I + 15 C |
| **Galley** `galley` | 0 | 100 | 4.69 | 22.5 | cannonball | 4 I + 9 C |
|   | 1 | 1000 | 1.56 | 58.13 | mortarball | 4 I + 9 C |
| **Frigate** `frigate` | 0 | 1800 | 2.34 | 30.94 | cannonball | 25 I + 35 C |
| **Xebec** `xebec` | 0 | 1800 | 1.56 | 31.88 | cannonball | 25 I + 35 C |
| **Ship of the Line** `battleship` | 0 | 1800 | 0.62 | 36.56 | cannonball | 5 I + 15 C |

**Real-DPS @ fast and analysis of combat effectiveness by class** - in [`../../recon/world/combat/naval_combat.md` §5.1](../../recon/world/combat/naval_combat.md). Full attack speed tables are in [`reports/combat/attack_rates.md`](../../reports/combat/attack_rates.md).

<a id="транспорт-ferry"></a>
## Ferry (`ferry`)
```
HP        = 62000
speed     = 28
transport = 120    (infantry/cavalry capacity slots)
buildtime = 56.0 game sec (40.0 real sec @ fast)
cost      = 300 W / 50 G / 100 I
weapon    = none (cannot attack)
vision    = 24 t
```
**What does `transport = 120` mean:** one Ferry can hold up to **120 population units** (farm slots). Most infantry occupy 1 slot, cavalry - 2-3, artillery - 5+. Therefore, Ferry transports approximately 100 musketeers or 40 reiters.

Details (behavior during loading, vulnerability, escort) are in [`../../recon/world/combat/naval_combat.md` §4](../../recon/world/combat/naval_combat.md).

<a id="рыбачья-лодка-fishboat"></a>
## Fishing boat (`fishboat`)
```
HP            = 300
speed         = 16
fishingmax    = 1000    (food storage capacity)
fishingspeed  = 12      (frames per food unit)
buildtime     = 40.0 game sec
cost          = 600 W
```
Fishing cycle, `fishingperc` upgrades, vulnerability and strategy - in [`../../recon/world/combat/naval_combat.md` §6](../../recon/world/combat/naval_combat.md).

<a id="источники"></a>
## Sources

[^n1]: Parameters Shipyard (`<cluster>por`) - `lib/unit.script:2148-2206` (common block plus `commonpor` / `commonrus` / `commontur` / `ukr`-overrides).
