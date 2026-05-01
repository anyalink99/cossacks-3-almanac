# Map predictions vs replay ground truth

Сравнение модели `compute_map_resources.compute_counts(...)` с фактическими cluster counts из replay / save файлов (`docs/derived/replay_ground_truth.json`). Расшифровка значений `mapsize` / `relieftype` / `terraintype` / `season` — [`lobby_settings.md`](lobby_settings.md).

**Replays processed:** 20

## Buckets

Replays сгруппированы по `(mapsize, relieftype, terraintype, mask_kind)` — **только внутри одного bucket** калибровка имеет смысл (там одинаковые predictions). Cross-bucket averages могут оказаться ratio≈1.0 чисто случайно (Tiny занижено, Huge завышено — кросс-сумма ~ правде).

| msz | rel | tt | mask | n_replays |
| --- | --- | --- | --- | ---: |
| 3 | 3 | 0 | `4pl_nowater` | 10 |
| 0 | 5 (Random) | 5 | `4pl_continent` | 2 |
| 3 | 5 (Random) | 5 | `4pl_continent` | 2 |
| 0 | 5 (Random) | 1 | `4pl_mediterranean` | 1 |
| 2 | 5 (Random) | 2 | `7pl_peninsulas` | 1 |
| 3 | 3 | 7 | `2pl_lakes` | 1 |
| 1 | 3 | 0 | `6pl_nowater` | 1 |
| 2 | 5 (Random) | 9 | `3pl_coastal` | 1 |
| 3 | 5 (Random) | 0 | `4pl_nowater` | 1 |

## Per-type calibration — LARGEST BUCKET (n=10)

Bucket: msz=3 (Tiny=3, Normal=0, Large=1, Huge=2), rel=3 (Highlands=3, Random=5), tt=0 (Land=0), mask=`4pl_nowater`.

| pattern_type | actual avg | predicted avg | ratio | n_replays |
| --- | ---: | ---: | ---: | ---: |
| `plain_small` | 28.9 | 0.0 | — | 9 |
| `stones` | 19.2 | 19.0 | 1.01 | 10 |
| `plain_medium` | 17.1 | 0.0 | — | 9 |
| `mng` | 14.7 | 14.7 | 1.00 | 10 |
| `mnc` | 14.7 | 14.7 | 1.00 | 10 |
| `mni` | 14.7 | 14.7 | 1.00 | 10 |
| `forests_pine_medium` | 14.5 | 14.0 | 1.04 | 10 |
| `mountains` | 11.7 | 0.0 | — | 9 |
| `forests_pine_small` | 11.5 | 12.0 | 0.96 | 10 |
| `swamp_small` | 11.3 | 0.0 | — | 9 |
| `forests_pine_big` | 10.8 | 11.0 | 0.98 | 10 |
| `forests_pine_big_2` | 10.0 | 10.0 | 1.00 | 10 |
| `forests_spruce_big` | 3.0 | 3.0 | 1.00 | 10 |
| `stoneforests` | 2.7 | 0.0 | — | 9 |
| `plain_huge` | 2.0 | 0.0 | — | 8 |
| `hills_dark` | 1.8 | 0.0 | — | 9 |
| `forests_pinefir_medium` | 1.5 | 2.0 | 0.75 | 10 |
| `hills_light` | 1.4 | 0.0 | — | 7 |
| `plateau_big` | 1.2 | 0.0 | — | 6 |
| `forests_pinefir_big` | 1.1 | 1.0 | 1.10 | 10 |
| `plain_big` | 1.0 | 0.0 | — | 5 |
| `plateau` | 1.0 | 0.0 | — | 4 |
| `plateau_small` | 1.0 | 0.0 | — | 1 |
| `decor_big` | 1.0 | 0.0 | — | 1 |
| `forests_pinefir_small` | 0.8 | 1.0 | 0.80 | 10 |
| `forests_spruce_medium` | 0.7 | 1.0 | 0.70 | 10 |

## Per-pattern-type calibration — MIXED (all replays)

⚠ Усреднение через разные mapsizes/reliefs. Может маскировать per-setting bias. См. bucket выше.

