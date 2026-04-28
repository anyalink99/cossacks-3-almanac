# Recon: Map generation pipeline (DoGenerate full timeline)

**Источник:** [`data/scripts/common.inc/dogenerate.inc`](C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/common.inc/dogenerate.inc) (2103 строки), вызывается через `ExecuteState('DoGenerate')` из [`initmapgen.inc:232`](C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/common.inc/initmapgen.inc#L232).

> **Связанные документы:**
> - [map_seed_space.md](map_seed_space.md) — что именно определяет seed (`inputbitmap` + `randkey0/1`).
> - [peasant_extraction.md §8](peasant_extraction.md) — densities (frs_big, mnt, …) и distance-таблицы для mines.
> - [pattern_format.md](../output/reference/pattern_format.md) — что такое `.pattern` файл и как mask мапится в env-объекты.

---

## 1. Глобальные константы (объявлены до процедур)

Из [dogenerate.inc:407-416](C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/common.inc/dogenerate.inc#L407):

```
cCircle1MaskX = 5    cCircle1MaskY = 7    // forbidden zone — здесь только Phase-1 mines
cCircle2MaskX = 12   cCircle2MaskY = 15   // 1× stoneforest + 1× stones + 2× forests
cCircle3MaskX = 22   cCircle3MaskY = 18   // 1× stones + 1× forest
cBorderObjDist = 1                        // peacetime wall spacing (tiles)
```

Это **полу-оси эллипсов** в `gPatternMask`, центрированные на каждой стартовой точке. Внутри эллипса `gPatternMask[x,y] := True` → ничего больше нельзя ставить (ни лес, ни камни, ни здания env-плеера). Эллипсы заполняются через `_misc_FillPatternMaskElipse(pointx, pointy+2, rx, ry)` — **с +2 смещением по Y** (стартовый поинт сдвинут вверх относительно центра масок).

Также:
- `var foreststype : Integer = floor(RandomExt*3); foreststype := 0;` ([dogenerate.inc:5-6](C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/common.inc/dogenerate.inc#L5)) — **foreststype всегда = 0**. Случайная инициализация немедленно перезаписана. Следствие: на Land **никогда** не бывает leaf-only (`foreststype=1`) или mixed-only (`foreststype=2`) карт. Только foreststype=0 mix: pinefir/spruce/pine/pine_big_2 (big), pinefir/spruce/pine (mid), pinefir/pine (small).
- `var bDesert : Boolean = (gMap.settings.gen.season=3);` — season=3 переключает все pattern types на `desert_*`. Для Land+любая-другая-сезон bDesert=False.
- `var maphW : Integer = mapW div 2;` — половина ширины карты (используется для tiny-corner-snapping в SetupMines round 2).

---

## 2. Pipeline (хронологический порядок, файлы от вершины DoGenerate вниз)

### Phase 0 — подготовка
1. [Lines 1-78] Helper-procedures для масок (FillPatternMaskElipse/Circle/Rectangle/MapBorder).
2. [Lines 80-419] Helper-procedures для юнитов и UniqueStartingUnits (нация-специфичные офицеры/барабанщики при `startingunits>default`).
3. [Lines 444-497] `ClearMapMaskAndObjects` — очистка `gPatternMask` (640×640), `arrStartPos[0..7]`, `arrStartPosBusy[i] := -1`.
4. [Lines 1284-1289] `_gui_ProcessProgressBar('progressbar.loadingenvironment')` → `LoadPatterns(True, False)` + `LoadPatterns(True, True)` — загружает все `.pattern` файлы из `data/gen/patterns/*`.

### Phase 1 — terrain
5. [Lines 1291-1296] Подсчёт `plcount` = существующие non-spectator игроки.
6. [Line 1535] `SetupTiledPatterns('tiles')` (или `desert_tiles` если bDesert) — кладёт фоновые decoration-tiles (например, грязь, трещины) на 25×25-tile сетку: `wcount = mapW div 25`, `hcount = mapH div 25`, центр каждого блока `realx = (x*25) + 12 - mapW/2 - 1`. Для 256×256 это ~10×10 ≈ **100 размещений**.
7. [Line 1538] `SetRandomKey(randkey1)` — все последующие `RandomExt` детерминированы этим seed.
8. [Lines 1542-1565] `relieftype`, `terraintype`, `minesdensity` resolved (random если выходит за валидный диапазон). Выбирается `pTerrainTypes` (DLC5 или нет в зависимости от gRecordGeneratorVersion). `ExecuteState('GenerateMap')` — engine-builtin строит heightmap из выбранного `inputbitmap.tga`, заполняет тайлы.
9. [Lines 1568-1581] Маркер water shore: для каждой клетки если height < -0.1 → `gPatternMask[x,y] := True`.
10. [Lines 1585-1587] Если `minesdensity > 2` (random) → `floor(RandomExt*3)`.
11. [Line 1590] `_misc_SetDesert(False, False)` если bDesert.

### Phase 2 — старт-поинты
12. [Lines 1596-1611] Цикл по игрокам: для каждого с валидным `startx/y` (`>= -mapW/2`) → `arrStartPos[i] := startx, starty`. **Сами координаты `gMap.players[i].startx/y` приходят из C++ engine** — он их вычисляет при загрузке `inputbitmap.tga` (по специальным маркерам в маске). `spcount` = количество игроков с валидным стартом.
13. [Line 1613] `_misc_FillPatternMaskMapBorder(3)` — внешняя рамка 3 тайла шириной заблокирована.
14. [Line 1615] **`RandomStartingPoints(spcount, minesdensity)`** — назначает игроков на arrStartPos с учётом team option (см. §3 ниже). Внутри для каждого игрока вызывается `CreateStartPoint(plInd, pointx, pointy, minesdensity, plcount)` → который делает:
    - `_misc_FillPatternMaskElipse(pointx, pointy+2, cCircle1MaskX=5, cCircle1MaskY=7)` — закрывает innermost зону.
    - `SetupMines(pointx, pointy, minround=0, maxround=1, minesdensity, spcount)` — **только round 0** (близкие mines).
    - `SetupStartingResources(pointx, pointy)` — кладёт ~5-6 кластеров вокруг (см. §4).
15. [Line 1616] `SetRandomKey(randkey1)` — re-seed (детали placement не должны влиять на следующие фазы).

### Phase 3 — relief densities + Phase-2 mines
16. [Lines 1621-1650] `relieftype` cases: plt/mnt/hil выбираются. Highlands (=3): plt=0.000055, mnt=0.000120, hil=0.000050.
17. [Lines 1688-1693] `frs_big=0.0009`, `frs_mid=0.0009`, `frs_small=0.00054`, `dcr=0.0005`, `stn1=0.00016`, `stn2=0.00012`.
18. [Lines 1715-1725] `_misc_GetFreePatternMaskModifier(probsmall, probmid, problarge, probhuge)` — Monte-Carlo на свободных клетках; затем умножается на map-size modifier `640/((mapW+mapH)/2)`. Для tiny это ×2.5.
19. [Lines 1727-1739] Финальные densities: `pln_small/_mid/_large/_huge`, `swamp_*`, `lake_*`, mnt/plt/hil умножены на `problarge`.
20. [Lines 1745-1766] `_misc_SetupPatternsByType(...)` для mountains/plateau (×3 части)/ravine/hills.
21. [Lines 1768-1771] **Phase-2 mines:** `for i:=0 to spcount-1 do SetupMines(arrStartPos[i].x, .y, minround=1, maxround=0, minesdensity, spcount)` — раунды 1..rounds-1 (внешние кольца). `maxround=0` означает «не override», т.к. условие `if (maxround>0)` false.
22. [Line 1772] `SetRandomKey(randkey1)` — re-seed снова.
23. [Lines 1774-1908] `_misc_SetupPatternsByType` для forests/stones/plain/swamp/lake — здесь `foreststype` диктует ветку (но всегда =0, так что только pine/spruce/pinefir и mixed pine_big_2).

### Phase 4 — старт-юниты + финализация
24. [Lines 1914-1923] **`for i:=0 to gc_MaxPlayerCount-1 do CreateStartPointPeasants(i, startx, starty)`** (или `CreateUniqueStartingUnits` если `startingunits>default`).
25. [Line 1925] `_misc_PreloadTextures(True, True, True)`.
26. [Line 1939] `gbool_gui_mapgenerationfinished := True`.
27. [Lines 1971-2027] Сезонная нормализация env-objects: зимой удаляются `leaftree*`; нерандомные scale clamping в `[scaleMin, scaleMax]`.
28. [Lines 2031-2050] AI setup: `gPlayer[i].progressTick := (cProgressAITick=16 div count)*ind`.
29. [Line 2052] `_player_SetupTeams(true)`.
30. [Line 2059] `gfloat_peacetime := _misc_GetPeaceTime(...)`; `gbool_peacemode := (peacetime <> default)`.
31. [Line 2062] **`FillOwnerMap(spcount)`** (см. §5).
32. [Lines 2064-2065] `if gbool_peacemode then SetupBorderObjects` (см. §6).
33. [Line 2068] `_misc_SetShoresCollision`.
34. [Lines 2075-2084] Color table per season (winter=6, desert=7, default=0; PHDR=1 для winter, 0 иначе).
35. [Line 2100] `TimeLog('Generation finished. relieftype=... minesdensity=...')`.

---

## 3. `RandomStartingPoints(plcount, minesdensity)` — раздача игроков

[dogenerate.inc:1090-1229](C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/common.inc/dogenerate.inc#L1090). Две ветки в зависимости от `gMap.settings.additional.teams`:

### 3.1 `teams = nearby` (союзники рядом)
1. Группируем игроков по `team` (5 команд: 0 = соло-плеера, 1..4 = командные).
2. Если в команде только 1 человек — переносим его в team[0] (соло).
3. Сортируем `teamlist` (команды с >1 игроком) — для каждой:
   - `SetRandomKey(randkey1)` + advance i раз.
   - Случайно выбираем стартовую команду из `teamlist`.
   - Вызываем `GenerateTeamStartingPoints(teamcount, pointsbusy, points)` (lines 999-1088): жадный greedy-алгоритм:
     - Берём random первую точку.
     - Каждую следующую выбираем как «точку, к которой ближе всего БОЛЬШИНСТВО уже выбранных» (если ничья по count → меньшая total distance).
   - В случайном порядке (через `SetRandomKey + RandomExt`) распределяем `points` между членами команды.

### 3.2 `teams = default` (по разным углам)
- Все игроки в team[0]. Для каждого: `SetRandomKey(randkey1) + advance(i+8)` → случайный `pointindex` из оставшихся.

В обоих случаях итогом является вызов `CreateStartPoint(player, x, y, minesdensity, plcount)` для каждого, который и запускает Phase-1 mines + StartingResources.

**Источник arrStartPos[].x/y:** **C++ engine читает inputbitmap.tga и находит спец-цвета (пиксели-маркеры старт-поинтов)**. Скрипт получает их готовыми через `gMap.players[i].startx/starty`. Скрипт умеет только переставить players между готовыми точками.

---

## 4. `SetupStartingResources(pointx, pointy)` — что спавнится возле города

[dogenerate.inc:720-978](C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/common.inc/dogenerate.inc#L720). Шесть последовательных placement-фаз, каждая пытается до 128×3 = 384 разных позиций (vary angle + distance). Вызывается из CreateStartPoint **после** того как cCircle1 уже заполнен.

| # | Pattern type | mindst (tiles) | dst формула | После: маска |
|--:|---|---:|---|---|
| 1 | `stoneforests` (или `desert_stoneforests`/`desert_forests_big` для bDesert) | min(5,7)=5 | `5 + RandomExt*3 + (i+j)*0.5` | — |
| 2 | _FillPatternMaskElipse(cCircle2=12,15) | — | — | блокирует средн. зону |
| 3 | `stones` | min(12,15)=12 | `12 + RandomExt*3 + (i+j)*0.5` | — |
| 4 | `forests_pinefir/spruce/pine_*_medium/big` (×2 раза, foreststype=0 → random pick из 7 вариантов) | 12 | то же | — |
| 5 | `stones` | min(12,15)+4 = 16 | `16 + RandomExt*2 + (i+j)*0.5` | — |
| 6 | `forests_*_medium/big` (ещё 1 раз) | 16 | то же | — |
| 7 | _FillPatternMaskElipse(cCircle3=22,18) | — | — | блокирует внеш. зону |

**Что это значит для базы игрока:** в радиусе **5..22 тайла** от центра города ВСЕГДА есть гарантировано:
- 1× `stoneforests` (mixed wood+stone в одном паттерне, mask~152)
- 2× `stones` (mask~138 каждый)
- 3× `forests_*_big/medium` (mask 148..1631 в зависимости от типа)

После этого зона ≤22 тайла полностью замаскирована — ничего больше Phase 3 туда не положит. **Это объясняет почему в начале игры всегда хватает дерева на ratuse + первый mill.**

Для desert замены: `desert_stoneforests`/`desert_forests_big`/`desert_stones`/`desert_forests_medium/big`.

---

## 5. `FillOwnerMap(spCount)` — кому какая клетка принадлежит

[dogenerate.inc:1370-1428](C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/common.inc/dogenerate.inc#L1370). Простой BFS:

1. Init `gScanGrid[i,j]` (размер `gc_scangrid_countx × gc_scangrid_county`): `owner=-1, dist=-1, fChecked=False`.
2. Для каждой стартовой позиции: `_misc_PosToScanGridIndices(arrStartPos[i].x, .y, gridX, gridY)` → `gScanGrid[gridX,gridY].owner := arrStartPosBusy[i]` (player id), `dist := 0`.
3. BFS: пока есть необработанные клетки на текущем dist → раздаём 4 соседям (i±1, j±1) тот же owner с `dist+1`.

Результат: каждая ячейка scan-grid'а помечена ID ближайшего игрока (по Manhattan distance в grid units).

---

## 6. `SetupBorderObjects` — peacetime walls

[dogenerate.inc:1430-1527](C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/common.inc/dogenerate.inc#L1430). Запускается **только если `gbool_peacemode`** (т.е. peacetime <> default).

Идея: для каждой пары соседних клеток `gScanGrid[i,j]` и `gScanGrid[i+1,j]` (а также `[i, j+1]`):
- Если `owner` различается → провести цепочку border-объектов между центрами этих клеток.
- Шаг: `cBorderObjDist = 1` тайл.
- На воде: `gc_basename_ptborderwater`, на суше: `gc_basename_ptborder`.
- Объекты создаются у misc-плеера (`gc_playerind_misc`), `GameObjectMakeUniqId` для uniqueness.

**Импликация для нашего sim:** мы peacetime игнорируем. На default peacetime эти стены не ставятся → можно не моделировать.

---

## 7. `CreateStartPointPeasants(plInd, pointx, pointy)` — стартовые крестьяне

[dogenerate.inc:1231-1281](C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/common.inc/dogenerate.inc#L1231).

```
count = 18         # ВСЕГДА 18 крестьян
cUnitR = 0.75      # шаг сетки
for i = 0 to 17:
    px = pointx + (i div 3) * 0.75 + (0.5 - RandomExt) * 0.25 - (6 * 0.75)/2
    pz = pointy + (i mod 3) * 0.75 + (0.5 - RandomExt) * 0.25 - (0 * 0.75)/2
    spawn peasant(px, py, pz)
    SetGameObjectRollAngleByHandle(goHnd, 180)  # лицом вниз
```

**Сетка:** 6 колонок × 3 ряда. Шаг 0.75 тайла. Random jitter ±0.125. **Quirk:** `count mod 3 = 18 mod 3 = 0`, поэтому Y-центрирующее смещение = 0. Z-координаты идут от `pointy + 0` до `pointy + 1.5` (т.е. сетка смещена ВНИЗ относительно центра, не центрирована). X-координаты центрированы корректно: от `pointx - 2.25` до `pointx + 1.5`.

Совпадает с empirically наблюдаемыми **18 idle peasant** в [reference_food_upkeep.md](../../Users/stasi/.claude/projects/c--projects-other-cossacks/memory/reference_food_upkeep.md) (verified 2026-04-29: 18 × 32 + 30 food/g-сек × 32/20000 × 120 = 214 food).

Если `gMap.settings.additional.startingunits > default` → вместо 18 пеасантов вызывается `CreateUniqueStartingUnits` (нация-специфичный squad: офицер + барабанщик + несколько infantry).

---

## 8. Что значит «Phase 1 vs Phase 2 mines»

`SetupMines(pointx, pointy, minround, maxround, minesdensity, spcount)` управляется флагами:

| Вызов | minround | maxround | rounds итог | Где |
|---|---:|---:|---|---|
| Phase 1 (внутри CreateStartPoint) | 0 | 1 | i:=0..0 (только round 0) | line 985 |
| Phase 2 (после relief) | 1 | 0 | i:=1..rounds-1 (round 0 пропущен) | line 1770 |

`if (maxround>0) and (rounds>maxround) then rounds := maxround;` ⇒ Phase 1 ограничивает rounds=1; Phase 2 maxround=0 → no override, использует полный rounds=case minesdensity.

Для **Rich (minesdensity=2) на Tiny (mapsize>2)** [version ≥80]:
- Phase 1: 1× round 0 × 3 ресурса = 3 close deposits (1g+1i+1c) на расстоянии 14..22 тайлов.
- Phase 2: rounds 1..4, но round 4 = `continue` на tiny ⇒ 3 outer rounds × 3 ресурса = 9 outer deposits.
- **Итого 12 deposits per player** при условии успеха всех 256-try попыток.

Особый случай: round 2 на tiny+spcount≤4 (line 658-696, version≥90) — `newpointx/y` snap на угол карты (`±maphW∓24, ±maphH∓24`) для самых дальних деопозитов. Это «ничейные» mines в углах, к которым нужно ехать вдоль карты.

---

## 9. Версионные различия (gRecordGeneratorVersion)

В коде много `if (gRecordGeneratorVersion < N) then …`. Текущий ванильный игровой клиент (DLC5 era) имеет version ≥ 90+, что включает:
- DLC5 terrain types (line 1555).
- Distance table v90+ (mines round 2 = 70..82 на tiny, snap to corner).
- `gRecordGeneratorVersion < 53` → удаляются player handle 8.
- `< 89` → удаляются 9, 10, 11.

Мод-разработчик может проверить `gRecordGeneratorVersion` через [`data/game/var/data.cfg`](C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/game/var/data.cfg) или через git log этого файла.

---

## 10. Что наша симуляция в `parser/` и `simulator/` модулирует / упрощает

Проверочный список того, что код dogenerate.inc делает, но мы либо игнорируем, либо приближаем:

| Реальность | Наша симуляция | Статус |
|---|---|---|
| Engine читает arrStartPos из inputbitmap.tga | Жёстко задаём 1 startpos | OK для 1pl-сценариев |
| 6 placement-фаз SetupStartingResources с конкретными шаблонами | Считаем aggregate forest/stone density | **Грубо** — стартовые ресурсы недоучтены |
| cCircle1/2/3 forbidden zones | Не учитываем | Влияет только на placement, не на totals |
| Phase 1 mines (round 0, 14..22 tile) | Аппроксимировано через total mine count | OK |
| Phase 2 corner-snap для round 2 на tiny | Не учитываем (даём 70..82 без snap) | Минорно |
| foreststype always 0 | Подразумеваем Land mix → совпадает | OK |
| FillOwnerMap + peacetime borders | Игнорируем | OK для default peacetime |
| 18 starting peasants в 6×3 grid | Жёстко 18 в config | OK |
| Sezon=3 → desert pattern types | Не реализовано | TODO если нужен desert |
| Random teams=nearby алгоритм | Не реализовано | OK для 1pl-сценариев |

---

## 11. Ключевые файлы pipeline

| Что | Где | Linenoы |
|---|---|---|
| Главный orchestrator | `data/scripts/common.inc/dogenerate.inc` | 1-2103 |
| Точка входа | `data/scripts/common.inc/initmapgen.inc` | 232 |
| Mission map вариант | `data/scripts/common.inc/dogeneratemissionmap.inc` | — |
| Engine RNG seed setup | `data/scripts/lib/map.script` | 322 (`GenerateMapRandKey`) |
| InputBitmap selection | `data/scripts/common.inc/generatemap.inc` | 179-216 |
| StandPattern (C++ внутри) | `data/scripts/lib/misc.script` | 3390 (declaration only) |
| GenerateMap state | engine-builtin | вызывается line 1565 |

---

## 12. Открытые вопросы (для следующих сессий)

1. **Точное положение arrStartPos в inputbitmap.tga.** Engine как-то находит маркеры в маске. Скорее всего по специальным RGB-кодам пикселей. Если декодировать `data/gen/terrainmasks/land/4pl_*.tga` руками — можно построить точную карту start-positions для каждого preset.

2. **`_misc_GetFreePatternMaskModifier`** возвращает 4 числа (probsmall/mid/large/huge). Источник в `data/scripts/lib/misc.script:3929-3941` ([peasant_extraction.md §8.4](peasant_extraction.md#84-леса-и-камни--densities-вне-шахт) описывает Monte-Carlo). Конкретные значения для нашего scope (Tiny+Highlands) — **не измерены**, оценка ≈1.85-2.06.

3. **`SetupTiledPatterns` влияет ли на placement других объектов?** ~100 tile-paterns на 256×256 — это «ground decoration» (трещины, грязевые пятна). Возможно, они также блокируют `gPatternMask` для последующих placement фаз — нужно проверить через `_misc_CheckStandPatternExt` поведение.

4. **C++ функции `StandPatternWithAngle`, `_misc_FillPatternMaskBy*`** — доступны только декларации, не тело. Значит финальный mapping `mask cell → конкретный env-object class` (oak vs leaftree vs decortree) — out of reach без disasm exe.

5. **gRecordGeneratorVersion live value** — нужно вытащить runtime значение чтобы знать какая ветка mines distance таблицы реально применяется. Скорее всего ≥90, но точно не подтверждено.
