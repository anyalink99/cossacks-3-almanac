<a id="машинно-читаемые-json-датасеты"></a>
# Machine-readable JSON datasets

**English** · [Русский](README.md)

Here are all the JSON files for the tools: build editor, simulator,
external analyzers, as well as engine-RE dumps from `cossacks.exe`. All
are generated. **Do not edit manually** - will be overwritten when
next regeneration.

<a id="игровые-данные-потребляются-writerами--редактором--симулятором"></a>
## Game data (consumed by writers/editor/simulator)

| File | What's inside | From |
|---|---|---|
| [`canonical_terms.json`](canonical_terms.json) | Canonical Russian names from the game locale: 21 nations, 22 buildings, 7 types of weapons, 5 difficulty levels, 79 lobby settings, 9 types of officer training, 75 upgrades, 148 units, 6 resources. **Single source of truth** for all writers and compute scripts. | [`parser/build_canonical_terms.py`](../parser/build_canonical_terms.py) |
| [`replay_upgrades.json`](replay_upgrades.json) | A compact directory of improvements for replay-parser, organized by nation. Stores only `sid`, Russian/English name and research building, so that the browser does not load the full `data.json`. | [`parser/build_replay_upgrades.py`](../parser/build_replay_upgrades.py) |
| [`game_settings.json`](game_settings.json) | All lobby options (`mapsize`, `terraintype`, `relieftype`, `peacetime`, `gamespeed`, etc.) - 95 values in 18 categories, with English and Russian labels + default values from `initmap.inc`. Used by the browser editor to build dropdowns. | [`compute/compute_game_settings.py`](../compute/compute_game_settings.py) |
| [`tech_tree.json`](tech_tree.json) | Dependency graph of buildings, units and upgrades: for each `sid` - a list of prereqs with types (`[B]` building, `[U]` unit, `[T]` upgrade) + base price and time. Used by the economic simulator and editor. | [`parser/build_tech_graph.py`](../parser/build_tech_graph.py) |
| [`builder_slots.json`](builder_slots.json) | How many peasants can build each building at the same time? It is considered to bypass the perimeter of the collision mask with step `gc_BuilderDist = 1.0`. Used in [`docs/reports/economy/builder_slots.md`](../docs_en/reports/economy/builder_slots.md) and in the editor. | [`compute/compute_builder_slots.py`](../compute/compute_builder_slots.py) |
| [`animations.json`](animations.json) | Animation frame base for each unit: `{sid: {anim_name: [start_frame, end_frame]}, ...}` - extracted from `<game>/data/animations/aaf/*.aaf`. Length of one frame = 1/32 game seconds. Used to calculate the actual speed of melee attacks. | [`parser/parse_animations.py`](../parser/parse_animations.py) |
| [`pattern_types.json`](pattern_types.json) | Map of pattern types from `data/game/var/generator.cfg`: which specific `.pattern` files belong to each category (`forests_pine_big`, `stones`, `mng/mni/mnc`, etc.) with weights `Freq`. | [`parser/parse_generator_cfg.py`](../parser/parse_generator_cfg.py) |
| [`pattern_inventory.json`](pattern_inventory.json) | Per-pattern statistics: for each `.pattern` file - dimensions, number of mask cells, number of objects. | [`parser/parse_pattern_inventory.py`](../parser/parse_pattern_inventory.py) |
| [`pattern_type_stats.json`](pattern_type_stats.json) | Per-type aggregates: median / min / max mask cells by pattern type (for calibrating the forest/stone counting model). | [`parser/parse_pattern_inventory.py`](../parser/parse_pattern_inventory.py) |
| [`replay_ground_truth.json`](replay_ground_truth.json) | Empirical ground truth from replays: for each `.rep`/`.map` - party settings + exact pattern clusters placed by the engine. Used to calibrate [`compute_map_resources`](../compute/compute_map_resources.py) against reality. | [`parser/parse_replay_aggregates.py`](../parser/parse_replay_aggregates.py) |

<a id="engine-reverse-engineering-потребляется-документацией-в-internals"></a>
## Engine reverse-engineering (consumed by documentation in `internals/`)

