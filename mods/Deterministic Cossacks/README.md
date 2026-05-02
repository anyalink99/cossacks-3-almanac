# Deterministic Cossacks — Cossacks 3 mod

Два направления изменений: **детерминизм RNG** и **anti-snowball механики боя**.

---

## На каких юнитов распространяется

**Все боевые изменения (п. 2.1–2.5) действуют только на пехоту и лошадей:**

| Тип | usage-константы |
|---|---|
| Пехота | `lightinfantry`, `grenadier`, `shooter`, `archer` |
| Лошади | `fasthorse`, `hardhorse`, `horseshooter` |

Пушки, здания, корабли, священники и все прочие юниты получают стоковое поведение во всём, что касается урона, выбора цели и пост-kill эффектов.

**Headshot +12** — дополнительно ограничен мушкетёрами и лучниками (`bCanHeadShot`, weapkind = bullet/arrow). Лошади неуязвимы как в стоке.

**Крестьяне** — только RNG-детерминизм добычи.

---

## 1. Детерминизм RNG

10 вызовов `random` в hot-path добычи и выбора цели заменены на
`SetRandomKey(seed) + random` с seed'ом из персистящегося game-state.
Один и тот же сейв при повторных загрузках → одинаковые исходы.

### Extraction (5 сайтов)

| Файл | Строка | Что |
|---|---|---|
| misc.script | 2790 | `FindResourceToExtract`: стартовый индекс в resgrid cell |
| misc.script | 2801 | `FindResourceToExtract`: wood vs stone |
| unit.script | 4055 | `SearchResourceInRadius`: standtime gate |
| unit.script | 4114 | `SearchResourceInRadius`: bskipcheck |
| unit.script | 4120 | `SearchResourceInRadius`: стартовый индекс кандидатов |

### Combat (4 сайта)

| Файл | Строка | Что |
|---|---|---|
| unit.script | 4796 | `SearchEnemyInCellShips`: rndind |
| unit.script | 4872 | `SearchEnemyInCell`: rndind |
| unit.script | 4992 | `SearchEnemyScanCellsLongRange`: dx |
| unit.script | 4993 | `SearchEnemyScanCellsLongRange`: dy |

---

## 2. Anti-snowball механики

### 2.1 Headshot (miscext2.script:420, 437)

**Stock:** 5% шанс → `+floor(uniqrnd×500)` урона (avg ~12.5, огромная дисперсия).

**Мод:** всегда срабатывает для `bCanHeadShot` → фиксированный **+12** урона.
Среднее DPS не меняется, дисперсия устранена.

**Suicidal shot (только мушкетёры, weapkind=bullet):** дополнительно 5% шанс
выстрела, который наносит **250 урона** и уничтожает самого стрелка — `hp := 1`
в момент выстрела, retarget gate убивает его в ближайшем retarget window.
Суицидальный выстрел обходит все прочие модификаторы урона.

### 2.2 Модификаторы урона (miscext2.script:437)

Применяются к каждому удару **пехоты и лошадей**, в следующем порядке:

| Условие | Эффект | Логика |
|---|---|---|
| У цели уже есть атакующие | 2-й: ×0.75 / 3-й: ×0.50 / 4-й+: ×0.30 | pile-on теряет эффективность |
| Атакующий `hp > 80% maxhp` | ×0.80 (−20%) | свежий юнит бьёт слабее |
| Атакующий `hp < 50% maxhp` | ×1.20 (+20%) | раненый юнит бьёт сильнее |
| На атакующего нападает N врагов (cap 5) | ×(1 + N×0.50), max ×3.50 | окружённый юнит бьёт сильнее |
| Атакующий `hp < 3` | урон ÷3, затем 80% шанс = 0 | умирающий наносит минимальный урон |

### 2.3 Пост-kill эффекты (miscext2.script:463)

После каждого убийства, совершённого **пехотой или лошадью**:

- **Retarget delay:** `attackdelay := max(attackdelay, 1.5 г-сек)` — юнит не ищет
  новую цель, пока delay не истечёт.
- **Fatigue:** применяется **только если убита огнестрельная единица**
  (`shooter` или `horseshooter`). Размер: пехота (`lightinfantry`, `grenadier`,
  `shooter`, `archer`) — `-15% maxhp`; лошади (`fasthorse`, `hardhorse`,
  `horseshooter`) — `-5% maxhp`. Minimum 1 hp — усталость не убивает напрямую.
- **Near-death kill:** если `hp < 3` — смерть в retarget window (см. п. 2.5).

