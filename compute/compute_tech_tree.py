"""Render the tech-tree graph as Markdown reports.

Reads `derived/tech_tree.json` (built by `parser/build_tech_graph.py`)
and `data.json` (for production rates), emits two markdown files:

- `docs/reports/tech/tech_tree.md` — per-nation prerequisite tables +
  a Mermaid building dependency graph for one representative nation.
- `docs/reports/economy/production_rates.md` — per-building production
  speeds: how many units per game-minute and per real-minute @ fast.

Run after `parser/build_tech_graph.py`:
    python compute/compute_tech_tree.py
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "parser"))
from citations import Citations
from config import (DATA_JSON, DERIVED_DIR, REPORTS_ECONOMY_DIR,
                    REPORTS_TECH_DIR, nation_ru, unit_ru)

TREE_JSON = DERIVED_DIR / "tech_tree.json"
TREE_MD = REPORTS_TECH_DIR / "tech_tree.md"
RATES_MD = REPORTS_ECONOMY_DIR / "production_rates.md"

GAMESPEED_FAST = 1.4

# Russian short labels for building suffixes — used in the Mermaid graph
# (full locale names like "Городской центр" make node text wrap awkwardly).
SHORT_BLD_LABELS = {
    "cen": "Город. центр", "hou": "Дом",
    "bar": "Казарма 17",   "ba2": "Казарма 18",
    "bla": "Кузница",      "sta": "Конюшня",     "tem": "Собор",
    "aca": "Академия",     "art": "Артиллерийское депо", "dip": "Дипломатический центр",
    "mil": "Мельница",     "sto": "Склад",       "mar": "Рынок",
    "por": "Порт",         "tow": "Башня",
    "gol": "Золотая шахта", "iro": "Железная шахта", "coa": "Угольная шахта",
    "swa": "Стена",        "sga": "Кам. ворота",
    "wga": "Дер. ворота",  "wwa": "Палисад",
}


def heading_anchor(text: str) -> str:
    """GitHub-flavored anchor for a heading. Mirrors writers/write_md_tree.py."""
    s = text.lower()
    s = re.sub(r"[^\w\s\-]", "", s, flags=re.UNICODE)
    return s.replace(" ", "-")


def name_ru_en(item: dict) -> str:
    ru = (item.get("name_ru") or "").strip()
    en = (item.get("name_en") or "").strip()
    sid = str(item.get("sid") or "")
    return unit_ru(sid, ru or en or "—")


def _short_bld_label(sid: str, nat: str) -> str:
    """Pick a compact Mermaid label: locale short name when known, else sid."""
    suf = sid[len(nat):] if sid.startswith(nat) else (sid[3:] if len(sid) > 3 else sid)
    return SHORT_BLD_LABELS.get(suf, sid)


RESOURCE_LABELS = {
    "food": "Еда",
    "wood": "Дерево",
    "stone": "Камень",
    "gold": "Золото",
    "iron": "Железо",
    "coal": "Уголь",
}


def _fmt_cost(cost: dict) -> str:
    return ", ".join(
        f"{RESOURCE_LABELS.get(key, key)} {value}"
        for key, value in cost.items()
        if value
    ) or "—"


def _fmt_prereq(p: dict, labels: dict[str, str]) -> str:
    sid = p["sid"]
    kind = {"building": "здание", "unit": "юнит", "upgrade": "улучшение"}.get(
        p["kind"], "объект"
    )
    return f"{labels.get(sid, sid)} (`{sid}`, {kind})"


def render_buildings_mermaid(nat: str, nt: dict) -> list[str]:
    """Mermaid building-dependency graph for one nation.

    Buildings only (units / upgrades clutter the diagram). Edges go
    prereq → building. Includes only prereqs that are themselves buildings,
    so all nodes appear.
    """
    L: list[str] = ["```mermaid", "graph LR"]
    bld_sids = sorted(nt["buildings"].keys())
    bld_set = set(bld_sids)
    for sid in bld_sids:
        # Mermaid does not support inline codespan in flowchart labels; emit
        # <code>…</code> directly (securityLevel="loose" lets htmlLabels through).
        L.append(f'    {sid}["{_short_bld_label(sid, nat)}<br/><code>{sid}</code>"]')

    def _nid(s: str) -> str:
        # Mermaid node IDs must be alphanumeric — replace '.' with '_' for upgrades.
        return s.replace(".", "_")

    for sid in bld_sids:
        b = nt["buildings"][sid]
        for p in b.get("prereqs") or []:
            if p.get("kind") == "building" and p.get("sid") in bld_set:
                L.append(f"    {_nid(p['sid'])} --> {_nid(sid)}")
            elif p.get("kind") == "upgrade" and p.get("sid", "").endswith(".1"):
                # cen.1 (era upgrade) is the gateway to ba2 — special node
                up_sid = p["sid"]
                L.append(f'    {_nid(up_sid)}{{"{up_sid}<br/>(апгрейд)"}}')
                L.append(f"    {_nid(up_sid)} --> {_nid(sid)}")
                host = up_sid.split(".")[0]
                if host in bld_set:
                    L.append(f"    {host} -.-> {_nid(up_sid)}")
    L.append("```")
    L.append("")
    return L


def write_tree_md(tree: dict) -> None:
    L: list[str] = []
    L.append("# Дерево развития")
    L.append("")
    L.append("[← Таблицы и расчёты](../README.md)")
    L.append("")
    L.append("Что нужно построить или исследовать, чтобы открыть выбранное здание, "
             "юнита или улучшение. Каноническое название показано первым, "
             "внутренний код — вторым.")
    L.append("")
    L.append("Для зданий указана цена первого экземпляра. Стоимость следующих "
             "экземпляров приведена в [таблице роста цен](../economy/scaling_prices.md).")
    L.append("")

    if "aus" in tree["nations"]:
        L.append("## Схема зданий на примере Австрии")
        L.append("")
        L.append("Стрелка идёт от требования к открываемому зданию. Пунктиром "
                 "показана связь Городского центра с переходом в XVIII век. "
                 "У большинства наций схема устроена так же.")
        L.append("")
        L.extend(render_buildings_mermaid("aus", tree["nations"]["aus"]))

    L.append("## Содержание")
    L.append("")
    nations_sorted = sorted(tree["nations"].keys())
    L.append("| Нация | Здания | Юниты | Ключевые апгрейды |")
    L.append("|---|---|---|---|")
    for nat in nations_sorted:
        nt = tree["nations"][nat]
        has_ug = any(ug["prereqs"] for ug in nt["upgrades"].values())
        anchor = heading_anchor(nation_ru(nat))
        nation_name = nation_ru(nat)
        bld_link = f"[здания](#{heading_anchor('Здания — ' + nation_name)})"
        unit_link = f"[юниты](#{heading_anchor('Юниты — ' + nation_name)})"
        ug_link = (f"[улучшения](#{heading_anchor('Ключевые улучшения — ' + nation_name)})"
                   if has_ug else "—")
        L.append(f"| **[{nation_ru(nat)}](#{anchor})** | {bld_link} | {unit_link} | {ug_link} |")
    L.append("")

    for nat in nations_sorted:
        nt = tree["nations"][nat]
        L.append(f"## {nation_ru(nat)}")
        L.append("")
        labels = {
            sid: name_ru_en(item)
            for category in ("buildings", "units", "upgrades")
            for sid, item in nt[category].items()
        }
        L.append(f"### Здания — {nation_ru(nat)}")
        L.append("")
        L.append("| Здание | Время строительства, игр. с | Цена | Места населения | Требуется |")
        L.append("|---|---:|---|---:|---|")
        for sid in sorted(nt["buildings"].keys()):
            b = nt["buildings"][sid]
            cost_str = _fmt_cost(b["cost"])
            prereqs_str = ", ".join(_fmt_prereq(p, labels) for p in b["prereqs"]) or "—"
            time_str = f"{b['buildtime_sec']:.1f}" if b['buildtime_sec'] else "—"
            farm_str = str(b["farm"] or "—")
            L.append(f"| **{name_ru_en(b)}** (`{sid}`) | {time_str} | {cost_str} | {farm_str} | {prereqs_str} |")
        L.append("")

        L.append(f"### Юниты — {nation_ru(nat)}")
        L.append("")
        L.append("| Юнит | Время найма, игр. с | Цена | Производится в | Требуется |")
        L.append("|---|---:|---|---|---|")
        for sid in sorted(nt["units"].keys()):
            u = nt["units"][sid]
            cost_str = _fmt_cost(u["cost"])
            time_str = f"{u['buildtime_sec']:.2f}" if u['buildtime_sec'] else "—"
            prereqs_str = ", ".join(_fmt_prereq(p, labels) for p in u["prereqs"]) or "—"
            tr_str = ", ".join(
                f"{labels.get(host, host)} (`{host}`)" for host in u["trained_in"]
            ) or "—"
            L.append(f"| **{name_ru_en(u)}** (`{sid}`) | {time_str} | {cost_str} | {tr_str} | {prereqs_str} |")
        L.append("")

        ug_with_reqs = [(sid, ug) for sid, ug in nt["upgrades"].items() if ug["prereqs"]]
        if ug_with_reqs:
            L.append(f"### Ключевые улучшения — {nation_ru(nat)}")
            L.append("")
            L.append("| Улучшение | Время исследования, игр. с | Цена | Требуется |")
            L.append("|---|---:|---|---|")
            for sid, ug in sorted(ug_with_reqs):
                cost_str = _fmt_cost(ug["cost"])
                time_str = f"{ug['time_sec']:.1f}" if ug['time_sec'] else "—"
                prereqs_str = ", ".join(_fmt_prereq(p, labels) for p in ug["prereqs"]) or "—"
                L.append(f"| **{name_ru_en(ug)}** (`{sid}`) | {time_str} | {cost_str} | {prereqs_str} |")
            L.append("")
        L.append("[↑ к содержанию](#содержание)")
        L.append("")
    TREE_MD.write_text("\n".join(L), encoding="utf-8")
    print(f"Wrote {TREE_MD} ({TREE_MD.stat().st_size:,} bytes)")


def write_production_rates_md(data: dict) -> None:
    """Per-nation: for each building that produces units, list (unit, buildtime,
    rate per g-min, rate per real-min @ fast)."""
    units_idx = {(u["sid"], u["nation"]): u for u in data["units"]}
    cites = Citations()
    L: list[str] = []
    L.append("# Скорость производства юнитов")
    L.append("")
    L.append("[← Таблицы и расчёты](../README.md)")
    L.append("")
    L.append("Сколько юнитов в минуту даёт **одно здание**, при бесперебойной "
             "очереди, свободных мест населения и достаточных ресурсов.")
    L.append("")
    progress_cite = cites.cite(
        "units/building.inc/doprogressorders.inc:120-373",
        label="`DoProgressOrders` для зданий — обработка очереди производства",
    )
    L.append(f"**Как это работает** {progress_cite}:")
    L.append("- У здания одна очередь; параллельно два юнита не производятся.")
    L.append("- Стоимость списывается при начале производства каждого юнита.")
    L.append("- Если нет свободных мест населения или достигнут лимит юнитов, "
             "производство останавливается.")
    L.append("")
    L.append("Сгруппировано по нациям. Для каждого здания — список юнитов, которых "
             "оно может производить.")
    L.append("")

    nations = sorted(set(b["nation"] for b in data["buildings"]))

    def production_anchor(nation: str, building_sid: str) -> str:
        return f"production-{nation}-{building_sid}"

    L.append("## Содержание")
    L.append("")
    for nat in nations:
        bldgs = [b for b in data["buildings"] if b["nation"] == nat and (b.get("produces") or [])]
        if not bldgs:
            continue
        bld_links = ", ".join(
            f"[{name_ru_en(b)}](#{production_anchor(nat, b['sid'])})"
            for b in sorted(bldgs, key=lambda x: x["sid"])
        )
        anchor = heading_anchor(nation_ru(nat))
        L.append(f"- **[{nation_ru(nat)}](#{anchor})** — {bld_links}")
    L.append("")

    for nat in nations:
        L.append(f"## {nation_ru(nat)}")
        L.append("")
        bldgs = [b for b in data["buildings"] if b["nation"] == nat and (b.get("produces") or [])]
        if not bldgs:
            L.append("(нет производящих зданий)")
            L.append("")
            continue
        for b in sorted(bldgs, key=lambda x: x["sid"]):
            L.append(f'<a id="{production_anchor(nat, b["sid"])}"></a>')
            L.append(f"### {name_ru_en(b)} — `{b['sid']}`")
            L.append("")
            L.append("| Юнит | Время найма, игр. с | За игровую минуту | "
                     "За реальную минуту на «Быстро» | Еда | Золото | Железо | Места населения | Расход еды |")
            L.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
            for unit_sid in sorted(b.get("produces") or []):
                u = units_idx.get((unit_sid, nat))
                if not u or not u.get("buildtime_sec"):
                    continue
                bt = u["buildtime_sec"]
                rate_g = 60 / bt
                rate_r = rate_g * GAMESPEED_FAST
                upkeep = (u.get("consume") or {}).get("food") if isinstance(u.get("consume"), dict) else None
                L.append(f"| **{name_ru_en(u)}** (`{unit_sid}`) | {bt:.2f} | {rate_g:.1f} | "
                         f"**{rate_r:.1f}** | {u.get('food') or 0} | {u.get('gold') or 0} | "
                         f"{u.get('iron') or 0} | {1 if not (u.get('peasantabsorber') or 0) else 0} | "
                         f"{upkeep or '—'} |")
            L.append("")
        L.append("[↑ к содержанию](#содержание)")
        L.append("")
    L.append("---")
    L.append("")
    L.append("## Замечания")
    L.append("")
    L.append("1. Каждый юнит занимает одно место населения. Городские центры, дома "
             "и казармы увеличивают доступный предел.")
    L.append("2. **Расход еды** показывает содержание юнита за игровую секунду.")
    L.append("3. **При нехватке мест населения производство останавливается:** "
             "юнит не выходит, а прогресс остаётся замороженным.")
    L.append("4. Несколько одинаковых зданий работают параллельно. Например, пять "
             "казарм дают примерно впятеро больше юнитов в минуту, чем одна.")
    L.extend(cites.render())
    RATES_MD.write_text("\n".join(L), encoding="utf-8")
    print(f"Wrote {RATES_MD} ({RATES_MD.stat().st_size:,} bytes)")


def main() -> None:
    if not TREE_JSON.exists():
        print(f"missing {TREE_JSON} — run parser/build_tech_graph.py first", file=sys.stderr)
        sys.exit(1)
    tree = json.loads(TREE_JSON.read_text(encoding="utf-8"))
    data = json.loads(DATA_JSON.read_text(encoding="utf-8"))
    TREE_MD.parent.mkdir(parents=True, exist_ok=True)
    RATES_MD.parent.mkdir(parents=True, exist_ok=True)
    write_tree_md(tree)
    write_production_rates_md(data)


if __name__ == "__main__":
    main()
