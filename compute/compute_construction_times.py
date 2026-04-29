"""Compute per-building construction time for different builder counts.

Output: output/reports/construction_times.md — table for every building showing:
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
from config import DATA_JSON, DERIVED_DIR, REPORTS_DIR, PEASANT_ANIM_SEC

OUT_PATH = REPORTS_DIR / "construction_times.md"
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
    """Format game-time seconds as 'Ng (Nr fast)'."""
    real = sec / GAMESPEED_FAST
    if sec >= 60:
        return f"{sec/60:.1f}m g ({real/60:.1f}m r)"
    return f"{sec:.0f}g ({real:.0f}r)"


def main():
    data = json.loads(DATA_JSON.read_text(encoding="utf-8"))
    nations = sorted(set(b["nation"] for b in data["buildings"]))

    L = []
    L.append("# Cossacks 3 — Время постройки и ремонта")
    L.append("")
    L.append("Время постройки (с нуля, новое здание) и ремонта (полностью повреждённое → полное HP) "
             "для каждого здания. Считается для разного числа крестьян.")
    L.append("")
    L.append("**Формулы** (см. [`recon/building_mechanics.md`](../../recon/building_mechanics.md)):")
    L.append("")
    L.append("- **Постройка**, время с N крестьянами: `buildtime_sec × 1.13 / N` (ограничено slot cap)")
    L.append("- **Ремонт**, время с N крестьянами: `maxhp / (20 × N / 0.406)` g-sec")
    L.append("- 1 цикл анимации construct = 13 frames / 32 fps = **0.406 g-sec**")
    L.append(f"- При скорости fast: real-time = g-sec / {GAMESPEED_FAST}")
    L.append("")
    L.append("**Slot caps** (точная симуляция `_unit_CalcBuilderPoints` для каждого здания, "
             "см. [`builder_slots.md`](builder_slots.md)):")
    L.append("")
    L.append("- Cap зависит от **периметра collision mask** конкретного здания — у разных "
             "наций одна и та же категория (например, казарма 18 века) может иметь от 19 до 30 слотов.")
    L.append(f"- Walls/gates: **{SLOT_CAP_FALLBACK_WALL}** слотов на сегмент (значение из "
             "`wallcustom.cfg`, для sid'ов, отсутствующих в `builder_slots.json`).")
    L.append("- Жёсткий лимит движка: `gc_MaxBuilderCount = 30`.")
    L.append("")
    L.append("**Колонки:** время в формате `<g-sec>g (<real-sec>r fast)`. Для длительных значений — в минутах.")
    L.append("")

    for nat in nations:
        L.append(f"## {nat}")
        L.append("")
        L.append("### Постройка с нуля")
        L.append("")
        head = ["sid", "имя", "buildtime_g", "slot_cap"] + [f"{n} строит." for n in BUILDER_COUNTS] + ["макс. строит."]
        L.append("| " + " | ".join(head) + " |")
        L.append("|" + "|".join(["---"] * len(head)) + "|")
        for b in sorted([b for b in data["buildings"] if b["nation"] == nat],
                         key=lambda x: x["sid"]):
            bt = b.get("buildtime_sec")
            if not bt:
                continue
            cap = slot_cap_for(b)
            cells = [
                f"`{b['sid']}`",
                name_ru_en(b),
                f"{bt:.0f}g",
                str(cap),
            ]
            for n in BUILDER_COUNTS:
                cells.append(fmt_time(build_time_g_sec(bt, n, cap)))
            cells.append(fmt_time(build_time_g_sec(bt, cap, cap)))
            L.append("| " + " | ".join(cells) + " |")
        L.append("")

        L.append("### Полный ремонт (0 → max HP)")
        L.append("")
        head = ["sid", "имя", "maxhp", "slot_cap"] + [f"{n} строит." for n in BUILDER_COUNTS] + ["макс. строит."]
        L.append("| " + " | ".join(head) + " |")
        L.append("|" + "|".join(["---"] * len(head)) + "|")
        for b in sorted([b for b in data["buildings"] if b["nation"] == nat],
                         key=lambda x: x["sid"]):
            hp = b.get("hp")
            if not hp:
                continue
            cap = slot_cap_for(b)
            cells = [
                f"`{b['sid']}`",
                name_ru_en(b),
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
