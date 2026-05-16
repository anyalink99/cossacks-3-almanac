# Recon: стены и ворота

Глубокий разбор: как устроены кластеры стен (`gWallSystem` /
`TWallCluster`), как сегменты строятся крестьянами, чем ворота
отличаются от обычной стены, что происходит при попытке захвата.

## TL;DR

- Стена — здание с `usage = gc_obj_usage_hardwall` или
  `gc_obj_usage_weakwall` и флагом `bwall = True` [^1]. Игрок «рисует»
  линию мышью, после клика появляются недостроенные сегменты
  (`bbuilt = False, hp = 10`), и крестьяне строят их **как обычные
  здания** через стандартный путь `_player_ConstructBuildingList` →
  `_player_OrderUnitsToBuild` [^2][^3].
- Сегмент стены — 1 × 1 тайл. Длинная стена — последовательность
  сегментов в `TWallCluster` [^4].
- Builder slots для каждого сегмента берутся из
  `gCustomBuildPointsWall[wallvariation]` (источник —
  `data/game/var/wallcustom.cfg`); вариация = 0 обрабатывается как
  обычное здание [^5].
- Все 21 нации имеют **частокол** (`ukrwwa` / `ukrwga`). **Каменная
  стена** (`eurswa` / `russwa` / `turswa` плюс ворота) есть у всех,
  **кроме UKR** [^6]. Конкретный кластер (`eur` / `rus` / `tur`)
  выбирается по семье нации.
- Ворота — это апгрейд `gc_upg_type_single_buildgate`, применяемый к
  выбранной достроенной стене [^7]. Стоимость — 400 wood (UKR) или
  500 stone (остальные нации). Апгрейд требует **прямой участок из
  трёх одинаковых достроенных сегментов**: углы и концы стены,
  T-перекрёстки, стройка отвергаются [^8].
- Постройка ворот **моментальная**: `_player_ConstructGates`
  выставляет на новом сегменте `individual.upglevel := 1`, после чего
  `_unit_ControlBuildProgress` через специальную ветку
  `if (bwall) and (upglevel>0) then hp := maxhp` ставит полное HP, а
  state-machine handler `OnTagStates.essential_none` сразу
  переключает `bbuilt := True, hp := maxhp, buildprogress := 1` [^9][^10].
  Крестьяне в постройке ворот не участвуют.
- Захват сегмента стены (или ворот) пехотой противника на
  `gc_gameplay_captureradius = 4` тайла **не передаёт владельца**, а
  уничтожает сегмент: в `_misc_CheckCapture` для всех `bwall`
  принудительно ставится `bDie := True` [^11]. Если HP сегмента
  меньше 1/3 от максимума, проверка захвата вообще пропускается —
  такой сегмент уже только добивают оружием [^12].

---

## 1. Типы стен и их доступность

Два класса по `usage` и `material` [^1]:

| Класс | `usage` | sid стены / ворот | Material | Доступность |
|---|---|---|---|---|
| Слабая (частокол) | `gc_obj_usage_weakwall` | `ukrwwa` / `ukrwga` | `gc_obj_material_woodwall` | **Все 21 нации** |
| Прочная (каменная), eur-кластер | `gc_obj_usage_hardwall` | `eurswa` / `eursga` | `gc_obj_material_building` | Все, кроме UKR / RUS / TUR / ALG |
| Прочная (каменная), rus-кластер | `gc_obj_usage_hardwall` | `russwa` / `russga` | `gc_obj_material_building` | RUS |
| Прочная (каменная), tur-кластер | `gc_obj_usage_hardwall` | `turswa` / `tursga` | `gc_obj_material_building` | TUR / ALG |

UKR имеет только частокол; каменной стены у этой нации нет [^6].

Параметры из кода [^1]:

**Частокол `ukrwwa` / `ukrwga`.** HP: 1500 у общей версии и 2500 у
UKR (стена), 1000 у общей и 1500 у UKR (ворота). Цена: 10 wood
(общее) / 12 wood (UKR). Buildtime в кадрах: 18 (общее) / 26 (UKR).
Bgate-флаг ставится только у `ukrwga`.

**Каменная стена `*swa` / `*sga`.** HP: 50000 у стены, 32000 у ворот.
Цена: 50 stone (eur) / 60 stone (rus, tur). Buildtime в кадрах:
288 (eur) / 640 (rus) / 384 (tur). Все три кластера ставят
`bwall = True`, `bgate = True` (только у `*sga`), `usage =
gc_obj_usage_hardwall`. У сегмента стены `consume.stone` = 250
(eur) / 200 (rus) / 150 (tur) — постоянное потребление stone, пока
сегмент стоит [^1].

