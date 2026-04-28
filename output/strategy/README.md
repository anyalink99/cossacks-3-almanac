# Strategy inputs — что есть для написания стратегий

Это **точка входа** для построения стратегий. Описывает что доступно после реализации пунктов 1-3 из плана.

## 1. Production-rate таблицы

**Файл:** [`production_rates.md`](production_rates.md) (~100 KB).

Что внутри: для каждой нации × каждого здания × каждого юнита, которого оно производит:
- buildtime (game-sec)
- rate units/g-min (теоретический максимум при бесперебойной очереди)
- rate units/real-min @ fast (×1.4)
- цена и upkeep food

Пример — Bavarian musketeer:

| Юнит | buildtime (g-sec) | rate units/g-min | rate units/real-min @ fast |
|---|---:|---:|---:|
| musketeer | 6.00 | 10.0 | **14.0** |

**Механика:** одно здание = одна очередь (`orders[0]`). Параллельной постройки **нет**. Чтобы получить 100 musketeer/min, нужно ~7 бараков.

Источник: `units/building.inc/doprogressorders.inc` — описано в шапке файла.

---

## 2. Tech tree (зависимости)

**Файлы:**
- [`tech_tree.md`](tech_tree.md) (~210 KB) — человеко-читаемый граф по нациям
- [`tech_tree.json`](tech_tree.json) (~2.8 MB) — структурированный для программ

Что внутри: для каждой сущности (здание/юнит/апгрейд) — список prereqs:
- `[B]` — нужно построенное здание
- `[U]` — нужен живой юнит (редко)
- `[T]` — нужен исследованный апгрейд

Пример (Бавария):
```
bavba2 (Барак 18в) → требует: [T] bavcen.1 (переход в 18в)
bavcen.1 (18 century) → требует: [B] bavaca, [B] bavtem, [B] bavart
cuirassier → требует: [B] bavbla, [T] bavcen.1
musketeer18bav → требует: [B] bavbla
```

**Источник:** `_country_AddFixedProduceWithAccessControl` и `_country_AddUpgradeWithAccessControl` (параметры `req0..req7`). Извлечение в `parser/simulate_upgrades.py` → `parser/build_data.py` → `compute/build_tech_tree.py`.

**Что НЕ покрыто:**
- Несколько prereq-ов помечены как `req0` (literal string) — это нерезолвенные переменные в скрипте, обычно для специфических наций.
- `century18` алиас: для большинства наций = `<csid>cen.1`. У `ukr/tur/alg` нет 18 века.

---

## 3. Timeline-симулятор экономики

**Скрипт:** [`simulator/simulate_economy.py`](../../simulator/simulate_economy.py)

**Использование:**
```bash
python simulator/simulate_economy.py simulator/build_orders/bav_basic_5min.json
# → output/sim_bav_basic_5min.csv
# → output/sim_bav_basic_5min.md
```

**Build order JSON** ([полная схема в шапке скрипта](../../simulator/simulate_economy.py)):
```json
{
  "nation": "bav",
  "game_speed": "fast",
  "starting_resources": {"food": 1000, "wood": 1000, ...},
  "starting_units": {"peaaus": 5},
  "starting_buildings": {"bavcen": 1, "eursto": 1, "euriro": 1, ...},
  "max_time_sec": 360,
  "actions": [
    {"at": 0,   "do": "assign", "food": 2, "wood": 2, "euriro": 1},
    {"at": 0,   "do": "train",  "building_sid": "bavcen", "unit_sid": "peaaus", "amount": 10},
    {"at": 30,  "do": "build",  "sid": "bavhou", "builders": 1},
    {"at": 200, "do": "build",  "sid": "bavbla", "builders": 1},
    {"at": 290, "do": "train",  "building_sid": "bavbar", "unit_sid": "musketeer", "amount": 15},
    {"at": 100, "do": "research", "upgrade_sid": "bavmil.1"}
  ]
}
```

**Action types:**
- `assign` — пересадить крестьян на ресурсы. Поля: `food`/`wood`/`stone` (выше земли) и любые `<cluster><gol|iro|coa>` (внутри шахт). Перезаписывает предыдущее назначение.
- `build` — начать постройку здания. Поля: `sid`, `builders` (1-5, влияет на скорость).
- `train` — поставить N юнитов в очередь конкретного здания. Поля: `building_sid`, `unit_sid`, `amount`.
- `research` — начать апгрейд. Поле: `upgrade_sid`.

**Что симулируется:**

