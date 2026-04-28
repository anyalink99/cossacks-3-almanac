"""Walk the entire `data/pattern/` directory, parse every .pattern file, and
write per-pattern + per-type inventory.

Outputs:
  - `output/reference/derived/pattern_inventory.json` — per pattern_name:
      {width, height, cells, occupied_cells, object_count, file_size, valid}
  - `output/reference/derived/pattern_type_stats.json` — per pattern_type
    (joined via parse_generator_cfg.parse() = generator.cfg PatternList map):
      {n_files, min, median, mean, max, files: [pattern_names]}

⚠ Caveats on `object_count`:
  - For FORESTS / BRUSHES: empirically each mask=1 cell ≈ one spawned object.
    Verified on `brush_plt_1x1` (4×4 mask, 8 occupied cells = 8 visible bushes).
  - For MINES (`mng/mni/mnc`): mask=1 cells are the deposit's collision
    footprint, NOT individual objects. All 18 mine patterns have exactly 32
    mask cells and produce ONE deposit each.
  - For STONES: mask=1 ≈ one stone (clusters of ~10 mask cells = ~10 stones).
  - Without engine-side C++ source, definitive answer requires in-game test.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Allow running as a script from anywhere within the repo.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "parser"))

from config import DERIVED_DIR, GAME_ROOT  # noqa: E402
from parse_patterns import parse_pattern_summary  # noqa: E402
from parse_generator_cfg import parse as parse_pattern_types  # noqa: E402


PATTERN_DIR = GAME_ROOT / "data" / "pattern"
OUT_PATH = DERIVED_DIR / "pattern_inventory.json"
TYPE_STATS_PATH = DERIVED_DIR / "pattern_type_stats.json"


def main() -> None:
    if not PATTERN_DIR.exists():
        raise SystemExit(f"Pattern directory not found: {PATTERN_DIR}")

    inventory: dict[str, dict] = {}
    files = sorted(PATTERN_DIR.glob("*.pattern"))
    bad = 0
    for fp in files:
        summary = parse_pattern_summary(fp)
        name = summary.pop("name")
        if not summary.get("valid", False):
            bad += 1
        inventory[name] = summary

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(
        json.dumps(inventory, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    print(f"Parsed {len(inventory)} patterns ({bad} invalid)")
    print(f"Wrote {OUT_PATH}")

    # Quick sanity report on the validation files mentioned in the original task.
    sample_names = [
        "brush_plt_1x1",
        "d_frt_small_1",
        "d_frt_mid_1",
        "d_frt_big_1",
    ]
    print("\nValidation samples:")
    for n in sample_names:
        info = inventory.get(n)
        if info is None:
            continue
        print(
            f"  {n:25s}  "
            f"{info.get('width', '?'):>3}x{info.get('height', '?'):<3}  "
            f"file={info.get('file_size'):>7}  "
            f"cells={info.get('cells', '?'):>5}  "
            f"objects={info.get('object_count', '?'):>5}"
        )

    # Aggregate by pattern TYPE (from generator.cfg PatternList) — this is the
    # authoritative grouping the engine uses when picking a pattern via
    # `_misc_PlacePatternByType('forests_pine_big', ...)`.
    type_to_patterns = parse_pattern_types()
    type_stats: dict[str, dict] = {}
    for tname, patterns in sorted(type_to_patterns.items()):
        counts = []
        for p in patterns:
            info = inventory.get(p)
            if info and info.get("valid"):
                counts.append(info["object_count"])
        if not counts:
            continue
        counts.sort()
        type_stats[tname] = {
            "n_files": len(counts),
            "min": min(counts),
            "median": counts[len(counts) // 2],
            "mean": round(sum(counts) / len(counts), 1),
            "max": max(counts),
            "files": list(patterns),
        }

    TYPE_STATS_PATH.write_text(
        json.dumps(type_stats, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    print(f"Wrote {TYPE_STATS_PATH}")

    print("\nForest pattern types — mask cell stats:")
    print(f"  {'type':<35} {'n':>3} {'min':>5} {'med':>5} {'mean':>6} {'max':>5}")
    for tname, s in sorted(type_stats.items()):
        if "forest" not in tname.lower() and "stone" not in tname.lower() and not tname.startswith("mn"):
            continue
        print(f"  {tname:<35} {s['n_files']:>3} {s['min']:>5} "
              f"{s['median']:>5} {s['mean']:>6.0f} {s['max']:>5}")


if __name__ == "__main__":
    main()
