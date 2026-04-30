# Условия победы и конец партии

Источник: `C:\Program Files (x86)\Steam\steamapps\common\Cossacks 3\data\scripts\` (Steam-установка).

Главная функция, разрешающая исход партии — `_misc_CheckEndGame` в `lib\miscext2.script:3770`. Она вызывается каждый раз, когда меняется состояние «жив ли игрок» (см. §4) либо игрок капитулирует (`_misc_Surrender`, той же файл, строка 3849). Никаких альтернативных условий (Wonder, Score-cap, Time-cap, Capture-flag) в скриптах не реализовано — есть только сценарные триггеры (см. §3).

## 1. Состояния игрока

`dmscript.global:777-779`:
```
gc_player_victorystate_none = 0;
gc_player_victorystate_win  = 1;
gc_player_victorystate_lose = 2;
```

`gc_map_gamestage_*` (`dmscript.global:254-257`): `none / waitingloading / started / finished`.

`gc_gamemode_*` (`dmscript.global:242-247`):
```
gc_gamemode_mainmenu          = 0;
gc_gamemode_game              = 1;
gc_gamemode_editor            = 2;
gc_gamemode_spectator         = 3;
gc_gamemode_replay            = 4;
gc_gamemode_endgamestatistics = 5;
```

## 2. Game modes

В `gMap` есть флаг `bbattle : Boolean` (`classes.script:121`, `miscext2.script:2645`) — это «Историческая битва» (`Historical Battle`, ставится в `initmaphistoricalbattle.inc`). Скрипты различают:

* **Random map / skirmish** — обычный standard-режим.
* **Historical Battle** (`gMap.bbattle = True`) — fixed-army карта без сбора крестьян: `progress.inc:65-67` *«if (gMap.bbattle) then gPlayer[plind].bexists := True»* (т.е. defeat по «no peasants & no center» отключён, остаётся только сценарный trigger или surrender).
* **Campaign** — построена поверх scenario-системы; константы `gc_ach_campaign_finalaus..finalrus` и каталог `data\game\var\campaigns.cfg` (`dmscript.global:1359, 1513-1522`). Win/Lose кампании пишут в `TCampaignProgress.finished/lose/maxfinishdifficulty` (`scenario.script:3007-3062`).
* **Editor** (`gc_gamemode_editor`) и **Scenario Editor** (`gScenario.bactive`).
* **Battle / Rated MP** — флаги `gMap.brating`, `gInternetShell.bratingroom`, `bautosearch` (см. §6).
* **Replay / Spectator** — read-only режимы.

`gInterface.gamemode = gc_gamemode_endgamestatistics` (=5) — финальный экран статистики после выяснения исхода.

## 3. Условия победы

### 3.1 Standard / random map

Единственное автоматическое условие победы — **«осталась только одна команда»**. `miscext2.script:3768-3845`:

```
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

То есть **last-team-standing**: игроки одной команды (по полю `gPlayer[i].team`) выигрывают, как только все игроки других команд `not gMap.players[i].bexists or bleave`. Если изначально только одна команда (`not bSecondTeamExist`), функция ничего не присваивает — никто не побеждает (free-build / sandbox).

Игроки одной команды-победителя помечаются `win` все скопом (даже если на момент финала уже были lose от ранней капитуляции — `miscext2.script:3822-3827`).

### 3.2 Scenario / Campaign

Кастомные сценарии могут выдавать `win`/`lose` через trigger-actions (`classes.script:6334-6335`):
```
gc_trigger_action_endgame_win  = 47;
gc_trigger_action_endgame_lose = 48;
```
Реализация — `scenario.script:2995-3065`. Применяется только к `myplind` (текущему игроку), **поэтому в кастомных миссиях нет multi-player win-condition тригером** — каждый клиент сам поднимает флаг.

Доступные триггер-условия (`classes.script:6251-6283`) включают `unitsCountInZone`, `playerResources`, `counterValue`, `timerFinished`, `flagActive` и т. д. То есть «captured the flag», «reach 50000 gold», «hold zone for X seconds», «kill commander» и пр. — это всё реализуется автором сценария комбинацией триггеров; в движок зашиты только два терминальных action'а `endgame_win/lose`.

### 3.3 Режимы победы из других RTS, которых в C3 нет

