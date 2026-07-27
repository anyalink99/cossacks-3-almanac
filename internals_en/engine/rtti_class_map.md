<a id="карта-delphi-классов-движка-rtti"></a>
# Delphi Engine Class Map (RTTI)

A structured overview of `cossacks.exe` subsystems derived from class names
found in RTTI.

> **Where the data comes from.** In the Pascal ShortString table `cossacks.exe`
> we extracted **1,779 Delphi class names** (`T*` / `E*` / `I*` / `F*`).
> Of these, about 266 are game-engine classes (prefixes `TX` and `TOSW`),
> the rest belong to the standard Delphi VCL, Indy 10, FastMM4, and
> JPEG/DDS/OpenGL bindings. The full dump is in
> [`../../derived/exe_strings.json`](../../derived/exe_strings.json),
> under `delphi_class_names`. The extractor is
> [`../../parser/engine_recon/dump_exe_strings.py`](../../parser/engine_recon/dump_exe_strings.py).

<a id="ключевые-префиксы"></a>
## Key prefixes

| Prefix | Count | Meaning |
|---|---:|---|
| `TX*` | 576 | Cossacks 3 engine classes: game objects, AI regions, patterns, state machines, paths, maps, scenarios, triggers, LAN, and more. |
| `TOSW*` | 263 | OpenSourceWorld engine: rendering, sound, particles, and atmosphere, inherited from a GLScene-like base. |
| `EId*` | ~50 | Indy 10 network stack (Internet Direct). |
| `T*` standard Delphi | ~700 | VCL: TForm, TButton, TStringList, TBitmap, TPersistent, etc. |
| `EAb*`, `EAccess*`, `EConvert*`, `EOut*` | ~150 | Standard Delphi exceptions. |
| `TXAIX*` | 4 | `.aix` format editor (see §10). |
| `T*OSW*Mod*` | 3 | Mod loader. |

<a id="1-игровые-объекты-txgameobject"></a>
## 1. Game objects (`TXGameObject*`)

The root class of all “things on the map” is `TXGameObject`.

| Class | Purpose |
|---|---|
| `TXGameObject` | Base object for units, buildings, resources, and effects. |
| `TXBrushGameObject` | “Brush” objects (scenery, static map elements). |
| `TXEventGameObject` | Trigger points, spawners. |
| `TXGameObjectsGrid` | Spatial grid of all objects on the map. |
| `TXGridGameObjectMap` | Grid type map → handle. |
| `TXPickedGameObjects` | Currently selected group (UI state). |

All 715 ECS API functions (`Get*ByHandle` / `Set*ByHandle`; see
[`native_api.md` §2.1](native_api.md)) work with `TXGameObject`.

<a id="2-behaviour-компоненты-txbehaviour-22-класса"></a>
## 2. Behavior components (`TXBehaviour*`, ~22 classes)

ECS-style design: each game object can contain several behavior components.

| Class | Purpose |
|---|---|
| `TXBaseBehaviour`, `TXBehaviour`, `TXBehaviours` | Base classes and container. |
| `TOSWBaseBehaviour`, `TOSWBehaviour`, `TOSWBehaviours` | Similar at the OSW (render) level. |
| `TXConditionMachineBehaviour` | Conditional behavior (FSM-like). |
| `TXDelayDestroyBehaviour`, `TXDelayDestroyListBehaviour` | Delayed deletion. |
| `TXMiniMapPrimitiveBehaviour` | Drawing a point on the minimap. |
| `TXPhysicalFallBehaviour` | Gravity-driven falling, such as a corpse after death. |
| `TXRollBehaviour`, `TXRotationBehaviour`, `TXTiltBehaviour`, `TXTurnObjectBehaviour` | Rotation/tilt. |
| `TXThrowBehaviour`, `TXThrowUpBehaviour` | Throwing (grenade, body). |
| `TXMoveRotateWaveBehaviour` | Pendulum movement. |
| `TXPoolBehaviour` | Object from the pool (for pooled-allocation). |
| `TXProgressChildrenBehaviour`, `TXProgressStateMachineBehaviour` | FSM-progress of “child” objects. |
| `TXRayCastBehaviour`, `TXRayCastBehaviourAxis`, `TXRayCastBehaviourWheel` | Raycast (surface contact/cart wheel). |
| `TXTLFAnimationBehaviour`, `TXTLFAnimationChildrenBehaviour` | Top-Level Frame animation. |
| `TXDecalChildrenBehaviour`, `TXDecalTransformBehaviour` | Decals (traces, blood, shadow). |

