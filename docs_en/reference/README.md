# Cossacks 3 Guide

_Extracted **2026-05-17 12:33:30** (local) from game files (unit.script mtime: 2026-04-28 03:32:28)._

Structured game reference. Every number is extracted directly from the game
scripts (`unit.script`, `country.script`, `dmscript.global`, and locale files)
and stored in [`../../data.json`](../../data.json); this directory is the
human-readable rendering of that data.

What's inside:

- **7 chapters on topics** - economics, combat, buildings, units, upgrades, market, fleet.
- **Information on nations** - a separate page for each of the 21 playable ones, with unique units, anomalies and access to the 18th century.
- **Comparisons** - side-by-side tables by unit class (all pikemen, all 18th century musketeers, etc.).
- **Formula Cheat Sheet** below on this page, plus a glossary of key game tags.

---

## Navigation

**Chapters by topic:**

| Chapter | What about |
|---|---|
| [01. Economics](01_economy/README.md) | Resource extraction: formulas, `eff`, mines, fields, hunger and upkeep, fishing. |
| [02. Combat and movement](02_combat/README.md) | Combat: damage formula, headshot, formations, dispersion, AoE, speed, counter-matrix. |
| [03. Buildings](03_buildings/README.md) | All buildings (national and general), prices, footprint. |
| [04. Units](04_units/README.md) | All units by class - infantry, cavalry, artillery, ships. |
| [05. Upgrades](05_upgrades/README.md) | All upgrades are grouped by research location. |
| [06. Market](06_market/README.md) | Market: exchange rates, first mover advantage, price degradation. |
| [07. Navy](07_naval/README.md) | Marine fleet: port, ships, transport, fisherman, DLC units. |

**Pointers to objects:**

- [`nations/`](nations/README.md) - one certificate for each of the 21 nations (what is unique about it).
- [`compare/`](compare/README.md) - comparisons of units of the same class side by side (all 17th century musketeers, all dragoons, etc.).
- [`../reports/map/lobby_settings.md`](../reports/map/lobby_settings.md) - all lobby options with canonical Russian names. The behavior of the engine for each option is in [`../recon/world/map/game_settings.md`](../recon/world/map/game_settings.md).

**Where to find the rest:**

| Catalog | What's inside |
|---|---|
| [`../reports/`](../reports/README.md) | Derived calculations: DPS, EHP, counter matrix, scaling, tech tree, production rates, builder slots, construction times, map resources. |
| [`../recon/`](../recon/README.md) | Handwritten reverse-engineering mechanics: mining, construction, RNG, ticks, server sync, map generation. |
| [`../../derived/`](../../derived/README.en.md) | Machine-readable JSON datasets (`tech_tree.json`, `canonical_terms.json`, etc.). |
| [`../architecture.md`](../architecture.md) | Data flow in a project: what comes from what. |
| [`../../data.json`](../../data.json) | Master dataset (~5.7 MB). Input for all writers and compute scripts. |

---

## Cheat sheet on formulas

Canonical formulas on which all other numbers are based. If anything in the tables below doesn't match your expectations, check this cheat sheet first: the discrepancy in the right column is usually explained by one of the formulas here.

### Resource extraction

| Resource | Portion/flight | Strikes to submission | Ideal rate (1 peasant, `eff = 100`, no road) |
|---|---:|---:|---:|
| food | **45** | 22 | ≈ 2.97 / g-sec |
| wood | **28** | 14 | ≈ 3.56 / g-sec |
| stone | **40** | 20 | ≈ 3.56 / g-sec |
| gold/iron/coal | **20** (hardcode) | n/a | through the mine: 1.664 per peasant in g-sec (without upgrades) |
`delivered = floor(portion × eff / 100)`. `eff` starts from 100; upgrades (`mill.X`, `aca.X`, `bla.X`) are added **additively**. Details - [chapter “Economy”](01_economy/README.md).

### Damage in battle
```
applied = max(1, weapon.damage
                 − target.shield                # / 3, если здание ещё строится
                 − target.protection[weapon.kind]
                 + бонусы отряда (LINE / SQUARE / KARE: +2..+7)
                 + HEADSHOT: +floor(uniqrnd × 500), 5% шанс для arrow / bullet
                                                по не-зданиям, кроме fasthorse в движении)
```
At least 1 HP always passes. Details - [`recon/world/combat/combat_damage_pipeline.md` §3](../recon/world/combat/combat_damage_pipeline.md). Source: `miscext2.script:_misc_DoDamage`.

<a id="цены-и-время"></a>
### Prices and times

- **Nth instance of a building of the same type:** `cost(N) = floor(base × (costpercent / 100)^(N-1))`. Ready tables N = 1..6 - in [`../reports/economy/scaling_prices.md`](../reports/economy/scaling_prices.md).
- **Build time with N builders:** `buildtime_sec × 1.13 / N`. Limit N - builder slots of the building (see [`../reports/economy/builder_slots.md`](../reports/economy/builder_slots.md)).
- **Real-time at fast speed:** `real_sec = g-sec / 1.4`. Speeds: slow = 7, normal = 10, fast = 14 ticks per real second.
- **`buildtime` of buildings is stored with a multiplier of 10:** `g-sec = frames × 10 / 32`, for units - `frames / 32`. In `data.json`, the `building.buildtime_sec` field already takes into account ×10.

<a id="ключевые-константы"></a>
### Key Constants

