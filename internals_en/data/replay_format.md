<a id="replay--save-rep-map--формат-oswmap13"></a>
# Replay / Save (`.rep`, `.map`) - format `OSWMap13`

Cossacks 3 writes replays and saves in one binary format
`OSWMap13`. The file is a **snapshot of the world at the start and a stream of network
packets**, the same stream that the server sends to clients in
online game (see
[`../engine/server_sync_architecture.md`](../engine/server_sync_architecture.md)).

Replay playback in the engine is implemented through client code
network game path: each packet from the tape is parsed by the same
`Read*`-handler, which would work for the online client upon receipt
packet over the network. The server in replay mode does not calculate anything
(see `progress.inc:46`: `if (_net_IsClient or _net_IsReplay) then //
global do not progress`).

Parsers in this project:

- [`parser/parse_replay.py`](../../parser/parse_replay.py) — header
  and counting map patterns.
- [`parser/parse_replay_events.py`](../../parser/parse_replay_events.py)
  — complete analysis of the event flow, displays a JSON timeline.

---

<a id="1-общая-разметка-файла"></a>
## 1. General file markup
```
+--- Header (~168 KB) -------------------------------------+
| OSWMap13 + Build.Ver[X.Y.Z.NNNN] + UID                   |
| GameMapSnapShotBegin                                     |
|   [BMP, ~145 KB — map preview]                           |
| GameMapSnapShotEnd                                       |
| GameMapRecordBegin                                       |
|   <key,value> pairs in text format:                      |
|     maskname, mapsize, relieftype, randkey0, randkey1,   |
|     terraintype, season, gamespeed, resourcemines,       |
|     limit, ver, ...                                      |
+--- Body ---------------------------------------------- ---+
| Entry stream with timestamps and payloads:               |
|   entry[0]:   ts=0,         payload = initial-world      |
|                              snapshot (units, resources) |
|   entry[1+]:  ts > 0 ticks, payload = one or more        |
|                              sub-packages                |
| GameMapRecordEnd                                         |
+----------------------------------------------------------+
| GameMapBegin + f64 elapsed_raw_s + map metadata          |
| map_file + width/height + init-state + GameMapEnd         |
+----------------------------------------------------------+
```
Headers and kv-pairs are parsed directly as long-prefix ASCII strings.
The body is a sequence of entry blocks; the decoder must pass
to the marker `GameMapRecordEnd` and do not try to parse the footer as entry.
A confirmed footer diagram is given in §7.5.

---

<a id="2-entry-18-байтовый-заголовок-и-payload"></a>
## 2. Entry: 18-byte header and payload
```
offset  size  field                                   note
---------------------------------------------------------------------
+0      4B    float ts                                ticks; see §2.1
+4      4B    u32 payload_size LE                     payload size
+8     10B    entry marker                            see §2.2
+18    N      payload                                  N = payload_size
```
<a id="21-семантика-ts"></a>
### 2.1 Semantics `ts`

`ts` are game ticks in increments of 0.1 g-sec:
```
g_sec = ts / 10
```
The 0.1 g-sec step is kept constant for all game speeds: at
any value lobby-`gamespeed` relation
`ticks_per_real_sec / game_factor` is always equal to 10:

| `gamespeed` | `gc_settings_gamespeed_N` (ticks/real-sec) | factor | g-sec/tick |
|------------|:------------------------------------------:|:------:|:----------:|
| Slow | 7 | 0.7 | 0.1 |
| Normal | 10 | 1.0 | 0.1 |
| Fast | 14 | 1.4 | 0.1 |

The values of `ts` are fractional (for example, 14.130 instead of 14.1) because
the engine writes `GetCurrentTime × GetTimeSpeedFactor` with full
float precision, rather than rounding to a whole tick.

<a id="22-десятибайтовый-entry-маркер--два-варианта"></a>
### 2.2 Ten-byte entry marker - two options

Each entry in body is preceded by a 10-byte sequence.
TWO options are observed; separates their middle-word state:
```
variant A (saves and local replays):
  b0 04 00 00 00 00 00 00 00 00

variant B (rated/online matches):
  b0 04 <4B signature> 00 00 00 00
                       ^^^^^^^^^^^ tail remains zero
         ^^^^^^^^^^^^^ nonzero word, CONSTANT within one file
```
Invariants that walker relies on:

- The first 2 bytes are always `b0 04`.
- The last 4 bytes are always zeros.
- Middle-word (offset +2 from the beginning of the marker) can be zero or
  non-zero, but within one file it is constant - this is a signature
  thread, issued when `RecordCustomBegin`-init.

Walker should scan prefix `b0 04` and accept any 10 bytes,
for which last-4 == 0. Old decoders that checked the entire token
literally, 98% of entries were lost on rated replays - exactly that entry-
the stream through which the server issues client commands.

