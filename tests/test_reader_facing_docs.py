import json
from pathlib import Path
import re
import unittest

from scripts.build_english_docs import github_slug


ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"


class ReaderFacingDocumentation(unittest.TestCase):
    def test_encyclopedia_home_is_for_readers(self):
        text = (DOCS / "README.md").read_text(encoding="utf-8")
        self.assertTrue(text.startswith("# Энциклопедия Cossacks 3"))
        self.assertNotIn("каталог артефактов", text.lower())
        self.assertNotIn("Регенерация", text)
        self.assertNotIn("known_issues", text)

    def test_no_ambiguous_index_backlinks(self):
        offenders = []
        for path in DOCS.rglob("*.md"):
            if "[← Index]" in path.read_text(encoding="utf-8"):
                offenders.append(path.relative_to(ROOT).as_posix())
        self.assertEqual(offenders, [])

    def test_reference_chapters_return_to_reference_home(self):
        for chapter in (
            "01_economy",
            "02_combat",
            "03_buildings",
            "04_units",
            "05_upgrades",
            "06_market",
            "07_naval",
        ):
            text = (DOCS / "reference" / chapter / "README.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("[← Краткий справочник](../README.md)", text)
            self.assertNotIn("[← Index](README.md)", text)

    def test_project_maintenance_pages_live_in_internals(self):
        for name in ("architecture.md", "known_issues.md", "known_issues_archive.md"):
            self.assertFalse((DOCS / name).exists())
            self.assertTrue((ROOT / "internals" / "project" / name).is_file())
        self.assertFalse(
            (DOCS / "reports" / "map" / "map_predictions_validation.md").exists()
        )
        self.assertTrue(
            (ROOT / "internals" / "data" / "map_predictions_validation.md").is_file()
        )

    def test_generated_tables_lead_with_canonical_names(self):
        units = (DOCS / "reference" / "04_units" / "README.md").read_text(
            encoding="utf-8"
        )
        buildings = (DOCS / "reference" / "03_buildings" / "README.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("**Крестьянин** `peaaus`", units)
        self.assertIn("**Чайка** `chaika`", units)
        self.assertIn("Крестьянин", buildings)
        self.assertNotIn("производит: peasant", buildings.lower())

    def test_canonical_terms_include_units_outside_units_locale_file(self):
        terms = json.loads(
            (ROOT / "derived" / "canonical_terms.json").read_text(encoding="utf-8")
        )
        self.assertEqual(terms["units"]["chaika"]["ru"], "Чайка")

    def test_mechanics_articles_have_reader_titles_and_backlinks(self):
        for path in (DOCS / "recon").rglob("*.md"):
            if path.name == "README.md":
                continue
            text = path.read_text(encoding="utf-8")
            self.assertNotRegex(text, r"(?m)^# Recon:")
            self.assertIn("[← Как устроена игра]", text)

    def test_naval_contents_links_match_headings(self):
        text = (DOCS / "reference" / "07_naval" / "README.md").read_text(
            encoding="utf-8"
        )
        headings = {
            github_slug(match.group(1))
            for match in re.finditer(r"^#{2,6}\s+(.+?)\s*$", text, flags=re.MULTILINE)
        }
        anchors = {
            match.group(1)
            for match in re.finditer(r"\]\(#([^)]+)\)", text)
        }
        self.assertTrue(anchors)
        self.assertEqual(anchors - headings, set())

    def test_core_articles_do_not_lead_with_internal_terms(self):
        market = (DOCS / "reference" / "06_market" / "README.md").read_text(
            encoding="utf-8"
        )
        naval = (DOCS / "reference" / "07_naval" / "README.md").read_text(
            encoding="utf-8"
        )
        settings = (
            DOCS / "reports" / "map" / "lobby_settings.md"
        ).read_text(encoding="utf-8")
        self.assertIn("| Еда |", market)
        self.assertNotIn("buycost[X]", market)
        self.assertIn("| Здоровье |", naval)
        self.assertNotIn("fishingmax", naval)
        self.assertIn("### Размер карты (`mapsize`)", settings)
        self.assertNotIn("## Генератор карты — `gMap.settings.gen`", settings)


if __name__ == "__main__":
    unittest.main()
