<a id="проверка-расчётной-модели-ресурсов-карты-по-реплеям"></a>
# Replay-based validation of the map resource model

Comparison of `compute_map_resources.compute_counts(...)` with actual cluster counts from replay and save files (`derived/replay_ground_truth.json`). See [match settings reference](../../docs_en/reports/map/lobby_settings.md) for the meaning of `mapsize`, `relieftype`, `terraintype`, and `season`.

**Replays processed:** 25

<a id="группы-одинаковых-настроек"></a>
## Groups with identical settings

Replays are grouped by `(mapsize, relieftype, terraintype, mask_kind)`. Calibration is meaningful **only within one bucket**, where predictions are comparable. A cross-bucket average can approach 1.0 by accident (Tiny underestimates while Huge overestimates).

| Size (`mapsize`) | Relief (`relieftype`) | Terrain (`terraintype`) | Mask | Replays |
| --- | --- | --- | --- | ---: |
| 3 | 3 | 0 | `4pl_nowater` | 13 |
| 0 | 5 (Random) | 5 | `4pl_continent` | 2 |
| 3 | 5 (Random) | 5 | `4pl_continent` | 2 |
| 0 | 5 (Random) | 1 | `4pl_mediterranean` | 1 |
| 1 | 3 | 0 | `6pl_nowater` | 1 |
| 2 | 5 (Random) | 2 | `7pl_peninsulas` | 1 |
| 2 | 5 (Random) | 9 | `3pl_coastal` | 1 |
| 3 | 0 | 0 | `4pl_nowater` | 1 |
| 3 | 3 | 5 | `2pl_continent` | 1 |
| 3 | 3 | 7 | `2pl_lakes` | 1 |
| 3 | 5 (Random) | 0 | `4pl_nowater` | 1 |

<a id="проверка-по-типам-для-крупнейшей-группы-13-реплеев"></a>
## Per-type validation for the largest group (13 replays)

Group settings: size (`mapsize`) — 3, relief (`relieftype`) — 3, terrain (`terraintype`) — 0, mask — `4pl_nowater`.

| Internal pattern type | Replay average | Predicted average | Ratio | Replays |
| --- | ---: | ---: | ---: | ---: |
| `plain_small` | 28.1 | 0.0 | — | 12 |
| `stones` | 20.2 | 19.0 | 1.06 | 13 |
| `plain_medium` | 16.6 | 0.0 | — | 12 |
| `mnc` | 15.0 | 15.0 | 1.00 | 13 |
| `mng` | 15.0 | 15.0 | 1.00 | 13 |
| `mni` | 15.0 | 15.0 | 1.00 | 13 |
| `forests_pine_medium` | 14.4 | 14.0 | 1.03 | 13 |
| `forests_pine_small` | 11.5 | 12.0 | 0.96 | 13 |
| `mountains` | 11.3 | 0.0 | — | 12 |
| `swamp_small` | 11.1 | 0.0 | — | 12 |
| `forests_pine_big` | 10.8 | 11.0 | 0.99 | 13 |
| `forests_pine_big_2` | 10.5 | 10.0 | 1.05 | 13 |
| `forests_spruce_big` | 3.2 | 3.0 | 1.08 | 13 |
| `stoneforests` | 3.0 | 0.0 | — | 12 |
| `plain_huge` | 1.8 | 0.0 | — | 11 |
| `hills_dark` | 1.8 | 0.0 | — | 12 |
| `forests_pinefir_medium` | 1.5 | 2.0 | 0.73 | 13 |
| `forests_pinefir_big` | 1.4 | 1.0 | 1.38 | 13 |
| `hills_light` | 1.3 | 0.0 | — | 9 |
| `plain_big` | 1.1 | 0.0 | — | 7 |
| `plateau_big` | 1.1 | 0.0 | — | 8 |
| `decor_big` | 1.0 | 0.0 | — | 1 |
| `plateau` | 1.0 | 0.0 | — | 6 |
| `plateau_small` | 1.0 | 0.0 | — | 1 |
| `swamp_medium` | 1.0 | 0.0 | — | 1 |
| `forests_spruce_medium` | 0.8 | 1.0 | 0.85 | 13 |
| `forests_pinefir_small` | 0.8 | 1.0 | 0.77 | 13 |

<a id="общее-сравнение-по-всем-реплеям"></a>
## Combined comparison across all replays

Averaging across map sizes and relief types can hide a systematic error for an individual setting. Use the largest group above for calibration.

| Internal pattern type | Replay average | Predicted average | Ratio | Replays |
| --- | ---: | ---: | ---: | ---: |
| `plain_small` | 50.3 | 0.0 | — | 23 |
| `desert_stones` | 29.0 | 0.0 | — | 1 |
| `forests_pine_small` | 25.6 | 29.4 | 0.87 | 25 |
| `mountains` | 24.9 | 0.0 | — | 20 |
| `desert_forests_medium` | 24.0 | 0.0 | — | 1 |
| `stones` | 22.5 | 47.2 | 0.48 | 25 |
| `forests_pine_medium` | 22.4 | 35.1 | 0.64 | 25 |
| `plain_medium` | 22.0 | 0.0 | — | 22 |
| `forests_pine_big` | 18.7 | 26.7 | 0.70 | 25 |
| `desert_lake` | 15.0 | 0.0 | — | 1 |
| `mng` | 14.8 | 16.2 | 0.92 | 25 |
| `mni` | 14.7 | 16.2 | 0.91 | 25 |
| `mnc` | 14.5 | 16.2 | 0.90 | 25 |
| `desert_forests_small` | 11.0 | 0.0 | — | 1 |
| `forests_pine_big_2` | 10.8 | 24.4 | 0.44 | 25 |
| `swamp_small` | 10.1 | 0.0 | — | 23 |
| `desert_mnc` | 8.0 | 0.0 | — | 1 |
| `desert_mng` | 8.0 | 0.0 | — | 1 |
| `desert_mni` | 8.0 | 0.0 | — | 1 |
| `desert_mountains` | 8.0 | 0.0 | — | 1 |
| `desert_plain_small` | 5.0 | 0.0 | — | 1 |
| `forests_spruce_big` | 4.2 | 6.8 | 0.63 | 25 |
| `stoneforests` | 3.3 | 0.0 | — | 23 |
| `hills_dark` | 3.1 | 0.0 | — | 19 |
| `desert_plain_big` | 3.0 | 0.0 | — | 1 |
| `desert_forests_unique` | 2.0 | 0.0 | — | 1 |
| `plain_huge` | 2.0 | 0.0 | — | 16 |
| `plain_big` | 1.8 | 0.0 | — | 12 |
| `hills_light` | 1.5 | 0.0 | — | 14 |
| `forests_pinefir_big` | 1.4 | 2.4 | 0.59 | 25 |
| `forests_pinefir_medium` | 1.4 | 4.4 | 0.32 | 25 |
| `plateau_big` | 1.3 | 0.0 | — | 11 |
| `forests_spruce_medium` | 1.1 | 2.0 | 0.57 | 25 |
| `plateau` | 1.1 | 0.0 | — | 10 |
| `decor_big` | 1.0 | 0.0 | — | 1 |
| `plateau_small` | 1.0 | 0.0 | — | 1 |
| `swamp_medium` | 1.0 | 0.0 | — | 2 |
| `forests_pinefir_small` | 0.6 | 1.8 | 0.34 | 25 |

