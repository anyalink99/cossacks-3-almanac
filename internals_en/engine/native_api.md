<a id="native-api-движка-cossacks-3-delphi--dws"></a>
# Cossacks 3 Engine Native API (Delphi + DWS)

This document reconstructs the native engine layer through static analysis of
`cossacks.exe`, using Python binary parsers rather than Ghidra or IDA.

**TL;DR:** the engine is written in Delphi, the scripting environment is DWS
(DelphiWebScript, open source). Every native primitive visible to scripts is
registered in the executable as a Delphi `AnsiString` containing its Pascal
declaration. These strings can be extracted directly. The resulting catalog
contains **4,856 native signatures**, of which **884 are actually called** from
`data/scripts/*`, giving complete coverage of script-used native primitives.

Related documents:

- [determinism_audit.md](determinism_audit.md) — RNG sources in hot paths.
- [server_sync_architecture.md](server_sync_architecture.md) —
  server-authoritative model C3.
- [ticks_and_subticks.md](ticks_and_subticks.md) — time model.

Machine-readable artifacts:

- `docs/derived/dws_native_signatures.json` - 4,856 signatures (name,
  parameters, return type, RVA in exe).
- `docs/derived/engine_primitives.json` - 884 native + 46 class
  castes + 19 DWS-builtins from scripts.
- `docs/derived/exe_strings.json` — 61,595 ASCII strings and 15,615 Pascal
  `ShortString` values with offsets, for cross-referencing.

<a id="1-методология"></a>
## 1. Methodology

<a id="11-идентификация-движка"></a>
### 1.1. Engine identification

The lines `cossacks.exe` confirm:

| Signature | Meaning |
|---|---|
| `FastMM4 (c) 2004 - 2011 Pierre le Riche` | Delphi memory manager → the executable is built with Delphi, not Free Pascal. |
| `TFormDWSDebugger`, `TFormScriptEvaluate` | Scripts use the open-source DWS (DelphiWebScript) runtime. |
| `TFormStateMachines` | Explicit FSM layer over scripts. |
| `TBitmap3DSx` | The 3DS model loader is built-in. |
| `EId*` exceptions (Indy 10) | The network layer uses the open-source Indy Internet Direct library. |
| `TFormHelloScreen` | UI on standard Delphi VCL/FMX forms. |

<a id="12-извлечение-сигнатур"></a>
### 1.2. Signature extraction

The DWS function is registered in Delphi code as:
```pascal
TdwsUnit.AddFunction(
  'function GetGameObjectPositionXByHandle(gohandle: Integer): Float',
  GetGameObjectPositionXByHandleNative);
```
The declaration is stored as an ordinary static Delphi `AnsiString`. In the
executable, its layout is:
```
... <ref_count = 0xFFFFFFFF> <length: u32> <chars[length]> 00 ...
```
The scanner in `parser/engine_recon/extract_dws_signatures.py` traverses the
binary, searches for the byte pattern
`\xFF\xFF\xFF\xFF<len:4>...\x00`, checks that the string begins with
`function` or `procedure` (allowing a leading space in record members), and
parses it as a Pascal declaration.

This is enough: **100% of script-callable primitives** were found by name.

<a id="2-что-говорят-4-856-сигнатур-про-устройство-движка"></a>
## 2. What 4,856 signatures say about the engine design

<a id="21-ecs-на-handleах"></a>
### 2.1. Handle-based ECS

Most of the API operates on `gohandle: Integer` (a game-object handle) and
`plhandle: Integer` (a player handle). Scripts never receive pointers to native
structures; they use integer handles and paired `Get*ByHandle` /
`Set*ByHandle` functions.

Subsystem size:

