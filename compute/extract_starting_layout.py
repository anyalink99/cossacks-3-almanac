"""Document the starting-point layout: peasant grid, resource ring distances,
and the `startingsettings.cfg` presets (default / armysmall / cannons / village …).

Sources:
- `data/scripts/common.inc/dogenerate.inc`
    - `CreateStartPointPeasants` (l. 1231-1281): 18-peasant 6×3 grid at start point
    - `SetupStartingResources` (l. 720-978): forest/stone pattern spawn rings
    - `cCircle{1,2,3}Mask{X,Y}` (l. 407-414): inner / mid / outer ring radii
- `data/game/var/startingsettings.cfg`: pickable starting-units presets
   (selected via the multiplayer-lobby "starting units" dropdown)

Output: output/reference/reports/starting_layout.md
"""
from __future__ import annotations
import sys
import re
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "parser"))
from config import GAME_ROOT, REPORTS_DIR


DOGEN_PATH = GAME_ROOT / "data" / "scripts" / "common.inc" / "dogenerate.inc"
SETTINGS_PATH = GAME_ROOT / "data" / "game" / "var" / "startingsettings.cfg"
DM_GLOBAL_PATH = GAME_ROOT / "data" / "scripts" / "dmscript.global"
MD_PATH = REPORTS_DIR / "starting_layout.md"

# These map the startid integer to the symbolic enum name from dmscript.global:1032-1045.
PRESET_NAMES = {
    -1: "(шаблон — не выбирается)",
    0:  "default",
    1:  "armysmall",
    2:  "armymedium",
    3:  "armylarge",
    4:  "peasantslot",
    5:  "differentnations",
    6:  "towers",
    7:  "cannons",
    8:  "cannonsandhowitzers",
    9:  "barrack18",
    10: "barrack17",
    11: "village",
    12: "logcabins",
    13: "union",
}


def extract_circle_consts(text: str) -> dict:
    """Inner/mid/outer ring half-axes (tiles) — they bound where forests/stones
    can spawn near a starting point."""
    out = {}
    for m in re.finditer(
        r"const\s+cCircle(\d)Mask([XY])\s*=\s*(\d+)\s*;", text
    ):
        n, axis, val = m.group(1), m.group(2), int(m.group(3))
        out[f"circle{n}_{axis.lower()}"] = val
    return out


def extract_peasant_grid(text: str) -> dict:
    """From `CreateStartPointPeasants`: count, grid shape (cols×rows),
    spacing, jitter."""
    out = {}
    body_m = re.search(
        r"procedure\s+CreateStartPointPeasants.*?procedure\b",
        text, re.DOTALL,
    )
    body = body_m.group(0) if body_m else text
    # count
    m = re.search(r"count\s*:\s*Integer\s*=\s*(\d+)", body)
    if m: out["peasant_count"] = int(m.group(1))
    # cUnitR
    m = re.search(r"const\s+cUnitR\s*=\s*([\d.]+)", body)
    if m: out["spacing_tiles"] = float(m.group(1))
    # i div N — column count
    m = re.search(r"\(i\s+div\s+(\d+)\)", body)
    if m:
        # Loop body uses `i div 3` and `i mod 3`. Cols = count/3, rows = 3.
        rows = int(m.group(1))
        out["rows"] = rows
        if "peasant_count" in out:
            out["cols"] = out["peasant_count"] // rows
    return out


def parse_settings(text: str) -> list[dict]:
    """Parse top-level `[*] : struct.begin … struct.end` blocks of
    `startingsettings.cfg`. Returns one dict per preset with:
        startid, dataversionmin, dataversionmax, addresources (top-level)."""
    out = []
    # Iterate top-level blocks. Top-level is depth-1 inside the outer
    # `startingsettings : section.begin` wrapper. We scan linearly using a
    # lightweight depth tracker on `struct.begin` / `struct.end` tokens.
    lines = text.splitlines()
    depth = 0
    in_top_level = False
    current: dict | None = None
    in_addresources = False
    addresources_depth = -1
    section_seen = False
    for ln_no, ln in enumerate(lines, 1):
        s = ln.strip()
        if s.startswith("//"):
            continue
        # Track section.begin (one-off wrapper)
        if "section.begin" in s:
            section_seen = True
            continue
        if "section.end" in s:
            continue
        if "struct.begin" in s:
            depth += 1
            # depth=1 = top-level preset block; depth=2 = addresources or countries block
            if depth == 1:
                current = {"startid": None, "dataversionmin": None,
                           "dataversionmax": None, "addresources": {}}
                in_top_level = True
                in_addresources = False
            elif depth == 2 and "addresources" in s:
                in_addresources = True
                addresources_depth = depth
            continue
        if "struct.end" in s:
            if in_addresources and depth == addresources_depth:
                in_addresources = False
                addresources_depth = -1
            if depth == 1 and current is not None:
                out.append(current)
                current = None
                in_top_level = False
            depth -= 1
            continue
        if not in_top_level or current is None:
            continue
        # Field assignments
        if depth == 1:
            m = re.match(r"(\w+)\s*=\s*(-?\d+)$", s)
            if m and m.group(1) in ("startid", "dataversionmin", "dataversionmax"):
                current[m.group(1)] = int(m.group(2))
        elif in_addresources and depth == addresources_depth:
            m = re.match(r"(\w+)\s*=\s*(-?\d+)$", s)
            if m and m.group(1) in ("food", "wood", "stone", "gold", "iron", "coal"):
                current["addresources"][m.group(1)] = int(m.group(2))
    return out


