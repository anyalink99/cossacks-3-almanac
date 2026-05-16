"""Parse the event stream of a Cossacks 3 replay (.rep) or save (.map).

OSWMap13 body decoder. See `internals/data/replay_format.md` for the full
spec. The replay is a stream of timestamped entries; each entry contains
1+ sub-packages. Two sub-package formats coexist:

**Class 0x00 (player commands + engine events):**

    [4B header: class=0x00, sub=0x03, pid, state_id]
    [1B 0x00 begin-marker — written by RecordCustomBegin]
    [typed body — sequence of RecordCustomWrite* values]
    [1B 0x01 end-marker — written by RecordCustomEnd]

**Class 0x09 (per-object state-sync stream / TagObject channel):**

    [1B 0x09 class]
    [3B u24 LE global sequence number]
    [4B u32 LE record count]
    [N records of variable per-record size]

`ts` is in engine ticks at 0.1 g-sec each — divide by 10 for g-seconds.

Usage:
    python parser/parse_replay_events.py <file.rep>            # write events.json
    python parser/parse_replay_events.py <file.rep> --summary  # stats to stdout
"""
from __future__ import annotations
import json
import struct
import sys
from collections import Counter, defaultdict
from pathlib import Path


# ----- Constants ---------------------------------------------------------
ENTRY_MARKER = b"\xb0\x04\x00\x00\x00\x00\x00\x00\x00\x00"
SUBPKG_BEGIN = 0x00
SUBPKG_END = 0x01

# gc_playerind_* from dmscript.global
PSEUDO_PLAYERS = {12: "env", 13: "misc", 14: "progress", 15: "pool"}

# State name table extracted from data/scripts/units/global.aix (section order).
# State_id = index of `Name = X` line in that file (including separators).
# Cross-verified: ReadConstruct(0x21=33), ReadNew(0x0d=13), ReadOrder(0x17=23),
# ReadMove(0x0b=11), ReadProj(0x29=41) — all match observed payloads exactly.
STATE_NAMES = {
    0x00: "Initial",        0x01: "OnBeforeSave",         0x02: "OnAfterLoad",
    0x03: "Progress",       0x04: "_SEPARATOR_",          0x05: "WriteSquadNew",
    0x06: "ReadSquadNew",   0x07: "WriteSquadListAction", 0x08: "ReadSquadListAction",
    0x09: "_SEPARATOR_",    0x0a: "WriteMove",            0x0b: "ReadMove",
    0x0c: "WriteNew",       0x0d: "ReadNew",              0x0e: "WriteFree",
    0x0f: "ReadFree",       0x10: "WriteDeath",           0x11: "ReadDeath",
    0x12: "WritePlayer",    0x13: "ReadPlayer",           0x14: "WriteRally",
    0x15: "ReadRally",      0x16: "WriteOrder",           0x17: "ReadOrder",
    0x18: "WriteUpgrade",   0x19: "ReadUpgrade",          0x1a: "WriteProduce",
    0x1b: "ReadProduce",    0x1c: "WriteSearch",          0x1d: "ReadSearch",
    0x1e: "WriteStand",     0x1f: "ReadStand",            0x20: "WriteConstruct",
    0x21: "ReadConstruct",  0x22: "WriteApply",           0x23: "ReadApply",
    0x24: "WriteLeaveOrder",0x25: "ReadLeaveOrder",       0x26: "WriteLeave",
    0x27: "ReadLeave",      0x28: "WriteProj",            0x29: "ReadProj",
    0x2a: "WriteProjFree",  0x2b: "ReadProjFree",         0x2c: "WriteNewP",
    0x2d: "ReadNewP",       0x2e: "WriteStop",            0x2f: "ReadStop",
    0x30: "WriteTrade",     0x31: "ReadTrade",            0x32: "WriteWall",
    0x33: "ReadWall",       0x34: "WriteGate",            0x35: "ReadGate",
    0x36: "WriteFreeList",  0x37: "ReadFreeList",         0x38: "WritePeaceTime",
    0x39: "ReadPeaceTime",  0x3a: "WriteSync",            0x3b: "ReadSync",
    0x3c: "WriteSyncUnitsParams", 0x3d: "ReadSyncUnitsParams",
    0x3e: "_SEPARATOR_",    0x3f: "WritePackage",         0x40: "ReadPackage",
    0x41: "_SEPARATOR_",    0x42: "ProgressAI",           0x43: "ProgressEconomicAI",
    0x44: "ProgressWarAI",  0x45: "CheckErrors",          0x46: "ReadTradeResources",
    0x47: "WriteTradeResources",
}

# gc_obj_order_type_* from dmscript.global:630-650
ORDER_TYPES = {
    0: "none", 1: "move", 2: "attackobj", 3: "gainres", 4: "produce",
    5: "patrol", 6: "attackpoint", 7: "continueattackpoint",
    8: "performupgrade", 9: "fishing", 10: "creategates",
    11: "buildwallcontinue", 12: "buildwall", 13: "gotomine",
    14: "gototransport", 15: "leavetransport", 16: "leavebuilding",
    17: "build", 18: "guard", 19: "repair", 20: "exitunits",
}

# state_id → (handler-name, decoder) — populated below
KNOWN_HANDLERS: dict[int, str] = {}


# ----- Low-level cursor reader ------------------------------------------
class Reader:
    """Cursor-based reader over a bytes payload with typed reads."""

    def __init__(self, data: bytes, start: int = 0):
        self.data = data
        self.pos = start

    def remaining(self) -> int:
        return len(self.data) - self.pos

    def u8(self) -> int:
        v = self.data[self.pos]; self.pos += 1; return v

    def u16(self) -> int:
        v = struct.unpack_from("<H", self.data, self.pos)[0]; self.pos += 2; return v

    def u24(self) -> int:
        b = self.data[self.pos:self.pos+3]; self.pos += 3
        return b[0] | (b[1] << 8) | (b[2] << 16)

    def u32(self) -> int:
        v = struct.unpack_from("<I", self.data, self.pos)[0]; self.pos += 4; return v

    def i32(self) -> int:
        v = struct.unpack_from("<i", self.data, self.pos)[0]; self.pos += 4; return v

    def f32(self) -> float:
        v = struct.unpack_from("<f", self.data, self.pos)[0]; self.pos += 4; return v

    def boolean(self) -> bool:
        return self.u8() != 0

    def string(self) -> str:
        """Pascal-style: [u16 len LE][bytes]."""
        n = self.u16()
        if n > 1024 or self.pos + n > len(self.data):
            raise ValueError(f"implausible string len={n} at pos={self.pos}")
        s = self.data[self.pos:self.pos+n].decode("ascii", errors="replace")
        self.pos += n
        return s


