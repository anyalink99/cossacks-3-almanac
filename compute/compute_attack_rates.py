"""Per-unit attack rate (swing / pause / attacks per sec).

Cossacks 3 has two attack-cycle models:
  - Ranged (`weapon.pause > 0`): cycle = pause_sec. Attack rate = 1 / pause_sec.
    The animation overlaps with the pause; pause IS the cooldown.
  - Melee (`weapon.pause = 0`): cycle = `attack0` animation length, looked up
    per-unit in `data/animations/aaf/<sid>.aaf` (parser/parse_animations.py
    extracts these). Falls back to median (15 frames ≈ 0.47 g-sec) when
    the .aaf file is missing or doesn't expose attack0.

This makes "attacks per second" a derived quantity that's awkward to extract
from data.json by eye — the consumer has to know which model applies and
which animation lookup to do. This report surfaces the answer for every
weapon-bearing unit, in both g-sec and real-sec @ fast (×1.4).

Output: docs/reports/combat/attack_rates.md
"""
from __future__ import annotations
import sys
import json
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "parser"))
from config import (DATA_JSON, REPORTS_DIR, PLAYABLE_NATIONS,
                    MELEE_SWING_FALLBACK_FRAMES, MELEE_SWING_FALLBACK_SEC,
                    melee_swing_sec, get_anim_sec, REPORTS_COMBAT_DIR,
                    USAGE_RU, WEAPON_KIND_RU, nation_ru, unit_ru)

MD_PATH = REPORTS_COMBAT_DIR / "attack_rates.md"
FAST_SPEED_MULT = 1.4


def _stats_fingerprint(u: dict) -> tuple:
    """Same shape as compute_combat_stats — collapses identical stats across nations."""
    weapons = []
    for w in u.get("weapons") or []:
        weapons.append((
            w.get("damage"), w.get("pause_sec"), w.get("radiusmax_tiles"),
            w.get("kind"),
        ))
    return (u.get("sid"), u.get("usage"), u.get("hp"), tuple(weapons))


def group_by_fingerprint(units: list[dict]) -> list[tuple[dict, list[str]]]:
    groups: dict[tuple, tuple[dict, list[str]]] = {}
    for u in units:
        fp = _stats_fingerprint(u)
        if fp not in groups:
            groups[fp] = (u, [])
        groups[fp][1].append(u.get("nation"))
    return [(rep, sorted(set(nats))) for fp, (rep, nats) in groups.items()]


def fmt_nations(nats: list[str]) -> str:
    if not nats:
        return "—"
    if len(nats) == len(PLAYABLE_NATIONS):
        return "все"
    if len(nats) > 6:
        head = ", ".join(nation_ru(nat) for nat in nats[:4])
        return f"{head} … (+{len(nats) - 4})"
    return ", ".join(nation_ru(nat) for nat in nats)


def attack_cycle(u: dict, w: dict) -> tuple[float, str]:
    """Return (cycle_g_sec, source_label). Source label is shown in column."""
    pause = w.get("pause_sec") or 0
    if pause > 0:
        return (pause, "перезарядка")
    swing = get_anim_sec(u.get("sid", ""), "attack0")
    if swing is not None:
        return (swing, "анимация")
    return (MELEE_SWING_FALLBACK_SEC, "оценка")


def render_unit_rows(groups: list[tuple[dict, list[str]]]) -> list[str]:
    L = []
    A = L.append
    A("## §1. Скорость атаки по юнитам")
    A("")
    A("Одна строка соответствует одному оружию юнита. Если характеристики "
      "одинаковы у нескольких наций, они объединены.")
    A("")
    A("**Длительность цикла** — время от одной атаки до следующей в игровых "
      "секундах. Для стрелкового оружия она равна перезарядке, для ближнего "
      "боя — длительности анимации удара. **Источник «оценка»** означает, что "
      "у юнита нет читаемой анимации и использовано медианное значение.")
    A("")
    A("Сначала показано стрелковое оружие, затем ближний бой; внутри группы "
      "строки отсортированы от самой быстрой атаки к самой медленной.")
    A("")
    rows: list[tuple] = []
    for u, nats in groups:
        sid = u.get("sid", "")
        usage = (u.get("usage_short") or u.get("usage") or "")
        for w in (u.get("weapons") or []):
            kind = w.get("kind")
            dmg = w.get("damage") or 0
            if not kind or kind == "heal" or dmg <= 0:
                continue
            cycle, src = attack_cycle(u, w)
            if cycle <= 0:
                continue
            attg = 1.0 / cycle
            rng = w.get("radiusmax_tiles") or 0
            is_melee = (w.get("pause_sec") or 0) == 0
            rows.append((
                is_melee,           # ranged first (False)
                -attg,              # higher rate first
                sid, unit_ru(sid, u.get("name_ru") or u.get("name_en") or sid),
                usage, kind, dmg, cycle, src, rng, w.get("index"), nats,
            ))
    rows.sort()
    A("| Юнит | Роль | Оружие | Урон | Дальность (клетки) | Цикл (игр. с) | Источник | Атак/игр. с | Атак/реал. с на «Быстро» | Нации |")
    A("| --- | --- | --- | ---: | ---: | ---: | --- | ---: | ---: | --- |")
    for is_melee, neg_rate, sid, name, usage, kind, dmg, cycle, src, rng, idx, nats in rows:
        att_g = -neg_rate
        att_r = att_g * FAST_SPEED_MULT
        slot = f"#{idx}" if idx is not None else ""
        A(f"| **{name}** (`{sid}`) | {USAGE_RU.get(usage, usage)} "
          f"| {WEAPON_KIND_RU.get(kind, kind)} {slot} | {dmg} | {rng} | "
          f"{cycle:.2f} | {src} | {att_g:.2f} | {att_r:.2f} | {fmt_nations(nats)} |")
    A("")
    return L


