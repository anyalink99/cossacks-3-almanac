# Recon: тики, сабтики, время

Модель времени в Cossacks 3: главный progress-loop, интервалы sub-tick
state-machine, переменный шаг по времени, адаптивная скорость игры. Это база,
чтобы понять, почему симуляция не воспроизводится даже на одном хосте после
Save / Load и почему разные машины расходятся. Все ссылки на код и сами
Pascal-блоки собраны в разделе [Источники](#источники) в конце документа.

**Связанные документы:**

- [determinism_audit.md](determinism_audit.md) — RNG-сайты в добыче и
  бою; этот документ описывает **когда** они вызываются.
- [server_sync_architecture.md](server_sync_architecture.md) — как
  server-authoritative архитектура связана с тиками; sync-пакеты в
  real-time против game-time-логики.

## TL;DR

- В коде сосуществуют **три временных шкалы**: real time (стенные секунды),
  game time (логическое время симуляции, масштабируется по `TimeSpeedFactor`)
  и frames (кадры анимаций; 32 кадра = 1 game-second).
- Главный progress-loop тикает каждые **20 мс** реального времени
  (`gc_progress_Interval = 0.02`). Внутри — раздача pathfinding-запросов,
  периодические события, экономика, адаптация скорости игры.
- Юниты тикают **не каждый кадр**, а раз в свой интервал: военные —
  100 мс, крестьяне — 135 мс (`gc_statemachine_interval_*`).
- На Save / Load часть таймштампов `gProgress.last*time` **не
  восстанавливается точно** — подсистемы могут пропустить тик или
  получить два подряд. Это один из источников нерекурсивности.

---

## 1. Три временных шкалы

В коде сосуществуют три разных «времени»:

| Шкала | Что | Где |
|---|---|---|
| **Real time** | Стенные секунды | `_misc_GetRealTime`, `GetCurrentTime` |
| **Game time** | Логическое время симуляции, масштабируется по `TimeSpeedFactor` | `GetGameTime`, обозначается `gametime` |
| **Frames** | Дискретные кадры анимаций и таймингов в скриптах | `gc_time_to_frames = 32` |

**Ключевые соотношения:**

```
1 game-second  =  32 frames                      (gc_time_to_frames)
1 game-second  =  1 / (TimeSpeedFactor/10)  real-seconds
                = 1.43 real-sec @ slow (factor 7)
                = 1.00 real-sec @ normal (factor 10)
                = 0.71 real-sec @ fast (factor 14)
```

Game-speed presets [^1]:

- `gc_settings_gamespeed_0 = 7` (slow)
- `gc_settings_gamespeed_1 = 10` (normal)
- `gc_settings_gamespeed_2 = 14` (fast)

Это лобби-опция `gMap.settings.additional.gamespeed`. Таблица всех скоростей —
[`reports/map/lobby_settings.md`](../reports/map/lobby_settings.md#gamespeed--скорость-партии);
расшифровка поведения — [`game_settings.md`](../world/game_settings.md) §3.6.

Все длительности в скриптах (анимации, `buildtime`, `attackpause`) — в
**frames**. Перевод в game-seconds: `frames / 32`. Перевод в real-seconds:
дополнительно делить на `TimeSpeedFactor/10`.

---

## 2. Главный progress-loop

Сердце симуляции живёт в `progress/progress.inc/nothing.inc` (745 строк). Это
state-машина «прогресса» — отдельный «игрок» в архитектуре Cossacks 3, который
тикает каждый раз, когда движок зовёт state `Nothing`.

### 2.1 Структура одного тика

В одном тике progress-loop читает `gametime`, считает `deltatime` относительно
прошлого тика и, если игра не на паузе, выполняет полный набор подсистем:
начисление экономики через `_res_ProcessEconomy(deltatime)`, раздача
pathfinding-запросов из `gWaterPathList` и `gGOPathList`, обработка
периодических событий по таймштампам и адаптация скорости игры по реальному
FPS. В конце тика `gProgress.progresstick` инкрементируется и
`gProgress.lastprogresstime` обновляется на текущий `gametime` [^2].

### 2.2 Что progress-loop НЕ делает

Он **не тикает каждого юнита** напрямую. Юниты — отдельные state-машины с
собственными циклами `Nothing`. Progress-loop:

- запускает экономику (`_res_ProcessEconomy(deltatime)`);
- раздаёт pathfinding-запросы;
- пушит периодические события;
- управляет progress sections (см. §3) — определяет, сколько юнитов *имеет
  право* потикать в этом кадре.

Юниты тикают сами, когда движок их зовёт через state machine, **с интервалом,
зависящим от их класса** (см. §3).

---

## 3. State-machine intervals — сабтики на классах юнитов

Здесь главный механизм sub-tick поведения.

### 3.1 Базовые интервалы

Константы `gc_statemachine_interval_units = 100` и
`gc_statemachine_interval_peasants = 135` задают миллисекунды реального
времени между тиками state machine для юнита данного класса [^3]:

- военные юниты тикают **~10 Hz** (10 раз в секунду);
- крестьяне тикают **~7.4 Hz** (около 7 раз в секунду).

То есть крестьянин получает обновление своего state machine **реже**, чем
солдат. Это экономия на массовых экономических симуляциях.

### 3.2 Progress sections

Не все юниты тикают каждый кадр — они разбиты на «секции», и движок проходит
по `secmax` объектам за тик [^4]. Секция — батч юнитов одного класса, который
должен быть «обновлён» в течение `interval` мс. `cycles` — сколько тиков
progress-loop успеет до следующего обязательного обновления секции. Эти числа
адаптируются по реальной нагрузке.

### 3.3 Импликации сабтиков

1. **Крестьяне принимают решения реже военных.** Время реакции на «нашёл /
   потерял ресурс» составляет около 135 мс, что заметно на высокой скорости
   игры.

2. **Порядок тиков юнитов в секции — детерминирован** (по списку), но границы
   секции могут смещаться между фреймами в зависимости от FPS. На высоком FPS
   все юниты тикают каждый раз, на низком — секция режется на куски.

3. **Под нагрузкой (тысячи юнитов) разные хосты с разным FPS получают разные
   «куски» секции в одном тике.** Это потенциальный источник межхостового
   рассинхрона, но в lockstep multiplayer он должен компенсироваться (см. §5).

---

## 4. Периодические события (mod-N + timed)

Внутри progress-loop срабатывают разные подсистемы по двум паттернам.

### 4.1 По счётчику тиков (`progresstick mod N`)

Pathfinding для воды выполняется каждый второй тик: условие проверяет
`gProgress.progresstick mod 2 = 0`, если есть водные запросы [^5]. Сетевая
синхронизация unit-параметров через `_misc_SyncUnitsParams` срабатывает каждый
53-й тик [^6].

### 4.2 По таймштампам (`gametime > last*time`)

Большинство периодических подсистем работает по схеме «если игровое время
превысило последний таймштамп — выполнить и переустановить таймштамп на
будущее». Все интервалы заданы как множители от `gc_progress_Interval = 0.02`
game-sec [^7]:

- `gc_progress_TimeMiscPlSecMax = 200 × 0.02 = 4.0` game-sec
- `gc_progress_TimePoolPlSecMax = 70 × 0.02 = 1.4` game-sec
- `gc_progress_TimeSearchEnemyCounter = 5 × 0.02 = 0.1` game-sec
- `gc_progress_TimeSearchEnemyCountSum = 10 × 0.02 = 0.2` game-sec
- `gc_progress_TimeSearchEnemyCountMid = 50 × 0.02 = 1.0` game-sec
- `gc_progress_TimeProgressStatistics = 10 × 0.02 = 0.2` game-sec
- `gc_progress_TimeProgressTopZones = gc_top_GlobalTick × 0.02`
- `gc_progress_TimeSoundProgressFreq = 0.02`

Эти таймштампы (`gProgress.last*time`) **сохраняются в save** и
инициализируются через `random` [^8] — чтобы **разнести по фазе** разные
подсистемы и избежать spike CPU, если бы все тикали в одном кадре.
Используется `random` (а не `RandomExt`), но эти инициализации происходят один
раз и потом просто переживают как обычное состояние.

---

## 5. Variable timestep + адаптивная скорость

### 5.1 deltatime — переменный

Переменная `deltatime` равна реальному игровому времени, прошедшему с
прошлого тика progress-loop, и **не фиксирована** [^2]:

- на высоком FPS: `deltatime ~16` мс, каждый тик — маленький;
- на низком FPS: `deltatime ~30+` мс, каждый тик — большой.

Экономика тикает через `_res_ProcessEconomy(deltatime)` — то есть **доход
шахты за один тик пропорционален `deltatime`**. Шахты дают одинаковый
накопленный доход в game-seconds независимо от FPS, потому что суммарный
`gametime` детерминирован для game speed × wall time.

### 5.2 Адаптивная скорость (главное)

Когда CPU не успевает обработать всех юнитов за реальное время, срабатывает
ключевой механизм [^9]:

1. Engine считает реальный FPS (`realfps`) и performance metrics (`pr`, `pp`,
   `pt`).
2. Если `realfps < 20`, `secmax` (макс. юнитов на тик) уменьшается.
3. Параллельно вызывается `SetTimeSpeedFactor(newspeed)` — **снижение игровой
   скорости динамически**.

Минимальный лимит — `5` (ниже даже `gc_settings_gamespeed_0 = 7`). То есть
под пиковой нагрузкой игра **сама замедляется до 50% от slow**. Здесь `speed`
— установленная пользователем скорость (`gamespeed_0/1/2`), `newfactor` —
коэффициент 0..1 в зависимости от того, насколько симуляция «не успевает».
Шаг изменения ограничен константами `cSpeedStepUp` и `cSpeedStepDown` (вместе
не больше 0.667 за один проход).

В мультиплеере сервер рассылает изменение через
`LanSendParser(gc_LAN_GAME_SYNC_GAMETIME, ...)` — все клиенты подстраиваются.

### 5.3 Импликации для детерминизма

**В single player:**

- Адаптивная скорость означает, что на разных машинах одна и та же реальная
  минута даёт **разное прошедшее game-time**. Разные деревья нарублены, разные
  шахты выкопаны.
- Это объясняет наблюдение «между хостами добыча разная»: даже с фиксированным
  сейвом, host A с быстрым CPU за 5 real-min прошёл условные 7 game-min,
  host B с медленным — 6.5 game-min. Разница в game-time даёт разную добычу.

**В multiplayer:**

- Server рассылает `SetTimeSpeedFactor` — все хосты получают одинаковое
  game-time-per-real-time.
- Но «секция» (какие юниты обработаны в каком тике) на разных хостах может
  варьироваться, потому что `secmax` тоже подстраивается локально.

**Same host, разные запуски одного сейва:**

- Адаптивная скорость зависит от текущей системной нагрузки (фоновые
  процессы, GPU и т. п.). Значит, даже на одной и той же машине между двумя
  запусками `SetTimeSpeedFactor` может сработать в разные моменты, давая
  разную сумму game-time за равное real-time.

---

## 6. Save / Load — что нормализуется, что теряется

### 6.1 Хуки

| State machine | OnBeforeSave | OnAfterLoad |
|---|---|---|
| Progress | `SwitchTo('Nothing')` | `SwitchTo('Nothing')` |
| Unit (peasant) | `SwitchTo('Nothing')` | `SwitchTo('Nothing')` (+ ship childs если водный) |
| Env (resource) | — (по умолчанию) | `ExecuteState('Initial'); SwitchTo('Nothing')` |

Соответствующие файлы хуков [^10].

### 6.2 Что точно сохраняется

Из формата network sync (он же save) [^11]:

- `posx`, `posz` (Float — sub-cell позиция);
- `upx, upy, upz, dirx, diry, dirz` (ориентация);
- `statestag` (битовое состояние тегов);
- `sto` (handle цели);
- `stpx, stpz, sta` (state target позиция и угол стрелки);
- `cid, id, pl, hp, bbuilt, bdead, buildprogress`;
- **`uniqrnd`** (per-unit nonce, см. [determinism_audit.md](determinism_audit.md)).

Из `gProgress` (тип `TProgress`) [^12]:

- `lastprogresstime`, `progresstick` — счётчик тиков и время последнего тика;
- все `last*time` для периодических событий.

Из per-unit `TObj` [^13]:

- `lastprogresstime`, `progresstick`, `soundlastprogresstime`,
  `soundprogresstick`, `soundcounterlastprogresstime`,
  `soundcounterprogresstick` — счётчики прогресса самого юнита.

### 6.3 Что НЕ сохраняется (или сбрасывается)

- **Текущая фаза анимации** — `OnBeforeSave` вызывает `SwitchTo('Nothing')`,
  что обрывает текущий анимационный цикл. После Load крестьянин начинает
  анимацию с нулевой фазы (или с той, что подобрал движок).
- **In-flight pathfinding state** — текущая позиция в track-point list, фаза
  интерполяции между трекпойнтами. После Load крестьянин стоит в позиции из
  save, и ему дают новый путь.
- **Глобальное состояние `random`** — почти точно НЕ сохраняется в save
  format. После Load `random` начинается «с нового места».
- **Позиция в обходе progress section** — после Load секция начинается заново.
- **Текущая нагрузка / FPS history** (`garrfloat_perf_progress`) — глобальный
  массив текущих perf-метрик. После Load заполняется заново, и адаптивная
  скорость может стартовать с другого `TimeSpeedFactor`.

### 6.4 Каскад на Load

1. Engine читает поля `gProgress` (включая `lastprogresstime`, `progresstick`).
2. Все юниты сбрасываются в `'Nothing'` через хук — теряется фаза анимации.
3. Все ресурсы сбрасываются `Initial → Nothing` через хук.
4. `garrfloat_perf_progress` обнуляется — adaptive speed начинает с дефолта.
5. Глобальный `random` стартует с того состояния, которое движок считает
   уместным (нет признаков, что он сериализуется).
6. Первый тик после Load: `deltatime = 0` (потому что
   `lastprogresstime = gametime` сразу после Load), значит цикл
   `if deltatime > 0` не сработает; переход к второму тику со стандартным
   `deltatime`.

---

## 7. Sub-tick state — что это и почему важно

«Sub-tick state» — состояние, которое **меняется внутри одного логического
тика** или между тиками state machine конкретного юнита, но не персистится
на гранулярности save / load.

### 7.1 Примеры sub-tick state у крестьянина

| State | Где живёт | Восстанавливается на Load? |
|---|---|---|
| Фаза анимации `workwood` / `workfood` / `walkwood` | engine animation system | НЕТ — `SwitchTo('Nothing')` сбрасывает |
| Sub-tile интерполяция позиции при walk | engine track-point system | Частично — позиция сохраняется, но фаза интерполяции теряется |
| Текущий `progresstick` юнита | `TObj.progresstick` | ДА — поле сохраняется |
| `lastprogresstime` юнита | `TObj.lastprogresstime` | ДА |
| `standtime` (сколько стоит без работы) | `TObj.standtime` | ДА (вероятно, есть в `TObj`) [^13] |
| Активный order (target, тип) | `TObj.orders[]` | ДА |
| `restype`, `resamount` (что несёт сейчас) | `TObj.*` | ДА |
| Текущая цель ресурса | `TObj.sto` | ДА (handle сохраняется) |

### 7.2 Где sub-tick state создаёт расхождение

После Load все sub-tick поля **либо восстановлены**, либо **сброшены в
нейтральное**. Кажется, что всё в порядке. Но:

1. Анимация сброшена — крестьянин начинает **новый work-cycle с фазой 0**,
   тогда как до сейва у него могла быть фаза 0.7. Значит, **первый удар после
   Load происходит позже, чем произошёл бы в той симуляции**.

2. Это смещение каскадирует: первая доставка ресурса позже — следующий поиск
   дерева в другое game-time — попадает в другую фазу
   `progresstick mod 53`-синхронизации — возможен другой выбор дерева через
   `random` (см. [determinism_audit.md](determinism_audit.md) §3).

3. Pathfinding сброшен — новый запрос к topology — tie-breaking в pathfinder
   — возможно, другой путь к тому же дереву.

Каждое из расхождений мало само по себе, но они **накапливаются в течение
минуты симуляции** до заметной разницы в добыче.

---

## 8. Сводная картина: почему симуляция расходится

### 8.1 Причины **на одном хосте**, разные запуски одного сейва

| Источник | Влияние |
|---|---|
| Анимационные фазы сбрасываются — первый удар сдвинут по фазе | Каскад в timing |
| Pathfinding tie-breaking даёт разный путь к тому же дереву | Разное время прибытия |
| Глобальное состояние `random` различается между запусками | Разные исходы 7 RNG-сайтов в добыче ([determinism_audit.md](determinism_audit.md) §3) |
| Adaptive speed зависит от текущей системной нагрузки | Разное реальное game-time за равное real-time |
| Progress section batch boundary стартует с нуля | Юниты сначала тикают «свежей пачкой» |

### 8.2 Дополнительные причины **между хостами**

| Источник | Влияние |
|---|---|
| Разный CPU — разный `realfps` — разный `TimeSpeedFactor` (single player) | Разное game-time за минуту real-time |
| Разная сериализация Float между x87 / SSE / FMA | Микро-расхождения в физике и геометрии |
| Разная инициализация `random` для `gProgress.last*time`, если игра стартует с нуля (не Load) | Разная фаза периодических событий |

### 8.3 Что детерминировано при Save / Load

- HP всех ресурсов и юнитов (целые числа).
- Целочисленные ресурсы игрока.
- `uniqrnd`, `progresstick`, все `last*time` (явно персистятся).
- Шахта: `produce_rate × N_workers × deltatime` — арифметика. Если сумма
  `deltatime` за окно одинакова между запусками (а она примерно одинакова
  при стабильном FPS), результат одинаков.

---

## 9. Связь с моделью добычи

**В аналитической модели** (см.
[peasant_extraction.md](../world/peasant_extraction.md)) мы считаем **в
game-time**, не в real-time. Это правильный подход — формулы инвариантны к
скорости игры.

**Но** реальный игрок сравнивает добычу **за real-time окно** (например,
«5 real-min»). Связь:

```
real_time × (TimeSpeedFactor / 10) = game_time
```

Если на хосте A `TimeSpeedFactor = 14` (заявленный fast) **поддерживается
строго**, то 5 real-min = 7 game-min. Если adaptive speed снизил его до 12,
то 5 real-min = 6 game-min — **на 15% меньше добычи** при идентичной
симуляции.

**Импликация:** при эмпирической калибровке модели нужно либо:

- (a) использовать game-time для измерений (но игра показывает real-time в
  UI; возможно, через replay с известной длительностью);
- (b) замерять FPS через игровой профайлер и вычислять effective speed factor;
- (c) прогонять короткие тесты (минуту) на лёгкой карте с малым числом
  юнитов, чтобы adaptive speed не срабатывал.

---

## 10. Cross-references

- [determinism_audit.md](determinism_audit.md) — RNG-сайты в добыче и бою.
  Этот документ ссылается на §6 (save / load) и §5 (адаптивная скорость) для
  объяснения механизма недетерминизма.
- [peasant_extraction.md](../world/peasant_extraction.md) — модель добычи в
  game-time. §1 этого документа дополняет переводом game-time ↔ real-time с
  учётом адаптивной скорости.
- [building_mechanics.md](../world/building_mechanics.md) — `buildtime` в
  frames, `deltatime` для строительства.

---

## Источники

Все ссылки относительно `data/scripts/` в установке Cossacks 3.

[^1]: Game-speed presets — `dmscript.global:1027-1029`:

    ```pascal
    gc_settings_gamespeed_0 = 7;     // slow
    gc_settings_gamespeed_1 = 10;    // normal
    gc_settings_gamespeed_2 = 14;    // fast
    ```

[^2]: Структура одного тика progress-loop — `progress/progress.inc/nothing.inc:71-759`:

    ```pascal
    var lastprogresstime : Float = gProgress.lastprogresstime;
    var gametime : Float = GetGameTime;
    var deltatime : Float = gametime - lastprogresstime;

    if (lastprogresstime>0) and (deltatime>0) then  // not on pause
    begin
       var perffps : Float = GetProgressPlayersPerformance;
       perffps := MinFloat(perffps, 1/FramesPerSecond);
       var cycletime : Float = perffps*(GetTimeSpeedFactor/10);

       _res_ProcessEconomy(deltatime);  // mines, fields regeneration

       // ... pathfinding for all units in gWaterPathList / gGOPathList ...
       // ... periodic events by timeouts (see section 4) ...
       // ... game-speed adaptation by real FPS (see section 5) ...
    end;

    if (lastprogresstime>0) and (deltatime>0) then
       gProgress.progresstick := gProgress.progresstick + 1;
    gProgress.lastprogresstime := gametime;
    ```

[^3]: Базовые интервалы state machine — `dmscript.global:1458-1459`:

    ```pascal
    gc_statemachine_interval_units = 100;       // ms — military units
    gc_statemachine_interval_peasants = 135;    // ms — peasants
    ```

[^4]: Progress sections — `progress/progress.inc/nothing.inc:475-498`:

    ```pascal
    var psind : Integer = GetPlayerProgressSectionIndexByInterval(plHnd, gc_statemachine_interval_peasants);
    peacount := GetPlayerProgressSectionCountGOByIndex(plHnd, psind);
    // ...
    psind := GetPlayerProgressSectionIndexByInterval(plHnd, gc_statemachine_interval_units);
    warcount := GetPlayerProgressSectionCountGOByIndex(plHnd, psind);

    psgocount := Max(peacount, warcount);
    secmax := _misc_RoundUp(psgocount/cycles);    // target: process all in `cycles` ticks
    secmax := Max(50, Min(psgocount, secmax));
    ```

[^5]: Pathfinding для воды каждый второй тик — `progress/progress.inc/nothing.inc:117`:

    ```pascal
    if (gWaterPathList.GetCount>0) and ((gGOPathList.GetCount=0) or (gProgress.progresstick mod 2=0)) then
    ```

[^6]: Сетевая синхронизация unit-параметров каждый 53-й тик — `progress/progress.inc/nothing.inc:405`:

    ```pascal
    if ((gProgress.progresstick mod 53)=0) and ... then
       _misc_SyncUnitsParams;
    ```

[^7]: Базовый шаг и интервалы периодических событий — `dmscript.global:1489-1498`:

    ```pascal
    gc_progress_Interval               = 0.02;       // base step (50 Hz)
    gc_progress_TimeMiscPlSecMax       = 200 * 0.02;
    gc_progress_TimePoolPlSecMax       = 70  * 0.02;
    gc_progress_TimeSearchEnemyCounter = 5   * 0.02;
    gc_progress_TimeSearchEnemyCountSum= 10  * 0.02;
    gc_progress_TimeSearchEnemyCountMid= 50  * 0.02;
    gc_progress_TimeProgressStatistics = 10  * 0.02;
    gc_progress_TimeProgressTopZones   = (gc_top_GlobalTick * 0.02);
    gc_progress_TimeSoundProgressFreq  = 0.02;
    ```

    Шаблон применения интервалов — например, для `lastmiscplsecmaxtime`:

    ```pascal
    if gametime > gProgress.lastmiscplsecmaxtime then
    begin
       gProgress.lastmiscplsecmaxtime := gametime + gc_progress_TimeMiscPlSecMax;
       // ... subsystem code ...
    end;
    ```

[^8]: Инициализация таймштампов через `random` — `miscext.script:1891-1898`:

    ```pascal
    gProgress.lastprogresshistorytime := random;
    gProgress.lastmiscplsecmaxtime := random*gc_progress_TimeMiscPlSecMax;
    // ...
    ```

[^9]: Адаптивная скорость — `progress/progress.inc/nothing.inc:510-628`:

    ```pascal
    var newspeed : Float = speed*(1-newfactor);
    newspeed := Clamp(newspeed, 5, gc_settings_gamespeed_2);
    // ...
    SetTimeSpeedFactor(newspeed);
    ```

[^10]: Хуки Save / Load — `progress/progress.inc/{onbeforesave,onafterload,initial}.inc`, `units/unit.inc/{onbeforesave,onafterload}.inc`, `env/env.inc/onafterload.inc`.

[^11]: Формат network sync (он же save) — `miscext2.script:4002-4027`. Включает `posx`, `posz`, ориентацию, `statestag`, `sto`, `stpx`, `stpz`, `sta`, `cid`, `id`, `pl`, `hp`, `bbuilt`, `bdead`, `buildprogress`, `uniqrnd`.

[^12]: Структура `TProgress` — `classes.script:6011`. Содержит `lastprogresstime`, `progresstick` и все `last*time` для периодических событий.

[^13]: Поля прогресса юнита в `TObj` — `classes.script:36-41, 3704+`. Включают `lastprogresstime`, `progresstick`, `soundlastprogresstime`, `soundprogresstick`, `soundcounterlastprogresstime`, `soundcounterprogresstick`.