# ----- Class=0x00 handler decoders --------------------------------------
def _ctx_from(ts: float, hdr: dict) -> dict:
    return {"ts_tick": ts, "ts_g_sec": ts / 10.0, "pid": hdr["pid"],
            "pid_name": (f"player_{hdr['pid']}" if hdr["pid"] < 12
                         else PSEUDO_PLAYERS.get(hdr["pid"], f"unknown_{hdr['pid']}"))}


def decode_construct(r: Reader, ts: float, hdr: dict) -> dict:
    """state_id=0x21 — ReadConstruct (place building order).

    Format: bool bFromServer, Int cid, String sid, Float posx, posz,
    bool clrord, Int count, count*Int builder-uids.
    """
    bFromServer = r.boolean()
    cid = r.i32()
    sid = r.string()
    posx = r.f32()
    posz = r.f32()
    clrord = r.boolean()
    count = r.i32()
    builders = [r.i32() for _ in range(count)]
    return {**_ctx_from(ts, hdr), "handler": "ReadConstruct",
            "sid": sid, "cid": cid, "pos": [posx, posz],
            "clrord": clrord, "from_server": bFromServer, "builders": builders}


def decode_new(r: Reader, ts: float, hdr: dict) -> dict:
    """state_id=0x0d — ReadNew (spawn unit on client).

    From readnew.inc: cid<=0 means -cid is country-id; cid>0 means it's
    the uid of the producing building.
    """
    bFromServer = r.boolean()
    race = r.string()
    base = r.string()
    posx = r.f32()
    posz = r.f32()
    cid = r.i32()
    uid = r.i32()
    num = r.i32()
    return {**_ctx_from(ts, hdr), "handler": "ReadNew",
            "race": race, "sid": base, "pos": [posx, posz],
            "producer_uid_or_negcountry": cid, "uid": uid,
            "num_units_total": num, "from_server": bFromServer}


def decode_newp(r: Reader, ts: float, hdr: dict) -> dict:
    """state_id=??? — ReadNewP (spawn primitive: field, balloon, ship-dummy)."""
    bFromServer = r.boolean()
    race = r.string()
    base = r.string()
    posx = r.f32(); posz = r.f32(); roll = r.f32()
    plind = r.i32(); id_ = r.i32(); uid = r.i32(); num = r.i32()
    return {**_ctx_from(ts, hdr), "handler": "ReadNewP",
            "race": race, "sid": base, "pos": [posx, posz], "roll": roll,
            "plind": plind, "id": id_, "uid": uid, "num_units_total": num,
            "from_server": bFromServer}


def decode_order(r: Reader, ts: float, hdr: dict) -> dict:
    """state_id=0x17 — ReadOrder (most player actions: gather, attack, etc).

    Format: Int ordtyp, Int taruid, Bool clrord, Bool locktrg, Int number,
    [Float posx, posz if ordtyp ∈ {patrol=5, attackpoint=6}], number*Int uids.
    """
    ordtyp = r.i32()
    taruid = r.i32()
    clrord = r.boolean()
    locktrg = r.boolean()
    number = r.i32()
    pos = None
    if ordtyp in (5, 6):  # patrol, attackpoint
        pos = [r.f32(), r.f32()]
    units = [r.i32() for _ in range(number)]
    return {**_ctx_from(ts, hdr), "handler": "ReadOrder",
            "ordtyp": ordtyp, "ordtyp_name": ORDER_TYPES.get(ordtyp, f"unknown_{ordtyp}"),
            "target_uid": taruid, "clrord": clrord, "locktrg": locktrg,
            "pos": pos, "units": units}


def decode_rally(r: Reader, ts: float, hdr: dict) -> dict:
    """state_id=0x15 — ReadRally (set rally point on a building).

    Format: Int uid, Bool rally, Float posx, Float posz.
    Note: NO bFromServer field (verified against writerally.inc).
    """
    uid = r.i32()
    rally = r.boolean()
    posx = r.f32()
    posz = r.f32()
    return {**_ctx_from(ts, hdr), "handler": "ReadRally",
            "building_uid": uid, "rally_on": rally, "pos": [posx, posz]}


def decode_apply(r: Reader, ts: float, hdr: dict) -> dict:
    """state_id=??? — ReadApply (apply finished upgrade)."""
    plind = r.i32(); uid = r.i32(); cid = r.i32(); ind = r.i32()
    return {**_ctx_from(ts, hdr), "handler": "ReadApply",
            "target_plind": plind, "target_uid": uid,
            "upgrade_cid": cid, "upgrade_ind": ind}


def decode_upgrade(r: Reader, ts: float, hdr: dict) -> dict:
    """state_id=??? — ReadUpgrade (start or cancel research)."""
    bFromServer = r.boolean()
    upgid = r.i32()
    state = r.boolean()
    count = r.i32()
    buildings = [r.i32() for _ in range(count)]
    return {**_ctx_from(ts, hdr), "handler": "ReadUpgrade",
            "upgrade_id": upgid, "start": state,
            "buildings": buildings, "from_server": bFromServer}


def decode_search(r: Reader, ts: float, hdr: dict) -> dict:
    """state_id=??? — ReadSearch (toggle search-enemy mode)."""
    state = r.boolean()
    count = r.i32()
    uids = [r.i32() for _ in range(count)]
    return {**_ctx_from(ts, hdr), "handler": "ReadSearch",
            "search_on": state, "units": uids}


def decode_stand(r: Reader, ts: float, hdr: dict) -> dict:
    """state_id=??? — ReadStand (toggle stand-ground)."""
    state = r.boolean()
    count = r.i32()
    uids = [r.i32() for _ in range(count)]
    return {**_ctx_from(ts, hdr), "handler": "ReadStand",
            "stand_on": state, "units": uids}