The semantics of middle-word have not yet been analyzed. `0x04b0 = 1200` occurs
in the exe code 99 times as a 16-bit operand, but as a 10-byte sequence not
present - the marker is generated by runtime from engine-internal
structs (`RecordCustomBegin` → channel-table).

---

<a id="3-sub-package-внутренняя-структура-payloadа"></a>
## 3. Sub-package: internal payload structure

One entry contains one or more sub-packages
(see native `RecordPackagesCount`, `RecordPackagesCursor`). When recording
each sub-package is wrapped in a pair `RecordCustomBegin(stateName) /
RecordCustomEnd`; when reading, the engine dispatches the package to the FSM section
with the name `stateName` through `SwitchTo(stateName)`.

<a id="31-class0x00-default-channel--формат"></a>
### 3.1 Class=0x00 (default channel) - format
```
offset  size  field                                   note
---------------------------------------------------------------------
+0      4B    [class=0x00, sub=0x03, pid, state_id]   4-byte header
+4      1B    0x00                                    begin marker
+5      ?B    typed body                              typed stream
+?      1B    0x01                                    end marker
```
This format is used for player commands (build, produce, move,
trade, ...) and for engine-progress events (see §3.5). Channel ID 0x03
- this is `RecordCustomBegin` (default channel, see §6).

**Pid mapping** (`dmscript.global`):

| pid | role |
|-------:|-------------------------------------------------------|
| 0..11 | real players (`gc_MaxPlayerCount = 12`) |
| 12 | `gc_playerind_env` |
| 13 | `gc_playerind_misc` |
| 14 | `gc_playerind_progress` – engine progress events |
| 15 | `gc_playerind_pool` |

<a id="32-class0x09-tagobject-state-sync-stream--формат"></a>
### 3.2 Class=0x09 (TagObject state-sync stream) - format

Channel per-object state-sync (`RecordCustomBeginTagObject @ 0x685c6c`)
written in a different scheme:
```
offset  size  field
------------------------------------------------------
+0      1B    0x09                       — class
+1      3B    u24 LE — global sequence counter (monotonic)
+4      4B    u32 LE — record count
+8      ?B    count variable-size records
```
The record size varies from 8 to 23 bytes in increments of ~3 bytes. Basic
part `[u32 uid][u32 statestag]` (8 bytes) is always present;
extensions are added by bits `statestag`.

<a id="three-way-dispatch--три-подформата-записи"></a>
#### Three-way dispatch - three record subformats

Decompilation of `RecordCustomBeginTagObject` (private recon-workspace
`cossacks-deep/decompiled/record.c:286-338`, cross note -
`cossacks-deep/findings/record_sync.md`) reveals that one and the same
class=0x09 channel carries three different sub-formats, selected by
the type of the passed handle. The engine sequentially tries three
classifications:

| Category | resolver | Source state_record | handle sign |
|----------------|-----------------------|------------------------|----------------------------|
| `TaggedHandle` (SM state) | `ResolveTaggedHandle` | `obj + 0x18` (variables collection) | high bits `0x8000` in both halves of handle |
| `GameObject` | `ValidateGameObjectHandle` | `FUN_007c32ec(go)` (sync-context accessor) | passes `ValidateGameObjectHandle` |
| `Player` | `ValidatePlayerHandle` | `obj + 0x24` (player.sync_field) | passes `ValidatePlayerHandle` |

All three paths end up being called `_RecordManager_BeginTagWrite` with different
state-record, so a set of serialized fields in records
class=0x09 depends on *what object was tagged when writing*.

A parser that tries to decode all class=0x09 records into one
scheme will periodically get confused. A correct decoder should
first dispatch by marker at the beginning of the record
(it is not yet clear which byte carries the tag category), and
apply different layouts to Tagged-SM / GameObject / Player streams.

In replay-parser's practice, it is easier to leave class=0x09 as “count
records, the body cannot be decoded” - almost the entire useful signal lies
in class=0x00 commands, and the sync stream is gigantic (millions of records in
long batch) and its decomposition slows down the parser by an order of magnitude.

<a id="33-типизированные-recordcustomread-примитивы"></a>
### 3.3 Typed `RecordCustomRead*` primitives
```
RecordCustomReadBoolean   — 1 byte (any nonzero value = true)
RecordCustomReadByte      — 1 byte
RecordCustomReadWord      — 2 bytes LE
RecordCustomReadSmallInt  — 2 bytes LE signed
RecordCustomReadInt24     — 3 bytes LE signed
RecordCustomReadInteger   — 4 bytes LE signed
RecordCustomReadFloat     — 4 bytes LE IEEE-754
RecordCustomReadString    — [u16 len LE][bytes]
RecordCustomReadShortString — [u8 len][bytes]
RecordCustomReadPackedFloat — 2-byte uint16 LE; decode = min + (raw/65535)*(max-min); min/max are not in the stream and come from the record context (see below)
RecordCustomReadBit + RecordCustomBeginReadBitFields — for bit streams
```
<a id="packedfloat--2-байта-uint16"></a>
#### `PackedFloat` - 2 bytes uint16

