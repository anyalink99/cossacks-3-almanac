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
from config import GAME_ROOT, OUTPUT_DIR, DERIVED_DIR, REPORTS_DIR, REPORTS_ECONOMY_DIR
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

    cites = Citations()
    L = []
    L.append("# Cossacks 3 — Слоты строителей у зданий")
    L.append("")
    L.append("Сколько крестьян могут одновременно строить здание. Считается из "
             "`collisionmaskproperty.Mask` каждого `.prop` файла в "
             "`data/objects/buildings/` по правилу, эмпирически согласованному с игрой.")
    L.append("")
    L.append("**Формула** (см. [`recon/world/building_mechanics.md`](../../recon/world/building_mechanics.md), "
             "раздел про слоты):")
    L.append("")
    L.append(f"- Для нормальных зданий — точный обход периметра `_unit_CalcBuilderPoints` "
             f"{cites.cite('lib/unit.script:8702-9006', label='`_unit_CalcBuilderPoints`')} "
             f"по верхне-левой компоненте collision mask. Для выпуклых форм результат "
             f"равен `bbox_cols + bbox_rows` (Manhattan-периметр); для non-convex "
             f"(арки, кресты) walker даёт больше.")
    L.append("- Если маска **разорвана на несколько линейных** «опорных» планок 1×N (склады) — "
             "движок ведёт себя так, будто bbox-объединение всех планок заполнено сплошняком. "
             "Используем `bbox_cols + bbox_rows` объединения (см. колонку «метод»).")
    L.append("- Жёсткий лимит движка: `gc_MaxBuilderCount = 30`.")
    L.append("")
    L.append("**Эмпирически подтверждено** (счёт крестьян в игре):")
    L.append("")
    L.append("| sid | предсказание | в игре | примечание |")
    L.append("|---|---|---|---|")
    L.append("| `polcen` (польский ГЦ) | 18 | 18 ✓ | выпуклый ромб |")
    L.append("| `ruscen` (русский ГЦ) | 24 | 24 ✓ | выпуклый |")
    L.append("| `swecen` (шведский ГЦ) | **27** | **27 ✓** | **non-convex** (арка с двумя ногами) |")
    L.append("| `eurmil` (европейская мельница) | 10 | 10 ✓ | выпуклый |")
    L.append("| `rusmil` (русская мельница) | 7 | 7 ✓ | выпуклый |")
    L.append("| `polbla` (польская кузница) | 18 | 18 ✓ | выпуклый |")
    L.append("| `polba2` (польская казарма 18 в.) | 25 | 25 ✓ | выпуклый |")
    L.append("| `tursto` (турецкий склад) | 8 | 8 ✓ | walker по большой компоненте |")
    L.append("| `spasto` (испанский склад) | 7 | 7 ✓ | walker по большой компоненте, орфан игнорируется (видна пустая левая сторона) |")
    L.append("| `russto` (русский склад) | 8 | 8 ✓ | правило bbox_union для линейных опор |")
    L.append("| `eursto` (европейский склад) | 9 | 8 | известное расхождение −1 |")
    L.append("")
    L.append("**Walker корректен и на non-convex** (`swecen` подтвердил это эмпирически: 27 = walker, "
             "не 24 = bbox_perim). Movement по внутренним вмятинам арки добавляет +3 слота относительно "
             "выпуклого bbox. Всего 5 single-component non-convex зданий: `scocen` (+4), `swecen` (+3), "
             "`portem` (+2), `bavhou` (+1), `ukrtem` (+1) — для них walker даёт больше слотов, чем bbox-perim.")
    L.append("")
    L.append("**Колонки таблиц:**")
    L.append("")
    L.append("- `bbox` — размеры прямоугольника, охватывающего все заполненные ячейки маски (в half-tile клетках).")
    L.append("- `cells` — общее число заполненных ячеек.")
    L.append("- `комп.` — число несвязанных компонент в маске (для большинства = 1).")
    L.append("- `метод` — `walker` (точный обход) или `bbox_union` (правило для линейных «опор»).")
    L.append("- `слоты` — итоговое число одновременных строителей (после cap=30).")
    L.append("")
    L.append("⚠️ **Ворота** (`*sga`, `*wga`, `*sga_*`, `*wga_*`) не строятся крестьянами. "
             "Игрок выделяет существующий участок стены и кликает «превратить в ворота» — "
             "слоты в таблицах ниже информативны, но в обычной игре не используются.")
    L.append("")

    suffix_groups = {
        "Городские центры (cen)": "cen",
        "Склады (sto)": "sto",
        "Мельницы (mil)": "mil",
        "Дома (hou)": "hou",
        "Конюшни (sta)": "sta",
        "Базары (mar)": "mar",
        "Дипломатические центры (dip)": "dip",
        "Храмы (tem)": "tem",
        "Казармы 17 в. (bar)": "bar",
        "Казармы 18 в. (ba2)": "ba2",
        "Кузницы (bla)": "bla",
        "Академии (aca)": "aca",
        "Артиллерийские депо (art)": "art",
        "Порты (por)": "por",
        "Башни (tow)": "tow",
        "Шахты (gol/iro/coa)": ("gol", "iro", "coa"),
        "Стены (swa/wwa)": ("swa", "wwa"),
        "Ворота (sga/wga) — не строятся крестьянами": ("sga", "wga"),
    }

    by_suffix: dict[str, list[tuple[str, dict]]] = {}
    for sid, info in results.items():
        sfx = sid[-3:] if len(sid) >= 3 else sid
        by_suffix.setdefault(sfx, []).append((sid, info))

    def render_table(rows_data):
        out = ["| sid | bbox | cells | комп. | метод | слоты |",
               "|---|---|---:|---:|---|---:|"]
        for sid, info in rows_data:
            method = info["method"]
            method_label = "walker" if method == "walker" else ("bbox_union" if method == "bbox_union" else method)
            out.append(f"| `{sid}` | {info['bbox_cols']}×{info['bbox_rows']} | "
                       f"{info['cells_total']} | {info['n_components']} | "
                       f"{method_label} | **{info['slots']}** |")
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
