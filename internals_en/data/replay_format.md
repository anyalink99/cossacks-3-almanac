<a id="replay--save-rep-map--формат-oswmap13"></a>
# Replay and Save Files (`.rep`, `.map`): `OSWMap13`

Cossacks 3 uses the same `OSWMap13` binary format for replays and saves.
Each file contains **an initial world snapshot followed by a stream of
network packets**—the same packet stream that the server sends to clients
during an online match (see
[`../engine/server_sync_architecture.md`](../engine/server_sync_architecture.md)).

Replay playback reuses the network client's code path: each recorded packet
is passed to the same `Read*` handler that would process it on receipt from
the network. Replay mode does not run server-side simulation (see
`progress.inc:46`:
`if (_net_IsClient or _net_IsReplay) then // global do not progress`).

Parsers in this project:

- [`parser/parse_replay.py`](../../parser/parse_replay.py) — parses the
  header and counts map patterns.
- [`parser/parse_replay_events.py`](../../parser/parse_replay_events.py)
  — decodes the event stream into a JSON timeline.

---

<a id="1-общая-разметка-файла"></a>
## 1. Overall File Layout
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
+--- Body ------------------------------------------------+
| Entry stream with timestamps and payloads:               |
|   entry[0]:   ts=0,         payload = initial-world      |
|                              snapshot (units, resources) |
|   entry[1+]:  ts > 0 ticks, payload = one or more        |
|                              sub-packages                |
| GameMapRecordEnd                                         |
+----------------------------------------------------------+
| GameMapBegin + f64 elapsed_raw_s + map metadata          |
| map_file + width/height + init-state + GameMapEnd        |
+----------------------------------------------------------+
```
Header keys and values are length-prefixed ASCII strings. The body is a
sequence of entries that ends at `GameMapRecordEnd`; a decoder must not
mistake the footer for another entry. The confirmed footer layout appears
in §7.5.

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
### 2.1 Meaning of `ts`

`ts` records game ticks in increments of 0.1 game seconds:
```
g_sec = ts / 10
```
The 0.1-game-second step is constant at every game speed because
`ticks_per_real_sec / game_factor` always equals 10:

| `gamespeed` | `gc_settings_gamespeed_N` (ticks/real-sec) | factor | g-sec/tick |
|------------|:------------------------------------------:|:------:|:----------:|
| Slow | 7 | 0.7 | 0.1 |
| Normal | 10 | 1.0 | 0.1 |
| Fast | 14 | 1.4 | 0.1 |

`ts` values can contain additional fractional digits—for example, 14.130
rather than 14.1—because the engine writes
`GetCurrentTime × GetTimeSpeedFactor` at full floating-point precision
instead of rounding to an integer tick.

<a id="22-десятибайтовый-entry-маркер--два-варианта"></a>
### 2.2 Ten-byte entry marker: two variants

Each body entry is preceded by a 10-byte sequence. Two variants have been
observed, distinguished by the middle four bytes:
```
variant A (saves and local replays):
  b0 04 00 00 00 00 00 00 00 00

variant B (rated/online matches):
  b0 04 <4B signature> 00 00 00 00
                       ^^^^^^^^^^^ tail remains zero
         ^^^^^^^^^^^^^ nonzero word, CONSTANT within one file
