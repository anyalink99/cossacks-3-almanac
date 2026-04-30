"""Process all replay files in a folder, extracting per-game ground truth.

For each `.rep` / `.map` file:
  1. Parse OSWMap13 header
  2. Extract game settings (mapsize, relief, mines, terraintype, season, randkeys, maskname, ...)
  3. Count occurrences of every known pattern_inventory entry — these are the
     EXACT clusters the engine placed on this game's map.

Writes:
  docs/derived/replay_ground_truth.json — per-replay records:
    {
      "file": "<basename>",
      "size_mb": float,
      "settings": {randkey0, randkey1, mapsize, relieftype, ...},
      "total_patterns": int,
      "type_counts": {pattern_type: cluster_count, ...},
      "pattern_counts": {pattern_name: count, ...}  # raw (per .pattern file)
    }

Usage:
    # Default: scan REPLAYS_DIR env var or known fallback paths
    python parser/parse_replay_aggregates.py

    # Explicit dir:
    python parser/parse_replay_aggregates.py "C:\\path\\to\\replays"
"""
from __future__ import annotations
import collections
import json
import os
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import DERIVED_DIR
from parse_replay import extract_settings, count_patterns_fast

OUT_PATH = DERIVED_DIR / "replay_ground_truth.json"


def find_replays_dir() -> Path | None:
    """Find the user's replays folder. Tries env var first, then common locations."""
    if env := os.environ.get("COSSACKS3_REPLAYS"):
        p = Path(env)
        if p.is_dir():
            return p
    # Common Cossacks 3 profile paths on Windows
    candidates = [
        Path.home() / "OneDrive" / "Документы" / "cossacks" / "profiles",
        Path.home() / "Documents" / "cossacks" / "profiles",
        Path.home() / "OneDrive" / "Documents" / "cossacks" / "profiles",
    ]
    for base in candidates:
        if not base.is_dir():
            continue
        # Look for any user profile with a replays subfolder
        for profile in base.iterdir():
            replays = profile / "replays"
            if replays.is_dir():
                return replays
    return None


def main():
    if len(sys.argv) >= 2:
        replays_dir = Path(sys.argv[1])
    else:
        replays_dir = find_replays_dir()
    if not replays_dir or not replays_dir.is_dir():
        print("No replays folder found. Set COSSACKS3_REPLAYS env var or pass as argument.")
        sys.exit(1)
    print(f"Replays dir: {replays_dir}")

    files = sorted(
        f for f in replays_dir.iterdir()
        if f.suffix.lower() in (".rep", ".map") and f.is_file()
    )
    print(f"Found {len(files)} replay files\n")

    inv_path = DERIVED_DIR / "pattern_inventory.json"
    types_path = DERIVED_DIR / "pattern_types.json"
    if not inv_path.exists() or not types_path.exists():
        print("Run parser/parse_generator_cfg.py + parser/parse_pattern_inventory.py first.")
        sys.exit(1)
    inv = json.loads(inv_path.read_text(encoding="utf-8"))
    types = json.loads(types_path.read_text(encoding="utf-8"))
    pattern_to_type: dict[str, list[str]] = {}
    for tname, pats in types.items():
        for p in pats:
            pattern_to_type.setdefault(p, []).append(tname)
    pattern_set = set(inv.keys())

    def best_type(pat_name: str) -> str | None:
        """Pick the most-specific type for a pattern. Some patterns appear in
        multiple type lists (e.g. mng_3 is in both `mng` and `desert_mng`):
        the engine actually picks based on bDesert flag. We attribute by
        longest-prefix match — `mng_3` → `mng` (not `desert_mng`), and
        `desert_mng_1_a` → `desert_mng` because pat starts with type name.
        """
        cands = pattern_to_type.get(pat_name, [])
        if not cands:
            return None
        # Prefer types whose name is a literal prefix of the pattern name.
        # Sort by name length DESC so 'desert_mng' beats 'mng' on 'desert_mng_*'.
        prefixed = [t for t in cands if pat_name.startswith(t)]
        if prefixed:
            return max(prefixed, key=len)
        # Fallback: shortest type name (most generic)
        return min(cands, key=len)

    # The replay folder typically contains personal save files with arbitrary
    # filenames (game titles, opponent names, etc.). To keep the derived JSON
    # neutral and shareable, we use opaque IDs (Replay 01, Replay 02, ...) ordered
    # by SHA-256 hash of the file contents. This is stable across runs of the
    # same replay set but reveals nothing about the original filenames.
    import hashlib
    files_with_hash = []
    for f in files:
        h = hashlib.sha256(f.read_bytes()).hexdigest()[:8]
        files_with_hash.append((h, f))
    files_with_hash.sort(key=lambda x: x[0])  # deterministic ID assignment

    all_data = []
    t_total = time.time()
    for idx, (h, f) in enumerate(files_with_hash, start=1):
        try:
            t0 = time.time()
            data = f.read_bytes()
            settings = extract_settings(data)
            pat_counts = count_patterns_fast(data, pattern_set)
            type_counts: collections.Counter = collections.Counter()
            for p, c in pat_counts.items():
                t = best_type(p)
                if t:
                    type_counts[t] += c
            replay_id = f"Replay {idx:02d}"
            all_data.append({
                "id": replay_id,
                "hash": h,                       # opaque content hash
                "size_mb": round(len(data) / 1e6, 1),
                "settings": settings,
                "total_patterns": sum(pat_counts.values()),
                "type_counts": dict(type_counts),
                "pattern_counts": dict(sorted(pat_counts.items())),
            })
            print(f"  {replay_id:<10} {h:<10} {len(data)/1e6:>6.1f}MB  "
                  f"{time.time()-t0:>5.1f}s  {sum(pat_counts.values())} patterns")
        except Exception as e:
            print(f"  Replay {idx:02d}: FAIL: {type(e).__name__}: {e}")

    print(f"\nTotal: {time.time()-t_total:.1f}s for {len(all_data)} replays")

    DERIVED_DIR.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(all_data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nWrote {OUT_PATH} ({OUT_PATH.stat().st_size:,} bytes)")

    # Summary
    print(f"\n=== Settings overview ===")
    print(f"{'id':<12} {'mskname':<35} {'tt':>2} {'rel':>3} {'msz':>3} {'mns':>3} {'rk1':>11}")
    for d in all_data:
        s = d["settings"]
        rid = d["id"]
        mn = (s.get("maskname") or "?")[:34]
        print(f"{rid:<12} {mn:<35} "
              f"{s.get('terraintype','?'):>2} {s.get('relieftype','?'):>3} "
              f"{s.get('mapsize','?'):>3} {s.get('resourcemines','?'):>3} "
              f"{s.get('randkey1','?'):>11}")

    print(f"\n=== Aggregate cluster counts (n={len(all_data)} replays) ===")
    totals = collections.Counter()
    by_type: dict[str, list[int]] = collections.defaultdict(list)
    for d in all_data:
        for k, v in d["type_counts"].items():
            totals[k] += v
            by_type[k].append(v)
    print(f"{'type':<35} {'avg':>5} {'min':>3} {'max':>3} {'n_games':>7}")
    for t, _ in sorted(totals.items(), key=lambda x: -x[1])[:30]:
        vals = by_type[t]
        print(f"  {t:<33} {sum(vals)/len(vals):>5.1f} "
              f"{min(vals):>3} {max(vals):>3} {len(vals):>7}")


if __name__ == "__main__":
    main()
