"""Validate relative file links and anchors in published Markdown.

The writer templates are intentionally excluded: their links are relative to
the generated destination under ``docs/reference/``, not to the template file.
External URLs are outside this check's scope.
"""
from __future__ import annotations

import argparse
import html
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
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
EXPLICIT_ID_LINE_RE = re.compile(
    r"\s*<(?:a|span)\s+[^>]*\bid=(?P<quote>[\"'])"
    r"(?P<id>[^\"']+)(?P=quote)[^>]*>\s*"
    r"</(?:a|span)>\s*",
    re.IGNORECASE,
)
EXTERNAL_PREFIXES = ("http://", "https://", "mailto:", "data:")


def published_markdown() -> list[Path]:
    files = [path for path in ROOT_MARKDOWN if path.is_file()]
    for root in PUBLISHED_ROOTS:
        if root.is_dir():
            files.extend(root.rglob("*.md"))
    return sorted(files)


def link_destination(raw: str) -> tuple[str, str]:
    """Return the decoded path and fragment of a Markdown destination.

    Destinations may be wrapped in ``<>`` and may have an optional quoted
    title after whitespace. Paths in this repository contain no literal
    parentheses, so the deliberately small parser is sufficient here.
    """
    value = raw.strip()
    if value.startswith("<") and ">" in value:
        value = value[1:value.index(">")]
    elif " \"" in value:
        value = value.split(" \"", 1)[0]
    path, separator, fragment = value.partition("#")
    return unquote(path.strip()), unquote(fragment.strip()) if separator else ""


def heading_slug(value: str) -> str:
    """Match ``headingSlug`` in ``assets/js/md-viewer.js``."""

    protected_code: dict[str, str] = {}

    def preserve_code(match: re.Match[str]) -> str:
        marker = f"\x00CODE{len(protected_code)}\x00"
        protected_code[marker] = match.group(1)
        return marker

    value = re.sub(r"`([^`\n]+)`", preserve_code, value)
    value = re.sub(r"!\[([^\]]*)]\([^)]+\)", r"\1", value)
    value = re.sub(r"\[([^\]]+)]\([^)]+\)", r"\1", value)
    value = re.sub(r"<[^>]+>", "", value)
    value = re.sub(r"(\*\*|__)(?=\S)(.+?)(?<=\S)\1", r"\2", value)
    value = re.sub(
        r"(?<![\w\\])([*_])(?=\S)(.+?)(?<=\S)\1(?!\w)",
        r"\2",
        value,
    )
    value = re.sub(r"~~(?=\S)(.+?)(?<=\S)~~", r"\1", value)
    for marker, code_text in protected_code.items():
        value = value.replace(marker, code_text)
    value = html.unescape(value).strip().lower()
    value = re.sub(r"[^\w\s-]", "", value, flags=re.UNICODE)
    return re.sub(r"\s", "-", value)


def document_ids(path: Path) -> set[str]:
    """Return IDs available after the Markdown reader renders a document."""
    text = path.read_text(encoding="utf-8")
    ids: set[str] = set()
    in_fence = False
    for line in text.splitlines():
        if re.match(r"^\s*(```|~~~)", line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        explicit_match = EXPLICIT_ID_LINE_RE.fullmatch(line)
        if explicit_match:
            ids.add(explicit_match.group("id"))
            continue
        match = HEADING_RE.match(line)
        if not match:
            continue
        base = heading_slug(match.group(2))
        if not base:
            continue
        candidate = base
        suffix = 1
        while candidate in ids:
            candidate = f"{base}-{suffix}"
            suffix += 1
        ids.add(candidate)
    return ids


def broken_links() -> list[tuple[Path, int, str]]:
    broken: list[tuple[Path, int, str]] = []
    ids_by_path: dict[Path, set[str]] = {}
    for source in published_markdown():
        text = source.read_text(encoding="utf-8")
        for line_no, line in enumerate(text.splitlines(), 1):
            for match in LINK_RE.finditer(line):
                target, fragment = link_destination(match.group(1))
                if target.lower().startswith(EXTERNAL_PREFIXES):
                    continue
                # Absolute local paths are never portable published links.
                if Path(target).is_absolute() or re.match(r"^[A-Za-z]:[/\\]", target):
                    broken.append((source, line_no, target))
                    continue
                resolved = (source.parent / target).resolve() if target else source.resolve()
                if not resolved.exists():
                    broken.append((source, line_no, target))
                    continue
                if fragment and resolved.is_file() and resolved.suffix.lower() == ".md":
                    ids = ids_by_path.setdefault(resolved, document_ids(resolved))
                    if fragment not in ids:
                        destination = f"{target}#{fragment}" if target else f"#{fragment}"
                        broken.append((source, line_no, destination))
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