| File | What's inside | From |
|---|---|---|
| [`dws_native_signatures.json`](dws_native_signatures.json) | **4,856 native DWS signatures** extracted directly from `cossacks.exe`: function name, argument list, types, RVA. 100% coverage of 884 primitives actually called by the script. See [`internals/engine/native_api.md`](../internals_en/engine/native_api.md). | [`parser/engine_recon/extract_dws_signatures.py`](../parser/engine_recon/extract_dws_signatures.py) |
| [`engine_primitives.json`](engine_primitives.json) | 884 native functions + 46 type-casts, distributed among subsystems (`game_object`, `player`, `path_command`, `save_load`, ...). Basic dump without arguments - for quick searching. | [`parser/engine_recon/extract_primitives.py`](../parser/engine_recon/extract_primitives.py) |
| [`engine_primitive_matches.json`](engine_primitive_matches.json) | Same as `engine_primitives.json`, but with RVA locations for each mapping. | [`parser/engine_recon/extract_primitives.py`](../parser/engine_recon/extract_primitives.py) |
| [`exe_strings.json`](exe_strings.json) | Raw string pool from `cossacks.exe`: ~61 k ASCII + ~15 k Pascal ShortString. The source for all extractors is above. | [`parser/engine_recon/dump_exe_strings.py`](../parser/engine_recon/dump_exe_strings.py) |

<a id="как-использовать"></a>
## How to use

<a id="из-редактора-browser"></a>
### From the editor (browser)
```javascript
fetch("../data.json").then(r => r.json())
fetch("../derived/canonical_terms.json").then(r => r.json())
fetch("../derived/game_settings.json").then(r => r.json())
fetch("../derived/tech_tree.json").then(r => r.json())
fetch("../derived/builder_slots.json").then(r => r.json())
```
See [`editor/js/data_loader.js`](../editor/js/data_loader.js).

<a id="из-python-writer--compute--simulator"></a>
### From Python (writer/compute/simulator)
```python
import json
from pathlib import Path
DERIVED = Path(__file__).resolve().parent.parent / "derived"
canon = json.loads((DERIVED / "canonical_terms.json").read_text(encoding="utf-8"))
```
Better - through ready-made utilities in [`parser/config.py`](../parser/config.py)
(`NATION_NAMES_RU`, `USAGE_RU`, `BUILDING_NAMES_RU`, `WEAPON_KIND_RU`,
`nation_ru()`, `nation_label()`, `usage_ru()`, `decode_upg_type(s, lang='ru')`).

<a id="регенерация"></a>
### Regeneration

After the game patch:
```bash
python scripts/regen.py derived          # all game-data JSON files in this directory
# Or regenerate individual datasets:
python parser/build_replay_upgrades.py
python parser/build_canonical_terms.py
python parser/parse_animations.py
python parser/parse_generator_cfg.py
python parser/parse_pattern_inventory.py
python parser/parse_replay_aggregates.py
python compute/compute_game_settings.py
python parser/build_tech_graph.py
python compute/compute_builder_slots.py

# Engine reverse-engineering dumps (regenerate only when cossacks.exe changes):
python parser/engine_recon/dump_exe_strings.py        # → derived/exe_strings.json
python parser/engine_recon/extract_primitives.py      # → derived/engine_primitives.json + engine_primitive_matches.json
python parser/engine_recon/extract_dws_signatures.py  # → derived/dws_native_signatures.json + internals/engine/native_primitives.md
```
The complete pipeline is `python scripts/regen.py all` (a little more than 4 minutes).

<a id="где-не-лежит"></a>
## Where it doesn't lie

- **Raw game data** — [`../data.json`](../data.json), the ~5.7 MB master
  dataset read by every generator.
- **Player-facing reference** — [`../docs_en/reference/`](../docs_en/reference/),
  [`../docs_en/reports/`](../docs_en/reports/), and [`../docs_en/recon/`](../docs_en/recon/).
- **Engine documentation** — [`../internals_en/`](../internals_en/) (engine,
  scripts, and data formats).
- **Pipeline architecture diagram** — [`../docs_en/architecture.md`](../docs_en/architecture.md).
