# Recon: выбор цели и attack-move

Реверс-инжиниринг функций поиска цели и того, как ордер «атакуй до точки»
расходится по разным веткам обработки в зависимости от типа юнита. Все
ссылки на код и сами Pascal-блоки собраны в разделе [Источники](#источники)
в конце документа.

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
  трёх тайлов эффективного радиуса обнаружения по формуле
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

Цикл по всем `gc_MaxPlayerCount` игрокам, фильтр по битовой маске
присутствия в ячейке и по принадлежности (свой / враг). В обычном режиме
обходятся только вражеские игроки. У священника (`scanmode = 1`) —
наоборот, только свои [^11].

### 2.2 Случайный стартовый индекс и циклический проход

Стартовый индекс задаётся как `floor(random × count)`, где `count` —
число юнитов игрока в ячейке. Далее идёт циклический проход по всем
`count` элементам, начиная с этого случайного индекса (по модулю
`count`). Первый кандидат, прошедший все проверки, объявляется
выбранным — соответствующая ветка делает `break(MAIN)` [^2].

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

Радиус — вычисляется по разному для ближнего и дальнего боя. Сначала
определяется тип юнита по флагу `bmelee` (он истинен, если максимальный
радиус атаки не превышает `gc_unit_meleeattackradius`). Для стрелков из
радиуса вычитается случайный штраф `gc_obj_maxattackradiusdisp × uniqrnd`,
для рукопашников — нет [^12].

Константы: `gc_unit_meleeattackradius = 0.5` тайла,
`gc_obj_maxattackradiusdisp = 3` тайла [^13]. Стрелковый юнит
теряет до `3 × uniqrnd` тайлов эффективного радиуса в момент сканирования.
Этот штраф применяется именно к выбору цели; штраф на дальность
выстрела при `standtime < 0.25` — отдельная история, описана в
[`ranged_units_behavior.md` §4](ranged_units_behavior.md#4-штраф-к-дальности-при-движении-standtime).

Топологическая проверка: цель валидна, если она в той же зоне топологии,
что и атакующий, или (для дальнего боя) если дистанция в евклидовой норме
не превышает `maxRad + max((goY - trgY) × 2, 0)` (с бонусом за
возвышенность) [^14]. То есть рукопашник требует общей зоны (одна суша,
один остров), а стрелок может пробить либо общую зону, либо просто
прямую видимость в радиусе.

### 2.4 Диспетчер по `scanmode`

Этот блок определяет, какой именно валидный кандидат выбирается.
Все ветки используют ранний выход `break(MAIN)` после нахождения первой
совместимой цели [^15]:

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

Через `_misc_CalcScanCellsMinMax` вычисляются индексы границ ячеек
вокруг позиции искателя; затем двойной цикл `i × j` по этому
прямоугольнику. `x1`, `y1` — индекс собственной ячейки искателя в
scan-grid; `rx1` — радиус в ячейках, считается на верхнем уровне
как `floor(maxsearchdist / gc_scangrid_size) + 1`. То есть охватывается
квадрат `(2 × rx1 + 1)²` ячеек — обычно 3×3 или 5×5 [^16].

### 3.2 Цикл и две метрики

Для каждой ячейки `_unit_SearchEnemyInCell` возвращает одного кандидата.
Дальше его проверяют на принадлежность кольцу радиусов
(`minsearchdistSqr < distSqr < maxsearchdistSqr`) и обновляют сразу
**две метрики**: абсолютную минимальную дистанцию `minTrgHnd` и
относительную минимальную `minRelativeTrgHnd` (с учётом нагрузки на
цель). Возвращается именно `minRelativeTrgHnd` [^17].

Заметные моменты:

- **Кольцо радиусов.** Обе границы — `minsearchdist` (мёртвая зона
  у стрелков, в неё попадает противник вплотную) и `maxsearchdist`
  (внешний радиус прицельного выстрела). Стрелок в движении считает
  по `Sqr(maxsearchdist - 3 × uniqrnd)`. Стоящий стрелок и любой
  рукопашник — по `maxsearchdist²` [^4].
- **Две параллельные метрики.** `minTrgHnd` — просто абсолютно
  ближайшая цель. `minRelativeTrgHnd` — ближайшая с поправкой на
  «нагруженность» (см. §3.3).
- **Возвращается `minRelativeTrgHnd`** — то есть всегда вариант
  с балансировкой; абсолютная `minTrgHnd` рассчитывается, но в
  результате не используется. Авторский комментарий это прямо
  оговаривает: *no help from relative dist cause we choose 1 unit
  from each cell* [^18].

### 3.3 Балансировка нагрузки для рукопашников

`stolist` — список юнитов, у которых state-target указывает на эту цель.
То есть это не «текущие в радиусе атаки», а **сколько в принципе идут
или собираются бить** конкретно этого противника. Для рукопашников
относительная дистанция считается как `distSqr × (1 + stolist.GetCount × 0.125)`,
то есть «загруженная» цель эффективно отодвигается [^3].

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

Если рукопашник нашёл цель **внутри половины scan-cell** (~4 тайла)
и улучшил `relativeDist`, цикл по ячейкам обрывается. Дальше искать
«более балансировочно подходящего» противника не имеет смысла —
текущий и так совсем рядом. Константа `cOkDist = (gc_scangrid_size / 2)²`
вычисляется внутри функции [^19].

Для стрелков такого выхода нет — они всегда обходят весь прямоугольник.

---

## 4. `_unit_SearchVictimOnProgress` — периодический поиск

Это функция, которую state-machine юнита зовёт каждые ~100 мс
(`gc_global_TimeProgressUnit`). Она и решает, на кого автоатаковать
в текущий момент [^8].

### 4.1 Радиусы

Базовые значения берутся из `objprop`: `searchdist = objprop.searchradius`,
`minsearchdist = objprop.minattackradius`. К стрелку (когда
`minsearchdist > gc_unit_meleeattackradius`) добавляется бонус с
возвышенности — `searchdist += goHeight × 2`, если `goHeight > 0`.
Для рукопашника в режиме Guard `searchdist` ограничен сверху
константой `gc_gameplay_meleeguardmaxsearchdist` — охранник не уходит
далеко [^20].

Бонус с возвышенности подробнее — в
[`ranged_units_behavior.md` §7](ranged_units_behavior.md#7-high-ground--бонус-с-возвышенности).

### 4.2 Выбор `scanmode`

Священник идёт в `scanmode = 1`. Все юниты, которые сами захватываются
(`bcapture` — например, артиллерия), а также водные и здания — в
`scanmode = 0` (только убивать). Все остальные не-захватываемые
наземные юниты (пехота, кавалерия) — в `scanmode = 2`: приоритет убить,
при провале — захватить [^21].

То есть пехотный юнит **по умолчанию пытается захватить** беззащитную
пушку или склад, если ничего убиваемого рядом нет.

### 4.3 Диспетчер обхода

В зависимости от среды и числа ячеек выбирается одна из трёх процедур
обхода: для водных юнитов — `_unit_SearchEnemyScanCellsShips`, для
дальнобойных (`_misc_GetShotPointsCount > 0`, артиллерия и башни) или
большого радиуса — `_unit_SearchEnemyScanCellsLongRange`, для
обычных — `_unit_SearchEnemyScanCells` [^22].

Long-range обходит до 18 ячеек (`cLongRangeTryNum = 18`) и выбирает
**первую попавшуюся** валидную цель — он не ищет минимум.

---

## 5. Attack-move

В Cossacks 3 attack-move выглядит для игрока как одно действие, но
в коде — это **несколько разных ордеров** в зависимости от типа юнита
и того, как игрок навёл прицел.

### 5.1 Для пехоты и кавалерии — `gc_obj_order_type_move` с подрежимами

`progress` ордера хранит подрежим [^5]:

| Подрежим | Константа | Поведение |
|---|---|---|
| `move_mode_default` | 0 | обычное движение к точке |
| `move_mode_attack` | 1 | aggressive move: каждый прогресс-тик зовёт `_unit_SearchVictimOnProgress` и при наличии цели берёт её в текущий ордер `_unit_OrderAttack` |

Дополнительно есть глобальный флаг профиля
`gProfile.bsearchenemyinfront` (по умолчанию `True` [^23]). Он добавляет
**умный поиск** для `move_mode_default`: если найдена потенциальная
цель и угол между направлением движения и направлением на неё не
превышает `cMinAngle = 30°`, юнит автоматически разворачивается в
атаку [^24].

То есть при включённом умном поиске обычное движение (правый клик)
тоже ловит врагов, но **только тех, кто в 30°-конусе впереди**. Враги
по бокам и сзади игнорируются. При aggressive move
(`move_mode_attack`) такого ограничения нет — берётся ближайший враг
куда угодно.

### 5.2 Для артиллерии — `gc_obj_order_type_attackpoint`

`_player_OrderUnitsToAttackPoint` обрабатывает только юниты с
`objprop.bartprepare = True`. Для каждого такого юнита снимается
`bstandground`, выставляется `bsearchenemy`, опционально очищаются
прежние ордера и выдаётся `_unit_OrderAttackPoint` с координатами [^6].

`bartprepare = True` стоит у `cannon`, `howitzer`, `framegun` (точные
ветки в скрипте — см. [^25]). Эти юниты:

1. Получают `gc_obj_order_type_attackpoint` с координатами точки.
2. На каждом прогресс-тике в `_unit_TryAttackPoint` [^26] проверяют,
   находится ли точка в радиусе, и стреляют по ней. Точка ни от кого
   не зависит — это просто координата.
3. AoE-урон ловит всех, кто оказался в радиусе взрыва (см.
   [`combat_damage_pipeline.md` §6.5](combat_damage_pipeline.md)).
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
В нём есть три точки, которые ставят `bsearchenemy := True` [^27],
и все они соответствуют ордерам, после которых юнит должен сам искать
противника:

- обычное движение `move`,
- `move_mode_attack`,
- `attackpoint` (артиллерия).

То есть «нашёл врага — переключился» работает **всегда**, кроме
случаев, когда `bstandground` явно стоит и `standtime > 0`. Это поведение
описано в
[`ranged_units_behavior.md` §1-2](ranged_units_behavior.md#1-standground-vs-обычный-режим).

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
  не «обычный» AI; см. [`ai_behavior.md`](../../systems/ai_behavior.md), раздел
  «Открытые вопросы».

---

## 7. Лечение священниками — `bpriest`

Священники (`priest`, `pope`, `mullah`, `padre`) — особый класс
юнитов с `bpriest = True`. Алгоритм выбора цели — режим
`scanmode = 1` (см. §2.1): сканируются **только свои** игроки, и
юнит выбирается по правилу «первый встреченный с `hp < maxhp`»;
если первый кандидат уже на полном HP — выход без результата.

«Атака» священника обрабатывается отдельной веткой
`_misc_DoDamage` (см. [`combat_damage_pipeline.md` §5](combat_damage_pipeline.md))
с `weapon.kind = gc_obj_weapon_kind_heal` [^32]. Формула:

```
target.hp += weapon.damage              # БЕЗ shield, БЕЗ protection
target.hp := min(target.hp, target.maxhp)
```

`heal pause = 0` — священник лечит каждый цикл анимации
(~0.7 г-сек), пока цель не выйдет на полный HP.

| Юнит | heal/удар | дальность (px / тайлы) | Где доступен |
|---|---:|---|---|
| Priest | 20 | 0–400 / 7.5 | большинство европейских наций |
| Pope | 25 | 0–350 / 6.6 | Папская область / Венеция |
| Mullah | 15 | 0–500 / **9.4** | Турция / Алжир (самая большая дальность) |
| Padre | 30 | 0–400 / 7.5 | Испания / Португалия (самое сильное лечение) |

### 7.1. Стратегические свойства

- **Лечение игнорирует броню и щит** — восстанавливает HP на
  полное `weapon.damage` независимо от защиты цели.
- **Несколько священников лечат одну цель параллельно** —
  рейтер с 282 HP лечится 4 священниками = +80 HP / цикл ≈ 115
  HP / реальную секунду.
- **Mullah имеет самую большую дальность** — лечит из второй
  линии, недосягаем для ближнего боя.
- **Padre самый эффективный** (30 / удар) — испано-португальская
  армия очень живуча.
- Священники сами уязвимы (низкий HP, нет брони) — приоритетная
  цель для рейдов.

### 7.2. Конверсии нет

В отличие от AoE2-style миссионеров, в Cossacks 3 священник —
**только лекарь**. Никакой конверсии вражеских юнитов в свои в
скриптах нет. См. также [`capture_mechanics.md`](../economy/capture_mechanics.md)
§7.

---

## 8. Реакция отряда на полученный удар

Любой не-артиллерийский юнит, получивший урон в `_misc_DoDamage`,
переключает свой `TSquad.fAgressive := True` и обновляет
`fLastBattleTime` [^33]. Эффект: **один поражающий выстрел / удар
по любому юниту отряда переводит весь отряд в боевой режим** —
все юниты начинают активно искать врага и контратаковать.

### 8.1. Стратегические следствия

- **Поклёвывание ИИ одним лучником** активирует **весь** отряд
  ИИ. Можно использовать как отвлечение: один разведчик дразнит
  армию, остальные обходят с фланга.
- **Артиллерия ИИ — исключение** (особый случай в коде): не
  переключается в `fAgressive` от удара, продолжает работать в
  своём приказе.
- **Скрытая собирательская деятельность** (рейд крестьянами в
  тыл) — **не атаковать** вообще, иначе вся армия зашевелится.

См. также [`combat_damage_pipeline.md` §8](combat_damage_pipeline.md)
о том же эффекте со стороны формулы урона.

---

## 9. Рассеяние и точность выстрела

Каждый выстрел снаряда рассеивается относительно цели по
формуле в `_weapon_CalcShotDispertion` [^34]:

```
maxdisp = dist × disp × 0.0267         # в тайлах
shot_x  = target_x + (1 − random × 2) × maxdisp
shot_z  = target_z + (1 − random × 2) × maxdisp
```

`dist` — дистанция до цели (тайлы), `disp` — `weapon.dispertion`
(тайлы, после `_misc_PixelsToTiles`). **Чем дальше — тем больше
рассеяние**, линейно.

### 9.1. Базовые значения dispertion

| Оружие | dispertion (px / тайлы) | На 15 t отклонение |
|---|---:|---:|
| Стрелец (SHOTMUSKET, base) | 200 / 3.75 | ±1.50 t |
| Лучник (STRELA) | 175 / 3.28 | ±1.31 t |
| Лучник (OSTRELA fire) | 200 / 3.75 | ±1.50 t |
| Мушкетёр base | 250 / 4.69 | ±1.88 t |
| Пушка (PPOINTT) | ~250 / 4.69 | ±1.88 t |
| Башня (PPOINTTTOW) | ~100 / 1.88 | ±0.75 t |
| Яхта / галера (PPOINTTKOR) | 25 / 0.47 | ±0.19 t |

### 9.2. Шанс попасть в юнит размером 1×1 тайл на дистанции `d`

- Если `2 × maxdisp ≤ 1` → ~100 % попадание.
- Если `2 × maxdisp > 1` → шанс ≈ `1 / (2 × maxdisp)` попасть в
  нужный квадрат.

Пример: мушкетёр (`disp = 3.75`) на 15 тайлах →
`maxdisp = 1.50`, окно ±1.50 = 3.00 → шанс попасть в цель 1×1 ≈
**1/3 = 33 %** одним выстрелом. То есть **TTK для дальних пуль и
стрел в идеализированных матрицах занижен в 3 раза**.

### 9.3. Апгрейды на dispertion

Только для **артиллерии**:
- `aca.20` («Research new sighting devices for artillery»):
  **−35 % dispersion**.
- `aca.27` («Develop mathematics»): **−35 %** (накапливается с
  `aca.20`).

Для мушкетёров и лучников **прямого** dispersion-апгрейда **нет**.

---

## 10. Открытые вопросы

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

[^2]: Случайный стартовый индекс и циклический проход по списку юнитов в ячейке — `lib/unit.script:4872-4877`:

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

[^3]: STO-балансировка для рукопашников — `lib/unit.script:5188-5198`:

    ```pascal
    var pstolist : Pointer = _misc_GetObjectArgData(trgHnd, gc_argunit_stolist);
    relativeDist := distSqr * (1 + TIntegerList(pstolist).GetCount * 0.125);
    ```

[^4]: Расчёт `maxsearchdistSqr` (штраф к радиусу для движущегося стрелка) — `lib/unit.script:5151-5156`:

    ```pascal
    var bmelee : Boolean = ...;
    if bmelee or (TObj(pobj).standtime > 0.25) then
       maxsearchdistSqr := maxsearchdist * maxsearchdist
    else
       maxsearchdistSqr := Sqr(maxsearchdist - gc_obj_maxattackradiusdisp * TObj(pObj).uniqrnd);
    ```

[^5]: Константы подрежимов движения — `dmscript.global:715-718`.

[^6]: `_player_OrderUnitsToAttackPoint` — `lib/player.script:2447-2481`:

    ```pascal
    if (gObjProp[TObj(pobj).cid][TObj(pobj).id].bartprepare) then
    begin
       TObj(pobj).bstandground := False;
       TObj(pobj).bsearchenemy := True;
       if (bClearOrders) then _unit_ClearOrders(goHnd);
       _unit_OrderAttackPoint(goHnd, trgx, trgz, False, bClearOrders);
    end;
    ```

[^7]: `_unit_SearchVictim` — `lib/unit.script:5214-5262`.

[^8]: `_unit_SearchVictimOnProgress` — `lib/unit.script:5443-5520`.

[^9]: `_unit_SearchEnemyInCell` — `lib/unit.script:4832-4961`.

[^10]: Битовые маски игроков на ячейке (`fplmask`, `myplmask`, `enemyplmask`) — `lib/unit.script:4842-4852`:

    ```pascal
    for plind := 0 to gc_MaxPlayerCount-1 do
    begin
       var enemyplmask : Integer = gPlayer[TObj(pObj).pl].enemyplmask;
       if scanmode <> 1 then
       begin
          if (gScanGrid[cellx, celly].fplmask and enemyplmask and (1 shl plind)) = 0 then
             continue;
       end
       else
       begin
          if (gScanGrid[cellx, celly].fplmask and gPlayer[TObj(pObj).pl].myplmask and (1 shl plind)) = 0 then
             continue;
       end;
       ...
    end;
    ```

[^11]: Та же ветка, см. [^10].

[^12]: Расчёт радиуса с учётом ближнего/дальнего боя — `lib/unit.script:4867-4870`:

    ```pascal
    var maxRad : Float = _unit_GetMaxAttackRadius(goHnd);
    var bmelee : Boolean = maxRad <= gc_unit_meleeattackradius;
    if not bmelee then
       maxRad := maxRad - gc_obj_maxattackradiusdisp * TObj(pobj).uniqRnd;
    ```

[^13]: Константы радиуса — `dmscript.global:113-116` (`gc_unit_meleeattackradius = 0.5 t`, `gc_obj_maxattackradiusdisp = 3 t`).

[^14]: Топологическая проверка цели — `lib/unit.script:4882-4889`:

    ```pascal
    if not bmelee then
    begin
       var trgX, trgY, trgZ : Float;
       GetGameObjectAbsolutePositionByHandle(trgHnd, trgX, trgY, trgZ);
       bFlag := (VectorDistance(goX, 0, goZ, trgx, 0, trgZ)) <= (maxRad + MaxFloat((goY - trgY) * 2, 0));
    end;

    if (_unit_GetRegion(trgHnd) = myRegion) or (bFlag) then ...
    ```

[^15]: Диспетчер по `scanmode` (выбор первой совместимой цели) — `lib/unit.script:4894-4961`. Все ветки 0/1/2/3 используют ранний выход `break(MAIN)`; ветка 4 (`AI sabotage`) обновляет `Result` по максимуму `weapon[0].damage` и не обрывается.

[^16]: Подсчёт прямоугольника ячеек — `lib/unit.script:5164-5170`:

    ```pascal
    var cellx, celly, cellxmax, cellymax : Integer;
    _misc_CalcScanCellsMinMax(x1, y1, rx1, cellx, celly, cellxmax, cellymax);
    var i, j : Integer;
    for [MAIN]i := cellx to (cellxmax) do
    for j := celly to (cellymax) do
       ...
    ```

[^17]: Главный цикл `_unit_SearchEnemyScanCells` — `lib/unit.script:5167-5210`:

    ```pascal
    for [MAIN]i := cellx to cellxmax do
    for j := celly to cellymax do
    begin
       trgHnd := _unit_SearchEnemyInCell(goHnd, i, j, scanmode);
       _misc_ScanGridCellDataUpdateResult(gScanGrid[i,j], trgHnd <> 0);
       if (trgHnd <> 0) then
       begin
          distSqr := Sqr(pX - GetGameObjectPositionXByHandle(trgHnd))
                   + Sqr(pZ - GetGameObjectPositionZByHandle(trgHnd));
          if (distSqr > minsearchdistSqr) and (distSqr < maxsearchdistSqr) then
          begin
             if (distSqr < mindist) then begin
                mindist := distSqr;
                minTrgHnd := trgHnd;
             end;
             if bmelee then
                relativeDist := distSqr * (1 + TIntegerList(pstolist).GetCount * 0.125)
             else
                relativeDist := distSqr;
             if (relativeDist < minRelativeDist) then
             begin
                minRelativeDist := relativeDist;
                minRelativeTrgHnd := trgHnd;
                if bmelee and (mindist < cOkDist) then break(MAIN);
             end;
          end;
       end;
    end;
    Result := minRelativeTrgHnd;
    ```

[^18]: Возврат `minRelativeTrgHnd` и комментарий автора — `lib/unit.script:5210`.

[^19]: Ранний выход для рукопашников — `lib/unit.script:5200-5202`:

    ```pascal
    const cOkDist = (gc_scangrid_size / 2) * (gc_scangrid_size / 2);
    if bmelee and (mindist < cOkDist) then
       break(MAIN);
    ```

[^20]: Расчёт радиусов в `_unit_SearchVictimOnProgress` — `lib/unit.script:5456-5475`:

    ```pascal
    var pobjprop : Pointer = gObjProp[TObj(pobj).cid][TObj(pobj).id];
    var searchdist : Float = TObjProp(pobjprop).searchradius;
    var minsearchdist : Float = TObjProp(pobjprop).minattackradius;

    if (minsearchdist > gc_unit_meleeattackradius) then
    begin
       var goHeight : Float = GetGameObjectPositionYByHandle(goHnd);
       if (goHeight < 0) then goHeight := 0;
       searchdist := searchdist + goHeight * 2;     // high-ground bonus
    end
    else
    begin
       if (TObj(pobj).orders[0].itype = gc_obj_order_type_guard) then
          searchdist := MinFloat(searchdist, gc_gameplay_meleeguardmaxsearchdist);
    end;
    ```

[^21]: Выбор `scanmode` в `_unit_SearchVictimOnProgress` — `lib/unit.script:5487-5492`:

    ```pascal
    var scanmode : Integer;
    if (TObjProp(pobjprop).bpriest) then
       scanmode := 1
    else if (not ((TObjProp(pobjprop).bcapture) or (TObjProp(pobjprop).media = gc_obj_media_water) or (TObjProp(pobjprop).bbuilding))) then
       scanmode := 2;
    ```

[^22]: Диспетчер обхода (water / long-range / regular) — `lib/unit.script:5494-5503`:

    ```pascal
    if (TObjProp(pobjprop).media = gc_obj_media_water) then
       trgHnd := _unit_SearchEnemyScanCellsShips(goHnd, posX, posZ, minsearchdist, scangridx, scangridy, rx1, scanmode)
    else
    begin
       if (_misc_GetShotPointsCount(goHnd) > 0) then
          trgHnd := _unit_SearchEnemyScanCellsLongRange(goHnd, posX, posZ, minsearchdist, scangridx, scangridy, rx1, cLongRangeTryNum, scanmode)
       else
       if (rx1 <= 5) and (scanmode <> 1) then
          trgHnd := _unit_SearchEnemyScanCells(goHnd, posX, posZ, minsearchdist, searchdist, scangridx, scangridy, rx1, scanmode)
       ...
    end;
    ```

[^23]: Дефолт флага `bsearchenemyinfront = True` — `lib/profile.script:30`.

[^24]: Умный поиск (фронтальный конус 30°) — `lib/unit.script:7334-7359`:

    ```pascal
    var bSmartSearch : Boolean = (gProfile.bsearchenemyinfront)
                              and (TObj(pobj).orders[0].itype = gc_obj_order_type_move)
                              and (TObj(pobj).orders[0].info.progress = gc_obj_order_move_mode_default);
    if bSmartSearch and (trgHnd <> 0) and (TObj(pobj).orders[0].bexecute) then
    begin
       ...
       const cMinAngle = 30;
       var dirx : Float = tpx - GetGameObjectPositionXByHandle(goHnd);
       var dirz : Float = tpz - GetGameObjectPositionZByHandle(goHnd);
       var dirx2 : Float = GetGameObjectPositionXByHandle(trgHnd) - GetGameObjectPositionXByHandle(goHnd);
       var dirz2 : Float = GetGameObjectPositionZByHandle(trgHnd) - GetGameObjectPositionZByHandle(goHnd);
       var angle : Float = VectorAngle(dirx, 0, dirz, dirx2, 0, dirz2);
       if (angle < cMinAngle) then
          _unit_OrderAttack(goHnd, trgHnd, True, False, False);
    end;
    ```

[^25]: `objprop.bartprepare := True` — `lib/unit.script:1724, 1756, 1846, 2240` (cannon, howitzer-проектив, framegun, tower built-in cannon).

[^26]: `_unit_TryAttackPoint` — `lib/unit.script:7512` и далее.

[^27]: Обработчик ордеров с `bsearchenemy := True` — `units/global.inc/readorder.inc:63, 88, 97`.

[^32]: Формула лечения через `gc_obj_weapon_kind_heal` —
       `lib/miscext2.script:371-398`. Описание священников и их
       параметров (heal/удар, дальность) — `lib/unit.script:1151-1188`.

[^33]: Реакция отряда на полученный урон — `lib/miscext2.script:406-417`.
       Обновление `TSquad.fAgressive := True` и `fLastBattleTime`
       при первом же успешном попадании по любому юниту отряда.

[^34]: Рассеяние выстрелов — `_weapon_CalcShotDispertion` в
       `lib/weapon.script:625`. Коэффициент `0.0267` —
       захардкожен; `weapon.dispertion` приходит из определения
       оружия в `lib/weapon.script` (после `_misc_PixelsToTiles`).