<a id="данные-по-отдельным-реплеям"></a>
## Per-replay data

Each replay sample includes its settings and a difference table. Pattern types with large discrepancies are marked ⚠. Names are opaque: `Replay NN` is assigned deterministically from the content hash; see `parse_replay_aggregates.py`.

### Replay 09

- mask: `4pl_mask_mediterranean_87_gauss.tga`
- size (`mapsize`) — 0, relief (`relieftype`) — 5, mines (`resourcemines`) — 2, terrain (`terraintype`) — 1, season (`season`) — 0
- inferred players: **4/4** (from the gold-mine count; Land only)

| Internal pattern type | Replay | Predicted | Ratio |
| --- | ---: | ---: | ---: |
| `plain_small` | 39 | 0 | — |
| `stones` | 22 | 38 | 0.58 |
| `forests_pine_medium` | 21 | 28 | 0.75 |
| `forests_pine_small` | 18 | 22 | 0.82 |
| `plain_medium` | 18 | 0 | — |
| `forests_pine_big` | 15 | 21 | 0.71 |
| `mnc` | 15 | 20 | 0.75 |
| `mng` | 15 | 20 | 0.75 |
| `mni` | 15 | 20 | 0.75 |
| `swamp_small` | 13 | 0 | — |
| `forests_pine_big_2` | 10 | 19 | 0.53 |
| `forests_spruce_big` | 4 | 5 | 0.80 |
| `mountains` | 4 | 0 | — |
| `plain_huge` | 4 | 0 | — |
| `forests_spruce_medium` | 3 | 1 | 3.00 ⚠ |
| `plain_big` | 3 | 0 | — |
| `stoneforests` | 3 | 0 | — |
| `hills_dark` | 2 | 0 | — |
| `hills_light` | 2 | 0 | — |
| `plateau` | 2 | 0 | — |
| `plateau_big` | 2 | 0 | — |
| `forests_pinefir_big` | 1 | 2 | 0.50 |
| `_n_real_players` | 0 | 4 | 0.00 ⚠ |
| `_spcount` | 0 | 4 | 0.00 ⚠ |
| `forests_pinefir_medium` | 0 | 3 | 0.00 ⚠ |
| `forests_pinefir_small` | 0 | 1 | 0.00 ⚠ |

### Replay 03

- mask: `4pl_mask_continent_43_gauss.tga`
- size (`mapsize`) — 0, relief (`relieftype`) — 5, mines (`resourcemines`) — 2, terrain (`terraintype`) — 5, season (`season`) — 0
- inferred players: **4/4** (from the gold-mine count; Land only)

| Internal pattern type | Replay | Predicted | Ratio |
| --- | ---: | ---: | ---: |
| `mnc` | 16 | 20 | 0.80 |
| `mng` | 16 | 20 | 0.80 |
| `mni` | 16 | 20 | 0.80 |
| `stones` | 11 | 38 | 0.29 ⚠ |
| `forests_pine_big_2` | 5 | 19 | 0.26 ⚠ |
| `plain_small` | 4 | 0 | — |
| `stoneforests` | 4 | 0 | — |
| `swamp_small` | 3 | 0 | — |
| `forests_pine_medium` | 2 | 28 | 0.07 ⚠ |
| `forests_pinefir_big` | 2 | 2 | 1.00 |
| `forests_spruce_medium` | 2 | 1 | 2.00 |
| `plain_medium` | 2 | 0 | — |
| `forests_pine_big` | 1 | 21 | 0.05 ⚠ |
| `forests_pine_small` | 1 | 22 | 0.05 ⚠ |
| `forests_pinefir_medium` | 1 | 3 | 0.33 ⚠ |
| `forests_spruce_big` | 1 | 5 | 0.20 ⚠ |
| `_n_real_players` | 0 | 4 | 0.00 ⚠ |
| `_spcount` | 0 | 4 | 0.00 ⚠ |
| `forests_pinefir_small` | 0 | 1 | 0.00 ⚠ |

### Replay 10

- mask: `4pl_mask_continent_82_gauss.tga`
- size (`mapsize`) — 0, relief (`relieftype`) — 5, mines (`resourcemines`) — 2, terrain (`terraintype`) — 5, season (`season`) — 0
- inferred players: **4/4** (from the gold-mine count; Land only)

| Internal pattern type | Replay | Predicted | Ratio |
| --- | ---: | ---: | ---: |
| `mng` | 16 | 20 | 0.80 |
| `mnc` | 15 | 20 | 0.75 |
| `mni` | 15 | 20 | 0.75 |
| `stones` | 12 | 38 | 0.32 ⚠ |
| `plain_small` | 9 | 0 | — |
| `swamp_small` | 8 | 0 | — |
| `forests_pine_medium` | 6 | 28 | 0.21 ⚠ |
| `forests_pine_big` | 5 | 21 | 0.24 ⚠ |
| `forests_pine_big_2` | 5 | 19 | 0.26 ⚠ |
| `forests_pine_small` | 3 | 22 | 0.14 ⚠ |
| `plain_medium` | 3 | 0 | — |
| `stoneforests` | 3 | 0 | — |
| `forests_spruce_big` | 2 | 5 | 0.40 ⚠ |
| `forests_pinefir_medium` | 1 | 3 | 0.33 ⚠ |
| `forests_spruce_medium` | 1 | 1 | 1.00 |
| `mountains` | 1 | 0 | — |
| `_n_real_players` | 0 | 4 | 0.00 ⚠ |
| `_spcount` | 0 | 4 | 0.00 ⚠ |
| `forests_pinefir_big` | 0 | 2 | 0.00 ⚠ |
| `forests_pinefir_small` | 0 | 1 | 0.00 ⚠ |

### Replay 17

- mask: `6pl_mask_nowater_5_gauss.tga`
- size (`mapsize`) — 1, relief (`relieftype`) — 3, mines (`resourcemines`) — 1, terrain (`terraintype`) — 0, season (`season`) — 0
- inferred players: **6/6** (from the gold-mine count; Land only)

