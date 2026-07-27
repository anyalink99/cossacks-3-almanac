# Технический разбор поиска пути и движения

[← Скрипты и сценарии](structure.md)

[Читательская статья о движении юнитов](../../docs/recon/world/combat/pathfinding.md)

Как юниты выбирают маршрут, обходят соседей и препятствия, двигаются строем
и реагируют на блокировку пути. Точное устройство нативного алгоритма
неизвестно, поэтому статья отделяет наблюдаемое игровое поведение от
[технических подробностей](#technical-details).

**Подробнее по связанным темам:**

- [Игровые такты](../engine/ticks_and_subticks.md) —
  частота основных расчётов.
- [Синхронизация сервера](../engine/server_sync_architecture.md) —
  передача приказов между сервером и клиентами.
- [Механика зданий](../../docs/recon/world/economy/building_mechanics.md) — занимаемая площадь
  зданий.

## Коротко

- Сначала игра строит маршрут до цели по карте препятствий, затем каждый
  кадр локально раздвигает соседние объекты.
- Запросы маршрута объединяются в пакет и обрабатываются раз в 20 мс.
- Карта столкновений имеет шаг 0,5 клетки.
- **Расталкивание союзников** проходит без события: свои отряды раздвигают друг друга,
  без анимации.
- **Враг в 90° спереди** — юнит автоматически переключается на атаку,
  даже если шёл на другую цель.
- **Построение** задаёт каждому юниту собственную цель с небольшим
  случайным смещением, а не заставляет всех следовать за командиром.
  Поэтому отряд в движении слегка расплывается.
- Если маршрут не найден, юнит останавливается. Отдельного телепорта или
  универсального тайм-аута застревания нет.

## Как движение выглядит для игрока

### Маршрут и препятствия

Приказ движения задаёт конечную точку, а игра возвращает юниту цепочку
промежуточных точек. Юнит может пропускать лишние изгибы, если следующий
участок просматривается по прямой. Сухопутные и водные маршруты считаются
отдельно; наземные запросы получают больший приоритет.

Если путь не найден, юнит останавливается. Повторный расчёт происходит при
новом приказе движения, при смене цели или после специальной попытки выйти
из плотной толпы. Постоянного пересчёта на каждом кадре нет.

### Обход соседей

На готовый маршрут накладывается локальное расталкивание:

- союзники мягко раздвигают друг друга без отдельной реакции;
- противник в переднем секторе 90° может заставить юнита перейти к атаке;
- здания остаются неподвижными, а юнит обтекает их;
- корабли значительно тяжелее сухопутных юнитов и сильнее расталкивают
  соседей.

### Что происходит в толпе

Если рядом больше трёх стоящих объектов и как минимум четверо из них не
двигаются уже три игровые секунды, юнит примерно раз в 3,075 игровой
секунды ищет свободное место по спирали в радиусе шести ячеек. Это помогает
рассасывать плотную толпу, но не гарантирует выход из любого тупика.

### Движение построения

Построение не имеет одного пути, которому слепо следует весь отряд. Игра
вычисляет место каждого бойца в сетке, добавляет небольшое случайное
смещение и отдаёт каждому отдельный приказ движения. Поэтому широкий строй
может растягиваться в проходе и собираться заново после остановки.

### Нагрузка при массовом приказе

Скриптового предела длины очереди маршрутов не найдено. Все юниты,
запросившие путь за один такт, передаются нативному движку одним пакетом.
Это хорошо для массовых приказов, но фактический предел производительности
зависит от скрытой реализации движка.

---

<a id="technical-details"></a>
## Технические подробности

### Архитектура: две независимые подсистемы

Движок разделяет навигацию юнита на две слабо связанные подсистемы:

| Подсистема | Что делает | Где живёт |
|---|---|---|
| **Топология и карта препятствий** (`Topology`, `QuadTree`) | Глобальный поиск пути A → B через зоны проходимости; возвращает массив маршрутных точек (`TrackPoint`). | Нативные функции `Topology*` / `TraceLine*`. |
| **Предотвращение столкновений** (`CollisionInertia`, сокращённо `CI`) | Каждый кадр помогает обходить и расталкивать соседей вдоль уже проложенного пути с учётом массы и инерции. | Нативные функции `*CI*`. |

Скрипты обращаются к обеим через `Set / Get*ByHandle` — **детали
реализации в нативном коде, скриптам не видны**.

Точка входа в скрипты: `_init_InitializeTopology` [^1]. Внутри задаются
ключевые константы топологии: `gc_top_TopologyPriority = 90`,
`gc_top_PathPriority = 70`, `gc_top_WallPriority = 95`,
`gc_top_EffectDist = 3` и др. [^2]

Это мир столкновений на основе `QuadTree` с двумя слоями приоритета:
первый включает все статические препятствия, второй — только рельеф и стены.
У запросов «юнит идёт через здание» приоритет ниже, чтобы поиск пути
мог найти путь «как будто здания нет».

---

### Где и как рассчитывается путь

#### Очередь и пакетная обработка

**Очередь:** два глобальных списка в `_unit_PathListAdd` [^3]. Юнит
добавляется в `gGOPathList` (земля) или `gWaterPathList` (вода) **ровно
один раз** при переходе в состояние `gc_statetag_execute_move` [^4].
Флаг `bpathrequested : Boolean` защищает от дублирования [^5].

**Списки сохраняются** в сохранениях и реплеях [^6] — это часть
состояния мира.

#### Главный пакет запросов (раз в 20 мс)

Вся пакетная обработка пути находится в
`progress/progress.inc/nothing.inc` [^7].
Ключевые шаги:

1. Выбирается одна очередь — `gWaterPathList` или `gGOPathList` —
   с приоритетом 2:1 в пользу земной (водная обрабатывается, только если
   земная пуста ИЛИ `progresstick mod 2 == 0`).
2. Для каждого юнита в очереди вызывается
   `TopologyAddPathGameObjectByHandle`, и юниту присваивается
   числовая метка отряда (`squad`) для наземных юнитов или `-1` для водных.
3. Один пакетный вызов — `TopologyGetPath` (земля) или `TopologyGetPathExt`
   (вода) — рассчитывает пути для всей очереди разом.
4. Для каждого юнита проверяется отсутствие пути (`noPath`), задаются
   индексы текущей маршрутной точки, после чего список очищается.

**Что важно:**

1. **Один пакет на такт `progress`.** `progresstick` увеличивается каждые
   20 мс (`gc_progress_Interval = 0.02`). За один тик решается **одна**
   очередь — водная или земная — никогда обе.
2. **Земная очередь — приоритетная (2:1).** Водная обрабатывается
   только если земная пуста ИЛИ `progresstick mod 2 == 0`.
3. **Весь список считается единым вызовом** `TopologyGetPath` /
   `TopologyGetPathExt`. Это **пакетный запрос в нативный код**: движок
   получает массив юнитов с начальной и конечной точками, ищет путь для
   каждого и заполняет маршрутные точки. Алгоритм внутри **не виден из
   скриптов**.
4. **`squad` передаётся как числовая метка** перед запросом. Возможно,
   движок использует её для согласования маршрутов юнитов одного отряда
   или общей карты стоимости движения. Подтвердить это без
   декомпиляции нельзя.
5. **`noPath` определяется по `TrackPointCount == 0`**: если движок не
   нашёл путь, список маршрутных точек пуст.
6. После расчёта скрипт сам вставляет точки выхода из здания
   казармы или транспорта) и обнуляет `bpathrequested`.

