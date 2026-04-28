# Cossacks 3 — Шаг 1. Разведка

## 1. Структура папки игры

`C:\Program Files (x86)\Steam\steamapps\common\Cossacks 3\`

```
data/
├── locale/{cs,de,en,es,fr,it,pl,po,ru,tu,uk}/
│   ├── units.txt    # имена юнитов и зданий (шаблоны %nat% %com%)
│   ├── upgrades.txt # имена апгрейдов с эффектами
│   └── gui.txt      # элементы интерфейса
└── scripts/
    ├── dmscript.global   # глобальные константы gc_*
    ├── dmscript.source   # порядок загрузки .script файлов
    ├── lib/              # все игровые правила
    │   ├── unit.script        ← 560 KB — главный файл, юниты + здания
    │   ├── country.script     ← 355 KB — нации, ростер, апгрейды
    │   ├── classes.script     ← 256 KB — структуры (TObjBase, TPlayer и т.п.)
    │   ├── player.script      ← 145 KB — состояние игрока, eff = 100 default
    │   ├── weapon.script      ← 69  KB — снаряды (TWeapon)
    │   └── … (и ещё ~25 файлов: AI, GUI, scenario)
    └── units/, common.inc/, env/, misc/, progress/  # state machines
dlcs/{summer,winter}/data/maps/   # ТОЛЬКО карты, никаких правил
```

DLC summer/winter содержат только карты — вся боевая/экономическая математика игры в одном месте.

## 2. Ключевая константа: `gc_time_to_frames = 32`

Все времена в скриптах хранятся **в кадрах** (32 кадра = 1 игровая секунда). Поэтому `buildtime = 144` означает 144/32 = **4.5 сек**, а `pause = 64` (между выстрелами) = 2 сек.

Скорости игры (`dmscript.global:1025-1029`):
| Speed | Тиков в сек |
|-------|-------------|
| 0     | 7           |
| 1     | 10 (default)|
| 2     | 14          |

## 3. Список наций

Из `country.script:7-41` — **24 кода нации**, **21 играбельная**:

| ID | sid | Имя (locale) | Кластер commonsid | Кластер пехоты |
|----|-----|--------------|--------------------|------------------|
| 0  | aus | Австрия      | eur | peaaus |
| 1  | fra | Франция      | eur | peaeng |
| 2  | eng | Англия       | eur | peaeng |
| 3  | spa | Испания      | spa | peaspa |
| 4  | rus | Россия       | rus | pearus |
| 5  | ukr | Украина      | ukr | peaukr |
| 6  | pol | Польша       | eur | peapol |
| 7  | swe | Швеция       | eur | peaeng |
| 8  | pru | Пруссия      | eur | peaaus |
| 9  | ven | Венеция      | eur | peaspa |
| 10 | tur | Турция       | tur | peatur |
| 11 | alg | Алжир        | tur | peatur |
| 12 | mis | (Originals/editor) | — | — |  ← НЕИГРАБЕЛЬНАЯ |
| 13 | net | Нидерланды   | eur | peaeng |
| 14 | den | Дания        | eur | peaeng |
| 15 | por | Португалия   | por | peaspa |
| 16 | pie | Пьемонт      | eur | peaspa |
| 17 | sax | Саксония     | eur | peaaus |
| 18 | bav | Бавария      | eur | peaaus |
| 19 | hun | Венгрия      | eur | peapol |
| 20 | swi | Швейцария    | eur | peaaus |
| 21 | sco | Шотландия    | eur | peasco |
| 22 | tat | (нет в локали)     | — | — | ← НЕИГРАБЕЛЬНАЯ |
| 23 | lit | (нет в локали)     | — | — | ← НЕИГРАБЕЛЬНАЯ |

Cluster commonsid восстановлен по `for i:=0..5 commonsid := eur/rus/tur/spa/ukr/por` в `unit.script:2113-2138`.

## 4. Структура определения юнита/здания

### Юниты — литеральный case в `unit.script:_unit_InitBase`

```pascal
case objprop.sid of
  'pikeman','pikemanpol','pikemantur','pikemanrus',
  'pikemansco','pikemanpor','pikemanspa','pikemanswi' : begin
    objbase.maxhp := 90;
    SetObjBaseWeapon(objprop, objbase, 0, 8, 0, 35, 100, 0, 100000,
                     gc_obj_weapon_kind_pike, True);
    SetObjBasePrice(objbase, 25, 0, 0, 3, 20, 0);
    SetObjBaseProtection(objbase, 3, 2, 4, 210, 6, 40);
    SetObjBaseSearchBuildVisionScore(objprop, objbase, 700, 144, 1, 10);
    objprop.usage := gc_obj_usage_lightinfantry;
    case nation of
      'pol': begin
        objbase.maxhp := 90;
        SetObjBasePrice(objbase, 25, 0, 0, 1, 0, 0);  // дешевле, без железа
        SetObjBaseProtection(objbase, 0, 0, 0, 0, 0, 0);
        SetObjBaseSearchBuildVisionScore(objprop, objbase, default, 96, default, default);
      end;
      'tur','alg': begin
        objbase.maxhp := 95;  …
      end;
      …
    end;
  end;
  'pikeman18','pikeman18swe' : begin … end;
  'lightinfantry','lightinfantrydip' : begin … end;
  …
