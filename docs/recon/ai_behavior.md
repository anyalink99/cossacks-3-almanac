# Поведение ИИ в Cossacks 3

Реверс-инжиниринг по `C:\Program Files (x86)\Steam\steamapps\common\Cossacks 3\data\scripts\`.

## Исходные файлы

| Путь | Размер | Роль |
|---|---:|---|
| `lib/ai.script` | 95.6 KB | Вспомогательная библиотека: запросы по армии (`_ai_GetArmyForce`, `_ai_GetArmyUnitsCount`), мэппинг ролей юнитов (`_ai_FillUnitUpgradeList`), таблицы апгрейдов, заполнение списка месторождений, `_ai_IsTeamAI`, `_ai_GetCommonNationName` (4 кластера: rus / tur / mis / eur). |
| `units/global.inc/progressai.inc` | 0.8 KB | **Диспетчер.** Каждый `gc_global_TimeProgressAI`-тик вызывает `ProgressEconomicAI`, затем `ProgressWarAI`. |
| `units/global.inc/progresseconomicai.inc` | 226 KB | Экономический ИИ: build order, цели по производству, баланс ресурсов, выбор апгрейдов. |
| `units/global.inc/progresswarai.inc` | 223 KB | Военный ИИ: формирование армий, решения об атаке/отходе, диверсионные группы, транспортные операции. |
| `misc/airegion.aix` | 3.0 KB | Триггеры зон ИИ для сценариев. К основному ИИ отношения не имеет. |

Интервал тиков: `gc_global_TimeProgressAI = 0.03 × 16 × 5 = 2.4` игровых секунд (`dmscript.global:1486`). Каждый ИИ-игрок прогоняет полный цикл раз в 2.4 g-сек. `lastprogressaitime` смещён по player-id (`player.script:140`: `id × 0.25 + gc_global_TimeProgressAI`), чтобы все ИИ не запускались в один тик.

Диспетчер (`progressai.inc`):

```
ExecuteState('ProgressEconomicAI');
ExecuteState('ProgressWarAI');
```

## Уровни сложности

`dmscript.global:781-786`:

```
gc_player_difficulty_none       = -1;
gc_player_difficulty_easy       =  0;
gc_player_difficulty_normal     =  1;
gc_player_difficulty_hard       =  2;
gc_player_difficulty_veryhard   =  3;
gc_player_difficulty_impossible =  4;
```

`gc_MaxAIDifficultyCount = 4` (`:235`) — UI показывает четыре уровня (easy / normal / hard / veryhard); `impossible` зарезервирован для сценариев (`initmaphistoricalbattle.inc:121` ставит исторические битвы на этот уровень).

Сложность хранится в `gMap.players[i].aidifficulty` (`classes.script:105`), копируется в `gPlayer[i].difficulty` при старте партии (`initmapgen.inc:132`). Дефолт в лобби — `easy` (`map.script:244`, `player.script:118`).

### Что меняется между уровнями

#### 1. Скорость постройки и найма — главный «чит»

`building.inc/doprogressorders.inc:222-230`:

```
if (gPlayer[plind].bai) and (not gPlayer[plInd].aiData.bhumanai) then
case gPlayer[plind].difficulty of
   gc_player_difficulty_easy       : deltabuildtime *= 0.30; // easy
   gc_player_difficulty_normal     : deltabuildtime *= 0.50; // normal
   gc_player_difficulty_hard       : deltabuildtime *= 0.75; // hard
   gc_player_difficulty_veryhard   : deltabuildtime *= 1.00; // very hard
   gc_player_difficulty_impossible : deltabuildtime *= 1.25; // impossible