```
The scanner relies on three invariants:

- The first 2 bytes are always `b0 04`.
- The last 4 bytes are always zeros.
- The middle word, beginning at offset +2, may be zero or nonzero but
  remains constant within a file. It is a stream signature created during
  `RecordCustomBegin` initialization.

The scanner should look for the `b0 04` prefix and accept any 10-byte
marker whose final four bytes are zero. Decoders that compared the complete
marker literally lost 98% of the entries in rated replays, including the
stream that carries server-issued client commands.

The meaning of the middle word is not yet known. `0x04b0 = 1200` occurs
99 times in the executable as a 16-bit operand, but the complete 10-byte
sequence does not. The marker is assembled at runtime from internal engine
structures (`RecordCustomBegin` → channel table).

---

<a id="3-sub-package-внутренняя-структура-payloadа"></a>
## 3. Sub-package: internal payload structure

An entry contains one or more subpackages (see the native
`RecordPackagesCount` and `RecordPackagesCursor` functions). During
recording, each subpackage is enclosed by
`RecordCustomBegin(stateName)` and `RecordCustomEnd`. During playback, the
engine dispatches it to the FSM section named `stateName` through
`SwitchTo(stateName)`.

<a id="31-class0x00-default-channel--формат"></a>
### 3.1 Class 0x00 (default channel)
```
offset  size  field                                   note
---------------------------------------------------------------------
+0      4B    [class=0x00, sub=0x03, pid, state_id]   4-byte header
+4      1B    0x00                                    begin marker
+5      ?B    typed body                              typed stream
+?      1B    0x01                                    end marker
```
This format carries player commands such as building, production, movement,
and trade, as well as engine-progress events (see §3.5). Channel ID 0x03
corresponds to the default `RecordCustomBegin` channel (see §6).

**Pid mapping** (`dmscript.global`):

| pid | role |
|-------:|-------------------------------------------------------|
| 0..11 | real players (`gc_MaxPlayerCount = 12`) |
| 12 | `gc_playerind_env` |
| 13 | `gc_playerind_misc` |
| 14 | `gc_playerind_progress` – engine progress events |
| 15 | `gc_playerind_pool` |

<a id="32-class0x09-tagobject-state-sync-stream--формат"></a>
### 3.2 Class 0x09 (TagObject state-synchronization stream)

The per-object state-synchronization channel
(`RecordCustomBeginTagObject @ 0x685c6c`) uses a different layout:
```
offset  size  field
------------------------------------------------------
+0      1B    0x09                       — class
+1      3B    u24 LE — global sequence counter (monotonic)
+4      4B    u32 LE — record count
+8      ?B    count variable-length records
```
Record size ranges from 8 to 23 bytes, typically in increments of about
three bytes. The eight-byte `[u32 uid][u32 statestag]` prefix is always
present; bits in `statestag` select additional fields.

<a id="three-way-dispatch--три-подформата-записи"></a>
#### Three-way dispatch: three record subformats

Decompilation of `RecordCustomBeginTagObject` (private recon-workspace
`cossacks-deep/decompiled/record.c:286-338`; cross-reference:
`cossacks-deep/findings/record_sync.md`) reveals that one and the same
class 0x09 channel carries three different subformats, selected by
the type of the supplied handle. The engine tests three categories in order:

| Category | Resolver | Source `state_record` | Handle marker |
|----------------|-----------------------|------------------------|----------------------------|
| `TaggedHandle` (SM state) | `ResolveTaggedHandle` | `obj + 0x18` (variables collection) | high bits `0x8000` in both halves of handle |
| `GameObject` | `ValidateGameObjectHandle` | `FUN_007c32ec(go)` (sync-context accessor) | passes `ValidateGameObjectHandle` |
| `Player` | `ValidatePlayerHandle` | `obj + 0x24` (player.sync_field) | passes `ValidatePlayerHandle` |

All three paths call `_RecordManager_BeginTagWrite` with a different state
record. The serialized fields in a class 0x09 record therefore depend on
the kind of object tagged during writing.

A parser that applies one layout to every class 0x09 record will
periodically lose alignment. A correct decoder must first determine the
tag category from the record prefix—the responsible byte is not yet
identified—and then apply the Tagged-SM, GameObject, or Player layout.

The replay parser therefore treats class 0x09 as a counted but opaque record
set. Nearly all useful analytical events are class 0x00 commands, while the
synchronization stream may contain millions of records and decoding it
would slow the parser by roughly an order of magnitude.

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
#### `PackedFloat`: two-byte `uint16`

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
**Important:** `min` and `max` **are not written to the stream**. They are
implied by the call site: every
`RecordCustomWritePackedFloat(value, min, max)` supplies fixed constants.
To decode a particular `PackedFloat` field, the parser must know the range
used during recording—a mapping of state and field to `min` and `max`.

<a id="строки"></a>
#### Strings

A `String` is encoded as `[u16 len LE][bytes]` with no additional prefix.
For example, the SID `"auscen"` appears in a payload as:
```
06 00                          u16 len = 6
61 75 73 63 65 6e              "auscen"
```
<a id="bitfield-order--lsb-first"></a>
#### Bitfield order: least-significant bit first

Inside the bit-pack (`BeginBitFields … WriteBit × N … EndBitFields`)
bits are packed LSB-first. Decompilation
`_Stream_WriteBit @ 0x5b4874` (private recon-workspace
`cossacks-deep/decompiled/record.c:728-745`):
```c
*(byte *)(stream + 0x14) |= *(byte *)(stream + 0x15);  // OR the mask into the current byte
*(byte *)(stream + 0x15) <<= 1;                         // mask <<= 1
```
The mask starts at `0x01` and shifts left after every recorded bit. The
first `WriteBit(true)` therefore sets `0x01`, the second sets `0x02`, and
so on. `ReadBit` must mirror this logic or every packed Boolean sequence
will be reversed.

`EndBitFields` completes the partial byte and resets the mask. The bitfield
therefore occupies `ceil(N_bits / 8)` whole bytes in the stream.

`Int24` is a signed, three-byte little-endian value.
`RecordCustomWriteInt24 @ 0x6860d4` calls `_Stream_WriteByte` three times
and extends the high byte when reading.

### 3.4 Multi-package entry

An entry often contains several subpackages. The `0x01` end marker is
followed either by `0x00 0x03 [pid] [state_id] 0x00`, which begins another
class 0x00 subpackage, or by `0x09 [u24 seq]`, which begins a class 0x09
TagObject record. The decoder must recognize both forms.

For example, a building request (`ReadConstruct`) is usually accompanied
by one class 0x09 record containing the server state tag for the
construction placeholder. A `ReadProduce` command for a Diplomatic Center
generates several nested `ReadNew` events for the mercenary candidates.

<a id="35-engine-progress-события-pid14"></a>
### 3.5 Engine-progress events (pid=14)

For PID 14 (`gc_playerind_progress`), state IDs identify **engine FSM
transitions**, not script-handler dispatch. The body of such a subpackage
**does not match** the script handler with the same state ID; instead, the
engine writes a compact delta of its own state.

The three most common engine-progress state IDs in the observed data are:

- `0x08` (`ReadSquadListAction`) — periodic squad-bookkeeping batch
- `0x0a` (`WriteMove`) — server-side broadcast of movement orders
- `0x0f` (`ReadFree`) — periodic cleanup of outdated objects

The decoder should skip these event bodies and label them
`engine_<state_name>`.

---

<a id="4-карта-state_id--handler"></a>
## 4. Mapping `state_id` to a Handler

**Source:** `data/scripts/units/global.aix`
lists FSM sections in load order. **`state_id` equals the section index**
in the file, including separators and `section.end`.

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

State IDs 0x04, 0x09, 0x12, 0x3e, and 0x41 are separator records
(`Name = ----------------------` in `global.aix`) and do not have handlers.

The signatures of all `Read*` handlers come from
`data/scripts/units/global.inc/read*.inc`.

<a id="41-сигнатуры-тел-ключевых-handlerов"></a>
### 4.1 Body signatures of key handlers

Parameters are listed in recording order. Types correspond to the
`RecordCustomRead*` primitives in §3.3. These six handlers cover almost all
player-command analysis.
```
ReadConstruct   (0x21)  Bool bFromServer
                        Int  cid                 ← player's nation index
                        Str  sid                 ← building sid
                        Float posx, posz
                        Bool clrord
                        Int  count
                        Int[count] builder-uids

