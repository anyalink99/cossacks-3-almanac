# Delphi engine class map (RTTI)

Structured overview of `cossacks.exe` subsystems through names
classes found in RTTI.

> **Where the data comes from.** In the Pascal ShortString table `cossacks.exe`
> we extracted **1,779 Delphi class names** (`T*` / `E*` / `I*` / `F*`).
> Of these, about 266 are game-engine classes (prefixes `TX` and `TOSW`),
> the rest are standard Delphi VCL, Indy 10, FastMM4 and
> JPEG / DDS / OpenGL binding. Full dump - in
> [`../../derived/exe_strings.json`](../../derived/exe_strings.json),
> field `delphi_class_names`. Extractor -
> [`../../parser/engine_recon/dump_exe_strings.py`](../../parser/engine_recon/dump_exe_strings.py).

## Key prefixes

| Prefix | Qty | What is this |
|---|---:|---|
| `TX*` | 576 | Game engine: GameObject, AIRegion, Pattern, StateMachine, Path, Map, Scenario, Trigger, Lan, etc. Classes specific to the Cossacks 3 engine. |
| `TOSW*` | 263 | OpenSourceWorld engine - render, sound, particles, atmosphere. Inherited from a GLScene-like base. |
| `EId*` | ~50 | Indy 10 - network stack (Internet Direct). |
| `T*` standard Delphi | ~700 | VCL: TForm, TButton, TStringList, TBitmap, TPersistent, etc. |
| `EAb*`, `EAccess*`, `EConvert*`, `EOut*` | ~150 | Standard Delphi exceptions. |
| `TXAIX*` | 4 | Editor of the `.aix` format (see §10). |
| `T*OSW*Mod*` | 3 | Mod loader. |

## 1. Game objects (`TXGameObject*`)

The root class of all “things on the map” is `TXGameObject`.

| Class | Destination |
|---|---|
| `TXGameObject` | Basic unit - unit, building, resource, effect. |
| `TXBrushGameObject` | “Brush” objects (scenery, static map elements). |
| `TXEventGameObject` | Trigger points, spawners. |
| `TXGameObjectsGrid` | Spatial grid of all objects on the map. |
| `TXGridGameObjectMap` | Grid type map → handle. |
| `TXPickedGameObjects` | Current selected group (UI-state). |

All 715 ECS-API functions (`Get*ByHandle` / `Set*ByHandle` - see.
[`native_api.md` §2.1](native_api.md)) work with `TXGameObject`.

## 2. Behavior components (`TXBehaviour*`, ~22 classes)

ECS style: each GameObject can carry several Behavior objects.

| Class | What does |
|---|---|
| `TXBaseBehaviour`, `TXBehaviour`, `TXBehaviours` | Basic/container. |
| `TOSWBaseBehaviour`, `TOSWBehaviour`, `TOSWBehaviours` | Similar at the OSW (render) level. |
| `TXConditionMachineBehaviour` | Conditional behavior (FSM-like). |
| `TXDelayDestroyBehaviour`, `TXDelayDestroyListBehaviour` | Delayed deletion. |
| `TXMiniMapPrimitiveBehaviour` | Drawing a point on the minimap. |
| `TXPhysicalFallBehaviour` | Falling due to gravity (corpse after death). |
| `TXRollBehaviour`, `TXRotationBehaviour`, `TXTiltBehaviour`, `TXTurnObjectBehaviour` | Rotation/tilt. |
| `TXThrowBehaviour`, `TXThrowUpBehaviour` | Throwing (grenade, body). |
| `TXMoveRotateWaveBehaviour` | Pendulum movement. |
| `TXPoolBehaviour` | Object from the pool (for pooled-allocation). |
| `TXProgressChildrenBehaviour`, `TXProgressStateMachineBehaviour` | FSM-progress of “child” objects. |
| `TXRayCastBehaviour`, `TXRayCastBehaviourAxis`, `TXRayCastBehaviourWheel` | Raycast (surface contact/cart wheel). |
| `TXTLFAnimationBehaviour`, `TXTLFAnimationChildrenBehaviour` | Top-Level Frame animation. |
| `TXDecalChildrenBehaviour`, `TXDecalTransformBehaviour` | Decals (traces, blood, shadow). |

