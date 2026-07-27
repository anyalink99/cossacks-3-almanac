<a id="форматы-файлов-в-data"></a>
# File formats in `data/`

A quick reference to the binary and text formats found under `data/`.
Each section summarizes the format and identifies the repository parser,
where one exists.

## `.script` – DWS source

CP1251-encoded text written in Object Pascal syntax with DWS extensions.
See [`../scripts/structure.md`](../scripts/structure.md) for the full
script layout and parsing notes.

<a id="parser--global--source--inc--текстовый-конфиг"></a>
## `.parser` / `.global` / `.source` / `.inc` - text config

A hierarchical key-value format read by the native parser in the
executable. It is used in:

- `data/scripts/dmscript.global` — global `gc_*` constants.
- `data/scripts/dmscript.source` — initial state of global vars.
- `data/scripts/units/<sid>/<sid>.parser` — unit configuration.
- `data/objects/*.parser` — config classes of objects.
- `data/gen/generator.cfg` — map generator parameters.

<a id="синтаксис"></a>
### Syntax
```
section.begin
   Code : struct.begin
      [*] = ;gc_ResCount = 7;
      [*] = ;gc_statetag_essential_none = 1 shl 0;
      ...
   end;
end;
```
Or a simpler form (objects):
```
gameobject begin
   classname = "Peasant"
   hp = 50
   actor = "actors/peasant.actor"
end;
```
<a id="парсер"></a>
### Parser

Native functions in exe (see [`../engine/native_api.md`](../engine/native_api.md)):
- `ParserCreate(name : String) : Integer` — create a parser handle.
- `ParserLoadFromFile(filename : String) : Boolean` — load a file from disk.
- `ParserSelectByHandleByKey(parserhnd, key : String) : Integer` — navigate by key.
- `ParserGetIntValueByKeyByHandle(parserhnd, key : String) : Integer`,
  `ParserGetFloatValueByKeyByHandle`, `ParserGetValueByKeyByHandle` — read values.
- `ParserSetIntValueByKeyByHandle` and its counterparts — write values.

The repository uses direct regular-expression parsers in
`parser/parse_country.py` and `parser/parse_units.py`. They implement only
the subsets required by the project rather than emulating the native parser
in full.

## `.aaf` – Actor Animation File

Text files under `data/animations/aaf/` that describe unit and building
animation tracks. Each track spans a range of frames.

<a id="структура"></a>
### Structure
```
"walk", 1, 24,
"attack0", 32, 46,
"workfood", 278, 299,
...
```
Format: `"track_name", start_frame, end_frame`. One frame equals 1/32 of
a game second (`gc_time_to_frames = 32`).

<a id="парсер-1"></a>
### Parser

[`parser/parse_animations.py`](../../parser/parse_animations.py) →
[`derived/animations.json`](../../derived/animations.json). The output
contains 1,382 tracks from 194 `.aaf` files. It supports frame-accurate DPS
calculations: `melee_swing_sec(sid)` converts the impact frame within an
attack animation to game seconds.

<a id="pattern--бинарный-шаблон-размещения"></a>
## `.pattern` - binary placement template

Stamp-like templates used by the map generator for forests, rock
formations, fields, and scenery groups. There are 711 files under
`data/pattern/`.

<a id="формат"></a>
### Format

The format is fully decoded in
[`parser/parse_patterns.py`](../../parser/parse_patterns.py). In brief:
```
offset    layout
0         u32 width                  // mask width in tile corners
4         u32 height                 //
8         u8[w*h] mask               // object-placement bitmask
8+C       f32[w*h] heightmap         // hilliness
...       padding
...       rec[cells] (24 bytes)     // for each occupied cell:
                                     //   u32 variant_id, f32 scale_x/y/z,
                                     //   f32 reserved, u32 flags
...       u8[cells*16] reserved
```
<a id="парсер-2"></a>
### Parser

[`parser/parse_patterns.py`](../../parser/parse_patterns.py) +
[`parser/parse_pattern_inventory.py`](../../parser/parse_pattern_inventory.py)
→ [`derived/pattern_inventory.json`](../../derived/pattern_inventory.json),
[`derived/pattern_types.json`](../../derived/pattern_types.json),
[`derived/pattern_type_stats.json`](../../derived/pattern_type_stats.json).

All files are parsed. The results calibrate
[`compute/compute_map_resources.py`](../../compute/compute_map_resources.py)
to estimate the number of trees on the map.

<a id="tga--truevision-targa-терреин-маски"></a>
## `.tga` – TrueVision Targa (terrain masks)

Standard 24- or 32-bit Targa images. Cossacks 3 uses them as terrain masks
for the map generator:

- `data/gen/terrainmasks/<terrain>/<n>pl_*.tga` — one set for each terrain
  type and player count. The four-player Land set contains about 230 base
  masks.

