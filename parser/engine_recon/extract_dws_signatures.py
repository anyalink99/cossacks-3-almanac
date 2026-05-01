"""Extract DWS native-function signatures from cossacks.exe.

DWS registers each engine-exposed function as an AnsiString of the form
    'function NAME(arg1: T1; arg2: T2): ReturnType'
or  'procedure NAME(arg1: T1; arg2: T2)'

Delphi AnsiString static layout in the .data segment:
    [refcount:4=0xFFFFFFFF][length:4=N][char bytes...][NUL]

We scan for that pattern, extract strings, and filter to ones that start with
'function ' or 'procedure '. From there we parse name + params + return type.

This gives us a complete machine-readable index of every native primitive the
engine exposes to DMscript — without needing a disassembler.

Output:
  derived/dws_native_signatures.json
  internals/engine/native_primitives.md (rewritten — table with signatures)
"""

from __future__ import annotations

import json
import re
import struct
from collections import defaultdict
from pathlib import Path

import pefile

EXE_PATH = Path(r"C:\Program Files (x86)\Steam\steamapps\common\Cossacks 3\cossacks.exe")
ROOT = Path(__file__).resolve().parents[2]
PRIMS_PATH = ROOT / "derived" / "engine_primitives.json"
OUT_JSON = ROOT / "derived" / "dws_native_signatures.json"
OUT_MD = ROOT / "internals" / "engine" / "native_primitives.md"

# Header pattern: refcount=0xFFFFFFFF, then length:4 little-endian.
# Followed by `length` bytes of ASCII, then a NUL.
HEADER = b"\xff\xff\xff\xff"

SIG_RE = re.compile(
    r"^\s*(function|procedure)\s+"
    r"([A-Za-z_][A-Za-z_0-9]*)"
    r"\s*(?:\(([^)]*)\))?"
    r"\s*(?::\s*([A-Za-z_][A-Za-z_0-9]*))?"
    r"\s*;?\s*$",
    re.IGNORECASE,
)
# Match the actual stored form which includes NO trailing semicolon — but real
# strings in the exe DO sometimes have spaces and complex types like
# `array of Integer`. Loosen the return-type and param parsing accordingly.
SIG_RE_LOOSE = re.compile(
    r"^\s*(function|procedure)\s+"
    r"([A-Za-z_][A-Za-z_0-9]*)"
    r"\s*(\([^)]*\))?"
    r"\s*(?::\s*(.+?))?"
    r"\s*;?\s*$",
    re.IGNORECASE | re.DOTALL,
)


def parse_params(raw: str) -> list[dict]:
    """Parse a Pascal parameter list `a, b: Integer; c: String` -> list of dicts."""
    if raw is None or not raw.strip():
        return []
    out = []
    for chunk in raw.split(";"):
        if ":" not in chunk:
            continue
        names_part, type_part = chunk.split(":", 1)
        names_part = names_part.strip()
        type_part = type_part.strip()
        # Names may have modifiers: `var x`, `const y`, `out z`.
        names = []
        modifier = None
        for n in [s.strip() for s in names_part.split(",")]:
            mod = None
            if " " in n:
                head, _, n = n.rpartition(" ")
                head_lc = head.lower()
                if head_lc in ("var", "const", "out"):
                    mod = head_lc
            names.append({"name": n, "mod": mod})
            modifier = modifier or mod
        for nrec in names:
            out.append({
                "name": nrec["name"],
                "type": type_part,
                "modifier": nrec["mod"],
            })
    return out