Конкретные числа по нациям — в
[`reference/03_buildings/README.md`](../../../reference/03_buildings/README.md).

## 2. Footprint и кластеры

Сегмент стены имеет collision-mask 2 × 2 ячейки (1 тайл). Несколько
последовательных сегментов:

```
[wall][wall][wall]   ← 3 тайла линии
```

Между сегментами зазора нет; pathfinding не пускает врагов через
плотную линию.

`gWallSystem` — глобальный объект (`TWallSystem`) со списком
кластеров (`TWallCluster`) [^4]. Каждый кластер содержит `wallType`
(`hardwall` / `weakwall`), `cid` нации, `plIndex` владельца, массив
`Cells` (по `TWallCell` на сегмент), а также флаги режима постройки
(`firstWall`, `buildWall`).

Когда сегмент умирает (HP = 0 или принудительный death-tag),
`_unit_OnDeath` вызывает `gWallSystem.RemoveHandle(pl, goHnd)` —
удаляет cell из кластера и обновляет связи соседей [^13].

### 2.1. Wall variations и builder slots

Builder slots сегмента зависят от его геометрической ориентации в
кластере (`wallvariation`). При сборе списка строителей в
`_player_OrderUnitsToBuild` логика выбирает массив точек из
`gCustomBuildPointsWall[variation]` для всех зданий с
`bwall or bgate = True`, **кроме случая `variation = 0`** — тогда
используется обычный `gCustomObjPoints[cid, id]`, как для не-стен
[^5].

Те же `builderPoints` используются и для постройки, и для ремонта —
обе ветки проходят через `_unit_OrderBuild` [^3].

Cap движка — `gc_MaxWallBuilderPointsCount = 16`. Содержимое массива
заполняется парсером `data/game/var/wallcustom.cfg` [^14].

## 3. Постройка стены крестьянами

Игрок выбирает sid стены в UI и протягивает линию мышью; превью
рисуется через `_misc_UpdateWall(gWallCluster)` (отдельные «фантомные»
объекты на players-misc, моргающие синим) [^15]. По нажатию
подтверждения каждый сегмент создаётся стандартной процедурой
`_player_ConstructBuildingList` [^2] — той же, что используется для
любого здания. Сегмент стартует с `bbuilt = False, buildprogress = 0,
hp = 10`, после чего `_player_OrderUnitsToBuild` рассылает крестьян на
постройку.

Крестьяне получают приказ `gc_obj_order_type_build`, идут к точке из
`gCustomBuildPointsWall[wallvariation]`, бьют молотком, поднимают HP и
buildprogress по обычной формуле постройки (см.
[`building_mechanics.md` §3](../economy/building_mechanics.md) о
механике в целом). На каждом тике state-machine `nothing` зданий
вызывается `_unit_ControlBuildProgress(myHnd)` [^16] — он пересчитывает
`buildprogress = hp / maxhp`, при `hp >= maxhp` ставит тег
`gc_statetag_essential_none`, по которому handler `OnTagStates`
переводит сегмент в `bbuilt := True` [^10].

Для обычной стены `individual.upglevel = 0`, поэтому fast-path
«hp := maxhp» в `_unit_ControlBuildProgress` не срабатывает, и
сегмент достраивается стандартным темпом крестьян. Ресурсы списываются
за каждый сегмент отдельно (`_unit_ApplyCostByID`). Отменить постройку
конкретного сегмента до завершения можно стандартной кнопкой —
недостроенный сегмент сносится с возвратом ресурсов по обычной формуле
refund.

## 4. Захват и снос сегмента

Стандартный механизм захвата идёт через `_misc_CheckCapture`: когда
вражеский пехотинец оказывается в `gc_gameplay_captureradius = 4`
тайла от объекта `bcapture = True` без своих защитников, объект
меняет владельца [^11]. Для стен и ворот эта процедура работает иначе:

1. Сначала отдельная функция `_unit_SearchCapturersForWall` ищет
   capturer'ов рядом — с менее строгим фильтром, чем для обычных
   зданий (`bcancapture` цели не требуется) [^11].
2. Если HP сегмента меньше 1/3 от `maxhp`, дальнейшая логика
   пропускается — сегмент уже доедают оружием, без эффекта capture
   [^12].
