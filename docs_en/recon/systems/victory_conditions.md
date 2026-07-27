<a id="recon-условия-победы-и-конец-партии"></a>
<a id="победа-поражение-и-завершение-партии"></a>
# Victory, Defeat, and the End of a Match

[← How the game works](../README.md)

This article explains how a Cossacks 3 match ends: who wins, who loses, how
points are calculated, and which familiar strategy-game victory conditions
are absent.

<a id="кратко"></a>
## Key points

- In an ordinary match, the **last remaining team** wins.
- Automatic defeat is tied to the number of the player's non-building units.
  At zero, the player loses even if buildings remain; at low population, the
  game separately checks for a Peasant or Town Hall. Historical Battles
  disable this check.
- There is no built-in Wonder, score-limit, time-limit, or
  capture-the-flag victory. A custom scenario can create such an objective.
- Score is used for statistics and achievements, but does not decide the
  match or determine rating changes.
- Surrender immediately marks the player as defeated and runs the ordinary
  check for surviving teams.

<a id="1-состояния-игрока"></a>
<a id="2-режимы-игры"></a>
<a id="режимы-партии"></a>
## Match types

The ending rules depend on the kind of match:

- **Random Map** — a standard unscripted match.
- **Historical Battle** — a map with fixed starting forces and no Peasant
  economy. The ordinary player-existence check is disabled; only a scenario
  rule or surrender remains [^7].
- **Campaign** — a sequence of scenarios that records victory, defeat, and
  the highest completed difficulty [^8] [^9].
- **Editor and Scenario Editor** — modes for testing custom maps.
- **Rated multiplayer** — the ordinary team victory condition plus special
  rules for publishing results and penalizing an early exit.
- **Replay / Spectator** — modes without army control.

