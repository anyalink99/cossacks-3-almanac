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

{dip_buildings_table}

Для всех: `buildtime = 1000` кадров = **312.5 g-сек**, `costpercent = 100`, `bcapture = False`. По локализации — «можно построить только один Дипломатический центр на игрока» (ограничение GUI, не `costpercent`).

### Каталог наёмников

8 sid, ростер одинаков для **всех 21 нации**. Цена и upkeep в gold; `bnohungry = True` (food не потребляют).

{mercenaries_table}

Формула gold-upkeep — та же, что у food: `Σ(consume.gold) × 32 / 20000`. Например, 50 `dragoon18dip` → `50 × 120 × 0.0016 = 9.6 gold/g-сек ≈ 576 gold/g-мин`.

**Масштабирование цены:** общее правило `cost(N) = floor(base × (costpercent/100)^(N−1))`, но потолок для наёмников — **2×** (вместо 20000× у обычных юнитов). Парные счётчики:
- `archerdip` ↔ `archerturdip` — общий счётчик в расчёте цены.
- `dragoon18dip` ↔ `lightcavalrydip` — аналогично.

**Карточный режим `marketdip = expensivemercs`** включает `gc_gameplay_expensivemercskoef = 3` — наёмники втрое дороже в gold.

### Расход gold юнитами

`consume[gold]` встречается у:
- **Башен** (`consume[gold] = 500` → 0.8 gold / г-сек ≈ 48 за г-минуту) — постоянный налог независимо от боя. См. [`../recon/world/combat/towers.md` §2](../recon/world/combat/towers.md).
- **Наёмников** через `consume.gold` — постоянный upkeep всех 8 sid.
- **Стрелковых юнитов** — только за выстрел через `weapon.cost[gold]`, не в простое.

Обычные пикинёры и мушкетёры gold в простое **не потребляют**.
