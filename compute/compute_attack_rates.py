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
                    melee_swing_sec, get_anim_sec, REPORTS_COMBAT_DIR)

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
        return "all"
    if len(nats) > 6:
        return f"{', '.join(nats[:4])} … (+{len(nats) - 4})"
    return ", ".join(nats)


def attack_cycle(u: dict, w: dict) -> tuple[float, str]:
    """Return (cycle_g_sec, source_label). Source label is shown in column."""
    pause = w.get("pause_sec") or 0
    if pause > 0:
        return (pause, "pause")
    swing = get_anim_sec(u.get("sid", ""), "attack0")
    if swing is not None:
        return (swing, "anim")
    return (MELEE_SWING_FALLBACK_SEC, "fallback")


def render_unit_rows(groups: list[tuple[dict, list[str]]]) -> list[str]:
    L = []
    A = L.append
    A("## §1. Скорость атаки по юнитам")
    A("")
    A("Одна строка на уникальный набор статов (юнит может присутствовать в "
      "нескольких нациях с одинаковыми параметрами — тогда `nations` = список).")
    A("")
    A("**Колонки:**")
    A("- **cycle_g** — длительность одного полного цикла атаки в **игровых** "
      "секундах. Для ranged = `weapon.pause_sec`. Для melee = длительность "
      "анимации `attack0` из `data/animations/aaf/<sid>.aaf`.")
    A("- **src** — откуда взято: `pause` (поле оружия), `anim` (анимация), "
      "`fallback` (нет .aaf — взят медианный 15-frame swing).")
    A("- **att/g-sec** — атак в игровую секунду = `1 / cycle_g`.")
    A(f"- **att/real-sec @ fast** — то же × {FAST_SPEED_MULT} (gc_settings_gamespeed_2).")
    A("")
    A("Сортировка: ranged → melee, внутри — по убыванию частоты атаки.")
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
                sid, usage, kind, dmg, cycle, src, rng, w.get("index"), nats,
            ))
    rows.sort()
    A("| sid | usage | weapon | dmg | range_t | cycle_g | src | att/g-sec | att/real @ fast | nations |")
    A("| --- | --- | --- | ---: | ---: | ---: | --- | ---: | ---: | --- |")
    for is_melee, neg_rate, sid, usage, kind, dmg, cycle, src, rng, idx, nats in rows:
        att_g = -neg_rate
        att_r = att_g * FAST_SPEED_MULT
        slot = f"#{idx}" if idx is not None else ""
        A(f"| `{sid}` | {usage} | {kind} {slot} | {dmg} | {rng} | "
          f"{cycle:.2f} | {src} | {att_g:.2f} | {att_r:.2f} | {fmt_nations(nats)} |")
    A("")
    return L


def render_summary_by_kind(groups: list[tuple[dict, list[str]]]) -> list[str]:
    L = []
    A = L.append
    A("## §2. Сводка по типу оружия")
    A("")
    A("Min / median / max длительности цикла для каждого `kind`. Помогает "
      "увидеть «насколько медленнее одна арбалетная атака другой» внутри "
      "класса и понять, где апгрейды `attpauseperc` дают больше всего профита.")
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
    A("| kind | n | min cycle (g-sec) | median | max | min att/real @ fast |")
    A("| --- | ---: | ---: | ---: | ---: | ---: |")
    for kind in sorted(by_kind):
        cycles = sorted(by_kind[kind])
        n = len(cycles)
        mn, mx = cycles[0], cycles[-1]
        med = cycles[n // 2]
        max_rate_real = (1.0 / mn) * FAST_SPEED_MULT
        A(f"| {kind} | {n} | {mn:.2f} | {med:.2f} | {mx:.2f} | {max_rate_real:.2f} |")
    A("")
    return L


def render_notes() -> list[str]:
    L = []
    A = L.append
    A("## §3. Замечания")
    A("")
    A("- **Pause vs swing.** В Cossacks 3 для дистанционного оружия `pause` — "
      "это полный цикл (анимация выстрела внутри pause). Для melee `pause=0` "
      "и цикл равен длине самой анимации `attack0`.")
    A(f"- **Fallback** для melee = {MELEE_SWING_FALLBACK_FRAMES} кадров "
      f"(≈ {MELEE_SWING_FALLBACK_SEC} g-sec, медиана по всем юнитам с .aaf). "
      "Применяется если для конкретного `sid` в `data/animations/aaf/` нет "
      "файла или нет трека `attack0`.")
    A("- **Multi-weapon юниты.** Musketeer18 (bayonet + musket), архер с "
      "горящими стрелами и т.п. — у них в таблице по строке на оружие, "
      "колонка `weapon` показывает `#index`.")
    A("- **`heal` исключён.** Священник = неагрессивный, не входит в боевой "
      "DPS-расчёт.")
    A("- **Real vs game.** Вся игровая логика (анимации, pause) — в "
      "**игровых** секундах. Чтобы получить реальное время на скорости fast, "
      f"делите g-sec на {FAST_SPEED_MULT} (или умножайте rate на {FAST_SPEED_MULT}).")
    A("- **Cooldown апгрейды.** `attpauseperc` (см. "
      "[`reference/05_upgrades/README.md`](../../reference/05_upgrades/README.md)) уменьшает "
      "только pause у ranged. Melee swing не апгрейдится — он привязан к "
      "анимации.")
    A("")
    return L


def main() -> None:
    data = json.loads(DATA_JSON.read_text(encoding="utf-8"))
    units = data["units"]
    MD_PATH.parent.mkdir(parents=True, exist_ok=True)

    L = []
    A = L.append
    A("# Cossacks 3 — Скорость атаки (per-unit)")
    A("")
    A("**Производный** отчёт. Считается из `data.json` + "
      "`derived/animations.json` скриптом "
      "[`compute/compute_attack_rates.py`](../../../compute/compute_attack_rates.py).")
    A("")
    A("## Модель")
    A("")
    A("Cossacks 3 не использует общую систему «атаки в секунду». Вместо неё:")
    A("")
    A("```")
    A("ranged (weapon.pause_sec > 0):   cycle = pause_sec")
    A("melee  (weapon.pause_sec = 0):   cycle = duration of attack0 animation")
    A("attacks_per_g_sec = 1 / cycle")
    A("attacks_per_real_sec @ fast = 1 / cycle × 1.4")
    A("```")
    A("")
    A("Для melee длительность `attack0` варьируется 11..33 кадра между юнитами "
      f"(median {MELEE_SWING_FALLBACK_FRAMES}). Источник: "
      "`data/animations/aaf/<sid>.aaf` → `derived/animations.json`.")
    A("")
    groups = group_by_fingerprint(units)
    L.extend(render_unit_rows(groups))
    L.extend(render_summary_by_kind(groups))
    L.extend(render_notes())
    A("---")
    A("")
    A("Перегенерация: `python compute/compute_attack_rates.py`")
    MD_PATH.write_text("\n".join(L), encoding="utf-8")
    print(f"Wrote {MD_PATH} ({MD_PATH.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
