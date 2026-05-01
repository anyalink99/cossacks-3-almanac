"""Build the tech-dependency graph from `data.json`.

Output: `derived/tech_tree.json` — structured graph for downstream
consumers (browser editor, simulator, `compute/compute_tech_tree.py`).

Graph extracted from:
- building.prereqs   (built buildings/upgrades required to construct)
- unit.prereqs       (usually "the producing building is ready")
- unit.trained_in    (which building trains the unit)
- upgrade.prereqs    (other upgrades / buildings / era)

Run after `parser/build_data.py`:
    python parser/build_tech_graph.py
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import DATA_JSON, DERIVED_DIR

TREE_JSON = DERIVED_DIR / "tech_tree.json"


def build_index(data: dict) -> dict:
    """Lookup tables for building / unit / upgrade by (sid, nation)."""
    bld = {(b["sid"], b["nation"]): b for b in data["buildings"]}
    unt = {(u["sid"], u["nation"]): u for u in data["units"]}
    upg = {(u["sid"], u["nation"]): u for u in data["upgrades"]}
    return {"buildings": bld, "units": unt, "upgrades": upg}


def kind_of(sid: str, nat: str, idx: dict) -> str | None:
    if (sid, nat) in idx["buildings"]:
        return "building"
    if (sid, nat) in idx["units"]:
        return "unit"
    if (sid, nat) in idx["upgrades"]:
        return "upgrade"
    return None


def _resolve_prereqs(prereqs: list[str], nat: str, idx: dict) -> list[dict]:
    """Map raw prereq sids to {kind, sid, note} entries; filter out junk."""
    out: list[dict] = []
    seen: set[tuple[str, str]] = set()
    for r in prereqs:
        if not r or r.startswith("'") or "+" in r or r in ("req0", "req1", "century18"):
            # 'century18' is a magic alias for csid+'cen.1' that the simulator
            # didn't resolve. Substitute with '<nat>cen.1' explicitly.
            if r == "century18":
                resolved = nat + "cen.1"
                kind = kind_of(resolved, nat, idx) or "upgrade"
                if (kind, resolved) in seen:
                    continue
                seen.add((kind, resolved))
                out.append({"kind": kind, "sid": resolved, "note": "century18 → cen.1 upgrade"})
            continue
        kind = kind_of(r, nat, idx)
        if kind is None:
            # Could be a common-cluster sid (e.g. eurmil/eurpor) for a non-eur
            # nation — try direct lookup ignoring nation.
            for n in [nat, "eur", "rus", "tur", "spa", "ukr", "por"]:
                if (r, n) in idx["buildings"]:
                    kind = "building"
                    break
                if (r, n) in idx["units"]:
                    kind = "unit"
                    break
                if (r, n) in idx["upgrades"]:
                    kind = "upgrade"
                    break
        if kind is None:
            # unknown — synthetic alias or unresolved variable; skip
            continue
        if (kind, r) in seen:
            continue
        seen.add((kind, r))
        out.append({"kind": kind, "sid": r, "note": ""})
    return out


def build_tree(data: dict) -> dict:
    """{nations: {<nat>: {buildings, units, upgrades}}} — each entry is a
    flat dict from sid to its stats + resolved prereqs."""
    idx = build_index(data)
    nations = sorted(set(b["nation"] for b in data["buildings"]))
    tree: dict = {"nations": {}}
    for nat in nations:
        nat_tree = {"buildings": {}, "units": {}, "upgrades": {}}
        for b in data["buildings"]:
            if b["nation"] != nat:
                continue
            nat_tree["buildings"][b["sid"]] = {
                "name_en": b.get("name_en"),
                "name_ru": b.get("name_ru"),
                "kind": b.get("kind"),
                "buildtime_sec": b.get("buildtime_sec"),
                "cost": {k: b.get(k) or 0 for k in ("food", "wood", "stone", "gold", "iron", "coal")},
                "hp": b.get("hp"),
                "farm": b.get("farm"),
                "produces": b.get("produces") or [],
                "prereqs": _resolve_prereqs(b.get("prereqs") or [], nat, idx),
                "costpercent": b.get("costpercent"),
            }
        for u in data["units"]:
            if u["nation"] != nat:
                continue
            nat_tree["units"][u["sid"]] = {
                "name_en": u.get("name_en"),
                "name_ru": u.get("name_ru"),
                "buildtime_sec": u.get("buildtime_sec"),
                "cost": {k: u.get(k) or 0 for k in ("food", "wood", "stone", "gold", "iron", "coal")},
                "hp": u.get("hp"),
                "trained_in": u.get("trained_in") or [],
                "prereqs": _resolve_prereqs(u.get("prereqs") or [], nat, idx),
            }
        for ug in data["upgrades"]:
            if ug["nation"] != nat:
                continue
            nat_tree["upgrades"][ug["sid"]] = {
                "name_en": ug.get("name_en"),
                "name_ru": ug.get("name_ru"),
                "itype": ug.get("itype"),
                "value": ug.get("value"),
                "time_sec": ug.get("time_sec"),
                "cost": {k: ug.get(k) or 0 for k in ("food", "wood", "stone", "gold", "iron", "coal")},
                "place": ug.get("place"),
                "prereqs": _resolve_prereqs(ug.get("prereqs") or [], nat, idx),
            }
        tree["nations"][nat] = nat_tree
    return tree


def main() -> None:
    data = json.loads(DATA_JSON.read_text(encoding="utf-8"))
    DERIVED_DIR.mkdir(parents=True, exist_ok=True)
    print("Building tech tree…")
    tree = build_tree(data)
    TREE_JSON.write_text(json.dumps(tree, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {TREE_JSON} ({TREE_JSON.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
