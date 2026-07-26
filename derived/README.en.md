Machine-readable JSON datasets

[English] (README.en.md) * * Russian**

Here are all JSON files for tools: build editor, simulator,
External analyzers and engine-RE dumps from `cossacks.exe`. All
generated. **Do not edit with your hands ** - will be rewritten at
next regeneration.

Game data (consumed by writer/editor/simulator)

| File | What's inside |
|---|---|---|
| [`canonical_terms.json`] (canonical_terms.json) | Canonical Russian names from the game locale: 21 nations, 22 buildings, 7 types of weapons, 5 difficulty levels, 79 lobby settings, 9 types of officer training, 75 upgrades, 148 units, 6 resources. **A single source of truth for all writers and compute scripts. | [`parser/build_canonical_terms.py`] (../parser/build_canonical_terms.py) |
| [`replay_upgrades.json`] (replay_upgrades.json) | Compact, nation-ordered improvement guide for replay-parser. Only saves `sid`, Russian/English name and research building, so that the browser does not download the full `data.json`. | [`parser/build_replay_upgrades.py`] (../parser/build_replay_upgrades.py) |
| [`game_settings.json`] (game_settings.json) | All lobby options (`mapsize`, `terraintype`, `relieftype`, `peacetime`, `gamespeed`, etc.) – 95 values in 18 categories, with English and Russian labels + default values from `initmap.inc`. Used by the browser editor to build dropdowns. | [`compute/compute_game_settings.py`] (../compute/compute_game_settings.py) |
| [`tech_tree.json`] (tech_tree.json) | Graph of Dependencies of Buildings, Units and Upgrades: for each `sid` - list of prereq's with types (`[B]` building, `[U]` unit, `[T]` upgrade) + base price and time. Used by an economics simulator and editor. | [`parser/build_tech_graph.py`] (../parser/build_tech_graph.py) |
| [`builder_slots.json`] (builder_slots.json) | How many peasants can build each building simultaneously. It is considered bypassing the perimeter of the collision mask with a step `gc_BuilderDist = 1.0`. Used in [`docs/reports/economy/builder_slots.md`] (../docs/reports/economy/builder_slots.md) and in the editor. | [`compute/compute_builder_slots.py`] (../compute/compute_builder_slots.py) |
| [`animations.json`] (animations.json) | Animated frame base for each unit: `{sid: {anim_name: [start_frame, end_frame]}, ...}` - extracted from `<game>/data/animations/aaf/*.aaf`. Length of one frame = 1 / 32 game seconds. It is used to calculate the real speed of melee attacks. | [`parser/parse_animations.py`] (../parser/parse_animations.py) |
| [`pattern_types.json`](pattern_types.json) | Pattern Map from `data/game/var/generator.cfg`: which specific `.pattern` files belong to each category (`forests_pine_big`, `stones`, `mng/mni/mnc`, etc.) with `Freq` weights. | [`parser/parse_generator_cfg.py`] (../parser/parse_generator_cfg.py) |
| [`pattern_inventory.json`] (pattern_inventory.json) | Per-pattern statistics: for each `.pattern` file, dimensions, number of mask cells, number of objects. | [`parser/parse_pattern_inventory.py`] (../parser/parse_pattern_inventory.py) |
| [`pattern_type_stats.json`] (pattern_type_stats.json) | Per-type aggregates: median / min / max mask cells by pattern type (for calibrating the forest/stone count model). | [`parser/parse_pattern_inventory.py`] (../parser/parse_pattern_inventory.py) |
| [`replay_ground_truth.json`] (replay_ground_truth.json) | Empirical ground truth from replays: for each `.rep`/`.map` - batch settings + exact clusters of patterns placed by the engine. It is used to calibrate [`compute_map_resources`] (../compute/compute_map_resources.py) against reality. | [`parser/parse_replay_aggregates.py`] (../parser/parse_replay_aggregates.py) |

<a id="машинно-читаемые-json-датасеты"></a>
# Engine reverse-engineering (consumed in documentation in `internals/`)

| File | What's inside |
|---|---|---|
| [`dws_native_signatures.json`] (dws_native_signatures.json) | **4,856 native DWS signatures** extracted directly from `cossacks.exe`: function name, argument list, types, RVA. 100% coverage of 884 primitives actually invoked by the script. See [`internals/engine/native_api.md`](../internals_en/engine/native_api.md). | [`parser/engine_recon/extract_dws_signatures.py`] (../parser/engine_recon/extract_dws_signatures.py) |
| [`engine_primitives.json`](engine_primitives.json) | 884 native-functions + 46 type-cast's spaced in subsystems (`game_object`, `player`, `path_command`, `save_load`, ...). Basic dump without arguments - for quick search. | [`parser/engine_recon/extract_primitives.py`] (../parser/engine_recon/extract_primitives.py) |
| [`engine_primitive_matches.json`](engine_primitive_matches.json) | Same as `engine_primitives.json`, but with RVA locations of each match. | [`parser/engine_recon/extract_primitives.py`] (../parser/engine_recon/extract_primitives.py) |
| [`exe_strings.json`](exe_strings.json) | Raw string pool from `cossacks.exe`: ~61 k ASCII + ~15 k Pascal ShortString. The source for all extractors is higher. | [`parser/engine_recon/dump_exe_strings.py`] (../parser/engine_recon/dump_exe_strings.py) |

<a id="игровые-данные-потребляются-writerами--редактором--симулятором"></a>
## How to use it

# From the editor (browser)
```javascript
fetch("../data.json").then(r => r.json())
fetch("../derived/canonical_terms.json").then(r => r.json())
fetch("../derived/game_settings.json").then(r => r.json())
fetch("../derived/tech_tree.json").then(r => r.json())
fetch("../derived/builder_slots.json").then(r => r.json())
```
See [`editor/js/data_loader.js`] (../editor/js/data_loader.js).

From Python (writer / compute / simulator)
```python
import json
from pathlib import Path
DERIVED = Path(__file__).resolve().parent.parent / "derived"
canon = json.loads((DERIVED / "canonical_terms.json").read_text(encoding="utf-8"))
```
Better - through ready-made utilities in [`parser/config.py`](../parser/config.py)
(`NATION_NAMES_RU`, `USAGE_RU`, `BUILDING_NAMES_RU`, `WEAPON_KIND_RU`),
`nation_ru()`, `nation_label()`, `usage_ru()`, `decode_upg_type(s, lang='ru')`.

Regeneration

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
Complete pipeline - `python scripts/regen.py all` (just over 4 minutes).

##Where it is not

- **Raw game data** - in [`../data.json`](../data.json) (master structure,
~5.7 MB; read all generators.
- **Ready for people help** - in [`../docs/reference/`](../docs/reference/),
[`../docs/reports/`](../docs/reports/), [`../docs/recon/`](../docs/recon/).
* Documentation of the engine** - in [`../internals/`] (../internals/) (engine, scripts, data).
**Data pipeline architecture diagram in [`../internals/project/architecture.md`](../internals_en/project/architecture.md).
