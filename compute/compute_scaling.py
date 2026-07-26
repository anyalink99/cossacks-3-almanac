"""Compute per-Nth building/unit prices using the costpercent scaling formula.

Source of formula: unit.script:5650-5689 (`_unit_GetCostByID`).

    costmodifier = pow(costpercent / 100, count)        # count = number already built/owned
    final_price[res] = floor(base_price[res] * costmodifier)

Special cases (from same function):
- if costpercent in {0, 100} -> no scaling (modifier stays 1)
- bmercenary units: count includes the paired merc (archerdip<->archerturdip,
  dragoon18dip<->lightcavalrydip), and modifier is capped at 2
- non-mercenary: modifier capped at 20000

Counter source (unit.script:3847, 3969): `gPlayer[pl].counter.all[cid][id]` is
incremented on creation and decremented on death/destruction, so destroying a
town center actually makes the next one cheaper again.

This script reads the already-extracted base prices from data.json and writes:
- docs/reports/economy/scaling_prices.md (grouped by building suffix)

Re-run it whenever the base data is regenerated.
"""

import sys
import json
from collections import defaultdict
from math import floor, pow
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "parser"))
from citations import Citations
from config import (PLAYABLE_NATIONS, DATA_JSON, REPORTS_DIR,
                    REPORTS_ECONOMY_DIR, nation_ru)

# Module-level citations registry — populated by header_block(), drained by write_md().
cites = Citations()

DATA_PATH = DATA_JSON
MD_PATH = REPORTS_ECONOMY_DIR / "scaling_prices.md"

MAX_N = 6
RES_KEYS = ("food", "wood", "stone", "gold", "iron", "coal")
RES_LETTER = {"food": "Е", "wood": "Д", "stone": "К",
              "gold": "З", "iron": "Ж", "coal": "У"}

# Per-nation building suffix categories — ordered for output.
PER_NAT_SUF = [
    ("cen", "Городской центр"),
    ("hou", "Дом"),
    ("bar", "Казарма 17 в."),
    ("ba2", "Казарма 18 в."),
    ("bla", "Кузница"),
    ("sta", "Конюшня"),
    ("tem", "Собор"),
    ("aca", "Академия"),
    ("art", "Артиллерийское депо"),
    ("dip", "Дипломатический центр"),
]
COMMON_SUF = [
    ("mil", "Мельница"),
    ("sto", "Склад"),
    ("mar", "Рынок"),
    ("por", "Порт"),
    ("tow", "Башня"),
    ("gol", "Золотая шахта"),
    ("iro", "Железная шахта"),
    ("coa", "Угольная шахта"),
    ("swa", "Каменная стена"),
    ("sga", "Каменные ворота"),
    ("wga", "Деревянные ворота"),
    ("wwa", "Палисад"),
]


def modifier(costpercent: int | float | None, n: int) -> float:
    """Return the cost multiplier for the Nth instance (N is 1-indexed)."""
    if costpercent is None:
        return 1.0
    cp = float(costpercent)
    if cp == 0 or cp == 100:
        return 1.0
    raw = pow(cp / 100.0, n - 1)
    # Non-mercenary cap (for mercenaries we'd cap at 2; this script handles
    # buildings where the merc rule does not apply).
    if raw > 20000:
        raw = 20000.0
    return raw


def price_for_n(b: dict, n: int) -> dict:
    """Compute integer prices for the Nth instance. Uses floor() per resource."""
    m = modifier(b.get("costpercent"), n)
    out = {}
    for k in RES_KEYS:
        base = b.get(k) or 0
        out[k] = floor(base * m) if base else 0
    return out


def name_ru_en(item: dict) -> str:
    """Russian name from locale, fallback to English, fallback to em-dash."""
    ru = (item.get("name_ru") or "").strip()
    en = (item.get("name_en") or "").strip()
    return ru or en or "—"


def fmt_cost(prices: dict) -> str:
    parts = [f"{RES_LETTER[k]}{v}" for k, v in prices.items() if v]
    return " ".join(parts) if parts else "—"


def note_for(b: dict) -> str:
    cp = b.get("costpercent") or 0
    if cp == 0 or cp == 100:
        return "цена постоянна"
    mult = cp / 100.0
    if mult == int(mult):
        return f"×{int(mult)} за каждый уже построенный"
    return f"×{mult:g} за каждый уже построенный"


def header_block() -> list[str]:
    """Lines for the explanatory header common to md output."""
    L = []
    L.append("# Цена каждого следующего здания")
    L.append("")
    L.append("[← Таблицы и расчёты](../README.md)")
    L.append("")
    L.append("Многие здания дорожают с каждым уже построенным экземпляром. "
             "Здесь показана цена первых шести зданий одного типа.")
    L.append("")
    L.append("## Формула")
    L.append("")
    formula_cite = cites.cite("lib/unit.script:5650-5689",
                              label="`_unit_GetCostByID` — расчёт цены N-го экземпляра")
    L.append(f"Цена умножается на коэффициент здания за каждый уже построенный "
             f"экземпляр {formula_cite}:")
    L.append("")
    L.append("```text")
    L.append("цена следующего = базовая цена × коэффициент ^ число построенных")
    L.append("```")
    L.append("")
    inc_cite = cites.cite("lib/unit.script:3847",
                          label="инкремент `counter.all[cid][unitID]` при создании")
    dec_cite = cites.cite("lib/unit.script:3969",
                          label="декремент `counter.all[cid][unitID]` при разрушении")
    L.append(f"Счётчик увеличивается при создании {inc_cite} и уменьшается при "
             f"разрушении {dec_cite}. Поэтому после потери городского центра "
             f"следующий центр снова становится дешевле.")
    L.append("")
    L.append("## Особые случаи")
    L.append("")
    L.append("- Если коэффициент равен единице, цена остаётся постоянной.")
    L.append("- Каждый ресурс округляется вниз отдельно, поэтому небольшой рост "
             "иногда происходит ступенями.")
    L.append("- В таблице перечислены только здания. Для наёмников действуют "
             "отдельные правила и предел удвоенной базовой цены.")
    L.append("")
    L.append(f"## Как читать таблицы")
    L.append("")
    L.append("«1-е» — цена первого экземпляра, «2-е» — второго и так далее. "
             "Ресурсы сокращены: Е — еда, Д — дерево, К — камень, З — золото, "
             "Ж — железо, У — уголь.")
    L.append("")
    return L


