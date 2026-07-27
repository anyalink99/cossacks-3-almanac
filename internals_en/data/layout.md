<a id="структура-data-в-cossacks-3"></a>
# The `data/` Directory in Cossacks 3

This page describes each subfolder under
`Steam/steamapps/common/Cossacks 3/data/`, the formats it contains, and
the repository tools that parse it.

<a id="сводка"></a>
## Summary

| Folder | Files | Size | What's inside |
|---|---:|---:|---|
| `actors/` | 5 220 | 894 MiB | 3D models of units and buildings (.actor, .tlf, .lib) |
| `animations/` | 282 | 0.5 MiB | Animation tracks (.aaf), libraries (.lib) |
| `brushes/` | 21 | 3.6 MiB | Texture brushes for the map editor |
| `cameras/` | 4 | 7 KiB | Camera configuration |
| `cursors/` | 23 | 100 KiB | Cursors (.cur, .bmp) |
| `env/` | 92 | 9 MiB | Environment (sky, fog, lighting presets) |
| `game/` | 11 | 1.9 MiB | Gameplay configs (.cfg) |
| `gen/` | 4,571 | 164 MiB | **Map generator**: pattern masks, terrainmasks, region templates |
| `gui/` | 139 | 2.4 MiB | UI elements (.aix, .cfg, .inc) |
| `hud/` | 180 | 153 MiB | HUD textures (icons, buttons) |
| `images/` | 22 | 6.3 MiB | Loading screens, etc. |
| `locale/` | 2,187 | 20 MiB | Localization into 7+ languages |
| `maps/` | 68 | 1.7 GiB | Prebuilt maps (`.map`, `.aix`) |
| `materials/` | 866 | 2.9 GiB | Materials and textures (`.mat`, `.dds`) |
| `objects/` | 1,290 | 3.4 MiB | Per-unit/building `.parser`-configs (see below) |
| `pattern/` | 711 | 60 MiB | **Pattern files** for placing objects on the map (binary .pattern) |
| `pfx/` | 26 | 47 MiB | Particles (fire, smoke, dust) |
| `posteffects/` | 3 | 5 KiB | Post-process shaders |
| `projects/` | 1 | 0.3 KiB | (official) |
| `resources/` | 4 | 46 KiB | `resource.lib` (local), `resource.dat` |
| `scripts/` | 222 | 4.3 MiB | **DWS scripts + .parser configs** (see [`../scripts/structure.md`](../scripts/structure.md)) |
| `shaders/` | 109 | 0.3 MiB | GLSL shaders (.vert, .frag) |
| `sounds/` | 330 | 282 MiB | OGG sounds + configs |
| `terrain/` | 607 | 685 MiB | Terrain tiles (textures by season) |
| `video/` | 1 | 0.1 KiB | `.lib` index only; video is supplied by DLC |
| `water/` | 11 | 5 MiB | Water shader assets |

**Total:** about 7.7 GiB, roughly 94% of the installed game.

<a id="что-нас-интересует-для-парсинга"></a>
## Data used by the parsers

The extraction pipeline uses these folders:

- `scripts/` is the main source of truth for gameplay. See
  [`../scripts/structure.md`](../scripts/structure.md).
- `objects/` — per-entity `.parser` configurations, including behavior and
  animation settings.
- `animations/` — `.aaf` tracks for frame-accurate attack timing.
- `pattern/` — binary `.pattern` map-generation templates.
- `gen/` — terrainmasks for the seed map system (`gen/terrainmasks/
  land/4pl_*.tga` — ~230 basic masks for 4-player Land).
- `locale/` — `.lng` and `.loc` text files containing canonical unit and
  upgrade names.
- `maps/` — prebuilt binary `.map` files for Historical Battles.

## scripts/

This is the main source of gameplay rules. Its layout is documented in
[`../scripts/structure.md`](../scripts/structure.md). Key files:

- `dmscript.global` — global `gc_*` constants in `.parser` format.
- `dmscript.source` — initial state of global vars.
- `lib/*.script` — 29 DWS libraries covering units, nations, AI, UI, and
  other systems.
- `units/<sid>/*.parser` — per-unit configurations.
- `gui/*.aix` — UI descriptions.

## objects/

Contains `.parser` object configs (1,290 files). Structure:
```
objects/
├── *.objects       Root class configs
├── *.lib           Indexes
├── *.prop          Properties
└── ...
```
Each Cossacks 3 `GameObject` class has an `.objects` configuration listing
its behaviors, animations, and materials. The engine loads these files
through the native `ParserLoadFromFile` function.

