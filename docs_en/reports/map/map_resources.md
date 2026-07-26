<a id="оценка-ресурсов-карты--tiny-256256--highlands--шахты-rich"></a>
<a id="сколько-ресурсов-появляется-на-карте"></a>
# Map resources

[← Tables and calculations](../README.md)

An approximate count of forests, stone deposits, and mines for one commonly
used set of match settings. Natural-object counts are estimates: uneven ground
and occupied points prevent some objects from being placed.

## Settings used

| Setting | Selected value |
|---|---|
| Map size | **Tiny**, 256×256 tiles |
| Relief | **Highlands** |
| Resource deposits | **Rich** |
| Terrain type | Land |

See [Match settings](lobby_settings.md) for the other available values.

<a id="1-модификаторы-вероятности-паттернов-оценка"></a>
<a id="настройки-расчёта"></a>
## 1. Pattern probability modifiers (evaluation)

Simulation of `_misc_GetFreePatternMaskCountModifier` at 256×256 with ~2% water (Land terrain - almost open field):

| testsize | calibration | raw_count(sim) | probe_raw | × modifier (2.5) |
|---:|---:|---:|---:|---:|
| 12 | 340 | 252 | 0.741 | **1.853** |
| 16 | 182 | 142 | 0.780 | **1.951** |
| 24 | 74 | 61 | 0.824 | **2.061** |
| 29 | 55 | 40 | 0.727 | **1.818** |

⚠ The simulation assumes that the water is one contiguous block, rather than scattered pixels.

<a id="2-плотности-после-умножения-на-вероятность"></a>
<a id="оценка-лесов-и-камней"></a>
## 2. Densities after multiplication by probability

| Var | base | ×prob | final density | needed = floor(area × density) |
|---|---:|---:|---:|---:|
| frs_big | 0.000900 | × probsmall = 1.853 | 0.001668 | 109 |
| frs_mid | 0.000900 | × probmid = 1.951 | 0.001755 | 115 |
| frs_small | 0.000540 | × problarge = 2.061 | 0.001113 | 72 |
| stn1 | 0.000160 | × probsmall = 1.853 | 0.000296 | 19 |
| stn2 | 0.000120 | × probsmall = 1.853 | 0.000222 | 14 |

<a id="3-запросы-паттернов-на-вызов"></a>
<a id="запасы-древесины-и-камня"></a>
## 3. Pattern requests (per call)

Each forest density is distributed into N different forest types (foreststype=0 → 4 big / 3 mid / 2 small types). Column **placement rate** — empirically calibrated per-type (for homogeneous Tiny+Land+Highlands bucket); for unknown types - fallback default `placement_success`.

| Pattern Type | frequency per call | need to call | placement rate | posted |
|---|---:|---:|---:|---:|
| `forests_pinefir_big` | 0.000208 | 13 | 0.07 | ~1 |
| `forests_spruce_big` | 0.000208 | 13 | 0.20 | ~3 |
| `forests_pine_big` | 0.000208 | 13 | 0.81 | ~11 |
| `forests_pine_big_2` | 0.000208 | 13 | 0.74 | ~10 |
| `forests_spruce_medium` | 0.000293 | 19 | 0.04 | ~1 |
| `forests_pinefir_medium` | 0.000293 | 19 | 0.09 | ~2 |
| `forests_pine_medium` | 0.000293 | 19 | 0.76 | ~14 |
| `forests_pinefir_small` | 0.000278 | 18 | 0.03 | ~1 |
| `forests_pine_small` | 0.000278 | 18 | 0.64 | ~12 |
| `stones` (stn1) | 0.000296 | 19 | 0.58 | ~11 |
| `stones` (stn2) | 0.000222 | 14 | 0.58 | ~8 |

**Where are placement rates taken from:** empirically from 10 replay samples (Tiny+Land+Highlands+4pl_nowater bucket). The size of the pattern footprint (mask cells) is the main factor: pine_big mask=148 → ~80% placement; pinefir_big mask=920 → ~7%. Methodology and complete table - `recon/map_generation_pipeline.md` §14. For non-Tiny/non-Highlands settings the numbers should be different - calibration is not extrapolated.