Exact internal fields are collected under
[Technical details](#technical-details).

<a id="3-условия-победы"></a>
<a id="условия-победы"></a>
## Victory conditions

<a id="31-standard--random-map"></a>
<a id="31-обычная-случайная-карта"></a>
<a id="обычная-случайная-карта"></a>
### 3.1 Standard/random map

The only automatic victory condition is **“only one team remains.”** The
game scans all players for a second living team. If none exists, the
survivors win and everyone else loses [^10].

Players on the same team win as soon as everyone on every other team has
been eliminated or has left. If only one team existed from the start, no
result is assigned, allowing a sandbox match.

All members of the winning team receive the team result, even players who
had already surrendered [^11].

<a id="32-scenario--campaign"></a>
<a id="32-сценарий-и-кампания"></a>
<a id="сценарий-и-кампания"></a>
### 3.2 Scenario/Campaign

Custom scenarios can declare victory or defeat for the current player
individually [^12] [^13]. Missions therefore have no single mandatory rule;
the map author defines the outcome.

A scenario can check the number of units in an area, resources, a counter, a
timer, or a flag [^14]. Objectives such as capturing a flag, accumulating
50,000 gold, holding a zone, or killing a commander can all be assembled
from these rules. See
[Scenarios and mission events](scenarios_and_triggers.md).

<a id="33-режимы-победы-из-других-rts-которых-в-c3-нет"></a>
<a id="33-режимы-победы-из-других-стратегий-которых-в-c3-нет"></a>
<a id="режимы-победы-из-других-стратегий-которых-в-cossacks-3-нет"></a>
### 3.3 Victory modes from other RTS that are not in C3

Players often expect these mechanics from Age of Empires II or the first
Cossacks games, but the standard Cossacks 3 rules do not use them:

- **Wonder of the World.** There is no standard building with a victory
  countdown. A scenario author can imitate one with a timer and an end-game
  action, but the game has no dedicated mode for it.
- **Diplomatic victory.** Victory depends on the teams chosen in the lobby.
  Changing diplomatic relationships during a scenario does not change those
  teams or end the match by itself [^15].
- **Score victory.** Points accumulate (see §5) but are used only for
  statistics and achievements; they determine neither the match result nor
  rating changes.
- **Win by time limit.** Ordinary matches limit pauses [^16], but have no
  overall duration limit. A scenario author can end a mission with a timer.

<a id="4-условия-поражения"></a>
## 4. Defeat conditions

The game periodically updates whether each participant still exists [^17].
This happens more often for an active player than for an inactive one.

The Historical Battle mode always treats the participant as alive. In other
modes, the decision begins with an internal occupied-population counter. It increases
once for every player-owned unit that is not a building and records neither
the number of buildings nor housing capacity.

- From 1 through 99, the game additionally looks for an eligible Peasant or
  Town Hall. If no Peasant remains but a Town Hall does, the player has
  **not** yet lost.
- At 100 or more, the participant is alive without that additional search.
- At zero, the participant loses even if buildings remain.

After declaring defeat, the game kills the participant's remaining units and
sends the result [^18].

In short, **a zero counter means defeat**, even if the player still owns a
Town Hall, Barracks, or other buildings. Zero establishes only that no
counted non-building units remain; it says nothing about surviving structures.
Historical Battle disables this automatic check, so defeat there comes only
from a scenario rule or surrender.

The counter increases when a counted unit appears and decreases when it dies,
is removed, or changes owner [^19].

<a id="5-начисление-очков"></a>
## 5. Point calculation

<a id="51-базовая-ценность-объекта"></a>
### 5.1 Base value of an object

Every object has a base point value [^20] [^21] [^23]. A Town Hall is worth
1,000 points [^22], for example, while a Peasant is worth 10 [^24].

<a id="52-накопление-при-убийстве"></a>
### 5.2 Points for kills and objects

When an **enemy** dies, the score gains twice the victim's value. Each unit
killed inside a building contributes three times its value [^25].

Capturing a new object adds five times its value; producing one adds its
base value [^26].

Losing a previously captured object deducts five times its value; transferring
a rebelling mercenary deducts three times its value; and an ordinary loss
deducts twice the value [^27]. The result cannot fall below zero.

<a id="53-live-сэмпл--временной-ряд"></a>
<a id="53-история-очков"></a>
### 5.3 Point history

Once every five game seconds, the game stores the current population and
score [^28]. These snapshots form the graphs on the final statistics screen.

<a id="54-использование-в-исходе-партии"></a>
### 5.4 Use in the outcome of the game

- In-game points **do not determine victory**; only the teams that remain
  matter.
- The leaderboard receives a fixed rating change rather than the difference
  between the points accumulated during the match [^29].

<a id="6-капитуляция"></a>
## 6. Surrender

Surrender immediately marks the player as defeated [^2]. Further handling
depends on the mode:

- **Server** — checks whether another team remains and tells the clients that
  the player has left.
- **Client** — sends a surrender request to the server.
- **Offline** — assigns defeat locally and immediately checks whether the
  match has ended.

There is no separate surrender chat command; the game uses an interface
action [^30].

The first player to leave during the first 15 minutes loses rating even if
their team eventually wins [^31]. In a two-player team, the leaver's partner
is not penalized.

<a id="7-ограничения-времени"></a>
## 7. Time limits and pauses

- **No match time limit.**
- **Pauses:** a player can pause at most four times for 120 seconds each
  [^16].
- **Publishing a result:** an unrated game shorter than ten minutes does not
  appear in the public log [^32].
- **Peacetime:** the available values are 0 / 10 / 15 / 20 / 30 / 45 / 60 /
  90 / 120 / 180 / 240 minutes [^33]. This is an attack ban at the start of
  the match, not an end-of-match timer. The full table is in
  [lobby settings](../../reports/map/lobby_settings.md#peacetime--время-мира);
  mechanics — [match settings](../world/map/game_settings.md#peacetime--как-устроен-мир).

<a id="8-multiplayer-specific-отличия"></a>
<a id="8-отличия-сетевой-игры"></a>
## 8. Multiplayer-specific differences

- The server sends victory or defeat to every client, publishes the result,
  and closes the session [^34].
- In rated rooms, the early-leaver coefficient is 1; in casual rooms it is 2
  [^35]. It applies to the **early-leaver penalty**, not to the score
  accumulated during the match.
- Casual games shorter than ten minutes do not publish a rating change
  (see §7).
- In a two-versus-two match, pairwise logic avoids penalizing the leaver's
  partner [^31].

<a id="9-сводка"></a>
## 9. Summary

| Topic | Meaning |
|---|---|
| **Default victory** | The last team standing wins. |
| **Default defeat** | No counted non-building unit remains. At counter values 1–99, the player additionally needs a Peasant or Town Hall. Disabled in Historical Battle. |
| **Wonder** | **Absent:** Cossacks 3 has no such victory mode or building. |
| **Score** | Accumulates for statistics and achievements but **does not determine the outcome**. A kill adds twice the victim's value, a killed garrison adds three times its value, a capture adds five times, and production adds the base value. Losses subtract between two and five times the value; the total cannot fall below zero. |
| **Time limit** | Absent; only peacetime and pause limits exist. |
| **Surrender** | The player is immediately defeated; the first player to leave during the first 15 minutes also loses rating. |
| **Scenario rules** | The mission author declares victory or defeat for the current player. |
| **Match types** | Random Map, Historical Battle, Campaign, Custom Scenario, and rated multiplayer add different ending rules. |

<a id="технические-подробности"></a>
## Technical details

An individual result is stored in `gc_player_victorystate_*`:
`none = 0`, `win = 1`, `lose = 2` [^3]. Map stages use
`gc_map_gamestage_*`; interface modes use `gc_gamemode_*` with
`mainmenu`, `game`, `editor`, `spectator`, `replay`, and
`endgamestatistics` [^4] [^5].

`gMap.bbattle` marks a Historical Battle, `gScenario.bactive` marks an active
scenario, and `gMap.brating`, `gInternetShell.bratingroom`, and `bautosearch`
mark rated-room paths [^6].

The main result check is `_misc_CheckEndGame` [^1]. Scenario actions
`gc_trigger_action_endgame_win = 47` and
`gc_trigger_action_endgame_lose = 48` apply to `myplind`. Surrender goes
through `_misc_Surrender` [^2].

<a id="источники"></a>
## Sources

All links are relative to `data/scripts/` in the Cossacks 3 installation.

[^1]: `_misc_CheckEndGame` — `lib/miscext2.script:3770`.

[^2]: `_misc_Surrender` — `lib/miscext2.script:3849-3896`:
    ```pascal
    gMap.players[plInd].bleave := True;
    if (_net_IsServer) then ...
       gPlayer[plind].victorystate := gc_player_victorystate_lose;
       if (not _misc_CheckEndGame) then ... LanSendParser(gc_LAN_GAME_SERVER_LEAVE, ...);
    else if (_net_IsClient) then
       LanSendParser(gc_LAN_GAME_SURRENDER, _parser_ParserEmpty);
    else if (_net_IsOffline) then
       gPlayer[plind].victorystate := gc_player_victorystate_lose;
       _misc_CheckEndGame;
    ```
[^3]: States `gc_player_victorystate_*` - `dmscript.global:777-779`:
    ```pascal
    gc_player_victorystate_none = 0;
    gc_player_victorystate_win  = 1;
    gc_player_victorystate_lose = 2;
    ```

[^4]: `gc_map_gamestage_*` — `dmscript.global:254-257`.

[^5]: `gc_gamemode_*` — `dmscript.global:242-247`:
    ```pascal
    gc_gamemode_mainmenu          = 0;
    gc_gamemode_game              = 1;
    gc_gamemode_editor            = 2;
    gc_gamemode_spectator         = 3;
    gc_gamemode_replay            = 4;
    gc_gamemode_endgamestatistics = 5;
    ```
[^6]: Flag `gMap.bbattle : Boolean` - `lib/classes.script:121`, `lib/miscext2.script:2645`.

[^7]: Disabling defeat check in Historical Battle - `units/global.inc/progress.inc:65-67`:
    ```pascal
    if (gMap.bbattle) then gPlayer[plind].bexists := True;
    ```
[^8]: Campaign catalog - `dmscript.global:1359, 1513-1522` (`gc_ach_campaign_finalaus..finalrus`, `data/game/var/campaigns.cfg`).

[^9]: Campaign progress record - `lib/scenario.script:3007-3062` (`TCampaignProgress.finished`, `lose`, `maxfinishdifficulty`).

[^10]: Main loop `_misc_CheckEndGame` - `lib/miscext2.script:3768-3845`:
    ```pascal
    function _misc_CheckEndGame() : Boolean;
    ...
       if (bSecondTeamExist) then ...
       if (bOneTeamLeft) then
       begin
          Result := True;
          ...
          gPlayer[i].victorystate := gc_player_victorystate_win;
          ...
          gPlayer[i].victorystate := gc_player_victorystate_lose;
          ...
          _misc_LanServerSendResults;
          _misc_LanCloseSessionSetScores;
       end;
    ```
[^11]: A team victory overwrites a previously assigned `lose` state —
    `lib/miscext2.script:3822-3827`.

[^12]: End-of-match trigger actions — `lib/classes.script:6334-6335`:
    ```pascal
    gc_trigger_action_endgame_win  = 47;
    gc_trigger_action_endgame_lose = 48;
    ```
[^13]: Implementation of `endgame_win`/`endgame_lose` for `myplind` - `lib/scenario.script:2995-3065`.

[^14]: List of available trigger conditions - `lib/classes.script:6251-6283`.

[^15]: Actions `playerSetAsAlly`/`Enemy`/`Neutral` - `lib/classes.script:6305-6307`.

[^16]: Pause limits - `dmscript.global:1662-1663`:
    ```pascal
    gc_pause_timelimit  = 120;
    gc_pause_countlimit = 4;
    ```
[^17]: Sub-tick check `bexists` — `units/global.inc/progress.inc:54-140`:
    ```pascal
    addtime := (0.125*plInd)+gc_global_TimeCheckExists*4   // active
    addtime := (0.125*plInd)+gc_global_TimeCheckExists*12  // inactive
    ...
    if (gMap.bbattle) then gPlayer[plind].bexists := True
    else
       var farmused := gPlayer[plInd].counter.farmused;
       if (farmused>0) and (farmused<100) then ...
       else
       gPlayer[plind].bexists := (farmused>0);
    ```
[^18]: Defeat branch in progress-tick - `units/global.inc/progress.inc:124-134`:
    ```pascal
    if (not gPlayer[plind].bexists) and ((bai) or (bhuman)) then
    begin
       if (GetPlayerGameObjectsCountByHandle(plHnd)>0) then _misc_KillPlayerUnits(plHnd);
       if (bPrevExists) then
       begin
          gPlayer[plind].victorystate := gc_player_victorystate_lose;
          ...
          _misc_LanServerSendResults;
       end;
    end;
    ```
[^19]: Increment/decrement `farmused` - `lib/unit.script:3905`.

[^20]: Field `score : Integer` in `TObjProp` is `lib/classes.script:3617`.

[^21]: Helper for buildings - `lib/unit.script:503` (`SetObjBuildingExtProperties(..., score, usage, ...)`).

[^22]: Town Hall score — `lib/unit.script:2371`:
    ```pascal
    SetObjBuildingExtProperties(objprop, objbase, 4000, 500, 300, True, 1000, gc_obj_usage_center, 0, 700, 700, 0, 0, 0)
    ```
[^23]: Helper for units - `lib/unit.script:571` (`SetObjBaseSearchBuildVisionScore(..., score)`).

[^24]: Peasant score — `lib/unit.script:636`:
    ```pascal
    SetObjBaseSearchBuildVisionScore(objprop, objbase, 700, 144, 1, 10)
    ```
[^25]: Accumulation on kill - `lib/miscext2.script:443-461`:
    ```pascal
    TObj(pobj2).hp <= 0:
       gPlayer[plInd].counter.scores += TObjProp(pobjprop2).score * 2;
       // plus all units inside the building (garrison)
       gPlayer[plInd].counter.scores += gObjProp[..].score * 3;
    ```
[^26]: Score added when an object appears — `lib/unit.script:3836-3841`:
    ```pascal
    var scoremodifier : Integer = bcaptured ? 5 : 1;
    gPlayer[pl].counter.scores += TObjProp(pobjprop).score * scoremodifier;
    ```
[^27]: Score deducted when an object is lost — `lib/unit.script:3939-3950`:
    ```pascal
    scoremodifier := bcaptured ? 5 : (brebellion and bmercenary ? 3 : 2);
    gPlayer[pl].counter.scores -= TObjProp(pobjprop).score * scoremodifier;
    if (gPlayer[pl].counter.scores<0) then gPlayer[pl].counter.scores := 0;
    ```
[^28]: Snapshot population/scores — `progress/progress.inc/nothing.inc:716-742`:
    ```pascal
    gPlayer[i].stat.population.Add(popul);   // farmused
    gPlayer[i].stat.scores.Add(score);       // counter.scores
    ```
[^29]: Leaderboard update — `lib/miscext2.script:3704-3766`
    (`_misc_LanCloseSessionSetScores`).

[^30]: Surrender protocol packets — `lib/classes.script:7569-7570`
    (`gc_LAN_GAME_SURRENDER = 10`, `gc_LAN_GAME_SURRENDER_CONFIRM = 11`).

[^31]: First-leaver penalty and two-versus-two logic —
    `lib/miscext2.script:3730-3757`:
    ```pascal
    if (firstleaverind=i) then LanSrvSetClientScore(... -w)   // leaver penalty
    case i of
       0: if firstleaverind<>1 ...
       1: if firstleaverind<>0 ...
       2: if firstleaverind<>3 ...
       3: if firstleaverind<>2 ...
    ```
[^32]: Grace period for publishing the result - `lib/miscext2.script:3712`:
    ```pascal
    if (gMap.brating) or (gt > 60*10) then ...
    ```
[^33]: Peacetime constants - `dmscript.global:1055-1066` (`gc_mapsettings_peacetime_*`, 11 values: 0..240 minutes).

[^34]: Distribution of the result - `lib/miscext2.script:3658-3686` (`_misc_LanServerSendResults`, package `gc_LAN_GAME_SESSION_RESULTS`).

[^35]: ELO-weight rated/casual - `lib/miscext2.script:3722-3725`.
