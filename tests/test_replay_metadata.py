"""Tests for replay header metadata that does not require game assets."""
from __future__ import annotations

import struct
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "parser"))

from parse_replay import (  # noqa: E402
    extract_pattern_placements,
    parse_footer,
    parse_header,
    parse_identity,
)


def lp(value: str) -> bytes:
    raw = value.encode("ascii")
    return struct.pack("<I", len(raw)) + raw


def kv(key: str, value: str) -> bytes:
    return lp(key) + lp(value)


def footer_bytes() -> bytes:
    return b"".join([
        lp("GameMapRecordEnd"),
        lp("GameMapBegin"),
        struct.pack("<dI", 123.5, 0),
        lp("cossacks"),
        lp(r"data\projects\project.main.prj"),
        b"\x00" * 73,
        lp("game_v92k1477631297.map"),
        lp("Default"),
        lp("Default"),
        struct.pack("<III", 256, 320, 1),
        b"\x00" * 50,
        lp(r".\data\gui\menu.cfg"),
        b"\x00" * 7,
        lp("light0"),
        b"\x00" * 5,
        lp("InitMapGen"),
        lp("player3"),
        lp("GameMapEnd"),
    ])


class ReplayFooter(unittest.TestCase):
    def test_parses_stable_footer_fields(self) -> None:
        prefix = b"event stream"
        footer = parse_footer(prefix + footer_bytes())

        self.assertTrue(footer["complete"])
        self.assertEqual(footer["record_end_offset"], len(prefix))
        self.assertEqual(footer["elapsed_raw_s"], 123.5)
        self.assertEqual(footer["project_name"], "cossacks")
        self.assertEqual(
            footer["project_path"],
            r"data\projects\project.main.prj",
        )
        self.assertEqual(footer["map_file"], "game_v92k1477631297.map")
        self.assertEqual((footer["map_width"], footer["map_height"]), (256, 320))
        self.assertEqual(footer["map_flags"], 1)
        self.assertEqual(footer["menu_config"], r".\data\gui\menu.cfg")
        self.assertEqual(footer["light"], "light0")
        self.assertEqual(footer["init_state"], "InitMapGen")
        self.assertEqual(footer["player_state"], "player3")

    def test_parse_header_includes_footer(self) -> None:
        header = lp(
            "OSWMap13.Map.Ver[0.0]Build.Ver[2.2.3.11591]Core.Ver[1]"
        )
        data = header + lp("UID123") + footer_bytes()

        info = parse_header(data)

        self.assertEqual(info["build_version"], "2.2.3.11591")
        self.assertEqual(info["uid"], "UID123")
        self.assertEqual(info["footer"]["map_width"], 256)

    def test_parse_identity_does_not_require_complete_replay(self) -> None:
        data = lp(
            "OSWMap13.Map.Ver[0.0]Build.Ver[2.2.3.11591]Core.Ver[1]"
        ) + lp("UID987")

        identity = parse_identity(data)

        self.assertEqual(identity["map_format_version"], 13)
        self.assertEqual(identity["build_version"], "2.2.3.11591")
        self.assertEqual(identity["uid"], "UID987")

    def test_rejects_truncated_footer(self) -> None:
        data = lp("GameMapRecordEnd") + lp("GameMapBegin") + b"\x00\x01"
        self.assertEqual(parse_footer(data), {})


class PatternList(unittest.TestCase):
    def test_extracts_adjacent_nxy_triplets_and_stops_at_event_stream(self) -> None:
        placement_data = b"".join([
            lp("PatternList"),
            kv("n", "mng_2"),
            kv("x", "-62"),
            kv("y", "-80"),
            kv("n", "mni_1"),
            kv("x", "10.5"),
            kv("y", "83"),
        ])
        marker = b"\xb0\x04\x00\x00\x00\x00\x00\x00\x00\x00"
        event_payload = kv("n", "must_not_be_read") + kv("x", "1") + kv("y", "2")
        event = struct.pack("<fI", 0.0, len(event_payload)) + marker + event_payload

        placements = extract_pattern_placements(placement_data + event)

        self.assertEqual(
            [
                {key: item[key] for key in ("name", "x", "y")}
                for item in placements
            ],
            [
                {"name": "mng_2", "x": -62, "y": -80},
                {"name": "mni_1", "x": 10.5, "y": 83},
            ],
        )
        self.assertTrue(all(isinstance(item["offset"], int) for item in placements))

    def test_missing_pattern_list_is_empty(self) -> None:
        self.assertEqual(extract_pattern_placements(b"not a replay"), [])


if __name__ == "__main__":
    unittest.main()
