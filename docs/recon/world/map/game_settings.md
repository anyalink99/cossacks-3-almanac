# Как настройки матча влияют на игру

[← Как устроена игра](../../README.md)

Этот документ — **handwritten reverse-engineering** того, как движок Cossacks 3
реагирует на выбор игрока в лобби. Сюда не выносятся значения и лейблы — для
этого есть две точки правды:

- **[`docs/reports/map/lobby_settings.md`](../../../reports/map/lobby_settings.md)** —
  готовый справочник всех опций (названия из локали, числовые значения,
  значения по умолчанию).
- **[`derived/game_settings.json`](../../../../derived/game_settings.json)** — то же
  самое в машинно-читаемом виде, для редактора и инструментов.

Здесь — только то, что нельзя увидеть в таблице: какие функции скриптов читают
эти значения, какие флаги выставляют, какие игровые механики при этом
включаются. Все ссылки на код и Pascal-блоки собраны в разделе
[Источники](#источники) в конце документа.

## 1. Структура `TMapSettings`

Корневая структура содержит два поля: `gen` и `additional` [^1]. `gen` решает,
**как** рисуется карта (рельеф, размер, ресурсы, сезон), `additional` — **по
каким правилам** идёт партия (peacetime, лимит, скорость, помощник). Содержимое
сохраняется в save через `_misc_SaveLanRoomData` [^2].

`TMapSettingsGen` содержит ключи RNG (`randkey0` для расстановки, `randkey1`
для рельефа), `mapsize` (0..3), `terraintype` (0..9), `relieftype` (0..5),
`resourcestart` (0..3), `resourcemines` (0..2), `season` (0..3) [^3].

`TMapSettingsAdditional` содержит `activeoption`, `startingunits`, `balloon`,
`cannons`, `peacetime`, `century18`, `capture`, `marketdip`, `teams`,
`autosave`, `limit`, `gamespeed`, `adviserassistant` [^4].

Числовые значения и человеческие названия — в
[`reports/map/lobby_settings.md`](../../../reports/map/lobby_settings.md). Здесь — что
именно читает движок.

## 2. Что движок делает с `gen`-параметрами

| Поле | Где применяется | Что делает |
|---|---|---|
| `mapsize` | [^5] | Задаёт `Width × Height` карты в тайлах (карта квадратная). Влияет на плотность размещения и `prob*` модификаторы [^6]. |
| `terraintype` | [^7] | Выбирает таблицу масок (`data/gen/terrainmasks/`) для базового изображения карты. `terraintype ∈ {2,3,4}` (Полуострова / Острова / Континенты) включает «морские» воды — без `por` (порт) к ним нельзя добраться. |
| `relieftype` | [^8] | Выбирает плотность гор/холмов (`mnt`, `hgh`). На `relieftype = 3` («Высокогорье») плотность гор максимальная — меньше ровных площадей под фермы и склады. |
| `resourcestart` | [^9] | Цикл по 6 ресурсам — каждому игроку даёт стартовое количество **каждого** из 6 ресурсов. Значения по `resourcestart`: 1000 / 4000 / 5000 / 1 000 000. |
| `resourcemines` | [^10] | Подставляется в `minesdensity` — управляет фазой размещения шахт. См. [`map_generation_pipeline.md`](map_generation_pipeline.md) §8 (3 раунда × 3 типа = 9 месторождений на игрока для Tiny + Rich). |
| `season` | [^11] | `bDesert := (season = 3)`. Этот флаг переключает набор pattern-типов (`forests_pinefir_*` → `desert_forests_*` и т. д.). Прочие сезоны меняют только текстуры. |
| `randkey0` / `randkey1` | [^12] | RNG-ключи. `randkey1` используется для рельефа (`SetRandomKey`), `randkey0` — для расстановки. **Тройка `(inputbitmap, randkey0, randkey1)` детерминирует карту** — поэтому реплеи воспроизводят ту же карту. Подробнее — [`map_generation_pipeline.md` §12](map_generation_pipeline.md#12-seed-space). |

> **`foreststype` и Land.** Игрок выбирает `foreststype` в lobby, но на
> `terraintype = 0` (Суша) движок немедленно перезаписывает его в `0` [^13].
> На non-Land картах выбор работает.

## 3. Что движок делает с `additional`-параметрами

### 3.1 `startingunits` — стартовая армия

Конкретный набор юнитов / зданий для каждого варианта читается из
`data/game/var/startingsettings.cfg`. Поля: `addresources` (доп. ресурсы),
`countries` (легенда расстановки: `P` = крестьянин, `X` = пехотинец, `B` =
барабанщик, `O` = офицер, `Q`/`W` = mission-здания и т. д.).

> **Базовые 18 крестьян появляются всегда.** Независимо от выбора движок
> вызывает `CreateStartPointPeasants` и расставляет **18 крестьян** в сетке
> 6×3 вокруг стартовой точки с радиусом 0.75 тайла [^14]. Даже на «По
> умолчанию» у игрока сразу 18 крестьян.

### 3.2 `peacetime` — как устроен мир

Функция `_misc_GetPeaceTime` декодирует индекс в игровые минуты и умножает на
60, чтобы получить g-секунды [^15]:

| `ind` | Игровые минуты |
|---:|---:|
| 0 | 0 (No peace time) |
| 1 | 10 |
| 2 | 20 |
| 3 | 30 |
| 4 | 45 |
| 5 | 60 |
| 6 | 90 |
| 7 | 120 |
| 8 | 180 |
| 9 | 240 |
| 11 | 15 |

Минуты — **игровые**: на скорости fast (`gamespeed = 2`) одна игровая минута
≈ 42.9 реальных секунд, и 10-минутный мир длится ≈ 7 реальных минут.

При генерации карты [^16]:

- `gbool_peacemode := (peacetime <> 0)` — флаг включается, если выбран любой
  ненулевой пресет.
- `gfloat_peacetime := _misc_GetPeaceTime(ind)` — конкретное значение в
  игровых секундах.
- `SetupBorderObjects` создаёт визуальные «границы» вокруг каждого игрока.

Пока `gbool_peacemode = True`:

- **Поиск врагов запрещён.** В `_unit_SearchEnemy*` проверяется `bpeacetime`
  — если `True`, ни один юнит не находит врагов и не атакует [^17].
- **Сетка владения территорией.** `_misc_IsCorrectScanCellOwner` возвращает
  `True` только для ничейных и собственных ячеек — враги не могут зайти на
  твою территорию [^18].
- **Захват зданий запрещён** на чужой территории.

Каждый Nothing-tick сервер проверяет окончание мира [^19]: если
`gbool_peacemode = True` и `gametime > gfloat_peacetime`, и при этом партия не
реплей и не клиент — флаг сбрасывается, `ptborder`-объекты удаляются, и партия
переходит в военный режим. Решение принимает только сервер (host в MP,
single-player). В реплеях и у клиентов состояние приходит через sync-event.

### 3.3 `century18` — переход в 18 век

| Значение | Что делает |
|---|---|
| 0 | Стандартно: апгрейд `<nat>cen.1` доступен после aca + tem + art (с обычной ценой). |
| 1 | Апгрейд `cen.1` отключён — 18 век недоступен в этой партии. |
| 2 | Игрок стартует в 18 веке — `cen.1` уже исследован. |

У наций без 18 в. (`ukr` Украина, `tur` Турция, `alg` Алжир) опция «Сразу»
бесполезна — у них нет апгрейда `cen.1` в `country.script`. См.
[`reference/05_upgrades/README.md`](../../../reference/05_upgrades/README.md).

### 3.4 `capture` — правила захвата

Геометрия захвата (радиусы, кто захватывается, кто нет, башни, стены) — в
[`recon/world/economy/capture_mechanics.md`](../economy/capture_mechanics.md).

Опция `capture` в лобби только включает / отключает классы целей: `1` запрещает
захват крестьян, `2` ещё и Городских центров, `3` оставляет только захват
артиллерией. Сам алгоритм проверки одинаковый.

### 3.5 `marketdip` — рынок и дипцентр

`value = 4` («Дорогие наёмники») умножает цену найма на
`gc_gameplay_expensivemercskoef = 3`. Подробности про экономику дипцентра — в
[`recon/systems/mercenaries_diplomacy.md`](../../systems/mercenaries_diplomacy.md).

### 3.6 `gamespeed` — скорость партии

Константы `gc_settings_gamespeed_*` задают число тиков на реальную секунду:
`slow = 7`, `normal = 10`, `fast = 14`; четвёртое значение `20` (ultra-fast) в
коде закомментировано [^20]. `gc_time_to_frames = 32` всегда (32 кадра в одной
игровой секунде); меняется только real-time-фактор.

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

Перечислены константы `gc_player_difficulty_*` от `-1` до `4` [^21]:

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
сложности. Подробнее — [`recon/systems/ai_behavior.md`](../../systems/ai_behavior.md).

См. также [`recon/systems/mercenaries_diplomacy.md`](../../systems/mercenaries_diplomacy.md) §3 — на
hard+ при `brebellion = True` шанс перехода наёмников ≈ 18.31% за тик
(значительно).

## 5. Глобальные константы партии

Это не лобби-опции, а константы движка, которые определяют форму всех
настроек [^22].

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
| `gc_obj_speed_peasant` | 40 | Заявленная скорость крестьянина — но в скрипте присвоение закомментировано [^23] (см. [`recon/world/economy/peasant_extraction.md`](../economy/peasant_extraction.md) §9). |

## 6. Победа и поражение

См. отдельный документ — [`recon/systems/victory_conditions.md`](../../systems/victory_conditions.md).
Кратко: победа = «осталась только одна команда»; `farmused = 0` ⇒ поражение,
но `farmused` не падает в 0 пока есть хоть один крестьянин **или** Городской
центр. Wonder-побед в C3 нет, score копится только для статистики.

---

## Источники

Все ссылки относительно `data/scripts/` в установке Cossacks 3. Номера строк —
из текущих файлов установки; после патча игры перепроверять.

[^1]: Корневая структура `TMapSettings` — `lib/classes.script:85-88`:

    ```pascal
    type TMapSettings = class
       gen        : TMapSettingsGen;          // параметры генератора карты
       additional : TMapSettingsAdditional;   // правила игры
    end;
    ```

[^2]: Сериализация настроек в save-файл — `_misc_SaveLanRoomData` в
    `lib/miscext2.script:2360-2380`.

[^3]: `TMapSettingsGen` — `lib/classes.script:74-83`:

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

[^4]: `TMapSettingsAdditional` — `lib/classes.script:58-72`:

    ```pascal
    type TMapSettingsAdditional = class
       activeoption     : Integer;
       startingunits    : Integer;   // стартовый набор юнитов / зданий
       balloon          : Integer;   // монгольфьеры
       cannons          : Integer;   // пушки / стены / башни
       peacetime        : Integer;   // время мира
       century18        : Integer;   // переход в 18 век
       capture           : Integer;  // правила захвата
       marketdip        : Integer;   // рынок / дипцентр
       teams            : Integer;   // расположение союзников
       autosave         : Integer;
       limit            : Integer;   // лимит населения
       gamespeed        : Integer;   // скорость партии
       adviserassistant : Integer;   // помощник
    end;
    ```

[^5]: Применение `mapsize` — `common.inc/dogenerate.inc:1530-1545`.

[^6]: Модификаторы плотности `prob*` от размера карты —
    `lib/misc.script:3929-3941`.

[^7]: Применение `terraintype` — `common.inc/dogenerate.inc:1500-1530`;
    проверка наличия моря — `_misc_HasMaritime` в `lib/misc.script:5466`.

[^8]: Применение `relieftype` — `common.inc/dogenerate.inc:1640-1660`.

[^9]: Применение `resourcestart` — `common.inc/initmapgen.inc:166-189`:

    ```pascal
    for j := 0 to gc_ResCount - 1 do
       _res_SetResToPlayerByIndex(i, j, ...);
    ```

[^10]: Применение `resourcemines` — `common.inc/dogenerate.inc:1544`,
    подставляется в `minesdensity`.

[^11]: Применение `season` — `common.inc/dogenerate.inc:4`:

    ```pascal
    bDesert := (season = 3);
    ```

[^12]: RNG-ключи `randkey0` / `randkey1` — `common.inc/generatemap.inc:142` и
    многократно в `common.inc/dogenerate.inc`.

[^13]: Перезапись `foreststype` на Land — `common.inc/dogenerate.inc:5-6`.

[^14]: Расстановка стартовых крестьян — `CreateStartPointPeasants` в
    `common.inc/dogenerate.inc:1231-1281`.

[^15]: Декодирование `peacetime` в игровые секунды —
    `lib/misc.script:4262-4282`:

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

[^16]: Инициализация peacetime при генерации — `common.inc/dogenerate.inc:2060`
    (`gbool_peacemode := (peacetime <> 0)`) и
    `common.inc/dogenerate.inc:2065` (`SetupBorderObjects`).

[^17]: Блокировка поиска врагов в peacetime — `lib/unit.script:5516`,
    проверка флага `bpeacetime` в `_unit_SearchEnemy*`.

[^18]: Запрет чужой территории в peacetime — `_misc_IsCorrectScanCellOwner` в
    `lib/misc.script:2424`.

[^19]: Окончание peacetime на Nothing-tick'е —
    `progress/nothing.inc:658`:

    ```pascal
    if (gbool_peacemode) and (gametime > gfloat_peacetime)
       and (not _net_IsReplay) and (not _net_IsClient) then
    begin
       gbool_peacemode := false;
       // удалить ptborder-объекты, перейти к войне
    end;
    ```

[^20]: Константы скорости партии — `dmscript.global:1025-1029`:

    ```pascal
    gc_settings_gamespeed_count   = 3;
    gc_settings_gamespeed_default = -1;
    gc_settings_gamespeed_0       = 7;     // slow   — 7 тиков / реальная секунда
    gc_settings_gamespeed_1       = 10;    // normal — 10 тиков / реальная секунда
    gc_settings_gamespeed_2       = 14;    // fast   — 14 тиков / реальная секунда
    //gc_settings_gamespeed_3 = 20;        // (закомментировано — был ultra-fast)
    ```

[^21]: Константы сложности AI — `dmscript.global:781-786`.

[^22]: Глобальные константы партии — `dmscript.global` (раздел констант
    игрового времени и кадровой развёртки, рядом со `gc_settings_gamespeed_*`).

[^23]: Закомментированное присвоение `speed` крестьянину —
    `lib/unit.script:1192`.
