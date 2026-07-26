# `parser/` - extract data from the game

**English** · [Русский](README.md)

The scripts in this folder do **parsing only**: read `.script`/`.global` Cossacks 3 files
and collect a single JSON snapshot in `data.json`. All scripts are idempotent: after
game patch, you restart the pipeline - all artifacts are updated.

Derivative calculations, writers and the simulator live in adjacent folders:
[`../compute/`](../compute/), [`../writers/`](../writers/), [`../simulator/`](../simulator/).

Inside the parser:
- [`engine_recon/`](engine_recon/) - extractors from `cossacks.exe` (DWS native API,
  primitives, exe-strings); write to `../derived/` directly and feed [`../internals/`](../internals_en/).
- [`debug/`](debug/) - dev scripts for debugging parsing steps.

## Pipeline
```
              ┌───────────────────────────┐
              │  Game files (Steam)       │
              │  data/scripts/lib/*.script│
              │  data/scripts/dmscript.*  │
              │  data/locale/<lang>/*.txt │
              └──────────────┬────────────┘
                             │
                             ▼
                ┌─────────────────────────┐
                │  parser/build_data.py   │  ← extracts EVERYTHING
                │  (orchestrator)         │
                └────┬────────────────────┘
                     │
                     ▼
              ┌──────────────────┐
              │  data.json       │  ← single source of truth (~4.7 MB, top-level)
              └────┬─────────────┘
                   │
   ┌───────────────┼─────────────────────────┐
   ▼               ▼                         ▼
writers/        compute/                  simulator/
write_md_tree   compute_scaling           simulate_economy
                compute_map_resources
                compute_tech_tree
                compute_construction_times

  parser/engine_recon/ → ../derived/{dws_native_signatures, engine_primitives, exe_strings}.json
                       (feeds internals/engine/*; independent of data.json)
```
## Files (`parser/`)

### Parsers (input: game files; output: JSON-friendly dicts)

| File | What does |
|---|---|
| **`config.py`** | Paths, table of 21 nations, mappings (cluster→prefix, usage_short, upg_type, speed_table). `GAME_ROOT` is taken from the env variable `COSSACKS3_PATH` (fallback is the standard Steam path). |
| **`extract_constants.py`** | Parsit `dmscript.global` → `{gc_name: {raw, value}}`. ~1463 constants. |
| **`parse_locale.py`** | UTF-8 / CP1251 auto-detect; templates `%nat%`/`%com%`/`%include%`. EN+RU. |
| **`parse_country.py`** | Recursive-descent Pascal parser. Retrieves the per-nation roster (members, upgrades, fixed_produces) via simulation `if (aus)`/`case cid` for each of the 21 nations. Inline `_country_InitUnitsUpgrades`. |
| **`parse_units.py`** | Text-based balanced-block walker. Parser `_unit_InitBase` - three case blocks (units / common buildings / per-nation buildings) with per-nation / per-cluster overrides. |
| **`simulate_upgrades.py`** | Symbolic Pascal executor for `_country_InitUnitsUpgrades` and `_country_Init`. Tracks `member`/`upgplace`, inline `SetUpgStruct*` + `AddUpgradePack`, deploys `for i:=1 to 3 do` (mine upgrades). Issue ~3000 fully-resolved upgrade rows. |

### Replay tools

| File | What does |
|---|---|
| **`parse_replay.py`** | Parses OSWMap13 header/footer, lobby settings, players and `PatternList`. In `--json` returns the exact `n/x/y` coordinates of placed patterns and map metadata from the footer. |
| **`parse_replay_events.py`** | Decodes the entry/sub-package stream into a JSON timeline of commands and state-sync events. |
| **`parse_replay_aggregates.py`** | Builds aggregates according to the replay catalog for empirical verification of the format. |
| **`replay_to_build_order.py`** | Converts decoded events into a construction/production sequence. |

### Orchestrator (input: parsers; output: single dict)

