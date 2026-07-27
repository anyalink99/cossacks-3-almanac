"""Per-unit DPS / EHP / armor metrics for combat balancing.

Damage flow (`miscext2.script:380`, `miscext2.script:434`):
    applied = max(1, base_damage + squad_bonus - target.protection[weapon_kind])
    target.hp -= applied

Squad bonuses (formation + standing) are ignored here — we report unmodified
unit-vs-unit numbers, treating shield as a flat reduction (the game subtracts it
**before** protection in `miscext2.script:340-354`).

Outputs (docs/reports/combat/combat_stats.md):

  §1  Unit combat sheet  — hp, speed, weapons (dmg/pause/range/kind),
                            DPS @ g-sec & @ fast-real, protections
  §2  DPS ranking        — combat units sorted by primary-weapon DPS
  §3  Effective HP       — HP and EHP vs each weapon kind (assuming
                            attacker_damage = 10 reference; user reads ratio)
  §4  Notes              — melee with pause=0, mortar/firearrow specials
"""
from __future__ import annotations
import sys
import json
from pathlib import Path
from collections import defaultdict

sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "parser"))
from config import (PLAYABLE_NATIONS, DATA_JSON, REPORTS_DIR, REPORTS_COMBAT_DIR,
                    USAGE_RU, WEAPON_KIND_RU, nation_ru)
from citations import Citations


MD_PATH = REPORTS_COMBAT_DIR / "combat_stats.md"

# Weapon kinds with a corresponding protection field on units.
PROT_KINDS = ("pike", "sword", "bullet", "cannister", "arrow", "cannonball")

COMBAT_USAGES = {
    "gc_obj_usage_lightinfantry",
    "gc_obj_usage_shooter",
    "gc_obj_usage_archer",
    "gc_obj_usage_grenadier",
    "gc_obj_usage_fasthorse",
    "gc_obj_usage_hardhorse",
    "gc_obj_usage_horseshooter",
    "gc_obj_usage_cannon",
    "gc_obj_usage_mortar",
    "gc_obj_usage_supermortar",
    "gc_obj_usage_mcannon",
}

FAST_SPEED_MULT = 1.4  # gc_settings_gamespeed_2 = 14 → ×1.4 vs game-time second
REF_DAMAGE = 10        # reference attacker damage for EHP table


def usg_ru(usg_short: str | None) -> str:
    return "—" if not usg_short else USAGE_RU.get(usg_short, usg_short)


def kind_ru(kind: str | None) -> str:
    return "—" if not kind else WEAPON_KIND_RU.get(kind, kind)


def primary_weapon(u: dict) -> dict | None:
    """Pick the role-defining weapon. Prefer ranged (pause > 0) over melee — a unit
    with both (e.g. musketeer18 = bayonet at index 0, musket at index 1) is identified
    strategically by its ranged weapon, not its emergency-bayonet."""
    candidates = [w for w in (u.get("weapons") or []) if w.get("kind") not in (None, "heal")]
    if not candidates:
        return None
    ranged = [w for w in candidates if (w.get("pause_sec") or 0) > 0 and (w.get("damage") or 0) > 0]
    if ranged:
        return max(ranged, key=lambda w: (w.get("damage") or 0) / (w.get("pause_sec") or 0.01))
    return max(candidates, key=lambda w: w.get("damage") or 0)


def dps_g_sec(weapon: dict | None) -> float | None:
    if not weapon:
        return None
    d = weapon.get("damage") or 0
    p = weapon.get("pause_sec") or 0
    if p <= 0:
        return None
    return round(d / p, 2)


def fmt_w(w: dict | None) -> str:
    if not w:
        return "—"
    d = w.get("damage")
    p = w.get("pause_sec")
    r = w.get("radiusmax_tiles")
    k = kind_ru(w.get("kind"))
    p_disp = f"{p} с" if p and p > 0 else "ближний бой"
    return f"{d} урона / {p_disp} / {r} тайла / {k}"


