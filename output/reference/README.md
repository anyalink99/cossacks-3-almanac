# Cossacks 3 Reference

_Extracted **2026-04-28 09:52:20** (local) from game files (unit.script mtime: 2026-04-28 03:32:28)._

Полный справочник по экономике, юнитам, зданиям и апгрейдам игры Cossacks 3, извлечённый напрямую из файлов игры в `C:\Program Files (x86)\Steam\steamapps\common\Cossacks 3\data\scripts\`.

Парсер: `parser/` (запусти `python parser/build_data.py && python writers/write_md_tree.py` после патча игры).

---

## TL;DR — главные цифры

- **Время:** `gc_time_to_frames = 32` (32 кадра / игр-сек). Game speeds: slow=`7`, normal=`10`, fast=`14` тиков/сек.
- **Pixels-to-tile:** `53.3333`. Радиус 800 px = 15 тайлов.
- **Лимиты:** 32000 объектов на карте, 12 игроков.
- **Поле:** HP = 25000. Шахта (база): 5 крестьян → 1.664 ресурса/игр-сек на крестьянина.

### Базовая добыча

| Ресурс | Порция за рейс | Hits перед сдачей | Real rate (1 крестьянин, eff=100) |
|---|---:|---:|---:|
| food (еда) | **45** | 22 | ≈ 2.97 / игр-сек (без дороги к складу) |
| wood | **28** | 14 | ≈ 3.56 / игр-сек |
| stone | **40** | 20 | ≈ 3.56 / игр-сек |
| gold/iron/coal | **20** (хардкод) | n/a | через шахту: 1.664 / крестьянин / игр-сек |

**Формула:** `delivered = (portion × eff) / 100`  (целочисл. деление). `eff` стартует со 100, апгрейды добавляют **аддитивно**.

### Боевая формула

```
applied = max(1, weapon.damage
                 - target.shield               # /3 if target is being built
                 - target.protection[kind]
                 + squad bonuses
                 + HEADSHOT: +floor(uniqrnd × 500) at 5% chance (arrow/bullet vs non-buildings))
```
**Минимум 1 хп**. Headshot = 5% шанс на каждый bullet/arrow выстрел против любого юнита (кроме light-cavalry-в-движении) даёт **до +499** бонусного damage. См. подробности в [02_combat.md → Headshot](02_combat.md#headshot-критический-удар--главная-скрытая-механика). Источник: `miscext2.script:_misc_DoDamage`.

### Цена N-го здания того же типа

`cost(N) = floor(base_cost × (costpercent/100)^(N-1))`. См. [derived/scaling_prices.md](derived/scaling_prices.md).

---

## Где что искать

### Главы справочника (этот каталог)

| Хочу узнать… | Открой |
|---|---|
| Формулы добычи и цикл крестьянина | [01_economy.md](01_economy.md) |
| Формула урона, защиты, скорости, формации | [02_combat.md](02_combat.md) |
| Все здания (общие + per-nation) | [03_buildings.md](03_buildings.md) |
| Все юниты по классам | [04_units.md](04_units.md) |
| Все апгрейды по местам | [05_upgrades.md](05_upgrades.md) |
| Курсы рынка и примеры обмена | [06_market.md](06_market.md) |
| Что уникального у нации X | [nations/](nations/README.md) |
| Сравнить юнитов одного класса | [compare/](compare/README.md) |

### Производные файлы (расчётные, на основе data.json)

В подкаталоге [`derived/`](derived/):

| Файл | Что внутри |
|---|---|
| [derived/scaling_prices.md](derived/scaling_prices.md) | Стоимости 2-го, 3-го, …N-го здания. Формула `cost(N) = floor(base × (costpercent/100)^(N-1))` |
| [derived/map_resources.md](derived/map_resources.md) | Подсчёт ресурсов на карте Tiny (256×256) + Highlands + Rich: ~109 больших деревьев, ~115 средних, ~72 маленьких; ~33 камня; до 12 шахт на игрока |
| [derived/efficiency_upgrades.md](derived/efficiency_upgrades.md) | Все `effect{food,wood,stone}` + `fieldlife` апгрейды на 21 нацию: пики, стоимость, прогрессия. |
| [derived/combat_stats.md](derived/combat_stats.md) | DPS / EHP / armor по всем combat-юнитам. Дедупликация по статам, ранкинг по DPS. |
| [derived/counter_matrix.md](derived/counter_matrix.md) | Матрица time-to-kill 22×22 эталонных юнитов с учётом protection. |
| [derived/starting_layout.md](derived/starting_layout.md) | Геометрия старт-точки: 18 крестьян 6×3 grid, ring distances для forest/stone/mines, 14 startingunits-presets. |

### Сырой источник

| Файл | Что |
|---|---|
| [../data.json](../data.json) | Сырой JSON (~4.7 MB) — вход для всех writer-скриптов. Регенерируется через `python parser/build_data.py`. |

### Глубокие исследования (recon/)

| Файл | Тема |
|---|---|
| [../../recon/peasant_extraction.md](../../recon/peasant_extraction.md) | Полный разбор механики добычи: цикл крестьянина, animation frames, walk speed, fieldlife регенерация, спавн ресурсов |
| [../../recon/extraction_formulas.md](../../recon/extraction_formulas.md) | Краткая формульная сводка для расчётов (game-time vs real-time, fast×1.4) |
| [../../recon/empirical_tests.md](../../recon/empirical_tests.md) | Открытые вопросы для эмпирической проверки (скорость крестьянина, animation frame rate, brised флаг для пней) |
| [../../recon/step1_findings.md](../../recon/step1_findings.md) | Исторический recon: исходное обнаружение структуры файлов игры (можно пропустить) |

## Расхождения с заметками промпта

(детали в [01_economy.md#discrepancies](01_economy.md))
| Факт | Заметки | Файл |
|---|---|---|
| hits_needed for food | 30 | **22** |
| Field melioration (academy aca.4) cost | W1400 / G522 | **W1000 / G475 (any nation)** |
| 'Manufacture agricultural equipment' (blacksmith) cost | W400 / G100 | **не найден в blacksmith — этот апгрейд может быть из старого названия** |

## Sanity checks: **112/112 PASS**

Полный список и категории — в xlsx-листе `Sanity_checks` или [01_economy.md](01_economy.md#sanity).

---

## Стат по объёмам

- **Нации:** 21
- **Здания:** 414 строк (sid×nation)
- **Юниты:** 714 строк
- **Апгрейды:** 4429 строк
- **Офицеры/формации:** 231 групп

## Принципы справочника

1. **Источник истины — файлы игры.** Если что-то расходится с внешними калькуляторами/гайдами — доверяй файлу. Расхождения задокументированы в `discrepancies`.
2. **Идемпотентность.** `python build_data.py && python write_xlsx.py && python write_md_tree.py` перегенерирует всё с нуля.
3. **Sanity checks.** 100+ автопроверок ловят регрессии после игровых патчей.
4. **Нет ручных правок.** Если хочешь подкрутить — правь скрипты в `parser/`, не сами md.