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

        for language in ("ru", "en"):
            entity_index = json.loads(
                (
                    ROOT
                    / "assets"
                    / "data"
                    / f"entity-index.{language}.json"
                ).read_text(encoding="utf-8")
            )
            self.assertEqual(entity_index["language"], language)
            self.assertEqual(
                entity_index["count"],
                sum(catalog["counts"].values()),
            )
            self.assertEqual(len(entity_index["entities"]), entity_index["count"])
            for sid, (kind, name, icon) in entity_index["entities"].items():
                with self.subTest(index_language=language, index_sid=sid):
                    self.assertIn(kind, catalog["entities"])
                    self.assertEqual(
                        name,
                        catalog["entities"][kind][sid]["name"][language],
                    )
                    icon_path = ROOT / icon.removeprefix("../")
                    self.assertTrue(icon_path.is_file(), icon_path)

    def test_entity_table_links_resolve_sid_from_a_separate_column(self):
        viewer = (ROOT / "assets" / "js" / "md-viewer.js").read_text(
            encoding="utf-8"
        )
        self.assertIn('row.querySelectorAll("code")', viewer)
        self.assertIn('sidCode.closest("td, th")', viewer)
        self.assertIn("cell = [...row.cells].find", viewer)
        self.assertIn("if (uniqueMatches.size !== 1) continue", viewer)

        fixtures = {
            "ru": ROOT / "docs" / "reference" / "compare" / "units" / "priests.md",
            "en": (
                ROOT
                / "docs_en"
                / "reference"
                / "compare"
                / "units"
                / "priests.md"
            ),
        }
        for language, path in fixtures.items():
            entity_index = json.loads(
                (
                    ROOT
                    / "assets"
                    / "data"
                    / f"entity-index.{language}.json"
                ).read_text(encoding="utf-8")
            )["entities"]
            rows = [
                line
                for line in path.read_text(encoding="utf-8").splitlines()
                if re.match(r"^\|\s*\*\*.+\*\*\s*\|\s*`[^`]+`\s*\|", line)
            ]
            self.assertEqual(len(rows), 4, path)
            for row in rows:
                name, sid = re.match(
                    r"^\|\s*\*\*(.+?)\*\*\s*\|\s*`([^`]+)`\s*\|", row
                ).groups()
                with self.subTest(language=language, sid=sid):
                    self.assertEqual(entity_index[sid][1], name)

    def test_entity_cards_group_nations_and_show_only_deviations(self):
        viewer = (ROOT / "assets" / "js" / "md-viewer.js").read_text(
            encoding="utf-8"
        )
        styles = (ROOT / "assets" / "css" / "md-viewer.css").read_text(
            encoding="utf-8"
        )
        self.assertIn("function groupDisplayVariants(entity, catalog)", viewer)
        self.assertIn("function variantDifferenceKeys(", viewer)
        self.assertIn("b[1].nations.length - a[1].nations.length", viewer)
        self.assertIn('baseValues: "Основные значения"', viewer)
        self.assertIn('differences: "Отличия"', viewer)
        self.assertIn('baseValues: "Base values"', viewer)
        self.assertIn('differences: "Differences"', viewer)
        self.assertIn(".entity-related-label", styles)
        self.assertNotIn("entity.variants.forEach", viewer)

        catalog = json.loads(
            (ROOT / "assets" / "data" / "entity-catalog.json").read_text(
                encoding="utf-8"
            )
        )
        # These are the regression fixtures that previously stretched one card
        # into 21 nearly identical national sections.
        self.assertEqual(
            len(catalog["entities"]["unit"]["cannon"]["variants"]),
            21,
        )
        self.assertEqual(
            len(catalog["entities"]["unit"]["howitzer"]["variants"]),
            21,
        )
        self.assertEqual(
            len(catalog["entities"]["building"]["ukrwwa"]["variants"]),
            2,
        )

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

    def test_capture_article_matches_parsed_building_flags(self):
        buildings = json.loads(
            (ROOT / "data.json").read_text(encoding="utf-8")
        )["buildings"]
        self.assertTrue(
            all(
                isinstance(building["capturable"], bool)
                for building in buildings
            ),
            "Every parsed building must have an explicit capturable flag",
        )
        ru = (
            DOCS / "recon" / "world" / "economy" / "capture_mechanics.md"
        ).read_text(encoding="utf-8")
        en = (
            ROOT
            / "docs_en"
            / "recon"
            / "world"
            / "economy"
            / "capture_mechanics.md"
        ).read_text(encoding="utf-8")
        cases = [
            ("eurmil", True, "Мельница", "Mill"),
            ("eurmar", True, "Рынок", "Market"),
            ("eursto", True, "Склад", "Storehouse"),
            ("eurgol", True, "Шахта", "Mine"),
            ("auscen", True, "Городской центр", "Town Hall"),
            ("aushou", True, "Дом, Изба или Хижина", "Housing, Izba, or Hut"),
            (
                "ausaca",
                True,
                "Академия; у Турции и Алжира — Минарет",
                "Academy; Minaret for Turkey and Algeria",
            ),
            ("ausart", True, "Артиллерийское депо", "Artillery Depot"),
            ("ausbla", True, "Кузница", "Blacksmith"),
            ("eurpor", False, "Порт", "Shipyard"),
            ("eurtow", False, "Башня", "Tower"),
            ("eurswa", False, "Стена или ворота", "Wall or Gate"),
            ("ausdip", False, "Дипломатический центр", "Diplomatic Center"),
            (
                "austem",
                False,
                "Собор, Православная церковь или Мечеть",
                "Cathedral, Orthodox Cathedral, or Mosque",
            ),
            (
                "ausbar",
                False,
                "Казарма XVII века и её национальные варианты",
                "Barracks, 17th century, and its national variants",
            ),
            (
                "ausba2",
                False,
                "Казарма XVIII века",
                "Barracks, 18th century",
            ),
            ("aussta", False, "Конюшня", "Stable"),
            (
                "misblg",
                False,
                "Здания и декорации миссий",
                "Mission buildings and scenery objects",
            ),
        ]
        for sid, capturable, ru_name, en_name in cases:
            with self.subTest(sid=sid):
                parsed_values = {
                    building["capturable"]
                    for building in buildings
                    if building["sid"] == sid
                }
                if parsed_values:
                    self.assertEqual(parsed_values, {capturable})
                self.assertIn(
                    f"| {'Можно захватить' if capturable else 'Нельзя захватить'}"
                    f" | {ru_name} |",
                    ru,
                )
                self.assertIn(
                    f"| {'Capturable' if capturable else 'Not capturable'}"
                    f" | {en_name} |",
                    en,
                )

    def test_generated_upgrade_names_are_reader_facing(self):
        ru = "\n".join(
            path.read_text(encoding="utf-8")
            for path in sorted(
                (DOCS / "reference" / "05_upgrades").glob("*.md")
            )
        )
        en = "\n".join(
            path.read_text(encoding="utf-8")
            for path in sorted(
                (ROOT / "docs_en" / "reference" / "05_upgrades").glob("*.md")
            )
        )
        self.assertNotIn("| damage |", ru)
        self.assertNotIn("| protection |", ru)
        self.assertNotIn("%value%", ru)
        self.assertNotIn("Stable cossackdon", en)
        self.assertIn("Донской козак: урон", ru)
        self.assertIn("Don Cossack: damage", en)

    def test_large_building_and_upgrade_chapters_are_split(self):
        expected_counts = {
            "03_buildings": 18,
            "05_upgrades": 24,
        }
        for language_root in (ROOT / "docs", ROOT / "docs_en"):
            for chapter, expected_count in expected_counts.items():
                directory = language_root / "reference" / chapter
                pages = sorted(directory.glob("*.md"))
                with self.subTest(
                    language=language_root.name,
                    chapter=chapter,
                ):
                    self.assertEqual(len(pages), expected_count)
                    self.assertLess(
                        (directory / "README.md").stat().st_size,
                        15_000,
                    )

        viewer = (ROOT / "assets" / "js" / "md-viewer.js").read_text(
            encoding="utf-8"
        )
        self.assertIn("LEGACY_REFERENCE_ROUTES", viewer)
        self.assertIn('"tower.md": [', viewer)
        self.assertIn('"stable.md": [', viewer)
        self.assertIn("applyLegacyReferenceRoute();", viewer)

        self.assertIn(
            "ausbar.roundshier.2.6",
            (
                ROOT
                / "docs_en"
                / "reference"
                / "05_upgrades"
                / "barracks_17_melee.md"
            ).read_text(encoding="utf-8"),
        )
        self.assertIn(
            "engba2.highlander.2.6",
            (
                ROOT
                / "docs_en"
                / "reference"
                / "05_upgrades"
                / "barracks_18_specialists.md"
            ).read_text(encoding="utf-8"),
        )

    def test_raw_upgrade_effect_aliases_are_localized(self):
        self.assertEqual(decode_upg_type("damage", "ru")[0], "+урон")
        self.assertEqual(decode_upg_type("protection", "ru")[0], "+защита")

    def test_reader_links_do_not_use_markdown_paths_as_labels(self):
        offenders = []
        for language_root in (ROOT / "docs", ROOT / "docs_en"):
            for path in language_root.rglob("*.md"):
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

    def test_recon_does_not_show_markdown_filenames_as_terms(self):
        offenders = []
        for language_root in (ROOT / "docs" / "recon", ROOT / "docs_en" / "recon"):
            for path in language_root.rglob("*.md"):
                text = re.sub(
                    r"```.*?```",
                    " ",
                    path.read_text(encoding="utf-8"),
                    flags=re.DOTALL,
                )
                for value in re.findall(r"`([^`\r\n]+)`", text):
                    if re.fullmatch(
                        r"[./\\\w-]+\.md(?:#[^\s]+)?",
                        value,
                        flags=re.IGNORECASE,
                    ):
                        offenders.append(
                            f"{path.relative_to(ROOT).as_posix()}: {value}"
                        )
        self.assertEqual(offenders, [])

    def test_russian_reader_terminology_is_consistent(self):
        forbidden = {
            "тайл": re.compile(r"(?<!\w)тайл\w*", re.IGNORECASE),
            "g-сек": re.compile(r"g[-‑–— ]?сек", re.IGNORECASE),
            "хедшот": re.compile(r"хедшот\w*", re.IGNORECASE),
        }
        offenders = []
        for path in DOCS.rglob("*.md"):
            visible = reader_visible_text(path.read_text(encoding="utf-8"))
            found = [
                label
                for label, pattern in forbidden.items()
                if pattern.search(visible)
            ]
            if found:
                offenders.append(
                    f"{path.relative_to(ROOT).as_posix()}: {', '.join(found)}"
                )
        self.assertEqual(offenders, [])

    def test_formation_support_and_town_hall_use_canonical_names(self):
        for language_root, forbidden in (
            (ROOT / "docs", "музыкант"),
            (ROOT / "docs_en", "musician"),
        ):
            offenders = []
            for path in language_root.rglob("*.md"):
                visible = reader_visible_text(path.read_text(encoding="utf-8"))
                if forbidden in visible.casefold():
                    offenders.append(path.relative_to(ROOT).as_posix())
            self.assertEqual(offenders, [])

        town_halls = (
            DOCS
            / "reference"
            / "compare"
            / "buildings"
            / "town_halls.md"
        ).read_text(encoding="utf-8")
        self.assertTrue(town_halls.startswith("# Городские центры"))
        self.assertNotIn("Ратуш", reader_visible_text(town_halls))

    def test_documentation_translation_workflow_is_manual(self):
        script = (ROOT / "scripts" / "build_english_docs.py").read_text(
            encoding="utf-8"
        )
        guide = (
            ROOT / "internals" / "project" / "documentation_style.md"
        ).read_text(encoding="utf-8")
        self.assertIn("Automatic translation is disabled", script)
        self.assertIn("переводится и редактируется вручную", guide)

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
        tech_tree = (DOCS / "reports" / "tech" / "tech_tree.md").read_text(
            encoding="utf-8"
        )
        buildings = "\n".join(
            path.read_text(encoding="utf-8")
            for path in sorted(
                (DOCS / "reference" / "03_buildings").glob("*.md")
            )
        )
        self.assertIn("**Крестьянин** `peaaus`", units)
        self.assertIn("**Чайка** `chaika`", units)
        self.assertIn("**Чайка** (`chaika`)", tech_tree)
        self.assertIn("Крестьянин", buildings)
        self.assertNotIn("производит: peasant", buildings.lower())

    def test_naval_units_use_canonical_russian_names(self):
        offenders = []
        for path in DOCS.rglob("*.md"):
            text = path.read_text(encoding="utf-8")
            noncanonical = (
                r"\bпаром(?:а|у|ом|е|ы|ов|ам|ами|ах)?\b",
                r"\bрыбач",
                r"\bбаттлшип",
            )
            if any(
                re.search(pattern, text, flags=re.IGNORECASE)
                for pattern in noncanonical
            ):
                offenders.append(path.relative_to(ROOT).as_posix())
        self.assertEqual(offenders, [])

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

    def test_documentation_states_current_rules_without_arguing_with_old_versions(self):
        patterns = (
            r"(?:раньше|прежде)\s+(?:в\s+)?(?:этой|данной)\s+статье",
            r"(?:раньше|прежде)\s+(?:в\s+)?этой\s+таблице",
            r"(?:в\s+)?(?:предыдущей|прежней)\s+версии\s+(?:этой\s+)?"
            r"(?:статьи|документа)",
            r"(?:ранее|раньше).{0,80}(?:написано|указано).{0,80}"
            r"(?:неверно|ошибочно)",
            r"\bмы\s+(?:исправили|поправили)\b",
            r"\bpreviously\s+in\s+this\s+table\b",
            r"\b(?:an\s+)?(?:earlier|previous)\s+version\s+of\s+"
            r"(?:this|the)\s+(?:article|document)\b",
            r"\bwe\s+(?:fixed|corrected)\b",
            r"~~.+?~~\s*(?:✅\s*)?(?:\*\*)?"
            r"(?:закрыто|closed|resolved|частично\s+отвечено|partly\s+answered)",
        )
        offenders = []
        for tree in (
            DOCS,
            ROOT / "docs_en",
            ROOT / "internals",
            ROOT / "internals_en",
        ):
            for path in tree.rglob("*.md"):
                if path.name == "documentation_style.md":
                    continue
                visible = reader_visible_text(path.read_text(encoding="utf-8"))
                if any(
                    re.search(pattern, visible, flags=re.IGNORECASE | re.DOTALL)
                    for pattern in patterns
                ):
                    offenders.append(path.relative_to(ROOT).as_posix())
        self.assertEqual(offenders, [])

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