def fmt_protection(u: dict) -> str:
    parts = []
    for k in PROT_KINDS:
        v = u.get(f"prot_{k}")
        if v is not None and v != 0:
            parts.append(f"{kind_ru(k)}={v}")
    if u.get("shield"):
        parts.append(f"общая броня={u['shield']}")
    return ", ".join(parts) if parts else "—"


def ehp_vs(u: dict, kind: str, ref_damage: int = REF_DAMAGE) -> float:
    """HP / damage_per_hit when attacker deals `ref_damage` of `kind`. Uses
    `applied = max(1, ref_damage - prot[kind])` per damage formula above."""
    prot = u.get(f"prot_{kind}") or 0
    applied = max(1, ref_damage - prot)
    hp = u.get("hp") or 0
    if hp <= 0:
        return 0.0
    return round(hp / applied, 1)


def _row_key(u: dict) -> tuple:
    """Sort: combat unit first, then by usage, hp, sid, nation."""
    is_combat = 0 if u.get("usage") in COMBAT_USAGES else 1
    return (is_combat, u.get("usage_short") or "", -(u.get("hp") or 0),
            u.get("sid") or "", u.get("nation") or "")


def _stats_fingerprint(u: dict) -> tuple:
    """Stats-only fingerprint (sid + the values shown on a row). Two unit-rows with
    identical fingerprints merge into one row with a 'nations' column."""
    weapons = []
    for w in u.get("weapons") or []:
        weapons.append((
            w.get("damage"), w.get("pause_sec"), w.get("radiusmax_tiles"),
            w.get("kind"),
        ))
    return (
        u.get("sid"),
        u.get("usage"),
        u.get("hp"),
        u.get("speed"),
        u.get("shield"),
        tuple(weapons),
        tuple(u.get(f"prot_{k}") or 0 for k in PROT_KINDS),
    )


def group_by_fingerprint(units: list[dict]) -> list[tuple[dict, list[str]]]:
    """Return list of (representative_unit, sorted_nation_list). Preserves
    'first-encountered' order so combat units (which sort early) stay early."""
    groups: dict[tuple, tuple[dict, list[str]]] = {}
    for u in units:
        fp = _stats_fingerprint(u)
        if fp not in groups:
            groups[fp] = (u, [])
        groups[fp][1].append(u.get("nation"))
    out = []
    for fp, (rep, nats) in groups.items():
        out.append((rep, sorted(set(nats))))
    return out


def fmt_nation_list(nations: list[str]) -> str:
    if not nations:
        return "—"
    if len(nations) == len(PLAYABLE_NATIONS):
        return "все 21"
    if len(nations) > 8:
        head = ", ".join(
            f"**{nation_ru(n)}** (`{n}`)"
            for n in nations[:5]
        )
        return f"{head} … (+{len(nations) - 5})"
    return ", ".join(
        f"**{nation_ru(n)}** (`{n}`)"
        for n in nations
    )


