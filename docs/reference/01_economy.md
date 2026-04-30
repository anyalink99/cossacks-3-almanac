# 01. Экономика

[← Index](README.md)

> **Глубокие исследования по этой главе:**
>
> - [`../recon/peasant_extraction.md`](../recon/peasant_extraction.md) — полный разбор цикла крестьянина, animation frames, walk speed, fieldlife регенерация, формулы и открытые empirical-вопросы (см. §9)
> - [`../recon/map_generation_pipeline.md`](../recon/map_generation_pipeline.md) — что появляется на карте (леса, камни, шахты) и где именно
> - [`../reports/map/map_resources.md`](../reports/map/map_resources.md) — подсчёт ресурсов на стандартной карте Tiny + Highlands + Rich (~109 больших деревьев, ~33 камня, до 12 шахт / игрок)

## Резюме

Один крестьянин за рейс приносит `delivered = (portion × eff) / 100`. `eff` стартует со 100, апгрейды накапливаются аддитивно. Шахты работают по другой схеме: каждый крестьянин внутри добавляет 13 к `gPlayer.counter.resincome`, реальная скорость — 1.664 ресурса в игровую секунду.

## Глобальные константы

| Параметр | Значение | Источник |
|---|---:|---|
| `gc_time_to_frames` | 32 | dmscript.global:175 |
| `gc_pixels_to_tile` | 53.3333 | dmscript.global:172 |
| `gc_settings_gamespeed_0` (slow) | 7 тиков/сек | dmscript.global:1027 |
| `gc_settings_gamespeed_1` (normal) | 10 | dmscript.global:1028 |
| `gc_settings_gamespeed_2` (fast) | 14 | dmscript.global:1029 |
| `gc_MaxObjCount` | 32000 | dmscript.global:110 |
| `gc_MaxPlayerCount` | 12 | dmscript.global:97 |
| `gc_FieldMaxHP` | 25000 | dmscript.global:128 |
| `gc_obj_foodperunit` | 30 food / юнит | dmscript.global:808 |
| Default `eff` | 100% | player.script:109 |

Все опции лобби (стартовые ресурсы, время мира, лимит населения, переход в 18 век, сложность ИИ и т. д.) — таблицы в [`docs/reports/map/lobby_settings.md`](../reports/map/lobby_settings.md), поведение движка — в [`docs/recon/game_settings.md`](../recon/game_settings.md).

## Базовые порции и hits

| Ресурс | Базовая порция | Hits | Источник |
|---|---:|---:|---|
| food | **45** | 22 | dmscript.global:799,804 |
| wood | **28** | 14 | dmscript.global:800,805 |
| stone | **40** | 20 | dmscript.global:801,806 |
| gold/iron/coal/прочее | **20** | n/a | unit.script:9551 (хардкод) |

## Формула добычи

```
delivered = (base_portion × eff) / 100   # integer division
```

Пример: с апгрейдами academy.1 (+40% food) и mill.1 (+140% food) → `eff = 100 + 40 + 140 = 280`. Крестьянин приносит `45 × 280 / 100 = 126` еды за рейс (вместо базовых 45).