| Internal pattern type | Replay | Predicted | Ratio |
| --- | ---: | ---: | ---: |
| `plain_small` | 143 | 0 | — |
| `forests_pine_small` | 101 | 76 | 1.33 |
| `mountains` | 88 | 0 | — |
| `forests_pine_medium` | 77 | 93 | 0.83 |
| `forests_pine_big` | 66 | 70 | 0.94 |
| `plain_medium` | 52 | 0 | — |
| `stones` | 46 | 126 | 0.37 ⚠ |
| `forests_pine_big_2` | 29 | 64 | 0.45 ⚠ |
| `mnc` | 24 | 24 | 1.00 |
| `mng` | 24 | 24 | 1.00 |
| `mni` | 24 | 24 | 1.00 |
| `swamp_small` | 16 | 0 | — |
| `hills_dark` | 11 | 0 | — |
| `forests_spruce_big` | 8 | 17 | 0.47 ⚠ |
| `stoneforests` | 6 | 0 | — |
| `forests_pinefir_big` | 5 | 6 | 0.83 |
| `plain_big` | 5 | 0 | — |
| `forests_pinefir_medium` | 4 | 11 | 0.36 ⚠ |
| `forests_spruce_medium` | 2 | 5 | 0.40 ⚠ |
| `forests_pinefir_small` | 1 | 4 | 0.25 ⚠ |
| `hills_light` | 1 | 0 | — |
| `plain_huge` | 1 | 0 | — |
| `plateau` | 1 | 0 | — |
| `_n_real_players` | 0 | 6 | 0.00 ⚠ |
| `_spcount` | 0 | 6 | 0.00 ⚠ |

### Replay 11

- mask: `7pl_mask_peninsulas_3_gauss.tga`
- size (`mapsize`) — 2, relief (`relieftype`) — 5, mines (`resourcemines`) — 2, terrain (`terraintype`) — 2, season (`season`) — 0
- inferred players: **7/7** (from the gold-mine count; Land only)

| Internal pattern type | Replay | Predicted | Ratio |
| --- | ---: | ---: | ---: |
| `plain_small` | 220 | 0 | — |
| `forests_pine_small` | 117 | 182 | 0.64 |
| `forests_pine_medium` | 98 | 217 | 0.45 ⚠ |
| `mountains` | 87 | 0 | — |
| `plain_medium` | 78 | 0 | — |
| `forests_pine_big` | 77 | 163 | 0.47 ⚠ |
| `stones` | 68 | 290 | 0.23 ⚠ |
| `mnc` | 27 | 35 | 0.77 |
| `mng` | 27 | 35 | 0.77 |
| `mni` | 27 | 35 | 0.77 |
| `forests_pine_big_2` | 22 | 149 | 0.15 ⚠ |
| `swamp_small` | 20 | 0 | — |
| `forests_spruce_big` | 15 | 40 | 0.38 ⚠ |
| `hills_dark` | 8 | 0 | — |
| `stoneforests` | 6 | 0 | — |
| `forests_pinefir_big` | 3 | 14 | 0.21 ⚠ |
| `forests_pinefir_medium` | 2 | 26 | 0.08 ⚠ |
| `forests_spruce_medium` | 2 | 11 | 0.18 ⚠ |
| `plain_big` | 2 | 0 | — |
| `forests_pinefir_small` | 1 | 9 | 0.11 ⚠ |
| `_n_real_players` | 0 | 7 | 0.00 ⚠ |
| `_spcount` | 0 | 7 | 0.00 ⚠ |

### Replay 18

- mask: `3pl_mask_coastal_1_gauss.tga`
- size (`mapsize`) — 2, relief (`relieftype`) — 5, mines (`resourcemines`) — 1, terrain (`terraintype`) — 9, season (`season`) — 0
- inferred players: **3/3** (from the gold-mine count; Land only)

| Internal pattern type | Replay | Predicted | Ratio |
| --- | ---: | ---: | ---: |
| `plain_small` | 334 | 0 | — |
| `forests_pine_small` | 220 | 182 | 1.21 |
| `mountains` | 174 | 0 | — |
| `forests_pine_big` | 135 | 163 | 0.83 |
| `forests_pine_medium` | 132 | 217 | 0.61 |
| `plain_medium` | 99 | 0 | — |
| `stones` | 81 | 290 | 0.28 ⚠ |
| `forests_pine_big_2` | 35 | 149 | 0.23 ⚠ |
| `forests_spruce_big` | 15 | 40 | 0.38 ⚠ |
| `swamp_small` | 11 | 0 | — |
| `hills_dark` | 10 | 0 | — |
| `mnc` | 9 | 12 | 0.75 |
| `mng` | 9 | 12 | 0.75 |
| `mni` | 9 | 12 | 0.75 |
| `stoneforests` | 3 | 0 | — |
| `forests_pinefir_medium` | 2 | 26 | 0.08 ⚠ |
| `forests_pinefir_small` | 2 | 9 | 0.22 ⚠ |
| `plain_big` | 2 | 0 | — |
| `forests_spruce_medium` | 1 | 11 | 0.09 ⚠ |
| `hills_light` | 1 | 0 | — |
| `plain_huge` | 1 | 0 | — |
| `swamp_medium` | 1 | 0 | — |
| `_n_real_players` | 0 | 3 | 0.00 ⚠ |
| `_spcount` | 0 | 3 | 0.00 ⚠ |
| `forests_pinefir_big` | 0 | 14 | 0.00 ⚠ |

### Replay 12

- mask: `4pl_mask_nowater_173_gauss.tga`
- size (`mapsize`) — 3, relief (`relieftype`) — 0, mines (`resourcemines`) — 2, terrain (`terraintype`) — 0, season (`season`) — 0
- inferred players: **2/4** (from the gold-mine count; Land only)

| Internal pattern type | Replay | Predicted | Ratio |
| --- | ---: | ---: | ---: |
| `plain_small` | 31 | 0 | — |
| `stones` | 21 | 19 | 1.11 |
| `forests_pine_medium` | 15 | 14 | 1.07 |
| `forests_pine_small` | 14 | 12 | 1.17 |
| `mnc` | 14 | 14 | 1.00 |
| `mng` | 14 | 14 | 1.00 |
| `mni` | 14 | 14 | 1.00 |
| `plain_medium` | 14 | 0 | — |
| `forests_pine_big` | 11 | 11 | 1.00 |
| `forests_pine_big_2` | 10 | 10 | 1.00 |
| `swamp_small` | 8 | 0 | — |
| `forests_spruce_big` | 6 | 3 | 2.00 |
| `hills_dark` | 4 | 0 | — |
| `hills_light` | 4 | 0 | — |
| `plain_huge` | 4 | 0 | — |
| `forests_pinefir_big` | 3 | 1 | 3.00 ⚠ |
| `mountains` | 2 | 0 | — |
| `plain_big` | 2 | 0 | — |
| `stoneforests` | 2 | 0 | — |
| `forests_pinefir_medium` | 1 | 2 | 0.50 |
| `forests_pinefir_small` | 1 | 1 | 1.00 |
| `_n_real_players` | 0 | 2 | 0.00 ⚠ |
| `_spcount` | 0 | 4 | 0.00 ⚠ |
| `forests_spruce_medium` | 0 | 1 | 0.00 ⚠ |