#### Наблюдаемая роль `TopologyGetPath`

Из контекста использования и имени класса:

- **`QuadTree`** — пространственный индекс препятствий, разбивает мир на
  ячейки.
- **Топология** — это надстроечный граф **зон**
  (`TopologyGetZoneIndex(x, z)`); набор `_unit_TopologyAdd` /
  `_unit_TopologyRemove` / `_unit_TopologyProgress` [^8] поддерживает
  «в какой зоне сейчас этот юнит» для быстрой проверки расстояния.
- **`TopologyGetPathDistance(x1,z1,x2,z2,bIncludeBuildings)`** [^9] —
  синхронная функция, возвращающая длину пути по топологическому графу.
  Используется компьютерным игроком, а не непосредственным движением.
- **`TopologyGetPathToZone(zoneInd)`** [^10] — запрос «маршрут в зону»,
  используемый боевой логикой компьютерного игрока.

**Гипотеза о слоях:**

- Высокий уровень — A* по графу зон (узлы — `TTopZone`, рёбра —
  соединения через `gc_top_EffectDist=3`).
- Низкий уровень — проверка столкновений внутри зоны по сетке или
  `QuadTree`, которая расставляет маршрутные точки между узлами.

Это совместимо с константой `TopologySetPosSearchRadius(7)` (как далеко
искать «ближайшую проходимую точку»).

**Сетка:** `gc_collision_size = 0.5` [^11] — это размер
базовой ячейки столкновений **в клетках** (то есть одна ячейка =
0.5 клетки ≈ 26 пикселей). Также `gc_MaxColMapWidth = 2*gc_MaxMapWidth`
подтверждает: карта столкновений в 2 раза подробнее карты (640 → 1280
ячеек/сторона).

> **Алгоритм не виден**: вызовы `TopologyGetPath` / `TopologyGetPathExt`
> ведут в нативный код. Из скриптов нельзя установить, A* ли это,
> алгоритм поля направлений, волновой поиск или что-то иное. Косвенные
> признаки: пакетная обработка списка юнитов, передача номера отряда как
> метки, отдельная структура зон, `QuadTree` и трассировка прямой
> `TraceLineQuadTree` (следовательно, внутри поиска проверяется прямая
> видимость).

---

### Маршрутные точки

После `TopologyGetPath` каждый юнит получает массив **маршрутных точек**
(`TrackPoint`), которые движок читает на каждом кадре для интерполяции
движения:

- `GameObjectTrackPointAddByHandle(hnd, x, y, z)` — добавляет точку в конец.
- `GameObjectTrackPointInsertByHandle(hnd, ind, x, y, z)` — вставляет
  точку по индексу (например, выход из здания **в начало**).
- `SetGameObjectTrackPointCurrentPointIndexByHandle(hnd, idx)` — задать
  текущий.
- `GetGameObjectTrackPointCountByHandle(hnd)` — длина списка.
- `SetGameObjectTrackPointSkipPointsByHandle(hnd, true)` — разрешить
  пропускать промежуточные точки (если до следующего видимость есть).
- `SetGameObjectTrackPointSkipQuadTree(quadTree)` / `SkipFactor(1)` /
  `SkipEpsilon(0.1)` [^12] — параметры сглаживания пути.

Каждый юнит выбирает дерево препятствий для пропуска лишних точек:
для суши (`gc_obj_media_land`) используется `TopologyGetPathQuadTree`,
а для воды (`gc_obj_media_water`) — `TopologyGetTopologyQuadTree` [^12].

При достижении конца пути срабатывает `OnEndPointReached` [^13] —
переход в состояние ожидания (`move_idle`) и удаление приказа.

При завершении поворота срабатывает `OnDirectionReached` [^14].

---

### Предотвращение столкновений (`CollisionInertia`, `CI`)

Главный механизм, который заставляет юнитов **обходить друг друга**.
По сути это локальное физическое расталкивание с учётом массы и инерции,
накладываемое поверх уже проложенного пути.

#### Параметры отдельного юнита

Параметры предотвращения столкновений (`CI`) выставляются в
`SetCustomCollisionInertia` [^15]: `CIMass`,
`CIIntersectRadius`, `CIDeltaStep`, `CIRotationSpeed`, `CIStuckAngle`,
`CIEpsilonAngle`, `CIEpsilonShift`, `CIEpsilonMove`,
`CIDistExtPointEpsilon`, `CIMaxCollideCounter`, `CIMaxProcessObject`.

Константы:

