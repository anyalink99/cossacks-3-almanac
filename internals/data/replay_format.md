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
+8     10B    entry-маркер                            см. §2.2
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

### 2.2 Десятибайтовый entry-маркер — два варианта

Каждый entry в body предваряется 10-байтовой последовательностью.
Наблюдаются ДВА варианта; разделяет их состояние middle-word'а:

```
вариант A (saves, локальные replay'и):
  b0 04 00 00 00 00 00 00 00 00

вариант B (rated/online матчи):
  b0 04 <4B signature> 00 00 00 00
                       ^^^^^^^^^^^ хвост остаётся нулевым
         ^^^^^^^^^^^^^ ненулевое слово, КОНСТАНТНОЕ для одного файла
```

Инварианты, на которые опирается walker:

- Первые 2 байта — всегда `b0 04`.
- Последние 4 байта — всегда нули.
- Middle-word (offset +2 от начала маркера) может быть нулевым или
  ненулевым, но в пределах одного файла он постоянен — это сигнатура
  потока, выдаваемая при `RecordCustomBegin`-init.

Walker должен сканировать prefix `b0 04` и принимать любые 10 байт,
у которых last-4 == 0. Старые декодеры, проверявшие весь маркер
literally, на rated-replay'ях теряли 98% entry'ев — именно тот entry-
поток, через который сервер раздаёт команды клиентов.

Семантика middle-word ещё не разобрана. `0x04b0 = 1200` встречается
в коде exe 99 раз как 16-битовый operand, но как 10-байт sequence не
присутствует — маркер формируется runtime'ом из engine-internal
struct'ы (`RecordCustomBegin` → channel-table).

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

Канал per-object state-sync (`RecordCustomBeginTagObject @ 0x685c6c`)
пишется в другой схеме:

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
расширения добавляются по битам `statestag`.

#### Three-way dispatch — три подформата записи

Декомпиляция `RecordCustomBeginTagObject` (приватный recon-workspace
`cossacks-deep/decompiled/record.c:286-338`, перекрёстная заметка —
`cossacks-deep/findings/record_sync.md`) раскрывает, что один и тот
же class=0x09 channel несёт три разных под-формата, выбираемые по
типу переданного handle. Движок последовательно пробует три
классификации:

| Категория      | Resolver               | Источник state_record   | Признак handle             |
|----------------|------------------------|-------------------------|----------------------------|
| `TaggedHandle` (SM state) | `ResolveTaggedHandle`      | `obj + 0x18` (variables collection) | high bits `0x8000` в обеих половинах handle |
| `GameObject`   | `ValidateGameObjectHandle` | `FUN_007c32ec(go)` (sync-context accessor) | проходит `ValidateGameObjectHandle` |
| `Player`       | `ValidatePlayerHandle`     | `obj + 0x24` (player.sync_field) | проходит `ValidatePlayerHandle` |

Все три пути в итоге зовут `_RecordManager_BeginTagWrite` с разным
state-record'ом, поэтому набор сериализованных полей в record'ах
class=0x09 зависит от того, *какой объект был тегирован при записи*.

Парсер, который пытается декодировать все class=0x09 записи единой
схемой, будет периодически путаться. Корректный декодер должен
сначала диспетчеризоваться по маркеру в начале record'а
(пока не разобрано — какой именно байт несёт tag-категорию), и
применять разные layout'ы к Tagged-SM / GameObject / Player потокам.