- `gc_time_to_frames = 32` - 32 frames in one game second.
- `gc_pixels_to_tile = 53.3333` — translation of `weapon.range` from pixels to tiles (for example, 800 px = 15 tiles).
- Map limits: **32000** objects in total, **12** players.
- Field: HP = **25000**. Mine without upgrades - 5 peasants, 1.664 resources / g-sec for each.

---

<a id="глоссарий-ключевые-игровые-теги"></a>
## Glossary: Key Game Tags

These are brief explanations of flags and fields that are often found in scripts and in this reference. Details are in the chapter files.

**Identifiers and common fields:**

| Tag | What does |
|---|---|
| `sid` | Internal object ID in `unit.script` (for example `bavcen`, `peaaus`, `aca.4`). |
| `cid` | Nation ID (Country ID, 0..23). See table in [04_units/README.md](04_units/README.md). |
| `usage` / `usage_short` | Unit/building class: `lightinfantry`, `fasthorse`, `building`, `tower`, etc. Affects AI and formulas. |
| `commonsid` / `cluster` | Common buildings cluster (`eur`/`rus`/`tur`/`spa`/`ukr`/`por`). For example `eurmil` is a mill for all eur-nations. |
| `costpercent` | Price multiplier for each next building instance: `cost(N) = floor(base × (cp/100)^(N-1))`. 100 = same, 300 = ×3 for the second, 0 = no scaling. |
| `farm` | By how many units does the building raise the population limit? |

**Mining and economics:**

| Tag | What does |
|---|---|
| `eff` (`resefficiency[cid][restype]`) | Current production efficiency in %. Default 100; upgrades (mill, academy) are added **additively**: `eff = 100 + Σ(upgrades)`. Real portion = `floor(base_portion × eff / 100)`. |
| `consume.food` / `consume[gold]` | How much resource a unit/building consumes per tick `gPlayer.counter.resconsume[…]`. Not to be confused with `cost` (build/hire price). |
| `peasantabsorber` | How many peasants can be inside the building (in the mine - up to 5 basic, up to 95 with upgrades). |
| `produce[restype]` | How much resource is added to `gPlayer.counter.resincome` for each peasant inside the building (for mines = 13). |
| `fieldlife` | Field strength bonus: each hit to the field removes `max(1, 100/(1+fieldlife/100))` HP instead of 100. Upgrades `aca.4` (+200) and `bla.1` (+100) give a total of 300 → 25 HP/hit, or ×4 food from the field. |

**Battle Flags:**

| Tag | What does |
|---|---|
| `bbuilt` | The building is completely completed (`True`) or still under construction (`False`). With `False`, incoming damage only subtracts `shield/3` instead of `shield`. |
| `bcapture` | The building can be captured by enemy infantry within a radius of `gc_gameplay_captureradius=4 tiles` without its defenders nearby. Capture instant. For all towers (`gc_obj_usage_tower`) it turns on automatically. |
| `bnohungry` | The unit/building does not consume food and is not killed by starvation. All buildings = `True`. Mercenaries = `True` (but they “eat” gold through Rebellion). For peasants and regular infantry = `False`. |
| `bmercenary` | Mercenary unit (`<unit>dip` suffix). They eat gold instead of food, and at `gold=0` they massively switch to neutral (see Rebellion in [01_economy/README.md](01_economy/README.md)). |
| `bfamine` | The player's hunger flag is: `food = 0` **and** there are units with `consume.food > 0`. Includes random death of units that have `bnohungry = False`. |
| `brebellion` | The player's riot flag: `gold = 0` **and** `consume[gold] > income[gold]`. Includes mass desertion of mercenaries. |
| `brised` | The resource is “active” - peasants can extract it. For wood, `True` remains even after turning the tree into a stump → endless wood pool. |
| `uniqrnd` | Random number `[0,1)`, fixed for each unit upon spawn. Used for reproducible dispersion (headshot bonus, projectile spread). See [internals/engine/determinism_audit.md](../../internals_en/engine/determinism_audit.md). |
| `gc_obj_weapon_kind_*` | Weapon type: `pike` / `sword` / `bullet` / `cannister` / `arrow` / `cannonball` / `grenade`, etc. It depends on which column The target's `protection[kind]` is subtracted from the target's damage. |

**Time:**

| Tag | What does |
|---|---|
| `gc_time_to_frames = 32` | 32 frames in one game second. All durations in scripts (animations, `pause`, `buildtime` units) are stored in frames. |
| `gc_buildtime_modifier = 10` | Additional multiplier **buildings only**: `buildtime_g_sec = frames × 10/32`. Units use `frames/32`. See [recon/world/economy/building_mechanics.md](../recon/world/economy/building_mechanics.md). |
| game speed | `slow=7 / normal=10 / fast=14` ticks/sec. On fast: `1 game-sec = 1/1.4 ≈ 0.71 real-sec`. |

---

<a id="что-в-данных"></a>
## What's in the data

The source of all numbers is `data.json`, generated by `python parser/build_data.py`. After each regeneration, automatic checks are run.

| What | How much |
|---|---:|
| Sanity checks (PASS / total) | **112 / 112** |
| Playable Nations | 21 |
| Buildings (`sid` × nation) | 456 |
| Units | 714 |
| Upgrades with fully authorized `cost / value / itype / prereqs` | 4483 |
| Groups of officers and formations | 231 |

Known parser gaps and discrepancies with external guides are in [`../known_issues.md`](../known_issues.md).