Created via native `BehaviourCreate(gohnd, classname)` - see.
[`native_api.md` §2.5](native_api.md). The name in `BehaviourCreate` is
string class name (one of the listed ones).

## 3. AI regions (`TXAIRegion*`, 5 classes)
Spatial AI mechanics. Each area of ​​interest is a separate object.

| Class | What |
|---|---|
| `TXAIRegion` | One region. |
| `TXAIRegions` | Collection of regions. |
| `TXAIRegionManager` | Creates, updates, deletes regions. |
| `TXAIRegionScanMode` | Enum scan modes (`scan` / `clear` / `update`). |
| `TXAIRegionViewer` | Visualizer for the editor (coloring zones in the editor). |

Script wrapper codes - see [`native_api.md` §2.6](native_api.md).
These 5 classes are enough to build spatial AI: AI
requests `TXAIRegionManager` to update the zone of interests,
gets a list of objects in it and decides to attack/retreat.

<a id="4-pathfinding-txpath-toswpath-tpathdata-6-классов"></a>
## 4. Pathfinding (`TXPath*`, `TOSWPath*`, `TPathData`, 6 classes)

Reveals what was "discovered" in `native_api.md §6.2`:

| Class | What |
|---|---|
| `TPathData` | Path data for one unit (waypoints, current segment). |
| `TOSWMovementPath` | One path as a sequence of nodes. |
| `TOSWMovementPaths` | Collection of active paths. |
| `TOSWPathNode` | Path node (point with coordinates + connections with neighbors). |
| `TOSWPathNodes` | Node graph. |
| `TXPathCellChangedArray` | An array of “changed cells” for cache invalidation. |

**Conclusion:** pathfinding in C3 uses **graph-based**
representation (nodes + connections) on top of the grid, not purely A* on the grid.
Nodes (`TOSWPathNode`) live in the `TOSWPathNodes` graph. When the cell
map changes (construction / demolition of building), `TXPathCellChangedArray`
marks it for recalculation.

Controlled asynchronously via `PathDataThread*` (14 functions, see
[`native_api.md` §2.3](native_api.md)) - separate thread pool with
priorities.

<a id="5-топология-txtopology-1-класс"></a>
## 5. Topology (`TXTopology`, 1st class)

The scripts contain the native primitive `TopologyGetPath` (mentioned in
[`docs/recon/world/combat/pathfinding.md`](../../docs_en/recon/world/combat/pathfinding.md)).
Class `TXTopology` is an object that encapsulates the patency of the map
(collisions, water-region, water-land). It is used
pathfinding engine for searching from point A to point B by nodes.

<a id="6-сценарии-и-триггеры-txscenario-txtrigger-8-классов"></a>
## 6. Scenarios and triggers (`TXScenario*`, `TXTrigger*`, 8 classes)

The engine basis of the script system (see also recon review:
[`scenarios_and_triggers.md`](../../docs_en/recon/systems/scenarios_and_triggers.md)).

| Class | What |
|---|---|
| `TXScenario` | One scenario (Historical Battle/campaign mission). |
| `TXScenarioList` | Collection of scenarios. |
| `TXTrigger` | One trigger (condition → action). |
| `TXTriggerEvent`, `TXTriggerEvents` | The event that triggers. |
| `TXTriggerEventMode` | Event processing mode (single-shot / repeating). |
| `TXTriggerEventType` | Event type (UnitDied / ResourceReached / TimeElapsed / ...). |
| `TXTriggerManager` | Manages all active triggers. |

This is the engine part. Script wrapper - `gScenario` and
`lib/scenario.script` (see
[`internals/scripts/structure.md` §5](../scripts/structure.md)).

<a id="7-state-machines-txstatemachine-9-классов"></a>
## 7. State Machines (`TXStateMachine*`, 9 classes)

| Class | What |
|---|---|
| `TXStateMachine` | One FSM instance. |
| `TXStateMachineArgs` | Current state arguments. |
| `TXStateMachineLibrary` | Loading ready-made FSMs from `.parser` files. |
| `TXStateMachineProperty` | State property. |
| `TXStateMachineStack`, `TXStateMachineStackItem` | State stack (nested FSMs). |
| `TXStateMachineProgressOption`, `TXStateMachineProgressChildrenOption` | Tick ​​options (how to continue progress on child FSMs). |
| `TFormStateMachines` | FSM editor (UI form in editor.exe). |