### Replay 23

- mask: `4pl_mask_nowater_172_gauss.tga`
- size (`mapsize`) — 3, relief (`relieftype`) — 3, mines (`resourcemines`) — 1, terrain (`terraintype`) — 0, season (`season`) — 0
- inferred players: **4/4** (from the gold-mine count; Land only)

| Internal pattern type | Replay | Predicted | Ratio |
| --- | ---: | ---: | ---: |
| `plain_small` | 23 | 0 | — |
| `stones` | 23 | 19 | 1.21 |
| `mnc` | 16 | 16 | 1.00 |
| `mng` | 16 | 16 | 1.00 |
| `mni` | 16 | 16 | 1.00 |
| `plain_medium` | 15 | 0 | — |
| `forests_pine_medium` | 12 | 14 | 0.86 |
| `forests_pine_big_2` | 11 | 10 | 1.10 |
| `forests_pine_big` | 10 | 11 | 0.91 |
| `forests_pine_small` | 10 | 12 | 0.83 |
| `mountains` | 9 | 0 | — |
| `swamp_small` | 9 | 0 | — |
| `forests_pinefir_big` | 5 | 1 | 5.00 ⚠ |
| `forests_spruce_big` | 4 | 3 | 1.33 |
| `stoneforests` | 4 | 0 | — |
| `forests_spruce_medium` | 2 | 1 | 2.00 |
| `plain_big` | 2 | 0 | — |
| `hills_dark` | 1 | 0 | — |
| `plain_huge` | 1 | 0 | — |
| `plateau` | 1 | 0 | — |
| `_n_real_players` | 0 | 4 | 0.00 ⚠ |
| `_spcount` | 0 | 4 | 0.00 ⚠ |
| `forests_pinefir_medium` | 0 | 2 | 0.00 ⚠ |
| `forests_pinefir_small` | 0 | 1 | 0.00 ⚠ |

### Replay 21

- mask: `4pl_mask_nowater_172_gauss.tga`
- size (`mapsize`) — 3, relief (`relieftype`) — 3, mines (`resourcemines`) — 1, terrain (`terraintype`) — 0, season (`season`) — 0
- inferred players: **4/4** (from the gold-mine count; Land only)

| Internal pattern type | Replay | Predicted | Ratio |
| --- | ---: | ---: | ---: |
| `plain_small` | 27 | 0 | — |
| `stones` | 24 | 19 | 1.26 |
| `plain_medium` | 17 | 0 | — |
| `mnc` | 16 | 16 | 1.00 |
| `mng` | 16 | 16 | 1.00 |
| `mni` | 16 | 16 | 1.00 |
| `forests_pine_medium` | 14 | 14 | 1.00 |
| `forests_pine_big_2` | 13 | 10 | 1.30 |
| `forests_pine_big` | 12 | 11 | 1.09 |
| `forests_pine_small` | 12 | 12 | 1.00 |
| `mountains` | 11 | 0 | — |
| `swamp_small` | 10 | 0 | — |
| `stoneforests` | 4 | 0 | — |
| `forests_spruce_big` | 3 | 3 | 1.00 |
| `forests_pinefir_big` | 2 | 1 | 2.00 |
| `forests_pinefir_medium` | 2 | 2 | 1.00 |
| `forests_pinefir_small` | 2 | 1 | 2.00 |
| `hills_dark` | 2 | 0 | — |
| `forests_spruce_medium` | 1 | 1 | 1.00 |
| `hills_light` | 1 | 0 | — |
| `plain_big` | 1 | 0 | — |
| `plain_huge` | 1 | 0 | — |
| `plateau_big` | 1 | 0 | — |
| `swamp_medium` | 1 | 0 | — |
| `_n_real_players` | 0 | 4 | 0.00 ⚠ |
| `_spcount` | 0 | 4 | 0.00 ⚠ |

### Replay 13

- mask: `4pl_mask_nowater_172_gauss.tga`
- size (`mapsize`) — 3, relief (`relieftype`) — 3, mines (`resourcemines`) — 1, terrain (`terraintype`) — 0, season (`season`) — 0
- inferred players: **4/4** (from the gold-mine count; Land only)

| Internal pattern type | Replay | Predicted | Ratio |
| --- | ---: | ---: | ---: |
| `plain_small` | 27 | 0 | — |
| `stones` | 23 | 19 | 1.21 |
| `forests_pine_medium` | 16 | 14 | 1.14 |
| `mnc` | 16 | 16 | 1.00 |
| `mng` | 16 | 16 | 1.00 |
| `mni` | 16 | 16 | 1.00 |
| `forests_pine_big_2` | 13 | 10 | 1.30 |
| `plain_medium` | 13 | 0 | — |
| `forests_pine_small` | 12 | 12 | 1.00 |
| `swamp_small` | 12 | 0 | — |
| `forests_pine_big` | 11 | 11 | 1.00 |
| `mountains` | 11 | 0 | — |
| `forests_spruce_big` | 5 | 3 | 1.67 |
| `stoneforests` | 4 | 0 | — |
| `forests_pinefir_medium` | 2 | 2 | 1.00 |
| `hills_dark` | 2 | 0 | — |
| `plain_huge` | 2 | 0 | — |
| `forests_spruce_medium` | 1 | 1 | 1.00 |
| `hills_light` | 1 | 0 | — |
| `plateau` | 1 | 0 | — |
| `plateau_big` | 1 | 0 | — |
| `_n_real_players` | 0 | 4 | 0.00 ⚠ |
| `_spcount` | 0 | 4 | 0.00 ⚠ |
| `forests_pinefir_big` | 0 | 1 | 0.00 ⚠ |
| `forests_pinefir_small` | 0 | 1 | 0.00 ⚠ |

### Replay 05

- mask: `4pl_mask_nowater_174_gauss.tga`
- size (`mapsize`) — 3, relief (`relieftype`) — 3, mines (`resourcemines`) — 2, terrain (`terraintype`) — 0, season (`season`) — 0
- inferred players: **2/4** (from the gold-mine count; Land only)

