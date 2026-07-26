import tempfile
import unittest
from pathlib import Path

from compute.build_md_manifest import markdown_search_text
from scripts.build_english_docs import (
    Protector,
    apply_manual_fenced_translations,
    ensure_heading_aliases,
    fenced_block_key,
    markdown_structure,
    sha256,
    translation_artifact_errors,
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


if __name__ == "__main__":
    unittest.main()
