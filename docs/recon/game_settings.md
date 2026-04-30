# Recon: настройки лобби — что движок делает с каждой опцией

Этот документ — **handwritten reverse-engineering** того, как движок Cossacks 3
реагирует на выбор игрока в лобби. Сюда не выносятся значения и лейблы — для
этого есть две точки правды:

- **[`docs/reports/map/lobby_settings.md`](../reports/map/lobby_settings.md)** —
  готовый справочник всех опций (названия из локали, числовые значения,
  значения по умолчанию).
- **[`docs/derived/game_settings.json`](../derived/game_settings.json)** — то же
  самое в машинно-читаемом виде, для редактора и инструментов.

Здесь — только то, что нельзя увидеть в таблице: какие функции скриптов читают
эти значения, какие флаги выставляют, какие игровые механики при этом
включаются.

## Источники

- `data/scripts/lib/classes.script:58-88` — структуры `TMapSettings`,
  `TMapSettingsGen`, `TMapSettingsAdditional`.
- `data/scripts/dmscript.global` — все `gc_mapsettings_*` константы (строки
  1025-1098), `gc_settings_gamespeed_*`, `gc_player_difficulty_*`.
- `data/scripts/common.inc/{dogenerate.inc, initmapgen.inc, initmap.inc}` —
  места, где значения применяются к игре.
- `data/scripts/lib/misc.script:_misc_GetPeaceTime` — декодирование `peacetime`
  в игровые секунды.
- `data/scripts/lib/miscext2.script:_misc_SaveLanRoomData` — сериализация
  настроек в save-файл (строки 2360-2380).

Все номера строк — из текущих файлов установки. После патча игры
перепроверять.

## 1. Структура `TMapSettings`

Из `classes.script:85-88`:

```pascal
type TMapSettings = class
   gen        : TMapSettingsGen;          // параметры генератора карты
   additional : TMapSettingsAdditional;   // правила игры
end;
```

`gen` решает, **как** рисуется карта (рельеф, размер, ресурсы, сезон),
`additional` — **по каким правилам** идёт партия (peacetime, лимит, скорость,
помощник). Содержимое сохраняется в save через
`_misc_SaveLanRoomData` (`miscext2.script:2360-2380`).

`TMapSettingsGen` (`classes.script:74-83`):

```pascal
type TMapSettingsGen = class
   randkey0      : Integer;   // RNG-ключ для размещения (mines / forests / stones)
   randkey1      : Integer;   // RNG-ключ для рельефа / ландшафта
   mapsize       : Integer;   // 0..3 — размер
   terraintype   : Integer;   // 0..9 — тип ландшафта / воды
   relieftype    : Integer;   // 0..5 — тип рельефа
   resourcestart : Integer;   // 0..3 — стартовые ресурсы
   resourcemines : Integer;   // 0..2 — плотность шахт
   season        : Integer;   // 0..3 — сезон / декорации
end;
```

`TMapSettingsAdditional` (`classes.script:58-72`):

```pascal
type TMapSettingsAdditional = class
   activeoption     : Integer;
   startingunits    : Integer;   // стартовый набор юнитов / зданий
   balloon          : Integer;   // монгольфьеры
   cannons          : Integer;   // пушки / стены / башни
   peacetime        : Integer;   // время мира
   century18        : Integer;   // переход в 18 век
   capture          : Integer;   // правила захвата
   marketdip        : Integer;   // рынок / дипцентр
   teams            : Integer;   // расположение союзников
   autosave         : Integer;
   limit            : Integer;   // лимит населения
   gamespeed        : Integer;   // скорость партии
   adviserassistant : Integer;   // помощник
end;
```

Числовые значения и человеческие названия — в
[`reports/map/lobby_settings.md`](../reports/map/lobby_settings.md). Здесь — что
именно читает движок.

## 2. Что движок делает с `gen`-параметрами

