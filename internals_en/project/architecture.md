<a id="архитектура-проекта"></a>
# Project architecture

**English** · [Русский](../../internals/project/architecture.md)

This document traces data from the game files to the Markdown reference. Read
it before adding a report or changing a generator.

<a id="поток-данных"></a>
## Data flow
```
┌─────────────────────────────────────────────────────────────────┐
│ Cossacks 3 install (read-only):                                 │
│   data/scripts/*.script, *.global, *.inc       (Pascal-like)    │
│   data/locale/{ru,en,...}/*.txt                (cp1251)         │
│   data/animations/aaf/*.aaf                    (animations)     │
│   data/pattern/*.pattern                       (map patterns)   │
│   data/game/var/*.cfg                          (formations, …)  │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ parser/ — extraction from game files to JSON                    │
│                                                                 │
│   parser/build_data.py            (orchestrator)                │
│     ├── parse_units.py            → unit / building / weapon    │
│     ├── parse_country.py          → upgrade / officer / squad   │
│     ├── parse_locale.py           → name_en / name_ru           │
│     ├── extract_constants.py      → gc_* constants              │
│     └── simulate_upgrades.py      → 4,483 upgrades + prereqs    │
│                                                                 │
│   parser/build_canonical_terms.py → canonical_terms.json        │
│   parser/parse_animations.py      → animations.json             │
│   parser/parse_pattern_inventory.py → pattern_*.json            │
│   parser/parse_replay_aggregates.py → replay_ground_truth.json  │
│   parser/parse_generator_cfg.py   → pattern_types.json          │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ data.json (top-level) + derived/*.json (top-level)              │
│                                                                 │
│   data.json              master dataset (~5.5 MB):              │
│     - 21 nations, 456 buildings, 714 units, 4,483 upgrades      │
│   derived/*.json         specialized datasets                   │
│     (see derived/README.md)                                     │
└─────────────────────────────────────────────────────────────────┘
                            │
            ┌───────────────┴───────────────┐
            ▼                               ▼
┌──────────────────────────┐   ┌──────────────────────────────────┐
│ writers/ — MD rendering  │   │ compute/ — derived calculations │
│                          │   │                                   │
│ write_md_tree.py         │   │ Combat:                          │
│   → docs/reference/      │   │   compute_combat_stats            │
│      01_economy/README.md │   │   compute_counter_matrix          │
│      02_combat/README.md  │   │   compute_attack_rates            │
│      …                   │   │   compute_vision                  │
│      nations/×21         │   │   compute_artillery               │
│      compare/×33         │   │ Economy:                         │
│   + templates/*.md       │   │   compute_scaling                 │
│   + docs/README.md       │   │   compute_efficiency_upgrades     │
│                          │   │   compute_construction_times      │
│                          │   │   compute_builder_slots           │
│ diff_snapshots.py        │   │ Technology tree:                 │
│   → diff.md              │   │   compute_tech_tree              │
│   compares two data.json │   │     → tech_tree.json + 2 reports│
│                          │   │ Map:                             │
│                          │   │   compute_game_settings.py        │
│                          │   │     → game_settings.json + md     │
│                          │   │   compute_map_resources           │
│                          │   │   compute_starting_layout        │
│                          │   │   validate_map_predictions.py     │
│                          │   │ Nations:                         │
│                          │   │   compute_nations_overview        │
└──────────────────────────┘   └──────────────────────────────────┘
            │                               │
            └───────────────┬───────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ docs/README.md + docs/reference/ + docs/reports/                 │
│ (human-readable Markdown rendered directly by GitHub)           │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ simulator/ — runtime economy simulator                          │
│                                                                 │
│   simulate_economy.py reads data.json + derived/tech_tree.json, │
│   accepts a build order (JSON), and returns a state timeline.   │
│   The browser editor runs it through Pyodide.                   │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ editor/ — browser build-order editor                            │
│                                                                 │
│   index.html + js/* load data.json + derived/*.json and run     │
│   the simulator through Pyodide.                                │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ internals/ + parser/engine_recon/                                │
│                                                                  │
│   parser/engine_recon/{dump_exe_strings, extract_primitives,     │
│   extract_dws_signatures}.py                                     │
│     ← read `cossacks.exe` (top-level <game>/cossacks.exe)        │
│     → derived/{exe_strings, engine_primitives,                   │
│         engine_primitive_matches, dws_native_signatures}.json    │
│     → internals/engine/native_primitives.md (auto-gen)           │
│   internals/engine/*.md — handwritten technical documentation    │
│     of the engine (RNG, sync, ticks, animation system, RTTI).    │
└─────────────────────────────────────────────────────────────────┘
```
<a id="принципы"></a>
## Principles

