"""Матрица национальных отклонений: где данная нация имеет здание/юнит со
статами, отличными от стандарта.

Контекст. В коде Cossacks 3 общие здания (Городской центр, Казармы, Академия,
Кузница и т. д.) задаются одной точкой определения с веткой `case i of nation:
SetObjBuildingProperties(...)`, которая может перезаписать HP/buildtime/цену
для конкретных наций. Аналогично — для юнитов: `if (commonrus) ...`,
`if (i = ukr) ...`. Без ручного просмотра скрипта эти отклонения теряются
в перечне «такая-то нация имеет такое-то значение».

Отчёт строится из `data.json`: для каждого семейства зданий или общего
sid'а юнита группируем 21 нацию по «отпечатку» (HP, buildtime, цена,
weapon-стат — для юнитов) и показываем, кто отклонился от мажоритарного.

Рядом — отчёт `reports/nations/overview.md` (общий roster, наёмники, рынок-кластер).
Здесь — детализированные дельты, которые нельзя восстановить из
overview.md без перекрёстного чтения per-nation cheatsheet'ов.

Output: docs/reports/nations/deviations.md.
"""
from __future__ import annotations
import sys
import json
from collections import defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "parser"))
from config import (DATA_JSON, PLAYABLE_NATIONS, REPORTS_NATIONS_DIR,
                    NATION_NAMES_RU, USAGE_RU, nation_ru)

MD_PATH = REPORTS_NATIONS_DIR / "deviations.md"


# Per-nation building suffixes (each nation has its own, so 21 records per suffix).
# Excludes cluster-shared buildings (sto/mar/por/...) — те разбираются в overview.md.
PER_NATION_BUILDING_SUFFIXES = [
    ("cen", "Городской центр"),
    ("hou", "Дом / ферма"),
    ("bar", "Казарма XVII в."),
    ("ba2", "Казарма XVIII в."),
    ("sta", "Конюшня"),
    ("aca", "Академия"),
    ("bla", "Кузница"),
    ("art", "Артиллерийское депо"),
    ("dip", "Дипломатический центр"),
    ("tem", "Храм"),
]

# Stat keys that count toward a building "fingerprint". Picked to surface
# meaningful gameplay differences while ignoring locale name and per-nation
# trivia. `produces` is included because the Ukrainian Sich, for example,
# trains units the European barracks does not.
BUILDING_FP_KEYS = (
    "hp", "buildtime_sec", "costpercent",
    "food", "wood", "stone", "gold", "iron", "coal",
    "score", "vision", "farm", "peasantabsorber", "consume",
    "weapon_damage", "weapon_pause_frames", "weapon_radiusmax",
    "produces",
)

UNIT_FP_KEYS = (
    "hp", "buildtime_sec", "costpercent",
    "food", "wood", "stone", "gold", "iron", "coal",
    "score", "shield", "speed", "vision",
    "prot_pike", "prot_sword", "prot_bullet",
    "prot_cannister", "prot_arrow", "prot_cannonball",
    "consume",
)


def freeze(value):
    """Make value hashable for fingerprint use."""
    if isinstance(value, dict):
        return tuple(sorted((k, freeze(v)) for k, v in value.items()))
    if isinstance(value, list):
        return tuple(freeze(v) for v in value)
    return value


def building_fingerprint(b: dict) -> tuple:
    return tuple(freeze(b.get(k)) for k in BUILDING_FP_KEYS)


def unit_fingerprint(u: dict) -> tuple:
    base = tuple(freeze(u.get(k)) for k in UNIT_FP_KEYS)
    weap = []
    for w in (u.get("weapons") or []):
        weap.append((
            w.get("damage"),
            w.get("pause_sec"),
            w.get("radiusmin_tiles"),
            w.get("radiusmax_tiles"),
            w.get("dispertion_tiles"),
            w.get("kind"),
            freeze(w.get("cost")),
        ))
    return base + (tuple(weap),)


def fmt_nations(nats: list[str]) -> str:
    if not nats:
        return "—"
    if len(nats) == len(PLAYABLE_NATIONS):
        return "**все 21 нация**"
    items = [f"**{n}** {nation_ru(n)}" for n in sorted(nats)]
    if len(items) > 6:
        return ", ".join(items[:5]) + f" … (+{len(items) - 5})"
    return ", ".join(items)


def fmt_cost(b: dict) -> str:
    parts = []
    for r in ("food", "wood", "stone", "gold", "iron", "coal"):
        v = b.get(r)
        if v:
            parts.append(f"{v} {r[:1].upper()}")
    return " · ".join(parts) if parts else "—"