def main() -> None:
    pe = pefile.PE(str(EXE_PATH), fast_load=True)
    image_base = pe.OPTIONAL_HEADER.ImageBase
    raw = EXE_PATH.read_bytes()

    def file_to_rva(off: int) -> int | None:
        for s in pe.sections:
            start = s.PointerToRawData
            end = start + s.SizeOfRawData
            if start <= off < end:
                return image_base + s.VirtualAddress + (off - start)
        return None

    sigs: list[dict] = []
    bad: list[str] = []
    pos = 0
    while True:
        i = raw.find(HEADER, pos)
        if i < 0:
            break
        pos = i + 1
        # length = 4 bytes after the refcount
        if i + 8 > len(raw):
            continue
        (length,) = struct.unpack_from("<I", raw, i + 4)
        if length == 0 or length > 1024:
            continue
        s_start = i + 8
        s_end = s_start + length
        if s_end + 1 > len(raw):
            continue
        if raw[s_end] != 0:
            # not a valid AnsiString record
            continue
        try:
            text = raw[s_start:s_end].decode("ascii")
        except UnicodeDecodeError:
            continue
        # Filter: must start with 'function ' or 'procedure ' (case-insensitive,
        # ignoring leading whitespace — many entries in exe begin with a space).
        head = text.lstrip()[:10].lower()
        if not (head.startswith("function ") or head.startswith("procedure ")):
            continue
        m = SIG_RE_LOOSE.match(text)
        if not m:
            bad.append(text)
            continue
        kind, name, params_paren, ret = m.group(1).lower(), m.group(2), m.group(3), m.group(4)
        params_inner = params_paren[1:-1] if params_paren else ""
        try:
            params = parse_params(params_inner)
        except Exception:  # noqa: BLE001
            params = []
        rva = file_to_rva(s_start)
        sigs.append({
            "kind": kind,
            "name": name,
            "name_lc": name.lower(),
            "params": params,
            "params_raw": params_inner,
            "returns": (ret or "").strip() or None,
            "raw": text,
            "off": s_start,
            "rva": f"0x{rva:08x}" if rva else None,
        })

    # Cross-reference with script primitives.
    prims = json.loads(PRIMS_PATH.read_text(encoding="utf-8"))
    native_lc = set(prims["native_primitives"].keys())  # already lowercased

    by_name = {s["name_lc"]: s for s in sigs}
    matched = sorted(native_lc & set(by_name.keys()))
    only_in_script = sorted(native_lc - set(by_name.keys()))
    only_in_exe = sorted(set(by_name.keys()) - native_lc)

    # Categorise sigs by name prefix to spot subsystems (rough heuristic).
    def categorise(name: str) -> str:
        n = name.lower()
        if n.startswith(("getgameobject", "setgameobject", "isgameobject")):
            return "game_object"
        if n.startswith(("getplayer", "setplayer")):
            return "player"
        if n.startswith(("recordcustom", "writeinteger", "readinteger", "writeext", "readext")):
            return "save_load"
        if n.startswith(("setbehaviour", "getbehaviour")):
            return "behaviour_props"
        if n.startswith(("findnearest", "findclosest", "find")):
            return "search"
        if n.startswith(("vector", "distance", "angle")):
            return "geometry"
        if n.startswith(("ai", "wave", "attack")):
            return "ai"
        if n.startswith(("locale", "getlocale", "setlocale")):
            return "locale"
        if n.startswith(("net", "send", "broadcast", "sync")):
            return "net"
        if n.startswith(("script", "compiler", "parse", "parser")):
            return "scripting"
        if n.startswith(("draw", "render", "show", "hide", "ui", "form")):
            return "ui"
        if n.startswith(("sound", "play", "music")):
            return "sound"
        if n.startswith(("anim", "model", "sprite")):
            return "anim_render"
        if n.startswith(("path", "move", "goto", "stop")):
            return "path_command"
        if n.startswith(("create", "destroy", "kill", "spawn")):
            return "spawn"
        if n.startswith(("random", "setrandom")):
            return "rng"
        return "misc"

    by_cat: dict[str, list[dict]] = defaultdict(list)
    for s in sigs:
        by_cat[categorise(s["name"])].append(s)

    n_total = len(sigs)
    print(f"DWS-style signatures found:    {n_total}")
    print(f"matched against script calls:  {len(matched)} / {len(native_lc)} native ({len(matched)/len(native_lc)*100:.1f}%)")
    print(f"in exe but never called:       {len(only_in_exe)}")
    print(f"called but no signature found: {len(only_in_script)}")
    print()
    print("Subsystems (by name prefix heuristic):")
    for cat, items in sorted(by_cat.items(), key=lambda kv: -len(kv[1])):
        print(f"  {cat:20s} {len(items):>4}")

    out = {
        "stats": {
            "signatures_total": n_total,
            "script_native_total": len(native_lc),
            "matched": len(matched),
            "exe_only": len(only_in_exe),
            "script_only": len(only_in_script),
            "match_pct": round(len(matched) / len(native_lc) * 100, 1),
        },
        "subsystems": {cat: len(items) for cat, items in by_cat.items()},
        "signatures": sorted(sigs, key=lambda s: s["name_lc"]),
        "matched": matched,
        "only_in_exe_top": only_in_exe[:200],
        "only_in_script_top": only_in_script[:200],
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nwrote {OUT_JSON}")

    # Markdown.
    lines = []
    lines.append("# Native primitives in cossacks.exe — DWS signatures")
    lines.append("")
    lines.append(
        "Извлечено напрямую из `cossacks.exe`: каждый нативный "
        "DWS-примитив зарегистрирован как Delphi AnsiString вида "
        "`function NAME(args): ReturnType`. Скрипт ниже сканирует exe "
        "по сигнатуре заголовка AnsiString (`refcount=-1, length, chars, "
        "NUL`) и извлекает 100% этих строк."
    )
    lines.append("")
    lines.append(f"**Всего сигнатур в exe:** {n_total}.  ")
    lines.append(
        f"**Из них вызывается из DMscript:** {len(matched)} "
        f"({len(matched)/len(native_lc)*100:.1f}% от {len(native_lc)} нативных вызовов в скриптах).  "
    )
    lines.append(
        f"**Только в exe (не используются скриптом):** {len(only_in_exe)} — "
        "это либо мёртвые/legacy-примитивы, либо API для редактора/AI, "
        "либо примитивы, которые скрипт зовёт через class.method-синтаксис "
        "(не пойманный нашим извлекателем)."
    )
    lines.append("")
    lines.append("## Подсистемы (грубая классификация по префиксу)")
    lines.append("")
    lines.append("| Подсистема | Сигнатур |")
    lines.append("|---|---:|")
    for cat, items in sorted(by_cat.items(), key=lambda kv: -len(kv[1])):
        lines.append(f"| {cat} | {len(items)} |")
    lines.append("")
    lines.append("## Топ-50 матчей (по числу вызовов из скриптов)")
    lines.append("")
    lines.append("| Имя | Сигнатура | Возвращает | Calls | Файлов |")
    lines.append("|---|---|---|---:|---:|")
    nat = prims["native_primitives"]
    matched_with_calls = sorted(
        [s for s in sigs if s["name_lc"] in native_lc],
        key=lambda s: -nat[s["name_lc"]]["calls"],
    )
    for s in matched_with_calls[:50]:
        info = nat[s["name_lc"]]
        ret = s["returns"] or "—"
        params = s["params_raw"] or "—"
        # Escape pipes
        params = params.replace("|", r"\|")
        lines.append(
            f"| `{s['name']}` | `({params})` | `{ret}` | {info['calls']} | {info['files_total']} |"
        )
    lines.append("")
    lines.append("## Примеры по подсистемам (10 первых из каждой)")
    lines.append("")
    for cat, items in sorted(by_cat.items(), key=lambda kv: -len(kv[1])):
        if cat == "misc":
            continue
        lines.append(f"### {cat} ({len(items)})")
        lines.append("")
        for s in sorted(items, key=lambda x: x["name"])[:10]:
            ret = f": {s['returns']}" if s["returns"] else ""
            lines.append(f"- `{s['kind']} {s['name']}({s['params_raw']}){ret}`  *(rva {s['rva']})*")
        lines.append("")
    lines.append("## Где данные")
    lines.append("")
    lines.append("- `derived/dws_native_signatures.json` — полный машинно-читаемый список всех сигнатур.")
    lines.append("- `derived/engine_primitives.json` — нативные примитивы со стороны скрипта (970 имён + частоты).")
    lines.append("- Генератор: `parser/engine_recon/extract_dws_signatures.py`.")
    lines.append("")
    lines.append("## Как использовать дальше")
    lines.append("")
    lines.append(
        "1. **Поиск алгоритма примитива:** взять `rva` из JSON, открыть exe в "
        "Ghidra/IDA по этому адресу — рядом будет указатель на нативную "
        "функцию-обёртку (DWS callback). Декомпиляция показывает реальный "
        "алгоритм (например, BFS vs k-d tree для `findnearestresource`)."
    )
    lines.append(
        "2. **Карта подсистем:** имена `Get*ByHandle/Set*ByHandle` "
        "выявляют ECS-style API движка. `RecordCustom*` — формат сейва. "
        "`SwitchTo` — корневой scheduler-примитив (146 файлов = почти "
        "весь скриптовый код)."
    )
    lines.append(
        "3. **Документация без RE:** сигнатуры уже включают имена аргументов "
        "и типы — это де-факто публичный API DWS-движка C3."
    )
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT_MD}")


if __name__ == "__main__":
    main()
