# Recon: pathfinding и движение юнитов

Как юниты в Cossacks 3 ищут путь, обходят друг друга и здания, и что
происходит при блокировке. **Главный вывод сразу:** сам алгоритм
pathfinding'а живёт в нативном движке (C++); скрипты только ставят юнитов
в очередь, передают целевую точку и читают результат. Алгоритм не виден —
виден только каркас вокруг него.

**Связанные документы:**

- [ticks_and_subticks.md](ticks_and_subticks.md) — главный progress-loop
  (`gc_progress_Interval = 0.02 s`), unit-tick = 100 ms.
- [server_sync_architecture.md](server_sync_architecture.md) —
  `WriteMove` / `ReadMove`, server-authoritative модель, сериализация
  очереди в save.
- [building_mechanics.md](building_mechanics.md) — footprint и `CIMass`
  у зданий (массивные «якоря» для коллизий).

Все пути к скриптам ниже — относительно `data/` в установке Cossacks 3.

## TL;DR

- Движение юнита — это **две независимые подсистемы**: глобальный
  pathfinding (поиск пути A → B через QuadTree-карту препятствий) и
  локальная коллизия / расталкивание (`CollisionInertia`). Обе живут в
  нативном движке; в скриптах — только запросы к ним.
- Pathfinding **батчится** раз в 20 мс (`progress`-тик): движок берёт всю
  очередь юнитов, ждущих маршрут, и считает пути одним проходом.
  Локальная коллизия — каждый кадр.
- Размер ячейки коллизии — `0.5` тайла (`gc_BuilderDist = 1.0` для
  расстановки строителей вокруг здания).
- **Дружественный push** — беззвучный: свои отряды раздвигают друг друга,
  без анимации.
- **Враг в 90° спереди** → юнит автоматически переключается на атаку
  даже если шёл на другую цель.
- **Формация** = jittered offset для каждого юнита, а не следование за
  squad-leader'ом. Поэтому и двигается «расплываясь».

## 1. Архитектура: две независимые подсистемы

Движок разделяет навигацию юнита на две слабо связанные подсистемы:

| Подсистема | Что делает | Где живёт |
|---|---|---|
| **Topology + QuadTree path-search** | Глобальный поиск пути A → B через зоны проходимости; возвращает массив `TrackPoint`'ов. | Нативные API `Topology*` / `TraceLine*`. |
| **CollisionInertia (CI)** | Per-frame локальный обход соседей вдоль уже проложенного пути (push / avoid с массами и инерцией). | Нативные API `*CI*`. |

Скрипты обращаются к обеим через `Set / Get*ByHandle` — **детали
реализации в нативном коде, скриптам не видны**.

Точка входа в скрипты: `_init_InitializeTopology` (lib/init.script:85-93):

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

Константы (`dmscript.global:140-153`):
```
gc_top_TopologyPriority = 90;   // QuadTree приоритет для блокеров (здания, terrain)
gc_top_PathPriority     = 70;   // QuadTree приоритет для path-search (без зданий, или fewer)
gc_top_WallPriority     = 95;   // отдельный для стен
gc_top_WallQuadTree     = 2;
gc_top_UnitTick         = 50;   // используется в gc_unit_TimeTopology
gc_top_GlobalTick       = 100;
gc_top_EffectDist       = 3;
gc_top_MaxUpdateAreas   = 500;
```

Это **QuadTree-based collision world** с двумя слоями приоритета: первый включает все статические препятствия, второй — только terrain и стены. У запросов «юнит идёт через здание» приоритет ниже, чтобы pathfinding мог найти путь «как будто здания нет».

---

## 2. Pathfinding: где и как

### 2.1 Очередь и батчевание

**Очередь:** два глобальных списка `unit.script:3324-3363`:

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

Юнит добавляется в `gGOPathList` (земля) или `gWaterPathList` (вода) **ровно один раз** при переходе в состояние `gc_statetag_execute_move` (units/unit.inc/ontagstates.inc:692):

```pascal
if (switchExecute=gc_statetag_execute_move) then
begin
   ...
   _unit_PathListAdd(myHnd);
   ...
end
```

Флаг `bpathrequested : Boolean` (dmscript.global:1747) защищает от дублирования.

**Списки сериализованы** в save/replay (dmscript.source:340-341) — это часть состояния мира.

