# Recon: Cossacks 3 — peasant resource extraction (модель добычи)

Цель: модель скорости добычи всех ресурсов с учётом всей логики игры. Уровень B (формулы + шахты + поля + апгрейды), потенциал C (симулятор).

**Контекст по умолчанию:**
- Game speed = **fast (2)**, множитель **1.4×** относительно нормальной (см. §1).
- Карта: terraintype=**0 Land**, relieftype=**3 Highlands**, resourcemines=**2 Rich/Many**, mapsize=**3 Tiny/Small (256×256)**.
- Все ссылки относятся к `C:\Program Files (x86)\Steam\steamapps\common\Cossacks 3\data\`.

> **Связанные документы:**
> - [determinism_audit.md](determinism_audit.md) — почему добыча не воспроизводима (RNG-сайты в hot-path), какой ожидать разброс при эмпирической калибровке этой модели.
> - [ticks_and_subticks.md](ticks_and_subticks.md) — модель времени, sub-tick state machine, adaptive game speed. **Критично для трактовки real-time vs game-time** при замерах.
> - [server_sync_architecture.md](server_sync_architecture.md) — server-authoritative модель C3, почему single-player и MP ведут себя по-разному.
>
> **TL;DR для этой модели:** аналитический потолок (формулы ниже) считаем в **game-time**. Реальная in-game добыча будет ниже из-за RNG-выборов в `_misc_FindResourceToExtract` ([determinism_audit.md](determinism_audit.md) §3). Разброс между запусками одного сейва ожидается 5-15%; шахты — 0%.

---

## 1. Игровая скорость и время

**Базовый тик:** `gc_time_to_frames = 32` ([dmscript.global](C:/Program Files (x86)/Steam/steamapps/common/Cossacks 3/data/scripts/dmscript.global)) — 32 кадра в одной игровой секунде. Все длительности в скриптах в "frames" нужно делить на 32 для перевода в **игровые секунды (game-time)**.

**Скорости игры** (`gc_settings_gamespeed_*`, dmscript.global:1027-1029):
| Mode | Tag | speedfactor | game-time : real-time |
|---|---:|---:|---|
| 0 (slow)   | 7  | 0.7× | 1 game-sec = 1.43 real-sec |
| 1 (normal) | 10 | 1.0× | 1 game-sec = 1.00 real-sec |
| **2 (fast)** | **14** | **1.4×** | **1 game-sec = 0.714 real-sec** |

**Вывод для расчётов:** все формулы ниже даны в **игровых секундах**. Для game speed 2 умножайте rate на 1.4 чтобы получить real-time rate, или делите длительности на 1.4.

## 2. Цикл добычи (поведение)

Пайплайн одного крестьянина:

1. **Удар (work tick).** При работе анимация `workfood`/`workwood`/`workstone` цикл = N кадров. По достижении конца цикла:
    - срабатывает `OnAclAnimationReachedWork` ([units/unit.inc/onaclanimationreachedwork.inc](C:/Program Files (x86)/Steam/steamapps/common/Cossacks 3/data/scripts/units/unit.inc/onaclanimationreachedwork.inc)).
    - `arg_obj.resamount += 1` — увеличивается счётчик "ударов" в инвентаре.
    - HP ресурса уменьшается:
      - food: `-= Max(1, floor(100/(1+fieldlife/100)))`. Default fieldlife=0 → 100 HP/удар.
      - wood: `-= 1`. При HP=0 → дерево становится пнём (см. §4.2).
      - stone: `-= 1`. Stone HP = 10 000 000, фактически бесконечно.

2. **Возврат к складу.** Когда `resamount >= hitsneeded` ([res.script:346-358](C:/Program Files (x86)/Steam/steamapps/common/Cossacks 3/data/scripts/lib/res.script#L346)):
    - food: 22, wood: 14, stone: 20 ударов.
    - Запускается `_unit_GetNearestStorehouse` ([unit.script:9572-9604](C:/Program Files (x86)/Steam/steamapps/common/Cossacks 3/data/scripts/lib/unit.script#L9572)) — поиск по списку `gPlayer[pl].lists.storehouses`. Учитываются здания с `usage=storage/mill/center` и `resourcebase[restype]=True`.
    - Цель — `resourcePoint` склада (точка сдачи на конкретном tile-offset от позиции здания).

3. **Сдача.** При попадании в радиус `gc_gameplay_resourceDropRadiusSqr = 0.5` (≈0.707 тайла):
    - `_unit_PeasantAddResToPlayerByIndex` → `delivered = (portion × eff) / 100` ([unit.script:9544-9569](C:/Program Files (x86)/Steam/steamapps/common/Cossacks 3/data/scripts/lib/unit.script#L9544)).
    - Базовые порции (`gc_obj_resource_portion_*`, dmscript.global:803-806): food=**45**, wood=**28**, stone=**40**, прочее=**20**.
    - `eff` — `gPlayer[pl].resefficiency[cid][restype]`, стартует со 100, апгрейды добавляют (см. §7).
    - `restype := none`, `resamount := 0`, поиск нового ресурса.

4. **Re-acquire.** `_unit_SearchResourceInRadius` ([unit.script:4041-4181](C:/Program Files (x86)/Steam/steamapps/common/Cossacks 3/data/scripts/lib/unit.script#L4041)) около **исходной точки задачи** (`TOrderInfo.x/y`):
    - Стандартный радиус: `gc_obj_res_searchradius = 6` тайлов.
    - Если `standtime>9` или `random>0.9` → расширение до `2× = 12` тайлов.
    - Скоринг кандидатов: `score = (1+myDst/5) × (1+resDst/4) × (1+stoFactor) × (1+attFactor)`. attFactor/stoFactor штрафуют ресурс, к которому уже идут другие.
    - Только `brised=True`. Лимит конкурентных добытчиков на ресурс: food=**3**, wood=**2**, stone=**3**.

## 3. Константы (extracted)

### Анимация — кадры одного work-цикла

Из [data/animations/aaf/peaaus.aaf](C:/Program Files (x86)/Steam/steamapps/common/Cossacks 3/data/animations/aaf/peaaus.aaf) (одинаково для всех наций кроме pearus):

| Cycle | Frames | game-sec @ 32fps | real-sec @ fast |
|---|---:|---:|---:|
| workfood (aus,fra,eng,...) | 22 | 0.6875 | 0.491 |
| workfood (rus) | 23 | 0.7188 | 0.513 |
| workwood | 18 | 0.5625 | 0.402 |
| workstone | 18 | 0.5625 | 0.402 |
| walk | 20 | 0.625 | 0.446 |
| walkfood | 20 | 0.625 | 0.446 |
| walkwood | 20 | 0.625 | 0.446 |
| walkstone | 20 | 0.625 | 0.446 |

⚠ Ключевое допущение: animation frame rate совпадает с `gc_time_to_frames=32`. Это не гарантировано — нужен empirical check (см. §9).

### Базовые числа добычи

| Параметр | Значение | Источник |
|---|---:|---|
| `gc_obj_resource_portion_food` | 45 | dmscript.global:804 |
| `gc_obj_resource_portion_wood` | 28 | dmscript.global:805 |
| `gc_obj_resource_portion_stone` | 40 | dmscript.global:806 |
| `gc_obj_resource_portion_others` | 20 | unit.script:9551 |
| `gc_resource_hitsneeded_food` | 22 | dmscript.global:799 |
| `gc_resource_hitsneeded_wood` | 14 | dmscript.global:800 |
| `gc_resource_hitsneeded_stone` | 20 | dmscript.global:801 |
| Default `eff` | 100 | player.script:109 |
| `gc_FieldMaxHP` | 25 000 | dmscript.global:128 |

### Радиусы и расстояния

| Параметр | Значение (тайлы) | Назначение |
|---|---:|---|
| `gc_obj_res_searchradius` | 6 | base search radius после сдачи |
| (расширение при standtime) | до 12 (2×) | unit.script:9824-9826 |
| `gc_obj_extract_food_radiusmax` | 1.5 (=80×0.01875) | дальность "удара" поля |
| `gc_obj_extract_wood_radiusmax` | 0.75 (=40×0.01875) | дальность "удара" дерева |
| `gc_obj_extract_stone_radiusmax` | 0.9375 (=50×0.01875) | дальность "удара" камня |
| `gc_gameplay_resourceDropRadiusSqr` | 0.5 (sqrt≈0.707) | радиус сдачи у склада |

### Скорости (абстрактные ед., не тайлы/сек)

`gc_obj_speed_*` ([dmscript.global:603-620](C:/Program Files (x86)/Steam/steamapps/common/Cossacks 3/data/scripts/dmscript.global#L603)):
- default = 32
- **peasant = 40**
- hardhorse = 56, fasthorse = 96, cannon = 20, mortar = 24

⚠ В скриптах строки `objbase.speed := gc_obj_speed_peasant` закомментированы ([unit.script:1192](C:/Program Files (x86)/Steam/steamapps/common/Cossacks 3/data/scripts/lib/unit.script#L1192)). Глобально `objbase.speed := 1` ([unit.script:618](C:/Program Files (x86)/Steam/steamapps/common/Cossacks 3/data/scripts/lib/unit.script#L618)). Скорость, видимо, читается из actor/mesh файлов или применяется через анимационный walkInterval. Для конверсии в тайлы/сек **нужен empirical test**: переместить крестьянина из (0,0) в (40,0) на normal speed и засечь время в секундах.

### Конкурентные добытчики на одном ресурсе

`gc_gameplay_resource_maxattackers_*`:
- food = 3, wood = **2**, stone = 3, none = 4

## 4. Per-resource математика

### 4.1 Идеальный rate (без хождения)

Для одного крестьянина, без учёта дороги к складу, при eff=100, fieldlife=0:

```
rate_per_trip = portion × eff / 100             # ресурс за поход
time_per_trip_game = hitsneeded × t_hit_game    # игровых секунд
rate = rate_per_trip / time_per_trip_game       # ресурс/игровая_сек
```

| Ресурс | portion | hitsneeded | t_hit_game | rate (units/game-sec) | rate @ fast (units/real-sec) |
|---|---:|---:|---:|---:|---:|
| food (default eff) | 45 | 22 | 0.6875 | 45/(22×0.6875) = **2.975** | 4.165 |
| wood | 28 | 14 | 0.5625 | 28/(14×0.5625) = **3.556** | 4.978 |
| stone | 40 | 20 | 0.5625 | 40/(20×0.5625) = **3.556** | 4.978 |

⚠ Это **верхняя граница** — реальный rate ниже из-за дороги к складу.

### 4.2 Wood — большие/средние/мелкие деревья

При спавне случайно ([env/env.inc/initial.inc:79-89](C:/Program Files (x86)/Steam/steamapps/common/Cossacks 3/data/scripts/env/env.inc/initial.inc#L79)):

| Шанс | HP | Тип | Ударов до пенька | Дерева на дереве (round/floor) |
|---:|---|---|---:|---:|
| 20% | floor(8000×(1+random)) = 8000..16000 | **гигант** | 8000..16000 | ~571..1142 ударов = ~40..80 рейсов = ~16k..32k wood |
| 15% | floor(125×(1+random×4)) = 125..624 | средний | 125..624 | ~9..45 рейсов = ~250..1200 wood |
| 45% | floor(10+rnd×(0.5+random×0.5)×100) = 10..~60 | мелкий | 10..60 | 1..4 рейса = ~28..112 wood |
| 20% | 10 | "пенёк" | 10 | <1 рейс = ~20 wood |

**Среднее ожидание HP** (грубо):
- 0.2 × 12000 + 0.15 × 375 + 0.45 × 35 + 0.2 × 10 ≈ **2474 HP** на дерево
- При 14 hits/trip = ~177 рейсов на одно "среднее" дерево, или ~4956 wood/дерево.

**Переход дерево→пень** ([env/env.inc/ontagstates.inc:50-78](C:/Program Files (x86)/Steam/steamapps/common/Cossacks 3/data/scripts/env/env.inc/ontagstates.inc#L50)):
- При HP=0 → `gc_statetag_essential_death` → меш меняется на `pinestump1..4` (распределение 70/20/5/5%), `collisioninertia=False`.
- `brised` для wood **никогда не выставляется в False** в коде (в отличие от food, где flag используется для замедления роста). Пень остаётся валидным ресурсом в `gResGrid`, search его видит, итип=wood сохраняется.

**Предпочтение целых деревьев — emergent через penalty queueing.** В скоринге кандидата ([unit.script:4141-4145](C:/Program Files (x86)/Steam/steamapps/common/Cossacks 3/data/scripts/lib/unit.script#L4141)):

```
score = (1 + dstMy/5) × (1 + dstRes/4) × (1 + stoFactor) × (1 + attFactor)
attFactor = 1 + attcount × 1.5    if attcount ≥ 1, else 0
stoFactor = 1 + stocount × 1.5    if stocount ≥ 1, else 0
```

`attcount` = сейчас рубят, `stocount` = сейчас идут к нему. `dstMy` — расстояние от крестьянина, `dstRes` — расстояние от исходной точки задания. **Минимальный score побеждает.**

Эффект: ресурс с 1 активным рубщиком получает множитель ×(1+2.5) = **×3.5** к скору. Целое дерево без рубщиков рядом всегда побеждает пень с рубщиком в 2-3 тайлах. Так возникает наблюдаемое предпочтение — **не из-за того, что это пень, а из-за того, что на пне уже работают**.

**Пустой пень vs целое дерево, оба без рубщиков** — побеждает ближний по дистанции, без штрафа. Когда лес вырублен (все стали пнями), крестьяне работают по ним равномерно, без избегания.

**Крест-овер дистанций** (примерно): пень с 1 рубщиком на 2 тайлах проигрывает целому дереву на ≤8 тайлах. Но search radius = 6 тайлов, так что эффективная зона — ~3-5 тайлов "форы" целому дереву над занятым пнём.

**Hard cap:** при `attcount ≥ maxattackers=2` для wood ресурс полностью фильтруется (75% времени, 25% шанс обхода через `bskipcheck = random>0.75`).

### 4.3 Stone — фактически бесконечный

HP = 10 000 000 ([initial.inc:96](C:/Program Files (x86)/Steam/steamapps/common/Cossacks 3/data/scripts/env/env.inc/initial.inc#L96)). Один камень держит 10M ударов = 500k рейсов = 20M камня. Бесконечно для практических целей. Все расчёты для stone — без учёта истощения.

### 4.4 Food — поле с регенерацией

**HP поля:** старт = 0, при `essential_birth → essential_none` устанавливается = `gc_FieldMaxHP = 25000` ([ontagstates.inc:119](C:/Program Files (x86)/Steam/steamapps/common/Cossacks 3/data/scripts/env/env.inc/ontagstates.inc#L119)).

**Урон полю за удар:** `resdec = Max(1, floor(100/(1+fieldlife/100)))`.

| fieldlife | resdec/удар | макс ударов до 0 HP | макс food (при eff=100) |
|---:|---:|---:|---:|
| 0   | 100 | 250 | 250 × 45/22 = **511** |
| 100 | 50  | 500 | 1023 |
| 200 | 33  | ~757 | 1549 |
| 300 | 25  | 1000 | 2045 |
| 500 | 16  | 1562 | 3196 |

(Каждые 22 удара — 1 рейс с 45 еды; формула: hits × portion / hitsneeded.)

**Регенерация поля** ([env/env.inc/nothing.inc:78-87](C:/Program Files (x86)/Steam/steamapps/common/Cossacks 3/data/scripts/env/env.inc/nothing.inc#L78)):
- При HP < FieldMaxHP **И** visualstage=0 (HP ≥ 13000): каждые `cFieldRestartTime = 31.25` игровых секунд → `HP += floor(25000 × random × 0.1)` (то есть 0..2500 случайно).
- На стадиях <stage_0 (HP<13000) — НЕ регенерирует.

**Перезапуск поля** ([nothing.inc:31-34](C:/Program Files (x86)/Steam/steamapps/common/Cossacks 3/data/scripts/env/env.inc/nothing.inc#L31)):
- HP=0 → `essential_death` → 21.875 игровых секунд → `essential_birth+visual_stage_0`.
- Затем `cFieldGrowTime = 4×21.875 = 87.5` игровых секунд роста (4 visual stages: 0→1→2→3). В это время `brised=False`, добывать нельзя.
- Полный простой: 21.875 + 87.5 = **109.375 игровых секунд** = 78.1 real sec @ fast.

## 5. Шахты (gold/iron/coal)

**Здание:** `eurgol`, `euriro`, `eurcoa` (общий cluster `eur` для большинства; `rusgol`/etc для rus/ukr; `turgol`/etc для tur/alg). Параметры ([unit.script:2311-2323](C:/Program Files (x86)/Steam/steamapps/common/Cossacks 3/data/scripts/lib/unit.script#L2311)):

| Параметр | Значение |
|---|---:|
| HP | 2500 |
| buildtime | 300 frames = 9.375 game-sec = 6.7 real-sec @ fast |
| Цена | W100 S100 (`costpercent=0` — не масштабируется) |
| `peasantabsorber` | **5** (макс 5 крестьян внутри) |
| `produce[gold/iron/coal]` | **13** |

**Механика:** крестьянин входит → `_unit_AddInside` ([unit.script:3016-3032](C:/Program Files (x86)/Steam/steamapps/common/Cossacks 3/data/scripts/lib/unit.script#L3016)):
```
gPlayer[pl].counter.resincome[i] += produce[i]   # +13 на каждого вошедшего
```

При выходе/смерти — соответствующее уменьшение.

**Income tick** ([player.script:240-266](C:/Program Files (x86)/Steam/steamapps/common/Cossacks 3/data/scripts/lib/player.script#L240)):
```
const mult  = 100
const speed = 256/1.024 = 250
resincome_eff = resincome × gc_time_to_frames        # =13×32=416 на крестьянина
bank        += resincome_eff × deltatime
realbank     = bank / speed
delivered    = floor(realbank)                        # к плательщику
```

**Скорость на 1 крестьянина в шахте:**
- За 1 игровую секунду: bank gain = 13 × 32 × 1.0 = 416. realbank = 416/250 = **1.664** ресурса/game-sec
- ≈ 99.84 ресурса/game-min
- @ game speed 2 (fast): **2.330 ресурса/real-sec на крестьянина** ≈ **139.7/real-min**

**Полная шахта (5 крестьян, без апгрейдов):**
- 5 × 1.664 = **8.32 ресурса/game-sec**
- @ fast: **11.65 ресурса/real-sec** ≈ **699/real-min**

### 5.1 Mine upgrades — расширение вместимости

Каждая шахта имеет 6 индивидуальных апгрейдов (`<commonName><res>.1`..`.6`, `bindividual=True` — нужно исследовать на каждой шахте отдельно). Type: `gc_upg_type_single_inside_mine`. Эффект: `addpeasantabsorber += value`.

Источник: [country.script:3871-3897](C:/Program Files (x86)/Steam/steamapps/common/Cossacks 3/data/scripts/lib/country.script#L3871). Время: 300 frames = 9.375 game-sec каждый.

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
- per game-sec: 1235 × 32 / 250 = **158.08 ресурса/game-sec**
- @ fast: **221.3 ресурса/real-sec** ≈ **13 278/real-min**

Total cost full upgrade одной шахты: **F104 550, G80 950** (плюс 6 × 9.375 = **56.25 game-sec** = 40.2 real-sec @ fast пока крестьяне не работают).

⚠ Апгрейды per-mine, не глобальные. Если у вас 12 шахт, каждую качать отдельно.

## 6. Поля и fieldlife — апгрейды

**Type:** `gc_upg_type_fieldlifeperc` (ID 23). Эффект ([player.script:1830-1832](C:/Program Files (x86)/Steam/steamapps/common/Cossacks 3/data/scripts/lib/player.script#L1830)): `gPlayer.fieldlife += value` (additive).

Найдены два апгрейда (стандартная eur-нация):
| Sid | upgplace | value | Цена | Источник |
|---|---|---:|---|---|
| `<csid>aca.4` | academy | +200 | F0 W1000 S0 G475 | country.script:3490 |
| `<csid>bla.1` | blacksmith | +100 | F0 W400 S0 G90 | country.script:3714 |

Суммарно при обоих: fieldlife = **300** → resdec=25 → 1000 hits/field → 2045 food/field.

⚠ Для нелатинских наций (rus, ukr, tur, alg, etc.) могут быть нюансы, нужно перепроверять (но базовая формула общая).

## 7. Апгрейды efficiency (resefficiency)

Все апгрейды efficiency аддитивно добавляются к `gPlayer.resefficiency[cid][restype]` (default 100):

| Type | restype |
|---|---|
| `gc_upg_type_effectfood` | food |
| `gc_upg_type_effectfoodperc` | food |
| `gc_upg_type_effectwood`/perc | wood |
| `gc_upg_type_effectstone`/perc | stone |

Наблюдаемые в country.script (mill upgrades — `<csid>mil.X` или `<commonName>mil.X`):
- mill `.1`: +40% food
- mill `.2`: +50% food
- mill `.3`: +50% food (требует уровень 2)
- aca `.8`: +100% wood (mill+blacksmith цепочка)
- aca `.23`: +100% stone, `.24`: +200% stone

⚠ Полный список на 21 нацию нужно достать через уже существующий `parser/simulate_upgrades.py`. См. §9.

## 8. Параметры генерации карты

### 8.1 Параметры в UI и индексы в коде

| UI label | Поле кода | Tag (наш выбор) | Значение |
|---|---|---:|---|
| Тип карты (Map Shape) | `terraintype` | **0** | Land (Суша) |
| Вид рельефа (Terrain Type) | `relieftype` | **3** | Highlands |
| Ресурсы (Minerals) | `resourcemines` | **2** | Rich (Много) |
| Размер карты | `mapsize` | **3** | Tiny (Маленькая, 256×256 тайлов) |

Источники UI: [data/gui/menu.inc/showcustomgame.inc](C:/Program Files (x86)/Steam/steamapps/common/Cossacks 3/data/gui/menu.inc/showcustomgame.inc), labels в [data/locale/ru/new.txt](C:/Program Files (x86)/Steam/steamapps/common/Cossacks 3/data/locale/ru/new.txt) и [data/locale/en/gui.txt:423-460](C:/Program Files (x86)/Steam/steamapps/common/Cossacks 3/data/locale/en/gui.txt#L423).

### 8.2 Highlands — рельеф (relieftype=3)

[dogenerate.inc:1640-1644](C:/Program Files (x86)/Steam/steamapps/common/Cossacks 3/data/scripts/common.inc/dogenerate.inc#L1640): плотности паттернов:
- `plt = 0.000055` (плато)
- `mnt = 0.000120` (горы) — **самый высокий из всех типов**
- `hil = 0.000050` (холмы)

Сравнение всех рельефов:
| Type | Name | plt | mnt | hil | Заметка |
|---:|---|---:|---:|---:|---|
| 0 | Plain | 0.000010 | 0.000020 | 0.000075 | мало рельефа |
| 1 | Low Mtn | 0.000020 | 0.000002 | 0.000125 | холмов больше |
| 2 | High Mtn | 0.000075 | 0.000075 | 0.000030 | горы+плато |
| **3** | **Highlands** | **0.000055** | **0.000120** | **0.000050** | максимум гор |
| 4 | Plateaus | 0.000090 | 0.000035 | 0.000035 | плато доминируют |

**Импликация для добычи:** на Highlands у вас будет много гор → меньше открытых ровных площадей под лес и поля → плотность лесов и полей может фактически снизиться из-за collision masks (трудно ставить дома, фермы, склады).

### 8.3 Resources=Rich, Tiny map — месторождения

**Терминология.** *Месторождение* — это геологическая залежь, помещаемая на карту генератором (basenames `minegold`/`mineiron`/`minecoal` через паттерны `mng`/`mni`/`mnc`). *Шахта* — это здание `eurgol`/`euriro`/`eurcoa`, которое игрок строит крестьянином на месторождении и куда потом могут заходить рабочие (peasantabsorber=5, до 95 с апгрейдами).

[dogenerate.inc:522-717](C:/Program Files (x86)/Steam/steamapps/common/Cossacks 3/data/scripts/common.inc/dogenerate.inc#L522): процедура `SetupMines(pointx, pointy, minround, maxround, minesdensity, spcount)`.

`rounds = case minesdensity of 0:3, 1:4, 2:5`. Для нас (minesdensity=2) **rounds=5** (раундов = "колец" вокруг стартовой точки).

**Структура размещения** (вложенные циклы):
- Внешний цикл `for i := 0 to rounds-1` — раунды.
- Внутренний цикл `for j := 0 to 2` — по типам ресурсов (j=0 gold, j=1 iron, j=2 coal).
- Внутренний-внутренний `for k := 0 to 255` — до 256 попыток найти валидное место. После успеха — `break` (line 712).

То есть **в каждом (раунд, тип ресурса) ставится ровно 1 месторождение** (или фейл при 256 неудачах).

Phase 1 (внутри `CreateStartPoint`, [dogenerate.inc:985](C:/Program Files (x86)/Steam/steamapps/common/Cossacks 3/data/scripts/common.inc/dogenerate.inc#L985)): только раунд i=0.
Phase 2 (после генерации террейна, [dogenerate.inc:1770](C:/Program Files (x86)/Steam/steamapps/common/Cossacks 3/data/scripts/common.inc/dogenerate.inc#L1770)): раунды i=1..rounds-1.

Расстояния от старта (game version ≥ 80, mapsize>2 = tiny):
| Раунд i | dst (tiles) | Phase | Что ставится |
|---:|---|:---:|---|
| 0 | 14..22 | Phase 1 (close) | 1 gold + 1 iron + 1 coal |
| 1 | 32..42 | Phase 2 | 1 gold + 1 iron + 1 coal |
| 2 | 70..82 | Phase 2 | 1 gold + 1 iron + 1 coal |
| 3 | 22..38 | Phase 2 | 1 gold + 1 iron + 1 coal |
| 4 | continue | — | пропущено на tiny |

**Итого** на игрока: **4 месторождения каждого типа** (4 gold + 4 iron + 4 coal = **12 месторождений всего**), при условии что все 12 попыток размещения нашли валидное место в пределах 256 попыток каждая. На tiny+highlands часть попыток может фейлиться из-за гор/воды/других объектов в радиусе.

### 8.4 Леса и камни — densities (вне шахт)

[dogenerate.inc:1688-1693](C:/Program Files (x86)/Steam/steamapps/common/Cossacks 3/data/scripts/common.inc/dogenerate.inc#L1688):
- `frs_big = 0.0009`, `frs_mid = 0.0009`, `frs_small = 0.00054`
- `stn1 = 0.00016`, `stn2 = 0.00012`
- `dcr = 0.0005` (декор)

Финальная density применяется через `_misc_SetupPatternsByType` ([misc.script:3681-3737](C:/Program Files (x86)/Steam/steamapps/common/Cossacks 3/data/scripts/lib/misc.script#L3681)):
```
needed = floor(mapW × mapH × freq)   # сколько паттернов запрашивается
trycount = 256 × mapsizeoptimise     # попыток разместить каждый
```
На tiny `mapsizeoptimise = (320×320)/(256×256) = 1.5625`, trycount=400. После terrain placement много попыток фейлятся.

Densities умножаются на:
1. `prob*` modifiers ([misc.script:3929-3941](C:/Program Files (x86)/Steam/steamapps/common/Cossacks 3/data/scripts/lib/misc.script#L3929)) — Monte Carlo прогон 32000×4 на 12/16/24/29-tile квадратах, делёный на калибровочные 340/182/74/55. Результат показывает "сколько свободного места под паттерны данного размера".
2. Tiny modifier ×2.5 (`640/256`) на все prob*.
3. Per-call splits: `frs_big/8` на 4 типа леса, `frs_mid/6` на 3 типа, `frs_small/4` на 2 типа.

**Конкретные числа для Tiny + Highlands + Land** (см. полный отчёт в [`output/cossacks3_map_resources.md`](../output/cossacks3_map_resources.md), генератор [`parser/compute_map_resources.py`](../parser/compute_map_resources.py)):

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

После расшифровки [`data/game/var/generator.cfg`](C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/game/var/generator.cfg) — `PatternList` секции мапят тип паттерна (типа `forests_pine_big`) на список конкретных `.pattern` файлов. Парсер: [`parser/parse_generator_cfg.py`](../parser/parse_generator_cfg.py) → `output/derived/pattern_types.json`.

Кросс-tabulating с `pattern_inventory.json` (mask cell counts) → `output/derived/pattern_type_stats.json`:

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

`mask=1` cells = **placement slots для env-объектов**, спавнятся C++ функцией [`StandPatternWithAngle`](C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/misc.script#L3390) (code недоступен).

**Mask cells содержат:** chopable trees (oak/pine/leaftree/...) + ground decoration (drytree, decortree*, fallen logs, grass tufts, stumps). Engine назначает variant_id → конкретный env-object class — но мы не видим этого мэппинга.

**Empirical calibration (источник — пользователь, 2026-04-29):**
- Маленький лес (`forests_pine_small`, mask median 44): visible chopable trees ≈ **10** → ratio = 0.23
- Большой лес (`forests_pine_big`, mask median 148): visible chopable trees ≈ **50** → ratio = 0.34
- Average: **TREE_CHOPABLE_RATIO ≈ 0.30**

**Counter-examples (mask ≠ objects):**
- 🪨 `mng/mni/mnc` (mines): все 18 файлов имеют ровно 32 mask клетки, но это **1 deposit per pattern** (mask = collision footprint). Не 32 шахты.
- 🌿 `brush_plt_1x1` (4×4, 8 mask=1): = **8 видимых кустов** в игре — здесь 1:1 (брыши плотные).

**Заключение:** для шахт `mask = footprint`, для брышей `mask = 1:1`, для лесов `mask × 0.30 ≈ chopable trees`. Этот ratio зашит в [`compute/compute_map_resources.py`](../compute/compute_map_resources.py) как `TREE_CHOPABLE_RATIO`. Refine when more empirical data доступна.

### Pattern type → file mapping

При вызове `_misc_PlacePatternByType('forests_pine_big', envHnd, x, y)` ([`misc.script:3655`](C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/misc.script#L3655)) движок ищет в `gPatternList`, выбирает один файл по `Freq` весу и пытается разместить через `_misc_CheckStandPatternExt`. После успеха вызывается `StandPatternWithAngle` — это ОНА спавнит env-объекты (источник недоступен).

Для `foreststype=0` (default mix) карта вызывает 4 разных big-типа (pinefir/spruce/pine/pine_big_2), 3 mid-типа, 2 small-типа. Каждый имеет свой median tree count → итоговая выборка взвешена по freq и mask-density.

### Pattern type → file mapping

При вызове `_misc_PlacePatternByType('forests_pine_big', envHnd, x, y)` ([`misc.script:3655`](C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/misc.script#L3655)) движок ищет в `gPatternList`, выбирает один файл по `Freq` весу и пытается разместить через `_misc_CheckStandPatternExt`. Для `foreststype=0` (default mix) карта вызывает 4 разных big-типа, 3 mid-типа, 2 small-типа. Каждый имеет свой median tree count → итоговая выборка взвешена по freq и mask-density.

## 8.5 Пеньки — бесконечный wood pool (КРИТИЧНО для симуляции)

**Источник:** [`onaclanimationreachedwork.inc:30-39`](C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/units/unit.inc/onaclanimationreachedwork.inc) + [`ontagstates.inc:50-78`](C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/env/env.inc/ontagstates.inc).

Жизненный цикл дерева:
1. **Spawn** ([`initial.inc:75-93`](C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/env/env.inc/initial.inc)): `brised := True`, HP назначается случайно по distribution (giant 8000-16000 / medium 125-624 / small 10-60 / stub 10).
2. **Каждый удар** крестьянина: `hp -= 1, peasant.resamount += 1`.
3. **При hp = 0**: `_unit_SetTagStates(trgHnd, gc_statetag_essential_death)`. Это триггерит ontagstates wood-death-handler:
   - mesh меняется на `pinestump<1..4>` (random)
   - `SetGameObjectCollisionInertiaByHandle(myHnd, False)`
   - **`brised` остаётся True** (никто его не сбрасывает на death)
4. **Пенек продолжает жить как валидная цель** для `_unit_SearchResourceInRadius` ([`unit.script:4148`](C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/unit.script): `if brised then ...` — проверки HP нет).
5. Удары продолжаются: `hp -= 1` уходит в отрицательные значения (-1, -2, -3, ...). Условие `if hp = 0` срабатывает только один раз (при ровно 0), потому повторного перехода в death нет.
6. `peasant.resamount` инкрементится каждый удар → **дерево даёт wood до бесконечности**.

**Поведенческое следствие:** wood «end-game» нет. Wood всегда доступен; единственное ограничение — пропускная способность peasants (1 hit/0.5625 g-sec = 3.56 wood/g-sec/peasant) и capacity (2 attackers/tree через `gc_gameplay_resource_maxattackers_wood`).

**Почему peasants всё-таки предпочитают целые деревья?** Не из-за HP-фильтра — из-за `attFactor` в score: `tmpRDist = (1+dst/5)*(1+resdst/4)*(1+stoFactor)*(1+attFactor)`, где `attFactor = 1+attcount*1.5` если ≥1 уже рубит. Поэтому свежее не-рубленное дерево всегда ближе по «scoring distance», чем популярный пень. Но если все деревья заняты, peasants идут на пеньки.

**Для симуляции:** wood pool = effectively infinite. Считаем только rate (peasants × 3.56 wood/g-sec × eff/100) минус walk_overhead до склада.

## 9. Открытые вопросы (на следующий этап)

| # | Вопрос | Как решить |
|---:|---|---|
| 1 | Точная скорость крестьянина в **тайлах/игр-сек** | Empirical test: построить 2 склада на расстоянии X, перевести крестьянина, засечь время; либо найти actor frame rate. |
| 2 | ~~Frame rate AAF-анимаций (32 fps?)~~ | **РЕШЕНО**: 32 fps — это `gc_time_to_frames` из dmscript.global:175, реальная engine constant. Не допущение. AAF-парсер написан: `compute/compute_animations.py` → `output/derived/animations.json`. |
| 3 | ~~`brised=False` для срубленных деревьев — есть ли где?~~ | **РЕШЕНО**: brised для wood никогда не меняется. Предпочтение целых деревьев работает через attFactor/stoFactor в скоринге (см. §4.2). |
| 4 | Полный список efficiency-апгрейдов по 21 нации | Использовать `parser/simulate_upgrades.py` — он уже инлайнит SetUpgStruct и перебирает `case cid`. |
| 5 | ~~Подсчёт деревьев / стоунов / мин на 256×256 highlands+Rich~~ | **РЕШЕНО** (через generator.cfg → pattern_types.json + per-type stats): см. §8.4 + §8.5. **~27K деревьев / ~3K stone-cells** для foreststype=0. Per-pattern-type медианы есть в `output/derived/pattern_type_stats.json`. Wood pool **бесконечен** через пеньки. Mines = 1 deposit per pattern (mask=footprint, не объекты). |
| 6 | Mine **upgrades** (`<commonName>gol.X` etc.) — что меняют (производительность? capacity?) | Прочитать в country.script вокруг мин, типы апгрейдов. |
| 7 | Реальная стоимость "хода к складу" в миллисекундах | Зависит от §1 (скорость) + расстояние. Симулятор. |
| 8 | Учёт `ferry`/доставка из изолированных островов леса | Не критично для tiny+land, отложить. |
| 9 | `walkintervalfactor` — как влияет на анимацию ходьбы | Похоже скейлит animation speed относительно физической скорости. Проверить позже. |

---

**Что есть для уровня B (формулы):** §3-§7 содержат всё нужное. Стоп-фактор — точная скорость крестьянина (вопрос 1) для модели "удалённость склада → реальный rate". Без неё можно дать формулу с параметром `peasant_tiles_per_game_sec` и численные значения для нескольких предположений.

**Что нужно для уровня C (симулятор):** дополнительно §9 пп. 1-5.
