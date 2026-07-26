<a id="recon-условия-победы-и-конец-партии"></a>
# Recon: victory conditions and end of game

Reverse engineering the conditions under which a game ends in Cossacks 3:
who is declared the winner, who is the loser, how the score is calculated and what
There are no victory modes from other RTS in C3. All links to the code themselves
Pascal blocks are collected in the [Sources](#sources) section at the end of the document.

## TL;DR

- The main function that resolves the outcome of the game is `_misc_CheckEndGame` [^1].
  It is called when the "player is alive" state changes (§4) or when
  the player capitulates via `_misc_Surrender` [^2].
- Alternative conditions (`Wonder`, Score cap, Time cap, Capture-the-flag)
  in scripts **no** - only last-team-standing and script triggers
  (§3).
- `farmused = 0` ⇒ defeat, but `farmused` does not fall to 0 while there is at least
  one peasant **or** Town Hall.
- Score is accumulated only for statistics and ELO, it does not affect the outcome of the game
  (§5.4).

<a id="1-состояния-игрока"></a>
## 1. Player states

The constants `gc_player_victorystate_*` set the outcome for an individual player:
`none = 0`, `win = 1`, `lose = 2` [^3].

The map stage `gc_map_gamestage_*` distinguishes between `none/waitingloading/
started / finished` [^4]. Global interface mode
`gc_gamemode_*` distinguishes six states: `mainmenu`, `game`, `editor`,
`spectator`, `replay`, `endgamestatistics` [^5]. Final screen
statistics after finding out the outcome is `gInterface.gamemode =
gc_gamemode_endgamestatistics` (=5).

## 2. Game modes

`gMap` has a flag `bbattle : Boolean` [^6] is a “Historical Battle”
(`Historical Battle`, placed in `initmaphistoricalbattle.inc`). Scripts
distinguish:

- **Random map / skirmish** - normal standard mode.
- **Historical Battle** (`gMap.bbattle = True`) — fixed-army map without
  gathering peasants: defeat by “no peasants & no center” is disabled, remains
  only scenario trigger or surrender [^7].
- **Campaign** - built on top of the scenario system; constants
  `gc_ach_campaign_finalaus..finalrus` and catalog
  `data/game/var/campaigns.cfg` [^8]. Win/Lose campaigns write in
  `TCampaignProgress.finished`, `lose`, `maxfinishdifficulty` [^9].
- **Editor** (`gc_gamemode_editor`) and **Scenario Editor**
  (`gScenario.bactive`).
- **Battle / Rated MP** - flags `gMap.brating`,
  `gInternetShell.bratingroom`, `bautosearch` (see §6).
- **Replay / Spectator** - read-only modes.

<a id="3-условия-победы"></a>
## 3. Victory conditions

<a id="31-standard--random-map"></a>
### 3.1 Standard/random map

The only automatic victory condition is **“only one left
team"**. Function `_misc_CheckEndGame` goes through all players, looking for
a second living team, and if there is none, assigns it to the survivors
`gc_player_victorystate_win`, the rest `gc_player_victorystate_lose`
[^10].

That is, **last-team-standing**: players of one team (across the field
`gPlayer[i].team`) win as soon as all players of other teams
meet the condition `not gMap.players[i].bexists or bleave`. If initially
only one command (`not bSecondTeamExist`), function nothing
assigns - no one wins (free-build / sandbox).

Players on the same winning team are marked `win` all together - even if
at the time of the final there were already `lose` from the early surrender of [^11].

<a id="32-scenario--campaign"></a>
### 3.2 Scenario/Campaign

Custom scripts can issue `win`/`lose` via trigger-actions
`gc_trigger_action_endgame_win = 47` and
`gc_trigger_action_endgame_lose = 48` [^12]. Implementation - in
`scenario.script` [^13]. Applies only to `myplind` (current
player), **therefore, there is no multi-player win-condition in custom missions
trigger** - each client raises the flag himself.

Available trigger conditions [^14] include `unitsCountInZone`,
`playerResources`, `counterValue`, `timerFinished`, `flagActive` and so on
further. That is, “captured the flag”, “reach 50000 gold”, “hold zone for X
seconds", "kill commander" - all this is implemented by the author of the script
combination of triggers; Only two terminal actions are hardwired into the engine
`endgame_win` and `endgame_lose`.

<a id="33-режимы-победы-из-других-rts-которых-в-c3-нет"></a>
### 3.3 Victory modes from other RTS that are not in C3

Each item below is the result of a direct grep search for `data/scripts/`.
Players often expect these mechanics from AoE2/C1, but they are not present in C3:

- **Wonder of the World.** The words `wonder`, `monument` are not in the scripts
  found (grep throughout `data/scripts/` gives 0 files). Timer buildings
  There is no countdown in C3. In a script, the effect can be collected from
  `timerFinished` + `endgame_win`, but as an independent mode of this
  no mechanics.
- **Diplomatic victory.** `team` - static affiliation from
  lobby does not change in runtime. Scenario action
  `playerSetAsAlly`/`Enemy`/`Neutral` [^15] switches relationships, but not
  runs a victory check: `_misc_CheckEndGame` looks only at
  `team`, not for relationships.
- **Win by points.** Score accumulates (see §5), but is only used
  for statistics and ranking - it is not readable in `_misc_CheckEndGame`.
- **Win by time limit.** Constant `gc_pause_timelimit = 120` [^16] —
  this is a **pause** limit, not a game limit (`gc_pause_countlimit = 4` on the same
  lines). Global `gametimelimit` / `matchduration` in scripts
  no. In the scenario, the analogue is assembled from `timerFinished` + `endgame_*`.

## 4. Defeat conditions

Main code - sub-tick state-machine in `progress.inc`, section `Progress`
[^17], executed on every “player tick”. The condition “the player is still
exists" is stored in `gPlayer[plInd].bexists`. The check is done with
at intervals of approximately `gc_global_TimeCheckExists × 4..12` game seconds
(`×4` for active player, `×12` for inactive player).

The logic is this. For Historical Battle (`gMap.bbattle`) the player always
marked alive. Otherwise, take `farmused` (occupied infantry slots), and:

- if `0 < farmused < 100` - the engine manually searches for at least one object with
  usage `gc_obj_usage_center` (Town Hall) or peasant with
  flags “real combat unit” (`bvisual_none + bessential_none`).
  If there are no peasants, but Town Hall is there, the player is **not** yet
  loses.
- otherwise `bexists := (farmused > 0)`.

If `bexists` fell to `False` and the player was alive on the previous tick, he
is set to `gc_player_victorystate_lose`, all of it is physically killed
units via `_misc_KillPlayerUnits`, the result [^18] is sent.

Result: **defeat = `farmused == 0`**, that is, the player does not have any
a peasant and not a single center/populated building, with two nuances:

- “Partial” case - `0 < farmused < 100` - above.
- In Historical Battle (`bbattle`) this code does not work - there is defeat
  can only be set by a script trigger or surrender.

`farmused` is incremented when any playable unit appears (including
including the peasant) and is decremented upon death/deletion of [^19].

## 5. Score formula

### 5.1 Per-object base score

Each `TObjProp` has a field `score : Integer` [^20]. Set via
assistants:

- `SetObjBuildingExtProperties(..., score, usage, ...)` [^21] - for
  buildings. Town Hall (`cen`) receives `score = 1000` [^22].
- `SetObjBaseSearchBuildVisionScore(..., score)` [^23] - for units.
  Peasant receives `score = 10` [^24].

The full score per-sid table requires parsing all calls
`SetObjBuildingExtProperties` and `SetObjBaseSearchBuildVisionScore`. Search
by `.score :=` to `unit.script` shows only two direct assignments,
both through these helper procedures, so accurate parsing of call sites
will give values ​​for all units and buildings.

<a id="52-накопление-при-убийстве"></a>
### 5.2 Accumulation on Kill

When an **enemy** dies - a projectile hits a unit - score
`gPlayer[plInd].counter.scores` grows by `victim score × 2`, plus more
`× 3` for each unit inside the building (garrison) [^25].

That is, **kill = +2× victim score**, **kill garrisoned unit = +3×
score**.

When a new object appears, the player’s score increases with the modifier: `+5×`
during capture, `+1×` during production [^26].

When an object is lost, the score is reduced with the modifier: `−5×` if it was
captured, `−3×` if it is an escaped mercenary in the uprising
(`brebellion and bmercenary`), otherwise `−2×` [^27]. Score does not go to
minus - clamp at zero there.

<a id="53-live-сэмпл--временной-ряд"></a>
### 5.3 Live sample/time series

Every `gc_progress_TimeProgressStatistics` seconds (every 5 seconds
game time) a snapshot of `farmused` and `counter.scores` is written in
`gPlayer[i].stat.population` and `gPlayer[i].stat.scores` [^28]. This gives
score and population chronogram for the final statistics screen.

<a id="54-использование-в-исходе-партии"></a>
### 5.4 Use in the outcome of the game

- `_misc_CheckEndGame` **score does not use** - victory is determined
  only by command.
- `_misc_LanCloseSessionSetScores` uses **±1/±2** (rated/not) for
  sending to the leaderboard [^29]. That is, in the multiplayer-rated ELO rating
  moves by one, not by the score difference.

## 6. Resignation / Surrender

The hotkey in the UI calls `_misc_Surrender(blanterminate)` [^2]. Function
puts `gMap.players[plInd].bleave := True`, and then forks along
network role:

- **Server** — assigns `gPlayer[plind].victorystate :=
  gc_player_victorystate_lose`, calls `_misc_CheckEndGame`; if
  the batch has not finished - sends out `gc_LAN_GAME_SERVER_LEAVE`.
- **Client** — sends the `gc_LAN_GAME_SURRENDER` (=10) packet to the server.
- **Offline** — assigns `lose` locally and immediately calls
  `_misc_CheckEndGame`.

There is no chat command `/resign` - grep by `resign` in scripts gives 0 matches.
The function is called only from ENG (binary engine), apparently this is
“Surrender” button in the game menu. Protocol constants `gc_LAN_GAME_SURRENDER
= 10` and `gc_LAN_GAME_SURRENDER_CONFIRM = 11` [^30].

“First leaver” - the first one to surrender in the first 15 minout - loses **−w ELO**
even if his team wins [^31]. And the liver's partner in the team from
two on the contrary ELO **are not written off** so as not to punish the “victim”
desertion.

## 7. Time / turn limits

- **Game time-limit: absent.** No `gametimelimit` in scripts
  no.
- **Pause-time-limit:** `gc_pause_timelimit = 120` sec,
  `gc_pause_countlimit = 4` [^16] - you can pause a maximum of 4 times
  for 120 seconds, then the engine refuses.
- **Score-history grace:** result counter in rated rooms
  sent only if `gMap.brating OR gt > 60*10` [^32] - then
  available in unrated games with a duration of less than 10 min total in
  There is no public log (anti-farming achievements).
- **Peacetime:** `gc_mapsettings_peacetime_*` [^33] —
  0 / 10 / 15 / 20 / 30 / 45 / 60 / 90 / 120 / 180 / 240 minutes. This
  attack ban in the first N minutes, not an end-of-game timer. Full table -
  [`reports/map/lobby_settings.md`](../../reports/map/lobby_settings.md#peacetime--время-мира);
  mechanics - [`game_settings.md`](../world/map/game_settings.md#peacetime--как-устроен-мир).

<a id="8-multiplayer-specific-отличия"></a>
## 8. Multiplayer-specific differences

- `_misc_LanServerSendResults` sends win/lose to all clients in a package
  `gc_LAN_GAME_SESSION_RESULTS` [^34].
- `_misc_LanCloseSessionSetScores` updates public rating (only
  at `_net_IsServer`), `LanPublicServerCloseSession` closes the session.
- In rated rooms (`gMap.brating`) ELO-weight = 1, in casual rooms
weight = 2 [^35]. At first glance it’s a paradox, but this is about the **fine** for the liver:
  for casual cheating the punishment is stronger, apparently to encourage
  ranked-mode.
- In casual games lasting less than 10 min, `LanSrvSetClientScore` is not
  called (see §7).
- For 2v2, pairwise logic “don’t penalize the liver’s partner” is provided
  [^31] - default commands `{0,1}` vs `{2,3}`.

## 9. Summary

| Topic | Meaning |
|---|---|
| **Default victory** | last-team-standing (`_misc_CheckEndGame`). |
| **Default defeat** | `farmused = 0` AND no peasant/Urban center owned. Disabled in Historical Battle. |
| **Wonder** | **missing** (there is no such mode/building in C3, unlike AoE2). |
| **Score** | accumulates for statistics and achievements, **does not determine the outcome**. Formula: kill = +2× score, kill garrisoned = +3× score, capture = +5× score, build = +1× score; loss = −2×, captured-from = −5×, rebel-merc = −3×; clamp at zero. |
| **Time-limit** | absent (there are only peacetime, pause-limit). |
| **Surrender** | `_misc_Surrender` sets `bleave = True`, `victorystate = lose`, trigger `_misc_CheckEndGame`. The first liver in the first 15 minut receives −w ELO. |
| **Scenario triggers** | `endgame_win = 47`, `endgame_lose = 48`, apply only to `myplind` (per-client). |
| **Game modes** | `mainmenu` / `game` / `editor` / `spectator` / `replay` / `endgamestatistics`. On top - Random map, Historical Battle (`gMap.bbattle`), Campaign, Custom Scenario, Rated MP (`gMap.brating`). |

## 10. Open questions

| # | Question | Where to dig |
|---:|---|---|
| 1 | Full per-sid score table: you need to parse all approximately 3000 calls `SetObjBuildingExtProperties` / `SetObjBaseSearchBuildVisionScore`. Now we know: peasant = 10, Town Hall = 1000. | Call site parser in `unit.script`. |
| 2 | Bridge between the binary engine and `_misc_Surrender` - where exactly is the GUI button called? It is assumed that this is the “Surrender” button in the game menu without a separate hotkey. | GUI callbacks in native binary. |
| 3 | `lastattacktime`-music ↔ defeat: when attacked, the interval `gc_gui_battlemusicinterval - gc_gui_underattackalarminterval` is for the “alert” tool. | Direct calculation using constants. |
| 4 | Gamestage transition `started → finished` - who triggers it? `_misc_CheckEndGame` does not write gamestage; Apparently this is a binary engine after `gc_gamemode_endgamestatistics`. | End-of-batch network protocol profiling. |
| 5 | “1 person per team” victory? If the starting setup is 1v1 without allies and the enemy capitulates at the 5th second, `_misc_CheckEndGame` still works (one team of survivors). If initially there was “sandbox” (1 player), the function early `exit` through `not bSecondTeamExist` should be checked empirically. | Empirically in the editor. |
| 6 | What exactly does "Score" do in the final screen - is it displayed as a formula or as a sampled timeseries from `stat.scores`? | UI extension was not extracted. |

---

## Sources

All links are relative to `data/scripts/` in the Cossacks 3 installation.

[^1]: `_misc_CheckEndGame` - `lib/miscext2.script:3770`.

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
[^11]: Overlapping the previously placed `lose` with a team victory - `lib/miscext2.script:3822-3827`.

[^12]: Trigger actions of the end of the party - `lib/classes.script:6334-6335`:
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
    addtime := (0.125*plInd)+gc_global_TimeCheckExists*4   // активен
    addtime := (0.125*plInd)+gc_global_TimeCheckExists*12  // не активен
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

[^22]: City Center Score - `lib/unit.script:2371`:
    ```pascal
    SetObjBuildingExtProperties(objprop, objbase, 4000, 500, 300, True, 1000, gc_obj_usage_center, 0, 700, 700, 0, 0, 0)
    ```
[^23]: Helper for units - `lib/unit.script:571` (`SetObjBaseSearchBuildVisionScore(..., score)`).

[^24]: Peasant Score - `lib/unit.script:636`:
    ```pascal
    SetObjBaseSearchBuildVisionScore(objprop, objbase, 700, 144, 1, 10)
    ```
[^25]: Accumulation on kill - `lib/miscext2.script:443-461`:
    ```pascal
    TObj(pobj2).hp <= 0:
       gPlayer[plInd].counter.scores += TObjProp(pobjprop2).score * 2;
       // плюс за всех юнитов внутри здания (гарнизон)
       gPlayer[plInd].counter.scores += gObjProp[..].score * 3;
    ```
[^26]: Accumulation when an object appears - `lib/unit.script:3836-3841`:
    ```pascal
    var scoremodifier : Integer = bcaptured ? 5 : 1;
    gPlayer[pl].counter.scores += TObjProp(pobjprop).score * scoremodifier;
    ```
[^27]: Write-off when an object is lost - `lib/unit.script:3939-3950`:
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
[^29]: Entry on the leaderboard - `lib/miscext2.script:3704-3766` (`_misc_LanCloseSessionSetScores`).

[^30]: Delivery protocol packages - `lib/classes.script:7569-7570` (`gc_LAN_GAME_SURRENDER = 10`, `gc_LAN_GAME_SURRENDER_CONFIRM = 11`).

[^31]: Penalty to the first leaver and 2v2 logic - `lib/miscext2.script:3730-3757`:
    ```pascal
    if (firstleaverind=i) then LanSrvSetClientScore(... -w)   // штраф ливеру
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