1. **One source of truth at each level:**
   - Game files are read-only inputs.
   - The top-level `data.json` is the single general-purpose dataset consumed
     by writers, computation scripts, the simulator, and the editor.
   - Top-level `derived/*.json` files are specialized datasets for individual
     consumers. Some describe gameplay (`canonical_terms`, `tech_tree`,
     `builder_slots`, `animations`); others are engine reverse-engineering
     dumps (`dws_native_signatures`, `engine_primitives`, `exe_strings`).
2. **Idempotency.** `python scripts/regen.py all` rebuilds every generated
   artifact from scratch without accumulating side effects. One run should be
   enough after a game update.
3. **Do not edit generated Markdown directly.** Regeneration overwrites it. To
   change wording, edit a template under `writers/templates/` or the source
   text in the relevant `compute/<script>.py`. The handwritten exceptions are:
   - `docs/recon/**/*.md` — handwritten explanations of game mechanics.
   - `internals/**/*.md` — handwritten technical documentation, except for the
     generated `internals/engine/native_primitives.md`.
   - `internals/project/known_issues*.md` — handwritten issue lists.
   - `internals/project/architecture.md` (this file) — handwritten.
   - `derived/README.md` — handwritten.
   - `docs/README.md` — generated by `writers/write_md_tree.py`.
4. **Canonical localized terms come from the game.** Do not invent a
   translation when the game already supplies one. The terminology dataset
   lives in `derived/canonical_terms.json` and is generated from
   `data/locale/{ru,en}/`; writers and computation scripts import it through
   `parser/config.py` (`NATION_NAMES_RU`, `USAGE_RU`, `BUILDING_NAMES_RU`,
   `WEAPON_KIND_RU`, `decode_usage(s, lang='ru')`, `nation_label(sid)`).
5. **Sanity checks.** `parser/build_data.py` runs 112 automatic checks on every
   build so that a changed invariant is visible immediately after a game
   update.

<a id="где-что-лежит"></a>
## Repository map

<a id="код"></a>
### Code

| Folder | Purpose |
|---|---|
| `parser/` | Reading game files → JSON (`data.json`, `derived/*.json`). |
| `parser/engine_recon/` | Extractors from `cossacks.exe` (DWS API, primitives, exe-strings). |
| `compute/` | Derived calculations based on JSON → Markdown reports under `docs/reports/`. |
| `writers/` | Rendering the canonical reference under `docs/reference/` and comparing snapshots. |
| `simulator/` | Runtime economic simulator (build orders → timelines). |
| `editor/` | Browser build editor (HTML + JS + Pyodide). |
| `mods/` | Game mods, each with a `build.py` patcher and its source files. |
| `scripts/` | Pipeline runner (`regen.py`) and supporting maintenance tools. |

<a id="документация"></a>
### Documentation

