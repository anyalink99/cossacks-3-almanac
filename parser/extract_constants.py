"""Extract gc_* constants from dmscript.global.

Stores both raw text and best-effort numeric value (eval'd if possible).
"""
import re
from pathlib import Path

CONST_RE = re.compile(r"^\s*(gc_[A-Za-z0-9_]+)\s*=\s*([^;]+);")


def parse_constants(path: Path) -> dict[str, dict]:
    text = path.read_text(encoding="utf-8", errors="replace")
    result: dict[str, dict] = {}
    # First pass: collect raw
    for line in text.splitlines():
        # strip line comments (// ...)
        # but preserve string contents (no strings here, safe)
        no_comment = re.sub(r"//.*$", "", line)
        m = CONST_RE.match(no_comment)
        if not m:
            continue
        name, expr = m.group(1), m.group(2).strip()
        result[name] = {"raw": expr, "value": None}
    # Second pass: try eval where possible (resolve refs to earlier consts)
    env: dict[str, float | int] = {}
    for name, info in result.items():
        expr = info["raw"]
        # translate Pascal "shl" to Python "<<", "div" → "//", "or" → "|", "and" → "&"
        py_expr = expr
        py_expr = re.sub(r"\bshl\b", "<<", py_expr)
        py_expr = re.sub(r"\bshr\b", ">>", py_expr)
        py_expr = re.sub(r"\bdiv\b", "//", py_expr)
        py_expr = re.sub(r"\bmod\b", "%", py_expr)
        py_expr = re.sub(r"\bor\b", "|", py_expr)
        py_expr = re.sub(r"\band\b", "&", py_expr)
        # strip strings
        if "'" in py_expr or '"' in py_expr:
            continue
        try:
            value = eval(py_expr, {"__builtins__": {}}, env)
            info["value"] = value
            env[name] = value
        except Exception:
            pass
    return result


if __name__ == "__main__":
    from config import DM_GLOBAL
    consts = parse_constants(DM_GLOBAL)
    print(f"Extracted {len(consts)} constants")
    keys = ["gc_time_to_frames", "gc_resource_hitsneeded_food",
            "gc_resource_hitsneeded_wood", "gc_resource_hitsneeded_stone",
            "gc_obj_resource_portion_food", "gc_obj_resource_portion_wood",
            "gc_obj_resource_portion_stone", "gc_obj_foodperunit",
            "gc_settings_gamespeed_0", "gc_settings_gamespeed_1",
            "gc_settings_gamespeed_2", "gc_FieldMaxHP",
            "gc_MaxObjCount", "gc_MaxPlayerCount", "gc_MaxCountryCount",
            "gc_MaxCountryCountRelease"]
    for k in keys:
        if k in consts:
            print(f"  {k} = {consts[k]['raw']!r}  [value={consts[k]['value']}]")
        else:
            print(f"  {k} : NOT FOUND")