| File | What does |
|---|---|
| **`build_data.py`** | Calls all parsers, merges them into a single `dict`, adds the versioned stamp, market rates, officers, sanity_checks (112 auto-statements). Saves to `data.json`. |

## How to launch

### After the game patch (full regeneration)

All commands are from the project root:
```bash
python parser/build_data.py                   # → data.json (source of truth)
python writers/write_md_tree.py               # → docs/reference/ + docs/README.md
python compute/compute_scaling.py             # → docs/reports/economy/scaling_prices.md
python compute/compute_map_resources.py       # → docs/reports/map/map_resources.md
python parser/build_tech_graph.py             # → derived/tech_tree.json
python compute/compute_tech_tree.py           # → docs/reports/tech/tech_tree.md + production_rates.md
python compute/compute_construction_times.py  # → docs/reports/economy/construction_times.md
```
More convenient - one runner: `python scripts/regen.py all` (full circle ~4 min)
or dotted `python scripts/regen.py reports-economy` / `reference` / `derived`.

All writer/compute scripts read only from `data.json` (except `compute/compute_map_resources.py`,
which also goes into game files for map gen densities). Therefore, it is enough to update once
data.json - then writers are executed in <30 seconds in total.

### Diff between snapshots
```bash
python parser/build_data.py                                       # current
cp data.json /tmp/data_old.json
# … patch the game …
python parser/build_data.py                                       # new
python writers/diff_snapshots.py /tmp/data_old.json data.json
```
## Sanity checks

`build_data.py` prints the result of **112 autochecks** at the end:
- 10 checks for `gc_*` constants (time_to_frames=32, hits_needed_*, base portions)
- 5 checks for counts (≥21 nations, ≥410 buildings, ≥750 units, ≥4000 upgrades)
- 21 building counts checks for each nation (≥15 buildings)
- 49 checks for the presence of Town Hall + Barracks 17c for each nation
- 4 mine upgrade chain checks (5+5+8+10+12+15+40 = 95 workers, total cost 104550 food + 80950 gold)
- 15 checks specific units (Strelet/Janissary/Vityaz unique, Strelet HP=50 dmg=9 range=15.0t weaponsid=SHOTMUSKET)
- 4 trained_in mappings checks
- 3 checks of market default rates
- 1 check pixels_to_tile=53.33

After the game patch, regressions in the data will be visible through `FAIL` in this list.

## Parser architecture

### Approach

Pascal game scripts are **executable code**, not data. To extract parameters,
we do **symbolic execution**: parse in AST, evaluate conditions (`if (aus)`,
`case cid of _aus`) for each nation separately, inline auxiliary procedures
(`SetUpgStructFoodGold`, `AddUpgradePack`).

### Key tricks

1. **Pre-substitution** (`_presubstitute`): csid → 'aus', commonName → 'eur',
   blacksmith → 'ausbla', tmptype → ctypeProtection. Done per-nation **before** parsing.

2. **Class/record/object/type keyword recognition**: without them `extract_proc_body`
   terminates at `type T = class … end;` and returns a stub of the procedure.

3. **Pascal-to-Python operator translation**: `<>` → `!=`, `=` → `==`. Without this
   `if (member<>'')` is always True (eval falls, fallback to True), and is issued
   false upgrades.

4. **For-loop unrolling**: `for i := 1 to 3 do … case i of 1:'gol'; 2:'iro'; 3:'coa'`
   unfolds in 3 iterations. Used for mine upgrades.

5. **Last-write-wins dedup**: matches the behavior of the game (`_country_AddUpgrade`
   with the same sid overwrites the previous one).

## Output directories

- [`../docs/README.md`](../docs_en/README.md) - directory index for the player
  (reference, recon, reports).
- [`../derived/README.md`](../derived/README.en.md) - JSON dataset directory
  (including engine-RE dumps from `parser/engine_recon/`).
- [`../internals/README.md`](../internals_en/README.md) - technical
  documentation of the engine / scripts / `data/`-directory.