The repository does not parse the image data directly.

<a id="bmp--windows-bitmap"></a>
## `.bmp` - Windows Bitmap

Standard BMP. Used for:

- `data/gen/*.bmp` — auxiliary generator bitmaps.
- `data/brushes/*.bmp` — editor brushes.

The repository does not parse these files.

<a id="dds--directdraw-surface-текстуры"></a>
## `.dds` - DirectDraw Surface (textures)

Standard DDS images with DXT-compressed textures, found under
`data/materials/` and `data/terrain/`. The repository does not parse them.

<a id="actor--tlf--3d-модели"></a>
## `.actor` / `.tlf` - 3D models

A proprietary GSC engine format containing 3D meshes, skeletons, and
materials. Decoding it is outside the project's scope because the generated
datasets do not use 3D assets.

<a id="lib--индексы--манифесты"></a>
## `.lib` - indexes / manifests

A general GSC container format holding resource lists and references. For
example:
- `data/animations/animations.lib` — animation-file index.
- `data/actors/*.lib` — model index (with meta).

The extractors bypass these manifests by scanning for the underlying files
directly, for example with `rglob('*.aaf')`.

<a id="aix--бинарный-ai-конфиг"></a>
## `.aix` - binary AI config

Used in:
- `data/scripts/common.aix` — shared AI constants.
- `data/maps/*.aix` — AI configurations for built-in maps.
- `data/gui/*.aix` — UI configurations.

The format is not parsed as a byte structure, but **the editor is built into
`editor.exe`** through classes `TAIXEditor`, `TAIXEditorState`,
`TAIXArgsEditor`, `TAIXVarsEditor` (see
[`../engine/rtti_class_map.md` §16](../engine/rtti_class_map.md)).
The class names indicate a variables-and-arguments structure. Recovering
the exact byte layout would require decompiling their RTTI methods.

The byte layout is not required for the current gameplay analysis: AI logic
is available in `lib/ai.script` and through the `AIRegion*` API (see
[`../engine/native_api.md` §2.6](../engine/native_api.md)).

<a id="lng--loc--локализация"></a>
## `.lng` / `.loc` - localization

`.loc` is a hierarchical text format similar to `.parser`:
```
language begin
   russian begin
      muskrussia18 = Мушкетёр (Russia, XVIII в.)
      ...
   end;
end;
```
`.lng` is a wrapper for `.loc`, inherited from the first Cossacks.

<a id="парсер-3"></a>
### Parser

[`parser/parse_locale.py`](../../parser/parse_locale.py) →
[`derived/canonical_terms.json`](../../derived/canonical_terms.json) and
the `name_ru` fields in `data.json`.

<a id="ogg--snd--звук"></a>
## `.ogg` / `.snd` - sound

Standard OGG Vorbis audio. `.snd` files are indexes. The repository does not
parse either format.

<a id="map--готовые-карты-historical-battles"></a>
## `.map` — prebuilt maps for Historical Battles

A proprietary GSC binary format used by 68 files in `data/maps/`. The
repository does not decode it because skirmish maps are generated
procedurally and the current datasets do not require prebuilt map contents.

## `.rep` / `.map` (skirmish saves) — OSWMap13

See [`replay_format.md`](replay_format.md) for the header, BMP preview,
key-value settings, timestamped network-packet stream, and catalog of
decoded `Read*` handlers.

<a id="cfg--текстовые-конфиги"></a>
## `.cfg` - text configs

A simple `key = value` format used under `data/game/`, `data/cameras/`,
and `data/sounds/`. Call sites parse the required values with regular
expressions.

<a id="сводка-что-мы-парсим-vs-что-нет"></a>
## Summary: what we parse vs what we don't

| Format | Parsed | Where | Why |
|---|---|---|---|
| `.script` | ✓ | parser/parse_units.py, country.py, simulate_upgrades.py | Primary source of gameplay rules. |
| `.parser` (units) | ✓ | parser/parse_units.py (regex) | Properties of units and buildings. |
| `.aaf` | ✓ | parser/parse_animations.py | Frame-precise timing of attacks. |
| `.pattern` | ✓ | parser/parse_patterns.py | Object placement templates. |
| `.tga` (terrainmasks) | (indirectly) | compute/compute_map_resources.py | Map resource calibration. |
| `.lng`/`.loc` | ✓ | parser/parse_locale.py | Russian names. |
| `.cfg` (generator) | ✓ | parser/parse_generator_cfg.py | PatternList → 60 types. |
| Replay (`.gold`?) | ✓ | parser/parse_replay.py | Read replay files for validation. |
| `.actor` / `.tlf` / `.dds` | ✗ | — | We don't need 3D data. |
| `.aix` (AI) | ✗ | — | AI is described in scripts, the binary is not critical. |
| `.map` | ✗ | — | Skirmish maps are generated procedurally. |
