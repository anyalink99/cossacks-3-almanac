"""Counter-unit matrix: time-to-kill for representative attacker × defender pairs.

For each (attacker, defender) pair:

    effective_damage = max(1, attacker.damage − defender.protection[attacker.weapon.kind])
    g_sec_per_hit    = attacker.weapon.pause_sec
    ttk_g_sec        = defender.hp / (effective_damage / g_sec_per_hit)
    ttk_real_fast    = ttk_g_sec / 1.4   # ×0.714 sec / g-sec

The matrix uses **representative reference units** rather than every (sid, nation)
row — 100 × 100 = 10000 cells is unreadable. Reference units are picked to span
roles (light infantry, shooter, archer, grenadier, cavalry, artillery) and are
listed with their `(sid, nation)` source so the user can verify.

Melee weapons (`pause = 0`) have no game-defined pause; their cycle is animation-
bound (~13-frame swing ≈ 0.4 g-sec assumption). They're shown with `melee` annotation
and a parametric TTK using that assumption — clearly marked.

Output: docs/reports/combat/counter_matrix.md
"""
from __future__ import annotations
import sys
import json
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "parser"))
from citations import Citations
from config import (DATA_JSON, REPORTS_COMBAT_DIR, MELEE_SWING_FALLBACK_SEC,
                    MELEE_SWING_FALLBACK_FRAMES, melee_swing_sec, nation_ru)


MD_PATH = REPORTS_COMBAT_DIR / "counter_matrix.md"
FAST_SPEED_MULT = 1.4

# Per-unit melee swing length is looked up via `melee_swing_sec(sid)` from the
# unit's .aaf file (data/animations/aaf/<sid>.aaf, attack0 frame range).
# Falls back to MELEE_SWING_FALLBACK_SEC (median across 84 melee units) when missing.

# Reference roster: (label, sid, nation). Picked so we cover canonical archetypes
# and a few national specials. Order matters — used as both row and column order.
REFERENCE_ROSTER = [
    # 17c basic
    ("Pikeman 17c (eur)",         "pikeman",      "aus"),
    ("Pikeman 17c (pol)",         "pikemanpol",   "pol"),
    ("Musketeer 17c (eur)",       "musketeer",    "fra"),
    ("Strelet (rus)",             "strelet",      "rus"),
    ("Chasseur (fra)",            "chasseur",     "fra"),
    ("Highlander (eng)",          "highlander",   "eng"),
    ("Pandur (aus)",              "pandur",       "aus"),
    ("Janissary (tur)",           "jannisary",    "tur"),
    ("Archer (alg)",              "archer",       "alg"),
    ("Tatar (tur)",               "tatar",        "tur"),
    # 18c
    ("Pikeman 18c (eur)",         "pikeman18",    "aus"),
    ("Musketeer 18c (eur)",       "musketeer18",  "aus"),
    ("Grenadier 17c (eur)",       "grenadier",    "aus"),
    ("Grenadier (pru)",           "grenadierpru", "pru"),
    # cavalry
    ("Hussar (eur)",              "hussar",       "aus"),
    ("Cuirassier (eur)",          "cuirassier",   "aus"),
    ("Reiter (eur)",              "reiter",       "aus"),
    ("Dragoon (eur)",             "dragoon",      "aus"),
    ("Sipahi (tur)",              "sipahi",       "tur"),
    ("Cossack-don (rus)",         "cossackdon",   "rus"),
    # artillery
    ("Cannon (eur)",              "cannon",       "aus"),
    ("Mortar (eur)",              "mortar",       "aus"),
]

PROT_KINDS = ("pike", "sword", "bullet", "cannister", "arrow", "cannonball")


def find_unit(units: list[dict], sid: str, nation: str) -> dict | None:
    for u in units:
        if u.get("sid") == sid and u.get("nation") == nation:
            return u
    return None


def primary_weapon(u: dict | None) -> dict | None:
    """Pick the role-defining weapon. Prefer ranged (pause > 0) over melee, since
    a unit with both (e.g. musketeer18 = bayonet + musket) is identified by its
    ranged weapon strategically. Within ranged, pick highest DPS; within melee,
    pick highest damage."""
    if not u:
        return None
    candidates = [w for w in (u.get("weapons") or []) if w.get("kind") not in (None, "heal")]
    if not candidates:
        return None
    ranged = [w for w in candidates if (w.get("pause_sec") or 0) > 0 and (w.get("damage") or 0) > 0]
    if ranged:
        return max(ranged, key=lambda w: (w.get("damage") or 0) / (w.get("pause_sec") or 0.01))
    return max(candidates, key=lambda w: w.get("damage") or 0)


