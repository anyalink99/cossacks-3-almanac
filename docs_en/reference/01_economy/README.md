<a id="экономика"></a>
# Economy

[← Quick reference](../README.md)

<a id="резюме"></a>
## Summary

A peasant chops wood, mines stone, or harvests food in small portions, then
carries the accumulated load to a storehouse. Gathering upgrades are additive:
bonuses of +40% and +140%, for example, turn the base 100% efficiency into
280%.

Mines work differently. A peasant inside a mine continuously produces about
**1.664 gold, iron, or coal per game second**. Mine upgrades do not make an
individual worker faster; they provide room for more workers.

<a id="сколько-крестьянин-приносит-за-рейс"></a>
## Amount gathered per trip

| Resource | Base amount | Work cycles before delivery |
|---|---:|---:|
| Food | **45** | 22 |
| Wood | **28** | 14 |
| Stone | **40** | 20 |
| Gold, iron, or coal | **20** | gathered inside a mine |

<a id="формула-добычи"></a>
## Gathering formula

```text
delivered amount = base amount × efficiency / 100
```

Example: +40% and +140% upgrades produce 280% efficiency. A peasant delivers
`45 × 280 / 100 = 126` food per trip instead of the base 45.

All available bonuses are listed in [Upgrades](../05_upgrades/README.md).

<a id="шахты"></a>
## Mines

Gold, iron, and coal mines work in the same way. A basic mine holds
**5 peasants**, costs 100 wood and 100 stone, and takes about 9.38 game seconds
to build.

```text
one peasant = 1.664 resources per game second
             ≈ 100 resources per game minute
```

**Fully upgrading one mine** adds six capacity upgrades:

| Upgrade | Additional slots | Food | Gold | Total slots |
|---|---:|---:|---:|---:|
| **Extend the mine and build a branching rail network (+5)** `eurgol.1` | +5 | 1,000 | 1,250 | 10 |
| **Extend the mine and build a branching rail network (+8)** `eurgol.2` | +8 | 5,250 | 4,950 | 18 |
| **Extend the mine and build a branching rail network (+10)** `eurgol.3` | +10 | 12,500 | 9,250 | 28 |
| **Extend the mine and build a branching rail network (+12)** `eurgol.4` | +12 | 15,800 | 18,500 | 40 |
| **Extend the mine and build a branching rail network (+15)** `eurgol.5` | +15 | 19,800 | 21,050 | 55 |
| **Extend the mine and build a branching rail network (+40)** `eurgol.6` | +40 | 50,200 | 25,950 | 95 |

The base 5 slots plus all upgrades allow **95 peasants in one mine**, producing
up to 158.1 resources per game second, or 9,485 per game minute.

All upgrades for one mine cost 104,550 food and 80,950 gold.

<a id="поля-и-запас-еды"></a>
## Fields and food capacity

A field has **25,000 health**. Durability upgrades increase the number of
harvesting cycles it survives and therefore the total amount of food it can
produce.

| Durability bonus | Damage to the field per cycle | Maximum cycles | Food without gathering upgrades |
|---:|---:|---:|---:|
| 0 | 100 | 250 | 511 |
| 100 | 50 | 500 | 1,022 |
| 200 | 33 | 757 | 1,548 |
| 300 | 25 | 1,000 | 2,045 |
| 500 | 16 | 1,562 | 3,195 |

The two standard durability upgrades provide a combined bonus of 300. A fully
worked field then produces about **2,045 food**, rather than the base 495.

<a id="рыбалка"></a>
## Fishing

A Fishing Boat has 300 health, costs 600 wood, and carries **1,000 food**.
One upgrade doubles its capacity to **2,000 food per trip**; another reduces
the boat’s construction cost by 85%.

See [Ship comparisons](../compare/units/ships.md) for the full fleet.

<a id="содержание-армии-голод-и-бунт"></a>
<a id="famine-голод-и-rebellion-восстание"></a>
## Army upkeep, famine, and rebellion

A normal army continuously consumes food. When food runs out, famine begins
and may be followed by rebellion. Buildings and mercenaries do not consume
food.

<a id="расход-еды-одним-юнитом"></a>
### Food consumption per unit

