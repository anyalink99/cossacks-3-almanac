<a id="recon-сценарии-и-триггеры"></a>
<a id="сценарии-и-триггеры"></a>
<a id="сценарии-и-условия-событий"></a>
# Scenarios and Event Rules

[← How the game works](../README.md)

How Historical Battles and campaigns work: what a scenario rule contains,
how conditions are evaluated, and which actions the game can perform.
Internal class names and source references are included for verification.

<a id="кратко"></a>
## TL;DR

- A scenario is loaded into the single `gScenario` object. In the shipped
  game, scenario data is primarily associated with `.aix` maps [^1].
- An event rule (`TScenarioTrigger`) connects a condition to one or more
  actions. It runs once when the condition becomes true unless another
  action explicitly enables it again.
- A condition (`TScenarioCondition`) inspects the game state: a unit count,
  a destroyed building, a unit reaching a point, and so on.
- An action (`TScenarioAction`) changes the game state by creating a unit,
  displaying text, granting resources, or enabling another rule.
- Mission stages are assembled from scenario flags and enabled or disabled
  rules. A separate scenario state machine is **not confirmed** by the
  inspected code.
- Loading a separate DWS script through `OnLoadScriptFileName` is likewise
  **not confirmed** for ordinary scenarios. The name occurs in editor and
  engine state-machine infrastructure.
- `gScenario.bactive = True` marks an active scenario and enables special
  behavior such as invulnerability at
  `hp >= gc_gameplay_infinitehp` and separate peacetime handling.

---

<a id="1-структура-сценария"></a>
## 1. Scenario structure

Scenario data normally lives under `data/maps/` or is included in a
campaign. The inspected implementation revolves around these objects:

| Object | What |
|---|---|
| `TScenarioTrigger` | Event rule: a condition and its actions. |
| `TScenarioCondition` | Condition that activates a rule. |
| `TScenarioAction` | Action performed by a rule. |
| `TScenarioResult` | Scenario result (win/loss/special). |
| `TScenarioQuery` | Query the game state (for difficult conditions). |

The main object is `gScenario`, with one instance per match.

---

<a id="2-триггер"></a>
<a id="2-сценарное-правило"></a>
## 2. Event rule

An event rule is a record with two key fields: a condition
(`TScenarioCondition`) and action (`TScenarioAction`).

<a id="21-жизненный-цикл"></a>
### 2.1. Life cycle

1. Active rules are registered for evaluation.
2. Every game tick, or at a configured interval, the script checks each
   active rule.
3. When the condition is true, the action is executed.
4. The rule is **disabled before its actions execute**. It can run again
   only when an action explicitly re-enables it.

<a id="22-типичные-условия"></a>
### 2.2. Typical conditions

`TScenarioCondition` supports many templates:

| Type | What checks |
|---|---|
| Unit count (`unit_count_le`, `unit_count_ge`) | The player has at most or at least the specified number of a unit type. |
| Destroyed building (`building_destroyed`) | A specified building has been destroyed. |
| Unit at point (`unit_at_point`) | A unit is within a specified radius of a point. |
| Time (`time_elapsed`) | A specified number of game seconds has elapsed. |
| Resource (`resource`) | A player's resource stock has reached a threshold. |
| Flag (`flag_set`) | A scenario flag is active. |
| Composite (`AND`, `OR`, `NOT`) | Several tests combined with Boolean operators. |

<a id="23-типичные-действия"></a>
### 2.3. Typical Actions

`TScenarioAction` supports:

| Type | What does |
|---|---|
| Create unit (`spawn_unit`) | Create a specified unit at a position. |
| Grant resources (`gc_trigger_action_player_giveResources`) | Add resources to a player. |
| AI control (`gc_trigger_action_player_disableAI` / `enableAI`) | Disable or enable a player's AI. |
| Rule control (`gc_trigger_action_advanced_disableTrigger` / `enableTrigger`) | Disable or enable another rule by index. |
| `gc_trigger_action_service_flagSetActive` / `flagSetNotActive` | Set/reset scenario flag (`gScenario.flags[id].bactive`). |
| Orders (`gc_trigger_action_order_*`) | Tell units to stop, attack, move, or stop searching for enemies automatically. |

The full list is `gc_trigger_action_*` in `dmscript.global` (roughly
60 types). In the inspected scenarios, effects are expressed through
predefined `TScenarioTriggerAction` types and their parameters.

<a id="24-однократное-срабатывание"></a>
### 2.4. Single execution

When a rule's condition succeeds, the rule is disabled before its actions
run: `gScenario.triggers[i].bactive := False` [^3]. It cannot
fire twice unless another action re-enables it with
`gc_trigger_action_advanced_enableTrigger`.

---

<a id="3-этапы-сценария"></a>
## 3. Stages of the scenario

The scenario has no confirmed separate state machine for stage transitions.
stages are implemented by a combination of flags (`gScenario.flags[]`) and
rule-control actions. A typical pattern is:

| Stage | Implementation |
|---|---|
| Introduction | Active rules detect the start of the match, display text, play sound, and enable later rules. |
| Battle phase 1 | A time condition enables the attack-wave rule (`enableTrigger`). |
| Battle phase 2 | A “squad destroyed” condition enables the second wave and disables the first. |
| Victory | A condition on defeated enemies performs the victory action (`victory`). |

That is, the “transition between states” is a series
`disableTrigger`/`enableTrigger`/`flagSetActive` actions inside
triggers, rather than a separate FSM mechanism.

---

<a id="4-inline-скрипты"></a>
<a id="4-что-известно-о-дополнительных-скриптах"></a>
## 4. What is known about additional scripts

The executable contains the field name `OnLoadScriptFileName`, but neither
`scenario.script` nor the inspected scenario handlers contain a call that
loads the named `.script` file when a mission stage changes. Ordinary
scenarios therefore cannot yet be said to support this feature.

The standard actions already cover resource grants, relationships, unit
orders, text, and rule switching. `OnLoadScriptFileName` may instead belong
to the editor or to state machines attached to individual game objects.

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
3. **Allied vision** (`AddFOWPlayers`): the main player (`plInd = 0`)
   does not share vision with **neutral** campaign characters
   (See [`vision_and_fow.md` §4.2](../world/combat/vision_and_fow.md)).
4. **AI**: AI opponents in the scenario use separate rules
   (often manual scripted aggression, not standard
   `_ai_DoTickAggressive`).

---

<a id="6-tscenarioquery--запросы-к-состоянию"></a>
<a id="6-запросы-к-состоянию-tscenarioquery"></a>
## 6. State queries (`TScenarioQuery`)

When a condition is not covered by a simple `unit_count` or `resource`
test, `TScenarioQuery` performs a parameterized query—for example, whether
the specified player owns a unit of a given type within a radius of a point.

The query runs every time the rule is checked and returns a Boolean result.
This supports flexible conditions without adding DWS code.

---

<a id="7-tscenarioresult--итоги"></a>
<a id="7-итоги-tscenarioresult"></a>
## 7. Results (`TScenarioResult`)

The scenario result is represented by `TScenarioResult`:

| Result | What |
|---|---|
| `victory` | The player wins, the ending is positive. |
| `defeat` | Defeat. |
| `draw` | Draw (rare). |
| `next_mission(id)` | In the campaign - transition to the next mission. |
| `replay_mission` | Repeat the same mission (player's choice). |

When a scenario completes, it writes the result to `gCampaignProgress`,
the campaign-wide progress structure.
This structure is saved to disk (see also
[`internals/engine/server_sync_packet_format.md`](../../../internals_en/engine/server_sync_packet_format.md)).

---

<a id="8-где-живут-сценарии"></a>
## 8. Where scenarios live

| File | What |
|---|---|
| `data/maps/<scenario>.aix` | Binary scenario format (not yet decoded). |
| `data/maps/<scenario>.map` | The map itself (terrain, initial units). |
| `data/scripts/lib/scenario.script` | Core scenario-processing logic (about 200 KB). |
| `data/scripts/lib/scenarioeditor.script` | Scenario editor logic for developers and modders. |

Parsing is implemented by the engine through
`Parser*ValueByKeyByHandle`; `lib/scenario.script` uses these calls to
load rules and conditions.

---

<a id="9-открытые-эмпирические-вопросы"></a>
## 9. Open empirical questions

1. **Exact `.aix` syntax.** The binary scenario format has not been
   decoded, and this project does not currently parse `.aix` files.
2. **Active-rule limit.** No hard limit was found, but evaluation may slow
   down with more than 100 active rules.
3. **Purpose of `OnLoadScriptFileName`.** No scenario code was found that
   loads a separate `.script` file when a stage activates. The field may
   belong to the editor or modding infrastructure instead.

---

<a id="источники"></a>
## Sources

[^1]: `data/scripts/lib/scenario.script` is the main scenario-processing
      script (about 200 KB and more than 30 functions). It declares
      `gScenario` and processes rules, conditions, and actions.

[^2]: Class `TFormStateMachines` found in RTTI `cossacks.exe` (see.
      [`internals/engine/native_api.md`](../../../internals_en/engine/native_api.md))
      is an editor interface for state machines. `MachineLibrary*` also
      serializes engine state machines to `.parser`. This is infrastructure
      for **per-object engine behavior** (`nothing`, `OnDeath`, and other
      states), not evidence of a mission-stage state machine.

[^3]: `data/scripts/progress/progress.inc/scenario.inc:71-77`:
      comes before `_scenario_EvaluateTriggerActions(ptrigger)`
      `gScenario.triggers[i].bactive := False`. Also
      `_scenario_EvaluateTriggerActions` — `lib/scenario.script:1739`
      handles `gc_trigger_action_advanced_disableTrigger`
      /`enableTrigger` (see lines 3076-3081 of the same file).