end;
```

`default = -1` означает «не трогать» (унаследовать значение из общего блока выше). Парсер должен это уважать.

### Здания — генеративный case в том же `_unit_InitBase`

```pascal
for i:=0 to 5 do begin
   var commonsid : String;
   case i of
     0: commonsid := 'eur';   // Aus, Fra, Eng, Swe, Pru, Ven, Den, Net, Sax, Bav, Hun, Swi, Pie, Pol, Sco
     1: commonsid := 'rus';   // Rus
     2: commonsid := 'tur';   // Tur, Alg
     3: commonsid := 'spa';   // Spa
     4: commonsid := 'ukr';   // Ukr
     5: commonsid := 'por';   // Por
   end;
   case objprop.sid of
     commonsid+'mil': …  // мельница
     commonsid+'sto': …  // склад
     commonsid+'mar': …  // рынок
     …
   end;
end;
```

Так получаются sid вида `eurmil`, `rusmil`, `turmil`, `spamil`, `ukrmil`, `pormil` — **6 экземпляров мельницы**, по одному на кластер.

### Per-nation здания (с реальным префиксом нации)

В отличие от common, они дискретны: `auscen` (Austrian Town Hall), `frabar` (French Barracks), `rustem` (Russian Cathedral), и т.д.

## 5. Полная схема sid-суффиксов

### Общие здания (commonsid + suffix)
| Suffix | Здание (RU) | Loc EN |
|--------|-------------|--------|
| coa    | Угольная шахта | Mine (coal) |
| gol    | Золотая шахта  | Mine (gold) |
| iro    | Железная шахта | Mine (iron) |
| mar    | Рынок          | Market |
| mil    | Мельница       | Mill |
| sto    | Склад          | Storehouse |
| por    | Порт/Верфь     | Shipyard |
| sga    | Каменные ворота | Stone Gate |
| swa    | Каменная стена | Stone Wall |
| tow    | Башня          | Tower |
| wga    | Деревянные ворота | Wood Gate |
| wwa    | Палисад        | Palisade |

### Per-nation здания (`<nat>` + suffix)
| Suffix | Здание (RU) | Loc EN |
|--------|-------------|--------|
| aca    | Академия    | Academy |
| art    | Артиллерийское депо | Artillery Depot |
| bar    | Казарма XVII в. | Barracks 17th |
| ba2    | Казарма XVIII в. | Barracks 18th |
| bla    | Кузница     | Blacksmith |
| cen    | Ратуша      | Town Hall |
| dip    | Дип. центр  | Diplomatic Center |
| hou    | Жильё       | Housing/Dwelling |
| sta    | Конюшня     | Stable |
| tem    | Собор       | Cathedral |

## 6. Глобальные константы (`dmscript.global`)

### Ресурсы (799-808)
```
gc_resource_hitsneeded_food  = 22   ← ВНИМАНИЕ: в твоём промпте было 30
gc_resource_hitsneeded_wood  = 14
gc_resource_hitsneeded_stone = 20

