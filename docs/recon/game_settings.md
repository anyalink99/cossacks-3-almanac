# Настройки игры

Полный справочник опций партии в Cossacks 3 — что выбирается в лобби и как каждая опция влияет на симуляцию. Источники:

- `data/scripts/dmscript.global` — все `gc_mapsettings_*` константы (строки 1025-1098).
- `data/scripts/lib/classes.script:58-83` — структуры `TMapSettings.gen` и `TMapSettings.additional`.
- `data/scripts/common.inc/{dogenerate.inc,initmapgen.inc,initmap.inc}` — где значения применяются.
- `data/scripts/lib/misc.script:_misc_GetPeaceTime` — декодирование peacetime.
- `data/locale/{en,ru}/gui.txt` — лейблы для UI (`@randommap.*`).

Все значения — из конкретных строк скриптов; в случае правок патчем числа надо перепроверить.

---

## 1. Структура: `TMapSettings`

В `classes.script:85-88`:

```pascal
type TMapSettings = class
   gen : TMapSettingsGen;          // параметры генератора карты
   additional : TMapSettingsAdditional;  // правила игры (peacetime, capture, …)
end;
```

`gen` решает **как** рисуется карта (рельеф, размер, ресурсы, сезон), `additional` — **по каким правилам** идёт партия. Хранится в save-файле через `_misc_SaveLanRoomData` (`miscext2.script:2360-2380`).

---

## 2. Генератор карты — `gMap.settings.gen`

Поля структуры (`classes.script:74-83`):

```pascal
type TMapSettingsGen = class
   randkey0 : Integer;        // RNG seed для размещения (mines/forests/stones)
   randkey1 : Integer;        // RNG seed для рельефа/ландшафта
   mapsize : Integer;         // 0..3 — размер
   terraintype : Integer;     // 0..9 — тип ландшафта/воды
   relieftype : Integer;      // 0..5 — тип рельефа
   resourcestart : Integer;   // 0..3 — стартовые ресурсы
   resourcemines : Integer;   // 0..2 — плотность шахт
   season : Integer;          // 0..3 — сезон/декорации
end;
```

### 2.1 `mapsize` — размер карты

Извлечено из `miscext2.script:19-26`. Значение задаёт ширину карты в тайлах; высота равна ширине (карта квадратная).

| `mapsize` | Размер (тайлы) | Привычное название |
|---|---:|---|
| 0 | 320 × 320 | Стандартная |
| 1 | 480 × 480 | Большая |
| 2 | 640 × 640 | Огромная |
| 3 | 256 × 256 | Маленькая (Tiny) |

Локали в `gui.txt` отдельных лейблов нет — UI хардкодит. Замеры в репозитории (`replay_aggregates`) делались на 256×256 (Tiny) и 480×480 (Big).

### 2.2 `terraintype` — тип ландшафта/воды

Из `gui.txt @randommap.terraintype.{0..9}`:

| `terraintype` | en | ru | Что значит |
|---|---|---|---|
| 0 | Land | Земля | Без воды, чисто суша |
| 1 | Mediterranean | Средиземноморье | Внутреннее море с островами |
| 2 | Peninsulas | Полуострова | Сушевые выступы в воду |
| 3 | Islands | Острова | Большие острова, разделённые морем |
| 4 | Several Continents | Несколько континентов | Большие материки + узкие проливы |
| 5 | Single Continent | Один континент | Один большой материк, океан вокруг |
| 6 | Lakes | Озёра | Внутренние водоёмы на суше |
| 7 | Coast | Побережье | Море с одной стороны |
| 8 | Rivers | Реки | Реки делят сушу |
| 9 | Without water | Без воды | Полный синоним 0 (legacy) |

Mapping в `_misc_HasMaritime` (`misc.script:5466`): `terraintype>=2 and terraintype<=4` → есть «морские» воды (peninsulas/islands/several_continents), требуется порт для доступа к воде.

Проверка `bDesert`: задаётся через `season`, не через terraintype (хотя в локали есть `relieftype.5 = Desert`).

### 2.3 `relieftype` — рельеф

Из `gui.txt @randommap.relieftype.{0..5}`:

| `relieftype` | en | ru |
|---|---|---|
| 0 | Plain | Равнина |
| 1 | Low Mountains | Низкие горы |
| 2 | High Mountains | Высокие горы |
| 3 | Highlands | Холмистая местность |
| 4 | Plateaus | Плато |
| 5 | Desert | Пустыня |

Дефолт в `initmap.inc:29` — **`relieftype := 3`** (Highlands).

**`foreststype` всегда = 0 на Land (terraintype=0)** — даже если игрок выбрал что-то другое в lobby (`dogenerate.inc:6`). На non-Land — в работу идёт выбранное.

### 2.4 `resourcestart` — стартовые ресурсы

`initmapgen.inc:166-189`:

```pascal
for j:=0 to gc_ResCount-1 do
case gMap.settings.gen.resourcestart of
   0: _res_SetResToPlayerByIndex(i, j, 1000);
   1: _res_SetResToPlayerByIndex(i, j, 4000);
   2: _res_SetResToPlayerByIndex(i, j, 5000);
   else  // 3+
   _res_SetResToPlayerByIndex(i, j, 1000000);
end;
```

| `resourcestart` | en | ru | Каждый ресурс |
|---|---|---|---:|
| 0 | Normal | Стандарт | **1 000** |
| 1 | Rich | Богато | **4 000** |
| 2 | Thousands | Тысячи | **5 000** |
| 3 | Millions | Миллионы | **1 000 000** |

Все 7 ресурсов (none/food/wood/stone/gold/iron/coal) получают одинаковое значение. Дефолт в `initmap.inc:30` = **2** (Тысячи / 5000). Дефолт в `map.script:252` (новая карта) — тоже 2.

### 2.5 `resourcemines` — плотность шахт

Из `gui.txt @randommap.minerals.{0..2}`:

| `resourcemines` | en | ru |
|---|---|---|
| 0 | Poor | Бедно |
| 1 | Medium | Средне |
| 2 | Rich | Богато |

Влияет на `minesdensity` в `dogenerate.inc:1544`. Конкретные числа шахт за уровень — в [`map_generation_pipeline.md`](map_generation_pipeline.md) (для Land-Highlands-Rich подсчитано: ~12 шахт на игрока @ Rich, Tiny). Дефолт `initmap.inc:31` = **1** (Medium).

### 2.6 `season` — сезон

Из кода (нет en/ru-локали — UI хардкод). Значение влияет на текстуры/декорации, и единственный flag-effect: `season=3` → пустыня (форсированный bDesert).

| `season` | Что делает |
|---|---|
| 0 | Лето (default) |
| 1 | Осень |
| 2 | Зима |
| 3 | Пустыня (`bDesert=True`, отдельный набор pattern types: `desert_*`) |

`dogenerate.inc:4` — `bDesert = (gMap.settings.gen.season=3)`. На пустыне другие brushes/паттерны для леса (`forests_pinefir_*` → `desert_forests_*`).

### 2.7 `randkey0` / `randkey1` — RNG seeds

`randkey1` используется для рельефа (`SetRandomKey(gMap.settings.gen.randkey1)` — много раз в `dogenerate.inc`). `randkey0` — для placement (`generatemap.inc:142`).

**Ключевая идея:** при одинаковых `(inputbitmap, randkey0, randkey1)` карта детерминирована. См. [`map_generation_pipeline.md`](map_generation_pipeline.md) §12. В replay-формате эти ключи сохранены — поэтому реплеи воспроизводят ту же карту.

---

## 3. Правила игры — `gMap.settings.additional`

Поля (`classes.script:58-72`):

```pascal
type TMapSettingsAdditional = class
   activeoption : Integer;
   startingunits : Integer;        // что добавлено в стартовый отряд
   balloon : Integer;              // воздушные шары
   cannons : Integer;              // пушки/стены/башни
   peacetime : Integer;            // время ненападения
   century18 : Integer;            // переход в 18 век
   capture : Integer;              // правила захвата
   marketdip : Integer;            // рынок/дипцентр
   teams : Integer;                // командное расположение
   autosave : Integer;             // автосохранение
   limit : Integer;                // лимит населения
   gamespeed : Integer;            // скорость партии
   adviserassistant : Integer;     // помощник-советник
end;
```

### 3.1 `startingunits` — стартовая армия