### 2.2 Главный батч (раз в progress-tick = 20ms)

Весь батч pathfinding'а — в progress/progress.inc/nothing.inc:115-323. Я цитирую ключевые строки (с очищенным синтаксисом):

```
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

**Что важно:**
1. **Один батч на progress-tick.** `progresstick` инкрементируется каждые 20 ms (`gc_progress_Interval = 0.02`). За один тик решается **одна** очередь — водная или земная — никогда обе.
2. **Земная очередь — приоритетная (2:1).** Водная обрабатывается только если земная пуста ИЛИ `progresstick mod 2 == 0`.
3. **Весь список считается единым вызовом** `TopologyGetPath` / `TopologyGetPathExt(quadTree, gc_collisiontag_water, gc_TestPriorityOption_Water)`. Это **батч-запрос в нативный код**: kernel получает массив юнитов с их (start, end), выполняет path-search для каждого, заполняет TrackPoint'ы. Алгоритм внутри — **не виден из скриптов**.
4. **`squad` передаётся как float-tag** перед запросом — kernel, видимо, использует его для group-routing (юниты одного отряда могут получать согласованные пути / shared cost-map). Подтвердить это эмпирически нельзя без декомпиляции.
5. **`noPath` определяется по `TrackPointCount == 0`**: если kernel не нашёл путь, TrackPoint'ов нет.
6. После батча скрипт сам вставляет building-exit-points (выход из казармы / транспорта) и обнуляет `bpathrequested`.

### 2.3 Что делает `TopologyGetPath` (наблюдаемо)

Из контекста использования и имени класса:
- **QuadTree** — пространственный индекс препятствий, разбивает мир на ячейки.
- **Topology** — это надстроечный граф **зон** (`TopologyGetZoneIndex(x, z)`), `_unit_TopologyAdd/Remove/Progress` (unit.script:3248-3287, 6957-6977) поддерживает «в какой зоне сейчас этот юнит» для быстрого distance-check.
- **`TopologyGetPathDistance(x1,z1,x2,z2,bIncludeBuildings)`** (unit.script:6142, 6150) — синхронная funciton, возвращающая длину пути по топологическому графу. Используется AI, не движением.
- **`TopologyGetPathToZone(zoneInd)`** (misc.script:3231, 3255, 5241, progresswarai.inc) — query «маршрут в зону», AI war-logic.

**Гипотеза о слоях:**
- Высокий уровень — A* по графу зон (узлы — `TTopZone`, рёбра — соединения через `gc_top_EffectDist=3`).
- Низкий уровень — внутри зоны grid/quadtree-collision-test, чтобы вписать TrackPoint'ы между узлами.

Это совместимо с константой `TopologySetPosSearchRadius(7)` (как далеко искать «ближайшую проходимую точку»).

**Сетка:** `gc_collision_size = 0.5` (dmscript.global:178) — это размер base-collision-cell **в тайлах** (т.е. 1 «collision cell» = 0.5 тайла = ~26 пикселей). Также `gc_MaxColMapWidth = 2*gc_MaxMapWidth` подтверждает: collision-карта в 2 раза мельче карты (640 → 1280 cells/side).

> **Алгоритм не виден**: вызовы `TopologyGetPath` / `TopologyGetPathExt` ведут в нативный код. Из скриптов нельзя установить, A* ли это, flow-field, wave-propagation или что-то иное. Документированные косвенные признаки: батчевая обработка списка юнитов, передача squad-id как hint, наличие отдельной структуры зон + QuadTree, raycast-функция `TraceLineQuadTree` (значит, есть LoS-checks внутри path-search).

---

## 3. TrackPoint'ы — выход pathfinding'а

После `TopologyGetPath` каждый юнит получает массив **TrackPoint'ов** (waypoints), которые читаются движком на каждом frame для интерполяции движения:

- `GameObjectTrackPointAddByHandle(hnd, x, y, z)` — append
- `GameObjectTrackPointInsertByHandle(hnd, ind, x, y, z)` — insert (используется чтобы вставить exit-point здания **в начало**)
- `SetGameObjectTrackPointCurrentPointIndexByHandle(hnd, idx)` — установить текущий
- `GetGameObjectTrackPointCountByHandle(hnd)` — длина списка
- `SetGameObjectTrackPointSkipPointsByHandle(hnd, true)` — позволять пропускать промежуточные точки (если до следующего видимость есть)
- `SetGameObjectTrackPointSkipQuadTree(quadTree)` / `SkipFactor(1)` / `SkipEpsilon(0.1)` (units/unit.inc/initial.inc:280-287) — параметры smoothing'а пути.

Каждый юнит-объект инициализирует skip-quadtree выбором:
```
gc_obj_media_land  : quadTree := TopologyGetPathQuadTree;     // 70 (path-mode, без зданий?)
gc_obj_media_water : quadTree := TopologyGetTopologyQuadTree; // 90 (full-mode)
```

При достижении конца пути: `OnEndPointReached` (units/unit.inc/onendpointreached.inc) — переключение в `move_idle`, удаление order'а.

При завершении поворота: `OnDirectionReached` (units/unit.inc/ondirectionreached.inc).

---

## 4. Collision avoidance (CI = CollisionInertia)

Главный механизм, который заставляет юнитов **обходить друг друга**. По
сути — локальное физическое расталкивание (push с массами и инерцией),
накладываемое поверх уже проложенного пути.

### 4.1 Per-unit init

units/unit.inc/initial.inc:21-56:

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

Константы:
- `gc_collision_radius_default = 0.16` (dmscript.global:972).
- `gc_collision_radius_stand   = 0.1`.
- `gc_collision_radius_attack  = 0.1`.

Поведенческие радиусы (использует `WriteMove` для дисперсии):
- `gc_obj_radius_default = 10`, `gc_obj_radius_horse = 15`.
- `gc_obj_radius_formation_default = 8`, `gc_obj_radius_formation_horse = 12`.

**Вывод:** intersect-radius у пешего юнита ≈ 0.16 тайла — очень маленький, юниты могут плотно стоять. Лошади получают `unitradius=15` (display-radius).

### 4.2 Корабли получают огромную CI

```pascal
'ferry'              : SetCustomCollisionInertia(myHnd, 11, 32, 0.1, ...);   // radius x11, mass x32
'battleship'         : ...                                                    11, 32
'frigate', 'xebec'   : ...                                                     9, 16
'galley'             : ...                                                     7, 12
'chaika'             : ...                                                     6,  8
'yacht', 'yachttur'  : ...                                                     6,  8
'fishboat'           : ...                                                     3,  1
```

Это объясняет, почему корабли **расталкивают** друг друга и **сами не сдвигаются** под напором пехоты: масса 32 против 1 у пехоты.

### 4.3 Здания — неподвижные тяжёлые блокеры

units/building.inc/initial.inc:59-72:

```pascal
SetGameObjectCollisionInertiaByHandle(colHnd, true);   // CI включён
SetGameObjectCIIntersectRadiusByHandle(colHnd, 0.35);  // 0.35 тайла
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

