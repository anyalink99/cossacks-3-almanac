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

Точное значение `bnohungry` для каждого юнита — в [`output/data.json`](../data.json), поле `bnohungry`.

**Голод также отключается**, если в профиле игрока `gProfile.bFamine = False`.

---

**Rebellion flag** (`brebellion = True`): срабатывает когда `gold = 0` И `consume[gold] > income[gold]`.

При rebellion **наёмники массово переходят на сторону нейтрала**:

| Difficulty | Шанс перехода за тик |
|---|---:|
| 0 (easy) | `RandomInt < 100` ≈ 0.15% |
| 1 (normal) | `RandomInt < 200` ≈ 0.3% |
| 2+ (hard+) | **`RandomInt < 6000` ≈ 9.2%** — буквально за секунды теряешь весь наёмный контингент |

**Стратегические выводы:**

- На сложности **hard и выше** держать food и gold выше нуля критически важно. Даже короткий простой → массовая смерть юнитов и/или дезертирство наёмников.
- На easy голод (famine) практически декоративен — можно играть без апгрейдов мельницы.
- **Наёмники (`<unit>dip` суффикс) тратят gold-апкип** — поэтому большая дипломатическая армия требует высокого дохода золота.

---

**Расход золота юнитами** (`consume[gold]`): в основном у стрелковых башен (port, tower) и наёмников. Стандартный pikeman / musketeer золото **не потребляет** (только при стрельбе — `weapon.cost[gold]`).
