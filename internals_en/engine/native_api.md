<a id="native-api-движка-cossacks-3-delphi--dws"></a>
# Native API of the Cossacks 3 engine (Delphi + DWS)

Reverse engineering of the native engine layer through static analysis
`cossacks.exe` - without Ghidra/IDA, only binary parsing in Python.

**TL;DR:** the engine is written in Delphi, the scripting environment is DWS
(DelphiWebScript, open-source). Every native primitive that is a script
sees as a function, registered in exe as Delphi `AnsiString` with
Pascal declaration signature string. These lines can be extracted
directly - we received **4,856 native signatures**, of which **884
are actually called** from `data/scripts/*` (100% coverage
script-callable primitives).

Related documents:

- [determinism_audit.md](determinism_audit.md) - RNG sources in hot
  ways.
- [server_sync_architecture.md](server_sync_architecture.md) —
  server-authoritative model C3.
- [ticks_and_subticks.md](ticks_and_subticks.md) - time model.

Machine-readable artifacts:

- `docs/derived/dws_native_signatures.json` - 4,856 signatures (name,
  parameters, return type, RVA in exe).
- `docs/derived/engine_primitives.json` - 884 native + 46 class
  castes + 19 DWS-builtins from scripts.
- `docs/derived/exe_strings.json` - 61,595 ASCII + 15,615 Pascal
  ShortString with offsets (if ever needed for xref).

<a id="1-методология"></a>
## 1. Methodology

<a id="11-идентификация-движка"></a>
### 1.1. Engine identification

The lines `cossacks.exe` confirm:

| Signature | What does this mean |
|---|---|
| `FastMM4 (c) 2004 - 2011 Pierre le Riche` | Delphi memory manager → binary exactly Delphi (not FreePascal). |
| `TFormDWSDebugger`, `TFormScriptEvaluate` | Scripts - DWS (DelphiWebScript). Open-source, github.com/EricGrange/DWScript. |
| `TFormStateMachines` | Explicit FSM layer over scripts. |
| `TBitmap3DSx` | The 3DS model loader is built-in. |
| `EId*` exceptions (Indy 10) | The network part is Indy Internet Direct, also open-source. |
| `TFormHelloScreen` | UI on standard Delphi VCL/FMX forms. |

<a id="12-извлечение-сигнатур"></a>
### 1.2. Signature extraction

The DWS function is registered in Delphi code as:
```pascal
TdwsUnit.AddFunction(
  'function GetGameObjectPositionXByHandle(gohandle: Integer): Float',
  GetGameObjectPositionXByHandleNative);
```
The declaration line is regular Delphi `AnsiString` (static,
runtime-immutable), which in `.exe` is:
```
... <ref_count = 0xFFFFFFFF> <length: u32> <chars[length]> 00 ...
```
The scanner at `parser/engine_recon/extract_dws_signatures.py` passes
binary, looks for byte pattern `\xFF\xFF\xFF\xFF<len:4>...\x00`, checks
that the line begins with `function` or `procedure` (adjusted for
leading space in the record part) and parses it as a Pascal declaration.

This is enough: **100% of script-callable primitives** were found by name.

<a id="2-что-говорят-4-856-сигнатур-про-устройство-движка"></a>
## 2. What 4,856 signatures say about the engine design

<a id="21-ecs-на-handleах"></a>
### 2.1. ECS on handles

The vast majority of the API is operations on `gohandle: Integer`
(GameObject handle) and `plhandle: Integer` (Player handle). None
the script does not receive a pointer to a C structure; everything through integer
descriptor and pairs `Get*ByHandle` / `Set*ByHandle`.

Subsystem size:

| Subsystem | Signature | What goes into it |
|---|---:|---|
| `game_object` | 715 | `Get/Set*ByHandle` for GameObject (position, orientation, AABB, ECS flags, anim, materials). |
| `player` | 185 | `Get/SetPlayer*ByHandle` (resources, limits, upgrades, relationships). |
| `scripting` | 85 | `EvaluateCodeThread`, `EvaluateFileThread`, `ParserGet*`, `ParserSet*`. |
| `save_load`/sync | 38 | `RecordCustom*`, `RecordSynch*`, `FileStream*`. |
| `behaviour_props` | 28 | `SetBehaviourBoolProperty`, `BehaviourCreate`, etc. - components on GameObject. |
| `spawn` | 25 | `Create*ByHandle`, `Destroy*`, `AddObjectToDestroyList`. |
| `ui` | 19 | `AddNewElement*`, `GetGuiTexture*`. |
| `path_command` | 15 | `MoveTo*ByHandle`, `StopOrders*`. |
| `geometry` | 11 | `VectorDistance`, `VectorRotateY`, `ArrayAffineVector*`. |
| `ai` | 10 | `AIRegionDoScanObjects*`. |
| `locale` | 9 | `GetLocaleTable*`. |
| `rng` | 5 | `Random`, `RandomExt`, `SetRandomKey`, etc. |
| `search` | 2 | `FindGameObjectByUniqId`, `FindUniqIdByGameObject`. |

The rest ~3,600 - `misc`: assets, particles, sound, render, debug, FOW,
camera, AI regional scans. Of these, approximately 4× more functions than
the script calls is an API for the editor (`editor.exe` is a separate binary,
but fumbling around the same DWS environment) and asset pipeline.

<a id="22-server-sync--что-это-такое-технически"></a>
### 2.2. Server sync - what is it technically?

In [server_sync_architecture.md](server_sync_architecture.md) we
described the `bProcess` pattern as an abstraction. Native API now
covers "how exactly the state is serialized":

**Low level - `RecordCustom*` (~25 functions):**

| Function | Purpose |
|---|---|
| `RecordCustomBegin{,GUI,Map,StateMachine,TagObject}` | Open a package of the appropriate type. |
| `RecordCustomEnd` | Close the package. |
| `RecordCustomReadBit/Boolean/Byte/Word/SmallInt/Int24/Integer/Float/PackedFloat/ShortString/String/Buffer` | Deserializers by type. |
| `RecordCustomWrite*` (mirror) | Serializers. |
| `RecordCustomBeginReadBitFields` / `EndReadBitFields` | Bit-packed blocks (several bit flags in one byte). |
| `RecordCustomGetReadPackageSize` / `WritePackageSize` | Current package size. |

The supported types hint at the network/save packet format:
- `Int24` - 24-bit integer (3 bytes, traffic saving).
- `PackedFloat` - float, packed into fewer bytes (probably scaled
  fixed-point).
- `Bit` + bit-fields - unit flags in bitstream.
- `ShortString` (Pascal, ≤255 bytes) and `String` (dynamic) - both
  are supported.

**Mid level - `RecordSynch*` (~30 functions):**

| Function | Purpose |
|---|---|
| `RecordSynchBegin{,GUI,MAP,ByHandle}` | Start synchronizing the specified status area. |
| `RecordSynchIntRegister` / `FloatRegister` / `StringRegister` | Register a slot in the synchronization stack. |
| `RecordSynchStackInt/Float/StringByName` | Synchronize value by name. |
| `RecordSynchStackInt/Float/StringByNameTestChanges` | Synchronize **only if it has changed** - this is delta encoding. |
| `RecordSynchState(name)` | Arbitrary marking of a point. |
| `SetRecordEnabled` / `SetRecordGroupEnabled` / `SetRecordInitializeEnabled` | Recording toggle switches. |

**Conclusion:** server-authoritative C3 works like this - the client calculates
its local state, runs through “registered” variables
via `RecordSynchStack*ByNameTestChanges`, and **sends only the delta
changes** in the form of a `RecordCustomWrite*`-packet, bit-packed by
type `Int24/PackedFloat/Bit-fields`. This explains why C3 traffic
small even in big battles.

`SetRecordInitializeEnabled` controls with a separate flag
“initial snapshot” (full state) vs “delta only”.

**Net I/O is not exposed in scripts.** There is none in signatures
`Net*`/`Send*`/`Broadcast*` - that is, below the level
`RecordSynch*`/`RecordCustom*` all inside `cossacks.exe` (Indy 10 +
Steam wrapper).

<a id="23-pathfinding--на-отдельном-потоке"></a>
### 2.3. Pathfinding - on a separate thread

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
in a separate pool of threads that have their own scheduler
(`StaticPriority`/`DynamicPriority`/`MinPriority`/`MaxPriority`,
`DeltaPriority`, `SleepStep`/`SleepLength`).

