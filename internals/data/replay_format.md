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

Размер записи на event обычно 8, 16, 20, или 28 байт. Самые частые
записи 8-байтовые: `[u32 uid][u32 statestag]` — компактное
обновление status-tag юнита. 16+ байтовые записи добавляют позицию
и/или дополнительные поля.

Это **74% всех sub-package'ей** (27 313 / 42 859 в `nick-niotid 2.rep`).
Эти записи — обычный server-сток state-tag'ов для каждого юнита
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

## 4. Карта `state_id` → handler

**Verified** (декодер построен и парсит 100% событий с этим state_id):

| state_id | handler           | сигнатура                              |
|---------:|-------------------|----------------------------------------|
| `0x0d`   | `ReadNew`         | Bool, String race, String base, 2*Float, 3*Int |
| `0x15`   | `ReadRally`       | Int uid, Bool, 2*Float (no bFromServer)|
| `0x17`   | `ReadOrder`       | Int ordtyp, Int taruid, 2*Bool, Int number, [2*Float if patrol/atkpoint], N*Int uids |
| `0x1b`   | `ReadProduce`     | 3*Int proid/prcid/amount, Bool state, Int count, N*Int building_uids |
| `0x21`   | `ReadConstruct`   | Bool, Int cid, String sid, 2*Float, Bool clrord, Int count, N*Int builder_uids |
| `0x23`   | `ReadApply`       | 4*Int plind/uid/cid/ind                |

**Probable** (по структурной близости к сигнатуре handler'а — нужна валидация):

| state_id | вероятно            | свидетельство                          |
|---------:|---------------------|----------------------------------------|
| `0x08`   | `Progress` или `ProgressEconomicAI` | 5629 событий с pid=14, периодика |
| `0x0f`   | `Progress` или `ProgressAI`         | 173 событий с pid=14            |
| `0x0a`   | `ProgressWarAI` (?) | 6 событий с pid=14, stats arrays      |
| `0x13`   | `ReadSquadNew` или `ReadSquadListAction` | большие nested события  |
| `0x3d`   | `ReadSyncUnitsParams` (?) | per-uid integer-stats updates   |
| `0x31`   | (контейнер с вложенным ReadNew) | спавн строящегося здания    |
| `0x19`   | `ReadStand` / `ReadSearch` (?) | 14-byte body, не совпало           |

**Unknown** (требуют отдельного разбора): `0x11, 0x27, 0x29, 0x2d, 0x33, 0x37, 0x39`.

Полные сигнатуры handler'ов читаются прямо в скриптах — см.
[`data/scripts/units/global.inc/read*.inc`](C:\Program Files (x86)\Steam\steamapps\common\Cossacks 3\data\scripts\units\global.inc\). 30 пар read/write secции в этой папке.

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

### 7.4 Распределение state_id (class=0x00)

| state_id | count | handler                  |
|---------:|------:|--------------------------|
| `0x08`   | 5 629 | (?) Progress             |
| `0x0d`   | 1 776 | ReadNew ✓                |
| `0x17`   |   436 | ReadOrder ✓              |
| `0x0f`   |   173 | (?) ProgressAI           |
| `0x3d`   |   150 | (?) ReadSyncUnitsParams  |
| `0x31`   |   110 | (?) контейнер с вложенным ReadNew |
| `0x21`   |    89 | ReadConstruct ✓          |
| `0x13`   |    86 | (?) ReadSquadListAction  |
| `0x1b`   |    52 | ReadProduce ✓            |
| `0x19`   |    37 | (?)                      |
| `0x23`   |    34 | ReadApply ✓              |
| `0x15`   |    19 | ReadRally ✓              |
| остальные|   <30 | TBD                      |

### 7.5 Pid-разбивка

- `progress` (pid=14): 11 693 событий — engine-internal tick updates
- `player_0`: 1 999 — реальный игрок P0
- `player_1`: 1 849 — реальный игрок P1

### 7.6 Топ-команды по типу

ReadOrder (662 events):
- `gainres` (gather resources) — главная экономическая команда
- `gotomine` — посадить пеасантов в шахту
- `build` — приказать строить
- `attackobj` / `attackpoint` — боевые приказы

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
| 6 ключевых handler'ов | ✓ | Construct, New, Rally, Order, Produce, Apply |

## 10. Открытые TBD

- 10-байт entry-маркер `b0 04 ...` (вероятно channel-id `0x04b0=1200`)
- Точное соответствие state_id для остальных handler'ов (≈20 state_id'ов не сопоставлены)
- `RecordCustomReadPackedFloat` — формат записи
- Class=0x09 запись: точные поля при rec_size > 16
- Размер-13 первый event в `nick-niotid 2.rep` (ts=14.13, payload
  `00 04 40 00 00 00 60 41 02 00 00 00 01`) — не подходит ни под
  один из проверенных handler'ов. Возможно `ReadPackage` или
  специальный init-пакет.

---

## 11. Связь с другими документами

- [`../engine/server_sync_architecture.md`](../engine/server_sync_architecture.md) — сетевая модель C3.
- [`../engine/server_sync_packet_format.md`](../engine/server_sync_packet_format.md) — бинарный `EconomyPackage`.
- [`../engine/ticks_and_subticks.md`](../engine/ticks_and_subticks.md) — `GetGameTime`/`GetCurrentTime`/`GetTimeSpeedFactor`.
- [`../engine/native_api.md`](../engine/native_api.md) — все `RecordCustom*` примитивы.
- [`../scripts/structure.md`](../scripts/structure.md) — FSM-формат `read*.inc`.
- [`../engine/rng_implementation.md`](../engine/rng_implementation.md) — `uniqrnd` синкается в ReadSync.
