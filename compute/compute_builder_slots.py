"""Compute exact builder-slot counts for all buildings.

Faithfully simulates `_unit_CalcBuilderPoints` from `data/scripts/lib/unit.script:8702-9006`.
Algorithm: walk the perimeter of the building's collision mask in cell-edge steps of 0.5 tile,
placing a builder point every `dist=1.0` tile. Hard cap from `gc_MaxBuilderCount=30`.

Reads each `.prop` file in `<game>/data/objects/buildings/`, parses
`collisionmaskproperty.Mask`, runs the simulation, and writes:
  - output/derived/builder_slots.json  — {sid: {cols, rows, cells, perim_tiles, slots}}
  - output/reports/builder_slots.md    — sortable per-nation table
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "parser"))
from config import GAME_ROOT, OUTPUT_DIR, DERIVED_DIR, REPORTS_DIR

BUILDINGS_DIR = GAME_ROOT / "data" / "objects" / "buildings"

GC_MAX_BUILDER_COUNT = 30
GC_BUILDER_DIST = 1.0
CELL_SIZE = 0.5


def parse_mask(prop_path: Path) -> list[list[bool]] | None:
    """Extract collision mask grid from a building .prop file."""
    txt = prop_path.read_text(encoding="utf-8", errors="ignore")
    m = re.search(
        r"collisionmaskproperty\s*:\s*section\.begin.*?Mask\s*:\s*struct\.begin(.*?)struct\.end",
        txt,
        re.DOTALL,
    )
    if not m:
        return None
    rows = re.findall(r"=\s*([01]+)", m.group(1))
    if not rows:
        return None
    width = max(len(r) for r in rows)
    return [[c == "1" for c in r.ljust(width, "0")] for r in rows]


def get(mask: list[list[bool]], r: int, c: int) -> bool:
    """Safe mask read: out-of-bounds returns False (matches engine behavior)."""
    if r < 0 or r >= len(mask) or c < 0 or c >= len(mask[0]):
        return False
    return mask[r][c]


def simulate_builder_points(mask: list[list[bool]]) -> int:
    """Faithful port of _unit_CalcBuilderPoints from unit.script:8702-9006.

    Returns the number of builder points produced (before the engine cap of 30).
    """
    rows = len(mask)
    cols = len(mask[0]) if rows else 0

    # Find topmost-leftmost filled cell
    cur_row, cur_col = -1, -1
    for i in range(rows):
        for j in range(cols):
            if mask[i][j]:
                cur_row, cur_col = i, j
                break
        if cur_row >= 0:
            break
    if cur_row < 0:
        return 0  # else-branch in engine creates a default circle of 20 points; we report 0 as "no mask"

    st_row, st_col = cur_row, cur_col
    cur_x = cur_col + 1.0
    cur_y = float(cur_row)
    st_dir_x, st_dir_y = -1, 0  # stDirY uninitialized in script ⇒ Pascal default 0
    dir_x, dir_y = st_dir_x, st_dir_y

    d_len = 0.0
    points = 0

    # Safety bound — perimeter can't exceed 4*N cells; loop should terminate sooner.
    # Increase to 8*rows*cols to give plenty of headroom for weird shapes.
    max_steps = 8 * max(1, rows * cols)
    steps = 0

    while True:
        steps += 1
        if steps > max_steps:
            break  # safety; shouldn't happen for well-formed masks

        length = CELL_SIZE
        while d_len + length >= GC_BUILDER_DIST:
            length = length - (GC_BUILDER_DIST - d_len)
            points += 1
            d_len = 0.0

        d_len += length

        cur_x += dir_x
        cur_y += dir_y

        if dir_x == -1 and dir_y == 0:
            if cur_y == cur_row:
                if get(mask, cur_row - 1, cur_col - 1):
                    cur_row -= 1
                    cur_col -= 1
                    dir_x, dir_y = 0, -1
                else:
                    if get(mask, cur_row, cur_col - 1):
                        cur_col -= 1
                        dir_x, dir_y = -1, 0
                    else:
                        dir_x, dir_y = 0, 1
            else:
                if get(mask, cur_row + 1, cur_col - 1):
                    cur_row += 1
                    cur_col -= 1
                    dir_x, dir_y = 0, 1
                else:
                    if get(mask, cur_row, cur_col - 1):
                        cur_col -= 1
                        dir_x, dir_y = -1, 0
                    else:
                        dir_x, dir_y = 0, -1
        elif dir_x == 1 and dir_y == 0:
            if cur_y == cur_row:
                if get(mask, cur_row - 1, cur_col + 1):
                    cur_row -= 1
                    cur_col += 1
                    dir_x, dir_y = 0, -1
                else:
                    if get(mask, cur_row, cur_col + 1):
                        cur_col += 1
                        dir_x, dir_y = 1, 0
                    else:
                        dir_x, dir_y = 0, 1
            else:
                if get(mask, cur_row + 1, cur_col + 1):
                    cur_row += 1
                    cur_col += 1
                    dir_x, dir_y = 0, 1
                else:
                    if get(mask, cur_row, cur_col + 1):
                        cur_col += 1
                        dir_x, dir_y = 1, 0
                    else:
                        dir_x, dir_y = 0, -1
        elif dir_x == 0 and dir_y == -1:
            if cur_x == cur_col:
                if get(mask, cur_row - 1, cur_col - 1):
                    cur_row -= 1
                    cur_col -= 1
                    dir_x, dir_y = -1, 0
                else:
                    if get(mask, cur_row - 1, cur_col):
                        cur_row -= 1
                        dir_x, dir_y = 0, -1
                    else:
                        dir_x, dir_y = 1, 0
            else:
                if get(mask, cur_row - 1, cur_col + 1):
                    cur_row -= 1
                    cur_col += 1
                    dir_x, dir_y = 1, 0
                else:
                    if get(mask, cur_row - 1, cur_col):
                        cur_row -= 1
                        dir_x, dir_y = 0, -1
                    else:
                        dir_x, dir_y = -1, 0
        elif dir_x == 0 and dir_y == 1:
            if cur_x == cur_col:
                if get(mask, cur_row + 1, cur_col - 1):
                    cur_row += 1
                    cur_col -= 1
                    dir_x, dir_y = -1, 0
                else:
                    if get(mask, cur_row + 1, cur_col):
                        cur_row += 1
                        dir_x, dir_y = 0, 1
                    else:
                        dir_x, dir_y = 1, 0
            else:
                if get(mask, cur_row + 1, cur_col + 1):
                    cur_row += 1
                    cur_col += 1
                    dir_x, dir_y = 1, 0
                else:
                    if get(mask, cur_row + 1, cur_col):
                        cur_row += 1
                        dir_x, dir_y = 0, 1
                    else:
                        dir_x, dir_y = -1, 0

        if cur_row == st_row and cur_col == st_col and dir_x == st_dir_x and dir_y == st_dir_y:
            break

    # Engine adds one extra point post-loop if remaining accumulator > dist/2
    if d_len > GC_BUILDER_DIST / 2:
        points += 1

    return points


def perim_tiles(mask: list[list[bool]]) -> float:
    rows = len(mask)
    cols = len(mask[0]) if rows else 0
    n = sum(sum(r) for r in mask)
    h = sum(1 for r in range(rows) for c in range(cols - 1) if mask[r][c] and mask[r][c + 1])
    v = sum(1 for r in range(rows - 1) for c in range(cols) if mask[r][c] and mask[r + 1][c])
    return (4 * n - 2 * (h + v)) * 0.5


def first_component(mask: list[list[bool]]) -> tuple[list[list[bool]], int]:
    """Return (mask of just the topmost-leftmost connected component, cell count of that component).

    Mirrors the engine: `_unit_CalcBuilderPoints` finds the first filled cell and walks ONE component.
    """
    rows = len(mask)
    cols = len(mask[0]) if rows else 0
    start = None
    for i in range(rows):
        for j in range(cols):
            if mask[i][j]:
                start = (i, j)
                break
        if start:
            break
    if not start:
        return [[False] * cols for _ in range(rows)], 0
    comp = [[False] * cols for _ in range(rows)]
    stack = [start]
    while stack:
        r, c = stack.pop()
        if r < 0 or r >= rows or c < 0 or c >= cols:
            continue
        if comp[r][c] or not mask[r][c]:
            continue
        comp[r][c] = True
        stack.extend([(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)])
    n = sum(sum(r) for r in comp)
    return comp, n


def main():
    DERIVED_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    results: dict[str, dict] = {}
    for prop in sorted(BUILDINGS_DIR.glob("*.prop")):
        sid = prop.stem
        mask = parse_mask(prop)
        if mask is None:
            continue
        rows = len(mask)
        cols = len(mask[0])
        cells_total = sum(sum(r) for r in mask)
        comp_mask, cells_walked = first_component(mask)
        p_total = perim_tiles(mask)
        p_walked = perim_tiles(comp_mask)
        sim = simulate_builder_points(mask)
        capped = min(sim, GC_MAX_BUILDER_COUNT)
        results[sid] = {
            "cols": cols,
            "rows": rows,
            "cells_total": cells_total,
            "cells_walked": cells_walked,
            "disconnected": cells_total != cells_walked,
            "footprint_tiles2": round(cells_total * 0.25, 2),
            "perim_walked_tiles": round(p_walked, 2),
            "perim_total_tiles": round(p_total, 2),
            "slots_raw": sim,
            "slots": capped,
        }

    bavba2 = results.get("bavba2")
    if bavba2:
        print(f"sanity: bavba2 → slots_raw={bavba2['slots_raw']} slots={bavba2['slots']} perim={bavba2['perim_walked_tiles']}")

    out_json = DERIVED_DIR / "builder_slots.json"
    out_json.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {out_json} ({len(results)} buildings)")

    # Per-suffix summary table
    L = []
    L.append("# Cossacks 3 — Builder slots per building")
    L.append("")
    L.append("Сколько крестьян могут одновременно строить здание (точная симуляция "
             "[`_unit_CalcBuilderPoints`](C:/Program Files (x86)/Steam/steamapps/common/Cossacks 3/data/scripts/lib/unit.script#L8702)).")
    L.append("")
    L.append("**Алгоритм:** обход периметра collision mask, 1 точка через каждый `dist=1.0` тайл. "
             "Hard cap движка: `gc_MaxBuilderCount = 30`.")
    L.append("")
    L.append("`slots_raw` — результат симуляции до cap; `slots` — фактический cap (raw, обрезанный до 30). "
             "`perim` — длина периметра обходимой компоненты в тайлах. `cells` — закрашенных клеток в этой "
             "компоненте. `footprint_tiles²` ≈ cells × 0.25.")
    L.append("")
    L.append("⚠️ Если маска состоит из нескольких несвязанных компонентов (см. колонку «disc»), "
             "движок обходит только верхнюю-левую — для остальных частей крестьянам **не назначаются** "
             "слоты. Это поведение из [`unit.script:8722-8729`](C:/Program Files (x86)/Steam/steamapps/common/Cossacks 3/data/scripts/lib/unit.script#L8722).")
    L.append("")

    suffix_groups = {
        "Town centers (cen)": "cen",
        "Storehouses (sto)": "sto",
        "Mills (mil)": "mil",
        "Houses (hou)": "hou",
        "Farms (sta)": "sta",
        "Markets (mar)": "mar",
        "Diplomatic (dip)": "dip",
        "Temples (tem)": "tem",
        "Barracks 17c (bar)": "bar",
        "Barracks 18c (ba2)": "ba2",
        "Stables (sta)": None,  # handled by sta above
        "Blacksmith (bla)": "bla",
        "Academy (aca)": "aca",
        "Artillery depot (art)": "art",
        "Shipyards (por)": "por",
        "Towers (tow)": "tow",
        "Mines (gol/iro/coa)": ("gol", "iro", "coa"),
        "Walls (swa/wwa)": ("swa", "wwa"),
        "Gates (sga/wga)": ("sga", "wga"),
    }

    by_suffix: dict[str, list[tuple[str, dict]]] = {}
    for sid, info in results.items():
        # last 3 chars after the 3-char nation/cluster prefix
        sfx = sid[-3:] if len(sid) >= 3 else sid
        by_suffix.setdefault(sfx, []).append((sid, info))

    for label, suffixes in suffix_groups.items():
        if suffixes is None:
            continue
        keys = (suffixes,) if isinstance(suffixes, str) else suffixes
        rows = []
        for k in keys:
            rows.extend(by_suffix.get(k, []))
        if not rows:
            continue
        rows.sort(key=lambda x: x[1]["slots"])
        L.append(f"## {label}")
        L.append("")
        L.append("| sid | cols × rows | cells (walked / total) | perim (walked) | disc | slots |")
        L.append("|---|---|---|---|---|---|")
        for sid, info in rows:
            cells = (f"{info['cells_walked']} / {info['cells_total']}"
                     if info["disconnected"] else f"{info['cells_walked']}")
            disc = "⚠ да" if info["disconnected"] else "—"
            L.append(f"| `{sid}` | {info['cols']}×{info['rows']} | {cells} | "
                     f"{info['perim_walked_tiles']} | {disc} | **{info['slots']}** |")
        L.append("")

    # leftover suffixes not covered
    covered = set()
    for s in suffix_groups.values():
        if s is None:
            continue
        if isinstance(s, str):
            covered.add(s)
        else:
            covered.update(s)
    other_keys = sorted(set(by_suffix.keys()) - covered)
    if other_keys:
        L.append("## Прочие (не классифицированы по суффиксу)")
        L.append("")
        L.append("| sid | cols × rows | cells (walked / total) | perim (walked) | disc | slots |")
        L.append("|---|---|---|---|---|---|")
        rows = []
        for k in other_keys:
            rows.extend(by_suffix[k])
        rows.sort(key=lambda x: (x[0]))
        for sid, info in rows:
            cells = (f"{info['cells_walked']} / {info['cells_total']}"
                     if info["disconnected"] else f"{info['cells_walked']}")
            disc = "⚠ да" if info["disconnected"] else "—"
            L.append(f"| `{sid}` | {info['cols']}×{info['rows']} | {cells} | "
                     f"{info['perim_walked_tiles']} | {disc} | **{info['slots']}** |")
        L.append("")

    out_md = REPORTS_DIR / "builder_slots.md"
    out_md.write_text("\n".join(L), encoding="utf-8")
    print(f"Wrote {out_md}")


if __name__ == "__main__":
    main()