- `gc_collision_radius_default = 0.16` [^16].
- `gc_collision_radius_stand = 0.1`.
- `gc_collision_radius_attack = 0.1`.

Поведенческие радиусы (использует `WriteMove` для дисперсии):

- `gc_obj_radius_default = 10`, `gc_obj_radius_horse = 15`.
- `gc_obj_radius_formation_default = 8`, `gc_obj_radius_formation_horse = 12`.

**Вывод:** радиус столкновения пешего юнита — около 0,16 клетки, то есть
маленький, юниты могут плотно стоять. Лошади получают `unitradius=15`
визуальный радиус.

#### Корабли получают большую инерцию столкновений

Корабли вызывают `SetCustomCollisionInertia` с большими множителями [^17]:
Транспорт (`ferry`) и Линейный корабль (`battleship`) получают
`radius × 11, mass × 32`; Фрегат (`frigate`) и Шебека (`xebec`) —
`9, 16`; Галера (`galley`) — `7, 12`; Чайка (`chaika`), Яхта
(`yacht`) и Турецкая яхта (`yachttur`) — `6, 8`; Рыбацкая лодка
(`fishboat`) — `3, 1`.

Это объясняет, почему корабли **расталкивают** друг друга и **сами не
сдвигаются** под напором пехоты: масса 32 против 1 у пехоты.

#### Здания — тяжёлые неподвижные препятствия

Здания инициализируются с `CollisionInertia=true`,
`CIIntersectRadius=0.35` клетки, `CIMovable=false`, `CIMass=10000`,
`CIStuckAngle=5` (у юнитов — 0), `CIAvoidPointMaxAngle=120`,
`CIMaxCollideCounter=7` [^18].

**Вывод:** здания — массивные неподвижные препятствия с радиусом 0,35
(плюс отдельная маска занимаемой площади на сетке; см.
[строительстве и ремонте](../../docs/recon/world/economy/building_mechanics.md)). Глобальный путь вокруг
здания строит глобальный поиск пути; локальная система столкновений лишь
страхует, чтобы
юнит не упёрся в стену вплотную.

#### Расталкивание юнитов и передний сектор в 90°

Правила столкновений задаются для трёх категорий: союзник (`Fr`), враг
(`En`) и нейтральный объект (`Nl`) — через
`SetGameObjectMyRuleCollidedExec*` [^19]:

- Союзник (`Fr`): событие **не** создаётся. Система всё равно физически
  расталкивает юнитов, но скрипт не вмешивается.
- Враг (`En`): событие создаётся, **только если враг в передних 90°**
  (`_misc_Collided`). Это объясняет, почему юнит начинает атаку врага
  «лицом к лицу», но не если задели сзади.
- Нейтральный объект (`Nl`): как и союзник, не создаёт события.

Сам обработчик `_misc_Collided` [^20] проверяет, что оба объекта —
`gc_obj_material_body`, и при попадании пытается атаковать через
`_unit_TryAttack`; если цель вне дальности и юнит не убегает —
заменяет текущий приказ на атаку.

**Итог работы расталкивания:**

1. **Союзник → союзник:** только физика (`mass` / `intersect` /
   `inertia`), без событий. Юниты «слипаются» и плавно расталкиваются —
   передний по направлению движения толкает заднего.
2. **Юнит → враг (фронт 90°):** вызывается `_misc_Collided`, который
   автоматически инициирует атаку.
3. **Юнит → здание / здание → юнит:** здание имеет
   `bMovable=False` и `mass=10000`, поэтому расталкивание его не
   сдвигает, а юнит обтекает препятствие.
4. **Снаряды и пешеход-маркеры:**
`SetGameObjectMyCollisionDetection(False)` — игнорируют систему
предотвращения столкновений.

---

### Обработка застревания

#### Проверка каждый кадр: «нет пути — остановиться»

После пакетного вызова `TopologyGetPath` [^21] для каждого юнита
вычисляется `noPath` через `TrackPointCount = 0`. Если маршрутные точки
есть, задаётся индекс текущей точки и включается анимация движения.
Если нет — и юнит был в `gc_statetag_move_walk` — вызывается
`_unit_Stop`.

**Если путь не найден** — юнит **просто останавливается**, без таймаута
и повторной попытки. Приказ остаётся (если `bRemove=False`), и юнит
«попробует ещё»
при следующем переходе в `execute_move`.

#### Сжатая толпа — `FindBestPosition`

`FindBestPosition` [^22] вызывается из `nothing.inc`, когда юнит стоит и
`standtime > 1` — пытается выйти из плотной толпы. Условия: число соседей
по коллизии больше `maxdensity = 3`, и из них хотя бы столько же стоят
`standtime >= 3 s`. Тогда начинается **спиральный поиск** в радиусе
шести ячеек сетки ожидания вокруг текущей позиции, после чего юнит
получает приказ переместиться в свободную клетку.
Срабатывает не каждый тик — период
`gc_unit_TimeFindBestPosition = 0.1*31 - 0.025 ≈ 3.075 s` контролируется
через `lasttimebestposition`.

#### Топология обновляется по таймеру

В `unit.inc/nothing.inc` периодически вызывается `_unit_TopologyProgress`
с интервалом `gc_unit_TimeTopology = 0.1*50 - 0.025 ≈ 4.975 s` [^23].
Это **не повторный поиск пути**, а переоценка текущей топологической
зоны для запросов расстояния компьютерного игрока.

#### Аварийное исправление зависания

В `unit.inc/nothing.inc` есть сторожевой таймер для невидимых юнитов в состоянии
«рождаюсь, но не вижусь» (вышел из казармы, но не отрисовался) [^24]:
после 1 с `standtime` им форсированно проставляется
`gc_statetag_essential_none`. Это не обычное застревание, а защита от
ошибки при выходе из транспорта или здания.

#### Проверка при загрузке: «два юнита в одной точке»

