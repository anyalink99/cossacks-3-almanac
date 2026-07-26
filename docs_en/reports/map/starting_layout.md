# Cossacks 3 - Starting layout

**Derived** file (calculated, not extracted). Considered from `data/scripts/common.inc/dogenerate.inc` and `data/game/var/startingsettings.cfg` script [`compute/compute_starting_layout.py`](../../../compute/compute_starting_layout.py).

## §1. Peasant placement (default mode)

The arrangement is done in `CreateStartPointPeasants` [^1].

- **18 peasants** will spawn in the **6×3** grid (`i div 3`, `i mod 3`)
- Step between peasants: `cUnitR = 0.75` tile
- The grid is centered at the starting point: a total of `(6×0.75) × (3×0.75) = 4.5×2.25` tiles
- Random displacement of each peasant: ±0.125 tiles on both axes
- Originals peasant sid is taken from `gCountry[cid].members[]` for the first unit with `usage = gc_obj_usage_peasant` (for example `peaaus` for Austria, `peaeng` for England, etc.)

**In practice:** at the start you have a pile of 18 peasants occupying approximately `5×3` tiles, which fits into the inner clearing circle `cCircle1` (see §2). Nothing else will spawn there - this is a safe “home” for the first minute.

## §2. Resource spawn rings around the starting point

The arrangement of the rings is done by `SetupStartingResources` [^2].

Around each player’s starting point there are three ellipses (X-radius × Y-radius, tiles):

| Ring | X-radius | Y-radius | What spawns on the border |
| --- | ---: | ---: | --- |
| Inner (`cCircle1`) | 5 | 7 | cleared, resources will NOT spawn (peasants only) |
| Mid (`cCircle2`) | 12 | 15 | 1× stoneforests + 1× stones at the inner border |
| — _between mid+4 and outer_ | — | — | additional 2× forests + 1× stones |
| Outer (`cCircle3`) | 22 | 18 | 1× forest at the border (then the mask is filled) |

**Spawn algorithm** (`for [MAIN]i:=0 to 127 do begin … VectorRotateY(px, …, angle); _misc_CheckStandPattern… end`): in each “ring” - 128 attempts × 3 sub-attempts to find a valid position for the selected pattern. Angle `angle` - `RandomExt × 360°`. The distance from the center is `mindst + RandomExt × N + (i+j) × 0.5` tile. This means:

- **Inner stoneforest:** distance ~5-8 tiles
- **Inner stones:** distance ~5-8 tiles (separate random angle, maybe on the back side)
- **Mid forests** (×2): distance ~12-18 tiles (mindst=12, +2 random)
- **Mid stones:** distance ~16-22 tiles (mindst=12+4=16, +2 random)
- **Outer forest:** distance ~22-28 tiles

The forest type is determined by the `foreststype` parameter in the map generation settings: 0 = pinefir/spruce/pine (coniferous, 7 options), 1 = leaf (deciduous), 2 = mixed. In desert maps, `desert_forests_*` patterns are used instead of forests.

Mines (gold / iron / coal) - separate function `SetupMines` [^3]. Mine spawning follows a different logic (in rounds according to distance, see [recon/world/economy/peasant_extraction.md](../../recon/world/economy/peasant_extraction.md) §8.3 + [recon/world/map/map_generation_pipeline.md](../../recon/world/map/map_generation_pipeline.md) §8).

## §3. Starting unit presets

Preset source - `data/game/var/startingsettings.cfg` + enum `gc_mapsettings_startingunits_*` [^4]. All 14 presets with canonical Russian names - [`lobby_settings.md`](lobby_settings.md). Engine behavior (how units and resources are added) - [`recon/world/map/game_settings.md`](../../recon/world/map/game_settings.md) §3.1.

The player selects one of these modes in the lobby. **default** (id=0) is what is described in §1 (just 18 peasants, no additional resources or units). The remaining modes add resources and/or additional units + buildings (through complex ASCII masks in the cfg file).

**Summary of startid → preset → starting resources (on top of default):**
| startid | preset | dataversion | +F | +W | +S | +G | +I | +C |
| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| -1 | (template - not selectable) | — | 0 | 0 | 0 | 0 | 0 | 0 |
| 0 | default | — | 0 | 0 | 0 | 0 | 0 | 0 |
| 1 | armysmall | 60…1000 | 1000 | 0 | 0 | 0 | 0 | 0 |
| 1 | armysmall | 0…59 | 1000 | 0 | 0 | 0 | 0 | 0 |
| 2 | armymedium | 60…1000 | 20000 | 0 | 0 | 0 | 0 | 0 |
| 2 | armymedium | 0…59 | 20000 | 0 | 0 | 0 | 0 | 0 |
| 3 | armylarge | 60…1000 | 20000 | 0 | 0 | 0 | 6000 | 9000 |
| 3 | armylarge | 0…59 | 20000 | 0 | 0 | 0 | 6000 | 9000 |
| 4 | peasantslot | 60…1000 | 20000 | 0 | 0 | 0 | 6000 | 9000 |
| 4 | peasantslot | 0…59 | 20000 | 0 | 0 | 0 | 6000 | 9000 |
| 5 | differentnations | — | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 |
| 6 | towers | — | 20000 | 0 | 0 | 0 | 6000 | 9000 |
| 7 | cannons | — | 20000 | 0 | 0 | 1000 | 6000 | 9000 |
| 8 | cannonsandhowitzers | — | 20000 | 0 | 0 | 1000 | 6000 | 9000 |
| 9 | barrack18 | — | 65000 | 2000 | 2000 | 15000 | 6000 | 9000 |
| 10 | barrack17 | — | 5000 | 1000 | 1000 | 2500 | 3000 | 3000 |
| 11 | village | — | 1000 | 1000 | 1000 | 1000 | 2500 | 2500 |
| 12 | logcabins | — | 0 | 0 | 0 | 0 | 2500 | 2500 |
| 13 | union | — | 1000 | 0 | 0 | 0 | 0 | 0 |

**Notes:**
- Resources are an **increase** to the standard starting 0/0/0/0/0/0. Players start with exactly these numbers on the counters.
- `dataversion` indicates the range of engine versions in which this entry is active. Old entries (`dataversion 0…59`) have been retained for compatibility with replays. For the current version, entries with `dataversionmin ≥ 60` are used.
- In addition to resources, each non-default preset spawns **additional buildings and units** through ASCII masks (`mask : struct.begin`), which are not parsed here (too variable among nations). Open `startingsettings.cfg` in its entirety if you need exact locations.
- `legends : struct.begin` under each `allowedcountries` is a dictionary of mask characters (`X = peasant`, `O = officer17`, `B = drummer17`, `P = polish unit`, etc.). The specific sid of the unit is taken via `role` (= gc_ai_unit_*) or explicit `basename`.

---

Generated from game files. For regeneration:
```
python compute/compute_starting_layout.py
```
## Sources

All links are relative to `data/scripts/` in the Cossacks 3 installation.

[^1]: `CreateStartPointPeasants` - arrangement of 18 peasants 6x3 - `common.inc/dogenerate.inc:1231-1281`.

[^2]: `SetupStartingResources` + `cCircle*Mask` constants - `common.inc/dogenerate.inc:407-414, 720-978`.

[^3]: `SetupMines` - placement of deposits - `common.inc/dogenerate.inc:985`.

[^4]: enum `gc_mapsettings_startingunits_*` - `dmscript.global:1032-1045`.
