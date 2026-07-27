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
from config import (DATA_JSON, REPORTS_DIR, PLAYABLE_NATIONS, REPORTS_NATIONS_DIR,
                    NATION_NAMES_RU, USAGE_RU, nation_ru, unit_ru)

MD_PATH = REPORTS_NATIONS_DIR / "overview.md"

# Standard building categories shown in the §2 matrix. Each entry is the
# English `usage_short` value as stored in `data.json`; the Russian label
# rendered in the report header comes from `config.USAGE_RU`.
STD_BUILDING_USAGES = [
    "Town Hall",
    "Housing/Farm",
    "Mill",
    "Storehouse",
    "Tower",
    "Stone Wall/Gate",
    "Mine",
    "Shipyard",
    "Diplomatic Center",
]


def nat_cell(nat: str) -> str:
    """Render the canonical nation name first and its code second."""
    return f"**{nation_ru(nat)}** (`{nat}`)"


def render_roster_size(units: list[dict]) -> list[str]:
    L = []
    A = L.append
    A("## §1. Размер армии и доступ к XVIII веку")
    A("")
    A("Сколько разных юнитов доступно нации и есть ли у неё Казарма XVIII века. "
      "Сценарные и тестовые объекты в боевые категории не включаются.")
    A("")
    nat_units = defaultdict(list)
    nat_18c = defaultdict(bool)
    for u in units:
        nat_units[u["nation"]].append(u)
    nat_buildings_18 = set()
    A("| Нация | Всего юнитов | Боевых | Стрелков | Кавалерии | Гренадёров | Кораблей | 18 в. |")
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
        A(f"| {nat_cell(nat)} | {total} | {combat} | "
          f"{shooters} | {cavalry} | {grenadiers} | {ships} | "
          f"{'✅' if has_ba2 else '❌'} |")
    A("")
    return L


def render_building_coverage(buildings: list[dict]) -> list[str]:
    L = []
    A = L.append
    A("## §2. Покрытие стандартных построек")
    A("")
    A("`✅` = у нации есть это здание, `❌` = у нации его нет. Полный справочник "
      "зданий — в [главе о зданиях](../../reference/03_buildings/README.md).")
    A("")
    nat_have = defaultdict(set)
    for b in buildings:
        usage = b.get("usage_short")
        if usage:
            nat_have[b["nation"]].add(usage)
    headers = [USAGE_RU.get(en, en) for en in STD_BUILDING_USAGES]
    A("| Нация | " + " | ".join(headers) + " |")
    A("| --- | " + " | ".join(":---:" for _ in STD_BUILDING_USAGES) + " |")
    for nat in sorted(nat_have):
        cells = ["✅" if en in nat_have[nat] else "❌" for en in STD_BUILDING_USAGES]
        A(f"| {nat_cell(nat)} | " + " | ".join(cells) + " |")
    A("")
    notable = []
    for nat in sorted(nat_have):
        missing = [USAGE_RU.get(en, en) for en in STD_BUILDING_USAGES
                   if en not in nat_have[nat]]
        if missing:
            notable.append(f"- {nat_cell(nat)} — нет: {', '.join(missing)}")
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
    A("Юниты, доступные только одной нации, без учёта наёмников. "
      "Внутренний код приведён после канонического названия.")
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
    A("| Нация | Уникальные юниты (роль · здоровье) |")
    A("| --- | --- |")
    for nat in sorted(by_nation):
        items = sorted(by_nation[nat], key=lambda u: -(u.get("hp") or 0))
        cells = []
        for u in items:
            sid = u.get("sid")
            usg = USAGE_RU.get(u.get("usage_short") or "", u.get("usage_short") or "?")
            hp = u.get("hp")
            name = unit_ru(sid, u.get("name_ru") or u.get("name_en") or sid)
            cells.append(f"**{name}** (`{sid}`; {usg}, здоровье {hp})")
        A(f"| {nat_cell(nat)} | " + "<br>".join(cells) + " |")
    A("")
    no_unique = sorted(set(NATION_NAMES_RU) - set(by_nation))
    if no_unique:
        no_unique_cells = ", ".join(nat_cell(n) for n in no_unique)
        A(f"**Без уникальных не-наёмничьих юнитов:** {no_unique_cells} — "
          "используют только общий ростер.")
        A("")
    return L