def decode_stop(r: Reader, ts: float, hdr: dict) -> dict:
    """state_id=??? — ReadStop (cancel orders)."""
    count = r.i32()
    uids = [r.i32() for _ in range(count)]
    return {**_ctx_from(ts, hdr), "handler": "ReadStop", "units": uids}


def decode_produce(r: Reader, ts: float, hdr: dict) -> dict:
    """state_id=??? — ReadProduce (queue unit for production)."""
    proid = r.i32(); prcid = r.i32(); amoun = r.i32()
    state = r.boolean()
    count = r.i32()
    buildings = [r.i32() for _ in range(count)]
    return {**_ctx_from(ts, hdr), "handler": "ReadProduce",
            "proid": proid, "prcid": prcid, "amount": amoun,
            "state": state, "buildings": buildings}


def decode_player(r: Reader, ts: float, hdr: dict) -> dict:
    """state_id=0x13 — ReadPlayer (transfer ownership / capture).

    Format: Int uid, Bool cap. Often appears in batches inside one entry —
    e.g. capturing 6 units = 6 nested ReadPlayer sub-packages.
    """
    uid = r.i32(); cap = r.boolean()
    return {**_ctx_from(ts, hdr), "handler": "ReadPlayer",
            "uid": uid, "capture": cap}


def decode_death(r: Reader, ts: float, hdr: dict) -> dict:
    """state_id=0x11 — ReadDeath.

    Format: Bool bFromServer, Int mode, Float randkey, Int count, N*Int uids.
    """
    bFromServer = r.boolean()
    mode = r.i32()
    randkey = r.f32()
    count = r.i32()
    uids = [r.i32() for _ in range(count)]
    return {**_ctx_from(ts, hdr), "handler": "ReadDeath",
            "mode": mode, "randkey": randkey,
            "dead_uids": uids, "from_server": bFromServer}


def decode_upgrade(r: Reader, ts: float, hdr: dict) -> dict:
    """state_id=0x19 — ReadUpgrade (start/cancel research).

    Format: Bool bFromServer, Int upgid, Bool state, Int count, N*Int building-uids.
    state=true means "start research", false means "cancel".
    """
    bFromServer = r.boolean()
    upgid = r.i32()
    state = r.boolean()
    count = r.i32()
    buildings = [r.i32() for _ in range(count)]
    return {**_ctx_from(ts, hdr), "handler": "ReadUpgrade",
            "upgrade_id": upgid, "start": state,
            "buildings": buildings, "from_server": bFromServer}


def decode_sync_units_params(r: Reader, ts: float, hdr: dict) -> dict:
    """state_id=0x3d — ReadSyncUnitsParams (HP sync for multiple units).

    Format: Int count + N*(Int uid + Bool bvalid + Int hp).
    """
    count = r.i32()
    updates = []
    for _ in range(count):
        uid = r.i32()
        bvalid = r.boolean()
        hp = r.i32()
        updates.append({"uid": uid, "valid": bvalid, "hp": hp})
    return {**_ctx_from(ts, hdr), "handler": "ReadSyncUnitsParams",
            "hp_updates": updates}


def decode_trade(r: Reader, ts: float, hdr: dict) -> dict:
    """state_id=0x31 — ReadTrade (resource trade on market).

    Format: Bool bFromServer, Byte sell, Byte buy, Int amount.
    sell/buy are gc_resource_type_* indices (1=food, 2=wood, 3=stone, 4=gold,
    5=iron, 6=coal).
    """
    bFromServer = r.boolean()
    sell = r.u8()
    buy = r.u8()
    amount = r.i32()
    return {**_ctx_from(ts, hdr), "handler": "ReadTrade",
            "sell_res": sell, "buy_res": buy, "amount": amount,
            "from_server": bFromServer}


def decode_leave(r: Reader, ts: float, hdr: dict) -> dict:
    """state_id=0x27 — ReadLeave (unit goes outside of a building).

    Format: Bool dead, Int uid.
    """
    dead = r.boolean()
    uid = r.i32()
    return {**_ctx_from(ts, hdr), "handler": "ReadLeave",
            "dead": dead, "uid": uid}


def decode_newp(r: Reader, ts: float, hdr: dict) -> dict:
    """state_id=0x2d — ReadNewP (spawn primitive: field, balloon, ship-dummy).

    Format: Bool bFromServer, String race, String base, Float posx, posz, roll,
    Int plind, Int id, Int uid, Int num.

    Entries with state_id=0x2d usually contain MANY nested ReadNewP packages
    (e.g. when planting a row of fields, the engine writes one ReadNewP per
    field cell, all into one entry).
    """
    bFromServer = r.boolean()
    race = r.string()
    base = r.string()
    posx = r.f32(); posz = r.f32(); roll = r.f32()
    plind = r.i32(); id_ = r.i32(); uid = r.i32(); num = r.i32()
    return {**_ctx_from(ts, hdr), "handler": "ReadNewP",
            "race": race, "sid": base, "pos": [posx, posz], "roll": roll,
            "plind": plind, "id": id_, "uid": uid, "num_units_total": num,
            "from_server": bFromServer}


def decode_search(r: Reader, ts: float, hdr: dict) -> dict:
    """state_id=0x1d — ReadSearch (toggle search-enemy mode)."""
    state = r.boolean()
    count = r.i32()
    uids = [r.i32() for _ in range(count)]
    return {**_ctx_from(ts, hdr), "handler": "ReadSearch",
            "search_on": state, "units": uids}


def decode_stand(r: Reader, ts: float, hdr: dict) -> dict:
    """state_id=0x1f — ReadStand (toggle stand-ground)."""
    state = r.boolean()
    count = r.i32()
    uids = [r.i32() for _ in range(count)]
    return {**_ctx_from(ts, hdr), "handler": "ReadStand",
            "stand_on": state, "units": uids}


def decode_stop(r: Reader, ts: float, hdr: dict) -> dict:
    """state_id=0x2f — ReadStop."""
    count = r.i32()
    uids = [r.i32() for _ in range(count)]
    return {**_ctx_from(ts, hdr), "handler": "ReadStop", "units": uids}


def decode_gate(r: Reader, ts: float, hdr: dict) -> dict:
    """state_id=0x35 — ReadGate (open/close gates)."""
    state = r.boolean()
    count = r.i32()
    uids = [r.i32() for _ in range(count)]
    return {**_ctx_from(ts, hdr), "handler": "ReadGate",
            "open": state, "gates": uids}