Confirmed by decompilation `_Stream_WritePackedFloat @ 0x5b46e0`
(private `cossacks-deep/decompiled/record.c` + `findings/record_sync.md`).
Engine-side:
```c
normalized = clamp((value - min) / (max - min), 0, 1);
write_u16_le(round(normalized * 65535));
```
Decode in the parser (`Reader.packed_float(min, max)` in
`parser/parse_replay_events.py`):
```python
raw = read_u16_le()
value = min + (raw / 65535.0) * (max - min)
```
**Important subtlety.** `min/max` **are not written to the stream**. They
**implied** use-site - every call
`RecordCustomWritePackedFloat(value, min, max)` uses its
constants. To correctly decode a specific PackedFloat field,
the parser must know what range was used when recording.
In practice, this means the table “state X, field Y → min=N, max=M”.

<a id="строки"></a>
#### Lines

`String` is just `[u16 len LE][bytes]`, no prefix. For example,
sid `"auscen"` in payload looks like:
```
06 00                          u16 len = 6
61 75 73 63 65 6e              "auscen"
```
<a id="bitfield-order--lsb-first"></a>
#### Bitfield order - LSB-first

Inside the bit-pack (`BeginBitFields … WriteBit × N … EndBitFields`)
bits are packed LSB-first. Decompilation
`_Stream_WriteBit @ 0x5b4874` (private recon-workspace
`cossacks-deep/decompiled/record.c:728-745`):
```c
*(byte *)(stream + 0x14) |= *(byte *)(stream + 0x15);  // OR the mask into the current byte
*(byte *)(stream + 0x15) <<= 1;                         // mask <<= 1
```
Mask starts from the value `0x01` and shifts to the left after each
recorded bit. This means: the first `WriteBit(true)` sets the bit
`0x01`, the second - `0x02`, and so on. On reading (`ReadBit`) parser
must repeat the same logic - otherwise all packed bools will unfold
in mirror order.

With `EndBitFields`, the partial byte is aligned to an integer, mask
reset. That is, the length of the bit-pack in the stream is `ceil(N_bits / 8)`
byte, not compressed to a bit.

`Int24` confirmed as 3 bytes LE signed (`RecordCustomWriteInt24 @
0x6860d4` uses `_Stream_WriteByte × 3` unsigned extend
at upper-byte).

### 3.4 Multi-package entry

One entry often contains several sub-packages. After
end-marker `0x01` goes immediately or `0x00 0x03 [pid] [state_id] 0x00`
(beginning of the next class=0x00 sub-package), or `0x09 [u24 seq]`
(class=0x09 TagObject-record). The decoder must recognize both forms.

Example: request to construct a building (`ReadConstruct`) usually
accompanied by one `class=0x09`-record - server state-tag
for the created construction dummy. Command `ReadProduce` to deep center
generates several nested `ReadNew` for each
mercenary candidate.

<a id="35-engine-progress-события-pid14"></a>
### 3.5 Engine-progress events (pid=14)

When pid=14 (`gc_playerind_progress`) state_ids are used as
**tags of FSM transitions of the engine**, and not as dispatchers of handlers.
The body of such a sub-package **does not correspond** to the signature of the script
handler with the same state_id; instead the engine writes compact
delta of its own state.

The three most common engine-progress state_ids (according to empirical data):

- `0x08` (`ReadSquadListAction`) — periodic squad-bookkeeping batch
- `0x0a` (`WriteMove`) — server-side broadcast of movement orders
- `0x0f` (`ReadFree`) — periodic cleanup of outdated objects

The decoder SHOULD skip the body of such events, marking them as
`engine_<state_name>`.

---

<a id="4-карта-stateid--handler"></a>
## 4. Map state_id → handler

**Source:** `data/scripts/units/global.aix`
describes FSM sections in boot order. **`state_id` matches
section index** in the file (including separators and `section.end`).