FSM in Cossacks 3 is also **unit behavior** (idle → walk → work
→ return → drop), and **script trigger logic** (see §6).
All state machines are loaded from `.parser` files via
`TXStateMachineLibrary`. Native-API `MachineLibrary*`-functions (see.
[`native_api.md` §2.5](native_api.md)) work with this class.

<a id="8-карты-и-генерация-7-классов"></a>
## 8. Maps and generation (7 classes)

| Class | What |
|---|---|
| `TXMap` | Base map - terrain, objects, size. |
| `TXMapGenerator` | Procedural generator for skirmish. |
| `TXGlobalMapGenerator` | Campaign generator (for the global campaign map). |
| `TXTileMap`, `TXTileMapSchemesList` | Tile-grid of terrain (cluster by type). |
| `TXHeightMap` | Terrain height (heightmap). |
| `TXMiniMap` | Minimap (render in the corner of the UI). |
| `TXGridGameObjectMap` | See §1. |

`TXMapGenerator` works with `(randkey0, randkey1)` pair, which
explains the 64-bit state of the seed (see.
[`rng_implementation.md` §8](rng_implementation.md)).

<a id="9-pattern-25-классов"></a>
## 9. Pattern (25 classes)

| Class | What |
|---|---|
| `TXPattern`, `TXPatternCollection` | One “stamp” template/collection. |
| `TXPatternMask` | Object placement mask. |
| `TXPatternObject` | An object that is placed according to the mask. |
| `TXPatternFreq`, `TXPatternFreqs` | Repetition frequencies (for randomization). |
| `TXPatternCover`, `TXPatternCoverList` | Map area coverage. |
| `TXPatternListCollection`, `TXPatternListItem` | List metadata. |
| `TXBrushPatternPaint`, `TXEventPatternPaint` | Editor brushes. |
| `TXPatternDecal` | Decals by pattern. |
| `TXPatternWater` | Pattern for water. |
| `TXPatternLocalZone`, `TXPatternLocalZonesList` | Local zones pattern. |
| `TXBridgePatternFreq`, `TXBridgePatternFreqs` | Bridges pattern. |
| `TXLightPattern`, `TXLightPatternItem`, `TXLightPattern[List|s]` | Lighting pattern. |
| `TXColorPatternsList` | Color pattern. |
| `TXGlobalPatternList` | Global list of all patterns. |
| `TPatternManager` | Main manager object. |

The binary format of `.pattern` files has been parsed into
[`../../parser/parse_patterns.py`](../../parser/parse_patterns.py).
These classes are runtime wrappers.

<a id="10-multiplayer--lan-txlan-8-классов"></a>
## 10. Multiplayer / LAN (`TXLan*`, 8 classes)

Expands sin-stack under `RecordSynch*` / `RecordCustom*`-API (see.
[`server_sync_packet_format.md`](server_sync_packet_format.md)):

| Class | What |
|---|---|
| `TXLan`, `TXLanManager` | Main network object. |
| `TXLanClientInfo`, `TXLanClientInfoBase` | Client status. |
| `TXLanPublicServer`, `TXLanServerInfoBase` | Public server lobby. |
| `TXLanPublicServerClient`, `TXLanPublicServerSession` | Connection to the server. |

Ferry - **Indy 10** (`EId*` exception classes in exe).
`TXLan*` - game-side wrapper for Indy.

`TXLanPublicServer` hints that Cossacks 3 had its own public
matchmaking server (separate from Steam). It seems to be working now
via Steam wrapper (visible by `SteamwrapStartVoiceRecording` and
other Steamwrap functions in the native API).

<a id="11-mod-loader-toswmod-3-класса"></a>
## 11. Mod loader (`TOSWMod*`, 3 classes)

| Class | What |
|---|---|
| `TOSWModDat` | One `.dat` mod file. |
| `TOSWModLib`, `TOSWModLibrary` | Mod library (container). |

Used by external `modman.exe` (see also
[`../scripts/structure.md` §1](../scripts/structure.md)).

<a id="12-сериализация-и-сохранение"></a>
## 12. Serialization and saving

