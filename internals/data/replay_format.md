# Replay / Save (`.rep`, `.map`) — формат `OSWMap13`

Cossacks 3 пишет реплеи и save-файлы в одном формате `OSWMap13`. По
сути файл — это **снимок мира на старте + поток net-пакетов**, тот
же поток, который сервер рассылает клиентам в онлайн-игре (см.
[`../engine/server_sync_architecture.md`](../engine/server_sync_architecture.md)).

Воспроизведение реплея в exe реализовано через клиентский кодовый
путь сетевой игры: каждый "package" из ленты разбирается тем же
`Read*`-handler'ом, который сработал бы у online-клиента при получении
этого пакета по сети. Сервер в replay-режиме ничего не просчитывает
(см. `progress.inc:46`: `if (_net_IsClient or _net_IsReplay) then //
global do not progress`).

Парсер: [`parser/parse_replay_events.py`](../../parser/parse_replay_events.py)
(decoded JSON timeline), [`parser/parse_replay.py`](../../parser/parse_replay.py)
(header + pattern counts).

Тестовый файл по которому всё это валидировалось:
`nick-niotid 2.rep`, ≈5.36 MB, build 92, gamespeed=Fast.

---

## 1. Общая разметка файла

```
+--- Header (~168 KB) -------------------------------------+
| OSWMap13 + Build.Ver[X.Y.Z.NNNN] + UID                   |
| GameMapSnapShotBegin                                     |
|   [BMP, ~145 KB — превью карты]                          |
| GameMapSnapShotEnd                                       |
| GameMapRecordBegin                                       |
|   <key,value> пары в текстовом формате                   |
|     maskname, mapsize, relieftype, randkey0, randkey1,   |
|     terraintype, season, gamespeed, resourcemines,       |
|     limit, ver, ...   (951 пара в nick-niotid 2.rep)     |
+--- Body (~5 МБ) ---------------------------------------- +
| Поток entry'ев с timestamp'ом и net-payload              |
|   entry[0]: ts=0, payload=снапшот стартового мира        |
|   entry[1]: ts=14.13 (ticks), payload=первый net-пакет   |
|   ...                                                    |
|   entry[N]: ts=12152.3, последний пакет                  |
| GameMapRecordEnd                                         |
+----------------------------------------------------------+
| Хвост (~360 байт): пара финальных kv                     |
+----------------------------------------------------------+
```

В `nick-niotid 2.rep`: **33 256 entry**, расширяющихся в
**42 859 sub-package'ей** (один entry содержит ≥1 sub-package).

---

## 2. Entry: 18-байтовый заголовок + payload

```
offset  size  поле                                    замечание
---------------------------------------------------------------------
+0      4B    float ts                                ticks (0.1 g-сек/tick)
+4      4B    u32 payload_size LE                     размер payload
+8      10B   const "b0 04 00 00 00 00 00 00 00 00"   entry-маркер
+18     N     payload                                  N = payload_size
```

### 2.1 Семантика `ts`

**`ts` в repреплее — это движковые ticks с шагом 0.1 g-сек.**
То есть `g_sec = ts / 10`.

Эмпирическая проверка по `nick-niotid 2.rep`:

| событие                | ts (raw) | g_sec | user-recall          |
|------------------------|---------:|------:|----------------------|
| Постройка TC `auscen`  |    33.3  |  3.3  | мгновенно после старта|
| Постройка рынка `eurmar`|   288.6  | 28.9  | «на 30-й секунде» ✓  |
| Конец игры             |  12152.3 |1215.2 | ≈20 минут            |

Почему 0.1 g-сек/tick: при любом lobby-`gamespeed` соотношение
`ticks_per_real_sec / game_factor` всегда равно 10:

| `gamespeed` | `gc_settings_gamespeed_N` (ticks/real-sec) | factor | g-sec/tick |
|-------------|:------------------------------------------:|:------:|:----------:|
| Slow        | 7                                          | 0.7    | 0.1        |
| Normal      | 10                                         | 1.0    | 0.1        |
| Fast        | 14                                         | 1.4    | 0.1        |

Float-значения `ts` дробные (14.130, не 14.1) — движок пишет
`GetCurrentTime × GetTimeSpeedFactor` с полной float-precision.