При генерации карты вызывается
`_misc_FixCollisionInertiaObjectsInOnePoint` [^25]: за три прохода
**уничтожаются** объекты окружения, наложившиеся в одной точке, —
иначе трассировка пути могла бы зациклиться. Проверка запускается из
`common.inc/dogenerate.inc:2070`.

#### Чего не найдено

- **Нет таймаута на путь.** Юнит может «бесконечно» висеть с
  `bpathrequested=True`, потом получить пустой путь и остановиться.
- **Нет телепорта по застреванию.** Сторожевой таймер
  `essential_none` из описанной выше аварийной проверки не
  телепортирует, а лишь сбрасывает флаг.
- **Нет ограничения длины очереди** `gGOPathList`. Скриптовый код её не
  ограничивает; всё, что попало в очередь, считается одним пакетом.

---

### Движение построения: каждый юнит идёт сам

Главный вывод: **построение не двигается как единое целое**.
Отдельного ведущего отряда нет — **каждый юнит получает собственную
целевую точку**.

#### `WriteMove`: отдельный приказ каждому юниту

`WriteMove` [^26] обходит сетку формации и для каждого юнита:

1. Вычисляет целевую клетку формации в мировых координатах.
2. Добавляет небольшое случайное смещение в пределах
   `unitradius * 1.1` через поворот на `random*360`.
3. Вызывает `_unit_OrderMove(gohnd, x_personal, y_personal, ...)` —
   отдельный приказ двигаться к своей клетке со случайным смещением.

Дальше юнит идёт **самостоятельно**, через стандартную цепочку
`_unit_PathListAdd` → `TopologyGetPath`. Никакого
«лидер-ведёт-остальные» нет.

Циклическая метка `gPathTag` (1–255) записывается в `info.amount` и
**не относится к поиску пути**: она нужна для синхронизации приказа
между сервером и клиентом.

#### Сетка построения

`_squad_FullRebuildGrid` [^27] хранит для каждого отряда сетку
`arGrid[i,j]`: какой юнит занимает каждую клетку. При перестроении
(поворот, переход в режим атаки и т. д.)
пересортировывает по направлению.

Константы [^28]: `gc_formation_maxcount = 160` (максимум юнитов в отряде),
`gc_formation_maskmaxwidth = 54`, `gc_formation_maskmaxheight = 24`.

#### `fMoveCount`: простой счётчик

`_player_CalcSquadsMoveCount` [^29] просто пересчитывает у каждого отряда
число юнитов в состоянии `gc_statetag_move_walk`. Запускается с периодом
`gc_global_TimeCalcSquadsMoveCount = 0.03*10 = 0.3 s`. Используется только
логикой агрессивного поведения отряда и проверкой удержания позиции
[^30]. К поиску пути отношения не имеет.

#### Номер отряда как подсказка движку

Перед пакетным вызовом `TopologyGetPath` каждый юнит получает
`SetGameObjectTagFloatByHandle(goHnd, TObj(pObj).squad)`. Что движок с
этим делает — **не видно из скриптов**. Гипотеза: согласование маршрутов
для одного отряда (юниты не пересекают друг другу пути в шахматном
порядке). Но это **не подтверждено**; нужна декомпиляция или
эмпирический тест с двумя отрядами в узком проходе.

#### Неиспользуемая константа

`gc_player_SquadMoveTick = 10` [^31] — **определена, но нигде не
используется** (поиск по всем файлам `.script` даёт только определение).
Возможно, она предназначалась для повторного поиска пути всем отрядом,
но не
реализована.

---

### Когда путь рассчитывается заново

| Когда юнит запрашивает новый путь | Почему |
|---|---|
| Переход в `gc_statetag_execute_move` | `_unit_PathListAdd` явно вызывается из `ontagstates.inc` |
| Сброс или смена приказа — `_unit_ClearOrders` → новый `_unit_OrderMove` | `_unit_OrderMove` создаёт приказ типа `gc_obj_order_type_move`, который выставляет `bDoPosition := True` в `_misc_DoProgressOrders` [^32] → `gc_statetag_execute_move` → `_unit_PathListAdd` |
| Сжатая толпа — `FindBestPosition` нашла свободную клетку | Раз в 3,075 игровой секунды максимум |

**Сценарии, в которых повторный поиск НЕ запускается** (подтверждено
поиском по
`unit.inc` и `miscext.script`):

- **Периодический пересчёт во время движения к цели.** Не реализован:
  не нашлось ни таймера, ни вызова. Если цель двигается, новый приказ ставит
  сама атака-логика.
- **Пересчёт при столкновении с врагом.** `_misc_Collided` вызывает не
  поиск пути,
  а `_unit_TryAttack` / `_unit_OrderAttack`. Сама атака уже даст новый
  приказ движения, если он нужен.
- **Пересчёт при появлении нового препятствия на пути.** Не найден. Если
  здание поставили прямо на маршрут идущего юнита, тот упрётся в
  `OnEndPointReached` и через `_unit_RemoveOrder` [^33] остановится.
  Дальше поведение зависит от типа приказа: `move` без `bRemove` войдёт
  в `move_walk` повторно и даст новый `PathListAdd`.

---

### Производительность и лимиты

#### Лимиты в скриптах

- **Очередь поиска пути не ограничена** в скриптах. Сколько юнитов
  попало в `gGOPathList` за тик (20 мс), столько и обработается за один
  вызов `TopologyGetPath`.
- **Сглаживание маршрутных точек:** `SkipFactor=1`, `SkipEpsilon=0.1`,
  `SkipPoints=true` [^12] — юнит может срезать промежуточные точки, если
  впереди прямая видимость.
- **Лимит обработки столкновений одного юнита** [^15]:
  - `MaxCollideCounter = 7*3 = 21` (число коллизий за тик до отбоя);
  - `MaxProcessObject = 4*3 = 12` (число объектов в окрестности,
обрабатываемых системой предотвращения столкновений).

#### Встроенный профайлер

Скрипт оборачивает `TopologyGetPath` в вызовы
`_misc_ProfilerBegin('progress.GetPath')` и `_misc_ProfilerEnd` [^34].
Данных профайлера в скриптах нет, но измерять стоимость движок может.