Components are created through native `BehaviourCreate(gohnd, classname)`; see
[`native_api.md` §2.5](native_api.md). The name in `BehaviourCreate` is
string class name (one of the listed ones).

<a id="3-ai-регионы-txairegion-5-классов"></a>
## 3. AI regions (`TXAIRegion*`, 5 classes)
Spatial AI mechanics. Each area of interest is a separate object.

| Class | Purpose |
|---|---|
| `TXAIRegion` | One region. |
| `TXAIRegions` | Collection of regions. |
| `TXAIRegionManager` | Creates, updates, deletes regions. |
| `TXAIRegionScanMode` | Enum scan modes (`scan` / `clear` / `update`). |
| `TXAIRegionViewer` | Visualizer for the editor (coloring zones in the editor). |

For script wrappers, see [`native_api.md` §2.6](native_api.md).
Together, these five classes implement spatial AI: the AI asks
`TXAIRegionManager` to update an area of interest, receives the objects within
it, and decides whether to attack or retreat.

<a id="4-pathfinding-txpath-toswpath-tpathdata-6-классов"></a>
## 4. Pathfinding (`TXPath*`, `TOSWPath*`, `TPathData`, 6 classes)

These classes clarify the pathfinding model described in `native_api.md §6.2`:

| Class | Purpose |
|---|---|
| `TPathData` | Path data for one unit (waypoints, current segment). |
| `TOSWMovementPath` | One path as a sequence of nodes. |
| `TOSWMovementPaths` | Collection of active paths. |
| `TOSWPathNode` | Path node (point with coordinates + connections with neighbors). |
| `TOSWPathNodes` | Node graph. |
| `TXPathCellChangedArray` | An array of “changed cells” for cache invalidation. |

**Conclusion:** C3 pathfinding uses a **graph-based representation** (nodes and
connections) layered over the grid, rather than plain grid-based A*.
Nodes (`TOSWPathNode`) live in the `TOSWPathNodes` graph. When the cell
map changes (construction / demolition of building), `TXPathCellChangedArray`
marks it for recalculation.

It runs asynchronously through the 14 `PathDataThread*` functions (see
[`native_api.md` §2.3](native_api.md)) in a separate prioritized thread pool.

<a id="5-топология-txtopology-1-класс"></a>
## 5. Topology (`TXTopology`, 1 class)

The scripts contain the native primitive `TopologyGetPath` (mentioned in
[`docs/recon/world/combat/pathfinding.md`](../../docs_en/recon/world/combat/pathfinding.md)).
`TXTopology` encapsulates map traversability, including collisions and
water/land regions. The pathfinding engine uses it to search the node graph
from one point to another.

<a id="6-сценарии-и-триггеры-txscenario-txtrigger-8-классов"></a>
## 6. Scenarios and triggers (`TXScenario*`, `TXTrigger*`, 8 classes)

These are the engine-side foundations of the script system (see also
[`scenarios_and_triggers.md`](../../docs_en/recon/systems/scenarios_and_triggers.md)).

| Class | Purpose |
|---|---|
| `TXScenario` | One scenario (Historical Battle/campaign mission). |
| `TXScenarioList` | Collection of scenarios. |
| `TXTrigger` | One trigger (condition → action). |
| `TXTriggerEvent`, `TXTriggerEvents` | Triggering events. |
| `TXTriggerEventMode` | Event processing mode (single-shot / repeating). |
| `TXTriggerEventType` | Event type (UnitDied / ResourceReached / TimeElapsed / ...). |
| `TXTriggerManager` | Manages all active triggers. |

The script-side wrappers are `gScenario` and
`lib/scenario.script` (see
[`internals/scripts/structure.md` §5](../scripts/structure.md)).

