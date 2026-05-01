# Deterministic Cossacks — Cossacks 3 mod

> Раньше мод назывался **Deterministic Extraction** и патчил только добычу. После добавления combat-сайтов (headshot, выбор цели) переименован — добыча больше не одна.

Заменяет 10 вызовов `random` в hot-path добычи и боя на `SetRandomKey + random` с seed'ом из персистящегося game-state. Цель: один и тот же сейв при повторных загрузках, и одно и то же состояние симуляции на разных хостах, дают одинаковую добычу леса/камня и одинаковые боевые исходы (в пределах движкового tie-breaking pathfinder'а, который скриптом не починить).

См.:
- [internals/engine/rng_implementation.md](../../internals/engine/rng_implementation.md) §3 — почему `SetRandomKey` ловит **только** Random-стрим, и почему `RandomExt` патчить нельзя без `SetRandomExtKey64`.
- [docs/recon/world/economy/peasant_extraction.md](../../docs/recon/world/economy/peasant_extraction.md) — каталог extraction RNG-сайтов.
- [internals/engine/rtti_class_map.md](../../internals/engine/rtti_class_map.md) §4 — `TPathData` / `TOSWPathNode` (остаточный non-determinism в pathfinding'е).

## История

**v1 (2026-04, broken):** патчи использовали `SetRandomKey(...) + RandomExt`. Это **не работает**: `SetRandomKey` сидит только 32-битный LCG `Random`, а `RandomExt` живёт на отдельном 64-битном seed'е (`SetRandomExtKey64`) и не реагирует на `SetRandomKey`. Реальные значения `RandomExt` оставались произвольными.

**v2 (2026-05, this version):** все патчи переведены на канонический stock-движковый паттерн `SetRandomKey(seed); ... random`. Этот же паттерн используется самим C3 для синхронизации в multiplayer — см. [unit.script:5301, 11453, 11528](C:/Program%20Files%20%28x86%29/Steam/steamapps/common/Cossacks%203/data/scripts/lib/unit.script) и [weapon.script:1051](C:/Program%20Files%20%28x86%29/Steam/steamapps/common/Cossacks%203/data/scripts/lib/weapon.script). Дополнительно добавлены 5 combat RNG-сайтов (выбор цели, headshot).

## Что патчится

### Extraction (peasant resource search) — 5 сайтов

| File | Line | Что | Seed inputs |
|---|---|---|---|
| lib/misc.script | 2790 | `_misc_FindResourceToExtract`: стартовый индекс в `gResGrid` cell | px, py, plInd, progresstick |
| lib/misc.script | 2801 | `_misc_FindResourceToExtract`: wood vs stone | px, py, plInd, progresstick |
| lib/unit.script | 4055 | `_unit_SearchResourceInRadius`: standtime gate | goHnd, progresstick |
| lib/unit.script | 4114 | `_unit_SearchResourceInRadius`: bskipcheck | goHnd, progresstick |
| lib/unit.script | 4120 | `_unit_SearchResourceInRadius`: стартовый индекс кандидатов | goHnd, progresstick |

### Combat (target selection / headshot) — 5 сайтов

| File | Line | Что | Seed inputs |
|---|---|---|---|
| lib/miscext2.script | 420 | `_misc_DoDamage`: bHeadShot (`random<0.05`) | attacker uniqrnd, target uniqrnd, progresstick |
| lib/unit.script | 4796 | `_unit_SearchEnemyInCellShips`: rndind (стартовый индекс в cell) | attacker uniqrnd, cellx, celly, progresstick |
| lib/unit.script | 4872 | `_unit_SearchEnemyInCell`: rndind | attacker uniqrnd, cellx, celly, plind, progresstick |
| lib/unit.script | 4992 | `_unit_SearchEnemyScanCellsLongRange`: dx random pick | attacker uniqrnd, loop i, cellx, progresstick |
| lib/unit.script | 4993 | `_unit_SearchEnemyScanCellsLongRange`: dy random pick | attacker uniqrnd, loop i, celly, progresstick |

Все seed-входы персистятся через save/load и идентичны на всех клиентах в multiplayer:
- `goHnd` — handle юнита; стабилен в пределах session, при Save/Load uid сохраняется.
- `TObj(pobj).uniqrnd` — per-unit Float ∈ [0, 1), фиксируется при спауне юнита через `RandomExt` и сохраняется в save (`pSync` packet, `WriteX/ReadX`).
- `cellx, celly, plind, plInd, i` — детерминированные локальные переменные функции.
- `px, py` — позиция юнита (Float), сохраняется в save format.
- `gProgress.progresstick` — глобальный счётчик тиков, сохраняется в save ([classes.script:6011](C:/Program%20Files%20%28x86%29/Steam/steamapps/common/Cossacks%203/data/scripts/lib/classes.script)).

## Что НЕ патчится (и почему)

- **Init random** (`obj.uniqrnd := RandomExt`, `gProgress.last*time := random*X`) — вызывается один раз при создании юнита/старте игры и потом сохраняется как обычное состояние. Не нужно патчить.
- **`_weapon_CalcShotDispertion`** — использует `RandomExt`, но уже обёрнут в `SetRandomKey(floor(newuniqrnd*gc_MaxInt))` upstream'ом ([weapon.script:1051](C:/Program%20Files%20%28x86%29/Steam/steamapps/common/Cossacks%203/data/scripts/lib/weapon.script)). Это движковый bug stock-кода (SetRandomKey не ловит RandomExt), но скриптом починить нельзя — нужен `SetRandomExtKey64`, а его параметры не выставляются из скрипта без знания внутреннего state.
- **AI random** (`RandomExt < _misc_RandToRandom(N)` в ai.script, `random<0.05` в `_unit_SearchVictim` для fake-friendly) — это AI-логика, не критична для воспроизводимости боя на стороне игрока.
- **Visual random** (анимации смерти, debris discard angle) — намеренный десинк визуала разработчиками, не влияет на состояние симуляции.
- **Pathfinding tie-breaking** — async поток (`PathDataThread*`, см. [internals/engine/rtti_class_map.md](../../internals/engine/rtti_class_map.md) §4), недоступно скрипту. Это остаточный источник дисперсии после нашего фикса.

## Как собрать

```bash
cd c:/projects/other/cossacks
python "mods/Deterministic Cossacks/build.py"
```

Скрипт читает оригинальные `lib/{misc,miscext2,unit}.script` из `$COSSACKS3_PATH` (default `C:\Program Files (x86)\Steam\steamapps\common\Cossacks 3`), применяет 10 патчей и пишет результат в `mods/Deterministic Cossacks/build/Deterministic Cossacks/`.

Если игра обновилась и оригинальные строки сместились — патчер выдаст warning «drift > 5» или ошибку «original line not found». В этом случае нужно перепроверить sites через [docs/recon/world/economy/peasant_extraction.md](../../docs/recon/world/economy/peasant_extraction.md) и [internals/engine/rng_implementation.md](../../internals/engine/rng_implementation.md), и обновить `expected_line` в `build.py`.

## Как установить

### Вариант 1: автоматически (нужны права записи в Program Files)

```bash
python "mods/Deterministic Cossacks/build.py" --install
```

Скопирует `mods/Deterministic Cossacks/build/Deterministic Cossacks/` в `<game>/mods/Deterministic Cossacks/` и пропишет mod в `<game>/mods/mods.ini`.

### Вариант 2: вручную

1. Скопируй папку `mods/Deterministic Cossacks/build/Deterministic Cossacks/` в `<game>/mods/`.
2. Открой `<game>/mods/mods.ini` и добавь внутри `mods : struct.begin` блок:
   ```
   [*] : struct.begin
      dir = ..\Deterministic Cossacks
      dis = False
   struct.end
   ```
3. Перезапусти Cossacks 3 (или запусти `modman.exe`).

## Тест-протокол

Карта Land+Highlands+Rich+Tiny на game speed fast.

### A. Тест добычи

Сейв с фиксированной расстановкой крестьян (например, 10 на лесу + 10 на камне).

**Без мода** (baseline):
1. Загрузить сейв.
2. Подождать 5 g-минут.
3. Записать накопленный wood/stone.
4. Повторить 5 раз.
5. Посчитать σ/μ.

**С модом**: то же самое.

**Ожидаемый результат:**
- Без мода: σ/μ ≈ 5–15% по wood/stone, ≈0% по mines.
- С модом: σ/μ <2% по wood/stone (остаточная дисперсия от pathfinding), 0% по mines.

### B. Тест боя

Сейв с фиксированной встречей (например, 20 mush vs 20 mush на симметричной позиции, без построений, без формаций).

**Без мода**:
1. Загрузить сейв.
2. Запустить бой, дождаться окончания.
3. Записать: время боя в g-сек, число выживших с каждой стороны, число headshot'ов (по логу), HP-остатки выживших.
4. Повторить 5 раз.

**С модом**: то же самое.

**Ожидаемый результат:**
- Без мода: разные исходы между загрузками (variance в победителе/выживших).
- С модом: бит-в-бит идентичный исход на каждой загрузке (если pathfinding не вмешался — а в открытом поле без obstacles он практически детерминирован).

Если σ/μ с модом не упал значительно — доминирует движковый источник дисперсии (pathfinding async thread, или stock `_weapon_CalcShotDispertion` с непатченным RandomExt) и без DLL injection это уже не починить.

## Ограничения

- **Не лечит async pathfinding.** Если два дерева/таргета на одинаковой дистанции, движковый pathfinder в `PathDataThread*` выбирает по своему внутреннему обходу графа, и порядок зависит от тайминга потока.
- **Не лечит `_weapon_CalcShotDispertion`.** Stock-код использует `RandomExt` после `SetRandomKey` — это bug движка, починить нельзя без `SetRandomExtKey64`.
- **Не лечит adaptive game speed** ([internals/engine/ticks_and_subticks.md](../../internals/engine/ticks_and_subticks.md) §5.2). На разных компах за равное real-time проходит разное game-time. Для сравнения исходов берите g-time, не real-time.
- При обновлении игры файлы `misc.script` / `miscext2.script` / `unit.script` в моде могут разойтись с оригиналом → нужен ребилд. Drift-warning сработает автоматически.

## Структура

```
mods/Deterministic Cossacks/
├── README.md                  ← этот файл
├── build.py                   ← патчер (читает оригиналы, генерит мод)
├── .gitignore
├── src/
│   └── mod.ini                ← metadata template
└── build/                     ← результат сборки (.gitignore'нут)
    └── Deterministic Cossacks/
        ├── mod.ini
        └── data/scripts/lib/
            ├── misc.script        ← пропатченный
            ├── miscext2.script    ← пропатченный
            └── unit.script        ← пропатченный
```

`build/` создаётся при каждом запуске `build.py` (с `shutil.rmtree` сначала). Не редактировать вручную — изменения перезатрутся.

## Откат

Если что-то сломалось:
1. В `mods/mods.ini` поставь `dis = True` для нашего mod entry, либо
2. Удали `<game>/mods/Deterministic Cossacks/`, либо
3. Удали entry из mods.ini.

Никаких следов мод не оставляет — оригинальные скрипты в `<game>/data/scripts/` не трогаются.
