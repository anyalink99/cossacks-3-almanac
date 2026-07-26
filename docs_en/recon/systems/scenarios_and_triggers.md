<a id="recon-сценарии-и-триггеры"></a>
<a id="сценарии-и-триггеры"></a>
# Scenarios and Triggers

[← How the game works](../README.md)

Deep dive: how the scenarios work (Historical Battles and
campaign) - what is a trigger, condition, action, FSM state.
All links to the code are in [Sources](#sources).

## TL;DR

- The script is a file `.parser` with a description of the FSM state,
  uploaded via `gScenario` [^1].
- Trigger (`TScenarioTrigger`) - a “condition + action” pair.
  When the condition is true, the action is executed once.
- Condition (`TScenarioCondition`) - checking the game state:
  “the player has N units”, “building X is destroyed”, “the player has reached the point”.
- Action (`TScenarioAction`) - state change: “unit spawn”,
  “text on screen”, “transition to next FSM state”.
- FSM (`TScenarioStateMachine`) switches trigger sets: in
  In the “fight” state, some triggers work; in the “victory” state, others work.
- Scripts use **inline DWS scripts** through the field
  `OnLoadScriptFileName` (see
  [`scripts/structure.md` §3](../../../internals_en/scripts/structure.md)).
- The active script is marked `gScenario.bactive = True` - this is
  includes special effects (invulnerability for `hp >= gc_gameplay_infinitehp`,
  separate peace-mode processing, etc.).

---

<a id="1-структура-сценария"></a>
## 1. Scenario structure

The script is described in the `.parser` file, usually located in
`data/maps/` or embedded in a campaign. Root objects:

| Object | What |
|---|---|
| `TScenarioStateMachine` | State machine of the scenario. |
| `TScenarioState` | One state (for example, “fight”, “victory”, “dialogue”). |
| `TScenarioTrigger` | Trigger - link `condition → action`. |
| `TScenarioCondition` | Trigger condition. |
| `TScenarioAction` | Trigger action. |
| `TScenarioResult` | Scenario result (win/loss/special). |
| `TScenarioQuery` | Query the game state (for difficult conditions). |

The main object is `gScenario`, the only copy per batch.

---

<a id="2-триггер"></a>
## 2. Trigger

A trigger is a record with two key fields: condition
(`TScenarioCondition`) and action (`TScenarioAction`).

<a id="21-жизненный-цикл"></a>
### 2.1. Life cycle

1. When the FSM state is activated, all its triggers **connect**
   to check.
2. Each game tick (or with a given frequency) script
   checks the condition of each active trigger.
3. When the condition is true, the action is executed.
4. After execution, the trigger is **deactivated** (if it
   `single-shot`) or remains for repeated operation
   (`repeating`).

<a id="22-типичные-условия"></a>
### 2.2. Typical conditions

`TScenarioCondition` supports many templates:

| Type | What checks |
|---|---|
| `unit_count_le(player, sid, N)` | The player now has N units of a specific type ≤ N. |
| `unit_count_ge(player, sid, N)` | …became ≥ N. |
| `building_destroyed(handle)` | The building is destroyed. |
| `unit_at_point(handle, x, z, radius)` | Unit in radius from the point. |
| `time_elapsed(seconds)` | N game seconds has passed since the beginning of the state. |
| `resource(player, type, op, amount)` | Player resource ≥/≤ N. |
| `flag_set(name)` | The script flag is set. |
| `composite (AND, OR, NOT)` | Combination of conditions. |

<a id="23-типичные-действия"></a>
### 2.3. Typical Actions

`TScenarioAction` supports:

| Type | What does |
|---|---|
| `spawn_unit(player, sid, x, z)` | Create a unit. |
| `gc_trigger_action_player_giveResources` | Add resources to the player. |
| `gc_trigger_action_player_disableAI` / `enableAI` | Turn off/on the player's AI. |
| `gc_trigger_action_advanced_disableTrigger` / `enableTrigger` | Disable/enable another trigger by index. |
| `gc_trigger_action_service_flagSetActive` / `flagSetNotActive` | Set/reset scenario flag (`gScenario.flags[id].bactive`). |
| `gc_trigger_action_order_*` | Unit commands: stop, attack, move, disableSearchEnemy, etc. |

The complete list is `gc_trigger_action_*` to `dmscript.global` (about 60 types). There is no Inline DWS code in the script scripts - all effects go through pre-defined `TScenarioTriggerAction` types; The level of customization is determined by the choice of action and its parameters.

### 2.3. Single-shot

When the trigger conditions are met, before executing the actions, it
immediately deactivated: `gScenario.triggers[i].bactive := False`
[^TriggerOnce]. The same trigger will not fire twice until
someone obviously won't turn it back on after
`gc_trigger_action_advanced_enableTrigger`.

---

<a id="3-этапы-сценария"></a>
## 3. Stages of the scenario

The script does not have a separate FSM with transitions between “states” -
stages are implemented by a combination of flags (`gScenario.flags[]`) and
`disable/enableTrigger`-action. Typical pattern:

| Stage | Implementation |
|---|---|
| Introduction | Active triggers with conditions for starting the game; their actions - text, sound, activation of the following. |
| Battle phase 1 | Trigger with the condition “X time has passed” → enableTrigger for the attack wave. |
| Battle phase 2 | Trigger with the condition “squad destroyed” → enable triggers of the second wave and disable the first. |
| Victory | Trigger with a condition for killed enemies → victory action. |

That is, the “transition between states” is a series
`disableTrigger`/`enableTrigger`/`flagSetActive` actions inside
triggers, rather than a separate FSM mechanism.

---

<a id="4-inline-скрипты"></a>
## 4. Inline scripts

Complex actions (which are not covered by standard
`TScenarioAction` types) are implemented through inline DWS scripts.
The script field `OnLoadScriptFileName` points to a separate
`.script` file that is loaded when the FSM state is activated.

This file contains normal DWS functions that can call
any native API (see
[`internals/engine/native_api.md`](../../../internals_en/engine/native_api.md))
and read `gScenario.*`-fields.

This gives writers the full power of scripts: you can do
arbitrary logic of dialogues, allies, custom triggers.

---

<a id="5-особые-эффекты-gscenariobactive"></a>
## 5. Special effects `gScenario.bactive`

When `gScenario.bactive = True`, the engine turns on several
special behaviors:

1. **Scenario invulnerability**: units with `hp >= gc_gameplay_infinitehp`
   or `not GetGameObjectPlayableObjectByHandle(handle)` do not receive
   damage (see [`combat_damage_pipeline.md` §7](../world/combat/combat_damage_pipeline.md)).
2. **Peace-mode** (`gbool_peacemode`) is processed with special
   way - the hero player can only attack certain
   opponents.
3. **Union review** (`AddFOWPlayers`): main player (plInd = 0)
   does not share reviews with **neutral** characters in the campaign
   (See [`vision_and_fow.md` §4.2](../world/combat/vision_and_fow.md)).
4. **AI**: AI opponents in the scenario use separate rules
   (often manual scripted aggression, not standard
   `_ai_DoTickAggressive`).

---

<a id="6-tscenarioquery--запросы-к-состоянию"></a>
## 6. `TScenarioQuery` - status queries

When the trigger condition is not covered by simple `unit_count` /
`resource`, used `TScenarioQuery` - parameterized
request. For example, “are there any units within a radius R from point (x, z)
specific type of player P".

The query is executed every time the trigger is checked and returns
boolean result. This allows for flexible conditions without
rewrites on DWS.

---

<a id="7-tscenarioresult--итоги"></a>
## 7. `TScenarioResult` - results

The final state of the script is `TScenarioResult`. Possible
values:

| Result | What |
|---|---|
| `victory` | The player wins, the ending is positive. |
| `defeat` | Defeat. |
| `draw` | Draw (rare). |
| `next_mission(id)` | In the campaign - transition to the next mission. |
| `replay_mission` | Repeat the same mission (player's choice). |

When the script completes, the script writes the result to
`gCampaignProgress` - structure with progress throughout the campaign.
This structure is saved to disk (see also
[`internals/engine/server_sync_packet_format.md`](../../../internals_en/engine/server_sync_packet_format.md)).

---

<a id="8-где-живут-сценарии"></a>
## 8. Where scripts live

| File | What |
|---|---|
| `data/maps/<scenario>.aix` | Binary script format (compiled?). |
| `data/maps/<scenario>.map` | The map itself (terrain, initial units). |
| `data/scripts/lib/scenario.script` | Basic scripting logic for processing scripts (~200 KB of code). |
| `data/scripts/lib/scenarioeditor.script` | Script editor (for developers and modders). |

Script parser - native (via `Parser*ValueByKeyByHandle`),
script `lib/scenario.script` loads trigger structures and
conditions through these challenges.

---

<a id="9-открытые-эмпирические-вопросы"></a>
## 9. Open empirical questions

1. **Exact syntax of `.aix` file**. Binary script format,
   which is not disassembled. In the current project `.aix` files are not
   are being parsed.
2. **Limit on the number of triggers in one state**. Looks like
   there is no hard limit, but with a large number (>100) the frequency
   checks may sag.
3. **Inline DWS scripts in a script**. Statement about
   `OnLoadScriptFileName` needs verification: in `scenario.script`
   and script handlers for explicit downloads of a separate `.script` file
   When activating the stage, it could not be found. Perhaps this opportunity
   refers to the script editor/modding, not the basic one
   engine.

---

<a id="источники"></a>
## Sources

[^1]: `data/scripts/lib/scenario.script` - main processing script
      scripts (~200 KB, 30+ functions). Announces `gScenario`,
      processes triggers, states, FSM transitions.

[^2]: Class `TFormStateMachines` found in RTTI `cossacks.exe` (see.
      [`internals/engine/native_api.md`](../../../internals_en/engine/native_api.md))
      — UI of the FSM script editor. Also `MachineLibrary*` -
      serialization of state machines in `.parser` format. This
      infrastructure for **engine** state-machines (per-object,
      `nothing`/`OnDeath`/etc.), not for scenario FSM.

[^TriggerOnce]: `data/scripts/progress/progress.inc/scenario.inc:71-77`:
      comes before `_scenario_EvaluateTriggerActions(ptrigger)`
      `gScenario.triggers[i].bactive := False`. Also
      `_scenario_EvaluateTriggerActions` — `lib/scenario.script:1739`
      — contains handler `gc_trigger_action_advanced_disableTrigger`
      /`enableTrigger` (see lines 3076-3081 of the same file).
