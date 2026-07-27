# Стены и ворота

[← Как устроена игра](../../README.md)

Как прокладываются и строятся линии стен, где разрешено поставить ворота и
почему вражеская пехота не захватывает сегмент, а разрушает его. Внутренние
структуры и последовательности вызовов вынесены в
[технические подробности](#technical-details).

## Коротко

- Игрок протягивает линию мышью, после чего крестьяне возводят каждый
  сегмент **как обычное здание** [^2][^3].
- Один сегмент занимает одну клетку. Длинная стена состоит из связанных
  сегментов без зазоров [^4].
- У разных вариантов сегмента свои места для строителей; одновременно
  предусмотрено до 16 рабочих мест [^5].
- Все 21 нации имеют **Частокол** и частокольные ворота. **Каменная
  стена** есть у всех, кроме Украины [^6].
- Ворота создаются улучшением выбранного достроенного сегмента [^7].
  Стоимость — 400 дерева для
  Частокола или 500 камня для Каменной стены. Улучшение требует
  **прямого участка из
  трёх одинаковых достроенных сегментов**: углы и концы стены,
  T-перекрёстки, стройка отвергаются [^8].
- Ворота появляются **мгновенно и с полным здоровьем**. Крестьяне в
  постройке не участвуют [^9][^10].
- Пехота противника на расстоянии четырёх клеток **не получает стену во
  владение, а уничтожает сегмент** [^11]. Если его здоровье
  меньше 1/3 от максимума, проверка захвата вообще пропускается —
  такой сегмент уже только добивают оружием [^12].

---

## 1. Типы стен и их доступность

В игре есть два класса стен [^1]:

| Класс | Внутренние имена стены / ворот | Свойства движка | Доступность |
|---|---|---|---|
| **Частокол и частокольные ворота** | `ukrwwa` / `ukrwga` | `gc_obj_usage_weakwall`, `gc_obj_material_woodwall` | **Все 21 нации** |
| **Европейская Каменная стена и ворота** | `eurswa` / `eursga` | `gc_obj_usage_hardwall`, `gc_obj_material_building` | Все, кроме Украины, России, Турции и Алжира |
| **Русская Каменная стена и ворота** | `russwa` / `russga` | `gc_obj_usage_hardwall`, `gc_obj_material_building` | Россия |
| **Турецкая Каменная стена и ворота** | `turswa` / `tursga` | `gc_obj_usage_hardwall`, `gc_obj_material_building` | Турция и Алжир |

Украина имеет только Частокол; Каменной стены у этой нации нет [^6].

Параметры из кода [^1]:

**Частокол (`ukrwwa`) и ворота (`ukrwga`).** Здоровье стены: 1500 у
общей версии и 2500 у Украины; здоровье ворот: 1000 и 1500
соответственно. Цена — 10 дерева, у Украины — 12. Время постройки
(`buildtime`) — 18 кадров, у Украины — 26. Флаг ворот `bgate`
установлен только у `ukrwga`.

**Каменная стена (`*swa`) и ворота (`*sga`).** Здоровье стены —
50 000, ворот — 32 000. Цена — 50 камня у европейского варианта и
60 камня у русского и турецкого. Время постройки — 288 кадров у
европейского, 640 у русского и 384 у турецкого. Все три варианта ставят
`bwall = True`, `bgate = True` (только у `*sga`), `usage =
gc_obj_usage_hardwall`. У сегмента стены `consume.stone` = 250
для европейского, 200 для русского и 150 для турецкого варианта —
постоянное потребление камня, пока
сегмент стоит [^1].

Конкретные числа по нациям — в
[Здания](../../../reference/03_buildings/README.md).

## 2. Занимаемая площадь и линии стен

Сегмент стены занимает одну клетку. Последовательные сегменты соединяются
без зазоров:

```
[wall][wall][wall]   ← 3 клетки линии
```

Плотная линия становится непрерывным препятствием для поиска пути. После
уничтожения одного сегмента в ней образуется проход, а соседние сегменты
пересоединяются между собой [^13].

### 2.1. Варианты сегментов и места для строителей

Места, с которых крестьяне строят и ремонтируют сегмент, зависят от его
ориентации: прямой участок, угол и соединение требуют разных подходов.
Предусмотрено до 16 таких мест. Нулевой вариант обрабатывается как обычное
здание [^5][^14].

## 3. Постройка стены крестьянами

Игрок выбирает тип стены в интерфейсе и протягивает линию мышью.
До подтверждения интерфейс показывает синие предварительные сегменты [^15].
После щелчка каждый настоящий сегмент появляется с 10 единицами здоровья,
а назначенные крестьяне подходят к свободным местам и постепенно увеличивают
его здоровье и готовность (см.
[Строительство, ремонт и разрушение зданий §3](../economy/building_mechanics.md) о
механике в целом). Обычная стена строится с обычной скоростью здания,
а готовность равна доле текущего здоровья от максимального [^10][^16].

Ресурсы списываются за каждый сегмент отдельно. Отменить постройку
конкретного сегмента до завершения можно стандартной кнопкой:
недостроенный сегмент сносится с возвратом ресурсов по обычной формуле
возврата.

## 4. Захват и снос сегмента

Обычное захватываемое здание меняет владельца, если вражеская пехота
подходит на четыре клетки и рядом нет защитников. Для стен и ворот действует
особое правило [^11]:

1. Игра ищет поблизости любой подходящий вражеский объект, который не
   является зданием. Способность захватывать обычные здания не требуется.
2. Если здоровье сегмента меньше 1/3 от `maxhp`, дальнейшая логика
   пропускается: сегмент уже добивают оружием, без эффекта захвата
   [^12].
3. Иначе при найденном противнике сегмент мгновенно уничтожается.

Поведение одинаковое и для готовой стены, и для недостроенной
(`bbuilt = False`): в обоих случаях достаточно пехотинца врага в
радиусе 4 клеток — сегмент мгновенно сносится. Это «снос», а не
«захват»; владельцем сегмент не становится.

Правило одинаково для стен и ворот.

## 5. Как создаются ворота

Ворота — индивидуальное улучшение одного выбранного сегмента [^7][^17].

| Тип стены | Цена | Где применяется |
|---|---|---|
| **Частокол** | 400 дерева | выбранный сегмент Частокола |
| **Европейская Каменная стена** | 500 камня | выбранный европейский сегмент |
| **Русская Каменная стена** | 500 камня | выбранный русский сегмент |
| **Турецкая Каменная стена** | 500 камня | выбранный турецкий сегмент |

Перед запуском игра проверяет геометрию [^8]. Ворота разрешены, только если:

1. выбранный сегмент **не на конце** кластера (есть соседи слева и
   справа);
2. оба соседа имеют тот же вариант изображения (стена идёт прямо — не угол, не
   T-перекрёсток);
3. все три сегмента **достроены**;
4. в радиусе 1.85 клетки от центра ровно три стены (не больше).

Если хоть одно условие не выполнено, улучшение не запустится. Поэтому ворота
можно ставить только посреди прямого
участка стены минимум из трёх достроенных сегментов.

### 5.1. Что происходит при создании ворот

Игра заменяет центральный сегмент новым объектом ворот, обновляет изображения
его соседей и переносит выделение на новый объект [^9]. Список назначенных
крестьян при этом пуст.

На ближайшем такте специальное правило стены с выполненным улучшением сразу
поднимает здоровье до максимума и помечает объект полностью готовым
[^10][^16][^20]. Поэтому с точки зрения игрока ворота появляются
**мгновенно и с полным здоровьем**.

### 5.2. Почему атакующие могут потерять цель

Прикладной приём, вытекающий из последовательности выше:

- противник атакует конкретный сегмент стены;
- игрок превращает этот сегмент в ворота, если форма стены позволяет;
- старый сегмент заменяется новым объектом;
- атакующие юниты теряют цель — для возобновления атаки противнику
  нужно отдать новую команду на ворота;
- накопленный по старому сегменту урон не переносится: Каменные ворота
  появляются с 32 000 здоровья, частокольные — с 1000–1500. Защитник получает замену
  потрёпанной стены на свежую.

## 6. Стенные башни

Часть наций имеет отдельные стенные башни, которые встают в линию без зазора и
стреляют как обычная Башня. Механика прицеливания и стоимость выстрела
описаны в статье
[Как работают башни](towers.md).

<a id="technical-details"></a>
## 7. Технические подробности

Стена определяется `usage = gc_obj_usage_hardwall` или
`gc_obj_usage_weakwall` и `bwall = True`; ворота дополнительно имеют
`bgate = True` [^1]. Линии хранятся в `gWallSystem` как
`TWallCluster`: тип стены, нация, владелец и массив `TWallCell` [^4].
При смерти сегмента `_unit_OnDeath` вызывает
`gWallSystem.RemoveHandle`, удаляя ячейку и обновляя соседние связи [^13].

`_player_ConstructBuildingList` создаёт сегмент с `bbuilt = False`,
`buildprogress = 0`, `hp = 10`, а `_player_OrderUnitsToBuild` назначает
крестьян [^2][^3]. Для вариантов стены точки берутся из
`gCustomBuildPointsWall[wallvariation]`; при `wallvariation = 0`
используются обычные `gCustomObjPoints` [^5]. Максимум задаёт
`gc_MaxWallBuilderPointsCount = 16`, данные загружаются из
`data/game/var/wallcustom.cfg` [^14].

Проверка сноса проходит через `_misc_CheckCapture`. Для стены поиск
`_unit_SearchCapturersForWall` не требует у кандидата `bcancapture`.
При найденном противнике ветка `bwall` устанавливает `bDie := True` и
`gc_statetag_essential_death`; при `hp < maxhp / 3` эта проверка
пропускается [^11][^12].

Ворота создаёт индивидуальное улучшение
`gc_upg_type_single_buildgate`. `_misc_GetGateBaseSprite` разрешает его
только на прямом достроенном участке из трёх сегментов [^7][^8].
`_player_ConstructGates` заменяет центральный объект и увеличивает
`individual.upglevel` [^9]. Затем `_unit_ControlBuildProgress` выполняет
`if (bwall) and (upglevel > 0) then hp := maxhp`, а
`OnTagStates.essential_none` выставляет `bbuilt := True`,
`buildprogress := 1` [^10][^20]. После первого создания ворот
`gbool_gui_gatefinished` также меняет визуальную обработку взрыва
Каменной стены в `_unit_DoExplosion` [^19].

## 8. Что ещё требует проверки

1. Как именно `costpercent` применяется к сегментам стены при
   массовой стройке: за каждый сегмент или за весь рисунок.
2. Точная скорость постройки сегмента крестьянами в зависимости от
   `wallvariation`: вариант 0 идёт по обычной формуле, остальные —
   по явно заданным точкам `builderPoints`.
3. Поведение в редкой ситуации: улучшение ворот (`buildgate`) запущено, но к
   моменту достройки соседние сегменты уже разрушены — корректно ли
   ворота останутся в кластере или окажутся «висящим» зданием.

---

## Источники

[^1]: `data/scripts/lib/unit.script:2258-2310` — `commonsid+'swa'` /
      `commonsid+'sga'` (каменные стены и ворота, общие для кластеров
`eur` / `rus` / `tur`), `'ukrwwa'` / `'ukrwga'` (частокол и
      деревянные ворота). Здесь устанавливаются `usage`, `bwall`,
`bgate`, `material`, `maxhp`, цены, `consume`.

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
Линии 9280-9286 выбирают источник точек строительства
(`builderPoints`) для стен и ворот:

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
внутренних идентификаторов стен в нацию. `ukrwwa` / `ukrwga` добавляются всем 21
      нациям без условий. Каменная стена идёт через ветки кластеров
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

У Украины ни одна из ветвей `swa` не активируется — каменной
      стены нация не получает.

[^7]: `data/scripts/lib/player.script:1974-1981` — обработчик улучшения
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
      `_misc_GetGateBaseSprite`. Возвращает номер спрайта (14, 15, 16, 17),
      только если все условия про прямой участок и достроенность
      выполнены; иначе `-1` (апгрейд блокируется).

[^9]: `data/scripts/lib/player.script:1583-1645` —
      `_player_ConstructGates`. Линия 1612 создаёт новый объект
      ворот через `_player_ConstructBuildingList`, линия 1615
      инкрементирует `individual.upglevel`, линия 1616
      переписывает `TWallCell(p2).goHnd` на новый дескриптор.

[^10]: `data/scripts/units/building.inc/ontagstates.inc:134-137` —
       обработчик `OnTagStates` зданий, ветка
       `gc_statetag_essential_none`. Здесь объект окончательно
       переходит в состояние готовности:

       ```pascal
       arg_obj.bbuilt := True;
       arg_obj.hp := gPlayer[arg_obj.pl].objBase[arg_obj.cid][arg_obj.id].maxhp;
       arg_obj.buildprogress := 1;
       _unit_AddObjToPlayerCounters(myHnd, True, False, False);
       ```

[^11]: `data/scripts/lib/miscext.script:961-1185` —
       `_misc_CheckCapture`. Линия 975 — `bwall :=
       TObjProp(pobjprop).bwall`. Линии 1003-1006 переключают
поиск потенциальных захватчиков через `_unit_SearchCapturersForWall`
(без требования `bcancapture` у захватчика). Линия 1106 —
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
       При здоровье менее 1/3 максимума ветка захвата полностью пропускается.

[^13]: `data/scripts/lib/unit.script:3954` — вызов
       `gWallSystem.RemoveHandle(pl, goHnd)` при смерти сегмента в
       `_unit_OnDeath`.

[^14]: `data/scripts/lib/country.script:4096-4101` — заполнение
       `gCustomBuildPointsWall[variation].builderCount` и
       `builderPoints[j].x/y` парсером
       `data/game/var/wallcustom.cfg`.
       `gc_MaxWallBuilderPointsCount = 16` — `dmscript.global`.

[^15]: `data/scripts/lib/miscext2.script:933-975` — `_misc_UpdateWall`:
       создаёт «фантомные» объекты на `players-misc` и зажигает синюю
       подсветку при наведении, обновляет `gCanPlaceBuildingWalls`.

[^16]: `data/scripts/units/building.inc/nothing.inc:296-307` —
       обработчик состояния `nothing` (ожидание) для зданий. Пока
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

[^17]: Поле `bindividual := True` у улучшения `buildgate`
    ([`country.script:3944`][^18])
       помечает его как индивидуальный — применяется к одному
       выбранному объекту, а не глобально к нации.

[^18]: `data/scripts/lib/country.script:3942-3973` — регистрация
улучшений `buildgate`:

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
       обломки сегментов каменной стены отключаются до конца матча.

[^20]: `data/scripts/lib/unit.script:6572-6608` —
       `_unit_ControlBuildProgress`. Ключевая ветка для ворот в
       начале процедуры:

       ```pascal
       if (gObjProp[TObj(pobj).cid][TObj(pobj).id].bwall) and (TObj(pobj).individual.upglevel>0) then
          TObj(pobj).hp := gPlayer[TObj(pobj).pl].objbase[TObj(pobj).cid][TObj(pobj).id].maxhp;
       ```

       После присвоения проверяется
       `if hp >= maxhp then _unit_SetTagStates(hnd, gc_statetag_essential_none ...)`
       — это и запускает обработчик `OnTagStates` [^10], в котором
       `bbuilt := True`.