| Subsystem | Signatures | Contents |
|---|---:|---|
| `game_object` | 715 | `Get/Set*ByHandle` for GameObject (position, orientation, AABB, ECS flags, anim, materials). |
| `player` | 185 | `Get/SetPlayer*ByHandle` (resources, limits, upgrades, relationships). |
| `scripting` | 85 | `EvaluateCodeThread`, `EvaluateFileThread`, `ParserGet*`, `ParserSet*`. |
| `save_load`/sync | 38 | `RecordCustom*`, `RecordSynch*`, `FileStream*`. |
| `behaviour_props` | 28 | `SetBehaviourBoolProperty`, `BehaviourCreate`, and other game-object component operations. |
| `spawn` | 25 | `Create*ByHandle`, `Destroy*`, `AddObjectToDestroyList`. |
| `ui` | 19 | `AddNewElement*`, `GetGuiTexture*`. |
| `path_command` | 15 | `MoveTo*ByHandle`, `StopOrders*`. |
| `geometry` | 11 | `VectorDistance`, `VectorRotateY`, `ArrayAffineVector*`. |
| `ai` | 10 | `AIRegionDoScanObjects*`. |
| `locale` | 9 | `GetLocaleTable*`. |
| `rng` | 5 | `Random`, `RandomExt`, `SetRandomKey`, etc. |
| `search` | 2 | `FindGameObjectByUniqId`, `FindUniqIdByGameObject`. |

The remaining roughly 3,600 functions fall under `misc`: assets, particles,
sound, rendering, debugging, fog of war, camera control, and regional AI scans.
The large set unused by game scripts belongs mainly to the editor
(`editor.exe` uses the same DWS environment) and the asset pipeline.

<a id="22-server-sync--что-это-такое-технически"></a>
### 2.2. How server synchronization works

In [server_sync_architecture.md](server_sync_architecture.md) we
describes the `bProcess` pattern at a high level. The native API shows how the
state is serialized:

**Low level - `RecordCustom*` (~25 functions):**

| Function | Purpose |
|---|---|
| `RecordCustomBegin{,GUI,Map,StateMachine,TagObject}` | Open a package of the appropriate type. |
| `RecordCustomEnd` | Close the package. |
| `RecordCustomReadBit/Boolean/Byte/Word/SmallInt/Int24/Integer/Float/PackedFloat/ShortString/String/Buffer` | Deserializers by type. |
| `RecordCustomWrite*` (mirror) | Serializers. |
| `RecordCustomBeginReadBitFields` / `EndReadBitFields` | Bit-packed blocks (several bit flags in one byte). |
| `RecordCustomGetReadPackageSize` / `WritePackageSize` | Current package size. |

The supported types reveal features of the network/save packet format:
- `Int24` — a three-byte integer used to reduce traffic.
- `PackedFloat` — a floating-point value packed into fewer bytes (probably scaled
  fixed-point).
- `Bit` plus bit fields — unit flags in a bitstream.
- `ShortString` (Pascal, ≤255 bytes) and dynamic `String` — both
  are supported.

**Mid level - `RecordSynch*` (~30 functions):**

| Function | Purpose |
|---|---|
| `RecordSynchBegin{,GUI,MAP,ByHandle}` | Start synchronizing the specified state area. |
| `RecordSynchIntRegister` / `FloatRegister` / `StringRegister` | Register a slot in the synchronization stack. |
| `RecordSynchStackInt/Float/StringByName` | Synchronize value by name. |
| `RecordSynchStackInt/Float/StringByNameTestChanges` | Synchronize **only if it has changed** - this is delta encoding. |
| `RecordSynchState(name)` | Arbitrary marking of a point. |
| `SetRecordEnabled` / `SetRecordGroupEnabled` / `SetRecordInitializeEnabled` | Recording toggle switches. |

**Conclusion:** C3's server-authoritative synchronization walks through
registered state variables via `RecordSynchStack*ByNameTestChanges` and
transmits **only changed values** in `RecordCustomWrite*` packets. Types such
as `Int24`, `PackedFloat`, and bit fields keep the representation compact, even
in large battles.

`SetRecordInitializeEnabled` selects between an initial full-state snapshot and
delta-only updates.

**Network I/O is not exposed to scripts.** There are no relevant
`Net*`/`Send*`/`Broadcast*` signatures. Everything below
`RecordSynch*`/`RecordCustom*` stays inside `cossacks.exe` (Indy 10 plus the
Steam wrapper).