ReadNew         (0x0d)  Bool bFromServer
                        Str  race, base
                        Float posx, posz
                        Int  cid                 ← cid≤0 → -cid = nation;
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
                        Int  prcid               ← unit's nation index
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

- **`ReadProduce.proid`** indexes the nation's ordered member list, built
  by `_country_AddMember` in `country.script`:
  `country_members[NATION_BY_CID[prcid]][proid] = sid`.
  The list of members is extracted by the upgrade simulator in
  `derived/country_members.json`.
- **`ReadUpgrade.upgid` and `ReadApply.ind`** index
  `gCountry[cid].upgrade[]`. The engine builds this array in `_country_Init`
  (through the inline call `_country_InitUnitsUpgrades`) by invoking
  `SetUpgStruct`, `AddUpgradePack`, and `_country_AddUpgrade` in a fixed
  order. [`parser/simulate_upgrades.py`](../../parser/simulate_upgrades.py)
  reproduces that sequence and writes an ordered per-nation list to
  `data.json :: upgrades`; its list index equals `upgid` or `ind`.
  Without the correct order, `upgid = 2` would incorrectly resolve to a
  Barracks upgrade rather than a Mill upgrade.
- **`ReadConstruct.cid`** — nation index of the player (same as
  `TMapPlayer.cid`, see §11.2). Useful for determining the nation when
  the corresponding `TMapPlayer` has `cid=-2` (random) and the nation is not
  known in advance.

