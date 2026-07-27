<a id="формат-сетевых-пакетов-c3-через-анализ-скриптовых-вызовов"></a>
# Cossacks 3 Network Packet Format

This document reconstructs synchronization-packet layouts **without
decompiling the executable**, using only native API calls found under
`data/scripts/lib/`.

> Companion documents: [`server_sync_architecture.md`](server_sync_architecture.md)
> describes the overall model, and [`native_api.md`](native_api.md) lists
> the serialization primitives exported by the executable.

<a id="1-двойная-система-сериализации"></a>
## 1. Two serialization systems

Cossacks 3 records state through **two separate serialization systems**:

| System | API | Format | Where it is used |
|---|---|---|---|
| **Binary** | `RecordCustomWrite{Bit, Byte, Word, Int24, Integer, Float, PackedFloat, ShortString, String}` | bit-packed binary stream | Real-time economy synchronization and small multiplayer deltas. |
| **Parser-text** | `ParserSet{Int, Float, Bool, String}ValueByKeyByHandle` | flat key=value text in `.parser` format | Unit/squad state snapshots, save files, debug sync. |

The scripts contain 15 `RecordCustomWrite*` calls. Most calls in
`lib/miscext2.script` belong to commented-out code; the active calls are
the economy writers in `lib/classes.script`. Most unit synchronization
uses parser format through the 29 `ParserSet*` calls in
`AddUnitInfoToParser`.

<a id="почему-так"></a>
### Why both exist

Binary packets are compact at 1–18 bytes each. Parser-format payloads are
flexible, easy to inspect, and tolerant of added fields. Frequently sent
per-tick data uses binary encoding; event-driven and save data uses parser
text.

<a id="2-бинарный-пакет-economypackage"></a>
## 2. Binary package: `EconomyPackage`

The most frequently sent synchronization packet carries player economy
counters. Its source is
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
### 2.2. Sizes

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
### 2.4. Full package

The scripts wrap these records in:
```pascal
type TLanSyncData = class
    playerstosync : Word;                                    // bitmask: players included in the packet
    economyfieldstosync : array [0..11] of Byte;             // fields included for each player
    netplayer : array [0..11] of TLanSyncPlayerData;
end;
```
A full economy snapshot is a `Word` player mask followed by up to 12
`EconomyPackage` records. The maximum size is
2 + 12 × 18 = **218 bytes** in a 12-player match. Most packets include
only a few changes and occupy 5–30 bytes.

<a id="3-parser-формат-unit-state-snapshots"></a>
## 3. Parser format: unit state snapshots

Source: `data/scripts/lib/miscext2.script` →
`AddUnitInfoToParser(pSync, syncuid : Integer)`. Unit fields
are written as `key=value` entries in a parser handle:

<a id="31-список-полей-29-штук"></a>
### 3.1. Field list (29 fields)

| Group | Key | Type | Meaning |
|---|---|---|---|
| **identity** | `syncuid` | int | sync-UID of unit (stable) |
| | `bexists` | bool | alive or deleted |
| | `racename` | string | nation sid (`aus`, `fra`, ...) |
| | `basename` | string | unit sid (`musket18`, `cen`, ...) |
| | `cid` | int | nation ID (0..23) |
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

The `angle` field appears in the code but is **commented out**, so this
channel does not synchronize it.

<a id="32-формат-на-проводе"></a>
### 3.2. Format on wire

A package serializes the parser handle into flat text:
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
This is the standard Cossacks 3 `.parser` syntax also used by
`dmscript.global` and other configuration files.

`LoadUnitInfoFromParser` reads the same payload. The paired
`Get*ValueByKeyByHandle` functions retrieve fields by name, so field order
does not matter and new fields can be added without breaking compatibility.

<a id="33-размер"></a>
### 3.3. Size

One unit occupies about **400–600 bytes** in text form, depending on name
lengths. A 200-unit state snapshot is therefore roughly 100 KB.

This is larger than an equivalent binary record, which would need roughly
80 bytes per unit with `Int24`, `PackedFloat`, and bitfields. Full snapshots
are sent infrequently, however—primarily when a client connects or requests
on-demand synchronization—and most units do not change on every tick.

<a id="4-что-мы-не-нашли-в-скриптах"></a>
## 4. Native APIs Not Called by Scripts

The executable exposes the following APIs, but scripts **do not call them**:

- `RecordCustomBeginGUI` / `RecordCustomBeginMap` /
  `RecordCustomBeginStateMachine` / `RecordCustomBeginTagObject` —
  have no script call sites. The engine itself may use them for other
  synchronization channels, such as GUI state, state machines, or map updates.
- `RecordSynch*` (more than 40 functions) is **never** called from scripts.
  Delta marking and stack-based synchronization are therefore internal
  engine mechanisms. On the wire, scripts expose only
  `RecordCustom*`-serialized results.
- `RecordCustomReadBit` / `RecordCustomBeginReadBitFields` /
  `RecordCustomReadInt24` / `RecordCustomReadPackedFloat` — available in
  the executable, but scripts do not call them. The engine can decode
  hard-coded packet layouts without script involvement.

<a id="5-что-это-меняет-в-существующем-server_sync_architecturemd"></a>
## 5. Implications for `server_sync_architecture.md`

[`server_sync_architecture.md`](server_sync_architecture.md) describes
`bProcess` as an abstraction without committing to a payload format. The
concrete implementations are:

| `bProcess`-stream | Real implementation |
|---|---|
| Per-event mod-53 sync unit parameters | Parser format, `AddUnitInfoToParser` (see §3) |
| Periodic real-time sync economy | Binary `EconomyPackage` (see §2) |
| On-demand full state | Parser snapshot of all units (large) |

Indy 10 handles network I/O outside the scripting environment. Scripts only
prepare a **payload** in one of the two formats.

<a id="6-воспроизведение-результатов"></a>
## 6. Reproducing the analysis

The analysis is entirely static and can be reproduced with:
```powershell
# List the available native synchronization functions
python -c "import json; d=json.load(open('derived/dws_native_signatures.json',encoding='utf-8')); print('\n'.join(s['raw'] for s in d['signatures'] if 'record' in s['name'].lower() or 'serial' in s['name'].lower()))"

# Find where and how scripts call them
grep -rn -E 'RecordCustom|ParserSet.*ValueByKey' "C:\Program Files (x86)\Steam\steamapps\common\Cossacks 3\data\scripts"
```
<a id="7-что-осталось-закопанным"></a>
## 7. Remaining unknowns

1. **Exact meaning of `Word playerstosync`.** Bit 0 may represent player 0
   or the first player included in the packet. Capturing network traffic is
   required to distinguish the two.
2. **Compression.** The engine may compress parser-text payloads with zlib
   before transmission. The executable contains the Pascal class
   `ECompressionError`, suggesting zlib or gzip support.
3. **Authentication or signing.** Protection against modified clients is
   not visible in scripts; it may be implemented through Steam
   authentication, Indy SSL, or another native mechanism.