def render_stat_anomalies(units: list[dict]) -> list[str]:
    L = []
    A = L.append
    A("## §4. Отличия характеристик похожих юнитов")
    A("")
    A("Один и тот же класс у разных наций может иметь разные здоровье, урон "
      "и защиту. Здесь показаны категории, где разница здоровья достигает 20% и более.")
    A("")
    by_usage_nation = defaultdict(lambda: defaultdict(list))
    for u in units:
        usg = u.get("usage_short")
        if not usg or usg in {"Peasant", "?", "Transport", "Fishing Boat"}:
            continue
        if u.get("bmercenary"):
            continue  # mercenaries are nation-agnostic
        by_usage_nation[usg][u["nation"]].append(u)
    A("| Класс | Минимальное здоровье | Максимальное здоровье | Разница |")
    A("| --- | --- | --- | ---: |")
    rows = []
    for usg in sorted(by_usage_nation):
        all_units = []
        for nat, lst in by_usage_nation[usg].items():
            for u in lst:
                hp = u.get("hp") or 0
                if hp > 0:
                    sid = u.get("sid")
                    all_units.append((hp, nat, sid,
                                      unit_ru(sid, u.get("name_ru") or u.get("name_en") or sid)))
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
        A(f"| {USAGE_RU.get(usg, usg)} "
          f"| {mn[3]} (`{mn[2]}`), {nation_ru(mn[1])}: {mn[0]} | "
          f"{mx[3]} (`{mx[2]}`), {nation_ru(mx[1])}: {mx[0]} | +{round(spread*100)}% |")
    A("")
    return L


def render_mercenaries(units: list[dict]) -> list[str]:
    L = []
    A = L.append
    A("## §5. Доступные наёмники (через дипломатический центр)")
    A("")
    A("Юниты, которых можно нанять в Дипломатическом центре. Они оплачиваются "
      "золотом и не требуют обычной цепочки казарм. При нехватке золота "
      "наёмники могут поднять бунт; подробности — в "
      "[главе об экономике](../../reference/01_economy/README.md).")
    A("")
    dip_to_nations = defaultdict(set)
    dip_to_unit = {}
    for u in units:
        ti = u.get("trained_in") or []
        for tr in ti:
            if tr.endswith("dip"):
                dip_to_nations[u["sid"]].add(u["nation"])
                dip_to_unit[u["sid"]] = u
    A("| Наёмник | Класс | Здоровье | Максимальный урон | Подвержен бунту | Нации |")
    A("| --- | --- | ---: | ---: | :---: | --- |")
    rows = []
    for sid, nats in dip_to_nations.items():
        u = dip_to_unit[sid]
        weapons = u.get("weapons") or []
        dmg = max((w.get("damage") or 0) for w in weapons) if weapons else 0
        is_merc = u.get("bmercenary") or False
        name = unit_ru(sid, u.get("name_ru") or u.get("name_en") or sid)
        rows.append((u.get("usage_short") or "?", sid, name, u.get("hp"), dmg, is_merc, sorted(nats)))
    for usg, sid, name, hp, dmg, is_merc, nats in sorted(rows):
        if len(nats) == len(PLAYABLE_NATIONS):
            nat_str = "все 21 нация"
        else:
            shown = nats[:6]
            nat_str = ", ".join(nation_ru(n) for n in shown)
            if len(nats) > 6:
                nat_str += f" … (+{len(nats)-6})"
        merc_mark = "✅" if is_merc else "—"
        usg_ru = USAGE_RU.get(usg, usg)
        A(f"| **{name}** (`{sid}`) | {usg_ru} | {hp} | {dmg} | {merc_mark} | {nat_str} |")
    A("")
    return L


def render_market_cluster(buildings: list[dict]) -> list[str]:
    L = []
    A = L.append
    A("## §6. Архитектурные варианты рынка")
    A("")
    A("У рынка четыре архитектурных варианта, которые отличаются здоровьем, "
      "ценой и временем строительства. Курсы обмена при этом общие для всех "
      "игроков матча и не зависят от внешнего вида рынка.")
    A("")
    nat_to_cluster = {}
    for b in buildings:
        sid = b.get("sid") or ""
        if sid in {"eurmar", "rusmar", "spamar", "turmar"}:
            nat_to_cluster[b["nation"]] = sid[:3]
    by_cluster = defaultdict(list)
    for nat, cl in nat_to_cluster.items():
        by_cluster[cl].append(nat)
    A("| Вариант рынка | Нации |")
    A("| --- | --- |")
    for cl in sorted(by_cluster):
        nats = sorted(by_cluster[cl])
        A(f"| `{cl}mar` | " + ", ".join(nat_cell(n) for n in nats) + " |")
    A("")
    return L


def main() -> None:
    data = json.loads(DATA_JSON.read_text(encoding="utf-8"))
    units = data["units"]
    buildings = data["buildings"]
    MD_PATH.parent.mkdir(parents=True, exist_ok=True)

    L = []
    A = L.append
    A("# Сравнение наций")
    A("")
    A("[← Таблицы и расчёты](../README.md)")
    A("")
    A("Сводное сравнение всех 21 наций: доступ к XVIII веку, здания, "
      "уникальные войска, заметные отличия характеристик и наёмники. "
      "Подробные страницы находятся в [справочнике по нациям]"
      "(../../reference/nations/README.md).")
    A("")
    L.extend(render_roster_size(units))
    L.extend(render_building_coverage(buildings))
    L.extend(render_unique_units(units))
    L.extend(render_stat_anomalies(units))
    L.extend(render_mercenaries(units))
    L.extend(render_market_cluster(buildings))
    MD_PATH.write_text("\n".join(L), encoding="utf-8")
    print(f"Wrote {MD_PATH} ({MD_PATH.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