---

<a id="5-gc_obj_order_type_--типы-приказов-в-readorder"></a>
## 5. `gc_obj_order_type_*` Values in `ReadOrder`

Values from `dmscript.global:630-650`:

| code | name | meaning |
|----:|----------|-------------------------------------------------|
| 0 | `none` | no order |
| 1 | `move` | movement |
| 2 | `attackobj` | attack a specific unit/building |
| 3 | `gainres` | collect resource |
| 4 | `produce` | production (internal) |
| 5 | `patrol` | patrol |
| 6 | `attackpoint` | attack point |
| 7 | `continueattackpoint`| continue an attack-point order |
| 8 | `performupgrade` | upgrade in progress |
| 9 | `fishing` | fishing |
| 10 | `creategates` | create a gate in a wall |
| 11 | `buildwallcontinue` | continue building the wall |
| 12 | `buildwall` | build a wall |
| 13 | `gotomine` | enter a mine |
| 14 | `gototransport` | board a transport |
| 15 | `leavetransport` | leave a transport |
| 16 | `leavebuilding` | leave the building |
| 17 | `build` | move a builder to a construction site |
| 18 | `guard` | guard |
| 19 | `repair` | repair |
| 20 | `exitunits` | order units to exit |

When `ReadOrder` has `ordtyp ∈ {patrol=5, attackpoint=6}`, two additional
floating-point fields, `posx` and `posz`, follow `number` and specify the
order location. Other order types do not write coordinates.

A normal **right-click movement command** uses the separate `ReadMove`
handler (`state_id = 0x0b`) rather than `ReadOrder`. In practice,
`ordtyp = 1` (`move`) is extremely rare in `ReadOrder`.

---

<a id="6-каналы-записи"></a>
## 6. Recording channels

The native API exports five `RecordCustomBegin*` channel variants.
Disassembly of `RecordCustomBegin` (VA `0x685c38`, implementation
`0x733590`) shows that **the second byte of the subpackage** is the
channel ID selected from the dispatch table:

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
- bytes 2–3 — packed `pid` and `state_id`

A class 0x09 subpackage belongs to the TagObject channel. Its first byte is
always `0x09`, and it uses a different record layout (see §3.2) to store
compact per-object state deltas.

Reference addresses in `cossacks.exe` for further research:
`RecordCustomBegin = VA 0x685c38`, implementation = `0x733590`,
`WriteBytes = 0x5b4620`, channel-tables `0x789980` (Map),
`0x7c3160`, `0x7af5e8`.

<a id="current-write-stream--проверка-парности"></a>
#### Current write stream and begin/end pairing

The `RecordManager` layout was recovered by decompiling `record.c`
(private recon-workspace `cossacks-deep/decompiled/record.c` plus
review `cossacks-deep/findings/record_sync.md`). Every
`RecordCustomWrite*` primitive reads the current-buffer pointer at:
```
*(int*)(*(int*)(root + 0x4c) + 0x6c) + 0x118
                 │              │     │
                 │              │     └── current write stream (ptr)
                 │              └──────── RecordManager
                 └─────────────────────── main sub-manager
```
If `+0x118` is NULL, the write operation silently writes nothing.
This means that a **valid replay stream must pair every begin and end**:
`RecordCustomBegin*` initializes the stream,
`RecordCustomEnd` (`@ 0x685e00`) resets it, and any
write call between them appends to the buffer. Calls made after the end do
nothing.

Consequences for the parser:

- Subpackages follow the sequence
  “begin → body → end → begin → body → end…”. In class 0x00, the `0x01`
  end marker confirms that `RecordCustomEnd` ran and closed the stream.
- Several consecutive begin markers without an end indicate either nested
  streams, such as TagObject inside a state machine, or a damaged file.
  No nesting was observed in the replay sample: TagObject always appeared
  as a separate subpackage.