<a id="7-state-machines-txstatemachine-9-классов"></a>
## 7. State Machines (`TXStateMachine*`, 9 classes)

| Class | Purpose |
|---|---|
| `TXStateMachine` | One FSM instance. |
| `TXStateMachineArgs` | Current state arguments. |
| `TXStateMachineLibrary` | Loading ready-made FSMs from `.parser` files. |
| `TXStateMachineProperty` | State property. |
| `TXStateMachineStack`, `TXStateMachineStackItem` | State stack (nested FSMs). |
| `TXStateMachineProgressOption`, `TXStateMachineProgressChildrenOption` | Tick options (how to continue progress on child FSMs). |
| `TFormStateMachines` | FSM editor (UI form in editor.exe). |

In Cossacks 3, state machines drive both **unit behavior** (idle → walk → work
→ return → drop), and **script trigger logic** (see §6).
All state machines are loaded from `.parser` files via
`TXStateMachineLibrary`. Native `MachineLibrary*` functions (see
[`native_api.md` §2.5](native_api.md)) work with this class.

<a id="8-карты-и-генерация-7-классов"></a>
## 8. Maps and generation (7 classes)

| Class | Purpose |
|---|---|
| `TXMap` | Base map containing terrain, objects, and dimensions. |
| `TXMapGenerator` | Procedural generator for skirmish. |
| `TXGlobalMapGenerator` | Campaign generator (for the global campaign map). |
| `TXTileMap`, `TXTileMapSchemesList` | Tile-grid of terrain (cluster by type). |
| `TXHeightMap` | Terrain height (heightmap). |
| `TXMiniMap` | Minimap (render in the corner of the UI). |
| `TXGridGameObjectMap` | See §1. |

`TXMapGenerator` uses the `(randkey0, randkey1)` pair, which represents
64 bits of seed state (see
[`rng_implementation.md` §8](rng_implementation.md)).

<a id="9-pattern-25-классов"></a>
## 9. Pattern (25 classes)

| Class | Purpose |
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

The binary `.pattern` format is parsed by
[`../../parser/parse_patterns.py`](../../parser/parse_patterns.py).
These classes are runtime wrappers.

<a id="10-multiplayer--lan-txlan-8-классов"></a>
## 10. Multiplayer / LAN (`TXLan*`, 8 classes)

These classes expose the networking layer beneath the `RecordSynch*` /
`RecordCustom*` API (see
[`server_sync_packet_format.md`](server_sync_packet_format.md)):

| Class | Purpose |
|---|---|
| `TXLan`, `TXLanManager` | Main network object. |
| `TXLanClientInfo`, `TXLanClientInfoBase` | Client status. |
| `TXLanPublicServer`, `TXLanServerInfoBase` | Public server lobby. |
| `TXLanPublicServerClient`, `TXLanPublicServerSession` | Connection to the server. |

The transport layer is **Indy 10**, identified by `EId*` exception classes in
the executable. `TXLan*` provides the game-side wrapper around Indy.

`TXLanPublicServer` suggests that Cossacks 3 had its own public matchmaking
service separate from Steam. Current integration appears to use the Steam
wrapper, as indicated by `SteamwrapStartVoiceRecording` and other `Steamwrap`
functions in the native API.

<a id="11-mod-loader-toswmod-3-класса"></a>
## 11. Mod loader (`TOSWMod*`, 3 classes)

| Class | Purpose |
|---|---|
| `TOSWModDat` | One `.dat` mod file. |
| `TOSWModLib`, `TOSWModLibrary` | Mod library (container). |

Used by external `modman.exe` (see also
[`../scripts/structure.md` §1](../scripts/structure.md)).

<a id="12-сериализация-и-сохранение"></a>
## 12. Serialization and Save Data

| Class | Purpose |
|---|---|
| `TPersistent`, `TPersistentClass` | Standard Delphi base. |
| Names with `Custom*Read*` / `Custom*Write*` (via RTTI methods) | Corresponds to native-API `RecordCustom*` (see [`server_sync_packet_format.md`](server_sync_packet_format.md)). |

<a id="13-звук-26-классов"></a>
## 13. Sound (26 classes)

