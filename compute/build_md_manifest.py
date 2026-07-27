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

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGETS = {
    "docs": "Энциклопедия Cossacks 3",
    "docs_en": "Cossacks 3 Encyclopedia",
    "internals": "Техническая документация",
    "internals_en": "Technical documentation",
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


def heading_slug(value: str) -> str:
    """Match the GitHub-style heading IDs assigned by ``md-viewer.js``."""

    value = value.strip().lower()
    value = re.sub(r"[^\w\s_-]", "", value, flags=re.UNICODE)
    return value.replace(" ", "-")


def markdown_sections(text: str) -> list[dict[str, str]]:
    """Return searchable article sections with exact heading fragments."""

    explicit_ids = set(
        re.findall(r"<a\s+id=[\"']([^\"']+)[\"']\s*></a>", text)
    )
    used_ids = set(explicit_ids)
    headings: list[tuple[int, str, str, int, int]] = []
    fenced = False
    fence_marker = ""
    offset = 0
    for line in text.splitlines(keepends=True):
        fence_match = re.match(r"^\s*(```+|~~~+)", line)
        if fence_match:
            marker = fence_match.group(1)[0]
            if not fenced:
                fenced = True
                fence_marker = marker
            elif marker == fence_marker:
                fenced = False
            offset += len(line)
            continue
        if not fenced:
            match = re.match(r"^(#{2,6})\s+(.+?)\s*#*\s*(?:\r?\n)?$", line)
            if match:
                level = len(match.group(1))
                title = re.sub(r"\s+#+\s*$", "", match.group(2)).strip()
                base = heading_slug(title)
                if base:
                    fragment = base
                    suffix = 1
                    while fragment in used_ids:
                        fragment = f"{base}-{suffix}"
                        suffix += 1
                    used_ids.add(fragment)
                    headings.append((level, title, fragment, offset, offset + len(line)))
        offset += len(line)

    sections: list[dict[str, str]] = []
    for index, (_, title, fragment, _, content_start) in enumerate(headings):
        end = headings[index + 1][3] if index + 1 < len(headings) else len(text)
        section_text = markdown_search_text(text[content_start:end])
        sections.append({
            "title": markdown_search_text(title),
            "fragment": fragment,
            "text": section_text,
        })
    return sections


def markdown_page_intro(text: str) -> str:
    """Index the lead once; headed sections are indexed independently."""

    match = re.search(r"(?m)^#{2,6}\s+", text)
    lead = text[:match.start()] if match else text
    return markdown_search_text(lead)


def entity_search_entries(root_key: str) -> list[dict]:
    """Add direct entity-card results to the two encyclopedia indexes."""

    if root_key not in {"docs", "docs_en"}:
        return []
    catalog_path = ROOT / "assets" / "data" / "entity-catalog.json"
    if not catalog_path.is_file():
        return []
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    lang = "en" if root_key == "docs_en" else "ru"
    kind_labels = {
        "ru": {
            "unit": "Юнит",
            "building": "Здание",
            "upgrade": "Улучшение",
        },
        "en": {
            "unit": "Unit",
            "building": "Building",
            "upgrade": "Upgrade",
        },
    }
    entries: list[dict] = []
    for kind, values in catalog.get("entities", {}).items():
        for sid, entity in values.items():
            title = entity.get("name", {}).get(lang) or sid
            alternate = entity.get("name", {}).get("ru" if lang == "en" else "en") or ""
            effects = " ".join(
                str(variant.get("effect", {}).get(lang) or "")
                for variant in entity.get("variants", [])
            )
            entries.append({
                "entity": f"{kind}:{sid}",
                "kind": kind,
                "kindLabel": kind_labels[lang][kind],
                "path": "",
                "title": title,
                "text": re.sub(
                    r"\s+",
                    " ",
                    f"{title} {alternate} {sid} {kind_labels[lang][kind]} {effects}",
                ).strip(),
            })
    return entries


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
            "kind": "page",
            "title": heading,
            "text": markdown_page_intro(text),
        })
        for section in markdown_sections(text):
            search_entries.append({
                "path": rel,
                "kind": "section",
                "title": section["title"],
                "fragment": section["fragment"],
                "pageTitle": heading,
                "text": section["text"],
            })
    search_entries.extend(entity_search_entries(root_key))
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
