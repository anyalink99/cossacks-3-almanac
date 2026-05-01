"""Build comprehensive canonical_terms.json from game locale.

Reads `data/locale/{ru,en}/*.txt` from the game install (CP1251), resolves
`%include(...)%`, `%nat%`, `%com%`, style markers, and emits
`derived/canonical_terms.json` — the single source of truth for Russian
display names used by writers, compute scripts, and prose docs.

Run after game patch:
    python parser/build_canonical_terms.py
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import LOCALE, PLAYABLE_NATIONS, NATION_TO_COMMON_CLUSTER, DERIVED_DIR

INCLUDE_RE = re.compile(r"%include\(([^;]+);([^)]+)\)%")
STYLE_RE = re.compile(r"%(def|pos|neg|val)%")
ANY_PCT_RE = re.compile(r"%[^%]+%")
KEY_RE = re.compile(r"^\t@(\S+)\s*$")


def parse_locale_file(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        text = raw.decode("cp1251", errors="replace")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    out: dict[str, str] = {}
    cur_key: str | None = None
    cur_val: list[str] = []
    for line in text.split("\n"):
        m = KEY_RE.match(line)
        if m:
            if cur_key is not None:
                out[cur_key] = "\n".join(cur_val).rstrip()
            cur_key = m.group(1)
            cur_val = []
        else:
            if cur_key is not None:
                cur_val.append(line)
    if cur_key is not None:
        out[cur_key] = "\n".join(cur_val).rstrip()
    return out


def load_lang(lang: str) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    base = LOCALE / lang
    for fname in ("gui.txt", "units.txt", "upgrades.txt", "misc.txt", "new.txt", "tools.txt", "style.txt"):
        out[fname.replace(".txt", "")] = parse_locale_file(base / fname)
    return out


def resolve(loc: dict[str, dict[str, str]], fname: str, key: str, depth: int = 0) -> str | None:
    if depth > 8:
        return None
    d = loc.get(fname)
    if not d:
        return None
    raw = d.get(key)
    if raw is None:
        return None

    def repl(m: re.Match) -> str:
        sub_f = m.group(1).strip()
        sub_k = m.group(2).strip()
        v = resolve(loc, sub_f, sub_k, depth + 1)
        return v if v is not None else m.group(0)

    return INCLUDE_RE.sub(repl, raw)


def clean(s: str | None) -> str:
    if not s:
        return ""
    s = STYLE_RE.sub("", s)
    s = ANY_PCT_RE.sub("", s)
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\(\s*$", "", s).strip()
    return s


def build() -> dict:
    ru = load_lang("ru")
    en = load_lang("en")

    canon: dict = {
        "_meta": {
            "source": "Cossacks 3 game files (data/locale/{ru,en}/*.txt)",
            "note": "Generated from game locale; do not edit by hand. Regenerate via "
                    "`python parser/build_canonical_terms.py`.",
        }
    }

    canon["nations"] = {
        n: {"ru": ru["units"].get(n, "?"), "en": en["units"].get(n, "?")}
        for n in PLAYABLE_NATIONS
    }

    canon["settings"] = {}
    for k in sorted(ru["gui"]):
        if k.startswith("randommap.") or k == "customgame.text.nation":
            canon["settings"][k] = {"ru": ru["gui"][k], "en": en["gui"].get(k, "")}

    canon["difficulty"] = {
        k: {"ru": ru["gui"][k], "en": en["gui"].get(k, "")}
        for k in sorted(ru["gui"]) if k.startswith("difficulty.")
    }

    BUILDING_KEYS = [
        ("cen", "nat"), ("bar", "nat"), ("ba2", "nat"), ("aca", "nat"),
        ("art", "nat"), ("bla", "nat"), ("dip", "nat"), ("hou", "nat"),
        ("sta", "nat"), ("tem", "nat"),
        ("mar", "com"), ("mil", "com"), ("por", "com"), ("sto", "com"),
        ("tow", "com"), ("coa", "com"), ("gol", "com"), ("iro", "com"),
        ("sga", "com"), ("wga", "com"), ("swa", "com"), ("wwa", "com"),
    ]
    canon["buildings"] = {}
    for sid, kind in BUILDING_KEYS:
        pref = "%nat%" if kind == "nat" else "%com%"
        ru_v = ru["units"].get(pref + sid, "")
        en_v = en["units"].get(pref + sid, "")
        canon["buildings"][sid] = {
            "kind": kind,
            "template_key": pref + sid,
            "ru": clean(ru_v),
            "en": clean(en_v),
        }

    RES_KEYS = {
        "food":  "restype.1",
        "wood":  "restype.2",
        "stone": "restype.3",
        "gold":  "restype.4",
        "iron":  "restype.5",
        "coal":  "restype.6",
    }
    canon["resources"] = {}
    for res, k in RES_KEYS.items():
        ru_v = ""
        en_v = ""
        for fname in ("misc", "new", "units", "gui", "tools"):
            if not ru_v and ru.get(fname, {}).get(k):
                ru_v = ru[fname][k]
            if not en_v and en.get(fname, {}).get(k):
                en_v = en[fname][k]
        canon["resources"][res] = {"ru": clean(ru_v), "en": clean(en_v)}

    weapon_idx_to_kind = {0: "sword", 1: "pike", 2: "bullet", 3: "arrow",
                          4: "cannonball", 5: "cannister", 6: "firearrow"}
    canon["weapon_kinds"] = {}
    for idx, kind in weapon_idx_to_kind.items():
        k = f"unitpanel.hint.damage.weaponkind.{idx}"
        canon["weapon_kinds"][kind] = {
            "index": idx,
            "gc_id": f"gc_obj_weapon_kind_{kind}",
            "ru": ru["gui"].get(k, ""),
            "en": en["gui"].get(k, ""),
        }

    canon["upgrade_names"] = {}
    for k in sorted(ru["upgrades"]):
        if k.startswith("tooltiptype."):
            continue
        canon["upgrade_names"][k] = {
            "ru": clean(resolve(ru, "upgrades", k))[:160],
            "en": clean(resolve(en, "upgrades", k))[:160],
        }

    canon["tooltip_types"] = {}
    for k in sorted(ru["upgrades"]):
        if not k.startswith("tooltiptype."):
            continue
        canon["tooltip_types"][k] = {
            "ru": clean(resolve(ru, "upgrades", k))[:160],
            "en": clean(resolve(en, "upgrades", k))[:160],
        }

    canon["units"] = {}
    SKIP_PREFIX = ("descr.", "UNITS", "BUILDINGS", "UPGRADES", "NATIONS", "ARTILLERY", "%")
    for k, v in ru["units"].items():
        if any(k.startswith(p) for p in SKIP_PREFIX):
            continue
        if k in PLAYABLE_NATIONS:
            continue
        if k.endswith(".ext") or k.endswith(".alternative"):
            continue
        if not v or v.startswith("*") or v.startswith("@"):
            continue
        ru_c = clean(resolve(ru, "units", k) or v)
        if not ru_c or len(ru_c) > 80:
            continue
        en_c = clean(resolve(en, "units", k) or en["units"].get(k, ""))
        canon["units"][k] = {"ru": ru_c, "en": en_c}

    return canon


def main() -> None:
    DERIVED_DIR.mkdir(parents=True, exist_ok=True)
    out_path = DERIVED_DIR / "canonical_terms.json"
    canon = build()
    out_path.write_text(json.dumps(canon, ensure_ascii=False, indent=2), encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    print(f"saved -> {out_path}")
    for cat in ("nations", "settings", "difficulty", "buildings", "resources",
                "weapon_kinds", "upgrade_names", "tooltip_types", "units"):
        print(f"  {cat}: {len(canon[cat])}")


if __name__ == "__main__":
    main()
