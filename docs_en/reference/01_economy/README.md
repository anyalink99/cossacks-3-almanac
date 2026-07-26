#01. Economics

[← Index](README.md)

> **Deep Research for this chapter:**
>
> - [`../../recon/world/economy/peasant_extraction.md`](../../recon/world/economy/peasant_extraction.md) - complete analysis of the peasant cycle, animation frames, walk speed, fieldlife regeneration, formulas and open empirical questions (see §9)
> - [`../../recon/world/map/map_generation_pipeline.md`](../../recon/world/map/map_generation_pipeline.md) - what appears on the map (forests, stones, mines) and where exactly
> - [`../../reports/map/map_resources.md`](../../reports/map/map_resources.md) - counting resources on the standard map Tiny + Highlands + Rich (~109 large trees, ~33 stones, up to 12 mines / player)

## Summary

One peasant per trip brings `delivered = (portion × eff) / 100`. `eff` starts at 100, upgrades accumulate additively. The mines work according to a different scheme: each peasant inside adds 13 to `gPlayer.counter.resincome`, the real speed is 1.664 resources per game second.

## Global constants

| Parameter | Meaning | Source |
|---|---:|---|
| `gc_time_to_frames` | 32 | dmscript.global:175 |
| `gc_pixels_to_tile` | 53.3333 | dmscript.global:172 |
| `gc_settings_gamespeed_0` (slow) | 7 ticks/sec | dmscript.global:1027 |
| `gc_settings_gamespeed_1` (normal) | 10 | dmscript.global:1028 |
| `gc_settings_gamespeed_2` (fast) | 14 | dmscript.global:1029 |
| `gc_MaxObjCount` | 32000 | dmscript.global:110 |
| `gc_MaxPlayerCount` | 12 | dmscript.global:97 |
| `gc_FieldMaxHP` | 25000 | dmscript.global:128 |
| `gc_obj_foodperunit` | 30 food/unit | dmscript.global:808 |
| Default `eff` | 100% | player.script:109 |

All lobby options (starting resources, peace time, population limit, advance to the 18th century, AI difficulty, etc.) - tables in [`docs/reports/map/lobby_settings.md`](../../reports/map/lobby_settings.md), engine behavior - in [`docs/recon/world/map/game_settings.md`](../../recon/world/map/game_settings.md).

## Basic portions and hits

| Resource | Basic portion | Hits | Source |
|---|---:|---:|---|
| food | **45** | 22 | dmscript.global:799,804 |
| wood | **28** | 14 | dmscript.global:800,805 |
| stone | **40** | 20 | dmscript.global:801,806 |
| gold/iron/coal/other | **20** | n/a | unit.script:9551 (hardcode) |

## Extraction formula
```
delivered = (base_portion × eff) / 100   # integer division
```
Example: with upgrades academy.1 (+40% food) and mill.1 (+140% food) → `eff = 100 + 40 + 140 = 280`. Peasant brings `45 × 280 / 100 = 126` food per flight (instead of the base 45).

