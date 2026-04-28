# 01. Экономика

[← Index](README.md)

> **Глубокие исследования по этой главе:**
> - [`../../recon/peasant_extraction.md`](../../recon/peasant_extraction.md) — полный разбор цикла крестьянина, animation frames, walk speed, fieldlife регенерация
> - [`../../recon/extraction_formulas.md`](../../recon/extraction_formulas.md) — формульная сводка для расчётов (game-time vs real-time)
> - [`derived/map_resources.md`](derived/map_resources.md) — подсчёт ресурсов на карте Tiny+Highlands+Rich (~109 больших деревьев, ~33 камня, до 12 шахт/игрок)
> - [`../../recon/empirical_tests.md`](../../recon/empirical_tests.md) — открытые вопросы для эмпирической проверки (скорость крестьянина, frame rate)


## Резюме

Один крестьянин за рейс приносит `delivered = (portion × eff) / 100`. Eff стартует со 100, апгрейды накапливаются аддитивно. Шахты работают по другой схеме: каждый крестьянин внутри добавляет 13 к `gPlayer.counter.resincome`, реальная скорость = 1.664 ресурса/игр-сек.

## Глобальные константы

| Параметр | Значение | Источник |
|---|---:|---|
| `gc_time_to_frames` | 32 | dmscript.global:175 |
| `gc_pixels_to_tile` | 53.3333 | dmscript.global:172 |
| `gc_settings_gamespeed_0` (slow) | 7 тиков/сек | dmscript.global:1027 |
| `gc_settings_gamespeed_1` (normal) | 10 | dmscript.global:1028 |
| `gc_settings_gamespeed_2` (fast) | 14 | dmscript.global:1029 |
| `gc_MaxObjCount` | 32000 | dmscript.global:110 |
| `gc_MaxPlayerCount` | 12 | dmscript.global:97 |
| `gc_FieldMaxHP` | 25000 | dmscript.global:128 |
| `gc_obj_foodperunit` | 30 food / юнит | dmscript.global:808 |
| Default `eff` | 100% | player.script:109 |

## Базовые порции и hits

| Ресурс | Базовая порция | Hits | Источник |
|---|---:|---:|---|
| food | **45** | 22 | dmscript.global:799,804 |
| wood | **28** | 14 | dmscript.global:800,805 |
| stone | **40** | 20 | dmscript.global:801,806 |
| gold/iron/coal/прочее | **20** | n/a | unit.script:9551 (хардкод) |

## Формула добычи

```
delivered = (base_portion × eff) / 100   # integer division
```
Пример: с апгрейдами academy.1 (+40% food) и mill.1 (+140% food) → `eff = 100 + 40 + 140 = 280`. Крестьянин приносит `45 × 280 / 100 = 126` еды за рейс (вместо базовых 45).