<a id="23-pathfinding--на-отдельном-потоке"></a>
### 2.3. Pathfinding on separate threads

Found 14 functions `PathDataThread*`:
```pascal
PathDataThreadCount(): Integer;
PathDataThreadResume();
PathDataThreadSuspend();
PathDataThreadSuspended(): Boolean;
PathDataThreadTerminate();
PathDataThreadStaticPriority(val: Integer);
PathDataThreadDynamicPriority(val: Boolean);
PathDataThreadMinPriority(val: Integer);
PathDataThreadMaxPriority(val: Integer);
PathDataThreadDeltaPriority(val: Integer);
PathDataThreadSleepStep(val: Integer);
PathDataThreadSleepLength(val: Integer);
PathDataThreadSafeClean();
```
**Pathfinding in C3 is asynchronous.** Path requests are processed
by a separate thread pool with its own scheduler
(`StaticPriority`/`DynamicPriority`/`MinPriority`/`MaxPriority`,
`DeltaPriority`, `SleepStep`/`SleepLength`).

This changes the determinism model: even with fixed RNG, path-completion order
depends on the operating system's thread scheduler. Resource-gathering results
can therefore differ between runs of the same save on the same host not only
because of RNG, but also because of a **race between pathfinding results**.

The scripting API does not expose separate `Find*` functions for creating path
requests. Instead, scripts issue commands through `Set*ByHandle` functions
(for example, `MoveTo`-style calls); the asynchronous search runs internally,
and the script waits for a later tick.

<a id="24-rng--глубже-чем-мы-думали"></a>
<a id="24-четыре-независимых-хранилища-rng"></a>
### 2.4. Four Independent RNG Seed Stores

`random`, `RandomExt`, and the map generator do not share one state. The
native API exposes **four independent seed stores**, each with its own
algorithm.

> `Random` wraps `System._Random`, which mutates Delphi's standard 32-bit
> `RandSeed`. This state is independent of the extended 64-bit seed controlled
> by `SetRandomKey` and `SetRandomExtKey64`. For the full analysis, see the
> private `cossacks-deep/findings/rng_implementation.md`.

| Storage | Seed functions | Algorithm built on it | Purpose |
|---|---|---|---|
| **Delphi `System.RandSeed`** (32-bit) | `Randomize` or a direct write to `System.RandSeed` (not exposed by DWS) | `Random` (`System._Random`: `seed := seed * 0x8088405 + 1`) | Default gameplay RNG. Not controlled by `SetRandomKey`. |
| **Extended 64-bit seed** | `SetRandomKey(key: Integer)` (32-bit → sign-extend), `SetRandomExtKey64(k0, k1: Integer)` (full 64-bit) | `RandomExt` (64-bit LCG, own pair of constants) | Controlled flow for randomness where determinism through reseeding is needed. |
| **Map-generator seed** | `SetMapGeneratorRandomKey(const randkey0, randkey1)` | Internal generator algorithm (not disassembled) | Isolated RNG for `_DoGenerate` (terrain relief, object placement, starting positions). |
| **Global map-generator seed** | `SetGlobalMapGeneratorRandomKey(const randkey0, randkey1)` | Separate algorithm (not disassembled) | Parallel storage in map-state structures; a candidate for world-map or lobby-preview generation. |

Additionally: `GetPlayerCubeRandomValue(playerhandle: Integer): Float`
— a separate deterministic per-player value, probably used by AI or other
decisions that require a stable player-specific sequence.

There is also a “weather” RNG: `GetAirWeatherRandom`, `SetAirWeatherRandom`,
`GetAirWeatherRandomStart`, `GetAirWeatherRandomEnd`,
`GetAirWindRandom` — an isolated stream for atmospheric effects such as wind
and clouds, preventing visual randomness from consuming gameplay RNG values.

