"""Per-nation efficiency upgrade table.

Surfaces every upgrade that touches resource extraction (`effectfood`/`effectwood`/
`effectstone` and their `perc` siblings) plus the field-HP modifier (`fieldlifeperc`),
sums them per nation, and tabulates the chain. Result feeds strategy decisions like
"how much food efficiency can rus actually stack vs aus" and "what's the cheapest
path to +200% wood for ven".

The values are **additive** to a base of 100 — see `_player_ApplyUpgrade` in
player.script:1812+. So `value: 40` means "+40% to that resource's efficiency".

Output: docs/reports/economy/efficiency_upgrades.md
"""
from __future__ import annotations
import sys
import json
from collections import defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "parser"))
from config import (PLAYABLE_NATIONS, DATA_JSON, REPORTS_DIR, REPORTS_ECONOMY_DIR,
                    nation_label, nation_ru)


MD_PATH = REPORTS_ECONOMY_DIR / "efficiency_upgrades.md"

# Group `effectfood` and `effectfoodperc` together — they apply the same way
# (additive to resefficiency[food]), the `perc` suffix is historical naming.
ITYPE_TO_BUCKET = {
    "gc_upg_type_effectfood":      "food",
    "gc_upg_type_effectfoodperc":  "food",
    "gc_upg_type_effectwood":      "wood",
    "gc_upg_type_effectwoodperc":  "wood",
    "gc_upg_type_effectstone":     "stone",
    "gc_upg_type_effectstoneperc": "stone",
    "gc_upg_type_fieldlifeperc":   "fieldlife",
}

BUCKET_ORDER = ["food", "wood", "stone", "fieldlife"]
BUCKET_LABEL = {
    "food":      "Эффективность еды",
    "wood":      "Эффективность дерева",
    "stone":     "Эффективность камня",
    "fieldlife": "HP полей (fieldlife)",
}

RES_LETTER = {"food": "F", "wood": "W", "stone": "S",
              "gold": "G", "iron": "I", "coal": "C"}


def fmt_cost(u: dict) -> str:
    parts = []
    for k in ("food", "wood", "stone", "gold", "iron", "coal"):
        v = u.get(k) or 0
        if v:
            parts.append(f"{RES_LETTER[k]}{v}")
    return " ".join(parts) if parts else "—"


def collect(data: dict) -> dict:
    """Returns:
    {
        nation: {
            bucket: [ {sid, level, value, time_sec, food, wood, ..., name_en} sorted by level/sid ]
        }
    }
    """
    out: dict[str, dict[str, list]] = defaultdict(lambda: defaultdict(list))
    for u in data["upgrades"]:
        bucket = ITYPE_TO_BUCKET.get(u.get("itype") or "")
        if not bucket:
            continue
        nat = u.get("nation")
        if nat not in PLAYABLE_NATIONS:
            continue
        out[nat][bucket].append(u)
    # Sort each chain by sid (which encodes both building suffix and level)
    for nat, by_bucket in out.items():
        for bucket, rows in by_bucket.items():
            rows.sort(key=lambda r: (r.get("sid") or "", r.get("level") or 0))
    return out


def summarize_peaks(by_bucket: dict) -> dict:
    """Per-bucket: max single value and sum of all values (the achievable cap)."""
    res = {}
    for bucket in BUCKET_ORDER:
        rows = by_bucket.get(bucket) or []
        total = sum(int(r.get("value") or 0) for r in rows)
        res[bucket] = {
            "count":   len(rows),
            "sum":     total,
            "max":     max((int(r.get("value") or 0) for r in rows), default=0),
        }
    return res