В практике replay-parser'а проще оставить class=0x09 как «считать
record'ы, тело не декодировать» — почти весь полезный сигнал лежит
в class=0x00 командах, а sync-поток гигантский (миллионы записей в
длинной партии) и его декомпозиция замедляет парсер на порядок.

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
RecordCustomReadPackedFloat — 2 байта uint16 LE; decode = min + (raw/65535)*(max-min); min/max не в потоке, подразумеваются контекстом записи (см. ниже)
RecordCustomReadBit + RecordCustomBeginReadBitFields — для bit-stream'ов
```

#### `PackedFloat` — 2 байта uint16

Подтверждено декомпиляцией `_Stream_WritePackedFloat @ 0x5b46e0`
(приватный `cossacks-deep/decompiled/record.c` + `findings/record_sync.md`).
Engine-side:

```c
normalized = clamp((value - min) / (max - min), 0, 1);
write_u16_le(round(normalized * 65535));
```

Decode в парсере (`Reader.packed_float(min, max)` в
`parser/parse_replay_events.py`):

```python
raw = read_u16_le()
value = min + (raw / 65535.0) * (max - min)
```

**Важная тонкость.** `min/max` **не записываются в поток**. Они
**подразумеваются** use-site'ом — каждый вызов
`RecordCustomWritePackedFloat(value, min, max)` использует свои
константы. Чтобы корректно декодировать конкретное PackedFloat-поле,
парсер должен знать какой диапазон был использован при записи.
В практике это означает таблицу «state X, поле Y → min=N, max=M».

#### Строки

`String` — это просто `[u16 len LE][bytes]`, никакого префикса. Например,
sid `"auscen"` в payload'е выглядит как:

```
06 00                          u16 len = 6
61 75 73 63 65 6e              "auscen"
```

#### Bitfield order — LSB-first

Внутри bit-pack'а (`BeginBitFields … WriteBit × N … EndBitFields`)
биты пакуются **младшим вперёд** (LSB-first). Декомпиляция
`_Stream_WriteBit @ 0x5b4874` (приватный recon-workspace
`cossacks-deep/decompiled/record.c:728-745`):

```c
*(byte *)(stream + 0x14) |= *(byte *)(stream + 0x15);  // OR в текущий байт по маске
*(byte *)(stream + 0x15) <<= 1;                         // mask <<= 1
```

Mask стартует со значения `0x01` и сдвигается влево после каждого
записанного бита. Это значит: первый `WriteBit(true)` ставит бит
`0x01`, второй — `0x02`, и так далее. На чтении (`ReadBit`) парсер
обязан повторять эту же логику — иначе все packed bool'ы развернутся
в зеркальном порядке.

При `EndBitFields` неполный байт выравнивается до целого, mask
сбрасывается. То есть длина bit-pack'а в потоке — `ceil(N_bits / 8)`
байт, а не сжатая до бита.

`Int24` подтверждён как 3 байта LE signed (`RecordCustomWriteInt24 @
0x6860d4` использует `_Stream_WriteByte × 3` без знакового extend
при upper-byte).

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

### 4.1 Сигнатуры тел ключевых handler'ов

Параметры в порядке записи. Типы — это `RecordCustomRead*`-примитивы
из §3.3. Эти шесть handler'ов покрывают почти весь анализ команд
игрока.

```
ReadConstruct   (0x21)  Bool bFromServer
                        Int  cid                 ← country index игрока
                        Str  sid                 ← sid здания
                        Float posx, posz
                        Bool clrord
                        Int  count
                        Int[count] builder-uids

ReadNew         (0x0d)  Bool bFromServer
                        Str  race, base
                        Float posx, posz
                        Int  cid                 ← cid≤0 → -cid = country;
                                                   cid>0 → uid здания-производителя
                        Int  uid, num

ReadNewP        (0x2d)  Bool bFromServer
                        Str  race, base
                        Float posx, posz, roll
                        Int  plind, id, uid, num

ReadOrder       (0x17)  Int  ordtyp              ← см. §5
                        Int  taruid
                        Bool clrord, locktrg
                        Int  number
                        Float posx, posz         ← только при ordtyp ∈ {5,6}
                        Int[number] unit-uids

ReadProduce     (0x1b)  Int  proid               ← индекс в country.members[]
                        Int  prcid               ← country index юнита
                        Int  amount              ← -1 = infinite queue
                        Bool state               ← start / cancel
                        Int  count
                        Int[count] building-uids

ReadUpgrade     (0x19)  Bool bFromServer
                        Int  upgid               ← индекс в gCountry[cid].upgrade[]
                        Bool state               ← start / cancel
                        Int  count
                        Int[count] building-uids

