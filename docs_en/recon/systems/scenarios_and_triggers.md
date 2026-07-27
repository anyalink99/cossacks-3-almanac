<a id="сценарии-и-условия-событий"></a>
<a id="сценарии-и-события-в-миссиях"></a>
# Scenarios and Mission Events

[← How the game works](../README.md)

Historical Battles and campaigns do not follow one hard-coded plot. They are
built from rules: the game watches for events on the map and responds with
predefined actions. A mission can notice that the player has reached a
crossing, display a message, create reinforcements, and unlock the next
objective.

<a id="кратко"></a>
<a id="главное"></a>
## Key points

- Each rule connects a **condition** to one or more **actions**.
- A condition may check time, resources, unit count, a destroyed building,
  entry into an area, or a scenario flag.
- An action may show text, grant resources, create units, change relations,
  issue an order, declare victory, or enable another rule.
- A rule disables itself when it fires. It can run again only if another
  action explicitly enables it.
- Mission stages form chains of explicitly enabled rules and flags: one
  action enables the next rule or changes a flag.

<a id="жизненный-цикл"></a>
<a id="как-развивается-миссия"></a>
## How a mission progresses

On each scenario update, the game checks the active rules. If a condition is
true, the rule is disabled first and its actions are then executed [^1].
This normally prevents the same event from repeating every game tick.

A typical mission works like this:

1. The introduction is shown and the first objective rule is enabled.
2. A unit entering a specified area starts dialogue or an enemy attack.
3. Destroying the attacking group sets a flag for the next stage.
4. The new flag enables reinforcements, changes the objective, or opens the
   next part of the map.
5. The final condition declares victory or defeat.

A rule can be enabled again, so a scenario can create recurring waves. The
mission author must build that loop explicitly; repetition is not automatic.

<a id="типичные-условия"></a>
<a id="какие-условия-можно-проверять"></a>
## Conditions a mission can check

| Condition | Example use |
|---|---|
| Unit count | Continue when the army reaches a required size, or fail after an escorted force dies. |
| Destroyed building | Open a route after a fortress is destroyed. |
| Unit in an area | Start an ambush near a bridge. |
| Elapsed time | Create the next wave after several minutes. |
| Resource stockpile | Complete an economic objective after enough gold is collected. |
| Scenario flag | Connect events that happened in different locations. |
| Combined conditions | Require the player to hold an area and keep a commander alive. |

Simple checks can be combined with AND, OR, and NOT. For a more complex
case, the scenario can query the current map state—for example, search a
radius for units of a given type and owner.

<a id="типичные-действия"></a>
<a id="что-сценарий-может-изменить"></a>
## What a scenario can change

| Action | What the player sees |
|---|---|
| Create objects | Reinforcements, enemies, or scenery appear on the map. |
| Grant resources | The selected resource stockpile increases. |
| Issue unit orders | A force moves, attacks, stops, or stops searching for enemies on its own. |
| Control a computer player | Its normal AI behavior is enabled or disabled. |
| Change relations | Players become allies, enemies, or neutral parties. |
| Show text or play sound | Dialogue, a hint, or audio is presented. |
| Control rules and flags | The next stage opens or an earlier event is repeated. |
| End the mission | The game declares victory or defeat. |

The complete system contains about sixty action types. Their internal names
are collected under [Technical details](#technical-details), where editor
terminology does not interrupt the explanation of play.

<a id="особые-эффекты-gscenariobactive"></a>
<a id="чем-сценарная-партия-отличается-от-случайной-карты"></a>
## How a scenario differs from a random-map match

An active scenario changes more than the objectives:

1. **Scripted invulnerability.** Objects with a special health value and
   non-playable characters may ignore damage. See
   [Damage calculation](../world/combat/combat_damage_pipeline.md).
2. **Special peace-time rules.** The main hero may interact only with the
   opponents selected by the mission.
3. **Special allied vision.** The main player does not receive vision from
   neutral campaign characters. See
   [Vision and fog of war](../world/combat/vision_and_fow.md).
4. **Scripted aggression.** An opponent may follow scenario orders rather
   than the standard computer-player algorithm.

The same army can therefore behave differently in a campaign and on a
random map; that is not necessarily an AI bug.

<a id="итоги-tscenarioresult"></a>
<a id="победа-поражение-и-переход-между-миссиями"></a>
## Victory, defeat, and moving between missions

A scenario can end the current mission in victory or defeat. The campaign
then records the result and opens the prescribed continuation. A mission can
also end in a draw, restart from the beginning, or advance to the next stage.

The ordinary “one team remains” rule is covered in
[Victory and defeat](victory_conditions.md). A scenario can instead end a
match on any authored condition: holding an area, collecting resources,
losing a character, or reaching a timer.

<a id="технические-подробности"></a>
## Technical details

<a id="структура-сценария"></a>
<a id="внутренние-объекты"></a>
### Internal objects

The scenario is loaded into the single `gScenario` object. In the shipped
game, this data is found primarily in `.aix` map files [^2].

| Game concept | Internal class |
|---|---|
| Event rule | `TScenarioTrigger` |
| Condition | `TScenarioCondition` |
| Action | `TScenarioAction` |
| State query | `TScenarioQuery` |
| Mission result | `TScenarioResult` |

After a condition succeeds,
`gScenario.triggers[i].bactive := False` disables the rule. The
`gc_trigger_action_advanced_enableTrigger` action can enable it again;
`gc_trigger_action_service_flagSetActive` and
`gc_trigger_action_service_flagSetNotActive` change scenario flags.

The scenario system includes `gc_trigger_action_player_giveResources`,
`gc_trigger_action_player_disableAI` / `enableAI`,
`gc_trigger_action_advanced_disableTrigger` / `enableTrigger`,
`gc_trigger_action_order_*`, and the victory and defeat actions. The full
`gc_trigger_action_*` list is declared in `dmscript.global`.

For complex conditions, `TScenarioQuery` runs on every rule check and returns
a Boolean result. It can search an area without requiring a separate `DWS`
file.

<a id="где-живут-сценарии"></a>
<a id="где-хранятся-данные"></a>
### Where the data lives

| File | Purpose |
|---|---|
| `data/maps/<scenario>.aix` | Scenario data loaded by the game's native parser. |
| `data/maps/<scenario>.map` | Terrain and initial map objects. |
| `data/scripts/lib/scenario.script` | Loading and execution of rules, conditions, and actions. |
| `data/scripts/lib/scenarioeditor.script` | Scenario-editor support. |

The scenario-data parser is native. The script reads values through the
`Parser*ValueByKeyByHandle` family.

<a id="источники"></a>
## Sources

[^1]: In `data/scripts/progress/progress.inc/scenario.inc:71-77`,
      `gScenario.triggers[i].bactive := False` is executed before
      `_scenario_EvaluateTriggerActions(ptrigger)`. Rule enabling and
      disabling are handled at
      `data/scripts/lib/scenario.script:1739,3076-3081`.

[^2]: `data/scripts/lib/scenario.script` is the main scenario-system script
      (about 200 KB). It declares `gScenario`, loads the data, and processes
      rules, conditions, and actions.