**Implication for the simulator:** reproducing peasant behavior in the
[resource-gathering model](../../docs_en/recon/world/economy/peasant_extraction.md)
requires identifying which `Random*` function each hot-path step calls. A
plain `random` call requires simulation of Delphi's `RandSeed`;
`SetRandomKey + RandomExt` requires the extended seed and its LCG. The
independent map and weather RNG stores do not affect this chain.

<a id="25-поведенческие-компоненты-behaviour"></a>
### 2.5. Behavioral components (Behaviour)

`BehaviourCreate`, `BehaviourCreateWithKey`, `BehaviourDestroy`, and roughly
28 `SetBehaviour*Property` functions show that a unit consists of a game object
plus a set of behavior components. In DWS, a behavior is identified by a class
name string:
```pascal
BehaviourCreate(gohnd: Integer; const classname: String;
                uniq: Boolean; usecurrentparams: Boolean): Integer;
```
The names of `Behaviour*` classes are stored in RTTI and `.parser` files, and
their properties can be transferred through
`BehaviourPropertiesLoadFromParser` / `SaveToParser`. This explains why
`unit.script` can work with concepts such as HP, weapons, animation, and vision
without declaring their fields explicitly: those fields belong to behavior
components.

Of particular interest is `BehaviourInertia*` (apply force/torque/translation,
mirror, surface bounce): built-in **physical simulation of inertia**
for flying or thrown objects, such as cannonballs and galloping cavalry.

<a id="26-ai--региональная-архитектура"></a>
### 2.6. Regional AI architecture

All AI primitives (10 functions) are built around
`AIRegion*`:
```pascal
AIRegionDoScanObjects(const name: String);
AIRegionDoScanObjectsByHandle(const reghnd: Integer);
AIRegionDoScanObjectsExtByHandle(const reghnd: Integer);
AIRegionDoUpdateObject(const reghnd, gohnd: Integer; const notify: Boolean);
AIRegionDoClearObjects/ByHandle(...);
AIRegionFromParserStruct/ToParserStruct(...);
AIRegionLoadFromTextFile/SaveToTextFile(...);
```
**AI operates on spatial regions**: separate areas of interest, each with its
own object list. The AI requests a region update through `DoScanObjects`,
receives the game objects within it, and makes decisions from that set. This
answers the question of how the AI searches for targets.

<a id="27-скриптовая-среда--dws-со-своими-расширениями"></a>
### 2.7. DWS scripting environment and engine extensions

`EvaluateCodeThread(const code: String): Integer` and
`EvaluateFileThread(const filename: String): Integer` show that
DWS scripts can be run in separate threads. This explains
why some script chains, such as campaign logic, appear to run concurrently.

`AddProcAddress` and `PointerOf` extend standard DWS by exposing function
pointers to scripts. This suggests that some gameplay logic, such as script
trigger handlers, is passed as callbacks.

<a id="3-топ-50-самых-частых-нативных-вызовов"></a>
## 3. Top 50 most common native calls

(Generated in `native_primitives.md` nearby, here is a condensed TOP 30 for reference.)

| # | Name | Calls | Purpose |
|---|---|---:|---|
| 1 | `GetPlayerHandleByIndex` | 270 | Get player handle by index. |
| 2 | `GetGameObjectPositionXByHandle` | 263 | X-coordinate of the object. |
| 3 | `GetGameObjectPositionZByHandle` | 263 | Z-coordinate (3D). |
| 4 | `ErrorLog` | 387 | Logging. |
| 5 | `GetLocaleTableListItemById` | 197 | Localization. |
| 6 | `SwitchTo` | 146 | Root scheduler primitive (146 files!). |
| 7 | `VectorDistance` | 137 | Distance between points. |
| 8 | `SetBehaviourBoolProperty` | 127 | Set ECS-property. |
| 9 | `GetPlayerIndexByHandle` | 120 | Inverse mapping. |
| 10 | `ParserGetFloatValueByKeyByHandle` | 115 | Reading from `.parser` file. |
| 11 | `RecordCustomWriteInteger` | 111 | Integer serialization. |
| 12 | `ReadInteger` | 106 | Reading from stream. |
| 13 | `GetGameObjectUniqueIdByHandle` | 95 | Object UID. |
| 14 | `GetGameObjectHandleByUniqueId` | 94 | Inverse. |
| 15 | `GetPlayerGameObjectsCountByHandle` | 89 | Count a player's game objects. |
| 16 | `WriteInteger` | 87 | Write an integer to a stream. |
| 17 | `StrExists` | 86 | Search for a substring. |
| 18 | `SetBehaviourFloatProperty` | 84 | Set ECS-property. |

