# Оценка ресурсов карты — Tiny (256×256) + Highlands + шахты Rich

**Производный** документ. Считается из `compute/compute_map_resources.py`. Перегенерация: `python compute/compute_map_resources.py`.

Per-type placement rates **эмпирически откалиброваны** на 10 sample replays (Tiny+Land+Highlands+4pl_nowater bucket, ratios 0.96-1.04). Pipeline: `compute/compute_replay_aggregates.py` → `compute/validate_map_predictions.py`. См. также [recon/map_generation_pipeline.md §14](../recon/map_generation_pipeline.md).

**Настройки:** mapsize=3 (Tiny, 256×256 = 65536 tiles), relief=3 (Highlands), resourcemines=2 (Rich), foreststype=0.

## 1. Модификаторы вероятности паттернов (оценка)

Симуляция `_misc_GetFreePatternMaskCountModifier` на 256×256 с ~2% воды (Land terrain — почти открытое поле):

| testsize | calibration | raw_count (sim) | prob_raw | × modifier (2.5) |
|---:|---:|---:|---:|---:|
| 12 | 340 | 252 | 0.741 | **1.853** |
| 16 | 182 | 142 | 0.780 | **1.951** |
| 24 | 74 | 61 | 0.824 | **2.061** |
| 29 | 55 | 40 | 0.727 | **1.818** |

⚠ Симуляция допускает, что вода — один смежный блок, а не разрозненные пиксели.

## 2. Плотности после умножения на вероятность

| Var | base | × prob | final density | needed = floor(area × density) |
|---|---:|---:|---:|---:|
| frs_big   | 0.000900 | × probsmall = 1.853 | 0.001668 | 109 |
| frs_mid   | 0.000900 | × probmid = 1.951     | 0.001755 | 115 |
| frs_small | 0.000540 | × problarge = 2.061 | 0.001113 | 72 |
| stn1      | 0.000160 | × probsmall = 1.853     | 0.000296 | 19 |
| stn2      | 0.000120 | × probsmall = 1.853     | 0.000222 | 14 |

## 3. Запросы паттернов (на вызов)

Каждая плотность леса распределяется на N разных типов леса (foreststype=0 → 4 big / 3 mid / 2 small типов). Колонка **placement rate** — empirically calibrated per-type (на homogeneous Tiny+Land+Highlands bucket); для unknown types — fallback default `placement_success`.

| Тип паттерна | частота на вызов | нужно на вызов | placement rate | размещено |
|---|---:|---:|---:|---:|
| `forests_pinefir_big` | 0.000208 | 13 | 0.07 | ~1 |
| `forests_spruce_big` | 0.000208 | 13 | 0.20 | ~3 |
| `forests_pine_big` | 0.000208 | 13 | 0.81 | ~11 |
| `forests_pine_big_2` | 0.000208 | 13 | 0.74 | ~10 |
| `forests_spruce_medium` | 0.000293 | 19 | 0.04 | ~1 |
| `forests_pinefir_medium` | 0.000293 | 19 | 0.09 | ~2 |
| `forests_pine_medium` | 0.000293 | 19 | 0.76 | ~14 |
| `forests_pinefir_small` | 0.000278 | 18 | 0.03 | ~1 |
| `forests_pine_small` | 0.000278 | 18 | 0.64 | ~12 |
| `stones` (stn1) | 0.000296 | 19 | 0.58 | ~11 |
| `stones` (stn2) | 0.000222 | 14 | 0.58 | ~8 |

**Откуда взяты placement rates:** эмпирически из 10 replay-выборок (Tiny+Land+Highlands+4pl_nowater bucket). Размер pattern footprint (mask cells) — главный фактор: pine_big mask=148 → ~80% placement; pinefir_big mask=920 → ~7%. Методика и полная таблица — `recon/map_generation_pipeline.md` §14. Для не-Tiny / не-Highlands settings числа должны отличаться — calibration не экстраполирована.

## 4. Всего кластеров (оценка)

- Big forest clusters:    **~25**
- Medium forest clusters: **~17**
- Small forest clusters:  **~13**
- Stone clusters:         **~19**

## 5. Деревья и камни — per pattern type

Числа = медиана `mask=1` клеток для каждого pattern type из `docs/derived/pattern_type_stats.json` (парсер: `compute/compute_pattern_inventory.py`, mapping pattern→type из `data/game/var/generator.cfg`). Гипотеза: 1 mask cell = 1 дерево (подтверждено на brushes; для шахт mask = footprint, не объекты — см. caveat).

**Калибровка:** mask cells (placement slots) × **0.3** ≈ видимые chopable trees. Источник: эмпирическая оценка пользователя (small forest = ~10 trees, big = ~50). Кросс-проверка: forests_pine_big median mask = 148 → 148 × 0.34 = 50 ✓. См. caveat в начале файла.

| pattern type | clusters placed | mask cells/cluster | trees/cluster | total trees |
|---|---:|---:|---:|---:|
| `forests_pinefir_big` (big) | 1 | 920 | 276 | 276 |
| `forests_spruce_big` (big) | 3 | 571 | 171 | 513 |
| `forests_pine_big` (big) | 11 | 148 | 44 | 484 |
| `forests_pine_big_2` (big) | 10 | 185 | 56 | 560 |
| `forests_spruce_medium` (mid) | 1 | 469 | 141 | 141 |
| `forests_pinefir_medium` (mid) | 2 | 311 | 93 | 186 |
| `forests_pine_medium` (mid) | 14 | 59 | 18 | 252 |
| `forests_pinefir_small` (small) | 1 | 172 | 52 | 52 |
| `forests_pine_small` (small) | 12 | 44 | 13 | 156 |
| `stones` | 19 | 138 | 41 | 779 |

