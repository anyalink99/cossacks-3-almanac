# Replay / Save (`.rep`, `.map`) — формат `OSWMap13`

Cossacks 3 пишет реплеи и сохранения в одном бинарном формате
`OSWMap13`. Файл — это **снимок мира на старте и поток сетевых
пакетов**, тот же поток, который сервер рассылает клиентам в
онлайн-игре (см.
[`../engine/server_sync_architecture.md`](../engine/server_sync_architecture.md)).

Воспроизведение реплея в движке реализовано через клиентский кодовый
путь сетевой игры: каждый пакет из ленты разбирается тем же
`Read*`-handler'ом, который сработал бы у online-клиента при получении
пакета по сети. Сервер в replay-режиме ничего не просчитывает
(см. `progress.inc:46`: `if (_net_IsClient or _net_IsReplay) then //
global do not progress`).

Парсеры в этом проекте:

- [`parser/parse_replay.py`](../../parser/parse_replay.py) — header
  и подсчёт паттернов карты.
- [`parser/parse_replay_events.py`](../../parser/parse_replay_events.py)
  — полный разбор потока событий, выводит JSON-таймлайн.

---

## 1. Общая разметка файла

```
+--- Header (~168 КБ) -------------------------------------+
| OSWMap13 + Build.Ver[X.Y.Z.NNNN] + UID                   |
| GameMapSnapShotBegin                                     |
|   [BMP, ~145 КБ — превью карты]                          |
| GameMapSnapShotEnd                                       |
| GameMapRecordBegin                                       |
|   <key,value> пары в текстовом формате:                  |
|     maskname, mapsize, relieftype, randkey0, randkey1,   |
|     terraintype, season, gamespeed, resourcemines,       |
|     limit, ver, ...                                      |
+--- Body ---------------------------------------------- ---+
| Поток entry'ев с timestamp'ом и payload'ом:              |
|   entry[0]:   ts=0,         payload = снимок стартового  |
|                              мира (юниты, ресурсы)       |
|   entry[1+]:  ts > 0 ticks, payload = один или несколько |
|                              sub-package'ей              |
| GameMapRecordEnd                                         |
+----------------------------------------------------------+
| Хвост: несколько финальных kv-пар (init-state markers)   |
+----------------------------------------------------------+
```

Header'ы и kv-пары парсятся напрямую как длиннопрефиксные ASCII-строки.
Тело — это последовательность entry-блоков; декодер должен пройти
до маркера `GameMapRecordEnd` и не пытаться парсить хвост как entry.

---

## 2. Entry: 18-байтовый заголовок и payload

```
offset  size  поле                                    замечание
---------------------------------------------------------------------
+0      4B    float ts                                ticks; см. §2.1
+4      4B    u32 payload_size LE                     размер payload
+8     10B    const "b0 04 00 00 00 00 00 00 00 00"   entry-маркер
+18    N      payload                                  N = payload_size
```

### 2.1 Семантика `ts`

`ts` — это игровые ticks с шагом 0.1 g-сек:

```
g_sec = ts / 10
```

Шаг 0.1 g-сек держится константно для всех игровых скоростей: при
любом значении lobby-`gamespeed` отношение
`ticks_per_real_sec / game_factor` всегда равно 10:

| `gamespeed` | `gc_settings_gamespeed_N` (ticks/real-sec) | factor | g-sec/tick |
|-------------|:------------------------------------------:|:------:|:----------:|
| Slow        | 7                                          | 0.7    | 0.1        |
| Normal      | 10                                         | 1.0    | 0.1        |
| Fast        | 14                                         | 1.4    | 0.1        |

Значения `ts` дробные (например, 14.130 вместо 14.1), потому что
движок пишет `GetCurrentTime × GetTimeSpeedFactor` с полной
float-точностью, а не округляет до целого тика.

### 2.2 Десятибайтовый entry-маркер

Каждый entry в body предваряется фиксированной последовательностью
`b0 04 00 00 00 00 00 00 00 00`. Эти 10 байт идентичны для всех
entry'ев в одном файле. Семантика байт пока не разобрана; вероятная
интерпретация — `u16 0x04b0 = 1200` как идентификатор канала записи
плюс 8 байт резерва. В коде исполняемого файла literal-сравнения с
этой последовательностью не обнаружено — маркер, вероятно,
формируется runtime'ом из значения engine-internal struct'ы.

---

## 3. Sub-package: внутренняя структура payload'а

