"""Vision and searchradius lookup table.

Cossacks 3 has TWO concentric "awareness" radii:
  - vision        — fog-of-war reveal radius. Engine callback `_unit_GetVision`
                    (unit.script:11565) returns `floor(20 + 4 × vision)` in tiles.
                    Values 0..8 stored in `objprop.vision`.
  - searchradius  — auto-attack target-acquisition radius. Stored in pixels
                    (`gc_pixels_to_tile = 53.333`). What `bartprepare` /
                    `_unit_SearchTarget` actually use to find a target.

Units appear in fog when their actual position enters someone's vision-circle.
A unit can see further than it can fire (vision > searchradius for everyone).
A standing-ground shooter detects on the full searchradius; a moving one is
clipped by `addradius` rules (see 02_combat → "Бонус к дальности в покое").

Output: docs/reports/combat/vision_radii.md
"""
from __future__ import annotations
import sys
import json
from pathlib import Path
from collections import defaultdict

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "parser"))
from config import DATA_JSON, REPORTS_DIR, PLAYABLE_NATIONS, REPORTS_COMBAT_DIR

MD_PATH = REPORTS_COMBAT_DIR / "vision_radii.md"

# Engine constants (unit.script:11570-11571).
VISION_BASE = 20
VISION_MOD = 4


def vision_tiles(vision_field: int) -> int:
    """Return real fog-of-war reveal radius in tiles."""
    return VISION_BASE + VISION_MOD * (vision_field or 0)


def render_legend() -> list[str]:
    L = []
    A = L.append
    A("## Формула")
    A("")
    A("Радиус обзора в тайлах = `floor(20 + 4 × vision)`, где `vision` — "
      "поле в `objprop`, ЦЕЛОЕ число (обычно 0..8). Источник — "
      "`_unit_GetVision` в `unit.script:11565`.")
    A("")
    A("| `vision` | tiles | Кто типичный носитель |")
    A("| ---: | ---: | --- |")
    rows = [
        (0, "Default minimum (peasant fallback)"),
        (1, "Бо́льшая часть пехоты, артиллерия, башня без апгрейдов"),
        (2, "Лёгкая пехота, конница средней зоркости"),
        (3, "Драгуны, средняя кавалерия, башня с апгрейдом"),
        (4, "Скауты, разведка, ukr-крестьянин"),
        (5, "Hussar prussian, dragoon18 piedmontese"),
        (7, "Hetman (топ-обзор среди тяжёлой кавалерии)"),
        (8, "Drummer/Bagpiper, корабли (Battleship/Frigate)"),
    ]
    for v, who in rows:
        A(f"| {v} | **{vision_tiles(v)}** | {who} |")
    A("")
    return L


def render_unit_table(units: list[dict]) -> list[str]:
    L = []
    A = L.append
    A("## §1. Полная таблица: vision (FOW) и searchradius (target acquisition) по юнитам")
    A("")
    A("Группировка: одна строка на уникальный набор `(sid, vision, searchradius_tiles)`. "
      "Колонка **searchradius** — pause `weapon[0].radiusmax_tiles` (или 0 если оружие нет / melee=0).")
    A("")
    seen: dict[tuple, list[str]] = defaultdict(list)
    for u in units:
        sid = u.get("sid", "")
        v = u.get("vision") or 0
        sr_tile = u.get("searchradius_tiles") or 0
        sr_px = u.get("searchradius_px") or 0
        usg = u.get("usage_short") or "?"
        key = (usg, sid, v, sr_tile, sr_px)
        seen[key].append(u.get("nation"))
    rows = []
    for key, nats in seen.items():
        usg, sid, v, sr_tile, sr_px = key
        rows.append((-vision_tiles(v), usg, sid, v, sr_tile, sr_px, sorted(set(nats))))
    rows.sort()
    A("| usage | sid | vision | fov tiles | searchradius (tiles) | nations |")
    A("| --- | --- | ---: | ---: | ---: | --- |")
    for _, usg, sid, v, sr_tile, sr_px, nats in rows:
        nat_str = "all" if len(nats) == len(PLAYABLE_NATIONS) else (
            ", ".join(nats[:6]) + (f" … (+{len(nats)-6})" if len(nats) > 6 else ""))
        A(f"| {usg} | `{sid}` | {v} | **{vision_tiles(v)}** | "
          f"{sr_tile if sr_tile else '—'} | {nat_str} |")
    A("")
    return L