| Механика | Реализована? | Формула / источник |
|---|:---:|---|
| Income food/wood/stone | yes | `portion × eff / (hits × T_hit) × (1-walk_overhead)` |
| Income gold/iron/coal | yes | `13 × 32 / 250 × eff/100 × (1-mine_overhead)` per peasant inside mine |
| Upkeep food | yes | `consume_food × 32 / 20000` per unit per g-sec |
| Building construction | yes | `buildtime × speedup_by_builders` (1→1.0, 2→0.65, 3→0.5...) |
| Unit production | yes | 1 unit per `unit.buildtime` per building instance |
| Upgrade research | yes | takes `upgrade.time_sec` |
| Prereq enforcement | yes | actions skip with warning if any prereq missing |
| Cost scaling (costpercent) | yes | `floor(base × (cp/100)^count)` |
| Farm cap | yes | training stops if `farm_used + 1 > farm_cap` |
| Efficiency upgrades | yes | apply effectfood/wood/stone/perc on completion |
| Field life upgrades | yes | apply fieldlifeperc on completion |

**Что НЕ симулируется (упрощения):**

| Механика | Почему |
|---|---|
| Walking distance physically | используется статический `walk_overhead = 0.30` (можно настроить в build_order) |
| Tree depletion | пул дерева на карте безграничный |
| Field regen + restart циклы | предполагается бесконечная еда от поля |
| Stone exhaustion | камень бесконечный (10M HP, реалистично) |
| Очередь продолжения после произведённого юнита | `train amount=10` ставит 10 в очередь сразу — после производства одного следующий из очереди стартует автоматически. Но cost для каждого ВЫЧИТАЕТСЯ при старте этого юнита. |
| Несколько типов юнитов в очереди одного барака | сейчас работает корректно (массив unit_queues[bld] поддерживает разные `unit_sid`). |
| Отмена постройки / возврат ресурсов | не реализовано. |

**Output:**

1. `<prefix>.csv` — snapshot каждые 5 g-sec со столбцами:
   - `t_g, t_real`
   - `res_food, res_wood, res_stone, res_gold, res_iron, res_coal`
   - `farm_cap, farm_used, peasants_total, peasants_idle`
   - `bld_<sid>` для каждого построенного типа здания
   - `unit_<sid>` для каждого типа юнита
   
2. `<prefix>.md` — markdown отчёт с:
   - финальное состояние
   - сводная timeline-таблица каждые 15 g-sec
   - полный лог событий (TRAIN, BUILT, RESEARCHED, SKIP, ERROR)

---

## Пример: bavarian basic opening

**Build order:** [`simulator/build_orders/bav_basic_5min.json`](../../simulator/build_orders/bav_basic_5min.json)
**Result:** [`sim/sim_bav_basic_5min.md`](sim/sim_bav_basic_5min.md)

К t=360g (≈4.3 real-min @ fast):
- 15 peasants, 1 town center, 2 housing, 1 mill, 1 blacksmith, 1 barracks, 5 mines (1 active iron, 1 active gold)
- 10 musketeer'ов произведено (rate ~1 musketeer/7 g-sec из одного барака)
- ~1500 еды / ~2700 wood / ~500 stone / ~520 gold / ~1700 iron в банке

---

## Что писать на этих инструментах

С production rates + tech tree + симулятором можно теперь:

### A. Сравнить разные openings численно
Написать 3-5 разных build_orders для одной нации, прогнать симулятор, сравнить:
- "к t=180g кого больше юнитов?"
- "у кого выше income в момент пика?"
- "у кого позиция ресурсов лучше для следующего шага?"

### B. Оптимизировать distribution крестьян
Запускать симуляции с разными `assign` (3-2-0 vs 2-3-1 vs 4-2-1) и сравнить final state.

### C. Посчитать "минимум peasants для X юнитов/мин"
Если хочу выпускать 30 musketeer/min, мне нужно ~3 барака. Каждый musketeer стоит F45 G6 I5. 30/min × 5 iron = 150 iron/min = 2.5 iron/sec. Нужно ~1.6 крестьянина в железной шахте при walk_overhead=0.05 → 2 крестьянина с запасом.

### D. Спланировать переход в 18 век
Прогнать build_order с research="bavcen.1" в момент когда есть aca+tem+art и достаточно ресурсов (F30000 G5000 I2000 C2000).

### E. Сравнить нации
Тот же build_order для разных наций (`"nation": "fra"` vs `"nation": "rus"` etc.) → разница в стоимостях, скоростях постройки, peasant cost (rus 26 food/peasant vs default 32 для fra).

---

## Чего ещё не хватает (для следующих шагов)

Обозначено как пункты 4-9 в [`memory/project_extraction_model_plan.md`](.):
- DPS / EHP метрики
- Counter-unit матрицы
- Time-to-X таблицы (автокалькулятор минимального build_order для цели)
- Per-resource budget income vs upkeep
- Empirical: peasant speed in tiles/g-sec (для уточнения walk_overhead)
- Per-nation tier list (требует судейства)

---

## Скрипты этого блока

| Скрипт | Что делает | Output |
|---|---|---|
| `parser/build_data.py` | Извлекает всё из игры (расширен с prereqs) | `output/data.json` |
| `compute/build_tech_tree.py` | Tech tree + production rates | `output/tech_tree.{json,md}`, `output/production_rates.md` |
| `simulator/simulate_economy.py` | Симулятор экономики | `output/sim_<name>.{csv,md}` |
