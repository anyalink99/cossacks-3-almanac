"""Parse Cossacks 3 locale files (units.txt, upgrades.txt, gui.txt).

Format:
    \t@<key>
    <line 1 of value>
    <line 2 ...>      (until next \t@<key> or EOF)
    \t@<next key>
    ...

Templates: %nat%, %com%, %include(file;key)%, %farm%, %def%/%pos%/%neg% (style),
%val% etc. We resolve %nat% and %com% by expansion against nation list,
and resolve %include(...)% recursively (max depth).
"""
from __future__ import annotations
import re
from pathlib import Path
from collections import OrderedDict


KEY_RE = re.compile(r"^\t@(.+?)\s*$")
INCLUDE_RE = re.compile(r"%include\(([^;]+);([^)]+)\)%")
STYLE_RE = re.compile(r"%(def|pos|neg|val)%")
WHITESPACE_RUN_RE = re.compile(r"\s+")


def _normalize_label(s: str) -> str:
    """Collapse all whitespace runs to a single space and strip ends.

    Locale templates frequently introduce double spaces after `%include(...)%`
    expansion, because both the parent string and the included fragment carry
    a separator space. Run this on every value that ends up as user-facing
    text (unit / building / upgrade names).
    """
    return WHITESPACE_RUN_RE.sub(" ", s).strip()


def parse_locale_file(path: Path, encoding: str | None = None) -> "OrderedDict[str, str]":
    """Return {key: raw_value} preserving order. Raw value can contain templates."""
    result: "OrderedDict[str, str]" = OrderedDict()
    if not path.exists():
        return result
    if encoding is None:
        # Try utf-8 first; fall back to cp1251 (used by Russian/Ukrainian/Polish locale)
        raw = path.read_bytes()
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            text = raw.decode("cp1251", errors="replace")
    else:
        text = path.read_text(encoding=encoding, errors="replace")
    current_key: str | None = None
    current_value: list[str] = []

    def flush():
        nonlocal current_key, current_value
        if current_key is not None:
            value = "\n".join(current_value).rstrip()
            result[current_key] = value
        current_key = None
        current_value = []

    for raw_line in text.splitlines():
        m = KEY_RE.match(raw_line)
        if m:
            flush()
            current_key = m.group(1).strip()
        else:
            if current_key is not None:
                current_value.append(raw_line)
    flush()
    return result


class LocaleResolver:
    """Resolve %nat%, %com%, %include(...)% templates."""

    def __init__(self, files: dict[str, "OrderedDict[str, str]"]):
        # files: {filename_no_ext: {key: value}}; e.g., 'units' -> dict
        self.files = files

    def get(self, filename: str, key: str, *, depth: int = 0) -> str | None:
        if depth > 8:
            return f"<INCLUDE_DEPTH:{key}>"
        d = self.files.get(filename)
        if not d:
            return None
        raw = d.get(key)
        if raw is None:
            return None
        # Resolve %include(file;key)%
        def repl_inc(m):
            sub_file = m.group(1).strip()
            sub_key = m.group(2).strip()
            v = self.get(sub_file, sub_key, depth=depth + 1)
            return v if v is not None else m.group(0)
        return INCLUDE_RE.sub(repl_inc, raw)

    def resolve_for_nation(self, filename: str, key_template: str,
                           nat: str, com: str, farm: int | None = None) -> str | None:
        """Substitute %nat%, %com%, %farm% then look up the key, then resolve includes.

        key_template may itself contain %nat% / %com% (e.g. '%nat%aca' -> 'auscen').
        """
        key = key_template.replace("%nat%", nat).replace("%com%", com)
        raw = self.get(filename, key)
        if raw is None:
            return None
        if farm is not None:
            raw = raw.replace("%farm%", str(farm))
        # Replace style markers with empty (display only)
        raw = STYLE_RE.sub("", raw)
        return raw

    def lookup_unit_name(self, sid: str, nat: str | None = None,
                         com: str | None = None) -> str | None:
        """Look up the display name for a unit/building sid. Tries direct key first,
        then per-nation/per-cluster templates if nat/com given.

        After include-resolution, locale templates can leave double spaces (the
        included fragment has a leading space, plus a separator space already in
        the parent — e.g., `archerdip = "Лучник %include(units;descr.ability.
        mercenary)%"` + `descr.ability.mercenary = " (наемник)"`). Collapse
        runs of whitespace to a single space.
        """
        # First, try direct
        v = self.get("units", sid)
        if v is not None:
            return _normalize_label(STYLE_RE.sub("", v.split("\n", 1)[0]))
        # Try template form
        if nat is not None and sid.startswith(nat):
            tail = sid[len(nat):]
            v = self.get("units", "%nat%" + tail)
            if v is not None:
                v = v.split("\n", 1)[0]
                return _normalize_label(STYLE_RE.sub("", v.replace("%nat%", nat)))
        if com is not None and sid.startswith(com):
            tail = sid[len(com):]
            v = self.get("units", "%com%" + tail)
            if v is not None:
                v = v.split("\n", 1)[0]
                return _normalize_label(STYLE_RE.sub("", v.replace("%com%", com)))
        return None


def load_all(locale_dir: Path, lang: str = "en") -> LocaleResolver:
    base = locale_dir / lang
    # Russian/Ukrainian/etc. files are in CP1251; English/Spanish/etc. in UTF-8 (or
    # close-enough Latin-1). Auto-detect.
    enc = None
    if lang in ("ru", "uk", "pl", "cs", "tu"):
        enc = "cp1251"
    files = {
        "units":    parse_locale_file(base / "units.txt", enc),
        "upgrades": parse_locale_file(base / "upgrades.txt", enc),
        "gui":      parse_locale_file(base / "gui.txt", enc),
        "tools":    parse_locale_file(base / "tools.txt", enc),
        "style":    parse_locale_file(base / "style.txt", enc),
    }
    return LocaleResolver(files)


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    from config import LOCALE, PLAYABLE_NATIONS, NATION_TO_COMMON_CLUSTER
    res = load_all(LOCALE, "en")
    print(f"units.txt keys: {len(res.files['units'])}")
    print(f"upgrades.txt keys: {len(res.files['upgrades'])}")
    print("\nSample nations:")
    for n in PLAYABLE_NATIONS[:5]:
        print(f"  {n}: {res.get('units', n)!r}")
    print("\nSample buildings:")
    for nat in ["aus", "rus", "tur", "spa", "ukr", "por"]:
        com = NATION_TO_COMMON_CLUSTER[nat]
        print(f"  {nat} (com={com}):")
        print(f"    cen     -> {res.lookup_unit_name(nat + 'cen', nat=nat, com=com)!r}")
        print(f"    bar     -> {res.lookup_unit_name(nat + 'bar', nat=nat, com=com)!r}")
        print(f"    {com}mil -> {res.lookup_unit_name(com + 'mil', nat=nat, com=com)!r}")
        print(f"    {com}por -> {res.lookup_unit_name(com + 'por', nat=nat, com=com)!r}")
    print("\nSample units:")
    for sid in ["pikeman", "pikemanpol", "pikemanrus", "musketeerspa", "strelet", "jannisary", "peaaus"]:
        print(f"  {sid} -> {res.lookup_unit_name(sid)!r}")