| Folder | What's inside | Source |
|---|---|---|
| `docs/reference/` | Canonical reference: 7 chapters, 21 nations, 33 comparison articles. | Auto-gen (`writers/write_md_tree.py` + `templates/`). |
| `docs/reports/` | Derived calculations for combat, economy, technology, maps, and nations. | Auto-generated (`compute/*.py`). |
| `docs/recon/world/{economy,combat,map}/` and `docs/recon/systems/` | Detailed explanations of game mechanics, arranged by topic. | **Handwritten.** |
| `internals/engine/` | Engine design: Delphi, DWS, random-number generation, synchronization, ticks, and animation. | **Handwritten**, except for generated `native_primitives.md`. |
| `internals/scripts/` | The structure, load order, and entry points of `data/scripts/*`. | **Handwritten.** |
| `internals/data/` | The game `data/` directory, its subfolders, and file formats. | **Handwritten.** |
| `derived/` | Machine-readable JSON for the editor, tools, and documentation. | Auto-generated by `parser/*.py`, `parser/engine_recon/*.py`, and selected computation scripts. |
| `internals/project/known_issues*.md` | Parser gaps, discrepancies, and current verified limitations. | **Handwritten.** Resolved issues move to `known_issues_archive.md`. |
| `internals/project/research_backlog_*.md` | Unverified hypotheses and reproducible experiment plans. | **Handwritten.** The single source for detailed open questions. |
| `internals/project/architecture.md` | This file. | **Handwritten.** |

<a id="расширение-pipeline"></a>
<a id="расширение-конвейера"></a>
## Extending the pipeline

<a id="добавить-новый-отчёт"></a>
### Add a new report

1. Create `compute/compute_<topic>.py`, following a neighboring
   `compute_*.py` script.
2. Register it under the appropriate `reports-*` target in
   `scripts/regen.py`.
3. Write the report to one of the existing sections—`combat`, `economy`,
   `tech`, `map`, or `nations`—under
   `docs/reports/<section>/<name>.md`. For a new section, create its directory
   and add it to `docs/reports/README.md`.
4. If the report belongs on the encyclopedia home page, add it to the
   corresponding section of `writers/write_md_tree.py`, which generates
   [`docs/README.md`](../../docs_en/README.md).

<a id="добавить-новый-json-датасет"></a>
### Add a new JSON dataset

1. Create `parser/parse_<name>.py` when the dataset reads game files, or
   `compute/compute_<name>.py` when it depends only on `data.json`.
2. Write the result to `derived/<name>.json`.
3. Describe the dataset in `derived/README.md`.
4. Register the generator under the `derived` target or the corresponding
   `reports-*` target in `scripts/regen.py`.

<a id="добавить-нацию-теоретически"></a>
### Add a nation (theoretically)

There is no plug-in registration path for a new nation. The list is embedded
in the game localization (`data/locale/*/units.txt`) and in `country.script`.
After a game update introduces a nation, extend `PLAYABLE_NATIONS` in
`parser/config.py`, then rerun `parser/build_canonical_terms.py` and
`parser/build_data.py`.

<a id="регенерация--порядок-зависимостей"></a>
## Regeneration dependency order
```
parser/build_data.py            ← reads the game; emits data.json
parser/build_canonical_terms.py ← reads locales; emits canonical_terms.json
parser/parse_animations.py      ← independent (reads .aaf)
parser/parse_generator_cfg.py   ← independent (reads .cfg)
parser/parse_pattern_inventory.py  ← after parse_generator_cfg.py
parser/parse_replay_aggregates.py  ← after parse_pattern_inventory.py

writers/write_md_tree.py        ← after data.json + canonical_terms.json
compute/compute_*.py            ← after data.json (+ selected derived/*.json)
compute/compute_game_settings.py ← independent (reads locales directly)
parser/build_tech_graph.py      ← after data.json (emits tech_tree.json)
compute/compute_tech_tree.py    ← after tech_tree.json (emits Markdown)
compute/validate_map_predictions.py ← after replay_ground_truth + compute_map_resources
simulator/simulate_economy.py   ← after tech_tree.json
```
`scripts/regen.py` resolves these dependencies through a declarative list of
targets and aliases:
```bash
python scripts/regen.py all              # complete rebuild
python scripts/regen.py reference        # writers only
python scripts/regen.py reports-combat   # combat reports only
python scripts/regen.py help             # all targets
```
Likewise via `make`: `make all`, `make reports`, `make sanity`, etc.
