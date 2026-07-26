"""Validate relative file links in the repository's published Markdown.

The writer templates are intentionally excluded: their links are relative to
the generated destination under ``docs/reference/``, not to the template file.
External URLs and same-document anchors are outside this check's scope.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parent.parent
PUBLISHED_ROOTS = (
    ROOT / "docs",
    ROOT / "docs_en",
    ROOT / "internals",
    ROOT / "internals_en",
)
ROOT_MARKDOWN = (
    ROOT / "README.md",
    ROOT / "README.en.md",
    ROOT / "CONTRIBUTING.md",
    ROOT / "CONTRIBUTING.en.md",
)

# Inline Markdown links. Image links are harmless to validate with the same
# rules, so the optional leading ``!`` is deliberately outside the capture.
LINK_RE = re.compile(r"!?\[[^\]]*]\(([^)]+)\)")
EXTERNAL_PREFIXES = ("http://", "https://", "mailto:", "data:")


def published_markdown() -> list[Path]:
    files = [path for path in ROOT_MARKDOWN if path.is_file()]
    for root in PUBLISHED_ROOTS:
        if root.is_dir():
            files.extend(root.rglob("*.md"))
    return sorted(files)


def link_target(raw: str) -> str:
    """Return the path part of a Markdown destination.

    Destinations may be wrapped in ``<>`` and may have an optional quoted
    title after whitespace. Paths in this repository contain no literal
    parentheses, so the deliberately small parser is sufficient here.
    """
    value = raw.strip()
    if value.startswith("<") and ">" in value:
        value = value[1:value.index(">")]
    elif " \"" in value:
        value = value.split(" \"", 1)[0]
    return unquote(value.split("#", 1)[0].strip())


def broken_links() -> list[tuple[Path, int, str]]:
    broken: list[tuple[Path, int, str]] = []
    for source in published_markdown():
        text = source.read_text(encoding="utf-8")
        for line_no, line in enumerate(text.splitlines(), 1):
            for match in LINK_RE.finditer(line):
                target = link_target(match.group(1))
                if not target or target.lower().startswith(EXTERNAL_PREFIXES):
                    continue
                # Absolute local paths are never portable published links.
                if Path(target).is_absolute() or re.match(r"^[A-Za-z]:[/\\]", target):
                    broken.append((source, line_no, target))
                    continue
                resolved = (source.parent / target).resolve()
                if not resolved.exists():
                    broken.append((source, line_no, target))
    return broken


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="only return a non-zero exit code when broken links are found",
    )
    args = parser.parse_args()

    broken = broken_links()
    if broken and not args.quiet:
        for source, line_no, target in broken:
            print(f"{source.relative_to(ROOT)}:{line_no}: {target}")
        print(f"\n{len(broken)} broken relative link(s)")
    elif not args.quiet:
        print(f"Markdown links OK ({len(published_markdown())} files)")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
