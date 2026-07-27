<a id="форматы-файлов-в-data"></a>
# File formats in `data/`

A quick reference to binary and text formats that
found in `data/`. For each - an indication of our parser
(if any) and briefly the essence.

## `.script` – DWS source

Text in `cp1251`, Object Pascal syntax with DWS extensions. See
[`../scripts/structure.md`](../scripts/structure.md) - there is a complete
information about structure and parsing.

<a id="parser--global--source--inc--текстовый-конфиг"></a>
## `.parser` / `.global` / `.source` / `.inc` - text config

Hierarchical key-value format, native parser in exe. Used
in:

- `data/scripts/dmscript.global` - global `gc_*` constants.
- `data/scripts/dmscript.source` — initial state of global vars.
- `data/scripts/units/<sid>/<sid>.parser` - unit config.
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
- `ParserCreate(name : String) : Integer` — create parser-handle.
- `ParserLoadFromFile(filename : String) : Boolean` - load from disk.
- `ParserSelectByHandleByKey(parserhnd, key : String) : Integer` - navigation by key.
- `ParserGetIntValueByKeyByHandle(parserhnd, key : String) : Integer`,
  `ParserGetFloatValueByKeyByHandle`, `ParserGetValueByKeyByHandle` - reading.
- `ParserSetIntValueByKeyByHandle` (and analogues) - record.

Our code contains direct regex parsers
(`parser/parse_country.py`, `parser/parse_units.py`) - we do not
We emulate the native parser completely, only the subsets we need.

## `.aaf` – Actor Animation File

Text (in `data/animations/aaf/*.aaf`) describing the animation
unit/building tracks. Each track is a range of frames.

<a id="структура"></a>
### Structure
```
"walk", 1, 24,
"attack0", 32, 46,
"workfood", 278, 299,
...
```
Format: `"track_name", start_frame, end_frame`. 1 frame = 1/32 game
seconds (`gc_time_to_frames = 32`).

<a id="парсер-1"></a>
### Parser

[`parser/parse_animations.py`](../../parser/parse_animations.py) →
[`derived/animations.json`](../../derived/animations.json). 1 382
track from 194 .aaf files. Used to calculate real DPS:
`melee_swing_sec(sid)` takes the impact point in the attack frames and translates
in g-seconds.

<a id="pattern--бинарный-шаблон-размещения"></a>
## `.pattern` - binary placement template

“Stamp” brushes for the map generator: forest, rock formations, fields,
scenery groups. 711 files in `data/pattern/`.

<a id="формат"></a>
### Format

Complete disassembly at the beginning
[`parser/parse_patterns.py`](../../parser/parse_patterns.py). Briefly:
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

100% of files are parsed. Used in calibration
[`compute/compute_map_resources.py`](../../compute/compute_map_resources.py)
to estimate the number of trees on the map.

<a id="tga--truevision-targa-терреин-маски"></a>
## `.tga` – TrueVision Targa (terrein masks)

Standard 24/32-bit Targa format. In C3 it is used for
Terrain masks of the map generator:

- `data/gen/terrainmasks/<terrain>/<n>pl_*.tga` - for each type
  landscape × number of players. ~230 basic for Land 4-player.

It is not parsed by us (only the engine is used).

<a id="bmp--windows-bitmap"></a>
## `.bmp` - Windows Bitmap

Standard BMP. Used for:

- `data/gen/*.bmp` — service bitmaps of the generator.
- `data/brushes/*.bmp` - editor brushes.

Doesn't work for us.

<a id="dds--directdraw-surface-текстуры"></a>
## `.dds` - DirectDraw Surface (textures)

Standard DDS format (DXT-compressed textures). In `data/materials/`
and `data/terrain/`. Doesn't parse.

<a id="actor--tlf--3d-модели"></a>
## `.actor` / `.tlf` - 3D models

Binary format of the GSC engine. 3D meshes, skeletons, materials. Not
dismantled by us and is not planned (we do not work with 3D data).

