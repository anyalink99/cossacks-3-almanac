<a id="формат-сетевых-пакетов-c3-через-анализ-скриптовых-вызовов"></a>
# C3 network packet format (via script call analysis)

Bit-layout of synchronization packages, restored **without decompilation
exe** - only through analysis of native API calls in scripts
`data/scripts/lib/`.

>Accompanies [`server_sync_architecture.md`](server_sync_architecture.md)
> (general model) and [`native_api.md`](native_api.md) (full list
> serialization primitives in exe).

<a id="1-двойная-система-сериализации"></a>
## 1. Double serialization system

C3 is home to **two different state recording systems** using
various native APIs:

| System | API | Format | Where it is used |
|---|---|---|---|
| **Binary** | `RecordCustomWrite{Bit, Byte, Word, Int24, Integer, Float, PackedFloat, ShortString, String}` | bit-packed binary stream | Real-time sync economy, small delta packages in multiplayer. |
| **Parser-text** | `ParserSet{Int, Float, Bool, String}ValueByKeyByHandle` | flat key=value text in `.parser` format | Unit/squad state snapshots, save files, debug sync. |

This can be seen in fact: in scripts `RecordCustomWrite*` is called **15
times** (in `lib/miscext2.script`, mostly **commented out** -
old code), and really active calls are only in
`lib/classes.script` for economics. Most unit synchronization
(29 ParserSet calls in `AddUnitInfoToParser`) uses
parser-format.

<a id="почему-так"></a>
### Why so

The binary is compact (1–18 bytes per packet), the parser format is
flexibility and debug-friendly (you can open the package in a text editor).
C3 selects the format based on the criterion “how often it is sent”: what is sent
**each game-tick** is a binary; what is sent **for an event** or for
save - parser-text.

<a id="2-бинарный-пакет-economypackage"></a>
## 2. Binary package: `EconomyPackage`

The hottest sync package in C3 is economic synchronization
player indicators. Source:
`data/scripts/lib/classes.script` → `TLanSyncPlayerData.WriteEconomyPackage`.

<a id="21-структура"></a>
### 2.1. Structure

Full bit-layout (read top-to-bottom):
```
struct EconomyPackage {
    Byte   economyfieldstosync;   // bitmask: fields changed
                                  // since the previous tick
    if (economyfieldstosync > 0) {
        Byte plind;               // player index (0..11)
        if (mask bit 0) Word idlepeasants;     // idle peasants
        if (mask bit 1) Word idlemines;        // empty mines
        if (mask bit 2) Word workers_food;     // gathering food
        if (mask bit 3) Word workers_wood;     // gathering wood
        if (mask bit 4) Word workers_stone;    // gathering stone
        if (mask bit 5) Word workers_gold;     // gathering gold
        if (mask bit 6) Word workers_iron;     // gathering iron
        if (mask bit 7) Word workers_coal;     // gathering coal
    }
};
```
<a id="22-размеры"></a>
### 2.2. Dimensions

| Script | Package Size |
|---|---:|
| No changes | 1 byte (only mask `0x00`) |
| 1 indicator has changed | 1 + 1 + 2 = **4 bytes** |
| All 8 economic fields | 1 + 1 + 8×2 = **18 bytes** |

<a id="23-воспроизведение"></a>
### 2.3. Playback
```pascal
// classes.script:
type TLanSyncPlayerData = class
    plind : Byte;
    idlepeasants : Word;
    idlemines : Word;
    workersonres : array [0..gc_ResCount-1] of Word;

    procedure WriteEconomyPackage(economyfieldstosync : Word);
    begin
        RecordCustomWriteByte(economyfieldstosync);
        if (economyfieldstosync > 0) then
        begin
            RecordCustomWriteByte(plind);
            if ((economyfieldstosync and (1 shl 0)) <> 0) then
                RecordCustomWriteWord(idlepeasants);
            // ... the other 7 fields use the same mask pattern
        end;
    end;
end;
```
<a id="24-полный-пакет"></a>
### 2.4. Complete package

The scripts also have a covering type:
```pascal
type TLanSyncData = class
    playerstosync : Word;                                    // bitmask: players included in the packet
    economyfieldstosync : array [0..11] of Byte;             // fields included for each player
    netplayer : array [0..11] of TLanSyncPlayerData;
end;
```
That is, full economy-snapshot = `Word`-player mask + 12 packages
`EconomyPackage`. Maximum - 2 + 12 × 18 = **218 bytes** per 12-player
map (everything with everything). In reality, changes are rare, and the package is usually
weighs 5–30 bytes.

<a id="3-parser-формат-unit-state-snapshots"></a>
## 3. Parser format: unit state snapshots

Source: `data/scripts/lib/miscext2.script` →
`AddUnitInfoToParser(pSync, syncuid : Integer)`. Unit fields
are written as `key=value` in parser-handle:

<a id="31-список-полей-29-штук"></a>
### 3.1. List of fields (29 pieces)