def decode_leaveorder(r: Reader, ts: float, hdr: dict) -> dict:
    """state_id=0x25 — ReadLeaveOrder (list of units leaving building)."""
    dead = r.boolean()
    count = r.i32()
    uids = [r.i32() for _ in range(count)]
    return {**_ctx_from(ts, hdr), "handler": "ReadLeaveOrder",
            "dead": dead, "uids": uids}


def decode_free(r: Reader, ts: float, hdr: dict) -> dict:
    """state_id=0x0f — ReadFree (destroy game object).

    NB: pid=14 (engine progress) events with state_id=0x0f have a much
    larger payload that DOESN'T follow this signature. Those are
    engine-internal state-machine transitions, not actual ReadFree calls.
    """
    uid = r.i32()
    num = r.i32()
    return {**_ctx_from(ts, hdr), "handler": "ReadFree",
            "uid": uid, "num_total": num}


def decode_projfree(r: Reader, ts: float, hdr: dict) -> dict:
    """state_id=0x2b — ReadProjFree (projectile destroyed)."""
    uid = r.i32()
    num = r.i32()
    return {**_ctx_from(ts, hdr), "handler": "ReadProjFree",
            "proj_uid": uid, "num_total": num}


def decode_peacetime(r: Reader, ts: float, hdr: dict) -> dict:
    """state_id=0x39 — ReadPeaceTime (peace mode toggle)."""
    state = r.boolean()
    return {**_ctx_from(ts, hdr), "handler": "ReadPeaceTime",
            "peacemode_on": state}


def decode_package(r: Reader, ts: float, hdr: dict) -> dict:
    """state_id=0x40 — ReadPackage (generic text net-message)."""
    bFromServer = r.boolean()
    msg = r.string()
    return {**_ctx_from(ts, hdr), "handler": "ReadPackage",
            "from_server": bFromServer, "message": msg}


def decode_traderesources(r: Reader, ts: float, hdr: dict) -> dict:
    """state_id=0x46 — ReadTradeResources (transfer resources to ally)."""
    bFromServer = r.boolean()
    plind = r.u8()
    targetplayer = r.u8()
    resource = r.u8()
    amount = r.i32()
    return {**_ctx_from(ts, hdr), "handler": "ReadTradeResources",
            "from_pl": plind, "to_pl": targetplayer,
            "resource": resource, "amount": amount,
            "from_server": bFromServer}


def decode_proj(r: Reader, ts: float, hdr: dict) -> dict:
    """state_id=0x29 — ReadProj (projectile fired).

    Format (61 bytes body):
      Int uid (shooter), Int trguid (target uid or 0), Bool busetrgpos,
      3*Float (sx, sy, sz) source pos including height,
      Int weaponid,
      3*Float (tx, ty, tz) target pos,
      Int cid, Int id, Int weapind, Float randkey,
      Int projuid (assigned to new projectile), Int num.

    Records every musket shot / arrow / cannonball.
    """
    uid = r.i32()
    trguid = r.i32()
    busetrgpos = r.boolean()
    sx = r.f32(); sy = r.f32(); sz = r.f32()
    weaponid = r.i32()
    tx = r.f32(); ty = r.f32(); tz = r.f32()
    cid = r.i32(); id_ = r.i32(); weapind = r.i32()
    randkey = r.f32()
    projuid = r.i32(); num = r.i32()
    return {**_ctx_from(ts, hdr), "handler": "ReadProj",
            "shooter_uid": uid, "target_uid": trguid,
            "use_target_pos": busetrgpos,
            "source_pos": [sx, sy, sz],
            "weapon_id": weaponid,
            "target_pos": [tx, ty, tz],
            "cid": cid, "id": id_, "weapon_index": weapind,
            "randkey": randkey,
            "proj_uid": projuid, "num_total": num}


def decode_freelist(r: Reader, ts: float, hdr: dict) -> dict:
    """state_id=0x37 — ReadFreeList (mass-delete game objects).

    Format: Int count + N*Int uids. Used for cleanup (e.g. dead units,
    cancelled construction).
    """
    count = r.i32()
    uids = [r.i32() for _ in range(count)]
    return {**_ctx_from(ts, hdr), "handler": "ReadFreeList",
            "freed_uids": uids}


def decode_wall(r: Reader, ts: float, hdr: dict) -> dict:
    """state_id=0x33 — ReadWall (build wall cluster of cells).

    Format: Bool bFromServer, Byte usage, Byte cid, Byte id, Int count,
    count*(Byte sprite + Float px + Float pz + Int gouid), Int num, Int peasantcount,
    peasantcount*Int hnduids.
    """
    bFromServer = r.boolean()
    usage = r.u8()
    cid = r.u8()
    id_ = r.u8()
    count = r.i32()
    cells = []
    for _ in range(count):
        sprite = r.u8()
        px = r.f32(); pz = r.f32()
        gouid = r.i32()
        cells.append({"sprite": sprite, "pos": [px, pz], "gouid": gouid})
    num = r.i32()
    peasantcount = r.i32()
    builders = [r.i32() for _ in range(peasantcount)]
    return {**_ctx_from(ts, hdr), "handler": "ReadWall",
            "wall_usage": usage, "cid": cid, "id": id_,
            "cells": cells, "num_units_total": num,
            "builders": builders, "from_server": bFromServer}


def decode_move(r: Reader, ts: float, hdr: dict) -> dict:
    """state_id=??? — ReadMove (move units)."""
    dirx = r.f32(); dirz = r.f32()
    addo = r.boolean(); dofirst = r.boolean()
    mode = r.i32(); count = r.i32()
    moves = []
    for _ in range(count):
        u = r.i32(); x = r.f32(); z = r.f32()
        moves.append({"uid": u, "pos": [x, z]})
    # version-gated squad fields
    squaduid = r.u16() if r.remaining() >= 2 else 0
    plind = r.u8() if squaduid > 0 and r.remaining() >= 1 else None
    return {**_ctx_from(ts, hdr), "handler": "ReadMove",
            "facing": [dirx, dirz], "append": addo, "dofirst": dofirst,
            "mode": mode, "moves": moves,
            "squad_uid": squaduid, "squad_plind": plind}