| pattern_type | actual avg | predicted avg | ratio | n_replays |
| --- | ---: | ---: | ---: | ---: |
| `plain_small` | 57.6 | 0.0 | — | 18 |
| `mountains` | 30.7 | 0.0 | — | 15 |
| `forests_pine_small` | 29.3 | 33.7 | 0.87 | 20 |
| `desert_stones` | 29.0 | 0.0 | — | 1 |
| `forests_pine_medium` | 24.8 | 40.4 | 0.61 | 20 |
| `plain_medium` | 24.6 | 0.0 | — | 17 |
| `desert_forests_medium` | 24.0 | 0.0 | — | 1 |
| `stones` | 23.1 | 54.3 | 0.43 | 20 |
| `forests_pine_big` | 20.9 | 30.6 | 0.68 | 20 |
| `mng` | 15.0 | 16.7 | 0.90 | 20 |
| `desert_lake` | 15.0 | 0.0 | — | 1 |
| `mni` | 14.8 | 16.7 | 0.89 | 20 |
| `mnc` | 14.7 | 16.7 | 0.88 | 20 |
| `desert_forests_small` | 11.0 | 0.0 | — | 1 |
| `forests_pine_big_2` | 10.8 | 27.9 | 0.39 | 20 |
| `swamp_small` | 10.3 | 0.0 | — | 18 |
| `desert_mng` | 8.0 | 0.0 | — | 1 |
| `desert_mountains` | 8.0 | 0.0 | — | 1 |
| `desert_mnc` | 8.0 | 0.0 | — | 1 |
| `desert_mni` | 8.0 | 0.0 | — | 1 |
| `desert_plain_small` | 5.0 | 0.0 | — | 1 |
| `forests_spruce_big` | 4.2 | 7.7 | 0.55 | 20 |
| `hills_dark` | 3.4 | 0.0 | — | 14 |
| `stoneforests` | 3.3 | 0.0 | — | 18 |
| `desert_plain_big` | 3.0 | 0.0 | — | 1 |
| `plain_huge` | 2.0 | 0.0 | — | 12 |
| `desert_forests_unique` | 2.0 | 0.0 | — | 1 |
| `plain_big` | 1.9 | 0.0 | — | 9 |
| `forests_pinefir_medium` | 1.4 | 5.0 | 0.29 | 20 |
| `plateau_big` | 1.4 | 0.0 | — | 8 |
| `hills_light` | 1.4 | 0.0 | — | 11 |
| `forests_pinefir_big` | 1.2 | 2.7 | 0.46 | 20 |
| `forests_spruce_medium` | 1.2 | 2.2 | 0.55 | 20 |
| `plateau` | 1.1 | 0.0 | — | 7 |
| `plateau_small` | 1.0 | 0.0 | — | 1 |
| `swamp_medium` | 1.0 | 0.0 | — | 1 |
| `decor_big` | 1.0 | 0.0 | — | 1 |
| `forests_pinefir_small` | 0.6 | 1.9 | 0.31 | 20 |

## Per-replay detail

Для каждой replay-выборки: settings + diff таблица. Pattern types с большими расхождениями отмечены ⚠. Имена опаковые (`Replay NN` назначены детерминированно по хешу содержимого — см. `parse_replay_aggregates.py`).

### Replay 08

- mask: `4pl_mask_mediterranean_87_gauss.tga`
- mapsize=0, relief=5, mines=2, terraintype=1, season=0
- inferred players: **4/4** (from mng count, Land only)

| pattern_type | actual | predicted | actual/pred |
| --- | ---: | ---: | ---: |
| `plain_small` | 39 | 0 | — |
| `stones` | 22 | 38 | 0.58 |
| `forests_pine_medium` | 21 | 28 | 0.75 |
| `plain_medium` | 18 | 0 | — |
| `forests_pine_small` | 18 | 22 | 0.82 |
| `mng` | 15 | 20 | 0.75 |
| `forests_pine_big` | 15 | 21 | 0.71 |
| `mnc` | 15 | 20 | 0.75 |
| `mni` | 15 | 20 | 0.75 |
| `swamp_small` | 13 | 0 | — |
| `forests_pine_big_2` | 10 | 19 | 0.53 |
| `plain_huge` | 4 | 0 | — |
| `forests_spruce_big` | 4 | 5 | 0.80 |
| `mountains` | 4 | 0 | — |
| `stoneforests` | 3 | 0 | — |
| `forests_spruce_medium` | 3 | 1 | 3.00 ⚠ |
| `plain_big` | 3 | 0 | — |
| `plateau_big` | 2 | 0 | — |
| `plateau` | 2 | 0 | — |
| `hills_light` | 2 | 0 | — |
| `hills_dark` | 2 | 0 | — |
| `forests_pinefir_big` | 1 | 2 | 0.50 |
| `_n_real_players` | 0 | 4 | 0.00 ⚠ |
| `forests_pinefir_small` | 0 | 1 | 0.00 ⚠ |
| `_spcount` | 0 | 4 | 0.00 ⚠ |
| `forests_pinefir_medium` | 0 | 3 | 0.00 ⚠ |

### Replay 03

- mask: `4pl_mask_continent_43_gauss.tga`
- mapsize=0, relief=5, mines=2, terraintype=5, season=0
- inferred players: **4/4** (from mng count, Land only)

| pattern_type | actual | predicted | actual/pred |
| --- | ---: | ---: | ---: |
| `mng` | 16 | 20 | 0.80 |
| `mnc` | 16 | 20 | 0.80 |
| `mni` | 16 | 20 | 0.80 |
| `stones` | 11 | 38 | 0.29 ⚠ |
| `forests_pine_big_2` | 5 | 19 | 0.26 ⚠ |
| `stoneforests` | 4 | 0 | — |
| `plain_small` | 4 | 0 | — |
| `swamp_small` | 3 | 0 | — |
| `forests_pinefir_big` | 2 | 2 | 1.00 |
| `plain_medium` | 2 | 0 | — |
| `forests_pine_medium` | 2 | 28 | 0.07 ⚠ |
| `forests_spruce_medium` | 2 | 1 | 2.00 |
| `forests_pine_big` | 1 | 21 | 0.05 ⚠ |
| `forests_spruce_big` | 1 | 5 | 0.20 ⚠ |
| `forests_pine_small` | 1 | 22 | 0.05 ⚠ |
| `forests_pinefir_medium` | 1 | 3 | 0.33 ⚠ |
| `_n_real_players` | 0 | 4 | 0.00 ⚠ |
| `forests_pinefir_small` | 0 | 1 | 0.00 ⚠ |
| `_spcount` | 0 | 4 | 0.00 ⚠ |

