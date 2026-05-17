"""Parse a Cossacks 3 replay (.rep) or saved map (.map) file.

These files share the OSWMap13 format. Layout (RE'd from binary inspection):

- Header:
    [u32 = 53] "OSWMap13.Map.Ver[0.0]Build.Ver[X.Y.Z.NNNN]Core.Ver[1]"
    [u32]      "UID<digits>"
    [u32]      "GameMapSnapShotBegin"
    BMP image (full Windows DIB; starts with `BM` magic, size in BMP header)
    [u32]      "GameMapSnapShotEnd"
    [u32]      "GameMapRecordBegin"
    ... key-value pairs + nested sections ...
    [u32]      "GameMapRecordEnd"

- Inside `GameMapRecordBegin`, data is serialized as (length-prefixed-string)
  pairs of (key, value) where both key and value are u32-LE-len + ASCII bytes.
  Numeric values are ALSO stored as ASCII strings (e.g. randkey1 = "1176877135").

- All placed pattern instances appear as ASCII pattern names (e.g. `frt_b_p_1`,
  `d_stn_2`, `mng_3`) at various offsets — these are the patterns the engine
  actually selected for this game. Cross-reference with `derived/
  pattern_types.json` to count by pattern type (= GROUND TRUTH for map gen).

Usage:
    python parser/parse_replay.py <path>           # summary + ground truth
    python parser/parse_replay.py <path> --bmp     # also extract BMP thumbnail
    python parser/parse_replay.py <path> --strings # dump all readable strings
    python parser/parse_replay.py <path> --json    # output structured JSON

Use `--json` for empirical-validation pipelines (compute/validate_map_predictions.py).
"""
from __future__ import annotations
import struct
import sys
import re
from pathlib import Path


def read_lp_string(data: bytes, offset: int) -> tuple[str, int] | None:
    """Read a length-prefixed string starting at `offset`. Returns (str, end_offset)
    or None if implausible. Length is u32 LE."""
    if offset + 4 > len(data):
        return None
    n = struct.unpack_from("<I", data, offset)[0]
    if n <= 0 or n > 1024 or offset + 4 + n > len(data):
        return None
    raw = data[offset + 4 : offset + 4 + n]
    try:
        s = raw.decode("ascii")
    except UnicodeDecodeError:
        return None
    # Reject if it's mostly non-printable
    printable = sum(1 for c in s if 32 <= ord(c) < 127)
    if printable < n * 0.85:
        return None
    return s, offset + 4 + n


def parse_header(data: bytes) -> dict:
    """Parse the OSWMap13 header. Returns dict with version, uid, sections."""
    info: dict = {"size": len(data), "header": None, "uid": None, "sections": []}
    pos = 0
    first = read_lp_string(data, pos)
    if first is None:
        return info
    s, pos = first
    info["header"] = s
    # Parse Build.Ver from header
    m = re.search(r"Build\.Ver\[([^\]]+)\]", s)
    if m:
        info["build_version"] = m.group(1)
    m = re.search(r"OSWMap(\d+)", s)
    if m:
        info["map_format_version"] = int(m.group(1))
    # Next: UID (length-prefixed)
    nxt = read_lp_string(data, pos)
    if nxt and nxt[0].startswith("UID"):
        info["uid"] = nxt[0]
        pos = nxt[1]
    # Walk forward looking for known section markers
    # Markers we expect to see (length-prefixed):
    expected_markers = {
        "GameMapSnapShotBegin", "GameMapSnapShotEnd",
        "GameMapRecordBegin",   "GameMapRecordEnd",
    }
    while pos < len(data) - 4:
        s = read_lp_string(data, pos)
        if s and s[0] in expected_markers:
            info["sections"].append({"name": s[0], "offset": pos})
            pos = s[1]
            # If this is SnapShotBegin, expect a BMP next
            if s[0] == "GameMapSnapShotBegin":
                # skip the inner u32 (1) and find BMP
                if pos + 6 < len(data) and data[pos+4:pos+6] == b"BM":
                    bmp_size = struct.unpack_from("<I", data, pos + 6)[0]
                    info["bmp_offset"] = pos + 4
                    info["bmp_size"] = bmp_size
                    pos = pos + 4 + bmp_size
                    continue
        else:
            pos += 1  # scan byte by byte
    return info


def extract_strings(data: bytes, min_len: int = 4) -> list[tuple[int, str]]:
    """Find all printable ASCII strings of length ≥ min_len. Returns [(offset, str), ...].

    Uses regex over the raw bytes for ~100× speedup vs byte-by-byte loop on
    large (>10MB) replays.
    """
    pat = re.compile(rb"[\x20-\x7e]{%d,}" % min_len)
    return [(m.start(), m.group().decode("ascii")) for m in pat.finditer(data)]


