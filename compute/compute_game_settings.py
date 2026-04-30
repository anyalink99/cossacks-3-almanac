"""Extract all lobby/game settings from dmscript.global + locale,
emit `docs/derived/game_settings.json` for the editor.

Source-of-truth for the *meaning* of each enum value: docs/recon/game_settings.md.
This script just dumps the structured data so the editor doesn't reinvent it.

Outputs `docs/derived/game_settings.json` with keys:
  - mapsize       — list of {value, tiles, label_en, label_ru}
  - terraintype   — list of {value, label_en, label_ru}
  - relieftype    — list of {value, label_en, label_ru}
  - resourcestart — list of {value, amount, label_en, label_ru}
  - resourcemines — list of {value, label_en, label_ru}
  - season        — list of {value, label_ru}     (no locale — handcrafted)
  - startingunits — list of {value, label_en, label_ru}
  - balloon       — list of {value, label_en, label_ru}
  - cannons       — list of {value, label_en, label_ru}
  - peacetime     — list of {value, minutes, gsec, label_en, label_ru}
  - century18     — list of {value, label_en, label_ru}
  - capture       — list of {value, label_en, label_ru}
  - marketdip     — list of {value, label_en, label_ru}
  - teams         — list of {value, label_en, label_ru}
  - limit         — list of {value, units, label_en, label_ru}
  - gamespeed     — list of {value, ticks_per_sec, factor, label_ru}
  - difficulty    — list of {value, label_ru, koef}
  - defaults      — {gen: {...}, additional: {...}} matching initmap.inc
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "parser"))
from config import DM_GLOBAL, LOCALE, DERIVED_DIR
from parse_locale import parse_locale_file


def _loc(loc, key):
    v = loc.get(key, "")
    return v.split("\n", 1)[0].strip() if v else ""


def build_settings():
    en = parse_locale_file(LOCALE / "en" / "gui.txt")
    ru = parse_locale_file(LOCALE / "ru" / "gui.txt")

    def pair(key):
        return {"label_en": _loc(en, key), "label_ru": _loc(ru, key)}

    out = {}

    # ─── gen.mapsize (no locale, hardcoded) ────────────────────────────
    out["mapsize"] = [
        {"value": 0, "tiles": 320, "label_en": "Standard",  "label_ru": "Стандартная"},
        {"value": 1, "tiles": 480, "label_en": "Big",       "label_ru": "Большая"},
        {"value": 2, "tiles": 640, "label_en": "Huge",      "label_ru": "Огромная"},
        {"value": 3, "tiles": 256, "label_en": "Tiny",      "label_ru": "Маленькая"},
    ]

    # ─── gen.terraintype ───────────────────────────────────────────────
    out["terraintype"] = [
        {"value": v, **pair(f"randommap.terraintype.{v}")} for v in range(10)
    ]

    # ─── gen.relieftype ────────────────────────────────────────────────
    out["relieftype"] = [
        {"value": v, **pair(f"randommap.relieftype.{v}")} for v in range(6)
    ]

    # ─── gen.resourcestart ─────────────────────────────────────────────
    AMOUNTS = {0: 1000, 1: 4000, 2: 5000, 3: 1000000}
    out["resourcestart"] = [
        {"value": v, "amount": AMOUNTS[v], **pair(f"randommap.initialresources.{v}")}
        for v in range(4)
    ]

    # ─── gen.resourcemines ─────────────────────────────────────────────
    out["resourcemines"] = [
        {"value": v, **pair(f"randommap.minerals.{v}")} for v in range(3)
    ]

    # ─── gen.season ────────────────────────────────────────────────────
    out["season"] = [
        {"value": 0, "label_ru": "Лето",     "label_en": "Summer"},
        {"value": 1, "label_ru": "Осень",    "label_en": "Autumn"},
        {"value": 2, "label_ru": "Зима",     "label_en": "Winter"},
        {"value": 3, "label_ru": "Пустыня",  "label_en": "Desert"},
    ]

    # ─── additional.startingunits ──────────────────────────────────────
    SU_KEYS = [
        (0,  "default"),
        (1,  "armysmall"),
        (2,  "armymedium"),
        (3,  "armylarge"),
        (4,  "peasantslot"),
        (5,  "differentnations"),
        (6,  "towers"),
        (7,  "cannons"),
        (8,  "cannonsandhowitzers"),
        (9,  "barrack18"),
        (10, "barrack17"),
        (11, "village"),
        (12, "logcabins"),
        (13, "union"),
    ]
    # Russian fallbacks for keys missing in locale
    SU_RU_FALLBACK = {
        "barrack17": "Казарма 17 в.",
        "village":   "Деревня",
        "logcabins": "Срубы",
        "union":     "Уния",
    }
    out["startingunits"] = []
    for v, k in SU_KEYS:
        info = pair(f"randommap.settings.startingunits.{k}")
        if not info["label_ru"]:
            info["label_ru"] = SU_RU_FALLBACK.get(k, k)
        if not info["label_en"]:
            info["label_en"] = k.replace("_", " ").title()
        out["startingunits"].append({"value": v, **info})

    # ─── additional.balloon ────────────────────────────────────────────
    out["balloon"] = [
        {"value": 0, **pair("randommap.settings.balloon.default")},
        {"value": 1, **pair("randommap.settings.balloon.no")},
        {"value": 2, **pair("randommap.settings.balloon.with")},
    ]

    # ─── additional.cannons ────────────────────────────────────────────
    out["cannons"] = [
        {"value": 0, **pair("randommap.settings.cannons.default")},
        {"value": 1, **pair("randommap.settings.cannons.nocannonstowerswalls")},
        {"value": 2, **pair("randommap.settings.cannons.expensivecannons")},
    ]

    # ─── additional.peacetime ──────────────────────────────────────────
    PEACETIME_MIN = {0: 0, 1: 10, 2: 20, 3: 30, 4: 45, 5: 60, 6: 90, 7: 120, 8: 180, 9: 240, 11: 15}
    PEACETIME_LOC_KEY = {0: "default", 1: "10", 2: "20", 3: "30", 4: "45", 5: "60",
                         6: "90", 7: "120", 8: "180", 9: "240", 11: "15"}
    out["peacetime"] = []
    for v, key in PEACETIME_LOC_KEY.items():
        m = PEACETIME_MIN[v]
        info = pair(f"randommap.settings.peacetime.{key}")
        out["peacetime"].append({
            "value": v,
            "minutes_g": m,
            "gsec": m * 60,
            **info,
        })
    out["peacetime"].sort(key=lambda x: x["value"])

    # ─── additional.century18 ──────────────────────────────────────────
    out["century18"] = [
        {"value": 0, **pair("randommap.settings.century18.default")},
        {"value": 1, **pair("randommap.settings.century18.no")},
        {"value": 2, **pair("randommap.settings.century18.with")},
    ]

    # ─── additional.capture ────────────────────────────────────────────
    out["capture"] = [
        {"value": 0, **pair("randommap.settings.capture.default")},
        {"value": 1, **pair("randommap.settings.capture.nopeasants")},
        {"value": 2, **pair("randommap.settings.capture.nocenterspeasants")},
        {"value": 3, **pair("randommap.settings.capture.onlyartillery")},
    ]

    # ─── additional.marketdip ──────────────────────────────────────────
    MD_KEYS = ["default", "nodip", "nomarket", "noboth"]
    out["marketdip"] = [
        {"value": v, **pair(f"randommap.settings.marketdip.{k}")} for v, k in enumerate(MD_KEYS)
    ]
    # value 4 = expensivemercs (locale not always present — fallback)
    em = pair("randommap.settings.marketdip.expensivemercs")
    if not em["label_en"]: em["label_en"] = "Expensive Mercenaries"
    if not em["label_ru"]: em["label_ru"] = "Дорогие наёмники"
    out["marketdip"].append({"value": 4, **em})

    # ─── additional.teams ──────────────────────────────────────────────
    out["teams"] = [
        {"value": 0, **pair("randommap.settings.teams.default")},
        {"value": 1, **pair("randommap.settings.teams.nearby")},
    ]

    # ─── additional.limit ──────────────────────────────────────────────
    LIMIT_UNITS = {0: None, 1: 500, 2: 750, 3: 1000, 4: 1500, 5: 2200, 6: 3000, 7: 5000, 8: 8000}
    out["limit"] = []
    for v, units in LIMIT_UNITS.items():
        if v == 0:
            info = pair("randommap.settings.limit.default")
            label_en = info["label_en"] or "Map default"
            label_ru = info["label_ru"] or "Без явного лимита"
        else:
            label_en = f"{units} units"
            label_ru = f"{units} юнитов"
        out["limit"].append({"value": v, "units": units, "label_en": label_en, "label_ru": label_ru})

    # ─── additional.gamespeed ──────────────────────────────────────────
    out["gamespeed"] = [
        {"value": 0, "ticks_per_sec": 7,  "factor": 0.7, "label_ru": "Медленно",  "label_en": "Slow"},
        {"value": 1, "ticks_per_sec": 10, "factor": 1.0, "label_ru": "Нормально", "label_en": "Normal"},
        {"value": 2, "ticks_per_sec": 14, "factor": 1.4, "label_ru": "Быстро",    "label_en": "Fast"},
    ]

    # ─── additional.adviserassistant ───────────────────────────────────
    out["adviserassistant"] = [
        {"value": 0, **pair("randommap.settings.adviserassistant.default")},
        {"value": 1, **pair("randommap.settings.adviserassistant.without")},
    ]

    # ─── difficulty ────────────────────────────────────────────────────
    out["difficulty"] = [
        {"value": 0, "koef": 0.30, "label_ru": "Легко",       "label_en": "Easy"},
        {"value": 1, "koef": 0.50, "label_ru": "Нормально",   "label_en": "Normal"},
        {"value": 2, "koef": 0.75, "label_ru": "Сложно",      "label_en": "Hard"},
        {"value": 3, "koef": 1.00, "label_ru": "Очень сложно","label_en": "Very Hard"},
        {"value": 4, "koef": 1.25, "label_ru": "Невозможно",  "label_en": "Impossible"},
    ]

    # ─── defaults from initmap.inc:29-31 ───────────────────────────────
    out["defaults"] = {
        "gen": {
            "mapsize": 0,           # не задано в initmap.inc; default = stand. ?
            "terraintype": 0,       # Land
            "relieftype": 3,        # Highlands (initmap.inc:29)
            "resourcestart": 2,     # Thousands / 5000 (initmap.inc:30)
            "resourcemines": 1,     # Medium (initmap.inc:31)
            "season": 0,            # Summer
        },
        "additional": {
            "startingunits": 0,     # Default
            "balloon": 0,
            "cannons": 0,
            "peacetime": 0,         # No peace time
            "century18": 0,
            "capture": 0,
            "marketdip": 0,
            "teams": 0,
            "limit": 0,             # map default
            "gamespeed": 2,         # Fast
            "adviserassistant": 0,
        },
    }

    return out


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    settings = build_settings()
    out_path = DERIVED_DIR / "game_settings.json"
    DERIVED_DIR.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(settings, ensure_ascii=False, indent=2), encoding="utf-8")
    total = sum(len(v) for v in settings.values() if isinstance(v, list))
    print(f"Wrote {out_path} ({total} enum values across {len(settings) - 1} categories)")


if __name__ == "__main__":
    main()
