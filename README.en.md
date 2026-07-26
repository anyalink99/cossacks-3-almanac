# Cossacks 3 Almanac

**English** · [Русский](README.md)

A complete guide to the economy, units, buildings and upgrades of the game **Cossacks 3 - Back to War**, extracted directly from game scripts (`unit.script`, `country.script`, `dmscript.global`, locale files). In the repository: parser of game files, a set of derivative calculations, writers for markdown / xlsx, economics simulator and accumulated research mechanics.

> The source of all numbers is the installed game files. If something
> disagrees with an external calculator or guide, trust the repository; known
> discrepancies are documented. The pipeline is idempotent: after a game
> patch, regenerate it and all artifacts will be updated.

<a id="что-внутри"></a>
## What's inside

**Ready directory for players** - open directly on GitHub, you do not need to run anything. Everything is in [`docs/`](docs_en/):

- [`docs/reference/`](docs_en/reference/) - Canonical reference: 7 chapters by topic, 21 nations, 15 side-by-side comparisons
- [`docs/recon/`](docs_en/recon/) - handwritten reverse-engineering game mechanics, broken down by theme:
`world/economy/` (mining, building, capture, starvation, queue, upgrades), `world/combat/` (damage, formations, target selection, towers, walls, artillery, fleet, review), `world/map/` (map generation, lobby options), `systems/` (AI, mercenaries, victory conditions, scenarios, UI/ent)
[`docs/reports/`](docs_en/reports/) are derived calculations grouped by theme:
`combat/` (DPS, counter-matrix, attack speed, vision, artillery), `economy/` (scaling, builders, construction, production, slot, efficiency), `tech/` (tech tree), `map/` (resources, launch layout, replay validation), `nations/` (overview, deviations)

** Technical documentation (for developers/modders)** - separate from `docs/` in [`internals/`](internals_en/):

[`internals/engine/`](internals_en/engine/) — engine device (Delphi + DWS): native API (4,856 functions), RTTI, RNG, animation system, network packages, tics
[`internals/scripts/`](internals_en/scripts/) — the `data/scripts/*` (load order, entry points) structure
- [`internals/data/`](internals_en/data/) - `data/` game directory: subfolders and file formats (`.parser`, `.pattern`, `.aaf`)

**Machine-readable JSON datasets** - for build editor, simulator, external analyzers:

- [`data.json`](data.json) - master structure (~5.7 MB): 21 nations, 456 buildings, 714 units, 4,483 upgrades
- [`derived/`](derived/) - Specialized slices: `tech_tree.json`, `builder_slots.json`, `animations.json`, `game_settings.json`, `canonical_terms.json`, `pattern_*.json`, `replay_ground_truth.json`, plus engine-RE dumps (`dws_native_signatures.json`, `engine_primitives.json`, `exe_strings.json`)

**Pipeline for regeneration after game patch:**

- [`parser/`](parser/) - extraction of data from `.script` (Pascal parser with symbolic execution); subfolder [`engine_recon/`](parser/engine_recon/) - extractors from the `cossacks.exe` binary
- [`compute/`](compute/) - derived calculations (scaling, map gen, tech tree, construction times, etc.)
- [`writers/`](writers/) - generation of markdown directory + diff between snapshots
- [`simulator/`](simulator/) - timeline economy simulator (backend for browser editor via Pyodide)
- [`editor/`](editor/) - browser build editor (HTML + JS + Pyodide), runs the simulator directly in the browser
- [`scripts/regen.py`](scripts/regen.py) + [`Makefile`](Makefile) - a single runner for the entire pipeline
**Before starting work with `data.json`:** [`internals/project/known_issues.md`](internals_en/project/known_issues.md) — a list of current parser gaps, discrepancies with external guides and open empirical questions. Closed issues, including a previous error with mercenary stats, are transferred to [`internals/project/known_issues_archive.md`](internals_en/project/known_issues_archive.md).

**Mods** - changes in game logic via C3 mod-loader:

- [`mods/`](mods/) - each mod as a subfolder with `build.py` (patcher) and the result collected. See [`mods/README.md`](mods/README.md) for the convention.

<a id="структура-репозитория"></a>
## Structure of the repository
```
.
├── data.json                master data (~5.7 MB; downstream source of truth)
├── derived/                 machine-readable JSON datasets and engine RE dumps
├── parser/                  game .script parsers → data.json
│   └── engine_recon/        extractors for the DWS native API, RTTI, and primitives
├── compute/                 derived calculations → docs/reports/<topic>/
├── writers/                 data.json → Markdown plus prose templates
├── simulator/               timeline economy simulator used through Pyodide
├── editor/                  browser-based build-order editor
├── mods/                    mods, each with build.py + src/ + build/
├── scripts/                 pipeline runner (regen.py)
│
├── docs/                    Russian player documentation
├── docs_en/                 English player documentation
│   ├── reference/           canonical reference, nations, and comparisons
│   ├── recon/               handwritten mechanics research
│   └── reports/             generated combat, economy, tech, map, and nation reports
│
├── internals/               Russian technical documentation
└── internals_en/            English technical documentation
    ├── engine/              cossacks.exe, DWS, RNG, synchronization, ticks, animations
    ├── scripts/             data/scripts/* load order and entry points
    └── data/                data/ directory layout and file formats
```
<a id="быстрый-старт"></a>
## Quick start

