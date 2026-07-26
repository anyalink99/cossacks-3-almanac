<a id="структура-скриптовой-среды-cossacks-3"></a>
# Structure of the Cossacks 3 scripting environment

Where is the logic in `data/scripts/`, how do the files get into
script VM, what are their entry points.

<a id="1-что-такое-скрипт-в-c3"></a>
## 1. What is a “script” in C3

Cossacks 3 uses **DWS** (DelphiWebScript, open-source:
[github.com/EricGrange/DWScript](https://github.com/EricGrange/DWScript))
as an embedded scripting language. Syntax - Object Pascal:
```pascal
function _unit_GetTObj(handle : Integer) : TObj;
begin
   Result := TObj(GetGameObjectTagByHandle(handle));
end;
```
The game provides scripts with **4,856 native functions** - a ready-made API
to the engine (see [`../engine/native_api.md`](../engine/native_api.md)).
Scripts call them, pass object handles, read and write
properties. The gameplay logic itself (what to do with these handles) -
lives in `.script` files.

This means: **most of the “rules of the game” are in the scripts**, and the engine
provides ECS-runtime, render, pathfinding, sync and I/O. This
makes the game very moddable (mod loader `modman.exe`).

<a id="2-файлы-и-форматы-в-datascripts"></a>
## 2. Files and formats in `data/scripts/`
```
data/scripts/
├── dmscript.global           Global constants (.parser format)
├── dmscript.source           Initial state of global variables
├── common.aix                AI constants (binary)
├── common.inc                ?
├── resource.script           Top level: load locale
├── env/env.inc               Environment variables
├── lib/                      29 .script files — logic libraries
│   ├── unit.script           (534 KB) — unit and building behavior
│   ├── country.script        (342 KB) — nations, upgrades, roster
│   ├── classes.script        (242 KB) — record types and helpers
│   ├── miscext2.script       (198 KB) — advanced miscellaneous helpers
│   ├── misc.script           (237 KB) — common helpers
│   ├── gui.script            (162 KB) — UI logic
│   ├── player.script         (138 KB) — player state
│   ├── ai.script             ( 90 KB) — AI behavior
│   ├── serial.script         ( 91 KB) — serialization
│   ├── weapon.script         ( 66 KB) — weapons/projectiles
│   ├── miscext.script        ( 70 KB)
│   ├── movie.script          ( 45 KB) — cutscenes
│   ├── scenario.script       (200 KB) — scenarios and campaign
│   ├── control.script        ( 27 KB) — selection/commands
│   ├── steam.script          ( 27 KB) — Steam wrapper
│   ├── sound.script          ( 26 KB)
│   ├── profile.script        ( 26 KB)
│   ├── squad.script          ( 23 KB) — squads
│   ├── ui.script             ( 22 KB)
│   ├── pfx.script            ( 17 KB) — particles
│   ├── res.script            ( 12 KB) — resources
│   ├── map.script            ( 11 KB)
│   ├── miscext3.script       ( 10 KB)
│   ├── init.script           ( 10 KB) — initialization
│   ├── scenarioeditor.script ( 10 KB)
│   ├── net.script            (  6 KB) — multiplayer state
│   ├── group.script          (  5 KB)
│   ├── parser.script         (  2 KB) — DWS Parser wrapper
├── misc/                     Additional .inc files
├── progress/progress.inc
├── units/<sid>/              Per-unit `.parser` configs
├── user/user.inc
└── env/env.inc
```
**Extensions and format:**

- `.script` - DWS source. Object Pascal with DWS extensions.
  Encoding `cp1251` (Russian commentary is common).
- `.global`, `.source`, `.inc` — `.parser`-format (text
  hierarchical config with `section.begin / struct.begin / [*] = ;...`).
  It is not parsed by DWS, but by the native `Parser*` API.
- `.aix` - binary AI config.

<a id="3-как-скрипты-попадают-в-vm"></a>
## 3. How scripts get into the VM

Unlike Lua/Python with explicit `require/import`, DWS in C3 does not have **
`uses` directives in library files**. Loading occurs via **configs
entities** (`.parser` files) and engine:

| Field in .parser | What does |
|---|---|
| `DMScriptGlobalFileName` | Global constants (`dmscript.global`). Loads once at startup. |
| `OnLoadScriptFileName` | A script that is called when an entity is created/loaded. |
| `startscript` | A script executed immediately when the game is initialized. |
| `ScenarioStateName` | The script name for a specific FSM script state. |
| `OnLoadScript` (inline) | Inline-DWS code in .parser. |

All these fields are found in `cossacks.exe` as RTTI properties of DWS classes
scripts (RVA `0x34fc84` for `DMScriptGlobalFileName`, etc., see
[`derived/exe_strings.json`](../../derived/exe_strings.json) if
we need exact addresses).

**Practical effect:** all `lib/*.script` are loaded implicitly - they
refer to each other through function names (`_unit_*`, `_misc_*`),
and the DWS compiler resolves references at the time the entire set is compiled.
Each `.script` is a **unit library of functions with no explicit imports**.

<a id="4-namespacing-конвенция"></a>
## 4. Namespacing convention

C3 uses Pascal-style namespace via underscores:

| Prefix | File | Contents |
|---|---|---|
| `_unit_*` | `unit.script` | Logic of units and buildings: `_unit_DoExtract`, `_unit_SearchEnemy`, `_unit_GetTObj`. |
| `_misc_*` | `misc.script`, `miscext.script`, `miscext2.script` | General helpers: `_misc_DoDamage`, `_misc_GetPickedUnitHandle`. |
| `_country_*` | `country.script` | Nations, upgrades: `_country_GetSIDByID`, `_country_DoUpgrade`. |
| `_player_*` | `player.script` | Player status: `_player_GetTPlayerArgs`, `_player_DoStartingResources`. |
| `_ai_*` | `ai.script` | AI logic: `_ai_IsEnemiesExists`, `_ai_DoTickAggressive`. |
| `_net_*` | `net.script` | Multiplayer flags: `_net_IsClient`, `_net_IsServer`. |
| `_parser_*` | `parser.script` | A wrapper for the DWS-Parser API. |
| `_gui_*` | `gui.script` | UI: `_gui_GetTop`, `_gui_OnElementClick`. |
| `_squad_*` | `squad.script` | Squads: `_squad_GetOfficer`, `_squad_DoFormation`. |
| `_weapon_*` | `weapon.script` | Weapons/projectiles: `_weapon_GetTProj`. |
| `_res_*` | `res.script` | Resources: `_res_GetTRes`. |
| `_init_*` | `init.script` | Initialization at game start. |
| `_map_*` | `map.script`, `miscext2.script` | Card logic: `_map_Init`, `_map_RestoreSettings`. |
| `_control_*` | `control.script` | Unit commands: `_control_DeselectAllUnits`. |
| `_movie_*` | `movie.script` | Cut scenes: `_movie_SaveCamera`, `_movie_DoPlay`. |
| `_pfx_*` | `pfx.script` | Particles. |
| `_sound_*` | `sound.script` | Sound: `_sound_GetIndexesByTag`. |
| `_profile_*` | `profile.script` | Player profile. |
| `_group_*` | `group.script` | Groups (fire ships). |

In total, ~1,600 functions are defined in scripts (see.
`derived/engine_primitives.json` field `defined`).

<a id="5-что-в-каждом-главном-файле"></a>
## 5. What's in each main file

<a id="libunitscript-534-kb-250-функций--главный"></a>
### `lib/unit.script` (534 KB, 250 functions) - main

Behavior of all units and buildings. Contains huge `case sid of`
block: for each side unit/building ID - the corresponding
branch with setting properties (HP, weapon, animations, behaviors).

**Key Points:**
- `_unit_GetTObj(handle) : TObj` — get a record wrapper from handle.
- `_unit_DoExtract` - peasant booty, FSM walk → work → return.
- `_unit_SearchEnemy*` — search for a target in scan-grid (see.
  [`docs/recon/world/target_selection.md`](../../docs_en/recon/world/combat/target_selection.md)).
- `_unit_DoDamage` - application of damage.
- `_unit_OnTickXxx` - per-tick FSM state handlers.

<a id="libcountryscript-342-kb-64-функции--нации"></a>
### `lib/country.script` (342 KB, 64 functions) - nations

Large `case cid of`-block for 21 nations. For each:

- List of available units (`AddCountryUnit`).
- List of buildings (`AddCountryBuilding`).
- Wood upgrades (`SetUpgStruct`, `AddUpgradePack`).
- Features (for example, Pol has an infantry pikeman, Ven has light cavalry).

Parses automatically in `parser/parse_country.py` and
`parser/simulate_upgrades.py`.

<a id="libclassesscript-242-kb-438-функций--типы"></a>
### `lib/classes.script` (242 KB, 438 functions) - types

Record definitions and their helpers. Contains wrappers `TObj`, `TSquad`,
`TArmy`, `TWeapon`, `TPlayerArgs`, `TIntegerList`, etc. - everything that
scripts are used as types. These records are not real Delphi-classes
(these are “thin” wrappers around the `Integer` handle), but through DWS they
behave like objects.

<a id="libplayerscript-138-kb--игрок"></a>
### `lib/player.script` (138 KB) - player

The condition of one of the 12 players. Starting resources, population limits,
food/gold consumption, relationships with other players, flags
`bfamine`/`brebellion`.

<a id="libaiscript-90-kb--ии"></a>
### `lib/ai.script` (90 KB) - AI

AI enemy: tick every 2.4 g-sec, build order, target selection
aggression. Uses `AIRegion*` (see
[`docs/recon/systems/ai_behavior.md`](../../docs_en/recon/systems/ai_behavior.md)
and [`../engine/native_api.md` §2.6](../engine/native_api.md)).

<a id="libserialscript-91-kb--сериализация"></a>
### `lib/serial.script` (91 KB) - serialization

Saving and loading state. 108 type procedures
`DoSerializeUnit`, `DoSerializePlayer`. Uses native
`RecordCustomWrite*`/`RecordSynch*` (see
[`../engine/native_api.md` §2.2](../engine/native_api.md)).

<a id="libscenarioscript-200-kb--сценарии"></a>
### `lib/scenario.script` (200 KB) - scripts

Campaign and Historical Battles. Triggers (`TScenarioTrigger`),
conditions (`TScenarioCondition`), actions (`TScenarioAction`),
results (`TScenarioResult`).

<a id="resourcescript-top-level--точка-входа-локали"></a>
### `resource.script` (top-level) - locale entry point

Not in `lib/`. Not a library, but an **executable script** (without `function/
procedure`-deflarations, direct code). Loads at startup
`data/locale/lang.loc`, selects language via Steam (`SteamwrapGetSteamUILanguage`),
fills `resource.lib` parser. See the file itself - it is short (~2 KB).

<a id="6-точки-входа-в-скриптовый-vm"></a>
## 6. Entry points to the script VM

Three classes of entry points were found from the exe analysis:

1. **`startscript`** - script executed when creating a session.
   Used for one-time initialization.
2. **`OnLoadScriptFileName`** - script bound to the class
   essence. Called every time creation/deserialization occurs
   object of this class.
3. **`ScenarioStateName`** - script handler for one FSM state.
   Scenario = graph of such states.

In addition, the `lib/*.script` functions are called:

- From other scripts via DWS function-call (compile-time linking).
- From the engine via **callback names**: for example,
  `BehaviourCreate(gohnd, 'WoodChopperBehaviour')` refers to
  Behavior class that has a script callback with this
  name (via RTTI Delphi class in exe).

<a id="7-глобальные-константы-и-состояние"></a>
## 7. Global constants and state

<a id="dmscriptglobal-86-kb-2-400-строк"></a>
### `dmscript.global` (86 KB, 2,400 lines)

In `.parser` format (not DWS!). Contains ALL `gc_*` constants:
- `gc_statetag_*` — FSM status bits (see file).
- `gc_obj_usage_*` - unit types (`lightinfantry`, `cavalry`, ...).
- `gc_obj_weapon_kind_*` - weapon types (`pike`, `sword`, `bullet`, ...).
- `gc_resource_type_*` - resource types.
- `gc_time_to_frames = 32` - frames in game seconds.
- `gc_pixels_to_tile = 53.3333` - range conversion.
- And hundreds of others.

Loads once at startup via
`DMScriptGlobalFileName`-field. After this, `gc_*` names are available as
named DWS constants in all scripts.

### `dmscript.source`

Also `.parser` format. Contains **initial state of all
global vars** (names starting with `g`: `gint_*`, `gbool_*`,
`gstring_*`). When you start a new game, everything is initialized from here.

<a id="8-кодировка-и-язык"></a>
## 8. Encoding and language

- `.script` - `cp1251` (Windows-1251). Comments are often in Russian
  (Russian developer GSC).
- `.parser` (`.global`, `.source`, `.inc`) - also `cp1251`.
- DWS case-insensitive: `_unit_GetTObj` and `_UNIT_gettobj`
  are equivalent (important for our parsing - we lowercase everything).

<a id="9-полезные-срезы"></a>
## 9. Useful cuts

All this data is available natively in [`derived/`](../../derived/):

| File | What contains |
|---|---|
| `engine_primitives.json` | 884 native calls from scripts + 46 type-casts + 19 DWS builtins with frequencies and file lists. |
| `dws_native_signatures.json` | 4,856 native signatures from exe (name, types, RVA). |
| `tech_tree.json` | Graph `nation × upgrade × prerequisite`, squeezed from `country.script` via `parser/build_tech_graph.py`. |
| `canonical_terms.json` | Canonical Russian names from `data/locale/`. |

<a id="10-как-читать-скрипт-без-знания-pascal"></a>
## 10. How to read a script without knowledge of Pascal

Shortcut for reading C3 scripts:

| DWS/Pascal | Equivalent in C-style |
|---|---|
| `:=` | `=` |
| `=` | `==` |
| `<>` | `!=` |
| `var x : Integer = 0;` | `int x = 0;` |
| `begin ... end;` | `{ ... }` |
| `if cond then begin ... end else begin ... end;` | `if (cond) { ... } else { ... }` |
| `for i := 0 to N-1 do begin ... end;` | `for (int i=0; i<N; i++) { ... }` |
| `case x of 1: ... ; 2: ... ; else ... end;` | `switch (x) { case 1: ... break; case 2: ... break; default: ... }` |
| `function F(a : Integer) : Boolean;` | `bool F(int a)` |
| `procedure P(a : Integer);` | `void P(int a)` |
| `Result := value;` | `return value;` (but without explicit return) |
| `TObj(handle).hp` | `((TObj*)handle)->hp` (thin type-cast) |

**Subtleties of C3 scripts:**

- `TObj`/`TSquad`/`TArmy` are NOT real classes, but type-casts
  above `Integer` handle. All “methods” are native functions
  `Get*ByHandle(int)`/`Set*ByHandle(int, ...)`.
- No OOP inheritance. There are only records and handles.
- `random` and `RandomExt` are global RNG functions, not methods.
- There is no automatic memory - all “objects” live in the engine,
  The script only holds Integer-handles.

<a id="дальнейшее-чтение"></a>
## Further reading

- [`../engine/native_api.md`](../engine/native_api.md) - what the engine provides to scripts (4,856 native functions, divided into subsystems).
- [`../data/layout.md`](../data/layout.md) - what is in `data/`, next to the scripts.
- [DWS on GitHub](https://github.com/EricGrange/DWScript) - open-source implementation of the language, can be read as a reference.