### 2.2 10-байт entry-маркер

Все 33 256 entry в исследованном файле имеют **одинаковый** маркер
`b0 04 00 00 00 00 00 00 00 00`. Значит весь поток ходит по одному
каналу (см. §6). Точный смысл этих 10 байт пока не разобран —
вероятнее всего `u16 0x04b0 = 1200` — channel-id, а 8 нулей — резерв.

---

## 3. Sub-package: внутренняя структура payload'а

Один entry содержит 1+ sub-package'ей (см. native
`RecordPackagesCount`/`RecordPackagesCursor`). Каждый sub-package
пишется на write-стороне парой `RecordCustomBegin(stateName) /
RecordCustomEnd`, на read-стороне диспатчится через
`SwitchTo(stateName)`.

### 3.1 Class=0x00 (клиентские команды + engine events) — формат

```
offset  size  поле                                    замечание
---------------------------------------------------------------------
+0      4B    [class=0x00, sub=0x03, pid, state_id]   4-байтовый header
+4      1B    0x00                                    begin-marker
+5      ?B    typed body                              RecordCustomWrite* sequence
+?      1B    0x01                                    end-marker
```

**Verified эмпирически:** ReadConstruct (auscen build) парсится
байт-в-байт с этой схемой; trailing end-marker = `0x01` присутствует
в 100% (89/89) ReadConstruct, ReadNew, ReadRally, ReadOrder,
ReadProduce, ReadApply событий.

**Pid mapping** (из `dmscript.global`):

| pid | роль                          |
|-----|-------------------------------|
| 0..11 | реальные игроки (`gc_MaxPlayerCount = 12`) |
| 12  | `gc_playerind_env`            |
| 13  | `gc_playerind_misc`           |
| 14  | `gc_playerind_progress` — engine progress events |
| 15  | `gc_playerind_pool`           |

### 3.2 Class=0x09 (TagObject state-sync stream) — формат

Это **отдельный binary-формат**, не использующий sub-package header
из §3.1. Похоже на канал `RecordCustomBeginTagObject`.

```
offset  size  поле
------------------------------------------------------
+0      1B    0x09                       — class
+1      3B    u24 LE — global sequence counter (монотонно растёт от 0)
+4      4B    u32 LE — count записей
+8      ?B    count записей с переменным размером
```

**Записи имеют переменный размер**, 8..23 байта, шаг ~3 байта.
В `nick-niotid 2.rep` распределение размеров (для events где
`(payload_size − 8) % count == 0`):

| record bytes | events | расшифровка                          |
|-------------:|-------:|--------------------------------------|
| 8            | 2199   | `[u32 uid][u32 statestag]` — minimum |
| 11           |  727   |  + 3B (Int24?)                       |
| 12           |  610   |  + 4B (Int/Float?)                   |
| 14           |  578   |                                      |
| 16           | 1806   | `[u32 uid][u32 statestag][2*Float pos]` |
| 19           | 2767   | `[u32 uid][u32 statestag][Int24][2*Float pos]` (verified for ReadConstruct trail) |
| 20           | 2802   | + 4B extra                           |
| 23           |  375   |                                      |

Точный variable-length формат каждой записи зависит от **state-tag
flags** на текущем объекте — TagObject пишет ровно те поля, что
изменились (position если двигался, hp если ранен, и т.д.). Без
disasm движка точная схема не разобрана.

Это **74% всех sub-package'ей** (27 313 / 42 859 в `nick-niotid 2.rep`).
Эти записи — server-сток state-tag'ов для каждого юнита
(см. [`../engine/server_sync_architecture.md`](../engine/server_sync_architecture.md)).

### 3.3 Типизированные RecordCustomRead*-примитивы

```
RecordCustomReadBoolean  — 1 байт
RecordCustomReadByte     — 1 байт
RecordCustomReadWord     — 2 байта LE
RecordCustomReadSmallInt — 2 байта LE signed
RecordCustomReadInt24    — 3 байта LE signed
RecordCustomReadInteger  — 4 байта LE signed
RecordCustomReadFloat    — 4 байта LE IEEE-754
RecordCustomReadString   — [u16 len LE][bytes ASCII/cp1251]
RecordCustomReadShortString — [u8 len][bytes]   (см. §3.4)
RecordCustomReadPackedFloat — float в фиксированном диапазоне (TBD: format)
RecordCustomReadBit + RecordCustomBeginReadBitFields — для bit-stream'ов
```

