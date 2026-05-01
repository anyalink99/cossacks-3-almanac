# Recon: выбор цели и attack-move

Реверс-инжиниринг функций поиска цели и того, как ордер «атакуй до точки»
расходится по разным веткам обработки в зависимости от типа юнита. Все
ссылки на код собраны в разделе [Источники](#источники) в конце документа.

## TL;DR

- Поиск идёт через **scan-grid** [^1] — карта разбита на ячейки фиксированного
  размера, каждая хранит свой список юнитов по игроку. Сканер обходит
  прямоугольник ячеек вокруг искателя, в каждой ячейке выбирает одного
  кандидата и в конце берёт ближайшего.
- Внутри ячейки порядок обхода **рандомизирован**: стартовый индекс задаётся
  как `floor(random × count)`, и первый кандидат, прошедший все фильтры,
  становится выбором [^2].
- Для **юнитов ближнего боя** между ячейками работает балансировка нагрузки:
  расстояние до цели умножается на `1 + STO_count × 0.125`, где `STO_count` —
  сколько союзных юнитов уже идут в эту цель. Чем больше уже бьющих —
  тем целевая ячейка считается «дальше», и второй пикинёр предпочтёт
  другого врага. Это распределяет шеренгу по фронту, а не сваливает её
  на одного противника [^3].
- Для **стрелковых юнитов** балансировки нет — выбирается просто ближайший
  в радиусе.
- Стрелок в движении (когда `standtime ≤ 0.25` игровой секунды) теряет до
  трёх тайлов эффективного радиуса обнаружения — формула
  `maxRad -= 3 × uniqrnd`. На стоянии полный радиус возвращается [^4].
- **Attack-move** для пехоты и кавалерии — это ордер `gc_obj_order_type_move`
  с подрежимом `move_mode_attack`. Юнит идёт к точке и каждые 100 мс
  ищет цель в полном `searchradius`. При обычном `move_mode_default`
  поиск ограничен передним конусом 30° [^5].
- **Артиллерия** с флагом `bartprepare` идёт по отдельной ветке через
  `_player_OrderUnitsToAttackPoint` и получает `gc_obj_order_type_attackpoint` —
  стрельбу по координате, не по конкретной цели. Точка не двигается за
  врагом [^6].

---

## 1. Точки входа

Четыре функции, через которые проходит весь процесс выбора цели:

| Функция | Когда зовётся | Что отвечает |
|---|---|---|
| `_unit_SearchVictim` [^7] | разовый поиск (отход стрелка, ручная переоценка) | прямой запрос «найди мне цель в кольце `[r0..r1]` от точки» |
| `_unit_SearchVictimOnProgress` [^8] | каждый прогресс-тик юнита (~100 мс) | автоатака и реагирование на врагов в процессе движения |
| `_unit_SearchEnemyScanCells` [^1] | вызывается обоими выше | обход ячеек scan-grid и выбор минимально-релевантной цели |
| `_unit_SearchEnemyInCell` [^9] | вызывается из `_unit_SearchEnemyScanCells` | один проход по списку юнитов в одной ячейке |

Цикл такой: `_unit_SearchVictimOnProgress` определяет режим
(`scanmode`) и радиусы из `objprop`, затем вызывает
`_unit_SearchEnemyScanCells`. Тот для каждой ячейки получает кандидата
от `_unit_SearchEnemyInCell` и в конце выбирает того, у кого
минимальная относительная дистанция.

Сам scan-grid (`gScanGrid`, `gScanGridUnits`) — это разбиение карты по
ячейкам фиксированного размера, отдельное для каждого игрока. В каждой
ячейке хранится список присутствующих юнитов и битовая маска
(`fplmask`, `myplmask`, `enemyplmask`). Это позволяет сразу отфильтровать
ячейки, в которых нет противника, и не открывать их вовсе [^10].

---

## 2. `_unit_SearchEnemyInCell` — выбор внутри одной ячейки

Возвращает один хэндл `goHnd` (или 0, если кандидата нет) [^9].

### 2.1 Какие игроки рассматриваются

```pascal
for plind := 0 to gc_MaxPlayerCount-1 do
   if scanmode <> 1 then
      if (gScanGrid[cellx, celly].fplmask AND enemyplmask AND (1 shl plind)) = 0 then continue
   else  // scanmode = 1 (priest healing)
      if (gScanGrid[cellx, celly].fplmask AND myplmask AND (1 shl plind)) = 0 then continue
```

В обычном режиме обходятся только вражеские игроки. У священника
(`scanmode = 1`) — наоборот, только свои.

### 2.2 Случайный стартовый индекс и циклический проход

```pascal
var count : Integer = gScanGrid[cellx, celly].fPlCount[plind];
rndind := floor(random * count);
for i := 0 to count - 1 do
begin
   newind := (rndind + i) mod count;
   trgHnd := gScanGridUnits[plind, cellx, celly].Get(newind);
   ...
end;
```

Стартовый индекс — равномерно случайный, далее идёт циклический проход
по всем `count` юнитам игрока в ячейке. Первый прошедший все проверки
объявляется выбранным — соответствующая ветка делает `break(MAIN)`.

Это значит: **внутри одной ячейки выбор статистически равномерен**
среди подходящих кандидатов. Если в ячейке четыре вражеских мушкетёра,
у каждого равные шансы стать целью.

### 2.3 Фильтры на кандидата

Минимальные:

- `trgHnd <> 0`,
- `trgHnd <> goHnd` (не сам себе),
- visual-state не `gc_statetag_visual_hide`,
- essential-state включает `gc_statetag_essential_none` (юнит не в смерти
  и не в рождении).

Радиус — вычисляется по разному для ближнего и дальнего боя:

```pascal
var maxRad : Float = _unit_GetMaxAttackRadius(goHnd);
var bmelee : Boolean = maxRad <= gc_unit_meleeattackradius;
if not bmelee then
   maxRad := maxRad - gc_obj_maxattackradiusdisp * TObj(pobj).uniqRnd;
```

Константы: `gc_unit_meleeattackradius = 0.5` тайла,
`gc_obj_maxattackradiusdisp = 3` тайла [^11]. Стрелковый юнит
теряет до `3 × uniqrnd` тайлов эффективного радиуса в момент сканирования.
Этот штраф применяется именно к выбору цели; штраф на дальность
выстрела при `standtime < 0.25` — отдельная история, описана
в [`02_combat.md → Штраф к дальности при движении`](../reference/02_combat.md#штраф-к-дальности-при-движении).

Топология:

```pascal
if (_unit_GetRegion(trgHnd) = myRegion) or bFlag then ...
```

`bFlag` определён только для дальнего боя — это евклидово расстояние до
цели, не превышающее `maxRad + max((goY - trgY) × 2, 0)` (с бонусом за
возвышенность). То есть рукопашник требует общей зоны топологии
(одна суша, один остров), а стрелок может пробить либо общую зону,
либо просто прямую видимость в радиусе.

### 2.4 Диспетчер по `scanmode`

Этот блок определяет, какой именно валидный кандидат выбирается.
Все ветки используют ранний выход `break(MAIN)` после нахождения первой
совместимой цели:

| `scanmode` | Где включается | Кого выбирает |
|---:|---|---|
| 0 (default) | обычный юнит | первый враг с `material ∈ {body, iron}` либо (если атакующий — здание) `material = wood`. Дополнительный фильтр `bcankill` через `kmask AND mmask`. |
| 1 (priest) | у юнита `objprop.bpriest = True` | первый **свой** юнит с `hp < maxhp`. Если первый кандидат на полном HP — функция выходит из цикла без результата. |
| 2 (capture-fallback) | по умолчанию для большинства не-`bcapture` юнитов на progress-tick'е | сначала ищет убиваемую цель (как scanmode 0); если не нашёл — отдельным проходом проверяет `bcapture && _unit_TestCapture(trgHnd)` и возвращает захватываемую. |
| 3 (capture-only) | специализированный поиск (например, AI на задачах захвата) | возвращает первую `bcapture` + `_unit_TestCapture` валидную, ничего другого не рассматривает. |
| 4 (AI sabotage) | AI-режим на специальных задачах | агрегирует: проходит ВСЕХ кандидатов и выбирает того, у кого `weapon[0].damage` максимален. То есть AI-диверсант целит в самое опасное, а не в ближайшее. |

«Первый» в режимах 0, 1, 2, 3 — это первый по тому самому случайному
обходу из §2.2. В режиме 4 цикл не обрывается ранним выходом —
`Result` обновляется по максимуму `damage`.

---

## 3. `_unit_SearchEnemyScanCells` — обход ячеек

Возвращает один хэндл `goHnd` или 0 [^1].

### 3.1 Прямоугольник ячеек

```pascal
_misc_CalcScanCellsMinMax(x1, y1, rx1, cellx, celly, cellxmax, cellymax);
for i := cellx to cellxmax do
for j := celly to cellymax do
   ...
```

`x1`, `y1` — индекс собственной ячейки искателя в scan-grid; `rx1` —
радиус в ячейках, считается на верхнем уровне как
`floor(maxsearchdist / gc_scangrid_size) + 1`. То есть охватывается
квадрат `(2 × rx1 + 1)²` ячеек — обычно 3×3 или 5×5.

### 3.2 Цикл и две метрики

Внутри цикла:

```pascal
trgHnd := _unit_SearchEnemyInCell(goHnd, i, j, scanmode);
if trgHnd <> 0 then
begin
   distSqr := Sqr(pX - ...) + Sqr(pZ - ...);
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

- **Кольцо радиусов.** Обе границы — `minsearchdist` (мёртвая зона
  у стрелков, в неё попадает противник вплотную) и `maxsearchdist`
  (внешний радиус прицельного выстрела). Стрелок в движении считает
  по `Sqr(maxsearchdist - 3 × uniqrnd)`. Стоящий стрелок и любой
  рукопашник — по `maxsearchdist²` [^12].
- **Две параллельные метрики.** `minTrgHnd` — просто абсолютно
  ближайшая цель. `minRelativeTrgHnd` — ближайшая с поправкой на
  «нагруженность» (см. §3.3).
- **Возвращается `minRelativeTrgHnd`** — то есть всегда вариант
  с балансировкой; абсолютная `minTrgHnd` рассчитывается, но в
  результате не используется. Авторский комментарий это прямо
  оговаривает: *no help from relative dist cause we choose 1 unit
  from each cell* [^13].

### 3.3 Балансировка нагрузки для рукопашников

```pascal
var pstolist : Pointer = _misc_GetObjectArgData(trgHnd, gc_argunit_stolist);
relativeDist := distSqr * (1 + TIntegerList(pstolist).GetCount * 0.125);
```

`stolist` — список юнитов, у которых state-target указывает на эту цель.
То есть это не «текущие в радиусе атаки», а **сколько в принципе идут
или собираются бить** конкретно этого противника.

Эффект для рукопашника при выборе:

| `STO_count` | Множитель к `distSqr` | На квадрате расстояния |
|---:|---:|---|
| 0 | ×1.000 | реальная дистанция |
| 1 | ×1.125 | +6.1% линейной дистанции |
| 4 | ×1.500 | +22.5% |
| 8 | ×2.000 | +41.4% |
| 16 | ×3.000 | +73.2% |

Цель, к которой уже бегут восемь твоих, эффективно «отодвигается»
на 41% — и второй пикинёр, скорее всего, выберет другого врага в той же
ячейке. Это делает строй более размазанным по фронту.

Для стрелков балансировки нет. Все мушкетёры одного отряда обычно
валят одну ближайшую цель; распределение получается естественно —
через рассеяние выстрелов и порядок обхода ячеек, а не через явную
метрику.

### 3.4 Ранний выход для рукопашников

```pascal
const cOkDist = (gc_scangrid_size / 2) * (gc_scangrid_size / 2);
if bmelee and (mindist < cOkDist) then break(MAIN);
```

Если рукопашник нашёл цель **внутри половины scan-cell** (~4 тайла)
и улучшил `relativeDist`, цикл по ячейкам обрывается. Дальше искать
«более балансировочно подходящего» противника не имеет смысла —
текущий и так совсем рядом.

Для стрелков такого выхода нет — они всегда обходят весь прямоугольник.

---

## 4. `_unit_SearchVictimOnProgress` — периодический поиск

Это функция, которую state-machine юнита зовёт каждые ~100 мс
(`gc_global_TimeProgressUnit`). Она и решает, на кого автоатаковать
в текущий момент [^8].

### 4.1 Радиусы

```pascal
searchdist := objprop.searchradius;
minsearchdist := objprop.minattackradius;

if (minsearchdist > gc_unit_meleeattackradius) then
begin
   var goHeight := GetGameObjectPositionYByHandle(goHnd);
   if goHeight < 0 then goHeight := 0;
   searchdist := searchdist + goHeight * 2;     // high-ground bonus
end
else
begin
   if (orders[0].itype = gc_obj_order_type_guard) then
      searchdist := MinFloat(searchdist, gc_gameplay_meleeguardmaxsearchdist);
end;
```

- Стрелок на возвышенности получает `searchdist += goHeight × 2`. Это
  уже описано в [`02_combat.md → Высокая позиция`](../reference/02_combat.md#высокая-позиция-high-ground).
- Рукопашник в режиме Guard: `searchdist` ограничен сверху константой
  `gc_gameplay_meleeguardmaxsearchdist` — охранник не уходит далеко.

### 4.2 Выбор `scanmode`

```pascal
if objprop.bpriest then
   scanmode := 1
else if not (objprop.bcapture or objprop.media = water or objprop.bbuilding) then
   scanmode := 2;
```

Все юниты, которые сами захватываются (`bcapture` — например,
артиллерия), а также водные и здания — идут в `scanmode = 0` (только
убивать). Все обычные не-захватываемые наземные юниты (пехота,
кавалерия) — в `scanmode = 2`: приоритет убить, при провале — захватить.

То есть пехотный юнит **по умолчанию пытается захватить** беззащитную
пушку или склад, если ничего убиваемого рядом нет.

### 4.3 Диспетчер обхода

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

Три варианта обхода: для водных юнитов, обычный (5×5 ячеек или меньше)
и Long-range с дополнительными попытками (`cLongRangeTryNum = 18`)
для дальнобойных юнитов с `_misc_GetShotPointsCount > 0` (артиллерия,
башни) либо когда радиус сканирования большой. Long-range обходит 18
ячеек и выбирает первую попавшуюся валидную цель — он не ищет минимум.

---

## 5. Attack-move

В Cossacks 3 attack-move выглядит для игрока как одно действие, но
в коде — это **несколько разных ордеров** в зависимости от типа юнита
и того, как игрок навёл прицел.

### 5.1 Для пехоты и кавалерии — `gc_obj_order_type_move` с подрежимами

`progress` ордера хранит подрежим [^14]:

| Подрежим | Константа | Поведение |
|---|---|---|
| `move_mode_default` | 0 | обычное движение к точке |
| `move_mode_attack` | 1 | aggressive move: каждый прогресс-тик зовёт `_unit_SearchVictimOnProgress` и при наличии цели берёт её в текущий ордер `_unit_OrderAttack` |

Дополнительно есть глобальный флаг профиля
`gProfile.bsearchenemyinfront` (по умолчанию `True` [^15]). Он добавляет
**умный поиск** для `move_mode_default` [^16]:

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

То есть при включённом умном поиске обычное движение (правый клик)
тоже ловит врагов, но **только тех, кто в 30°-конусе впереди**. Враги
по бокам и сзади игнорируются. При aggressive move
(`move_mode_attack`) такого ограничения нет — берётся ближайший враг
куда угодно.

### 5.2 Для артиллерии — `gc_obj_order_type_attackpoint`

`_player_OrderUnitsToAttackPoint` обрабатывает только юниты с
`objprop.bartprepare = True` [^6]:

```pascal
if (gObjProp[cid][id].bartprepare) then
begin
   TObj(pobj).bstandground := False;
   TObj(pobj).bsearchenemy := True;
   if bClearOrders then _unit_ClearOrders(goHnd);
   _unit_OrderAttackPoint(goHnd, trgx, trgz, False, bClearOrders);
end;
```

`bartprepare = True` стоит у `cannon`, `howitzer`, `framegun` (точные
ветки в скрипте — см. [^17]). Эти юниты:

1. Получают `gc_obj_order_type_attackpoint` с координатами точки.
2. На каждом прогресс-тике в `_unit_TryAttackPoint` [^18] проверяют,
   находится ли точка в радиусе, и стреляют по ней. Точка ни от кого
   не зависит — это просто координата.
3. AoE-урон ловит всех, кто оказался в радиусе взрыва (см.
   [`02_combat.md → AoE damage cap`](../reference/02_combat.md#aoe-damage-cap--как-кучкование-защищает)).
4. Из-за `bsearchenemy := True` артиллерия параллельно сама выбирает
   цели через `_unit_SearchVictimOnProgress`, если в её обычном радиусе
   появился противник, — но текущий `attackpoint`-ордер не сменит,
   пока не отстреляется.

Отличие от move-attack: артиллерия **стреляет по координате**, даже
если цель ушла. Это удобно для подавления и мортирной поддержки за
линию видимости. Но если враг отбежал, обычная артиллерия с приказом
attack-point молотит по пустому месту до новой команды.

### 5.3 Через GUI

GUI шлёт пакет, который обрабатывает `units/global.inc/readorder.inc`.
В нём есть три точки, которые ставят `bsearchenemy := True` [^19],
и все они соответствуют ордерам, после которых юнит должен сам искать
противника:

- обычное движение `move`,
- `move_mode_attack`,
- `attackpoint` (артиллерия).

То есть «нашёл врага — переключился» работает **всегда**, кроме
случаев, когда `bstandground` явно стоит и `standtime > 0`. Это поведение
описано в [`02_combat.md → Standground / bartprepare`](../reference/02_combat.md#standground--bartprepare--режимы-атаки).

---

## 6. Что отсюда следует для микроконтроля

- **Фокус-стрельба сама по себе не работает.** Стрелки одного отряда
  выбирают цели индивидуально — random внутри ячейки плюс
  `minRelativeTrgHnd` по ячейкам, — а не координируют общую цель.
  Чтобы все 36 мушкетёров стреляли в одного врага, нужно явно дать
  `OrderAttack` (правый клик по цели), и даже это удерживается
  не жёстко: после убийства или ухода врага из радиуса каждый юнит
  переоценит самостоятельно.
- **Рукопашка распределяется** по фронту через STO-балансировку:
  каждый следующий пикинёр в строю учитывает, сколько уже бьёт
  текущего кандидата, и при равных дистанциях скорее выберет
  другого. Поэтому строй пикинёров естественно охватывает шеренгу
  врагов, а не сваливается в одну точку.
- **Стрельба с отходом** ограничена углом `cMinAngle = 30°`. Если
  стрелок двигается обычным move (не aggressive) — он замечает
  врагов только в переднем конусе. Кавалерист, заходящий с тыла или
  фланга, не активирует автоатаку у мушкетёра, идущего вперёд по
  правому клику. Нужно либо `move_mode_attack`, либо явный stop.
- **Артиллерия по точке полезна как запрет зоны.** Поставленная на
  attack-point пушка не пересчитывает цель — она будет стрелять по
  координате с заложенным `dispertion`, накрывая AoE всех, кто туда
  заходит.
- **Стрелок в движении эффективно «ниже» на 3 тайла** по радиусу
  обнаружения: `maxRad -= 3 × uniqrnd` пока `standtime < 0.25`.
  Юнит с высоким `uniqrnd ≈ 0.9` теряет сразу 2.7 тайла, низкий
  `≈ 0.1` — 0.3 тайла. То есть в одной шеренге часть мушкетёров
  «увидит» цель раньше, остальные — позже.
- **AI-диверсант целит в максимальный урон.** В режиме `scanmode = 4`
  (специальные задачи AI на саботажные операции) юнит выбирает
  не ближайшего, а самого опасного врага по `weapon[0].damage`. Это
  не «обычный» AI; см. [`ai_behavior.md`](ai_behavior.md), раздел
  «Открытые вопросы».

---

## 7. Открытые вопросы

| # | Вопрос | Где копать |
|---:|---|---|
| 1 | Точное условие, при котором `move_mode_default` приходит вместо `move_mode_attack` от GUI: видимо, обычный правый клик = default, A + клик = attack — но в скриптах это условие не отслеживается, оно решается GUI-слоем в C++. | Эмпирически в редакторе, либо чтение GUI-callback'ов в native binary. |
| 2 | Вес 0.125 в STO-балансировке — выбран эмпирически или подобран? | Сравнить с C1 либо экспериментально замерить разброс целей у 36 пикинёров против 36 мушкетёров. |
| 3 | `_misc_GetShotPointsCount(goHnd) > 0` как условие выбора `_unit_SearchEnemyScanCellsLongRange`: у каких юнитов это True? Артиллерия — точно, башни — наверное; полный список нужно вытащить из определений `objprop.shotpoints`. | `parse_animations.py` или прямой grep по `shotpoints`. |
| 4 | Long-range всегда возвращает «первую найденную» — это значит юниты с дальним прицелом ищут менее точно? Либо поведение перекрывается в native code? | Профилирование AI-сценария с одной мортирой против нескольких целей. |

---

## Источники

Все ссылки относительно `data/scripts/` в установке Cossacks 3.

[^1]: `_unit_SearchEnemyScanCells` — `lib/unit.script:5142-5212`.

[^2]: Случайный стартовый индекс и циклический проход по списку юнитов в ячейке — `lib/unit.script:4872-4877`.

[^3]: STO-балансировка для рукопашников — `lib/unit.script:5188-5198`.

[^4]: Штраф к радиусу для движущегося стрелка — `lib/unit.script:5151-5156`.

[^5]: Подрежимы движения `move_mode_default` / `move_mode_attack` — `dmscript.global:715-718`.

[^6]: `_player_OrderUnitsToAttackPoint` — `lib/player.script:2447-2481`.

[^7]: `_unit_SearchVictim` — `lib/unit.script:5214-5262`.

[^8]: `_unit_SearchVictimOnProgress` — `lib/unit.script:5443-5520`.

[^9]: `_unit_SearchEnemyInCell` — `lib/unit.script:4832-4961`.

[^10]: Битовые маски игроков на ячейке (`fplmask`, `myplmask`, `enemyplmask`) — `lib/unit.script:4842-4852`.

[^11]: Константы радиуса — `dmscript.global:113-116` (`gc_unit_meleeattackradius = 0.5 t`, `gc_obj_maxattackradiusdisp = 3 t`).

[^12]: Расчёт `maxsearchdistSqr` — `lib/unit.script:5151-5156`.

[^13]: Возврат `minRelativeTrgHnd` и комментарий автора — `lib/unit.script:5210`.

[^14]: Константы подрежимов движения — `dmscript.global:715-718`.

[^15]: Дефолт флага `bsearchenemyinfront = True` — `lib/profile.script:30`.

[^16]: Умный поиск (фронтальный конус 30°) — `lib/unit.script:7334-7359`.

[^17]: `objprop.bartprepare := True` — `lib/unit.script:1724, 1756, 1846, 2240` (cannon, howitzer-проектив, framegun, tower built-in cannon).

[^18]: `_unit_TryAttackPoint` — `lib/unit.script:7512` и далее.

[^19]: Обработчик ордеров с `bsearchenemy := True` — `units/global.inc/readorder.inc:63, 88, 97`.