def render_summary_by_kind(groups: list[tuple[dict, list[str]]]) -> list[str]:
    L = []
    A = L.append
    A("## §2. Сводка по типу оружия")
    A("")
    A("Минимальная, медианная и максимальная длительность цикла для каждого "
      "типа оружия. Таблица показывает общий разброс темпа атак внутри класса.")
    A("")
    by_kind: dict[str, list[float]] = {}
    for u, _ in groups:
        for w in (u.get("weapons") or []):
            kind = w.get("kind")
            dmg = w.get("damage") or 0
            if not kind or kind == "heal" or dmg <= 0:
                continue
            cycle, _ = attack_cycle(u, w)
            if cycle > 0:
                by_kind.setdefault(kind, []).append(cycle)
    A("| Тип оружия | Вариантов | Самый короткий цикл (игр. с) | Медиана | Самый длинный | Макс. атак/реал. с на «Быстро» |")
    A("| --- | ---: | ---: | ---: | ---: | ---: |")
    for kind in sorted(by_kind):
        cycles = sorted(by_kind[kind])
        n = len(cycles)
        mn, mx = cycles[0], cycles[-1]
        med = cycles[n // 2]
        max_rate_real = (1.0 / mn) * FAST_SPEED_MULT
        A(f"| {WEAPON_KIND_RU.get(kind, kind)} | {n} | {mn:.2f} | {med:.2f} "
          f"| {mx:.2f} | {max_rate_real:.2f} |")
    A("")
    return L


def render_notes() -> list[str]:
    L = []
    A = L.append
    A("## §3. Замечания")
    A("")
    A("- У стрелкового оружия перезарядка задаёт полный цикл; анимация "
      "выстрела проходит внутри этого времени. В ближнем бою цикл равен "
      "длительности самой анимации удара.")
    A(f"- Если анимация удара недоступна, используется оценка "
      f"{MELEE_SWING_FALLBACK_FRAMES} кадров, или примерно "
      f"{MELEE_SWING_FALLBACK_SEC:.2f} игровой секунды.")
    A("- У мушкетёров, гренадёров и других юнитов с несколькими видами оружия "
      "каждое оружие показано отдельной строкой.")
    A("- Лечение священников исключено: это не боевая атака.")
    A(f"- Чтобы получить реальный темп на скорости «Быстро», частота в игровых "
      f"секундах умножается на {FAST_SPEED_MULT}.")
    A("- Улучшения перезарядки ускоряют только дистанционное оружие. Темп "
      "ближнего боя привязан к анимации и такими улучшениями не меняется.")
    A("")
    return L


def main() -> None:
    data = json.loads(DATA_JSON.read_text(encoding="utf-8"))
    units = data["units"]
    MD_PATH.parent.mkdir(parents=True, exist_ok=True)

    L = []
    A = L.append
    A("# Скорость атаки")
    A("")
    A("[← Таблицы и расчёты](../README.md)")
    A("")
    A("## Модель")
    A("")
    A("Cossacks 3 не использует общую систему «атаки в секунду». Вместо неё:")
    A("")
    A("- Для стрелкового оружия цикл равен времени перезарядки.")
    A("- Для ближнего боя цикл равен длительности анимации удара.")
    A("- Число атак в игровую секунду равно `1 / длительность цикла`.")
    A("- На скорости «Быстро» реальный темп в 1,4 раза выше.")
    A("")
    A("Анимация ближнего удара занимает от 11 до 33 кадров в зависимости от "
      f"юнита; медианное значение — {MELEE_SWING_FALLBACK_FRAMES} кадров.")
    A("")
    groups = group_by_fingerprint(units)
    L.extend(render_unit_rows(groups))
    L.extend(render_summary_by_kind(groups))
    L.extend(render_notes())
    MD_PATH.write_text("\n".join(L), encoding="utf-8")
    print(f"Wrote {MD_PATH} ({MD_PATH.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
