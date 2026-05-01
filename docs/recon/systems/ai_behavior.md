# Recon: поведение ИИ

Реверс-инжиниринг по `data/scripts/` в установке Cossacks 3. Все ссылки
на код и сами Pascal-блоки собраны в разделе [Источники](#источники)
в конце документа.

## TL;DR

- ИИ-игрок тикает раз в **2.4 игровых секунды**. Каждый цикл — две фазы:
  `progresseconomicai` (build order, добыча, апгрейды) и `progresswarai`
  (армия, атака, диверсии).
- **«Сложность» — это множитель скорости постройки и найма**, ничего
  больше: easy 30 % / normal 50 % / hard 75 % / very hard 100 % /
  impossible 125 %. Стартовых ресурсов ИИ **не получает** ни на какой
  сложности.
- **Build order rule-based** и нация-зависимый. Нет ML, нет рандома —
  просто if-каскад от текущего состояния (есть казарма → строй второй
  склад; есть aca → исследуй cen.1 → ставь ba2; и так далее).
- **`aggressor` wave** = 5 отрядов. Когда они собраны, ИИ отправляет их
  на ближайшую цель.
- **Дипломатия** статическая: команды берутся из лобби, в процессе
  партии ИИ союзов не заключает и не разрывает.

## Исходные файлы

| Путь | Размер | Роль |
|---|---:|---|
| `lib/ai.script` | 95.6 KB | Вспомогательная библиотека: запросы по армии (`_ai_GetArmyForce`, `_ai_GetArmyUnitsCount`), мэппинг ролей юнитов (`_ai_FillUnitUpgradeList`), таблицы апгрейдов, заполнение списка месторождений, `_ai_IsTeamAI`, `_ai_GetCommonNationName` (4 кластера: rus / tur / mis / eur). |
| `units/global.inc/progressai.inc` | 0.8 KB | **Диспетчер.** Каждый `gc_global_TimeProgressAI`-тик вызывает `ProgressEconomicAI`, затем `ProgressWarAI`. |
| `units/global.inc/progresseconomicai.inc` | 226 KB | Экономический ИИ: build order, цели по производству, баланс ресурсов, выбор апгрейдов. |
| `units/global.inc/progresswarai.inc` | 223 KB | Военный ИИ: формирование армий, решения об атаке/отходе, диверсионные группы, транспортные операции. |
| `misc/airegion.aix` | 3.0 KB | Триггеры зон ИИ для сценариев. К основному ИИ отношения не имеет. |

Интервал тиков: `gc_global_TimeProgressAI = 0.03 × 16 × 5 = 2.4` игровых
секунд [^1]. Каждый ИИ-игрок прогоняет полный цикл раз в 2.4 g-сек.
`lastprogressaitime` смещён по player-id (`id × 0.25 +
gc_global_TimeProgressAI`), чтобы все ИИ не запускались в один тик [^2].

Диспетчер просто последовательно дергает экономическую и военную
фазы [^3].

## Уровни сложности

В коде определены пять уровней — от `easy` до `impossible` — плюс
служебное значение `none = -1` [^4]. `gc_MaxAIDifficultyCount = 4` [^5];
UI показывает четыре уровня (easy / normal / hard / veryhard);
`impossible` зарезервирован для сценариев — например,
`initmaphistoricalbattle.inc` ставит исторические битвы на этот
уровень [^6].

Сложность хранится в `gMap.players[i].aidifficulty` [^7], копируется
в `gPlayer[i].difficulty` при старте партии [^8]. Значение по умолчанию
в лобби — `easy` [^9]. Полная таблица из 5 уровней с множителями —
[`reports/map/lobby_settings.md`](../../reports/map/lobby_settings.md#difficulty--сложность);
поведение движка — [`game_settings.md`](../world/map/game_settings.md) §4.

### Что меняется между уровнями

#### 1. Скорость постройки и найма — главный «чит»

`deltabuildtime` — это прибавка за тик к прогрессу постройки и найма;
для ИИ она домножается на коэффициент сложности [^10]. Эффект:

- **easy** — ИИ строит на **30 %** скорости игрока (в 3.33 раза медленнее);
- **normal** — 50 % (в 2 раза медленнее);
- **hard** — 75 %;
- **veryhard** — паритет с игроком;
- **impossible** — 125 % (на 25 % быстрее) — единственный режим, где ИИ получает реальное преимущество.

Флаг `aiData.bhumanai` (по умолчанию `False` [^11]) отключает
множитель — ИИ играет на паритете независимо от уровня.

#### 2. Лимит апгрейдов башни

Максимальный уровень апгрейда башни: easy = 2, normal = 3, hard = 4,
veryhard = 5, impossible = 5 [^12].

#### 3. Размер диверсионных групп

`numdiver` зависит от уровня: normal = 0, hard = 2, veryhard = 4,
impossible = 4 [^13]. Easy не отправляет диверсий вообще. Veryhard и
impossible держат до четырёх параллельных диверсионных армий
(`cap = gc_ai_MaxDiverArmies = 2` плюс существующие).

#### 4. Лимит апгрейдов шахты

Easy ограничен уровнем 0, normal — 2/3, выше — до 7 [^14].

#### 5. Базовые ворота через `if difficulty > easy`

Easy не исследует: `bricks1`, `fort`, `armor1`, `accurency1`, `artlife`,
`horseswords`. Не строит гаубиц и мортир [^15].

#### 6. Дополнительные проверки на hard+

Только `difficulty >= hard` запускает логику аварийного найма
дипломат-драгунов (наёмников) при нехватке золота [^16].

#### 7. `bricks1` — только veryhard и impossible

См. [^17].

#### 8. Поблажка игроку на низких уровнях

Стрелки игрока на сложности `<= normal` имеют ослабленную проверку
`standtime`, что делает их менее назойливыми в управлении [^18]. Это
бонус **игроку**, а не ИИ.

### Что НЕ меняется по сложности

- **Стартовые ресурсы.** Все игроки получают одинаковые значения по
  `resourcestart`: 0 → 1000 каждого, 1 → 4000, 2 → 5000, 3 → 1 000 000 [^19].
  ИИ не получает бонусных ресурсов ни на одном уровне.
- **Постоянный «капельный» доход и читы по доходу.** В скриптах не
  найдено. ИИ добывает ресурсы стандартными шахтами, а вызовы
  `_ai_SetResouceBalance` управляют только приоритетами производства
  и торговли, но не дают бесплатных ресурсов.
- **Скорость игры.** `gc_settings_gamespeed_*` — глобальная,
  не персональная.

## Build order

Эко-ИИ — **адаптивный, но правило-ориентированный**. Решения
о постройке не записаны как фиксированный массив — это длинная
последовательность вызовов `_ai_TryUnit(plind, cid, gc_ai_unit_<X>,
target_count, false)`, в которой условие обычно ссылается на текущий
счётчик других зданий (например, `_ai_GetUnitCount(plind, cid,
gc_ai_unit_ba17) >= 2`).

Макро-фазы [^20]:

1. Всегда пытается: **Городской центр** (1 → 2 в начале), **рынок**, **мельница**.
2. Только Алжир и Турция: оппортунистический **дом**, если есть кузница, склад, рынок и бараки 17 в.
3. **Шахты** (`gc_ai_unit_minegold`, `_mineiron`, `_minecoal`) — через `_ai_BuildMines` (использует `gc_ai_dist_mines_lvl1 = 30`, `lvl2 = 60`, `expansion = 85` [^21]).
4. **Кузница** (1 шт.).
5. **Казарма 17 в. (ba17)**: цель 1 → 2 → 3 → 6 / 8 в зависимости от количества Городских центров и флага водной карты — например, 8 для большинства наций и 6 для России [^22].
6. Расширение **до 5 Городских центров**, если `centercount >= 2`.
7. **Академия** при `>= 2` ba17 и `>= 2` Городских центрах.
8. **Конюшня, артиллерийский склад, дипломатический центр, храм** после академии.
9. **Казарма 18 в. (ba18)** появляется после исследования академии и `gc_ai_upg_century`.
10. **Башни** при наличии академии и активной war-AI на `difficulty > easy`: `numTowers = Min(3, peasants div 75)` [^23].

Build order сильно зависит от нации. Каждый `cid_<nat>` (24 нации:
aus..lit) имеет собственную ветку во многих местах. Три заметных
подхода: Украина (`cid_ukr`) часто пропускает ba17 / officer-цепочку
и делает ставку на массовый musk17; Алжир и Турция (`cid_alg` /
`cid_tur`) ведут параллельную ветку «лучники из академии»; Россия
(`cid_rus`) занижает count бараков до 6 в режиме «миллионы» ресурсов.

Контрольные точки build order (репрезентативные):

- 2 ba17 + 2 Городских центров → академия [^24];
- 2 ba17 + 4 Городских центров → баланс ресурсов смещается в сторону золота [^25];
- ba18 ≥ 5 → запуск ещё 3 ba17 и шестого Городского центра [^26];
- pikemanCount ≥ 36 × 4 → переключение с пикинёров на pikeman + musk [^27];
- pikemanCount ≥ 36 × 7 + `gc_ai_max_guards (120)` → только musk17 [^28].

Баланс ресурсов адаптируется к числу крестьян: доля еды растёт 12 →
21 → 27 → 36 → 45 (× 1.3 если пикинёры ещё не апгрейжены) на
breakpoint'ах 30 / 45 / 85 / 120 крестьян [^29]. Россия и Польша
используют 16 → 24 → 31 → 40 → 49.

## Цели по производству

Точка входа — `_ai_RequestUnitsProduction` [^30].

### Крестьяне

Жёсткий cap: **400 крестьян суммарно** (по всем подконтрольным нациям)
ИЛИ **30 на одну нацию**, что выполнится раньше [^31]. Формула «2
на Городской центр» — это скорость пополнения. `_ai_DecreasePeasants`
снижает count при превышении [^32].

### Военные цели

В блоке `:2103-2150` и далее [^33]:

- `numOfficers = pikemanCount div 36` (минимум 1, если pikemanCount > 28);
- `numReiters = stable_count × 2`;
- `numInf18 = ba18_count × 2`;
- `bar_count` (цель производства inf17) = `ba17_count × 2`;
- `cannon_count = ClampInt(num_depo × 6, 6, 30)`;
- `howitzer_count = ClampInt(num_depo × 2, 2, 8)`;
- `mortar_count = ClampInt(num_depo × 8, 8, 40)`;
- 18-вечный драгун и пикинёр: зависят от апгрейда `gc_ai_upg_horse` и нации;
- Лучники (alg / sco): `_ai_GetUnitCount < farmused / 3` (на водной карте `/5`).

Эти числа — **count'ы для очереди производства**, переданные
`_ai_TryUnit`, а не жёсткие лимиты. Казармы тренируют до достижения
цели и снова просыпаются на следующем ИИ-тике.

`gc_ai_max_guards = 120` [^34] — буфер над пикинёрским порогом, после
которого включается «только musk17».

## Триггеры агрессии и атаки

Константы [^35]:

| Имя | Значение | Смысл |
|---|---:|---|
| `gc_ai_AgressorsCount` | 5 | отрядов в первой агрессорской волне |
| `gc_ai_MaxDiverArmies` | 2 | максимум диверсионных армий одновременно |
| `gc_ai_OfficerWaitTime` | 20 | сек на normal speed ожидания барабанщика или офицера |
| `gc_ai_GreArmyBattleDist` | 2 | grenadier scan grid distance |
| `gc_ai_ArmyBattleDist` | 4 | обычный scan grid distance |
| `gc_ai_BitvaInterval` | 8 | интервал перепроверки в бою |
| `gc_ai_CityDangerDist` | 20 | |
| `gc_ai_MergeArmyCityDist` | 25 | |
| `gc_ai_MergeApproachDist` | 10 | |
| `gc_ai_MinStoreHouseDist` | 9 | |

Pipeline атаки:

- `progresswarai.inc` собирает армии и раздаёт ордера. Перечисление
  ордеров (`gc_ai_armyorder_*` [^36]): `none / makebattle / bitva /
  buildmine / sabotage / agressor / makewaterbattle / transport /
  attackwall`.
- **Первая агрессорская волна** (`_ai_SendAgressors` [^37]): ИИ
  отправляет одну стартовую волну из 5 отрядов, как только в пуле
  `aiData.agressors` наберётся достаточно подвижных юнитов.
  Последующие волны идут через `_ai_ArmyMakeBattleLink`.
- **Отступление** [^38]: `myForce = _ai_GetArmyForce(pArmy)`. Если
  `uCount > 200` или `myForce > 3800`, `myForce := 100000` (трактуется
  как абсолютное превосходство, отступление не запускается). Иначе
  умножается на 8 (heavy bonus) или 2 (light). При `enForce > myForce`
  армия отступает.
- **Диверсия** (`_ai_ArmyDiversia*`): если враг слабее моей армии
  в радиусе 30 — атакуем; в радиусе 400 — тоже идём в атаку.
- **Атака стен** (`_ai_ArmyCheckWallAttack`): если цель — стена, все
  отряды в `searchRadius` армии переключаются на attack-wall
  (артиллерия исключена).
- **Peacetime** (`gbool_peacemode`): ставится при
  `gMap.settings.additional.peacetime <> default` [^39]. Пока активен,
  все агрессорские и диверсионные ветки делают early-exit [^40].
- **Дипломатия и команды:** `gPlayer[i].team`. ИИ считает игрока
  врагом, если `team` отличается или равен 0 [^41]. `_ai_IsTeamAI`
  определяет, ИИ ли в команде [^42]. Альянсы в run-time не
  формируются — команды задаются в лобби и не меняются. Сценарный
  триггер `gc_trigger_action_player_playerSetAsAlly = 19` существует,
  но ИИ из random-карт его не использует.

## Читы

| Уровень | Чит применён? | Величина |
|---|---|---|
| Easy | Да — гандикап (замедляет ИИ) | Постройка и найм на 30 % скорости |
| Normal | Да — гандикап | На 50 % |
| Hard | Да — слабый гандикап | На 75 % |
| Very hard | Нет | Паритет (100 %) |
| Impossible | Да — единственный «честный» чит | На 125 % (быстрее игрока) |

Источник — множитель `deltabuildtime` [^10]. Условие срабатывания:
`gPlayer[plind].bai and not aiData.bhumanai`. Флаг `bhumanai` [^43]
по умолчанию `False`; если его выставить, ИИ играет на паритете
независимо от уровня.

**Стартовых ресурсов ИИ не получает** — у человека и ИИ одинаковая
выдача из `resourcestart` (1000 / 4000 / 5000 / 1 000 000),
подтверждено в `initmapgen.inc` [^19].

**Доход, обзор, скорость движения** — читов не найдено. ИИ не видит
ресурсы под туманом сверх того, что обнаружили его собственные юниты:
`_ai_FillOreList` использует `GetGameObjectVisibleByHandle` [^44].

## Дипломатия

- Команды задаются в лобби (`gMap.players[i].team`). Инициализация
  делает игроков врагами, если их `team` различаются либо одна из
  команд равна 0 [^45]. Команда `0` означает «без команды» — все враги.
- ИИ против ИИ: `_ai_IsEnemiesExists` [^46] проходит по всем игрокам
  и считает врагом любого с другой командой. ИИ-игроки в одной
  команде дружат и не атакуют друг друга.
- **Динамической дипломатии нет.** Ни логики формирования альянсов,
  ни их разрыва не найдено в `lib/ai.script`, `progresseconomicai.inc`,
  `progresswarai.inc`. Сценарии могут менять отношения
  (`scenario.script` + `gc_trigger_action_player_playerSetAsAlly`),
  но в random-карте такого механизма не существует.
- ИИ относится ко всем врагам **симметрично** — `_ai_GetRandomEnemy`
  [^47] выбирает случайного врага для следующего удара. Нет
  приоритизации слабого, нет постоянной «вендетты».

## Открытые вопросы

1. **Скорость пополнения `aggressor`-пула.** Список
   `gPlayer[plInd].aiData.agressors` где-то наполняется. Чтобы
   предсказать тайминг первой атаки на свежей карте, нужно отследить
   вызовы `aiData.agressors.Add`.
2. **Активация `bhumanai`.** Флаг есть в коде, но в скриптах сеттер
   не найден. Возможно, выставляется со стороны C++-движка — например,
   через UI-чекбокс «Fair AI» в опциях или через турнирный режим.
   Стоит проверить `gui/options/`.
3. **`fAttackCount` per squad.** У TSquad есть поля `fAttackCount`,
   `fMoveCount`, `fDelayCount` (TArmy их запрашивает). Где они
   выставляются? Скорее всего, в обработчиках `unit.inc/onattack*.inc`.
4. **Что именно значит `gc_ai_max_guards = 120`.** Используется как
   буфер над пикинёрским порогом, но смысловая роль (количество
   защитников у базы?) непонятна.
5. **Логика `centerfound`.** ИИ не запускает полноценный bootstrap,
   пока `aidata.centerfound = True` [^48]. Когда флаг переключается?
   Скорее всего, при первой постройке Городского центра.
6. **Скорость принятия решений в war-AI.** `progresswarai` тикает раз
   в 2.4 g-сек на игрока, но у каждой армии собственные
   `fStateTime`-кулдауны. Чтобы знать задержку конкретного действия,
   нужно пройти `progresswarai.inc:4100-4220`.
7. **Влияние сложности на частоту атак.** Триггеры `aggressor` и
   sabotage используют `gc_ai_AgressorsCount = 5` независимо
   от уровня (масштабируется только число параллельных диверсий).
   То есть easy и impossible ИИ должны отправлять первую атаку
   в одно и то же время — отличается только скорость постройки.
   Стоит проверить эмпирически.
8. **`gc_ai_AgressorsCount = 5` против `gc_ai_max_guards = 120`.**
   Очень маленькая первая волна для армии в 100 пикинёров — всего 5
   отрядов, остальные стоят дома. Нужно проверить, масштабируются ли
   последующие волны.
9. **Дальности `gc_ai_dist_mines_lvl1 = 30` / `lvl2 = 60` /
   `expansion = 85`.** Это в тайлах. Стоит верифицировать, какой
   уровень ИИ использует на Tiny против Normal-карты.
10. **`bprogressWar` и `bprogressUpgrades`** в `aidata` — когда
    переключаются в `True`? Скорее всего, по таймеру, но трассировки
    пока нет.

---

## Источники

Все ссылки относительно `data/scripts/` в установке Cossacks 3.

[^1]: `gc_global_TimeProgressAI = 0.03 × 16 × 5 = 2.4` — `dmscript.global:1486`.

[^2]: Сдвиг `lastprogressaitime` по player-id — `player.script:140`:

    ```pascal
    lastprogressaitime := id * 0.25 + gc_global_TimeProgressAI;
    ```

[^3]: Диспетчер — `units/global.inc/progressai.inc`:

    ```pascal
    ExecuteState('ProgressEconomicAI');
    ExecuteState('ProgressWarAI');
    ```

[^4]: Перечисление уровней сложности — `dmscript.global:781-786`:

    ```pascal
    gc_player_difficulty_none       = -1;
    gc_player_difficulty_easy       =  0;
    gc_player_difficulty_normal     =  1;
    gc_player_difficulty_hard       =  2;
    gc_player_difficulty_veryhard   =  3;
    gc_player_difficulty_impossible =  4;
    ```

[^5]: `gc_MaxAIDifficultyCount = 4` — `dmscript.global:235`.

[^6]: Импоссибл для исторических битв — `initmaphistoricalbattle.inc:121`.

[^7]: Поле `aidifficulty` в записи карты — `classes.script:105`.

[^8]: Копирование в `gPlayer[i].difficulty` при старте — `initmapgen.inc:132`.

[^9]: Дефолт `easy` в лобби — `map.script:244`, `player.script:118`.

[^10]: Множитель `deltabuildtime` от сложности ИИ — `building.inc/doprogressorders.inc:222-230`:

    ```pascal
    if (gPlayer[plind].bai) and (not gPlayer[plInd].aiData.bhumanai) then
    case gPlayer[plind].difficulty of
       gc_player_difficulty_easy       : deltabuildtime *= 0.30;
       gc_player_difficulty_normal     : deltabuildtime *= 0.50;
       gc_player_difficulty_hard       : deltabuildtime *= 0.75;
       gc_player_difficulty_veryhard   : deltabuildtime *= 1.00;
       gc_player_difficulty_impossible : deltabuildtime *= 1.25;
    end;
    ```

[^11]: Дефолт `aiData.bhumanai = False` — `classes.script:2688`.

[^12]: Лимит апгрейдов башни — `progresseconomicai.inc:3653-3658`.

[^13]: Размер диверсионных групп — `progresseconomicai.inc:2322-2326`:

    ```pascal
    case difficulty of
       gc_player_difficulty_normal     : numdiver := 0;
       gc_player_difficulty_hard       : numdiver := 2;
       gc_player_difficulty_veryhard   : numdiver := 4;
       gc_player_difficulty_impossible : numdiver := 4;
    end;
    ```

[^14]: Лимит апгрейдов шахты — `progresseconomicai.inc:2202-2212` и `~2396-2410`.

[^15]: Запрет гаубиц и мортир на easy — `progresseconomicai.inc:2349-2353`.

[^16]: Аварийный найм наёмников при `difficulty >= hard` — `progresseconomicai.inc:2306`.

[^17]: `bricks1` — только veryhard и impossible — `progresseconomicai.inc:2452`.

[^18]: Поблажка стрелкам игрока на `<= normal` — `unit.script:7367`.

[^19]: Раздача стартовых ресурсов одинакова для всех игроков — `initmapgen.inc:166-189`.

[^20]: Макро-фазы build order — `progresseconomicai.inc:2700-2830`.

[^21]: Дальности шахт — `dmscript.global:503-506` (`gc_ai_dist_mines_lvl1 = 30`, `lvl2 = 60`, `expansion = 85`).

[^22]: Цель ba17 — `progresseconomicai.inc:2771`:

    ```pascal
    _ai_TryUnit(plind, cid, gc_ai_unit_ba17, 8, False)
    // для России — 6
    ```

[^23]: Башни — `progresseconomicai.inc:2926-2929`:

    ```pascal
    numTowers := Min(3, peasants div 75);
    ```

[^24]: 2 ba17 + 2 Городских центров → академия — `progresseconomicai.inc:2796`.

[^25]: 2 ba17 + 4 Городских центров → баланс в сторону золота — `progresseconomicai.inc:2036-2039`.

[^26]: ba18 ≥ 5 → ещё 3 ba17 и шестой Городской центр — `progresseconomicai.inc:2789-2793`.

[^27]: pikemanCount ≥ 36 × 4 → pikeman + musk — `progresseconomicai.inc:2134`.

[^28]: pikemanCount ≥ 36 × 7 + `gc_ai_max_guards` → только musk17 — `progresseconomicai.inc:2152-2158`.

[^29]: Баланс еды по числу крестьян — `progresseconomicai.inc:1999-2031`.

[^30]: `_ai_RequestUnitsProduction` — `progresseconomicai.inc:2085+`.

[^31]: Cap крестьян — `progresseconomicai.inc:2088`:

    ```pascal
    var numpeasants : Integer = _ai_GetUnitCount(plind, cid, gc_ai_unit_center) * 2;
    if (peasants_total < 400) or (peasants_this_nation < 30) then
       if food < 700 then queue numpeasants
       else queue 1
    ```

[^32]: `_ai_DecreasePeasants` — `progresseconomicai.inc:3856`.

[^33]: Цели по военным юнитам — `progresseconomicai.inc:2103-2150` (и далее `:2347`, `:2351`, `:2352` для пушек, гаубиц и мортир).

[^34]: `gc_ai_max_guards = 120` — `dmscript.global:500`.

[^35]: Константы агрессии и атаки — `dmscript.global:474-481`.

[^36]: Перечисление `gc_ai_armyorder_*` — `dmscript.global:430-438`.

[^37]: Первая агрессорская волна — `progresswarai.inc:3560-3568` (`_ai_SendAgressors`):

    ```pascal
    if (not gbool_peacemode) and (agressorsSent = 0) and
       (agressors.GetCount >= gc_ai_AgressorsCount) then
    begin
       pArmy := _ai_CreateAgressorArmy(plInd, 5, agressors);
       _ai_ArmyMakeAgressorBattle(pArmy);
    end;
    ```

[^38]: Логика отступления — `progresswarai.inc:2398-2407`:

    ```pascal
    myForce := _ai_GetArmyForce(pArmy);
    if (uCount > 200) or (myForce > 3800) then
       myForce := 100000;
    // иначе myForce *= 8 (heavy) или *= 2 (light)
    if (enForce > myForce) then ...retreat...
    ```

[^39]: Установка `gbool_peacemode` — `dogenerate.inc:2060-2064`.

[^40]: Early-exit агрессии и диверсий при peacetime — `progresswarai.inc:2787` и `:3562`.

[^41]: Враждебность по `team` — `initmapgen.inc:160`.

[^42]: `_ai_IsTeamAI` — `ai.script:527`.

[^43]: Поле `bhumanai` — `classes.script:2611`.

[^44]: Видимость ресурсов для ИИ — `ai.script:228` (`_ai_FillOreList` использует `GetGameObjectVisibleByHandle`).

[^45]: Инициализация отношений по командам — `initmapgen.inc:158-163`:

    ```pascal
    if (myteam <> histeam) or (histeam = 0) or (myteam = 0) then
       AddPlayerEnemyPlayerByHandle(...)
    else
       AddPlayerFriendPlayerByHandle(...);
    ```

[^46]: `_ai_IsEnemiesExists` — `ai.script:7-19`.

[^47]: `_ai_GetRandomEnemy` — `progresseconomicai.inc:67-94`.

[^48]: Условие `aidata.centerfound = True` — `ai.script:451`.