This changes our model of determinism: even if the RNG is fixed,
The order in which paths are completed depends on the OS thread scheduler. Probably
therefore in [determinism_audit.md](determinism_audit.md) production between
launches of the same save differ even on the same host - not
only because of RNG, but also because of the **race for the results of the pathfinding stream**.

Scripting API for pathfinding (how the script **creates** a request
paths) are not separate `Find*` functions, but commands through
`Set*ByHandle` (for example, `MoveTo`-style); the search itself is asynchronous and
the script just waits for the next tick.

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
| **Delphi `System.RandSeed`** (32-bit) | `Randomize` or direct entry `System.RandSeed` (DWS does not issue) | `Random` (`System._Random`: `seed := seed * 0x8088405 + 1`) | Default gameplay-RNG. Not controlled by `SetRandomKey`. |
| **Extended 64-bit seed** | `SetRandomKey(key: Integer)` (32-bit → sign-extend), `SetRandomExtKey64(k0, k1: Integer)` (full 64-bit) | `RandomExt` (64-bit LCG, own pair of constants) | Controlled flow for randomness where determinism through reseeding is needed. |
| **Seed of the map generator** | `SetMapGeneratorRandomKey(const randkey0, randkey1)` | Internal algorithm of the generator (not disassembled) | Isolated RNG for `_DoGenerate` (relief, placement of objects, starting positions). |
| **Global seed map generator** | `SetGlobalMapGeneratorRandomKey(const randkey0, randkey1)` | Separate (not disassembled) | Parallel storage in map state structures is a candidate for a worldmap or map preview in the lobby. |

Additionally: `GetPlayerCubeRandomValue(playerhandle: Integer): Float`
— a separate per-player deterministic “cube of randomness” (probably
for AI/decisions, so that each player sees his repeatable
sequence).

There is also a “weather” RNG: `GetAirWeatherRandom`, `SetAirWeatherRandom`,
`GetAirWeatherRandomStart`, `GetAirWeatherRandomEnd`,
`GetAirWindRandom` - isolated stream for atmospheric effects
(wind, clouds) so that the visual does not affect gameplay-PRNG.

**What does this change for the simulator:** when in [extraction
model](../../docs_en/recon/world/economy/peasant_extraction.md) we need
reproduce the behavior of peasants, it is important to understand which `Random*`
The script calls at every hot-path step. If only `random` is necessary
simulate Delphi `RandSeed`. If there is `SetRandomKey + RandomExt` -
simulate an extended seed and its LCG. Map RNG and weather are independent
storages do not affect the extraction chain.

<a id="25-поведенческие-компоненты-behaviour"></a>
### 2.5. Behavioral components (Behaviour)

`BehaviourCreate`, `BehaviourCreateWithKey`, `BehaviourDestroy` plus
~28 functions `SetBehaviour*Property` show that units are
GameObject + set of Behavior components. Behavior in DWS is
string class-name:
```pascal
BehaviourCreate(gohnd: Integer; const classname: String;
                uniq: Boolean; usecurrentparams: Boolean): Integer;
```
The names of `Behaviour*` classes are stored in RTTI and in `.parser` files - their
can be transferred via `BehaviourPropertiesLoadFromParser` /
`SaveToParser`. This explains architecturally why `unit.script`
operates with abstractions like “the unit has hp, weapon, anim, vision”
without explicit declaration of fields - fields live in Behavior components.

Of particular interest is `BehaviourInertia*` (apply force/torque/translation,
mirror, surface bounce): built-in **physical simulation of inertia**
for flying/throwable objects (for example, cannonballs, cavalry in
gallop).

<a id="26-ai--региональная-архитектура"></a>
### 2.6. AI - regional architecture

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
**AI operates in spatial regions** - separate “areas of interest” with
own list of objects. AI requests zone update
(`DoScanObjects`), gets a list of GameObjects in it, accepts
solutions. This beats `recon/ai.md` (if there is one) and closes the issue
"how AI searches for targets."

<a id="27-скриптовая-среда--dws-со-своими-расширениями"></a>
### 2.7. Scripting environment - DWS with its extensions

`EvaluateCodeThread(const code: String): Integer` and
`EvaluateFileThread(const filename: String): Integer` show that
DWS scripts can be run in separate threads. This explains
why do some script chains (for example, a campaign) look
"simultaneously working".