<a id="просто-почитать"></a>
### Just read

GitHub renders markdown – open the file. Entrance points:

- [`docs/reference/README.md`](docs_en/reference/README.md) - Table of Contents of Reference + Brief Extract
[`docs/recon/README.md`](docs_en/recon/README.md) - Deep Research Index
- [`docs/reports/README.md`](docs_en/reports/README.md) - index of derivative reports

<a id="регенерировать-после-патча-игры"></a>
### Regenerate after a game patch

Requirements: Python 3.11+ and installed Cossacks 3 (Steam). Default is searched in `C:\Program Files (x86)\Steam\steamapps\common\Cossacks 3` - for another path, set the env variable:
```bash
# Linux/macOS
export COSSACKS3_PATH="/path/to/Cossacks 3"

# Windows (PowerShell)
$env:COSSACKS3_PATH = "D:\Games\Cossacks 3"
```
Then from the root of the repository one of the options:
```bash
# Option 1 — cross-platform Python runner:
python scripts/regen.py                         # full regeneration
python scripts/regen.py reference               # writers only
python scripts/regen.py reports-combat          # docs/reports/combat only
python scripts/regen.py help                    # list all targets

# Option 2 — make:
make all          # = python scripts/regen.py all
make reference
make reports
make sanity       # parser + 112 sanity checks
make help
```
What is inside (for a turn-based call without a runner):
```bash
python parser/build_data.py                     # → data.json (master data)
python parser/build_canonical_terms.py          # → derived/canonical_terms.json
python writers/write_md_tree.py                 # → docs/reference/ + docs/README.md
python compute/compute_combat_stats.py          # → docs/reports/combat/combat_stats.md
python compute/compute_counter_matrix.py        # → docs/reports/combat/counter_matrix.md
python compute/compute_attack_rates.py          # → docs/reports/combat/attack_rates.md
python compute/compute_vision.py                # → docs/reports/combat/vision_radii.md
python compute/compute_scaling.py               # → docs/reports/economy/scaling_prices.md
python compute/compute_efficiency_upgrades.py   # → docs/reports/economy/efficiency_upgrades.md
python compute/compute_construction_times.py    # → docs/reports/economy/construction_times.md
python compute/compute_builder_slots.py         # → docs/reports/economy/builder_slots.md (+derived/builder_slots.json)
python parser/build_tech_graph.py               # → derived/tech_tree.json
python compute/compute_tech_tree.py             # → docs/reports/tech/tech_tree.md + economy/production_rates.md
python compute/compute_game_settings.py         # → docs/reports/map/lobby_settings.md (+derived/game_settings.json)
python compute/compute_map_resources.py         # → docs/reports/map/map_resources.md
python compute/compute_starting_layout.py       # → docs/reports/map/starting_layout.md
python compute/validate_map_predictions.py      # → docs/reports/map/map_predictions_validation.md
python compute/compute_nations_overview.py      # → docs/reports/nations/overview.md
python parser/parse_animations.py               # → derived/animations.json
python parser/parse_generator_cfg.py            # → derived/pattern_types.json
python parser/parse_pattern_inventory.py        # → derived/pattern_{inventory,type_stats}.json
```
`parser/build_data.py` is the only script that reads game files. All others consume `data.json` and work in <30 seconds.

<a id="diff-снапшотов-после-патча"></a>
### Compare snapshots after a patch

One step through make (or manual - three commands below):
```bash
make diff   # snapshot data.json, regenerate, write diff.md
```
Or by hand:
```bash
python parser/build_data.py
cp data.json /tmp/data_old.json
# … update the game …
python parser/build_data.py
python writers/diff_snapshots.py /tmp/data_old.json data.json --out diff.md
```
After the regeneration in `diff.md`, you can see all stat changes between versions of the game.

## Sanity checks

`parser/build_data.py` runs **112 autochecks** at each launch and feils if the game changes something key (time constants, base portions, known numbers of specific units, mine upgrade chain, market rates). Coverage – `parser/README.md` contains a list of categories.

<a id="что-сейчас-в-данных"></a>
## What's in the data now

- **Nations:**21 (playable; mis/tat/lit excluded)
** Buildings:** 456 lines (sid×nation)
- ** Units: ** 714 lines
* Upgrades:** 4483 lines (with full cost/value/itype/prereqs allowed)
- **Officers/formations:** 231 groups

<a id="лицензия-и-атрибуция"></a>
## License and attribution

This repository contains **only derived data** from publicly distributed Cossacks 3 (GSC Game World) game files. Game resources and trademarks belong to their owners. Scripts in this repository are a separate work, distributed without a special license (use at your own risk).