| Class | What |
|---|---|
| `TPersistent`, `TPersistentClass` | Standard Delphi base. |
| Names with `Custom*Read*` / `Custom*Write*` (via RTTI methods) | Corresponds to native-API `RecordCustom*` (see [`server_sync_packet_format.md`](server_sync_packet_format.md)). |

<a id="13-звук-26-классов"></a>
## 13. Sound (26 classes)

| Class | What |
|---|---|
| `TOSWSoundManager` | The main sound is an object. |
| `TOSWSoundLibrary` | Sound library. |
| `TOSWSoundSample`, `TOSWSoundSamples` | Samples. |
| `TOSWSoundEmitter`, `TOSWBSoundEmitter` | Sound source on the card. |
| `TOSWSoundEmittersList` | Active sources. |
| `TOSWSoundEnvironment` | Ambience (reverb, effects). |
| `TOSWSoundFile`, `TOSWSoundFileFormat`, `TOSWSoundFileFormatsList` | Format `.ogg` / `.snd`. |
| `TOSWSoundSampling`, `TOSWSoundSource`, `TOSWSoundSourceChange*` | Sampling-rate and dynamics. |
| `TOSWSoundVolumeGroup` | Group mixer. |
| `TXSoundCollection`, `TXSoundInterface`, `TXSoundItem`, `TXSoundLibrary*`, `TXSoundManager`, `TXSoundProperty`, `TXSoundVolume*` | Game-side wrappers. |

## 14. Render (~25 classes) and shaders

| Class | What |
|---|---|
| `TXShader`, `TXShadowMap` | Shader, shadow map. |
| `TXPHDRToneMapShader` | HDR tonemap shader. |
| `TOSWCadencerMode`, `TOSWCameraInvarianceMode` | Camera movement options. |
| `TOSWAtmosphere*`, `TOSWAtmosphereException` | Sky, atmosphere, precipitation. |
| Many `T*` for model rendering, FBO, shadow casting. |

It's not critical for gameplay - it's a 3D stack.

## 15. Particles (27 classes)

`TXParticle*`, `TXSourcePFX*` - particle system (fire, smoke, blood,
explosions). Not critical for gameplay logic, but interesting for
visual modding.

## 16. AIX format (`TAIX*`, 4 classes)

| Class | What |
|---|---|
| `TAIXEditor` | Editor of `.aix` files. |
| `TAIXEditorState` | Editor state. |
| `TAIXArgsEditor`, `TAIXVarsEditor` | Submodules (arguments/variables). |

That is, the `.aix` format editor is built into `editor.exe`. This means:
- `.aix`-format **binary**, but **editable** through the UI.
- The structure is stored by “fields” (`TAIXVarsEditor` - this is about
  variables, `TAIXArgsEditor` - about arguments).
- If you ever need to parse `.aix`, the entry point is RVA class
  `TAIXEditorState` in exe (method names in RTTI are visible).

## 17. UI forms (25+)

`TForm*` classes are editor windows:

| Class | What |
|---|---|
| `TFormDWSDebugger` | DWS script debugger. |
| `TFormScriptEvaluate` | Expression evaluation window. |
| `TFormStateMachines` | FSM editor. |
| `TFormDbgCtrl` | Debug controls. |
| `TFormHelloScreen` | Game start screen. |
| Other `TForm*` | Editor/settings/mod manager UI. |

## Limitations of this review

1. **Not all 1779 classes are listed** - only subsystems
   game-engine (`TX*`, `TOSW*`, AIX). Standard Delphi VCL and
   Indy 10 is not understood - they are open-source.
2. **Class names only** - not methods. To get full
   the list of published methods of each class needs to be expanded
   `dump_exe_strings.py` walker by VMT (see.
   [`native_api.md` §9](native_api.md)).
3. **Statics, not semantics.** The name `TXAIRegion` hints that this is
   AI zone, but the exact set of class fields is not visible without
   decompilation.

Nevertheless, names provide a **structural map**: you understand which
entities live in the engine and in which subsystem.

## Play
```powershell
cd c:\projects\other\cossacks
python parser\engine_recon\dump_exe_strings.py
# → derived/exe_strings.json (поле delphi_class_names)
```
