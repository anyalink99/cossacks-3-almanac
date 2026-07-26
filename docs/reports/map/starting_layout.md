# Cossacks 3 — Starting layout

**Производный** файл (расчётный, не извлечение). Считается из `data/scripts/common.inc/dogenerate.inc` и `data/game/var/startingsettings.cfg` скриптом [`compute/compute_starting_layout.py`](../../../compute/compute_starting_layout.py).

## §1. Расстановка крестьян (режим default)

Расстановка делается в `CreateStartPointPeasants` [^1].

- **18 крестьян** спавнятся в сетке **6×3** (`i div 3`, `i mod 3`)
- Шаг между крестьянами: `cUnitR = 0.75` тайла
- Сетка центрирована на старт-точке: суммарно `(6×0.75) × (3×0.75) = 4.5×2.25` тайла
- Случайное смещение каждого крестьянина: ±0.125 тайла по обеим осям
- Уникальный sid крестьянина берётся из `gCountry[cid].members[]` по первому юниту с `usage = gc_obj_usage_peasant` (например `peaaus` у Австрии, `peaeng` у Англии, и т.п.)

**На практике:** при старте у тебя горка из 18 крестьян занимает примерно `5×3` тайла, что укладывается во внутренний круг очистки `cCircle1` (см. §2). Ничего другого там не спавнится — это безопасный «дом» для первой минуты.

## §2. Кольца спавна ресурсов вокруг старт-точки

Расстановку колец делает `SetupStartingResources` [^2].

Вокруг каждой старт-точки игрока — три эллипса (X-радиус × Y-радиус, тайлы):

| Кольцо | X-радиус | Y-радиус | Что спавнится на границе |
| --- | ---: | ---: | --- |
| Inner (`cCircle1`) | 5 | 7 | очищается, ресурсы НЕ спавнятся (только крестьяне) |
| Mid (`cCircle2`) | 12 | 15 | 1× stoneforests + 1× stones (камни) у внутренней границы |
| — _между mid+4 и outer_ | — | — | дополнительные 2× forests + 1× stones (камни) |
| Outer (`cCircle3`) | 22 | 18 | 1× forest у границы (затем маска заполняется) |

**Алгоритм спавна** (`for [MAIN]i:=0 to 127 do begin … VectorRotateY(px, …, angle); _misc_CheckStandPattern… end`): в каждом «кольце» — 128 попыток × 3 под-попытки найти валидную позицию под выбранный паттерн. Угол `angle` — `RandomExt × 360°`. Дистанция от центра — `mindst + RandomExt × N + (i+j) × 0.5` тайла. Это значит:

- **Inner stoneforest:** дистанция ~5-8 тайл
- **Inner stones:** дистанция ~5-8 тайл (отдельный random angle, может быть с обратной стороны)
- **Mid forests** (×2): дистанция ~12-18 тайл (mindst=12, +2 random)
- **Mid stones:** дистанция ~16-22 тайл (mindst=12+4=16, +2 random)
- **Outer forest:** дистанция ~22-28 тайл

Тип леса определяется параметром `foreststype` в настройках генерации карты: 0 = pinefir/spruce/pine (хвойные, 7 вариантов), 1 = leaf (лиственные), 2 = mixed (смешанные). В desert-картах вместо forests используются паттерны `desert_forests_*`.

Шахты (gold / iron / coal) — отдельная функция `SetupMines` [^3]. Спавн шахт идёт по другой логике (раундами по дистанции, см. [recon/world/economy/peasant_extraction.md](../../recon/world/economy/peasant_extraction.md) §8.3 + [recon/world/map/map_generation_pipeline.md](../../recon/world/map/map_generation_pipeline.md) §8).

## §3. Пресеты стартовых юнитов

Источник пресетов — `data/game/var/startingsettings.cfg` + enum `gc_mapsettings_startingunits_*` [^4]. Все 14 пресетов с каноничными русскими названиями — [`lobby_settings.md`](lobby_settings.md). Поведение движка (как добавляются юниты и ресурсы) — [`recon/world/map/game_settings.md`](../../recon/world/map/game_settings.md) §3.1.