def render_md(by_nation: dict) -> str:
    L: list[str] = []
    A = L.append
    A("# Cossacks 3 — Efficiency upgrades per nation")
    A("")
    A("**Производный** файл (расчётный, не извлечение). Считается из "
      "`docs/data.json` скриптом "
      "[`compute/compute_efficiency_upgrades.py`](../../compute/compute_efficiency_upgrades.py).")
    A("")
    A("## Что это")
    A("")
    A("Каждый апгрейд `gc_upg_type_effect{food,wood,stone}[perc]` **аддитивно** "
      "прибавляет `value` к `resefficiency[res]` ([`player.script:1812+`]"
      "(<C:/Program Files (x86)/Steam/steamapps/common/Cossacks 3/data/scripts/lib/player.script>)).")
    A("База = 100. Формула добычи на удар: `delivered = floor(portion × eff / 100)`, "
      "где `portion` = 45/28/40 для food/wood/stone (`unit.script:9551-9555`).")
    A("")
    A("`gc_upg_type_fieldlifeperc` аддитивно прибавляет к `objbase.fieldlife` поля. "
      "Снижает урон/удар по полю на `100 / (1 + fieldlife/100)` — повышает выход "
      "за один цикл и уменьшает частоту перезапусков.")
    A("")
    A("## Сводка по нациям (кумулятивные пики)")
    A("")
    A("Сумма всех значений в линейке = пик для нации, если исследовать ВСЕ соответствующие "
      "апгрейды. На практике некоторые апгрейды эксклюзивны (один building с .1..6 "
      "ступенями), но скрипт суммирует всё — это **верхняя граница**.")
    A("")
    A("| Нация | food eff % | wood eff % | stone eff % | fieldlife % | Σ апгрейдов |")
    A("| --- | ---: | ---: | ---: | ---: | ---: |")
    nations_sorted = sorted(by_nation.keys())
    for nat in nations_sorted:
        peaks = summarize_peaks(by_nation[nat])
        food_sum = peaks["food"]["sum"]
        wood_sum = peaks["wood"]["sum"]
        stone_sum = peaks["stone"]["sum"]
        flife_sum = peaks["fieldlife"]["sum"]
        total_count = sum(peaks[b]["count"] for b in BUCKET_ORDER)
        A(f"| {nat} | +{food_sum} | +{wood_sum} | +{stone_sum} | +{flife_sum} | {total_count} |")
    A("")
    # Pretty: max-of-each highlighted in commentary
    A("**Лучшие пики по всем нациям:**")
    for bucket in BUCKET_ORDER:
        peaks = [(nat, summarize_peaks(by_nation[nat])[bucket]["sum"]) for nat in nations_sorted]
        max_val = max(p[1] for p in peaks)
        winners = [n for n, v in peaks if v == max_val]
        suffix = f" ({len(winners)} nations tied)" if len(winners) > 1 else ""
        names = ", ".join(winners) if len(winners) <= 5 else f"{', '.join(winners[:3])}, …"
        A(f"- {BUCKET_LABEL[bucket]}: **+{max_val}** — {names}{suffix}")
    A("")
    # Cheapest path to standard chain — useful for strategy.
    A("**Самая дешёвая прогрессия food-eff (суммарное золото за ВСЕ апгрейды food-eff):**")
    A("")
    A("| Нация | всего gold | всего food | всего wood |")
    A("| --- | ---: | ---: | ---: |")
    food_costs = []
    for nat in nations_sorted:
        rows = by_nation[nat].get("food") or []
        g = sum(int(r.get("gold") or 0) for r in rows)
        f = sum(int(r.get("food") or 0) for r in rows)
        w = sum(int(r.get("wood") or 0) for r in rows)
        food_costs.append((nat, g, f, w))
    food_costs.sort(key=lambda x: (x[1], x[2]))
    for nat, g, f, w in food_costs:
        A(f"| **{nat}** {nation_ru(nat)} | {g} | {f} | {w} |")
    A("")
    A("## Подробно по нациям")
    A("")
    A("Каждая ячейка cost — стоимость **этого** апгрейда (не суммарная).")
    A("")
    for nat in nations_sorted:
        A(f"### {nation_label(nat)}")
        A("")
        for bucket in BUCKET_ORDER:
            rows = by_nation[nat].get(bucket) or []
            if not rows:
                continue
            A(f"#### {BUCKET_LABEL[bucket]}")
            A("")
            A("| sid | lvl | +value | time (g-s) | cost | prereqs |")
            A("| --- | ---: | ---: | ---: | --- | --- |")
            for r in rows:
                sid = r.get("sid") or "—"
                lvl = r.get("level") if r.get("level") is not None else "—"
                val = r.get("value") if r.get("value") is not None else "—"
                t = r.get("time_sec") if r.get("time_sec") is not None else "—"
                cost = fmt_cost(r)
                prereqs = ", ".join(r.get("prereqs") or []) or "—"
                A(f"| `{sid}` | {lvl} | +{val} | {t} | {cost} | {prereqs} |")
            running = 0
            for r in rows:
                running += int(r.get("value") or 0)
            A("")
            A(f"_Кумулятивный пик: +{running}_")
            A("")
        A("")
    A("---")
    A("")
    A("Сгенерировано из `docs/data.json`. Для перегенерации:")
    A("")
    A("```")
    A("python compute/compute_efficiency_upgrades.py")
    A("```")
    return "\n".join(L)


def main():
    data = json.loads(DATA_JSON.read_text(encoding="utf-8"))
    by_nation = collect(data)
    MD_PATH.parent.mkdir(parents=True, exist_ok=True)
    md = render_md(by_nation)
    MD_PATH.write_text(md, encoding="utf-8")
    print(f"Wrote {MD_PATH} ({MD_PATH.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
