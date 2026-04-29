"""Cross-nation overview matrix.

Per-nation cheatsheets (docs/reference/nations/<nat>.md) cover one nation
at a time. This report is the side-by-side view: at-a-glance answers to
"who has what?" — useful for opponent ID, race comparison, and matchup prep.

Sections:
  §1 Roster size & era access      — total units, Shooter/Cavalry mix, has 18c?
  §2 Building coverage matrix      — which nations lack which standard
                                     buildings (e.g. ukr has no walls / towers)
  §3 Unique units per nation       — sid that appears in only one nation
  §4 Stat anomalies on common units — same usage_short, different stats by nation
  §5 Mercenary access              — what each nation can hire from dip
  §6 Market cluster                — which mar variant (eur/rus/spa/tur)
"""
from __future__ import annotations
import sys
import json
from pathlib import Path
from collections import defaultdict

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "parser"))
from config import DATA_JSON, REPORTS_DIR, PLAYABLE_NATIONS, REPORTS_NATIONS_DIR

MD_PATH = REPORTS_NATIONS_DIR / "overview.md"

NATION_NAMES = {
    "aus": "Austria", "fra": "France", "eng": "England", "spa": "Spain",
    "rus": "Russia", "ukr": "Ukraine", "pol": "Poland", "swe": "Sweden",
    "pru": "Prussia", "ven": "Venice", "tur": "Turkey", "alg": "Algeria",
    "net": "Netherlands", "den": "Denmark", "por": "Portugal", "pie": "Piedmont",
    "sax": "Saxony", "bav": "Bavaria", "hun": "Hungary", "swi": "Switzerland",
    "sco": "Scotland",
}

# Standard building categories. Keys match `usage_short` in data.json (English),
# values are the localized labels shown in the report header.
STD_BUILDINGS = [
    ("Town Hall",         "Городской центр"),
    ("Housing/Farm",      "Дом"),
    ("Mill",              "Мельница"),
    ("Storehouse",        "Склад"),
    ("Tower",             "Башня"),
    ("Stone Wall/Gate",   "Стена/ворота"),
    ("Mine",              "Шахта"),
    ("Shipyard",          "Порт"),
    ("Diplomatic Center", "Дипломатический центр"),
]


def render_roster_size(units: list[dict]) -> list[str]:
    L = []
    A = L.append
    A("## §1. Размер ростера и эпохальный доступ")
    A("")
    A("Сколько разных юнит-sid'ов доступно нации (`?` — мисс / тест-юниты, "
      "Drummer/Officer/Priest и т.п. отнесены отдельно). Колонка **18c** — "
      "есть ли у нации Barracks 18-в. (`<nat>ba2`); если нет — нация заперта "
      "в 17-в. эпохе.")
    A("")
    nat_units = defaultdict(list)
    nat_18c = defaultdict(bool)
    for u in units:
        nat_units[u["nation"]].append(u)
    nat_buildings_18 = set()
    A("| Nation | Total units | Combat | Shooters | Cavalry | Grenadiers | Ships | 18c access |")
    A("| --- | ---: | ---: | ---: | ---: | ---: | ---: | :---: |")
    for nat in sorted(nat_units):
        us = nat_units[nat]
        total = len(us)
        combat_usages = {"Shooter", "Light Infantry", "Archer",
                         "Light Cavalry", "Heavy Cavalry", "Mounted Shooter",
                         "Grenadier", "Cannon", "Mortar", "Super Mortar",
                         "Multi-cannon"}
        combat = sum(1 for u in us if (u.get("usage_short") or "") in combat_usages)
        shooters = sum(1 for u in us if u.get("usage_short") == "Shooter")
        cavalry = sum(1 for u in us if "Cavalry" in (u.get("usage_short") or "")
                      or u.get("usage_short") == "Mounted Shooter")
        grenadiers = sum(1 for u in us if u.get("usage_short") == "Grenadier")
        ships = sum(1 for u in us if (u.get("usage_short") or "") in
                    {"Galley", "Frigate", "Battleship", "Yacht", "Transport",
                     "Fishing Boat"})
        # 18c: has any unit trained_in == "<nat>ba2"
        has_ba2 = any(f"{nat}ba2" in (u.get("trained_in") or []) for u in us)
        A(f"| **{nat}** {NATION_NAMES.get(nat,'')} | {total} | {combat} | "
          f"{shooters} | {cavalry} | {grenadiers} | {ships} | "
          f"{'✅' if has_ba2 else '❌'} |")
    A("")
    return L


