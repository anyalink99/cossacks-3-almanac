# Recon: детерминизм добычи и боя (RNG audit)

Все источники недетерминизма в горячем пути добычи и боя: где RNG в
скриптах (можно модифицировать), а где в движке (нельзя). Нужно для
оценки разброса в симуляторе и для потенциального мод-фикса. Все
ссылки на код и сами Pascal-блоки собраны в разделе
[Источники](#источники) в конце документа.

**Связанные документы:**

- [ticks_and_subticks.md](ticks_and_subticks.md) — модель времени,
  sub-tick state, адаптивная скорость.
- [server_sync_architecture.md](server_sync_architecture.md) —
  server-authoritative архитектура C3, net modes, почему `random`
  допустим в server-only-логике.

**Эмпирический контекст (наблюдения игрока):**

- Загрузка одного и того же сейва с фиксированной расстановкой крестьян
  → за равный интервал реального времени добыча ресурсов **различается
  между запусками** (один и тот же хост).
- Между разными хостами расхождение ещё больше.
- **Шахты — стабильны** между запусками, их поведение полностью
  воспроизводимо.

Все пути к скриптам ниже — относительно `data/` в установке Cossacks 3.

---

## 1. Как устроен RNG в DMscript

Скриптовая среда экспонирует два основных источника случайности и одну функцию контроля:

| Идентификатор | Что делает | Где определён |
|---|---|---|
| `random` | Float ∈ [0,1) из глобального PRNG | engine builtin |
| `RandomExt` | Float ∈ [0,1) из «расширенного» PRNG | engine builtin |
| `SetRandomKey(seed : Integer)` | Перезасев глобального PRNG | engine builtin |

**Ключевая семантика:** оба генератора **глобальные**, но используются по-разному:

- `random` — расходный поток, состояние которого продвигается каждым вызовом и не реинициализируется между ними.
- `RandomExt` — используется явно после `SetRandomKey(...)` для получения **детерминированной от seed** последовательности.

В коде есть осознанный паттерн: перед серией вызовов `RandomExt` ставится
`SetRandomKey(floor(uniqrnd × gc_MaxInt))`, после чего последовательность
становится воспроизводимой при одном и том же `uniqrnd` [^1].

Авторские комментарии прямо это подтверждают: один помечен как
`sync multiplayer` (там `RandomExt` нужен синхронным между хостами) [^2],
другой — `I use general random, cause no need to sync it and randomext
may change planned results on dif PCs` [^3]. То есть `random` и
`RandomExt` различаются по гарантиям межхостовой синхронизации.

**Вывод 1.** Паттерн осознанный: `random` — одноразовый, `RandomExt` —
синхронизируемый через явный seed. Использование `random` без
предварительного `SetRandomKey` создаёт зависимость от истории
глобального состояния PRNG.

---

## 2. Что переживает Save/Load

### 2.1 `uniqrnd` — детерминированный per-unit nonce

Каждый юнит получает `uniqrnd : Float ∈ [0,1)` при создании [^4], и
**этот float явно сериализуется** в network sync / save: отдельно
запись [^5] и чтение [^6].

Также сохраняется `progresstick : Integer = floor(RandomExt × 32)` [^7]
и ряд per-unit float-полей — `lasttimecheckcapture`, `lasttimeidlegrid`,
`lasttimescangrid`, `lasttimetopology`, `lasttimebestposition`,
`lastsearchenemy` [^8]. Все они инициализируются через `random` один раз
при старте и потом сохраняются как обычное состояние.

### 2.2 OnBeforeSave / OnAfterLoad

Движок экспонирует хуки сохранения и загрузки в скрипты. Для крестьянина
`OnBeforeSave` вызывает `SwitchTo('Nothing')` [^9], а `OnAfterLoad` —
для water-юнитов воссоздаёт ship childs, для всех — снова
`SwitchTo('Nothing')` [^10]. Для ресурса `OnAfterLoad` исполняет
`Initial`-state и переходит в `'Nothing'` [^11].

**Вывод 2.** Разработчики **знают про нестабильность sub-tick state** и
принудительно ресетят state machine крестьянина в `'Nothing'` и при
сохранении, и при загрузке. Это нормализует фазу анимации и текущий
action, но **не нормализует**: позицию (sub-cell), цель (sto handle),
направление и состояние глобального PRNG.

### 2.3 Что не сохраняется (или ресетится)

- Глобальное состояние `random` (явно нет в save format'е унитов; вероятно reseeded на load или совсем не сохраняется).
- Текущая фаза work-цикла анимации (ресетится через `SwitchTo('Nothing')`).
- In-flight pathfinding state (waypoint queue, partial step interpolation) — почти точно ресетится.

---

## 3. RNG в добыче

### 3.1 Site map (полный)

Все вызовы `random` в hot path добычи ресурсов:

| Что выбирается | Влияние | Уровень |
|---|---|---|
| `rndind := floor(random × count)` — стартовый индекс при сканировании выбранной ячейки `gResGrid` в `_misc_FindResourceToExtract` [^12] | **Какое дерево/камень** выберет крестьянин в найденной ячейке | script |
| `if (random < (testW / (testW + testS)))` — выбор wood vs stone когда `filterres = none` [^13] | **Какой ресурс** добывает (только при auto-выборе типа) | script |
| `if (random < waitrnd)` в `_unit_SearchResourceInRadius` — гейт по standtime [^14] | **Запустится ли поиск** на этом тике (если standtime > 0.1) | script |
| `bskipcheck := (random > 0.75)` [^15] | **Пропустить ли часть проверок** при выборе цели | script |
| `rndind := floor(random × count)` — стартовый индекс в `gIntegerList` [^16] | **Какой кандидат** выбирается среди равно подходящих ресурсов в радиусе | script |
| `rmax := gc_obj_extract_food_radiusmaxSqr × random` (только food, при move_walk) [^17] | **Радиус вокруг поля**, в котором считается «можно бить» | script |
| `if (TObj(pobj).standtime >= 9) or (random > 0.9)` [^18] | **Срабатывание расширенного поиска** соседнего ресурса | script |

Также внутри `_unit_SearchResourceInRadius` есть ещё несколько
`floor(random × count)` для других case-ов поиска [^19].

### 3.2 Алгоритм поиска (по `_misc_FindResourceToExtract`)

Логика [^20]:

1. Перебор всех ячеек `gResGrid[i,j]` (детерминированный обход — порядок ячеек фиксирован).
2. Для каждой считается `reldst = (2 + dst) / (1 + (freewood + freestone/2)/40)` — детерминированная метрика «выгодности».
3. Запоминается ячейка с минимальным `reldst` (`mingridx`, `mingridy`).
4. **Внутри найденной ячейки** выбирается стартовый индекс `rndind := floor(random × count)`, и от него линейный поиск.
5. Если `filterres = none`, выбор wood/stone делается через `if (random < (testW / (testW + testS)))`.

**Шаги 1-3 полностью детерминированы**. Шаги 4-5 — два вызова `random`.
Это объясняет, почему между запусками одного и того же сейва крестьяне
начинают выбирать разные деревья/камни внутри одной зоны.

### 3.3 Цепная реакция

Малое HP единичного дерева (8000-16000 для пня, при `gc_resource_type_wood`
HP уменьшается на 1 за удар) и частые походы на склад создают **много
точек принятия решений** за минуту реального времени. Каждая точка —
точка ветвления через `random`. Это и есть механизм накопления
дисперсии.

---

## 4. RNG в бою

### 4.1 Site map

| Что выбирается | Сидируется uniqrnd? | Уровень |
|---|---|---|
| `bHeadShot := bCanHeadShot and (random < 0.05) and (not bFastHorseBullet)` [^21] | **Нет** — raw `random` | script |
| `damage := damage + floor(TObj(pobj).uniqrnd × 500)` (бонус хедшота) [^22] | **Да** — фиксированный per-unit | детерминирован |
| `SetRandomKey(floor(TObj(pobj).uniqrnd × gc_MaxInt))` перед спавном debris при разрушении здания [^23] | **Да, явно сидируется** | детерминирован |
| `SetRandomKey(floor(random × gc_MaxInt))` перед сетевой синхронизацией снаряда [^24] | **Нет** — `random` для сидирования | script |
| `(random < 0.05)` — kill-check (вероятно для NPC env) [^25] | **Нет** | script |
| `SetGameObjectIntervalFactorByHandle(hnd, 0.7 + random × 0.6)` — десинхронизация анимации смерти **намеренно** [^26] | Нет | визуал, не геймплей |
| `GameObjectRollByHandle(hnd, -cDeathRollAngle + random × cDeathRollAngle × 2)` — угол падения трупа [^27] | Нет | визуал |
| `SetRandomKey(floor(newuniqrnd × gc_MaxInt))` для расчёта траектории снаряда [^1] | **Да** | детерминирован |

### 4.2 Урон

Базовый урон считается полностью детерминированно:
`damage = weapon.damage + squad.bonus - target.protection[weapkind]`.

Хедшот:

- Срабатывание: `bHeadShot = (random < 0.05)` — **источник дисперсии**.
- Бонус если сработал: `+ floor(uniqrnd × 500)` — **детерминирован**
  (`uniqrnd` персистится).

То есть **в ~95% выстрелов урон полностью детерминирован**. В ~5%
урон деваривируется через срабатывание хедшота, которое зависит от
глобального состояния `random` на момент выстрела.

### 4.3 Снаряды и дисперсия

Паттерн `_unit_DoProjectile` устроен так: сначала глобальный PRNG
сидируется текущим значением `random`, дальше идёт расчёт дисперсии
через `RandomExt` (теперь воспроизводимый от seed), и в конце seed
сохраняется в `TPlayerArgs(parg).frnd` для серверной репликации [^28].

Это **полу-детерминированный** паттерн: сам seed (`random`) случаен,
но после установки seed дальнейшие вычисления воспроизводимы. Между
хостами **состояние `random` синхронизировано** через lockstep, поэтому
все хосты получают одинаковый seed → одинаковые `RandomExt` →
одинаковую дисперсию выстрела.

**Однако** этот же паттерн объясняет, почему `random` критичен для
синка: если на одном из хостов глобальный PRNG продвинулся на лишний
вызов из-за какого-то скрипта, *весь последующий бой* получит другие
seed-ы.

### 4.4 Что детерминировано в бою

- Урон без хедшота (95% случаев)
- Бонус хедшота (через `uniqrnd`)
- Дисперсия снаряда (через `SetRandomKey + RandomExt`)
- Время полёта снаряда, упреждение, попадание/промах в общем виде
- Анимации помечены авторским комментарием
  `units die at different animation speed, to desyncronise visual part` [^26] —
  это намеренный десинк только визуала.

**Вывод 3.** Бой намного более детерминирован, чем добыча. Главный
источник дисперсии — 5%-е срабатывание хедшота на raw `random`.
Остальные `random` в боевом коде — визуальные.

---

## 5. RNG в init и AI

Для полноты картины:

| Что | Когда |
|---|---|
| `obj.progresstick := floor(RandomExt × 32)` — фаза unit progress тика [^7] | init-only, **сохраняется как state** |
| `obj.uniqrnd := RandomExt` — per-unit nonce [^4] | init-only, **сохраняется** |
| Init `gProgress.last*time` через `random` — глобальные таймеры [^29] | init-only |
| Per-unit `lasttime*` через `random` [^8] | init-only, потом сохраняется |
| AI decisions через `RandomExt < _misc_RandToRandom(N)` [^30] | каждый тик AI, влияет на поведение AI игрока |
| `SetRandomKey(floor(random × gc_MaxInt))` — синхронизация для какого-то процесса [^31] | hot-path |

AI сильно зависит от `random` и `RandomExt`. Это объясняет, почему
игры с AI ещё менее детерминированы, чем PvP.

---

## 6. Почему шахты воспроизводимы

Проверяем гипотезу из эмпирики игрока. Шахта — это unit с
`produce[gc_resource_type_*]`. Доход реализован в
`_player_ProcessResourceIncome` (см.
[peasant_extraction.md](../../docs/recon/world/economy/peasant_extraction.md)).

В hot-path шахты **нет вызовов** `random`:

- Крестьянин входит в шахту → `_unit_AddInside` → state «inside»
- Доход = `produce_rate × N_workers × dt` — чистая арифметика
- Нет поиска цели, нет pathfinding, нет очереди (слоты фиксированы)

Это идеально согласуется с эмпирикой: шахты дают одинаковый результат
в каждом запуске.

---

## 7. Механизм недетерминизма (синтез)

> Для понимания tick-loop-а, sub-tick state и adaptive game speed см.
> [ticks_and_subticks.md](ticks_and_subticks.md). Здесь даём короткую
> сводку с фокусом на RNG.

### 7.1 Один хост, разные запуски одного сейва

Сценарий: загружаем сейв с 10 крестьянами на лесу, ждём 5 мин real-time,
считаем дерево.

**Что одинаково после Load:**

- Позиции крестьян и складов (целочисленные/тайловые компоненты — точно; sub-cell — вероятно, сохранено как float).
- `uniqrnd` каждого крестьянина (явно персистится).
- HP всех деревьев и полей.
- Текущая цель (`sto`) каждого крестьянина — handle ресурса.
- `progresstick`, все `lasttime*` — персистятся.

**Что различается:**

1. **Глобальное состояние PRNG** (`random`-курсор) — почти точно НЕ сохраняется в save format'е и инициализируется по системному времени старта или иным образом, который варьирует от запуска к запуску.
2. Состояние state machine крестьянина — принудительно ресетится в `'Nothing'` (см. §2.2), но это значит, что после Load крестьяне **заново ищут цель** через `_misc_FindResourceToExtract` / `_unit_SearchResourceInRadius`, попадая в RNG-зависимые шаги §3.1.
3. In-flight pathfinding state — теряется при `SwitchTo('Nothing')`.

**Каскад:** Load → ресет state в `Nothing` → каждый крестьянин заново
зовёт поиск → 5 вызовов `random` на каждом крестьянине влияют на выбор
стартового индекса в resgrid → разные деревья → разные пути → разные
времена прибытия → разные конкуренции за ресурс → дальше обратной связи
нет, но есть множитель: каждый Save/Load умножает дисперсию.

### 7.2 Между хостами

Помимо §7.1, добавляются:

- **Floating-point** различия (особенно если CPU поддерживает разные расширения).
- Возможный рассинхрон lockstep-а при single-player save (он не сетевой и не обязан быть строго детерминированным).
- Различный init seed `gProgress.last*time` — он выполняется один раз при старте, у каждого хоста свой `random` [^29].

### 7.3 Ранг источников по влиянию

Для добычи в порядке убывания вклада в дисперсию (по hot-path частоте):

1. **Случайные выборы внутри `_misc_FindResourceToExtract`** [^12][^13] — вызывается каждый раз, когда крестьянин возвращает ресурс на склад и ищет следующий.
2. **Случайные выборы в `_unit_SearchResourceInRadius`** [^14][^15][^16] — повторный поиск при потере цели.
3. **Pathfinding tie-breaking** (engine, недоступно скрипту) — когда несколько путей одинаковой длины, выбор зависит от внутреннего порядка обхода графа.
4. **Sub-tick state не нормализуется на Save/Load** (engine, частично смягчено через `SwitchTo('Nothing')`).
5. **Variable timestep** (engine, если есть).

---

## 8. Что детерминировано by-design

- **Шахты**: чистая арифметика тика, без RNG.
- **Per-unit характеристики**: `uniqrnd`, `progresstick`, все `lasttime*` — персистятся.
- **Урон без хедшота** (95% боевых случаев).
- **Дисперсия снарядов** (через `SetRandomKey + RandomExt` от per-unit nonce).
- **Бонус хедшота** (через `uniqrnd`).
- **Метрика выгодности ячейки `gResGrid`** (`reldst` в `_misc_FindResourceToExtract` — чистая функция координат и счётчиков).
- **Расчёт урона в `OnAclAnimationReachedWork`** [^32] — полностью детерминирован, нет `random`.

---

## 9. Что в движке (вне досягаемости скрипта)

- **Save/load format** — какие поля `TObj` сохраняются, какие нет (но точно сохраняется список из network sync: `pos`, `dir`, `statestag`, `sto`, `hp`, `uniqrnd` [^33]). Можно частично смягчить через `OnBeforeSave` (как уже делает `SwitchTo('Nothing')`).
- **Pathfinding** и его tie-breaking при равных дистанциях.
- **Resource grid iteration** — порядок объектов в `gResGrid[i,j]` зависит от истории вставок/удалений в массив, что в свою очередь зависит от истории спавна и убийства ресурсов.
- **Variable logical tick** — `deltatime` зависит от FPS, см. [ticks_and_subticks.md](ticks_and_subticks.md) §5.
- **Adaptive game speed** — engine динамически снижает `TimeSpeedFactor` под нагрузкой, см. [ticks_and_subticks.md](ticks_and_subticks.md) §5.2. Это **главный** источник межхостового рассинхрона в single player.
- **Floating-point точность между разными CPU**.
- **Устройство глобального `random`** — алгоритм PRNG, начальный seed.

---

## 10. Импликации для модели добычи

Из этого аудита вытекают конкретные допущения для модели:

1. **Аналитический потолок** (best-case rate с идеальным распределением) — считаем строго детерминированно по формулам из [`peasant_extraction.md`](../../docs/recon/world/economy/peasant_extraction.md). RNG не учитываем. Время — в **game-time**, не real-time (см. [ticks_and_subticks.md](ticks_and_subticks.md) §1, 9).

2. **Реальная добыча в игре** = `theoretical × (1 - loss_factor)`, где `loss_factor` — эмпирически калибруемый коэффициент потерь от:
   - Конкуренции за дерево (несколько крестьян на одно дерево).
   - Pathfinding overhead (выбор не оптимального дерева).
   - Микро-задержек поиска цели после возврата на склад.

3. **Ожидаемый разброс между запусками одного сейва** (gut-feel прогноз до эмпирического замера): σ/μ ≈ 5-15% на 5-минутном окне для леса/камня. Для шахт σ/μ ≈ 0.

4. **Валидация модели**: запускать сейв ≥ 3 раз, брать среднее, не один прогон.

5. **Калибровка `loss_factor`**: можно потенциально приближать через мод-фикс RNG (см. §11), который должен значительно сжать дисперсию и приблизить к теоретическому потолку.

---

## 11. Указатель на потенциальный мод-фикс

Полная картина того, **что моддится**:

- `_misc_FindResourceToExtract` [^20] — переписать `random` → детерминированный hash от `uniqrnd + GetGameTime + goHnd`.
- `_unit_SearchResourceInRadius` [^34] — то же.
- 7 RNG-сайтов в добыче (см. §3.1) — все script-level.
- Срабатывание хедшота [^21] — опционально, для полной детерминированности боя.

**Что НЕ починить модом:**

- Pathfinding tie-breaking.
- Расширение save-формата (нужен DLL injection или hex-патч exe).
- Порядок обхода в `gResGrid` (порядок вставок).
- Межзапусковая стабильность глобального состояния PRNG (нужно патчить инициализацию движка).

**Деплой:** через мод-систему игры (`mods/<modname>/data/scripts/lib/...`
оверрайдит файлы из игры). Mod manager — `modman.exe`, конфиг —
`mods/mods.ini`. Существующие воркшоп-моды (например, `1585067167` —
Back to War OST) подтверждают этот формат.

**Минус:** оверрайд по целым файлам (не по функциям) — приходится
копировать `misc.script` (256 КБ) и `unit.script` (560 КБ) полностью и
поддерживать diff после игровых патчей.

**Тест-протокол:** сейв с фиксированной расстановкой → 5 запусков без
мода (записать σ/μ) → 5 запусков с модом → сравнение. Если σ/μ упало
с > 5% до < 2% — RNG-источники доминировали и фикс работает. Если
осталось ≈ 5% — доминируют движковые источники (pathfinding,
sub-tick state).

См. отдельный документ по мод-плану (TBD).

---

## Источники

Все ссылки относительно `data/scripts/` в установке Cossacks 3.

[^1]: Сидирование PRNG значением `uniqrnd` для расчёта траектории снаряда — `lib/weapon.script:1051`:

    ```pascal
    SetRandomKey(floor(newuniqrnd * gc_MaxInt)); // sync multiplayer
    ```

[^2]: Авторский комментарий «sync multiplayer» (там же) — `lib/weapon.script:1051`.

[^3]: Авторский комментарий о различии `random` и `RandomExt` — `lib/weapon.script:1011`:

    ```pascal
    // I use general random, cause no need to sync it and randomext may change planned results on dif PCs
    ```

[^4]: Инициализация `obj.uniqrnd := RandomExt` — `lib/unit.script:2726`.

[^5]: Запись `uniqrnd` в network sync — `lib/miscext2.script:4027`:

    ```pascal
    ParserSetFloatValueByKeyByHandle(pSync, 'uniqrnd', uniqrnd);
    ```

[^6]: Чтение `uniqrnd` из network sync — `lib/miscext2.script:4120, 4152`:

    ```pascal
    TObj(pobj).uniqrnd := uniqrnd;
    ```

[^7]: Инициализация `obj.progresstick := floor(RandomExt * 32)` — `lib/unit.script:2707`.

[^8]: Per-unit `lasttime*` поля (`lasttimecheckcapture`, `lasttimeidlegrid`, `lasttimescangrid`, `lasttimetopology`, `lasttimebestposition`, `lastsearchenemy`) — `lib/miscext.script:2757-2762`.

[^9]: `OnBeforeSave` для крестьянина — `units/unit.inc/onbeforesave.inc`:

    ```pascal
    SwitchTo('Nothing');
    ```

[^10]: `OnAfterLoad` для крестьянина (water-юниты пересобирают ship childs, остальные — `SwitchTo('Nothing')`) — `units/unit.inc/onafterload.inc`.

[^11]: `OnAfterLoad` для ресурса — `env/env.inc/onafterload.inc`:

    ```pascal
    ExecuteState('Initial');
    SwitchTo('Nothing');
    ```

[^12]: Стартовый индекс при сканировании ячейки `gResGrid` в `_misc_FindResourceToExtract` — `lib/misc.script:2790`:

    ```pascal
    rndind := floor(random * count);
    ```

[^13]: Выбор wood vs stone, когда `filterres = none` — `lib/misc.script:2801`:

    ```pascal
    if (random < (testW / (testW + testS))) then ...
    ```

[^14]: Гейт по standtime в `_unit_SearchResourceInRadius` — `lib/unit.script:4055`:

    ```pascal
    if (random < waitrnd) then ...
    ```

[^15]: Пропуск части проверок при выборе цели — `lib/unit.script:4114`:

    ```pascal
    bskipcheck := (random > 0.75);
    ```

[^16]: Стартовый индекс в `gIntegerList` для выбора кандидата среди подходящих ресурсов — `lib/unit.script:4120`:

    ```pascal
    rndind := floor(random * count);
    ```

[^17]: Радиус вокруг поля для food-добычи при `move_walk` — `lib/unit.script:9790`:

    ```pascal
    rmax := gc_obj_extract_food_radiusmaxSqr * random;
    ```

[^18]: Срабатывание расширенного поиска соседнего ресурса — `lib/unit.script:9822`:

    ```pascal
    if (TObj(pobj).standtime >= 9) or (random > 0.9) then ...
    ```

[^19]: Дополнительные `floor(random * count)` в `_unit_SearchResourceInRadius` для других case-ов поиска — `lib/unit.script:4623, 4647, 4674, 4796, 4872`.

[^20]: Тело `_misc_FindResourceToExtract` — `lib/misc.script:2730-2823`.

[^21]: Срабатывание хедшота — `lib/miscext2.script:420`:

    ```pascal
    bHeadShot := bCanHeadShot and (random < 0.05) and (not bFastHorseBullet);
    ```

[^22]: Бонус урона при хедшоте — `lib/miscext2.script:437`:

    ```pascal
    damage := damage + floor(TObj(pobj).uniqrnd * 500);
    ```

[^23]: Сидирование PRNG значением `uniqrnd` перед спавном debris при разрушении здания — `lib/unit.script:11453`:

    ```pascal
    SetRandomKey(floor(TObj(pobj).uniqrnd * gc_MaxInt));
    ```

[^24]: Сидирование PRNG значением `random` перед сетевой синхронизацией снаряда — `lib/unit.script:11528`:

    ```pascal
    SetRandomKey(floor(random * gc_MaxInt)); // needed to sync multiplayer arg.frnd
    ```

[^25]: Kill-check для NPC env — `lib/unit.script:7289`:

    ```pascal
    if (random < 0.05) then ...
    ```

[^26]: Намеренная десинхронизация скорости анимации смерти — `lib/unit.script:11103`:

    ```pascal
    SetGameObjectIntervalFactorByHandle(hnd, 0.7 + random * 0.6);
    // units die at different animation speed, to desyncronise visual part
    ```

[^27]: Угол падения трупа — `lib/unit.script:10824`:

    ```pascal
    GameObjectRollByHandle(hnd, -cDeathRollAngle + random * cDeathRollAngle * 2);
    ```

[^28]: Тело `_unit_DoProjectile` (сидирование `random` → расчёт `RandomExt` → сохранение seed в `frnd`) — `lib/unit.script:11518-11554`:

    ```pascal
    SetRandomKey(floor(random * gc_MaxInt)); // line 11528 — сидируем PRNG значением random
    if (disp > 0) then
       _weapon_CalcShotDispertion(...);   // использует RandomExt, теперь воспроизводимый от seed
    TPlayerArgs(parg).frnd := RandomExt; // line 11554 — сохраняем seed для серверной репликации
    ```

[^29]: Init глобальных таймеров `gProgress.last*time` через `random` — `lib/miscext.script:1891-1898`.

[^30]: AI decisions через `RandomExt < _misc_RandToRandom(N)` — `lib/unit.script:3644-3665`.

[^31]: `SetRandomKey(floor(random * gc_MaxInt))` для синхронизации — `lib/unit.script:5301`.

[^32]: Детерминированный расчёт урона на удар — `units/unit.inc/onaclanimationreachedwork.inc`.

[^33]: Список полей `TObj`, гарантированно сохраняемых в network sync (`pos`, `dir`, `statestag`, `sto`, `hp`, `uniqrnd`) — `lib/miscext2.script:4002-4027`.

[^34]: Тело `_unit_SearchResourceInRadius` — `lib/unit.script:4043+`.