| state_id | section name | note |
|---------:|----------------------------|----------------------------------------|
| `0x00` | `Initial` | initial state FSM |
| `0x01` | `OnBeforeSave` |                                         |
| `0x02` | `OnAfterLoad` |                                         |
| `0x03` | `Progress` | per-player progress tick |
| `0x05` | `WriteSquadNew` |                                         |
| `0x06` | `ReadSquadNew` | creation of formation |
| `0x07` | `WriteSquadListAction` |                                         |
| `0x08` | `ReadSquadListAction` | action on the list of squads |
| `0x0a` | `WriteMove` | server broadcasts move |
| `0x0b` | `ReadMove` | per-unit destination + facing |
| `0x0c` | `WriteNew` |                                         |
| `0x0d` | `ReadNew` | spawn unit from server |
| `0x0e` | `WriteFree` |                                         |
| `0x0f` | `ReadFree` | object deletion |
| `0x10` | `WriteDeath` |                                         |
| `0x11` | `ReadDeath` | unit death (with RNG seed restore) |
| `0x12` | `WritePlayer` |                                         |
| `0x13` | `ReadPlayer` | change of ownership (takeover) |
| `0x14` | `WriteRally` |                                         |
| `0x15` | `ReadRally` | rally-point on the building |
| `0x16` | `WriteOrder` |                                         |
| `0x17` | `ReadOrder` | order (build/gainres/attackobj/...) |
| `0x18` | `WriteUpgrade` |                                         |
| `0x19` | `ReadUpgrade` | start/cancel research |
| `0x1a` | `WriteProduce` |                                         |
| `0x1b` | `ReadProduce` | queue for unit production |
| `0x1c` | `WriteSearch` |                                         |
| `0x1d` | `ReadSearch` | switch search-enemy |
| `0x1e` | `WriteStand` |                                         |
| `0x1f` | `ReadStand` | switching stand-ground |
| `0x20` | `WriteConstruct` |                                         |
| `0x21` | `ReadConstruct` | building construction order |
| `0x22` | `WriteApply` |                                         |
| `0x23` | `ReadApply` | applying a completed upgrade |
| `0x24` | `WriteLeaveOrder` |                                         |
| `0x25` | `ReadLeaveOrder` | list of units to exit the building |
| `0x26` | `WriteLeave` |                                         |
| `0x27` | `ReadLeave` | unit exiting the building |
| `0x28` | `WriteProj` |                                         |
| `0x29` | `ReadProj` | projectile shot |
| `0x2a` | `WriteProjFree` |                                         |
| `0x2b` | `ReadProjFree` | destruction of the projectile |
| `0x2c` | `WriteNewP` |                                         |
| `0x2d` | `ReadNewP` | spawn primitive (fields, balls, ship-dummy)|
| `0x2e` | `WriteStop` |                                         |
| `0x2f` | `ReadStop` | canceling orders |
| `0x30` | `WriteTrade` |                                         |
| `0x31` | `ReadTrade` | trading on the market |
| `0x32` | `WriteWall` |                                         |
| `0x33` | `ReadWall` | construction of a wall cluster |
| `0x34` | `WriteGate` |                                         |
| `0x35` | `ReadGate` | open/close gate |
| `0x36` | `WriteFreeList` |                                         |
| `0x37` | `ReadFreeList` | mass deletion of objects |
| `0x38` | `WritePeaceTime` |                                         |
| `0x39` | `ReadPeaceTime` | switching peace-mode |
| `0x3a` | `WriteSync` |                                         |
| `0x3b` | `ReadSync` | full unit snapshot |
| `0x3c` | `WriteSyncUnitsParams` |                                         |
| `0x3d` | `ReadSyncUnitsParams` | HP synchronization for a group of units |
| `0x3f` | `WritePackage` |                                         |
| `0x40` | `ReadPackage` | arbitrary text net message |
| `0x42` | `ProgressAI` | engine internal |
| `0x43` | `ProgressEconomicAI` | engine internal |
| `0x44` | `ProgressWarAI` | engine internal |
| `0x45` | `CheckErrors` | engine internal |
| `0x46` | `ReadTradeResources` | transfer of resources to an ally |
| `0x47` | `WriteTradeResources` |                                         |

State_ids 0x04, 0x09, 0x12, 0x3e, 0x41 are separator records
(`Name = ----------------------` to `global.aix`), they are not
associated with the handler.

The signatures of all `Read*`-handlers are read from
`data/scripts/units/global.inc/read*.inc`.

<a id="41-сигнатуры-тел-ключевых-handlerов"></a>
### 4.1 Body signatures of key handlers

Parameters in order of recording. Types are `RecordCustomRead*` primitives
from §3.3. These six handlers cover almost all command analysis
player.
```
ReadConstruct   (0x21)  Bool bFromServer
                        Int  cid                 ← player's country index
                        Str  sid                 ← building sid
                        Float posx, posz
                        Bool clrord
                        Int  count
                        Int[count] builder-uids

ReadNew         (0x0d)  Bool bFromServer
                        Str  race, base
                        Float posx, posz
                        Int  cid                 ← cid≤0 → -cid = country;
                                                   cid>0 → producing-building uid
                        Int  uid, num

ReadNewP        (0x2d)  Bool bFromServer
                        Str  race, base
                        Float posx, posz, roll
                        Int  plind, id, uid, num

ReadOrder       (0x17)  Int  ordtyp              ← see §5
                        Int  taruid
                        Bool clrord, locktrg
                        Int  number
                        Float posx, posz         ← only when ordtyp ∈ {5,6}
                        Int[number] unit-uids

ReadProduce     (0x1b)  Int  proid               ← index in country.members[]
                        Int  prcid               ← unit's country index
                        Int  amount              ← -1 = infinite queue
                        Bool state               ← start / cancel
                        Int  count
                        Int[count] building-uids

ReadUpgrade     (0x19)  Bool bFromServer
                        Int  upgid               ← index in gCountry[cid].upgrade[]
                        Bool state               ← start / cancel
                        Int  count
                        Int[count] building-uids

ReadApply       (0x23)  Int  plind, uid          ← target
                        Int  cid, ind            ← gCountry[cid].upgrade[ind]
```
Semantic notes:

- **`ReadProduce.proid`** is the index in the ordered list
  members of the nation (`_country_AddMember` to `country.script`).
  Explanation: `country_members[NATION_BY_CID[prcid]][proid] = sid`.
  The list of members is extracted by the upgrade simulator in
  `derived/country_members.json`.
- **`ReadUpgrade.upgid` and `ReadApply.ind`** - index in
  `gCountry[cid].upgrade[]`. Engine builds this array at `_country_Init`
  (with inline-call `_country_InitUnitsUpgrades`), calling
  `SetUpgStruct` / `AddUpgradePack` / `_country_AddUpgrade` by fixed
  in order. Parser in [`parser/simulate_upgrades.py`](../../parser/simulate_upgrades.py)
  repeats the same sequence and issues `data.json :: upgrades`
  with an ordered per-nation list - list-index in it is equal to
  `upgid`/`ind`. Without the correct order `upgid=2` will be false
  point to "barracks" rather than to the mill.
- **`ReadConstruct.cid`** — country index of the player (same as
  `TMapPlayer.cid`, see §11.2). Useful for determining the nation when
  in TMapPlayer it is `cid=-2` (random) and the nation is unknown in advance.

---

<a id="5-gcobjordertype--типы-приказов-в-readorder"></a>
## 5. `gc_obj_order_type_*` - types of orders in `ReadOrder`

Values from `dmscript.global:630-650`:

| code | name | meaning |
|----:|----------|-------------------------------------------------|
| 0 | `none` | no order |
| 1 | `move` | movement |
| 2 | `attackobj` | attack a specific unit/building |
| 3 | `gainres` | collect resource |
| 4 | `produce` | produce (internal) |
| 5 | `patrol` | patrol |
| 6 | `attackpoint` | attack point |
| 7 | `continueattackpoint`| continue attackpoint |
| 8 | `performupgrade` | upgrade in progress |
| 9 | `fishing` | fishing |
| 10 | `creategates` | create a gate in the wall |
| 11 | `buildwallcontinue` | continue building the wall |
| 12 | `buildwall` | build a wall |
| 13 | `gotomine` | enter the mine |
| 14 | `gototransport` | enter transport |
| 15 | `leavetransport` | get out of transport |
| 16 | `leavebuilding` | leave the building |
| 17 | `build` | builder goes to construction site |
| 18 | `guard` | to guard |
| 19 | `repair` | to repair |
| 20 | `exitunits` | output of units |

In `ReadOrder` with `ordtyp ∈ {patrol=5, attackpoint=6}` after the field
`number` there are two additional `Float`'s `posx, posz` - period
order. For other values, coordinates are not written.

Real **right-click-on-dot** go not through `ReadOrder`, but through
separate handler `ReadMove` (state_id=`0x0b`). `ordtyp=1 (move)` in
`ReadOrder` is extremely rare in practice.

---

<a id="6-каналы-записи"></a>
## 6. Recording channels

The Native API exports five channel variants `RecordCustomBegin*`.
Disassembly `RecordCustomBegin` (VA `0x685c38`, implementation
`0x733590`) indicates that **second byte of the sub-package** is
channel ID selected from the comparison table:

| channel ID | native API |
|-----------:|-------------------------------------|
| 1 | `RecordCustomBeginMap` |
| 2 | (reserved/internal) |
| **3** | **`RecordCustomBegin`** (default) |
| 4 | `RecordCustomBeginStateMachine` |
| 5 | `RecordCustomBeginTagObject` |

For the default channel this gives the sub-package's observable prefix
`00 03 [pid] [state_id]`:

- byte 0 = `0x00` — hardcoded begin-marker
- byte 1 = `0x03` — channel ID (default)
- bytes 2-3 - packed `pid` and `state_id`

Class=`0x09` sub-package is TagObject channel; its first byte
has a fixed value `0x09`, and its recording scheme is
is different (see §3.2): the engine writes per-object state deltas in
compact form.

Reference addresses in `cossacks.exe` for further research:
`RecordCustomBegin = VA 0x685c38`, implementation = `0x733590`,
`WriteBytes = 0x5b4620`, channel-tables `0x789980` (Map),
`0x7c3160`, `0x7af5e8`.

<a id="current-write-stream--проверка-парности"></a>
#### Current write stream + parity check