| Поле | Где применяется | Что делает |
|---|---|---|
| `mapsize` | `dogenerate.inc:1530-1545` | Задаёт `Width × Height` карты в тайлах (карта квадратная). Влияет на плотность размещения и `prob*` модификаторы (`misc.script:3929-3941`). |
| `terraintype` | `dogenerate.inc:1500-1530`, `_misc_HasMaritime` (`misc.script:5466`) | Выбирает таблицу масок (`data/gen/terrainmasks/`) для базового изображения карты. `terraintype ∈ {2,3,4}` (Полуострова / Острова / Континенты) включает «морские» воды — без `por` (порт) к ним нельзя добраться. |
| `relieftype` | `dogenerate.inc:1640-1660` | Выбирает плотность гор/холмов (`mnt`, `hgh`). На `relieftype = 3` («Высокогорье») плотность гор максимальная — меньше ровных площадей под фермы и склады. |
| `resourcestart` | `initmapgen.inc:166-189` | Цикл `for j := 0 to gc_ResCount - 1 do _res_SetResToPlayerByIndex(i, j, ...)` — каждому игроку даёт стартовое количество **каждого** из 6 ресурсов. Значения по `resourcestart`: 1000 / 4000 / 5000 / 1 000 000. |
| `resourcemines` | `dogenerate.inc:1544` | Подставляется в `minesdensity` — управляет фазой размещения шахт. См. [`map_generation_pipeline.md`](map_generation_pipeline.md) §8 (3 раунда × 3 типа = 9 месторождений на игрока для Tiny + Rich). |
| `season` | `dogenerate.inc:4` | `bDesert := (season = 3)`. Этот флаг переключает набор pattern-типов (`forests_pinefir_*` → `desert_forests_*` и т. д.). Прочие сезоны меняют только текстуры. |
| `randkey0` / `randkey1` | `generatemap.inc:142`, `dogenerate.inc` (многократно) | RNG-ключи. `randkey1` используется для рельефа (`SetRandomKey`), `randkey0` — для расстановки. **Тройка `(inputbitmap, randkey0, randkey1)` детерминирует карту** — поэтому реплеи воспроизводят ту же карту. Подробнее — [`map_generation_pipeline.md` §12](map_generation_pipeline.md#12-seed-space). |

> **`foreststype` и Land.** Игрок выбирает `foreststype` в lobby, но на
> `terraintype = 0` (Суша) движок немедленно перезаписывает его в `0`
> (`dogenerate.inc:5-6`). На non-Land картах выбор работает.

## 3. Что движок делает с `additional`-параметрами

### 3.1 `startingunits` — стартовая армия

Конкретный набор юнитов / зданий для каждого варианта читается из
`data/game/var/startingsettings.cfg`. Поля: `addresources` (доп. ресурсы),
`countries` (легенда расстановки: `P` = крестьянин, `X` = пехотинец, `B` =
барабанщик, `O` = офицер, `Q`/`W` = mission-здания и т. д.).

> **Базовые 18 крестьян появляются всегда.** Независимо от выбора движок
> вызывает `CreateStartPointPeasants` (`dogenerate.inc:1231-1281`) и расставляет
> **18 крестьян** в сетке 6×3 вокруг стартовой точки с радиусом 0.75 тайла.
> Даже на «По умолчанию» у игрока сразу 18 крестьян.

### 3.2 `peacetime` — как устроен мир

Декодирование значения в игровые секунды:

```pascal
function _misc_GetPeaceTime(ind : Integer) : Float;
begin
   case ind of
      0  : Result := 0;     // No peace time
      1  : Result := 10;    // 10 минут
      2  : Result := 20;
      3  : Result := 30;
      4  : Result := 45;
      5  : Result := 60;
      6  : Result := 90;
      7  : Result := 120;
      8  : Result := 180;
      9  : Result := 240;
      11 : Result := 15;
   end;
   Result := Result * 60;   // переводим в g-секунды
end;
```

`misc.script:4262-4282`. Минуты — **игровые**: на скорости fast (`gamespeed = 2`)
одна игровая минута ≈ 42.9 реальных секунд, и 10-минутный мир длится ≈ 7
реальных минут.

При генерации карты:

- `gbool_peacemode := (peacetime <> 0)` — флаг включается, если выбран любой
  ненулевой пресет (`dogenerate.inc:2060`).
- `gfloat_peacetime := _misc_GetPeaceTime(ind)` — конкретное значение в
  игровых секундах.
- `SetupBorderObjects` создаёт визуальные «границы» вокруг каждого игрока
  (`dogenerate.inc:2065`).

Пока `gbool_peacemode = True`:

- **Поиск врагов запрещён.** В `_unit_SearchEnemy*` (`unit.script:5516`)
  проверяется `bpeacetime` — если `True`, ни один юнит не находит врагов и не
  атакует.
- **Сетка владения территорией.** `_misc_IsCorrectScanCellOwner`
  (`misc.script:2424`) возвращает `True` только для ничейных и собственных
  ячеек — враги не могут зайти на твою территорию.
- **Захват зданий запрещён** на чужой территории.

Каждый Nothing-tick (`progress/nothing.inc:658`) сервер проверяет окончание
мира:

```pascal
if (gbool_peacemode) and (gametime > gfloat_peacetime)
   and (not _net_IsReplay) and (not _net_IsClient) then
begin
   gbool_peacemode := false;
   // удалить ptborder-объекты, перейти к войне
end;
```

Решение принимает только сервер (host в MP, single-player). В реплеях и у
клиентов состояние приходит через sync-event.

### 3.3 `century18` — переход в 18 век

| Значение | Что делает |
|---|---|
| 0 | Стандартно: апгрейд `<nat>cen.1` доступен после aca + tem + art (с обычной ценой). |
| 1 | Апгрейд `cen.1` отключён — 18 век недоступен в этой партии. |
| 2 | Игрок стартует в 18 веке — `cen.1` уже исследован. |

У наций без 18 в. (`ukr` Украина, `tur` Турция, `alg` Алжир) опция «Сразу»
бесполезна — у них нет апгрейда `cen.1` в `country.script`. См.
[`reference/05_upgrades.md`](../reference/05_upgrades.md).

### 3.4 `capture` — правила захвата

Геометрия захвата (радиусы, кто захватывается, кто нет, башни, стены) — в
[`recon/capture_mechanics.md`](capture_mechanics.md).

Опция `capture` в лобби только включает / отключает классы целей: `1` запрещает
захват крестьян, `2` ещё и Городских центров, `3` оставляет только захват
артиллерией. Сам алгоритм проверки одинаковый.

### 3.5 `marketdip` — рынок и дипцентр

`value = 4` («Дорогие наёмники») умножает цену найма на
`gc_gameplay_expensivemercskoef = 3`. Подробности про экономику дипцентра — в
[`recon/mercenaries_diplomacy.md`](mercenaries_diplomacy.md).

### 3.6 `gamespeed` — скорость партии

`gc_settings_gamespeed_0..2` (`dmscript.global:1025-1029`):

```pascal
gc_settings_gamespeed_count   = 3;
gc_settings_gamespeed_default = -1;
gc_settings_gamespeed_0       = 7;     // slow   — 7 тиков / реальная секунда
gc_settings_gamespeed_1       = 10;    // normal — 10 тиков / реальная секунда
gc_settings_gamespeed_2       = 14;    // fast   — 14 тиков / реальная секунда
//gc_settings_gamespeed_3 = 20;        // (закомментировано — был ultra-fast)
```

`gc_time_to_frames = 32` всегда (32 кадра в одной игровой секунде); меняется
только real-time-фактор.

| Скорость | Тиков / реальную секунду | Множитель | Реальное время на 1 игровую секунду |
|---:|---:|---:|---:|
| 0 (slow)   | 7  | ×0.7 | 1.43 реальных секунд |
| 1 (normal) | 10 | ×1.0 | 1.00 реальных секунд |
| 2 (fast)   | 14 | ×1.4 | 0.71 реальных секунд |

### 3.7 `limit` — лимит населения

Это **глобальный потолок поверх** локального лимита по зданиям:

```
pop_cap = cen × 100 + bar × 150 + ba2 × 250 + hou × 25
```

Глобальный потолок (`limit = 1..8` → 500 / 750 / 1000 / 1500 / 2200 / 3000 /
5000 / 8000) никогда не превышается, даже если ферм-бонус позволяет больше.

UI пишет значение через `randommap.settings.limit.custom = "%value% юнитов"` —
его подставляет `_misc_GetLimitText`.

### 3.8 `adviserassistant` — помощник

Контекстные подсказки в углу экрана. Не влияет на симуляцию — только UI.

## 4. Сложность ИИ — `gc_player_difficulty_*`

Из `dmscript.global:781-786`:

| `difficulty` | Локаль (gui) | Что значит | Множитель скорости |
|---:|---|---|---:|
| -1 | (none) | Нет AI | — |
| 0  | difficulty.1 | Easy / Лёгкий | 0.30 |
| 1  | difficulty.1 | Normal / Нормальный | 0.50 |
| 2  | difficulty.2 | Hard / Тяжёлый | 0.75 |
| 3  | difficulty.3 | Very Hard / Очень тяжёлый | 1.00 |
| 4  | difficulty.4 | Impossible / Невозможный | 1.25 |

Множитель применяется через `_player_GetDifficultyKoef` к скорости
постройки/найма у AI. **Стартовых ресурсов AI не получает** ни на какой
сложности. Подробнее — [`recon/ai_behavior.md`](ai_behavior.md).

См. также [`recon/mercenaries_diplomacy.md`](mercenaries_diplomacy.md) §3 — на
hard+ при `brebellion = True` шанс перехода наёмников ≈ 18.31% за тик
(значительно).

## 5. Глобальные константы партии

Из `dmscript.global` — это не лобби-опции, а константы движка, которые
определяют форму всех настроек.

| Константа | Значение | Что значит |
|---|---:|---|
| `gc_MaxPlayerCount` | 12 | Максимум игроков (включая нейтрала и слот наёмников). |
| `gc_MaxObjCount` | 32000 | Хард-кап юнитов на карте (все игроки вместе). |
| `gc_time_to_frames` | 32 | Кадров в одной игровой секунде. |
| `gc_buildtime_modifier` | 10 | Дополнительный множитель **только для зданий**: реальное время в g-секундах = `frames × 10 / 32`. У юнитов — без множителя. |
| `gc_resource_hitsneeded_food` | 22 | Ударов мотыгой до сдачи food. |
| `gc_resource_hitsneeded_wood` | 14 | Ударов топором до сдачи wood. |
| `gc_resource_hitsneeded_stone` | 20 | Ударов киркой до сдачи stone. |
| `gc_obj_resource_portion_food` | 45 | Еды за рейс при `eff = 100`. |
| `gc_obj_resource_portion_wood` | 28 | Дерева за рейс при `eff = 100`. |
| `gc_obj_resource_portion_stone` | 40 | Камня за рейс при `eff = 100`. |
| `gc_obj_speed_peasant` | 40 | Заявленная скорость крестьянина — но в `unit.script:1192` присвоение закомментировано (см. [`recon/peasant_extraction.md`](peasant_extraction.md) §9). |

## 6. Победа и поражение

См. отдельный документ — [`recon/victory_conditions.md`](victory_conditions.md).
Кратко: победа = «осталась только одна команда»; `farmused = 0` ⇒ поражение,
но `farmused` не падает в 0 пока есть хоть один крестьянин **или** Городской
центр. Wonder-побед в C3 нет, score копится только для статистики.