# State_id → decoder dispatch. The state_id-to-name correspondence is
# fixed by the order of sections in data/scripts/units/global.aix;
# decoders implement the typed-field signature declared in each
# read*.inc handler.
DECODERS: dict[int, callable] = {
    0x21: decode_construct,         # ✓ ReadConstruct
    0x0d: decode_new,               # ✓ ReadNew
    0x15: decode_rally,             # ✓ ReadRally
    0x17: decode_order,             # ✓ ReadOrder
    0x23: decode_apply,             # ✓ ReadApply
    0x1b: decode_produce,           # ✓ ReadProduce
    0x11: decode_death,             # ✓ ReadDeath (13+4N body, randkey is RNG seed restore)
    0x19: decode_upgrade,           # ✓ ReadUpgrade (10+4N body)
    0x3d: decode_sync_units_params, # ✓ ReadSyncUnitsParams (HP sync per uid)
    0x31: decode_trade,             # ✓ ReadTrade (Bool+2*Byte+Int=7 body)
    0x27: decode_leave,             # ✓ ReadLeave (Bool+Int=5 body)
    0x13: decode_player,            # ✓ ReadPlayer (5B body — multiple nested in one entry)
    0x2d: decode_newp,              # ✓ ReadNewP (race+base, multi-pkg envelope for fields)
    0x33: decode_wall,              # ✓ ReadWall (wall cluster with per-cell records)
    0x37: decode_freelist,          # ✓ ReadFreeList (mass-delete; see end-game cleanup)
    0x29: decode_proj,              # ✓ ReadProj (projectile fired — every musket shot)
    0x0b: decode_move,              # ✓ ReadMove (per-unit destination)
    0x0f: decode_free,              # ✓ ReadFree (single object destroy)
    0x1d: decode_search,            # ✓ ReadSearch (search-enemy toggle)
    0x1f: decode_stand,             # ✓ ReadStand (stand-ground toggle)
    0x25: decode_leaveorder,        # ✓ ReadLeaveOrder
    0x2b: decode_projfree,          # ✓ ReadProjFree
    0x2f: decode_stop,              # ✓ ReadStop
    0x35: decode_gate,              # ✓ ReadGate
    0x39: decode_peacetime,         # ✓ ReadPeaceTime (peace mode end)
    0x40: decode_package,           # ✓ ReadPackage (text net-message)
    0x46: decode_traderesources,    # ✓ ReadTradeResources (ally transfer)
}


# ----- Class=0x09 decoder (per-object state-sync stream) -----------------
def decode_class_09(payload: bytes, ts: float) -> dict:
    """[0x09][u24 seq][u32 count][records]."""
    r = Reader(payload, 0)
    _ = r.u8()
    seq = r.u24()
    count = r.u32()
    total_rec_bytes = len(payload) - 8
    rec_size = total_rec_bytes // count if count > 0 else 0
    records = []
    for _ in range(count):
        if r.remaining() < rec_size: break
        if rec_size >= 4:
            uid = r.u32()
            rest = r.data[r.pos:r.pos + rec_size - 4]
            r.pos += len(rest)
            # Decode first 8 / 16 bytes pattern
            rec = {"uid": uid}
            if rec_size >= 8:
                rec["statestag"] = struct.unpack_from("<I", rest, 0)[0]
            if rec_size >= 16:
                rec["pos"] = list(struct.unpack_from("<ff", rest, 4))
            if rec_size > 16:
                rec["rest_hex"] = rest[12:].hex()
            records.append(rec)
    return {"handler": "class_09_sync", "ts_tick": ts, "ts_g_sec": ts / 10.0,
            "seq": seq, "count": count, "rec_size": rec_size, "records": records}


# ----- Sub-package walker (multi-package within an entry) ----------------
def decode_subpackages(payload: bytes, ts: float) -> list[dict]:
    """Walk all sub-packages in an entry. Returns list of decoded dicts."""
    results: list[dict] = []
    r = Reader(payload, 0)

    while r.remaining() > 0:
        if r.data[r.pos] == 0x09:
            # class=0x09 sub-package: read [seq u24][count u32][records]
            # Records consume rest of entry — we can't easily know inner size
            # without parsing each record. For now, consume to end-of-entry.
            start = r.pos
            sub_bytes = r.data[start:]
            results.append(decode_class_09(sub_bytes, ts))
            r.pos = len(r.data)
            break

        if r.remaining() < 5:
            results.append({"handler": "tiny_residue",
                            "size": r.remaining(),
                            "raw": r.data[r.pos:].hex()})
            break

        cls = r.u8()
        if cls != 0x00:
            results.append({"handler": f"unknown_class_0x{cls:02x}",
                            "raw_first_16": r.data[r.pos-1:r.pos+15].hex()})
            break
        sub = r.u8()
        pid = r.u8()
        state_id = r.u8()
        begin = r.u8()  # expected 0x00
        if sub != 0x03 or begin != 0x00:
            results.append({"handler": f"unknown_sub_0x{sub:02x}_begin_0x{begin:02x}",
                            "state_id_hex": f"0x{state_id:02x}",
                            "raw_first_16": r.data[r.pos-5:r.pos+11].hex()})
            # Skip to next begin? For now, stop.
            break

        hdr = {"class": cls, "pid": pid, "state_id": state_id}
        body_start = r.pos
        state_name = STATE_NAMES.get(state_id, f"unknown_0x{state_id:02x}")
        decoder = DECODERS.get(state_id)

        # pid=14 (progress) events use state_ids as labels for engine-internal
        # state-machine transitions; payload format DOES NOT match the script
        # handler signature. We skip decoding for these and just label them.
        engine_internal = pid == 14

        if decoder is None or engine_internal:
            # Find next sub-pkg by scanning for `01 00 03` (end + next start)
            tail = r.data[body_start:]
            next_start = tail.find(b"\x01\x00\x03")
            if next_start >= 0:
                consumed = next_start + 1
            else:
                consumed = len(tail)
            label = (f"engine_{state_name}" if engine_internal
                     else (state_name if decoder is None else f"undecoded_{state_name}"))
            results.append({**_ctx_from(ts, hdr),
                            "handler": label,
                            "size": consumed,
                            "raw_first_24": tail[:24].hex()})
            r.pos += consumed
            continue

        try:
            rec = decoder(r, ts, hdr)
            # Expect 0x01 end-marker
            if r.remaining() >= 1 and r.data[r.pos] == SUBPKG_END:
                r.pos += 1  # consume end-marker
                rec["end_marker_ok"] = True
            else:
                rec["end_marker_ok"] = False
                rec["end_marker_actual"] = (f"0x{r.data[r.pos]:02x}"
                                            if r.remaining() else "EOF")
            results.append(rec)
        except (struct.error, IndexError, UnicodeDecodeError, ValueError) as e:
            results.append({**_ctx_from(ts, hdr),
                            "handler": f"decode_error_state_0x{state_id:02x}",
                            "error": str(e),
                            "raw_first_24": payload[body_start:body_start+24].hex()})
            # Skip to next sub-pkg via heuristic
            tail = payload[body_start:]
            next_start = tail.find(b"\x01\x00\x03")
            if next_start >= 0:
                r.pos = body_start + next_start + 1
            else:
                r.pos = len(payload)
            continue
    return results