Каждый пункт ниже — результат прямого греп-поиска по `data\scripts\`. Игроки часто ожидают эти механики из AoE2 / C1, но в C3 их нет:

* **Wonder of the World.** Слов `wonder`, `monument` в скриптах не найдено (grep по всей `data\scripts\` даёт 0 файлов). Здания-таймера обратного отсчёта в C3 нет. В сценарии эффект можно собрать из `timerFinished` + `endgame_win`, но как самостоятельного режима этой механики нет.
* **Дипломатическая победа.** `team` — статическая принадлежность из лобби, в рантайме не меняется. Сценарный action `playerSetAsAlly/Enemy/Neutral` (строки 6305-6307) переключает отношения, но не запускает проверку победы: `_misc_CheckEndGame` смотрит только на `team`, не на отношения.
* **Победа по очкам.** Score копится (см. §5), но используется только для статистики и ранкинга — в `_misc_CheckEndGame` он не читается.
* **Победа по тайм-лимиту.** Константа `gc_pause_timelimit = 120` (`dmscript.global:1662`) — это лимит **паузы**, а не игры (см. `gc_pause_countlimit = 4`). Глобального `gametimelimit` / `matchduration` в скриптах нет. В сценарии аналог собирается из `timerFinished` + `endgame_*`.

## 4. Defeat conditions

Главный код — `units\global.inc\progress.inc:54-140` (sub-tick state-machine, секция `Progress`, исполняется на каждый «player tick»). Условие «игрок ещё существует» хранится в `gPlayer[plInd].bexists`.

```
addtime := (0.125*plInd)+gc_global_TimeCheckExists*4   // активен
addtime := (0.125*plInd)+gc_global_TimeCheckExists*12  // не активен
```
То есть проверка делается с интервалом ~`gc_global_TimeCheckExists` × 4..12 game-сек. Логика:

```
if (gMap.bbattle) then gPlayer[plind].bexists := True   // в HB всегда «жив»
else
   var farmused := gPlayer[plInd].counter.farmused;     // занятые слоты пехоты
   if (farmused>0) and (farmused<100) then ...
       // редкий частный случай: ищет ХОТЯ БЫ ОДНОГО peasant'а или центра (cen)
       // → если нашёл — bexists=True; иначе bexists=False
   else
   gPlayer[plind].bexists := (farmused>0);
```

Затем (`progress.inc:124-134`):
```
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

Итог: **defeat = `farmused == 0`**, т. е. у игрока нет ни одного **peasant** и ни одного центра/населённой постройки, при двух нюансах:
* «Частичный» случай (`0 < farmused < 100`): движок вручную ищет хотя бы один объект usage `gc_obj_usage_center` (Городской центр) или peasant с `bvisual_none + bessential_none` (флаги «настоящая боевая единица»). Если peasant'ов нет, но Городской центр есть — игрок ещё **не** проигрывает.
* В Historical Battle (`bbattle`) этот код не работает — там defeat ставится только сценарным триггером или surrender'ом.

После смерти все юниты игрока физически убиваются (`_misc_KillPlayerUnits`).

`farmused` инкрементируется при появлении любого playable-юнита (в т. ч. peasant) и декрементируется при смерти/удалении (`unit.script:3905`).

## 5. Score formula

### 5.1 Per-object base score
Каждый `TObjProp` имеет поле `score : Integer` (`classes.script:3617`). Задаётся через помощники:
* `SetObjBuildingExtProperties(..., score, usage, ...)` (`unit.script:503`) — для зданий.
  - Городской центр (`cen`): score = 1000 (`unit.script:2371`: `SetObjBuildingExtProperties(objprop, objbase, 4000, 500, 300, True, 1000, gc_obj_usage_center, 0, 700, 700, 0, 0, 0)`).
* `SetObjBaseSearchBuildVisionScore(..., score)` (`unit.script:571`) — для юнитов.
  - Peasant: score = 10 (`unit.script:636`: `SetObjBaseSearchBuildVisionScore(objprop, objbase, 700, 144, 1, 10)`).

(Полная таблица score per-sid — это уже задача для извлекалки из xlsx, но grep по `\.score :=` всего 2 присвоения в `unit.script` — оба через эти helper-процедуры, так что аккуратное парсение SetObj* call-сайтов даст значения для всех юнитов/зданий.)

### 5.2 Накопление при убийстве