| Internal pattern type | Replay | Predicted | Ratio |
| --- | ---: | ---: | ---: |
| `plain_small` | 31 | 0 | — |
| `forests_pine_medium` | 20 | 14 | 1.43 |
| `plain_medium` | 19 | 0 | — |
| `stones` | 17 | 19 | 0.89 |
| `forests_pine_small` | 14 | 12 | 1.17 |
| `mnc` | 14 | 14 | 1.00 |
| `mng` | 14 | 14 | 1.00 |
| `mni` | 14 | 14 | 1.00 |
| `mountains` | 13 | 0 | — |
| `forests_pine_big` | 12 | 11 | 1.09 |
| `forests_pine_big_2` | 11 | 10 | 1.10 |
| `swamp_small` | 8 | 0 | — |
| `forests_spruce_big` | 3 | 3 | 1.00 |
| `plain_huge` | 3 | 0 | — |
| `forests_pinefir_small` | 2 | 1 | 2.00 |
| `hills_dark` | 2 | 0 | — |
| `stoneforests` | 2 | 0 | — |
| `forests_pinefir_medium` | 1 | 2 | 0.50 |
| `plateau` | 1 | 0 | — |
| `plateau_big` | 1 | 0 | — |
| `plateau_small` | 1 | 0 | — |
| `_n_real_players` | 0 | 2 | 0.00 ⚠ |
| `_spcount` | 0 | 4 | 0.00 ⚠ |
| `forests_pinefir_big` | 0 | 1 | 0.00 ⚠ |
| `forests_spruce_medium` | 0 | 1 | 0.00 ⚠ |

### Replay 07

- mask: `4pl_mask_nowater_174_gauss.tga`
- size (`mapsize`) — 3, relief (`relieftype`) — 3, mines (`resourcemines`) — 2, terrain (`terraintype`) — 0, season (`season`) — 0
- inferred players: **2/4** (from the gold-mine count; Land only)

| Internal pattern type | Replay | Predicted | Ratio |
| --- | ---: | ---: | ---: |
| `plain_small` | 32 | 0 | — |
| `stones` | 21 | 19 | 1.11 |
| `plain_medium` | 20 | 0 | — |
| `forests_pine_big_2` | 16 | 10 | 1.60 |
| `forests_pine_medium` | 16 | 14 | 1.14 |
| `forests_pine_small` | 14 | 12 | 1.17 |
| `mnc` | 14 | 14 | 1.00 |
| `mng` | 14 | 14 | 1.00 |
| `mni` | 14 | 14 | 1.00 |
| `forests_pine_big` | 13 | 11 | 1.18 |
| `mountains` | 13 | 0 | — |
| `swamp_small` | 12 | 0 | — |
| `forests_pinefir_small` | 2 | 1 | 2.00 |
| `hills_dark` | 2 | 0 | — |
| `hills_light` | 2 | 0 | — |
| `plain_huge` | 2 | 0 | — |
| `stoneforests` | 2 | 0 | — |
| `forests_pinefir_medium` | 1 | 2 | 0.50 |
| `forests_spruce_big` | 1 | 3 | 0.33 ⚠ |
| `plateau_big` | 1 | 0 | — |
| `_n_real_players` | 0 | 2 | 0.00 ⚠ |
| `_spcount` | 0 | 4 | 0.00 ⚠ |
| `forests_pinefir_big` | 0 | 1 | 0.00 ⚠ |
| `forests_spruce_medium` | 0 | 1 | 0.00 ⚠ |

### Replay 25

- mask: `4pl_mask_nowater_174_gauss.tga`
- size (`mapsize`) — 3, relief (`relieftype`) — 3, mines (`resourcemines`) — 1, terrain (`terraintype`) — 0, season (`season`) — 0
- inferred players: **4/4** (from the gold-mine count; Land only)

| Internal pattern type | Replay | Predicted | Ratio |
| --- | ---: | ---: | ---: |
| `plain_small` | 24 | 0 | — |
| `stones` | 23 | 19 | 1.21 |
| `mnc` | 16 | 16 | 1.00 |
| `mng` | 16 | 16 | 1.00 |
| `mni` | 16 | 16 | 1.00 |
| `forests_pine_medium` | 15 | 14 | 1.07 |
| `swamp_small` | 15 | 0 | — |
| `plain_medium` | 14 | 0 | — |
| `forests_pine_big` | 11 | 11 | 1.00 |
| `forests_pine_small` | 10 | 12 | 0.83 |
| `mountains` | 9 | 0 | — |
| `forests_pine_big_2` | 8 | 10 | 0.80 |
| `forests_pinefir_medium` | 4 | 2 | 2.00 |
| `forests_spruce_big` | 4 | 3 | 1.33 |
| `stoneforests` | 4 | 0 | — |
| `forests_pinefir_big` | 2 | 1 | 2.00 |
| `forests_pinefir_small` | 1 | 1 | 1.00 |
| `forests_spruce_medium` | 1 | 1 | 1.00 |
| `hills_dark` | 1 | 0 | — |
| `hills_light` | 1 | 0 | — |
| `plain_big` | 1 | 0 | — |
| `plain_huge` | 1 | 0 | — |
| `plateau_big` | 1 | 0 | — |
| `_n_real_players` | 0 | 4 | 0.00 ⚠ |
| `_spcount` | 0 | 4 | 0.00 ⚠ |

### Replay 15

- mask: `4pl_mask_nowater_176_gauss.tga`
- size (`mapsize`) — 3, relief (`relieftype`) — 3, mines (`resourcemines`) — 2, terrain (`terraintype`) — 0, season (`season`) — 0
- inferred players: **2/4** (from the gold-mine count; Land only)

| Internal pattern type | Replay | Predicted | Ratio |
| --- | ---: | ---: | ---: |
| `plain_small` | 30 | 0 | — |
| `stones` | 22 | 19 | 1.16 |
| `plain_medium` | 19 | 0 | — |
| `forests_pine_medium` | 17 | 14 | 1.21 |
| `forests_pine_small` | 14 | 12 | 1.17 |
| `mnc` | 14 | 14 | 1.00 |
| `mng` | 14 | 14 | 1.00 |
| `mni` | 14 | 14 | 1.00 |
| `forests_pine_big_2` | 12 | 10 | 1.20 |
| `mountains` | 12 | 0 | — |
| `swamp_small` | 12 | 0 | — |
| `forests_pine_big` | 11 | 11 | 1.00 |
| `forests_spruce_big` | 3 | 3 | 1.00 |
| `hills_dark` | 2 | 0 | — |
| `hills_light` | 2 | 0 | — |
| `stoneforests` | 2 | 0 | — |
| `forests_pinefir_big` | 1 | 1 | 1.00 |
| `forests_pinefir_medium` | 1 | 2 | 0.50 |
| `forests_spruce_medium` | 1 | 1 | 1.00 |
| `plain_huge` | 1 | 0 | — |
| `plateau` | 1 | 0 | — |
| `_n_real_players` | 0 | 2 | 0.00 ⚠ |
| `_spcount` | 0 | 4 | 0.00 ⚠ |
| `forests_pinefir_small` | 0 | 1 | 0.00 ⚠ |