gc_obj_resource_portion_food  = 45  ← совпадает с твоим
gc_obj_resource_portion_wood  = 28
gc_obj_resource_portion_stone = 40  ← совпадает
gc_obj_foodperunit            = 30  ← упкип крестьянина
```

Для остальных ресурсов (gold/iron/coal) базовая порция = **20** (`unit.script:9551`).

### Лимиты
```
gc_MaxObjCount    = 32000
gc_MaxPlayerCount = 12
gc_MaxCountryCount = 24
gc_MaxKeyColorCount = 24
gc_FieldMaxHP     = 25000     ← общий «HP» поля для жатвы
```

### Время
```
gc_time_to_frames           = 32
gc_settings_gamespeed_0     = 7
gc_settings_gamespeed_1     = 10  (default)
gc_settings_gamespeed_2     = 14
gc_BuildingSlowDeathHP      = 1999
gc_BuildingSlowDeathRandom  = 300
gc_BuildingSlowDeathSpeed   = 90
```

## 7. Формула добычи (подтверждена кодом)

`unit.script:9555-9561`:
```
function _unit_GetPeasantAddResToPlayerAmountByIndex(plInd, cid, restype) : Integer;
begin
   var eff : Integer = gPlayer[plInd].resefficiency[cid][restype];
   Result := ((_unit_GetPeasantResPortion(restype) * eff) div 100);
end;
```

`eff` инициализируется = 100 в `player.script:109`, апгрейды складывают свои значения **аддитивно** (`player.script:1813-1828`):
```pascal
gPlayer[plInd].resefficiency[cid][gc_resource_type_food]
  := gPlayer[plInd].resefficiency[cid][gc_resource_type_food] + round(value);