Из `dmscript.global:1032-1045` и `gui.txt @randommap.settings.startingunits.*`:

| `startingunits` | en | ru | Что добавляет |
|---|---|---|---|
| 0 | Default | По умолчанию | только базовые 18 крестьян (см. §3.1.1) |
| 1 | Army | Маленькая армия | +1000 food + малый отряд (P/X/B/O паттерн) |
| 2 | Big Army | Средняя армия | средний отряд |
| 3 | Huge Army | Большая армия | большой отряд |
| 4 | Army of Peasants | Слот крестьян | дополнительные крестьяне (без боевых) |
| 5 | Different Nations | Разные нации | стартовый набор разнонациональных юнитов |
| 6 | Towers | Башни | + башни |
| 7 | Cannons | Пушки | + пушки |
| 8 | Cannons and Howitzers | Пушки и гаубицы | + пушки и гаубицы |
| 9 | 18th Century Barracks | Казарма 18 в. | стартует с казармой 18в. построенной |
| 10 | (нет в локали) | Казарма 17в. | стартует с казармой 17в. |
| 11 | (нет в локали) | Деревня | домики/крестьяне в виде деревни |
| 12 | (нет в локали) | Срубы | log cabins |
| 13 | (нет в локали) | Уния | union variant |

Конфигурация каждого варианта в `data/game/var/startingsettings.cfg` — для каждого `startid` своя секция: `addresources` (доп. ресурсы), `countries` (legend pattern для размещения юнитов в виде P=peasant / X=infantry / B=drummer / O=officer / Q,W=mission-buildings и т. д.).

#### 3.1.1 Базовые 18 крестьян

Независимо от `startingunits`, движок всегда запускает `CreateStartPointPeasants` (`dogenerate.inc:1231-1281`), который размещает **18 крестьян** в **6×3 grid** вокруг стартовой точки, с радиусом 0.75 тайла. Это игровой default; даже на `startingunits=0` (Default) у игрока сразу 18 крестьян.

### 3.2 `balloon` — воздушные шары

| `balloon` | en | ru |
|---|---|---|
| 0 | Default | По умолчанию (включены) |
| 1 | No Balloons | Без воздушных шаров |
| 2 | Balloons | С воздушными шарами |

Воздушный шар — особый юнит, повторяющий vision на большой высоте.

### 3.3 `cannons` — пушки/стены/башни

| `cannons` | en | ru |
|---|---|---|
| 0 | Default | По умолчанию |
| 1 | No Cannons, Towers and Walls | Без пушек, башен и стен |
| 2 | Expensive Cannons | Дорогие пушки |

`expensivecannons` повышает цену пушек (точные множители — в `country.script` upgrade hooks; коэффициент проверить эмпирически).

### 3.4 `peacetime` — время ненападения

Из `_misc_GetPeaceTime` (`misc.script:4262-4282`):

```pascal
function _misc_GetPeaceTime(ind : Integer) : Float;
begin
   case ind of
      0  : Result := 0;     //  default — без peacetime
      1  : Result := 10;    //  10 минут
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
   Result := Result * 60;   // в g-секундах
end;
```

| `peacetime` | en | ru | Минут | g-сек |
|---|---|---|---:|---:|
| 0 | No Peace Time | Без ненападения | 0 | 0 |
| 1 | 10 min | 10 мин | 10 | 600 |
| 2 | 20 min | 20 мин | 20 | 1200 |
| 3 | 30 min | 30 мин | 30 | 1800 |
| 4 | 45 min | 45 мин | 45 | 2700 |
| 5 | 60 min | 60 мин | 60 | 3600 |
| 6 | 1.5 hours | 1.5 часа | 90 | 5400 |
| 7 | 2 hours | 2 часа | 120 | 7200 |
| 8 | 3 hours | 3 часа | 180 | 10800 |
| 9 | 4 hours | 4 часа | 240 | 14400 |
| 10 | (зарезервировано) | — | — | — |
| 11 | 15 min | 15 мин | 15 | 900 |

> ⚠ Минуты — **игровое время** (g-минуты). На fast (×1.4) одна g-минута = 60/1.4 ≈ 42.9 real-секунд. Т.е. 10-минутный peacetime реально длится ~7 real-min.