### Replay 16

- mask: `4pl_mask_nowater_178_gauss.tga`
- size (`mapsize`) — 3, relief (`relieftype`) — 3, mines (`resourcemines`) — 1, terrain (`terraintype`) — 0, season (`season`) — 0
- inferred players: **4/4** (from the gold-mine count; Land only)

| Internal pattern type | Replay | Predicted | Ratio |
| --- | ---: | ---: | ---: |
| `plain_small` | 25 | 0 | — |
| `stones` | 21 | 19 | 1.11 |
| `mnc` | 16 | 16 | 1.00 |
| `mng` | 16 | 16 | 1.00 |
| `mni` | 16 | 16 | 1.00 |
| `plain_medium` | 14 | 0 | — |
| `forests_pine_medium` | 13 | 14 | 0.93 |
| `swamp_small` | 13 | 0 | — |
| `forests_pine_big_2` | 10 | 10 | 1.00 |
| `forests_pine_small` | 10 | 12 | 0.83 |
| `forests_pine_big` | 9 | 11 | 0.82 |
| `mountains` | 9 | 0 | — |
| `forests_spruce_big` | 5 | 3 | 1.67 |
| `forests_pinefir_big` | 4 | 1 | 4.00 ⚠ |
| `forests_spruce_medium` | 4 | 1 | 4.00 ⚠ |
| `stoneforests` | 4 | 0 | — |
| `forests_pinefir_medium` | 3 | 2 | 1.50 |
| `hills_dark` | 1 | 0 | — |
| `hills_light` | 1 | 0 | — |
| `plain_big` | 1 | 0 | — |
| `plain_huge` | 1 | 0 | — |
| `plateau_big` | 1 | 0 | — |
| `_n_real_players` | 0 | 4 | 0.00 ⚠ |
| `_spcount` | 0 | 4 | 0.00 ⚠ |
| `forests_pinefir_small` | 0 | 1 | 0.00 ⚠ |

### Replay 24

- mask: `4pl_mask_nowater_179_gauss.tga`
- size (`mapsize`) — 3, relief (`relieftype`) — 3, mines (`resourcemines`) — 2, terrain (`terraintype`) — 0, season (`season`) — 0
- inferred players: **2/4** (from the gold-mine count; Land only)

| Internal pattern type | Replay | Predicted | Ratio |
| --- | ---: | ---: | ---: |
| `plain_small` | 31 | 0 | — |
| `stones` | 22 | 19 | 1.16 |
| `forests_pine_medium` | 17 | 14 | 1.21 |
| `plain_medium` | 17 | 0 | — |
| `forests_pine_small` | 14 | 12 | 1.17 |
| `mnc` | 14 | 14 | 1.00 |
| `mng` | 14 | 14 | 1.00 |
| `mni` | 14 | 14 | 1.00 |
| `forests_pine_big` | 13 | 11 | 1.18 |
| `mountains` | 13 | 0 | — |
| `forests_pine_big_2` | 11 | 10 | 1.10 |
| `swamp_small` | 9 | 0 | — |
| `forests_spruce_big` | 3 | 3 | 1.00 |
| `plain_huge` | 3 | 0 | — |
| `hills_dark` | 2 | 0 | — |
| `stoneforests` | 2 | 0 | — |
| `forests_pinefir_big` | 1 | 1 | 1.00 |
| `forests_pinefir_medium` | 1 | 2 | 0.50 |
| `forests_pinefir_small` | 1 | 1 | 1.00 |
| `hills_light` | 1 | 0 | — |
| `plateau` | 1 | 0 | — |
| `_n_real_players` | 0 | 2 | 0.00 ⚠ |
| `_spcount` | 0 | 4 | 0.00 ⚠ |
| `forests_spruce_medium` | 0 | 1 | 0.00 ⚠ |

### Replay 22

- mask: `4pl_mask_nowater_181_gauss.tga`
- size (`mapsize`) — 3, relief (`relieftype`) — 3, mines (`resourcemines`) — 1, terrain (`terraintype`) — 0, season (`season`) — 0
- inferred players: **4/4** (from the gold-mine count; Land only)

| Internal pattern type | Replay | Predicted | Ratio |
| --- | ---: | ---: | ---: |
| `plain_small` | 26 | 0 | — |
| `stones` | 26 | 19 | 1.37 |
| `forests_pine_medium` | 16 | 14 | 1.14 |
| `mnc` | 16 | 16 | 1.00 |
| `mng` | 16 | 16 | 1.00 |
| `mni` | 16 | 16 | 1.00 |
| `plain_medium` | 15 | 0 | — |
| `forests_pine_big` | 12 | 11 | 1.09 |
| `forests_pine_big_2` | 12 | 10 | 1.20 |
| `forests_pine_small` | 12 | 12 | 1.00 |
| `swamp_small` | 12 | 0 | — |
| `mountains` | 11 | 0 | — |
| `forests_spruce_big` | 7 | 3 | 2.33 ⚠ |
| `stoneforests` | 4 | 0 | — |
| `hills_dark` | 2 | 0 | — |
| `hills_light` | 2 | 0 | — |
| `decor_big` | 1 | 0 | — |
| `forests_pinefir_small` | 1 | 1 | 1.00 |
| `plain_big` | 1 | 0 | — |
| `plateau` | 1 | 0 | — |
| `_n_real_players` | 0 | 4 | 0.00 ⚠ |
| `_spcount` | 0 | 4 | 0.00 ⚠ |
| `forests_pinefir_big` | 0 | 1 | 0.00 ⚠ |
| `forests_pinefir_medium` | 0 | 2 | 0.00 ⚠ |
| `forests_spruce_medium` | 0 | 1 | 0.00 ⚠ |

### Replay 01

- mask: `4pl_mask_nowater_181_gauss.tga`
- size (`mapsize`) — 3, relief (`relieftype`) — 3, mines (`resourcemines`) — 2, terrain (`terraintype`) — 0, season (`season`) — 0
- inferred players: **2/4** (from the gold-mine count; Land only)

