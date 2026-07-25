"""Tests for replay header metadata that does not require game assets."""
from __future__ import annotations

import json
import struct
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "parser"))

from parse_replay import (  # noqa: E402
    extract_header_kv_pairs,
    extract_pattern_placements,
    extract_players,
    extract_settings,
    parse_footer,
    parse_header,
    parse_identity,
)
from parse_replay_events import (  # noqa: E402
    decode_subpackages,
    parse_replay_from_bytes,
)
from build_replay_upgrades import build_catalog  # noqa: E402


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


class HeaderMetadata(unittest.TestCase):
    def test_shared_header_scan_stops_before_event_stream(self) -> None:
        header = b"".join([
            kv("gamespeed", "2"),
            kv("id", "0"),
            kv("cid", "4"),
            kv("name", "Header player"),
            kv("bexists", "true"),
        ])
        event_payload = b"".join([
            kv("gamespeed", "0"),
            kv("id", "1"),
            kv("cid", "5"),
            kv("name", "Event-stream decoy"),
            kv("bexists", "true"),
        ])
        marker = b"\xb0\x04\x00\x00\x00\x00\x00\x00\x00\x00"
        event = struct.pack("<fI", 1.0, len(event_payload)) + marker + event_payload
        data = header + event

        pairs = extract_header_kv_pairs(data)

        self.assertEqual(extract_settings(data, pairs)["gamespeed"], 2)
        self.assertEqual(
            [player["name"] for player in extract_players(data, pairs)],
            ["Header player"],
        )
        self.assertNotIn("Event-stream decoy", [value for _, _, value in pairs])

    def test_comprehensive_parser_scans_header_once(self) -> None:
        header = b"".join([
            kv("gamespeed", "2"),
            kv("id", "0"),
            kv("cid", "4"),
            kv("name", "Player"),
            kv("bexists", "true"),
        ])
        marker = b"\xb0\x04\x00\x00\x00\x00\x00\x00\x00\x00"
        event = struct.pack("<fI", 1.0, 1) + marker + b"\x00"

        import parse_replay
        from unittest.mock import patch

        original = parse_replay.extract_header_kv_pairs
        with patch(
            "parse_replay.extract_header_kv_pairs",
            wraps=original,
        ) as scan:
            result = parse_replay_from_bytes(header + event)

        self.assertEqual(scan.call_count, 1)
        self.assertEqual(result["settings"]["gamespeed"], 2)


class ReplayUpgradeCatalog(unittest.TestCase):
    def test_committed_catalog_matches_data_json(self) -> None:
        data = json.loads((ROOT / "data.json").read_text(encoding="utf-8"))
        committed = json.loads(
            (ROOT / "derived" / "replay_upgrades.json").read_text(
                encoding="utf-8",
            )
        )

        self.assertEqual(committed, build_catalog(data))


class CompactEventDecode(unittest.TestCase):
    @staticmethod
    def package(state_id: int, body: bytes) -> bytes:
        return bytes((0x00, 0x03, 0x00, state_id, 0x00)) + body + b"\x01"

    def test_skips_unused_projectile_fields_but_preserves_summary(self) -> None:
        payload = self.package(0x29, b"\x00" * 61)

        detailed = decode_subpackages(payload, 10.0)
        compact = decode_subpackages(payload, 10.0, compact=True)

        self.assertEqual(compact[0]["handler"], detailed[0]["handler"])
        self.assertEqual(compact[0]["pid"], detailed[0]["pid"])
        self.assertNotIn("source_pos", compact[0])
        self.assertTrue(compact[0]["end_marker_ok"])

    def test_skips_unused_hp_records_but_consumes_complete_package(self) -> None:
        body = struct.pack("<i", 2)
        body += struct.pack("<i?i", 101, True, 900)
        body += struct.pack("<i?i", 102, False, 0)
        payload = self.package(0x3D, body)

        detailed = decode_subpackages(payload, 10.0)
        compact = decode_subpackages(payload, 10.0, compact=True)

        self.assertEqual(compact[0]["handler"], detailed[0]["handler"])
        self.assertEqual(len(detailed[0]["hp_updates"]), 2)
        self.assertNotIn("hp_updates", compact[0])
        self.assertTrue(compact[0]["end_marker_ok"])


if __name__ == "__main__":
    unittest.main()
