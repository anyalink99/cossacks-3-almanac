import json
from pathlib import Path
import re
import unittest

from scripts.build_english_docs import github_slug
from parser.config import decode_upg_type


ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"


def reader_visible_text(text: str) -> str:
    """Remove the places where literal engine identifiers are expected."""

    text = re.sub(r"```.*?```", " ", text, flags=re.DOTALL)
    text = re.sub(r"`[^`]*`", " ", text)
    text = re.sub(r"\]\([^)\n]*\)", "]", text)
    text = re.sub(r"<[^>\n]+>", " ", text)
    return text


class ReaderFacingDocumentation(unittest.TestCase):
    def test_entity_catalog_has_complete_real_icon_coverage(self):
        catalog = json.loads(
            (ROOT / "assets" / "data" / "entity-catalog.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(
            catalog["counts"],
            {"unit": 119, "building": 237, "upgrade": 3933},
        )
        for kind, entities in catalog["entities"].items():
            self.assertEqual(len(entities), catalog["counts"][kind])
            for sid, entity in entities.items():
                with self.subTest(kind=kind, sid=sid):
                    self.assertTrue(entity["icon"])
                    icon_path = ROOT / entity["icon"].removeprefix("../")
                    self.assertTrue(icon_path.is_file(), icon_path)

    def test_search_index_contains_exact_sections_and_entities(self):
        ru_entries = json.loads(
            (DOCS / "_search.json").read_text(encoding="utf-8")
        )["entries"]
        en_entries = json.loads(
            (ROOT / "docs_en" / "_search.json").read_text(encoding="utf-8")
        )["entries"]
        winged_hussar = next(
            entry
            for entry in ru_entries
            if entry.get("entity") == "unit:wingedhussar"
        )
        self.assertEqual(winged_hussar["title"], "Крылатый гусар")
        upgrades_section = next(
            entry
            for entry in en_entries
            if entry.get("title") == "How upgrades combine"
        )
        self.assertEqual(upgrades_section["kind"], "section")
        self.assertEqual(upgrades_section["fragment"], "how-upgrades-combine")

    def test_generated_upgrade_names_are_reader_facing(self):
        ru = (DOCS / "reference" / "05_upgrades" / "README.md").read_text(
            encoding="utf-8"
        )
        en = (
            ROOT / "docs_en" / "reference" / "05_upgrades" / "README.md"
        ).read_text(encoding="utf-8")
        self.assertNotIn("| damage |", ru)
        self.assertNotIn("| protection |", ru)
        self.assertNotIn("%value%", ru)
        self.assertNotIn("Stable cossackdon", en)
        self.assertIn("Донской козак: урон", ru)
        self.assertIn("Don Cossack: damage", en)

    def test_raw_upgrade_effect_aliases_are_localized(self):
        self.assertEqual(decode_upg_type("damage", "ru")[0], "+урон")
        self.assertEqual(decode_upg_type("protection", "ru")[0], "+защита")

    def test_reader_links_do_not_use_markdown_paths_as_labels(self):
        offenders = []
        for language_root in (ROOT / "docs", ROOT / "docs_en"):
            for area in ("reference", "reports"):
                for path in (language_root / area).rglob("*.md"):
                    text = re.sub(
                        r"```.*?```",
                        " ",
                        path.read_text(encoding="utf-8"),
                        flags=re.DOTALL,
                    )
                    for label in re.findall(r"\[([^\]]+)\]\([^)]+\)", text):
                        if ".md" in label.casefold():
                            offenders.append(
                                f"{path.relative_to(ROOT).as_posix()}: {label}"
                            )
        self.assertEqual(offenders, [])

    def test_documentation_style_guide_is_linked_and_mirrored(self):
        ru_guide = ROOT / "internals" / "project" / "documentation_style.md"
        en_guide = ROOT / "internals_en" / "project" / "documentation_style.md"
        self.assertTrue(ru_guide.is_file())
        self.assertTrue(en_guide.is_file())
        self.assertIn(
            "internals/project/documentation_style.md",
            (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8"),
        )
        self.assertIn(
            "internals_en/project/documentation_style.md",
            (ROOT / "CONTRIBUTING.en.md").read_text(encoding="utf-8"),
        )

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

    def test_recon_prose_does_not_expose_english_engine_jargon(self):
        jargon = (
            "ascii",
            "attack-move",
            "blink",
            "build order",
            "built-state",
            "callback",
            "capture",
            "cluster",
            "damage",
            "damage cap",
            "debris",
            "event",
            "flag",
            "handle",
            "handler",
            "hardwall",
            "hp",
            "idle-state",
            "mode",
            "owner",
            "pause",
            "per-resource",
            "queue",
            "range",
            "score",
            "search radius",
            "spawn",
            "sprite",
            "state-machine",
            "sub-tick",
            "target",
            "trigger",
            "ui",
        )
        offenders = []
        for path in (DOCS / "recon").rglob("*.md"):
            visible = reader_visible_text(path.read_text(encoding="utf-8")).casefold()
            found = [
                term
                for term in jargon
                if re.search(
                    rf"(?<![\w]){re.escape(term)}(?![\w])",
                    visible,
                    flags=re.IGNORECASE,
                )
            ]
            if found:
                offenders.append(
                    f"{path.relative_to(ROOT).as_posix()}: {', '.join(found)}"
                )
        self.assertEqual(offenders, [])

    def test_recon_prose_keeps_known_object_ids_in_code(self):
        canonical = json.loads(
            (ROOT / "derived" / "canonical_terms.json").read_text(encoding="utf-8")
        )
        object_ids = {
            sid.casefold()
            for category in ("buildings", "units")
            for sid in canonical[category]
            if len(sid) >= 4
        }
        offenders = []
        for path in (DOCS / "recon").rglob("*.md"):
            visible = reader_visible_text(path.read_text(encoding="utf-8"))
            found = sorted(
                sid
                for sid in object_ids
                if re.search(
                    rf"(?<![\w]){re.escape(sid)}(?![\w])",
                    visible,
                    flags=re.IGNORECASE,
                )
            )
            if found:
                offenders.append(
                    f"{path.relative_to(ROOT).as_posix()}: {', '.join(found)}"
                )
        self.assertEqual(offenders, [])

    def test_recon_prose_formats_remaining_latin_terms_as_technical(self):
        allowed_words = {
            "age",
            "cossacks",
            "empires",
            "ii",
            "of",
            "pascal",
            "windows",
            "xvii",
            "xviii",
        }
        offenders = []
        for path in (DOCS / "recon").rglob("*.md"):
            visible = reader_visible_text(path.read_text(encoding="utf-8"))
            words = sorted(
                {
                    word.casefold()
                    for word in re.findall(
                        r"(?<![\w])[A-Za-z][A-Za-z-]{1,}(?![\w])",
                        visible,
                    )
                    if word.casefold() not in allowed_words
                }
            )
            if words:
                offenders.append(
                    f"{path.relative_to(ROOT).as_posix()}: {', '.join(words)}"
                )
        self.assertEqual(offenders, [])

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