`SwitchTo` (used in 146 files) acts like `goto state` for state machines.
Together with `TFormStateMachines` in RTTI and `MachineLibrary*` in the API,
this shows that high-level script behavior is organized as finite-state
machines and that `SwitchTo` performs a state transition.

<a id="4-где-хранится-остальное-что-не-в-скриптах"></a>
## 4. Native Functions Not Used by Game Scripts

Of the 4,856 native functions in the executable, game scripts call only 884.
The remaining 3,972 belong to:

- **Editor API** — `AddEditorControl`, `AddEditorFormInput`,
  `AddCameraTrackPoint`, `ResourceTexturesReload`, etc. Used
  in `editor.exe` (separate binary, searches the same DWS environment).
- **Asset/pipeline** – `EnvironmentLoadLensFlareFromFile`,
  `MachineLibrarySaveSerialsToFile`, `ResourceLODActorLibrary*`.
- **Internal-only** — pre-render, low-level TLF (Top-Level Frame)
  and particle-effect operations that scripts do not call.
- **Steam wrapper** — `SteamwrapStartVoiceRecording`,
  `TSteamAchievement` API.
- **Indy network layer** - `TInternetShellClient`, `TInternetShellSession`
  (uses Steam transport, visible in Pascal class names).

For future editor or network-stack analysis, every extracted name and RVA is
available in `dws_native_signatures.json`.

<a id="5-что-закрыто-этим-документом"></a>
## 5. Questions Answered by This Document

| Question | Where was opened | Answer |
|---|---|---|
| What is `bProcess` at the network level | `server_sync_architecture.md` | `RecordSynch*` + `RecordCustom*` - see §2.2. |
| How many RNG streams are in the engine | `determinism_audit.md` | 4 independent: `Random`, `RandomExt`, `MapGenerator`, `GlobalMapGenerator` + weather. §2.4. |
| How AI searches for targets | `ai.md` (TODO) | Via `AIRegionDoScanObjects*` - spatial regions. §2.6. |
| Is pathfinding synchronous or asynchronous? | (open) | **Asynchronous**, with a prioritized thread pool. §2.3. |
| How units are serialized | (open) | `RecordCustom*` with types `Int24`, `PackedFloat`, `Bit-fields`. §2.2. |
| What is the “Behaviour” of a unit | `unit.script` guesses | Full ECS components with `BehaviourCreate(classname: String)`. §2.5. |

<a id="6-что-ещё-открыто--и-как-это-закрыть-без-декомпилятора"></a>
## 6. Remaining Questions and How to Answer Them **Without a Decompiler**

Most of the initially open questions have been closed in related
documents. The current status is:

