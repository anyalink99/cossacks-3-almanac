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
from config import PLAYABLE_NATIONS, DATA_JSON, REPORTS_DIR, REPORTS_ECONOMY_DIR

# Module-level citations registry — populated by header_block(), drained by write_md().
cites = Citations()

DATA_PATH = DATA_JSON
MD_PATH = REPORTS_ECONOMY_DIR / "scaling_prices.md"

MAX_N = 6
RES_KEYS = ("food", "wood", "stone", "gold", "iron", "coal")
RES_LETTER = {"food": "F", "wood": "W", "stone": "S",
              "gold": "G", "iron": "I", "coal": "C"}

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
        return "не масштабируется (`costpercent` = 0/100)"
    mult = cp / 100.0
    if mult == int(mult):
        return f"×{int(mult)} за каждый уже построенный"
    return f"×{mult:g} за каждый уже построенный"


def header_block() -> list[str]:
    """Lines for the explanatory header common to md output."""
    L = []
    L.append("# Cossacks 3 — Цены зданий по N-му экземпляру")
    L.append("")
    L.append("**Производный** файл (расчётный, не извлечение). Считается из "
             "`data.json` скриптом "
             "[`compute/compute_scaling.py`](../../compute/compute_scaling.py).")
    L.append("")
    L.append("## Формула")
    L.append("")
    formula_cite = cites.cite("lib/unit.script:5650-5689",
                              label="`_unit_GetCostByID` — расчёт цены N-го экземпляра")
    L.append(f"Расчёт цены — в `_unit_GetCostByID` {formula_cite}:")
    L.append("")
    L.append("```")
    L.append("costmodifier   = pow(costpercent / 100, count)         // count = уже у игрока")
    L.append("final_price[r] = floor(base_price[r] * costmodifier)   // отдельно для F/W/S/G/I/C")
    L.append("```")
    L.append("")
    inc_cite = cites.cite("lib/unit.script:3847",
                          label="инкремент `counter.all[cid][unitID]` при создании")
    dec_cite = cites.cite("lib/unit.script:3969",
                          label="декремент `counter.all[cid][unitID]` при разрушении")
    L.append(f"Где `count` — это `gPlayer[plInd].counter.all[cid][unitID]`. "
             f"Счётчик инкрементируется при создании {inc_cite} и **декрементируется** "
             f"при разрушении {dec_cite} — снесли центр, следующий снова дешевле.")
    L.append("")
    L.append("## Особые случаи")
    L.append("")
    L.append("- `costpercent = 0` или `100` → масштабирования нет, цена постоянная.")
    L.append("- Для **наёмников** (`bmercenary=True`) счётчик объединяется с парным юнитом "
             "(`archerdip ↔ archerturdip`, `dragoon18dip ↔ lightcavalrydip`), и модификатор "
             "ограничен сверху значением **×2**. В этой таблице наёмников нет — только здания.")
    L.append("- Для не-наёмников модификатор ограничен сверху значением **×20000**. "
             "На N≤6 этот предел никогда не срабатывает (даже у казарм с `costpercent=500`: "
             "5⁵ = 3125 < 20000).")
    L.append("- **Округление вниз (floor)** для каждого ресурса независимо. Для дорогих зданий с "
             "`costpercent=104` это даёт ступенчатый рост, а не плавный.")
    L.append("")
    L.append(f"## Колонки N=1..{MAX_N}")
    L.append("")
    L.append("`N=1` — стоимость **первого** экземпляра (count=0, модификатор=1, цена = базовая). "
             "`N=2` — второго (count=1) и т.д. Каждая ячейка — суммарная стоимость в формате "
             "`F<food> W<wood> S<stone> G<gold> I<iron> C<coal>` (нулевые ресурсы скрыты).")
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
        head = ["Нация", "sid", "Имя", "cost%"] + [f"N={i}" for i in range(1, MAX_N+1)] + ["Примечание"]
    else:
        head = ["sid", "Используют нации", "Имя", "cost%"] + [f"N={i}" for i in range(1, MAX_N+1)] + ["Примечание"]
    A("| " + " | ".join(head) + " |")
    align = ["---"] * len(head)
    align[3] = "---:"  # cost%
    for i in range(4, 4 + MAX_N):
        align[i] = "---"
    A("| " + " | ".join(align) + " |")
    if show_nation:
        for b in rows:
            cells = [
                b["nation"],
                f"`{b['sid']}`",
                name_ru_en(b),
                str(b.get("costpercent") if b.get("costpercent") is not None else "—"),
            ]
            for n in range(1, MAX_N+1):
                cells.append(fmt_cost(price_for_n(b, n)))
            cells.append(note_for(b))
            A("| " + " | ".join(cells) + " |")
    else:
        for sid, group in rows:
            b = group[0]
            nats = ", ".join(sorted(g["nation"] for g in group))
            cells = [
                f"`{sid}`",
                nats,
                name_ru_en(b),
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

    A("## 1. Постройки по нациям")
    A("")
    A("Каждая нация имеет свой набор. sid формируется как `<nat><suffix>`. "
      "Сгруппировано по типу здания, все 21 нация в одной таблице на тип.")
    A("")

    by_suffix_per: dict[str, list[dict]] = defaultdict(list)
    for b in data["buildings"]:
        if b["kind"] != "per-nation":
            continue
        suf = b["sid"][len(b["nation"]):]
        by_suffix_per[suf].append(b)

    for suf, label in PER_NAT_SUF:
        rows = sorted(by_suffix_per.get(suf, []), key=lambda x: x["nation"])
        section_md(f"1.{PER_NAT_SUF.index((suf, label))+1} `{suf}` — {label}",
                   rows, show_nation=True, lines=out)

    # Per-nation buildings not in our pretty list
    other_per = [s for s in by_suffix_per if s not in {x[0] for x in PER_NAT_SUF}]
    if other_per:
        for suf in sorted(other_per):
            rows = sorted(by_suffix_per[suf], key=lambda x: x["nation"])
            section_md(f"`{suf}` — (прочее)", rows, show_nation=True, lines=out)

    A("## 2. Общие постройки (по кластерам)")
    A("")
    A("sid формируется как `<cluster><suffix>` — общий для группы наций. "
      "Один sid обычно используется несколькими нациями — они перечислены в столбце.")
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
        section_md(f"2.{COMMON_SUF.index((suf, label))+1} `{suf}` — {label}",
                   rows, show_nation=False, lines=out)

    other_com = [s for s in by_suffix_com if s not in {x[0] for x in COMMON_SUF}]
    if other_com:
        for suf in sorted(other_com):
            rows = sorted(by_suffix_com[suf].items())
            section_md(f"`{suf}` — (прочее)", rows, show_nation=False, lines=out)

    out.extend(cites.render())
    # Footer with derivation note
    A("---")
    A("")
    A("Сгенерировано из `data.json`. Для перегенерации:")
    A("")
    A("```")
    A("python compute/compute_scaling.py")
    A("```")

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