# ----- Entry walker ------------------------------------------------------
def walk_entries(data: bytes) -> list[tuple[float, int, bytes]]:
    entries: list[tuple[float, int, bytes]] = []
    i = 0
    while True:
        j = data.find(ENTRY_MARKER, i)
        if j < 0: break
        if j >= 8:
            ts = struct.unpack_from("<f", data, j-8)[0]
            size = struct.unpack_from("<I", data, j-4)[0]
            if 0 < size <= 0x100000 and j + 10 + size <= len(data):
                payload = data[j+10:j+10+size]
                entries.append((ts, size, payload))
        i = j + 1
    return entries


_UPGRADE_NAME_CACHE: dict | None = None


def _load_upgrade_names() -> dict:
    """Load `(nation_sid, upgrade_index) → {sid, name_ru, name_en, place, member}`
    once per process. The data.json upgrade list is ordered per-nation in
    the same sequence the engine builds `gCountry[cid].upgrade[]`, so the
    list-index equals the engine's `upgrade_id` argument seen in replays.
    """
    global _UPGRADE_NAME_CACHE
    if _UPGRADE_NAME_CACHE is not None:
        return _UPGRADE_NAME_CACHE
    candidates = [
        Path(__file__).resolve().parent.parent / "data.json",
        Path("/c3/data.json"),  # Pyodide virtual FS layout
        Path("data.json"),
    ]
    for path in candidates:
        if path.exists():
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                continue
            by_nation: dict[str, list[dict]] = {}
            for u in data.get("upgrades", []):
                nation = u.get("nation")
                if nation:
                    by_nation.setdefault(nation, []).append(u)
            _UPGRADE_NAME_CACHE = by_nation
            return by_nation
    _UPGRADE_NAME_CACHE = {}
    return {}


# gCountry cid → nation sid, matches NATION_ID_TO_SID in parser/config.py.
NATION_BY_CID = {
    0: "aus",  1: "fra",  2: "eng",  3: "spa",  4: "rus",  5: "ukr",
    6: "pol",  7: "swe",  8: "pru",  9: "ven",  10: "tur", 11: "alg",
    12: "mis", 13: "net", 14: "den", 15: "por", 16: "pie", 17: "sax",
    18: "bav", 19: "hun", 20: "swi", 21: "sco", 22: "tat", 23: "lit",
}


def _resolve_upgrade(cid: int, upgrade_id: int) -> dict | None:
    """Look up upgrade metadata by country index + upgrade index."""
    nation = NATION_BY_CID.get(cid)
    if not nation:
        return None
    upgrades = _load_upgrade_names().get(nation)
    if not upgrades or upgrade_id < 0 or upgrade_id >= len(upgrades):
        return None
    return upgrades[upgrade_id]


def _build_player_nations(decoded: list[dict]) -> dict[int, str]:
    """Infer each player's nation from the sid of their first ReadConstruct.

    Building sids are prefixed by the nation tag (`auscen`, `piebar`, ...);
    same for many unit sids. The first three letters are the canonical
    nation tag used as `gCountry[cid].sid`.
    """
    nations: dict[int, str] = {}
    for rec in decoded:
        if rec.get("handler") != "ReadConstruct":
            continue
        pid = rec.get("pid")
        sid = rec.get("sid", "")
        if pid is None or len(sid) < 3 or pid in nations:
            continue
        nations[pid] = sid[:3]
    return nations


def _build_uid_index(decoded: list[dict]) -> dict[int, dict]:
    """Map runtime UID → spawn metadata for every object we see spawned.
    Used to translate abuse-finding building_uid'ы into sids.
    """
    out: dict[int, dict] = {}
    for rec in decoded:
        h = rec.get("handler")
        if h in ("ReadNew", "ReadNewP"):
            uid = rec.get("uid")
            if uid:
                out[uid] = {"sid": rec.get("sid", ""), "kind": h,
                            "race": rec.get("race", ""), "pid": rec.get("pid")}
    return out