3. Иначе при найденном capturer'е принудительно срабатывает
   `bDie := True` (специальная ветка для `bwall`) — сегмент
   получает `gc_statetag_essential_death` и уничтожается [^11].

Поведение одинаковое и для готовой стены, и для недостроенной
(`bbuilt = False`): в обоих случаях достаточно пехотинца врага в
радиусе 4 тайлов — сегмент мгновенно сносится. Это «снос», а не
«захват»; владельцем сегмент не становится.

У ворот `bwall = True` (плюс дополнительный `bgate = True`), поэтому
ветка `bDie := True` срабатывает и для них.

## 5. Ворота как моментальный апгрейд

Ворота создаются исключительно через `gc_upg_type_single_buildgate` —
индивидуальный апгрейд, применяемый к одному выбранному сегменту
стены [^7][^17]. Стоимость и место исследования по `country.script`
[^18]:

| Нация / sid | Цена | Куда исследуется |
|---|---|---|
| `ukrwwa.1` | 400 wood | у выбранного сегмента ukrwwa |
| `eurswa.1` | 500 stone | у выбранного сегмента eurswa (eur-кластер) |
| `russwa.1` | 500 stone | у выбранного сегмента russwa (RUS) |
| `turswa.1` | 500 stone | у выбранного сегмента turswa (TUR / ALG) |

Перед запуском апгрейда движок проверяет геометрию через
`_misc_GetGateBaseSprite` [^8]: возвращает корректный sprite ворот,
только если

1. выбранный сегмент **не на конце** кластера (есть соседи слева и
   справа);
2. оба соседа имеют тот же sprite (стена идёт прямо — не угол, не
   T-перекрёсток);
3. все три сегмента (`p1, p2, p3`) **достроены** (`bbuilt = True`);
4. в радиусе 1.85 тайла от центра ровно три стены (не больше).

Если хоть одно условие не выполнено — `Result = -1`, и апгрейд не
запустится. Поэтому ворота можно ставить только посреди прямого
участка стены минимум из трёх достроенных сегментов.

### 5.1. Что происходит при срабатывании апгрейда

`_player_ConstructGates(goHnd)` [^9]:

1. Устанавливает `gbool_gui_gatefinished := True` (используется позже
   в `_unit_DoExplosion`, чтобы пропускать визуальный взрыв
   hardwall-сегментов после первой постройки ворот в матче [^19]).
2. Получает `wallcluster`, в котором лежит `goHnd`, и индекс
   центральной cell.
3. Очищает sprite у соседних cells (`p1` и `p3`) и ставит на
   центральной (`p2`) sprite ворот.
4. Создаёт новый объект ворот в той же позиции через
   `_player_ConstructBuildingList` с **пустым списком крестьян**
   (`gIntegerList.Clear` перед вызовом). Объект на этом этапе имеет
   обычный для стройки набор: `bbuilt = False, hp = 10,
   buildprogress = 0`.
5. **Сразу после возврата** ставит `TObj(pobj).individual.upglevel :=
   upglevel + 1` — этот инкремент и активирует следующий шаг.
6. Привязывает новый handle к cell: `TWallCell(p2).goHnd := trgHnd`.
7. Если игрок наблюдатель — переключает UI-выделение со старого
   сегмента на новый объект ворот.

На ближайшем тике state-machine handler `nothing` для зданий вызывает
`_unit_ControlBuildProgress(myHnd)` [^16]. У свежесозданных ворот
теперь `bwall = True` и `upglevel = 1 > 0`, и срабатывает специальная
ветка [^20]:

> `if (bwall) and (upglevel>0) then hp := maxhp;`

После присвоения hp сразу же выполняется проверка
`if hp >= maxhp then SetTagStates(essential_none)`, по которой handler
`OnTagStates` ([building.inc/ontagstates.inc:134][^10]) переводит
объект в финальное состояние: `bbuilt := True, hp := maxhp,
buildprogress := 1`, плюс инкремент player-counters и
обновление визуала.

С точки зрения игрока ворота появляются **полностью построенными**
сразу после применения апгрейда. Никакой паузы на стройку и никаких
крестьян для них не нужно.

### 5.2. Подмена цели при создании ворот

Прикладной приём, вытекающий из последовательности выше:

- противник атакует сегмент стены (`goHnd_old`); атака идёт по
  конкретному handle (`gc_obj_order_type_attackobj` хранит trg);