def render_building_coverage(buildings: list[dict]) -> list[str]:
    L = []
    A = L.append
    A("## §2. Покрытие стандартных построек")
    A("")
    A("`✅` = нация имеет здание, `—` = у нации этого здания нет. "
      "Полный каталог зданий — [03_buildings.md](../reference/03_buildings.md).")
    A("")
    nat_have = defaultdict(set)
    for b in buildings:
        usage = b.get("usage_short")
        if usage:
            nat_have[b["nation"]].add(usage)
    headers = [ru for _en, ru in STD_BUILDINGS]
    A("| Нация | " + " | ".join(headers) + " |")
    A("| --- | " + " | ".join(":---:" for _ in STD_BUILDINGS) + " |")
    for nat in sorted(nat_have):
        cells = ["✅" if en in nat_have[nat] else "❌" for en, _ru in STD_BUILDINGS]
        A(f"| **{nat}** | " + " | ".join(cells) + " |")
    A("")
    # Notable absences
    notable = []
    for nat in sorted(nat_have):
        missing = [ru for en, ru in STD_BUILDINGS if en not in nat_have[nat]]
        if missing:
            notable.append(f"- **{nat}** — нет: {', '.join(missing)}")
    if notable:
        A("**Заметные пропуски:**")
        A("")
        L.extend(notable)
        A("")
    return L


def render_unique_units(units: list[dict]) -> list[str]:
    L = []
    A = L.append
    A("## §3. Уникальные юниты по нациям")
    A("")
    A("Юниты с `sid`, который встречается только у одной нации (после "
      "слияния `<unit>dip`-наёмников). Это «фишечные» отряды, с которыми "
      "нация ассоциируется. Мерсенарские sid (`<unit>dip`) показываются "
      "отдельно в §5.")
    A("")
    sid_to_nations = defaultdict(set)
    sid_to_unit = {}
    for u in units:
        if u.get("bmercenary"):
            continue
        sid = u["sid"]
        sid_to_nations[sid].add(u["nation"])
        sid_to_unit[sid] = u
    by_nation = defaultdict(list)
    for sid, nats in sid_to_nations.items():
        if len(nats) == 1:
            nat = next(iter(nats))
            by_nation[nat].append(sid_to_unit[sid])
    A("| Nation | Уникальные sid (usage · HP) |")
    A("| --- | --- |")
    for nat in sorted(by_nation):
        items = sorted(by_nation[nat], key=lambda u: -(u.get("hp") or 0))
        cells = []
        for u in items:
            sid = u.get("sid")
            usg = u.get("usage_short") or "?"
            hp = u.get("hp")
            name = u.get("name_en") or sid
            cells.append(f"`{sid}` _{name}_ ({usg}, HP={hp})")
        A(f"| **{nat}** | " + "<br>".join(cells) + " |")
    A("")
    no_unique = sorted(set(NATION_NAMES) - set(by_nation))
    if no_unique:
        A(f"**Без уникальных не-наёмных юнитов:** {', '.join(no_unique)} "
          "— используют только общий ростер.")
        A("")
    return L


def render_stat_anomalies(units: list[dict]) -> list[str]:
    L = []
    A = L.append
    A("## §4. Стат-аномалии на «одинаковых» юнитах")
    A("")
    A("Один и тот же `usage_short` у разных наций может иметь разные HP / "
      "damage / armor — это и есть скрытые балансовые отличия. Здесь — "
      "категории, где разброс HP между нациями ≥ 20%.")
    A("")
    by_usage_nation = defaultdict(lambda: defaultdict(list))
    for u in units:
        usg = u.get("usage_short")
        if not usg or usg in {"Peasant", "?", "Transport", "Fishing Boat"}:
            continue
        if u.get("bmercenary"):
            continue  # mercenaries are nation-agnostic
        by_usage_nation[usg][u["nation"]].append(u)
    A("| Usage | Min HP (nation · sid) | Max HP (nation · sid) | Spread |")
    A("| --- | --- | --- | ---: |")
    rows = []
    for usg in sorted(by_usage_nation):
        all_units = []
        for nat, lst in by_usage_nation[usg].items():
            for u in lst:
                hp = u.get("hp") or 0
                if hp > 0:
                    all_units.append((hp, nat, u.get("sid")))
        if len(all_units) < 2:
            continue
        all_units.sort()
        mn = all_units[0]
        mx = all_units[-1]
        if mn[0] == 0 or mx[0] == 0:
            continue
        spread = (mx[0] - mn[0]) / mn[0]
        if spread < 0.2:
            continue
        rows.append((spread, usg, mn, mx))
    rows.sort(key=lambda r: -r[0])
    for spread, usg, mn, mx in rows:
        A(f"| {usg} | {mn[1]} · `{mn[2]}` ({mn[0]}) | "
          f"{mx[1]} · `{mx[2]}` ({mx[0]}) | +{round(spread*100)}% |")
    A("")
    return L


