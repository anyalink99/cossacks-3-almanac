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
    """state_id=??? — ReadPlayer (transfer ownership)."""
    uid = r.i32(); cap = r.boolean()
    return {**_ctx_from(ts, hdr), "handler": "ReadPlayer",
            "uid": uid, "capture": cap}


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


# Heuristic state_id → decoder. ReadConstruct (0x21), ReadNew (0x0d),
# ReadRally (0x15), ReadOrder (0x17) are EMPIRICALLY VERIFIED on
# nick-niotid 2.rep. Others are GUESSED by structural fit and may need
# correction.
DECODERS: dict[int, callable] = {
    0x21: decode_construct,  # ✓ verified on 89 events
    0x0d: decode_new,        # ✓ verified on 1776 events
    0x15: decode_rally,      # ✓ verified on 19 events
    0x17: decode_order,      # ✓ verified (ordtyp values in [0..20] enum)
    0x23: decode_apply,      # ✓ verified — 4 Integers match plind/uid/cid/ind
    0x1b: decode_produce,    # ✓ verified — amoun=-1 matches gc_obj_order_produce_infinite
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
        decoder = DECODERS.get(state_id)
        if decoder is None:
            # Unknown handler — record stub. Find next sub-pkg by scanning for
            # `00 03 XX XX 00` pattern, else dump rest.
            # Heuristic: look for `01 00 03` (end-marker + start of next pkg).
            tail = r.data[body_start:]
            next_start = tail.find(b"\x01\x00\x03")
            if next_start >= 0:
                consumed = next_start + 1  # include the 0x01 end-marker
            else:
                consumed = len(tail)
            results.append({**_ctx_from(ts, hdr),
                            "handler": f"unknown_state_0x{state_id:02x}",
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


def parse_replay_events(path: Path) -> dict:
    data = path.read_bytes()
    entries = walk_entries(data)
    body_entries = entries[1:] if entries and entries[0][0] == 0.0 else entries

    decoded: list[dict] = []
    by_handler: Counter = Counter()
    by_state_id: Counter = Counter()
    by_pid: Counter = Counter()
    by_state_id_per_pid: defaultdict = defaultdict(Counter)

    for ts, size, payload in body_entries:
        recs = decode_subpackages(payload, ts)
        for rec in recs:
            decoded.append(rec)
            by_handler[rec.get("handler", "?")] += 1
            if "pid" in rec:
                by_pid[rec["pid_name"]] += 1
        # Track entry's first state_id (a proxy)
        if len(payload) >= 4 and payload[0] == 0x00:
            by_state_id[payload[3]] += 1
            by_state_id_per_pid[payload[2]][payload[3]] += 1

    # Aggregated timelines
    build_timeline = sorted(
        (r for r in decoded if r.get("handler") == "ReadConstruct"),
        key=lambda r: r["ts_g_sec"])
    new_timeline = sorted(
        (r for r in decoded if r.get("handler") == "ReadNew"),
        key=lambda r: r["ts_g_sec"])
    order_timeline = sorted(
        (r for r in decoded if r.get("handler") == "ReadOrder"),
        key=lambda r: r["ts_g_sec"])
    rally_timeline = sorted(
        (r for r in decoded if r.get("handler") == "ReadRally"),
        key=lambda r: r["ts_g_sec"])

    return {
        "file": str(path),
        "n_entries": len(entries),
        "n_sub_packages": len(decoded),
        "duration_g_sec": round(entries[-1][0] / 10.0, 2) if entries else 0,
        "by_handler": dict(by_handler.most_common()),
        "by_state_id_hex": {f"0x{k:02x}": v for k, v in by_state_id.most_common()},
        "by_pid": dict(by_pid.most_common()),
        "state_id_breakdown_per_pid": {
            (f"player_{p}" if p < 12 else PSEUDO_PLAYERS.get(p, f"unknown_{p}")):
                {f"0x{sid:02x}": c for sid, c in cnt.most_common()}
            for p, cnt in sorted(by_state_id_per_pid.items())
        },
        "build_timeline": build_timeline,
        "new_timeline_sample": new_timeline[:30],
        "n_new_total": len(new_timeline),
        "order_timeline_sample": order_timeline[:30],
        "n_order_total": len(order_timeline),
        "rally_timeline": rally_timeline,
        "all_events": decoded if len(decoded) < 8000 else "[truncated — too many events]",
    }


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