def effective_damage(attacker_dmg: int, defender: dict, kind: str) -> int:
    """Apply protection. min damage = 1 (`miscext2.script:381`)."""
    prot = defender.get(f"prot_{kind}") or 0
    return max(1, attacker_dmg - prot)


def ttk_real_sec(attacker: dict, defender: dict, w: dict) -> tuple[float | None, str]:
    """Returns (ttk_real_seconds, note) where note explains anomalies (melee, immune)."""
    kind = w.get("kind")
    dmg = w.get("damage") or 0
    pause = w.get("pause_sec") or 0
    if dmg <= 0:
        return (None, "no-dmg")
    target_hp = defender.get("hp") or 0
    if target_hp <= 0:
        return (None, "no-hp")

    # Some kinds (mortarball, firearrow) bypass standard protection. Use raw dmg.
    if kind in PROT_KINDS:
        ed = effective_damage(dmg, defender, kind)
    else:
        ed = max(1, dmg)
    if pause <= 0:
        # Melee — per-unit attack0 length from the unit's .aaf file (falls back to median).
        swing = melee_swing_sec(attacker.get("sid", ""))
        ttk_g = target_hp / ed * swing
        return (round(ttk_g / FAST_SPEED_MULT, 1), "melee")
    ttk_g = target_hp / ed * pause
    return (round(ttk_g / FAST_SPEED_MULT, 1), "")


def render_matrix(roster_units: list[tuple[str, dict]]) -> list[str]:
    """Render a TTK matrix. Rows = attackers, columns = defenders. Cell = real-sec
    @ fast-speed for one attacker to kill one defender, no movement, no shield/squad."""
    L = []
    A = L.append
    A("## Время победы в поединке")
    A("")
    A("Ячейка показывает, сколько реальных секунд на скорости «Быстро» нужно "
      "**одному** атакующему, чтобы победить **одного** защитника. "
      "Учитывается защита от типа оружия, но не учитываются щит отряда, "
      "перемещение и дальность. Для артиллерии один снаряд может зацепить нескольких — здесь "
      "считаем урон только по одной цели.")
    A("")
    A("**Как читать:** меньше — лучше для атакующего. Знак `m̃` отмечает "
      "ближний бой, где темп зависит от анимации удара. `—` означает, что "
      "у юнита нет подходящего оружия или запаса здоровья.")
    A("")
    short_labels = [f"D{i+1}" for i in range(len(roster_units))]
    head_cells = ["№", "Атакующий"] + short_labels
    A("| " + " | ".join(head_cells) + " |")
    sep = ["---", "---"] + ["---:" for _ in short_labels]
    A("| " + " | ".join(sep) + " |")
    roster = list(roster_units)
    for i, (label_a, u_a) in enumerate(roster):
        w_a = primary_weapon(u_a)
        cells = [f"A{i+1}", label_a]
        for j, (label_d, u_d) in enumerate(roster):
            if u_a is None or u_d is None:
                cells.append("—")
                continue
            if w_a is None:
                cells.append("—")
                continue
            ttk, note = ttk_real_sec(u_a, u_d, w_a)
            if ttk is None:
                cells.append("—")
            else:
                marker = "m̃" if note == "melee" else ""
                cells.append(f"{ttk}{marker}")
        A("| " + " | ".join(cells) + " |")
    A("")
    # Legend table — explains short labels
    A("**Обозначения:** D# — столбец защитника с тем же номером, что строка A#.")
    A("")
    A("| № | Юнит | Код · нация | Здоровье | Защита: пика / меч / пуля / картечь / стрела / ядро |")
    A("| ---: | --- | --- | ---: | --- |")
    for i, (label, u) in enumerate(roster):
        sid = u.get("sid") if u else "—"
        nat = u.get("nation") if u else "—"
        hp = u.get("hp") if u else "—"
        if u:
            armor = "/".join(str(u.get(f"prot_{k}") or 0) for k in PROT_KINDS)
        else:
            armor = "—"
        A(f"| {i+1} | {label} | `{sid}` · {nation_ru(nat)} | {hp} | {armor} |")
    A("")
    return L


