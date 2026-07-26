"""Smoke tests for `data.json` integrity and downstream JSON structure.

These tests assume the data.json committed to the repo is valid and self-
consistent. After regenerating data.json, run them to catch obvious breaks
before pushing.
"""
from __future__ import annotations
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class DataJson(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads((ROOT / "data.json").read_text(encoding="utf-8"))

    def test_structure(self) -> None:
        for key in ("nations", "buildings", "units", "upgrades", "sanity_checks"):
            self.assertIn(key, self.data)

    def test_nations_count(self) -> None:
        # Engine has 24 cids; 21 are playable (mis/tat/lit excluded).
        self.assertEqual(len(self.data["nations"]), 21)

    def test_sanity_checks_pass(self) -> None:
        checks = self.data["sanity_checks"]
        # Each check stores `{category, name, expected, actual, pass}`.
        failed = [c for c in checks if not c.get("pass")]
        self.assertEqual(
            [(c["category"], c["name"]) for c in failed],
            [],
            f"{len(failed)} sanity check(s) failed",
        )
        # Establish a floor — drop in count is a smell.
        self.assertGreaterEqual(len(checks), 100)

    def test_nation_names_populated(self) -> None:
        for n in self.data["nations"]:
            self.assertTrue(n.get("name_en"), f"nation {n['sid']} missing name_en")
            self.assertTrue(n.get("name_ru"), f"nation {n['sid']} missing name_ru")


class TechTree(unittest.TestCase):
    """Verify `derived/tech_tree.json` follows expected shape."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.tree = json.loads((ROOT / "derived" / "tech_tree.json").read_text(encoding="utf-8"))

    def test_top_level(self) -> None:
        self.assertIn("nations", self.tree)
        self.assertEqual(len(self.tree["nations"]), 21)

    def test_per_nation_structure(self) -> None:
        for nat, nt in self.tree["nations"].items():
            self.assertIn("buildings", nt, f"{nat} missing buildings")
            self.assertIn("units", nt, f"{nat} missing units")
            self.assertIn("upgrades", nt, f"{nat} missing upgrades")
            self.assertGreater(len(nt["buildings"]), 0, f"{nat} has no buildings")
            self.assertGreater(len(nt["units"]), 0, f"{nat} has no units")


class GameSettings(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.gs = json.loads((ROOT / "derived" / "game_settings.json").read_text(encoding="utf-8"))

    def test_required_categories(self) -> None:
        for cat in ("mapsize", "terraintype", "relieftype", "resourcestart",
                    "resourcemines", "season", "startingunits", "balloon",
                    "cannons", "peacetime", "century18", "capture",
                    "marketdip", "teams", "limit", "gamespeed",
                    "adviserassistant", "difficulty", "defaults"):
            self.assertIn(cat, self.gs)

    def test_canonical_labels(self) -> None:
        # Critical labels — if these change the game patch shifted something.
        relief_3 = next(r for r in self.gs["relieftype"] if r["value"] == 3)
        self.assertEqual(relief_3["label_ru"], "Высокогорье")
        balloon_no = next(b for b in self.gs["balloon"] if b["value"] == 1)
        self.assertEqual(balloon_no["label_ru"], "Без монгольфьеров")

    def test_initmap_defaults(self) -> None:
        gen = self.gs["defaults"]["gen"]
        # initmap.inc:29-31
        self.assertEqual(gen["relieftype"], 3)
        self.assertEqual(gen["resourcestart"], 2)
        self.assertEqual(gen["resourcemines"], 1)


if __name__ == "__main__":
    unittest.main()
