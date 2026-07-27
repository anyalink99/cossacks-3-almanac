<a id="энциклопедия-cossacks-3"></a>
# Cossacks 3 Encyclopedia

**English** · [Русский](../docs/README.md)

This encyclopedia answers practical questions about the game: how much a
building costs, how nations differ, how damage is calculated, where an
upgrade is researched, and what each match setting changes.

<a id="выберите-тему"></a>
## Choose a topic

| Section | What you can learn |
|---|---|
| [Economy](reference/01_economy/README.md) | How food, wood, stone, and ores are gathered; how mines and fields work; and how famine and army upkeep affect a player. |
| [Combat and movement](reference/02_combat/README.md) | How damage is calculated and how armor, formations, range, speed, and weapon type affect a fight. |
| [Buildings](reference/03_buildings/README.md) | Cost, health, construction time, capacity, production, and national building variants. |
| [Units](reference/04_units/README.md) | Infantry, cavalry, artillery, and ships: health, cost, training time, damage, range, and protection. |
| [Upgrades](reference/05_upgrades/README.md) | Where each upgrade is researched, how much it costs, and what it changes. |
| [Market](reference/06_market/README.md) | How exchange rates move, why one large trade can be better, and how the market recovers. |
| [Navy](reference/07_naval/README.md) | Shipyards, warships, transports, and fishing boats. |
| [Match settings](reports/map/lobby_settings.md) | Map size and type, starting resources, peace time, population limit, and other lobby options. |

<a id="найти-нужный-объект"></a>
## Find an object

- On the website, search for a unit, building, or upgrade, or click a
  recognized name in a reference table to open its object card. Each card
  brings the in-game icon, cost, statistics, production or research location,
  and related links together on one page.
- [Choose a nation](reference/nations/README.md) — unique units and buildings,
  access to the 18th century, and national differences.
- [Compare units](reference/compare/units/README.md) — for example, all
  pikemen, musketeers, dragoons, or ships in the same class.
- [Compare buildings](reference/compare/buildings/README.md) — town halls,
  barracks, academies, markets, mines, and other structures.
- [Compare weapons and projectiles](reference/compare/weapons/README.md) —
  arrows, bullets, cannonballs, grenades, and the units that use them.
- [Browse the technology tree](reports/tech/tech_tree.md) — what must be
  built or researched before the object you need becomes available.
- Check [construction times](reports/economy/construction_times.md) and
  [unit production rates](reports/economy/production_rates.md).

<a id="частые-вопросы"></a>
## Common questions

- [How does a peasant gather and deliver resources?](recon/world/economy/peasant_extraction.md)
- [Why does each additional building cost more?](reports/economy/scaling_prices.md)
- [How many builders actually speed up construction?](reports/economy/builder_slots.md)
- [How is damage calculated, and why does at least one point always get through?](recon/world/combat/combat_damage_pipeline.md)
- [How does a unit choose its target?](recon/world/combat/target_selection.md)
- [What bonuses do formations provide?](recon/world/combat/formations.md)
- [How are buildings captured?](recon/world/economy/capture_mechanics.md)
- [How do towers, walls, and gates work?](recon/world/combat/towers.md)
- [What determines the initial map and resource placement?](recon/world/map/map_generation_pipeline.md)

<a id="как-читать-таблицы"></a>
## How to read the tables

The primary label is always the **canonical English name from the game
localization**. A short code in backticks—such as `pikeman` or `ruscen`—is an
internal identifier. It is shown only when needed to distinguish similar
variants or to make the underlying game files searchable.

Compact tables abbreviate resources as follows: **F** food, **W** wood,
**S** stone, **G** gold, **I** iron, and **C** coal. A “game second” is time
inside the simulation; at the Fast speed, one game second takes about
0.71 real seconds.

<a id="подробные-разборы"></a>
## In-depth material

[How the game works](recon/README.md) is for readers who need more than a
ready-made number. It explains hidden formulas, order queues, ranged-unit
behavior, map generation, artificial intelligence, and other mechanics.

The [Tables and calculations](reports/README.md) section contains expanded
comparisons of combat efficiency, attack rates, construction time, scaling
building prices, national differences, and other numerical summaries.

---

Canonical names come from the Cossacks 3 localization; values come from game
data and verifiable formulas. Project architecture, extraction limitations,
file formats, and contributor notes live in
[Technical documentation](../internals_en/README.md).