ReadApply       (0x23)  Int  plind, uid          ← target
                        Int  cid, ind            ← gCountry[cid].upgrade[ind]
```

Семантические замечания:

- **`ReadProduce.proid`** — это индекс в упорядоченном списке
  members нации (`_country_AddMember` в `country.script`).
  Расшифровка: `country_members[NATION_BY_CID[prcid]][proid] = sid`.
  Список member'ов экстрактится симулятором апгрейдов в
  `derived/country_members.json`.
- **`ReadUpgrade.upgid` и `ReadApply.ind`** — индекс в
  `gCountry[cid].upgrade[]`. Engine строит этот массив в `_country_Init`
  (с inline-call'ом `_country_InitUnitsUpgrades`), вызывая
  `SetUpgStruct` / `AddUpgradePack` / `_country_AddUpgrade` по фиксированному
  порядку. Парсер в [`parser/simulate_upgrades.py`](../../parser/simulate_upgrades.py)
  повторяет ту же последовательность и эмитит `data.json :: upgrades`
  с упорядоченным per-nation списком — list-index в нём равен
  `upgid`/`ind`. Без правильного порядка `upgid=2` будет ложно
  указывать на «казармы», а не на мельницу.
- **`ReadConstruct.cid`** — country index игрока (тот же что
  `TMapPlayer.cid`, см. §11.2). Полезен для определения нации, когда
  в TMapPlayer стоит `cid=-2` (random) и нация неизвестна заранее.

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

#### Current write stream + проверка парности

Раскладка `RecordManager`-структуры выявлена декомпиляцией record.c
(приватный recon-workspace `cossacks-deep/decompiled/record.c` плюс
обзор `cossacks-deep/findings/record_sync.md`). Все
`RecordCustomWrite*`-примитивы перед сериализацией читают указатель
на текущий буфер по адресу:

```
*(int*)(*(int*)(root + 0x4c) + 0x6c) + 0x118
                 │              │     │
                 │              │     └── current write stream (ptr)
                 │              └──────── RecordManager
                 └─────────────────────── главный sub-manager
