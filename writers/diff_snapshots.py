"""Diff two cossacks3_data.json snapshots — useful after a game patch.

Usage:
    python diff_snapshots.py <old.json> <new.json> [--out diff.md]

Output: a markdown report showing what changed between snapshots:
- Constants that changed value
- Buildings/units added/removed
- Stat changes per (sid, nation) — HP, costs, weapon damage, etc.
- New/removed upgrades
- Sanity check delta (newly failing checks)
"""
from __future__ import annotations
import sys, json, argparse
sys.stdout.reconfigure(encoding="utf-8")
from pathlib import Path
from collections import defaultdict


def index_by_keys(rows: list[dict], keys: tuple) -> dict[tuple, dict]:
    """Index list of dicts by tuple of values from keys."""
    out = {}
    for r in rows:
        k = tuple(r.get(kk) for kk in keys)
        out[k] = r
    return out


def diff_dicts(old: dict, new: dict, ignore_keys: set = None) -> dict:
    """Return {field: (old_value, new_value)} for fields that differ."""
    ignore_keys = ignore_keys or set()
    changed = {}
    all_keys = set(old.keys()) | set(new.keys())
    for k in all_keys:
        if k in ignore_keys:
            continue
        ov, nv = old.get(k), new.get(k)
        if ov != nv:
            changed[k] = (ov, nv)
    return changed


def diff_collection(old_idx: dict, new_idx: dict, ignore_keys: set = None) -> dict:
    """Diff two indexed collections. Returns {added: [...], removed: [...], changed: {key: {field: (ov, nv)}}}."""
    added = sorted(set(new_idx.keys()) - set(old_idx.keys()))
    removed = sorted(set(old_idx.keys()) - set(new_idx.keys()))
    changed = {}
    for k in sorted(set(old_idx.keys()) & set(new_idx.keys())):
        d = diff_dicts(old_idx[k], new_idx[k], ignore_keys)
        if d:
            changed[k] = d
    return {"added": added, "removed": removed, "changed": changed}


def fmt_keytuple(k: tuple) -> str:
    return " · ".join(str(x) for x in k)


def fmt_value(v) -> str:
    if v is None:
        return "—"
    if isinstance(v, (list, dict)):
        return json.dumps(v, ensure_ascii=False, sort_keys=True)
    return str(v)