def detect_abuses(decoded: list[dict], player_nations: dict[int, str] | None = None) -> list[dict]:
    """Scan decoded sub-package list for known multiplayer-abuse patterns.

    Currently detects:

    - **double-upgrade-start**: two `ReadUpgrade` events with `start=True`
      for the same `(pid, building_uid, upgrade_id)` within
      `DOUBLE_UPGRADE_WINDOW_TICKS` ticks. This is the canonical
      race-condition exploit where a non-host client spams the upgrade
      button as it nears completion and forces the host to queue the
      research more than once.
    - **double-apply**: two `ReadApply` events for the same
      `(target_uid, upgrade_cid, upgrade_ind)`. Each `ReadApply` invokes
      `_player_ApplyUpgrade`, which has no idempotency check and
      compounds the effect on every call.

    Returns a list of findings; each finding is a dict with:
        kind, pid, ts_g_sec_first, ts_g_sec_second, gap_ticks, details
    """
    # Race-condition abuse fingerprint:
    #   - exactly 2 starts of the same (pid, building, upgrade) — the
    #     second one is the spammed extra click that landed during the
    #     "almost complete" window.
    #   - gap between starts is roughly one upgrade-completion-cycle —
    #     between 50 ticks (5 g-сек) and 200 ticks (20 g-сек).
    #
    # Below 50 ticks the cluster looks like legitimate spam-hire on a
    # queueable upgrade — mercenary purchase at a diplomatic centre, or
    # peasant-absorber slots on a mine — both fire `ReadUpgrade` per click
    # at sub-tick spacing and pack tens of starts into one second.
    # Above 200 ticks the pair is too far apart to be the same lifecycle.
    GAP_MIN_TICKS = 50
    GAP_MAX_TICKS = 200
    findings: list[dict] = []

    # Index ReadUpgrade(start=True) events
    upgrade_starts: dict[tuple, list[dict]] = {}
    for rec in decoded:
        if rec.get("handler") != "ReadUpgrade":
            continue
        if not rec.get("start"):
            continue
        for bld in rec.get("buildings", []):
            key = (rec["pid"], bld, rec["upgrade_id"])
            upgrade_starts.setdefault(key, []).append(rec)

    for key, events in upgrade_starts.items():
        if len(events) != 2:
            # >2 starts → almost certainly a queueable hire (merc, miner);
            # singletons obviously aren't duplicates.
            continue
        events_sorted = sorted(events, key=lambda r: r["ts_tick"])
        a, b = events_sorted
        gap = b["ts_tick"] - a["ts_tick"]
        if gap < GAP_MIN_TICKS or gap > GAP_MAX_TICKS:
            continue
        pid, bld_uid, upg_id = key
        upg_meta = None
        if player_nations and pid in player_nations:
            nation = player_nations[pid]
            upgrades = _load_upgrade_names().get(nation)
            if upgrades and 0 <= upg_id < len(upgrades):
                upg_meta = upgrades[upg_id]
        details = {"building_uid": bld_uid, "upgrade_id": upg_id}
        if upg_meta:
            details["upgrade_sid"] = upg_meta.get("sid")
            details["upgrade_name_ru"] = upg_meta.get("name_ru") or ""
            details["upgrade_name_en"] = upg_meta.get("name_en") or ""
            details["place"] = upg_meta.get("place")
        findings.append({
            "kind": "double-upgrade-start",
            "pid": pid,
            "ts_g_sec_first": round(a["ts_g_sec"], 2),
            "ts_g_sec_second": round(b["ts_g_sec"], 2),
            "gap_ticks": round(gap, 2),
            "details": details,
        })

    # Same logic for ReadApply: a real race-condition apply lands in the
    # same gap window as the duplicate start, from the same pid, and only
    # twice (queueable hires can apply many times legitimately).
    # Skip zero-tuple records — those are engine-stub events with garbage
    # body that decode to (0, 0, 0).
    apply_seen: dict[tuple, list[dict]] = {}
    for rec in decoded:
        if rec.get("handler") != "ReadApply":
            continue
        tgt = rec["target_uid"]; cid = rec["upgrade_cid"]; ind = rec["upgrade_ind"]
        if tgt == 0 and cid == 0 and ind == 0:
            continue
        # Bound check — sub-package garbage parsed as ReadApply produces
        # uint32-sized values that aren't valid uids or country/upgrade indices.
        if not (0 < tgt < 0x100000):
            continue
        if not (0 <= cid < 256 and 0 <= ind < 4096):
            continue
        apply_seen.setdefault((tgt, cid, ind), []).append(rec)

    for key, events in apply_seen.items():
        if len(events) != 2:
            continue
        events_sorted = sorted(events, key=lambda r: r["ts_tick"])
        a, b = events_sorted
        if a["pid"] != b["pid"]:
            continue
        gap = b["ts_tick"] - a["ts_tick"]
        if gap < GAP_MIN_TICKS or gap > GAP_MAX_TICKS:
            continue
        tgt_uid, cid, ind = key
        details = {"target_uid": tgt_uid, "cid": cid, "ind": ind}
        upg_meta = _resolve_upgrade(cid, ind)
        if upg_meta:
            details["upgrade_sid"] = upg_meta.get("sid")
            details["upgrade_name_ru"] = upg_meta.get("name_ru") or ""
            details["upgrade_name_en"] = upg_meta.get("name_en") or ""
            details["place"] = upg_meta.get("place")
            details["nation"] = NATION_BY_CID.get(cid)
        findings.append({
            "kind": "double-apply",
            "pid": b["pid"],
            "ts_g_sec_first": round(a["ts_g_sec"], 2),
            "ts_g_sec_second": round(b["ts_g_sec"], 2),
            "gap_ticks": round(gap, 2),
            "details": details,
        })

    return findings