- `recordEnabled` / `recordGroupEnabled` / `recordInitializeEnabled`
  flags in `RecordManager` (`+0x130`, `+0x131`, `+0x132`) can reset the
  stream dynamically. The initial snapshot (`ts == 0`) is written with
  `recordInitializeEnabled = true`.

---

<a id="7-что-хранится-в-headerе"></a>
## 7. Header Contents

### 7.1 Lobby settings

Every `gMap.settings.*` field is written to the header as a textual
key-value record with little-endian lengths:
`[u32 keylen][key][u32 vallen][val]`. See
[`Match settings`](../../docs_en/recon/world/map/game_settings.md) for the
field meanings and `derived/game_settings.json` for canonical enum labels.
The stream includes all match rules (`peacetime`, `century18`, `capture`, `marketdip`,
`cannons`, `balloon`, `startingunits`, `resourcestart`, `gamespeed`,
`resourcemines`, `terraintype`, `relieftype`, `season`, `limit`,
`maskname`, `randkey0`, `randkey1`, `brating`, `bbattle`, `dlcs`,
`autosave`, `adviserassistant`, `teams`).

<a id="72-per-player-tmapplayer-блоки"></a>
### 7.2 Per-player TMapPlayer blocks

The header contains 12 consecutive `TMapPlayer` records
(`gc_MaxPlayerCount = 12`). Fields within each key-value block appear in a
fixed order:
```
id, cid, csid, name, team, color, lanid,
startx, starty, aidifficulty,
bexists, bai, bhuman, bclosed, bready, bloaded, bleave,
(+ random-nation enable/options: sic, snX, si1..si3)
```
The parser starts a new block whenever it encounters `id`, the first
`TMapPlayer` field, and then removes slots where `bexists != true`. A
player's runtime engine `pid` is **its position in the filtered list, not
the value of its `id` field**. See §11.1.

<a id="73-bmp-превью-и-стартовый-снимок"></a>
### 7.3 BMP preview and starting snapshot

- BMP map preview (~145 KB) between `GameMapSnapShotBegin/End`.
- The first entry body (`ts == 0`) contains the initial snapshot of the world:
  starting units, resource clusters, mines, fog. This entry
  differs from later entries mainly in size and normally serves only as
  the decoder's baseline.
- A third-party tool proposed a repeated record layout
  `[f32 x][f32 y][u16 id][20 00 1a][u32 flag]` (actually 17, not
  16 bytes), but it did not recur in a sample of 25 replays and is not
  treated as part of the confirmed starting-snapshot schema.

<a id="74-patternlist-имена-и-координаты-размещённых-паттернов"></a>
### 7.4 PatternList: names and coordinates of placed patterns

After the LP marker `PatternList` there are successive text kv-triples:
```
[u32 1] "n" [u32 name_len] pattern_name
[u32 1] "x" [u32 x_len]    x_ascii
[u32 1] "y" [u32 y_len]    y_ascii
```
`n` is the generator-selected pattern filename; `x` and `y` are its map
coordinates serialized as ASCII numbers, usually signed integers. The three
records must be adjacent. Isolated `n`, `x`, or `y` keys outside
`PatternList` do not describe a placement.

The schema was confirmed on 25 replays: from 62 entries on a 256×256 map to
1,291 on a 640×640 map. `parser/parse_replay.py` returns them through
`extract_pattern_placements()` and JSON field `pattern_placements`.

<a id="75-футер-после-gamemaprecordend"></a>
### 7.5 Footer after GameMapRecordEnd

All 25 tested replays use the same frame immediately after the entry stream:
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
The sample contains 256×256, 320×320, 480×480, and 640×640 maps; a parser
must not hard-code a single size. `elapsed_raw_s` is a finite, nonnegative,
time-like value, but it **does not equal** the stream duration
`last_ts / 10`. Until its clock semantics are known, it cannot replace
`duration_g_sec`.

Parser `parse_footer()` returns confirmed fields and marks the footer
`complete=true` only when `GameMapEnd` is found.