### Replay 09

- mask: `4pl_mask_continent_82_gauss.tga`
- mapsize=0, relief=5, mines=2, terraintype=5, season=0
- inferred players: **4/4** (from mng count, Land only)

| pattern_type | actual | predicted | actual/pred |
| --- | ---: | ---: | ---: |
| `mng` | 16 | 20 | 0.80 |
| `mnc` | 15 | 20 | 0.75 |
| `mni` | 15 | 20 | 0.75 |
| `stones` | 12 | 38 | 0.32 ⚠ |
| `plain_small` | 9 | 0 | — |
| `swamp_small` | 8 | 0 | — |
| `forests_pine_medium` | 6 | 28 | 0.21 ⚠ |
| `forests_pine_big_2` | 5 | 19 | 0.26 ⚠ |
| `forests_pine_big` | 5 | 21 | 0.24 ⚠ |
| `plain_medium` | 3 | 0 | — |
| `stoneforests` | 3 | 0 | — |
| `forests_pine_small` | 3 | 22 | 0.14 ⚠ |
| `forests_spruce_big` | 2 | 5 | 0.40 ⚠ |
| `forests_pinefir_medium` | 1 | 3 | 0.33 ⚠ |
| `forests_spruce_medium` | 1 | 1 | 1.00 |
| `mountains` | 1 | 0 | — |
| `forests_pinefir_big` | 0 | 2 | 0.00 ⚠ |
| `_n_real_players` | 0 | 4 | 0.00 ⚠ |
| `forests_pinefir_small` | 0 | 1 | 0.00 ⚠ |
| `_spcount` | 0 | 4 | 0.00 ⚠ |

### Replay 14

- mask: `6pl_mask_nowater_5_gauss.tga`
- mapsize=1, relief=3, mines=1, terraintype=0, season=0
- inferred players: **6/6** (from mng count, Land only)

| pattern_type | actual | predicted | actual/pred |
| --- | ---: | ---: | ---: |
| `plain_small` | 143 | 0 | — |
| `forests_pine_small` | 101 | 76 | 1.33 |
| `mountains` | 88 | 0 | — |
| `forests_pine_medium` | 77 | 93 | 0.83 |
| `forests_pine_big` | 66 | 70 | 0.94 |
| `plain_medium` | 52 | 0 | — |
| `stones` | 46 | 126 | 0.37 ⚠ |
| `forests_pine_big_2` | 29 | 64 | 0.45 ⚠ |
| `mng` | 24 | 24 | 1.00 |
| `mnc` | 24 | 24 | 1.00 |
| `mni` | 24 | 24 | 1.00 |
| `swamp_small` | 16 | 0 | — |
| `hills_dark` | 11 | 0 | — |
| `forests_spruce_big` | 8 | 17 | 0.47 ⚠ |
| `stoneforests` | 6 | 0 | — |
| `forests_pinefir_big` | 5 | 6 | 0.83 |
| `plain_big` | 5 | 0 | — |
| `forests_pinefir_medium` | 4 | 11 | 0.36 ⚠ |
| `forests_spruce_medium` | 2 | 5 | 0.40 ⚠ |
| `plain_huge` | 1 | 0 | — |
| `plateau` | 1 | 0 | — |
| `hills_light` | 1 | 0 | — |
| `forests_pinefir_small` | 1 | 4 | 0.25 ⚠ |
| `_spcount` | 0 | 6 | 0.00 ⚠ |
| `_n_real_players` | 0 | 6 | 0.00 ⚠ |

### Replay 10

- mask: `7pl_mask_peninsulas_3_gauss.tga`
- mapsize=2, relief=5, mines=2, terraintype=2, season=0
- inferred players: **7/7** (from mng count, Land only)

| pattern_type | actual | predicted | actual/pred |
| --- | ---: | ---: | ---: |
| `plain_small` | 220 | 0 | — |
| `forests_pine_small` | 117 | 182 | 0.64 |
| `forests_pine_medium` | 98 | 217 | 0.45 ⚠ |
| `mountains` | 87 | 0 | — |
| `plain_medium` | 78 | 0 | — |
| `forests_pine_big` | 77 | 163 | 0.47 ⚠ |
| `stones` | 68 | 290 | 0.23 ⚠ |
| `mng` | 27 | 35 | 0.77 |
| `mnc` | 27 | 35 | 0.77 |
| `mni` | 27 | 35 | 0.77 |
| `forests_pine_big_2` | 22 | 149 | 0.15 ⚠ |
| `swamp_small` | 20 | 0 | — |
| `forests_spruce_big` | 15 | 40 | 0.38 ⚠ |
| `hills_dark` | 8 | 0 | — |
| `stoneforests` | 6 | 0 | — |
| `forests_pinefir_big` | 3 | 14 | 0.21 ⚠ |
| `forests_spruce_medium` | 2 | 11 | 0.18 ⚠ |
| `plain_big` | 2 | 0 | — |
| `forests_pinefir_medium` | 2 | 26 | 0.08 ⚠ |
| `forests_pinefir_small` | 1 | 9 | 0.11 ⚠ |
| `_n_real_players` | 0 | 7 | 0.00 ⚠ |
| `_spcount` | 0 | 7 | 0.00 ⚠ |