#### Глобальное ограничение цикла расчёта

В `progress.inc` [^35] для служебных игроков `misc` и `pool` есть
динамический `secmax` (адаптивная нарезка обработки). При `count > 700`
шаг растёт как `count div 20`; иначе условие `count < 2000` для обычного
неотрицательного счётчика всегда истинно и шаг равен `count div 15`.
Последняя ветка с `count div 10` фактически недостижима — вероятно, это
ошибка порядка условий. Для собственно `gGOPathList` **такого деления нет**:
очередь обрабатывается полностью.

---

## 9. Что ещё требует проверки

1. **Алгоритм поиска** — A*, поле направлений или волновой поиск?
   Нужна декомпиляция
   нативного `TopologyGetPath` или эмпирический тест: длинный путь с
   несколькими равно-длинными альтернативами и наблюдение, какой выбран.
   Гипотеза: A* с евклидовой эвристикой.
2. **Влияние числовой метки отряда:** действительно ли движок использует
   её для согласования маршрутов? Для проверки можно провести два отряда
   параллельно через узкий проход шириной в одна клетка и посмотреть,
   конфликтуют ли пути.
3. **Предел одновременного запроса:** сколько юнитов могут одновременно
   начать движение
   без падения частоты кадров — 200, 500, 1000? Скрипт очередь не
   ограничивает; у движка внутреннее ограничение возможно.
4. **Пересчёт при новом препятствии:** построить здание ровно на пути
   идущего отряда. Произойдёт ли автоматический пересчёт или юниты
   упрутся и остановятся?
5. **`CIStuckAngle = 0` у юнитов против `= 5` у зданий**: что это значит
   поведенчески? У зданий порог «считать застрявшим» 5°, у юнитов 0°.
   Вероятно, параметр связан с привязкой поворота в системе столкновений.
6. **Корабли + фрегат-дамми**: `bIsShipDummy` [^36] — отдельная
   коллизионная сущность? Влияет ли она на поиск пути?
7. **Связь маски здания (ячейка 0,5) и `CIIntersectRadius=0.35`:**
   `0.35 < 0.5`, значит радиус столкновения **меньше** сетки блокировки. Юниты
   могут «царапаться» о углы зданий — этой геометрией скрыта. Стоит
   проверить эмпирически.

---

## Сводка технических выводов

- **Алгоритм поиска пути находится в нативном движке.** Скрипты только:
  (а) добавляют юнитов в `gGOPathList` или `gWaterPathList` при начале движения,
  (б) вызывают `TopologyGetPath` или `TopologyGetPathExt` раз в 20 мс,
  (в) интерпретируют возвращённые маршрутные точки. Сам поиск
  **не виден**; косвенные признаки — мир столкновений `QuadTree`, граф
  `TTopZone` со связностью на радиусе 3 и `TraceLineQuadTree` для
  проверки прямой видимости.
- **Столкновениями управляет `CollisionInertia` (`CI`):** у каждого юнита
  есть масса и радиус. Здания имеют `mass=10000, movable=False`, корабли
  получают увеличенную массу и радиус. Союзники расталкиваются без
  события; враг в передних 90° вызывает автоматическую атаку.
- **Обработка застревания минимальна.** Если путь не найден, юнит просто
  стоит (ни таймаута, ни телепорта). При больше 3 стоящих соседей и
  `standtime >= 3 s` — `FindBestPosition` спирально ищет свободную
  клетку в радиусе 6. На старте
  `_misc_FixCollisionInertiaObjectsInOnePoint` сносит наложившиеся
  объекты окружения, чтобы не зацикливалась трассировка пути.
- **У построения нет общего ведущего.** `WriteMove` разбивает группу:
  группу: каждому юниту приходит свой
  `_unit_OrderMove(personal_x, personal_y)` со случайным смещением в
  пределах радиуса юнита. Единых путей отряда в скриптах нет; номер
  отряда передаётся движку как числовая метка, но эффект не виден из кода.
  `gc_player_SquadMoveTick = 10` — неиспользуемая константа.
- **Путь пересчитывается** только при смене приказа или новой команде
  движения; периодического пересчёта нет.
- **Лимитов в скриптах нет:** очередь обрабатывается одним батчем. Если
  500 юнитов одновременно стартуют — все в одном вызове
  `TopologyGetPath`. Стоимость измеряется встроенным `_misc_Profiler`,
  но скрипты не используют результат для ограничения нагрузки.

**Все вызовы из скрипта идут в нативный код, алгоритм поиска пути не
виден.** Дальнейшее исследование требует декомпиляции исполняемого файла
Cossacks 3 или
эмпирических тестов с целевыми сценариями (см. §9).

---

## Источники

Все пути относительно `data/scripts/` в установке Cossacks 3.

[^1]: `_init_InitializeTopology` — `lib/init.script:85-93`:

    ```pascal
    procedure _init_InitializeTopology();
    begin
       TopologyCreate;
       TopologySetTopologyPriority(gc_top_TopologyPriority);  // = 90
       TopologySetPathPriority(gc_top_PathPriority);          // = 70
       TopologySetPosSearchRadius(7);
       TopologySetBufferSize(SizeOf(TTopZone));
       TopologySetConnectionRadius(gc_top_EffectDist);        // = 3
    end;
    ```

[^2]: Константы топологии — `dmscript.global:140-153`:

    ```pascal
    gc_top_TopologyPriority = 90;   // QuadTree приоритет для блокеров (здания, terrain)
    gc_top_PathPriority     = 70;   // QuadTree приоритет для path-search (без зданий, или fewer)
    gc_top_WallPriority     = 95;   // отдельный для стен
    gc_top_WallQuadTree     = 2;
    gc_top_UnitTick         = 50;   // используется в gc_unit_TimeTopology
    gc_top_GlobalTick       = 100;
    gc_top_EffectDist       = 3;
    gc_top_MaxUpdateAreas   = 500;
    ```

