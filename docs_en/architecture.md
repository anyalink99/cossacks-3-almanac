<a id="архитектура-проекта"></a>
# Project architecture

How data moves from the game files to the markdown reference. Helpful
read before adding a new report or editing the generator.

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
│   parser/parse_pattern_inventory  → pattern_*.json              │
│   parser/parse_replay_aggregates  → replay_ground_truth.json    │
│   parser/parse_generator_cfg.py   → pattern_types.json          │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ data.json (top-level) + derived/*.json (top-level)              │
│                                                                 │
│   data.json              master dataset (~5.7 MB):              │
│     - 21 nations, 456 buildings, 714 units, 4,483 upgrades      │
│   derived/*.json         specialized datasets                   │
│     (see ../derived/README.md)                                  │
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
│      compare/×16         │   │ Economy:                         │
│   + templates/*.md       │   │   compute_scaling                 │
│   + docs/README.md       │   │   compute_efficiency_upgrades     │
│                          │   │   compute_construction_times      │
│                          │   │   compute_builder_slots           │
│ diff_snapshots.py        │   │ Technology tree:                 │
│   → diff.md              │   │   compute_tech_tree              │
│   compares two data.json │   │     → tech_tree.json + 2 reports│
│                          │   │ Map:                             │
│                          │   │   compute_game_settings           │
│                          │   │     → game_settings.json + md     │
│                          │   │   compute_map_resources           │
│                          │   │   compute_starting_layout        │
│                          │   │   validate_map_predictions        │
│                          │   │ Nations:                         │
│                          │   │   compute_nations_overview        │
└──────────────────────────┘   └──────────────────────────────────┘
            │                               │
            └───────────────┬───────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ docs/reference/ + docs/reports/ + docs/known_issues.md           │
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

1. **One source of truth per level:**
   - Game files are read-only.
   - `data.json` (top-level) - the only “general” dataset, everyone reads it
     generators (writers + compute + simulator + editor).
   - `derived/*.json` (top-level) - highly specialized sections for specific
     consumers. Some are gaming (canonical_terms, tech_tree, builder_slots,
     animations, ...), part - engine-RE dumps (dws_native_signatures,
     engine_primitives, exe_strings).
2. **Idempotency.** `python scripts/regen.py all` regenerates everything with
   zero, no side effects. After the game patch - one launch.
3. **No manual edits in auto-generated md.** Everything that is generated is
   is overwritten. If you need to change the wording, edit the template in
   `writers/templates/` or text in `compute/<script>.py`. Lists of exceptions:
   - `docs/recon/**/*.md` - handwritten reverse-engineering, corrected by hand.
   - `internals/**/*.md` - handwritten technical documentation (except
     `internals/engine/native_primitives.md` - auto-gen).
   - `docs/known_issues*.md` - handwritten lists.
   - `docs/architecture.md` (this file) - handwritten.
   - `derived/README.md` - handwritten.
   - `docs/README.md` - handwritten header + block copy from the template.
4. **Canonical Russian terms are from the game locale.** Never don’t make this up
   translation If the game says "Highlands" - write "Highlands". Canon
   lives in `derived/canonical_terms.json` (generated from
   `data/locale/{ru,en}/`); writers and compute import it via
   `parser/config.py` (`NATION_NAMES_RU`, `USAGE_RU`, `BUILDING_NAMES_RU`,
   `WEAPON_KIND_RU`, `decode_usage(s, lang='ru')`, `nation_label(sid)`).
5. **Sanity checks.** `parser/build_data.py` runs 112 auto-checks for
   every launch. Any regression after the patch is immediately visible.

<a id="где-что-лежит"></a>
## Where is it?

<a id="код"></a>
### Code

| Folder | Destination |
|---|---|
| `parser/` | Reading game files → JSON (`data.json`, `derived/*.json`). |
| `parser/engine_recon/` | Extractors from `cossacks.exe` (DWS API, primitives, exe-strings). |
| `compute/` | Derived calculations based on JSON → markdown reports in `docs/reports/`. |
| `writers/` | Render canonical help `docs/reference/` + diff between snapshots. |
| `simulator/` | Runtime economic simulator (build orders → timelines). |
| `editor/` | Browser build editor (HTML + JS + Pyodide). |
| `mods/` | Game mods (each - `build.py` patcher + assembly). |
| `scripts/` | Pipeline-runner (`regen.py`). |

<a id="документация"></a>
### Documentation

| Folder | What's inside | Source |
|---|---|---|
| `docs/reference/` | Canonical reference: 7 chapters, 21 nations, 16 comparisons. | Auto-gen (`writers/write_md_tree.py` + `templates/`). |
| `docs/reports/` | Derivative calculations on the topics: combat / economy / tech / map / nations. | Auto-gen (`compute/*.py`). |
| `docs/recon/world/{economy,combat,map}/` + `docs/recon/systems/` | Deep RE of game mechanics, divided by topic. | **Handwritten.** |
| `internals/engine/` | Engine design (Delphi/DWS, RNG, sync, ticks, animation). | **Handwritten** (plus `native_primitives.md` - auto-gen). |
| `internals/scripts/` | Structure `data/scripts/*` (load order, entry points). | **Handwritten.** |
| `internals/data/` | `data/`-game directory: subfolders and file formats. | **Handwritten.** |
| `derived/` | Machine-readable JSON for editor / tools / documentation. | Auto-gen (`parser/*.py`, `parser/engine_recon/*.py`, `compute/compute_game_settings.py`). |
| `docs/known_issues*.md` | Parser gaps, discrepancies, open questions. | **Handwritten.** Archive - `known_issues_archive.md`. |
| `docs/architecture.md` | This file. | **Handwritten.** |

<a id="расширение-pipeline"></a>
## Extending the pipeline

<a id="добавить-новый-отчёт"></a>
### Add a new report

1. Create `compute/compute_<topic>.py` based on its neighbors (`compute_*.py`).
2. Add it to `scripts/regen.py` in the appropriate target (`reports-*`).
3. If the report is associated with one of the 5 ready-made sections
   (`combat / economy / tech / map / nations`) - write to
   `docs/reports/<section>/<name>.md`. If it’s a new section, create a folder and
   add to `docs/reports/README.md`.
4. If the report needs to be shown in [`docs/README.md`](README.md), enter it in
   list (this file is not auto-gen).

<a id="добавить-новый-json-датасет"></a>
### Add a new JSON dataset

1. Create a parser in `parser/parse_<X>.py` or extractor in
   `compute/compute_<X>.py` (if it depends only on `../data.json`).
2. Issue in `derived/<name>.json`.
3. Describe the dataset in `derived/README.md`.
4. Add to `scripts/regen.py` (target `derived` or corresponding
   `reports-*`).

<a id="добавить-нацию-теоретически"></a>
### Add a nation (theoretically)

Not provided: the list of nations is embedded in the game locale (`data/locale/*/units.txt`)
and in `country.script`. After the patch with the new nation we need to expand
`PLAYABLE_NATIONS` to `parser/config.py`, rerun
`parser/build_canonical_terms.py` and `parser/build_data.py`.

<a id="регенерация--порядок-зависимостей"></a>
## Regeneration - dependency order
```
parser/build_data.py            ← reads the game; emits data.json
parser/build_canonical_terms.py ← reads locales; emits canonical_terms.json
parser/parse_animations.py      ← independent (reads .aaf)
parser/parse_generator_cfg.py   ← independent (reads .cfg)
parser/parse_pattern_inventory  ← after parse_generator_cfg
parser/parse_replay_aggregates  ← after parse_pattern_inventory

writers/write_md_tree.py        ← after data.json + canonical_terms.json
compute/compute_*.py            ← after data.json (+ selected derived/*.json)
compute/compute_game_settings   ← independent (reads locales directly)
parser/build_tech_graph.py      ← after data.json (emits tech_tree.json)
compute/compute_tech_tree.py    ← after tech_tree.json (emits Markdown)
compute/validate_map_predictions← after replay_ground_truth + compute_map_resources
simulator/simulate_economy.py   ← after tech_tree.json
```
All dependencies are resolved by `scripts/regen.py` via a declarative list
targets and aliases. Launch:
```bash
python scripts/regen.py all              # complete rebuild
python scripts/regen.py reference        # writers only
python scripts/regen.py reports-combat   # combat reports only
python scripts/regen.py help             # all targets
```
Likewise via `make`: `make all`, `make reports`, `make sanity`, etc.
