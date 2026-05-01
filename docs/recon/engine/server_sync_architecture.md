# Recon: серверная архитектура и сетевая синхронизация

Модель сетевой синхронизации в C3 — кто симулирует, что и когда передаётся
по сети, как это связано с тиками и `random`. Третий документ в связке с
[determinism_audit.md](determinism_audit.md) (RNG-сайты) и
[ticks_and_subticks.md](ticks_and_subticks.md) (модель времени). Без этого
слоя нельзя объяснить, почему даже синхронизация adaptive speed между
хостами не делает поведение воспроизводимым.

Все пути к скриптам ниже — относительно `data/` в установке Cossacks 3.
Все ссылки на код и сами Pascal-блоки собраны в разделе
[Источники](#источники) в конце документа.

## TL;DR

- **C3 — server-authoritative, не lockstep.** Один хост (сервер) считает
  всю гейм-логику; остальные (клиенты, реплеи) только отображают.
- В коде это везде паттерн `if not (_net_IsClient or _net_IsReplay) then …`
  — гейм-логика выполняется только на сервере [^1].
- Sync-пакеты идут двумя путями: per-event (одна сделка, один захват) и
  периодически (раз в 53 progress-тика — `_misc_SyncUnitsParams`).
- Из-за этого детерминизм между хостами **не обязан** держаться — в
  отличие от lockstep, расхождение по `random()` нельзя исправить общим
  seed.

---

## 1. Главное: C3 — server-authoritative, **не** lockstep

### 1.1 Что это значит

В классическом lockstep RTS (StarCraft, Age of Empires II) **все хосты
прогоняют идентичную симуляцию** с одного seed PRNG, синхронизируясь
только по командам игроков. Любой rng-вызов идентичен на всех хостах,
потому что входные состояния идентичны.

C3 сделан **по-другому**: один хост (сервер) симулирует, остальные
(клиенты) **только отображают** то что им присылают. Это видно по
основополагающему паттерну, который в коде встречается десятки раз:
блок гейм-логики оборачивается в `if (bProcess) then …`, где `bProcess`
определяется как `not (_net_IsClient or _net_IsReplay)` [^1].

Клиенты и replay'и **не выполняют гейм-логику**. Они слушают пакеты от
сервера и применяют изменения локально. Этот паттерн встречается в
обработчиках добычи ресурса, нанесения урона, прогресса строительства и
во множестве других хуков [^2].

### 1.2 Net modes

Пять режимов сети [^3]:

| Mode | Условие | Кто симулирует |
|---|---|---|
| `_net_IsOffline` | `GetLanMode = 0` (single player) | Локально (= сервер для себя) |
| `_net_IsServer` | `GetLanMode > gc_lanmode_client` | Этот хост |
| `_net_IsClient` | `GetLanMode = gc_lanmode_client` | Принимает от сервера |
| `_net_IsRecord` | `GetRecordManagerGameMode = 2` | Локально, плюс пишет replay |
| `_net_IsReplay` | `GetRecordManagerGameMode = 1` | Принимает из record-файла |

Single-player = `_net_IsOffline` = клиент-сам-себе-сервер. `bProcess`
всегда true.

### 1.3 Архитектурные следствия

- **Зачем `random` сидируется через `SetRandomKey(uniqrnd*MaxInt)`** [^4]:
  чтобы клиент мог **воспроизвести** дисперсию снаряда от того же seed.
  Сервер шлёт `frnd : Float = RandomExt` → клиент применяет
  `SetRandomKey` со значением, восстановленным из этого `frnd`, и
  получает идентичную дисперсию.

- **Почему `random` (без `SetRandomKey`) не критичен для межхостовой
  синхронизации**: его результат используется только на сервере (под
  `bProcess`). Клиенты не вызывают эту ветку. Авторский комментарий это
  прямо подтверждает: «использую general random, синхронизировать его
  не нужно, а randomext может изменить запланированные результаты на
  разных PC» [^5]. Разработчики **знают**, что `random` не воспроизводим
  между хостами, и используют его только там, где это не нужно для
  синхронизации.

---

## 2. Что синхронизируется и как

### 2.1 Per-event пакеты (отправляются по факту события)

Каждый игровой объект-«игрок» (player state machine) имеет пары
`WriteX` / `ReadX` для каждого типа события. В каталоге глобальных
обработчиков таких пар больше тридцати:

| Событие | Write* | Read* | Что несёт |
|---|---|---|---|
| Создание юнита | writenew.inc | readnew.inc | uid, race/base, pos, cid |
| Уничтожение | writefree.inc | readfree.inc | uid |
| Смерть | writedeath.inc | readdeath.inc | uid |
| Команда move | writemove.inc | readmove.inc | uid, target pos |
| Order | writeorder.inc | readorder.inc | uid, order type, target |
| Search/найти ресурс | writesearch.inc | readsearch.inc | — |
| Снаряд | writeproj.inc | readproj.inc | uid, weapon, **frnd** для синка дисперсии |
| Apply upgrade | writeapply.inc | readapply.inc | uid, upgrade |
| Construct progress | writeconstruct.inc | readconstruct.inc | uid, hp delta |
| ... ещё ~25 событий | | | |

Шаблон обработчика создания таков [^6]: сервер локально создаёт объект
через `CreatePlayerGameObjectHandleByHandle`, **получает локальный uid**,
и отсылает клиентам этот uid в пакете. Клиенты создают локальные
объекты с **тем же uid** (таблица uid → handle) и применяют параметры.
Так сохраняется консистентность ссылок между хостами.

### 2.2 Periodic пакеты (по таймауту)

Главный цикл прогресса проверяет три таймера каждый тик [^7]:

| Что | Период | Шкала |
|---|---|---|
| `WriteRes` (текущий запас ресурсов игрока) | 0.1 sec | **real time** |
| `WriteLanSyncData` (общий блок sync) | 0.1 sec | **real time** |
| `WriteStats` (счётчики) | 20 sec | **real time** |

**Важно:** периоды в **real time**. Это значит:
- На fast (×1.4) game speed между двумя `WriteRes` проходит 0.1 real-sec
  ≈ 0.14 game-sec.
- На slow (×0.7) — 0.07 game-sec.
- На adaptively-замедленной до 5/10 = 0.5× — 0.05 game-sec.

Соответственно, **частота пакетов одинакова в real-time на разных
скоростях**, что хорошо для пропускной способности сети, но плохо для
воспроизводимости game-логики.

### 2.3 Sync unit params (mod 53)

Раз в 53 прогресс-тика сервер вызывает `_misc_SyncUnitsParams` [^8]: тот
берёт юнитов из `gLanSyncUnitsParamsUIDList` (юниты, которые сервер
пометил как «нуждающихся в sync», обычно после нетривиальных изменений)
и шлёт их состояние через `WriteSyncUnitsParams` [^9].

**Период:** каждый 53-й tick прогресса. Tick зависит от FPS (см.
[ticks_and_subticks.md](ticks_and_subticks.md) §5). При 50 Hz tick это
~1.06 sec real-time. То есть unit param sync лагает в среднем на ~1
секунду real-time.

### 2.4 GameTime/speed sync

**Только сервер** (внешнее условие `_net_IsServer`) меняет
`TimeSpeedFactor`. Сервер отсылает пакет с парой (`GetGameTime`,
`newspeed`) через `LanSendParser(gc_LAN_GAME_SYNC_GAMETIME, …)` [^10].
Клиенты применяют — это синхронизирует **прогрессию игрового времени**.

Условие отправки: только когда `newspeed <> GetTimeSpeedFactor`
(фактическое изменение). Между изменениями — никаких сообщений; клиенты
просто продолжают тикать с последней установленной скоростью.

### 2.5 On-demand full sync

При подозрении на десинк выполняется тяжёлая синхронизация всего
состояния:

1. Клиент шлёт `gc_LAN_GAME_SYNC_REQUEST` с тройкой `(cuid, nuid, envc)`
   (счётчики uid'ов) [^11].
2. Сервер запускает `_misc_WriteSyncServer` и шлёт **полное состояние
   всех юнитов** [^12]: для каждого uid — `bexists`, и (если объект
   существует) `racename`, `basename`, `posx/z`, `scale`, ориентация,
   `statestag`, `sto`, `stp`, `sta`, `cid`, `id`, `pl`, `hp`, `bbuilt`,
   `bdead`, `buildprogress`, **`uniqrnd`**.
3. Клиент в `_misc_ReadSyncClient` пересоздаёт недостающие объекты или
   восстанавливает состояние существующих [^13].

Это «hard reset» — дорогая операция, не используется в нормальном тике,
только при потере консистентности.

---

## 3. Почему поведение расходится даже при синхронизации

Главный вопрос: «adaptive speed синхронизируется на всех, почему всё
равно расходится?». Здесь полный список причин.

### 3.1 Real-time-driven sync конфликтует с game-time-driven логикой

Sync-пакеты идут в **real time** (см. §2.2). Гейм-логика тикает в
**game time** (см. [ticks_and_subticks.md](ticks_and_subticks.md) §1).
Когда сервер меняет `TimeSpeedFactor`:

1. На сервере `gametime` теперь идёт быстрее/медленнее.
2. `WriteRes` продолжает слать каждые 0.1 real-sec.
3. Между двумя `WriteRes` на сервере накопилось `0.1 × speedfactor/10`
   game-time добычи.
4. Клиент применяет полученные значения через 0.1 real-sec.

**Но клиент в это время тоже тикает свой progress-loop**:
`_res_ProcessEconomy(deltatime)` запускается у клиента из той же общей
точки прогресса. У клиента `deltatime` считается как
`GetGameTime - lastprogresstime`, и `GetGameTime` идёт со скоростью,
заданной последним полученным `gc_LAN_GAME_SYNC_GAMETIME`.

**Проблема:** между моментом когда сервер меняет скорость и моментом
когда клиент получает пакет, проходит сетевой лаг (~5-100 мс). В этом
окне:
- Сервер уже ушёл вперёд по game-time с новой скоростью.
- Клиент всё ещё тикает со старой скоростью.
- После прихода `SYNC_GAMETIME` клиент должен **скачком** догнать
  game-time сервера, либо — что вероятно — просто принять новый speed
  и продолжить со своей текущей gametime.

Различие в gametime между сервером и клиентом → разные `deltatime`
приходятся на разные мини-фазы → клиентский показ ресурсов может
отображать «фантомное» значение.

В нашей конкретной задаче это не главное (если бы добыча на сервере
была воспроизводима, клиент-расхождения не имели бы значения для
геймплея). Но это объясняет почему «разные хосты видят разное» — у них
разный effective game-time прошёл за равное real-time из-за лагов
sync-пакетов.

### 3.2 Adaptive speed основан на **локальных** perf-метриках сервера

Сервер усредняет **свой собственный** `GetPerfRender` (рендер FPS) и
`garrfloat_perf_progress` (sim FPS) по окнам 16 и
`gc_perf_progresshistory` кадров соответственно [^14]. Эти метрики
**локальные** и зависят от состояния процесса в моменте: фоновые задачи
Windows, обновление антивируса, GPU-спайки и так далее.

То есть:
- Сервер A в момент T₁ имеет realfps=30 → speed остаётся максимальным.
- Сервер B в тот же момент T₁ имеет realfps=18 → speed снижен до
  8/14 = ~57%.
- При **одинаковом сейве** на A и B за 5 real-min прошло разное
  game-time.

Разный game-time → разное число добычных циклов → разные суммы ресурсов.

### 3.3 Init `random` и `RandomExt` различаются между хостами

C3 при старте новой игры (не Load) вызывает много `random` и
`RandomExt` для:
- `gProgress.last*time := random*X` [^15];
- `obj.uniqrnd := RandomExt` для **каждого** юнита и ресурса [^16];
- `obj.progresstick := floor(RandomExt*32)` [^17];
- `lasttime*` per-unit [^18];
- Init положений деревьев на карте через `RandomExt` [^19].

В multiplayer **только сервер** делает init и шлёт результат через
`WriteNew`/`WriteSyncServer`. Клиенты получают `uniqrnd`, `pos` и
прочее от сервера и применяют. Поэтому в multiplayer init консистентен
между хостами.

В **single-player** на хосте A инициализация даёт одни значения (random
seed = system time на запуске A), на хосте B — другие. Если игрок
копирует один и тот же сейв на оба хоста — Load в save-формате
**должен** содержать `uniqrnd` всех объектов (см.
[determinism_audit.md](determinism_audit.md) §2.1), и они будут
одинаковы. Но **глобальное состояние `random` и фаза adaptive speed
различаются**.

### 3.4 Save/Load: чтобы гарантировать консистентность нужны вещи которых в save нет

Из аудита save format'а ([determinism_audit.md](determinism_audit.md) §2
+ [ticks_and_subticks.md](ticks_and_subticks.md) §6):

**Save содержит:**
- Все per-unit `uniqrnd`, `progresstick`, `lasttime*`, `hp`, pos,
  `statestag`, `sto`.
- `gProgress.lastprogresstime`, `progresstick`, `last*time`.

**Save НЕ содержит:**
- Состояние глобального `random` PRNG cursor.
- Текущую `garrfloat_perf_progress` history (заполняется заново после
  Load).
- Sub-tick фазу анимации крестьянина (ресетится через
  `SwitchTo('Nothing')` в `OnAfterLoad`).
- In-flight pathfinding state.

Когда мы загружаем сейв на одном и том же хосте, второй раз:
1. PRNG `random` стартует с какого-то нового состояния (зависящего от
   истории игры с момента запуска приложения).
2. `garrfloat_perf_progress` пустой → adaptive speed реагирует с другим
   лагом первые секунд 5.
3. Все крестьяне ресетнуты в `'Nothing'` → их следующее действие = новый
   поиск ресурса через `_misc_FindResourceToExtract`
   ([determinism_audit.md](determinism_audit.md) §3.1) → 2 вызова
   `random` дают **разные** результаты потому что глобальный PRNG в
   другом состоянии.

Это и есть финальное объяснение «один сейв, разные запуски — разная
добыча».

### 3.5 Между хостами в single player

Дополнительно к §3.3 и §3.4:
- Floating-point поведение между x87/SSE/FMA может различаться в
  последнем бите. Накапливается за минуты симуляции.
- Adaptive speed на разных хостах рассинхронизирована (§3.2).
- Если игрок не переносит сейв точно (например, выбирает «новая игра»
  с одинаковыми настройками), карта генерится заново с **другим** seed
  → совершенно другие позиции деревьев.

---

## 4. Сводная таблица: что синхронно, что нет

| Состояние | Single-player Load → Load на одном хосте | Multiplayer между хостами | Single-player на двух хостах |
|---|---|---|---|
| Per-unit `uniqrnd` | ✓ персистится в save | ✓ через `WriteNew` | ✓ если одинаковый сейв |
| Per-unit `hp`, pos | ✓ | ✓ через периодический sync | ✓ |
| Per-unit `progresstick` | ✓ | ✓ | ✓ |
| Глобальный `random` cursor | ✗ — divergence after Load | ✓ всё равно не нужен (server-only) | ✗ — divergence |
| `gProgress.last*time` | ✓ | ✓ | ✓ |
| Анимационная фаза | ✗ — ресетится `OnAfterLoad` | n/a — клиенты не симулируют | ✗ |
| In-flight pathfinding | ✗ — теряется | ✗ — но клиент догоняет через `WriteMove` | ✗ |
| Adaptive speed phase | ✗ — perf history пустая | ✗ — server-only решение | ✗ |
| Resource grid order | ✓ персистится с unit list | ✓ | потенциально ✓ если карта одна |
| Position в progress section | ✗ — секция начинается заново | ✗ — но клиенту неважно | ✗ |
| Map gen RNG seed | n/a (карта в save) | ✓ если использовать single seed | ✗ — если новые игры стартуют независимо |

---

## 5. Чем server-authoritative помогает в добыче

В мультиплеере с server-authoritative моделью **поведение крестьянина
определяется целиком сервером**. Клиент видит результат:
- Сервер вызвал `_misc_FindResourceToExtract` с двумя `random` —
  выбрал дерево №142.
- Сервер послал `WriteOrder` или `WriteSearch` клиенту с handle №142.
- Клиент видит крестьянина идущего к дереву №142.

Поэтому **в multiplayer добыча на разных хостах одинакова** — это видит
сервер, остальные — синхронизированный результат.

**Десинк начинается** когда:
- Сетевой лаг приводит к тому, что команда игрока (например, отправить
  крестьянина) приходит на сервер позже чем эстимировано → задержка
  применения.
- Adaptive speed сменился с лагом → клиенты видят дёрганые движения.
- Сетевой пакет потерялся (UDP) → state на клиенте устаревает до
  следующего sync.

В single-player ничего из этого нет — **ваш собственный `bProcess`
всегда true, нет sync-лагов**. Но появляются проблемы 3.4 (save/load).

---

## 6. Импликации для мод-фикса

В контексте **single-player детерминизма** (наша задача):
- Network sync можно игнорировать — `bProcess` всегда true.
- **Нужно решить проблему `random` после Save/Load** (см.
  [determinism_audit.md](determinism_audit.md) §3.1) — убрать `random`
  из hot-path добычи, заменить на детерминированный hash от
  сохранённых полей (`uniqrnd`, `progresstick`, `goHnd`).
- Adaptive speed — отдельная проблема, требует:
  - либо отключения через мод (если есть скриптовый hook на её
    триггер),
  - либо измерения в game-time (см.
    [ticks_and_subticks.md](ticks_and_subticks.md) §9).

В контексте **multiplayer** (если когда-нибудь захочется делать MP мод):
- Не трогать структуру `WriteNew`/`ReadNew` и прочих парных
  обработчиков — там всё работает правильно.
- При патче `_misc_FindResourceToExtract` обязательно учитывать
  `bProcess`. Логика выбора дерева идёт **только** на сервере, поэтому
  новый детерминированный hash должен использовать поля, **которые**
  есть на сервере (`uniqrnd`, `gametime` — оба синкаются).
- Не использовать в hash ничего, что может различаться между сервером
  и клиентом (например, локальный perf history).

Поскольку планируется single-player мод-фикс, эти ограничения
соблюдаются автоматически.

---

## 7. Cross-references

- [determinism_audit.md](determinism_audit.md) §1 описывает `random` vs
  `RandomExt` vs `SetRandomKey`. Этот документ §1.3 объясняет **зачем**
  разработчики разделили эти механизмы (server-authoritative
  architecture).
- [determinism_audit.md](determinism_audit.md) §2 описывает что
  персистится в save format. Этот документ §2.5 показывает что **тот
  же** формат используется для on-demand network resync.
- [ticks_and_subticks.md](ticks_and_subticks.md) §5.2 описывает adaptive
  speed. Этот документ §3.2 объясняет почему adaptive speed не помогает
  консистентности между хостами.
- [ticks_and_subticks.md](ticks_and_subticks.md) §6 описывает save/load
  хуки. Этот документ §3.4 объясняет почему даже эти хуки не
  достаточны.
- [peasant_extraction.md](../world/peasant_extraction.md) — модель
  добычи. **Должен быть обновлён** ссылкой на determinism_audit.md (§3)
  для учёта потерь через RNG.

---

## Источники

Все ссылки относительно `data/scripts/` в установке Cossacks 3.

[^1]: Основной паттерн `bProcess` — пример использования:

    ```pascal
    var bProcess : Boolean = not (_net_IsClient or _net_IsReplay);
    if (bProcess) then
    begin
       // ... уменьшаем HP ресурса
       // ... начисляем ресурс игроку
       // ... вычисляем урон и применяем
    end;
    ```

[^2]: Примеры обработчиков с проверкой `bProcess`:
    `units/unit.inc/onaclanimationreachedwork.inc:8` (добыча ресурса),
    `units/unit.inc/onaclanimationreachedattack.inc:8` (нанесение
    урона), `units/unit.inc/onaclanimationreachedconstruct.inc:8`
    (прогресс строительства), `units/unit.inc/ontagstates.inc:720` и
    другие.

[^3]: Определения `_net_IsOffline`, `_net_IsServer`, `_net_IsClient`,
    `_net_IsRecord`, `_net_IsReplay` — `lib/net.script:39-67`.
    Константы `gc_LAN_GAME_*` — `lib/classes.script:7560-7591`.

[^4]: Сидирование PRNG для дисперсии снаряда —
    `weapon.script:1051`, `unit.script:11453`. Передача `frnd` от
    сервера клиенту — `unit.script:11554`.

[^5]: Авторский комментарий о выборе general random —
    `weapon.script:1011`:

    ```pascal
    // I use general random, cause no need to sync it
    // and randomext may change planned results on dif PCs
    ```

[^6]: Шаблон `WriteNew` — `units/global.inc/writenew.inc:15-71`:

    ```pascal
    if _net_IsServer or _net_IsOffline then begin
       // ... locally create unit ...
       gohnd := CreatePlayerGameObjectHandleByHandle(plhnd, race, base, posx, 0, posz);
    end;

    if _net_IsOnline or _net_IsRecord then begin
       RecordCustomBegin('ReadNew');
       // ... write fields to package ...
       var gouid: Integer;
       if _net_IsServer or _net_IsRecord then
          gouid := GetGameObjectUniqueIdByHandle(gohnd);
       RecordCustomWriteString(race);
       // ...
       RecordCustomEnd;
    end;
    ```

[^7]: Periodic-таймеры в главном цикле прогресса —
    `progress/progress.inc/nothing.inc:697-713`:

    ```pascal
    var curtime : Float = GetCurrentTime;   // <-- REAL TIME, не game time!
    if (curtime - gfloat_lan_lastsyncrestime) > 0.1 then
    begin
       gfloat_lan_lastsyncrestime := curtime;
       ExecuteState('WriteRes');
    end;
    if (curtime - gfloat_lan_lastsyncstatstime) > 20 then
    begin
       gfloat_lan_lastsyncstatstime := curtime;
       ExecuteState('WriteStats');
    end;
    if (curtime - gfloat_lan_lastsyncdatatime) > 0.1 then
    begin
       gfloat_lan_lastsyncdatatime := curtime;
       gbool_net_forcesyncdata := true;
       ExecuteState('WriteLanSyncData');
    end;
    ```

[^8]: Тригер `_misc_SyncUnitsParams` по mod 53 —
    `progress/progress.inc/nothing.inc:405-406`:

    ```pascal
    if ((gProgress.progresstick mod 53)=0) and (gLanSyncUnitsParamsUIDList.GetCount>0) and ((_net_IsOnline and _net_IsServer) or (_net_IsRecord)) then
       _misc_SyncUnitsParams;
    ```

[^9]: Реализация `_misc_SyncUnitsParams` —
    `miscext2.script:4301-4338`.

[^10]: Отправка пакета синхронизации gameTime/speed —
    `progress/progress.inc/nothing.inc:617-622`:

    ```pascal
    SetTimeSpeedFactor(newspeed);
    var pLan : Integer = _parser_ParserTemporary(True);
    ParserSetFloatValueByKeyByHandle(pLan, 't', GetGameTime);
    ParserSetFloatValueByKeyByHandle(pLan, 's', newspeed);
    LanSendParser(gc_LAN_GAME_SYNC_GAMETIME, pLan);
    ```

[^11]: `_misc_WriteSyncClient` (запрос на ресинк) —
    `miscext2.script:3955-3963`.

[^12]: `_misc_WriteSyncServer` (полное состояние всех юнитов) —
    `miscext2.script:3965-4072`.

[^13]: `_misc_ReadSyncClient` — `miscext2.script:4083+`.

[^14]: Локальные perf-метрики adaptive speed —
    `progress/progress.inc/nothing.inc:563-578`:

    ```pascal
    var pr, pp : Float;
    const cCheckFrames = 16;
    for i:=0 to cCheckFrames-1 do
       pr := pr+GetPerfRender(i);
    pr := (pr/cCheckFrames);

    var progfps : Float;
    for i:=0 to gc_perf_progresshistory-1 do
       progfps := progfps+garrfloat_perf_progress[i];
    progfps := progfps/gc_perf_progresshistory;
    ```

[^15]: Init `gProgress.last*time` через `random` —
    `miscext.script:1891-1898`.

[^16]: `obj.uniqrnd := RandomExt` для каждого юнита/ресурса —
    `unit.script:2726`.

[^17]: Init `obj.progresstick := floor(RandomExt*32)` —
    `unit.script:2707`.

[^18]: Per-unit `lasttime*` инициализация — `miscext.script:2757-2762`.

[^19]: Init положений деревьев через `RandomExt` —
    `misc.script:3714-3715`, `misc.script:3906-3907`.