def render_mercenaries(units: list[dict]) -> list[str]:
    L = []
    A = L.append
    A("## §5. Доступные наёмники (через дипломатический центр)")
    A("")
    A("Юниты, обучаемые в `<nat>dip` (Дипломатический центр). Большинство из них "
      "имеет суффикс `dip` в `sid`. Платежи в gold, тренируются как обычные "
      "юниты, но не зависят от барачных prereq'ов. Юниты с явным флагом "
      "`bmercenary=True` (только `battleship` в текущем балансе) дополнительно "
      "потребляют gold-upkeep и при `gold=0` подвержены Rebellion (см. "
      "[`reference/01_economy.md`](../reference/01_economy.md#famine-голод-и-rebellion-восстание)).")
    A("")
    dip_to_nations = defaultdict(set)
    dip_to_unit = {}
    for u in units:
        ti = u.get("trained_in") or []
        for tr in ti:
            if tr.endswith("dip"):
                dip_to_nations[u["sid"]].add(u["nation"])
                dip_to_unit[u["sid"]] = u
    A("| Sid | Usage | HP | max dmg | bmerc? | nations |")
    A("| --- | --- | ---: | ---: | :---: | --- |")
    rows = []
    for sid, nats in dip_to_nations.items():
        u = dip_to_unit[sid]
        weapons = u.get("weapons") or []
        dmg = max((w.get("damage") or 0) for w in weapons) if weapons else 0
        is_merc = u.get("bmercenary") or False
        rows.append((u.get("usage_short") or "?", sid, u.get("hp"), dmg, is_merc, sorted(nats)))
    for usg, sid, hp, dmg, is_merc, nats in sorted(rows):
        nat_str = "all" if len(nats) == len(PLAYABLE_NATIONS) else (
            ", ".join(nats[:6]) + (f" … (+{len(nats)-6})" if len(nats) > 6 else ""))
        merc_mark = "✅" if is_merc else "—"
        A(f"| `{sid}` | {usg} | {hp} | {dmg} | {merc_mark} | {nat_str} |")
    A("")
    return L


def render_market_cluster(buildings: list[dict]) -> list[str]:
    L = []
    A = L.append
    A("## §6. Вариант рынка")
    A("")
    A("`mar` — общее здание (см. [03_buildings.md → mar](../reference/03_buildings.md#mar--market)). "
      "У наций — 4 разных вариантов здания (`eurmar`/`rusmar`/`spamar`/`turmar`), отличающихся "
      "HP, ценой и временем постройки. Это **только варианты здания** — курсы рынка глобальные "
      "и одни и те же для всех игроков в матче, независимо от того, какой `mar` они построили "
      "(см. [06_market.md](../reference/06_market.md#курсы--глобальные-их-видят-все-игроки)).")
    A("")
    nat_to_cluster = {}
    for b in buildings:
        sid = b.get("sid") or ""
        if sid in {"eurmar", "rusmar", "spamar", "turmar"}:
            nat_to_cluster[b["nation"]] = sid[:3]
    by_cluster = defaultdict(list)
    for nat, cl in nat_to_cluster.items():
        by_cluster[cl].append(nat)
    A("| Cluster | Nations |")
    A("| --- | --- |")
    for cl in sorted(by_cluster):
        nats = sorted(by_cluster[cl])
        A(f"| `{cl}mar` | {', '.join(nats)} |")
    A("")
    return L


def main() -> None:
    data = json.loads(DATA_JSON.read_text(encoding="utf-8"))
    units = data["units"]
    buildings = data["buildings"]
    MD_PATH.parent.mkdir(parents=True, exist_ok=True)

    L = []
    A = L.append
    A("# Cossacks 3 — Cross-nation overview")
    A("")
    A("**Производный** отчёт. Считается из `docs/data.json` скриптом "
      "[`compute/compute_nations_overview.py`](../../compute/compute_nations_overview.py).")
    A("")
    A("Side-by-side сравнение всех 21 наций. Для подробностей по конкретной "
      "нации — [`reference/nations/<nat>.md`](../reference/nations/README.md).")
    A("")
    L.extend(render_roster_size(units))
    L.extend(render_building_coverage(buildings))
    L.extend(render_unique_units(units))
    L.extend(render_stat_anomalies(units))
    L.extend(render_mercenaries(units))
    L.extend(render_market_cluster(buildings))
    A("---")
    A("")
    A("Перегенерация: `python compute/compute_nations_overview.py`")
    MD_PATH.write_text("\n".join(L), encoding="utf-8")
    print(f"Wrote {MD_PATH} ({MD_PATH.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
