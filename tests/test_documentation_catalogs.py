import tempfile
import unittest
from pathlib import Path

from compute.build_md_manifest import markdown_search_text, markdown_sections
from scripts.check_markdown_links import (
    document_ids,
    heading_slug as link_heading_slug,
)
from scripts.build_english_docs import (
    Protector,
    apply_manual_fenced_translations,
    canonicalize_english_unit_list_column,
    clean_english_building_comparison,
    clean_english_nation_page,
    clean_english_upgrade_table,
    ensure_heading_aliases,
    fenced_block_key,
    markdown_structure,
    ROOT,
    sha256,
    translation_artifact_errors,
    validate_pair_text,
)


class SearchText(unittest.TestCase):
    def test_flattens_markdown_but_keeps_diagram_content(self):
        source = """# Replay format

[Details](format.md) and `RecordBegin`.

```
Header -> Body
```
"""
        flattened = markdown_search_text(source)
        self.assertIn("Replay format", flattened)
        self.assertIn("Details and RecordBegin", flattened)
        self.assertIn("Header -> Body", flattened)
        self.assertNotIn("```", flattened)
        self.assertNotIn("format.md", flattened)

    def test_keeps_a_numbered_sentence_continuation(self):
        source = """The total remains below
400. Each Town Hall adds two Peasants.

1. First list item
2. Second list item
"""
        flattened = markdown_search_text(source)
        self.assertIn("below 400. Each Town Hall", flattened)
        self.assertIn("First list item", flattened)
        self.assertIn("Second list item", flattened)

    def test_heading_fragments_use_rendered_markdown_text(self):
        source = """# Reference

## [Юниты](units/README.md)

## `<nat>cen` — Town Hall

## game_object (715)

## 4. Map state_id → handler
"""
        sections = markdown_sections(source)
        self.assertEqual(
            [section["fragment"] for section in sections],
            [
                "юниты",
                "natcen--town-hall",
                "game_object-715",
                "4-map-state_id--handler",
            ],
        )

    def test_link_checker_uses_the_same_rendered_heading_text(self):
        self.assertEqual(link_heading_slug("game_object (715)"), "game_object-715")
        self.assertEqual(
            link_heading_slug("4. Map state_id → handler"),
            "4-map-state_id--handler",
        )
        self.assertEqual(link_heading_slug("`<nat>cen` — Town Hall"), "natcen--town-hall")
        self.assertEqual(link_heading_slug("_Emphasis_"), "emphasis")

    def test_inline_code_anchor_example_is_not_an_explicit_id(self):
        source = """# Reference

Write `<a id="..."></a>` before a translated heading.

```html
<a id="fenced-example"></a>
```

<a id="real-anchor"></a>
<span id='single-quoted-anchor'></span>
## Details
"""
        sections = markdown_sections(source)
        self.assertEqual(sections[0]["fragment"], "details")

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "example.md"
            path.write_text(source, encoding="utf-8")
            ids = document_ids(path)
        self.assertIn("real-anchor", ids)
        self.assertIn("single-quoted-anchor", ids)
        self.assertIn("details", ids)
        self.assertNotIn("...", ids)
        self.assertNotIn("fenced-example", ids)