- игрок применяет апгрейд buildgate на этом сегменте, если форма
  стены позволяет;
- `_player_ConstructGates` создаёт новый handle ворот (`goHnd_new`),
  переставляет указатель cell на него и инкрементирует `upglevel`;
  старый сегмент теряет роль активной точки в кластере;
- атакующие юниты теряют цель — для возобновления атаки противнику
  нужно отдать новую команду на новый объект;
- накопленный по старому сегменту урон не переносится: ворота уже
  стоят с полным HP (`maxhp = 32000` у hardwall, ~1000–1500 у
  частокольного `ukrwga`). Защитник получает прямую замену
  потрёпанной стены на свежую.

## 6. Стенные башни

Часть наций имеет отдельные sid'ы стенных башен (`stonewalltower` и
аналоги), которые встают в линию стены без зазора и стреляют как
обычная башня. Для механики прицеливания и стоимости выстрела см.
[`towers.md`](towers.md).

## 7. Открытые эмпирические вопросы

1. Как именно `costpercent` применяется к сегментам стены при
   массовой стройке: за каждый сегмент или за весь рисунок.
2. Точная скорость постройки сегмента крестьянами в зависимости от
   `wallvariation` (variation = 0 идёт по обычной формуле, остальные —
   по explicit `builderPoints`).
3. Поведение в редкой ситуации: апгрейд buildgate стартует, но к
   моменту достройки соседние сегменты уже разрушены — корректно ли
   ворота останутся в кластере или окажутся «висящим» зданием.

---

## Источники

[^1]: `data/scripts/lib/unit.script:2258-2310` — `commonsid+'swa'` /
      `commonsid+'sga'` (каменные стены и ворота, общие для cluster'ов
      eur / rus / tur), `'ukrwwa'` / `'ukrwga'` (частокол и
      деревянные ворота). Здесь устанавливаются `usage`, `bwall`,
      `bgate`, `material`, `maxhp`, цены, consume.

      ```pascal
      commonsid+'swa', commonsid+'sga' : begin
         SetObjBuildingProperties(objprop, objbase, 50000, 288, 0);
         SetObjBasePrice(objbase, 0, 0, 50, 0, 0, 0);
         objprop.consume[gc_resource_type_stone] := 250;
         objprop.bwall := True;
         objprop.usage := gc_obj_usage_hardwall;
         if (commonrus) then ... // 60 stone, consume 200, bt 640
         if (commontur) then ... // 60 stone, consume 150, bt 384
         if (objprop.sid=commonsid+'sga') then begin
            objprop.bgate := True;
            objbase.maxhp := 32000;
         end;
      end;
      'ukrwwa', 'ukrwga' : begin
         SetObjBuildingProperties(objprop, objbase, 1500, 18, 0);
         if (ukr) then SetObjBuildingProperties(objprop, objbase, 2500, 26, 0);
         SetObjBasePrice(objbase, 0, 10, 0, 0, 0, 0);
         if (ukr) then SetObjBasePrice(objbase, 0, 12, 0, 0, 0, 0);
         objprop.material := gc_obj_material_woodwall;
         objprop.bwall := True;
         objprop.usage := gc_obj_usage_weakwall;
         if (objprop.sid='ukrwga') then begin
            objprop.bgate := True;
            if (ukr) then objbase.maxhp := 1500
            else objbase.maxhp := 1000;
         end;
      end;
      ```

[^2]: `data/scripts/lib/player.script:1476-1581` —
      `_player_ConstructBuildingList`. Создаёт здание стандартным
      путём, перезаписывая инициализированные `_unit_InitObj`
      значения на стройку:

      ```pascal
      trghnd := CreatePlayerGameObjectHandleByHandle(plHnd, gc_racename_buildings, sid, px, 0, pz);
      var pobj : Pointer = _unit_GetTObj(trghnd);
      if pobj <> nil then begin
         TObj(pobj).bbuilt := False;
         TObj(pobj).buildprogress := 0;
         TObj(pobj).hp := 10;
         _unit_ControlBuildProgress(trghnd);
      end;
      ...
      _player_OrderUnitsToBuild(list, trgHnd, bClearOrders, false, false);
      ```