[^3]: `_unit_PathListAdd` — `lib/unit.script:3324-3363`:

    ```pascal
    procedure _unit_PathListAdd(const goHnd : Integer);
    begin
       var pobj : Pointer = _unit_GetTObj(goHnd);
       if (pobj<>nil) then
       begin
          if (not TObj(pobj).bpathrequested) then
          begin
             if _unit_IsWaterUnit(goHnd) then
             gWaterPathList.Add(goHnd)
             else
             gGOPathList.Add(goHnd);
             TObj(pobj).bpathrequested := True;
          end;
       end;
    end;
    ```

[^4]: Вызов из `units/unit.inc/ontagstates.inc:692`:

    ```pascal
    if (switchExecute=gc_statetag_execute_move) then
    begin
       ...
       _unit_PathListAdd(myHnd);
       ...
    end
    ```

[^5]: Флаг `bpathrequested : Boolean` — `dmscript.global:1747`.

[^6]: Сериализация списков `gGOPathList` и `gWaterPathList` —
    `dmscript.source:340-341`.

[^7]: Главный батч `pathfinding`'а — `progress/progress.inc/nothing.inc:115-323`:

    ```pascal
    117: if (gWaterPathList.GetCount>0) and ((gGOPathList.GetCount=0) or (gProgress.progresstick mod 2=0)) then
    118:    pList := gWaterPathList; landPath := false;
    123: else
    124:    pList := gGOPathList; landPath := true;
    128:
    129: var count : Integer = TIntegerList(pList).GetCount;
    130: if (count>0) then begin
    131:    TopologyClearPathGameObjects;
    132:    for i := 0 to count-1 do begin
    135:       var goHnd : Integer = TIntegerList(pList).Get(i);
    144:       TopologyAddPathGameObjectByHandle(goHnd);
    149:       if TObjProp(pObjProp).media = gc_obj_media_land then
    150:          SetGameObjectTagFloatByHandle(goHnd, TObj(pObj).squad)   // squad-id для group-cost
    151:       else
    152:          SetGameObjectTagFloatByHandle(goHnd, -1);
    153:    end;
    155:    _misc_ProfilerBegin('progress.GetPath');
    157:    if landPath then
    158:       TopologyGetPath
    159:    else begin
    161:       var quadTree : Integer = TopologyGetTopologyQuadTree;
    162:       TopologyGetPathExt(quadTree, gc_collisiontag_water, gc_TestPriorityOption_Water);
    163:    end;
    165:    _misc_ProfilerEnd('progress.GetPath');
    167:    for i:=0 to count-1 do begin
    169:       var goHnd : Integer = TIntegerList(pList).Get(i);
    171:       var noPath : Boolean = (GetGameObjectTrackPointCountByHandle(goHnd) = 0);
    177:       TObj(pobj).bpathrequested := False;
           ...     // вставка exit-points у зданий, отворачивание трапа у транспортов и т.п.
    307:       DoSetupMoveAnimation(goHnd);
    308:       SetGameObjectTrackPointCurrentPointIndexByHandle(goHnd, 0);
    309:       SetGameObjectTrackPointCurrentPointIndexByHandle(goHnd, 1);
           ...
    322:    TIntegerList(pList).Clear;
    323: end;
    ```

[^8]: Поддержка топо-зон у юнита — `lib/unit.script:3248-3287, 6957-6977`
    (`_unit_TopologyAdd`, `_unit_TopologyRemove`, `_unit_TopologyProgress`).

[^9]: `TopologyGetPathDistance` — `lib/unit.script:6142, 6150`.

[^10]: `TopologyGetPathToZone` — `lib/misc.script:3231, 3255, 5241` и
    `progresswarai.inc`.

[^11]: `gc_collision_size = 0.5`, `gc_MaxColMapWidth = 2*gc_MaxMapWidth` —
    `dmscript.global:178`.

[^12]: Параметры сглаживания маршрутных точек —
       `units/unit.inc/initial.inc:280-287`:

    ```pascal
    gc_obj_media_land  : quadTree := TopologyGetPathQuadTree;     // 70 (path-mode, без зданий?)
    gc_obj_media_water : quadTree := TopologyGetTopologyQuadTree; // 90 (full-mode)
    ```

[^13]: `OnEndPointReached` — `units/unit.inc/onendpointreached.inc`.

[^14]: `OnDirectionReached` — `units/unit.inc/ondirectionreached.inc`.

[^15]: Начальные параметры столкновений отдельного юнита —
       `units/unit.inc/initial.inc:21-56`:

    ```pascal
    procedure SetCustomCollisionInertia(hnd : Integer; IntersectRadiusFactor, MassFactor, DeltaStepFactor : Float; bMovable : Boolean);
    begin
       SetGameObjectCollisionInertiaByHandle(hnd, IntersectRadiusFactor>0);
       if (IntersectRadiusFactor<=0) then exit;
       SetGameObjectCIAvoidPointMaxAngleByHandle(hnd, 180);
       SetGameObjectCIMassByHandle(hnd, 1*massFactor);
       SetGameObjectCIIntersectRadiusByHandle(hnd, gc_collision_radius_default*IntersectRadiusFactor);
       SetGameObjectCIMaxDistKoefByHandle(hnd, 2);
       SetGameObjectCIDeltaStepByHandle(hnd, 0.005/DeltaStepFactor);
       SetGameObjectCIRotationSpeedByHandle(hnd, 5);
       SetGameObjectCIStuckAngleByHandle(hnd, 0); // 0.5 in rw2to
       SetGameObjectCIEpsilonAngleByHandle(hnd, 4);
       SetGameObjectCIEpsilonShiftByHandle(hnd, 0.001);
       SetGameObjectCIEpsilonMoveByHandle(hnd, 0.02);
       SetGameObjectCIDistExtPointEpsilonByHandle(hnd, 0.005);
       SetGameObjectCIMovableByHandle(hnd, bMovable);
       SetGameObjectCIBuildExtPointsByHandle(hnd, True);
       SetGameObjectCIMaxCollideCounterByHandle(hnd, 7*3);
       SetGameObjectCIMaxProcessObjectByHandle(hnd, 4*3);
       ...
    end;
    ```

