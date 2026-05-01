# Расчётные отчёты (derived reports)

Производные расчёты на основе [`../../data.json`](../../data.json) — то, что нельзя прочитать напрямую из игровых скриптов и нужно посчитать. Сгруппированы по теме; индекс ниже.

## Бой ([`combat/`](combat/))

| Файл | Что внутри | Генератор |
|---|---|---|
| [combat/combat_stats.md](combat/combat_stats.md) | DPS и effective HP (EHP) по типу оружия для всех боевых юнитов. | `compute/compute_combat_stats.py` |
| [combat/counter_matrix.md](combat/counter_matrix.md) | Приближённый TTK (time-to-kill) между классами юнитов с учётом защиты и попадания. | `compute/compute_counter_matrix.py` |
| [combat/attack_rates.md](combat/attack_rates.md) | Скорость атаки на юнита: длительность цикла (pause или анимация attack0), атак/g-сек, атак/real @ fast. | `compute/compute_attack_rates.py` |
| [combat/vision_radii.md](combat/vision_radii.md) | Vision (FOW) и searchradius по всем юнитам. Формула `floor(20 + 4×vision)` тайлов. Лучшие скауты (Барабанщик, Гетьман, корабли). | `compute/compute_vision.py` |
| [combat/artillery.md](combat/artillery.md) | Сводка по сухопутной артиллерии (`bartillery = True`): damage, pause, dispertion, цена выстрела, лимит парка от Артиллерийского депо, экономика юнита и национальные различия. | `compute/compute_artillery.py` |

## Экономика ([`economy/`](economy/))

| Файл | Что внутри | Генератор |
|---|---|---|
| [economy/scaling_prices.md](economy/scaling_prices.md) | Цена N-го экземпляра здания: `cost(N) = floor(base × (costpercent/100)^(N-1))`. Таблицы N=1..6. | `compute/compute_scaling.py` |
| [economy/efficiency_upgrades.md](economy/efficiency_upgrades.md) | Сводка по `gc_upg_type_effect*` — какие апгрейды что прибавляют (food/wood/stone/damage/protection/range). | `compute/compute_efficiency_upgrades.py` |
| [economy/production_rates.md](economy/production_rates.md) | Для каждой нации × здания × юнита: `buildtime`, `units/g-min`, `units/real-min @ fast`, цена и upkeep. | `compute/compute_tech_tree.py` |
| [economy/construction_times.md](economy/construction_times.md) | Время постройки каждого здания с 1, 2, 5, 10 строителями и при максимуме слотов. | `compute/compute_construction_times.py` |
| [economy/builder_slots.md](economy/builder_slots.md) | Сколько крестьян одновременно могут строить здание (вычисляется обходом периметра mask с шагом `gc_BuilderDist=1.0`). | `compute/compute_builder_slots.py` |

## Тех-дерево ([`tech/`](tech/))

| Файл | Что внутри | Генератор |
|---|---|---|
| [tech/tech_tree.md](tech/tech_tree.md) | Дерево зависимостей: для каждого здания/юнита/апгрейда — список пререквизитов (`[B]` здание, `[U]` юнит, `[T]` апгрейд). Машинная версия — `../../derived/tech_tree.json`. | `compute/compute_tech_tree.py` |

## Карта ([`map/`](map/))

| Файл | Что внутри | Генератор |
|---|---|---|
| [map/lobby_settings.md](map/lobby_settings.md) | Все опции лобби с каноничными русскими названиями из локали игры (рельеф, ресурсы, время мира, лимит населения, сложность ИИ — 95 значений в 18 категориях). | `compute/compute_game_settings.py` |
| [map/map_resources.md](map/map_resources.md) | Подсчёт лесов, камней и шахт на стандартной карте Маленькая + Высокогорье + Много. Около 109 больших деревьев, 33 камня, до 12 месторождений на игрока. | `compute/compute_map_resources.py` |
| [map/starting_layout.md](map/starting_layout.md) | Стартовая раскладка: 18 крестьян в сетке 6×3 возле Городского центра, расположение `cen` / `sto` / шахт. | `compute/compute_starting_layout.py` |
| [map/map_predictions_validation.md](map/map_predictions_validation.md) | Валидация модели `compute_map_resources` против реплейного ground truth (10 однородных реплеев Маленькая + Суша + Высокогорье). | `compute/validate_map_predictions.py` |

## Нации ([`nations/`](nations/))

| Файл | Что внутри | Генератор |
|---|---|---|
| [nations/overview.md](nations/overview.md) | Side-by-side сравнение всех 21 нации: размер ростера, доступ к 18 в., уникальные юниты, стат-аномалии, наёмники, рыночный кластер. | `compute/compute_nations_overview.py` |
| [nations/deviations.md](nations/deviations.md) | Полные стат-отпечатки общих зданий (`<nat>cen`, `<nat>aca`, `<nat>art` и т. д.) и общих юнитов: какие нации отклоняются от базового варианта и в чём именно. Дополняет overview.md по детализации. | `compute/compute_nation_deviations.py` |

## Связанные данные

- [`../reference/`](../reference/README.md) — каноническая справка (главы 01–07, `nations/`, `compare/`). Отчёты выше построены поверх неё.
- [`../recon/`](../recon/README.md) — глубокие исследования механик, на которые эти отчёты опираются.
- [`../../derived/`](../../derived/) — машинно-читаемые JSON-датасеты (`tech_tree.json`, `builder_slots.json`, `pattern_*.json`, `animations.json`).

## Регенерация

После обновления `data.json`:

```bash
python compute/compute_combat_stats.py        # → reports/combat/combat_stats.md
python compute/compute_counter_matrix.py      # → reports/combat/counter_matrix.md
python compute/compute_attack_rates.py        # → reports/combat/attack_rates.md
python compute/compute_vision.py              # → reports/combat/vision_radii.md
python compute/compute_artillery.py           # → reports/combat/artillery.md
python compute/compute_scaling.py             # → reports/economy/scaling_prices.md
python compute/compute_efficiency_upgrades.py # → reports/economy/efficiency_upgrades.md
python compute/compute_builder_slots.py       # → reports/economy/builder_slots.md (+derived/builder_slots.json)
python compute/compute_construction_times.py  # → reports/economy/construction_times.md
python parser/build_tech_graph.py             # → derived/tech_tree.json
python compute/compute_tech_tree.py           # → reports/tech/tech_tree.md, reports/economy/production_rates.md
python compute/compute_game_settings.py        # → reports/map/lobby_settings.md (+derived/game_settings.json)
python compute/compute_map_resources.py        # → reports/map/map_resources.md
python compute/compute_starting_layout.py     # → reports/map/starting_layout.md
python compute/validate_map_predictions.py     # → reports/map/map_predictions_validation.md
python compute/compute_nations_overview.py     # → reports/nations/overview.md
python compute/compute_nation_deviations.py    # → reports/nations/deviations.md
```
