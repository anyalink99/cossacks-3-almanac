<a id="исследовательский-план-игровые-системы"></a>
# Research Backlog: Game Systems

[Русский](../../internals/project/research_backlog_systems.md) · **English**

[← Project architecture and maintenance](README.md)

This page collects questions that cannot yet be answered from the available
scripts and extracted data. It is a technical research plan, not part of the
encyclopedia's account of confirmed game rules.

<a id="победа-поражение-и-завершение-партии"></a>
## Victory, Defeat, and the End of a Match

Reader article: [Victory, Defeat, and the End of a Match](../../docs_en/recon/systems/victory_conditions.md).

| # | Question | Next step |
|---:|---|---|
| 1 | What is the complete score table by internal ID? The known values are 10 for a Peasant and 1,000 for a Town Hall, while the complete set is distributed across roughly 3,000 calls to `SetObjBuildingExtProperties` and `SetObjBaseSearchBuildVisionScore`. | Parse the call sites in `unit.script`. |
| 2 | Where does the native executable call `_misc_Surrender`, and which interface control invokes it? The likely candidate is the **Surrender** button in the game menu, with no separate hotkey. | Inspect the native interface callbacks. |
| 3 | How do the battle-music and attack-warning intervals relate to each other? The difference between `gc_gui_battlemusicinterval` and `gc_gui_underattackalarminterval` may be useful to warning-analysis tools. | Calculate the intervals from the constants and verify them in play. |
| 4 | What changes the map stage from `started` to `finished`? `_misc_CheckEndGame` does not write it; a likely transition point is entry into `gc_gamemode_endgamestatistics`. | Profile the network protocol at the end of a match. |
| 5 | How is victory handled when only one team was present from the start? After an opponent surrenders, `_misc_CheckEndGame` sees one surviving team, but a match started without opponents takes the `not bSecondTeamExist` early exit. | Compare both setups in the editor. |
| 6 | Does the final screen display one score total or the sampled `stat.scores` time series? | Inspect the interface extension. |

<a id="искусственный-интеллект"></a>
## Artificial Intelligence

Reader article: [How the Computer Player Works](../../docs_en/recon/systems/ai_behavior.md).

1. **Population of the aggressor pool.** Trace
   `gPlayer[plInd].aiData.agressors.Add` to establish the exact conditions
   and timing of the first attack.
2. **Activation of `bhumanai`.** No script setter has been found. Check the
   native engine and `gui/options/`; an option or tournament mode may set it.
3. **Per-squad action counters.** Find the writers of
   `TSquad.fAttackCount`, `fMoveCount`, and `fDelayCount`, which `TArmy`
   reads. Likely locations include `unit.inc/onattack*.inc`.
4. **Meaning of `gc_ai_max_guards = 120`.** Determine whether this is a
   base-defender count or another limit. It currently appears as a buffer
   above the threshold for **Pikemen, 17th century**.
5. **The `centerfound` transition.** Full development waits for
   `aidata.centerfound = True`. Find the writer and test whether it is tied
   to the first Town Hall.
6. **Military decision latency.** `progresswarai` runs once every 2.4 game
   seconds per player, while each army has its own `fStateTime` delays.
   Exact intervals require tracing `progresswarai.inc:4100-4220`.
7. **Effect of difficulty on attack frequency.** The `aggressor` and
   `sabotage` branches use `gc_ai_AgressorsCount = 5` at every difficulty;
   only the number of parallel raids changes. Compare the first attack on
   Easy and Impossible while accounting for construction speed.
8. **Size of later waves.** Five squads is a small first wave for an army
   of 100 **Pikemen, 17th century**; the remaining squads stay near the
   base during the first dispatch. Test whether later waves grow relative
   to `gc_ai_max_guards = 120`.
9. **Mine-search ranges.** Determine which of
   `gc_ai_dist_mines_lvl1 = 30`, `lvl2 = 60`, and `expansion = 85` is used
   on Tiny and Normal maps. The values are measured in cells.
10. **War and upgrade phase transitions.** Find the writers of
    `aidata.bprogressWar` and `aidata.bprogressUpgrades`.

<a id="добыча-ресурсов-и-экономика"></a>
## Resource Gathering and the Economy

Reader article:
[Peasant Resource Gathering](../../docs_en/recon/world/economy/peasant_extraction.md).

1. **Travel-time losses.** Measure the exact `loss_factor`—the share of
   working time a peasant spends walking to a storehouse—for several
   reproducible resource and storehouse layouts.
2. **Variation in practical gathering rates.** Repeat five-minute runs from
   the same saved game and estimate the effect of random target selection
   separately for wood, stone, and mines.
3. **Trees per map pattern.** Refine the `K` coefficient that converts forest
   pattern counts into tree counts. The current estimate of 0.30 is calibrated
   against Tiny and Large maps; inspect the environment of several generated
   maps to obtain a stronger estimate.

<a id="захват-объектов"></a>
## Object Capture

Reader article:
[Capturing Objects](../../docs_en/recon/world/economy/capture_mechanics.md).

1. **Building point used for distance checks.** Determine whether `(px, py)`
   is the model center, bounding-box center, or anchor point. Approach
   different sides of the same building with a Peasant and record the minimum
   distance.
