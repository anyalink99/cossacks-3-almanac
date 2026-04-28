# Cossacks 3 — Формулы добычи (производный документ)

Краткий справочник формул для подсчёта добычи. Подробный recon с источниками см. [`recon/peasant_extraction.md`](peasant_extraction.md).

**Контекст:** game speed = **fast (×1.4)**. Карта: Land + Highlands + Resources=Many + Tiny (256×256).

**Условные обозначения:**
- `t_g` = игровая секунда (game-time second, базовая единица всех скриптов)
- `t_r` = реальная секунда (real-time second). При fast: `t_r = t_g / 1.4`, или `t_g = 1.4 × t_r`.

---

## 1. Базовые константы (memorize)

| Symbol | Value | Что это |
|---|---:|---|
| `frames_per_g` | 32 | кадров в одной игровой секунде |
| `T_food` | 22 frames = 0.6875 t_g | длительность одного "удара" по полю |
| `T_wood` | 18 frames = 0.5625 t_g | длительность одного "удара" по дереву |
| `T_stone` | 18 frames = 0.5625 t_g | длительность одного "удара" по камню |
| `H_food` | 22 | hits до сдачи food |
| `H_wood` | 14 | hits до сдачи wood |
| `H_stone` | 20 | hits до сдачи stone |
| `P_food` | 45 | base portion food за рейс |
| `P_wood` | 28 | base portion wood за рейс |
| `P_stone` | 40 | base portion stone за рейс |
| `eff` | 100 default | resefficiency, увеличивается апгрейдами аддитивно |
| `gameSpeed` | ×1.4 (fast) | множитель real→game time |

---

## 2. Идеальный rate (без хождения к складу)

```
trip_yield   = floor(P_res × eff / 100)            # ресурсов за один поход
trip_time_g  = H_res × T_res                       # игровых секунд на удары
rate_g       = trip_yield / trip_time_g            # ресурсов за игровую секунду
rate_r       = rate_g × gameSpeed                  # ресурсов за реальную секунду @ fast
```

### Численно при eff=100, fieldlife=0

| Ресурс | trip_yield | trip_time_g | rate_g | rate_r @ fast |
|---|---:|---:|---:|---:|
| food | 45 | 15.125 | 2.975 | **4.165 / real-sec** |
| wood | 28 | 7.875 | 3.556 | **4.978 / real-sec** |
| stone | 40 | 11.25 | 3.556 | **4.978 / real-sec** |

Это **верхняя граница**. В реальности крестьянин ходит к складу.

---

## 3. С хождением к складу (round-trip)

```
walk_time_g = (2 × dist_tiles) / V_g               # туда+обратно
trip_time_g = H_res × T_res + walk_time_g
rate_g      = trip_yield / trip_time_g
```

`V_g` = скорость крестьянина в **тайлах за игровую секунду** (см. §6 — нужен empirical test).

### Эффект расстояния (приближение, V_g=2 tiles/g-sec, eff=100)

| dist (tiles) | walk_g | trip_g (wood) | rate wood (g-sec) | rate wood @ fast (real-sec) | от ideal |
|---:|---:|---:|---:|---:|---:|
| 0 | 0 | 7.88 | 3.56 | 4.98 | 100% |
| 2 | 2.0 | 9.88 | 2.83 | 3.97 | 80% |
| 5 | 5.0 | 12.88 | 2.17 | 3.05 | 61% |
| 10 | 10.0 | 17.88 | 1.57 | 2.19 | 44% |
| 20 | 20.0 | 27.88 | 1.00 | 1.41 | 28% |

Аналогично для food/stone (с учётом своих H, T, P).

⚠ V_g — не подтверждена. Может быть 1, 2, 3 или иное значение тайлов/g-sec. Пока не верифицировано — все цифры в этой таблице **предварительные**.

---

## 4. Шахты (gold/iron/coal)

### 4.1 Базовая ставка

Каждый крестьянин внутри шахты добавляет к доходу **13 единиц/тик resincome**. Реальная скорость:

```
rate_per_peasant_g = 13 × 32 / 250 = 1.664 ресурса / game-sec
rate_per_peasant_r = 1.664 × 1.4   = 2.330 ресурса / real-sec @ fast
```

### 4.2 По уровням апгрейда (single mine, F+G total cost)

Каждый апгрейд `+addpeasantabsorber`. Стартовая capacity = 5.

| Уровень | absorber | rate (real-sec, fast) | rate (real-min) | total cost upgrades |
|---|---:|---:|---:|---|
| base | 5 | 11.65 | 699 | — |
| `.1` | 10 | 23.30 | 1398 | F1000 G1250 |
| `.2` | 18 | 41.94 | 2516 | F6250 G6200 |
| `.3` | 28 | 65.24 | 3914 | F18750 G15450 |
| `.4` | 40 | 93.20 | 5592 | F34550 G33950 (need 18c) |
| `.5` | 55 | 128.15 | 7689 | F54350 G55000 |
| `.6` | **95** | **221.30** | **13 278** | **F104 550 G80 950** |

(Если у вас 12 шахт fully-upgraded × 3 типа ресурсов: ~13 278 × 12 = 159k/min на каждый из gold/iron/coal. Reality check.)

---

## 5. Поля (food)

### 5.1 Hit damage и hits до 0 HP

```
field_hp_max = 25 000
resdec       = max(1, floor(100 / (1 + fieldlife/100)))
hits_per_field = field_hp_max / resdec
food_per_field = floor(hits_per_field / H_food) × P_food × eff/100
```

(food_per_field здесь — округлённое вниз: каждый рейс = 22 hits → 45×eff/100 еды. Лишние hits в конце пропадают.)

