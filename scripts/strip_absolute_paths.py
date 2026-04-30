"""Replace markdown links with absolute Windows paths to the game install
with plain text. These links don't resolve on GitHub or any machine that
doesn't have Cossacks 3 installed at exactly the expected location.

Pattern: `[text](C:/Program Files (x86)/Steam/...)` → `text`
        `[text](<C:/Program Files (x86)/Steam/...>)` → `text`
        `[text](file:///C:/Program Files (x86)/Steam/...)` → `text`

Run from repo root: `python scripts/strip_absolute_paths.py [--dry-run]`
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGETS = [ROOT / "docs", ROOT / "writers" / "templates"]
EXTENSIONS = {".md"}

# Match [text](optional<>file:///?C:/Program{ |%20}Files{ |%20}(x86)/Steam/...optional#L...optional>)
# `Program Files (x86)` may appear with literal spaces OR URL-encoded %20.
LINK_RE = re.compile(
    r"\[([^\]]+)\]\("
    r"<?(?:file:///)?C:/Program(?:\s|%20)+Files(?:\s|%20)+\(x86\)/Steam/steamapps/common/Cossacks(?:\s|%20)+3/"
    r"[^)]*?>?\)"
)


def process_file(path: Path, dry_run: bool) -> int:
    raw = path.read_text(encoding="utf-8")
    new, n = LINK_RE.subn(r"\1", raw)
    if n and not dry_run:
        path.write_text(new, encoding="utf-8")
    return n


def main() -> None:
    dry = "--dry-run" in sys.argv
    total_files = 0
    total_subs = 0
    for target in TARGETS:
        for path in target.rglob("*"):
            if path.suffix not in EXTENSIONS:
                continue
            n = process_file(path, dry)
            if n:
                rel = path.relative_to(ROOT)
                print(f"{rel}: {n} replacement{'s' if n != 1 else ''}")
                total_files += 1
                total_subs += n
    verb = "would change" if dry else "changed"
    print(f"\n{verb} {total_subs} link(s) across {total_files} file(s)")


if __name__ == "__main__":
    main()
