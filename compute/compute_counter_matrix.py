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

Output: output/reports/counter_matrix.md
"""
from __future__ import annotations
import sys
import json
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "parser"))
from config import (DATA_JSON, REPORTS_DIR, MELEE_SWING_FALLBACK_SEC,
                    MELEE_SWING_FALLBACK_FRAMES, melee_swing_sec)


MD_PATH = REPORTS_DIR / "counter_matrix.md"
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
    A("## Time-to-kill matrix (real-sec @ fast)")
    A("")
    A("**Cell (row=attacker, col=defender)** = сколько секунд **одному** атакующему "
      "нужно чтобы убить **одного** защитника, считая игровое время × 1.4 (fast). "
      "Учитывает protection, **не** учитывает shield/бонусы отряда/перемещение/дальность. "
      "Для артиллерии (cannon/mortar): один снаряд может зацепить нескольких — здесь "
      "считаем урон только по одной цели.")
    A("")
    A("**Чтение:** меньше — лучше для атакующего. `m̃` = ближний бой (pause=0, "
      f"swing-rate из `attack0` в .aaf для каждого юнита; fallback ≈ {MELEE_SWING_FALLBACK_SEC} g-sec). "
      "`—` = недоступно (нет оружия / hp).")
    A("")
    short_labels = [f"D{i+1}" for i in range(len(roster_units))]
    head_cells = ["#", "Attacker"] + short_labels
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
    A("**Legend** (D# = defender column = same unit as A# row):")
    A("")
    A("| # | Unit | sid · nation | HP | armor (pike/sword/bullet/cannister/arrow/cannonball) |")
    A("| ---: | --- | --- | ---: | --- |")
    for i, (label, u) in enumerate(roster):
        sid = u.get("sid") if u else "—"
        nat = u.get("nation") if u else "—"
        hp = u.get("hp") if u else "—"
        if u:
            armor = "/".join(str(u.get(f"prot_{k}") or 0) for k in PROT_KINDS)
        else:
            armor = "—"
        A(f"| {i+1} | {label} | `{sid}` · {nat} | {hp} | {armor} |")
    A("")
    return L


def render_dps_against(roster_units: list[tuple[str, dict]]) -> list[str]:
    """Effective DPS (real-sec @ fast): attacker DPS *after* defender protection."""
    L = []
    A = L.append
    A("## Матрица эффективного DPS (real-sec @ fast)")
    A("")
    A("Сколько урона **в секунду реального времени** атакующий наносит защитнику "
      "после вычета protection. `effective_dps = max(1, dmg - prot[kind]) / pause_sec × 1.4`. "
      "Ближний бой — деление на длительность `attack0` из .aaf (per-unit; "
      f"fallback ≈ {MELEE_SWING_FALLBACK_SEC} g-sec).")
    A("")
    A("Таблица **симметрична** по форме относительно TTK выше: TTK = HP / DPS, "
      "так что эта таблица позволяет быстро прикинуть «есть ли вообще шанс» (DPS близко к 1 "
      "= protection почти полностью съедает урон).")
    A("")
    short_labels = [f"D{i+1}" for i in range(len(roster_units))]
    A("| Attacker | " + " | ".join(short_labels) + " |")
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


def render_notes() -> list[str]:
    L = []
    A = L.append
    A("## Оговорки")
    A("")
    A("- **Бонусы отряда/формации** проигнорированы: `fAddDamage` (агрессивная "
      "стойка) до +50%, `fAddShieldHold` (стеновой режим) до +50 EHP.")
    A("- **Дальность** не учтена. Стрелок может бить 15 тайлов, кавалерист 1 — но "
      "матрица считает «привезли друг к другу и стреляют из позиции». Реальный "
      "исход боя зависит от `searchradius` (когда видит) против `radiusmax` (когда "
      "бьёт).")
    A("- **Перемещение.** Для танковых «шкафов» (cuirassier 300hp) дешёвый раш "
      "мушкетёров может убить за 4 сек/шт., но времени перезарядки мушкетёра "
      "достаточно, чтобы cuirassier подъехал и зарубил в ближнем бою. Этого "
      "симулятор не учитывает.")
    A(f"- **Melee swing rate** — длительность `attack0` из `data/animations/aaf/<sid>.aaf` "
      "(per-unit, разброс 11-33 кадров). Если файл отсутствует, fallback = "
      f"{MELEE_SWING_FALLBACK_FRAMES} кадров = {MELEE_SWING_FALLBACK_SEC} g-sec (медиана 84 melee-юнитов). "
      "Все melee TTK помечены `m̃`.")
    A("- **Оружие по нескольким целям** (cannon, mortar) считает урон по одному "
      "юниту. В реальности cannonball пробивает линию — в плотном строю ×3-5 "
      "эффективнее.")
    A("- **Нанесение урона:** `applied = max(1, base_dmg + squad_bonus - prot[kind])` "
      "(`miscext2.script:380, 434`). Минимум 1 даже если protection > damage — то "
      "есть **никакая броня не делает юнита бессмертным** против пик-копий, но "
      "TTK взрывается до сотен секунд.")
    A("- **Юниты 18 в. (musketeer18, pikeman18, grenadier 18)** требуют исследования "
      "century18 + соответствующего здания. Включены для сравнения, но появляются "
      "только после длительного развития экономики.")
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
        roster.append((label, u))
    if missing:
        print("WARNING: missing roster units:", missing)

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    L = []
    A = L.append
    A("# Cossacks 3 — Counter-unit matrix")
    A("")
    A("**Производный** файл (расчётный, не извлечение). Считается из "
      "`output/data.json` скриптом "
      "[`compute/compute_counter_matrix.py`](../../compute/compute_counter_matrix.py).")
    A("")
    A("## Метод")
    A("")
    A("```")
    A("effective_damage = max(1, attacker.damage − defender.protection[attacker.kind])")
    A("game_dps         = effective_damage / attacker.pause_sec       # melee: / attack0_sec from .aaf")
    A("real_dps_fast    = game_dps × 1.4")
    A("ttk_real_fast    = defender.hp / real_dps_fast")
    A("```")
    A("")
    A("Источник формулы — `miscext2.script:380, 434` (damage application). "
      "FAST = `gc_settings_gamespeed_2 = 14` → ×1.4 от game-time. Подробности и оговорки в §Оговорки.")
    A("")
    L.extend(render_matrix(roster))
    L.extend(render_dps_against(roster))
    L.extend(render_notes())
    A("---")
    A("")
    A("Сгенерировано из `output/data.json`. Для перегенерации:")
    A("")
    A("```")
    A("python compute/compute_counter_matrix.py")
    A("```")
    MD_PATH.write_text("\n".join(L), encoding="utf-8")
    print(f"Wrote {MD_PATH} ({MD_PATH.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