`AddProcAddress`, `PointerOf` - extensions over the standard DWS, give
scripts have access to function pointers. This suggests that part
gameplay logic is passed as callbacks (for example, handlers
script triggers).

<a id="3-топ-50-самых-частых-нативных-вызовов"></a>
## 3. Top 50 most common native calls

(Generated in `native_primitives.md` nearby, here is a condensed TOP 30 for reference.)

| # | Name | Calls | What does |
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
| 11 | `RecordCustomWriteInteger` | 111 | Serialization of the whole. |
| 12 | `ReadInteger` | 106 | Reading from stream. |
| 13 | `GetGameObjectUniqueIdByHandle` | 95 | Object UID. |
| 14 | `GetGameObjectHandleByUniqueId` | 94 | Inverse. |
| 15 | `GetPlayerGameObjectsCountByHandle` | 89 | Player object counter. |
| 16 | `WriteInteger` | 87 | Recording in stream. |
| 17 | `StrExists` | 86 | Search for a substring. |
| 18 | `SetBehaviourFloatProperty` | 84 | Set ECS-property. |

`SwitchTo` (146 files!) is something like `goto state` for
state-machines. Considering that there is `TFormStateMachines` in RTTI and
`MachineLibrary*` in API, behavioral level script logic
is organized as an FSM, and `SwitchTo` is a transition between states.

<a id="4-где-хранится-остальное-что-не-в-скриптах"></a>
## 4. Where is the rest stored (what is not in scripts)

Of the 4,856 native functions in the exe, the script calls only 884. The rest
3 972 is:

- **Editor API** — `AddEditorControl`, `AddEditorFormInput`,
  `AddCameraTrackPoint`, `ResourceTexturesReload`, etc. Used
  in `editor.exe` (separate binary, searches the same DWS environment).
- **Asset/pipeline** – `EnvironmentLoadLensFlareFromFile`,
  `MachineLibrarySaveSerialsToFile`, `ResourceLODActorLibrary*`.
- **Internal-only** — pre-render, low-level TLF (Top-Level Frame)
  and particle-FX operations, which the script never pulls.
- **Steam wrapper** — `SteamwrapStartVoiceRecording`,
  `TSteamAchievement` API.
- **Indy network layer** - `TInternetShellClient`, `TInternetShellSession`
  (uses Steam transport, visible in Pascal class names).

If you ever need to dig into the editor or network stack - all names
yes, RVA in `dws_native_signatures.json`.

<a id="5-что-закрыто-этим-документом"></a>
## 5. What is covered by this document

| Question | Where was opened | Answer |
|---|---|---|
| What is `bProcess` at the network level | `server_sync_architecture.md` | `RecordSynch*` + `RecordCustom*` - see §2.2. |
| How many RNG streams are in the engine | `determinism_audit.md` | 4 independent: `Random`, `RandomExt`, `MapGenerator`, `GlobalMapGenerator` + weather. §2.4. |
| How AI searches for targets | `ai.md` (TODO) | Via `AIRegionDoScanObjects*` - spatial regions. §2.6. |
| Pathfinding - sync or async | (open) | **Async, separate thread pool** with priorities. §2.3. |
| How units are serialized | (open) | `RecordCustom*` with types `Int24`, `PackedFloat`, `Bit-fields`. §2.2. |
| What is the “Behaviour” of a unit | `unit.script` guesses | Full ECS components with `BehaviourCreate(classname: String)`. §2.5. |

<a id="6-что-ещё-открыто--и-как-это-закрыть-без-декомпилятора"></a>
## 6. What else is open - and how to close it **without a decompiler**

Most of the initially open questions have been closed in related
documents Below is the status of each:

| Question | Where revealed |
|---|---|
| 6.1. Bit-layout of network packets | ✅ Fully described in [`server_sync_packet_format.md`](server_sync_packet_format.md): `EconomyPackage` (binary, 1–18 bytes), unit-state via parser-text. |
| 6.2. Implementation `Random` LCG | ✅ Fully described in [`rng_implementation.md`](rng_implementation.md): Delphi LCG `X = X × 134775813 + 1 mod 2³²`, plus per-decision deterministic seed pattern. |
| 6.3. Engine class map | ✅ See [`rtti_class_map.md`](rtti_class_map.md): 266 game-engine classes by subsystem, including `TXAIRegion*`, `TXPath*`, `TXTrigger*`, `TXLan*`. |
| 6.4. Algorithm for searching for a resource by a peasant | 🔬 Logic in `lib/unit.script:_unit_DoExtract` and related ones. There is no native `findnearestresource` - the search uses a combination of scan-grid (see [`target_selection.md`](../../docs_en/recon/world/combat/target_selection.md) §2) and `AIRegionDoScanObjects*` for large zones. Further parse using grep using scripts - without a decompiler. |
| 6.5. Exact pathfinding formula | 🔬 From RTTI classes (`TPathData`, `TOSWMovementPath`, `TOSWPathNode`, `TOSWPathNodes`, `TXPathCellChangedArray` - see [`rtti_class_map.md` §4](rtti_class_map.md)) it is clear that pathfinding is built **on a graph of nodes**, not on pure A* grid. Nodes are recalculated via `TXPathCellChangedArray` when the map changes. The exact graph search algorithm (Dijkstra / A* / weighted A*) is the only thing that requires decompilation; characteristics are observable through `PathDataThread*` parameters. |
| 6.6. Algorithm `MapGenerator` | 🔬 The `TXMapGenerator` class (see [`rtti_class_map.md` §8](rtti_class_map.md)) accepts a `(randkey0, randkey1)` pair - these are two uint32, a total of 64 status bits (like `RandomExt`, see [`rng_implementation.md` §3](rng_implementation.md)). A specific PRNG (Xorshift64? L'Ecuyer?) inside a class cannot be determined without decompilation. Not critical: given the same seed, the map is deterministic. |
| 6.7. Format `.aix` (AI-config) | 🔬 The `.aix` editor is built into `editor.exe` via `TAIXEditor` / `TAIXEditorState` / `TAIXArgsEditor` / `TAIXVarsEditor` (see [`rtti_class_map.md` §16](rtti_class_map.md)). The structure is “variables + arguments”, binary, but not critical: gameplay-AI is described in `lib/ai.script` and through `AIRegion*`-API. |
| 6.8. Format `.map` | ❌ Binary, not parsed. Used only for built-in missions (Historical Battle, campaign). Skirmish maps are procedural. See [`../data/file_formats.md`](../data/file_formats.md). |

**Principle:** “🔬” is theoretically solvable without a decompiler via
scripts or RTTI; “❌” really requires RE.

<a id="7-файлы-и-инструменты"></a>
## 7. Files and tools

| File | What does |
|---|---|
| `parser/engine_recon/extract_primitives.py` | Scans `data/scripts/*` → 884 native candidates + 46 type-casts + 19 DWS builtins. |
| `parser/engine_recon/dump_exe_strings.py` | Dump all ASCII (61k) and Pascal ShortString (15k) from `cossacks.exe` with RVA. |
| `parser/engine_recon/extract_dws_signatures.py` | Main: scans the AnsiString table, extracts 4,856 DWS signatures, cross-reference with script → 100% coverage. |

<a id="8-воспроизведение"></a>
## 8. Playback
```powershell
cd c:\projects\other\cossacks
python parser\engine_recon\extract_primitives.py
python parser\engine_recon\dump_exe_strings.py
python parser\engine_recon\extract_dws_signatures.py
```
Artifacts appear in `derived/*.json` and update the report in
`native_primitives.md` (adjacent file in the same folder).

<a id="9-если-всё-таки-понадобится-декомпилятор"></a>
## 9. If you still need a decompiler

`dws_native_signatures.json` contains the RVA of each signature - period
input for Ghidra/IDR/IDA. Scenario:

1. Open `cossacks.exe` in Ghidra with the Delphi plugin (DelphiHelper or
   IDR-import).
2. Go to the RVA of the desired signature - next to it is a pointer to the native one
   callback (standard DWS registration pattern in Delphi).
3. F5 → C-decompile. Delphi compile-output is easy to read (no
   C++ templates, no inline aggression).

The name of the callback function is often available from RTTI methods - each
The Delphi class in the exe contains `vmtTypeInfo` with a list of published methods.
You can strengthen `dump_exe_strings.py` by adding a walker via VMT, and
get ~1,779 classes with their methods as ASCII. But **it's already
extreme case** - statics covers 95% of tasks.
