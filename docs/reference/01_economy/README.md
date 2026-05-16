# 01. Экономика

[← Index](README.md)

> **Глубокие исследования по этой главе:**
>
> - [`../recon/world/economy/peasant_extraction.md`](../recon/world/economy/peasant_extraction.md) — полный разбор цикла крестьянина, animation frames, walk speed, fieldlife регенерация, формулы и открытые empirical-вопросы (см. §9)
> - [`../recon/world/map/map_generation_pipeline.md`](../recon/world/map/map_generation_pipeline.md) — что появляется на карте (леса, камни, шахты) и где именно
> - [`../reports/map/map_resources.md`](../reports/map/map_resources.md) — подсчёт ресурсов на стандартной карте Tiny + Highlands + Rich (~109 больших деревьев, ~33 камня, до 12 шахт / игрок)

## Резюме

Один крестьянин за рейс приносит `delivered = (portion × eff) / 100`. `eff` стартует со 100, апгрейды накапливаются аддитивно. Шахты работают по другой схеме: каждый крестьянин внутри добавляет 13 к `gPlayer.counter.resincome`, реальная скорость — 1.664 ресурса в игровую секунду.

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

Все опции лобби (стартовые ресурсы, время мира, лимит населения, переход в 18 век, сложность ИИ и т. д.) — таблицы в [`docs/reports/map/lobby_settings.md`](../reports/map/lobby_settings.md), поведение движка — в [`docs/recon/world/map/game_settings.md`](../recon/world/map/game_settings.md).

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

