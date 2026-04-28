"""Build tech tree (dependency graph) from data.json.

Outputs (under output/strategy/):
- output/derived/tech_tree.json — структурированный граф (для симулятора и других консументов)
- output/strategy/tech_tree.md   — человеко-читаемая версия (по нациям)
- output/strategy/production_rates.md — таблица "сколько юнитов/мин одно здание"

Зависимости извлекаются из:
- building.prereqs (список зданий или апгрейдов, нужных чтобы строить здание)
- unit.prereqs (нужно для тренировки юнита, обычно "его здание готово")
- unit.trained_in (какое здание тренирует)
- upgrade.prereqs (другие апгрейды/здания/век)

Производственная скорость:
- 1 здание = 1 юнит за раз (sequential queue, см. units/building.inc/doprogressorders.inc)
- rate_per_g_sec = 1 / unit.buildtime_sec
- rate_per_real_sec @ fast = rate_per_g_sec × 1.4
"""
from __future__ import annotations
import json
import sys
from collections import defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "parser"))
from config import DATA_JSON, STRATEGY_DIR, DERIVED_DIR
DATA_PATH = DATA_JSON
TREE_JSON = DERIVED_DIR / "tech_tree.json"  # JSON → derived/
TREE_MD = STRATEGY_DIR / "tech_tree.md"     # MD → strategy/
RATES_MD = STRATEGY_DIR / "production_rates.md"

GAMESPEED_FAST = 1.4

# Buildings the user typically cares about for strategy (per-nation)
PER_NAT_BLD = ["cen", "hou", "bla", "bar", "ba2", "sta", "tem", "aca", "art", "dip"]
COMMON_BLD = ["mil", "sto", "mar", "por", "tow", "gol", "iro", "coa"]


def name_ru_en(item: dict) -> str:
    ru = (item.get("name_ru") or "").strip()
    en = (item.get("name_en") or "").strip()
    return ru or en or "—"


def _build_index(data: dict) -> dict:
    """Build lookup tables for building/unit/upgrade by (sid, nation)."""
    bld = {(b["sid"], b["nation"]): b for b in data["buildings"]}
    unt = {(u["sid"], u["nation"]): u for u in data["units"]}
    upg = {(u["sid"], u["nation"]): u for u in data["upgrades"]}
    return {"buildings": bld, "units": unt, "upgrades": upg}


def _kind_of(sid: str, nat: str, idx: dict) -> str | None:
    if (sid, nat) in idx["buildings"]:
        return "building"
    if (sid, nat) in idx["units"]:
        return "unit"
    if (sid, nat) in idx["upgrades"]:
        return "upgrade"
    return None


def _resolve_prereqs(prereqs: list[str], nat: str, idx: dict) -> list[dict]:
    """Map raw prereq sids to {kind,sid,note} entries. Filter out obvious junk."""
    out = []
    seen = set()
    for r in prereqs:
        if not r or r.startswith("'") or "+" in r or r in ("req0", "req1", "century18"):
            # 'century18' is a magic alias for csid+'cen.1' that the simulator
            # didn't resolve. Substitute with '<nat>cen.1' explicitly.
            if r == "century18":
                resolved = nat + "cen.1"
                kind = _kind_of(resolved, nat, idx) or "upgrade"
                if (kind, resolved) in seen:
                    continue
                seen.add((kind, resolved))
                out.append({"kind": kind, "sid": resolved, "note": "century18 → cen.1 upgrade"})
            continue
        kind = _kind_of(r, nat, idx)
        if kind is None:
            # Could be a common-cluster sid (e.g. eurmil/eurpor) for a non-eur nation
            # — try direct lookup ignoring nation.
            for n in [nat, "eur", "rus", "tur", "spa", "ukr", "por"]:
                if (r, n) in idx["buildings"]:
                    kind = "building"
                    break
                if (r, n) in idx["units"]:
                    kind = "unit"
                    break
                if (r, n) in idx["upgrades"]:
                    kind = "upgrade"
                    break
        if kind is None:
            # unknown — likely synthetic alias or unresolved variable; skip
            continue
        if (kind, r) in seen:
            continue
        seen.add((kind, r))
        out.append({"kind": kind, "sid": r, "note": ""})
    return out


