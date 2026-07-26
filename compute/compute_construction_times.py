"""Compute per-building construction time for different builder counts.

Output: docs/reports/economy/construction_times.md — table for every building showing:
- buildtime (1 builder, real game-sec)
- time with 2/5/10/cap builders
- repair time (full HP) with 1/cap builders

Formula (from recon/building_mechanics.md):
- 1 builder: buildtime_sec × 1.13
- N builders: buildtime_sec × 1.13 / N (clamped at slot_cap)
- Repair: maxhp / 49.3 g-sec per builder; full = maxhp / (49.3 × N)
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "parser"))
from config import (DATA_JSON, DERIVED_DIR, REPORTS_DIR, PEASANT_ANIM_SEC,
                    REPORTS_ECONOMY_DIR, nation_ru)

OUT_PATH = REPORTS_ECONOMY_DIR / "construction_times.md"
BUILDER_SLOTS_JSON = DERIVED_DIR / "builder_slots.json"

GAMESPEED_FAST = 1.4
ANIM_OVERHEAD = 1.13   # buildtime × 1.13 = time with 1 builder (anim cycle longer than progressperhit)
REPAIR_HP_PER_HIT = 20  # gc_gameplay_repairhp, dmscript.global:211
ANIM_CYCLE_SEC = PEASANT_ANIM_SEC["construct"]  # 13 frames / 32 = 0.406 g-sec, from peaaus.aaf


def name_ru_en(item: dict) -> str:
    ru = (item.get("name_ru") or "").strip()
    en = (item.get("name_en") or "").strip()
    return ru or en or "—"

# Slot caps come from a faithful simulation of `_unit_CalcBuilderPoints`
# (see compute/compute_builder_slots.py). Walls/gates without their own .prop
# fall back to wallcustom.cfg's straight-segment value.
SLOT_CAP_FALLBACK_WALL = 4    # straight wall segment in wallcustom.cfg
GC_MAX_BUILDER_COUNT = 30     # engine ceiling, gc_MaxBuilderCount

# N values to show in the table
BUILDER_COUNTS = [1, 2, 5, 10]

_SLOTS_CACHE: dict[str, int] | None = None


def _load_slots() -> dict[str, int]:
    global _SLOTS_CACHE
    if _SLOTS_CACHE is None:
        if BUILDER_SLOTS_JSON.exists():
            raw = json.loads(BUILDER_SLOTS_JSON.read_text(encoding="utf-8"))
            _SLOTS_CACHE = {sid: info["slots"] for sid, info in raw.items()}
        else:
            _SLOTS_CACHE = {}
    return _SLOTS_CACHE


def slot_cap_for(b: dict) -> int:
    sid = b.get("sid", "")
    slots = _load_slots()
    if sid in slots:
        return slots[sid]
    # Common-cluster building? Try the cluster prefix variants.
    for prefix in ("eur", "rus", "ukr", "tur", "spa", "por"):
        if slots.get(prefix + sid[3:]) is not None:
            return slots[prefix + sid[3:]]
    # Wall/gate sids that don't appear directly (engine generates them at runtime
    # from wallcustom.cfg variations).
    if any(sid.endswith(s) for s in ("swa", "sga", "wga", "wwa")):
        return SLOT_CAP_FALLBACK_WALL
    # Unknown building — use engine ceiling (no silent under-estimate).
    return GC_MAX_BUILDER_COUNT


def build_time_g_sec(buildtime_sec: float, n_builders: int, cap: int) -> float:
    """Time with N builders (game-time seconds), formula from construct.inc."""
    n = min(n_builders, cap)
    return buildtime_sec * ANIM_OVERHEAD / n


def repair_time_g_sec(maxhp: int, n_builders: int, cap: int) -> float:
    """Time to fully repair (game-sec). maxhp / (REPAIR_HP_PER_HIT × N / ANIM_CYCLE_SEC)."""
    n = min(n_builders, cap)
    repair_rate = REPAIR_HP_PER_HIT * n / ANIM_CYCLE_SEC  # HP/g-sec
    return maxhp / repair_rate


def fmt_time(sec: float) -> str:
    """Format game time with its real-time equivalent on Fast speed."""
    real = sec / GAMESPEED_FAST
    if sec >= 60:
        return f"{sec/60:.1f} мин. игр. ({real/60:.1f} мин. реал.)"
    return f"{sec:.0f} с игр. ({real:.0f} с реал.)"


def main():
    data = json.loads(DATA_JSON.read_text(encoding="utf-8"))
    nations = sorted(set(b["nation"] for b in data["buildings"]))

    L = []
    L.append("# Время строительства и ремонта")
    L.append("")
    L.append("[← Таблицы и расчёты](../README.md)")
    L.append("")
    L.append("Сколько занимает строительство нового здания и полный ремонт "
             "с разным числом крестьян. В скобках дано реальное время на "
             "скорости «Быстро».")
    L.append("")
    L.append("Время почти обратно пропорционально числу работников, но у каждого "
             "здания есть предел крестьян, которые могут работать одновременно. "
             "Этот предел указан в столбце «Максимум строителей».")
    L.append("")
    L.append("Почему предел различается и как он рассчитан, объяснено в "
             "[отдельной таблице строителей](builder_slots.md). Подробная формула — "
             "в статье [о строительстве и ремонте](../../recon/world/economy/building_mechanics.md).")
    L.append("")

    for nat in nations:
        L.append(f"## {nation_ru(nat)} (`{nat}`)")
        L.append("")
        L.append("### Постройка с нуля")
        L.append("")
        head = ["Здание", "Код", "Базовое время", "Максимум строителей"] + [
            f"{n} кр." for n in BUILDER_COUNTS
        ] + ["При максимуме"]
        L.append("| " + " | ".join(head) + " |")
        L.append("|" + "|".join(["---"] * len(head)) + "|")
        for b in sorted([b for b in data["buildings"] if b["nation"] == nat],
                         key=lambda x: x["sid"]):
            bt = b.get("buildtime_sec")
            if not bt:
                continue
            cap = slot_cap_for(b)
            cells = [
                name_ru_en(b),
                f"`{b['sid']}`",
                f"{bt:.0f} игровых секунд",
                str(cap),
            ]
            for n in BUILDER_COUNTS:
                cells.append(fmt_time(build_time_g_sec(bt, n, cap)))
            cells.append(fmt_time(build_time_g_sec(bt, cap, cap)))
            L.append("| " + " | ".join(cells) + " |")
        L.append("")

        L.append("### Полный ремонт")
        L.append("")
        head = ["Здание", "Код", "Здоровье", "Максимум ремонтников"] + [
            f"{n} кр." for n in BUILDER_COUNTS
        ] + ["При максимуме"]
        L.append("| " + " | ".join(head) + " |")
        L.append("|" + "|".join(["---"] * len(head)) + "|")
        for b in sorted([b for b in data["buildings"] if b["nation"] == nat],
                         key=lambda x: x["sid"]):
            hp = b.get("hp")
            if not hp:
                continue
            cap = slot_cap_for(b)
            cells = [
                name_ru_en(b),
                f"`{b['sid']}`",
                f"{hp}",
                str(cap),
            ]
            for n in BUILDER_COUNTS:
                cells.append(fmt_time(repair_time_g_sec(hp, n, cap)))
            cells.append(fmt_time(repair_time_g_sec(hp, cap, cap)))
            L.append("| " + " | ".join(cells) + " |")
        L.append("")

    OUT_PATH.write_text("\n".join(L), encoding="utf-8")
    print(f"Wrote {OUT_PATH} ({OUT_PATH.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