def count_patterns_fast(data: bytes, pattern_set: set[str]) -> dict[str, int]:
    """Count occurrences of known pattern names by extracting all printable
    ASCII runs first (single regex, fast) then testing each against the set.

    This is dramatically faster than building a 700-pattern alternation regex
    over the raw bytes because:
      - extract_strings does ONE pass with a tiny regex `[\\x20-\\x7e]+`
      - python `set` lookup is O(1) per string
      - .pattern files in OSWMap13 are stored as length-prefixed strings,
        so they appear as printable runs that exactly match pattern names
    """
    if not pattern_set:
        return {}
    counts: dict[str, int] = {}
    for _, s in extract_strings(data, min_len=4):
        if s in pattern_set:
            counts[s] = counts.get(s, 0) + 1
    return counts


def is_ascii_str(b: bytes) -> bool:
    return all(32 <= c < 127 for c in b)


def extract_kv_pairs(data: bytes) -> list[tuple[int, str, str]]:
    """Walk file extracting all (u32 keylen, key, u32 vallen, value) pairs.
    Both keys and values are ASCII length-prefixed. Values are returned as
    strings (raw ASCII bytes); numeric values come pre-formatted (e.g. "1176877135").
    """
    out = []
    i = 0
    while i < len(data) - 8:
        klen = struct.unpack_from("<I", data, i)[0]
        if 1 <= klen <= 64 and i + 4 + klen + 4 < len(data):
            kbytes = data[i + 4 : i + 4 + klen]
            if is_ascii_str(kbytes):
                vlen = struct.unpack_from("<I", data, i + 4 + klen)[0]
                if 0 <= vlen <= 1024 and i + 4 + klen + 4 + vlen <= len(data):
                    vbytes = data[i + 4 + klen + 4 : i + 4 + klen + 4 + vlen]
                    if vlen == 0 or is_ascii_str(vbytes):
                        k = kbytes.decode("ascii")
                        v = vbytes.decode("ascii") if vlen else ""
                        if (
                            re.match(r"^[a-zA-Z0-9_.\-]+$", k)
                            and not k.endswith(("Begin", "End"))
                        ):
                            out.append((i, k, v))
                            i += 4 + klen + 4 + vlen
                            continue
        i += 1
    return out


def extract_settings(data: bytes) -> dict:
    """Extract known game settings from the kv pair stream."""
    pairs = extract_kv_pairs(data)
    settings: dict = {}
    keys_to_extract = {
        # Map / generator
        "randkey0", "randkey1", "maskname", "maskpath",
        "mapsize", "relieftype", "resourcemines", "terraintype", "season",
        "resourcestart",
        # Game / lobby rules — all the gc_mapsettings_* enums
        "limit", "gamespeed", "playerscount", "startid", "teams",
        "peacetime", "century18", "capture", "marketdip",
        "cannons", "balloon", "startingunits", "adviserassistant",
        "brating", "bbattle", "autosave", "dlcs",
    }
    seen = set()
    for off, k, v in pairs:
        if k in keys_to_extract and k not in seen:
            settings[k] = v
            seen.add(k)
    # Convert numeric strings to ints where reasonable
    for k in (
        "randkey0", "randkey1", "mapsize", "relieftype",
        "resourcemines", "terraintype", "season", "limit",
        "gamespeed", "playerscount", "startid", "teams",
        "resourcestart", "peacetime", "century18", "capture",
        "marketdip", "cannons", "balloon", "startingunits",
        "adviserassistant", "autosave", "dlcs",
    ):
        if k in settings:
            try:
                settings[k] = int(settings[k])
            except (ValueError, TypeError):
                pass
    return settings


def extract_players(data: bytes) -> list[dict]:
    """Extract per-player metadata from kv pairs.

    The replay header carries 12 (= `gc_MaxPlayerCount`) sequential blocks
    of the `TMapPlayer` record: id, cid, csid, name, team, color, lanid,
    startx, starty, aidifficulty, bexists, bai, bhuman, bclosed, bready,
    bloaded, bleave (+ random-nation enable/options sic/snX/si1..si3).
    We walk the kv stream once, packing each player's fields together by
    the order they appear, then drop slots with `bexists=false`. The
    surviving slots' indices form the engine's runtime `pid`.

    Returns a list of {pid, name, lanid, team, color, csid, cid}.
    """
    pairs = extract_kv_pairs(data)
    # Skip leading game-level `name` ("game_v92k…") so the per-player
    # blocks start at the first true player slot.
    seen_game_name = False
    # Group consecutive (key, value) into slot dicts, starting a new slot
    # whenever we see `id` (the first field of TMapPlayer).
    slot_keys = ("id", "cid", "csid", "name", "team", "color", "lanid",
                 "startx", "starty", "aidifficulty",
                 "bexists", "bai", "bhuman", "bclosed",
                 "bready", "bloaded", "bleave")
    slots: list[dict] = []
    current: dict | None = None
    for _, k, v in pairs:
        if k == "name" and not seen_game_name and v.startswith("game_"):
            seen_game_name = True
            continue
        if k == "id":
            current = {"id": v}
            slots.append(current)
        elif current is not None and k in slot_keys:
            current[k] = v
    # The engine's runtime `pid` in event packets is the SLOT INDEX of
    # existing slots (filtered by bexists), not the explicit `id` field
    # inside TMapPlayer — the id field is something else (probably session
    # id or join order). We confirmed this empirically: known abusers in
    # ex1.rep land on slot-order pid, not id-order pid.
    out: list[dict] = []
    for idx, s in enumerate(slots):
        if str(s.get("bexists", "false")).lower() != "true":
            continue
        try:
            team_int = int(s.get("team", "-1"))
        except (ValueError, TypeError):
            team_int = -1
        try:
            color_int = int(s.get("color", "-1"))
        except (ValueError, TypeError):
            color_int = -1
        try:
            cid_int = int(s.get("cid", "-1"))
        except (ValueError, TypeError):
            cid_int = -1
        try:
            tmpid = int(s.get("id", "-1"))
        except (ValueError, TypeError):
            tmpid = -1
        out.append({
            "pid": len(out),  # engine pid = position in bexists-filtered list
            "name": s.get("name", ""),
            "lanid": s.get("lanid", ""),
            "team": team_int,
            "color": color_int,
            "csid": s.get("csid", ""),
            "cid": cid_int,
            "slot_idx": idx,
            "map_player_id": tmpid,
        })
    return out