Все апгрейды eff — в `player.script:1813-1828`. Список — в [05_upgrades.md](05_upgrades.md#economy-eff).

## Шахты (gold/iron/coal)

Шахта: HP = 2500, `buildtime` = 300 кадров = 9.38 g-сек, цена W100 / S100, `peasantabsorber = 5` (5 крестьян макс. база). Каждый крестьянин внутри добавляет к `produce[restype]` 13.

**Расчёт:**

```
bank_per_sec = 13 × 32 = 416   # на крестьянина в игровую секунду
real_per_sec = 416 / 250 ≈ 1.664   # ресурса в игровую секунду
real_per_min = 99.84            # ≈ 100 ресурса в игровую минуту на крестьянина
```

**Полная прокачка одной шахты** (6 апгрейдов):

| Уровень | +работников | F | G | Накопительно |
|---:|---:|---:|---:|---:|
| eurgol.1 | +5 | 1000 | 1250 | 10 |
| eurgol.2 | +8 | 5250 | 4950 | 18 |
| eurgol.3 | +10 | 12500 | 9250 | 28 |
| eurgol.4 | +12 | 15800 | 18500 | 40 |
| eurgol.5 | +15 | 19800 | 21050 | 55 |
| eurgol.6 | +40 | 50200 | 25950 | 95 |

**Итого:** 5 базовых + 6 апгрейдов = **95 крестьян/шахта = 158.1 ресурса в g-сек = 9485 в g-мин**.

**Стоимость полной прокачки одной шахты:** F104,550 + G80,950.

## Поле (food, fieldlife, регенерация)

HP поля = `gc_FieldMaxHP = 25000`. Урон полю за удар: `resdec = max(1, floor(100 / (1 + fieldlife / 100)))`.

| fieldlife | resdec/удар | Макс. ударов | Макс. food при eff=100 |
|---:|---:|---:|---:|
| 0 | 100 | 250 | 511 |
| 100 | 50 | 500 | 1022 |
| 200 | 33 | 757 | 1548 |
| 300 | 25 | 1000 | 2045 |
| 500 | 16 | 1562 | 3195 |

Апгрейды fieldlife: `aca.4` (+200), `bla.1` (+100). Сумма = 300 → ~2045 food / поле.

## Корабли — fishing

`fishboat`: HP = 300, цена W600, `fishingmax = 1000` (база), `fishingspeed = 50/4 = 12` тиков на одну рыбу. Апгрейд `aca.5` (`+100% boat efficiency`) удваивает грузоподъёмность → **2000 food / рейс**. Апгрейд `aca.7` (`-85% fishing boat cost`) удешевляет постройку.

Полный список кораблей — в [compare/ships.md](compare/ships.md).

## Famine (голод) и Rebellion (восстание)

Источник: `unit.inc/nothing.inc:445-505`, `player.script:280-322`

**Расход food (upkeep).** Каждый юнит без `bnohungry = True` накапливает у игрока `gPlayer.counter.resconsume[food]` (`unit.script:3810,3821`):

```
per_unit_resconsume_food = consume.food          # из case-ветки в unit.script
                         + gc_obj_foodperunit    # = 30, если !bnohungry и !bbuilding
```

Расход food за игровую секунду (`player.script:_player_ProcessResourceConsume`):

```
food_per_g_sec = sum_of_resconsume_food × gc_time_to_frames / 20000
               = sum × 32 / 20000  =  sum × 0.0016
```

**Sanity-check (verified empirically 2026-04-29):** 18 австрийских крестьян (`consume.food = 32`, `bnohungry = False`) простаивают 2 игровые минуты:

```
sum = 18 × (32 + 30) = 1116
food / g-sec = 1116 × 32 / 20000 ≈ 1.786
за 120 g-сек ≈ 214 food   ✓
```

Расход food / g-сек на одного юнита (для `bnohungry = False`):

| Юнит | `consume.food` | + `gc_obj_foodperunit` | итого | food / g-сек |
|---|---:|---:|---:|---:|
| peasant (aus / pol / spa / eng / ukr / sco) | 32 | +30 | 62 | 0.0992 |
| peasant `peatur` / `peaalg` | 28 | +30 | 58 | 0.0928 |
| peasant `pearus` | 26 | +30 | 56 | 0.0896 |
| infantry без явного `consume.food` | 0 | +30 | 30 | 0.0480 |

**Famine flag** (`bfamine = True`): срабатывает когда `food = 0` И есть `consume > 0`.

При famine **юниты без `bnohungry` начинают умирать рандомно**. Шанс смерти за тик зависит от **сложности игрока** (`gPlayer.difficulty`):

| Difficulty | Шанс смерти за тик | Ожидаемое время до смерти 1 юнита |
|---|---:|---|
| 0 (easy) | `RandomInt < 5` ≈ 0.0076% | очень медленно (часы) |
| 1 (normal) | `RandomInt < 12` ≈ 0.018% | ~часы |
| 2+ (hard / very hard / impossible) | **`RandomInt < 50` ≈ 0.076%** | **минуты** (4-10× быстрее normal) |

**Кто иммунен к голоду** (`bnohungry = True` в `unit.script`):

- Все здания — флаг ставится в `SetObjBuildingBaseSettings` / `SetObjBuildingExtProperties` (`unit.script:471`).
- Наёмники (`bmercenary = True`). У них свой триггер — Rebellion (см. ниже). Едят gold, не food.

**Кто НЕ иммунен** (вопреки распространённому заблуждению):

- **Крестьяне** — у всех `bnohungry = False`. У `peaaus` / `peapol` / `peaspa` / `peaeng` / `peaukr` / `peasco` `consume.food = 32`, у `pearus` = 26, у `peatur` / `peaalg` = 28. Плюс +30 от `gc_obj_foodperunit`. Простаивающие крестьяне расходуют food.
- **Officers / drummers / priests** — едят food (+30) поверх своего `consume[gold]`.
- **Регулярная пехота / кавалерия** — `bnohungry = False`, `food upkeep = consume.food + 30`.

Точное значение `bnohungry` для каждого юнита — в [`docs/data.json`](../data.json), поле `bnohungry`.

**Голод также отключается**, если в профиле игрока `gProfile.bFamine = False`.

---

## Дипломатический центр и наёмники

Полный разбор — в [`recon/mercenaries_diplomacy.md`](../recon/mercenaries_diplomacy.md). Здесь — суть.

Дипломатический центр (`<nat>dip`) — здание середины игры, требующее **Академию** (`<nat>aca`) и Городской центр. Есть у всех 21 нации, но характеристики различаются:

| Здание | Нации | HP | Wood | Stone | Gold |
|---|---|---:|---:|---:|---:|
| `<nat>dip` (default) | aus, fra, eng, spa, pol, swe, pru, ven, net, den, por, pie, sax, bav, hun, swi, sco | 4500 | 4900 | 1700 | 0 |
| `rusdip` | rus | 6500 | 7900 | 3700 | 0 |
| `ukrdip` | ukr | 5000 | 3900 | 2700 | 0 |
| `turdip` / `algdip` | tur, alg | 5500 | 4600 | 2020 | 0 |

Для всех: `buildtime = 1000` кадров = **312.5 g-сек**, `costpercent = 100` (цена каждого следующего здания не растёт), `bcapture = False` (захвату не подлежит, только разрушение). По локализации — **«можно построить только один Дипломатический центр на игрока»**; это ограничение GUI, а не `costpercent`.

### Каталог наёмников (8 sid)

Ростер одинаков для **всех 21 нации**. Цена в gold, upkeep тоже в gold (`consume.gold`), `bnohungry = True` (food не потребляют).

С 2026-04-30 `docs/data.json` корректно учитывает `if (bmercenary)`-override; все 168 dip-юнитов несут merc-статы. Числа ниже совпадают с тем, что в data.json.

| sid | HP | buildtime (frames) | gold (цена) | consume.gold (upkeep) | costpercent | оружие |
|---|---:|---:|---:|---:|---:|---|
| `lightinfantrydip` | 50 | 40 | **4** | 4 | 100 | sword 16 (range 50px) |
| `roundshierdip` | 75 | 48 | **12** | 20 | 100 | sword 6 (range 50px) |
| `archerdip` | 20 | 40 | **15** | 16 | 100.5 | arrow 25 / firearrow 100 |
| `archerturdip` *(EarlyBird DLC)* | 20 | 40 | 15 | 16 | 100.5 | то же |
| `grenadierdip` | 30 | 48 | **25** | 60 | 100.5 | pike 30 / bullet 16 / grenade 200 |
| `cossacksichdip` | 150 | 80 | **60** | 150 | 100.5 | horse-sword 8 |
| `dragoon18dip` | 100 | 64 | **120** | 120 | 102 | horse-bullet 18 (range 800) |
| `lightcavalrydip` *(EarlyBird DLC)* | 100 | 64 | 120 | 120 | 102 | то же |

### Масштабирование цены

Действует общее правило `cost(N) = floor(base × (costpercent/100)^N)`, **но потолок для наёмников = 2×** (вместо 20000× у обычных юнитов). При `costpercent = 100.5` потолок достигается примерно на 139-м экземпляре, дальше цена не растёт.

**Парные счётчики:**

- `archerdip` ↔ `archerturdip` — общий счётчик в расчёте цены. Наняв 100 turdip-лучников, игрок получает обычных `archerdip` уже **вдвое дороже**.
- `dragoon18dip` ↔ `lightcavalrydip` — аналогично.

### Формула gold-upkeep

```
drain_per_g_sec = Σ(consume.gold) × 32 / 20000
                = Σ × 0.0016
```

Та же формула, что и для food-upkeep (см. выше). Например, 50 `dragoon18dip` → 50 × 120 × 0.0016 = **9.6 gold/g-сек ≈ 576 gold за игровую минуту**. Потребуется доход gold уровня середины игры (1–2 шахты + рынок).

### Rebellion (восстание): механика

**`brebellion = True`** срабатывает, когда выполнены оба условия:

1. `gPlayer.res[gold] = 0` (gold исчерпан);
2. **и** `gPlayer.counter.resconsume[gold] > resincome[gold]` (структурный дефицит, а не кратковременный пик расхода).

Если доход gold покрывает upkeep, **бунт не возникает даже при кратком обнулении gold**. Если игрок продаёт всех наёмников — `resconsume[gold] = 0`, и бунт автоматически снимается.

При активном `brebellion` каждый наёмник на каждом Nothing-тике (периодически, ~0.625 g-сек) делает бросок `_misc_RandomInt < threshold`, где `_misc_RandomInt = floor(random × 32768)`:

| Difficulty | Threshold | Шанс перехода за тик |
|---|---:|---:|
| 0 (easy) | 100 | 100/32768 ≈ **0.305%** |
| 1 (normal) | 200 | 200/32768 ≈ **0.610%** |
| ≥ 2 (hard / veryhard / impossible) | **6000** | 6000/32768 ≈ **18.31%** |

На hard ожидаемое время до перехода одного наёмника составляет `0.625 / 0.1831 × 0.5 ≈ 1.7 g-сек`. **Армия из 50 наёмников разбегается почти полностью за 5–10 g-сек.** На easy и normal бунт практически декоративен.

При переходе наёмник попадает в **виртуального игрока-наёмника** (`gc_player_mercenaryind = MaxPlayerCount - 1`), автоматически враждебного всем настоящим игрокам. То есть бывший союзник становится агрессивным NPC-юнитом, а не нейтралом.

### Стратегические выводы

- **Наёмники наиболее эффективны на средне-длинной дистанции:** food не потребляют (`bnohungry = True`), но требуют постоянного дохода gold. В долгих играх с большой армией наёмники могут оказаться дешевле обычных юнитов (нет затрат food и крестьян на её добычу).
- **Один тип наёмников быстрее «прогревает» цену.** Нужно много `dragoon18dip` — чередуй с `lightcavalrydip`: парный счётчик удорожает обоих одинаково, но всё равно не выше потолка 2×.
- **Не держи большую наёмную армию при нулевом gold.** На hard это **мгновенная катастрофа** (18% за тик × 50 юнитов — почти вся армия за пару секунд).
- **`cossacksichdip` HP = 150 за 60 gold и 150 gold upkeep** — самый дешёвый и живучий gold-юнит, доступный всем нациям. Но melee-урон 8 — это «деньги в HP», а не в DPS.

### Карточный режим `marketdip = expensivemercs`

Включает множитель `gc_gameplay_expensivemercskoef = 3` — наёмники стоят **втрое дороже** в gold. Используется в ряде исторических битв для ослабления dip-стратегии.

---

**Расход gold юнитами** (`consume[gold]`): в основном у башен (`consume[gold] = 500`), у некоторых стрелковых юнитов (выстрел тратит `weapon.cost[gold]`) и у **всех наёмников через `consume.gold`**. Обычные pikeman и musketeer gold **не потребляют** в простое — только при выстреле, через `weapon.cost[gold]`.

## Discrepancies (расхождения с промпт-заметками)

| Факт | Заметки | В файле | Источник | Вердикт |
|---|---|---|---|---|
| hits_needed for food | 30 | **22** | dmscript.global:799 gc_resource_hitsneeded_food | Файл: 22, не 30. Доверяем файлу — крестьянин делает 22 удара мотыгой до возврата к складу, не 30. Это укорачивает рейс и повышает фактический rate. |
| Field melioration (academy aca.4) cost | W1400 / G522 | **W1000 / G475 (any nation)** | country.script:3490 _country_AddUpgrade('aca.4', ..., wood=1000, gold=475) | Файл: W1000/G475. Расхождение с промпт-заметками — возможно, цифры из старой версии игры. Все 21 нация имеют одинаковую стоимость. |
| 'Manufacture agricultural equipment' (blacksmith) cost | W400 / G100 | **не найден в blacksmith — этот апгрейд может быть из старого названия** | country.script — нет blacksmith-апгрейда с такими параметрами | Текущий blacksmith содержит per-unit damage/protection апгрейды. Возможно, в C1 был отдельный agricultural-equipment апгрейд, который в C3 переименован в `aca.X` (academy). См. лист Upgrades с place=aca. |

## Sanity

Sanity checks: **112/112** PASS. См. xlsx → лист `Sanity_checks`.