| Internal pattern type | Replay | Predicted | Ratio |
| --- | ---: | ---: | ---: |
| `plain_small` | 30 | 0 | — |
| `plain_medium` | 18 | 0 | — |
| `stones` | 16 | 19 | 0.84 |
| `forests_pine_medium` | 15 | 14 | 1.07 |
| `forests_pine_big` | 14 | 11 | 1.27 |
| `forests_pine_small` | 14 | 12 | 1.17 |
| `mnc` | 14 | 14 | 1.00 |
| `mng` | 14 | 14 | 1.00 |
| `mni` | 14 | 14 | 1.00 |
| `mountains` | 13 | 0 | — |
| `swamp_small` | 11 | 0 | — |
| `forests_pine_big_2` | 8 | 10 | 0.80 |
| `plain_huge` | 3 | 0 | — |
| `forests_spruce_big` | 2 | 3 | 0.67 |
| `hills_dark` | 2 | 0 | — |
| `plateau_big` | 2 | 0 | — |
| `stoneforests` | 2 | 0 | — |
| `forests_pinefir_big` | 1 | 1 | 1.00 |
| `forests_pinefir_medium` | 1 | 2 | 0.50 |
| `forests_spruce_medium` | 1 | 1 | 1.00 |
| `plain_big` | 1 | 0 | — |
| `_n_real_players` | 0 | 2 | 0.00 ⚠ |
| `_spcount` | 0 | 4 | 0.00 ⚠ |
| `forests_pinefir_small` | 0 | 1 | 0.00 ⚠ |

### Replay 08

- mask: `4pl_mask_nowater_181_gauss.tga`
- size (`mapsize`) — 3, relief (`relieftype`) — 3, mines (`resourcemines`) — 2, terrain (`terraintype`) — 0, season (`season`) — 0
- inferred players: **3/4** (from the gold-mine count; Land only)

| Internal pattern type | Replay | Predicted | Ratio |
| --- | ---: | ---: | ---: |
| `mnc` | 15 | 15 | 1.00 |
| `mng` | 15 | 15 | 1.00 |
| `mni` | 15 | 15 | 1.00 |
| `_n_real_players` | 0 | 3 | 0.00 ⚠ |
| `_spcount` | 0 | 4 | 0.00 ⚠ |
| `forests_pine_big` | 0 | 11 | 0.00 ⚠ |
| `forests_pine_big_2` | 0 | 10 | 0.00 ⚠ |
| `forests_pine_medium` | 0 | 14 | 0.00 ⚠ |
| `forests_pine_small` | 0 | 12 | 0.00 ⚠ |
| `forests_pinefir_big` | 0 | 1 | 0.00 ⚠ |
| `forests_pinefir_medium` | 0 | 2 | 0.00 ⚠ |
| `forests_pinefir_small` | 0 | 1 | 0.00 ⚠ |
| `forests_spruce_big` | 0 | 3 | 0.00 ⚠ |
| `forests_spruce_medium` | 0 | 1 | 0.00 ⚠ |
| `stones` | 0 | 19 | 0.00 ⚠ |

### Replay 02

- mask: `4pl_mask_nowater_181_gauss.tga`
- size (`mapsize`) — 3, relief (`relieftype`) — 3, mines (`resourcemines`) — 2, terrain (`terraintype`) — 0, season (`season`) — 0
- inferred players: **2/4** (from the gold-mine count; Land only)

| Internal pattern type | Replay | Predicted | Ratio |
| --- | ---: | ---: | ---: |
| `plain_small` | 31 | 0 | — |
| `stones` | 24 | 19 | 1.26 |
| `plain_medium` | 18 | 0 | — |
| `forests_pine_medium` | 16 | 14 | 1.14 |
| `mnc` | 14 | 14 | 1.00 |
| `mng` | 14 | 14 | 1.00 |
| `mni` | 14 | 14 | 1.00 |
| `forests_pine_big` | 13 | 11 | 1.18 |
| `forests_pine_small` | 13 | 12 | 1.08 |
| `forests_pine_big_2` | 12 | 10 | 1.20 |
| `mountains` | 12 | 0 | — |
| `swamp_small` | 10 | 0 | — |
| `forests_pinefir_medium` | 3 | 2 | 1.50 |
| `forests_pinefir_big` | 2 | 1 | 2.00 |
| `forests_spruce_big` | 2 | 3 | 0.67 |
| `hills_dark` | 2 | 0 | — |
| `plain_huge` | 2 | 0 | — |
| `stoneforests` | 2 | 0 | — |
| `forests_pinefir_small` | 1 | 1 | 1.00 |
| `hills_light` | 1 | 0 | — |
| `plain_big` | 1 | 0 | — |
| `plateau_big` | 1 | 0 | — |
| `_n_real_players` | 0 | 2 | 0.00 ⚠ |
| `_spcount` | 0 | 4 | 0.00 ⚠ |
| `forests_spruce_medium` | 0 | 1 | 0.00 ⚠ |

### Replay 04

- mask: `2pl_mask_continent_27_gauss.tga`
- size (`mapsize`) — 3, relief (`relieftype`) — 3, mines (`resourcemines`) — 2, terrain (`terraintype`) — 5, season (`season`) — 0
- inferred players: **2/2** (from the gold-mine count; Land only)

| Internal pattern type | Replay | Predicted | Ratio |
| --- | ---: | ---: | ---: |
| `plain_small` | 12 | 0 | — |
| `stones` | 9 | 19 | 0.47 ⚠ |
| `mnc` | 8 | 8 | 1.00 |
| `mng` | 8 | 8 | 1.00 |
| `mni` | 8 | 8 | 1.00 |
| `plain_medium` | 8 | 0 | — |
| `forests_pine_big_2` | 7 | 10 | 0.70 |
| `forests_pine_medium` | 7 | 14 | 0.50 |
| `swamp_small` | 7 | 0 | — |
| `forests_pine_small` | 5 | 12 | 0.42 ⚠ |
| `forests_pine_big` | 4 | 11 | 0.36 ⚠ |
| `mountains` | 4 | 0 | — |
| `forests_spruce_big` | 3 | 3 | 1.00 |
| `stoneforests` | 2 | 0 | — |
| `forests_pinefir_medium` | 1 | 2 | 0.50 |
| `hills_dark` | 1 | 0 | — |
| `plateau` | 1 | 0 | — |
| `plateau_big` | 1 | 0 | — |
| `_n_real_players` | 0 | 2 | 0.00 ⚠ |
| `_spcount` | 0 | 2 | 0.00 ⚠ |
| `forests_pinefir_big` | 0 | 1 | 0.00 ⚠ |
| `forests_pinefir_small` | 0 | 1 | 0.00 ⚠ |
| `forests_spruce_medium` | 0 | 1 | 0.00 ⚠ |

### Replay 14

- mask: `2pl_mask_lakes_27_gauss.tga`
- size (`mapsize`) — 3, relief (`relieftype`) — 3, mines (`resourcemines`) — 2, terrain (`terraintype`) — 7, season (`season`) — 3
- inferred players: **2/2** (from the gold-mine count; Land only)