**Вывод:** здания — это массивные неподвижные блокеры с радиусом 0.35 (плюс отдельный footprint-mask на cell-grid, см. [building_mechanics.md](building_mechanics.md)). Глобальный путь вокруг здания строит pathfinding; локальная коллизия (CI) лишь страхует от того, чтобы юнит не упёрся в стену вплотную.

### 4.4 Push-mechanic между юнитами: правило «передний + 90° FOV»

units/unit.inc/initial.inc:303-318:

```
SetGameObjectMyCollisionExecAsFunc(true);
SetGameObjectMyRuleCollidedExecFr(4, 35.0, False);   // friendly:  flags=4, fov=35° → no collide event
SetGameObjectMyRuleCollidedExecEn(2, 90.0, False);   // enemy:     flags=2, fov=90° → fire event
SetGameObjectMyRuleCollidedExecNl(4, 35.0, False);   // neutral:   flags=4, fov=35° → no collide event
if gbool_use_collision then SetGameObjectMyCollidedStateName('_misc_Collided');
```

Семантика рулей CI (по используемым параметрам):
- `Fr` (friendly): event **не** генерируется. CI всё равно физически расталкивает (push), но скрипт не вмешивается.
- `En` (enemy): event генерируется, **только если враг в передних 90°** (_misc_Collided). Это объясняет, почему юнит начинает атаку врага «лицом к лицу», но не если задели сзади.
- `Nl` (neutral): как и friendly — без event'а.