### 3.4 String — пример

`String` — это просто `[u16 len LE][bytes]`. Никакого префикса.
Например для `ReadConstruct` с sid="auscen" в payload встречается:

```
06 00       u16 = 6
61 75 73 63 65 6e   "auscen"
```

Раньше документ говорил про загадочный 0x00-byte перед строкой —
это была ошибка в моей разметке: байт `0x00` это **begin-marker
sub-package'а** из §3.1, а не часть String.

---

## 4. Карта `state_id` → handler — ПОЛНАЯ

**Источник правды:** [`data/scripts/units/global.aix`](C:\Program Files (x86)\Steam\steamapps\common\Cossacks 3\data\scripts\units\global.aix) — там описаны все sections
в порядке загрузки. **`state_id = индекс секции`** (включая разделители
`---SEP---` и `section.end`).

| state_id | section name           | decoder        | примечание                           |
|---------:|------------------------|----------------|--------------------------------------|
| `0x00`   | `Initial`              | —              | начальное состояние FSM             |
| `0x01`   | `OnBeforeSave`         | —              |                                      |
| `0x02`   | `OnAfterLoad`          | —              |                                      |
| `0x03`   | `Progress`             | —              | per-player progress tick            |
| `0x04`   | _SEPARATOR_            | —              |                                      |
| `0x05`   | `WriteSquadNew`        | —              |                                      |
| `0x06`   | `ReadSquadNew`         | TODO           | формация: создание                  |
| `0x07`   | `WriteSquadListAction` | —              |                                      |
| `0x08`   | `ReadSquadListAction`  | (engine-only)  | **engine пишет 5629×** от pid=14   |
| `0x09`   | _SEPARATOR_            | —              |                                      |
| `0x0a`   | `WriteMove`            | (engine-only)  | engine broadcasts moves (44× от pid=14) |
| `0x0b`   | **`ReadMove`** ✓        | `decode_move`  | per-unit destination + facing       |
| `0x0c`   | `WriteNew`             | —              |                                      |
| `0x0d`   | **`ReadNew`** ✓         | `decode_new`   | спавн юнита от сервера              |
| `0x0e`   | `WriteFree`            | —              |                                      |
| `0x0f`   | **`ReadFree`** ✓        | `decode_free`  | удаление объекта; **engine 5929×** от pid=14 |
| `0x10`   | `WriteDeath`           | —              |                                      |
| `0x11`   | **`ReadDeath`** ✓       | `decode_death` | смерть юнита (RNG seed restore)     |
| `0x12`   | `WritePlayer`          | —              |                                      |
| `0x13`   | **`ReadPlayer`** ✓      | `decode_player`| захват/передача владельца            |
| `0x14`   | `WriteRally`           | —              |                                      |
| `0x15`   | **`ReadRally`** ✓       | `decode_rally` | rally-point на здании                |
| `0x16`   | `WriteOrder`           | —              |                                      |
| `0x17`   | **`ReadOrder`** ✓       | `decode_order` | основные приказы (build/gainres/...)|
| `0x18`   | `WriteUpgrade`         | —              |                                      |
| `0x19`   | **`ReadUpgrade`** ✓     | `decode_upgrade`| start/cancel research                |
| `0x1a`   | `WriteProduce`         | —              |                                      |
| `0x1b`   | **`ReadProduce`** ✓     | `decode_produce`| queue unit (amount=-1=infinite)      |
| `0x1c`   | `WriteSearch`          | —              |                                      |
| `0x1d`   | **`ReadSearch`** ✓      | `decode_search`| search-enemy toggle                  |
| `0x1e`   | `WriteStand`           | —              |                                      |
| `0x1f`   | **`ReadStand`** ✓       | `decode_stand` | stand-ground toggle                  |
| `0x20`   | `WriteConstruct`       | —              |                                      |
| `0x21`   | **`ReadConstruct`** ✓   | `decode_construct`| build building                    |
| `0x22`   | `WriteApply`           | —              |                                      |
| `0x23`   | **`ReadApply`** ✓       | `decode_apply` | apply finished upgrade               |
| `0x24`   | `WriteLeaveOrder`      | —              |                                      |
| `0x25`   | **`ReadLeaveOrder`** ✓  | `decode_leaveorder`| list of units leaving           |
| `0x26`   | `WriteLeave`           | —              |                                      |
| `0x27`   | **`ReadLeave`** ✓       | `decode_leave` | unit goes outside                    |
| `0x28`   | `WriteProj`            | —              |                                      |
| `0x29`   | **`ReadProj`** ✓        | `decode_proj`  | projectile fired (61B fixed body)    |
| `0x2a`   | `WriteProjFree`        | —              |                                      |
| `0x2b`   | **`ReadProjFree`** ✓    | `decode_projfree`| projectile destroyed               |
| `0x2c`   | `WriteNewP`            | —              |                                      |
| `0x2d`   | **`ReadNewP`** ✓        | `decode_newp`  | spawn primitive (fields/balloons)    |
| `0x2e`   | `WriteStop`            | —              |                                      |
| `0x2f`   | **`ReadStop`** ✓        | `decode_stop`  | cancel orders                        |
| `0x30`   | `WriteTrade`           | —              |                                      |
| `0x31`   | **`ReadTrade`** ✓       | `decode_trade` | market trade                         |
| `0x32`   | `WriteWall`            | —              |                                      |
| `0x33`   | **`ReadWall`** ✓        | `decode_wall`  | wall cluster (per-cell records)      |
| `0x34`   | `WriteGate`            | —              |                                      |
| `0x35`   | **`ReadGate`** ✓        | `decode_gate`  | open/close gates                     |
| `0x36`   | `WriteFreeList`        | —              |                                      |
| `0x37`   | **`ReadFreeList`** ✓    | `decode_freelist`| mass-delete (end-game cleanup)    |
| `0x38`   | `WritePeaceTime`       | —              |                                      |
| `0x39`   | **`ReadPeaceTime`** ✓   | `decode_peacetime`| peace mode toggle                |
| `0x3a`   | `WriteSync`            | —              |                                      |
| `0x3b`   | `ReadSync`             | TODO           | full unit-snapshot sync (rare)       |
| `0x3c`   | `WriteSyncUnitsParams` | —              |                                      |
| `0x3d`   | **`ReadSyncUnitsParams`** ✓ | `decode_sync_units_params`| HP sync       |
| `0x3e`   | _SEPARATOR_            | —              |                                      |
| `0x3f`   | `WritePackage`         | —              |                                      |
| `0x40`   | **`ReadPackage`** ✓     | `decode_package`| text net-message                    |
| `0x41`   | _SEPARATOR_            | —              |                                      |
| `0x42`   | `ProgressAI`           | —              | engine internal                      |
| `0x43`   | `ProgressEconomicAI`   | —              | engine internal                      |
| `0x44`   | `ProgressWarAI`        | —              | engine internal                      |
| `0x45`   | `CheckErrors`          | —              | engine internal                      |
| `0x46`   | **`ReadTradeResources`** ✓ | `decode_traderesources`| ally transfer                |
| `0x47`   | `WriteTradeResources`  | —              |                                      |

