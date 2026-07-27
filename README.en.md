# Cossacks 3 Almanac

**English** · [Русский](README.md)

A data-backed encyclopedia of the economy, units, buildings, upgrades, and
hidden mechanics of **Cossacks 3: Back to War**. The repository extracts its
facts directly from the game scripts and localization files, then publishes
them as a reader-facing reference, detailed mechanics articles, calculated
reports, machine-readable datasets, and browser tools.

> The source of all numbers is the installed game files. If something
> disagrees with an external calculator or guide, trust the repository; known
> discrepancies are documented. The pipeline is idempotent: after a game
> patch, regenerate it and all artifacts will be updated.

<a id="что-внутри"></a>
## What's inside

**For players:** open the [English encyclopedia](docs_en/README.md). Nothing
needs to be installed or regenerated.

- [`docs_en/reference/`](docs_en/reference/) — a concise reference arranged by
  topic, nation, and side-by-side comparison
- [`docs_en/recon/`](docs_en/recon/) — handwritten explanations of economy,
  combat, orders, map generation, artificial intelligence, and other mechanics
- [`docs_en/reports/`](docs_en/reports/) — calculated tables for combat,
  economy, technology, maps, and national differences

**For developers and modders:** [`internals_en/`](internals_en/) documents the
Delphi and DWS engine, native API, synchronization, random-number generators,
script layout, game data, and file formats.

**For tools and external analysis:**

- [`data.json`](data.json) — the master dataset: 21 nations, 456
  nation-specific building rows, 714 unit rows, and 4,483 upgrade rows
- [`derived/`](derived/) — specialized datasets such as `tech_tree.json`,
  `builder_slots.json`, `canonical_terms.json`, map-generation data, replay
  ground truth, and engine reverse-engineering dumps

**For regeneration after a game update:**

- [`parser/`](parser/) extracts game scripts, localization, animations, and
  other source data
- [`compute/`](compute/) derives formulas and comparison tables
- [`writers/`](writers/) renders the Markdown reference
- [`simulator/`](simulator/) and [`editor/`](editor/) provide the economy
  simulator and browser build-order editor
- [`scripts/regen.py`](scripts/regen.py) and [`Makefile`](Makefile) run the
  complete or targeted pipeline

Before relying on `data.json` for development, read the
[known limitations](internals_en/project/known_issues.md). Resolved issues are
kept in the [archive](internals_en/project/known_issues_archive.md).

[`mods/`](mods/) contains game-logic modifications built for the C3 mod loader;
its [README](mods/README.md) describes the directory convention.

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

GitHub renders Markdown directly. Start with:

- [Cossacks 3 Encyclopedia](docs_en/README.md)
- [Quick Reference](docs_en/reference/README.md)
- [How the Game Works](docs_en/recon/README.md)
- [Tables and Calculations](docs_en/reports/README.md)

<a id="регенерировать-после-патча-игры"></a>
### Regenerate after a game patch

Requirements: Python 3.11+ and an installed Steam copy of Cossacks 3. The
default path is
`C:\Program Files (x86)\Steam\steamapps\common\Cossacks 3`. Set
`COSSACKS3_PATH` when the game is installed elsewhere:
```bash
# Linux/macOS
export COSSACKS3_PATH="/path/to/Cossacks 3"

# Windows (PowerShell)
$env:COSSACKS3_PATH = "D:\Games\Cossacks 3"
```
From the repository root, use either the Python runner or `make`:
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
The individual generators can also be run directly:
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
python scripts/build_entity_catalog.py           # → assets/data/entity-catalog.json + game UI icons
```
`parser/build_data.py` reads gameplay data, while
`scripts/build_entity_catalog.py` reads the HUD material map and UI atlases.
The other generators consume `data.json` without parsing the game installation
again.

<a id="diff-снапшотов-после-патча"></a>
### Compare snapshots after a patch

Run the complete snapshot comparison through `make`:
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
The resulting `diff.md` lists every detected statistic change between the two
game versions.

## Sanity checks

`parser/build_data.py` runs **112 automatic checks** on each launch and fails if
an update changes a key invariant: timing constants, base resource portions,
known unit values, the mine-upgrade chain, or market rates. The coverage
categories are listed in `parser/README.md`.

<a id="что-сейчас-в-данных"></a>
## What's in the data now

- **Nations:** 21 playable nations (`mis`, `tat`, and `lit` excluded)
- **Buildings:** 456 nation-specific rows
- **Units:** 714 rows
- **Upgrades:** 4,483 rows with complete cost, value, effect, and prerequisite data
- **Officers/formations:** 231 groups

<a id="лицензия-и-атрибуция"></a>
## License and attribution

This repository primarily contains derived data from publicly distributed
Cossacks 3 files (GSC Game World). The visual object cards also include small
UI icons cropped automatically from the game's atlases. Game artwork, names,
and trademarks belong to their respective owners. The repository's scripts are
a separate work distributed without a specific license; use them at your own
risk.