class HeadingAliases(unittest.TestCase):
    def test_adds_source_slug_before_translated_heading(self):
        source = "# Юниты\n\n## Священники (4 варианта)\n"
        translated = "# Units\n\n## Priests (4 options)\n"
        repaired = ensure_heading_aliases(source, translated)
        self.assertIn('<a id="священники-4-варианта"></a>\n## Priests', repaired)

    def test_does_not_duplicate_existing_alias(self):
        source = "# Юниты\n"
        translated = '<a id="юниты"></a>\n# Units\n'
        repaired = ensure_heading_aliases(source, translated)
        self.assertEqual(repaired.count('id="юниты"'), 1)

    def test_numbers_duplicate_source_heading_aliases(self):
        source = "## Прочность полей\n\n## Прочность полей\n"
        translated = "## Field durability\n\n## Field durability\n"
        repaired = ensure_heading_aliases(source, translated)
        self.assertIn('<a id="прочность-полей"></a>', repaired)
        self.assertIn('<a id="прочность-полей-1"></a>', repaired)

    def test_moves_stale_aliases_to_their_corresponding_headings(self):
        source = """# Справочник

## Карта

## Правила
"""
        translated = """<a id="справочник"></a>
# Reference

<a id="правила"></a>
<a id="legacy-map"></a>
## Map

<a id="карта"></a>
<a id="legacy-rules"></a>
## Rules
"""
        before_errors = validate_pair_text(
            ROOT / "docs" / "fixture.md",
            ROOT / "docs_en" / "fixture.md",
            source,
            translated,
        )
        self.assertTrue(
            any("attached to the wrong" in error for error in before_errors)
        )

        repaired = ensure_heading_aliases(source, translated)
        self.assertIn(
            '<a id="legacy-map"></a>\n'
            '<a id="карта"></a>\n'
            "## Map",
            repaired,
        )
        self.assertIn(
            '<a id="legacy-rules"></a>\n'
            '<a id="правила"></a>\n'
            "## Rules",
            repaired,
        )
        self.assertEqual(repaired.count('id="карта"'), 1)
        self.assertEqual(repaired.count('id="правила"'), 1)
        self.assertEqual(ensure_heading_aliases(source, repaired), repaired)
        after_errors = validate_pair_text(
            ROOT / "docs" / "fixture.md",
            ROOT / "docs_en" / "fixture.md",
            source,
            repaired,
        )
        self.assertFalse(
            any("attached to the wrong" in error for error in after_errors)
        )

    def test_aliases_use_rendered_link_and_inline_code_text(self):
        source = """# Справочник

## [Юниты](units/README.md)

## `<nat>cen` — Городской центр
"""
        translated = """# Reference

## Units

## `<nat>cen` — Town Hall
"""
        repaired = ensure_heading_aliases(source, translated)
        self.assertIn('<a id="юниты"></a>\n## Units', repaired)
        self.assertIn(
            '<a id="natcen--городской-центр"></a>\n'
            "## `<nat>cen` — Town Hall",
            repaired,
        )
        self.assertNotIn("юнитыunitsreadmemd", repaired)

    def test_aliases_preserve_literal_heading_underscores(self):
        source = """# Карта

## game_object (715)

## 4. Карта state_id → handler
"""
        translated = """# Map

## game object (715)

## 4. Map state ID to handler
"""
        repaired = ensure_heading_aliases(source, translated)
        self.assertIn('<a id="game_object-715"></a>\n## game object', repaired)
        self.assertIn(
            '<a id="4-карта-state_id--handler"></a>\n## 4. Map',
            repaired,
        )

    def test_migrates_only_aliases_produced_by_the_legacy_slugger(self):
        source = """# Сравнения

## [Юниты](units/README.md)

## `<nat>cen` — Городской центр
"""
        translated = """<a id="сравнения"></a>
# Comparisons

<a id="unitsreadmemd--сравнения-юнитов"></a>
<a id="юнитыunitsreadmemd"></a>
## [Units](units/README.md)

<a id="cen--городской-центр"></a>
## `<nat>cen` — Town Hall
"""
        repaired = ensure_heading_aliases(source, translated)

        self.assertIn(
            '<a id="unitsreadmemd--сравнения-юнитов"></a>',
            repaired,
        )
        self.assertNotIn('<a id="юнитыunitsreadmemd"></a>', repaired)
        self.assertNotIn('<a id="cen--городской-центр"></a>', repaired)
        self.assertIn('<a id="юниты"></a>\n## [Units]', repaired)
        self.assertIn(
            '<a id="natcen--городской-центр"></a>\n'
            "## `<nat>cen` — Town Hall",
            repaired,
        )
        self.assertEqual(ensure_heading_aliases(source, repaired), repaired)

    def test_compare_template_and_output_have_migrated_link_heading_aliases(self):
        template = (
            ROOT
            / "writers"
            / "templates"
            / "reference"
            / "compare"
            / "README.en.md"
        ).read_text(encoding="utf-8")
        output = (
            ROOT / "docs_en" / "reference" / "compare" / "README.md"
        ).read_text(encoding="utf-8")

        for text in (template, output):
            for alias in ("юниты", "здания", "оружие-и-снаряды"):
                self.assertIn(f'<a id="{alias}"></a>', text)
            for stale in (
                "юнитыunitsreadmemd",
                "зданияbuildingsreadmemd",
                "оружие-и-снарядыweaponsreadmemd",
            ):
                self.assertNotIn(f'<a id="{stale}"></a>', text)

        self.assertIn(
            '<a id="unitsreadmemd--сравнения-юнитов"></a>',
            output,
        )