⚠ **Caveat про mask=1 интерпретацию:** brushes подтверждают (brush_plt_1x1: 8 mask = 8 видимых кустов), но шахты (`mng/mni/mnc`) — 32 mask клетки = **1 deposit** (mask = collision footprint). Для лесов мы предполагаем «1 cell = 1 tree», но без in-game test это upper bound. Точное число — empirical.

**Деревьев всего на карте:** ~2 620
**Камней всего на карте:**   ~779

## 6. Запасы древесины и камня

**Дерево — фактически бесконечно.** Когда HP дерева достигает 0, движок ([`onaclanimationreachedwork.inc:30-39`](C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/units/unit.inc/onaclanimationreachedwork.inc) + [`ontagstates.inc:50-78`](C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/env/env.inc/ontagstates.inc)):
- меняет mesh на `pinestump<N>` (визуально пень)
- **НЕ меняет** `brised=True` → пенек остаётся валидной целью для поиска
- продолжает принимать удары: `hp -= 1, peasant.resamount += 1` (даже при HP < 0)

Поэтому wood pool на карте **не лимитирован числом деревьев**. Среднее начальное HP (2474/tree из distribution: 20% giants 8-16K HP / 15% medium 125-624 / 45% small 10-60 / 20% stubs 10) определяет только сколько «халявных» хитов до перехода в режим бесконечной добычи.

Сумма начальных HP всех деревьев: ~6 481 880 hits ≈ **12 963 760 «бесплатной» древесины** @ eff=100  после чего тот же лес продолжает давать ту же скорость через пеньки.

**Real bottleneck для древесины:** число одновременных слотов (maxattackers_wood = 2 на дерево/пенек), скорость крестьянина и расстояние до склада, не количество.

**Камень:** каждый камень имеет HP=10 000 000 (фактически бесконечен). ~779 камней × 10M HP = неограниченный запас.

## 7. Месторождения (Resources=Rich, Tiny)

**Терминология:** *месторождение* — геологическая залежь на местности (placed by `SetupMines`, basenames `minegold`/`mineiron`/`minecoal`). *Шахта* — здание `eurgol`/`euriro`/`eurcoa`, которое игрок строит на месторождении крестьянином (peasantabsorber=5, апгрейды до 95).

Параметры из [`dogenerate.inc:522-717`](C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/common.inc/dogenerate.inc#L522):
- minesdensity=2 → **5 раундов** на стартовую точку.
- На tiny раунд 4 пропускается через `continue` → **4 эффективных раундов**.
- В каждом раунде ставится по **1 месторождению каждого типа** (gold/iron/coal).
- **Итого: 4 gold + 4 iron + 4 coal = 12 месторождений на игрока** (если все попытки увенчались успехом; до 256 попыток на каждое размещение).

Дистанции от старта (mapsize>2 = tiny, gRecordGeneratorVersion ≥ 80):
- **round 0**: 14-22 тайла (Phase 1, при создании start point — 1 gold + 1 iron + 1 coal)
- **round 1**: 32-42 тайла (Phase 2)
- **round 2**: 70-82 тайла (Phase 2)
- **round 3**: 22-38 тайлов (Phase 2)
- ~~round 4~~: пропускается на tiny

## 8. Допущения и предел точности

**Что точно (из кода):**
- Формула `count = floor(W*H*freq)` — прямо из `_misc_SetupPatternsByType`.
- Densities `frs_big/mid/small/stn1/stn2` — из dogenerate.inc:1688-1693.
- Modifier ×2.5 для tiny — из dogenerate.inc:1718-1725.
- Mine rounds — из dogenerate.inc:528-602.
- Per-position mine count formula `P × (1 + n_after) + (spcount - P) × n_after`.

**Что эмпирически валидировано (replay-based, 2026-04-29):**
- Per-type placement rates — откалиброваны на 10 sample replays (Tiny+Land+Highlands+4pl_nowater bucket). Bucket ratios actual/predicted = 0.96-1.04 для всех major types (forests_pine_*, stones, mng/mni/mnc).
- Pipeline: `compute/compute_replay_aggregates.py` → `compute/validate_map_predictions.py`. Output: `docs/reports/map/map_predictions_validation.md`.
- Player count выводится из mng count для Land terrain (формула обратима).

**Что оценено / не валидировано:**
- `prob*` modifiers — Monte Carlo симуляция `_misc_GetFreePatternMaskCountModifier`. Для tiny с допущением о слабом блокировании водой (`water_blocking_pct=0.02`).
- Trees/stones per pattern — `TREE_CHOPABLE_RATIO=0.30` калибровано на эмпирической оценке пользователя (small=10 trees, big=50 trees). Не верифицировано против реального in-game tree count.
- На non-Tiny / non-Highlands settings placement rates **могут отличаться** — нет данных.

**Открытые gap'ы:**
- Pattern types `plain_*`, `mountains`, `swamp_small`, `hills_*`, `stoneforests`, `plateau*` **не предсказываются** `compute_counts` (~50% всех cluster occurrences в replay-data). Нужно расширить модель — см. recon/map_generation_pipeline.md §13 Q7.
- `desert_*` (season=3) не реализовано — 1/20 replays.
- Non-Land mine formula отличается — open question §13 Q6.

**Предел точности (Tiny+Land+Highlands):** ±5% по predicted cluster counts для covered types. По total wood pool / stones — ±30-50% (TREE_CHOPABLE_RATIO не валидирован).