### Replay 15

- mask: `3pl_mask_coastal_1_gauss.tga`
- mapsize=2, relief=5, mines=1, terraintype=9, season=0
- inferred players: **3/3** (from mng count, Land only)

| pattern_type | actual | predicted | actual/pred |
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
| `mng` | 9 | 12 | 0.75 |
| `mnc` | 9 | 12 | 0.75 |
| `mni` | 9 | 12 | 0.75 |
| `stoneforests` | 3 | 0 | — |
| `forests_pinefir_small` | 2 | 9 | 0.22 ⚠ |
| `plain_big` | 2 | 0 | — |
| `forests_pinefir_medium` | 2 | 26 | 0.08 ⚠ |
| `plain_huge` | 1 | 0 | — |
| `hills_light` | 1 | 0 | — |
| `swamp_medium` | 1 | 0 | — |
| `forests_spruce_medium` | 1 | 11 | 0.09 ⚠ |
| `forests_pinefir_big` | 0 | 14 | 0.00 ⚠ |
| `_n_real_players` | 0 | 3 | 0.00 ⚠ |
| `_spcount` | 0 | 3 | 0.00 ⚠ |

### Replay 04

- mask: `4pl_mask_nowater_174_gauss.tga`
- mapsize=3, relief=3, mines=2, terraintype=0, season=0
- inferred players: **2/4** (from mng count, Land only)

| pattern_type | actual | predicted | actual/pred |
| --- | ---: | ---: | ---: |
| `plain_small` | 31 | 0 | — |
| `forests_pine_medium` | 20 | 14 | 1.43 |
| `plain_medium` | 19 | 0 | — |
| `stones` | 17 | 19 | 0.89 |
| `mng` | 14 | 14 | 1.00 |
| `forests_pine_small` | 14 | 12 | 1.17 |
| `mnc` | 14 | 14 | 1.00 |
| `mni` | 14 | 14 | 1.00 |
| `mountains` | 13 | 0 | — |
| `forests_pine_big` | 12 | 11 | 1.09 |
| `forests_pine_big_2` | 11 | 10 | 1.10 |
| `swamp_small` | 8 | 0 | — |
| `plain_huge` | 3 | 0 | — |
| `forests_spruce_big` | 3 | 3 | 1.00 |
| `stoneforests` | 2 | 0 | — |
| `forests_pinefir_small` | 2 | 1 | 2.00 |
| `hills_dark` | 2 | 0 | — |
| `plateau_big` | 1 | 0 | — |
| `plateau` | 1 | 0 | — |
| `plateau_small` | 1 | 0 | — |
| `forests_pinefir_medium` | 1 | 2 | 0.50 |
| `forests_pinefir_big` | 0 | 1 | 0.00 ⚠ |
| `_n_real_players` | 0 | 2 | 0.00 ⚠ |
| `_spcount` | 0 | 4 | 0.00 ⚠ |
| `forests_spruce_medium` | 0 | 1 | 0.00 ⚠ |

### Replay 06

- mask: `4pl_mask_nowater_174_gauss.tga`
- mapsize=3, relief=3, mines=2, terraintype=0, season=0
- inferred players: **2/4** (from mng count, Land only)

| pattern_type | actual | predicted | actual/pred |
| --- | ---: | ---: | ---: |
| `plain_small` | 32 | 0 | — |
| `stones` | 21 | 19 | 1.11 |
| `plain_medium` | 20 | 0 | — |
| `forests_pine_big_2` | 16 | 10 | 1.60 |
| `forests_pine_medium` | 16 | 14 | 1.14 |
| `mng` | 14 | 14 | 1.00 |
| `forests_pine_small` | 14 | 12 | 1.17 |
| `mnc` | 14 | 14 | 1.00 |
| `mni` | 14 | 14 | 1.00 |
| `forests_pine_big` | 13 | 11 | 1.18 |
| `mountains` | 13 | 0 | — |
| `swamp_small` | 12 | 0 | — |
| `plain_huge` | 2 | 0 | — |
| `hills_light` | 2 | 0 | — |
| `stoneforests` | 2 | 0 | — |
| `forests_pinefir_small` | 2 | 1 | 2.00 |
| `hills_dark` | 2 | 0 | — |
| `plateau_big` | 1 | 0 | — |
| `forests_spruce_big` | 1 | 3 | 0.33 ⚠ |
| `forests_pinefir_medium` | 1 | 2 | 0.50 |
| `forests_pinefir_big` | 0 | 1 | 0.00 ⚠ |
| `_n_real_players` | 0 | 2 | 0.00 ⚠ |
| `_spcount` | 0 | 4 | 0.00 ⚠ |
| `forests_spruce_medium` | 0 | 1 | 0.00 ⚠ |

