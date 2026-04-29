"""Parse data/game/var/generator.cfg into a pattern_type → [pattern_files] mapping.

This file is the missing link between the abstract pattern names used by
`_misc_PlacePatternByType('forests_pine_big', ...)` and the concrete
`.pattern` files on disk. Without it, compute_map_resources had to guess
which patterns correspond to "forests_pine_big" / "stones" / etc.

Output: output/derived/pattern_types.json
  {
    "forests_pine_big": ["frt_b_p_1", "frt_b_p_2", ...],
    "forests_mixed_big": ["e_frt_big_1", ...],
    "stones": ["d_stn_1", ...],
    "mng": ["mng_1", "mng_2", ...],
    ...
  }

Used by:
  - compute_pattern_inventory.py (group stats by type, not raw filename prefix)
  - compute_map_resources.py (pick correct tree-count median per `foreststype`)
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import GAME_ROOT, DERIVED_DIR

CFG_PATH = GAME_ROOT / "data" / "game" / "var" / "generator.cfg"
OUT_PATH = DERIVED_DIR / "pattern_types.json"


def parse() -> dict[str, list[str]]:
    if not CFG_PATH.exists():
        raise FileNotFoundError(f"{CFG_PATH} not found")
    text = CFG_PATH.read_text(encoding="utf-8", errors="ignore")

    type_to_patterns: dict[str, list[str]] = {}
    current_type: str | None = None
    in_pattern_list = False
    for line in text.splitlines():
        m = re.match(r'\s+Name\s*=\s*(\S+)', line)
        if m:
            current_type = m.group(1)
            type_to_patterns.setdefault(current_type, [])
            in_pattern_list = False
            continue
        if 'PatternList' in line and 'struct.begin' in line:
            in_pattern_list = True
            continue
        if in_pattern_list and current_type:
            m = re.match(r'\s+Pattern\s*=\s*(\S+)', line)
            if m:
                type_to_patterns[current_type].append(m.group(1))
    return type_to_patterns


def main():
    DERIVED_DIR.mkdir(parents=True, exist_ok=True)
    types = parse()
    OUT_PATH.write_text(json.dumps(types, indent=2, sort_keys=True), encoding="utf-8")
    n_types = len(types)
    n_pats = sum(len(v) for v in types.values())
    print(f"Wrote {OUT_PATH} ({n_types} types, {n_pats} pattern refs)")
    print("\nForest type families (n_files):")
    for t in sorted(types):
        if 'forest' in t.lower() or 'frt' in t.lower():
            print(f"  {t}: {len(types[t])}")


if __name__ == "__main__":
    main()
