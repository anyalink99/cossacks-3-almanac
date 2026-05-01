"""Extract the vocabulary of identifiers used in DMscript (DWS) source.

Goal: split everything into three buckets so we know what to look for in the
native engine:

  defined  — function/procedure DEFINED in .script files (user/game logic)
  called   — identifier appears as `name(` somewhere
  unknown  — called but never defined → engine-native primitive or DWS builtin

The "unknown" set is the list of native entry points that the engine exposes
to the script VM. Those names are registered via `TdwsUnit.AddFunction(...)` in
Delphi and embedded as ASCII strings in cossacks.exe — so cross-referencing
this set with the exe's string table gives us a `script_name -> exe_offset`
mapping.

Output: derived/engine_primitives.json
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

SCRIPTS_ROOT = Path(r"C:\Program Files (x86)\Steam\steamapps\common\Cossacks 3\data\scripts")
OUT_PATH = Path(__file__).resolve().parents[2] / "derived" / "engine_primitives.json"

# DWS standard library — known-builtin functions from DelphiWebScript.
# Source: github.com/EricGrange/DWScript/wiki + dwsMathFunctions.pas etc.
# Lowercased for matching since DWS is case-insensitive.
DWS_BUILTINS = {
    # Math
    "abs", "sqr", "sqrt", "sin", "cos", "tan", "arctan", "arcsin", "arccos",
    "exp", "ln", "log10", "log2", "logn", "power", "intpower",
    "round", "trunc", "floor", "ceil", "frac", "int",
    "min", "max", "clamp", "sign", "odd",
    "pi", "e", "infinity", "nan",
    "degtorad", "radtodeg", "hypot",
    # String
    "length", "setlength", "low", "high",
    "copy", "delete", "insert", "pos", "trim", "trimleft", "trimright",
    "uppercase", "lowercase", "uppercaseletter", "lowercaseletter",
    "inttostr", "strtoint", "strtointdef", "floattostr", "strtofloat",
    "format", "stringofchar", "chr", "ord",
    "comparestr", "comparetext",
    "stringreplace", "leftstr", "rightstr", "midstr",
    "hextoint", "inttohex",
    # Conversion / IO
    "ord", "chr", "boolean", "integer", "float", "string",
    "writeln", "write", "print", "println", "readln",
    # Arrays / containers
    "swap", "concat", "join", "split",
    "include", "exclude",
    # Random (we KNOW these are engine-side global PRNG hooks per determinism_audit)
    "random", "randomext", "setrandomkey", "randomize",
    "randg", "randomseed",
    # System
    "exit", "halt", "assert", "raise",
    "now", "date", "time", "gettickcount",
    # Type checks / operators that look like calls
    "assigned", "is", "as", "sizeof", "pointerof",
}

# Identifiers matching this regex are Pascal class names used as type casts
# (e.g. `Tobj(handle).hp`, `TSquad(army).count`). They look like function
# calls but are not native primitives — the engine never sees them as calls.
PASCAL_CLASS_CAST_RE = re.compile(r"^t[a-z][a-z0-9]*$", re.IGNORECASE)

# DWS keywords that can look like calls but aren't.
DWS_KEYWORDS = {
    "if", "then", "else", "while", "for", "repeat", "until", "do", "case", "of",
    "begin", "end", "function", "procedure", "var", "const", "type", "array",
    "record", "class", "interface", "implementation", "uses", "unit", "program",
    "exit", "break", "continue", "with", "in", "not", "and", "or", "xor", "div",
    "mod", "shl", "shr", "true", "false", "nil", "to", "downto", "step", "is",
    "as", "out", "inherited", "self", "result", "string", "integer", "float",
    "boolean", "char", "byte", "word", "longint", "double", "real",
    "try", "except", "finally", "raise", "on",
    "set", "object", "constructor", "destructor", "property", "read", "write",
    "default", "external", "forward", "stdcall", "register", "cdecl", "safecall",
    "overload", "override", "virtual", "abstract", "static", "private", "public",
    "protected", "published", "packed", "label", "goto",
}

DEF_RE = re.compile(
    r"\b(?:function|procedure)\s+([A-Za-z_][A-Za-z_0-9]*)\b",
    re.IGNORECASE,
)
# Identifier followed by `(` — but NOT preceded by `.` (those are method calls
# on records/classes, not free-standing primitives).
# We also skip identifiers that are part of `function/procedure NAME(` defs by
# stripping definitions first.
CALL_RE = re.compile(
    r"(?<![A-Za-z_0-9.])([A-Za-z_][A-Za-z_0-9]*)\s*\(",
)
# Strip Pascal comments: { ... }, (* ... *), //...
COMMENT_RE = re.compile(r"\(\*.*?\*\)|\{[^}]*\}|//[^\n]*", re.DOTALL)
# Strip string literals so identifiers inside strings don't pollute.
STRING_RE = re.compile(r"'(?:''|[^'])*'")


def strip_noise(text: str) -> str:
    text = COMMENT_RE.sub(" ", text)
    text = STRING_RE.sub(" ", text)
    return text


def main() -> None:
    if not SCRIPTS_ROOT.exists():
        print(f"scripts root not found: {SCRIPTS_ROOT}", file=sys.stderr)
        sys.exit(1)

    files = sorted(SCRIPTS_ROOT.rglob("*.script")) + sorted(
        SCRIPTS_ROOT.rglob("*.inc")
    ) + sorted(SCRIPTS_ROOT.rglob("dmscript.global"))

    defined: dict[str, list[str]] = {}      # name_lc -> [files]
    called: dict[str, list[str]] = {}       # name_lc -> [files]
    call_count: dict[str, int] = {}

    for f in files:
        try:
            text = f.read_text(encoding="cp1251", errors="replace")
        except Exception as e:  # noqa: BLE001
            print(f"skip {f}: {e}", file=sys.stderr)
            continue
        clean = strip_noise(text)

        for m in DEF_RE.finditer(clean):
            n = m.group(1).lower()
            defined.setdefault(n, [])
            rel = str(f.relative_to(SCRIPTS_ROOT))
            if rel not in defined[n]:
                defined[n].append(rel)

        # Strip the `function NAME` / `procedure NAME` markers themselves so
        # the call regex doesn't pick them up.
        clean_no_def = DEF_RE.sub(" ", clean)
        for m in CALL_RE.finditer(clean_no_def):
            n = m.group(1).lower()
            if n in DWS_KEYWORDS:
                continue
            called.setdefault(n, [])
            rel = str(f.relative_to(SCRIPTS_ROOT))
            if rel not in called[n]:
                called[n].append(rel)
            call_count[n] = call_count.get(n, 0) + 1

    # Native primitives = called - defined - dws_builtins - pascal-class-casts
    native = {}
    type_casts = {}
    for n in called:
        if n in defined or n in DWS_BUILTINS:
            continue
        info = {
            "calls": call_count.get(n, 0),
            "files": called[n][:5],
            "files_total": len(called[n]),
        }
        if PASCAL_CLASS_CAST_RE.match(n):
            type_casts[n] = info
        else:
            native[n] = info
    # DWS builtins seen in script (sanity check)
    dws_seen = {
        n: call_count[n]
        for n in called
        if n in DWS_BUILTINS
    }
    # Defined-but-never-called (dead code / future hooks)
    unused_defs = sorted(set(defined) - set(called))

    out = {
        "stats": {
            "files_scanned": len(files),
            "defined": len(defined),
            "called": len(called),
            "native_candidates": len(native),
            "type_casts": len(type_casts),
            "dws_builtins_seen": len(dws_seen),
            "unused_defs": len(unused_defs),
        },
        "native_primitives": dict(
            sorted(native.items(), key=lambda kv: -kv[1]["calls"])
        ),
        "pascal_type_casts": dict(
            sorted(type_casts.items(), key=lambda kv: -kv[1]["calls"])
        ),
        "dws_builtins_seen": dict(
            sorted(dws_seen.items(), key=lambda kv: -kv[1])
        ),
        "unused_defs_sample": unused_defs[:50],
    }
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"wrote {OUT_PATH}")
    print(f"  defined:           {len(defined)}")
    print(f"  called:            {len(called)}")
    print(f"  native candidates: {len(native)}")
    print(f"  DWS builtins seen: {len(dws_seen)}")
    print()
    print("Top 30 native primitives by call count:")
    for n, info in list(out["native_primitives"].items())[:30]:
        print(f"  {info['calls']:>5}  {n}  ({info['files_total']} files)")


if __name__ == "__main__":
    main()