```

Расхождение с промптом по `hitsneeded_food`: в файле **22**, не 30. Это влияет на расчётную скорость еды (короче рейс ⇒ выше DPS).

## 8. Население

`objprop.farm := X` поднимает лимит на X при постройке (`unit.script:3805: gPlayer[pl].farm := gPlayer[pl].farm+TObjProp(pobjprop).farm`). Подтверждённые значения из выборочного просмотра вокруг строк 2370-2500: 25, 50, 75, 100, 150, 200, 250 — что согласуется с твоими «Town Hall +100, Dwelling +15, Барак 17в +150, Барак 18в +250», но точные привязки к sid нужно тащить парсером.

## 9. Локализация

- `data/locale/<lang>/units.txt` — формат:
  ```
  	@<key>
  Display name
  	@<key>.ext
  Tooltip lines (с %def% %pos% %neg% префиксами стиля)
  ```
- Шаблоны:
  - `%nat%` → префикс нации (aus/fra/…/sco)
  - `%com%` → префикс кластера (eur/rus/tur/spa/ukr/por)
  - `%include(file;key)%` → подстановка
  - `%farm%` → значение `objprop.farm` для этого здания
- 12 языков: cs, de, en, es, fr, it, pl, po, ru, tu, uk + en. Парсить буду `en` (как primary) и `ru` (как fallback / справка).

## 10. Апгрейды

`country.script:_country_AddUpgradeWithAccessControl` (л. 920) и аналоги — 136 вызовов добавления апгрейда, 168 вызовов `_country_AddMember`. Параметры апгрейда:
```
upgid (e.g. 'bla.pikeman.1.5')
level, tooltiptype, itype, value
enabled, time, x, y
food, wood, stone, gold, iron, coal
iarr1p[0..2], sarr2p[0..9]      # доп. параметры
req[0..7]                        # пред-условия
```

Имя апгрейда строится как `<place>.<member>.<itype>.<level>`:
- `bla.<unit>.1.<lvl>` — кузница, damage, ур. 2..6
- `bla.<unit>.2.<lvl>` — кузница, protection, ур. 2..6
- `aca.<N>` — академия (см. `upgrades.txt` для 28+ исследований)
- `mil.<N>` — мельница

В `upgrades.txt` всего 165 строк — это означает ~80 уникальных апгрейд-ключей.

## 11. Отдельные счётчики

| Что | Кол-во вызовов | Файл |
|-----|----------------|------|
| `SetObjBuildingProperties / Ext` | **105** | unit.script |
| `_country_AddMember(country, …)` | **168** | country.script |
| `_country_AddUpgrade*(country, …)` | **136** | country.script |
| Нации в `_country_GetSIDByID` | 24 (21 играбельных) | country.script |
| Уникальных строк юнита (case branches) | ~32 групп (каждая = до 8 nation override) | unit.script |
| Common building suffixes | 12 (10 в case + wga/wwa в локали) | unit.script |
| Per-nation building suffixes | 10 | locale |

## 12. Что я УЖЕ НАШЁЛ vs твоих «известных фактов»

| Факт из промпта | В файле | Статус |
|-----------------|---------|--------|
| Eff default = 100 | `player.script:109 → 100` | ✅ совпало |
| Апгрейды складываются аддитивно | `player.script:1813+` подтверждает | ✅ |
| Базовая порция еды = 45 | `gc_obj_resource_portion_food = 45` | ✅ |
| Порция камня = 40 | `gc_obj_resource_portion_stone = 40` | ✅ |
| Порция дерева = 28 | `gc_obj_resource_portion_wood = 28` (в промпте не указано — добавится в ref) | новый |
| Порция др. ресурсов = 20 | `unit.script:9551 → 20` | ✅ |
| Hits needed food = 30 | **22** в файле | ❌ РАСХОЖДЕНИЕ |
| Hits needed wood = ? | 14 | новый факт |
| Hits needed stone = ? | 20 | новый факт |
| 350 кадров за 7 сек камня | при `gc_time_to_frames=32` 350 кадров = 10.94 сек ⁂ | ⚠️ нужна проверка с учётом game speed |
| 21 нация | подтверждено (24 кода, 21 в локали) | ✅ |

⁂ Возможно «350 кадров» считалось при другом gamespeed (14 t/s ⇒ 350/14 ≈ 25 сек?) — пересчитаем после полного парсинга, когда будет реальный buildtime/pause анимации экстракции.

## 13. План на Шаг 2 (на одобрение)

Напишу `parser/parse.py`, который:
1. Загружает `dmscript.global` → константы (regex `^\s*(gc_\w+)\s*=\s*(.+);`).
2. Загружает `unit.script`:
   - Находит `_unit_InitBase` блок, идёт по `case objprop.sid of … else bCheckBuilding := True; end;` — это юниты.
   - Внутри каждой ветки парсит `SetObjBaseWeapon`, `SetObjBasePrice`, `SetObjBaseProtection`, `SetObjBaseSearchBuildVisionScore`, `SetObjBaseMaterialCanKill`, плюс прямые `objbase.*`/`objprop.*` присваивания.
   - Для `case nation of 'pol': … end;` — фиксирует override-блоки и применяет их поверх базы.
   - Парсит здания через ту же логику, плюс разворачивает `commonsid+'XYZ'` × 6 кластеров.
3. Загружает `country.script`:
   - `_country_Init` для каждого `cid` — определяет, какие sid доступны (`_country_AddMember` + флаги наций `aus, fra, …, sco`).
   - Парсит все `_country_AddUpgrade*` → таблица апгрейдов.
4. Загружает `locale/en/units.txt` + `upgrades.txt` → словарь sid→display name.
5. Подставляет `%nat%`/`%com%` для каждой нации.
6. Складывает данные в pandas DataFrames, потом → `output/cossacks3_reference.xlsx` (8 листов) + `output/cossacks3_reference.md`.

Скрипт идемпотентный, входные пути в `parser/config.py`. Парсер на Python 3 + `openpyxl` или `xlsxwriter`, `pandas` опционален.

**Сложность:** Pascal-подобный синтаксис со вложенными `begin/end`, со скобочной аккуратностью. Буду парсить через **строгий статусный парсер** (стек блоков begin/end), а не regex по всему файлу.

**Что заложу в `Gaps`:** AI-overrides, скрипты state machines (units.inc), сложные требования (`req[0..7]`), опциональные параметры с `default`/-1 (буду сохранять как «inherit»).