def render_building_table(buildings: list[dict]) -> list[str]:
    L = []
    A = L.append
    A("## §2. Vision у зданий")
    A("")
    A("В отличие от юнитов, у большинства зданий `vision=0` или поле не "
      "задано — обзор обеспечивается «врезкой» из FOW callback'а на самом "
      "здании (engine native). Здесь — те, у кого vision явно прописан.")
    A("")
    rows = []
    for b in buildings:
        v = b.get("vision") or 0
        if v == 0:
            continue
        usg = (b.get("name_ru") or b.get("usage_short") or b.get("sid") or "?")
        rows.append((usg, b.get("sid"), v, b.get("nation")))
    rows.sort()
    if not rows:
        A("_Здания с явным `vision>0` не найдены — все используют default._")
        A("")
        return L
    A("| usage | sid | vision | fov tiles | nation |")
    A("| --- | --- | ---: | ---: | --- |")
    seen = set()
    for usg, sid, v, nat in rows:
        if (sid, v) in seen:
            continue
        seen.add((sid, v))
        A(f"| {usg} | `{sid}` | {v} | **{vision_tiles(v)}** | {nat} |")
    A("")
    return L


def render_notes() -> list[str]:
    L = []
    A = L.append
    A("## §3. Замечания")
    A("")
    A("- **Vision > searchradius** для всех юнитов кроме мортир (mortar/super "
      "mortar) и башен с пустым `searchradius`. Это значит: юнит **видит** "
      "врага раньше, чем может **обнаружить как цель**.")
    A("- **Default `vision=0`** даёт всё ещё 20 тайлов обзора — минимальный "
      "круг, чтобы юнит вообще видел окружение.")
    A("- **Drummer/Bagpiper** имеют `vision=8` ⇒ **52 тайла обзора**, при "
      "этом не атакуют (`searchradius=0`). Это лучший «чистый скаут» в игре.")
    A("- **Корабли** (Battleship/Frigate) `vision=8` — нужен для морских "
      "патрулей, далеко за пределы artillery range.")
    A("- **Hetman** (Ukraine) `vision=7` — самый зоркий конный юнит на берегу.")
    A("- **Vision не апгрейдится.** В `efficiency_upgrades.md` нет записи на "
      "`visionperc` или `+vision`.")
    A("")
    return L


def main() -> None:
    data = json.loads(DATA_JSON.read_text(encoding="utf-8"))
    units = data["units"]
    buildings = data["buildings"]
    MD_PATH.parent.mkdir(parents=True, exist_ok=True)

    L = []
    A = L.append
    A("# Cossacks 3 — Vision и searchradius")
    A("")
    A("**Производный** отчёт. Считается из `docs/data.json` скриптом "
      "[`compute/compute_vision.py`](../../compute/compute_vision.py).")
    A("")
    A("Cossacks 3 имеет два концентрических радиуса «осведомлённости»:")
    A("")
    A("- **vision** — радиус развёртывания fog-of-war (FOW). Сколько тайлов "
      "вокруг юнита открыты на миникарте и игровом экране для владельца.")
    A("- **searchradius** — радиус **обнаружения цели для авто-атаки**. "
      "Используется в `bartprepare` / `_unit_SearchTarget`. Пехота "
      "**не атакует** врага вне этого круга, даже если он виден через FOW.")
    A("")
    L.extend(render_legend())
    L.extend(render_unit_table(units))
    L.extend(render_building_table(buildings))
    L.extend(render_notes())
    A("---")
    A("")
    A("Перегенерация: `python compute/compute_vision.py`")
    MD_PATH.write_text("\n".join(L), encoding="utf-8")
    print(f"Wrote {MD_PATH} ({MD_PATH.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
