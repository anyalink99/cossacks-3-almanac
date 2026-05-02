# Recon: добыча ресурсов крестьянами

Полная модель скорости добычи всех ресурсов: формулы, шахты, поля,
апгрейды эффективности, влияние карты. На этих числах строятся симулятор
экономики и расчёты в [`docs/reference/01_economy.md`](../../../reference/01_economy.md).
Все ссылки на код и сами Pascal-блоки собраны в разделе
[Источники](#источники) в конце документа.

**Контекст по умолчанию (если в тексте не указано иное):**

- Скорость партии — **fast** (`gamespeed = 2`, множитель ×1.4 к нормальной; см. §1).
- Карта — `terraintype = 0` (Суша), `relieftype = 3` (Высокогорье),
  `resourcemines = 2` (Много), `mapsize = 3` (Маленькая, 256 × 256).
- Все пути к скриптам в [Источниках](#источники) — относительно `data/` в установке Cossacks 3.

> **Связанные документы:**
>
> - [determinism_audit.md](../../../../internals/engine/determinism_audit.md) — RNG-сайты в горячем
>   пути добычи и ожидаемый разброс между запусками.
> - [ticks_and_subticks.md](../../../../internals/engine/ticks_and_subticks.md) — модель времени,
>   sub-tick state-machine, адаптивная скорость. Нужен для правильной
>   интерпретации real-time против game-time при замерах.
> - [server_sync_architecture.md](../../../../internals/engine/server_sync_architecture.md) —
>   server-authoritative архитектура C3 (важна для multiplayer-замеров).
> - [map_generation_pipeline.md](../map/map_generation_pipeline.md) — таймлайн
>   `DoGenerate`, стартовые позиции, размещение лесов / камней / шахт.

> **TL;DR.** Аналитический потолок добычи (формулы ниже) считаем в
> **игровом времени**. Реальная in-game добыча будет ниже — из-за
> RNG-выборов цели в `_misc_FindResourceToExtract` (см.
> [determinism_audit.md](../../../../internals/engine/determinism_audit.md) §3). Разброс между
> запусками одного сейва на 5-минутном окне — 5–15% для леса и камня,
> ≈ 0% для шахт.

---

## 1. Игровая скорость и время

**Базовый тик:** `gc_time_to_frames = 32` — 32 кадра в одной игровой
секунде [^1]. Все длительности в скриптах в "frames" нужно делить на 32 для
перевода в **игровые секунды (game-time)**.

**Скорости игры** (`gc_settings_gamespeed_*`) [^2]:

| Mode | Tag | speedfactor |
|---|---:|---:|
| 0 (slow)   | 7  | 0.7× |
| 1 (normal) | 10 | 1.0× |
| **2 (fast)** | **14** | **1.4×** |

**Вывод для расчётов:** все формулы ниже даны в **игровых секундах**.

## 2. Цикл добычи (поведение)

Пайплайн одного крестьянина:

1. **Удар (work tick).** При работе анимация `workfood`/`workwood`/`workstone`
   цикл = N кадров. По достижении конца цикла:
    - срабатывает `OnAclAnimationReachedWork` [^3].
    - `arg_obj.resamount += 1` — увеличивается счётчик "ударов" в инвентаре.
    - HP ресурса уменьшается:
      - food: `-= Max(1, floor(100/(1+fieldlife/100)))`. Default fieldlife=0 → 100 HP/удар.
      - wood: `-= 1`. При HP=0 → дерево становится пнём (см. §4.2).
      - stone: `-= 1`. Stone HP = 10 000 000, фактически бесконечно.

2. **Возврат к складу.** Когда `resamount >= hitsneeded` [^4]:
    - food: 22, wood: 14, stone: 20 ударов.
    - Запускается `_unit_GetNearestStorehouse` — поиск по списку
      `gPlayer[pl].lists.storehouses` [^5]. Учитываются здания с
      `usage=storage/mill/center` и `resourcebase[restype]=True`.
    - Цель — `resourcePoint` склада (точка сдачи в тайловых координатах
      от позиции здания; таблицы по всем типам — в §3 «Точки сдачи ресурсов»).

3. **Сдача.** При попадании в радиус `gc_gameplay_resourceDropRadiusSqr = 0.5` (≈0.707 тайла):
    - `_unit_PeasantAddResToPlayerByIndex` → `delivered = (portion × eff) / 100` [^6].
    - Базовые порции (`gc_obj_resource_portion_*`): food=**45**, wood=**28**,
      stone=**40**, прочее=**20** [^7].
    - `eff` — `gPlayer[pl].resefficiency[cid][restype]`, стартует со 100,
      апгрейды добавляют (см. §7).
    - `restype := none`, `resamount := 0`, поиск нового ресурса.

4. **Re-acquire.** `_unit_SearchResourceInRadius` около **исходной точки задачи**
   (`TOrderInfo.x/y`) [^8]:
    - Стандартный радиус: `gc_obj_res_searchradius = 6` тайлов.
    - Если `standtime>9` или `random>0.9` → расширение до `2× = 12` тайлов [^9].
    - Скоринг кандидатов: `score = (1+myDst/5) × (1+resDst/4) × (1+stoFactor) × (1+attFactor)`.
      `attFactor`/`stoFactor` штрафуют ресурс, к которому уже идут другие.
    - Только `brised=True`. Лимит конкурентных добытчиков на ресурс:
      food=**3**, wood=**2**, stone=**3**.

## 3. Константы (extracted)

### Анимация — кадры одного work-цикла

Из `data/animations/aaf/peaaus.aaf` (одинаково для всех наций кроме `pearus`):

| Cycle | Frames | g-sec |
|---|---:|---:|
| workfood (aus,fra,eng,...) | 22 | 0.6875 |
| workfood (rus) | 23 | 0.7188 |
| workwood | 18 | 0.5625 |
| workstone | 18 | 0.5625 |
| walk | 20 | 0.625 |
| walkfood | 20 | 0.625 |
| walkwood | 20 | 0.625 |
| walkstone | 20 | 0.625 |

Animation frame rate совпадает с `gc_time_to_frames = 32` (32
кадра / g-sec) — подтверждено через `parser/parse_animations.py`
и согласовано с `refspeed.acl`-таблицей `TrackPointMoveStep`. См.
[`internals/engine/animation_system.md`](../../../../internals/engine/animation_system.md).

### Базовые числа добычи

| Параметр | Значение | Источник |
|---|---:|---|
| `gc_obj_resource_portion_food` | 45 | [^7] |
| `gc_obj_resource_portion_wood` | 28 | [^7] |
| `gc_obj_resource_portion_stone` | 40 | [^7] |
| `gc_obj_resource_portion_others` | 20 | [^6] |
| `gc_resource_hitsneeded_food` | 22 | [^4] |
| `gc_resource_hitsneeded_wood` | 14 | [^4] |
| `gc_resource_hitsneeded_stone` | 20 | [^4] |
| Default `eff` | 100 | [^10] |
| `gc_FieldMaxHP` | 25 000 | [^11] |

### Радиусы и расстояния

| Параметр | Значение (тайлы) | Назначение |
|---|---:|---|
| `gc_obj_res_searchradius` | 6 | base search radius после сдачи |
| (расширение при standtime) | до 12 (2×) | [^9] |
| `gc_obj_extract_food_radiusmax` | 1.5 (=80×0.01875) | дальность "удара" поля |
| `gc_obj_extract_wood_radiusmax` | 0.75 (=40×0.01875) | дальность "удара" дерева |
| `gc_obj_extract_stone_radiusmax` | 0.9375 (=50×0.01875) | дальность "удара" камня |
| `gc_gameplay_resourceDropRadiusSqr` | 0.5 (sqrt≈0.707) | радиус сдачи у склада |

### Точки сдачи ресурсов (resourcePoint)

Каждое здание-приёмник ресурсов имеет в `data/game/var/objcustom.cfg` фиксированную точку
`ResourcePoint {x, z}` — смещение в **тайловых координатах** от мировой позиции здания.
Именно к ней идёт крестьянин; она же используется в `_unit_GetNearestStorehouse`
для ранжирования ближайшего склада. Здания с `usage = storage / mill / center` и
`resourcebase[restype] = True` попадают в список кандидатов [^5].

В C3 отрицательный z = север = верхняя часть экрана. Все значения с большим отрицательным z
находятся на **северной (верхней) стороне** здания.

**Склады** (`gc_obj_usage_storage`):

| sid | Нации | x | z | Позиция |
|---|---|---:|---:|---|
| eursto | aus, bav, den, eng, fra, hun, net, pie, pru, sax, sco, swe, swi, ven | +0.20 | −1.69 | северный угол |
| russto | pol, rus, ukr | +0.19 | −1.50 | северный угол |
| tursto | alg, tur | +0.17 | −1.67 | северный угол |
| spasto | por, spa | — | — | центр здания (0, 0) — не задан |

**Мельницы** (`gc_obj_usage_mill`):

| sid | x | z | Позиция |
|---|---:|---:|---|
| eurmil | −0.02 | −1.61 | северная сторона |
| rusmil | +0.04 | −1.09 | северная сторона |
| turmil | −0.44 | −2.56 | северная сторона |

**Городские центры** (`gc_obj_usage_center`):

| sid | x | z |
|---|---:|---:|
| vencen | +0.07 | −3.86 |
| swecen | +0.02 | −3.68 |
| engcen | −0.50 | −3.67 |
| turcen | +0.49 | −3.41 |
| auscen | −0.11 | −3.34 |
| spacen | +0.10 | −3.35 |
| saxcen | +0.24 | −3.25 |
| porcen | +0.30 | −3.17 |
| ukrcen | −1.30 | −3.16 |
| algcen | +0.80 | −3.20 |
| ruscen | −0.28 | −3.22 |
| fracen | +0.01 | −3.12 |
| prucen | −0.06 | −3.07 |
| bavcen | −1.45 | −3.07 |
| polcen | −0.06 | −2.63 |
| swicen | −1.82 | −2.51 |
| huncen | +1.39 | −2.25 |
| piecen | −0.25 | −2.42 |
| dencen | −0.10 | −2.20 |
| netcen | +0.43 | −2.23 |
| scocen | 0 | **−0.72** ⚠ аномалия — фактически центр здания |

Источник: `data/game/var/objcustom.cfg` (парсится `_country_initobjcustom` при старте).

### Скорости движения

Реальная скорость задаётся в `data/animations/ref/refspeed.acl`
через параметр `TrackPointMoveStep` (тайлов за один кадр walk-анимации).
Скорость в тайлах за игровую секунду = `TrackPointMoveStep × 32`:

| Класс | `TrackPointMoveStep` | Тайлов / g-sec |
|---|---:|---:|
| infantry | 0.03 | **0.96** |
| **peasant** | **0.0375** | **1.20** |
| hardhorse | 0.0525 | 1.68 |
| fasthorse | 0.09 | 2.88 |
| cannon | 0.020625 | 0.66 |

Абстрактная шкала `gc_obj_speed_*` (default = 32, peasant = 40,
hardhorse = 56, fasthorse = 96, cannon = 20, mortar = 24) [^12]
**пропорциональна** `TrackPointMoveStep`, но используется
скриптами для AI-расчётов и упрощённого relative-сравнения. Для
точных реальных скоростей в тайлах берут отсюда (`refspeed.acl`).
Подробности — в [`internals/engine/animation_system.md` §2.4](../../../../internals/engine/animation_system.md).

### Конкурентные добытчики на одном ресурсе

`gc_gameplay_resource_maxattackers_*`:

- food = 3, wood = **2**, stone = 3, none = 4

## 4. Per-resource математика

### 4.1 Идеальный rate (без хождения)

Для одного крестьянина, без учёта дороги к складу, при `eff=100`, `fieldlife=0`:

```
rate_per_trip = portion × eff / 100             # ресурс за поход
time_per_trip_game = hitsneeded × t_hit_game    # игровых секунд
rate = rate_per_trip / time_per_trip_game       # ресурс/игровая_сек
```

| Ресурс | portion | hitsneeded | t_hit_game | rate (units/g-sec) | units/g-min |
|---|---:|---:|---:|---:|---:|
| food (default eff) | 45 | 22 | 0.6875 | **2.975** | **178** |
| wood | 28 | 14 | 0.5625 | **3.556** | **213** |
| stone | 40 | 20 | 0.5625 | **3.556** | **213** |

⚠ Это **верхняя граница** — реальный rate ниже из-за дороги к складу.

### 4.2 Wood — большие/средние/мелкие деревья

При спавне случайно [^14]:

| Шанс | HP | Тип | Wood с дерева |
|---:|---|---|---:|
| 20% | `floor(8000×(1+random)) = 8000..16000` | **гигант** | ≈ 16k..32k wood (HP × 2) |
| 15% | `floor(125×(1+random×4)) = 125..624` | средний | ≈ 250..1248 wood |
| 45% | `floor(10+rnd×(0.5+random×0.5)×100)`, `rnd∈[0.2,0.65]` → **20..75** | мелкий | ≈ 40..150 wood |
| 20% | 10 | «пенёк» | ≈ 20 wood |

Расчёт: `gc_resource_hitsneeded_wood = 14`, `gc_obj_resource_portion_wood = 28`, то есть **2 wood на удар** (28/14). Поэтому `wood ≈ HP × 2`. Это без апгрейдов (`eff = 100`); `mill.X` / `aca.X` / `bla.X` множат через `eff`.

**Среднее ожидание HP** (грубо):

- 0.2 × 12000 + 0.15 × 375 + 0.45 × 47 + 0.2 × 10 ≈ **2480 HP** на дерево
- При 14 hits/trip ≈ 177 рейсов на «среднее» дерево, ≈ **4956 wood/дерево**.

**Переход дерево→пень** [^15]:

- При HP=0 → `gc_statetag_essential_death` → меш меняется на `pinestump1..4`
  (распределение 70/20/5/5%), `collisioninertia=False`.
- `brised` для wood **никогда не выставляется в False** в коде (в отличие
  от food, где flag используется для замедления роста). Пень остаётся
  валидным ресурсом в `gResGrid`, search его видит, итип=wood сохраняется.

**Предпочтение целых деревьев — emergent через penalty queueing.** В
скоринге кандидата [^16]:

```
score = (1 + dstMy/5) × (1 + dstRes/4) × (1 + stoFactor) × (1 + attFactor)
attFactor = 1 + attcount × 1.5    if attcount ≥ 1, else 0
stoFactor = 1 + stocount × 1.5    if stocount ≥ 1, else 0
```

`attcount` = сейчас рубят, `stocount` = сейчас идут к нему. `dstMy` —
расстояние от крестьянина, `dstRes` — расстояние от исходной точки
задания. **Минимальный score побеждает.**

Эффект: ресурс с 1 активным рубщиком получает множитель ×(1+2.5) = **×3.5**
к скору. Целое дерево без рубщиков рядом всегда побеждает пень с рубщиком
в 2-3 тайлах. Так возникает наблюдаемое предпочтение — **не из-за того,
что это пень, а из-за того, что на пне уже работают**.

**Пустой пень vs целое дерево, оба без рубщиков** — побеждает ближний по
дистанции, без штрафа. Когда лес вырублен (все стали пнями), крестьяне
работают по ним равномерно, без избегания.

**Крест-овер дистанций** (примерно): пень с 1 рубщиком на 2 тайлах
проигрывает целому дереву на ≤8 тайлах. Но search radius = 6 тайлов, так
что эффективная зона — ~3-5 тайлов "форы" целому дереву над занятым пнём.

**Hard cap:** при `attcount ≥ maxattackers=2` для wood ресурс полностью
фильтруется (75% времени, 25% шанс обхода через `bskipcheck = random>0.75`).

### 4.3 Stone — фактически бесконечный

HP = 10 000 000 [^17]. Один камень держит 10M ударов = 500k рейсов = 20M
камня. Бесконечно для практических целей. Все расчёты для stone — без
учёта истощения.

### 4.4 Food — поле с регенерацией

**HP поля:** старт = 0, при `essential_birth → essential_none`
устанавливается = `gc_FieldMaxHP = 25000` [^18].

**Урон полю за удар:** `resdec = Max(1, floor(100/(1+fieldlife/100)))`.

| fieldlife | resdec/удар | макс ударов до 0 HP | макс food (при eff=100) |
|---:|---:|---:|---:|
| 0   | 100 | 250 | 250 × 45/22 = **511** |
| 100 | 50  | 500 | 1023 |
| 200 | 33  | ~757 | 1549 |
| 300 | 25  | 1000 | 2045 |
| 500 | 16  | 1562 | 3196 |

(Каждые 22 удара — 1 рейс с 45 еды; формула: hits × portion / hitsneeded.)

**Регенерация поля** [^19]:

- При HP < FieldMaxHP **И** `visualstage=0` (HP ≥ 13000): каждые
  `cFieldRestartTime = 31.25` игровых секунд → `HP += floor(25000 × random × 0.1)`
  (то есть 0..2500 случайно).
- На стадиях <stage_0 (HP<13000) — НЕ регенерирует.

**Перезапуск поля** [^20]:

- HP=0 → `essential_death` → 21.875 игровых секунд → `essential_birth+visual_stage_0`.
- Затем `cFieldGrowTime = 4×21.875 = 87.5` игровых секунд роста (4 visual
  stages: 0→1→2→3). В это время `brised=False`, добывать нельзя.
- Полный простой: 21.875 + 87.5 = **109.375 игровых секунд**.

## 5. Шахты (gold/iron/coal)

**Здание:** `eurgol`, `euriro`, `eurcoa` (общий cluster `eur` для большинства;
`rusgol`/etc для `rus`/`ukr`; `turgol`/etc для `tur`/`alg`). Параметры [^21]:

| Параметр | Значение |
|---|---:|
| HP | 2500 |
| buildtime | 300 frames = 9.375 g-sec |
| Цена | W100 S100 (`costpercent=0` — не масштабируется) |
| `peasantabsorber` | **5** (макс 5 крестьян внутри) |
| `produce[gold/iron/coal]` | **13** |

**Механика:** крестьянин входит → `_unit_AddInside` [^22]:

```
gPlayer[pl].counter.resincome[i] += produce[i]   # +13 на каждого вошедшего
```

При выходе/смерти — соответствующее уменьшение.

**Income tick** [^23]:

```
const mult  = 100
const speed = 256/1.024 = 250
resincome_eff = resincome × gc_time_to_frames        # =13×32=416 на крестьянина
bank        += resincome_eff × deltatime
realbank     = bank / speed
delivered    = floor(realbank)                        # к плательщику
```

**Скорость на 1 крестьянина в шахте:**

- За 1 g-sec: bank gain = 13 × 32 × 1.0 = 416. realbank = 416/250 = **1.664** ресурса/g-sec ≈ **99.8/g-min**

**Полная шахта (5 крестьян, без апгрейдов):**

- 5 × 1.664 = **8.32 ресурса/g-sec** ≈ **499/g-min**

### 5.1 Mine upgrades — расширение вместимости

Каждая шахта имеет 6 индивидуальных апгрейдов (`<commonName><res>.1`..`.6`,
`bindividual=True` — нужно исследовать на каждой шахте отдельно). Type:
`gc_upg_type_single_inside_mine`. Эффект: `addpeasantabsorber += value`.
Время: 300 frames = 9.375 game-sec каждый [^24].

| Upgrade | +absorber | абсорбер после | Цена | Требование |
|---|---:|---:|---|---|
| `.1` | +5 | 10 | F1000, G1250 | — |
| `.2` | +8 | 18 | F5250, G4950 | — |
| `.3` | +10 | 28 | F12500, G9250 | — |
| `.4` | +12 | 40 | F15800, G18500 | 18 century |
| `.5` | +15 | 55 | F19800, G21050 | 18 century |
| `.6` | +40 | **95** | F50200, G25950 | 18 century |

**Полностью прокаченная одна шахта (95 peasants):**

- resincome += 95 × 13 = 1235
- 1235 × 32 / 250 = **158.08 ресурса/g-sec** ≈ **9 485/g-min**

Total cost full upgrade одной шахты: **F104 550, G80 950** (плюс 6 × 9.375 = **56.25 g-sec** пока крестьяне не работают).

⚠ Апгрейды per-mine, не глобальные. Если у вас 12 шахт, каждую качать отдельно.

## 6. Поля и fieldlife — апгрейды

**Type:** `gc_upg_type_fieldlifeperc` (ID 23). Эффект:
`gPlayer.fieldlife += value` (additive) [^25].

Найдены два апгрейда (стандартная eur-нация):

| Sid | upgplace | value | Цена | Источник |
|---|---|---:|---|---|
| `<csid>aca.4` | academy | +200 | F0 W1000 S0 G475 | [^26] |
| `<csid>bla.1` | blacksmith | +100 | F0 W400 S0 G90 | [^27] |

Суммарно при обоих: fieldlife = **300** → resdec=25 → 1000 hits/field → 2045 food/field.

⚠ Для нелатинских наций (`rus`, `ukr`, `tur`, `alg`, etc.) могут быть
нюансы, нужно перепроверять (но базовая формула общая).

## 7. Апгрейды efficiency (resefficiency)

Все апгрейды efficiency аддитивно добавляются к
`gPlayer.resefficiency[cid][restype]` (default 100):

| Type | restype |
|---|---|
| `gc_upg_type_effectfood` | food |
| `gc_upg_type_effectfoodperc` | food |
| `gc_upg_type_effectwood`/perc | wood |
| `gc_upg_type_effectstone`/perc | stone |

Наблюдаемые в `country.script` (mill upgrades — `<csid>mil.X` или `<commonName>mil.X`):

- mill `.1`: +40% food
- mill `.2`: +50% food
- mill `.3`: +50% food (требует уровень 2)
- aca `.8`: +100% wood (mill+blacksmith цепочка)
- aca `.23`: +100% stone, `.24`: +200% stone

⚠ Полный список на 21 нацию нужно достать через уже существующий
`parser/simulate_upgrades.py`. См. §9.

## 8. Карта как вход для модели

Полная процедура `DoGenerate` (cCircle1/2/3, SetupStartingResources, фазы
mines, FillOwnerMap, peacetime borders) — в
[map_generation_pipeline.md](../map/map_generation_pipeline.md). Ниже только то,
что нужно для extraction-формул.

### 8.1 Игровые параметры (наш контекст)

| UI label | Поле кода | Tag | Значение |
|---|---|---:|---|
| Map Shape | `terraintype` | 0 | Land |
| Terrain Type | `relieftype` | 3 | Highlands |
| Minerals | `resourcemines` | 2 | Rich |
| Map Size | `mapsize` | 3 | Tiny (256×256) |

Источники: `data/gui/menu.inc/showcustomgame.inc`, labels в
`data/locale/{en,ru}/{gui,new}.txt`.

**Важная деталь Highlands**: density гор (`mnt = 0.000120`) — максимальная
среди всех рельефов [^28]. Меньше ровных площадей под фермы/склады, больше
попыток placement фейлятся.

### 8.2 Терминология: месторождение vs шахта

*Месторождение* — геологическая залежь, помещаемая генератором (паттерны
`mng`/`mni`/`mnc`, basenames `minegold`/`mineiron`/`minecoal`).
*Шахта* — здание `eurgol`/`euriro`/`eurcoa`, строится крестьянином на
месторождении (`peasantabsorber=5`, до 95 с апгрейдами).

### 8.3 Сколько ресурсов на старте

**Месторождения.** На Tiny + Rich → 4 раунда × 3 типа = **12 месторождений
на игрока** (round 4 пропущен на tiny). Расстояния от старта: round 0 =
14-22 tiles (Phase 1, в `CreateStartPoint`), 1 = 32-42, 2 = 70-82, 3 =
22-38 (всё Phase 2). Подробности —
[map_generation_pipeline.md §8](../map/map_generation_pipeline.md#8-что-значит-phase-1-vs-phase-2-mines).

**Стартовые ресурсы вне mines.** В радиусе 5-22 тайла от центра города
всегда есть: **1× stoneforest, 2× stones, 3× forests** (medium/big,
foreststype=0 mix) через `SetupStartingResources`
([map_generation_pipeline.md §4](../map/map_generation_pipeline.md#4-setupstartingresourcespointx-pointy--что-спавнится-возле-города)).
Это объясняет, почему в начале игры всегда хватает дерева на ratuse +
первый mill ещё ДО общего forest spawn'а.

### 8.4 Леса и камни — densities + калибровка trees-per-pattern

> **`foreststype` всегда = 0 для Land.** Случайная инициализация
> `floor(RandomExt*3)` немедленно перезаписана нулём [^29]. `foreststype=1`
> (leaf-only) и =2 (mixed-only) на Land **не активируются**. Используется
> `foreststype=0` mix: pinefir/spruce/pine/pine_big_2 (big),
> pinefir/spruce/pine (mid), pinefir/pine (small).

Densities [^30]:

- `frs_big = 0.0009`, `frs_mid = 0.0009`, `frs_small = 0.00054`
- `stn1 = 0.00016`, `stn2 = 0.00012`
- `dcr = 0.0005` (декор)

Финальная density применяется через `_misc_SetupPatternsByType` [^31] с
тремя множителями:

1. `prob*` modifiers [^32] — Monte Carlo на 32000×4 пробах в 12/16/24/29-tile
   квадратах. Показывает «сколько свободного места» осталось после terrain
   placement.
2. Tiny modifier ×2.5 (`640/256`) на все `prob*`.
3. Per-call splits: `frs_big/8` на 4 типа леса, `frs_mid/6` на 3 типа,
   `frs_small/4` на 2 типа.

**Числа для Tiny + Highlands + Land** (источник:
[`compute/compute_map_resources.py`](../compute/compute_map_resources.py),
отчёт в [`docs/reports/map/map_resources.md`](../../../reports/map/map_resources.md)):

| Параметр | Значение |
|---|---:|
| Размер карты | 65536 тайлов (256×256) |
| `prob*` (после ×2.5 modifier) | ≈1.85-2.06 (зависит от размера паттерна) |
| Big forest clusters (placed, 65% success) | ~34 |
| Mid forest clusters | ~37 |
| Small forest clusters | ~23 |
| Stone clusters | ~21 |
| **Mask cell sum** (placement slots all types) | ~**27 000** на карту |
| **Calibrated chopable trees** (mask × 0.30) | ~**8 200** на карту |
| Камней всего на карте (calibrated) | ~**861** (mask × 0.30) |
| **Начальный wood pool** (сумма HP всех деревьев) | ~**40M wood units** |
| **Эффективный wood pool** | **∞** — пеньки бесконечны (см. §8.5) |
| **Месторождения** на игрока (Rich + Tiny) | **4 gold + 4 iron + 4 coal = 12** (4 раунда × 3 ресурса; round 4 пропущен на tiny) |

### Per-pattern-type tree counts (real data)

После расшифровки `data/game/var/generator.cfg` секции `PatternList`
сопоставляют тип паттерна (например, `forests_pine_big`) со списком
конкретных `.pattern` файлов. Парсер —
[`parser/parse_generator_cfg.py`](../../parser/parse_generator_cfg.py) →
`docs/derived/pattern_types.json`.

Кросс-tabulating с `pattern_inventory.json` (mask cell counts) →
`docs/derived/pattern_type_stats.json`:

| pattern type | n_files | min | **median** | max | example |
|---|---:|---:|---:|---:|---|
| forests_pine_big | 8 | 71 | **148** | 304 | `frt_b_p_1` |
| forests_pine_big_2 | 3 | 155 | **185** | 204 | `b_frt_b_p_1` |
| forests_pine_medium | 10 | 49 | **59** | 97 | `frt_m_p_1` |
| forests_pine_small | 6 | 21 | **44** | 46 | `frt_s_p_1` |
| forests_pinefir_big | 6 | 613 | **920** | 1494 | `d_frt_big_1` |
| forests_pinefir_medium | 6 | 218 | **311** | 383 | `d_frt_mid_1` |
| forests_pinefir_small | 6 | 80 | **172** | 200 | `d_frt_small_1` |
| forests_pinedrygreen_small | 4 | 367 | **629** | 638 | `d_frt_pinedry_*` |
| forests_spruce_big | 4 | 498 | **571** | 576 | spruce variants |
| forests_spruce_medium | 4 | 368 | **469** | 549 | |
| forests_leaf_big | 2 | 574 | **695** | 695 | `g_frt_big_1` |
| forests_leaf_medium | 2 | 388 | **514** | 514 | |
| forests_leaf_small | 6 | 122 | **250** | 450 | |
| forests_mixed_big | 3 | 1111 | **1631** | 2906 | `e_frt_big_1` |
| forests_mixed_medium | 5 | 656 | **895** | 1034 | |
| stoneforests | 8 | 121 | **152** | 164 | forest+stones |
| stones | 7 | 108 | **138** | 193 | `d_stn_*` |
| desert_stones | 12 | 53 | **74** | 101 | пустынный камень |
| **mng / mni / mnc** (mines) | 6 each | 32 | **32** | 32 | `mng_1` etc. — **= 1 deposit, не 32 объекта** |

### Что значит mask=1: РЕШЕНИЕ через empirical calibration

`mask=1` cells = **placement slots для env-объектов**, спавнятся C++
функцией `StandPatternWithAngle` (code недоступен).

**Mask cells содержат:** chopable trees (oak/pine/leaftree/...) + ground
decoration (drytree, decortree*, fallen logs, grass tufts, stumps). Engine
назначает variant_id → конкретный env-object class — но мы не видим этого
мэппинга.

**Empirical calibration (источник — пользователь, 2026-04-29):**

- Маленький лес (`forests_pine_small`, mask median 44): visible chopable trees ≈ **10** → ratio = 0.23
- Большой лес (`forests_pine_big`, mask median 148): visible chopable trees ≈ **50** → ratio = 0.34
- Average: **TREE_CHOPABLE_RATIO ≈ 0.30**

**Counter-examples (mask ≠ objects):**

- `mng/mni/mnc` (mines): все 18 файлов имеют ровно 32 mask клетки, но это
  **1 deposit per pattern** (mask = collision footprint). Не 32 шахты.
- `brush_plt_1x1` (4×4, 8 mask=1): = **8 видимых кустов** в игре — здесь
  1:1 (брыши плотные).

**Заключение:** для шахт `mask = footprint`, для брышей `mask = 1:1`, для
лесов `mask × 0.30 ≈ chopable trees`. Этот ratio зашит в
[`compute/compute_map_resources.py`](../compute/compute_map_resources.py)
как `TREE_CHOPABLE_RATIO`. Refine when more empirical data доступна.

### Pattern type → file mapping

При вызове `_misc_PlacePatternByType('forests_pine_big', envHnd, x, y)` [^33]
движок ищет в `gPatternList`, выбирает один файл по `Freq` весу и пытается
разместить через `_misc_CheckStandPatternExt`. После успеха вызывается
C++ `StandPatternWithAngle` — она и спавнит env-объекты (тело недоступно).

Для `foreststype=0` (default mix) карта вызывает 4 разных big-типа
(pinefir/spruce/pine/pine_big_2), 3 mid-типа, 2 small-типа. Каждый имеет
свой median tree count → итоговая выборка взвешена по freq и mask-density.

### 8.5 Пеньки — бесконечный wood pool (критично для симуляции)

Источник поведения — `OnAclAnimationReachedWork` плюс ontagstates
wood-death-handler [^3] [^15].

Жизненный цикл дерева:

1. **Spawn** [^14]: `brised := True`, HP назначается случайно по distribution
   (giant 8000-16000 / medium 125-624 / small 10-60 / stub 10).
2. **Каждый удар** крестьянина: `hp -= 1, peasant.resamount += 1`.
3. **При hp = 0**: `_unit_SetTagStates(trgHnd, gc_statetag_essential_death)`.
   Это триггерит ontagstates wood-death-handler:
   - mesh меняется на `pinestump<1..4>` (random)
   - `SetGameObjectCollisionInertiaByHandle(myHnd, False)`
   - **`brised` остаётся True** (никто его не сбрасывает на death)
4. **Пенек продолжает жить как валидная цель** для
   `_unit_SearchResourceInRadius` [^34] — только проверка `brised`, проверки
   HP нет.
5. Удары продолжаются: `hp -= 1` уходит в отрицательные значения (-1, -2, -3, ...).
   Условие `if hp = 0` срабатывает только один раз (при ровно 0), потому
   повторного перехода в death нет.
6. `peasant.resamount` инкрементится каждый удар → **дерево даёт wood до бесконечности**.

**Поведенческое следствие:** wood «end-game» нет. Wood всегда доступен;
единственное ограничение — пропускная способность peasants (1 hit/0.5625
g-sec = 3.56 wood/g-sec/peasant) и capacity (2 attackers/tree через
`gc_gameplay_resource_maxattackers_wood`).

**Почему peasants всё-таки предпочитают целые деревья?** Не из-за
HP-фильтра — из-за `attFactor` в score:
`tmpRDist = (1+dst/5)*(1+resdst/4)*(1+stoFactor)*(1+attFactor)`, где
`attFactor = 1+attcount*1.5` если ≥1 уже рубит. Поэтому свежее
не-рубленное дерево всегда ближе по «scoring distance», чем популярный
пень. Но если все деревья заняты, peasants идут на пеньки.

**Для симуляции:** wood pool = effectively infinite. Считаем только rate
(peasants × 3.56 wood/g-sec × eff/100) минус walk_overhead до склада.

## 9. Открытые вопросы

| # | Вопрос | Как решить |
|---:|---|---|
| 1 | ~~Точная скорость крестьянина~~ | ✅ **Закрыто:** `TrackPointMoveStep = 0.0375` × 32 кадра / g-sec = **1.20 тайла / g-sec** (см. §3 «Скорости движения» и [`internals/engine/animation_system.md` §2.4](../../../../internals/engine/animation_system.md)). |
| 2 | Полный список efficiency-апгрейдов по 21 нации | Использовать `parser/simulate_upgrades.py` (уже инлайнит SetUpgStruct и перебирает `case cid`). |
| 3 | Реальная стоимость хода к складу | Скорость теперь известна (см. вопрос 1) → дистанция × 1/1.20 g-sec/тайл. |
| 4 | Учёт `ferry` (доставка с изолированных островов леса) | Не критично для tiny+land, отложить. |
| 5 | `walkintervalfactor` — как влияет на анимацию ходьбы | Похоже скейлит animation speed относительно физической скорости. Отложить (см. также [`internals/engine/animation_system.md` §9](../../../../internals/engine/animation_system.md)). |

**Что нужно для уровня B (формулы):** §3-§7 покрывают всё.
Главный параметр — скорость крестьянина — закрыт через
`TrackPointMoveStep`.

**Что нужно для уровня C (симулятор):** дополнительно п. 2 (полный
список efficiency-апгрейдов).

---

## Источники

Все ссылки относительно `data/` в установке Cossacks 3.

[^1]: `gc_time_to_frames = 32` — `scripts/dmscript.global`.

[^2]: `gc_settings_gamespeed_*` — `scripts/dmscript.global:1027-1029`.

[^3]: `OnAclAnimationReachedWork` — `scripts/units/unit.inc/onaclanimationreachedwork.inc`.

[^4]: `gc_resource_hitsneeded_*` (food=22, wood=14, stone=20) и проверка `resamount >= hitsneeded` — `scripts/dmscript.global:799-801` и `scripts/lib/res.script:346-358`.

[^5]: `_unit_GetNearestStorehouse` — `scripts/lib/unit.script:9572-9604`.

[^6]: `_unit_PeasantAddResToPlayerByIndex` — `scripts/lib/unit.script:9544-9569`.

[^7]: Базовые порции `gc_obj_resource_portion_*` — `scripts/dmscript.global:803-806`.

[^8]: `_unit_SearchResourceInRadius` — `scripts/lib/unit.script:4041-4181`.

[^9]: Расширение search radius при `standtime>9` или `random>0.9` — `scripts/lib/unit.script:9824-9826`.

[^10]: Default `eff = 100` — `scripts/lib/player.script:109`.

[^11]: `gc_FieldMaxHP = 25000` — `scripts/dmscript.global:128`.

[^12]: `gc_obj_speed_*` — `scripts/dmscript.global:603-620`.

[^13]: `objbase.speed := gc_obj_speed_peasant` закомментировано в `scripts/lib/unit.script:1192`; глобальный `objbase.speed := 1` — `scripts/lib/unit.script:618`.

[^14]: HP distribution деревьев при спавне — `scripts/env/env.inc/initial.inc:79-89`.

[^15]: Переход дерево→пень — `scripts/env/env.inc/ontagstates.inc:50-78`.

[^16]: Скоринг кандидата ресурса — `scripts/lib/unit.script:4141-4145`.

[^17]: HP камня `10 000 000` — `scripts/env/env.inc/initial.inc:96`.

[^18]: HP поля устанавливается = `gc_FieldMaxHP` при `essential_birth → essential_none` — `scripts/env/env.inc/ontagstates.inc:119`.

[^19]: Регенерация поля (`cFieldRestartTime = 31.25`) — `scripts/env/env.inc/nothing.inc:78-87`.

[^20]: Перезапуск поля и `cFieldGrowTime = 87.5` — `scripts/env/env.inc/nothing.inc:31-34`.

[^21]: Параметры зданий `eurgol`/`euriro`/`eurcoa` — `scripts/lib/unit.script:2311-2323`.

[^22]: `_unit_AddInside` — `scripts/lib/unit.script:3016-3032`.

[^23]: Income tick — `scripts/lib/player.script:240-266`.

[^24]: Mine upgrades (`gc_upg_type_single_inside_mine`, addpeasantabsorber) — `scripts/lib/country.script:3871-3897`.

[^25]: `gc_upg_type_fieldlifeperc` (ID 23), `gPlayer.fieldlife += value` — `scripts/lib/player.script:1830-1832`.

[^26]: Upgrade `<csid>aca.4` (academy, +200 fieldlife) — `scripts/lib/country.script:3490`.

[^27]: Upgrade `<csid>bla.1` (blacksmith, +100 fieldlife) — `scripts/lib/country.script:3714`.

[^28]: Density гор Highlands `mnt = 0.000120` — `scripts/lib/dogenerate.inc:1640-1644`.

[^29]: `foreststype` всегда = 0 на Land — `scripts/lib/dogenerate.inc:5-6`.

[^30]: Densities (frs_big/mid/small, stn1/2, dcr) — `scripts/lib/dogenerate.inc:1688-1693`.

[^31]: `_misc_SetupPatternsByType` — `scripts/lib/misc.script:3681-3737`.

[^32]: `prob*` Monte Carlo modifiers — `scripts/lib/misc.script:3929-3941`.

[^33]: `_misc_PlacePatternByType` — `scripts/lib/misc.script:3655`.

[^34]: Поиск ресурса проверяет только `brised` (без проверки HP) — `scripts/lib/unit.script:4148`.