The values below are per game second:

| Unit | Food per second |
|---|---:|
| Peasant of most European nations | 0.0992 |
| Ottoman or Algerian Peasant | 0.0928 |
| Russian Peasant | 0.0896 |
| Ordinary infantry without a special rate | 0.0480 |

For example, 18 Austrian Peasants consume about **214 food** over two game
minutes.

<a id="дипломатический-центр"></a>
### Diplomatic Center

The Diplomatic Center is a mid-game building that requires an Academy and a
Town Hall. Each player may have only one.

| Variant | Nations | Health | Wood | Stone | Gold |
|---|---|---:|---:|---:|---:|
| **Diplomatic Center** `ausdip` | Austria, France, England, Spain, Poland … (+12) | 4,500 | 4,900 | 1,700 | 0 |
| **Diplomatic Center** `rusdip` | Russia | 6,500 | 7,900 | 3,700 | 0 |
| **Diplomatic Center** `ukrdip` | Ukraine | 5,000 | 3,900 | 2,700 | 0 |
| **Diplomatic Center** `turdip` | Turkey, Algeria | 5,500 | 4,600 | 2,020 | 0 |

All variants take **312.5 game seconds** to build and cannot be captured.

<a id="наёмники"></a>
### Mercenaries

The same eight mercenaries are available to all 21 nations. They consume no
food, but require continuous gold upkeep.

| Mercenary | Health | Training time, game seconds | Gold | Gold upkeep | Weapon |
|---|---:|---:|---:|---:|---|
| **Light Infantry (mercenary)** `lightinfantrydip` | 50 | 1.25 | **4** | 4 | sword 16 |
| **Roundshier (mercenary)** `roundshierdip` | 75 | 1.5 | **12** | 20 | sword 6 |
| **Archer (mercenary)** `archerdip` | 20 | 1.25 | **15** | 16 | arrows: 25, range 13.13 / fire arrow: 100, range 14.06 |
| **Ottoman Archer (mercenary)** `archerturdip` | 20 | 1.25 | **15** | 16 | arrows: 25, range 13.13 / fire arrow: 100, range 14.06 |
| **Grenadier (mercenary)** `grenadierdip` | 30 | 1.5 | **25** | 60 | pike 30 / bullet: 16, range 15.0 / mortar blast: 200, range 7.5 |
| **Sich Cossack (mercenary)** `cossacksichdip` | 150 | 2.5 | **60** | 150 | sword 8 |
| **Dragoon, 18th century (mercenary)** `dragoon18dip` | 100 | 2.0 | **120** | 120 | bullet: 18, range 15.0 |
| **Light Cavalry (mercenary)** `lightcavalrydip` | 100 | 2.0 | **120** | 120 | bullet: 18, range 15.0 |

Fifty mercenary Dragoons, for example, consume about **9.6 gold per game
second**, or **576 gold per game minute**.

Each additional mercenary of the same type costs more, up to twice the base
price. European and Ottoman Archers share one price counter; the mercenary
Dragoon and Light Cavalry share another. The “Expensive mercenaries” match
rule triples their price.

<a id="другие-постоянные-расходы-золота"></a>
### Other continuous gold expenses

- A **Tower** continuously consumes 0.8 gold per game second, or 48 per game
  minute, even when it is not firing.
- **Mercenaries** consume gold according to the table above.
- **Ranged units** pay for individual shots but consume nothing while idle.

Ordinary Pikemen and Musketeers do **not** consume gold while idle.

The probability of rebellion and difficulty-specific behavior are covered in
[Famine and mercenary rebellion](../../recon/world/economy/hunger_and_rebellion.md).
Diplomatic Center rules are covered in
[Mercenaries and the Diplomatic Center](../../recon/systems/mercenaries_diplomacy.md).

<a id="если-нужны-все-подробности"></a>
## Further reading

- [The full peasant work cycle](../../recon/world/economy/peasant_extraction.md):
  work cycles, carrying, travel to a storehouse, and gathering upgrades.
- [How the map generator places resources](../../recon/world/map/map_generation_pipeline.md):
  forests, stones, and mines around players.
- [Estimated resources on a typical map](../../reports/map/map_resources.md).