| Question | Where revealed |
|---|---|
| 6.1. Bit-layout of network packets | ✅ Fully described in [`server_sync_packet_format.md`](server_sync_packet_format.md): `EconomyPackage` (binary, 1–18 bytes), unit-state via parser-text. |
| 6.2. Implementation `Random` LCG | ✅ Fully described in [`rng_implementation.md`](rng_implementation.md): Delphi LCG `X = X × 134775813 + 1 mod 2³²`, plus per-decision deterministic seed pattern. |
| 6.3. Engine class map | ✅ See [`rtti_class_map.md`](rtti_class_map.md): 266 game-engine classes by subsystem, including `TXAIRegion*`, `TXPath*`, `TXTrigger*`, `TXLan*`. |
| 6.4. Peasant resource-search algorithm | 🔬 The logic is in `lib/unit.script:_unit_DoExtract` and related functions. There is no native `findnearestresource`; the search combines the scan grid (see [`target_selection.md`](../../docs_en/recon/world/combat/target_selection.md) §2) with `AIRegionDoScanObjects*` for large areas. It can be traced through scripts without a decompiler. |
| 6.5. Exact pathfinding formula | 🔬 RTTI classes (`TPathData`, `TOSWMovementPath`, `TOSWPathNode`, `TOSWPathNodes`, `TXPathCellChangedArray`; see [`rtti_class_map.md` §4](rtti_class_map.md)) show that pathfinding uses **a graph of nodes**, not a plain A* grid. `TXPathCellChangedArray` recalculates nodes when the map changes. Identifying the exact graph-search algorithm (Dijkstra, A*, or weighted A*) requires decompilation, although runtime characteristics are observable through `PathDataThread*` parameters. |
| 6.6. `MapGenerator` algorithm | 🔬 `TXMapGenerator` (see [`rtti_class_map.md` §8](rtti_class_map.md)) accepts `(randkey0, randkey1)`, two `uint32` values forming 64 bits of state, like `RandomExt` (see [`rng_implementation.md` §3](rng_implementation.md)). The exact internal PRNG cannot be identified without decompilation. This is not critical to reproducibility: the same seed produces the same map. |
| 6.7. `.aix` format (AI configuration) | 🔬 The `.aix` editor is built into `editor.exe` through `TAIXEditor`, `TAIXEditorState`, `TAIXArgsEditor`, and `TAIXVarsEditor` (see [`rtti_class_map.md` §16](rtti_class_map.md)). The binary structure contains variables and arguments. Gameplay AI itself is documented in `lib/ai.script` and the `AIRegion*` API. |
| 6.8. Format `.map` | ❌ Binary, not parsed. Used only for built-in missions (Historical Battle, campaign). Skirmish maps are procedural. See [`../data/file_formats.md`](../data/file_formats.md). |

**Legend:** “🔬” can in principle be answered without a decompiler through
scripts or RTTI; “❌” requires binary reverse engineering.

<a id="7-файлы-и-инструменты"></a>
## 7. Files and tools

| File | Purpose |
|---|---|
| `parser/engine_recon/extract_primitives.py` | Scans `data/scripts/*` → 884 native candidates + 46 type-casts + 19 DWS builtins. |
| `parser/engine_recon/dump_exe_strings.py` | Dump all ASCII (61k) and Pascal ShortString (15k) from `cossacks.exe` with RVA. |
| `parser/engine_recon/extract_dws_signatures.py` | Main: scans the AnsiString table, extracts 4,856 DWS signatures, cross-reference with script → 100% coverage. |

<a id="8-воспроизведение"></a>
## 8. Reproducing the Analysis
```powershell
cd c:\projects\other\cossacks
python parser\engine_recon\extract_primitives.py
python parser\engine_recon\dump_exe_strings.py
python parser\engine_recon\extract_dws_signatures.py
```
Artifacts appear in `derived/*.json` and update the report in
`native_primitives.md` (adjacent file in the same folder).

<a id="9-если-всё-таки-понадобится-декомпилятор"></a>
## 9. If a Decompiler Is Still Needed

`dws_native_signatures.json` contains the RVA of every signature and provides a
starting point for Ghidra, IDR, or IDA:

1. Open `cossacks.exe` in Ghidra with the Delphi plugin (DelphiHelper or
   IDR-import).
2. Go to the desired signature's RVA. A pointer to the native callback should
   be nearby, following the standard Delphi DWS registration pattern.
3. Decompile it. Delphi output is relatively straightforward because it has no
   C++ templates and little aggressive inlining.

Callback names are often available through RTTI: each Delphi class in the
executable contains `vmtTypeInfo` with its published methods. Extending
`dump_exe_strings.py` with a VMT walker could recover roughly 1,779 classes and
their method names. This is a last resort; the existing static analysis covers
about 95% of practical questions.