class TranslationIntegrity(unittest.TestCase):
    def test_hash_ignores_checkout_line_endings(self):
        with tempfile.TemporaryDirectory() as directory:
            lf = Path(directory) / "lf.md"
            crlf = Path(directory) / "crlf.md"
            lf.write_bytes(b"# Title\n\nBody\n")
            crlf.write_bytes(b"# Title\r\n\r\nBody\r\n")
            self.assertEqual(sha256(lf), sha256(crlf))

    def test_protector_rejects_missing_or_duplicated_markers(self):
        protector = Protector([])
        protected = protector.protect("Use `unit.sid` here")
        marker = next(iter(protector.restore))
        with self.assertRaises(RuntimeError):
            protector.unprotect(protected.replace(marker, ""))

        protector = Protector([])
        protected = protector.protect("Use `unit.sid` here")
        marker = next(iter(protector.restore))
        with self.assertRaises(RuntimeError):
            protector.unprotect(protected.replace(marker, marker + marker))

    def test_detects_truncation_and_translation_placeholders(self):
        errors = translation_artifact_errors(
            "Body …5522 tokens truncated… ZXX00037"
        )
        self.assertTrue(any("truncation marker" in error for error in errors))
        self.assertTrue(any("protector artifacts" in error for error in errors))

    def test_detects_malformed_heading(self):
        structure = markdown_structure("# Good\n\n###Broken\n")
        self.assertEqual(structure["malformed_headings"], [3])

    def test_detects_explicit_ids_that_duplicate_natural_heading_ids(self):
        errors = translation_artifact_errors(
            '<a id="details"></a>\n'
            "## Details\n\n"
            "## Details\n"
            '<a id="details-1"></a>\n'
        )
        self.assertTrue(
            any(
                "duplicate natural heading IDs" in error
                and "details" in error
                and "details-1" in error
                for error in errors
            )
        )
        legitimate_alias_errors = translation_artifact_errors(
            '<a id="подробности"></a>\n## Details\n'
        )
        self.assertFalse(
            any(
                "duplicate natural heading IDs" in error
                for error in legitimate_alias_errors
            )
        )
        fenced_example_errors = translation_artifact_errors(
            "```html\n"
            '<a id="details"></a>\n'
            "```\n\n"
            "## Details\n"
        )
        self.assertFalse(
            any(
                "duplicate natural heading IDs" in error
                for error in fenced_example_errors
            )
        )


class ManualFencedTranslations(unittest.TestCase):
    def test_replaces_reviewed_fence_body_and_preserves_delimiters(self):
        source_body = "заголовок\nданные"
        translated = apply_manual_fenced_translations(
            f"Before\n```text\n{source_body}\n```\nAfter\n",
            {
                fenced_block_key(source_body): {
                    "literal": False,
                    "text": "header\ndata",
                }
            },
        )
        self.assertEqual(
            translated,
            "Before\n```text\nheader\ndata\n```\nAfter\n",
        )

    def test_preserves_explicit_literal_game_data(self):
        source_body = "name = Мушкетёр"
        translated = apply_manual_fenced_translations(
            f"```\n{source_body}\n```\n",
            {fenced_block_key(source_body): {"literal": True, "text": None}},
        )
        self.assertIn(source_body, translated)