### Replay 20

- mask: `4pl_mask_nowater_174_gauss.tga`
- mapsize=3, relief=3, mines=1, terraintype=0, season=0
- inferred players: **4/4** (from mng count, Land only)

| pattern_type | actual | predicted | actual/pred |
| --- | ---: | ---: | ---: |
| `plain_small` | 24 | 0 | — |
| `stones` | 23 | 19 | 1.21 |
| `mng` | 16 | 16 | 1.00 |
| `mnc` | 16 | 16 | 1.00 |
| `mni` | 16 | 16 | 1.00 |
| `swamp_small` | 15 | 0 | — |
| `forests_pine_medium` | 15 | 14 | 1.07 |
| `plain_medium` | 14 | 0 | — |
| `forests_pine_big` | 11 | 11 | 1.00 |
| `forests_pine_small` | 10 | 12 | 0.83 |
| `mountains` | 9 | 0 | — |
| `forests_pine_big_2` | 8 | 10 | 0.80 |
| `stoneforests` | 4 | 0 | — |
| `forests_spruce_big` | 4 | 3 | 1.33 |
| `forests_pinefir_medium` | 4 | 2 | 2.00 |
| `forests_pinefir_big` | 2 | 1 | 2.00 |
| `plain_huge` | 1 | 0 | — |
| `forests_spruce_medium` | 1 | 1 | 1.00 |
| `plateau_big` | 1 | 0 | — |
| `hills_light` | 1 | 0 | — |
| `forests_pinefir_small` | 1 | 1 | 1.00 |
| `plain_big` | 1 | 0 | — |
| `hills_dark` | 1 | 0 | — |
| `_spcount` | 0 | 4 | 0.00 ⚠ |
| `_n_real_players` | 0 | 4 | 0.00 ⚠ |

### Replay 12

- mask: `4pl_mask_nowater_176_gauss.tga`
- mapsize=3, relief=3, mines=2, terraintype=0, season=0
- inferred players: **2/4** (from mng count, Land only)

| pattern_type | actual | predicted | actual/pred |
| --- | ---: | ---: | ---: |
| `plain_small` | 30 | 0 | — |
| `stones` | 22 | 19 | 1.16 |
| `plain_medium` | 19 | 0 | — |
| `forests_pine_medium` | 17 | 14 | 1.21 |
| `mng` | 14 | 14 | 1.00 |
| `forests_pine_small` | 14 | 12 | 1.17 |
| `mnc` | 14 | 14 | 1.00 |
| `mni` | 14 | 14 | 1.00 |
| `forests_pine_big_2` | 12 | 10 | 1.20 |
| `swamp_small` | 12 | 0 | — |
| `mountains` | 12 | 0 | — |
| `forests_pine_big` | 11 | 11 | 1.00 |
| `forests_spruce_big` | 3 | 3 | 1.00 |
| `hills_light` | 2 | 0 | — |
| `stoneforests` | 2 | 0 | — |
| `hills_dark` | 2 | 0 | — |
| `plateau` | 1 | 0 | — |
| `plain_huge` | 1 | 0 | — |
| `forests_pinefir_big` | 1 | 1 | 1.00 |
| `forests_spruce_medium` | 1 | 1 | 1.00 |
| `forests_pinefir_medium` | 1 | 2 | 0.50 |
| `_n_real_players` | 0 | 2 | 0.00 ⚠ |
| `forests_pinefir_small` | 0 | 1 | 0.00 ⚠ |
| `_spcount` | 0 | 4 | 0.00 ⚠ |

### Replay 13

- mask: `4pl_mask_nowater_178_gauss.tga`
- mapsize=3, relief=3, mines=1, terraintype=0, season=0
- inferred players: **4/4** (from mng count, Land only)

| pattern_type | actual | predicted | actual/pred |
| --- | ---: | ---: | ---: |
| `plain_small` | 25 | 0 | — |
| `stones` | 21 | 19 | 1.11 |
| `mng` | 16 | 16 | 1.00 |
| `mnc` | 16 | 16 | 1.00 |
| `mni` | 16 | 16 | 1.00 |
| `plain_medium` | 14 | 0 | — |
| `swamp_small` | 13 | 0 | — |
| `forests_pine_medium` | 13 | 14 | 0.93 |
| `forests_pine_big_2` | 10 | 10 | 1.00 |
| `forests_pine_small` | 10 | 12 | 0.83 |
| `forests_pine_big` | 9 | 11 | 0.82 |
| `mountains` | 9 | 0 | — |
| `forests_spruce_big` | 5 | 3 | 1.67 |
| `forests_pinefir_big` | 4 | 1 | 4.00 ⚠ |
| `stoneforests` | 4 | 0 | — |
| `forests_spruce_medium` | 4 | 1 | 4.00 ⚠ |
| `forests_pinefir_medium` | 3 | 2 | 1.50 |
| `plateau_big` | 1 | 0 | — |
| `hills_light` | 1 | 0 | — |
| `plain_huge` | 1 | 0 | — |
| `plain_big` | 1 | 0 | — |
| `hills_dark` | 1 | 0 | — |
| `_n_real_players` | 0 | 4 | 0.00 ⚠ |
| `forests_pinefir_small` | 0 | 1 | 0.00 ⚠ |
| `_spcount` | 0 | 4 | 0.00 ⚠ |

