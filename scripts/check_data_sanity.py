"""Fail when one or more committed parser sanity checks do not pass."""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    data = json.loads((ROOT / "data.json").read_text(encoding="utf-8"))
    checks = data.get("sanity_checks", [])
    failed = [check for check in checks if not check.get("pass")]
    print(f"{len(checks) - len(failed)}/{len(checks)} passed")
    if failed:
        details = ", ".join(
            f"{check.get('category')}: {check.get('name')}"
            for check in failed[:10]
        )
        raise SystemExit(f"{len(failed)} sanity check(s) failed: {details}")


if __name__ == "__main__":
    main()
