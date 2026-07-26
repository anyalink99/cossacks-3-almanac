"""Build navigation manifests and full-text indexes for documentation trees.

The viewer in each documentation directory consumes its local manifest to
render a navigable tree and its local search index for client-side search.

Outputs:
    docs/_manifest.json
    docs/_search.json
    docs_en/_manifest.json
    docs_en/_search.json
    internals/_manifest.json
    internals/_search.json
    internals_en/_manifest.json
    internals_en/_search.json

Each manifest has shape:
    {
      "root": "docs",
      "title": "Документация",
      "entries": [
         { "path": "README.md", "title": "Cossacks 3 Almanac",
           "size": 1234, "lines": 64 },
         ...
      ]
    }

Run: `python compute/build_md_manifest.py`
"""
from __future__ import annotations

import json
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGETS = {
    "docs": "Документация",
    "docs_en": "Documentation",
    "internals": "Internals (engine recon)",
    "internals_en": "Internals (engine recon)",
}


def first_heading(text: str) -> str | None:
    """Return the first markdown level-1 heading, stripped."""
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip().rstrip("·–—-").strip()
    return None


def markdown_search_text(text: str) -> str:
    """Flatten Markdown into compact, readable text for search snippets."""
    text = re.sub(r"<a\s+id=[\"'][^\"']*[\"']\s*></a>", " ", text)
    text = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"^\s*(```|~~~)[^\n]*$", " ", text, flags=re.MULTILINE)
    text = text.replace("`", "")
    text = re.sub(r"^\s{0,3}#{1,6}\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*[-*+]\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*\d+[.)]\s+", "", text, flags=re.MULTILINE)
    text = text.replace("|", " ")
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def build_catalogs(root_dir: Path, root_key: str, title: str) -> tuple[dict, dict]:
    entries = []
    search_entries = []
    for md in sorted(root_dir.rglob("*.md")):
        rel = md.relative_to(root_dir).as_posix()
        try:
            text = md.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = md.read_text(encoding="cp1251", errors="replace")
        lines = text.count("\n") + 1
        heading = first_heading(text) or rel.rsplit("/", 1)[-1].removesuffix(".md")
        entries.append({
            "path": rel,
            "title": heading,
            "size": md.stat().st_size,
            "lines": lines,
        })
        search_entries.append({
            "path": rel,
            "title": heading,
            "text": markdown_search_text(text),
        })
    manifest = {
        "root": root_key,
        "title": title,
        "entries": entries,
    }
    search_index = {
        "root": root_key,
        "entries": search_entries,
    }
    return manifest, search_index


def main() -> None:
    for key, title in TARGETS.items():
        src = ROOT / key
        if not src.is_dir():
            print(f"skip {key}: not a directory", file=sys.stderr)
            continue
        manifest, search_index = build_catalogs(src, key, title)
        manifest_out = src / "_manifest.json"
        manifest_out.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        search_out = src / "_search.json"
        search_out.write_text(
            json.dumps(
                search_index,
                ensure_ascii=False,
                separators=(",", ":"),
            ) + "\n",
            encoding="utf-8",
        )
        print(
            f"wrote {manifest_out.relative_to(ROOT)} and "
            f"{search_out.relative_to(ROOT)}: {len(manifest['entries'])} files"
        )


if __name__ == "__main__":
    main()