def parse_replay_from_bytes(data: bytes) -> dict:
    """Comprehensive replay parse from raw bytes.

    Returns a JSON-friendly dict with header settings, player roster,
    event timelines, summaries and abuse findings — everything a web
    UI needs in one round-trip.
    """
    # Import lazily so this module remains importable on its own
    from parse_replay import extract_settings, extract_players

    settings = extract_settings(data)
    players = extract_players(data)
    entries = walk_entries(data)
    body_entries = entries[1:] if entries and entries[0][0] == 0.0 else entries

    decoded: list[dict] = []
    by_handler: Counter = Counter()
    by_pid: Counter = Counter()
    for ts, _size, payload in body_entries:
        for rec in decode_subpackages(payload, ts):
            decoded.append(rec)
            by_handler[rec.get("handler", "?")] += 1
            if "pid" in rec:
                by_pid[rec["pid_name"]] += 1

    # Per-player aggregations
    builds_per_pid: dict = defaultdict(list)
    units_built_per_pid: dict = defaultdict(Counter)
    spawns_per_pid: dict = defaultdict(Counter)
    orders_per_pid: dict = defaultdict(Counter)
    trades_per_pid: dict = defaultdict(list)
    upgrades_per_pid: dict = defaultdict(list)
    deaths_per_pid: Counter = Counter()
    proj_per_pid: Counter = Counter()
    rally_per_pid: dict = defaultdict(int)

    for rec in decoded:
        h = rec.get("handler")
        pid = rec.get("pid")
        if h == "ReadConstruct" and pid is not None:
            builds_per_pid[pid].append({
                "ts_g_sec": rec["ts_g_sec"], "sid": rec["sid"],
                "pos": rec["pos"], "builders": len(rec["builders"]),
            })
            units_built_per_pid[pid][rec["sid"]] += 1
        elif h == "ReadNew" and pid is not None:
            spawns_per_pid[pid][rec["sid"]] += 1
        elif h == "ReadOrder" and pid is not None:
            orders_per_pid[pid][rec["ordtyp_name"]] += 1
        elif h == "ReadTrade" and pid is not None:
            trades_per_pid[pid].append({
                "ts_g_sec": rec["ts_g_sec"],
                "sell": rec["sell_res"], "buy": rec["buy_res"],
                "amount": rec["amount"],
            })
        elif h == "ReadUpgrade" and pid is not None:
            upgrades_per_pid[pid].append({
                "ts_g_sec": rec["ts_g_sec"],
                "upgrade_id": rec["upgrade_id"], "start": rec["start"],
                "buildings": rec["buildings"],
            })
        elif h == "ReadDeath" and pid is not None:
            deaths_per_pid[pid] += len(rec.get("dead_uids", []))
        elif h == "ReadProj" and pid is not None:
            proj_per_pid[pid] += 1
        elif h == "ReadRally" and pid is not None:
            rally_per_pid[pid] += 1

    player_nations = _build_player_nations(decoded)
    abuses = detect_abuses(decoded, player_nations)
    duration_g_sec = round(entries[-1][0] / 10.0, 2) if entries else 0.0

    return {
        "settings": settings,
        "players": players,
        "duration_g_sec": duration_g_sec,
        "n_entries": len(entries),
        "n_sub_packages": len(decoded),
        "by_handler": dict(by_handler.most_common()),
        "by_pid": dict(by_pid.most_common()),
        "builds_per_pid": {p: v for p, v in builds_per_pid.items()},
        "units_built_per_pid": {p: dict(v) for p, v in units_built_per_pid.items()},
        "spawns_per_pid": {p: dict(v) for p, v in spawns_per_pid.items()},
        "orders_per_pid": {p: dict(v) for p, v in orders_per_pid.items()},
        "trades_per_pid": {p: v for p, v in trades_per_pid.items()},
        "upgrades_per_pid": {p: v for p, v in upgrades_per_pid.items()},
        "deaths_per_pid": dict(deaths_per_pid),
        "proj_per_pid": dict(proj_per_pid),
        "rally_per_pid": dict(rally_per_pid),
        "abuses": abuses,
    }


def parse_replay_events(path: Path) -> dict:
    """Legacy file-path-based wrapper, used by CLI/aggregate scripts."""
    data = path.read_bytes()
    result = parse_replay_from_bytes(data)
    result["file"] = str(path)
    # Keep the older timeline-list shape too for CLI summary printing
    decoded: list[dict] = []
    for ts, _size, payload in walk_entries(data)[1:]:
        for rec in decode_subpackages(payload, ts):
            decoded.append(rec)
    result["build_timeline"] = sorted(
        (r for r in decoded if r.get("handler") == "ReadConstruct"),
        key=lambda r: r["ts_g_sec"])
    result["new_timeline_sample"] = sorted(
        (r for r in decoded if r.get("handler") == "ReadNew"),
        key=lambda r: r["ts_g_sec"])[:30]
    result["n_new_total"] = sum(1 for r in decoded if r.get("handler") == "ReadNew")
    result["order_timeline_sample"] = sorted(
        (r for r in decoded if r.get("handler") == "ReadOrder"),
        key=lambda r: r["ts_g_sec"])[:30]
    result["n_order_total"] = sum(1 for r in decoded if r.get("handler") == "ReadOrder")
    result["rally_timeline"] = sorted(
        (r for r in decoded if r.get("handler") == "ReadRally"),
        key=lambda r: r["ts_g_sec"])
    return result


def print_summary(result: dict, path: Path) -> None:
    print(f"=== {path.name} ===")
    print(f"  Entries:                {result['n_entries']:,}")
    print(f"  Sub-packages (decoded): {result['n_sub_packages']:,}")
    print(f"  Game duration:          {result['duration_g_sec']:.1f} g-sec "
          f"({result['duration_g_sec']/60:.1f} g-min)")

    print(f"\n  By handler:")
    for h, c in result["by_handler"].items():
        print(f"    {h:<35s} {c:6,}")

    print(f"\n  Class=0x00 state_id distribution:")
    for sid, c in list(result["by_state_id_hex"].items())[:15]:
        known = next((k for k, v in DECODERS.items() if f"0x{k:02x}" == sid), None)
        mark = " ✓" if known is not None else ""
        print(f"    {sid:>6s} {c:6,}{mark}")

    print(f"\n  By pid:")
    for pid, c in result["by_pid"].items():
        print(f"    {pid:<15s} {c:6,}")

    print(f"\n  Build-timeline ({len(result['build_timeline'])} events):")
    for ev in result["build_timeline"][:20]:
        print(f"    t={ev['ts_g_sec']:6.1f} pid={ev['pid']} "
              f"sid={ev['sid']:<12s} pos=({ev['pos'][0]:6.1f},{ev['pos'][1]:6.1f}) "
              f"builders={len(ev['builders'])}")

    print(f"\n  Order-timeline first 20 / {result['n_order_total']}:")
    for ev in result["order_timeline_sample"][:20]:
        pos = f" pos=({ev['pos'][0]:.0f},{ev['pos'][1]:.0f})" if ev.get("pos") else ""
        print(f"    t={ev['ts_g_sec']:6.1f} pid={ev['pid']} "
              f"{ev['ordtyp_name']:<14s} taruid={ev['target_uid']:>5} "
              f"units={len(ev['units'])}{pos}")

    print(f"\n  Rally points set ({len(result['rally_timeline'])}):")
    for ev in result["rally_timeline"][:20]:
        print(f"    t={ev['ts_g_sec']:6.1f} pid={ev['pid']} "
              f"bld_uid={ev['building_uid']:>5} on={ev['rally_on']} "
              f"pos=({ev['pos'][0]:6.1f},{ev['pos'][1]:6.1f})")


def main():
    if len(sys.argv) < 2:
        print("usage: parse_replay_events.py <file.rep> [--summary]")
        sys.exit(1)
    path = Path(sys.argv[1])
    flags = set(sys.argv[2:])
    sys.stdout.reconfigure(encoding="utf-8")

    result = parse_replay_events(path)

    if "--summary" in flags:
        print_summary(result, path)
    else:
        out_path = path.with_suffix(".events.json")
        out_path.write_text(
            json.dumps(result, indent=2, ensure_ascii=False),
            encoding="utf-8")
        print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
