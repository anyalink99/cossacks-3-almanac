"""Catch RU/EN keyboard typos that produce visually-plausible garbage.

Cyrillic `а о е с р у х` look identical to Latin `a o e c p y x`, so a
slip of the keyboard layout produces words like `Glоballоe`, `reпейр`,
`саkmpы` that pass spell-check (they're not real words in either
language) but render as nonsense to a reader.

This test fails on any word in `docs/` that mixes the two alphabets.
"""
from __future__ import annotations
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCAN_DIRS = [ROOT / "docs", ROOT / "writers" / "templates"]
EXTENSIONS = {".md"}

WORD_RE = re.compile(r"[A-Za-zА-Яа-яЁё]{3,}")

# Code blocks contain script identifiers like `gc_obj_speed_peasant` plus
# nation prefixes — those are intentionally part-Cyrillic, part-Latin in
# documentation cells (`peapol`, `auscen`, etc., which are Latin-only —
# but in surrounding prose, headers like `## ALG — Алжир (Algeria)` are
# fine because spaces / dashes break the words apart).
# We only flag words *inside* a single contiguous letter sequence that
# mix alphabets.

# Skip files that are explicitly test fixtures (we have none right now,
# but reserve the option).
SKIP = set()


def has_mixed_alphabet(word: str) -> bool:
    has_lat = any("a" <= c.lower() <= "z" for c in word)
    has_cyr = any("а" <= c.lower() <= "я" or c in "Ёё" for c in word)
    return has_lat and has_cyr


class NoMixedAlphabet(unittest.TestCase):
    """Run as: python -m unittest tests.test_no_mixed_alphabet"""

    def test_no_mixed_alphabet_words(self) -> None:
        bad: list[tuple[Path, int, str]] = []
        for root in SCAN_DIRS:
            if not root.exists():
                continue
            for path in root.rglob("*"):
                if path.suffix not in EXTENSIONS or path in SKIP:
                    continue
                text = path.read_text(encoding="utf-8")
                # English mirrors retain source-language heading slugs as
                # hidden compatibility anchors. A slug such as `writerов`
                # must stay byte-for-byte compatible with old links and is
                # not reader-visible prose.
                visible_text = re.sub(
                    r'<a\s+id="[^"]*"\s*></a>',
                    lambda match: " " * len(match.group(0)),
                    text,
                )
                for m in WORD_RE.finditer(visible_text):
                    w = m.group(0)
                    if has_mixed_alphabet(w):
                        line_no = text.count("\n", 0, m.start()) + 1
                        bad.append((path.relative_to(ROOT), line_no, w))
        self.assertEqual(
            bad, [],
            "Found words mixing Cyrillic and Latin letters (likely RU/EN "
            "keyboard typos). Examples:\n  " + "\n  ".join(
                f"{p}:{ln}  {w!r}" for p, ln, w in bad[:20]
            ),
        )


if __name__ == "__main__":
    unittest.main()