Все апгрейды eff — в `player.script:1813-1828`. Список → [05_upgrades.md](05_upgrades.md#economy-eff).

## Шахты (gold/iron/coal)

Шахта: HP=2500, buildtime=300 frames=9.38s, цена W100/S100, `peasantabsorber=5` (5 крестьян макс. база). Каждый крестьянин внутри добавляет к `produce[restype] = 13`.

**Расчёт:**

```
bank_per_sec = 13 × 32 = 416  # (per peasant per game-sec)
real_per_sec = 416 / 250 ≈ 1.664  # ресурса в игр-секунду
real_per_min = 99.84  # ≈ 100 ресурса/игр-мин/крестьянин
```
**Полная прокачка одной шахты** (6 апгрейдов):

| Уровень | +работников | F | G | Накопительно |
|---:|---:|---:|---:|---:|
| eurgol.1 | +5 | 1000 | 1250 | 10 |
| eurgol.2 | +8 | 5250 | 4950 | 18 |
| eurgol.3 | +10 | 12500 | 9250 | 28 |
| eurgol.4 | +12 | 15800 | 18500 | 40 |
| eurgol.5 | +15 | 19800 | 21050 | 55 |
| eurgol.6 | +40 | 50200 | 25950 | 95 |

**Итого:** 5 базовых + 6 апгрейдов = **95 крестьян/шахта = 158.1 ресурса/игр-сек = 9485 / игр-мин**.

**Стоимость полной прокачки одной шахты:** F104,550 + G80,950.

## Поле (food, fieldlife, регенерация)

HP поля = `gc_FieldMaxHP = 25000`. Урон полю за удар: `resdec = max(1, floor(100/(1+fieldlife/100)))`.

| fieldlife | resdec/удар | Макс. ударов | Макс. food при eff=100 |
|---:|---:|---:|---:|
| 0 | 100 | 250 | 511 |
| 100 | 50 | 500 | 1022 |
| 200 | 33 | 757 | 1548 |
| 300 | 25 | 1000 | 2045 |
| 500 | 16 | 1562 | 3195 |

Апгрейды fieldlife: `aca.4` (+200), `bla.1` (+100). Сумма = 300 → ~2045 food/поле.

## Корабли — fishing

`fishboat`: HP=300, цена W600, `fishingmax=1000` (база), `fishingspeed = 50/4 = 12` тиков на одну рыбу. Апгрейд `aca.5` (`+100% boat efficiency`) удваивает грузоподъёмность → **2000 food/рейс**. Апгрейд `aca.7` (`-85% fishing boat cost`) удешевляет постройку.

Полный список кораблей → [compare/ships.md](compare/ships.md).

## Famine (голод) и Rebellion (восстание)

Источник: [`unit.inc/nothing.inc:445-505`](file:///C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/units/unit.inc/nothing.inc), [`player.script:280-322`](file:///C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/player.script)

**Upkeep:** все юниты без флага `bnohungry` потребляют food. Скорость потребления:

```
food_per_g_sec = consume × time_to_frames / 20000
                = consume × 32 / 20000  =  consume × 0.0016
```
Для типичного юнита `consume=30` (food per unit, `gc_obj_foodperunit=30`): **0.048 food/игр-сек = 2.88 food/игр-мин на юнит**.

**Famine flag** (`bfamine=True`): срабатывает когда `food=0` И есть consume>0.

При famine **юниты без `bnohungry` начинают умирать рандомно**. Шанс смерти за тик зависит от **сложности игрока** (`gPlayer.difficulty`):

| Difficulty | Шанс смерти за тик | Ожидаемое время до смерти 1 юнита |
|---|---:|---|
| 0 (easy) | `RandomInt < 5` ≈ 0.0076% | очень медленно (часы) |
| 1 (normal) | `RandomInt < 12` ≈ 0.018% | ~часы |
| 2+ (hard / very hard / impossible) | **`RandomInt < 50` ≈ 0.076%** | **минуты** (4-10× быстрее normal) |

**Кто иммунен к famine** (`bnohungry=True`):
- Все здания (`bbuilding=True`)
- Все наёмники (`bmercenary=True`) — у них свой триггер (см. Rebellion)
- Большинство peasant'ов (но НЕ все — `peatur` не имеет bnohungry)
- Корабли
- Officers / drummers / priests

**Famine также отключается** если игрок не задал в профиле `gProfile.bFamine=True` (опция).

---

**Rebellion flag** (`brebellion=True`): срабатывает когда `gold=0` И `consume[gold] > income[gold]`.

При rebellion **наёмники массово переходят на сторону нейтрала**:

| Difficulty | Шанс перехода за тик |
|---|---:|
| 0 (easy) | `RandomInt < 100` ≈ 0.15% |
| 1 (normal) | `RandomInt < 200` ≈ 0.3% |
| 2+ (hard+) | **`RandomInt < 6000` ≈ 9.2%** — буквально за секунды теряешь весь наёмный контингент |

**Стратегические выводы:**
- На **hard и выше** keeping food и gold > 0 — критически важно. Даже короткий простой = массовая смерть/дезертирство.
- На easy famine практически бутафория, можно играть без mill optimization.
- **Наёмники (`<unit>dip` суффикс) тратят gold упкип** — поэтому держать большую diplomatic армию = высокий gold income required.

---

**Гольд upkeep юнитов** (`consume[gold]`): в основном у стрелковых башен (port, tower) и наёмников. Стандартный pikeman/musketeer **gold НЕ потребляет** (только при стрельбе — weapon.cost[gold]).

## Discrepancies (расхождения с промпт-заметками)

| Факт | Заметки | В файле | Источник | Вердикт |
|---|---|---|---|---|
| hits_needed for food | 30 | **22** | dmscript.global:799 gc_resource_hitsneeded_food | Файл: 22, не 30. Доверяем файлу — крестьянин делает 22 удара мотыгой до возврата к складу, не 30. Это укорачивает рейс и повышает фактический rate. |
| Field melioration (academy aca.4) cost | W1400 / G522 | **W1000 / G475 (any nation)** | country.script:3490 _country_AddUpgrade('aca.4', ..., wood=1000, gold=475) | Файл: W1000/G475. Расхождение с промпт-заметками — возможно, цифры из старой версии игры. Все 21 нация имеют одинаковую стоимость. |
| 'Manufacture agricultural equipment' (blacksmith) cost | W400 / G100 | **не найден в blacksmith — этот апгрейд может быть из старого названия** | country.script — нет blacksmith-апгрейда с такими параметрами | Текущий blacksmith содержит per-unit damage/protection апгрейды. Возможно, в C1 был отдельный agricultural-equipment апгрейд, который в C3 переименован в `aca.X` (academy). См. лист Upgrades с place=aca. |

## Sanity

Sanity checks: **112/112** PASS. См. xlsx → лист `Sanity_checks`.