The layout of the `RecordManager` structure was revealed by decompilation of record.c
(private recon-workspace `cossacks-deep/decompiled/record.c` plus
review `cossacks-deep/findings/record_sync.md`). All
`RecordCustomWrite*` - primitives read the pointer before serialization
to the current buffer at:
```
*(int*)(*(int*)(root + 0x4c) + 0x6c) + 0x118
                 │              │     │
                 │              │     └── current write stream (ptr)
                 │              └──────── RecordManager
                 └─────────────────────── main sub-manager
```
If `+0x118` is NULL, the write operation silently writes nothing.
This means that the **valid replay stream must contain paired
begin/end entries**: `RecordCustomBegin*` initializes stream,
`RecordCustomEnd` (`@ 0x685e00`) resets it, and any
write calls between them go into the buffer, but after end they don’t.

Applied consequences for the parser:

- The flow of sub-packages in one entry is arranged as follows:
  "begin → body → end → begin → body → end...", end-marker `0x01`
  in class=0x00 is a runtime-side confirmation that
  `RecordCustomEnd` is executed and stream is closed.
- If the decoder encounters the situation “several begin’s in a row
  without end" - these are either nested begin's (TagObject inside SM),
  or a damaged file. There are no attachments in the observed replays
  noticed: TagObject is always a separate sub-package.
- `recordEnabled` / `recordGroupEnabled` / `recordInitializeEnabled`
  flags in RecordManager (`+0x130`, `+0x131`, `+0x132`) can
  reset stream on the fly; initial snapshot (entry with `ts == 0`)
  written with `recordInitializeEnabled = true`.

---

<a id="7-что-хранится-в-headerе"></a>
## 7. What is stored in the header

### 7.1 Lobby settings

All fields `gMap.settings.*` are written in the kv-stream header in the text
shape (`[u32 keylen][key][u32 vallen][val]`, little-endian length). Full list (names ↔
meaning) - in [`docs/recon/world/map/game_settings.md`](../../docs_en/recon/world/map/game_settings.md);
canonical enum labels → `derived/game_settings.json`. This includes
all party rules (`peacetime`, `century18`, `capture`, `marketdip`,
`cannons`, `balloon`, `startingunits`, `resourcestart`, `gamespeed`,
`resourcemines`, `terraintype`, `relieftype`, `season`, `limit`,
`maskname`, `randkey0`, `randkey1`, `brating`, `bbattle`, `dlcs`,
`autosave`, `adviserassistant`, `teams`).

<a id="72-per-player-tmapplayer-блоки"></a>
### 7.2 Per-player TMapPlayer blocks

Header contains 12 (= `gc_MaxPlayerCount`) consecutive blocks
record `TMapPlayer`. The fields of one block in kv-stream go to a fixed
order:
```
id, cid, csid, name, team, color, lanid,
startx, starty, aidifficulty,
bexists, bai, bhuman, bclosed, bready, bloaded, bleave,
(+ random-nation enable/options: sic, snX, si1..si3)
```
The parser groups kv-pairs into blocks based on the appearance of the `id` field (the first in
TMapPlayer), then filters `bexists != true`. List of remaining
existing slots and determines the engine runtime `pid` of each
player - **this is the position in the bexists-filtered list, NOT the value
fields `id`**. See §11.1.

<a id="73-bmp-превью-и-стартовый-снимок"></a>
### 7.3 BMP preview and starting snapshot

- BMP map preview (~145 KB) between `GameMapSnapShotBegin/End`.
- The first entry body (`ts == 0`) contains the initial snapshot of the world:
  starting units, resource clusters, mines, fog. This entry
  differs from the others only in size and in that the decoder
  usually needed only as a baseline.
- Duplicate record hypothesis published by a third party tool
  `[f32 x][f32 y][u16 id][20 00 1a][u32 flag]` (actually 17, not
  16 bytes) was not reproduced in a sample of 25 replays. Canonical
  it is not considered part of the starting-snapshot schema.

<a id="74-patternlist-имена-и-координаты-размещённых-паттернов"></a>
### 7.4 PatternList: names and coordinates of placed patterns

After the LP marker `PatternList` there are successive text kv-triples:
```
[u32 1] "n" [u32 name_len] pattern_name
[u32 1] "x" [u32 x_len]    x_ascii
[u32 1] "y" [u32 y_len]    y_ascii
```
`n` is the name of the pattern file selected by the generator, `x` and `y` are its
coordinates on the map, serialized as ASCII numbers (usually integers, in
including negative ones). The triple must be adjacent: separate
the keys `n`, `x` or `y` outside `PatternList` are not a placement record.

The schema was confirmed on 25 replays: from 62 entries on a 256×256 map to
1,291 on a 640×640 map. `parser/parse_replay.py` returns them through
`extract_pattern_placements()` and JSON field `pattern_placements`.

<a id="75-футер-после-gamemaprecordend"></a>
### 7.5 Footer after GameMapRecordEnd

