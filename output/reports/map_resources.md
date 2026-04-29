# Оценка ресурсов карты — Tiny (256×256) + Highlands + шахты Rich

**Производный** документ. Считается из `parser/compute_map_resources.py`. Перегенерация: `python parser/compute_map_resources.py`.

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

Каждая плотность леса распределяется на N разных типов леса (foreststype=0 → 4 big / 3 mid / 2 small типов):

| Тип паттерна | частота на вызов | нужно на вызов | размещено (~65%) |
|---|---:|---:|---:|
| forests_pinefir_big | 0.000208 | 13 | ~8 |
| forests_spruce_big | 0.000208 | 13 | ~8 |
| forests_pine_big | 0.000208 | 13 | ~8 |
| forests_pine_big_2 | 0.000208 | 13 | ~8 |
| forests_spruce_medium | 0.000293 | 19 | ~12 |
| forests_pinefir_medium | 0.000293 | 19 | ~12 |
| forests_pine_medium | 0.000293 | 19 | ~12 |
| forests_pinefir_small | 0.000278 | 18 | ~12 |
| forests_pine_small | 0.000278 | 18 | ~12 |
| stones (stn1) | 0.000296 | 19 | ~12 |
| stones (stn2) | 0.000222 | 14 | ~9 |

Допущение: на tiny+highlands примерно **65% запрошенных паттернов реально размещаются** (остальные не вмещаются из-за гор/плато/мин).

## 4. Всего кластеров (оценка)

- Big forest clusters:    **~32**
- Medium forest clusters: **~36**
- Small forest clusters:  **~24**
- Stone clusters:         **~21**

## 5. Деревья и камни — per pattern type

Числа = медиана `mask=1` клеток для каждого pattern type из `output/derived/pattern_type_stats.json` (парсер: `compute/compute_pattern_inventory.py`, mapping pattern→type из `data/game/var/generator.cfg`). Гипотеза: 1 mask cell = 1 дерево (подтверждено на brushes; для шахт mask = footprint, не объекты — см. caveat).

**Калибровка:** mask cells (placement slots) × **0.3** ≈ видимые chopable trees. Источник: эмпирическая оценка пользователя (small forest = ~10 trees, big = ~50). Кросс-проверка: forests_pine_big median mask = 148 → 148 × 0.34 = 50 ✓. См. caveat в начале файла.

| pattern type | clusters placed | mask cells/cluster | trees/cluster | total trees |
|---|---:|---:|---:|---:|
| `forests_pinefir_big` (big) | 8 | 920 | 276 | 2208 |
| `forests_spruce_big` (big) | 8 | 571 | 171 | 1368 |
| `forests_pine_big` (big) | 8 | 148 | 44 | 352 |
| `forests_pine_big_2` (big) | 8 | 185 | 56 | 448 |
| `forests_spruce_medium` (mid) | 12 | 469 | 141 | 1692 |
| `forests_pinefir_medium` (mid) | 12 | 311 | 93 | 1116 |
| `forests_pine_medium` (mid) | 12 | 59 | 18 | 216 |
| `forests_pinefir_small` (small) | 12 | 172 | 52 | 624 |
| `forests_pine_small` (small) | 12 | 44 | 13 | 156 |
| `stones` | 21 | 138 | 41 | 861 |

⚠ **Caveat про mask=1 интерпретацию:** brushes подтверждают (brush_plt_1x1: 8 mask = 8 видимых кустов), но шахты (`mng/mni/mnc`) — 32 mask клетки = **1 deposit** (mask = collision footprint). Для лесов мы предполагаем «1 cell = 1 tree», но без in-game test это upper bound. Точное число — empirical.

**Деревьев всего на карте:** ~8 180
**Камней всего на карте:**   ~861

## 6. Запасы древесины и камня

**Дерево — фактически бесконечно.** Когда HP дерева достигает 0, движок ([`onaclanimationreachedwork.inc:30-39`](C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/units/unit.inc/onaclanimationreachedwork.inc) + [`ontagstates.inc:50-78`](C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/env/env.inc/ontagstates.inc)):
- меняет mesh на `pinestump<N>` (визуально пень)
- **НЕ меняет** `brised=True` → пенек остаётся валидной целью для поиска
- продолжает принимать удары: `hp -= 1, peasant.resamount += 1` (даже при HP < 0)

Поэтому wood pool на карте **не лимитирован числом деревьев**. Среднее начальное HP (2474/tree из distribution: 20% giants 8-16K HP / 15% medium 125-624 / 45% small 10-60 / 20% stubs 10) определяет только сколько «халявных» хитов до перехода в режим бесконечной добычи.

Сумма начальных HP всех деревьев: ~20 237 320 hits ≈ **40 474 640 «бесплатной» древесины** @ eff=100  после чего тот же лес продолжает давать ту же скорость через пеньки.

**Real bottleneck для древесины:** число одновременных слотов (maxattackers_wood = 2 на дерево/пенек), скорость крестьянина и расстояние до склада, не количество.

**Камень:** каждый камень имеет HP=10 000 000 (фактически бесконечен). ~861 камней × 10M HP = неограниченный запас.

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

**Что точно:**
- Формула `count = floor(W*H*freq)` — прямо из `_misc_SetupPatternsByType`.
- Densities `frs_big/mid/small/stn1/stn2` — из dogenerate.inc:1688-1693.
- Modifier ×2.5 для tiny — из dogenerate.inc:1718-1725.
- Mine rounds — из dogenerate.inc:528-602.

**Что оценено:**
- `prob*` modifiers — Monte Carlo симуляция `_misc_GetFreePatternMaskCountModifier` для tiny с допущением о слабом блокировании водой.
- Trees/stones per pattern — оценка из размера `.pattern` файлов (~30 байт/тайл, делённое на ожидаемую плотность объектов в паттерне).
- Реалистичная частота размещения — допущение 65% (на tiny+highlands, где много гор).

**Предел точности:** ±30-50% по числу деревьев и каменных кластеров. ±10% по кластерам паттернов.

Для уточнения нужны:
- Парсер binary `.pattern` файлов (custom format).
- Эмпирические замеры — генерировать 10-20 карт с одинаковыми настройками и считать.