### Replay 19

- mask: `4pl_mask_nowater_179_gauss.tga`
- mapsize=3, relief=3, mines=2, terraintype=0, season=0
- inferred players: **2/4** (from mng count, Land only)

| pattern_type | actual | predicted | actual/pred |
| --- | ---: | ---: | ---: |
| `plain_small` | 31 | 0 | — |
| `stones` | 22 | 19 | 1.16 |
| `plain_medium` | 17 | 0 | — |
| `forests_pine_medium` | 17 | 14 | 1.21 |
| `mng` | 14 | 14 | 1.00 |
| `forests_pine_small` | 14 | 12 | 1.17 |
| `mnc` | 14 | 14 | 1.00 |
| `mni` | 14 | 14 | 1.00 |
| `forests_pine_big` | 13 | 11 | 1.18 |
| `mountains` | 13 | 0 | — |
| `forests_pine_big_2` | 11 | 10 | 1.10 |
| `swamp_small` | 9 | 0 | — |
| `plain_huge` | 3 | 0 | — |
| `forests_spruce_big` | 3 | 3 | 1.00 |
| `stoneforests` | 2 | 0 | — |
| `hills_dark` | 2 | 0 | — |
| `plateau` | 1 | 0 | — |
| `hills_light` | 1 | 0 | — |
| `forests_pinefir_big` | 1 | 1 | 1.00 |
| `forests_pinefir_small` | 1 | 1 | 1.00 |
| `forests_pinefir_medium` | 1 | 2 | 0.50 |
| `_n_real_players` | 0 | 2 | 0.00 ⚠ |
| `_spcount` | 0 | 4 | 0.00 ⚠ |
| `forests_spruce_medium` | 0 | 1 | 0.00 ⚠ |

### Replay 18

- mask: `4pl_mask_nowater_181_gauss.tga`
- mapsize=3, relief=3, mines=1, terraintype=0, season=0
- inferred players: **4/4** (from mng count, Land only)

| pattern_type | actual | predicted | actual/pred |
| --- | ---: | ---: | ---: |
| `stones` | 26 | 19 | 1.37 |
| `plain_small` | 26 | 0 | — |
| `mng` | 16 | 16 | 1.00 |
| `forests_pine_medium` | 16 | 14 | 1.14 |
| `mnc` | 16 | 16 | 1.00 |
| `mni` | 16 | 16 | 1.00 |
| `plain_medium` | 15 | 0 | — |
| `forests_pine_big_2` | 12 | 10 | 1.20 |
| `forests_pine_big` | 12 | 11 | 1.09 |
| `swamp_small` | 12 | 0 | — |
| `forests_pine_small` | 12 | 12 | 1.00 |
| `mountains` | 11 | 0 | — |
| `forests_spruce_big` | 7 | 3 | 2.33 ⚠ |
| `stoneforests` | 4 | 0 | — |
| `hills_light` | 2 | 0 | — |
| `hills_dark` | 2 | 0 | — |
| `plateau` | 1 | 0 | — |
| `forests_pinefir_small` | 1 | 1 | 1.00 |
| `decor_big` | 1 | 0 | — |
| `plain_big` | 1 | 0 | — |
| `forests_pinefir_big` | 0 | 1 | 0.00 ⚠ |
| `_n_real_players` | 0 | 4 | 0.00 ⚠ |
| `_spcount` | 0 | 4 | 0.00 ⚠ |
| `forests_pinefir_medium` | 0 | 2 | 0.00 ⚠ |
| `forests_spruce_medium` | 0 | 1 | 0.00 ⚠ |

### Replay 01

- mask: `4pl_mask_nowater_181_gauss.tga`
- mapsize=3, relief=3, mines=2, terraintype=0, season=0
- inferred players: **2/4** (from mng count, Land only)

| pattern_type | actual | predicted | actual/pred |
| --- | ---: | ---: | ---: |
| `plain_small` | 30 | 0 | — |
| `plain_medium` | 18 | 0 | — |
| `stones` | 16 | 19 | 0.84 |
| `forests_pine_medium` | 15 | 14 | 1.07 |
| `mng` | 14 | 14 | 1.00 |
| `forests_pine_big` | 14 | 11 | 1.27 |
| `forests_pine_small` | 14 | 12 | 1.17 |
| `mnc` | 14 | 14 | 1.00 |
| `mni` | 14 | 14 | 1.00 |
| `mountains` | 13 | 0 | — |
| `swamp_small` | 11 | 0 | — |
| `forests_pine_big_2` | 8 | 10 | 0.80 |
| `plain_huge` | 3 | 0 | — |
| `plateau_big` | 2 | 0 | — |
| `stoneforests` | 2 | 0 | — |
| `forests_spruce_big` | 2 | 3 | 0.67 |
| `hills_dark` | 2 | 0 | — |
| `forests_pinefir_big` | 1 | 1 | 1.00 |
| `forests_spruce_medium` | 1 | 1 | 1.00 |
| `plain_big` | 1 | 0 | — |
| `forests_pinefir_medium` | 1 | 2 | 0.50 |
| `_n_real_players` | 0 | 2 | 0.00 ⚠ |
| `forests_pinefir_small` | 0 | 1 | 0.00 ⚠ |
| `_spcount` | 0 | 4 | 0.00 ⚠ |