def render_unit_sheet(groups: list[tuple[dict, list[str]]]) -> list[str]:
    L = []
    A = L.append
    A("## §1. Сводная таблица боевых юнитов")
    A("")
    A("Одна строка соответствует одному уникальному набору характеристик. "
      "Колонка **Нации** показывает, где доступен этот вариант. "
      "Если у юнита разные значения у разных наций (например `pikemanpol` имеет "
      "половину брони от стандарта) — это разные строки.")
    A("")
    A("Показаны здоровье, внутренняя скорость, основное оружие, урон в "
      "игровую и реальную секунду на скорости «Быстро», защиты от разных "
      "типов оружия и общая броня. У юнита может быть несколько видов оружия — "
      "показано **сильнейшее по соотношению урон/пауза**.")
    A("")
    A("| Юнит | Нации | Роль | Здоровье | Скорость | Основное оружие | Урон/игр. с | Урон/реал. с на «Быстро» | Защиты |")
    A("| --- | --- | --- | ---: | ---: | --- | ---: | ---: | --- |")
    sorted_groups = sorted(groups, key=lambda g: _row_key(g[0]))
    for u, nats in sorted_groups:
        if u.get("usage") not in COMBAT_USAGES:
            continue
        w = primary_weapon(u)
        d_g = dps_g_sec(w)
        d_r = round(d_g * FAST_SPEED_MULT, 2) if d_g is not None else None
        cells = [
            f"**{u.get('name_ru') or u.get('name_en') or u['sid']}** (`{u['sid']}`)",
            fmt_nation_list(nats),
            usg_ru(u.get("usage_short")),
            str(u.get("hp") or "—"),
            str(u.get("speed") or "—"),
            fmt_w(w),
            f"{d_g}" if d_g is not None else "—",
            f"{d_r}" if d_r is not None else "—",
            fmt_protection(u),
        ]
        A("| " + " | ".join(cells) + " |")
    A("")
    return L


def render_dps_ranking(groups: list[tuple[dict, list[str]]]) -> list[str]:
    L = []
    A = L.append
    A("## §2. Рейтинг урона в секунду")
    A("")
    A("Включены боевые юниты с дистанционным оружием. Ближний бой вынесен из "
      "рейтинга, потому что его темп задаётся анимацией удара. Реальное "
      "значение на скорости «Быстро» в 1,4 раза выше игрового.")
    A("")
    rows = []
    for u, nats in groups:
        if u.get("usage") not in COMBAT_USAGES:
            continue
        w = primary_weapon(u)
        d_g = dps_g_sec(w)
        if d_g is None:
            continue
        rows.append((u, nats, w, d_g))
    rows.sort(key=lambda x: -x[3])
    A("| # | Юнит | Нации | Роль | Здоровье | Тип оружия | Урон | Перезарядка (с) | Дальность (тайлы) | Урон/игр. с | Урон/реал. с |")
    A("| ---: | --- | --- | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |")
    for i, (u, nats, w, d_g) in enumerate(rows, 1):
        name = u.get("name_ru") or u.get("name_en") or u["sid"]
        A(f"| {i} | **{name}** (`{u['sid']}`) | {fmt_nation_list(nats)} | "
          f"{usg_ru(u.get('usage_short'))} | {u.get('hp') or '—'} | "
          f"{kind_ru(w.get('kind'))} | {w.get('damage') or '—'} | "
          f"{w.get('pause_sec')} | {w.get('radiusmax_tiles')} | "
          f"{d_g} | {round(d_g * FAST_SPEED_MULT, 2)} |")
    A("")
    return L