#### 3.4.1 Как работает peacetime

При генерации карты:
- `gbool_peacemode := (peacetime != 0)` — флаг включён, если выбран любой ненулевой пресет (`dogenerate.inc:2060`).
- `gfloat_peacetime := _misc_GetPeaceTime(ind)` — конкретное значение в g-сек.
- `SetupBorderObjects` создаёт визуальные «границы» вокруг каждого игрока (`dogenerate.inc:2065`).

Во время `gbool_peacemode = True`:
- **Поиск врагов запрещён.** В `_unit_SearchEnemy*` (`unit.script:5516`) проверяется `bpeacetime` — если True, ни один юнит не находит врагов и не атакует.
- **Сетка владения территорией.** `_misc_IsCorrectScanCellOwner` (`misc.script:2424`) возвращает True только если ячейка ничейная или твоя — враги не могут зайти на твою территорию.
- **Захват зданий запрещён** на чужой территории.

Каждый Nothing-tick (`progress/nothing.inc:658`) проверяется:

```pascal
if (gbool_peacemode) and (gametime > gfloat_peacetime) and (not _net_IsReplay) and (not _net_IsClient) then
begin
   gbool_peacemode := false;
   // удалить ptborder-объекты, перейти к войне
end;
```

Только сервер (host в MP, single-player) принимает решение о завершении peacetime. В реплеях / у клиентов состояние приходит через sync-event.

### 3.5 `century18` — переход в 18 век

| `century18` | en | ru | Что делает |
|---|---|---|---|
| 0 | Default | По умолчанию | Переход доступен через апгрейд Городского центра `<nat>cen.1` (стандартная цена) |
| 1 | Never | Никогда | Апгрейд `cen.1` отключён, 18в. недоступен на этой карте |
| 2 | Immediately | Сразу | Игрок стартует в 18в. (cen.1 уже исследован) |

Для 17в.-only наций (ukr/tur/alg) опция «Сразу» бесполезна — у них нет `cen.1` (см. [`reference_strategy_stack`](../../docs/reference/05_upgrades.md) и `country.script` для конкретных наций).

### 3.6 `capture` — правила захвата

| `capture` | en | ru |
|---|---|---|
| 0 | Default | По умолчанию |
| 1 | No Capturing Peasants | Нельзя захватывать крестьян |
| 2 | No Capturing Peasants or Centres | Нельзя захватывать крестьян и Городские центры |
| 3 | Artillery Only | Захват только артиллерией |

Подробности геометрии захвата — [`capture_mechanics.md`](capture_mechanics.md). Дефолт допускает захват любых зданий и юнитов (включая крестьян).

### 3.7 `marketdip` — рынок и дипцентр

| `marketdip` | en | ru | Эффект |
|---|---|---|---|
| 0 | Default | По умолчанию | Оба здания доступны |
| 1 | Without dip. center | Без дипцентра | Дипцентр нельзя строить |
| 2 | Without market | Без рынка | Рынок нельзя строить |
| 3 | Without both | Без обоих | Ни рынок, ни дипцентр не строятся |
| 4 | Expensive Mercenaries | Дорогие наёмники | Цена золота наёмников × **3** (`gc_gameplay_expensivemercskoef=3`) |

Подробности про наёмников — [`mercenaries_diplomacy.md`](mercenaries_diplomacy.md).

### 3.8 `teams` — расположение команд

| `teams` | en | ru |
|---|---|---|
| 0 | Default | По умолчанию (стартовые позиции по жребию) |
| 1 | Nearby | Команды стартуют рядом |

При `teams=1` союзники по команде спавнятся в соседних стартовых позициях, а не разбросанно.

### 3.9 `limit` — лимит населения

Из `dmscript.global:1089-1098`:

| `limit` | Лимит юнитов |
|---|---:|
| 0 (default) | по умолчанию (зависит от карты) |
| 1 | 500 |
| 2 | 750 |
| 3 | 1 000 |
| 4 | 1 500 |
| 5 | 2 200 |
| 6 | 3 000 |
| 7 | 5 000 |
| 8 | 8 000 |

Это **глобальный потолок поверх** локального cap'а, считаемого по зданиям: `pop_cap = cen × 100 + bar × 150 + ba2 × 250 + hou × 25`. Глобальный потолок никогда не превышается, даже если ферма допускает больше.