Group | Key | Type | What |
|---|---|---|---|
| **identity** | `syncuid` | int | sync-UID of unit (stable) |
| | `bexists` | bool | alive or deleted |
| | `racename` | string | nation sid (`aus`, `fra`, ...) |
| | `basename` | string | unit sid (`musket18`, `cen`, ...) |
| | `cid` | int | country id (0..23) |
| | `id` | int | internal id |
| | `pl` | int | player handle |
| **position** | `posx`, `posz` | float | coordinates on the map (tiles) |
| | `scale` | float | model scale |
| | `upx`, `upy`, `upz` | float | up-vector (for orientation) |
| | `dirx`, `diry`, `dirz` | float | direction-vector |
| **state** | `statestag` | int | FSM state bitmask (see `gc_statetag_*`) |
| | `sto` | int | sub-tick offset |
| | `stpx`, `stpz`, `sta` | float | start-position and start-angle (for lerp) |
| **health** | `hp` | int | current HP |
| | `bbuilt` | bool | building completed (`True`) or under construction |
| | `bdead` | bool | dead |
| | `buildprogress` | float | construction progress |
| **rng** | `uniqrnd` | float | per-unit random seed `[0,1)` (for headshot reproducibility) |

(field `angle` is present in the code, but **commented out** - that is
angle is not synchronized through this channel.)

<a id="32-формат-на-проводе"></a>
### 3.2. Format on wire

A package is a serialized parser-handle that turns into
flat text like:
```
unit_<syncuid> begin
   syncuid = 12345
   bexists = true
   racename = aus
   basename = peaaus
   posx = 47.5
   posz = 122.3
   scale = 1.0
   upx = 0.0; upy = 1.0; upz = 0.0
   dirx = 0.7; diry = 0.0; dirz = 0.7
   statestag = 0x00000C20
   sto = 95
   hp = 5
   bbuilt = true
   bdead = false
   uniqrnd = 0.4827
end
```
(The exact syntax is the format `.parser` in C3, exactly the same as in
`dmscript.global` and other configs.)

In parallel, the function `LoadUnitInfoFromParser` in the same file reads
back. Paired `Get*ValueByKeyByHandle` allows you to read any field
without knowing the order - therefore the format is version tolerant (new
fields can be added without breaking compatibility).

<a id="33-размер"></a>
### 3.3. Size

One unit ≈ **400–600 bytes** in text form (plus/minus, depends
depending on name lengths). For 200 units on a four-player map, the result is
about 100 KB.
state-snapshot.

This is **more** than a packaged binary would give (in the same place ~ 80 bytes per unit
using `Int24`+`PackedFloat`+bit-fields), but C3 prefers
text: delta between ticks is small (most units do not move
every tick), and a full snapshot is rarely sent (only when connecting
new client and with ON-DEMAND synchronization).

<a id="4-что-мы-не-нашли-в-скриптах"></a>
## 4. What we didn't find in the scripts

There is an API in the exe, but it is **not called in scripts**:

- `RecordCustomBeginGUI` / `RecordCustomBeginMap` /
  `RecordCustomBeginStateMachine` / `RecordCustomBeginTagObject` —
  not a single call. These functions remained on the engine side and
  used by the engine directly for other sync channels
  (for example, GUI-state, FSM, map updates).
- `RecordSynch*` (40+ functions) - **completely** not called from
  scripts. This means "delta-mark and stack-based sync" - this is
  purely internal mechanism of the engine. On the wire we only see
  `RecordCustom*`-serialized results.
- `RecordCustomReadBit` / `RecordCustomBeginReadBitFields` /
  `RecordCustomReadInt24` / `RecordCustomReadPackedFloat` - available in
  exe, but the scripts don't call them. Again, the engine can decode
  packages without a script (if the structure is hardwired).

<a id="5-что-это-меняет-в-существующем-serversyncarchitecturemd"></a>
## 5. What does this change in the existing `server_sync_architecture.md`

Document
[`server_sync_architecture.md`](server_sync_architecture.md) described
pattern `bProcess` as an abstraction, without specifying a specific format.
Now we know:

| `bProcess`-stream | Real implementation |
|---|---|
| Per-event mod-53 sync unit parameters | Parser format, `AddUnitInfoToParser` (see §3) |
| Periodic real-time sync economy | Binary `EconomyPackage` (see §2) |
| On-demand full state | Parser snapshot of all units (large) |

Net I/O (network sending itself) - Indy 10, not available to scripts.
The scripts only prepare **payload** in one of two formats.

<a id="6-воспроизведение-результатов"></a>
## 6. Reproduction of results

All this data is obtained statically. To repeat:
```powershell
# List the available native synchronization functions
python -c "import json; d=json.load(open('derived/dws_native_signatures.json',encoding='utf-8')); print('\n'.join(s['raw'] for s in d['signatures'] if 'record' in s['name'].lower() or 'serial' in s['name'].lower()))"

# Find where and how scripts call them
grep -rn -E 'RecordCustom|ParserSet.*ValueByKey' "C:\Program Files (x86)\Steam\steamapps\common\Cossacks 3\data\scripts"
```
<a id="7-что-осталось-закопанным"></a>
## 7. What remains buried

1. **Exact semantics of `Word playerstosync`** - bit order: bit 0
   = player 0, or bit 0 = first "available in the package"? Without sniff
   original traffic cannot be allowed unambiguously.
2. **Compression**. Perhaps the engine compresses the text
   parser-payload by zlib before sending. The native API has
   `ECompressionError` (Pascal class in exe) - hints at zlib/gzip.
3. **MAC/signing**. A way to protect against dishonest clients in exe
   definitely there (Steam-auth + Indy SSL?), but not visible through scripts.