При смерти **врага** (попадание снаряда в юнита, `miscext2.script:443-461`):
```
TObj(pobj2).hp <= 0:
   gPlayer[plInd].counter.scores += TObjProp(pobjprop2).score * 2;
   // плюс за всех юнитов внутри здания (гарнизон)
   gPlayer[plInd].counter.scores += gObjProp[..].score * 3;
```

То есть **kill = +2× score** жертвы, **kill garrisoned unit = +3× score**.

При появлении нового объекта у игрока (`unit.script:3836-3841`):
```
var scoremodifier : Integer = bcaptured ? 5 : 1;
gPlayer[pl].counter.scores += TObjProp(pobjprop).score * scoremodifier;
```
(score за **производство** = +1× score; за **захват** чужого = +5×.)

При потере объекта (`unit.script:3939-3950`):
```
scoremodifier := bcaptured ? 5 : (brebellion and bmercenary ? 3 : 2);
gPlayer[pl].counter.scores -= TObjProp(pobjprop).score * scoremodifier;
if (gPlayer[pl].counter.scores<0) then gPlayer[pl].counter.scores := 0;
```

Свод: при **смерти** своего юнита = −2× (или −3× если это сбежавший наёмник в восстании, или −5× если был захвачен).

Score не уходит в минус.

### 5.3 Live-сэмпл / временной ряд

В `progress\progress.inc\nothing.inc:716-742` каждые `gc_progress_TimeProgressStatistics` секунд (раз в 5 сек игрового времени) пишется снимок:
```
gPlayer[i].stat.population.Add(popul);   // farmused
gPlayer[i].stat.scores.Add(score);       // counter.scores
```
Это даёт хронограмму очков и населения для финального экрана статистики.

### 5.4 Использование в исходе партии

* `_misc_CheckEndGame` **score не использует** — победа определяется только по командам.
* `_misc_LanCloseSessionSetScores` (`miscext2.script:3704-3766`) использует **±1/±2** (rated/нет) для отправки на лидерборд. То есть в multiplayer-rated рейтинг ELO движется на единицу, а не на разницу score.

## 6. Resignation / Surrender

Хоткей в UI вызывает `_misc_Surrender(blanterminate)` (`miscext2.script:3849-3896`):

```
gMap.players[plInd].bleave := True;        // помечен как «ушёл»
if (_net_IsServer) then ...
   gPlayer[plind].victorystate := gc_player_victorystate_lose;
   if (not _misc_CheckEndGame) then ... LanSendParser(gc_LAN_GAME_SERVER_LEAVE, ...);
else if (_net_IsClient) then
   LanSendParser(gc_LAN_GAME_SURRENDER, _parser_ParserEmpty);   // const = 10
else if (_net_IsOffline) then
   gPlayer[plind].victorystate := gc_player_victorystate_lose;
   _misc_CheckEndGame;
```

Нет «/resign»-чат-команды (grep `resign` в скриптах = 0 матчей). Функция вызывается только из ENG (бинарного движка) — судя по всему, это «сдаться» в game-меню. `gc_LAN_GAME_SURRENDER = 10` и `gc_LAN_GAME_SURRENDER_CONFIRM = 11` (`classes.script:7569-7570`) — пакеты протокола.

«First leaver» — первый сдавшийся в первые 15 мин — теряет **−2× ELO** даже если его команда выиграет (`miscext2.script:3730-3756`):
```
if (firstleaverind=i) then LanSrvSetClientScore(... -w)   // штраф ливеру
```
а напарнику ливера в команде из 2-х наоборот ELO **не списывают**, чтобы не наказывать «жертву» дезертирства.

## 7. Time / turn limits

