# Cossacks 3 — Полный справочник цифр (LEGACY)

> ⚠ **Этот файл — устаревшая монолитная версия.** Актуальная структурированная справка — в [`reference/`](reference/README.md) (главы 01-06, нации, сравнения), производные расчёты — в [`reports/`](reports/README.md). Файл сохраняется для обратной совместимости со старыми ссылками.

Извлечено напрямую из файлов игры в `C:\Program Files (x86)\Steam\steamapps\common\Cossacks 3\data\scripts\`. Скрипты парсера: `parser/`. Все цифры — немодифицированные значения из `unit.script`, `country.script`, `dmscript.global`.

**Версия игры:** актуальная на момент парсинга (Steam install).

## Содержание

- [1. Глобальная экономика](#1-глобальная-экономика)
- [2. Расхождения и автопроверки](#2-расхождения-и-автопроверки)
- [3. Нации (21)](#3-нации-21)
- [4. Здания по нациям](#4-здания-по-нациям)
    - [4.1 Per-nation постройки (`<nat><suffix>`)](#41-per-nation-постройки)
    - [4.2 Общие постройки (`<cluster><suffix>`)](#42-общие-постройки)
    - [4.3 Сводка по каждой нации](#43-сводка-по-каждой-нации)
- [5. Юниты](#5-юниты)
- [5b. Корабли](#5b-корабли)
- [5c. Шахты — апгрейды (gol/iro/coa)](#5c-шахты--апгрейды-goliroсoa)
- [6. Боевая математика](#6-боевая-математика)
    - [6a. Damage formula](#6a-damage-formula)
    - [6b. Скорости юнитов](#6b-скорости-юнитов)
    - [6c. Офицеры и формации](#6c-офицеры-и-формации)
- [6d. Рынок — обменные курсы](#6d-рынок--обменные-курсы)
- [7. Апгрейды](#7-апгрейды)
- [8. Дыры в данных и оговорки](#8-дыры-в-данных-и-оговорки)

## 1. Глобальная экономика

### Время
| Параметр | Значение | Что значит |
|---|---:|---|
| `gc_time_to_frames` | **32** | кадров в одной игровой секунде. `buildtime=144` = 4.5 сек. |
| game speed 0 (slow) | 7 | тиков/сек |
| game speed 1 (default) | 10 | тиков/сек |
| game speed 2 (fast) | 14 | тиков/сек |

### Базовые порции (сколько крестьянин приносит за один рейс при eff=100)
| Ресурс | Базовая порция | hits_needed (циклов работы перед сдачей) |
|---|---:|---:|
| food (еда) | **45** | 22 |
| wood (дерево) | **28** | 14 |
| stone (камень) | **40** | 20 |
| gold/iron/coal/etc. | **20** | (не задействован — шахты в режиме `produce`) |

### Формула добычи

```
delivered = (base_portion * eff) / 100  (integer division). eff defaults to 100; upgrades add to it additively.
```

`eff` инициализируется = **100** в `player.script:109`. Каждый апгрейд (mill, academy, blacksmith) добавляет своё значение к eff аддитивно. Например, +40% и +140% дают eff=280, и крестьянин приносит `45×280/100=126` еды за рейс.

### Прочее

- **Лимит юнитов на карте:** 32000
- **Лимит игроков:** 12
- **HP поля (для жатвы):** 25000
- **Upkeep юнита:** 30 food / unit (для большинства).

## 2. Расхождения и автопроверки

### 2a. Расхождения с промпт-заметками

Места, где значения в скриптах отличаются от исходных пользовательских заметок. Источник истины — файлы игры.

| Факт | В заметках | В файле | Источник | Вердикт |
|---|---|---|---|---|
| hits_needed for food | 30 | 22 | dmscript.global:799 gc_resource_hitsneeded_food | Файл: 22, не 30. Доверяем файлу — крестьянин делает 22 удара мотыгой до возврата к складу, не 30. Это укорачивает рейс и повышает фактический rate. |
| Field melioration (academy aca.4) cost | W1400 / G522 | W1000 / G475 (any nation) | country.script:3490 _country_AddUpgrade('aca.4', ..., wood=1000, gold=475) | Файл: W1000/G475. Расхождение с промпт-заметками — возможно, цифры из старой версии игры. Все 21 нация имеют одинаковую стоимость. |
| 'Manufacture agricultural equipment' (blacksmith) cost | W400 / G100 | не найден в blacksmith — этот апгрейд может быть из старого названия | country.script — нет blacksmith-апгрейда с такими параметрами | Текущий blacksmith содержит per-unit damage/protection апгрейды. Возможно, в C1 был отдельный agricultural-equipment апгрейд, который в C3 переименован в `aca.X` (academy). См. лист Upgrades с place=aca. |

### 2b. Sanity checks (автоматические утверждения)

**112/112 проверок прошли.** Если после патча игры тут появятся `FAIL` — это сигнал, что цифры/структура поменялись и нужно проверить парсер.

**✅ PASSED (по категориям):**

- **buildings** (49): aus has Town Hall (auscen), aus has Barracks 17c (ausbar), fra has Town Hall (fracen), fra has Barracks 17c (frabar), eng has Town Hall (engcen), eng has Barracks 17c (engbar) (+43)
- **constants** (10): gc_time_to_frames, gc_resource_hitsneeded_food, gc_resource_hitsneeded_wood, gc_resource_hitsneeded_stone, gc_obj_resource_portion_food, gc_obj_resource_portion_wood (+4)
- **conversions** (1): pixels_to_tile
- **counts** (5): Playable nations, Building rows (sid×nation), Unit rows (sid×nation), Upgrade rows (sid×nation), Officer entries
- **market** (3): food buy_default, food buy_max, wood sell_default
- **mine_upgrades** (4): Mine upgrades count (eurgol.*, aus), Mine total workers (5 base + 6 upgrades), Mine full upgrade total food cost, Mine full upgrade total gold cost
- **nations** (21): aus building count, fra building count, eng building count, spa building count, rus building count, ukr building count (+15)
- **trained_in** (4): Strelet trained at rusbar, Reiter trained at aussta, Fishboat trained at eurpor, peaaus trained at auscen
- **units** (15): Strelet (rus) exists, Strelet is rus-unique, Janissary (tur) exists, Janissary is tur-unique, Vityaz (rus) exists, Vityaz is rus-unique (+9)

## 3. Нации (21)

| ID | sid | Английское имя | Русское имя | Кластер `commonName` | Пехотный пеасант |
|---:|---|---|---|---|---|
| 0 | `aus` | Austria | Австрия | `eur` | `peaaus` |
| 1 | `fra` | France | Франция | `eur` | `peaeng` |
| 2 | `eng` | England | Англия | `eur` | `peaeng` |
| 3 | `spa` | Spain | Испания | `eur` | `peaspa` |
| 4 | `rus` | Russia | Россия | `rus` | `pearus` |
| 5 | `ukr` | Ukraine | Украина | `rus` | `peaukr` |
| 6 | `pol` | Poland | Польша | `eur` | `peapol` |
| 7 | `swe` | Sweden | Швеция | `eur` | `peaeng` |
| 8 | `pru` | Prussia | Пруссия | `eur` | `peaaus` |
| 9 | `ven` | Venice | Венеция | `eur` | `peaspa` |
| 10 | `tur` | Turkey | Турция | `tur` | `peatur` |
| 11 | `alg` | Algeria | Алжир | `tur` | `peatur` |
| 12 | `net` | Netherlands | Нидерланды | `eur` | `peaeng` |
| 13 | `den` | Denmark | Дания | `eur` | `peaeng` |
| 14 | `por` | Portugal | Португалия | `eur` | `peaspa` |
| 15 | `pie` | Piedmont | Пьемонт | `eur` | `peaspa` |
| 16 | `sax` | Saxony | Саксония | `eur` | `peaaus` |
| 17 | `bav` | Bavaria | Бавария | `eur` | `peaaus` |
| 18 | `hun` | Hungary | Венгрия | `eur` | `peapol` |
| 19 | `swi` | Switzerland | Швейцария | `eur` | `peaaus` |
| 20 | `sco` | Scotland | Шотландия | `eur` | `peasco` |

## 4. Здания по нациям

Цены и времена постройки даны для **базового** экземпляра. Каждое следующее здание того же типа стоит дороже на величину `costpercent` (200 = вторая постройка стоит ×2 от первой).

Время в секундах рассчитано как `buildtime / 32` (`gc_time_to_frames = 32`).

### 4.1 Per-nation постройки

Каждая нация имеет свой набор; sid формируется как `<nat>+<3-letter>`. Например, для Австрии: `auscen` (Town Hall), `ausbar` (Barracks), `ausaca` (Academy).

#### cen — Ratusha (Town Hall)

| Нация | sid | Имя (EN) | HP | Время (сек) | costpercent | Цена | farm |
|---|---|---|---:|---:|---:|---|---:|
| alg | `algcen` | Town Hall | 5500 | 156.25 | 300 | W450 S700 | 50 |
| aus | `auscen` | Town Hall | 4000 | 46.88 | 300 | W700 S700 | 100 |
| bav | `bavcen` | Town Hall | 4000 | 156.25 | 300 | W700 S700 | 100 |
| den | `dencen` | Town Hall | 4030 | 156.25 | 300 | W700 S700 | 100 |
| eng | `engcen` | Town Hall | 4030 | 156.25 | 300 | W700 S700 | 100 |
| fra | `fracen` | Town Hall | 4500 | 156.25 | 300 | W700 S700 | 100 |
| hun | `huncen` | Town Hall | 4000 | 156.25 | 300 | W700 S700 | 100 |
| net | `netcen` | Town Hall | 4950 | 156.25 | 300 | W700 S700 | 100 |
| pie | `piecen` | Town Hall | 4000 | 156.25 | 300 | W700 S700 | 100 |
| pol | `polcen` | Town Hall | 4300 | 156.25 | 300 | W700 S700 | 100 |
| por | `porcen` | Town Hall | 4000 | 156.25 | 300 | W700 S700 | 100 |
| pru | `prucen` | Town Hall | 4200 | 156.25 | 300 | W700 S700 | 100 |
| rus | `ruscen` | Town Hall | 4050 | 156.25 | 300 | W680 S700 | 75 |
| sax | `saxcen` | Town Hall | 4000 | 156.25 | 300 | W700 S700 | 100 |
| sco | `scocen` | Town Hall | 4000 | 156.25 | 300 | W700 S700 | 100 |
| spa | `spacen` | Town Hall | 4250 | 156.25 | 300 | W700 S700 | 100 |
| swe | `swecen` | Town Hall | 5000 | 156.25 | 300 | W700 S700 | 100 |
| swi | `swicen` | Town Hall | 4000 | 156.25 | 300 | W700 S700 | 100 |
| tur | `turcen` | Town Hall | 4000 | 156.25 | 300 | W600 S500 | 100 |
| ukr | `ukrcen` | Town Hall | 5300 | 156.25 | 400 | W700 | 200 |
| ven | `vencen` | Town Hall | 5100 | 156.25 | 300 | W700 S700 | 100 |

#### hou — Housing/Dwelling

| Нация | sid | Имя (EN) | HP | Время (сек) | costpercent | Цена | farm |
|---|---|---|---:|---:|---:|---|---:|
| alg | `alghou` | Housing | 4300 | 31.25 | 104 | W100 S100 | 25 |
| aus | `aushou` | Housing | 4000 | 31.25 | 104 | W100 S100 | 25 |
| bav | `bavhou` | Housing | 4000 | 31.25 | 104 | W100 S100 | 25 |
| den | `denhou` | Housing | 4000 | 31.25 | 104 | W100 S100 | 25 |
| eng | `enghou` | Housing | 5000 | 31.25 | 104 | W100 S100 | 25 |
| fra | `frahou` | Housing | 4000 | 31.25 | 104 | W100 S100 | 25 |
| hun | `hunhou` | Housing | 4000 | 31.25 | 104 | W100 S100 | 25 |
| net | `nethou` | Housing | 4500 | 31.25 | 104 | W100 S100 | 25 |
| pie | `piehou` | Housing | 4000 | 31.25 | 104 | W100 S100 | 25 |
| pol | `polhou` | Housing | 4100 | 31.25 | 104 | W100 S100 | 25 |
| por | `porhou` | Housing | 4000 | 31.25 | 104 | W100 S100 | 25 |
| pru | `pruhou` | Housing | 4500 | 31.25 | 104 | W100 S100 | 25 |
| rus | `rushou` | Izba | 5000 | 31.25 | 104 | W120 | 25 |
| sax | `saxhou` | Housing | 4000 | 31.25 | 104 | W100 S100 | 25 |
| sco | `scohou` | Housing | 4000 | 31.25 | 104 | W100 S100 | 25 |
| spa | `spahou` | Housing | 4200 | 31.25 | 104 | W100 S100 | 25 |
| swe | `swehou` | Housing | 5000 | 31.25 | 104 | W100 S100 | 25 |
| swi | `swihou` | Housing | 4000 | 31.25 | 104 | W100 S100 | 25 |
| tur | `turhou` | Housing | 4000 | 31.25 | 106 | W100 S100 | 25 |
| ukr | `ukrhou` | Hut | 4150 | 31.25 | 105 | W120 | 25 |
| ven | `venhou` | Housing | 5000 | 31.25 | 104 | W100 S100 | 25 |

#### bar — Barracks 17в.

| Нация | sid | Имя (EN) | HP | Время (сек) | costpercent | Цена | farm |
|---|---|---|---:|---:|---:|---|---:|
| alg | `algbar` | Barracks | 35000 | 93.75 | 500 | W400 S400 | 50 |
| aus | `ausbar` | Barracks, 17th century | 40000 | 93.75 | 500 | W100 S100 G500 | 150 |
| bav | `bavbar` | Barracks, 17th century | 40000 | 93.75 | 500 | W100 S100 G500 | 150 |
| den | `denbar` | Barracks, 17th century | 40000 | 93.75 | 500 | W100 S100 G500 | 150 |
| eng | `engbar` | Barracks, 17th century | 40000 | 93.75 | 500 | W100 S100 G500 | 150 |
| fra | `frabar` | Barracks, 17th century | 40000 | 93.75 | 500 | W100 S100 G500 | 150 |
| hun | `hunbar` | Barracks, 17th century | 40000 | 93.75 | 500 | W100 S100 G500 | 150 |
| net | `netbar` | Barracks, 17th century | 40000 | 93.75 | 500 | W100 S100 G500 | 150 |
| pie | `piebar` | Barracks, 17th century | 40000 | 93.75 | 500 | W100 S100 G500 | 150 |
| pol | `polbar` | Barracks, 17th century | 40000 | 93.75 | 500 | W100 S100 G500 | 150 |
| por | `porbar` | Barracks, 17th century | 40000 | 93.75 | 500 | W100 S100 G500 | 150 |
| pru | `prubar` | Barracks, 17th century | 40000 | 93.75 | 500 | W100 S100 G500 | 150 |
| rus | `rusbar` | Strelets Barracks | 25000 | 78.12 | 300 | W200 S20 | 25 |
| sax | `saxbar` | Barracks, 17th century | 40000 | 93.75 | 500 | W100 S100 G500 | 150 |
| sco | `scobar` | Barracks, 17th century | 30000 | 93.75 | 500 | W100 S100 G500 | 150 |
| spa | `spabar` | Barracks, 17th century | 40000 | 93.75 | 500 | W100 S100 G500 | 150 |
| swe | `swebar` | Barracks, 17th century | 40000 | 93.75 | 500 | W100 S100 G500 | 150 |
| swi | `swibar` | Barracks, 17th century | 40000 | 93.75 | 500 | W100 S100 G500 | 150 |
| tur | `turbar` | Barracks | 35000 | 93.75 | 500 | W400 S400 | 50 |
| ukr | `ukrbar` | Cossack House | 20000 | 93.75 | 300 | W150 S150 | 75 |
| ven | `venbar` | Barracks, 17th century | 40000 | 93.75 | 500 | W100 S100 G500 | 150 |

#### ba2 — Barracks 18в.

| Нация | sid | Имя (EN) | HP | Время (сек) | costpercent | Цена | farm |
|---|---|---|---:|---:|---:|---|---:|
| aus | `ausba2` | Barracks, 18th century | 55000 | 5625.0 | 200 | W1700 S2950 G4000 | 250 |
| bav | `bavba2` | Barracks, 18th century | 55000 | 5625.0 | 200 | W1700 S2950 G4000 | 250 |
| den | `denba2` | Barracks, 18th century | 55000 | 5625.0 | 200 | W1700 S2950 G4000 | 250 |
| eng | `engba2` | Barracks, 18th century | 55000 | 5625.0 | 200 | W1700 S2950 G4000 | 250 |
| fra | `fraba2` | Barracks, 18th century | 55000 | 5625.0 | 200 | W1700 S2950 G4000 | 250 |
| hun | `hunba2` | Barracks, 18th century | 55000 | 5625.0 | 200 | W1700 S2950 G4000 | 250 |
| net | `netba2` | Barracks, 18th century | 55000 | 5625.0 | 200 | W1700 S2950 G4000 | 250 |
| pie | `pieba2` | Barracks, 18th century | 55000 | 5625.0 | 200 | W1700 S2950 G4000 | 250 |
| pol | `polba2` | Barracks, 18th century | 55000 | 5625.0 | 200 | W1700 S2950 G4000 | 250 |
| por | `porba2` | Barracks, 18th century | 55000 | 5625.0 | 200 | W1700 S2950 G4000 | 250 |
| pru | `pruba2` | Barracks, 18th century | 55000 | 5625.0 | 200 | W1700 S2950 G4000 | 250 |
| rus | `rusba2` | Barracks, 18th century | 55000 | 5625.0 | 200 | W1700 S2950 G4000 | 250 |
| sax | `saxba2` | Barracks, 18th century | 55000 | 5625.0 | 200 | W1700 S2950 G4000 | 250 |
| sco | `scoba2` | Castle | 40000 | 625.0 | 250 | W640 S2400 G2400 | 150 |
| spa | `spaba2` | Barracks, 18th century | 55000 | 5625.0 | 200 | W1700 S2950 G4000 | 250 |
| swe | `sweba2` | Barracks, 18th century | 55000 | 5625.0 | 200 | W1700 S2950 G4000 | 250 |
| swi | `swiba2` | Barracks, 18th century | 55000 | 5625.0 | 200 | W1700 S2950 G4000 | 250 |
| ven | `venba2` | Barracks, 18th century | 55000 | 5625.0 | 200 | W1700 S2950 G4000 | 250 |

#### bla — Blacksmith

| Нация | sid | Имя (EN) | HP | Время (сек) | costpercent | Цена | farm |
|---|---|---|---:|---:|---:|---|---:|
| alg | `algbla` | Blacksmith | 6500 | 109.38 | 400 | W100 S30 I640 | 0 |
| aus | `ausbla` | Blacksmith | 5500 | 93.75 | 400 | W100 S30 I640 | 0 |
| bav | `bavbla` | Blacksmith | 5500 | 93.75 | 400 | W100 S30 I640 | 0 |
| den | `denbla` | Blacksmith | 5500 | 93.75 | 400 | W100 S30 I640 | 0 |
| eng | `engbla` | Blacksmith | 5500 | 93.75 | 400 | W100 S30 I640 | 0 |
| fra | `frabla` | Blacksmith | 5500 | 93.75 | 600 | W100 S30 I640 | 0 |
| hun | `hunbla` | Blacksmith | 5500 | 93.75 | 400 | W100 S30 I640 | 0 |
| net | `netbla` | Blacksmith | 5500 | 93.75 | 400 | W100 S30 I640 | 0 |
| pie | `piebla` | Blacksmith | 5500 | 93.75 | 400 | W100 S30 I640 | 0 |
| pol | `polbla` | Blacksmith | 5500 | 93.75 | 400 | W100 S30 I640 | 0 |
| por | `porbla` | Blacksmith | 5500 | 93.75 | 400 | W100 S30 I640 | 0 |
| pru | `prubla` | Blacksmith | 5500 | 93.75 | 400 | W100 S30 I640 | 0 |
| rus | `rusbla` | Blacksmith | 5500 | 93.75 | 400 | W100 S30 I640 | 0 |
| sax | `saxbla` | Blacksmith | 5500 | 93.75 | 400 | W100 S30 I640 | 0 |
| sco | `scobla` | Blacksmith | 5500 | 93.75 | 400 | W100 S30 I640 | 0 |
| spa | `spabla` | Blacksmith | 5500 | 93.75 | 400 | W100 S30 I640 | 0 |
| swe | `swebla` | Blacksmith | 5500 | 93.75 | 400 | W100 S30 I640 | 0 |
| swi | `swibla` | Blacksmith | 5500 | 93.75 | 400 | W100 S30 I640 | 0 |
| tur | `turbla` | Blacksmith | 6500 | 109.38 | 400 | W100 S30 I640 | 0 |
| ukr | `ukrbla` | Blacksmith | 4500 | 62.5 | 400 | W100 S30 I640 | 0 |
| ven | `venbla` | Blacksmith | 5500 | 93.75 | 400 | W100 S30 I640 | 0 |

#### sta — Stable

| Нация | sid | Имя (EN) | HP | Время (сек) | costpercent | Цена | farm |
|---|---|---|---:|---:|---:|---|---:|
| alg | `algsta` | Stable | 55000 | 156.25 | 700 | W1000 S2200 | 0 |
| aus | `aussta` | Stable | 20000 | 625.0 | 200 | W2500 S100 G600 | 0 |
| bav | `bavsta` | Stable | 20000 | 625.0 | 200 | W2500 S100 G600 | 0 |
| den | `densta` | Stable | 20000 | 625.0 | 200 | W2500 S100 G600 | 0 |
| eng | `engsta` | Stable | 25000 | 375.0 | 200 | W2350 G800 | 0 |
| fra | `frasta` | Stable | 20000 | 625.0 | 200 | W2500 S100 G600 | 0 |
| hun | `hunsta` | Stable | 20000 | 625.0 | 200 | W2500 S100 G600 | 0 |
| net | `netsta` | Stable | 20000 | 625.0 | 200 | W2500 S100 G600 | 0 |
| pie | `piesta` | Stable | 20000 | 625.0 | 200 | W2500 S100 G600 | 0 |
| pol | `polsta` | Stable | 20000 | 625.0 | 200 | W2500 S100 G600 | 0 |
| por | `porsta` | Stable | 20000 | 625.0 | 200 | W2500 S100 G600 | 0 |
| pru | `prusta` | Stable | 20000 | 625.0 | 200 | W2500 S100 G600 | 0 |
| rus | `russta` | Stable | 25000 | 375.0 | 200 | W7950 G550 | 0 |
| sax | `saxsta` | Stable | 20000 | 625.0 | 200 | W2500 S100 G600 | 0 |
| sco | `scosta` | Stable | 25000 | 375.0 | 200 | W2350 G800 | 0 |
| spa | `spasta` | Stable | 20000 | 625.0 | 200 | W2500 S100 G600 | 0 |
| swe | `swesta` | Stable | 20000 | 625.0 | 200 | W2500 S100 G600 | 0 |
| swi | `swista` | Stable | 20000 | 625.0 | 200 | W2500 S100 G600 | 0 |
| tur | `tursta` | Stable | 55000 | 156.25 | 700 | W1000 S2600 | 0 |
| ukr | `ukrsta` | Stable | 10000 | 156.25 | 300 | W3200 S850 G850 | 0 |
| ven | `vensta` | Stable | 20000 | 625.0 | 200 | W2500 S100 G600 | 0 |

#### tem — Cathedral

| Нация | sid | Имя (EN) | HP | Время (сек) | costpercent | Цена | farm |
|---|---|---|---:|---:|---:|---|---:|
| alg | `algtem` | Mosque | 5000 | 93.75 | 300 | W1000 S1200 I500 | 0 |
| aus | `austem` | Cathedral | 4200 | 156.25 | 300 | W1000 S1200 I500 | 0 |
| bav | `bavtem` | Cathedral | 4200 | 156.25 | 300 | W1000 S1200 I500 | 0 |
| den | `dentem` | Cathedral | 4200 | 156.25 | 300 | W1000 S1200 I500 | 0 |
| eng | `engtem` | Cathedral | 4200 | 156.25 | 300 | W1000 S1200 I500 | 0 |
| fra | `fratem` | Cathedral | 6000 | 312.5 | 300 | W1100 S2000 I600 | 0 |
| hun | `huntem` | Cathedral | 4200 | 156.25 | 300 | W1000 S1200 I500 | 0 |
| net | `nettem` | Cathedral | 4200 | 156.25 | 300 | W1000 S1200 I500 | 0 |
| pie | `pietem` | Cathedral | 4200 | 156.25 | 300 | W1000 S1200 I500 | 0 |
| pol | `poltem` | Cathedral | 4200 | 156.25 | 300 | W1000 S1200 I500 | 0 |
| por | `portem` | Cathedral | 4200 | 156.25 | 300 | W1000 S1200 I500 | 0 |
| pru | `prutem` | Cathedral | 4200 | 156.25 | 300 | W1000 S1200 I500 | 0 |
| rus | `rustem` | Orthodox Cathedral | 4500 | 156.25 | 300 | W1150 S1650 G100 I500 | 0 |
| sax | `saxtem` | Cathedral | 4200 | 156.25 | 300 | W1000 S1200 I500 | 0 |
| sco | `scotem` | Cathedral | 4200 | 156.25 | 300 | W1000 S1200 I500 | 0 |
| spa | `spatem` | Cathedral | 4200 | 156.25 | 300 | W1000 S1200 I500 | 0 |
| swe | `swetem` | Cathedral | 4200 | 156.25 | 300 | W1000 S1200 I500 | 0 |
| swi | `switem` | Cathedral | 4200 | 156.25 | 300 | W1000 S1200 I500 | 0 |
| tur | `turtem` | Mosque | 5000 | 93.75 | 300 | W1000 S1200 I500 | 0 |
| ukr | `ukrtem` | Orthodox Cathedral | 5300 | 156.25 | 300 | W1100 S1400 I300 | 0 |
| ven | `ventem` | Cathedral | 4200 | 156.25 | 300 | W1000 S1200 I500 | 0 |

#### aca — Academy

| Нация | sid | Имя (EN) | HP | Время (сек) | costpercent | Цена | farm |
|---|---|---|---:|---:|---:|---|---:|
| alg | `algaca` | Minaret | 65000 | 156.25 | 300 | W1450 S1100 | 0 |
| aus | `ausaca` | Academy | 65000 | 625.0 | 300 | W1250 S1100 | 0 |
| bav | `bavaca` | Academy | 63000 | 625.0 | 300 | W1250 S1100 | 0 |
| den | `denaca` | Academy | 63000 | 625.0 | 300 | W1450 S900 | 0 |
| eng | `engaca` | Academy | 63000 | 625.0 | 300 | W1150 S1200 | 0 |
| fra | `fraaca` | Academy | 63000 | 625.0 | 300 | W1250 S1100 | 0 |
| hun | `hunaca` | Academy | 63000 | 625.0 | 300 | W1250 S1100 | 0 |
| net | `netaca` | Academy | 63000 | 625.0 | 300 | W1050 S1230 | 0 |
| pie | `pieaca` | Academy | 63000 | 625.0 | 300 | W1250 S1100 | 0 |
| pol | `polaca` | Academy | 63000 | 625.0 | 300 | W950 S800 | 0 |
| por | `poraca` | Academy | 63000 | 625.0 | 300 | W1250 S1100 | 0 |
| pru | `pruaca` | Academy | 63000 | 625.0 | 300 | W1200 S1150 | 0 |
| rus | `rusaca` | Academy | 65000 | 843.75 | 300 | W1250 S1300 | 0 |
| sax | `saxaca` | Academy | 63000 | 625.0 | 300 | W1250 S1100 | 0 |
| sco | `scoaca` | Academy | 63000 | 625.0 | 300 | W1250 S1100 | 0 |
| spa | `spaaca` | Academy | 63000 | 625.0 | 300 | W1350 S1000 | 0 |
| swe | `sweaca` | Academy | 63000 | 625.0 | 300 | W1350 S1000 | 0 |
| swi | `swiaca` | Academy | 63000 | 625.0 | 300 | W1250 S1100 | 0 |
| tur | `turaca` | Minaret | 65000 | 156.25 | 300 | W1450 S1100 | 0 |
| ukr | `ukraca` | Academy | 65000 | 46.88 | 300 | W1350 S1200 | 0 |
| ven | `venaca` | Academy | 63000 | 625.0 | 300 | W1090 S1260 | 0 |

#### art — Artillery Depot

| Нация | sid | Имя (EN) | HP | Время (сек) | costpercent | Цена | farm |
|---|---|---|---:|---:|---:|---|---:|
| alg | `algart` | Artillery Depot | 40000 | 245.94 | 200 | W100 S1000 C1400 | 0 |
| aus | `ausart` | Artillery Depot | 40000 | 245.94 | 200 | W100 S1000 C1400 | 0 |
| bav | `bavart` | Artillery Depot | 40000 | 245.94 | 200 | W100 S1000 C1400 | 0 |
| den | `denart` | Artillery Depot | 40000 | 245.94 | 200 | W100 S1000 C1400 | 0 |
| eng | `engart` | Artillery Depot | 40000 | 245.94 | 200 | W100 S1000 C1400 | 0 |
| fra | `fraart` | Artillery Depot | 40000 | 245.94 | 200 | W100 S1000 C1400 | 0 |
| hun | `hunart` | Artillery Depot | 40000 | 245.94 | 200 | W100 S1000 C1400 | 0 |
| net | `netart` | Artillery Depot | 40000 | 245.94 | 200 | W100 S1000 C1400 | 0 |
| pie | `pieart` | Artillery Depot | 40000 | 245.94 | 200 | W100 S1000 C1400 | 0 |
| pol | `polart` | Artillery Depot | 40000 | 245.94 | 200 | W100 S1000 C1400 | 0 |
| por | `porart` | Artillery Depot | 40000 | 245.94 | 200 | W100 S1000 C1400 | 0 |
| pru | `pruart` | Artillery Depot | 40000 | 245.94 | 200 | W100 S1000 C1400 | 0 |
| rus | `rusart` | Artillery Depot | 40000 | 245.94 | 200 | W100 S1000 C1400 | 0 |
| sax | `saxart` | Artillery Depot | 40000 | 245.94 | 200 | W100 S1000 C1400 | 0 |
| sco | `scoart` | Artillery Depot | 40000 | 245.94 | 200 | W100 S1000 C1400 | 0 |
| spa | `spaart` | Artillery Depot | 40000 | 245.94 | 200 | W100 S1000 C1400 | 0 |
| swe | `sweart` | Artillery Depot | 40000 | 245.94 | 200 | W100 S1000 C1400 | 0 |
| swi | `swiart` | Artillery Depot | 40000 | 245.94 | 200 | W100 S1000 C1400 | 0 |
| tur | `turart` | Artillery Depot | 40000 | 245.94 | 200 | W500 S1200 C1400 | 0 |
| ukr | `ukrart` | Artillery Depot | 40000 | 245.94 | 200 | W4250 S4400 G100 C1400 | 0 |
| ven | `venart` | Artillery Depot | 40000 | 245.94 | 200 | W100 S1000 C1400 | 0 |

#### dip — Diplomatic Center

| Нация | sid | Имя (EN) | HP | Время (сек) | costpercent | Цена | farm |
|---|---|---|---:|---:|---:|---|---:|
| alg | `algdip` | Diplomatic Center | 5500 | 312.5 | 100 | W4600 S2020 | 0 |
| aus | `ausdip` | Diplomatic Center | 4500 | 312.5 | 100 | W4900 S1700 | 0 |
| bav | `bavdip` | Diplomatic Center | 4500 | 312.5 | 100 | W4900 S1700 | 0 |
| den | `dendip` | Diplomatic Center | 4500 | 312.5 | 100 | W4900 S1700 | 0 |
| eng | `engdip` | Diplomatic Center | 4500 | 312.5 | 100 | W4900 S1700 | 0 |
| fra | `fradip` | Diplomatic Center | 4500 | 312.5 | 100 | W4900 S1700 | 0 |
| hun | `hundip` | Diplomatic Center | 4500 | 312.5 | 100 | W4900 S1700 | 0 |
| net | `netdip` | Diplomatic Center | 4500 | 312.5 | 100 | W4900 S1700 | 0 |
| pie | `piedip` | Diplomatic Center | 4500 | 312.5 | 100 | W4900 S1700 | 0 |
| pol | `poldip` | Diplomatic Center | 4500 | 312.5 | 100 | W4900 S1700 | 0 |
| por | `pordip` | Diplomatic Center | 4500 | 312.5 | 100 | W4900 S1700 | 0 |
| pru | `prudip` | Diplomatic Center | 4500 | 312.5 | 100 | W4900 S1700 | 0 |
| rus | `rusdip` | Diplomatic Center | 6500 | 312.5 | 100 | W7900 S3700 | 0 |
| sax | `saxdip` | Diplomatic Center | 4500 | 312.5 | 100 | W4900 S1700 | 0 |
| sco | `scodip` | Diplomatic Center | 4500 | 312.5 | 100 | W4900 S1700 | 0 |
| spa | `spadip` | Diplomatic Center | 4500 | 312.5 | 100 | W4900 S1700 | 0 |
| swe | `swedip` | Diplomatic Center | 4500 | 312.5 | 100 | W4900 S1700 | 0 |
| swi | `swidip` | Diplomatic Center | 4500 | 312.5 | 100 | W4900 S1700 | 0 |
| tur | `turdip` | Diplomatic Center | 5500 | 312.5 | 100 | W4600 S2020 | 0 |
| ukr | `ukrdip` | Diplomatic Center | 5000 | 312.5 | 100 | W3900 S2700 | 0 |
| ven | `vendip` | Diplomatic Center | 4500 | 312.5 | 100 | W4900 S1700 | 0 |

### 4.2 Общие постройки

Sid формируется как `<cluster>+<3-letter>`, где cluster зависит от нации и типа здания (см. функцию `building_cluster()` в `parser/config.py`).

#### mil — Mill

| sid (cluster) | Используют нации | HP | Время (сек) | costpercent | Цена | Доп. |
|---|---|---:|---:|---:|---|---|
| `eurmil` | aus, bav, den, eng, fra, hun, net, pie, pol, por, pru, sax, sco, spa, swe, swi, ven | 20000 | 93.75 | 200 | W30 S150 | — |
| `rusmil` | rus, ukr | 15000 | 93.75 | 200 | W210 | — |
| `turmil` | alg, tur | 20000 | 93.75 | 200 | W30 S150 | — |

#### sto — Storehouse

| sid (cluster) | Используют нации | HP | Время (сек) | costpercent | Цена | Доп. |
|---|---|---:|---:|---:|---|---|
| `eursto` | aus, bav, den, eng, fra, hun, net, pie, pru, sax, sco, swe, swi, ven | 10000 | 31.25 | 150 | W50 S20 | — |
| `russto` | pol, rus, ukr | 10000 | 31.25 | 200 | W50 S20 | — |
| `spasto` | por, spa | 10000 | 31.25 | 150 | W20 S20 | — |
| `tursto` | alg, tur | 10000 | 31.25 | 200 | W30 S10 | — |

#### mar — Market

| sid (cluster) | Используют нации | HP | Время (сек) | costpercent | Цена | Доп. |
|---|---|---:|---:|---:|---|---|
| `eurmar` | aus, bav, den, eng, fra, hun, net, pie, pol, pru, sax, sco, swe, swi, ven | 4000 | 234.38 | 2000 | W450 | — |
| `rusmar` | rus, ukr | 4000 | 234.38 | 2000 | W450 | — |
| `spamar` | por, spa | 4000 | 156.25 | 2000 | W450 | — |
| `turmar` | alg, tur | 4500 | 234.38 | 1500 | W450 S150 | — |

#### por — Shipyard

| sid (cluster) | Используют нации | HP | Время (сек) | costpercent | Цена | Доп. |
|---|---|---:|---:|---:|---|---|
| `eurpor` | aus, bav, den, eng, fra, hun, net, pie, pol, pru, sax, sco, spa, swe, swi, ven | 50000 | 1562.5 | 150 | W1600 S800 I400 | — |
| `porpor` | por | 50000 | 1562.5 | 150 | W1600 S800 I400 | dmg 1000; range 1500; upkeep {"gold": 250} |
| `ruspor` | rus | 45000 | 1562.5 | 150 | W1200 S800 I400 | — |
| `turpor` | alg, tur | 40000 | 1562.5 | 150 | W800 S800 I400 | — |
| `ukrpor` | ukr | 45000 | 1562.5 | 150 | W2000 | — |

#### tow — Tower

| sid (cluster) | Используют нации | HP | Время (сек) | costpercent | Цена | Доп. |
|---|---|---:|---:|---:|---|---|
| `eurtow` | aus, bav, den, eng, fra, hun, net, pie, pol, por, pru, sax, sco, spa, swe, swi, ven | 20000 | 1230.31 | 120 | W100 S100 G150 | dmg 1000; range 1500; upkeep {"gold": 500} |
| `rustow` | rus | 21000 | 1476.56 | 125 | W100 S100 G150 | dmg 1000; range 1500; upkeep {"gold": 500} |
| `turtow` | alg, tur | 22500 | 984.38 | 125 | W150 S90 G100 | dmg 1200; range 1600; upkeep {"gold": 500} |

#### gol — Gold Mine

| sid (cluster) | Используют нации | HP | Время (сек) | costpercent | Цена | Доп. |
|---|---|---:|---:|---:|---|---|
| `eurgol` | alg, aus, bav, den, eng, fra, hun, net, pie, pol, por, pru, rus, sax, sco, spa, swe, swi, tur, ukr, ven | 2500 | 93.75 | 0 | W100 S100 | produce {"gold": 13}; peasants 5 |

#### iro — Iron Mine

| sid (cluster) | Используют нации | HP | Время (сек) | costpercent | Цена | Доп. |
|---|---|---:|---:|---:|---|---|
| `euriro` | alg, aus, bav, den, eng, fra, hun, net, pie, pol, por, pru, rus, sax, sco, spa, swe, swi, tur, ukr, ven | 2500 | 93.75 | 0 | W100 S100 | produce {"iron": 13}; peasants 5 |

#### coa — Coal Mine

| sid (cluster) | Используют нации | HP | Время (сек) | costpercent | Цена | Доп. |
|---|---|---:|---:|---:|---|---|
| `eurcoa` | alg, aus, bav, den, eng, fra, hun, net, pie, pol, por, pru, rus, sax, sco, spa, swe, swi, tur, ukr, ven | 2500 | 93.75 | 0 | W100 S100 | produce {"coal": 13}; peasants 5 |

#### swa — Stone Wall

| sid (cluster) | Используют нации | HP | Время (сек) | costpercent | Цена | Доп. |
|---|---|---:|---:|---:|---|---|
| `eurswa` | aus, bav, den, eng, fra, hun, net, pie, pol, por, pru, sax, sco, spa, swe, swi, ven | 50000 | 90.0 | 0 | S50 | upkeep {"stone": 250} |
| `russwa` | rus | 50000 | 200.0 | 0 | S60 | upkeep {"stone": 200} |
| `turswa` | alg, tur | 50000 | 120.0 | 0 | S60 | upkeep {"stone": 150} |

#### sga — Stone Gate

| sid (cluster) | Используют нации | HP | Время (сек) | costpercent | Цена | Доп. |
|---|---|---:|---:|---:|---|---|
| `eursga` | aus, bav, den, eng, fra, hun, net, pie, pol, por, pru, sax, sco, spa, swe, swi, ven | 50000 | 90.0 | 0 | S50 | upkeep {"stone": 250} |
| `russga` | rus | 50000 | 200.0 | 0 | S60 | upkeep {"stone": 200} |
| `tursga` | alg, tur | 50000 | 120.0 | 0 | S60 | upkeep {"stone": 150} |

### 4.3 Сводка по каждой нации

Полный набор зданий + общая стоимость 1× каждого.

#### aus — Austria

| sid | name | HP | Time (s) | cost% | F | W | S | G | I | C | farm | produces |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `eurcoa` | Mine | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | 0 | — |
| `eurgol` | Mine | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | 0 | — |
| `euriro` | Mine | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | 0 | — |
| `eurmar` | Market | 4000 | 234.38 | 2000 | 0 | 450 | 0 | 0 | 0 | 0 | 0 | — |
| `eurmil` | Mill | 20000 | 93.75 | 200 | 0 | 30 | 150 | 0 | 0 | 0 | 0 | field |
| `eurpor` | Shipyard | 50000 | 1562.5 | 150 | 0 | 1600 | 800 | 0 | 400 | 0 | 0 | battleship, chaika, ferry, fishboat, frigate, galley (+3) |
| `eursga` | Gate | 50000 | 90.0 | 0 | 0 | 0 | 50 | 0 | 0 | 0 | 0 | — |
| `eursto` | Storehouse | 10000 | 31.25 | 150 | 0 | 50 | 20 | 0 | 0 | 0 | 0 | — |
| `eurswa` | Wall | 50000 | 90.0 | 0 | 0 | 0 | 50 | 0 | 0 | 0 | 0 | — |
| `eurtow` | Tower | 20000 | 1230.31 | 120 | 0 | 100 | 100 | 150 | 0 | 0 | 0 | — |
| `ausaca` | Academy | 65000 | 625.0 | 300 | 0 | 1250 | 1100 | 0 | 0 | 0 | 0 | — |
| `ausart` | Artillery Depot | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |
| `ausba2` | Barracks, 18th century | 55000 | 5625.0 | 200 | 0 | 1700 | 2950 | 4000 | 0 | 0 | 250 | archersco, bagpiper, chasseur, drummer18, grenadier, grenadierbav (+18) |
| `ausbar` | Barracks, 17th century | 40000 | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | archer, archertur, drummer, drummerrus, drummertur, gauduk (+23) |
| `ausbla` | Blacksmith | 5500 | 93.75 | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| `auscen` | Town Hall | 4000 | 46.88 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | peaaus, peaeng, peapol, pearus, peasco, peaspa (+2) |
| `ausdip` | Diplomatic Center | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip, lightcavalrydip (+2) |
| `aushou` | Housing | 4000 | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| `aussta` | Stable | 20000 | 625.0 | 200 | 0 | 2500 | 100 | 600 | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier, dragoon (+24) |
| `austem` | Cathedral | 4200 | 156.25 | 300 | 0 | 1000 | 1200 | 0 | 500 | 0 | 0 | mullah, padre, pope, priest |

#### fra — France

| sid | name | HP | Time (s) | cost% | F | W | S | G | I | C | farm | produces |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `eurcoa` | Mine | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | 0 | — |
| `eurgol` | Mine | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | 0 | — |
| `euriro` | Mine | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | 0 | — |
| `eurmar` | Market | 4000 | 234.38 | 2000 | 0 | 450 | 0 | 0 | 0 | 0 | 0 | — |
| `eurmil` | Mill | 20000 | 93.75 | 200 | 0 | 30 | 150 | 0 | 0 | 0 | 0 | field |
| `eurpor` | Shipyard | 50000 | 1562.5 | 150 | 0 | 1600 | 800 | 0 | 400 | 0 | 0 | battleship, chaika, ferry, fishboat, frigate, galley (+3) |
| `eursga` | Gate | 50000 | 90.0 | 0 | 0 | 0 | 50 | 0 | 0 | 0 | 0 | — |
| `eursto` | Storehouse | 10000 | 31.25 | 150 | 0 | 50 | 20 | 0 | 0 | 0 | 0 | — |
| `eurswa` | Wall | 50000 | 90.0 | 0 | 0 | 0 | 50 | 0 | 0 | 0 | 0 | — |
| `eurtow` | Tower | 20000 | 1230.31 | 120 | 0 | 100 | 100 | 150 | 0 | 0 | 0 | — |
| `fraaca` | Academy | 63000 | 625.0 | 300 | 0 | 1250 | 1100 | 0 | 0 | 0 | 0 | — |
| `fraart` | Artillery Depot | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |
| `fraba2` | Barracks, 18th century | 55000 | 5625.0 | 200 | 0 | 1700 | 2950 | 4000 | 0 | 0 | 250 | archersco, bagpiper, chasseur, drummer18, grenadier, grenadierbav (+18) |
| `frabar` | Barracks, 17th century | 40000 | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | archer, archertur, drummer, drummerrus, drummertur, gauduk (+23) |
| `frabla` | Blacksmith | 5500 | 93.75 | 600 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| `fracen` | Town Hall | 4500 | 156.25 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | peaaus, peaeng, peapol, pearus, peasco, peaspa (+2) |
| `fradip` | Diplomatic Center | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip, lightcavalrydip (+2) |
| `frahou` | Housing | 4000 | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| `frasta` | Stable | 20000 | 625.0 | 200 | 0 | 2500 | 100 | 600 | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier, dragoon (+24) |
| `fratem` | Cathedral | 6000 | 312.5 | 300 | 0 | 1100 | 2000 | 0 | 600 | 0 | 0 | mullah, padre, pope, priest |

#### eng — England

| sid | name | HP | Time (s) | cost% | F | W | S | G | I | C | farm | produces |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `eurcoa` | Mine | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | 0 | — |
| `eurgol` | Mine | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | 0 | — |
| `euriro` | Mine | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | 0 | — |
| `eurmar` | Market | 4000 | 234.38 | 2000 | 0 | 450 | 0 | 0 | 0 | 0 | 0 | — |
| `eurmil` | Mill | 20000 | 93.75 | 200 | 0 | 30 | 150 | 0 | 0 | 0 | 0 | field |
| `eurpor` | Shipyard | 50000 | 1562.5 | 150 | 0 | 1600 | 800 | 0 | 400 | 0 | 0 | battleship, chaika, ferry, fishboat, frigate, galley (+3) |
| `eursga` | Gate | 50000 | 90.0 | 0 | 0 | 0 | 50 | 0 | 0 | 0 | 0 | — |
| `eursto` | Storehouse | 10000 | 31.25 | 150 | 0 | 50 | 20 | 0 | 0 | 0 | 0 | — |
| `eurswa` | Wall | 50000 | 90.0 | 0 | 0 | 0 | 50 | 0 | 0 | 0 | 0 | — |
| `eurtow` | Tower | 20000 | 1230.31 | 120 | 0 | 100 | 100 | 150 | 0 | 0 | 0 | — |
| `engaca` | Academy | 63000 | 625.0 | 300 | 0 | 1150 | 1200 | 0 | 0 | 0 | 0 | — |
| `engart` | Artillery Depot | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |
| `engba2` | Barracks, 18th century | 55000 | 5625.0 | 200 | 0 | 1700 | 2950 | 4000 | 0 | 0 | 250 | archersco, bagpiper, chasseur, drummer18, grenadier, grenadierbav (+18) |
| `engbar` | Barracks, 17th century | 40000 | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | archer, archertur, drummer, drummerrus, drummertur, gauduk (+23) |
| `engbla` | Blacksmith | 5500 | 93.75 | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| `engcen` | Town Hall | 4030 | 156.25 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | peaaus, peaeng, peapol, pearus, peasco, peaspa (+2) |
| `engdip` | Diplomatic Center | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip, lightcavalrydip (+2) |
| `enghou` | Housing | 5000 | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| `engsta` | Stable | 25000 | 375.0 | 200 | 0 | 2350 | 0 | 800 | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier, dragoon (+24) |
| `engtem` | Cathedral | 4200 | 156.25 | 300 | 0 | 1000 | 1200 | 0 | 500 | 0 | 0 | mullah, padre, pope, priest |

#### spa — Spain

| sid | name | HP | Time (s) | cost% | F | W | S | G | I | C | farm | produces |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `eurcoa` | Mine | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | 0 | — |
| `eurgol` | Mine | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | 0 | — |
| `euriro` | Mine | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | 0 | — |
| `eurmil` | Mill | 20000 | 93.75 | 200 | 0 | 30 | 150 | 0 | 0 | 0 | 0 | field |
| `eurpor` | Shipyard | 50000 | 1562.5 | 150 | 0 | 1600 | 800 | 0 | 400 | 0 | 0 | battleship, chaika, ferry, fishboat, frigate, galley (+3) |
| `eursga` | Gate | 50000 | 90.0 | 0 | 0 | 0 | 50 | 0 | 0 | 0 | 0 | — |
| `eurswa` | Wall | 50000 | 90.0 | 0 | 0 | 0 | 50 | 0 | 0 | 0 | 0 | — |
| `eurtow` | Tower | 20000 | 1230.31 | 120 | 0 | 100 | 100 | 150 | 0 | 0 | 0 | — |
| `spamar` | Market | 4000 | 156.25 | 2000 | 0 | 450 | 0 | 0 | 0 | 0 | 0 | — |
| `spasto` | Storehouse | 10000 | 31.25 | 150 | 0 | 20 | 20 | 0 | 0 | 0 | 0 | — |
| `spaaca` | Academy | 63000 | 625.0 | 300 | 0 | 1350 | 1000 | 0 | 0 | 0 | 0 | — |
| `spaart` | Artillery Depot | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |
| `spaba2` | Barracks, 18th century | 55000 | 5625.0 | 200 | 0 | 1700 | 2950 | 4000 | 0 | 0 | 250 | archersco, bagpiper, chasseur, drummer18, grenadier, grenadierbav (+18) |
| `spabar` | Barracks, 17th century | 40000 | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | archer, archertur, drummer, drummerrus, drummertur, gauduk (+23) |
| `spabla` | Blacksmith | 5500 | 93.75 | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| `spacen` | Town Hall | 4250 | 156.25 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | peaaus, peaeng, peapol, pearus, peasco, peaspa (+2) |
| `spadip` | Diplomatic Center | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip, lightcavalrydip (+2) |
| `spahou` | Housing | 4200 | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| `spasta` | Stable | 20000 | 625.0 | 200 | 0 | 2500 | 100 | 600 | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier, dragoon (+24) |
| `spatem` | Cathedral | 4200 | 156.25 | 300 | 0 | 1000 | 1200 | 0 | 500 | 0 | 0 | mullah, padre, pope, priest |

#### rus — Russia

| sid | name | HP | Time (s) | cost% | F | W | S | G | I | C | farm | produces |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `eurcoa` | Mine | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | 0 | — |
| `eurgol` | Mine | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | 0 | — |
| `euriro` | Mine | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | 0 | — |
| `rusmar` | Market | 4000 | 234.38 | 2000 | 0 | 450 | 0 | 0 | 0 | 0 | 0 | — |
| `rusmil` | Mill | 15000 | 93.75 | 200 | 0 | 210 | 0 | 0 | 0 | 0 | 0 | field |
| `ruspor` | Shipyard | 45000 | 1562.5 | 150 | 0 | 1200 | 800 | 0 | 400 | 0 | 0 | battleship, chaika, ferry, fishboat, frigate, galley (+3) |
| `russga` | Gate | 50000 | 200.0 | 0 | 0 | 0 | 60 | 0 | 0 | 0 | 0 | — |
| `russto` | Storehouse | 10000 | 31.25 | 200 | 0 | 50 | 20 | 0 | 0 | 0 | 0 | — |
| `russwa` | Wall | 50000 | 200.0 | 0 | 0 | 0 | 60 | 0 | 0 | 0 | 0 | — |
| `rustow` | Tower | 21000 | 1476.56 | 125 | 0 | 100 | 100 | 150 | 0 | 0 | 0 | — |
| `rusaca` | Academy | 65000 | 843.75 | 300 | 0 | 1250 | 1300 | 0 | 0 | 0 | 0 | — |
| `rusart` | Artillery Depot | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |
| `rusba2` | Barracks, 18th century | 55000 | 5625.0 | 200 | 0 | 1700 | 2950 | 4000 | 0 | 0 | 250 | archersco, bagpiper, chasseur, drummer18, grenadier, grenadierbav (+18) |
| `rusbar` | Strelets Barracks | 25000 | 78.12 | 300 | 0 | 200 | 20 | 0 | 0 | 0 | 25 | archer, archertur, drummer, drummerrus, drummertur, gauduk (+23) |
| `rusbla` | Blacksmith | 5500 | 93.75 | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| `ruscen` | Town Hall | 4050 | 156.25 | 300 | 0 | 680 | 700 | 0 | 0 | 0 | 75 | peaaus, peaeng, peapol, pearus, peasco, peaspa (+2) |
| `rusdip` | Diplomatic Center | 6500 | 312.5 | 100 | 0 | 7900 | 3700 | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip, lightcavalrydip (+2) |
| `rushou` | Izba | 5000 | 31.25 | 104 | 0 | 120 | 0 | 0 | 0 | 0 | 25 | — |
| `russta` | Stable | 25000 | 375.0 | 200 | 0 | 7950 | 0 | 550 | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier, dragoon (+24) |
| `rustem` | Orthodox Cathedral | 4500 | 156.25 | 300 | 0 | 1150 | 1650 | 100 | 500 | 0 | 0 | mullah, padre, pope, priest |

#### ukr — Ukraine

| sid | name | HP | Time (s) | cost% | F | W | S | G | I | C | farm | produces |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `eurcoa` | Mine | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | 0 | — |
| `eurgol` | Mine | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | 0 | — |
| `euriro` | Mine | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | 0 | — |
| `rusmar` | Market | 4000 | 234.38 | 2000 | 0 | 450 | 0 | 0 | 0 | 0 | 0 | — |
| `rusmil` | Mill | 15000 | 93.75 | 200 | 0 | 210 | 0 | 0 | 0 | 0 | 0 | field |
| `russto` | Storehouse | 10000 | 31.25 | 200 | 0 | 50 | 20 | 0 | 0 | 0 | 0 | — |
| `ukrpor` | Shipyard | 45000 | 1562.5 | 150 | 0 | 2000 | 0 | 0 | 0 | 0 | 0 | battleship, chaika, ferry, fishboat, frigate, galley (+3) |
| `ukraca` | Academy | 65000 | 46.88 | 300 | 0 | 1350 | 1200 | 0 | 0 | 0 | 0 | — |
| `ukrart` | Artillery Depot | 40000 | 245.94 | 200 | 0 | 4250 | 4400 | 100 | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |
| `ukrbar` | Cossack House | 20000 | 93.75 | 300 | 0 | 150 | 150 | 0 | 0 | 0 | 75 | archer, archertur, drummer, drummerrus, drummertur, gauduk (+23) |
| `ukrbla` | Blacksmith | 4500 | 62.5 | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| `ukrcen` | Town Hall | 5300 | 156.25 | 400 | 0 | 700 | 0 | 0 | 0 | 0 | 200 | peaaus, peaeng, peapol, pearus, peasco, peaspa (+2) |
| `ukrdip` | Diplomatic Center | 5000 | 312.5 | 100 | 0 | 3900 | 2700 | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip, lightcavalrydip (+2) |
| `ukrhou` | Hut | 4150 | 31.25 | 105 | 0 | 120 | 0 | 0 | 0 | 0 | 25 | — |
| `ukrsta` | Stable | 10000 | 156.25 | 300 | 0 | 3200 | 850 | 850 | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier, dragoon (+24) |
| `ukrtem` | Orthodox Cathedral | 5300 | 156.25 | 300 | 0 | 1100 | 1400 | 0 | 300 | 0 | 0 | mullah, padre, pope, priest |

#### pol — Poland

| sid | name | HP | Time (s) | cost% | F | W | S | G | I | C | farm | produces |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `eurcoa` | Mine | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | 0 | — |
| `eurgol` | Mine | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | 0 | — |
| `euriro` | Mine | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | 0 | — |
| `eurmar` | Market | 4000 | 234.38 | 2000 | 0 | 450 | 0 | 0 | 0 | 0 | 0 | — |
| `eurmil` | Mill | 20000 | 93.75 | 200 | 0 | 30 | 150 | 0 | 0 | 0 | 0 | field |
| `eurpor` | Shipyard | 50000 | 1562.5 | 150 | 0 | 1600 | 800 | 0 | 400 | 0 | 0 | battleship, chaika, ferry, fishboat, frigate, galley (+3) |
| `eursga` | Gate | 50000 | 90.0 | 0 | 0 | 0 | 50 | 0 | 0 | 0 | 0 | — |
| `eurswa` | Wall | 50000 | 90.0 | 0 | 0 | 0 | 50 | 0 | 0 | 0 | 0 | — |
| `eurtow` | Tower | 20000 | 1230.31 | 120 | 0 | 100 | 100 | 150 | 0 | 0 | 0 | — |
| `russto` | Storehouse | 10000 | 31.25 | 200 | 0 | 50 | 20 | 0 | 0 | 0 | 0 | — |
| `polaca` | Academy | 63000 | 625.0 | 300 | 0 | 950 | 800 | 0 | 0 | 0 | 0 | — |
| `polart` | Artillery Depot | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |
| `polba2` | Barracks, 18th century | 55000 | 5625.0 | 200 | 0 | 1700 | 2950 | 4000 | 0 | 0 | 250 | archersco, bagpiper, chasseur, drummer18, grenadier, grenadierbav (+18) |
| `polbar` | Barracks, 17th century | 40000 | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | archer, archertur, drummer, drummerrus, drummertur, gauduk (+23) |
| `polbla` | Blacksmith | 5500 | 93.75 | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| `polcen` | Town Hall | 4300 | 156.25 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | peaaus, peaeng, peapol, pearus, peasco, peaspa (+2) |
| `poldip` | Diplomatic Center | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip, lightcavalrydip (+2) |
| `polhou` | Housing | 4100 | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| `polsta` | Stable | 20000 | 625.0 | 200 | 0 | 2500 | 100 | 600 | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier, dragoon (+24) |
| `poltem` | Cathedral | 4200 | 156.25 | 300 | 0 | 1000 | 1200 | 0 | 500 | 0 | 0 | mullah, padre, pope, priest |

#### swe — Sweden

| sid | name | HP | Time (s) | cost% | F | W | S | G | I | C | farm | produces |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `eurcoa` | Mine | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | 0 | — |
| `eurgol` | Mine | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | 0 | — |
| `euriro` | Mine | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | 0 | — |
| `eurmar` | Market | 4000 | 234.38 | 2000 | 0 | 450 | 0 | 0 | 0 | 0 | 0 | — |
| `eurmil` | Mill | 20000 | 93.75 | 200 | 0 | 30 | 150 | 0 | 0 | 0 | 0 | field |
| `eurpor` | Shipyard | 50000 | 1562.5 | 150 | 0 | 1600 | 800 | 0 | 400 | 0 | 0 | battleship, chaika, ferry, fishboat, frigate, galley (+3) |
| `eursga` | Gate | 50000 | 90.0 | 0 | 0 | 0 | 50 | 0 | 0 | 0 | 0 | — |
| `eursto` | Storehouse | 10000 | 31.25 | 150 | 0 | 50 | 20 | 0 | 0 | 0 | 0 | — |
| `eurswa` | Wall | 50000 | 90.0 | 0 | 0 | 0 | 50 | 0 | 0 | 0 | 0 | — |
| `eurtow` | Tower | 20000 | 1230.31 | 120 | 0 | 100 | 100 | 150 | 0 | 0 | 0 | — |
| `sweaca` | Academy | 63000 | 625.0 | 300 | 0 | 1350 | 1000 | 0 | 0 | 0 | 0 | — |
| `sweart` | Artillery Depot | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |
| `sweba2` | Barracks, 18th century | 55000 | 5625.0 | 200 | 0 | 1700 | 2950 | 4000 | 0 | 0 | 250 | archersco, bagpiper, chasseur, drummer18, grenadier, grenadierbav (+18) |
| `swebar` | Barracks, 17th century | 40000 | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | archer, archertur, drummer, drummerrus, drummertur, gauduk (+23) |
| `swebla` | Blacksmith | 5500 | 93.75 | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| `swecen` | Town Hall | 5000 | 156.25 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | peaaus, peaeng, peapol, pearus, peasco, peaspa (+2) |
| `swedip` | Diplomatic Center | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip, lightcavalrydip (+2) |
| `swehou` | Housing | 5000 | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| `swesta` | Stable | 20000 | 625.0 | 200 | 0 | 2500 | 100 | 600 | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier, dragoon (+24) |
| `swetem` | Cathedral | 4200 | 156.25 | 300 | 0 | 1000 | 1200 | 0 | 500 | 0 | 0 | mullah, padre, pope, priest |

#### pru — Prussia

| sid | name | HP | Time (s) | cost% | F | W | S | G | I | C | farm | produces |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `eurcoa` | Mine | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | 0 | — |
| `eurgol` | Mine | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | 0 | — |
| `euriro` | Mine | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | 0 | — |
| `eurmar` | Market | 4000 | 234.38 | 2000 | 0 | 450 | 0 | 0 | 0 | 0 | 0 | — |
| `eurmil` | Mill | 20000 | 93.75 | 200 | 0 | 30 | 150 | 0 | 0 | 0 | 0 | field |
| `eurpor` | Shipyard | 50000 | 1562.5 | 150 | 0 | 1600 | 800 | 0 | 400 | 0 | 0 | battleship, chaika, ferry, fishboat, frigate, galley (+3) |
| `eursga` | Gate | 50000 | 90.0 | 0 | 0 | 0 | 50 | 0 | 0 | 0 | 0 | — |
| `eursto` | Storehouse | 10000 | 31.25 | 150 | 0 | 50 | 20 | 0 | 0 | 0 | 0 | — |
| `eurswa` | Wall | 50000 | 90.0 | 0 | 0 | 0 | 50 | 0 | 0 | 0 | 0 | — |
| `eurtow` | Tower | 20000 | 1230.31 | 120 | 0 | 100 | 100 | 150 | 0 | 0 | 0 | — |
| `pruaca` | Academy | 63000 | 625.0 | 300 | 0 | 1200 | 1150 | 0 | 0 | 0 | 0 | — |
| `pruart` | Artillery Depot | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |
| `pruba2` | Barracks, 18th century | 55000 | 5625.0 | 200 | 0 | 1700 | 2950 | 4000 | 0 | 0 | 250 | archersco, bagpiper, chasseur, drummer18, grenadier, grenadierbav (+18) |
| `prubar` | Barracks, 17th century | 40000 | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | archer, archertur, drummer, drummerrus, drummertur, gauduk (+23) |
| `prubla` | Blacksmith | 5500 | 93.75 | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| `prucen` | Town Hall | 4200 | 156.25 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | peaaus, peaeng, peapol, pearus, peasco, peaspa (+2) |
| `prudip` | Diplomatic Center | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip, lightcavalrydip (+2) |
| `pruhou` | Housing | 4500 | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| `prusta` | Stable | 20000 | 625.0 | 200 | 0 | 2500 | 100 | 600 | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier, dragoon (+24) |
| `prutem` | Cathedral | 4200 | 156.25 | 300 | 0 | 1000 | 1200 | 0 | 500 | 0 | 0 | mullah, padre, pope, priest |

#### ven — Venice

| sid | name | HP | Time (s) | cost% | F | W | S | G | I | C | farm | produces |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `eurcoa` | Mine | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | 0 | — |
| `eurgol` | Mine | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | 0 | — |
| `euriro` | Mine | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | 0 | — |
| `eurmar` | Market | 4000 | 234.38 | 2000 | 0 | 450 | 0 | 0 | 0 | 0 | 0 | — |
| `eurmil` | Mill | 20000 | 93.75 | 200 | 0 | 30 | 150 | 0 | 0 | 0 | 0 | field |
| `eurpor` | Shipyard | 50000 | 1562.5 | 150 | 0 | 1600 | 800 | 0 | 400 | 0 | 0 | battleship, chaika, ferry, fishboat, frigate, galley (+3) |
| `eursga` | Gate | 50000 | 90.0 | 0 | 0 | 0 | 50 | 0 | 0 | 0 | 0 | — |
| `eursto` | Storehouse | 10000 | 31.25 | 150 | 0 | 50 | 20 | 0 | 0 | 0 | 0 | — |
| `eurswa` | Wall | 50000 | 90.0 | 0 | 0 | 0 | 50 | 0 | 0 | 0 | 0 | — |
| `eurtow` | Tower | 20000 | 1230.31 | 120 | 0 | 100 | 100 | 150 | 0 | 0 | 0 | — |
| `venaca` | Academy | 63000 | 625.0 | 300 | 0 | 1090 | 1260 | 0 | 0 | 0 | 0 | — |
| `venart` | Artillery Depot | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |
| `venba2` | Barracks, 18th century | 55000 | 5625.0 | 200 | 0 | 1700 | 2950 | 4000 | 0 | 0 | 250 | archersco, bagpiper, chasseur, drummer18, grenadier, grenadierbav (+18) |
| `venbar` | Barracks, 17th century | 40000 | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | archer, archertur, drummer, drummerrus, drummertur, gauduk (+23) |
| `venbla` | Blacksmith | 5500 | 93.75 | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| `vencen` | Town Hall | 5100 | 156.25 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | peaaus, peaeng, peapol, pearus, peasco, peaspa (+2) |
| `vendip` | Diplomatic Center | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip, lightcavalrydip (+2) |
| `venhou` | Housing | 5000 | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| `vensta` | Stable | 20000 | 625.0 | 200 | 0 | 2500 | 100 | 600 | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier, dragoon (+24) |
| `ventem` | Cathedral | 4200 | 156.25 | 300 | 0 | 1000 | 1200 | 0 | 500 | 0 | 0 | mullah, padre, pope, priest |

#### tur — Turkey

| sid | name | HP | Time (s) | cost% | F | W | S | G | I | C | farm | produces |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `eurcoa` | Mine | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | 0 | — |
| `eurgol` | Mine | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | 0 | — |
| `euriro` | Mine | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | 0 | — |
| `turmar` | Bazaar | 4500 | 234.38 | 1500 | 0 | 450 | 150 | 0 | 0 | 0 | 0 | — |
| `turmil` | Mill | 20000 | 93.75 | 200 | 0 | 30 | 150 | 0 | 0 | 0 | 0 | field |
| `turpor` | Shipyard | 40000 | 1562.5 | 150 | 0 | 800 | 800 | 0 | 400 | 0 | 0 | battleship, chaika, ferry, fishboat, frigate, galley (+3) |
| `tursga` | Gate | 50000 | 120.0 | 0 | 0 | 0 | 60 | 0 | 0 | 0 | 0 | — |
| `tursto` | Storehouse | 10000 | 31.25 | 200 | 0 | 30 | 10 | 0 | 0 | 0 | 0 | — |
| `turswa` | Wall | 50000 | 120.0 | 0 | 0 | 0 | 60 | 0 | 0 | 0 | 0 | — |
| `turtow` | Tower | 22500 | 984.38 | 125 | 0 | 150 | 90 | 100 | 0 | 0 | 0 | — |
| `turaca` | Minaret | 65000 | 156.25 | 300 | 0 | 1450 | 1100 | 0 | 0 | 0 | 0 | — |
| `turart` | Artillery Depot | 40000 | 245.94 | 200 | 0 | 500 | 1200 | 0 | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |
| `turbar` | Barracks | 35000 | 93.75 | 500 | 0 | 400 | 400 | 0 | 0 | 0 | 50 | archer, archertur, drummer, drummerrus, drummertur, gauduk (+23) |
| `turbla` | Blacksmith | 6500 | 109.38 | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| `turcen` | Town Hall | 4000 | 156.25 | 300 | 0 | 600 | 500 | 0 | 0 | 0 | 100 | peaaus, peaeng, peapol, pearus, peasco, peaspa (+2) |
| `turdip` | Diplomatic Center | 5500 | 312.5 | 100 | 0 | 4600 | 2020 | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip, lightcavalrydip (+2) |
| `turhou` | Housing | 4000 | 31.25 | 106 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| `tursta` | Stable | 55000 | 156.25 | 700 | 0 | 1000 | 2600 | 0 | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier, dragoon (+24) |
| `turtem` | Mosque | 5000 | 93.75 | 300 | 0 | 1000 | 1200 | 0 | 500 | 0 | 0 | mullah, padre, pope, priest |

#### alg — Algeria

| sid | name | HP | Time (s) | cost% | F | W | S | G | I | C | farm | produces |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `eurcoa` | Mine | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | 0 | — |
| `eurgol` | Mine | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | 0 | — |
| `euriro` | Mine | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | 0 | — |
| `turmar` | Bazaar | 4500 | 234.38 | 1500 | 0 | 450 | 150 | 0 | 0 | 0 | 0 | — |
| `turmil` | Mill | 20000 | 93.75 | 200 | 0 | 30 | 150 | 0 | 0 | 0 | 0 | field |
| `turpor` | Shipyard | 40000 | 1562.5 | 150 | 0 | 800 | 800 | 0 | 400 | 0 | 0 | battleship, chaika, ferry, fishboat, frigate, galley (+3) |
| `tursga` | Gate | 50000 | 120.0 | 0 | 0 | 0 | 60 | 0 | 0 | 0 | 0 | — |
| `tursto` | Storehouse | 10000 | 31.25 | 200 | 0 | 30 | 10 | 0 | 0 | 0 | 0 | — |
| `turswa` | Wall | 50000 | 120.0 | 0 | 0 | 0 | 60 | 0 | 0 | 0 | 0 | — |
| `turtow` | Tower | 22500 | 984.38 | 125 | 0 | 150 | 90 | 100 | 0 | 0 | 0 | — |
| `algaca` | Minaret | 65000 | 156.25 | 300 | 0 | 1450 | 1100 | 0 | 0 | 0 | 0 | — |
| `algart` | Artillery Depot | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |
| `algbar` | Barracks | 35000 | 93.75 | 500 | 0 | 400 | 400 | 0 | 0 | 0 | 50 | archer, archertur, drummer, drummerrus, drummertur, gauduk (+23) |
| `algbla` | Blacksmith | 6500 | 109.38 | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| `algcen` | Town Hall | 5500 | 156.25 | 300 | 0 | 450 | 700 | 0 | 0 | 0 | 50 | peaaus, peaeng, peapol, pearus, peasco, peaspa (+2) |
| `algdip` | Diplomatic Center | 5500 | 312.5 | 100 | 0 | 4600 | 2020 | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip, lightcavalrydip (+2) |
| `alghou` | Housing | 4300 | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| `algsta` | Stable | 55000 | 156.25 | 700 | 0 | 1000 | 2200 | 0 | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier, dragoon (+24) |
| `algtem` | Mosque | 5000 | 93.75 | 300 | 0 | 1000 | 1200 | 0 | 500 | 0 | 0 | mullah, padre, pope, priest |

#### net — Netherlands

| sid | name | HP | Time (s) | cost% | F | W | S | G | I | C | farm | produces |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `eurcoa` | Mine | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | 0 | — |
| `eurgol` | Mine | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | 0 | — |
| `euriro` | Mine | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | 0 | — |
| `eurmar` | Market | 4000 | 234.38 | 2000 | 0 | 450 | 0 | 0 | 0 | 0 | 0 | — |
| `eurmil` | Mill | 20000 | 93.75 | 200 | 0 | 30 | 150 | 0 | 0 | 0 | 0 | field |
| `eurpor` | Shipyard | 50000 | 1562.5 | 150 | 0 | 1600 | 800 | 0 | 400 | 0 | 0 | battleship, chaika, ferry, fishboat, frigate, galley (+3) |
| `eursga` | Gate | 50000 | 90.0 | 0 | 0 | 0 | 50 | 0 | 0 | 0 | 0 | — |
| `eursto` | Storehouse | 10000 | 31.25 | 150 | 0 | 50 | 20 | 0 | 0 | 0 | 0 | — |
| `eurswa` | Wall | 50000 | 90.0 | 0 | 0 | 0 | 50 | 0 | 0 | 0 | 0 | — |
| `eurtow` | Tower | 20000 | 1230.31 | 120 | 0 | 100 | 100 | 150 | 0 | 0 | 0 | — |
| `netaca` | Academy | 63000 | 625.0 | 300 | 0 | 1050 | 1230 | 0 | 0 | 0 | 0 | — |
| `netart` | Artillery Depot | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |
| `netba2` | Barracks, 18th century | 55000 | 5625.0 | 200 | 0 | 1700 | 2950 | 4000 | 0 | 0 | 250 | archersco, bagpiper, chasseur, drummer18, grenadier, grenadierbav (+18) |
| `netbar` | Barracks, 17th century | 40000 | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | archer, archertur, drummer, drummerrus, drummertur, gauduk (+23) |
| `netbla` | Blacksmith | 5500 | 93.75 | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| `netcen` | Town Hall | 4950 | 156.25 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | peaaus, peaeng, peapol, pearus, peasco, peaspa (+2) |
| `netdip` | Diplomatic Center | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip, lightcavalrydip (+2) |
| `nethou` | Housing | 4500 | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| `netsta` | Stable | 20000 | 625.0 | 200 | 0 | 2500 | 100 | 600 | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier, dragoon (+24) |
| `nettem` | Cathedral | 4200 | 156.25 | 300 | 0 | 1000 | 1200 | 0 | 500 | 0 | 0 | mullah, padre, pope, priest |

#### den — Denmark

| sid | name | HP | Time (s) | cost% | F | W | S | G | I | C | farm | produces |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `eurcoa` | Mine | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | 0 | — |
| `eurgol` | Mine | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | 0 | — |
| `euriro` | Mine | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | 0 | — |
| `eurmar` | Market | 4000 | 234.38 | 2000 | 0 | 450 | 0 | 0 | 0 | 0 | 0 | — |
| `eurmil` | Mill | 20000 | 93.75 | 200 | 0 | 30 | 150 | 0 | 0 | 0 | 0 | field |
| `eurpor` | Shipyard | 50000 | 1562.5 | 150 | 0 | 1600 | 800 | 0 | 400 | 0 | 0 | battleship, chaika, ferry, fishboat, frigate, galley (+3) |
| `eursga` | Gate | 50000 | 90.0 | 0 | 0 | 0 | 50 | 0 | 0 | 0 | 0 | — |
| `eursto` | Storehouse | 10000 | 31.25 | 150 | 0 | 50 | 20 | 0 | 0 | 0 | 0 | — |
| `eurswa` | Wall | 50000 | 90.0 | 0 | 0 | 0 | 50 | 0 | 0 | 0 | 0 | — |
| `eurtow` | Tower | 20000 | 1230.31 | 120 | 0 | 100 | 100 | 150 | 0 | 0 | 0 | — |
| `denaca` | Academy | 63000 | 625.0 | 300 | 0 | 1450 | 900 | 0 | 0 | 0 | 0 | — |
| `denart` | Artillery Depot | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |
| `denba2` | Barracks, 18th century | 55000 | 5625.0 | 200 | 0 | 1700 | 2950 | 4000 | 0 | 0 | 250 | archersco, bagpiper, chasseur, drummer18, grenadier, grenadierbav (+18) |
| `denbar` | Barracks, 17th century | 40000 | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | archer, archertur, drummer, drummerrus, drummertur, gauduk (+23) |
| `denbla` | Blacksmith | 5500 | 93.75 | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| `dencen` | Town Hall | 4030 | 156.25 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | peaaus, peaeng, peapol, pearus, peasco, peaspa (+2) |
| `dendip` | Diplomatic Center | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip, lightcavalrydip (+2) |
| `denhou` | Housing | 4000 | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| `densta` | Stable | 20000 | 625.0 | 200 | 0 | 2500 | 100 | 600 | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier, dragoon (+24) |
| `dentem` | Cathedral | 4200 | 156.25 | 300 | 0 | 1000 | 1200 | 0 | 500 | 0 | 0 | mullah, padre, pope, priest |

#### por — Portugal

| sid | name | HP | Time (s) | cost% | F | W | S | G | I | C | farm | produces |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `eurcoa` | Mine | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | 0 | — |
| `eurgol` | Mine | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | 0 | — |
| `euriro` | Mine | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | 0 | — |
| `eurmil` | Mill | 20000 | 93.75 | 200 | 0 | 30 | 150 | 0 | 0 | 0 | 0 | field |
| `eursga` | Gate | 50000 | 90.0 | 0 | 0 | 0 | 50 | 0 | 0 | 0 | 0 | — |
| `eurswa` | Wall | 50000 | 90.0 | 0 | 0 | 0 | 50 | 0 | 0 | 0 | 0 | — |
| `eurtow` | Tower | 20000 | 1230.31 | 120 | 0 | 100 | 100 | 150 | 0 | 0 | 0 | — |
| `porpor` | Shipyard | 50000 | 1562.5 | 150 | 0 | 1600 | 800 | 0 | 400 | 0 | 0 | battleship, chaika, ferry, fishboat, frigate, galley (+3) |
| `spamar` | Market | 4000 | 156.25 | 2000 | 0 | 450 | 0 | 0 | 0 | 0 | 0 | — |
| `spasto` | Storehouse | 10000 | 31.25 | 150 | 0 | 20 | 20 | 0 | 0 | 0 | 0 | — |
| `poraca` | Academy | 63000 | 625.0 | 300 | 0 | 1250 | 1100 | 0 | 0 | 0 | 0 | — |
| `porart` | Artillery Depot | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |
| `porba2` | Barracks, 18th century | 55000 | 5625.0 | 200 | 0 | 1700 | 2950 | 4000 | 0 | 0 | 250 | archersco, bagpiper, chasseur, drummer18, grenadier, grenadierbav (+18) |
| `porbar` | Barracks, 17th century | 40000 | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | archer, archertur, drummer, drummerrus, drummertur, gauduk (+23) |
| `porbla` | Blacksmith | 5500 | 93.75 | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| `porcen` | Town Hall | 4000 | 156.25 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | peaaus, peaeng, peapol, pearus, peasco, peaspa (+2) |
| `pordip` | Diplomatic Center | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip, lightcavalrydip (+2) |
| `porhou` | Housing | 4000 | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| `porsta` | Stable | 20000 | 625.0 | 200 | 0 | 2500 | 100 | 600 | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier, dragoon (+24) |
| `portem` | Cathedral | 4200 | 156.25 | 300 | 0 | 1000 | 1200 | 0 | 500 | 0 | 0 | mullah, padre, pope, priest |

#### pie — Piedmont

| sid | name | HP | Time (s) | cost% | F | W | S | G | I | C | farm | produces |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `eurcoa` | Mine | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | 0 | — |
| `eurgol` | Mine | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | 0 | — |
| `euriro` | Mine | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | 0 | — |
| `eurmar` | Market | 4000 | 234.38 | 2000 | 0 | 450 | 0 | 0 | 0 | 0 | 0 | — |
| `eurmil` | Mill | 20000 | 93.75 | 200 | 0 | 30 | 150 | 0 | 0 | 0 | 0 | field |
| `eurpor` | Shipyard | 50000 | 1562.5 | 150 | 0 | 1600 | 800 | 0 | 400 | 0 | 0 | battleship, chaika, ferry, fishboat, frigate, galley (+3) |
| `eursga` | Gate | 50000 | 90.0 | 0 | 0 | 0 | 50 | 0 | 0 | 0 | 0 | — |
| `eursto` | Storehouse | 10000 | 31.25 | 150 | 0 | 50 | 20 | 0 | 0 | 0 | 0 | — |
| `eurswa` | Wall | 50000 | 90.0 | 0 | 0 | 0 | 50 | 0 | 0 | 0 | 0 | — |
| `eurtow` | Tower | 20000 | 1230.31 | 120 | 0 | 100 | 100 | 150 | 0 | 0 | 0 | — |
| `pieaca` | Academy | 63000 | 625.0 | 300 | 0 | 1250 | 1100 | 0 | 0 | 0 | 0 | — |
| `pieart` | Artillery Depot | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |
| `pieba2` | Barracks, 18th century | 55000 | 5625.0 | 200 | 0 | 1700 | 2950 | 4000 | 0 | 0 | 250 | archersco, bagpiper, chasseur, drummer18, grenadier, grenadierbav (+18) |
| `piebar` | Barracks, 17th century | 40000 | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | archer, archertur, drummer, drummerrus, drummertur, gauduk (+23) |
| `piebla` | Blacksmith | 5500 | 93.75 | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| `piecen` | Town Hall | 4000 | 156.25 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | peaaus, peaeng, peapol, pearus, peasco, peaspa (+2) |
| `piedip` | Diplomatic Center | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip, lightcavalrydip (+2) |
| `piehou` | Housing | 4000 | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| `piesta` | Stable | 20000 | 625.0 | 200 | 0 | 2500 | 100 | 600 | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier, dragoon (+24) |
| `pietem` | Cathedral | 4200 | 156.25 | 300 | 0 | 1000 | 1200 | 0 | 500 | 0 | 0 | mullah, padre, pope, priest |

#### sax — Saxony

| sid | name | HP | Time (s) | cost% | F | W | S | G | I | C | farm | produces |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `eurcoa` | Mine | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | 0 | — |
| `eurgol` | Mine | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | 0 | — |
| `euriro` | Mine | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | 0 | — |
| `eurmar` | Market | 4000 | 234.38 | 2000 | 0 | 450 | 0 | 0 | 0 | 0 | 0 | — |
| `eurmil` | Mill | 20000 | 93.75 | 200 | 0 | 30 | 150 | 0 | 0 | 0 | 0 | field |
| `eurpor` | Shipyard | 50000 | 1562.5 | 150 | 0 | 1600 | 800 | 0 | 400 | 0 | 0 | battleship, chaika, ferry, fishboat, frigate, galley (+3) |
| `eursga` | Gate | 50000 | 90.0 | 0 | 0 | 0 | 50 | 0 | 0 | 0 | 0 | — |
| `eursto` | Storehouse | 10000 | 31.25 | 150 | 0 | 50 | 20 | 0 | 0 | 0 | 0 | — |
| `eurswa` | Wall | 50000 | 90.0 | 0 | 0 | 0 | 50 | 0 | 0 | 0 | 0 | — |
| `eurtow` | Tower | 20000 | 1230.31 | 120 | 0 | 100 | 100 | 150 | 0 | 0 | 0 | — |
| `saxaca` | Academy | 63000 | 625.0 | 300 | 0 | 1250 | 1100 | 0 | 0 | 0 | 0 | — |
| `saxart` | Artillery Depot | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |
| `saxba2` | Barracks, 18th century | 55000 | 5625.0 | 200 | 0 | 1700 | 2950 | 4000 | 0 | 0 | 250 | archersco, bagpiper, chasseur, drummer18, grenadier, grenadierbav (+18) |
| `saxbar` | Barracks, 17th century | 40000 | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | archer, archertur, drummer, drummerrus, drummertur, gauduk (+23) |
| `saxbla` | Blacksmith | 5500 | 93.75 | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| `saxcen` | Town Hall | 4000 | 156.25 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | peaaus, peaeng, peapol, pearus, peasco, peaspa (+2) |
| `saxdip` | Diplomatic Center | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip, lightcavalrydip (+2) |
| `saxhou` | Housing | 4000 | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| `saxsta` | Stable | 20000 | 625.0 | 200 | 0 | 2500 | 100 | 600 | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier, dragoon (+24) |
| `saxtem` | Cathedral | 4200 | 156.25 | 300 | 0 | 1000 | 1200 | 0 | 500 | 0 | 0 | mullah, padre, pope, priest |

#### bav — Bavaria

| sid | name | HP | Time (s) | cost% | F | W | S | G | I | C | farm | produces |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `eurcoa` | Mine | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | 0 | — |
| `eurgol` | Mine | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | 0 | — |
| `euriro` | Mine | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | 0 | — |
| `eurmar` | Market | 4000 | 234.38 | 2000 | 0 | 450 | 0 | 0 | 0 | 0 | 0 | — |
| `eurmil` | Mill | 20000 | 93.75 | 200 | 0 | 30 | 150 | 0 | 0 | 0 | 0 | field |
| `eurpor` | Shipyard | 50000 | 1562.5 | 150 | 0 | 1600 | 800 | 0 | 400 | 0 | 0 | battleship, chaika, ferry, fishboat, frigate, galley (+3) |
| `eursga` | Gate | 50000 | 90.0 | 0 | 0 | 0 | 50 | 0 | 0 | 0 | 0 | — |
| `eursto` | Storehouse | 10000 | 31.25 | 150 | 0 | 50 | 20 | 0 | 0 | 0 | 0 | — |
| `eurswa` | Wall | 50000 | 90.0 | 0 | 0 | 0 | 50 | 0 | 0 | 0 | 0 | — |
| `eurtow` | Tower | 20000 | 1230.31 | 120 | 0 | 100 | 100 | 150 | 0 | 0 | 0 | — |
| `bavaca` | Academy | 63000 | 625.0 | 300 | 0 | 1250 | 1100 | 0 | 0 | 0 | 0 | — |
| `bavart` | Artillery Depot | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |
| `bavba2` | Barracks, 18th century | 55000 | 5625.0 | 200 | 0 | 1700 | 2950 | 4000 | 0 | 0 | 250 | archersco, bagpiper, chasseur, drummer18, grenadier, grenadierbav (+18) |
| `bavbar` | Barracks, 17th century | 40000 | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | archer, archertur, drummer, drummerrus, drummertur, gauduk (+23) |
| `bavbla` | Blacksmith | 5500 | 93.75 | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| `bavcen` | Town Hall | 4000 | 156.25 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | peaaus, peaeng, peapol, pearus, peasco, peaspa (+2) |
| `bavdip` | Diplomatic Center | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip, lightcavalrydip (+2) |
| `bavhou` | Housing | 4000 | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| `bavsta` | Stable | 20000 | 625.0 | 200 | 0 | 2500 | 100 | 600 | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier, dragoon (+24) |
| `bavtem` | Cathedral | 4200 | 156.25 | 300 | 0 | 1000 | 1200 | 0 | 500 | 0 | 0 | mullah, padre, pope, priest |

#### hun — Hungary

| sid | name | HP | Time (s) | cost% | F | W | S | G | I | C | farm | produces |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `eurcoa` | Mine | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | 0 | — |
| `eurgol` | Mine | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | 0 | — |
| `euriro` | Mine | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | 0 | — |
| `eurmar` | Market | 4000 | 234.38 | 2000 | 0 | 450 | 0 | 0 | 0 | 0 | 0 | — |
| `eurmil` | Mill | 20000 | 93.75 | 200 | 0 | 30 | 150 | 0 | 0 | 0 | 0 | field |
| `eurpor` | Shipyard | 50000 | 1562.5 | 150 | 0 | 1600 | 800 | 0 | 400 | 0 | 0 | battleship, chaika, ferry, fishboat, frigate, galley (+3) |
| `eursga` | Gate | 50000 | 90.0 | 0 | 0 | 0 | 50 | 0 | 0 | 0 | 0 | — |
| `eursto` | Storehouse | 10000 | 31.25 | 150 | 0 | 50 | 20 | 0 | 0 | 0 | 0 | — |
| `eurswa` | Wall | 50000 | 90.0 | 0 | 0 | 0 | 50 | 0 | 0 | 0 | 0 | — |
| `eurtow` | Tower | 20000 | 1230.31 | 120 | 0 | 100 | 100 | 150 | 0 | 0 | 0 | — |
| `hunaca` | Academy | 63000 | 625.0 | 300 | 0 | 1250 | 1100 | 0 | 0 | 0 | 0 | — |
| `hunart` | Artillery Depot | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |
| `hunba2` | Barracks, 18th century | 55000 | 5625.0 | 200 | 0 | 1700 | 2950 | 4000 | 0 | 0 | 250 | archersco, bagpiper, chasseur, drummer18, grenadier, grenadierbav (+18) |
| `hunbar` | Barracks, 17th century | 40000 | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | archer, archertur, drummer, drummerrus, drummertur, gauduk (+23) |
| `hunbla` | Blacksmith | 5500 | 93.75 | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| `huncen` | Town Hall | 4000 | 156.25 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | peaaus, peaeng, peapol, pearus, peasco, peaspa (+2) |
| `hundip` | Diplomatic Center | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip, lightcavalrydip (+2) |
| `hunhou` | Housing | 4000 | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| `hunsta` | Stable | 20000 | 625.0 | 200 | 0 | 2500 | 100 | 600 | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier, dragoon (+25) |
| `huntem` | Cathedral | 4200 | 156.25 | 300 | 0 | 1000 | 1200 | 0 | 500 | 0 | 0 | mullah, padre, pope, priest |

#### swi — Switzerland

| sid | name | HP | Time (s) | cost% | F | W | S | G | I | C | farm | produces |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `eurcoa` | Mine | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | 0 | — |
| `eurgol` | Mine | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | 0 | — |
| `euriro` | Mine | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | 0 | — |
| `eurmar` | Market | 4000 | 234.38 | 2000 | 0 | 450 | 0 | 0 | 0 | 0 | 0 | — |
| `eurmil` | Mill | 20000 | 93.75 | 200 | 0 | 30 | 150 | 0 | 0 | 0 | 0 | field |
| `eurpor` | Shipyard | 50000 | 1562.5 | 150 | 0 | 1600 | 800 | 0 | 400 | 0 | 0 | battleship, chaika, ferry, fishboat, frigate, galley (+3) |
| `eursga` | Gate | 50000 | 90.0 | 0 | 0 | 0 | 50 | 0 | 0 | 0 | 0 | — |
| `eursto` | Storehouse | 10000 | 31.25 | 150 | 0 | 50 | 20 | 0 | 0 | 0 | 0 | — |
| `eurswa` | Wall | 50000 | 90.0 | 0 | 0 | 0 | 50 | 0 | 0 | 0 | 0 | — |
| `eurtow` | Tower | 20000 | 1230.31 | 120 | 0 | 100 | 100 | 150 | 0 | 0 | 0 | — |
| `swiaca` | Academy | 63000 | 625.0 | 300 | 0 | 1250 | 1100 | 0 | 0 | 0 | 0 | — |
| `swiart` | Artillery Depot | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |
| `swiba2` | Barracks, 18th century | 55000 | 5625.0 | 200 | 0 | 1700 | 2950 | 4000 | 0 | 0 | 250 | archersco, bagpiper, chasseur, drummer18, grenadier, grenadierbav (+18) |
| `swibar` | Barracks, 17th century | 40000 | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | archer, archertur, drummer, drummerrus, drummertur, gauduk (+23) |
| `swibla` | Blacksmith | 5500 | 93.75 | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| `swicen` | Town Hall | 4000 | 156.25 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | peaaus, peaeng, peapol, pearus, peasco, peaspa (+2) |
| `swidip` | Diplomatic Center | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip, lightcavalrydip (+2) |
| `swihou` | Housing | 4000 | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| `swista` | Stable | 20000 | 625.0 | 200 | 0 | 2500 | 100 | 600 | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier, dragoon (+24) |
| `switem` | Cathedral | 4200 | 156.25 | 300 | 0 | 1000 | 1200 | 0 | 500 | 0 | 0 | mullah, padre, pope, priest |

#### sco — Scotland

| sid | name | HP | Time (s) | cost% | F | W | S | G | I | C | farm | produces |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `eurcoa` | Mine | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | 0 | — |
| `eurgol` | Mine | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | 0 | — |
| `euriro` | Mine | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | 0 | — |
| `eurmar` | Market | 4000 | 234.38 | 2000 | 0 | 450 | 0 | 0 | 0 | 0 | 0 | — |
| `eurmil` | Mill | 20000 | 93.75 | 200 | 0 | 30 | 150 | 0 | 0 | 0 | 0 | field |
| `eurpor` | Shipyard | 50000 | 1562.5 | 150 | 0 | 1600 | 800 | 0 | 400 | 0 | 0 | battleship, chaika, ferry, fishboat, frigate, galley (+3) |
| `eursga` | Gate | 50000 | 90.0 | 0 | 0 | 0 | 50 | 0 | 0 | 0 | 0 | — |
| `eursto` | Storehouse | 10000 | 31.25 | 150 | 0 | 50 | 20 | 0 | 0 | 0 | 0 | — |
| `eurswa` | Wall | 50000 | 90.0 | 0 | 0 | 0 | 50 | 0 | 0 | 0 | 0 | — |
| `eurtow` | Tower | 20000 | 1230.31 | 120 | 0 | 100 | 100 | 150 | 0 | 0 | 0 | — |
| `scoaca` | Academy | 63000 | 625.0 | 300 | 0 | 1250 | 1100 | 0 | 0 | 0 | 0 | — |
| `scoart` | Artillery Depot | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |
| `scoba2` | Castle | 40000 | 625.0 | 250 | 0 | 640 | 2400 | 2400 | 0 | 0 | 150 | archersco, chasseur, drummer18, grenadier, grenadierbav, grenadierden (+17) |
| `scobar` | Barracks, 17th century | 30000 | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | archer, archertur, bagpiper, drummer, drummerrus, drummertur (+24) |
| `scobla` | Blacksmith | 5500 | 93.75 | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| `scocen` | Town Hall | 4000 | 156.25 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | peaaus, peaeng, peapol, pearus, peasco, peaspa (+2) |
| `scodip` | Diplomatic Center | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip, lightcavalrydip (+2) |
| `scohou` | Housing | 4000 | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| `scosta` | Stable | 25000 | 375.0 | 200 | 0 | 2350 | 0 | 800 | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier, dragoon (+24) |
| `scotem` | Cathedral | 4200 | 156.25 | 300 | 0 | 1000 | 1200 | 0 | 500 | 0 | 0 | mullah, padre, pope, priest |

## 5. Юниты

Группировка по нациям. Цена дана в food / wood / stone / gold / iron / coal. Защиты — числа в диапазоне 0..240+ (выше = меньше получаемого урона по правилам игры).

### aus — Austria (38 юнитов)

| sid | name | usage | trained_in | uniqueness | HP | Time | F | G | I | dmg | rng (t) | reload | пика | меч | пуля | картечь | стрела | ядро |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `archerdip` | Archer (mercenary) | Archer | ausdip | common | 40 | 1.5 | 20 | 1 | 0 | 15 | 15.0 | 2.34 | — | — | — | — | — | — |
| `archerturdip` | Turkish archer (mercenary) | Archer | ausdip | common | 40 | 1.5 | 20 | 1 | 0 | 15 | 15.0 | 2.34 | — | — | — | — | — | — |
| `battleship` | Ship of the Line | Battleship | eurpor | common | 90000 | 390.0 | 0 | 3200 | 700 | 1800 | 36.56 | 0.62 | — | — | — | — | — | — |
| `cannon` | Cannon | Cannon | ausart | common | 9000 | 75.0 | 0 | 400 | 400 | 1800 | 40.5 | 10.94 | — | — | — | — | — | — |
| `cossacksichdip` | Sich Cossack (mercenary) | Light Cavalry | ausdip | common | 250 | 13.5 | 130 | 0 | 2 | 13 | 1.22 | 0.0 | — | — | — | — | — | — |
| `croat` | Croat | Light Cavalry | aussta | unique | 260 | 15.75 | 80 | 6 | 2 | 9 | 1.22 | 0.0 | — | — | — | — | — | — |
| `cuirassier` | Cuirassier | Heavy Cavalry | aussta | shared (17n) | 300 | 22.5 | 120 | 35 | 25 | 14 | 1.22 | 0.0 | 2 | 4 | 10 | 160 | 5 | 80 |
| `dragoon` | Dragoon, 17th century | Mounted Shooter | aussta | shared (16n) | 220 | 15.0 | 90 | 7 | 5 | 15 | 15.0 | 5.62 | — | — | — | — | — | — |
| `dragoon18` | Dragoon, 18th century | Mounted Shooter | aussta | shared (13n) | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | — | — | — | — | — | — |
| `dragoon18dip` | Dragoon, 18th century (mercenary) | Mounted Shooter | ausdip | common | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | — | — | — | — | — | — |
| `drummer` | Drummer, 17th century | Light Infantry | ausbar | shared (16n) | 75 | 6.0 | 50 | 30 | 0 | — | — | — | — | — | — | — | — | — |
| `drummer18` | Drummer, 18th century | Light Infantry | ausba2 | shared (16n) | 75 | 6.0 | 50 | 30 | 0 | — | — | — | — | — | — | — | — | — |
| `ferry` | Ferry | Transport | eurpor | common | 62000 | 56.0 | 0 | 50 | 100 | — | — | — | — | — | — | — | — | — |
| `fishboat` | Boat | Fishing Boat | eurpor | common | 300 | 40.0 | 0 | 0 | 0 | — | — | — | — | — | — | — | — | — |
| `frigate` | Frigate | Frigate | eurpor | common | 50000 | 230.0 | 0 | 1100 | 600 | 1800 | 30.94 | 2.34 | — | — | — | — | — | — |
| `galley` | Galley | Galley | eurpor | common | 35000 | 50.0 | 0 | 900 | 800 | 100 | 22.5 | 4.69 | — | — | — | — | — | — |
| `grenadier` | Grenadier | Grenadier | ausba2 | shared (13n) | 120 | 6.0 | 80 | 60 | 40 | 18 | 1.5 | 0.0 | — | — | — | — | — | — |
| `grenadierdip` | Grenadier (mercenary) | Grenadier | ausdip | common | 120 | 6.0 | 80 | 60 | 40 | 18 | 1.5 | 0.0 | — | — | — | — | — | — |
| `howitzer` | Howitzer | Mortar | ausart | common | 3000 | 94.0 | 0 | 350 | 300 | 4000 | 26.25 | 18.75 | — | — | — | — | — | — |
| `hussar` | Hussar | Light Cavalry | aussta | shared (14n) | 230 | 15.0 | 70 | 20 | 2 | 12 | 1.22 | 0.0 | — | — | — | — | — | — |
| `lightcavalrydip` | Light cavalry (mercenary) | Mounted Shooter | ausdip | common | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | — | — | — | — | — | — |
| `lightinfantrydip` | Light Infantryman (mercenary) | Light Infantry | ausdip | common | 55 | 1.0 | 25 | 0 | 1 | 5 | 0.94 | 0.0 | — | — | — | — | — | — |
| `mortar` | Bombard | Super Mortar | ausart | common | 400 | 25.0 | 0 | 75 | 200 | 200 | 48.75 | 7.81 | — | — | — | — | — | — |
| `multicannon` | Multi-barrelled Cannon | Multi-cannon | ausart | shared (17n) | 2000 | 50.0 | 0 | 400 | 250 | 500 | 13.13 | 1.88 | — | — | — | — | — | — |
| `musketeer18` | Musketeer, 18th century | Shooter | ausba2 | shared (13n) | 100 | 4.5 | 50 | 40 | 40 | 10 | 1.22 | 0.0 | — | — | — | — | — | — |
| `musketeeraus` | Musketeer, 17th century | Shooter | ausbar | unique | 55 | 6.5 | 35 | 9 | 15 | 12 | 15.0 | 5.0 | 2 | 2 | 5 | 165 | 5 | 35 |
| `officer` | Officer, 17th century | Light Infantry | ausbar | shared (16n) | 125 | 10.0 | 50 | 150 | 30 | 30 | 1.22 | 0.0 | 2 | 2 | 5 | 200 | 10 | 30 |
| `officer18` | Officer, 18th century | Light Infantry | ausba2 | shared (17n) | 125 | 6.0 | 50 | 200 | 10 | 50 | 1.22 | 0.0 | — | — | — | — | — | — |
| `pandur` | Pandur | Shooter | ausba2 | unique | 85 | 6.0 | 40 | 15 | 10 | 17 | 16.88 | 4.69 | — | — | — | — | — | — |
| `peaaus` | Peasant | Peasant | auscen | shared (5n) | 50 | 12.5 | 100 | 0 | 0 | 20 | 1.22 | 0.0 | — | — | — | — | — | — |
| `pikeman` | Pikeman, 17th century | Light Infantry | ausbar | shared (13n) | 90 | 4.5 | 25 | 3 | 20 | 8 | 1.88 | 0.0 | 3 | 2 | 4 | 210 | 6 | 40 |
| `pikeman18` | Pikeman, 18th century | Light Infantry | ausba2 | shared (16n) | 85 | 1.25 | 30 | 2 | 0 | 9 | 1.88 | 0.0 | — | — | — | — | — | — |
| `priest` | Priest | Light Infantry | austem | shared (16n) | 100 | 15.0 | 30 | 10 | 0 | 15 | 9.38 | 0.0 | — | — | — | — | — | — |
| `reiter` | Reiter | Heavy Cavalry | aussta | shared (14n) | 300 | 24.0 | 120 | 10 | 40 | 15 | 1.22 | 0.0 | 2 | 6 | 6 | 190 | 15 | 40 |
| `roundshier` | Roundshier | Light Infantry | ausbar | unique | 100 | 4.0 | 20 | 3 | 25 | 6 | 1.13 | 0.0 | 3 | 3 | 7 | 225 | 16 | 80 |
| `roundshierdip` | Roundshier (mercenary) | Light Infantry | ausdip | common | 100 | 4.0 | 20 | 3 | 25 | 6 | 1.13 | 0.0 | 3 | 3 | 7 | 225 | 16 | 80 |
| `unitbox` | — | — | — | common | 100 | 3.12 | 100 | 0 | 0 | — | — | — | — | — | — | — | — | — |
| `yacht` | Yacht | Yacht | eurpor | common | 31000 | 48.0 | 0 | 450 | 150 | 1000 | 20.63 | 10.94 | — | — | — | — | — | — |

### fra — France (37 юнитов)

| sid | name | usage | trained_in | uniqueness | HP | Time | F | G | I | dmg | rng (t) | reload | пика | меч | пуля | картечь | стрела | ядро |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `archerdip` | Archer (mercenary) | Archer | fradip | common | 40 | 1.5 | 20 | 1 | 0 | 15 | 15.0 | 2.34 | — | — | — | — | — | — |
| `archerturdip` | Turkish archer (mercenary) | Archer | fradip | common | 40 | 1.5 | 20 | 1 | 0 | 15 | 15.0 | 2.34 | — | — | — | — | — | — |
| `battleship` | Ship of the Line | Battleship | eurpor | common | 90000 | 390.0 | 0 | 3200 | 700 | 1800 | 36.56 | 0.62 | — | — | — | — | — | — |
| `cannon` | Cannon | Cannon | fraart | common | 9000 | 75.0 | 0 | 400 | 400 | 1800 | 40.5 | 10.94 | — | — | — | — | — | — |
| `chasseur` | Chasseur | Shooter | fraba2 | unique | 75 | 6.0 | 50 | 45 | 15 | 20 | 19.69 | 5.94 | — | — | — | — | — | — |
| `cossacksichdip` | Sich Cossack (mercenary) | Light Cavalry | fradip | common | 250 | 13.5 | 130 | 0 | 2 | 13 | 1.22 | 0.0 | — | — | — | — | — | — |
| `cuirassier` | Cuirassier | Heavy Cavalry | frasta | shared (17n) | 300 | 22.5 | 120 | 35 | 25 | 14 | 1.22 | 0.0 | 2 | 4 | 10 | 160 | 5 | 80 |
| `dragoon` | Dragoon, 17th century | Mounted Shooter | frasta | shared (16n) | 220 | 15.0 | 90 | 7 | 5 | 15 | 15.0 | 5.62 | — | — | — | — | — | — |
| `dragoon18dip` | Dragoon, 18th century (mercenary) | Mounted Shooter | fradip | common | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | — | — | — | — | — | — |
| `dragoon18fra` | Dragoon, 18th century | Mounted Shooter | frasta | unique | 140 | 15.0 | 50 | 30 | 6 | 10 | 15.0 | 4.69 | — | — | — | — | — | — |
| `drummer` | Drummer, 17th century | Light Infantry | frabar | shared (16n) | 75 | 6.0 | 50 | 30 | 0 | — | — | — | — | — | — | — | — | — |
| `drummer18` | Drummer, 18th century | Light Infantry | fraba2 | shared (16n) | 75 | 6.0 | 50 | 30 | 0 | — | — | — | — | — | — | — | — | — |
| `ferry` | Ferry | Transport | eurpor | common | 62000 | 56.0 | 0 | 50 | 100 | — | — | — | — | — | — | — | — | — |
| `fishboat` | Boat | Fishing Boat | eurpor | common | 300 | 40.0 | 0 | 0 | 0 | — | — | — | — | — | — | — | — | — |
| `frigate` | Frigate | Frigate | eurpor | common | 50000 | 230.0 | 0 | 1100 | 600 | 1800 | 30.94 | 2.34 | — | — | — | — | — | — |
| `galley` | Galley | Galley | eurpor | common | 35000 | 50.0 | 0 | 900 | 800 | 100 | 22.5 | 4.69 | — | — | — | — | — | — |
| `grenadier` | Grenadier | Grenadier | fraba2 | shared (13n) | 120 | 6.0 | 80 | 60 | 40 | 18 | 1.5 | 0.0 | — | — | — | — | — | — |
| `grenadierdip` | Grenadier (mercenary) | Grenadier | fradip | common | 120 | 6.0 | 80 | 60 | 40 | 18 | 1.5 | 0.0 | — | — | — | — | — | — |
| `howitzer` | Howitzer | Mortar | fraart | common | 3000 | 94.0 | 0 | 350 | 300 | 4000 | 26.25 | 18.75 | — | — | — | — | — | — |
| `hussar` | Hussar | Light Cavalry | frasta | shared (14n) | 230 | 15.0 | 70 | 20 | 2 | 12 | 1.22 | 0.0 | — | — | — | — | — | — |
| `kingmusketeer` | King's Musketeer | Mounted Shooter | frasta | unique | 280 | 27.0 | 100 | 100 | 8 | 43 | 13.13 | 6.88 | — | — | — | — | — | — |
| `lightcavalrydip` | Light cavalry (mercenary) | Mounted Shooter | fradip | common | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | — | — | — | — | — | — |
| `lightinfantrydip` | Light Infantryman (mercenary) | Light Infantry | fradip | common | 55 | 1.0 | 25 | 0 | 1 | 5 | 0.94 | 0.0 | — | — | — | — | — | — |
| `mortar` | Bombard | Super Mortar | fraart | common | 400 | 25.0 | 0 | 75 | 200 | 200 | 48.75 | 7.81 | — | — | — | — | — | — |
| `multicannon` | Multi-barrelled Cannon | Multi-cannon | fraart | shared (17n) | 2000 | 50.0 | 0 | 400 | 250 | 500 | 13.13 | 1.88 | — | — | — | — | — | — |
| `musketeer` | Musketeer, 17th century | Shooter | frabar | shared (11n) | 70 | 6.0 | 45 | 6 | 5 | 12 | 15.0 | 4.69 | — | — | — | — | — | — |
| `musketeer18` | Musketeer, 18th century | Shooter | fraba2 | shared (13n) | 100 | 4.5 | 50 | 40 | 40 | 10 | 1.22 | 0.0 | — | — | — | — | — | — |
| `officer` | Officer, 17th century | Light Infantry | frabar | shared (16n) | 125 | 10.0 | 50 | 150 | 30 | 30 | 1.22 | 0.0 | 2 | 2 | 5 | 200 | 10 | 30 |
| `officer18` | Officer, 18th century | Light Infantry | fraba2 | shared (17n) | 125 | 6.0 | 50 | 200 | 10 | 50 | 1.22 | 0.0 | — | — | — | — | — | — |
| `peaeng` | Peasant | Peasant | fracen | shared (5n) | 50 | 12.5 | 100 | 0 | 0 | 20 | 1.22 | 0.0 | — | — | — | — | — | — |
| `pikeman` | Pikeman, 17th century | Light Infantry | frabar | shared (13n) | 90 | 4.5 | 25 | 3 | 20 | 8 | 1.88 | 0.0 | 3 | 2 | 4 | 210 | 6 | 40 |
| `pikeman18` | Pikeman, 18th century | Light Infantry | fraba2 | shared (16n) | 85 | 1.25 | 30 | 2 | 0 | 9 | 1.88 | 0.0 | — | — | — | — | — | — |
| `priest` | Priest | Light Infantry | fratem | shared (16n) | 100 | 15.0 | 30 | 10 | 0 | 15 | 9.38 | 0.0 | — | — | — | — | — | — |
| `reiter` | Reiter | Heavy Cavalry | frasta | shared (14n) | 300 | 24.0 | 120 | 10 | 40 | 15 | 1.22 | 0.0 | 2 | 6 | 6 | 190 | 15 | 40 |
| `roundshierdip` | Roundshier (mercenary) | Light Infantry | fradip | common | 100 | 4.0 | 20 | 3 | 25 | 6 | 1.13 | 0.0 | 3 | 3 | 7 | 225 | 16 | 80 |
| `unitbox` | — | — | — | common | 100 | 3.12 | 100 | 0 | 0 | — | — | — | — | — | — | — | — | — |
| `yacht` | Yacht | Yacht | eurpor | common | 31000 | 48.0 | 0 | 450 | 150 | 1000 | 20.63 | 10.94 | — | — | — | — | — | — |

### eng — England (36 юнитов)

| sid | name | usage | trained_in | uniqueness | HP | Time | F | G | I | dmg | rng (t) | reload | пика | меч | пуля | картечь | стрела | ядро |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `archerdip` | Archer (mercenary) | Archer | engdip | common | 40 | 1.5 | 20 | 1 | 0 | 15 | 15.0 | 2.34 | — | — | — | — | — | — |
| `archerturdip` | Turkish archer (mercenary) | Archer | engdip | common | 40 | 1.5 | 20 | 1 | 0 | 15 | 15.0 | 2.34 | — | — | — | — | — | — |
| `bagpiper` | Bagpiper | Light Infantry | engba2 | semi-unique (2n) | 75 | 6.0 | 50 | 30 | 0 | — | — | — | — | — | — | — | — | — |
| `battleship` | Ship of the Line | Battleship | eurpor | common | 90000 | 390.0 | 0 | 3200 | 700 | 1800 | 36.56 | 0.62 | — | — | — | — | — | — |
| `cannon` | Cannon | Cannon | engart | common | 9000 | 75.0 | 0 | 400 | 400 | 1800 | 40.5 | 10.94 | — | — | — | — | — | — |
| `cossacksichdip` | Sich Cossack (mercenary) | Light Cavalry | engdip | common | 250 | 13.5 | 130 | 0 | 2 | 13 | 1.22 | 0.0 | — | — | — | — | — | — |
| `cuirassier` | Cuirassier | Heavy Cavalry | engsta | shared (17n) | 300 | 22.5 | 120 | 35 | 25 | 14 | 1.22 | 0.0 | 2 | 4 | 10 | 160 | 5 | 80 |
| `dragoon` | Dragoon, 17th century | Mounted Shooter | engsta | shared (16n) | 220 | 15.0 | 90 | 7 | 5 | 15 | 15.0 | 5.62 | — | — | — | — | — | — |
| `dragoon18` | Dragoon, 18th century | Mounted Shooter | engsta | shared (13n) | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | — | — | — | — | — | — |
| `dragoon18dip` | Dragoon, 18th century (mercenary) | Mounted Shooter | engdip | common | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | — | — | — | — | — | — |
| `drummer` | Drummer, 17th century | Light Infantry | engbar | shared (16n) | 75 | 6.0 | 50 | 30 | 0 | — | — | — | — | — | — | — | — | — |
| `ferry` | Ferry | Transport | eurpor | common | 62000 | 56.0 | 0 | 50 | 100 | — | — | — | — | — | — | — | — | — |
| `fishboat` | Boat | Fishing Boat | eurpor | common | 300 | 40.0 | 0 | 0 | 0 | — | — | — | — | — | — | — | — | — |
| `frigate` | Frigate | Frigate | eurpor | common | 50000 | 230.0 | 0 | 1100 | 600 | 1800 | 30.94 | 2.34 | — | — | — | — | — | — |
| `galley` | Galley | Galley | eurpor | common | 35000 | 50.0 | 0 | 900 | 800 | 100 | 22.5 | 4.69 | — | — | — | — | — | — |
| `grenadier` | Grenadier | Grenadier | engba2 | shared (13n) | 120 | 6.0 | 80 | 60 | 40 | 18 | 1.5 | 0.0 | — | — | — | — | — | — |
| `grenadierdip` | Grenadier (mercenary) | Grenadier | engdip | common | 120 | 6.0 | 80 | 60 | 40 | 18 | 1.5 | 0.0 | — | — | — | — | — | — |
| `highlander` | Highlander | Shooter | engba2 | unique | 130 | 6.0 | 90 | 25 | 10 | 16 | 15.94 | 5.0 | — | — | — | — | — | — |
| `howitzer` | Howitzer | Mortar | engart | common | 3000 | 94.0 | 0 | 350 | 300 | 4000 | 26.25 | 18.75 | — | — | — | — | — | — |
| `hussar` | Hussar | Light Cavalry | engsta | shared (14n) | 230 | 15.0 | 70 | 20 | 2 | 12 | 1.22 | 0.0 | — | — | — | — | — | — |
| `lightcavalrydip` | Light cavalry (mercenary) | Mounted Shooter | engdip | common | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | — | — | — | — | — | — |
| `lightinfantrydip` | Light Infantryman (mercenary) | Light Infantry | engdip | common | 55 | 1.0 | 25 | 0 | 1 | 5 | 0.94 | 0.0 | — | — | — | — | — | — |
| `mortar` | Bombard | Super Mortar | engart | common | 400 | 25.0 | 0 | 75 | 200 | 200 | 48.75 | 7.81 | — | — | — | — | — | — |
| `multicannon` | Multi-barrelled Cannon | Multi-cannon | engart | shared (17n) | 2000 | 50.0 | 0 | 400 | 250 | 500 | 13.13 | 1.88 | — | — | — | — | — | — |
| `musketeer` | Musketeer, 17th century | Shooter | engbar | shared (11n) | 70 | 6.0 | 45 | 6 | 5 | 12 | 15.0 | 4.69 | — | — | — | — | — | — |
| `musketeer18` | Musketeer, 18th century | Shooter | engba2 | shared (13n) | 100 | 4.5 | 50 | 40 | 40 | 10 | 1.22 | 0.0 | — | — | — | — | — | — |
| `officer` | Officer, 17th century | Light Infantry | engbar | shared (16n) | 125 | 10.0 | 50 | 150 | 30 | 30 | 1.22 | 0.0 | 2 | 2 | 5 | 200 | 10 | 30 |
| `officer18` | Officer, 18th century | Light Infantry | engba2 | shared (17n) | 125 | 6.0 | 50 | 200 | 10 | 50 | 1.22 | 0.0 | — | — | — | — | — | — |
| `peaeng` | Peasant | Peasant | engcen | shared (5n) | 50 | 12.5 | 100 | 0 | 0 | 20 | 1.22 | 0.0 | — | — | — | — | — | — |
| `pikeman` | Pikeman, 17th century | Light Infantry | engbar | shared (13n) | 90 | 4.5 | 25 | 3 | 20 | 8 | 1.88 | 0.0 | 3 | 2 | 4 | 210 | 6 | 40 |
| `pikeman18` | Pikeman, 18th century | Light Infantry | engba2 | shared (16n) | 85 | 1.25 | 30 | 2 | 0 | 9 | 1.88 | 0.0 | — | — | — | — | — | — |
| `priest` | Priest | Light Infantry | engtem | shared (16n) | 100 | 15.0 | 30 | 10 | 0 | 15 | 9.38 | 0.0 | — | — | — | — | — | — |
| `reiter` | Reiter | Heavy Cavalry | engsta | shared (14n) | 300 | 24.0 | 120 | 10 | 40 | 15 | 1.22 | 0.0 | 2 | 6 | 6 | 190 | 15 | 40 |
| `roundshierdip` | Roundshier (mercenary) | Light Infantry | engdip | common | 100 | 4.0 | 20 | 3 | 25 | 6 | 1.13 | 0.0 | 3 | 3 | 7 | 225 | 16 | 80 |
| `unitbox` | — | — | — | common | 100 | 3.12 | 100 | 0 | 0 | — | — | — | — | — | — | — | — | — |
| `yacht` | Yacht | Yacht | eurpor | common | 31000 | 48.0 | 0 | 450 | 150 | 1000 | 20.63 | 10.94 | — | — | — | — | — | — |

### spa — Spain (36 юнитов)

| sid | name | usage | trained_in | uniqueness | HP | Time | F | G | I | dmg | rng (t) | reload | пика | меч | пуля | картечь | стрела | ядро |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `archerdip` | Archer (mercenary) | Archer | spadip | common | 40 | 1.5 | 20 | 1 | 0 | 15 | 15.0 | 2.34 | — | — | — | — | — | — |
| `archerturdip` | Turkish archer (mercenary) | Archer | spadip | common | 40 | 1.5 | 20 | 1 | 0 | 15 | 15.0 | 2.34 | — | — | — | — | — | — |
| `battleship` | Ship of the Line | Battleship | eurpor | common | 90000 | 390.0 | 0 | 3200 | 700 | 1800 | 36.56 | 0.62 | — | — | — | — | — | — |
| `cannon` | Cannon | Cannon | spaart | common | 9000 | 75.0 | 0 | 400 | 400 | 1800 | 40.5 | 10.94 | — | — | — | — | — | — |
| `cossacksichdip` | Sich Cossack (mercenary) | Light Cavalry | spadip | common | 250 | 13.5 | 130 | 0 | 2 | 13 | 1.22 | 0.0 | — | — | — | — | — | — |
| `cuirassier` | Cuirassier | Heavy Cavalry | spasta | shared (17n) | 300 | 22.5 | 120 | 35 | 25 | 14 | 1.22 | 0.0 | 2 | 4 | 10 | 160 | 5 | 80 |
| `dragoon` | Dragoon, 17th century | Mounted Shooter | spasta | shared (16n) | 220 | 15.0 | 90 | 7 | 5 | 15 | 15.0 | 5.62 | — | — | — | — | — | — |
| `dragoon18` | Dragoon, 18th century | Mounted Shooter | spasta | shared (13n) | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | — | — | — | — | — | — |
| `dragoon18dip` | Dragoon, 18th century (mercenary) | Mounted Shooter | spadip | common | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | — | — | — | — | — | — |
| `drummer` | Drummer, 17th century | Light Infantry | spabar | shared (16n) | 75 | 6.0 | 50 | 30 | 0 | — | — | — | — | — | — | — | — | — |
| `drummer18` | Drummer, 18th century | Light Infantry | spaba2 | shared (16n) | 75 | 6.0 | 50 | 30 | 0 | — | — | — | — | — | — | — | — | — |
| `ferry` | Ferry | Transport | eurpor | common | 62000 | 56.0 | 0 | 50 | 100 | — | — | — | — | — | — | — | — | — |
| `fishboat` | Boat | Fishing Boat | eurpor | common | 300 | 40.0 | 0 | 0 | 0 | — | — | — | — | — | — | — | — | — |
| `frigate` | Frigate | Frigate | eurpor | common | 50000 | 230.0 | 0 | 1100 | 600 | 1800 | 30.94 | 2.34 | — | — | — | — | — | — |
| `galley` | Galley | Galley | eurpor | common | 35000 | 50.0 | 0 | 900 | 800 | 100 | 22.5 | 4.69 | — | — | — | — | — | — |
| `grenadier` | Grenadier | Grenadier | spaba2 | shared (13n) | 120 | 6.0 | 80 | 60 | 40 | 18 | 1.5 | 0.0 | — | — | — | — | — | — |
| `grenadierdip` | Grenadier (mercenary) | Grenadier | spadip | common | 120 | 6.0 | 80 | 60 | 40 | 18 | 1.5 | 0.0 | — | — | — | — | — | — |
| `howitzer` | Howitzer | Mortar | spaart | common | 3000 | 94.0 | 0 | 350 | 300 | 4000 | 26.25 | 18.75 | — | — | — | — | — | — |
| `hussar` | Hussar | Light Cavalry | spasta | shared (14n) | 230 | 15.0 | 70 | 20 | 2 | 12 | 1.22 | 0.0 | — | — | — | — | — | — |
| `lightcavalrydip` | Light cavalry (mercenary) | Mounted Shooter | spadip | common | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | — | — | — | — | — | — |
| `lightinfantrydip` | Light Infantryman (mercenary) | Light Infantry | spadip | common | 55 | 1.0 | 25 | 0 | 1 | 5 | 0.94 | 0.0 | — | — | — | — | — | — |
| `mortar` | Bombard | Super Mortar | spaart | common | 400 | 25.0 | 0 | 75 | 200 | 200 | 48.75 | 7.81 | — | — | — | — | — | — |
| `multicannon` | Multi-barrelled Cannon | Multi-cannon | spaart | shared (17n) | 2000 | 50.0 | 0 | 400 | 250 | 500 | 13.13 | 1.88 | — | — | — | — | — | — |
| `musketeer18` | Musketeer, 18th century | Shooter | spaba2 | shared (13n) | 100 | 4.5 | 50 | 40 | 40 | 10 | 1.22 | 0.0 | — | — | — | — | — | — |
| `musketeerspa` | Musketeer, 17th century | Shooter | spabar | unique | 85 | 7.5 | 40 | 12 | 20 | 15 | 15.94 | 5.94 | 3 | 2 | 5 | 210 | 7 | 40 |
| `officer` | Officer, 17th century | Light Infantry | spabar | shared (16n) | 125 | 10.0 | 50 | 150 | 30 | 30 | 1.22 | 0.0 | 2 | 2 | 5 | 200 | 10 | 30 |
| `officer18` | Officer, 18th century | Light Infantry | spaba2 | shared (17n) | 125 | 6.0 | 50 | 200 | 10 | 50 | 1.22 | 0.0 | — | — | — | — | — | — |
| `peaspa` | Peasant | Peasant | spacen | shared (4n) | 50 | 12.5 | 100 | 0 | 0 | 20 | 1.22 | 0.0 | — | — | — | — | — | — |
| `pikeman` | Pikeman, 17th century | Light Infantry | spabar | shared (13n) | 100 | 5.5 | 35 | 7 | 30 | 10 | 1.88 | 0.0 | 3 | 4 | 6 | 240 | 12 | 50 |
| `pikeman18` | Pikeman, 18th century | Light Infantry | spaba2 | shared (16n) | 85 | 1.25 | 30 | 2 | 0 | 9 | 1.88 | 0.0 | — | — | — | — | — | — |
| `pikemanspa` | Coselete | Light Infantry | spabar | unique | 100 | 5.5 | 35 | 7 | 30 | 10 | 1.88 | 0.0 | 3 | 4 | 6 | 240 | 12 | 50 |
| `priest` | Priest | Light Infantry | spatem | shared (16n) | 100 | 15.0 | 30 | 10 | 0 | 15 | 9.38 | 0.0 | — | — | — | — | — | — |
| `reiter` | Reiter | Heavy Cavalry | spasta | shared (14n) | 300 | 24.0 | 120 | 10 | 40 | 15 | 1.22 | 0.0 | 2 | 6 | 6 | 190 | 15 | 40 |
| `roundshierdip` | Roundshier (mercenary) | Light Infantry | spadip | common | 100 | 4.0 | 20 | 3 | 25 | 6 | 1.13 | 0.0 | 3 | 3 | 7 | 225 | 16 | 80 |
| `unitbox` | — | — | — | common | 100 | 3.12 | 100 | 0 | 0 | — | — | — | — | — | — | — | — | — |
| `yacht` | Yacht | Yacht | eurpor | common | 31000 | 48.0 | 0 | 450 | 150 | 1000 | 20.63 | 10.94 | — | — | — | — | — | — |

### rus — Russia (35 юнитов)

| sid | name | usage | trained_in | uniqueness | HP | Time | F | G | I | dmg | rng (t) | reload | пика | меч | пуля | картечь | стрела | ядро |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `archerdip` | Archer (mercenary) | Archer | rusdip | common | 40 | 1.5 | 20 | 1 | 0 | 15 | 15.0 | 2.34 | — | — | — | — | — | — |
| `archerturdip` | Turkish archer (mercenary) | Archer | rusdip | common | 40 | 1.5 | 20 | 1 | 0 | 15 | 15.0 | 2.34 | — | — | — | — | — | — |
| `battleship` | Ship of the Line | Battleship | ruspor | common | 90000 | 390.0 | 0 | 3200 | 700 | 1800 | 36.56 | 0.62 | — | — | — | — | — | — |
| `cannon` | Cannon | Cannon | rusart | common | 9000 | 75.0 | 0 | 400 | 400 | 1800 | 40.5 | 10.94 | — | — | — | — | — | — |
| `cossackdon` | Don Cossack | Heavy Cavalry | russta | unique | 220 | 13.5 | 100 | 0 | 0 | 13 | 1.88 | 0.0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `cossacksichdip` | Sich Cossack (mercenary) | Light Cavalry | rusdip | common | 250 | 13.5 | 130 | 0 | 2 | 13 | 1.22 | 0.0 | — | — | — | — | — | — |
| `cuirassier` | Cuirassier | Heavy Cavalry | russta | shared (17n) | 300 | 22.5 | 120 | 35 | 25 | 14 | 1.22 | 0.0 | 2 | 4 | 10 | 160 | 5 | 80 |
| `dragoon18` | Dragoon, 18th century | Mounted Shooter | russta | shared (13n) | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | — | — | — | — | — | — |
| `dragoon18dip` | Dragoon, 18th century (mercenary) | Mounted Shooter | rusdip | common | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | — | — | — | — | — | — |
| `drummer18` | Drummer, 18th century | Light Infantry | rusba2 | shared (16n) | 100 | 6.0 | 90 | 15 | 0 | — | — | — | — | — | — | — | — | — |
| `drummerrus` | Drummer, 17th century | Light Infantry | rusbar | unique | 100 | 6.0 | 90 | 15 | 0 | — | — | — | — | — | — | — | — | — |
| `ferry` | Ferry | Transport | ruspor | common | 62000 | 56.0 | 0 | 50 | 100 | — | — | — | — | — | — | — | — | — |
| `fishboat` | Boat | Fishing Boat | ruspor | common | 300 | 40.0 | 0 | 0 | 0 | — | — | — | — | — | — | — | — | — |
| `frigate` | Frigate | Frigate | ruspor | common | 50000 | 230.0 | 0 | 1100 | 600 | 1800 | 30.94 | 2.34 | — | — | — | — | — | — |
| `galley` | Galley | Galley | ruspor | common | 35000 | 50.0 | 0 | 900 | 800 | 100 | 22.5 | 4.69 | — | — | — | — | — | — |
| `grenadier` | Grenadier | Grenadier | rusba2 | shared (13n) | 120 | 6.0 | 80 | 60 | 40 | 18 | 1.5 | 0.0 | — | — | — | — | — | — |
| `grenadierdip` | Grenadier (mercenary) | Grenadier | rusdip | common | 120 | 6.0 | 80 | 60 | 40 | 18 | 1.5 | 0.0 | — | — | — | — | — | — |
| `howitzer` | Howitzer | Mortar | rusart | common | 3000 | 94.0 | 0 | 350 | 300 | 4000 | 26.25 | 18.75 | — | — | — | — | — | — |
| `hussar` | Hussar | Light Cavalry | russta | shared (14n) | 230 | 15.0 | 70 | 20 | 2 | 12 | 1.22 | 0.0 | — | — | — | — | — | — |
| `lightcavalrydip` | Light cavalry (mercenary) | Mounted Shooter | rusdip | common | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | — | — | — | — | — | — |
| `lightinfantrydip` | Light Infantryman (mercenary) | Light Infantry | rusdip | common | 55 | 1.0 | 25 | 0 | 1 | 5 | 0.94 | 0.0 | — | — | — | — | — | — |
| `mortar` | Bombard | Super Mortar | rusart | common | 400 | 25.0 | 0 | 75 | 200 | 200 | 48.75 | 7.81 | — | — | — | — | — | — |
| `multicannon` | Multi-barrelled Cannon | Multi-cannon | rusart | shared (17n) | 2000 | 50.0 | 0 | 400 | 250 | 500 | 13.13 | 1.88 | — | — | — | — | — | — |
| `musketeer18` | Musketeer, 18th century | Shooter | rusba2 | shared (13n) | 100 | 4.5 | 50 | 40 | 40 | 10 | 1.22 | 0.0 | — | — | — | — | — | — |
| `officer18` | Officer, 18th century | Light Infantry | rusba2 | shared (17n) | 125 | 6.0 | 50 | 200 | 10 | 50 | 1.22 | 0.0 | — | — | — | — | — | — |
| `officerrus` | Commander | Light Infantry | rusbar | unique | 125 | 12.5 | 100 | 125 | 5 | 40 | 1.22 | 0.0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `pearus` | Serf | Peasant | ruscen | unique | 50 | 12.5 | 100 | 0 | 0 | 20 | 1.22 | 0.0 | — | — | — | — | — | — |
| `pikeman18` | Pikeman, 18th century | Light Infantry | rusba2 | shared (16n) | 85 | 1.25 | 30 | 2 | 0 | 9 | 1.88 | 0.0 | — | — | — | — | — | — |
| `pikemanrus` | Spearman | Light Infantry | rusbar | unique | 85 | 5.5 | 45 | 4 | 15 | 8 | 1.69 | 0.0 | 2 | 1 | 4 | 140 | 4 | 25 |
| `pope` | Pope | Light Infantry | rustem | semi-unique (2n) | 100 | 15.0 | 30 | 10 | 0 | 15 | 9.38 | 0.0 | — | — | — | — | — | — |
| `roundshierdip` | Roundshier (mercenary) | Light Infantry | rusdip | common | 100 | 4.0 | 20 | 3 | 25 | 6 | 1.13 | 0.0 | 3 | 3 | 7 | 225 | 16 | 80 |
| `strelet` | Strelets | Shooter | rusbar | unique | 85 | 8.5 | 70 | 7 | 9 | 12 | 13.13 | 4.69 | — | — | — | — | — | — |
| `unitbox` | — | — | — | common | 100 | 3.12 | 100 | 0 | 0 | — | — | — | — | — | — | — | — | — |
| `vityaz` | Vityaz | Heavy Cavalry | russta | unique | 380 | 25.5 | 160 | 13 | 25 | 14 | 1.22 | 0.0 | 2 | 4 | 3 | 160 | 17 | 40 |
| `yacht` | Yacht | Yacht | ruspor | common | 31000 | 48.0 | 0 | 450 | 150 | 1000 | 20.63 | 10.94 | — | — | — | — | — | — |

### ukr — Ukraine (22 юнитов)

| sid | name | usage | trained_in | uniqueness | HP | Time | F | G | I | dmg | rng (t) | reload | пика | меч | пуля | картечь | стрела | ядро |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `archerdip` | Archer (mercenary) | Archer | ukrdip | common | 40 | 1.5 | 20 | 1 | 0 | 15 | 15.0 | 2.34 | — | — | — | — | — | — |
| `archerturdip` | Turkish archer (mercenary) | Archer | ukrdip | common | 40 | 1.5 | 20 | 1 | 0 | 15 | 15.0 | 2.34 | — | — | — | — | — | — |
| `cannon` | Cannon | Cannon | ukrart | common | 9000 | 75.0 | 0 | 400 | 400 | 1800 | 40.5 | 10.94 | — | — | — | — | — | — |
| `chaika` | — | Yacht | ukrpor | unique | 25000 | 40.0 | 0 | 600 | 200 | 1000 | 20.63 | 2.34 | — | — | — | — | — | — |
| `cossackregister` | Register Cossack | Heavy Cavalry | ukrsta | unique | 250 | 10.5 | 70 | 15 | 0 | 12 | 1.88 | 0.0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `cossacksich` | Sich Cossack | Light Cavalry | ukrsta | unique | 250 | 13.5 | 130 | 0 | 2 | 13 | 1.22 | 0.0 | — | — | — | — | — | — |
| `cossacksichdip` | Sich Cossack (mercenary) | Light Cavalry | ukrdip | common | 250 | 13.5 | 130 | 0 | 2 | 13 | 1.22 | 0.0 | — | — | — | — | — | — |
| `dragoon18dip` | Dragoon, 18th century (mercenary) | Mounted Shooter | ukrdip | common | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | — | — | — | — | — | — |
| `ferry` | Ferry | Transport | ukrpor | common | 62000 | 56.0 | 0 | 50 | 100 | — | — | — | — | — | — | — | — | — |
| `fishboat` | Boat | Fishing Boat | ukrpor | common | 300 | 40.0 | 0 | 0 | 0 | — | — | — | — | — | — | — | — | — |
| `galley` | Galley | Galley | ukrpor | common | 35000 | 50.0 | 0 | 900 | 800 | 100 | 22.5 | 4.69 | — | — | — | — | — | — |
| `grenadierdip` | Grenadier (mercenary) | Grenadier | ukrdip | common | 120 | 6.0 | 80 | 60 | 40 | 18 | 1.5 | 0.0 | — | — | — | — | — | — |
| `hetman` | Hetman | Heavy Cavalry | ukrsta | unique | 320 | 16.5 | 150 | 150 | 10 | 70 | 1.22 | 0.0 | 0 | 1 | 3 | 75 | 3 | 15 |
| `howitzer` | Howitzer | Mortar | ukrart | common | 3000 | 94.0 | 0 | 350 | 300 | 4000 | 26.25 | 18.75 | — | — | — | — | — | — |
| `lightcavalrydip` | Light cavalry (mercenary) | Mounted Shooter | ukrdip | common | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | — | — | — | — | — | — |
| `lightinfantrydip` | Light Infantryman (mercenary) | Light Infantry | ukrdip | common | 55 | 1.0 | 25 | 0 | 1 | 5 | 0.94 | 0.0 | — | — | — | — | — | — |
| `mortar` | Bombard | Super Mortar | ukrart | common | 400 | 25.0 | 0 | 75 | 200 | 200 | 48.75 | 7.81 | — | — | — | — | — | — |
| `peaukr` | Peasant | Peasant | ukrcen | unique | 75 | 11.25 | 100 | 0 | 0 | 20 | 1.22 | 0.0 | — | — | — | — | — | — |
| `pope` | Pope | Light Infantry | ukrtem | semi-unique (2n) | 100 | 15.0 | 30 | 10 | 0 | 15 | 9.38 | 0.0 | — | — | — | — | — | — |
| `roundshierdip` | Roundshier (mercenary) | Light Infantry | ukrdip | common | 100 | 4.0 | 20 | 3 | 25 | 6 | 1.13 | 0.0 | 3 | 3 | 7 | 225 | 16 | 80 |
| `serdiuk` | Serdiuk | Shooter | ukrbar | unique | 85 | 11.0 | 60 | 11 | 5 | 12 | 16.88 | 4.06 | — | — | — | — | — | — |
| `unitbox` | — | — | — | common | 100 | 3.12 | 100 | 0 | 0 | — | — | — | — | — | — | — | — | — |

### pol — Poland (37 юнитов)

| sid | name | usage | trained_in | uniqueness | HP | Time | F | G | I | dmg | rng (t) | reload | пика | меч | пуля | картечь | стрела | ядро |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `archerdip` | Archer (mercenary) | Archer | poldip | common | 40 | 1.5 | 20 | 1 | 0 | 15 | 15.0 | 2.34 | — | — | — | — | — | — |
| `archerturdip` | Turkish archer (mercenary) | Archer | poldip | common | 40 | 1.5 | 20 | 1 | 0 | 15 | 15.0 | 2.34 | — | — | — | — | — | — |
| `battleship` | Ship of the Line | Battleship | eurpor | common | 90000 | 390.0 | 0 | 3200 | 700 | 1800 | 36.56 | 0.62 | — | — | — | — | — | — |
| `cannon` | Cannon | Cannon | polart | common | 9000 | 75.0 | 0 | 400 | 400 | 1800 | 40.5 | 10.94 | — | — | — | — | — | — |
| `cossacksichdip` | Sich Cossack (mercenary) | Light Cavalry | poldip | common | 250 | 13.5 | 130 | 0 | 2 | 13 | 1.22 | 0.0 | — | — | — | — | — | — |
| `cuirassier` | Cuirassier | Heavy Cavalry | polsta | shared (17n) | 300 | 22.5 | 120 | 35 | 25 | 14 | 1.22 | 0.0 | 2 | 4 | 10 | 160 | 5 | 80 |
| `dragoon` | Dragoon, 17th century | Mounted Shooter | polsta | shared (16n) | 220 | 15.0 | 90 | 7 | 5 | 15 | 15.0 | 5.62 | — | — | — | — | — | — |
| `dragoon18` | Dragoon, 18th century | Mounted Shooter | polsta | shared (13n) | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | — | — | — | — | — | — |
| `dragoon18dip` | Dragoon, 18th century (mercenary) | Mounted Shooter | poldip | common | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | — | — | — | — | — | — |
| `dragoonpol` | Pospolite ruszenie | Mounted Shooter | polsta | unique | 185 | 13.5 | 70 | 5 | 4 | 13 | 15.94 | 5.0 | — | — | — | — | — | — |
| `drummer` | Drummer, 17th century | Light Infantry | polbar | shared (16n) | 75 | 6.0 | 50 | 30 | 0 | — | — | — | — | — | — | — | — | — |
| `drummer18` | Drummer, 18th century | Light Infantry | polba2 | shared (16n) | 75 | 6.0 | 50 | 30 | 0 | — | — | — | — | — | — | — | — | — |
| `ferry` | Ferry | Transport | eurpor | common | 62000 | 56.0 | 0 | 50 | 100 | — | — | — | — | — | — | — | — | — |
| `fishboat` | Boat | Fishing Boat | eurpor | common | 300 | 40.0 | 0 | 0 | 0 | — | — | — | — | — | — | — | — | — |
| `frigate` | Frigate | Frigate | eurpor | common | 50000 | 230.0 | 0 | 1100 | 600 | 1800 | 30.94 | 2.34 | — | — | — | — | — | — |
| `galley` | Galley | Galley | eurpor | common | 35000 | 50.0 | 0 | 900 | 800 | 100 | 22.5 | 4.69 | — | — | — | — | — | — |
| `grenadier` | Grenadier | Grenadier | polba2 | shared (13n) | 120 | 6.0 | 80 | 60 | 40 | 18 | 1.5 | 0.0 | — | — | — | — | — | — |
| `grenadierdip` | Grenadier (mercenary) | Grenadier | poldip | common | 120 | 6.0 | 80 | 60 | 40 | 18 | 1.5 | 0.0 | — | — | — | — | — | — |
| `howitzer` | Howitzer | Mortar | polart | common | 3000 | 94.0 | 0 | 350 | 300 | 4000 | 26.25 | 18.75 | — | — | — | — | — | — |
| `hussar` | Hussar | Light Cavalry | polsta | shared (14n) | 230 | 15.0 | 70 | 20 | 2 | 12 | 1.22 | 0.0 | — | — | — | — | — | — |
| `lightcavalrydip` | Light cavalry (mercenary) | Mounted Shooter | poldip | common | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | — | — | — | — | — | — |
| `lightinfantrydip` | Light Infantryman (mercenary) | Light Infantry | poldip | common | 55 | 1.0 | 25 | 0 | 1 | 5 | 0.94 | 0.0 | — | — | — | — | — | — |
| `mortar` | Bombard | Super Mortar | polart | common | 400 | 25.0 | 0 | 75 | 200 | 200 | 48.75 | 7.81 | — | — | — | — | — | — |
| `multicannon` | Multi-barrelled Cannon | Multi-cannon | polart | shared (17n) | 2000 | 50.0 | 0 | 400 | 250 | 500 | 13.13 | 1.88 | — | — | — | — | — | — |
| `musketeer18` | Musketeer, 18th century | Shooter | polba2 | shared (13n) | 100 | 4.5 | 50 | 40 | 40 | 10 | 1.22 | 0.0 | — | — | — | — | — | — |
| `musketeerpol` | Musketeer, 17th century | Shooter | polbar | unique | 70 | 4.5 | 40 | 3 | 3 | 9 | 13.13 | 3.12 | — | — | — | — | — | — |
| `officer` | Officer, 17th century | Light Infantry | polbar | shared (16n) | 125 | 10.0 | 50 | 150 | 30 | 30 | 1.22 | 0.0 | 2 | 2 | 5 | 200 | 10 | 30 |
| `officer18` | Officer, 18th century | Light Infantry | polba2 | shared (17n) | 125 | 6.0 | 50 | 200 | 10 | 50 | 1.22 | 0.0 | — | — | — | — | — | — |
| `peapol` | Peasant | Peasant | polcen | semi-unique (2n) | 50 | 12.5 | 100 | 0 | 0 | 20 | 1.22 | 0.0 | — | — | — | — | — | — |
| `pikeman18` | Pikeman, 18th century | Light Infantry | polba2 | shared (16n) | 85 | 1.25 | 30 | 2 | 0 | 9 | 1.88 | 0.0 | — | — | — | — | — | — |
| `pikemanpol` | Pikeman, 17th century | Light Infantry | polbar | unique | 90 | 3.0 | 25 | 1 | 0 | 8 | 2.06 | 0.0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `priest` | Priest | Light Infantry | poltem | shared (16n) | 100 | 15.0 | 30 | 10 | 0 | 15 | 9.38 | 0.0 | — | — | — | — | — | — |
| `reiterpol` | Light Reiter | Heavy Cavalry | polsta | unique | 190 | 8.25 | 60 | 5 | 2 | 9 | 1.22 | 0.0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `roundshierdip` | Roundshier (mercenary) | Light Infantry | poldip | common | 100 | 4.0 | 20 | 3 | 25 | 6 | 1.13 | 0.0 | 3 | 3 | 7 | 225 | 16 | 80 |
| `unitbox` | — | — | — | common | 100 | 3.12 | 100 | 0 | 0 | — | — | — | — | — | — | — | — | — |
| `wingedhussar` | Winged Hussar | Light Cavalry | polsta | unique | 225 | 26.0 | 130 | 30 | 25 | 14 | 1.88 | 0.0 | 1 | 2 | 5 | 160 | 10 | 30 |
| `yacht` | Yacht | Yacht | eurpor | common | 31000 | 48.0 | 0 | 450 | 150 | 1000 | 20.63 | 10.94 | — | — | — | — | — | — |

### swe — Sweden (36 юнитов)

| sid | name | usage | trained_in | uniqueness | HP | Time | F | G | I | dmg | rng (t) | reload | пика | меч | пуля | картечь | стрела | ядро |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `archerdip` | Archer (mercenary) | Archer | swedip | common | 40 | 1.5 | 20 | 1 | 0 | 15 | 15.0 | 2.34 | — | — | — | — | — | — |
| `archerturdip` | Turkish archer (mercenary) | Archer | swedip | common | 40 | 1.5 | 20 | 1 | 0 | 15 | 15.0 | 2.34 | — | — | — | — | — | — |
| `battleship` | Ship of the Line | Battleship | eurpor | common | 90000 | 390.0 | 0 | 3200 | 700 | 1800 | 36.56 | 0.62 | — | — | — | — | — | — |
| `cannon` | Cannon | Cannon | sweart | common | 9000 | 75.0 | 0 | 400 | 400 | 1800 | 40.5 | 10.94 | — | — | — | — | — | — |
| `cossacksichdip` | Sich Cossack (mercenary) | Light Cavalry | swedip | common | 250 | 13.5 | 130 | 0 | 2 | 13 | 1.22 | 0.0 | — | — | — | — | — | — |
| `cuirassier` | Cuirassier | Heavy Cavalry | swesta | shared (17n) | 300 | 22.5 | 120 | 35 | 25 | 14 | 1.22 | 0.0 | 2 | 4 | 10 | 160 | 5 | 80 |
| `dragoon` | Dragoon, 17th century | Mounted Shooter | swesta | shared (16n) | 220 | 15.0 | 90 | 7 | 5 | 15 | 15.0 | 5.62 | — | — | — | — | — | — |
| `dragoon18` | Dragoon, 18th century | Mounted Shooter | swesta | shared (13n) | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | — | — | — | — | — | — |
| `dragoon18dip` | Dragoon, 18th century (mercenary) | Mounted Shooter | swedip | common | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | — | — | — | — | — | — |
| `drummer` | Drummer, 17th century | Light Infantry | swebar | shared (16n) | 75 | 6.0 | 50 | 30 | 0 | — | — | — | — | — | — | — | — | — |
| `drummer18` | Drummer, 18th century | Light Infantry | sweba2 | shared (16n) | 75 | 6.0 | 50 | 30 | 0 | — | — | — | — | — | — | — | — | — |
| `ferry` | Ferry | Transport | eurpor | common | 62000 | 56.0 | 0 | 50 | 100 | — | — | — | — | — | — | — | — | — |
| `fishboat` | Boat | Fishing Boat | eurpor | common | 300 | 40.0 | 0 | 0 | 0 | — | — | — | — | — | — | — | — | — |
| `frigate` | Frigate | Frigate | eurpor | common | 50000 | 230.0 | 0 | 1100 | 600 | 1800 | 30.94 | 2.34 | — | — | — | — | — | — |
| `galley` | Galley | Galley | eurpor | common | 35000 | 50.0 | 0 | 900 | 800 | 100 | 22.5 | 4.69 | — | — | — | — | — | — |
| `grenadier` | Grenadier | Grenadier | sweba2 | shared (13n) | 120 | 6.0 | 80 | 60 | 40 | 18 | 1.5 | 0.0 | — | — | — | — | — | — |
| `grenadierdip` | Grenadier (mercenary) | Grenadier | swedip | common | 120 | 6.0 | 80 | 60 | 40 | 18 | 1.5 | 0.0 | — | — | — | — | — | — |
| `hackapell` | Hakkapeliitta | Light Cavalry | swesta | unique | 245 | 18.0 | 80 | 7 | 2 | 12 | 1.22 | 0.0 | — | — | — | — | — | — |
| `howitzer` | Howitzer | Mortar | sweart | common | 3000 | 94.0 | 0 | 350 | 300 | 4000 | 26.25 | 18.75 | — | — | — | — | — | — |
| `hussar` | Hussar | Light Cavalry | swesta | shared (14n) | 230 | 15.0 | 70 | 20 | 2 | 12 | 1.22 | 0.0 | — | — | — | — | — | — |
| `lightcavalrydip` | Light cavalry (mercenary) | Mounted Shooter | swedip | common | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | — | — | — | — | — | — |
| `lightinfantrydip` | Light Infantryman (mercenary) | Light Infantry | swedip | common | 55 | 1.0 | 25 | 0 | 1 | 5 | 0.94 | 0.0 | — | — | — | — | — | — |
| `mortar` | Bombard | Super Mortar | sweart | common | 400 | 25.0 | 0 | 75 | 200 | 200 | 48.75 | 7.81 | — | — | — | — | — | — |
| `multicannon` | Multi-barrelled Cannon | Multi-cannon | sweart | shared (17n) | 2000 | 50.0 | 0 | 400 | 250 | 500 | 13.13 | 1.88 | — | — | — | — | — | — |
| `musketeer` | Musketeer, 17th century | Shooter | swebar | shared (11n) | 70 | 6.0 | 45 | 6 | 5 | 12 | 15.0 | 4.69 | — | — | — | — | — | — |
| `musketeer18` | Musketeer, 18th century | Shooter | sweba2 | shared (13n) | 100 | 4.5 | 50 | 40 | 40 | 10 | 1.22 | 0.0 | — | — | — | — | — | — |
| `officer` | Officer, 17th century | Light Infantry | swebar | shared (16n) | 125 | 10.0 | 50 | 150 | 30 | 30 | 1.22 | 0.0 | 2 | 2 | 5 | 200 | 10 | 30 |
| `officer18` | Officer, 18th century | Light Infantry | sweba2 | shared (17n) | 125 | 6.0 | 50 | 200 | 10 | 50 | 1.22 | 0.0 | — | — | — | — | — | — |
| `peaeng` | Peasant | Peasant | swecen | shared (5n) | 50 | 12.5 | 100 | 0 | 0 | 20 | 1.22 | 0.0 | — | — | — | — | — | — |
| `pikeman` | Pikeman, 17th century | Light Infantry | swebar | shared (13n) | 90 | 4.5 | 25 | 3 | 20 | 8 | 1.88 | 0.0 | 3 | 2 | 4 | 210 | 6 | 40 |
| `pikeman18swe` | Pikeman, 18th century | Light Infantry | sweba2 | unique | 110 | 1.5 | 40 | 3 | 0 | 11 | 1.88 | 0.0 | — | — | — | — | — | — |
| `priest` | Priest | Light Infantry | swetem | shared (16n) | 100 | 15.0 | 30 | 10 | 0 | 15 | 9.38 | 0.0 | — | — | — | — | — | — |
| `reiterswe` | Swedish Reiter | Heavy Cavalry | swesta | unique | 300 | 22.5 | 130 | 7 | 20 | 14 | 1.22 | 0.0 | 2 | 3 | 7 | 140 | 7 | 35 |
| `roundshierdip` | Roundshier (mercenary) | Light Infantry | swedip | common | 100 | 4.0 | 20 | 3 | 25 | 6 | 1.13 | 0.0 | 3 | 3 | 7 | 225 | 16 | 80 |
| `unitbox` | — | — | — | common | 100 | 3.12 | 100 | 0 | 0 | — | — | — | — | — | — | — | — | — |
| `yacht` | Yacht | Yacht | eurpor | common | 31000 | 48.0 | 0 | 450 | 150 | 1000 | 20.63 | 10.94 | — | — | — | — | — | — |

### pru — Prussia (36 юнитов)

| sid | name | usage | trained_in | uniqueness | HP | Time | F | G | I | dmg | rng (t) | reload | пика | меч | пуля | картечь | стрела | ядро |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `archerdip` | Archer (mercenary) | Archer | prudip | common | 40 | 1.5 | 20 | 1 | 0 | 15 | 15.0 | 2.34 | — | — | — | — | — | — |
| `archerturdip` | Turkish archer (mercenary) | Archer | prudip | common | 40 | 1.5 | 20 | 1 | 0 | 15 | 15.0 | 2.34 | — | — | — | — | — | — |
| `battleship` | Ship of the Line | Battleship | eurpor | common | 90000 | 390.0 | 0 | 3200 | 700 | 1800 | 36.56 | 0.62 | — | — | — | — | — | — |
| `cannon` | Cannon | Cannon | pruart | common | 9000 | 75.0 | 0 | 400 | 400 | 1800 | 40.5 | 10.94 | — | — | — | — | — | — |
| `cossacksichdip` | Sich Cossack (mercenary) | Light Cavalry | prudip | common | 250 | 13.5 | 130 | 0 | 2 | 13 | 1.22 | 0.0 | — | — | — | — | — | — |
| `cuirassier` | Cuirassier | Heavy Cavalry | prusta | shared (17n) | 300 | 22.5 | 120 | 35 | 25 | 14 | 1.22 | 0.0 | 2 | 4 | 10 | 160 | 5 | 80 |
| `dragoon` | Dragoon, 17th century | Mounted Shooter | prusta | shared (16n) | 220 | 15.0 | 90 | 7 | 5 | 15 | 15.0 | 5.62 | — | — | — | — | — | — |
| `dragoon18` | Dragoon, 18th century | Mounted Shooter | prusta | shared (13n) | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | — | — | — | — | — | — |
| `dragoon18dip` | Dragoon, 18th century (mercenary) | Mounted Shooter | prudip | common | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | — | — | — | — | — | — |
| `drummer` | Drummer, 17th century | Light Infantry | prubar | shared (16n) | 75 | 6.0 | 50 | 30 | 0 | — | — | — | — | — | — | — | — | — |
| `drummer18` | Drummer, 18th century | Light Infantry | pruba2 | shared (16n) | 75 | 6.0 | 50 | 30 | 0 | — | — | — | — | — | — | — | — | — |
| `ferry` | Ferry | Transport | eurpor | common | 62000 | 56.0 | 0 | 50 | 100 | — | — | — | — | — | — | — | — | — |
| `fishboat` | Boat | Fishing Boat | eurpor | common | 300 | 40.0 | 0 | 0 | 0 | — | — | — | — | — | — | — | — | — |
| `frigate` | Frigate | Frigate | eurpor | common | 50000 | 230.0 | 0 | 1100 | 600 | 1800 | 30.94 | 2.34 | — | — | — | — | — | — |
| `galley` | Galley | Galley | eurpor | common | 35000 | 50.0 | 0 | 900 | 800 | 100 | 22.5 | 4.69 | — | — | — | — | — | — |
| `grenadier` | Grenadier | Grenadier | pruba2 | shared (13n) | 120 | 6.0 | 80 | 60 | 40 | 18 | 1.5 | 0.0 | — | — | — | — | — | — |
| `grenadierdip` | Grenadier (mercenary) | Grenadier | prudip | common | 120 | 6.0 | 80 | 60 | 40 | 18 | 1.5 | 0.0 | — | — | — | — | — | — |
| `grenadierpru` | Grenadier | Grenadier | pruba2 | unique | 125 | 7.0 | 90 | 100 | 45 | 18 | 1.5 | 0.0 | — | — | — | — | — | — |
| `howitzer` | Howitzer | Mortar | pruart | common | 3000 | 94.0 | 0 | 350 | 300 | 4000 | 26.25 | 18.75 | — | — | — | — | — | — |
| `hussarpru` | Hussar | Light Cavalry | prusta | unique | 240 | 11.25 | 80 | 15 | 2 | 9 | 1.22 | 0.0 | — | — | — | — | — | — |
| `lightcavalrydip` | Light cavalry (mercenary) | Mounted Shooter | prudip | common | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | — | — | — | — | — | — |
| `lightinfantrydip` | Light Infantryman (mercenary) | Light Infantry | prudip | common | 55 | 1.0 | 25 | 0 | 1 | 5 | 0.94 | 0.0 | — | — | — | — | — | — |
| `mortar` | Bombard | Super Mortar | pruart | common | 400 | 25.0 | 0 | 75 | 200 | 200 | 48.75 | 7.81 | — | — | — | — | — | — |
| `multicannon` | Multi-barrelled Cannon | Multi-cannon | pruart | shared (17n) | 2000 | 50.0 | 0 | 400 | 250 | 500 | 13.13 | 1.88 | — | — | — | — | — | — |
| `musketeer` | Musketeer, 17th century | Shooter | prubar | shared (11n) | 70 | 6.0 | 45 | 6 | 5 | 12 | 15.0 | 4.69 | — | — | — | — | — | — |
| `musketeer18pru` | Musketeer, 18th century | Shooter | pruba2 | unique | 100 | 6.0 | 70 | 80 | 40 | 10 | 1.59 | 0.0 | — | — | — | — | — | — |
| `officer` | Officer, 17th century | Light Infantry | prubar | shared (16n) | 125 | 10.0 | 50 | 150 | 30 | 30 | 1.22 | 0.0 | 2 | 2 | 5 | 200 | 10 | 30 |
| `officer18` | Officer, 18th century | Light Infantry | pruba2 | shared (17n) | 125 | 6.0 | 50 | 200 | 10 | 50 | 1.22 | 0.0 | — | — | — | — | — | — |
| `peaaus` | Peasant | Peasant | prucen | shared (5n) | 50 | 12.5 | 100 | 0 | 0 | 20 | 1.22 | 0.0 | — | — | — | — | — | — |
| `pikeman` | Pikeman, 17th century | Light Infantry | prubar | shared (13n) | 90 | 4.5 | 25 | 3 | 20 | 8 | 1.88 | 0.0 | 3 | 2 | 4 | 210 | 6 | 40 |
| `pikeman18` | Pikeman, 18th century | Light Infantry | pruba2 | shared (16n) | 85 | 1.25 | 30 | 2 | 0 | 9 | 1.88 | 0.0 | — | — | — | — | — | — |
| `priest` | Priest | Light Infantry | prutem | shared (16n) | 100 | 15.0 | 30 | 10 | 0 | 15 | 9.38 | 0.0 | — | — | — | — | — | — |
| `reiter` | Reiter | Heavy Cavalry | prusta | shared (14n) | 300 | 24.0 | 120 | 10 | 40 | 15 | 1.22 | 0.0 | 2 | 6 | 6 | 190 | 15 | 40 |
| `roundshierdip` | Roundshier (mercenary) | Light Infantry | prudip | common | 100 | 4.0 | 20 | 3 | 25 | 6 | 1.13 | 0.0 | 3 | 3 | 7 | 225 | 16 | 80 |
| `unitbox` | — | — | — | common | 100 | 3.12 | 100 | 0 | 0 | — | — | — | — | — | — | — | — | — |
| `yacht` | Yacht | Yacht | eurpor | common | 31000 | 48.0 | 0 | 450 | 150 | 1000 | 20.63 | 10.94 | — | — | — | — | — | — |

### ven — Venice (35 юнитов)

| sid | name | usage | trained_in | uniqueness | HP | Time | F | G | I | dmg | rng (t) | reload | пика | меч | пуля | картечь | стрела | ядро |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `archerdip` | Archer (mercenary) | Archer | vendip | common | 40 | 1.5 | 20 | 1 | 0 | 15 | 15.0 | 2.34 | — | — | — | — | — | — |
| `archerturdip` | Turkish archer (mercenary) | Archer | vendip | common | 40 | 1.5 | 20 | 1 | 0 | 15 | 15.0 | 2.34 | — | — | — | — | — | — |
| `battleship` | Ship of the Line | Battleship | eurpor | common | 90000 | 390.0 | 0 | 3200 | 700 | 1800 | 36.56 | 0.62 | — | — | — | — | — | — |
| `cannon` | Cannon | Cannon | venart | common | 9000 | 75.0 | 0 | 400 | 400 | 1800 | 40.5 | 10.94 | — | — | — | — | — | — |
| `cossacksichdip` | Sich Cossack (mercenary) | Light Cavalry | vendip | common | 250 | 13.5 | 130 | 0 | 2 | 13 | 1.22 | 0.0 | — | — | — | — | — | — |
| `cuirassier` | Cuirassier | Heavy Cavalry | vensta | shared (17n) | 300 | 22.5 | 120 | 35 | 25 | 14 | 1.22 | 0.0 | 2 | 4 | 10 | 160 | 5 | 80 |
| `dragoon` | Dragoon, 17th century | Mounted Shooter | vensta | shared (16n) | 220 | 15.0 | 90 | 7 | 5 | 15 | 15.0 | 5.62 | — | — | — | — | — | — |
| `dragoon18` | Dragoon, 18th century | Mounted Shooter | vensta | shared (13n) | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | — | — | — | — | — | — |
| `dragoon18dip` | Dragoon, 18th century (mercenary) | Mounted Shooter | vendip | common | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | — | — | — | — | — | — |
| `drummer` | Drummer, 17th century | Light Infantry | venbar | shared (16n) | 75 | 6.0 | 50 | 30 | 0 | — | — | — | — | — | — | — | — | — |
| `drummer18` | Drummer, 18th century | Light Infantry | venba2 | shared (16n) | 75 | 6.0 | 50 | 30 | 0 | — | — | — | — | — | — | — | — | — |
| `ferry` | Ferry | Transport | eurpor | common | 62000 | 56.0 | 0 | 50 | 100 | — | — | — | — | — | — | — | — | — |
| `fishboat` | Boat | Fishing Boat | eurpor | common | 300 | 40.0 | 0 | 0 | 0 | — | — | — | — | — | — | — | — | — |
| `frigate` | Frigate | Frigate | eurpor | common | 50000 | 230.0 | 0 | 1100 | 600 | 1800 | 30.94 | 2.34 | — | — | — | — | — | — |
| `galley` | Galley | Galley | eurpor | common | 35000 | 50.0 | 0 | 900 | 800 | 100 | 22.5 | 4.69 | — | — | — | — | — | — |
| `grenadier` | Grenadier | Grenadier | venba2 | shared (13n) | 120 | 6.0 | 80 | 60 | 40 | 18 | 1.5 | 0.0 | — | — | — | — | — | — |
| `grenadierdip` | Grenadier (mercenary) | Grenadier | vendip | common | 120 | 6.0 | 80 | 60 | 40 | 18 | 1.5 | 0.0 | — | — | — | — | — | — |
| `howitzer` | Howitzer | Mortar | venart | common | 3000 | 94.0 | 0 | 350 | 300 | 4000 | 26.25 | 18.75 | — | — | — | — | — | — |
| `hussar` | Hussar | Light Cavalry | vensta | shared (14n) | 230 | 15.0 | 70 | 20 | 2 | 12 | 1.22 | 0.0 | — | — | — | — | — | — |
| `lightcavalrydip` | Light cavalry (mercenary) | Mounted Shooter | vendip | common | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | — | — | — | — | — | — |
| `lightinfantrydip` | Light Infantryman (mercenary) | Light Infantry | vendip | common | 55 | 1.0 | 25 | 0 | 1 | 5 | 0.94 | 0.0 | — | — | — | — | — | — |
| `mortar` | Bombard | Super Mortar | venart | common | 400 | 25.0 | 0 | 75 | 200 | 200 | 48.75 | 7.81 | — | — | — | — | — | — |
| `multicannon` | Multi-barrelled Cannon | Multi-cannon | venart | shared (17n) | 2000 | 50.0 | 0 | 400 | 250 | 500 | 13.13 | 1.88 | — | — | — | — | — | — |
| `musketeer` | Musketeer, 17th century | Shooter | venbar | shared (11n) | 70 | 6.0 | 45 | 6 | 5 | 12 | 15.0 | 4.69 | — | — | — | — | — | — |
| `musketeer18` | Musketeer, 18th century | Shooter | venba2 | shared (13n) | 100 | 4.5 | 50 | 40 | 40 | 10 | 1.22 | 0.0 | — | — | — | — | — | — |
| `officer` | Officer, 17th century | Light Infantry | venbar | shared (16n) | 125 | 10.0 | 50 | 150 | 30 | 30 | 1.22 | 0.0 | 2 | 2 | 5 | 200 | 10 | 30 |
| `officer18` | Officer, 18th century | Light Infantry | venba2 | shared (17n) | 125 | 6.0 | 50 | 200 | 10 | 50 | 1.22 | 0.0 | — | — | — | — | — | — |
| `peaspa` | Peasant | Peasant | vencen | shared (4n) | 50 | 12.5 | 100 | 0 | 0 | 20 | 1.22 | 0.0 | — | — | — | — | — | — |
| `pikeman` | Pikeman, 17th century | Light Infantry | venbar | shared (13n) | 90 | 4.5 | 25 | 3 | 20 | 8 | 1.88 | 0.0 | 3 | 2 | 4 | 210 | 6 | 40 |
| `pikeman18` | Pikeman, 18th century | Light Infantry | venba2 | shared (16n) | 85 | 1.25 | 30 | 2 | 0 | 9 | 1.88 | 0.0 | — | — | — | — | — | — |
| `priest` | Priest | Light Infantry | ventem | shared (16n) | 100 | 15.0 | 30 | 10 | 0 | 15 | 9.38 | 0.0 | — | — | — | — | — | — |
| `reiter` | Reiter | Heavy Cavalry | vensta | shared (14n) | 300 | 24.0 | 120 | 10 | 40 | 15 | 1.22 | 0.0 | 2 | 6 | 6 | 190 | 15 | 40 |
| `roundshierdip` | Roundshier (mercenary) | Light Infantry | vendip | common | 100 | 4.0 | 20 | 3 | 25 | 6 | 1.13 | 0.0 | 3 | 3 | 7 | 225 | 16 | 80 |
| `unitbox` | — | — | — | common | 100 | 3.12 | 100 | 0 | 0 | — | — | — | — | — | — | — | — | — |
| `yacht` | Yacht | Yacht | eurpor | common | 31000 | 48.0 | 0 | 450 | 150 | 1000 | 20.63 | 10.94 | — | — | — | — | — | — |

### tur — Turkey (29 юнитов)

| sid | name | usage | trained_in | uniqueness | HP | Time | F | G | I | dmg | rng (t) | reload | пика | меч | пуля | картечь | стрела | ядро |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `archerdip` | Archer (mercenary) | Archer | turdip | common | 65 | 3.0 | 45 | 4 | 0 | 20 | 16.88 | 2.66 | — | — | — | — | — | — |
| `archertur` | Turkish archer | Archer | turbar | unique | 65 | 3.0 | 45 | 4 | 0 | 20 | 16.88 | 2.66 | — | — | — | — | — | — |
| `archerturdip` | Turkish archer (mercenary) | Archer | turdip | common | 65 | 3.0 | 45 | 4 | 0 | 20 | 16.88 | 2.66 | — | — | — | — | — | — |
| `battleship` | Ship of the Line | Battleship | turpor | common | 90000 | 390.0 | 0 | 3200 | 700 | 1800 | 36.56 | 0.62 | — | — | — | — | — | — |
| `cannon` | Cannon | Cannon | turart | common | 9000 | 75.0 | 0 | 400 | 400 | 1800 | 40.5 | 10.94 | — | — | — | — | — | — |
| `cossacksichdip` | Sich Cossack (mercenary) | Light Cavalry | turdip | common | 250 | 13.5 | 130 | 0 | 2 | 13 | 1.22 | 0.0 | — | — | — | — | — | — |
| `dragoon18dip` | Dragoon, 18th century (mercenary) | Mounted Shooter | turdip | common | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | — | — | — | — | — | — |
| `drummertur` | Drummer, 17th century | Light Infantry | turbar | semi-unique (2n) | 50 | 4.0 | 30 | 15 | 0 | — | — | — | — | — | — | — | — | — |
| `ferry` | Ferry | Transport | turpor | common | 62000 | 56.0 | 0 | 50 | 100 | — | — | — | — | — | — | — | — | — |
| `fishboat` | Boat | Fishing Boat | turpor | common | 300 | 40.0 | 0 | 0 | 0 | — | — | — | — | — | — | — | — | — |
| `galley` | Galley | Galley | turpor | common | 35000 | 50.0 | 0 | 900 | 800 | 100 | 22.5 | 4.69 | — | — | — | — | — | — |
| `grenadierdip` | Grenadier (mercenary) | Grenadier | turdip | common | 120 | 6.0 | 80 | 60 | 40 | 18 | 1.5 | 0.0 | — | — | — | — | — | — |
| `howitzer` | Howitzer | Mortar | turart | common | 3000 | 94.0 | 0 | 350 | 300 | 4000 | 26.25 | 18.75 | — | — | — | — | — | — |
| `jannisary` | Janissary | Shooter | turbar | unique | 65 | 8.0 | 55 | 13 | 5 | 12 | 15.94 | 4.69 | — | — | — | — | — | — |
| `lightcavalrydip` | Light cavalry (mercenary) | Mounted Shooter | turdip | common | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | — | — | — | — | — | — |
| `lightinfantry` | Light Infantryman | Light Infantry | turbar | semi-unique (2n) | 55 | 1.0 | 25 | 0 | 1 | 5 | 0.94 | 0.0 | — | — | — | — | — | — |
| `lightinfantrydip` | Light Infantryman (mercenary) | Light Infantry | turdip | common | 55 | 1.0 | 25 | 0 | 1 | 5 | 0.94 | 0.0 | — | — | — | — | — | — |
| `mortar` | Bombard | Super Mortar | turart | common | 400 | 25.0 | 0 | 75 | 200 | 200 | 48.75 | 7.81 | — | — | — | — | — | — |
| `mullah` | Mullah | Light Infantry | turtem | semi-unique (2n) | 100 | 15.0 | 30 | 10 | 0 | 15 | 9.38 | 0.0 | — | — | — | — | — | — |
| `officertur` | Officer | Light Infantry | turbar | semi-unique (2n) | 125 | 7.5 | 50 | 100 | 0 | 30 | 1.22 | 0.0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `peatur` | Peasant | Peasant | turcen | semi-unique (2n) | 50 | 12.5 | 100 | 0 | 0 | 20 | 1.22 | 0.0 | — | — | — | — | — | — |
| `pikemantur` | Ottoman Pikeman | Light Infantry | turbar | semi-unique (2n) | 95 | 5.5 | 55 | 5 | 0 | 9 | 2.06 | 0.0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `roundshierdip` | Roundshier (mercenary) | Light Infantry | turdip | common | 100 | 4.0 | 20 | 3 | 25 | 6 | 1.13 | 0.0 | 3 | 3 | 7 | 225 | 16 | 80 |
| `sipahi` | Heavy Sipahi | Heavy Cavalry | tursta | unique | 360 | 18.0 | 130 | 20 | 70 | 15 | 1.22 | 0.0 | 3 | 7 | 4 | 225 | 24 | 60 |
| `spakh` | Light Sipahi | Heavy Cavalry | tursta | unique | 230 | 9.0 | 80 | 6 | 5 | 15 | 1.88 | 0.0 | 0 | 1 | 0 | 10 | 2 | 0 |
| `tatar` | Tatar | Archer | tursta | unique | 185 | 11.25 | 70 | 6 | 0 | 15 | 20.63 | 1.56 | — | — | — | — | — | — |
| `unitbox` | — | — | — | common | 100 | 3.12 | 100 | 0 | 0 | — | — | — | — | — | — | — | — | — |
| `xebec` | Xebec | Frigate | turpor | semi-unique (2n) | 65000 | 230.0 | 0 | 1600 | 320 | 1800 | 31.88 | 1.56 | — | — | — | — | — | — |
| `yachttur` | Yacht | Yacht | turpor | unique | 31000 | 48.0 | 0 | 450 | 150 | 1000 | 20.63 | 10.94 | — | — | — | — | — | — |

### alg — Algeria (25 юнитов)

| sid | name | usage | trained_in | uniqueness | HP | Time | F | G | I | dmg | rng (t) | reload | пика | меч | пуля | картечь | стрела | ядро |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `archer` | Archer | Archer | algbar | unique | 40 | 1.5 | 20 | 1 | 0 | 15 | 15.0 | 2.34 | — | — | — | — | — | — |
| `archerdip` | Archer (mercenary) | Archer | algdip | common | 40 | 1.5 | 20 | 1 | 0 | 15 | 15.0 | 2.34 | — | — | — | — | — | — |
| `archerturdip` | Turkish archer (mercenary) | Archer | algdip | common | 40 | 1.5 | 20 | 1 | 0 | 15 | 15.0 | 2.34 | — | — | — | — | — | — |
| `battleship` | Ship of the Line | Battleship | turpor | common | 90000 | 390.0 | 0 | 3200 | 700 | 1800 | 36.56 | 0.62 | — | — | — | — | — | — |
| `cannon` | Cannon | Cannon | algart | common | 9000 | 75.0 | 0 | 400 | 400 | 1800 | 40.5 | 10.94 | — | — | — | — | — | — |
| `cossacksichdip` | Sich Cossack (mercenary) | Light Cavalry | algdip | common | 250 | 13.5 | 130 | 0 | 2 | 13 | 1.22 | 0.0 | — | — | — | — | — | — |
| `dragoon18dip` | Dragoon, 18th century (mercenary) | Mounted Shooter | algdip | common | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | — | — | — | — | — | — |
| `drummertur` | Drummer, 17th century | Light Infantry | algbar | semi-unique (2n) | 50 | 4.0 | 30 | 15 | 0 | — | — | — | — | — | — | — | — | — |
| `ferry` | Ferry | Transport | turpor | common | 62000 | 56.0 | 0 | 50 | 100 | — | — | — | — | — | — | — | — | — |
| `fishboat` | Boat | Fishing Boat | turpor | common | 300 | 40.0 | 0 | 0 | 0 | — | — | — | — | — | — | — | — | — |
| `galley` | Galley | Galley | turpor | common | 35000 | 50.0 | 0 | 900 | 800 | 100 | 22.5 | 4.69 | — | — | — | — | — | — |
| `grenadierdip` | Grenadier (mercenary) | Grenadier | algdip | common | 120 | 6.0 | 80 | 60 | 40 | 18 | 1.5 | 0.0 | — | — | — | — | — | — |
| `howitzer` | Howitzer | Mortar | algart | common | 3000 | 94.0 | 0 | 350 | 300 | 4000 | 26.25 | 18.75 | — | — | — | — | — | — |
| `lightcavalrydip` | Light cavalry (mercenary) | Mounted Shooter | algdip | common | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | — | — | — | — | — | — |
| `lightinfantry` | Light Infantryman | Light Infantry | algbar | semi-unique (2n) | 55 | 1.0 | 25 | 0 | 1 | 5 | 0.94 | 0.0 | — | — | — | — | — | — |
| `lightinfantrydip` | Light Infantryman (mercenary) | Light Infantry | algdip | common | 55 | 1.0 | 25 | 0 | 1 | 5 | 0.94 | 0.0 | — | — | — | — | — | — |
| `mameluke` | Mameluke | Heavy Cavalry | algsta | unique | 280 | 12.0 | 100 | 8 | 0 | 16 | 1.88 | 0.0 | 1 | 3 | 1 | 75 | 8 | 0 |
| `mortar` | Bombard | Super Mortar | algart | common | 400 | 25.0 | 0 | 75 | 200 | 200 | 48.75 | 7.81 | — | — | — | — | — | — |
| `mullah` | Mullah | Light Infantry | algtem | semi-unique (2n) | 100 | 15.0 | 30 | 10 | 0 | 15 | 9.38 | 0.0 | — | — | — | — | — | — |
| `officertur` | Officer | Light Infantry | algbar | semi-unique (2n) | 125 | 7.5 | 50 | 100 | 0 | 30 | 1.22 | 0.0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `peatur` | Peasant | Peasant | algcen | semi-unique (2n) | 50 | 12.5 | 100 | 0 | 0 | 20 | 1.22 | 0.0 | — | — | — | — | — | — |
| `pikemantur` | Ottoman Pikeman | Light Infantry | algbar | semi-unique (2n) | 95 | 5.5 | 55 | 5 | 0 | 9 | 2.06 | 0.0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `roundshierdip` | Roundshier (mercenary) | Light Infantry | algdip | common | 100 | 4.0 | 20 | 3 | 25 | 6 | 1.13 | 0.0 | 3 | 3 | 7 | 225 | 16 | 80 |
| `unitbox` | — | — | — | common | 100 | 3.12 | 100 | 0 | 0 | — | — | — | — | — | — | — | — | — |
| `xebec` | Xebec | Frigate | turpor | semi-unique (2n) | 65000 | 230.0 | 0 | 1600 | 320 | 1800 | 31.88 | 1.56 | — | — | — | — | — | — |

### net — Netherlands (35 юнитов)

| sid | name | usage | trained_in | uniqueness | HP | Time | F | G | I | dmg | rng (t) | reload | пика | меч | пуля | картечь | стрела | ядро |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `archerdip` | Archer (mercenary) | Archer | netdip | common | 40 | 1.5 | 20 | 1 | 0 | 15 | 15.0 | 2.34 | — | — | — | — | — | — |
| `archerturdip` | Turkish archer (mercenary) | Archer | netdip | common | 40 | 1.5 | 20 | 1 | 0 | 15 | 15.0 | 2.34 | — | — | — | — | — | — |
| `battleship` | Ship of the Line | Battleship | eurpor | common | 90000 | 390.0 | 0 | 3200 | 700 | 1800 | 36.56 | 0.62 | — | — | — | — | — | — |
| `cannon` | Cannon | Cannon | netart | common | 9000 | 75.0 | 0 | 400 | 400 | 1800 | 40.5 | 10.94 | — | — | — | — | — | — |
| `cossacksichdip` | Sich Cossack (mercenary) | Light Cavalry | netdip | common | 250 | 13.5 | 130 | 0 | 2 | 13 | 1.22 | 0.0 | — | — | — | — | — | — |
| `cuirassier` | Cuirassier | Heavy Cavalry | netsta | shared (17n) | 300 | 22.5 | 120 | 35 | 25 | 14 | 1.22 | 0.0 | 2 | 4 | 10 | 160 | 5 | 80 |
| `dragoon` | Dragoon, 17th century | Mounted Shooter | netsta | shared (16n) | 220 | 15.0 | 90 | 7 | 5 | 15 | 15.0 | 5.62 | — | — | — | — | — | — |
| `dragoon18dip` | Dragoon, 18th century (mercenary) | Mounted Shooter | netdip | common | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | — | — | — | — | — | — |
| `dragoon18net` | Dragoon, 18th century | Mounted Shooter | netsta | unique | 320 | 24.0 | 100 | 70 | 7 | 17 | 15.94 | 5.0 | — | — | — | — | — | — |
| `drummer` | Drummer, 17th century | Light Infantry | netbar | shared (16n) | 75 | 6.0 | 50 | 30 | 0 | — | — | — | — | — | — | — | — | — |
| `drummer18` | Drummer, 18th century | Light Infantry | netba2 | shared (16n) | 75 | 6.0 | 50 | 30 | 0 | — | — | — | — | — | — | — | — | — |
| `ferry` | Ferry | Transport | eurpor | common | 62000 | 56.0 | 0 | 50 | 100 | — | — | — | — | — | — | — | — | — |
| `fishboat` | Boat | Fishing Boat | eurpor | common | 300 | 40.0 | 0 | 0 | 0 | — | — | — | — | — | — | — | — | — |
| `frigate` | Frigate | Frigate | eurpor | common | 50000 | 230.0 | 0 | 1100 | 600 | 1800 | 30.94 | 2.34 | — | — | — | — | — | — |
| `galley` | Galley | Galley | eurpor | common | 35000 | 50.0 | 0 | 900 | 800 | 100 | 22.5 | 4.69 | — | — | — | — | — | — |
| `grenadier` | Grenadier | Grenadier | netba2 | shared (13n) | 120 | 6.0 | 80 | 60 | 40 | 18 | 1.5 | 0.0 | — | — | — | — | — | — |
| `grenadierdip` | Grenadier (mercenary) | Grenadier | netdip | common | 120 | 6.0 | 80 | 60 | 40 | 18 | 1.5 | 0.0 | — | — | — | — | — | — |
| `howitzer` | Howitzer | Mortar | netart | common | 3000 | 94.0 | 0 | 350 | 300 | 4000 | 26.25 | 18.75 | — | — | — | — | — | — |
| `hussar` | Hussar | Light Cavalry | netsta | shared (14n) | 230 | 15.0 | 70 | 20 | 2 | 12 | 1.22 | 0.0 | — | — | — | — | — | — |
| `lightcavalrydip` | Light cavalry (mercenary) | Mounted Shooter | netdip | common | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | — | — | — | — | — | — |
| `lightinfantrydip` | Light Infantryman (mercenary) | Light Infantry | netdip | common | 55 | 1.0 | 25 | 0 | 1 | 5 | 0.94 | 0.0 | — | — | — | — | — | — |
| `mortar` | Bombard | Super Mortar | netart | common | 400 | 25.0 | 0 | 75 | 200 | 200 | 48.75 | 7.81 | — | — | — | — | — | — |
| `multicannon` | Multi-barrelled Cannon | Multi-cannon | netart | shared (17n) | 2000 | 50.0 | 0 | 400 | 250 | 500 | 13.13 | 1.88 | — | — | — | — | — | — |
| `musketeer18` | Musketeer, 18th century | Shooter | netba2 | shared (13n) | 100 | 4.5 | 50 | 40 | 40 | 10 | 1.22 | 0.0 | — | — | — | — | — | — |
| `musketeernet` | Musketeer, 17th century | Shooter | netbar | unique | 65 | 5.0 | 50 | 8 | 4 | 10 | 15.0 | 3.75 | — | — | — | — | — | — |
| `officer` | Officer, 17th century | Light Infantry | netbar | shared (16n) | 125 | 10.0 | 50 | 150 | 30 | 30 | 1.22 | 0.0 | 2 | 2 | 5 | 200 | 10 | 30 |
| `officer18` | Officer, 18th century | Light Infantry | netba2 | shared (17n) | 125 | 6.0 | 50 | 200 | 10 | 50 | 1.22 | 0.0 | — | — | — | — | — | — |
| `peaeng` | Peasant | Peasant | netcen | shared (5n) | 50 | 12.5 | 100 | 0 | 0 | 20 | 1.22 | 0.0 | — | — | — | — | — | — |
| `pikeman` | Pikeman, 17th century | Light Infantry | netbar | shared (13n) | 90 | 4.5 | 25 | 3 | 20 | 8 | 1.88 | 0.0 | 3 | 2 | 4 | 210 | 6 | 40 |
| `pikeman18` | Pikeman, 18th century | Light Infantry | netba2 | shared (16n) | 85 | 1.25 | 30 | 2 | 0 | 9 | 1.88 | 0.0 | — | — | — | — | — | — |
| `priest` | Priest | Light Infantry | nettem | shared (16n) | 100 | 15.0 | 30 | 10 | 0 | 15 | 9.38 | 0.0 | — | — | — | — | — | — |
| `reiter` | Reiter | Heavy Cavalry | netsta | shared (14n) | 300 | 24.0 | 120 | 10 | 40 | 15 | 1.22 | 0.0 | 2 | 6 | 6 | 190 | 15 | 40 |
| `roundshierdip` | Roundshier (mercenary) | Light Infantry | netdip | common | 100 | 4.0 | 20 | 3 | 25 | 6 | 1.13 | 0.0 | 3 | 3 | 7 | 225 | 16 | 80 |
| `unitbox` | — | — | — | common | 100 | 3.12 | 100 | 0 | 0 | — | — | — | — | — | — | — | — | — |
| `yacht` | Yacht | Yacht | eurpor | common | 31000 | 48.0 | 0 | 450 | 150 | 1000 | 20.63 | 10.94 | — | — | — | — | — | — |

### den — Denmark (35 юнитов)

| sid | name | usage | trained_in | uniqueness | HP | Time | F | G | I | dmg | rng (t) | reload | пика | меч | пуля | картечь | стрела | ядро |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `archerdip` | Archer (mercenary) | Archer | dendip | common | 40 | 1.5 | 20 | 1 | 0 | 15 | 15.0 | 2.34 | — | — | — | — | — | — |
| `archerturdip` | Turkish archer (mercenary) | Archer | dendip | common | 40 | 1.5 | 20 | 1 | 0 | 15 | 15.0 | 2.34 | — | — | — | — | — | — |
| `battleship` | Ship of the Line | Battleship | eurpor | common | 90000 | 390.0 | 0 | 3200 | 700 | 1800 | 36.56 | 0.62 | — | — | — | — | — | — |
| `cannon` | Cannon | Cannon | denart | common | 9000 | 75.0 | 0 | 400 | 400 | 1800 | 40.5 | 10.94 | — | — | — | — | — | — |
| `cossacksichdip` | Sich Cossack (mercenary) | Light Cavalry | dendip | common | 250 | 13.5 | 130 | 0 | 2 | 13 | 1.22 | 0.0 | — | — | — | — | — | — |
| `cuirassier` | Cuirassier | Heavy Cavalry | densta | shared (17n) | 300 | 22.5 | 120 | 35 | 25 | 14 | 1.22 | 0.0 | 2 | 4 | 10 | 160 | 5 | 80 |
| `dragoon` | Dragoon, 17th century | Mounted Shooter | densta | shared (16n) | 220 | 15.0 | 90 | 7 | 5 | 15 | 15.0 | 5.62 | — | — | — | — | — | — |
| `dragoon18` | Dragoon, 18th century | Mounted Shooter | densta | shared (13n) | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | — | — | — | — | — | — |
| `dragoon18dip` | Dragoon, 18th century (mercenary) | Mounted Shooter | dendip | common | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | — | — | — | — | — | — |
| `drummer` | Drummer, 17th century | Light Infantry | denbar | shared (16n) | 75 | 6.0 | 50 | 30 | 0 | — | — | — | — | — | — | — | — | — |
| `drummer18` | Drummer, 18th century | Light Infantry | denba2 | shared (16n) | 75 | 6.0 | 50 | 30 | 0 | — | — | — | — | — | — | — | — | — |
| `ferry` | Ferry | Transport | eurpor | common | 62000 | 56.0 | 0 | 50 | 100 | — | — | — | — | — | — | — | — | — |
| `fishboat` | Boat | Fishing Boat | eurpor | common | 300 | 40.0 | 0 | 0 | 0 | — | — | — | — | — | — | — | — | — |
| `frigate` | Frigate | Frigate | eurpor | common | 50000 | 230.0 | 0 | 1100 | 600 | 1800 | 30.94 | 2.34 | — | — | — | — | — | — |
| `galley` | Galley | Galley | eurpor | common | 35000 | 50.0 | 0 | 900 | 800 | 100 | 22.5 | 4.69 | — | — | — | — | — | — |
| `grenadierden` | Grenadier | Grenadier | denba2 | unique | 125 | 6.5 | 100 | 90 | 40 | 22 | 1.5 | 0.0 | — | — | — | — | — | — |
| `grenadierdip` | Grenadier (mercenary) | Grenadier | dendip | common | 120 | 6.0 | 80 | 60 | 40 | 18 | 1.5 | 0.0 | — | — | — | — | — | — |
| `howitzer` | Howitzer | Mortar | denart | common | 3000 | 94.0 | 0 | 350 | 300 | 4000 | 26.25 | 18.75 | — | — | — | — | — | — |
| `hussar` | Hussar | Light Cavalry | densta | shared (14n) | 230 | 15.0 | 70 | 20 | 2 | 12 | 1.22 | 0.0 | — | — | — | — | — | — |
| `lightcavalrydip` | Light cavalry (mercenary) | Mounted Shooter | dendip | common | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | — | — | — | — | — | — |
| `lightinfantrydip` | Light Infantryman (mercenary) | Light Infantry | dendip | common | 55 | 1.0 | 25 | 0 | 1 | 5 | 0.94 | 0.0 | — | — | — | — | — | — |
| `mortar` | Bombard | Super Mortar | denart | common | 400 | 25.0 | 0 | 75 | 200 | 200 | 48.75 | 7.81 | — | — | — | — | — | — |
| `multicannon` | Multi-barrelled Cannon | Multi-cannon | denart | shared (17n) | 2000 | 50.0 | 0 | 400 | 250 | 500 | 13.13 | 1.88 | — | — | — | — | — | — |
| `musketeer` | Musketeer, 17th century | Shooter | denbar | shared (11n) | 70 | 6.0 | 45 | 6 | 5 | 12 | 15.0 | 4.69 | — | — | — | — | — | — |
| `musketeer18den` | Musketeer, 18th century | Shooter | denba2 | unique | 100 | 5.5 | 50 | 80 | 40 | 8 | 1.59 | 0.0 | — | — | — | — | — | — |
| `officer` | Officer, 17th century | Light Infantry | denbar | shared (16n) | 125 | 10.0 | 50 | 150 | 30 | 30 | 1.22 | 0.0 | 2 | 2 | 5 | 200 | 10 | 30 |
| `officer18` | Officer, 18th century | Light Infantry | denba2 | shared (17n) | 125 | 6.0 | 50 | 200 | 10 | 50 | 1.22 | 0.0 | — | — | — | — | — | — |
| `peaeng` | Peasant | Peasant | dencen | shared (5n) | 50 | 12.5 | 100 | 0 | 0 | 20 | 1.22 | 0.0 | — | — | — | — | — | — |
| `pikeman` | Pikeman, 17th century | Light Infantry | denbar | shared (13n) | 90 | 4.5 | 25 | 3 | 20 | 8 | 1.88 | 0.0 | 3 | 2 | 4 | 210 | 6 | 40 |
| `pikeman18` | Pikeman, 18th century | Light Infantry | denba2 | shared (16n) | 85 | 1.25 | 30 | 2 | 0 | 9 | 1.88 | 0.0 | — | — | — | — | — | — |
| `priest` | Priest | Light Infantry | dentem | shared (16n) | 100 | 15.0 | 30 | 10 | 0 | 15 | 9.38 | 0.0 | — | — | — | — | — | — |
| `reiter` | Reiter | Heavy Cavalry | densta | shared (14n) | 300 | 24.0 | 120 | 10 | 40 | 15 | 1.22 | 0.0 | 2 | 6 | 6 | 190 | 15 | 40 |
| `roundshierdip` | Roundshier (mercenary) | Light Infantry | dendip | common | 100 | 4.0 | 20 | 3 | 25 | 6 | 1.13 | 0.0 | 3 | 3 | 7 | 225 | 16 | 80 |
| `unitbox` | — | — | — | common | 100 | 3.12 | 100 | 0 | 0 | — | — | — | — | — | — | — | — | — |
| `yacht` | Yacht | Yacht | eurpor | common | 31000 | 48.0 | 0 | 450 | 150 | 1000 | 20.63 | 10.94 | — | — | — | — | — | — |

### por — Portugal (36 юнитов)

| sid | name | usage | trained_in | uniqueness | HP | Time | F | G | I | dmg | rng (t) | reload | пика | меч | пуля | картечь | стрела | ядро |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `archerdip` | Archer (mercenary) | Archer | pordip | common | 40 | 1.5 | 20 | 1 | 0 | 15 | 15.0 | 2.34 | — | — | — | — | — | — |
| `archerturdip` | Turkish archer (mercenary) | Archer | pordip | common | 40 | 1.5 | 20 | 1 | 0 | 15 | 15.0 | 2.34 | — | — | — | — | — | — |
| `battleship` | Ship of the Line | Battleship | porpor | common | 90000 | 390.0 | 0 | 3200 | 700 | 1800 | 36.56 | 0.62 | — | — | — | — | — | — |
| `cannon` | Cannon | Cannon | porart | common | 9000 | 75.0 | 0 | 400 | 400 | 1800 | 40.5 | 10.94 | — | — | — | — | — | — |
| `cossacksichdip` | Sich Cossack (mercenary) | Light Cavalry | pordip | common | 250 | 13.5 | 130 | 0 | 2 | 13 | 1.22 | 0.0 | — | — | — | — | — | — |
| `cuirassier` | Cuirassier | Heavy Cavalry | porsta | shared (17n) | 300 | 22.5 | 120 | 35 | 25 | 14 | 1.22 | 0.0 | 2 | 4 | 10 | 160 | 5 | 80 |
| `dragoon` | Dragoon, 17th century | Mounted Shooter | porsta | shared (16n) | 220 | 15.0 | 90 | 7 | 5 | 15 | 15.0 | 5.62 | — | — | — | — | — | — |
| `dragoon18` | Dragoon, 18th century | Mounted Shooter | porsta | shared (13n) | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | — | — | — | — | — | — |
| `dragoon18dip` | Dragoon, 18th century (mercenary) | Mounted Shooter | pordip | common | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | — | — | — | — | — | — |
| `drummer` | Drummer, 17th century | Light Infantry | porbar | shared (16n) | 75 | 6.0 | 50 | 30 | 0 | — | — | — | — | — | — | — | — | — |
| `drummer18` | Drummer, 18th century | Light Infantry | porba2 | shared (16n) | 75 | 6.0 | 50 | 30 | 0 | — | — | — | — | — | — | — | — | — |
| `ferry` | Ferry | Transport | porpor | common | 62000 | 56.0 | 0 | 50 | 100 | — | — | — | — | — | — | — | — | — |
| `fishboat` | Boat | Fishing Boat | porpor | common | 300 | 40.0 | 0 | 0 | 0 | — | — | — | — | — | — | — | — | — |
| `frigate` | Frigate | Frigate | porpor | common | 50000 | 230.0 | 0 | 1100 | 600 | 1800 | 30.94 | 2.34 | — | — | — | — | — | — |
| `galley` | Galley | Galley | porpor | common | 35000 | 50.0 | 0 | 900 | 800 | 100 | 22.5 | 4.69 | — | — | — | — | — | — |
| `grenadier` | Grenadier | Grenadier | porba2 | shared (13n) | 120 | 6.0 | 80 | 60 | 40 | 18 | 1.5 | 0.0 | — | — | — | — | — | — |
| `grenadierdip` | Grenadier (mercenary) | Grenadier | pordip | common | 120 | 6.0 | 80 | 60 | 40 | 18 | 1.5 | 0.0 | — | — | — | — | — | — |
| `howitzer` | Howitzer | Mortar | porart | common | 3000 | 94.0 | 0 | 350 | 300 | 4000 | 26.25 | 18.75 | — | — | — | — | — | — |
| `hussar` | Hussar | Light Cavalry | porsta | shared (14n) | 230 | 15.0 | 70 | 20 | 2 | 12 | 1.22 | 0.0 | — | — | — | — | — | — |
| `jagerpor` | Volunteer | Shooter | porba2 | unique | 50 | 6.0 | 30 | 2 | 5 | 10 | 15.0 | 5.94 | — | — | — | — | — | — |
| `lightcavalrydip` | Light cavalry (mercenary) | Mounted Shooter | pordip | common | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | — | — | — | — | — | — |
| `lightinfantrydip` | Light Infantryman (mercenary) | Light Infantry | pordip | common | 55 | 1.0 | 25 | 0 | 1 | 5 | 0.94 | 0.0 | — | — | — | — | — | — |
| `mortar` | Bombard | Super Mortar | porart | common | 400 | 25.0 | 0 | 75 | 200 | 200 | 48.75 | 7.81 | — | — | — | — | — | — |
| `multicannon` | Multi-barrelled Cannon | Multi-cannon | porart | shared (17n) | 2000 | 50.0 | 0 | 400 | 250 | 500 | 13.13 | 1.88 | — | — | — | — | — | — |
| `musketeer` | Musketeer, 17th century | Shooter | porbar | shared (11n) | 70 | 6.0 | 45 | 6 | 5 | 12 | 15.0 | 4.69 | — | — | — | — | — | — |
| `musketeer18` | Musketeer, 18th century | Shooter | porba2 | shared (13n) | 100 | 4.5 | 50 | 40 | 40 | 10 | 1.22 | 0.0 | — | — | — | — | — | — |
| `officer` | Officer, 17th century | Light Infantry | porbar | shared (16n) | 125 | 10.0 | 50 | 150 | 30 | 30 | 1.22 | 0.0 | 2 | 2 | 5 | 200 | 10 | 30 |
| `officer18` | Officer, 18th century | Light Infantry | porba2 | shared (17n) | 125 | 6.0 | 50 | 200 | 10 | 50 | 1.22 | 0.0 | — | — | — | — | — | — |
| `peaspa` | Peasant | Peasant | porcen | shared (4n) | 50 | 12.5 | 100 | 0 | 0 | 20 | 1.22 | 0.0 | — | — | — | — | — | — |
| `pikeman18` | Pikeman, 18th century | Light Infantry | porba2 | shared (16n) | 85 | 1.25 | 30 | 2 | 0 | 9 | 1.88 | 0.0 | — | — | — | — | — | — |
| `pikemanpor` | Pikeman, 17th century | Light Infantry | porbar | unique | 100 | 4.0 | 40 | 4 | 5 | 9 | 1.88 | 0.0 | 0 | 1 | 1 | 25 | 4 | 0 |
| `priest` | Priest | Light Infantry | portem | shared (16n) | 100 | 15.0 | 30 | 10 | 0 | 15 | 9.38 | 0.0 | — | — | — | — | — | — |
| `reiter` | Reiter | Heavy Cavalry | porsta | shared (14n) | 300 | 24.0 | 120 | 10 | 40 | 15 | 1.22 | 0.0 | 2 | 6 | 6 | 190 | 15 | 40 |
| `roundshierdip` | Roundshier (mercenary) | Light Infantry | pordip | common | 100 | 4.0 | 20 | 3 | 25 | 6 | 1.13 | 0.0 | 3 | 3 | 7 | 225 | 16 | 80 |
| `unitbox` | — | — | — | common | 100 | 3.12 | 100 | 0 | 0 | — | — | — | — | — | — | — | — | — |
| `yacht` | Yacht | Yacht | porpor | common | 31000 | 48.0 | 0 | 450 | 150 | 1000 | 20.63 | 10.94 | — | — | — | — | — | — |

### pie — Piedmont (35 юнитов)

| sid | name | usage | trained_in | uniqueness | HP | Time | F | G | I | dmg | rng (t) | reload | пика | меч | пуля | картечь | стрела | ядро |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `archerdip` | Archer (mercenary) | Archer | piedip | common | 40 | 1.5 | 20 | 1 | 0 | 15 | 15.0 | 2.34 | — | — | — | — | — | — |
| `archerturdip` | Turkish archer (mercenary) | Archer | piedip | common | 40 | 1.5 | 20 | 1 | 0 | 15 | 15.0 | 2.34 | — | — | — | — | — | — |
| `battleship` | Ship of the Line | Battleship | eurpor | common | 90000 | 390.0 | 0 | 3200 | 700 | 1800 | 36.56 | 0.62 | — | — | — | — | — | — |
| `cannon` | Cannon | Cannon | pieart | common | 9000 | 75.0 | 0 | 400 | 400 | 1800 | 40.5 | 10.94 | — | — | — | — | — | — |
| `cossacksichdip` | Sich Cossack (mercenary) | Light Cavalry | piedip | common | 250 | 13.5 | 130 | 0 | 2 | 13 | 1.22 | 0.0 | — | — | — | — | — | — |
| `cuirassier` | Cuirassier | Heavy Cavalry | piesta | shared (17n) | 300 | 22.5 | 120 | 35 | 25 | 14 | 1.22 | 0.0 | 2 | 4 | 10 | 160 | 5 | 80 |
| `dragoon` | Dragoon, 17th century | Mounted Shooter | piesta | shared (16n) | 220 | 15.0 | 90 | 7 | 5 | 15 | 15.0 | 5.62 | — | — | — | — | — | — |
| `dragoon18dip` | Dragoon, 18th century (mercenary) | Mounted Shooter | piedip | common | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | — | — | — | — | — | — |
| `dragoon18pie` | Dragoon, 18th century | Mounted Shooter | piesta | unique | 200 | 20.25 | 60 | 65 | 7 | 19 | 16.88 | 5.0 | — | — | — | — | — | — |
| `drummer` | Drummer, 17th century | Light Infantry | piebar | shared (16n) | 75 | 6.0 | 50 | 30 | 0 | — | — | — | — | — | — | — | — | — |
| `drummer18` | Drummer, 18th century | Light Infantry | pieba2 | shared (16n) | 75 | 6.0 | 50 | 30 | 0 | — | — | — | — | — | — | — | — | — |
| `ferry` | Ferry | Transport | eurpor | common | 62000 | 56.0 | 0 | 50 | 100 | — | — | — | — | — | — | — | — | — |
| `fishboat` | Boat | Fishing Boat | eurpor | common | 300 | 40.0 | 0 | 0 | 0 | — | — | — | — | — | — | — | — | — |
| `frigate` | Frigate | Frigate | eurpor | common | 50000 | 230.0 | 0 | 1100 | 600 | 1800 | 30.94 | 2.34 | — | — | — | — | — | — |
| `galley` | Galley | Galley | eurpor | common | 35000 | 50.0 | 0 | 900 | 800 | 100 | 22.5 | 4.69 | — | — | — | — | — | — |
| `grenadier` | Grenadier | Grenadier | pieba2 | shared (13n) | 120 | 6.0 | 80 | 60 | 40 | 18 | 1.5 | 0.0 | — | — | — | — | — | — |
| `grenadierdip` | Grenadier (mercenary) | Grenadier | piedip | common | 120 | 6.0 | 80 | 60 | 40 | 18 | 1.5 | 0.0 | — | — | — | — | — | — |
| `howitzer` | Howitzer | Mortar | pieart | common | 3000 | 94.0 | 0 | 350 | 300 | 4000 | 26.25 | 18.75 | — | — | — | — | — | — |
| `hussar` | Hussar | Light Cavalry | piesta | shared (14n) | 230 | 15.0 | 70 | 20 | 2 | 12 | 1.22 | 0.0 | — | — | — | — | — | — |
| `lightcavalrydip` | Light cavalry (mercenary) | Mounted Shooter | piedip | common | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | — | — | — | — | — | — |
| `lightinfantrydip` | Light Infantryman (mercenary) | Light Infantry | piedip | common | 55 | 1.0 | 25 | 0 | 1 | 5 | 0.94 | 0.0 | — | — | — | — | — | — |
| `mortar` | Bombard | Super Mortar | pieart | common | 400 | 25.0 | 0 | 75 | 200 | 200 | 48.75 | 7.81 | — | — | — | — | — | — |
| `multicannon` | Multi-barrelled Cannon | Multi-cannon | pieart | shared (17n) | 2000 | 50.0 | 0 | 400 | 250 | 500 | 13.13 | 1.88 | — | — | — | — | — | — |
| `musketeer` | Musketeer, 17th century | Shooter | piebar | shared (11n) | 70 | 6.0 | 45 | 6 | 5 | 12 | 15.0 | 4.69 | — | — | — | — | — | — |
| `musketeer18` | Musketeer, 18th century | Shooter | pieba2 | shared (13n) | 100 | 4.5 | 50 | 40 | 40 | 10 | 1.22 | 0.0 | — | — | — | — | — | — |
| `officer` | Officer, 17th century | Light Infantry | piebar | shared (16n) | 125 | 10.0 | 50 | 150 | 30 | 30 | 1.22 | 0.0 | 2 | 2 | 5 | 200 | 10 | 30 |
| `officer18` | Officer, 18th century | Light Infantry | pieba2 | shared (17n) | 125 | 6.0 | 50 | 200 | 10 | 50 | 1.22 | 0.0 | — | — | — | — | — | — |
| `padre` | Padre | Light Infantry | pietem | unique | 100 | 15.0 | 30 | 10 | 0 | 15 | 9.38 | 0.0 | — | — | — | — | — | — |
| `peaspa` | Peasant | Peasant | piecen | shared (4n) | 50 | 12.5 | 100 | 0 | 0 | 20 | 1.22 | 0.0 | — | — | — | — | — | — |
| `pikeman` | Pikeman, 17th century | Light Infantry | piebar | shared (13n) | 90 | 4.5 | 25 | 3 | 20 | 8 | 1.88 | 0.0 | 3 | 2 | 4 | 210 | 6 | 40 |
| `pikeman18` | Pikeman, 18th century | Light Infantry | pieba2 | shared (16n) | 85 | 1.25 | 30 | 2 | 0 | 9 | 1.88 | 0.0 | — | — | — | — | — | — |
| `reiter` | Reiter | Heavy Cavalry | piesta | shared (14n) | 300 | 24.0 | 120 | 10 | 40 | 15 | 1.22 | 0.0 | 2 | 6 | 6 | 190 | 15 | 40 |
| `roundshierdip` | Roundshier (mercenary) | Light Infantry | piedip | common | 100 | 4.0 | 20 | 3 | 25 | 6 | 1.13 | 0.0 | 3 | 3 | 7 | 225 | 16 | 80 |
| `unitbox` | — | — | — | common | 100 | 3.12 | 100 | 0 | 0 | — | — | — | — | — | — | — | — | — |
| `yacht` | Yacht | Yacht | eurpor | common | 31000 | 48.0 | 0 | 450 | 150 | 1000 | 20.63 | 10.94 | — | — | — | — | — | — |

### sax — Saxony (36 юнитов)

| sid | name | usage | trained_in | uniqueness | HP | Time | F | G | I | dmg | rng (t) | reload | пика | меч | пуля | картечь | стрела | ядро |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `archerdip` | Archer (mercenary) | Archer | saxdip | common | 40 | 1.5 | 20 | 1 | 0 | 15 | 15.0 | 2.34 | — | — | — | — | — | — |
| `archerturdip` | Turkish archer (mercenary) | Archer | saxdip | common | 40 | 1.5 | 20 | 1 | 0 | 15 | 15.0 | 2.34 | — | — | — | — | — | — |
| `battleship` | Ship of the Line | Battleship | eurpor | common | 90000 | 390.0 | 0 | 3200 | 700 | 1800 | 36.56 | 0.62 | — | — | — | — | — | — |
| `cannon` | Cannon | Cannon | saxart | common | 9000 | 75.0 | 0 | 400 | 400 | 1800 | 40.5 | 10.94 | — | — | — | — | — | — |
| `cossacksichdip` | Sich Cossack (mercenary) | Light Cavalry | saxdip | common | 250 | 13.5 | 130 | 0 | 2 | 13 | 1.22 | 0.0 | — | — | — | — | — | — |
| `cuirassier` | Cuirassier | Heavy Cavalry | saxsta | shared (17n) | 300 | 22.5 | 120 | 35 | 25 | 14 | 1.22 | 0.0 | 2 | 4 | 10 | 160 | 5 | 80 |
| `dragoon` | Dragoon, 17th century | Mounted Shooter | saxsta | shared (16n) | 220 | 15.0 | 90 | 7 | 5 | 15 | 15.0 | 5.62 | — | — | — | — | — | — |
| `dragoon18` | Dragoon, 18th century | Mounted Shooter | saxsta | shared (13n) | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | — | — | — | — | — | — |
| `dragoon18dip` | Dragoon, 18th century (mercenary) | Mounted Shooter | saxdip | common | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | — | — | — | — | — | — |
| `drummer` | Drummer, 17th century | Light Infantry | saxbar | shared (16n) | 75 | 6.0 | 50 | 30 | 0 | — | — | — | — | — | — | — | — | — |
| `drummer18` | Drummer, 18th century | Light Infantry | saxba2 | shared (16n) | 75 | 6.0 | 50 | 30 | 0 | — | — | — | — | — | — | — | — | — |
| `ferry` | Ferry | Transport | eurpor | common | 62000 | 56.0 | 0 | 50 | 100 | — | — | — | — | — | — | — | — | — |
| `fishboat` | Boat | Fishing Boat | eurpor | common | 300 | 40.0 | 0 | 0 | 0 | — | — | — | — | — | — | — | — | — |
| `frigate` | Frigate | Frigate | eurpor | common | 50000 | 230.0 | 0 | 1100 | 600 | 1800 | 30.94 | 2.34 | — | — | — | — | — | — |
| `galley` | Galley | Galley | eurpor | common | 35000 | 50.0 | 0 | 900 | 800 | 100 | 22.5 | 4.69 | — | — | — | — | — | — |
| `grenadierdip` | Grenadier (mercenary) | Grenadier | saxdip | common | 120 | 6.0 | 80 | 60 | 40 | 18 | 1.5 | 0.0 | — | — | — | — | — | — |
| `grenadiersax` | Grenadier | Grenadier | saxba2 | unique | 100 | 6.0 | 50 | 60 | 40 | 22 | 1.5 | 0.0 | — | — | — | — | — | — |
| `guardcavalrysax` | Cavalry Guard | Heavy Cavalry | saxsta | unique | 320 | 24.0 | 140 | 50 | 20 | 15 | 1.22 | 0.0 | 2 | 5 | 9 | 150 | 9 | 70 |
| `howitzer` | Howitzer | Mortar | saxart | common | 3000 | 94.0 | 0 | 350 | 300 | 4000 | 26.25 | 18.75 | — | — | — | — | — | — |
| `hussar` | Hussar | Light Cavalry | saxsta | shared (14n) | 230 | 15.0 | 70 | 20 | 2 | 12 | 1.22 | 0.0 | — | — | — | — | — | — |
| `lightcavalrydip` | Light cavalry (mercenary) | Mounted Shooter | saxdip | common | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | — | — | — | — | — | — |
| `lightinfantrydip` | Light Infantryman (mercenary) | Light Infantry | saxdip | common | 55 | 1.0 | 25 | 0 | 1 | 5 | 0.94 | 0.0 | — | — | — | — | — | — |
| `mortar` | Bombard | Super Mortar | saxart | common | 400 | 25.0 | 0 | 75 | 200 | 200 | 48.75 | 7.81 | — | — | — | — | — | — |
| `multicannon` | Multi-barrelled Cannon | Multi-cannon | saxart | shared (17n) | 2000 | 50.0 | 0 | 400 | 250 | 500 | 13.13 | 1.88 | — | — | — | — | — | — |
| `musketeer` | Musketeer, 17th century | Shooter | saxbar | shared (11n) | 70 | 6.0 | 45 | 6 | 5 | 12 | 15.0 | 4.69 | — | — | — | — | — | — |
| `musketeer18sax` | Musketeer, 18th century | Shooter | saxba2 | unique | 90 | 4.5 | 40 | 45 | 40 | 7 | 1.22 | 0.0 | — | — | — | — | — | — |
| `officer` | Officer, 17th century | Light Infantry | saxbar | shared (16n) | 125 | 10.0 | 50 | 150 | 30 | 30 | 1.22 | 0.0 | 2 | 2 | 5 | 200 | 10 | 30 |
| `officer18` | Officer, 18th century | Light Infantry | saxba2 | shared (17n) | 125 | 6.0 | 50 | 200 | 10 | 50 | 1.22 | 0.0 | — | — | — | — | — | — |
| `peaaus` | Peasant | Peasant | saxcen | shared (5n) | 50 | 12.5 | 100 | 0 | 0 | 20 | 1.22 | 0.0 | — | — | — | — | — | — |
| `pikeman` | Pikeman, 17th century | Light Infantry | saxbar | shared (13n) | 90 | 4.5 | 25 | 3 | 20 | 8 | 1.88 | 0.0 | 3 | 2 | 4 | 210 | 6 | 40 |
| `pikeman18` | Pikeman, 18th century | Light Infantry | saxba2 | shared (16n) | 85 | 1.25 | 30 | 2 | 0 | 9 | 1.88 | 0.0 | — | — | — | — | — | — |
| `priest` | Priest | Light Infantry | saxtem | shared (16n) | 100 | 15.0 | 30 | 10 | 0 | 15 | 9.38 | 0.0 | — | — | — | — | — | — |
| `reiter` | Reiter | Heavy Cavalry | saxsta | shared (14n) | 300 | 24.0 | 120 | 10 | 40 | 15 | 1.22 | 0.0 | 2 | 6 | 6 | 190 | 15 | 40 |
| `roundshierdip` | Roundshier (mercenary) | Light Infantry | saxdip | common | 100 | 4.0 | 20 | 3 | 25 | 6 | 1.13 | 0.0 | 3 | 3 | 7 | 225 | 16 | 80 |
| `unitbox` | — | — | — | common | 100 | 3.12 | 100 | 0 | 0 | — | — | — | — | — | — | — | — | — |
| `yacht` | Yacht | Yacht | eurpor | common | 31000 | 48.0 | 0 | 450 | 150 | 1000 | 20.63 | 10.94 | — | — | — | — | — | — |

### bav — Bavaria (35 юнитов)

| sid | name | usage | trained_in | uniqueness | HP | Time | F | G | I | dmg | rng (t) | reload | пика | меч | пуля | картечь | стрела | ядро |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `archerdip` | Archer (mercenary) | Archer | bavdip | common | 40 | 1.5 | 20 | 1 | 0 | 15 | 15.0 | 2.34 | — | — | — | — | — | — |
| `archerturdip` | Turkish archer (mercenary) | Archer | bavdip | common | 40 | 1.5 | 20 | 1 | 0 | 15 | 15.0 | 2.34 | — | — | — | — | — | — |
| `battleship` | Ship of the Line | Battleship | eurpor | common | 90000 | 390.0 | 0 | 3200 | 700 | 1800 | 36.56 | 0.62 | — | — | — | — | — | — |
| `cannon` | Cannon | Cannon | bavart | common | 9000 | 75.0 | 0 | 400 | 400 | 1800 | 40.5 | 10.94 | — | — | — | — | — | — |
| `cossacksichdip` | Sich Cossack (mercenary) | Light Cavalry | bavdip | common | 250 | 13.5 | 130 | 0 | 2 | 13 | 1.22 | 0.0 | — | — | — | — | — | — |
| `cuirassier` | Cuirassier | Heavy Cavalry | bavsta | shared (17n) | 300 | 22.5 | 120 | 35 | 25 | 14 | 1.22 | 0.0 | 2 | 4 | 10 | 160 | 5 | 80 |
| `dragoon` | Dragoon, 17th century | Mounted Shooter | bavsta | shared (16n) | 220 | 15.0 | 90 | 7 | 5 | 15 | 15.0 | 5.62 | — | — | — | — | — | — |
| `dragoon18` | Dragoon, 18th century | Mounted Shooter | bavsta | shared (13n) | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | — | — | — | — | — | — |
| `dragoon18dip` | Dragoon, 18th century (mercenary) | Mounted Shooter | bavdip | common | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | — | — | — | — | — | — |
| `drummer` | Drummer, 17th century | Light Infantry | bavbar | shared (16n) | 75 | 6.0 | 50 | 30 | 0 | — | — | — | — | — | — | — | — | — |
| `drummer18` | Drummer, 18th century | Light Infantry | bavba2 | shared (16n) | 75 | 6.0 | 50 | 30 | 0 | — | — | — | — | — | — | — | — | — |
| `ferry` | Ferry | Transport | eurpor | common | 62000 | 56.0 | 0 | 50 | 100 | — | — | — | — | — | — | — | — | — |
| `fishboat` | Boat | Fishing Boat | eurpor | common | 300 | 40.0 | 0 | 0 | 0 | — | — | — | — | — | — | — | — | — |
| `frigate` | Frigate | Frigate | eurpor | common | 50000 | 230.0 | 0 | 1100 | 600 | 1800 | 30.94 | 2.34 | — | — | — | — | — | — |
| `galley` | Galley | Galley | eurpor | common | 35000 | 50.0 | 0 | 900 | 800 | 100 | 22.5 | 4.69 | — | — | — | — | — | — |
| `grenadierbav` | Grenadier | Grenadier | bavba2 | unique | 125 | 6.0 | 95 | 70 | 40 | 14 | 1.5 | 0.0 | — | — | — | — | — | — |
| `grenadierdip` | Grenadier (mercenary) | Grenadier | bavdip | common | 120 | 6.0 | 80 | 60 | 40 | 18 | 1.5 | 0.0 | — | — | — | — | — | — |
| `howitzer` | Howitzer | Mortar | bavart | common | 3000 | 94.0 | 0 | 350 | 300 | 4000 | 26.25 | 18.75 | — | — | — | — | — | — |
| `hussar` | Hussar | Light Cavalry | bavsta | shared (14n) | 230 | 15.0 | 70 | 20 | 2 | 12 | 1.22 | 0.0 | — | — | — | — | — | — |
| `lightcavalrydip` | Light cavalry (mercenary) | Mounted Shooter | bavdip | common | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | — | — | — | — | — | — |
| `lightinfantrydip` | Light Infantryman (mercenary) | Light Infantry | bavdip | common | 55 | 1.0 | 25 | 0 | 1 | 5 | 0.94 | 0.0 | — | — | — | — | — | — |
| `mortar` | Bombard | Super Mortar | bavart | common | 400 | 25.0 | 0 | 75 | 200 | 200 | 48.75 | 7.81 | — | — | — | — | — | — |
| `multicannon` | Multi-barrelled Cannon | Multi-cannon | bavart | shared (17n) | 2000 | 50.0 | 0 | 400 | 250 | 500 | 13.13 | 1.88 | — | — | — | — | — | — |
| `musketeer` | Musketeer, 17th century | Shooter | bavbar | shared (11n) | 70 | 6.0 | 45 | 6 | 5 | 12 | 15.0 | 4.69 | — | — | — | — | — | — |
| `musketeer18bav` | Musketeer, 18th century | Shooter | bavba2 | unique | 100 | 5.0 | 60 | 55 | 35 | 5 | 1.59 | 0.0 | — | — | — | — | — | — |
| `officer` | Officer, 17th century | Light Infantry | bavbar | shared (16n) | 125 | 10.0 | 50 | 150 | 30 | 30 | 1.22 | 0.0 | 2 | 2 | 5 | 200 | 10 | 30 |
| `officer18` | Officer, 18th century | Light Infantry | bavba2 | shared (17n) | 125 | 6.0 | 50 | 200 | 10 | 50 | 1.22 | 0.0 | — | — | — | — | — | — |
| `peaaus` | Peasant | Peasant | bavcen | shared (5n) | 50 | 12.5 | 100 | 0 | 0 | 20 | 1.22 | 0.0 | — | — | — | — | — | — |
| `pikeman` | Pikeman, 17th century | Light Infantry | bavbar | shared (13n) | 90 | 4.5 | 25 | 3 | 20 | 8 | 1.88 | 0.0 | 3 | 2 | 4 | 210 | 6 | 40 |
| `pikeman18` | Pikeman, 18th century | Light Infantry | bavba2 | shared (16n) | 85 | 1.25 | 30 | 2 | 0 | 9 | 1.88 | 0.0 | — | — | — | — | — | — |
| `priest` | Priest | Light Infantry | bavtem | shared (16n) | 100 | 15.0 | 30 | 10 | 0 | 15 | 9.38 | 0.0 | — | — | — | — | — | — |
| `reiter` | Reiter | Heavy Cavalry | bavsta | shared (14n) | 300 | 24.0 | 120 | 10 | 40 | 15 | 1.22 | 0.0 | 2 | 6 | 6 | 190 | 15 | 40 |
| `roundshierdip` | Roundshier (mercenary) | Light Infantry | bavdip | common | 100 | 4.0 | 20 | 3 | 25 | 6 | 1.13 | 0.0 | 3 | 3 | 7 | 225 | 16 | 80 |
| `unitbox` | — | — | — | common | 100 | 3.12 | 100 | 0 | 0 | — | — | — | — | — | — | — | — | — |
| `yacht` | Yacht | Yacht | eurpor | common | 31000 | 48.0 | 0 | 450 | 150 | 1000 | 20.63 | 10.94 | — | — | — | — | — | — |

### hun — Hungary (36 юнитов)

| sid | name | usage | trained_in | uniqueness | HP | Time | F | G | I | dmg | rng (t) | reload | пика | меч | пуля | картечь | стрела | ядро |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `archerdip` | Archer (mercenary) | Archer | hundip | common | 40 | 1.5 | 20 | 1 | 0 | 15 | 15.0 | 2.34 | — | — | — | — | — | — |
| `archerturdip` | Turkish archer (mercenary) | Archer | hundip | common | 40 | 1.5 | 20 | 1 | 0 | 15 | 15.0 | 2.34 | — | — | — | — | — | — |
| `battleship` | Ship of the Line | Battleship | eurpor | common | 90000 | 390.0 | 0 | 3200 | 700 | 1800 | 36.56 | 0.62 | — | — | — | — | — | — |
| `cannon` | Cannon | Cannon | hunart | common | 9000 | 75.0 | 0 | 400 | 400 | 1800 | 40.5 | 10.94 | — | — | — | — | — | — |
| `cossacksichdip` | Sich Cossack (mercenary) | Light Cavalry | hundip | common | 250 | 13.5 | 130 | 0 | 2 | 13 | 1.22 | 0.0 | — | — | — | — | — | — |
| `cuirassier` | Cuirassier | Heavy Cavalry | hunsta | shared (17n) | 300 | 22.5 | 120 | 35 | 25 | 14 | 1.22 | 0.0 | 2 | 4 | 10 | 160 | 5 | 80 |
| `dragoon` | Dragoon, 17th century | Mounted Shooter | hunsta | shared (16n) | 220 | 15.0 | 90 | 7 | 5 | 15 | 15.0 | 5.62 | — | — | — | — | — | — |
| `dragoon18dip` | Dragoon, 18th century (mercenary) | Mounted Shooter | hundip | common | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | — | — | — | — | — | — |
| `drummer` | Drummer, 17th century | Light Infantry | hunbar | shared (16n) | 75 | 6.0 | 50 | 30 | 0 | — | — | — | — | — | — | — | — | — |
| `drummer18` | Drummer, 18th century | Light Infantry | hunba2 | shared (16n) | 75 | 6.0 | 50 | 30 | 0 | — | — | — | — | — | — | — | — | — |
| `ferry` | Ferry | Transport | eurpor | common | 62000 | 56.0 | 0 | 50 | 100 | — | — | — | — | — | — | — | — | — |
| `fishboat` | Boat | Fishing Boat | eurpor | common | 300 | 40.0 | 0 | 0 | 0 | — | — | — | — | — | — | — | — | — |
| `frigate` | Frigate | Frigate | eurpor | common | 50000 | 230.0 | 0 | 1100 | 600 | 1800 | 30.94 | 2.34 | — | — | — | — | — | — |
| `galley` | Galley | Galley | eurpor | common | 35000 | 50.0 | 0 | 900 | 800 | 100 | 22.5 | 4.69 | — | — | — | — | — | — |
| `gauduk` | Hajduk | Shooter | hunbar | unique | 60 | 4.5 | 35 | 4 | 4 | 9 | 14.06 | 3.12 | — | — | — | — | — | — |
| `grenadierdip` | Grenadier (mercenary) | Grenadier | hundip | common | 120 | 6.0 | 80 | 60 | 40 | 18 | 1.5 | 0.0 | — | — | — | — | — | — |
| `grenadierhun` | Grenadier | Grenadier | hunba2 | unique | 125 | 6.5 | 90 | 80 | 40 | 30 | 1.5 | 0.0 | — | — | — | — | — | — |
| `howitzer` | Howitzer | Mortar | hunart | common | 3000 | 94.0 | 0 | 350 | 300 | 4000 | 26.25 | 18.75 | — | — | — | — | — | — |
| `hussarhun` | Hussar | Light Cavalry | hunsta | unique | 250 | 21.0 | 100 | 30 | 2 | 10 | 1.22 | 0.0 | — | — | — | — | — | — |
| `lightcavalry` | Light cavalry | Mounted Shooter | hunsta | unique | 175 | 21.0 | 90 | 50 | 6 | 14 | 18.75 | 5.31 | — | — | — | — | — | — |
| `lightcavalrydip` | Light cavalry (mercenary) | Mounted Shooter | hundip | common | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | — | — | — | — | — | — |
| `lightinfantrydip` | Light Infantryman (mercenary) | Light Infantry | hundip | common | 55 | 1.0 | 25 | 0 | 1 | 5 | 0.94 | 0.0 | — | — | — | — | — | — |
| `mortar` | Bombard | Super Mortar | hunart | common | 400 | 25.0 | 0 | 75 | 200 | 200 | 48.75 | 7.81 | — | — | — | — | — | — |
| `multicannon` | Multi-barrelled Cannon | Multi-cannon | hunart | shared (17n) | 2000 | 50.0 | 0 | 400 | 250 | 500 | 13.13 | 1.88 | — | — | — | — | — | — |
| `musketeer18` | Musketeer, 18th century | Shooter | hunba2 | shared (13n) | 100 | 4.5 | 50 | 40 | 40 | 10 | 1.22 | 0.0 | — | — | — | — | — | — |
| `officer` | Officer, 17th century | Light Infantry | hunbar | shared (16n) | 125 | 10.0 | 50 | 150 | 30 | 30 | 1.22 | 0.0 | 2 | 2 | 5 | 200 | 10 | 30 |
| `officer18` | Officer, 18th century | Light Infantry | hunba2 | shared (17n) | 125 | 6.0 | 50 | 200 | 10 | 50 | 1.22 | 0.0 | — | — | — | — | — | — |
| `pandurhun` | Szekely | Shooter | hunba2 | unique | 75 | 6.0 | 30 | 25 | 10 | 19 | 18.75 | 5.0 | — | — | — | — | — | — |
| `peapol` | Peasant | Peasant | huncen | semi-unique (2n) | 50 | 12.5 | 100 | 0 | 0 | 20 | 1.22 | 0.0 | — | — | — | — | — | — |
| `pikeman` | Pikeman, 17th century | Light Infantry | hunbar | shared (13n) | 90 | 4.5 | 25 | 3 | 20 | 8 | 1.88 | 0.0 | 3 | 2 | 4 | 210 | 6 | 40 |
| `pikeman18` | Pikeman, 18th century | Light Infantry | hunba2 | shared (16n) | 85 | 1.25 | 30 | 2 | 0 | 9 | 1.88 | 0.0 | — | — | — | — | — | — |
| `priest` | Priest | Light Infantry | huntem | shared (16n) | 100 | 15.0 | 30 | 10 | 0 | 15 | 9.38 | 0.0 | — | — | — | — | — | — |
| `reiter` | Reiter | Heavy Cavalry | hunsta | shared (14n) | 300 | 24.0 | 120 | 10 | 40 | 15 | 1.22 | 0.0 | 2 | 6 | 6 | 190 | 15 | 40 |
| `roundshierdip` | Roundshier (mercenary) | Light Infantry | hundip | common | 100 | 4.0 | 20 | 3 | 25 | 6 | 1.13 | 0.0 | 3 | 3 | 7 | 225 | 16 | 80 |
| `unitbox` | — | — | — | common | 100 | 3.12 | 100 | 0 | 0 | — | — | — | — | — | — | — | — | — |
| `yacht` | Yacht | Yacht | eurpor | common | 31000 | 48.0 | 0 | 450 | 150 | 1000 | 20.63 | 10.94 | — | — | — | — | — | — |

### swi — Switzerland (36 юнитов)

| sid | name | usage | trained_in | uniqueness | HP | Time | F | G | I | dmg | rng (t) | reload | пика | меч | пуля | картечь | стрела | ядро |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `archerdip` | Archer (mercenary) | Archer | swidip | common | 40 | 1.5 | 20 | 1 | 0 | 15 | 15.0 | 2.34 | — | — | — | — | — | — |
| `archerturdip` | Turkish archer (mercenary) | Archer | swidip | common | 40 | 1.5 | 20 | 1 | 0 | 15 | 15.0 | 2.34 | — | — | — | — | — | — |
| `battleship` | Ship of the Line | Battleship | eurpor | common | 90000 | 390.0 | 0 | 3200 | 700 | 1800 | 36.56 | 0.62 | — | — | — | — | — | — |
| `cannon` | Cannon | Cannon | swiart | common | 9000 | 75.0 | 0 | 400 | 400 | 1800 | 40.5 | 10.94 | — | — | — | — | — | — |
| `cossacksichdip` | Sich Cossack (mercenary) | Light Cavalry | swidip | common | 250 | 13.5 | 130 | 0 | 2 | 13 | 1.22 | 0.0 | — | — | — | — | — | — |
| `cuirassier` | Cuirassier | Heavy Cavalry | swista | shared (17n) | 300 | 22.5 | 120 | 35 | 25 | 14 | 1.22 | 0.0 | 2 | 4 | 10 | 160 | 5 | 80 |
| `dragoon` | Dragoon, 17th century | Mounted Shooter | swista | shared (16n) | 220 | 15.0 | 90 | 7 | 5 | 15 | 15.0 | 5.62 | — | — | — | — | — | — |
| `dragoon18` | Dragoon, 18th century | Mounted Shooter | swista | shared (13n) | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | — | — | — | — | — | — |
| `dragoon18dip` | Dragoon, 18th century (mercenary) | Mounted Shooter | swidip | common | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | — | — | — | — | — | — |
| `drummer` | Drummer, 17th century | Light Infantry | swibar | shared (16n) | 75 | 6.0 | 50 | 30 | 0 | — | — | — | — | — | — | — | — | — |
| `drummer18` | Drummer, 18th century | Light Infantry | swiba2 | shared (16n) | 75 | 6.0 | 50 | 30 | 0 | — | — | — | — | — | — | — | — | — |
| `ferry` | Ferry | Transport | eurpor | common | 62000 | 56.0 | 0 | 50 | 100 | — | — | — | — | — | — | — | — | — |
| `fishboat` | Boat | Fishing Boat | eurpor | common | 300 | 40.0 | 0 | 0 | 0 | — | — | — | — | — | — | — | — | — |
| `frigate` | Frigate | Frigate | eurpor | common | 50000 | 230.0 | 0 | 1100 | 600 | 1800 | 30.94 | 2.34 | — | — | — | — | — | — |
| `galley` | Galley | Galley | eurpor | common | 35000 | 50.0 | 0 | 900 | 800 | 100 | 22.5 | 4.69 | — | — | — | — | — | — |
| `grenadier` | Grenadier | Grenadier | swiba2 | shared (13n) | 120 | 6.0 | 80 | 60 | 40 | 18 | 1.5 | 0.0 | — | — | — | — | — | — |
| `grenadierdip` | Grenadier (mercenary) | Grenadier | swidip | common | 120 | 6.0 | 80 | 60 | 40 | 18 | 1.5 | 0.0 | — | — | — | — | — | — |
| `howitzer` | Howitzer | Mortar | swiart | common | 3000 | 94.0 | 0 | 350 | 300 | 4000 | 26.25 | 18.75 | — | — | — | — | — | — |
| `hussarswi` | Mounted Jaeger | Light Cavalry | swista | unique | 265 | 19.5 | 120 | 30 | 2 | 14 | 1.22 | 0.0 | — | — | — | — | — | — |
| `jagerswi` | Jaeger | Shooter | swiba2 | unique | 65 | 6.0 | 40 | 70 | 20 | 20 | 22.5 | 6.88 | — | — | — | — | — | — |
| `lightcavalrydip` | Light cavalry (mercenary) | Mounted Shooter | swidip | common | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | — | — | — | — | — | — |
| `lightinfantrydip` | Light Infantryman (mercenary) | Light Infantry | swidip | common | 55 | 1.0 | 25 | 0 | 1 | 5 | 0.94 | 0.0 | — | — | — | — | — | — |
| `mortar` | Bombard | Super Mortar | swiart | common | 400 | 25.0 | 0 | 75 | 200 | 200 | 48.75 | 7.81 | — | — | — | — | — | — |
| `multicannon` | Multi-barrelled Cannon | Multi-cannon | swiart | shared (17n) | 2000 | 50.0 | 0 | 400 | 250 | 500 | 13.13 | 1.88 | — | — | — | — | — | — |
| `musketeer` | Musketeer, 17th century | Shooter | swibar | shared (11n) | 70 | 6.0 | 45 | 6 | 5 | 12 | 15.0 | 4.69 | — | — | — | — | — | — |
| `musketeer18` | Musketeer, 18th century | Shooter | swiba2 | shared (13n) | 100 | 4.5 | 50 | 40 | 40 | 10 | 1.22 | 0.0 | — | — | — | — | — | — |
| `officer` | Officer, 17th century | Light Infantry | swibar | shared (16n) | 125 | 10.0 | 50 | 150 | 30 | 30 | 1.22 | 0.0 | 2 | 2 | 5 | 200 | 10 | 30 |
| `officer18` | Officer, 18th century | Light Infantry | swiba2 | shared (17n) | 125 | 6.0 | 50 | 200 | 10 | 50 | 1.22 | 0.0 | — | — | — | — | — | — |
| `peaaus` | Peasant | Peasant | swicen | shared (5n) | 50 | 12.5 | 100 | 0 | 0 | 20 | 1.22 | 0.0 | — | — | — | — | — | — |
| `pikeman18` | Pikeman, 18th century | Light Infantry | swiba2 | shared (16n) | 85 | 1.25 | 30 | 2 | 0 | 9 | 1.88 | 0.0 | — | — | — | — | — | — |
| `pikemanswi` | Pikeman, 17th century | Light Infantry | swibar | unique | 90 | 5.0 | 40 | 6 | 20 | 10 | 1.88 | 0.0 | 3 | 3 | 6 | 220 | 6 | 45 |
| `priest` | Priest | Light Infantry | switem | shared (16n) | 100 | 15.0 | 30 | 10 | 0 | 15 | 9.38 | 0.0 | — | — | — | — | — | — |
| `reiter` | Reiter | Heavy Cavalry | swista | shared (14n) | 300 | 24.0 | 120 | 10 | 40 | 15 | 1.22 | 0.0 | 2 | 6 | 6 | 190 | 15 | 40 |
| `roundshierdip` | Roundshier (mercenary) | Light Infantry | swidip | common | 100 | 4.0 | 20 | 3 | 25 | 6 | 1.13 | 0.0 | 3 | 3 | 7 | 225 | 16 | 80 |
| `unitbox` | — | — | — | common | 100 | 3.12 | 100 | 0 | 0 | — | — | — | — | — | — | — | — | — |
| `yacht` | Yacht | Yacht | eurpor | common | 31000 | 48.0 | 0 | 450 | 150 | 1000 | 20.63 | 10.94 | — | — | — | — | — | — |

### sco — Scotland (28 юнитов)

| sid | name | usage | trained_in | uniqueness | HP | Time | F | G | I | dmg | rng (t) | reload | пика | меч | пуля | картечь | стрела | ядро |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `archerdip` | Archer (mercenary) | Archer | scodip | common | 150 | 6.0 | 80 | 7 | 0 | 20 | 18.75 | 3.12 | — | — | — | — | — | — |
| `archersco` | Bow Clansman | Archer | scoba2 | unique | 150 | 6.0 | 80 | 7 | 0 | 20 | 18.75 | 3.12 | — | — | — | — | — | — |
| `archerturdip` | Turkish archer (mercenary) | Archer | scodip | common | 150 | 6.0 | 80 | 7 | 0 | 20 | 18.75 | 3.12 | — | — | — | — | — | — |
| `bagpiper` | Bagpiper | Light Infantry | scobar | semi-unique (2n) | 75 | 6.0 | 50 | 30 | 0 | — | — | — | — | — | — | — | — | — |
| `battleship` | Ship of the Line | Battleship | eurpor | common | 90000 | 390.0 | 0 | 3200 | 700 | 1800 | 36.56 | 0.62 | — | — | — | — | — | — |
| `cannon` | Cannon | Cannon | scoart | common | 9000 | 75.0 | 0 | 400 | 400 | 1800 | 40.5 | 10.94 | — | — | — | — | — | — |
| `cossacksichdip` | Sich Cossack (mercenary) | Light Cavalry | scodip | common | 250 | 13.5 | 130 | 0 | 2 | 13 | 1.22 | 0.0 | — | — | — | — | — | — |
| `dragoon18dip` | Dragoon, 18th century (mercenary) | Mounted Shooter | scodip | common | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | — | — | — | — | — | — |
| `ferry` | Ferry | Transport | eurpor | common | 62000 | 56.0 | 0 | 50 | 100 | — | — | — | — | — | — | — | — | — |
| `fishboat` | Boat | Fishing Boat | eurpor | common | 300 | 40.0 | 0 | 0 | 0 | — | — | — | — | — | — | — | — | — |
| `framegun` | Frame gun | Cannon | scoart | unique | 3000 | 50.0 | 0 | 300 | 150 | 500 | 33.75 | 2.81 | — | — | — | — | — | — |
| `frigate` | Frigate | Frigate | eurpor | common | 50000 | 230.0 | 0 | 1100 | 600 | 1800 | 30.94 | 2.34 | — | — | — | — | — | — |
| `grenadierdip` | Grenadier (mercenary) | Grenadier | scodip | common | 120 | 6.0 | 80 | 60 | 40 | 18 | 1.5 | 0.0 | — | — | — | — | — | — |
| `howitzer` | Howitzer | Mortar | scoart | common | 3000 | 94.0 | 0 | 350 | 300 | 4000 | 26.25 | 18.75 | — | — | — | — | — | — |
| `lancersco` | Lancer | Heavy Cavalry | scosta | unique | 320 | 21.0 | 120 | 6 | 0 | 11 | 1.88 | 0.0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `lightcavalrydip` | Light cavalry (mercenary) | Mounted Shooter | scodip | common | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | — | — | — | — | — | — |
| `lightinfantrydip` | Light Infantryman (mercenary) | Light Infantry | scodip | common | 55 | 1.0 | 25 | 0 | 1 | 5 | 0.94 | 0.0 | — | — | — | — | — | — |
| `mortar` | Bombard | Super Mortar | scoart | common | 400 | 25.0 | 0 | 75 | 200 | 200 | 48.75 | 7.81 | — | — | — | — | — | — |
| `musketeersco` | Covenanter musketeer | Shooter | scobar | unique | 90 | 7.0 | 55 | 8 | 7 | 12 | 15.94 | 4.69 | — | — | — | — | — | — |
| `officersco` | Officer | Light Infantry | scobar | unique | 150 | 10.0 | 130 | 130 | 10 | 40 | 1.22 | 0.0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `peasco` | Peasant | Peasant | scocen | unique | 60 | 12.5 | 100 | 0 | 0 | 20 | 1.22 | 0.0 | — | — | — | — | — | — |
| `pikemansco` | Covenanter pikeman | Light Infantry | scobar | unique | 100 | 4.0 | 35 | 2 | 0 | 9 | 1.88 | 0.0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `priest` | Priest | Light Infantry | scotem | shared (16n) | 100 | 15.0 | 30 | 10 | 0 | 15 | 9.38 | 0.0 | — | — | — | — | — | — |
| `raidersco` | Raider | Light Cavalry | scosta | unique | 280 | 22.5 | 130 | 8 | 2 | 11 | 1.22 | 0.0 | — | — | — | — | — | — |
| `roundshierdip` | Roundshier (mercenary) | Light Infantry | scodip | common | 180 | 7.0 | 110 | 10 | 0 | 10 | 1.13 | 0.0 | 1 | 2 | 2 | 110 | 6 | 10 |
| `swordsmansco` | Sword Clansman | Light Infantry | scoba2 | unique | 180 | 7.0 | 110 | 10 | 0 | 10 | 1.13 | 0.0 | 1 | 2 | 2 | 110 | 6 | 10 |
| `unitbox` | — | — | — | common | 100 | 3.12 | 100 | 0 | 0 | — | — | — | — | — | — | — | — | — |
| `yacht` | Yacht | Yacht | eurpor | common | 31000 | 48.0 | 0 | 450 | 150 | 1000 | 20.63 | 10.94 | — | — | — | — | — | — |

## 5b. Корабли

Морские юниты: рыбацкая лодка, военные суда (фрегат / xebec / battleship / chaika), стрелковые яхты / галеи. У всех `transport` — пассажирская грузоподъёмность, `fishingmax` — ёмкость трюма для рыбы, `fishingspeed` — тиков на одну рыбу.

| sid | nation | name | trained_in | HP | wood | gold | iron | coal | weap0 dmg | range (t) | reload (s) | weap0 cost | weap1 dmg | weap1 range | transport | fishingmax | fishingspeed | gold upkeep |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|
| `battleship` | aus | Ship of the Line | eurpor | 90000 | 9000 | 3200 | 700 | 6500 | 1800 | 36.56 | 0.62 | {"iron": 5, "coal": 15} | — | — | — | — | — | 15000 |
| `chaika` | ukr | — | ukrpor | 25000 | 1050 | 600 | 200 | 400 | 1000 | 20.63 | 2.34 | {"iron": 4, "coal": 9} | — | — | — | — | — | 0 |
| `fishboat` | aus | Boat | eurpor | 300 | 600 | 0 | 0 | 0 | — | — | — | — | — | — | — | 1000 | 12 | — |
| `frigate` | aus | Frigate | eurpor | 50000 | 5000 | 1100 | 600 | 800 | 1800 | 30.94 | 2.34 | {"iron": 25, "coal": 35} | — | — | — | — | — | 150 |
| `galley` | aus | Galley | eurpor | 35000 | 9500 | 900 | 800 | 0 | 100 | 22.5 | 4.69 | {"iron": 4, "coal": 9} | 1000 | 58.13 | — | — | — | 1000 |
| `xebec` | tur | Xebec | turpor | 65000 | 7000 | 1600 | 320 | 960 | 1800 | 31.88 | 1.56 | {"iron": 25, "coal": 35} | — | — | — | — | — | 0 |
| `yacht` | aus | Yacht | eurpor | 31000 | 900 | 450 | 150 | 200 | 1000 | 20.63 | 10.94 | {"iron": 4, "coal": 9} | — | — | — | — | — | 50 |
| `yachttur` | tur | Yacht | turpor | 31000 | 900 | 450 | 150 | 200 | 1000 | 20.63 | 10.94 | {"iron": 4, "coal": 9} | — | — | — | — | — | 50 |

**Заметки:**

- Базовая `fishingmax = 1000` у `fishboat`. Апгрейд `aca.5` (academy.5, **boat efficiency +100%**) удваивает грузоподъёмность лодки → 2000 рыбы за рейс.
- Апгрейд `aca.7` (`fishing boat cost -85%`) удешевляет постройку лодок.
- `transport` на торговых / транспортных судах = сколько юнитов поместится.
- `consume.gold` = золото в секунду игрового времени на upkeep (тратится при стрельбе).

## 5c. Шахты — апгрейды (gol/iro/coa)

Шахты сразу после постройки имеют `peasantabsorber = 5` (5 крестьян). Каждый апгрейд `<cluster>{gol|iro|coa}.X` добавляет N крестьян. Все 6 апгрейдов **накапливаются** на каждой шахте отдельно (`bindividual = True`). Полная прокачка одной шахты: **5 + 5 + 8 + 10 + 12 + 15 + 40 = 95 крестьян**.

| sid | level | +workers | F | G | total workers (cumulative) |
|---|---:|---:|---:|---:|---:|
| `eurcoa.1` | 2 | +5 | 1000 | 1250 | 10 |
| `eurcoa.2` | 3 | +8 | 5250 | 4950 | 18 |
| `eurcoa.3` | 4 | +10 | 12500 | 9250 | 28 |
| `eurcoa.4` | 5 | +12 | 15800 | 18500 | 40 |
| `eurcoa.5` | 6 | +15 | 19800 | 21050 | 55 |
| `eurcoa.6` | 7 | +40 | 50200 | 25950 | 95 |
| `eurgol.1` | 2 | +5 | 1000 | 1250 | 10 |
| `eurgol.2` | 3 | +8 | 5250 | 4950 | 18 |
| `eurgol.3` | 4 | +10 | 12500 | 9250 | 28 |
| `eurgol.4` | 5 | +12 | 15800 | 18500 | 40 |
| `eurgol.5` | 6 | +15 | 19800 | 21050 | 55 |
| `eurgol.6` | 7 | +40 | 50200 | 25950 | 95 |
| `euriro.1` | 2 | +5 | 1000 | 1250 | 10 |
| `euriro.2` | 3 | +8 | 5250 | 4950 | 18 |
| `euriro.3` | 4 | +10 | 12500 | 9250 | 28 |
| `euriro.4` | 5 | +12 | 15800 | 18500 | 40 |
| `euriro.5` | 6 | +15 | 19800 | 21050 | 55 |
| `euriro.6` | 7 | +40 | 50200 | 25950 | 95 |

**Стоимость полной прокачки одной шахты** (eur cluster, без override): F1000 + 5250 + 12500 + 15800 + 19800 + 50200 = **104 550 food**, G1250 + 4950 + 9250 + 18500 + 21050 + 25950 = **80 950 gold**.

**Производительность шахты:** 1 крестьянин внутри → +13 add to `gPlayer.counter.resincome[restype]` (`player.script`). Реальная скорость = 13 × 32 / 250 ≈ **1.664 ресурса / игр-сек на крестьянина**. Полностью прокачанная шахта (95 крестьян) = **158 / игр-сек** = **9460 / игр-мин**.

## 6. Боевая математика

### 6a. Damage formula

Расчёт реально нанесённого урона (`miscext2.script:_misc_DoDamage`):

```
damage = weapon.damage
if (target is fast cavalry on the move AND weapon kind in {arrow, bullet}):
    damage -= 5  # headshot bonus
if (target is fully built):
    damage -= target.shield
else:  # still under construction
    damage -= target.shield // 3
if (target in formation): damage -= squad.AddShield  (or AddShieldHold if hold-mode)
damage -= target.protection[weapon.kind]
damage = max(1, damage)  # minimum 1 damage per hit
target.hp -= damage
```

**Ключевые свойства:**

- `protection` и `shield` уменьшают урон **аддитивно** (не процентно).
- Минимум **1 хп** урона за попадание — нет нулевого урона, даже если protection > damage.
- Танки / слоны (высокий shield) безусловно лучше, чем тяжёлые protection — shield применяется ВСЕГДА.
- Pikeman vs cavalry: pike kind с damage 8-10 vs heavy cavalry protection_pike (типично 0-3) ≈ 5-10 хп / удар.
- Cavalry vs pikeman: sword / saber damage ≈ 5-7 vs pike protection (0-3) ≈ 2-7 хп / удар.
- Ranged attack: bullet / arrow damage 9-12 vs musketeer protection (default 0-4) ≈ 5-12 хп / удар; против тяжёлой пехоты с `protection_bullet ≥ 6` урон режется существенно.

### 6b. Скорости юнитов (абстрактные единицы)

Базовые `gc_obj_speed_*` из `dmscript.global:603-620`. Это **относительные** значения скорости, **не тайлы / сек**. Реальная скорость зависит от animation `walkInterval`, `walkintervalfactor` юнита и game speed. Для перевода в тайлы / сек нужен empirical test.

| Класс | Базовая скорость |
|---|---:|
| default | 32 |
| peasant | 40 |
| hardhorse | 56 |
| fasthorse | 96 |
| cannon | 20 |
| mortar | 24 |
| howitzer | 20 |
| multicannon | 16 |
| fishboat | 16 |
| ferry | 28 |
| yacht | 40 |
| yachttur | 70 |
| chaika | 55 |
| galley | 40 |
| frigate | 30 |
| xebec | 28 |
| battleship | 16 |

Большие значения = быстрее. fasthorse (96) ≈ ×3 от cannon (20). Peasant (40) примерно посередине. Battleship / multicannon (16) — самые медленные.

### 6c. Офицеры и формации

Каждая нация имеет N групп офицеров. Один офицер ведёт строй из определённых юнитов (чаще пехота / кавалерия одного класса). Формации стандартные для всех: **LINE / SQUARE / KARE × 15 / 36 / 72 / 120 / 196 / 400 юнитов**. Чем больше формация, тем сильнее бонусы (атака, защита, дистанция, мораль). Источник: `country.script:_country_InitOfficerFormations`.

#### aus — Austria (11 офицеров)

| officer | drummer | юниты в строю |
|---|---|---|
| `roundshierdip` | `roundshierdip` | roundshierdip |
| `grenadierdip` | `grenadierdip` | grenadierdip |
| `officer` | `drummer` | pikemanpol, roundshier, musketeer, musketeeraus, musketeerpol, musketeerspa, grenadierdip, roundshierdip (+5) |
| `officerrus` | `drummerrus` | pikemanrus, strelet, grenadierdip, roundshierdip |
| `officertur` | `drummertur` | pikemantur, lightinfantry, archer, archertur, jannisary, grenadierdip, roundshierdip |
| `officer18` | `drummer18` | pikeman18, pikeman18swe, pandur, chasseur, highlander, musketeer18, musketeer18pru, grenadier (+11) |
| `officer18` | `bagpiper` | pikeman18, pikeman18swe, pandur, chasseur, highlander, musketeer18, musketeer18pru, grenadier (+7) |
| `officersco` | `bagpiper` | pikemansco, musketeersco, grenadierdip, roundshierdip |
| `serdiuk` | `serdiuk` | serdiuk |
| `archersco` | `archersco` | archersco |
| `swordsmansco` | `swordsmansco` | swordsmansco |

#### fra — France (11 офицеров)

| officer | drummer | юниты в строю |
|---|---|---|
| `roundshierdip` | `roundshierdip` | roundshierdip |
| `grenadierdip` | `grenadierdip` | grenadierdip |
| `officer` | `drummer` | pikemanpol, roundshier, musketeer, musketeeraus, musketeerpol, musketeerspa, grenadierdip, roundshierdip (+5) |
| `officerrus` | `drummerrus` | pikemanrus, strelet, grenadierdip, roundshierdip |
| `officertur` | `drummertur` | pikemantur, lightinfantry, archer, archertur, jannisary, grenadierdip, roundshierdip |
| `officer18` | `drummer18` | pikeman18, pikeman18swe, pandur, chasseur, highlander, musketeer18, musketeer18pru, grenadier (+11) |
| `officer18` | `bagpiper` | pikeman18, pikeman18swe, pandur, chasseur, highlander, musketeer18, musketeer18pru, grenadier (+7) |
| `officersco` | `bagpiper` | pikemansco, musketeersco, grenadierdip, roundshierdip |
| `serdiuk` | `serdiuk` | serdiuk |
| `archersco` | `archersco` | archersco |
| `swordsmansco` | `swordsmansco` | swordsmansco |

#### eng — England (11 офицеров)

| officer | drummer | юниты в строю |
|---|---|---|
| `roundshierdip` | `roundshierdip` | roundshierdip |
| `grenadierdip` | `grenadierdip` | grenadierdip |
| `officer` | `drummer` | pikemanpol, roundshier, musketeer, musketeeraus, musketeerpol, musketeerspa, grenadierdip, roundshierdip (+5) |
| `officerrus` | `drummerrus` | pikemanrus, strelet, grenadierdip, roundshierdip |
| `officertur` | `drummertur` | pikemantur, lightinfantry, archer, archertur, jannisary, grenadierdip, roundshierdip |
| `officer18` | `drummer18` | pikeman18, pikeman18swe, pandur, chasseur, highlander, musketeer18, musketeer18pru, grenadier (+11) |
| `officer18` | `bagpiper` | pikeman18, pikeman18swe, pandur, chasseur, highlander, musketeer18, musketeer18pru, grenadier (+7) |
| `officersco` | `bagpiper` | pikemansco, musketeersco, grenadierdip, roundshierdip |
| `serdiuk` | `serdiuk` | serdiuk |
| `archersco` | `archersco` | archersco |
| `swordsmansco` | `swordsmansco` | swordsmansco |

#### spa — Spain (11 офицеров)

| officer | drummer | юниты в строю |
|---|---|---|
| `roundshierdip` | `roundshierdip` | roundshierdip |
| `grenadierdip` | `grenadierdip` | grenadierdip |
| `officer` | `drummer` | pikemanpol, roundshier, musketeer, musketeeraus, musketeerpol, musketeerspa, grenadierdip, roundshierdip (+5) |
| `officerrus` | `drummerrus` | pikemanrus, strelet, grenadierdip, roundshierdip |
| `officertur` | `drummertur` | pikemantur, lightinfantry, archer, archertur, jannisary, grenadierdip, roundshierdip |
| `officer18` | `drummer18` | pikeman18, pikeman18swe, pandur, chasseur, highlander, musketeer18, musketeer18pru, grenadier (+11) |
| `officer18` | `bagpiper` | pikeman18, pikeman18swe, pandur, chasseur, highlander, musketeer18, musketeer18pru, grenadier (+7) |
| `officersco` | `bagpiper` | pikemansco, musketeersco, grenadierdip, roundshierdip |
| `serdiuk` | `serdiuk` | serdiuk |
| `archersco` | `archersco` | archersco |
| `swordsmansco` | `swordsmansco` | swordsmansco |

#### rus — Russia (11 офицеров)

| officer | drummer | юниты в строю |
|---|---|---|
| `roundshierdip` | `roundshierdip` | roundshierdip |
| `grenadierdip` | `grenadierdip` | grenadierdip |
| `officer` | `drummer` | pikemanpol, roundshier, musketeer, musketeeraus, musketeerpol, musketeerspa, grenadierdip, roundshierdip (+5) |
| `officerrus` | `drummerrus` | pikemanrus, strelet, grenadierdip, roundshierdip |
| `officertur` | `drummertur` | pikemantur, lightinfantry, archer, archertur, jannisary, grenadierdip, roundshierdip |
| `officer18` | `drummer18` | pikeman18, pikeman18swe, pandur, chasseur, highlander, musketeer18, musketeer18pru, grenadier (+11) |
| `officer18` | `bagpiper` | pikeman18, pikeman18swe, pandur, chasseur, highlander, musketeer18, musketeer18pru, grenadier (+7) |
| `officersco` | `bagpiper` | pikemansco, musketeersco, grenadierdip, roundshierdip |
| `serdiuk` | `serdiuk` | serdiuk |
| `archersco` | `archersco` | archersco |
| `swordsmansco` | `swordsmansco` | swordsmansco |

#### ukr — Ukraine (11 офицеров)

| officer | drummer | юниты в строю |
|---|---|---|
| `roundshierdip` | `roundshierdip` | roundshierdip |
| `grenadierdip` | `grenadierdip` | grenadierdip |
| `officer` | `drummer` | pikemanpol, roundshier, musketeer, musketeeraus, musketeerpol, musketeerspa, grenadierdip, roundshierdip (+5) |
| `officerrus` | `drummerrus` | pikemanrus, strelet, grenadierdip, roundshierdip |
| `officertur` | `drummertur` | pikemantur, lightinfantry, archer, archertur, jannisary, grenadierdip, roundshierdip |
| `officer18` | `drummer18` | pikeman18, pikeman18swe, pandur, chasseur, highlander, musketeer18, musketeer18pru, grenadier (+11) |
| `officer18` | `bagpiper` | pikeman18, pikeman18swe, pandur, chasseur, highlander, musketeer18, musketeer18pru, grenadier (+7) |
| `officersco` | `bagpiper` | pikemansco, musketeersco, grenadierdip, roundshierdip |
| `serdiuk` | `serdiuk` | serdiuk |
| `archersco` | `archersco` | archersco |
| `swordsmansco` | `swordsmansco` | swordsmansco |

#### pol — Poland (11 офицеров)

| officer | drummer | юниты в строю |
|---|---|---|
| `roundshierdip` | `roundshierdip` | roundshierdip |
| `grenadierdip` | `grenadierdip` | grenadierdip |
| `officer` | `drummer` | pikemanpol, roundshier, musketeer, musketeeraus, musketeerpol, musketeerspa, grenadierdip, roundshierdip (+5) |
| `officerrus` | `drummerrus` | pikemanrus, strelet, grenadierdip, roundshierdip |
| `officertur` | `drummertur` | pikemantur, lightinfantry, archer, archertur, jannisary, grenadierdip, roundshierdip |
| `officer18` | `drummer18` | pikeman18, pikeman18swe, pandur, chasseur, highlander, musketeer18, musketeer18pru, grenadier (+11) |
| `officer18` | `bagpiper` | pikeman18, pikeman18swe, pandur, chasseur, highlander, musketeer18, musketeer18pru, grenadier (+7) |
| `officersco` | `bagpiper` | pikemansco, musketeersco, grenadierdip, roundshierdip |
| `serdiuk` | `serdiuk` | serdiuk |
| `archersco` | `archersco` | archersco |
| `swordsmansco` | `swordsmansco` | swordsmansco |

#### swe — Sweden (11 офицеров)

| officer | drummer | юниты в строю |
|---|---|---|
| `roundshierdip` | `roundshierdip` | roundshierdip |
| `grenadierdip` | `grenadierdip` | grenadierdip |
| `officer` | `drummer` | pikemanpol, roundshier, musketeer, musketeeraus, musketeerpol, musketeerspa, grenadierdip, roundshierdip (+5) |
| `officerrus` | `drummerrus` | pikemanrus, strelet, grenadierdip, roundshierdip |
| `officertur` | `drummertur` | pikemantur, lightinfantry, archer, archertur, jannisary, grenadierdip, roundshierdip |
| `officer18` | `drummer18` | pikeman18, pikeman18swe, pandur, chasseur, highlander, musketeer18, musketeer18pru, grenadier (+11) |
| `officer18` | `bagpiper` | pikeman18, pikeman18swe, pandur, chasseur, highlander, musketeer18, musketeer18pru, grenadier (+7) |
| `officersco` | `bagpiper` | pikemansco, musketeersco, grenadierdip, roundshierdip |
| `serdiuk` | `serdiuk` | serdiuk |
| `archersco` | `archersco` | archersco |
| `swordsmansco` | `swordsmansco` | swordsmansco |

#### pru — Prussia (11 офицеров)

| officer | drummer | юниты в строю |
|---|---|---|
| `roundshierdip` | `roundshierdip` | roundshierdip |
| `grenadierdip` | `grenadierdip` | grenadierdip |
| `officer` | `drummer` | pikemanpol, roundshier, musketeer, musketeeraus, musketeerpol, musketeerspa, grenadierdip, roundshierdip (+5) |
| `officerrus` | `drummerrus` | pikemanrus, strelet, grenadierdip, roundshierdip |
| `officertur` | `drummertur` | pikemantur, lightinfantry, archer, archertur, jannisary, grenadierdip, roundshierdip |
| `officer18` | `drummer18` | pikeman18, pikeman18swe, pandur, chasseur, highlander, musketeer18, musketeer18pru, grenadier (+11) |
| `officer18` | `bagpiper` | pikeman18, pikeman18swe, pandur, chasseur, highlander, musketeer18, musketeer18pru, grenadier (+7) |
| `officersco` | `bagpiper` | pikemansco, musketeersco, grenadierdip, roundshierdip |
| `serdiuk` | `serdiuk` | serdiuk |
| `archersco` | `archersco` | archersco |
| `swordsmansco` | `swordsmansco` | swordsmansco |

#### ven — Venice (11 офицеров)

| officer | drummer | юниты в строю |
|---|---|---|
| `roundshierdip` | `roundshierdip` | roundshierdip |
| `grenadierdip` | `grenadierdip` | grenadierdip |
| `officer` | `drummer` | pikemanpol, roundshier, musketeer, musketeeraus, musketeerpol, musketeerspa, grenadierdip, roundshierdip (+5) |
| `officerrus` | `drummerrus` | pikemanrus, strelet, grenadierdip, roundshierdip |
| `officertur` | `drummertur` | pikemantur, lightinfantry, archer, archertur, jannisary, grenadierdip, roundshierdip |
| `officer18` | `drummer18` | pikeman18, pikeman18swe, pandur, chasseur, highlander, musketeer18, musketeer18pru, grenadier (+11) |
| `officer18` | `bagpiper` | pikeman18, pikeman18swe, pandur, chasseur, highlander, musketeer18, musketeer18pru, grenadier (+7) |
| `officersco` | `bagpiper` | pikemansco, musketeersco, grenadierdip, roundshierdip |
| `serdiuk` | `serdiuk` | serdiuk |
| `archersco` | `archersco` | archersco |
| `swordsmansco` | `swordsmansco` | swordsmansco |

#### tur — Turkey (11 офицеров)

| officer | drummer | юниты в строю |
|---|---|---|
| `roundshierdip` | `roundshierdip` | roundshierdip |
| `grenadierdip` | `grenadierdip` | grenadierdip |
| `officer` | `drummer` | pikemanpol, roundshier, musketeer, musketeeraus, musketeerpol, musketeerspa, grenadierdip, roundshierdip (+5) |
| `officerrus` | `drummerrus` | pikemanrus, strelet, grenadierdip, roundshierdip |
| `officertur` | `drummertur` | pikemantur, lightinfantry, archer, archertur, jannisary, grenadierdip, roundshierdip |
| `officer18` | `drummer18` | pikeman18, pikeman18swe, pandur, chasseur, highlander, musketeer18, musketeer18pru, grenadier (+11) |
| `officer18` | `bagpiper` | pikeman18, pikeman18swe, pandur, chasseur, highlander, musketeer18, musketeer18pru, grenadier (+7) |
| `officersco` | `bagpiper` | pikemansco, musketeersco, grenadierdip, roundshierdip |
| `serdiuk` | `serdiuk` | serdiuk |
| `archersco` | `archersco` | archersco |
| `swordsmansco` | `swordsmansco` | swordsmansco |

#### alg — Algeria (11 офицеров)

| officer | drummer | юниты в строю |
|---|---|---|
| `roundshierdip` | `roundshierdip` | roundshierdip |
| `grenadierdip` | `grenadierdip` | grenadierdip |
| `officer` | `drummer` | pikemanpol, roundshier, musketeer, musketeeraus, musketeerpol, musketeerspa, grenadierdip, roundshierdip (+5) |
| `officerrus` | `drummerrus` | pikemanrus, strelet, grenadierdip, roundshierdip |
| `officertur` | `drummertur` | pikemantur, lightinfantry, archer, archertur, jannisary, grenadierdip, roundshierdip |
| `officer18` | `drummer18` | pikeman18, pikeman18swe, pandur, chasseur, highlander, musketeer18, musketeer18pru, grenadier (+11) |
| `officer18` | `bagpiper` | pikeman18, pikeman18swe, pandur, chasseur, highlander, musketeer18, musketeer18pru, grenadier (+7) |
| `officersco` | `bagpiper` | pikemansco, musketeersco, grenadierdip, roundshierdip |
| `serdiuk` | `serdiuk` | serdiuk |
| `archersco` | `archersco` | archersco |
| `swordsmansco` | `swordsmansco` | swordsmansco |

#### net — Netherlands (11 офицеров)

| officer | drummer | юниты в строю |
|---|---|---|
| `roundshierdip` | `roundshierdip` | roundshierdip |
| `grenadierdip` | `grenadierdip` | grenadierdip |
| `officer` | `drummer` | pikemanpol, roundshier, musketeer, musketeeraus, musketeerpol, musketeerspa, grenadierdip, roundshierdip (+5) |
| `officerrus` | `drummerrus` | pikemanrus, strelet, grenadierdip, roundshierdip |
| `officertur` | `drummertur` | pikemantur, lightinfantry, archer, archertur, jannisary, grenadierdip, roundshierdip |
| `officer18` | `drummer18` | pikeman18, pikeman18swe, pandur, chasseur, highlander, musketeer18, musketeer18pru, grenadier (+11) |
| `officer18` | `bagpiper` | pikeman18, pikeman18swe, pandur, chasseur, highlander, musketeer18, musketeer18pru, grenadier (+7) |
| `officersco` | `bagpiper` | pikemansco, musketeersco, grenadierdip, roundshierdip |
| `serdiuk` | `serdiuk` | serdiuk |
| `archersco` | `archersco` | archersco |
| `swordsmansco` | `swordsmansco` | swordsmansco |

#### den — Denmark (11 офицеров)

| officer | drummer | юниты в строю |
|---|---|---|
| `roundshierdip` | `roundshierdip` | roundshierdip |
| `grenadierdip` | `grenadierdip` | grenadierdip |
| `officer` | `drummer` | pikemanpol, roundshier, musketeer, musketeeraus, musketeerpol, musketeerspa, grenadierdip, roundshierdip (+5) |
| `officerrus` | `drummerrus` | pikemanrus, strelet, grenadierdip, roundshierdip |
| `officertur` | `drummertur` | pikemantur, lightinfantry, archer, archertur, jannisary, grenadierdip, roundshierdip |
| `officer18` | `drummer18` | pikeman18, pikeman18swe, pandur, chasseur, highlander, musketeer18, musketeer18pru, grenadier (+11) |
| `officer18` | `bagpiper` | pikeman18, pikeman18swe, pandur, chasseur, highlander, musketeer18, musketeer18pru, grenadier (+7) |
| `officersco` | `bagpiper` | pikemansco, musketeersco, grenadierdip, roundshierdip |
| `serdiuk` | `serdiuk` | serdiuk |
| `archersco` | `archersco` | archersco |
| `swordsmansco` | `swordsmansco` | swordsmansco |

#### por — Portugal (11 офицеров)

| officer | drummer | юниты в строю |
|---|---|---|
| `roundshierdip` | `roundshierdip` | roundshierdip |
| `grenadierdip` | `grenadierdip` | grenadierdip |
| `officer` | `drummer` | pikemanpol, roundshier, musketeer, musketeeraus, musketeerpol, musketeerspa, grenadierdip, roundshierdip (+5) |
| `officerrus` | `drummerrus` | pikemanrus, strelet, grenadierdip, roundshierdip |
| `officertur` | `drummertur` | pikemantur, lightinfantry, archer, archertur, jannisary, grenadierdip, roundshierdip |
| `officer18` | `drummer18` | pikeman18, pikeman18swe, pandur, chasseur, highlander, musketeer18, musketeer18pru, grenadier (+11) |
| `officer18` | `bagpiper` | pikeman18, pikeman18swe, pandur, chasseur, highlander, musketeer18, musketeer18pru, grenadier (+7) |
| `officersco` | `bagpiper` | pikemansco, musketeersco, grenadierdip, roundshierdip |
| `serdiuk` | `serdiuk` | serdiuk |
| `archersco` | `archersco` | archersco |
| `swordsmansco` | `swordsmansco` | swordsmansco |

#### pie — Piedmont (11 офицеров)

| officer | drummer | юниты в строю |
|---|---|---|
| `roundshierdip` | `roundshierdip` | roundshierdip |
| `grenadierdip` | `grenadierdip` | grenadierdip |
| `officer` | `drummer` | pikemanpol, roundshier, musketeer, musketeeraus, musketeerpol, musketeerspa, grenadierdip, roundshierdip (+5) |
| `officerrus` | `drummerrus` | pikemanrus, strelet, grenadierdip, roundshierdip |
| `officertur` | `drummertur` | pikemantur, lightinfantry, archer, archertur, jannisary, grenadierdip, roundshierdip |
| `officer18` | `drummer18` | pikeman18, pikeman18swe, pandur, chasseur, highlander, musketeer18, musketeer18pru, grenadier (+11) |
| `officer18` | `bagpiper` | pikeman18, pikeman18swe, pandur, chasseur, highlander, musketeer18, musketeer18pru, grenadier (+7) |
| `officersco` | `bagpiper` | pikemansco, musketeersco, grenadierdip, roundshierdip |
| `serdiuk` | `serdiuk` | serdiuk |
| `archersco` | `archersco` | archersco |
| `swordsmansco` | `swordsmansco` | swordsmansco |

#### sax — Saxony (11 офицеров)

| officer | drummer | юниты в строю |
|---|---|---|
| `roundshierdip` | `roundshierdip` | roundshierdip |
| `grenadierdip` | `grenadierdip` | grenadierdip |
| `officer` | `drummer` | pikemanpol, roundshier, musketeer, musketeeraus, musketeerpol, musketeerspa, grenadierdip, roundshierdip (+5) |
| `officerrus` | `drummerrus` | pikemanrus, strelet, grenadierdip, roundshierdip |
| `officertur` | `drummertur` | pikemantur, lightinfantry, archer, archertur, jannisary, grenadierdip, roundshierdip |
| `officer18` | `drummer18` | pikeman18, pikeman18swe, pandur, chasseur, highlander, musketeer18, musketeer18pru, grenadier (+11) |
| `officer18` | `bagpiper` | pikeman18, pikeman18swe, pandur, chasseur, highlander, musketeer18, musketeer18pru, grenadier (+7) |
| `officersco` | `bagpiper` | pikemansco, musketeersco, grenadierdip, roundshierdip |
| `serdiuk` | `serdiuk` | serdiuk |
| `archersco` | `archersco` | archersco |
| `swordsmansco` | `swordsmansco` | swordsmansco |

#### bav — Bavaria (11 офицеров)

| officer | drummer | юниты в строю |
|---|---|---|
| `roundshierdip` | `roundshierdip` | roundshierdip |
| `grenadierdip` | `grenadierdip` | grenadierdip |
| `officer` | `drummer` | pikemanpol, roundshier, musketeer, musketeeraus, musketeerpol, musketeerspa, grenadierdip, roundshierdip (+5) |
| `officerrus` | `drummerrus` | pikemanrus, strelet, grenadierdip, roundshierdip |
| `officertur` | `drummertur` | pikemantur, lightinfantry, archer, archertur, jannisary, grenadierdip, roundshierdip |
| `officer18` | `drummer18` | pikeman18, pikeman18swe, pandur, chasseur, highlander, musketeer18, musketeer18pru, grenadier (+11) |
| `officer18` | `bagpiper` | pikeman18, pikeman18swe, pandur, chasseur, highlander, musketeer18, musketeer18pru, grenadier (+7) |
| `officersco` | `bagpiper` | pikemansco, musketeersco, grenadierdip, roundshierdip |
| `serdiuk` | `serdiuk` | serdiuk |
| `archersco` | `archersco` | archersco |
| `swordsmansco` | `swordsmansco` | swordsmansco |

#### hun — Hungary (11 офицеров)

| officer | drummer | юниты в строю |
|---|---|---|
| `roundshierdip` | `roundshierdip` | roundshierdip |
| `grenadierdip` | `grenadierdip` | grenadierdip |
| `officer` | `drummer` | pikemanpol, roundshier, musketeer, musketeeraus, musketeerpol, musketeerspa, grenadierdip, roundshierdip (+5) |
| `officerrus` | `drummerrus` | pikemanrus, strelet, grenadierdip, roundshierdip |
| `officertur` | `drummertur` | pikemantur, lightinfantry, archer, archertur, jannisary, grenadierdip, roundshierdip |
| `officer18` | `drummer18` | pikeman18, pikeman18swe, pandur, chasseur, highlander, musketeer18, musketeer18pru, grenadier (+11) |
| `officer18` | `bagpiper` | pikeman18, pikeman18swe, pandur, chasseur, highlander, musketeer18, musketeer18pru, grenadier (+7) |
| `officersco` | `bagpiper` | pikemansco, musketeersco, grenadierdip, roundshierdip |
| `serdiuk` | `serdiuk` | serdiuk |
| `archersco` | `archersco` | archersco |
| `swordsmansco` | `swordsmansco` | swordsmansco |

#### swi — Switzerland (11 офицеров)

| officer | drummer | юниты в строю |
|---|---|---|
| `roundshierdip` | `roundshierdip` | roundshierdip |
| `grenadierdip` | `grenadierdip` | grenadierdip |
| `officer` | `drummer` | pikemanpol, roundshier, musketeer, musketeeraus, musketeerpol, musketeerspa, grenadierdip, roundshierdip (+5) |
| `officerrus` | `drummerrus` | pikemanrus, strelet, grenadierdip, roundshierdip |
| `officertur` | `drummertur` | pikemantur, lightinfantry, archer, archertur, jannisary, grenadierdip, roundshierdip |
| `officer18` | `drummer18` | pikeman18, pikeman18swe, pandur, chasseur, highlander, musketeer18, musketeer18pru, grenadier (+11) |
| `officer18` | `bagpiper` | pikeman18, pikeman18swe, pandur, chasseur, highlander, musketeer18, musketeer18pru, grenadier (+7) |
| `officersco` | `bagpiper` | pikemansco, musketeersco, grenadierdip, roundshierdip |
| `serdiuk` | `serdiuk` | serdiuk |
| `archersco` | `archersco` | archersco |
| `swordsmansco` | `swordsmansco` | swordsmansco |

#### sco — Scotland (11 офицеров)

| officer | drummer | юниты в строю |
|---|---|---|
| `roundshierdip` | `roundshierdip` | roundshierdip |
| `grenadierdip` | `grenadierdip` | grenadierdip |
| `officer` | `drummer` | pikemanpol, roundshier, musketeer, musketeeraus, musketeerpol, musketeerspa, grenadierdip, roundshierdip (+5) |
| `officerrus` | `drummerrus` | pikemanrus, strelet, grenadierdip, roundshierdip |
| `officertur` | `drummertur` | pikemantur, lightinfantry, archer, archertur, jannisary, grenadierdip, roundshierdip |
| `officer18` | `drummer18` | pikeman18, pikeman18swe, pandur, chasseur, highlander, musketeer18, musketeer18pru, grenadier (+11) |
| `officer18` | `bagpiper` | pikeman18, pikeman18swe, pandur, chasseur, highlander, musketeer18, musketeer18pru, grenadier (+7) |
| `officersco` | `bagpiper` | pikemansco, musketeersco, grenadierdip, roundshierdip |
| `serdiuk` | `serdiuk` | serdiuk |
| `archersco` | `archersco` | archersco |
| `swordsmansco` | `swordsmansco` | swordsmansco |

## 6d. Рынок — обменные курсы

Рынок (`mar` building) позволяет менять ресурсы. Формула обмена использует **buy** и **sell** цены каждого ресурса. После сделки цены **сдвигаются**: `buycost` растёт к `buycostmax`, `sellcost` падает к `sellcostmin`. Поэтому повторные продажи одного и того же ресурса дают всё меньше.

> **Полная статья по рынку:** [`reference/06_market.md`](reference/06_market.md) — global rates, first-mover advantage, формулы пересчёта, численные примеры.

**Default ratio:** при стандартных ценах `received_Y = sold_X × sellcost[X] / buycost[Y]`.

| Ресурс | buy_min | buy_def | buy_max | sell_min | sell_def | sell_max |
|---|---:|---:|---:|---:|---:|---:|
| food | 20 | 25.00 | 40 | 10.64 | 15.20 | 19.76 |
| wood | 40 | 50.00 | 60 | 20.00 | 30.00 | 40.00 |
| stone | 40 | 50.00 | 60 | 15.68 | 20.90 | 26.13 |
| gold | 140 | 190.00 | 240 | 80.00 | 110.00 | 140.00 |
| iron | 100 | 140.00 | 180 | 40.00 | 60.00 | 80.00 |
| coal | 100 | 140.00 | 180 | 40.00 | 60.00 | 80.00 |

**Пример обмена при default-ценах:**

- Sell 100 food (sellcost ≈ 15.20) → получишь `100 × 15.20 / 50 = 30.4` wood.
- Sell 100 gold (sellcost = 110) → получишь `100 × 110 / 50 = 220` wood.
- Sell 100 iron (sellcost = 60) → получишь `100 × 60 / 25 = 240` food.

Источник: `res.script:_res_InitEconomy` (стр. 178-249), `res.script:_res_MarketTradeResources` (стр. 320-344). `gc_economy_exp = 0.00002` контролирует скорость деградации курса.

### Стоимость одного выстрела (только для юнитов / зданий с `weapon.cost`)

| sid | nation | weapon | dmg | reload (s) | shots/min | iron/выстрел | coal/выстрел | gold/выстрел |
|---|---|---|---:|---:|---:|---:|---:|---:|
| `archer` | alg | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerdip` | alg | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerdip` | aus | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerdip` | bav | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerdip` | den | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerdip` | eng | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerdip` | fra | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerdip` | hun | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerdip` | net | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerdip` | pie | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerdip` | pol | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerdip` | por | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerdip` | pru | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerdip` | rus | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerdip` | sax | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerdip` | sco | `OSTRELA` | 150 | 4.38 | 13.7 | — | — | — |
| `archerdip` | spa | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerdip` | swe | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerdip` | swi | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerdip` | tur | `OSTRELA` | 150 | 4.38 | 13.7 | — | — | — |
| `archerdip` | ukr | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerdip` | ven | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archersco` | sco | `OSTRELA` | 150 | 4.38 | 13.7 | — | — | — |
| `archertur` | tur | `OSTRELA` | 150 | 4.38 | 13.7 | — | — | — |
| `archerturdip` | alg | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerturdip` | aus | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerturdip` | bav | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerturdip` | den | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerturdip` | eng | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerturdip` | fra | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerturdip` | hun | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerturdip` | net | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerturdip` | pie | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerturdip` | pol | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerturdip` | por | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerturdip` | pru | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerturdip` | rus | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerturdip` | sax | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerturdip` | sco | `OSTRELA` | 150 | 4.38 | 13.7 | — | — | — |
| `archerturdip` | spa | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerturdip` | swe | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerturdip` | swi | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerturdip` | tur | `OSTRELA` | 150 | 4.38 | 13.7 | — | — | — |
| `archerturdip` | ukr | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerturdip` | ven | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `battleship` | alg | `PPOINTTKOR` | 1800 | 0.62 | 96.8 | 5 | 15 | — |
| `battleship` | aus | `PPOINTTKOR` | 1800 | 0.62 | 96.8 | 5 | 15 | — |
| `battleship` | bav | `PPOINTTKOR` | 1800 | 0.62 | 96.8 | 5 | 15 | — |
| `battleship` | den | `PPOINTTKOR` | 1800 | 0.62 | 96.8 | 5 | 15 | — |
| `battleship` | eng | `PPOINTTKOR` | 1800 | 0.62 | 96.8 | 5 | 15 | — |
| `battleship` | fra | `PPOINTTKOR` | 1800 | 0.62 | 96.8 | 5 | 15 | — |
| `battleship` | hun | `PPOINTTKOR` | 1800 | 0.62 | 96.8 | 5 | 15 | — |
| `battleship` | net | `PPOINTTKOR` | 1800 | 0.62 | 96.8 | 5 | 15 | — |
| `battleship` | pie | `PPOINTTKOR` | 1800 | 0.62 | 96.8 | 5 | 15 | — |
| `battleship` | pol | `PPOINTTKOR` | 1800 | 0.62 | 96.8 | 5 | 15 | — |
| `battleship` | por | `PPOINTTKOR` | 1800 | 0.62 | 96.8 | 5 | 15 | — |
| `battleship` | pru | `PPOINTTKOR` | 1800 | 0.62 | 96.8 | 5 | 15 | — |
| `battleship` | rus | `PPOINTTKOR` | 1800 | 0.62 | 96.8 | 5 | 15 | — |
| `battleship` | sax | `PPOINTTKOR` | 1800 | 0.62 | 96.8 | 5 | 15 | — |
| `battleship` | sco | `PPOINTTKOR` | 1800 | 0.62 | 96.8 | 5 | 15 | — |
| `battleship` | spa | `PPOINTTKOR` | 1800 | 0.62 | 96.8 | 5 | 15 | — |
| `battleship` | swe | `PPOINTTKOR` | 1800 | 0.62 | 96.8 | 5 | 15 | — |
| `battleship` | swi | `PPOINTTKOR` | 1800 | 0.62 | 96.8 | 5 | 15 | — |
| `battleship` | tur | `PPOINTTKOR` | 1800 | 0.62 | 96.8 | 5 | 15 | — |
| `battleship` | ven | `PPOINTTKOR` | 1800 | 0.62 | 96.8 | 5 | 15 | — |
| `cannon` | alg | `PPOINTT` | 1800 | 10.94 | 5.5 | 20 | 40 | — |
| `cannon` | aus | `PPOINTT` | 1800 | 10.94 | 5.5 | 20 | 40 | — |
| `cannon` | bav | `PPOINTT` | 1800 | 10.94 | 5.5 | 20 | 40 | — |
| `cannon` | den | `PPOINTT` | 1800 | 10.94 | 5.5 | 20 | 40 | — |
| `cannon` | eng | `PPOINTT` | 1800 | 10.94 | 5.5 | 20 | 40 | — |
| `cannon` | fra | `PPOINTT` | 1800 | 10.94 | 5.5 | 20 | 40 | — |
| `cannon` | hun | `PPOINTT` | 1800 | 10.94 | 5.5 | 20 | 40 | — |
| `cannon` | net | `PPOINTT` | 1800 | 10.94 | 5.5 | 20 | 40 | — |
| `cannon` | pie | `PPOINTT` | 1800 | 10.94 | 5.5 | 20 | 40 | — |
| `cannon` | pol | `PPOINTT` | 1800 | 10.94 | 5.5 | 20 | 40 | — |
| `cannon` | por | `PPOINTT` | 1800 | 10.94 | 5.5 | 20 | 40 | — |
| `cannon` | pru | `PPOINTT` | 1800 | 10.94 | 5.5 | 20 | 40 | — |
| `cannon` | rus | `PPOINTT` | 1800 | 10.94 | 5.5 | 20 | 40 | — |
| `cannon` | sax | `PPOINTT` | 1800 | 10.94 | 5.5 | 20 | 40 | — |
| `cannon` | sco | `PPOINTT` | 1800 | 10.94 | 5.5 | 20 | 40 | — |
| `cannon` | spa | `PPOINTT` | 1800 | 10.94 | 5.5 | 20 | 40 | — |
| `cannon` | swe | `PPOINTT` | 1800 | 10.94 | 5.5 | 20 | 40 | — |
| `cannon` | swi | `PPOINTT` | 1800 | 10.94 | 5.5 | 20 | 40 | — |
| `cannon` | tur | `PPOINTT` | 1800 | 10.94 | 5.5 | 20 | 40 | — |
| `cannon` | ukr | `PPOINTT` | 1800 | 10.94 | 5.5 | 20 | 40 | — |
| `cannon` | ven | `PPOINTT` | 1800 | 10.94 | 5.5 | 20 | 40 | — |
| `chaika` | ukr | `PPOINTTKOR` | 1000 | 2.34 | 25.6 | 4 | 9 | — |
| `chasseur` | fra | `SHOTMUSKET` | 20 | 5.94 | 10.1 | 4 | 8 | — |
| `dragoon` | aus | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon` | bav | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon` | den | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon` | eng | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon` | fra | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon` | hun | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon` | net | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon` | pie | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon` | pol | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon` | por | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon` | pru | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon` | sax | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon` | spa | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon` | swe | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon` | swi | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon` | ven | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon18` | aus | `SHOTMUSKET` | 19 | 5.31 | 11.3 | 4 | 5 | — |
| `dragoon18` | bav | `SHOTMUSKET` | 19 | 5.31 | 11.3 | 4 | 5 | — |
| `dragoon18` | den | `SHOTMUSKET` | 19 | 5.31 | 11.3 | 4 | 5 | — |
| `dragoon18` | eng | `SHOTMUSKET` | 19 | 5.31 | 11.3 | 4 | 5 | — |
| `dragoon18` | pol | `SHOTMUSKET` | 19 | 5.31 | 11.3 | 4 | 5 | — |
| `dragoon18` | por | `SHOTMUSKET` | 19 | 5.31 | 11.3 | 4 | 5 | — |
| `dragoon18` | pru | `SHOTMUSKET` | 19 | 5.31 | 11.3 | 4 | 5 | — |
| `dragoon18` | rus | `SHOTMUSKET` | 19 | 5.31 | 11.3 | 4 | 5 | — |
| `dragoon18` | sax | `SHOTMUSKET` | 19 | 5.31 | 11.3 | 4 | 5 | — |
| `dragoon18` | spa | `SHOTMUSKET` | 19 | 5.31 | 11.3 | 4 | 5 | — |
| `dragoon18` | swe | `SHOTMUSKET` | 19 | 5.31 | 11.3 | 4 | 5 | — |
| `dragoon18` | swi | `SHOTMUSKET` | 19 | 5.31 | 11.3 | 4 | 5 | — |
| `dragoon18` | ven | `SHOTMUSKET` | 19 | 5.31 | 11.3 | 4 | 5 | — |
| `dragoon18dip` | alg | `SHOTMUSKET` | 19 | 5.31 | 11.3 | 4 | 5 | — |
| `dragoon18dip` | aus | `SHOTMUSKET` | 19 | 5.31 | 11.3 | 4 | 5 | — |
| `dragoon18dip` | bav | `SHOTMUSKET` | 19 | 5.31 | 11.3 | 4 | 5 | — |
| `dragoon18dip` | den | `SHOTMUSKET` | 19 | 5.31 | 11.3 | 4 | 5 | — |
| `dragoon18dip` | eng | `SHOTMUSKET` | 19 | 5.31 | 11.3 | 4 | 5 | — |
| `dragoon18dip` | fra | `SHOTMUSKET` | 19 | 5.31 | 11.3 | 4 | 5 | — |
| `dragoon18dip` | hun | `SHOTMUSKET` | 19 | 5.31 | 11.3 | 4 | 5 | — |
| `dragoon18dip` | net | `SHOTMUSKET` | 19 | 5.31 | 11.3 | 4 | 5 | — |
| `dragoon18dip` | pie | `SHOTMUSKET` | 19 | 5.31 | 11.3 | 4 | 5 | — |
| `dragoon18dip` | pol | `SHOTMUSKET` | 19 | 5.31 | 11.3 | 4 | 5 | — |
| `dragoon18dip` | por | `SHOTMUSKET` | 19 | 5.31 | 11.3 | 4 | 5 | — |
| `dragoon18dip` | pru | `SHOTMUSKET` | 19 | 5.31 | 11.3 | 4 | 5 | — |
| `dragoon18dip` | rus | `SHOTMUSKET` | 19 | 5.31 | 11.3 | 4 | 5 | — |
| `dragoon18dip` | sax | `SHOTMUSKET` | 19 | 5.31 | 11.3 | 4 | 5 | — |
| `dragoon18dip` | sco | `SHOTMUSKET` | 19 | 5.31 | 11.3 | 4 | 5 | — |
| `dragoon18dip` | spa | `SHOTMUSKET` | 19 | 5.31 | 11.3 | 4 | 5 | — |
| `dragoon18dip` | swe | `SHOTMUSKET` | 19 | 5.31 | 11.3 | 4 | 5 | — |
| `dragoon18dip` | swi | `SHOTMUSKET` | 19 | 5.31 | 11.3 | 4 | 5 | — |
| `dragoon18dip` | tur | `SHOTMUSKET` | 19 | 5.31 | 11.3 | 4 | 5 | — |
| `dragoon18dip` | ukr | `SHOTMUSKET` | 19 | 5.31 | 11.3 | 4 | 5 | — |
| `dragoon18dip` | ven | `SHOTMUSKET` | 19 | 5.31 | 11.3 | 4 | 5 | — |
| `dragoon18fra` | fra | `SHOTMUSKET` | 10 | 4.69 | 12.8 | 3 | 3 | — |
| `dragoon18net` | net | `SHOTMUSKET` | 17 | 5.0 | 12.0 | 3 | 4 | — |
| `dragoon18pie` | pie | `SHOTMUSKET` | 19 | 5.0 | 12.0 | 4 | 5 | — |
| `dragoonpol` | pol | `SHOTMUSKET` | 13 | 5.0 | 12.0 | 2 | 3 | — |
| `eurtow` | aus | `cannonball` | 1000 | 12.5 | 4.8 | 10 | 30 | — |
| `eurtow` | bav | `cannonball` | 1000 | 12.5 | 4.8 | 10 | 30 | — |
| `eurtow` | den | `cannonball` | 1000 | 12.5 | 4.8 | 10 | 30 | — |
| `eurtow` | eng | `cannonball` | 1000 | 12.5 | 4.8 | 10 | 30 | — |
| `eurtow` | fra | `cannonball` | 1000 | 12.5 | 4.8 | 10 | 30 | — |
| `eurtow` | hun | `cannonball` | 1000 | 12.5 | 4.8 | 10 | 30 | — |
| `eurtow` | net | `cannonball` | 1000 | 12.5 | 4.8 | 10 | 30 | — |
| `eurtow` | pie | `cannonball` | 1000 | 12.5 | 4.8 | 10 | 30 | — |
| `eurtow` | pol | `cannonball` | 1000 | 12.5 | 4.8 | 10 | 30 | — |
| `eurtow` | por | `cannonball` | 1000 | 12.5 | 4.8 | 10 | 30 | — |
| `eurtow` | pru | `cannonball` | 1000 | 12.5 | 4.8 | 10 | 30 | — |
| `eurtow` | sax | `cannonball` | 1000 | 12.5 | 4.8 | 10 | 30 | — |
| `eurtow` | sco | `cannonball` | 1000 | 12.5 | 4.8 | 10 | 30 | — |
| `eurtow` | spa | `cannonball` | 1000 | 12.5 | 4.8 | 10 | 30 | — |
| `eurtow` | swe | `cannonball` | 1000 | 12.5 | 4.8 | 10 | 30 | — |
| `eurtow` | swi | `cannonball` | 1000 | 12.5 | 4.8 | 10 | 30 | — |
| `eurtow` | ven | `cannonball` | 1000 | 12.5 | 4.8 | 10 | 30 | — |
| `framegun` | sco | `PPOINTTFRAME` | 500 | 2.81 | 21.4 | 30 | 40 | — |
| `frigate` | aus | `PPOINTTKOR` | 1800 | 2.34 | 25.6 | 25 | 35 | — |
| `frigate` | bav | `PPOINTTKOR` | 1800 | 2.34 | 25.6 | 25 | 35 | — |
| `frigate` | den | `PPOINTTKOR` | 1800 | 2.34 | 25.6 | 25 | 35 | — |
| `frigate` | eng | `PPOINTTKOR` | 1800 | 2.34 | 25.6 | 25 | 35 | — |
| `frigate` | fra | `PPOINTTKOR` | 1800 | 2.34 | 25.6 | 25 | 35 | — |
| `frigate` | hun | `PPOINTTKOR` | 1800 | 2.34 | 25.6 | 25 | 35 | — |
| `frigate` | net | `PPOINTTKOR` | 1800 | 2.34 | 25.6 | 25 | 35 | — |
| `frigate` | pie | `PPOINTTKOR` | 1800 | 2.34 | 25.6 | 25 | 35 | — |
| `frigate` | pol | `PPOINTTKOR` | 1800 | 2.34 | 25.6 | 25 | 35 | — |
| `frigate` | por | `PPOINTTKOR` | 1800 | 2.34 | 25.6 | 25 | 35 | — |
| `frigate` | pru | `PPOINTTKOR` | 1800 | 2.34 | 25.6 | 25 | 35 | — |
| `frigate` | rus | `PPOINTTKOR` | 1800 | 2.34 | 25.6 | 25 | 35 | — |
| `frigate` | sax | `PPOINTTKOR` | 1800 | 2.34 | 25.6 | 25 | 35 | — |
| `frigate` | sco | `PPOINTTKOR` | 1800 | 2.34 | 25.6 | 25 | 35 | — |
| `frigate` | spa | `PPOINTTKOR` | 1800 | 2.34 | 25.6 | 25 | 35 | — |
| `frigate` | swe | `PPOINTTKOR` | 1800 | 2.34 | 25.6 | 25 | 35 | — |
| `frigate` | swi | `PPOINTTKOR` | 1800 | 2.34 | 25.6 | 25 | 35 | — |
| `frigate` | ven | `PPOINTTKOR` | 1800 | 2.34 | 25.6 | 25 | 35 | — |
| `galley` | alg | `DIMMORT2KOR` | 1000 | 1.56 | 38.5 | 4 | 9 | — |
| `galley` | aus | `DIMMORT2KOR` | 1000 | 1.56 | 38.5 | 4 | 9 | — |
| `galley` | bav | `DIMMORT2KOR` | 1000 | 1.56 | 38.5 | 4 | 9 | — |
| `galley` | den | `DIMMORT2KOR` | 1000 | 1.56 | 38.5 | 4 | 9 | — |
| `galley` | eng | `DIMMORT2KOR` | 1000 | 1.56 | 38.5 | 4 | 9 | — |
| `galley` | fra | `DIMMORT2KOR` | 1000 | 1.56 | 38.5 | 4 | 9 | — |
| `galley` | hun | `DIMMORT2KOR` | 1000 | 1.56 | 38.5 | 4 | 9 | — |
| `galley` | net | `DIMMORT2KOR` | 1000 | 1.56 | 38.5 | 4 | 9 | — |
| `galley` | pie | `DIMMORT2KOR` | 1000 | 1.56 | 38.5 | 4 | 9 | — |
| `galley` | pol | `DIMMORT2KOR` | 1000 | 1.56 | 38.5 | 4 | 9 | — |
| `galley` | por | `DIMMORT2KOR` | 1000 | 1.56 | 38.5 | 4 | 9 | — |
| `galley` | pru | `DIMMORT2KOR` | 1000 | 1.56 | 38.5 | 4 | 9 | — |
| `galley` | rus | `DIMMORT2KOR` | 1000 | 1.56 | 38.5 | 4 | 9 | — |
| `galley` | sax | `DIMMORT2KOR` | 1000 | 1.56 | 38.5 | 4 | 9 | — |
| `galley` | spa | `DIMMORT2KOR` | 1000 | 1.56 | 38.5 | 4 | 9 | — |
| `galley` | swe | `DIMMORT2KOR` | 1000 | 1.56 | 38.5 | 4 | 9 | — |
| `galley` | swi | `DIMMORT2KOR` | 1000 | 1.56 | 38.5 | 4 | 9 | — |
| `galley` | tur | `DIMMORT2KOR` | 1000 | 1.56 | 38.5 | 4 | 9 | — |
| `galley` | ukr | `DIMMORT2KOR` | 1000 | 1.56 | 38.5 | 4 | 9 | — |
| `galley` | ven | `DIMMORT2KOR` | 1000 | 1.56 | 38.5 | 4 | 9 | — |
| `gauduk` | hun | `SHOTMUSKET` | 9 | 3.12 | 19.2 | 1 | 2 | — |
| `grenadier` | aus | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadier` | eng | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadier` | fra | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadier` | net | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadier` | pie | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadier` | pol | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadier` | por | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadier` | pru | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadier` | rus | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadier` | spa | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadier` | swe | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadier` | swi | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadier` | ven | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadierbav` | bav | `SHOTMUSKET` | 19 | 5.31 | 11.3 | 3 | 3 | — |
| `grenadierden` | den | `SHOTMUSKET` | 19 | 5.94 | 10.1 | 3 | 3 | — |
| `grenadierdip` | alg | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadierdip` | aus | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadierdip` | bav | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadierdip` | den | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadierdip` | eng | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadierdip` | fra | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadierdip` | hun | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadierdip` | net | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadierdip` | pie | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadierdip` | pol | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadierdip` | por | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadierdip` | pru | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadierdip` | rus | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadierdip` | sax | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadierdip` | sco | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadierdip` | spa | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadierdip` | swe | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadierdip` | swi | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadierdip` | tur | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadierdip` | ukr | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadierdip` | ven | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadierhun` | hun | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadierpru` | pru | `SHOTMUSKET` | 16 | 4.38 | 13.7 | 2 | 3 | — |
| `grenadiersax` | sax | `SHOTMUSKET` | 19 | 5.31 | 11.3 | 3 | 3 | — |
| `highlander` | eng | `SHOTMUSKET` | 16 | 5.0 | 12.0 | 3 | 4 | — |
| `howitzer` | alg | `DIMMORT1` | 4000 | 18.75 | 3.2 | 20 | 100 | — |
| `howitzer` | aus | `DIMMORT1` | 4000 | 18.75 | 3.2 | 20 | 100 | — |
| `howitzer` | bav | `DIMMORT1` | 4000 | 18.75 | 3.2 | 20 | 100 | — |
| `howitzer` | den | `DIMMORT1` | 4000 | 18.75 | 3.2 | 20 | 100 | — |
| `howitzer` | eng | `DIMMORT1` | 4000 | 18.75 | 3.2 | 20 | 100 | — |
| `howitzer` | fra | `DIMMORT1` | 4000 | 18.75 | 3.2 | 20 | 100 | — |
| `howitzer` | hun | `DIMMORT1` | 4000 | 18.75 | 3.2 | 20 | 100 | — |
| `howitzer` | net | `DIMMORT1` | 4000 | 18.75 | 3.2 | 20 | 100 | — |
| `howitzer` | pie | `DIMMORT1` | 4000 | 18.75 | 3.2 | 20 | 100 | — |
| `howitzer` | pol | `DIMMORT1` | 4000 | 18.75 | 3.2 | 20 | 100 | — |
| `howitzer` | por | `DIMMORT1` | 4000 | 18.75 | 3.2 | 20 | 100 | — |
| `howitzer` | pru | `DIMMORT1` | 4000 | 18.75 | 3.2 | 20 | 100 | — |
| `howitzer` | rus | `DIMMORT1` | 4000 | 18.75 | 3.2 | 20 | 100 | — |
| `howitzer` | sax | `DIMMORT1` | 4000 | 18.75 | 3.2 | 20 | 100 | — |
| `howitzer` | sco | `DIMMORT1` | 4000 | 18.75 | 3.2 | 20 | 100 | — |
| `howitzer` | spa | `DIMMORT1` | 4000 | 18.75 | 3.2 | 20 | 100 | — |
| `howitzer` | swe | `DIMMORT1` | 4000 | 18.75 | 3.2 | 20 | 100 | — |
| `howitzer` | swi | `DIMMORT1` | 4000 | 18.75 | 3.2 | 20 | 100 | — |
| `howitzer` | tur | `DIMMORT1` | 4000 | 18.75 | 3.2 | 20 | 100 | — |
| `howitzer` | ukr | `DIMMORT1` | 4000 | 18.75 | 3.2 | 20 | 100 | — |
| `howitzer` | ven | `DIMMORT1` | 4000 | 18.75 | 3.2 | 20 | 100 | — |
| `jagerpor` | por | `SHOTMUSKET` | 10 | 5.94 | 10.1 | 2 | 4 | — |
| `jagerswi` | swi | `SHOTMUSKET` | 20 | 6.88 | 8.7 | 4 | 9 | — |
| `jannisary` | tur | `SHOTMUSKET` | 12 | 4.69 | 12.8 | 3 | 5 | — |
| `kingmusketeer` | fra | `SHOTMUSKET` | 43 | 6.88 | 8.7 | 6 | 10 | — |
| `lightcavalry` | hun | `SHOTMUSKET` | 14 | 5.31 | 11.3 | 2 | 3 | — |
| `lightcavalrydip` | alg | `SHOTMUSKET` | 19 | 5.31 | 11.3 | 4 | 5 | — |
| `lightcavalrydip` | aus | `SHOTMUSKET` | 19 | 5.31 | 11.3 | 4 | 5 | — |
| `lightcavalrydip` | bav | `SHOTMUSKET` | 19 | 5.31 | 11.3 | 4 | 5 | — |
| `lightcavalrydip` | den | `SHOTMUSKET` | 19 | 5.31 | 11.3 | 4 | 5 | — |
| `lightcavalrydip` | eng | `SHOTMUSKET` | 19 | 5.31 | 11.3 | 4 | 5 | — |
| `lightcavalrydip` | fra | `SHOTMUSKET` | 19 | 5.31 | 11.3 | 4 | 5 | — |
| `lightcavalrydip` | hun | `SHOTMUSKET` | 19 | 5.31 | 11.3 | 4 | 5 | — |
| `lightcavalrydip` | net | `SHOTMUSKET` | 19 | 5.31 | 11.3 | 4 | 5 | — |
| `lightcavalrydip` | pie | `SHOTMUSKET` | 19 | 5.31 | 11.3 | 4 | 5 | — |
| `lightcavalrydip` | pol | `SHOTMUSKET` | 19 | 5.31 | 11.3 | 4 | 5 | — |
| `lightcavalrydip` | por | `SHOTMUSKET` | 19 | 5.31 | 11.3 | 4 | 5 | — |
| `lightcavalrydip` | pru | `SHOTMUSKET` | 19 | 5.31 | 11.3 | 4 | 5 | — |
| `lightcavalrydip` | rus | `SHOTMUSKET` | 19 | 5.31 | 11.3 | 4 | 5 | — |
| `lightcavalrydip` | sax | `SHOTMUSKET` | 19 | 5.31 | 11.3 | 4 | 5 | — |
| `lightcavalrydip` | sco | `SHOTMUSKET` | 19 | 5.31 | 11.3 | 4 | 5 | — |
| `lightcavalrydip` | spa | `SHOTMUSKET` | 19 | 5.31 | 11.3 | 4 | 5 | — |
| `lightcavalrydip` | swe | `SHOTMUSKET` | 19 | 5.31 | 11.3 | 4 | 5 | — |
| `lightcavalrydip` | swi | `SHOTMUSKET` | 19 | 5.31 | 11.3 | 4 | 5 | — |
| `lightcavalrydip` | tur | `SHOTMUSKET` | 19 | 5.31 | 11.3 | 4 | 5 | — |
| `lightcavalrydip` | ukr | `SHOTMUSKET` | 19 | 5.31 | 11.3 | 4 | 5 | — |
| `lightcavalrydip` | ven | `SHOTMUSKET` | 19 | 5.31 | 11.3 | 4 | 5 | — |
| `mortar` | alg | `DIMMORT2` | 200 | 7.81 | 7.7 | 20 | 30 | — |
| `mortar` | aus | `DIMMORT2` | 200 | 7.81 | 7.7 | 20 | 30 | — |
| `mortar` | bav | `DIMMORT2` | 200 | 7.81 | 7.7 | 20 | 30 | — |
| `mortar` | den | `DIMMORT2` | 200 | 7.81 | 7.7 | 20 | 30 | — |
| `mortar` | eng | `DIMMORT2` | 200 | 7.81 | 7.7 | 20 | 30 | — |
| `mortar` | fra | `DIMMORT2` | 200 | 7.81 | 7.7 | 20 | 30 | — |
| `mortar` | hun | `DIMMORT2` | 200 | 7.81 | 7.7 | 20 | 30 | — |
| `mortar` | net | `DIMMORT2` | 200 | 7.81 | 7.7 | 20 | 30 | — |
| `mortar` | pie | `DIMMORT2` | 200 | 7.81 | 7.7 | 20 | 30 | — |
| `mortar` | pol | `DIMMORT2` | 200 | 7.81 | 7.7 | 20 | 30 | — |
| `mortar` | por | `DIMMORT2` | 200 | 7.81 | 7.7 | 20 | 30 | — |
| `mortar` | pru | `DIMMORT2` | 200 | 7.81 | 7.7 | 20 | 30 | — |
| `mortar` | rus | `DIMMORT2` | 200 | 7.81 | 7.7 | 20 | 30 | — |
| `mortar` | sax | `DIMMORT2` | 200 | 7.81 | 7.7 | 20 | 30 | — |
| `mortar` | sco | `DIMMORT2` | 200 | 7.81 | 7.7 | 20 | 30 | — |
| `mortar` | spa | `DIMMORT2` | 200 | 7.81 | 7.7 | 20 | 30 | — |
| `mortar` | swe | `DIMMORT2` | 200 | 7.81 | 7.7 | 20 | 30 | — |
| `mortar` | swi | `DIMMORT2` | 200 | 7.81 | 7.7 | 20 | 30 | — |
| `mortar` | tur | `DIMMORT2` | 200 | 7.81 | 7.7 | 20 | 30 | — |
| `mortar` | ukr | `DIMMORT2` | 200 | 7.81 | 7.7 | 20 | 30 | — |
| `mortar` | ven | `DIMMORT2` | 200 | 7.81 | 7.7 | 20 | 30 | — |
| `multicannon` | aus | `PSMPOINTT` | 500 | 1.88 | 31.9 | 40 | 30 | — |
| `multicannon` | bav | `PSMPOINTT` | 500 | 1.88 | 31.9 | 40 | 30 | — |
| `multicannon` | den | `PSMPOINTT` | 500 | 1.88 | 31.9 | 40 | 30 | — |
| `multicannon` | eng | `PSMPOINTT` | 500 | 1.88 | 31.9 | 40 | 30 | — |
| `multicannon` | fra | `PSMPOINTT` | 500 | 1.88 | 31.9 | 40 | 30 | — |
| `multicannon` | hun | `PSMPOINTT` | 500 | 1.88 | 31.9 | 40 | 30 | — |
| `multicannon` | net | `PSMPOINTT` | 500 | 1.88 | 31.9 | 40 | 30 | — |
| `multicannon` | pie | `PSMPOINTT` | 500 | 1.88 | 31.9 | 40 | 30 | — |
| `multicannon` | pol | `PSMPOINTT` | 500 | 1.88 | 31.9 | 40 | 30 | — |
| `multicannon` | por | `PSMPOINTT` | 500 | 1.88 | 31.9 | 40 | 30 | — |
| `multicannon` | pru | `PSMPOINTT` | 500 | 1.88 | 31.9 | 40 | 30 | — |
| `multicannon` | rus | `PSMPOINTT` | 500 | 1.88 | 31.9 | 40 | 30 | — |
| `multicannon` | sax | `PSMPOINTT` | 500 | 1.88 | 31.9 | 40 | 30 | — |
| `multicannon` | spa | `PSMPOINTT` | 500 | 1.88 | 31.9 | 40 | 30 | — |
| `multicannon` | swe | `PSMPOINTT` | 500 | 1.88 | 31.9 | 40 | 30 | — |
| `multicannon` | swi | `PSMPOINTT` | 500 | 1.88 | 31.9 | 40 | 30 | — |
| `multicannon` | ven | `PSMPOINTT` | 500 | 1.88 | 31.9 | 40 | 30 | — |
| `musketeer` | bav | `SHOTMUSKET` | 12 | 4.69 | 12.8 | 2 | 4 | — |
| `musketeer` | den | `SHOTMUSKET` | 12 | 4.69 | 12.8 | 2 | 4 | — |
| `musketeer` | eng | `SHOTMUSKET` | 12 | 4.69 | 12.8 | 2 | 4 | — |
| `musketeer` | fra | `SHOTMUSKET` | 12 | 4.69 | 12.8 | 2 | 4 | — |
| `musketeer` | pie | `SHOTMUSKET` | 12 | 4.69 | 12.8 | 2 | 4 | — |
| `musketeer` | por | `SHOTMUSKET` | 12 | 4.69 | 12.8 | 2 | 4 | — |
| `musketeer` | pru | `SHOTMUSKET` | 12 | 4.69 | 12.8 | 2 | 4 | — |
| `musketeer` | sax | `SHOTMUSKET` | 12 | 4.69 | 12.8 | 2 | 4 | — |
| `musketeer` | swe | `SHOTMUSKET` | 12 | 4.69 | 12.8 | 2 | 4 | — |
| `musketeer` | swi | `SHOTMUSKET` | 12 | 4.69 | 12.8 | 2 | 4 | — |
| `musketeer` | ven | `SHOTMUSKET` | 12 | 4.69 | 12.8 | 2 | 4 | — |
| `musketeer18` | aus | `SHOTMUSKET` | 16 | 4.69 | 12.8 | 2 | 3 | — |
| `musketeer18` | eng | `SHOTMUSKET` | 16 | 4.69 | 12.8 | 2 | 3 | — |
| `musketeer18` | fra | `SHOTMUSKET` | 16 | 4.69 | 12.8 | 2 | 3 | — |
| `musketeer18` | hun | `SHOTMUSKET` | 16 | 4.69 | 12.8 | 2 | 3 | — |
| `musketeer18` | net | `SHOTMUSKET` | 16 | 4.69 | 12.8 | 2 | 3 | — |
| `musketeer18` | pie | `SHOTMUSKET` | 16 | 4.69 | 12.8 | 2 | 3 | — |
| `musketeer18` | pol | `SHOTMUSKET` | 16 | 4.69 | 12.8 | 2 | 3 | — |
| `musketeer18` | por | `SHOTMUSKET` | 16 | 4.69 | 12.8 | 2 | 3 | — |
| `musketeer18` | rus | `SHOTMUSKET` | 16 | 4.69 | 12.8 | 2 | 3 | — |
| `musketeer18` | spa | `SHOTMUSKET` | 16 | 4.69 | 12.8 | 2 | 3 | — |
| `musketeer18` | swe | `SHOTMUSKET` | 16 | 4.69 | 12.8 | 2 | 3 | — |
| `musketeer18` | swi | `SHOTMUSKET` | 16 | 4.69 | 12.8 | 2 | 3 | — |
| `musketeer18` | ven | `SHOTMUSKET` | 16 | 4.69 | 12.8 | 2 | 3 | — |
| `musketeer18bav` | bav | `SHOTMUSKET` | 22 | 5.94 | 10.1 | 3 | 4 | — |
| `musketeer18den` | den | `SHOTMUSKET` | 29 | 5.94 | 10.1 | 4 | 5 | — |
| `musketeer18pru` | pru | `SHOTMUSKET` | 22 | 4.69 | 12.8 | 3 | 4 | — |
| `musketeer18sax` | sax | `SHOTMUSKET` | 19 | 4.38 | 13.7 | 3 | 3 | — |
| `musketeeraus` | aus | `SHOTMUSKET` | 12 | 5.0 | 12.0 | 2 | 4 | — |
| `musketeernet` | net | `SHOTMUSKET` | 10 | 3.75 | 16.0 | 1 | 3 | — |
| `musketeerpol` | pol | `SHOTMUSKET` | 9 | 3.12 | 19.2 | 1 | 2 | — |
| `musketeersco` | sco | `SHOTMUSKET` | 12 | 4.69 | 12.8 | 2 | 5 | — |
| `musketeerspa` | spa | `SHOTMUSKET` | 15 | 5.94 | 10.1 | 3 | 6 | — |
| `pandur` | aus | `SHOTMUSKET` | 17 | 4.69 | 12.8 | 3 | 6 | — |
| `pandurhun` | hun | `SHOTMUSKET` | 19 | 5.0 | 12.0 | 3 | 7 | — |
| `porpor` | por | `cannonball` | 1000 | 8.75 | 6.9 | 10 | 30 | — |
| `rustow` | rus | `cannonball` | 1000 | 9.38 | 6.4 | 10 | 30 | — |
| `serdiuk` | ukr | `SHOTMUSKET` | 12 | 4.06 | 14.8 | 3 | 6 | — |
| `strelet` | rus | `SHOTMUSKET` | 12 | 4.69 | 12.8 | 2 | 4 | — |
| `tatar` | tur | `STRELA` | 15 | 1.56 | 38.5 | — | — | — |
| `turtow` | alg | `cannonball` | 1200 | 15.62 | 3.8 | 15 | 40 | — |
| `turtow` | tur | `cannonball` | 1200 | 15.62 | 3.8 | 15 | 40 | — |
| `xebec` | alg | `PPOINTTKOR` | 1800 | 1.56 | 38.5 | 25 | 35 | — |
| `xebec` | tur | `PPOINTTKOR` | 1800 | 1.56 | 38.5 | 25 | 35 | — |
| `yacht` | aus | `PPOINTTKOR` | 1000 | 10.94 | 5.5 | 4 | 9 | — |
| `yacht` | bav | `PPOINTTKOR` | 1000 | 10.94 | 5.5 | 4 | 9 | — |
| `yacht` | den | `PPOINTTKOR` | 1000 | 10.94 | 5.5 | 4 | 9 | — |
| `yacht` | eng | `PPOINTTKOR` | 1000 | 10.94 | 5.5 | 4 | 9 | — |
| `yacht` | fra | `PPOINTTKOR` | 1000 | 10.94 | 5.5 | 4 | 9 | — |
| `yacht` | hun | `PPOINTTKOR` | 1000 | 10.94 | 5.5 | 4 | 9 | — |
| `yacht` | net | `PPOINTTKOR` | 1000 | 10.94 | 5.5 | 4 | 9 | — |
| `yacht` | pie | `PPOINTTKOR` | 1000 | 10.94 | 5.5 | 4 | 9 | — |
| `yacht` | pol | `PPOINTTKOR` | 1000 | 10.94 | 5.5 | 4 | 9 | — |
| `yacht` | por | `PPOINTTKOR` | 1000 | 10.94 | 5.5 | 4 | 9 | — |
| `yacht` | pru | `PPOINTTKOR` | 1000 | 10.94 | 5.5 | 4 | 9 | — |
| `yacht` | rus | `PPOINTTKOR` | 1000 | 10.94 | 5.5 | 4 | 9 | — |
| `yacht` | sax | `PPOINTTKOR` | 1000 | 10.94 | 5.5 | 4 | 9 | — |
| `yacht` | sco | `PPOINTTKOR` | 1000 | 10.94 | 5.5 | 4 | 9 | — |
| `yacht` | spa | `PPOINTTKOR` | 1000 | 10.94 | 5.5 | 4 | 9 | — |
| `yacht` | swe | `PPOINTTKOR` | 1000 | 10.94 | 5.5 | 4 | 9 | — |
| `yacht` | swi | `PPOINTTKOR` | 1000 | 10.94 | 5.5 | 4 | 9 | — |
| `yacht` | ven | `PPOINTTKOR` | 1000 | 10.94 | 5.5 | 4 | 9 | — |
| `yachttur` | tur | `PPOINTTKOR` | 1000 | 10.94 | 5.5 | 4 | 9 | — |

## 7. Апгрейды

Доступные апгрейды по нациям. Цена показана только для тех, что удалось извлечь из script (большинство — из `_country_Init` / `_country_InitUnitsUpgrades`). Для апгрейдов из локали без cost / time в этой таблице — данные см. в самом скрипте.

### aus — Austria

| sid | имя (EN) | level | value | время (s) | F | W | S | G | I | C |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `ausaca.1` | Cultivate new cultures of wheat (harvesting +40%) | 1 | 40 | 15.62 | 0 | 200 | 0 | 325 | 0 | 0 |
| `ausaca.10` | Raise builders' salary (building construction time -75%) | 1 | -7500000 | 15.62 | 0 | 0 | 0 | 6950 | 0 | 0 |
| `ausaca.11` | Research new fortification grades (durability of walls and towers +80) | 1 | 80 | 15.62 | 0 | 0 | 16200 | 1500 | 0 | 0 |
| `ausaca.12` | Improve firearms: rifled barrel (fire power +10%) | 1 | 10 | 15.62 | 0 | 0 | 0 | 0 | 5000 | 0 |
| `ausaca.13` | Research granular gunpowder (fire power +10%) | 1 | 10 | 15.62 | 0 | 0 | 0 | 4000 | 0 | 0 |
| `ausaca.14` | Research new sulphur purification methods (fire power +15%) | 1 | 15 | 15.62 | 0 | 0 | 0 | 7000 | 0 | 0 |
| `ausaca.15` | Research new nitre purification methods (fire power +25%) | 1 | 25 | 15.62 | 0 | 0 | 0 | 0 | 0 | 11000 |
| `ausaca.16` | Research improved additions to gunpowder formula (artillery range +5%) | 1 | 5 | 15.62 | 0 | 0 | 0 | 2000 | 12150 | 0 |
| `ausaca.17` | Design new barrel types: unicorn, carronade (artillery range +10%) | 1 | 10 | 15.62 | 0 | 0 | 3000 | 4550 | 19200 | 0 |
| `ausaca.18` | Design more durable gun carriage: Gribovalle system (artillery durability +50%) | 1 | 50 | 15.62 | 0 | 0 | 0 | 500 | 3830 | 1500 |
| `ausaca.19` | Design multi-barrelled cannon | 1 | 0 | 15.62 | 0 | 0 | 0 | 1500 | 0 | 2500 |
| `ausaca.2` | Cultivate new cultures of rye (harvesting +50%) | 1 | 50 | 15.62 | 0 | 2400 | 0 | 625 | 0 | 0 |
| `ausaca.20` | Research new sighting devices for artillery (artillery accuracy +35%) | 1 | -35 | 15.62 | 0 | 3540 | 0 | 2000 | 0 | 7250 |
| `ausaca.21` | Finance artillery repair shops (repair all artillery) | 1 | 25 | 15.62 | 0 | 350 | 0 | 100 | 0 | 250 |
| `ausaca.22` | Develop geology (previously hidden deposits appear on the map) | 1 | 0 | 15.62 | 0 | 0 | 0 | 250 | 0 | 0 |
| `ausaca.23` | Develop mining (stone excavation efficiency +100%) | 1 | 100 | 15.62 | 0 | 0 | 0 | 1550 | 3000 | 0 |
| `ausaca.24` | Raise miners' salary (stone excavation efficiency +200%) | 1 | 200 | 15.62 | 4200 | 0 | 0 | 1550 | 0 | 12520 |
| `ausaca.25` | Design Montgolfier (reveals the whole map) | 1 | 0 | 15.62 | 0 | 0 | 0 | 5750 | 0 | 0 |
| `ausaca.26` | Develop medical science (heals all live units) | 1 | 50 | 31.25 | 0 | 0 | 0 | 200 | 0 | 200 |
| `ausaca.27` | Develop mathematics (artillery accuracy +35%) | 1 | -35 | 15.62 | 0 | 9540 | 0 | 12000 | 0 | 65200 |
| `ausaca.28` | Design new rigging types (ship speed +40%) | 1 | 40 | 15.62 | 0 | 65400 | 0 | 24050 | 0 | 0 |
| `ausaca.29` | Design new rib system and new hulls (battleship construction) | 1 | 0 | 15.62 | 0 | 32300 | 0 | 6800 | 9000 | 12800 |
| `ausaca.3` | Raise agriculturists' salary (harvesting +50%) | 1 | 50 | 15.62 | 0 | 3600 | 0 | 850 | 0 | 0 |
| `ausaca.30` | Train carpenters (shipbuilding speed x10) | 1 | -5000000 | 15.62 | 0 | 2300 | 42700 | 1150 | 0 | 0 |
| `ausaca.31` | Design wheellock (rate of fire +30%) | 1 | -30 | 15.62 | 0 | 0 | 6000 | 5500 | 4200 | 0 |
| `ausaca.32` | Design flintlock (musket cost -50%) | 1 | 0 | 15.62 | 0 | 0 | 0 | 6050 | 0 | 7750 |
| `ausaca.33` | Design paper cartridge and iron ramrod (rate of fire +30%) | 1 | -30 | 15.62 | 0 | 5000 | 0 | 5500 | 0 | 15200 |
| `ausaca.34` | Research improved steel grades for cuirasses (armoured soldier defence +2) | 1 | 2 | 15.62 | 0 | 0 | 0 | 9750 | 0 | 0 |
| `ausaca.35` | Design bayonet: barrel-inserted, bayonet with a tube (cold steel weapons +5) | 1 | 5 | 15.62 | 0 | 0 | 0 | 11500 | 0 | 0 |
| `ausaca.36` | Research new steel grades (18c musketeer/grenadier melee attack efficiency +25%) | 1 | 25 | 15.62 | 0 | 0 | 0 | 19500 | 0 | 0 |
| `ausaca.4` | Carry out field melioration (field capacity +200%) | 1 | 200 | 15.62 | 0 | 1000 | 0 | 475 | 0 | 0 |
| `ausaca.5` | Design new tackle and fishing nets (boat efficiency +100%) | 1 | 100 | 15.62 | 0 | 12400 | 0 | 2520 | 0 | 0 |
| `ausaca.6` | Develop new woodworking methods (frigate building) | 1 | 0 | 15.62 | 0 | 12400 | 0 | 7040 | 0 | 0 |
| `ausaca.7` | Build new shipyards for fishing boats (fishing boat cost -85%) | 1 | 0 | 15.62 | 0 | 7300 | 0 | 1220 | 0 | 0 |
| `ausaca.8` | Design new woodworking tools (woodcutting efficiency +100%) | 1 | 100 | 15.62 | 5500 | 0 | 0 | 550 | 0 | 0 |
| `ausaca.9` | Use new construction materials (durability of buildings +85) | 1 | 85 | 15.62 | 0 | 9400 | 7850 | 1150 | 0 | 0 |
| `ausart.cannon.1.1` | — | 2 | — | 10.0 | 0 | 1000 | 500 | 300 | 0 | 0 |
| `ausart.cannon.1.2` | — | 3 | — | 10.0 | 0 | 3000 | 1000 | 500 | 0 | 0 |
| `ausart.cannon.1.3` | — | 4 | — | 10.0 | 0 | 6000 | 2000 | 1000 | 0 | 0 |
| `ausart.cannon.1.4` | — | 5 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `ausart.cannon.1.5` | — | 6 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `ausart.cannon.1.6` | — | 7 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `ausart.cannon.2.1` | — | 2 | -2500000 | 10.0 | 0 | 0 | 0 | 500 | 1000 | 0 |
| `ausart.cannon.2.2` | — | 3 | -2500000 | 10.0 | 0 | 0 | 0 | 1000 | 2000 | 0 |
| `ausart.cannon.2.3` | — | 4 | -2500000 | 10.0 | 0 | 0 | 0 | 2000 | 3000 | 0 |
| `ausart.cannon.2.4` | — | 5 | -2000000 | 15.62 | 2560 | 0 | 0 | 0 | 0 | 0 |
| `ausart.cannon.2.5` | — | 6 | -2000000 | 15.62 | 3560 | 0 | 0 | 0 | 0 | 0 |
| `ausart.cannon.2.6` | — | 7 | -2000000 | 15.62 | 5560 | 0 | 0 | 0 | 0 | 0 |
| `ausart.howitzer.1.1` | — | 2 | — | 10.0 | 0 | 1000 | 500 | 300 | 0 | 0 |
| `ausart.howitzer.1.2` | — | 3 | — | 10.0 | 0 | 3000 | 1000 | 500 | 0 | 0 |
| `ausart.howitzer.1.3` | — | 4 | — | 10.0 | 0 | 6000 | 2000 | 1000 | 0 | 0 |
| `ausart.howitzer.1.4` | — | 5 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `ausart.howitzer.1.5` | — | 6 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `ausart.howitzer.1.6` | — | 7 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `ausart.howitzer.2.1` | — | 2 | -2500000 | 10.0 | 0 | 0 | 0 | 500 | 1000 | 0 |
| `ausart.howitzer.2.2` | — | 3 | -2500000 | 10.0 | 0 | 0 | 0 | 1000 | 2000 | 0 |
| `ausart.howitzer.2.3` | — | 4 | -2500000 | 10.0 | 0 | 0 | 0 | 2000 | 3000 | 0 |
| `ausart.howitzer.2.4` | — | 5 | -2000000 | 31.25 | 2560 | 0 | 0 | 0 | 0 | 0 |
| `ausart.howitzer.2.5` | — | 6 | -2000000 | 31.25 | 3560 | 0 | 0 | 0 | 0 | 0 |
| `ausart.howitzer.2.6` | — | 7 | -2000000 | 31.25 | 5560 | 0 | 0 | 0 | 0 | 0 |
| `ausba2.drummer18.2.1` | Barracks 18c drummer18 protection +15 (lvl 2) | 2 | 15 | 15.62 | 706 | 0 | 0 | 50 | 0 | 0 |
| `ausba2.grenadier.1.1` | Barracks 18c grenadier damage +2 (lvl 2) | 2 | 2 | 15.62 | 2000 | 0 | 0 | 800 | 0 | 0 |
| `ausba2.grenadier.1.2` | Barracks 18c grenadier damage +3 (lvl 3) | 3 | 3 | 15.62 | 12000 | 0 | 0 | 1800 | 0 | 0 |
| `ausba2.grenadier.1.3` | Barracks 18c grenadier damage +4 (lvl 4) | 4 | 4 | 15.62 | 32000 | 0 | 0 | 2800 | 0 | 0 |
| `ausba2.grenadier.1.4` | Barracks 18c grenadier damage +5 (lvl 5) | 5 | 5 | 15.62 | 42000 | 0 | 0 | 3800 | 0 | 0 |
| `ausba2.grenadier.1.5` | Barracks 18c grenadier damage +6 (lvl 6) | 6 | 6 | 15.62 | 52000 | 0 | 0 | 4800 | 0 | 0 |
| `ausba2.grenadier.1.6` | Barracks 18c grenadier damage +1500 (lvl 7) | 7 | 1500 | 15.62 | 62000 | 0 | 0 | 15800 | 0 | 0 |
| `ausba2.grenadier.2.1` | Barracks 18c grenadier protection +1 (lvl 2) | 2 | 1 | 15.62 | 3706 | 0 | 0 | 350 | 0 | 0 |
| `ausba2.grenadier.2.2` | Barracks 18c grenadier protection +2 (lvl 3) | 3 | 2 | 15.62 | 11030 | 0 | 0 | 1350 | 0 | 0 |
| `ausba2.grenadier.2.3` | Barracks 18c grenadier protection +3 (lvl 4) | 4 | 3 | 15.62 | 35706 | 0 | 0 | 3000 | 0 | 0 |
| `ausba2.grenadier.2.4` | Barracks 18c grenadier protection +1 (lvl 5) | 5 | 1 | 15.62 | 36556 | 0 | 0 | 3350 | 0 | 0 |
| `ausba2.grenadier.2.5` | Barracks 18c grenadier protection +2 (lvl 6) | 6 | 2 | 15.62 | 30060 | 0 | 0 | 1350 | 0 | 0 |
| `ausba2.grenadier.2.6` | Barracks 18c grenadier protection +3 (lvl 7) | 7 | 3 | 15.62 | 64000 | 0 | 0 | 1350 | 0 | 0 |
| `ausba2.musketeer18.1.1` | Barracks 18c musketeer18 damage +1 (lvl 2) | 2 | 1 | 15.62 | 1000 | 0 | 0 | 800 | 0 | 0 |
| `ausba2.musketeer18.1.2` | Barracks 18c musketeer18 damage +1 (lvl 3) | 3 | 1 | 15.62 | 1500 | 0 | 0 | 800 | 0 | 0 |
| `ausba2.musketeer18.1.3` | Barracks 18c musketeer18 damage +2 (lvl 4) | 4 | 2 | 15.62 | 2000 | 0 | 0 | 800 | 0 | 0 |
| `ausba2.musketeer18.1.4` | Barracks 18c musketeer18 damage +2 (lvl 5) | 5 | 2 | 15.62 | 2500 | 0 | 0 | 800 | 0 | 0 |
| `ausba2.musketeer18.1.5` | Barracks 18c musketeer18 damage +3 (lvl 6) | 6 | 3 | 15.62 | 3000 | 0 | 0 | 800 | 0 | 0 |
| `ausba2.musketeer18.1.6` | Barracks 18c musketeer18 damage +3 (lvl 7) | 7 | 3 | 15.62 | 3500 | 0 | 0 | 800 | 0 | 0 |
| `ausba2.musketeer18.2.1` | Barracks 18c musketeer18 protection +1 (lvl 2) | 2 | 1 | 15.62 | 3706 | 0 | 0 | 350 | 0 | 0 |
| `ausba2.musketeer18.2.2` | Barracks 18c musketeer18 protection +2 (lvl 3) | 3 | 2 | 15.62 | 11030 | 0 | 0 | 1350 | 0 | 0 |
| `ausba2.musketeer18.2.3` | Barracks 18c musketeer18 protection +2 (lvl 4) | 4 | 2 | 15.62 | 35706 | 0 | 0 | 4000 | 0 | 0 |
| `ausba2.musketeer18.2.4` | Barracks 18c musketeer18 protection +1 (lvl 5) | 5 | 1 | 15.62 | 36556 | 0 | 0 | 4350 | 0 | 0 |
| `ausba2.musketeer18.2.5` | Barracks 18c musketeer18 protection +2 (lvl 6) | 6 | 2 | 15.62 | 30060 | 0 | 0 | 1350 | 0 | 0 |
| `ausba2.musketeer18.2.6` | Barracks 18c musketeer18 protection +2 (lvl 7) | 7 | 2 | 15.62 | 37600 | 0 | 0 | 1350 | 0 | 0 |
| `ausba2.officer18.1.1` | Barracks 18c officer18 damage +30 (lvl 2) | 2 | 30 | 15.62 | 1000 | 0 | 0 | 800 | 0 | 0 |
| `ausba2.officer18.2.1` | Barracks 18c officer18 protection +12 (lvl 2) | 2 | 12 | 15.62 | 1706 | 0 | 0 | 350 | 0 | 0 |
| `ausba2.pandur.1.1` | Barracks 18c pandur damage +1 (lvl 2) | 2 | 1 | 15.62 | 3000 | 0 | 0 | 750 | 0 | 0 |
| `ausba2.pandur.1.2` | Barracks 18c pandur damage +1 (lvl 3) | 3 | 1 | 15.62 | 4000 | 0 | 0 | 1100 | 0 | 0 |
| `ausba2.pandur.1.3` | Barracks 18c pandur damage +2 (lvl 4) | 4 | 2 | 15.62 | 7000 | 0 | 0 | 1800 | 0 | 0 |
| `ausba2.pandur.1.4` | Barracks 18c pandur damage +1 (lvl 5) | 5 | 1 | 15.62 | 12000 | 0 | 0 | 350 | 0 | 0 |
| `ausba2.pandur.1.5` | Barracks 18c pandur damage +1 (lvl 6) | 6 | 1 | 15.62 | 32020 | 0 | 0 | 850 | 0 | 0 |
| `ausba2.pandur.1.6` | Barracks 18c pandur damage +2 (lvl 7) | 7 | 2 | 15.62 | 45200 | 0 | 0 | 1330 | 0 | 0 |
| `ausba2.pandur.2.1` | Barracks 18c pandur protection +1 (lvl 2) | 2 | 1 | 15.62 | 3706 | 0 | 0 | 350 | 0 | 0 |
| `ausba2.pandur.2.2` | Barracks 18c pandur protection +2 (lvl 3) | 3 | 2 | 15.62 | 12060 | 0 | 0 | 1350 | 0 | 0 |
| `ausba2.pandur.2.3` | Barracks 18c pandur protection +2 (lvl 4) | 4 | 2 | 15.62 | 36706 | 0 | 0 | 2250 | 0 | 0 |
| `ausba2.pandur.2.4` | Barracks 18c pandur protection +1 (lvl 5) | 5 | 1 | 15.62 | 36706 | 0 | 0 | 3350 | 0 | 0 |
| `ausba2.pandur.2.5` | Barracks 18c pandur protection +2 (lvl 6) | 6 | 2 | 15.62 | 37060 | 0 | 0 | 1350 | 0 | 0 |
| `ausba2.pandur.2.6` | Barracks 18c pandur protection +2 (lvl 7) | 7 | 2 | 15.62 | 16706 | 0 | 0 | 1350 | 0 | 0 |
| `ausba2.pikeman18.1.1` | Barracks 18c pikeman18 damage +2 (lvl 2) | 2 | 2 | 15.62 | 2000 | 0 | 0 | 800 | 0 | 0 |
| `ausba2.pikeman18.1.2` | Barracks 18c pikeman18 damage +2 (lvl 3) | 3 | 2 | 15.62 | 8000 | 0 | 0 | 1200 | 0 | 0 |
| `ausba2.pikeman18.1.3` | Barracks 18c pikeman18 damage +2 (lvl 4) | 4 | 2 | 15.62 | 20000 | 0 | 0 | 2500 | 0 | 0 |
| `ausba2.pikeman18.1.4` | Barracks 18c pikeman18 damage +2 (lvl 5) | 5 | 2 | 15.62 | 32000 | 0 | 0 | 2800 | 0 | 0 |
| `ausba2.pikeman18.1.5` | Barracks 18c pikeman18 damage +2 (lvl 6) | 6 | 2 | 15.62 | 32000 | 0 | 0 | 3800 | 0 | 0 |
| `ausba2.pikeman18.1.6` | Barracks 18c pikeman18 damage +2 (lvl 7) | 7 | 2 | 15.62 | 40500 | 0 | 0 | 4800 | 0 | 0 |
| `ausba2.pikeman18.2.1` | Barracks 18c pikeman18 protection +2 (lvl 2) | 2 | 2 | 15.62 | 1500 | 0 | 0 | 500 | 0 | 0 |
| `ausba2.pikeman18.2.2` | Barracks 18c pikeman18 protection +3 (lvl 3) | 3 | 3 | 15.62 | 7000 | 0 | 0 | 1500 | 0 | 0 |
| `ausba2.pikeman18.2.3` | Barracks 18c pikeman18 protection +2 (lvl 4) | 4 | 2 | 15.62 | 37000 | 0 | 0 | 2000 | 0 | 0 |
| `ausba2.pikeman18.2.4` | Barracks 18c pikeman18 protection +3 (lvl 5) | 5 | 3 | 15.62 | 37000 | 0 | 0 | 5500 | 0 | 0 |
| `ausba2.pikeman18.2.5` | Barracks 18c pikeman18 protection +2 (lvl 6) | 6 | 2 | 15.62 | 37000 | 0 | 0 | 5500 | 0 | 0 |
| `ausba2.pikeman18.2.6` | Barracks 18c pikeman18 protection +3 (lvl 7) | 7 | 3 | 15.62 | 64600 | 0 | 0 | 5500 | 0 | 0 |
| `ausbar.1` | — | 1 | 140 | 15.62 | 750 | 0 | 0 | 250 | 0 | 0 |
| `ausbar.2` | — | 2 | 180 | 15.62 | 25600 | 0 | 0 | 3350 | 2000 | 0 |
| `ausbar.drummer.2.1` | Barracks 17c drummer protection +12 (lvl 2) | 2 | 12 | 15.62 | 706 | 0 | 0 | 50 | 0 | 0 |
| `ausbar.musketeeraus.1.1` | Barracks 17c musketeeraus damage +1 (lvl 2) | 2 | 1 | 15.62 | 2000 | 0 | 0 | 100 | 0 | 0 |
| `ausbar.musketeeraus.1.2` | Barracks 17c musketeeraus damage +1 (lvl 3) | 3 | 1 | 15.62 | 1000 | 0 | 0 | 300 | 0 | 0 |
| `ausbar.musketeeraus.1.3` | Barracks 17c musketeeraus damage +2 (lvl 4) | 4 | 2 | 15.62 | 500 | 0 | 0 | 700 | 0 | 0 |
| `ausbar.musketeeraus.2.1` | Barracks 17c musketeeraus protection +1 (lvl 2) | 2 | 1 | 15.62 | 170 | 0 | 0 | 50 | 100 | 0 |
| `ausbar.musketeeraus.2.2` | Barracks 17c musketeeraus protection +1 (lvl 3) | 3 | 1 | 15.62 | 405 | 0 | 0 | 150 | 200 | 0 |
| `ausbar.musketeeraus.2.3` | Barracks 17c musketeeraus protection +1 (lvl 4) | 4 | 1 | 15.62 | 1570 | 0 | 0 | 100 | 350 | 0 |
| `ausbar.musketeeraus.2.4` | Barracks 17c musketeeraus protection +1 (lvl 5) | 5 | 1 | 15.62 | 1556 | 0 | 0 | 550 | 100 | 0 |
| `ausbar.musketeeraus.2.5` | Barracks 17c musketeeraus protection +1 (lvl 6) | 6 | 1 | 15.62 | 1060 | 0 | 0 | 850 | 400 | 0 |
| `ausbar.musketeeraus.2.6` | Barracks 17c musketeeraus protection +1 (lvl 7) | 7 | 1 | 15.62 | 3700 | 0 | 0 | 750 | 700 | 0 |
| `ausbar.officer.1.1` | Barracks 17c officer damage +20 (lvl 2) | 2 | 20 | 15.62 | 100 | 0 | 0 | 50 | 0 | 0 |
| `ausbar.officer.2.1` | Barracks 17c officer protection +6 (lvl 2) | 2 | 6 | 15.62 | 1850 | 0 | 0 | 450 | 0 | 0 |
| `ausbar.pikeman.1.1` | Barracks 17c pikeman damage +1 (lvl 2) | 2 | 1 | 15.62 | 200 | 0 | 0 | 50 | 0 | 0 |
| `ausbar.pikeman.1.2` | Barracks 17c pikeman damage +2 (lvl 3) | 3 | 2 | 15.62 | 1300 | 0 | 0 | 300 | 0 | 0 |
| `ausbar.pikeman.1.3` | Barracks 17c pikeman damage +2 (lvl 4) | 4 | 2 | 15.62 | 3600 | 0 | 0 | 450 | 0 | 0 |
| `ausbar.pikeman.1.4` | Barracks 17c pikeman damage +1 (lvl 5) | 5 | 1 | 15.62 | 7200 | 0 | 0 | 1850 | 0 | 0 |
| `ausbar.pikeman.1.5` | Barracks 17c pikeman damage +2 (lvl 6) | 6 | 2 | 15.62 | 16030 | 0 | 0 | 2000 | 0 | 0 |
| `ausbar.pikeman.1.6` | — | 7 | 2 | 15.62 | 15000 | 0 | 0 | 1875 | 0 | 0 |
| `ausbar.pikeman.2.1` | Barracks 17c pikeman protection +1 (lvl 2) | 2 | 1 | 15.62 | 150 | 0 | 0 | 50 | 0 | 0 |
| `ausbar.pikeman.2.2` | Barracks 17c pikeman protection +1 (lvl 3) | 3 | 1 | 15.62 | 900 | 0 | 0 | 175 | 0 | 0 |
| `ausbar.pikeman.2.3` | Barracks 17c pikeman protection +2 (lvl 4) | 4 | 2 | 15.62 | 4500 | 0 | 0 | 300 | 0 | 0 |
| `ausbar.pikeman.2.4` | Barracks 17c pikeman protection +1 (lvl 5) | 5 | 1 | 15.62 | 9005 | 0 | 0 | 507 | 0 | 0 |
| `ausbar.pikeman.2.5` | Barracks 17c pikeman protection +1 (lvl 6) | 6 | 1 | 15.62 | 18010 | 0 | 0 | 3050 | 0 | 0 |
| `ausbar.pikeman.2.6` | — | 7 | 2 | 15.62 | 11250 | 0 | 0 | 1500 | 0 | 0 |
| `ausbar.roundshier.1.1` | Barracks 17c roundshier damage +1 (lvl 2) | 2 | 1 | 15.62 | 150 | 0 | 0 | 50 | 0 | 0 |
| `ausbar.roundshier.1.2` | Barracks 17c roundshier damage +1 (lvl 3) | 3 | 1 | 15.62 | 1500 | 0 | 0 | 200 | 0 | 0 |
| `ausbar.roundshier.1.3` | Barracks 17c roundshier damage +2 (lvl 4) | 4 | 2 | 15.62 | 1300 | 0 | 0 | 325 | 0 | 0 |
| `ausbar.roundshier.1.4` | — | 5 | 1 | 15.62 | 7500 | 0 | 0 | 900 | 0 | 0 |
| `ausbar.roundshier.1.5` | — | 6 | 1 | 15.62 | 9000 | 0 | 0 | 1080 | 0 | 0 |
| `ausbar.roundshier.1.6` | — | 7 | 2 | 15.62 | 18750 | 0 | 0 | 2250 | 0 | 0 |
| `ausbar.roundshier.2.1` | Barracks 17c roundshier protection +1 (lvl 2) | 2 | 1 | 15.62 | 200 | 0 | 0 | 70 | 120 | 0 |
| `ausbar.roundshier.2.2` | Barracks 17c roundshier protection +2 (lvl 3) | 3 | 2 | 15.62 | 4360 | 0 | 0 | 150 | 320 | 0 |
| `ausbar.roundshier.2.3` | Barracks 17c roundshier protection +2 (lvl 4) | 4 | 2 | 15.62 | 506 | 0 | 0 | 250 | 420 | 0 |
| `ausbar.roundshier.2.4` | — | 5 | 1 | 15.62 | 3750 | 0 | 0 | 450 | 0 | 0 |
| `ausbar.roundshier.2.5` | — | 6 | 1 | 15.62 | 6750 | 0 | 0 | 810 | 0 | 0 |
| `ausbar.roundshier.2.6` | — | 7 | 2 | 15.62 | 9375 | 0 | 0 | 1125 | 0 | 0 |
| `ausbla.1` | Manufacture agricultural equipment (field capacity +100%) | 1 | 100 | 15.62 | 0 | 400 | 0 | 90 | 0 | 0 |
| `ausbla.2` | Forge metal armature and gratings (building defence +50) | 1 | 50 | 15.62 | 0 | 0 | 12320 | 350 | 900 | 0 |
| `ausbla.3` | Forge harnesses for horses (mounted units recruitment speed -33%) | 1 | -3333333 | 15.62 | 0 | 0 | 0 | 3650 | 5300 | 8200 |
| `ausbla.4` | Forge bayonets and broadswords for infantry (18c musketeer/grenadier melee attack +5) | 1 | 5 | 15.62 | 0 | 1300 | 0 | 1500 | 900 | 5000 |
| `ausbla.5` | Forge new types of broadswords and sabres (cavalry and sword clansman attack +5) | 1 | 5 | 15.62 | 0 | 0 | 0 | 4000 | 7900 | 0 |
| `ausbla.6` | Forge new cuirasses (armoured soldiers defence +2) | 1 | 2 | 15.62 | 0 | 0 | 0 | 4950 | 10500 | 0 |
| `auscen.1` | — | 1 | 0 | 9.38 | 30000 | 0 | 0 | 5000 | 2000 | 2000 |
| `aussta.croat.2.1` | Stable croat protection +1 (lvl 2) | 2 | 1 | 15.62 | 2000 | 0 | 0 | 1350 | 0 | 0 |
| `aussta.croat.2.2` | Stable croat protection +1 (lvl 3) | 3 | 1 | 15.62 | 1500 | 0 | 0 | 2100 | 0 | 0 |
| `aussta.croat.2.3` | Stable croat protection +2 (lvl 4) | 4 | 2 | 15.62 | 5000 | 0 | 0 | 2300 | 0 | 0 |
| `aussta.croat.2.4` | Stable croat protection +2 (lvl 5) | 5 | 2 | 15.62 | 10500 | 0 | 0 | 3400 | 0 | 0 |
| `aussta.croat.2.5` | Stable croat protection +3 (lvl 6) | 6 | 3 | 15.62 | 12600 | 0 | 0 | 4500 | 0 | 0 |
| `aussta.croat.2.6` | Stable croat protection +3 (lvl 7) | 7 | 3 | 15.62 | 40000 | 0 | 0 | 5000 | 0 | 0 |
| `aussta.cuirassier.1.1` | Stable cuirassier damage +1 (lvl 2) | 2 | 1 | 15.62 | 12000 | 0 | 0 | 600 | 0 | 0 |
| `aussta.cuirassier.1.2` | Stable cuirassier damage +1 (lvl 3) | 3 | 1 | 15.62 | 32000 | 0 | 0 | 1300 | 0 | 0 |
| `aussta.cuirassier.1.3` | Stable cuirassier damage +1 (lvl 4) | 4 | 1 | 15.62 | 62000 | 0 | 0 | 2200 | 0 | 0 |
| `aussta.cuirassier.1.4` | Stable cuirassier damage +2 (lvl 5) | 5 | 2 | 15.62 | 61000 | 0 | 0 | 3150 | 0 | 0 |
| `aussta.cuirassier.1.5` | Stable cuirassier damage +2 (lvl 6) | 6 | 2 | 15.62 | 57055 | 0 | 0 | 4100 | 0 | 0 |
| `aussta.cuirassier.1.6` | Stable cuirassier damage +3 (lvl 7) | 7 | 3 | 15.62 | 49050 | 0 | 0 | 8020 | 0 | 0 |
| `aussta.cuirassier.2.1` | Stable cuirassier protection +2 (lvl 2) | 2 | 2 | 15.62 | 1760 | 0 | 0 | 350 | 1000 | 0 |
| `aussta.cuirassier.2.2` | Stable cuirassier protection +3 (lvl 3) | 3 | 3 | 15.62 | 3000 | 0 | 0 | 750 | 2000 | 0 |
| `aussta.cuirassier.2.3` | Stable cuirassier protection +3 (lvl 4) | 4 | 3 | 15.62 | 7600 | 0 | 0 | 300 | 3030 | 0 |
| `aussta.cuirassier.2.4` | Stable cuirassier protection +2 (lvl 5) | 5 | 2 | 15.62 | 8700 | 0 | 0 | 6200 | 100 | 0 |
| `aussta.cuirassier.2.5` | Stable cuirassier protection +1 (lvl 6) | 6 | 1 | 15.62 | 8700 | 0 | 0 | 2350 | 5000 | 0 |
| `aussta.cuirassier.2.6` | Stable cuirassier protection +1 (lvl 7) | 7 | 1 | 15.62 | 9700 | 0 | 0 | 4444 | 7060 | 0 |
| `aussta.dragoon.1.1` | Stable dragoon damage +1 (lvl 2) | 2 | 1 | 15.62 | 500 | 0 | 0 | 150 | 0 | 0 |
| `aussta.dragoon.1.2` | Stable dragoon damage +1 (lvl 3) | 3 | 1 | 15.62 | 700 | 0 | 0 | 200 | 0 | 0 |
| `aussta.dragoon.1.3` | Stable dragoon damage +2 (lvl 4) | 4 | 2 | 15.62 | 900 | 0 | 0 | 340 | 0 | 0 |
| `aussta.dragoon.1.4` | Stable dragoon damage +1 (lvl 5) | 5 | 1 | 15.62 | 0 | 0 | 0 | 0 | 0 | 0 |
| `aussta.dragoon.1.5` | Stable dragoon damage +1 (lvl 6) | 6 | 1 | 15.62 | 0 | 0 | 0 | 0 | 0 | 0 |
| `aussta.dragoon.1.6` | Stable dragoon damage +3 (lvl 7) | 7 | 3 | 15.62 | 0 | 0 | 0 | 0 | 0 | 0 |
| `aussta.dragoon.2.1` | Stable dragoon protection +1 (lvl 2) | 2 | 1 | 15.62 | 900 | 0 | 0 | 150 | 0 | 0 |
| `aussta.dragoon.2.2` | Stable dragoon protection +2 (lvl 3) | 3 | 2 | 15.62 | 6600 | 0 | 0 | 750 | 0 | 0 |
| `aussta.dragoon.2.3` | Stable dragoon protection +2 (lvl 4) | 4 | 2 | 15.62 | 5000 | 0 | 0 | 1250 | 0 | 0 |
| `aussta.dragoon.2.4` | Stable dragoon protection +1 (lvl 5) | 5 | 1 | 15.62 | 3000 | 0 | 0 | 700 | 0 | 0 |
| `aussta.dragoon.2.5` | Stable dragoon protection +2 (lvl 6) | 6 | 2 | 15.62 | 1000 | 0 | 0 | 2350 | 0 | 0 |
| `aussta.dragoon.2.6` | Stable dragoon protection +2 (lvl 7) | 7 | 2 | 15.62 | 6001 | 0 | 0 | 5000 | 0 | 0 |
| `aussta.dragoon18.1.1` | Stable dragoon18 damage +2 (lvl 2) | 2 | 2 | 15.62 | 2000 | 0 | 0 | 100 | 0 | 0 |
| `aussta.dragoon18.1.2` | Stable dragoon18 damage +2 (lvl 3) | 3 | 2 | 15.62 | 9000 | 0 | 0 | 350 | 0 | 0 |
| `aussta.dragoon18.1.3` | Stable dragoon18 damage +4 (lvl 4) | 4 | 4 | 15.62 | 12000 | 0 | 0 | 400 | 0 | 0 |
| `aussta.dragoon18.1.4` | Stable dragoon18 damage +2 (lvl 5) | 5 | 2 | 15.62 | 23000 | 0 | 0 | 580 | 0 | 0 |
| `aussta.dragoon18.1.5` | Stable dragoon18 damage +2 (lvl 6) | 6 | 2 | 15.62 | 32000 | 0 | 0 | 680 | 0 | 0 |
| `aussta.dragoon18.1.6` | Stable dragoon18 damage +4 (lvl 7) | 7 | 4 | 15.62 | 42000 | 0 | 0 | 780 | 0 | 0 |
| `aussta.dragoon18.2.1` | Stable dragoon18 protection +1 (lvl 2) | 2 | 1 | 15.62 | 760 | 0 | 0 | 935 | 0 | 0 |
| `aussta.dragoon18.2.2` | Stable dragoon18 protection +1 (lvl 3) | 3 | 1 | 15.62 | 1260 | 0 | 0 | 1150 | 0 | 0 |
| `aussta.dragoon18.2.3` | Stable dragoon18 protection +2 (lvl 4) | 4 | 2 | 15.62 | 15600 | 0 | 0 | 2350 | 0 | 0 |
| `aussta.dragoon18.2.4` | Stable dragoon18 protection +1 (lvl 5) | 5 | 1 | 15.62 | 17600 | 0 | 0 | 3350 | 0 | 0 |
| `aussta.dragoon18.2.5` | Stable dragoon18 protection +2 (lvl 6) | 6 | 2 | 15.62 | 19600 | 0 | 0 | 5350 | 0 | 0 |
| `aussta.dragoon18.2.6` | Stable dragoon18 protection +3 (lvl 7) | 7 | 3 | 15.62 | 21760 | 0 | 0 | 9350 | 0 | 0 |
| `aussta.hussar.1.1` | Stable hussar damage +1 (lvl 2) | 2 | 1 | 15.62 | 0 | 0 | 0 | 1800 | 1000 | 0 |
| `aussta.hussar.1.2` | Stable hussar damage +2 (lvl 3) | 3 | 2 | 15.62 | 0 | 0 | 0 | 3800 | 2000 | 0 |
| `aussta.hussar.1.3` | Stable hussar damage +3 (lvl 4) | 4 | 3 | 15.62 | 20200 | 0 | 0 | 0 | 2000 | 0 |
| `aussta.hussar.1.4` | Stable hussar damage +4 (lvl 5) | 5 | 4 | 15.62 | 32000 | 0 | 0 | 0 | 3000 | 0 |
| `aussta.hussar.1.5` | Stable hussar damage +1 (lvl 6) | 6 | 1 | 15.62 | 49200 | 0 | 0 | 0 | 3500 | 0 |
| `aussta.hussar.1.6` | Stable hussar damage +1 (lvl 7) | 7 | 1 | 15.62 | 20000 | 0 | 0 | 0 | 6000 | 0 |
| `aussta.hussar.2.1` | Stable hussar protection +1 (lvl 2) | 2 | 1 | 15.62 | 1760 | 0 | 0 | 1350 | 0 | 0 |
| `aussta.hussar.2.2` | Stable hussar protection +1 (lvl 3) | 3 | 1 | 15.62 | 1900 | 0 | 0 | 2350 | 0 | 0 |
| `aussta.hussar.2.3` | Stable hussar protection +1 (lvl 4) | 4 | 1 | 15.62 | 1600 | 0 | 0 | 5350 | 0 | 0 |
| `aussta.hussar.2.4` | Stable hussar protection +2 (lvl 5) | 5 | 2 | 15.62 | 8000 | 0 | 0 | 8350 | 0 | 0 |
| `aussta.hussar.2.5` | Stable hussar protection +2 (lvl 6) | 6 | 2 | 15.62 | 2000 | 0 | 0 | 15350 | 0 | 0 |
| `aussta.hussar.2.6` | Stable hussar protection +3 (lvl 7) | 7 | 3 | 15.62 | 56000 | 0 | 0 | 20150 | 0 | 0 |
| `aussta.reiter.1.1` | Stable reiter damage +1 (lvl 2) | 2 | 1 | 15.62 | 500 | 0 | 0 | 100 | 0 | 0 |
| `aussta.reiter.1.2` | Stable reiter damage +2 (lvl 3) | 3 | 2 | 15.62 | 900 | 0 | 0 | 220 | 0 | 0 |
| `aussta.reiter.1.3` | Stable reiter damage +1 (lvl 4) | 4 | 1 | 15.62 | 4400 | 0 | 0 | 280 | 0 | 0 |
| `aussta.reiter.1.4` | Stable reiter damage +1 (lvl 5) | 5 | 1 | 15.62 | 2250 | 0 | 0 | 320 | 0 | 0 |
| `aussta.reiter.1.5` | Stable reiter damage +1 (lvl 6) | 6 | 1 | 15.62 | 3030 | 0 | 0 | 600 | 0 | 0 |
| `aussta.reiter.1.6` | Stable reiter damage +1 (lvl 7) | 7 | 1 | 15.62 | 7500 | 0 | 0 | 1800 | 0 | 0 |
| `aussta.reiter.2.1` | Stable reiter protection +2 (lvl 2) | 2 | 2 | 15.62 | 200 | 0 | 0 | 135 | 300 | 0 |
| `aussta.reiter.2.2` | Stable reiter protection +3 (lvl 3) | 3 | 3 | 15.62 | 600 | 0 | 0 | 100 | 400 | 0 |
| `aussta.reiter.2.3` | Stable reiter protection +3 (lvl 4) | 4 | 3 | 15.62 | 800 | 0 | 0 | 200 | 560 | 0 |
| `aussta.reiter.2.4` | Stable reiter protection +2 (lvl 5) | 5 | 2 | 15.62 | 1600 | 0 | 0 | 300 | 640 | 0 |
| `aussta.reiter.2.5` | Stable reiter protection +1 (lvl 6) | 6 | 1 | 15.62 | 3200 | 0 | 0 | 350 | 300 | 0 |
| `aussta.reiter.2.6` | Stable reiter protection +1 (lvl 7) | 7 | 1 | 15.62 | 16000 | 0 | 0 | 1000 | 5000 | 0 |
| `eurcoa.1` | — | 2 | 5 | 9.38 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `eurcoa.2` | — | 3 | 8 | 9.38 | 5250 | 0 | 0 | 4950 | 0 | 0 |
| `eurcoa.3` | — | 4 | 10 | 9.38 | 12500 | 0 | 0 | 9250 | 0 | 0 |
| `eurcoa.4` | — | 5 | 12 | 9.38 | 15800 | 0 | 0 | 18500 | 0 | 0 |
| `eurcoa.5` | — | 6 | 15 | 9.38 | 19800 | 0 | 0 | 21050 | 0 | 0 |
| `eurcoa.6` | — | 7 | 40 | 9.38 | 50200 | 0 | 0 | 25950 | 0 | 0 |
| `eurgol.1` | — | 2 | 5 | 9.38 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `eurgol.2` | — | 3 | 8 | 9.38 | 5250 | 0 | 0 | 4950 | 0 | 0 |
| `eurgol.3` | — | 4 | 10 | 9.38 | 12500 | 0 | 0 | 9250 | 0 | 0 |
| `eurgol.4` | — | 5 | 12 | 9.38 | 15800 | 0 | 0 | 18500 | 0 | 0 |
| `eurgol.5` | — | 6 | 15 | 9.38 | 19800 | 0 | 0 | 21050 | 0 | 0 |
| `eurgol.6` | — | 7 | 40 | 9.38 | 50200 | 0 | 0 | 25950 | 0 | 0 |
| `euriro.1` | — | 2 | 5 | 9.38 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `euriro.2` | — | 3 | 8 | 9.38 | 5250 | 0 | 0 | 4950 | 0 | 0 |
| `euriro.3` | — | 4 | 10 | 9.38 | 12500 | 0 | 0 | 9250 | 0 | 0 |
| `euriro.4` | — | 5 | 12 | 9.38 | 15800 | 0 | 0 | 18500 | 0 | 0 |
| `euriro.5` | — | 6 | 15 | 9.38 | 19800 | 0 | 0 | 21050 | 0 | 0 |
| `euriro.6` | — | 7 | 40 | 9.38 | 50200 | 0 | 0 | 25950 | 0 | 0 |
| `eurpor.1` | — | 1 | 50 | 46.88 | 0 | 20000 | 0 | 1500 | 0 | 0 |
| `eurswa.1` | — | 2 | 5 | 0.03 | 0 | 0 | 500 | 0 | 0 | 0 |
| `eurtow.1` | — | 2 | -20 | 31.25 | 0 | 0 | 0 | 250 | 0 | 0 |
| `eurtow.2` | — | 3 | -20 | 31.25 | 0 | 0 | 0 | 0 | 350 | 0 |
| `eurtow.3` | — | 4 | -10 | 31.25 | 0 | 0 | 0 | 0 | 0 | 400 |
| `eurtow.4` | — | 5 | -10 | 31.25 | 0 | 0 | 0 | 0 | 450 | 0 |
| `eurtow.5` | — | 6 | -10 | 31.25 | 0 | 0 | 0 | 0 | 0 | 500 |
| `ferry.1` | Improve transport vessel design (+%value% capacity) | 2 | 200 | 15.62 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `ukrwwa.1` | — | 2 | 5 | 0.03 | 0 | 400 | 0 | 0 | 0 | 0 |

### fra — France

| sid | имя (EN) | level | value | время (s) | F | W | S | G | I | C |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `eurcoa.1` | — | 2 | 5 | 9.38 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `eurcoa.2` | — | 3 | 8 | 9.38 | 5250 | 0 | 0 | 4950 | 0 | 0 |
| `eurcoa.3` | — | 4 | 10 | 9.38 | 12500 | 0 | 0 | 9250 | 0 | 0 |
| `eurcoa.4` | — | 5 | 12 | 9.38 | 15800 | 0 | 0 | 18500 | 0 | 0 |
| `eurcoa.5` | — | 6 | 15 | 9.38 | 19800 | 0 | 0 | 21050 | 0 | 0 |
| `eurcoa.6` | — | 7 | 40 | 9.38 | 50200 | 0 | 0 | 25950 | 0 | 0 |
| `eurgol.1` | — | 2 | 5 | 9.38 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `eurgol.2` | — | 3 | 8 | 9.38 | 5250 | 0 | 0 | 4950 | 0 | 0 |
| `eurgol.3` | — | 4 | 10 | 9.38 | 12500 | 0 | 0 | 9250 | 0 | 0 |
| `eurgol.4` | — | 5 | 12 | 9.38 | 15800 | 0 | 0 | 18500 | 0 | 0 |
| `eurgol.5` | — | 6 | 15 | 9.38 | 19800 | 0 | 0 | 21050 | 0 | 0 |
| `eurgol.6` | — | 7 | 40 | 9.38 | 50200 | 0 | 0 | 25950 | 0 | 0 |
| `euriro.1` | — | 2 | 5 | 9.38 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `euriro.2` | — | 3 | 8 | 9.38 | 5250 | 0 | 0 | 4950 | 0 | 0 |
| `euriro.3` | — | 4 | 10 | 9.38 | 12500 | 0 | 0 | 9250 | 0 | 0 |
| `euriro.4` | — | 5 | 12 | 9.38 | 15800 | 0 | 0 | 18500 | 0 | 0 |
| `euriro.5` | — | 6 | 15 | 9.38 | 19800 | 0 | 0 | 21050 | 0 | 0 |
| `euriro.6` | — | 7 | 40 | 9.38 | 50200 | 0 | 0 | 25950 | 0 | 0 |
| `eurpor.1` | — | 1 | 50 | 46.88 | 0 | 20000 | 0 | 1500 | 0 | 0 |
| `eurswa.1` | — | 2 | 5 | 0.03 | 0 | 0 | 500 | 0 | 0 | 0 |
| `eurtow.1` | — | 2 | -20 | 31.25 | 0 | 0 | 0 | 250 | 0 | 0 |
| `eurtow.2` | — | 3 | -20 | 31.25 | 0 | 0 | 0 | 0 | 350 | 0 |
| `eurtow.3` | — | 4 | -10 | 31.25 | 0 | 0 | 0 | 0 | 0 | 400 |
| `eurtow.4` | — | 5 | -10 | 31.25 | 0 | 0 | 0 | 0 | 450 | 0 |
| `eurtow.5` | — | 6 | -10 | 31.25 | 0 | 0 | 0 | 0 | 0 | 500 |
| `ferry.1` | Improve transport vessel design (+%value% capacity) | 2 | 200 | 15.62 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `fraaca.1` | Cultivate new cultures of wheat (harvesting +40%) | 1 | 40 | 15.62 | 0 | 190 | 0 | 315 | 0 | 0 |
| `fraaca.10` | Raise builders' salary (building construction time -75%) | 1 | -7500000 | 15.62 | 0 | 0 | 0 | 6950 | 0 | 0 |
| `fraaca.11` | Research new fortification grades (durability of walls and towers +80) | 1 | 80 | 15.62 | 0 | 0 | 16200 | 500 | 0 | 0 |
| `fraaca.12` | Improve firearms: rifled barrel (fire power +10%) | 1 | 10 | 15.62 | 0 | 0 | 0 | 0 | 5000 | 0 |
| `fraaca.13` | Research granular gunpowder (fire power +10%) | 1 | 10 | 15.62 | 0 | 0 | 0 | 4000 | 0 | 0 |
| `fraaca.14` | Research new sulphur purification methods (fire power +15%) | 1 | 15 | 15.62 | 0 | 0 | 0 | 7000 | 0 | 0 |
| `fraaca.15` | Research new nitre purification methods (fire power +25%) | 1 | 25 | 15.62 | 0 | 0 | 0 | 0 | 0 | 11000 |
| `fraaca.16` | Research improved additions to gunpowder formula (artillery range +5%) | 1 | 5 | 15.62 | 0 | 0 | 0 | 2000 | 12150 | 0 |
| `fraaca.17` | Design new barrel types: unicorn, carronade (artillery range +10%) | 1 | 10 | 15.62 | 0 | 0 | 3000 | 4550 | 19200 | 0 |
| `fraaca.18` | Design more durable gun carriage: Gribovalle system (artillery durability +50%) | 1 | 50 | 15.62 | 0 | 0 | 0 | 500 | 3830 | 1500 |
| `fraaca.19` | Design multi-barrelled cannon | 1 | 0 | 15.62 | 0 | 0 | 0 | 1500 | 0 | 2500 |
| `fraaca.2` | Cultivate new cultures of rye (harvesting +50%) | 1 | 50 | 15.62 | 0 | 2400 | 0 | 625 | 0 | 0 |
| `fraaca.20` | Research new sighting devices for artillery (artillery accuracy +35%) | 1 | -35 | 15.62 | 0 | 13540 | 0 | 1500 | 0 | 5950 |
| `fraaca.21` | Finance artillery repair shops (repair all artillery) | 1 | 25 | 15.62 | 0 | 350 | 0 | 100 | 0 | 250 |
| `fraaca.22` | Develop geology (previously hidden deposits appear on the map) | 1 | 0 | 15.62 | 0 | 0 | 0 | 250 | 0 | 0 |
| `fraaca.23` | Develop mining (stone excavation efficiency +100%) | 1 | 100 | 15.62 | 0 | 0 | 0 | 1550 | 3000 | 0 |
| `fraaca.24` | Raise miners' salary (stone excavation efficiency +200%) | 1 | 200 | 15.62 | 4200 | 0 | 0 | 1550 | 0 | 12520 |
| `fraaca.25` | Design Montgolfier (reveals the whole map) | 1 | 0 | 15.62 | 0 | 0 | 0 | 5750 | 0 | 0 |
| `fraaca.26` | Develop medical science (heals all live units) | 1 | 50 | 31.25 | 0 | 0 | 0 | 200 | 0 | 200 |
| `fraaca.27` | Develop mathematics (artillery accuracy +35%) | 1 | -35 | 15.62 | 0 | 23580 | 0 | 9800 | 0 | 65400 |
| `fraaca.28` | Design new rigging types (ship speed +40%) | 1 | 40 | 15.62 | 0 | 65400 | 0 | 24050 | 0 | 0 |
| `fraaca.29` | Design new rib system and new hulls (battleship construction) | 1 | 0 | 15.62 | 0 | 32300 | 0 | 6800 | 9000 | 12800 |
| `fraaca.3` | Raise agriculturists' salary (harvesting +50%) | 1 | 50 | 15.62 | 0 | 3600 | 0 | 850 | 0 | 0 |
| `fraaca.30` | Train carpenters (shipbuilding speed x10) | 1 | -5000000 | 15.62 | 0 | 2300 | 42700 | 1150 | 0 | 0 |
| `fraaca.31` | Design wheellock (rate of fire +30%) | 1 | -30 | 15.62 | 0 | 0 | 6000 | 5500 | 4200 | 0 |
| `fraaca.32` | Design flintlock (musket cost -50%) | 1 | 0 | 15.62 | 0 | 0 | 0 | 6050 | 0 | 7750 |
| `fraaca.33` | Design paper cartridge and iron ramrod (rate of fire +30%) | 1 | -30 | 15.62 | 0 | 5000 | 0 | 5500 | 0 | 15200 |
| `fraaca.34` | Research improved steel grades for cuirasses (armoured soldier defence +2) | 1 | 2 | 15.62 | 0 | 0 | 0 | 9750 | 0 | 0 |
| `fraaca.35` | Design bayonet: barrel-inserted, bayonet with a tube (cold steel weapons +5) | 1 | 5 | 15.62 | 0 | 0 | 0 | 11500 | 0 | 0 |
| `fraaca.36` | Research new steel grades (18c musketeer/grenadier melee attack efficiency +25%) | 1 | 25 | 15.62 | 0 | 0 | 0 | 19500 | 0 | 0 |
| `fraaca.4` | Carry out field melioration (field capacity +200%) | 1 | 200 | 15.62 | 0 | 1000 | 0 | 475 | 0 | 0 |
| `fraaca.5` | Design new tackle and fishing nets (boat efficiency +100%) | 1 | 100 | 15.62 | 0 | 13900 | 0 | 2420 | 0 | 0 |
| `fraaca.6` | Develop new woodworking methods (frigate building) | 1 | 0 | 15.62 | 0 | 13500 | 0 | 7250 | 0 | 0 |
| `fraaca.7` | Build new shipyards for fishing boats (fishing boat cost -85%) | 1 | 0 | 15.62 | 0 | 7800 | 0 | 1110 | 0 | 0 |
| `fraaca.8` | Design new woodworking tools (woodcutting efficiency +100%) | 1 | 100 | 15.62 | 5500 | 0 | 0 | 550 | 0 | 0 |
| `fraaca.9` | Use new construction materials (durability of buildings +85) | 1 | 85 | 15.62 | 0 | 9400 | 7850 | 1150 | 0 | 0 |
| `fraart.cannon.1.1` | — | 2 | — | 10.0 | 0 | 1000 | 500 | 300 | 0 | 0 |
| `fraart.cannon.1.2` | — | 3 | — | 10.0 | 0 | 3000 | 1000 | 500 | 0 | 0 |
| `fraart.cannon.1.3` | — | 4 | — | 10.0 | 0 | 6000 | 2000 | 1000 | 0 | 0 |
| `fraart.cannon.1.4` | — | 5 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `fraart.cannon.1.5` | — | 6 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `fraart.cannon.1.6` | — | 7 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `fraart.cannon.2.1` | — | 2 | -2500000 | 10.0 | 0 | 0 | 0 | 500 | 1000 | 0 |
| `fraart.cannon.2.2` | — | 3 | -2500000 | 10.0 | 0 | 0 | 0 | 1000 | 2000 | 0 |
| `fraart.cannon.2.3` | — | 4 | -2500000 | 10.0 | 0 | 0 | 0 | 2000 | 3000 | 0 |
| `fraart.cannon.2.4` | — | 5 | -2000000 | 15.62 | 2560 | 0 | 0 | 0 | 0 | 0 |
| `fraart.cannon.2.5` | — | 6 | -2000000 | 15.62 | 3560 | 0 | 0 | 0 | 0 | 0 |
| `fraart.cannon.2.6` | — | 7 | -2000000 | 15.62 | 5560 | 0 | 0 | 0 | 0 | 0 |
| `fraart.howitzer.1.1` | — | 2 | — | 10.0 | 0 | 1000 | 500 | 300 | 0 | 0 |
| `fraart.howitzer.1.2` | — | 3 | — | 10.0 | 0 | 3000 | 1000 | 500 | 0 | 0 |
| `fraart.howitzer.1.3` | — | 4 | — | 10.0 | 0 | 6000 | 2000 | 1000 | 0 | 0 |
| `fraart.howitzer.1.4` | — | 5 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `fraart.howitzer.1.5` | — | 6 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `fraart.howitzer.1.6` | — | 7 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `fraart.howitzer.2.1` | — | 2 | -2500000 | 10.0 | 0 | 0 | 0 | 500 | 1000 | 0 |
| `fraart.howitzer.2.2` | — | 3 | -2500000 | 10.0 | 0 | 0 | 0 | 1000 | 2000 | 0 |
| `fraart.howitzer.2.3` | — | 4 | -2500000 | 10.0 | 0 | 0 | 0 | 2000 | 3000 | 0 |
| `fraart.howitzer.2.4` | — | 5 | -2000000 | 31.25 | 2560 | 0 | 0 | 0 | 0 | 0 |
| `fraart.howitzer.2.5` | — | 6 | -2000000 | 31.25 | 3560 | 0 | 0 | 0 | 0 | 0 |
| `fraart.howitzer.2.6` | — | 7 | -2000000 | 31.25 | 5560 | 0 | 0 | 0 | 0 | 0 |
| `fraba2.chasseur.1.1` | Barracks 18c chasseur damage +2 (lvl 2) | 2 | 2 | 15.62 | 3000 | 0 | 0 | 750 | 0 | 0 |
| `fraba2.chasseur.1.2` | Barracks 18c chasseur damage +2 (lvl 3) | 3 | 2 | 15.62 | 4000 | 0 | 0 | 1100 | 0 | 0 |
| `fraba2.chasseur.1.3` | Barracks 18c chasseur damage +2 (lvl 4) | 4 | 2 | 15.62 | 7000 | 0 | 0 | 1800 | 0 | 0 |
| `fraba2.chasseur.1.4` | Barracks 18c chasseur damage +2 (lvl 5) | 5 | 2 | 15.62 | 12000 | 0 | 0 | 350 | 0 | 0 |
| `fraba2.chasseur.1.5` | Barracks 18c chasseur damage +2 (lvl 6) | 6 | 2 | 15.62 | 32020 | 0 | 0 | 850 | 0 | 0 |
| `fraba2.chasseur.1.6` | Barracks 18c chasseur damage +2 (lvl 7) | 7 | 2 | 15.62 | 45200 | 0 | 0 | 1330 | 0 | 0 |
| `fraba2.chasseur.2.1` | Barracks 18c chasseur protection +1 (lvl 2) | 2 | 1 | 15.62 | 3706 | 0 | 0 | 350 | 0 | 0 |
| `fraba2.chasseur.2.2` | Barracks 18c chasseur protection +1 (lvl 3) | 3 | 1 | 15.62 | 12060 | 0 | 0 | 1350 | 0 | 0 |
| `fraba2.chasseur.2.3` | Barracks 18c chasseur protection +1 (lvl 4) | 4 | 1 | 15.62 | 36706 | 0 | 0 | 2150 | 0 | 0 |
| `fraba2.chasseur.2.4` | Barracks 18c chasseur protection +1 (lvl 5) | 5 | 1 | 15.62 | 36706 | 0 | 0 | 3350 | 0 | 0 |
| `fraba2.chasseur.2.5` | Barracks 18c chasseur protection +1 (lvl 6) | 6 | 1 | 15.62 | 37060 | 0 | 0 | 1350 | 0 | 0 |
| `fraba2.chasseur.2.6` | Barracks 18c chasseur protection +1 (lvl 7) | 7 | 1 | 15.62 | 16706 | 0 | 0 | 1350 | 0 | 0 |
| `fraba2.drummer18.2.1` | Barracks 18c drummer18 protection +15 (lvl 2) | 2 | 15 | 15.62 | 805 | 0 | 0 | 65 | 0 | 0 |
| `fraba2.grenadier.1.1` | Barracks 18c grenadier damage +2 (lvl 2) | 2 | 2 | 15.62 | 1800 | 0 | 0 | 800 | 0 | 0 |
| `fraba2.grenadier.1.2` | Barracks 18c grenadier damage +3 (lvl 3) | 3 | 3 | 15.62 | 11200 | 0 | 0 | 1750 | 0 | 0 |
| `fraba2.grenadier.1.3` | Barracks 18c grenadier damage +4 (lvl 4) | 4 | 4 | 15.62 | 33000 | 0 | 0 | 2900 | 0 | 0 |
| `fraba2.grenadier.1.4` | Barracks 18c grenadier damage +5 (lvl 5) | 5 | 5 | 15.62 | 42000 | 0 | 0 | 4800 | 0 | 0 |
| `fraba2.grenadier.1.5` | Barracks 18c grenadier damage +6 (lvl 6) | 6 | 6 | 15.62 | 52000 | 0 | 0 | 3800 | 0 | 0 |
| `fraba2.grenadier.1.6` | Barracks 18c grenadier damage +1500 (lvl 7) | 7 | 1500 | 15.62 | 64010 | 0 | 0 | 15200 | 0 | 0 |
| `fraba2.grenadier.2.1` | Barracks 18c grenadier protection +1 (lvl 2) | 2 | 1 | 15.62 | 3506 | 0 | 0 | 220 | 0 | 0 |
| `fraba2.grenadier.2.2` | Barracks 18c grenadier protection +2 (lvl 3) | 3 | 2 | 15.62 | 11250 | 0 | 0 | 1450 | 0 | 0 |
| `fraba2.grenadier.2.3` | Barracks 18c grenadier protection +3 (lvl 4) | 4 | 3 | 15.62 | 37200 | 0 | 0 | 3300 | 0 | 0 |
| `fraba2.grenadier.2.4` | Barracks 18c grenadier protection +1 (lvl 5) | 5 | 1 | 15.62 | 40400 | 0 | 0 | 3050 | 0 | 0 |
| `fraba2.grenadier.2.5` | Barracks 18c grenadier protection +2 (lvl 6) | 6 | 2 | 15.62 | 22060 | 0 | 0 | 350 | 0 | 0 |
| `fraba2.grenadier.2.6` | Barracks 18c grenadier protection +3 (lvl 7) | 7 | 3 | 15.62 | 63900 | 0 | 0 | 2350 | 0 | 0 |
| `fraba2.musketeer18.1.1` | Barracks 18c musketeer18 damage +1 (lvl 2) | 2 | 1 | 15.62 | 500 | 0 | 0 | 200 | 0 | 0 |
| `fraba2.musketeer18.1.2` | Barracks 18c musketeer18 damage +1 (lvl 3) | 3 | 1 | 15.62 | 2000 | 0 | 0 | 400 | 0 | 0 |
| `fraba2.musketeer18.1.3` | Barracks 18c musketeer18 damage +2 (lvl 4) | 4 | 2 | 15.62 | 1200 | 0 | 0 | 1800 | 0 | 0 |
| `fraba2.musketeer18.1.4` | Barracks 18c musketeer18 damage +2 (lvl 5) | 5 | 2 | 15.62 | 3300 | 0 | 0 | 100 | 0 | 0 |
| `fraba2.musketeer18.1.5` | Barracks 18c musketeer18 damage +3 (lvl 6) | 6 | 3 | 15.62 | 1100 | 0 | 0 | 200 | 0 | 0 |
| `fraba2.musketeer18.1.6` | Barracks 18c musketeer18 damage +3 (lvl 7) | 7 | 3 | 15.62 | 5500 | 0 | 0 | 2100 | 0 | 0 |
| `fraba2.musketeer18.2.1` | Barracks 18c musketeer18 protection +1 (lvl 2) | 2 | 1 | 15.62 | 3500 | 0 | 0 | 370 | 0 | 0 |
| `fraba2.musketeer18.2.2` | Barracks 18c musketeer18 protection +2 (lvl 3) | 3 | 2 | 15.62 | 35030 | 0 | 0 | 1050 | 0 | 0 |
| `fraba2.musketeer18.2.3` | Barracks 18c musketeer18 protection +2 (lvl 4) | 4 | 2 | 15.62 | 11706 | 0 | 0 | 4300 | 0 | 0 |
| `fraba2.musketeer18.2.4` | Barracks 18c musketeer18 protection +1 (lvl 5) | 5 | 1 | 15.62 | 36700 | 0 | 0 | 4450 | 0 | 0 |
| `fraba2.musketeer18.2.5` | Barracks 18c musketeer18 protection +2 (lvl 6) | 6 | 2 | 15.62 | 30160 | 0 | 0 | 1550 | 0 | 0 |
| `fraba2.musketeer18.2.6` | Barracks 18c musketeer18 protection +2 (lvl 7) | 7 | 2 | 15.62 | 33600 | 0 | 0 | 1150 | 0 | 0 |
| `fraba2.officer18.1.1` | Barracks 18c officer18 damage +30 (lvl 2) | 2 | 30 | 15.62 | 1200 | 0 | 0 | 700 | 0 | 0 |
| `fraba2.officer18.2.1` | Barracks 18c officer18 protection +12 (lvl 2) | 2 | 12 | 15.62 | 2105 | 0 | 0 | 450 | 0 | 0 |
| `fraba2.pikeman18.1.1` | Barracks 18c pikeman18 damage +2 (lvl 2) | 2 | 2 | 15.62 | 2000 | 0 | 0 | 800 | 0 | 0 |
| `fraba2.pikeman18.1.2` | Barracks 18c pikeman18 damage +2 (lvl 3) | 3 | 2 | 15.62 | 8000 | 0 | 0 | 1200 | 0 | 0 |
| `fraba2.pikeman18.1.3` | Barracks 18c pikeman18 damage +2 (lvl 4) | 4 | 2 | 15.62 | 20000 | 0 | 0 | 2500 | 0 | 0 |
| `fraba2.pikeman18.1.4` | Barracks 18c pikeman18 damage +2 (lvl 5) | 5 | 2 | 15.62 | 32000 | 0 | 0 | 2800 | 0 | 0 |
| `fraba2.pikeman18.1.5` | Barracks 18c pikeman18 damage +2 (lvl 6) | 6 | 2 | 15.62 | 32000 | 0 | 0 | 3800 | 0 | 0 |
| `fraba2.pikeman18.1.6` | Barracks 18c pikeman18 damage +2 (lvl 7) | 7 | 2 | 15.62 | 40500 | 0 | 0 | 4800 | 0 | 0 |
| `fraba2.pikeman18.2.1` | Barracks 18c pikeman18 protection +2 (lvl 2) | 2 | 2 | 15.62 | 1500 | 0 | 0 | 500 | 0 | 0 |
| `fraba2.pikeman18.2.2` | Barracks 18c pikeman18 protection +3 (lvl 3) | 3 | 3 | 15.62 | 7000 | 0 | 0 | 1500 | 0 | 0 |
| `fraba2.pikeman18.2.3` | Barracks 18c pikeman18 protection +2 (lvl 4) | 4 | 2 | 15.62 | 37000 | 0 | 0 | 2000 | 0 | 0 |
| `fraba2.pikeman18.2.4` | Barracks 18c pikeman18 protection +3 (lvl 5) | 5 | 3 | 15.62 | 37000 | 0 | 0 | 5500 | 0 | 0 |
| `fraba2.pikeman18.2.5` | Barracks 18c pikeman18 protection +2 (lvl 6) | 6 | 2 | 15.62 | 37000 | 0 | 0 | 5500 | 0 | 0 |
| `fraba2.pikeman18.2.6` | Barracks 18c pikeman18 protection +3 (lvl 7) | 7 | 3 | 15.62 | 64600 | 0 | 0 | 5500 | 0 | 0 |
| `frabar.1` | — | 1 | 140 | 15.62 | 750 | 0 | 0 | 250 | 0 | 0 |
| `frabar.2` | — | 2 | 180 | 15.62 | 25600 | 0 | 0 | 3350 | 2000 | 0 |
| `frabar.drummer.2.1` | Barracks 17c drummer protection +12 (lvl 2) | 2 | 12 | 15.62 | 500 | 0 | 0 | 75 | 0 | 0 |
| `frabar.musketeer.1.1` | Barracks 17c musketeer damage +1 (lvl 2) | 2 | 1 | 15.62 | 100 | 0 | 0 | 50 | 0 | 0 |
| `frabar.musketeer.1.2` | Barracks 17c musketeer damage +1 (lvl 3) | 3 | 1 | 15.62 | 3000 | 0 | 0 | 500 | 0 | 0 |
| `frabar.musketeer.1.3` | Barracks 17c musketeer damage +2 (lvl 4) | 4 | 2 | 15.62 | 2500 | 0 | 0 | 750 | 0 | 0 |
| `frabar.musketeer.2.1` | Barracks 17c musketeer protection +1 (lvl 2) | 2 | 1 | 15.62 | 200 | 0 | 0 | 75 | 200 | 0 |
| `frabar.musketeer.2.2` | Barracks 17c musketeer protection +2 (lvl 3) | 3 | 2 | 15.62 | 705 | 0 | 0 | 250 | 250 | 0 |
| `frabar.musketeer.2.3` | Barracks 17c musketeer protection +2 (lvl 4) | 4 | 2 | 15.62 | 2560 | 0 | 0 | 300 | 450 | 0 |
| `frabar.musketeer.2.4` | Barracks 17c musketeer protection +1 (lvl 5) | 5 | 1 | 15.62 | 1556 | 0 | 0 | 550 | 100 | 0 |
| `frabar.musketeer.2.5` | Barracks 17c musketeer protection +2 (lvl 6) | 6 | 2 | 15.62 | 1060 | 0 | 0 | 850 | 400 | 0 |
| `frabar.musketeer.2.6` | Barracks 17c musketeer protection +2 (lvl 7) | 7 | 2 | 15.62 | 3700 | 0 | 0 | 650 | 700 | 0 |
| `frabar.officer.1.1` | Barracks 17c officer damage +20 (lvl 2) | 2 | 20 | 15.62 | 200 | 0 | 0 | 25 | 0 | 0 |
| `frabar.officer.2.1` | Barracks 17c officer protection +6 (lvl 2) | 2 | 6 | 15.62 | 1950 | 0 | 0 | 350 | 0 | 0 |
| `frabar.pikeman.1.1` | Barracks 17c pikeman damage +1 (lvl 2) | 2 | 1 | 15.62 | 100 | 0 | 0 | 25 | 0 | 0 |
| `frabar.pikeman.1.2` | Barracks 17c pikeman damage +2 (lvl 3) | 3 | 2 | 15.62 | 1400 | 0 | 0 | 325 | 0 | 0 |
| `frabar.pikeman.1.3` | Barracks 17c pikeman damage +2 (lvl 4) | 4 | 2 | 15.62 | 4600 | 0 | 0 | 650 | 0 | 0 |
| `frabar.pikeman.1.4` | Barracks 17c pikeman damage +1 (lvl 5) | 5 | 1 | 15.62 | 6200 | 0 | 0 | 1650 | 0 | 0 |
| `frabar.pikeman.1.5` | Barracks 17c pikeman damage +2 (lvl 6) | 6 | 2 | 15.62 | 15300 | 0 | 0 | 2075 | 0 | 0 |
| `frabar.pikeman.1.6` | — | 7 | 2 | 15.62 | 15000 | 0 | 0 | 1875 | 0 | 0 |
| `frabar.pikeman.2.1` | Barracks 17c pikeman protection +1 (lvl 2) | 2 | 1 | 15.62 | 350 | 0 | 0 | 90 | 0 | 0 |
| `frabar.pikeman.2.2` | Barracks 17c pikeman protection +1 (lvl 3) | 3 | 1 | 15.62 | 1000 | 0 | 0 | 135 | 0 | 0 |
| `frabar.pikeman.2.3` | Barracks 17c pikeman protection +2 (lvl 4) | 4 | 2 | 15.62 | 4200 | 0 | 0 | 500 | 0 | 0 |
| `frabar.pikeman.2.4` | Barracks 17c pikeman protection +1 (lvl 5) | 5 | 1 | 15.62 | 11075 | 0 | 0 | 310 | 0 | 0 |
| `frabar.pikeman.2.5` | Barracks 17c pikeman protection +1 (lvl 6) | 6 | 1 | 15.62 | 15050 | 0 | 0 | 3050 | 0 | 0 |
| `frabar.pikeman.2.6` | — | 7 | 2 | 15.62 | 11250 | 0 | 0 | 1500 | 0 | 0 |
| `frabla.1` | Manufacture agricultural equipment (field capacity +100%) | 1 | 100 | 15.62 | 0 | 400 | 0 | 90 | 0 | 0 |
| `frabla.2` | Forge metal armature and gratings (building defence +50) | 1 | 50 | 15.62 | 0 | 0 | 12320 | 350 | 900 | 0 |
| `frabla.3` | Forge harnesses for horses (mounted units recruitment speed -33%) | 1 | -3333333 | 15.62 | 0 | 0 | 0 | 3650 | 5300 | 8200 |
| `frabla.4` | Forge bayonets and broadswords for infantry (18c musketeer/grenadier melee attack +5) | 1 | 5 | 15.62 | 0 | 1300 | 0 | 1500 | 900 | 5000 |
| `frabla.5` | Forge new types of broadswords and sabres (cavalry and sword clansman attack +5) | 1 | 5 | 15.62 | 0 | 0 | 0 | 4000 | 7900 | 0 |
| `frabla.6` | Forge new cuirasses (armoured soldiers defence +2) | 1 | 2 | 15.62 | 0 | 0 | 0 | 4950 | 10500 | 0 |
| `fracen.1` | — | 1 | 0 | 9.38 | 40000 | 0 | 0 | 3500 | 4000 | 4000 |
| `frasta.cuirassier.1.1` | Stable cuirassier damage +1 (lvl 2) | 2 | 1 | 15.62 | 32000 | 0 | 0 | 600 | 0 | 0 |
| `frasta.cuirassier.1.2` | Stable cuirassier damage +1 (lvl 3) | 3 | 1 | 15.62 | 12000 | 0 | 0 | 2200 | 0 | 0 |
| `frasta.cuirassier.1.3` | Stable cuirassier damage +1 (lvl 4) | 4 | 1 | 15.62 | 62000 | 0 | 0 | 1300 | 0 | 0 |
| `frasta.cuirassier.1.4` | Stable cuirassier damage +2 (lvl 5) | 5 | 2 | 15.62 | 57000 | 0 | 0 | 3150 | 0 | 0 |
| `frasta.cuirassier.1.5` | Stable cuirassier damage +2 (lvl 6) | 6 | 2 | 15.62 | 61055 | 0 | 0 | 8100 | 0 | 0 |
| `frasta.cuirassier.1.6` | Stable cuirassier damage +3 (lvl 7) | 7 | 3 | 15.62 | 47150 | 0 | 0 | 4020 | 0 | 0 |
| `frasta.cuirassier.2.1` | Stable cuirassier protection +2 (lvl 2) | 2 | 2 | 15.62 | 1520 | 0 | 0 | 750 | 1000 | 0 |
| `frasta.cuirassier.2.2` | Stable cuirassier protection +3 (lvl 3) | 3 | 3 | 15.62 | 3200 | 0 | 0 | 350 | 1950 | 0 |
| `frasta.cuirassier.2.3` | Stable cuirassier protection +3 (lvl 4) | 4 | 3 | 15.62 | 7600 | 0 | 0 | 300 | 3110 | 0 |
| `frasta.cuirassier.2.4` | Stable cuirassier protection +2 (lvl 5) | 5 | 2 | 15.62 | 6200 | 0 | 0 | 6200 | 100 | 0 |
| `frasta.cuirassier.2.5` | Stable cuirassier protection +1 (lvl 6) | 6 | 1 | 15.62 | 11700 | 0 | 0 | 4450 | 7000 | 0 |
| `frasta.cuirassier.2.6` | Stable cuirassier protection +1 (lvl 7) | 7 | 1 | 15.62 | 9700 | 0 | 0 | 3244 | 5060 | 0 |
| `frasta.dragoon.1.1` | Stable dragoon damage +1 (lvl 2) | 2 | 1 | 15.62 | 500 | 0 | 0 | 150 | 0 | 0 |
| `frasta.dragoon.1.2` | Stable dragoon damage +1 (lvl 3) | 3 | 1 | 15.62 | 700 | 0 | 0 | 200 | 0 | 0 |
| `frasta.dragoon.1.3` | Stable dragoon damage +2 (lvl 4) | 4 | 2 | 15.62 | 900 | 0 | 0 | 340 | 0 | 0 |
| `frasta.dragoon.1.4` | Stable dragoon damage +1 (lvl 5) | 5 | 1 | 15.62 | 0 | 0 | 0 | 0 | 0 | 0 |
| `frasta.dragoon.1.5` | Stable dragoon damage +1 (lvl 6) | 6 | 1 | 15.62 | 0 | 0 | 0 | 0 | 0 | 0 |
| `frasta.dragoon.1.6` | Stable dragoon damage +3 (lvl 7) | 7 | 3 | 15.62 | 0 | 0 | 0 | 0 | 0 | 0 |
| `frasta.dragoon.2.1` | Stable dragoon protection +1 (lvl 2) | 2 | 1 | 15.62 | 900 | 0 | 0 | 150 | 0 | 0 |
| `frasta.dragoon.2.2` | Stable dragoon protection +2 (lvl 3) | 3 | 2 | 15.62 | 6600 | 0 | 0 | 750 | 0 | 0 |
| `frasta.dragoon.2.3` | Stable dragoon protection +2 (lvl 4) | 4 | 2 | 15.62 | 5000 | 0 | 0 | 1250 | 0 | 0 |
| `frasta.dragoon.2.4` | Stable dragoon protection +1 (lvl 5) | 5 | 1 | 15.62 | 3000 | 0 | 0 | 700 | 0 | 0 |
| `frasta.dragoon.2.5` | Stable dragoon protection +2 (lvl 6) | 6 | 2 | 15.62 | 1000 | 0 | 0 | 2350 | 0 | 0 |
| `frasta.dragoon.2.6` | Stable dragoon protection +2 (lvl 7) | 7 | 2 | 15.62 | 6001 | 0 | 0 | 5000 | 0 | 0 |
| `frasta.dragoon18fra.1.1` | Stable dragoon18fra damage +2 (lvl 2) | 2 | 2 | 15.62 | 2000 | 0 | 0 | 100 | 0 | 0 |
| `frasta.dragoon18fra.1.2` | Stable dragoon18fra damage +2 (lvl 3) | 3 | 2 | 15.62 | 9000 | 0 | 0 | 350 | 0 | 0 |
| `frasta.dragoon18fra.1.3` | Stable dragoon18fra damage +4 (lvl 4) | 4 | 4 | 15.62 | 12000 | 0 | 0 | 400 | 0 | 0 |
| `frasta.dragoon18fra.1.4` | Stable dragoon18fra damage +2 (lvl 5) | 5 | 2 | 15.62 | 23000 | 0 | 0 | 580 | 0 | 0 |
| `frasta.dragoon18fra.1.5` | Stable dragoon18fra damage +2 (lvl 6) | 6 | 2 | 15.62 | 32000 | 0 | 0 | 680 | 0 | 0 |
| `frasta.dragoon18fra.1.6` | Stable dragoon18fra damage +4 (lvl 7) | 7 | 4 | 15.62 | 42000 | 0 | 0 | 780 | 0 | 0 |
| `frasta.dragoon18fra.2.1` | Stable dragoon18fra protection +1 (lvl 2) | 2 | 1 | 15.62 | 760 | 0 | 0 | 935 | 0 | 0 |
| `frasta.dragoon18fra.2.2` | Stable dragoon18fra protection +2 (lvl 3) | 3 | 2 | 15.62 | 1260 | 0 | 0 | 1150 | 0 | 0 |
| `frasta.dragoon18fra.2.3` | Stable dragoon18fra protection +2 (lvl 4) | 4 | 2 | 15.62 | 15600 | 0 | 0 | 2350 | 0 | 0 |
| `frasta.dragoon18fra.2.4` | Stable dragoon18fra protection +1 (lvl 5) | 5 | 1 | 15.62 | 17600 | 0 | 0 | 3350 | 0 | 0 |
| `frasta.dragoon18fra.2.5` | Stable dragoon18fra protection +2 (lvl 6) | 6 | 2 | 15.62 | 19600 | 0 | 0 | 5350 | 0 | 0 |
| `frasta.dragoon18fra.2.6` | Stable dragoon18fra protection +2 (lvl 7) | 7 | 2 | 15.62 | 21760 | 0 | 0 | 9350 | 0 | 0 |
| `frasta.hussar.1.1` | Stable hussar damage +1 (lvl 2) | 2 | 1 | 15.62 | 0 | 0 | 0 | 800 | 200 | 0 |
| `frasta.hussar.1.2` | Stable hussar damage +2 (lvl 3) | 3 | 2 | 15.62 | 0 | 0 | 0 | 4800 | 2800 | 0 |
| `frasta.hussar.1.3` | Stable hussar damage +3 (lvl 4) | 4 | 3 | 15.62 | 25200 | 0 | 0 | 0 | 2500 | 0 |
| `frasta.hussar.1.4` | Stable hussar damage +4 (lvl 5) | 5 | 4 | 15.62 | 27000 | 0 | 0 | 0 | 2500 | 0 |
| `frasta.hussar.1.5` | Stable hussar damage +1 (lvl 6) | 6 | 1 | 15.62 | 46200 | 0 | 0 | 0 | 4300 | 0 |
| `frasta.hussar.1.6` | Stable hussar damage +1 (lvl 7) | 7 | 1 | 15.62 | 21000 | 0 | 0 | 0 | 5200 | 0 |
| `frasta.hussar.2.1` | Stable hussar protection +1 (lvl 2) | 2 | 1 | 15.62 | 760 | 0 | 0 | 1350 | 0 | 0 |
| `frasta.hussar.2.2` | Stable hussar protection +1 (lvl 3) | 3 | 1 | 15.62 | 2900 | 0 | 0 | 2350 | 0 | 0 |
| `frasta.hussar.2.3` | Stable hussar protection +1 (lvl 4) | 4 | 1 | 15.62 | 4600 | 0 | 0 | 5350 | 0 | 0 |
| `frasta.hussar.2.4` | Stable hussar protection +2 (lvl 5) | 5 | 2 | 15.62 | 4000 | 0 | 0 | 8350 | 0 | 0 |
| `frasta.hussar.2.5` | Stable hussar protection +2 (lvl 6) | 6 | 2 | 15.62 | 7000 | 0 | 0 | 15350 | 0 | 0 |
| `frasta.hussar.2.6` | Stable hussar protection +3 (lvl 7) | 7 | 3 | 15.62 | 51000 | 0 | 0 | 20150 | 0 | 0 |
| `frasta.kingmusketeer.1.1` | Stable kingmusketeer damage +20 (lvl 2) | 2 | 20 | 15.62 | 7000 | 0 | 0 | 2500 | 0 | 0 |
| `frasta.kingmusketeer.2.1` | Stable kingmusketeer protection +12 (lvl 2) | 2 | 12 | 15.62 | 2000 | 0 | 0 | 1350 | 0 | 0 |
| `frasta.kingmusketeer.2.2` | Stable kingmusketeer protection +1 (lvl 3) | 3 | 1 | 15.62 | 0 | 0 | 0 | 0 | 0 | 0 |
| `frasta.kingmusketeer.2.3` | Stable kingmusketeer protection +2 (lvl 4) | 4 | 2 | 15.62 | 0 | 0 | 0 | 0 | 0 | 0 |
| `frasta.kingmusketeer.2.4` | Stable kingmusketeer protection +2 (lvl 5) | 5 | 2 | 15.62 | 0 | 0 | 0 | 0 | 0 | 0 |
| `frasta.kingmusketeer.2.5` | Stable kingmusketeer protection +2 (lvl 6) | 6 | 2 | 15.62 | 0 | 0 | 0 | 0 | 0 | 0 |
| `frasta.kingmusketeer.2.6` | Stable kingmusketeer protection +2 (lvl 7) | 7 | 2 | 15.62 | 0 | 0 | 0 | 0 | 0 | 0 |
| `frasta.reiter.1.1` | Stable reiter damage +1 (lvl 2) | 2 | 1 | 15.62 | 900 | 0 | 0 | 100 | 0 | 0 |
| `frasta.reiter.1.2` | Stable reiter damage +2 (lvl 3) | 3 | 2 | 15.62 | 500 | 0 | 0 | 280 | 0 | 0 |
| `frasta.reiter.1.3` | Stable reiter damage +1 (lvl 4) | 4 | 1 | 15.62 | 4400 | 0 | 0 | 220 | 0 | 0 |
| `frasta.reiter.1.4` | Stable reiter damage +1 (lvl 5) | 5 | 1 | 15.62 | 3050 | 0 | 0 | 320 | 0 | 0 |
| `frasta.reiter.1.5` | Stable reiter damage +1 (lvl 6) | 6 | 1 | 15.62 | 2030 | 0 | 0 | 800 | 0 | 0 |
| `frasta.reiter.1.6` | Stable reiter damage +1 (lvl 7) | 7 | 1 | 15.62 | 7000 | 0 | 0 | 1600 | 0 | 0 |
| `frasta.reiter.2.1` | Stable reiter protection +2 (lvl 2) | 2 | 2 | 15.62 | 600 | 0 | 0 | 135 | 400 | 0 |
| `frasta.reiter.2.2` | Stable reiter protection +3 (lvl 3) | 3 | 3 | 15.62 | 200 | 0 | 0 | 200 | 300 | 0 |
| `frasta.reiter.2.3` | Stable reiter protection +3 (lvl 4) | 4 | 3 | 15.62 | 800 | 0 | 0 | 100 | 560 | 0 |
| `frasta.reiter.2.4` | Stable reiter protection +2 (lvl 5) | 5 | 2 | 15.62 | 3200 | 0 | 0 | 300 | 300 | 0 |
| `frasta.reiter.2.5` | Stable reiter protection +1 (lvl 6) | 6 | 1 | 15.62 | 1600 | 0 | 0 | 350 | 650 | 0 |
| `frasta.reiter.2.6` | Stable reiter protection +1 (lvl 7) | 7 | 1 | 15.62 | 15700 | 0 | 0 | 1000 | 5000 | 0 |
| `ukrwwa.1` | — | 2 | 5 | 0.03 | 0 | 400 | 0 | 0 | 0 | 0 |

### eng — England

| sid | имя (EN) | level | value | время (s) | F | W | S | G | I | C |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `engaca.1` | Cultivate new cultures of wheat (harvesting +40%) | 1 | 40 | 15.62 | 0 | 200 | 0 | 325 | 0 | 0 |
| `engaca.10` | Raise builders' salary (building construction time -75%) | 1 | -7500000 | 15.62 | 0 | 0 | 0 | 6950 | 0 | 0 |
| `engaca.11` | Research new fortification grades (durability of walls and towers +80) | 1 | 80 | 15.62 | 0 | 0 | 16200 | 1500 | 0 | 0 |
| `engaca.12` | Improve firearms: rifled barrel (fire power +10%) | 1 | 10 | 15.62 | 0 | 0 | 0 | 0 | 5000 | 0 |
| `engaca.13` | Research granular gunpowder (fire power +10%) | 1 | 10 | 15.62 | 0 | 0 | 0 | 4000 | 0 | 0 |
| `engaca.14` | Research new sulphur purification methods (fire power +15%) | 1 | 15 | 15.62 | 0 | 0 | 0 | 7000 | 0 | 0 |
| `engaca.15` | Research new nitre purification methods (fire power +25%) | 1 | 25 | 15.62 | 0 | 0 | 0 | 0 | 0 | 11000 |
| `engaca.16` | Research improved additions to gunpowder formula (artillery range +5%) | 1 | 5 | 15.62 | 0 | 0 | 0 | 2000 | 12150 | 0 |
| `engaca.17` | Design new barrel types: unicorn, carronade (artillery range +10%) | 1 | 10 | 15.62 | 0 | 0 | 3000 | 4550 | 19200 | 0 |
| `engaca.18` | Design more durable gun carriage: Gribovalle system (artillery durability +50%) | 1 | 50 | 15.62 | 0 | 0 | 0 | 500 | 3830 | 1500 |
| `engaca.19` | Design multi-barrelled cannon | 1 | 0 | 15.62 | 0 | 0 | 0 | 1500 | 0 | 2500 |
| `engaca.2` | Cultivate new cultures of rye (harvesting +50%) | 1 | 50 | 15.62 | 0 | 2400 | 0 | 625 | 0 | 0 |
| `engaca.20` | Research new sighting devices for artillery (artillery accuracy +35%) | 1 | -35 | 15.62 | 0 | 3540 | 0 | 2000 | 0 | 7250 |
| `engaca.21` | Finance artillery repair shops (repair all artillery) | 1 | 25 | 15.62 | 0 | 350 | 0 | 100 | 0 | 250 |
| `engaca.22` | Develop geology (previously hidden deposits appear on the map) | 1 | 0 | 15.62 | 0 | 0 | 0 | 250 | 0 | 0 |
| `engaca.23` | Develop mining (stone excavation efficiency +100%) | 1 | 100 | 15.62 | 0 | 0 | 0 | 1550 | 3000 | 0 |
| `engaca.24` | Raise miners' salary (stone excavation efficiency +200%) | 1 | 200 | 15.62 | 4200 | 0 | 0 | 1550 | 0 | 12520 |
| `engaca.25` | Design Montgolfier (reveals the whole map) | 1 | 0 | 15.62 | 0 | 0 | 0 | 5750 | 0 | 0 |
| `engaca.26` | Develop medical science (heals all live units) | 1 | 50 | 31.25 | 0 | 0 | 0 | 200 | 0 | 200 |
| `engaca.27` | Develop mathematics (artillery accuracy +35%) | 1 | -35 | 15.62 | 0 | 9540 | 0 | 12000 | 0 | 65200 |
| `engaca.28` | Design new rigging types (ship speed +40%) | 1 | 40 | 15.62 | 0 | 53400 | 0 | 22050 | 0 | 0 |
| `engaca.29` | Design new rib system and new hulls (battleship construction) | 1 | 0 | 15.62 | 0 | 22300 | 0 | 6800 | 7500 | 13200 |
| `engaca.3` | Raise agriculturists' salary (harvesting +50%) | 1 | 50 | 15.62 | 0 | 3600 | 0 | 850 | 0 | 0 |
| `engaca.30` | Train carpenters (shipbuilding speed x10) | 1 | -5000000 | 15.62 | 0 | 2300 | 42700 | 1150 | 0 | 0 |
| `engaca.31` | Design wheellock (rate of fire +30%) | 1 | -30 | 15.62 | 0 | 0 | 6000 | 5500 | 4200 | 0 |
| `engaca.32` | Design flintlock (musket cost -50%) | 1 | 0 | 15.62 | 0 | 0 | 0 | 6050 | 0 | 7750 |
| `engaca.33` | Design paper cartridge and iron ramrod (rate of fire +30%) | 1 | -30 | 15.62 | 0 | 5000 | 0 | 5500 | 0 | 15200 |
| `engaca.34` | Research improved steel grades for cuirasses (armoured soldier defence +2) | 1 | 2 | 15.62 | 0 | 0 | 0 | 9750 | 0 | 0 |
| `engaca.35` | Design bayonet: barrel-inserted, bayonet with a tube (cold steel weapons +5) | 1 | 5 | 15.62 | 0 | 0 | 0 | 11500 | 0 | 0 |
| `engaca.36` | Research new steel grades (18c musketeer/grenadier melee attack efficiency +25%) | 1 | 25 | 15.62 | 0 | 0 | 0 | 19500 | 0 | 0 |
| `engaca.4` | Carry out field melioration (field capacity +200%) | 1 | 200 | 15.62 | 0 | 1000 | 0 | 475 | 0 | 0 |
| `engaca.5` | Design new tackle and fishing nets (boat efficiency +100%) | 1 | 100 | 15.62 | 0 | 12400 | 0 | 3520 | 0 | 0 |
| `engaca.6` | Develop new woodworking methods (frigate building) | 1 | 0 | 15.62 | 0 | 12400 | 0 | 7040 | 0 | 0 |
| `engaca.7` | Build new shipyards for fishing boats (fishing boat cost -85%) | 1 | 0 | 15.62 | 0 | 7300 | 0 | 1220 | 0 | 0 |
| `engaca.8` | Design new woodworking tools (woodcutting efficiency +100%) | 1 | 100 | 15.62 | 5500 | 0 | 0 | 550 | 0 | 0 |
| `engaca.9` | Use new construction materials (durability of buildings +85) | 1 | 85 | 15.62 | 0 | 9400 | 7850 | 1150 | 0 | 0 |
| `engart.cannon.1.1` | — | 2 | — | 10.0 | 0 | 1000 | 500 | 300 | 0 | 0 |
| `engart.cannon.1.2` | — | 3 | — | 10.0 | 0 | 3000 | 1000 | 500 | 0 | 0 |
| `engart.cannon.1.3` | — | 4 | — | 10.0 | 0 | 6000 | 2000 | 1000 | 0 | 0 |
| `engart.cannon.1.4` | — | 5 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `engart.cannon.1.5` | — | 6 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `engart.cannon.1.6` | — | 7 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `engart.cannon.2.1` | — | 2 | -2500000 | 10.0 | 0 | 0 | 0 | 500 | 1000 | 0 |
| `engart.cannon.2.2` | — | 3 | -2500000 | 10.0 | 0 | 0 | 0 | 1000 | 2000 | 0 |
| `engart.cannon.2.3` | — | 4 | -2500000 | 10.0 | 0 | 0 | 0 | 2000 | 3000 | 0 |
| `engart.cannon.2.4` | — | 5 | -2000000 | 15.62 | 2560 | 0 | 0 | 0 | 0 | 0 |
| `engart.cannon.2.5` | — | 6 | -2000000 | 15.62 | 3560 | 0 | 0 | 0 | 0 | 0 |
| `engart.cannon.2.6` | — | 7 | -2000000 | 15.62 | 5560 | 0 | 0 | 0 | 0 | 0 |
| `engart.howitzer.1.1` | — | 2 | — | 10.0 | 0 | 1000 | 500 | 300 | 0 | 0 |
| `engart.howitzer.1.2` | — | 3 | — | 10.0 | 0 | 3000 | 1000 | 500 | 0 | 0 |
| `engart.howitzer.1.3` | — | 4 | — | 10.0 | 0 | 6000 | 2000 | 1000 | 0 | 0 |
| `engart.howitzer.1.4` | — | 5 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `engart.howitzer.1.5` | — | 6 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `engart.howitzer.1.6` | — | 7 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `engart.howitzer.2.1` | — | 2 | -2500000 | 10.0 | 0 | 0 | 0 | 500 | 1000 | 0 |
| `engart.howitzer.2.2` | — | 3 | -2500000 | 10.0 | 0 | 0 | 0 | 1000 | 2000 | 0 |
| `engart.howitzer.2.3` | — | 4 | -2500000 | 10.0 | 0 | 0 | 0 | 2000 | 3000 | 0 |
| `engart.howitzer.2.4` | — | 5 | -2000000 | 31.25 | 2560 | 0 | 0 | 0 | 0 | 0 |
| `engart.howitzer.2.5` | — | 6 | -2000000 | 31.25 | 3560 | 0 | 0 | 0 | 0 | 0 |
| `engart.howitzer.2.6` | — | 7 | -2000000 | 31.25 | 5560 | 0 | 0 | 0 | 0 | 0 |
| `engba2.1` | — | 1 | 140 | 15.62 | 750 | 0 | 0 | 250 | 0 | 0 |
| `engba2.2` | — | 2 | 180 | 15.62 | 25600 | 0 | 0 | 3350 | 2000 | 0 |
| `engba2.bagpiper.2.1` | Barracks 18c bagpiper protection +10 (lvl 2) | 2 | 10 | 15.62 | 555 | 0 | 0 | 90 | 0 | 0 |
| `engba2.grenadier.1.1` | Barracks 18c grenadier damage +2 (lvl 2) | 2 | 2 | 15.62 | 1000 | 0 | 0 | 1300 | 0 | 0 |
| `engba2.grenadier.1.2` | Barracks 18c grenadier damage +3 (lvl 3) | 3 | 3 | 15.62 | 10000 | 0 | 0 | 1900 | 0 | 0 |
| `engba2.grenadier.1.3` | Barracks 18c grenadier damage +4 (lvl 4) | 4 | 4 | 15.62 | 22000 | 0 | 0 | 2900 | 0 | 0 |
| `engba2.grenadier.1.4` | Barracks 18c grenadier damage +5 (lvl 5) | 5 | 5 | 15.62 | 52000 | 0 | 0 | 3700 | 0 | 0 |
| `engba2.grenadier.1.5` | Barracks 18c grenadier damage +6 (lvl 6) | 6 | 6 | 15.62 | 52000 | 0 | 0 | 4800 | 0 | 0 |
| `engba2.grenadier.1.6` | Barracks 18c grenadier damage +1500 (lvl 7) | 7 | 1500 | 15.62 | 60000 | 0 | 0 | 16000 | 0 | 0 |
| `engba2.grenadier.2.1` | Barracks 18c grenadier protection +1 (lvl 2) | 2 | 1 | 15.62 | 3250 | 0 | 0 | 450 | 0 | 0 |
| `engba2.grenadier.2.2` | Barracks 18c grenadier protection +2 (lvl 3) | 3 | 2 | 15.62 | 11030 | 0 | 0 | 1350 | 0 | 0 |
| `engba2.grenadier.2.3` | Barracks 18c grenadier protection +3 (lvl 4) | 4 | 3 | 15.62 | 36200 | 0 | 0 | 2500 | 0 | 0 |
| `engba2.grenadier.2.4` | Barracks 18c grenadier protection +1 (lvl 5) | 5 | 1 | 15.62 | 16600 | 0 | 0 | 3650 | 0 | 0 |
| `engba2.grenadier.2.5` | Barracks 18c grenadier protection +2 (lvl 6) | 6 | 2 | 15.62 | 60060 | 0 | 0 | 1050 | 0 | 0 |
| `engba2.grenadier.2.6` | Barracks 18c grenadier protection +3 (lvl 7) | 7 | 3 | 15.62 | 64000 | 0 | 0 | 1650 | 0 | 0 |
| `engba2.highlander.1.1` | Barracks 18c highlander damage +1 (lvl 2) | 2 | 1 | 15.62 | 4000 | 0 | 0 | 750 | 0 | 0 |
| `engba2.highlander.1.2` | Barracks 18c highlander damage +2 (lvl 3) | 3 | 2 | 15.62 | 3000 | 0 | 0 | 1100 | 0 | 0 |
| `engba2.highlander.1.3` | Barracks 18c highlander damage +3 (lvl 4) | 4 | 3 | 15.62 | 7500 | 0 | 0 | 1700 | 0 | 0 |
| `engba2.highlander.1.4` | Barracks 18c highlander damage +1 (lvl 5) | 5 | 1 | 15.62 | 11000 | 0 | 0 | 400 | 0 | 0 |
| `engba2.highlander.1.5` | Barracks 18c highlander damage +1 (lvl 6) | 6 | 1 | 15.62 | 27020 | 0 | 0 | 1150 | 0 | 0 |
| `engba2.highlander.1.6` | Barracks 18c highlander damage +1 (lvl 7) | 7 | 1 | 15.62 | 40200 | 0 | 0 | 1220 | 0 | 0 |
| `engba2.highlander.2.1` | Barracks 18c highlander protection +2 (lvl 2) | 2 | 2 | 15.62 | 3006 | 0 | 0 | 400 | 0 | 0 |
| `engba2.highlander.2.2` | Barracks 18c highlander protection +2 (lvl 3) | 3 | 2 | 15.62 | 10020 | 0 | 0 | 1550 | 0 | 0 |
| `engba2.highlander.2.3` | Barracks 18c highlander protection +2 (lvl 4) | 4 | 2 | 15.62 | 35706 | 0 | 0 | 1850 | 0 | 0 |
| `engba2.highlander.2.4` | — | 5 | 3 | 15.62 | 3600 | 0 | 0 | 600 | 0 | 0 |
| `engba2.highlander.2.5` | — | 6 | 3 | 15.62 | 5400 | 0 | 0 | 900 | 0 | 0 |
| `engba2.highlander.2.6` | — | 7 | 3 | 15.62 | 11250 | 0 | 0 | 1875 | 0 | 0 |
| `engba2.musketeer18.1.1` | Barracks 18c musketeer18 damage +1 (lvl 2) | 2 | 1 | 15.62 | 1100 | 0 | 0 | 750 | 0 | 0 |
| `engba2.musketeer18.1.2` | Barracks 18c musketeer18 damage +1 (lvl 3) | 3 | 1 | 15.62 | 1670 | 0 | 0 | 850 | 0 | 0 |
| `engba2.musketeer18.1.3` | Barracks 18c musketeer18 damage +2 (lvl 4) | 4 | 2 | 15.62 | 1900 | 0 | 0 | 200 | 0 | 0 |
| `engba2.musketeer18.1.4` | Barracks 18c musketeer18 damage +2 (lvl 5) | 5 | 2 | 15.62 | 2340 | 0 | 0 | 1800 | 0 | 0 |
| `engba2.musketeer18.1.5` | Barracks 18c musketeer18 damage +3 (lvl 6) | 6 | 3 | 15.62 | 3000 | 0 | 0 | 900 | 0 | 0 |
| `engba2.musketeer18.1.6` | Barracks 18c musketeer18 damage +3 (lvl 7) | 7 | 3 | 15.62 | 3500 | 0 | 0 | 700 | 0 | 0 |
| `engba2.musketeer18.2.1` | Barracks 18c musketeer18 protection +1 (lvl 2) | 2 | 1 | 15.62 | 3750 | 0 | 0 | 370 | 0 | 0 |
| `engba2.musketeer18.2.2` | Barracks 18c musketeer18 protection +2 (lvl 3) | 3 | 2 | 15.62 | 10020 | 0 | 0 | 1450 | 0 | 0 |
| `engba2.musketeer18.2.3` | Barracks 18c musketeer18 protection +2 (lvl 4) | 4 | 2 | 15.62 | 34200 | 0 | 0 | 3850 | 0 | 0 |
| `engba2.musketeer18.2.4` | Barracks 18c musketeer18 protection +1 (lvl 5) | 5 | 1 | 15.62 | 35000 | 0 | 0 | 2350 | 0 | 0 |
| `engba2.musketeer18.2.5` | Barracks 18c musketeer18 protection +2 (lvl 6) | 6 | 2 | 15.62 | 31250 | 0 | 0 | 3350 | 0 | 0 |
| `engba2.musketeer18.2.6` | Barracks 18c musketeer18 protection +2 (lvl 7) | 7 | 2 | 15.62 | 30570 | 0 | 0 | 1450 | 0 | 0 |
| `engba2.officer18.1.1` | Barracks 18c officer18 damage +30 (lvl 2) | 2 | 30 | 15.62 | 800 | 0 | 0 | 950 | 0 | 0 |
| `engba2.officer18.2.1` | Barracks 18c officer18 protection +12 (lvl 2) | 2 | 12 | 15.62 | 2105 | 0 | 0 | 300 | 0 | 0 |
| `engba2.pikeman18.1.1` | Barracks 18c pikeman18 damage +2 (lvl 2) | 2 | 2 | 15.62 | 2000 | 0 | 0 | 800 | 0 | 0 |
| `engba2.pikeman18.1.2` | Barracks 18c pikeman18 damage +2 (lvl 3) | 3 | 2 | 15.62 | 8000 | 0 | 0 | 1200 | 0 | 0 |
| `engba2.pikeman18.1.3` | Barracks 18c pikeman18 damage +2 (lvl 4) | 4 | 2 | 15.62 | 20000 | 0 | 0 | 2500 | 0 | 0 |
| `engba2.pikeman18.1.4` | Barracks 18c pikeman18 damage +2 (lvl 5) | 5 | 2 | 15.62 | 32000 | 0 | 0 | 2800 | 0 | 0 |
| `engba2.pikeman18.1.5` | Barracks 18c pikeman18 damage +2 (lvl 6) | 6 | 2 | 15.62 | 32000 | 0 | 0 | 3800 | 0 | 0 |
| `engba2.pikeman18.1.6` | Barracks 18c pikeman18 damage +2 (lvl 7) | 7 | 2 | 15.62 | 40500 | 0 | 0 | 4800 | 0 | 0 |
| `engba2.pikeman18.2.1` | Barracks 18c pikeman18 protection +2 (lvl 2) | 2 | 2 | 15.62 | 1500 | 0 | 0 | 500 | 0 | 0 |
| `engba2.pikeman18.2.2` | Barracks 18c pikeman18 protection +3 (lvl 3) | 3 | 3 | 15.62 | 7000 | 0 | 0 | 1500 | 0 | 0 |
| `engba2.pikeman18.2.3` | Barracks 18c pikeman18 protection +2 (lvl 4) | 4 | 2 | 15.62 | 37000 | 0 | 0 | 2000 | 0 | 0 |
| `engba2.pikeman18.2.4` | Barracks 18c pikeman18 protection +3 (lvl 5) | 5 | 3 | 15.62 | 37000 | 0 | 0 | 5500 | 0 | 0 |
| `engba2.pikeman18.2.5` | Barracks 18c pikeman18 protection +2 (lvl 6) | 6 | 2 | 15.62 | 37000 | 0 | 0 | 5500 | 0 | 0 |
| `engba2.pikeman18.2.6` | Barracks 18c pikeman18 protection +3 (lvl 7) | 7 | 3 | 15.62 | 64600 | 0 | 0 | 5500 | 0 | 0 |
| `engbar.drummer.2.1` | Barracks 17c drummer protection +12 (lvl 2) | 2 | 12 | 15.62 | 670 | 0 | 0 | 45 | 0 | 0 |
| `engbar.musketeer.1.1` | Barracks 17c musketeer damage +1 (lvl 2) | 2 | 1 | 15.62 | 1900 | 0 | 0 | 150 | 0 | 0 |
| `engbar.musketeer.1.2` | Barracks 17c musketeer damage +1 (lvl 3) | 3 | 1 | 15.62 | 1000 | 0 | 0 | 300 | 0 | 0 |
| `engbar.musketeer.1.3` | Barracks 17c musketeer damage +2 (lvl 4) | 4 | 2 | 15.62 | 500 | 0 | 0 | 700 | 0 | 0 |
| `engbar.musketeer.2.1` | Barracks 17c musketeer protection +1 (lvl 2) | 2 | 1 | 15.62 | 220 | 0 | 0 | 50 | 100 | 0 |
| `engbar.musketeer.2.2` | Barracks 17c musketeer protection +2 (lvl 3) | 3 | 2 | 15.62 | 505 | 0 | 0 | 140 | 200 | 0 |
| `engbar.musketeer.2.3` | Barracks 17c musketeer protection +2 (lvl 4) | 4 | 2 | 15.62 | 1670 | 0 | 0 | 100 | 350 | 0 |
| `engbar.musketeer.2.4` | Barracks 17c musketeer protection +1 (lvl 5) | 5 | 1 | 15.62 | 1000 | 0 | 0 | 920 | 100 | 0 |
| `engbar.musketeer.2.5` | Barracks 17c musketeer protection +2 (lvl 6) | 6 | 2 | 15.62 | 1060 | 0 | 0 | 700 | 400 | 0 |
| `engbar.musketeer.2.6` | Barracks 17c musketeer protection +2 (lvl 7) | 7 | 2 | 15.62 | 3900 | 0 | 0 | 550 | 700 | 0 |
| `engbar.officer.1.1` | Barracks 17c officer damage +20 (lvl 2) | 2 | 20 | 15.62 | 250 | 0 | 0 | 75 | 0 | 0 |
| `engbar.officer.2.1` | Barracks 17c officer protection +6 (lvl 2) | 2 | 6 | 15.62 | 1650 | 0 | 0 | 425 | 0 | 0 |
| `engbar.pikeman.1.1` | Barracks 17c pikeman damage +1 (lvl 2) | 2 | 1 | 15.62 | 200 | 0 | 0 | 50 | 0 | 0 |
| `engbar.pikeman.1.2` | Barracks 17c pikeman damage +2 (lvl 3) | 3 | 2 | 15.62 | 1250 | 0 | 0 | 310 | 0 | 0 |
| `engbar.pikeman.1.3` | Barracks 17c pikeman damage +2 (lvl 4) | 4 | 2 | 15.62 | 3900 | 0 | 0 | 650 | 0 | 0 |
| `engbar.pikeman.1.4` | Barracks 17c pikeman damage +1 (lvl 5) | 5 | 1 | 15.62 | 7200 | 0 | 0 | 1850 | 0 | 0 |
| `engbar.pikeman.1.5` | Barracks 17c pikeman damage +2 (lvl 6) | 6 | 2 | 15.62 | 16030 | 0 | 0 | 2000 | 0 | 0 |
| `engbar.pikeman.1.6` | — | 7 | 2 | 15.62 | 15000 | 0 | 0 | 1875 | 0 | 0 |
| `engbar.pikeman.2.1` | Barracks 17c pikeman protection +1 (lvl 2) | 2 | 1 | 15.62 | 990 | 0 | 0 | 50 | 0 | 0 |
| `engbar.pikeman.2.2` | Barracks 17c pikeman protection +1 (lvl 3) | 3 | 1 | 15.62 | 200 | 0 | 0 | 175 | 0 | 0 |
| `engbar.pikeman.2.3` | Barracks 17c pikeman protection +2 (lvl 4) | 4 | 2 | 15.62 | 4500 | 0 | 0 | 300 | 0 | 0 |
| `engbar.pikeman.2.4` | Barracks 17c pikeman protection +1 (lvl 5) | 5 | 1 | 15.62 | 9005 | 0 | 0 | 507 | 0 | 0 |
| `engbar.pikeman.2.5` | Barracks 17c pikeman protection +1 (lvl 6) | 6 | 1 | 15.62 | 17010 | 0 | 0 | 3050 | 0 | 0 |
| `engbar.pikeman.2.6` | — | 7 | 2 | 15.62 | 11250 | 0 | 0 | 1500 | 0 | 0 |
| `engbla.1` | Manufacture agricultural equipment (field capacity +100%) | 1 | 100 | 15.62 | 0 | 400 | 0 | 90 | 0 | 0 |
| `engbla.2` | Forge metal armature and gratings (building defence +50) | 1 | 50 | 15.62 | 0 | 0 | 12320 | 350 | 900 | 0 |
| `engbla.3` | Forge harnesses for horses (mounted units recruitment speed -33%) | 1 | -3333333 | 15.62 | 0 | 0 | 0 | 3550 | 4100 | 6700 |
| `engbla.4` | Forge bayonets and broadswords for infantry (18c musketeer/grenadier melee attack +5) | 1 | 5 | 15.62 | 0 | 1300 | 0 | 1500 | 900 | 5000 |
| `engbla.5` | Forge new types of broadswords and sabres (cavalry and sword clansman attack +5) | 1 | 5 | 15.62 | 0 | 0 | 0 | 6550 | 7900 | 0 |
| `engbla.6` | Forge new cuirasses (armoured soldiers defence +2) | 1 | 2 | 15.62 | 0 | 0 | 0 | 4950 | 10500 | 0 |
| `engcen.1` | — | 1 | 0 | 9.38 | 25000 | 0 | 0 | 5000 | 5500 | 5500 |
| `engsta.cuirassier.1.1` | Stable cuirassier damage +1 (lvl 2) | 2 | 1 | 15.62 | 10000 | 0 | 0 | 900 | 0 | 0 |
| `engsta.cuirassier.1.2` | Stable cuirassier damage +1 (lvl 3) | 3 | 1 | 15.62 | 34000 | 0 | 0 | 1000 | 0 | 0 |
| `engsta.cuirassier.1.3` | Stable cuirassier damage +1 (lvl 4) | 4 | 1 | 15.62 | 42000 | 0 | 0 | 3200 | 0 | 0 |
| `engsta.cuirassier.1.4` | Stable cuirassier damage +2 (lvl 5) | 5 | 2 | 15.62 | 61000 | 0 | 0 | 3150 | 0 | 0 |
| `engsta.cuirassier.1.5` | Stable cuirassier damage +2 (lvl 6) | 6 | 2 | 15.62 | 47055 | 0 | 0 | 4100 | 0 | 0 |
| `engsta.cuirassier.1.6` | Stable cuirassier damage +3 (lvl 7) | 7 | 3 | 15.62 | 59050 | 0 | 0 | 11020 | 0 | 0 |
| `engsta.cuirassier.2.1` | Stable cuirassier protection +2 (lvl 2) | 2 | 2 | 15.62 | 1260 | 0 | 0 | 350 | 200 | 0 |
| `engsta.cuirassier.2.2` | Stable cuirassier protection +3 (lvl 3) | 3 | 3 | 15.62 | 3500 | 0 | 0 | 750 | 2800 | 0 |
| `engsta.cuirassier.2.3` | Stable cuirassier protection +3 (lvl 4) | 4 | 3 | 15.62 | 2600 | 0 | 0 | 900 | 2930 | 0 |
| `engsta.cuirassier.2.4` | Stable cuirassier protection +2 (lvl 5) | 5 | 2 | 15.62 | 12700 | 0 | 0 | 5600 | 200 | 0 |
| `engsta.cuirassier.2.5` | Stable cuirassier protection +1 (lvl 6) | 6 | 1 | 15.62 | 5700 | 0 | 0 | 1350 | 7000 | 0 |
| `engsta.cuirassier.2.6` | Stable cuirassier protection +1 (lvl 7) | 7 | 1 | 15.62 | 12700 | 0 | 0 | 5424 | 5060 | 0 |
| `engsta.dragoon.1.1` | Stable dragoon damage +1 (lvl 2) | 2 | 1 | 15.62 | 400 | 0 | 0 | 150 | 0 | 0 |
| `engsta.dragoon.1.2` | Stable dragoon damage +1 (lvl 3) | 3 | 1 | 15.62 | 800 | 0 | 0 | 200 | 0 | 0 |
| `engsta.dragoon.1.3` | Stable dragoon damage +2 (lvl 4) | 4 | 2 | 15.62 | 300 | 0 | 0 | 340 | 0 | 0 |
| `engsta.dragoon.1.4` | Stable dragoon damage +1 (lvl 5) | 5 | 1 | 15.62 | 0 | 0 | 0 | 0 | 0 | 0 |
| `engsta.dragoon.1.5` | Stable dragoon damage +1 (lvl 6) | 6 | 1 | 15.62 | 0 | 0 | 0 | 0 | 0 | 0 |
| `engsta.dragoon.1.6` | Stable dragoon damage +3 (lvl 7) | 7 | 3 | 15.62 | 0 | 0 | 0 | 0 | 0 | 0 |
| `engsta.dragoon.2.1` | Stable dragoon protection +1 (lvl 2) | 2 | 1 | 15.62 | 1300 | 0 | 0 | 250 | 0 | 0 |
| `engsta.dragoon.2.2` | Stable dragoon protection +2 (lvl 3) | 3 | 2 | 15.62 | 5200 | 0 | 0 | 650 | 0 | 0 |
| `engsta.dragoon.2.3` | Stable dragoon protection +2 (lvl 4) | 4 | 2 | 15.62 | 2000 | 0 | 0 | 1450 | 0 | 0 |
| `engsta.dragoon.2.4` | Stable dragoon protection +1 (lvl 5) | 5 | 1 | 15.62 | 6000 | 0 | 0 | 100 | 0 | 0 |
| `engsta.dragoon.2.5` | Stable dragoon protection +2 (lvl 6) | 6 | 2 | 15.62 | 1000 | 0 | 0 | 3250 | 0 | 0 |
| `engsta.dragoon.2.6` | Stable dragoon protection +2 (lvl 7) | 7 | 2 | 15.62 | 7001 | 0 | 0 | 4400 | 0 | 0 |
| `engsta.dragoon18.1.1` | Stable dragoon18 damage +2 (lvl 2) | 2 | 2 | 15.62 | 1000 | 0 | 0 | 200 | 0 | 0 |
| `engsta.dragoon18.1.2` | Stable dragoon18 damage +2 (lvl 3) | 3 | 2 | 15.62 | 10200 | 0 | 0 | 250 | 0 | 0 |
| `engsta.dragoon18.1.3` | Stable dragoon18 damage +4 (lvl 4) | 4 | 4 | 15.62 | 15200 | 0 | 0 | 200 | 0 | 0 |
| `engsta.dragoon18.1.4` | Stable dragoon18 damage +2 (lvl 5) | 5 | 2 | 15.62 | 19850 | 0 | 0 | 280 | 0 | 0 |
| `engsta.dragoon18.1.5` | Stable dragoon18 damage +2 (lvl 6) | 6 | 2 | 15.62 | 32000 | 0 | 0 | 1180 | 0 | 0 |
| `engsta.dragoon18.1.6` | Stable dragoon18 damage +4 (lvl 7) | 7 | 4 | 15.62 | 32000 | 0 | 0 | 980 | 0 | 0 |
| `engsta.dragoon18.2.1` | Stable dragoon18 protection +1 (lvl 2) | 2 | 1 | 15.62 | 250 | 0 | 0 | 999 | 0 | 0 |
| `engsta.dragoon18.2.2` | Stable dragoon18 protection +1 (lvl 3) | 3 | 1 | 15.62 | 1360 | 0 | 0 | 1250 | 0 | 0 |
| `engsta.dragoon18.2.3` | Stable dragoon18 protection +2 (lvl 4) | 4 | 2 | 15.62 | 17600 | 0 | 0 | 2150 | 0 | 0 |
| `engsta.dragoon18.2.4` | Stable dragoon18 protection +1 (lvl 5) | 5 | 1 | 15.62 | 15600 | 0 | 0 | 5350 | 0 | 0 |
| `engsta.dragoon18.2.5` | Stable dragoon18 protection +2 (lvl 6) | 6 | 2 | 15.62 | 19600 | 0 | 0 | 3350 | 0 | 0 |
| `engsta.dragoon18.2.6` | Stable dragoon18 protection +3 (lvl 7) | 7 | 3 | 15.62 | 25760 | 0 | 0 | 8350 | 0 | 0 |
| `engsta.hussar.1.1` | Stable hussar damage +1 (lvl 2) | 2 | 1 | 15.62 | 0 | 0 | 0 | 1200 | 400 | 0 |
| `engsta.hussar.1.2` | Stable hussar damage +2 (lvl 3) | 3 | 2 | 15.62 | 0 | 0 | 0 | 3800 | 2000 | 0 |
| `engsta.hussar.1.3` | Stable hussar damage +3 (lvl 4) | 4 | 3 | 15.62 | 10200 | 0 | 0 | 0 | 3000 | 0 |
| `engsta.hussar.1.4` | Stable hussar damage +4 (lvl 5) | 5 | 4 | 15.62 | 42000 | 0 | 0 | 0 | 2000 | 0 |
| `engsta.hussar.1.5` | Stable hussar damage +1 (lvl 6) | 6 | 1 | 15.62 | 49200 | 0 | 0 | 0 | 6500 | 0 |
| `engsta.hussar.1.6` | Stable hussar damage +1 (lvl 7) | 7 | 1 | 15.62 | 14000 | 0 | 0 | 0 | 2000 | 0 |
| `engsta.hussar.2.1` | Stable hussar protection +1 (lvl 2) | 2 | 1 | 15.62 | 1550 | 0 | 0 | 1150 | 0 | 0 |
| `engsta.hussar.2.2` | Stable hussar protection +1 (lvl 3) | 3 | 1 | 15.62 | 2150 | 0 | 0 | 2550 | 0 | 0 |
| `engsta.hussar.2.3` | Stable hussar protection +1 (lvl 4) | 4 | 1 | 15.62 | 5600 | 0 | 0 | 4350 | 0 | 0 |
| `engsta.hussar.2.4` | Stable hussar protection +2 (lvl 5) | 5 | 2 | 15.62 | 4000 | 0 | 0 | 9350 | 0 | 0 |
| `engsta.hussar.2.5` | Stable hussar protection +2 (lvl 6) | 6 | 2 | 15.62 | 9000 | 0 | 0 | 13200 | 0 | 0 |
| `engsta.hussar.2.6` | Stable hussar protection +2 (lvl 7) | 7 | 2 | 15.62 | 52000 | 0 | 0 | 19850 | 0 | 0 |
| `engsta.reiter.1.1` | Stable reiter damage +1 (lvl 2) | 2 | 1 | 15.62 | 400 | 0 | 0 | 50 | 0 | 0 |
| `engsta.reiter.1.2` | Stable reiter damage +2 (lvl 3) | 3 | 2 | 15.62 | 1000 | 0 | 0 | 270 | 0 | 0 |
| `engsta.reiter.1.3` | Stable reiter damage +1 (lvl 4) | 4 | 1 | 15.62 | 4400 | 0 | 0 | 180 | 0 | 0 |
| `engsta.reiter.1.4` | Stable reiter damage +1 (lvl 5) | 5 | 1 | 15.62 | 2750 | 0 | 0 | 420 | 0 | 0 |
| `engsta.reiter.1.5` | Stable reiter damage +1 (lvl 6) | 6 | 1 | 15.62 | 2530 | 0 | 0 | 600 | 0 | 0 |
| `engsta.reiter.1.6` | Stable reiter damage +1 (lvl 7) | 7 | 1 | 15.62 | 7500 | 0 | 0 | 1700 | 0 | 0 |
| `engsta.reiter.2.1` | Stable reiter protection +2 (lvl 2) | 2 | 2 | 15.62 | 500 | 0 | 0 | 35 | 200 | 0 |
| `engsta.reiter.2.2` | Stable reiter protection +3 (lvl 3) | 3 | 3 | 15.62 | 300 | 0 | 0 | 200 | 500 | 0 |
| `engsta.reiter.2.3` | Stable reiter protection +3 (lvl 4) | 4 | 3 | 15.62 | 950 | 0 | 0 | 200 | 620 | 0 |
| `engsta.reiter.2.4` | Stable reiter protection +2 (lvl 5) | 5 | 2 | 15.62 | 1450 | 0 | 0 | 300 | 540 | 0 |
| `engsta.reiter.2.5` | Stable reiter protection +1 (lvl 6) | 6 | 1 | 15.62 | 6200 | 0 | 0 | 550 | 600 | 0 |
| `engsta.reiter.2.6` | Stable reiter protection +1 (lvl 7) | 7 | 1 | 15.62 | 12000 | 0 | 0 | 720 | 3730 | 0 |
| `eurcoa.1` | — | 2 | 5 | 9.38 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `eurcoa.2` | — | 3 | 8 | 9.38 | 5250 | 0 | 0 | 4950 | 0 | 0 |
| `eurcoa.3` | — | 4 | 10 | 9.38 | 12500 | 0 | 0 | 9250 | 0 | 0 |
| `eurcoa.4` | — | 5 | 12 | 9.38 | 15800 | 0 | 0 | 18500 | 0 | 0 |
| `eurcoa.5` | — | 6 | 15 | 9.38 | 19800 | 0 | 0 | 21050 | 0 | 0 |
| `eurcoa.6` | — | 7 | 40 | 9.38 | 50200 | 0 | 0 | 25950 | 0 | 0 |
| `eurgol.1` | — | 2 | 5 | 9.38 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `eurgol.2` | — | 3 | 8 | 9.38 | 5250 | 0 | 0 | 4950 | 0 | 0 |
| `eurgol.3` | — | 4 | 10 | 9.38 | 12500 | 0 | 0 | 9250 | 0 | 0 |
| `eurgol.4` | — | 5 | 12 | 9.38 | 15800 | 0 | 0 | 18500 | 0 | 0 |
| `eurgol.5` | — | 6 | 15 | 9.38 | 19800 | 0 | 0 | 21050 | 0 | 0 |
| `eurgol.6` | — | 7 | 40 | 9.38 | 50200 | 0 | 0 | 25950 | 0 | 0 |
| `euriro.1` | — | 2 | 5 | 9.38 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `euriro.2` | — | 3 | 8 | 9.38 | 5250 | 0 | 0 | 4950 | 0 | 0 |
| `euriro.3` | — | 4 | 10 | 9.38 | 12500 | 0 | 0 | 9250 | 0 | 0 |
| `euriro.4` | — | 5 | 12 | 9.38 | 15800 | 0 | 0 | 18500 | 0 | 0 |
| `euriro.5` | — | 6 | 15 | 9.38 | 19800 | 0 | 0 | 21050 | 0 | 0 |
| `euriro.6` | — | 7 | 40 | 9.38 | 50200 | 0 | 0 | 25950 | 0 | 0 |
| `eurpor.1` | — | 1 | 50 | 46.88 | 0 | 12000 | 0 | 500 | 0 | 0 |
| `eurswa.1` | — | 2 | 5 | 0.03 | 0 | 0 | 500 | 0 | 0 | 0 |
| `eurtow.1` | — | 2 | -20 | 31.25 | 0 | 0 | 0 | 250 | 0 | 0 |
| `eurtow.2` | — | 3 | -20 | 31.25 | 0 | 0 | 0 | 0 | 350 | 0 |
| `eurtow.3` | — | 4 | -10 | 31.25 | 0 | 0 | 0 | 0 | 0 | 400 |
| `eurtow.4` | — | 5 | -10 | 31.25 | 0 | 0 | 0 | 0 | 450 | 0 |
| `eurtow.5` | — | 6 | -10 | 31.25 | 0 | 0 | 0 | 0 | 0 | 500 |
| `ferry.1` | Improve transport vessel design (+%value% capacity) | 2 | 200 | 15.62 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `ukrwwa.1` | — | 2 | 5 | 0.03 | 0 | 400 | 0 | 0 | 0 | 0 |

### spa — Spain

| sid | имя (EN) | level | value | время (s) | F | W | S | G | I | C |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `eurcoa.1` | — | 2 | 5 | 9.38 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `eurcoa.2` | — | 3 | 8 | 9.38 | 5250 | 0 | 0 | 4950 | 0 | 0 |
| `eurcoa.3` | — | 4 | 10 | 9.38 | 12500 | 0 | 0 | 9250 | 0 | 0 |
| `eurcoa.4` | — | 5 | 12 | 9.38 | 15800 | 0 | 0 | 18500 | 0 | 0 |
| `eurcoa.5` | — | 6 | 15 | 9.38 | 19800 | 0 | 0 | 21050 | 0 | 0 |
| `eurcoa.6` | — | 7 | 40 | 9.38 | 50200 | 0 | 0 | 25950 | 0 | 0 |
| `eurgol.1` | — | 2 | 5 | 9.38 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `eurgol.2` | — | 3 | 8 | 9.38 | 5250 | 0 | 0 | 4950 | 0 | 0 |
| `eurgol.3` | — | 4 | 10 | 9.38 | 12500 | 0 | 0 | 9250 | 0 | 0 |
| `eurgol.4` | — | 5 | 12 | 9.38 | 15800 | 0 | 0 | 18500 | 0 | 0 |
| `eurgol.5` | — | 6 | 15 | 9.38 | 19800 | 0 | 0 | 21050 | 0 | 0 |
| `eurgol.6` | — | 7 | 40 | 9.38 | 50200 | 0 | 0 | 25950 | 0 | 0 |
| `euriro.1` | — | 2 | 5 | 9.38 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `euriro.2` | — | 3 | 8 | 9.38 | 5250 | 0 | 0 | 4950 | 0 | 0 |
| `euriro.3` | — | 4 | 10 | 9.38 | 12500 | 0 | 0 | 9250 | 0 | 0 |
| `euriro.4` | — | 5 | 12 | 9.38 | 15800 | 0 | 0 | 18500 | 0 | 0 |
| `euriro.5` | — | 6 | 15 | 9.38 | 19800 | 0 | 0 | 21050 | 0 | 0 |
| `euriro.6` | — | 7 | 40 | 9.38 | 50200 | 0 | 0 | 25950 | 0 | 0 |
| `eurpor.1` | — | 1 | 50 | 46.88 | 0 | 20000 | 0 | 1500 | 0 | 0 |
| `eurswa.1` | — | 2 | 5 | 0.03 | 0 | 0 | 500 | 0 | 0 | 0 |
| `eurtow.1` | — | 2 | -20 | 31.25 | 0 | 0 | 0 | 250 | 0 | 0 |
| `eurtow.2` | — | 3 | -20 | 31.25 | 0 | 0 | 0 | 0 | 350 | 0 |
| `eurtow.3` | — | 4 | -10 | 31.25 | 0 | 0 | 0 | 0 | 0 | 400 |
| `eurtow.4` | — | 5 | -10 | 31.25 | 0 | 0 | 0 | 0 | 450 | 0 |
| `eurtow.5` | — | 6 | -10 | 31.25 | 0 | 0 | 0 | 0 | 0 | 500 |
| `ferry.1` | Improve transport vessel design (+%value% capacity) | 2 | 200 | 15.62 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `spaaca.1` | Cultivate new cultures of wheat (harvesting +40%) | 1 | 40 | 15.62 | 0 | 200 | 0 | 325 | 0 | 0 |
| `spaaca.10` | Raise builders' salary (building construction time -75%) | 1 | -7500000 | 15.62 | 0 | 0 | 0 | 6950 | 0 | 0 |
| `spaaca.11` | Research new fortification grades (durability of walls and towers +80) | 1 | 80 | 15.62 | 0 | 0 | 16200 | 1500 | 0 | 0 |
| `spaaca.12` | Improve firearms: rifled barrel (fire power +10%) | 1 | 10 | 15.62 | 0 | 0 | 0 | 0 | 5000 | 0 |
| `spaaca.13` | Research granular gunpowder (fire power +10%) | 1 | 10 | 15.62 | 0 | 0 | 0 | 4000 | 0 | 0 |
| `spaaca.14` | Research new sulphur purification methods (fire power +15%) | 1 | 15 | 15.62 | 0 | 0 | 0 | 7000 | 0 | 0 |
| `spaaca.15` | Research new nitre purification methods (fire power +25%) | 1 | 25 | 15.62 | 0 | 0 | 0 | 0 | 0 | 11000 |
| `spaaca.16` | Research improved additions to gunpowder formula (artillery range +5%) | 1 | 5 | 15.62 | 0 | 0 | 0 | 2000 | 12150 | 0 |
| `spaaca.17` | Design new barrel types: unicorn, carronade (artillery range +10%) | 1 | 10 | 15.62 | 0 | 0 | 3000 | 4550 | 19200 | 0 |
| `spaaca.18` | Design more durable gun carriage: Gribovalle system (artillery durability +50%) | 1 | 50 | 15.62 | 0 | 0 | 0 | 500 | 3830 | 1500 |
| `spaaca.19` | Design multi-barrelled cannon | 1 | 0 | 15.62 | 0 | 0 | 0 | 1500 | 0 | 2500 |
| `spaaca.2` | Cultivate new cultures of rye (harvesting +50%) | 1 | 50 | 15.62 | 0 | 2400 | 0 | 625 | 0 | 0 |
| `spaaca.20` | Research new sighting devices for artillery (artillery accuracy +35%) | 1 | -35 | 15.62 | 0 | 3540 | 0 | 2000 | 0 | 7250 |
| `spaaca.21` | Finance artillery repair shops (repair all artillery) | 1 | 25 | 15.62 | 0 | 350 | 0 | 100 | 0 | 250 |
| `spaaca.22` | Develop geology (previously hidden deposits appear on the map) | 1 | 0 | 15.62 | 0 | 0 | 0 | 250 | 0 | 0 |
| `spaaca.23` | Develop mining (stone excavation efficiency +100%) | 1 | 100 | 15.62 | 0 | 0 | 0 | 1550 | 3000 | 0 |
| `spaaca.24` | Raise miners' salary (stone excavation efficiency +200%) | 1 | 200 | 15.62 | 4200 | 0 | 0 | 1550 | 0 | 12520 |
| `spaaca.25` | Design Montgolfier (reveals the whole map) | 1 | 0 | 15.62 | 0 | 0 | 0 | 5750 | 0 | 0 |
| `spaaca.26` | Develop medical science (heals all live units) | 1 | 50 | 31.25 | 0 | 0 | 0 | 200 | 0 | 200 |
| `spaaca.27` | Develop mathematics (artillery accuracy +35%) | 1 | -35 | 15.62 | 0 | 9540 | 0 | 12000 | 0 | 65200 |
| `spaaca.28` | Design new rigging types (ship speed +40%) | 1 | 40 | 15.62 | 0 | 65400 | 0 | 24050 | 0 | 0 |
| `spaaca.29` | Design new rib system and new hulls (battleship construction) | 1 | 0 | 15.62 | 0 | 32300 | 0 | 6800 | 9000 | 12800 |
| `spaaca.3` | Raise agriculturists' salary (harvesting +50%) | 1 | 50 | 15.62 | 0 | 3600 | 0 | 850 | 0 | 0 |
| `spaaca.30` | Train carpenters (shipbuilding speed x10) | 1 | -5000000 | 15.62 | 0 | 2300 | 42700 | 1150 | 0 | 0 |
| `spaaca.31` | Design wheellock (rate of fire +30%) | 1 | -30 | 15.62 | 0 | 0 | 6000 | 5500 | 4200 | 0 |
| `spaaca.32` | Design flintlock (musket cost -50%) | 1 | 0 | 15.62 | 0 | 0 | 0 | 6050 | 0 | 7750 |
| `spaaca.33` | Design paper cartridge and iron ramrod (rate of fire +30%) | 1 | -30 | 15.62 | 0 | 5000 | 0 | 5500 | 0 | 15200 |
| `spaaca.34` | Research improved steel grades for cuirasses (armoured soldier defence +2) | 1 | 2 | 15.62 | 0 | 0 | 0 | 9750 | 0 | 0 |
| `spaaca.35` | Design bayonet: barrel-inserted, bayonet with a tube (cold steel weapons +5) | 1 | 5 | 15.62 | 0 | 0 | 0 | 11500 | 0 | 0 |
| `spaaca.36` | Research new steel grades (18c musketeer/grenadier melee attack efficiency +25%) | 1 | 25 | 15.62 | 0 | 0 | 0 | 19500 | 0 | 0 |
| `spaaca.4` | Carry out field melioration (field capacity +200%) | 1 | 200 | 15.62 | 0 | 1000 | 0 | 475 | 0 | 0 |
| `spaaca.5` | Design new tackle and fishing nets (boat efficiency +100%) | 1 | 100 | 15.62 | 0 | 12400 | 0 | 2520 | 0 | 0 |
| `spaaca.6` | Develop new woodworking methods (frigate building) | 1 | 0 | 15.62 | 0 | 12400 | 0 | 7040 | 0 | 0 |
| `spaaca.7` | Build new shipyards for fishing boats (fishing boat cost -85%) | 1 | 0 | 15.62 | 0 | 7300 | 0 | 1220 | 0 | 0 |
| `spaaca.8` | Design new woodworking tools (woodcutting efficiency +100%) | 1 | 100 | 15.62 | 5500 | 0 | 0 | 550 | 0 | 0 |
| `spaaca.9` | Use new construction materials (durability of buildings +85) | 1 | 85 | 15.62 | 0 | 9400 | 7850 | 1150 | 0 | 0 |
| `spaart.cannon.1.1` | — | 2 | — | 10.0 | 0 | 1000 | 500 | 300 | 0 | 0 |
| `spaart.cannon.1.2` | — | 3 | — | 10.0 | 0 | 3000 | 1000 | 500 | 0 | 0 |
| `spaart.cannon.1.3` | — | 4 | — | 10.0 | 0 | 6000 | 2000 | 1000 | 0 | 0 |
| `spaart.cannon.1.4` | — | 5 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `spaart.cannon.1.5` | — | 6 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `spaart.cannon.1.6` | — | 7 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `spaart.cannon.2.1` | — | 2 | -2500000 | 10.0 | 0 | 0 | 0 | 500 | 1000 | 0 |
| `spaart.cannon.2.2` | — | 3 | -2500000 | 10.0 | 0 | 0 | 0 | 1000 | 2000 | 0 |
| `spaart.cannon.2.3` | — | 4 | -2500000 | 10.0 | 0 | 0 | 0 | 2000 | 3000 | 0 |
| `spaart.cannon.2.4` | — | 5 | -2000000 | 15.62 | 2560 | 0 | 0 | 0 | 0 | 0 |
| `spaart.cannon.2.5` | — | 6 | -2000000 | 15.62 | 3560 | 0 | 0 | 0 | 0 | 0 |
| `spaart.cannon.2.6` | — | 7 | -2000000 | 15.62 | 5560 | 0 | 0 | 0 | 0 | 0 |
| `spaart.howitzer.1.1` | — | 2 | — | 10.0 | 0 | 1000 | 500 | 300 | 0 | 0 |
| `spaart.howitzer.1.2` | — | 3 | — | 10.0 | 0 | 3000 | 1000 | 500 | 0 | 0 |
| `spaart.howitzer.1.3` | — | 4 | — | 10.0 | 0 | 6000 | 2000 | 1000 | 0 | 0 |
| `spaart.howitzer.1.4` | — | 5 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `spaart.howitzer.1.5` | — | 6 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `spaart.howitzer.1.6` | — | 7 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `spaart.howitzer.2.1` | — | 2 | -2500000 | 10.0 | 0 | 0 | 0 | 500 | 1000 | 0 |
| `spaart.howitzer.2.2` | — | 3 | -2500000 | 10.0 | 0 | 0 | 0 | 1000 | 2000 | 0 |
| `spaart.howitzer.2.3` | — | 4 | -2500000 | 10.0 | 0 | 0 | 0 | 2000 | 3000 | 0 |
| `spaart.howitzer.2.4` | — | 5 | -2000000 | 31.25 | 2560 | 0 | 0 | 0 | 0 | 0 |
| `spaart.howitzer.2.5` | — | 6 | -2000000 | 31.25 | 3560 | 0 | 0 | 0 | 0 | 0 |
| `spaart.howitzer.2.6` | — | 7 | -2000000 | 31.25 | 5560 | 0 | 0 | 0 | 0 | 0 |
| `spaba2.drummer18.2.1` | Barracks 18c drummer18 protection +15 (lvl 2) | 2 | 15 | 15.62 | 706 | 0 | 0 | 50 | 0 | 0 |
| `spaba2.grenadier.1.1` | Barracks 18c grenadier damage +2 (lvl 2) | 2 | 2 | 15.62 | 2000 | 0 | 0 | 800 | 0 | 0 |
| `spaba2.grenadier.1.2` | Barracks 18c grenadier damage +3 (lvl 3) | 3 | 3 | 15.62 | 12000 | 0 | 0 | 1800 | 0 | 0 |
| `spaba2.grenadier.1.3` | Barracks 18c grenadier damage +4 (lvl 4) | 4 | 4 | 15.62 | 32000 | 0 | 0 | 2800 | 0 | 0 |
| `spaba2.grenadier.1.4` | Barracks 18c grenadier damage +5 (lvl 5) | 5 | 5 | 15.62 | 42000 | 0 | 0 | 3800 | 0 | 0 |
| `spaba2.grenadier.1.5` | Barracks 18c grenadier damage +6 (lvl 6) | 6 | 6 | 15.62 | 52000 | 0 | 0 | 4800 | 0 | 0 |
| `spaba2.grenadier.1.6` | Barracks 18c grenadier damage +1500 (lvl 7) | 7 | 1500 | 15.62 | 62000 | 0 | 0 | 15800 | 0 | 0 |
| `spaba2.grenadier.2.1` | Barracks 18c grenadier protection +1 (lvl 2) | 2 | 1 | 15.62 | 3706 | 0 | 0 | 350 | 0 | 0 |
| `spaba2.grenadier.2.2` | Barracks 18c grenadier protection +2 (lvl 3) | 3 | 2 | 15.62 | 11030 | 0 | 0 | 1350 | 0 | 0 |
| `spaba2.grenadier.2.3` | Barracks 18c grenadier protection +3 (lvl 4) | 4 | 3 | 15.62 | 35706 | 0 | 0 | 3000 | 0 | 0 |
| `spaba2.grenadier.2.4` | Barracks 18c grenadier protection +1 (lvl 5) | 5 | 1 | 15.62 | 36556 | 0 | 0 | 3350 | 0 | 0 |
| `spaba2.grenadier.2.5` | Barracks 18c grenadier protection +2 (lvl 6) | 6 | 2 | 15.62 | 30060 | 0 | 0 | 1350 | 0 | 0 |
| `spaba2.grenadier.2.6` | Barracks 18c grenadier protection +3 (lvl 7) | 7 | 3 | 15.62 | 64000 | 0 | 0 | 1350 | 0 | 0 |
| `spaba2.musketeer18.1.1` | Barracks 18c musketeer18 damage +1 (lvl 2) | 2 | 1 | 15.62 | 1000 | 0 | 0 | 800 | 0 | 0 |
| `spaba2.musketeer18.1.2` | Barracks 18c musketeer18 damage +1 (lvl 3) | 3 | 1 | 15.62 | 1500 | 0 | 0 | 800 | 0 | 0 |
| `spaba2.musketeer18.1.3` | Barracks 18c musketeer18 damage +2 (lvl 4) | 4 | 2 | 15.62 | 2000 | 0 | 0 | 800 | 0 | 0 |
| `spaba2.musketeer18.1.4` | Barracks 18c musketeer18 damage +2 (lvl 5) | 5 | 2 | 15.62 | 2500 | 0 | 0 | 800 | 0 | 0 |
| `spaba2.musketeer18.1.5` | Barracks 18c musketeer18 damage +3 (lvl 6) | 6 | 3 | 15.62 | 3000 | 0 | 0 | 800 | 0 | 0 |
| `spaba2.musketeer18.1.6` | Barracks 18c musketeer18 damage +3 (lvl 7) | 7 | 3 | 15.62 | 3500 | 0 | 0 | 800 | 0 | 0 |
| `spaba2.musketeer18.2.1` | Barracks 18c musketeer18 protection +1 (lvl 2) | 2 | 1 | 15.62 | 3706 | 0 | 0 | 350 | 0 | 0 |
| `spaba2.musketeer18.2.2` | Barracks 18c musketeer18 protection +2 (lvl 3) | 3 | 2 | 15.62 | 11030 | 0 | 0 | 1350 | 0 | 0 |
| `spaba2.musketeer18.2.3` | Barracks 18c musketeer18 protection +2 (lvl 4) | 4 | 2 | 15.62 | 35706 | 0 | 0 | 4000 | 0 | 0 |
| `spaba2.musketeer18.2.4` | Barracks 18c musketeer18 protection +1 (lvl 5) | 5 | 1 | 15.62 | 36556 | 0 | 0 | 4350 | 0 | 0 |
| `spaba2.musketeer18.2.5` | Barracks 18c musketeer18 protection +2 (lvl 6) | 6 | 2 | 15.62 | 30060 | 0 | 0 | 1350 | 0 | 0 |
| `spaba2.musketeer18.2.6` | Barracks 18c musketeer18 protection +2 (lvl 7) | 7 | 2 | 15.62 | 37600 | 0 | 0 | 1350 | 0 | 0 |
| `spaba2.officer18.1.1` | Barracks 18c officer18 damage +30 (lvl 2) | 2 | 30 | 15.62 | 1000 | 0 | 0 | 800 | 0 | 0 |
| `spaba2.officer18.2.1` | Barracks 18c officer18 protection +12 (lvl 2) | 2 | 12 | 15.62 | 1706 | 0 | 0 | 350 | 0 | 0 |
| `spaba2.pikeman18.1.1` | Barracks 18c pikeman18 damage +2 (lvl 2) | 2 | 2 | 15.62 | 2000 | 0 | 0 | 800 | 0 | 0 |
| `spaba2.pikeman18.1.2` | Barracks 18c pikeman18 damage +2 (lvl 3) | 3 | 2 | 15.62 | 8000 | 0 | 0 | 1200 | 0 | 0 |
| `spaba2.pikeman18.1.3` | Barracks 18c pikeman18 damage +2 (lvl 4) | 4 | 2 | 15.62 | 20000 | 0 | 0 | 2500 | 0 | 0 |
| `spaba2.pikeman18.1.4` | Barracks 18c pikeman18 damage +2 (lvl 5) | 5 | 2 | 15.62 | 32000 | 0 | 0 | 2800 | 0 | 0 |
| `spaba2.pikeman18.1.5` | Barracks 18c pikeman18 damage +2 (lvl 6) | 6 | 2 | 15.62 | 32000 | 0 | 0 | 3800 | 0 | 0 |
| `spaba2.pikeman18.1.6` | Barracks 18c pikeman18 damage +2 (lvl 7) | 7 | 2 | 15.62 | 40500 | 0 | 0 | 4800 | 0 | 0 |
| `spaba2.pikeman18.2.1` | Barracks 18c pikeman18 protection +2 (lvl 2) | 2 | 2 | 15.62 | 1500 | 0 | 0 | 500 | 0 | 0 |
| `spaba2.pikeman18.2.2` | Barracks 18c pikeman18 protection +3 (lvl 3) | 3 | 3 | 15.62 | 7000 | 0 | 0 | 1500 | 0 | 0 |
| `spaba2.pikeman18.2.3` | Barracks 18c pikeman18 protection +2 (lvl 4) | 4 | 2 | 15.62 | 37000 | 0 | 0 | 2000 | 0 | 0 |
| `spaba2.pikeman18.2.4` | Barracks 18c pikeman18 protection +3 (lvl 5) | 5 | 3 | 15.62 | 37000 | 0 | 0 | 5500 | 0 | 0 |
| `spaba2.pikeman18.2.5` | Barracks 18c pikeman18 protection +2 (lvl 6) | 6 | 2 | 15.62 | 37000 | 0 | 0 | 5500 | 0 | 0 |
| `spaba2.pikeman18.2.6` | Barracks 18c pikeman18 protection +3 (lvl 7) | 7 | 3 | 15.62 | 64600 | 0 | 0 | 5500 | 0 | 0 |
| `spabar.1` | — | 1 | 140 | 15.62 | 750 | 0 | 0 | 250 | 0 | 0 |
| `spabar.2` | — | 2 | 180 | 15.62 | 25600 | 0 | 0 | 3350 | 2000 | 0 |
| `spabar.drummer.2.1` | Barracks 17c drummer protection +12 (lvl 2) | 2 | 12 | 15.62 | 706 | 0 | 0 | 50 | 0 | 0 |
| `spabar.musketeerspa.1.1` | Barracks 17c musketeerspa damage +1 (lvl 2) | 2 | 1 | 15.62 | 2000 | 0 | 0 | 100 | 0 | 0 |
| `spabar.musketeerspa.1.2` | Barracks 17c musketeerspa damage +1 (lvl 3) | 3 | 1 | 15.62 | 1000 | 0 | 0 | 300 | 0 | 0 |
| `spabar.musketeerspa.1.3` | Barracks 17c musketeerspa damage +2 (lvl 4) | 4 | 2 | 15.62 | 500 | 0 | 0 | 700 | 0 | 0 |
| `spabar.musketeerspa.2.1` | Barracks 17c musketeerspa protection +1 (lvl 2) | 2 | 1 | 15.62 | 170 | 0 | 0 | 50 | 100 | 0 |
| `spabar.musketeerspa.2.2` | Barracks 17c musketeerspa protection +1 (lvl 3) | 3 | 1 | 15.62 | 405 | 0 | 0 | 150 | 200 | 0 |
| `spabar.musketeerspa.2.3` | Barracks 17c musketeerspa protection +1 (lvl 4) | 4 | 1 | 15.62 | 1570 | 0 | 0 | 100 | 350 | 0 |
| `spabar.musketeerspa.2.4` | Barracks 17c musketeerspa protection +1 (lvl 5) | 5 | 1 | 15.62 | 1556 | 0 | 0 | 550 | 100 | 0 |
| `spabar.musketeerspa.2.5` | Barracks 17c musketeerspa protection +1 (lvl 6) | 6 | 1 | 15.62 | 1060 | 0 | 0 | 850 | 400 | 0 |
| `spabar.musketeerspa.2.6` | Barracks 17c musketeerspa protection +1 (lvl 7) | 7 | 1 | 15.62 | 3700 | 0 | 0 | 650 | 700 | 0 |
| `spabar.officer.1.1` | Barracks 17c officer damage +20 (lvl 2) | 2 | 20 | 15.62 | 100 | 0 | 0 | 50 | 0 | 0 |
| `spabar.officer.2.1` | Barracks 17c officer protection +6 (lvl 2) | 2 | 6 | 15.62 | 1850 | 0 | 0 | 450 | 0 | 0 |
| `spabar.pikeman.1.1` | Barracks 17c pikeman damage +1 (lvl 2) | 2 | 1 | 15.62 | 200 | 0 | 0 | 50 | 0 | 0 |
| `spabar.pikeman.1.2` | Barracks 17c pikeman damage +2 (lvl 3) | 3 | 2 | 15.62 | 1300 | 0 | 0 | 300 | 0 | 0 |
| `spabar.pikeman.1.3` | Barracks 17c pikeman damage +2 (lvl 4) | 4 | 2 | 15.62 | 3600 | 0 | 0 | 450 | 0 | 0 |
| `spabar.pikeman.1.4` | Barracks 17c pikeman damage +1 (lvl 5) | 5 | 1 | 15.62 | 7200 | 0 | 0 | 1850 | 0 | 0 |
| `spabar.pikeman.1.5` | Barracks 17c pikeman damage +2 (lvl 6) | 6 | 2 | 15.62 | 16030 | 0 | 0 | 2000 | 0 | 0 |
| `spabar.pikeman.1.6` | — | 7 | 2 | 15.62 | 15000 | 0 | 0 | 1875 | 0 | 0 |
| `spabar.pikeman.2.1` | Barracks 17c pikeman protection +1 (lvl 2) | 2 | 1 | 15.62 | 150 | 0 | 0 | 50 | 0 | 0 |
| `spabar.pikeman.2.2` | Barracks 17c pikeman protection +1 (lvl 3) | 3 | 1 | 15.62 | 900 | 0 | 0 | 175 | 0 | 0 |
| `spabar.pikeman.2.3` | Barracks 17c pikeman protection +2 (lvl 4) | 4 | 2 | 15.62 | 4500 | 0 | 0 | 300 | 0 | 0 |
| `spabar.pikeman.2.4` | Barracks 17c pikeman protection +1 (lvl 5) | 5 | 1 | 15.62 | 9005 | 0 | 0 | 507 | 0 | 0 |
| `spabar.pikeman.2.5` | Barracks 17c pikeman protection +1 (lvl 6) | 6 | 1 | 15.62 | 18010 | 0 | 0 | 3050 | 0 | 0 |
| `spabar.pikeman.2.6` | — | 7 | 2 | 15.62 | 11250 | 0 | 0 | 1500 | 0 | 0 |
| `spabar.pikemanspa.1.1` | Barracks 17c pikemanspa damage +1 (lvl 2) | 2 | 1 | 15.62 | 200 | 0 | 0 | 50 | 0 | 0 |
| `spabar.pikemanspa.1.2` | Barracks 17c pikemanspa damage +2 (lvl 3) | 3 | 2 | 15.62 | 1300 | 0 | 0 | 300 | 0 | 0 |
| `spabar.pikemanspa.1.3` | Barracks 17c pikemanspa damage +3 (lvl 4) | 4 | 3 | 15.62 | 3600 | 0 | 0 | 450 | 0 | 0 |
| `spabar.pikemanspa.1.4` | Barracks 17c pikemanspa damage +2 (lvl 5) | 5 | 2 | 15.62 | 7200 | 0 | 0 | 1850 | 0 | 0 |
| `spabar.pikemanspa.1.5` | Barracks 17c pikemanspa damage +1 (lvl 6) | 6 | 1 | 15.62 | 16030 | 0 | 0 | 2000 | 0 | 0 |
| `spabar.pikemanspa.1.6` | Barracks 17c pikemanspa damage +1 (lvl 7) | 7 | 1 | 15.62 | 15000 | 0 | 0 | 1875 | 0 | 0 |
| `spabar.pikemanspa.2.1` | Barracks 17c pikemanspa protection +1 (lvl 2) | 2 | 1 | 15.62 | 150 | 0 | 0 | 50 | 0 | 0 |
| `spabar.pikemanspa.2.2` | Barracks 17c pikemanspa protection +1 (lvl 3) | 3 | 1 | 15.62 | 900 | 0 | 0 | 175 | 0 | 0 |
| `spabar.pikemanspa.2.3` | Barracks 17c pikemanspa protection +2 (lvl 4) | 4 | 2 | 15.62 | 4500 | 0 | 0 | 300 | 0 | 0 |
| `spabar.pikemanspa.2.4` | Barracks 17c pikemanspa protection +1 (lvl 5) | 5 | 1 | 15.62 | 9005 | 0 | 0 | 507 | 0 | 0 |
| `spabar.pikemanspa.2.5` | Barracks 17c pikemanspa protection +1 (lvl 6) | 6 | 1 | 15.62 | 18010 | 0 | 0 | 3050 | 0 | 0 |
| `spabar.pikemanspa.2.6` | Barracks 17c pikemanspa protection +2 (lvl 7) | 7 | 2 | 15.62 | 16000 | 0 | 0 | 1000 | 0 | 0 |
| `spabla.1` | Manufacture agricultural equipment (field capacity +100%) | 1 | 100 | 15.62 | 0 | 400 | 0 | 90 | 0 | 0 |
| `spabla.2` | Forge metal armature and gratings (building defence +50) | 1 | 50 | 15.62 | 0 | 0 | 12320 | 350 | 900 | 0 |
| `spabla.3` | Forge harnesses for horses (mounted units recruitment speed -33%) | 1 | -3333333 | 15.62 | 0 | 0 | 0 | 3650 | 5300 | 8200 |
| `spabla.4` | Forge bayonets and broadswords for infantry (18c musketeer/grenadier melee attack +5) | 1 | 5 | 15.62 | 0 | 1300 | 0 | 1500 | 900 | 5000 |
| `spabla.5` | Forge new types of broadswords and sabres (cavalry and sword clansman attack +5) | 1 | 5 | 15.62 | 0 | 0 | 0 | 4000 | 7900 | 0 |
| `spabla.6` | Forge new cuirasses (armoured soldiers defence +2) | 1 | 2 | 15.62 | 0 | 0 | 0 | 4950 | 10500 | 0 |
| `spacen.1` | — | 1 | 0 | 9.38 | 30000 | 0 | 0 | 5000 | 2000 | 2000 |
| `spasta.cuirassier.1.1` | Stable cuirassier damage +1 (lvl 2) | 2 | 1 | 15.62 | 12000 | 0 | 0 | 600 | 0 | 0 |
| `spasta.cuirassier.1.2` | Stable cuirassier damage +1 (lvl 3) | 3 | 1 | 15.62 | 32000 | 0 | 0 | 1300 | 0 | 0 |
| `spasta.cuirassier.1.3` | Stable cuirassier damage +1 (lvl 4) | 4 | 1 | 15.62 | 62000 | 0 | 0 | 2200 | 0 | 0 |
| `spasta.cuirassier.1.4` | Stable cuirassier damage +2 (lvl 5) | 5 | 2 | 15.62 | 61000 | 0 | 0 | 3150 | 0 | 0 |
| `spasta.cuirassier.1.5` | Stable cuirassier damage +2 (lvl 6) | 6 | 2 | 15.62 | 57055 | 0 | 0 | 4100 | 0 | 0 |
| `spasta.cuirassier.1.6` | Stable cuirassier damage +3 (lvl 7) | 7 | 3 | 15.62 | 49050 | 0 | 0 | 8020 | 0 | 0 |
| `spasta.cuirassier.2.1` | Stable cuirassier protection +2 (lvl 2) | 2 | 2 | 15.62 | 1760 | 0 | 0 | 350 | 1000 | 0 |
| `spasta.cuirassier.2.2` | Stable cuirassier protection +3 (lvl 3) | 3 | 3 | 15.62 | 3000 | 0 | 0 | 750 | 2000 | 0 |
| `spasta.cuirassier.2.3` | Stable cuirassier protection +3 (lvl 4) | 4 | 3 | 15.62 | 7600 | 0 | 0 | 300 | 3030 | 0 |
| `spasta.cuirassier.2.4` | Stable cuirassier protection +2 (lvl 5) | 5 | 2 | 15.62 | 8700 | 0 | 0 | 6200 | 100 | 0 |
| `spasta.cuirassier.2.5` | Stable cuirassier protection +1 (lvl 6) | 6 | 1 | 15.62 | 8700 | 0 | 0 | 2350 | 5000 | 0 |
| `spasta.cuirassier.2.6` | Stable cuirassier protection +1 (lvl 7) | 7 | 1 | 15.62 | 9700 | 0 | 0 | 4444 | 7060 | 0 |
| `spasta.dragoon.1.1` | Stable dragoon damage +1 (lvl 2) | 2 | 1 | 15.62 | 500 | 0 | 0 | 150 | 0 | 0 |
| `spasta.dragoon.1.2` | Stable dragoon damage +1 (lvl 3) | 3 | 1 | 15.62 | 700 | 0 | 0 | 200 | 0 | 0 |
| `spasta.dragoon.1.3` | Stable dragoon damage +2 (lvl 4) | 4 | 2 | 15.62 | 900 | 0 | 0 | 340 | 0 | 0 |
| `spasta.dragoon.1.4` | Stable dragoon damage +1 (lvl 5) | 5 | 1 | 15.62 | 0 | 0 | 0 | 0 | 0 | 0 |
| `spasta.dragoon.1.5` | Stable dragoon damage +1 (lvl 6) | 6 | 1 | 15.62 | 0 | 0 | 0 | 0 | 0 | 0 |
| `spasta.dragoon.1.6` | Stable dragoon damage +3 (lvl 7) | 7 | 3 | 15.62 | 0 | 0 | 0 | 0 | 0 | 0 |
| `spasta.dragoon.2.1` | Stable dragoon protection +1 (lvl 2) | 2 | 1 | 15.62 | 900 | 0 | 0 | 150 | 0 | 0 |
| `spasta.dragoon.2.2` | Stable dragoon protection +2 (lvl 3) | 3 | 2 | 15.62 | 6600 | 0 | 0 | 750 | 0 | 0 |
| `spasta.dragoon.2.3` | Stable dragoon protection +2 (lvl 4) | 4 | 2 | 15.62 | 5000 | 0 | 0 | 1250 | 0 | 0 |
| `spasta.dragoon.2.4` | Stable dragoon protection +1 (lvl 5) | 5 | 1 | 15.62 | 3000 | 0 | 0 | 700 | 0 | 0 |
| `spasta.dragoon.2.5` | Stable dragoon protection +2 (lvl 6) | 6 | 2 | 15.62 | 1000 | 0 | 0 | 2350 | 0 | 0 |
| `spasta.dragoon.2.6` | Stable dragoon protection +2 (lvl 7) | 7 | 2 | 15.62 | 6001 | 0 | 0 | 6000 | 0 | 0 |
| `spasta.dragoon18.1.1` | Stable dragoon18 damage +2 (lvl 2) | 2 | 2 | 15.62 | 2000 | 0 | 0 | 100 | 0 | 0 |
| `spasta.dragoon18.1.2` | Stable dragoon18 damage +2 (lvl 3) | 3 | 2 | 15.62 | 9000 | 0 | 0 | 350 | 0 | 0 |
| `spasta.dragoon18.1.3` | Stable dragoon18 damage +4 (lvl 4) | 4 | 4 | 15.62 | 12000 | 0 | 0 | 400 | 0 | 0 |
| `spasta.dragoon18.1.4` | Stable dragoon18 damage +2 (lvl 5) | 5 | 2 | 15.62 | 23000 | 0 | 0 | 580 | 0 | 0 |
| `spasta.dragoon18.1.5` | Stable dragoon18 damage +2 (lvl 6) | 6 | 2 | 15.62 | 32000 | 0 | 0 | 680 | 0 | 0 |
| `spasta.dragoon18.1.6` | Stable dragoon18 damage +4 (lvl 7) | 7 | 4 | 15.62 | 42000 | 0 | 0 | 780 | 0 | 0 |
| `spasta.dragoon18.2.1` | Stable dragoon18 protection +1 (lvl 2) | 2 | 1 | 15.62 | 760 | 0 | 0 | 935 | 0 | 0 |
| `spasta.dragoon18.2.2` | Stable dragoon18 protection +1 (lvl 3) | 3 | 1 | 15.62 | 1260 | 0 | 0 | 1150 | 0 | 0 |
| `spasta.dragoon18.2.3` | Stable dragoon18 protection +2 (lvl 4) | 4 | 2 | 15.62 | 15600 | 0 | 0 | 2350 | 0 | 0 |
| `spasta.dragoon18.2.4` | Stable dragoon18 protection +1 (lvl 5) | 5 | 1 | 15.62 | 17600 | 0 | 0 | 3350 | 0 | 0 |
| `spasta.dragoon18.2.5` | Stable dragoon18 protection +2 (lvl 6) | 6 | 2 | 15.62 | 19600 | 0 | 0 | 5350 | 0 | 0 |
| `spasta.dragoon18.2.6` | Stable dragoon18 protection +3 (lvl 7) | 7 | 3 | 15.62 | 21760 | 0 | 0 | 9350 | 0 | 0 |
| `spasta.hussar.1.1` | Stable hussar damage +1 (lvl 2) | 2 | 1 | 15.62 | 0 | 0 | 0 | 1800 | 1000 | 0 |
| `spasta.hussar.1.2` | Stable hussar damage +2 (lvl 3) | 3 | 2 | 15.62 | 0 | 0 | 0 | 3800 | 2000 | 0 |
| `spasta.hussar.1.3` | Stable hussar damage +3 (lvl 4) | 4 | 3 | 15.62 | 20200 | 0 | 0 | 0 | 2000 | 0 |
| `spasta.hussar.1.4` | Stable hussar damage +4 (lvl 5) | 5 | 4 | 15.62 | 32000 | 0 | 0 | 0 | 3000 | 0 |
| `spasta.hussar.1.5` | Stable hussar damage +1 (lvl 6) | 6 | 1 | 15.62 | 49200 | 0 | 0 | 0 | 3500 | 0 |
| `spasta.hussar.1.6` | Stable hussar damage +1 (lvl 7) | 7 | 1 | 15.62 | 20000 | 0 | 0 | 0 | 6000 | 0 |
| `spasta.hussar.2.1` | Stable hussar protection +1 (lvl 2) | 2 | 1 | 15.62 | 1760 | 0 | 0 | 1350 | 0 | 0 |
| `spasta.hussar.2.2` | Stable hussar protection +1 (lvl 3) | 3 | 1 | 15.62 | 1900 | 0 | 0 | 2350 | 0 | 0 |
| `spasta.hussar.2.3` | Stable hussar protection +1 (lvl 4) | 4 | 1 | 15.62 | 1600 | 0 | 0 | 5350 | 0 | 0 |
| `spasta.hussar.2.4` | Stable hussar protection +2 (lvl 5) | 5 | 2 | 15.62 | 8000 | 0 | 0 | 8350 | 0 | 0 |
| `spasta.hussar.2.5` | Stable hussar protection +2 (lvl 6) | 6 | 2 | 15.62 | 2000 | 0 | 0 | 15350 | 0 | 0 |
| `spasta.hussar.2.6` | Stable hussar protection +3 (lvl 7) | 7 | 3 | 15.62 | 56000 | 0 | 0 | 20150 | 0 | 0 |
| `spasta.reiter.1.1` | Stable reiter damage +1 (lvl 2) | 2 | 1 | 15.62 | 500 | 0 | 0 | 100 | 0 | 0 |
| `spasta.reiter.1.2` | Stable reiter damage +2 (lvl 3) | 3 | 2 | 15.62 | 900 | 0 | 0 | 220 | 0 | 0 |
| `spasta.reiter.1.3` | Stable reiter damage +1 (lvl 4) | 4 | 1 | 15.62 | 4400 | 0 | 0 | 280 | 0 | 0 |
| `spasta.reiter.1.4` | Stable reiter damage +1 (lvl 5) | 5 | 1 | 15.62 | 2250 | 0 | 0 | 320 | 0 | 0 |
| `spasta.reiter.1.5` | Stable reiter damage +1 (lvl 6) | 6 | 1 | 15.62 | 3030 | 0 | 0 | 600 | 0 | 0 |
| `spasta.reiter.1.6` | Stable reiter damage +1 (lvl 7) | 7 | 1 | 15.62 | 7000 | 0 | 0 | 1800 | 0 | 0 |
| `spasta.reiter.2.1` | Stable reiter protection +2 (lvl 2) | 2 | 2 | 15.62 | 200 | 0 | 0 | 135 | 300 | 0 |
| `spasta.reiter.2.2` | Stable reiter protection +3 (lvl 3) | 3 | 3 | 15.62 | 600 | 0 | 0 | 100 | 400 | 0 |
| `spasta.reiter.2.3` | Stable reiter protection +3 (lvl 4) | 4 | 3 | 15.62 | 800 | 0 | 0 | 200 | 560 | 0 |
| `spasta.reiter.2.4` | Stable reiter protection +2 (lvl 5) | 5 | 2 | 15.62 | 1600 | 0 | 0 | 300 | 640 | 0 |
| `spasta.reiter.2.5` | Stable reiter protection +1 (lvl 6) | 6 | 1 | 15.62 | 3200 | 0 | 0 | 350 | 300 | 0 |
| `spasta.reiter.2.6` | Stable reiter protection +1 (lvl 7) | 7 | 1 | 15.62 | 16000 | 0 | 0 | 1000 | 5000 | 0 |
| `ukrwwa.1` | — | 2 | 5 | 0.03 | 0 | 400 | 0 | 0 | 0 | 0 |

### rus — Russia

| sid | имя (EN) | level | value | время (s) | F | W | S | G | I | C |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `eurcoa.1` | — | 2 | 5 | 9.38 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `eurcoa.2` | — | 3 | 8 | 9.38 | 5250 | 0 | 0 | 4950 | 0 | 0 |
| `eurcoa.3` | — | 4 | 10 | 9.38 | 12500 | 0 | 0 | 9250 | 0 | 0 |
| `eurcoa.4` | — | 5 | 12 | 9.38 | 15800 | 0 | 0 | 18500 | 0 | 0 |
| `eurcoa.5` | — | 6 | 15 | 9.38 | 19800 | 0 | 0 | 21050 | 0 | 0 |
| `eurcoa.6` | — | 7 | 40 | 9.38 | 50200 | 0 | 0 | 25950 | 0 | 0 |
| `eurgol.1` | — | 2 | 5 | 9.38 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `eurgol.2` | — | 3 | 8 | 9.38 | 5250 | 0 | 0 | 4950 | 0 | 0 |
| `eurgol.3` | — | 4 | 10 | 9.38 | 12500 | 0 | 0 | 9250 | 0 | 0 |
| `eurgol.4` | — | 5 | 12 | 9.38 | 15800 | 0 | 0 | 18500 | 0 | 0 |
| `eurgol.5` | — | 6 | 15 | 9.38 | 19800 | 0 | 0 | 21050 | 0 | 0 |
| `eurgol.6` | — | 7 | 40 | 9.38 | 50200 | 0 | 0 | 25950 | 0 | 0 |
| `euriro.1` | — | 2 | 5 | 9.38 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `euriro.2` | — | 3 | 8 | 9.38 | 5250 | 0 | 0 | 4950 | 0 | 0 |
| `euriro.3` | — | 4 | 10 | 9.38 | 12500 | 0 | 0 | 9250 | 0 | 0 |
| `euriro.4` | — | 5 | 12 | 9.38 | 15800 | 0 | 0 | 18500 | 0 | 0 |
| `euriro.5` | — | 6 | 15 | 9.38 | 19800 | 0 | 0 | 21050 | 0 | 0 |
| `euriro.6` | — | 7 | 40 | 9.38 | 50200 | 0 | 0 | 25950 | 0 | 0 |
| `ferry.1` | Improve transport vessel design (+%value% capacity) | 2 | 200 | 15.62 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `rusaca.1` | Cultivate new cultures of wheat (harvesting +40%) | 1 | 40 | 15.62 | 0 | 200 | 0 | 325 | 0 | 0 |
| `rusaca.10` | Raise builders' salary (building construction time -75%) | 1 | -7500000 | 15.62 | 0 | 0 | 0 | 6950 | 0 | 0 |
| `rusaca.11` | Research new fortification grades (durability of walls and towers +80) | 1 | 80 | 15.62 | 0 | 0 | 16200 | 1500 | 0 | 0 |
| `rusaca.12` | Improve firearms: rifled barrel (fire power +10%) | 1 | 10 | 15.62 | 0 | 0 | 0 | 0 | 5000 | 0 |
| `rusaca.13` | Research granular gunpowder (fire power +10%) | 1 | 10 | 15.62 | 0 | 0 | 0 | 4000 | 0 | 0 |
| `rusaca.14` | Research new sulphur purification methods (fire power +15%) | 1 | 15 | 15.62 | 0 | 0 | 0 | 7000 | 0 | 0 |
| `rusaca.15` | Research new nitre purification methods (fire power +25%) | 1 | 25 | 15.62 | 0 | 0 | 0 | 0 | 0 | 11000 |
| `rusaca.16` | Research improved additions to gunpowder formula (artillery range +5%) | 1 | 5 | 15.62 | 0 | 0 | 0 | 2000 | 12150 | 0 |
| `rusaca.17` | Design new barrel types: unicorn, carronade (artillery range +10%) | 1 | 10 | 15.62 | 0 | 0 | 3000 | 4550 | 19200 | 0 |
| `rusaca.18` | Design more durable gun carriage: Gribovalle system (artillery durability +50%) | 1 | 50 | 15.62 | 0 | 0 | 0 | 500 | 3830 | 1500 |
| `rusaca.19` | Design multi-barrelled cannon | 1 | 0 | 15.62 | 0 | 0 | 0 | 1500 | 0 | 2500 |
| `rusaca.2` | Cultivate new cultures of rye (harvesting +50%) | 1 | 50 | 15.62 | 0 | 2400 | 0 | 625 | 0 | 0 |
| `rusaca.20` | Research new sighting devices for artillery (artillery accuracy +35%) | 1 | -35 | 15.62 | 0 | 3540 | 0 | 2000 | 0 | 7250 |
| `rusaca.21` | Finance artillery repair shops (repair all artillery) | 1 | 25 | 15.62 | 0 | 350 | 0 | 100 | 0 | 250 |
| `rusaca.22` | Develop geology (previously hidden deposits appear on the map) | 1 | 0 | 15.62 | 0 | 0 | 0 | 250 | 0 | 0 |
| `rusaca.23` | Develop mining (stone excavation efficiency +100%) | 1 | 100 | 15.62 | 0 | 0 | 0 | 1550 | 3000 | 0 |
| `rusaca.24` | Raise miners' salary (stone excavation efficiency +200%) | 1 | 200 | 15.62 | 4200 | 0 | 0 | 1550 | 0 | 12520 |
| `rusaca.25` | Design Montgolfier (reveals the whole map) | 1 | 0 | 15.62 | 0 | 0 | 0 | 5750 | 0 | 0 |
| `rusaca.26` | Develop medical science (heals all live units) | 1 | 50 | 31.25 | 0 | 0 | 0 | 200 | 0 | 200 |
| `rusaca.27` | Develop mathematics (artillery accuracy +35%) | 1 | -35 | 15.62 | 0 | 9540 | 0 | 12000 | 0 | 65200 |
| `rusaca.28` | Design new rigging types (ship speed +40%) | 1 | 40 | 15.62 | 0 | 65400 | 0 | 24050 | 0 | 0 |
| `rusaca.29` | Design new rib system and new hulls (battleship construction) | 1 | 0 | 15.62 | 0 | 32300 | 0 | 6800 | 9000 | 12800 |
| `rusaca.3` | Raise agriculturists' salary (harvesting +50%) | 1 | 50 | 15.62 | 0 | 3600 | 0 | 850 | 0 | 0 |
| `rusaca.30` | Train carpenters (shipbuilding speed x10) | 1 | -5000000 | 15.62 | 0 | 2300 | 42700 | 1150 | 0 | 0 |
| `rusaca.31` | Design wheellock (rate of fire +30%) | 1 | -30 | 15.62 | 0 | 0 | 6000 | 5500 | 4200 | 0 |
| `rusaca.32` | Design flintlock (musket cost -50%) | 1 | 0 | 15.62 | 0 | 0 | 0 | 6050 | 0 | 7750 |
| `rusaca.33` | Design paper cartridge and iron ramrod (rate of fire +30%) | 1 | -30 | 15.62 | 0 | 5000 | 0 | 5500 | 0 | 15200 |
| `rusaca.34` | Research improved steel grades for cuirasses (armoured soldier defence +2) | 1 | 2 | 15.62 | 0 | 0 | 0 | 9750 | 0 | 0 |
| `rusaca.35` | Design bayonet: barrel-inserted, bayonet with a tube (cold steel weapons +5) | 1 | 5 | 15.62 | 0 | 0 | 0 | 11500 | 0 | 0 |
| `rusaca.36` | Research new steel grades (18c musketeer/grenadier melee attack efficiency +25%) | 1 | 25 | 15.62 | 0 | 0 | 0 | 19500 | 0 | 0 |
| `rusaca.4` | Carry out field melioration (field capacity +200%) | 1 | 200 | 15.62 | 0 | 1000 | 0 | 475 | 0 | 0 |
| `rusaca.5` | Design new tackle and fishing nets (boat efficiency +100%) | 1 | 100 | 15.62 | 0 | 12400 | 0 | 2520 | 0 | 0 |
| `rusaca.6` | Develop new woodworking methods (frigate building) | 1 | 0 | 15.62 | 0 | 12400 | 0 | 7040 | 0 | 0 |
| `rusaca.7` | Build new shipyards for fishing boats (fishing boat cost -85%) | 1 | 0 | 15.62 | 0 | 7300 | 0 | 1220 | 0 | 0 |
| `rusaca.8` | Design new woodworking tools (woodcutting efficiency +100%) | 1 | 100 | 15.62 | 5500 | 0 | 0 | 550 | 0 | 0 |
| `rusaca.9` | Use new construction materials (durability of buildings +85) | 1 | 85 | 15.62 | 0 | 9400 | 7850 | 1150 | 0 | 0 |
| `rusart.cannon.1.1` | — | 2 | — | 10.0 | 0 | 1000 | 500 | 300 | 0 | 0 |
| `rusart.cannon.1.2` | — | 3 | — | 10.0 | 0 | 3000 | 1000 | 500 | 0 | 0 |
| `rusart.cannon.1.3` | — | 4 | — | 10.0 | 0 | 6000 | 2000 | 1000 | 0 | 0 |
| `rusart.cannon.1.4` | — | 5 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `rusart.cannon.1.5` | — | 6 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `rusart.cannon.1.6` | — | 7 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `rusart.cannon.2.1` | — | 2 | -2500000 | 10.0 | 0 | 0 | 0 | 500 | 1000 | 0 |
| `rusart.cannon.2.2` | — | 3 | -2500000 | 10.0 | 0 | 0 | 0 | 1000 | 2000 | 0 |
| `rusart.cannon.2.3` | — | 4 | -2500000 | 10.0 | 0 | 0 | 0 | 2000 | 3000 | 0 |
| `rusart.cannon.2.4` | — | 5 | -2000000 | 15.62 | 2560 | 0 | 0 | 0 | 0 | 0 |
| `rusart.cannon.2.5` | — | 6 | -2000000 | 15.62 | 3560 | 0 | 0 | 0 | 0 | 0 |
| `rusart.cannon.2.6` | — | 7 | -2000000 | 15.62 | 5560 | 0 | 0 | 0 | 0 | 0 |
| `rusart.howitzer.1.1` | — | 2 | — | 10.0 | 0 | 1000 | 500 | 300 | 0 | 0 |
| `rusart.howitzer.1.2` | — | 3 | — | 10.0 | 0 | 3000 | 1000 | 500 | 0 | 0 |
| `rusart.howitzer.1.3` | — | 4 | — | 10.0 | 0 | 6000 | 2000 | 1000 | 0 | 0 |
| `rusart.howitzer.1.4` | — | 5 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `rusart.howitzer.1.5` | — | 6 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `rusart.howitzer.1.6` | — | 7 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `rusart.howitzer.2.1` | — | 2 | -2500000 | 10.0 | 0 | 0 | 0 | 500 | 1000 | 0 |
| `rusart.howitzer.2.2` | — | 3 | -2500000 | 10.0 | 0 | 0 | 0 | 1000 | 2000 | 0 |
| `rusart.howitzer.2.3` | — | 4 | -2500000 | 10.0 | 0 | 0 | 0 | 2000 | 3000 | 0 |
| `rusart.howitzer.2.4` | — | 5 | -2000000 | 31.25 | 2560 | 0 | 0 | 0 | 0 | 0 |
| `rusart.howitzer.2.5` | — | 6 | -2000000 | 31.25 | 3560 | 0 | 0 | 0 | 0 | 0 |
| `rusart.howitzer.2.6` | — | 7 | -2000000 | 31.25 | 5560 | 0 | 0 | 0 | 0 | 0 |
| `rusba2.drummer18.2.1` | Barracks 18c drummer18 protection +15 (lvl 2) | 2 | 15 | 15.62 | 706 | 0 | 0 | 50 | 0 | 0 |
| `rusba2.grenadier.1.1` | Barracks 18c grenadier damage +2 (lvl 2) | 2 | 2 | 15.62 | 2000 | 0 | 0 | 800 | 0 | 0 |
| `rusba2.grenadier.1.2` | Barracks 18c grenadier damage +3 (lvl 3) | 3 | 3 | 15.62 | 12000 | 0 | 0 | 1800 | 0 | 0 |
| `rusba2.grenadier.1.3` | Barracks 18c grenadier damage +4 (lvl 4) | 4 | 4 | 15.62 | 32000 | 0 | 0 | 2800 | 0 | 0 |
| `rusba2.grenadier.1.4` | Barracks 18c grenadier damage +5 (lvl 5) | 5 | 5 | 15.62 | 42000 | 0 | 0 | 3800 | 0 | 0 |
| `rusba2.grenadier.1.5` | Barracks 18c grenadier damage +6 (lvl 6) | 6 | 6 | 15.62 | 52000 | 0 | 0 | 4800 | 0 | 0 |
| `rusba2.grenadier.1.6` | Barracks 18c grenadier damage +1500 (lvl 7) | 7 | 1500 | 15.62 | 62000 | 0 | 0 | 15800 | 0 | 0 |
| `rusba2.grenadier.2.1` | Barracks 18c grenadier protection +1 (lvl 2) | 2 | 1 | 15.62 | 3706 | 0 | 0 | 350 | 0 | 0 |
| `rusba2.grenadier.2.2` | Barracks 18c grenadier protection +2 (lvl 3) | 3 | 2 | 15.62 | 11030 | 0 | 0 | 1350 | 0 | 0 |
| `rusba2.grenadier.2.3` | Barracks 18c grenadier protection +3 (lvl 4) | 4 | 3 | 15.62 | 35706 | 0 | 0 | 3000 | 0 | 0 |
| `rusba2.grenadier.2.4` | Barracks 18c grenadier protection +1 (lvl 5) | 5 | 1 | 15.62 | 36556 | 0 | 0 | 3350 | 0 | 0 |
| `rusba2.grenadier.2.5` | Barracks 18c grenadier protection +2 (lvl 6) | 6 | 2 | 15.62 | 30060 | 0 | 0 | 1350 | 0 | 0 |
| `rusba2.grenadier.2.6` | Barracks 18c grenadier protection +3 (lvl 7) | 7 | 3 | 15.62 | 64000 | 0 | 0 | 1350 | 0 | 0 |
| `rusba2.musketeer18.1.1` | Barracks 18c musketeer18 damage +1 (lvl 2) | 2 | 1 | 15.62 | 1000 | 0 | 0 | 800 | 0 | 0 |
| `rusba2.musketeer18.1.2` | Barracks 18c musketeer18 damage +1 (lvl 3) | 3 | 1 | 15.62 | 1500 | 0 | 0 | 800 | 0 | 0 |
| `rusba2.musketeer18.1.3` | Barracks 18c musketeer18 damage +2 (lvl 4) | 4 | 2 | 15.62 | 2000 | 0 | 0 | 800 | 0 | 0 |
| `rusba2.musketeer18.1.4` | Barracks 18c musketeer18 damage +2 (lvl 5) | 5 | 2 | 15.62 | 2500 | 0 | 0 | 800 | 0 | 0 |
| `rusba2.musketeer18.1.5` | Barracks 18c musketeer18 damage +3 (lvl 6) | 6 | 3 | 15.62 | 3000 | 0 | 0 | 800 | 0 | 0 |
| `rusba2.musketeer18.1.6` | Barracks 18c musketeer18 damage +3 (lvl 7) | 7 | 3 | 15.62 | 3500 | 0 | 0 | 800 | 0 | 0 |
| `rusba2.musketeer18.2.1` | Barracks 18c musketeer18 protection +1 (lvl 2) | 2 | 1 | 15.62 | 3706 | 0 | 0 | 350 | 0 | 0 |
| `rusba2.musketeer18.2.2` | Barracks 18c musketeer18 protection +2 (lvl 3) | 3 | 2 | 15.62 | 11030 | 0 | 0 | 1350 | 0 | 0 |
| `rusba2.musketeer18.2.3` | Barracks 18c musketeer18 protection +2 (lvl 4) | 4 | 2 | 15.62 | 35706 | 0 | 0 | 4000 | 0 | 0 |
| `rusba2.musketeer18.2.4` | Barracks 18c musketeer18 protection +1 (lvl 5) | 5 | 1 | 15.62 | 36556 | 0 | 0 | 4350 | 0 | 0 |
| `rusba2.musketeer18.2.5` | Barracks 18c musketeer18 protection +2 (lvl 6) | 6 | 2 | 15.62 | 30060 | 0 | 0 | 1350 | 0 | 0 |
| `rusba2.musketeer18.2.6` | Barracks 18c musketeer18 protection +2 (lvl 7) | 7 | 2 | 15.62 | 37600 | 0 | 0 | 1350 | 0 | 0 |
| `rusba2.officer18.1.1` | Barracks 18c officer18 damage +30 (lvl 2) | 2 | 30 | 15.62 | 1000 | 0 | 0 | 800 | 0 | 0 |
| `rusba2.officer18.2.1` | Barracks 18c officer18 protection +12 (lvl 2) | 2 | 12 | 15.62 | 1706 | 0 | 0 | 350 | 0 | 0 |
| `rusba2.pikeman18.1.1` | Barracks 18c pikeman18 damage +2 (lvl 2) | 2 | 2 | 15.62 | 2000 | 0 | 0 | 800 | 0 | 0 |
| `rusba2.pikeman18.1.2` | Barracks 18c pikeman18 damage +2 (lvl 3) | 3 | 2 | 15.62 | 8000 | 0 | 0 | 1200 | 0 | 0 |
| `rusba2.pikeman18.1.3` | Barracks 18c pikeman18 damage +2 (lvl 4) | 4 | 2 | 15.62 | 20000 | 0 | 0 | 2500 | 0 | 0 |
| `rusba2.pikeman18.1.4` | Barracks 18c pikeman18 damage +2 (lvl 5) | 5 | 2 | 15.62 | 32000 | 0 | 0 | 2800 | 0 | 0 |
| `rusba2.pikeman18.1.5` | Barracks 18c pikeman18 damage +2 (lvl 6) | 6 | 2 | 15.62 | 32000 | 0 | 0 | 3800 | 0 | 0 |
| `rusba2.pikeman18.1.6` | Barracks 18c pikeman18 damage +2 (lvl 7) | 7 | 2 | 15.62 | 40500 | 0 | 0 | 4800 | 0 | 0 |
| `rusba2.pikeman18.2.1` | Barracks 18c pikeman18 protection +2 (lvl 2) | 2 | 2 | 15.62 | 1500 | 0 | 0 | 500 | 0 | 0 |
| `rusba2.pikeman18.2.2` | Barracks 18c pikeman18 protection +3 (lvl 3) | 3 | 3 | 15.62 | 7000 | 0 | 0 | 1500 | 0 | 0 |
| `rusba2.pikeman18.2.3` | Barracks 18c pikeman18 protection +2 (lvl 4) | 4 | 2 | 15.62 | 37000 | 0 | 0 | 2000 | 0 | 0 |
| `rusba2.pikeman18.2.4` | Barracks 18c pikeman18 protection +3 (lvl 5) | 5 | 3 | 15.62 | 37000 | 0 | 0 | 5500 | 0 | 0 |
| `rusba2.pikeman18.2.5` | Barracks 18c pikeman18 protection +2 (lvl 6) | 6 | 2 | 15.62 | 37000 | 0 | 0 | 5500 | 0 | 0 |
| `rusba2.pikeman18.2.6` | Barracks 18c pikeman18 protection +3 (lvl 7) | 7 | 3 | 15.62 | 64600 | 0 | 0 | 5500 | 0 | 0 |
| `rusbar.1` | — | 1 | 140 | 15.62 | 750 | 0 | 0 | 250 | 0 | 0 |
| `rusbar.2` | — | 2 | 180 | 15.62 | 25600 | 0 | 0 | 3350 | 2000 | 0 |
| `rusbar.drummerrus.2.1` | Barracks 17c drummerrus protection +10 (lvl 2) | 2 | 10 | 15.62 | 706 | 0 | 0 | 50 | 0 | 0 |
| `rusbar.officerrus.1.1` | Barracks 17c officerrus damage +30 (lvl 2) | 2 | 30 | 15.62 | 100 | 0 | 0 | 50 | 0 | 0 |
| `rusbar.officerrus.2.1` | Barracks 17c officerrus protection +10 (lvl 2) | 2 | 10 | 15.62 | 1850 | 0 | 0 | 450 | 0 | 0 |
| `rusbar.pikemanrus.1.1` | Barracks 17c pikemanrus damage +1 (lvl 2) | 2 | 1 | 15.62 | 200 | 0 | 0 | 50 | 0 | 0 |
| `rusbar.pikemanrus.1.2` | Barracks 17c pikemanrus damage +2 (lvl 3) | 3 | 2 | 15.62 | 1300 | 0 | 0 | 300 | 0 | 0 |
| `rusbar.pikemanrus.1.3` | Barracks 17c pikemanrus damage +2 (lvl 4) | 4 | 2 | 15.62 | 3600 | 0 | 0 | 450 | 0 | 0 |
| `rusbar.pikemanrus.1.4` | Barracks 17c pikemanrus damage +1 (lvl 5) | 5 | 1 | 15.62 | 7200 | 0 | 0 | 1850 | 0 | 0 |
| `rusbar.pikemanrus.1.5` | Barracks 17c pikemanrus damage +2 (lvl 6) | 6 | 2 | 15.62 | 16030 | 0 | 0 | 2000 | 0 | 0 |
| `rusbar.pikemanrus.1.6` | — | 7 | 2 | 15.62 | 15000 | 0 | 0 | 1875 | 0 | 0 |
| `rusbar.pikemanrus.2.1` | Barracks 17c pikemanrus protection +1 (lvl 2) | 2 | 1 | 15.62 | 150 | 0 | 0 | 50 | 0 | 0 |
| `rusbar.pikemanrus.2.2` | Barracks 17c pikemanrus protection +1 (lvl 3) | 3 | 1 | 15.62 | 900 | 0 | 0 | 175 | 0 | 0 |
| `rusbar.pikemanrus.2.3` | Barracks 17c pikemanrus protection +2 (lvl 4) | 4 | 2 | 15.62 | 4500 | 0 | 0 | 300 | 0 | 0 |
| `rusbar.pikemanrus.2.4` | Barracks 17c pikemanrus protection +1 (lvl 5) | 5 | 1 | 15.62 | 9005 | 0 | 0 | 507 | 0 | 0 |
| `rusbar.pikemanrus.2.5` | Barracks 17c pikemanrus protection +1 (lvl 6) | 6 | 1 | 15.62 | 18010 | 0 | 0 | 3050 | 0 | 0 |
| `rusbar.pikemanrus.2.6` | — | 7 | 2 | 15.62 | 11250 | 0 | 0 | 1500 | 0 | 0 |
| `rusbar.strelet.1.1` | Barracks 17c strelet damage +1 (lvl 2) | 2 | 1 | 15.62 | 2000 | 0 | 0 | 100 | 0 | 0 |
| `rusbar.strelet.1.2` | Barracks 17c strelet damage +1 (lvl 3) | 3 | 1 | 15.62 | 1000 | 0 | 0 | 300 | 0 | 0 |
| `rusbar.strelet.1.3` | Barracks 17c strelet damage +2 (lvl 4) | 4 | 2 | 15.62 | 500 | 0 | 0 | 700 | 0 | 0 |
| `rusbar.strelet.2.1` | Barracks 17c strelet protection +3 (lvl 2) | 2 | 3 | 15.62 | 170 | 0 | 0 | 50 | 100 | 0 |
| `rusbar.strelet.2.2` | Barracks 17c strelet protection +3 (lvl 3) | 3 | 3 | 15.62 | 405 | 0 | 0 | 150 | 200 | 0 |
| `rusbar.strelet.2.3` | Barracks 17c strelet protection +2 (lvl 4) | 4 | 2 | 15.62 | 1570 | 0 | 0 | 100 | 350 | 0 |
| `rusbar.strelet.2.4` | Barracks 17c strelet protection +2 (lvl 5) | 5 | 2 | 15.62 | 1556 | 0 | 0 | 550 | 100 | 0 |
| `rusbar.strelet.2.5` | Barracks 17c strelet protection +1 (lvl 6) | 6 | 1 | 15.62 | 1060 | 0 | 0 | 850 | 400 | 0 |
| `rusbar.strelet.2.6` | Barracks 17c strelet protection +1 (lvl 7) | 7 | 1 | 15.62 | 3700 | 0 | 0 | 650 | 700 | 0 |
| `rusbla.1` | Manufacture agricultural equipment (field capacity +100%) | 1 | 100 | 15.62 | 0 | 400 | 0 | 90 | 0 | 0 |
| `rusbla.2` | Forge metal armature and gratings (building defence +50) | 1 | 50 | 15.62 | 0 | 0 | 12320 | 350 | 900 | 0 |
| `rusbla.3` | Forge harnesses for horses (mounted units recruitment speed -33%) | 1 | -3333333 | 15.62 | 0 | 0 | 0 | 3650 | 5300 | 8200 |
| `rusbla.4` | Forge bayonets and broadswords for infantry (18c musketeer/grenadier melee attack +5) | 1 | 5 | 15.62 | 0 | 1300 | 0 | 1500 | 900 | 5000 |
| `rusbla.5` | Forge new types of broadswords and sabres (cavalry and sword clansman attack +5) | 1 | 5 | 15.62 | 0 | 0 | 0 | 4000 | 7900 | 0 |
| `rusbla.6` | Forge new cuirasses (armoured soldiers defence +2) | 1 | 2 | 15.62 | 0 | 0 | 0 | 4950 | 10500 | 0 |
| `ruscen.1` | — | 1 | 0 | 9.38 | 30000 | 0 | 0 | 5000 | 2000 | 2000 |
| `ruspor.1` | — | 1 | 50 | 46.88 | 0 | 20000 | 0 | 1500 | 0 | 0 |
| `russta.cossackdon.2.1` | Stable cossackdon protection +1 (lvl 2) | 2 | 1 | 15.62 | 2000 | 0 | 0 | 1350 | 0 | 0 |
| `russta.cossackdon.2.2` | Stable cossackdon protection +1 (lvl 3) | 3 | 1 | 15.62 | 1500 | 0 | 0 | 2100 | 0 | 0 |
| `russta.cossackdon.2.3` | Stable cossackdon protection +1 (lvl 4) | 4 | 1 | 15.62 | 5000 | 0 | 0 | 3300 | 0 | 0 |
| `russta.cossackdon.2.4` | Stable cossackdon protection +1 (lvl 5) | 5 | 1 | 15.62 | 10500 | 0 | 0 | 4400 | 0 | 0 |
| `russta.cossackdon.2.5` | Stable cossackdon protection +2 (lvl 6) | 6 | 2 | 15.62 | 12600 | 0 | 0 | 5500 | 0 | 0 |
| `russta.cossackdon.2.6` | Stable cossackdon protection +2 (lvl 7) | 7 | 2 | 15.62 | 40000 | 0 | 0 | 6000 | 0 | 0 |
| `russta.cuirassier.1.1` | Stable cuirassier damage +1 (lvl 2) | 2 | 1 | 15.62 | 12000 | 0 | 0 | 600 | 0 | 0 |
| `russta.cuirassier.1.2` | Stable cuirassier damage +1 (lvl 3) | 3 | 1 | 15.62 | 32000 | 0 | 0 | 1300 | 0 | 0 |
| `russta.cuirassier.1.3` | Stable cuirassier damage +1 (lvl 4) | 4 | 1 | 15.62 | 62000 | 0 | 0 | 2200 | 0 | 0 |
| `russta.cuirassier.1.4` | Stable cuirassier damage +2 (lvl 5) | 5 | 2 | 15.62 | 61000 | 0 | 0 | 3150 | 0 | 0 |
| `russta.cuirassier.1.5` | Stable cuirassier damage +2 (lvl 6) | 6 | 2 | 15.62 | 57055 | 0 | 0 | 4100 | 0 | 0 |
| `russta.cuirassier.1.6` | Stable cuirassier damage +3 (lvl 7) | 7 | 3 | 15.62 | 49050 | 0 | 0 | 8020 | 0 | 0 |
| `russta.cuirassier.2.1` | Stable cuirassier protection +2 (lvl 2) | 2 | 2 | 15.62 | 1760 | 0 | 0 | 350 | 1000 | 0 |
| `russta.cuirassier.2.2` | Stable cuirassier protection +3 (lvl 3) | 3 | 3 | 15.62 | 3000 | 0 | 0 | 750 | 2000 | 0 |
| `russta.cuirassier.2.3` | Stable cuirassier protection +3 (lvl 4) | 4 | 3 | 15.62 | 7600 | 0 | 0 | 300 | 3030 | 0 |
| `russta.cuirassier.2.4` | Stable cuirassier protection +2 (lvl 5) | 5 | 2 | 15.62 | 8700 | 0 | 0 | 6200 | 100 | 0 |
| `russta.cuirassier.2.5` | Stable cuirassier protection +1 (lvl 6) | 6 | 1 | 15.62 | 8700 | 0 | 0 | 2350 | 5000 | 0 |
| `russta.cuirassier.2.6` | Stable cuirassier protection +1 (lvl 7) | 7 | 1 | 15.62 | 9700 | 0 | 0 | 4444 | 7060 | 0 |
| `russta.dragoon18.1.1` | Stable dragoon18 damage +2 (lvl 2) | 2 | 2 | 15.62 | 2000 | 0 | 0 | 100 | 0 | 0 |
| `russta.dragoon18.1.2` | Stable dragoon18 damage +2 (lvl 3) | 3 | 2 | 15.62 | 9000 | 0 | 0 | 350 | 0 | 0 |
| `russta.dragoon18.1.3` | Stable dragoon18 damage +4 (lvl 4) | 4 | 4 | 15.62 | 12000 | 0 | 0 | 400 | 0 | 0 |
| `russta.dragoon18.1.4` | Stable dragoon18 damage +2 (lvl 5) | 5 | 2 | 15.62 | 23000 | 0 | 0 | 580 | 0 | 0 |
| `russta.dragoon18.1.5` | Stable dragoon18 damage +2 (lvl 6) | 6 | 2 | 15.62 | 32000 | 0 | 0 | 680 | 0 | 0 |
| `russta.dragoon18.1.6` | Stable dragoon18 damage +4 (lvl 7) | 7 | 4 | 15.62 | 42000 | 0 | 0 | 780 | 0 | 0 |
| `russta.dragoon18.2.1` | Stable dragoon18 protection +1 (lvl 2) | 2 | 1 | 15.62 | 760 | 0 | 0 | 935 | 0 | 0 |
| `russta.dragoon18.2.2` | Stable dragoon18 protection +1 (lvl 3) | 3 | 1 | 15.62 | 1260 | 0 | 0 | 1150 | 0 | 0 |
| `russta.dragoon18.2.3` | Stable dragoon18 protection +2 (lvl 4) | 4 | 2 | 15.62 | 15600 | 0 | 0 | 2350 | 0 | 0 |
| `russta.dragoon18.2.4` | Stable dragoon18 protection +1 (lvl 5) | 5 | 1 | 15.62 | 17600 | 0 | 0 | 3350 | 0 | 0 |
| `russta.dragoon18.2.5` | Stable dragoon18 protection +2 (lvl 6) | 6 | 2 | 15.62 | 19600 | 0 | 0 | 5350 | 0 | 0 |
| `russta.dragoon18.2.6` | Stable dragoon18 protection +3 (lvl 7) | 7 | 3 | 15.62 | 21760 | 0 | 0 | 9350 | 0 | 0 |
| `russta.hussar.1.1` | Stable hussar damage +1 (lvl 2) | 2 | 1 | 15.62 | 0 | 0 | 0 | 1800 | 1000 | 0 |
| `russta.hussar.1.2` | Stable hussar damage +2 (lvl 3) | 3 | 2 | 15.62 | 0 | 0 | 0 | 3800 | 2000 | 0 |
| `russta.hussar.1.3` | Stable hussar damage +3 (lvl 4) | 4 | 3 | 15.62 | 20200 | 0 | 0 | 0 | 2000 | 0 |
| `russta.hussar.1.4` | Stable hussar damage +4 (lvl 5) | 5 | 4 | 15.62 | 32000 | 0 | 0 | 0 | 3000 | 0 |
| `russta.hussar.1.5` | Stable hussar damage +1 (lvl 6) | 6 | 1 | 15.62 | 49200 | 0 | 0 | 0 | 3500 | 0 |
| `russta.hussar.1.6` | Stable hussar damage +1 (lvl 7) | 7 | 1 | 15.62 | 20000 | 0 | 0 | 0 | 6000 | 0 |
| `russta.hussar.2.1` | Stable hussar protection +1 (lvl 2) | 2 | 1 | 15.62 | 1760 | 0 | 0 | 1350 | 0 | 0 |
| `russta.hussar.2.2` | Stable hussar protection +1 (lvl 3) | 3 | 1 | 15.62 | 1900 | 0 | 0 | 2350 | 0 | 0 |
| `russta.hussar.2.3` | Stable hussar protection +1 (lvl 4) | 4 | 1 | 15.62 | 1600 | 0 | 0 | 5350 | 0 | 0 |
| `russta.hussar.2.4` | Stable hussar protection +2 (lvl 5) | 5 | 2 | 15.62 | 8000 | 0 | 0 | 8350 | 0 | 0 |
| `russta.hussar.2.5` | Stable hussar protection +2 (lvl 6) | 6 | 2 | 15.62 | 2000 | 0 | 0 | 15350 | 0 | 0 |
| `russta.hussar.2.6` | Stable hussar protection +3 (lvl 7) | 7 | 3 | 15.62 | 56000 | 0 | 0 | 20150 | 0 | 0 |
| `russta.vityaz.1.1` | Stable vityaz damage +1 (lvl 2) | 2 | 1 | 15.62 | 500 | 0 | 0 | 100 | 0 | 0 |
| `russta.vityaz.1.2` | Stable vityaz damage +2 (lvl 3) | 3 | 2 | 15.62 | 900 | 0 | 0 | 220 | 0 | 0 |
| `russta.vityaz.1.3` | Stable vityaz damage +1 (lvl 4) | 4 | 1 | 15.62 | 4400 | 0 | 0 | 280 | 0 | 0 |
| `russta.vityaz.1.4` | Stable vityaz damage +1 (lvl 5) | 5 | 1 | 15.62 | 2250 | 0 | 0 | 320 | 0 | 0 |
| `russta.vityaz.1.5` | Stable vityaz damage +1 (lvl 6) | 6 | 1 | 15.62 | 3030 | 0 | 0 | 600 | 0 | 0 |
| `russta.vityaz.1.6` | Stable vityaz damage +1 (lvl 7) | 7 | 1 | 15.62 | 7000 | 0 | 0 | 1800 | 0 | 0 |
| `russta.vityaz.2.1` | Stable vityaz protection +2 (lvl 2) | 2 | 2 | 15.62 | 200 | 0 | 0 | 135 | 300 | 0 |
| `russta.vityaz.2.2` | Stable vityaz protection +3 (lvl 3) | 3 | 3 | 15.62 | 600 | 0 | 0 | 100 | 400 | 0 |
| `russta.vityaz.2.3` | Stable vityaz protection +3 (lvl 4) | 4 | 3 | 15.62 | 800 | 0 | 0 | 200 | 560 | 0 |
| `russta.vityaz.2.4` | Stable vityaz protection +2 (lvl 5) | 5 | 2 | 15.62 | 1600 | 0 | 0 | 300 | 640 | 0 |
| `russta.vityaz.2.5` | Stable vityaz protection +1 (lvl 6) | 6 | 1 | 15.62 | 3200 | 0 | 0 | 350 | 300 | 0 |
| `russta.vityaz.2.6` | Stable vityaz protection +1 (lvl 7) | 7 | 1 | 15.62 | 16000 | 0 | 0 | 1000 | 5000 | 0 |
| `russwa.1` | — | 2 | 5 | 0.03 | 0 | 0 | 500 | 0 | 0 | 0 |
| `rustow.1` | — | 2 | -20 | 31.25 | 0 | 0 | 0 | 250 | 0 | 0 |
| `rustow.2` | — | 3 | -20 | 31.25 | 0 | 0 | 0 | 0 | 350 | 0 |
| `rustow.3` | — | 4 | -10 | 31.25 | 0 | 0 | 0 | 0 | 0 | 400 |
| `rustow.4` | — | 5 | -10 | 31.25 | 0 | 0 | 0 | 0 | 450 | 0 |
| `rustow.5` | — | 6 | -10 | 31.25 | 0 | 0 | 0 | 0 | 0 | 500 |
| `ukrwwa.1` | — | 2 | 5 | 0.03 | 0 | 400 | 0 | 0 | 0 | 0 |

### ukr — Ukraine

| sid | имя (EN) | level | value | время (s) | F | W | S | G | I | C |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `eurcoa.1` | — | 2 | 5 | 9.38 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `eurcoa.2` | — | 3 | 8 | 9.38 | 5250 | 0 | 0 | 4950 | 0 | 0 |
| `eurcoa.3` | — | 4 | 10 | 9.38 | 12500 | 0 | 0 | 9250 | 0 | 0 |
| `eurcoa.4` | — | 5 | 12 | 9.38 | 15800 | 0 | 0 | 18500 | 0 | 0 |
| `eurcoa.5` | — | 6 | 15 | 9.38 | 19800 | 0 | 0 | 21050 | 0 | 0 |
| `eurcoa.6` | — | 7 | 40 | 9.38 | 7080 | 0 | 0 | 25410 | 0 | 0 |
| `eurgol.1` | — | 2 | 5 | 9.38 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `eurgol.2` | — | 3 | 8 | 9.38 | 5250 | 0 | 0 | 4950 | 0 | 0 |
| `eurgol.3` | — | 4 | 10 | 9.38 | 12500 | 0 | 0 | 9250 | 0 | 0 |
| `eurgol.4` | — | 5 | 12 | 9.38 | 15800 | 0 | 0 | 18500 | 0 | 0 |
| `eurgol.5` | — | 6 | 15 | 9.38 | 19800 | 0 | 0 | 21050 | 0 | 0 |
| `eurgol.6` | — | 7 | 40 | 9.38 | 7080 | 0 | 0 | 25410 | 0 | 0 |
| `euriro.1` | — | 2 | 5 | 9.38 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `euriro.2` | — | 3 | 8 | 9.38 | 5250 | 0 | 0 | 4950 | 0 | 0 |
| `euriro.3` | — | 4 | 10 | 9.38 | 12500 | 0 | 0 | 9250 | 0 | 0 |
| `euriro.4` | — | 5 | 12 | 9.38 | 15800 | 0 | 0 | 18500 | 0 | 0 |
| `euriro.5` | — | 6 | 15 | 9.38 | 19800 | 0 | 0 | 21050 | 0 | 0 |
| `euriro.6` | — | 7 | 40 | 9.38 | 7080 | 0 | 0 | 25410 | 0 | 0 |
| `ukraca.1` | Cultivate new cultures of wheat (harvesting +40%) | 1 | 40 | 15.62 | 0 | 200 | 0 | 325 | 0 | 0 |
| `ukraca.10` | Raise builders' salary (building construction time -75%) | 1 | -7500000 | 15.62 | 0 | 0 | 0 | 1750 | 0 | 0 |
| `ukraca.11` | Research new fortification grades %color(FFAA00)%(durability of walls and towers +80) | — | — | — | — | — | — | — | — | — |
| `ukraca.12` | Improve firearms: rifled barrel (fire power +10%) | 1 | 10 | 15.62 | 0 | 0 | 0 | 0 | 5000 | 0 |
| `ukraca.13` | Research granular gunpowder (fire power +10%) | 1 | 10 | 15.62 | 0 | 0 | 0 | 4000 | 0 | 0 |
| `ukraca.14` | Research new sulphur purification methods (fire power +15%) | 1 | 15 | 15.62 | 0 | 0 | 0 | 7000 | 0 | 0 |
| `ukraca.15` | Research new nitre purification methods (fire power +25%) | 1 | 25 | 15.62 | 0 | 0 | 0 | 0 | 0 | 11000 |
| `ukraca.16` | Research improved additions to gunpowder formula (artillery range +5%) | 1 | 5 | 15.62 | 0 | 0 | 0 | 2000 | 12150 | 0 |
| `ukraca.17` | Design new barrel types: unicorn, carronade (artillery range +10%) | 1 | 10 | 15.62 | 0 | 0 | 3000 | 4550 | 19200 | 0 |
| `ukraca.18` | Design more durable gun carriage: Gribovalle system (artillery durability +50%) | 1 | 50 | 15.62 | 0 | 0 | 0 | 500 | 3830 | 1500 |
| `ukraca.19` | %color(FFAA00)%Design multi-barrelled cannon | — | — | — | — | — | — | — | — | — |
| `ukraca.2` | Cultivate new cultures of rye (harvesting +50%) | 1 | 50 | 15.62 | 0 | 2400 | 0 | 625 | 0 | 0 |
| `ukraca.20` | Research new sighting devices for artillery (artillery accuracy +35%) | 1 | -35 | 15.62 | 0 | 3540 | 0 | 2000 | 0 | 7250 |
| `ukraca.21` | Finance artillery repair shops (repair all artillery) | 1 | 25 | 15.62 | 0 | 350 | 0 | 100 | 0 | 250 |
| `ukraca.22` | Develop geology (previously hidden deposits appear on the map) | 1 | 0 | 15.62 | 0 | 0 | 0 | 250 | 0 | 0 |
| `ukraca.23` | Develop mining (stone excavation efficiency +100%) | 1 | 100 | 15.62 | 0 | 0 | 0 | 1550 | 3000 | 0 |
| `ukraca.24` | Raise miners' salary (stone excavation efficiency +200%) | 1 | 200 | 15.62 | 4200 | 0 | 0 | 1550 | 0 | 12520 |
| `ukraca.25` | Design Montgolfier (reveals the whole map) | 1 | 0 | 15.62 | 0 | 0 | 0 | 12750 | 0 | 0 |
| `ukraca.26` | Develop medical science (heals all live units) | 1 | 50 | 31.25 | 0 | 0 | 0 | 200 | 0 | 200 |
| `ukraca.27` | Develop mathematics (artillery accuracy +35%) | 1 | -35 | 15.62 | 0 | 9540 | 0 | 12000 | 0 | 65200 |
| `ukraca.28` | Design new rigging types (ship speed +40%) | 1 | 40 | 15.62 | 0 | 0 | 0 | 900 | 0 | 0 |
| `ukraca.29` | Design new rib system and new hulls %color(FFAA00)%(battleship construction) | — | — | — | — | — | — | — | — | — |
| `ukraca.3` | Raise agriculturists' salary (harvesting +50%) | 1 | 50 | 15.62 | 0 | 3600 | 0 | 850 | 0 | 0 |
| `ukraca.30` | Train carpenters (shipbuilding speed x10) | 1 | -5000000 | 15.62 | 0 | 2300 | 42700 | 1150 | 0 | 0 |
| `ukraca.31` | Design wheellock (rate of fire +30%) | 1 | -30 | 15.62 | 0 | 0 | 6000 | 5500 | 4200 | 0 |
| `ukraca.32` | Design flintlock %color(FFAA00)%(musket cost -50%) | — | — | — | — | — | — | — | — | — |
| `ukraca.33` | Design paper cartridge and iron ramrod (rate of fire +30%) | 1 | -30 | 15.62 | 0 | 5000 | 0 | 5500 | 0 | 15200 |
| `ukraca.34` | Research improved steel grades for cuirasses %color(FFAA00)%(armoured soldier defence +2) | — | — | — | — | — | — | — | — | — |
| `ukraca.35` | Design bayonet: barrel-inserted, bayonet with a tube %color(FFAA00)%(cold steel weapons +5) | — | — | — | — | — | — | — | — | — |
| `ukraca.36` | Research new steel grades %color(FFAA00)%(18c musketeer/grenadier melee attack efficiency +25%) | — | — | — | — | — | — | — | — | — |
| `ukraca.4` | Carry out field melioration (field capacity +200%) | 1 | 200 | 15.62 | 0 | 1000 | 0 | 475 | 0 | 0 |
| `ukraca.5` | Design new tackle and fishing nets (boat efficiency +100%) | 1 | 100 | 15.62 | 0 | 12400 | 0 | 2520 | 0 | 0 |
| `ukraca.6` | Develop new woodworking methods %color(FFAA00)%(frigate building) | — | — | — | — | — | — | — | — | — |
| `ukraca.7` | Build new shipyards for fishing boats (fishing boat cost -85%) | 1 | 0 | 15.62 | 0 | 7300 | 0 | 1220 | 0 | 0 |
| `ukraca.8` | Design new woodworking tools (woodcutting efficiency +100%) | 1 | 100 | 15.62 | 5500 | 0 | 0 | 550 | 0 | 0 |
| `ukraca.9` | Use new construction materials (durability of buildings +85) | 1 | 85 | 15.62 | 0 | 3200 | 7850 | 950 | 0 | 0 |
| `ukrart.cannon.1.1` | — | 2 | — | 10.0 | 0 | 1000 | 500 | 300 | 0 | 0 |
| `ukrart.cannon.1.2` | — | 3 | — | 10.0 | 0 | 3000 | 1000 | 500 | 0 | 0 |
| `ukrart.cannon.1.3` | — | 4 | — | 10.0 | 0 | 6000 | 2000 | 1000 | 0 | 0 |
| `ukrart.cannon.1.4` | — | 5 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `ukrart.cannon.1.5` | — | 6 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `ukrart.cannon.1.6` | — | 7 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `ukrart.cannon.2.1` | — | 2 | -2500000 | 10.0 | 0 | 0 | 0 | 500 | 1000 | 0 |
| `ukrart.cannon.2.2` | — | 3 | -2500000 | 10.0 | 0 | 0 | 0 | 1000 | 2000 | 0 |
| `ukrart.cannon.2.3` | — | 4 | -2500000 | 10.0 | 0 | 0 | 0 | 2000 | 3000 | 0 |
| `ukrart.cannon.2.4` | — | 5 | -2000000 | 15.62 | 2560 | 0 | 0 | 0 | 0 | 0 |
| `ukrart.cannon.2.5` | — | 6 | -2000000 | 15.62 | 3560 | 0 | 0 | 0 | 0 | 0 |
| `ukrart.cannon.2.6` | — | 7 | -2000000 | 15.62 | 5560 | 0 | 0 | 0 | 0 | 0 |
| `ukrart.howitzer.1.1` | — | 2 | — | 10.0 | 0 | 1000 | 500 | 300 | 0 | 0 |
| `ukrart.howitzer.1.2` | — | 3 | — | 10.0 | 0 | 3000 | 1000 | 500 | 0 | 0 |
| `ukrart.howitzer.1.3` | — | 4 | — | 10.0 | 0 | 6000 | 2000 | 1000 | 0 | 0 |
| `ukrart.howitzer.1.4` | — | 5 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `ukrart.howitzer.1.5` | — | 6 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `ukrart.howitzer.1.6` | — | 7 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `ukrart.howitzer.2.1` | — | 2 | -2500000 | 10.0 | 0 | 0 | 0 | 500 | 1000 | 0 |
| `ukrart.howitzer.2.2` | — | 3 | -2500000 | 10.0 | 0 | 0 | 0 | 1000 | 2000 | 0 |
| `ukrart.howitzer.2.3` | — | 4 | -2500000 | 10.0 | 0 | 0 | 0 | 2000 | 3000 | 0 |
| `ukrart.howitzer.2.4` | — | 5 | -2000000 | 31.25 | 2560 | 0 | 0 | 0 | 0 | 0 |
| `ukrart.howitzer.2.5` | — | 6 | -2000000 | 31.25 | 3560 | 0 | 0 | 0 | 0 | 0 |
| `ukrart.howitzer.2.6` | — | 7 | -2000000 | 31.25 | 5560 | 0 | 0 | 0 | 0 | 0 |
| `ukrbar.1` | — | 1 | 140 | 15.62 | 750 | 0 | 0 | 250 | 0 | 0 |
| `ukrbar.2` | — | 2 | 180 | 15.62 | 5600 | 0 | 0 | 1350 | 1900 | 0 |
| `ukrbar.serdiuk.1.1` | Barracks 17c serdiuk damage +2 (lvl 2) | 2 | 2 | 15.62 | 5400 | 0 | 0 | 350 | 0 | 0 |
| `ukrbar.serdiuk.1.2` | Barracks 17c serdiuk damage +2 (lvl 3) | 3 | 2 | 15.62 | 22000 | 0 | 0 | 800 | 0 | 0 |
| `ukrbar.serdiuk.1.3` | Barracks 17c serdiuk damage +2 (lvl 4) | 4 | 2 | 15.62 | 32400 | 0 | 0 | 5800 | 0 | 0 |
| `ukrbar.serdiuk.1.4` | Barracks 17c serdiuk damage +2 (lvl 5) | 5 | 2 | 15.62 | 42010 | 0 | 0 | 6800 | 0 | 0 |
| `ukrbar.serdiuk.1.5` | Barracks 17c serdiuk damage +2 (lvl 6) | 6 | 2 | 15.62 | 52300 | 0 | 0 | 1800 | 7400 | 0 |
| `ukrbar.serdiuk.1.6` | — | 7 | 3 | 15.62 | 60000 | 0 | 0 | 8000 | 0 | 0 |
| `ukrbar.serdiuk.2.1` | Barracks 17c serdiuk protection +1 (lvl 2) | 2 | 1 | 15.62 | 200 | 0 | 0 | 40 | 0 | 0 |
| `ukrbar.serdiuk.2.2` | Barracks 17c serdiuk protection +2 (lvl 3) | 3 | 2 | 15.62 | 600 | 0 | 0 | 120 | 0 | 0 |
| `ukrbar.serdiuk.2.3` | Barracks 17c serdiuk protection +2 (lvl 4) | 4 | 2 | 15.62 | 1500 | 0 | 0 | 300 | 0 | 0 |
| `ukrbar.serdiuk.2.4` | Barracks 17c serdiuk protection +1 (lvl 5) | 5 | 1 | 15.62 | 3500 | 0 | 0 | 450 | 0 | 0 |
| `ukrbar.serdiuk.2.5` | Barracks 17c serdiuk protection +2 (lvl 6) | 6 | 2 | 15.62 | 8100 | 0 | 0 | 210 | 0 | 0 |
| `ukrbar.serdiuk.2.6` | — | 7 | 2 | 15.62 | 11250 | 0 | 0 | 1125 | 0 | 0 |
| `ukrbla.1` | Manufacture agricultural equipment (field capacity +100%) | 1 | 100 | 15.62 | 0 | 400 | 0 | 90 | 0 | 0 |
| `ukrbla.2` | Forge metal armature and gratings (building defence +50) | 1 | 50 | 15.62 | 0 | 0 | 12320 | 350 | 900 | 0 |
| `ukrbla.3` | Forge harnesses for horses (mounted units recruitment speed -33%) | 1 | -3333333 | 15.62 | 0 | 0 | 0 | 3650 | 5300 | 8200 |
| `ukrbla.4` | Forge bayonets and broadswords for infantry %color(FFAA00)%(18c musketeer/grenadier melee attack +5) | — | — | — | — | — | — | — | — | — |
| `ukrbla.5` | Forge new types of broadswords and sabres (cavalry and sword clansman attack +5) | 1 | 5 | 15.62 | 0 | 0 | 0 | 4000 | 7900 | 0 |
| `ukrbla.6` | Forge new cuirasses %color(FFAA00)%(armoured soldiers defence +2) | — | — | — | — | — | — | — | — | — |
| `ukrcen.1` | — | 1 | 0 | 9.38 | 30000 | 0 | 0 | 5000 | 2000 | 2000 |
| `ukrpor.1` | — | 1 | 50 | 46.88 | 0 | 20000 | 0 | 1500 | 0 | 0 |
| `ukrsta.cossackregister.2.1` | Stable cossackregister protection +2 (lvl 2) | 2 | 2 | 15.62 | 200 | 0 | 0 | 135 | 3000 | 0 |
| `ukrsta.cossackregister.2.2` | Stable cossackregister protection +2 (lvl 3) | 3 | 2 | 15.62 | 2000 | 0 | 0 | 100 | 5000 | 0 |
| `ukrsta.cossackregister.2.3` | Stable cossackregister protection +2 (lvl 4) | 4 | 2 | 15.62 | 65000 | 0 | 0 | 200 | 10000 | 0 |
| `ukrsta.cossackregister.2.4` | Stable cossackregister protection +2 (lvl 5) | 5 | 2 | 15.62 | 65000 | 0 | 0 | 300 | 4000 | 0 |
| `ukrsta.cossackregister.2.5` | Stable cossackregister protection +2 (lvl 6) | 6 | 2 | 15.62 | 65000 | 0 | 0 | 350 | 20000 | 0 |
| `ukrsta.cossackregister.2.6` | Stable cossackregister protection +2 (lvl 7) | 7 | 2 | 15.62 | 65000 | 0 | 0 | 1000 | 30000 | 0 |
| `ukrsta.cossacksich.2.1` | Stable cossacksich protection +2 (lvl 2) | 2 | 2 | 15.62 | 200 | 0 | 0 | 135 | 3000 | 0 |
| `ukrsta.cossacksich.2.2` | Stable cossacksich protection +2 (lvl 3) | 3 | 2 | 15.62 | 2000 | 0 | 0 | 100 | 5000 | 0 |
| `ukrsta.cossacksich.2.3` | Stable cossacksich protection +2 (lvl 4) | 4 | 2 | 15.62 | 44930 | 0 | 0 | 200 | 10000 | 0 |
| `ukrsta.cossacksich.2.4` | Stable cossacksich protection +2 (lvl 5) | 5 | 2 | 15.62 | 44930 | 0 | 0 | 300 | 4000 | 0 |
| `ukrsta.cossacksich.2.5` | Stable cossacksich protection +2 (lvl 6) | 6 | 2 | 15.62 | 44930 | 0 | 0 | 350 | 20000 | 0 |
| `ukrsta.cossacksich.2.6` | Stable cossacksich protection +2 (lvl 7) | 7 | 2 | 15.62 | 44930 | 0 | 0 | 1000 | 30000 | 0 |
| `ukrsta.hetman.1.1` | Stable hetman damage +30 (lvl 2) | 2 | 30 | 15.62 | 7000 | 0 | 0 | 18000 | 0 | 0 |
| `ukrsta.hetman.2.1` | Stable hetman protection +10 (lvl 2) | 2 | 10 | 15.62 | 44950 | 0 | 0 | 1000 | 20000 | 0 |
| `ukrwwa.1` | — | 2 | 5 | 0.03 | 0 | 400 | 0 | 0 | 0 | 0 |

### pol — Poland

| sid | имя (EN) | level | value | время (s) | F | W | S | G | I | C |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `eurcoa.1` | — | 2 | 5 | 9.38 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `eurcoa.2` | — | 3 | 8 | 9.38 | 5250 | 0 | 0 | 4950 | 0 | 0 |
| `eurcoa.3` | — | 4 | 10 | 9.38 | 12500 | 0 | 0 | 9250 | 0 | 0 |
| `eurcoa.4` | — | 5 | 12 | 9.38 | 15800 | 0 | 0 | 18500 | 0 | 0 |
| `eurcoa.5` | — | 6 | 15 | 9.38 | 19800 | 0 | 0 | 21050 | 0 | 0 |
| `eurcoa.6` | — | 7 | 40 | 9.38 | 50200 | 0 | 0 | 25950 | 0 | 0 |
| `eurgol.1` | — | 2 | 5 | 9.38 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `eurgol.2` | — | 3 | 8 | 9.38 | 5250 | 0 | 0 | 4950 | 0 | 0 |
| `eurgol.3` | — | 4 | 10 | 9.38 | 12500 | 0 | 0 | 9250 | 0 | 0 |
| `eurgol.4` | — | 5 | 12 | 9.38 | 15800 | 0 | 0 | 18500 | 0 | 0 |
| `eurgol.5` | — | 6 | 15 | 9.38 | 19800 | 0 | 0 | 21050 | 0 | 0 |
| `eurgol.6` | — | 7 | 40 | 9.38 | 50200 | 0 | 0 | 25950 | 0 | 0 |
| `euriro.1` | — | 2 | 5 | 9.38 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `euriro.2` | — | 3 | 8 | 9.38 | 5250 | 0 | 0 | 4950 | 0 | 0 |
| `euriro.3` | — | 4 | 10 | 9.38 | 12500 | 0 | 0 | 9250 | 0 | 0 |
| `euriro.4` | — | 5 | 12 | 9.38 | 15800 | 0 | 0 | 18500 | 0 | 0 |
| `euriro.5` | — | 6 | 15 | 9.38 | 19800 | 0 | 0 | 21050 | 0 | 0 |
| `euriro.6` | — | 7 | 40 | 9.38 | 50200 | 0 | 0 | 25950 | 0 | 0 |
| `eurpor.1` | — | 1 | 50 | 46.88 | 0 | 20000 | 0 | 1500 | 0 | 0 |
| `eurswa.1` | — | 2 | 5 | 0.03 | 0 | 0 | 500 | 0 | 0 | 0 |
| `eurtow.1` | — | 2 | -20 | 31.25 | 0 | 0 | 0 | 250 | 0 | 0 |
| `eurtow.2` | — | 3 | -20 | 31.25 | 0 | 0 | 0 | 0 | 350 | 0 |
| `eurtow.3` | — | 4 | -10 | 31.25 | 0 | 0 | 0 | 0 | 0 | 400 |
| `eurtow.4` | — | 5 | -10 | 31.25 | 0 | 0 | 0 | 0 | 450 | 0 |
| `eurtow.5` | — | 6 | -10 | 31.25 | 0 | 0 | 0 | 0 | 0 | 500 |
| `ferry.1` | Improve transport vessel design (+%value% capacity) | 2 | 200 | 15.62 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `polaca.1` | Cultivate new cultures of wheat (harvesting +40%) | 1 | 40 | 15.62 | 0 | 200 | 0 | 325 | 0 | 0 |
| `polaca.10` | Raise builders' salary (building construction time -75%) | 1 | -7500000 | 15.62 | 0 | 0 | 0 | 6950 | 0 | 0 |
| `polaca.11` | Research new fortification grades (durability of walls and towers +80) | 1 | 80 | 15.62 | 0 | 0 | 16200 | 1500 | 0 | 0 |
| `polaca.12` | Improve firearms: rifled barrel (fire power +10%) | 1 | 10 | 15.62 | 0 | 0 | 0 | 0 | 5000 | 0 |
| `polaca.13` | Research granular gunpowder (fire power +10%) | 1 | 10 | 15.62 | 0 | 0 | 0 | 4000 | 0 | 0 |
| `polaca.14` | Research new sulphur purification methods (fire power +15%) | 1 | 15 | 15.62 | 0 | 0 | 0 | 7000 | 0 | 0 |
| `polaca.15` | Research new nitre purification methods (fire power +25%) | 1 | 25 | 15.62 | 0 | 0 | 0 | 0 | 0 | 11000 |
| `polaca.16` | Research improved additions to gunpowder formula (artillery range +5%) | 1 | 5 | 15.62 | 0 | 0 | 0 | 2000 | 12150 | 0 |
| `polaca.17` | Design new barrel types: unicorn, carronade (artillery range +10%) | 1 | 10 | 15.62 | 0 | 0 | 3000 | 4550 | 19200 | 0 |
| `polaca.18` | Design more durable gun carriage: Gribovalle system (artillery durability +50%) | 1 | 50 | 15.62 | 0 | 0 | 0 | 500 | 3830 | 1500 |
| `polaca.19` | Design multi-barrelled cannon | 1 | 0 | 15.62 | 0 | 0 | 0 | 1500 | 0 | 2500 |
| `polaca.2` | Cultivate new cultures of rye (harvesting +50%) | 1 | 50 | 15.62 | 0 | 2400 | 0 | 625 | 0 | 0 |
| `polaca.20` | Research new sighting devices for artillery (artillery accuracy +35%) | 1 | -35 | 15.62 | 0 | 3540 | 0 | 2000 | 0 | 7250 |
| `polaca.21` | Finance artillery repair shops (repair all artillery) | 1 | 25 | 15.62 | 0 | 350 | 0 | 100 | 0 | 250 |
| `polaca.22` | Develop geology (previously hidden deposits appear on the map) | 1 | 0 | 15.62 | 0 | 0 | 0 | 250 | 0 | 0 |
| `polaca.23` | Develop mining (stone excavation efficiency +100%) | 1 | 100 | 15.62 | 0 | 0 | 0 | 1550 | 3000 | 0 |
| `polaca.24` | Raise miners' salary (stone excavation efficiency +200%) | 1 | 200 | 15.62 | 4200 | 0 | 0 | 1550 | 0 | 12520 |
| `polaca.25` | Design Montgolfier (reveals the whole map) | 1 | 0 | 15.62 | 0 | 0 | 0 | 5750 | 0 | 0 |
| `polaca.26` | Develop medical science (heals all live units) | 1 | 50 | 31.25 | 0 | 0 | 0 | 200 | 0 | 200 |
| `polaca.27` | Develop mathematics (artillery accuracy +35%) | 1 | -35 | 15.62 | 0 | 9540 | 0 | 12000 | 0 | 65200 |
| `polaca.28` | Design new rigging types (ship speed +40%) | 1 | 40 | 15.62 | 0 | 65400 | 0 | 24050 | 0 | 0 |
| `polaca.29` | Design new rib system and new hulls (battleship construction) | 1 | 0 | 15.62 | 0 | 32300 | 0 | 6800 | 9000 | 12800 |
| `polaca.3` | Raise agriculturists' salary (harvesting +50%) | 1 | 50 | 15.62 | 0 | 3600 | 0 | 850 | 0 | 0 |
| `polaca.30` | Train carpenters (shipbuilding speed x10) | 1 | -5000000 | 15.62 | 0 | 2300 | 42700 | 1150 | 0 | 0 |
| `polaca.31` | Design wheellock (rate of fire +30%) | 1 | -30 | 15.62 | 0 | 0 | 6000 | 5500 | 4200 | 0 |
| `polaca.32` | Design flintlock (musket cost -50%) | 1 | 0 | 15.62 | 0 | 0 | 0 | 6050 | 0 | 7750 |
| `polaca.33` | Design paper cartridge and iron ramrod (rate of fire +30%) | 1 | -30 | 15.62 | 0 | 5000 | 0 | 5500 | 0 | 15200 |
| `polaca.34` | Research improved steel grades for cuirasses (armoured soldier defence +2) | 1 | 2 | 15.62 | 0 | 0 | 0 | 9750 | 0 | 0 |
| `polaca.35` | Design bayonet: barrel-inserted, bayonet with a tube (cold steel weapons +5) | 1 | 5 | 15.62 | 0 | 0 | 0 | 11500 | 0 | 0 |
| `polaca.36` | Research new steel grades (18c musketeer/grenadier melee attack efficiency +25%) | 1 | 25 | 15.62 | 0 | 0 | 0 | 19500 | 0 | 0 |
| `polaca.4` | Carry out field melioration (field capacity +200%) | 1 | 200 | 15.62 | 0 | 1000 | 0 | 475 | 0 | 0 |
| `polaca.5` | Design new tackle and fishing nets (boat efficiency +100%) | 1 | 100 | 15.62 | 0 | 12400 | 0 | 2520 | 0 | 0 |
| `polaca.6` | Develop new woodworking methods (frigate building) | 1 | 0 | 15.62 | 0 | 12400 | 0 | 7040 | 0 | 0 |
| `polaca.7` | Build new shipyards for fishing boats (fishing boat cost -85%) | 1 | 0 | 15.62 | 0 | 7300 | 0 | 1220 | 0 | 0 |
| `polaca.8` | Design new woodworking tools (woodcutting efficiency +100%) | 1 | 100 | 15.62 | 5500 | 0 | 0 | 550 | 0 | 0 |
| `polaca.9` | Use new construction materials (durability of buildings +85) | 1 | 85 | 15.62 | 0 | 9400 | 7850 | 1150 | 0 | 0 |
| `polart.cannon.1.1` | — | 2 | — | 10.0 | 0 | 1000 | 500 | 300 | 0 | 0 |
| `polart.cannon.1.2` | — | 3 | — | 10.0 | 0 | 3000 | 1000 | 500 | 0 | 0 |
| `polart.cannon.1.3` | — | 4 | — | 10.0 | 0 | 6000 | 2000 | 1000 | 0 | 0 |
| `polart.cannon.1.4` | — | 5 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `polart.cannon.1.5` | — | 6 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `polart.cannon.1.6` | — | 7 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `polart.cannon.2.1` | — | 2 | -2500000 | 10.0 | 0 | 0 | 0 | 500 | 1000 | 0 |
| `polart.cannon.2.2` | — | 3 | -2500000 | 10.0 | 0 | 0 | 0 | 1000 | 2000 | 0 |
| `polart.cannon.2.3` | — | 4 | -2500000 | 10.0 | 0 | 0 | 0 | 2000 | 3000 | 0 |
| `polart.cannon.2.4` | — | 5 | -2000000 | 15.62 | 2560 | 0 | 0 | 0 | 0 | 0 |
| `polart.cannon.2.5` | — | 6 | -2000000 | 15.62 | 3560 | 0 | 0 | 0 | 0 | 0 |
| `polart.cannon.2.6` | — | 7 | -2000000 | 15.62 | 5560 | 0 | 0 | 0 | 0 | 0 |
| `polart.howitzer.1.1` | — | 2 | — | 10.0 | 0 | 1000 | 500 | 300 | 0 | 0 |
| `polart.howitzer.1.2` | — | 3 | — | 10.0 | 0 | 3000 | 1000 | 500 | 0 | 0 |
| `polart.howitzer.1.3` | — | 4 | — | 10.0 | 0 | 6000 | 2000 | 1000 | 0 | 0 |
| `polart.howitzer.1.4` | — | 5 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `polart.howitzer.1.5` | — | 6 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `polart.howitzer.1.6` | — | 7 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `polart.howitzer.2.1` | — | 2 | -2500000 | 10.0 | 0 | 0 | 0 | 500 | 1000 | 0 |
| `polart.howitzer.2.2` | — | 3 | -2500000 | 10.0 | 0 | 0 | 0 | 1000 | 2000 | 0 |
| `polart.howitzer.2.3` | — | 4 | -2500000 | 10.0 | 0 | 0 | 0 | 2000 | 3000 | 0 |
| `polart.howitzer.2.4` | — | 5 | -2000000 | 31.25 | 2560 | 0 | 0 | 0 | 0 | 0 |
| `polart.howitzer.2.5` | — | 6 | -2000000 | 31.25 | 3560 | 0 | 0 | 0 | 0 | 0 |
| `polart.howitzer.2.6` | — | 7 | -2000000 | 31.25 | 5560 | 0 | 0 | 0 | 0 | 0 |
| `polba2.drummer18.2.1` | Barracks 18c drummer18 protection +15 (lvl 2) | 2 | 15 | 15.62 | 205 | 0 | 0 | 150 | 0 | 0 |
| `polba2.grenadier.1.1` | Barracks 18c grenadier damage +2 (lvl 2) | 2 | 2 | 15.62 | 3000 | 0 | 0 | 800 | 0 | 0 |
| `polba2.grenadier.1.2` | Barracks 18c grenadier damage +3 (lvl 3) | 3 | 3 | 15.62 | 11000 | 0 | 0 | 1800 | 0 | 0 |
| `polba2.grenadier.1.3` | Barracks 18c grenadier damage +4 (lvl 4) | 4 | 4 | 15.62 | 31000 | 0 | 0 | 2800 | 0 | 0 |
| `polba2.grenadier.1.4` | Barracks 18c grenadier damage +5 (lvl 5) | 5 | 5 | 15.62 | 43000 | 0 | 0 | 3800 | 0 | 0 |
| `polba2.grenadier.1.5` | Barracks 18c grenadier damage +6 (lvl 6) | 6 | 6 | 15.62 | 62000 | 0 | 0 | 4800 | 0 | 0 |
| `polba2.grenadier.1.6` | Barracks 18c grenadier damage +1500 (lvl 7) | 7 | 1500 | 15.62 | 52000 | 0 | 0 | 15800 | 0 | 0 |
| `polba2.grenadier.2.1` | Barracks 18c grenadier protection +1 (lvl 2) | 2 | 1 | 15.62 | 4506 | 0 | 0 | 750 | 0 | 0 |
| `polba2.grenadier.2.2` | Barracks 18c grenadier protection +2 (lvl 3) | 3 | 2 | 15.62 | 10130 | 0 | 0 | 950 | 0 | 0 |
| `polba2.grenadier.2.3` | Barracks 18c grenadier protection +3 (lvl 4) | 4 | 3 | 15.62 | 25706 | 0 | 0 | 500 | 0 | 0 |
| `polba2.grenadier.2.4` | Barracks 18c grenadier protection +1 (lvl 5) | 5 | 1 | 15.62 | 46556 | 0 | 0 | 1350 | 0 | 0 |
| `polba2.grenadier.2.5` | Barracks 18c grenadier protection +2 (lvl 6) | 6 | 2 | 15.62 | 50060 | 0 | 0 | 6050 | 0 | 0 |
| `polba2.grenadier.2.6` | Barracks 18c grenadier protection +3 (lvl 7) | 7 | 3 | 15.62 | 44000 | 0 | 0 | 1650 | 0 | 0 |
| `polba2.musketeer18.1.1` | Barracks 18c musketeer18 damage +1 (lvl 2) | 2 | 1 | 15.62 | 1000 | 0 | 0 | 100 | 0 | 0 |
| `polba2.musketeer18.1.2` | Barracks 18c musketeer18 damage +1 (lvl 3) | 3 | 1 | 15.62 | 2500 | 0 | 0 | 200 | 0 | 0 |
| `polba2.musketeer18.1.3` | Barracks 18c musketeer18 damage +2 (lvl 4) | 4 | 2 | 15.62 | 1000 | 0 | 0 | 300 | 0 | 0 |
| `polba2.musketeer18.1.4` | Barracks 18c musketeer18 damage +2 (lvl 5) | 5 | 2 | 15.62 | 3500 | 0 | 0 | 400 | 0 | 0 |
| `polba2.musketeer18.1.5` | Barracks 18c musketeer18 damage +3 (lvl 6) | 6 | 3 | 15.62 | 2000 | 0 | 0 | 3800 | 0 | 0 |
| `polba2.musketeer18.1.6` | Barracks 18c musketeer18 damage +3 (lvl 7) | 7 | 3 | 15.62 | 3500 | 0 | 0 | 600 | 0 | 0 |
| `polba2.musketeer18.2.1` | Barracks 18c musketeer18 protection +1 (lvl 2) | 2 | 1 | 15.62 | 5706 | 0 | 0 | 350 | 0 | 0 |
| `polba2.musketeer18.2.2` | Barracks 18c musketeer18 protection +2 (lvl 3) | 3 | 2 | 15.62 | 9030 | 0 | 0 | 4350 | 0 | 0 |
| `polba2.musketeer18.2.3` | Barracks 18c musketeer18 protection +2 (lvl 4) | 4 | 2 | 15.62 | 32706 | 0 | 0 | 1000 | 0 | 0 |
| `polba2.musketeer18.2.4` | Barracks 18c musketeer18 protection +1 (lvl 5) | 5 | 1 | 15.62 | 39556 | 0 | 0 | 2350 | 0 | 0 |
| `polba2.musketeer18.2.5` | Barracks 18c musketeer18 protection +2 (lvl 6) | 6 | 2 | 15.62 | 27060 | 0 | 0 | 3350 | 0 | 0 |
| `polba2.musketeer18.2.6` | Barracks 18c musketeer18 protection +2 (lvl 7) | 7 | 2 | 15.62 | 40600 | 0 | 0 | 1550 | 0 | 0 |
| `polba2.officer18.1.1` | Barracks 18c officer18 damage +30 (lvl 2) | 2 | 30 | 15.62 | 2000 | 0 | 0 | 200 | 0 | 0 |
| `polba2.officer18.2.1` | Barracks 18c officer18 protection +12 (lvl 2) | 2 | 12 | 15.62 | 605 | 0 | 0 | 950 | 0 | 0 |
| `polba2.pikeman18.1.1` | Barracks 18c pikeman18 damage +2 (lvl 2) | 2 | 2 | 15.62 | 2000 | 0 | 0 | 800 | 0 | 0 |
| `polba2.pikeman18.1.2` | Barracks 18c pikeman18 damage +2 (lvl 3) | 3 | 2 | 15.62 | 8000 | 0 | 0 | 1200 | 0 | 0 |
| `polba2.pikeman18.1.3` | Barracks 18c pikeman18 damage +2 (lvl 4) | 4 | 2 | 15.62 | 20000 | 0 | 0 | 2500 | 0 | 0 |
| `polba2.pikeman18.1.4` | Barracks 18c pikeman18 damage +2 (lvl 5) | 5 | 2 | 15.62 | 32000 | 0 | 0 | 2800 | 0 | 0 |
| `polba2.pikeman18.1.5` | Barracks 18c pikeman18 damage +2 (lvl 6) | 6 | 2 | 15.62 | 32000 | 0 | 0 | 3800 | 0 | 0 |
| `polba2.pikeman18.1.6` | Barracks 18c pikeman18 damage +2 (lvl 7) | 7 | 2 | 15.62 | 40500 | 0 | 0 | 4800 | 0 | 0 |
| `polba2.pikeman18.2.1` | Barracks 18c pikeman18 protection +2 (lvl 2) | 2 | 2 | 15.62 | 1500 | 0 | 0 | 500 | 0 | 0 |
| `polba2.pikeman18.2.2` | Barracks 18c pikeman18 protection +3 (lvl 3) | 3 | 3 | 15.62 | 7000 | 0 | 0 | 1500 | 0 | 0 |
| `polba2.pikeman18.2.3` | Barracks 18c pikeman18 protection +2 (lvl 4) | 4 | 2 | 15.62 | 37000 | 0 | 0 | 2000 | 0 | 0 |
| `polba2.pikeman18.2.4` | Barracks 18c pikeman18 protection +3 (lvl 5) | 5 | 3 | 15.62 | 37000 | 0 | 0 | 5500 | 0 | 0 |
| `polba2.pikeman18.2.5` | Barracks 18c pikeman18 protection +2 (lvl 6) | 6 | 2 | 15.62 | 37000 | 0 | 0 | 5500 | 0 | 0 |
| `polba2.pikeman18.2.6` | Barracks 18c pikeman18 protection +3 (lvl 7) | 7 | 3 | 15.62 | 64600 | 0 | 0 | 5500 | 0 | 0 |
| `polbar.1` | — | 1 | 140 | 15.62 | 750 | 0 | 0 | 250 | 0 | 0 |
| `polbar.2` | — | 2 | 180 | 15.62 | 25600 | 0 | 0 | 3350 | 2000 | 0 |
| `polbar.drummer.2.1` | Barracks 17c drummer protection +12 (lvl 2) | 2 | 12 | 15.62 | 405 | 0 | 0 | 250 | 0 | 0 |
| `polbar.musketeerpol.1.1` | Barracks 17c musketeerpol damage +1 (lvl 2) | 2 | 1 | 15.62 | 500 | 0 | 0 | 125 | 0 | 0 |
| `polbar.musketeerpol.1.2` | Barracks 17c musketeerpol damage +1 (lvl 3) | 3 | 1 | 15.62 | 1250 | 0 | 0 | 275 | 0 | 0 |
| `polbar.musketeerpol.1.3` | Barracks 17c musketeerpol damage +2 (lvl 4) | 4 | 2 | 15.62 | 2500 | 0 | 0 | 650 | 0 | 0 |
| `polbar.musketeerpol.2.1` | Barracks 17c musketeerpol protection +1 (lvl 2) | 2 | 1 | 15.62 | 125 | 0 | 0 | 150 | 100 | 0 |
| `polbar.musketeerpol.2.2` | Barracks 17c musketeerpol protection +1 (lvl 3) | 3 | 1 | 15.62 | 375 | 0 | 0 | 100 | 200 | 0 |
| `polbar.musketeerpol.2.3` | Barracks 17c musketeerpol protection +2 (lvl 4) | 4 | 2 | 15.62 | 1570 | 0 | 0 | 300 | 450 | 0 |
| `polbar.musketeerpol.2.4` | Barracks 17c musketeerpol protection +1 (lvl 5) | 5 | 1 | 15.62 | 2556 | 0 | 0 | 350 | 400 | 0 |
| `polbar.musketeerpol.2.5` | Barracks 17c musketeerpol protection +1 (lvl 6) | 6 | 1 | 15.62 | 3060 | 0 | 0 | 650 | 100 | 0 |
| `polbar.musketeerpol.2.6` | Barracks 17c musketeerpol protection +2 (lvl 7) | 7 | 2 | 15.62 | 2700 | 0 | 0 | 750 | 600 | 0 |
| `polbar.officer.1.1` | Barracks 17c officer damage +20 (lvl 2) | 2 | 20 | 15.62 | 50 | 0 | 0 | 150 | 0 | 0 |
| `polbar.officer.2.1` | Barracks 17c officer protection +6 (lvl 2) | 2 | 6 | 15.62 | 1550 | 0 | 0 | 650 | 0 | 0 |
| `polbar.pikemanpol.1.1` | Barracks 17c pikemanpol damage +1 (lvl 2) | 2 | 1 | 15.62 | 500 | 0 | 0 | 50 | 0 | 0 |
| `polbar.pikemanpol.1.2` | Barracks 17c pikemanpol damage +1 (lvl 3) | 3 | 1 | 15.62 | 1400 | 0 | 0 | 100 | 0 | 0 |
| `polbar.pikemanpol.1.3` | Barracks 17c pikemanpol damage +1 (lvl 4) | 4 | 1 | 15.62 | 3200 | 0 | 0 | 450 | 0 | 0 |
| `polbar.pikemanpol.1.4` | Barracks 17c pikemanpol damage +2 (lvl 5) | 5 | 2 | 15.62 | 8200 | 0 | 0 | 2220 | 0 | 0 |
| `polbar.pikemanpol.1.5` | Barracks 17c pikemanpol damage +2 (lvl 6) | 6 | 2 | 15.62 | 15030 | 0 | 0 | 1800 | 0 | 0 |
| `polbar.pikemanpol.1.6` | — | 7 | 3 | 15.62 | 22500 | 0 | 0 | 2800 | 0 | 0 |
| `polbar.pikemanpol.2.1` | Barracks 17c pikemanpol protection +1 (lvl 2) | 2 | 1 | 15.62 | 250 | 0 | 0 | 75 | 0 | 0 |
| `polbar.pikemanpol.2.2` | Barracks 17c pikemanpol protection +1 (lvl 3) | 3 | 1 | 15.62 | 800 | 0 | 0 | 150 | 0 | 0 |
| `polbar.pikemanpol.2.3` | Barracks 17c pikemanpol protection +2 (lvl 4) | 4 | 2 | 15.62 | 3500 | 0 | 0 | 225 | 0 | 0 |
| `polbar.pikemanpol.2.4` | Barracks 17c pikemanpol protection +2 (lvl 5) | 5 | 2 | 15.62 | 9005 | 0 | 0 | 407 | 0 | 0 |
| `polbar.pikemanpol.2.5` | Barracks 17c pikemanpol protection +4 (lvl 6) | 6 | 4 | 15.62 | 19010 | 0 | 0 | 2975 | 0 | 0 |
| `polbar.pikemanpol.2.6` | — | 7 | 3 | 15.62 | 15000 | 0 | 0 | 1000 | 0 | 0 |
| `polbla.1` | Manufacture agricultural equipment (field capacity +100%) | 1 | 100 | 15.62 | 0 | 400 | 0 | 90 | 0 | 0 |
| `polbla.2` | Forge metal armature and gratings (building defence +50) | 1 | 50 | 15.62 | 0 | 0 | 12320 | 350 | 900 | 0 |
| `polbla.3` | Forge harnesses for horses (mounted units recruitment speed -33%) | 1 | -3333333 | 15.62 | 0 | 0 | 0 | 3650 | 5300 | 8200 |
| `polbla.4` | Forge bayonets and broadswords for infantry (18c musketeer/grenadier melee attack +5) | 1 | 5 | 15.62 | 0 | 1300 | 0 | 1500 | 900 | 5000 |
| `polbla.5` | Forge new types of broadswords and sabres (cavalry and sword clansman attack +5) | 1 | 5 | 15.62 | 0 | 0 | 0 | 4000 | 7900 | 0 |
| `polbla.6` | Forge new cuirasses (armoured soldiers defence +2) | 1 | 2 | 15.62 | 0 | 0 | 0 | 4950 | 10500 | 0 |
| `polcen.1` | — | 1 | 0 | 9.38 | 30000 | 0 | 0 | 4800 | 2200 | 2200 |
| `polsta.cuirassier.1.1` | Stable cuirassier damage +1 (lvl 2) | 2 | 1 | 15.62 | 12000 | 0 | 0 | 600 | 0 | 0 |
| `polsta.cuirassier.1.2` | Stable cuirassier damage +1 (lvl 3) | 3 | 1 | 15.62 | 32000 | 0 | 0 | 1300 | 0 | 0 |
| `polsta.cuirassier.1.3` | Stable cuirassier damage +1 (lvl 4) | 4 | 1 | 15.62 | 62000 | 0 | 0 | 2200 | 0 | 0 |
| `polsta.cuirassier.1.4` | Stable cuirassier damage +2 (lvl 5) | 5 | 2 | 15.62 | 61000 | 0 | 0 | 3150 | 0 | 0 |
| `polsta.cuirassier.1.5` | Stable cuirassier damage +2 (lvl 6) | 6 | 2 | 15.62 | 57055 | 0 | 0 | 4100 | 0 | 0 |
| `polsta.cuirassier.1.6` | Stable cuirassier damage +3 (lvl 7) | 7 | 3 | 15.62 | 49050 | 0 | 0 | 8020 | 0 | 0 |
| `polsta.cuirassier.2.1` | Stable cuirassier protection +2 (lvl 2) | 2 | 2 | 15.62 | 1760 | 0 | 0 | 350 | 1000 | 0 |
| `polsta.cuirassier.2.2` | Stable cuirassier protection +3 (lvl 3) | 3 | 3 | 15.62 | 3000 | 0 | 0 | 750 | 2000 | 0 |
| `polsta.cuirassier.2.3` | Stable cuirassier protection +3 (lvl 4) | 4 | 3 | 15.62 | 7600 | 0 | 0 | 300 | 3030 | 0 |
| `polsta.cuirassier.2.4` | Stable cuirassier protection +2 (lvl 5) | 5 | 2 | 15.62 | 8700 | 0 | 0 | 6200 | 100 | 0 |
| `polsta.cuirassier.2.5` | Stable cuirassier protection +1 (lvl 6) | 6 | 1 | 15.62 | 8700 | 0 | 0 | 2350 | 5000 | 0 |
| `polsta.cuirassier.2.6` | Stable cuirassier protection +1 (lvl 7) | 7 | 1 | 15.62 | 9700 | 0 | 0 | 4444 | 7060 | 0 |
| `polsta.dragoon18.1.1` | Stable dragoon18 damage +2 (lvl 2) | 2 | 2 | 15.62 | 2000 | 0 | 0 | 100 | 0 | 0 |
| `polsta.dragoon18.1.2` | Stable dragoon18 damage +2 (lvl 3) | 3 | 2 | 15.62 | 9000 | 0 | 0 | 350 | 0 | 0 |
| `polsta.dragoon18.1.3` | Stable dragoon18 damage +4 (lvl 4) | 4 | 4 | 15.62 | 12000 | 0 | 0 | 400 | 0 | 0 |
| `polsta.dragoon18.1.4` | Stable dragoon18 damage +2 (lvl 5) | 5 | 2 | 15.62 | 23000 | 0 | 0 | 580 | 0 | 0 |
| `polsta.dragoon18.1.5` | Stable dragoon18 damage +2 (lvl 6) | 6 | 2 | 15.62 | 32000 | 0 | 0 | 680 | 0 | 0 |
| `polsta.dragoon18.1.6` | Stable dragoon18 damage +4 (lvl 7) | 7 | 4 | 15.62 | 42000 | 0 | 0 | 780 | 0 | 0 |
| `polsta.dragoon18.2.1` | Stable dragoon18 protection +1 (lvl 2) | 2 | 1 | 15.62 | 760 | 0 | 0 | 935 | 0 | 0 |
| `polsta.dragoon18.2.2` | Stable dragoon18 protection +1 (lvl 3) | 3 | 1 | 15.62 | 1260 | 0 | 0 | 1150 | 0 | 0 |
| `polsta.dragoon18.2.3` | Stable dragoon18 protection +2 (lvl 4) | 4 | 2 | 15.62 | 15600 | 0 | 0 | 2350 | 0 | 0 |
| `polsta.dragoon18.2.4` | Stable dragoon18 protection +1 (lvl 5) | 5 | 1 | 15.62 | 17600 | 0 | 0 | 3350 | 0 | 0 |
| `polsta.dragoon18.2.5` | Stable dragoon18 protection +2 (lvl 6) | 6 | 2 | 15.62 | 19600 | 0 | 0 | 5350 | 0 | 0 |
| `polsta.dragoon18.2.6` | Stable dragoon18 protection +3 (lvl 7) | 7 | 3 | 15.62 | 21760 | 0 | 0 | 9350 | 0 | 0 |
| `polsta.dragoonpol.1.1` | Stable dragoonpol damage +1 (lvl 2) | 2 | 1 | 15.62 | 700 | 0 | 0 | 250 | 0 | 0 |
| `polsta.dragoonpol.1.2` | Stable dragoonpol damage +1 (lvl 3) | 3 | 1 | 15.62 | 500 | 0 | 0 | 200 | 0 | 0 |
| `polsta.dragoonpol.1.3` | Stable dragoonpol damage +2 (lvl 4) | 4 | 2 | 15.62 | 700 | 0 | 0 | 240 | 0 | 0 |
| `polsta.dragoonpol.1.4` | Stable dragoonpol damage +1 (lvl 5) | 5 | 1 | 15.62 | 0 | 0 | 0 | 0 | 0 | 0 |
| `polsta.dragoonpol.1.5` | Stable dragoonpol damage +1 (lvl 6) | 6 | 1 | 15.62 | 0 | 0 | 0 | 0 | 0 | 0 |
| `polsta.dragoonpol.1.6` | Stable dragoonpol damage +3 (lvl 7) | 7 | 3 | 15.62 | 0 | 0 | 0 | 0 | 0 | 0 |
| `polsta.dragoonpol.2.1` | Stable dragoonpol protection +1 (lvl 2) | 2 | 1 | 15.62 | 900 | 0 | 0 | 250 | 0 | 0 |
| `polsta.dragoonpol.2.2` | Stable dragoonpol protection +1 (lvl 3) | 3 | 1 | 15.62 | 6200 | 0 | 0 | 550 | 0 | 0 |
| `polsta.dragoonpol.2.3` | Stable dragoonpol protection +1 (lvl 4) | 4 | 1 | 15.62 | 5400 | 0 | 0 | 1150 | 0 | 0 |
| `polsta.dragoonpol.2.4` | Stable dragoonpol protection +1 (lvl 5) | 5 | 1 | 15.62 | 2000 | 0 | 0 | 800 | 0 | 0 |
| `polsta.dragoonpol.2.5` | Stable dragoonpol protection +2 (lvl 6) | 6 | 2 | 15.62 | 3000 | 0 | 0 | 2250 | 0 | 0 |
| `polsta.dragoonpol.2.6` | Stable dragoonpol protection +2 (lvl 7) | 7 | 2 | 15.62 | 5001 | 0 | 0 | 6100 | 0 | 0 |
| `polsta.hussar.1.1` | Stable hussar damage +1 (lvl 2) | 2 | 1 | 15.62 | 0 | 0 | 0 | 1800 | 1000 | 0 |
| `polsta.hussar.1.2` | Stable hussar damage +2 (lvl 3) | 3 | 2 | 15.62 | 0 | 0 | 0 | 3800 | 2000 | 0 |
| `polsta.hussar.1.3` | Stable hussar damage +3 (lvl 4) | 4 | 3 | 15.62 | 20200 | 0 | 0 | 0 | 2000 | 0 |
| `polsta.hussar.1.4` | Stable hussar damage +4 (lvl 5) | 5 | 4 | 15.62 | 32000 | 0 | 0 | 0 | 3000 | 0 |
| `polsta.hussar.1.5` | Stable hussar damage +1 (lvl 6) | 6 | 1 | 15.62 | 49200 | 0 | 0 | 0 | 3500 | 0 |
| `polsta.hussar.1.6` | Stable hussar damage +1 (lvl 7) | 7 | 1 | 15.62 | 20000 | 0 | 0 | 0 | 6000 | 0 |
| `polsta.hussar.2.1` | Stable hussar protection +1 (lvl 2) | 2 | 1 | 15.62 | 1760 | 0 | 0 | 1350 | 0 | 0 |
| `polsta.hussar.2.2` | Stable hussar protection +1 (lvl 3) | 3 | 1 | 15.62 | 1900 | 0 | 0 | 2350 | 0 | 0 |
| `polsta.hussar.2.3` | Stable hussar protection +1 (lvl 4) | 4 | 1 | 15.62 | 1600 | 0 | 0 | 5350 | 0 | 0 |
| `polsta.hussar.2.4` | Stable hussar protection +2 (lvl 5) | 5 | 2 | 15.62 | 8000 | 0 | 0 | 8350 | 0 | 0 |
| `polsta.hussar.2.5` | Stable hussar protection +2 (lvl 6) | 6 | 2 | 15.62 | 2000 | 0 | 0 | 15350 | 0 | 0 |
| `polsta.hussar.2.6` | Stable hussar protection +3 (lvl 7) | 7 | 3 | 15.62 | 56000 | 0 | 0 | 20150 | 0 | 0 |
| `polsta.reiterpol.1.1` | Stable reiterpol damage +1 (lvl 2) | 2 | 1 | 15.62 | 2000 | 0 | 0 | 500 | 0 | 0 |
| `polsta.reiterpol.1.2` | Stable reiterpol damage +1 (lvl 3) | 3 | 1 | 15.62 | 5000 | 0 | 0 | 800 | 0 | 0 |
| `polsta.reiterpol.1.3` | Stable reiterpol damage +1 (lvl 4) | 4 | 1 | 15.62 | 10000 | 0 | 0 | 800 | 0 | 0 |
| `polsta.reiterpol.1.4` | Stable reiterpol damage +2 (lvl 5) | 5 | 2 | 15.62 | 20000 | 0 | 0 | 950 | 0 | 0 |
| `polsta.reiterpol.1.5` | Stable reiterpol damage +2 (lvl 6) | 6 | 2 | 15.62 | 30000 | 0 | 0 | 300 | 0 | 0 |
| `polsta.reiterpol.1.6` | Stable reiterpol damage +3 (lvl 7) | 7 | 3 | 15.62 | 20000 | 0 | 0 | 1500 | 0 | 0 |
| `polsta.reiterpol.2.1` | Stable reiterpol protection +1 (lvl 2) | 2 | 1 | 15.62 | 2000 | 0 | 0 | 900 | 0 | 0 |
| `polsta.reiterpol.2.2` | Stable reiterpol protection +1 (lvl 3) | 3 | 1 | 15.62 | 1500 | 0 | 0 | 850 | 0 | 0 |
| `polsta.reiterpol.2.3` | Stable reiterpol protection +1 (lvl 4) | 4 | 1 | 15.62 | 5000 | 0 | 0 | 950 | 0 | 0 |
| `polsta.reiterpol.2.4` | Stable reiterpol protection +2 (lvl 5) | 5 | 2 | 15.62 | 10500 | 0 | 0 | 400 | 0 | 0 |
| `polsta.reiterpol.2.5` | Stable reiterpol protection +2 (lvl 6) | 6 | 2 | 15.62 | 12600 | 0 | 0 | 1500 | 0 | 0 |
| `polsta.reiterpol.2.6` | Stable reiterpol protection +3 (lvl 7) | 7 | 3 | 15.62 | 40000 | 0 | 0 | 9000 | 0 | 0 |
| `polsta.wingedhussar.1.1` | Stable wingedhussar damage +1 (lvl 2) | 2 | 1 | 15.62 | 400 | 0 | 0 | 200 | 0 | 0 |
| `polsta.wingedhussar.1.2` | Stable wingedhussar damage +2 (lvl 3) | 3 | 2 | 15.62 | 990 | 0 | 0 | 120 | 0 | 0 |
| `polsta.wingedhussar.1.3` | Stable wingedhussar damage +2 (lvl 4) | 4 | 2 | 15.62 | 2400 | 0 | 0 | 380 | 0 | 0 |
| `polsta.wingedhussar.1.4` | Stable wingedhussar damage +2 (lvl 5) | 5 | 2 | 15.62 | 4250 | 0 | 0 | 220 | 0 | 0 |
| `polsta.wingedhussar.1.5` | Stable wingedhussar damage +2 (lvl 6) | 6 | 2 | 15.62 | 7030 | 0 | 0 | 200 | 0 | 0 |
| `polsta.wingedhussar.1.6` | Stable wingedhussar damage +1 (lvl 7) | 7 | 1 | 15.62 | 3000 | 0 | 0 | 2200 | 0 | 0 |
| `polsta.wingedhussar.2.1` | Stable wingedhussar protection +2 (lvl 2) | 2 | 2 | 15.62 | 300 | 0 | 0 | 35 | 100 | 0 |
| `polsta.wingedhussar.2.2` | Stable wingedhussar protection +2 (lvl 3) | 3 | 2 | 15.62 | 500 | 0 | 0 | 200 | 600 | 0 |
| `polsta.wingedhussar.2.3` | Stable wingedhussar protection +2 (lvl 4) | 4 | 2 | 15.62 | 600 | 0 | 0 | 300 | 260 | 0 |
| `polsta.wingedhussar.2.4` | Stable wingedhussar protection +2 (lvl 5) | 5 | 2 | 15.62 | 1800 | 0 | 0 | 200 | 940 | 0 |
| `polsta.wingedhussar.2.5` | Stable wingedhussar protection +2 (lvl 6) | 6 | 2 | 15.62 | 2200 | 0 | 0 | 150 | 700 | 0 |
| `polsta.wingedhussar.2.6` | Stable wingedhussar protection +2 (lvl 7) | 7 | 2 | 15.62 | 17150 | 0 | 0 | 1200 | 4600 | 0 |
| `ukrwwa.1` | — | 2 | 5 | 0.03 | 0 | 400 | 0 | 0 | 0 | 0 |

### swe — Sweden

| sid | имя (EN) | level | value | время (s) | F | W | S | G | I | C |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `eurcoa.1` | — | 2 | 5 | 9.38 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `eurcoa.2` | — | 3 | 8 | 9.38 | 5250 | 0 | 0 | 4950 | 0 | 0 |
| `eurcoa.3` | — | 4 | 10 | 9.38 | 12500 | 0 | 0 | 9250 | 0 | 0 |
| `eurcoa.4` | — | 5 | 12 | 9.38 | 15800 | 0 | 0 | 18500 | 0 | 0 |
| `eurcoa.5` | — | 6 | 15 | 9.38 | 19800 | 0 | 0 | 21050 | 0 | 0 |
| `eurcoa.6` | — | 7 | 40 | 9.38 | 50200 | 0 | 0 | 25950 | 0 | 0 |
| `eurgol.1` | — | 2 | 5 | 9.38 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `eurgol.2` | — | 3 | 8 | 9.38 | 5250 | 0 | 0 | 4950 | 0 | 0 |
| `eurgol.3` | — | 4 | 10 | 9.38 | 12500 | 0 | 0 | 9250 | 0 | 0 |
| `eurgol.4` | — | 5 | 12 | 9.38 | 15800 | 0 | 0 | 18500 | 0 | 0 |
| `eurgol.5` | — | 6 | 15 | 9.38 | 19800 | 0 | 0 | 21050 | 0 | 0 |
| `eurgol.6` | — | 7 | 40 | 9.38 | 50200 | 0 | 0 | 25950 | 0 | 0 |
| `euriro.1` | — | 2 | 5 | 9.38 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `euriro.2` | — | 3 | 8 | 9.38 | 5250 | 0 | 0 | 4950 | 0 | 0 |
| `euriro.3` | — | 4 | 10 | 9.38 | 12500 | 0 | 0 | 9250 | 0 | 0 |
| `euriro.4` | — | 5 | 12 | 9.38 | 15800 | 0 | 0 | 18500 | 0 | 0 |
| `euriro.5` | — | 6 | 15 | 9.38 | 19800 | 0 | 0 | 21050 | 0 | 0 |
| `euriro.6` | — | 7 | 40 | 9.38 | 50200 | 0 | 0 | 25950 | 0 | 0 |
| `eurpor.1` | — | 1 | 50 | 46.88 | 0 | 20000 | 0 | 1500 | 0 | 0 |
| `eurswa.1` | — | 2 | 5 | 0.03 | 0 | 0 | 500 | 0 | 0 | 0 |
| `eurtow.1` | — | 2 | -20 | 31.25 | 0 | 0 | 0 | 250 | 0 | 0 |
| `eurtow.2` | — | 3 | -20 | 31.25 | 0 | 0 | 0 | 0 | 350 | 0 |
| `eurtow.3` | — | 4 | -10 | 31.25 | 0 | 0 | 0 | 0 | 0 | 400 |
| `eurtow.4` | — | 5 | -10 | 31.25 | 0 | 0 | 0 | 0 | 450 | 0 |
| `eurtow.5` | — | 6 | -10 | 31.25 | 0 | 0 | 0 | 0 | 0 | 500 |
| `ferry.1` | Improve transport vessel design (+%value% capacity) | 2 | 200 | 15.62 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `sweaca.1` | Cultivate new cultures of wheat (harvesting +40%) | 1 | 40 | 15.62 | 0 | 200 | 0 | 325 | 0 | 0 |
| `sweaca.10` | Raise builders' salary (building construction time -75%) | 1 | -7500000 | 15.62 | 0 | 0 | 0 | 6950 | 0 | 0 |
| `sweaca.11` | Research new fortification grades (durability of walls and towers +80) | 1 | 80 | 15.62 | 0 | 12200 | 16200 | 1100 | 0 | 0 |
| `sweaca.12` | Improve firearms: rifled barrel (fire power +10%) | 1 | 10 | 15.62 | 0 | 0 | 0 | 0 | 5000 | 0 |
| `sweaca.13` | Research granular gunpowder (fire power +10%) | 1 | 10 | 15.62 | 0 | 0 | 0 | 4000 | 0 | 0 |
| `sweaca.14` | Research new sulphur purification methods (fire power +15%) | 1 | 15 | 15.62 | 0 | 0 | 0 | 7000 | 0 | 0 |
| `sweaca.15` | Research new nitre purification methods (fire power +25%) | 1 | 25 | 15.62 | 0 | 0 | 0 | 0 | 0 | 11000 |
| `sweaca.16` | Research improved additions to gunpowder formula (artillery range +5%) | 1 | 5 | 15.62 | 0 | 0 | 0 | 2000 | 12150 | 0 |
| `sweaca.17` | Design new barrel types: unicorn, carronade (artillery range +10%) | 1 | 10 | 15.62 | 0 | 0 | 3000 | 4550 | 19200 | 0 |
| `sweaca.18` | Design more durable gun carriage: Gribovalle system (artillery durability +50%) | 1 | 50 | 15.62 | 0 | 0 | 0 | 500 | 3830 | 1500 |
| `sweaca.19` | Design multi-barrelled cannon | 1 | 0 | 15.62 | 0 | 0 | 0 | 1500 | 0 | 2500 |
| `sweaca.2` | Cultivate new cultures of rye (harvesting +50%) | 1 | 50 | 15.62 | 0 | 2400 | 0 | 625 | 0 | 0 |
| `sweaca.20` | Research new sighting devices for artillery (artillery accuracy +35%) | 1 | -35 | 15.62 | 0 | 3540 | 0 | 2000 | 0 | 7250 |
| `sweaca.21` | Finance artillery repair shops (repair all artillery) | 1 | 25 | 15.62 | 0 | 350 | 0 | 100 | 0 | 250 |
| `sweaca.22` | Develop geology (previously hidden deposits appear on the map) | 1 | 0 | 15.62 | 0 | 0 | 0 | 250 | 0 | 0 |
| `sweaca.23` | Develop mining (stone excavation efficiency +100%) | 1 | 100 | 15.62 | 0 | 0 | 0 | 1550 | 3000 | 0 |
| `sweaca.24` | Raise miners' salary (stone excavation efficiency +200%) | 1 | 200 | 15.62 | 4200 | 0 | 0 | 1550 | 0 | 12520 |
| `sweaca.25` | Design Montgolfier (reveals the whole map) | 1 | 0 | 15.62 | 0 | 0 | 0 | 5750 | 0 | 0 |
| `sweaca.26` | Develop medical science (heals all live units) | 1 | 50 | 31.25 | 0 | 0 | 0 | 200 | 0 | 200 |
| `sweaca.27` | Develop mathematics (artillery accuracy +35%) | 1 | -35 | 15.62 | 0 | 9540 | 0 | 12000 | 0 | 65200 |
| `sweaca.28` | Design new rigging types (ship speed +40%) | 1 | 40 | 15.62 | 0 | 65400 | 0 | 24050 | 0 | 0 |
| `sweaca.29` | Design new rib system and new hulls (battleship construction) | 1 | 0 | 15.62 | 0 | 32300 | 0 | 6800 | 9000 | 12800 |
| `sweaca.3` | Raise agriculturists' salary (harvesting +50%) | 1 | 50 | 15.62 | 0 | 3600 | 0 | 850 | 0 | 0 |
| `sweaca.30` | Train carpenters (shipbuilding speed x10) | 1 | -5000000 | 15.62 | 0 | 2300 | 42700 | 1150 | 0 | 0 |
| `sweaca.31` | Design wheellock (rate of fire +30%) | 1 | -30 | 15.62 | 0 | 0 | 6000 | 5500 | 4200 | 0 |
| `sweaca.32` | Design flintlock (musket cost -50%) | 1 | 0 | 15.62 | 0 | 0 | 0 | 6050 | 0 | 7750 |
| `sweaca.33` | Design paper cartridge and iron ramrod (rate of fire +30%) | 1 | -30 | 15.62 | 0 | 5000 | 0 | 5500 | 0 | 15200 |
| `sweaca.34` | Research improved steel grades for cuirasses (armoured soldier defence +2) | 1 | 2 | 15.62 | 0 | 0 | 0 | 9750 | 0 | 0 |
| `sweaca.35` | Design bayonet: barrel-inserted, bayonet with a tube (cold steel weapons +5) | 1 | 5 | 15.62 | 0 | 0 | 0 | 11500 | 0 | 0 |
| `sweaca.36` | Research new steel grades (18c musketeer/grenadier melee attack efficiency +25%) | 1 | 25 | 15.62 | 0 | 0 | 0 | 19500 | 0 | 0 |
| `sweaca.4` | Carry out field melioration (field capacity +200%) | 1 | 200 | 15.62 | 0 | 1000 | 0 | 475 | 0 | 0 |
| `sweaca.5` | Design new tackle and fishing nets (boat efficiency +100%) | 1 | 100 | 15.62 | 0 | 12400 | 0 | 2520 | 0 | 0 |
| `sweaca.6` | Develop new woodworking methods (frigate building) | 1 | 0 | 15.62 | 0 | 12400 | 0 | 7040 | 0 | 0 |
| `sweaca.7` | Build new shipyards for fishing boats (fishing boat cost -85%) | 1 | 0 | 15.62 | 0 | 7300 | 0 | 1220 | 0 | 0 |
| `sweaca.8` | Design new woodworking tools (woodcutting efficiency +100%) | 1 | 100 | 15.62 | 5500 | 0 | 0 | 550 | 0 | 0 |
| `sweaca.9` | Use new construction materials (durability of buildings +85) | 1 | 85 | 15.62 | 0 | 9400 | 7850 | 1150 | 0 | 0 |
| `sweart.cannon.1.1` | — | 2 | — | 10.0 | 0 | 1000 | 500 | 300 | 0 | 0 |
| `sweart.cannon.1.2` | — | 3 | — | 10.0 | 0 | 3000 | 1000 | 500 | 0 | 0 |
| `sweart.cannon.1.3` | — | 4 | — | 10.0 | 0 | 6000 | 2000 | 1000 | 0 | 0 |
| `sweart.cannon.1.4` | — | 5 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `sweart.cannon.1.5` | — | 6 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `sweart.cannon.1.6` | — | 7 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `sweart.cannon.2.1` | — | 2 | -2500000 | 10.0 | 0 | 0 | 0 | 500 | 1000 | 0 |
| `sweart.cannon.2.2` | — | 3 | -2500000 | 10.0 | 0 | 0 | 0 | 1000 | 2000 | 0 |
| `sweart.cannon.2.3` | — | 4 | -2500000 | 10.0 | 0 | 0 | 0 | 2000 | 3000 | 0 |
| `sweart.cannon.2.4` | — | 5 | -2000000 | 15.62 | 2560 | 0 | 0 | 0 | 0 | 0 |
| `sweart.cannon.2.5` | — | 6 | -2000000 | 15.62 | 3560 | 0 | 0 | 0 | 0 | 0 |
| `sweart.cannon.2.6` | — | 7 | -2000000 | 15.62 | 5560 | 0 | 0 | 0 | 0 | 0 |
| `sweart.howitzer.1.1` | — | 2 | — | 10.0 | 0 | 1000 | 500 | 300 | 0 | 0 |
| `sweart.howitzer.1.2` | — | 3 | — | 10.0 | 0 | 3000 | 1000 | 500 | 0 | 0 |
| `sweart.howitzer.1.3` | — | 4 | — | 10.0 | 0 | 6000 | 2000 | 1000 | 0 | 0 |
| `sweart.howitzer.1.4` | — | 5 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `sweart.howitzer.1.5` | — | 6 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `sweart.howitzer.1.6` | — | 7 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `sweart.howitzer.2.1` | — | 2 | -2500000 | 10.0 | 0 | 0 | 0 | 500 | 1000 | 0 |
| `sweart.howitzer.2.2` | — | 3 | -2500000 | 10.0 | 0 | 0 | 0 | 1000 | 2000 | 0 |
| `sweart.howitzer.2.3` | — | 4 | -2500000 | 10.0 | 0 | 0 | 0 | 2000 | 3000 | 0 |
| `sweart.howitzer.2.4` | — | 5 | -2000000 | 31.25 | 2560 | 0 | 0 | 0 | 0 | 0 |
| `sweart.howitzer.2.5` | — | 6 | -2000000 | 31.25 | 3560 | 0 | 0 | 0 | 0 | 0 |
| `sweart.howitzer.2.6` | — | 7 | -2000000 | 31.25 | 5560 | 0 | 0 | 0 | 0 | 0 |
| `sweba2.drummer18.2.1` | Barracks 18c drummer18 protection +15 (lvl 2) | 2 | 15 | 15.62 | 205 | 0 | 0 | 90 | 0 | 0 |
| `sweba2.grenadier.1.1` | Barracks 18c grenadier damage +2 (lvl 2) | 2 | 2 | 15.62 | 1000 | 0 | 0 | 800 | 0 | 0 |
| `sweba2.grenadier.1.2` | Barracks 18c grenadier damage +3 (lvl 3) | 3 | 3 | 15.62 | 13000 | 0 | 0 | 1800 | 0 | 0 |
| `sweba2.grenadier.1.3` | Barracks 18c grenadier damage +4 (lvl 4) | 4 | 4 | 15.62 | 25000 | 0 | 0 | 1800 | 0 | 0 |
| `sweba2.grenadier.1.4` | Barracks 18c grenadier damage +5 (lvl 5) | 5 | 5 | 15.62 | 49000 | 0 | 0 | 4800 | 0 | 0 |
| `sweba2.grenadier.1.5` | Barracks 18c grenadier damage +6 (lvl 6) | 6 | 6 | 15.62 | 54000 | 0 | 0 | 5800 | 0 | 0 |
| `sweba2.grenadier.1.6` | Barracks 18c grenadier damage +1500 (lvl 7) | 7 | 1500 | 15.62 | 60000 | 0 | 0 | 14590 | 0 | 0 |
| `sweba2.grenadier.2.1` | Barracks 18c grenadier protection +1 (lvl 2) | 2 | 1 | 15.62 | 7705 | 0 | 0 | 350 | 0 | 0 |
| `sweba2.grenadier.2.2` | Barracks 18c grenadier protection +2 (lvl 3) | 3 | 2 | 15.62 | 7030 | 0 | 0 | 1350 | 0 | 0 |
| `sweba2.grenadier.2.3` | Barracks 18c grenadier protection +3 (lvl 4) | 4 | 3 | 15.62 | 21706 | 0 | 0 | 1000 | 0 | 0 |
| `sweba2.grenadier.2.4` | Barracks 18c grenadier protection +1 (lvl 5) | 5 | 1 | 15.62 | 22556 | 0 | 0 | 5350 | 0 | 0 |
| `sweba2.grenadier.2.5` | Barracks 18c grenadier protection +2 (lvl 6) | 6 | 2 | 15.62 | 30060 | 0 | 0 | 1750 | 0 | 0 |
| `sweba2.grenadier.2.6` | Barracks 18c grenadier protection +3 (lvl 7) | 7 | 3 | 15.62 | 62000 | 0 | 0 | 950 | 0 | 0 |
| `sweba2.musketeer18.1.1` | Barracks 18c musketeer18 damage +1 (lvl 2) | 2 | 1 | 15.62 | 9000 | 0 | 0 | 200 | 0 | 0 |
| `sweba2.musketeer18.1.2` | Barracks 18c musketeer18 damage +1 (lvl 3) | 3 | 1 | 15.62 | 600 | 0 | 0 | 200 | 0 | 0 |
| `sweba2.musketeer18.1.3` | Barracks 18c musketeer18 damage +2 (lvl 4) | 4 | 2 | 15.62 | 4000 | 0 | 0 | 100 | 0 | 0 |
| `sweba2.musketeer18.1.4` | Barracks 18c musketeer18 damage +2 (lvl 5) | 5 | 2 | 15.62 | 500 | 0 | 0 | 2100 | 0 | 0 |
| `sweba2.musketeer18.1.5` | Barracks 18c musketeer18 damage +3 (lvl 6) | 6 | 3 | 15.62 | 3000 | 0 | 0 | 200 | 0 | 0 |
| `sweba2.musketeer18.1.6` | Barracks 18c musketeer18 damage +3 (lvl 7) | 7 | 3 | 15.62 | 3500 | 0 | 0 | 1400 | 0 | 0 |
| `sweba2.musketeer18.2.1` | Barracks 18c musketeer18 protection +1 (lvl 2) | 2 | 1 | 15.62 | 5706 | 0 | 0 | 750 | 0 | 0 |
| `sweba2.musketeer18.2.2` | Barracks 18c musketeer18 protection +2 (lvl 3) | 3 | 2 | 15.62 | 9030 | 0 | 0 | 1050 | 0 | 0 |
| `sweba2.musketeer18.2.3` | Barracks 18c musketeer18 protection +2 (lvl 4) | 4 | 2 | 15.62 | 32706 | 0 | 0 | 2900 | 0 | 0 |
| `sweba2.musketeer18.2.4` | Barracks 18c musketeer18 protection +1 (lvl 5) | 5 | 1 | 15.62 | 39556 | 0 | 0 | 5450 | 0 | 0 |
| `sweba2.musketeer18.2.5` | Barracks 18c musketeer18 protection +2 (lvl 6) | 6 | 2 | 15.62 | 30060 | 0 | 0 | 1350 | 0 | 0 |
| `sweba2.musketeer18.2.6` | Barracks 18c musketeer18 protection +2 (lvl 7) | 7 | 2 | 15.62 | 37600 | 0 | 0 | 1350 | 0 | 0 |
| `sweba2.officer18.1.1` | Barracks 18c officer18 damage +30 (lvl 2) | 2 | 30 | 15.62 | 200 | 0 | 0 | 910 | 0 | 0 |
| `sweba2.officer18.2.1` | Barracks 18c officer18 protection +12 (lvl 2) | 2 | 12 | 15.62 | 305 | 0 | 0 | 950 | 0 | 0 |
| `sweba2.pikeman18swe.1.1` | Barracks 18c pikeman18swe damage +2 (lvl 2) | 2 | 2 | 15.62 | 2000 | 0 | 0 | 800 | 0 | 0 |
| `sweba2.pikeman18swe.1.2` | Barracks 18c pikeman18swe damage +2 (lvl 3) | 3 | 2 | 15.62 | 8000 | 0 | 0 | 1200 | 0 | 0 |
| `sweba2.pikeman18swe.1.3` | Barracks 18c pikeman18swe damage +2 (lvl 4) | 4 | 2 | 15.62 | 20000 | 0 | 0 | 2500 | 0 | 0 |
| `sweba2.pikeman18swe.1.4` | Barracks 18c pikeman18swe damage +2 (lvl 5) | 5 | 2 | 15.62 | 32000 | 0 | 0 | 2800 | 0 | 0 |
| `sweba2.pikeman18swe.1.5` | Barracks 18c pikeman18swe damage +2 (lvl 6) | 6 | 2 | 15.62 | 32000 | 0 | 0 | 3800 | 0 | 0 |
| `sweba2.pikeman18swe.1.6` | Barracks 18c pikeman18swe damage +2 (lvl 7) | 7 | 2 | 15.62 | 40500 | 0 | 0 | 4800 | 0 | 0 |
| `sweba2.pikeman18swe.2.1` | Barracks 18c pikeman18swe protection +2 (lvl 2) | 2 | 2 | 15.62 | 1500 | 0 | 0 | 500 | 0 | 0 |
| `sweba2.pikeman18swe.2.2` | Barracks 18c pikeman18swe protection +3 (lvl 3) | 3 | 3 | 15.62 | 7000 | 0 | 0 | 1500 | 0 | 0 |
| `sweba2.pikeman18swe.2.3` | Barracks 18c pikeman18swe protection +2 (lvl 4) | 4 | 2 | 15.62 | 37000 | 0 | 0 | 2000 | 0 | 0 |
| `sweba2.pikeman18swe.2.4` | Barracks 18c pikeman18swe protection +3 (lvl 5) | 5 | 3 | 15.62 | 37000 | 0 | 0 | 5500 | 0 | 0 |
| `sweba2.pikeman18swe.2.5` | Barracks 18c pikeman18swe protection +2 (lvl 6) | 6 | 2 | 15.62 | 37000 | 0 | 0 | 5500 | 0 | 0 |
| `sweba2.pikeman18swe.2.6` | Barracks 18c pikeman18swe protection +3 (lvl 7) | 7 | 3 | 15.62 | 64600 | 0 | 0 | 5500 | 0 | 0 |
| `swebar.1` | — | 1 | 140 | 15.62 | 750 | 0 | 0 | 250 | 0 | 0 |
| `swebar.2` | — | 2 | 180 | 15.62 | 25600 | 0 | 0 | 3350 | 2000 | 0 |
| `swebar.drummer.2.1` | Barracks 17c drummer protection +12 (lvl 2) | 2 | 12 | 15.62 | 905 | 0 | 0 | 25 | 0 | 0 |
| `swebar.musketeer.1.1` | Barracks 17c musketeer damage +1 (lvl 2) | 2 | 1 | 15.62 | 1000 | 0 | 0 | 200 | 0 | 0 |
| `swebar.musketeer.1.2` | Barracks 17c musketeer damage +1 (lvl 3) | 3 | 1 | 15.62 | 2000 | 0 | 0 | 200 | 0 | 0 |
| `swebar.musketeer.1.3` | Barracks 17c musketeer damage +2 (lvl 4) | 4 | 2 | 15.62 | 100 | 0 | 0 | 200 | 0 | 0 |
| `swebar.musketeer.2.1` | Barracks 17c musketeer protection +1 (lvl 2) | 2 | 1 | 15.62 | 450 | 0 | 0 | 550 | 300 | 0 |
| `swebar.musketeer.2.2` | Barracks 17c musketeer protection +2 (lvl 3) | 3 | 2 | 15.62 | 405 | 0 | 0 | 150 | 20 | 0 |
| `swebar.musketeer.2.3` | Barracks 17c musketeer protection +2 (lvl 4) | 4 | 2 | 15.62 | 1570 | 0 | 0 | 100 | 290 | 0 |
| `swebar.musketeer.2.4` | Barracks 17c musketeer protection +1 (lvl 5) | 5 | 1 | 15.62 | 1956 | 0 | 0 | 450 | 700 | 0 |
| `swebar.musketeer.2.5` | Barracks 17c musketeer protection +2 (lvl 6) | 6 | 2 | 15.62 | 1660 | 0 | 0 | 650 | 400 | 0 |
| `swebar.musketeer.2.6` | Barracks 17c musketeer protection +2 (lvl 7) | 7 | 2 | 15.62 | 2700 | 0 | 0 | 650 | 100 | 0 |
| `swebar.officer.1.1` | Barracks 17c officer damage +20 (lvl 2) | 2 | 20 | 15.62 | 800 | 0 | 0 | 150 | 0 | 0 |
| `swebar.officer.2.1` | Barracks 17c officer protection +6 (lvl 2) | 2 | 6 | 15.62 | 1050 | 0 | 0 | 350 | 0 | 0 |
| `swebar.pikeman.1.1` | Barracks 17c pikeman damage +1 (lvl 2) | 2 | 1 | 15.62 | 100 | 0 | 0 | 90 | 0 | 0 |
| `swebar.pikeman.1.2` | Barracks 17c pikeman damage +2 (lvl 3) | 3 | 2 | 15.62 | 300 | 0 | 0 | 450 | 0 | 0 |
| `swebar.pikeman.1.3` | Barracks 17c pikeman damage +2 (lvl 4) | 4 | 2 | 15.62 | 4600 | 0 | 0 | 300 | 0 | 0 |
| `swebar.pikeman.1.4` | Barracks 17c pikeman damage +1 (lvl 5) | 5 | 1 | 15.62 | 9200 | 0 | 0 | 1250 | 0 | 0 |
| `swebar.pikeman.1.5` | Barracks 17c pikeman damage +2 (lvl 6) | 6 | 2 | 15.62 | 14030 | 0 | 0 | 2600 | 0 | 0 |
| `swebar.pikeman.1.6` | — | 7 | 2 | 15.62 | 15000 | 0 | 0 | 1875 | 0 | 0 |
| `swebar.pikeman.2.1` | Barracks 17c pikeman protection +1 (lvl 2) | 2 | 1 | 15.62 | 350 | 0 | 0 | 50 | 0 | 0 |
| `swebar.pikeman.2.2` | Barracks 17c pikeman protection +1 (lvl 3) | 3 | 1 | 15.62 | 700 | 0 | 0 | 275 | 0 | 0 |
| `swebar.pikeman.2.3` | Barracks 17c pikeman protection +2 (lvl 4) | 4 | 2 | 15.62 | 2500 | 0 | 0 | 200 | 0 | 0 |
| `swebar.pikeman.2.4` | Barracks 17c pikeman protection +1 (lvl 5) | 5 | 1 | 15.62 | 13005 | 0 | 0 | 997 | 0 | 0 |
| `swebar.pikeman.2.5` | Barracks 17c pikeman protection +1 (lvl 6) | 6 | 1 | 15.62 | 16010 | 0 | 0 | 2550 | 0 | 0 |
| `swebar.pikeman.2.6` | — | 7 | 2 | 15.62 | 11250 | 0 | 0 | 1500 | 0 | 0 |
| `swebla.1` | Manufacture agricultural equipment (field capacity +100%) | 1 | 100 | 15.62 | 0 | 400 | 0 | 90 | 0 | 0 |
| `swebla.2` | Forge metal armature and gratings (building defence +50) | 1 | 50 | 15.62 | 0 | 0 | 12320 | 350 | 900 | 0 |
| `swebla.3` | Forge harnesses for horses (mounted units recruitment speed -33%) | 1 | -3333333 | 15.62 | 0 | 0 | 0 | 3650 | 5300 | 8200 |
| `swebla.4` | Forge bayonets and broadswords for infantry (18c musketeer/grenadier melee attack +5) | 1 | 5 | 15.62 | 0 | 1300 | 0 | 1500 | 900 | 5000 |
| `swebla.5` | Forge new types of broadswords and sabres (cavalry and sword clansman attack +5) | 1 | 5 | 15.62 | 0 | 0 | 0 | 4000 | 7900 | 0 |
| `swebla.6` | Forge new cuirasses (armoured soldiers defence +2) | 1 | 2 | 15.62 | 0 | 0 | 0 | 4950 | 10500 | 0 |
| `swecen.1` | — | 1 | 0 | 9.38 | 37000 | 0 | 0 | 5500 | 1500 | 1500 |
| `swesta.cuirassier.1.1` | Stable cuirassier damage +1 (lvl 2) | 2 | 1 | 15.62 | 11000 | 0 | 0 | 1600 | 0 | 0 |
| `swesta.cuirassier.1.2` | Stable cuirassier damage +1 (lvl 3) | 3 | 1 | 15.62 | 33000 | 0 | 0 | 300 | 0 | 0 |
| `swesta.cuirassier.1.3` | Stable cuirassier damage +1 (lvl 4) | 4 | 1 | 15.62 | 64000 | 0 | 0 | 3200 | 0 | 0 |
| `swesta.cuirassier.1.4` | Stable cuirassier damage +2 (lvl 5) | 5 | 2 | 15.62 | 59000 | 0 | 0 | 2150 | 0 | 0 |
| `swesta.cuirassier.1.5` | Stable cuirassier damage +2 (lvl 6) | 6 | 2 | 15.62 | 52055 | 0 | 0 | 5100 | 0 | 0 |
| `swesta.cuirassier.1.6` | Stable cuirassier damage +3 (lvl 7) | 7 | 3 | 15.62 | 54050 | 0 | 0 | 7020 | 0 | 0 |
| `swesta.cuirassier.2.1` | Stable cuirassier protection +2 (lvl 2) | 2 | 2 | 15.62 | 2505 | 0 | 0 | 350 | 1000 | 0 |
| `swesta.cuirassier.2.2` | Stable cuirassier protection +3 (lvl 3) | 3 | 3 | 15.62 | 2000 | 0 | 0 | 300 | 2000 | 0 |
| `swesta.cuirassier.2.3` | Stable cuirassier protection +3 (lvl 4) | 4 | 3 | 15.62 | 5600 | 0 | 0 | 750 | 3030 | 0 |
| `swesta.cuirassier.2.4` | Stable cuirassier protection +2 (lvl 5) | 5 | 2 | 15.62 | 10700 | 0 | 0 | 6100 | 100 | 0 |
| `swesta.cuirassier.2.5` | Stable cuirassier protection +1 (lvl 6) | 6 | 1 | 15.62 | 8100 | 0 | 0 | 2150 | 5000 | 0 |
| `swesta.cuirassier.2.6` | Stable cuirassier protection +1 (lvl 7) | 7 | 1 | 15.62 | 9200 | 0 | 0 | 4900 | 7060 | 0 |
| `swesta.dragoon.1.1` | Stable dragoon damage +1 (lvl 2) | 2 | 1 | 15.62 | 500 | 0 | 0 | 150 | 0 | 0 |
| `swesta.dragoon.1.2` | Stable dragoon damage +1 (lvl 3) | 3 | 1 | 15.62 | 700 | 0 | 0 | 200 | 0 | 0 |
| `swesta.dragoon.1.3` | Stable dragoon damage +2 (lvl 4) | 4 | 2 | 15.62 | 900 | 0 | 0 | 340 | 0 | 0 |
| `swesta.dragoon.1.4` | Stable dragoon damage +1 (lvl 5) | 5 | 1 | 15.62 | 0 | 0 | 0 | 0 | 0 | 0 |
| `swesta.dragoon.1.5` | Stable dragoon damage +1 (lvl 6) | 6 | 1 | 15.62 | 0 | 0 | 0 | 0 | 0 | 0 |
| `swesta.dragoon.1.6` | Stable dragoon damage +3 (lvl 7) | 7 | 3 | 15.62 | 0 | 0 | 0 | 0 | 0 | 0 |
| `swesta.dragoon.2.1` | Stable dragoon protection +1 (lvl 2) | 2 | 1 | 15.62 | 900 | 0 | 0 | 150 | 0 | 0 |
| `swesta.dragoon.2.2` | Stable dragoon protection +2 (lvl 3) | 3 | 2 | 15.62 | 6600 | 0 | 0 | 650 | 0 | 0 |
| `swesta.dragoon.2.3` | Stable dragoon protection +2 (lvl 4) | 4 | 2 | 15.62 | 5000 | 0 | 0 | 1250 | 0 | 0 |
| `swesta.dragoon.2.4` | Stable dragoon protection +1 (lvl 5) | 5 | 1 | 15.62 | 3000 | 0 | 0 | 700 | 0 | 0 |
| `swesta.dragoon.2.5` | Stable dragoon protection +2 (lvl 6) | 6 | 2 | 15.62 | 1000 | 0 | 0 | 2350 | 0 | 0 |
| `swesta.dragoon.2.6` | Stable dragoon protection +2 (lvl 7) | 7 | 2 | 15.62 | 6001 | 0 | 0 | 6000 | 0 | 0 |
| `swesta.dragoon18.1.1` | Stable dragoon18 damage +2 (lvl 2) | 2 | 2 | 15.62 | 2000 | 0 | 0 | 100 | 0 | 0 |
| `swesta.dragoon18.1.2` | Stable dragoon18 damage +2 (lvl 3) | 3 | 2 | 15.62 | 9000 | 0 | 0 | 350 | 0 | 0 |
| `swesta.dragoon18.1.3` | Stable dragoon18 damage +4 (lvl 4) | 4 | 4 | 15.62 | 12000 | 0 | 0 | 400 | 0 | 0 |
| `swesta.dragoon18.1.4` | Stable dragoon18 damage +2 (lvl 5) | 5 | 2 | 15.62 | 23000 | 0 | 0 | 580 | 0 | 0 |
| `swesta.dragoon18.1.5` | Stable dragoon18 damage +2 (lvl 6) | 6 | 2 | 15.62 | 32000 | 0 | 0 | 680 | 0 | 0 |
| `swesta.dragoon18.1.6` | Stable dragoon18 damage +4 (lvl 7) | 7 | 4 | 15.62 | 42000 | 0 | 0 | 780 | 0 | 0 |
| `swesta.dragoon18.2.1` | Stable dragoon18 protection +1 (lvl 2) | 2 | 1 | 15.62 | 260 | 0 | 0 | 935 | 0 | 0 |
| `swesta.dragoon18.2.2` | Stable dragoon18 protection +1 (lvl 3) | 3 | 1 | 15.62 | 1460 | 0 | 0 | 1150 | 0 | 0 |
| `swesta.dragoon18.2.3` | Stable dragoon18 protection +2 (lvl 4) | 4 | 2 | 15.62 | 12600 | 0 | 0 | 3350 | 0 | 0 |
| `swesta.dragoon18.2.4` | Stable dragoon18 protection +1 (lvl 5) | 5 | 1 | 15.62 | 19600 | 0 | 0 | 2350 | 0 | 0 |
| `swesta.dragoon18.2.5` | Stable dragoon18 protection +2 (lvl 6) | 6 | 2 | 15.62 | 12600 | 0 | 0 | 7350 | 0 | 0 |
| `swesta.dragoon18.2.6` | Stable dragoon18 protection +3 (lvl 7) | 7 | 3 | 15.62 | 26760 | 0 | 0 | 7350 | 0 | 0 |
| `swesta.hackapell.1.1` | Stable hackapell damage +1 (lvl 2) | 2 | 1 | 15.62 | 2000 | 0 | 0 | 500 | 0 | 0 |
| `swesta.hackapell.1.2` | Stable hackapell damage +2 (lvl 3) | 3 | 2 | 15.62 | 5000 | 0 | 0 | 800 | 0 | 0 |
| `swesta.hackapell.1.3` | Stable hackapell damage +2 (lvl 4) | 4 | 2 | 15.62 | 10000 | 0 | 0 | 1200 | 0 | 0 |
| `swesta.hackapell.1.4` | Stable hackapell damage +1 (lvl 5) | 5 | 1 | 15.62 | 20000 | 0 | 0 | 1300 | 0 | 0 |
| `swesta.hackapell.1.5` | Stable hackapell damage +2 (lvl 6) | 6 | 2 | 15.62 | 30000 | 0 | 0 | 3000 | 0 | 0 |
| `swesta.hackapell.1.6` | Stable hackapell damage +2 (lvl 7) | 7 | 2 | 15.62 | 20000 | 0 | 0 | 5000 | 0 | 0 |
| `swesta.hackapell.2.1` | Stable hackapell protection +1 (lvl 2) | 2 | 1 | 15.62 | 2000 | 0 | 0 | 1350 | 0 | 0 |
| `swesta.hackapell.2.2` | Stable hackapell protection +2 (lvl 3) | 3 | 2 | 15.62 | 1500 | 0 | 0 | 2100 | 0 | 0 |
| `swesta.hackapell.2.3` | Stable hackapell protection +2 (lvl 4) | 4 | 2 | 15.62 | 5000 | 0 | 0 | 2300 | 0 | 0 |
| `swesta.hackapell.2.4` | Stable hackapell protection +1 (lvl 5) | 5 | 1 | 15.62 | 10500 | 0 | 0 | 3400 | 0 | 0 |
| `swesta.hackapell.2.5` | Stable hackapell protection +2 (lvl 6) | 6 | 2 | 15.62 | 12600 | 0 | 0 | 4500 | 0 | 0 |
| `swesta.hackapell.2.6` | Stable hackapell protection +2 (lvl 7) | 7 | 2 | 15.62 | 40000 | 0 | 0 | 5000 | 0 | 0 |
| `swesta.hussar.1.1` | Stable hussar damage +1 (lvl 2) | 2 | 1 | 15.62 | 0 | 0 | 0 | 1200 | 1500 | 0 |
| `swesta.hussar.1.2` | Stable hussar damage +2 (lvl 3) | 3 | 2 | 15.62 | 0 | 0 | 0 | 4400 | 1500 | 0 |
| `swesta.hussar.1.3` | Stable hussar damage +3 (lvl 4) | 4 | 3 | 15.62 | 10200 | 0 | 0 | 0 | 1500 | 0 |
| `swesta.hussar.1.4` | Stable hussar damage +4 (lvl 5) | 5 | 4 | 15.62 | 42000 | 0 | 0 | 0 | 3500 | 0 |
| `swesta.hussar.1.5` | Stable hussar damage +1 (lvl 6) | 6 | 1 | 15.62 | 29200 | 0 | 0 | 0 | 5500 | 0 |
| `swesta.hussar.1.6` | Stable hussar damage +1 (lvl 7) | 7 | 1 | 15.62 | 40000 | 0 | 0 | 0 | 4400 | 0 |
| `swesta.hussar.2.1` | Stable hussar protection +1 (lvl 2) | 2 | 1 | 15.62 | 500 | 0 | 0 | 350 | 0 | 0 |
| `swesta.hussar.2.2` | Stable hussar protection +1 (lvl 3) | 3 | 1 | 15.62 | 3900 | 0 | 0 | 3350 | 0 | 0 |
| `swesta.hussar.2.3` | Stable hussar protection +1 (lvl 4) | 4 | 1 | 15.62 | 1100 | 0 | 0 | 5350 | 0 | 0 |
| `swesta.hussar.2.4` | Stable hussar protection +2 (lvl 5) | 5 | 2 | 15.62 | 7800 | 0 | 0 | 8350 | 0 | 0 |
| `swesta.hussar.2.5` | Stable hussar protection +2 (lvl 6) | 6 | 2 | 15.62 | 1700 | 0 | 0 | 17350 | 0 | 0 |
| `swesta.hussar.2.6` | Stable hussar protection +3 (lvl 7) | 7 | 3 | 15.62 | 55200 | 0 | 0 | 17150 | 0 | 0 |
| `swesta.reiterswe.1.1` | Stable reiterswe damage +1 (lvl 2) | 2 | 1 | 15.62 | 500 | 0 | 0 | 100 | 0 | 0 |
| `swesta.reiterswe.1.2` | Stable reiterswe damage +2 (lvl 3) | 3 | 2 | 15.62 | 900 | 0 | 0 | 220 | 0 | 0 |
| `swesta.reiterswe.1.3` | Stable reiterswe damage +1 (lvl 4) | 4 | 1 | 15.62 | 4400 | 0 | 0 | 280 | 0 | 0 |
| `swesta.reiterswe.1.4` | Stable reiterswe damage +1 (lvl 5) | 5 | 1 | 15.62 | 2250 | 0 | 0 | 320 | 0 | 0 |
| `swesta.reiterswe.1.5` | Stable reiterswe damage +1 (lvl 6) | 6 | 1 | 15.62 | 3030 | 0 | 0 | 600 | 0 | 0 |
| `swesta.reiterswe.1.6` | Stable reiterswe damage +1 (lvl 7) | 7 | 1 | 15.62 | 7000 | 0 | 0 | 1800 | 0 | 0 |
| `swesta.reiterswe.2.1` | Stable reiterswe protection +1 (lvl 2) | 2 | 1 | 15.62 | 200 | 0 | 0 | 135 | 300 | 0 |
| `swesta.reiterswe.2.2` | Stable reiterswe protection +1 (lvl 3) | 3 | 1 | 15.62 | 600 | 0 | 0 | 100 | 400 | 0 |
| `swesta.reiterswe.2.3` | Stable reiterswe protection +2 (lvl 4) | 4 | 2 | 15.62 | 800 | 0 | 0 | 200 | 560 | 0 |
| `swesta.reiterswe.2.4` | Stable reiterswe protection +2 (lvl 5) | 5 | 2 | 15.62 | 1600 | 0 | 0 | 300 | 640 | 0 |
| `swesta.reiterswe.2.5` | Stable reiterswe protection +3 (lvl 6) | 6 | 3 | 15.62 | 3200 | 0 | 0 | 350 | 300 | 0 |
| `swesta.reiterswe.2.6` | Stable reiterswe protection +2 (lvl 7) | 7 | 2 | 15.62 | 16000 | 0 | 0 | 1000 | 5000 | 0 |
| `ukrwwa.1` | — | 2 | 5 | 0.03 | 0 | 400 | 0 | 0 | 0 | 0 |

### pru — Prussia

| sid | имя (EN) | level | value | время (s) | F | W | S | G | I | C |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `eurcoa.1` | — | 2 | 5 | 9.38 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `eurcoa.2` | — | 3 | 8 | 9.38 | 5250 | 0 | 0 | 4950 | 0 | 0 |
| `eurcoa.3` | — | 4 | 10 | 9.38 | 12500 | 0 | 0 | 9250 | 0 | 0 |
| `eurcoa.4` | — | 5 | 12 | 9.38 | 15800 | 0 | 0 | 18500 | 0 | 0 |
| `eurcoa.5` | — | 6 | 15 | 9.38 | 19800 | 0 | 0 | 21050 | 0 | 0 |
| `eurcoa.6` | — | 7 | 40 | 9.38 | 50200 | 0 | 0 | 25950 | 0 | 0 |
| `eurgol.1` | — | 2 | 5 | 9.38 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `eurgol.2` | — | 3 | 8 | 9.38 | 5250 | 0 | 0 | 4950 | 0 | 0 |
| `eurgol.3` | — | 4 | 10 | 9.38 | 12500 | 0 | 0 | 9250 | 0 | 0 |
| `eurgol.4` | — | 5 | 12 | 9.38 | 15800 | 0 | 0 | 18500 | 0 | 0 |
| `eurgol.5` | — | 6 | 15 | 9.38 | 19800 | 0 | 0 | 21050 | 0 | 0 |
| `eurgol.6` | — | 7 | 40 | 9.38 | 50200 | 0 | 0 | 25950 | 0 | 0 |
| `euriro.1` | — | 2 | 5 | 9.38 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `euriro.2` | — | 3 | 8 | 9.38 | 5250 | 0 | 0 | 4950 | 0 | 0 |
| `euriro.3` | — | 4 | 10 | 9.38 | 12500 | 0 | 0 | 9250 | 0 | 0 |
| `euriro.4` | — | 5 | 12 | 9.38 | 15800 | 0 | 0 | 18500 | 0 | 0 |
| `euriro.5` | — | 6 | 15 | 9.38 | 19800 | 0 | 0 | 21050 | 0 | 0 |
| `euriro.6` | — | 7 | 40 | 9.38 | 50200 | 0 | 0 | 25950 | 0 | 0 |
| `eurpor.1` | — | 1 | 50 | 46.88 | 0 | 20000 | 0 | 1500 | 0 | 0 |
| `eurswa.1` | — | 2 | 5 | 0.03 | 0 | 0 | 500 | 0 | 0 | 0 |
| `eurtow.1` | — | 2 | -20 | 31.25 | 0 | 0 | 0 | 250 | 0 | 0 |
| `eurtow.2` | — | 3 | -20 | 31.25 | 0 | 0 | 0 | 0 | 350 | 0 |
| `eurtow.3` | — | 4 | -10 | 31.25 | 0 | 0 | 0 | 0 | 0 | 400 |
| `eurtow.4` | — | 5 | -10 | 31.25 | 0 | 0 | 0 | 0 | 450 | 0 |
| `eurtow.5` | — | 6 | -10 | 31.25 | 0 | 0 | 0 | 0 | 0 | 500 |
| `ferry.1` | Improve transport vessel design (+%value% capacity) | 2 | 200 | 15.62 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `pruaca.1` | Cultivate new cultures of wheat (harvesting +40%) | 1 | 40 | 15.62 | 0 | 200 | 0 | 325 | 0 | 0 |
| `pruaca.10` | Raise builders' salary (building construction time -75%) | 1 | -7500000 | 15.62 | 0 | 0 | 0 | 6950 | 0 | 0 |
| `pruaca.11` | Research new fortification grades (durability of walls and towers +80) | 1 | 80 | 15.62 | 0 | 0 | 16200 | 1500 | 0 | 0 |
| `pruaca.12` | Improve firearms: rifled barrel (fire power +10%) | 1 | 10 | 15.62 | 0 | 0 | 0 | 0 | 5000 | 0 |
| `pruaca.13` | Research granular gunpowder (fire power +10%) | 1 | 10 | 15.62 | 0 | 0 | 0 | 4000 | 0 | 0 |
| `pruaca.14` | Research new sulphur purification methods (fire power +15%) | 1 | 15 | 15.62 | 0 | 0 | 0 | 7000 | 0 | 0 |
| `pruaca.15` | Research new nitre purification methods (fire power +25%) | 1 | 25 | 15.62 | 0 | 0 | 0 | 0 | 0 | 11000 |
| `pruaca.16` | Research improved additions to gunpowder formula (artillery range +5%) | 1 | 5 | 15.62 | 0 | 0 | 0 | 2000 | 12150 | 0 |
| `pruaca.17` | Design new barrel types: unicorn, carronade (artillery range +10%) | 1 | 10 | 15.62 | 0 | 0 | 3000 | 4550 | 19200 | 0 |
| `pruaca.18` | Design more durable gun carriage: Gribovalle system (artillery durability +50%) | 1 | 50 | 15.62 | 0 | 0 | 0 | 500 | 3830 | 1500 |
| `pruaca.19` | Design multi-barrelled cannon | 1 | 0 | 15.62 | 0 | 0 | 0 | 1500 | 0 | 2500 |
| `pruaca.2` | Cultivate new cultures of rye (harvesting +50%) | 1 | 50 | 15.62 | 0 | 2400 | 0 | 625 | 0 | 0 |
| `pruaca.20` | Research new sighting devices for artillery (artillery accuracy +35%) | 1 | -35 | 15.62 | 0 | 23540 | 0 | 1900 | 0 | 4250 |
| `pruaca.21` | Finance artillery repair shops (repair all artillery) | 1 | 25 | 15.62 | 0 | 350 | 0 | 100 | 0 | 250 |
| `pruaca.22` | Develop geology (previously hidden deposits appear on the map) | 1 | 0 | 15.62 | 0 | 0 | 0 | 250 | 0 | 0 |
| `pruaca.23` | Develop mining (stone excavation efficiency +100%) | 1 | 100 | 15.62 | 0 | 0 | 0 | 1550 | 3000 | 0 |
| `pruaca.24` | Raise miners' salary (stone excavation efficiency +200%) | 1 | 200 | 15.62 | 4200 | 0 | 0 | 1550 | 0 | 12520 |
| `pruaca.25` | Design Montgolfier (reveals the whole map) | 1 | 0 | 15.62 | 0 | 0 | 0 | 5750 | 0 | 0 |
| `pruaca.26` | Develop medical science (heals all live units) | 1 | 50 | 31.25 | 0 | 0 | 0 | 200 | 0 | 200 |
| `pruaca.27` | Develop mathematics (artillery accuracy +35%) | 1 | -35 | 15.62 | 0 | 12540 | 0 | 8500 | 0 | 57200 |
| `pruaca.28` | Design new rigging types (ship speed +40%) | 1 | 40 | 15.62 | 0 | 65400 | 0 | 24050 | 0 | 0 |
| `pruaca.29` | Design new rib system and new hulls (battleship construction) | 1 | 0 | 15.62 | 0 | 32300 | 0 | 6800 | 9000 | 12800 |
| `pruaca.3` | Raise agriculturists' salary (harvesting +50%) | 1 | 50 | 15.62 | 0 | 3600 | 0 | 850 | 0 | 0 |
| `pruaca.30` | Train carpenters (shipbuilding speed x10) | 1 | -5000000 | 15.62 | 0 | 2300 | 42700 | 1150 | 0 | 0 |
| `pruaca.31` | Design wheellock (rate of fire +30%) | 1 | -30 | 15.62 | 0 | 0 | 6000 | 5500 | 4200 | 0 |
| `pruaca.32` | Design flintlock (musket cost -50%) | 1 | 0 | 15.62 | 0 | 0 | 0 | 6050 | 0 | 7750 |
| `pruaca.33` | Design paper cartridge and iron ramrod (rate of fire +30%) | 1 | -30 | 15.62 | 0 | 5000 | 0 | 5500 | 0 | 15200 |
| `pruaca.34` | Research improved steel grades for cuirasses (armoured soldier defence +2) | 1 | 2 | 15.62 | 0 | 0 | 0 | 9750 | 0 | 0 |
| `pruaca.35` | Design bayonet: barrel-inserted, bayonet with a tube (cold steel weapons +5) | 1 | 5 | 15.62 | 0 | 0 | 0 | 11500 | 0 | 0 |
| `pruaca.36` | Research new steel grades (18c musketeer/grenadier melee attack efficiency +25%) | 1 | 25 | 15.62 | 0 | 0 | 0 | 19500 | 0 | 0 |
| `pruaca.4` | Carry out field melioration (field capacity +200%) | 1 | 200 | 15.62 | 0 | 1000 | 0 | 475 | 0 | 0 |
| `pruaca.5` | Design new tackle and fishing nets (boat efficiency +100%) | 1 | 100 | 15.62 | 0 | 12400 | 0 | 2520 | 0 | 0 |
| `pruaca.6` | Develop new woodworking methods (frigate building) | 1 | 0 | 15.62 | 0 | 12400 | 0 | 7040 | 0 | 0 |
| `pruaca.7` | Build new shipyards for fishing boats (fishing boat cost -85%) | 1 | 0 | 15.62 | 0 | 7300 | 0 | 1220 | 0 | 0 |
| `pruaca.8` | Design new woodworking tools (woodcutting efficiency +100%) | 1 | 100 | 15.62 | 5500 | 0 | 0 | 550 | 0 | 0 |
| `pruaca.9` | Use new construction materials (durability of buildings +85) | 1 | 85 | 15.62 | 0 | 9400 | 7850 | 1150 | 0 | 0 |
| `pruart.cannon.1.1` | — | 2 | — | 10.0 | 0 | 1000 | 500 | 300 | 0 | 0 |
| `pruart.cannon.1.2` | — | 3 | — | 10.0 | 0 | 3000 | 1000 | 500 | 0 | 0 |
| `pruart.cannon.1.3` | — | 4 | — | 10.0 | 0 | 6000 | 2000 | 1000 | 0 | 0 |
| `pruart.cannon.1.4` | — | 5 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `pruart.cannon.1.5` | — | 6 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `pruart.cannon.1.6` | — | 7 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `pruart.cannon.2.1` | — | 2 | -2500000 | 10.0 | 0 | 0 | 0 | 500 | 1000 | 0 |
| `pruart.cannon.2.2` | — | 3 | -2500000 | 10.0 | 0 | 0 | 0 | 1000 | 2000 | 0 |
| `pruart.cannon.2.3` | — | 4 | -2500000 | 10.0 | 0 | 0 | 0 | 2000 | 3000 | 0 |
| `pruart.cannon.2.4` | — | 5 | -2000000 | 15.62 | 2560 | 0 | 0 | 0 | 0 | 0 |
| `pruart.cannon.2.5` | — | 6 | -2000000 | 15.62 | 3560 | 0 | 0 | 0 | 0 | 0 |
| `pruart.cannon.2.6` | — | 7 | -2000000 | 15.62 | 5560 | 0 | 0 | 0 | 0 | 0 |
| `pruart.howitzer.1.1` | — | 2 | — | 10.0 | 0 | 1000 | 500 | 300 | 0 | 0 |
| `pruart.howitzer.1.2` | — | 3 | — | 10.0 | 0 | 3000 | 1000 | 500 | 0 | 0 |
| `pruart.howitzer.1.3` | — | 4 | — | 10.0 | 0 | 6000 | 2000 | 1000 | 0 | 0 |
| `pruart.howitzer.1.4` | — | 5 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `pruart.howitzer.1.5` | — | 6 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `pruart.howitzer.1.6` | — | 7 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `pruart.howitzer.2.1` | — | 2 | -2500000 | 10.0 | 0 | 0 | 0 | 500 | 1000 | 0 |
| `pruart.howitzer.2.2` | — | 3 | -2500000 | 10.0 | 0 | 0 | 0 | 1000 | 2000 | 0 |
| `pruart.howitzer.2.3` | — | 4 | -2500000 | 10.0 | 0 | 0 | 0 | 2000 | 3000 | 0 |
| `pruart.howitzer.2.4` | — | 5 | -2000000 | 31.25 | 2560 | 0 | 0 | 0 | 0 | 0 |
| `pruart.howitzer.2.5` | — | 6 | -2000000 | 31.25 | 3560 | 0 | 0 | 0 | 0 | 0 |
| `pruart.howitzer.2.6` | — | 7 | -2000000 | 31.25 | 5560 | 0 | 0 | 0 | 0 | 0 |
| `pruba2.drummer18.2.1` | Barracks 18c drummer18 protection +15 (lvl 2) | 2 | 15 | 15.62 | 900 | 0 | 0 | 45 | 0 | 0 |
| `pruba2.grenadierpru.1.1` | Barracks 18c grenadierpru damage +2 (lvl 2) | 2 | 2 | 15.62 | 1000 | 0 | 0 | 800 | 0 | 0 |
| `pruba2.grenadierpru.1.2` | Barracks 18c grenadierpru damage +3 (lvl 3) | 3 | 3 | 15.62 | 13000 | 0 | 0 | 2800 | 0 | 0 |
| `pruba2.grenadierpru.1.3` | Barracks 18c grenadierpru damage +4 (lvl 4) | 4 | 4 | 15.62 | 32000 | 0 | 0 | 1800 | 0 | 0 |
| `pruba2.grenadierpru.1.4` | Barracks 18c grenadierpru damage +5 (lvl 5) | 5 | 5 | 15.62 | 52000 | 0 | 0 | 4800 | 0 | 0 |
| `pruba2.grenadierpru.1.5` | Barracks 18c grenadierpru damage +6 (lvl 6) | 6 | 6 | 15.62 | 42000 | 0 | 0 | 3800 | 0 | 0 |
| `pruba2.grenadierpru.1.6` | Barracks 18c grenadierpru damage +1500 (lvl 7) | 7 | 1500 | 15.62 | 64000 | 0 | 0 | 14800 | 0 | 0 |
| `pruba2.grenadierpru.2.1` | Barracks 18c grenadierpru protection +1 (lvl 2) | 2 | 1 | 15.62 | 3205 | 0 | 0 | 375 | 0 | 0 |
| `pruba2.grenadierpru.2.2` | Barracks 18c grenadierpru protection +2 (lvl 3) | 3 | 2 | 15.62 | 11030 | 0 | 0 | 4350 | 0 | 0 |
| `pruba2.grenadierpru.2.3` | Barracks 18c grenadierpru protection +3 (lvl 4) | 4 | 3 | 15.62 | 36206 | 0 | 0 | 500 | 0 | 0 |
| `pruba2.grenadierpru.2.4` | Barracks 18c grenadierpru protection +1 (lvl 5) | 5 | 1 | 15.62 | 34950 | 0 | 0 | 1350 | 0 | 0 |
| `pruba2.grenadierpru.2.5` | Barracks 18c grenadierpru protection +2 (lvl 6) | 6 | 2 | 15.62 | 30060 | 0 | 0 | 2150 | 0 | 0 |
| `pruba2.grenadierpru.2.6` | Barracks 18c grenadierpru protection +3 (lvl 7) | 7 | 3 | 15.62 | 64000 | 0 | 0 | 2550 | 0 | 0 |
| `pruba2.musketeer18pru.1.1` | Barracks 18c musketeer18pru damage +1 (lvl 2) | 2 | 1 | 15.62 | 900 | 0 | 0 | 700 | 0 | 0 |
| `pruba2.musketeer18pru.1.2` | Barracks 18c musketeer18pru damage +1 (lvl 3) | 3 | 1 | 15.62 | 1600 | 0 | 0 | 800 | 0 | 0 |
| `pruba2.musketeer18pru.1.3` | Barracks 18c musketeer18pru damage +2 (lvl 4) | 4 | 2 | 15.62 | 2500 | 0 | 0 | 900 | 0 | 0 |
| `pruba2.musketeer18pru.1.4` | Barracks 18c musketeer18pru damage +2 (lvl 5) | 5 | 2 | 15.62 | 2000 | 0 | 0 | 600 | 0 | 0 |
| `pruba2.musketeer18pru.1.5` | Barracks 18c musketeer18pru damage +3 (lvl 6) | 6 | 3 | 15.62 | 3500 | 0 | 0 | 1000 | 0 | 0 |
| `pruba2.musketeer18pru.1.6` | Barracks 18c musketeer18pru damage +3 (lvl 7) | 7 | 3 | 15.62 | 3000 | 0 | 0 | 800 | 0 | 0 |
| `pruba2.musketeer18pru.2.1` | Barracks 18c musketeer18pru protection +1 (lvl 2) | 2 | 1 | 15.62 | 3500 | 0 | 0 | 350 | 0 | 0 |
| `pruba2.musketeer18pru.2.2` | Barracks 18c musketeer18pru protection +2 (lvl 3) | 3 | 2 | 15.62 | 11230 | 0 | 0 | 1350 | 0 | 0 |
| `pruba2.musketeer18pru.2.3` | Barracks 18c musketeer18pru protection +2 (lvl 4) | 4 | 2 | 15.62 | 35706 | 0 | 0 | 4000 | 0 | 0 |
| `pruba2.musketeer18pru.2.4` | Barracks 18c musketeer18pru protection +1 (lvl 5) | 5 | 1 | 15.62 | 36556 | 0 | 0 | 4350 | 0 | 0 |
| `pruba2.musketeer18pru.2.5` | Barracks 18c musketeer18pru protection +2 (lvl 6) | 6 | 2 | 15.62 | 30060 | 0 | 0 | 1350 | 0 | 0 |
| `pruba2.musketeer18pru.2.6` | Barracks 18c musketeer18pru protection +2 (lvl 7) | 7 | 2 | 15.62 | 37600 | 0 | 0 | 1350 | 0 | 0 |
| `pruba2.officer18.1.1` | Barracks 18c officer18 damage +30 (lvl 2) | 2 | 30 | 15.62 | 1200 | 0 | 0 | 750 | 0 | 0 |
| `pruba2.officer18.2.1` | Barracks 18c officer18 protection +12 (lvl 2) | 2 | 12 | 15.62 | 1500 | 0 | 0 | 375 | 0 | 0 |
| `pruba2.pikeman18.1.1` | Barracks 18c pikeman18 damage +2 (lvl 2) | 2 | 2 | 15.62 | 2000 | 0 | 0 | 800 | 0 | 0 |
| `pruba2.pikeman18.1.2` | Barracks 18c pikeman18 damage +2 (lvl 3) | 3 | 2 | 15.62 | 8000 | 0 | 0 | 1200 | 0 | 0 |
| `pruba2.pikeman18.1.3` | Barracks 18c pikeman18 damage +2 (lvl 4) | 4 | 2 | 15.62 | 20000 | 0 | 0 | 2500 | 0 | 0 |
| `pruba2.pikeman18.1.4` | Barracks 18c pikeman18 damage +2 (lvl 5) | 5 | 2 | 15.62 | 32000 | 0 | 0 | 2800 | 0 | 0 |
| `pruba2.pikeman18.1.5` | Barracks 18c pikeman18 damage +2 (lvl 6) | 6 | 2 | 15.62 | 32000 | 0 | 0 | 3800 | 0 | 0 |
| `pruba2.pikeman18.1.6` | Barracks 18c pikeman18 damage +2 (lvl 7) | 7 | 2 | 15.62 | 40500 | 0 | 0 | 4800 | 0 | 0 |
| `pruba2.pikeman18.2.1` | Barracks 18c pikeman18 protection +2 (lvl 2) | 2 | 2 | 15.62 | 1500 | 0 | 0 | 500 | 0 | 0 |
| `pruba2.pikeman18.2.2` | Barracks 18c pikeman18 protection +3 (lvl 3) | 3 | 3 | 15.62 | 7000 | 0 | 0 | 1500 | 0 | 0 |
| `pruba2.pikeman18.2.3` | Barracks 18c pikeman18 protection +2 (lvl 4) | 4 | 2 | 15.62 | 37000 | 0 | 0 | 2000 | 0 | 0 |
| `pruba2.pikeman18.2.4` | Barracks 18c pikeman18 protection +3 (lvl 5) | 5 | 3 | 15.62 | 37000 | 0 | 0 | 5500 | 0 | 0 |
| `pruba2.pikeman18.2.5` | Barracks 18c pikeman18 protection +2 (lvl 6) | 6 | 2 | 15.62 | 37000 | 0 | 0 | 5500 | 0 | 0 |
| `pruba2.pikeman18.2.6` | Barracks 18c pikeman18 protection +3 (lvl 7) | 7 | 3 | 15.62 | 64600 | 0 | 0 | 5500 | 0 | 0 |
| `prubar.1` | — | 1 | 140 | 15.62 | 750 | 0 | 0 | 250 | 0 | 0 |
| `prubar.2` | — | 2 | 180 | 15.62 | 25600 | 0 | 0 | 3350 | 2000 | 0 |
| `prubar.drummer.2.1` | Barracks 17c drummer protection +12 (lvl 2) | 2 | 12 | 15.62 | 1205 | 0 | 0 | 90 | 0 | 0 |
| `prubar.musketeer.1.1` | Barracks 17c musketeer damage +1 (lvl 2) | 2 | 1 | 15.62 | 2000 | 0 | 0 | 100 | 0 | 0 |
| `prubar.musketeer.1.2` | Barracks 17c musketeer damage +1 (lvl 3) | 3 | 1 | 15.62 | 1000 | 0 | 0 | 300 | 0 | 0 |
| `prubar.musketeer.1.3` | Barracks 17c musketeer damage +2 (lvl 4) | 4 | 2 | 15.62 | 500 | 0 | 0 | 700 | 0 | 0 |
| `prubar.musketeer.2.1` | Barracks 17c musketeer protection +1 (lvl 2) | 2 | 1 | 15.62 | 170 | 0 | 0 | 50 | 100 | 0 |
| `prubar.musketeer.2.2` | Barracks 17c musketeer protection +2 (lvl 3) | 3 | 2 | 15.62 | 405 | 0 | 0 | 150 | 200 | 0 |
| `prubar.musketeer.2.3` | Barracks 17c musketeer protection +2 (lvl 4) | 4 | 2 | 15.62 | 1570 | 0 | 0 | 100 | 350 | 0 |
| `prubar.musketeer.2.4` | Barracks 17c musketeer protection +1 (lvl 5) | 5 | 1 | 15.62 | 1556 | 0 | 0 | 550 | 100 | 0 |
| `prubar.musketeer.2.5` | Barracks 17c musketeer protection +2 (lvl 6) | 6 | 2 | 15.62 | 1060 | 0 | 0 | 850 | 400 | 0 |
| `prubar.musketeer.2.6` | Barracks 17c musketeer protection +2 (lvl 7) | 7 | 2 | 15.62 | 3700 | 0 | 0 | 450 | 700 | 0 |
| `prubar.officer.1.1` | Barracks 17c officer damage +20 (lvl 2) | 2 | 20 | 15.62 | 150 | 0 | 0 | 25 | 0 | 0 |
| `prubar.officer.2.1` | Barracks 17c officer protection +6 (lvl 2) | 2 | 6 | 15.62 | 1650 | 0 | 0 | 395 | 0 | 0 |
| `prubar.pikeman.1.1` | Barracks 17c pikeman damage +1 (lvl 2) | 2 | 1 | 15.62 | 3600 | 0 | 0 | 450 | 0 | 0 |
| `prubar.pikeman.1.2` | Barracks 17c pikeman damage +2 (lvl 3) | 3 | 2 | 15.62 | 1300 | 0 | 0 | 300 | 0 | 0 |
| `prubar.pikeman.1.3` | Barracks 17c pikeman damage +2 (lvl 4) | 4 | 2 | 15.62 | 200 | 0 | 0 | 50 | 0 | 0 |
| `prubar.pikeman.1.4` | Barracks 17c pikeman damage +1 (lvl 5) | 5 | 1 | 15.62 | 6800 | 0 | 0 | 1950 | 0 | 0 |
| `prubar.pikeman.1.5` | Barracks 17c pikeman damage +2 (lvl 6) | 6 | 2 | 15.62 | 15030 | 0 | 0 | 2300 | 0 | 0 |
| `prubar.pikeman.1.6` | — | 7 | 2 | 15.62 | 15000 | 0 | 0 | 1875 | 0 | 0 |
| `prubar.pikeman.2.1` | Barracks 17c pikeman protection +1 (lvl 2) | 2 | 1 | 15.62 | 175 | 0 | 0 | 40 | 0 | 0 |
| `prubar.pikeman.2.2` | Barracks 17c pikeman protection +1 (lvl 3) | 3 | 1 | 15.62 | 990 | 0 | 0 | 275 | 0 | 0 |
| `prubar.pikeman.2.3` | Barracks 17c pikeman protection +2 (lvl 4) | 4 | 2 | 15.62 | 4700 | 0 | 0 | 280 | 0 | 0 |
| `prubar.pikeman.2.4` | Barracks 17c pikeman protection +1 (lvl 5) | 5 | 1 | 15.62 | 9505 | 0 | 0 | 707 | 0 | 0 |
| `prubar.pikeman.2.5` | Barracks 17c pikeman protection +1 (lvl 6) | 6 | 1 | 15.62 | 17510 | 0 | 0 | 2950 | 0 | 0 |
| `prubar.pikeman.2.6` | — | 7 | 2 | 15.62 | 11250 | 0 | 0 | 1500 | 0 | 0 |
| `prubla.1` | Manufacture agricultural equipment (field capacity +100%) | 1 | 100 | 15.62 | 0 | 400 | 0 | 90 | 0 | 0 |
| `prubla.2` | Forge metal armature and gratings (building defence +50) | 1 | 50 | 15.62 | 0 | 0 | 12320 | 350 | 900 | 0 |
| `prubla.3` | Forge harnesses for horses (mounted units recruitment speed -33%) | 1 | -3333333 | 15.62 | 0 | 0 | 0 | 3650 | 4300 | 5200 |
| `prubla.4` | Forge bayonets and broadswords for infantry (18c musketeer/grenadier melee attack +5) | 1 | 5 | 15.62 | 0 | 1300 | 0 | 1500 | 900 | 5000 |
| `prubla.5` | Forge new types of broadswords and sabres (cavalry and sword clansman attack +5) | 1 | 5 | 15.62 | 0 | 0 | 0 | 9550 | 7900 | 0 |
| `prubla.6` | Forge new cuirasses (armoured soldiers defence +2) | 1 | 2 | 15.62 | 0 | 0 | 0 | 4950 | 10500 | 0 |
| `prucen.1` | — | 1 | 0 | 9.38 | 20000 | 0 | 0 | 6500 | 1100 | 1100 |
| `prusta.cuirassier.1.1` | Stable cuirassier damage +1 (lvl 2) | 2 | 1 | 15.62 | 10000 | 0 | 0 | 200 | 0 | 0 |
| `prusta.cuirassier.1.2` | Stable cuirassier damage +1 (lvl 3) | 3 | 1 | 15.62 | 34000 | 0 | 0 | 1700 | 0 | 0 |
| `prusta.cuirassier.1.3` | Stable cuirassier damage +1 (lvl 4) | 4 | 1 | 15.62 | 64000 | 0 | 0 | 2100 | 0 | 0 |
| `prusta.cuirassier.1.4` | Stable cuirassier damage +2 (lvl 5) | 5 | 2 | 15.62 | 58000 | 0 | 0 | 4150 | 0 | 0 |
| `prusta.cuirassier.1.5` | Stable cuirassier damage +2 (lvl 6) | 6 | 2 | 15.62 | 59055 | 0 | 0 | 3100 | 0 | 0 |
| `prusta.cuirassier.1.6` | Stable cuirassier damage +3 (lvl 7) | 7 | 3 | 15.62 | 47050 | 0 | 0 | 8150 | 0 | 0 |
| `prusta.cuirassier.2.1` | Stable cuirassier protection +2 (lvl 2) | 2 | 2 | 15.62 | 1520 | 0 | 0 | 450 | 1000 | 0 |
| `prusta.cuirassier.2.2` | Stable cuirassier protection +3 (lvl 3) | 3 | 3 | 15.62 | 7000 | 0 | 0 | 750 | 2000 | 0 |
| `prusta.cuirassier.2.3` | Stable cuirassier protection +3 (lvl 4) | 4 | 3 | 15.62 | 3600 | 0 | 0 | 3300 | 3050 | 0 |
| `prusta.cuirassier.2.4` | Stable cuirassier protection +2 (lvl 5) | 5 | 2 | 15.62 | 8700 | 0 | 0 | 3200 | 200 | 0 |
| `prusta.cuirassier.2.5` | Stable cuirassier protection +1 (lvl 6) | 6 | 1 | 15.62 | 8700 | 0 | 0 | 2650 | 4300 | 0 |
| `prusta.cuirassier.2.6` | Stable cuirassier protection +1 (lvl 7) | 7 | 1 | 15.62 | 11200 | 0 | 0 | 4700 | 6760 | 0 |
| `prusta.dragoon.1.1` | Stable dragoon damage +1 (lvl 2) | 2 | 1 | 15.62 | 700 | 0 | 0 | 250 | 0 | 0 |
| `prusta.dragoon.1.2` | Stable dragoon damage +1 (lvl 3) | 3 | 1 | 15.62 | 500 | 0 | 0 | 100 | 0 | 0 |
| `prusta.dragoon.1.3` | Stable dragoon damage +2 (lvl 4) | 4 | 2 | 15.62 | 900 | 0 | 0 | 640 | 0 | 0 |
| `prusta.dragoon.1.4` | Stable dragoon damage +1 (lvl 5) | 5 | 1 | 15.62 | 0 | 0 | 0 | 0 | 0 | 0 |
| `prusta.dragoon.1.5` | Stable dragoon damage +1 (lvl 6) | 6 | 1 | 15.62 | 0 | 0 | 0 | 0 | 0 | 0 |
| `prusta.dragoon.1.6` | Stable dragoon damage +3 (lvl 7) | 7 | 3 | 15.62 | 0 | 0 | 0 | 0 | 0 | 0 |
| `prusta.dragoon.2.1` | Stable dragoon protection +1 (lvl 2) | 2 | 1 | 15.62 | 500 | 0 | 0 | 250 | 0 | 0 |
| `prusta.dragoon.2.2` | Stable dragoon protection +2 (lvl 3) | 3 | 2 | 15.62 | 6300 | 0 | 0 | 850 | 0 | 0 |
| `prusta.dragoon.2.3` | Stable dragoon protection +2 (lvl 4) | 4 | 2 | 15.62 | 4600 | 0 | 0 | 1350 | 0 | 0 |
| `prusta.dragoon.2.4` | Stable dragoon protection +1 (lvl 5) | 5 | 1 | 15.62 | 2500 | 0 | 0 | 750 | 0 | 0 |
| `prusta.dragoon.2.5` | Stable dragoon protection +2 (lvl 6) | 6 | 2 | 15.62 | 800 | 0 | 0 | 2750 | 0 | 0 |
| `prusta.dragoon.2.6` | Stable dragoon protection +2 (lvl 7) | 7 | 2 | 15.62 | 2001 | 0 | 0 | 7200 | 0 | 0 |
| `prusta.dragoon18.1.1` | Stable dragoon18 damage +2 (lvl 2) | 2 | 2 | 15.62 | 4500 | 0 | 0 | 200 | 0 | 0 |
| `prusta.dragoon18.1.2` | Stable dragoon18 damage +2 (lvl 3) | 3 | 2 | 15.62 | 5500 | 0 | 0 | 250 | 0 | 0 |
| `prusta.dragoon18.1.3` | Stable dragoon18 damage +4 (lvl 4) | 4 | 4 | 15.62 | 22000 | 0 | 0 | 500 | 0 | 0 |
| `prusta.dragoon18.1.4` | Stable dragoon18 damage +2 (lvl 5) | 5 | 2 | 15.62 | 13000 | 0 | 0 | 480 | 0 | 0 |
| `prusta.dragoon18.1.5` | Stable dragoon18 damage +2 (lvl 6) | 6 | 2 | 15.62 | 42000 | 0 | 0 | 780 | 0 | 0 |
| `prusta.dragoon18.1.6` | Stable dragoon18 damage +4 (lvl 7) | 7 | 4 | 15.62 | 32000 | 0 | 0 | 680 | 0 | 0 |
| `prusta.dragoon18.2.1` | Stable dragoon18 protection +1 (lvl 2) | 2 | 1 | 15.62 | 750 | 0 | 0 | 935 | 0 | 0 |
| `prusta.dragoon18.2.2` | Stable dragoon18 protection +1 (lvl 3) | 3 | 1 | 15.62 | 1260 | 0 | 0 | 1150 | 0 | 0 |
| `prusta.dragoon18.2.3` | Stable dragoon18 protection +2 (lvl 4) | 4 | 2 | 15.62 | 10600 | 0 | 0 | 2350 | 0 | 0 |
| `prusta.dragoon18.2.4` | Stable dragoon18 protection +1 (lvl 5) | 5 | 1 | 15.62 | 22600 | 0 | 0 | 6350 | 0 | 0 |
| `prusta.dragoon18.2.5` | Stable dragoon18 protection +2 (lvl 6) | 6 | 2 | 15.62 | 19600 | 0 | 0 | 4350 | 0 | 0 |
| `prusta.dragoon18.2.6` | Stable dragoon18 protection +3 (lvl 7) | 7 | 3 | 15.62 | 15760 | 0 | 0 | 9350 | 0 | 0 |
| `prusta.hussarpru.1.1` | Stable hussarpru damage +1 (lvl 2) | 2 | 1 | 15.62 | 0 | 0 | 0 | 2800 | 1600 | 0 |
| `prusta.hussarpru.1.2` | Stable hussarpru damage +1 (lvl 3) | 3 | 1 | 15.62 | 0 | 0 | 0 | 2800 | 1400 | 0 |
| `prusta.hussarpru.1.3` | Stable hussarpru damage +2 (lvl 4) | 4 | 2 | 15.62 | 10200 | 0 | 0 | 0 | 3000 | 0 |
| `prusta.hussarpru.1.4` | Stable hussarpru damage +2 (lvl 5) | 5 | 2 | 15.62 | 42000 | 0 | 0 | 0 | 2000 | 0 |
| `prusta.hussarpru.1.5` | Stable hussarpru damage +3 (lvl 6) | 6 | 3 | 15.62 | 29200 | 0 | 0 | 0 | 5500 | 0 |
| `prusta.hussarpru.1.6` | Stable hussarpru damage +3 (lvl 7) | 7 | 3 | 15.62 | 40000 | 0 | 0 | 0 | 4000 | 0 |
| `prusta.hussarpru.2.1` | Stable hussarpru protection +1 (lvl 2) | 2 | 1 | 15.62 | 150 | 0 | 0 | 1250 | 0 | 0 |
| `prusta.hussarpru.2.2` | Stable hussarpru protection +1 (lvl 3) | 3 | 1 | 15.62 | 3200 | 0 | 0 | 2450 | 0 | 0 |
| `prusta.hussarpru.2.3` | Stable hussarpru protection +1 (lvl 4) | 4 | 1 | 15.62 | 3600 | 0 | 0 | 3350 | 0 | 0 |
| `prusta.hussarpru.2.4` | Stable hussarpru protection +2 (lvl 5) | 5 | 2 | 15.62 | 6000 | 0 | 0 | 10350 | 0 | 0 |
| `prusta.hussarpru.2.5` | Stable hussarpru protection +2 (lvl 6) | 6 | 2 | 15.62 | 9000 | 0 | 0 | 13350 | 0 | 0 |
| `prusta.hussarpru.2.6` | Stable hussarpru protection +3 (lvl 7) | 7 | 3 | 15.62 | 48000 | 0 | 0 | 22150 | 0 | 0 |
| `prusta.reiter.1.1` | Stable reiter damage +1 (lvl 2) | 2 | 1 | 15.62 | 800 | 0 | 0 | 100 | 0 | 0 |
| `prusta.reiter.1.2` | Stable reiter damage +2 (lvl 3) | 3 | 2 | 15.62 | 800 | 0 | 0 | 220 | 0 | 0 |
| `prusta.reiter.1.3` | Stable reiter damage +1 (lvl 4) | 4 | 1 | 15.62 | 2400 | 0 | 0 | 380 | 0 | 0 |
| `prusta.reiter.1.4` | Stable reiter damage +1 (lvl 5) | 5 | 1 | 15.62 | 4250 | 0 | 0 | 220 | 0 | 0 |
| `prusta.reiter.1.5` | Stable reiter damage +1 (lvl 6) | 6 | 1 | 15.62 | 4030 | 0 | 0 | 900 | 0 | 0 |
| `prusta.reiter.1.6` | Stable reiter damage +1 (lvl 7) | 7 | 1 | 15.62 | 6000 | 0 | 0 | 1600 | 0 | 0 |
| `prusta.reiter.2.1` | Stable reiter protection +2 (lvl 2) | 2 | 2 | 15.62 | 200 | 0 | 0 | 135 | 400 | 0 |
| `prusta.reiter.2.2` | Stable reiter protection +3 (lvl 3) | 3 | 3 | 15.62 | 600 | 0 | 0 | 100 | 300 | 0 |
| `prusta.reiter.2.3` | Stable reiter protection +3 (lvl 4) | 4 | 3 | 15.62 | 800 | 0 | 0 | 200 | 560 | 0 |
| `prusta.reiter.2.4` | Stable reiter protection +2 (lvl 5) | 5 | 2 | 15.62 | 1600 | 0 | 0 | 300 | 340 | 0 |
| `prusta.reiter.2.5` | Stable reiter protection +1 (lvl 6) | 6 | 1 | 15.62 | 2200 | 0 | 0 | 350 | 600 | 0 |
| `prusta.reiter.2.6` | Stable reiter protection +1 (lvl 7) | 7 | 1 | 15.62 | 17000 | 0 | 0 | 950 | 5200 | 0 |
| `ukrwwa.1` | — | 2 | 5 | 0.03 | 0 | 400 | 0 | 0 | 0 | 0 |

### ven — Venice

| sid | имя (EN) | level | value | время (s) | F | W | S | G | I | C |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `eurcoa.1` | — | 2 | 5 | 9.38 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `eurcoa.2` | — | 3 | 8 | 9.38 | 5250 | 0 | 0 | 4950 | 0 | 0 |
| `eurcoa.3` | — | 4 | 10 | 9.38 | 12500 | 0 | 0 | 9250 | 0 | 0 |
| `eurcoa.4` | — | 5 | 12 | 9.38 | 15800 | 0 | 0 | 18500 | 0 | 0 |
| `eurcoa.5` | — | 6 | 15 | 9.38 | 19800 | 0 | 0 | 21050 | 0 | 0 |
| `eurcoa.6` | — | 7 | 40 | 9.38 | 50200 | 0 | 0 | 25950 | 0 | 0 |
| `eurgol.1` | — | 2 | 5 | 9.38 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `eurgol.2` | — | 3 | 8 | 9.38 | 5250 | 0 | 0 | 4950 | 0 | 0 |
| `eurgol.3` | — | 4 | 10 | 9.38 | 12500 | 0 | 0 | 9250 | 0 | 0 |
| `eurgol.4` | — | 5 | 12 | 9.38 | 15800 | 0 | 0 | 18500 | 0 | 0 |
| `eurgol.5` | — | 6 | 15 | 9.38 | 19800 | 0 | 0 | 21050 | 0 | 0 |
| `eurgol.6` | — | 7 | 40 | 9.38 | 50200 | 0 | 0 | 25950 | 0 | 0 |
| `euriro.1` | — | 2 | 5 | 9.38 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `euriro.2` | — | 3 | 8 | 9.38 | 5250 | 0 | 0 | 4950 | 0 | 0 |
| `euriro.3` | — | 4 | 10 | 9.38 | 12500 | 0 | 0 | 9250 | 0 | 0 |
| `euriro.4` | — | 5 | 12 | 9.38 | 15800 | 0 | 0 | 18500 | 0 | 0 |
| `euriro.5` | — | 6 | 15 | 9.38 | 19800 | 0 | 0 | 21050 | 0 | 0 |
| `euriro.6` | — | 7 | 40 | 9.38 | 50200 | 0 | 0 | 25950 | 0 | 0 |
| `eurpor.1` | — | 1 | 50 | 46.88 | 0 | 20000 | 0 | 1500 | 0 | 0 |
| `eurswa.1` | — | 2 | 5 | 0.03 | 0 | 0 | 500 | 0 | 0 | 0 |
| `eurtow.1` | — | 2 | -20 | 31.25 | 0 | 0 | 0 | 250 | 0 | 0 |
| `eurtow.2` | — | 3 | -20 | 31.25 | 0 | 0 | 0 | 0 | 350 | 0 |
| `eurtow.3` | — | 4 | -10 | 31.25 | 0 | 0 | 0 | 0 | 0 | 400 |
| `eurtow.4` | — | 5 | -10 | 31.25 | 0 | 0 | 0 | 0 | 450 | 0 |
| `eurtow.5` | — | 6 | -10 | 31.25 | 0 | 0 | 0 | 0 | 0 | 500 |
| `ferry.1` | Improve transport vessel design (+%value% capacity) | 2 | 200 | 15.62 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `ukrwwa.1` | — | 2 | 5 | 0.03 | 0 | 400 | 0 | 0 | 0 | 0 |
| `venaca.1` | Cultivate new cultures of wheat (harvesting +40%) | 1 | 40 | 15.62 | 0 | 200 | 0 | 325 | 0 | 0 |
| `venaca.10` | Raise builders' salary (building construction time -75%) | 1 | -7500000 | 15.62 | 0 | 0 | 0 | 6950 | 0 | 0 |
| `venaca.11` | Research new fortification grades (durability of walls and towers +80) | 1 | 80 | 15.62 | 0 | 0 | 16200 | 1500 | 0 | 0 |
| `venaca.12` | Improve firearms: rifled barrel (fire power +10%) | 1 | 10 | 15.62 | 0 | 0 | 0 | 0 | 5000 | 0 |
| `venaca.13` | Research granular gunpowder (fire power +10%) | 1 | 10 | 15.62 | 0 | 0 | 0 | 4000 | 0 | 0 |
| `venaca.14` | Research new sulphur purification methods (fire power +15%) | 1 | 15 | 15.62 | 0 | 0 | 0 | 7000 | 0 | 0 |
| `venaca.15` | Research new nitre purification methods (fire power +25%) | 1 | 25 | 15.62 | 0 | 0 | 0 | 0 | 0 | 11000 |
| `venaca.16` | Research improved additions to gunpowder formula (artillery range +5%) | 1 | 5 | 15.62 | 0 | 0 | 0 | 2000 | 12150 | 0 |
| `venaca.17` | Design new barrel types: unicorn, carronade (artillery range +10%) | 1 | 10 | 15.62 | 0 | 0 | 3000 | 4550 | 19200 | 0 |
| `venaca.18` | Design more durable gun carriage: Gribovalle system (artillery durability +50%) | 1 | 50 | 15.62 | 0 | 0 | 0 | 500 | 3830 | 1500 |
| `venaca.19` | Design multi-barrelled cannon | 1 | 0 | 15.62 | 0 | 0 | 0 | 1500 | 0 | 2500 |
| `venaca.2` | Cultivate new cultures of rye (harvesting +50%) | 1 | 50 | 15.62 | 0 | 2400 | 0 | 625 | 0 | 0 |
| `venaca.20` | Research new sighting devices for artillery (artillery accuracy +35%) | 1 | -35 | 15.62 | 0 | 3540 | 0 | 2000 | 0 | 7250 |
| `venaca.21` | Finance artillery repair shops (repair all artillery) | 1 | 25 | 15.62 | 0 | 350 | 0 | 100 | 0 | 250 |
| `venaca.22` | Develop geology (previously hidden deposits appear on the map) | 1 | 0 | 15.62 | 0 | 0 | 0 | 250 | 0 | 0 |
| `venaca.23` | Develop mining (stone excavation efficiency +100%) | 1 | 100 | 15.62 | 0 | 0 | 0 | 1550 | 3000 | 0 |
| `venaca.24` | Raise miners' salary (stone excavation efficiency +200%) | 1 | 200 | 15.62 | 4200 | 0 | 0 | 1550 | 0 | 12520 |
| `venaca.25` | Design Montgolfier (reveals the whole map) | 1 | 0 | 15.62 | 0 | 0 | 0 | 5750 | 0 | 0 |
| `venaca.26` | Develop medical science (heals all live units) | 1 | 50 | 31.25 | 0 | 0 | 0 | 200 | 0 | 200 |
| `venaca.27` | Develop mathematics (artillery accuracy +35%) | 1 | -35 | 15.62 | 0 | 9540 | 0 | 12000 | 0 | 65200 |
| `venaca.28` | Design new rigging types (ship speed +40%) | 1 | 40 | 15.62 | 0 | 65400 | 0 | 24050 | 0 | 0 |
| `venaca.29` | Design new rib system and new hulls (battleship construction) | 1 | 0 | 15.62 | 0 | 32300 | 0 | 6800 | 9000 | 12800 |
| `venaca.3` | Raise agriculturists' salary (harvesting +50%) | 1 | 50 | 15.62 | 0 | 3600 | 0 | 850 | 0 | 0 |
| `venaca.30` | Train carpenters (shipbuilding speed x10) | 1 | -5000000 | 15.62 | 0 | 2300 | 42700 | 1150 | 0 | 0 |
| `venaca.31` | Design wheellock (rate of fire +30%) | 1 | -30 | 15.62 | 0 | 0 | 6000 | 5500 | 4200 | 0 |
| `venaca.32` | Design flintlock (musket cost -50%) | 1 | 0 | 15.62 | 0 | 0 | 0 | 6050 | 0 | 7750 |
| `venaca.33` | Design paper cartridge and iron ramrod (rate of fire +30%) | 1 | -30 | 15.62 | 0 | 5000 | 0 | 5500 | 0 | 15200 |
| `venaca.34` | Research improved steel grades for cuirasses (armoured soldier defence +2) | 1 | 2 | 15.62 | 0 | 0 | 0 | 9750 | 0 | 0 |
| `venaca.35` | Design bayonet: barrel-inserted, bayonet with a tube (cold steel weapons +5) | 1 | 5 | 15.62 | 0 | 0 | 0 | 11500 | 0 | 0 |
| `venaca.36` | Research new steel grades (18c musketeer/grenadier melee attack efficiency +25%) | 1 | 25 | 15.62 | 0 | 0 | 0 | 19500 | 0 | 0 |
| `venaca.4` | Carry out field melioration (field capacity +200%) | 1 | 200 | 15.62 | 0 | 1000 | 0 | 475 | 0 | 0 |
| `venaca.5` | Design new tackle and fishing nets (boat efficiency +100%) | 1 | 100 | 15.62 | 0 | 12400 | 0 | 2520 | 0 | 0 |
| `venaca.6` | Develop new woodworking methods (frigate building) | 1 | 0 | 15.62 | 0 | 12400 | 0 | 7040 | 0 | 0 |
| `venaca.7` | Build new shipyards for fishing boats (fishing boat cost -85%) | 1 | 0 | 15.62 | 0 | 7300 | 0 | 1220 | 0 | 0 |
| `venaca.8` | Design new woodworking tools (woodcutting efficiency +100%) | 1 | 100 | 15.62 | 5500 | 0 | 0 | 550 | 0 | 0 |
| `venaca.9` | Use new construction materials (durability of buildings +85) | 1 | 85 | 15.62 | 0 | 9400 | 7850 | 1150 | 0 | 0 |
| `venart.cannon.1.1` | — | 2 | — | 10.0 | 0 | 1000 | 500 | 300 | 0 | 0 |
| `venart.cannon.1.2` | — | 3 | — | 10.0 | 0 | 3000 | 1000 | 500 | 0 | 0 |
| `venart.cannon.1.3` | — | 4 | — | 10.0 | 0 | 6000 | 2000 | 1000 | 0 | 0 |
| `venart.cannon.1.4` | — | 5 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `venart.cannon.1.5` | — | 6 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `venart.cannon.1.6` | — | 7 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `venart.cannon.2.1` | — | 2 | -2500000 | 10.0 | 0 | 0 | 0 | 500 | 1000 | 0 |
| `venart.cannon.2.2` | — | 3 | -2500000 | 10.0 | 0 | 0 | 0 | 1000 | 2000 | 0 |
| `venart.cannon.2.3` | — | 4 | -2500000 | 10.0 | 0 | 0 | 0 | 2000 | 3000 | 0 |
| `venart.cannon.2.4` | — | 5 | -2000000 | 15.62 | 2560 | 0 | 0 | 0 | 0 | 0 |
| `venart.cannon.2.5` | — | 6 | -2000000 | 15.62 | 3560 | 0 | 0 | 0 | 0 | 0 |
| `venart.cannon.2.6` | — | 7 | -2000000 | 15.62 | 5560 | 0 | 0 | 0 | 0 | 0 |
| `venart.howitzer.1.1` | — | 2 | — | 10.0 | 0 | 1000 | 500 | 300 | 0 | 0 |
| `venart.howitzer.1.2` | — | 3 | — | 10.0 | 0 | 3000 | 1000 | 500 | 0 | 0 |
| `venart.howitzer.1.3` | — | 4 | — | 10.0 | 0 | 6000 | 2000 | 1000 | 0 | 0 |
| `venart.howitzer.1.4` | — | 5 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `venart.howitzer.1.5` | — | 6 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `venart.howitzer.1.6` | — | 7 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `venart.howitzer.2.1` | — | 2 | -2500000 | 10.0 | 0 | 0 | 0 | 500 | 1000 | 0 |
| `venart.howitzer.2.2` | — | 3 | -2500000 | 10.0 | 0 | 0 | 0 | 1000 | 2000 | 0 |
| `venart.howitzer.2.3` | — | 4 | -2500000 | 10.0 | 0 | 0 | 0 | 2000 | 3000 | 0 |
| `venart.howitzer.2.4` | — | 5 | -2000000 | 31.25 | 2560 | 0 | 0 | 0 | 0 | 0 |
| `venart.howitzer.2.5` | — | 6 | -2000000 | 31.25 | 3560 | 0 | 0 | 0 | 0 | 0 |
| `venart.howitzer.2.6` | — | 7 | -2000000 | 31.25 | 5560 | 0 | 0 | 0 | 0 | 0 |
| `venba2.drummer18.2.1` | Barracks 18c drummer18 protection +15 (lvl 2) | 2 | 15 | 15.62 | 706 | 0 | 0 | 50 | 0 | 0 |
| `venba2.grenadier.1.1` | Barracks 18c grenadier damage +2 (lvl 2) | 2 | 2 | 15.62 | 2000 | 0 | 0 | 800 | 0 | 0 |
| `venba2.grenadier.1.2` | Barracks 18c grenadier damage +3 (lvl 3) | 3 | 3 | 15.62 | 12000 | 0 | 0 | 1800 | 0 | 0 |
| `venba2.grenadier.1.3` | Barracks 18c grenadier damage +4 (lvl 4) | 4 | 4 | 15.62 | 32000 | 0 | 0 | 2800 | 0 | 0 |
| `venba2.grenadier.1.4` | Barracks 18c grenadier damage +5 (lvl 5) | 5 | 5 | 15.62 | 42000 | 0 | 0 | 3800 | 0 | 0 |
| `venba2.grenadier.1.5` | Barracks 18c grenadier damage +6 (lvl 6) | 6 | 6 | 15.62 | 52000 | 0 | 0 | 4800 | 0 | 0 |
| `venba2.grenadier.1.6` | Barracks 18c grenadier damage +1500 (lvl 7) | 7 | 1500 | 15.62 | 62000 | 0 | 0 | 15800 | 0 | 0 |
| `venba2.grenadier.2.1` | Barracks 18c grenadier protection +1 (lvl 2) | 2 | 1 | 15.62 | 3706 | 0 | 0 | 350 | 0 | 0 |
| `venba2.grenadier.2.2` | Barracks 18c grenadier protection +2 (lvl 3) | 3 | 2 | 15.62 | 11030 | 0 | 0 | 1350 | 0 | 0 |
| `venba2.grenadier.2.3` | Barracks 18c grenadier protection +3 (lvl 4) | 4 | 3 | 15.62 | 35706 | 0 | 0 | 3000 | 0 | 0 |
| `venba2.grenadier.2.4` | Barracks 18c grenadier protection +1 (lvl 5) | 5 | 1 | 15.62 | 36556 | 0 | 0 | 3350 | 0 | 0 |
| `venba2.grenadier.2.5` | Barracks 18c grenadier protection +2 (lvl 6) | 6 | 2 | 15.62 | 30060 | 0 | 0 | 1350 | 0 | 0 |
| `venba2.grenadier.2.6` | Barracks 18c grenadier protection +3 (lvl 7) | 7 | 3 | 15.62 | 64000 | 0 | 0 | 1350 | 0 | 0 |
| `venba2.musketeer18.1.1` | Barracks 18c musketeer18 damage +1 (lvl 2) | 2 | 1 | 15.62 | 1000 | 0 | 0 | 800 | 0 | 0 |
| `venba2.musketeer18.1.2` | Barracks 18c musketeer18 damage +1 (lvl 3) | 3 | 1 | 15.62 | 1500 | 0 | 0 | 800 | 0 | 0 |
| `venba2.musketeer18.1.3` | Barracks 18c musketeer18 damage +2 (lvl 4) | 4 | 2 | 15.62 | 2000 | 0 | 0 | 800 | 0 | 0 |
| `venba2.musketeer18.1.4` | Barracks 18c musketeer18 damage +2 (lvl 5) | 5 | 2 | 15.62 | 2500 | 0 | 0 | 800 | 0 | 0 |
| `venba2.musketeer18.1.5` | Barracks 18c musketeer18 damage +3 (lvl 6) | 6 | 3 | 15.62 | 3000 | 0 | 0 | 800 | 0 | 0 |
| `venba2.musketeer18.1.6` | Barracks 18c musketeer18 damage +3 (lvl 7) | 7 | 3 | 15.62 | 3500 | 0 | 0 | 800 | 0 | 0 |
| `venba2.musketeer18.2.1` | Barracks 18c musketeer18 protection +1 (lvl 2) | 2 | 1 | 15.62 | 3706 | 0 | 0 | 350 | 0 | 0 |
| `venba2.musketeer18.2.2` | Barracks 18c musketeer18 protection +2 (lvl 3) | 3 | 2 | 15.62 | 11030 | 0 | 0 | 1350 | 0 | 0 |
| `venba2.musketeer18.2.3` | Barracks 18c musketeer18 protection +2 (lvl 4) | 4 | 2 | 15.62 | 35706 | 0 | 0 | 4000 | 0 | 0 |
| `venba2.musketeer18.2.4` | Barracks 18c musketeer18 protection +1 (lvl 5) | 5 | 1 | 15.62 | 36556 | 0 | 0 | 4350 | 0 | 0 |
| `venba2.musketeer18.2.5` | Barracks 18c musketeer18 protection +2 (lvl 6) | 6 | 2 | 15.62 | 30060 | 0 | 0 | 1350 | 0 | 0 |
| `venba2.musketeer18.2.6` | Barracks 18c musketeer18 protection +2 (lvl 7) | 7 | 2 | 15.62 | 37600 | 0 | 0 | 1350 | 0 | 0 |
| `venba2.officer18.1.1` | Barracks 18c officer18 damage +30 (lvl 2) | 2 | 30 | 15.62 | 1000 | 0 | 0 | 800 | 0 | 0 |
| `venba2.officer18.2.1` | Barracks 18c officer18 protection +12 (lvl 2) | 2 | 12 | 15.62 | 1706 | 0 | 0 | 350 | 0 | 0 |
| `venba2.pikeman18.1.1` | Barracks 18c pikeman18 damage +2 (lvl 2) | 2 | 2 | 15.62 | 2000 | 0 | 0 | 800 | 0 | 0 |
| `venba2.pikeman18.1.2` | Barracks 18c pikeman18 damage +2 (lvl 3) | 3 | 2 | 15.62 | 8000 | 0 | 0 | 1200 | 0 | 0 |
| `venba2.pikeman18.1.3` | Barracks 18c pikeman18 damage +2 (lvl 4) | 4 | 2 | 15.62 | 20000 | 0 | 0 | 2500 | 0 | 0 |
| `venba2.pikeman18.1.4` | Barracks 18c pikeman18 damage +2 (lvl 5) | 5 | 2 | 15.62 | 32000 | 0 | 0 | 2800 | 0 | 0 |
| `venba2.pikeman18.1.5` | Barracks 18c pikeman18 damage +2 (lvl 6) | 6 | 2 | 15.62 | 32000 | 0 | 0 | 3800 | 0 | 0 |
| `venba2.pikeman18.1.6` | Barracks 18c pikeman18 damage +2 (lvl 7) | 7 | 2 | 15.62 | 40500 | 0 | 0 | 4800 | 0 | 0 |
| `venba2.pikeman18.2.1` | Barracks 18c pikeman18 protection +2 (lvl 2) | 2 | 2 | 15.62 | 1500 | 0 | 0 | 500 | 0 | 0 |
| `venba2.pikeman18.2.2` | Barracks 18c pikeman18 protection +3 (lvl 3) | 3 | 3 | 15.62 | 7000 | 0 | 0 | 1500 | 0 | 0 |
| `venba2.pikeman18.2.3` | Barracks 18c pikeman18 protection +2 (lvl 4) | 4 | 2 | 15.62 | 37000 | 0 | 0 | 2000 | 0 | 0 |
| `venba2.pikeman18.2.4` | Barracks 18c pikeman18 protection +3 (lvl 5) | 5 | 3 | 15.62 | 37000 | 0 | 0 | 5500 | 0 | 0 |
| `venba2.pikeman18.2.5` | Barracks 18c pikeman18 protection +2 (lvl 6) | 6 | 2 | 15.62 | 37000 | 0 | 0 | 5500 | 0 | 0 |
| `venba2.pikeman18.2.6` | Barracks 18c pikeman18 protection +3 (lvl 7) | 7 | 3 | 15.62 | 64600 | 0 | 0 | 5500 | 0 | 0 |
| `venbar.1` | — | 1 | 140 | 15.62 | 750 | 0 | 0 | 250 | 0 | 0 |
| `venbar.2` | — | 2 | 180 | 15.62 | 25600 | 0 | 0 | 3350 | 2000 | 0 |
| `venbar.drummer.2.1` | Barracks 17c drummer protection +12 (lvl 2) | 2 | 12 | 15.62 | 706 | 0 | 0 | 50 | 0 | 0 |
| `venbar.musketeer.1.1` | Barracks 17c musketeer damage +1 (lvl 2) | 2 | 1 | 15.62 | 2000 | 0 | 0 | 100 | 0 | 0 |
| `venbar.musketeer.1.2` | Barracks 17c musketeer damage +1 (lvl 3) | 3 | 1 | 15.62 | 1000 | 0 | 0 | 300 | 0 | 0 |
| `venbar.musketeer.1.3` | Barracks 17c musketeer damage +2 (lvl 4) | 4 | 2 | 15.62 | 500 | 0 | 0 | 700 | 0 | 0 |
| `venbar.musketeer.2.1` | Barracks 17c musketeer protection +1 (lvl 2) | 2 | 1 | 15.62 | 170 | 0 | 0 | 50 | 100 | 0 |
| `venbar.musketeer.2.2` | Barracks 17c musketeer protection +2 (lvl 3) | 3 | 2 | 15.62 | 405 | 0 | 0 | 150 | 200 | 0 |
| `venbar.musketeer.2.3` | Barracks 17c musketeer protection +2 (lvl 4) | 4 | 2 | 15.62 | 1570 | 0 | 0 | 100 | 350 | 0 |
| `venbar.musketeer.2.4` | Barracks 17c musketeer protection +1 (lvl 5) | 5 | 1 | 15.62 | 1556 | 0 | 0 | 550 | 100 | 0 |
| `venbar.musketeer.2.5` | Barracks 17c musketeer protection +2 (lvl 6) | 6 | 2 | 15.62 | 1060 | 0 | 0 | 850 | 400 | 0 |
| `venbar.musketeer.2.6` | Barracks 17c musketeer protection +2 (lvl 7) | 7 | 2 | 15.62 | 3700 | 0 | 0 | 450 | 700 | 0 |
| `venbar.officer.1.1` | Barracks 17c officer damage +20 (lvl 2) | 2 | 20 | 15.62 | 100 | 0 | 0 | 50 | 0 | 0 |
| `venbar.officer.2.1` | Barracks 17c officer protection +6 (lvl 2) | 2 | 6 | 15.62 | 1450 | 0 | 0 | 450 | 0 | 0 |
| `venbar.pikeman.1.1` | Barracks 17c pikeman damage +1 (lvl 2) | 2 | 1 | 15.62 | 200 | 0 | 0 | 50 | 0 | 0 |
| `venbar.pikeman.1.2` | Barracks 17c pikeman damage +2 (lvl 3) | 3 | 2 | 15.62 | 1300 | 0 | 0 | 300 | 0 | 0 |
| `venbar.pikeman.1.3` | Barracks 17c pikeman damage +2 (lvl 4) | 4 | 2 | 15.62 | 3600 | 0 | 0 | 450 | 0 | 0 |
| `venbar.pikeman.1.4` | Barracks 17c pikeman damage +1 (lvl 5) | 5 | 1 | 15.62 | 7200 | 0 | 0 | 1850 | 0 | 0 |
| `venbar.pikeman.1.5` | Barracks 17c pikeman damage +2 (lvl 6) | 6 | 2 | 15.62 | 16030 | 0 | 0 | 2000 | 0 | 0 |
| `venbar.pikeman.1.6` | — | 7 | 2 | 15.62 | 15000 | 0 | 0 | 1875 | 0 | 0 |
| `venbar.pikeman.2.1` | Barracks 17c pikeman protection +1 (lvl 2) | 2 | 1 | 15.62 | 150 | 0 | 0 | 50 | 0 | 0 |
| `venbar.pikeman.2.2` | Barracks 17c pikeman protection +1 (lvl 3) | 3 | 1 | 15.62 | 900 | 0 | 0 | 175 | 0 | 0 |
| `venbar.pikeman.2.3` | Barracks 17c pikeman protection +2 (lvl 4) | 4 | 2 | 15.62 | 4500 | 0 | 0 | 300 | 0 | 0 |
| `venbar.pikeman.2.4` | Barracks 17c pikeman protection +1 (lvl 5) | 5 | 1 | 15.62 | 9005 | 0 | 0 | 507 | 0 | 0 |
| `venbar.pikeman.2.5` | Barracks 17c pikeman protection +1 (lvl 6) | 6 | 1 | 15.62 | 18010 | 0 | 0 | 3050 | 0 | 0 |
| `venbar.pikeman.2.6` | — | 7 | 2 | 15.62 | 11250 | 0 | 0 | 1500 | 0 | 0 |
| `venbla.1` | Manufacture agricultural equipment (field capacity +100%) | 1 | 100 | 15.62 | 0 | 400 | 0 | 90 | 0 | 0 |
| `venbla.2` | Forge metal armature and gratings (building defence +50) | 1 | 50 | 15.62 | 0 | 0 | 12320 | 350 | 900 | 0 |
| `venbla.3` | Forge harnesses for horses (mounted units recruitment speed -33%) | 1 | -3333333 | 15.62 | 0 | 0 | 0 | 650 | 9800 | 530 |
| `venbla.4` | Forge bayonets and broadswords for infantry (18c musketeer/grenadier melee attack +5) | 1 | 5 | 15.62 | 0 | 1300 | 0 | 1500 | 900 | 5000 |
| `venbla.5` | Forge new types of broadswords and sabres (cavalry and sword clansman attack +5) | 1 | 5 | 15.62 | 0 | 0 | 0 | 4000 | 7900 | 0 |
| `venbla.6` | Forge new cuirasses (armoured soldiers defence +2) | 1 | 2 | 15.62 | 0 | 0 | 0 | 4950 | 10500 | 0 |
| `vencen.1` | — | 1 | 0 | 9.38 | 40000 | 0 | 0 | 3000 | 2500 | 2500 |
| `vensta.cuirassier.1.1` | Stable cuirassier damage +1 (lvl 2) | 2 | 1 | 15.62 | 12000 | 0 | 0 | 600 | 0 | 0 |
| `vensta.cuirassier.1.2` | Stable cuirassier damage +1 (lvl 3) | 3 | 1 | 15.62 | 32000 | 0 | 0 | 1300 | 0 | 0 |
| `vensta.cuirassier.1.3` | Stable cuirassier damage +1 (lvl 4) | 4 | 1 | 15.62 | 62000 | 0 | 0 | 2200 | 0 | 0 |
| `vensta.cuirassier.1.4` | Stable cuirassier damage +2 (lvl 5) | 5 | 2 | 15.62 | 61000 | 0 | 0 | 3150 | 0 | 0 |
| `vensta.cuirassier.1.5` | Stable cuirassier damage +2 (lvl 6) | 6 | 2 | 15.62 | 57055 | 0 | 0 | 4100 | 0 | 0 |
| `vensta.cuirassier.1.6` | Stable cuirassier damage +3 (lvl 7) | 7 | 3 | 15.62 | 49050 | 0 | 0 | 8020 | 0 | 0 |
| `vensta.cuirassier.2.1` | Stable cuirassier protection +2 (lvl 2) | 2 | 2 | 15.62 | 1760 | 0 | 0 | 350 | 1000 | 0 |
| `vensta.cuirassier.2.2` | Stable cuirassier protection +3 (lvl 3) | 3 | 3 | 15.62 | 3000 | 0 | 0 | 750 | 2000 | 0 |
| `vensta.cuirassier.2.3` | Stable cuirassier protection +3 (lvl 4) | 4 | 3 | 15.62 | 7600 | 0 | 0 | 300 | 3030 | 0 |
| `vensta.cuirassier.2.4` | Stable cuirassier protection +2 (lvl 5) | 5 | 2 | 15.62 | 8700 | 0 | 0 | 6200 | 100 | 0 |
| `vensta.cuirassier.2.5` | Stable cuirassier protection +1 (lvl 6) | 6 | 1 | 15.62 | 8700 | 0 | 0 | 2350 | 5000 | 0 |
| `vensta.cuirassier.2.6` | Stable cuirassier protection +1 (lvl 7) | 7 | 1 | 15.62 | 9700 | 0 | 0 | 4444 | 7060 | 0 |
| `vensta.dragoon.1.1` | Stable dragoon damage +1 (lvl 2) | 2 | 1 | 15.62 | 500 | 0 | 0 | 150 | 0 | 0 |
| `vensta.dragoon.1.2` | Stable dragoon damage +1 (lvl 3) | 3 | 1 | 15.62 | 700 | 0 | 0 | 200 | 0 | 0 |
| `vensta.dragoon.1.3` | Stable dragoon damage +2 (lvl 4) | 4 | 2 | 15.62 | 900 | 0 | 0 | 340 | 0 | 0 |
| `vensta.dragoon.1.4` | Stable dragoon damage +1 (lvl 5) | 5 | 1 | 15.62 | 0 | 0 | 0 | 0 | 0 | 0 |
| `vensta.dragoon.1.5` | Stable dragoon damage +1 (lvl 6) | 6 | 1 | 15.62 | 0 | 0 | 0 | 0 | 0 | 0 |
| `vensta.dragoon.1.6` | Stable dragoon damage +3 (lvl 7) | 7 | 3 | 15.62 | 0 | 0 | 0 | 0 | 0 | 0 |
| `vensta.dragoon.2.1` | Stable dragoon protection +1 (lvl 2) | 2 | 1 | 15.62 | 900 | 0 | 0 | 150 | 0 | 0 |
| `vensta.dragoon.2.2` | Stable dragoon protection +2 (lvl 3) | 3 | 2 | 15.62 | 6600 | 0 | 0 | 750 | 0 | 0 |
| `vensta.dragoon.2.3` | Stable dragoon protection +2 (lvl 4) | 4 | 2 | 15.62 | 5000 | 0 | 0 | 1250 | 0 | 0 |
| `vensta.dragoon.2.4` | Stable dragoon protection +1 (lvl 5) | 5 | 1 | 15.62 | 3000 | 0 | 0 | 700 | 0 | 0 |
| `vensta.dragoon.2.5` | Stable dragoon protection +2 (lvl 6) | 6 | 2 | 15.62 | 1000 | 0 | 0 | 2350 | 0 | 0 |
| `vensta.dragoon.2.6` | Stable dragoon protection +2 (lvl 7) | 7 | 2 | 15.62 | 6001 | 0 | 0 | 6000 | 0 | 0 |
| `vensta.dragoon18.1.1` | Stable dragoon18 damage +2 (lvl 2) | 2 | 2 | 15.62 | 2000 | 0 | 0 | 100 | 0 | 0 |
| `vensta.dragoon18.1.2` | Stable dragoon18 damage +2 (lvl 3) | 3 | 2 | 15.62 | 9000 | 0 | 0 | 350 | 0 | 0 |
| `vensta.dragoon18.1.3` | Stable dragoon18 damage +4 (lvl 4) | 4 | 4 | 15.62 | 12000 | 0 | 0 | 400 | 0 | 0 |
| `vensta.dragoon18.1.4` | Stable dragoon18 damage +2 (lvl 5) | 5 | 2 | 15.62 | 23000 | 0 | 0 | 580 | 0 | 0 |
| `vensta.dragoon18.1.5` | Stable dragoon18 damage +2 (lvl 6) | 6 | 2 | 15.62 | 32000 | 0 | 0 | 680 | 0 | 0 |
| `vensta.dragoon18.1.6` | Stable dragoon18 damage +4 (lvl 7) | 7 | 4 | 15.62 | 42000 | 0 | 0 | 780 | 0 | 0 |
| `vensta.dragoon18.2.1` | Stable dragoon18 protection +1 (lvl 2) | 2 | 1 | 15.62 | 760 | 0 | 0 | 935 | 0 | 0 |
| `vensta.dragoon18.2.2` | Stable dragoon18 protection +1 (lvl 3) | 3 | 1 | 15.62 | 1260 | 0 | 0 | 1150 | 0 | 0 |
| `vensta.dragoon18.2.3` | Stable dragoon18 protection +2 (lvl 4) | 4 | 2 | 15.62 | 15600 | 0 | 0 | 2350 | 0 | 0 |
| `vensta.dragoon18.2.4` | Stable dragoon18 protection +1 (lvl 5) | 5 | 1 | 15.62 | 17600 | 0 | 0 | 3350 | 0 | 0 |
| `vensta.dragoon18.2.5` | Stable dragoon18 protection +2 (lvl 6) | 6 | 2 | 15.62 | 19600 | 0 | 0 | 5350 | 0 | 0 |
| `vensta.dragoon18.2.6` | Stable dragoon18 protection +3 (lvl 7) | 7 | 3 | 15.62 | 21760 | 0 | 0 | 9350 | 0 | 0 |
| `vensta.hussar.1.1` | Stable hussar damage +1 (lvl 2) | 2 | 1 | 15.62 | 0 | 0 | 0 | 1800 | 1000 | 0 |
| `vensta.hussar.1.2` | Stable hussar damage +2 (lvl 3) | 3 | 2 | 15.62 | 0 | 0 | 0 | 3800 | 2000 | 0 |
| `vensta.hussar.1.3` | Stable hussar damage +3 (lvl 4) | 4 | 3 | 15.62 | 20200 | 0 | 0 | 0 | 2000 | 0 |
| `vensta.hussar.1.4` | Stable hussar damage +4 (lvl 5) | 5 | 4 | 15.62 | 32000 | 0 | 0 | 0 | 3000 | 0 |
| `vensta.hussar.1.5` | Stable hussar damage +1 (lvl 6) | 6 | 1 | 15.62 | 49200 | 0 | 0 | 0 | 3500 | 0 |
| `vensta.hussar.1.6` | Stable hussar damage +1 (lvl 7) | 7 | 1 | 15.62 | 20000 | 0 | 0 | 0 | 6000 | 0 |
| `vensta.hussar.2.1` | Stable hussar protection +1 (lvl 2) | 2 | 1 | 15.62 | 1760 | 0 | 0 | 1350 | 0 | 0 |
| `vensta.hussar.2.2` | Stable hussar protection +1 (lvl 3) | 3 | 1 | 15.62 | 1900 | 0 | 0 | 2350 | 0 | 0 |
| `vensta.hussar.2.3` | Stable hussar protection +1 (lvl 4) | 4 | 1 | 15.62 | 1600 | 0 | 0 | 5350 | 0 | 0 |
| `vensta.hussar.2.4` | Stable hussar protection +2 (lvl 5) | 5 | 2 | 15.62 | 8000 | 0 | 0 | 8350 | 0 | 0 |
| `vensta.hussar.2.5` | Stable hussar protection +2 (lvl 6) | 6 | 2 | 15.62 | 2000 | 0 | 0 | 15350 | 0 | 0 |
| `vensta.hussar.2.6` | Stable hussar protection +3 (lvl 7) | 7 | 3 | 15.62 | 56000 | 0 | 0 | 20150 | 0 | 0 |
| `vensta.reiter.1.1` | Stable reiter damage +1 (lvl 2) | 2 | 1 | 15.62 | 500 | 0 | 0 | 100 | 0 | 0 |
| `vensta.reiter.1.2` | Stable reiter damage +2 (lvl 3) | 3 | 2 | 15.62 | 900 | 0 | 0 | 220 | 0 | 0 |
| `vensta.reiter.1.3` | Stable reiter damage +1 (lvl 4) | 4 | 1 | 15.62 | 4400 | 0 | 0 | 280 | 0 | 0 |
| `vensta.reiter.1.4` | Stable reiter damage +1 (lvl 5) | 5 | 1 | 15.62 | 2250 | 0 | 0 | 320 | 0 | 0 |
| `vensta.reiter.1.5` | Stable reiter damage +1 (lvl 6) | 6 | 1 | 15.62 | 3030 | 0 | 0 | 600 | 0 | 0 |
| `vensta.reiter.1.6` | Stable reiter damage +1 (lvl 7) | 7 | 1 | 15.62 | 7000 | 0 | 0 | 1800 | 0 | 0 |
| `vensta.reiter.2.1` | Stable reiter protection +2 (lvl 2) | 2 | 2 | 15.62 | 200 | 0 | 0 | 135 | 300 | 0 |
| `vensta.reiter.2.2` | Stable reiter protection +3 (lvl 3) | 3 | 3 | 15.62 | 600 | 0 | 0 | 100 | 400 | 0 |
| `vensta.reiter.2.3` | Stable reiter protection +3 (lvl 4) | 4 | 3 | 15.62 | 800 | 0 | 0 | 200 | 560 | 0 |
| `vensta.reiter.2.4` | Stable reiter protection +2 (lvl 5) | 5 | 2 | 15.62 | 1600 | 0 | 0 | 300 | 640 | 0 |
| `vensta.reiter.2.5` | Stable reiter protection +1 (lvl 6) | 6 | 1 | 15.62 | 3200 | 0 | 0 | 350 | 300 | 0 |
| `vensta.reiter.2.6` | Stable reiter protection +1 (lvl 7) | 7 | 1 | 15.62 | 16000 | 0 | 0 | 1000 | 5000 | 0 |

### tur — Turkey

| sid | имя (EN) | level | value | время (s) | F | W | S | G | I | C |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `eurcoa.1` | — | 2 | 5 | 9.38 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `eurcoa.2` | — | 3 | 8 | 9.38 | 5250 | 0 | 0 | 4950 | 0 | 0 |
| `eurcoa.3` | — | 4 | 10 | 9.38 | 12500 | 0 | 0 | 9250 | 0 | 0 |
| `eurcoa.4` | — | 5 | 12 | 9.38 | 15800 | 0 | 0 | 18500 | 0 | 0 |
| `eurcoa.5` | — | 6 | 15 | 9.38 | 19800 | 0 | 0 | 21050 | 0 | 0 |
| `eurcoa.6` | — | 7 | 40 | 9.38 | 7080 | 0 | 0 | 25410 | 0 | 0 |
| `eurgol.1` | — | 2 | 5 | 9.38 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `eurgol.2` | — | 3 | 8 | 9.38 | 5250 | 0 | 0 | 4950 | 0 | 0 |
| `eurgol.3` | — | 4 | 10 | 9.38 | 12500 | 0 | 0 | 9250 | 0 | 0 |
| `eurgol.4` | — | 5 | 12 | 9.38 | 15800 | 0 | 0 | 18500 | 0 | 0 |
| `eurgol.5` | — | 6 | 15 | 9.38 | 19800 | 0 | 0 | 21050 | 0 | 0 |
| `eurgol.6` | — | 7 | 40 | 9.38 | 7080 | 0 | 0 | 25410 | 0 | 0 |
| `euriro.1` | — | 2 | 5 | 9.38 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `euriro.2` | — | 3 | 8 | 9.38 | 5250 | 0 | 0 | 4950 | 0 | 0 |
| `euriro.3` | — | 4 | 10 | 9.38 | 12500 | 0 | 0 | 9250 | 0 | 0 |
| `euriro.4` | — | 5 | 12 | 9.38 | 15800 | 0 | 0 | 18500 | 0 | 0 |
| `euriro.5` | — | 6 | 15 | 9.38 | 19800 | 0 | 0 | 21050 | 0 | 0 |
| `euriro.6` | — | 7 | 40 | 9.38 | 7080 | 0 | 0 | 25410 | 0 | 0 |
| `turaca.1` | Cultivate new cultures of wheat (harvesting +40%) | 1 | 40 | 15.62 | 0 | 200 | 0 | 325 | 0 | 0 |
| `turaca.10` | Raise builders' salary (building construction time -75%) | 1 | -7500000 | 15.62 | 0 | 0 | 0 | 6950 | 0 | 0 |
| `turaca.11` | Research new fortification grades (durability of walls and towers +80) | 1 | 80 | 15.62 | 0 | 16200 | 0 | 1500 | 0 | 0 |
| `turaca.12` | Improve firearms: rifled barrel (fire power +10%) | 1 | 10 | 15.62 | 0 | 0 | 0 | 0 | 5000 | 0 |
| `turaca.13` | Research granular gunpowder (fire power +10%) | 1 | 10 | 15.62 | 0 | 0 | 0 | 4000 | 0 | 0 |
| `turaca.14` | Research new sulphur purification methods (fire power +15%) | 1 | 15 | 15.62 | 0 | 0 | 0 | 7000 | 0 | 0 |
| `turaca.15` | Research new nitre purification methods (fire power +25%) | 1 | 25 | 15.62 | 0 | 0 | 0 | 0 | 0 | 11000 |
| `turaca.16` | Research improved additions to gunpowder formula (artillery range +5%) | 1 | 5 | 15.62 | 0 | 0 | 0 | 2000 | 0 | 0 |
| `turaca.17` | Design new barrel types: unicorn, carronade (artillery range +10%) | 1 | 10 | 15.62 | 0 | 0 | 3000 | 4550 | 0 | 0 |
| `turaca.18` | Design more durable gun carriage: Gribovalle system (artillery durability +50%) | 1 | 50 | 15.62 | 0 | 0 | 0 | 500 | 3830 | 1500 |
| `turaca.19` | %color(FFAA00)%Design multi-barrelled cannon | — | — | — | — | — | — | — | — | — |
| `turaca.2` | Cultivate new cultures of rye (harvesting +50%) | 1 | 50 | 15.62 | 0 | 400 | 0 | 522 | 0 | 0 |
| `turaca.20` | Research new sighting devices for artillery (artillery accuracy +35%) | 1 | -35 | 15.62 | 0 | 3540 | 0 | 2000 | 0 | 7250 |
| `turaca.21` | Finance artillery repair shops (repair all artillery) | 1 | 25 | 15.62 | 0 | 350 | 0 | 100 | 0 | 250 |
| `turaca.22` | Develop geology (previously hidden deposits appear on the map) | 1 | 0 | 15.62 | 0 | 0 | 0 | 250 | 0 | 0 |
| `turaca.23` | Develop mining (stone excavation efficiency +100%) | 1 | 100 | 15.62 | 0 | 0 | 0 | 1550 | 3000 | 0 |
| `turaca.24` | Raise miners' salary (stone excavation efficiency +200%) | 1 | 200 | 15.62 | 4200 | 0 | 0 | 1550 | 0 | 12520 |
| `turaca.25` | Design Montgolfier %color(FFAA00)%(reveals the whole map) | — | — | — | — | — | — | — | — | — |
| `turaca.26` | Develop medical science (heals all live units) | 1 | 50 | 31.25 | 0 | 0 | 0 | 200 | 0 | 200 |
| `turaca.27` | Develop mathematics (artillery accuracy +35%) | 1 | -35 | 15.62 | 0 | 9540 | 0 | 12000 | 0 | 65200 |
| `turaca.28` | Design new rigging types (ship speed +40%) | 1 | 40 | 15.62 | 0 | 0 | 0 | 1900 | 0 | 0 |
| `turaca.29` | Design new rib system and new hulls (battleship construction) | 1 | 0 | 15.62 | 0 | 32300 | 0 | 6800 | 9000 | 12800 |
| `turaca.3` | Raise agriculturists' salary (harvesting +50%) | 1 | 50 | 15.62 | 0 | 2400 | 0 | 850 | 0 | 0 |
| `turaca.30` | Train carpenters (shipbuilding speed x10) | 1 | -5000000 | 15.62 | 0 | 0 | 42700 | 0 | 0 | 0 |
| `turaca.31` | Design wheellock (rate of fire +30%) | 1 | -30 | 15.62 | 0 | 0 | 6000 | 5500 | 4200 | 0 |
| `turaca.32` | Design flintlock %color(FFAA00)%(musket cost -50%) | — | — | — | — | — | — | — | — | — |
| `turaca.33` | Design paper cartridge and iron ramrod (rate of fire +30%) | 1 | -30 | 15.62 | 0 | 5000 | 0 | 5500 | 0 | 15200 |
| `turaca.34` | Research improved steel grades for cuirasses (armoured soldier defence +2) | 1 | 2 | 15.62 | 0 | 0 | 0 | 6950 | 0 | 0 |
| `turaca.35` | Design bayonet: barrel-inserted, bayonet with a tube %color(FFAA00)%(cold steel weapons +5) | — | — | — | — | — | — | — | — | — |
| `turaca.36` | Research new steel grades %color(FFAA00)%(18c musketeer/grenadier melee attack efficiency +25%) | — | — | — | — | — | — | — | — | — |
| `turaca.4` | Carry out field melioration (field capacity +200%) | 1 | 200 | 15.62 | 0 | 1000 | 0 | 475 | 0 | 0 |
| `turaca.5` | Design new tackle and fishing nets (boat efficiency +100%) | 1 | 100 | 15.62 | 0 | 12400 | 0 | 2520 | 0 | 0 |
| `turaca.6` | Develop new woodworking methods (xebec building) | 1 | 0 | 15.62 | 0 | 9500 | 0 | 7040 | 0 | 0 |
| `turaca.7` | Build new shipyards for fishing boats (fishing boat cost -85%) | 1 | 0 | 15.62 | 0 | 7300 | 0 | 1220 | 0 | 0 |
| `turaca.8` | Design new woodworking tools (woodcutting efficiency +100%) | 1 | 100 | 15.62 | 5500 | 0 | 0 | 550 | 0 | 0 |
| `turaca.9` | Use new construction materials (durability of buildings +85) | 1 | 85 | 15.62 | 0 | 9400 | 0 | 1150 | 0 | 0 |
| `turart.cannon.1.1` | — | 2 | — | 10.0 | 0 | 1000 | 500 | 300 | 0 | 0 |
| `turart.cannon.1.2` | — | 3 | — | 10.0 | 0 | 3000 | 1000 | 500 | 0 | 0 |
| `turart.cannon.1.3` | — | 4 | — | 10.0 | 0 | 6000 | 2000 | 1000 | 0 | 0 |
| `turart.cannon.1.4` | — | 5 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `turart.cannon.1.5` | — | 6 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `turart.cannon.1.6` | — | 7 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `turart.cannon.2.1` | — | 2 | -2500000 | 10.0 | 0 | 0 | 0 | 950 | 1000 | 0 |
| `turart.cannon.2.2` | — | 3 | -2500000 | 10.0 | 0 | 0 | 0 | 150 | 2000 | 0 |
| `turart.cannon.2.3` | — | 4 | -2500000 | 10.0 | 0 | 0 | 0 | 250 | 3000 | 0 |
| `turart.cannon.2.4` | — | 5 | -2000000 | 15.62 | 2560 | 0 | 0 | 1350 | 0 | 0 |
| `turart.cannon.2.5` | — | 6 | -2000000 | 15.62 | 3560 | 0 | 0 | 2500 | 0 | 0 |
| `turart.cannon.2.6` | — | 7 | -2000000 | 15.62 | 5560 | 0 | 0 | 3350 | 0 | 0 |
| `turart.howitzer.1.1` | — | 2 | — | 10.0 | 0 | 1000 | 500 | 300 | 0 | 0 |
| `turart.howitzer.1.2` | — | 3 | — | 10.0 | 0 | 3000 | 1000 | 500 | 0 | 0 |
| `turart.howitzer.1.3` | — | 4 | — | 10.0 | 0 | 6000 | 2000 | 1000 | 0 | 0 |
| `turart.howitzer.1.4` | — | 5 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `turart.howitzer.1.5` | — | 6 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `turart.howitzer.1.6` | — | 7 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `turart.howitzer.2.1` | — | 2 | -2500000 | 10.0 | 0 | 0 | 0 | 350 | 1000 | 0 |
| `turart.howitzer.2.2` | — | 3 | -2500000 | 10.0 | 0 | 0 | 0 | 450 | 2000 | 0 |
| `turart.howitzer.2.3` | — | 4 | -2500000 | 10.0 | 0 | 0 | 0 | 550 | 3000 | 0 |
| `turart.howitzer.2.4` | — | 5 | -2000000 | 31.25 | 2560 | 0 | 0 | 1150 | 0 | 0 |
| `turart.howitzer.2.5` | — | 6 | -2000000 | 31.25 | 3560 | 0 | 0 | 3200 | 0 | 0 |
| `turart.howitzer.2.6` | — | 7 | -2000000 | 31.25 | 5560 | 0 | 0 | 4500 | 0 | 0 |
| `turbar.archertur.1.1` | Barracks 17c archertur damage +2 (lvl 2) | 2 | 2 | 15.62 | 700 | 0 | 0 | 250 | 0 | 0 |
| `turbar.archertur.1.2` | Barracks 17c archertur damage +2 (lvl 3) | 3 | 2 | 15.62 | 500 | 0 | 0 | 200 | 0 | 0 |
| `turbar.archertur.1.3` | Barracks 17c archertur damage +2 (lvl 4) | 4 | 2 | 15.62 | 700 | 0 | 0 | 240 | 0 | 0 |
| `turbar.archertur.1.4` | Barracks 17c archertur damage +3 (lvl 5) | 5 | 3 | 15.62 | 1200 | 0 | 0 | 900 | 0 | 0 |
| `turbar.archertur.1.5` | Barracks 17c archertur damage +3 (lvl 6) | 6 | 3 | 15.62 | 1800 | 0 | 0 | 800 | 0 | 0 |
| `turbar.archertur.1.6` | Barracks 17c archertur damage +3 (lvl 7) | 7 | 3 | 15.62 | 850 | 0 | 0 | 650 | 0 | 0 |
| `turbar.archertur.2.1` | Barracks 17c archertur protection +1 (lvl 2) | 2 | 1 | 15.62 | 900 | 0 | 0 | 250 | 0 | 0 |
| `turbar.archertur.2.2` | Barracks 17c archertur protection +2 (lvl 3) | 3 | 2 | 15.62 | 6200 | 0 | 0 | 1150 | 0 | 0 |
| `turbar.archertur.2.3` | Barracks 17c archertur protection +2 (lvl 4) | 4 | 2 | 15.62 | 5400 | 0 | 0 | 2150 | 0 | 0 |
| `turbar.archertur.2.4` | Barracks 17c archertur protection +1 (lvl 5) | 5 | 1 | 15.62 | 2000 | 0 | 0 | 1200 | 0 | 0 |
| `turbar.archertur.2.5` | Barracks 17c archertur protection +2 (lvl 6) | 6 | 2 | 15.62 | 3000 | 0 | 0 | 4250 | 0 | 0 |
| `turbar.archertur.2.6` | Barracks 17c archertur protection +2 (lvl 7) | 7 | 2 | 15.62 | 5001 | 0 | 0 | 8101 | 0 | 0 |
| `turbar.drummertur.2.1` | Barracks 17c drummertur protection +10 (lvl 2) | 2 | 10 | 15.62 | 706 | 0 | 0 | 50 | 0 | 0 |
| `turbar.jannisary.1.1` | Barracks 17c jannisary damage +1 (lvl 2) | 2 | 1 | 15.62 | 2000 | 0 | 0 | 100 | 0 | 0 |
| `turbar.jannisary.1.2` | Barracks 17c jannisary damage +1 (lvl 3) | 3 | 1 | 15.62 | 1000 | 0 | 0 | 300 | 0 | 0 |
| `turbar.jannisary.1.3` | Barracks 17c jannisary damage +2 (lvl 4) | 4 | 2 | 15.62 | 500 | 0 | 0 | 700 | 0 | 0 |
| `turbar.jannisary.1.4` | — | 5 | 1 | 15.62 | 5000 | 0 | 0 | 1600 | 0 | 0 |
| `turbar.jannisary.1.5` | — | 6 | 2 | 15.62 | 7500 | 0 | 0 | 3200 | 0 | 0 |
| `turbar.jannisary.1.6` | — | 7 | 3 | 15.62 | 10000 | 0 | 0 | 4800 | 0 | 0 |
| `turbar.jannisary.2.1` | Barracks 17c jannisary protection +1 (lvl 2) | 2 | 1 | 15.62 | 170 | 0 | 0 | 50 | 100 | 0 |
| `turbar.jannisary.2.2` | Barracks 17c jannisary protection +2 (lvl 3) | 3 | 2 | 15.62 | 405 | 0 | 0 | 150 | 200 | 0 |
| `turbar.jannisary.2.3` | Barracks 17c jannisary protection +2 (lvl 4) | 4 | 2 | 15.62 | 1570 | 0 | 0 | 100 | 350 | 0 |
| `turbar.jannisary.2.4` | Barracks 17c jannisary protection +1 (lvl 5) | 5 | 1 | 15.62 | 1556 | 0 | 0 | 550 | 100 | 0 |
| `turbar.jannisary.2.5` | Barracks 17c jannisary protection +2 (lvl 6) | 6 | 2 | 15.62 | 1060 | 0 | 0 | 850 | 400 | 0 |
| `turbar.jannisary.2.6` | Barracks 17c jannisary protection +2 (lvl 7) | 7 | 2 | 15.62 | 4700 | 0 | 0 | 450 | 700 | 0 |
| `turbar.lightinfantry.1.1` | Barracks 17c lightinfantry damage +1 (lvl 2) | 2 | 1 | 15.62 | 100 | 0 | 0 | 50 | 0 | 0 |
| `turbar.lightinfantry.1.2` | Barracks 17c lightinfantry damage +1 (lvl 3) | 3 | 1 | 15.62 | 1100 | 0 | 0 | 200 | 0 | 0 |
| `turbar.lightinfantry.1.3` | Barracks 17c lightinfantry damage +11300 (lvl 4) | 4 | 11300 | 15.62 | 325 | 0 | 0 | 0 | 0 | 0 |
| `turbar.lightinfantry.1.4` | — | 5 | 1 | 15.62 | 3000 | 0 | 0 | 360 | 0 | 0 |
| `turbar.lightinfantry.1.5` | — | 6 | 1 | 15.62 | 4500 | 0 | 0 | 540 | 0 | 0 |
| `turbar.lightinfantry.1.6` | — | 7 | 2 | 15.62 | 9375 | 0 | 0 | 1125 | 0 | 0 |
| `turbar.lightinfantry.2.1` | Barracks 17c lightinfantry protection +1 (lvl 2) | 2 | 1 | 15.62 | 200 | 0 | 0 | 70 | 120 | 0 |
| `turbar.lightinfantry.2.2` | Barracks 17c lightinfantry protection +1 (lvl 3) | 3 | 1 | 15.62 | 6360 | 0 | 0 | 150 | 320 | 0 |
| `turbar.lightinfantry.2.3` | Barracks 17c lightinfantry protection +2 (lvl 4) | 4 | 2 | 15.62 | 506 | 0 | 0 | 250 | 420 | 0 |
| `turbar.lightinfantry.2.4` | — | 5 | 1 | 15.62 | 3600 | 0 | 0 | 600 | 0 | 0 |
| `turbar.lightinfantry.2.5` | — | 6 | 1 | 15.62 | 5400 | 0 | 0 | 900 | 0 | 0 |
| `turbar.lightinfantry.2.6` | — | 7 | 2 | 15.62 | 11250 | 0 | 0 | 1875 | 0 | 0 |
| `turbar.officertur.1.1` | Barracks 17c officertur damage +20 (lvl 2) | 2 | 20 | 15.62 | 1000 | 0 | 0 | 800 | 0 | 0 |
| `turbar.officertur.2.1` | Barracks 17c officertur protection +10 (lvl 2) | 2 | 10 | 15.62 | 1706 | 0 | 0 | 350 | 0 | 0 |
| `turbar.pikemantur.1.1` | Barracks 17c pikemantur damage +2 (lvl 2) | 2 | 2 | 15.62 | 200 | 0 | 0 | 50 | 0 | 0 |
| `turbar.pikemantur.1.2` | Barracks 17c pikemantur damage +2 (lvl 3) | 3 | 2 | 15.62 | 600 | 0 | 0 | 300 | 0 | 0 |
| `turbar.pikemantur.1.3` | Barracks 17c pikemantur damage +2 (lvl 4) | 4 | 2 | 15.62 | 1200 | 0 | 0 | 450 | 0 | 0 |
| `turbar.pikemantur.1.4` | Barracks 17c pikemantur damage +2 (lvl 5) | 5 | 2 | 15.62 | 2200 | 0 | 0 | 1850 | 0 | 0 |
| `turbar.pikemantur.1.5` | Barracks 17c pikemantur damage +2 (lvl 6) | 6 | 2 | 15.62 | 16030 | 0 | 0 | 2000 | 0 | 0 |
| `turbar.pikemantur.1.6` | — | 7 | 2 | 15.62 | 18750 | 0 | 0 | 2350 | 0 | 0 |
| `turbar.pikemantur.2.1` | Barracks 17c pikemantur protection +1 (lvl 2) | 2 | 1 | 15.62 | 150 | 0 | 0 | 50 | 0 | 0 |
| `turbar.pikemantur.2.2` | Barracks 17c pikemantur protection +2 (lvl 3) | 3 | 2 | 15.62 | 900 | 0 | 0 | 175 | 0 | 0 |
| `turbar.pikemantur.2.3` | Barracks 17c pikemantur protection +3 (lvl 4) | 4 | 3 | 15.62 | 4500 | 0 | 0 | 300 | 0 | 0 |
| `turbar.pikemantur.2.4` | Barracks 17c pikemantur protection +1 (lvl 5) | 5 | 1 | 15.62 | 9005 | 0 | 0 | 507 | 0 | 0 |
| `turbar.pikemantur.2.5` | Barracks 17c pikemantur protection +2 (lvl 6) | 6 | 2 | 15.62 | 18010 | 0 | 0 | 3050 | 0 | 0 |
| `turbar.pikemantur.2.6` | — | 7 | 3 | 15.62 | 16875 | 0 | 0 | 2250 | 0 | 0 |
| `turbla.1` | Manufacture agricultural equipment (field capacity +100%) | 1 | 100 | 15.62 | 0 | 400 | 0 | 90 | 0 | 0 |
| `turbla.2` | Forge metal armature and gratings (building defence +50) | 1 | 50 | 15.62 | 0 | 0 | 12320 | 350 | 900 | 0 |
| `turbla.3` | Forge harnesses for horses (mounted units recruitment speed -33%) | 1 | -3333333 | 15.62 | 0 | 0 | 0 | 3650 | 5300 | 8200 |
| `turbla.4` | Forge bayonets and broadswords for infantry %color(FFAA00)%(18c musketeer/grenadier melee attack +5) | — | — | — | — | — | — | — | — | — |
| `turbla.5` | Forge new types of broadswords and sabres (cavalry and sword clansman attack +5) | 1 | 5 | 15.62 | 0 | 0 | 0 | 4000 | 7900 | 0 |
| `turbla.6` | Forge new cuirasses (armoured soldiers defence +2) | 1 | 2 | 15.62 | 0 | 0 | 0 | 4950 | 10200 | 0 |
| `turcen.1` | — | 1 | 0 | 9.38 | 30000 | 0 | 0 | 5000 | 2000 | 2000 |
| `turpor.1` | — | 1 | 50 | 46.88 | 0 | 20000 | 0 | 1500 | 0 | 0 |
| `tursta.1` | — | 1 | 140 | 15.62 | 600 | 0 | 0 | 250 | 0 | 0 |
| `tursta.sipahi.1.1` | Stable sipahi damage +1 (lvl 2) | 2 | 1 | 15.62 | 500 | 0 | 0 | 100 | 0 | 0 |
| `tursta.sipahi.1.2` | Stable sipahi damage +2 (lvl 3) | 3 | 2 | 15.62 | 900 | 0 | 0 | 220 | 0 | 0 |
| `tursta.sipahi.1.3` | Stable sipahi damage +1 (lvl 4) | 4 | 1 | 15.62 | 4400 | 0 | 0 | 280 | 0 | 0 |
| `tursta.sipahi.1.4` | Stable sipahi damage +1 (lvl 5) | 5 | 1 | 15.62 | 2250 | 0 | 0 | 320 | 0 | 0 |
| `tursta.sipahi.1.5` | Stable sipahi damage +1 (lvl 6) | 6 | 1 | 15.62 | 3030 | 0 | 0 | 600 | 0 | 0 |
| `tursta.sipahi.1.6` | Stable sipahi damage +1 (lvl 7) | 7 | 1 | 15.62 | 7000 | 0 | 0 | 1800 | 0 | 0 |
| `tursta.sipahi.2.1` | Stable sipahi protection +1 (lvl 2) | 2 | 1 | 15.62 | 200 | 0 | 0 | 135 | 300 | 0 |
| `tursta.sipahi.2.2` | Stable sipahi protection +2 (lvl 3) | 3 | 2 | 15.62 | 600 | 0 | 0 | 100 | 400 | 0 |
| `tursta.sipahi.2.3` | Stable sipahi protection +2 (lvl 4) | 4 | 2 | 15.62 | 800 | 0 | 0 | 200 | 560 | 0 |
| `tursta.sipahi.2.4` | Stable sipahi protection +2 (lvl 5) | 5 | 2 | 15.62 | 1600 | 0 | 0 | 300 | 640 | 0 |
| `tursta.sipahi.2.5` | Stable sipahi protection +2 (lvl 6) | 6 | 2 | 15.62 | 3200 | 0 | 0 | 350 | 300 | 0 |
| `tursta.sipahi.2.6` | Stable sipahi protection +3 (lvl 7) | 7 | 3 | 15.62 | 16000 | 0 | 0 | 1000 | 5000 | 0 |
| `tursta.spakh.2.1` | Stable spakh protection +1 (lvl 2) | 2 | 1 | 15.62 | 200 | 0 | 0 | 135 | 1000 | 0 |
| `tursta.spakh.2.2` | Stable spakh protection +1 (lvl 3) | 3 | 1 | 15.62 | 2000 | 0 | 0 | 100 | 1000 | 0 |
| `tursta.spakh.2.3` | Stable spakh protection +2 (lvl 4) | 4 | 2 | 15.62 | 40000 | 0 | 0 | 200 | 4000 | 0 |
| `tursta.spakh.2.4` | Stable spakh protection +3 (lvl 5) | 5 | 3 | 15.62 | 40000 | 0 | 0 | 300 | 6000 | 0 |
| `tursta.spakh.2.5` | Stable spakh protection +2 (lvl 6) | 6 | 2 | 15.62 | 40000 | 0 | 0 | 350 | 8000 | 0 |
| `tursta.spakh.2.6` | Stable spakh protection +1 (lvl 7) | 7 | 1 | 15.62 | 40000 | 0 | 0 | 1000 | 10000 | 0 |
| `tursta.tatar.1.1` | Stable tatar damage +2 (lvl 2) | 2 | 2 | 15.62 | 700 | 0 | 0 | 250 | 0 | 0 |
| `tursta.tatar.1.2` | Stable tatar damage +2 (lvl 3) | 3 | 2 | 15.62 | 500 | 0 | 0 | 200 | 0 | 0 |
| `tursta.tatar.1.3` | Stable tatar damage +2 (lvl 4) | 4 | 2 | 15.62 | 700 | 0 | 0 | 240 | 0 | 0 |
| `tursta.tatar.1.4` | Stable tatar damage +3 (lvl 5) | 5 | 3 | 15.62 | 1200 | 0 | 0 | 900 | 0 | 0 |
| `tursta.tatar.1.5` | Stable tatar damage +3 (lvl 6) | 6 | 3 | 15.62 | 1800 | 0 | 0 | 800 | 0 | 0 |
| `tursta.tatar.1.6` | Stable tatar damage +3 (lvl 7) | 7 | 3 | 15.62 | 850 | 0 | 0 | 650 | 0 | 0 |
| `tursta.tatar.2.1` | Stable tatar protection +1 (lvl 2) | 2 | 1 | 15.62 | 900 | 0 | 0 | 250 | 0 | 0 |
| `tursta.tatar.2.2` | Stable tatar protection +1 (lvl 3) | 3 | 1 | 15.62 | 6200 | 0 | 0 | 1150 | 0 | 0 |
| `tursta.tatar.2.3` | Stable tatar protection +2 (lvl 4) | 4 | 2 | 15.62 | 5400 | 0 | 0 | 2150 | 0 | 0 |
| `tursta.tatar.2.4` | Stable tatar protection +1 (lvl 5) | 5 | 1 | 15.62 | 2000 | 0 | 0 | 1200 | 0 | 0 |
| `tursta.tatar.2.5` | Stable tatar protection +1 (lvl 6) | 6 | 1 | 15.62 | 3000 | 0 | 0 | 4250 | 0 | 0 |
| `tursta.tatar.2.6` | Stable tatar protection +2 (lvl 7) | 7 | 2 | 15.62 | 5001 | 0 | 0 | 8101 | 0 | 0 |
| `turswa.1` | — | 2 | 5 | 0.03 | 0 | 0 | 500 | 0 | 0 | 0 |
| `turtow.1` | — | 2 | -20 | 31.25 | 0 | 0 | 0 | 250 | 0 | 0 |
| `turtow.2` | — | 3 | -20 | 31.25 | 0 | 0 | 0 | 0 | 350 | 0 |
| `turtow.3` | — | 4 | -10 | 31.25 | 0 | 0 | 0 | 0 | 0 | 400 |
| `turtow.4` | — | 5 | -10 | 31.25 | 0 | 0 | 0 | 0 | 450 | 0 |
| `turtow.5` | — | 6 | -10 | 31.25 | 0 | 0 | 0 | 0 | 0 | 500 |
| `ukrwwa.1` | — | 2 | 5 | 0.03 | 0 | 400 | 0 | 0 | 0 | 0 |

### alg — Algeria

| sid | имя (EN) | level | value | время (s) | F | W | S | G | I | C |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `algaca.1` | Cultivate new cultures of wheat (harvesting +40%) | 1 | 40 | 15.62 | 0 | 200 | 0 | 325 | 0 | 0 |
| `algaca.10` | Raise builders' salary (building construction time -75%) | 1 | -7500000 | 15.62 | 0 | 0 | 0 | 6950 | 0 | 0 |
| `algaca.11` | Research new fortification grades (durability of walls and towers +80) | 1 | 80 | 15.62 | 0 | 16200 | 0 | 1500 | 0 | 0 |
| `algaca.12` | Improve firearms: rifled barrel %color(FFAA00)%(fire power +10%) | — | — | — | — | — | — | — | — | — |
| `algaca.13` | Research granular gunpowder %color(FFAA00)%(fire power +10%) | — | — | — | — | — | — | — | — | — |
| `algaca.14` | Research new sulphur purification methods %color(FFAA00)%(fire power +15%) | — | — | — | — | — | — | — | — | — |
| `algaca.15` | Research new nitre purification methods %color(FFAA00)%(fire power +25%) | — | — | — | — | — | — | — | — | — |
| `algaca.16` | Research improved additions to gunpowder formula (artillery range +5%) | 1 | 5 | 15.62 | 0 | 0 | 0 | 2000 | 0 | 0 |
| `algaca.17` | Design new barrel types: unicorn, carronade (artillery range +10%) | 1 | 10 | 15.62 | 0 | 0 | 3000 | 4550 | 0 | 0 |
| `algaca.18` | Design more durable gun carriage: Gribovalle system (artillery durability +50%) | 1 | 50 | 15.62 | 0 | 0 | 0 | 500 | 3830 | 1500 |
| `algaca.19` | %color(FFAA00)%Design multi-barrelled cannon | — | — | — | — | — | — | — | — | — |
| `algaca.2` | Cultivate new cultures of rye (harvesting +50%) | 1 | 50 | 15.62 | 0 | 400 | 0 | 522 | 0 | 0 |
| `algaca.20` | Research new sighting devices for artillery (artillery accuracy +35%) | 1 | -35 | 15.62 | 0 | 3540 | 0 | 2000 | 0 | 7250 |
| `algaca.21` | Finance artillery repair shops (repair all artillery) | 1 | 25 | 15.62 | 0 | 350 | 0 | 100 | 0 | 250 |
| `algaca.22` | Develop geology (previously hidden deposits appear on the map) | 1 | 0 | 15.62 | 0 | 0 | 0 | 250 | 0 | 0 |
| `algaca.23` | Develop mining (stone excavation efficiency +100%) | 1 | 100 | 15.62 | 0 | 0 | 0 | 1550 | 3000 | 0 |
| `algaca.24` | Raise miners' salary (stone excavation efficiency +200%) | 1 | 200 | 15.62 | 4200 | 0 | 0 | 1550 | 0 | 12520 |
| `algaca.25` | Design Montgolfier %color(FFAA00)%(reveals the whole map) | — | — | — | — | — | — | — | — | — |
| `algaca.26` | Develop medical science (heals all live units) | 1 | 50 | 31.25 | 0 | 0 | 0 | 200 | 0 | 200 |
| `algaca.27` | Develop mathematics (artillery accuracy +35%) | 1 | -35 | 15.62 | 0 | 9540 | 0 | 12000 | 0 | 65200 |
| `algaca.28` | Design new rigging types (ship speed +40%) | 1 | 40 | 15.62 | 0 | 0 | 0 | 1900 | 0 | 0 |
| `algaca.29` | Design new rib system and new hulls (battleship construction) | 1 | 0 | 15.62 | 0 | 32300 | 0 | 6800 | 9000 | 12800 |
| `algaca.3` | Raise agriculturists' salary (harvesting +50%) | 1 | 50 | 15.62 | 0 | 1240 | 0 | 850 | 0 | 0 |
| `algaca.30` | Train carpenters (shipbuilding speed x10) | 1 | -5000000 | 15.62 | 0 | 0 | 42700 | 0 | 0 | 0 |
| `algaca.31` | Design wheellock %color(FFAA00)%(rate of fire +30%) | — | — | — | — | — | — | — | — | — |
| `algaca.32` | Design flintlock %color(FFAA00)%(musket cost -50%) | — | — | — | — | — | — | — | — | — |
| `algaca.33` | Design paper cartridge and iron ramrod %color(FFAA00)%(rate of fire +30%) | — | — | — | — | — | — | — | — | — |
| `algaca.34` | Research improved steel grades for cuirasses %color(FFAA00)%(armoured soldier defence +2) | — | — | — | — | — | — | — | — | — |
| `algaca.35` | Design bayonet: barrel-inserted, bayonet with a tube %color(FFAA00)%(cold steel weapons +5) | — | — | — | — | — | — | — | — | — |
| `algaca.36` | Research new steel grades %color(FFAA00)%(18c musketeer/grenadier melee attack efficiency +25%) | — | — | — | — | — | — | — | — | — |
| `algaca.4` | Carry out field melioration (field capacity +200%) | 1 | 200 | 15.62 | 0 | 700 | 0 | 475 | 0 | 0 |
| `algaca.5` | Design new tackle and fishing nets (boat efficiency +100%) | 1 | 100 | 15.62 | 0 | 12400 | 0 | 2520 | 0 | 0 |
| `algaca.6` | Develop new woodworking methods (xebec building) | 1 | 0 | 15.62 | 0 | 9500 | 0 | 7040 | 0 | 0 |
| `algaca.7` | Build new shipyards for fishing boats (fishing boat cost -85%) | 1 | 0 | 15.62 | 0 | 7300 | 0 | 1220 | 0 | 0 |
| `algaca.8` | Design new woodworking tools (woodcutting efficiency +100%) | 1 | 100 | 15.62 | 5500 | 0 | 0 | 550 | 0 | 0 |
| `algaca.9` | Use new construction materials (durability of buildings +85) | 1 | 85 | 15.62 | 0 | 9400 | 0 | 1150 | 0 | 0 |
| `algart.cannon.1.1` | — | 2 | — | 10.0 | 0 | 1000 | 500 | 300 | 0 | 0 |
| `algart.cannon.1.2` | — | 3 | — | 10.0 | 0 | 3000 | 1000 | 500 | 0 | 0 |
| `algart.cannon.1.3` | — | 4 | — | 10.0 | 0 | 6000 | 2000 | 1000 | 0 | 0 |
| `algart.cannon.1.4` | — | 5 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `algart.cannon.1.5` | — | 6 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `algart.cannon.1.6` | — | 7 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `algart.cannon.2.1` | — | 2 | -2500000 | 10.0 | 0 | 0 | 0 | 950 | 1000 | 0 |
| `algart.cannon.2.2` | — | 3 | -2500000 | 10.0 | 0 | 0 | 0 | 150 | 2000 | 0 |
| `algart.cannon.2.3` | — | 4 | -2500000 | 10.0 | 0 | 0 | 0 | 250 | 3000 | 0 |
| `algart.cannon.2.4` | — | 5 | -2000000 | 15.62 | 2560 | 0 | 0 | 1350 | 0 | 0 |
| `algart.cannon.2.5` | — | 6 | -2000000 | 15.62 | 3560 | 0 | 0 | 2500 | 0 | 0 |
| `algart.cannon.2.6` | — | 7 | -2000000 | 15.62 | 5560 | 0 | 0 | 3350 | 0 | 0 |
| `algart.howitzer.1.1` | — | 2 | — | 10.0 | 0 | 1000 | 500 | 300 | 0 | 0 |
| `algart.howitzer.1.2` | — | 3 | — | 10.0 | 0 | 3000 | 1000 | 500 | 0 | 0 |
| `algart.howitzer.1.3` | — | 4 | — | 10.0 | 0 | 6000 | 2000 | 1000 | 0 | 0 |
| `algart.howitzer.1.4` | — | 5 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `algart.howitzer.1.5` | — | 6 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `algart.howitzer.1.6` | — | 7 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `algart.howitzer.2.1` | — | 2 | -2500000 | 10.0 | 0 | 0 | 0 | 350 | 1000 | 0 |
| `algart.howitzer.2.2` | — | 3 | -2500000 | 10.0 | 0 | 0 | 0 | 450 | 2000 | 0 |
| `algart.howitzer.2.3` | — | 4 | -2500000 | 10.0 | 0 | 0 | 0 | 550 | 3000 | 0 |
| `algart.howitzer.2.4` | — | 5 | -2000000 | 31.25 | 2560 | 0 | 0 | 1150 | 0 | 0 |
| `algart.howitzer.2.5` | — | 6 | -2000000 | 31.25 | 3560 | 0 | 0 | 3200 | 0 | 0 |
| `algart.howitzer.2.6` | — | 7 | -2000000 | 31.25 | 5560 | 0 | 0 | 4500 | 0 | 0 |
| `algbar.1` | — | 1 | 140 | 15.62 | 600 | 0 | 0 | 250 | 0 | 0 |
| `algbar.archer.1.1` | Barracks 17c archer damage +2 (lvl 2) | 2 | 2 | 15.62 | 700 | 0 | 0 | 250 | 0 | 0 |
| `algbar.archer.1.2` | Barracks 17c archer damage +2 (lvl 3) | 3 | 2 | 15.62 | 500 | 0 | 0 | 200 | 0 | 0 |
| `algbar.archer.1.3` | Barracks 17c archer damage +2 (lvl 4) | 4 | 2 | 15.62 | 700 | 0 | 0 | 240 | 0 | 0 |
| `algbar.archer.1.4` | Barracks 17c archer damage +3 (lvl 5) | 5 | 3 | 15.62 | 1200 | 0 | 0 | 900 | 0 | 0 |
| `algbar.archer.1.5` | Barracks 17c archer damage +3 (lvl 6) | 6 | 3 | 15.62 | 1800 | 0 | 0 | 800 | 0 | 0 |
| `algbar.archer.1.6` | Barracks 17c archer damage +3 (lvl 7) | 7 | 3 | 15.62 | 850 | 0 | 0 | 650 | 0 | 0 |
| `algbar.archer.2.1` | Barracks 17c archer protection +1 (lvl 2) | 2 | 1 | 15.62 | 900 | 0 | 0 | 250 | 0 | 0 |
| `algbar.archer.2.2` | Barracks 17c archer protection +1 (lvl 3) | 3 | 1 | 15.62 | 2200 | 0 | 0 | 550 | 0 | 0 |
| `algbar.archer.2.3` | Barracks 17c archer protection +2 (lvl 4) | 4 | 2 | 15.62 | 3400 | 0 | 0 | 850 | 0 | 0 |
| `algbar.archer.2.4` | Barracks 17c archer protection +1 (lvl 5) | 5 | 1 | 15.62 | 2000 | 0 | 0 | 400 | 0 | 0 |
| `algbar.archer.2.5` | Barracks 17c archer protection +1 (lvl 6) | 6 | 1 | 15.62 | 3000 | 0 | 0 | 850 | 0 | 0 |
| `algbar.archer.2.6` | Barracks 17c archer protection +2 (lvl 7) | 7 | 2 | 15.62 | 4000 | 0 | 0 | 1200 | 0 | 0 |
| `algbar.drummertur.2.1` | Barracks 17c drummertur protection +10 (lvl 2) | 2 | 10 | 15.62 | 706 | 0 | 0 | 50 | 0 | 0 |
| `algbar.lightinfantry.1.1` | Barracks 17c lightinfantry damage +1 (lvl 2) | 2 | 1 | 15.62 | 100 | 0 | 0 | 50 | 0 | 0 |
| `algbar.lightinfantry.1.2` | Barracks 17c lightinfantry damage +1 (lvl 3) | 3 | 1 | 15.62 | 1100 | 0 | 0 | 200 | 0 | 0 |
| `algbar.lightinfantry.1.3` | Barracks 17c lightinfantry damage +1 (lvl 4) | 4 | 1 | 15.62 | 1300 | 0 | 0 | 325 | 0 | 0 |
| `algbar.lightinfantry.1.4` | — | 5 | 2 | 15.62 | 3000 | 0 | 0 | 360 | 0 | 0 |
| `algbar.lightinfantry.1.5` | — | 6 | 2 | 15.62 | 4500 | 0 | 0 | 540 | 0 | 0 |
| `algbar.lightinfantry.1.6` | — | 7 | 3 | 15.62 | 9375 | 0 | 0 | 1125 | 0 | 0 |
| `algbar.lightinfantry.2.1` | Barracks 17c lightinfantry protection +1 (lvl 2) | 2 | 1 | 15.62 | 200 | 0 | 0 | 70 | 120 | 0 |
| `algbar.lightinfantry.2.2` | Barracks 17c lightinfantry protection +1 (lvl 3) | 3 | 1 | 15.62 | 6360 | 0 | 0 | 150 | 320 | 0 |
| `algbar.lightinfantry.2.3` | Barracks 17c lightinfantry protection +2 (lvl 4) | 4 | 2 | 15.62 | 506 | 0 | 0 | 250 | 420 | 0 |
| `algbar.lightinfantry.2.4` | — | 5 | 1 | 15.62 | 3600 | 0 | 0 | 600 | 0 | 0 |
| `algbar.lightinfantry.2.5` | — | 6 | 1 | 15.62 | 5400 | 0 | 0 | 900 | 0 | 0 |
| `algbar.lightinfantry.2.6` | — | 7 | 2 | 15.62 | 11250 | 0 | 0 | 1875 | 0 | 0 |
| `algbar.officertur.1.1` | Barracks 17c officertur damage +20 (lvl 2) | 2 | 20 | 15.62 | 1000 | 0 | 0 | 800 | 0 | 0 |
| `algbar.officertur.2.1` | Barracks 17c officertur protection +10 (lvl 2) | 2 | 10 | 15.62 | 1706 | 0 | 0 | 350 | 0 | 0 |
| `algbar.pikemantur.1.1` | Barracks 17c pikemantur damage +2 (lvl 2) | 2 | 2 | 15.62 | 200 | 0 | 0 | 50 | 0 | 0 |
| `algbar.pikemantur.1.2` | Barracks 17c pikemantur damage +2 (lvl 3) | 3 | 2 | 15.62 | 600 | 0 | 0 | 300 | 0 | 0 |
| `algbar.pikemantur.1.3` | Barracks 17c pikemantur damage +2 (lvl 4) | 4 | 2 | 15.62 | 1200 | 0 | 0 | 450 | 0 | 0 |
| `algbar.pikemantur.1.4` | Barracks 17c pikemantur damage +2 (lvl 5) | 5 | 2 | 15.62 | 2200 | 0 | 0 | 1850 | 0 | 0 |
| `algbar.pikemantur.1.5` | Barracks 17c pikemantur damage +2 (lvl 6) | 6 | 2 | 15.62 | 16030 | 0 | 0 | 2000 | 0 | 0 |
| `algbar.pikemantur.1.6` | — | 7 | 2 | 15.62 | 18750 | 0 | 0 | 2350 | 0 | 0 |
| `algbar.pikemantur.2.1` | Barracks 17c pikemantur protection +1 (lvl 2) | 2 | 1 | 15.62 | 150 | 0 | 0 | 50 | 0 | 0 |
| `algbar.pikemantur.2.2` | Barracks 17c pikemantur protection +2 (lvl 3) | 3 | 2 | 15.62 | 900 | 0 | 0 | 175 | 0 | 0 |
| `algbar.pikemantur.2.3` | Barracks 17c pikemantur protection +3 (lvl 4) | 4 | 3 | 15.62 | 4500 | 0 | 0 | 300 | 0 | 0 |
| `algbar.pikemantur.2.4` | Barracks 17c pikemantur protection +1 (lvl 5) | 5 | 1 | 15.62 | 9005 | 0 | 0 | 507 | 0 | 0 |
| `algbar.pikemantur.2.5` | Barracks 17c pikemantur protection +2 (lvl 6) | 6 | 2 | 15.62 | 18010 | 0 | 0 | 3050 | 0 | 0 |
| `algbar.pikemantur.2.6` | — | 7 | 3 | 15.62 | 16875 | 0 | 0 | 2250 | 0 | 0 |
| `algbla.1` | Manufacture agricultural equipment (field capacity +100%) | 1 | 100 | 15.62 | 0 | 400 | 0 | 90 | 0 | 0 |
| `algbla.2` | Forge metal armature and gratings (building defence +50) | 1 | 50 | 15.62 | 0 | 0 | 12320 | 350 | 900 | 0 |
| `algbla.3` | Forge harnesses for horses (mounted units recruitment speed -33%) | 1 | -3333333 | 15.62 | 0 | 0 | 0 | 3650 | 5300 | 8200 |
| `algbla.4` | Forge bayonets and broadswords for infantry %color(FFAA00)%(18c musketeer/grenadier melee attack +5) | — | — | — | — | — | — | — | — | — |
| `algbla.5` | Forge new types of broadswords and sabres (cavalry and sword clansman attack +5) | 1 | 5 | 15.62 | 0 | 0 | 0 | 4000 | 7900 | 0 |
| `algbla.6` | Forge new cuirasses %color(FFAA00)%(armoured soldiers defence +2) | — | — | — | — | — | — | — | — | — |
| `algcen.1` | — | 1 | 0 | 9.38 | 30000 | 0 | 0 | 5000 | 2000 | 2000 |
| `algsta.mameluke.2.1` | Stable mameluke protection +1 (lvl 2) | 2 | 1 | 15.62 | 200 | 0 | 0 | 135 | 1000 | 0 |
| `algsta.mameluke.2.2` | Stable mameluke protection +2 (lvl 3) | 3 | 2 | 15.62 | 2000 | 0 | 0 | 100 | 1000 | 0 |
| `algsta.mameluke.2.3` | Stable mameluke protection +3 (lvl 4) | 4 | 3 | 15.62 | 40000 | 0 | 0 | 200 | 4000 | 0 |
| `algsta.mameluke.2.4` | Stable mameluke protection +3 (lvl 5) | 5 | 3 | 15.62 | 40000 | 0 | 0 | 300 | 6000 | 0 |
| `algsta.mameluke.2.5` | Stable mameluke protection +2 (lvl 6) | 6 | 2 | 15.62 | 40000 | 0 | 0 | 350 | 8000 | 0 |
| `algsta.mameluke.2.6` | Stable mameluke protection +1 (lvl 7) | 7 | 1 | 15.62 | 40000 | 0 | 0 | 1000 | 10000 | 0 |
| `eurcoa.1` | — | 2 | 5 | 9.38 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `eurcoa.2` | — | 3 | 8 | 9.38 | 5250 | 0 | 0 | 4950 | 0 | 0 |
| `eurcoa.3` | — | 4 | 10 | 9.38 | 12500 | 0 | 0 | 9250 | 0 | 0 |
| `eurcoa.4` | — | 5 | 12 | 9.38 | 15800 | 0 | 0 | 18500 | 0 | 0 |
| `eurcoa.5` | — | 6 | 15 | 9.38 | 19800 | 0 | 0 | 21050 | 0 | 0 |
| `eurcoa.6` | — | 7 | 40 | 9.38 | 7080 | 0 | 0 | 25410 | 0 | 0 |
| `eurgol.1` | — | 2 | 5 | 9.38 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `eurgol.2` | — | 3 | 8 | 9.38 | 5250 | 0 | 0 | 4950 | 0 | 0 |
| `eurgol.3` | — | 4 | 10 | 9.38 | 12500 | 0 | 0 | 9250 | 0 | 0 |
| `eurgol.4` | — | 5 | 12 | 9.38 | 15800 | 0 | 0 | 18500 | 0 | 0 |
| `eurgol.5` | — | 6 | 15 | 9.38 | 19800 | 0 | 0 | 21050 | 0 | 0 |
| `eurgol.6` | — | 7 | 40 | 9.38 | 7080 | 0 | 0 | 25410 | 0 | 0 |
| `euriro.1` | — | 2 | 5 | 9.38 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `euriro.2` | — | 3 | 8 | 9.38 | 5250 | 0 | 0 | 4950 | 0 | 0 |
| `euriro.3` | — | 4 | 10 | 9.38 | 12500 | 0 | 0 | 9250 | 0 | 0 |
| `euriro.4` | — | 5 | 12 | 9.38 | 15800 | 0 | 0 | 18500 | 0 | 0 |
| `euriro.5` | — | 6 | 15 | 9.38 | 19800 | 0 | 0 | 21050 | 0 | 0 |
| `euriro.6` | — | 7 | 40 | 9.38 | 7080 | 0 | 0 | 25410 | 0 | 0 |
| `turpor.1` | — | 1 | 50 | 46.88 | 0 | 20000 | 0 | 1500 | 0 | 0 |
| `turswa.1` | — | 2 | 5 | 0.03 | 0 | 0 | 500 | 0 | 0 | 0 |
| `turtow.1` | — | 2 | -20 | 31.25 | 0 | 0 | 0 | 250 | 0 | 0 |
| `turtow.2` | — | 3 | -20 | 31.25 | 0 | 0 | 0 | 0 | 350 | 0 |
| `turtow.3` | — | 4 | -10 | 31.25 | 0 | 0 | 0 | 0 | 0 | 400 |
| `turtow.4` | — | 5 | -10 | 31.25 | 0 | 0 | 0 | 0 | 450 | 0 |
| `turtow.5` | — | 6 | -10 | 31.25 | 0 | 0 | 0 | 0 | 0 | 500 |
| `ukrwwa.1` | — | 2 | 5 | 0.03 | 0 | 400 | 0 | 0 | 0 | 0 |

### net — Netherlands

| sid | имя (EN) | level | value | время (s) | F | W | S | G | I | C |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `eurcoa.1` | — | 2 | 5 | 9.38 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `eurcoa.2` | — | 3 | 8 | 9.38 | 5250 | 0 | 0 | 4950 | 0 | 0 |
| `eurcoa.3` | — | 4 | 10 | 9.38 | 12500 | 0 | 0 | 9250 | 0 | 0 |
| `eurcoa.4` | — | 5 | 12 | 9.38 | 15800 | 0 | 0 | 18500 | 0 | 0 |
| `eurcoa.5` | — | 6 | 15 | 9.38 | 19800 | 0 | 0 | 21050 | 0 | 0 |
| `eurcoa.6` | — | 7 | 40 | 9.38 | 50200 | 0 | 0 | 25950 | 0 | 0 |
| `eurgol.1` | — | 2 | 5 | 9.38 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `eurgol.2` | — | 3 | 8 | 9.38 | 5250 | 0 | 0 | 4950 | 0 | 0 |
| `eurgol.3` | — | 4 | 10 | 9.38 | 12500 | 0 | 0 | 9250 | 0 | 0 |
| `eurgol.4` | — | 5 | 12 | 9.38 | 15800 | 0 | 0 | 18500 | 0 | 0 |
| `eurgol.5` | — | 6 | 15 | 9.38 | 19800 | 0 | 0 | 21050 | 0 | 0 |
| `eurgol.6` | — | 7 | 40 | 9.38 | 50200 | 0 | 0 | 25950 | 0 | 0 |
| `euriro.1` | — | 2 | 5 | 9.38 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `euriro.2` | — | 3 | 8 | 9.38 | 5250 | 0 | 0 | 4950 | 0 | 0 |
| `euriro.3` | — | 4 | 10 | 9.38 | 12500 | 0 | 0 | 9250 | 0 | 0 |
| `euriro.4` | — | 5 | 12 | 9.38 | 15800 | 0 | 0 | 18500 | 0 | 0 |
| `euriro.5` | — | 6 | 15 | 9.38 | 19800 | 0 | 0 | 21050 | 0 | 0 |
| `euriro.6` | — | 7 | 40 | 9.38 | 50200 | 0 | 0 | 25950 | 0 | 0 |
| `eurpor.1` | — | 1 | 50 | 46.88 | 0 | 20000 | 0 | 1500 | 0 | 0 |
| `eurswa.1` | — | 2 | 5 | 0.03 | 0 | 0 | 500 | 0 | 0 | 0 |
| `eurtow.1` | — | 2 | -20 | 31.25 | 0 | 0 | 0 | 250 | 0 | 0 |
| `eurtow.2` | — | 3 | -20 | 31.25 | 0 | 0 | 0 | 0 | 350 | 0 |
| `eurtow.3` | — | 4 | -10 | 31.25 | 0 | 0 | 0 | 0 | 0 | 400 |
| `eurtow.4` | — | 5 | -10 | 31.25 | 0 | 0 | 0 | 0 | 450 | 0 |
| `eurtow.5` | — | 6 | -10 | 31.25 | 0 | 0 | 0 | 0 | 0 | 500 |
| `ferry.1` | Improve transport vessel design (+%value% capacity) | 2 | 200 | 15.62 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `netaca.1` | Cultivate new cultures of wheat (harvesting +40%) | 1 | 40 | 15.62 | 0 | 200 | 0 | 325 | 0 | 0 |
| `netaca.10` | Raise builders' salary (building construction time -75%) | 1 | -7500000 | 15.62 | 0 | 0 | 0 | 6950 | 0 | 0 |
| `netaca.11` | Research new fortification grades (durability of walls and towers +80) | 1 | 80 | 15.62 | 0 | 0 | 16200 | 1500 | 0 | 0 |
| `netaca.12` | Improve firearms: rifled barrel (fire power +10%) | 1 | 10 | 15.62 | 0 | 0 | 0 | 0 | 5000 | 0 |
| `netaca.13` | Research granular gunpowder (fire power +10%) | 1 | 10 | 15.62 | 0 | 0 | 0 | 4000 | 0 | 0 |
| `netaca.14` | Research new sulphur purification methods (fire power +15%) | 1 | 15 | 15.62 | 0 | 0 | 0 | 7000 | 0 | 0 |
| `netaca.15` | Research new nitre purification methods (fire power +25%) | 1 | 25 | 15.62 | 0 | 0 | 0 | 0 | 0 | 11000 |
| `netaca.16` | Research improved additions to gunpowder formula (artillery range +5%) | 1 | 5 | 15.62 | 0 | 0 | 0 | 2000 | 12150 | 0 |
| `netaca.17` | Design new barrel types: unicorn, carronade (artillery range +10%) | 1 | 10 | 15.62 | 0 | 0 | 3000 | 4550 | 19200 | 0 |
| `netaca.18` | Design more durable gun carriage: Gribovalle system (artillery durability +50%) | 1 | 50 | 15.62 | 0 | 0 | 0 | 500 | 3830 | 1500 |
| `netaca.19` | Design multi-barrelled cannon | 1 | 0 | 15.62 | 0 | 0 | 0 | 1500 | 0 | 2500 |
| `netaca.2` | Cultivate new cultures of rye (harvesting +50%) | 1 | 50 | 15.62 | 0 | 2400 | 0 | 625 | 0 | 0 |
| `netaca.20` | Research new sighting devices for artillery (artillery accuracy +35%) | 1 | -35 | 15.62 | 0 | 3540 | 0 | 2000 | 0 | 7250 |
| `netaca.21` | Finance artillery repair shops (repair all artillery) | 1 | 25 | 15.62 | 0 | 350 | 0 | 100 | 0 | 250 |
| `netaca.22` | Develop geology (previously hidden deposits appear on the map) | 1 | 0 | 15.62 | 0 | 0 | 0 | 250 | 0 | 0 |
| `netaca.23` | Develop mining (stone excavation efficiency +100%) | 1 | 100 | 15.62 | 0 | 0 | 0 | 1550 | 3000 | 0 |
| `netaca.24` | Raise miners' salary (stone excavation efficiency +200%) | 1 | 200 | 15.62 | 4200 | 0 | 0 | 1550 | 0 | 12520 |
| `netaca.25` | Design Montgolfier (reveals the whole map) | 1 | 0 | 15.62 | 0 | 0 | 0 | 5750 | 0 | 0 |
| `netaca.26` | Develop medical science (heals all live units) | 1 | 50 | 31.25 | 0 | 0 | 0 | 200 | 0 | 200 |
| `netaca.27` | Develop mathematics (artillery accuracy +35%) | 1 | -35 | 15.62 | 0 | 9540 | 0 | 12000 | 0 | 65200 |
| `netaca.28` | Design new rigging types (ship speed +40%) | 1 | 40 | 15.62 | 0 | 65400 | 0 | 24050 | 0 | 0 |
| `netaca.29` | Design new rib system and new hulls (battleship construction) | 1 | 0 | 15.62 | 0 | 32300 | 0 | 6800 | 9000 | 12800 |
| `netaca.3` | Raise agriculturists' salary (harvesting +50%) | 1 | 50 | 15.62 | 0 | 3600 | 0 | 850 | 0 | 0 |
| `netaca.30` | Train carpenters (shipbuilding speed x10) | 1 | -5000000 | 15.62 | 0 | 2300 | 42700 | 1150 | 0 | 0 |
| `netaca.31` | Design wheellock (rate of fire +30%) | 1 | -30 | 15.62 | 0 | 0 | 6000 | 5500 | 4200 | 0 |
| `netaca.32` | Design flintlock (musket cost -50%) | 1 | 0 | 15.62 | 0 | 0 | 0 | 6050 | 0 | 7750 |
| `netaca.33` | Design paper cartridge and iron ramrod (rate of fire +30%) | 1 | -30 | 15.62 | 0 | 5000 | 0 | 5500 | 0 | 15200 |
| `netaca.34` | Research improved steel grades for cuirasses (armoured soldier defence +2) | 1 | 2 | 15.62 | 0 | 0 | 0 | 9750 | 0 | 0 |
| `netaca.35` | Design bayonet: barrel-inserted, bayonet with a tube (cold steel weapons +5) | 1 | 5 | 15.62 | 0 | 0 | 0 | 11500 | 0 | 0 |
| `netaca.36` | Research new steel grades (18c musketeer/grenadier melee attack efficiency +25%) | 1 | 25 | 15.62 | 0 | 0 | 0 | 19500 | 0 | 0 |
| `netaca.4` | Carry out field melioration (field capacity +200%) | 1 | 200 | 15.62 | 0 | 1000 | 0 | 475 | 0 | 0 |
| `netaca.5` | Design new tackle and fishing nets (boat efficiency +100%) | 1 | 100 | 15.62 | 0 | 12400 | 0 | 2520 | 0 | 0 |
| `netaca.6` | Develop new woodworking methods (frigate building) | 1 | 0 | 15.62 | 0 | 12400 | 0 | 7040 | 0 | 0 |
| `netaca.7` | Build new shipyards for fishing boats (fishing boat cost -85%) | 1 | 0 | 15.62 | 0 | 7300 | 0 | 1220 | 0 | 0 |
| `netaca.8` | Design new woodworking tools (woodcutting efficiency +100%) | 1 | 100 | 15.62 | 5500 | 0 | 0 | 550 | 0 | 0 |
| `netaca.9` | Use new construction materials (durability of buildings +85) | 1 | 85 | 15.62 | 0 | 9400 | 7850 | 1150 | 0 | 0 |
| `netart.cannon.1.1` | — | 2 | — | 10.0 | 0 | 1000 | 500 | 300 | 0 | 0 |
| `netart.cannon.1.2` | — | 3 | — | 10.0 | 0 | 3000 | 1000 | 500 | 0 | 0 |
| `netart.cannon.1.3` | — | 4 | — | 10.0 | 0 | 6000 | 2000 | 1000 | 0 | 0 |
| `netart.cannon.1.4` | — | 5 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `netart.cannon.1.5` | — | 6 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `netart.cannon.1.6` | — | 7 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `netart.cannon.2.1` | — | 2 | -2500000 | 10.0 | 0 | 0 | 0 | 500 | 1000 | 0 |
| `netart.cannon.2.2` | — | 3 | -2500000 | 10.0 | 0 | 0 | 0 | 1000 | 2000 | 0 |
| `netart.cannon.2.3` | — | 4 | -2500000 | 10.0 | 0 | 0 | 0 | 2000 | 3000 | 0 |
| `netart.cannon.2.4` | — | 5 | -2000000 | 15.62 | 2560 | 0 | 0 | 0 | 0 | 0 |
| `netart.cannon.2.5` | — | 6 | -2000000 | 15.62 | 3560 | 0 | 0 | 0 | 0 | 0 |
| `netart.cannon.2.6` | — | 7 | -2000000 | 15.62 | 5560 | 0 | 0 | 0 | 0 | 0 |
| `netart.howitzer.1.1` | — | 2 | — | 10.0 | 0 | 1000 | 500 | 300 | 0 | 0 |
| `netart.howitzer.1.2` | — | 3 | — | 10.0 | 0 | 3000 | 1000 | 500 | 0 | 0 |
| `netart.howitzer.1.3` | — | 4 | — | 10.0 | 0 | 6000 | 2000 | 1000 | 0 | 0 |
| `netart.howitzer.1.4` | — | 5 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `netart.howitzer.1.5` | — | 6 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `netart.howitzer.1.6` | — | 7 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `netart.howitzer.2.1` | — | 2 | -2500000 | 10.0 | 0 | 0 | 0 | 500 | 1000 | 0 |
| `netart.howitzer.2.2` | — | 3 | -2500000 | 10.0 | 0 | 0 | 0 | 1000 | 2000 | 0 |
| `netart.howitzer.2.3` | — | 4 | -2500000 | 10.0 | 0 | 0 | 0 | 2000 | 3000 | 0 |
| `netart.howitzer.2.4` | — | 5 | -2000000 | 31.25 | 2560 | 0 | 0 | 0 | 0 | 0 |
| `netart.howitzer.2.5` | — | 6 | -2000000 | 31.25 | 3560 | 0 | 0 | 0 | 0 | 0 |
| `netart.howitzer.2.6` | — | 7 | -2000000 | 31.25 | 5560 | 0 | 0 | 0 | 0 | 0 |
| `netba2.drummer18.2.1` | Barracks 18c drummer18 protection +15 (lvl 2) | 2 | 15 | 15.62 | 450 | 0 | 0 | 75 | 0 | 0 |
| `netba2.grenadier.1.1` | Barracks 18c grenadier damage +2 (lvl 2) | 2 | 2 | 15.62 | 2000 | 0 | 0 | 800 | 0 | 0 |
| `netba2.grenadier.1.2` | Barracks 18c grenadier damage +3 (lvl 3) | 3 | 3 | 15.62 | 12000 | 0 | 0 | 1800 | 0 | 0 |
| `netba2.grenadier.1.3` | Barracks 18c grenadier damage +4 (lvl 4) | 4 | 4 | 15.62 | 32000 | 0 | 0 | 2800 | 0 | 0 |
| `netba2.grenadier.1.4` | Barracks 18c grenadier damage +5 (lvl 5) | 5 | 5 | 15.62 | 42000 | 0 | 0 | 3800 | 0 | 0 |
| `netba2.grenadier.1.5` | Barracks 18c grenadier damage +6 (lvl 6) | 6 | 6 | 15.62 | 52000 | 0 | 0 | 4800 | 0 | 0 |
| `netba2.grenadier.1.6` | Barracks 18c grenadier damage +1500 (lvl 7) | 7 | 1500 | 15.62 | 62000 | 0 | 0 | 15800 | 0 | 0 |
| `netba2.grenadier.2.1` | Barracks 18c grenadier protection +1 (lvl 2) | 2 | 1 | 15.62 | 3706 | 0 | 0 | 350 | 0 | 0 |
| `netba2.grenadier.2.2` | Barracks 18c grenadier protection +2 (lvl 3) | 3 | 2 | 15.62 | 11030 | 0 | 0 | 1350 | 0 | 0 |
| `netba2.grenadier.2.3` | Barracks 18c grenadier protection +3 (lvl 4) | 4 | 3 | 15.62 | 35706 | 0 | 0 | 3000 | 0 | 0 |
| `netba2.grenadier.2.4` | Barracks 18c grenadier protection +1 (lvl 5) | 5 | 1 | 15.62 | 36556 | 0 | 0 | 3350 | 0 | 0 |
| `netba2.grenadier.2.5` | Barracks 18c grenadier protection +2 (lvl 6) | 6 | 2 | 15.62 | 30060 | 0 | 0 | 1350 | 0 | 0 |
| `netba2.grenadier.2.6` | Barracks 18c grenadier protection +3 (lvl 7) | 7 | 3 | 15.62 | 64000 | 0 | 0 | 1350 | 0 | 0 |
| `netba2.musketeer18.1.1` | Barracks 18c musketeer18 damage +1 (lvl 2) | 2 | 1 | 15.62 | 900 | 0 | 0 | 100 | 0 | 0 |
| `netba2.musketeer18.1.2` | Barracks 18c musketeer18 damage +1 (lvl 3) | 3 | 1 | 15.62 | 1600 | 0 | 0 | 200 | 0 | 0 |
| `netba2.musketeer18.1.3` | Barracks 18c musketeer18 damage +2 (lvl 4) | 4 | 2 | 15.62 | 1500 | 0 | 0 | 300 | 0 | 0 |
| `netba2.musketeer18.1.4` | Barracks 18c musketeer18 damage +2 (lvl 5) | 5 | 2 | 15.62 | 3100 | 0 | 0 | 2600 | 0 | 0 |
| `netba2.musketeer18.1.5` | Barracks 18c musketeer18 damage +3 (lvl 6) | 6 | 3 | 15.62 | 2900 | 0 | 0 | 200 | 0 | 0 |
| `netba2.musketeer18.1.6` | Barracks 18c musketeer18 damage +3 (lvl 7) | 7 | 3 | 15.62 | 3200 | 0 | 0 | 1400 | 0 | 0 |
| `netba2.musketeer18.2.1` | Barracks 18c musketeer18 protection +1 (lvl 2) | 2 | 1 | 15.62 | 3906 | 0 | 0 | 350 | 0 | 0 |
| `netba2.musketeer18.2.2` | Barracks 18c musketeer18 protection +2 (lvl 3) | 3 | 2 | 15.62 | 9030 | 0 | 0 | 1150 | 0 | 0 |
| `netba2.musketeer18.2.3` | Barracks 18c musketeer18 protection +2 (lvl 4) | 4 | 2 | 15.62 | 37706 | 0 | 0 | 4200 | 0 | 0 |
| `netba2.musketeer18.2.4` | Barracks 18c musketeer18 protection +1 (lvl 5) | 5 | 1 | 15.62 | 32556 | 0 | 0 | 3350 | 0 | 0 |
| `netba2.musketeer18.2.5` | Barracks 18c musketeer18 protection +2 (lvl 6) | 6 | 2 | 15.62 | 34060 | 0 | 0 | 2350 | 0 | 0 |
| `netba2.musketeer18.2.6` | Barracks 18c musketeer18 protection +2 (lvl 7) | 7 | 2 | 15.62 | 36500 | 0 | 0 | 1550 | 0 | 0 |
| `netba2.officer18.1.1` | Barracks 18c officer18 damage +30 (lvl 2) | 2 | 30 | 15.62 | 900 | 0 | 0 | 775 | 0 | 0 |
| `netba2.officer18.2.1` | Barracks 18c officer18 protection +12 (lvl 2) | 2 | 12 | 15.62 | 1606 | 0 | 0 | 650 | 0 | 0 |
| `netba2.pikeman18.1.1` | Barracks 18c pikeman18 damage +2 (lvl 2) | 2 | 2 | 15.62 | 2000 | 0 | 0 | 800 | 0 | 0 |
| `netba2.pikeman18.1.2` | Barracks 18c pikeman18 damage +2 (lvl 3) | 3 | 2 | 15.62 | 8000 | 0 | 0 | 1200 | 0 | 0 |
| `netba2.pikeman18.1.3` | Barracks 18c pikeman18 damage +2 (lvl 4) | 4 | 2 | 15.62 | 20000 | 0 | 0 | 2500 | 0 | 0 |
| `netba2.pikeman18.1.4` | Barracks 18c pikeman18 damage +2 (lvl 5) | 5 | 2 | 15.62 | 32000 | 0 | 0 | 2800 | 0 | 0 |
| `netba2.pikeman18.1.5` | Barracks 18c pikeman18 damage +2 (lvl 6) | 6 | 2 | 15.62 | 32000 | 0 | 0 | 3800 | 0 | 0 |
| `netba2.pikeman18.1.6` | Barracks 18c pikeman18 damage +2 (lvl 7) | 7 | 2 | 15.62 | 40500 | 0 | 0 | 4800 | 0 | 0 |
| `netba2.pikeman18.2.1` | Barracks 18c pikeman18 protection +2 (lvl 2) | 2 | 2 | 15.62 | 1500 | 0 | 0 | 500 | 0 | 0 |
| `netba2.pikeman18.2.2` | Barracks 18c pikeman18 protection +3 (lvl 3) | 3 | 3 | 15.62 | 7000 | 0 | 0 | 1500 | 0 | 0 |
| `netba2.pikeman18.2.3` | Barracks 18c pikeman18 protection +2 (lvl 4) | 4 | 2 | 15.62 | 37000 | 0 | 0 | 2000 | 0 | 0 |
| `netba2.pikeman18.2.4` | Barracks 18c pikeman18 protection +3 (lvl 5) | 5 | 3 | 15.62 | 37000 | 0 | 0 | 5500 | 0 | 0 |
| `netba2.pikeman18.2.5` | Barracks 18c pikeman18 protection +2 (lvl 6) | 6 | 2 | 15.62 | 37000 | 0 | 0 | 5500 | 0 | 0 |
| `netba2.pikeman18.2.6` | Barracks 18c pikeman18 protection +3 (lvl 7) | 7 | 3 | 15.62 | 64600 | 0 | 0 | 5500 | 0 | 0 |
| `netbar.1` | — | 1 | 140 | 15.62 | 750 | 0 | 0 | 250 | 0 | 0 |
| `netbar.2` | — | 2 | 180 | 15.62 | 25600 | 0 | 0 | 3350 | 2000 | 0 |
| `netbar.drummer.2.1` | Barracks 17c drummer protection +12 (lvl 2) | 2 | 12 | 15.62 | 845 | 0 | 0 | 95 | 0 | 0 |
| `netbar.musketeernet.1.1` | Barracks 17c musketeernet damage +1 (lvl 2) | 2 | 1 | 15.62 | 2000 | 0 | 0 | 100 | 0 | 0 |
| `netbar.musketeernet.1.2` | Barracks 17c musketeernet damage +1 (lvl 3) | 3 | 1 | 15.62 | 1000 | 0 | 0 | 300 | 0 | 0 |
| `netbar.musketeernet.1.3` | Barracks 17c musketeernet damage +2 (lvl 4) | 4 | 2 | 15.62 | 500 | 0 | 0 | 700 | 0 | 0 |
| `netbar.musketeernet.2.1` | Barracks 17c musketeernet protection +1 (lvl 2) | 2 | 1 | 15.62 | 170 | 0 | 0 | 50 | 100 | 0 |
| `netbar.musketeernet.2.2` | Barracks 17c musketeernet protection +1 (lvl 3) | 3 | 1 | 15.62 | 405 | 0 | 0 | 150 | 200 | 0 |
| `netbar.musketeernet.2.3` | Barracks 17c musketeernet protection +2 (lvl 4) | 4 | 2 | 15.62 | 1570 | 0 | 0 | 100 | 350 | 0 |
| `netbar.musketeernet.2.4` | Barracks 17c musketeernet protection +1 (lvl 5) | 5 | 1 | 15.62 | 1556 | 0 | 0 | 550 | 100 | 0 |
| `netbar.musketeernet.2.5` | Barracks 17c musketeernet protection +1 (lvl 6) | 6 | 1 | 15.62 | 1060 | 0 | 0 | 850 | 400 | 0 |
| `netbar.musketeernet.2.6` | Barracks 17c musketeernet protection +2 (lvl 7) | 7 | 2 | 15.62 | 3700 | 0 | 0 | 450 | 700 | 0 |
| `netbar.officer.1.1` | Barracks 17c officer damage +20 (lvl 2) | 2 | 20 | 15.62 | 500 | 0 | 0 | 25 | 0 | 0 |
| `netbar.officer.2.1` | Barracks 17c officer protection +6 (lvl 2) | 2 | 6 | 15.62 | 1550 | 0 | 0 | 475 | 0 | 0 |
| `netbar.pikeman.1.1` | Barracks 17c pikeman damage +1 (lvl 2) | 2 | 1 | 15.62 | 900 | 0 | 0 | 150 | 0 | 0 |
| `netbar.pikeman.1.2` | Barracks 17c pikeman damage +2 (lvl 3) | 3 | 2 | 15.62 | 700 | 0 | 0 | 400 | 0 | 0 |
| `netbar.pikeman.1.3` | Barracks 17c pikeman damage +2 (lvl 4) | 4 | 2 | 15.62 | 3100 | 0 | 0 | 250 | 0 | 0 |
| `netbar.pikeman.1.4` | Barracks 17c pikeman damage +1 (lvl 5) | 5 | 1 | 15.62 | 6700 | 0 | 0 | 1950 | 0 | 0 |
| `netbar.pikeman.1.5` | Barracks 17c pikeman damage +2 (lvl 6) | 6 | 2 | 15.62 | 16030 | 0 | 0 | 2000 | 0 | 0 |
| `netbar.pikeman.1.6` | — | 7 | 2 | 15.62 | 15000 | 0 | 0 | 1875 | 0 | 0 |
| `netbar.pikeman.2.1` | Barracks 17c pikeman protection +1 (lvl 2) | 2 | 1 | 15.62 | 250 | 0 | 0 | 150 | 0 | 0 |
| `netbar.pikeman.2.2` | Barracks 17c pikeman protection +1 (lvl 3) | 3 | 1 | 15.62 | 800 | 0 | 0 | 275 | 0 | 0 |
| `netbar.pikeman.2.3` | Barracks 17c pikeman protection +2 (lvl 4) | 4 | 2 | 15.62 | 4200 | 0 | 0 | 100 | 0 | 0 |
| `netbar.pikeman.2.4` | Barracks 17c pikeman protection +1 (lvl 5) | 5 | 1 | 15.62 | 9305 | 0 | 0 | 707 | 0 | 0 |
| `netbar.pikeman.2.5` | Barracks 17c pikeman protection +1 (lvl 6) | 6 | 1 | 15.62 | 17890 | 0 | 0 | 2850 | 0 | 0 |
| `netbar.pikeman.2.6` | — | 7 | 2 | 15.62 | 11250 | 0 | 0 | 1500 | 0 | 0 |
| `netbla.1` | Manufacture agricultural equipment (field capacity +100%) | 1 | 100 | 15.62 | 0 | 400 | 0 | 90 | 0 | 0 |
| `netbla.2` | Forge metal armature and gratings (building defence +50) | 1 | 50 | 15.62 | 0 | 0 | 12320 | 350 | 900 | 0 |
| `netbla.3` | Forge harnesses for horses (mounted units recruitment speed -33%) | 1 | -3333333 | 15.62 | 0 | 0 | 0 | 3650 | 5300 | 8200 |
| `netbla.4` | Forge bayonets and broadswords for infantry (18c musketeer/grenadier melee attack +5) | 1 | 5 | 15.62 | 0 | 1300 | 0 | 1500 | 900 | 5000 |
| `netbla.5` | Forge new types of broadswords and sabres (cavalry and sword clansman attack +5) | 1 | 5 | 15.62 | 0 | 0 | 0 | 4000 | 7900 | 0 |
| `netbla.6` | Forge new cuirasses (armoured soldiers defence +2) | 1 | 2 | 15.62 | 0 | 0 | 0 | 4950 | 10500 | 0 |
| `netcen.1` | — | 1 | 0 | 9.38 | 33000 | 0 | 0 | 4800 | 1800 | 1800 |
| `netsta.cuirassier.1.1` | Stable cuirassier damage +1 (lvl 2) | 2 | 1 | 15.62 | 32000 | 0 | 0 | 600 | 0 | 0 |
| `netsta.cuirassier.1.2` | Stable cuirassier damage +1 (lvl 3) | 3 | 1 | 15.62 | 12000 | 0 | 0 | 1300 | 0 | 0 |
| `netsta.cuirassier.1.3` | Stable cuirassier damage +1 (lvl 4) | 4 | 1 | 15.62 | 64000 | 0 | 0 | 2200 | 0 | 0 |
| `netsta.cuirassier.1.4` | Stable cuirassier damage +2 (lvl 5) | 5 | 2 | 15.62 | 58000 | 0 | 0 | 3150 | 0 | 0 |
| `netsta.cuirassier.1.5` | Stable cuirassier damage +2 (lvl 6) | 6 | 2 | 15.62 | 59055 | 0 | 0 | 4100 | 0 | 0 |
| `netsta.cuirassier.1.6` | Stable cuirassier damage +3 (lvl 7) | 7 | 3 | 15.62 | 47050 | 0 | 0 | 8050 | 0 | 0 |
| `netsta.cuirassier.2.1` | Stable cuirassier protection +2 (lvl 2) | 2 | 2 | 15.62 | 1250 | 0 | 0 | 450 | 1000 | 0 |
| `netsta.cuirassier.2.2` | Stable cuirassier protection +3 (lvl 3) | 3 | 3 | 15.62 | 2500 | 0 | 0 | 650 | 2000 | 0 |
| `netsta.cuirassier.2.3` | Stable cuirassier protection +3 (lvl 4) | 4 | 3 | 15.62 | 4600 | 0 | 0 | 200 | 3050 | 0 |
| `netsta.cuirassier.2.4` | Stable cuirassier protection +2 (lvl 5) | 5 | 2 | 15.62 | 11700 | 0 | 0 | 6100 | 100 | 0 |
| `netsta.cuirassier.2.5` | Stable cuirassier protection +1 (lvl 6) | 6 | 1 | 15.62 | 8700 | 0 | 0 | 2350 | 5000 | 0 |
| `netsta.cuirassier.2.6` | Stable cuirassier protection +1 (lvl 7) | 7 | 1 | 15.62 | 9700 | 0 | 0 | 4444 | 7060 | 0 |
| `netsta.dragoon.1.1` | Stable dragoon damage +1 (lvl 2) | 2 | 1 | 15.62 | 700 | 0 | 0 | 250 | 0 | 0 |
| `netsta.dragoon.1.2` | Stable dragoon damage +1 (lvl 3) | 3 | 1 | 15.62 | 600 | 0 | 0 | 100 | 0 | 0 |
| `netsta.dragoon.1.3` | Stable dragoon damage +2 (lvl 4) | 4 | 2 | 15.62 | 800 | 0 | 0 | 540 | 0 | 0 |
| `netsta.dragoon.1.4` | Stable dragoon damage +1 (lvl 5) | 5 | 1 | 15.62 | 0 | 0 | 0 | 0 | 0 | 0 |
| `netsta.dragoon.1.5` | Stable dragoon damage +1 (lvl 6) | 6 | 1 | 15.62 | 0 | 0 | 0 | 0 | 0 | 0 |
| `netsta.dragoon.1.6` | Stable dragoon damage +3 (lvl 7) | 7 | 3 | 15.62 | 0 | 0 | 0 | 0 | 0 | 0 |
| `netsta.dragoon.2.1` | Stable dragoon protection +1 (lvl 2) | 2 | 1 | 15.62 | 400 | 0 | 0 | 250 | 0 | 0 |
| `netsta.dragoon.2.2` | Stable dragoon protection +2 (lvl 3) | 3 | 2 | 15.62 | 7600 | 0 | 0 | 550 | 0 | 0 |
| `netsta.dragoon.2.3` | Stable dragoon protection +2 (lvl 4) | 4 | 2 | 15.62 | 4000 | 0 | 0 | 950 | 0 | 0 |
| `netsta.dragoon.2.4` | Stable dragoon protection +1 (lvl 5) | 5 | 1 | 15.62 | 4000 | 0 | 0 | 900 | 0 | 0 |
| `netsta.dragoon.2.5` | Stable dragoon protection +2 (lvl 6) | 6 | 2 | 15.62 | 4000 | 0 | 0 | 2150 | 0 | 0 |
| `netsta.dragoon.2.6` | Stable dragoon protection +2 (lvl 7) | 7 | 2 | 15.62 | 3001 | 0 | 0 | 6200 | 0 | 0 |
| `netsta.dragoon18net.1.1` | Stable dragoon18net damage +1 (lvl 2) | 2 | 1 | 15.62 | 2000 | 0 | 0 | 100 | 0 | 0 |
| `netsta.dragoon18net.1.2` | Stable dragoon18net damage +2 (lvl 3) | 3 | 2 | 15.62 | 9000 | 0 | 0 | 350 | 0 | 0 |
| `netsta.dragoon18net.1.3` | Stable dragoon18net damage +3 (lvl 4) | 4 | 3 | 15.62 | 12000 | 0 | 0 | 400 | 0 | 0 |
| `netsta.dragoon18net.1.4` | Stable dragoon18net damage +1 (lvl 5) | 5 | 1 | 15.62 | 23000 | 0 | 0 | 580 | 0 | 0 |
| `netsta.dragoon18net.1.5` | Stable dragoon18net damage +2 (lvl 6) | 6 | 2 | 15.62 | 32000 | 0 | 0 | 680 | 0 | 0 |
| `netsta.dragoon18net.1.6` | Stable dragoon18net damage +3 (lvl 7) | 7 | 3 | 15.62 | 42000 | 0 | 0 | 780 | 0 | 0 |
| `netsta.dragoon18net.2.1` | Stable dragoon18net protection +1 (lvl 2) | 2 | 1 | 15.62 | 760 | 0 | 0 | 935 | 0 | 0 |
| `netsta.dragoon18net.2.2` | Stable dragoon18net protection +2 (lvl 3) | 3 | 2 | 15.62 | 1260 | 0 | 0 | 1150 | 0 | 0 |
| `netsta.dragoon18net.2.3` | Stable dragoon18net protection +2 (lvl 4) | 4 | 2 | 15.62 | 15600 | 0 | 0 | 2350 | 0 | 0 |
| `netsta.dragoon18net.2.4` | Stable dragoon18net protection +1 (lvl 5) | 5 | 1 | 15.62 | 17600 | 0 | 0 | 4350 | 0 | 0 |
| `netsta.dragoon18net.2.5` | Stable dragoon18net protection +2 (lvl 6) | 6 | 2 | 15.62 | 19600 | 0 | 0 | 5350 | 0 | 0 |
| `netsta.dragoon18net.2.6` | Stable dragoon18net protection +2 (lvl 7) | 7 | 2 | 15.62 | 21760 | 0 | 0 | 8350 | 0 | 0 |
| `netsta.hussar.1.1` | Stable hussar damage +1 (lvl 2) | 2 | 1 | 15.62 | 0 | 0 | 0 | 1800 | 1000 | 0 |
| `netsta.hussar.1.2` | Stable hussar damage +2 (lvl 3) | 3 | 2 | 15.62 | 0 | 0 | 0 | 3800 | 2000 | 0 |
| `netsta.hussar.1.3` | Stable hussar damage +3 (lvl 4) | 4 | 3 | 15.62 | 20200 | 0 | 0 | 0 | 3000 | 0 |
| `netsta.hussar.1.4` | Stable hussar damage +4 (lvl 5) | 5 | 4 | 15.62 | 32000 | 0 | 0 | 0 | 3000 | 0 |
| `netsta.hussar.1.5` | Stable hussar damage +1 (lvl 6) | 6 | 1 | 15.62 | 49200 | 0 | 0 | 0 | 3500 | 0 |
| `netsta.hussar.1.6` | Stable hussar damage +1 (lvl 7) | 7 | 1 | 15.62 | 20000 | 0 | 0 | 0 | 6000 | 0 |
| `netsta.hussar.2.1` | Stable hussar protection +1 (lvl 2) | 2 | 1 | 15.62 | 1760 | 0 | 0 | 1350 | 0 | 0 |
| `netsta.hussar.2.2` | Stable hussar protection +1 (lvl 3) | 3 | 1 | 15.62 | 1900 | 0 | 0 | 2350 | 0 | 0 |
| `netsta.hussar.2.3` | Stable hussar protection +1 (lvl 4) | 4 | 1 | 15.62 | 1600 | 0 | 0 | 5350 | 0 | 0 |
| `netsta.hussar.2.4` | Stable hussar protection +2 (lvl 5) | 5 | 2 | 15.62 | 8000 | 0 | 0 | 8350 | 0 | 0 |
| `netsta.hussar.2.5` | Stable hussar protection +2 (lvl 6) | 6 | 2 | 15.62 | 2000 | 0 | 0 | 15350 | 0 | 0 |
| `netsta.hussar.2.6` | Stable hussar protection +3 (lvl 7) | 7 | 3 | 15.62 | 56000 | 0 | 0 | 20150 | 0 | 0 |
| `netsta.reiter.1.1` | Stable reiter damage +1 (lvl 2) | 2 | 1 | 15.62 | 500 | 0 | 0 | 100 | 0 | 0 |
| `netsta.reiter.1.2` | Stable reiter damage +2 (lvl 3) | 3 | 2 | 15.62 | 900 | 0 | 0 | 220 | 0 | 0 |
| `netsta.reiter.1.3` | Stable reiter damage +1 (lvl 4) | 4 | 1 | 15.62 | 4600 | 0 | 0 | 280 | 0 | 0 |
| `netsta.reiter.1.4` | Stable reiter damage +1 (lvl 5) | 5 | 1 | 15.62 | 2050 | 0 | 0 | 220 | 0 | 0 |
| `netsta.reiter.1.5` | Stable reiter damage +1 (lvl 6) | 6 | 1 | 15.62 | 3530 | 0 | 0 | 500 | 0 | 0 |
| `netsta.reiter.1.6` | Stable reiter damage +1 (lvl 7) | 7 | 1 | 15.62 | 6500 | 0 | 0 | 1900 | 0 | 0 |
| `netsta.reiter.2.1` | Stable reiter protection +2 (lvl 2) | 2 | 2 | 15.62 | 250 | 0 | 0 | 55 | 300 | 0 |
| `netsta.reiter.2.2` | Stable reiter protection +3 (lvl 3) | 3 | 3 | 15.62 | 550 | 0 | 0 | 200 | 400 | 0 |
| `netsta.reiter.2.3` | Stable reiter protection +3 (lvl 4) | 4 | 3 | 15.62 | 600 | 0 | 0 | 100 | 560 | 0 |
| `netsta.reiter.2.4` | Stable reiter protection +2 (lvl 5) | 5 | 2 | 15.62 | 1800 | 0 | 0 | 500 | 640 | 0 |
| `netsta.reiter.2.5` | Stable reiter protection +1 (lvl 6) | 6 | 1 | 15.62 | 5200 | 0 | 0 | 250 | 300 | 0 |
| `netsta.reiter.2.6` | Stable reiter protection +1 (lvl 7) | 7 | 1 | 15.62 | 14000 | 0 | 0 | 990 | 5000 | 0 |
| `ukrwwa.1` | — | 2 | 5 | 0.03 | 0 | 400 | 0 | 0 | 0 | 0 |

### den — Denmark

| sid | имя (EN) | level | value | время (s) | F | W | S | G | I | C |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `denaca.1` | Cultivate new cultures of wheat (harvesting +40%) | 1 | 40 | 15.62 | 0 | 200 | 0 | 325 | 0 | 0 |
| `denaca.10` | Raise builders' salary (building construction time -75%) | 1 | -7500000 | 15.62 | 0 | 0 | 0 | 6950 | 0 | 0 |
| `denaca.11` | Research new fortification grades (durability of walls and towers +80) | 1 | 80 | 15.62 | 0 | 0 | 16200 | 1500 | 0 | 0 |
| `denaca.12` | Improve firearms: rifled barrel (fire power +10%) | 1 | 10 | 15.62 | 0 | 0 | 0 | 0 | 5000 | 0 |
| `denaca.13` | Research granular gunpowder (fire power +10%) | 1 | 10 | 15.62 | 0 | 0 | 0 | 4000 | 0 | 0 |
| `denaca.14` | Research new sulphur purification methods (fire power +15%) | 1 | 15 | 15.62 | 0 | 0 | 0 | 7000 | 0 | 0 |
| `denaca.15` | Research new nitre purification methods (fire power +25%) | 1 | 25 | 15.62 | 0 | 0 | 0 | 0 | 0 | 11000 |
| `denaca.16` | Research improved additions to gunpowder formula (artillery range +5%) | 1 | 5 | 15.62 | 0 | 0 | 0 | 2000 | 12150 | 0 |
| `denaca.17` | Design new barrel types: unicorn, carronade (artillery range +10%) | 1 | 10 | 15.62 | 0 | 0 | 3000 | 4550 | 19200 | 0 |
| `denaca.18` | Design more durable gun carriage: Gribovalle system (artillery durability +50%) | 1 | 50 | 15.62 | 0 | 0 | 0 | 500 | 3830 | 1500 |
| `denaca.19` | Design multi-barrelled cannon | 1 | 0 | 15.62 | 0 | 0 | 0 | 1500 | 0 | 2500 |
| `denaca.2` | Cultivate new cultures of rye (harvesting +50%) | 1 | 50 | 15.62 | 0 | 2400 | 0 | 625 | 0 | 0 |
| `denaca.20` | Research new sighting devices for artillery (artillery accuracy +35%) | 1 | -35 | 15.62 | 0 | 3540 | 0 | 2000 | 0 | 7250 |
| `denaca.21` | Finance artillery repair shops (repair all artillery) | 1 | 25 | 15.62 | 0 | 350 | 0 | 100 | 0 | 250 |
| `denaca.22` | Develop geology (previously hidden deposits appear on the map) | 1 | 0 | 15.62 | 0 | 0 | 0 | 250 | 0 | 0 |
| `denaca.23` | Develop mining (stone excavation efficiency +100%) | 1 | 100 | 15.62 | 0 | 0 | 0 | 1550 | 3000 | 0 |
| `denaca.24` | Raise miners' salary (stone excavation efficiency +200%) | 1 | 200 | 15.62 | 4200 | 0 | 0 | 1550 | 0 | 12520 |
| `denaca.25` | Design Montgolfier (reveals the whole map) | 1 | 0 | 15.62 | 0 | 0 | 0 | 5750 | 0 | 0 |
| `denaca.26` | Develop medical science (heals all live units) | 1 | 50 | 31.25 | 0 | 0 | 0 | 200 | 0 | 200 |
| `denaca.27` | Develop mathematics (artillery accuracy +35%) | 1 | -35 | 15.62 | 0 | 9540 | 0 | 12000 | 0 | 65200 |
| `denaca.28` | Design new rigging types (ship speed +40%) | 1 | 40 | 15.62 | 0 | 65400 | 0 | 24050 | 0 | 0 |
| `denaca.29` | Design new rib system and new hulls (battleship construction) | 1 | 0 | 15.62 | 0 | 32300 | 0 | 6800 | 9000 | 12800 |
| `denaca.3` | Raise agriculturists' salary (harvesting +50%) | 1 | 50 | 15.62 | 0 | 3600 | 0 | 850 | 0 | 0 |
| `denaca.30` | Train carpenters (shipbuilding speed x10) | 1 | -5000000 | 15.62 | 0 | 2300 | 42700 | 1150 | 0 | 0 |
| `denaca.31` | Design wheellock (rate of fire +30%) | 1 | -30 | 15.62 | 0 | 0 | 6000 | 5500 | 4200 | 0 |
| `denaca.32` | Design flintlock (musket cost -50%) | 1 | 0 | 15.62 | 0 | 0 | 0 | 6050 | 0 | 7750 |
| `denaca.33` | Design paper cartridge and iron ramrod (rate of fire +30%) | 1 | -30 | 15.62 | 0 | 5000 | 0 | 5500 | 0 | 15200 |
| `denaca.34` | Research improved steel grades for cuirasses (armoured soldier defence +2) | 1 | 2 | 15.62 | 0 | 0 | 0 | 9750 | 0 | 0 |
| `denaca.35` | Design bayonet: barrel-inserted, bayonet with a tube (cold steel weapons +5) | 1 | 5 | 15.62 | 0 | 0 | 0 | 11500 | 0 | 0 |
| `denaca.36` | Research new steel grades (18c musketeer/grenadier melee attack efficiency +25%) | 1 | 25 | 15.62 | 0 | 0 | 0 | 19500 | 0 | 0 |
| `denaca.4` | Carry out field melioration (field capacity +200%) | 1 | 200 | 15.62 | 0 | 1000 | 0 | 475 | 0 | 0 |
| `denaca.5` | Design new tackle and fishing nets (boat efficiency +100%) | 1 | 100 | 15.62 | 0 | 12400 | 0 | 2520 | 0 | 0 |
| `denaca.6` | Develop new woodworking methods (frigate building) | 1 | 0 | 15.62 | 0 | 12400 | 0 | 7040 | 0 | 0 |
| `denaca.7` | Build new shipyards for fishing boats (fishing boat cost -85%) | 1 | 0 | 15.62 | 0 | 7300 | 0 | 1220 | 0 | 0 |
| `denaca.8` | Design new woodworking tools (woodcutting efficiency +100%) | 1 | 100 | 15.62 | 5500 | 0 | 0 | 550 | 0 | 0 |
| `denaca.9` | Use new construction materials (durability of buildings +85) | 1 | 85 | 15.62 | 0 | 9400 | 7850 | 1150 | 0 | 0 |
| `denart.cannon.1.1` | — | 2 | — | 10.0 | 0 | 1000 | 500 | 300 | 0 | 0 |
| `denart.cannon.1.2` | — | 3 | — | 10.0 | 0 | 3000 | 1000 | 500 | 0 | 0 |
| `denart.cannon.1.3` | — | 4 | — | 10.0 | 0 | 6000 | 2000 | 1000 | 0 | 0 |
| `denart.cannon.1.4` | — | 5 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `denart.cannon.1.5` | — | 6 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `denart.cannon.1.6` | — | 7 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `denart.cannon.2.1` | — | 2 | -2500000 | 10.0 | 0 | 0 | 0 | 500 | 1000 | 0 |
| `denart.cannon.2.2` | — | 3 | -2500000 | 10.0 | 0 | 0 | 0 | 1000 | 2000 | 0 |
| `denart.cannon.2.3` | — | 4 | -2500000 | 10.0 | 0 | 0 | 0 | 2000 | 3000 | 0 |
| `denart.cannon.2.4` | — | 5 | -2000000 | 15.62 | 2560 | 0 | 0 | 0 | 0 | 0 |
| `denart.cannon.2.5` | — | 6 | -2000000 | 15.62 | 3560 | 0 | 0 | 0 | 0 | 0 |
| `denart.cannon.2.6` | — | 7 | -2000000 | 15.62 | 5560 | 0 | 0 | 0 | 0 | 0 |
| `denart.howitzer.1.1` | — | 2 | — | 10.0 | 0 | 1000 | 500 | 300 | 0 | 0 |
| `denart.howitzer.1.2` | — | 3 | — | 10.0 | 0 | 3000 | 1000 | 500 | 0 | 0 |
| `denart.howitzer.1.3` | — | 4 | — | 10.0 | 0 | 6000 | 2000 | 1000 | 0 | 0 |
| `denart.howitzer.1.4` | — | 5 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `denart.howitzer.1.5` | — | 6 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `denart.howitzer.1.6` | — | 7 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `denart.howitzer.2.1` | — | 2 | -2500000 | 10.0 | 0 | 0 | 0 | 500 | 1000 | 0 |
| `denart.howitzer.2.2` | — | 3 | -2500000 | 10.0 | 0 | 0 | 0 | 1000 | 2000 | 0 |
| `denart.howitzer.2.3` | — | 4 | -2500000 | 10.0 | 0 | 0 | 0 | 2000 | 3000 | 0 |
| `denart.howitzer.2.4` | — | 5 | -2000000 | 31.25 | 2560 | 0 | 0 | 0 | 0 | 0 |
| `denart.howitzer.2.5` | — | 6 | -2000000 | 31.25 | 3560 | 0 | 0 | 0 | 0 | 0 |
| `denart.howitzer.2.6` | — | 7 | -2000000 | 31.25 | 5560 | 0 | 0 | 0 | 0 | 0 |
| `denba2.drummer18.2.1` | Barracks 18c drummer18 protection +15 (lvl 2) | 2 | 15 | 15.62 | 900 | 0 | 0 | 45 | 0 | 0 |
| `denba2.grenadierden.1.1` | Barracks 18c grenadierden damage +3 (lvl 2) | 2 | 3 | 15.62 | 1000 | 0 | 0 | 800 | 0 | 0 |
| `denba2.grenadierden.1.2` | Barracks 18c grenadierden damage +4 (lvl 3) | 3 | 4 | 15.62 | 13000 | 0 | 0 | 2800 | 0 | 0 |
| `denba2.grenadierden.1.3` | Barracks 18c grenadierden damage +4 (lvl 4) | 4 | 4 | 15.62 | 32000 | 0 | 0 | 1800 | 0 | 0 |
| `denba2.grenadierden.1.4` | Barracks 18c grenadierden damage +4 (lvl 5) | 5 | 4 | 15.62 | 52000 | 0 | 0 | 4800 | 0 | 0 |
| `denba2.grenadierden.1.5` | Barracks 18c grenadierden damage +5 (lvl 6) | 6 | 5 | 15.62 | 42000 | 0 | 0 | 3800 | 0 | 0 |
| `denba2.grenadierden.1.6` | Barracks 18c grenadierden damage +1500 (lvl 7) | 7 | 1500 | 15.62 | 64000 | 0 | 0 | 14800 | 0 | 0 |
| `denba2.grenadierden.2.1` | Barracks 18c grenadierden protection +2 (lvl 2) | 2 | 2 | 15.62 | 3205 | 0 | 0 | 375 | 0 | 0 |
| `denba2.grenadierden.2.2` | Barracks 18c grenadierden protection +3 (lvl 3) | 3 | 3 | 15.62 | 11030 | 0 | 0 | 4350 | 0 | 0 |
| `denba2.grenadierden.2.3` | Barracks 18c grenadierden protection +3 (lvl 4) | 4 | 3 | 15.62 | 36206 | 0 | 0 | 500 | 0 | 0 |
| `denba2.grenadierden.2.4` | Barracks 18c grenadierden protection +2 (lvl 5) | 5 | 2 | 15.62 | 34950 | 0 | 0 | 1350 | 0 | 0 |
| `denba2.grenadierden.2.5` | Barracks 18c grenadierden protection +1 (lvl 6) | 6 | 1 | 15.62 | 30060 | 0 | 0 | 2150 | 0 | 0 |
| `denba2.grenadierden.2.6` | Barracks 18c grenadierden protection +1 (lvl 7) | 7 | 1 | 15.62 | 64000 | 0 | 0 | 2550 | 0 | 0 |
| `denba2.musketeer18den.1.1` | Barracks 18c musketeer18den damage +1 (lvl 2) | 2 | 1 | 15.62 | 900 | 0 | 0 | 700 | 0 | 0 |
| `denba2.musketeer18den.1.2` | Barracks 18c musketeer18den damage +1 (lvl 3) | 3 | 1 | 15.62 | 1600 | 0 | 0 | 800 | 0 | 0 |
| `denba2.musketeer18den.1.3` | Barracks 18c musketeer18den damage +1 (lvl 4) | 4 | 1 | 15.62 | 2500 | 0 | 0 | 900 | 0 | 0 |
| `denba2.musketeer18den.1.4` | Barracks 18c musketeer18den damage +1 (lvl 5) | 5 | 1 | 15.62 | 2000 | 0 | 0 | 600 | 0 | 0 |
| `denba2.musketeer18den.1.5` | Barracks 18c musketeer18den damage +1 (lvl 6) | 6 | 1 | 15.62 | 3500 | 0 | 0 | 1000 | 0 | 0 |
| `denba2.musketeer18den.1.6` | Barracks 18c musketeer18den damage +1 (lvl 7) | 7 | 1 | 15.62 | 3000 | 0 | 0 | 800 | 0 | 0 |
| `denba2.musketeer18den.2.1` | Barracks 18c musketeer18den protection +1 (lvl 2) | 2 | 1 | 15.62 | 3500 | 0 | 0 | 350 | 0 | 0 |
| `denba2.musketeer18den.2.2` | Barracks 18c musketeer18den protection +1 (lvl 3) | 3 | 1 | 15.62 | 11230 | 0 | 0 | 1350 | 0 | 0 |
| `denba2.musketeer18den.2.3` | Barracks 18c musketeer18den protection +1 (lvl 4) | 4 | 1 | 15.62 | 35706 | 0 | 0 | 4000 | 0 | 0 |
| `denba2.musketeer18den.2.4` | Barracks 18c musketeer18den protection +2 (lvl 5) | 5 | 2 | 15.62 | 36556 | 0 | 0 | 4350 | 0 | 0 |
| `denba2.musketeer18den.2.5` | Barracks 18c musketeer18den protection +2 (lvl 6) | 6 | 2 | 15.62 | 30060 | 0 | 0 | 1350 | 0 | 0 |
| `denba2.musketeer18den.2.6` | Barracks 18c musketeer18den protection +3 (lvl 7) | 7 | 3 | 15.62 | 37600 | 0 | 0 | 1350 | 0 | 0 |
| `denba2.officer18.1.1` | Barracks 18c officer18 damage +30 (lvl 2) | 2 | 30 | 15.62 | 1200 | 0 | 0 | 750 | 0 | 0 |
| `denba2.officer18.2.1` | Barracks 18c officer18 protection +12 (lvl 2) | 2 | 12 | 15.62 | 1500 | 0 | 0 | 375 | 0 | 0 |
| `denba2.pikeman18.1.1` | Barracks 18c pikeman18 damage +2 (lvl 2) | 2 | 2 | 15.62 | 2000 | 0 | 0 | 800 | 0 | 0 |
| `denba2.pikeman18.1.2` | Barracks 18c pikeman18 damage +2 (lvl 3) | 3 | 2 | 15.62 | 8000 | 0 | 0 | 1200 | 0 | 0 |
| `denba2.pikeman18.1.3` | Barracks 18c pikeman18 damage +2 (lvl 4) | 4 | 2 | 15.62 | 20000 | 0 | 0 | 2500 | 0 | 0 |
| `denba2.pikeman18.1.4` | Barracks 18c pikeman18 damage +2 (lvl 5) | 5 | 2 | 15.62 | 32000 | 0 | 0 | 2800 | 0 | 0 |
| `denba2.pikeman18.1.5` | Barracks 18c pikeman18 damage +2 (lvl 6) | 6 | 2 | 15.62 | 32000 | 0 | 0 | 3800 | 0 | 0 |
| `denba2.pikeman18.1.6` | Barracks 18c pikeman18 damage +2 (lvl 7) | 7 | 2 | 15.62 | 40500 | 0 | 0 | 4800 | 0 | 0 |
| `denba2.pikeman18.2.1` | Barracks 18c pikeman18 protection +2 (lvl 2) | 2 | 2 | 15.62 | 1500 | 0 | 0 | 500 | 0 | 0 |
| `denba2.pikeman18.2.2` | Barracks 18c pikeman18 protection +3 (lvl 3) | 3 | 3 | 15.62 | 7000 | 0 | 0 | 1500 | 0 | 0 |
| `denba2.pikeman18.2.3` | Barracks 18c pikeman18 protection +2 (lvl 4) | 4 | 2 | 15.62 | 37000 | 0 | 0 | 2000 | 0 | 0 |
| `denba2.pikeman18.2.4` | Barracks 18c pikeman18 protection +3 (lvl 5) | 5 | 3 | 15.62 | 37000 | 0 | 0 | 5500 | 0 | 0 |
| `denba2.pikeman18.2.5` | Barracks 18c pikeman18 protection +2 (lvl 6) | 6 | 2 | 15.62 | 37000 | 0 | 0 | 5500 | 0 | 0 |
| `denba2.pikeman18.2.6` | Barracks 18c pikeman18 protection +3 (lvl 7) | 7 | 3 | 15.62 | 64600 | 0 | 0 | 5500 | 0 | 0 |
| `denbar.1` | — | 1 | 140 | 15.62 | 750 | 0 | 0 | 250 | 0 | 0 |
| `denbar.2` | — | 2 | 180 | 15.62 | 25600 | 0 | 0 | 3350 | 2000 | 0 |
| `denbar.drummer.2.1` | Barracks 17c drummer protection +12 (lvl 2) | 2 | 12 | 15.62 | 1205 | 0 | 0 | 90 | 0 | 0 |
| `denbar.musketeer.1.1` | Barracks 17c musketeer damage +1 (lvl 2) | 2 | 1 | 15.62 | 2000 | 0 | 0 | 100 | 0 | 0 |
| `denbar.musketeer.1.2` | Barracks 17c musketeer damage +1 (lvl 3) | 3 | 1 | 15.62 | 1000 | 0 | 0 | 300 | 0 | 0 |
| `denbar.musketeer.1.3` | Barracks 17c musketeer damage +2 (lvl 4) | 4 | 2 | 15.62 | 500 | 0 | 0 | 700 | 0 | 0 |
| `denbar.musketeer.2.1` | Barracks 17c musketeer protection +1 (lvl 2) | 2 | 1 | 15.62 | 170 | 0 | 0 | 50 | 100 | 0 |
| `denbar.musketeer.2.2` | Barracks 17c musketeer protection +2 (lvl 3) | 3 | 2 | 15.62 | 405 | 0 | 0 | 150 | 200 | 0 |
| `denbar.musketeer.2.3` | Barracks 17c musketeer protection +2 (lvl 4) | 4 | 2 | 15.62 | 1570 | 0 | 0 | 100 | 350 | 0 |
| `denbar.musketeer.2.4` | Barracks 17c musketeer protection +1 (lvl 5) | 5 | 1 | 15.62 | 1556 | 0 | 0 | 550 | 100 | 0 |
| `denbar.musketeer.2.5` | Barracks 17c musketeer protection +2 (lvl 6) | 6 | 2 | 15.62 | 1060 | 0 | 0 | 850 | 400 | 0 |
| `denbar.musketeer.2.6` | Barracks 17c musketeer protection +2 (lvl 7) | 7 | 2 | 15.62 | 3700 | 0 | 0 | 450 | 700 | 0 |
| `denbar.officer.1.1` | Barracks 17c officer damage +20 (lvl 2) | 2 | 20 | 15.62 | 150 | 0 | 0 | 25 | 0 | 0 |
| `denbar.officer.2.1` | Barracks 17c officer protection +6 (lvl 2) | 2 | 6 | 15.62 | 1650 | 0 | 0 | 395 | 0 | 0 |
| `denbar.pikeman.1.1` | Barracks 17c pikeman damage +1 (lvl 2) | 2 | 1 | 15.62 | 3600 | 0 | 0 | 450 | 0 | 0 |
| `denbar.pikeman.1.2` | Barracks 17c pikeman damage +2 (lvl 3) | 3 | 2 | 15.62 | 1300 | 0 | 0 | 300 | 0 | 0 |
| `denbar.pikeman.1.3` | Barracks 17c pikeman damage +2 (lvl 4) | 4 | 2 | 15.62 | 200 | 0 | 0 | 50 | 0 | 0 |
| `denbar.pikeman.1.4` | Barracks 17c pikeman damage +1 (lvl 5) | 5 | 1 | 15.62 | 6800 | 0 | 0 | 1950 | 0 | 0 |
| `denbar.pikeman.1.5` | Barracks 17c pikeman damage +2 (lvl 6) | 6 | 2 | 15.62 | 15030 | 0 | 0 | 2300 | 0 | 0 |
| `denbar.pikeman.1.6` | — | 7 | 2 | 15.62 | 15000 | 0 | 0 | 1875 | 0 | 0 |
| `denbar.pikeman.2.1` | Barracks 17c pikeman protection +1 (lvl 2) | 2 | 1 | 15.62 | 175 | 0 | 0 | 40 | 0 | 0 |
| `denbar.pikeman.2.2` | Barracks 17c pikeman protection +1 (lvl 3) | 3 | 1 | 15.62 | 990 | 0 | 0 | 275 | 0 | 0 |
| `denbar.pikeman.2.3` | Barracks 17c pikeman protection +2 (lvl 4) | 4 | 2 | 15.62 | 4700 | 0 | 0 | 280 | 0 | 0 |
| `denbar.pikeman.2.4` | Barracks 17c pikeman protection +1 (lvl 5) | 5 | 1 | 15.62 | 9005 | 0 | 0 | 707 | 0 | 0 |
| `denbar.pikeman.2.5` | Barracks 17c pikeman protection +1 (lvl 6) | 6 | 1 | 15.62 | 17510 | 0 | 0 | 2950 | 0 | 0 |
| `denbar.pikeman.2.6` | — | 7 | 2 | 15.62 | 11250 | 0 | 0 | 1500 | 0 | 0 |
| `denbla.1` | Manufacture agricultural equipment (field capacity +100%) | 1 | 100 | 15.62 | 0 | 400 | 0 | 90 | 0 | 0 |
| `denbla.2` | Forge metal armature and gratings (building defence +50) | 1 | 50 | 15.62 | 0 | 0 | 12320 | 350 | 900 | 0 |
| `denbla.3` | Forge harnesses for horses (mounted units recruitment speed -33%) | 1 | -3333333 | 15.62 | 0 | 0 | 0 | 3650 | 5300 | 8200 |
| `denbla.4` | Forge bayonets and broadswords for infantry (18c musketeer/grenadier melee attack +5) | 1 | 5 | 15.62 | 0 | 1300 | 0 | 1500 | 900 | 5000 |
| `denbla.5` | Forge new types of broadswords and sabres (cavalry and sword clansman attack +5) | 1 | 5 | 15.62 | 0 | 0 | 0 | 4000 | 7900 | 0 |
| `denbla.6` | Forge new cuirasses (armoured soldiers defence +2) | 1 | 2 | 15.62 | 0 | 0 | 0 | 4950 | 10500 | 0 |
| `dencen.1` | — | 1 | 0 | 9.38 | 20000 | 0 | 0 | 6500 | 1100 | 1100 |
| `densta.cuirassier.1.1` | Stable cuirassier damage +1 (lvl 2) | 2 | 1 | 15.62 | 10000 | 0 | 0 | 200 | 0 | 0 |
| `densta.cuirassier.1.2` | Stable cuirassier damage +1 (lvl 3) | 3 | 1 | 15.62 | 34000 | 0 | 0 | 1700 | 0 | 0 |
| `densta.cuirassier.1.3` | Stable cuirassier damage +1 (lvl 4) | 4 | 1 | 15.62 | 64000 | 0 | 0 | 2100 | 0 | 0 |
| `densta.cuirassier.1.4` | Stable cuirassier damage +2 (lvl 5) | 5 | 2 | 15.62 | 58000 | 0 | 0 | 4150 | 0 | 0 |
| `densta.cuirassier.1.5` | Stable cuirassier damage +2 (lvl 6) | 6 | 2 | 15.62 | 59055 | 0 | 0 | 3100 | 0 | 0 |
| `densta.cuirassier.1.6` | Stable cuirassier damage +3 (lvl 7) | 7 | 3 | 15.62 | 47050 | 0 | 0 | 8150 | 0 | 0 |
| `densta.cuirassier.2.1` | Stable cuirassier protection +2 (lvl 2) | 2 | 2 | 15.62 | 1520 | 0 | 0 | 450 | 1000 | 0 |
| `densta.cuirassier.2.2` | Stable cuirassier protection +3 (lvl 3) | 3 | 3 | 15.62 | 7000 | 0 | 0 | 750 | 2000 | 0 |
| `densta.cuirassier.2.3` | Stable cuirassier protection +3 (lvl 4) | 4 | 3 | 15.62 | 3600 | 0 | 0 | 3300 | 3050 | 0 |
| `densta.cuirassier.2.4` | Stable cuirassier protection +2 (lvl 5) | 5 | 2 | 15.62 | 8700 | 0 | 0 | 3200 | 200 | 0 |
| `densta.cuirassier.2.5` | Stable cuirassier protection +1 (lvl 6) | 6 | 1 | 15.62 | 8700 | 0 | 0 | 2650 | 4300 | 0 |
| `densta.cuirassier.2.6` | Stable cuirassier protection +1 (lvl 7) | 7 | 1 | 15.62 | 11200 | 0 | 0 | 4700 | 6760 | 0 |
| `densta.dragoon.1.1` | Stable dragoon damage +1 (lvl 2) | 2 | 1 | 15.62 | 700 | 0 | 0 | 250 | 0 | 0 |
| `densta.dragoon.1.2` | Stable dragoon damage +1 (lvl 3) | 3 | 1 | 15.62 | 500 | 0 | 0 | 100 | 0 | 0 |
| `densta.dragoon.1.3` | Stable dragoon damage +2 (lvl 4) | 4 | 2 | 15.62 | 900 | 0 | 0 | 640 | 0 | 0 |
| `densta.dragoon.1.4` | Stable dragoon damage +1 (lvl 5) | 5 | 1 | 15.62 | 0 | 0 | 0 | 0 | 0 | 0 |
| `densta.dragoon.1.5` | Stable dragoon damage +1 (lvl 6) | 6 | 1 | 15.62 | 0 | 0 | 0 | 0 | 0 | 0 |
| `densta.dragoon.1.6` | Stable dragoon damage +3 (lvl 7) | 7 | 3 | 15.62 | 0 | 0 | 0 | 0 | 0 | 0 |
| `densta.dragoon.2.1` | Stable dragoon protection +1 (lvl 2) | 2 | 1 | 15.62 | 500 | 0 | 0 | 250 | 0 | 0 |
| `densta.dragoon.2.2` | Stable dragoon protection +2 (lvl 3) | 3 | 2 | 15.62 | 6300 | 0 | 0 | 850 | 0 | 0 |
| `densta.dragoon.2.3` | Stable dragoon protection +2 (lvl 4) | 4 | 2 | 15.62 | 4600 | 0 | 0 | 1350 | 0 | 0 |
| `densta.dragoon.2.4` | Stable dragoon protection +1 (lvl 5) | 5 | 1 | 15.62 | 2500 | 0 | 0 | 750 | 0 | 0 |
| `densta.dragoon.2.5` | Stable dragoon protection +2 (lvl 6) | 6 | 2 | 15.62 | 800 | 0 | 0 | 2750 | 0 | 0 |
| `densta.dragoon.2.6` | Stable dragoon protection +2 (lvl 7) | 7 | 2 | 15.62 | 2001 | 0 | 0 | 8200 | 0 | 0 |
| `densta.dragoon18.1.1` | Stable dragoon18 damage +2 (lvl 2) | 2 | 2 | 15.62 | 4500 | 0 | 0 | 200 | 0 | 0 |
| `densta.dragoon18.1.2` | Stable dragoon18 damage +2 (lvl 3) | 3 | 2 | 15.62 | 5500 | 0 | 0 | 250 | 0 | 0 |
| `densta.dragoon18.1.3` | Stable dragoon18 damage +4 (lvl 4) | 4 | 4 | 15.62 | 22000 | 0 | 0 | 500 | 0 | 0 |
| `densta.dragoon18.1.4` | Stable dragoon18 damage +2 (lvl 5) | 5 | 2 | 15.62 | 13000 | 0 | 0 | 480 | 0 | 0 |
| `densta.dragoon18.1.5` | Stable dragoon18 damage +2 (lvl 6) | 6 | 2 | 15.62 | 42000 | 0 | 0 | 780 | 0 | 0 |
| `densta.dragoon18.1.6` | Stable dragoon18 damage +4 (lvl 7) | 7 | 4 | 15.62 | 32000 | 0 | 0 | 680 | 0 | 0 |
| `densta.dragoon18.2.1` | Stable dragoon18 protection +1 (lvl 2) | 2 | 1 | 15.62 | 750 | 0 | 0 | 935 | 0 | 0 |
| `densta.dragoon18.2.2` | Stable dragoon18 protection +1 (lvl 3) | 3 | 1 | 15.62 | 1260 | 0 | 0 | 1150 | 0 | 0 |
| `densta.dragoon18.2.3` | Stable dragoon18 protection +2 (lvl 4) | 4 | 2 | 15.62 | 10600 | 0 | 0 | 2350 | 0 | 0 |
| `densta.dragoon18.2.4` | Stable dragoon18 protection +1 (lvl 5) | 5 | 1 | 15.62 | 22600 | 0 | 0 | 5350 | 0 | 0 |
| `densta.dragoon18.2.5` | Stable dragoon18 protection +2 (lvl 6) | 6 | 2 | 15.62 | 19600 | 0 | 0 | 3350 | 0 | 0 |
| `densta.dragoon18.2.6` | Stable dragoon18 protection +3 (lvl 7) | 7 | 3 | 15.62 | 15760 | 0 | 0 | 9350 | 0 | 0 |
| `densta.hussar.1.1` | Stable hussar damage +1 (lvl 2) | 2 | 1 | 15.62 | 0 | 0 | 0 | 2800 | 1600 | 0 |
| `densta.hussar.1.2` | Stable hussar damage +2 (lvl 3) | 3 | 2 | 15.62 | 0 | 0 | 0 | 2800 | 1400 | 0 |
| `densta.hussar.1.3` | Stable hussar damage +3 (lvl 4) | 4 | 3 | 15.62 | 10200 | 0 | 0 | 0 | 4000 | 0 |
| `densta.hussar.1.4` | Stable hussar damage +4 (lvl 5) | 5 | 4 | 15.62 | 42000 | 0 | 0 | 0 | 2000 | 0 |
| `densta.hussar.1.5` | Stable hussar damage +1 (lvl 6) | 6 | 1 | 15.62 | 29200 | 0 | 0 | 0 | 5500 | 0 |
| `densta.hussar.1.6` | Stable hussar damage +1 (lvl 7) | 7 | 1 | 15.62 | 40000 | 0 | 0 | 0 | 4000 | 0 |
| `densta.hussar.2.1` | Stable hussar protection +1 (lvl 2) | 2 | 1 | 15.62 | 150 | 0 | 0 | 1250 | 0 | 0 |
| `densta.hussar.2.2` | Stable hussar protection +1 (lvl 3) | 3 | 1 | 15.62 | 3200 | 0 | 0 | 2450 | 0 | 0 |
| `densta.hussar.2.3` | Stable hussar protection +1 (lvl 4) | 4 | 1 | 15.62 | 3600 | 0 | 0 | 3350 | 0 | 0 |
| `densta.hussar.2.4` | Stable hussar protection +2 (lvl 5) | 5 | 2 | 15.62 | 6000 | 0 | 0 | 10350 | 0 | 0 |
| `densta.hussar.2.5` | Stable hussar protection +2 (lvl 6) | 6 | 2 | 15.62 | 9000 | 0 | 0 | 13350 | 0 | 0 |
| `densta.hussar.2.6` | Stable hussar protection +3 (lvl 7) | 7 | 3 | 15.62 | 48000 | 0 | 0 | 22150 | 0 | 0 |
| `densta.reiter.1.1` | Stable reiter damage +1 (lvl 2) | 2 | 1 | 15.62 | 800 | 0 | 0 | 100 | 0 | 0 |
| `densta.reiter.1.2` | Stable reiter damage +2 (lvl 3) | 3 | 2 | 15.62 | 800 | 0 | 0 | 220 | 0 | 0 |
| `densta.reiter.1.3` | Stable reiter damage +1 (lvl 4) | 4 | 1 | 15.62 | 2400 | 0 | 0 | 380 | 0 | 0 |
| `densta.reiter.1.4` | Stable reiter damage +1 (lvl 5) | 5 | 1 | 15.62 | 4250 | 0 | 0 | 220 | 0 | 0 |
| `densta.reiter.1.5` | Stable reiter damage +1 (lvl 6) | 6 | 1 | 15.62 | 4030 | 0 | 0 | 900 | 0 | 0 |
| `densta.reiter.1.6` | Stable reiter damage +1 (lvl 7) | 7 | 1 | 15.62 | 6000 | 0 | 0 | 1600 | 0 | 0 |
| `densta.reiter.2.1` | Stable reiter protection +2 (lvl 2) | 2 | 2 | 15.62 | 200 | 0 | 0 | 135 | 400 | 0 |
| `densta.reiter.2.2` | Stable reiter protection +3 (lvl 3) | 3 | 3 | 15.62 | 600 | 0 | 0 | 100 | 300 | 0 |
| `densta.reiter.2.3` | Stable reiter protection +3 (lvl 4) | 4 | 3 | 15.62 | 800 | 0 | 0 | 200 | 560 | 0 |
| `densta.reiter.2.4` | Stable reiter protection +2 (lvl 5) | 5 | 2 | 15.62 | 1600 | 0 | 0 | 300 | 340 | 0 |
| `densta.reiter.2.5` | Stable reiter protection +1 (lvl 6) | 6 | 1 | 15.62 | 2200 | 0 | 0 | 350 | 600 | 0 |
| `densta.reiter.2.6` | Stable reiter protection +1 (lvl 7) | 7 | 1 | 15.62 | 17000 | 0 | 0 | 950 | 5200 | 0 |
| `eurcoa.1` | — | 2 | 5 | 9.38 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `eurcoa.2` | — | 3 | 8 | 9.38 | 5250 | 0 | 0 | 4950 | 0 | 0 |
| `eurcoa.3` | — | 4 | 10 | 9.38 | 12500 | 0 | 0 | 9250 | 0 | 0 |
| `eurcoa.4` | — | 5 | 12 | 9.38 | 15800 | 0 | 0 | 18500 | 0 | 0 |
| `eurcoa.5` | — | 6 | 15 | 9.38 | 19800 | 0 | 0 | 21050 | 0 | 0 |
| `eurcoa.6` | — | 7 | 40 | 9.38 | 50200 | 0 | 0 | 25950 | 0 | 0 |
| `eurgol.1` | — | 2 | 5 | 9.38 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `eurgol.2` | — | 3 | 8 | 9.38 | 5250 | 0 | 0 | 4950 | 0 | 0 |
| `eurgol.3` | — | 4 | 10 | 9.38 | 12500 | 0 | 0 | 9250 | 0 | 0 |
| `eurgol.4` | — | 5 | 12 | 9.38 | 15800 | 0 | 0 | 18500 | 0 | 0 |
| `eurgol.5` | — | 6 | 15 | 9.38 | 19800 | 0 | 0 | 21050 | 0 | 0 |
| `eurgol.6` | — | 7 | 40 | 9.38 | 50200 | 0 | 0 | 25950 | 0 | 0 |
| `euriro.1` | — | 2 | 5 | 9.38 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `euriro.2` | — | 3 | 8 | 9.38 | 5250 | 0 | 0 | 4950 | 0 | 0 |
| `euriro.3` | — | 4 | 10 | 9.38 | 12500 | 0 | 0 | 9250 | 0 | 0 |
| `euriro.4` | — | 5 | 12 | 9.38 | 15800 | 0 | 0 | 18500 | 0 | 0 |
| `euriro.5` | — | 6 | 15 | 9.38 | 19800 | 0 | 0 | 21050 | 0 | 0 |
| `euriro.6` | — | 7 | 40 | 9.38 | 50200 | 0 | 0 | 25950 | 0 | 0 |
| `eurpor.1` | — | 1 | 50 | 46.88 | 0 | 20000 | 0 | 1500 | 0 | 0 |
| `eurswa.1` | — | 2 | 5 | 0.03 | 0 | 0 | 500 | 0 | 0 | 0 |
| `eurtow.1` | — | 2 | -20 | 31.25 | 0 | 0 | 0 | 250 | 0 | 0 |
| `eurtow.2` | — | 3 | -20 | 31.25 | 0 | 0 | 0 | 0 | 350 | 0 |
| `eurtow.3` | — | 4 | -10 | 31.25 | 0 | 0 | 0 | 0 | 0 | 400 |
| `eurtow.4` | — | 5 | -10 | 31.25 | 0 | 0 | 0 | 0 | 450 | 0 |
| `eurtow.5` | — | 6 | -10 | 31.25 | 0 | 0 | 0 | 0 | 0 | 500 |
| `ferry.1` | Improve transport vessel design (+%value% capacity) | 2 | 200 | 15.62 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `ukrwwa.1` | — | 2 | 5 | 0.03 | 0 | 400 | 0 | 0 | 0 | 0 |

### por — Portugal

| sid | имя (EN) | level | value | время (s) | F | W | S | G | I | C |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `eurcoa.1` | — | 2 | 5 | 9.38 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `eurcoa.2` | — | 3 | 8 | 9.38 | 5250 | 0 | 0 | 4950 | 0 | 0 |
| `eurcoa.3` | — | 4 | 10 | 9.38 | 12500 | 0 | 0 | 9250 | 0 | 0 |
| `eurcoa.4` | — | 5 | 12 | 9.38 | 15800 | 0 | 0 | 18500 | 0 | 0 |
| `eurcoa.5` | — | 6 | 15 | 9.38 | 19800 | 0 | 0 | 21050 | 0 | 0 |
| `eurcoa.6` | — | 7 | 40 | 9.38 | 50200 | 0 | 0 | 25950 | 0 | 0 |
| `eurgol.1` | — | 2 | 5 | 9.38 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `eurgol.2` | — | 3 | 8 | 9.38 | 5250 | 0 | 0 | 4950 | 0 | 0 |
| `eurgol.3` | — | 4 | 10 | 9.38 | 12500 | 0 | 0 | 9250 | 0 | 0 |
| `eurgol.4` | — | 5 | 12 | 9.38 | 15800 | 0 | 0 | 18500 | 0 | 0 |
| `eurgol.5` | — | 6 | 15 | 9.38 | 19800 | 0 | 0 | 21050 | 0 | 0 |
| `eurgol.6` | — | 7 | 40 | 9.38 | 50200 | 0 | 0 | 25950 | 0 | 0 |
| `euriro.1` | — | 2 | 5 | 9.38 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `euriro.2` | — | 3 | 8 | 9.38 | 5250 | 0 | 0 | 4950 | 0 | 0 |
| `euriro.3` | — | 4 | 10 | 9.38 | 12500 | 0 | 0 | 9250 | 0 | 0 |
| `euriro.4` | — | 5 | 12 | 9.38 | 15800 | 0 | 0 | 18500 | 0 | 0 |
| `euriro.5` | — | 6 | 15 | 9.38 | 19800 | 0 | 0 | 21050 | 0 | 0 |
| `euriro.6` | — | 7 | 40 | 9.38 | 50200 | 0 | 0 | 25950 | 0 | 0 |
| `eurswa.1` | — | 2 | 5 | 0.03 | 0 | 0 | 500 | 0 | 0 | 0 |
| `eurtow.1` | — | 2 | -20 | 31.25 | 0 | 0 | 0 | 250 | 0 | 0 |
| `eurtow.2` | — | 3 | -20 | 31.25 | 0 | 0 | 0 | 0 | 350 | 0 |
| `eurtow.3` | — | 4 | -10 | 31.25 | 0 | 0 | 0 | 0 | 0 | 400 |
| `eurtow.4` | — | 5 | -10 | 31.25 | 0 | 0 | 0 | 0 | 450 | 0 |
| `eurtow.5` | — | 6 | -10 | 31.25 | 0 | 0 | 0 | 0 | 0 | 500 |
| `ferry.1` | Improve transport vessel design (+%value% capacity) | 2 | 200 | 15.62 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `poraca.1` | Cultivate new cultures of wheat (harvesting +40%) | 1 | 40 | 15.62 | 0 | 200 | 0 | 325 | 0 | 0 |
| `poraca.10` | Raise builders' salary (building construction time -75%) | 1 | -7500000 | 15.62 | 0 | 0 | 0 | 6950 | 0 | 0 |
| `poraca.11` | Research new fortification grades (durability of walls and towers +80) | 1 | 80 | 15.62 | 0 | 0 | 16200 | 1500 | 0 | 0 |
| `poraca.12` | Improve firearms: rifled barrel (fire power +10%) | 1 | 10 | 15.62 | 0 | 0 | 0 | 0 | 5000 | 0 |
| `poraca.13` | Research granular gunpowder (fire power +10%) | 1 | 10 | 15.62 | 0 | 0 | 0 | 4000 | 0 | 0 |
| `poraca.14` | Research new sulphur purification methods (fire power +15%) | 1 | 15 | 15.62 | 0 | 0 | 0 | 7000 | 0 | 0 |
| `poraca.15` | Research new nitre purification methods (fire power +25%) | 1 | 25 | 15.62 | 0 | 0 | 0 | 0 | 0 | 11000 |
| `poraca.16` | Research improved additions to gunpowder formula (artillery range +5%) | 1 | 5 | 15.62 | 0 | 0 | 0 | 2000 | 12150 | 0 |
| `poraca.17` | Design new barrel types: unicorn, carronade (artillery range +10%) | 1 | 10 | 15.62 | 0 | 0 | 3000 | 4550 | 19200 | 0 |
| `poraca.18` | Design more durable gun carriage: Gribovalle system (artillery durability +50%) | 1 | 50 | 15.62 | 0 | 0 | 0 | 500 | 3830 | 1500 |
| `poraca.19` | Design multi-barrelled cannon | 1 | 0 | 15.62 | 0 | 0 | 0 | 1500 | 0 | 2500 |
| `poraca.2` | Cultivate new cultures of rye (harvesting +50%) | 1 | 50 | 15.62 | 0 | 2400 | 0 | 625 | 0 | 0 |
| `poraca.20` | Research new sighting devices for artillery (artillery accuracy +35%) | 1 | -35 | 15.62 | 0 | 3540 | 0 | 2000 | 0 | 7250 |
| `poraca.21` | Finance artillery repair shops (repair all artillery) | 1 | 25 | 15.62 | 0 | 350 | 0 | 100 | 0 | 250 |
| `poraca.22` | Develop geology (previously hidden deposits appear on the map) | 1 | 0 | 15.62 | 0 | 0 | 0 | 250 | 0 | 0 |
| `poraca.23` | Develop mining (stone excavation efficiency +100%) | 1 | 100 | 15.62 | 0 | 0 | 0 | 1550 | 3000 | 0 |
| `poraca.24` | Raise miners' salary (stone excavation efficiency +200%) | 1 | 200 | 15.62 | 4200 | 0 | 0 | 1550 | 0 | 12520 |
| `poraca.25` | Design Montgolfier (reveals the whole map) | 1 | 0 | 15.62 | 0 | 0 | 0 | 5750 | 0 | 0 |
| `poraca.26` | Develop medical science (heals all live units) | 1 | 50 | 31.25 | 0 | 0 | 0 | 200 | 0 | 200 |
| `poraca.27` | Develop mathematics (artillery accuracy +35%) | 1 | -35 | 15.62 | 0 | 9540 | 0 | 12000 | 0 | 65200 |
| `poraca.28` | Design new rigging types (ship speed +40%) | 1 | 40 | 15.62 | 0 | 65400 | 0 | 24050 | 0 | 0 |
| `poraca.29` | Design new rib system and new hulls (battleship construction) | 1 | 0 | 15.62 | 0 | 32300 | 0 | 6800 | 9000 | 12800 |
| `poraca.3` | Raise agriculturists' salary (harvesting +50%) | 1 | 50 | 15.62 | 0 | 3600 | 0 | 850 | 0 | 0 |
| `poraca.30` | Train carpenters (shipbuilding speed x10) | 1 | -5000000 | 15.62 | 0 | 2300 | 42700 | 1150 | 0 | 0 |
| `poraca.31` | Design wheellock (rate of fire +30%) | 1 | -30 | 15.62 | 0 | 0 | 6000 | 5500 | 4200 | 0 |
| `poraca.32` | Design flintlock (musket cost -50%) | 1 | 0 | 15.62 | 0 | 0 | 0 | 6050 | 0 | 7750 |
| `poraca.33` | Design paper cartridge and iron ramrod (rate of fire +30%) | 1 | -30 | 15.62 | 0 | 5000 | 0 | 5500 | 0 | 15200 |
| `poraca.34` | Research improved steel grades for cuirasses (armoured soldier defence +2) | 1 | 2 | 15.62 | 0 | 0 | 0 | 9750 | 0 | 0 |
| `poraca.35` | Design bayonet: barrel-inserted, bayonet with a tube (cold steel weapons +5) | 1 | 5 | 15.62 | 0 | 0 | 0 | 11500 | 0 | 0 |
| `poraca.36` | Research new steel grades (18c musketeer/grenadier melee attack efficiency +25%) | 1 | 25 | 15.62 | 0 | 0 | 0 | 19500 | 0 | 0 |
| `poraca.4` | Carry out field melioration (field capacity +200%) | 1 | 200 | 15.62 | 0 | 1000 | 0 | 475 | 0 | 0 |
| `poraca.5` | Design new tackle and fishing nets (boat efficiency +100%) | 1 | 100 | 15.62 | 0 | 12400 | 0 | 2520 | 0 | 0 |
| `poraca.6` | Develop new woodworking methods (frigate building) | 1 | 0 | 15.62 | 0 | 12400 | 0 | 7040 | 0 | 0 |
| `poraca.7` | Build new shipyards for fishing boats (fishing boat cost -85%) | 1 | 0 | 15.62 | 0 | 7300 | 0 | 1220 | 0 | 0 |
| `poraca.8` | Design new woodworking tools (woodcutting efficiency +100%) | 1 | 100 | 15.62 | 5500 | 0 | 0 | 550 | 0 | 0 |
| `poraca.9` | Use new construction materials (durability of buildings +85) | 1 | 85 | 15.62 | 0 | 9400 | 7850 | 1150 | 0 | 0 |
| `porart.cannon.1.1` | — | 2 | — | 10.0 | 0 | 1000 | 500 | 300 | 0 | 0 |
| `porart.cannon.1.2` | — | 3 | — | 10.0 | 0 | 3000 | 1000 | 500 | 0 | 0 |
| `porart.cannon.1.3` | — | 4 | — | 10.0 | 0 | 6000 | 2000 | 1000 | 0 | 0 |
| `porart.cannon.1.4` | — | 5 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `porart.cannon.1.5` | — | 6 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `porart.cannon.1.6` | — | 7 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `porart.cannon.2.1` | — | 2 | -2500000 | 10.0 | 0 | 0 | 0 | 500 | 1000 | 0 |
| `porart.cannon.2.2` | — | 3 | -2500000 | 10.0 | 0 | 0 | 0 | 1000 | 2000 | 0 |
| `porart.cannon.2.3` | — | 4 | -2500000 | 10.0 | 0 | 0 | 0 | 2000 | 3000 | 0 |
| `porart.cannon.2.4` | — | 5 | -2000000 | 15.62 | 2560 | 0 | 0 | 0 | 0 | 0 |
| `porart.cannon.2.5` | — | 6 | -2000000 | 15.62 | 3560 | 0 | 0 | 0 | 0 | 0 |
| `porart.cannon.2.6` | — | 7 | -2000000 | 15.62 | 5560 | 0 | 0 | 0 | 0 | 0 |
| `porart.howitzer.1.1` | — | 2 | — | 10.0 | 0 | 1000 | 500 | 300 | 0 | 0 |
| `porart.howitzer.1.2` | — | 3 | — | 10.0 | 0 | 3000 | 1000 | 500 | 0 | 0 |
| `porart.howitzer.1.3` | — | 4 | — | 10.0 | 0 | 6000 | 2000 | 1000 | 0 | 0 |
| `porart.howitzer.1.4` | — | 5 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `porart.howitzer.1.5` | — | 6 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `porart.howitzer.1.6` | — | 7 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `porart.howitzer.2.1` | — | 2 | -2500000 | 10.0 | 0 | 0 | 0 | 500 | 1000 | 0 |
| `porart.howitzer.2.2` | — | 3 | -2500000 | 10.0 | 0 | 0 | 0 | 1000 | 2000 | 0 |
| `porart.howitzer.2.3` | — | 4 | -2500000 | 10.0 | 0 | 0 | 0 | 2000 | 3000 | 0 |
| `porart.howitzer.2.4` | — | 5 | -2000000 | 31.25 | 2560 | 0 | 0 | 0 | 0 | 0 |
| `porart.howitzer.2.5` | — | 6 | -2000000 | 31.25 | 3560 | 0 | 0 | 0 | 0 | 0 |
| `porart.howitzer.2.6` | — | 7 | -2000000 | 31.25 | 5560 | 0 | 0 | 0 | 0 | 0 |
| `porba2.drummer18.2.1` | Barracks 18c drummer18 protection +15 (lvl 2) | 2 | 15 | 15.62 | 205 | 0 | 0 | 90 | 0 | 0 |
| `porba2.grenadier.1.1` | Barracks 18c grenadier damage +2 (lvl 2) | 2 | 2 | 15.62 | 2000 | 0 | 0 | 800 | 0 | 0 |
| `porba2.grenadier.1.2` | Barracks 18c grenadier damage +3 (lvl 3) | 3 | 3 | 15.62 | 12000 | 0 | 0 | 1800 | 0 | 0 |
| `porba2.grenadier.1.3` | Barracks 18c grenadier damage +4 (lvl 4) | 4 | 4 | 15.62 | 32000 | 0 | 0 | 2800 | 0 | 0 |
| `porba2.grenadier.1.4` | Barracks 18c grenadier damage +5 (lvl 5) | 5 | 5 | 15.62 | 42000 | 0 | 0 | 3800 | 0 | 0 |
| `porba2.grenadier.1.5` | Barracks 18c grenadier damage +6 (lvl 6) | 6 | 6 | 15.62 | 52000 | 0 | 0 | 4800 | 0 | 0 |
| `porba2.grenadier.1.6` | Barracks 18c grenadier damage +1500 (lvl 7) | 7 | 1500 | 15.62 | 62000 | 0 | 0 | 15800 | 0 | 0 |
| `porba2.grenadier.2.1` | Barracks 18c grenadier protection +1 (lvl 2) | 2 | 1 | 15.62 | 3706 | 0 | 0 | 350 | 0 | 0 |
| `porba2.grenadier.2.2` | Barracks 18c grenadier protection +2 (lvl 3) | 3 | 2 | 15.62 | 11030 | 0 | 0 | 1350 | 0 | 0 |
| `porba2.grenadier.2.3` | Barracks 18c grenadier protection +3 (lvl 4) | 4 | 3 | 15.62 | 35706 | 0 | 0 | 3000 | 0 | 0 |
| `porba2.grenadier.2.4` | Barracks 18c grenadier protection +1 (lvl 5) | 5 | 1 | 15.62 | 36556 | 0 | 0 | 3350 | 0 | 0 |
| `porba2.grenadier.2.5` | Barracks 18c grenadier protection +2 (lvl 6) | 6 | 2 | 15.62 | 30060 | 0 | 0 | 1350 | 0 | 0 |
| `porba2.grenadier.2.6` | Barracks 18c grenadier protection +3 (lvl 7) | 7 | 3 | 15.62 | 64000 | 0 | 0 | 1350 | 0 | 0 |
| `porba2.jagerpor.1.1` | Barracks 18c jagerpor damage +1 (lvl 2) | 2 | 1 | 15.62 | 3000 | 0 | 0 | 750 | 0 | 0 |
| `porba2.jagerpor.1.2` | Barracks 18c jagerpor damage +1 (lvl 3) | 3 | 1 | 15.62 | 4000 | 0 | 0 | 1100 | 0 | 0 |
| `porba2.jagerpor.1.3` | Barracks 18c jagerpor damage +1 (lvl 4) | 4 | 1 | 15.62 | 7000 | 0 | 0 | 1800 | 0 | 0 |
| `porba2.jagerpor.1.4` | Barracks 18c jagerpor damage +1 (lvl 5) | 5 | 1 | 15.62 | 12000 | 0 | 0 | 350 | 0 | 0 |
| `porba2.jagerpor.1.5` | Barracks 18c jagerpor damage +1 (lvl 6) | 6 | 1 | 15.62 | 32020 | 0 | 0 | 850 | 0 | 0 |
| `porba2.jagerpor.1.6` | Barracks 18c jagerpor damage +1 (lvl 7) | 7 | 1 | 15.62 | 45200 | 0 | 0 | 1330 | 0 | 0 |
| `porba2.jagerpor.2.1` | Barracks 18c jagerpor protection +1 (lvl 2) | 2 | 1 | 15.62 | 3706 | 0 | 0 | 350 | 0 | 0 |
| `porba2.jagerpor.2.2` | Barracks 18c jagerpor protection +1 (lvl 3) | 3 | 1 | 15.62 | 12060 | 0 | 0 | 1350 | 0 | 0 |
| `porba2.jagerpor.2.3` | Barracks 18c jagerpor protection +1 (lvl 4) | 4 | 1 | 15.62 | 36706 | 0 | 0 | 2250 | 0 | 0 |
| `porba2.jagerpor.2.4` | Barracks 18c jagerpor protection +1 (lvl 5) | 5 | 1 | 15.62 | 36706 | 0 | 0 | 3350 | 0 | 0 |
| `porba2.jagerpor.2.5` | Barracks 18c jagerpor protection +1 (lvl 6) | 6 | 1 | 15.62 | 37060 | 0 | 0 | 1350 | 0 | 0 |
| `porba2.jagerpor.2.6` | Barracks 18c jagerpor protection +1 (lvl 7) | 7 | 1 | 15.62 | 16706 | 0 | 0 | 1350 | 0 | 0 |
| `porba2.musketeer18.1.1` | Barracks 18c musketeer18 damage +1 (lvl 2) | 2 | 1 | 15.62 | 1000 | 0 | 0 | 800 | 0 | 0 |
| `porba2.musketeer18.1.2` | Barracks 18c musketeer18 damage +1 (lvl 3) | 3 | 1 | 15.62 | 1500 | 0 | 0 | 800 | 0 | 0 |
| `porba2.musketeer18.1.3` | Barracks 18c musketeer18 damage +2 (lvl 4) | 4 | 2 | 15.62 | 2000 | 0 | 0 | 800 | 0 | 0 |
| `porba2.musketeer18.1.4` | Barracks 18c musketeer18 damage +2 (lvl 5) | 5 | 2 | 15.62 | 2500 | 0 | 0 | 800 | 0 | 0 |
| `porba2.musketeer18.1.5` | Barracks 18c musketeer18 damage +3 (lvl 6) | 6 | 3 | 15.62 | 3000 | 0 | 0 | 800 | 0 | 0 |
| `porba2.musketeer18.1.6` | Barracks 18c musketeer18 damage +3 (lvl 7) | 7 | 3 | 15.62 | 3500 | 0 | 0 | 800 | 0 | 0 |
| `porba2.musketeer18.2.1` | Barracks 18c musketeer18 protection +1 (lvl 2) | 2 | 1 | 15.62 | 3706 | 0 | 0 | 350 | 0 | 0 |
| `porba2.musketeer18.2.2` | Barracks 18c musketeer18 protection +2 (lvl 3) | 3 | 2 | 15.62 | 11030 | 0 | 0 | 1350 | 0 | 0 |
| `porba2.musketeer18.2.3` | Barracks 18c musketeer18 protection +2 (lvl 4) | 4 | 2 | 15.62 | 35706 | 0 | 0 | 4000 | 0 | 0 |
| `porba2.musketeer18.2.4` | Barracks 18c musketeer18 protection +1 (lvl 5) | 5 | 1 | 15.62 | 36556 | 0 | 0 | 4350 | 0 | 0 |
| `porba2.musketeer18.2.5` | Barracks 18c musketeer18 protection +2 (lvl 6) | 6 | 2 | 15.62 | 30060 | 0 | 0 | 1350 | 0 | 0 |
| `porba2.musketeer18.2.6` | Barracks 18c musketeer18 protection +2 (lvl 7) | 7 | 2 | 15.62 | 37600 | 0 | 0 | 1350 | 0 | 0 |
| `porba2.officer18.1.1` | Barracks 18c officer18 damage +30 (lvl 2) | 2 | 30 | 15.62 | 200 | 0 | 0 | 910 | 0 | 0 |
| `porba2.officer18.2.1` | Barracks 18c officer18 protection +12 (lvl 2) | 2 | 12 | 15.62 | 305 | 0 | 0 | 950 | 0 | 0 |
| `porba2.pikeman18.1.1` | Barracks 18c pikeman18 damage +2 (lvl 2) | 2 | 2 | 15.62 | 2000 | 0 | 0 | 800 | 0 | 0 |
| `porba2.pikeman18.1.2` | Barracks 18c pikeman18 damage +2 (lvl 3) | 3 | 2 | 15.62 | 8000 | 0 | 0 | 1200 | 0 | 0 |
| `porba2.pikeman18.1.3` | Barracks 18c pikeman18 damage +2 (lvl 4) | 4 | 2 | 15.62 | 20000 | 0 | 0 | 2500 | 0 | 0 |
| `porba2.pikeman18.1.4` | Barracks 18c pikeman18 damage +2 (lvl 5) | 5 | 2 | 15.62 | 32000 | 0 | 0 | 2800 | 0 | 0 |
| `porba2.pikeman18.1.5` | Barracks 18c pikeman18 damage +2 (lvl 6) | 6 | 2 | 15.62 | 32000 | 0 | 0 | 3800 | 0 | 0 |
| `porba2.pikeman18.1.6` | Barracks 18c pikeman18 damage +2 (lvl 7) | 7 | 2 | 15.62 | 40500 | 0 | 0 | 4800 | 0 | 0 |
| `porba2.pikeman18.2.1` | Barracks 18c pikeman18 protection +2 (lvl 2) | 2 | 2 | 15.62 | 1500 | 0 | 0 | 500 | 0 | 0 |
| `porba2.pikeman18.2.2` | Barracks 18c pikeman18 protection +3 (lvl 3) | 3 | 3 | 15.62 | 7000 | 0 | 0 | 1500 | 0 | 0 |
| `porba2.pikeman18.2.3` | Barracks 18c pikeman18 protection +2 (lvl 4) | 4 | 2 | 15.62 | 37000 | 0 | 0 | 2000 | 0 | 0 |
| `porba2.pikeman18.2.4` | Barracks 18c pikeman18 protection +3 (lvl 5) | 5 | 3 | 15.62 | 37000 | 0 | 0 | 5500 | 0 | 0 |
| `porba2.pikeman18.2.5` | Barracks 18c pikeman18 protection +2 (lvl 6) | 6 | 2 | 15.62 | 37000 | 0 | 0 | 5500 | 0 | 0 |
| `porba2.pikeman18.2.6` | Barracks 18c pikeman18 protection +3 (lvl 7) | 7 | 3 | 15.62 | 64600 | 0 | 0 | 5500 | 0 | 0 |
| `porbar.1` | — | 1 | 140 | 15.62 | 750 | 0 | 0 | 250 | 0 | 0 |
| `porbar.2` | — | 2 | 180 | 15.62 | 25600 | 0 | 0 | 3350 | 2000 | 0 |
| `porbar.drummer.2.1` | Barracks 17c drummer protection +12 (lvl 2) | 2 | 12 | 15.62 | 905 | 0 | 0 | 25 | 0 | 0 |
| `porbar.musketeer.1.1` | Barracks 17c musketeer damage +1 (lvl 2) | 2 | 1 | 15.62 | 1000 | 0 | 0 | 200 | 0 | 0 |
| `porbar.musketeer.1.2` | Barracks 17c musketeer damage +1 (lvl 3) | 3 | 1 | 15.62 | 2000 | 0 | 0 | 200 | 0 | 0 |
| `porbar.musketeer.1.3` | Barracks 17c musketeer damage +2 (lvl 4) | 4 | 2 | 15.62 | 100 | 0 | 0 | 200 | 0 | 0 |
| `porbar.musketeer.2.1` | Barracks 17c musketeer protection +1 (lvl 2) | 2 | 1 | 15.62 | 450 | 0 | 0 | 550 | 300 | 0 |
| `porbar.musketeer.2.2` | Barracks 17c musketeer protection +2 (lvl 3) | 3 | 2 | 15.62 | 405 | 0 | 0 | 150 | 20 | 0 |
| `porbar.musketeer.2.3` | Barracks 17c musketeer protection +2 (lvl 4) | 4 | 2 | 15.62 | 1570 | 0 | 0 | 100 | 290 | 0 |
| `porbar.musketeer.2.4` | Barracks 17c musketeer protection +1 (lvl 5) | 5 | 1 | 15.62 | 1956 | 0 | 0 | 450 | 700 | 0 |
| `porbar.musketeer.2.5` | Barracks 17c musketeer protection +2 (lvl 6) | 6 | 2 | 15.62 | 1660 | 0 | 0 | 550 | 400 | 0 |
| `porbar.musketeer.2.6` | Barracks 17c musketeer protection +2 (lvl 7) | 7 | 2 | 15.62 | 2700 | 0 | 0 | 850 | 100 | 0 |
| `porbar.officer.1.1` | Barracks 17c officer damage +20 (lvl 2) | 2 | 20 | 15.62 | 800 | 0 | 0 | 150 | 0 | 0 |
| `porbar.officer.2.1` | Barracks 17c officer protection +6 (lvl 2) | 2 | 6 | 15.62 | 1050 | 0 | 0 | 350 | 0 | 0 |
| `porbar.pikemanpor.1.1` | Barracks 17c pikemanpor damage +1 (lvl 2) | 2 | 1 | 15.62 | 3600 | 0 | 0 | 450 | 0 | 0 |
| `porbar.pikemanpor.1.2` | Barracks 17c pikemanpor damage +1 (lvl 3) | 3 | 1 | 15.62 | 1300 | 0 | 0 | 300 | 0 | 0 |
| `porbar.pikemanpor.1.3` | Barracks 17c pikemanpor damage +2 (lvl 4) | 4 | 2 | 15.62 | 200 | 0 | 0 | 50 | 0 | 0 |
| `porbar.pikemanpor.1.4` | Barracks 17c pikemanpor damage +1 (lvl 5) | 5 | 1 | 15.62 | 6800 | 0 | 0 | 1950 | 0 | 0 |
| `porbar.pikemanpor.1.5` | Barracks 17c pikemanpor damage +2 (lvl 6) | 6 | 2 | 15.62 | 15030 | 0 | 0 | 2300 | 0 | 0 |
| `porbar.pikemanpor.1.6` | — | 7 | 3 | 15.62 | 15000 | 0 | 0 | 1875 | 0 | 0 |
| `porbar.pikemanpor.2.1` | Barracks 17c pikemanpor protection +1 (lvl 2) | 2 | 1 | 15.62 | 350 | 0 | 0 | 50 | 0 | 0 |
| `porbar.pikemanpor.2.2` | Barracks 17c pikemanpor protection +1 (lvl 3) | 3 | 1 | 15.62 | 700 | 0 | 0 | 275 | 0 | 0 |
| `porbar.pikemanpor.2.3` | Barracks 17c pikemanpor protection +2 (lvl 4) | 4 | 2 | 15.62 | 2500 | 0 | 0 | 200 | 0 | 0 |
| `porbar.pikemanpor.2.4` | Barracks 17c pikemanpor protection +1 (lvl 5) | 5 | 1 | 15.62 | 13005 | 0 | 0 | 997 | 0 | 0 |
| `porbar.pikemanpor.2.5` | Barracks 17c pikemanpor protection +2 (lvl 6) | 6 | 2 | 15.62 | 16010 | 0 | 0 | 2550 | 0 | 0 |
| `porbar.pikemanpor.2.6` | — | 7 | 3 | 15.62 | 11250 | 0 | 0 | 1500 | 0 | 0 |
| `porbla.1` | Manufacture agricultural equipment (field capacity +100%) | 1 | 100 | 15.62 | 0 | 400 | 0 | 90 | 0 | 0 |
| `porbla.2` | Forge metal armature and gratings (building defence +50) | 1 | 50 | 15.62 | 0 | 0 | 12320 | 350 | 900 | 0 |
| `porbla.3` | Forge harnesses for horses (mounted units recruitment speed -33%) | 1 | -3333333 | 15.62 | 0 | 0 | 0 | 3650 | 5300 | 8200 |
| `porbla.4` | Forge bayonets and broadswords for infantry (18c musketeer/grenadier melee attack +5) | 1 | 5 | 15.62 | 0 | 1300 | 0 | 1500 | 900 | 5000 |
| `porbla.5` | Forge new types of broadswords and sabres (cavalry and sword clansman attack +5) | 1 | 5 | 15.62 | 0 | 0 | 0 | 4000 | 7900 | 0 |
| `porbla.6` | Forge new cuirasses (armoured soldiers defence +2) | 1 | 2 | 15.62 | 0 | 0 | 0 | 4950 | 10500 | 0 |
| `porcen.1` | — | 1 | 0 | 9.38 | 30000 | 0 | 0 | 5000 | 2000 | 2000 |
| `porpor.1` | — | 1 | 50 | 46.88 | 0 | 20000 | 0 | 1500 | 0 | 0 |
| `porsta.cuirassier.1.1` | Stable cuirassier damage +1 (lvl 2) | 2 | 1 | 15.62 | 11000 | 0 | 0 | 1600 | 0 | 0 |
| `porsta.cuirassier.1.2` | Stable cuirassier damage +1 (lvl 3) | 3 | 1 | 15.62 | 33000 | 0 | 0 | 300 | 0 | 0 |
| `porsta.cuirassier.1.3` | Stable cuirassier damage +1 (lvl 4) | 4 | 1 | 15.62 | 64000 | 0 | 0 | 3200 | 0 | 0 |
| `porsta.cuirassier.1.4` | Stable cuirassier damage +2 (lvl 5) | 5 | 2 | 15.62 | 59000 | 0 | 0 | 2150 | 0 | 0 |
| `porsta.cuirassier.1.5` | Stable cuirassier damage +2 (lvl 6) | 6 | 2 | 15.62 | 52055 | 0 | 0 | 5100 | 0 | 0 |
| `porsta.cuirassier.1.6` | Stable cuirassier damage +3 (lvl 7) | 7 | 3 | 15.62 | 54050 | 0 | 0 | 7020 | 0 | 0 |
| `porsta.cuirassier.2.1` | Stable cuirassier protection +2 (lvl 2) | 2 | 2 | 15.62 | 2505 | 0 | 0 | 350 | 1000 | 0 |
| `porsta.cuirassier.2.2` | Stable cuirassier protection +3 (lvl 3) | 3 | 3 | 15.62 | 2000 | 0 | 0 | 300 | 2000 | 0 |
| `porsta.cuirassier.2.3` | Stable cuirassier protection +3 (lvl 4) | 4 | 3 | 15.62 | 5600 | 0 | 0 | 750 | 3030 | 0 |
| `porsta.cuirassier.2.4` | Stable cuirassier protection +2 (lvl 5) | 5 | 2 | 15.62 | 10700 | 0 | 0 | 6100 | 100 | 0 |
| `porsta.cuirassier.2.5` | Stable cuirassier protection +1 (lvl 6) | 6 | 1 | 15.62 | 8100 | 0 | 0 | 2150 | 5000 | 0 |
| `porsta.cuirassier.2.6` | Stable cuirassier protection +1 (lvl 7) | 7 | 1 | 15.62 | 9200 | 0 | 0 | 4900 | 7060 | 0 |
| `porsta.dragoon.1.1` | Stable dragoon damage +1 (lvl 2) | 2 | 1 | 15.62 | 500 | 0 | 0 | 150 | 0 | 0 |
| `porsta.dragoon.1.2` | Stable dragoon damage +1 (lvl 3) | 3 | 1 | 15.62 | 700 | 0 | 0 | 200 | 0 | 0 |
| `porsta.dragoon.1.3` | Stable dragoon damage +2 (lvl 4) | 4 | 2 | 15.62 | 900 | 0 | 0 | 340 | 0 | 0 |
| `porsta.dragoon.1.4` | Stable dragoon damage +1 (lvl 5) | 5 | 1 | 15.62 | 0 | 0 | 0 | 0 | 0 | 0 |
| `porsta.dragoon.1.5` | Stable dragoon damage +1 (lvl 6) | 6 | 1 | 15.62 | 0 | 0 | 0 | 0 | 0 | 0 |
| `porsta.dragoon.1.6` | Stable dragoon damage +3 (lvl 7) | 7 | 3 | 15.62 | 0 | 0 | 0 | 0 | 0 | 0 |
| `porsta.dragoon.2.1` | Stable dragoon protection +1 (lvl 2) | 2 | 1 | 15.62 | 900 | 0 | 0 | 150 | 0 | 0 |
| `porsta.dragoon.2.2` | Stable dragoon protection +2 (lvl 3) | 3 | 2 | 15.62 | 6600 | 0 | 0 | 750 | 0 | 0 |
| `porsta.dragoon.2.3` | Stable dragoon protection +2 (lvl 4) | 4 | 2 | 15.62 | 5000 | 0 | 0 | 1250 | 0 | 0 |
| `porsta.dragoon.2.4` | Stable dragoon protection +1 (lvl 5) | 5 | 1 | 15.62 | 3000 | 0 | 0 | 600 | 0 | 0 |
| `porsta.dragoon.2.5` | Stable dragoon protection +2 (lvl 6) | 6 | 2 | 15.62 | 1000 | 0 | 0 | 2350 | 0 | 0 |
| `porsta.dragoon.2.6` | Stable dragoon protection +2 (lvl 7) | 7 | 2 | 15.62 | 6001 | 0 | 0 | 6000 | 0 | 0 |
| `porsta.dragoon18.1.1` | Stable dragoon18 damage +2 (lvl 2) | 2 | 2 | 15.62 | 2000 | 0 | 0 | 100 | 0 | 0 |
| `porsta.dragoon18.1.2` | Stable dragoon18 damage +2 (lvl 3) | 3 | 2 | 15.62 | 9000 | 0 | 0 | 350 | 0 | 0 |
| `porsta.dragoon18.1.3` | Stable dragoon18 damage +4 (lvl 4) | 4 | 4 | 15.62 | 12000 | 0 | 0 | 400 | 0 | 0 |
| `porsta.dragoon18.1.4` | Stable dragoon18 damage +2 (lvl 5) | 5 | 2 | 15.62 | 23000 | 0 | 0 | 580 | 0 | 0 |
| `porsta.dragoon18.1.5` | Stable dragoon18 damage +2 (lvl 6) | 6 | 2 | 15.62 | 32000 | 0 | 0 | 680 | 0 | 0 |
| `porsta.dragoon18.1.6` | Stable dragoon18 damage +4 (lvl 7) | 7 | 4 | 15.62 | 42000 | 0 | 0 | 780 | 0 | 0 |
| `porsta.dragoon18.2.1` | Stable dragoon18 protection +1 (lvl 2) | 2 | 1 | 15.62 | 260 | 0 | 0 | 935 | 0 | 0 |
| `porsta.dragoon18.2.2` | Stable dragoon18 protection +1 (lvl 3) | 3 | 1 | 15.62 | 1460 | 0 | 0 | 1150 | 0 | 0 |
| `porsta.dragoon18.2.3` | Stable dragoon18 protection +2 (lvl 4) | 4 | 2 | 15.62 | 12600 | 0 | 0 | 3350 | 0 | 0 |
| `porsta.dragoon18.2.4` | Stable dragoon18 protection +1 (lvl 5) | 5 | 1 | 15.62 | 19600 | 0 | 0 | 3350 | 0 | 0 |
| `porsta.dragoon18.2.5` | Stable dragoon18 protection +2 (lvl 6) | 6 | 2 | 15.62 | 12600 | 0 | 0 | 7350 | 0 | 0 |
| `porsta.dragoon18.2.6` | Stable dragoon18 protection +3 (lvl 7) | 7 | 3 | 15.62 | 26760 | 0 | 0 | 6350 | 0 | 0 |
| `porsta.hussar.1.1` | Stable hussar damage +1 (lvl 2) | 2 | 1 | 15.62 | 0 | 0 | 0 | 1800 | 1000 | 0 |
| `porsta.hussar.1.2` | Stable hussar damage +2 (lvl 3) | 3 | 2 | 15.62 | 0 | 0 | 0 | 3800 | 2000 | 0 |
| `porsta.hussar.1.3` | Stable hussar damage +3 (lvl 4) | 4 | 3 | 15.62 | 20200 | 0 | 0 | 0 | 3000 | 0 |
| `porsta.hussar.1.4` | Stable hussar damage +4 (lvl 5) | 5 | 4 | 15.62 | 32000 | 0 | 0 | 0 | 3000 | 0 |
| `porsta.hussar.1.5` | Stable hussar damage +1 (lvl 6) | 6 | 1 | 15.62 | 49200 | 0 | 0 | 0 | 3500 | 0 |
| `porsta.hussar.1.6` | Stable hussar damage +1 (lvl 7) | 7 | 1 | 15.62 | 20000 | 0 | 0 | 0 | 6000 | 0 |
| `porsta.hussar.2.1` | Stable hussar protection +1 (lvl 2) | 2 | 1 | 15.62 | 1760 | 0 | 0 | 1350 | 0 | 0 |
| `porsta.hussar.2.2` | Stable hussar protection +1 (lvl 3) | 3 | 1 | 15.62 | 1900 | 0 | 0 | 2350 | 0 | 0 |
| `porsta.hussar.2.3` | Stable hussar protection +1 (lvl 4) | 4 | 1 | 15.62 | 1600 | 0 | 0 | 5350 | 0 | 0 |
| `porsta.hussar.2.4` | Stable hussar protection +2 (lvl 5) | 5 | 2 | 15.62 | 8000 | 0 | 0 | 8350 | 0 | 0 |
| `porsta.hussar.2.5` | Stable hussar protection +2 (lvl 6) | 6 | 2 | 15.62 | 2000 | 0 | 0 | 15350 | 0 | 0 |
| `porsta.hussar.2.6` | Stable hussar protection +3 (lvl 7) | 7 | 3 | 15.62 | 56000 | 0 | 0 | 20150 | 0 | 0 |
| `porsta.reiter.1.1` | Stable reiter damage +1 (lvl 2) | 2 | 1 | 15.62 | 500 | 0 | 0 | 100 | 0 | 0 |
| `porsta.reiter.1.2` | Stable reiter damage +2 (lvl 3) | 3 | 2 | 15.62 | 800 | 0 | 0 | 220 | 0 | 0 |
| `porsta.reiter.1.3` | Stable reiter damage +1 (lvl 4) | 4 | 1 | 15.62 | 2400 | 0 | 0 | 380 | 0 | 0 |
| `porsta.reiter.1.4` | Stable reiter damage +1 (lvl 5) | 5 | 1 | 15.62 | 4250 | 0 | 0 | 220 | 0 | 0 |
| `porsta.reiter.1.5` | Stable reiter damage +1 (lvl 6) | 6 | 1 | 15.62 | 4030 | 0 | 0 | 900 | 0 | 0 |
| `porsta.reiter.1.6` | Stable reiter damage +1 (lvl 7) | 7 | 1 | 15.62 | 6000 | 0 | 0 | 1600 | 0 | 0 |
| `porsta.reiter.2.1` | Stable reiter protection +2 (lvl 2) | 2 | 2 | 15.62 | 200 | 0 | 0 | 135 | 400 | 0 |
| `porsta.reiter.2.2` | Stable reiter protection +3 (lvl 3) | 3 | 3 | 15.62 | 600 | 0 | 0 | 100 | 300 | 0 |
| `porsta.reiter.2.3` | Stable reiter protection +3 (lvl 4) | 4 | 3 | 15.62 | 800 | 0 | 0 | 200 | 560 | 0 |
| `porsta.reiter.2.4` | Stable reiter protection +2 (lvl 5) | 5 | 2 | 15.62 | 1600 | 0 | 0 | 300 | 340 | 0 |
| `porsta.reiter.2.5` | Stable reiter protection +1 (lvl 6) | 6 | 1 | 15.62 | 2200 | 0 | 0 | 350 | 600 | 0 |
| `porsta.reiter.2.6` | Stable reiter protection +1 (lvl 7) | 7 | 1 | 15.62 | 17000 | 0 | 0 | 950 | 5200 | 0 |
| `ukrwwa.1` | — | 2 | 5 | 0.03 | 0 | 400 | 0 | 0 | 0 | 0 |

### pie — Piedmont

| sid | имя (EN) | level | value | время (s) | F | W | S | G | I | C |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `eurcoa.1` | — | 2 | 5 | 9.38 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `eurcoa.2` | — | 3 | 8 | 9.38 | 5250 | 0 | 0 | 4950 | 0 | 0 |
| `eurcoa.3` | — | 4 | 10 | 9.38 | 12500 | 0 | 0 | 9250 | 0 | 0 |
| `eurcoa.4` | — | 5 | 12 | 9.38 | 15800 | 0 | 0 | 18500 | 0 | 0 |
| `eurcoa.5` | — | 6 | 15 | 9.38 | 19800 | 0 | 0 | 21050 | 0 | 0 |
| `eurcoa.6` | — | 7 | 40 | 9.38 | 50200 | 0 | 0 | 25950 | 0 | 0 |
| `eurgol.1` | — | 2 | 5 | 9.38 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `eurgol.2` | — | 3 | 8 | 9.38 | 5250 | 0 | 0 | 4950 | 0 | 0 |
| `eurgol.3` | — | 4 | 10 | 9.38 | 12500 | 0 | 0 | 9250 | 0 | 0 |
| `eurgol.4` | — | 5 | 12 | 9.38 | 15800 | 0 | 0 | 18500 | 0 | 0 |
| `eurgol.5` | — | 6 | 15 | 9.38 | 19800 | 0 | 0 | 21050 | 0 | 0 |
| `eurgol.6` | — | 7 | 40 | 9.38 | 50200 | 0 | 0 | 25950 | 0 | 0 |
| `euriro.1` | — | 2 | 5 | 9.38 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `euriro.2` | — | 3 | 8 | 9.38 | 5250 | 0 | 0 | 4950 | 0 | 0 |
| `euriro.3` | — | 4 | 10 | 9.38 | 12500 | 0 | 0 | 9250 | 0 | 0 |
| `euriro.4` | — | 5 | 12 | 9.38 | 15800 | 0 | 0 | 18500 | 0 | 0 |
| `euriro.5` | — | 6 | 15 | 9.38 | 19800 | 0 | 0 | 21050 | 0 | 0 |
| `euriro.6` | — | 7 | 40 | 9.38 | 50200 | 0 | 0 | 25950 | 0 | 0 |
| `eurpor.1` | — | 1 | 50 | 46.88 | 0 | 20000 | 0 | 1500 | 0 | 0 |
| `eurswa.1` | — | 2 | 5 | 0.03 | 0 | 0 | 500 | 0 | 0 | 0 |
| `eurtow.1` | — | 2 | -20 | 31.25 | 0 | 0 | 0 | 250 | 0 | 0 |
| `eurtow.2` | — | 3 | -20 | 31.25 | 0 | 0 | 0 | 0 | 350 | 0 |
| `eurtow.3` | — | 4 | -10 | 31.25 | 0 | 0 | 0 | 0 | 0 | 400 |
| `eurtow.4` | — | 5 | -10 | 31.25 | 0 | 0 | 0 | 0 | 450 | 0 |
| `eurtow.5` | — | 6 | -10 | 31.25 | 0 | 0 | 0 | 0 | 0 | 500 |
| `ferry.1` | Improve transport vessel design (+%value% capacity) | 2 | 200 | 15.62 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `pieaca.1` | Cultivate new cultures of wheat (harvesting +40%) | 1 | 40 | 15.62 | 0 | 200 | 0 | 325 | 0 | 0 |
| `pieaca.10` | Raise builders' salary (building construction time -75%) | 1 | -7500000 | 15.62 | 0 | 0 | 0 | 6950 | 0 | 0 |
| `pieaca.11` | Research new fortification grades (durability of walls and towers +80) | 1 | 80 | 15.62 | 0 | 0 | 16200 | 1500 | 0 | 0 |
| `pieaca.12` | Improve firearms: rifled barrel (fire power +10%) | 1 | 10 | 15.62 | 0 | 0 | 0 | 0 | 5000 | 0 |
| `pieaca.13` | Research granular gunpowder (fire power +10%) | 1 | 10 | 15.62 | 0 | 0 | 0 | 4000 | 0 | 0 |
| `pieaca.14` | Research new sulphur purification methods (fire power +15%) | 1 | 15 | 15.62 | 0 | 0 | 0 | 7000 | 0 | 0 |
| `pieaca.15` | Research new nitre purification methods (fire power +25%) | 1 | 25 | 15.62 | 0 | 0 | 0 | 0 | 0 | 11000 |
| `pieaca.16` | Research improved additions to gunpowder formula (artillery range +5%) | 1 | 5 | 15.62 | 0 | 0 | 0 | 2000 | 12150 | 0 |
| `pieaca.17` | Design new barrel types: unicorn, carronade (artillery range +10%) | 1 | 10 | 15.62 | 0 | 0 | 3000 | 4550 | 19200 | 0 |
| `pieaca.18` | Design more durable gun carriage: Gribovalle system (artillery durability +50%) | 1 | 50 | 15.62 | 0 | 0 | 0 | 500 | 3830 | 1500 |
| `pieaca.19` | Design multi-barrelled cannon | 1 | 0 | 15.62 | 0 | 0 | 0 | 1500 | 0 | 2500 |
| `pieaca.2` | Cultivate new cultures of rye (harvesting +50%) | 1 | 50 | 15.62 | 0 | 2400 | 0 | 625 | 0 | 0 |
| `pieaca.20` | Research new sighting devices for artillery (artillery accuracy +35%) | 1 | -35 | 15.62 | 0 | 3540 | 0 | 2000 | 0 | 7250 |
| `pieaca.21` | Finance artillery repair shops (repair all artillery) | 1 | 25 | 15.62 | 0 | 350 | 0 | 100 | 0 | 250 |
| `pieaca.22` | Develop geology (previously hidden deposits appear on the map) | 1 | 0 | 15.62 | 0 | 0 | 0 | 250 | 0 | 0 |
| `pieaca.23` | Develop mining (stone excavation efficiency +100%) | 1 | 100 | 15.62 | 0 | 0 | 0 | 1550 | 3000 | 0 |
| `pieaca.24` | Raise miners' salary (stone excavation efficiency +200%) | 1 | 200 | 15.62 | 4200 | 0 | 0 | 1550 | 0 | 12520 |
| `pieaca.25` | Design Montgolfier (reveals the whole map) | 1 | 0 | 15.62 | 0 | 0 | 0 | 5750 | 0 | 0 |
| `pieaca.26` | Develop medical science (heals all live units) | 1 | 50 | 31.25 | 0 | 0 | 0 | 200 | 0 | 200 |
| `pieaca.27` | Develop mathematics (artillery accuracy +35%) | 1 | -35 | 15.62 | 0 | 9540 | 0 | 12000 | 0 | 65200 |
| `pieaca.28` | Design new rigging types (ship speed +40%) | 1 | 40 | 15.62 | 0 | 65400 | 0 | 24050 | 0 | 0 |
| `pieaca.29` | Design new rib system and new hulls (battleship construction) | 1 | 0 | 15.62 | 0 | 32300 | 0 | 6800 | 9000 | 12800 |
| `pieaca.3` | Raise agriculturists' salary (harvesting +50%) | 1 | 50 | 15.62 | 0 | 3600 | 0 | 850 | 0 | 0 |
| `pieaca.30` | Train carpenters (shipbuilding speed x10) | 1 | -5000000 | 15.62 | 0 | 2300 | 42700 | 1150 | 0 | 0 |
| `pieaca.31` | Design wheellock (rate of fire +30%) | 1 | -30 | 15.62 | 0 | 0 | 6000 | 5500 | 4200 | 0 |
| `pieaca.32` | Design flintlock (musket cost -50%) | 1 | 0 | 15.62 | 0 | 0 | 0 | 6050 | 0 | 7750 |
| `pieaca.33` | Design paper cartridge and iron ramrod (rate of fire +30%) | 1 | -30 | 15.62 | 0 | 5000 | 0 | 5500 | 0 | 15200 |
| `pieaca.34` | Research improved steel grades for cuirasses (armoured soldier defence +2) | 1 | 2 | 15.62 | 0 | 0 | 0 | 9750 | 0 | 0 |
| `pieaca.35` | Design bayonet: barrel-inserted, bayonet with a tube (cold steel weapons +5) | 1 | 5 | 15.62 | 0 | 0 | 0 | 11500 | 0 | 0 |
| `pieaca.36` | Research new steel grades (18c musketeer/grenadier melee attack efficiency +25%) | 1 | 25 | 15.62 | 0 | 0 | 0 | 19500 | 0 | 0 |
| `pieaca.4` | Carry out field melioration (field capacity +200%) | 1 | 200 | 15.62 | 0 | 1000 | 0 | 475 | 0 | 0 |
| `pieaca.5` | Design new tackle and fishing nets (boat efficiency +100%) | 1 | 100 | 15.62 | 0 | 12400 | 0 | 2520 | 0 | 0 |
| `pieaca.6` | Develop new woodworking methods (frigate building) | 1 | 0 | 15.62 | 0 | 12400 | 0 | 7040 | 0 | 0 |
| `pieaca.7` | Build new shipyards for fishing boats (fishing boat cost -85%) | 1 | 0 | 15.62 | 0 | 7300 | 0 | 1220 | 0 | 0 |
| `pieaca.8` | Design new woodworking tools (woodcutting efficiency +100%) | 1 | 100 | 15.62 | 5500 | 0 | 0 | 550 | 0 | 0 |
| `pieaca.9` | Use new construction materials (durability of buildings +85) | 1 | 85 | 15.62 | 0 | 9400 | 7850 | 1150 | 0 | 0 |
| `pieart.cannon.1.1` | — | 2 | — | 10.0 | 0 | 1000 | 500 | 300 | 0 | 0 |
| `pieart.cannon.1.2` | — | 3 | — | 10.0 | 0 | 3000 | 1000 | 500 | 0 | 0 |
| `pieart.cannon.1.3` | — | 4 | — | 10.0 | 0 | 6000 | 2000 | 1000 | 0 | 0 |
| `pieart.cannon.1.4` | — | 5 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `pieart.cannon.1.5` | — | 6 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `pieart.cannon.1.6` | — | 7 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `pieart.cannon.2.1` | — | 2 | -2500000 | 10.0 | 0 | 0 | 0 | 500 | 1000 | 0 |
| `pieart.cannon.2.2` | — | 3 | -2500000 | 10.0 | 0 | 0 | 0 | 1000 | 2000 | 0 |
| `pieart.cannon.2.3` | — | 4 | -2500000 | 10.0 | 0 | 0 | 0 | 2000 | 3000 | 0 |
| `pieart.cannon.2.4` | — | 5 | -2000000 | 15.62 | 2560 | 0 | 0 | 0 | 0 | 0 |
| `pieart.cannon.2.5` | — | 6 | -2000000 | 15.62 | 3560 | 0 | 0 | 0 | 0 | 0 |
| `pieart.cannon.2.6` | — | 7 | -2000000 | 15.62 | 5560 | 0 | 0 | 0 | 0 | 0 |
| `pieart.howitzer.1.1` | — | 2 | — | 10.0 | 0 | 1000 | 500 | 300 | 0 | 0 |
| `pieart.howitzer.1.2` | — | 3 | — | 10.0 | 0 | 3000 | 1000 | 500 | 0 | 0 |
| `pieart.howitzer.1.3` | — | 4 | — | 10.0 | 0 | 6000 | 2000 | 1000 | 0 | 0 |
| `pieart.howitzer.1.4` | — | 5 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `pieart.howitzer.1.5` | — | 6 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `pieart.howitzer.1.6` | — | 7 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `pieart.howitzer.2.1` | — | 2 | -2500000 | 10.0 | 0 | 0 | 0 | 500 | 1000 | 0 |
| `pieart.howitzer.2.2` | — | 3 | -2500000 | 10.0 | 0 | 0 | 0 | 1000 | 2000 | 0 |
| `pieart.howitzer.2.3` | — | 4 | -2500000 | 10.0 | 0 | 0 | 0 | 2000 | 3000 | 0 |
| `pieart.howitzer.2.4` | — | 5 | -2000000 | 31.25 | 2560 | 0 | 0 | 0 | 0 | 0 |
| `pieart.howitzer.2.5` | — | 6 | -2000000 | 31.25 | 3560 | 0 | 0 | 0 | 0 | 0 |
| `pieart.howitzer.2.6` | — | 7 | -2000000 | 31.25 | 5560 | 0 | 0 | 0 | 0 | 0 |
| `pieba2.drummer18.2.1` | Barracks 18c drummer18 protection +15 (lvl 2) | 2 | 15 | 15.62 | 706 | 0 | 0 | 50 | 0 | 0 |
| `pieba2.grenadier.1.1` | Barracks 18c grenadier damage +2 (lvl 2) | 2 | 2 | 15.62 | 2000 | 0 | 0 | 800 | 0 | 0 |
| `pieba2.grenadier.1.2` | Barracks 18c grenadier damage +3 (lvl 3) | 3 | 3 | 15.62 | 12000 | 0 | 0 | 1800 | 0 | 0 |
| `pieba2.grenadier.1.3` | Barracks 18c grenadier damage +4 (lvl 4) | 4 | 4 | 15.62 | 32000 | 0 | 0 | 2800 | 0 | 0 |
| `pieba2.grenadier.1.4` | Barracks 18c grenadier damage +5 (lvl 5) | 5 | 5 | 15.62 | 42000 | 0 | 0 | 3800 | 0 | 0 |
| `pieba2.grenadier.1.5` | Barracks 18c grenadier damage +6 (lvl 6) | 6 | 6 | 15.62 | 52000 | 0 | 0 | 4800 | 0 | 0 |
| `pieba2.grenadier.1.6` | Barracks 18c grenadier damage +1500 (lvl 7) | 7 | 1500 | 15.62 | 62000 | 0 | 0 | 15800 | 0 | 0 |
| `pieba2.grenadier.2.1` | Barracks 18c grenadier protection +1 (lvl 2) | 2 | 1 | 15.62 | 3706 | 0 | 0 | 350 | 0 | 0 |
| `pieba2.grenadier.2.2` | Barracks 18c grenadier protection +2 (lvl 3) | 3 | 2 | 15.62 | 11030 | 0 | 0 | 1350 | 0 | 0 |
| `pieba2.grenadier.2.3` | Barracks 18c grenadier protection +3 (lvl 4) | 4 | 3 | 15.62 | 35706 | 0 | 0 | 3000 | 0 | 0 |
| `pieba2.grenadier.2.4` | Barracks 18c grenadier protection +1 (lvl 5) | 5 | 1 | 15.62 | 36556 | 0 | 0 | 3350 | 0 | 0 |
| `pieba2.grenadier.2.5` | Barracks 18c grenadier protection +2 (lvl 6) | 6 | 2 | 15.62 | 30060 | 0 | 0 | 1350 | 0 | 0 |
| `pieba2.grenadier.2.6` | Barracks 18c grenadier protection +3 (lvl 7) | 7 | 3 | 15.62 | 64000 | 0 | 0 | 1350 | 0 | 0 |
| `pieba2.musketeer18.1.1` | Barracks 18c musketeer18 damage +1 (lvl 2) | 2 | 1 | 15.62 | 1000 | 0 | 0 | 800 | 0 | 0 |
| `pieba2.musketeer18.1.2` | Barracks 18c musketeer18 damage +1 (lvl 3) | 3 | 1 | 15.62 | 1500 | 0 | 0 | 800 | 0 | 0 |
| `pieba2.musketeer18.1.3` | Barracks 18c musketeer18 damage +2 (lvl 4) | 4 | 2 | 15.62 | 2000 | 0 | 0 | 800 | 0 | 0 |
| `pieba2.musketeer18.1.4` | Barracks 18c musketeer18 damage +2 (lvl 5) | 5 | 2 | 15.62 | 2500 | 0 | 0 | 800 | 0 | 0 |
| `pieba2.musketeer18.1.5` | Barracks 18c musketeer18 damage +3 (lvl 6) | 6 | 3 | 15.62 | 3000 | 0 | 0 | 800 | 0 | 0 |
| `pieba2.musketeer18.1.6` | Barracks 18c musketeer18 damage +3 (lvl 7) | 7 | 3 | 15.62 | 3500 | 0 | 0 | 800 | 0 | 0 |
| `pieba2.musketeer18.2.1` | Barracks 18c musketeer18 protection +1 (lvl 2) | 2 | 1 | 15.62 | 3706 | 0 | 0 | 350 | 0 | 0 |
| `pieba2.musketeer18.2.2` | Barracks 18c musketeer18 protection +2 (lvl 3) | 3 | 2 | 15.62 | 11030 | 0 | 0 | 1350 | 0 | 0 |
| `pieba2.musketeer18.2.3` | Barracks 18c musketeer18 protection +2 (lvl 4) | 4 | 2 | 15.62 | 35706 | 0 | 0 | 4000 | 0 | 0 |
| `pieba2.musketeer18.2.4` | Barracks 18c musketeer18 protection +1 (lvl 5) | 5 | 1 | 15.62 | 36556 | 0 | 0 | 4350 | 0 | 0 |
| `pieba2.musketeer18.2.5` | Barracks 18c musketeer18 protection +2 (lvl 6) | 6 | 2 | 15.62 | 30060 | 0 | 0 | 1350 | 0 | 0 |
| `pieba2.musketeer18.2.6` | Barracks 18c musketeer18 protection +2 (lvl 7) | 7 | 2 | 15.62 | 37600 | 0 | 0 | 1350 | 0 | 0 |
| `pieba2.officer18.1.1` | Barracks 18c officer18 damage +30 (lvl 2) | 2 | 30 | 15.62 | 1000 | 0 | 0 | 800 | 0 | 0 |
| `pieba2.officer18.2.1` | Barracks 18c officer18 protection +12 (lvl 2) | 2 | 12 | 15.62 | 1706 | 0 | 0 | 350 | 0 | 0 |
| `pieba2.pikeman18.1.1` | Barracks 18c pikeman18 damage +2 (lvl 2) | 2 | 2 | 15.62 | 2000 | 0 | 0 | 800 | 0 | 0 |
| `pieba2.pikeman18.1.2` | Barracks 18c pikeman18 damage +2 (lvl 3) | 3 | 2 | 15.62 | 8000 | 0 | 0 | 1200 | 0 | 0 |
| `pieba2.pikeman18.1.3` | Barracks 18c pikeman18 damage +2 (lvl 4) | 4 | 2 | 15.62 | 20000 | 0 | 0 | 2500 | 0 | 0 |
| `pieba2.pikeman18.1.4` | Barracks 18c pikeman18 damage +2 (lvl 5) | 5 | 2 | 15.62 | 32000 | 0 | 0 | 2800 | 0 | 0 |
| `pieba2.pikeman18.1.5` | Barracks 18c pikeman18 damage +2 (lvl 6) | 6 | 2 | 15.62 | 32000 | 0 | 0 | 3800 | 0 | 0 |
| `pieba2.pikeman18.1.6` | Barracks 18c pikeman18 damage +2 (lvl 7) | 7 | 2 | 15.62 | 40500 | 0 | 0 | 4800 | 0 | 0 |
| `pieba2.pikeman18.2.1` | Barracks 18c pikeman18 protection +2 (lvl 2) | 2 | 2 | 15.62 | 1500 | 0 | 0 | 500 | 0 | 0 |
| `pieba2.pikeman18.2.2` | Barracks 18c pikeman18 protection +3 (lvl 3) | 3 | 3 | 15.62 | 7000 | 0 | 0 | 1500 | 0 | 0 |
| `pieba2.pikeman18.2.3` | Barracks 18c pikeman18 protection +2 (lvl 4) | 4 | 2 | 15.62 | 37000 | 0 | 0 | 2000 | 0 | 0 |
| `pieba2.pikeman18.2.4` | Barracks 18c pikeman18 protection +3 (lvl 5) | 5 | 3 | 15.62 | 37000 | 0 | 0 | 5500 | 0 | 0 |
| `pieba2.pikeman18.2.5` | Barracks 18c pikeman18 protection +2 (lvl 6) | 6 | 2 | 15.62 | 37000 | 0 | 0 | 5500 | 0 | 0 |
| `pieba2.pikeman18.2.6` | Barracks 18c pikeman18 protection +3 (lvl 7) | 7 | 3 | 15.62 | 64600 | 0 | 0 | 5500 | 0 | 0 |
| `piebar.1` | — | 1 | 140 | 15.62 | 750 | 0 | 0 | 250 | 0 | 0 |
| `piebar.2` | — | 2 | 180 | 15.62 | 25600 | 0 | 0 | 3350 | 2000 | 0 |
| `piebar.drummer.2.1` | Barracks 17c drummer protection +12 (lvl 2) | 2 | 12 | 15.62 | 500 | 0 | 0 | 75 | 0 | 0 |
| `piebar.musketeer.1.1` | Barracks 17c musketeer damage +1 (lvl 2) | 2 | 1 | 15.62 | 2000 | 0 | 0 | 100 | 0 | 0 |
| `piebar.musketeer.1.2` | Barracks 17c musketeer damage +1 (lvl 3) | 3 | 1 | 15.62 | 1000 | 0 | 0 | 300 | 0 | 0 |
| `piebar.musketeer.1.3` | Barracks 17c musketeer damage +2 (lvl 4) | 4 | 2 | 15.62 | 500 | 0 | 0 | 700 | 0 | 0 |
| `piebar.musketeer.2.1` | Barracks 17c musketeer protection +1 (lvl 2) | 2 | 1 | 15.62 | 170 | 0 | 0 | 50 | 100 | 0 |
| `piebar.musketeer.2.2` | Barracks 17c musketeer protection +2 (lvl 3) | 3 | 2 | 15.62 | 405 | 0 | 0 | 150 | 200 | 0 |
| `piebar.musketeer.2.3` | Barracks 17c musketeer protection +2 (lvl 4) | 4 | 2 | 15.62 | 1570 | 0 | 0 | 100 | 350 | 0 |
| `piebar.musketeer.2.4` | Barracks 17c musketeer protection +1 (lvl 5) | 5 | 1 | 15.62 | 1556 | 0 | 0 | 550 | 100 | 0 |
| `piebar.musketeer.2.5` | Barracks 17c musketeer protection +2 (lvl 6) | 6 | 2 | 15.62 | 1060 | 0 | 0 | 850 | 400 | 0 |
| `piebar.musketeer.2.6` | Barracks 17c musketeer protection +2 (lvl 7) | 7 | 2 | 15.62 | 3700 | 0 | 0 | 450 | 700 | 0 |
| `piebar.officer.1.1` | Barracks 17c officer damage +20 (lvl 2) | 2 | 20 | 15.62 | 100 | 0 | 0 | 50 | 0 | 0 |
| `piebar.officer.2.1` | Barracks 17c officer protection +6 (lvl 2) | 2 | 6 | 15.62 | 1050 | 0 | 0 | 350 | 0 | 0 |
| `piebar.pikeman.1.1` | Barracks 17c pikeman damage +1 (lvl 2) | 2 | 1 | 15.62 | 200 | 0 | 0 | 50 | 0 | 0 |
| `piebar.pikeman.1.2` | Barracks 17c pikeman damage +2 (lvl 3) | 3 | 2 | 15.62 | 1300 | 0 | 0 | 300 | 0 | 0 |
| `piebar.pikeman.1.3` | Barracks 17c pikeman damage +2 (lvl 4) | 4 | 2 | 15.62 | 3600 | 0 | 0 | 450 | 0 | 0 |
| `piebar.pikeman.1.4` | Barracks 17c pikeman damage +1 (lvl 5) | 5 | 1 | 15.62 | 7200 | 0 | 0 | 1850 | 0 | 0 |
| `piebar.pikeman.1.5` | Barracks 17c pikeman damage +2 (lvl 6) | 6 | 2 | 15.62 | 16030 | 0 | 0 | 2000 | 0 | 0 |
| `piebar.pikeman.1.6` | — | 7 | 2 | 15.62 | 15000 | 0 | 0 | 1875 | 0 | 0 |
| `piebar.pikeman.2.1` | Barracks 17c pikeman protection +1 (lvl 2) | 2 | 1 | 15.62 | 150 | 0 | 0 | 50 | 0 | 0 |
| `piebar.pikeman.2.2` | Barracks 17c pikeman protection +1 (lvl 3) | 3 | 1 | 15.62 | 900 | 0 | 0 | 175 | 0 | 0 |
| `piebar.pikeman.2.3` | Barracks 17c pikeman protection +2 (lvl 4) | 4 | 2 | 15.62 | 4500 | 0 | 0 | 300 | 0 | 0 |
| `piebar.pikeman.2.4` | Barracks 17c pikeman protection +1 (lvl 5) | 5 | 1 | 15.62 | 9005 | 0 | 0 | 507 | 0 | 0 |
| `piebar.pikeman.2.5` | Barracks 17c pikeman protection +1 (lvl 6) | 6 | 1 | 15.62 | 18010 | 0 | 0 | 3050 | 0 | 0 |
| `piebar.pikeman.2.6` | — | 7 | 2 | 15.62 | 11250 | 0 | 0 | 1500 | 0 | 0 |
| `piebla.1` | Manufacture agricultural equipment (field capacity +100%) | 1 | 100 | 15.62 | 0 | 400 | 0 | 90 | 0 | 0 |
| `piebla.2` | Forge metal armature and gratings (building defence +50) | 1 | 50 | 15.62 | 0 | 0 | 12320 | 350 | 900 | 0 |
| `piebla.3` | Forge harnesses for horses (mounted units recruitment speed -33%) | 1 | -3333333 | 15.62 | 0 | 0 | 0 | 3650 | 5300 | 8200 |
| `piebla.4` | Forge bayonets and broadswords for infantry (18c musketeer/grenadier melee attack +5) | 1 | 5 | 15.62 | 0 | 1300 | 0 | 1500 | 900 | 5000 |
| `piebla.5` | Forge new types of broadswords and sabres (cavalry and sword clansman attack +5) | 1 | 5 | 15.62 | 0 | 0 | 0 | 4000 | 7900 | 0 |
| `piebla.6` | Forge new cuirasses (armoured soldiers defence +2) | 1 | 2 | 15.62 | 0 | 0 | 0 | 4950 | 10500 | 0 |
| `piecen.1` | — | 1 | 0 | 9.38 | 30000 | 0 | 0 | 5000 | 2000 | 2000 |
| `piesta.cuirassier.1.1` | Stable cuirassier damage +1 (lvl 2) | 2 | 1 | 15.62 | 12000 | 0 | 0 | 600 | 0 | 0 |
| `piesta.cuirassier.1.2` | Stable cuirassier damage +1 (lvl 3) | 3 | 1 | 15.62 | 32000 | 0 | 0 | 1300 | 0 | 0 |
| `piesta.cuirassier.1.3` | Stable cuirassier damage +1 (lvl 4) | 4 | 1 | 15.62 | 62000 | 0 | 0 | 2200 | 0 | 0 |
| `piesta.cuirassier.1.4` | Stable cuirassier damage +2 (lvl 5) | 5 | 2 | 15.62 | 61000 | 0 | 0 | 3150 | 0 | 0 |
| `piesta.cuirassier.1.5` | Stable cuirassier damage +2 (lvl 6) | 6 | 2 | 15.62 | 57055 | 0 | 0 | 4100 | 0 | 0 |
| `piesta.cuirassier.1.6` | Stable cuirassier damage +3 (lvl 7) | 7 | 3 | 15.62 | 49050 | 0 | 0 | 8020 | 0 | 0 |
| `piesta.cuirassier.2.1` | Stable cuirassier protection +2 (lvl 2) | 2 | 2 | 15.62 | 1760 | 0 | 0 | 350 | 1000 | 0 |
| `piesta.cuirassier.2.2` | Stable cuirassier protection +3 (lvl 3) | 3 | 3 | 15.62 | 3000 | 0 | 0 | 750 | 2000 | 0 |
| `piesta.cuirassier.2.3` | Stable cuirassier protection +3 (lvl 4) | 4 | 3 | 15.62 | 7600 | 0 | 0 | 300 | 3030 | 0 |
| `piesta.cuirassier.2.4` | Stable cuirassier protection +2 (lvl 5) | 5 | 2 | 15.62 | 8700 | 0 | 0 | 6200 | 100 | 0 |
| `piesta.cuirassier.2.5` | Stable cuirassier protection +1 (lvl 6) | 6 | 1 | 15.62 | 8700 | 0 | 0 | 2350 | 5000 | 0 |
| `piesta.cuirassier.2.6` | Stable cuirassier protection +1 (lvl 7) | 7 | 1 | 15.62 | 9700 | 0 | 0 | 4444 | 7060 | 0 |
| `piesta.dragoon.1.1` | Stable dragoon damage +1 (lvl 2) | 2 | 1 | 15.62 | 500 | 0 | 0 | 150 | 0 | 0 |
| `piesta.dragoon.1.2` | Stable dragoon damage +1 (lvl 3) | 3 | 1 | 15.62 | 700 | 0 | 0 | 200 | 0 | 0 |
| `piesta.dragoon.1.3` | Stable dragoon damage +2 (lvl 4) | 4 | 2 | 15.62 | 900 | 0 | 0 | 340 | 0 | 0 |
| `piesta.dragoon.1.4` | Stable dragoon damage +1 (lvl 5) | 5 | 1 | 15.62 | 0 | 0 | 0 | 0 | 0 | 0 |
| `piesta.dragoon.1.5` | Stable dragoon damage +1 (lvl 6) | 6 | 1 | 15.62 | 0 | 0 | 0 | 0 | 0 | 0 |
| `piesta.dragoon.1.6` | Stable dragoon damage +3 (lvl 7) | 7 | 3 | 15.62 | 0 | 0 | 0 | 0 | 0 | 0 |
| `piesta.dragoon.2.1` | Stable dragoon protection +1 (lvl 2) | 2 | 1 | 15.62 | 900 | 0 | 0 | 150 | 0 | 0 |
| `piesta.dragoon.2.2` | Stable dragoon protection +2 (lvl 3) | 3 | 2 | 15.62 | 6600 | 0 | 0 | 750 | 0 | 0 |
| `piesta.dragoon.2.3` | Stable dragoon protection +2 (lvl 4) | 4 | 2 | 15.62 | 5000 | 0 | 0 | 1250 | 0 | 0 |
| `piesta.dragoon.2.4` | Stable dragoon protection +1 (lvl 5) | 5 | 1 | 15.62 | 3000 | 0 | 0 | 700 | 0 | 0 |
| `piesta.dragoon.2.5` | Stable dragoon protection +2 (lvl 6) | 6 | 2 | 15.62 | 1000 | 0 | 0 | 2350 | 0 | 0 |
| `piesta.dragoon.2.6` | Stable dragoon protection +2 (lvl 7) | 7 | 2 | 15.62 | 6001 | 0 | 0 | 6000 | 0 | 0 |
| `piesta.dragoon18pie.1.1` | Stable dragoon18pie damage +2 (lvl 2) | 2 | 2 | 15.62 | 2000 | 0 | 0 | 100 | 0 | 0 |
| `piesta.dragoon18pie.1.2` | Stable dragoon18pie damage +2 (lvl 3) | 3 | 2 | 15.62 | 9000 | 0 | 0 | 350 | 0 | 0 |
| `piesta.dragoon18pie.1.3` | Stable dragoon18pie damage +4 (lvl 4) | 4 | 4 | 15.62 | 12000 | 0 | 0 | 400 | 0 | 0 |
| `piesta.dragoon18pie.1.4` | Stable dragoon18pie damage +2 (lvl 5) | 5 | 2 | 15.62 | 23000 | 0 | 0 | 580 | 0 | 0 |
| `piesta.dragoon18pie.1.5` | Stable dragoon18pie damage +2 (lvl 6) | 6 | 2 | 15.62 | 32000 | 0 | 0 | 680 | 0 | 0 |
| `piesta.dragoon18pie.1.6` | Stable dragoon18pie damage +4 (lvl 7) | 7 | 4 | 15.62 | 42000 | 0 | 0 | 780 | 0 | 0 |
| `piesta.dragoon18pie.2.1` | Stable dragoon18pie protection +1 (lvl 2) | 2 | 1 | 15.62 | 760 | 0 | 0 | 935 | 0 | 0 |
| `piesta.dragoon18pie.2.2` | Stable dragoon18pie protection +1 (lvl 3) | 3 | 1 | 15.62 | 1260 | 0 | 0 | 1150 | 0 | 0 |
| `piesta.dragoon18pie.2.3` | Stable dragoon18pie protection +2 (lvl 4) | 4 | 2 | 15.62 | 15600 | 0 | 0 | 2350 | 0 | 0 |
| `piesta.dragoon18pie.2.4` | Stable dragoon18pie protection +1 (lvl 5) | 5 | 1 | 15.62 | 17600 | 0 | 0 | 4350 | 0 | 0 |
| `piesta.dragoon18pie.2.5` | Stable dragoon18pie protection +1 (lvl 6) | 6 | 1 | 15.62 | 19600 | 0 | 0 | 5350 | 0 | 0 |
| `piesta.dragoon18pie.2.6` | Stable dragoon18pie protection +2 (lvl 7) | 7 | 2 | 15.62 | 21760 | 0 | 0 | 8350 | 0 | 0 |
| `piesta.hussar.1.1` | Stable hussar damage +1 (lvl 2) | 2 | 1 | 15.62 | 0 | 0 | 0 | 1800 | 1000 | 0 |
| `piesta.hussar.1.2` | Stable hussar damage +2 (lvl 3) | 3 | 2 | 15.62 | 0 | 0 | 0 | 3800 | 2000 | 0 |
| `piesta.hussar.1.3` | Stable hussar damage +3 (lvl 4) | 4 | 3 | 15.62 | 20200 | 0 | 0 | 0 | 2000 | 0 |
| `piesta.hussar.1.4` | Stable hussar damage +4 (lvl 5) | 5 | 4 | 15.62 | 32000 | 0 | 0 | 0 | 3000 | 0 |
| `piesta.hussar.1.5` | Stable hussar damage +1 (lvl 6) | 6 | 1 | 15.62 | 49200 | 0 | 0 | 0 | 3500 | 0 |
| `piesta.hussar.1.6` | Stable hussar damage +1 (lvl 7) | 7 | 1 | 15.62 | 20000 | 0 | 0 | 0 | 6000 | 0 |
| `piesta.hussar.2.1` | Stable hussar protection +1 (lvl 2) | 2 | 1 | 15.62 | 1760 | 0 | 0 | 1350 | 0 | 0 |
| `piesta.hussar.2.2` | Stable hussar protection +1 (lvl 3) | 3 | 1 | 15.62 | 1900 | 0 | 0 | 2350 | 0 | 0 |
| `piesta.hussar.2.3` | Stable hussar protection +1 (lvl 4) | 4 | 1 | 15.62 | 1600 | 0 | 0 | 5350 | 0 | 0 |
| `piesta.hussar.2.4` | Stable hussar protection +2 (lvl 5) | 5 | 2 | 15.62 | 8000 | 0 | 0 | 8350 | 0 | 0 |
| `piesta.hussar.2.5` | Stable hussar protection +2 (lvl 6) | 6 | 2 | 15.62 | 2000 | 0 | 0 | 15350 | 0 | 0 |
| `piesta.hussar.2.6` | Stable hussar protection +3 (lvl 7) | 7 | 3 | 15.62 | 56000 | 0 | 0 | 20150 | 0 | 0 |
| `piesta.reiter.1.1` | Stable reiter damage +1 (lvl 2) | 2 | 1 | 15.62 | 500 | 0 | 0 | 100 | 0 | 0 |
| `piesta.reiter.1.2` | Stable reiter damage +2 (lvl 3) | 3 | 2 | 15.62 | 900 | 0 | 0 | 220 | 0 | 0 |
| `piesta.reiter.1.3` | Stable reiter damage +1 (lvl 4) | 4 | 1 | 15.62 | 4400 | 0 | 0 | 280 | 0 | 0 |
| `piesta.reiter.1.4` | Stable reiter damage +1 (lvl 5) | 5 | 1 | 15.62 | 2250 | 0 | 0 | 320 | 0 | 0 |
| `piesta.reiter.1.5` | Stable reiter damage +1 (lvl 6) | 6 | 1 | 15.62 | 3030 | 0 | 0 | 600 | 0 | 0 |
| `piesta.reiter.1.6` | Stable reiter damage +1 (lvl 7) | 7 | 1 | 15.62 | 7000 | 0 | 0 | 1800 | 0 | 0 |
| `piesta.reiter.2.1` | Stable reiter protection +2 (lvl 2) | 2 | 2 | 15.62 | 200 | 0 | 0 | 135 | 300 | 0 |
| `piesta.reiter.2.2` | Stable reiter protection +3 (lvl 3) | 3 | 3 | 15.62 | 600 | 0 | 0 | 100 | 400 | 0 |
| `piesta.reiter.2.3` | Stable reiter protection +3 (lvl 4) | 4 | 3 | 15.62 | 800 | 0 | 0 | 200 | 560 | 0 |
| `piesta.reiter.2.4` | Stable reiter protection +2 (lvl 5) | 5 | 2 | 15.62 | 1600 | 0 | 0 | 300 | 640 | 0 |
| `piesta.reiter.2.5` | Stable reiter protection +1 (lvl 6) | 6 | 1 | 15.62 | 3200 | 0 | 0 | 350 | 300 | 0 |
| `piesta.reiter.2.6` | Stable reiter protection +1 (lvl 7) | 7 | 1 | 15.62 | 16000 | 0 | 0 | 1000 | 5000 | 0 |
| `ukrwwa.1` | — | 2 | 5 | 0.03 | 0 | 400 | 0 | 0 | 0 | 0 |

### sax — Saxony

| sid | имя (EN) | level | value | время (s) | F | W | S | G | I | C |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `eurcoa.1` | — | 2 | 5 | 9.38 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `eurcoa.2` | — | 3 | 8 | 9.38 | 5250 | 0 | 0 | 4950 | 0 | 0 |
| `eurcoa.3` | — | 4 | 10 | 9.38 | 12500 | 0 | 0 | 9250 | 0 | 0 |
| `eurcoa.4` | — | 5 | 12 | 9.38 | 15800 | 0 | 0 | 18500 | 0 | 0 |
| `eurcoa.5` | — | 6 | 15 | 9.38 | 19800 | 0 | 0 | 21050 | 0 | 0 |
| `eurcoa.6` | — | 7 | 40 | 9.38 | 50200 | 0 | 0 | 25950 | 0 | 0 |
| `eurgol.1` | — | 2 | 5 | 9.38 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `eurgol.2` | — | 3 | 8 | 9.38 | 5250 | 0 | 0 | 4950 | 0 | 0 |
| `eurgol.3` | — | 4 | 10 | 9.38 | 12500 | 0 | 0 | 9250 | 0 | 0 |
| `eurgol.4` | — | 5 | 12 | 9.38 | 15800 | 0 | 0 | 18500 | 0 | 0 |
| `eurgol.5` | — | 6 | 15 | 9.38 | 19800 | 0 | 0 | 21050 | 0 | 0 |
| `eurgol.6` | — | 7 | 40 | 9.38 | 50200 | 0 | 0 | 25950 | 0 | 0 |
| `euriro.1` | — | 2 | 5 | 9.38 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `euriro.2` | — | 3 | 8 | 9.38 | 5250 | 0 | 0 | 4950 | 0 | 0 |
| `euriro.3` | — | 4 | 10 | 9.38 | 12500 | 0 | 0 | 9250 | 0 | 0 |
| `euriro.4` | — | 5 | 12 | 9.38 | 15800 | 0 | 0 | 18500 | 0 | 0 |
| `euriro.5` | — | 6 | 15 | 9.38 | 19800 | 0 | 0 | 21050 | 0 | 0 |
| `euriro.6` | — | 7 | 40 | 9.38 | 50200 | 0 | 0 | 25950 | 0 | 0 |
| `eurpor.1` | — | 1 | 50 | 46.88 | 0 | 20000 | 0 | 1500 | 0 | 0 |
| `eurswa.1` | — | 2 | 5 | 0.03 | 0 | 0 | 500 | 0 | 0 | 0 |
| `eurtow.1` | — | 2 | -20 | 31.25 | 0 | 0 | 0 | 250 | 0 | 0 |
| `eurtow.2` | — | 3 | -20 | 31.25 | 0 | 0 | 0 | 0 | 350 | 0 |
| `eurtow.3` | — | 4 | -10 | 31.25 | 0 | 0 | 0 | 0 | 0 | 400 |
| `eurtow.4` | — | 5 | -10 | 31.25 | 0 | 0 | 0 | 0 | 450 | 0 |
| `eurtow.5` | — | 6 | -10 | 31.25 | 0 | 0 | 0 | 0 | 0 | 500 |
| `ferry.1` | Improve transport vessel design (+%value% capacity) | 2 | 200 | 15.62 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `saxaca.1` | Cultivate new cultures of wheat (harvesting +40%) | 1 | 40 | 15.62 | 0 | 200 | 0 | 325 | 0 | 0 |
| `saxaca.10` | Raise builders' salary (building construction time -75%) | 1 | -7500000 | 15.62 | 0 | 0 | 0 | 6950 | 0 | 0 |
| `saxaca.11` | Research new fortification grades (durability of walls and towers +80) | 1 | 80 | 15.62 | 0 | 0 | 16200 | 1500 | 0 | 0 |
| `saxaca.12` | Improve firearms: rifled barrel (fire power +10%) | 1 | 10 | 15.62 | 0 | 0 | 0 | 0 | 5000 | 0 |
| `saxaca.13` | Research granular gunpowder (fire power +10%) | 1 | 10 | 15.62 | 0 | 0 | 0 | 4000 | 0 | 0 |
| `saxaca.14` | Research new sulphur purification methods (fire power +15%) | 1 | 15 | 15.62 | 0 | 0 | 0 | 7000 | 0 | 0 |
| `saxaca.15` | Research new nitre purification methods (fire power +25%) | 1 | 25 | 15.62 | 0 | 0 | 0 | 0 | 0 | 11000 |
| `saxaca.16` | Research improved additions to gunpowder formula (artillery range +5%) | 1 | 5 | 15.62 | 0 | 0 | 0 | 2000 | 12150 | 0 |
| `saxaca.17` | Design new barrel types: unicorn, carronade (artillery range +10%) | 1 | 10 | 15.62 | 0 | 0 | 3000 | 4550 | 19200 | 0 |
| `saxaca.18` | Design more durable gun carriage: Gribovalle system (artillery durability +50%) | 1 | 50 | 15.62 | 0 | 0 | 0 | 500 | 3830 | 1500 |
| `saxaca.19` | Design multi-barrelled cannon | 1 | 0 | 15.62 | 0 | 0 | 0 | 1500 | 0 | 2500 |
| `saxaca.2` | Cultivate new cultures of rye (harvesting +50%) | 1 | 50 | 15.62 | 0 | 2400 | 0 | 625 | 0 | 0 |
| `saxaca.20` | Research new sighting devices for artillery (artillery accuracy +35%) | 1 | -35 | 15.62 | 0 | 3540 | 0 | 2000 | 0 | 7250 |
| `saxaca.21` | Finance artillery repair shops (repair all artillery) | 1 | 25 | 15.62 | 0 | 350 | 0 | 100 | 0 | 250 |
| `saxaca.22` | Develop geology (previously hidden deposits appear on the map) | 1 | 0 | 15.62 | 0 | 0 | 0 | 250 | 0 | 0 |
| `saxaca.23` | Develop mining (stone excavation efficiency +100%) | 1 | 100 | 15.62 | 0 | 0 | 0 | 1550 | 3000 | 0 |
| `saxaca.24` | Raise miners' salary (stone excavation efficiency +200%) | 1 | 200 | 15.62 | 4200 | 0 | 0 | 1550 | 0 | 12520 |
| `saxaca.25` | Design Montgolfier (reveals the whole map) | 1 | 0 | 15.62 | 0 | 0 | 0 | 5750 | 0 | 0 |
| `saxaca.26` | Develop medical science (heals all live units) | 1 | 50 | 31.25 | 0 | 0 | 0 | 200 | 0 | 200 |
| `saxaca.27` | Develop mathematics (artillery accuracy +35%) | 1 | -35 | 15.62 | 0 | 9540 | 0 | 12000 | 0 | 65200 |
| `saxaca.28` | Design new rigging types (ship speed +40%) | 1 | 40 | 15.62 | 0 | 65400 | 0 | 24050 | 0 | 0 |
| `saxaca.29` | Design new rib system and new hulls (battleship construction) | 1 | 0 | 15.62 | 0 | 32300 | 0 | 6800 | 9000 | 12800 |
| `saxaca.3` | Raise agriculturists' salary (harvesting +50%) | 1 | 50 | 15.62 | 0 | 3600 | 0 | 850 | 0 | 0 |
| `saxaca.30` | Train carpenters (shipbuilding speed x10) | 1 | -5000000 | 15.62 | 0 | 2300 | 42700 | 1150 | 0 | 0 |
| `saxaca.31` | Design wheellock (rate of fire +30%) | 1 | -30 | 15.62 | 0 | 0 | 6000 | 5500 | 4200 | 0 |
| `saxaca.32` | Design flintlock (musket cost -50%) | 1 | 0 | 15.62 | 0 | 0 | 0 | 6050 | 0 | 7750 |
| `saxaca.33` | Design paper cartridge and iron ramrod (rate of fire +30%) | 1 | -30 | 15.62 | 0 | 5000 | 0 | 5500 | 0 | 15200 |
| `saxaca.34` | Research improved steel grades for cuirasses (armoured soldier defence +2) | 1 | 2 | 15.62 | 0 | 0 | 0 | 9750 | 0 | 0 |
| `saxaca.35` | Design bayonet: barrel-inserted, bayonet with a tube (cold steel weapons +5) | 1 | 5 | 15.62 | 0 | 0 | 0 | 11500 | 0 | 0 |
| `saxaca.36` | Research new steel grades (18c musketeer/grenadier melee attack efficiency +25%) | 1 | 25 | 15.62 | 0 | 0 | 0 | 19500 | 0 | 0 |
| `saxaca.4` | Carry out field melioration (field capacity +200%) | 1 | 200 | 15.62 | 0 | 1000 | 0 | 475 | 0 | 0 |
| `saxaca.5` | Design new tackle and fishing nets (boat efficiency +100%) | 1 | 100 | 15.62 | 0 | 12400 | 0 | 2520 | 0 | 0 |
| `saxaca.6` | Develop new woodworking methods (frigate building) | 1 | 0 | 15.62 | 0 | 12400 | 0 | 7040 | 0 | 0 |
| `saxaca.7` | Build new shipyards for fishing boats (fishing boat cost -85%) | 1 | 0 | 15.62 | 0 | 7300 | 0 | 1220 | 0 | 0 |
| `saxaca.8` | Design new woodworking tools (woodcutting efficiency +100%) | 1 | 100 | 15.62 | 5500 | 0 | 0 | 550 | 0 | 0 |
| `saxaca.9` | Use new construction materials (durability of buildings +85) | 1 | 85 | 15.62 | 0 | 9400 | 7850 | 1150 | 0 | 0 |
| `saxart.cannon.1.1` | — | 2 | — | 10.0 | 0 | 1000 | 500 | 300 | 0 | 0 |
| `saxart.cannon.1.2` | — | 3 | — | 10.0 | 0 | 3000 | 1000 | 500 | 0 | 0 |
| `saxart.cannon.1.3` | — | 4 | — | 10.0 | 0 | 6000 | 2000 | 1000 | 0 | 0 |
| `saxart.cannon.1.4` | — | 5 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `saxart.cannon.1.5` | — | 6 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `saxart.cannon.1.6` | — | 7 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `saxart.cannon.2.1` | — | 2 | -2500000 | 10.0 | 0 | 0 | 0 | 500 | 1000 | 0 |
| `saxart.cannon.2.2` | — | 3 | -2500000 | 10.0 | 0 | 0 | 0 | 1000 | 2000 | 0 |
| `saxart.cannon.2.3` | — | 4 | -2500000 | 10.0 | 0 | 0 | 0 | 2000 | 3000 | 0 |
| `saxart.cannon.2.4` | — | 5 | -2000000 | 15.62 | 2560 | 0 | 0 | 0 | 0 | 0 |
| `saxart.cannon.2.5` | — | 6 | -2000000 | 15.62 | 3560 | 0 | 0 | 0 | 0 | 0 |
| `saxart.cannon.2.6` | — | 7 | -2000000 | 15.62 | 5560 | 0 | 0 | 0 | 0 | 0 |
| `saxart.howitzer.1.1` | — | 2 | — | 10.0 | 0 | 1000 | 500 | 300 | 0 | 0 |
| `saxart.howitzer.1.2` | — | 3 | — | 10.0 | 0 | 3000 | 1000 | 500 | 0 | 0 |
| `saxart.howitzer.1.3` | — | 4 | — | 10.0 | 0 | 6000 | 2000 | 1000 | 0 | 0 |
| `saxart.howitzer.1.4` | — | 5 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `saxart.howitzer.1.5` | — | 6 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `saxart.howitzer.1.6` | — | 7 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `saxart.howitzer.2.1` | — | 2 | -2500000 | 10.0 | 0 | 0 | 0 | 500 | 1000 | 0 |
| `saxart.howitzer.2.2` | — | 3 | -2500000 | 10.0 | 0 | 0 | 0 | 1000 | 2000 | 0 |
| `saxart.howitzer.2.3` | — | 4 | -2500000 | 10.0 | 0 | 0 | 0 | 2000 | 3000 | 0 |
| `saxart.howitzer.2.4` | — | 5 | -2000000 | 31.25 | 2560 | 0 | 0 | 0 | 0 | 0 |
| `saxart.howitzer.2.5` | — | 6 | -2000000 | 31.25 | 3560 | 0 | 0 | 0 | 0 | 0 |
| `saxart.howitzer.2.6` | — | 7 | -2000000 | 31.25 | 5560 | 0 | 0 | 0 | 0 | 0 |
| `saxba2.drummer18.2.1` | Barracks 18c drummer18 protection +15 (lvl 2) | 2 | 15 | 15.62 | 900 | 0 | 0 | 45 | 0 | 0 |
| `saxba2.grenadiersax.1.1` | Barracks 18c grenadiersax damage +2 (lvl 2) | 2 | 2 | 15.62 | 1000 | 0 | 0 | 800 | 0 | 0 |
| `saxba2.grenadiersax.1.2` | Barracks 18c grenadiersax damage +3 (lvl 3) | 3 | 3 | 15.62 | 13000 | 0 | 0 | 1800 | 0 | 0 |
| `saxba2.grenadiersax.1.3` | Barracks 18c grenadiersax damage +4 (lvl 4) | 4 | 4 | 15.62 | 25000 | 0 | 0 | 1800 | 0 | 0 |
| `saxba2.grenadiersax.1.4` | Barracks 18c grenadiersax damage +5 (lvl 5) | 5 | 5 | 15.62 | 49000 | 0 | 0 | 4800 | 0 | 0 |
| `saxba2.grenadiersax.1.5` | Barracks 18c grenadiersax damage +6 (lvl 6) | 6 | 6 | 15.62 | 54000 | 0 | 0 | 5800 | 0 | 0 |
| `saxba2.grenadiersax.1.6` | Barracks 18c grenadiersax damage +1500 (lvl 7) | 7 | 1500 | 15.62 | 60000 | 0 | 0 | 14590 | 0 | 0 |
| `saxba2.grenadiersax.2.1` | Barracks 18c grenadiersax protection +2 (lvl 2) | 2 | 2 | 15.62 | 7705 | 0 | 0 | 350 | 0 | 0 |
| `saxba2.grenadiersax.2.2` | Barracks 18c grenadiersax protection +2 (lvl 3) | 3 | 2 | 15.62 | 7030 | 0 | 0 | 1350 | 0 | 0 |
| `saxba2.grenadiersax.2.3` | Barracks 18c grenadiersax protection +2 (lvl 4) | 4 | 2 | 15.62 | 21706 | 0 | 0 | 1000 | 0 | 0 |
| `saxba2.grenadiersax.2.4` | Barracks 18c grenadiersax protection +2 (lvl 5) | 5 | 2 | 15.62 | 22556 | 0 | 0 | 5350 | 0 | 0 |
| `saxba2.grenadiersax.2.5` | Barracks 18c grenadiersax protection +2 (lvl 6) | 6 | 2 | 15.62 | 30060 | 0 | 0 | 1750 | 0 | 0 |
| `saxba2.grenadiersax.2.6` | Barracks 18c grenadiersax protection +2 (lvl 7) | 7 | 2 | 15.62 | 62000 | 0 | 0 | 950 | 0 | 0 |
| `saxba2.musketeer18sax.1.1` | Barracks 18c musketeer18sax damage +1 (lvl 2) | 2 | 1 | 15.62 | 9000 | 0 | 0 | 200 | 0 | 0 |
| `saxba2.musketeer18sax.1.2` | Barracks 18c musketeer18sax damage +2 (lvl 3) | 3 | 2 | 15.62 | 600 | 0 | 0 | 200 | 0 | 0 |
| `saxba2.musketeer18sax.1.3` | Barracks 18c musketeer18sax damage +2 (lvl 4) | 4 | 2 | 15.62 | 4000 | 0 | 0 | 100 | 0 | 0 |
| `saxba2.musketeer18sax.1.4` | Barracks 18c musketeer18sax damage +1 (lvl 5) | 5 | 1 | 15.62 | 500 | 0 | 0 | 2100 | 0 | 0 |
| `saxba2.musketeer18sax.1.5` | Barracks 18c musketeer18sax damage +2 (lvl 6) | 6 | 2 | 15.62 | 3000 | 0 | 0 | 200 | 0 | 0 |
| `saxba2.musketeer18sax.1.6` | Barracks 18c musketeer18sax damage +2 (lvl 7) | 7 | 2 | 15.62 | 3500 | 0 | 0 | 1400 | 0 | 0 |
| `saxba2.musketeer18sax.2.1` | Barracks 18c musketeer18sax protection +1 (lvl 2) | 2 | 1 | 15.62 | 5706 | 0 | 0 | 750 | 0 | 0 |
| `saxba2.musketeer18sax.2.2` | Barracks 18c musketeer18sax protection +2 (lvl 3) | 3 | 2 | 15.62 | 9030 | 0 | 0 | 1050 | 0 | 0 |
| `saxba2.musketeer18sax.2.3` | Barracks 18c musketeer18sax protection +2 (lvl 4) | 4 | 2 | 15.62 | 32706 | 0 | 0 | 2900 | 0 | 0 |
| `saxba2.musketeer18sax.2.4` | Barracks 18c musketeer18sax protection +1 (lvl 5) | 5 | 1 | 15.62 | 39556 | 0 | 0 | 5450 | 0 | 0 |
| `saxba2.musketeer18sax.2.5` | Barracks 18c musketeer18sax protection +2 (lvl 6) | 6 | 2 | 15.62 | 30060 | 0 | 0 | 1350 | 0 | 0 |
| `saxba2.musketeer18sax.2.6` | Barracks 18c musketeer18sax protection +2 (lvl 7) | 7 | 2 | 15.62 | 37600 | 0 | 0 | 1350 | 0 | 0 |
| `saxba2.officer18.1.1` | Barracks 18c officer18 damage +30 (lvl 2) | 2 | 30 | 15.62 | 1200 | 0 | 0 | 750 | 0 | 0 |
| `saxba2.officer18.2.1` | Barracks 18c officer18 protection +12 (lvl 2) | 2 | 12 | 15.62 | 1500 | 0 | 0 | 375 | 0 | 0 |
| `saxba2.pikeman18.1.1` | Barracks 18c pikeman18 damage +2 (lvl 2) | 2 | 2 | 15.62 | 2000 | 0 | 0 | 800 | 0 | 0 |
| `saxba2.pikeman18.1.2` | Barracks 18c pikeman18 damage +2 (lvl 3) | 3 | 2 | 15.62 | 8000 | 0 | 0 | 1200 | 0 | 0 |
| `saxba2.pikeman18.1.3` | Barracks 18c pikeman18 damage +2 (lvl 4) | 4 | 2 | 15.62 | 20000 | 0 | 0 | 2500 | 0 | 0 |
| `saxba2.pikeman18.1.4` | Barracks 18c pikeman18 damage +2 (lvl 5) | 5 | 2 | 15.62 | 32000 | 0 | 0 | 2800 | 0 | 0 |
| `saxba2.pikeman18.1.5` | Barracks 18c pikeman18 damage +2 (lvl 6) | 6 | 2 | 15.62 | 32000 | 0 | 0 | 3800 | 0 | 0 |
| `saxba2.pikeman18.1.6` | Barracks 18c pikeman18 damage +2 (lvl 7) | 7 | 2 | 15.62 | 40500 | 0 | 0 | 4800 | 0 | 0 |
| `saxba2.pikeman18.2.1` | Barracks 18c pikeman18 protection +2 (lvl 2) | 2 | 2 | 15.62 | 1500 | 0 | 0 | 500 | 0 | 0 |
| `saxba2.pikeman18.2.2` | Barracks 18c pikeman18 protection +3 (lvl 3) | 3 | 3 | 15.62 | 7000 | 0 | 0 | 1500 | 0 | 0 |
| `saxba2.pikeman18.2.3` | Barracks 18c pikeman18 protection +2 (lvl 4) | 4 | 2 | 15.62 | 37000 | 0 | 0 | 2000 | 0 | 0 |
| `saxba2.pikeman18.2.4` | Barracks 18c pikeman18 protection +3 (lvl 5) | 5 | 3 | 15.62 | 37000 | 0 | 0 | 5500 | 0 | 0 |
| `saxba2.pikeman18.2.5` | Barracks 18c pikeman18 protection +2 (lvl 6) | 6 | 2 | 15.62 | 37000 | 0 | 0 | 5500 | 0 | 0 |
| `saxba2.pikeman18.2.6` | Barracks 18c pikeman18 protection +3 (lvl 7) | 7 | 3 | 15.62 | 64600 | 0 | 0 | 5500 | 0 | 0 |
| `saxbar.1` | — | 1 | 140 | 15.62 | 750 | 0 | 0 | 250 | 0 | 0 |
| `saxbar.2` | — | 2 | 180 | 15.62 | 25600 | 0 | 0 | 3350 | 2000 | 0 |
| `saxbar.drummer.2.1` | Barracks 17c drummer protection +12 (lvl 2) | 2 | 12 | 15.62 | 1205 | 0 | 0 | 90 | 0 | 0 |
| `saxbar.musketeer.1.1` | Barracks 17c musketeer damage +1 (lvl 2) | 2 | 1 | 15.62 | 2000 | 0 | 0 | 100 | 0 | 0 |
| `saxbar.musketeer.1.2` | Barracks 17c musketeer damage +1 (lvl 3) | 3 | 1 | 15.62 | 1000 | 0 | 0 | 300 | 0 | 0 |
| `saxbar.musketeer.1.3` | Barracks 17c musketeer damage +2 (lvl 4) | 4 | 2 | 15.62 | 500 | 0 | 0 | 700 | 0 | 0 |
| `saxbar.musketeer.2.1` | Barracks 17c musketeer protection +1 (lvl 2) | 2 | 1 | 15.62 | 170 | 0 | 0 | 50 | 100 | 0 |
| `saxbar.musketeer.2.2` | Barracks 17c musketeer protection +2 (lvl 3) | 3 | 2 | 15.62 | 405 | 0 | 0 | 150 | 200 | 0 |
| `saxbar.musketeer.2.3` | Barracks 17c musketeer protection +2 (lvl 4) | 4 | 2 | 15.62 | 1570 | 0 | 0 | 100 | 350 | 0 |
| `saxbar.musketeer.2.4` | Barracks 17c musketeer protection +1 (lvl 5) | 5 | 1 | 15.62 | 1556 | 0 | 0 | 550 | 100 | 0 |
| `saxbar.musketeer.2.5` | Barracks 17c musketeer protection +2 (lvl 6) | 6 | 2 | 15.62 | 1060 | 0 | 0 | 850 | 400 | 0 |
| `saxbar.musketeer.2.6` | Barracks 17c musketeer protection +2 (lvl 7) | 7 | 2 | 15.62 | 3700 | 0 | 0 | 450 | 700 | 0 |
| `saxbar.officer.1.1` | Barracks 17c officer damage +20 (lvl 2) | 2 | 20 | 15.62 | 150 | 0 | 0 | 25 | 0 | 0 |
| `saxbar.officer.2.1` | Barracks 17c officer protection +6 (lvl 2) | 2 | 6 | 15.62 | 1650 | 0 | 0 | 395 | 0 | 0 |
| `saxbar.pikeman.1.1` | Barracks 17c pikeman damage +1 (lvl 2) | 2 | 1 | 15.62 | 100 | 0 | 0 | 90 | 0 | 0 |
| `saxbar.pikeman.1.2` | Barracks 17c pikeman damage +2 (lvl 3) | 3 | 2 | 15.62 | 300 | 0 | 0 | 450 | 0 | 0 |
| `saxbar.pikeman.1.3` | Barracks 17c pikeman damage +2 (lvl 4) | 4 | 2 | 15.62 | 4600 | 0 | 0 | 300 | 0 | 0 |
| `saxbar.pikeman.1.4` | Barracks 17c pikeman damage +1 (lvl 5) | 5 | 1 | 15.62 | 9200 | 0 | 0 | 1250 | 0 | 0 |
| `saxbar.pikeman.1.5` | Barracks 17c pikeman damage +2 (lvl 6) | 6 | 2 | 15.62 | 14030 | 0 | 0 | 2600 | 0 | 0 |
| `saxbar.pikeman.1.6` | — | 7 | 2 | 15.62 | 15000 | 0 | 0 | 1875 | 0 | 0 |
| `saxbar.pikeman.2.1` | Barracks 17c pikeman protection +1 (lvl 2) | 2 | 1 | 15.62 | 175 | 0 | 0 | 40 | 0 | 0 |
| `saxbar.pikeman.2.2` | Barracks 17c pikeman protection +1 (lvl 3) | 3 | 1 | 15.62 | 990 | 0 | 0 | 275 | 0 | 0 |
| `saxbar.pikeman.2.3` | Barracks 17c pikeman protection +2 (lvl 4) | 4 | 2 | 15.62 | 4700 | 0 | 0 | 280 | 0 | 0 |
| `saxbar.pikeman.2.4` | Barracks 17c pikeman protection +1 (lvl 5) | 5 | 1 | 15.62 | 9505 | 0 | 0 | 707 | 0 | 0 |
| `saxbar.pikeman.2.5` | Barracks 17c pikeman protection +1 (lvl 6) | 6 | 1 | 15.62 | 17510 | 0 | 0 | 2950 | 0 | 0 |
| `saxbar.pikeman.2.6` | — | 7 | 2 | 15.62 | 11250 | 0 | 0 | 1500 | 0 | 0 |
| `saxbla.1` | Manufacture agricultural equipment (field capacity +100%) | 1 | 100 | 15.62 | 0 | 400 | 0 | 90 | 0 | 0 |
| `saxbla.2` | Forge metal armature and gratings (building defence +50) | 1 | 50 | 15.62 | 0 | 0 | 12320 | 350 | 900 | 0 |
| `saxbla.3` | Forge harnesses for horses (mounted units recruitment speed -33%) | 1 | -3333333 | 15.62 | 0 | 0 | 0 | 3650 | 5300 | 8200 |
| `saxbla.4` | Forge bayonets and broadswords for infantry (18c musketeer/grenadier melee attack +5) | 1 | 5 | 15.62 | 0 | 1300 | 0 | 1500 | 900 | 5000 |
| `saxbla.5` | Forge new types of broadswords and sabres (cavalry and sword clansman attack +5) | 1 | 5 | 15.62 | 0 | 0 | 0 | 4000 | 7900 | 0 |
| `saxbla.6` | Forge new cuirasses (armoured soldiers defence +2) | 1 | 2 | 15.62 | 0 | 0 | 0 | 4950 | 10500 | 0 |
| `saxcen.1` | — | 1 | 0 | 9.38 | 30000 | 0 | 0 | 5000 | 2000 | 2000 |
| `saxsta.dragoon.1.1` | Stable dragoon damage +1 (lvl 2) | 2 | 1 | 15.62 | 700 | 0 | 0 | 250 | 0 | 0 |
| `saxsta.dragoon.1.2` | Stable dragoon damage +1 (lvl 3) | 3 | 1 | 15.62 | 500 | 0 | 0 | 100 | 0 | 0 |
| `saxsta.dragoon.1.3` | Stable dragoon damage +2 (lvl 4) | 4 | 2 | 15.62 | 900 | 0 | 0 | 640 | 0 | 0 |
| `saxsta.dragoon.1.4` | Stable dragoon damage +1 (lvl 5) | 5 | 1 | 15.62 | 0 | 0 | 0 | 0 | 0 | 0 |
| `saxsta.dragoon.1.5` | Stable dragoon damage +1 (lvl 6) | 6 | 1 | 15.62 | 0 | 0 | 0 | 0 | 0 | 0 |
| `saxsta.dragoon.1.6` | Stable dragoon damage +3 (lvl 7) | 7 | 3 | 15.62 | 0 | 0 | 0 | 0 | 0 | 0 |
| `saxsta.dragoon.2.1` | Stable dragoon protection +1 (lvl 2) | 2 | 1 | 15.62 | 500 | 0 | 0 | 250 | 0 | 0 |
| `saxsta.dragoon.2.2` | Stable dragoon protection +2 (lvl 3) | 3 | 2 | 15.62 | 6300 | 0 | 0 | 850 | 0 | 0 |
| `saxsta.dragoon.2.3` | Stable dragoon protection +2 (lvl 4) | 4 | 2 | 15.62 | 4600 | 0 | 0 | 1350 | 0 | 0 |
| `saxsta.dragoon.2.4` | Stable dragoon protection +1 (lvl 5) | 5 | 1 | 15.62 | 2500 | 0 | 0 | 750 | 0 | 0 |
| `saxsta.dragoon.2.5` | Stable dragoon protection +2 (lvl 6) | 6 | 2 | 15.62 | 800 | 0 | 0 | 2750 | 0 | 0 |
| `saxsta.dragoon.2.6` | Stable dragoon protection +2 (lvl 7) | 7 | 2 | 15.62 | 2001 | 0 | 0 | 8200 | 0 | 0 |
| `saxsta.dragoon18.1.1` | Stable dragoon18 damage +2 (lvl 2) | 2 | 2 | 15.62 | 4500 | 0 | 0 | 200 | 0 | 0 |
| `saxsta.dragoon18.1.2` | Stable dragoon18 damage +2 (lvl 3) | 3 | 2 | 15.62 | 5500 | 0 | 0 | 250 | 0 | 0 |
| `saxsta.dragoon18.1.3` | Stable dragoon18 damage +4 (lvl 4) | 4 | 4 | 15.62 | 22000 | 0 | 0 | 500 | 0 | 0 |
| `saxsta.dragoon18.1.4` | Stable dragoon18 damage +2 (lvl 5) | 5 | 2 | 15.62 | 13000 | 0 | 0 | 480 | 0 | 0 |
| `saxsta.dragoon18.1.5` | Stable dragoon18 damage +2 (lvl 6) | 6 | 2 | 15.62 | 42000 | 0 | 0 | 780 | 0 | 0 |
| `saxsta.dragoon18.1.6` | Stable dragoon18 damage +4 (lvl 7) | 7 | 4 | 15.62 | 32000 | 0 | 0 | 680 | 0 | 0 |
| `saxsta.dragoon18.2.1` | Stable dragoon18 protection +1 (lvl 2) | 2 | 1 | 15.62 | 750 | 0 | 0 | 935 | 0 | 0 |
| `saxsta.dragoon18.2.2` | Stable dragoon18 protection +1 (lvl 3) | 3 | 1 | 15.62 | 1260 | 0 | 0 | 1150 | 0 | 0 |
| `saxsta.dragoon18.2.3` | Stable dragoon18 protection +2 (lvl 4) | 4 | 2 | 15.62 | 10600 | 0 | 0 | 2350 | 0 | 0 |
| `saxsta.dragoon18.2.4` | Stable dragoon18 protection +1 (lvl 5) | 5 | 1 | 15.62 | 22600 | 0 | 0 | 5350 | 0 | 0 |
| `saxsta.dragoon18.2.5` | Stable dragoon18 protection +2 (lvl 6) | 6 | 2 | 15.62 | 19600 | 0 | 0 | 3350 | 0 | 0 |
| `saxsta.dragoon18.2.6` | Stable dragoon18 protection +3 (lvl 7) | 7 | 3 | 15.62 | 15760 | 0 | 0 | 9350 | 0 | 0 |
| `saxsta.guardcavalrysax.1.1` | Stable guardcavalrysax damage +2 (lvl 2) | 2 | 2 | 15.62 | 10000 | 0 | 0 | 200 | 0 | 0 |
| `saxsta.guardcavalrysax.1.2` | Stable guardcavalrysax damage +2 (lvl 3) | 3 | 2 | 15.62 | 34000 | 0 | 0 | 1700 | 0 | 0 |
| `saxsta.guardcavalrysax.1.3` | Stable guardcavalrysax damage +3 (lvl 4) | 4 | 3 | 15.62 | 64000 | 0 | 0 | 2100 | 0 | 0 |
| `saxsta.guardcavalrysax.1.4` | Stable guardcavalrysax damage +1 (lvl 5) | 5 | 1 | 15.62 | 58000 | 0 | 0 | 4150 | 0 | 0 |
| `saxsta.guardcavalrysax.1.5` | Stable guardcavalrysax damage +1 (lvl 6) | 6 | 1 | 15.62 | 59055 | 0 | 0 | 3100 | 0 | 0 |
| `saxsta.guardcavalrysax.1.6` | Stable guardcavalrysax damage +1 (lvl 7) | 7 | 1 | 15.62 | 47050 | 0 | 0 | 8150 | 0 | 0 |
| `saxsta.guardcavalrysax.2.1` | Stable guardcavalrysax protection +2 (lvl 2) | 2 | 2 | 15.62 | 1520 | 0 | 0 | 450 | 1000 | 0 |
| `saxsta.guardcavalrysax.2.2` | Stable guardcavalrysax protection +2 (lvl 3) | 3 | 2 | 15.62 | 7000 | 0 | 0 | 750 | 2000 | 0 |
| `saxsta.guardcavalrysax.2.3` | Stable guardcavalrysax protection +3 (lvl 4) | 4 | 3 | 15.62 | 3600 | 0 | 0 | 3300 | 3050 | 0 |
| `saxsta.guardcavalrysax.2.4` | Stable guardcavalrysax protection +3 (lvl 5) | 5 | 3 | 15.62 | 8700 | 0 | 0 | 3200 | 200 | 0 |
| `saxsta.guardcavalrysax.2.5` | Stable guardcavalrysax protection +1 (lvl 6) | 6 | 1 | 15.62 | 8700 | 0 | 0 | 2650 | 4300 | 0 |
| `saxsta.guardcavalrysax.2.6` | Stable guardcavalrysax protection +1 (lvl 7) | 7 | 1 | 15.62 | 11200 | 0 | 0 | 4700 | 6760 | 0 |
| `saxsta.hussar.1.1` | Stable hussar damage +1 (lvl 2) | 2 | 1 | 15.62 | 0 | 0 | 0 | 1200 | 1500 | 0 |
| `saxsta.hussar.1.2` | Stable hussar damage +2 (lvl 3) | 3 | 2 | 15.62 | 0 | 0 | 0 | 4400 | 1500 | 0 |
| `saxsta.hussar.1.3` | Stable hussar damage +3 (lvl 4) | 4 | 3 | 15.62 | 10200 | 0 | 0 | 0 | 2500 | 0 |
| `saxsta.hussar.1.4` | Stable hussar damage +4 (lvl 5) | 5 | 4 | 15.62 | 42000 | 0 | 0 | 0 | 3500 | 0 |
| `saxsta.hussar.1.5` | Stable hussar damage +1 (lvl 6) | 6 | 1 | 15.62 | 29200 | 0 | 0 | 0 | 5500 | 0 |
| `saxsta.hussar.1.6` | Stable hussar damage +1 (lvl 7) | 7 | 1 | 15.62 | 40000 | 0 | 0 | 0 | 4400 | 0 |
| `saxsta.hussar.2.1` | Stable hussar protection +1 (lvl 2) | 2 | 1 | 15.62 | 500 | 0 | 0 | 350 | 0 | 0 |
| `saxsta.hussar.2.2` | Stable hussar protection +1 (lvl 3) | 3 | 1 | 15.62 | 3900 | 0 | 0 | 3350 | 0 | 0 |
| `saxsta.hussar.2.3` | Stable hussar protection +1 (lvl 4) | 4 | 1 | 15.62 | 1100 | 0 | 0 | 5350 | 0 | 0 |
| `saxsta.hussar.2.4` | Stable hussar protection +2 (lvl 5) | 5 | 2 | 15.62 | 7800 | 0 | 0 | 8350 | 0 | 0 |
| `saxsta.hussar.2.5` | Stable hussar protection +2 (lvl 6) | 6 | 2 | 15.62 | 1700 | 0 | 0 | 17350 | 0 | 0 |
| `saxsta.hussar.2.6` | Stable hussar protection +3 (lvl 7) | 7 | 3 | 15.62 | 55200 | 0 | 0 | 17150 | 0 | 0 |
| `saxsta.reiter.1.1` | Stable reiter damage +1 (lvl 2) | 2 | 1 | 15.62 | 500 | 0 | 0 | 100 | 0 | 0 |
| `saxsta.reiter.1.2` | Stable reiter damage +2 (lvl 3) | 3 | 2 | 15.62 | 900 | 0 | 0 | 220 | 0 | 0 |
| `saxsta.reiter.1.3` | Stable reiter damage +1 (lvl 4) | 4 | 1 | 15.62 | 4400 | 0 | 0 | 280 | 0 | 0 |
| `saxsta.reiter.1.4` | Stable reiter damage +1 (lvl 5) | 5 | 1 | 15.62 | 2250 | 0 | 0 | 320 | 0 | 0 |
| `saxsta.reiter.1.5` | Stable reiter damage +1 (lvl 6) | 6 | 1 | 15.62 | 3030 | 0 | 0 | 600 | 0 | 0 |
| `saxsta.reiter.1.6` | Stable reiter damage +1 (lvl 7) | 7 | 1 | 15.62 | 7000 | 0 | 0 | 1800 | 0 | 0 |
| `saxsta.reiter.2.1` | Stable reiter protection +2 (lvl 2) | 2 | 2 | 15.62 | 200 | 0 | 0 | 135 | 300 | 0 |
| `saxsta.reiter.2.2` | Stable reiter protection +3 (lvl 3) | 3 | 3 | 15.62 | 600 | 0 | 0 | 100 | 400 | 0 |
| `saxsta.reiter.2.3` | Stable reiter protection +3 (lvl 4) | 4 | 3 | 15.62 | 800 | 0 | 0 | 200 | 560 | 0 |
| `saxsta.reiter.2.4` | Stable reiter protection +2 (lvl 5) | 5 | 2 | 15.62 | 1600 | 0 | 0 | 300 | 640 | 0 |
| `saxsta.reiter.2.5` | Stable reiter protection +1 (lvl 6) | 6 | 1 | 15.62 | 3200 | 0 | 0 | 350 | 300 | 0 |
| `saxsta.reiter.2.6` | Stable reiter protection +1 (lvl 7) | 7 | 1 | 15.62 | 16000 | 0 | 0 | 1000 | 5000 | 0 |
| `ukrwwa.1` | — | 2 | 5 | 0.03 | 0 | 400 | 0 | 0 | 0 | 0 |

### bav — Bavaria

| sid | имя (EN) | level | value | время (s) | F | W | S | G | I | C |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `bavaca.1` | Cultivate new cultures of wheat (harvesting +40%) | 1 | 40 | 15.62 | 0 | 200 | 0 | 325 | 0 | 0 |
| `bavaca.10` | Raise builders' salary (building construction time -75%) | 1 | -7500000 | 15.62 | 0 | 0 | 0 | 6950 | 0 | 0 |
| `bavaca.11` | Research new fortification grades (durability of walls and towers +80) | 1 | 80 | 15.62 | 0 | 0 | 16200 | 1500 | 0 | 0 |
| `bavaca.12` | Improve firearms: rifled barrel (fire power +10%) | 1 | 10 | 15.62 | 0 | 0 | 0 | 0 | 5000 | 0 |
| `bavaca.13` | Research granular gunpowder (fire power +10%) | 1 | 10 | 15.62 | 0 | 0 | 0 | 4000 | 0 | 0 |
| `bavaca.14` | Research new sulphur purification methods (fire power +15%) | 1 | 15 | 15.62 | 0 | 0 | 0 | 7000 | 0 | 0 |
| `bavaca.15` | Research new nitre purification methods (fire power +25%) | 1 | 25 | 15.62 | 0 | 0 | 0 | 0 | 0 | 11000 |
| `bavaca.16` | Research improved additions to gunpowder formula (artillery range +5%) | 1 | 5 | 15.62 | 0 | 0 | 0 | 2000 | 12150 | 0 |
| `bavaca.17` | Design new barrel types: unicorn, carronade (artillery range +10%) | 1 | 10 | 15.62 | 0 | 0 | 3000 | 4550 | 19200 | 0 |
| `bavaca.18` | Design more durable gun carriage: Gribovalle system (artillery durability +50%) | 1 | 50 | 15.62 | 0 | 0 | 0 | 500 | 3830 | 1500 |
| `bavaca.19` | Design multi-barrelled cannon | 1 | 0 | 15.62 | 0 | 0 | 0 | 1500 | 0 | 2500 |
| `bavaca.2` | Cultivate new cultures of rye (harvesting +50%) | 1 | 50 | 15.62 | 0 | 2400 | 0 | 625 | 0 | 0 |
| `bavaca.20` | Research new sighting devices for artillery (artillery accuracy +35%) | 1 | -35 | 15.62 | 0 | 3540 | 0 | 2000 | 0 | 7250 |
| `bavaca.21` | Finance artillery repair shops (repair all artillery) | 1 | 25 | 15.62 | 0 | 350 | 0 | 100 | 0 | 250 |
| `bavaca.22` | Develop geology (previously hidden deposits appear on the map) | 1 | 0 | 15.62 | 0 | 0 | 0 | 250 | 0 | 0 |
| `bavaca.23` | Develop mining (stone excavation efficiency +100%) | 1 | 100 | 15.62 | 0 | 0 | 0 | 1550 | 3000 | 0 |
| `bavaca.24` | Raise miners' salary (stone excavation efficiency +200%) | 1 | 200 | 15.62 | 4200 | 0 | 0 | 1550 | 0 | 12520 |
| `bavaca.25` | Design Montgolfier (reveals the whole map) | 1 | 0 | 15.62 | 0 | 0 | 0 | 5750 | 0 | 0 |
| `bavaca.26` | Develop medical science (heals all live units) | 1 | 50 | 31.25 | 0 | 0 | 0 | 200 | 0 | 200 |
| `bavaca.27` | Develop mathematics (artillery accuracy +35%) | 1 | -35 | 15.62 | 0 | 9540 | 0 | 12000 | 0 | 65200 |
| `bavaca.28` | Design new rigging types (ship speed +40%) | 1 | 40 | 15.62 | 0 | 65400 | 0 | 24050 | 0 | 0 |
| `bavaca.29` | Design new rib system and new hulls (battleship construction) | 1 | 0 | 15.62 | 0 | 32300 | 0 | 6800 | 9000 | 12800 |
| `bavaca.3` | Raise agriculturists' salary (harvesting +50%) | 1 | 50 | 15.62 | 0 | 3600 | 0 | 850 | 0 | 0 |
| `bavaca.30` | Train carpenters (shipbuilding speed x10) | 1 | -5000000 | 15.62 | 0 | 2300 | 42700 | 1150 | 0 | 0 |
| `bavaca.31` | Design wheellock (rate of fire +30%) | 1 | -30 | 15.62 | 0 | 0 | 6000 | 5500 | 4200 | 0 |
| `bavaca.32` | Design flintlock (musket cost -50%) | 1 | 0 | 15.62 | 0 | 0 | 0 | 6050 | 0 | 7750 |
| `bavaca.33` | Design paper cartridge and iron ramrod (rate of fire +30%) | 1 | -30 | 15.62 | 0 | 5000 | 0 | 5500 | 0 | 15200 |
| `bavaca.34` | Research improved steel grades for cuirasses (armoured soldier defence +2) | 1 | 2 | 15.62 | 0 | 0 | 0 | 9750 | 0 | 0 |
| `bavaca.35` | Design bayonet: barrel-inserted, bayonet with a tube (cold steel weapons +5) | 1 | 5 | 15.62 | 0 | 0 | 0 | 11500 | 0 | 0 |
| `bavaca.36` | Research new steel grades (18c musketeer/grenadier melee attack efficiency +25%) | 1 | 25 | 15.62 | 0 | 0 | 0 | 19500 | 0 | 0 |
| `bavaca.4` | Carry out field melioration (field capacity +200%) | 1 | 200 | 15.62 | 0 | 1000 | 0 | 475 | 0 | 0 |
| `bavaca.5` | Design new tackle and fishing nets (boat efficiency +100%) | 1 | 100 | 15.62 | 0 | 12400 | 0 | 2520 | 0 | 0 |
| `bavaca.6` | Develop new woodworking methods (frigate building) | 1 | 0 | 15.62 | 0 | 12400 | 0 | 7040 | 0 | 0 |
| `bavaca.7` | Build new shipyards for fishing boats (fishing boat cost -85%) | 1 | 0 | 15.62 | 0 | 7300 | 0 | 1220 | 0 | 0 |
| `bavaca.8` | Design new woodworking tools (woodcutting efficiency +100%) | 1 | 100 | 15.62 | 5500 | 0 | 0 | 550 | 0 | 0 |
| `bavaca.9` | Use new construction materials (durability of buildings +85) | 1 | 85 | 15.62 | 0 | 9400 | 7850 | 1150 | 0 | 0 |
| `bavart.cannon.1.1` | — | 2 | — | 10.0 | 0 | 1000 | 500 | 300 | 0 | 0 |
| `bavart.cannon.1.2` | — | 3 | — | 10.0 | 0 | 3000 | 1000 | 500 | 0 | 0 |
| `bavart.cannon.1.3` | — | 4 | — | 10.0 | 0 | 6000 | 2000 | 1000 | 0 | 0 |
| `bavart.cannon.1.4` | — | 5 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `bavart.cannon.1.5` | — | 6 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `bavart.cannon.1.6` | — | 7 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `bavart.cannon.2.1` | — | 2 | -2500000 | 10.0 | 0 | 0 | 0 | 500 | 1000 | 0 |
| `bavart.cannon.2.2` | — | 3 | -2500000 | 10.0 | 0 | 0 | 0 | 1000 | 2000 | 0 |
| `bavart.cannon.2.3` | — | 4 | -2500000 | 10.0 | 0 | 0 | 0 | 2000 | 3000 | 0 |
| `bavart.cannon.2.4` | — | 5 | -2000000 | 15.62 | 2560 | 0 | 0 | 0 | 0 | 0 |
| `bavart.cannon.2.5` | — | 6 | -2000000 | 15.62 | 3560 | 0 | 0 | 0 | 0 | 0 |
| `bavart.cannon.2.6` | — | 7 | -2000000 | 15.62 | 5560 | 0 | 0 | 0 | 0 | 0 |
| `bavart.howitzer.1.1` | — | 2 | — | 10.0 | 0 | 1000 | 500 | 300 | 0 | 0 |
| `bavart.howitzer.1.2` | — | 3 | — | 10.0 | 0 | 3000 | 1000 | 500 | 0 | 0 |
| `bavart.howitzer.1.3` | — | 4 | — | 10.0 | 0 | 6000 | 2000 | 1000 | 0 | 0 |
| `bavart.howitzer.1.4` | — | 5 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `bavart.howitzer.1.5` | — | 6 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `bavart.howitzer.1.6` | — | 7 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `bavart.howitzer.2.1` | — | 2 | -2500000 | 10.0 | 0 | 0 | 0 | 500 | 1000 | 0 |
| `bavart.howitzer.2.2` | — | 3 | -2500000 | 10.0 | 0 | 0 | 0 | 1000 | 2000 | 0 |
| `bavart.howitzer.2.3` | — | 4 | -2500000 | 10.0 | 0 | 0 | 0 | 2000 | 3000 | 0 |
| `bavart.howitzer.2.4` | — | 5 | -2000000 | 31.25 | 2560 | 0 | 0 | 0 | 0 | 0 |
| `bavart.howitzer.2.5` | — | 6 | -2000000 | 31.25 | 3560 | 0 | 0 | 0 | 0 | 0 |
| `bavart.howitzer.2.6` | — | 7 | -2000000 | 31.25 | 5560 | 0 | 0 | 0 | 0 | 0 |
| `bavba2.drummer18.2.1` | Barracks 18c drummer18 protection +15 (lvl 2) | 2 | 15 | 15.62 | 205 | 0 | 0 | 90 | 0 | 0 |
| `bavba2.grenadierbav.1.1` | Barracks 18c grenadierbav damage +2 (lvl 2) | 2 | 2 | 15.62 | 1000 | 0 | 0 | 800 | 0 | 0 |
| `bavba2.grenadierbav.1.2` | Barracks 18c grenadierbav damage +3 (lvl 3) | 3 | 3 | 15.62 | 13000 | 0 | 0 | 2800 | 0 | 0 |
| `bavba2.grenadierbav.1.3` | Barracks 18c grenadierbav damage +4 (lvl 4) | 4 | 4 | 15.62 | 32000 | 0 | 0 | 1800 | 0 | 0 |
| `bavba2.grenadierbav.1.4` | Barracks 18c grenadierbav damage +5 (lvl 5) | 5 | 5 | 15.62 | 52000 | 0 | 0 | 4800 | 0 | 0 |
| `bavba2.grenadierbav.1.5` | Barracks 18c grenadierbav damage +6 (lvl 6) | 6 | 6 | 15.62 | 42000 | 0 | 0 | 3800 | 0 | 0 |
| `bavba2.grenadierbav.1.6` | Barracks 18c grenadierbav damage +1500 (lvl 7) | 7 | 1500 | 15.62 | 64000 | 0 | 0 | 14800 | 0 | 0 |
| `bavba2.grenadierbav.2.1` | Barracks 18c grenadierbav protection +1 (lvl 2) | 2 | 1 | 15.62 | 3205 | 0 | 0 | 375 | 0 | 0 |
| `bavba2.grenadierbav.2.2` | Barracks 18c grenadierbav protection +2 (lvl 3) | 3 | 2 | 15.62 | 11030 | 0 | 0 | 4350 | 0 | 0 |
| `bavba2.grenadierbav.2.3` | Barracks 18c grenadierbav protection +3 (lvl 4) | 4 | 3 | 15.62 | 36206 | 0 | 0 | 500 | 0 | 0 |
| `bavba2.grenadierbav.2.4` | Barracks 18c grenadierbav protection +1 (lvl 5) | 5 | 1 | 15.62 | 34950 | 0 | 0 | 1350 | 0 | 0 |
| `bavba2.grenadierbav.2.5` | Barracks 18c grenadierbav protection +2 (lvl 6) | 6 | 2 | 15.62 | 30060 | 0 | 0 | 2150 | 0 | 0 |
| `bavba2.grenadierbav.2.6` | Barracks 18c grenadierbav protection +3 (lvl 7) | 7 | 3 | 15.62 | 64000 | 0 | 0 | 2550 | 0 | 0 |
| `bavba2.musketeer18bav.1.1` | Barracks 18c musketeer18bav damage +1 (lvl 2) | 2 | 1 | 15.62 | 900 | 0 | 0 | 700 | 0 | 0 |
| `bavba2.musketeer18bav.1.2` | Barracks 18c musketeer18bav damage +1 (lvl 3) | 3 | 1 | 15.62 | 1600 | 0 | 0 | 800 | 0 | 0 |
| `bavba2.musketeer18bav.1.3` | Barracks 18c musketeer18bav damage +1 (lvl 4) | 4 | 1 | 15.62 | 2500 | 0 | 0 | 900 | 0 | 0 |
| `bavba2.musketeer18bav.1.4` | Barracks 18c musketeer18bav damage +1 (lvl 5) | 5 | 1 | 15.62 | 2000 | 0 | 0 | 600 | 0 | 0 |
| `bavba2.musketeer18bav.1.5` | Barracks 18c musketeer18bav damage +1 (lvl 6) | 6 | 1 | 15.62 | 3500 | 0 | 0 | 1000 | 0 | 0 |
| `bavba2.musketeer18bav.1.6` | Barracks 18c musketeer18bav damage +1 (lvl 7) | 7 | 1 | 15.62 | 3000 | 0 | 0 | 800 | 0 | 0 |
| `bavba2.musketeer18bav.2.1` | Barracks 18c musketeer18bav protection +1 (lvl 2) | 2 | 1 | 15.62 | 3500 | 0 | 0 | 350 | 0 | 0 |
| `bavba2.musketeer18bav.2.2` | Barracks 18c musketeer18bav protection +1 (lvl 3) | 3 | 1 | 15.62 | 11230 | 0 | 0 | 1350 | 0 | 0 |
| `bavba2.musketeer18bav.2.3` | Barracks 18c musketeer18bav protection +1 (lvl 4) | 4 | 1 | 15.62 | 35706 | 0 | 0 | 4000 | 0 | 0 |
| `bavba2.musketeer18bav.2.4` | Barracks 18c musketeer18bav protection +2 (lvl 5) | 5 | 2 | 15.62 | 36556 | 0 | 0 | 4350 | 0 | 0 |
| `bavba2.musketeer18bav.2.5` | Barracks 18c musketeer18bav protection +2 (lvl 6) | 6 | 2 | 15.62 | 30060 | 0 | 0 | 1350 | 0 | 0 |
| `bavba2.musketeer18bav.2.6` | Barracks 18c musketeer18bav protection +3 (lvl 7) | 7 | 3 | 15.62 | 37600 | 0 | 0 | 1350 | 0 | 0 |
| `bavba2.officer18.1.1` | Barracks 18c officer18 damage +30 (lvl 2) | 2 | 30 | 15.62 | 200 | 0 | 0 | 910 | 0 | 0 |
| `bavba2.officer18.2.1` | Barracks 18c officer18 protection +12 (lvl 2) | 2 | 12 | 15.62 | 305 | 0 | 0 | 950 | 0 | 0 |
| `bavba2.pikeman18.1.1` | Barracks 18c pikeman18 damage +2 (lvl 2) | 2 | 2 | 15.62 | 2000 | 0 | 0 | 800 | 0 | 0 |
| `bavba2.pikeman18.1.2` | Barracks 18c pikeman18 damage +2 (lvl 3) | 3 | 2 | 15.62 | 8000 | 0 | 0 | 1200 | 0 | 0 |
| `bavba2.pikeman18.1.3` | Barracks 18c pikeman18 damage +2 (lvl 4) | 4 | 2 | 15.62 | 20000 | 0 | 0 | 2500 | 0 | 0 |
| `bavba2.pikeman18.1.4` | Barracks 18c pikeman18 damage +2 (lvl 5) | 5 | 2 | 15.62 | 32000 | 0 | 0 | 2800 | 0 | 0 |
| `bavba2.pikeman18.1.5` | Barracks 18c pikeman18 damage +2 (lvl 6) | 6 | 2 | 15.62 | 32000 | 0 | 0 | 3800 | 0 | 0 |
| `bavba2.pikeman18.1.6` | Barracks 18c pikeman18 damage +2 (lvl 7) | 7 | 2 | 15.62 | 40500 | 0 | 0 | 4800 | 0 | 0 |
| `bavba2.pikeman18.2.1` | Barracks 18c pikeman18 protection +2 (lvl 2) | 2 | 2 | 15.62 | 1500 | 0 | 0 | 500 | 0 | 0 |
| `bavba2.pikeman18.2.2` | Barracks 18c pikeman18 protection +3 (lvl 3) | 3 | 3 | 15.62 | 7000 | 0 | 0 | 1500 | 0 | 0 |
| `bavba2.pikeman18.2.3` | Barracks 18c pikeman18 protection +2 (lvl 4) | 4 | 2 | 15.62 | 37000 | 0 | 0 | 2000 | 0 | 0 |
| `bavba2.pikeman18.2.4` | Barracks 18c pikeman18 protection +3 (lvl 5) | 5 | 3 | 15.62 | 37000 | 0 | 0 | 5500 | 0 | 0 |
| `bavba2.pikeman18.2.5` | Barracks 18c pikeman18 protection +2 (lvl 6) | 6 | 2 | 15.62 | 37000 | 0 | 0 | 5500 | 0 | 0 |
| `bavba2.pikeman18.2.6` | Barracks 18c pikeman18 protection +3 (lvl 7) | 7 | 3 | 15.62 | 64600 | 0 | 0 | 5500 | 0 | 0 |
| `bavbar.1` | — | 1 | 140 | 15.62 | 750 | 0 | 0 | 250 | 0 | 0 |
| `bavbar.2` | — | 2 | 180 | 15.62 | 25600 | 0 | 0 | 3350 | 2000 | 0 |
| `bavbar.drummer.2.1` | Barracks 17c drummer protection +12 (lvl 2) | 2 | 12 | 15.62 | 905 | 0 | 0 | 25 | 0 | 0 |
| `bavbar.musketeer.1.1` | Barracks 17c musketeer damage +1 (lvl 2) | 2 | 1 | 15.62 | 1000 | 0 | 0 | 200 | 0 | 0 |
| `bavbar.musketeer.1.2` | Barracks 17c musketeer damage +1 (lvl 3) | 3 | 1 | 15.62 | 2000 | 0 | 0 | 200 | 0 | 0 |
| `bavbar.musketeer.1.3` | Barracks 17c musketeer damage +2 (lvl 4) | 4 | 2 | 15.62 | 100 | 0 | 0 | 200 | 0 | 0 |
| `bavbar.musketeer.2.1` | Barracks 17c musketeer protection +1 (lvl 2) | 2 | 1 | 15.62 | 450 | 0 | 0 | 550 | 300 | 0 |
| `bavbar.musketeer.2.2` | Barracks 17c musketeer protection +2 (lvl 3) | 3 | 2 | 15.62 | 405 | 0 | 0 | 150 | 20 | 0 |
| `bavbar.musketeer.2.3` | Barracks 17c musketeer protection +2 (lvl 4) | 4 | 2 | 15.62 | 1570 | 0 | 0 | 100 | 290 | 0 |
| `bavbar.musketeer.2.4` | Barracks 17c musketeer protection +1 (lvl 5) | 5 | 1 | 15.62 | 1956 | 0 | 0 | 450 | 700 | 0 |
| `bavbar.musketeer.2.5` | Barracks 17c musketeer protection +2 (lvl 6) | 6 | 2 | 15.62 | 1660 | 0 | 0 | 550 | 400 | 0 |
| `bavbar.musketeer.2.6` | Barracks 17c musketeer protection +2 (lvl 7) | 7 | 2 | 15.62 | 2700 | 0 | 0 | 750 | 100 | 0 |
| `bavbar.officer.1.1` | Barracks 17c officer damage +20 (lvl 2) | 2 | 20 | 15.62 | 800 | 0 | 0 | 150 | 0 | 0 |
| `bavbar.officer.2.1` | Barracks 17c officer protection +6 (lvl 2) | 2 | 6 | 15.62 | 1050 | 0 | 0 | 350 | 0 | 0 |
| `bavbar.pikeman.1.1` | Barracks 17c pikeman damage +1 (lvl 2) | 2 | 1 | 15.62 | 3600 | 0 | 0 | 450 | 0 | 0 |
| `bavbar.pikeman.1.2` | Barracks 17c pikeman damage +2 (lvl 3) | 3 | 2 | 15.62 | 1300 | 0 | 0 | 300 | 0 | 0 |
| `bavbar.pikeman.1.3` | Barracks 17c pikeman damage +2 (lvl 4) | 4 | 2 | 15.62 | 200 | 0 | 0 | 50 | 0 | 0 |
| `bavbar.pikeman.1.4` | Barracks 17c pikeman damage +1 (lvl 5) | 5 | 1 | 15.62 | 6800 | 0 | 0 | 1950 | 0 | 0 |
| `bavbar.pikeman.1.5` | Barracks 17c pikeman damage +2 (lvl 6) | 6 | 2 | 15.62 | 15030 | 0 | 0 | 2300 | 0 | 0 |
| `bavbar.pikeman.1.6` | — | 7 | 2 | 15.62 | 15000 | 0 | 0 | 1875 | 0 | 0 |
| `bavbar.pikeman.2.1` | Barracks 17c pikeman protection +1 (lvl 2) | 2 | 1 | 15.62 | 350 | 0 | 0 | 50 | 0 | 0 |
| `bavbar.pikeman.2.2` | Barracks 17c pikeman protection +1 (lvl 3) | 3 | 1 | 15.62 | 700 | 0 | 0 | 275 | 0 | 0 |
| `bavbar.pikeman.2.3` | Barracks 17c pikeman protection +2 (lvl 4) | 4 | 2 | 15.62 | 2500 | 0 | 0 | 200 | 0 | 0 |
| `bavbar.pikeman.2.4` | Barracks 17c pikeman protection +1 (lvl 5) | 5 | 1 | 15.62 | 13005 | 0 | 0 | 997 | 0 | 0 |
| `bavbar.pikeman.2.5` | Barracks 17c pikeman protection +1 (lvl 6) | 6 | 1 | 15.62 | 16010 | 0 | 0 | 2550 | 0 | 0 |
| `bavbar.pikeman.2.6` | — | 7 | 2 | 15.62 | 11250 | 0 | 0 | 1500 | 0 | 0 |
| `bavbla.1` | Manufacture agricultural equipment (field capacity +100%) | 1 | 100 | 15.62 | 0 | 400 | 0 | 90 | 0 | 0 |
| `bavbla.2` | Forge metal armature and gratings (building defence +50) | 1 | 50 | 15.62 | 0 | 0 | 12320 | 350 | 900 | 0 |
| `bavbla.3` | Forge harnesses for horses (mounted units recruitment speed -33%) | 1 | -3333333 | 15.62 | 0 | 0 | 0 | 3650 | 5300 | 8200 |
| `bavbla.4` | Forge bayonets and broadswords for infantry (18c musketeer/grenadier melee attack +5) | 1 | 5 | 15.62 | 0 | 1300 | 0 | 1500 | 900 | 5000 |
| `bavbla.5` | Forge new types of broadswords and sabres (cavalry and sword clansman attack +5) | 1 | 5 | 15.62 | 0 | 0 | 0 | 4000 | 7900 | 0 |
| `bavbla.6` | Forge new cuirasses (armoured soldiers defence +2) | 1 | 2 | 15.62 | 0 | 0 | 0 | 4950 | 10500 | 0 |
| `bavcen.1` | — | 1 | 0 | 9.38 | 30000 | 0 | 0 | 5000 | 2000 | 2000 |
| `bavsta.cuirassier.1.1` | Stable cuirassier damage +1 (lvl 2) | 2 | 1 | 15.62 | 11000 | 0 | 0 | 1600 | 0 | 0 |
| `bavsta.cuirassier.1.2` | Stable cuirassier damage +1 (lvl 3) | 3 | 1 | 15.62 | 33000 | 0 | 0 | 300 | 0 | 0 |
| `bavsta.cuirassier.1.3` | Stable cuirassier damage +1 (lvl 4) | 4 | 1 | 15.62 | 64000 | 0 | 0 | 3200 | 0 | 0 |
| `bavsta.cuirassier.1.4` | Stable cuirassier damage +2 (lvl 5) | 5 | 2 | 15.62 | 59000 | 0 | 0 | 2150 | 0 | 0 |
| `bavsta.cuirassier.1.5` | Stable cuirassier damage +2 (lvl 6) | 6 | 2 | 15.62 | 52055 | 0 | 0 | 5100 | 0 | 0 |
| `bavsta.cuirassier.1.6` | Stable cuirassier damage +3 (lvl 7) | 7 | 3 | 15.62 | 54050 | 0 | 0 | 7020 | 0 | 0 |
| `bavsta.cuirassier.2.1` | Stable cuirassier protection +2 (lvl 2) | 2 | 2 | 15.62 | 2505 | 0 | 0 | 350 | 1000 | 0 |
| `bavsta.cuirassier.2.2` | Stable cuirassier protection +3 (lvl 3) | 3 | 3 | 15.62 | 2000 | 0 | 0 | 300 | 2000 | 0 |
| `bavsta.cuirassier.2.3` | Stable cuirassier protection +3 (lvl 4) | 4 | 3 | 15.62 | 5600 | 0 | 0 | 750 | 3030 | 0 |
| `bavsta.cuirassier.2.4` | Stable cuirassier protection +2 (lvl 5) | 5 | 2 | 15.62 | 10700 | 0 | 0 | 6100 | 100 | 0 |
| `bavsta.cuirassier.2.5` | Stable cuirassier protection +1 (lvl 6) | 6 | 1 | 15.62 | 8100 | 0 | 0 | 2150 | 5000 | 0 |
| `bavsta.cuirassier.2.6` | Stable cuirassier protection +1 (lvl 7) | 7 | 1 | 15.62 | 9200 | 0 | 0 | 4900 | 7060 | 0 |
| `bavsta.dragoon.1.1` | Stable dragoon damage +1 (lvl 2) | 2 | 1 | 15.62 | 500 | 0 | 0 | 150 | 0 | 0 |
| `bavsta.dragoon.1.2` | Stable dragoon damage +1 (lvl 3) | 3 | 1 | 15.62 | 700 | 0 | 0 | 200 | 0 | 0 |
| `bavsta.dragoon.1.3` | Stable dragoon damage +2 (lvl 4) | 4 | 2 | 15.62 | 900 | 0 | 0 | 340 | 0 | 0 |
| `bavsta.dragoon.1.4` | Stable dragoon damage +1 (lvl 5) | 5 | 1 | 15.62 | 0 | 0 | 0 | 0 | 0 | 0 |
| `bavsta.dragoon.1.5` | Stable dragoon damage +1 (lvl 6) | 6 | 1 | 15.62 | 0 | 0 | 0 | 0 | 0 | 0 |
| `bavsta.dragoon.1.6` | Stable dragoon damage +3 (lvl 7) | 7 | 3 | 15.62 | 0 | 0 | 0 | 0 | 0 | 0 |
| `bavsta.dragoon.2.1` | Stable dragoon protection +1 (lvl 2) | 2 | 1 | 15.62 | 900 | 0 | 0 | 150 | 0 | 0 |
| `bavsta.dragoon.2.2` | Stable dragoon protection +2 (lvl 3) | 3 | 2 | 15.62 | 6600 | 0 | 0 | 750 | 0 | 0 |
| `bavsta.dragoon.2.3` | Stable dragoon protection +2 (lvl 4) | 4 | 2 | 15.62 | 5000 | 0 | 0 | 1250 | 0 | 0 |
| `bavsta.dragoon.2.4` | Stable dragoon protection +1 (lvl 5) | 5 | 1 | 15.62 | 3000 | 0 | 0 | 700 | 0 | 0 |
| `bavsta.dragoon.2.5` | Stable dragoon protection +2 (lvl 6) | 6 | 2 | 15.62 | 1000 | 0 | 0 | 2350 | 0 | 0 |
| `bavsta.dragoon.2.6` | Stable dragoon protection +2 (lvl 7) | 7 | 2 | 15.62 | 6001 | 0 | 0 | 6000 | 0 | 0 |
| `bavsta.dragoon18.1.1` | Stable dragoon18 damage +2 (lvl 2) | 2 | 2 | 15.62 | 2000 | 0 | 0 | 100 | 0 | 0 |
| `bavsta.dragoon18.1.2` | Stable dragoon18 damage +2 (lvl 3) | 3 | 2 | 15.62 | 9000 | 0 | 0 | 350 | 0 | 0 |
| `bavsta.dragoon18.1.3` | Stable dragoon18 damage +4 (lvl 4) | 4 | 4 | 15.62 | 12000 | 0 | 0 | 400 | 0 | 0 |
| `bavsta.dragoon18.1.4` | Stable dragoon18 damage +2 (lvl 5) | 5 | 2 | 15.62 | 23000 | 0 | 0 | 580 | 0 | 0 |
| `bavsta.dragoon18.1.5` | Stable dragoon18 damage +2 (lvl 6) | 6 | 2 | 15.62 | 32000 | 0 | 0 | 680 | 0 | 0 |
| `bavsta.dragoon18.1.6` | Stable dragoon18 damage +4 (lvl 7) | 7 | 4 | 15.62 | 42000 | 0 | 0 | 780 | 0 | 0 |
| `bavsta.dragoon18.2.1` | Stable dragoon18 protection +1 (lvl 2) | 2 | 1 | 15.62 | 260 | 0 | 0 | 935 | 0 | 0 |
| `bavsta.dragoon18.2.2` | Stable dragoon18 protection +1 (lvl 3) | 3 | 1 | 15.62 | 1460 | 0 | 0 | 1150 | 0 | 0 |
| `bavsta.dragoon18.2.3` | Stable dragoon18 protection +2 (lvl 4) | 4 | 2 | 15.62 | 12600 | 0 | 0 | 3350 | 0 | 0 |
| `bavsta.dragoon18.2.4` | Stable dragoon18 protection +1 (lvl 5) | 5 | 1 | 15.62 | 19600 | 0 | 0 | 3350 | 0 | 0 |
| `bavsta.dragoon18.2.5` | Stable dragoon18 protection +2 (lvl 6) | 6 | 2 | 15.62 | 12600 | 0 | 0 | 7350 | 0 | 0 |
| `bavsta.dragoon18.2.6` | Stable dragoon18 protection +3 (lvl 7) | 7 | 3 | 15.62 | 26760 | 0 | 0 | 7350 | 0 | 0 |
| `bavsta.hussar.1.1` | Stable hussar damage +1 (lvl 2) | 2 | 1 | 15.62 | 0 | 0 | 0 | 1800 | 1000 | 0 |
| `bavsta.hussar.1.2` | Stable hussar damage +2 (lvl 3) | 3 | 2 | 15.62 | 0 | 0 | 0 | 3800 | 2000 | 0 |
| `bavsta.hussar.1.3` | Stable hussar damage +3 (lvl 4) | 4 | 3 | 15.62 | 20200 | 0 | 0 | 0 | 3000 | 0 |
| `bavsta.hussar.1.4` | Stable hussar damage +4 (lvl 5) | 5 | 4 | 15.62 | 32000 | 0 | 0 | 0 | 3000 | 0 |
| `bavsta.hussar.1.5` | Stable hussar damage +1 (lvl 6) | 6 | 1 | 15.62 | 49200 | 0 | 0 | 0 | 3500 | 0 |
| `bavsta.hussar.1.6` | Stable hussar damage +1 (lvl 7) | 7 | 1 | 15.62 | 20000 | 0 | 0 | 0 | 6000 | 0 |
| `bavsta.hussar.2.1` | Stable hussar protection +1 (lvl 2) | 2 | 1 | 15.62 | 1760 | 0 | 0 | 1350 | 0 | 0 |
| `bavsta.hussar.2.2` | Stable hussar protection +1 (lvl 3) | 3 | 1 | 15.62 | 1900 | 0 | 0 | 2350 | 0 | 0 |
| `bavsta.hussar.2.3` | Stable hussar protection +1 (lvl 4) | 4 | 1 | 15.62 | 1600 | 0 | 0 | 5350 | 0 | 0 |
| `bavsta.hussar.2.4` | Stable hussar protection +2 (lvl 5) | 5 | 2 | 15.62 | 8000 | 0 | 0 | 8350 | 0 | 0 |
| `bavsta.hussar.2.5` | Stable hussar protection +2 (lvl 6) | 6 | 2 | 15.62 | 2000 | 0 | 0 | 15350 | 0 | 0 |
| `bavsta.hussar.2.6` | Stable hussar protection +3 (lvl 7) | 7 | 3 | 15.62 | 56000 | 0 | 0 | 20150 | 0 | 0 |
| `bavsta.reiter.1.1` | Stable reiter damage +1 (lvl 2) | 2 | 1 | 15.62 | 500 | 0 | 0 | 100 | 0 | 0 |
| `bavsta.reiter.1.2` | Stable reiter damage +2 (lvl 3) | 3 | 2 | 15.62 | 800 | 0 | 0 | 220 | 0 | 0 |
| `bavsta.reiter.1.3` | Stable reiter damage +1 (lvl 4) | 4 | 1 | 15.62 | 2400 | 0 | 0 | 380 | 0 | 0 |
| `bavsta.reiter.1.4` | Stable reiter damage +1 (lvl 5) | 5 | 1 | 15.62 | 4250 | 0 | 0 | 220 | 0 | 0 |
| `bavsta.reiter.1.5` | Stable reiter damage +1 (lvl 6) | 6 | 1 | 15.62 | 4030 | 0 | 0 | 900 | 0 | 0 |
| `bavsta.reiter.1.6` | Stable reiter damage +1 (lvl 7) | 7 | 1 | 15.62 | 6000 | 0 | 0 | 1600 | 0 | 0 |
| `bavsta.reiter.2.1` | Stable reiter protection +2 (lvl 2) | 2 | 2 | 15.62 | 200 | 0 | 0 | 135 | 400 | 0 |
| `bavsta.reiter.2.2` | Stable reiter protection +3 (lvl 3) | 3 | 3 | 15.62 | 600 | 0 | 0 | 100 | 300 | 0 |
| `bavsta.reiter.2.3` | Stable reiter protection +3 (lvl 4) | 4 | 3 | 15.62 | 800 | 0 | 0 | 200 | 560 | 0 |
| `bavsta.reiter.2.4` | Stable reiter protection +2 (lvl 5) | 5 | 2 | 15.62 | 1600 | 0 | 0 | 300 | 340 | 0 |
| `bavsta.reiter.2.5` | Stable reiter protection +1 (lvl 6) | 6 | 1 | 15.62 | 2200 | 0 | 0 | 350 | 600 | 0 |
| `bavsta.reiter.2.6` | Stable reiter protection +1 (lvl 7) | 7 | 1 | 15.62 | 17000 | 0 | 0 | 950 | 5200 | 0 |
| `eurcoa.1` | — | 2 | 5 | 9.38 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `eurcoa.2` | — | 3 | 8 | 9.38 | 5250 | 0 | 0 | 4950 | 0 | 0 |
| `eurcoa.3` | — | 4 | 10 | 9.38 | 12500 | 0 | 0 | 9250 | 0 | 0 |
| `eurcoa.4` | — | 5 | 12 | 9.38 | 15800 | 0 | 0 | 18500 | 0 | 0 |
| `eurcoa.5` | — | 6 | 15 | 9.38 | 19800 | 0 | 0 | 21050 | 0 | 0 |
| `eurcoa.6` | — | 7 | 40 | 9.38 | 50200 | 0 | 0 | 25950 | 0 | 0 |
| `eurgol.1` | — | 2 | 5 | 9.38 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `eurgol.2` | — | 3 | 8 | 9.38 | 5250 | 0 | 0 | 4950 | 0 | 0 |
| `eurgol.3` | — | 4 | 10 | 9.38 | 12500 | 0 | 0 | 9250 | 0 | 0 |
| `eurgol.4` | — | 5 | 12 | 9.38 | 15800 | 0 | 0 | 18500 | 0 | 0 |
| `eurgol.5` | — | 6 | 15 | 9.38 | 19800 | 0 | 0 | 21050 | 0 | 0 |
| `eurgol.6` | — | 7 | 40 | 9.38 | 50200 | 0 | 0 | 25950 | 0 | 0 |
| `euriro.1` | — | 2 | 5 | 9.38 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `euriro.2` | — | 3 | 8 | 9.38 | 5250 | 0 | 0 | 4950 | 0 | 0 |
| `euriro.3` | — | 4 | 10 | 9.38 | 12500 | 0 | 0 | 9250 | 0 | 0 |
| `euriro.4` | — | 5 | 12 | 9.38 | 15800 | 0 | 0 | 18500 | 0 | 0 |
| `euriro.5` | — | 6 | 15 | 9.38 | 19800 | 0 | 0 | 21050 | 0 | 0 |
| `euriro.6` | — | 7 | 40 | 9.38 | 50200 | 0 | 0 | 25950 | 0 | 0 |
| `eurpor.1` | — | 1 | 50 | 46.88 | 0 | 20000 | 0 | 1500 | 0 | 0 |
| `eurswa.1` | — | 2 | 5 | 0.03 | 0 | 0 | 500 | 0 | 0 | 0 |
| `eurtow.1` | — | 2 | -20 | 31.25 | 0 | 0 | 0 | 250 | 0 | 0 |
| `eurtow.2` | — | 3 | -20 | 31.25 | 0 | 0 | 0 | 0 | 350 | 0 |
| `eurtow.3` | — | 4 | -10 | 31.25 | 0 | 0 | 0 | 0 | 0 | 400 |
| `eurtow.4` | — | 5 | -10 | 31.25 | 0 | 0 | 0 | 0 | 450 | 0 |
| `eurtow.5` | — | 6 | -10 | 31.25 | 0 | 0 | 0 | 0 | 0 | 500 |
| `ferry.1` | Improve transport vessel design (+%value% capacity) | 2 | 200 | 15.62 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `ukrwwa.1` | — | 2 | 5 | 0.03 | 0 | 400 | 0 | 0 | 0 | 0 |

### hun — Hungary

| sid | имя (EN) | level | value | время (s) | F | W | S | G | I | C |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `eurcoa.1` | — | 2 | 5 | 9.38 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `eurcoa.2` | — | 3 | 8 | 9.38 | 5250 | 0 | 0 | 4950 | 0 | 0 |
| `eurcoa.3` | — | 4 | 10 | 9.38 | 12500 | 0 | 0 | 9250 | 0 | 0 |
| `eurcoa.4` | — | 5 | 12 | 9.38 | 15800 | 0 | 0 | 18500 | 0 | 0 |
| `eurcoa.5` | — | 6 | 15 | 9.38 | 19800 | 0 | 0 | 21050 | 0 | 0 |
| `eurcoa.6` | — | 7 | 40 | 9.38 | 50200 | 0 | 0 | 25950 | 0 | 0 |
| `eurgol.1` | — | 2 | 5 | 9.38 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `eurgol.2` | — | 3 | 8 | 9.38 | 5250 | 0 | 0 | 4950 | 0 | 0 |
| `eurgol.3` | — | 4 | 10 | 9.38 | 12500 | 0 | 0 | 9250 | 0 | 0 |
| `eurgol.4` | — | 5 | 12 | 9.38 | 15800 | 0 | 0 | 18500 | 0 | 0 |
| `eurgol.5` | — | 6 | 15 | 9.38 | 19800 | 0 | 0 | 21050 | 0 | 0 |
| `eurgol.6` | — | 7 | 40 | 9.38 | 50200 | 0 | 0 | 25950 | 0 | 0 |
| `euriro.1` | — | 2 | 5 | 9.38 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `euriro.2` | — | 3 | 8 | 9.38 | 5250 | 0 | 0 | 4950 | 0 | 0 |
| `euriro.3` | — | 4 | 10 | 9.38 | 12500 | 0 | 0 | 9250 | 0 | 0 |
| `euriro.4` | — | 5 | 12 | 9.38 | 15800 | 0 | 0 | 18500 | 0 | 0 |
| `euriro.5` | — | 6 | 15 | 9.38 | 19800 | 0 | 0 | 21050 | 0 | 0 |
| `euriro.6` | — | 7 | 40 | 9.38 | 50200 | 0 | 0 | 25950 | 0 | 0 |
| `eurpor.1` | — | 1 | 50 | 46.88 | 0 | 20000 | 0 | 1500 | 0 | 0 |
| `eurswa.1` | — | 2 | 5 | 0.03 | 0 | 0 | 500 | 0 | 0 | 0 |
| `eurtow.1` | — | 2 | -20 | 31.25 | 0 | 0 | 0 | 250 | 0 | 0 |
| `eurtow.2` | — | 3 | -20 | 31.25 | 0 | 0 | 0 | 0 | 350 | 0 |
| `eurtow.3` | — | 4 | -10 | 31.25 | 0 | 0 | 0 | 0 | 0 | 400 |
| `eurtow.4` | — | 5 | -10 | 31.25 | 0 | 0 | 0 | 0 | 450 | 0 |
| `eurtow.5` | — | 6 | -10 | 31.25 | 0 | 0 | 0 | 0 | 0 | 500 |
| `ferry.1` | Improve transport vessel design (+%value% capacity) | 2 | 200 | 15.62 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `hunaca.1` | Cultivate new cultures of wheat (harvesting +40%) | 1 | 40 | 15.62 | 0 | 200 | 0 | 325 | 0 | 0 |
| `hunaca.10` | Raise builders' salary (building construction time -75%) | 1 | -7500000 | 15.62 | 0 | 0 | 0 | 6950 | 0 | 0 |
| `hunaca.11` | Research new fortification grades (durability of walls and towers +80) | 1 | 80 | 15.62 | 0 | 0 | 16200 | 1500 | 0 | 0 |
| `hunaca.12` | Improve firearms: rifled barrel (fire power +10%) | 1 | 10 | 15.62 | 0 | 0 | 0 | 0 | 5000 | 0 |
| `hunaca.13` | Research granular gunpowder (fire power +10%) | 1 | 10 | 15.62 | 0 | 0 | 0 | 4000 | 0 | 0 |
| `hunaca.14` | Research new sulphur purification methods (fire power +15%) | 1 | 15 | 15.62 | 0 | 0 | 0 | 7000 | 0 | 0 |
| `hunaca.15` | Research new nitre purification methods (fire power +25%) | 1 | 25 | 15.62 | 0 | 0 | 0 | 0 | 0 | 11000 |
| `hunaca.16` | Research improved additions to gunpowder formula (artillery range +5%) | 1 | 5 | 15.62 | 0 | 0 | 0 | 2000 | 12150 | 0 |
| `hunaca.17` | Design new barrel types: unicorn, carronade (artillery range +10%) | 1 | 10 | 15.62 | 0 | 0 | 3000 | 4550 | 19200 | 0 |
| `hunaca.18` | Design more durable gun carriage: Gribovalle system (artillery durability +50%) | 1 | 50 | 15.62 | 0 | 0 | 0 | 500 | 3830 | 1500 |
| `hunaca.19` | Design multi-barrelled cannon | 1 | 0 | 15.62 | 0 | 0 | 0 | 1500 | 0 | 2500 |
| `hunaca.2` | Cultivate new cultures of rye (harvesting +50%) | 1 | 50 | 15.62 | 0 | 2400 | 0 | 625 | 0 | 0 |
| `hunaca.20` | Research new sighting devices for artillery (artillery accuracy +35%) | 1 | -35 | 15.62 | 0 | 3540 | 0 | 2000 | 0 | 7250 |
| `hunaca.21` | Finance artillery repair shops (repair all artillery) | 1 | 25 | 15.62 | 0 | 350 | 0 | 100 | 0 | 250 |
| `hunaca.22` | Develop geology (previously hidden deposits appear on the map) | 1 | 0 | 15.62 | 0 | 0 | 0 | 250 | 0 | 0 |
| `hunaca.23` | Develop mining (stone excavation efficiency +100%) | 1 | 100 | 15.62 | 0 | 0 | 0 | 1550 | 3000 | 0 |
| `hunaca.24` | Raise miners' salary (stone excavation efficiency +200%) | 1 | 200 | 15.62 | 4200 | 0 | 0 | 1550 | 0 | 12520 |
| `hunaca.25` | Design Montgolfier (reveals the whole map) | 1 | 0 | 15.62 | 0 | 0 | 0 | 5750 | 0 | 0 |
| `hunaca.26` | Develop medical science (heals all live units) | 1 | 50 | 31.25 | 0 | 0 | 0 | 200 | 0 | 200 |
| `hunaca.27` | Develop mathematics (artillery accuracy +35%) | 1 | -35 | 15.62 | 0 | 9540 | 0 | 12000 | 0 | 65200 |
| `hunaca.28` | Design new rigging types (ship speed +40%) | 1 | 40 | 15.62 | 0 | 65400 | 0 | 24050 | 0 | 0 |
| `hunaca.29` | Design new rib system and new hulls (battleship construction) | 1 | 0 | 15.62 | 0 | 32300 | 0 | 6800 | 9000 | 12800 |
| `hunaca.3` | Raise agriculturists' salary (harvesting +50%) | 1 | 50 | 15.62 | 0 | 3600 | 0 | 850 | 0 | 0 |
| `hunaca.30` | Train carpenters (shipbuilding speed x10) | 1 | -5000000 | 15.62 | 0 | 2300 | 42700 | 1150 | 0 | 0 |
| `hunaca.31` | Design wheellock (rate of fire +30%) | 1 | -30 | 15.62 | 0 | 0 | 6000 | 5500 | 4200 | 0 |
| `hunaca.32` | Design flintlock (musket cost -50%) | 1 | 0 | 15.62 | 0 | 0 | 0 | 6050 | 0 | 7750 |
| `hunaca.33` | Design paper cartridge and iron ramrod (rate of fire +30%) | 1 | -30 | 15.62 | 0 | 5000 | 0 | 5500 | 0 | 15200 |
| `hunaca.34` | Research improved steel grades for cuirasses (armoured soldier defence +2) | 1 | 2 | 15.62 | 0 | 0 | 0 | 9750 | 0 | 0 |
| `hunaca.35` | Design bayonet: barrel-inserted, bayonet with a tube (cold steel weapons +5) | 1 | 5 | 15.62 | 0 | 0 | 0 | 11500 | 0 | 0 |
| `hunaca.36` | Research new steel grades (18c musketeer/grenadier melee attack efficiency +25%) | 1 | 25 | 15.62 | 0 | 0 | 0 | 19500 | 0 | 0 |
| `hunaca.4` | Carry out field melioration (field capacity +200%) | 1 | 200 | 15.62 | 0 | 1000 | 0 | 475 | 0 | 0 |
| `hunaca.5` | Design new tackle and fishing nets (boat efficiency +100%) | 1 | 100 | 15.62 | 0 | 12400 | 0 | 2520 | 0 | 0 |
| `hunaca.6` | Develop new woodworking methods (frigate building) | 1 | 0 | 15.62 | 0 | 12400 | 0 | 7040 | 0 | 0 |
| `hunaca.7` | Build new shipyards for fishing boats (fishing boat cost -85%) | 1 | 0 | 15.62 | 0 | 7300 | 0 | 1220 | 0 | 0 |
| `hunaca.8` | Design new woodworking tools (woodcutting efficiency +100%) | 1 | 100 | 15.62 | 5500 | 0 | 0 | 550 | 0 | 0 |
| `hunaca.9` | Use new construction materials (durability of buildings +85) | 1 | 85 | 15.62 | 0 | 9400 | 7850 | 1150 | 0 | 0 |
| `hunart.cannon.1.1` | — | 2 | — | 10.0 | 0 | 1000 | 500 | 300 | 0 | 0 |
| `hunart.cannon.1.2` | — | 3 | — | 10.0 | 0 | 3000 | 1000 | 500 | 0 | 0 |
| `hunart.cannon.1.3` | — | 4 | — | 10.0 | 0 | 6000 | 2000 | 1000 | 0 | 0 |
| `hunart.cannon.1.4` | — | 5 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `hunart.cannon.1.5` | — | 6 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `hunart.cannon.1.6` | — | 7 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `hunart.cannon.2.1` | — | 2 | -2500000 | 10.0 | 0 | 0 | 0 | 500 | 1000 | 0 |
| `hunart.cannon.2.2` | — | 3 | -2500000 | 10.0 | 0 | 0 | 0 | 1000 | 2000 | 0 |
| `hunart.cannon.2.3` | — | 4 | -2500000 | 10.0 | 0 | 0 | 0 | 2000 | 3000 | 0 |
| `hunart.cannon.2.4` | — | 5 | -2000000 | 15.62 | 2560 | 0 | 0 | 0 | 0 | 0 |
| `hunart.cannon.2.5` | — | 6 | -2000000 | 15.62 | 3560 | 0 | 0 | 0 | 0 | 0 |
| `hunart.cannon.2.6` | — | 7 | -2000000 | 15.62 | 5560 | 0 | 0 | 0 | 0 | 0 |
| `hunart.howitzer.1.1` | — | 2 | — | 10.0 | 0 | 1000 | 500 | 300 | 0 | 0 |
| `hunart.howitzer.1.2` | — | 3 | — | 10.0 | 0 | 3000 | 1000 | 500 | 0 | 0 |
| `hunart.howitzer.1.3` | — | 4 | — | 10.0 | 0 | 6000 | 2000 | 1000 | 0 | 0 |
| `hunart.howitzer.1.4` | — | 5 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `hunart.howitzer.1.5` | — | 6 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `hunart.howitzer.1.6` | — | 7 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `hunart.howitzer.2.1` | — | 2 | -2500000 | 10.0 | 0 | 0 | 0 | 500 | 1000 | 0 |
| `hunart.howitzer.2.2` | — | 3 | -2500000 | 10.0 | 0 | 0 | 0 | 1000 | 2000 | 0 |
| `hunart.howitzer.2.3` | — | 4 | -2500000 | 10.0 | 0 | 0 | 0 | 2000 | 3000 | 0 |
| `hunart.howitzer.2.4` | — | 5 | -2000000 | 31.25 | 2560 | 0 | 0 | 0 | 0 | 0 |
| `hunart.howitzer.2.5` | — | 6 | -2000000 | 31.25 | 3560 | 0 | 0 | 0 | 0 | 0 |
| `hunart.howitzer.2.6` | — | 7 | -2000000 | 31.25 | 5560 | 0 | 0 | 0 | 0 | 0 |
| `hunba2.drummer18.2.1` | Barracks 18c drummer18 protection +15 (lvl 2) | 2 | 15 | 15.62 | 900 | 0 | 0 | 45 | 0 | 0 |
| `hunba2.grenadierhun.1.1` | Barracks 18c grenadierhun damage +6 (lvl 2) | 2 | 6 | 15.62 | 1000 | 0 | 0 | 800 | 0 | 0 |
| `hunba2.grenadierhun.1.2` | Barracks 18c grenadierhun damage +5 (lvl 3) | 3 | 5 | 15.62 | 13000 | 0 | 0 | 1800 | 0 | 0 |
| `hunba2.grenadierhun.1.3` | Barracks 18c grenadierhun damage +4 (lvl 4) | 4 | 4 | 15.62 | 25000 | 0 | 0 | 1800 | 0 | 0 |
| `hunba2.grenadierhun.1.4` | Barracks 18c grenadierhun damage +3 (lvl 5) | 5 | 3 | 15.62 | 49000 | 0 | 0 | 4800 | 0 | 0 |
| `hunba2.grenadierhun.1.5` | Barracks 18c grenadierhun damage +2 (lvl 6) | 6 | 2 | 15.62 | 54000 | 0 | 0 | 5800 | 0 | 0 |
| `hunba2.grenadierhun.1.6` | Barracks 18c grenadierhun damage +1500 (lvl 7) | 7 | 1500 | 15.62 | 60000 | 0 | 0 | 14590 | 0 | 0 |
| `hunba2.grenadierhun.2.1` | Barracks 18c grenadierhun protection +2 (lvl 2) | 2 | 2 | 15.62 | 7705 | 0 | 0 | 350 | 0 | 0 |
| `hunba2.grenadierhun.2.2` | Barracks 18c grenadierhun protection +2 (lvl 3) | 3 | 2 | 15.62 | 7030 | 0 | 0 | 1350 | 0 | 0 |
| `hunba2.grenadierhun.2.3` | Barracks 18c grenadierhun protection +2 (lvl 4) | 4 | 2 | 15.62 | 21706 | 0 | 0 | 1000 | 0 | 0 |
| `hunba2.grenadierhun.2.4` | Barracks 18c grenadierhun protection +2 (lvl 5) | 5 | 2 | 15.62 | 22556 | 0 | 0 | 5350 | 0 | 0 |
| `hunba2.grenadierhun.2.5` | Barracks 18c grenadierhun protection +2 (lvl 6) | 6 | 2 | 15.62 | 30060 | 0 | 0 | 1750 | 0 | 0 |
| `hunba2.grenadierhun.2.6` | Barracks 18c grenadierhun protection +2 (lvl 7) | 7 | 2 | 15.62 | 62000 | 0 | 0 | 950 | 0 | 0 |
| `hunba2.musketeer18.1.1` | Barracks 18c musketeer18 damage +1 (lvl 2) | 2 | 1 | 15.62 | 1000 | 0 | 0 | 800 | 0 | 0 |
| `hunba2.musketeer18.1.2` | Barracks 18c musketeer18 damage +1 (lvl 3) | 3 | 1 | 15.62 | 1500 | 0 | 0 | 800 | 0 | 0 |
| `hunba2.musketeer18.1.3` | Barracks 18c musketeer18 damage +2 (lvl 4) | 4 | 2 | 15.62 | 2000 | 0 | 0 | 800 | 0 | 0 |
| `hunba2.musketeer18.1.4` | Barracks 18c musketeer18 damage +2 (lvl 5) | 5 | 2 | 15.62 | 2500 | 0 | 0 | 800 | 0 | 0 |
| `hunba2.musketeer18.1.5` | Barracks 18c musketeer18 damage +3 (lvl 6) | 6 | 3 | 15.62 | 3000 | 0 | 0 | 800 | 0 | 0 |
| `hunba2.musketeer18.1.6` | Barracks 18c musketeer18 damage +3 (lvl 7) | 7 | 3 | 15.62 | 3500 | 0 | 0 | 800 | 0 | 0 |
| `hunba2.musketeer18.2.1` | Barracks 18c musketeer18 protection +1 (lvl 2) | 2 | 1 | 15.62 | 3706 | 0 | 0 | 350 | 0 | 0 |
| `hunba2.musketeer18.2.2` | Barracks 18c musketeer18 protection +2 (lvl 3) | 3 | 2 | 15.62 | 11030 | 0 | 0 | 1350 | 0 | 0 |
| `hunba2.musketeer18.2.3` | Barracks 18c musketeer18 protection +2 (lvl 4) | 4 | 2 | 15.62 | 35706 | 0 | 0 | 4000 | 0 | 0 |
| `hunba2.musketeer18.2.4` | Barracks 18c musketeer18 protection +1 (lvl 5) | 5 | 1 | 15.62 | 36556 | 0 | 0 | 4350 | 0 | 0 |
| `hunba2.musketeer18.2.5` | Barracks 18c musketeer18 protection +2 (lvl 6) | 6 | 2 | 15.62 | 30060 | 0 | 0 | 1350 | 0 | 0 |
| `hunba2.musketeer18.2.6` | Barracks 18c musketeer18 protection +2 (lvl 7) | 7 | 2 | 15.62 | 37600 | 0 | 0 | 1350 | 0 | 0 |
| `hunba2.officer18.1.1` | Barracks 18c officer18 damage +30 (lvl 2) | 2 | 30 | 15.62 | 1200 | 0 | 0 | 750 | 0 | 0 |
| `hunba2.officer18.2.1` | Barracks 18c officer18 protection +12 (lvl 2) | 2 | 12 | 15.62 | 1500 | 0 | 0 | 375 | 0 | 0 |
| `hunba2.pandurhun.1.1` | Barracks 18c pandurhun damage +1 (lvl 2) | 2 | 1 | 15.62 | 3000 | 0 | 0 | 750 | 0 | 0 |
| `hunba2.pandurhun.1.2` | Barracks 18c pandurhun damage +1 (lvl 3) | 3 | 1 | 15.62 | 4000 | 0 | 0 | 1100 | 0 | 0 |
| `hunba2.pandurhun.1.3` | Barracks 18c pandurhun damage +2 (lvl 4) | 4 | 2 | 15.62 | 7000 | 0 | 0 | 1800 | 0 | 0 |
| `hunba2.pandurhun.1.4` | Barracks 18c pandurhun damage +1 (lvl 5) | 5 | 1 | 15.62 | 12000 | 0 | 0 | 350 | 0 | 0 |
| `hunba2.pandurhun.1.5` | Barracks 18c pandurhun damage +1 (lvl 6) | 6 | 1 | 15.62 | 32020 | 0 | 0 | 850 | 0 | 0 |
| `hunba2.pandurhun.1.6` | Barracks 18c pandurhun damage +2 (lvl 7) | 7 | 2 | 15.62 | 45200 | 0 | 0 | 1330 | 0 | 0 |
| `hunba2.pandurhun.2.1` | Barracks 18c pandurhun protection +1 (lvl 2) | 2 | 1 | 15.62 | 3706 | 0 | 0 | 350 | 0 | 0 |
| `hunba2.pandurhun.2.2` | Barracks 18c pandurhun protection +1 (lvl 3) | 3 | 1 | 15.62 | 12060 | 0 | 0 | 1350 | 0 | 0 |
| `hunba2.pandurhun.2.3` | Barracks 18c pandurhun protection +2 (lvl 4) | 4 | 2 | 15.62 | 36706 | 0 | 0 | 2050 | 0 | 0 |
| `hunba2.pandurhun.2.4` | Barracks 18c pandurhun protection +1 (lvl 5) | 5 | 1 | 15.62 | 36706 | 0 | 0 | 3350 | 0 | 0 |
| `hunba2.pandurhun.2.5` | Barracks 18c pandurhun protection +1 (lvl 6) | 6 | 1 | 15.62 | 37060 | 0 | 0 | 1350 | 0 | 0 |
| `hunba2.pandurhun.2.6` | Barracks 18c pandurhun protection +2 (lvl 7) | 7 | 2 | 15.62 | 16706 | 0 | 0 | 1350 | 0 | 0 |
| `hunba2.pikeman18.1.1` | Barracks 18c pikeman18 damage +2 (lvl 2) | 2 | 2 | 15.62 | 2000 | 0 | 0 | 800 | 0 | 0 |
| `hunba2.pikeman18.1.2` | Barracks 18c pikeman18 damage +2 (lvl 3) | 3 | 2 | 15.62 | 8000 | 0 | 0 | 1200 | 0 | 0 |
| `hunba2.pikeman18.1.3` | Barracks 18c pikeman18 damage +2 (lvl 4) | 4 | 2 | 15.62 | 20000 | 0 | 0 | 2500 | 0 | 0 |
| `hunba2.pikeman18.1.4` | Barracks 18c pikeman18 damage +2 (lvl 5) | 5 | 2 | 15.62 | 32000 | 0 | 0 | 2800 | 0 | 0 |
| `hunba2.pikeman18.1.5` | Barracks 18c pikeman18 damage +2 (lvl 6) | 6 | 2 | 15.62 | 32000 | 0 | 0 | 3800 | 0 | 0 |
| `hunba2.pikeman18.1.6` | Barracks 18c pikeman18 damage +2 (lvl 7) | 7 | 2 | 15.62 | 40500 | 0 | 0 | 4800 | 0 | 0 |
| `hunba2.pikeman18.2.1` | Barracks 18c pikeman18 protection +2 (lvl 2) | 2 | 2 | 15.62 | 1500 | 0 | 0 | 500 | 0 | 0 |
| `hunba2.pikeman18.2.2` | Barracks 18c pikeman18 protection +3 (lvl 3) | 3 | 3 | 15.62 | 7000 | 0 | 0 | 1500 | 0 | 0 |
| `hunba2.pikeman18.2.3` | Barracks 18c pikeman18 protection +2 (lvl 4) | 4 | 2 | 15.62 | 37000 | 0 | 0 | 2000 | 0 | 0 |
| `hunba2.pikeman18.2.4` | Barracks 18c pikeman18 protection +3 (lvl 5) | 5 | 3 | 15.62 | 37000 | 0 | 0 | 5500 | 0 | 0 |
| `hunba2.pikeman18.2.5` | Barracks 18c pikeman18 protection +2 (lvl 6) | 6 | 2 | 15.62 | 37000 | 0 | 0 | 5500 | 0 | 0 |
| `hunba2.pikeman18.2.6` | Barracks 18c pikeman18 protection +3 (lvl 7) | 7 | 3 | 15.62 | 64600 | 0 | 0 | 5500 | 0 | 0 |
| `hunbar.1` | — | 1 | 140 | 15.62 | 750 | 0 | 0 | 250 | 0 | 0 |
| `hunbar.2` | — | 2 | 180 | 15.62 | 25600 | 0 | 0 | 3350 | 2000 | 0 |
| `hunbar.drummer.2.1` | Barracks 17c drummer protection +12 (lvl 2) | 2 | 12 | 15.62 | 1205 | 0 | 0 | 90 | 0 | 0 |
| `hunbar.gauduk.1.1` | Barracks 17c gauduk damage +1 (lvl 2) | 2 | 1 | 15.62 | 500 | 0 | 0 | 125 | 0 | 0 |
| `hunbar.gauduk.1.2` | Barracks 17c gauduk damage +1 (lvl 3) | 3 | 1 | 15.62 | 1250 | 0 | 0 | 275 | 0 | 0 |
| `hunbar.gauduk.1.3` | Barracks 17c gauduk damage +2 (lvl 4) | 4 | 2 | 15.62 | 2500 | 0 | 0 | 650 | 0 | 0 |
| `hunbar.gauduk.2.1` | Barracks 17c gauduk protection +1 (lvl 2) | 2 | 1 | 15.62 | 125 | 0 | 0 | 150 | 100 | 0 |
| `hunbar.gauduk.2.2` | Barracks 17c gauduk protection +1 (lvl 3) | 3 | 1 | 15.62 | 375 | 0 | 0 | 100 | 200 | 0 |
| `hunbar.gauduk.2.3` | Barracks 17c gauduk protection +2 (lvl 4) | 4 | 2 | 15.62 | 1570 | 0 | 0 | 300 | 450 | 0 |
| `hunbar.gauduk.2.4` | Barracks 17c gauduk protection +1 (lvl 5) | 5 | 1 | 15.62 | 2556 | 0 | 0 | 350 | 400 | 0 |
| `hunbar.gauduk.2.5` | Barracks 17c gauduk protection +1 (lvl 6) | 6 | 1 | 15.62 | 2060 | 0 | 0 | 450 | 100 | 0 |
| `hunbar.gauduk.2.6` | Barracks 17c gauduk protection +2 (lvl 7) | 7 | 2 | 15.62 | 2700 | 0 | 0 | 950 | 600 | 0 |
| `hunbar.officer.1.1` | Barracks 17c officer damage +20 (lvl 2) | 2 | 20 | 15.62 | 150 | 0 | 0 | 25 | 0 | 0 |
| `hunbar.officer.2.1` | Barracks 17c officer protection +6 (lvl 2) | 2 | 6 | 15.62 | 1650 | 0 | 0 | 395 | 0 | 0 |
| `hunbar.pikeman.1.1` | Barracks 17c pikeman damage +1 (lvl 2) | 2 | 1 | 15.62 | 100 | 0 | 0 | 90 | 0 | 0 |
| `hunbar.pikeman.1.2` | Barracks 17c pikeman damage +2 (lvl 3) | 3 | 2 | 15.62 | 300 | 0 | 0 | 450 | 0 | 0 |
| `hunbar.pikeman.1.3` | Barracks 17c pikeman damage +2 (lvl 4) | 4 | 2 | 15.62 | 4600 | 0 | 0 | 300 | 0 | 0 |
| `hunbar.pikeman.1.4` | Barracks 17c pikeman damage +1 (lvl 5) | 5 | 1 | 15.62 | 9200 | 0 | 0 | 1250 | 0 | 0 |
| `hunbar.pikeman.1.5` | Barracks 17c pikeman damage +2 (lvl 6) | 6 | 2 | 15.62 | 14030 | 0 | 0 | 2600 | 0 | 0 |
| `hunbar.pikeman.1.6` | — | 7 | 2 | 15.62 | 15000 | 0 | 0 | 1875 | 0 | 0 |
| `hunbar.pikeman.2.1` | Barracks 17c pikeman protection +1 (lvl 2) | 2 | 1 | 15.62 | 175 | 0 | 0 | 40 | 0 | 0 |
| `hunbar.pikeman.2.2` | Barracks 17c pikeman protection +1 (lvl 3) | 3 | 1 | 15.62 | 990 | 0 | 0 | 275 | 0 | 0 |
| `hunbar.pikeman.2.3` | Barracks 17c pikeman protection +2 (lvl 4) | 4 | 2 | 15.62 | 4700 | 0 | 0 | 280 | 0 | 0 |
| `hunbar.pikeman.2.4` | Barracks 17c pikeman protection +1 (lvl 5) | 5 | 1 | 15.62 | 9505 | 0 | 0 | 707 | 0 | 0 |
| `hunbar.pikeman.2.5` | Barracks 17c pikeman protection +1 (lvl 6) | 6 | 1 | 15.62 | 17510 | 0 | 0 | 2950 | 0 | 0 |
| `hunbar.pikeman.2.6` | — | 7 | 2 | 15.62 | 11250 | 0 | 0 | 1500 | 0 | 0 |
| `hunbla.1` | Manufacture agricultural equipment (field capacity +100%) | 1 | 100 | 15.62 | 0 | 400 | 0 | 90 | 0 | 0 |
| `hunbla.2` | Forge metal armature and gratings (building defence +50) | 1 | 50 | 15.62 | 0 | 0 | 12320 | 350 | 900 | 0 |
| `hunbla.3` | Forge harnesses for horses (mounted units recruitment speed -33%) | 1 | -3333333 | 15.62 | 0 | 0 | 0 | 3650 | 5300 | 8200 |
| `hunbla.4` | Forge bayonets and broadswords for infantry (18c musketeer/grenadier melee attack +5) | 1 | 5 | 15.62 | 0 | 1300 | 0 | 1500 | 900 | 5000 |
| `hunbla.5` | Forge new types of broadswords and sabres (cavalry and sword clansman attack +5) | 1 | 5 | 15.62 | 0 | 0 | 0 | 4000 | 7900 | 0 |
| `hunbla.6` | Forge new cuirasses (armoured soldiers defence +2) | 1 | 2 | 15.62 | 0 | 0 | 0 | 4950 | 10500 | 0 |
| `huncen.1` | — | 1 | 0 | 9.38 | 30000 | 0 | 0 | 5000 | 2000 | 2000 |
| `hunsta.cuirassier.1.1` | Stable cuirassier damage +1 (lvl 2) | 2 | 1 | 15.62 | 10000 | 0 | 0 | 200 | 0 | 0 |
| `hunsta.cuirassier.1.2` | Stable cuirassier damage +1 (lvl 3) | 3 | 1 | 15.62 | 34000 | 0 | 0 | 1700 | 0 | 0 |
| `hunsta.cuirassier.1.3` | Stable cuirassier damage +1 (lvl 4) | 4 | 1 | 15.62 | 64000 | 0 | 0 | 2100 | 0 | 0 |
| `hunsta.cuirassier.1.4` | Stable cuirassier damage +2 (lvl 5) | 5 | 2 | 15.62 | 58000 | 0 | 0 | 4150 | 0 | 0 |
| `hunsta.cuirassier.1.5` | Stable cuirassier damage +2 (lvl 6) | 6 | 2 | 15.62 | 59055 | 0 | 0 | 3100 | 0 | 0 |
| `hunsta.cuirassier.1.6` | Stable cuirassier damage +3 (lvl 7) | 7 | 3 | 15.62 | 47050 | 0 | 0 | 8150 | 0 | 0 |
| `hunsta.cuirassier.2.1` | Stable cuirassier protection +2 (lvl 2) | 2 | 2 | 15.62 | 1520 | 0 | 0 | 450 | 1000 | 0 |
| `hunsta.cuirassier.2.2` | Stable cuirassier protection +3 (lvl 3) | 3 | 3 | 15.62 | 7000 | 0 | 0 | 750 | 2000 | 0 |
| `hunsta.cuirassier.2.3` | Stable cuirassier protection +3 (lvl 4) | 4 | 3 | 15.62 | 3600 | 0 | 0 | 3300 | 3050 | 0 |
| `hunsta.cuirassier.2.4` | Stable cuirassier protection +2 (lvl 5) | 5 | 2 | 15.62 | 8700 | 0 | 0 | 3200 | 200 | 0 |
| `hunsta.cuirassier.2.5` | Stable cuirassier protection +1 (lvl 6) | 6 | 1 | 15.62 | 8700 | 0 | 0 | 2650 | 4300 | 0 |
| `hunsta.cuirassier.2.6` | Stable cuirassier protection +1 (lvl 7) | 7 | 1 | 15.62 | 11200 | 0 | 0 | 4700 | 6760 | 0 |
| `hunsta.dragoon.1.1` | Stable dragoon damage +1 (lvl 2) | 2 | 1 | 15.62 | 700 | 0 | 0 | 250 | 0 | 0 |
| `hunsta.dragoon.1.2` | Stable dragoon damage +1 (lvl 3) | 3 | 1 | 15.62 | 500 | 0 | 0 | 100 | 0 | 0 |
| `hunsta.dragoon.1.3` | Stable dragoon damage +2 (lvl 4) | 4 | 2 | 15.62 | 900 | 0 | 0 | 640 | 0 | 0 |
| `hunsta.dragoon.1.4` | Stable dragoon damage +1 (lvl 5) | 5 | 1 | 15.62 | 0 | 0 | 0 | 0 | 0 | 0 |
| `hunsta.dragoon.1.5` | Stable dragoon damage +1 (lvl 6) | 6 | 1 | 15.62 | 0 | 0 | 0 | 0 | 0 | 0 |
| `hunsta.dragoon.1.6` | Stable dragoon damage +3 (lvl 7) | 7 | 3 | 15.62 | 0 | 0 | 0 | 0 | 0 | 0 |
| `hunsta.dragoon.2.1` | Stable dragoon protection +1 (lvl 2) | 2 | 1 | 15.62 | 500 | 0 | 0 | 250 | 0 | 0 |
| `hunsta.dragoon.2.2` | Stable dragoon protection +2 (lvl 3) | 3 | 2 | 15.62 | 6300 | 0 | 0 | 850 | 0 | 0 |
| `hunsta.dragoon.2.3` | Stable dragoon protection +2 (lvl 4) | 4 | 2 | 15.62 | 4600 | 0 | 0 | 1350 | 0 | 0 |
| `hunsta.dragoon.2.4` | Stable dragoon protection +1 (lvl 5) | 5 | 1 | 15.62 | 2500 | 0 | 0 | 700 | 0 | 0 |
| `hunsta.dragoon.2.5` | Stable dragoon protection +2 (lvl 6) | 6 | 2 | 15.62 | 800 | 0 | 0 | 2750 | 0 | 0 |
| `hunsta.dragoon.2.6` | Stable dragoon protection +2 (lvl 7) | 7 | 2 | 15.62 | 2001 | 0 | 0 | 8200 | 0 | 0 |
| `hunsta.hussarhun.2.1` | Stable hussarhun protection +1 (lvl 2) | 2 | 1 | 15.62 | 2000 | 0 | 0 | 1350 | 0 | 0 |
| `hunsta.hussarhun.2.2` | Stable hussarhun protection +1 (lvl 3) | 3 | 1 | 15.62 | 1500 | 0 | 0 | 2100 | 0 | 0 |
| `hunsta.hussarhun.2.3` | Stable hussarhun protection +1 (lvl 4) | 4 | 1 | 15.62 | 5000 | 0 | 0 | 2300 | 0 | 0 |
| `hunsta.hussarhun.2.4` | Stable hussarhun protection +2 (lvl 5) | 5 | 2 | 15.62 | 10500 | 0 | 0 | 3400 | 0 | 0 |
| `hunsta.hussarhun.2.5` | Stable hussarhun protection +2 (lvl 6) | 6 | 2 | 15.62 | 12600 | 0 | 0 | 4500 | 0 | 0 |
| `hunsta.hussarhun.2.6` | Stable hussarhun protection +3 (lvl 7) | 7 | 3 | 15.62 | 40000 | 0 | 0 | 5000 | 0 | 0 |
| `hunsta.lightcavalry.1.1` | Stable lightcavalry damage +1 (lvl 2) | 2 | 1 | 15.62 | 4500 | 0 | 0 | 200 | 0 | 0 |
| `hunsta.lightcavalry.1.2` | Stable lightcavalry damage +2 (lvl 3) | 3 | 2 | 15.62 | 5500 | 0 | 0 | 250 | 0 | 0 |
| `hunsta.lightcavalry.1.3` | Stable lightcavalry damage +3 (lvl 4) | 4 | 3 | 15.62 | 22000 | 0 | 0 | 500 | 0 | 0 |
| `hunsta.lightcavalry.1.4` | Stable lightcavalry damage +1 (lvl 5) | 5 | 1 | 15.62 | 13000 | 0 | 0 | 480 | 0 | 0 |
| `hunsta.lightcavalry.1.5` | Stable lightcavalry damage +1 (lvl 6) | 6 | 1 | 15.62 | 42000 | 0 | 0 | 780 | 0 | 0 |
| `hunsta.lightcavalry.1.6` | Stable lightcavalry damage +2 (lvl 7) | 7 | 2 | 15.62 | 32000 | 0 | 0 | 680 | 0 | 0 |
| `hunsta.lightcavalry.2.1` | Stable lightcavalry protection +1 (lvl 2) | 2 | 1 | 15.62 | 750 | 0 | 0 | 935 | 0 | 0 |
| `hunsta.lightcavalry.2.2` | Stable lightcavalry protection +1 (lvl 3) | 3 | 1 | 15.62 | 1260 | 0 | 0 | 1150 | 0 | 0 |
| `hunsta.lightcavalry.2.3` | Stable lightcavalry protection +2 (lvl 4) | 4 | 2 | 15.62 | 10600 | 0 | 0 | 2350 | 0 | 0 |
| `hunsta.lightcavalry.2.4` | Stable lightcavalry protection +1 (lvl 5) | 5 | 1 | 15.62 | 22600 | 0 | 0 | 5350 | 0 | 0 |
| `hunsta.lightcavalry.2.5` | Stable lightcavalry protection +1 (lvl 6) | 6 | 1 | 15.62 | 19600 | 0 | 0 | 3350 | 0 | 0 |
| `hunsta.lightcavalry.2.6` | Stable lightcavalry protection +2 (lvl 7) | 7 | 2 | 15.62 | 15760 | 0 | 0 | 9350 | 0 | 0 |
| `hunsta.reiter.1.1` | Stable reiter damage +1 (lvl 2) | 2 | 1 | 15.62 | 500 | 0 | 0 | 100 | 0 | 0 |
| `hunsta.reiter.1.2` | Stable reiter damage +2 (lvl 3) | 3 | 2 | 15.62 | 900 | 0 | 0 | 220 | 0 | 0 |
| `hunsta.reiter.1.3` | Stable reiter damage +1 (lvl 4) | 4 | 1 | 15.62 | 4400 | 0 | 0 | 280 | 0 | 0 |
| `hunsta.reiter.1.4` | Stable reiter damage +1 (lvl 5) | 5 | 1 | 15.62 | 2250 | 0 | 0 | 320 | 0 | 0 |
| `hunsta.reiter.1.5` | Stable reiter damage +1 (lvl 6) | 6 | 1 | 15.62 | 3030 | 0 | 0 | 600 | 0 | 0 |
| `hunsta.reiter.1.6` | Stable reiter damage +1 (lvl 7) | 7 | 1 | 15.62 | 7000 | 0 | 0 | 1800 | 0 | 0 |
| `hunsta.reiter.2.1` | Stable reiter protection +2 (lvl 2) | 2 | 2 | 15.62 | 200 | 0 | 0 | 135 | 300 | 0 |
| `hunsta.reiter.2.2` | Stable reiter protection +3 (lvl 3) | 3 | 3 | 15.62 | 600 | 0 | 0 | 100 | 400 | 0 |
| `hunsta.reiter.2.3` | Stable reiter protection +3 (lvl 4) | 4 | 3 | 15.62 | 800 | 0 | 0 | 200 | 560 | 0 |
| `hunsta.reiter.2.4` | Stable reiter protection +2 (lvl 5) | 5 | 2 | 15.62 | 1600 | 0 | 0 | 300 | 640 | 0 |
| `hunsta.reiter.2.5` | Stable reiter protection +1 (lvl 6) | 6 | 1 | 15.62 | 3200 | 0 | 0 | 350 | 300 | 0 |
| `hunsta.reiter.2.6` | Stable reiter protection +1 (lvl 7) | 7 | 1 | 15.62 | 16000 | 0 | 0 | 1000 | 5000 | 0 |
| `ukrwwa.1` | — | 2 | 5 | 0.03 | 0 | 400 | 0 | 0 | 0 | 0 |

### swi — Switzerland

| sid | имя (EN) | level | value | время (s) | F | W | S | G | I | C |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `eurcoa.1` | — | 2 | 5 | 9.38 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `eurcoa.2` | — | 3 | 8 | 9.38 | 5250 | 0 | 0 | 4950 | 0 | 0 |
| `eurcoa.3` | — | 4 | 10 | 9.38 | 12500 | 0 | 0 | 9250 | 0 | 0 |
| `eurcoa.4` | — | 5 | 12 | 9.38 | 15800 | 0 | 0 | 18500 | 0 | 0 |
| `eurcoa.5` | — | 6 | 15 | 9.38 | 19800 | 0 | 0 | 21050 | 0 | 0 |
| `eurcoa.6` | — | 7 | 40 | 9.38 | 50200 | 0 | 0 | 25950 | 0 | 0 |
| `eurgol.1` | — | 2 | 5 | 9.38 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `eurgol.2` | — | 3 | 8 | 9.38 | 5250 | 0 | 0 | 4950 | 0 | 0 |
| `eurgol.3` | — | 4 | 10 | 9.38 | 12500 | 0 | 0 | 9250 | 0 | 0 |
| `eurgol.4` | — | 5 | 12 | 9.38 | 15800 | 0 | 0 | 18500 | 0 | 0 |
| `eurgol.5` | — | 6 | 15 | 9.38 | 19800 | 0 | 0 | 21050 | 0 | 0 |
| `eurgol.6` | — | 7 | 40 | 9.38 | 50200 | 0 | 0 | 25950 | 0 | 0 |
| `euriro.1` | — | 2 | 5 | 9.38 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `euriro.2` | — | 3 | 8 | 9.38 | 5250 | 0 | 0 | 4950 | 0 | 0 |
| `euriro.3` | — | 4 | 10 | 9.38 | 12500 | 0 | 0 | 9250 | 0 | 0 |
| `euriro.4` | — | 5 | 12 | 9.38 | 15800 | 0 | 0 | 18500 | 0 | 0 |
| `euriro.5` | — | 6 | 15 | 9.38 | 19800 | 0 | 0 | 21050 | 0 | 0 |
| `euriro.6` | — | 7 | 40 | 9.38 | 50200 | 0 | 0 | 25950 | 0 | 0 |
| `eurpor.1` | — | 1 | 50 | 46.88 | 0 | 20000 | 0 | 1500 | 0 | 0 |
| `eurswa.1` | — | 2 | 5 | 0.03 | 0 | 0 | 500 | 0 | 0 | 0 |
| `eurtow.1` | — | 2 | -20 | 31.25 | 0 | 0 | 0 | 250 | 0 | 0 |
| `eurtow.2` | — | 3 | -20 | 31.25 | 0 | 0 | 0 | 0 | 350 | 0 |
| `eurtow.3` | — | 4 | -10 | 31.25 | 0 | 0 | 0 | 0 | 0 | 400 |
| `eurtow.4` | — | 5 | -10 | 31.25 | 0 | 0 | 0 | 0 | 450 | 0 |
| `eurtow.5` | — | 6 | -10 | 31.25 | 0 | 0 | 0 | 0 | 0 | 500 |
| `ferry.1` | Improve transport vessel design (+%value% capacity) | 2 | 200 | 15.62 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `swiaca.1` | Cultivate new cultures of wheat (harvesting +40%) | 1 | 40 | 15.62 | 0 | 200 | 0 | 325 | 0 | 0 |
| `swiaca.10` | Raise builders' salary (building construction time -75%) | 1 | -7500000 | 15.62 | 0 | 0 | 0 | 6950 | 0 | 0 |
| `swiaca.11` | Research new fortification grades (durability of walls and towers +80) | 1 | 80 | 15.62 | 0 | 0 | 16200 | 1500 | 0 | 0 |
| `swiaca.12` | Improve firearms: rifled barrel (fire power +10%) | 1 | 10 | 15.62 | 0 | 0 | 0 | 0 | 5000 | 0 |
| `swiaca.13` | Research granular gunpowder (fire power +10%) | 1 | 10 | 15.62 | 0 | 0 | 0 | 4000 | 0 | 0 |
| `swiaca.14` | Research new sulphur purification methods (fire power +15%) | 1 | 15 | 15.62 | 0 | 0 | 0 | 7000 | 0 | 0 |
| `swiaca.15` | Research new nitre purification methods (fire power +25%) | 1 | 25 | 15.62 | 0 | 0 | 0 | 0 | 0 | 11000 |
| `swiaca.16` | Research improved additions to gunpowder formula (artillery range +5%) | 1 | 5 | 15.62 | 0 | 0 | 0 | 2000 | 12150 | 0 |
| `swiaca.17` | Design new barrel types: unicorn, carronade (artillery range +10%) | 1 | 10 | 15.62 | 0 | 0 | 3000 | 4550 | 19200 | 0 |
| `swiaca.18` | Design more durable gun carriage: Gribovalle system (artillery durability +50%) | 1 | 50 | 15.62 | 0 | 0 | 0 | 500 | 3830 | 1500 |
| `swiaca.19` | Design multi-barrelled cannon | 1 | 0 | 15.62 | 0 | 0 | 0 | 1500 | 0 | 2500 |
| `swiaca.2` | Cultivate new cultures of rye (harvesting +50%) | 1 | 50 | 15.62 | 0 | 2400 | 0 | 625 | 0 | 0 |
| `swiaca.20` | Research new sighting devices for artillery (artillery accuracy +35%) | 1 | -35 | 15.62 | 0 | 3540 | 0 | 2000 | 0 | 7250 |
| `swiaca.21` | Finance artillery repair shops (repair all artillery) | 1 | 25 | 15.62 | 0 | 350 | 0 | 100 | 0 | 250 |
| `swiaca.22` | Develop geology (previously hidden deposits appear on the map) | 1 | 0 | 15.62 | 0 | 0 | 0 | 250 | 0 | 0 |
| `swiaca.23` | Develop mining (stone excavation efficiency +100%) | 1 | 100 | 15.62 | 0 | 0 | 0 | 1550 | 3000 | 0 |
| `swiaca.24` | Raise miners' salary (stone excavation efficiency +200%) | 1 | 200 | 15.62 | 4200 | 0 | 0 | 1550 | 0 | 12520 |
| `swiaca.25` | Design Montgolfier (reveals the whole map) | 1 | 0 | 15.62 | 0 | 0 | 0 | 5750 | 0 | 0 |
| `swiaca.26` | Develop medical science (heals all live units) | 1 | 50 | 31.25 | 0 | 0 | 0 | 200 | 0 | 200 |
| `swiaca.27` | Develop mathematics (artillery accuracy +35%) | 1 | -35 | 15.62 | 0 | 9540 | 0 | 12000 | 0 | 65200 |
| `swiaca.28` | Design new rigging types (ship speed +40%) | 1 | 40 | 15.62 | 0 | 65400 | 0 | 24050 | 0 | 0 |
| `swiaca.29` | Design new rib system and new hulls (battleship construction) | 1 | 0 | 15.62 | 0 | 32300 | 0 | 6800 | 9000 | 12800 |
| `swiaca.3` | Raise agriculturists' salary (harvesting +50%) | 1 | 50 | 15.62 | 0 | 3600 | 0 | 850 | 0 | 0 |
| `swiaca.30` | Train carpenters (shipbuilding speed x10) | 1 | -5000000 | 15.62 | 0 | 2300 | 42700 | 1150 | 0 | 0 |
| `swiaca.31` | Design wheellock (rate of fire +30%) | 1 | -30 | 15.62 | 0 | 0 | 6000 | 5500 | 4200 | 0 |
| `swiaca.32` | Design flintlock (musket cost -50%) | 1 | 0 | 15.62 | 0 | 0 | 0 | 6050 | 0 | 7750 |
| `swiaca.33` | Design paper cartridge and iron ramrod (rate of fire +30%) | 1 | -30 | 15.62 | 0 | 5000 | 0 | 5500 | 0 | 15200 |
| `swiaca.34` | Research improved steel grades for cuirasses (armoured soldier defence +2) | 1 | 2 | 15.62 | 0 | 0 | 0 | 9750 | 0 | 0 |
| `swiaca.35` | Design bayonet: barrel-inserted, bayonet with a tube (cold steel weapons +5) | 1 | 5 | 15.62 | 0 | 0 | 0 | 11500 | 0 | 0 |
| `swiaca.36` | Research new steel grades (18c musketeer/grenadier melee attack efficiency +25%) | 1 | 25 | 15.62 | 0 | 0 | 0 | 19500 | 0 | 0 |
| `swiaca.4` | Carry out field melioration (field capacity +200%) | 1 | 200 | 15.62 | 0 | 1000 | 0 | 475 | 0 | 0 |
| `swiaca.5` | Design new tackle and fishing nets (boat efficiency +100%) | 1 | 100 | 15.62 | 0 | 12400 | 0 | 2520 | 0 | 0 |
| `swiaca.6` | Develop new woodworking methods (frigate building) | 1 | 0 | 15.62 | 0 | 12400 | 0 | 7040 | 0 | 0 |
| `swiaca.7` | Build new shipyards for fishing boats (fishing boat cost -85%) | 1 | 0 | 15.62 | 0 | 7300 | 0 | 1220 | 0 | 0 |
| `swiaca.8` | Design new woodworking tools (woodcutting efficiency +100%) | 1 | 100 | 15.62 | 5500 | 0 | 0 | 550 | 0 | 0 |
| `swiaca.9` | Use new construction materials (durability of buildings +85) | 1 | 85 | 15.62 | 0 | 9400 | 7850 | 1150 | 0 | 0 |
| `swiart.cannon.1.1` | — | 2 | — | 10.0 | 0 | 1000 | 500 | 300 | 0 | 0 |
| `swiart.cannon.1.2` | — | 3 | — | 10.0 | 0 | 3000 | 1000 | 500 | 0 | 0 |
| `swiart.cannon.1.3` | — | 4 | — | 10.0 | 0 | 6000 | 2000 | 1000 | 0 | 0 |
| `swiart.cannon.1.4` | — | 5 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `swiart.cannon.1.5` | — | 6 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `swiart.cannon.1.6` | — | 7 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `swiart.cannon.2.1` | — | 2 | -2500000 | 10.0 | 0 | 0 | 0 | 500 | 1000 | 0 |
| `swiart.cannon.2.2` | — | 3 | -2500000 | 10.0 | 0 | 0 | 0 | 1000 | 2000 | 0 |
| `swiart.cannon.2.3` | — | 4 | -2500000 | 10.0 | 0 | 0 | 0 | 2000 | 3000 | 0 |
| `swiart.cannon.2.4` | — | 5 | -2000000 | 15.62 | 2560 | 0 | 0 | 0 | 0 | 0 |
| `swiart.cannon.2.5` | — | 6 | -2000000 | 15.62 | 3560 | 0 | 0 | 0 | 0 | 0 |
| `swiart.cannon.2.6` | — | 7 | -2000000 | 15.62 | 5560 | 0 | 0 | 0 | 0 | 0 |
| `swiart.howitzer.1.1` | — | 2 | — | 10.0 | 0 | 1000 | 500 | 300 | 0 | 0 |
| `swiart.howitzer.1.2` | — | 3 | — | 10.0 | 0 | 3000 | 1000 | 500 | 0 | 0 |
| `swiart.howitzer.1.3` | — | 4 | — | 10.0 | 0 | 6000 | 2000 | 1000 | 0 | 0 |
| `swiart.howitzer.1.4` | — | 5 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `swiart.howitzer.1.5` | — | 6 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `swiart.howitzer.1.6` | — | 7 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `swiart.howitzer.2.1` | — | 2 | -2500000 | 10.0 | 0 | 0 | 0 | 500 | 1000 | 0 |
| `swiart.howitzer.2.2` | — | 3 | -2500000 | 10.0 | 0 | 0 | 0 | 1000 | 2000 | 0 |
| `swiart.howitzer.2.3` | — | 4 | -2500000 | 10.0 | 0 | 0 | 0 | 2000 | 3000 | 0 |
| `swiart.howitzer.2.4` | — | 5 | -2000000 | 31.25 | 2560 | 0 | 0 | 0 | 0 | 0 |
| `swiart.howitzer.2.5` | — | 6 | -2000000 | 31.25 | 3560 | 0 | 0 | 0 | 0 | 0 |
| `swiart.howitzer.2.6` | — | 7 | -2000000 | 31.25 | 5560 | 0 | 0 | 0 | 0 | 0 |
| `swiba2.drummer18.2.1` | Barracks 18c drummer18 protection +15 (lvl 2) | 2 | 15 | 15.62 | 706 | 0 | 0 | 50 | 0 | 0 |
| `swiba2.grenadier.1.1` | Barracks 18c grenadier damage +2 (lvl 2) | 2 | 2 | 15.62 | 2000 | 0 | 0 | 800 | 0 | 0 |
| `swiba2.grenadier.1.2` | Barracks 18c grenadier damage +3 (lvl 3) | 3 | 3 | 15.62 | 12000 | 0 | 0 | 1800 | 0 | 0 |
| `swiba2.grenadier.1.3` | Barracks 18c grenadier damage +4 (lvl 4) | 4 | 4 | 15.62 | 32000 | 0 | 0 | 2800 | 0 | 0 |
| `swiba2.grenadier.1.4` | Barracks 18c grenadier damage +5 (lvl 5) | 5 | 5 | 15.62 | 42000 | 0 | 0 | 3800 | 0 | 0 |
| `swiba2.grenadier.1.5` | Barracks 18c grenadier damage +6 (lvl 6) | 6 | 6 | 15.62 | 52000 | 0 | 0 | 4800 | 0 | 0 |
| `swiba2.grenadier.1.6` | Barracks 18c grenadier damage +1500 (lvl 7) | 7 | 1500 | 15.62 | 62000 | 0 | 0 | 15800 | 0 | 0 |
| `swiba2.grenadier.2.1` | Barracks 18c grenadier protection +1 (lvl 2) | 2 | 1 | 15.62 | 3706 | 0 | 0 | 350 | 0 | 0 |
| `swiba2.grenadier.2.2` | Barracks 18c grenadier protection +2 (lvl 3) | 3 | 2 | 15.62 | 11030 | 0 | 0 | 1350 | 0 | 0 |
| `swiba2.grenadier.2.3` | Barracks 18c grenadier protection +3 (lvl 4) | 4 | 3 | 15.62 | 35706 | 0 | 0 | 3000 | 0 | 0 |
| `swiba2.grenadier.2.4` | Barracks 18c grenadier protection +1 (lvl 5) | 5 | 1 | 15.62 | 36556 | 0 | 0 | 3350 | 0 | 0 |
| `swiba2.grenadier.2.5` | Barracks 18c grenadier protection +2 (lvl 6) | 6 | 2 | 15.62 | 30060 | 0 | 0 | 1350 | 0 | 0 |
| `swiba2.grenadier.2.6` | Barracks 18c grenadier protection +3 (lvl 7) | 7 | 3 | 15.62 | 64000 | 0 | 0 | 1350 | 0 | 0 |
| `swiba2.jagerswi.1.1` | Barracks 18c jagerswi damage +3 (lvl 2) | 2 | 3 | 15.62 | 3000 | 0 | 0 | 750 | 0 | 0 |
| `swiba2.jagerswi.1.2` | Barracks 18c jagerswi damage +2 (lvl 3) | 3 | 2 | 15.62 | 4000 | 0 | 0 | 1100 | 0 | 0 |
| `swiba2.jagerswi.1.3` | Barracks 18c jagerswi damage +1 (lvl 4) | 4 | 1 | 15.62 | 7000 | 0 | 0 | 1800 | 0 | 0 |
| `swiba2.jagerswi.1.4` | Barracks 18c jagerswi damage +3 (lvl 5) | 5 | 3 | 15.62 | 12000 | 0 | 0 | 350 | 0 | 0 |
| `swiba2.jagerswi.1.5` | Barracks 18c jagerswi damage +2 (lvl 6) | 6 | 2 | 15.62 | 32020 | 0 | 0 | 850 | 0 | 0 |
| `swiba2.jagerswi.1.6` | Barracks 18c jagerswi damage +1 (lvl 7) | 7 | 1 | 15.62 | 45200 | 0 | 0 | 1330 | 0 | 0 |
| `swiba2.jagerswi.2.1` | Barracks 18c jagerswi protection +1 (lvl 2) | 2 | 1 | 15.62 | 3706 | 0 | 0 | 350 | 0 | 0 |
| `swiba2.jagerswi.2.2` | Barracks 18c jagerswi protection +1 (lvl 3) | 3 | 1 | 15.62 | 12060 | 0 | 0 | 1350 | 0 | 0 |
| `swiba2.jagerswi.2.3` | Barracks 18c jagerswi protection +1 (lvl 4) | 4 | 1 | 15.62 | 36706 | 0 | 0 | 2250 | 0 | 0 |
| `swiba2.jagerswi.2.4` | Barracks 18c jagerswi protection +1 (lvl 5) | 5 | 1 | 15.62 | 36706 | 0 | 0 | 3350 | 0 | 0 |
| `swiba2.jagerswi.2.5` | Barracks 18c jagerswi protection +1 (lvl 6) | 6 | 1 | 15.62 | 37060 | 0 | 0 | 1350 | 0 | 0 |
| `swiba2.jagerswi.2.6` | Barracks 18c jagerswi protection +1 (lvl 7) | 7 | 1 | 15.62 | 16706 | 0 | 0 | 1350 | 0 | 0 |
| `swiba2.musketeer18.1.1` | Barracks 18c musketeer18 damage +1 (lvl 2) | 2 | 1 | 15.62 | 1000 | 0 | 0 | 800 | 0 | 0 |
| `swiba2.musketeer18.1.2` | Barracks 18c musketeer18 damage +1 (lvl 3) | 3 | 1 | 15.62 | 1500 | 0 | 0 | 800 | 0 | 0 |
| `swiba2.musketeer18.1.3` | Barracks 18c musketeer18 damage +2 (lvl 4) | 4 | 2 | 15.62 | 2000 | 0 | 0 | 800 | 0 | 0 |
| `swiba2.musketeer18.1.4` | Barracks 18c musketeer18 damage +2 (lvl 5) | 5 | 2 | 15.62 | 2500 | 0 | 0 | 800 | 0 | 0 |
| `swiba2.musketeer18.1.5` | Barracks 18c musketeer18 damage +3 (lvl 6) | 6 | 3 | 15.62 | 3000 | 0 | 0 | 800 | 0 | 0 |
| `swiba2.musketeer18.1.6` | Barracks 18c musketeer18 damage +3 (lvl 7) | 7 | 3 | 15.62 | 3500 | 0 | 0 | 800 | 0 | 0 |
| `swiba2.musketeer18.2.1` | Barracks 18c musketeer18 protection +1 (lvl 2) | 2 | 1 | 15.62 | 3706 | 0 | 0 | 350 | 0 | 0 |
| `swiba2.musketeer18.2.2` | Barracks 18c musketeer18 protection +2 (lvl 3) | 3 | 2 | 15.62 | 11030 | 0 | 0 | 1350 | 0 | 0 |
| `swiba2.musketeer18.2.3` | Barracks 18c musketeer18 protection +2 (lvl 4) | 4 | 2 | 15.62 | 35706 | 0 | 0 | 4000 | 0 | 0 |
| `swiba2.musketeer18.2.4` | Barracks 18c musketeer18 protection +1 (lvl 5) | 5 | 1 | 15.62 | 36556 | 0 | 0 | 4350 | 0 | 0 |
| `swiba2.musketeer18.2.5` | Barracks 18c musketeer18 protection +2 (lvl 6) | 6 | 2 | 15.62 | 30060 | 0 | 0 | 1350 | 0 | 0 |
| `swiba2.musketeer18.2.6` | Barracks 18c musketeer18 protection +2 (lvl 7) | 7 | 2 | 15.62 | 37600 | 0 | 0 | 1350 | 0 | 0 |
| `swiba2.officer18.1.1` | Barracks 18c officer18 damage +30 (lvl 2) | 2 | 30 | 15.62 | 1000 | 0 | 0 | 800 | 0 | 0 |
| `swiba2.officer18.2.1` | Barracks 18c officer18 protection +12 (lvl 2) | 2 | 12 | 15.62 | 1706 | 0 | 0 | 350 | 0 | 0 |
| `swiba2.pikeman18.1.1` | Barracks 18c pikeman18 damage +2 (lvl 2) | 2 | 2 | 15.62 | 2000 | 0 | 0 | 800 | 0 | 0 |
| `swiba2.pikeman18.1.2` | Barracks 18c pikeman18 damage +2 (lvl 3) | 3 | 2 | 15.62 | 8000 | 0 | 0 | 1200 | 0 | 0 |
| `swiba2.pikeman18.1.3` | Barracks 18c pikeman18 damage +2 (lvl 4) | 4 | 2 | 15.62 | 20000 | 0 | 0 | 2500 | 0 | 0 |
| `swiba2.pikeman18.1.4` | Barracks 18c pikeman18 damage +2 (lvl 5) | 5 | 2 | 15.62 | 32000 | 0 | 0 | 2800 | 0 | 0 |
| `swiba2.pikeman18.1.5` | Barracks 18c pikeman18 damage +2 (lvl 6) | 6 | 2 | 15.62 | 32000 | 0 | 0 | 3800 | 0 | 0 |
| `swiba2.pikeman18.1.6` | Barracks 18c pikeman18 damage +2 (lvl 7) | 7 | 2 | 15.62 | 40500 | 0 | 0 | 4800 | 0 | 0 |
| `swiba2.pikeman18.2.1` | Barracks 18c pikeman18 protection +2 (lvl 2) | 2 | 2 | 15.62 | 1500 | 0 | 0 | 500 | 0 | 0 |
| `swiba2.pikeman18.2.2` | Barracks 18c pikeman18 protection +3 (lvl 3) | 3 | 3 | 15.62 | 7000 | 0 | 0 | 1500 | 0 | 0 |
| `swiba2.pikeman18.2.3` | Barracks 18c pikeman18 protection +2 (lvl 4) | 4 | 2 | 15.62 | 37000 | 0 | 0 | 2000 | 0 | 0 |
| `swiba2.pikeman18.2.4` | Barracks 18c pikeman18 protection +3 (lvl 5) | 5 | 3 | 15.62 | 37000 | 0 | 0 | 5500 | 0 | 0 |
| `swiba2.pikeman18.2.5` | Barracks 18c pikeman18 protection +2 (lvl 6) | 6 | 2 | 15.62 | 37000 | 0 | 0 | 5500 | 0 | 0 |
| `swiba2.pikeman18.2.6` | Barracks 18c pikeman18 protection +3 (lvl 7) | 7 | 3 | 15.62 | 64600 | 0 | 0 | 5500 | 0 | 0 |
| `swibar.1` | — | 1 | 140 | 15.62 | 750 | 0 | 0 | 250 | 0 | 0 |
| `swibar.2` | — | 2 | 180 | 15.62 | 25600 | 0 | 0 | 3350 | 2000 | 0 |
| `swibar.drummer.2.1` | Barracks 17c drummer protection +12 (lvl 2) | 2 | 12 | 15.62 | 670 | 0 | 0 | 45 | 0 | 0 |
| `swibar.musketeer.1.1` | Barracks 17c musketeer damage +1 (lvl 2) | 2 | 1 | 15.62 | 2000 | 0 | 0 | 100 | 0 | 0 |
| `swibar.musketeer.1.2` | Barracks 17c musketeer damage +1 (lvl 3) | 3 | 1 | 15.62 | 1000 | 0 | 0 | 300 | 0 | 0 |
| `swibar.musketeer.1.3` | Barracks 17c musketeer damage +2 (lvl 4) | 4 | 2 | 15.62 | 500 | 0 | 0 | 700 | 0 | 0 |
| `swibar.musketeer.2.1` | Barracks 17c musketeer protection +1 (lvl 2) | 2 | 1 | 15.62 | 170 | 0 | 0 | 50 | 100 | 0 |
| `swibar.musketeer.2.2` | Barracks 17c musketeer protection +2 (lvl 3) | 3 | 2 | 15.62 | 405 | 0 | 0 | 150 | 200 | 0 |
| `swibar.musketeer.2.3` | Barracks 17c musketeer protection +2 (lvl 4) | 4 | 2 | 15.62 | 1570 | 0 | 0 | 100 | 350 | 0 |
| `swibar.musketeer.2.4` | Barracks 17c musketeer protection +1 (lvl 5) | 5 | 1 | 15.62 | 1556 | 0 | 0 | 550 | 100 | 0 |
| `swibar.musketeer.2.5` | Barracks 17c musketeer protection +2 (lvl 6) | 6 | 2 | 15.62 | 1060 | 0 | 0 | 850 | 400 | 0 |
| `swibar.musketeer.2.6` | Barracks 17c musketeer protection +2 (lvl 7) | 7 | 2 | 15.62 | 3700 | 0 | 0 | 450 | 700 | 0 |
| `swibar.officer.1.1` | Barracks 17c officer damage +20 (lvl 2) | 2 | 20 | 15.62 | 200 | 0 | 0 | 25 | 0 | 0 |
| `swibar.officer.2.1` | Barracks 17c officer protection +6 (lvl 2) | 2 | 6 | 15.62 | 1650 | 0 | 0 | 395 | 0 | 0 |
| `swibar.pikemanswi.1.1` | Barracks 17c pikemanswi damage +2 (lvl 2) | 2 | 2 | 15.62 | 200 | 0 | 0 | 50 | 0 | 0 |
| `swibar.pikemanswi.1.2` | Barracks 17c pikemanswi damage +3 (lvl 3) | 3 | 3 | 15.62 | 1300 | 0 | 0 | 300 | 0 | 0 |
| `swibar.pikemanswi.1.3` | Barracks 17c pikemanswi damage +2 (lvl 4) | 4 | 2 | 15.62 | 3600 | 0 | 0 | 450 | 0 | 0 |
| `swibar.pikemanswi.1.4` | Barracks 17c pikemanswi damage +1 (lvl 5) | 5 | 1 | 15.62 | 7200 | 0 | 0 | 1850 | 0 | 0 |
| `swibar.pikemanswi.1.5` | Barracks 17c pikemanswi damage +1 (lvl 6) | 6 | 1 | 15.62 | 16030 | 0 | 0 | 2000 | 0 | 0 |
| `swibar.pikemanswi.1.6` | — | 7 | 1 | 15.62 | 15000 | 0 | 0 | 1875 | 0 | 0 |
| `swibar.pikemanswi.2.1` | Barracks 17c pikemanswi protection +2 (lvl 2) | 2 | 2 | 15.62 | 150 | 0 | 0 | 50 | 0 | 0 |
| `swibar.pikemanswi.2.2` | Barracks 17c pikemanswi protection +2 (lvl 3) | 3 | 2 | 15.62 | 900 | 0 | 0 | 175 | 0 | 0 |
| `swibar.pikemanswi.2.3` | Barracks 17c pikemanswi protection +1 (lvl 4) | 4 | 1 | 15.62 | 4500 | 0 | 0 | 300 | 0 | 0 |
| `swibar.pikemanswi.2.4` | Barracks 17c pikemanswi protection +1 (lvl 5) | 5 | 1 | 15.62 | 9005 | 0 | 0 | 507 | 0 | 0 |
| `swibar.pikemanswi.2.5` | Barracks 17c pikemanswi protection +1 (lvl 6) | 6 | 1 | 15.62 | 18010 | 0 | 0 | 3050 | 0 | 0 |
| `swibar.pikemanswi.2.6` | — | 7 | 1 | 15.62 | 11250 | 0 | 0 | 1500 | 0 | 0 |
| `swibla.1` | Manufacture agricultural equipment (field capacity +100%) | 1 | 100 | 15.62 | 0 | 400 | 0 | 90 | 0 | 0 |
| `swibla.2` | Forge metal armature and gratings (building defence +50) | 1 | 50 | 15.62 | 0 | 0 | 12320 | 350 | 900 | 0 |
| `swibla.3` | Forge harnesses for horses (mounted units recruitment speed -33%) | 1 | -3333333 | 15.62 | 0 | 0 | 0 | 3650 | 5300 | 8200 |
| `swibla.4` | Forge bayonets and broadswords for infantry (18c musketeer/grenadier melee attack +5) | 1 | 5 | 15.62 | 0 | 1300 | 0 | 1500 | 900 | 5000 |
| `swibla.5` | Forge new types of broadswords and sabres (cavalry and sword clansman attack +5) | 1 | 5 | 15.62 | 0 | 0 | 0 | 4000 | 7900 | 0 |
| `swibla.6` | Forge new cuirasses (armoured soldiers defence +2) | 1 | 2 | 15.62 | 0 | 0 | 0 | 4950 | 10500 | 0 |
| `swicen.1` | — | 1 | 0 | 9.38 | 30000 | 0 | 0 | 5000 | 2000 | 2000 |
| `swista.cuirassier.1.1` | Stable cuirassier damage +1 (lvl 2) | 2 | 1 | 15.62 | 12000 | 0 | 0 | 600 | 0 | 0 |
| `swista.cuirassier.1.2` | Stable cuirassier damage +1 (lvl 3) | 3 | 1 | 15.62 | 32000 | 0 | 0 | 1300 | 0 | 0 |
| `swista.cuirassier.1.3` | Stable cuirassier damage +1 (lvl 4) | 4 | 1 | 15.62 | 62000 | 0 | 0 | 2200 | 0 | 0 |
| `swista.cuirassier.1.4` | Stable cuirassier damage +2 (lvl 5) | 5 | 2 | 15.62 | 61000 | 0 | 0 | 3150 | 0 | 0 |
| `swista.cuirassier.1.5` | Stable cuirassier damage +2 (lvl 6) | 6 | 2 | 15.62 | 57055 | 0 | 0 | 4100 | 0 | 0 |
| `swista.cuirassier.1.6` | Stable cuirassier damage +3 (lvl 7) | 7 | 3 | 15.62 | 49050 | 0 | 0 | 8020 | 0 | 0 |
| `swista.cuirassier.2.1` | Stable cuirassier protection +2 (lvl 2) | 2 | 2 | 15.62 | 1760 | 0 | 0 | 350 | 1000 | 0 |
| `swista.cuirassier.2.2` | Stable cuirassier protection +3 (lvl 3) | 3 | 3 | 15.62 | 3000 | 0 | 0 | 750 | 2000 | 0 |
| `swista.cuirassier.2.3` | Stable cuirassier protection +3 (lvl 4) | 4 | 3 | 15.62 | 7600 | 0 | 0 | 300 | 3030 | 0 |
| `swista.cuirassier.2.4` | Stable cuirassier protection +2 (lvl 5) | 5 | 2 | 15.62 | 8700 | 0 | 0 | 6200 | 100 | 0 |
| `swista.cuirassier.2.5` | Stable cuirassier protection +1 (lvl 6) | 6 | 1 | 15.62 | 8700 | 0 | 0 | 2350 | 5000 | 0 |
| `swista.cuirassier.2.6` | Stable cuirassier protection +1 (lvl 7) | 7 | 1 | 15.62 | 9700 | 0 | 0 | 4444 | 7060 | 0 |
| `swista.dragoon.1.1` | Stable dragoon damage +1 (lvl 2) | 2 | 1 | 15.62 | 500 | 0 | 0 | 150 | 0 | 0 |
| `swista.dragoon.1.2` | Stable dragoon damage +1 (lvl 3) | 3 | 1 | 15.62 | 700 | 0 | 0 | 200 | 0 | 0 |
| `swista.dragoon.1.3` | Stable dragoon damage +2 (lvl 4) | 4 | 2 | 15.62 | 900 | 0 | 0 | 340 | 0 | 0 |
| `swista.dragoon.1.4` | Stable dragoon damage +1 (lvl 5) | 5 | 1 | 15.62 | 0 | 0 | 0 | 0 | 0 | 0 |
| `swista.dragoon.1.5` | Stable dragoon damage +1 (lvl 6) | 6 | 1 | 15.62 | 0 | 0 | 0 | 0 | 0 | 0 |
| `swista.dragoon.1.6` | Stable dragoon damage +3 (lvl 7) | 7 | 3 | 15.62 | 0 | 0 | 0 | 0 | 0 | 0 |
| `swista.dragoon.2.1` | Stable dragoon protection +1 (lvl 2) | 2 | 1 | 15.62 | 900 | 0 | 0 | 150 | 0 | 0 |
| `swista.dragoon.2.2` | Stable dragoon protection +2 (lvl 3) | 3 | 2 | 15.62 | 6600 | 0 | 0 | 750 | 0 | 0 |
| `swista.dragoon.2.3` | Stable dragoon protection +2 (lvl 4) | 4 | 2 | 15.62 | 5000 | 0 | 0 | 1250 | 0 | 0 |
| `swista.dragoon.2.4` | Stable dragoon protection +1 (lvl 5) | 5 | 1 | 15.62 | 3000 | 0 | 0 | 700 | 0 | 0 |
| `swista.dragoon.2.5` | Stable dragoon protection +2 (lvl 6) | 6 | 2 | 15.62 | 1000 | 0 | 0 | 2350 | 0 | 0 |
| `swista.dragoon.2.6` | Stable dragoon protection +2 (lvl 7) | 7 | 2 | 15.62 | 6001 | 0 | 0 | 6000 | 0 | 0 |
| `swista.dragoon18.1.1` | Stable dragoon18 damage +2 (lvl 2) | 2 | 2 | 15.62 | 2000 | 0 | 0 | 100 | 0 | 0 |
| `swista.dragoon18.1.2` | Stable dragoon18 damage +2 (lvl 3) | 3 | 2 | 15.62 | 9000 | 0 | 0 | 350 | 0 | 0 |
| `swista.dragoon18.1.3` | Stable dragoon18 damage +4 (lvl 4) | 4 | 4 | 15.62 | 12000 | 0 | 0 | 400 | 0 | 0 |
| `swista.dragoon18.1.4` | Stable dragoon18 damage +2 (lvl 5) | 5 | 2 | 15.62 | 23000 | 0 | 0 | 580 | 0 | 0 |
| `swista.dragoon18.1.5` | Stable dragoon18 damage +2 (lvl 6) | 6 | 2 | 15.62 | 32000 | 0 | 0 | 680 | 0 | 0 |
| `swista.dragoon18.1.6` | Stable dragoon18 damage +4 (lvl 7) | 7 | 4 | 15.62 | 42000 | 0 | 0 | 780 | 0 | 0 |
| `swista.dragoon18.2.1` | Stable dragoon18 protection +1 (lvl 2) | 2 | 1 | 15.62 | 760 | 0 | 0 | 935 | 0 | 0 |
| `swista.dragoon18.2.2` | Stable dragoon18 protection +1 (lvl 3) | 3 | 1 | 15.62 | 1260 | 0 | 0 | 1150 | 0 | 0 |
| `swista.dragoon18.2.3` | Stable dragoon18 protection +2 (lvl 4) | 4 | 2 | 15.62 | 15600 | 0 | 0 | 2350 | 0 | 0 |
| `swista.dragoon18.2.4` | Stable dragoon18 protection +1 (lvl 5) | 5 | 1 | 15.62 | 17600 | 0 | 0 | 3350 | 0 | 0 |
| `swista.dragoon18.2.5` | Stable dragoon18 protection +2 (lvl 6) | 6 | 2 | 15.62 | 19600 | 0 | 0 | 5350 | 0 | 0 |
| `swista.dragoon18.2.6` | Stable dragoon18 protection +3 (lvl 7) | 7 | 3 | 15.62 | 21760 | 0 | 0 | 9350 | 0 | 0 |
| `swista.hussarswi.1.1` | Stable hussarswi damage +2 (lvl 2) | 2 | 2 | 15.62 | 0 | 0 | 0 | 2800 | 1600 | 0 |
| `swista.hussarswi.1.2` | Stable hussarswi damage +2 (lvl 3) | 3 | 2 | 15.62 | 0 | 0 | 0 | 2800 | 1400 | 0 |
| `swista.hussarswi.1.3` | Stable hussarswi damage +2 (lvl 4) | 4 | 2 | 15.62 | 10200 | 0 | 0 | 0 | 3000 | 0 |
| `swista.hussarswi.1.4` | Stable hussarswi damage +2 (lvl 5) | 5 | 2 | 15.62 | 42000 | 0 | 0 | 0 | 2000 | 0 |
| `swista.hussarswi.1.5` | Stable hussarswi damage +2 (lvl 6) | 6 | 2 | 15.62 | 29200 | 0 | 0 | 0 | 5500 | 0 |
| `swista.hussarswi.1.6` | Stable hussarswi damage +2 (lvl 7) | 7 | 2 | 15.62 | 40000 | 0 | 0 | 0 | 4000 | 0 |
| `swista.hussarswi.2.1` | Stable hussarswi protection +1 (lvl 2) | 2 | 1 | 15.62 | 150 | 0 | 0 | 1250 | 0 | 0 |
| `swista.hussarswi.2.2` | Stable hussarswi protection +2 (lvl 3) | 3 | 2 | 15.62 | 3200 | 0 | 0 | 2450 | 0 | 0 |
| `swista.hussarswi.2.3` | Stable hussarswi protection +2 (lvl 4) | 4 | 2 | 15.62 | 3600 | 0 | 0 | 3350 | 0 | 0 |
| `swista.hussarswi.2.4` | Stable hussarswi protection +1 (lvl 5) | 5 | 1 | 15.62 | 6000 | 0 | 0 | 10350 | 0 | 0 |
| `swista.hussarswi.2.5` | Stable hussarswi protection +2 (lvl 6) | 6 | 2 | 15.62 | 9000 | 0 | 0 | 13350 | 0 | 0 |
| `swista.hussarswi.2.6` | Stable hussarswi protection +2 (lvl 7) | 7 | 2 | 15.62 | 48000 | 0 | 0 | 22150 | 0 | 0 |
| `swista.reiter.1.1` | Stable reiter damage +1 (lvl 2) | 2 | 1 | 15.62 | 500 | 0 | 0 | 100 | 0 | 0 |
| `swista.reiter.1.2` | Stable reiter damage +2 (lvl 3) | 3 | 2 | 15.62 | 900 | 0 | 0 | 220 | 0 | 0 |
| `swista.reiter.1.3` | Stable reiter damage +1 (lvl 4) | 4 | 1 | 15.62 | 4400 | 0 | 0 | 280 | 0 | 0 |
| `swista.reiter.1.4` | Stable reiter damage +1 (lvl 5) | 5 | 1 | 15.62 | 2250 | 0 | 0 | 320 | 0 | 0 |
| `swista.reiter.1.5` | Stable reiter damage +1 (lvl 6) | 6 | 1 | 15.62 | 3030 | 0 | 0 | 600 | 0 | 0 |
| `swista.reiter.1.6` | Stable reiter damage +1 (lvl 7) | 7 | 1 | 15.62 | 7000 | 0 | 0 | 1800 | 0 | 0 |
| `swista.reiter.2.1` | Stable reiter protection +2 (lvl 2) | 2 | 2 | 15.62 | 200 | 0 | 0 | 135 | 300 | 0 |
| `swista.reiter.2.2` | Stable reiter protection +3 (lvl 3) | 3 | 3 | 15.62 | 600 | 0 | 0 | 100 | 400 | 0 |
| `swista.reiter.2.3` | Stable reiter protection +3 (lvl 4) | 4 | 3 | 15.62 | 800 | 0 | 0 | 200 | 560 | 0 |
| `swista.reiter.2.4` | Stable reiter protection +2 (lvl 5) | 5 | 2 | 15.62 | 1600 | 0 | 0 | 300 | 640 | 0 |
| `swista.reiter.2.5` | Stable reiter protection +1 (lvl 6) | 6 | 1 | 15.62 | 3200 | 0 | 0 | 350 | 300 | 0 |
| `swista.reiter.2.6` | Stable reiter protection +1 (lvl 7) | 7 | 1 | 15.62 | 16000 | 0 | 0 | 1000 | 5000 | 0 |
| `ukrwwa.1` | — | 2 | 5 | 0.03 | 0 | 400 | 0 | 0 | 0 | 0 |

### sco — Scotland

| sid | имя (EN) | level | value | время (s) | F | W | S | G | I | C |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `eurcoa.1` | — | 2 | 5 | 9.38 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `eurcoa.2` | — | 3 | 8 | 9.38 | 5250 | 0 | 0 | 4950 | 0 | 0 |
| `eurcoa.3` | — | 4 | 10 | 9.38 | 12500 | 0 | 0 | 9250 | 0 | 0 |
| `eurcoa.4` | — | 5 | 12 | 9.38 | 15800 | 0 | 0 | 18500 | 0 | 0 |
| `eurcoa.5` | — | 6 | 15 | 9.38 | 19800 | 0 | 0 | 21050 | 0 | 0 |
| `eurcoa.6` | — | 7 | 40 | 9.38 | 50200 | 0 | 0 | 25950 | 0 | 0 |
| `eurgol.1` | — | 2 | 5 | 9.38 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `eurgol.2` | — | 3 | 8 | 9.38 | 5250 | 0 | 0 | 4950 | 0 | 0 |
| `eurgol.3` | — | 4 | 10 | 9.38 | 12500 | 0 | 0 | 9250 | 0 | 0 |
| `eurgol.4` | — | 5 | 12 | 9.38 | 15800 | 0 | 0 | 18500 | 0 | 0 |
| `eurgol.5` | — | 6 | 15 | 9.38 | 19800 | 0 | 0 | 21050 | 0 | 0 |
| `eurgol.6` | — | 7 | 40 | 9.38 | 50200 | 0 | 0 | 25950 | 0 | 0 |
| `euriro.1` | — | 2 | 5 | 9.38 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `euriro.2` | — | 3 | 8 | 9.38 | 5250 | 0 | 0 | 4950 | 0 | 0 |
| `euriro.3` | — | 4 | 10 | 9.38 | 12500 | 0 | 0 | 9250 | 0 | 0 |
| `euriro.4` | — | 5 | 12 | 9.38 | 15800 | 0 | 0 | 18500 | 0 | 0 |
| `euriro.5` | — | 6 | 15 | 9.38 | 19800 | 0 | 0 | 21050 | 0 | 0 |
| `euriro.6` | — | 7 | 40 | 9.38 | 50200 | 0 | 0 | 25950 | 0 | 0 |
| `eurpor.1` | — | 1 | 50 | 46.88 | 0 | 20000 | 0 | 1500 | 0 | 0 |
| `eurswa.1` | — | 2 | 5 | 0.03 | 0 | 0 | 500 | 0 | 0 | 0 |
| `eurtow.1` | — | 2 | -20 | 31.25 | 0 | 0 | 0 | 250 | 0 | 0 |
| `eurtow.2` | — | 3 | -20 | 31.25 | 0 | 0 | 0 | 0 | 350 | 0 |
| `eurtow.3` | — | 4 | -10 | 31.25 | 0 | 0 | 0 | 0 | 0 | 400 |
| `eurtow.4` | — | 5 | -10 | 31.25 | 0 | 0 | 0 | 0 | 450 | 0 |
| `eurtow.5` | — | 6 | -10 | 31.25 | 0 | 0 | 0 | 0 | 0 | 500 |
| `ferry.1` | Improve transport vessel design (+%value% capacity) | 2 | 200 | 15.62 | 1000 | 0 | 0 | 1250 | 0 | 0 |
| `scoaca.1` | Cultivate new cultures of wheat (harvesting +40%) | 1 | 40 | 15.62 | 0 | 200 | 0 | 325 | 0 | 0 |
| `scoaca.10` | Raise builders' salary (building construction time -75%) | 1 | -7500000 | 15.62 | 0 | 0 | 0 | 2650 | 0 | 0 |
| `scoaca.11` | Research new fortification grades (durability of walls and towers +80) | 1 | 80 | 15.62 | 0 | 0 | 16200 | 1500 | 0 | 0 |
| `scoaca.12` | Improve firearms: rifled barrel (fire power +10%) | 1 | 10 | 15.62 | 0 | 0 | 0 | 0 | 5000 | 0 |
| `scoaca.13` | Research granular gunpowder (fire power +10%) | 1 | 10 | 15.62 | 0 | 0 | 0 | 4000 | 0 | 0 |
| `scoaca.14` | Research new sulphur purification methods (fire power +15%) | 1 | 15 | 15.62 | 0 | 0 | 0 | 7000 | 0 | 0 |
| `scoaca.15` | Research new nitre purification methods (fire power +25%) | 1 | 25 | 15.62 | 0 | 0 | 0 | 0 | 0 | 11000 |
| `scoaca.16` | Research improved additions to gunpowder formula (artillery range +5%) | 1 | 5 | 15.62 | 0 | 0 | 0 | 2000 | 12150 | 0 |
| `scoaca.17` | Design new barrel types: unicorn, carronade (artillery range +10%) | 1 | 10 | 15.62 | 0 | 0 | 3000 | 4550 | 19200 | 0 |
| `scoaca.18` | Design more durable gun carriage: Gribovalle system (artillery durability +50%) | 1 | 50 | 15.62 | 0 | 0 | 0 | 500 | 3830 | 1500 |
| `scoaca.19` | %color(FFAA00)%Design multi-barrelled cannon | — | — | — | — | — | — | — | — | — |
| `scoaca.2` | Cultivate new cultures of rye (harvesting +50%) | 1 | 50 | 15.62 | 0 | 2400 | 0 | 625 | 0 | 0 |
| `scoaca.20` | Research new sighting devices for artillery (artillery accuracy +35%) | 1 | -35 | 15.62 | 0 | 3540 | 0 | 2000 | 0 | 7250 |
| `scoaca.21` | Finance artillery repair shops (repair all artillery) | 1 | 25 | 15.62 | 0 | 350 | 0 | 100 | 0 | 250 |
| `scoaca.22` | Develop geology (previously hidden deposits appear on the map) | 1 | 0 | 15.62 | 0 | 0 | 0 | 250 | 0 | 0 |
| `scoaca.23` | Develop mining (stone excavation efficiency +100%) | 1 | 100 | 15.62 | 0 | 0 | 0 | 1550 | 3000 | 0 |
| `scoaca.24` | Raise miners' salary (stone excavation efficiency +200%) | 1 | 200 | 15.62 | 4200 | 0 | 0 | 1550 | 0 | 12520 |
| `scoaca.25` | Design Montgolfier (reveals the whole map) | 1 | 0 | 15.62 | 0 | 0 | 0 | 12750 | 0 | 0 |
| `scoaca.26` | Develop medical science (heals all live units) | 1 | 50 | 31.25 | 0 | 0 | 0 | 200 | 0 | 200 |
| `scoaca.27` | Develop mathematics (artillery accuracy +35%) | 1 | -35 | 15.62 | 0 | 9540 | 0 | 12000 | 0 | 65200 |
| `scoaca.28` | Design new rigging types (ship speed +40%) | 1 | 40 | 15.62 | 0 | 65400 | 0 | 24050 | 0 | 0 |
| `scoaca.29` | Design new rib system and new hulls (battleship construction) | 1 | 0 | 15.62 | 0 | 32300 | 0 | 6800 | 9000 | 12800 |
| `scoaca.3` | Raise agriculturists' salary (harvesting +50%) | 1 | 50 | 15.62 | 0 | 3600 | 0 | 850 | 0 | 0 |
| `scoaca.30` | Train carpenters (shipbuilding speed x10) | 1 | -5000000 | 15.62 | 0 | 2300 | 42700 | 1150 | 0 | 0 |
| `scoaca.31` | Design wheellock (rate of fire +30%) | 1 | -30 | 15.62 | 0 | 0 | 6000 | 5500 | 4200 | 0 |
| `scoaca.32` | Design flintlock (musket cost -50%) | 1 | 0 | 15.62 | 0 | 0 | 0 | 6050 | 0 | 7750 |
| `scoaca.33` | Design paper cartridge and iron ramrod (rate of fire +30%) | 1 | -30 | 15.62 | 0 | 5000 | 0 | 5500 | 0 | 15200 |
| `scoaca.34` | Research improved steel grades for cuirasses (armoured soldier defence +2) | 1 | 2 | 15.62 | 0 | 0 | 0 | 9750 | 0 | 0 |
| `scoaca.35` | Design bayonet: barrel-inserted, bayonet with a tube (cold steel weapons +5) | 1 | 5 | 15.62 | 0 | 0 | 0 | 11500 | 0 | 0 |
| `scoaca.36` | Research new steel grades (18c musketeer/grenadier melee attack efficiency +25%) | 1 | 25 | 15.62 | 0 | 0 | 0 | 19500 | 0 | 0 |
| `scoaca.4` | Carry out field melioration (field capacity +200%) | 1 | 200 | 15.62 | 0 | 1000 | 0 | 475 | 0 | 0 |
| `scoaca.5` | Design new tackle and fishing nets (boat efficiency +100%) | 1 | 100 | 15.62 | 0 | 12400 | 0 | 2520 | 0 | 0 |
| `scoaca.6` | Develop new woodworking methods (frigate building) | 1 | 0 | 15.62 | 0 | 12400 | 0 | 7040 | 0 | 0 |
| `scoaca.7` | Build new shipyards for fishing boats (fishing boat cost -85%) | 1 | 0 | 15.62 | 0 | 7300 | 0 | 1220 | 0 | 0 |
| `scoaca.8` | Design new woodworking tools (woodcutting efficiency +100%) | 1 | 100 | 15.62 | 5500 | 0 | 0 | 550 | 0 | 0 |
| `scoaca.9` | Use new construction materials (durability of buildings +85) | 1 | 85 | 15.62 | 0 | 9400 | 7850 | 1150 | 0 | 0 |
| `scoart.cannon.1.1` | — | 2 | — | 10.0 | 0 | 1000 | 500 | 300 | 0 | 0 |
| `scoart.cannon.1.2` | — | 3 | — | 10.0 | 0 | 3000 | 1000 | 500 | 0 | 0 |
| `scoart.cannon.1.3` | — | 4 | — | 10.0 | 0 | 6000 | 2000 | 1000 | 0 | 0 |
| `scoart.cannon.1.4` | — | 5 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `scoart.cannon.1.5` | — | 6 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `scoart.cannon.1.6` | — | 7 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `scoart.cannon.2.1` | — | 2 | -2500000 | 10.0 | 0 | 0 | 0 | 500 | 1000 | 0 |
| `scoart.cannon.2.2` | — | 3 | -2500000 | 10.0 | 0 | 0 | 0 | 1000 | 2000 | 0 |
| `scoart.cannon.2.3` | — | 4 | -2500000 | 10.0 | 0 | 0 | 0 | 2000 | 3000 | 0 |
| `scoart.cannon.2.4` | — | 5 | -2000000 | 15.62 | 2560 | 0 | 0 | 0 | 0 | 0 |
| `scoart.cannon.2.5` | — | 6 | -2000000 | 15.62 | 3560 | 0 | 0 | 0 | 0 | 0 |
| `scoart.cannon.2.6` | — | 7 | -2000000 | 15.62 | 5560 | 0 | 0 | 0 | 0 | 0 |
| `scoart.howitzer.1.1` | — | 2 | — | 10.0 | 0 | 1000 | 500 | 300 | 0 | 0 |
| `scoart.howitzer.1.2` | — | 3 | — | 10.0 | 0 | 3000 | 1000 | 500 | 0 | 0 |
| `scoart.howitzer.1.3` | — | 4 | — | 10.0 | 0 | 6000 | 2000 | 1000 | 0 | 0 |
| `scoart.howitzer.1.4` | — | 5 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `scoart.howitzer.1.5` | — | 6 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `scoart.howitzer.1.6` | — | 7 | — | 15.62 | 1760 | 0 | 0 | 350 | 0 | 0 |
| `scoart.howitzer.2.1` | — | 2 | -2500000 | 10.0 | 0 | 0 | 0 | 500 | 1000 | 0 |
| `scoart.howitzer.2.2` | — | 3 | -2500000 | 10.0 | 0 | 0 | 0 | 1000 | 2000 | 0 |
| `scoart.howitzer.2.3` | — | 4 | -2500000 | 10.0 | 0 | 0 | 0 | 2000 | 3000 | 0 |
| `scoart.howitzer.2.4` | — | 5 | -2000000 | 31.25 | 2560 | 0 | 0 | 0 | 0 | 0 |
| `scoart.howitzer.2.5` | — | 6 | -2000000 | 31.25 | 3560 | 0 | 0 | 0 | 0 | 0 |
| `scoart.howitzer.2.6` | — | 7 | -2000000 | 31.25 | 5560 | 0 | 0 | 0 | 0 | 0 |
| `scoba2.archersco.1.1` | Barracks 18c archersco damage +2 (lvl 2) | 2 | 2 | 15.62 | 3000 | 0 | 0 | 360 | 0 | 0 |
| `scoba2.archersco.1.2` | Barracks 18c archersco damage +3 (lvl 3) | 3 | 3 | 15.62 | 7500 | 0 | 0 | 700 | 0 | 0 |
| `scoba2.archersco.1.3` | Barracks 18c archersco damage +4 (lvl 4) | 4 | 4 | 15.62 | 9750 | 0 | 0 | 1200 | 0 | 0 |
| `scoba2.archersco.1.4` | Barracks 18c archersco damage +2 (lvl 5) | 5 | 2 | 15.62 | 18000 | 0 | 0 | 1800 | 0 | 0 |
| `scoba2.archersco.1.5` | Barracks 18c archersco damage +4 (lvl 6) | 6 | 4 | 15.62 | 33200 | 0 | 0 | 4320 | 0 | 0 |
| `scoba2.archersco.1.6` | Barracks 18c archersco damage +5 (lvl 7) | 7 | 5 | 15.62 | 55000 | 0 | 0 | 7550 | 0 | 0 |
| `scoba2.archersco.2.1` | Barracks 18c archersco protection +1 (lvl 2) | 2 | 1 | 15.62 | 900 | 0 | 0 | 250 | 0 | 0 |
| `scoba2.archersco.2.2` | Barracks 18c archersco protection +2 (lvl 3) | 3 | 2 | 15.62 | 2200 | 0 | 0 | 450 | 0 | 0 |
| `scoba2.archersco.2.3` | Barracks 18c archersco protection +3 (lvl 4) | 4 | 3 | 15.62 | 5400 | 0 | 0 | 800 | 0 | 0 |
| `scoba2.archersco.2.4` | Barracks 18c archersco protection +3 (lvl 5) | 5 | 3 | 15.62 | 12500 | 0 | 0 | 1000 | 0 | 0 |
| `scoba2.archersco.2.5` | Barracks 18c archersco protection +2 (lvl 6) | 6 | 2 | 15.62 | 20000 | 0 | 0 | 1200 | 0 | 0 |
| `scoba2.archersco.2.6` | Barracks 18c archersco protection +1 (lvl 7) | 7 | 1 | 15.62 | 16500 | 0 | 0 | 1875 | 0 | 0 |
| `scoba2.swordsmansco.1.1` | Barracks 18c swordsmansco damage +2 (lvl 2) | 2 | 2 | 15.62 | 450 | 0 | 0 | 110 | 0 | 0 |
| `scoba2.swordsmansco.1.2` | Barracks 18c swordsmansco damage +3 (lvl 3) | 3 | 3 | 15.62 | 900 | 0 | 0 | 220 | 0 | 0 |
| `scoba2.swordsmansco.1.3` | Barracks 18c swordsmansco damage +4 (lvl 4) | 4 | 4 | 15.62 | 3350 | 0 | 0 | 850 | 0 | 0 |
| `scoba2.swordsmansco.1.4` | Barracks 18c swordsmansco damage +5 (lvl 5) | 5 | 5 | 15.62 | 14400 | 0 | 0 | 2060 | 0 | 0 |
| `scoba2.swordsmansco.1.5` | Barracks 18c swordsmansco damage +6 (lvl 6) | 6 | 6 | 15.62 | 37800 | 0 | 0 | 4525 | 0 | 0 |
| `scoba2.swordsmansco.1.6` | Barracks 18c swordsmansco damage +10 (lvl 7) | 7 | 10 | 15.62 | 90000 | 0 | 0 | 8000 | 0 | 0 |
| `scoba2.swordsmansco.2.1` | Barracks 18c swordsmansco protection +1 (lvl 2) | 2 | 1 | 15.62 | 200 | 0 | 0 | 75 | 0 | 0 |
| `scoba2.swordsmansco.2.2` | Barracks 18c swordsmansco protection +2 (lvl 3) | 3 | 2 | 15.62 | 700 | 0 | 0 | 225 | 0 | 0 |
| `scoba2.swordsmansco.2.3` | Barracks 18c swordsmansco protection +2 (lvl 4) | 4 | 2 | 15.62 | 2500 | 0 | 0 | 560 | 0 | 0 |
| `scoba2.swordsmansco.2.4` | Barracks 18c swordsmansco protection +2 (lvl 5) | 5 | 2 | 15.62 | 7750 | 0 | 0 | 1125 | 0 | 0 |
| `scoba2.swordsmansco.2.5` | Barracks 18c swordsmansco protection +3 (lvl 6) | 6 | 3 | 15.62 | 15800 | 0 | 0 | 1800 | 0 | 0 |
| `scoba2.swordsmansco.2.6` | Barracks 18c swordsmansco protection +5 (lvl 7) | 7 | 5 | 15.62 | 36125 | 0 | 0 | 3350 | 0 | 0 |
| `scobar.1` | — | 1 | 140 | 15.62 | 750 | 0 | 0 | 250 | 0 | 0 |
| `scobar.2` | — | 2 | 180 | 15.62 | 5600 | 0 | 0 | 1350 | 1900 | 0 |
| `scobar.bagpiper.2.1` | Barracks 17c bagpiper protection +10 (lvl 2) | 2 | 10 | 15.62 | 706 | 0 | 0 | 50 | 0 | 0 |
| `scobar.musketeersco.1.1` | Barracks 17c musketeersco damage +1 (lvl 2) | 2 | 1 | 15.62 | 2500 | 0 | 0 | 200 | 0 | 0 |
| `scobar.musketeersco.1.2` | Barracks 17c musketeersco damage +1 (lvl 3) | 3 | 1 | 15.62 | 1500 | 0 | 0 | 400 | 0 | 0 |
| `scobar.musketeersco.1.3` | Barracks 17c musketeersco damage +2 (lvl 4) | 4 | 2 | 15.62 | 500 | 0 | 0 | 800 | 0 | 0 |
| `scobar.musketeersco.2.1` | Barracks 17c musketeersco protection +1 (lvl 2) | 2 | 1 | 15.62 | 250 | 0 | 0 | 30 | 0 | 0 |
| `scobar.musketeersco.2.2` | Barracks 17c musketeersco protection +1 (lvl 3) | 3 | 1 | 15.62 | 500 | 0 | 0 | 400 | 60 | 0 |
| `scobar.musketeersco.2.3` | Barracks 17c musketeersco protection +2 (lvl 4) | 4 | 2 | 15.62 | 875 | 0 | 0 | 225 | 0 | 0 |
| `scobar.musketeersco.2.4` | Barracks 17c musketeersco protection +1 (lvl 5) | 5 | 1 | 15.62 | 4200 | 0 | 0 | 240 | 0 | 0 |
| `scobar.musketeersco.2.5` | Barracks 17c musketeersco protection +1 (lvl 6) | 6 | 1 | 15.62 | 6300 | 0 | 0 | 360 | 0 | 0 |
| `scobar.musketeersco.2.6` | Barracks 17c musketeersco protection +2 (lvl 7) | 7 | 2 | 15.62 | 13125 | 0 | 0 | 750 | 0 | 0 |
| `scobar.officersco.1.1` | Barracks 17c officersco damage +30 (lvl 2) | 2 | 30 | 15.62 | 250 | 0 | 0 | 75 | 0 | 0 |
| `scobar.officersco.2.1` | Barracks 17c officersco protection +10 (lvl 2) | 2 | 10 | 15.62 | 1550 | 0 | 0 | 425 | 0 | 0 |
| `scobar.pikemansco.1.1` | Barracks 17c pikemansco damage +1 (lvl 2) | 2 | 1 | 15.62 | 250 | 0 | 0 | 70 | 0 | 0 |
| `scobar.pikemansco.1.2` | Barracks 17c pikemansco damage +2 (lvl 3) | 3 | 2 | 15.62 | 750 | 0 | 0 | 210 | 0 | 0 |
| `scobar.pikemansco.1.3` | Barracks 17c pikemansco damage +3 (lvl 4) | 4 | 3 | 15.62 | 2800 | 0 | 0 | 790 | 0 | 0 |
| `scobar.pikemansco.1.4` | Barracks 17c pikemansco damage +1 (lvl 5) | 5 | 1 | 15.62 | 6000 | 0 | 0 | 750 | 0 | 0 |
| `scobar.pikemansco.1.5` | Barracks 17c pikemansco damage +2 (lvl 6) | 6 | 2 | 15.62 | 10800 | 0 | 0 | 1350 | 0 | 0 |
| `scobar.pikemansco.1.6` | — | 7 | 3 | 15.62 | 22500 | 0 | 0 | 2800 | 0 | 0 |
| `scobar.pikemansco.2.1` | Barracks 17c pikemansco protection +1 (lvl 2) | 2 | 1 | 15.62 | 150 | 0 | 0 | 60 | 0 | 0 |
| `scobar.pikemansco.2.2` | Barracks 17c pikemansco protection +2 (lvl 3) | 3 | 2 | 15.62 | 450 | 0 | 0 | 180 | 0 | 0 |
| `scobar.pikemansco.2.3` | Barracks 17c pikemansco protection +3 (lvl 4) | 4 | 3 | 15.62 | 1690 | 0 | 0 | 675 | 0 | 0 |
| `scobar.pikemansco.2.4` | Barracks 17c pikemansco protection +1 (lvl 5) | 5 | 1 | 15.62 | 4500 | 0 | 0 | 600 | 0 | 0 |
| `scobar.pikemansco.2.5` | Barracks 17c pikemansco protection +2 (lvl 6) | 6 | 2 | 15.62 | 8100 | 0 | 0 | 1080 | 0 | 0 |
| `scobar.pikemansco.2.6` | — | 7 | 3 | 15.62 | 16875 | 0 | 0 | 2250 | 0 | 0 |
| `scobla.1` | Manufacture agricultural equipment (field capacity +100%) | 1 | 100 | 15.62 | 0 | 400 | 0 | 90 | 0 | 0 |
| `scobla.2` | Forge metal armature and gratings (building defence +50) | 1 | 50 | 15.62 | 0 | 0 | 12320 | 350 | 900 | 0 |
| `scobla.3` | Forge harnesses for horses (mounted units recruitment speed -33%) | 1 | -3333333 | 15.62 | 0 | 0 | 0 | 3650 | 5300 | 8200 |
| `scobla.4` | Forge bayonets and broadswords for infantry (18c musketeer/grenadier melee attack +5) | 1 | 5 | 15.62 | 0 | 1300 | 0 | 1500 | 900 | 5000 |
| `scobla.5` | Forge new types of broadswords and sabres (cavalry and sword clansman attack +5) | 1 | 5 | 15.62 | 0 | 0 | 0 | 4000 | 7900 | 0 |
| `scobla.6` | Forge new cuirasses (armoured soldiers defence +2) | 1 | 2 | 15.62 | 0 | 0 | 0 | 4950 | 10500 | 0 |
| `scocen.1` | — | 1 | 0 | 9.38 | 30000 | 0 | 0 | 5000 | 2000 | 2000 |
| `scosta.lancersco.2.1` | Stable lancersco protection +1 (lvl 2) | 2 | 1 | 15.62 | 4000 | 0 | 0 | 1350 | 0 | 0 |
| `scosta.lancersco.2.2` | Stable lancersco protection +1 (lvl 3) | 3 | 1 | 15.62 | 3500 | 0 | 0 | 2100 | 0 | 0 |
| `scosta.lancersco.2.3` | Stable lancersco protection +2 (lvl 4) | 4 | 2 | 15.62 | 8000 | 0 | 0 | 3300 | 0 | 0 |
| `scosta.lancersco.2.4` | Stable lancersco protection +3 (lvl 5) | 5 | 3 | 15.62 | 14500 | 0 | 0 | 4400 | 0 | 0 |
| `scosta.lancersco.2.5` | Stable lancersco protection +3 (lvl 6) | 6 | 3 | 15.62 | 22600 | 0 | 0 | 5500 | 0 | 0 |
| `scosta.lancersco.2.6` | Stable lancersco protection +2 (lvl 7) | 7 | 2 | 15.62 | 30000 | 0 | 0 | 6000 | 0 | 0 |
| `scosta.raidersco.2.1` | Stable raidersco protection +1 (lvl 2) | 2 | 1 | 15.62 | 500 | 0 | 0 | 50 | 0 | 0 |
| `scosta.raidersco.2.2` | Stable raidersco protection +2 (lvl 3) | 3 | 2 | 15.62 | 1500 | 0 | 0 | 150 | 0 | 0 |
| `scosta.raidersco.2.3` | Stable raidersco protection +2 (lvl 4) | 4 | 2 | 15.62 | 5625 | 0 | 0 | 560 | 0 | 0 |
| `scosta.raidersco.2.4` | Stable raidersco protection +2 (lvl 5) | 5 | 2 | 15.62 | 16200 | 0 | 0 | 1080 | 0 | 0 |
| `scosta.raidersco.2.5` | Stable raidersco protection +2 (lvl 6) | 6 | 2 | 15.62 | 16200 | 0 | 0 | 1080 | 0 | 0 |
| `scosta.raidersco.2.6` | Stable raidersco protection +1 (lvl 7) | 7 | 1 | 15.62 | 15000 | 0 | 0 | 750 | 0 | 0 |
| `ukrwwa.1` | — | 2 | 5 | 0.03 | 0 | 400 | 0 | 0 | 0 | 0 |

## 8. Дыры в данных и оговорки

### Unit sids referenced in nation rosters but not extracted from unit.script

- Кол-во: 0

### Per-unit blacksmith/stable/barracks upgrades (resolved)

- Кол-во: 0

### Известные ограничения парсера

- **Per-unit blacksmith / stable / barracks апгрейды:** symbolic-симулятор в `parser/simulate_upgrades.py` теперь раскрывает их полностью — извлекает cost, time, value для каждого `<nat><place>.<unit>.<itype>.<level>`. См. лист `Upgrades` в xlsx или [секцию 7 этого md](#7-апгрейды) — ~4000 строк апгрейдов с полными данными.
- **Override-механика апгрейдов:** некоторые апгрейды нация-специфично патчатся через `_country_ModifyUpgrade(country, ind-1, …)`. Симулятор отслеживает последний emit и накладывает патч. Если значение неожиданно — проверяй соседние строки в скрипте.
- **AI-метаданные** (`aiforce`, `bstandground`, `bturnoff` и т. д.) опущены — это тюнинг для AI-бота, не игрового баланса.
- **State-machine скрипты** (в `data/scripts/units/*.inc`) не парсятся — они описывают анимации / триггеры, а не статы.
- **Странные значения `value`:** некоторые апгрейды имеют `value = -7500000` или `value = -30` — это сырые числа из `_country_AddUpgrade`, представляют разные шкалы (множители времени, проценты со знаком). Смотри `gc_upg_type_*` в `dmscript.global` для расшифровки шкалы.

---

Сгенерировано из файлов игры. Перепарсить можно, запустив:

```
python parser/build_data.py     # обновляет output/data.json
python writers/write_xlsx.py    # обновляет xlsx
python writers/write_md.py      # обновляет этот md
```