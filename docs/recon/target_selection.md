# Recon: выбор цели и attack-move

Реверс-инжиниринг функций `_unit_SearchEnemyInCell`, `_unit_SearchEnemyScanCells`,
`_unit_SearchVictimOnProgress` и пути attack-move от GUI до per-tick поиска. Всё
ниже — `data/scripts/lib/unit.script` и сопутствующие файлы.

## TL;DR

- Поиск идёт через **scan-grid** — карта разбита на ячейки `gc_scangrid_size` (~8 тайлов), каждая хранит свой список юнитов по игроку. Сканер обходит прямоугольник ячеек вокруг искателя, в каждой ячейке выбирает одного кандидата и в конце берёт ближайшего.
- Внутри ячейки порядок обхода **рандомизирован** (`rndind = floor(random*count)`), но первый совпадающий по фильтрам и есть выбор. Для немелкой модели одна цель на одну ячейку.
- Для **мили** между ячейками работает балансировка: расстояние умножается на `1 + STO_count × 0.125` (где `STO_count` — сколько юнитов уже идут к этой цели). Чем больше «уже бьющих» — тем целевая ячейка считается «дальше». Это распределяет атакующих, а не сваливает всех на одного.
- Для **рейнджа** балансировки нет — берётся просто ближайший в радиусе.
- Стрелок в движении (`standtime ≤ 0.25 g-сек`) теряет до `gc_obj_maxattackradiusdisp = 3` тайлов эффективного радиуса (`maxRad -= 3 × uniqrnd`). На стоянии радиус возвращается.
- **Attack-move** для не-артиллерии — это ордер `gc_obj_order_type_move` с `info.progress = move_mode_attack`. Юнит идёт к точке и каждые 100 мс ищет цель в полном `searchradius`. При `move_mode_default` поиск ограничен передним конусом 30°.
- **Артиллерия** (`bartprepare = True`) идёт по отдельной ветке `_player_OrderUnitsToAttackPoint` → `gc_obj_order_type_attackpoint`: стреляет по координате, не по конкретной цели; сама точка не меняется при движении врага.

---

## 1. Точки входа

| Функция | Где зовётся | Что отвечает |
|---|---|---|
| `_unit_SearchVictim` (unit.script:5214-5262) | разовый поиск (RunAway, ручная переоценка) | прямой запрос «найди мне цель в кольце `[r0..r1]` от точки» |
| `_unit_SearchVictimOnProgress` (unit.script:5443-5520) | каждый прогресс-тик юнита (~100 мс) | автоатака/реагирование на врага по дороге |
| `_unit_SearchEnemyScanCells` (unit.script:5142-5212) | вызывается обоими выше | обход ячеек scan-grid и выбор минимально-«релевантной» цели |
| `_unit_SearchEnemyInCell` (unit.script:4832-4961) | вызывается из `_unit_SearchEnemyScanCells` | один проход по списку юнитов в одной ячейке |

Цикл: верхний `_unit_SearchVictimOnProgress` определяет режим (`scanmode`) и радиусы из `objprop`, затем зовёт `_unit_SearchEnemyScanCells`, который для каждой ячейки получает кандидата от `_unit_SearchEnemyInCell` и в конце выбирает того, у кого минимальная относительная дистанция.

Scan-grid (`gScanGrid`, `gScanGridUnits`) — это per-player разбиение карты по ячейкам `gc_scangrid_size`. В каждой ячейке хранится список юнитов конкретного игрока и битовая маска присутствия (`fplmask`, `myplmask`, `enemyplmask`). Это позволяет кандидатам отфильтровать чужие ячейки до их открытия и пропускать пустые через быстрый `_misc_ScanGridCellDataCheckNeeded`.

---

## 2. `_unit_SearchEnemyInCell` — выбор внутри одной ячейки

`unit.script:4832-4961`. Возвращает один `goHnd` или 0.

### 2.1 Какие ячейки игроков рассматриваются

```pascal
for plind := 0 to gc_MaxPlayerCount-1 do
   if scanmode <> 1 then
      if (gScanGrid[cellx, celly].fplmask AND enemyplmask AND (1 shl plind)) = 0 then continue
   else  // scanmode = 1 (priest healing)
      if (gScanGrid[cellx, celly].fplmask AND myplmask AND (1 shl plind)) = 0 then continue
```

В обычном режиме обходятся только вражеские игроки. Священник (`scanmode = 1`) — наоборот, только свои.

### 2.2 Случайный стартовый индекс и циклический проход

