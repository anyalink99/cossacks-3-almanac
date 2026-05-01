# Animation system: тайминги, циклы, точка удара

Что такое `.aaf` и `.acl` файлы, как кадры переводятся в g-секунды,
где живёт «момент удара» (swing point) и «момент выстрела»
(projectile spawn), где задаётся скорость движения каждого класса
юнитов. Все ссылки на код — в [Источниках](#источники).

> **Связанные документы:**
> [`../../docs/recon/world/combat/combat_damage_pipeline.md`](../../docs/recon/world/combat/combat_damage_pipeline.md)
> — формула урона; [`../../docs/recon/world/economy/building_mechanics.md`](../../docs/recon/world/economy/building_mechanics.md)
> — постройка через анимацию `construct`; [`../../docs/recon/world/combat/ranged_units_behavior.md`](../../docs/recon/world/combat/ranged_units_behavior.md)
> — стрельба и свойства снаряда.

## TL;DR

- **`gc_time_to_frames = 32`** — 32 кадра в одной игровой секунде.
  Юниты используют этот множитель напрямую. Для **зданий** есть
  дополнительный `gc_buildtime_modifier = 10`: их `buildtime`
  хранится в кадрах с множителем 10, реальное время постройки =
  `frames × 10 / 32` g-сек.
- **`.aaf`-файлы** (`data/animations/aaf/<sid>.aaf`) — текстовая
  таблица треков с `(name, start_frame, end_frame)`. 1 382 трека
  из 194 файлов (см. `derived/animations.json`).
- **`.acl`-файлы** (`data/animations/acl/<class>.acl`) — Animation
  Cycles List: FSM-граф переходов между анимациями. Внутри —
  `actAnimation`, `actExecuteState`, `actTrackPoint`-шаги.
- **`refspeed.acl`** — глобальный конфиг скоростей движения и
  поворота для каждого класса (`peasantwalk`, `infantrywalk`,
  `fasthorsewalk`, `cannonwalk`, …). Параметры
  `TrackPointMoveStep` / `TrackPointTurnStep`.
- **Момент удара / выстрела** — это callback `OnAclAnimationReachedAttack`
  (`units/unit.inc/onaclanimationreachedattack.inc`). Он встроен в
  `.acl`-цепочку attack-анимации между `actAnimation` и
  `actExecuteState 'OnAclAnimationReachedAttackEnd'` — то есть
  срабатывает в **точном кадре**, заданном файлом для каждого
  оружия / класса.
- **`gWeapons[].propagation`** определяет: применить урон сразу
  (`immediate` — для рукопашной, картечи, лучевого) или спавнить
  снаряд, который полетит и поразит цель позже.
- **Звуки выстрелов** на больших баталиях фильтруются RNG'ом через
  `gWeapons[].volumeclippedfreq`, чтобы не клипали — детали §6.

---

## 1. Frame-time и `gc_time_to_frames = 32`

`gc_time_to_frames = 32` — фундаментальная константа времени в
движке. Каждое игровое событие, которое описывается в кадрах
(анимации, паузы оружия, таймеры), переводится в g-секунды как
`frames / 32`.

**Исключение — здания.** `gc_buildtime_modifier = 10` — поле
`buildtime` у зданий хранится в **кадрах × 10**. То есть реальное
время постройки = `buildtime_frames × 10 / 32` g-сек. У юнитов
такого множителя нет, у них `buildtime / 32` — и всё.

| Объект | `buildtime` хранится как | Формула g-сек |
|---|---|---|
| Юнит (peasant / pikeman / cannon) | кадры | `buildtime / 32` |
| Здание (cen / bar / aca) | кадры × 10 | `buildtime × 10 / 32` |

См. также
[`../../docs/recon/world/economy/building_mechanics.md`](../../docs/recon/world/economy/building_mechanics.md).

---

## 2. Файлы и форматы

### 2.1. `.aaf` — Actor Animation File

Текстовый файл (формат cp1251) в `data/animations/aaf/`:

```
AAF
18
"idle",64,113,morph
"walk",1,20,morph
"attack0",237,254,morph
"workfood",278,299,morph
"workwood",237,254,morph
"workstone",217,234,morph
"construct",186,198,morph
"reaction",456,481,morph
"prepare0",64,65,morph
...
```

Заголовок `AAF` + число записей, далее одна строка на трек:
`"name", start_frame, end_frame, mode` (mode обычно `morph`).

**Формат включения:** `start` и `end` — оба inclusive.
Длительность = `end − start + 1` кадров = `(end − start + 1) / 32`
г-сек.

Примеры из `peaaus.aaf`:

| Трек | start–end | Длительность |
|---|---:|---:|
| `walk` | 1–20 | 20 кадров = 0.625 г-сек |
| `attack0` | 237–254 | 18 кадров = 0.5625 г-сек |
| `construct` | 186–198 | **13 кадров = 0.4063 г-сек** |
| `workfood` | 278–299 | 22 кадра = 0.6875 г-сек |
| `workstone` | 217–234 | 18 кадров = 0.5625 г-сек |

**Ключевые имена треков:**

- `idle`, `idle0`, `idle1`, … — стояние без действия.
- `walk` — основное движение. `walkfood/wood/stone` — с грузом.
- `attack0`, `attack1`, `attack2` — три слота оружия (см. §5).
- `workfood/wood/stone` — собирательная работа.
- `construct` — стройка / ремонт здания.
- `death` — смерть.
- `prepare0`, `prepareN` / `unprepareN` — подготовка / упаковка
  (для `bartprepare`-юнитов: артиллерия, башни).
- `reaction` — реакция на близкого врага (готовность к бою).
- `idlefood/wood/stone` — стояние с грузом (промежуточное состояние).

**Сводка по нашему парсеру:** `parser/parse_animations.py` извлекает
все треки в [`derived/animations.json`](../../derived/animations.json).
Среднее `attack0` по всем рукопашным юнитам — **15 кадров (0.469 г-сек)**.
Это и зашито в `parser/config.py` как `MELEE_SWING_FALLBACK_FRAMES = 15`
для случаев, когда у юнита нет своего `.aaf`.

### 2.2. `.acl` — Animation Cycles List

Текстовый `.parser`-формат в `data/animations/acl/`. Описывает
**FSM-граф переходов** между анимациями. Каждая запись —
именованный цикл со списком actions.

Пример из `cannon.acl` (атака пушки):

```
[*] : struct.begin
   Name = attack0
   From = attack0
   CyclesList = False
   Options : struct.begin
      acoSmoothAnimation = True
      acoRandomFrame = False
      acoRandomCycle = False
      acoSkipActions = False
   struct.end
   global : struct.begin {refurl=.\data\animations\ref\refspeed.acl; refkey=.cannonidle}
      Action = actTrackPoint
      TrackPointIdleName = 
      TrackPointMode = mmNone
      TrackPointPreset = 
   struct.end
   items : struct.begin
      [*] : struct.begin
         Action = actExecuteState
         ExecuteStateName = OnAclAnimationReachedAttack
      struct.end
      [*] : struct.begin
         Action = actAnimation
         AnimationName = attack0
         NumberCycle = 1
      struct.end
      [*] : struct.begin
         Action = actExecuteState
         ExecuteStateName = OnAclAnimationReachedAttackEnd
      struct.end
   struct.end
struct.end
```

**Ключевые поля:**

| Поле | Что |
|---|---|
| `Name` | Имя цикла (внутри .acl-FSM). |
| `From` | Состояние, из которого приходим. |
| `CyclesList` | Можно ли цикл проигрывать в списке. |
| `Options.acoSmoothAnimation` | Сглаживание перехода (blend). |
| `Options.acoRandomFrame` | Стартовать с случайного кадра (для разнообразия в группе юнитов). |
| `Options.acoRandomCycle` | Случайно выбирать вариант цикла. |
| `Options.acoSkipActions` | Пропустить `items[]` (только анимация без callback'ов). |
| `global` | Глобальная настройка через `refurl`-include из `refspeed.acl`. |
| `items[]` | Последовательность action'ов (см. §2.3). |

**`refurl` / `refkey`:** include-механизм. `refurl=.\data\animations\
ref\refspeed.acl; refkey=.cannonidle` означает «вставь сюда
запись `cannonidle` из `refspeed.acl`». Аналог `#include` в C.

### 2.3. Action-типы в `.acl`

| Action | Что делает |
|---|---|
| `actAnimation` | Проиграть анимацию (по имени трека из `.aaf`); параметр `NumberCycle` — сколько повторов. |
| `actExecuteState` | Перейти в FSM-состояние юнита (по имени) — вызывает `units/unit.inc/<state>.inc`-обработчик. |
| `actTrackPoint` | Изменить trackpoint юнита (для движения по предзаписанной траектории). Параметры `TrackPointMode = mmNone / mmRelative / mmAbsolute`. |

Главные `ExecuteStateName`:

- `OnAclAnimationReachedAttack` — **момент удара / выстрела** (§5).
- `OnAclAnimationReachedAttackEnd` — конец attack-анимации.
- `OnAclAnimationStarted`, `OnAclAnimationFinished` — начало / конец.

### 2.4. `refspeed.acl` — таблица скоростей движения

В `data/animations/ref/refspeed.acl` — общий конфиг с шагом
движения и поворота для каждого класса юнитов. Каждый класс имеет
два режима: `…idle` (на месте) и `…walk` (в движении).

| Класс | `walk.TrackPointMoveStep` | `walk.TrackPointTurnStep` |
|---|---:|---:|
| infantry | 0.03 | 11.125 |
| peasant | **0.0375** | 11.125 |
| hardhorse | 0.0525 | 11.125 |
| fasthorse | **0.09** | 11.125 |
| cannon | 0.020625 | 2.225 |
| mortar | 0.0225 | 8.9 |
| howitzer | 0.020625 | 8.9 |
| multicannon | 0.018 | 11.125 |
| fishboat | 0.015 | 1.1125 |
| ferry | (см. файл) | (см. файл) |

`TrackPointMoveStep` — сколько тайлов сдвигается юнит на **один
кадр анимации walk** (то есть за `1/32` г-сек). `TrackPointTurnStep`
— угол поворота за один кадр (в градусах).

Скорость в тайлах за секунду:

```
tiles_per_g_sec = TrackPointMoveStep × 32
```

| Класс | Скорость (тайлов / г-сек) |
|---|---:|
| infantry | 0.96 |
| peasant | 1.20 |
| hardhorse | 1.68 |
| fasthorse | **2.88** (×3 от пехоты) |
| cannon | 0.66 |
| mortar | 0.72 |
| howitzer | 0.66 |
| fishboat | 0.48 |

См. также `gc_obj_speed_*` константы в `dmscript.global`
(`peasant = 40`, `fasthorse = 96`, и т. д.) — это абстрактная
шкала, **пропорциональная** `TrackPointMoveStep`, но не
тождественная. Для точных значений в тайлах берут отсюда
(`refspeed.acl`).

### 2.5. `refunit.acl`

Общий конфиг базовых циклов `idle / walk / death` — переиспользуется
через `refurl`-include из конкретных `<class>.acl`-файлов.
Снижает дублирование: типичная привязка — «у пушки `idle` такой
же как у инфантерии, но `walk` особый».

---

## 3. Native API для анимаций

`derived/dws_native_signatures.json` содержит **600+ функций**
работы с анимациями. Ключевые группы:

### 3.1. Frame-data

| Функция | Что |
|---|---|
| `GetGameObjectFrameAnimationDataByHandle(gohnd, animname, var sf, ef): Boolean` | Получить start / end кадры анимации `animname` для объекта. Используется в `_unit_ApplyAttackPause` для расчёта пауз. |
| `GetGameObjectDeferredFramesByHandle(gohnd, var defcurrentframe, defframes)` | Текущий кадр и общее число кадров отложенного цикла. |

### 3.2. Switch / blend

| Функция | Что |
|---|---|
| `GameObjectSetFrameAnimationByHandle(gohnd, frameanimationname, randomoffsetframeanimation)` | Прямая установка анимации. |
| `GameObjectSwitchToAnimationCyclesBlendByHandle(gohnd, name, ...)` | Плавный blend между текущим и новым циклом. |
| `GameObjectMySwitchToFrameAnimationBlend(name, randomframe, smooth, ...)` | Тот же blend для «своего» (current-actor) контекста. |

### 3.3. TrackPoint

| Функция | Что |
|---|---|
| `GameObjectMyTrackPointAdd(x, y, z)` | Добавить точку для движения по path'у. |
| `GameObjectMyTrackPointInsert(ind, x, y, z)` | Вставить в позицию `ind`. |
| `GameObjectMyTrackPointClear()` | Очистить все track points. |
| `GameObjectGetTrackPointMoveDistanceToEndByHandle(gohnd)` | Дистанция от текущей позиции до конца пути. |
| `GameObjectGetTrackPointMoveDistanceToAlignByHandle(gohnd)` | Дистанция до точки выравнивания (формация). |

---

## 4. FSM юнита и её связь с анимациями

Каждый юнит — FSM, состояния хранятся как битмаска
`gc_statetag_*` в `TObj.statestag` (см. таблицу в
`dmscript.global`). Главные группы:

| Группа | Биты |
|---|---|
| Essential | `essential_none`, `essential_birth`, `essential_death` |
| Move | `move_idle`, `move_walk`, `move_turn` |
| Action | `action_none`, `action_attack`, `action_build`, `action_extract` |
| Execute | `execute_none`, `execute_move` |
| Weapon | `weapon_none`, `weapon_0`, `weapon_1`, `weapon_2` |
| Resource | `resource_none`, `resource_food`, `resource_wood`, `resource_stone` |
| Visual | `visual_none`, `visual_stage_0..3`, `visual_hide` |

При смене состояний `.acl`-FSM подбирает соответствующую анимацию
(например, `walkfood` если `state = move_walk + resource_food`).

Конкретные обработчики FSM-переходов — в
`data/scripts/units/unit.inc/<state>.inc`. Например:
`onaclanimationreachedattack.inc` срабатывает на event
«анимация атаки достигла swing-point» (§5).

---

## 5. `OnAclAnimationReachedAttack` — момент удара / выстрела

Это **главный callback** животной системы: момент в кадре, когда
урон применяется по цели или вылетает снаряд. Полностью описан в
`data/scripts/units/unit.inc/onaclanimationreachedattack.inc`.

### 5.1. Где задаётся точный кадр

В `.acl`-файле для атаки (`attack0` / `attack1` / `attack2`)
порядок `items[]` определяет, **в какой момент** анимации
сработает callback. Стандартная структура:

```
items:
  [0] actExecuteState 'OnAclAnimationReachedAttack'    ← swing point
  [1] actAnimation 'attack0' (NumberCycle = 1)         ← полная анимация
  [2] actExecuteState 'OnAclAnimationReachedAttackEnd' ← завершение
```

`actExecuteState` срабатывает в момент когда `actAnimation`
дойдёт до соответствующей метки. То есть `swing-point` встроен
**в саму анимацию** через `.acl`-конфиг — для разных юнитов он
может быть в начале, середине или конце attack-цикла.

### 5.2. Что callback делает

Псевдокод (`onaclanimationreachedattack.inc`):

```
1. Если юнит мёртв — выход.
2. weapind := номер оружия из statetag (gc_statetag_weapon_0/1/2 → 0/1/2).
3. _unit_ApplyWeaponCost(myHnd, weapind)        ← списание iron/coal/gold за выстрел
4. _unit_ApplyAttackPause(myHnd, weapind)        ← пауза до следующего цикла
5. weaponid := objprop.weapon[weapind].weaponid
   trgHnd := GetGameObjectSTOHandleByHandle(myHnd)  ← кэш найденной цели
6. Если trgHnd ≠ 0:
   а) weaponid == 0 (рукопашный):
      - Звук удара (sword/sabre/pike) через _unit_RequestPlaySound
      - _misc_DoDamage(myHnd, trgHnd, damage, weapind, kind) ← урон сразу
   б) propagation == immediate (картечь, lightning):
      - _misc_DoDamage сразу
      - Звук выстрела
      - Spawn fxshot-эффекта (вспышка, дым)
   в) обычный снаряд:
      - Spawn projectile через CreatePlayerGameObjectHandleByHandle
      - Полётом снаряда занимается отдельная FSM проектиля
      - _misc_DoDamage применится на event '_OnTargetReached'
```

### 5.3. Семантика для разных типов оружия

| Тип `weaponid` | Что в момент swing |
|---|---|
| Рукопашный (`weaponid = 0`) | Урон сразу. Звук — `sabre`/`pike`/`sword` (по `kind`). |
| Стрелковый с `propagation = immediate` (картечь, lightning) | Урон сразу + звук + fxshot. Радиус AoE применяется здесь же. |
| Обычный снаряд (стрела, пуля, ядро) | Спавнится `projectile`-объект, летит к цели. Урон применяется на момент **прибытия** снаряда (event `_OnTargetReached`), а не на момент swing. Это даёт «время полёта» для стрел и ядер. |

### 5.4. RNG-фильтр звуков выстрела

Если объект **не в frustum** камеры и
`gWeapons[weaponid].volumeclippedfreq > 0`, делается RNG-проверка:
`if vcf < random` — звук **пропускается**. То есть на больших
баталиях, где 100 мушкетёров стреляют залпом, часть звуков
случайно отбрасывается, чтобы не клипало миксер.

Если `volumeclippedfreq <= 0` — звук всегда играется (мушкет в
frustum, артиллерия). Если `volumeclippedfreq` высокий (≈ 0.9) —
звук пропускается часто (фоновая стрельба вне поля зрения).

---

## 6. `_unit_ApplyAttackPause` — следующий цикл

После каждого свинга устанавливается пауза до следующего
цикла атаки [^2]:

```
attpause := objbase.weapon[weapind].pause
if individual.benabled and attpause > 0:
    attpause *= individual.attackrate    ← апгрейды-перцент
```

Конкретное число `pause` хранится в данных юнита. Для мушкетёра
17 в. — `pause ≈ 150` кадров = 4.69 г-сек. С апгрейдами
`aca.31`+`aca.33` (60 % cumulative reduction) — `≈ 1.88 г-сек`.

В коде есть **закомментированная** ветка проверки «достаточна ли
пауза для длины анимации»: если `attpause - frames/30 < 1/60`,
пауза не нужна (анимация и так длинная). На текущий момент эта
ветка **отключена** — пауза применяется всегда, даже если она
короче анимации (это не критично: следующая swing-точка не
сработает раньше следующего цикла `.acl`).

---

## 7. `_unit_ApplyWeaponCost` — стоимость выстрела

При каждом swing'е списывается `weapon[weapind].cost[restype]` за
выстрел [^3]:

```
for i := 0 to gc_ResCount-1:
   if weapon[weapind].cost[i] > 0:
      if gPlayer[plInd].res[i] >= weapon[weapind].cost[i]:
         res[i] -= weapon[weapind].cost[i]
      else:
         res[i] := 0  ← если ресурса меньше, списывается остаток
```

То есть если у игрока кончился `iron` или `coal`, башня / пушка
**всё равно стреляет** (списывает остаток до нуля), но потом без
ресурса перестаёт. Не выстрел блокируется ресурсом — он списывается
по факту удара. Это ключевой механизм: **на момент свинга проверка
ресурса нет**, проверка идёт раньше — на этапе выбора цели.

Полные таблицы цены выстрела по каждому юниту — в
[`../../docs/reference/02_combat.md` → «Стоимость одного выстрела»](../../docs/reference/02_combat.md).

---

## 8. Ключевые тайминги (сводка)

Из 1 382 треков в `derived/animations.json`:

| Класс | `attack0` (кадры) | `attack0` (г-сек) | `walk` (кадры) | Real-DPS @ fast (если known) |
|---|---:|---:|---:|---:|
| Крестьянин (peaaus) | 18 | 0.563 | 20 | — |
| Пикинёр 17 в. | 14 | 0.438 | 20 | ~7-8 |
| Мушкетёр 17 в. | 18 | 0.563 | 22 | ~6-7 (через `weapon.pause`) |
| Кавалерист | 18 | 0.563 | 26 | — |
| Пушка | 14-16 | 0.5 | (см. §2.4) | по `weapon.pause = 350 frames` |
| Башня | 14 | 0.438 | (idle) | по `weapon.pause = 400 frames` |

`attack0` — длительность анимации удара. Реальный темп атаки
определяется `weapon.pause` (см. §6), который обычно **больше**
`attack0` (из-за встроенного отдыха между свингами). Для
рукопашников `weapon.pause = 0` — они бьют каждый цикл анимации,
то есть **`attack0`-длительность и есть DPS-цикл**.

См. функцию `melee_swing_sec(sid)` в
[`parser/config.py`](../../parser/config.py) — берёт реальный
`attack0` из `derived/animations.json` или fallback на медиану 15
кадров (0.469 г-сек).

---

## 9. Открытые вопросы

1. **Точные значения refspeed для всех классов.** Я перечислил
   главные (infantry / peasant / hardhorse / fasthorse / cannon /
   mortar / howitzer / multicannon / fishboat / ferry), но в
   `refspeed.acl` есть и более экзотические (`balloondock`,
   `ducha`-морские классы и т. д.). Полный дамп — открыть файл.
2. **Как `gc_obj_speed_*` соотносится с `TrackPointMoveStep`.**
   Похоже что это две **разные** шкалы: `gc_obj_speed_*` —
   абстрактная для AI-расчётов, `TrackPointMoveStep` — реальная
   для рендера. Связь не вычитана.
3. **`actTrackPoint` с режимом `mmRelative` vs `mmAbsolute`** —
   как именно используется при движении в строю.
4. **`acoRandomFrame` поведение.** Если включён, юниты в группе
   стартуют walk-анимацию с разных кадров — но как выбирается
   стартовый кадр? Через `random()` или `uniqrnd`?

---

## Источники

[^1]: `data/scripts/units/unit.inc/onaclanimationreachedattack.inc`
      — главный handler момента удара. Параметры: `arg_obj : TObj`.
      Внутри проверяет `bdead`, `attackdelay`, выбирает оружие
      через `statetag`, применяет `_unit_ApplyWeaponCost` /
      `_unit_ApplyAttackPause`, делегирует урон в `_misc_DoDamage`
      (для рукопашной / immediate) или спавнит `projectile`-объект
      (для дальней атаки).

[^2]: `_unit_ApplyAttackPause` — `lib/unit.script` (поиск
      `procedure _unit_ApplyAttackPause`). Считает финальную паузу
      как `attpause * individual.attackrate` (если индивидуальные
      апгрейды активны).

[^3]: `_unit_ApplyWeaponCost` — `lib/unit.script` (поиск
      `procedure _unit_ApplyWeaponCost`). Списывает
      `weapon[weapind].cost[i]` для всех 7 ресурсов (food / wood /
      stone / gold / iron / coal / +1).
