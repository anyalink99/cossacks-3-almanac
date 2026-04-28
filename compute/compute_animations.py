"""Build per-unit animation frame database from .aaf files.

Scans `<game>/data/animations/aaf/*.aaf`, extracts every animation track's
[start, end] frame range, and writes a flat dictionary keyed by aaf basename:
  output/reference/derived/animations.json
    {
      "pikeman": {"attack0": [32, 46], "walk": [1, 24], ...},
      "peaaus":  {"construct": [186, 198], "workfood": [278, 299], ...},
      ...
    }

Each frame is 1 / gc_time_to_frames = 1/32 game-second (engine constant).
So animation length in g-sec = (end - start) / 32.

Intended consumers: counter-matrix (real per-unit melee swing), DPS tables,
construct-time / repair tables (currently uses peasant aaf only).
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "parser"))
from config import GAME_ROOT, DERIVED_DIR

AAF_DIR = GAME_ROOT / "data" / "animations" / "aaf"
OUT_PATH = DERIVED_DIR / "animations.json"

TRACK_RE = re.compile(r'"(\w+)"\s*,\s*(\d+)\s*,\s*(\d+)')


def parse_aaf(path: Path) -> dict[str, list[int]]:
    tracks: dict[str, list[int]] = {}
    txt = path.read_text(encoding="utf-8", errors="ignore")
    for m in TRACK_RE.finditer(txt):
        name = m.group(1)
        start = int(m.group(2))
        end = int(m.group(3))
        tracks[name] = [start, end]
    return tracks


def main():
    DERIVED_DIR.mkdir(parents=True, exist_ok=True)
    if not AAF_DIR.exists():
        print(f"ERROR: {AAF_DIR} not found", file=sys.stderr)
        sys.exit(1)

    out: dict[str, dict] = {}
    for path in sorted(AAF_DIR.glob("*.aaf")):
        tracks = parse_aaf(path)
        if tracks:
            out[path.stem] = tracks

    OUT_PATH.write_text(json.dumps(out, indent=2, sort_keys=True), encoding="utf-8")
    print(f"Wrote {OUT_PATH} ({len(out)} aaf files, "
          f"{sum(len(v) for v in out.values())} animation tracks)")

    # Sanity: peasant construct (inclusive frame range; length = end - start + 1)
    pea = out.get("peaaus", {})
    if "construct" in pea:
        s, e = pea["construct"]
        n = e - s + 1
        print(f"sanity: peaaus.construct = frames {s}-{e} (inclusive) = {n} frames = {n/32:.4f} g-sec")

    # Median attack0 across all (inclusive convention)
    attack_lens = []
    for sid, tracks in out.items():
        if "attack0" in tracks:
            s, e = tracks["attack0"]
            n = e - s + 1
            # Filter outliers (>100 frames is probably a multi-attack track)
            if 0 < n < 100:
                attack_lens.append(n)
    if attack_lens:
        attack_lens.sort()
        median = attack_lens[len(attack_lens) // 2]
        mean = sum(attack_lens) / len(attack_lens)
        print(f"sanity: attack0 across {len(attack_lens)} units — "
              f"median={median} frames ({median/32:.4f}s), mean={mean:.1f} frames ({mean/32:.4f}s)")


if __name__ == "__main__":
    main()