def render_report(old: dict, new: dict, out_path: Path):
    lines = []
    A = lines.append
    A("# Cossacks 3 — Snapshot diff\n")

    # Versions
    ov = old.get("version", {}).get("extracted_at_local", "?")
    nv = new.get("version", {}).get("extracted_at_local", "?")
    om = old.get("version", {}).get("game_files_mtime", {}).get("unit.script", "?")
    nm = new.get("version", {}).get("game_files_mtime", {}).get("unit.script", "?")
    A(f"- **Old snapshot:** extracted {ov} (game mtime {om})")
    A(f"- **New snapshot:** extracted {nv} (game mtime {nm})\n")

    # Constants
    A("## Constants\n")
    old_c = old.get("constants", {})
    new_c = new.get("constants", {})
    const_changes = []
    for k in sorted(set(old_c.keys()) | set(new_c.keys())):
        ov_ = old_c.get(k, {}).get("value")
        nv_ = new_c.get(k, {}).get("value")
        if ov_ != nv_:
            const_changes.append((k, ov_, nv_))
    if not const_changes:
        A("Без изменений.\n")
    else:
        A("| Константа | Old | New |")
        A("|---|---:|---:|")
        for k, ov_, nv_ in const_changes:
            A(f"| `{k}` | {fmt_value(ov_)} | {fmt_value(nv_)} |")
        A("")

    # Buildings
    A("## Buildings\n")
    old_b = index_by_keys(old.get("buildings", []), ("sid", "nation"))
    new_b = index_by_keys(new.get("buildings", []), ("sid", "nation"))
    b_diff = diff_collection(old_b, new_b,
                              ignore_keys={"name_en", "name_ru", "produces", "weapon_cost"})
    A(f"- Добавлено: **{len(b_diff['added'])}**, удалено: **{len(b_diff['removed'])}**, "
      f"изменено: **{len(b_diff['changed'])}**\n")
    if b_diff["added"]:
        A("**Added:** " + ", ".join(f"`{k[0]}@{k[1]}`" for k in b_diff["added"][:30]))
        A("")
    if b_diff["removed"]:
        A("**Removed:** " + ", ".join(f"`{k[0]}@{k[1]}`" for k in b_diff["removed"][:30]))
        A("")
    if b_diff["changed"]:
        A("**Changed:**\n")
        A("| Building | Nation | Поле | Old | New |")
        A("|---|---|---|---:|---:|")
        for k in sorted(b_diff["changed"].keys()):
            for field, (ov_, nv_) in sorted(b_diff["changed"][k].items()):
                A(f"| `{k[0]}` | {k[1]} | {field} | {fmt_value(ov_)} | {fmt_value(nv_)} |")
        A("")

    # Units
    A("## Units\n")
    old_u = index_by_keys(old.get("units", []), ("sid", "nation"))
    new_u = index_by_keys(new.get("units", []), ("sid", "nation"))
    u_diff = diff_collection(old_u, new_u,
                              ignore_keys={"name_en", "name_ru", "trained_in",
                                            "uniqueness", "available_in_nations",
                                            "weapons"})  # weapons handled separately
    A(f"- Добавлено: **{len(u_diff['added'])}**, удалено: **{len(u_diff['removed'])}**, "
      f"изменено (без weapons): **{len(u_diff['changed'])}**\n")
    if u_diff["added"]:
        A("**Added:** " + ", ".join(f"`{k[0]}@{k[1]}`" for k in u_diff["added"][:30]))
        A("")
    if u_diff["removed"]:
        A("**Removed:** " + ", ".join(f"`{k[0]}@{k[1]}`" for k in u_diff["removed"][:30]))
        A("")
    if u_diff["changed"]:
        A("**Changed (top 50):**\n")
        A("| Unit | Nation | Поле | Old | New |")
        A("|---|---|---|---:|---:|")
        count = 0
        for k in sorted(u_diff["changed"].keys()):
            for field, (ov_, nv_) in sorted(u_diff["changed"][k].items()):
                if count >= 50:
                    break
                A(f"| `{k[0]}` | {k[1]} | {field} | {fmt_value(ov_)} | {fmt_value(nv_)} |")
                count += 1
            if count >= 50:
                break
        if count >= 50:
            A(f"\n_... и ещё {sum(len(v) for v in u_diff['changed'].values()) - 50} изменений._")
        A("")

    # Weapon-specific changes (units only — flat compare on weapons[0])
    weapon_changes = []
    for k in sorted(set(old_u.keys()) & set(new_u.keys())):
        ow = (old_u[k].get("weapons") or [{}])[0]
        nw = (new_u[k].get("weapons") or [{}])[0]
        for field in ("damage", "pause_sec", "radiusmax_tiles", "kind"):
            if ow.get(field) != nw.get(field):
                weapon_changes.append((k, field, ow.get(field), nw.get(field)))
    if weapon_changes:
        A("### Weapon stat changes\n")
        A("| Unit | Nation | Поле | Old | New |")
        A("|---|---|---|---:|---:|")
        for k, field, ov_, nv_ in weapon_changes[:50]:
            A(f"| `{k[0]}` | {k[1]} | weapon.{field} | {fmt_value(ov_)} | {fmt_value(nv_)} |")
        A("")

    # Upgrades
    A("## Upgrades\n")
    old_up = index_by_keys(old.get("upgrades", []), ("sid", "nation"))
    new_up = index_by_keys(new.get("upgrades", []), ("sid", "nation"))
    up_diff = diff_collection(old_up, new_up,
                                ignore_keys={"name_en", "name_ru",
                                              "itype_short", "itype_desc"})
    A(f"- Добавлено: **{len(up_diff['added'])}**, удалено: **{len(up_diff['removed'])}**, "
      f"изменено: **{len(up_diff['changed'])}**\n")
    if up_diff["added"]:
        A(f"**Added (sample):** " + ", ".join(f"`{k[0]}@{k[1]}`" for k in up_diff["added"][:20])
          + (f" (+{len(up_diff['added']) - 20} more)" if len(up_diff["added"]) > 20 else ""))
        A("")
    if up_diff["removed"]:
        A(f"**Removed (sample):** " + ", ".join(f"`{k[0]}@{k[1]}`" for k in up_diff["removed"][:20])
          + (f" (+{len(up_diff['removed']) - 20} more)" if len(up_diff["removed"]) > 20 else ""))
        A("")
    if up_diff["changed"]:
        A("**Changed (top 50):**\n")
        A("| Upgrade | Nation | Поле | Old | New |")
        A("|---|---|---|---:|---:|")
        count = 0
        for k in sorted(up_diff["changed"].keys()):
            for field, (ov_, nv_) in sorted(up_diff["changed"][k].items()):
                if count >= 50:
                    break
                A(f"| `{k[0]}` | {k[1]} | {field} | {fmt_value(ov_)} | {fmt_value(nv_)} |")
                count += 1
            if count >= 50:
                break
        A("")

    # Sanity checks
    A("## Sanity checks\n")
    old_s = {(c["category"], c["name"]): c for c in old.get("sanity_checks", [])}
    new_s = {(c["category"], c["name"]): c for c in new.get("sanity_checks", [])}
    new_failures = []
    new_passes = []
    for k in sorted(set(old_s.keys()) | set(new_s.keys())):
        op = old_s.get(k, {}).get("pass")
        np = new_s.get(k, {}).get("pass")
        if op == True and np == False:
            new_failures.append(k)
        elif op == False and np == True:
            new_passes.append(k)
    A(f"- Newly failing: **{len(new_failures)}**, newly passing: **{len(new_passes)}**\n")
    if new_failures:
        A("**❌ Stopped passing:**")
        for k in new_failures:
            c = new_s.get(k, {})
            A(f"- [{k[0]}] {k[1]}: expected `{c.get('expected')}`, got `{c.get('actual')}`")
        A("")
    if new_passes:
        A("**✅ Started passing:**")
        for k in new_passes[:20]:
            A(f"- [{k[0]}] {k[1]}")
        A("")

    # Counts
    A("## Counts\n")
    A("| Category | Old | New | Δ |")
    A("|---|---:|---:|---:|")
    for label, key in [("Buildings", "buildings"), ("Units", "units"),
                        ("Upgrades", "upgrades"), ("Officers", "officers"),
                        ("Nations", "nations")]:
        on = len(old.get(key, []))
        nn = len(new.get(key, []))
        A(f"| {label} | {on} | {nn} | {nn - on:+d} |")

    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote diff report to {out_path} ({out_path.stat().st_size:,} bytes)")
    print(f"  Constants changed: {len(const_changes)}")
    print(f"  Buildings: +{len(b_diff['added'])}, -{len(b_diff['removed'])}, "
          f"~{len(b_diff['changed'])}")
    print(f"  Units: +{len(u_diff['added'])}, -{len(u_diff['removed'])}, "
          f"~{len(u_diff['changed'])} ({len(weapon_changes)} weapon changes)")
    print(f"  Upgrades: +{len(up_diff['added'])}, -{len(up_diff['removed'])}, "
          f"~{len(up_diff['changed'])}")
    print(f"  Sanity: {len(new_failures)} newly failing, {len(new_passes)} newly passing")


def main():
    ap = argparse.ArgumentParser(description="Diff two cossacks3_data.json snapshots")
    ap.add_argument("old", help="Path to old data.json")
    ap.add_argument("new", help="Path to new data.json")
    ap.add_argument("--out", default="snapshot_diff.md", help="Output report path")
    args = ap.parse_args()

    old = json.loads(Path(args.old).read_text(encoding="utf-8"))
    new = json.loads(Path(args.new).read_text(encoding="utf-8"))
    out_path = Path(args.out)
    render_report(old, new, out_path)


if __name__ == "__main__":
    main()