Игрок выбирает один из этих режимов в лобби. **default** (id=0) — это то, что описано в §1 (просто 18 крестьян, никаких добавочных ресурсов или юнитов). Остальные режимы добавляют ресурсы и/или дополнительные юниты + здания (через сложные ASCII-маски в cfg-файле).

**Сводка по startid → пресет → стартовые ресурсы (поверх default):**

| startid | preset | dataversion | +F | +W | +S | +G | +I | +C |
| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| -1 | (шаблон — не выбирается) | — | 0 | 0 | 0 | 0 | 0 | 0 |
| 0 | default | — | 0 | 0 | 0 | 0 | 0 | 0 |
| 1 | armysmall | 60…1000 | 1000 | 0 | 0 | 0 | 0 | 0 |
| 1 | armysmall | 0…59 | 1000 | 0 | 0 | 0 | 0 | 0 |
| 2 | armymedium | 60…1000 | 20000 | 0 | 0 | 0 | 0 | 0 |
| 2 | armymedium | 0…59 | 20000 | 0 | 0 | 0 | 0 | 0 |
| 3 | armylarge | 60…1000 | 20000 | 0 | 0 | 0 | 6000 | 9000 |
| 3 | armylarge | 0…59 | 20000 | 0 | 0 | 0 | 6000 | 9000 |
| 4 | peasantslot | 60…1000 | 20000 | 0 | 0 | 0 | 6000 | 9000 |
| 4 | peasantslot | 0…59 | 20000 | 0 | 0 | 0 | 6000 | 9000 |
| 5 | differentnations | — | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 |
| 6 | towers | — | 20000 | 0 | 0 | 0 | 6000 | 9000 |
| 7 | cannons | — | 20000 | 0 | 0 | 1000 | 6000 | 9000 |
| 8 | cannonsandhowitzers | — | 20000 | 0 | 0 | 1000 | 6000 | 9000 |
| 9 | barrack18 | — | 65000 | 2000 | 2000 | 15000 | 6000 | 9000 |
| 10 | barrack17 | — | 5000 | 1000 | 1000 | 2500 | 3000 | 3000 |
| 11 | village | — | 1000 | 1000 | 1000 | 1000 | 2500 | 2500 |
| 12 | logcabins | — | 0 | 0 | 0 | 0 | 2500 | 2500 |
| 13 | union | — | 1000 | 0 | 0 | 0 | 0 | 0 |

**Замечания:**
- Ресурсы — это **прибавка** к стандартным стартовым 0/0/0/0/0/0. Игроки начинают ровно с этими числами на счётчиках.
- `dataversion` указывает диапазон версий движка, в которых эта запись активна. Старые записи (`dataversion 0…59`) сохранены для совместимости с реплеями. Для текущей версии используются записи с `dataversionmin ≥ 60`.
- Помимо ресурсов каждый не-default пресет спавнит **дополнительные здания и юниты** через ASCII-маски (`mask : struct.begin`), которые тут не парсятся (слишком вариативно по нациям). Открой `startingsettings.cfg` целиком, если нужны точные расположения.
- `legends : struct.begin` под каждым `allowedcountries` — это словарь символов маски (`X = peasant`, `O = officer17`, `B = drummer17`, `P = polish unit`, и т.д.). Конкретный sid юнита берётся через `role` (= gc_ai_unit_*) или явный `basename`.

---

Сгенерировано из игровых файлов. Для перегенерации:

```
python compute/compute_starting_layout.py
```

## Источники

Все ссылки относительно `data/scripts/` в установке Cossacks 3.

[^1]: `CreateStartPointPeasants` — расстановка 18 крестьян 6×3 — `common.inc/dogenerate.inc:1231-1281`.

[^2]: `SetupStartingResources` + `cCircle*Mask` константы — `common.inc/dogenerate.inc:407-414, 720-978`.

[^3]: `SetupMines` — расстановка месторождений — `common.inc/dogenerate.inc:985`.

[^4]: enum `gc_mapsettings_startingunits_*` — `dmscript.global:1032-1045`.