**lib/miscext.script:1235-1289 `_misc_Collided`:**

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

**Резюме push-механики:**
1. **Союзный → союзный**: чистая физика CI (`mass` / `intersect` / `inertia`), без событий. Юниты «слипаются» и плавно расталкиваются — передний по направлению движения толкает заднего.
2. **Враг → враг (фронт 90°)**: вызывается `_misc_Collided`, который автоматически инициирует атаку.
3. **Юнит → здание / здание → юнит**: здание `bMovable=False` + mass=10000 → push physics не двигает здание, юнит обтекает.
4. **Снаряды / пешеход-маркеры**: `SetGameObjectMyCollisionDetection(False)` — игнорируют CI.

---

## 5. Stuck handling

### 5.1 Per-frame: "no path → stop"

В батче pathfinding'а (progress.inc/nothing.inc:171-316):

```
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

**Если путь не найден** → юнит **просто останавливается**, без таймаута и retry. Order остаётся (если `bRemove=False`), и юнит «попробует ещё» при следующем переходе в `execute_move`.

### 5.2 Сжатая толпа — `FindBestPosition`

lib/miscext.script:190-252: вызывается из nothing.inc когда юнит idle и `standtime>1` (miscext.script:654-658) — пытается выйти из плотной толпы:

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

**Условия:** `count_of_collided_neighbors > 3` И из них `standtime >= 3s` тоже > 3. Тогда — **спиральный поиск** в радиусе 6 idle-grid-cells вокруг текущей позиции, и order на перемещение в свободную клетку. Триггер не каждый тик: контролируется `lasttimebestposition` с периодом `gc_unit_TimeFindBestPosition = 0.1*31 - 0.025 = 3.075s`.

### 5.3 Топология обновляется по таймеру

units/unit.inc/nothing.inc:128-132:

```pascal
if gametime>arg_obj.lasttimetopology then begin
   arg_obj.lasttimetopology := gametimewithrnd+gc_unit_TimeTopology;
   _unit_TopologyProgress(myHnd);