[^16]: Константы радиусов коллизии — `dmscript.global:972`
    (`gc_collision_radius_default = 0.16`, `gc_collision_radius_stand = 0.1`,
    `gc_collision_radius_attack = 0.1`).

[^17]: Параметры предотвращения столкновений кораблей —
    `units/unit.inc/initial.inc`:

    ```pascal
    'ferry'              : SetCustomCollisionInertia(myHnd, 11, 32, 0.1, ...);   // radius x11, mass x32
    'battleship'         : ...                                                    11, 32
    'frigate', 'xebec'   : ...                                                     9, 16
    'galley'             : ...                                                     7, 12
    'chaika'             : ...                                                     6,  8
    'yacht', 'yachttur'  : ...                                                     6,  8
    'fishboat'           : ...                                                     3,  1
    ```

[^18]: Параметры предотвращения столкновений зданий —
    `units/building.inc/initial.inc:59-72`:

    ```pascal
    SetGameObjectCollisionInertiaByHandle(colHnd, true);   // CI включён
    SetGameObjectCIIntersectRadiusByHandle(colHnd, 0.35);  // 0.35 клетки
    SetGameObjectCIMovableByHandle(colHnd, false);         // не двигается
    SetGameObjectCIMassByHandle(colHnd, 10000);            // 10000 — фактически бесконечная
    SetGameObjectCIMaxDistKoefByHandle(colHnd, 2);
    SetGameObjectCIDeltaStepByHandle(colHnd, 0.005);
    SetGameObjectCIRotationSpeedByHandle(colHnd, 5);
    SetGameObjectCIStuckAngleByHandle(colHnd, 5);          // !! здания → 5°, юниты → 0
    SetGameObjectCIEpsilonAngleByHandle(colHnd, 4);
    SetGameObjectCIEpsilonShiftByHandle(colHnd, 0.001);
    SetGameObjectCIEpsilonMoveByHandle(colHnd, 0.02);
    SetGameObjectCIDistExtPointEpsilonByHandle(colHnd, 0.005);
    SetGameObjectCIAvoidPointMaxAngleByHandle(colHnd, 120);
    SetGameObjectCIMaxCollideCounterByHandle(colHnd, 7);
    ```

[^19]: Правила расталкивания союзников, врагов и нейтральных объектов —
       `units/unit.inc/initial.inc:303-318`:

    ```pascal
    SetGameObjectMyCollisionExecAsFunc(true);
    SetGameObjectMyRuleCollidedExecFr(4, 35.0, False);   // friendly:  flags=4, fov=35° → no collide event
    SetGameObjectMyRuleCollidedExecEn(2, 90.0, False);   // enemy:     flags=2, fov=90° → fire event
    SetGameObjectMyRuleCollidedExecNl(4, 35.0, False);   // neutral:   flags=4, fov=35° → no collide event
    if gbool_use_collision then SetGameObjectMyCollidedStateName('_misc_Collided');
    ```

[^20]: `_misc_Collided` — `lib/miscext.script:1235-1289`:

    ```pascal
    procedure _misc_Collided(const hnd: Integer);
    begin
       if (_net_IsOffline or _net_IsServer) and not _net_IsReplay
           and (GetGameObjectPlayableObjectByHandle(hnd)) then begin
          var trg: integer = GetGameObjectStateCollisionObjectByHandle(hnd);
          ...
          if (gObjProp[TObj(pobj).cid][TObj(pobj).id].material = gc_obj_material_body)
             and (gObjProp[TObj(pobj2).cid][TObj(pobj2).id].material = gc_obj_material_body) then
          begin
             if (GetGameObjectTrackPointMovementModeIntByHandle(hnd) <> 0) then
             begin
                var res : Integer = _unit_TryAttack(hnd, trg, false);
                if (res<=gc_result_tryattack_outofrange) then begin
                   if not isrunaway then begin
                      if (orders[0].itype=attackobj) and (orders[0].info.trg<>trg) then
                         _unit_SetOrderTrg(hnd, 0, trg, True)
                      else
                         _unit_OrderAttack(hnd, trg, True, False, False);
                   end;
                end;
             end;
             // и симметрично для trg → hnd (если trg тоже двигался)
          end;
       end;
    end;
    ```

[^21]: Обработка `noPath` — `progress/progress.inc/nothing.inc:171-316`:

    ```pascal
    171: var noPath : Boolean = (GetGameObjectTrackPointCountByHandle(goHnd) = 0);
    ...
    301: var tpCount : Integer = GetGameObjectTrackPointCountByHandle(goHnd);
    302: if tpCount > 0 then begin
           SetGameObjectTargetRotatingModeByHandle(goHnd, 'trmNone');
           DoSetupMoveAnimation(goHnd);
           SetGameObjectTrackPointCurrentPointIndexByHandle(goHnd, 0);
           SetGameObjectTrackPointCurrentPointIndexByHandle(goHnd, 1);
    312: end else begin
    313:    if _unit_GetTagStateByType(goHnd, gc_statetag_move) = gc_statetag_move_walk then
    314:       _unit_Stop(goHnd);
    315: end;
    ```

[^22]: `FindBestPosition` — `lib/miscext.script:190-252`, вызов из
    `nothing.inc`/`miscext.script:654-658`:

    ```pascal
    function FindBestPosition(goHnd : Integer; var px, pz : Float) : Boolean;
    begin
       const maxdensity = 3;
       var count : Integer = GetGameObjectCountCollidedObjectsByHandle(goHnd);
       if (count>maxdensity) then begin
          var standcount : Integer;
          for i:=0 to count-1 do begin
             trgHnd := GetGameObjectCollidedGOHandleByHandle(goHnd, i);
             ptrgobj := _unit_GetTObj(trgHnd);
             if (ptrgobj<>nil) and (TObj(ptrgobj).standtime>=3) then
                standcount := standcount+1;
          end;
          if (standcount>maxdensity) then begin
             var radius : Integer = 6;
             var minind : Integer = 8+floor(random*16);
             var maxind : Integer = GetSpiralStepsByRadius(radius)-1;
             if (ProcessSpiralIdleGridSearch(goX, goZ, 1, minind, maxind, radius, x, y)) then
                ...
                _unit_OrderMove(goHnd, goX, goZ, vecx, vecz, gc_obj_order_move_mode_default, False);
          end;
       end;
    end;
    ```