<a id="4-всего-кластеров-оценка"></a>
<a id="месторождения-у-каждого-игрока"></a>
## 4. Total clusters (estimate)

- Big forest clusters: **~25**
- Medium forest clusters: **~17**
- Small forest clusters: **~13**
- Stone clusters: **~19**

<a id="5-деревья-и-камни--per-pattern-type"></a>
## 5. Trees and stones - per pattern type
Numbers = median of `mask=1` cells for each pattern type from `derived/pattern_type_stats.json` (parser: `parser/parse_pattern_inventory.py`, mapping pattern→type from `data/game/var/generator.cfg`). Hypothesis: 1 mask cell = 1 tree (confirmed on brushes; for mines mask = footprint, not objects - see caveat).

**Calibration:** mask cells (placement slots) × **0.3** ≈ visible chopable trees. Source: empirical user assessment (small forest = ~10 trees, big = ~50). Cross-validation: forests_pine_big median mask = 148 → 148 × 0.34 = 50 ✓. See caveat at the beginning of the file.

| pattern type | clusters placed | mask cells/cluster | trees/cluster | total trees |
|---|---:|---:|---:|---:|
| `forests_pinefir_big` (big) | 1 | 920 | 276 | 276 |
| `forests_spruce_big` (big) | 3 | 571 | 171 | 513 |
| `forests_pine_big` (big) | 11 | 148 | 44 | 484 |
| `forests_pine_big_2` (big) | 10 | 185 | 56 | 560 |
| `forests_spruce_medium` (mid) | 1 | 469 | 141 | 141 |
| `forests_pinefir_medium` (mid) | 2 | 311 | 93 | 186 |
| `forests_pine_medium` (mid) | 14 | 59 | 18 | 252 |
| `forests_pinefir_small` (small) | 1 | 172 | 52 | 52 |
| `forests_pine_small` (small) | 12 | 44 | 13 | 156 |
| `stones` | 19 | 138 | 41 | 779 |

⚠ **Caveat about mask=1 interpretation:** brushes confirm (brush_plt_1x1: 8 mask = 8 visible bushes), but mines (`mng/mni/mnc`) - 32 mask cells = **1 deposit** (mask = collision footprint). For forests we assume "1 cell = 1 tree", but without in-game test this is upper bound. The exact number is empirical.

**Total trees on the map:** ~2,620
**Total stones on the map:** ~779

<a id="6-запасы-древесины-и-камня"></a>
## 6. Wood and stone reserves

**Wood - actually infinite.** When the tree's HP reaches 0, the [^1] engine:
- changes mesh to `pinestump<N>` (visually stump)
- **DOES NOT change** `brised=True` → the stump remains a valid target for searching
- continues to take hits: `hp -= 1, peasant.resamount += 1` (even with HP < 0)

Therefore, the wood pool on the map is **not limited by the number of trees**. Mediume initial HP (2474/tree from distribution: 20% giants 8-16K HP / 15% medium 125-624 / 45% small 10-60 / 20% stubs 10) only determines how many “free” hits before switching to endless mining mode.

Sum of initial HP of all trees: ~6,481,880 hits ≈ **12,963,760 “free” wood** @ eff=100 after which the same forest continues to give the same speed through stumps.

**Real bottleneck for wood:** number of simultaneous slots (maxattackers_wood = 2 per tree/stump), peasant speed and distance to warehouse, not quantity.

**Stone:** each stone has HP=10,000,000 (effectively infinite). ~779 gems × 10M HP = unlimited supply.

<a id="7-месторождения-resourcesrich-tiny"></a>
## 7. Deposits (Resources=Rich, Tiny)