def fmt_consume(c: dict | None) -> str:
    if not c:
        return "—"
    parts = []
    for r in ("food", "wood", "stone", "gold", "iron", "coal"):
        v = c.get(r)
        if v:
            parts.append(f"{v} {r[:1].upper()}/тик")
    return " · ".join(parts) if parts else "—"


def render_header() -> list[str]:
    L: list[str] = []
    A = L.append
    A("# Национальные отклонения — здания и юниты")
    A("")
    A("**Производный** файл (расчётный, не извлечение). Считается из "
      "[`docs/data.json`](../../data.json) скриптом "
      "[`compute/compute_nation_deviations.py`](../../../compute/compute_nation_deviations.py).")
    A("")
    A("Цель — собрать в одном месте ВСЕ места, где у конкретной нации значение "
      "стата здания или общего юнита отличается от того, что у большинства. "
      "Источник дельт — `case i of nation:` ветки в `unit.script`, которые "
      "перезаписывают `SetObjBuildingProperties` / `SetObjBaseWeapon` для "
      "отдельных наций.")
    A("")
    A("Формат: для каждого семейства (например, `<nat>cen` — Городской центр) "
      "21 нация группируется по «отпечатку» — кортежу значимых статов. "
      "Мажоритарная группа считается базовым вариантом; меньшие группы "
      "перечисляются как отклонения с явным указанием того, чем именно они "
      "отличаются.")
    A("")
    A("Этот отчёт **не дублирует**, а дополняет "
      "[`reports/nations/overview.md`](overview.md). overview даёт "
      "обзор «у кого что есть» (roster size, building coverage, рынок-"
      "кластеры) и top-10 stat-anomalies по HP-разбросу. Здесь же "
      "перечисляются полные стат-отпечатки.")
    A("")
    A("Содержание:")
    A("")
    A("- [§1. Здания общего класса (Городской центр, Казармы, Академия и т. д.)](#1-здания-общего-класса)")
    A("- [§2. Юниты, общие для нескольких наций](#2-юниты-общие-для-нескольких-наций)")
    A("")
    return L


def render_buildings_section(buildings: list[dict]) -> list[str]:
    L: list[str] = []
    A = L.append
    A("## §1. Здания общего класса")
    A("")
    A("Для каждого семейства зданий — `<nat>` + суффикс — собираются "
      "записи всех наций, у которых это здание есть. Затем нации "
      "группируются по идентичности стат-отпечатка: значения, которые в "
      "скрипте читаются через `SetObjBuildingProperties` / "
      "`SetObjBuildingExtProperties`. Если у нации этого здания нет "
      "(например, Украина без Башни и каменных стен — см. "
      "[`overview.md` §2](overview.md)), она в данной группе не появляется.")
    A("")
    A("Тип «отпечатка»: HP · buildtime · costpercent · цена · score · "
      "vision · farm · peasantabsorber · consume · weapon (damage/pause/radiusmax) · produces.")
    A("")

    by_suffix: dict[str, list[dict]] = defaultdict(list)
    for b in buildings:
        sid = b["sid"]
        if len(sid) > 3 and sid[:3] in PLAYABLE_NATIONS:
            suffix = sid[3:]
            by_suffix[suffix].append(b)

    for suf, ru_label in PER_NATION_BUILDING_SUFFIXES:
        recs = by_suffix.get(suf, [])
        if not recs:
            continue
        A(f"### `<nat>{suf}` — {ru_label}")
        A("")
        groups: dict[tuple, list[dict]] = defaultdict(list)
        for b in recs:
            groups[building_fingerprint(b)].append(b)
        # Sort groups by descending size — majority first.
        ordered = sorted(groups.items(), key=lambda kv: -len(kv[1]))
        for idx, (_, members) in enumerate(ordered):
            rep = members[0]
            label = "**Базовый вариант**" if idx == 0 else f"**Отклонение {idx}**"
            nats = sorted({m["nation"] for m in members})
            A(f"- {label} ({len(nats)}/21): {fmt_nations(nats)}")
            consume_str = fmt_consume(rep.get("consume"))
            produces = ", ".join(rep.get("produces") or []) or "—"
            weapon_bits = []
            if rep.get("weapon_damage"):
                weapon_bits.append(
                    f"weapon: {rep['weapon_damage']} dmg · "
                    f"{rep.get('weapon_pause_frames', '?')}f pause · "
                    f"{rep.get('weapon_radiusmax', '?')} px range")
            A(f"  - HP **{rep.get('hp')}**, "
              f"buildtime **{rep.get('buildtime_sec')}** g-сек, "
              f"costpercent **{rep.get('costpercent')}**")
            A(f"  - цена: {fmt_cost(rep)}")
            extras = []
            if rep.get("score") is not None: extras.append(f"score={rep['score']}")
            if rep.get("vision") is not None: extras.append(f"vision={rep['vision']}")
            if rep.get("farm"): extras.append(f"farm={rep['farm']}")
            if rep.get("peasantabsorber"): extras.append(
                f"peasantabsorber={rep['peasantabsorber']}")
            if extras:
                A("  - " + ", ".join(extras))
            if consume_str != "—":
                A(f"  - consume: {consume_str}")
            for wb in weapon_bits:
                A(f"  - {wb}")
            A(f"  - produces: {produces}")
            A("")
        A("")
    return L