end;
```

`deltabuildtime` — это прибавка за тик к прогрессу постройки/найма. Эффект:

- **easy** — ИИ строит на **30 %** скорости игрока (в 3.33 раза медленнее);
- **normal** — 50 % (в 2 раза медленнее);
- **hard** — 75 %;
- **veryhard** — паритет с игроком;
- **impossible** — 125 % (на 25 % быстрее) — единственный режим, где ИИ получает реальное преимущество.

Флаг `aiData.bhumanai` (по умолчанию `False`, `classes.script:2688`) отключает множитель — ИИ играет на паритете независимо от уровня.

#### 2. Лимит апгрейдов башни

`progresseconomicai.inc:3653-3658`. Максимальный уровень апгрейда башни: easy = 2, normal = 3, hard = 4, veryhard = 5, impossible = 5.

#### 3. Размер диверсионных групп

`progresseconomicai.inc:2322-2326`:

```
case difficulty of
   gc_player_difficulty_normal     : numdiver := 0;
   gc_player_difficulty_hard       : numdiver := 2;
   gc_player_difficulty_veryhard   : numdiver := 4;
   gc_player_difficulty_impossible : numdiver := 4;
end;
```

Easy не отправляет диверсий вообще. Veryhard / impossible держат до 4 параллельных диверсионных армий (cap `gc_ai_MaxDiverArmies = 2` плюс существующие).

#### 4. Лимит апгрейдов шахты

`progresseconomicai.inc:2202-2212` и `~2396-2410`. Easy ограничен уровнем 0, normal — 2/3, выше — до 7.

#### 5. Базовые ворота через `if difficulty > easy`

Easy не исследует: `bricks1`, `fort`, `armor1`, `accurency1`, `artlife`, `horseswords`. Не строит гаубиц и мортир (`progresseconomicai.inc:2349-2353`).

#### 6. Дополнительные проверки на hard+

`progresseconomicai.inc:2306` — только `difficulty >= hard` запускает логику аварийного найма дипломат-драгунов (наёмников) при нехватке золота.

#### 7. `bricks1` — только veryhard и impossible

`progresseconomicai.inc:2452`.

#### 8. Поблажка игроку на низких уровнях

`unit.script:7367` — стрелки игрока на сложности `<= normal` имеют ослабленную проверку `standtime`, что делает их менее назойливыми в управлении. Это бонус **игроку**, а не ИИ.

### Что НЕ меняется по сложности

- **Стартовые ресурсы.** `initmapgen.inc:167-189` ставит всем игрокам одинаковые значения по `resourcestart`: 0 → 1000 каждого, 1 → 4000, 2 → 5000, 3 → 1 000 000. ИИ не получает бонусных ресурсов ни на одном уровне.
- **Постоянный «капельный» доход / читы по доходу.** В скриптах не найдено. ИИ добывает ресурсы стандартными шахтами, а вызовы `_ai_SetResouceBalance` управляют только приоритетами производства/торговли, но не дают бесплатных ресурсов.
- **Скорость игры.** `gc_settings_gamespeed_*` — глобальная, не персональная.

## Build order (порядок постройки)

Эко-ИИ — **адаптивный, но правило-ориентированный**. Решения о постройке не записаны как фиксированный массив — это длинная последовательность вызовов `_ai_TryUnit(plind, cid, gc_ai_unit_<X>, target_count, false)`, в которой условие обычно ссылается на текущий счётчик других зданий (например, `_ai_GetUnitCount(plind, cid, gc_ai_unit_ba17) >= 2`).

Макро-фазы (`progresseconomicai.inc:2700-2830`):

1. Всегда пытается: **Городской центр** (1 → 2 в начале), **рынок**, **мельница**.
2. Только Алжир / Турция: оппортунистический **дом**, если есть кузница + склад + рынок + бараки 17в.
3. **Шахты** (`gc_ai_unit_minegold/_mineiron/_minecoal`) — через `_ai_BuildMines` (использует `gc_ai_dist_mines_lvl1=30`, `lvl2=60`, `expansion=85` из `dmscript.global:503-506`).
4. **Кузница** (1 шт.).
5. **Казарма 17в. (ba17)**: цель 1 → 2 → 3 → 6 / 8 в зависимости от количества Городских центров и флага водной карты (например, `:2771`: `_ai_TryUnit(plind, cid, gc_ai_unit_ba17, 8, False)` если не Россия, иначе 6).
6. Расширение **до 5 Городских центров**, если `centercount >= 2`.
7. **Академия** при `>= 2` ba17 и `>= 2` Городских центрах.
8. **Конюшня / артиллерийский склад / дипломатический центр / храм** после академии.
9. **Казарма 18в. (ba18)** появляются после исследования академии и `gc_ai_upg_century`.
10. **Башни** при наличии академии и активной war-AI на `difficulty > easy` (`:2926-2929`): `numTowers = Min(3, peasants div 75)`.

Build order сильно зависит от нации. Каждый `cid_<nat>` (24 нации: aus..lit) имеет собственную ветку во многих местах. Три заметных подхода: Украина (`cid_ukr`) часто пропускает ba17 / officer-цепочку и делает ставку на массовый musk17; Алжир / Турция (`cid_alg`/`cid_tur`) ведут параллельную ветку «лучники из академии»; Россия (`cid_rus`) занижает count бараков до 6 в режиме «миллионы» ресурсов.

Контрольные точки build order (репрезентативные):

- 2 ba17 + 2 Городских центров → академия (`:2796`);
- 2 ba17 + 4 Городских центров → баланс ресурсов смещается в сторону золота (`:2036-2039`);
- ba18 ≥ 5 → запуск ещё 3 ba17 и шестого Городского центра (`:2789-2793`);
- pikemanCount ≥ 36×4 → переключение с пикинёров на pikeman + musk (`:2134`);
- pikemanCount ≥ 36×7 + `gc_ai_max_guards (120)` → только musk17 (`:2152-2158`).

Баланс ресурсов адаптируется к числу крестьян (`progresseconomicai.inc:1999-2031`): доля еды растёт 12 → 21 → 27 → 36 → 45 (× 1.3 если пикинёры ещё не апгрейжены) на breakpoint'ах 30 / 45 / 85 / 120 крестьян. Россия и Польша используют 16 → 24 → 31 → 40 → 49.

## Цели по производству

В `_ai_RequestUnitsProduction` (`progresseconomicai.inc:2085+`):

### Крестьяне

```
var numpeasants : Integer = _ai_GetUnitCount(plind, cid, gc_ai_unit_center) * 2;
if (peasants_total < 400) or (peasants_this_nation < 30) then
   if food < 700 then queue numpeasants
   else queue 1
