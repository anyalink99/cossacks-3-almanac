"""Compute builder-slot counts (how many peasants can simultaneously build a structure).

Two regimes, picked per-mask:

1. **Walker** — faithful port of `_unit_CalcBuilderPoints` from
   `data/scripts/lib/unit.script:8702-9006`. Walks the perimeter of the topmost-leftmost
   connected component in 0.5-tile steps, placing a point every `dist=1.0`.
   Empirically verified against in-game counts for: tursto=8, spasto=7, polcen=18,
   eurmil=10, rusmil=7, ruscen=24, polbla=18, polba2=25.

2. **Bbox-of-union** — used only when the mask has multiple disconnected components
   AND every component is linear (1 cell wide in some axis). For these "corner-post"
   masks, the walker undercounts because it walks only one bar. Empirical:
   russto=8 (matches bbox 5×3 perim exactly), eursto=8 (bbox 6×3 perim=9, off by 1
   — accepted as a known edge case).

Hard cap from `gc_MaxBuilderCount=30`. Note: gates (`*sga`, `*wga`, `*sga_*`) are
**not built by peasants** in normal play — wall players click an existing wall segment
to convert it. Their slot counts are reported but unused in practice.

Reads each `.prop` in `<game>/data/objects/buildings/`, parses
`collisionmaskproperty.Mask`, runs the chosen formula, and writes:
  - derived/builder_slots.json  — {sid: {cols, rows, cells, slots, method, ...}}
  - docs/reports/economy/builder_slots.md    — per-category table (Russian)
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "parser"))
from config import (GAME_ROOT, OUTPUT_DIR, DERIVED_DIR, REPORTS_DIR,
                    REPORTS_ECONOMY_DIR, DATA_JSON, nation_ru)
from citations import Citations

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


def all_components(mask: list[list[bool]]) -> list[list[tuple[int, int]]]:
    """Return list of all 4-connected components as cell-coordinate lists."""
    rows = len(mask)
    cols = len(mask[0]) if rows else 0
    seen = [[False] * cols for _ in range(rows)]
    comps: list[list[tuple[int, int]]] = []
    for r in range(rows):
        for c in range(cols):
            if not mask[r][c] or seen[r][c]:
                continue
            comp: list[tuple[int, int]] = []
            stack = [(r, c)]
            while stack:
                rr, cc = stack.pop()
                if rr < 0 or rr >= rows or cc < 0 or cc >= cols:
                    continue
                if seen[rr][cc] or not mask[rr][cc]:
                    continue
                seen[rr][cc] = True
                comp.append((rr, cc))
                stack.extend([(rr - 1, cc), (rr + 1, cc), (rr, cc - 1), (rr, cc + 1)])
            comps.append(comp)
    return comps


def is_linear(comp: list[tuple[int, int]]) -> bool:
    """True if component spans only 1 row OR only 1 column (a 1-cell-wide bar)."""
    if not comp:
        return True
    rs = {r for r, _ in comp}
    cs = {c for _, c in comp}
    return len(rs) == 1 or len(cs) == 1


def union_bbox(cells: list[tuple[int, int]]) -> tuple[int, int]:
    """Return (cols, rows) of the bounding rectangle covering all given cells."""
    if not cells:
        return 0, 0
    rmin = min(r for r, _ in cells)
    rmax = max(r for r, _ in cells)
    cmin = min(c for _, c in cells)
    cmax = max(c for _, c in cells)
    return cmax - cmin + 1, rmax - rmin + 1


def calc_slots(mask: list[list[bool]]) -> tuple[int, str]:
    """Return (slots_raw, method) — uncapped slot count plus which formula was used.

    Rule (empirically derived):
    - If mask is disconnected AND every component is linear (1 cell wide), use the
      bbox of the union (cols+rows). This catches "corner-post" storehouse masks
      where the walker would only see one bar.
    - Otherwise use the engine's literal walker on the topmost-leftmost component.
      For convex/single-component masks this equals cols+rows of that component's
      bbox by Manhattan-perimeter geometry, which has been verified empirically.
    """
    comps = all_components(mask)
    if not comps:
        return 0, "empty"
    if len(comps) > 1 and all(is_linear(c) for c in comps):
        cells = [cell for comp in comps for cell in comp]
        c, r = union_bbox(cells)
        return c + r, "bbox_union"
    return simulate_builder_points(mask), "walker"


def main():
    DERIVED_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_ECONOMY_DIR.mkdir(parents=True, exist_ok=True)

    results: dict[str, dict] = {}
    for prop in sorted(BUILDINGS_DIR.glob("*.prop")):
        sid = prop.stem
        mask = parse_mask(prop)
        if mask is None:
            continue
        rows = len(mask)
        cols = len(mask[0])
        cells_total = sum(sum(r) for r in mask)
        comps = all_components(mask)
        n_comps = len(comps)
        all_linear = bool(comps) and all(is_linear(c) for c in comps)
        cells_in_comps = [cell for comp in comps for cell in comp]
        bbox_cols, bbox_rows = union_bbox(cells_in_comps)
        slots_raw, method = calc_slots(mask)
        capped = min(slots_raw, GC_MAX_BUILDER_COUNT)
        results[sid] = {
            "cols": cols,
            "rows": rows,
            "cells_total": cells_total,
            "n_components": n_comps,
            "all_linear": all_linear,
            "bbox_cols": bbox_cols,
            "bbox_rows": bbox_rows,
            "footprint_tiles2": round(cells_total * 0.25, 2),
            "method": method,
            "slots_raw": slots_raw,
            "slots": capped,
        }

    out_json = DERIVED_DIR / "builder_slots.json"
    out_json.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {out_json} ({len(results)} buildings)")

    # Sanity: storehouses (the cases that drove the model)
    for sid in ("russto", "eursto", "spasto", "tursto"):
        info = results.get(sid)
        if info:
            print(f"  {sid}: {info['bbox_cols']}×{info['bbox_rows']} "
                  f"comps={info['n_components']} linear={info['all_linear']} "
                  f"method={info['method']} → slots={info['slots']}")

    data = json.loads(DATA_JSON.read_text(encoding="utf-8"))
    buildings_by_sid: dict[str, dict] = {}
    nations_by_sid: dict[str, set[str]] = {}
    for building in data.get("buildings", []):
        sid = building.get("sid")
        if not sid:
            continue
        buildings_by_sid.setdefault(sid, building)
        nations_by_sid.setdefault(sid, set()).add(building.get("nation"))

    cites = Citations()
    L = []
    L.append("# Максимальное число строителей")
    L.append("")
    L.append("[← Таблицы и расчёты](../README.md)")
    L.append("")
    L.append("У каждого здания есть предел крестьян, которые могут одновременно "
             "участвовать в строительстве или ремонте. Лишние рабочие не ускоряют "
             "процесс. Предел зависит от формы и размера здания, поэтому национальные "
             "варианты одной постройки иногда различаются.")
    L.append("")
    L.append("Игра никогда не допускает больше **30** одновременных строителей. "
             "Расчёт ниже повторяет расстановку рабочих по периметру здания "
             f"{cites.cite('lib/unit.script:8702-9006', label='расстановка строителей')}. "
             "Основные значения дополнительно проверены непосредственно в игре.")
    L.append("")
    L.append("Ворота создаются мгновенным преобразованием выбранного сегмента стены. "
             "Указанный для них предел нужен только при ремонте.")
    L.append("")
    L.append("Практическое время с разным числом рабочих приведено в "
             "[таблице строительства и ремонта](construction_times.md).")
    L.append("")

    suffix_groups = {
        "Городские центры": "cen",
        "Склады": "sto",
        "Мельницы": "mil",
        "Дома": "hou",
        "Конюшни": "sta",
        "Рынки": "mar",
        "Дипломатические центры": "dip",
        "Храмы": "tem",
        "Казармы XVII века": "bar",
        "Казармы XVIII века": "ba2",
        "Кузницы": "bla",
        "Академии": "aca",
        "Артиллерийские депо": "art",
        "Порты": "por",
        "Башни": "tow",
        "Шахты": ("gol", "iro", "coa"),
        "Стены": ("swa", "wwa"),
        "Ворота": ("sga", "wga"),
    }

    by_suffix: dict[str, list[tuple[str, dict]]] = {}
    for sid, info in results.items():
        sfx = sid[-3:] if len(sid) >= 3 else sid
        by_suffix.setdefault(sfx, []).append((sid, info))

    def render_table(rows_data):
        out = ["| Здание | Код | Нации | Максимум строителей |",
               "|---|---|---|---:|"]
        for sid, info in rows_data:
            building = buildings_by_sid.get(sid) or {}
            name = building.get("name_ru") or building.get("name_en") or "Здание"
            nation_codes = sorted(n for n in nations_by_sid.get(sid, set()) if n)
            nation_text = "все 21" if len(nation_codes) == 21 else ", ".join(
                nation_ru(nation) for nation in nation_codes
            )
            out.append(f"| {name} | `{sid}` | {nation_text or '—'} | "
                       f"**{info['slots']}** |")
        return out

    for label, suffixes in suffix_groups.items():
        keys = (suffixes,) if isinstance(suffixes, str) else suffixes
        rows = []
        for k in keys:
            rows.extend(by_suffix.get(k, []))
        if not rows:
            continue
        rows.sort(key=lambda x: x[1]["slots"])
        L.append(f"## {label}")
        L.append("")
        L.extend(render_table(rows))
        L.append("")

    covered = set()
    for s in suffix_groups.values():
        if isinstance(s, str):
            covered.add(s)
        else:
            covered.update(s)
    other_keys = sorted(set(by_suffix.keys()) - covered)
    if other_keys:
        L.append("## Прочие (миссии/сегменты стен/мосты)")
        L.append("")
        L.extend(render_table(sorted(
            [item for k in other_keys for item in by_suffix[k]],
            key=lambda x: x[0],
        )))
        L.append("")

    L.extend(cites.render())
    out_md = REPORTS_ECONOMY_DIR / "builder_slots.md"
    out_md.write_text("\n".join(L), encoding="utf-8")
    print(f"Wrote {out_md}")


if __name__ == "__main__":
    main()