### Replay 07

- mask: `4pl_mask_nowater_181_gauss.tga`
- mapsize=3, relief=3, mines=2, terraintype=0, season=0
- inferred players: **3/4** (from mng count, Land only)

| pattern_type | actual | predicted | actual/pred |
| --- | ---: | ---: | ---: |
| `mng` | 15 | 15 | 1.00 |
| `mnc` | 15 | 15 | 1.00 |
| `mni` | 15 | 15 | 1.00 |
| `forests_pine_big_2` | 0 | 10 | 0.00 ⚠ |
| `forests_pine_big` | 0 | 11 | 0.00 ⚠ |
| `forests_pinefir_big` | 0 | 1 | 0.00 ⚠ |
| `_n_real_players` | 0 | 3 | 0.00 ⚠ |
| `forests_spruce_big` | 0 | 3 | 0.00 ⚠ |
| `forests_pinefir_small` | 0 | 1 | 0.00 ⚠ |
| `stones` | 0 | 19 | 0.00 ⚠ |
| `_spcount` | 0 | 4 | 0.00 ⚠ |
| `forests_pine_small` | 0 | 12 | 0.00 ⚠ |
| `forests_pine_medium` | 0 | 14 | 0.00 ⚠ |
| `forests_spruce_medium` | 0 | 1 | 0.00 ⚠ |
| `forests_pinefir_medium` | 0 | 2 | 0.00 ⚠ |

### Replay 02

- mask: `4pl_mask_nowater_181_gauss.tga`
- mapsize=3, relief=3, mines=2, terraintype=0, season=0
- inferred players: **2/4** (from mng count, Land only)

| pattern_type | actual | predicted | actual/pred |
| --- | ---: | ---: | ---: |
| `plain_small` | 31 | 0 | — |
| `stones` | 24 | 19 | 1.26 |
| `plain_medium` | 18 | 0 | — |
| `forests_pine_medium` | 16 | 14 | 1.14 |
| `mng` | 14 | 14 | 1.00 |
| `mnc` | 14 | 14 | 1.00 |
| `mni` | 14 | 14 | 1.00 |
| `forests_pine_big` | 13 | 11 | 1.18 |
| `forests_pine_small` | 13 | 12 | 1.08 |
| `forests_pine_big_2` | 12 | 10 | 1.20 |
| `mountains` | 12 | 0 | — |
| `swamp_small` | 10 | 0 | — |
| `forests_pinefir_medium` | 3 | 2 | 1.50 |
| `plain_huge` | 2 | 0 | — |
| `forests_pinefir_big` | 2 | 1 | 2.00 |
| `stoneforests` | 2 | 0 | — |
| `forests_spruce_big` | 2 | 3 | 0.67 |
| `hills_dark` | 2 | 0 | — |
| `plateau_big` | 1 | 0 | — |
| `hills_light` | 1 | 0 | — |
| `forests_pinefir_small` | 1 | 1 | 1.00 |
| `plain_big` | 1 | 0 | — |
| `_n_real_players` | 0 | 2 | 0.00 ⚠ |
| `_spcount` | 0 | 4 | 0.00 ⚠ |
| `forests_spruce_medium` | 0 | 1 | 0.00 ⚠ |

### Replay 11

- mask: `2pl_mask_lakes_27_gauss.tga`
- mapsize=3, relief=3, mines=2, terraintype=7, season=3
- inferred players: **2/2** (from mng count, Land only)

| pattern_type | actual | predicted | actual/pred |
| --- | ---: | ---: | ---: |
| `desert_stones` | 29 | 0 | — |
| `desert_forests_medium` | 24 | 0 | — |
| `desert_lake` | 15 | 0 | — |
| `desert_forests_small` | 11 | 0 | — |
| `desert_mng` | 8 | 0 | — |
| `desert_mountains` | 8 | 0 | — |
| `desert_mnc` | 8 | 0 | — |
| `desert_mni` | 8 | 0 | — |
| `desert_plain_small` | 5 | 0 | — |
| `desert_plain_big` | 3 | 0 | — |
| `desert_forests_unique` | 2 | 0 | — |
| `forests_pine_big_2` | 0 | 10 | 0.00 ⚠ |
| `mng` | 0 | 8 | 0.00 ⚠ |
| `forests_pine_big` | 0 | 11 | 0.00 ⚠ |
| `forests_pinefir_big` | 0 | 1 | 0.00 ⚠ |
| `_n_real_players` | 0 | 2 | 0.00 ⚠ |
| `forests_spruce_big` | 0 | 3 | 0.00 ⚠ |
| `forests_pinefir_small` | 0 | 1 | 0.00 ⚠ |
| `stones` | 0 | 19 | 0.00 ⚠ |
| `_spcount` | 0 | 2 | 0.00 ⚠ |
| `forests_pine_small` | 0 | 12 | 0.00 ⚠ |
| `forests_pinefir_medium` | 0 | 2 | 0.00 ⚠ |
| `forests_pine_medium` | 0 | 14 | 0.00 ⚠ |
| `forests_spruce_medium` | 0 | 1 | 0.00 ⚠ |
| `mnc` | 0 | 8 | 0.00 ⚠ |
| `mni` | 0 | 8 | 0.00 ⚠ |