<a id="lib--индексы--манифесты"></a>
## `.lib` - indexes / manifests

Universal GSC wrapper format. Contains a list of resources and
pointers to them. For example:
- `data/animations/animations.lib` - index of anim files.
- `data/actors/*.lib` — model index (with meta).

We don’t disassemble it - we bypass it directly via `rglob('*.aaf')`, etc.

<a id="aix--бинарный-ai-конфиг"></a>
## `.aix` - binary AI config

Used in:
- `data/scripts/common.aix` - general AI constants.
- `data/maps/*.aix` - AI configs for built-in maps.
- `data/gui/*.aix` - UI configs.

The format is not parsed as a byte structure, but **the editor is built into
`editor.exe`** through classes `TAIXEditor`, `TAIXEditorState`,
`TAIXArgsEditor`, `TAIXVarsEditor` (see
[`../engine/rtti_class_map.md` §16](../engine/rtti_class_map.md)).
By name, this is a “variables + arguments” structure. Accurate
bytes - only decompilation of RTTI methods of these classes.

Not critical for gameplay: AI logic is described in `lib/ai.script` and
via `AIRegion*`-API (see [`../engine/native_api.md` §2.6](../engine/native_api.md)).

<a id="lng--loc--локализация"></a>
## `.lng` / `.loc` - localization

`.loc` - text “hierarchical” format, analogue of `.parser`:
```
language begin
   russian begin
      muskrussia18 = Мушкетёр (Russia, XVIII в.)
      ...
   end;
end;
```
`.lng` - wrapper for `.loc` (old format, inherited from Cossacks 1).

<a id="парсер-3"></a>
### Parser

[`parser/parse_locale.py`](../../parser/parse_locale.py) →
[`derived/canonical_terms.json`](../../derived/canonical_terms.json) and
fields `name_ru` to `data.json`.

<a id="ogg--snd--звук"></a>
## `.ogg` / `.snd` - sound

Standard OGG Vorbis. `.snd` - index. They don't parse.

<a id="map--готовые-карты-historical-battles"></a>
## `.map` — prebuilt maps for Historical Battles

GSC binary format. 68 files in `data/maps/`. Not disassembled -
Skirmish maps are generated procedurally, so the `.map` format is not suitable for us
needed.

## `.rep` / `.map` (skirmish saves) — OSWMap13

See separate document [`replay_format.md`](replay_format.md) - there
full description of header, BMP preview, kv settings, entry stream
(time-stamped net-packets) and the directory `Read*`-handlers with
decoded formats.

<a id="cfg--текстовые-конфиги"></a>
## `.cfg` - text configs

Simple `key = value` format. In `data/game/*.cfg`,
`data/cameras/*.cfg`, `data/sounds/*.cfg`. Parsed by regex
place of use.

<a id="сводка-что-мы-парсим-vs-что-нет"></a>
## Summary: what we parse vs what we don't

| Format | Parsim | Where | Why |
|---|---|---|---|
| `.script` | ✓ | parser/parse_units.py, country.py, simulate_upgrades.py | The main source of truth is gameplay. |
| `.parser` (units) | ✓ | parser/parse_units.py (regex) | Properties of units and buildings. |
| `.aaf` | ✓ | parser/parse_animations.py | Frame-precise timing of attacks. |
| `.pattern` | ✓ | parser/parse_patterns.py | Object placement templates. |
| `.tga` (terrainmasks) | (indirectly) | compute/compute_map_resources.py | Map resource calibration. |
| `.lng`/`.loc` | ✓ | parser/parse_locale.py | Russian names. |
| `.cfg` (generator) | ✓ | parser/parse_generator_cfg.py | PatternList → 60 types. |
| Replay (`.gold`?) | ✓ | parser/parse_replay.py | Sniff replay file for validation. |
| `.actor` / `.tlf` / `.dds` | ✗ | — | We don't need 3D data. |
| `.aix` (AI) | ✗ | — | AI is described in scripts, the binary is not critical. |
| `.map` | ✗ | — | Skirmish maps are generated procedurally. |