Один entry содержит один или несколько sub-package'ей
(см. native `RecordPackagesCount`, `RecordPackagesCursor`). При записи
каждый sub-package обёрнут парой `RecordCustomBegin(stateName) /
RecordCustomEnd`; при чтении движок диспетчеризует пакет в FSM-секцию
с именем `stateName` через `SwitchTo(stateName)`.

### 3.1 Class=0x00 (default channel) — формат

```
offset  size  поле                                    замечание
---------------------------------------------------------------------
+0      4B    [class=0x00, sub=0x03, pid, state_id]   4-байтовый header
+4      1B    0x00                                    begin-marker
+5      ?B    typed body                              типизированный поток
+?      1B    0x01                                    end-marker
```

Этот формат используется для команд игрока (build, produce, move,
trade, ...) и для engine-progress событий (см. §3.5). Channel ID 0x03
— это `RecordCustomBegin` (default channel, см. §6).

**Pid mapping** (`dmscript.global`):

| pid    | роль                                              |
|-------:|---------------------------------------------------|
| 0..11  | реальные игроки (`gc_MaxPlayerCount = 12`)        |
| 12     | `gc_playerind_env`                                |
| 13     | `gc_playerind_misc`                               |
| 14     | `gc_playerind_progress` — engine progress events  |
| 15     | `gc_playerind_pool`                               |

### 3.2 Class=0x09 (TagObject state-sync stream) — формат

Канал per-object state-sync (`RecordCustomBeginTagObject`) пишется
в другой схеме:

```
offset  size  поле
------------------------------------------------------
+0      1B    0x09                       — class
+1      3B    u24 LE — global sequence counter (монотонный)
+4      4B    u32 LE — count записей
+8      ?B    count записей переменного размера
```

Размер записи варьируется от 8 до 23 байт с шагом ~3 байта. Базовая
часть `[u32 uid][u32 statestag]` (8 байт) присутствует всегда;
расширения добавляются по битам `statestag` — например, при изменении
позиции пишется пара `Float posx, posz`. Конкретный набор полей для
каждой комбинации флагов в публичных скриптах не описан.

### 3.3 Типизированные `RecordCustomRead*`-примитивы

```
RecordCustomReadBoolean   — 1 байт (любое ненулевое = true)
RecordCustomReadByte      — 1 байт
RecordCustomReadWord      — 2 байта LE
RecordCustomReadSmallInt  — 2 байта LE signed
RecordCustomReadInt24     — 3 байта LE signed
RecordCustomReadInteger   — 4 байта LE signed
RecordCustomReadFloat     — 4 байта LE IEEE-754
RecordCustomReadString    — [u16 len LE][bytes]
RecordCustomReadShortString — [u8 len][bytes]
RecordCustomReadPackedFloat — float, упакованный в фиксированный диапазон
RecordCustomReadBit + RecordCustomBeginReadBitFields — для bit-stream'ов
```

`String` — это просто `[u16 len LE][bytes]`, никакого префикса. Например,
sid `"auscen"` в payload'е выглядит как:

```
06 00                          u16 len = 6
61 75 73 63 65 6e              "auscen"
```

### 3.4 Multi-package entry