В UI сообщение `randommap.settings.limit.custom = "%value% units"` — позволяет видеть число для текущего пресета.

### 3.10 `gamespeed` — скорость партии

Из `dmscript.global:1025-1029`:

```pascal
gc_settings_gamespeed_count = 3;
gc_settings_gamespeed_default = -1;
gc_settings_gamespeed_0 = 7;     // slow — 7 ticks/real-sec
gc_settings_gamespeed_1 = 10;    // normal — 10 ticks/real-sec
gc_settings_gamespeed_2 = 14;    // fast — 14 ticks/real-sec
//gc_settings_gamespeed_3 = 20;  // (закомментировано — был ultra-fast)
```

| `gamespeed` | tick/real-sec | g-sec / real-sec | Реальное время за 1 g-сек |
|---|---:|---:|---:|
| 0 | 7  | ×0.7 | 1.43 real-сек |
| 1 | 10 | ×1.0 | 1.00 real-сек |
| 2 | 14 | ×1.4 | 0.71 real-сек |

`gc_time_to_frames=32` всегда (32 frame/g-sec); меняется только real-time-факторное scaling. Слот 3 (×2.0) был, но отключён в текущей версии.

### 3.11 `adviserassistant` — помощник-советник

| `adviserassistant` | en | ru |
|---|---|---|
| 0 | Default | По умолчанию |
| 1 | Without adviser | Без советника |

Контекстные подсказки в углу экрана. Не влияет на симуляцию — только UI.

---

## 4. Сложность ИИ — `gc_player_difficulty_*`

Из `dmscript.global:781-786`:

| `difficulty` | Локаль (gui.difficulty.X) | en | Множитель скорости (`_player_GetDifficultyKoef`) |
|---|---|---|---:|
| -1 | (none) | None | — |
| 0 | difficulty.1 (sic) | Easy | 0.30 |
| 1 | difficulty.1 | Normal | 0.50 |
| 2 | difficulty.2 | Hard | 0.75 |
| 3 | difficulty.3 | Very Hard | 1.00 |
| 4 | difficulty.4 | Impossible | 1.25 |

Подробности AI — [`ai_behavior.md`](ai_behavior.md). Cheat'ы у ИИ только в скорости постройки/найма (множитель к buildtime), стартовых ресурсов **не получает** ни на одной сложности. См. также [`mercenaries_diplomacy.md`](mercenaries_diplomacy.md) §3 — на hard+ существенно (18.31% / тик) выше шанс перехода наёмников при `brebellion`.

---

## 5. Глобальные константы партии

Из `dmscript.global`:

| Константа | Значение | Что |
|---|---:|---|
| `gc_MaxPlayerCount` | 12 | Максимум игроков (включая нейтрала и mercenary) |
| `gc_MaxObjCount` | 32000 | Хард-кап юнитов на карте |
| `gc_time_to_frames` | 32 | Кадров/g-секунда |
| `gc_buildtime_modifier` | 10 | Дополнительный множитель только для зданий: `buildtime_g_sec = frames × 10/32` |
| `gc_resource_hitsneeded_food` | 22 | Удары мотыгой до сдачи food |
| `gc_resource_hitsneeded_wood` | 14 | Удары топором до сдачи wood |
| `gc_resource_hitsneeded_stone` | 20 | Удары киркой до сдачи stone |
| `gc_obj_resource_portion_food` | 45 | Сколько food принесёт крестьянин за рейс (eff=100) |
| `gc_obj_resource_portion_wood` | 28 | Сколько wood за рейс |
| `gc_obj_resource_portion_stone` | 40 | Сколько stone за рейс |
| `gc_obj_speed_peasant` | 40 | Скорость крестьянина (объявлено; присвоение в коде закомментировано — см. extraction_model плана) |

---

## 6. Победа / поражение

См. отдельный документ — [`victory_conditions.md`](victory_conditions.md).
TL;DR: победа = last team standing. `farmused == 0` ⇒ defeat, но `farmused` не падает в 0 пока есть хоть один peasant ИЛИ Городской центр. Wonder-победы в C3 нет. Score копится для статистики, не для победы.