def render_ehp_table(groups: list[tuple[dict, list[str]]], cites: Citations) -> list[str]:
    L = []
    A = L.append
    A(f"## §3. Живучесть против атаки силой {REF_DAMAGE}")
    A("")
    A(f"Таблица показывает, сколько ударов выдержит юнит, если по нему бьёт "
      f"оружие определённого типа с базовым уроном {REF_DAMAGE}. Для атак с "
      f"бо́льшим или меньшим уроном результат меняется пропорционально, пока "
      f"урон выше защиты. Даже если защита полностью поглощает атаку, движок "
      f"всё равно снимает минимум единицу здоровья "
      f"{cites.cite('lib/miscext2.script:381', label='минимальный урон равен единице')}.")
    A("")
    A("Включены только юниты, у которых есть ненулевая защита хотя бы от "
      "одного типа оружия.")
    A("")
    A("| Юнит | Нации | Роль | Здоровье | Общая броня | Пика | Меч | Пуля | Картечь | Стрела | Ядро |")
    A("| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    sorted_groups = sorted(groups, key=lambda g: _row_key(g[0]))
    for u, nats in sorted_groups:
        if not any(u.get(f"prot_{k}") for k in PROT_KINDS):
            continue
        cells = [
            f"**{u.get('name_ru') or u.get('name_en') or u['sid']}** (`{u['sid']}`)",
            fmt_nation_list(nats),
            usg_ru(u.get("usage_short")),
            str(u.get("hp") or "—"),
            str(u.get("shield") or "—"),
        ]
        for k in PROT_KINDS:
            cells.append(str(ehp_vs(u, k)))
        A("| " + " | ".join(cells) + " |")
    A("")
    return L


def render_notes(cites: Citations) -> list[str]:
    L = []
    A = L.append
    A("## §4. Замечания и оговорки")
    A("")
    A("- **Ближний бой** — урон в секунду здесь не считается. Урон "
      "наносится по триггеру анимационного кадра (`onaclanimationreachedwork`), "
      "цикл ~25–32 кадра ≈ 1 удар за игровую секунду. Точное значение требует "
      "замера (FPS анимаций не подтверждён эмпирически).")
    A("- **Бонусы отряда** проигнорированы. `fAddDamage` (наступательный) и "
      "`fAddShield`/`fAddShieldHold` (стеновой режим) могут добавлять до +50% "
      "к урону и до +50 к защите — но они зависят от построения и состояния, а не "
      "от юнита. Сравнение в этой таблице — базовые статы против базовых.")
    A("- **Миномётная бомба и огненная стрела** — отдельные типы оружия без "
      "собственного показателя защиты. Они входят в расчёт урона, но в §3 не "
      "показаны (защиты нет).")
    A("- **Оружие `heal`** у священника исключено из всех расчётов — это "
      "неагрессивная способность.")
    A(f"- **Скорость 32** на пехоте — это базовое значение движка. Реальная скорость "
      f"крестьянина (`gc_obj_speed_peasant=40`) **закомментирована** "
      f"{cites.cite('lib/unit.script:1192', label='закомментированное `objbase.speed := gc_obj_speed_peasant`')}, "
      f"по умолчанию применяется `objbase.speed:=1`. Числа в столбце скорости — "
      f"таблица констант "
      f"{cites.cite('dmscript.global:603-620', label='таблица `gc_obj_speed_*`')}, "
      f"то есть _декларированные_ значения, не верифицированные эмпирически.")
    A("- **Реальное время.** На скорости «Быстро» умножьте урон за игровую "
      "секунду на 1,4. На скорости «Нормально» значение не меняется.")
    A("")
    return L


def main():
    data = json.loads(DATA_JSON.read_text(encoding="utf-8"))
    units = data["units"]
    MD_PATH.parent.mkdir(parents=True, exist_ok=True)

    cites = Citations()
    L = []
    A = L.append
    A("# Боевые характеристики")
    A("")
    A("[← Таблицы и расчёты](../README.md)")
    A("")
    A("## Формула урона")
    A("")
    formula_cite = cites.cite(
        "lib/miscext2.script:380, 434",
        label="`_misc_DoDamage` — вычитание защиты и срабатывание хедшота",
    )
    A(f"Игра вычитает из базового урона броню и защиту от конкретного типа "
      f"оружия {formula_cite}. Итог никогда не бывает меньше единицы:")
    A("")
    A("```")
    A("итоговый урон = max(1, базовый урон + бонус построения − защита цели)")
    A("здоровье цели = здоровье цели − итоговый урон")
    A("```")
    A("")
    A(f"На скорости «Быстро» реальный урон в секунду в {FAST_SPEED_MULT} раза "
      "выше урона за игровую секунду.")
    A("")
    groups = group_by_fingerprint(units)
    L.extend(render_unit_sheet(groups))
    L.extend(render_dps_ranking(groups))
    L.extend(render_ehp_table(groups, cites))
    L.extend(render_notes(cites))
    L.extend(cites.render())
    MD_PATH.write_text("\n".join(L), encoding="utf-8")
    print(f"Wrote {MD_PATH} ({MD_PATH.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