Один entry часто содержит несколько sub-package'ей. После
end-marker'а `0x01` сразу идёт либо `0x00 0x03 [pid] [state_id] 0x00`
(начало следующего class=0x00 sub-package'а), либо `0x09 [u24 seq]`
(class=0x09 TagObject-запись). Декодер должен распознавать обе формы.

Пример: запрос на постройку здания (`ReadConstruct`) обычно
сопровождается одной `class=0x09`-записью — серверным state-tag'ом
для созданной construction dummy. Команда `ReadProduce` на дип-центр
порождает несколько вложенных `ReadNew` для каждого
наёмника-кандидата.

### 3.5 Engine-progress события (pid=14)

При pid=14 (`gc_playerind_progress`) state_id'ы используются как
**метки FSM-переходов движка**, а не как dispatch'еры handler'ов.
Тело такого sub-package'а **не соответствует** сигнатуре скриптового
handler'а с тем же state_id; вместо этого движок пишет компактную
дельту собственного состояния.

Три самых частых engine-progress state_id (по эмпирическим данным):

- `0x08` (`ReadSquadListAction`) — periodic squad-bookkeeping batch
- `0x0a` (`WriteMove`) — server-side broadcast приказов движения
- `0x0f` (`ReadFree`) — periodic cleanup устаревших объектов

Декодеру следует пропускать тело таких событий, маркируя их как
`engine_<state_name>`.

---

## 4. Карта state_id → handler

**Источник:** [`data/scripts/units/global.aix`](C:\Program Files (x86)\Steam\steamapps\common\Cossacks 3\data\scripts\units\global.aix)
описывает FSM-секции в порядке загрузки. **`state_id` совпадает с
индексом секции** в файле (включая separator'ы и `section.end`).

| state_id | section name                | примечание                              |
|---------:|-----------------------------|-----------------------------------------|
| `0x00`   | `Initial`                   | начальное состояние FSM                 |
| `0x01`   | `OnBeforeSave`              |                                         |
| `0x02`   | `OnAfterLoad`               |                                         |
| `0x03`   | `Progress`                  | per-player progress tick                |
| `0x05`   | `WriteSquadNew`             |                                         |
| `0x06`   | `ReadSquadNew`              | создание формации                       |
| `0x07`   | `WriteSquadListAction`      |                                         |
| `0x08`   | `ReadSquadListAction`       | действие над списком squad'ов           |
| `0x0a`   | `WriteMove`                 | server broadcasts move                  |
| `0x0b`   | `ReadMove`                  | per-unit destination + facing           |
| `0x0c`   | `WriteNew`                  |                                         |
| `0x0d`   | `ReadNew`                   | спавн юнита от сервера                  |
| `0x0e`   | `WriteFree`                 |                                         |
| `0x0f`   | `ReadFree`                  | удаление объекта                        |
| `0x10`   | `WriteDeath`                |                                         |
| `0x11`   | `ReadDeath`                 | смерть юнита (с RNG seed restore)       |
| `0x12`   | `WritePlayer`               |                                         |
| `0x13`   | `ReadPlayer`                | смена владельца (захват)                |
| `0x14`   | `WriteRally`                |                                         |
| `0x15`   | `ReadRally`                 | rally-point на здании                   |
| `0x16`   | `WriteOrder`                |                                         |
| `0x17`   | `ReadOrder`                 | приказ (build/gainres/attackobj/...)    |
| `0x18`   | `WriteUpgrade`              |                                         |
| `0x19`   | `ReadUpgrade`               | start/cancel research                   |
| `0x1a`   | `WriteProduce`              |                                         |
| `0x1b`   | `ReadProduce`               | очередь на производство юнита           |
| `0x1c`   | `WriteSearch`               |                                         |
| `0x1d`   | `ReadSearch`                | переключение search-enemy               |
| `0x1e`   | `WriteStand`                |                                         |
| `0x1f`   | `ReadStand`                 | переключение stand-ground               |
| `0x20`   | `WriteConstruct`            |                                         |
| `0x21`   | `ReadConstruct`             | заказ строительства здания              |
| `0x22`   | `WriteApply`                |                                         |
| `0x23`   | `ReadApply`                 | применение завершённого апгрейда        |
| `0x24`   | `WriteLeaveOrder`           |                                         |
| `0x25`   | `ReadLeaveOrder`            | список юнитов на выход из здания        |
| `0x26`   | `WriteLeave`                |                                         |
| `0x27`   | `ReadLeave`                 | выход юнита из здания                   |
| `0x28`   | `WriteProj`                 |                                         |
| `0x29`   | `ReadProj`                  | выстрел снаряда                         |
| `0x2a`   | `WriteProjFree`             |                                         |
| `0x2b`   | `ReadProjFree`              | уничтожение снаряда                     |
| `0x2c`   | `WriteNewP`                 |                                         |
| `0x2d`   | `ReadNewP`                  | спавн primitive (поля, шары, ship-dummy)|
| `0x2e`   | `WriteStop`                 |                                         |
| `0x2f`   | `ReadStop`                  | отмена приказов                         |
| `0x30`   | `WriteTrade`                |                                         |
| `0x31`   | `ReadTrade`                 | торговля на рынке                       |
| `0x32`   | `WriteWall`                 |                                         |
| `0x33`   | `ReadWall`                  | строительство стенного кластера         |
| `0x34`   | `WriteGate`                 |                                         |
| `0x35`   | `ReadGate`                  | открыть/закрыть ворота                  |
| `0x36`   | `WriteFreeList`             |                                         |
| `0x37`   | `ReadFreeList`              | массовое удаление объектов              |
| `0x38`   | `WritePeaceTime`            |                                         |
| `0x39`   | `ReadPeaceTime`             | переключение peace-mode                 |
| `0x3a`   | `WriteSync`                 |                                         |
| `0x3b`   | `ReadSync`                  | полный snapshot юнита                   |
| `0x3c`   | `WriteSyncUnitsParams`      |                                         |
| `0x3d`   | `ReadSyncUnitsParams`       | HP-синхронизация для группы юнитов      |
| `0x3f`   | `WritePackage`              |                                         |
| `0x40`   | `ReadPackage`               | произвольное текстовое net-сообщение    |
| `0x42`   | `ProgressAI`                | engine internal                         |
| `0x43`   | `ProgressEconomicAI`        | engine internal                         |
| `0x44`   | `ProgressWarAI`             | engine internal                         |
| `0x45`   | `CheckErrors`               | engine internal                         |
| `0x46`   | `ReadTradeResources`        | передача ресурсов союзнику              |
| `0x47`   | `WriteTradeResources`       |                                         |

State_id'ы 0x04, 0x09, 0x12, 0x3e, 0x41 — это separator-записи
(`Name = ----------------------` в `global.aix`), они не
ассоциированы с handler'ом.

Сигнатуры всех `Read*`-handler'ов читаются из
[`data/scripts/units/global.inc/read*.inc`](C:\Program Files (x86)\Steam\steamapps\common\Cossacks 3\data\scripts\units\global.inc\).

---

## 5. `gc_obj_order_type_*` — типы приказов в `ReadOrder`

Значения из `dmscript.global:630-650`:

| код | имя                  | смысл                              |
|----:|----------------------|------------------------------------|
| 0   | `none`               | нет приказа                        |
| 1   | `move`               | движение                           |
| 2   | `attackobj`          | атаковать конкретный юнит/здание   |
| 3   | `gainres`            | собирать ресурс                    |
| 4   | `produce`            | производить (внутренний)           |
| 5   | `patrol`             | патруль                            |
| 6   | `attackpoint`        | атаковать точку                    |
| 7   | `continueattackpoint`| продолжить attackpoint             |
| 8   | `performupgrade`     | выполняющийся апгрейд              |
| 9   | `fishing`            | рыбалка                            |
| 10  | `creategates`        | создать ворота в стене             |
| 11  | `buildwallcontinue`  | продолжить строить стену           |
| 12  | `buildwall`          | строить стену                      |
| 13  | `gotomine`           | войти в шахту                      |
| 14  | `gototransport`      | войти в транспорт                  |
| 15  | `leavetransport`     | выйти из транспорта                |
| 16  | `leavebuilding`      | выйти из здания                    |
| 17  | `build`              | строитель идёт к стройке           |
| 18  | `guard`              | охранять                           |
| 19  | `repair`             | чинить                             |
| 20  | `exitunits`          | вывод юнитов                       |

В `ReadOrder` при `ordtyp ∈ {patrol=5, attackpoint=6}` после поля
`number` идут два дополнительных `Float`'а `posx, posz` — точка
приказа. Для остальных значений координаты не пишутся.

Реальные **right-click-на-точку** идут не через `ReadOrder`, а через
отдельный handler `ReadMove` (state_id=`0x0b`). `ordtyp=1 (move)` в
`ReadOrder` встречается на практике крайне редко.

---

## 6. Каналы записи

Native API экспортирует пять channel-варианта `RecordCustomBegin*`.
Disassembly `RecordCustomBegin` (VA `0x685c38`, реализация
`0x733590`) показывает, что **второй байт sub-package'а** — это
channel ID, выбираемый из таблицы сравнений:

| channel ID | native API                          |
|-----------:|-------------------------------------|
| 1          | `RecordCustomBeginMap`              |
| 2          | (зарезервированный/internal)        |
| **3**      | **`RecordCustomBegin`** (default)   |
| 4          | `RecordCustomBeginStateMachine`     |
| 5          | `RecordCustomBeginTagObject`        |

Для default-канала это даёт наблюдаемый префикс sub-package'а
`00 03 [pid] [state_id]`:

- byte 0 = `0x00` — hardcoded begin-marker
- byte 1 = `0x03` — channel ID (default)
- bytes 2-3 — упакованные `pid` и `state_id`

Class=`0x09` sub-package'и — это TagObject channel; его первый байт
имеет фиксированное значение `0x09`, и схема записи у него
отличается (см. §3.2): движок пишет per-object state deltas в
компактной форме.

Опорные адреса в `cossacks.exe` для дальнейшего исследования:
`RecordCustomBegin = VA 0x685c38`, реализация = `0x733590`,
`WriteBytes = 0x5b4620`, channel-tables `0x789980` (Map),
`0x7c3160`, `0x7af5e8`.

---

## 7. Что хранится и что не хранится

**Хранится:**

- Настройки лобби (карта, randkey'и, peacetime, gamespeed,
  resourcemines, terraintype, season).
- BMP-превью карты.
- Стартовый снимок мира (начальные юниты, ресурсы, кластеры).
- Полный лог клиентских команд: build, produce, order, move, apply,
  rally, trade, capture, wall, upgrade.
- Полный лог серверных state-sync пакетов (class=`0x09`): обновления
  state-tag, позиций, hp юнитов.

**Не хранится в header'е, но восстанавливается:**

- `playerscount` и `startid` — выводятся по counts паттернов карты
  (см. [`map_generation_pipeline.md`](../../docs/recon/world/map/map_generation_pipeline.md)).
- Нации игроков — определяются по sid'ам в первых `ReadConstruct`'ах.

**Не хранится вообще:**

- Имена игроков (только pid'ы).
- Чат и голос — возможно идут через `ReadPackage`, но в наблюдаемых
  потоках не зафиксированы.
- ELO и рейтинг — приходят отдельно из Steam match-сервера.

---

## 8. Закрытые TBD

| TBD                                   | Закрыто как                              |
|---------------------------------------|------------------------------------------|
| Семантика `ts`                        | ticks × 0.1 = g-сек                      |
| Pid byte interpretation               | `gc_playerind_progress=14` и др.         |
| Sub-package header layout             | 4B header + 0x00 begin + body + 0x01 end |
| String encoding                       | `[u16 len][bytes]`, без префикса         |
| Multi-package boundaries              | через end-marker `0x01` и распознавание `00 03` старта следующего sub-pkg |
| Class=0x09 layout                     | `[09][u24 seq][u32 count][records]`      |
| Полная карта state_id                 | через индекс section'а в `global.aix`    |
| Различение Read*/Write*               | Read и Write идут попеременно в `global.aix` |
| Каналы записи                         | из disasm `RecordCustomBegin` (§6)       |
| Семантика engine pid=14 событий       | state_id используется как метка FSM-перехода, payload — engine-internal |

## 9. Открытые TBD

- Содержимое 10-байт entry-маркера `b0 04 00 00 00 00 00 00 00 00`.
  Значение `0x04b0 = 1200` встречается в коде exe 99 раз как
  16-битовый константный operand, но как 10-байт последовательность
  не присутствует. Маркер, вероятно, формируется runtime'ом из
  engine-internal struct'ы.
- Точная схема variable-length записи class=`0x09` при размере
  больше 8 байт. Дополнительные поля выбираются битами `statestag`;
  таблица соответствия флагов и полей требует disasm
  `RecordCustomBeginTagObject` и связанных write-routine'ов.
- Формат `RecordCustomReadPackedFloat`. Native существует, но в
  стандартных streams не наблюдается; вероятно, используется в
  `ReadSync` для упаковки координат и углов.
- Тело engine-progress payload'ов (state_id'ы 0x08, 0x0a, 0x0f
  при pid=14). Layout отличается от script handler signature и
  записывается напрямую engine-кодом.
- `ReadSync` (state_id=`0x3b`). Сложная сигнатура (полный snapshot
  юнита со всеми ориентационными матрицами, hp, RNG-seed). В
  обычных replay'ях не наблюдается; вероятно, используется при
  initial-connect клиента к идущей игре.

---

## 10. Связь с другими документами

- [`../engine/server_sync_architecture.md`](../engine/server_sync_architecture.md)
  — сетевая архитектура C3.
- [`../engine/server_sync_packet_format.md`](../engine/server_sync_packet_format.md)
  — бинарный `EconomyPackage`.
- [`../engine/ticks_and_subticks.md`](../engine/ticks_and_subticks.md)
  — `GetGameTime`, `GetCurrentTime`, `GetTimeSpeedFactor`.
- [`../engine/native_api.md`](../engine/native_api.md) — каталог
  `RecordCustom*`-примитивов.
- [`../scripts/structure.md`](../scripts/structure.md) — формат
  FSM-секций в `read*.inc`/`write*.inc`.
- [`../engine/rng_implementation.md`](../engine/rng_implementation.md)
  — `uniqrnd` (per-object RNG seed), синхронизируемый в `ReadSync`
  и `ReadDeath`.
