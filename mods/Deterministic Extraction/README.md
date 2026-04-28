# Deterministic Extraction — Cossacks 3 mod

Заменяет 5 вызовов `random` в hot-path поиска ресурса на детерминированные `SetRandomKey + RandomExt` с seed'ом из персистящегося game-state. Цель: одинаковый сейв при повторных загрузках даёт одинаковую добычу леса/камня (в пределах движкового tie-breaking pathfinder'а, который скриптом не починить).

См. [recon/determinism_audit.md](../../recon/determinism_audit.md) §3 для каталога RNG-сайтов и [recon/server_sync_architecture.md](../../recon/server_sync_architecture.md) §6 для обоснования выбора параметров seed'а.

## Что патчится

5 RNG-сайтов в двух файлах:

| File | Line | Что | Seed inputs |
|---|---|---|---|
| lib/misc.script | 2790 | `_misc_FindResourceToExtract`: стартовый индекс в `gResGrid` cell | px, py, plInd, progresstick |
| lib/misc.script | 2801 | `_misc_FindResourceToExtract`: wood vs stone | px, py, plInd, progresstick |
| lib/unit.script | 4055 | `_unit_SearchResourceInRadius`: standtime gate | goHnd, progresstick |
| lib/unit.script | 4114 | `_unit_SearchResourceInRadius`: bskipcheck | goHnd, progresstick |
| lib/unit.script | 4120 | `_unit_SearchResourceInRadius`: стартовый индекс кандидатов | goHnd, progresstick |

Все seed-входы персистятся через save/load:
- `goHnd` стабилен в пределах session, при Save/Load uid сохраняется и handle восстанавливается;
- `px, py` — позиция (Float), сохраняется в save format ([miscext2.script:4004-4005](C:/Program%20Files%20%28x86%29/Steam/steamapps/common/Cossacks%203/data/scripts/lib/miscext2.script));
- `plInd` — индекс игрока, фиксирован;
- `gProgress.progresstick` — глобальный счётчик тиков, сохраняется в save ([classes.script:6011](C:/Program%20Files%20%28x86%29/Steam/steamapps/common/Cossacks%203/data/scripts/lib/classes.script)).

Многократно перепробованный паттерн `SetRandomKey(...) + RandomExt` уже используется движком для синхронизации снарядов в multiplayer ([weapon.script:1051](C:/Program%20Files%20%28x86%29/Steam/steamapps/common/Cossacks%203/data/scripts/lib/weapon.script)).

## Что НЕ патчится (и почему)

- **Init random** (`obj.uniqrnd := RandomExt`, `gProgress.last*time := random*X`) — вызывается один раз при создании юнита/старте игры и потом сохраняется как обычное состояние. Не нужно патчить.
- **Combat random**: `bHeadShot := (random<0.05)` ([miscext2.script:420](C:/Program%20Files%20%28x86%29/Steam/steamapps/common/Cossacks%203/data/scripts/lib/miscext2.script)) — оставлен. Бой и так на ~95% детерминирован (см. determinism_audit §4); хедшоты редкая случайность которая не влияет на economic flow.
- **Visual random** (анимации смерти, debris discard angle) — намеренный десинк визуала разработчиками.
- **AI random** (`RandomExt < _misc_RandToRandom(N)` на ai.script) — это бот-логика, отдельная задача.
- **Pathfinding tie-breaking** — в движке, недоступно скрипту. Это остаточный источник дисперсии после нашего фикса.

## Как собрать

```bash
cd c:/projects/other/cossacks
python "mods/Deterministic Extraction/build.py"
```

Скрипт читает оригинальные `lib/{misc,unit}.script` из `$COSSACKS3_PATH` (default `C:\Program Files (x86)\Steam\steamapps\common\Cossacks 3`), применяет 5 патчей и пишет результат в `mods/Deterministic Extraction/build/Deterministic Extraction/`.

Если игра обновилась и оригинальные строки сместились — патчер выдаст warning «drift > 5» или ошибку «original line not found». В этом случае нужно перепроверить sites через [recon/determinism_audit.md](../../recon/determinism_audit.md) §3 и обновить `expected_line` в `build.py`.

## Как установить

### Вариант 1: автоматически (нужны права записи в Program Files)

```bash
python "mods/Deterministic Extraction/build.py" --install
```

Скопирует `mods/Deterministic Extraction/build/Deterministic Extraction/` в `<game>/mods/Deterministic Extraction/` и пропишет mod в `<game>/mods/mods.ini`.

### Вариант 2: вручную

1. Скопируй папку `mods/Deterministic Extraction/build/Deterministic Extraction/` в `<game>/mods/`.
2. Открой `<game>/mods/mods.ini` и добавь внутри `mods : struct.begin` блок:
   ```
   [*] : struct.begin
      dir = ..\Deterministic Extraction
      dis = False
   struct.end
   ```
3. Перезапусти Cossacks 3 (или запусти `modman.exe`).

## Тест-протокол

Сейв с фиксированной расстановкой крестьян (например, 10 на лесу + 10 на камне), карта Land+Highlands+Rich+Tiny на game speed fast.

**Без мода** (baseline):
1. Загрузить сейв.
2. Подождать 5 минут real-time.
3. Записать накопленный wood/stone.
4. Повторить 5 раз.
5. Посчитать σ/μ.

**С модом**:
6. То же самое.

**Ожидаемый результат:**
- Без мода: σ/μ ≈ 5-15% по wood/stone, ≈0% по mines.
- С модом: σ/μ <2% по wood/stone (остаточная дисперсия от pathfinding), 0% по mines.

Если σ/μ с модом не упал значительно — доминирует движковый источник дисперсии (pathfinding или Save format incompleteness) и без DLL injection это уже не починить (см. determinism_audit §9).

## Ограничения

- Только **single-player детерминизм** (загрузка одного сейва). В multiplayer и так уже было детерминированно (server-authoritative + WriteX/ReadX sync), мод просто избыточен.
- **Не лечит adaptive game speed** ([ticks_and_subticks.md](../../recon/ticks_and_subticks.md) §5.2). На разных компах за равное real-time проходит разное game-time. Для калибровки модели сравнивать game-time, не real-time.
- **Не лечит pathfinding ties**. Если два дерева на одинаковой дистанции, движковый pathfinder выбирает по своему внутреннему обходу графа.
- При обновлении игры файлы `misc.script`/`unit.script` в моде могут разойтись с оригиналом → нужен ребилд.

## Структура

```
mods/Deterministic Extraction/
├── README.md                  ← этот файл
├── build.py                   ← патчер (читает оригиналы, генерит мод)
├── .gitignore
├── src/
│   └── mod.ini                ← metadata template
└── build/                     ← результат сборки (.gitignore'нут)
    └── Deterministic Extraction/
        ├── mod.ini
        └── data/scripts/lib/
            ├── misc.script    ← пропатченный
            └── unit.script    ← пропатченный
```

`build/` создаётся при каждом запуске `build.py` (с `shutil.rmtree` сначала). Не редактировать вручную — изменения перезатрутся.

## Откат

Если что-то сломалось:
1. В `mods/mods.ini` поставь `dis = True` для нашего mod entry, либо
2. Удали `<game>/mods/Deterministic Extraction/`, либо
3. Удали entry из mods.ini.

Никаких следов мод не оставляет — оригинальные `lib/misc.script`/`unit.script` в `<game>/data/scripts/` не трогаются.