| Internal pattern type | Replay | Predicted | Ratio |
| --- | ---: | ---: | ---: |
| `desert_stones` | 29 | 0 | — |
| `desert_forests_medium` | 24 | 0 | — |
| `desert_lake` | 15 | 0 | — |
| `desert_forests_small` | 11 | 0 | — |
| `desert_mnc` | 8 | 0 | — |
| `desert_mng` | 8 | 0 | — |
| `desert_mni` | 8 | 0 | — |
| `desert_mountains` | 8 | 0 | — |
| `desert_plain_small` | 5 | 0 | — |
| `desert_plain_big` | 3 | 0 | — |
| `desert_forests_unique` | 2 | 0 | — |
| `_n_real_players` | 0 | 2 | 0.00 ⚠ |
| `_spcount` | 0 | 2 | 0.00 ⚠ |
| `forests_pine_big` | 0 | 11 | 0.00 ⚠ |
| `forests_pine_big_2` | 0 | 10 | 0.00 ⚠ |
| `forests_pine_medium` | 0 | 14 | 0.00 ⚠ |
| `forests_pine_small` | 0 | 12 | 0.00 ⚠ |
| `forests_pinefir_big` | 0 | 1 | 0.00 ⚠ |
| `forests_pinefir_medium` | 0 | 2 | 0.00 ⚠ |
| `forests_pinefir_small` | 0 | 1 | 0.00 ⚠ |
| `forests_spruce_big` | 0 | 3 | 0.00 ⚠ |
| `forests_spruce_medium` | 0 | 1 | 0.00 ⚠ |
| `mnc` | 0 | 8 | 0.00 ⚠ |
| `mng` | 0 | 8 | 0.00 ⚠ |
| `mni` | 0 | 8 | 0.00 ⚠ |
| `stones` | 0 | 19 | 0.00 ⚠ |

### Replay 19

- mask: `4pl_mask_nowater_180_gauss.tga`
- size (`mapsize`) — 3, relief (`relieftype`) — 5, mines (`resourcemines`) — 2, terrain (`terraintype`) — 0, season (`season`) — 0
- inferred players: **4/4** (from the gold-mine count; Land only)

| Internal pattern type | Replay | Predicted | Ratio |
| --- | ---: | ---: | ---: |
| `plain_small` | 24 | 0 | — |
| `stones` | 18 | 19 | 0.95 |
| `mnc` | 16 | 16 | 1.00 |
| `mng` | 16 | 16 | 1.00 |
| `mni` | 16 | 16 | 1.00 |
| `forests_pine_medium` | 11 | 14 | 0.79 |
| `forests_pine_small` | 11 | 12 | 0.92 |
| `swamp_small` | 11 | 0 | — |
| `forests_pine_big` | 10 | 11 | 0.91 |
| `plain_medium` | 10 | 0 | — |
| `forests_pine_big_2` | 9 | 10 | 0.90 |
| `forests_spruce_big` | 7 | 3 | 2.33 ⚠ |
| `stoneforests` | 4 | 0 | — |
| `forests_pinefir_big` | 3 | 1 | 3.00 ⚠ |
| `forests_spruce_medium` | 2 | 1 | 2.00 |
| `mountains` | 2 | 0 | — |
| `plain_huge` | 2 | 0 | — |
| `plateau_big` | 2 | 0 | — |
| `forests_pinefir_medium` | 1 | 2 | 0.50 |
| `hills_dark` | 1 | 0 | — |
| `hills_light` | 1 | 0 | — |
| `plateau` | 1 | 0 | — |
| `_n_real_players` | 0 | 4 | 0.00 ⚠ |
| `_spcount` | 0 | 4 | 0.00 ⚠ |
| `forests_pinefir_small` | 0 | 1 | 0.00 ⚠ |

### Replay 20

- mask: `4pl_mask_continent_73_gauss.tga`
- size (`mapsize`) — 3, relief (`relieftype`) — 5, mines (`resourcemines`) — 2, terrain (`terraintype`) — 5, season (`season`) — 0
- inferred players: **4/4** (from the gold-mine count; Land only)

| Internal pattern type | Replay | Predicted | Ratio |
| --- | ---: | ---: | ---: |
| `mng` | 14 | 16 | 0.88 |
| `mni` | 13 | 16 | 0.81 |
| `mnc` | 11 | 16 | 0.69 |
| `stones` | 7 | 19 | 0.37 ⚠ |
| `stoneforests` | 3 | 0 | — |
| `forests_pine_medium` | 2 | 14 | 0.14 ⚠ |
| `forests_pinefir_medium` | 2 | 2 | 1.00 |
| `forests_spruce_big` | 2 | 3 | 0.67 |
| `forests_spruce_medium` | 2 | 1 | 2.00 |
| `plain_medium` | 2 | 0 | — |
| `plain_small` | 2 | 0 | — |
| `forests_pine_big_2` | 1 | 10 | 0.10 ⚠ |
| `swamp_small` | 1 | 0 | — |
| `_n_real_players` | 0 | 4 | 0.00 ⚠ |
| `_spcount` | 0 | 4 | 0.00 ⚠ |
| `forests_pine_big` | 0 | 11 | 0.00 ⚠ |
| `forests_pine_small` | 0 | 12 | 0.00 ⚠ |
| `forests_pinefir_big` | 0 | 1 | 0.00 ⚠ |
| `forests_pinefir_small` | 0 | 1 | 0.00 ⚠ |

### Replay 06

- mask: `4pl_mask_continent_89_gauss.tga`
- size (`mapsize`) — 3, relief (`relieftype`) — 5, mines (`resourcemines`) — 2, terrain (`terraintype`) — 5, season (`season`) — 0
- inferred players: **4/4** (from the gold-mine count; Land only)

| Internal pattern type | Replay | Predicted | Ratio |
| --- | ---: | ---: | ---: |
| `mng` | 16 | 16 | 1.00 |
| `mni` | 15 | 16 | 0.94 |
| `mnc` | 13 | 16 | 0.81 |
| `stones` | 6 | 19 | 0.32 ⚠ |
| `stoneforests` | 4 | 0 | — |
| `forests_pine_big` | 2 | 11 | 0.18 ⚠ |
| `forests_spruce_medium` | 2 | 1 | 2.00 |
| `forests_pine_big_2` | 1 | 10 | 0.10 ⚠ |
| `forests_pine_medium` | 1 | 14 | 0.07 ⚠ |
| `forests_pinefir_medium` | 1 | 2 | 0.50 |
| `forests_spruce_big` | 1 | 3 | 0.33 ⚠ |
| `plain_small` | 1 | 0 | — |
| `swamp_small` | 1 | 0 | — |
| `_n_real_players` | 0 | 4 | 0.00 ⚠ |
| `_spcount` | 0 | 4 | 0.00 ⚠ |
| `forests_pine_small` | 0 | 12 | 0.00 ⚠ |
| `forests_pinefir_big` | 0 | 1 | 0.00 ⚠ |
| `forests_pinefir_small` | 0 | 1 | 0.00 ⚠ |
