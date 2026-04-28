"""Compute per-building construction time for different builder counts.

Output: output/strategy/construction_times.md — table for every building showing:
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
from config import DATA_JSON, STRATEGY_DIR

OUT_PATH = STRATEGY_DIR / "construction_times.md"

GAMESPEED_FAST = 1.4
ANIM_OVERHEAD = 1.13   # buildtime × 1.13 = time with 1 builder (anim cycle longer than progressperhit)
REPAIR_HP_PER_HIT = 20  # gc_gameplay_repairhp
ANIM_CYCLE_SEC = 13 / 32  # 13 frames at 32 fps for the construct cycle

# Conservative defaults for slot caps based on building footprint perimeter.
# For walls/gates: 4 slots per segment (from wallcustom.cfg, variation 1).
# For buildings: ~12 slots (from typical 12-cell-perimeter buildings).
SLOT_CAP_DEFAULT = 12
SLOT_CAP_WALL = 4
SLOT_CAP_TOWER = 8

# N values to show in the table
BUILDER_COUNTS = [1, 2, 5, 10]


def slot_cap_for(b: dict) -> int:
    sid = b.get("sid", "")
    if any(sid.endswith(s) for s in ("swa", "sga", "wga", "wwa")):
        return SLOT_CAP_WALL
    if sid.endswith("tow"):
        return SLOT_CAP_TOWER
    if sid.endswith("ba2") or sid.endswith("aca") or sid.endswith("cen") or sid.endswith("por"):
        return 16  # large buildings have more perimeter
    return SLOT_CAP_DEFAULT


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
    L.append("# Cossacks 3 — Construction & Repair Times")
    L.append("")
    L.append("Время постройки (с нуля, новое здание) и ремонта (полностью повреждённое → полное HP) "
             "для каждого здания. Считает с разным числом крестьян одновременно.")
    L.append("")
    L.append("**Формулы** (см. [`recon/building_mechanics.md`](../../recon/building_mechanics.md)):")
    L.append("")
    L.append("- **Постройка**, время с N крестьянами: `buildtime_sec × 1.13 / N` (clamp на slot cap)")
    L.append("- **Ремонт**, время с N крестьянами: `maxhp / (20 × N / 0.406)` g-sec")
    L.append("- 1 цикл construct анимации = 13 frames / 32 fps = **0.406 g-sec**")
    L.append(f"- @ fast game speed real-time = g-sec / {GAMESPEED_FAST}")
    L.append("")
    L.append("**Slot caps** (грубая оценка периметра collision mask, см. recon §3.2):")
    L.append("")
    L.append(f"- Walls/gates: **{SLOT_CAP_WALL}** slots per segment (явно заданы в `wallcustom.cfg`)")
    L.append(f"- Towers: **{SLOT_CAP_TOWER}** slots")
    L.append(f"- Большие здания (cen/aca/ba2/por): **16** slots")
    L.append(f"- Прочие: **{SLOT_CAP_DEFAULT}** slots")
    L.append("")
    L.append("Cap не из кода напрямую (там `_unit_CalcBuilderPoints` динамически "
             "обходит периметр), а оценка для практики. Hard cap движка: 30.")
    L.append("")
    L.append("**Колонки:** время в формате `<g-sec>g (<real-sec>r fast)`. Для длинных — в минутах.")
    L.append("")

    for nat in nations:
        L.append(f"## {nat}")
        L.append("")
        L.append("### Постройка с нуля")
        L.append("")
        head = ["sid", "имя", "buildtime_g", "slot_cap"] + [f"{n} builders" for n in BUILDER_COUNTS] + ["max builders"]
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
                (b.get("name_en") or "—")[:25],
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
        head = ["sid", "имя", "maxhp", "slot_cap"] + [f"{n} builders" for n in BUILDER_COUNTS] + ["max builders"]
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
                (b.get("name_en") or "—")[:25],
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