**Итого декодированных handler'ов: 21** (`ReadConstruct`, `ReadNew`,
`ReadRally`, `ReadOrder`, `ReadProduce`, `ReadApply`, `ReadDeath`,
`ReadUpgrade`, `ReadTrade`, `ReadLeave`, `ReadPlayer`, `ReadNewP`,
`ReadWall`, `ReadFreeList`, `ReadProj`, `ReadMove`, `ReadSyncUnitsParams`,
`ReadFree`, `ReadSearch`, `ReadStand`, `ReadStop`, `ReadGate`,
`ReadLeaveOrder`, `ReadProjFree`, `ReadPeaceTime`, `ReadPackage`,
`ReadTradeResources`). Не декодированы: `ReadSquadNew` и `ReadSync`
(не встретились в проверенных replay'ах).

### 4.1 Engine-internal events (pid=14)

При pid=14 (`gc_playerind_progress`) state_id'ы — это **labels для
state-machine transitions движка**, а не вызовы handler'ов. Payload
для таких событий **НЕ совпадает** со script-handler signature
соответствующего state_id'а. Парсер помечает их как `engine_<state_name>`
и не пытается декодировать тело.

Примеры (`nick-niotid 2.rep`):
- `engine_ReadFree` (5897 событий) — engine periodically frees stale objects
- `engine_ReadSquadListAction` (5752) — engine batches squad updates
- `engine_WriteMove` (44) — engine broadcasts move packets

Эти ~12k pid=14 событий составляют большую часть entry'ев и
объясняют, почему класс=0x00 не "пуст" между явными командами игроков.

---

## 5. `gc_obj_order_type_*` — типы приказов

Из `dmscript.global:630-650`:

| код | имя              | смысл                              |
|----:|------------------|------------------------------------|
| 0   | `none`           | нет приказа                       |
| 1   | `move`           | движение                          |
| 2   | `attackobj`      | атаковать конкретный юнит/здание  |
| 3   | `gainres`        | собирать ресурс                   |
| 4   | `produce`        | производить (внутренний)          |
| 5   | `patrol`         | патруль (требует posx/posz)       |
| 6   | `attackpoint`    | атаковать точку (требует posx/posz)|
| 7   | `continueattackpoint` | продолжить attackpoint        |
| 8   | `performupgrade` | выполняющийся апгрейд             |
| 9   | `fishing`        | рыбалка                            |
| 10  | `creategates`    | создать ворота в стене             |
| 11  | `buildwallcontinue` | продолжить строить стену        |
| 12  | `buildwall`      | строить стену                      |
| 13  | `gotomine`       | войти в шахту                      |
| 14  | `gototransport`  | войти в транспорт                  |
| 15  | `leavetransport` | выйти из транспорта                |
| 16  | `leavebuilding`  | выйти из здания                    |
| 17  | `build`          | строить (=строитель идёт к стройке)|
| 18  | `guard`          | охранять                          |
| 19  | `repair`         | чинить                            |
| 20  | `exitunits`      | вывод юнитов                       |

В ReadOrder: при `ordtyp ∈ {5, 6}` (patrol/attackpoint) после `Int
number` идут **2 дополнительных Float'а posx, posz** (точка приказа).
Для остальных типов координаты не пишутся.

---

## 6. Каналы записи (5 native-каналов)

```
RecordCustomBegin(state)                       — default (units progress)
RecordCustomBeginGUI(state)                    — UI events
RecordCustomBeginMap(state)                    — map-level
RecordCustomBeginStateMachine(smhnd, state)    — конкретная FSM
RecordCustomBeginTagObject(taghnd, state)      — per-object FSM
```

В наблюдаемом `.rep` все entry имеют одинаковый 10-байт маркер —
либо в реплей пишется только default-канал, либо TagObject-канал
(class=0x09) идёт сквозно через тот же entry-формат, плюс редкие
class=0x00 (default-канал).

---

## 7. Эмпирические цифры по `nick-niotid 2.rep`

### 7.1 Партия в целом

| Метрика                          | Значение                              |
|----------------------------------|---------------------------------------|
| Размер файла                     | 5 362 671 байт                        |
| Длительность                     | 12152 ticks = **20.25 g-минут**       |
| Entries                          | 33 256                                |
| Sub-package'ей                   | 42 859                                |
| Стартовый снимок                 | 102 664 байт                          |
| Class=0x09 sync                  | 27 313 (74% sub-pkg)                  |
| Class=0x00 commands              | 8 640 (26% sub-pkg)                   |
| Игроков                          | 2 (pid=0 и pid=1)                     |
| Нации                            | Австрия (обе)                         |

### 7.2 Build-таймлайн (по ReadConstruct)

| g-сек | pid | sid          | builders |
|------:|:---:|--------------|---------:|
|   3.3 | 0   | auscen (TC)  | 12       |
|   4.7 | 1   | auscen (TC)  | 12       |
|   5.8 | 0   | eurmil (мельница) | 6   |
|   7.3 | 1   | eurmil       | 6        |
|  13.7 | 0   | eursto (камень) | 12    |
|  15.7 | 1   | eursto       | 12       |
|  28.9 | 0   | **eurmar (рынок)** | 18 ← user-validated «на 30-й секунде» |
|  32.0 | 1   | eurmar       | 18       |
|  34.2 | 0   | auscen (2-й TC) | 18    |
|  34.8 | 1   | eurgol (золото) | 12    |
| ...   |     |              |          |

### 7.3 Order-таймлайн (первые приказы)

| g-сек | pid | ordtyp     | таргет uid | юнитов |
|------:|:---:|------------|-----------:|-------:|
| 128.1 | 0   | gainres    | 6995       | 15     |
| 200.4 | 0   | build      | 7165       | 4      |
| 241.8 | 0   | gainres    | 4341       | 17     |
| 254.2 | 0   | gainres    | 4337       | 13     |
| 295.7 | 0   | gotomine   | 7065       | 15     |

### 7.4 Распределение state_id (class=0x00, верифицировано на 3 replay'ах)

| state_id | nick-niotid 2 | nick-niotid 1 | Длинная | handler                |
|---------:|--------------:|--------------:|--------:|------------------------|
| `0x08`   | 5 629         | 5 301         |  —      | (?) Progress           |
| `0x0d`   | 1 776 ✓       | 1 806 ✓       |  —      | ReadNew                |
| `0x17`   |   436 ✓       |   350 ✓       |   51 ✓  | ReadOrder              |
| `0x0f`   |   173         |   147         |  —      | (?) Progress           |
| `0x3d`   |   150 ✓       |   125 ✓       |  —      | ReadSyncUnitsParams    |
| `0x31`   |   110 ✓       |    94 ✓       |  246 ✓  | ReadTrade              |
| `0x2d`   |   124 ✓       |   144 ✓       |  —      | ReadNewP (fields)      |
| `0x21`   |    89 ✓       |    87 ✓       |  110 ✓  | ReadConstruct          |
| `0x13`   |    86 ✓       |     7 ✓       |  —      | ReadPlayer             |
| `0x29`   |     3 ✓       |    51 ✓       |  —      | ReadProj (combat)      |
| `0x1b`   |    52 ✓       |    36 ✓       |   88 ✓  | ReadProduce            |
| `0x19`   |    37 ✓       |    45 ✓       |   69 ✓  | ReadUpgrade            |
| `0x23`   |    34 ✓       |    41 ✓       |  —      | ReadApply              |
| `0x15`   |    19 ✓       |    26 ✓       |   13 ✓  | ReadRally              |
| `0x11`   |    19 ✓       |     3 ✓       |    4 ✓  | ReadDeath              |
| `0x0b`   |     1 ✓       |  —            |   43 ✓  | ReadMove               |
| `0x33`   |     7 ✓       |     6 ✓       |  —      | ReadWall               |
| `0x37`   |     1 ✓       |     1 ✓       |  —      | ReadFreeList (cleanup) |
| `0x0a`   |     6         |     7         |  —      | (?) Progress           |
| остальные|   <10         |   <10         |  —      | rare, TBD              |

### 7.5 Pid-разбивка

- `progress` (pid=14): 11 693 событий — engine-internal tick updates
- `player_0`: 1 999 — реальный игрок P0
- `player_1`: 1 849 — реальный игрок P1

### 7.6 ReadOrder ordtyp-распределение (на `nick-niotid 2.rep`, 662 events)

| ordtyp_name | count | смысл                                |
|-------------|------:|--------------------------------------|
| `build`     | 643   | приказ пеасантам строить здание     |
| `gainres`   |  13   | собирать ресурсы с заданной точки   |
| `gotomine`  |   6   | войти в шахту                       |

Move-команды (right-click на пустую землю) идут через **ReadMove** (state_id=0x0b),
а не через ReadOrder. Server-state-sync для движения юнитов — в class=0x09 stream.

### 7.7 ReadTrade распределение (на `nick-niotid 2.rep`, 133 events)

Большинство торгов: food → gold (54), gold → stone (17), gold → iron (12),
wood → gold (12), food → stone (11). То есть игроки активно конвертировали
еду в золото для найма наёмников и продавали золото за стратегические ресурсы.

---

## 8. Что хранится → что **не** хранится

**Хранится:**
- Настройки лобби (карта, randkey'и, peacetime, gamespeed, ...).
- Бинарное превью карты (BMP).
- Снапшот стартового мира (35 пеасантов, trees, mines, ...).
- Полный лог клиентских команд: build, produce, order, move, apply,
  rally, trade, capture.
- Полный лог серверных state-sync пакетов (class=0x09): обновления
  state-tag, позиций, hp юнитов.

**Не хранится в header'е** (но восстанавливается):
- `playerscount` и `startid` — выводятся по counts паттернов.
- Нации игроков — видны по sid'ам в первых ReadConstruct'ах.

**Не хранится вообще:**
- Имена игроков (только pid'ы).
- Чат / голос. (Может проходить через `ReadPackage`, не подтверждено).
- ELO / rating — приходят отдельно от Steam match-сервера.

---

## 9. Закрытые TBD

| TBD | Статус | Закрыто как |
|-----|--------|-------------|
| Семантика `ts` | ✓ | ticks × 0.1 = g-сек |
| Pid byte interpretation | ✓ | `gc_playerind_progress=14` и др. |
| Sub-package header layout | ✓ | 4B header + 1B 0x00 begin + body + 1B 0x01 end |
| String encoding | ✓ | `[u16 len][bytes]` (без префикса) |
| Multi-package boundaries | ✓ | через end-marker 0x01 и распознавание `00 03` начала след. sub-pkg |
| Class=0x09 layout | ✓ | `[09][u24 seq][u32 count][records]` |
| Class=0x09 record sizes | ✓ | variable 8..23B, base `[u32 uid][u32 statestag]` + state-flag-driven extensions |
| **ПОЛНАЯ карта state_id** | ✓ | из [`global.aix`](C:\Program Files (x86)\Steam\steamapps\common\Cossacks 3\data\scripts\units\global.aix), state_id = индекс section'а в файле |
| 27 handler'ов verified или identified | ✓ | см. таблицу в §4 |
| Cross-replay stability | ✓ | Карта state_id константна на 3 replay'ах |
| Где move-команды | ✓ | через `ReadMove` (state=0x0b) — отдельный handler, не через ReadOrder |
| Парность Read/Write state_id | ✓ | по global.aix: Read и Write идут попеременно (parity flips после separator'ов) |
| Engine pid=14 events | ✓ | те же state_id'ы, но payload — engine-internal, НЕ соответствует script handler |
| Размер-13 первый event | ✓ | sub=0x04 — особый init-пакет с другим layout'ом |

## 10. Открытые TBD

- **10-байт entry-маркер** `b0 04 ...` (`0x04b0=1200` — встречается в exe 99 раз как u16, но не как 10-байт последовательность). Скорее всего, генерируется runtime'ом из engine-internal struct'ы. Без disasm не разобрать.
- **`RecordCustomReadPackedFloat`** — native существует, в наших replay'ах не встречался. Возможно используется в `ReadSync` для компактного хранения координат.
- **Engine-internal payloads pid=14** (state=0x08, 0x0a, 0x0f). state_id это **label**, а не handler-dispatcher; payload пишется по другой схеме (probably packed state-tag deltas + stats). Не разобрано.
- **`ReadSync` (state=0x3b)** — самый сложный handler (полный snapshot юнита). Не встречен в replay'ах (вероятно используется только при initial-connect клиента к идущей игре). Можно поймать в save-файле.
- **`ReadSquadNew` (state=0x06)** — встречен 1-2 раза, decoder не написан. Сигнатура сложная (Bool + Int + String + 6*Int + 2*Bool + Int + Int + N*Int).
- Variable-record-size декодирование class=0x09 — записи >8B имеют поля, зависящие от state-flags юнита; без exe-disasm точная схема не выводится.

---

## 11. Связь с другими документами

- [`../engine/server_sync_architecture.md`](../engine/server_sync_architecture.md) — сетевая модель C3.
- [`../engine/server_sync_packet_format.md`](../engine/server_sync_packet_format.md) — бинарный `EconomyPackage`.
- [`../engine/ticks_and_subticks.md`](../engine/ticks_and_subticks.md) — `GetGameTime`/`GetCurrentTime`/`GetTimeSpeedFactor`.
- [`../engine/native_api.md`](../engine/native_api.md) — все `RecordCustom*` примитивы.
- [`../scripts/structure.md`](../scripts/structure.md) — FSM-формат `read*.inc`.
- [`../engine/rng_implementation.md`](../engine/rng_implementation.md) — `uniqrnd` синкается в ReadSync.