* **Game time-limit: отсутствует.** Никакой `gametimelimit` в скриптах нет.
* **Pause-time-limit:** `gc_pause_timelimit = 120` сек, `gc_pause_countlimit = 4` (`dmscript.global:1662-1663`) — паузу можно ставить максимум 4 раза по 120 сек, дальше движок отказывается ставить.
* **Score-history grace:** В rated-комнатах счётчик результата отправляется только если `gMap.brating OR gt > 60*10` (`miscext2.script:3712`) — т. е. в нерейтинговых играх, длившихся <10 мин, итог в публичный лог не идёт (анти-фермерство ачивок).
* **Peacetime:** `gc_mapsettings_peacetime_*` (`dmscript.global:1055-1066`) — 0 / 10 / 15 / 20 / 30 / 45 / 60 / 90 / 120 / 180 / 240 минут. Это запрет атаки в первые N минут, а не таймер конца игры. Полная таблица — [`reports/map/lobby_settings.md`](../reports/map/lobby_settings.md#peacetime--время-мира); механика — [`game_settings.md`](game_settings.md#peacetime--как-устроен-мир).

## 8. Multiplayer-specific отличия

* `_misc_LanServerSendResults` рассылает win/lose всем клиентам пакетом `gc_LAN_GAME_SESSION_RESULTS` (`miscext2.script:3658-3686`).
* `_misc_LanCloseSessionSetScores` обновляет публичный рейтинг (только при `_net_IsServer`), `LanPublicServerCloseSession` закрывает сессию.
* В rated-комнатах (`gMap.brating`) ELO-вес = 1, в casual-комнатах вес = 2 (`miscext2.script:3722-3725`) — на первый взгляд парадокс, но это про **штраф** ливеру: за casual-ливерство наказание сильнее, видимо, чтобы поощрять ranked-режим.
* В casual-играх <10 мин — `LanSrvSetClientScore` не вызывается (см. §7).
* Для 2v2 предусмотрена попарная логика «не штрафуй напарника ливера»: `case i of 0: if firstleaverind<>1 ... 1: if firstleaverind<>0 ... 2: if firstleaverind<>3 ... 3: if firstleaverind<>2` (`miscext2.script:3740-3757`) — т.е. команды по умолчанию `{0,1}` vs `{2,3}`.

## 9. Сводка

| Тема | Значение |
|---|---|
| **Default victory** | last-team-standing (`_misc_CheckEndGame`, `miscext2.script:3770`). |
| **Default defeat** | `farmused = 0` AND нет peasant'а / Городского центра в собственности (`progress.inc:54-140`). В Historical Battle отключено. |
| **Wonder** | **отсутствует** (нет такого режима/здания в C3, в отличие от AoE2). |
| **Score** | копится для статистики/ачивок, **не определяет исход**. Формула: kill=+2×score, kill garrisoned=+3×score, capture=+5×score, build=+1×score; loss=−2×, captured-from=−5×, rebel-merc=−3×; clamp `>=0`. |
| **Time-limit** | отсутствует (есть только peacetime, pause-limit). |
| **Surrender** | `_misc_Surrender` ставит `bleave=True` + `victorystate=lose` + триггерит `_misc_CheckEndGame`. Первый ливер в первые 15 мин получает −w ELO. |
| **Scenario triggers** | `endgame_win=47`, `endgame_lose=48`, применяются только к `myplind` (per-client). |
| **Game modes** | mainmenu / game / editor / spectator / replay / endgamestatistics (`gc_gamemode_*`). Поверх — Random map, Historical Battle (`gMap.bbattle`), Campaign, Custom Scenario, Rated MP (`gMap.brating`). |

## 10. Open questions

1. **Полная таблица per-sid score** — нужно распарсить все ~3000 SetObjBuildingExtProperties / SetObjBaseSearchBuildVisionScore call-сайтов, чтобы сложить значения. Сейчас известно: peasant=10, town hall=1000.
2. **Bridge между бинарным движком и `_misc_Surrender`** — где именно вызывается? GUI button name? (предполагается, что это резерв menu-кнопки «Surrender», не доступной отдельным хоткеем).
3. **`lastattacktime`-music** ↔ defeat: когда атакован, `gc_gui_battlemusicinterval - gc_gui_underattackalarminterval` — нужно вычислить интервал для тулзы «alert».
4. **Gamestage transition `started → finished`** — кто его триггерит? `_misc_CheckEndGame` не пишет gamestage; видимо, это бинарный движок после `gc_gamemode_endgamestatistics`.
5. **«1 человек на команде» победа?** Если в стартовой расстановке 1v1 без союзников и враг капитулирует на 5-й сек — `_misc_CheckEndGame` всё ещё работает (одна команда из выживших). Если же изначально стояла «sandbox» (1 player), функция ранний `exit` через `not bSecondTeamExist` — проверить эмпирически.
6. **Что точно делает «Score» в финальном экране** — отображается ли как формула или как сэмплированный таймсериес из `stat.scores`? (UI extension не извлекался.)