def render_dps_against(roster_units: list[tuple[str, dict]]) -> list[str]:
    """Effective DPS (real-sec @ fast): attacker DPS *after* defender protection."""
    L = []
    A = L.append
    A("## Урон в секунду по каждому защитнику")
    A("")
    A("Сколько урона **в секунду реального времени** атакующий наносит защитнику "
      "после вычета защиты. Для ближнего боя используется длительность "
      "анимации удара конкретного юнита.")
    A("")
    A("Таблица позволяет увидеть, насколько защита цели поглощает атаку. "
      "Значение около единицы означает, что почти весь базовый урон нейтрализован.")
    A("")
    short_labels = [f"D{i+1}" for i in range(len(roster_units))]
    A("| Атакующий | " + " | ".join(short_labels) + " |")
    A("| --- | " + " | ".join("---:" for _ in short_labels) + " |")
    for i, (label_a, u_a) in enumerate(roster_units):
        w_a = primary_weapon(u_a)
        cells = [f"A{i+1} · {label_a}"]
        for j, (label_d, u_d) in enumerate(roster_units):
            if u_a is None or u_d is None or w_a is None:
                cells.append("—")
                continue
            kind = w_a.get("kind")
            dmg = w_a.get("damage") or 0
            pause = w_a.get("pause_sec") or 0
            if dmg <= 0:
                cells.append("—")
                continue
            if kind in PROT_KINDS:
                ed = effective_damage(dmg, u_d, kind)
            else:
                ed = max(1, dmg)
            if pause <= 0:
                dps_g = ed / melee_swing_sec(u_a.get("sid", ""))
                marker = "m̃"
            else:
                dps_g = ed / pause
                marker = ""
            dps_real = round(dps_g * FAST_SPEED_MULT, 1)
            cells.append(f"{dps_real}{marker}")
        A("| " + " | ".join(cells) + " |")
    A("")
    return L


def render_notes(cites: Citations) -> list[str]:
    L = []
    A = L.append
    A("## Оговорки")
    A("")
    A("- **Бонусы построения** не учитываются. Агрессивный строй может увеличить "
      "урон до 50%, а оборонительный — добавить до 50 единиц защиты.")
    A("- **Дальность** не учитывается. Стрелок часто начинает бой раньше "
      "кавалериста, поэтому исход настоящей стычки зависит не только от чисел "
      "в таблице.")
    A("- **Перемещение** не моделируется. Тяжёлый кавалерист может успеть "
      "сблизиться с мушкетёром во время перезарядки и полностью изменить исход "
      "поединка.")
    A(f"- **Темп ближнего боя** берётся из анимации удара каждого юнита "
      f"(обычно 11–33 кадра). Если точных данных нет, используется медиана: "
      f"{MELEE_SWING_FALLBACK_FRAMES} кадров, или {MELEE_SWING_FALLBACK_SEC} игровой секунды. "
      "Такие значения помечены `m̃`.")
    A("- **Оружие по площади** здесь поражает только одну цель. В настоящем "
      "плотном строю ядро или взрыв мортиры могут задеть нескольких юнитов.")
    A(f"- **Нанесение урона:** `итог = максимум(1, урон + бонус строя − защита)` "
      f"{cites.cite('lib/miscext2.script:380, 434', label='`_misc_DoDamage` — нанесение урона')}. "
      f"Минимум 1 действует даже тогда, когда защита выше урона: броня не "
      f"делает юнита бессмертным, но бой может растянуться на сотни секунд.")
    A("- **Юниты XVIII века** требуют перехода в новую эпоху и соответствующего "
      "здания. Они включены для сравнения, хотя появляются только после "
      "длительного развития экономики.")
    A("")
    return L


def main():
    data = json.loads(DATA_JSON.read_text(encoding="utf-8"))
    units = data["units"]

    roster: list[tuple[str, dict | None]] = []
    missing = []
    for label, sid, nat in REFERENCE_ROSTER:
        u = find_unit(units, sid, nat)
        if u is None:
            missing.append((label, sid, nat))
        reader_label = (
            u.get("name_ru") or u.get("name_en") or label
            if u is not None else label
        )
        roster.append((reader_label, u))
    if missing:
        print("WARNING: missing roster units:", missing)

    MD_PATH.parent.mkdir(parents=True, exist_ok=True)
    cites = Citations()
    L = []
    A = L.append
    A("# Кто кого побеждает")
    A("")
    A("[← Таблицы и расчёты](../README.md)")
    A("")
    A("Приблизительное сравнение выбранных типичных юнитов в поединке один на один. "
      "Это расчёт по характеристикам, а не симуляция движения целых отрядов.")
    A("")
    A("## Метод")
    A("")
    A("```text")
    A("урон после защиты = максимум(1, базовый урон − защита от типа оружия)")
    A("урон в секунду = урон после защиты / длительность цикла атаки")
    A("время победы = здоровье защитника / урон в секунду")
    A("```")
    A("")
    A(f"Источник формулы — `_misc_DoDamage` "
      f"{cites.cite('lib/miscext2.script:380, 434', label='`_misc_DoDamage` — нанесение урона')}. "
      f"Результат пересчитан в реальное время на скорости «Быстро» (×1,4). "
      f"Подробности и ограничения перечислены ниже.")
    A("")
    L.extend(render_matrix(roster))
    L.extend(render_dps_against(roster))
    L.extend(render_notes(cites))
    L.extend(cites.render())
    MD_PATH.write_text("\n".join(L), encoding="utf-8")
    print(f"Wrote {MD_PATH} ({MD_PATH.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
