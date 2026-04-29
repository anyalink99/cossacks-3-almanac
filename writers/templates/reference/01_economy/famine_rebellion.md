## Famine (голод) и Rebellion (восстание)

Источник: [`unit.inc/nothing.inc:445-505`](file:///C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/units/unit.inc/nothing.inc), [`player.script:280-322`](file:///C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/player.script)

**Расход food (upkeep).** Каждый юнит без `bnohungry = True` накапливает у игрока `gPlayer.counter.resconsume[food]` ([`unit.script:3810,3821`](file:///C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/unit.script)):

```
per_unit_resconsume_food = consume.food          # из case-ветки в unit.script
                         + gc_obj_foodperunit    # = 30, если !bnohungry и !bbuilding
```

Расход food за игровую секунду ([`player.script:_player_ProcessResourceConsume`](file:///C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/player.script)):

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

- Все здания — флаг ставится в `SetObjBuildingBaseSettings` / `SetObjBuildingExtProperties` ([`unit.script:471`](file:///C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/unit.script)).
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

⚠️ **В `docs/data.json` для всех 168 dip-юнитов лежат НЕ-наёмничьи характеристики** — парсер не учитывает `if (bmercenary)`-override в скриптах. Числа ниже взяты из исходника `unit.script`.

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