Все апгрейды efficiency применяются в одной ветке `_player_ApplyUpgrade` [^1]; их полный список — в [05_upgrades/README.md](05_upgrades/README.md#economy-eff).

## Источники

[^1]: применение `gc_upg_type_effect*perc` к `resefficiency[res]` — `lib/player.script:1813-1828`.

## Шахты (gold/iron/coal)

Шахта: HP = 2500, `buildtime` = 300 кадров = 9.38 g-сек, цена W100 / S100, `peasantabsorber = 5` (5 крестьян макс. база). Каждый крестьянин внутри добавляет к `produce[restype]` 13.

**Расчёт:**

```
bank_per_sec = 13 × 32 = 416   # на крестьянина в игровую секунду
real_per_sec = 416 / 250 ≈ 1.664   # ресурса в игровую секунду
real_per_min = 99.84            # ≈ 100 ресурса в игровую минуту на крестьянина
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

**Итого:** 5 базовых + 6 апгрейдов = **95 крестьян/шахта = 158.1 ресурса в g-сек = 9485 в g-мин**.

**Стоимость полной прокачки одной шахты:** F104,550 + G80,950.

## Поле (food, fieldlife, регенерация)

HP поля = `gc_FieldMaxHP = 25000`. Урон полю за удар: `resdec = max(1, floor(100 / (1 + fieldlife / 100)))`.

| fieldlife | resdec/удар | Макс. ударов | Макс. food при eff=100 |
|---:|---:|---:|---:|
| 0 | 100 | 250 | 511 |
| 100 | 50 | 500 | 1022 |
| 200 | 33 | 757 | 1548 |
| 300 | 25 | 1000 | 2045 |
| 500 | 16 | 1562 | 3195 |

Апгрейды fieldlife: `aca.4` (+200), `bla.1` (+100). Сумма = 300 → ~2045 food / поле.

## Корабли — fishing

`fishboat`: HP = 300, цена W600, `fishingmax = 1000` (база), `fishingspeed = 50/4 = 12` тиков на одну рыбу. Апгрейд `aca.5` (`+100% boat efficiency`) удваивает грузоподъёмность → **2000 food / рейс**. Апгрейд `aca.7` (`-85% fishing boat cost`) удешевляет постройку.

Полный список кораблей — в [compare/units/ships.md](compare/units/ships.md).

## Голод и бунт — таблицы upkeep

> **Полный разбор механики:** [`../recon/world/economy/hunger_and_rebellion.md`](../recon/world/economy/hunger_and_rebellion.md) (RNG-пороги по сложности, виртуальный игрок-наёмник, защитные стратегии). Дипломатический центр и наёмники как **система** — [`../recon/systems/mercenaries_diplomacy.md`](../recon/systems/mercenaries_diplomacy.md).

### Расход food / g-сек на одного юнита

Формула: `food_per_g_sec = (consume.food + 30) × 32 / 20000`, если
`bnohungry = False`. Константа `gc_obj_foodperunit = 30` —
дополнительная порция к каждому едящему юниту.

| Юнит | `consume.food` | + 30 | итого | food / g-сек |
|---|---:|---:|---:|---:|
| peasant (aus / pol / spa / eng / ukr / sco) | 32 | +30 | 62 | 0.0992 |
| peasant `peatur` / `peaalg` | 28 | +30 | 58 | 0.0928 |
| peasant `pearus` | 26 | +30 | 56 | 0.0896 |
| infantry без явного `consume.food` | 0 | +30 | 30 | 0.0480 |

**Sanity-check (verified empirically 2026-04-29):** 18 австрийских крестьян простаивают 2 игровые минуты:
`sum = 18 × 62 = 1116` → `1116 × 32 / 20000 = 1.786 food/g-сек` → **за 120 g-сек ≈ 214 food** ✓

Точное значение `bnohungry` для каждого юнита — в [`../data.json`](../../data.json), поле `bnohungry`. Кратко: здания и наёмники (`bmercenary = True`) — `True`; крестьяне, обычная пехота / кавалерия, офицеры / барабанщики / священники — `False`.

### Дипломатический центр

Здание середины игры, требует **Академию** + Городской центр.

| Дип-центр | Нации | HP | Wood | Stone | Gold |
| --- | --- | ---: | ---: | ---: | ---: |
| **Дипломатический центр** `ausdip` (default) | aus, fra, eng, spa, pol … (+12) | 4500 | 4900 | 1700 | 0 |
| **Дипломатический центр** `rusdip` (rus) | rus | 6500 | 7900 | 3700 | 0 |
| **Дипломатический центр** `ukrdip` (ukr) | ukr | 5000 | 3900 | 2700 | 0 |
| **Дипломатический центр** `turdip` (tur / alg) | tur, alg | 5500 | 4600 | 2020 | 0 |

Для всех: `buildtime = 1000` кадров = **312.5 g-сек**, `costpercent = 100`, `bcapture = False`. По локализации — «можно построить только один Дипломатический центр на игрока» (ограничение GUI, не `costpercent`).

### Каталог наёмников

8 sid, ростер одинаков для **всех 21 нации**. Цена и upkeep в gold; `bnohungry = True` (food не потребляют).

| Наёмник | HP | bt, g-сек | gold (цена) | gold/тик upkeep | costpercent | Оружие |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| **Легкий пехотинец (наемник)** `lightinfantrydip` | 50 | 1.25 | **4** | 4 | 100 | sword 16 |
| **Рундашир (наемник)** `roundshierdip` | 75 | 1.5 | **12** | 20 | 100 | sword 6 |
| **Лучник (наемник)** `archerdip` | 20 | 1.25 | **15** | 16 | 100.5 | arrow 25 (range 13.13 t) / firearrow 100 (range 14.06 t) |
| **Турецкий лучник (наемник)** `archerturdip` | 20 | 1.25 | **15** | 16 | 100.5 | arrow 25 (range 13.13 t) / firearrow 100 (range 14.06 t) |
| **Гренадер (наемник)** `grenadierdip` | 30 | 1.5 | **25** | 60 | 100.5 | pike 30 / bullet 16 (range 15.0 t) / mortarball 200 (range 7.5 t) |
| **Сечевой козак (наемник)** `cossacksichdip` | 150 | 2.5 | **60** | 150 | 100.5 | sword 8 |
| **Драгун 18в. (наемник)** `dragoon18dip` | 100 | 2.0 | **120** | 120 | 102 | bullet 18 (range 15.0 t) |
| **Легкий кавалерист (наемник)** `lightcavalrydip` | 100 | 2.0 | **120** | 120 | 102 | bullet 18 (range 15.0 t) |

Формула gold-upkeep — та же, что у food: `Σ(consume.gold) × 32 / 20000`. Например, 50 `dragoon18dip` → `50 × 120 × 0.0016 = 9.6 gold/g-сек ≈ 576 gold/g-мин`.

**Масштабирование цены:** общее правило `cost(N) = floor(base × (costpercent/100)^(N−1))`, но потолок для наёмников — **2×** (вместо 20000× у обычных юнитов). Парные счётчики:
- `archerdip` ↔ `archerturdip` — общий счётчик в расчёте цены.
- `dragoon18dip` ↔ `lightcavalrydip` — аналогично.

**Карточный режим `marketdip = expensivemercs`** включает `gc_gameplay_expensivemercskoef = 3` — наёмники втрое дороже в gold.

### Расход gold юнитами

`consume[gold]` встречается у:
- **Башен** (`consume[gold] = 500` → 0.8 gold / g-sec ≈ 48 за g-minуту) — постоянный налог независимо от боя. См. [`../recon/world/combat/towers.md` §2](../recon/world/combat/towers.md).
- **Наёмников** через `consume.gold` — постоянный upkeep всех 8 sid.
- **Стрелковых юнитов** — только за выстрел через `weapon.cost[gold]`, не в простое.

Обычные пикинёры и мушкетёры gold в простое **не потребляют**.

## Sanity

Sanity checks: **112/112** PASS. См. xlsx → лист `Sanity_checks`.