In all 25 tested replays, immediately after the end of the entry stream there is
same frame:
```
[LP]  "GameMapRecordEnd"
[LP]  "GameMapBegin"
[f64] elapsed_raw_s
[u32] reserved0                  // 0 in the verified sample
[LP]  project_name               // "cossacks"
[LP]  project_path               // data\projects\project.main.prj
[...] padding / unread fields
[LP]  map_file                   // game_v....map
[LP]  "Default"
[LP]  "Default"
[u32] map_width
[u32] map_height
[u32] map_flags
[...] unread fields
[LP]  menu_config                // .\data\gui\menu.cfg
[LP]  light                      // light0
[LP]  "InitMapGen"
[LP]  player_state               // playerN
[LP]  "GameMapEnd"
```
The map sizes in the sample are 256x256, 320x320, 480x480 and 640x640; they are not allowed
hardcoding one example at a time. `elapsed_raw_s` - finite non-negative
time-like value, but it **does not match** the duration of the stream
`last_ts / 10`. Until the clock semantics are established, this field cannot be
substitute `duration_g_sec`.

Parser `parse_footer()` returns confirmed fields and marks the footer
`complete=true` only when `GameMapEnd` is found.

The leads on `PatternList` and the footer frame were checked against
[`czanchetta/cossacks3-replay-tools`](https://github.com/czanchetta/cossacks3-replay-tools/blob/main/docs/FORMATO_REP_COSSACKS3.md),
after which they were independently tested on a local sample. Code from external
the repository was not migrated; snapshot's unconfirmed hypothesis is rejected.

<a id="76-поток-событий"></a>
### 7.6 Event flow

Full log of client commands and server state-sync packages - see §3.

<a id="77-что-не-хранится"></a>
### 7.7 What is NOT stored

- Chat and voice (possibly going through `ReadPackage`, but in observable
  threads are not recorded).
- ELO and rating - come separately from the Steam match server.

---

<a id="8-закрытые-tbd"></a>
## 8. Closed TBDs

| TBD | Closed as |
|---------------------------------------|------------------------------------------|
| Semantics `ts` | ticks × 0.1 = g-sec |
| Pid byte interpretation | `gc_playerind_progress=14` and others |
| Sub-package header layout | 4B header + 0x00 begin + body + 0x01 end |
| String encoding | `[u16 len][bytes]`, no prefix |
| Multi-package boundaries | through end-marker `0x01` and recognition of `00 03` start of the next sub-pkg |
| Class=0x09 layout | `[09][u24 seq][u32 count][records]` |
| Full map state_id | via section's index in `global.aix` |
| Read*/Write* distinction | Read and Write go alternately in `global.aix` |
| Recording channels | from disasm `RecordCustomBegin` (§6) |
| Semantics engine pid=14 events | state_id is used as an FSM transition label, payload is engine-internal |
| 10-byte entry marker (two options) | b0 04 + (zero \| signature) + zero-tail; see §2.2 |
| Names and nations of players | stored in TMapPlayer blocks; see §7.2, §11 |
| Host player ranked | `brating=true` ⇒ host = color 0 (red); see §11.2 |
| Class=0x09 three-way dispatch | TaggedHandle/GameObject/Player branches in `RecordCustomBeginTagObject @ 0x685c6c`; see §3.2 |
| Bit order in bit-pack | LSB-first (`_Stream_WriteBit @ 0x5b4874`); see §3.3 |
| begin/end pairing in stream | via `+0x118` write stream - write outside begin/end silently no-op; see §6 |
| PatternList placement records | adjacent LP-kv triples `n`/`x`/`y`; see §7.4 |
| replay footer frame | `GameMapBegin` → map metadata → `GameMapEnd`; see §7.5 |

<a id="9-открытые-tbd"></a>
## 9. Open TBDs

- Semantics of the middle-word of the alternative entry marker (option B
  from §2.2): where does runtime get this value and why is it different
  rated vs saves. Suspicion - channel/session ID issued by
  match server, but disasm `RecordCustomBegin` does not confirm this.
- Exact scheme of variable-length record class=`0x09` with size
  more than 8 bytes. Additional fields are selected by bits `statestag`;
  table of correspondence between flags and fields requires disasm
  `RecordCustomBeginTagObject` and related write-routines.
- Format `RecordCustomReadPackedFloat` / `WritePackedFloat`
(`@ 0x6860ac` / `@ 0x6860c4`). Native exists, but in standard
  streams is not observed; probably used in `ReadSync` for
  packing of coordinates and angles. A one-time decompilation of the body will give
  layout (half-float, fixed-point with range, or delta-encoded).
- Body of engine-progress payloads (state_ids 0x08, 0x0a, 0x0f
  at pid=14). Layout is different from script handler signature and
  written directly by the engine code.
- `ReadSync` (state_id=`0x3b`). Complex signature (full snapshot
  unit with all orientation matrices, hp, RNG-seed). B
  there are no regular replays; probably used for
  initial-connect the client to the running game.
- Host identification in non-rated games. Works in the rating
  the rule is “color=0”, but in LAN/private-lobby players can freely change
  colors, and the host-pid in the file is not marked with anything obvious.
- The exact semantics of the footer field `elapsed_raw_s`: the value is time-like, but
  not equal to game time `last_ts / 10`; wall-clock possible,
  pause-aware or engine-lifetime clock.
- Exact binary scheme of the initial entry (`ts == 0`). Hypothesis about
  17-byte record with delimiter `20 00 1a` on 25 replays is not
  reproduced.

---

<a id="10-связь-с-другими-документами"></a>
## 10. Relationship with other documents

- [`../engine/server_sync_architecture.md`](../engine/server_sync_architecture.md)
  — network architecture C3.
- [`../engine/server_sync_packet_format.md`](../engine/server_sync_packet_format.md)
  - binary `EconomyPackage`.
- [`../engine/ticks_and_subticks.md`](../engine/ticks_and_subticks.md)
  — `GetGameTime`, `GetCurrentTime`, `GetTimeSpeedFactor`.
- [`../engine/native_api.md`](../engine/native_api.md) - catalog
  `RecordCustom*`-primitives.
- [`../scripts/structure.md`](../scripts/structure.md) - format
  FSM sections in `read*.inc`/`write*.inc`.
- [`../engine/rng_implementation.md`](../engine/rng_implementation.md)
  — `uniqrnd` (per-object RNG seed), synchronized in `ReadSync`
  and `ReadDeath`.

---

## 11. Identification conventions

Agreements on how to extract “who is who” from the header and stream.
Useful for any external tool that needs
compare the replay of people, nations and roles.

### 11.1 Runtime `pid` ≠ `TMapPlayer.id`

Engine `pid`, which goes into each sub-package, is
**player position in the bexists-filtered list of slots**, not
value `TMapPlayer.id`. That is:

1. Collect slots in the order of appearance in kv-stream.
2. Throw out slots with `bexists != true` (closed / empty).
3. For the remaining `pid = index in this filtered list`.

The `TMapPlayer.id` field is stored separately (apparently session/join id) and in
event payloads are not used. Empirically tested: known
cheaters in `ex1.rep` fall specifically on the slot-order, and not on the id-order.

<a id="112-нация-tmapplayercid-как-канонический-источник"></a>
### 11.2 Nation: `TMapPlayer.cid` as canonical source

The `cid` field in the TMapPlayer block is the country index `0..23`, which
mapped to nation sid through a static table (`NATION_BY_CID` in
parser, also known as `gc_country_*` in `country.script`):

| cid | sid |  | cid | sid |  | cid | sid |  | cid | sid |
|----:|-------|--|----:|-------|--|----:|-------|--|----:|-------|
| 0 | aus |  | 6 | pol |  | 12 | mis |  | 18 | bav |
| 1 | fra |  | 7 | swe |  | 13 | net |  | 19 | hun |
| 2 | eng |  | 8 | pru |  | 14 | den |  | 20 | swi |
| 3 | spa |  | 9 | ven |  | 15 | por |  | 21 | sco |
| 4 | rus |  | 10 | tur |  | 16 | pie |  | 22 | tat |
| 5 | ukr |  | 11 | alg |  | 17 | sax |  | 23 | lit |

Special meanings:

- `cid = -2` - the player chose “**Random nation**”, the result is fixed
at the start of the game. There is no final nation in the header - it must be displayed
  from the player’s first `ReadConstruct` (field `cid` in payload - see.
  §3.1 / handler-table), or from the sid prefix (with a general filter
  clusters `eur*/rus*/tur*/spa*/por*/ukr*`).
- `cid = 24` - **closed slot** (`bexists` may remain true for
  spectators / observer-chair, but there is no playing player).

In the first ReadConstructs of the player, the payload also carries `cid` - this
an additional channel of the same information, useful for cid=-2 cases.

<a id="113-host-игрок"></a>
### 11.3 Host player

In rating games (`brating = "true"` in settings) **host is
player with `color = 0` (red)**. Match server when creating a room
assigns red to the host, and players cannot change colors in the ranking.

In non-rated games (LAN, private lobby) this rule **is not
works** - players freely change colors in the lobby, and host-pid is nowhere
not clearly marked. For analyzing exploits like double-upgrade
race-condition (which is physically possible only for the client, not
at the host) this means that in non-rated replays the host
you won’t be able to filter - you have to put up with possible
false-positives based on the actions of the host itself.

Engine-source: `GetKeyColorByPlayerIndex` in
`lib/classes.script:7986`
paints index 0 in rgb(164, 0, 0).

<a id="114-имена-игроков"></a>
### 11.4 Player names

`TMapPlayer.name` is the display name (what the player entered in the profile:
`[WhoT]Niotid`, `macaron`, `skipi_lon`). `TMapPlayer.lanid` - numeric
Profile ID from the match server, convenient as a stable key for
aggregation of statistics for a player through many replays.
