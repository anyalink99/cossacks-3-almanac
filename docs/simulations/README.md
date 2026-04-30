# Симуляции экономики

Выходы симулятора по конкретным build order'ам. Каждая симуляция — пара `<name>.csv` (снимок состояния каждые 5 g-сек) + `<name>.md` (человеко-читаемый отчёт: финальное состояние, таймлайн, журнал событий).

## Что есть сейчас

| Симуляция | Билд-ордер | Описание |
|---|---|---|
| [sim_bav_basic_5min.md](sim_bav_basic_5min.md) | [`simulator/build_orders/bav_basic_5min.json`](../../simulator/build_orders/bav_basic_5min.json) | Базовый дебют за Баварию: к ~4.3 real-min — 15 крестьян, 1 ратуша, 2 жилища, mill+bla+bar, 5 шахт, 10 мушкетёров. |
| [sim_bav_with_fields.md](sim_bav_with_fields.md) | [`simulator/build_orders/bav_with_fields.json`](../../simulator/build_orders/bav_with_fields.json) | Тот же дебют + посадка полей через `plant_fields`. Сравнение по food-добыче. |

## Как запустить свою симуляцию

```bash
python simulator/simulate_economy.py simulator/build_orders/<your_build>.json
# → docs/simulations/sim_<your_build>.csv
# → docs/simulations/sim_<your_build>.md
```

Скрипт: [`../../simulator/simulate_economy.py`](../../simulator/simulate_economy.py). Полная схема build order'а — в шапке файла.

## Формат build order

```json
{
  "nation": "bav",
  "game_speed": "fast",
  "starting_resources": {"food": 1000, "wood": 1000, "stone": 0, "gold": 0, "iron": 0, "coal": 0},
  "starting_units": {"peaaus": 5},
  "starting_buildings": {"bavcen": 1, "eursto": 1, "euriro": 1},
  "max_time_sec": 360,
  "actions": [
    {"at": 0,   "do": "assign", "food": 2, "wood": 2, "euriro": 1},
    {"at": 0,   "do": "train",  "building_sid": "bavcen", "unit_sid": "peaaus", "amount": 10},
    {"at": 30,  "do": "build",  "sid": "bavhou", "builders": 1},
    {"at": 100, "do": "research", "upgrade_sid": "bavmil.1"},
    {"at": 200, "do": "build",  "sid": "bavbla", "builders": 1},
    {"at": 290, "do": "train",  "building_sid": "bavbar", "unit_sid": "musketeer", "amount": 15}
  ]
}
```

**Действия:**

| `do` | Поля | Что делает |
|---|---|---|
| `assign` | `food`/`wood`/`stone` (поверхность) и/или `<cluster><gol\|iro\|coa>` (внутри шахт) | Перераспределяет крестьян на ресурсы. Перезаписывает предыдущее назначение. |
| `build` | `sid`, `builders` (1-5) | Начинает постройку. Цена списывается мгновенно при размещении foundation. |
| `train` | `building_sid`, `unit_sid`, `amount` | Ставит N юнитов в очередь конкретного здания. Цена каждого списывается при старте. |
| `research` | `upgrade_sid` | Запускает апгрейд. Здание занято на `upgrade.time_sec`. |
| `plant_fields` | `mill_sid`, `count` | Сажает N полей вокруг мельницы. Цикл: рост 87.5 g-сек → урожай → restart 21.875 g-сек. |

## Что симулируется (и что нет)

| Механика | Реализована | Формула / источник |
|---|:---:|---|
| Доход food/wood/stone | да | `portion × eff / (hits × T_hit) × (1 - walk_overhead)` |
| Доход gold/iron/coal | да | `13 × 32 / 250 × eff/100 × (1 - mine_overhead)` на крестьянина в шахте |
| Расход food (upkeep) | да | `consume.food × 32 / 20000` на юнит за g-сек |
| Постройка зданий | да | `buildtime × speedup_by_builders` (1→1.0, 2→0.65, 3→0.5...) |
| Производство юнитов | да | 1 юнит за `unit.buildtime` на каждый экземпляр здания |
| Исследование апгрейдов | да | занимает `upgrade.time_sec` |
| Проверка предусловий | да | действия пропускаются с предупреждением, если prereq не выполнен |
| Масштабирование цены (`costpercent`) | да | `floor(base × (cp/100)^count)` |
| Лимит фермы | да | тренировка останавливается при `farm_used + 1 > farm_cap` |
| Апгрейды эффективности | да | `effectfood`/`wood`/`stone`/`perc` применяется по завершении |
| Апгрейды HP полей (`fieldlifeperc`) | да | применяется по завершении |
| Поля (рост/харвест/restart) | да | через `plant_fields`, цикл по реальной механике |

| Не симулируется | Почему |
|---|---|
| Физическая длина перемещения | используется статический `walk_overhead = 0.30` (настраивается) |
| Истощение деревьев | пеньки бесконечны → wood pool безлимитен (это правда игры) |
| Истощение камня | 10M HP — практически бесконечно |
| Отмена постройки / возврат ресурсов | не реализовано |

## Что писать с помощью этих инструментов

С `production_rates.md` + `tech_tree.md` + симулятором можно:

- **Сравнить дебюты численно.** Написать 3-5 разных build order'ов для одной нации, прогнать симулятор, посмотреть «у кого больше юнитов к t=180g», «у кого выше доход в пике».
- **Оптимизировать распределение крестьян.** Прогонять симуляции с разными `assign` (3-2-0 vs 2-3-1 vs 4-2-1) и сравнивать итог.
- **Посчитать «минимум крестьян для X юнитов/мин»** — комбинация production_rates + цены + симулятор.
- **Спланировать переход в 18 век** — прогнать с `research="<csid>cen.1"` после aca/tem/art и достаточных ресурсов.
- **Сравнить нации** — тот же build order для разных `nation` → разница в стоимости, скорости, цене крестьянина (rus 26 food/peasant против 32 у большинства).

## Что ещё не реализовано

- **Time-to-X калькулятор** — обратная задача: «хочу 30 мушкетёров к t=10 min, предложи build order» (микро-поиск поверх симулятора).
- **Бюджет «доход против upkeep»** — комбинация production_rates с расходом еды/золота юнитами: при какой армии экономика «уходит в минус».
- **Эмпирическая скорость крестьянина** в тайлах за g-сек — нужна для замены статического `walk_overhead = 0.30` физическим расчётом. См. [`../recon/peasant_extraction.md`](../recon/peasant_extraction.md) §9.
- **Тир-лист по нациям** — требует судейства, не извлекается автоматически.
