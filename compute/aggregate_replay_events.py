"""Walk a directory of `.rep` files, decode every event, and emit
aggregate statistics covering handler frequency, ordtyp distribution,
trade-pair counts, first-build timings and per-replay summaries.

The replay directory is taken from `$COSSACKS3_REPLAYS`, the first CLI
argument, or autodetected under the user's Cossacks 3 profile folder.

Outputs:
    derived/replay_events_per_file.json
    derived/replay_events_aggregate.json
    derived/replay_events_summary.csv

Run: `python compute/aggregate_replay_events.py [<replays_dir>]`
"""
from __future__ import annotations
import csv
import json
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "parser"))

from parse_replay_events import walk_entries, decode_subpackages  # type: ignore
from parse_replay_aggregates import find_replays_dir  # type: ignore

OUT_DIR = PROJECT_ROOT / "derived"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def process_replay(path: Path) -> dict:
    """Walk one replay, return aggregate stats for that file."""
    data = path.read_bytes()
    entries = walk_entries(data)
    body_entries = entries[1:] if entries and entries[0][0] == 0.0 else entries

    by_handler: Counter = Counter()
    by_pid: Counter = Counter()
    by_ordtyp: Counter = Counter()
    by_sid_built: Counter = Counter()  # ReadConstruct sids
    by_sid_produced: Counter = Counter()  # ReadNew sids
    trade_pairs: Counter = Counter()
    upgrade_ids: Counter = Counter()
    deaths_per_player: Counter = Counter()
    construct_per_player: Counter = Counter()
    produce_per_player: Counter = Counter()
    first_build_ts = {}
    last_event_ts = 0.0

    for ts, _sz, payload in body_entries:
        for rec in decode_subpackages(payload, ts):
            h = rec.get("handler", "?")
            by_handler[h] += 1
            pid = rec.get("pid")
            if pid is not None:
                by_pid[pid] += 1
            if h == "ReadOrder":
                by_ordtyp[rec.get("ordtyp_name", "?")] += 1
            elif h == "ReadConstruct":
                sid = rec.get("sid", "?")
                by_sid_built[sid] += 1
                construct_per_player[pid] += 1
                key = (pid, sid)
                if key not in first_build_ts:
                    first_build_ts[key] = rec["ts_g_sec"]
            elif h == "ReadNew":
                by_sid_produced[rec.get("sid", "?")] += 1
                produce_per_player[pid] += 1
            elif h == "ReadTrade":
                trade_pairs[(rec["sell_res"], rec["buy_res"])] += 1
            elif h == "ReadUpgrade":
                upgrade_ids[rec.get("upgrade_id", -1)] += 1
            elif h == "ReadDeath":
                deaths_per_player[pid] += len(rec.get("dead_uids", []))
        if entries:
            last_event_ts = ts

    return {
        "file": path.name,
        "size_bytes": len(data),
        "n_entries": len(entries),
        "duration_g_sec": round(last_event_ts / 10.0, 2),
        "by_handler": dict(by_handler.most_common()),
        "by_pid": dict(by_pid.most_common()),
        "by_ordtyp": dict(by_ordtyp.most_common()),
        "constructs_per_pid": dict(construct_per_player),
        "spawns_per_pid": dict(produce_per_player),
        "deaths_per_pid": dict(deaths_per_player),
        "buildings_built": dict(by_sid_built.most_common()),
        "units_spawned_top": dict(by_sid_produced.most_common(15)),
        "trade_pairs": {f"{s}->{b}": c for (s, b), c in trade_pairs.most_common()},
        "upgrade_ids_used": dict(upgrade_ids.most_common(15)),
        "first_builds": {f"pid{p}/{sid}": round(t, 1) for (p, sid), t in sorted(first_build_ts.items())},
    }


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) > 1:
        replays_dir = Path(sys.argv[1])
    else:
        replays_dir = find_replays_dir()
    if replays_dir is None or not replays_dir.is_dir():
        print("error: replays directory not found. Set $COSSACKS3_REPLAYS "
              "or pass the path as first argument.", file=sys.stderr)
        sys.exit(1)
    replays = sorted(replays_dir.glob("*.rep"))
    print(f"Found {len(replays)} replays in {replays_dir}")

    per_replay = []
    total_handler: Counter = Counter()
    total_ordtyp: Counter = Counter()
    total_sid_built: Counter = Counter()
    total_units_spawned: Counter = Counter()
    total_trade_pairs: Counter = Counter()
    total_upgrade_ids: Counter = Counter()
    total_first_build_by_sid = defaultdict(list)
    durations: list[float] = []

    for i, path in enumerate(replays):
        print(f"  [{i+1}/{len(replays)}] {path.name}...", end=" ", flush=True)
        try:
            stats = process_replay(path)
            per_replay.append(stats)
            durations.append(stats["duration_g_sec"])
            for h, c in stats["by_handler"].items():
                total_handler[h] += c
            for o, c in stats["by_ordtyp"].items():
                total_ordtyp[o] += c
            for s, c in stats["buildings_built"].items():
                total_sid_built[s] += c
            for s, c in stats["units_spawned_top"].items():
                total_units_spawned[s] += c
            for k, c in stats["trade_pairs"].items():
                total_trade_pairs[k] += c
            for uid, c in stats["upgrade_ids_used"].items():
                total_upgrade_ids[int(uid)] += c
            for key, t in stats["first_builds"].items():
                _, sid = key.split("/", 1)
                total_first_build_by_sid[sid].append(t)
            print(f"OK {stats['duration_g_sec']/60:.1f}min, {sum(stats['by_handler'].values())} sub-pkg")
        except Exception as e:
            print(f"ERROR: {e}")

    # Write per-replay JSON
    (OUT_DIR / "replay_events_per_file.json").write_text(
        json.dumps(per_replay, indent=2, ensure_ascii=False), encoding="utf-8")

    # CSV summary
    csv_path = OUT_DIR / "replay_events_summary.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["file", "size_bytes", "n_entries", "duration_g_min",
                    "n_sub_pkg", "n_constructs", "n_spawns", "n_deaths",
                    "n_orders", "n_trades", "n_upgrades", "n_walls",
                    "n_proj"])
        for s in per_replay:
            h = s["by_handler"]
            w.writerow([
                s["file"], s["size_bytes"], s["n_entries"],
                round(s["duration_g_sec"]/60, 1),
                sum(h.values()),
                h.get("ReadConstruct", 0), h.get("ReadNew", 0),
                sum(s["deaths_per_pid"].values()),
                h.get("ReadOrder", 0), h.get("ReadTrade", 0),
                h.get("ReadUpgrade", 0), h.get("ReadWall", 0),
                h.get("ReadProj", 0),
            ])
    print(f"\nWrote per-file CSV: {csv_path}")

    # Aggregate stats
    aggregate = {
        "n_replays": len(per_replay),
        "total_duration_g_min": round(sum(durations) / 60, 1),
        "avg_duration_g_min": round((sum(durations) / len(durations)) / 60, 1) if durations else 0,
        "min_duration_g_min": round(min(durations) / 60, 1) if durations else 0,
        "max_duration_g_min": round(max(durations) / 60, 1) if durations else 0,
        "all_handlers": dict(total_handler.most_common()),
        "all_ordtyp": dict(total_ordtyp.most_common()),
        "all_buildings_built": dict(total_sid_built.most_common(30)),
        "all_units_spawned": dict(total_units_spawned.most_common(30)),
        "all_trade_pairs": dict(total_trade_pairs.most_common(20)),
        "all_upgrade_ids": dict(total_upgrade_ids.most_common(20)),
        "first_build_ts_per_sid": {
            sid: {"min": round(min(ts), 1), "max": round(max(ts), 1),
                  "avg": round(sum(ts)/len(ts), 1), "n": len(ts)}
            for sid, ts in sorted(total_first_build_by_sid.items())
        },
    }
    agg_path = OUT_DIR / "replay_events_aggregate.json"
    agg_path.write_text(
        json.dumps(aggregate, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote aggregate JSON: {agg_path}")

    # Print key findings
    print("\n=== Aggregate findings ===")
    print(f"Replays parsed: {aggregate['n_replays']}")
    print(f"Total game-time: {aggregate['total_duration_g_min']} g-min")
    print(f"Avg game length: {aggregate['avg_duration_g_min']} g-min")
    print(f"Min/Max:         {aggregate['min_duration_g_min']} / {aggregate['max_duration_g_min']} g-min")
    print(f"\nTop handlers across all replays:")
    for h, c in list(aggregate["all_handlers"].items())[:15]:
        print(f"  {h:<30s} {c:>10,}")
    print(f"\nTop ordtyp (player commands):")
    for o, c in aggregate["all_ordtyp"].items():
        print(f"  {o:<25s} {c:>8,}")
    print(f"\nTop buildings built:")
    for s, c in list(aggregate["all_buildings_built"].items())[:15]:
        print(f"  {s:<15s} {c:>6,}")
    print(f"\nTop units spawned:")
    for s, c in list(aggregate["all_units_spawned"].items())[:15]:
        print(f"  {s:<20s} {c:>6,}")


if __name__ == "__main__":
    main()
