"""Render the tech-tree graph as Markdown reports.

Reads `docs/derived/tech_tree.json` (built by `parser/build_tech_graph.py`)
and `docs/data.json` (for production rates), emits two markdown files:

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
from config import (DATA_JSON, DERIVED_DIR, REPORTS_ECONOMY_DIR,
                    REPORTS_TECH_DIR, nation_label)

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
    "aca": "Академия",     "art": "Артдепо",     "dip": "Диппцентр",
    "mil": "Мельница",     "sto": "Склад",       "mar": "Рынок",
    "por": "Порт",         "tow": "Башня",
    "gol": "Шахта (gold)", "iro": "Шахта (iron)", "coa": "Шахта (coal)",
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
    return ru or en or "—"


def _short_bld_label(sid: str, nat: str) -> str:
    """Pick a compact Mermaid label: locale short name when known, else sid."""
    suf = sid[len(nat):] if sid.startswith(nat) else (sid[3:] if len(sid) > 3 else sid)
    return SHORT_BLD_LABELS.get(suf, sid)


def _fmt_prereq(p: dict) -> str:
    glyph = {"building": "B", "unit": "U", "upgrade": "T"}.get(p["kind"], "?")
    return f"[{glyph}] `{p['sid']}`"


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
        L.append(f'    {sid}["{_short_bld_label(sid, nat)}<br/>`{sid}`"]')

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
    L.append("# Cossacks 3 — Tech Tree (по нациям)")
    L.append("")
    L.append("Граф зависимостей: что нужно построить или исследовать перед чем. "
             "Извлечено из `_country_AddFixedProduceWithAccessControl` и "
             "`_country_AddUpgradeWithAccessControl` (параметры `req0`..`req7`). "
             "Источник истины — [`docs/derived/tech_tree.json`](../../derived/tech_tree.json).")
    L.append("")
    L.append("**Условные обозначения:**")
    L.append("- `[B]` — здание, `[U]` — юнит, `[T]` — апгрейд (technology, исследование)")
    L.append("- `→ X, Y` — для разблокировки нужны X и Y одновременно")
    L.append("- Для зданий показана базовая цена (см. [`scaling_prices.md`](../economy/scaling_prices.md) для N>1)")
    L.append("")

    if "aus" in tree["nations"]:
        L.append("## Граф зданий (Австрия как репрезентативный пример)")
        L.append("")
        L.append("Граф показывает зависимости постройки одного здания от другого. "
                 "Сплошные стрелки — `prereqs` из `country.script`, пунктирные — "
                 "связь «здание → его апгрейд» (например, `auscen → auscen.1`, "
                 "переход в 18 век). У других наций граф структурно идентичен — "
                 "отличаются только нация-специфичные имена `<nat>cen`, `<nat>bar` "
                 "и т. д.")
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
        anchor = heading_anchor(nation_label(nat))
        bld_link = f"[здания](#{heading_anchor(nat + ' — здания')})"
        unit_link = f"[юниты](#{heading_anchor(nat + ' — юниты')})"
        ug_link = (f"[апгрейды](#{heading_anchor(nat + ' — ключевые апгрейды (с зависимостями)')})"
                   if has_ug else "—")
        L.append(f"| **[{nation_label(nat)}](#{anchor})** | {bld_link} | {unit_link} | {ug_link} |")
    L.append("")

    for nat in nations_sorted:
        nt = tree["nations"][nat]
        L.append(f"## {nation_label(nat)}")
        L.append("")
        L.append(f"### `{nat}` — здания")
        L.append("")
        L.append("| sid | имя | Время (g-сек) | цена | ферма | требует |")
        L.append("|---|---|---:|---|---:|---|")
        for sid in sorted(nt["buildings"].keys()):
            b = nt["buildings"][sid]
            cost_str = " ".join(f"{k[0].upper()}{v}" for k, v in b["cost"].items() if v)
            prereqs_str = ", ".join(_fmt_prereq(p) for p in b["prereqs"]) or "—"
            time_str = f"{b['buildtime_sec']:.1f}" if b['buildtime_sec'] else "—"
            farm_str = str(b["farm"] or "—")
            L.append(f"| `{sid}` | {name_ru_en(b)} | {time_str} | {cost_str or '—'} | {farm_str} | {prereqs_str} |")
        L.append("")

        L.append(f"### `{nat}` — юниты")
        L.append("")
        L.append("| sid | имя | Время (g-сек) | цена | тренируется в | требует |")
        L.append("|---|---|---:|---|---|---|")
        for sid in sorted(nt["units"].keys()):
            u = nt["units"][sid]
            cost_str = " ".join(f"{k[0].upper()}{v}" for k, v in u["cost"].items() if v)
            time_str = f"{u['buildtime_sec']:.2f}" if u['buildtime_sec'] else "—"
            prereqs_str = ", ".join(_fmt_prereq(p) for p in u["prereqs"]) or "—"
            tr_str = ", ".join(u["trained_in"]) or "—"
            L.append(f"| `{sid}` | {name_ru_en(u)} | {time_str} | {cost_str or '—'} | {tr_str} | {prereqs_str} |")
        L.append("")

        ug_with_reqs = [(sid, ug) for sid, ug in nt["upgrades"].items() if ug["prereqs"]]
        if ug_with_reqs:
            L.append(f"### `{nat}` — ключевые апгрейды (с зависимостями)")
            L.append("")
            L.append("| sid | имя | Время (g-сек) | цена | требует |")
            L.append("|---|---|---:|---|---|")
            for sid, ug in sorted(ug_with_reqs):
                cost_str = " ".join(f"{k[0].upper()}{v}" for k, v in ug["cost"].items() if v)
                time_str = f"{ug['time_sec']:.1f}" if ug['time_sec'] else "—"
                prereqs_str = ", ".join(_fmt_prereq(p) for p in ug["prereqs"]) or "—"
                L.append(f"| `{sid}` | {name_ru_en(ug)} | {time_str} | {cost_str or '—'} | {prereqs_str} |")
            L.append("")
        L.append("[↑ к содержанию](#содержание)")
        L.append("")
    TREE_MD.write_text("\n".join(L), encoding="utf-8")
    print(f"Wrote {TREE_MD} ({TREE_MD.stat().st_size:,} bytes)")


def write_production_rates_md(data: dict) -> None:
    """Per-nation: for each building that produces units, list (unit, buildtime,
    rate per g-min, rate per real-min @ fast)."""
    units_idx = {(u["sid"], u["nation"]): u for u in data["units"]}
    L: list[str] = []
    L.append("# Cossacks 3 — Темпы производства")
    L.append("")
    L.append("Сколько юнитов в минуту даёт **одно здание**, при бесперебойной "
             "очереди и без farm/resource ограничений.")
    L.append("")
    L.append("**Механика** (`units/building.inc/doprogressorders.inc:120-373`):")
    L.append("- Здание имеет ОДНУ очередь (`orders[0]`). Параллельной постройки **нет**.")
    L.append("- Прогресс: `progress += deltatime / unit.buildtime`. При `progress ≥ 1` "
             "юнит спавнится, прогресс сбрасывается.")
    L.append("- Стоимость списывается **сразу (upfront)** при старте каждого юнита.")
    L.append("- Если упёрлись в farm cap или unit cap — производство **встаёт**, "
             "прогресс не идёт.")
    L.append("")
    L.append("**Формулы:**")
    L.append("- `rate_per_g_sec = 1 / unit.buildtime_sec`")
    L.append(f"- `rate_per_real_sec_fast = rate_per_g_sec × {GAMESPEED_FAST}`")
    L.append(f"- `units_per_real_min_fast = rate_per_real_sec_fast × 60`")
    L.append("")
    L.append("Сгруппировано по нациям. Для каждого здания — список юнитов, которых "
             "оно может производить.")
    L.append("")

    nations = sorted(set(b["nation"] for b in data["buildings"]))
    L.append("## Содержание")
    L.append("")
    for nat in nations:
        bldgs = [b for b in data["buildings"] if b["nation"] == nat and (b.get("produces") or [])]
        if not bldgs:
            continue
        bld_links = ", ".join(
            f"[`{b['sid']}`](#{heading_anchor(b['sid'] + ' — ' + name_ru_en(b))})"
            for b in sorted(bldgs, key=lambda x: x["sid"])
        )
        anchor = heading_anchor(nation_label(nat))
        L.append(f"- **[{nation_label(nat)}](#{anchor})** — {bld_links}")
    L.append("")

    for nat in nations:
        L.append(f"## {nation_label(nat)}")
        L.append("")
        bldgs = [b for b in data["buildings"] if b["nation"] == nat and (b.get("produces") or [])]
        if not bldgs:
            L.append("(нет производящих зданий)")
            L.append("")
            continue
        for b in sorted(bldgs, key=lambda x: x["sid"]):
            L.append(f"### `{b['sid']}` — {name_ru_en(b)}")
            L.append("")
            L.append("| Юнит | имя | Время (g-сек) | темп (units / g-мин) | "
                     "темп (units / real-мин @ fast) | F | G | I | ферма | расход еды |")
            L.append("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|")
            for unit_sid in sorted(b.get("produces") or []):
                u = units_idx.get((unit_sid, nat))
                if not u or not u.get("buildtime_sec"):
                    continue
                bt = u["buildtime_sec"]
                rate_g = 60 / bt
                rate_r = rate_g * GAMESPEED_FAST
                upkeep = (u.get("consume") or {}).get("food") if isinstance(u.get("consume"), dict) else None
                L.append(f"| `{unit_sid}` | {name_ru_en(u)} | {bt:.2f} | {rate_g:.1f} | "
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
    L.append("1. **farm = 1 для каждого юнита** — каждый юнит занимает 1 слот популяции "
             "(контролируется `gPlayer.farm`). Зданиям, увеличивающим лимит — "
             "`cen = +100`, `hou = +25`, `bar = +150`, `ba2 = +250` и т. д.")
    L.append("2. **Расход еды** — потребление еды в одну игровую секунду делится на 32 "
             "(см. `gc_obj_foodperunit`). Стандарт — 32 для пехоты, 26 для русских "
             "крестьян, 40+ для тяжёлой кавалерии.")
    L.append("3. **При нехватке farm производство останавливается** — здание попытается "
             "списать ресурс, но юнит не выйдет, прогресс заморожен.")
    L.append("4. **N зданий = N × rate.** 5 пехотных казарм = 5 × ~13 мушкетёр/мин @ fast "
             "= ~65 мушкетёров/мин.")
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