All efficiency upgrades are applied in one branch `_player_ApplyUpgrade` [^1]; their complete list is in [05_upgrades/README.md](../05_upgrades/README.md#economy-eff).

## Sources

[^1]: Applying `gc_upg_type_effect*perc` to `resefficiency[res]` - `lib/player.script:1813-1828`.

## Mines (gold/iron/coal)

Mine: HP = 2500, `buildtime` = 300 frames = 9.38 g-sec, price W100 / S100, `peasantabsorber = 5` (5 peasants max. base). Each peasant inside adds 13 to `produce[restype]`.

**Calculation:**
```
bank_per_sec = 13 × 32 = 416   # на крестьянина в игровую секунду
real_per_sec = 416 / 250 ≈ 1.664   # ресурса в игровую секунду
real_per_min = 99.84            # ≈ 100 ресурса в игровую минуту на крестьянина
```
**Full pumping of one mine** (6 upgrades):

| Level | +workers | F | G | Cumulatively |
|---:|---:|---:|---:|---:|
| eurgol.1 | +5 | 1000 | 1250 | 10 |
| eurgol.2 | +8 | 5250 | 4950 | 18 |
| eurgol.3 | +10 | 12500 | 9250 | 28 |
| eurgol.4 | +12 | 15800 | 18500 | 40 |
| eurgol.5 | +15 | 19800 | 21050 | 55 |
| eurgol.6 | +40 | 50200 | 25950 | 95 |

**Total:** 5 basic + 6 upgrades = **95 peasants/mine = 158.1 resource per g-sec = 9485 per g-min**.

**Cost of full pumping of one mine:** F104,550 + G80,950.

## Field (food, fieldlife, regeneration)

HP fields = `gc_FieldMaxHP = 25000`. Field damage per hit: `resdec = max(1, floor(100 / (1 + fieldlife / 100)))`.

| fieldlife | resdec/strike | Max. blows | Max. food at eff=100 |
|---:|---:|---:|---:|
| 0 | 100 | 250 | 511 |
| 100 | 50 | 500 | 1022 |
| 200 | 33 | 757 | 1548 |
| 300 | 25 | 1000 | 2045 |
| 500 | 16 | 1562 | 3195 |

Fieldlife upgrades: `aca.4` (+200), `bla.1` (+100). Amount = 300 → ~2045 food / field.

## Ships - fishing

`fishboat`: HP = 300, price W600, `fishingmax = 1000` (base), `fishingspeed = 50/4 = 12` ticks per fish. Upgrade `aca.5` (`+100% boat efficiency`) doubles the carrying capacity → **2000 food / flight**. The upgrade `aca.7` (`-85% fishing boat cost`) reduces the cost of construction.

The full list of ships is in [compare/units/ships.md](../compare/units/ships.md).

## Hunger and Riot - upkeep tables

> **Full analysis of the mechanics:** [`../../recon/world/economy/hunger_and_rebellion.md`](../../recon/world/economy/hunger_and_rebellion.md) (RNG difficulty thresholds, virtual mercenary player, defensive strategies). Diplomatic Center and mercenaries as a **system** - [`../../recon/systems/mercenaries_diplomacy.md`](../../recon/systems/mercenaries_diplomacy.md).

### Food consumption / g-sec per unit

Formula: `food_per_g_sec = (consume.food + 30) × 32 / 20000`, if
`bnohungry = False`. Constant `gc_obj_foodperunit = 30` —
additional portion for each eating unit.

| Unit | `consume.food` | + 30 | total | food/g-sec |
|---|---:|---:|---:|---:|
| peasant (aus / pol / spa / eng / ukr / sco) | 32 | +30 | 62 | 0.0992 |
| peasant `peatur` / `peaalg` | 28 | +30 | 58 | 0.0928 |
| peasant `pearus` | 26 | +30 | 56 | 0.0896 |
| infantry without explicit `consume.food` | 0 | +30 | 30 | 0.0480 |

**Sanity-check (verified empirically 2026-04-29):** 18 Austrian peasants are idle for 2 game minutes:
`sum = 18 × 62 = 1116` → `1116 × 32 / 20000 = 1.786 food/game sec` → **for 120 g-sec ≈ 214 food** ✓

The exact value of `bnohungry` for each unit is in [`data.json`](../../../data.json), field `bnohungry`. Briefly: buildings and mercenaries (`bmercenary = True`) - `True`; peasants, regular infantry/cavalry, officers/drummers/priests - `False`.

### Diplomatic Center

Mid-game building, requires **Academy** + Town Hall.

| Deep Center | Nations | HP | Wood | Stone | Gold |
| --- | --- | ---: | ---: | ---: | ---: |
| **Diplomatic Center** `ausdip` (default) | aus, fra, eng, spa, pol… (+12) | 4500 | 4900 | 1700 | 0 |
| **Diplomatic Center** `rusdip` (rus) | rus | 6500 | 7900 | 3700 | 0 |
| **Diplomatic Center** `ukrdip` (ukr) | ukr | 5000 | 3900 | 2700 | 0 |
| **Diplomatic Center** `turdip` (tur/alg) | tur, alg | 5500 | 4600 | 2020 | 0 |

For everyone: `buildtime = 1000` frames = **312.5 g-sec**, `costpercent = 100`, `bcapture = False`. According to localization - “you can only build one Diplomatic Center per player” (GUI limitation, not `costpercent`).

### Mercenary Catalog
8 sid, the roster is the same for **all 21 nations**. Price and upkeep in gold; `bnohungry = True` (food is not consumed).

| Mercenary | HP | bt, g-sec | gold (price) | gold/tick upkeep | costpercent | Weapons |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| **Light Infantryman (mercenary)** `lightinfantrydip` | 50 | 1.25 | **4** | 4 | 100 | sword 16 |
| **Roundshier (mercenary)** `roundshierdip` | 75 | 1.5 | **12** | 20 | 100 | sword 6 |
| **Archer (mercenary)** `archerdip` | 20 | 1.25 | **15** | 16 | 100.5 | arrow 25 (range 13.13 t) / firearrow 100 (range 14.06 t) |
| **Turkish archer (mercenary)** `archerturdip` | 20 | 1.25 | **15** | 16 | 100.5 | arrow 25 (range 13.13 t) / firearrow 100 (range 14.06 t) |
| **Grenadier (mercenary)** `grenadierdip` | 30 | 1.5 | **25** | 60 | 100.5 | pike 30 / bullet 16 (range 15.0 t) / mortarball 200 (range 7.5 t) |
| **Sich Cossack (mercenary)** `cossacksichdip` | 150 | 2.5 | **60** | 150 | 100.5 | sword 8 |
| **Dragoon, 18th century (mercenary)** `dragoon18dip` | 100 | 2.0 | **120** | 120 | 102 | bullet 18 (range 15.0 t) |
| **Light cavalry (mercenary)** `lightcavalrydip` | 100 | 2.0 | **120** | 120 | 102 | bullet 18 (range 15.0 t) |

The gold-upkeep formula is the same as food: `Σ(consume.gold) × 32 / 20000`. For example, 50 `dragoon18dip` → `50 × 120 × 0.0016 = 9.6 gold/game sec ≈ 576 gold/game min`.

**Price scaling:** general rule `cost(N) = floor(base × (costpercent/100)^(N−1))`, but the ceiling for mercenaries is **2×** (instead of 20000× for regular units). Paired counters:
- `archerdip` ↔ `archerturdip` - general counter in price calculation.
- `dragoon18dip` ↔ `lightcavalrydip` - similar.

**Card mode `marketdip = expensivemercs`** includes `gc_gameplay_expensivemercskoef = 3` - mercenaries are three times more expensive in gold.

<a id="расход-gold-юнитами"></a>
### Gold consumption by units

`consume[gold]` occurs in:
- **Towers** (`consume[gold] = 500` → 0.8 gold / g-sec ≈ 48 per g-minute) - a constant tax regardless of the battle. See [`../../recon/world/combat/towers.md` §2](../../recon/world/combat/towers.md).
- **Mercenaries** via `consume.gold` - permanent upkeep of all 8 sid.
- **Shooting units** - only per shot through `weapon.cost[gold]`, not idle.

Normal pikemen and musketeers **do not consume gold when idle**.

## Sanity

Sanity checks: **112/112** PASS. See xlsx → sheet `Sanity_checks`.
