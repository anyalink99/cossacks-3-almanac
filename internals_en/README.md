<a id="internals--техническое-устройство-cossacks-3"></a>
# Cossacks 3 Internals

**English** · [Русский](../internals/README.md)

This folder is **not a player's guide**. It documents the game's internal
structure: the engine executable, the DWS scripting environment, the `data/`
directory, and file formats. Game statistics, comparisons, and explanations
of player-visible mechanics are in the
[encyclopedia](../docs_en/README.md).

This includes everything that:

- describes the engine (`cossacks.exe`) — Delphi, DWS, Indy, and FastMM4;
- maps the script structure (`data/scripts/*`) — each file's responsibility
  and how the files call one another;
- describes the formats and location of files in `data/` (`.parser`,
  `.pattern`, `.aaf`, locales, map generation);
- explains implementation details where `docs_en/recon/` describes only
  player-visible behavior.

<a id="структура"></a>
## Structure

| Section | What's inside |
|---|---|
| [engine/](engine/) | Executable structure, scripting VM, networking model, ticks, and random-number generation. |
| [scripts/](scripts/) | The layout and load order of `data/scripts/*`, with the entry points exposed by each file. |
| [data/](data/) | The `data/` directory: subfolders and formats such as `.parser`, `.pattern`, and `.aaf`. |
| [project/](project/) | Repository architecture, documentation rules, research plans, and known limitations. |

## engine/

These documents are based on static analysis of `cossacks.exe`. The extraction
scripts parse the executable directly with Python rather than relying on Ghidra
or IDA project files.

| File | What's inside |
|---|---|
| [engine/native_api.md](engine/native_api.md) | Main document. **4,856 native DWS signatures** (name, argument types, RVA), extracted directly from the executable through the `AnsiString` pattern `\xFF\xFF\xFF\xFF<len><chars>\x00`. Covers all 884 primitives called by game scripts. Subsystems include `game_object`, `player`, `save_load`, and `path_command`. |
| [engine/native_primitives.md](engine/native_primitives.md) | Machine-generated quick search: top 50 + 10 examples per subsystem. |
| [engine/rtti_class_map.md](engine/rtti_class_map.md) | A subsystem map of **1,779 Delphi classes** in the executable: `TXGameObject`, `TXBehaviour*` (22 classes), `TXAIRegion*` (5), `TXPath*` / `TPathData` (6), `TXTrigger*` (8), `TXStateMachine*` (9), `TXLan*` (8 multiplayer classes), `TXMapGenerator`, `TXPattern*` (25), `TAIX*` (4 editor `.aix` classes), and others. |
| [engine/determinism_audit.md](engine/determinism_audit.md) | RNG audit: which random-number functions appear in resource gathering and combat, what survives save/load, and what a deterministic mod can change. |
| [engine/rng_implementation.md](engine/rng_implementation.md) | Implementation of `Random` (Delphi LCG `X = X × 134775813 + 1 mod 2³²`, uses `System.RandSeed`) and `RandomExt` (64-bit LCG over a **separate** extended seed, which is set via `SetRandomKey`/`SetRandomExtKey64`). Main pattern: per-decision deterministic seed. RE-validated via private `cossacks-deep`. |
| [engine/server_sync_architecture.md](engine/server_sync_architecture.md) | The server-authoritative networking model, synchronization periods, network modes, and the `bProcess` pattern. |
| [engine/server_sync_packet_format.md](engine/server_sync_packet_format.md) | Network-packet layouts: binary `EconomyPackage` records (1–18 bytes) and parser-text unit-state snapshots. |
| [engine/ticks_and_subticks.md](engine/ticks_and_subticks.md) | Real time, game time, frames, the main progress loop, and sub-tick state-machine intervals (135 ms for peasants and 100 ms for units). |
| [engine/animation_system.md](engine/animation_system.md) | Animation system: `.aaf` format (1,382 tracks) and `.acl` (FSM cycle graph), `refspeed.acl` (movement speeds by class), `OnAclAnimationReachedAttack` callback (impact moment), `_unit_ApplyWeaponCost` / `ApplyAttackPause`, RNG filter for gunshot sounds. |
| [engine/script_modding_constraints.md](engine/script_modding_constraints.md) | Practical limits of script mods: what DWS scripts can change, what belongs in game data, and where engine constraints take over. |