[^3]: `data/scripts/lib/unit.script:9268-9378` — `_unit_OrderBuild`.
      Линии 9280-9286 выбирают источник builderPoints для стен/ворот:

      ```pascal
      var bwall : Boolean = gObjProp[cid][id].bwall;
      var variation : Integer = TObj(pTrgObj).wallvariation;
      var bCount : Integer;
      if (bwall) then
         bCount := gCustomBuildPointsWall[variation].builderCount
      else
         bCount := gCustomObjPoints[cid, id].builderCount;
      ```

      Команда `_unit_AddOrder(..., gc_obj_order_type_build, ...)`
      выдаётся на 9371. Та же функция используется и для
      `gc_obj_order_type_repair`.

[^4]: `data/scripts/lib/classes.script:2857-3232` — `TWallCluster` и
      `TWallSystem`: поля (`wallType`, `cid`, `plIndex`, `Cells`),
      методы `AddCell` / `DeleteCell` / `Clear` / `ConnectToPoint` /
      `KeepSegment` / `CreateSprites` / `SetWallBuildMode`.

[^5]: `data/scripts/lib/player.script:1137-1148` — выбор массива
      `builderPoints` для стен/ворот при рассылке крестьян:

      ```pascal
      var bwall : Boolean = (gObjProp[cid][id].bwall) or (gObjProp[cid][id].bgate);
      var variation : Integer = TObj(pTrgObj).wallvariation;
      if (bwall) and (variation=0) then
         bwall := False;
      if (bwall) then
         bCount := gCustomBuildPointsWall[variation].builderCount
      else
         bCount := gCustomObjPoints[cid, id].builderCount;
      ```

      `gCustomBuildPointsWall` объявлен в
      `classes.script:7664` как глобальный массив длины
      `gc_MaxWallVariationCount`.

[^6]: `data/scripts/lib/country.script:2867-2886` — добавление
      sid'ов стен в нацию. `ukrwwa` / `ukrwga` добавляются всем 21
      нациям без условий. Каменная стена идёт через cluster-ветки
      (`not ukr and not tur and not alg and not rus → eurswa`,
      `tur or alg → turswa`, `rus → russwa`):

      ```pascal
      _country_AddMember(country, 'ukrwwa', ind, True, ...);
      _country_AddMember(country, 'ukrwga', ind, True, ...);
      if (not ukr) and (not tur) and (not alg) and (not rus) then
      begin
         _country_AddMember(country, 'eurswa', ind, True, ...);
         _country_AddMember(country, 'eursga', ind, True, ...);
      end;
      if (tur) or (alg) then begin _country_AddMember(country, 'turswa', ...); ... end;
      if (rus) then        begin _country_AddMember(country, 'russwa', ...); ... end;
      ```

      У UKR ни одна из ветвей `swa` не активируется — каменной
      стены нация не получает.

[^7]: `data/scripts/lib/player.script:1974-1981` — handler апгрейда
      `gc_upg_type_single_buildgate` в `_player_ApplyUpgrade`:

      ```pascal
      gc_upg_type_single_buildgate : begin
         var pobj : Pointer = _unit_GetTObj(goHnd);
         if (pobj<>nil) and (gObjProp[TObj(pobj).cid][TObj(pobj).id].bwall) then
         begin
            TObj(pobj).individual.benabled := True;
            TObj(pobj).individual.upglevel := TObj(pobj).individual.upglevel + 1;
            _player_ConstructGates(goHnd);
         end;
      end;
      ```

[^8]: `data/scripts/lib/misc.script:3998-4058` —
      `_misc_GetGateBaseSprite`. Возвращает sprite (14, 15, 16, 17),
      только если все условия про прямой участок и достроенность
      выполнены; иначе `-1` (апгрейд блокируется).

[^9]: `data/scripts/lib/player.script:1583-1645` —
      `_player_ConstructGates`. Линия 1612 создаёт новый объект
      ворот через `_player_ConstructBuildingList`, линия 1615
      инкрементирует `individual.upglevel`, линия 1616
      переписывает `TWallCell(p2).goHnd` на новый handle.

[^10]: `data/scripts/units/building.inc/ontagstates.inc:134-137` —
       handler `OnTagStates` зданий, ветка
       `gc_statetag_essential_none`. Здесь объект окончательно
       переходит в built-state:

       ```pascal
       arg_obj.bbuilt := True;
       arg_obj.hp := gPlayer[arg_obj.pl].objBase[arg_obj.cid][arg_obj.id].maxhp;
       arg_obj.buildprogress := 1;
       _unit_AddObjToPlayerCounters(myHnd, True, False, False);
       ```

