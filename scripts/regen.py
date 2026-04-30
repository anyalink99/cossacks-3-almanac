"""Single-command pipeline runner — works on any OS with Python 3.11+.

Usage:
    python scripts/regen.py             # full pipeline
    python scripts/regen.py reference   # only reference chapters
    python scripts/regen.py reports     # only derived reports
    python scripts/regen.py --serial    # disable parallelism within a target
    python scripts/regen.py help        # list targets

Each named target is a list of independent script invocations. When the
target has more than one script, they run **concurrently** (default), since
all reports / derived JSONs read from `docs/data.json` and don't write to
each other. Pass `--serial` to disable this if you're debugging.

Mirrors the Makefile targets so contributors without `make` (typical on
Windows) can run any subset.
"""
from __future__ import annotations
import argparse
import concurrent.futures as cf
import os
import subprocess
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
PY = sys.executable

# Targets that MUST run sequentially (output of one feeds input of another).
# All other targets fan out their scripts in parallel.
SEQUENTIAL_TARGETS = {"data", "tech", "simulations"}


def run_one(args: list[str], capture: bool) -> tuple[list[str], int, float, str]:
    """Invoke one script. Returns (args, returncode, elapsed_seconds, output)."""
    cmd = [PY, *args]
    t0 = time.time()
    if capture:
        r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
        out = (r.stdout or "") + (r.stderr or "")
    else:
        r = subprocess.run(cmd, cwd=ROOT)
        out = ""
    return args, r.returncode, time.time() - t0, out


def run_group(group: list[list[str]], parallel: bool) -> None:
    """Run a list of script invocations. If parallel, fan out via thread pool;
    otherwise run sequentially with live output."""
    if not parallel or len(group) <= 1:
        for args in group:
            print(f"$ {' '.join(args)}", flush=True)
            args, rc, dt, _ = run_one(args, capture=False)
            if rc != 0:
                print(f"FAILED ({dt:.1f}s) — exit {rc}", flush=True)
                sys.exit(rc)
            print(f"  ok ({dt:.1f}s)\n", flush=True)
        return
    # Parallel: capture each script's output so they don't interleave on stdout.
    print(f"# running {len(group)} scripts in parallel:", flush=True)
    for args in group:
        print(f"  $ {' '.join(args)}", flush=True)
    workers = min(len(group), os.cpu_count() or 4)
    with cf.ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(run_one, args, True) for args in group]
        for fut in cf.as_completed(futures):
            args, rc, dt, out = fut.result()
            if out.strip():
                print(out.rstrip(), flush=True)
            if rc != 0:
                print(f"FAILED ({' '.join(args)}, {dt:.1f}s) — exit {rc}", flush=True)
                sys.exit(rc)
            print(f"  ok ({' '.join(args)}, {dt:.1f}s)", flush=True)
    print()


# Targets are pure shell-callable: a list of argv-tails, each launched via `python <tail>`.

TARGETS: dict[str, list[list[str]]] = {

    "data": [
        ["parser/build_data.py"],
        ["parser/parse_generator_cfg.py"],
        ["parser/build_canonical_terms.py"],
        ["parser/build_tech_graph.py"],
    ],

    "reference": [
        ["writers/write_md_tree.py"],
    ],

    "reports-combat": [
        ["compute/compute_combat_stats.py"],
        ["compute/compute_counter_matrix.py"],
        ["compute/compute_attack_rates.py"],
        ["compute/compute_vision.py"],
    ],

    "reports-economy": [
        ["compute/compute_scaling.py"],
        ["compute/compute_efficiency_upgrades.py"],
        ["compute/compute_construction_times.py"],
        ["compute/compute_builder_slots.py"],
    ],

    "reports-map": [
        ["compute/compute_game_settings.py"],
        ["compute/compute_map_resources.py"],
        ["compute/compute_starting_layout.py"],
        ["compute/validate_map_predictions.py"],
    ],

    "reports-nations": [
        ["compute/compute_nations_overview.py"],
    ],

    "tech": [
        ["compute/compute_tech_tree.py"],
    ],

    "derived": [
        ["parser/parse_animations.py"],
        ["parser/parse_pattern_inventory.py"],
        ["parser/parse_replay_aggregates.py"],
        ["compute/compute_game_settings.py"],
    ],

    "simulations": [
        ["simulator/simulate_economy.py", "simulator/build_orders/bav_basic_5min.json"],
        ["simulator/simulate_economy.py", "simulator/build_orders/bav_with_fields.json"],
    ],
}

# Aggregate targets: order matters (data must come before reports/reference).
ALIASES: dict[str, list[str]] = {
    "reports": ["reports-combat", "reports-economy", "reports-map",
                "reports-nations", "tech"],
    "all":     ["data", "reference", "reports-combat", "reports-economy",
                "reports-map", "reports-nations", "tech", "derived",
                "simulations"],
}


def help_text() -> str:
    lines = ["Usage: python scripts/regen.py [target]", "", "Targets:"]
    for name in ["all", "data", "reference", "reports", "reports-combat",
                 "reports-economy", "reports-map", "reports-nations",
                 "tech", "derived", "simulations"]:
        descr = {
            "all":             "full regen (data + reference + reports + tech + derived + simulations)",
            "data":            "parser only (game scripts → docs/data.json)",
            "reference":       "writers (data.json → docs/reference/, legacy md, xlsx)",
            "reports":         "all derived reports",
            "reports-combat":  "docs/reports/combat/",
            "reports-economy": "docs/reports/economy/",
            "reports-map":     "docs/reports/map/",
            "reports-nations": "docs/reports/nations/",
            "tech":            "tech_tree.md + production_rates.md + tech_tree.json",
            "derived":         "animations, patterns, replay aggregates → docs/derived/",
            "simulations":     "run example build orders → docs/simulations/",
        }[name]
        lines.append(f"  {name:<18} {descr}")
    lines.append("")
    lines.append("Default target is `all`.")
    return "\n".join(lines)


def expand(name: str) -> list[list[str]]:
    if name in ALIASES:
        out: list[list[str]] = []
        for sub in ALIASES[name]:
            out.extend(expand(sub))
        return out
    if name in TARGETS:
        return TARGETS[name]
    raise SystemExit(f"unknown target: {name!r}\n\n{help_text()}")


def main() -> None:
    parser = argparse.ArgumentParser(prog="scripts/regen.py", add_help=False)
    parser.add_argument("targets", nargs="*", default=["all"])
    parser.add_argument("--serial", action="store_true",
                        help="run scripts within each target sequentially "
                             "(default: parallel where safe)")
    parser.add_argument("-h", "--help", action="store_true")
    args = parser.parse_args()

    if args.help or "help" in args.targets:
        print(help_text())
        return

    targets = args.targets or ["all"]
    t0 = time.time()
    for name in targets:
        # `data`, `tech`, `simulations` chain steps that depend on each other,
        # so always run them sequentially regardless of --serial.
        force_serial = name in SEQUENTIAL_TARGETS or args.serial
        # An alias (e.g. `all`) expands into a list of named targets; we run
        # them in order, but inside each named target the scripts can fan out.
        if name in ALIASES:
            for sub in ALIASES[name]:
                group = TARGETS[sub] if sub in TARGETS else expand(sub)
                run_group(group, parallel=not (sub in SEQUENTIAL_TARGETS or args.serial))
        else:
            run_group(expand(name), parallel=not force_serial)
    print(f"== done ({time.time() - t0:.1f}s total) ==")


if __name__ == "__main__":
    main()