class ReaderCleanup(unittest.TestCase):
    def test_building_abbreviations_do_not_corrupt_identifiers_or_literals(self):
        source = """Before HP = 10, W = 20, S = 30, G = 40; newW = 50.
`HP = 60`

```text
HP = 70
```
"""
        cleaned = clean_english_building_comparison(source)
        self.assertIn(
            "Before health = 10, wood = 20, stone = 30, gold = 40; newW = 50.",
            cleaned,
        )
        self.assertIn("`HP = 60`", cleaned)
        self.assertIn("HP = 70", cleaned)
        self.assertEqual(clean_english_building_comparison(cleaned), cleaned)

    def test_upgrade_cleanup_uses_a_real_table_header(self):
        source = """| Upgrade | Effect | Value |
|---|---|---:|
| Test | build time % | -7500000 |

| Label | Other |
|---|---|
| Effect | Value |
| untouched | build time % |
"""
        cleaned = clean_english_upgrade_table(source)
        self.assertIn("| Test | Construction time | -75% |", cleaned)
        self.assertIn("| untouched | build time % |", cleaned)
        self.assertEqual(clean_english_upgrade_table(cleaned), cleaned)

    def test_unit_list_cleanup_requires_the_named_header_column(self):
        source = """| Building | Produces |
|---|---|
| Test | cannon, unitbox |

| Label | Other |
|---|---|
| Produces | Units |
| cannon | unitbox |
"""
        cleaned = canonicalize_english_unit_list_column(source, "Produces")
        self.assertIn("Cannon (`cannon`), Mission placeholder (`unitbox`)", cleaned)
        self.assertIn("| cannon | unitbox |", cleaned)
        self.assertEqual(
            canonicalize_english_unit_list_column(cleaned, "Produces"),
            cleaned,
        )

    def test_nation_role_cleanup_does_not_replace_the_unit_column(self):
        source = """| Unit | Role |
|---|---|
| Cannon | Cannon |
| Yacht | Yacht |
"""
        cleaned = clean_english_nation_page(source)
        self.assertIn("| Cannon | Artillery |", cleaned)
        self.assertIn("| Yacht | Warship |", cleaned)
        self.assertEqual(clean_english_nation_page(cleaned), cleaned)

    def test_damage_article_has_one_friendly_fire_section_and_no_artifact_numbers(self):
        paths = (
            ROOT / "docs/recon/world/combat/combat_damage_pipeline.md",
            ROOT / "docs_en/recon/world/combat/combat_damage_pipeline.md",
        )
        expected_titles = ("Дружественный огонь", "Friendly fire")
        for path, expected_title in zip(paths, expected_titles):
            text = path.read_text(encoding="utf-8")
            headings = [
                line.lstrip("#").strip()
                for line in text.splitlines()
                if line.startswith(("### ", "#### "))
            ]
            self.assertEqual(headings.count(expected_title), 1)
            self.assertFalse(
                any(heading and heading[0].isdigit() for heading in headings)
            )

    def test_naval_article_uses_reader_terms_and_not_extractor_status(self):
        ru = (
            ROOT / "docs/recon/world/combat/naval_combat.md"
        ).read_text(encoding="utf-8")
        en = (
            ROOT / "docs_en/recon/world/combat/naval_combat.md"
        ).read_text(encoding="utf-8")
        ru_visible = "\n".join(
            line for line in ru.splitlines()
            if not line.lstrip().startswith("<a id=")
        )
        en_visible = "\n".join(
            line for line in en.splitlines()
            if not line.lstrip().startswith("<a id=")
        )

        self.assertIn("### 6.2. Улучшения", ru)
        self.assertIn("## 9. Морской бой на случайных картах", ru)
        self.assertNotIn("апгрейд", ru_visible.casefold())
        self.assertNotIn("скирмиш", ru_visible.casefold())
        self.assertNotIn("skirmish", en_visible.casefold())
        for stale in ("текущих выгрузок", "текущий парсер"):
            self.assertNotIn(stale, ru.casefold())
        for stale in ("current exported data", "current parser"):
            self.assertNotIn(stale, en.casefold())

    def test_ai_article_uses_improvements_in_visible_russian_text(self):
        text = (
            ROOT / "docs/recon/systems/ai_behavior.md"
        ).read_text(encoding="utf-8")
        visible = "\n".join(
            line for line in text.splitlines()
            if not line.lstrip().startswith("<a id=")
        )
        self.assertNotIn("апгрейд", visible.casefold())
        self.assertIn("#### 2. Лимит улучшений башни", visible)
        self.assertIn("#### 4. Лимит улучшений шахты", visible)

    def test_hunger_article_keeps_open_measurement_in_backlog_only(self):
        ru = (
            ROOT / "docs/recon/world/economy/hunger_and_rebellion.md"
        ).read_text(encoding="utf-8")
        en = (
            ROOT / "docs_en/recon/world/economy/hunger_and_rebellion.md"
        ).read_text(encoding="utf-8")
        for stale in ("не измерен", "контрольное измерение", "незакрытое исследование"):
            self.assertNotIn(stale, ru.casefold())
        for stale in (
            "has not yet been measured",
            "control measurement",
            "open research",
        ):
            self.assertNotIn(stale, en.casefold())

        ru_backlog = (
            ROOT / "internals/project/research_backlog_systems.md"
        ).read_text(encoding="utf-8")
        en_backlog = (
            ROOT / "internals_en/project/research_backlog_systems.md"
        ).read_text(encoding="utf-8")
        self.assertIn("перевод в игровые секунды не измерен", ru_backlog)
        self.assertIn(
            "conversion to game seconds has not been measured",
            en_backlog,
        )


if __name__ == "__main__":
    unittest.main()
