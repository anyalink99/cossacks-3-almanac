# Победа, поражение и завершение партии

[← Как устроена игра](../README.md)

Реверс-инжиниринг условий, при которых партия в Cossacks 3 заканчивается:
кто объявляется победителем, кто проигравшим, как считается счёт и какие
режимы победы из других RTS в C3 отсутствуют. Все ссылки на код и сами
Pascal-блоки собраны в разделе [Источники](#источники) в конце документа.

## TL;DR

- Главная функция, разрешающая исход партии — `_misc_CheckEndGame` [^1].
  Она вызывается, когда меняется состояние «жив ли игрок» (§4) или когда
  игрок капитулирует через `_misc_Surrender` [^2].
- Альтернативных условий (`Wonder`, Score cap, Time cap, Capture-the-flag)
  в скриптах **нет** — только last-team-standing и сценарные триггеры
  (§3).
- `farmused = 0` ⇒ defeat, но `farmused` не падает в 0, пока есть хоть
  один крестьянин **или** Городской центр.
- Score копится только для статистики и ELO, на исход партии не влияет
  (§5.4).

## 1. Состояния игрока

Константы `gc_player_victorystate_*` задают исход для отдельного игрока:
`none = 0`, `win = 1`, `lose = 2` [^3].

Стадия карты `gc_map_gamestage_*` различает `none / waitingloading /
started / finished` [^4]. Глобальный режим интерфейса
`gc_gamemode_*` различает шесть состояний: `mainmenu`, `game`, `editor`,
`spectator`, `replay`, `endgamestatistics` [^5]. Финальный экран
статистики после выяснения исхода — это `gInterface.gamemode =
gc_gamemode_endgamestatistics` (=5).

## 2. Game modes

В `gMap` есть флаг `bbattle : Boolean` [^6] — это «Историческая битва»
(`Historical Battle`, ставится в `initmaphistoricalbattle.inc`). Скрипты
различают:

- **Random map / skirmish** — обычный standard-режим.
- **Historical Battle** (`gMap.bbattle = True`) — fixed-army карта без
  сбора крестьян: defeat по «no peasants & no center» отключён, остаётся
  только сценарный trigger или surrender [^7].
- **Campaign** — построена поверх scenario-системы; константы
  `gc_ach_campaign_finalaus..finalrus` и каталог
  `data/game/var/campaigns.cfg` [^8]. Win/Lose кампании пишут в
  `TCampaignProgress.finished`, `lose`, `maxfinishdifficulty` [^9].
- **Editor** (`gc_gamemode_editor`) и **Scenario Editor**
  (`gScenario.bactive`).
- **Battle / Rated MP** — флаги `gMap.brating`,
  `gInternetShell.bratingroom`, `bautosearch` (см. §6).
- **Replay / Spectator** — read-only режимы.

## 3. Условия победы

### 3.1 Standard / random map

Единственное автоматическое условие победы — **«осталась только одна
команда»**. Функция `_misc_CheckEndGame` проходит по всем игрокам, ищет
вторую живую команду, и если её нет — присваивает выжившим
`gc_player_victorystate_win`, остальным `gc_player_victorystate_lose`
[^10].

То есть **last-team-standing**: игроки одной команды (по полю
`gPlayer[i].team`) выигрывают, как только все игроки других команд
отвечают условию `not gMap.players[i].bexists or bleave`. Если изначально
только одна команда (`not bSecondTeamExist`), функция ничего не
присваивает — никто не побеждает (free-build / sandbox).

Игроки одной команды-победителя помечаются `win` все скопом — даже если
на момент финала уже были `lose` от ранней капитуляции [^11].

### 3.2 Scenario / Campaign

Кастомные сценарии могут выдавать `win`/`lose` через trigger-actions
`gc_trigger_action_endgame_win = 47` и
`gc_trigger_action_endgame_lose = 48` [^12]. Реализация — в
`scenario.script` [^13]. Применяется только к `myplind` (текущему
игроку), **поэтому в кастомных миссиях нет multi-player win-condition
триггера** — каждый клиент сам поднимает флаг.

Доступные триггер-условия [^14] включают `unitsCountInZone`,
`playerResources`, `counterValue`, `timerFinished`, `flagActive` и так
далее. То есть «captured the flag», «reach 50000 gold», «hold zone for X
seconds», «kill commander» — всё это реализуется автором сценария
комбинацией триггеров; в движок зашиты только два терминальных action'а
`endgame_win` и `endgame_lose`.

### 3.3 Режимы победы из других RTS, которых в C3 нет

Каждый пункт ниже — результат прямого греп-поиска по `data/scripts/`.
Игроки часто ожидают эти механики из AoE2 / C1, но в C3 их нет:

- **Wonder of the World.** Слов `wonder`, `monument` в скриптах не
  найдено (grep по всей `data/scripts/` даёт 0 файлов). Здания-таймера
  обратного отсчёта в C3 нет. В сценарии эффект можно собрать из
  `timerFinished` + `endgame_win`, но как самостоятельного режима этой
  механики нет.
- **Дипломатическая победа.** `team` — статическая принадлежность из
  лобби, в рантайме не меняется. Сценарный action
  `playerSetAsAlly`/`Enemy`/`Neutral` [^15] переключает отношения, но не
  запускает проверку победы: `_misc_CheckEndGame` смотрит только на
  `team`, не на отношения.
- **Победа по очкам.** Score копится (см. §5), но используется только
  для статистики и ранкинга — в `_misc_CheckEndGame` он не читается.
- **Победа по тайм-лимиту.** Константа `gc_pause_timelimit = 120` [^16] —
  это лимит **паузы**, а не игры (`gc_pause_countlimit = 4` на тех же
  строках). Глобального `gametimelimit` / `matchduration` в скриптах
  нет. В сценарии аналог собирается из `timerFinished` + `endgame_*`.

## 4. Defeat conditions

Главный код — sub-tick state-machine в `progress.inc`, секция `Progress`
[^17], исполняется на каждый «player tick». Условие «игрок ещё
существует» хранится в `gPlayer[plInd].bexists`. Проверка делается с
интервалом примерно `gc_global_TimeCheckExists × 4..12` игровых секунд
(`×4` для активного игрока, `×12` для неактивного).

Логика такая. Для Historical Battle (`gMap.bbattle`) игрок всегда
помечается живым. Иначе берётся `farmused` (занятые слоты пехоты), и:

- если `0 < farmused < 100` — движок вручную ищет хотя бы один объект с
  usage `gc_obj_usage_center` (Городской центр) или крестьянина с
  флагами «настоящая боевая единица» (`bvisual_none + bessential_none`).
  Если крестьян нет, но Городской центр есть — игрок ещё **не**
  проигрывает.
- иначе `bexists := (farmused > 0)`.

Если `bexists` упал в `False` и игрок был жив на предыдущем тике, ему
ставится `gc_player_victorystate_lose`, физически убиваются все его
юниты через `_misc_KillPlayerUnits`, рассылается результат [^18].

Итог: **defeat = `farmused == 0`**, то есть у игрока нет ни одного
крестьянина и ни одного центра/населённой постройки, при двух нюансах:

- «Частичный» случай — `0 < farmused < 100` — выше.
- В Historical Battle (`bbattle`) этот код не работает — там defeat
  ставится только сценарным триггером или surrender'ом.

`farmused` инкрементируется при появлении любого playable-юнита (в том
числе крестьянина) и декрементируется при смерти/удалении [^19].

## 5. Score formula

### 5.1 Per-object base score

Каждый `TObjProp` имеет поле `score : Integer` [^20]. Задаётся через
помощники:

- `SetObjBuildingExtProperties(..., score, usage, ...)` [^21] — для
  зданий. Городской центр (`cen`) получает `score = 1000` [^22].
- `SetObjBaseSearchBuildVisionScore(..., score)` [^23] — для юнитов.
  Крестьянин получает `score = 10` [^24].

Полная таблица score per-sid требует распарсить все вызовы
`SetObjBuildingExtProperties` и `SetObjBaseSearchBuildVisionScore`. Поиск
по `.score :=` в `unit.script` показывает только две прямые присвоения,
обе через эти helper-процедуры, так что аккуратное парсение call-сайтов
даст значения для всех юнитов и зданий.

### 5.2 Накопление при убийстве

При смерти **врага** — попадании снаряда в юнита — счёт
`gPlayer[plInd].counter.scores` растёт на `score жертвы × 2`, плюс ещё
`× 3` за каждого юнита внутри здания (гарнизон) [^25].

То есть **kill = +2× score жертвы**, **kill garrisoned unit = +3×
score**.

При появлении нового объекта у игрока счёт растёт с модификатором: `+5×`
при захвате, `+1×` при производстве [^26].

При потере объекта счёт уменьшается с модификатором: `−5×` если был
захвачен, `−3×` если это сбежавший наёмник в восстании
(`brebellion and bmercenary`), иначе `−2×` [^27]. Score не уходит в
минус — clamp на нуле там же.

### 5.3 Live-сэмпл / временной ряд

Каждые `gc_progress_TimeProgressStatistics` секунд (раз в 5 секунд
игрового времени) пишется снимок `farmused` и `counter.scores` в
`gPlayer[i].stat.population` и `gPlayer[i].stat.scores` [^28]. Это даёт
хронограмму очков и населения для финального экрана статистики.

### 5.4 Использование в исходе партии

- `_misc_CheckEndGame` **score не использует** — победа определяется
  только по командам.
- `_misc_LanCloseSessionSetScores` использует **±1/±2** (rated/нет) для
  отправки на лидерборд [^29]. То есть в multiplayer-rated рейтинг ELO
  движется на единицу, а не на разницу score.

## 6. Resignation / Surrender

Хоткей в UI вызывает `_misc_Surrender(blanterminate)` [^2]. Функция
ставит `gMap.players[plInd].bleave := True`, и дальше развилка по
сетевой роли:

- **Server** — присваивает `gPlayer[plind].victorystate :=
  gc_player_victorystate_lose`, вызывает `_misc_CheckEndGame`; если
  партия не закончилась — рассылает `gc_LAN_GAME_SERVER_LEAVE`.
- **Client** — отправляет пакет `gc_LAN_GAME_SURRENDER` (=10) серверу.
- **Offline** — присваивает `lose` локально и сразу зовёт
  `_misc_CheckEndGame`.

Чат-команды `/resign` нет — grep по `resign` в скриптах даёт 0 матчей.
Функция вызывается только из ENG (бинарного движка), судя по всему — это
кнопка «Сдаться» в game-меню. Константы протокола `gc_LAN_GAME_SURRENDER
= 10` и `gc_LAN_GAME_SURRENDER_CONFIRM = 11` [^30].

«First leaver» — первый сдавшийся в первые 15 минут — теряет **−w ELO**
даже если его команда выиграет [^31]. А напарнику ливера в команде из
двух наоборот ELO **не списывают**, чтобы не наказывать «жертву»
дезертирства.

## 7. Time / turn limits

- **Game time-limit: отсутствует.** Никакой `gametimelimit` в скриптах
  нет.
- **Pause-time-limit:** `gc_pause_timelimit = 120` сек,
  `gc_pause_countlimit = 4` [^16] — паузу можно ставить максимум 4 раза
  по 120 секунд, дальше движок отказывается.
- **Score-history grace:** в rated-комнатах счётчик результата
  отправляется только если `gMap.brating OR gt > 60*10` [^32] — то
  есть в нерейтинговых играх длительностью менее 10 минут итог в
  публичный лог не идёт (анти-фермерство ачивок).
- **Peacetime:** `gc_mapsettings_peacetime_*` [^33] —
  0 / 10 / 15 / 20 / 30 / 45 / 60 / 90 / 120 / 180 / 240 минут. Это
  запрет атаки в первые N минут, а не таймер конца игры. Полная таблица —
  [`reports/map/lobby_settings.md`](../../reports/map/lobby_settings.md#peacetime--время-мира);
  механика — [`game_settings.md`](../world/map/game_settings.md#peacetime--как-устроен-мир).

## 8. Multiplayer-specific отличия

- `_misc_LanServerSendResults` рассылает win/lose всем клиентам пакетом
  `gc_LAN_GAME_SESSION_RESULTS` [^34].
- `_misc_LanCloseSessionSetScores` обновляет публичный рейтинг (только
  при `_net_IsServer`), `LanPublicServerCloseSession` закрывает сессию.
- В rated-комнатах (`gMap.brating`) ELO-вес = 1, в casual-комнатах
  вес = 2 [^35]. На первый взгляд парадокс, но это про **штраф** ливеру:
  за casual-ливерство наказание сильнее, видимо, чтобы поощрять
  ranked-режим.
- В casual-играх длительностью менее 10 минут `LanSrvSetClientScore` не
  вызывается (см. §7).
- Для 2v2 предусмотрена попарная логика «не штрафуй напарника ливера»
  [^31] — команды по умолчанию `{0,1}` против `{2,3}`.

## 9. Сводка

| Тема | Значение |
|---|---|
| **Default victory** | last-team-standing (`_misc_CheckEndGame`). |
| **Default defeat** | `farmused = 0` AND нет крестьянина / Городского центра в собственности. В Historical Battle отключено. |
| **Wonder** | **отсутствует** (нет такого режима/здания в C3, в отличие от AoE2). |
| **Score** | копится для статистики и ачивок, **не определяет исход**. Формула: kill = +2× score, kill garrisoned = +3× score, capture = +5× score, build = +1× score; loss = −2×, captured-from = −5×, rebel-merc = −3×; clamp на нуле. |
| **Time-limit** | отсутствует (есть только peacetime, pause-limit). |
| **Surrender** | `_misc_Surrender` ставит `bleave = True`, `victorystate = lose`, триггерит `_misc_CheckEndGame`. Первый ливер в первые 15 минут получает −w ELO. |
| **Scenario triggers** | `endgame_win = 47`, `endgame_lose = 48`, применяются только к `myplind` (per-client). |
| **Game modes** | `mainmenu` / `game` / `editor` / `spectator` / `replay` / `endgamestatistics`. Поверх — Random map, Historical Battle (`gMap.bbattle`), Campaign, Custom Scenario, Rated MP (`gMap.brating`). |

## 10. Открытые вопросы

| # | Вопрос | Где копать |
|---:|---|---|
| 1 | Полная таблица per-sid score: нужно распарсить все примерно 3000 вызовов `SetObjBuildingExtProperties` / `SetObjBaseSearchBuildVisionScore`. Сейчас известно: крестьянин = 10, Городской центр = 1000. | Парсер call-сайтов в `unit.script`. |
| 2 | Bridge между бинарным движком и `_misc_Surrender` — где именно вызывается, как называется GUI-кнопка? Предполагается, что это кнопка «Surrender» в game-меню без отдельного хоткея. | GUI-callback'и в native binary. |
| 3 | `lastattacktime`-music ↔ defeat: когда атакован, интервал `gc_gui_battlemusicinterval - gc_gui_underattackalarminterval` — для тулзы «alert». | Прямой расчёт по константам. |
| 4 | Gamestage transition `started → finished` — кто его триггерит? `_misc_CheckEndGame` не пишет gamestage; видимо, это бинарный движок после `gc_gamemode_endgamestatistics`. | Профилирование сетевого протокола в конце партии. |
| 5 | «1 человек на команде» победа? Если в стартовой расстановке 1v1 без союзников и враг капитулирует на 5-й секунде — `_misc_CheckEndGame` всё ещё работает (одна команда из выживших). Если же изначально стояла «sandbox» (1 player), функция ранний `exit` через `not bSecondTeamExist` — проверить эмпирически. | Эмпирически в редакторе. |
| 6 | Что точно делает «Score» в финальном экране — отображается ли как формула или как сэмплированный таймсериес из `stat.scores`? | UI extension не извлекался. |

---

## Источники

Все ссылки относительно `data/scripts/` в установке Cossacks 3.

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

[^3]: Состояния `gc_player_victorystate_*` — `dmscript.global:777-779`:

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

[^6]: Флаг `gMap.bbattle : Boolean` — `lib/classes.script:121`, `lib/miscext2.script:2645`.

[^7]: Отключение defeat-проверки в Historical Battle — `units/global.inc/progress.inc:65-67`:

    ```pascal
    if (gMap.bbattle) then gPlayer[plind].bexists := True;
    ```

[^8]: Каталог кампаний — `dmscript.global:1359, 1513-1522` (`gc_ach_campaign_finalaus..finalrus`, `data/game/var/campaigns.cfg`).

[^9]: Запись прогресса кампании — `lib/scenario.script:3007-3062` (`TCampaignProgress.finished`, `lose`, `maxfinishdifficulty`).

[^10]: Главный цикл `_misc_CheckEndGame` — `lib/miscext2.script:3768-3845`:

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

[^11]: Перекрытие ранее проставленного `lose` командной победой — `lib/miscext2.script:3822-3827`.

[^12]: Триггер-action'ы конца партии — `lib/classes.script:6334-6335`:

    ```pascal
    gc_trigger_action_endgame_win  = 47;
    gc_trigger_action_endgame_lose = 48;
    ```

[^13]: Реализация `endgame_win`/`endgame_lose` для `myplind` — `lib/scenario.script:2995-3065`.

[^14]: Список доступных триггер-условий — `lib/classes.script:6251-6283`.

[^15]: Действия `playerSetAsAlly`/`Enemy`/`Neutral` — `lib/classes.script:6305-6307`.

[^16]: Лимиты паузы — `dmscript.global:1662-1663`:

    ```pascal
    gc_pause_timelimit  = 120;
    gc_pause_countlimit = 4;
    ```

[^17]: Sub-tick проверка `bexists` — `units/global.inc/progress.inc:54-140`:

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

[^18]: Defeat-ветка в progress-tick — `units/global.inc/progress.inc:124-134`:

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

[^19]: Инкремент/декремент `farmused` — `lib/unit.script:3905`.

[^20]: Поле `score : Integer` в `TObjProp` — `lib/classes.script:3617`.

[^21]: Helper для зданий — `lib/unit.script:503` (`SetObjBuildingExtProperties(..., score, usage, ...)`).

[^22]: Score Городского центра — `lib/unit.script:2371`:

    ```pascal
    SetObjBuildingExtProperties(objprop, objbase, 4000, 500, 300, True, 1000, gc_obj_usage_center, 0, 700, 700, 0, 0, 0)
    ```

[^23]: Helper для юнитов — `lib/unit.script:571` (`SetObjBaseSearchBuildVisionScore(..., score)`).

[^24]: Score крестьянина — `lib/unit.script:636`:

    ```pascal
    SetObjBaseSearchBuildVisionScore(objprop, objbase, 700, 144, 1, 10)
    ```

[^25]: Накопление при убийстве — `lib/miscext2.script:443-461`:

    ```pascal
    TObj(pobj2).hp <= 0:
       gPlayer[plInd].counter.scores += TObjProp(pobjprop2).score * 2;
       // плюс за всех юнитов внутри здания (гарнизон)
       gPlayer[plInd].counter.scores += gObjProp[..].score * 3;
    ```

[^26]: Накопление при появлении объекта — `lib/unit.script:3836-3841`:

    ```pascal
    var scoremodifier : Integer = bcaptured ? 5 : 1;
    gPlayer[pl].counter.scores += TObjProp(pobjprop).score * scoremodifier;
    ```

[^27]: Списание при потере объекта — `lib/unit.script:3939-3950`:

    ```pascal
    scoremodifier := bcaptured ? 5 : (brebellion and bmercenary ? 3 : 2);
    gPlayer[pl].counter.scores -= TObjProp(pobjprop).score * scoremodifier;
    if (gPlayer[pl].counter.scores<0) then gPlayer[pl].counter.scores := 0;
    ```

[^28]: Снимок population/scores — `progress/progress.inc/nothing.inc:716-742`:

    ```pascal
    gPlayer[i].stat.population.Add(popul);   // farmused
    gPlayer[i].stat.scores.Add(score);       // counter.scores
    ```

[^29]: Запись на лидерборд — `lib/miscext2.script:3704-3766` (`_misc_LanCloseSessionSetScores`).

[^30]: Пакеты протокола сдачи — `lib/classes.script:7569-7570` (`gc_LAN_GAME_SURRENDER = 10`, `gc_LAN_GAME_SURRENDER_CONFIRM = 11`).

[^31]: Штраф первому ливеру и логика 2v2 — `lib/miscext2.script:3730-3757`:

    ```pascal
    if (firstleaverind=i) then LanSrvSetClientScore(... -w)   // штраф ливеру
    case i of
       0: if firstleaverind<>1 ...
       1: if firstleaverind<>0 ...
       2: if firstleaverind<>3 ...
       3: if firstleaverind<>2 ...
    ```

[^32]: Grace-период публикации результата — `lib/miscext2.script:3712`:

    ```pascal
    if (gMap.brating) or (gt > 60*10) then ...
    ```

[^33]: Константы peacetime — `dmscript.global:1055-1066` (`gc_mapsettings_peacetime_*`, 11 значений: 0..240 минут).

[^34]: Рассылка результата — `lib/miscext2.script:3658-3686` (`_misc_LanServerSendResults`, пакет `gc_LAN_GAME_SESSION_RESULTS`).

[^35]: ELO-вес rated/casual — `lib/miscext2.script:3722-3725`.
