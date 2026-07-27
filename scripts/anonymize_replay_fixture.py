"""Create a privacy-safe replay fixture without changing its binary layout.

Length-prefixed player names and account identifiers are overwritten with
same-length ASCII placeholders. Replacing in place preserves every offset, so
the fixture continues to exercise the real parser rather than a reconstructed
format sample.

Usage:
    python scripts/anonymize_replay_fixture.py source.rep target.rep
"""
from __future__ import annotations

import argparse
import struct
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "parser"))

from parse_replay import extract_header_kv_pairs  # noqa: E402


IDENTITY_KEYS = {"lanid", "steamid", "accountid", "profileid", "uid"}


def placeholder(length: int, index: int) -> bytes:
    seed = f"Player{index:02d}".encode("ascii")
    return (seed + b"_" * length)[:length]


def overwrite_value(data: bytearray, pair_offset: int, key: str, value: str, replacement: bytes) -> None:
    key_size = struct.unpack_from("<I", data, pair_offset)[0]
    value_size_offset = pair_offset + 4 + key_size
    value_size = struct.unpack_from("<I", data, value_size_offset)[0]
    raw_offset = value_size_offset + 4
    if value_size != len(value.encode("utf-8")) or len(replacement) != value_size:
        raise ValueError(f"cannot safely replace {key!r} at {pair_offset}")
    data[raw_offset:raw_offset + value_size] = replacement


def anonymize(source: Path, target: Path) -> None:
    original = source.read_bytes()
    data = bytearray(original)
    pairs = extract_header_kv_pairs(original)
    player_index = 0
    player_names: list[bytes] = []

    for offset, key, value in pairs:
        raw = value.encode("utf-8")
        if not raw:
            continue
        if key == "name" and not value.startswith("game_v"):
            player_index += 1
            player_names.append(raw)
            overwrite_value(data, offset, key, value, placeholder(len(raw), player_index))
        elif key in IDENTITY_KEYS:
            overwrite_value(data, offset, key, value, b"0" * len(raw))

    # Some profile labels are repeated outside the key/value header. Replace
    # the alphanumeric parts as well, always with the same byte length.
    for index, name in enumerate(player_names, 1):
        for token in name.replace(b"[", b" ").replace(b"]", b" ").split():
            if len(token) >= 4:
                data[:] = data.replace(token, placeholder(len(token), index))

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    print(f"Wrote {target} ({len(data):,} bytes; {player_index} player names anonymized)")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("target", type=Path)
    args = parser.parse_args()
    anonymize(args.source, args.target)


if __name__ == "__main__":
    main()