2. **Purpose of `bAutoKill`.** The field is declared but never assigned in
   `_misc_CheckCapture`. Inspect native callers and determine whether it is
   unused legacy behavior from an earlier game.
3. **Wall capture path.** `_unit_SearchCapturersForWall` does not check
   `bcancapture`. Test whether Peasants or artillery can damage a Wall through
   this execution path.

<a id="генератор-случайных-чисел-и-детерминизм"></a>
## Random-Number Generation and Determinism

Reader article:
[Determinism Audit](../engine/determinism_audit.md).

1. **Saving the generator state.** Test whether the global `random` cursor is
   serialized in a saved game. Load the same save repeatedly and compare the
   sequence of subsequent random events.
2. **Variable time step.** Determine which gameplay systems depend on native
   frame duration and whether that dependency can make replays diverge when
   the command stream is unchanged.

<a id="генерация-случайной-карты"></a>
## Random-Map Generation

Reader article:
[Random-Map Generation](../../docs_en/recon/world/map/map_generation_pipeline.md).

1. **Complete variation space.** The 230 base layouts are known, but the
   effective range of random keys is not. Perform a bounded enumeration and
   separate unique maps from duplicates.
2. **Starting-position encoding.** Decode the `arrStartPos` RGB markers in
   `inputbitmap.tga` and match them to player positions on the generated map.
3. **Desert patterns.** Add the `season = 3` patterns to
   `compute_map_resources.py` after checking their contents across several
   runs. They currently appear in only one of twenty inspected replays.

<a id="управление-и-обратная-связь"></a>
## Controls and Player Feedback

Reader article: [Controls and Player Feedback](../../docs_en/recon/systems/ui_input_and_feedback.md).

1. **Function of `Shift+Alt+0..9`.** The combinations are reserved, but
   their purpose is not visible in the scripts. Inspect the native
   interface handlers or test them in play.
2. **Allied sounds beyond the fog of war.** Test whether an allied unit can
   be heard when it is hidden from the current player but visible to its
   owner.
3. **Warning delay.** The threshold is 135 internal units, or about
   4.22 game seconds on a 32-frames-per-second scale. Measure the actual
   interval in play.
4. **Double-clicking a unit portrait.** Test whether it invokes
   `MoveCameraToSelectedUnits`; the trigger itself has not been found in
   the scripts.
5. **The `Ctrl+W` and `Ctrl+F` camera jumps.** The engine reserves both
   combinations, but their exact destinations are not established. Inspect
   the interface handlers and test each combination in play.
6. **Native control-group handlers.** Establish the role of `TXGroup4`, its
   relationship with `TXGroupSelectionViewer`, and the entry points used to
   assign and recall groups. Do not treat `SetGUIEventStateOn*` as the
   confirmed numeric-group handler without separate evidence.

<a id="наёмники-и-дипломатический-центр"></a>
## Mercenaries and the Diplomatic Center

Reader article: [Mercenaries and the Diplomatic Center](../../docs_en/recon/systems/mercenaries_diplomacy.md).

| # | Question | Next step |
|---:|---|---|
| 1 | Can a player actually build only one Diplomatic Center? Localization states the limit, but no explicit check for human players has been found. The AI check `_ai_GetUnitCount(..., gc_ai_unit_dipcenter) > 0` does not constrain a human player, and `costpercent = 100` does not prevent another building. | Inspect `gui.script`, the `_ai_TryUnit` quota, behavior in play, and any check equivalent to `if count(dip) >= 1 then bproduceenabled := False`. |
| 2 | What is `bnoreputation` intended to represent? None of the inspected `.script` or `.global` files assigns it; it may be inherited from an earlier game in the series or have been identified under the wrong name. | Search the complete game data and trace the field's origin. |
| 3 | What is the interval between eligible idle-state checks for famine and rebellion? The per-check probabilities are known, but the conversion to game seconds has not been measured. | Relate the `Nothing` handler to [ticks and game time](../engine/ticks_and_subticks.md) and measure the interval at every game speed. |
| 4 | Why do 20 **Ship of the Line** (`battleship`) variants in `data.json` have `bmercenary = True` when the `case 'battleship'` branch in `unit.script` does not set the flag? | Inspect the separate Shipyard path and rule out a parser artifact. |

<a id="сценарии-и-события-в-миссиях"></a>
## Scenarios and Mission Events

Reader article: [Scenarios and Mission Events](../../docs_en/recon/systems/scenarios_and_triggers.md).

1. **`OnLoadScriptFileName`.** The field exists in the executable, but
   ordinary scenario handlers do not use it to load a separate `.script`
   or DWS file when the stage changes. Find the native consumer.
2. **`TFormStateMachines`.** This RTTI class belongs to editor
   infrastructure for individual-object state machines. Establish
   separately whether mission stages use another state machine. The class
   appears in the `cossacks.exe` RTTI, while the `MachineLibrary*` family
   serializes individual-object state machines to `.parser`; see
   [native engine functions](../engine/native_api.md).
3. **Active-rule limit.** No hard limit has been found. Measure evaluation
   frequency with more than one hundred rules.
4. **`.aix` binary format.** Document the scenario-data container consumed
   by the native parser and map its fields to `TScenarioTrigger`,
   `TScenarioCondition`, `TScenarioAction`, and `TScenarioQuery`.