| fieldlife | resdec | hits/field | trips/field | food/field @ eff=100 |
|---:|---:|---:|---:|---:|
| 0 (default) | 100 | 250 | 11 | 495 |
| 100 | 50 | 500 | 22 | 990 |
| 200 | 33 | 757 | 34 | 1530 |
| **300** (aca.4 + bla.1) | **25** | **1000** | **45** | **2025** |
| 500 | 16 | 1562 | 71 | 3195 |

### 5.2 Регенерация

- Если HP ≥ 13 000 (visual_stage_0) и HP < max: каждые **31.25 t_g** (= 22.32 real-sec @ fast) → `HP += random(0..2500)`.
- Среднее за тик: +1250 HP (random ravnomerno).
- Долгосрочный equilibrium: если крестьянин выкачивает W food/g-sec, регенерация даёт +1250 / 31.25 = 40 HP/g-sec. Если расход HP/g-sec ≤ 40 → поле бесконечно.
- При fieldlife=300: расход HP за g-sec = (1/T_food) × resdec = (1/0.6875) × 25 = 36.4 HP/g-sec ≤ 40 → **одного крестьянина поле выдерживает бесконечно при условии HP не падает <13000**.
- Без fieldlife: расход = 1.45 × 100 = 145 HP/g-sec ≫ 40 → поле вырабатывается за ~250 hits / 1.45 ≈ 172 g-sec ≈ 123 real-sec @ fast.

### 5.3 Простой при перезапуске (когда HP=0)

```
restart_time_g = 21.875 + 4 × 21.875 = 109.375 t_g  ≈ 78.1 real-sec @ fast
```

В это время крестьянин уйдёт на другое поле или будет idle.

---

## 6. Скорость крестьянина (UNRESOLVED)

`gc_obj_speed_peasant = 40` (в `gc_obj_speed_default = 32` единицах). В скриптах объявлено, но строки `objbase.speed := gc_obj_speed_peasant` **закомментированы** ([unit.script:1192](C:/Program Files (x86)/Steam/steamapps/common/Cossacks 3/data/scripts/lib/unit.script#L1192)). Глобально объявлено `objbase.speed := 1` ([unit.script:618](C:/Program Files (x86)/Steam/steamapps/common/Cossacks 3/data/scripts/lib/unit.script#L618)).

Возможные интерпретации:
- "40 пикселей в кадре" при `gc_pixels_to_tile = 53.33`: 40 × 32 / 53.33 = 24 tile/g-sec (быстро)
- "40 единиц в секунду": 40 / 53.33 = 0.75 tile/g-sec (медленно)
- "40" как абстрактный коэффициент, фактическое от actor mesh

**Рекомендуемый эмпирический тест:**
1. Game speed = **normal** (1×) для чистого замера.
2. Поставить два склада на расстоянии 10 тайлов.
3. Перевести крестьянина из одной точки в другую с пустыми руками (right-click move).
4. Засечь секундомером.
5. `V_g = 10 / time_seconds`.

Альтернативно: засечь время одного work-цикла секундомером (должен быть ≈ 0.5625 game-sec для wood) → проверить наше допущение про 32 fps анимаций.

---

## 7. Сводная формула: добыча с леса

Учёт:
- ходьба к дереву (re-acquire) пренебрежимо мала, если деревья плотные
- ходьба к складу dist_d
- средний HP дерева ≈ 2474 (см. §4.2 в recon)

```
trips_per_tree = floor(2474 / 14)               # ≈ 176 рейсов на "среднее" дерево
yield_per_tree = trips_per_tree × P_wood × eff/100   # ≈ 4928 wood @ eff=100
                                                
# rate_at_distance:
trip_time_g = H_wood × T_wood + 2 × dist_d / V_g
rate_g      = (P_wood × eff/100) / trip_time_g
```

Так как дерево даёт МНОГО hits подряд, его исчерпание не влияет на rate (просто переключение на следующее дерево добавит ~2-5 тайлов хода ≈ 1 рейс пропустить).

---

## 8. Сводная формула: добыча с поля

Учёт реален только при fieldlife=0 (без апгрейдов) — поле истощается быстро. С fieldlife=300 — почти бесконечно (см. §5.2).

```
# При fieldlife=0:
hits_to_depletion = 250
trips_to_depletion = floor(250 / 22) = 11
food_per_field    = 11 × 45 × eff/100  # 495 @ eff=100, 990 @ eff=200

cycle_time_g = trips × (H_food × T_food + walk_g) + restart_time_g
             = 11 × (15.125 + walk_g) + 109.375
                                                
food_per_g   = food_per_field / cycle_time_g
```

При dist_to_storehouse=2, V_g=2: walk_g=2, cycle_time = 11×17.125+109.4 = 297.7 g-sec, food/g-sec = 495/297.7 = **1.66**.
@ fast: **2.33 food/real-sec на одного крестьянина при отсутствии апгрейдов**.

С `fieldlife=300, eff=200`:
- 45 рейсов × 90 food = 4050 food/cycle (одного поля хватает надолго)
- Если расход HP ≤ regen → поле бесконечно, тогда rate = ideal: 2.975 × eff/100 / (1 + walk_overhead) ≈ 5-6 food/g-sec на крестьянина.

---

## 9. Что использовать для калькулятора стратегий

**Для MVP (формульный калькулятор):** §1-§5 + предположение о V_g (использовать 2 tile/g-sec пока не измерено).

**Для точного симулятора:** требуются п.п. §6 (скорость), стохастика HP деревьев, distance distributions от спавн-точки, regen полей и ходьба между несколькими складами.

**Открытые вопросы для дальнейшего recon:** см. §9 в `peasant_extraction.md`.