def section_md(title: str, rows: list[dict], show_nation: bool, lines: list[str]):
    """Append one section table to lines list. rows is a list of building dicts."""
    if not rows:
        return
    A = lines.append
    A(f"### {title}")
    A("")
    if show_nation:
        head = ["Нация", "Здание", "Код", "Коэффициент, %"] + [
            f"{i}-е" for i in range(1, MAX_N+1)
        ] + ["Примечание"]
    else:
        head = ["Здание", "Код", "Используют нации", "Коэффициент, %"] + [
            f"{i}-е" for i in range(1, MAX_N+1)
        ] + ["Примечание"]
    A("| " + " | ".join(head) + " |")
    align = ["---"] * len(head)
    align[3] = "---:"  # cost%
    for i in range(4, 4 + MAX_N):
        align[i] = "---"
    A("| " + " | ".join(align) + " |")
    if show_nation:
        for b in rows:
            cells = [
                nation_ru(b["nation"]),
                name_ru_en(b),
                f"`{b['sid']}`",
                str(b.get("costpercent") if b.get("costpercent") is not None else "—"),
            ]
            for n in range(1, MAX_N+1):
                cells.append(fmt_cost(price_for_n(b, n)))
            cells.append(note_for(b))
            A("| " + " | ".join(cells) + " |")
    else:
        for sid, group in rows:
            b = group[0]
            nats = ", ".join(nation_ru(nat) for nat in sorted(g["nation"] for g in group))
            cells = [
                name_ru_en(b),
                f"`{sid}`",
                nats,
                str(b.get("costpercent") if b.get("costpercent") is not None else "—"),
            ]
            for n in range(1, MAX_N+1):
                cells.append(fmt_cost(price_for_n(b, n)))
            cells.append(note_for(b))
            A("| " + " | ".join(cells) + " |")
    A("")


def write_md(data: dict):
    out: list[str] = header_block()
    A = out.append

    A("## Национальные варианты зданий")
    A("")
    A("Сгруппировано по типу здания, чтобы варианты всех 21 нации можно было "
      "сравнить рядом.")
    A("")

    by_suffix_per: dict[str, list[dict]] = defaultdict(list)
    for b in data["buildings"]:
        if b["kind"] != "per-nation":
            continue
        suf = b["sid"][len(b["nation"]):]
        by_suffix_per[suf].append(b)

    for suf, label in PER_NAT_SUF:
        rows = sorted(by_suffix_per.get(suf, []), key=lambda x: x["nation"])
        section_md(f"{label} (`{suf}`)",
                   rows, show_nation=True, lines=out)

    # Per-nation buildings not in our pretty list
    other_per = [s for s in by_suffix_per if s not in {x[0] for x in PER_NAT_SUF}]
    if other_per:
        for suf in sorted(other_per):
            rows = sorted(by_suffix_per[suf], key=lambda x: x["nation"])
            section_md(f"`{suf}` — (прочее)", rows, show_nation=True, lines=out)

    A("## Общие варианты зданий")
    A("")
    A("Некоторые варианты одинаковы сразу у нескольких наций. Эти нации "
      "перечислены в отдельном столбце.")
    A("")

    by_suffix_com: dict[str, dict[str, list[dict]]] = defaultdict(lambda: defaultdict(list))
    for b in data["buildings"]:
        if b["kind"] != "common":
            continue
        suf = b["sid"][3:]   # cluster prefix is always 3 letters
        by_suffix_com[suf][b["sid"]].append(b)

    for suf, label in COMMON_SUF:
        groups = by_suffix_com.get(suf, {})
        if not groups:
            continue
        rows = sorted(groups.items())
        section_md(f"{label} (`{suf}`)",
                   rows, show_nation=False, lines=out)

    other_com = [s for s in by_suffix_com if s not in {x[0] for x in COMMON_SUF}]
    if other_com:
        for suf in sorted(other_com):
            rows = sorted(by_suffix_com[suf].items())
            section_md(f"`{suf}` — (прочее)", rows, show_nation=False, lines=out)

    out.extend(cites.render())
    MD_PATH.write_text("\n".join(out), encoding="utf-8")
    print(f"Wrote {MD_PATH} ({MD_PATH.stat().st_size:,} bytes, {len(out):,} lines)")


def main():
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    MD_PATH.parent.mkdir(parents=True, exist_ok=True)
    write_md(data)
    # xlsx output dropped — md is the canonical format. The write_xlsx() function
    # is kept in this file for reference but no longer invoked from main().


if __name__ == "__main__":
    main()