[^11]: `data/scripts/lib/miscext.script:961-1185` —
       `_misc_CheckCapture`. Линия 975 — `bwall :=
       TObjProp(pobjprop).bwall`. Линии 1003-1006 переключают
       поиск capturer'ов на `_unit_SearchCapturersForWall` (без
       требования `bcancapture` у capturer'а). Линия 1106 —
       специальная ветка для `bwall`:

       ```pascal
       var bDie : Boolean;
       var bAutoKill : Boolean;
       if (bAutoKill) or (TObjProp(pobjprop).bwall) then
       begin
          bDie := True;
       end;
       ```

       После чего ниже выполняется
       `_unit_SetTagStates(goHnd, gc_statetag_essential_death)`.

[^12]: `data/scripts/lib/miscext.script:1034` —
       `if (not ((bwall) and (TObj(pobj).hp<TObjBase(pobjbase).maxhp/3))) then`.
       При HP менее 1/3 от max ветка capture полностью пропускается.

[^13]: `data/scripts/lib/unit.script:3954` — вызов
       `gWallSystem.RemoveHandle(pl, goHnd)` при смерти сегмента в
       `_unit_OnDeath`.

[^14]: `data/scripts/lib/country.script:4096-4101` — заполнение
       `gCustomBuildPointsWall[variation].builderCount` и
       `builderPoints[j].x/y` парсером
       `data/game/var/wallcustom.cfg`.
       `gc_MaxWallBuilderPointsCount = 16` — `dmscript.global`.

[^15]: `data/scripts/lib/miscext2.script:933-975` — `_misc_UpdateWall`:
       создаёт «фантомные» объекты на players-misc и зажигает синий
       blink при наведении, обновляет `gCanPlaceBuildingWalls`.

[^16]: `data/scripts/units/building.inc/nothing.inc:296-307` —
       state-machine handler `nothing` (idle) для зданий. Пока
       `not arg_obj.bbuilt`, на каждом срабатывании вызывается
       `_unit_ControlBuildProgress(myHnd)`:

       ```pascal
       if (not arg_obj.bbuilt) then
       begin
          if gametime>arg_obj.lasttimecheckcapture then
          begin
             arg_obj.lasttimecheckcapture := gametimewithrnd+gc_unit_TimeCheckCapture;
             _misc_CheckCapture(myHnd);
          end;
          _unit_ControlBuildProgress(myHnd);
       end;
       ```

[^17]: Поле `bindividual := True` у апгрейда buildgate ([country.script:3944][^18])
       помечает его как индивидуальный — применяется к одному
       выбранному объекту, а не глобально к нации.

[^18]: `data/scripts/lib/country.script:3942-3973` — регистрация
       апгрейдов buildgate:

       ```pascal
       upgplace := 'ukrwwa';
       _country_AddUpgradeWithAccessControl(country, upgplace+'.1', 2, ..., gc_upg_type_single_buildgate, 5, ..., 0, 400, 0, ...);  // 400 wood
       country.upgrade[ind-1].bindividual := True;
       ...
       if (rus) then begin upgplace := 'russwa'; ... 0, 0, 500, ... end; // 500 stone
       if (tur) or (alg) then begin upgplace := 'turswa'; ... 0, 0, 500, ... end;
       if (not ukr) then begin upgplace := 'eurswa'; ... 0, 0, 500, ... end;
       ```

[^19]: `data/scripts/lib/unit.script:11429` — условие в
       `_unit_DoExplosion`:
       `if (not gbool_gui_gatefinished) or (TObjProp(pobjprop).usage<>gc_obj_usage_hardwall) then`.
       После первого `_player_ConstructGates` визуальный взрыв
       debris для hardwall-сегментов отключается на оставшийся матч.

[^20]: `data/scripts/lib/unit.script:6572-6608` —
       `_unit_ControlBuildProgress`. Ключевая ветка для ворот в
       начале процедуры:

       ```pascal
       if (gObjProp[TObj(pobj).cid][TObj(pobj).id].bwall) and (TObj(pobj).individual.upglevel>0) then
          TObj(pobj).hp := gPlayer[TObj(pobj).pl].objbase[TObj(pobj).cid][TObj(pobj).id].maxhp;
       ```

       После присвоения проверяется
       `if hp >= maxhp then _unit_SetTagStates(hnd, gc_statetag_essential_none ...)`
       — это и триггерит OnTagStates handler [^10], в котором
       `bbuilt := True`.