## scripts/

The structure of `data/scripts/*`: where each subsystem lives, how files are
loaded, and which entry points they expose.

| File | What's inside |
|---|---|
| [scripts/structure.md](scripts/structure.md) | Load order, main `.script` files and their purpose, entry points into the scripting environment. |

<a id="технические-приложения-к-игровым-механикам"></a>
### Technical appendices for game mechanics

| Topic | Appendices |
|---|---|
| Economy and construction | [Resource gathering](scripts/peasant_extraction_evidence.md), [construction and repair](scripts/building_mechanics_evidence.md), [capture](scripts/capture_mechanics_evidence.md), [upgrades](scripts/upgrades_application_evidence.md), [famine and rebellion](scripts/hunger_and_rebellion_evidence.md), [production queues](scripts/production_queue_evidence.md) |
| Combat and movement | [Target selection](scripts/target_selection_evidence.md), [pathfinding](scripts/pathfinding_evidence.md) |
| Map | [Random-map generation](scripts/map_generation_evidence.md) |

## data/

The contents of `data/`: directories, formats, and parsing rules.

| File | What's inside |
|---|---|
| [data/layout.md](data/layout.md) | A directory-by-directory guide to the 26 subfolders under `data/`. |
| [data/file_formats.md](data/file_formats.md) | File formats: `.parser` (text configs), `.pattern` (brush maps), `.aaf` (animations), `.tga`/`.dds` (textures). |
| [data/game_fields_glossary.md](data/game_fields_glossary.md) | Glossary of internal fields found in `data.json` and game scripts. |
| [data/nation_deviations.md](data/nation_deviations.md) | Technical fingerprints for national building and unit variants. |
| [data/map_predictions_validation.md](data/map_predictions_validation.md) | Replay-based calibration of the map-resource model. |
| [data/replay_format.md](data/replay_format.md) | The `OSWMap13` replay and save format: header, entries, command packets, and state synchronization. |

<a id="чем-это-отличается-от-docsrecon"></a>
## How this differs from `docs_en/recon/`

| `docs_en/recon/` (for players) | `internals_en/` (for developers and modders) |
|---|---|
| “How many mines will I have at the start?” | "In what order does `dmscript.source` initialize the global state?" |
| “Why can two saved games produce different outcomes?” | “Which linear congruential generator backs Delphi's `Random`, and which systems consume each RNG stream?” |
| “How do units move in formation?” | “How does the pathfinding thread pool interact with the script tick?” |

The boundary is practical: native function names, binary formats, and
byte-level executable details belong here. Game values and behavior observable
during a match belong in [`docs_en/`](../docs_en/).

<a id="связанные-машинные-дампы"></a>
## Related machine dumps

All JSON datasets generated from these documents or from a binary are in
[`../derived/`](../derived/):

- `dws_native_signatures.json` — 4,856 native signatures (see [engine/native_api.md](engine/native_api.md)).
- `engine_primitives.json` — 884 native + 46 type-casts from scripts.
- `exe_strings.json` — 61,000 ASCII strings and 15,000 Pascal
  `ShortString` values extracted from the executable.
- Other datasets (`game_settings`, `tech_tree`, `builder_slots`, and so on)
  support the player-facing reference.

<a id="инструменты"></a>
## Tools

All extractors are in [`../parser/engine_recon/`](../parser/engine_recon/):
```powershell
python parser\engine_recon\extract_primitives.py     # → derived/engine_primitives.json
python parser\engine_recon\dump_exe_strings.py       # → derived/exe_strings.json
python parser\engine_recon\extract_dws_signatures.py # → derived/dws_native_signatures.json
                                                     # + internals/engine/native_primitives.md
```