def build_tree(data: dict) -> dict:
    """Build {nation: {buildings: {sid: {prereqs:[...], stats}}, units: {...}, upgrades: {...}}}."""
    idx = _build_index(data)
    nations = sorted(set(b["nation"] for b in data["buildings"]))
    tree: dict = {"nations": {}}
    for nat in nations:
        nat_tree = {"buildings": {}, "units": {}, "upgrades": {}}
        for b in data["buildings"]:
            if b["nation"] != nat:
                continue
            nat_tree["buildings"][b["sid"]] = {
                "name_en": b.get("name_en"),
                "name_ru": b.get("name_ru"),
                "kind": b.get("kind"),
                "buildtime_sec": b.get("buildtime_sec"),
                "cost": {k: b.get(k) or 0 for k in ("food", "wood", "stone", "gold", "iron", "coal")},
                "hp": b.get("hp"),
                "farm": b.get("farm"),
                "produces": b.get("produces") or [],
                "prereqs": _resolve_prereqs(b.get("prereqs") or [], nat, idx),
                "costpercent": b.get("costpercent"),
            }
        for u in data["units"]:
            if u["nation"] != nat:
                continue
            nat_tree["units"][u["sid"]] = {
                "name_en": u.get("name_en"),
                "name_ru": u.get("name_ru"),
                "buildtime_sec": u.get("buildtime_sec"),
                "cost": {k: u.get(k) or 0 for k in ("food", "wood", "stone", "gold", "iron", "coal")},
                "hp": u.get("hp"),
                "trained_in": u.get("trained_in") or [],
                "prereqs": _resolve_prereqs(u.get("prereqs") or [], nat, idx),
            }
        for ug in data["upgrades"]:
            if ug["nation"] != nat:
                continue
            nat_tree["upgrades"][ug["sid"]] = {
                "name_en": ug.get("name_en"),
                "name_ru": ug.get("name_ru"),
                "itype": ug.get("itype"),
                "value": ug.get("value"),
                "time_sec": ug.get("time_sec"),
                "cost": {k: ug.get(k) or 0 for k in ("food", "wood", "stone", "gold", "iron", "coal")},
                "place": ug.get("place"),
                "prereqs": _resolve_prereqs(ug.get("prereqs") or [], nat, idx),
            }
        tree["nations"][nat] = nat_tree
    return tree


# ---------- Markdown output ----------

def write_tree_md(tree: dict):
    L = []
    L.append("# Cossacks 3 — Tech Tree (по нациям)")
    L.append("")
    L.append("Граф зависимостей: что нужно построить/исследовать перед чем. Извлечено из "
             "`_country_AddFixedProduceWithAccessControl` и `_country_AddUpgradeWithAccessControl` "
             "(параметры `req0`..`req7`). Источник истины — `output/derived/tech_tree.json`.")
    L.append("")
    L.append("**Условные обозначения:**")
    L.append("- `[B]` — здание, `[U]` — юнит, `[T]` — апгрейд (technology, исследование)")
    L.append("- `→ X, Y` — для разблокировки нужны X и Y одновременно")
    L.append("- Для зданий показана базовая цена (см. `cossacks3_scaling_prices.md` для N>1)")
    L.append("")
    L.append(f"## Содержание")
    L.append("")
    for nat in sorted(tree["nations"].keys()):
        L.append(f"- [{nat}](#{nat})")
    L.append("")

    for nat in sorted(tree["nations"].keys()):
        nt = tree["nations"][nat]
        L.append(f"## {nat}")
        L.append("")
        # Buildings
        L.append(f"### `{nat}` — здания")
        L.append("")
        L.append("| sid | имя | время | цена | ферма | требует |")
        L.append("|---|---|---:|---|---:|---|")
        for sid in sorted(nt["buildings"].keys()):
            b = nt["buildings"][sid]
            cost_str = " ".join(f"{k[0].upper()}{v}" for k, v in b["cost"].items() if v)
            prereqs_str = ", ".join(_fmt_prereq(p) for p in b["prereqs"]) or "—"
            time_str = f"{b['buildtime_sec']:.1f}s" if b['buildtime_sec'] else "—"
            farm_str = str(b["farm"] or "—")
            L.append(f"| `{sid}` | {name_ru_en(b)} | {time_str} | {cost_str or '—'} | {farm_str} | {prereqs_str} |")
        L.append("")
        # Units
        L.append(f"### `{nat}` — юниты")
        L.append("")
        L.append("| sid | имя | время | цена | trained_in | требует |")
        L.append("|---|---|---:|---|---|---|")
        for sid in sorted(nt["units"].keys()):
            u = nt["units"][sid]
            cost_str = " ".join(f"{k[0].upper()}{v}" for k, v in u["cost"].items() if v)
            time_str = f"{u['buildtime_sec']:.2f}s" if u['buildtime_sec'] else "—"
            prereqs_str = ", ".join(_fmt_prereq(p) for p in u["prereqs"]) or "—"
            tr_str = ", ".join(u["trained_in"]) or "—"
            L.append(f"| `{sid}` | {name_ru_en(u)} | {time_str} | {cost_str or '—'} | {tr_str} | {prereqs_str} |")
        L.append("")
        # Upgrades — только те с непустыми prereqs (иначе шум)
        ug_with_reqs = [(sid, ug) for sid, ug in nt["upgrades"].items() if ug["prereqs"]]
        if ug_with_reqs:
            L.append(f"### `{nat}` — ключевые апгрейды (с зависимостями)")
            L.append("")
            L.append("| sid | имя | время | цена | требует |")
            L.append("|---|---|---:|---|---|")
            for sid, ug in sorted(ug_with_reqs):
                cost_str = " ".join(f"{k[0].upper()}{v}" for k, v in ug["cost"].items() if v)
                time_str = f"{ug['time_sec']:.1f}s" if ug['time_sec'] else "—"
                prereqs_str = ", ".join(_fmt_prereq(p) for p in ug["prereqs"]) or "—"
                L.append(f"| `{sid}` | {name_ru_en(ug)[:60]} | {time_str} | {cost_str or '—'} | {prereqs_str} |")
            L.append("")
    TREE_MD.write_text("\n".join(L), encoding="utf-8")
    print(f"Wrote {TREE_MD} ({TREE_MD.stat().st_size:,} bytes)")