### Replay 16

- mask: `4pl_mask_nowater_180_gauss.tga`
- mapsize=3, relief=5, mines=2, terraintype=0, season=0
- inferred players: **4/4** (from mng count, Land only)

| pattern_type | actual | predicted | actual/pred |
| --- | ---: | ---: | ---: |
| `plain_small` | 24 | 0 | — |
| `stones` | 18 | 19 | 0.95 |
| `mng` | 16 | 16 | 1.00 |
| `mnc` | 16 | 16 | 1.00 |
| `mni` | 16 | 16 | 1.00 |
| `swamp_small` | 11 | 0 | — |
| `forests_pine_small` | 11 | 12 | 0.92 |
| `forests_pine_medium` | 11 | 14 | 0.79 |
| `forests_pine_big` | 10 | 11 | 0.91 |
| `plain_medium` | 10 | 0 | — |
| `forests_pine_big_2` | 9 | 10 | 0.90 |
| `forests_spruce_big` | 7 | 3 | 2.33 ⚠ |
| `stoneforests` | 4 | 0 | — |
| `forests_pinefir_big` | 3 | 1 | 3.00 ⚠ |
| `plateau_big` | 2 | 0 | — |
| `plain_huge` | 2 | 0 | — |
| `mountains` | 2 | 0 | — |
| `forests_spruce_medium` | 2 | 1 | 2.00 |
| `plateau` | 1 | 0 | — |
| `hills_light` | 1 | 0 | — |
| `hills_dark` | 1 | 0 | — |
| `forests_pinefir_medium` | 1 | 2 | 0.50 |
| `_n_real_players` | 0 | 4 | 0.00 ⚠ |
| `forests_pinefir_small` | 0 | 1 | 0.00 ⚠ |
| `_spcount` | 0 | 4 | 0.00 ⚠ |

### Replay 17

- mask: `4pl_mask_continent_73_gauss.tga`
- mapsize=3, relief=5, mines=2, terraintype=5, season=0
- inferred players: **4/4** (from mng count, Land only)

| pattern_type | actual | predicted | actual/pred |
| --- | ---: | ---: | ---: |
| `mng` | 14 | 16 | 0.88 |
| `mni` | 13 | 16 | 0.81 |
| `mnc` | 11 | 16 | 0.69 |
| `stones` | 7 | 19 | 0.37 ⚠ |
| `stoneforests` | 3 | 0 | — |
| `plain_medium` | 2 | 0 | — |
| `forests_spruce_big` | 2 | 3 | 0.67 |
| `forests_pine_medium` | 2 | 14 | 0.14 ⚠ |
| `forests_spruce_medium` | 2 | 1 | 2.00 |
| `plain_small` | 2 | 0 | — |
| `forests_pinefir_medium` | 2 | 2 | 1.00 |
| `forests_pine_big_2` | 1 | 10 | 0.10 ⚠ |
| `swamp_small` | 1 | 0 | — |
| `forests_pine_big` | 0 | 11 | 0.00 ⚠ |
| `forests_pinefir_big` | 0 | 1 | 0.00 ⚠ |
| `_n_real_players` | 0 | 4 | 0.00 ⚠ |
| `forests_pinefir_small` | 0 | 1 | 0.00 ⚠ |
| `_spcount` | 0 | 4 | 0.00 ⚠ |
| `forests_pine_small` | 0 | 12 | 0.00 ⚠ |

### Replay 05

- mask: `4pl_mask_continent_89_gauss.tga`
- mapsize=3, relief=5, mines=2, terraintype=5, season=0
- inferred players: **4/4** (from mng count, Land only)

| pattern_type | actual | predicted | actual/pred |
| --- | ---: | ---: | ---: |
| `mng` | 16 | 16 | 1.00 |
| `mni` | 15 | 16 | 0.94 |
| `mnc` | 13 | 16 | 0.81 |
| `stones` | 6 | 19 | 0.32 ⚠ |
| `stoneforests` | 4 | 0 | — |
| `forests_pine_big` | 2 | 11 | 0.18 ⚠ |
| `forests_spruce_medium` | 2 | 1 | 2.00 |
| `forests_pine_big_2` | 1 | 10 | 0.10 ⚠ |
| `swamp_small` | 1 | 0 | — |
| `forests_spruce_big` | 1 | 3 | 0.33 ⚠ |
| `forests_pine_medium` | 1 | 14 | 0.07 ⚠ |
| `plain_small` | 1 | 0 | — |
| `forests_pinefir_medium` | 1 | 2 | 0.50 |
| `forests_pinefir_big` | 0 | 1 | 0.00 ⚠ |
| `_n_real_players` | 0 | 4 | 0.00 ⚠ |
| `forests_pinefir_small` | 0 | 1 | 0.00 ⚠ |
| `_spcount` | 0 | 4 | 0.00 ⚠ |
| `forests_pine_small` | 0 | 12 | 0.00 ⚠ |
