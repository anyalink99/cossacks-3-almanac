# Recon: Cossacks 3 — Building Mechanics

Глубокий разбор: footprint, постройка/починка крестьянами, стены, гарнизон/башни, захват, разрушение.

**Контекст:** game speed = fast (×1.4). Все длительности в game-seconds, real-seconds = g-sec / 1.4.

> **Buildtime в game-time.** Для зданий движок хранит `objbase.buildtime = frames × (1/32) × gc_buildtime_modifier`, где `gc_buildtime_modifier = 10` ([`misc.script:478-482`](C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/misc.script#L478)). Для юнитов модификатор = 1. Это объясняет, почему «реальное» время постройки здания ≈ frames × 10/32, а не frames/32. В нашем `docs/data.json` поле `building.buildtime_sec` уже учитывает ×10.

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

Полная таблица «время с N крестьян» по всем зданиям всех наций — в [`docs/reports/economy/construction_times.md`](../docs/reports/economy/construction_times.md) (генератор: [`compute/compute_construction_times.py`](../compute/compute_construction_times.py)).

**Что в нашей JSON:** поле `building.buildtime_sec` = `frames × 10/32` — это **нормированный buildtime** из formula (`objbase.buildtime`). Время-с-1-builder ≈ `buildtime_sec × 1.13`. То есть **поле НЕ равно реальному времени постройки — оно всегда требует деления на N**.

Чтобы избежать путаницы: можно интерпретировать `buildtime_sec` как "секунд работы для 1 builder, для накопления полного прогресса" — в момент когда N builders, делите на N.

### 3.2 Builder slots (сколько крестьян могут одновременно строить)

**Cap:** `gc_MaxBuilderCount = 30` ([`dmscript.global:159`](C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/dmscript.global#L159)).
**Min spacing:** `gc_BuilderDist = 1.0` тайл ([`dmscript.global:160`](C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/dmscript.global#L160)).

**Builder points** — конкретные позиции вокруг здания, где крестьянин стоит и работает.

**Источник позиций:**
1. Для большинства зданий — **динамически вычисляются** из collision mask через [`_unit_CalcBuilderPoints`](C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/unit.script#L8702) (unit.script:8702-9006). Алгоритм: обходит периметр маски с шагом 0.5 тайла (1 cell), ставит точку каждые `dist=1.0` тайл, после цикла добавляет ещё одну если `dLen > dist/2`.
2. Для стен — из [`data/game/var/wallcustom.cfg`](C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/game/var/wallcustom.cfg) (BuilderPoints per wall variation, до 16).
3. (Опционально) Override per-building в [`data/game/var/objcustom.cfg`](C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/game/var/objcustom.cfg) — в текущем файле там только ExitPoints/SmokePoints/Decal, BuilderPoints нет.

**Точные значения для каждого здания:** [`docs/reports/economy/builder_slots.md`](../docs/reports/economy/builder_slots.md) и [`docs/derived/builder_slots.json`](../docs/derived/builder_slots.json) — генерируются [`compute/compute_builder_slots.py`](../compute/compute_builder_slots.py).

**Геометрический инсайт.** Для любой выпуклой формы (диск, ромб, скруглённый прямоугольник, диагональный slab — то есть для подавляющего большинства зданий) Manhattan-периметр = `bbox_cols + bbox_rows`. Walker и `bbox_cols+bbox_rows` дают одинаковый результат для convex.

**Non-convex здания** — есть, но мало (5 из ~350): `scocen` (две «ноги» сверху, walker=28 vs bbox 24), `swecen` (арка с двумя ногами внизу, walker=27 vs bbox 24), `portem` (выступ справа-внизу, +2), `bavhou` (две ножки, +1), `ukrtem` (крестообразный, +1). Walker корректно обходит внутренние вмятины и считает дополнительные слоты — **подтверждено эмпирически на swecen=27** (engine действительно ставит крестьян внутри арки).

**Полная таблица эмпирических точек** (9 из 10 матчат предсказание):
- Convex: polcen=18, ruscen=24, eurmil=10, rusmil=7, polbla=18, polba2=25 ✓
- Non-convex: swecen=27 ✓
- Sparse storehouses: tursto=8 (walker по большой компоненте), spasto=7 (walker по большой, орфан игнорируется), russto=8 (bbox_union для линейных опор) ✓
- Известное расхождение: eursto предсказание 9, эмпирика 8 (off by 1, причина не выявлена).

**Сильная зависимость от нации.** Размер маски (а значит и периметр) у одной и той же категории здания может различаться кратно. Пример для 18c казармы (`*ba2`):

| nation | mask | cells | perim (тайлов) | slots |
|---|---|---:|---:|---:|
| ven | 12×9 | 58 | 19 | **19** |
| sax | 12×9 | 59 | 20 | **20** |
| net | 12×10 | 69 | 21 | **21** |
| swi/pie/pru/den | 12×12 | 63-91 | 22 | **22** |
| bav/eng | 12×11 | 65-73 | 23 | **23** |
| por | 12×14 | 86 | 24 | **24** |
| pol | 14×14 | 87 | 25 | **25** |
| spa/hun | 14×13 | 101-103 | 26 | **26** |
| swe | 14×13 | 108 | 27 | **27** |
| aus/fra | 16×15-17 | 112-129 | 29 | **29** |
| sco/rus | 16×15-18 | 123-133 | 30+ | **30** (cap'd) |

**Engine quirk — sparse-маски складов.** У 4 складов (`russto`, `eursto`, `spasto`, `tursto`) маска не выпуклая. У `tursto` всё ещё одна большая компонента — walker даёт 8 = факт. У `spasto` — большая клякса + 1 мелкий орфан в углу; walker правильно ходит большую часть и игнорирует орфан → 7 = факт (с пустой левой стороной у строящего здания, что видно в игре). У `russto` и `eursto` маска вырождается до **двух линейных «опорных» планок** (1×2 и 1×3) с пустотой между ними — walker по одной планке даёт 3-4 слота, но в игре крестьяне обходят bbox целиком: 8 vs предсказанный walker'ом результат. Эмпирически: правило «если все компоненты линейные → используй `bbox_cols + bbox_rows` объединения» воспроизводит russto точно (8=8) и eursto с известным расхождением −1 (предсказание 9, факт 8). Реализовано как fallback `method=bbox_union` в [`compute_builder_slots.py`](../compute/compute_builder_slots.py).

**Ворота не строятся крестьянами.** `*sga`, `*wga`, `*sga_14..17` и т.д. в обычной игре создаются конвертацией существующего участка стены: игрок выделяет стену → клик «превратить в ворота». Слоты для них в отчёте указаны для полноты, но непосредственно не используются.

**Сим vs in-game ±1.** Помимо описанного ±1 для eursto, симуляция предсказывает 23 для bavba2, а пользователь наблюдал 22 (это исторический замер, не перепроверенный на новой формуле — пока трактуем как pathing failure для одной точки или edge of map).

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

### 5.3 Tower — built-in cannon

Башня НЕ имеет garrison (peasantabsorber=0, transport=0). Это статичная пушка-здание со встроенным оружием ([`unit.script:2223-2240`](C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/unit.script#L2223)):

| параметр | значение |
|---|---|
| weapon[0].kind | `gc_obj_weapon_kind_cannonball` |
| weapon[0].damage | 400 |
| weapon[0].radiusmin/max (px) | 400 / 1500 |
| weapon[0].radiusmax (tiles) | ≈ 28.1 |
| weapon[0].pause | 1000 frames = 31.25 g-sec |
| weapon[0].cost / shot | iron=10, coal=30 |
| weapon[0].dispertion | 100 px |
| searchradius | 1400 px ≈ 26.25 tiles |
| consume.gold | **500/tick = 0.8 gold/g-sec** ([`unit.script:2235`](.)) |
| HP | 20000 |
| `bturnoff=True` | можно отключить — снижает gold-drain |

**Apgrades:** `gc_ach_upgrade_towerattspeed` (achievement-related, attack speed). RUS вариант: dmg 300 (вместо 400), shield=5, dispertion 125.

⚠ Гарнизон-ить пехоту в башню **нельзя** — это другие RTS. В C3 башня сама стреляет.

**Парсер gap:** weapons для зданий пока не извлекаются в `data.json`. См. [`reference_session_findings_2026-04-29.md`](../memory/...) — есть TODO.

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
- **Захват instant** (verified empirically 2026-04-29). Старая оценка про «5%/tick → ~25-30% за 5-7 sec» была неверной — относилась к другой механике или была неаккуратной интерпретацией. Реально: один тик с условием `enemy_in_radius && owner_not_in_radius` → ownership flip.

**Какие здания захватываются:** все шахты, центры, ratusha, и многие другие. Список — где `bcapture=True` в коде. У стен/ворот **нет** bcapture.

При захвате:
- HP сохраняется
- Player ownership → новый
- Score "захватчику" с множителем 5 ([`unit.script:3837-3841`](C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/unit.script#L3837))

⚠ Тонкости: при захвате `counter.all` инкрементируется, но `counter.built` нет. Это влияет на масштабирование цен (если захватили центр, следующий ваш центр будет ×3 как обычно — но захваченный учитывается в счётчике).

---

## 8. Резюме механик (быстрый ответ на частые вопросы)

| Вопрос | Ответ |
|---|---|
| Длина одного сегмента стены | 2×2 тайла, 4-12 builder slots в зависимости от variation (§4) |
| objcustom.cfg BuilderPoints override? | В файле только `ExitPoints/SmokePoints/Decal` — **все здания** считаются через динамический `_unit_CalcBuilderPoints` (обход периметра mask). Стены — единственное исключение, у них explicit BuilderPoints в `wallcustom.cfg`. |
| Ветшание (decay) | **Нет.** Здания теряют HP только от damage. Ни константы `gc_decay`, ни вызовов `_hp_decay` в скриптах не существует. |
| Можно ли восстановить здание после HP=0 | **Нет.** [`OnDeath`](C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/units/building.inc/ondeath.inc) вызывает `_unit_DestroyObj` — здание удаляется. Мэш `<sid>_death1a/2a` — визуальные руины, не игровой объект. Только новое foundation. |
| Capture radius универсальный? | Да. `gc_gameplay_captureradius = 4.0 тайла` ([`miscext.script:1018`](C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/miscext.script#L1018)). Per-building override не найден. |
| Refund при отмене постройки | **Юнит-очередь:** [`_unit_CancelUnitProduction`](C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/unit.script#L5891) даёт full refund. **Foundation (Del):** добавляется в `deluids`, refund foundation cost в коде не найден — скорее всего **не возвращается**. |

## 9. Открытые вопросы

| # | Вопрос | Как решить |
|---:|---|---|
| 1 | FPS construct-анимации (= 32 или другой?) | Empirical: засечь время одного цикла молотка на строящемся здании |
| 2 | Точная стоимость одного сегмента стены (50 stone — за сегмент или за весь чертёж?) | Empirical: в редакторе поставить 1 сегмент, посмотреть списанные ресурсы |
