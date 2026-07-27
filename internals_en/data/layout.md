<a id="структура-data-в-cossacks-3"></a>
# Structure `data/` in Cossacks 3

What is in each subfolder of the game directory (`Steam/steamapps/
common/Cossacks 3/data/`), what format is there and who parses it.

<a id="сводка"></a>
## Summary

| Folder | Files | Size | What's inside |
|---|---:|---:|---|
| `actors/` | 5 220 | 894 MiB | 3D models of units and buildings (.actor, .tlf, .lib) |
| `animations/` | 282 | 0.5 MiB | Animation tracks (.aaf), libraries (.lib) |
| `brushes/` | 21 | 3.6 MiB | Texture brushes for the map editor |
| `cameras/` | 4 | 7 KiB | Camera Configuration |
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
| `terrain/` | 607 | 685 MiB | Terain tiles (textures by season) |
| `video/` | 1 | 0.1 KiB | (only .lib index - video in DLC) |
| `water/` | 11 | 5 MiB | Water shader assets |

**Total:** ~7.7 GiB. Data = ~94% game size.

<a id="что-нас-интересует-для-парсинга"></a>
## What we are interested in for parsing

Of all 26 folders they actually parse:

- `scripts/` is the main source of truth for gameplay. See
  [`../scripts/structure.md`](../scripts/structure.md).
- `objects/` - per-entity `.parser`-configs (example: each unit
  has a .parser file with behavior and animation settings).
- `animations/` — `.aaf` tracks for frame-accurate timing attacks.
- `pattern/` - binary `.pattern` for generating maps.
- `gen/` — terrainmasks for the seed map system (`gen/terrainmasks/
  land/4pl_*.tga` — ~230 basic masks for 4-player Land).
- `locale/` - text files `.lng` and `.loc` for Russian titles
  units/upgrades.
- `maps/` - ready-made `.map` for Historical Battles (binary).

## scripts/

The most important folder for us. Completely disassembled
[`../scripts/structure.md`](../scripts/structure.md). Key
files:

- `dmscript.global` - global `gc_*` constants (.parser format).
- `dmscript.source` — initial state of global vars.
- `lib/*.script` - 29 DWS libraries (unit, country, ai, gui, ...).
- `units/<sid>/*.parser` - per-unit configs.
- `gui/*.aix` - UI descriptions.

## objects/

Contains `.parser` object configs (1,290 files). Structure:
```
objects/
├── *.objects       Root class configs
├── *.lib           Indexes
├── *.prop          Properties
└── ...
```
Each GameObject class in C3 has a `.objects` config with a list
behavior, animations, materials. Parses the engine via
`ParserLoadFromFile` (native function, available in RTTI).

## animations/

Animation tracks. Files:

- `<sid>.aaf` - Actor Animation File. Contains timings of each
  frame: melee swing point, projectile-spawn frame, footsteps and
  etc.
- `*.acl` - animation cycles libraries.
- `*.library` - index.

Parses in [`../../parser/parse_animations.py`](../../parser/parse_animations.py)
→ [`../../derived/animations.json`](../../derived/animations.json).
1,382 anim tracks from 194 .aaf files.

## pattern/

Binary brushes for placing groups of objects on the map. 711 files.
Used by the map generator.

Completely disassembled
[`../../docs/recon/world/map_generation_pipeline.md`](../../docs_en/recon/world/map/map_generation_pipeline.md)
and
[`../../parser/parse_patterns.py`](../../parser/parse_patterns.py)
→ [`../../derived/pattern_inventory.json`](../../derived/pattern_inventory.json).

## gen/

Map generation pipeline. Contains:

- `gen/terrainmasks/<terrain>/<count>pl_*.tga` - basic masks for
  each terrain type × player count. For example, for Land 4 players
  — ~230 templates in `gen/terrainmasks/land/4pl_*.tga`.
- `gen/*.cfg` — generator.cfg with PatternList → 60 types of patterns.
- `gen/*.bmp` - service bitmaps.

Parses in `parser/parse_generator_cfg.py`.

## locale/

Localization. For each language - a folder with `.lng`/`.loc` files:
```
locale/
├── english/
│   ├── units.txt        Unit and building names
│   ├── upgrades.txt     Upgrade names
│   └── ...
├── russian/
└── ...
```
Parses in `parser/parse_locale.py` → `derived/canonical_terms.json`.
In `data.json`, each name is in the `name_ru` (Russian) field.

## maps/

Ready-made maps (Historical Battles, campaign missions). 68 files,
1.7 GiB. Binary format `.map` - not yet **parsed**. Plans for
There is no parsing either (maps for skirmish are generated procedurally).

## actors/

3D models of units and buildings. 5,220 files, ~900 MiB. Binary
formats:

- `.actor` - model + skeleton + materials.
- `.tlf` — Top-Level Frame (separate animated part).
- `.osm`/`.oss` - internal indexes.

Can't be parsed - we don't work with 3D data.

## materials/

Materials (shaders + textures). 2.9 GiB. `.mat` files configure
binding textures to shaders. `.dds` - actual textures.

## sounds/

Sound effects. OGG format. 330 files, 282 MiB.

## DLC

In addition to `data/`, in the root of the game there is:
```
dlcs/
├── summer/        Summer map (map data only)
└── winter/        Winter map
```
DLC **do not contain** override rules - only additional ones
maps. Units, nations, and upgrades are defined primarily under `data/`.

<a id="что-не-парсится-и-не-планируется"></a>
## What is not parsed (and is not planned)

- 3D models (`actors/`, `materials/`).
- Sprite animations in .actor (used natively by the engine).
- Shaders (`shaders/`).
- Sound (`sounds/`).
- HUD textures (`hud/`).
- Maps (`maps/.map` files).

<a id="где-у-нас-точки-парсинга"></a>
## Where are our parsing points?

| Parser | What does |
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