[^23]: Периодическое обновление топологии — `units/unit.inc/nothing.inc:128-132`:

    ```pascal
    if gametime>arg_obj.lasttimetopology then begin
       arg_obj.lasttimetopology := gametimewithrnd+gc_unit_TimeTopology;
       _unit_TopologyProgress(myHnd);
    end;
    ```

[^24]: Аварийное исправление зависания —
       `units/unit.inc/nothing.inc:148-154`:

    ```pascal
    else if (statetag and gc_statetag_essential_birth<>0)
           and (statetag and gc_statetag_visual_none<>0) then
    if ((arg_obj.orders[0].itype<gc_obj_order_type_leavetransport)
        and (arg_obj.orders[0].itype>gc_obj_order_type_leavebuilding))
        or (arg_obj.standtime>1) then
    begin
       _unit_SetTagStates(myHnd, gc_statetag_essential_none);
       ErrorLog('unit:nothing: Possible hang unit was fixed to essential_none');
    end;
    ```

[^25]: `_misc_FixCollisionInertiaObjectsInOnePoint` —
    `lib/misc.script:3739-3780`:

    ```pascal
    // fix issue when game may stuck on path trace
    var tries : Integer;
    for [MAIN]tries:=0 to 2 do
    if (GetCountOfPlayers>gc_playerind_env) then begin
       const epsilon = 0.001;
       ...
       for i:=GetPlayerGameObjectsCountByHandle(plhnd)-1 downto 0 do begin
          ...
          if (...VectorDistance < epsilon) then begin
             GameObjectDestroyByHandle(goHnd);
             break;
          end;
       end;
    end;
    ```

[^26]: `WriteMove` (раздача отдельных приказов движения юнитам отряда) —
    `units/global.inc/writemove.inc:79-138`:

    ```pascal
    for j:=rows-1 downto 0 do
    for i:=cols-1 downto 0 do begin
       var gohnd : Integer = GetGroupGameObjectHandleByGridColRow(grhnd, i, j);
       if gohnd <> 0 then begin
          // вычисляем целевую клетку формации в мировых координатах
          x := posx + (i-cols/2+0.5) * minx * hdirx - (j+0.5) * miny * dirx;
          y := posz + (i-cols/2+0.5) * minx * hdirz - (j+0.5) * miny * dirz;

          // случайная дисперсия в пределах unit-radius (jitter)
          var unitradius : Float = gObjProp[...].radius;
          var dispradius : Float = unitradius*1.1;
          var dispx : Float = (0.5-random)*dispradius;
          VectorRotateY(dispx, dispy, dispz, random*360);
          x := x+dispx;
          y := y+dispz;

          if not addord then _unit_ClearOrders(gohnd);
          var pOrder : Pointer = _unit_OrderMove(gohnd, x, y, dirX, dirZ, mode, dofirst);
          if (pOrder<>nil) then TOrder(pOrder).info.amount := gPathTag;
       end;
    end;
    ```

[^27]: `_squad_FullRebuildGrid` — `lib/squad.script:199-263`.

[^28]: Константы формации — `dmscript.global:166-168`:

    ```pascal
      gc_formation_maxcount      = 160;   // максимум юнитов в отряде
    gc_formation_maskmaxwidth  = 54;
    gc_formation_maskmaxheight = 24;
    ```

[^29]: `_player_CalcSquadsMoveCount` — `lib/player.script:2591-2607`:

    ```pascal
    procedure _player_CalcSquadsMoveCount(plInd : Integer);
    begin
       for i := gPlayer[plInd].squads.GetCount-1 downto 0 do begin
          var pSquad : Pointer = gPlayer[plInd].squads.Get(i);
          TSquad(pSquad).fMoveCount := 0;
          for j := TSquad(pSquad).GetCount-1 downto 0 do begin
             var goHnd : Integer = TSquad(pSquad).Get(j);
             if ((GetGameObjectStatesTagByHandle(goHnd) and gc_statetag_move_walk)<>0) then
                TSquad(pSquad).fMoveCount := TSquad(pSquad).fMoveCount + 1;
          end;
       end;
    end;
    ```

[^30]: Использование `fMoveCount` — `progress.inc:152, 160`,
    `lib/miscext.script:20`.

[^31]: `gc_player_SquadMoveTick = 10` — `dmscript.global:155`.

[^32]: `_misc_DoProgressOrders` (выставление `bDoPosition := True` для
приказа `move`) — `lib/miscext.script:317-330, 613-633`.

[^33]: `_unit_RemoveOrder` при появлении непроходимого препятствия —
    `units/unit.inc/onendpointreached.inc:54-58`. Авторский комментарий
    `should be logged only if unit stop cause of new unpathable collision on his way`
    поясняет: сообщение следует записывать, только если юнит остановился
    из-за нового непроходимого препятствия на пути.

[^34]: Профайлер вокруг `TopologyGetPath` —
    `progress/progress.inc/nothing.inc:155, 165`:

    ```pascal
    _misc_ProfilerBegin('progress.GetPath');
    ... TopologyGetPath / TopologyGetPathExt ...
    _misc_ProfilerEnd('progress.GetPath');
    ```

[^35]: Адаптивный `secmax` — `progress/progress.inc:325-346`:

    ```pascal
    if (count>700) then secmax := secmax+(count div 20)
    else if (count<2000) then secmax := secmax+(count div 15)
    else secmax := secmax+(count div 10);
    ```

[^36]: `bIsShipDummy` — `units/unit.inc/initial.inc:200-256`.
