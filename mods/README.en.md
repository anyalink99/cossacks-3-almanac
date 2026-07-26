# Cossacks 3 mods

**English** · [Русский](README.md)

Folder for mods developed in this repository. Each mod is a separate subfolder named mod. Mods edit game scripts through the script mod-loader C3 (`mods/`, `mods.ini`, `modman.exe`) - without DLL injection and without editing `cossacks.exe`.

<a id="текущие-моды"></a>
## Current mods

| Mod | What does | Status |
|---|---|---|
| [Deterministic Cossacks](Deterministic%20Cossacks/) | Replaces 10 `random` in hot-path mining and combat with deterministic `SetRandomKey + random` for reproducible mining and the same combat outcomes for Save/Load and multiplayer | working, awaiting empirical validation |

<a id="конвенция-структуры-мода"></a>
## Convention structure mod

Each mod in `mods/<Mod Name>/` looks like:
```
mods/<Mod Name>/
├── README.md          ← rationale, installation, test protocol, limitations
├── build.py           ← patcher: reads <game>/data/, applies patches, emits the mod directory
├── .gitignore         ← at minimum: build/, __pycache__/
├── src/
│   └── mod.ini        ← metadata template for the C3 mod loader (not Steam Workshop)
└── build/             ← generated build output, ignored by Git
    └── <Mod Name>/
        ├── mod.ini
        └── data/...   ← mirrors the <game>/data/ structure
```
`build.py` imports `parser.config` for the canonical game path (`COSSACKS3_PATH` env var → default Steam path). This gives a single point of configuration between the parser and the mods.

<a id="как-добавить-новый-мод"></a>
## How to add a new mod

1. Copy `Deterministic Cossacks/` as a template, rename it.
2. In `build.py`, update `MOD_NAME` and the list `PATCHES` (each patch - `file`, `name`, `expected_line`, `original`, `replacement`).
3. In `src/mod.ini`, update `title`, `description`, `contentfolder`.
4. In `README.md` describe what is being patched and why, with links to recon documents that justify the changes.
5. Run `python "mods/<Mod Name>/build.py"` - the patcher will check that all `original` lines are unique in the files.
6. Install via `--install` or manually (see mod README).

<a id="совместимость-с-патчами-игры"></a>
## Compatible with game patches

Mods copy **entire files** from `<game>/data/scripts/lib/` (250-560 KB each), because C3 mod-loader does not know how to patch individual functions - it only overrides entire files. This means:

- After updating the game, `lib/{misc,unit}.script` may receive new lines → the old version of the mod will **overwrite** them back to the pre-update.
- `build.py` uses **exact text match** for each patch site, not line numbers. If the line remains unchanged, the patch will be found even if the number is shifted. If the line has changed, `build.py` crashes with the error `original line not found`, and the mod must be updated manually.
- Workflow after the game patch: `python parser/build_data.py` (check that the data is parsed) → `python "mods/<Mod>/build.py"` (rebuild). If it crashes, update the `original` lines in the patches.

<a id="совместимость-нескольких-модов"></a>
## Compatibility of several mods

If two mods patch **different** files (e.g. `misc.script` and `weapon.script`) - they get along. If the **same** file - the last one loaded into `mods.ini` wins (this is monitored by the C3 mod-loader). Current situation: only one mod, no problem yet.
