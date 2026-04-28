# Recon: Cossacks 3 — Building Mechanics

Глубокий разбор: footprint/форма, постройка крестьянами, починка, башни/гарнизон, разрушение/захват.

**Контекст:** game speed = fast (×1.4). Все длительности в game-seconds, real-seconds = g-sec / 1.4.

---

## 🚨 Critical bug discovery: building buildtime was 10× off (FIXED)

**Status:** ✅ Исправлено в этой сессии — `parser/build_data.py` теперь использует `_buildtime_to_sec()` для зданий (с ×10 модификатором). `cossacks3_reference.{md,xlsx}`, `tech_tree.*`, `production_rates.md`, `scaling_prices.md`, sim — всё перегенерировано.

В нашем `cossacks3_data.json` для **зданий** `buildtime_sec = buildtime_frames / 32`. **Было неверно** — нужно ещё умножить на `gc_buildtime_modifier = 10`.

**Источник:** [`misc.script:478-482`](C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/misc.script#L478):
```pascal
function _misc_BuildtimeToTime(const val : Integer) : Float;
begin
   Result := (val * gc_frames_to_time * gc_buildtime_modifier);
   //               ^=1/32           ^=10
end;
```

Когда `SetObjBuildingExtProperties(..., maxhp, buildtime=500, ...)` вызывается (например для bavcen), движок хранит `objbase.buildtime := 500 × 1/32 × 10 = 156.25 g-sec`. Не 15.625!

**Это касается ТОЛЬКО зданий** — для юнитов используется `_misc_FramesToTime(val) = val × 1/32` без ×10.

**Что неверно у нас сейчас:**
- `cossacks3_data.json` `building.buildtime_sec` — везде в 10× меньше
- `cossacks3_reference.{md,xlsx}` — все цифры buildtime для зданий в 10× меньше
- `simulate_economy.py` — постройка зданий в 10× быстрее реальной

**Правильные цифры с ×10:**
| Building | buildtime_frames | OLD sec (wrong) | **REAL sec** | REAL real-sec @ fast |
|---|---:|---:|---:|---:|
| bavhou | 100 | 3.12 | **31.25** | 22.3 |
| bavbla | 300 | 9.38 | **93.75** | 67.0 |
| bavbar | 300 | 9.38 | **93.75** | 67.0 |
| bavcen | 500 | 15.62 | **156.25** | 111.6 |
| bavart | 787 | 24.59 | **245.94** | 175.7 |
| eurmil | 300 | 9.38 | **93.75** | 67.0 |
| bavaca | 2000 | 62.5 | **625.00** | 446.4 |
| bavsta | 2000 | 62.5 | **625.00** | 446.4 |
| eurpor (shipyard) | 5000 | 156.25 | **1562.50** | 1116 (~19 min) |
| eurtow | 3937 | 123.03 | **1230.31** | 879 (~15 min) |
| bavba2 | 18000 | 562.5 | **5625.00** | 4017 (~67 min) |

⚠ Это с **1 builder**. Реально несколько крестьян ускоряют (см. §3).

**Что чинить:** в [`parser/build_data.py:362,417`](../parser/build_data.py#L362) добавить отдельную ветку для зданий с ×10. Перегенерировать всё.

---

## 1. Building footprint (форма и размер)

**Источник:** `data/objects/buildings/<sid>.prop` → `collisionmaskproperty.Mask`.

**Единица:** 1 mask cell = **0.5 тайла** ([`unit.script:8712`](C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/unit.script#L8712) `cellSize := 0.5`).

**Mask = 2D ASCII grid of 0/1**, где 1 = занятая клетка. Пример bavcen:
```
000110000000          12 cols × 11 rows = 6×5.5 тайлов
001111000000          ↓ заполненный диамант
011111100000
111111110000
011111111000
001111111110
000111111110
000011111100
000001111000
000000110000
000000000000
```
Занято ≈ 57 cells × 0.5² = 14.25 тайл². Визуально — диагональный квадрат.

**CustomBoundingAABB** (для отрисовки/clicking) — отдельный от collision mask, обычно меньше, в тайлах: для bavcen X=4.45, Z=2.70.

**ScaleFactor для mask:** 1 (из [`refbuilding.prop:45`](C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/objects/ref/refbuilding.prop#L45)) — mask cells не масштабируются. `DefaultScale=0.662` (визуальный) ≠ collision.

**Где хранится у нас:** пока нигде, нужно извлечь footprint mask из .prop файлов в JSON.

---

## 2. Repair (починка) — БЕСПЛАТНО

**Источник:** [`units/unit.inc/onaclanimationreachedconstruct.inc:40-41`](C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/units/unit.inc/onaclanimationreachedconstruct.inc#L40):
```pascal
if (arg_obj.orders[0].itype = gc_obj_order_type_repair) then
   TObj(pobj).hp := Min(TObj(pobj).hp + gc_gameplay_repairhp, TObjBase(pobjbase).maxhp);
```

**Constant:** `gc_gameplay_repairhp = 20` ([`dmscript.global:211`](C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/dmscript.global#L211)).

**Mechanic:**
- Каждый завершённый "construct" анимационный цикл крестьянина → +20 HP к зданию.
- **Никаких ресурсов не тратится.** Ремонт абсолютно бесплатен.
- Capped at maxhp.
- Несколько крестьян чинят параллельно (см. §3 builder slots).

**Construct animation:** 13 frames (186..198 в AAF). При допущении 32 fps = 0.406 g-sec на цикл.

**Расчёт скорости ремонта:**
- 1 крестьянин: 20 HP / 0.406 g-sec = **49.3 HP/g-sec**
- N крестьянин: 49.3 × N (до cap builder slots)
- Bavcen с HP=4000, починка с 0 до full: 4000 / 49.3 = **81 g-sec** одним крестьянином (~58 real-sec @ fast).
- С 12 builders (типичный лимит для центра): 81/12 = **6.75 g-sec** (~4.8 real-sec).

⚠ Применять reпейр только когда здание **уже построено** (bbuilt=True). До завершения постройки — другой механизм (см. §3).

---

## 3. Construction (постройка крестьянами)

### 3.1 Прогресс за один "удар молотком"

Из [onaclanimationreachedconstruct.inc:25-37](C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/units/unit.inc/onaclanimationreachedconstruct.inc#L25):
```pascal
delta := (gc_buildtime_progressperhit / TObjBase(pobjbase).buildtime)
buildprogress += delta
deltahp := round(maxhp * delta)
hp += deltahp   // capped at maxhp
```

Где `gc_buildtime_progressperhit = 10 × 1/32 × 1.15 = 0.359375`.

### 3.2 Время постройки vs число строителей — ВАЖНО

**Каждый крестьянин-строитель** независимо играет construct анимацию (13 frames @ 32 fps = 0.406 g-sec за цикл) и в конце цикла даёт +1 hit. С N строителями параллельно — N hits / 0.406 g-sec.

**Формула для N строителей:**
```
hits_total = buildtime_real_sec / 0.359375
T_with_N(g-sec) = hits_total / (N / 0.406) 
                = buildtime_real_sec × (0.406 / 0.359)/ N
                = buildtime_real_sec × 1.13 / N
```

**Practical rule:** `time = buildtime × 1.13 / N`. Удваиваешь крестьян → пополам время.

**Cap:** N ограничен числом builder slots (см. §3.3). Hard cap движка: 30.

**Пример bavba2 (Barracks 18 century, buildtime_real = 5625 g-sec)** — это объясняет «75 минут за 18-вечный барак»:

| N builders | g-sec | real-sec @ fast | минуты real |
|---:|---:|---:|---:|
| 1 | 6 356 | 4 540 | **76 min** ← вот эта страшная цифра |
| 2 | 3 178 | 2 270 | 38 min |
| 5 | 1 271 | 908 | 15 min |
| 10 | 636 | 454 | 7.6 min |
| 16 (slot cap для большого здания) | 397 | 284 | **4.7 min** ← реалистично |

**Никто не строит здание ОДНИМ крестьянином в реальной игре.** При размещении foundation сразу прибегают все idle крестьяне в окрестности, заполняя все builder slots.

Полная таблица "время с N крестьян" по всем зданиям всех наций — в [`output/strategy/construction_times.md`](../output/strategy/construction_times.md) (генератор: [`parser/compute_construction_times.py`](../parser/compute_construction_times.py)).

**Что в нашей JSON:** поле `building.buildtime_sec` = `frames × 10/32` — это **нормированный buildtime** из formula (`objbase.buildtime`). Время-с-1-builder ≈ `buildtime_sec × 1.13`. То есть **поле НЕ равно реальному времени постройки — оно всегда требует деления на N**.

Чтобы избежать путаницы: можно интерпретировать `buildtime_sec` как "секунд работы для 1 builder, для накопления полного прогресса" — в момент когда N builders, делите на N.

### 3.2 Builder slots (сколько крестьян могут одновременно строить)

**Cap:** `gc_MaxBuilderCount = 30` ([`dmscript.global:159`](C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/dmscript.global#L159)).
**Min spacing:** `gc_BuilderDist = 1.0` тайл ([`dmscript.global:160`](C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/dmscript.global#L160)).

**Builder points** — конкретные позиции вокруг здания, где крестьянин стоит и работает.

**Источник позиций:**
1. Для большинства зданий — **динамически вычисляются** из collision mask через [`_unit_CalcBuilderPoints`](C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/unit.script#L8700) (unit.script:8702-8870 примерно). Алгоритм: обходит периметр маски, ставит точку каждые `dist=1.0` тайл.
2. Для стен — из [`data/game/var/wallcustom.cfg`](C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/game/var/wallcustom.cfg) (BuilderPoints per wall variation, до 16).
3. (Опционально) Override per-building в [`data/game/var/objcustom.cfg`](C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/game/var/objcustom.cfg) — но в текущем файле я не вижу BuilderPoints, только ExitPoints/SmokePoints/Decal.

**Оценка точек для типового здания:**
- Перимfer mask cells × 0.5 / 1.0 = ~num_perimeter_cells × 0.5 builder slots
- bavcen (12×11 mask, диамант): periметр ≈ 22 cells (рёбра диаманта) × 0.5 / 1.0 = ~11 builder slots
- bavhou (тоже ~12×11, прямоугольник): ~12 builder slots
- Стена: 4 builder slots на сегмент (типично).

### 3.3 Алгоритм назначения крестьянина на стройку

[`_unit_OrderBuild` (unit.script:9285-9378)](C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/unit.script#L9285):
1. Получает builder slots для цели.
2. Для каждого слота проверяет: занят (на нём кто-то уже строит/ремонтирует)? Если да — пропуск.
3. Из свободных выбирает **ближайший по евклидову расстоянию** к крестьянину.
4. Назначает крестьянина на этот слот, отправляет туда командой move.
5. Крестьянин дойдя — начинает играть `construct` анимацию.
6. Каждый цикл анимации → +HP / +progress (см. §2/§3.1).

**Стоимость:** платится **upfront при постановке foundation** (когда вы дали команду построить и крестьянин подошёл). После этого ресурсы не тратятся.

---

## 4. Walls и Gates (строительство стен)

**Тип:** `gc_obj_usage_hardwall` / `gc_obj_usage_weakwall` (palisade, woodgate, stonegate, stonewall).

**Wall segment**: **2×2 тайла** на сегмент. Подтверждено по координатам в [`wallcustom.cfg`](C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/game/var/wallcustom.cfg) — все builder points в диапазоне [-1, +1] относительно центра сегмента.

**Builder slots per wall variation:**
| Variation | Геометрия | Slots |
|---:|---|---:|
| 1 | вертикальная стена | 4 (2 точки слева + 2 справа) |
| 2 | горизонтальная | 4 (2 сверху + 2 снизу) |
| 3 | угол / диагональ | 4 |
| 4 | угол / диагональ (зеркальная) | 4 |
| 5 | пересечение или ворота | **12** (12 точек по периметру 2×2) |
| 6+ | прочие | 4-8 |

Cap из движка: `gc_MaxWallBuilderPointsCount = 16` ([`dmscript.global:137`](C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/dmscript.global#L137)).

**Параметры стен** (после fix ×10):
| sid | maxhp | buildtime_g | Цена | costpercent |
|---|---:|---:|---|---:|
| eurswa (stone wall) | 50000 | **90 g-sec** | S50 | 0 (no scale) |
| eursga (stone gate) | 50000 | **90 g-sec** | S50 | 0 |
| ukrwwa (palisade) | varies | varies | W~50 | 0 |
| ukrwga (wood gate) | varies | varies | W~50 | 0 |

Время на 1 сегмент с 4 builders: 90 × 1.13 / 4 = **25.4 g-sec** ≈ 18 real-sec @ fast.

---

## 5. Garrison / Inside Units (объекты внутри зданий)

### 5.1 peasantabsorber — для шахт
Шахты `eurgol/euriro/eurcoa`: `peasantabsorber=5` (база), до 95 с апгрейдами. Рассмотрено в `recon/peasant_extraction.md` §5.

### 5.2 transport — для транспорта
Грузоподъёмность для транспортных юнитов:
- Ferry: `transport = 80+40 = 120` слотов ([`unit.script:2043`](C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/unit.script#L2043))
- Другие транспортные суда (`transport`)/корабли — TBD

### 5.3 Tower garrison
По коду [`unit.script:2224-2240`](C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/unit.script#L2224) башня НЕ имеет `peasantabsorber` или `transport`. Башня — статичное оборонительное здание со встроенным оружием (`weapon[0]`).

⚠ Вне-движковая фича "garrison units in tower" из других RTS отсутствует в Cossacks 3 для большинства зданий. Пехота гарнизон-ить нельзя.

### 5.4 Other inside-units checks
- `bcapture=True` отмечает, что объект **может быть захвачен** врагом (см. §7).
- `gc_obj_usage_tower` — особенный case: захватывается даже без bcapture ([`unit.script:178`](C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/unit.script#L178)).

---

## 6. Building destruction & decay

### 6.1 Decay (ветшание)
**Не найдено** в коде. Здания **не теряют HP** со временем сами по себе. HP меняется только от:
- Урон врагом
- Захват (?) — нужно проверить

### 6.2 Destruction (разрушение)
HP=0 → state-machine переход через `gc_statetag_essential_death`. У зданий есть `bavcen_death1a/death2a` меши (visualis) — ruins после смерти.

**Возможно ли отстроить?** — нужно проверить специально (предположительно: нет, только новое здание ставить).

### 6.3 Производство при низком HP
[`doprogressorders.inc`](C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/units/building.inc/doprogressorders.inc): нет проверки на HP. Здание производит юниты пока живо. **Неполное здание (bbuilt=False) — не производит.**

---

## 7. Capture (захват зданий)

**Trigger:** `objprop.bcapture = True` в коде или [`gc_obj_usage_tower`](C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/unit.script#L178).

**Mechanic:** [`miscext.script:1018-1030`](C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/miscext.script#L1018):
- Радиус: `gc_gameplay_captureradius = 214/53.33 = 4.0 тайла` ([`dmscript.global:208`](C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/dmscript.global#L208)).
- Block radius: `gc_gameplay_captureblockshotradius = 3.0 тайла`.
- Если вражеская пехота находится в радиусе захвата здания и игрока-владельца **нет** в этом радиусе → здание переходит к врагу.

**Какие здания захватываются:** все шахты, центры, ratusha, и многие другие. Список — где `bcapture=True` в коде. У стен/ворот **нет** bcapture.

При захвате:
- HP сохраняется
- Player ownership → новый
- Score "захватчику" с множителем 5 ([`unit.script:3837-3841`](C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/unit.script#L3837))

⚠ Тонкости: при захвате `counter.all` инкрементируется, но `counter.built` нет. Это влияет на масштабирование цен (если захватили центр, следующий ваш центр будет ×3 как обычно — но захваченный учитывается в счётчике).

---

## Закрытые вопросы (этой сессии)

| # | Вопрос | Ответ |
|---:|---|---|
| 1 | Длина стены и slots/segment | **2×2 тайла на сегмент**, 4-12 builder slots в зависимости от variation (см. §4) |
| 2 | objcustom.cfg BuilderPoints override | В файле есть только `ExitPoints/SmokePoints/Decal` для зданий — **ВСЕ здания** используют динамический `_unit_CalcBuilderPoints` (обход периметра mask). Только wall имеет explicit BuilderPoints в `wallcustom.cfg`. |
| 3 | Decay (ветшание) | **Нет** — здания не теряют HP сами по себе. Только от damage. Нет gc_decay константы или _hp_decay вызовов в скриптах. |
| 4 | После HP=0 — можно ли восстановить | **Нет.** [`OnDeath`](C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/units/building.inc/ondeath.inc) вызывает `_unit_DestroyObj(myHnd)` — здание удаляется. Меш `<sid>_death1a/2a` — визуальные ruins, но не игровой объект. Нужно ставить новое foundation. |
| 5 | Capture radius — у всех одинаковый? | Из кода ([`miscext.script:1018+`](C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/miscext.script#L1018)) используется единая константа `gc_gameplay_captureradius = 4.0 тайла`. Per-building override не найден. |
| 6 | Cancel construction — refund? | **Юнит cancel:** [`_unit_CancelUnitProduction` (unit.script:5891)](C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/unit.script#L5891) — full refund для очереди (с учётом costpercent). **Foundation cancel (Del):** add to `deluids` list — peasant adviser не auto-restore. **Refund foundation cost — НЕ найдено** в коде. Похоже не возвращается. |
| 7 | Construct animation FPS | 13 frames per cycle in AAF. Допущение 32 fps (= `gc_time_to_frames`). Без empirical теста не подтверждено — **открытый вопрос**, см. `recon/empirical_tests.md`. |

## Остающиеся открытые вопросы

| # | Вопрос | Как решить |
|---:|---|---|
| 1 | FPS construct анимации (32 или другое?) | Empirical test: засечь время одного "удара молотка" по строящемуся зданию |
| 2 | Стартовая позиция peasants/cen/sto при game start | Прочитать `CreateStartPointPeasants` в dogenerate.inc (для editor v1) |
| 3 | Точная стоимость каждого варианта стены (eurswa cost=50 stone — это за сегмент?) | Empirical: в редакторе, поставить 1 сегмент стены, посмотреть списанные ресурсы |

---

## Что записать в reference (после фикса bug'а ×10)

После исправления `parser/build_data.py`:
1. Перегенерировать `cossacks3_data.json` — все building.buildtime_sec ×10.
2. Перегенерировать `cossacks3_reference.{md,xlsx}` и `reference/`.
3. Перегенерировать `cossacks3_scaling_prices.md` (если он использует buildtime — кажется не использует).
4. Перегенерировать `output/strategy/production_rates.md` — таблицы units/min зависят от unit_buildtime, не building. Не трогать.
5. Перезапустить `simulate_economy.py` тесты — там сейчас здания строятся в 10× быстрее реальной.
6. Footprint и builder slots — извлечь из .prop файлов в новый dataset (опц.).

Обновить **production_rates** строки про "сколько секунд строится здание" если такие есть.
