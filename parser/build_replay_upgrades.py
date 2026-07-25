"""Build the compact upgrade catalog consumed by the replay parser.

The full ``data.json`` is several megabytes and contains combat, economy and
technology-tree fields that replay decoding never reads. This generator keeps
only the ordered per-nation upgrade metadata needed to resolve replay indices.

Usage:
    python parser/build_replay_upgrades.py
"""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "data.json"
OUTPUT = ROOT / "derived" / "replay_upgrades.json"
FIELDS = ("sid", "name_ru", "name_en", "place")


def build_catalog(data: dict) -> dict:
    upgrades_by_nation: dict[str, list[dict]] = {}
    for upgrade in data.get("upgrades", []):
        nation = upgrade.get("nation")
        if not nation:
            raise ValueError(f"upgrade without nation: {upgrade.get('sid')!r}")
        upgrades_by_nation.setdefault(nation, []).append({
            field: upgrade.get(field)
            for field in FIELDS
        })

    return {
        "_meta": {
            "schema_version": 1,
            "source": "data.json",
            "upgrade_count": sum(map(len, upgrades_by_nation.values())),
            "nation_count": len(upgrades_by_nation),
        },
        "upgrades_by_nation": upgrades_by_nation,
    }


def main() -> None:
    data = json.loads(SOURCE.read_text(encoding="utf-8"))
    catalog = build_catalog(data)
    OUTPUT.write_text(
        json.dumps(catalog, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        f"Wrote {OUTPUT.relative_to(ROOT)}: "
        f"{catalog['_meta']['upgrade_count']} upgrades, "
        f"{OUTPUT.stat().st_size / 1024:.0f} KiB"
    )


if __name__ == "__main__":
    main()