end;
```

`gc_unit_TimeTopology = 0.1*50 - 0.025 ≈ 4.975s`. Это **не repath**, это переоценка «в какой топо-зоне я нахожусь» (для AI distance-queries).

### 5.4 Hard «hang fix»

units/unit.inc/nothing.inc:148-154:

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

**Это watchdog для невидимых юнитов в состоянии «рождаюсь, но не вижусь»** (вышел из казармы, но не отрисовался) — после 1s standtime их форсированно «дорождают». Не обычный stuck, но защита от глитча transport/leave-building.

### 5.5 Loader-pass на старте: «два юнита в одной точке»

lib/misc.script:3739-3780 `_misc_FixCollisionInertiaObjectsInOnePoint`:

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

При генерации карты **уничтожаются** environment-объекты, наложившиеся в одну точку — иначе path-trace зацикливался бы. Запускается из common.inc/dogenerate.inc:2070.

### 5.6 Чего НЕ найдено

- **Нет таймаута на путь** — юнит может «бесконечно» висеть в `bpathrequested=True` через тик, потом получить пустой путь и остановиться.
- **Нет телепорта по стуку.** Watchdog `essential_none` (5.4) не телепортирует, а лишь сбрасывает флаг.
- **Нет cap'а на длину очереди** `gGOPathList`. Скриптовый код её не ограничивает; всё, что попало в очередь, считается за один батч.

---

## 6. Formation movement: каждый юнит идёт сам

Главный insight: **формация не двигается как единое целое**. Squad-leader'а как такового нет — **каждый юнит получает свой индивидуальный target**.

### 6.1 `WriteMove` — рассыпать squad на per-unit ордера

units/global.inc/writemove.inc:79-138:

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

**Каждый юнит получает свой `_unit_OrderMove(x_personal, y_personal, ...)` с координатами своей клетки** + `random*360` jitter дисперсии. Дальше юнит идёт **самостоятельно**, через стандартную `_unit_PathListAdd` → `TopologyGetPath` цепочку. Никакого «лидер-ведёт-остальные» нет.

`gPathTag` (rolling 1..255) пишется как `info.amount` — **не относится к pathfinding'у**, это order-cookie для server↔client sync.

### 6.2 Грид формации

lib/squad.script:199-263 `_squad_FullRebuildGrid`: держит per-squad `arGrid[i,j]` — какой юнит в какой клетке формации. При перестроении (drag угол поворота, attack-mode и т.д.) пересортировывает по направлению.

Константы (dmscript.global:166-168):
```
gc_formation_maxcount      = 160;   // макс юнитов в squad
gc_formation_maskmaxwidth  = 54;
gc_formation_maskmaxheight = 24;
```

### 6.3 `fMoveCount` — ПРОСТО счётчик

lib/player.script:2591-2607:

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

Запускается с периодом `gc_global_TimeCalcSquadsMoveCount = 0.03*10 = 0.3s` (progress.inc:152). Используется только squad-aggressive-логикой и hold-mode-проверкой (progress.inc:160, miscext.script:20). К pathfinding'у отношения не имеет.

### 6.4 Squad-id как hint для kernel

Помним из §2.2: перед `TopologyGetPath` каждый юнит получает `SetGameObjectTagFloatByHandle(goHnd, TObj(pObj).squad)`. Что kernel с этим делает — **не видно из скриптов**. Гипотеза: согласованный routing для одного отряда (юниты не пересекают друг другу пути в шахматном порядке). Но это **не подтверждено**; нужна декомпиляция или эмпирический тест с двумя отрядами в узком проходе.

### 6.5 Orphan-константа

`gc_player_SquadMoveTick = 10` (dmscript.global:155) — **определена, но нигде не используется** (Grep по всем .script даёт только определение). Возможно, был зарезервирован для сквадного repath, но не реализован.

---

## 7. Repath frequency

| Когда юнит запрашивает новый путь | Почему |
|---|---|
| Переход в `gc_statetag_execute_move` | `_unit_PathListAdd` явно вызывается из `ontagstates.inc` |
| Сброс/смена order'а — `_unit_ClearOrders` → новый `_unit_OrderMove` | `_unit_OrderMove` создаёт новый Order с типом `gc_obj_order_type_move`, который → `bDoPosition := True` в `_misc_DoProgressOrders` (miscext.script:317-330, 613-633) → `gc_statetag_execute_move` → `_unit_PathListAdd` |
| Сжатая толпа — `FindBestPosition` нашла свободную клетку | См. §5.2 — раз в 3.075 s максимум |

**Сценарии, в которых repath НЕ запускается** (подтверждено грепом по `unit.inc`/`miscext.script`):

- **Periodic repath во время движения к цели.** Не реализован — не нашлось ни таймера, ни вызова. Если цель двигается, новый order ставит сама атака-логика.
- **Repath при коллизии с врагом.** `_misc_Collided` вызывает не repath, а `_unit_TryAttack` / `_unit_OrderAttack`. Сама атака уже даст новый move-order, если он нужен.
- **Repath при появлении нового препятствия на пути.** Не найден. Если здание поставили прямо на маршрут идущего юнита, тот упрётся в `OnEndPointReached` и через `_unit_RemoveOrder` (onendpointreached.inc:54-58, комментарий «should be logged only if unit stop cause of new unpathable collision on his way») остановится. Дальше поведение зависит от вида order'а: `move` без `bRemove` войдёт в `move_walk` повторно и даст новый `PathListAdd`.

---

## 8. Производительность / лимиты

### 8.1 Лимиты в скриптах

- **Очередь pathfinding'а — без cap'а** в скриптах. Сколько юнитов вошли в `gGOPathList` за тик (20 ms), столько и обработается за один `TopologyGetPath`-вызов.
- **TrackPoint smoothing**: `SkipFactor=1`, `SkipEpsilon=0.1`, `SkipPoints=true` (initial.inc:286-287) — значит, юнит может срезать промежуточные точки если впереди прямая видимость.
- **CI per-unit budget**:
  - `MaxCollideCounter = 7*3 = 21` (число коллизий за тик до отбоя)
  - `MaxProcessObject = 4*3 = 12` (число объектов в окрестности, обрабатываемых CI)
  (initial.inc:43-44).

### 8.2 Профайлер встроен

Скрипт оборачивает `TopologyGetPath` в progress.inc:155, 165:

```
_misc_ProfilerBegin('progress.GetPath');
... TopologyGetPath / TopologyGetPathExt ...
_misc_ProfilerEnd('progress.GetPath');
```

Данных профайлера в скриптах нет, но измерять стоимость движок может.

### 8.3 Глобальный progress-cap

progress.inc:325-346: для misc/pool-плееров есть динамический `secmax` (адаптивная нарезка обработки).

```
if (count>700) then secmax := secmax+(count div 20)
else if (count<2000) then secmax := secmax+(count div 15)
else secmax := secmax+(count div 10);
```

Для собственно gGOPathList — **такого нет**, очередь обрабатывается полностью.

---

## 9. Open questions (для эмпирических замеров)

1. **Алгоритм path-search** — A*, flow-field или wave? Декомпиляция нативного `TopologyGetPath` или эмпирический тест: длинный путь с несколькими равно-длинными альтернативами и наблюдение, какой выбран. Гипотеза: A* с heuristic = euclidean.
2. **Влияние squad-id float-tag**: реально ли он передаётся kernel'у как group-routing hint? Эмпирически: двинуть два squad'а параллельно через узкий проход (1 тайл), посмотреть, конфликтуют ли пути.
3. **Граница path-list-burst**: сколько юнитов одновременно стартуют move без падения FPS? 200? 500? 1000? Скрипт не ограничивает, kernel — возможно.
4. **Repath на новое препятствие**: построить здание ровно на пути идущего отряда. Произойдёт ли автоматический repath или юниты упрутся и остановятся?
5. **CIStuckAngle = 0** у юнитов vs **= 5** у зданий: что это поведенчески значит? У зданий порог «считать застрявшим» 5°, у юнитов 0°. Скорее всего связано с rotation-snapping CI-physics.
6. **Корабли + фрегат-дамми**: `bIsShipDummy` (initial.inc:200-256) — отдельная коллизионная сущность? Влияет ли на pathfinding?
7. **Связь footprint-mask здания (cell=0.5) и CIIntersectRadius=0.35**: 0.35 < 0.5, значит CI-радиус **меньше** грида блокировки. Юниты могут «царапаться» о углы зданий — этой геометрией скрыта. Стоит проверить эмпирически.

---

## 10. Резюме

- **Алгоритм pathfinding'а — в нативном движке.** Скрипты только: (а) добавляют юнитов в `gGOPathList`/`gWaterPathList` при старте move, (б) вызывают `TopologyGetPath`/`TopologyGetPathExt` раз в 20 ms, (в) интерпретируют возвращённые TrackPoint'ы. Сам поиск (A* / flow / wave) **не виден**; косвенно — это QuadTree-collision-world + граф `TTopZone` со связностью на радиусе 3 + path-priority/topology-priority слои + `TraceLineQuadTree` для LoS-checks.
- **Collision avoidance — это CollisionInertia (CI)**: per-unit масса/радиус, push physics. Здания — `mass=10000, movable=False`, корабли получают увеличенную массу/радиус. Юнит-юнит push беззвучен; враг в передних 90° → автоматический attack-event.
- **Stuck handling — минимальный.** Если путь не найден — юнит просто стоит (ни таймаута, ни телепорта). При >3 стоящих соседей и `standtime>=3s` — `FindBestPosition` спирально ищет свободную клетку в радиусе 6. На старте `_misc_FixCollisionInertiaObjectsInOnePoint` сносит наложившиеся environment-объекты, чтобы не застревал path-trace.
- **Formation movement — НЕ squad-leader.** `WriteMove` рассыпает группу: каждому юниту приходит свой `_unit_OrderMove(personal_x, personal_y)` с jitter в пределах unit-radius. Никаких единых сквадных путей в скриптах нет; squad-id передаётся kernel как float-tag, но эффект не виден из кода. `gc_player_SquadMoveTick = 10` — orphan-константа.
- **Repath**: только при смене order'а или новом move-команде. Periodic repath отсутствует.
- **Лимитов в скриптах нет**: очередь обрабатывается одним батчем. Если зрелище 500 юнитов одновременно стартуют — все в одном `TopologyGetPath`-вызове. Стоимость измеряется встроенным `_misc_Profiler`, но скрипты её не используют для троттлинга.

**Вызовы из скрипта в нативный код, алгоритм path-search не виден.** Дальнейшее исследование требует декомпиляции Cossacks 3 EXE или эмпирических тестов с целевыми сценариями (см. §9).
