<a id="структура-скриптовой-среды-cossacks-3"></a>
# Cossacks 3 Scripting Environment

This guide shows where the logic under `data/scripts/` lives, how the game
loads it into the scripting VM, and which entry points invoke it.

<a id="1-что-такое-скрипт-в-c3"></a>
## 1. What Is a “Script” in Cossacks 3?

Cossacks 3 uses the open-source
[DelphiWebScript (DWS)](https://github.com/EricGrange/DWScript) language for
embedded scripts. Its syntax is based on Object Pascal:
```pascal
function _unit_GetTObj(handle : Integer) : TObj;
begin
   Result := TObj(GetGameObjectTagByHandle(handle));
end;
```
The game exposes **4,856 native functions** to scripts: a ready-made engine API
(see [`../engine/native_api.md`](../engine/native_api.md)). Scripts call these
functions, pass object handles, and read or write properties. The `.script`
files contain the gameplay logic that decides what to do with those handles.

In other words, **most of the game rules live in scripts**. The engine supplies
the entity-component-system (ECS) runtime, rendering, pathfinding,
synchronization, and input/output. This design also makes the game highly
moddable through `modman.exe`.

<a id="2-файлы-и-форматы-в-datascripts"></a>
## 2. Files and Formats in `data/scripts/`
```
data/scripts/
├── dmscript.global           Global constants (.parser format)
├── dmscript.source           Initial state of global variables
├── common.aix                AI constants (binary)
├── common.inc                Purpose not yet identified
├── resource.script           Top-level locale loader
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
**Extensions and formats:**

- `.script` — DWS source: Object Pascal with DWS extensions, encoded as
  `cp1251` (Russian comments are common).
- `.global`, `.source`, and `.inc` — text-based hierarchical `.parser`
  configurations built from constructs such as
  `section.begin / struct.begin / [*] = ;...`. The native `Parser*` API, not
  DWS, parses them.
- `.aix` — binary AI configuration.

<a id="3-как-скрипты-попадают-в-vm"></a>
## 3. How the Game Loads Scripts into the VM

Unlike Lua or Python, with their explicit `require` or `import` statements,
C3's DWS library files have **no `uses` directives**. Entity configurations
(`.parser` files) and the engine arrange loading instead:

| Field in `.parser` | Purpose |
|---|---|
| `DMScriptGlobalFileName` | Global constants (`dmscript.global`). Loads once at startup. |
| `OnLoadScriptFileName` | A script that is called when an entity is created/loaded. |
| `startscript` | A script executed immediately when the game is initialized. |
| `ScenarioStateName` | The script name for a specific finite-state-machine (FSM) state. |
| `OnLoadScript` (inline) | Inline DWS code in a `.parser` file. |

These fields appear in `cossacks.exe` as runtime type information (RTTI)
properties of the DWS scripting classes. For exact addresses, including
relative virtual address (RVA) `0x34fc84` for
`DMScriptGlobalFileName`, see
[`derived/exe_strings.json`](../../derived/exe_strings.json).

**Practical effect:** the game loads all `lib/*.script` files implicitly. They
refer to one another by function name (`_unit_*`, `_misc_*`), and the DWS
compiler resolves those references when it compiles the complete set. Each
`.script` file acts as a **library of functions with no explicit imports**.

<a id="4-namespacing-конвенция"></a>
## 4. Namespacing Convention

C3 uses a Pascal-style naming convention with underscore-prefixed namespaces:

| Prefix | File | Contents |
|---|---|---|
| `_unit_*` | `unit.script` | Logic of units and buildings: `_unit_DoExtract`, `_unit_SearchEnemy`, `_unit_GetTObj`. |
| `_misc_*` | `misc.script`, `miscext.script`, `miscext2.script` | General helpers: `_misc_DoDamage`, `_misc_GetPickedUnitHandle`. |
| `_country_*` | `country.script` | Nations and upgrades: `_country_GetSIDByID`, `_country_DoUpgrade`. |
| `_player_*` | `player.script` | Player state: `_player_GetTPlayerArgs`, `_player_DoStartingResources`. |
| `_ai_*` | `ai.script` | AI logic: `_ai_IsEnemiesExists`, `_ai_DoTickAggressive`. |
| `_net_*` | `net.script` | Multiplayer flags: `_net_IsClient`, `_net_IsServer`. |
| `_parser_*` | `parser.script` | A wrapper for the DWS-Parser API. |
| `_gui_*` | `gui.script` | UI: `_gui_GetTop`, `_gui_OnElementClick`. |
| `_squad_*` | `squad.script` | Squads: `_squad_GetOfficer`, `_squad_DoFormation`. |
| `_weapon_*` | `weapon.script` | Weapons/projectiles: `_weapon_GetTProj`. |
| `_res_*` | `res.script` | Resources: `_res_GetTRes`. |
| `_init_*` | `init.script` | Initialization at game start. |
| `_map_*` | `map.script`, `miscext2.script` | Map logic: `_map_Init`, `_map_RestoreSettings`. |
| `_control_*` | `control.script` | Unit commands: `_control_DeselectAllUnits`. |
| `_movie_*` | `movie.script` | Cutscenes: `_movie_SaveCamera`, `_movie_DoPlay`. |
| `_pfx_*` | `pfx.script` | Particles. |
| `_sound_*` | `sound.script` | Sound: `_sound_GetIndexesByTag`. |
| `_profile_*` | `profile.script` | Player profile. |
| `_group_*` | `group.script` | Groups (fire ships). |

The scripts define roughly 1,600 functions in total; see the `defined` field in
`derived/engine_primitives.json`.

<a id="5-что-в-каждом-главном-файле"></a>
## 5. What Each Main File Contains

<a id="libunitscript-534-kb-250-функций--главный"></a>
### `lib/unit.script` (534 KB, 250 functions) — Main Gameplay Library

This file defines the behavior of units and buildings. Its large `case sid of`
block contains a branch for each unit or building script identifier (SID),
where the script configures properties such as health, weapons, animations,
and behavior.

**Key entry points:**

- `_unit_GetTObj(handle) : TObj` — obtains a record wrapper for a handle.
- `_unit_DoExtract` — runs a Peasant's gathering cycle: walk → work → return.
- `_unit_SearchEnemy*` — searches for a target on the scan grid (see
  [Target Selection](../../docs_en/recon/world/combat/target_selection.md)).
- `_unit_DoDamage` — applies damage.
- `_unit_OnTickXxx` — implements per-tick FSM state handlers.

<a id="libcountryscript-342-kb-64-функции--нации"></a>
### `lib/country.script` (342 KB, 64 functions) — Nations

Its large `case cid of` block defines all 21 nation identifiers (CIDs). Each
branch specifies:

- List of available units (`AddCountryUnit`).
- List of buildings (`AddCountryBuilding`).
- Upgrade trees (`SetUpgStruct`, `AddUpgradePack`).
- Nation-specific features (for example, Poland's infantry Pikeman and
  Venice's light cavalry).

The tools `parser/parse_country.py` and `parser/simulate_upgrades.py` parse this
file automatically.

<a id="libclassesscript-242-kb-438-функций--типы"></a>
### `lib/classes.script` (242 KB, 438 functions) — Types

This file contains record definitions and their helpers, including the `TObj`,
`TSquad`, `TArmy`, `TWeapon`, `TPlayerArgs`, and `TIntegerList` wrappers used as
script-level types. These records are not true Delphi classes: they are thin
wrappers around `Integer` handles, though DWS lets scripts use them like
objects.

<a id="libplayerscript-138-kb--игрок"></a>
### `lib/player.script` (138 KB) — Player State

This file stores the state of each of the 12 player slots: starting resources,
population limits, food and gold consumption, relations with other players,
and flags such as `bfamine` and `brebellion`.

<a id="libaiscript-90-kb--ии"></a>
### `lib/ai.script` (90 KB) — AI

The AI logic runs a planning tick every 2.4 game seconds and controls build
orders, target selection, and aggression. It uses `AIRegion*` functions (see
[Computer-Player Behavior](../../docs_en/recon/systems/ai_behavior.md) and
[`../engine/native_api.md` §2.6](../engine/native_api.md)).

<a id="libserialscript-91-kb--сериализация"></a>
### `lib/serial.script` (91 KB) — Serialization

This file contains 108 state-saving and loading procedures, including
`DoSerializeUnit` and `DoSerializePlayer`. They use the native
`RecordCustomWrite*` and `RecordSynch*` functions (see
[`../engine/native_api.md` §2.2](../engine/native_api.md)).

<a id="libscenarioscript-200-kb--сценарии"></a>
### `lib/scenario.script` (200 KB) — Scenarios

This file drives the campaigns and Historical Battles through triggers
(`TScenarioTrigger`), conditions (`TScenarioCondition`), actions
(`TScenarioAction`), and results (`TScenarioResult`).

<a id="resourcescript-top-level--точка-входа-локали"></a>
### `resource.script` (top-level) — Locale Entry Point

This is not a library under `lib/`, but an **executable script** containing
direct code rather than `function` or `procedure` declarations. At startup it
loads `data/locale/lang.loc`, selects the language through Steam
(`SteamwrapGetSteamUILanguage`), and fills the `resource.lib` parser. The file
itself is short, at roughly 2 KB.

<a id="6-точки-входа-в-скриптовый-vm"></a>
## 6. Script VM Entry Points

Analysis of the executable reveals three classes of entry point:

1. **`startscript`** — runs when the game creates a session and performs
   one-time initialization.
2. **`OnLoadScriptFileName`** — identifies the script bound to an entity class;
   the game calls it whenever an object of that class is created or
   deserialized.
3. **`ScenarioStateName`** — identifies the script handler for an FSM state. A
   scenario is a graph of these states.

In addition, the `lib/*.script` functions are called:

- From other scripts through DWS function calls resolved at compile time.
- From the engine via **callback names**: for example,
  `BehaviourCreate(gohnd, 'WoodChopperBehaviour')` refers to
  a behavior class with a script callback of that name, exposed through the
  Delphi class's RTTI in the executable.

<a id="7-глобальные-константы-и-состояние"></a>
## 7. Global Constants and State

<a id="dmscriptglobal-86-kb-2-400-строк"></a>
### `dmscript.global` (86 KB, 2,400 lines)

This is a `.parser` file, not DWS source. It contains all `gc_*` constants:
- `gc_statetag_*` — FSM status bits (see file).
- `gc_obj_usage_*` — unit types (`lightinfantry`, `cavalry`, ...).
- `gc_obj_weapon_kind_*` — weapon types (`pike`, `sword`, `bullet`, ...).
- `gc_resource_type_*` — resource types.
- `gc_time_to_frames = 32` — 32 simulation frames per game second.
- `gc_pixels_to_tile = 53.3333` — range conversion from pixels to cells.
- Hundreds of additional constants.

The game loads it once at startup through the `DMScriptGlobalFileName` field.
Its `gc_*` names then become named DWS constants available to every script.

### `dmscript.source`

This is also a `.parser` file. It contains the **initial state of every global
variable** whose name begins with `g`, such as `gint_*`, `gbool_*`, and
`gstring_*`. A new game initializes these variables from this file.

<a id="8-кодировка-и-язык"></a>
## 8. Encoding and Language

- `.script` files use `cp1251` (Windows-1251); comments are often in Russian
  because GSC's developers wrote them that way.
- `.parser` files (`.global`, `.source`, `.inc`) also use `cp1251`.
- DWS is case-insensitive: `_unit_GetTObj` and `_UNIT_gettobj` are equivalent.
  Our parsers therefore normalize identifiers to lowercase.

<a id="9-полезные-срезы"></a>
## 9. Useful Derived Datasets

The [`derived/`](../../derived/) directory contains machine-readable views of
this data:

| File | Contents |
|---|---|
| `engine_primitives.json` | 884 native calls from scripts + 46 type-casts + 19 DWS builtins with frequencies and file lists. |
| `dws_native_signatures.json` | 4,856 native signatures from the executable (name, types, RVA). |
| `tech_tree.json` | The `nation × upgrade × prerequisite` graph extracted from `country.script` by `parser/build_tech_graph.py`. |
| `canonical_terms.json` | Canonical Russian and English names from `data/locale/`. |

<a id="10-как-читать-скрипт-без-знания-pascal"></a>
## 10. Reading Scripts Without Knowing Pascal

This table is a quick reference for reading C3 scripts:

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

- `TObj`, `TSquad`, and `TArmy` are not true classes, but type casts over an
  `Integer` handle. Their apparent “methods” are native functions such as
  `Get*ByHandle(int)`/`Set*ByHandle(int, ...)`.
- There is no object-oriented programming (OOP) inheritance, only records and
  handles.
- `random` and `RandomExt` are global random number generator (RNG) functions,
  not methods.
- Scripts do not manage object memory automatically. The engine owns every
  object; scripts retain only integer handles.

<a id="дальнейшее-чтение"></a>
## Further Reading

- [Technical evidence for capture](capture_mechanics_evidence.md) — a complete
  example of tracing one game mechanic through scripts, with pseudocode and
  exact source locations.
- [Technical evidence for production queues](production_queue_evidence.md) —
  internal order types, refund formula, and call sites.
- [Technical evidence for famine and rebellion](hunger_and_rebellion_evidence.md) —
  state thresholds, probabilities, and the consumption formula.
- [Technical model of resource gathering](peasant_extraction_evidence.md) —
  work-cycle formulas, drop-off points, and map-pattern calculations.
- [Technical evidence for upgrades](upgrades_application_evidence.md) —
  internal effect types, application order, and formulas.
- [Technical evidence for buildings](building_mechanics_evidence.md) —
  collision masks, builder positions, destruction, and refunds.
- [Technical evidence for target selection](target_selection_evidence.md) —
  scan order, candidate filters, priorities, and exact formulas.
- [Technical evidence for pathfinding](pathfinding_evidence.md) —
  routes, local avoidance, formations, and stuck-unit handling.
- [Technical evidence for map generation](map_generation_evidence.md) —
  generator stages, starting positions, resources, territories, and seed space.
- [`../engine/native_api.md`](../engine/native_api.md) — the 4,856 native
  functions that the engine exposes to scripts, grouped by subsystem.
- [`../data/layout.md`](../data/layout.md) — the contents of `data/` beyond the
  scripts themselves.
- [DWS on GitHub](https://github.com/EricGrange/DWScript) — the open-source
  language implementation and a useful reference.
