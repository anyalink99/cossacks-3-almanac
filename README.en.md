# Cossacks 3 Almanac

**English** · [Русский](README.md)

A comprehensive reference for the economy, units, buildings, and upgrades in **Cossacks 3 — Back to War**, extracted directly from game scripts (`unit.script`, `country.script`, `dmscript.global`, and locale files). The repository includes game-file parsers, derived calculations, Markdown/XLSX writers, an economy simulator, and reverse-engineering research.

> Every number comes from the installed game files. When an external calculator or guide disagrees, prefer this repository; known discrepancies are documented. The pipeline is idempotent, so a game patch can be handled by regenerating all artifacts.

## What's inside

**Player reference** — open it directly on GitHub; no local setup is required. The English edition is in [`docs_en/`](docs_en/):

- [`docs_en/reference/`](docs_en/reference/) - canonical reference: 7 chapters on topics, 21 nations, 15 side-by-side comparisons
- [`docs_en/recon/`](docs_en/recon/) - handwritten reverse-engineering game mechanics, divided into topics:
  `world/economy/` (production, construction, capture, hunger, queue, upgrades), `world/combat/` (damage, formations, target selection, towers, walls, artillery, fleet, review), `world/map/` (map generation, lobby options), `systems/` (AI, mercenaries, victory conditions, scenarios, UI/input)
- [`docs_en/reports/`](docs_en/reports/) - derivative calculations grouped by topic:
  `combat/` (DPS, counter-matrix, attack speed, vision, artillery), `economy/` (scaling, builder slots, construction, production, efficiency), `tech/` (tech tree), `map/` (resources, starting layout, replay validation), `nations/` (overview, deviations)

**Technical documentation for developers and modders** — kept separately in [`internals_en/`](internals_en/):

- [`internals/engine/`](internals_en/engine/) — engine internals (Delphi + DWS): native API (4,856 functions), RTTI, RNG, animation system, network packets, and ticks
- [`internals/scripts/`](internals_en/scripts/) — `data/scripts/*` structure, load order, and entry points
- [`internals/data/`](internals_en/data/) — the game's `data/` directory, subdirectories, and file formats (`.parser`, `.pattern`, `.aaf`)

**Machine-readable JSON datasets** - for the build editor, simulator, external analyzers:

- [`data.json`](data.json) — master dataset (~5.7 MB): 21 nations, 456 building rows, 714 unit rows, and 4,483 upgrade rows
- [`derived/`](derived/) - specialized sections: `tech_tree.json`, `builder_slots.json`, `animations.json`, `game_settings.json`, `canonical_terms.json`, `pattern_*.json`, `replay_ground_truth.json`, plus engine-RE dumps (`dws_native_signatures.json`, `engine_primitives.json`, `exe_strings.json`)

**Pipeline - for regeneration after a game patch:**

- [`parser/`](parser/) — extracting data from `.script` (Pascal parser with symbolic execution); subfolder [`engine_recon/`](parser/engine_recon/) - extractors from the `cossacks.exe` binary
- [`compute/`](compute/) - derivative calculations (scaling, map gen, tech tree, construction times, etc.)
- [`writers/`](writers/) - generation of markdown reference + diff between snapshots
- [`simulator/`](simulator/) - timeline economic simulator (backend for browser editor via Pyodide)
- [`editor/`](editor/) - browser-based build editor (HTML + JS + Pyodide), launches the simulator directly in the browser
- [`scripts/regen.py`](scripts/regen.py) + [`Makefile`](Makefile) - a single runner for the entire pipeline
**Before building on `data.json`:** read [`docs_en/known_issues.md`](docs_en/known_issues.md) for current parser gaps, discrepancies with external guides, and open empirical questions. Resolved issues, including the former mercenary-stat bug, are recorded in [`docs_en/known_issues_archive.md`](docs_en/known_issues_archive.md).

**Mods** - changes to game logic via C3 mod-loader:

- [`mods/`](mods/) - each mod as a subfolder with `build.py` (patcher) and the collected result. See [`mods/README.md`](mods/README.en.md) for convention.

## Repository structure
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
## Quick start

### Just read

GitHub renders markdown - open the required file. Entry points:

- [`docs/reference/README.md`](docs_en/reference/README.md) - table of contents of the directory + summary
- [`docs/recon/README.md`](docs_en/recon/README.md) - deep research index
- [`docs/reports/README.md`](docs_en/reports/README.md) — index of derived reports

### Regenerate after game patch

Requirements: Python 3.11+ and Cossacks 3 (Steam) installed. Default is searched in `C:\Program Files (x86)\Steam\steamapps\common\Cossacks 3` - for another path, set the env variable:
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
What's inside (for step-by-step calling without a runner):
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
`parser/build_data.py` is the only script that reads game files. All others consume `data.json` and work for <30 seconds in total.

### Diff snapshots after the patch

One step via make (or manual - three commands below):
```bash
make diff   # snapshot data.json, regenerate, write diff.md
```
Or manually:
```bash
python parser/build_data.py
cp data.json /tmp/data_old.json
# … update the game …
python parser/build_data.py
python writers/diff_snapshots.py /tmp/data_old.json data.json --out diff.md
```
After regeneration in `diff.md`, all stat changes between versions of the game are visible.

## Sanity checks

`parser/build_data.py` runs **112 automatic checks** on every invocation and fails when a key game invariant changes: time constants, base resource portions, known unit values, the mine-upgrade chain, market rates, and more. [`parser/README.en.md`](parser/README.en.md) lists the covered categories.

## What's in the data now

- **Nations:** 21 (playable; mis/tat/lit excluded)
- **Buildings:** 456 rows (sid×nation)
- **Units:** 714 lines
- **Upgrades:** 4,483 rows (with cost, value, `itype`, and prerequisites resolved)
- **Officers/formations:** 231 groups

## License and Attribution

This repository contains **derived data only** from publicly distributed Cossacks 3 game files (GSC Game World). Game resources and trademarks belong to their owners. The scripts in this repository are a separate work and are distributed without a special license (use at your own risk).
