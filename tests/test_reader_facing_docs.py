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

    def test_wall_demolition_uses_any_enemy_non_building_and_respects_defenders(self):
        russian = (
            DOCS / "recon" / "world" / "combat" / "walls_and_gates.md"
        ).read_text(encoding="utf-8")
        english = (
            ROOT
            / "docs_en"
            / "recon"
            / "world"
            / "combat"
            / "walls_and_gates.md"
        ).read_text(encoding="utf-8")

        russian_reader, russian_technical = russian.split("## 7.", maxsplit=1)
        english_reader, english_technical = english.split("## 7.", maxsplit=1)

        self.assertIn(
            "любой вражеский объект, не являющийся зданием",
            russian_reader.casefold(),
        )
        self.assertIn("крестьянин или артиллерия", russian_reader.casefold())
        self.assertRegex(
            russian_reader.casefold(),
            r"защитник.{0,80}(?:восьми|8).{0,40}клет",
        )
        self.assertNotIn(
            "достаточно пехотинца врага",
            russian_reader.casefold(),
        )

        self.assertIn("any enemy non-building object", english_reader)
        self.assertRegex(
            english_reader,
            r"(?s)Peasant.{0,80}artillery.{0,180}"
            r"friendly defender.{0,80}eight cells",
        )
        self.assertNotIn("enemy infantry within four cells", english_reader)
        self.assertNotIn("Wooden Gate", english)
        self.assertNotIn("Stone Gate", english)

        for technical in (russian_technical, english_technical):
            self.assertIn("_unit_SearchCapturersForWall", technical)
            self.assertIn("_unit_SearchProtectors", technical)
            self.assertIn("not bbuilding", technical)

    def test_turkish_tower_interval_and_canonical_ferry_name(self):
        russian = (
            DOCS / "recon" / "world" / "combat" / "towers.md"
        ).read_text(encoding="utf-8")
        english = (
            ROOT / "docs_en" / "recon" / "world" / "combat" / "towers.md"
        ).read_text(encoding="utf-8")

        self.assertIn("интервал на 25 % длиннее", russian)
        self.assertRegex(russian, r"темп стрельбы ниже на 20 %")
        self.assertNotIn("−25 % к темпу стрельбы", russian)

        self.assertIn("a 25% longer interval", english)
        self.assertIn("a 20% lower rate of fire", english)
        self.assertNotIn("25% lower rate of fire", english)
        self.assertIn("Mines and **Ferries**", english)
        self.assertNotIn("Transport Ship", english)

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

    def test_recon_keeps_research_backlogs_out_of_reader_articles(self):
        heading_patterns = (
            r"^#{2,4}\s+.*(?:открытые\s+(?:вопросы|эмпирические\s+вопросы))",
            r"^#{2,4}\s+.*(?:что\s+ещ[ёе]\s+(?:нужно|требует)\s+провер)",
            r"^#{2,4}\s+.*(?:open\s+(?:questions|empirical\s+questions))",
            r"^#{2,4}\s+.*(?:questions\s+requiring\s+further\s+testing)",
            r"^#{2,4}\s+.*(?:what\s+still\s+needs\s+(?:testing|verification))",
        )
        prose_patterns = (
            r"research_backlog",
            r"\b(?:research\s+(?:questions?|backlog)|open\s+questions?)\b",
            r"(?:исследовательск\w+\s+вопрос\w*|план\w*\s+(?:дальнейшего\s+)?"
            r"исследован\w*|открыт\w*\s+вопрос\w*)",
        )
        offenders = []
        for tree in (DOCS / "recon", ROOT / "docs_en" / "recon"):
            for path in tree.rglob("*.md"):
                text = path.read_text(encoding="utf-8")
                if any(
                    re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE)
                    for pattern in (*heading_patterns, *prose_patterns)
                ):
                    offenders.append(path.relative_to(ROOT).as_posix())
        self.assertEqual(offenders, [])

    def test_recon_does_not_narrate_the_research_search_process(self):
        research_narration = re.compile(
            r"(?:в\s+(?:изученном|просмотренном)\s+коде.{0,80}не\s+найден)"
            r"|(?:не\s+найдено\s+в\s+`[^`]+`)"
            r"|(?:вероятно,?\s+движок)"
            r"|(?:скриптового.{0,60}не\s+найдено)"
            r"|(?:the\s+inspected\s+code\s+does\s+not\s+confirm)"
            r"|(?:has\s+not\s+been\s+found\s+in)"
            r"|(?:no.{0,60}(?:was|has\s+been)\s+found\s+in)"
            r"|(?:\bне\s+измерен[аоы]?\b)"
            r"|(?:\bконтрольн(?:ое|ый)\s+измерени)"
            r"|(?:\bтекущ(?:ий|его)\s+парсер\b)"
            r"|(?:\bограничени[ея]\s+текущих\s+выгрузок\b)"
            r"|(?:\bhas\s+not\s+(?:yet\s+)?been\s+measured\b)"
            r"|(?:\bcontrol\s+measurement\b)"
            r"|(?:\bcurrent\s+parser\b)"
            r"|(?:\bcurrent\s+exported\s+data\b)",
            flags=re.IGNORECASE | re.DOTALL,
        )
        offenders = []
        for tree in (DOCS / "recon", ROOT / "docs_en" / "recon"):
            for path in tree.rglob("*.md"):
                visible = reader_visible_text(path.read_text(encoding="utf-8"))
                if research_narration.search(visible):
                    offenders.append(path.relative_to(ROOT).as_posix())
        self.assertEqual(offenders, [])

    def test_large_recon_articles_keep_evidence_in_internals(self):
        pages = (
            ("world/combat/pathfinding.md", "pathfinding_evidence.md"),
            ("world/combat/target_selection.md", "target_selection_evidence.md"),
            ("world/map/map_generation_pipeline.md", "map_generation_evidence.md"),
        )
        for language in ("", "_en"):
            docs_root = ROOT / f"docs{language}" / "recon"
            internals_root = ROOT / f"internals{language}" / "scripts"
            for relative_page, evidence_name in pages:
                reader_path = docs_root / relative_page
                evidence_path = internals_root / evidence_name
                with self.subTest(language=language or "ru", page=relative_page):
                    self.assertLess(reader_path.stat().st_size, 20_000)
                    self.assertGreater(evidence_path.stat().st_size, 30_000)
                    reader = reader_path.read_text(encoding="utf-8")
                    self.assertIn(evidence_name, reader)

    def test_ai_article_keeps_engine_symbols_in_technical_details(self):
        pages = (
            (
                DOCS / "recon" / "systems" / "ai_behavior.md",
                "## Техническая карта исходных файлов",
                "не более **двух одновременно действующих диверсионных армий**",
            ),
            (
                ROOT / "docs_en" / "recon" / "systems" / "ai_behavior.md",
                "## Technical source map",
                "no more than **two active sabotage armies at once**",
            ),
        )
        raw_engine_detail = re.compile(
            r"`[^`\n]+`|(?:\.inc|\.script)(?::\d+)?|"
            r"\b(?:gc_|_ai_|gMap|gPlayer|aiData|num[A-Z])\w*"
        )
        for path, marker, sabotage_rule in pages:
            text = path.read_text(encoding="utf-8")
            reader, technical = text.split(marker, 1)
            with self.subTest(path=path.relative_to(ROOT).as_posix()):
                self.assertNotRegex(reader, raw_engine_detail)
                self.assertIn("372", reader)
                self.assertIn(sabotage_rule, reader)
                for preserved_detail in (
                    "`_ai_RequestUnitsProduction`",
                    "`numOfficers = pikemanCount div 36`",
                    "`gc_ai_MaxDiverArmies`",
                    "`gc_ai_armyorder_*`",
                ):
                    self.assertIn(preserved_detail, technical)

    def test_recon_prose_does_not_expose_english_engine_jargon(self):
        jargon = (
            "апгрейд",
            "скирмиш",
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
            "bird",
            "cossacks",
            "early",
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

    def test_reader_first_articles_keep_inline_engine_names_below_the_appendix(self):
        reader_first_pages = (
            "systems/ai_behavior.md",
            "systems/mercenaries_diplomacy.md",
            "world/combat/ranged_units_behavior.md",
            "world/combat/walls_and_gates.md",
        )
        offenders = []
        for root in (DOCS / "recon", ROOT / "docs_en" / "recon"):
            for relative in reader_first_pages:
                path = root / relative
                text = path.read_text(encoding="utf-8")
                technical = re.search(
                    r"^##\s+.*(?:техническ|technical)",
                    text,
                    flags=re.IGNORECASE | re.MULTILINE,
                )
                self.assertIsNotNone(technical, path)
                reader_section = re.sub(
                    r"```.*?```",
                    "",
                    text[: technical.start()],
                    flags=re.DOTALL,
                )
                inline_code = re.findall(r"`([^`\n]+)`", reader_section)
                if inline_code:
                    offenders.append(
                        f"{path.relative_to(ROOT).as_posix()}: "
                        f"{', '.join(inline_code[:5])}"
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

    def test_starting_army_presets_do_not_claim_eighteen_peasants_are_universal(self):
        russian = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (
                DOCS / "recon" / "world" / "map" / "game_settings.md",
                DOCS / "reports" / "map" / "lobby_settings.md",
            )
        )
        english = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (
                ROOT / "docs_en" / "recon" / "world" / "map" / "game_settings.md",
                ROOT / "docs_en" / "reports" / "map" / "lobby_settings.md",
            )
        )
        self.assertNotRegex(
            russian,
            r"(?is)(?:независимо от выбора|появляются всегда).{0,160}18 крестьян"
            r"|18 крестьян.{0,80}(?:всегда|независимо от выбора)",
        )
        self.assertNotRegex(
            english,
            r"(?is)(?:regardless of (?:the )?choice|always appear).{0,160}18 peasants"
            r"|18 peasants.{0,80}(?:always|regardless of (?:the )?choice)",
        )
        self.assertIn("«По умолчанию»", russian)
        self.assertIn("Default", english)
        self.assertRegex(russian, r"(?i)(?:заменяет|заменяют|вместо стандартной группы)")
        self.assertRegex(english, r"(?i)(?:replace|replaces|replaced|instead of)")
        generator = (ROOT / "compute" / "compute_starting_layout.py").read_text(
            encoding="utf-8"
        )
        self.assertIn("Остальные режимы заменяют эту группу", generator)
        self.assertNotIn("Остальные режимы добавляют", generator)

    def test_land_forest_override_is_not_generalized_to_every_map_type(self):
        russian = (
            DOCS / "recon" / "world" / "map" / "game_settings.md"
        ).read_text(encoding="utf-8")
        english = (
            ROOT / "docs_en" / "recon" / "world" / "map" / "game_settings.md"
        ).read_text(encoding="utf-8")
        self.assertNotIn("для любого типа местности", russian)
        self.assertNotIn("for every terrain type", english)
        self.assertRegex(russian, r"(?:Для|На) карт[еы] «Суша»")
        self.assertIn("On Land maps", english)
        russian_evidence = (
            ROOT / "internals" / "scripts" / "map_generation_evidence.md"
        ).read_text(encoding="utf-8")
        english_evidence = (
            ROOT / "internals_en" / "scripts" / "map_generation_evidence.md"
        ).read_text(encoding="utf-8")
        generator = (ROOT / "compute" / "compute_starting_layout.py").read_text(
            encoding="utf-8"
        )
        self.assertNotIn("Тип леса всегда равен", russian_evidence)
        self.assertNotIn("Forest type always equals", english_evidence)
        self.assertIn("Для карты «Суша» тип леса", russian_evidence)
        self.assertIn("On Land maps, `foreststype` is forced", english_evidence)
        self.assertIn("На карте «Суша» генератор", generator)

    def test_economy_summaries_match_mine_and_repair_source_values(self):
        russian_economy = (
            DOCS / "reference" / "01_economy" / "README.md"
        ).read_text(encoding="utf-8")
        english_economy = (
            ROOT / "docs_en" / "reference" / "01_economy" / "README.md"
        ).read_text(encoding="utf-8")
        russian_buildings = (
            DOCS / "reference" / "03_buildings" / "README.md"
        ).read_text(encoding="utf-8")
        english_buildings = (
            ROOT / "docs_en" / "reference" / "03_buildings" / "README.md"
        ).read_text(encoding="utf-8")
        self.assertIn("93,75 игровой секунды", russian_economy)
        self.assertIn("93.75 game seconds", english_economy)
        self.assertIn("49,3 прочности", russian_buildings)
        self.assertIn("49.3 durability", english_buildings)
        self.assertNotIn("9,38 игровой секунды", russian_economy)
        self.assertNotIn("29 прочности", russian_buildings)

    def test_combat_guides_keep_verified_naval_and_dispersion_facts(self):
        russian_combat = DOCS / "recon" / "world" / "combat"
        english_combat = ROOT / "docs_en" / "recon" / "world" / "combat"
        naval_ru = (russian_combat / "naval_combat.md").read_text(
            encoding="utf-8"
        )
        naval_en = (english_combat / "naval_combat.md").read_text(
            encoding="utf-8"
        )
        ranged_ru = (russian_combat / "ranged_units_behavior.md").read_text(
            encoding="utf-8"
        )
        ranged_en = (english_combat / "ranged_units_behavior.md").read_text(
            encoding="utf-8"
        )
        commands_ru = (russian_combat / "unit_commands.md").read_text(
            encoding="utf-8"
        )

        for fact in ("62 000 здоровья", "1800 базового урона", "около 35"):
            self.assertIn(fact, naval_ru)
        for fact in ("62,000 health", "1,800 raw Cannon damage", "about 35"):
            self.assertIn(fact, naval_en)
        self.assertIn("Строй 3–4 Транспорта", naval_ru)
        self.assertIn("Build three or four Ferries", naval_en)
        self.assertNotIn("Брандер", naval_ru)
        self.assertNotIn("Fireship", naval_en)
        self.assertNotIn("за пару залпов", naval_ru)
        self.assertNotIn("couple of volleys", naval_en)
        self.assertNotIn("одна пушка с берега может потопить", naval_ru)
        self.assertNotIn("one Cannon on the coast can destroy", naval_en)

        self.assertIn("не больше 9 юнитов", ranged_ru)
        self.assertIn("more than nine targets", ranged_en)
        self.assertIn("показатель разброса на 14,3 % больше", ranged_ru)
        self.assertIn("dispersion value is 14.3% larger", ranged_en)
        self.assertNotIn("точность на 14 % хуже", ranged_ru)
        self.assertNotIn("14% less accurate", ranged_en)
        self.assertNotIn("target_selection.md)).", commands_ru)

    def test_combat_recon_matches_verified_engine_behavior(self):
        russian_combat = DOCS / "recon" / "world" / "combat"
        english_combat = ROOT / "docs_en" / "recon" / "world" / "combat"

        def read_pair(name):
            return (
                (russian_combat / name).read_text(encoding="utf-8"),
                (english_combat / name).read_text(encoding="utf-8"),
            )

        damage_ru, damage_en = read_pair("combat_damage_pipeline.md")
        artillery_ru, artillery_en = read_pair("artillery_specifics.md")
        naval_ru, naval_en = read_pair("naval_combat.md")
        towers_ru, towers_en = read_pair("towers.md")
        formations_ru, formations_en = read_pair("formations.md")
        paths_ru, paths_en = read_pair("pathfinding.md")
        vision_ru, vision_en = read_pair("vision_and_fow.md")
        damage_ru_compact = " ".join(damage_ru.split())
        damage_en_compact = " ".join(damage_en.split())
        towers_ru_compact = " ".join(towers_ru.split())
        towers_en_compact = " ".join(towers_en.split())
        vision_ru_compact = " ".join(vision_ru.split())
        vision_en_compact = " ".join(vision_en.split())
        paths_ru_compact = " ".join(paths_ru.split())
        paths_en_compact = " ".join(paths_en.split())

        self.assertIn(
            "общий поток `random` без предварительного `SetRandomKey`",
            damage_ru_compact,
        )
        self.assertIn(
            "shared `random` stream without a preceding `SetRandomKey`",
            damage_en_compact,
        )
        self.assertNotIn("Перед проверкой 5%-шанса", damage_ru)
        self.assertNotIn("Before checking the 5% chance", damage_en)
        self.assertIn(
            "добавляется **после** защиты по типу оружия", damage_ru_compact
        )
        self.assertIn(
            "added **after** weapon-type protection", damage_en_compact
        )
        self.assertNotIn("срабатывает **до** шага 4", damage_ru)
        self.assertNotIn("**before** step 4", damage_en)
        self.assertNotIn("Суммарный урон по", damage_ru)
        self.assertNotIn("Total damage", damage_en)

        formula = "`maxdisp = distance × dispertion × 0.0267`"
        self.assertIn(formula, artillery_ru)
        self.assertIn(formula, artillery_en)
        self.assertNotIn("spread_pct", artillery_ru)
        self.assertNotIn("spread_pct", artillery_en)
        self.assertNotIn("weapon_aoe_radius", artillery_ru)
        self.assertNotIn("weapon_aoe_radius", artillery_en)
        self.assertNotIn("ограничивает суммарный урон", artillery_ru)
        self.assertNotIn("limits how much total damage", artillery_en)

        self.assertIn("≈ 160 за игровую минуту", naval_ru)
        self.assertIn("about 160 per game minute", naval_en)
        self.assertIn("а не ускоряют отдельный шаг добычи", naval_ru)
        self.assertIn("rather than speeding up each gathering step", naval_en)

        self.assertIn(
            "напрямую сравнивать их с числом 32 нельзя", towers_ru_compact
        )
        self.assertIn("cannot be compared directly", towers_en_compact)
        self.assertIn(
            "напрямую сравнивать эти числа нельзя", vision_ru_compact
        )
        self.assertIn("cannot be compared directly", vision_en_compact)
        self.assertNotIn("С обзором в 32 клетки", towers_ru)
        self.assertNotIn("With a 32-cell vision radius", towers_en)
        self.assertIn(formula, towers_ru)
        self.assertIn(formula, towers_en)
        self.assertIn("около **1,41 клетки по каждой оси**", towers_ru)
        self.assertIn("about **1.41 cells on each axis**", towers_en)

        formations_ru_compact = " ".join(formations_ru.split())
        formations_en_compact = " ".join(formations_en.split())
        self.assertIn(
            "**после** вычитания базовой защиты (`shield`), но **до** защиты",
            formations_ru_compact,
        )
        self.assertIn(
            "**after** subtracting `shield`, but **before** `protection[kind]`",
            formations_en_compact,
        )

        self.assertIn(
            "Гарантированный способ создать новый запрос пути", paths_ru_compact
        )
        self.assertIn(
            "The guaranteed way to create a fresh path request", paths_en_compact
        )
        self.assertNotIn("Постоянной полной перепроверки", paths_ru)
        self.assertNotIn("does not rebuild every complete route", paths_en)
        self.assertNotIn("юниты обойдут её даже до того", vision_ru)
        self.assertNotIn("route around it even before", vision_en)

        backlog_ru = (
            ROOT / "internals" / "project" / "research_backlog_combat.md"
        ).read_text(encoding="utf-8")
        backlog_en = (
            ROOT / "internals_en" / "project" / "research_backlog_combat.md"
        ).read_text(encoding="utf-8")
        self.assertNotIn("Зависимость рассеяния от расстояния", backlog_ru)
        self.assertNotIn("How dispersion scales with distance", backlog_en)
        self.assertNotIn("Формула разброса Башни", backlog_ru)
        self.assertNotIn("Tower dispersion formula", backlog_en)
        self.assertIn("Предел суммарного урона по области", backlog_ru)
        self.assertIn("Total area-damage cap", backlog_en)

    def test_recon_blocker_regressions_stay_fixed(self):
        combat_ru = DOCS / "recon" / "world" / "combat"
        combat_en = ROOT / "docs_en" / "recon" / "world" / "combat"

        commands_ru = (combat_ru / "unit_commands.md").read_text(encoding="utf-8")
        commands_en = (combat_en / "unit_commands.md").read_text(encoding="utf-8")
        self.assertIn("во всём доступном радиусе", " ".join(commands_ru.split()))
        self.assertIn(
            "throughout its available radius", " ".join(commands_en.split())
        )
        self.assertNotIn("only in a 30° cone ahead", commands_en)

        walls_ru = (combat_ru / "walls_and_gates.md").read_text(encoding="utf-8")
        walls_en = (combat_en / "walls_and_gates.md").read_text(encoding="utf-8")
        self.assertIn("не меньше трети максимальной прочности", walls_ru)
        self.assertIn(
            "at least one third of their maximum durability",
            " ".join(walls_en.split()),
        )

        damage_ru = (combat_ru / "combat_damage_pipeline.md").read_text(
            encoding="utf-8"
        )
        damage_en = (combat_en / "combat_damage_pipeline.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("+2 × базовая ценность цели", damage_ru)
        self.assertIn("+2 × the target's base point value", damage_en)
        self.assertNotIn("+2 × cost", damage_en)

        ai_en = (
            ROOT / "docs_en" / "recon" / "systems" / "ai_behavior.md"
        ).read_text(encoding="utf-8")
        self.assertNotIn("Howitzers or Mortars", ai_en)
        self.assertIn("Howitzers or Bombards", ai_en)

        english_recon = "\n".join(
            reader_visible_text(path.read_text(encoding="utf-8"))
            for path in (ROOT / "docs_en" / "recon").rglob("*.md")
        )
        self.assertNotRegex(english_recon, r"(?i)\bskirmish\b")

        capture_en = (
            ROOT
            / "docs_en"
            / "recon"
            / "world"
            / "economy"
            / "capture_mechanics.md"
        ).read_text(encoding="utf-8")
        self.assertIn("objects are not all processed at once", capture_en)
        self.assertNotIn("every object on the map is not processed", capture_en)

    def test_famine_and_rebellion_probabilities_cadence_and_score_direction(self):
        russian = (
            DOCS / "recon" / "world" / "economy" / "hunger_and_rebellion.md"
        ).read_text(encoding="utf-8")
        english = (
            ROOT
            / "docs_en"
            / "recon"
            / "world"
            / "economy"
            / "hunger_and_rebellion.md"
        ).read_text(encoding="utf-8")
        russian_backlog = (
            ROOT / "internals" / "project" / "research_backlog_systems.md"
        ).read_text(encoding="utf-8")
        english_backlog = (
            ROOT / "internals_en" / "project" / "research_backlog_systems.md"
        ).read_text(encoding="utf-8")
        russian_compact = " ".join(russian.split())
        english_compact = " ".join(english.split())

        for value in ("0,0153 %", "0,0366 %", "0,1526 %"):
            self.assertIn(value, russian)
        for value in ("0.0153%", "0.0366%", "0.1526%"):
            self.assertIn(value, english)
        self.assertIn("из счёта прежнего владельца", russian)
        self.assertIn("Одновременно новому служебному владельцу", russian_compact)
        self.assertIn("тройная базовая ценность", russian_compact)
        self.assertIn("обычная одинарная ценность", russian_compact)
        self.assertNotIn("Другому игроку эти очки не начисляются", russian)
        self.assertIn("former owner's score", english)
        self.assertIn("new game-controlled owner receives", english_compact)
        self.assertIn("three times that unit's base value", english_compact)
        self.assertIn("receives the unit's base value once", english_compact)
        self.assertNotRegex(english, r"No opponent receives those\s+points")
        self.assertIn("На сложном уровне и выше", russian_compact)
        self.assertNotIn(
            "точный интервал проверок в игровых секундах пока не измерен",
            russian_compact,
        )
        self.assertNotIn("почти мгновенно", russian)
        self.assertIn("On Hard and above", english_compact)
        self.assertNotIn(
            "exact interval between checks in game seconds has not yet been measured",
            english_compact,
        )
        self.assertNotIn("almost at once", english)
        self.assertNotIn("135 мс", russian_backlog)
        self.assertNotIn("100 ms", english_backlog)
        self.assertIn("перевод в игровые секунды не измерен", russian_backlog)
        self.assertIn("conversion to game seconds has not been measured", english_backlog)

    def test_russian_serf_food_cycle_exception_is_documented(self):
        russian = (
            DOCS / "recon" / "world" / "economy" / "peasant_extraction.md"
        ).read_text(encoding="utf-8")
        english = (
            ROOT
            / "docs_en"
            / "recon"
            / "world"
            / "economy"
            / "peasant_extraction.md"
        ).read_text(encoding="utf-8")

        self.assertIn(
            "| Еда — большинство наций | 22 | 45 | 0,6875 игровой секунды | около 178 |",
            russian,
        )
        self.assertIn(
            "| Еда — **Крепостной** (Россия) | 22 | 45 | "
            "0,7188 игровой секунды (23 кадра) | около 171 |",
            russian,
        )
        self.assertIn(
            "| Food — most nations | 22 | 45 | 0.6875 game seconds | about 178 |",
            english,
        )
        self.assertIn(
            "| Food — **Serf** (Russia) | 22 | 45 | "
            "0.7188 game seconds (23 frames) | about 171 |",
            english,
        )

    def test_production_refund_keeps_one_tier_per_queue_entry(self):
        russian = (
            DOCS / "recon" / "world" / "economy" / "production_queue.md"
        ).read_text(encoding="utf-8")
        english = (
            ROOT
            / "docs_en"
            / "recon"
            / "world"
            / "economy"
            / "production_queue.md"
        ).read_text(encoding="utf-8")
        russian_compact = " ".join(russian.split())
        english_compact = " ".join(english.split())

        for fact in (
            "по одной и той же ступени",
            "Счётчик отменяемых копий в формулу не входит",
            "текущее значение",
            "улучшение, которое меняет цену юнита, меняет и сумму возврата",
        ):
            self.assertIn(fact, russian_compact)
        for fact in (
            "the same tier",
            "number of the canceled copy does not enter the formula",
            "current base price",
            "upgrade that changes the unit's price and completes after the "
            "order also changes the refund",
        ):
            self.assertIn(fact, english_compact)
        self.assertNotIn(
            "сумма рассчитывается отдельно для каждого из пяти",
            russian_compact,
        )
        self.assertNotIn("calculates five separate prices", english_compact)

    def test_resource_gathering_keeps_exact_tree_ranges_and_upgrade_chains(self):
        russian = (
            DOCS / "recon" / "world" / "economy" / "peasant_extraction.md"
        ).read_text(encoding="utf-8")
        english = (
            ROOT
            / "docs_en"
            / "recon"
            / "world"
            / "economy"
            / "peasant_extraction.md"
        ).read_text(encoding="utf-8")

        for fact in (
            "8 000–15 999",
            "20–74",
            "Усовершенствовать способы переработки зерна",
            "+140 %",
            "Усовершенствовать способы хранения зерна",
            "+180 %",
            "Культивировать новые сорта пшеницы",
            "Культивировать новые сорта ржи",
            "Увеличить жалование земледельцам",
            "560 %",
            "380 %",
        ):
            self.assertIn(fact, russian)
        for fact in (
            "8,000–15,999",
            "20–74",
            "Improve grain crops treatment",
            "+140%",
            "Improve grain crops storage",
            "+180%",
            "Cultivate new cultures of wheat",
            "Cultivate new cultures of rye",
            "Raise agriculturists' salary",
            "560%",
            "380%",
        ):
            self.assertIn(fact, english)
        for stale in (
            "8 000–16 000",
            "примерно 20–75",
            "три последовательных улучшения Мельницы",
        ):
            self.assertNotIn(stale, russian)
        for stale in (
            "8,000–16,000",
            "about 20–75",
            "three successive Mill upgrades",
        ):
            self.assertNotIn(stale, english)

    def test_three_nations_have_no_available_18th_century_transition(self):
        russian = (
            DOCS / "recon" / "world" / "economy" / "upgrades_application.md"
        ).read_text(encoding="utf-8")
        english = (
            ROOT
            / "docs_en"
            / "recon"
            / "world"
            / "economy"
            / "upgrades_application.md"
        ).read_text(encoding="utf-8")
        russian_evidence = (
            ROOT / "internals" / "scripts" / "upgrades_application_evidence.md"
        ).read_text(encoding="utf-8")
        english_evidence = (
            ROOT
            / "internals_en"
            / "scripts"
            / "upgrades_application_evidence.md"
        ).read_text(encoding="utf-8")
        russian_compact = " ".join(russian.split())
        english_compact = " ".join(english.split())
        russian_evidence_compact = " ".join(russian_evidence.split())
        english_evidence_compact = " ".join(english_evidence.split())

        self.assertIn(
            "Украина, Турция и Алжир не имеют доступного перехода в XVIII век",
            russian_compact,
        )
        self.assertIn(
            "Ukraine, Turkey, and Algeria have neither an available "
            "18th-century transition",
            english_compact,
        )
        for nation in ("Алжир", "Турция", "Украина"):
            self.assertRegex(
                russian_evidence,
                rf"\| {nation} \(`\w+`\) \| ❌ \| ❌ \|",
            )
        for nation in ("Algeria", "Turkey", "Ukraine"):
            self.assertRegex(
                english_evidence,
                rf"\| {nation} \(`\w+`\) \| ❌ \| ❌ \|",
            )
        for fact in (
            "`place = null`",
            "`member = null`",
            "пустой `_source`",
            "В сгенерированном дереве развития этих переходов также нет",
        ):
            self.assertIn(fact, russian_evidence_compact)
        for fact in (
            "`place` and `member` fields are null",
            "`_source` is empty",
            "generated technology tree does not contain these transitions",
        ):
            self.assertIn(fact, english_evidence_compact)
        self.assertNotIn("Их переход открывает", russian)
        self.assertNotIn("Their transition opens", english)
        self.assertNotRegex(
            russian_evidence,
            r"\| (?:Алжир|Турция|Украина) \(`\w+`\) \| ✅ \| ❌ \|",
        )
        self.assertNotRegex(
            english_evidence,
            r"\| (?:Algeria|Turkey|Ukraine) \(`\w+`\) \| ✅ \| ❌ \|",
        )

    def test_farmused_counts_non_building_population_not_surviving_structures(self):
        russian = (
            DOCS / "recon" / "systems" / "victory_conditions.md"
        ).read_text(encoding="utf-8")
        english = (
            ROOT / "docs_en" / "recon" / "systems" / "victory_conditions.md"
        ).read_text(encoding="utf-8")
        russian_compact = " ".join(russian.split())
        english_compact = " ".join(english.split())

        for fact in (
            "юнита, который не является зданием",
            "не показывает ни число построек, ни вместимость жилья",
            "даже если у него ещё стоят Городской центр",
            "ничего не сообщает о сохранившихся постройках",
            "При значении 100 и выше",
        ):
            self.assertIn(fact, russian_compact)
        for fact in (
            "unit that is not a building",
            "records neither the number of buildings nor housing capacity",
            "even if the player still owns a Town Hall",
            "it says nothing about surviving structures",
            "At 100 or more",
        ):
            self.assertIn(fact, english_compact)
        for stale in (
            "Игрок считается выбывшим, когда у него не остаётся ни одного "
            "крестьянина и ни одного Городского центра",
            "то есть у игрока нет ни одного крестьянина и ни одного "
            "центра/населённой постройки",
        ):
            self.assertNotIn(stale, russian_compact)
        for stale in (
            "A player is eliminated after losing every Peasant and every Town Hall",
            "the player has no Peasant and no Town Hall or other "
            "population-providing building",
        ):
            self.assertNotIn(stale, english_compact)

    def test_mercenary_score_penalty_happens_during_ownership_transfer(self):
        russian = (
            DOCS / "recon" / "systems" / "mercenaries_diplomacy.md"
        ).read_text(encoding="utf-8")
        english = (
            ROOT
            / "docs_en"
            / "recon"
            / "systems"
            / "mercenaries_diplomacy.md"
        ).read_text(encoding="utf-8")
        russian_reader = reader_visible_text(
            russian.split("## Технические подробности", 1)[0]
        )
        english_reader = reader_visible_text(
            english.split("## Technical details", 1)[0]
        )
        russian_compact = " ".join(russian_reader.split())
        english_compact = " ".join(english_reader.split())

        for fact in (
            "сразу вычитается **3× базовая ценность юнита**",
            "новому владельцу начисляется обычная **1× базовая ценность**",
            "смену владельца во время бунта",
            "не за последующую гибель или потерю юнита",
        ):
            self.assertIn(fact, russian_compact)
        for fact in (
            "three times the unit's base value",
            "receives the unit's base value **once** during the same transfer",
            "ownership transfer during rebellion",
            "not for the unit's later death or loss",
            "**Easy:** 0.305% per check",
            "**Normal:** 0.610% per check",
            "**Hard and above:** 18.31% per check",
        ):
            self.assertIn(fact, english_compact)
        self.assertIn("Сечевой козак", russian_compact)
        self.assertNotIn("Сечевой казак", russian_compact)
        self.assertIn("**6 базовых наёмников**", russian_compact)
        self.assertIn("Early Bird к ним добавляются", russian_compact)
        self.assertIn("**six base mercenaries**", english_compact)
        self.assertIn("Early Bird DLC adds", english_compact)
        self.assertNotRegex(russian_reader, r"\b(?:40|48|64|80|720)\s+кадр")
        self.assertNotRegex(english_reader, r"\b(?:40|48|64|80|720)\s+frames?\b")
        self.assertNotIn("пикселей", russian_reader)
        self.assertNotIn(" px", english_reader)
        self.assertNotIn("per update", english_compact)
        self.assertNotIn(
            "гибель наёмника во время бунта уменьшает счёт",
            russian_compact,
        )
        self.assertNotIn(
            "A mercenary lost during rebellion therefore costs more score",
            english_compact,
        )

        for raw_name in (
            "costpercent",
            "archerdip",
            "_player_processresourceconsume",
            "resconsume",
            "bfamine",
            "brebellion",
            "_misc_randomint",
            "gc_player_mercenaryind",
            "enemyplmask",
            "marketdip",
            "expensivemercs",
            "consume.gold",
            "bnohungry",
            "player.script",
            "nothing.inc",
        ):
            self.assertNotIn(raw_name, russian_reader.lower())
            self.assertNotIn(raw_name, english_reader.lower())

    def test_recon_economy_articles_keep_correct_live_process_and_position_rules(self):
        economy = DOCS / "recon" / "world" / "economy"
        economy_en = ROOT / "docs_en" / "recon" / "world" / "economy"

        upgrades_ru = (economy / "upgrades_application.md").read_text(
            encoding="utf-8"
        )
        upgrades_en = (economy_en / "upgrades_application.md").read_text(
            encoding="utf-8"
        )
        upgrades_ru_compact = " ".join(upgrades_ru.split())
        upgrades_en_compact = " ".join(upgrades_en.split())
        self.assertIn("со следующего обновления прогресса", upgrades_ru_compact)
        self.assertIn(
            "ускоряются и новые, и уже идущие процессы",
            upgrades_ru_compact,
        )
        self.assertIn("from its next progress update", upgrades_en_compact)
        self.assertIn(
            "Both new and ongoing work therefore accelerate",
            upgrades_en_compact,
        )
        for stale in (
            "не ускоряет уже начатый",
            "текущий процесс сохраняет прежнюю длительность",
            "только для заказов, созданных",
        ):
            self.assertNotIn(stale, upgrades_ru)
        for stale in (
            "does not accelerate a process that has already started",
            "the current process keeps its old duration",
            "begins affecting only orders created after",
        ):
            self.assertNotIn(stale, upgrades_en)

        buildings_ru = (economy / "building_mechanics.md").read_text(
            encoding="utf-8"
        )
        buildings_en = (economy_en / "building_mechanics.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("прочности до 1 999 или ниже", buildings_ru)
        self.assertIn("ниже 10 единиц", buildings_ru)
        self.assertIn("slow collapse", buildings_en)
        self.assertRegex(buildings_en, r"1,999 durability or less")
        self.assertRegex(buildings_en, r"Below\s+10 durability")
        self.assertNotIn("Здания не ветшают сами по себе", buildings_ru)
        self.assertNotIn(
            "Здания не теряют прочность от времени.",
            buildings_ru,
        )
        self.assertNotIn("Buildings do not decay by themselves", buildings_en)
        self.assertNotIn(
            "Buildings do not lose durability over time.",
            buildings_en,
        )

        capture_ru = (economy / "capture_mechanics.md").read_text(
            encoding="utf-8"
        )
        capture_en = (economy_en / "capture_mechanics.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("позициями объектов, которые возвращает", capture_ru)
        self.assertRegex(capture_en, r"object positions\s+returned by the engine")
        self.assertNotIn("опорной точки, расположенной около центра", capture_ru)
        self.assertNotIn("object's reference point", capture_en)
        self.assertNotRegex(
            capture_ru,
            r"(?is)(?:позици|точк).{0,80}(?:центр\s+модели|"
            r"геометрическ\w*\s+центр)",
        )
        self.assertNotRegex(
            capture_en,
            r"(?is)(?:position|point).{0,80}(?:model center|"
            r"center of the model|near its center)",
        )

    def test_english_reader_docs_use_consistent_american_spelling(self):
        british_spellings = re.compile(
            r"\b(?:behaviours?|armours?|neighbours?|centres?|localisation|"
            r"cancelled|cancelling|favours?|modelled|modelling|"
            r"manoeuv(?:re|res|red|ring))\b",
            flags=re.IGNORECASE,
        )
        offenders = []
        for path in (ROOT / "docs_en").rglob("*.md"):
            visible = reader_visible_text(path.read_text(encoding="utf-8"))
            visible = visible.replace("No Capturing Peasants or Centres", "")
            found = sorted(
                {match.group(0) for match in british_spellings.finditer(visible)},
                key=str.casefold,
            )
            if found:
                offenders.append(
                    f"{path.relative_to(ROOT).as_posix()}: {', '.join(found)}"
                )
        self.assertEqual(offenders, [])

    def test_english_prose_uses_consistent_american_variants(self):
        british_spellings = re.compile(
            r"\b(?:defence|colour(?:s|ed|ing)?|centres?|favours?|"
            r"modelled|modelling)\b",
            flags=re.IGNORECASE,
        )
        offenders = []
        for tree in (ROOT / "docs_en" / "recon", ROOT / "internals_en"):
            for path in tree.rglob("*.md"):
                visible = reader_visible_text(path.read_text(encoding="utf-8"))
                visible = visible.replace("No Capturing Peasants or Centres", "")
                found = sorted(
                    {match.group(0) for match in british_spellings.finditer(visible)},
                    key=str.casefold,
                )
                if found:
                    offenders.append(
                        f"{path.relative_to(ROOT).as_posix()}: {', '.join(found)}"
                    )
        self.assertEqual(offenders, [])

    def test_english_reader_docs_use_cells_and_game_seconds(self):
        legacy_units = re.compile(
            r"\btiles?\b|\bg-sec\b|\bgame sec\b",
            flags=re.IGNORECASE,
        )
        offenders = []
        for path in (ROOT / "docs_en").rglob("*.md"):
            visible = reader_visible_text(path.read_text(encoding="utf-8"))
            found = sorted(
                {match.group(0) for match in legacy_units.finditer(visible)},
                key=str.casefold,
            )
            if found:
                offenders.append(
                    f"{path.relative_to(ROOT).as_posix()}: {', '.join(found)}"
                )
        self.assertEqual(offenders, [])

    def test_english_reader_docs_do_not_expose_untranslated_cyrillic(self):
        offenders = []
        for path in (ROOT / "docs_en").rglob("*.md"):
            visible = reader_visible_text(path.read_text(encoding="utf-8"))
            visible = visible.replace("[Русский]", "")
            if re.search(r"[А-Яа-яЁё]", visible):
                offenders.append(path.relative_to(ROOT).as_posix())
        self.assertEqual(offenders, [])

    def test_unit_normalization_does_not_corrupt_projectile_words_or_links(self):
        offenders = []
        for path in (ROOT / "docs_en").rglob("*.md"):
            if "projeccell" in path.read_text(encoding="utf-8").casefold():
                offenders.append(path.relative_to(ROOT).as_posix())
        self.assertEqual(offenders, [])

    def test_english_docs_do_not_retain_known_machine_translation_artifacts(self):
        artifacts = re.compile(
            r"\b(?:upkip|peasant booty|class essence|procedure-deflarations|"
            r"squeezed from|interest is billed|does not works|allows to|"
            r"consists from|represents itself|in current moment|was got)\b"
            r"|(?:time for (?:hiring|construction).{0,20}games?\.\s+with)",
            flags=re.IGNORECASE,
        )
        offenders = []
        for tree in (ROOT / "docs_en", ROOT / "internals_en"):
            for path in tree.rglob("*.md"):
                visible = reader_visible_text(path.read_text(encoding="utf-8"))
                found = sorted(
                    {match.group(0) for match in artifacts.finditer(visible)},
                    key=str.casefold,
                )
                if found:
                    offenders.append(
                        f"{path.relative_to(ROOT).as_posix()}: {', '.join(found)}"
                    )
        self.assertEqual(offenders, [])


if __name__ == "__main__":
    unittest.main()
