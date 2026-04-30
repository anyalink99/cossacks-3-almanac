"""Single-command pipeline runner — works on any OS with Python 3.11+.

Usage:
    python scripts/regen.py            # full pipeline
    python scripts/regen.py reference  # only reference chapters
    python scripts/regen.py reports    # only derived reports
    python scripts/regen.py help       # list targets

Mirrors the Makefile targets so contributors without `make` (typical on Windows)
can run any subset.
"""
from __future__ import annotations
import subprocess
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
PY = sys.executable


def run(*args: str) -> None:
    cmd = [PY, *args]
    print(f"$ {' '.join(args)}", flush=True)
    t0 = time.time()
    r = subprocess.run(cmd, cwd=ROOT)
    dt = time.time() - t0
    if r.returncode != 0:
        print(f"FAILED ({dt:.1f}s) — exit {r.returncode}", flush=True)
        sys.exit(r.returncode)
    print(f"  ok ({dt:.1f}s)\n", flush=True)


# Targets are pure shell-callable: a list of argv-tails, each launched via `python <tail>`.

TARGETS: dict[str, list[list[str]]] = {

    "data": [
        ["parser/build_data.py"],
        ["parser/parse_generator_cfg.py"],
    ],

    "reference": [
        ["writers/write_md_tree.py"],
        ["writers/write_md.py"],
        ["writers/write_xlsx.py"],
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
        ["compute/compute_map_resources.py"],
        ["compute/extract_starting_layout.py"],
        ["compute/validate_map_predictions.py"],
    ],

    "reports-nations": [
        ["compute/compute_nations_overview.py"],
    ],

    "tech": [
        ["compute/build_tech_tree.py"],
    ],

    "derived": [
        ["compute/compute_animations.py"],
        ["compute/compute_pattern_inventory.py"],
        ["compute/compute_replay_aggregates.py"],
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
    args = sys.argv[1:] or ["all"]
    if any(a in ("help", "-h", "--help") for a in args):
        print(help_text())
        return
    t0 = time.time()
    for name in args:
        for tail in expand(name):
            run(*tail)
    print(f"== done ({time.time() - t0:.1f}s total) ==")


if __name__ == "__main__":
    main()