| Class | Purpose |
|---|---|
| `TOSWSoundManager` | Main sound-system manager. |
| `TOSWSoundLibrary` | Sound library. |
| `TOSWSoundSample`, `TOSWSoundSamples` | Samples. |
| `TOSWSoundEmitter`, `TOSWBSoundEmitter` | Positional sound emitters in the world. |
| `TOSWSoundEmittersList` | Active sources. |
| `TOSWSoundEnvironment` | Ambience (reverb, effects). |
| `TOSWSoundFile`, `TOSWSoundFileFormat`, `TOSWSoundFileFormatsList` | Format `.ogg` / `.snd`. |
| `TOSWSoundSampling`, `TOSWSoundSource`, `TOSWSoundSourceChange*` | Sampling-rate and dynamics. |
| `TOSWSoundVolumeGroup` | Group mixer. |
| `TXSoundCollection`, `TXSoundInterface`, `TXSoundItem`, `TXSoundLibrary*`, `TXSoundManager`, `TXSoundProperty`, `TXSoundVolume*` | Game-side wrappers. |

<a id="14-render-25-классов-и-шейдеры"></a>
## 14. Rendering and Shaders (~25 classes)

| Class | Purpose |
|---|---|
| `TXShader`, `TXShadowMap` | Shader, shadow map. |
| `TXPHDRToneMapShader` | HDR tonemap shader. |
| `TOSWCadencerMode`, `TOSWCameraInvarianceMode` | Camera movement options. |
| `TOSWAtmosphere*`, `TOSWAtmosphereException` | Sky, atmosphere, precipitation. |
| Many `T*` for model rendering, FBO, shadow casting. |

These classes belong to the 3D rendering stack and are not critical to
gameplay logic.

<a id="15-партиклы-27-классов"></a>
## 15. Particles (27 classes)

`TXParticle*` and `TXSourcePFX*` form the particle system (fire, smoke, blood,
explosions). Not critical for gameplay logic, but interesting for
visual modding.

<a id="16-aix-формат-taix-4-класса"></a>
## 16. AIX format (`TAIX*`, 4 classes)

| Class | Purpose |
|---|---|
| `TAIXEditor` | Editor of `.aix` files. |
| `TAIXEditorState` | Editor state. |
| `TAIXArgsEditor`, `TAIXVarsEditor` | Submodules (arguments/variables). |

The `.aix` editor is built into `editor.exe`. This tells us that:
- the `.aix` format is **binary**, but **editable** through the UI;
- its structure is organized around variables (`TAIXVarsEditor`) and arguments
  (`TAIXArgsEditor`);
- a future parser can begin with the `TAIXEditorState` class in the executable,
  whose method names are visible through RTTI.

<a id="17-ui-формы-25"></a>
## 17. UI forms (25+)

`TForm*` classes are editor windows:

| Class | Purpose |
|---|---|
| `TFormDWSDebugger` | DWS script debugger. |
| `TFormScriptEvaluate` | Expression evaluation window. |
| `TFormStateMachines` | FSM editor. |
| `TFormDbgCtrl` | Debug controls. |
| `TFormHelloScreen` | Game start screen. |
| Other `TForm*` | Editor/settings/mod manager UI. |

<a id="ограничения-этого-обзора"></a>
## Limitations of this review

1. **Not all 1,779 classes are listed.** This page covers only engine
   subsystems (`TX*`, `TOSW*`, and AIX). Standard Delphi VCL and Indy 10
   classes are omitted because their source is publicly available.
2. **Only class names are available, not methods.** Recovering every class's
   published methods would require extending `dump_exe_strings.py` with a VMT
   walker (see
   [`native_api.md` §9](native_api.md)).
3. **This is structural evidence, not full semantics.** A name such as
   `TXAIRegion` identifies an AI region, but its exact fields remain unknown without
   decompilation.

Even so, the names provide a useful **structural map** of the engine's entities
and subsystems.

<a id="воспроизведение"></a>
## Reproducing the Analysis
```powershell
cd c:\projects\other\cossacks
python parser\engine_recon\dump_exe_strings.py
# → derived/exe_strings.json (delphi_class_names field)
```