def _fmt_prereq(p: dict) -> str:
    glyph = {"building": "B", "unit": "U", "upgrade": "T"}.get(p["kind"], "?")
    return f"[{glyph}] `{p['sid']}`"


# ---------- Production rates ----------

def write_production_rates_md(data: dict):
    """Per nation: for each building that produces units, list (unit, buildtime, rate/min g-time, rate/min @ fast)."""
    idx = _build_index(data)
    L = []
    L.append("# Cossacks 3 — Темпы производства")
    L.append("")
    L.append("Сколько юнитов в минуту даёт **одно здание**, при бесперебойной очереди и без farm/resource ограничений.")
    L.append("")
    L.append(f"**Механика** ([units/building.inc/doprogressorders.inc:120-373](C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/units/building.inc/doprogressorders.inc)):")
    L.append("- Здание имеет ОДНУ очередь (`orders[0]`). Параллельной постройки **нет**.")
    L.append("- Прогресс: `progress += deltatime / unit.buildtime`. При `progress ≥ 1` юнит спавнится, прогресс сбрасывается.")
    L.append("- Стоимость списывается **сразу (upfront)** при старте каждого юнита.")
    L.append("- Если упёрлись в farm cap или unit cap — производство **встаёт**, прогресс не идёт.")
    L.append("")
    L.append("**Формулы:**")
    L.append("- `rate_per_g_sec = 1 / unit.buildtime_sec`")
    L.append(f"- `rate_per_real_sec_fast = rate_per_g_sec × {GAMESPEED_FAST}`")
    L.append(f"- `units_per_real_min_fast = rate_per_real_sec_fast × 60`")
    L.append("")
    L.append("Сгруппировано по нациям. Для каждого здания — список юнитов, которых оно может производить.")
    L.append("")

    nations = sorted(set(b["nation"] for b in data["buildings"]))
    for nat in nations:
        L.append(f"## {nat}")
        L.append("")
        # All buildings for this nation that have a `produces` list
        bldgs = [b for b in data["buildings"] if b["nation"] == nat and (b.get("produces") or [])]
        if not bldgs:
            L.append("(нет производящих зданий)")
            L.append("")
            continue
        for b in sorted(bldgs, key=lambda x: x["sid"]):
            L.append(f"### `{b['sid']}` — {name_ru_en(b)}")
            L.append("")
            L.append("| Юнит | имя | buildtime (g-sec) | темп (units/g-min) | темп (units/real-min @ fast) | F | G | I | ферма | расход еды |")
            L.append("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|")
            for unit_sid in sorted(b.get("produces") or []):
                u = idx["units"].get((unit_sid, nat))
                if not u or not u.get("buildtime_sec"):
                    continue
                bt = u["buildtime_sec"]
                rate_g = 60 / bt  # units per game-minute
                rate_r = rate_g * GAMESPEED_FAST  # real-minute @ fast
                upkeep = (u.get("consume") or {}).get("food") if isinstance(u.get("consume"), dict) else None
                L.append(f"| `{unit_sid}` | {name_ru_en(u)} | {bt:.2f} | {rate_g:.1f} | **{rate_r:.1f}** | {u.get('food') or 0} | {u.get('gold') or 0} | {u.get('iron') or 0} | {1 if not (u.get('peasantabsorber') or 0) else 0} | {upkeep or '—'} |")
            L.append("")
    L.append("---")
    L.append("")
    L.append("## Замечания")
    L.append("")
    L.append("1. **farm = 1 для каждого юнита** — каждый юнит занимает 1 слот популяции (контролируется `gPlayer.farm`). Зданиям, увеличивающим лимит — `cen=+100, hou=+25, bar=+150, ba2=+250` и т.д.")
    L.append("2. **расход еды** — потребление еды/g-sec, делится на 32 для игр-секунды (см. `gc_obj_foodperunit`). Стандарт = 32 для пехоты, 26 для рус крестьян, 40+ для тяжёлой кавалерии.")
    L.append("3. **При нехватке farm производство останавливается** — здание попытается списать ресурс, но units не выйдет, прогресс заморожен.")
    L.append("4. **N зданий = N×rate.** 5 бараков пехотных = 5 × ~13 musketeer/min @ fast = ~65 musketeer/min.")
    RATES_MD.write_text("\n".join(L), encoding="utf-8")
    print(f"Wrote {RATES_MD} ({RATES_MD.stat().st_size:,} bytes)")


def main():
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    STRATEGY_DIR.mkdir(parents=True, exist_ok=True)
    print("Building tech tree…")
    tree = build_tree(data)
    TREE_JSON.write_text(json.dumps(tree, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {TREE_JSON} ({TREE_JSON.stat().st_size:,} bytes)")
    write_tree_md(tree)
    write_production_rates_md(data)


if __name__ == "__main__":
    main()