**Terminology:** *field* - geological deposit on the ground (placed by `SetupMines`, basenames `minegold`/`mineiron`/`minecoal`). *Mine* - building `eurgol`/`euriro`/`eurcoa`, which the player builds on the mine as a peasant (peasantabsorber=5, upgrades to 95).

Parameters from [^2]:
- minesdensity=2 → **5 rounds** per starting point.
- On tiny, round 4 is skipped through `continue` → **4 effective rounds**.
- In each round, **1 deposit of each type** (gold/iron/coal) is bet.
- **Total: 4 gold + 4 iron + 4 coal = 12 deposits per player** (if all attempts are successful; up to 256 attempts per placement).

Distances from start (mapsize>2 = tiny, gRecordGeneratorVersion ≥ 80):
- **round 0**: 14-22 tiles (Phase 1, when creating a start point - 1 gold + 1 iron + 1 coal)
- **round 1**: 32-42 tiles (Phase 2)
- **round 2**: 70-82 tiles (Phase 2)
- **round 3**: 22-38 tiles (Phase 2)
- ~~round 4~~: skipped on tiny

<a id="8-допущения-и-предел-точности"></a>
## 8. Assumptions and limits of accuracy

**What exactly (from the code):**
- The formula `count = floor(W*H*freq)` is straight from `_misc_SetupPatternsByType`.
- Densities `frs_big/mid/small/stn1/stn2` - [^3].
- Modifier ×2.5 for tiny - [^4].
- Mine rounds - [^5].
- Per-position mine count formula `P × (1 + n_after) + (spcount - P) × n_after`.

**What is empirically validated (replay-based, 2026-04-29):**
- Per-type placement rates — calibrated for 10 sample replays (Tiny+Land+Highlands+4pl_nowater bucket). Bucket ratios actual/predicted = 0.96-1.04 for all major types (forests_pine_*, stones, mng/mni/mnc).
- Pipeline: `parser/parse_replay_aggregates.py` → `compute/validate_map_predictions.py`. Output: `internals_en/data/map_predictions_validation.md`.
- Player count is derived from mng count for Land terrain (the formula is reversible).

**What is assessed/not validated:**
- `prob*` modifiers - Monte Carlo simulation `_misc_GetFreePatternMaskCountModifier`. For tiny with the assumption of weak water blocking (`water_blocking_pct=0.02`).
- Trees/stones per pattern - `TREE_CHOPABLE_RATIO=0.30` calibrated based on the user's empirical assessment (small=10 trees, big=50 trees). Not verified against real in-game tree count.
- On non-Tiny / non-Highlands settings placement rates **may vary** - no data.

**Open spaces:**
- Pattern types `plain_*`, `mountains`, `swamp_small`, `hills_*`, `stoneforests`, `plateau*` **not predicted** `compute_counts` (~50% of all cluster occurrences in replay-data). It is necessary to expand the model - see [`recon/world/map/map_generation_pipeline.md`](../../recon/world/map/map_generation_pipeline.md) §13 Q7.
- `desert_*` (season=3) not implemented - 1/20 replays.
- Non-Land mine formula is different - open question §13 Q6.

**Accuracy limit (Tiny+Land+Highlands):** ±5% predicted cluster counts for covered types. For total wood pool / stones - ±30-50% (TREE_CHOPABLE_RATIO is not validated).

<a id="источники"></a>
## Sources

All links are relative to `data/scripts/` in the Cossacks 3 installation.

[^1]: turning a tree into a stump with `hp = 0` - `units/unit.inc/onaclanimationreachedwork.inc:30-39 + units/env.inc/ontagstates.inc:50-78`.

[^2]: Deposit placement phase: `mines rounds` and skip round 4 on tiny - `common.inc/dogenerate.inc:522-717`.

[^3]: base densities `frs_big/mid/small/stn1/stn2` - `common.inc/dogenerate.inc:1688-1693`.

[^4]: modifier ×2.5 for tiny - `common.inc/dogenerate.inc:1718-1725`.

[^5]: number and geometry of field placement rounds - `common.inc/dogenerate.inc:528-602`.
