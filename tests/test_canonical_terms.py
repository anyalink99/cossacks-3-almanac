"""Smoke tests for the canonical-terms glossary.

These don't require a Cossacks 3 install — they verify that the committed
`docs/derived/canonical_terms.json` and `parser/config.py` constants are
internally consistent.
"""
from __future__ import annotations
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "parser"))


class CanonicalTerms(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        path = ROOT / "docs" / "derived" / "canonical_terms.json"
        cls.canon = json.loads(path.read_text(encoding="utf-8"))

    def test_21_nations(self) -> None:
        self.assertEqual(len(self.canon["nations"]), 21)

    def test_known_translations(self) -> None:
        # If the game's locale changes a label, this test will catch it.
        self.assertEqual(self.canon["nations"]["aus"]["ru"], "Австрия")
        self.assertEqual(self.canon["nations"]["ukr"]["ru"], "Украина")
        self.assertEqual(self.canon["buildings"]["cen"]["ru"], "Городской центр")
        self.assertEqual(self.canon["buildings"]["bar"]["ru"], "Казарма 17в.")
        self.assertEqual(self.canon["settings"]["randommap.relieftype.3"]["ru"],
                         "Высокогорье")
        self.assertEqual(self.canon["settings"]["randommap.settings.balloon.no"]["ru"],
                         "Без монгольфьеров")
        self.assertEqual(
            self.canon["settings"]["randommap.settings.adviserassistant"]["ru"],
            "Помощник",
        )
        self.assertEqual(
            self.canon["settings"]["randommap.settings.peacetime.default"]["ru"],
            "Без времени мира",
        )

    def test_no_empty_labels(self) -> None:
        # Every category entry should have at least one of {ru, en} populated.
        for sid, names in self.canon["nations"].items():
            self.assertTrue(names["ru"] or names["en"], f"nation {sid!r} has no labels")
        for suffix, info in self.canon["buildings"].items():
            self.assertTrue(info["ru"] or info["en"],
                            f"building {suffix!r} has no labels")


class ConfigImports(unittest.TestCase):
    """parser/config.py is the single import target for downstream code."""

    def test_imports(self) -> None:
        from config import (NATION_NAMES_RU, NATION_NAMES_EN, USAGE_RU,
                            USAGE_DECODE, BUILDING_NAMES_RU, WEAPON_KIND_RU,
                            decode_usage, decode_upg_type,
                            nation_ru, nation_en, nation_label, usage_ru)
        # Just touch each one to make sure import + module init succeeded.
        self.assertEqual(NATION_NAMES_RU["aus"], "Австрия")
        self.assertEqual(NATION_NAMES_EN["aus"], "Austria")
        self.assertEqual(USAGE_RU["Town Hall"], "Городской центр")
        self.assertIn("gc_obj_usage_center", USAGE_DECODE)
        self.assertEqual(BUILDING_NAMES_RU["cen"], "Городской центр")
        self.assertEqual(WEAPON_KIND_RU["pike"], "пика")
        self.assertEqual(decode_usage("gc_obj_usage_center", "ru"), "Городской центр")
        ru_label, _en_desc = decode_upg_type("gc_upg_type_balloon", "ru")
        self.assertEqual(ru_label, "монгольфьер")
        self.assertEqual(nation_ru("aus"), "Австрия")
        self.assertEqual(nation_en("aus"), "Austria")
        self.assertEqual(nation_label("aus"), "AUS — Austria (Австрия)")
        self.assertEqual(usage_ru("Town Hall"), "Городской центр")
        self.assertEqual(usage_ru(None), "—")

    def test_decode_usage_fallback(self) -> None:
        from config import decode_usage
        # Unknown gc_id should pass through.
        self.assertEqual(decode_usage("gc_obj_usage_unknownThing", "ru"),
                         "gc_obj_usage_unknownThing")


if __name__ == "__main__":
    unittest.main()
