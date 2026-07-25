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

- `PatternList` stores exact adjacent `n`/`x`/`y` key-value triplets for every
  selected map pattern (for example `mng_3` at generator coordinates -62,-80).
  Cross-reference names with `derived/pattern_types.json` to aggregate by
  pattern type (= GROUND TRUTH for map gen).

Usage:
    python parser/parse_replay.py <path>           # summary + ground truth
    python parser/parse_replay.py <path> --bmp     # also extract BMP thumbnail
    python parser/parse_replay.py <path> --strings # dump all readable strings
    python parser/parse_replay.py <path> --json    # output structured JSON

Use `--json` for empirical-validation pipelines (compute/validate_map_predictions.py).
"""
from __future__ import annotations
import math
import re
import struct
import sys
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


def _lp_marker(value: str) -> bytes:
    raw = value.encode("ascii")
    return struct.pack("<I", len(raw)) + raw


def _scan_lp_strings(
    data: bytes, start: int, end: int
) -> list[tuple[int, str, int]]:
    """Return plausible LP strings in [start, end), including their offsets."""
    out: list[tuple[int, str, int]] = []
    pos = max(0, start)
    end = min(end, len(data))
    while pos + 4 <= end:
        item = read_lp_string(data, pos)
        if item is not None and item[1] <= end:
            value, next_pos = item
            out.append((pos, value, next_pos))
            pos = next_pos
        else:
            pos += 1
    return out


def parse_footer(data: bytes) -> dict:
    """Parse the stable metadata footer following GameMapRecordEnd.

    The first f64 is deliberately exposed as ``elapsed_raw_s``: it is finite
    and time-like in every checked replay, but it does not equal the event
    stream's game-time duration and its exact clock semantics remain unknown.
    Malformed or truncated data returns an empty/partial dict instead of
    raising.
    """
    record_marker = _lp_marker("GameMapRecordEnd")
    record_offset = data.rfind(record_marker)
    if record_offset < 0:
        return {}

    record = read_lp_string(data, record_offset)
    if record is None or record[0] != "GameMapRecordEnd":
        return {}
    begin = read_lp_string(data, record[1])
    if begin is None or begin[0] != "GameMapBegin":
        return {}

    cursor = begin[1]
    if cursor + 12 > len(data):
        return {}
    elapsed_raw_s = struct.unpack_from("<d", data, cursor)[0]
    if not math.isfinite(elapsed_raw_s) or elapsed_raw_s < 0:
        return {}
    cursor += 8
    reserved0 = struct.unpack_from("<I", data, cursor)[0]
    cursor += 4

    project_name = read_lp_string(data, cursor)
    if project_name is None:
        return {}
    cursor = project_name[1]
    project_path = read_lp_string(data, cursor)
    if project_path is None:
        return {}
    cursor = project_path[1]

    end_marker = _lp_marker("GameMapEnd")
    game_map_end_offset = data.find(end_marker, cursor)
    scan_end = (
        game_map_end_offset + len(end_marker)
        if game_map_end_offset >= 0
        else len(data)
    )
    tokens = _scan_lp_strings(data, cursor, scan_end)

    footer: dict = {
        "record_end_offset": record_offset,
        "game_map_begin_offset": record[1],
        "elapsed_raw_s": elapsed_raw_s,
        "reserved0": reserved0,
        "project_name": project_name[0],
        "project_path": project_path[0],
        "complete": game_map_end_offset >= 0,
    }
    if game_map_end_offset >= 0:
        footer["game_map_end_offset"] = game_map_end_offset

    map_token = next(
        (item for item in tokens if item[1].lower().endswith(".map")),
        None,
    )
    if map_token is not None:
        footer["map_file"] = map_token[1]
        default1 = read_lp_string(data, map_token[2])
        default2 = read_lp_string(data, default1[1]) if default1 else None
        if (
            default1 is not None
            and default2 is not None
            and default1[0] == "Default"
            and default2[0] == "Default"
            and default2[1] + 12 <= len(data)
        ):
            width, height, map_flags = struct.unpack_from("<III", data, default2[1])
            if 1 <= width <= 16384 and 1 <= height <= 16384:
                footer["map_width"] = width
                footer["map_height"] = height
                footer["map_flags"] = map_flags

    for _, value, _ in tokens:
        lower = value.lower()
        if lower.endswith(".cfg") and "menu_config" not in footer:
            footer["menu_config"] = value
        elif lower.startswith("light") and "light" not in footer:
            footer["light"] = value
        elif value == "InitMapGen":
            footer["init_state"] = value
        elif re.fullmatch(r"player\d+", value):
            footer["player_state"] = value

    return footer


def parse_identity(data: bytes) -> dict:
    """Read the fixed OSWMap identity prefix without scanning the event body."""
    info: dict = {"header": None, "uid": None}
    first = read_lp_string(data, 0)
    if first is None:
        return info
    header, cursor = first
    info["header"] = header
    build_match = re.search(r"Build\.Ver\[([^\]]+)\]", header)
    if build_match:
        info["build_version"] = build_match.group(1)
    format_match = re.search(r"OSWMap(\d+)", header)
    if format_match:
        info["map_format_version"] = int(format_match.group(1))
    uid = read_lp_string(data, cursor)
    if uid is not None and uid[0].startswith("UID"):
        info["uid"] = uid[0]
    return info


def parse_header(data: bytes) -> dict:
    """Parse the OSWMap13 header. Returns dict with version, uid, sections."""
    info: dict = {
        "size": len(data),
        "sections": [],
        **parse_identity(data),
    }
    pos = 0
    first = read_lp_string(data, pos)
    if first is None:
        return info
    s, pos = first
    # Next: UID (length-prefixed)
    nxt = read_lp_string(data, pos)
    if nxt and nxt[0].startswith("UID"):
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
    footer = parse_footer(data)
    if footer:
        info["footer"] = footer
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


def extract_kv_pairs(
    data: bytes,
    start: int = 0,
    end: int | None = None,
) -> list[tuple[int, str, str]]:
    """Extract (u32 keylen, key, u32 vallen, value) pairs in a byte range.

    Both keys and values are ASCII length-prefixed. Values are returned as
    strings (raw ASCII bytes); numeric values come pre-formatted (e.g. "1176877135").
    """
    out = []
    i = max(0, start)
    limit = len(data) if end is None else min(end, len(data))
    while i < limit - 8:
        klen = struct.unpack_from("<I", data, i)[0]
        if 1 <= klen <= 64 and i + 4 + klen + 4 < limit:
            kbytes = data[i + 4 : i + 4 + klen]
            if is_ascii_str(kbytes):
                vlen = struct.unpack_from("<I", data, i + 4 + klen)[0]
                if 0 <= vlen <= 1024 and i + 4 + klen + 4 + vlen <= limit:
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


def _find_first_entry_marker(data: bytes, start: int) -> int | None:
    """Find a structurally plausible replay-entry marker after ``start``."""
    marker_prefix = b"\xb0\x04"
    pos = data.find(marker_prefix, start)
    while pos >= 0:
        if (
            pos >= 8
            and pos + 10 <= len(data)
            and data[pos + 6 : pos + 10] == b"\x00\x00\x00\x00"
        ):
            payload_size = struct.unpack_from("<I", data, pos - 4)[0]
            if 0 < payload_size <= 0x1000000 and pos + 10 + payload_size <= len(data):
                return pos
        pos = data.find(marker_prefix, pos + 1)
    return None


def extract_header_kv_pairs(data: bytes) -> list[tuple[int, str, str]]:
    """Extract metadata pairs without scanning the replay event stream.

    Lobby settings, player slots and PatternList all precede the first replay
    entry. Long matches can contain hundreds of megabytes after that boundary,
    so a byte-by-byte scan of the complete file is prohibitively expensive in
    Pyodide.
    """
    body_offset = _find_first_entry_marker(data, 0)
    return extract_kv_pairs(
        data,
        end=body_offset if body_offset is not None else len(data),
    )


def _parse_ascii_number(value: str) -> int | float | None:
    if re.fullmatch(r"[+-]?\d+", value):
        return int(value)
    try:
        number = float(value)
    except ValueError:
        return None
    return number if math.isfinite(number) else None


def extract_pattern_placements(
    data: bytes,
    header_pairs: list[tuple[int, str, str]] | None = None,
) -> list[dict]:
    """Extract PatternList's adjacent ``n``/``x``/``y`` placement triplets.

    ``n`` is the selected pattern name; ``x`` and ``y`` are ASCII-encoded map
    coordinates. The scan is bounded to the header's PatternList section so
    command-stream strings cannot be mistaken for placements.
    """
    pattern_marker = _lp_marker("PatternList")
    marker_offset = data.find(pattern_marker)
    if marker_offset < 0:
        return []
    start = marker_offset + len(pattern_marker)

    entry_marker = _find_first_entry_marker(data, start)
    record_end_offset = data.find(_lp_marker("GameMapRecordEnd"), start)
    candidates = [
        offset
        for offset in (entry_marker, record_end_offset)
        if offset is not None and offset >= 0
    ]
    end = min(candidates) if candidates else len(data)

    if header_pairs is None:
        pairs = extract_kv_pairs(data, start=start, end=end)
    else:
        pairs = [pair for pair in header_pairs if start <= pair[0] < end]
    placements: list[dict] = []
    i = 0
    while i + 2 < len(pairs):
        name_pair, x_pair, y_pair = pairs[i : i + 3]
        if (
            name_pair[1] == "n"
            and x_pair[1] == "x"
            and y_pair[1] == "y"
        ):
            x = _parse_ascii_number(x_pair[2])
            y = _parse_ascii_number(y_pair[2])
            if name_pair[2] and x is not None and y is not None:
                placements.append({
                    "name": name_pair[2],
                    "x": x,
                    "y": y,
                    "offset": name_pair[0],
                })
                i += 3
                continue
        i += 1
    return placements


def extract_settings(
    data: bytes,
    header_pairs: list[tuple[int, str, str]] | None = None,
) -> dict:
    """Extract known game settings from the kv pair stream."""
    pairs = header_pairs if header_pairs is not None else extract_header_kv_pairs(data)
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


def extract_players(
    data: bytes,
    header_pairs: list[tuple[int, str, str]] | None = None,
) -> list[dict]:
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
    pairs = header_pairs if header_pairs is not None else extract_header_kv_pairs(data)
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
    placements = extract_pattern_placements(data)

    # Optional pattern-type aggregation (requires compute-pipeline inventory)
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
            "footer": info.get("footer", {}),
            "pattern_placements": placements,
            "total_pattern_placements": len(placements),
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
    if info.get("footer"):
        footer = info["footer"]
        print("\nFooter metadata:")
        if footer.get("map_file"):
            dims = ""
            if footer.get("map_width") and footer.get("map_height"):
                dims = f" ({footer['map_width']}x{footer['map_height']})"
            print(f"  map              = {footer['map_file']}{dims}")
        print(f"  elapsed_raw_s    = {footer['elapsed_raw_s']:.6f}")
        if footer.get("player_state"):
            print(f"  player_state     = {footer['player_state']}")
    if placements:
        print(f"\nPatternList coordinates: {len(placements)} placements")
    if pattern_counts:
        print(f"\nPattern inventory cross-check: {sum(pattern_counts.values())} instances "
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
