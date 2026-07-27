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
from config import (DATA_JSON, REPORTS_DIR, PLAYABLE_NATIONS, REPORTS_COMBAT_DIR,
                    USAGE_RU, nation_ru, unit_ru)
from citations import Citations

MD_PATH = REPORTS_COMBAT_DIR / "vision_radii.md"

# Engine constants (unit.script:11570-11571).
VISION_BASE = 20
VISION_MOD = 4


def vision_tiles(vision_field: int) -> int:
    """Return real fog-of-war reveal radius in tiles."""
    return VISION_BASE + VISION_MOD * (vision_field or 0)


def render_legend(cites: Citations) -> list[str]:
    L = []
    A = L.append
    A("## Формула")
    A("")
    cite = cites.cite("lib/unit.script:11565", label="`_unit_GetVision`")
    A(f"Радиус обзора = **20 + 4 × внутренний уровень обзора** {cite}. "
      f"Уровень обычно лежит в диапазоне от 0 до 8.")
    A("")
    A("| Внутренний уровень | Радиус, клеток | Типичный пример |")
    A("| ---: | ---: | --- |")
    rows = [
        (0, "Базовый минимум"),
        (1, "Бо́льшая часть пехоты, артиллерия, башня без апгрейдов"),
        (2, "Лёгкая пехота, конница средней зоркости"),
        (3, "Драгуны, средняя кавалерия, башня с апгрейдом"),
        (4, "Разведчики и украинский крестьянин"),
        (5, "Прусский гусар и пьемонтский драгун XVIII века"),
        (7, "Гетман — лучший обзор среди сухопутной кавалерии"),
        (8, "Барабанщик, волынщик, линейный корабль и фрегат"),
    ]
    for v, who in rows:
        A(f"| {v} | **{vision_tiles(v)}** | {who} |")
    A("")
    return L


def render_unit_table(units: list[dict]) -> list[str]:
    L = []
    A = L.append
    A("## Обзор и автоматическое обнаружение целей у юнитов")
    A("")
    A("Радиус обзора показывает, какая часть карты открывается вокруг юнита. "
      "Радиус автообнаружения показывает, насколько близко должен подойти враг, "
      "чтобы юнит самостоятельно выбрал его целью.")
    A("")
    seen: dict[tuple, list[str]] = defaultdict(list)
    for u in units:
        sid = u.get("sid", "")
        v = u.get("vision") or 0
        sr_tile = u.get("searchradius_tiles") or 0
        sr_px = u.get("searchradius_px") or 0
        usg = u.get("usage_short") or "?"
        name = unit_ru(sid, u.get("name_ru") or USAGE_RU.get(usg, usg))
        key = (name, sid, v, sr_tile, sr_px)
        seen[key].append(u.get("nation"))
    rows = []
    for key, nats in seen.items():
        name, sid, v, sr_tile, sr_px = key
        rows.append((-vision_tiles(v), name, sid, v, sr_tile, sr_px, sorted(set(nats))))
    rows.sort()
    A("| Юнит | Код | Обзор, клеток | Автообнаружение, клеток | Нации |")
    A("| --- | --- | ---: | ---: | --- |")
    for _, name, sid, v, sr_tile, sr_px, nats in rows:
        nat_names = [nation_ru(nat) for nat in nats]
        nat_str = "все 21" if len(nats) == len(PLAYABLE_NATIONS) else (
            ", ".join(nat_names[:6]) + (f" … (+{len(nats)-6})" if len(nats) > 6 else ""))
        A(f"| {name} | `{sid}` | **{vision_tiles(v)}** | "
          f"{sr_tile if sr_tile else '—'} | {nat_str} |")
    A("")
    return L


def render_building_table(buildings: list[dict]) -> list[str]:
    L = []
    A = L.append
    A("## Обзор у зданий")
    A("")
    A("У большинства зданий нет отдельного уровня обзора: их видимая область "
      "задаётся движком. Ниже перечислены исключения с явно заданным значением.")
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
        A("_Здания с отдельным уровнем обзора не найдены._")
        A("")
        return L
    A("| Здание | Код | Радиус обзора, клеток | Нация |")
    A("| --- | --- | ---: | --- |")
    seen = set()
    for usg, sid, v, nat in rows:
        if (sid, v) in seen:
            continue
        seen.add((sid, v))
        A(f"| {usg} | `{sid}` | **{vision_tiles(v)}** | {nation_ru(nat)} |")
    A("")
    return L


def render_notes() -> list[str]:
    L = []
    A = L.append
    A("## Что важно учитывать")
    A("")
    A("- Почти каждый юнит **видит врага раньше**, чем самостоятельно выбирает "
      "его целью. Исключение составляют некоторые мортиры.")
    A("- Даже минимальный внутренний уровень даёт **20 клеток обзора**, а не ноль.")
    A("- **Барабанщик и волынщик** открывают 52 клетки, но не атакуют. Это "
      "отличные чистые разведчики.")
    A("- **Линейный корабль и фрегат** также открывают 52 клетки, что полезно "
      "для морского патрулирования.")
    A("- **Гетман** — самый зоркий сухопутный кавалерист.")
    A("- Улучшений радиуса обзора в игре нет.")
    A("")
    return L


def main() -> None:
    data = json.loads(DATA_JSON.read_text(encoding="utf-8"))
    units = data["units"]
    buildings = data["buildings"]
    MD_PATH.parent.mkdir(parents=True, exist_ok=True)

    cites = Citations()
    L = []
    A = L.append
    A("# Радиус обзора и обнаружения целей")
    A("")
    A("[← Таблицы и расчёты](../README.md)")
    A("")
    A("У каждого юнита есть два разных расстояния:")
    A("")
    A("- **радиус обзора** — насколько далеко вокруг юнита открывается карта;")
    A("- **радиус автоматического обнаружения** — насколько близко должен "
      "подойти видимый враг, чтобы юнит сам начал атаку.")
    A("")
    L.extend(render_legend(cites))
    L.extend(render_unit_table(units))
    L.extend(render_building_table(buildings))
    L.extend(render_notes())
    L.extend(cites.render())
    MD_PATH.write_text("\n".join(L), encoding="utf-8")
    print(f"Wrote {MD_PATH} ({MD_PATH.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