def render_units_section(units: list[dict]) -> list[str]:
    L: list[str] = []
    A = L.append
    A("## §2. Юниты, общие для нескольких наций")
    A("")
    A("Берётся каждый sid юнита, у которого есть запись хотя бы у двух наций "
      "(если у одной — это уникальный юнит, описывается в "
      "[`reports/nations/overview.md`](overview.md) §3). Записи группируются по "
      "стат-отпечатку (HP / buildtime / цена / щит / скорость / защиты / "
      "consume / weapon-набор). Юниты с одинаковым отпечатком сливаются в "
      "одну группу.")
    A("")
    A("Если у sid'а одна группа на все доступные нации — отклонений нет, "
      "и он здесь не показывается. Если разные — перечисляются базовый "
      "вариант (мажоритарный) и отклонения.")
    A("")

    by_sid: dict[str, list[dict]] = defaultdict(list)
    for u in units:
        if u.get("nation") in PLAYABLE_NATIONS:
            by_sid[u["sid"]].append(u)

    output_count = 0
    for sid in sorted(by_sid.keys()):
        recs = by_sid[sid]
        if len(recs) < 2:
            continue
        groups: dict[tuple, list[dict]] = defaultdict(list)
        for u in recs:
            groups[unit_fingerprint(u)].append(u)
        if len(groups) == 1:
            continue  # все нации идентичны — пропускаем

        ordered = sorted(groups.items(), key=lambda kv: -len(kv[1]))
        rep0 = ordered[0][1][0]
        usage = USAGE_RU.get(rep0.get("usage_short"), rep0.get("usage_short", "—"))
        A(f"### `{sid}` — {usage}")
        A("")
        for idx, (_, members) in enumerate(ordered):
            rep = members[0]
            label = "**Базовый вариант**" if idx == 0 else f"**Отклонение {idx}**"
            nats = sorted({m["nation"] for m in members})
            A(f"- {label} ({len(nats)} наци{'й' if len(nats) != 1 else 'я'}): {fmt_nations(nats)}")
            A(f"  - HP **{rep.get('hp')}**, цена: {fmt_cost(rep)}, "
              f"buildtime **{rep.get('buildtime_sec')}** g-сек, "
              f"speed {rep.get('speed')}")
            extras = []
            if rep.get("shield"): extras.append(f"shield={rep['shield']}")
            if rep.get("score"): extras.append(f"score={rep['score']}")
            if rep.get("costpercent") is not None and rep.get("costpercent") != 100:
                extras.append(f"costpercent={rep['costpercent']}")
            if extras:
                A("  - " + ", ".join(extras))
            prots = []
            for k in ("pike", "sword", "bullet", "cannister", "arrow", "cannonball"):
                v = rep.get(f"prot_{k}")
                if v:
                    prots.append(f"{k}={v}")
            if prots:
                A("  - prot: " + ", ".join(prots))
            consume_str = fmt_consume(rep.get("consume"))
            if consume_str != "—":
                A(f"  - consume: {consume_str}")
            for w in (rep.get("weapons") or []):
                d = w.get("damage")
                p = w.get("pause_sec")
                rmax = w.get("radiusmax_tiles")
                kind = w.get("kind", "?")
                disp = w.get("dispertion_tiles")
                disp_str = f", disp {disp}t" if disp is not None else ""
                A(f"  - weapon[{w.get('index')}]: {d} dmg · pause {p} s · "
                  f"range {rmax} t · {kind}{disp_str}")
            A("")
        output_count += 1
    A("")
    A(f"Всего юнитов с межнациональными отклонениями: **{output_count}**.")
    A("")
    return L


def main() -> None:
    data = json.loads(DATA_JSON.read_text(encoding="utf-8"))
    buildings = data["buildings"]
    units = data["units"]

    print(f"compute_nation_deviations: zданий = {len(buildings)}, "
          f"юнитов-наций = {len(units)}")

    L: list[str] = []
    L += render_header()
    L += render_buildings_section(buildings)
    L += render_units_section(units)

    REPORTS_NATIONS_DIR.mkdir(parents=True, exist_ok=True)
    MD_PATH.write_text("\n".join(L), encoding="utf-8")
    print(f"saved -> {MD_PATH}")


if __name__ == "__main__":
    main()