## animations/

Animation tracks. Files:

- `<sid>.aaf` - Actor Animation File. Contains timings of each
  frame, including melee impact, projectile spawning, and footsteps.
- `*.acl` — animation-cycle libraries.
- `*.library` — indexes.

Parsed by [`../../parser/parse_animations.py`](../../parser/parse_animations.py)
→ [`../../derived/animations.json`](../../derived/animations.json).
The output contains 1,382 animation tracks from 194 `.aaf` files.

## pattern/

Binary brushes for placing groups of objects on the map. 711 files.
Used by the map generator.

The format is documented in
[`Random-map generation`](../../docs_en/recon/world/map/map_generation_pipeline.md)
and parsed by
[`../../parser/parse_patterns.py`](../../parser/parse_patterns.py)
→ [`../../derived/pattern_inventory.json`](../../derived/pattern_inventory.json).

## gen/

Map generation pipeline. Contains:

- `gen/terrainmasks/<terrain>/<count>pl_*.tga` - basic masks for
  each terrain type × player count. For example, for Land 4 players
  — ~230 templates in `gen/terrainmasks/land/4pl_*.tga`.
- `gen/*.cfg` — generator.cfg with PatternList → 60 types of patterns.
- `gen/*.bmp` — auxiliary bitmaps.

Parsed by `parser/parse_generator_cfg.py`.

## locale/

Each language has a folder containing `.lng` and `.loc` files:
```
locale/
├── english/
│   ├── units.txt        Unit and building names
│   ├── upgrades.txt     Upgrade names
│   └── ...
├── russian/
└── ...
```
Parsed by `parser/parse_locale.py` into `derived/canonical_terms.json`.
In `data.json`, Russian names are stored in `name_ru`.

## maps/

Prebuilt maps for Historical Battles and campaign missions: 68 files,
1.7 GiB in total. The binary `.map` format is not parsed, and current
work does not require it because skirmish maps are generated procedurally.

## actors/

3D models of units and buildings. 5,220 files, ~900 MiB. Binary
formats:

- `.actor` - model + skeleton + materials.
- `.tlf` — Top-Level Frame (separate animated part).
- `.osm`/`.oss` - internal indexes.

The repository does not parse them because its generated datasets do not
use 3D assets.

## materials/

Materials and textures occupy 2.9 GiB. `.mat` files bind textures to
shaders; `.dds` files contain the texture images.

## sounds/

Sound effects. OGG format. 330 files, 282 MiB.

## DLC

The game root also contains:
```
dlcs/
├── summer/        Summer map (map data only)
└── winter/        Winter map
```
These DLC directories contain additional maps rather than gameplay-rule
overrides. Units, nations, and upgrades are defined primarily under `data/`.

<a id="что-не-парсится-и-не-планируется"></a>
## What is not parsed (and is not planned)

- 3D models (`actors/`, `materials/`).
- Sprite animations in .actor (used natively by the engine).
- Shaders (`shaders/`).
- Sound (`sounds/`).
- HUD textures (`hud/`).
- Maps (`maps/.map` files).

<a id="где-у-нас-точки-парсинга"></a>
## Parser entry points

| Parser | Output |
|---|---|
| [`../../parser/parse_units.py`](../../parser/parse_units.py) | `lib/unit.script` → unit and building records. |
| [`../../parser/parse_country.py`](../../parser/parse_country.py) | `lib/country.script` → nations and roster. |
| [`../../parser/simulate_upgrades.py`](../../parser/simulate_upgrades.py) | `lib/country.script` inline `SetUpgStruct`/`AddUpgradePack` → 4,000 lines of upgrades. |
| [`../../parser/parse_animations.py`](../../parser/parse_animations.py) | `animations/*.aaf` → frame-accurate timing. |
| [`../../parser/parse_patterns.py`](../../parser/parse_patterns.py) | `pattern/*.pattern` → binary placement patterns. |
| [`../../parser/parse_generator_cfg.py`](../../parser/parse_generator_cfg.py) | `gen/generator.cfg` → 60 pattern types. |
| [`../../parser/parse_locale.py`](../../parser/parse_locale.py) | `locale/<lang>/*.txt` → canonical Russian names. |
| [`../../parser/build_data.py`](../../parser/build_data.py) | Collects everything in `docs/data.json`. |
| [`../../parser/engine_recon/*.py`](../../parser/engine_recon/) | `cossacks.exe` → `derived/dws_native_signatures.json`. |