```

Если по `+0x118` лежит NULL, write-операция тихо ничего не пишет.
Это значит, что **valid replay-поток обязан содержать парные
begin/end записи**: `RecordCustomBegin*` инициализирует stream,
`RecordCustomEnd` (`@ 0x685e00`) его обнуляет, и любые
write-вызовы между ними попадают в буфер, а после end'а — нет.

Прикладные следствия для парсера:

- Поток sub-package'ей в одном entry устроен как
  «begin → body → end → begin → body → end …», end-marker `0x01`
  в class=0x00 — это runtime-side подтверждение, что
  `RecordCustomEnd` выполнен и stream закрыт.
- Если декодер натыкается на ситуацию «несколько begin'ов подряд
  без end'а» — это либо вложенные begin'ы (TagObject внутри SM),
  либо повреждённый файл. В наблюдаемых replay'ях вложений не
  замечено: TagObject всегда стоит отдельным sub-package'ем.
- `recordEnabled` / `recordGroupEnabled` / `recordInitializeEnabled`
  флаги в RecordManager (`+0x130`, `+0x131`, `+0x132`) могут
  обнулять stream на лету; начальный snapshot (entry с `ts == 0`)
  пишется при `recordInitializeEnabled = true`.

---

## 7. Что хранится в header'е

### 7.1 Lobby settings

Все поля `gMap.settings.*` пишутся в kv-stream header'а в текстовой
форме (`[u16 keylen][key][u16 vallen][val]`). Полный список (имена ↔
смысл) — в [`docs/recon/world/map/game_settings.md`](../../docs/recon/world/map/game_settings.md);
канонические enum-метки → `derived/game_settings.json`. Сюда входят
все правила партии (`peacetime`, `century18`, `capture`, `marketdip`,
`cannons`, `balloon`, `startingunits`, `resourcestart`, `gamespeed`,
`resourcemines`, `terraintype`, `relieftype`, `season`, `limit`,
`maskname`, `randkey0`, `randkey1`, `brating`, `bbattle`, `dlcs`,
`autosave`, `adviserassistant`, `teams`).

### 7.2 Per-player TMapPlayer-блоки

Header содержит 12 (= `gc_MaxPlayerCount`) последовательных блоков
record'а `TMapPlayer`. Поля одного блока в kv-stream идут в фикс-
порядке:

```
id, cid, csid, name, team, color, lanid,
startx, starty, aidifficulty,
bexists, bai, bhuman, bclosed, bready, bloaded, bleave,
(+ random-nation enable/options: sic, snX, si1..si3)
```

Парсер группирует kv-пары в блоки по появлению поля `id` (первое в
TMapPlayer), затем фильтрует `bexists != true`. Список оставшихся
существующих слотов и определяет engine'овый runtime `pid` каждого
игрока — **это позиция в bexists-фильтрованном списке, НЕ значение
поля `id`**. См. §11.1.

### 7.3 BMP-превью и стартовый снимок

- BMP-превью карты (~145 КБ) между `GameMapSnapShotBegin/End`.
- В первом entry body (`ts == 0`) лежит начальный снимок мира:
  стартовые юниты, ресурсные кластеры, шахты, fog. Этот entry
  отличается от остальных только размером и тем, что декодеру
  обычно нужен лишь как baseline.

### 7.4 Поток событий

Полный лог клиентских команд и серверных state-sync пакетов — см. §3.

### 7.5 Что НЕ хранится

- Чат и голос (возможно идут через `ReadPackage`, но в наблюдаемых
  потоках не зафиксированы).
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
| 10-байт entry-маркер (два варианта)   | b0 04 + (zero \| signature) + zero-tail; см. §2.2 |
| Имена и нации игроков                 | хранятся в TMapPlayer-блоках; см. §7.2, §11 |
| Хост-игрок в рейтинге                 | `brating=true` ⇒ host = color 0 (red); см. §11.2 |
| Class=0x09 three-way dispatch         | TaggedHandle / GameObject / Player ветки в `RecordCustomBeginTagObject @ 0x685c6c`; см. §3.2 |
| Порядок битов в bit-pack'е            | LSB-first (`_Stream_WriteBit @ 0x5b4874`); см. §3.3 |
| Парность begin/end в потоке           | через `+0x118` write stream — write вне begin/end молча no-op; см. §6 |

## 9. Открытые TBD

- Семантика middle-word альтернативного entry-маркера (вариант B
  из §2.2): откуда runtime берёт это значение и почему оно отличается
  у rated против saves. Подозрение — channel/session ID, выдаваемый
  match-сервером, но disasm `RecordCustomBegin` это не подтверждает.
- Точная схема variable-length записи class=`0x09` при размере
  больше 8 байт. Дополнительные поля выбираются битами `statestag`;
  таблица соответствия флагов и полей требует disasm
  `RecordCustomBeginTagObject` и связанных write-routine'ов.
- Формат `RecordCustomReadPackedFloat` / `WritePackedFloat`
  (`@ 0x6860ac` / `@ 0x6860c4`). Native существует, но в стандартных
  streams не наблюдается; вероятно, используется в `ReadSync` для
  упаковки координат и углов. Разовая декомпиляция тела даст
  раскладку (half-float, fixed-point с диапазоном, или delta-encoded).
- Тело engine-progress payload'ов (state_id'ы 0x08, 0x0a, 0x0f
  при pid=14). Layout отличается от script handler signature и
  записывается напрямую engine-кодом.
- `ReadSync` (state_id=`0x3b`). Сложная сигнатура (полный snapshot
  юнита со всеми ориентационными матрицами, hp, RNG-seed). В
  обычных replay'ях не наблюдается; вероятно, используется при
  initial-connect клиента к идущей игре.
- Идентификация host'а в не-рейтинговых играх. В рейтинге работает
  правило «color=0», но в LAN/private-lobby игроки свободно меняют
  цвета, и host-pid в файле не маркируется ничем явным.

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

---

## 11. Identification conventions

Соглашения о том, как из header'а и потока вытащить «кто есть кто».
Полезно для любого внешнего инструмента, которому нужно
сопоставить replay'у людей, нации и роль.

### 11.1 Runtime `pid` ≠ `TMapPlayer.id`

Engine'овый `pid`, который попадает в каждый sub-package, — это
**позиция игрока в bexists-фильтрованном списке слотов**, а не
значение `TMapPlayer.id`. То есть:

1. Собрать слоты в порядке появления в kv-stream.
2. Выкинуть слоты с `bexists != true` (закрытые / пустые).
3. У оставшихся `pid = индекс в этом отфильтрованном списке`.

Поле `TMapPlayer.id` хранится отдельно (видимо session/join id) и в
event payload'ах не используется. Эмпирически проверено: известные
читеры в `ex1.rep` ложатся именно на slot-order, а не на id-order.

### 11.2 Нация: `TMapPlayer.cid` как канонический источник

Поле `cid` в TMapPlayer-блоке — это country index `0..23`, который
маппится в nation sid через статическую таблицу (`NATION_BY_CID` в
парсере, она же `gc_country_*` в `country.script`):

| cid | sid   |  | cid | sid   |  | cid | sid   |  | cid | sid   |
|----:|-------|--|----:|-------|--|----:|-------|--|----:|-------|
| 0   | aus   |  | 6   | pol   |  | 12  | mis   |  | 18  | bav   |
| 1   | fra   |  | 7   | swe   |  | 13  | net   |  | 19  | hun   |
| 2   | eng   |  | 8   | pru   |  | 14  | den   |  | 20  | swi   |
| 3   | spa   |  | 9   | ven   |  | 15  | por   |  | 21  | sco   |
| 4   | rus   |  | 10  | tur   |  | 16  | pie   |  | 22  | tat   |
| 5   | ukr   |  | 11  | alg   |  | 17  | sax   |  | 23  | lit   |

Спец-значения:

- `cid = -2` — игрок выбрал «**Random nation**», итог зафиксирован
  при старте партии. В header'е итоговой нации нет — её надо вывести
  из первой `ReadConstruct`'а игрока (поле `cid` в payload — см.
  §3.1 / handler-table), либо из sid-префикса (с фильтром общих
  кластеров `eur*/rus*/tur*/spa*/por*/ukr*`).
- `cid = 24` — **закрытый слот** (`bexists` может остаться true для
  spectators / observer-стула, но играющего игрока нет).

В первых ReadConstruct'ах игрока payload тоже несёт `cid` — это
дополнительный канал той же информации, полезный для cid=-2 случая.

### 11.3 Host-игрок

В рейтинговых партиях (`brating = "true"` в settings) **host — это
игрок с `color = 0` (красный)**. Match-сервер при создании комнаты
назначает красный хосту, и в рейтинге игроки не могут поменять цвета.

В не-рейтинговых партиях (LAN, private lobby) это правило **не
работает** — игроки свободно меняют цвета в лобби, и host-pid нигде
явно не маркируется. Для анализа эксплойтов вроде double-upgrade
race-condition (которое физически возможно только у клиента, не
у хоста) это означает, что в не-рейтинговых replay'ях host
отфильтровать не получится — приходится мириться с возможными
false-positive'ами на действиях самого хоста.

Engine-источник: `GetKeyColorByPlayerIndex` в
[`lib/classes.script:7986`](C:\Program Files (x86)\Steam\steamapps\common\Cossacks 3\data\scripts\lib\classes.script)
красит индекс 0 в rgb(164, 0, 0).

### 11.4 Имена игроков

`TMapPlayer.name` — это display-имя (то, что игрок ввёл в профиле:
`[WhoT]Niotid`, `macaron`, `skipi_lon`). `TMapPlayer.lanid` — числовой
ID профиля от match-сервера, удобен как стабильный ключ при
агрегации статистики по игроку через много replay'ев.
