# Cossacks 3 Reference

_Extracted **2026-04-29 01:48:04** (local) from game files (unit.script mtime: 2026-04-28 03:32:28)._

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
**Минимум 1 хп**. Хедшот = 5% шанс на каждый bullet/arrow выстрел против любого юнита (кроме light-cavalry-в-движении) даёт **до +499** бонусного урона. См. подробности в [02_combat.md → Хедшот](02_combat.md#хедшот-критический-удар--главная-скрытая-механика). Источник: `miscext2.script:_misc_DoDamage`.

### Цена N-го здания того же типа

`cost(N) = floor(base_cost × (costpercent/100)^(N-1))`. См. [`../reports/scaling_prices.md`](../reports/scaling_prices.md).

---

## Глоссарий: ключевые игровые теги

Это краткие пояснения к флагам и полям, которые часто встречаются в скриптах и в этом справочнике. Подробности — в файлах глав.

**Идентификаторы и общие поля:**

| Тег | Что значит |
|---|---|
| `sid` | Внутренний ID объекта в `unit.script` (например `bavcen`, `peaaus`, `aca.4`). |
| `cid` | Идентификатор нации (Country ID, 0..23). См. таблицу в [04_units.md](04_units.md). |
| `usage` / `usage_short` | Класс юнита/здания: `lightinfantry`, `fasthorse`, `building`, `tower`, и т. д. Влияет на AI и формулы. |
| `commonsid` / `cluster` | Кластер общих зданий (`eur`/`rus`/`tur`/`spa`/`ukr`/`por`). Например `eurmil` — мельница для всех eur-наций. |
| `costpercent` | Множитель цены каждого следующего экземпляра здания: `cost(N) = floor(base × (cp/100)^(N-1))`. 100 = одинаковая, 300 = ×3 за второе, 0 = без масштабирования. |
| `farm` | На сколько единиц здание поднимает лимит населения. |

**Добыча и экономика:**

| Тег | Что значит |
|---|---|
| `eff` (`resefficiency[cid][restype]`) | Текущая эффективность добычи в %. По умолчанию 100; апгрейды (mill, academy) добавляются **аддитивно**: `eff = 100 + Σ(апгрейды)`. Реальная порция = `floor(base_portion × eff / 100)`. |
| `consume.food` / `consume[gold]` | Сколько ресурса юнит/здание потребляет в тик `gPlayer.counter.resconsume[…]`. Не путать с `cost` (цена постройки/найма). |
| `peasantabsorber` | Сколько крестьян может находиться внутри здания (в шахте — до 5 базово, до 95 с апгрейдами). |
| `produce[restype]` | Сколько ресурса добавляется к `gPlayer.counter.resincome` за каждого крестьянина внутри здания (для шахт = 13). |
| `fieldlife` | Бонус прочности полей: каждый удар по полю снимает `max(1, 100/(1+fieldlife/100))` HP вместо 100. Апгрейды `aca.4` (+200) и `bla.1` (+100) дают суммарно 300 → 25 HP/удар, или ×4 еды с поля. |

**Боевые флаги:**

| Тег | Что значит |
|---|---|
| `bbuilt` | Здание полностью достроено (`True`) или ещё в стройке (`False`). При `False` входящий урон вычитает только `shield/3` вместо `shield`. |
| `bcapture` | Здание можно захватить вражеской пехотой в радиусе `gc_gameplay_captureradius=4 тайла` без своих защитников рядом. Захват мгновенный. У всех башен (`gc_obj_usage_tower`) включается автоматически. |
| `bnohungry` | Юнит/здание не потребляет food (нет голодной смерти). У всех зданий = `True`. У наёмников = `True` (но они едят gold через Rebellion). У крестьян и обычной пехоты = `False`. |
| `bmercenary` | Юнит-наёмник (`<unit>dip` суффикс). Едят gold вместо food, при `gold=0` массово переходят к нейтралу (см. Rebellion в [01_economy.md](01_economy.md)). |
| `bfamine` | Флаг голода у игрока: `food=0` И есть юниты с `consume>0`. Включает рандомную смерть юнитов с `bnohungry=False`. |
| `brebellion` | Флаг бунта у игрока: `gold=0` И `consume[gold] > income[gold]`. Включает массовый дезертир наёмников. |
| `brised` | Ресурс «активен» — крестьяне могут его добывать. Для wood остаётся `True` даже после превращения дерева в пень → бесконечный wood pool. |
| `uniqrnd` | Случайное число `[0,1)`, фиксированное у каждого юнита при спавне. Используется для воспроизводимой дисперсии (бонус хедшота, разлёт снаряда). См. [recon/determinism_audit.md](../../recon/determinism_audit.md). |
| `gc_obj_weapon_kind_*` | Тип оружия: `pike` / `sword` / `bullet` / `cannister` / `arrow` / `cannonball` / `grenade` и др. От него зависит, какая колонка `protection[kind]` цели вычитается из урона. |

**Время:**

| Тег | Что значит |
|---|---|
| `gc_time_to_frames = 32` | 32 кадра в одной игровой секунде. Все длительности в скриптах (анимации, `pause`, `buildtime` юнитов) хранятся в кадрах. |
| `gc_buildtime_modifier = 10` | Дополнительный множитель **только для зданий**: `buildtime_g_sec = frames × 10/32`. Юниты используют `frames/32`. См. [recon/building_mechanics.md](../../recon/building_mechanics.md). |
| game speed | `slow=7 / normal=10 / fast=14` тиков/сек. На fast: `1 game-sec = 1/1.4 ≈ 0.71 real-sec`. |

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

### Производные расчёты (рядом с этой папкой)

Все автоматически вычисляемые отчёты — в [`../reports/`](../reports/README.md):

- **Бой:** [`combat_stats.md`](../reports/combat_stats.md), [`counter_matrix.md`](../reports/counter_matrix.md)
- **Цены:** [`scaling_prices.md`](../reports/scaling_prices.md) — цена N-го экземпляра. [`efficiency_upgrades.md`](../reports/efficiency_upgrades.md) — что меняют апгрейды.
- **Темп:** [`tech_tree.md`](../reports/tech_tree.md), [`production_rates.md`](../reports/production_rates.md), [`construction_times.md`](../reports/construction_times.md), [`builder_slots.md`](../reports/builder_slots.md)
- **Карта:** [`map_resources.md`](../reports/map_resources.md), [`starting_layout.md`](../reports/starting_layout.md)

Машинно-читаемые JSON-датасеты — в [`../derived/`](../derived/) (`tech_tree.json`, `animations.json`, `builder_slots.json`, `pattern_*.json`).

### Сырой источник

| Файл | Что |
|---|---|
| [../data.json](../data.json) | Сырой JSON (~4.7 MB) — вход для всех writer-скриптов. Регенерируется через `python parser/build_data.py`. |

### Глубокие исследования (recon/)

| Файл | Тема |
|---|---|
| [../../recon/peasant_extraction.md](../../recon/peasant_extraction.md) | Полный разбор добычи: цикл крестьянина, animation frames, walk speed, fieldlife регенерация, спавн ресурсов |
| [../../recon/building_mechanics.md](../../recon/building_mechanics.md) | Постройка/починка крестьянами, builder slots, стены, гарнизон/башни, захват, разрушение |
| [../../recon/map_generation_pipeline.md](../../recon/map_generation_pipeline.md) | Полный таймлайн `DoGenerate` + что определяет уникальную карту (seed space) |
| [../../recon/determinism_audit.md](../../recon/determinism_audit.md) | RNG-сайты в hot-path добычи и боя, save/load, мод-фикс |
| [../../recon/ticks_and_subticks.md](../../recon/ticks_and_subticks.md) | Модель времени: progress-loop, sub-tick state, adaptive game speed |
| [../../recon/server_sync_architecture.md](../../recon/server_sync_architecture.md) | Server-authoritative модель C3, net modes, sync пакеты |

## Расхождения с заметками из промпта

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