def count_patterns(data: bytes, pattern_set: set[str]) -> dict:
    """Count occurrences of known pattern names in the data.

    `pattern_set` should be the keys of pattern_inventory.json. Returns
    {pattern_name: count}. Each occurrence in the file = one cluster placed.
    Delegates to count_patterns_fast (regex-based, ~100× faster on big files).
    """
    return count_patterns_fast(data, pattern_set)


def main():
    import json as _json
    if len(sys.argv) < 2:
        print("usage: parse_replay.py <file.rep|.map> [--bmp] [--strings] [--json]")
        sys.exit(1)
    path = Path(sys.argv[1])
    flags = set(sys.argv[2:])
    sys.stdout.reconfigure(encoding="utf-8")
    data = path.read_bytes()
    info = parse_header(data)

    # Settings
    settings = extract_settings(data)
    info["settings"] = settings

    # Pattern placements (require pattern_inventory.json from compute pipeline)
    inv_path = (Path(__file__).resolve().parent.parent
                / "output" / "derived" / "pattern_inventory.json")
    type_path = inv_path.parent / "pattern_types.json"
    pattern_counts: dict[str, int] = {}
    type_counts: dict[str, int] = {}
    if inv_path.exists():
        inv = _json.loads(inv_path.read_text(encoding="utf-8"))
        pattern_counts = count_patterns(data, set(inv.keys()))
    if type_path.exists() and pattern_counts:
        types = _json.loads(type_path.read_text(encoding="utf-8"))
        pattern_to_type = {}
        for tname, pats in types.items():
            for p in pats:
                pattern_to_type.setdefault(p, []).append(tname)
        for p, c in pattern_counts.items():
            for t in pattern_to_type.get(p, []):
                type_counts[t] = type_counts.get(t, 0) + c
                break  # one type per pattern

    if "--json" in flags:
        print(_json.dumps({
            "file": str(path),
            "size": info["size"],
            "build_version": info.get("build_version"),
            "uid": info.get("uid"),
            "settings": settings,
            "pattern_counts": pattern_counts,
            "type_counts": type_counts,
            "total_pattern_instances": sum(pattern_counts.values()),
        }, indent=2, sort_keys=True))
        return

    print(f"=== {path.name} ({info['size']:,} bytes) ===")
    print(f"Header: {info.get('header')}")
    print(f"Build:  {info.get('build_version', '?')}")
    print(f"UID:    {info.get('uid', '?')}")
    if settings:
        print(f"\nGame settings:")
        for k, v in sorted(settings.items()):
            print(f"  {k:<18} = {v}")
    if info.get("bmp_offset"):
        print(f"\nBMP thumbnail: @0x{info['bmp_offset']:x}, {info['bmp_size']:,} bytes")
        if "--bmp" in flags:
            bmp_path = path.with_suffix(".thumbnail.bmp")
            bmp_path.write_bytes(
                data[info["bmp_offset"] : info["bmp_offset"] + info["bmp_size"]]
            )
            print(f"  → wrote {bmp_path}")
    if pattern_counts:
        print(f"\nPattern placements: {sum(pattern_counts.values())} instances "
              f"({len(pattern_counts)} unique files)")
        print("\nBy pattern TYPE (from generator.cfg):")
        for t, c in sorted(type_counts.items(), key=lambda x: -x[1]):
            print(f"  {t:<35s} {c:>4d} clusters")
    if "--strings" in flags:
        strings = extract_strings(data, min_len=6)
        print(f"\nAll readable strings ≥ 6 chars: {len(strings)}")
        for off, s in strings[:100]:
            print(f"  @0x{off:08x}: {s[:120]}")


if __name__ == "__main__":
    main()