def fmt_resources(r: dict) -> str:
    if not r:
        return "—"
    parts = []
    for k, letter in (("food", "F"), ("wood", "W"), ("stone", "S"),
                      ("gold", "G"), ("iron", "I"), ("coal", "C")):
        v = r.get(k) or 0
        if v:
            parts.append(f"{letter}{v}")
    return " ".join(parts) if parts else "—"


def render(circles: dict, grid: dict, presets: list[dict]) -> str:
    L: list[str] = []
    A = L.append
    A("# Cossacks 3 — Starting layout")
    A("")
    A("**Производный** файл (расчётный, не извлечение). Считается из "
      "`data/scripts/common.inc/dogenerate.inc` и "
      "`data/game/var/startingsettings.cfg` скриптом "
      "[`compute/extract_starting_layout.py`](../../../compute/extract_starting_layout.py).")
    A("")
    A("## §1. Расстановка крестьян (режим default)")
    A("")
    A("Источник: [`dogenerate.inc:1231-1281` (`CreateStartPointPeasants`)]"
      "(<C:/Program Files (x86)/Steam/steamapps/common/Cossacks 3/data/scripts/common.inc/dogenerate.inc>).")
    A("")
    count = grid.get("peasant_count")
    cols = grid.get("cols")
    rows = grid.get("rows")
    spacing = grid.get("spacing_tiles")
    A(f"- **{count} крестьян** спавнятся в сетке **{cols}×{rows}** "
      f"(`i div {rows}`, `i mod {rows}`)")
    A(f"- Шаг между крестьянами: `cUnitR = {spacing}` тайла")
    A(f"- Сетка центрирована на старт-точке: суммарно "
      f"`({cols}×{spacing}) × ({rows}×{spacing}) = "
      f"{cols * spacing}×{rows * spacing}` тайла")
    A(f"- Случайное смещение каждого крестьянина: ±0.125 тайла по обеим осям")
    A("- Уникальный sid крестьянина берётся из `gCountry[cid].members[]` "
      "по первому юниту с `usage = gc_obj_usage_peasant` (например `peaaus` "
      "у Австрии, `peaeng` у Англии, и т.п.)")
    A("")
    A("**На практике:** при старте у тебя горка из 18 крестьян занимает примерно "
      "`5×3` тайла, что укладывается во внутренний круг очистки `cCircle1` "
      "(см. §2). Ничего другого там не спавнится — это безопасный «дом» "
      "для первой минуты.")
    A("")
    A("## §2. Кольца спавна ресурсов вокруг старт-точки")
    A("")
    A("Источник: [`dogenerate.inc:407-414, 720-978`]"
      "(<C:/Program Files (x86)/Steam/steamapps/common/Cossacks 3/data/scripts/common.inc/dogenerate.inc>) "
      "(`SetupStartingResources` + `cCircle*Mask` константы).")
    A("")
    A("Вокруг каждой старт-точки игрока — три эллипса (X-радиус × Y-радиус, тайлы):")
    A("")
    A("| Кольцо | X-радиус | Y-радиус | Что спавнится на границе |")
    A("| --- | ---: | ---: | --- |")
    A(f"| Inner (`cCircle1`) | {circles.get('circle1_x', '?')} | "
      f"{circles.get('circle1_y', '?')} | очищается, ресурсы НЕ спавнятся (только крестьяне) |")
    A(f"| Mid (`cCircle2`) | {circles.get('circle2_x', '?')} | "
      f"{circles.get('circle2_y', '?')} | 1× stoneforests + 1× stones (камни) у внутренней границы |")
    A(f"| — _между mid+4 и outer_ | — | — | дополнительные 2× forests + 1× stones (камни) |")
    A(f"| Outer (`cCircle3`) | {circles.get('circle3_x', '?')} | "
      f"{circles.get('circle3_y', '?')} | 1× forest у границы (затем маска заполняется) |")
    A("")
    A("**Алгоритм спавна** (`for [MAIN]i:=0 to 127 do begin … VectorRotateY(px, …, angle); _misc_CheckStandPattern… end`): "
      "в каждом «кольце» — 128 попыток × 3 под-попытки найти валидную позицию "
      "под выбранный паттерн. Угол `angle` — `RandomExt × 360°`. Дистанция от "
      "центра — `mindst + RandomExt × N + (i+j) × 0.5` тайла. Это значит:")
    A("")
    A("- **Inner stoneforest:** дистанция ~5-8 тайл")
    A("- **Inner stones:** дистанция ~5-8 тайл (отдельный random angle, может быть с обратной стороны)")
    A("- **Mid forests** (×2): дистанция ~12-18 тайл (mindst=12, +2 random)")
    A("- **Mid stones:** дистанция ~16-22 тайл (mindst=12+4=16, +2 random)")
    A("- **Outer forest:** дистанция ~22-28 тайл")
    A("")
    A("Тип леса определяется параметром `foreststype` в настройках генерации карты: "
      "0 = pinefir/spruce/pine (хвойные, 7 вариантов), 1 = leaf (лиственные), 2 = mixed (смешанные). "
      "В desert-картах вместо forests используются паттерны `desert_forests_*`.")
    A("")
    A("Шахты (gold/iron/coal) — отдельная функция `SetupMines` "
      "([`dogenerate.inc:985`]"
      "(<C:/Program Files (x86)/Steam/steamapps/common/Cossacks 3/data/scripts/common.inc/dogenerate.inc>)). "
      "Спавн шахт идёт по другой логике (раундами по дистанции, см. "
      "`reference_extraction_model.md` § \"Map gen для tiny\").")
    A("")
    A("## §3. Пресеты стартовых юнитов")
    A("")
    A("Источник: [`startingsettings.cfg`]"
      "(<C:/Program Files (x86)/Steam/steamapps/common/Cossacks 3/data/game/var/startingsettings.cfg>) + "
      "enum `gc_mapsettings_startingunits_*` ([`dmscript.global:1032-1045`]"
      "(<C:/Program Files (x86)/Steam/steamapps/common/Cossacks 3/data/scripts/dmscript.global>)).")
    A("")
    A("Игрок выбирает один из этих режимов в лобби. **default** (id=0) — это то, "
      "что описано в §1 (просто 18 крестьян, никаких добавочных ресурсов или "
      "юнитов). Остальные режимы добавляют ресурсы и/или дополнительные юниты "
      "+ здания (через сложные ASCII-маски в cfg-файле).")
    A("")
    A("**Сводка по startid → пресет → стартовые ресурсы (поверх default):**")
    A("")
    A("| startid | preset | dataversion | +F | +W | +S | +G | +I | +C |")
    A("| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |")
    # Sort by startid then by dataversionmin to put older variants below newer ones
    presets_sorted = sorted(presets, key=lambda p: (
        p["startid"] if p["startid"] is not None else -999,
        -(p.get("dataversionmin") or 0),
    ))
    for p in presets_sorted:
        if p["startid"] is None:
            continue
        name = PRESET_NAMES.get(p["startid"], "?")
        dvmin = p.get("dataversionmin")
        dvmax = p.get("dataversionmax")
        dv = "—"
        if dvmin is not None or dvmax is not None:
            dv = f"{dvmin if dvmin is not None else '*'}…{dvmax if dvmax is not None else '*'}"
        a = p["addresources"]
        cells = [
            str(p["startid"]),
            name,
            dv,
            str(a.get("food") or 0),
            str(a.get("wood") or 0),
            str(a.get("stone") or 0),
            str(a.get("gold") or 0),
            str(a.get("iron") or 0),
            str(a.get("coal") or 0),
        ]
        A("| " + " | ".join(cells) + " |")
    A("")
    A("**Замечания:**")
    A("- Ресурсы — это **прибавка** к default'у (default = 0/0/0/0/0/0). "
      "Игроки начинают ровно с этими числами на счётчиках.")
    A("- `dataversion` указывает диапазон версий движка, в которых эта запись "
      "активна. Старые записи (`dataversion 0…59`) сохранены для совместимости с реплеями. "
      "Для текущей версии используются записи с `dataversionmin ≥ 60`.")
    A("- Помимо ресурсов каждый не-default пресет спавнит **дополнительные "
      "здания и юниты** через ASCII-маски (`mask : struct.begin`), которые "
      "тут не парсятся (слишком вариативно по нациям). Открой "
      "`startingsettings.cfg` целиком, если нужны точные расположения.")
    A("- `legends : struct.begin` под каждым `allowedcountries` — это "
      "словарь символов маски (`X = peasant`, `O = officer17`, `B = drummer17`, "
      "`P = polish unit`, и т.д.). Конкретный sid юнита берётся через "
      "`role` (= gc_ai_unit_*) или явный `basename`.")
    A("")
    A("---")
    A("")
    A("Сгенерировано из игровых файлов. Для перегенерации:")
    A("")
    A("```")
    A("python compute/extract_starting_layout.py")
    A("```")
    return "\n".join(L)


def main():
    dogen_text = DOGEN_PATH.read_text(encoding="utf-8", errors="replace")
    settings_text = SETTINGS_PATH.read_text(encoding="utf-8", errors="replace")

    circles = extract_circle_consts(dogen_text)
    grid = extract_peasant_grid(dogen_text)
    presets = parse_settings(settings_text)

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    md = render(circles, grid, presets)
    MD_PATH.write_text(md, encoding="utf-8")
    print(f"Wrote {MD_PATH} ({MD_PATH.stat().st_size:,} bytes)")
    print(f"  circles: {circles}")
    print(f"  grid:    {grid}")
    print(f"  presets: {len(presets)} found")


if __name__ == "__main__":
    main()
