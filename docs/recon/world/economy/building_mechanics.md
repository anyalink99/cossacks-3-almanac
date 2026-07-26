# Recon: механика зданий

Глубокий разбор: footprint, постройка и ремонт крестьянами, стены, гарнизон
башен, захват, разрушение. Все ссылки на код и Pascal-блоки собраны в разделе
[Источники](#источники) в конце документа. Все пути там относительно `data/` в
установке Cossacks 3.

> **Технические детали анимации `construct` и frame-точные тайминги** —
> в [`internals/engine/animation_system.md`](../../../../internals/engine/animation_system.md).

## TL;DR

- **Buildtime** для зданий хранится с дополнительным множителем
  `gc_buildtime_modifier = 10` [^1]. У юнитов множитель = 1. Реальное время
  постройки = `frames × 10 / 32`, а не `frames / 32`. В `docs/data.json` поле
  `building.buildtime_sec` уже учитывает ×10.
- **Footprint = collision mask** в файле `<sid>.prop`. Размер ячейки —
  0.5 тайла (`gc_collision_size = 0.5`).
- **Ремонт бесплатен**, +20 HP за один удар крестьянина (`gc_gameplay_repairhp`).
- **Постройка**: `delta = 0.359 / buildtime` за удар. Анимация
  `construct` = 13 кадров = 0.406 g-сек.
- **Builder slots** = `bbox_cols + bbox_rows` (Manhattan-периметр) для
  выпуклых форм. Жёсткий лимит движка — 30. Стены — 4 слота на сегмент.
- **Captureradius** = 4 тайла (см. [capture_mechanics.md](capture_mechanics.md)).

---

## 1. Building footprint (форма и размер)

**Источник:** `collisionmaskproperty.Mask` в `.prop`-файле здания [^2].

**Единица:** 1 mask cell = **0.5 тайла** (`cellSize := 0.5` [^3]).

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

**ScaleFactor для mask:** 1 [^4] — mask cells не масштабируются. `DefaultScale=0.662` (визуальный) ≠ collision.

**Где хранится у нас:** пока нигде, нужно извлечь footprint mask из .prop файлов в JSON.

---

## 2. Repair (починка) — БЕСПЛАТНО

**Источник:** обработчик окончания construct-анимации проверяет тип ордера и
прибавляет фиксированное количество HP, ограниченное `maxhp` [^5].

**Constant:** `gc_gameplay_repairhp = 20` [^6].

**Mechanic:**

- Каждый завершённый «construct» анимационный цикл крестьянина → +20 HP к зданию.
- **Никаких ресурсов не тратится.** Ремонт абсолютно бесплатен.
- Capped at maxhp.
- Несколько крестьян чинят параллельно (см. §3 builder slots).

**Construct animation:** 13 frames (186..198 в AAF). При допущении 32 fps = 0.406 g-sec на цикл.

**Расчёт скорости ремонта:**

- 1 крестьянин: 20 HP / 0.406 g-sec = **49.3 HP/g-sec**
- N крестьянин: 49.3 × N (до cap builder slots)
- Bavcen с HP=4000, починка с 0 до full: 4000 / 49.3 = **81 g-sec** одним крестьянином (~58).
- С 12 builders (типичный лимит для центра): 81/12 = **6.75 g-sec**.

⚠ Ремонт работает только когда здание **уже достроено** (`bbuilt = True`). До завершения постройки действует другой механизм (см. §3).

---

## 3. Construction (постройка крестьянами)

### 3.1 Прогресс за один «удар молотком»

Расчёт `delta`, `buildprogress` и прибавки HP — на каждом завершении
construct-анимации [^7]:

- `delta := gc_buildtime_progressperhit / buildtime`
- `buildprogress += delta`
- `hp += round(maxhp × delta)` (capped at `maxhp`)

Где `gc_buildtime_progressperhit = 10 × 1/32 × 1.15 = 0.359375`.

### 3.2 Время постройки vs число строителей — ВАЖНО

**Каждый крестьянин-строитель** независимо играет construct анимацию (13 frames @ 32 fps = 0.406 g-sec за цикл) и в конце цикла даёт +1 hit. С N строителями параллельно — N hits / 0.406 g-sec.

**Формула для N строителей:**

```
hits_total = buildtime_g_sec / 0.359375
T_with_N(g-sec) = hits_total / (N / 0.406)
                = buildtime_g_sec × (0.406 / 0.359)/ N
                = buildtime_g_sec × 1.13 / N
```

**Practical rule:** `time = buildtime × 1.13 / N`. Удваиваешь крестьян → пополам время.

**Cap:** N ограничен числом builder slots (см. §3.3). Hard cap движка: 30.

**Пример bavba2 (Barracks 18 century, `buildtime = 5625 g-сек`)**:

| N builders | g-сек | мин g-sec |
|---:|---:|---:|
| 1 | 6 356 | 105.9 |
| 2 | 3 178 | 53.0 |
| 5 | 1 271 | 21.2 |
| 10 | 636 | 10.6 |
| 16 (slot cap для большого здания) | 397 | 284 | **4.7 min** ← реалистично |

**Никто не строит здание ОДНИМ крестьянином в реальной игре.** При размещении foundation сразу прибегают все idle крестьяне в окрестности, заполняя все builder slots.

Полная таблица «время с N крестьян» по всем зданиям всех наций — в [`docs/reports/economy/construction_times.md`](../../../reports/economy/construction_times.md) (генератор: [`compute/compute_construction_times.py`](../../../../compute/compute_construction_times.py)).

**Что в нашей JSON:** поле `building.buildtime_sec` = `frames × 10/32` — это **нормированный buildtime** из formula (`objbase.buildtime`). Время-с-1-builder ≈ `buildtime_sec × 1.13`. То есть **поле НЕ равно реальному времени постройки — оно всегда требует деления на N**.

Чтобы избежать путаницы: можно интерпретировать `buildtime_sec` как «секунд работы для 1 builder, для накопления полного прогресса» — в момент когда N builders, делите на N.

### 3.3 Builder slots (сколько крестьян могут одновременно строить)

**Cap:** `gc_MaxBuilderCount = 30` [^8].
**Min spacing:** `gc_BuilderDist = 1.0` тайл [^9].

**Builder points** — конкретные позиции вокруг здания, где крестьянин стоит и работает.

**Источник позиций:**

1. Для большинства зданий — **динамически вычисляются** из collision mask через `_unit_CalcBuilderPoints` [^10]. Алгоритм: обходит периметр маски с шагом 0.5 тайла (1 cell), ставит точку каждые `dist=1.0` тайл, после цикла добавляет ещё одну если `dLen > dist/2`.
2. Для стен — из `data/game/var/wallcustom.cfg` (BuilderPoints per wall variation, до 16).
3. (Опционально) Override per-building в `data/game/var/objcustom.cfg` — в текущем файле там только ExitPoints/SmokePoints/Decal, BuilderPoints нет.

**Точные значения для каждого здания:** [`docs/reports/economy/builder_slots.md`](../../../reports/economy/builder_slots.md) и [`derived/builder_slots.json`](../../../../derived/builder_slots.json) — генерируются [`compute/compute_builder_slots.py`](../../../../compute/compute_builder_slots.py).

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

**Engine quirk — sparse-маски складов.** У 4 складов (`russto`, `eursto`, `spasto`, `tursto`) маска не выпуклая. У `tursto` всё ещё одна большая компонента — walker даёт 8 = факт. У `spasto` — большая клякса + 1 мелкий орфан в углу; walker правильно ходит большую часть и игнорирует орфан → 7 = факт (с пустой левой стороной у строящего здания, что видно в игре). У `russto` и `eursto` маска вырождается до **двух линейных «опорных» планок** (1×2 и 1×3) с пустотой между ними — walker по одной планке даёт 3-4 слота, но в игре крестьяне обходят bbox целиком: 8 vs предсказанный walker'ом результат. Эмпирически: правило «если все компоненты линейные → используй `bbox_cols + bbox_rows` объединения» воспроизводит russto точно (8=8) и eursto с известным расхождением −1 (предсказание 9, факт 8). Реализовано как fallback `method=bbox_union` в [`compute_builder_slots.py`](../../../../compute/compute_builder_slots.py).

**Ворота — это моментальный индивидуальный апгрейд на существующем сегменте стены** (`gc_upg_type_single_buildgate`), а не отдельное здание, которое строят крестьяне. Игрок выделяет достроенный участок прямой стены минимум из трёх одинаковых сегментов и нажимает «построить ворота». На месте центрального сегмента создаётся новый объект ворот (`*sga` / `*wga`) с `individual.upglevel = 1`; ближайший вызов `_unit_ControlBuildProgress` через специальную ветку `if (bwall) and (upglevel>0) then hp := maxhp` сразу выставляет полное HP, после чего OnTagStates переводит объект в `bbuilt = True`. Никакая стройка крестьянами не происходит. Подробнее — в [`../combat/walls_and_gates.md`](../combat/walls_and_gates.md).

**Сим vs in-game ±1.** Помимо описанного ±1 для eursto, симуляция предсказывает 23 для bavba2, а пользователь наблюдал 22 (это исторический замер, не перепроверенный на новой формуле — пока трактуем как pathing failure для одной точки или edge of map).

### 3.4 Алгоритм назначения крестьянина на стройку

`_unit_OrderBuild` [^11]:

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

**Wall segment**: **2×2 тайла** на сегмент. Подтверждено по координатам в `wallcustom.cfg` — все builder points в диапазоне [-1, +1] относительно центра сегмента.

**Builder slots per wall variation:**

| Variation | Геометрия | Slots |
|---:|---|---:|
| 1 | вертикальная стена | 4 (2 точки слева + 2 справа) |
| 2 | горизонтальная | 4 (2 сверху + 2 снизу) |
| 3 | угол / диагональ | 4 |
| 4 | угол / диагональ (зеркальная) | 4 |
| 5 | пересечение или ворота | **12** (12 точек по периметру 2×2) |
| 6+ | прочие | 4-8 |

Cap из движка: `gc_MaxWallBuilderPointsCount = 16` [^12].

**Параметры стен** (`buildtime_g_sec = frames × 10/32`, см. конвенцию зданий):

| sid | maxhp | frames | buildtime g-sec | Цена | consume.stone |
|---|---:|---:|---:|---|---:|
| eurswa (eur-кластер, каменная стена) | 50000 | 288 | **90** | 50 stone | 250 |
| eursga (eur-кластер, каменные ворота) | 32000 | 288 | **90** | 50 stone | 250 |
| russwa (RUS, каменная стена) | 50000 | 640 | **200** | 60 stone | 200 |
| russga (RUS, каменные ворота) | 32000 | 640 | **200** | 60 stone | 200 |
| turswa (TUR/ALG, каменная стена) | 50000 | 384 | **120** | 60 stone | 150 |
| tursga (TUR/ALG, каменные ворота) | 32000 | 384 | **120** | 60 stone | 150 |
| ukrwwa (общий, частокол) | 1500 | 18 | **5.6** | 10 wood | 32 |
| ukrwwa (UKR, частокол) | 2500 | 26 | **8.1** | 12 wood | 40 |
| ukrwga (общий, дерев. ворота) | 1000 | 18 | **5.6** | 10 wood | 32 |
| ukrwga (UKR, дерев. ворота) | 1500 | 26 | **8.1** | 12 wood | 40 |

`costpercent = 0` — все сегменты по одной цене, без scaling. У стен есть `consume.stone` или `consume.wood` — постоянное потребление пока сегмент стоит (см. артиллерия в [`../combat/artillery_specifics.md`](../combat/artillery_specifics.md) о механике consume).

Время постройки одного сегмента с N builders: `bt × 1.13 / N` по обычной формуле зданий — но для стен N лимитирован `gCustomBuildPointsWall[wallvariation].builderCount` (см. §4 ниже).

---

## 5. Garrison / Inside Units (объекты внутри зданий)

### 5.1 peasantabsorber — для шахт

Шахты `eurgol/euriro/eurcoa`: `peasantabsorber=5` (база), до 95 с апгрейдами. Рассмотрено в `recon/world/economy/peasant_extraction.md` §5.

### 5.2 transport — для транспорта

Грузоподъёмность для транспортных юнитов:

- Ferry: `transport = 80+40 = 120` слотов [^13].
- Другие транспортные суда (`transport`)/корабли — TBD

### 5.3 Tower — built-in cannon

Башня НЕ имеет garrison (peasantabsorber=0, transport=0). Это статичная пушка-здание со встроенным оружием. Базовые параметры (европейский вариант [^14], сигнатура `SetObjBaseWeapon(... index, damage, pause, radiusmin, radiusmax, detectradiusmin, detectradiusmax, kind, bSearchMin)` [^15]):

| параметр | значение |
|---|---|
| weapon[0].kind | `gc_obj_weapon_kind_cannonball` |
| weapon[0].damage | 1000 |
| weapon[0].pause | 400 frames = 12.5 g-сек |
| weapon[0].radiusmin / radiusmax (px) | 550 / 1500 |
| weapon[0].radiusmax (tiles) | ≈ 28.1 |
| weapon[0].detectradiusmin / detectradiusmax (px) | 550 / 50000 |
| weapon[0].cost / shot | iron=10, coal=30 |
| weapon[0].dispertion | 100 px |
| searchradius | 1400 px ≈ 26.25 tiles |
| consume.gold | **500/tick = 0.8 gold/g-сек** [^16] |
| HP | 20000 |
| buildtime | 3937 frames ≈ 123 g-сек |
| costpercent | 120 |
| `bturnoff=True` | можно отключить — снижает gold-drain |

**Russian вариант** [^17]: HP=21000, buildtime=4725, costpercent=125, shield=5, dispertion=125 px. Перезаписывается только `pause` (300 frames = 9.375 g-сек); `damage`, `radiusmin/max`, `kind` остаются как у EUR (передан литерал `default = -1`, который `SetObjBaseWeapon` пропускает по условиям `if (damage<>-1)` [^18]).

**Turkish вариант** [^19]: HP=22500, buildtime=3150, costpercent=125, цена 150 stone/90 wood/100 gold. weapon: damage=1200, pause=500 frames = 15.625 g-сек, radiusmax=1600 px, searchradius=1500 px, weapon.cost — coal=40, iron=15.

**Апгрейды:** `gc_ach_upgrade_towerattspeed` (achievement-related, attack speed).

⚠ Гарнизон-ить пехоту в башню **нельзя** — это другие RTS. В C3 башня сама стреляет.

**Парсер gap:** weapons для зданий пока не извлекаются в `data.json` целиком — есть только скалярные поля (`weapon_damage`, `weapon_pause_frames`, `weapon_radiusmax`, `weapon_kind`, `weapon_cost`); если у здания два оружия, попадает только первое. Подробнее — [`docs/known_issues.md`](../../../known_issues.md).

### 5.4 Other inside-units checks

- `bcapture=True` отмечает, что объект **может быть захвачен** врагом (см. §7).
- `gc_obj_usage_tower` — особенный case: захватывается даже без bcapture [^20].

---

## 6. Building destruction & decay

### 6.1 Decay (ветшание)

**Не найдено** в коде. Здания **не теряют HP** со временем сами по себе. HP меняется только от:

- Урон врагом
- Захват (?) — нужно проверить

### 6.2 Destruction (разрушение)

HP=0 → state-machine переход через `gc_statetag_essential_death`. У зданий есть `bavcen_death1a/death2a` меши (visualis) — ruins после смерти.

**Возможно ли отстроить?** — нужно проверить специально (предположительно: нет, только новое здание ставить).

#### Timeline разрушения

При `hp ≤ 0` или `bDie := True` здание получает `essential_death`. State-машина [^27] ставит первый таймер `DelayExecuteState`:

- если здание было `essential_birth` (отмена недостроенного) — сразу `DeathStage2` через `gc_building_deathtime_1 = 30` g-сек;
- иначе — `DeathStage1` через `gc_building_deathtime_0 = 30` g-сек, затем `DeathStage1` [^28] меняет mesh на `<sid>_death1` и ставит `DeathStage2` ещё через 30 g-сек. Для `usage = mine` обе паузы удваиваются (60 g-сек каждая).

**Корпус** в этом промежутке остаётся на карте: визуально — mesh `<sid>_death1.mesh`, в состоянии `essential_death`, материал `'debris'` [^29], коллизия — прежняя. Постройка нового здания на этих клетках невозможна, пока корпус не исчезнет.

**Сброс клетки.** В `DeathStage2` [^30] для не-стен с `gc_collisiontag_terrain` вызывается `_unit_SetTerrainCollision(myHnd, gc_collisiontag_none)` + `_misc_UnitTopologyUpdate`, затем `GameObjectRequestToDestroyByHandle`. После этого клетка освобождается, и на ней можно ставить новое здание.

**Гарнизон внутри** (если у здания `peasantabsorber > 0` или `transport > 0`). `_unit_DestroyObj` [^31] собирает `gc_argunit_inside` и вызывает `_unit_DoUnitsGoOutside(list, bDead=True, ...)`. Эта процедура [^32] ставит каждому юниту в списке `essential_death`, то есть содержимое умирает вместе со зданием.

#### OnDeath: возврат ресурсов из очереди

Перед самым удалением `OnDeath`-хук [^33] прокручивает очередь заказов здания:

- `produce`-заказы прогоняются через `_unit_ProduceUnit(... bState=False, ...)` [^34] — внутри ведёт к `_unit_CancelUnitProduction` и возврату ресурсов.
- `performupgrade`-заказы — через `_unit_CancelUpgradePerform`, возврат базовой стоимости апгрейда.

То есть при сносе работающей казармы или академии ресурсы за уже оплаченные юниты и апгрейды **возвращаются** игроку, а не сгорают.

#### Score-штраф

При разрушении владельцу: `−2 × building.score` (или `−5×`, если здание ранее уже было захвачено — см. [`../systems/victory_conditions.md`](../../systems/victory_conditions.md)).

### 6.3 Refund при отмене заказов

| Действие | Возврат | Источник |
|---|---|---|
| Отмена недостроенного здания (Foundation, кнопка GUI) | **100 %** потраченных ресурсов | GUI-handler `_misc_GUICancelBuilding` [^25] вызывает `GameObjectDestroyByHandle`; зеркального `_res_AddResToPlayerByIndex` для foundation cost в скриптах нет — refund 100 %, видимо, обрабатывается на стороне C++ (поведение в игре подтверждено). |
| Отмена заказа юнита в очереди | **100 %** от того, что было списано в момент заказа | `_unit_CancelUnitProduction` [^24] возвращает `price[k] × costmodifier`, где `costmodifier = pow(costpercent/100, restype)` и `restype` — счётчик built-копий, сохранённый в `OrderInfo` в момент заказа. Тек. цена не учитывается. |
| Отмена апгрейда | **100 %** базовой стоимости | `_unit_CancelUpgradePerform` [^35] возвращает базу из `_country_GetUpgradeCostBySID`. Costpercent-масштабирования у апгрейдов нет. |
| Захват | Все отменяемые заказы прерываются и ресурсы возвращаются **прежнему** владельцу. | См. `_misc_ChangePlayer` ветку очистки в [`capture_mechanics.md`](capture_mechanics.md). |

### 6.4 Производство при низком HP

`doprogressorders.inc`: нет проверки на HP. Здание производит юниты пока живо. **Неполное здание (bbuilt=False) — не производит.**

---

## 7. Capture (захват зданий)

**Trigger:** `objprop.bcapture = True` в коде или `gc_obj_usage_tower`.

**Mechanic** [^21]:

- Радиус: `gc_gameplay_captureradius = 214/53.33 = 4.0 тайла` [^22].
- Block radius: `gc_gameplay_captureblockshotradius = 3.0 тайла`.
- Если вражеская пехота находится в радиусе захвата здания и игрока-владельца **нет** в этом радиусе → здание переходит к врагу.
- **Захват instant** (verified empirically 2026-04-29). Старая оценка про «5%/tick → ~25-30% за 5-7 sec» была неверной — относилась к другой механике или была неаккуратной интерпретацией. Реально: один тик с условием `enemy_in_radius && owner_not_in_radius` → ownership flip.

**Какие здания захватываются:** все шахты, центры, ratusha, и многие другие. Список — где `bcapture=True` в коде.

**Стены и ворота — отдельная ветка.** У сегментов `bcapture = False`, но в `_misc_CheckCapture` для всех `bwall` принудительно ставится `bDie := True` — пехотинец врага в радиусе 4 тайла без защитников **уничтожает** сегмент, не передавая владельцу. При HP < 1/3 от max ветка вообще пропускается (стену уже доедают оружием). Подробности — [`../combat/walls_and_gates.md` §4](../combat/walls_and_gates.md).

При захвате:

- HP сохраняется
- Player ownership → новый
- Score «захватчику» с множителем 5 [^23]

⚠ Тонкости: при захвате `counter.all` инкрементируется, но `counter.built` нет. Это влияет на масштабирование цен (если захватили центр, следующий ваш центр будет ×3 как обычно — но захваченный учитывается в счётчике).

---

## 8. Резюме механик (быстрый ответ на частые вопросы)

| Вопрос | Ответ |
|---|---|
| Длина одного сегмента стены | 2×2 тайла, 4-12 builder slots в зависимости от variation (§4) |
| objcustom.cfg BuilderPoints override? | В файле только `ExitPoints/SmokePoints/Decal` — **все здания** считаются через динамический `_unit_CalcBuilderPoints` (обход периметра mask). Стены — единственное исключение, у них explicit BuilderPoints в `wallcustom.cfg`. |
| Ветшание (decay) HP | **Нет.** Здания теряют HP только от damage. Ни константы `gc_decay`, ни вызовов `_hp_decay` в скриптах не существует. |
| Исчезновение обломков | **Да, через ~60 секунд** после смерти здания. Цепочка handlers: `OnTagStates.essential_death` → `GameObjectMyDelayExecuteState('DeathStage1', gc_building_deathtime_0=30)` → `DeathStage1` → `GameObjectMyDelayExecuteState('DeathStage2', gc_building_deathtime_1=30)` → `DeathStage2` → `GameObjectRequestToDestroyByHandle`. Шахты уходят в 2× медленнее (`deathtime := deathtime*2`). См. `units/building.inc/{settagstates,deathstage1,deathstage2}.inc`. |
| Можно ли восстановить здание после HP=0 | **Нет.** `OnDeath` вызывает `_unit_DestroyObj` — здание удаляется. Мэш `<sid>_death1a/2a` — визуальные руины, не игровой объект. Только новое foundation. |
| Capture radius универсальный? | Да. `gc_gameplay_captureradius = 4.0 тайла` [^22]. Per-building override не найден. |
| Refund при отмене постройки | **Юнит-очередь:** `_unit_CancelUnitProduction` [^24] возвращает `price[k] × costmodifier`, где `costmodifier = pow(costpercent/100, restype)` и `restype` — счётчик built-копий, сохранённый в момент заказа. То есть возвращается ровно столько, сколько было списано. **Foundation (отмена кнопкой):** GUI-обработчик `_misc_GUICancelBuilding` [^25] вызывает только `GameObjectDestroyByHandle`. Зеркального `_res_AddResToPlayerByIndex` для foundation cost в скриптах нет — обработка возврата 100% потраченных ресурсов делается, видимо, на стороне C++ (поведение в игре подтверждено). |

## 9. Открытые вопросы

| # | Вопрос | Как решить |
|---:|---|---|
| 1 | FPS construct-анимации (= 32 или другой?) | Empirical: засечь время одного цикла молотка на строящемся здании |
| 2 | Точная стоимость одного сегмента стены (50 stone — за сегмент или за весь чертёж?) | Empirical: в редакторе поставить 1 сегмент, посмотреть списанные ресурсы |

---

## Источники

Все ссылки относительно `data/scripts/` в установке Cossacks 3.

[^1]: `gc_buildtime_modifier = 10` для зданий — `lib/misc.script:478-482`.

[^2]: Маска коллизий хранится в `collisionmaskproperty.Mask` каждого `data/objects/buildings/<sid>.prop`.

[^3]: Размер ячейки маски — `lib/unit.script:8712`:

    ```pascal
    cellSize := 0.5;
    ```

[^4]: ScaleFactor маски = 1 — `data/objects/buildings/refbuilding.prop:45`.

[^5]: Прибавка HP при ремонте — `units/unit.inc/onaclanimationreachedconstruct.inc:40-41`:

    ```pascal
    if (arg_obj.orders[0].itype = gc_obj_order_type_repair) then
       TObj(pobj).hp := Min(TObj(pobj).hp + gc_gameplay_repairhp, TObjBase(pobjbase).maxhp);
    ```

[^6]: `gc_gameplay_repairhp = 20` — `dmscript.global:211`.

[^7]: Прогресс за один удар при постройке — `units/unit.inc/onaclanimationreachedconstruct.inc:25-37`:

    ```pascal
    delta := (gc_buildtime_progressperhit / TObjBase(pobjbase).buildtime)
    buildprogress += delta
    deltahp := round(maxhp * delta)
    hp += deltahp   // capped at maxhp
    ```

[^8]: `gc_MaxBuilderCount = 30` — `dmscript.global:159`.

[^9]: `gc_BuilderDist = 1.0` — `dmscript.global:160`.

[^10]: `_unit_CalcBuilderPoints` — `lib/unit.script:8702-9006`.

[^11]: `_unit_OrderBuild` — `lib/unit.script:9285-9378`.

[^12]: `gc_MaxWallBuilderPointsCount = 16` — `dmscript.global:137`.

[^13]: Грузоподъёмность ferry — `lib/unit.script:2043` (`transport = 80 + 40 = 120`).

[^14]: Базовая европейская башня — `lib/unit.script:2223-2240`:

    ```pascal
    SetObjBaseWeapon(objprop, objbase, 0, 1000, 400, 550, 1500, 550, 50000, gc_obj_weapon_kind_cannonball, True);
    ```

[^15]: Сигнатура `SetObjBaseWeapon` — `lib/unit.script:520`.

[^16]: `consume.gold = 500/tick` для башни — `lib/unit.script:2235`.

[^17]: Russian-вариант башни — `lib/unit.script:2241-2247` (ветка `commonrus`).

[^18]: Условия пропуска `default = -1` в `SetObjBaseWeapon` — `lib/unit.script:523-538` (`if (damage<>-1)` и т.д.).

[^19]: Turkish-вариант башни — `lib/unit.script:2248-2256` (ветка `commontur`).

[^20]: Спецслучай для `gc_obj_usage_tower` — `lib/unit.script:178`.

[^21]: Механика захвата — `lib/miscext.script:1018-1030`.

[^22]: `gc_gameplay_captureradius = 214/53.33 = 4.0` — `dmscript.global:208` (см. также `lib/miscext.script:1018`).

[^23]: Множитель score за захват — `lib/unit.script:3837-3841`.

[^24]: `_unit_CancelUnitProduction` — `lib/unit.script:5891-5977`.

[^25]: `_misc_GUICancelBuilding` — `lib/miscext2.script:3898-3953`.

[^27]: State-машина смерти здания — `data/scripts/units/building.inc/settagstates.inc:32-53`.

[^28]: `DeathStage1` — `data/scripts/units/building.inc/deathstage1.inc:5-11`. `DeathStage2` определён в `deathstage2.inc`.

[^29]: Установка материала `'debris'` для трупа здания — `data/scripts/units/building.inc/ontagstates.inc:286`.

[^30]: `DeathStage2` — освобождение клетки и финальное удаление — `data/scripts/units/building.inc/deathstage2.inc:8-15`.

[^31]: `_unit_DestroyObj` — `lib/miscext2.script:4232-4242`.

[^32]: `_unit_DoUnitsGoOutside` — `lib/unit.script:4559-4564`.

[^33]: OnDeath-хук здания — `data/scripts/units/building.inc/ondeath.inc:11-25`.

[^34]: `_unit_ProduceUnit` — `lib/unit.script:10351`.

[^35]: `_unit_CancelUpgradePerform` — `lib/unit.script:5837-5889`.
