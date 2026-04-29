# Расчётные отчёты (derived reports)

Производные расчёты на основе [`../data.json`](../data.json) — то, что нельзя прочитать напрямую из игровых скриптов и нужно посчитать. Каждый файл — самостоятельный отчёт; индекс ниже объясняет, что где искать.

## Боевая математика

| Файл | Что внутри | Генератор |
|---|---|---|
| [combat_stats.md](combat_stats.md) | DPS и effective HP (EHP) по типу оружия для всех боевых юнитов. | `compute/compute_combat_stats.py` |
| [counter_matrix.md](counter_matrix.md) | Приближённый TTK (time-to-kill) между классами юнитов с учётом защиты и попадания. | `compute/compute_counter_matrix.py` |

## Цены и масштабирование

| Файл | Что внутри | Генератор |
|---|---|---|
| [scaling_prices.md](scaling_prices.md) | Цена N-го экземпляра здания: `cost(N) = floor(base × (costpercent/100)^(N-1))`. Таблицы N=1..6. | `compute/compute_scaling.py` |
| [efficiency_upgrades.md](efficiency_upgrades.md) | Сводка по `gc_upg_type_effect*` — какие апгрейды что прибавляют (food/wood/stone/damage/protection/range). | `compute/compute_efficiency_upgrades.py` |

## Темп и тайминги

| Файл | Что внутри | Генератор |
|---|---|---|
| [production_rates.md](production_rates.md) | Для каждой нации × здания × юнита: `buildtime`, `units/g-min`, `units/real-min @ fast`, цена и upkeep. | `compute/build_tech_tree.py` |
| [tech_tree.md](tech_tree.md) | Дерево зависимостей: для каждого здания/юнита/апгрейда — список prereq'ов (`[B]` building, `[U]` unit, `[T]` upgrade). Машинная версия — `derived/tech_tree.json`. | `compute/build_tech_tree.py` |
| [construction_times.md](construction_times.md) | Время постройки каждого здания с 1, 2, 5, 10 строителями и при максимуме слотов. | `compute/compute_construction_times.py` |
| [builder_slots.md](builder_slots.md) | Сколько крестьян одновременно могут строить здание (вычисляется обходом периметра mask с шагом `gc_BuilderDist=1.0`). | `compute/compute_builder_slots.py` |

## Карта и старт

| Файл | Что внутри | Генератор |
|---|---|---|
| [map_resources.md](map_resources.md) | Подсчёт лесов/камней/шахт на стандартной карте Tiny + Highlands + Rich. ~109 больших деревьев, ~33 камня, до 12 месторождений на игрока. | `compute/compute_map_resources.py` |
| [starting_layout.md](starting_layout.md) | Стартовая раскладка: 18 крестьян в 6×3 grid возле центра города, расположение `cen` / `sto` / mines. | `compute/extract_starting_layout.py` |

## Связанные данные

- [`../reference/`](../reference/README.md) — каноническая справка (главы 01-06, nations, compare). Отчёты выше построены поверх неё.
- [`../derived/`](../derived/) — машинно-читаемые JSON-датасеты (`tech_tree.json`, `builder_slots.json`, `pattern_*.json`, `animations.json`).
- [`../simulations/`](../simulations/) — выходы симулятора экономики (timeline по конкретному build order).
- [`../../recon/`](../../recon/) — глубокие исследования механик, на которые опираются эти расчёты.

## Регенерация

После обновления `data.json`:

```bash
python compute/compute_combat_stats.py        # → reports/combat_stats.md
python compute/compute_counter_matrix.py      # → reports/counter_matrix.md
python compute/compute_efficiency_upgrades.py # → reports/efficiency_upgrades.md
python compute/compute_scaling.py             # → reports/scaling_prices.md
python compute/compute_map_resources.py       # → reports/map_resources.md
python compute/extract_starting_layout.py     # → reports/starting_layout.md
python compute/build_tech_tree.py             # → reports/tech_tree.md, production_rates.md + derived/tech_tree.json
python compute/compute_construction_times.py  # → reports/construction_times.md
python compute/compute_builder_slots.py       # → reports/builder_slots.md + derived/builder_slots.json
```
