# Recon: Map seed space (~200-330 уникальных карт per param set)

**Цель:** ответ на вопрос «сколько уникальных карт может сгенериться при фиксированных параметрах».

> **Связано:** [map_generation_pipeline.md](map_generation_pipeline.md) — что именно делает DoGenerate с этим seed (полный таймлайн, все procedures).

## TL;DR

Для одних и тех же параметров (terrain type + map size + relief + mines + players) **карта однозначно определяется парой `(inputbitmap, randkey1)`** где:
- `inputbitmap` выбирается из списка `data/gen/terrainmasks/<terrain>/Npl_mask_*.tga` (для N=4pl и terrain=land — **230 файлов**);
- `randkey0/randkey1` — 64-битная пара RNG-сидов (`SetRandomExtKey64`), задаёт распределение лесов/камней/шахт ВНУТРИ выбранной маски.

Базовых masks для 4 игроков:

| terrain folder | n_files |
|---|---:|
| `continent/` | 121 |
| `continents/` | 187 |
| `islands/` | 320 |
| `land/` | **230** |
| `mediterranean/` | 122 |
| `nowater/` | 42 |
| `nowater2/` | 33 |
| `peninsulas/` | 280 |

Итого по terrain Land+4pl: **~230 базовых форм** карт. Совпадает с user-observed «~200» (округлённо).

## Pipeline

1. **Lobby собирает settings.** `gMap.settings.gen` содержит: `mapsize`, `relieftype`, `resourcemines`, `terraintype`, `season`, `randkey0`, `randkey1`. Последние два устанавливаются вызовом `GenerateMapRandKey(randkey0, randkey1)` ([map.script:322](C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/map.script#L322)) — engine-builtin генерирует пару int.

2. **Выбор bitmap.** [`generatemap.inc:179-191`](C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/common.inc/generatemap.inc#L179):
   ```pascal
   ParserGetFilesInRoot(folderpath+'\Npl*.tga');   // N = playerscount
   var rndind : Integer = floor(RandomExt*count);
   inputbitmap := ParserGetValueByIndexByHandle(pFileList, rndind);
   ```
   Из найденного списка (см. таблицу выше) случайный индекс. `RandomExt` использует уже установленный `randkey1`.

3. **Apply randkey для деталей.** [`generatemap.inc:216`](C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/common.inc/generatemap.inc#L216):
   ```pascal
   SetRandomExtKey64(randkey0, randkey1);
   ```
   Все последующие `RandomExt`-вызовы (placement лесов, шахт, начальных юнитов) — детерминированы этим seed.

4. **Pattern placement.** [`misc.script:3704`](C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/misc.script#L3704): для каждого pattern type делается `floor(256*mapsizeoptimise)` попыток размещения, координата выбирается через `RandomExt*mapwidth`. Поэтому **точное расположение** леса/камня внутри одной и той же базы зависит от randkey, но **общее число** кластеров — функция density × area, не зависит от seed.

## Что это даёт

1. **Bounded enumeration.** Если хочешь обойти все возможные карты для (Land, Tiny, 4pl, Highlands, Rich) — это **230 базовых форм** × ~K randkey вариаций. K не известен но скорее всего лежит в 100-1000 (не миллионы). User estimate "~200" — это, видимо, доминирующий компонент = bitmap count.

2. **Deterministic replay.** Если знаешь `(inputbitmap, randkey0, randkey1)` пара — можешь воспроизвести КАРТУ (включая позиции каждого дерева/камня/шахты) bit-for-bit при условии что engine RNG детерминирован между запусками (см. [determinism_audit.md](determinism_audit.md)).

3. **Калибровка trees per pattern.** Можно сгенерить КАЖДЫЙ из 230 land-bitmaps с одним randkey, посчитать trees in-game (или в save-file) → empirical mapping `bitmap → tree count`. Усреднение → точная per-foreststype оценка вместо текущей `0.30 × mask_cells` калибровки.

## Ограничения / open questions

- **`GenerateMapRandKey` body unknown** — это engine-builtin, не Pascal. Range randkey0/randkey1 не точно известен.
- **`SetRandomExtKey64`** принимает 64-битный ключ — теоретически 2^64 значений, но lobby probably ограничивает диапазоном вроде 0..10^9 (4-байтный seed UI).
- **Save-files** хранят randkey1 в имени файла: `'game_v'+gSerialVersion+'k'+randkey1+'.map'` ([miscext2.script:15](C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/miscext2.script#L15)). Если читать save filenames из replays — можно собрать distribution actual seeds.

## Применение для tree-count empirics

Если хочешь точно посчитать деревья по типу паттерна:

1. Запусти 5-10 random map gen с фиксированным `(terraintype=Land, mapsize=Tiny, foreststype=0)`.
2. Для каждой записи `inputbitmap.tga` + `randkey1` (видны в game log).
3. В сейве парсить количество env-объектов с baseid=res и itype=wood — это даст **точное число chopable trees on this map**.
4. Делить на число placed clusters → empirical `chopable_trees_per_cluster` per pattern type.

С 5 запусков калибровка будет точнее текущей 0.30 константы.