The initial clues for `PatternList` and the footer frame were compared with
[`czanchetta/cossacks3-replay-tools`](https://github.com/czanchetta/cossacks3-replay-tools/blob/main/docs/FORMATO_REP_COSSACKS3.md),
then independently tested against a local sample. No code was copied from
the external repository, and its unconfirmed snapshot hypothesis was not
adopted.

<a id="76-поток-событий"></a>
### 7.6 Event flow

The event stream contains the full log of client commands and server
state-synchronization packages; see §3.

<a id="77-что-не-хранится"></a>
### 7.7 Data not stored in the replay

- Chat and voice. They may use `ReadPackage`, but do not appear in the
  observed streams.
- Elo rating data, which comes separately from the Steam match server.

---

<a id="8-закрытые-tbd"></a>
## 8. Resolved Questions

| Question | Resolution |
|---------------------------------------|------------------------------------------|
| Meaning of `ts` | ticks × 0.1 = game seconds |
| Pid byte interpretation | `gc_playerind_progress=14` and others |
| Sub-package header layout | 4B header + 0x00 begin + body + 0x01 end |
| String encoding | `[u16 len][bytes]`, no prefix |
| Multi-package boundaries | End marker `0x01`, followed by the next subpackage's `00 03` prefix |
| Class=0x09 layout | `[09][u24 seq][u32 count][records]` |
| Complete `state_id` map | Section indexes in `global.aix` |
| `Read*` / `Write*` distinction | Read and write sections alternate in `global.aix` |
| Recording channels | `RecordCustomBegin` disassembly (§6) |
| Meaning of engine events with pid=14 | `state_id` is an FSM transition label; the payload is engine-internal |
| 10-byte entry marker (two variants) | `b0 04` + (zero or signature) + zero tail; see §2.2 |
| Player names and nations | Stored in `TMapPlayer` blocks; see §7.2 and §11 |
| Host in rated matches | `brating=true` ⇒ host = color 0 (red); see §11.2 |
| Class=0x09 three-way dispatch | TaggedHandle/GameObject/Player branches in `RecordCustomBeginTagObject @ 0x685c6c`; see §3.2 |
| Bit order in bit-pack | LSB-first (`_Stream_WriteBit @ 0x5b4874`); see §3.3 |
| Begin/end pairing in the stream | The `+0x118` write stream; writes outside a begin/end pair silently do nothing; see §6 |
| `PatternList` placement records | Adjacent length-prefixed key/value triples `n`/`x`/`y`; see §7.4 |
| Replay footer frame | `GameMapBegin` → map metadata → `GameMapEnd`; see §7.5 |

<a id="9-открытые-tbd"></a>
## 9. Open Questions

- Meaning of the middle word in entry-marker variant B from §2.2: where
  the runtime obtains it and why rated matches differ from saves. It may be
  a channel or session ID issued by the match server, but the
  `RecordCustomBegin` disassembly does not confirm that.
- Exact layout of variable-length class 0x09 records longer than eight
  bytes. Bits in `statestag` select additional fields; mapping flags to
  fields requires disassembly of
  `RecordCustomBeginTagObject` and related write-routines.
- Layout of `RecordCustomReadPackedFloat` /
  `RecordCustomWritePackedFloat` (`@ 0x6860ac` / `@ 0x6860c4`). The native
  functions exist but do not appear in standard streams. They may pack
  coordinates and angles in `ReadSync`; decompiling the bodies would
  distinguish half-float, ranged fixed-point, and delta encoding.
- Bodies of PID 14 engine-progress payloads with state IDs 0x08, 0x0a,
  and 0x0f. Their layout differs from the corresponding script-handler
  signatures and is written directly by the engine.
- `ReadSync` (`state_id = 0x3b`). Its complex signature describes a full
  unit snapshot, including orientation matrices, health, and RNG seed. It
  does not occur in ordinary replays and may initialize a client that joins
  a running match.
- Host identification in non-rated matches. Rated matches use color 0, but
  LAN and private-lobby players can change colors freely, and no obvious
  field marks the host PID.
- Exact meaning of `elapsed_raw_s` in the footer. It is time-like but not
  equal to `last_ts / 10`; candidates include wall-clock time, pause-aware
  time, and engine-lifetime time.
- Exact binary layout of the initial entry (`ts == 0`). The proposed
  17-byte record with delimiter `20 00 1a` was not reproduced in the
  25-replay sample.

---

<a id="10-связь-с-другими-документами"></a>
## 10. Relationship to Other Documents

- [`../engine/server_sync_architecture.md`](../engine/server_sync_architecture.md)
  — Cossacks 3 network architecture.
- [`../engine/server_sync_packet_format.md`](../engine/server_sync_packet_format.md)
  — binary `EconomyPackage` layout.
- [`../engine/ticks_and_subticks.md`](../engine/ticks_and_subticks.md)
  — `GetGameTime`, `GetCurrentTime`, `GetTimeSpeedFactor`.
- [`../engine/native_api.md`](../engine/native_api.md) — catalog of
  `RecordCustom*` primitives.
- [`../scripts/structure.md`](../scripts/structure.md) — FSM-section layout
  in `read*.inc` and `write*.inc`.
- [`../engine/rng_implementation.md`](../engine/rng_implementation.md)
  — `uniqrnd` (per-object RNG seed), synchronized in `ReadSync`
  and `ReadDeath`.

---

## 11. Identification Conventions

These conventions identify players, nations, and roles from the header and
event stream. External replay tools can use the same rules to compare
participants across files.

### 11.1 Runtime `pid` ≠ `TMapPlayer.id`

The engine `pid` written to each subpackage is **the player's position in
the slot list after filtering by `bexists`**, not the value of
`TMapPlayer.id`:

1. Collect slots in the order of appearance in kv-stream.
2. Remove slots with `bexists != true` (closed or empty).
3. Assign `pid` from the index in the filtered list.

`TMapPlayer.id` is stored separately and appears to be a session or join
identifier; event payloads do not use it. In `ex1.rep`, known players map
correctly by slot order rather than ID order.

<a id="112-нация-tmapplayercid-как-канонический-источник"></a>
### 11.2 Nation: `TMapPlayer.cid` as canonical source

The `cid` field in a `TMapPlayer` block is a nation index from 0 to 23. A
static table maps it to a nation SID: `NATION_BY_CID` in the parser and
`gc_country_*` in `country.script`.

| cid | sid |  | cid | sid |  | cid | sid |  | cid | sid |
|----:|-------|--|----:|-------|--|----:|-------|--|----:|-------|
| 0 | aus |  | 6 | pol |  | 12 | mis |  | 18 | bav |
| 1 | fra |  | 7 | swe |  | 13 | net |  | 19 | hun |
| 2 | eng |  | 8 | pru |  | 14 | den |  | 20 | swi |
| 3 | spa |  | 9 | ven |  | 15 | por |  | 21 | sco |
| 4 | rus |  | 10 | tur |  | 16 | pie |  | 22 | tat |
| 5 | ukr |  | 11 | alg |  | 17 | sax |  | 23 | lit |

Special meanings:

- `cid = -2` — the player chose **Random nation**, which is resolved at
  match start. The header does not contain the final nation. Recover it
  from the `cid` field in the player's first `ReadConstruct` payload (see
  §3.1 and the handler table), or from the SID prefix after accounting for
  shared clusters such as `eur*`, `rus*`, `tur*`, `spa*`, `por*`, and
  `ukr*`.
- `cid = 24` — a **closed slot**. `bexists` may remain true for a
  spectator slot even though no player participates.

The player's first `ReadConstruct` payload also carries `cid`, providing
another source for resolving `cid = -2`.

<a id="113-host-игрок"></a>
### 11.3 Host player

In rated matches (`brating = "true"`), **the host is the player with
`color = 0` (red)**. The match server assigns red to the room creator, and
colors cannot be changed in a rated lobby.

The rule **does not apply** to LAN or private-lobby matches: players can
change colors freely, and no field clearly marks the host PID. Analyses of
client-only behavior, such as the double-upgrade race condition, therefore
cannot filter out the host in non-rated replays and may report host actions
as false positives.

Engine-source: `GetKeyColorByPlayerIndex` in
`lib/classes.script:7986`
paints index 0 in rgb(164, 0, 0).

<a id="114-имена-игроков"></a>
### 11.4 Player names

`TMapPlayer.name` is the display name entered in the player's profile, for
example `[WhoT]Niotid`, `macaron`, or `skipi_lon`. `TMapPlayer.lanid` is a
numeric profile ID from the match server. It is a convenient stable key for
aggregating one player's statistics across many replays.