```pascal
var count : Integer = gScanGrid[cellx, celly].fPlCount[plind];
rndind := floor(random*count);
for i := 0 to count-1 do
begin
   newind := (rndind+i) mod count;
   trgHnd := gScanGridUnits[plind, cellx, celly].Get(newind);
   ...
end;
```

Стартовый индекс — равномерно случайный, далее цикл по всем `count` юнитам игрока в ячейке. Первый прошедший все проверки и есть выбранный (`break(MAIN)` в нужной ветке `scanmode`).

Это значит: **внутри одной ячейки выбор статистически равномерен** среди подходящих кандидатов. Если ячейка содержит четырёх вражеских мушкетеров, у каждого равные шансы стать целью.

### 2.3 Фильтры на кандидата

Минимальные:

- `trgHnd <> 0`
- `trgHnd <> goHnd` (не сам себе)
- visual-state не `gc_statetag_visual_hide`
- essential-state включает `gc_statetag_essential_none` (не в смерти, не в рождении)

Радиус (мили против рейнджа):

```pascal
var maxRad : Float = _unit_GetMaxAttackRadius(goHnd);
var bmelee : Boolean = maxRad <= gc_unit_meleeattackradius;
if not bmelee then
   maxRad := maxRad - gc_obj_maxattackradiusdisp * TObj(pobj).uniqRnd;
```

