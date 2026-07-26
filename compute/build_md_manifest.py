"""Build manifest JSON files listing every translated documentation tree.

The viewer in each documentation directory consumes its local manifest to
render a navigable tree.

Outputs:
    docs/_manifest.json
    docs_en/_manifest.json
    internals/_manifest.json
    internals_en/_manifest.json

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


def build_manifest(root_dir: Path, root_key: str, title: str) -> dict:
    entries = []
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
    return {
        "root": root_key,
        "title": title,
        "entries": entries,
    }


def main() -> None:
    for key, title in TARGETS.items():
        src = ROOT / key
        if not src.is_dir():
            print(f"skip {key}: not a directory", file=sys.stderr)
            continue
        manifest = build_manifest(src, key, title)
        out = src / "_manifest.json"
        out.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"wrote {out.relative_to(ROOT)}: {len(manifest['entries'])} files")


if __name__ == "__main__":
    main()