Цепочка усталости: пехотинец (maxhp ~80) теряет 12 hp за убийство мушкетёра.
После ~6 таких убийств hp опускается до 1. При следующем убийстве
hp=1 < 3 → смерть в retarget gate.

### 2.4 Выбор цели — anti-clumping (unit.script:5127, 5191, 5194)

Применяется только когда цель ищёт **пехота или лошадь**.

Stock C3: `relativeDist := distSqr × (1 + pstolist.count × K)`, K=0.1/0.125.

**Мод:** K поднят до **0.5** для всех трёх сканов (long-range, melee, ranged).

| Атакующих на цели | Множитель видимой дистанции |
|---|---|
| 0 | ×1.0 |
| 1 | ×1.5 |
| 2 | ×2.0 |
| 3 | ×2.5 |

Дополнительно: цели с `50% > hp ≥ 3` получают ещё ×2.5 к дистанции —
юниты обходят раненых и переключаются на свежих. Умирающие (`hp < 3`)
из этого множителя исключены и остаются приоритетными.

### 2.5 Retarget gate (unit.script:8400)

Применяется только к **пехоте и лошадям**.

Пока `attackdelay > 0` — юнит не ищет новую цель (принудительный idle).
Если при этом `hp < 3` — смерть (`hp := 0` + `gc_statetag_essential_death`).

---

## Как работает anti-snowball в совокупности

Проблема stock C3: в симметричном бою первые несколько смертей создают
численный перевес → победитель получает «бесплатные» атаки по оставшимся
→ каскад. 100v100 → 0 vs 40.

Мод атакует каскад с нескольких сторон:

1. **Pile-on penalty** снижает эффективность численного перевеса при атаке.
2. **Fresh penalty** уменьшает урон от «победителей» с полным HP.
3. **Outnumbered bonus** усиливает окружённых, повышая цену окружения.
4. **Fatigue** делает «победителей» хрупкими после убийства огнестрельных.
5. **Near-death kill** выводит из строя юнитов, которые накопили усталость.
6. **Retarget delay** разрывает цепочки немедленного переключения на следующую цель.
7. **Suicidal shot** добавляет риск для мушкетёров при мощном выстреле.
8. **Anti-clumping K=0.5** мягко снижает вероятность pile-on при выборе цели.

---

## Как собрать

```bash
cd c:/projects/other/cossacks
python "mods/Deterministic Cossacks/build.py"
```

Читает оригинальные `lib/{misc,miscext2,unit}.script` из `$COSSACKS3_PATH`
(default `C:\Program Files (x86)\Steam\steamapps\common\Cossacks 3`),
применяет патчи, пишет результат в `mods/Deterministic Cossacks/build/`.

```bash
python "mods/Deterministic Cossacks/build.py" --install
```

Дополнительно копирует в `<game>/mods/` и прописывает в `mods.ini`.

### Если патч не находит строку

Если игра обновилась и строки сместились — `build.py` выдаст
`RuntimeError: original line not found` или warning `drift > 5`.
Обновить `expected_line` и `original` в `PATCHES` в `build.py`.

---

## Ограничения

- **Async pathfinding** (`PathDataThread*`) — недоступен скрипту, остаточный
  источник дисперсии.
- **`_weapon_CalcShotDispertion`** — использует `RandomExt`, stock-bug движка;
  без `SetRandomExtKey64` не патчится.
- **Adaptive game speed** — на разных компах за равное real-time проходит
  разное game-time; сравнивать исходы по g-time.

---

## Откат

- В `<game>/mods/mods.ini` поставить `dis = True`, или
- Удалить `<game>/mods/Deterministic Cossacks/`.

Оригинальные скрипты в `<game>/data/scripts/` не трогаются.

---

## Структура

```
mods/Deterministic Cossacks/
├── README.md
├── build.py           ← патчер
├── src/
│   └── mod.ini        ← metadata
└── build/             ← результат сборки (.gitignored)
    └── Deterministic Cossacks/
        ├── mod.ini
        └── data/scripts/lib/
            ├── misc.script
            ├── miscext2.script
            └── unit.script
```

## Дополнительно

- [internals/engine/script_modding_constraints.md](../../internals/engine/script_modding_constraints.md) —
  ограничения DWS-скриптинга: почему нельзя убивать атакующего изнутри
  DoDamage, двойной essential_death баг, безопасный retarget gate паттерн.
- [internals/engine/rng_implementation.md](../../internals/engine/rng_implementation.md) §3 —
  SetRandomKey vs SetRandomExtKey64.
- [docs/recon/world/economy/peasant_extraction.md](../../docs/recon/world/economy/peasant_extraction.md) —
  каталог extraction RNG-сайтов.