`gc_unit_meleeattackradius = 0.5 t`, `gc_obj_maxattackradiusdisp = 3 t` (`dmscript.global:113-116`). Стрелок теряет до `3 × uniqrnd` тайлов эффективного радиуса в момент сканирования; этот штраф не зависит от движения здесь — он применяется к выбору цели, а штраф на дальность выстрела при `standtime < 0.25` уже описан в [02_combat.md → Штраф к дальности при движении](../reference/02_combat.md#штраф-к-дальности-при-движении).

Топология:

```pascal
if (_unit_GetRegion(trgHnd) = myRegion) or bFlag then ...
```

Где `bFlag` — для рейнджа: евклидово расстояние до цели ≤ `maxRad + max((goY-trgY)*2, 0)` (бонус с возвышенности). То есть мили требует общей зоны топологии (одна суша / один остров), рейндж — либо общей зоны, либо просто прямой видимости в радиусе.

### 2.4 Диспетчер по `scanmode`

Эта пятёрка веток определяет, **какой именно** валидный кандидат выбирается. Все ветки используют один и тот же ранний выход `break(MAIN)` после нахождения первой совместимой цели:

| `scanmode` | Где включается | Кого выбирает |
|---:|---|---|
| 0 (default) | обычный юнит | первый враг с `material ∈ {body, iron}` либо (если атакующий — здание) `material = wood`. Дополнительный фильтр `bcankill` через `kmask AND mmask`. |
| 1 (priest) | `objprop.bpriest = True` | первый **свой** юнит с `hp < maxhp` (всегда `break(MAIN)` — даже если первый кандидат на полном HP, выходит из цикла). |
| 2 (capture-fallback) | по умолчанию для большинства не-`bcapture` юнитов на progress-tick'е (`unit.script:5491`) | сначала ищет убиваемую цель (как scanmode 0); если не нашёл — отдельным проходом проверяет `bcapture && _unit_TestCapture(trgHnd)` и возвращает захватываемую. |
| 3 (capture-only) | специализированный поиск (например, AI sabotage поверх особых типов целей) | возвращает первую `bcapture` + `_unit_TestCapture` валидную, ничего другого не рассматривает. |
| 4 (AI sabotage) | AI-режим на специальных задачах (`progresswarai.inc`) | агрегирует: проходит ВСЕХ кандидатов и выбирает того, у кого `weapon[0].damage` максимален. То есть AI saboteur целит в самое опасное, а не в ближайшее. |

«Первый» в режимах 0, 1, 2, 3 — это первый по тому самому случайному обходу из §2.2. В режиме 4 кандидаты не обрываются — `Result` обновляется по максимуму `damage`.

---

## 3. `_unit_SearchEnemyScanCells` — обход ячеек

`unit.script:5142-5212`. Возвращает один `goHnd` или 0.

### 3.1 Прямоугольник ячеек

```pascal
_misc_CalcScanCellsMinMax(x1, y1, rx1, cellx, celly, cellxmax, cellymax);
for i := cellx to cellxmax do
for j := celly to cellymax do
   ...
```

`x1, y1` — индекс собственной ячейки искателя в scan-grid; `rx1` — радиус в ячейках, считается на верхнем уровне как `floor(maxsearchdist / gc_scangrid_size) + 1`. То есть охватывается квадрат `(2·rx1+1)²` ячеек — обычно 3×3 или 5×5.

### 3.2 Цикл и две метрики

Внутри цикла:

```pascal
trgHnd := _unit_SearchEnemyInCell(goHnd, i, j, scanmode);
if trgHnd <> 0 then
begin
   distSqr := Sqr(pX-...) + Sqr(pZ-...);
   if (distSqr > minsearchdistSqr) and (distSqr < maxsearchdistSqr) then
   begin
      if distSqr < mindist then mindist := distSqr; minTrgHnd := trgHnd;

      if bmelee then
         relativeDist := distSqr * (1 + TIntegerList(pstolist).GetCount * 0.125)
      else
         relativeDist := distSqr;

      if relativeDist < minRelativeDist then
      begin
         minRelativeDist := relativeDist;
         minRelativeTrgHnd := trgHnd;
         if bmelee and (mindist < cOkDist) then break(MAIN);  // см. §3.4
      end;
   end;
end;
```

Заметные моменты:

- **Кольцо радиусов:** обе границы — `minsearchdist` (мёртвая зона у стрелков) и `maxsearchdist` (прицельный радиус). Стрелок в движении: `maxsearchdistSqr = Sqr(maxsearchdist - 3 × uniqrnd)`. Стоящий стрелок и любой милишник: `maxsearchdistSqr = maxsearchdist²` (`unit.script:5151-5156`).
- **Две метрики:** `minTrgHnd` — просто абсолютно ближайшая цель. `minRelativeTrgHnd` — ближайшая с поправкой на «нагруженность».
- **Возвращается `minRelativeTrgHnd`** (`unit.script:5210`) — то есть всегда вариант с балансировкой; абсолютная `minTrgHnd` рассчитывается, но не используется в Result. Комментарий в коде это и оговаривает: «no help from relative dist cause we choose 1 unit from each cell».

### 3.3 STO-балансировка для милишников

```pascal
var pstolist : Pointer = _misc_GetObjectArgData(trgHnd, gc_argunit_stolist);
relativeDist := distSqr * (1 + TIntegerList(pstolist).GetCount * 0.125);
```

`stolist` — список юнитов, уже «нацеленных» (state-target) на эту цель. `TIntegerList.GetCount` — это не «текущие в радиусе атаки», а **сколько в принципе идут / собираются бить** конкретно эту цель.

Эффект для милишника при выборе:

| `STO_count` | Множитель к `distSqr` | На квадрате расстояния |
|---:|---:|---|
| 0 | ×1.000 | реальное расстояние |
| 1 | ×1.125 | +6.1% от линейной дистанции |
| 4 | ×1.500 | +22.5% |
| 8 | ×2.000 | +41.4% |
| 16 | ×3.000 | +73.2% |

То есть цель, к которой уже бегут восемь твоих, эффективно «отодвигается» на 41% — и второй пикинёр, скорее всего, выберет другого врага в той же ячейке. Это делает строй более «размазанным» по фронту.

Для рейнджа балансировки нет. Все мушкетёры одного отряда обычно валят одну ближайшую цель; распределение получается естественно через рассеяние выстрелов и порядок обхода ячеек, а не через явную метрику.

### 3.4 Ранний выход для мили

```pascal
const cOkDist = (gc_scangrid_size/2) * (gc_scangrid_size/2);
if bmelee and (mindist < cOkDist) then break(MAIN);
```

Если милишник нашёл цель **внутри половины scan-cell** (~4 тайла) **и** улучшил `relativeDist`, цикл по ячейкам обрывается. Дальше искать «более балансировочно подходящего» врага не имеет смысла — текущий уже совсем рядом.

Для рейнджа этого выхода нет — он всегда обходит весь прямоугольник.

---

## 4. `_unit_SearchVictimOnProgress` — периодический поиск

`unit.script:5443-5520`. Это функция, которую state-machine юнита зовёт каждые ~100 мс (`gc_global_TimeProgressUnit`). Она и решает, на кого автоатаковать в текущий момент.

### 4.1 Радиусы

```pascal
searchdist := objprop.searchradius;
minsearchdist := objprop.minattackradius;

if (minsearchdist > gc_unit_meleeattackradius) then
begin
   var goHeight := GetGameObjectPositionYByHandle(goHnd);
   if goHeight < 0 then goHeight := 0;
   searchdist := searchdist + goHeight*2;     // high-ground bonus
end
else
begin
   if (orders[0].itype = gc_obj_order_type_guard) then
      searchdist := MinFloat(searchdist, gc_gameplay_meleeguardmaxsearchdist);
end;
```

- Стрелок на возвышенности: `searchdist += goHeight × 2`. Это уже описано в [02_combat.md → Высокая позиция](../reference/02_combat.md#высокая-позиция-high-ground).
- Милишник в режиме Guard: `searchdist` ограничен `gc_gameplay_meleeguardmaxsearchdist` — то есть охранник не уходит далеко.

### 4.2 Выбор `scanmode`

```pascal
if objprop.bpriest then
   scanmode := 1
else if not (objprop.bcapture or objprop.media = water or objprop.bbuilding) then
   scanmode := 2;
```

Все юниты, которые сами **захватываются** (`bcapture`, например артиллерия), а также водные и здания — идут в `scanmode = 0` (только убивать). Все обычные «не-захватываемые» наземные юниты (пехота, кавалерия) — в `scanmode = 2` (приоритет убить, при провале — захватить).

То есть пешая пехота **по умолчанию пытается захватить** беззащитную пушку или склад, если ничего убиваемого рядом нет.

### 4.3 Диспетчер

```pascal
if media = water then
   trgHnd := _unit_SearchEnemyScanCellsShips(...)
else if (_misc_GetShotPointsCount(goHnd) > 0) then
   trgHnd := _unit_SearchEnemyScanCellsLongRange(...)
else if (rx1 <= 5) and (scanmode <> 1) then
   trgHnd := _unit_SearchEnemyScanCells(...)
else
   trgHnd := _unit_SearchEnemyScanCellsLongRange(...);
```

Три варианта обхода: водные, обычный (5×5 ячеек или меньше), и Long-range с дополнительными «попытками» (`cLongRangeTryNum = 18`) для дальнобойных юнитов с `_misc_GetShotPointsCount > 0` (артиллерия, башни) либо когда радиус сканирования большой. Long-range обходит 18 ячеек и выбирает первую попавшуюся валидную цель — он не ищет минимум.

---

## 5. Attack-move

В Cossacks 3 attack-move выглядит для игрока как одно действие, но в коде это **несколько разных ордеров** в зависимости от типа юнита и того, как игрок навёл прицел.

### 5.1 Для не-артиллерии — `gc_obj_order_type_move` с режимами

`progress` ордера хранит подрежим (`dmscript.global:715-718`):

| Подрежим | Константа | Поведение |
|---|---|---|
| `move_mode_default` | 0 | обычное движение к точке |
| `move_mode_attack` | 1 | «aggressive move»: каждый прогресс-тик зовёт `_unit_SearchVictimOnProgress` и при наличии цели берёт её в текущий ордер `_unit_OrderAttack` |

Дополнительно в `dmscript.global` есть глобальный флаг профиля `gProfile.bsearchenemyinfront` (по умолчанию `True`, `profile.script:30`). Он добавляет **smart search** для `move_mode_default`:

`unit.script:7334-7359`:

```pascal
var bSmartSearch : Boolean = bsearchenemyinfront
                         and (orders[0].itype = move_mode_default)
                         and (movement order is in progress);

if bSmartSearch and trgHnd <> 0 then
begin
   ...
   var angle := VectorAngle(direction_of_travel, direction_to_target);
   if angle < cMinAngle (= 30°) then
      _unit_OrderAttack(...)
end;
```

То есть при включённом smart-search обычное движение (правый клик) тоже ловит врагов, но **только тех, кто в 30° переднем конусе**. Враги по бокам и сзади игнорируются. При aggressive move (`move_mode_attack`) такого ограничения нет — берётся ближайший враг куда угодно.

### 5.2 Для артиллерии — `gc_obj_order_type_attackpoint`

`_player_OrderUnitsToAttackPoint` (`player.script:2447-2481`) обрабатывает только юниты с `objprop.bartprepare = True`. Для каждого:

```pascal
if (gObjProp[cid][id].bartprepare) then
begin
   TObj(pobj).bstandground := False;
   TObj(pobj).bsearchenemy := True;
   if bClearOrders then _unit_ClearOrders(goHnd);
   _unit_OrderAttackPoint(goHnd, trgx, trgz, False, bClearOrders);
end;
```

`bartprepare = True` стоит у `cannon`, `mortar`, `multicannon` (и аналогов) — `unit.script:1724, 1756, 1846, 2240`. Эти юниты:

1. Получают `gc_obj_order_type_attackpoint` с координатами точки.
2. На каждом прогресс-тике в `_unit_TryAttackPoint` (`unit.script:7512-...`) они проверяют, в радиусе ли точка, и стреляют по ней. Сама точка ни от кого не зависит — это просто координата.
3. AoE-урон ловит всех, кто оказался в радиусе взрыва (см. [02_combat.md → AoE damage cap](../reference/02_combat.md#aoe-damage-cap--как-кучкование-защищает)).
4. Из-за `bsearchenemy := True` артиллерия параллельно **сама** выбирает цели через `_unit_SearchVictimOnProgress`, если в её обычном радиусе появился враг — но текущий `attackpoint`-ордер она не сменит, пока не отстреляется.

Отличие от обычного move-attack: артиллерия **стреляет по координате**, даже если цель ушла. Это удобно для подавления / мортирной поддержки за линию видимости — но если враг отбежал, обычная артиллерия с приказом attack-point молотит по пустому месту до новой команды.

### 5.3 Через GUI

GUI шлёт пакет, который `units/global.inc/readorder.inc` разбирает. В readorder есть три точки, ставящие `bsearchenemy := True` (строки 63, 88, 97), все они соответствуют ордерам, после которых юнит должен **сам** искать врагов. Эти соответствуют:

- обычному `move` (без специального флага);
- `move_mode_attack`;
- `attackpoint` (артиллерия).

То есть «нашёл врага — переключился» работает **всегда**, кроме случаев когда `bstandground` явно стоит и `standtime > 0` (см. [02_combat.md → Standground / bartprepare](../reference/02_combat.md#standground--bartprepare--режимы-атаки)).

---

## 6. Что отсюда следует для микро

- **Фокус-стрельба не работает «сам по себе».** Стрелки одного отряда выбирают индивидуально (random внутри ячейки + minRelativeTrgHnd по ячейкам), не по общей цели. Чтобы все 36 мушкетёров стреляли в одного врага, нужно явно дать `OrderAttack` (правый клик по цели), и то даже это не всегда жёстко удерживается, если враг убит или выходит из радиуса.
- **Мили распределяется** по фронту через STO-балансировку: каждый следующий пикинёр в строю учитывает, сколько уже бьёт текущего кандидата, и при равных дистанциях скорее выберет другого. Поэтому строй пикинёров естественно охватывает шеренгу врагов, а не сваливается в одну точку.
- **Кайтинг ограничен `cMinAngle = 30°`.** Если стрелок двигается обычным move (не aggressive) — он замечает врагов только в переднем конусе. Атакующий с тыла или фланга кавалерист не активирует автоатаку у мушкетёра, идущего вперёд по правому клику; нужно либо `move_mode_attack`, либо явный stop.
- **Артиллерия по точке полезна как «area denial».** Поставленная на attack-point пушка не пересчитывает цель — она будет стрелять по координате с заложенным `dispertion`, ловя AoE всех, кто туда заходит.
- **Стрелок в движении эффективно ниже на 3 t** по радиусу обнаружения — `maxRad -= 3 × uniqrnd` пока `standtime < 0.25`. Юнит с высоким `uniqrnd ~ 0.9` теряет сразу 2.7 тайла, низкий `~ 0.1` — 0.3 тайла. То есть в одной шеренге часть мушкетёров «увидит» цель раньше, остальные — позже.
- **AI-saboteur целит в максимальный урон.** В режиме `scanmode = 4` (специальные задачи AI на сапёрные операции) юнит выбирает не ближайшего, а самого опасного врага по `weapon[0].damage`. Это не «обычный» AI; см. [`ai_behavior.md`](ai_behavior.md) §«Открытые вопросы» — частоты использования этого режима в коде помечены.

---

## 7. Открытые вопросы

| # | Вопрос | Где копать |
|---:|---|---|
| 1 | Точное условие, при котором `move_mode_default` приходит вместо `move_mode_attack` от GUI: видимо, обычный правый клик = default, A+клик = attack — но триггер в скриптах не отслеживается, GUI-уровень в C++. | Эмпирически в редакторе, либо чтение GUI-callback'ов в native binary. |
| 2 | Вес 0.125 в STO-балансировке — выбран эмпирически или подобран? | Сравнить с C1 / экспериментально замерить разброс целей у 36 пикинёров против 36 мушкетёров. |
| 3 | `_misc_GetShotPointsCount(goHnd) > 0` как триггер `_unit_SearchEnemyScanCellsLongRange` — у каких именно юнитов это True? Артиллерия точно, башни — наверное; полный список нужно вытащить из определений `objprop.shotpoints`. | `parse_animations.py` или прямой grep по `shotpoints`. |
| 4 | Режим Long-range всегда возвращает «первую найденную» — это значит юниты с дальним прицелом ищут менее точно? Либо поведение перекрывается в native code? | Профилирование AI-сценария с одной мортирой против нескольких целей. |
