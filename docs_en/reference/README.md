<a id="краткий-справочник-cossacks-3"></a>
# Cossacks 3 Quick Reference

[← Encyclopedia home](../README.md)

This section collects the essential game values and rules. Choose a topic,
nation, or comparison for a quick answer. Internal identifiers are secondary
and are shown only when they help distinguish similar objects.

<a id="разделы-справочника"></a>
## Reference sections

| Topic | What you can learn |
|---|---|
| [Economy](01_economy/README.md) | Gathering, mines, fields, fishing, famine, and army upkeep. |
| [Combat and movement](02_combat/README.md) | Damage, protection, range, speed, formations, and unit efficiency. |
| [Buildings](03_buildings/README.md) | Cost, health, construction time, capacity, and available production. |
| [Units](04_units/README.md) | Cost, health, training time, weapons, and protection for every unit class. |
| [Upgrades](05_upgrades/README.md) | Research location, cost, and effect of every upgrade. |
| [Market](06_market/README.md) | Exchange rates, how trades change them, and gradual recovery. |
| [Navy](07_naval/README.md) | Shipyards, warships, transports, and fishing boats. |

More: [21 nations](nations/README.md),
[side-by-side comparisons of units, buildings, weapons, and projectiles](compare/README.md),
[match settings](../reports/map/lobby_settings.md), and the
[technology tree](../reports/tech/tech_tree.md).

<a id="шпаргалка-по-формулам"></a>
## Formula cheat sheet

<a id="добыча-ресурсов"></a>
### Resource gathering

| Resource | Amount per trip | Work cycles before delivery | Ideal rate for one peasant, excluding travel |
|---|---:|---:|---:|
| Food | **45** | 22 | ≈ 2.97 per game second |
| Wood | **28** | 14 | ≈ 3.56 per game second |
| Stone | **40** | 20 | ≈ 3.56 per game second |
| Gold, iron, or coal | **20** | — | 1.664 per peasant per game second inside a mine |

Gathering upgrades increase the base amount. See
[Economy](01_economy/README.md) for details.

<a id="урон-в-бою"></a>
### Combat damage

```text
final damage = max(1, base weapon damage
                       - target armor
                       - target protection against this weapon type
                       + formation bonus
                       + possible critical-hit bonus)
```

Once an attack passes the hit and damage checks, it removes at least one point
of durability. See
[Combat and movement](02_combat/README.md) for details.

<a id="цены-и-время"></a>
### Prices and time

- Each additional copy of a building may cost more. The first six copies are
  listed in [Scaling building prices](../reports/economy/scaling_prices.md).
- Multiple builders reduce construction time almost proportionally, but each
  building has a maximum number of simultaneous workers. See
  [Maximum builders](../reports/economy/builder_slots.md).
- At Fast speed, divide game time by 1.4. For example, 140 game seconds take
  100 real seconds.

<a id="если-готового-числа-недостаточно"></a>
## When a single number is not enough

| Section | Contents |
|---|---|
| [How the game works](../recon/README.md) | Detailed explanations of hidden rules and game behavior. |
| [Tables and calculations](../reports/README.md) | Expanded comparisons of damage, time, prices, and national differences. |
| [Technical documentation](../../internals_en/README.md) | Data formats, internal fields, architecture, and extraction limitations. |

<a id="откуда-взяты-сведения"></a>
## Sources

Object names come from the game localization. Characteristics and formulas are
checked against game data and scripts; disputed or unverified conclusions are
marked as such in the relevant article.