```

Жёсткий cap: **400 крестьян суммарно** (по всем подконтрольным нациям) ИЛИ **30 на одну нацию**, что выполнится раньше (`:2088`). Формула «2 на Городской центр» — это скорость пополнения. `_ai_DecreasePeasants` (`:3856`) снижает count при превышении.

### Военные цели (`:2103-2150` и далее)

- `numOfficers = pikemanCount div 36` (минимум 1 если pikemanCount > 28);
- `numReiters = stable_count × 2`;
- `numInf18 = ba18_count × 2`;
- `bar_count` (цель производства inf17) = `ba17_count × 2`;
- `cannon_count = ClampInt(num_depo × 6, 6, 30)` (`:2347`);
- `howitzer_count = ClampInt(num_depo × 2, 2, 8)` (`:2351`);
- `mortar_count = ClampInt(num_depo × 8, 8, 40)` (`:2352`);
- 18-вечный драгун / пикинёр: зависит от апгрейда `gc_ai_upg_horse` и нации;
- Лучники (alg / sco): `_ai_GetUnitCount < farmused/3` (на водной карте `/5`).

Эти числа — **count'ы для очереди производства**, переданные `_ai_TryUnit`, а не жёсткие лимиты. Казармы тренируют до достижения цели и снова просыпаются на следующем ИИ-тике.

`gc_ai_max_guards = 120` (`dmscript.global:500`) — буфер над пикинёрским порогом, после которого включается «только musk17».

## Триггеры агрессии и атаки

Константы (`dmscript.global:474-481`):

```
gc_ai_AgressorsCount     = 5    // отрядов в первой агрессорской волне
gc_ai_MaxDiverArmies     = 2    // максимум диверсионных армий одновременно
gc_ai_OfficerWaitTime    = 20   // сек (на normal speed) ожидания барабанщика/офицера
gc_ai_GreArmyBattleDist  = 2    // grenadier scan grid distance
gc_ai_ArmyBattleDist     = 4    // обычный scan grid distance
gc_ai_BitvaInterval      = 8    // интервал перепроверки в бою
gc_ai_CityDangerDist     = 20
gc_ai_MergeArmyCityDist  = 25
gc_ai_MergeApproachDist  = 10
gc_ai_MinStoreHouseDist  = 9
```

Pipeline атаки:

- `progresswarai.inc` собирает армии и раздаёт ордера. Перечисление ордеров (`gc_ai_armyorder_*`, `dmscript.global:430-438`): `none / makebattle / bitva / buildmine / sabotage / agressor / makewaterbattle / transport / attackwall`.
- **Первая агрессорская волна** (`progresswarai.inc:3560-3568`, `_ai_SendAgressors`):

  ```
  if (not gbool_peacemode) and (agressorsSent = 0) and
     (agressors.GetCount >= gc_ai_AgressorsCount=5) then
     pArmy := _ai_CreateAgressorArmy(plInd, 5, agressors);
     _ai_ArmyMakeAgressorBattle(pArmy);
  ```

  ИИ отправляет одну стартовую волну из 5 squads, как только в пуле наберётся достаточно подвижных юнитов. Последующие волны — через `_ai_ArmyMakeBattleLink`.

- **Отступление** (`:2398-2407`): `myForce = _ai_GetArmyForce(pArmy)`. Если `uCount > 200` или `myForce > 3800`, `myForce := 100000` (трактуется как абсолютное превосходство, отступление не запускается). Иначе умножается на 8 (heavy bonus) или 2 (light). При `enForce > myForce` — отступаем.
- **Диверсия** (`_ai_ArmyDiversia*`): если враг слабее моей армии в радиусе 30 — атакуем; в радиусе 400 — тоже идём в атаку.
- **Атака стен** (`_ai_ArmyCheckWallAttack`): если цель — стена, все squads в `searchRadius` армии переключаются на attack-wall (артиллерия исключена).
- **Peacetime** (`gbool_peacemode`): ставится при `gMap.settings.additional.peacetime <> default` (`dogenerate.inc:2060-2064`). Пока активен, все агрессорские и диверсионные ветки делают early-exit (`:2787`, `:3562`).
- **Дипломатия и команды:** `gPlayer[i].team`. ИИ считает игрока врагом, если `team` отличается или равен 0 (`initmapgen.inc:160`). `_ai_IsTeamAI` (`ai.script:527`) определяет, ИИ ли в команде. Альянсы в run-time не формируются — команды задаются в лобби и не меняются. Сценарный триггер `gc_trigger_action_player_playerSetAsAlly = 19` существует, но ИИ из random-карт его не использует.

## Читы

| Уровень | Чит применён? | Величина |
|---|---|---|
| Easy | Да — гандикап (замедляет ИИ) | Постройка/найм на 30 % скорости |
| Normal | Да — гандикап | На 50 % |
| Hard | Да — слабый гандикап | На 75 % |
| Very hard | Нет | Паритет (100 %) |
| Impossible | Да — единственный «честный» чит | На 125 % (быстрее игрока) |

Источник: `building.inc/doprogressorders.inc:222-230`. Условие срабатывания: `gPlayer[plind].bai and not aiData.bhumanai`. Флаг `bhumanai` (`classes.script:2611`) по умолчанию `False`; если его выставить, ИИ играет на паритете независимо от уровня.

**Стартовых ресурсов ИИ не получает** — у человека и ИИ одинаковая выдача из `resourcestart` (1000 / 4000 / 5000 / 1 000 000). Подтверждено в `initmapgen.inc:166-189`.

**Доход / обзор / скорость движения** — читов не найдено. ИИ не видит ресурсы под туманом сверх того, что обнаружили его собственные юниты (`_ai_FillOreList` использует `GetGameObjectVisibleByHandle`, `:228`).

## Дипломатия

- Команды задаются в лобби (`gMap.players[i].team`). Инициализация (`initmapgen.inc:158-163`):

  ```
  if (myteam <> histeam) or (histeam = 0) or (myteam = 0) then
     AddPlayerEnemyPlayerByHandle(...)
  else
     AddPlayerFriendPlayerByHandle(...)
  ```

  Команда `0` означает «без команды» — все враги.

- ИИ против ИИ: `_ai_IsEnemiesExists` (`ai.script:7-19`) проходит по всем игрокам, считает врагом любого с другой командой. ИИ-игроки в одной команде дружат и не атакуют друг друга.
- **Динамической дипломатии нет.** Ни логики формирования альянсов, ни их разрыва не найдено в `lib/ai.script`, `progresseconomicai.inc`, `progresswarai.inc`. Сценарии могут менять отношения (`scenario.script` + `gc_trigger_action_player_playerSetAsAlly`), но в random-карте такого механизма не существует.
- ИИ относится ко всем врагам **симметрично** — `_ai_GetRandomEnemy` (`progresseconomicai.inc:67-94`) выбирает случайного врага для следующего удара. Нет приоритизации слабого, нет постоянной «вендетты».

## Открытые вопросы

1. **Скорость пополнения agressor-пула.** Список `gPlayer[plInd].aiData.agressors` где-то наполняется. Чтобы предсказать тайминг первой атаки на свежей карте, нужно отследить вызовы `aiData.agressors.Add`.
2. **Активация `bhumanai`.** Флаг есть в коде, но в скриптах сеттер не найден. Возможно, выставляется со стороны C++-движка — например, через UI-чекбокс «Fair AI» в опциях или через турнирный режим. Стоит проверить `gui/options/`.
3. **`fAttackCount` per squad.** У TSquad есть поля `fAttackCount`, `fMoveCount`, `fDelayCount` (TArmy их запрашивает). Где они выставляются? Скорее всего, в обработчиках `unit.inc/onattack*.inc`.
4. **Что именно значит `gc_ai_max_guards = 120`.** Используется как буфер над пикинёрским порогом, но смысловая роль (количество защитников у базы?) непонятна.
5. **Логика `centerfound`.** ИИ не запускает полноценный bootstrap, пока `aidata.centerfound = True` (`ai.script:451`). Когда флаг переключается? Скорее всего, при первой постройке Городского центра.
6. **Скорость принятия решений в war-AI.** `ProgressWarAI` тикает раз в 2.4 g-сек на игрока, но у каждой армии собственные `fStateTime`-кулдауны. Чтобы знать задержку конкретного действия, нужно пройти `progresswarai.inc:4100-4220`.
7. **Влияние сложности на частоту атак.** Триггеры agressor / sabotage используют `gc_ai_AgressorsCount = 5` независимо от уровня (масштабируется только число параллельных диверсий). То есть easy и impossible ИИ должны отправлять первую атаку в одно и то же время — отличается только скорость постройки. Стоит проверить эмпирически.
8. **`gc_ai_AgressorsCount = 5` против `gc_ai_max_guards = 120`.** Очень маленькая первая волна для армии в 100 пикинёров — всего 5 squads, остальные стоят дома. Нужно проверить, масштабируются ли последующие волны.
9. **Дальности `gc_ai_dist_mines_lvl1 = 30 / lvl2 = 60 / expansion = 85`.** Это в тайлах. Стоит верифицировать, какой уровень ИИ использует на Tiny против Normal-карты.
10. **`bprogressWar` / `bprogressUpgrades`** в `aidata` — когда переключаются в `True`? Скорее всего, по таймеру, но трассировки пока нет.
