"""Parse unit.script `_unit_InitBase` body to extract per-sid stats.

The script has three giant case-blocks inside `_unit_InitBase`:

1. UNITS case: `case objprop.sid of 'pikeman','pikemanpol',... : begin … case nation of … end; end; end;`
2. COMMON BUILDINGS loop: `for i:=0 to 5 do begin case i of … commonsid := …; end; case objprop.sid of commonsid+'mil':begin … end; … end; end;`
3. PER-NATION BUILDINGS loop: `for i:=0 to gc_MaxCountryCount-1 do begin … csid := … ; case objprop.sid of csid+'cen':begin … case i of aus:…; fra:…; end; end; … end; end;`

For each branch we extract:
- base properties via SetObj* helper calls and direct `objbase.X := Y;` / `objprop.X := Y;`
- nested per-nation overrides

Approach: text-based balanced-block walker, then regex inside each branch.
"""
from __future__ import annotations
import re
from pathlib import Path
from collections import defaultdict
from typing import Iterator


# ---------- Reuse helpers from parse_country ----------

from parse_country import extract_proc_body, _is_word_boundary


# ---------- Block splitter ----------

def find_case_end(body: str, of_end: int) -> int:
    """Given position right after `of`, find the matching `end`. Returns position right
    after that `end` keyword. Tracks nested begin/case/record/try."""
    n = len(body)
    depth = 1
    k = of_end
    in_str = False
    while k < n and depth > 0:
        if in_str:
            if body[k] == "'":
                in_str = False
            k += 1
            continue
        if body[k] == "'":
            in_str = True
            k += 1
            continue
        if body[k:k+2] == "//":
            nl = body.find("\n", k)
            k = nl if nl != -1 else n
            continue
        if body[k] == "{":
            cl = body.find("}", k)
            k = cl + 1 if cl != -1 else n
            continue
        matched = False
        for kw, kl in (("begin", 5), ("case", 4), ("record", 6), ("try", 3)):
            if body[k:k+kl] == kw and _is_word_boundary(body, k, kl):
                depth += 1
                k += kl
                matched = True
                break
        if matched:
            continue
        if body[k:k+3] == "end" and _is_word_boundary(body, k, 3):
            depth -= 1
            k += 3
            continue
        k += 1
    return k


def find_top_cases(body: str) -> list[tuple[int, int, int, int]]:
    """Find every `case` statement in `body`, returning (case_kw_start, of_end, end_pos, _unused).

    We don't actually track outer depth meaningfully — the caller picks the right case by
    head text. Cases are returned in order of appearance.
    """
    n = len(body)
    cases: list[tuple[int, int, int, int]] = []
    i = 0
    in_str = False
    while i < n:
        c = body[i]
        if in_str:
            if c == "'":
                in_str = False
            i += 1
            continue
        if c == "'":
            in_str = True
            i += 1
            continue
        if body[i:i+2] == "//":
            nl = body.find("\n", i)
            i = nl if nl != -1 else n
            continue
        if c == "{":
            cl = body.find("}", i)
            i = cl + 1 if cl != -1 else n
            continue
        if body[i:i+4] == "case" and _is_word_boundary(body, i, 4):
            start = i
            # advance to 'of' (first one not inside parens/strings)
            j = i + 4
            paren = 0
            while j < n:
                if body[j] == "'":
                    j += 1
                    while j < n and body[j] != "'":
                        j += 1
                    j += 1
                    continue
                if body[j] == "(":
                    paren += 1
                elif body[j] == ")":
                    paren -= 1
                elif paren == 0 and body[j:j+2] == "of" and _is_word_boundary(body, j, 2):
                    break
                j += 1
            of_end = j + 2
            end_pos = find_case_end(body, of_end)
            cases.append((start, of_end, end_pos, 0))
            i = of_end  # continue scanning so we discover nested cases too
            continue
        i += 1
    return cases


# ---------- Branch splitter ----------

LABEL_LINE_RE = re.compile(r"\n\s+(.+?)\s*:\s*(?=begin|[A-Za-z_]|$)")  # rough; we'll do it manually


def split_case_branches(case_text: str) -> list[tuple[str, str]]:
    """Given the text BETWEEN 'of' and 'end' of a case statement, split into branches.
    Each branch is `<label-list>: <body>;`. Body may be a single statement or a begin..end block.
    Returns list of (label_str, body_str). Else-branch, if any, gets label 'else'.
    """
    branches: list[tuple[str, str]] = []
    n = len(case_text)
    i = 0
    inside_string = False
    while i < n:
        # skip whitespace, comments, semicolons
        while i < n:
            c = case_text[i]
            if c in " \t\r\n;":
                i += 1
                continue
            if case_text[i:i+2] == "//":
                nl = case_text.find("\n", i)
                i = nl if nl != -1 else n
                continue
            if c == "{":
                cl = case_text.find("}", i)
                i = cl + 1 if cl != -1 else n
                continue
            break
        if i >= n:
            break
        # else-branch?
        if case_text[i:i+4] == "else" and _is_word_boundary(case_text, i, 4):
            i += 4
            # collect until end of case (but we're already inside it, so consume rest as one body)
            body_start = i
            # consume one statement (begin..end or until ';')
            body, new_i = consume_statement(case_text, i)
            branches.append(("else", body))
            i = new_i
            continue
        # label list: read until ':' (NOT inside parens or strings)
        label_start = i
        paren = 0
        in_str = False
        while i < n:
            c = case_text[i]
            if in_str:
                if c == "'":
                    in_str = False
                i += 1
                continue
            if c == "'":
                in_str = True
                i += 1
                continue
            if c == "(":
                paren += 1
            elif c == ")":
                paren -= 1
            elif c == ":" and paren == 0:
                break
            i += 1
        label = case_text[label_start:i].strip()
        if i >= n:
            break
        i += 1  # consume ':'
        # skip whitespace
        while i < n and case_text[i] in " \t\r\n":
            i += 1
        body, new_i = consume_statement(case_text, i)
        branches.append((label, body))
        i = new_i
    return branches


def consume_statement(text: str, i: int) -> tuple[str, int]:
    """Consume one statement starting at i. Returns (body_text, end_index).
    A statement is either `begin … end[;]` (balanced) or text up to next `;` at top level.
    """
    n = len(text)
    # skip leading ws
    while i < n and text[i] in " \t\r\n":
        i += 1
    start = i
    if text[i:i+5] == "begin" and _is_word_boundary(text, i, 5):
        depth = 1
        i += 5
        in_str = False
        while i < n and depth > 0:
            if in_str:
                if text[i] == "'":
                    in_str = False
                i += 1
                continue
            if text[i] == "'":
                in_str = True
                i += 1
                continue
            if text[i:i+2] == "//":
                nl = text.find("\n", i)
                i = nl if nl != -1 else n
                continue
            if text[i] == "{":
                cl = text.find("}", i)
                i = cl + 1 if cl != -1 else n
                continue
            matched = False
            for kw, kl in (("begin", 5), ("case", 4), ("record", 6), ("try", 3)):
                if text[i:i+kl] == kw and _is_word_boundary(text, i, kl):
                    depth += 1
                    i += kl
                    matched = True
                    break
            if matched:
                continue
            if text[i:i+3] == "end" and _is_word_boundary(text, i, 3):
                depth -= 1
                i += 3
                continue
            i += 1
        # consume optional trailing ';'
        while i < n and text[i] in " \t\r\n":
            i += 1
        if i < n and text[i] == ";":
            i += 1
        return text[start:i], i
    # otherwise consume until ';' at depth 0
    paren = 0
    in_str = False
    while i < n:
        if in_str:
            if text[i] == "'":
                in_str = False
            i += 1
            continue
        if text[i] == "'":
            in_str = True
            i += 1
            continue
        if text[i:i+2] == "//":
            nl = text.find("\n", i)
            i = nl if nl != -1 else n
            continue
        if text[i] == "(":
            paren += 1
        elif text[i] == ")":
            paren -= 1
        elif text[i] == ";" and paren == 0:
            i += 1
            return text[start:i], i
        i += 1
    return text[start:i], i


# ---------- SetObj* call extraction ----------

CALL_RE = re.compile(
    r"\b(SetObjBuildingExtProperties|SetObjBuildingProperties|SetObjBasePrice"
    r"|SetObjBaseSearchBuildVisionScore|SetObjBaseWeapon|SetObjBaseProtection"
    r"|SetObjBaseMaterialCanKill|SetObjBuildingBaseSettings)\s*\(",
)

ASSIGN_RE = re.compile(
    r"\b(objbase\.[A-Za-z_][A-Za-z_0-9.\[\]]*|objprop\.[A-Za-z_][A-Za-z_0-9.\[\]]*)\s*:=\s*([^;]+);"
)


def parse_args(text: str, start: int) -> tuple[list[str], int]:
    """Starting at the position of '(', parse comma-separated args, return (args, end_after_)).
    Handles nested parens, strings, brace comments.
    """
    assert text[start] == "("
    i = start + 1
    n = len(text)
    args: list[str] = []
    cur: list[str] = []
    paren = 0
    in_str = False
    while i < n:
        c = text[i]
        if in_str:
            if c == "'":
                in_str = False
            cur.append(c)
            i += 1
            continue
        if c == "'":
            in_str = True
            cur.append(c)
            i += 1
            continue
        if text[i:i+2] == "//":
            nl = text.find("\n", i)
            i = nl if nl != -1 else n
            continue
        if c == "{":
            cl = text.find("}", i)
            i = cl + 1 if cl != -1 else n
            continue
        if c == "(":
            paren += 1
            cur.append(c)
        elif c == ")":
            if paren == 0:
                args.append("".join(cur).strip())
                return args, i + 1
            paren -= 1
            cur.append(c)
        elif c == "," and paren == 0:
            args.append("".join(cur).strip())
            cur = []
        else:
            cur.append(c)
        i += 1
    return args, i


def extract_calls(body: str) -> list[tuple[str, list[str]]]:
    """Find SetObj* calls in body."""
    calls: list[tuple[str, list[str]]] = []
    for m in CALL_RE.finditer(body):
        name = m.group(1)
        # arg-paren is at m.end()-1 (the '(')
        paren_pos = m.end() - 1
        args, _ = parse_args(body, paren_pos)
        calls.append((name, args))
    return calls


def extract_assignments(body: str) -> list[tuple[str, str]]:
    """Find direct objbase.X / objprop.X assignments (skipping nested cases)."""
    return [(m.group(1).strip(), m.group(2).strip()) for m in ASSIGN_RE.finditer(body)]


# ---------- Property aggregation ----------

DEFAULT = -1  # sentinel (matches Pascal `default = -1`)


def parse_int(s: str) -> int | None:
    s = s.strip()
    if s == "" or s.lower() == "default":
        return None
    if s.lower() == "true":
        return 1
    if s.lower() == "false":
        return 0
    # Strip {...} comments
    s = re.sub(r"\{[^}]*\}", "", s).strip()
    # try plain int
    try:
        return int(s)
    except ValueError:
        pass
    # gc_obj_weapon_kind_<X>
    m = re.match(r"gc_obj_weapon_kind_(\w+)", s)
    if m:
        return None  # encoded as string elsewhere
    # arithmetic
    try:
        return int(eval(s, {"__builtins__": {}}, {}))
    except Exception:
        return None


def parse_value(s: str):
    """Parse arbitrary value: int, float, string, identifier, or None for unknown."""
    s = re.sub(r"\{[^}]*\}", "", s).strip()  # strip {…} comments
    if s == "" or s.lower() == "default":
        return None
    if s.lower() == "true":
        return True
    if s.lower() == "false":
        return False
    if s.startswith("'") and s.endswith("'"):
        return s[1:-1]
    if s.startswith("gc_"):
        return s
    try:
        return int(s)
    except ValueError:
        pass
    try:
        return float(s)
    except ValueError:
        pass
    # Try Pascal arithmetic: div, mod, +, -, *, /, parens
    py = re.sub(r"\bdiv\b", "//", s)
    py = re.sub(r"\bmod\b", "%", py)
    try:
        return eval(py, {"__builtins__": {}}, {})
    except Exception:
        return s


def parse_bool(s: str) -> bool | None:
    s = s.strip().lower()
    if s == "true":
        return True
    if s == "false":
        return False
    return None


def apply_setobj_call(stats: dict, name: str, args: list[str]):
    """Update stats dict in place with a SetObj* call's effect."""
    def gi(idx: int):
        if idx >= len(args):
            return None
        return parse_int(args[idx])

    def gs(idx: int):
        if idx >= len(args):
            return None
        return parse_value(args[idx])

    if name == "SetObjBuildingProperties":
        # (objprop, objbase, maxhp, buildtime, costpercent)
        v = gi(2)
        if v is not None: stats["maxhp"] = v
        v = gi(3)
        if v is not None: stats["buildtime"] = v
        v = gs(4)
        if v is not None: stats["costpercent"] = v
    elif name == "SetObjBuildingExtProperties":
        # (objprop, objbase, maxhp, buildtime, costpercent, bcapture, score, usage,
        #  food, wood, stone, gold, iron, coal)
        v = gi(2)
        if v is not None: stats["maxhp"] = v
        v = gi(3)
        if v is not None: stats["buildtime"] = v
        v = gs(4)
        if v is not None: stats["costpercent"] = v
        v = parse_bool(args[5]) if len(args) > 5 else None
        if v is not None: stats["bcapture"] = v
        v = gi(6)
        if v is not None: stats["score"] = v
        v = gs(7)
        if v is not None: stats["usage"] = v
        for k, idx in (("food", 8), ("wood", 9), ("stone", 10), ("gold", 11), ("iron", 12), ("coal", 13)):
            v = gi(idx)
            if v is not None: stats[k] = v
    elif name == "SetObjBuildingBaseSettings":
        # (objprop, bcapture, score, usage)
        v = parse_bool(args[1]) if len(args) > 1 else None
        if v is not None: stats["bcapture"] = v
        v = gi(2)
        if v is not None: stats["score"] = v
        v = gs(3)
        if v is not None: stats["usage"] = v
    elif name == "SetObjBasePrice":
        # (objbase, food, wood, stone, gold, iron, coal)
        for k, idx in (("food", 1), ("wood", 2), ("stone", 3), ("gold", 4), ("iron", 5), ("coal", 6)):
            v = gi(idx)
            if v is not None: stats[k] = v
    elif name == "SetObjBaseProtection":
        # (objbase, pike, sword, bullet, cannister, arrow, cannonball)
        for k, idx in (("prot_pike", 1), ("prot_sword", 2), ("prot_bullet", 3),
                       ("prot_cannister", 4), ("prot_arrow", 5), ("prot_cannonball", 6)):
            v = gi(idx)
            if v is not None: stats[k] = v
    elif name == "SetObjBaseSearchBuildVisionScore":
        # (objprop, objbase, searchradius, buildtime, vision, score)
        v = gi(2)
        if v is not None: stats["searchradius"] = v
        v = gi(3)
        if v is not None: stats["buildtime"] = v
        v = gi(4)
        if v is not None: stats["vision"] = v
        v = gi(5)
        if v is not None: stats["score"] = v
    elif name == "SetObjBaseWeapon":
        # (objprop, objbase, index, damage, pause, radiusmin, radiusmax,
        #  detectradiusmin, detectradiusmax, kind, bSearchMinAttackRadius)
        idx = gi(2)
        if idx is None:
            return
        weapons = stats.setdefault("weapons", {})
        w = weapons.setdefault(idx, {})
        v = gi(3)
        if v is not None: w["damage"] = v
        v = gi(4)
        if v is not None: w["pause"] = v
        v = gi(5)
        if v is not None: w["radiusmin"] = v
        v = gi(6)
        if v is not None: w["radiusmax"] = v
        v = gi(7)
        if v is not None: w["detectradiusmin"] = v
        v = gi(8)
        if v is not None: w["detectradiusmax"] = v
        v = gs(9)
        if v is not None:
            # 'gc_obj_weapon_kind_pike' → 'pike'
            if isinstance(v, str) and v.startswith("gc_obj_weapon_kind_"):
                w["kind"] = v[len("gc_obj_weapon_kind_"):]
            else:
                w["kind"] = v


def apply_assignment(stats: dict, lhs: str, rhs: str):
    """Apply objbase.X / objprop.X := Y; assignment to stats."""
    val = parse_value(rhs)
    # Map LHS to a stat key
    if lhs.startswith("objbase.maxhp"):
        if val is not None: stats["maxhp"] = val
    elif lhs.startswith("objbase.buildtime"):
        if val is not None: stats["buildtime"] = val
    elif lhs == "objprop.farm":
        if val is not None: stats["farm"] = val
    elif lhs == "objprop.usage":
        if val is not None: stats["usage"] = val
    elif lhs.startswith("objprop.consume[gc_resource_type_"):
        m = re.match(r"objprop\.consume\[gc_resource_type_(\w+)\]", lhs)
        if m and val is not None:
            stats.setdefault("consume", {})[m.group(1)] = val
    elif lhs.startswith("objprop.produce[gc_resource_type_"):
        m = re.match(r"objprop\.produce\[gc_resource_type_(\w+)\]", lhs)
        if m and val is not None:
            stats.setdefault("produce", {})[m.group(1)] = val
    elif lhs.startswith("objprop.weapon[") and ".cost[gc_resource_type_" in lhs:
        m = re.match(r"objprop\.weapon\[(\d+)\]\.cost\[gc_resource_type_(\w+)\]", lhs)
        if m and val is not None:
            wi, res = int(m.group(1)), m.group(2)
            stats.setdefault("weapons", {}).setdefault(wi, {}).setdefault("cost", {})[res] = val
    elif lhs.startswith("objprop.peasantabsorber"):
        if val is not None: stats["peasantabsorber"] = val
    elif lhs.startswith("objprop.transport"):
        if val is not None: stats["transport"] = val
    elif lhs.startswith("objbase.fishingspeed"):
        if val is not None: stats["fishingspeed"] = val
    elif lhs.startswith("objbase.fishingmax"):
        if val is not None: stats["fishingmax"] = val
    elif lhs.startswith("objbase.shield"):
        if val is not None: stats["shield"] = val
    elif lhs.startswith("objbase.speed"):
        if val is not None: stats["speed"] = val
    elif lhs.startswith("objprop.vision"):
        if val is not None: stats["vision"] = val
    elif lhs.startswith("objprop.aiforce"):
        if val is not None: stats["aiforce"] = val
    elif lhs.startswith("objprop.walkintervalfactor"):
        if val is not None: stats["walkintervalfactor"] = val
    elif lhs.startswith("objprop.score"):
        if val is not None: stats["score"] = val
    elif lhs == "objprop.bcapture":
        if val is not None: stats["bcapture"] = val
    elif lhs.startswith("objprop.resourcebase[gc_resource_type_"):
        m = re.match(r"objprop\.resourcebase\[gc_resource_type_(\w+)\]", lhs)
        if m and val:
            stats.setdefault("resourcebase", set()).add(m.group(1))
    elif lhs.startswith("objbase.weapon[") and ".dispertion" in lhs:
        m = re.match(r"objbase\.weapon\[(\d+)\]\.dispertion", lhs)
        if m and val is not None:
            stats.setdefault("weapons", {}).setdefault(int(m.group(1)), {})["dispertion"] = val
    elif lhs.startswith("objprop.weapon[") and ".weaponsid" in lhs:
        m = re.match(r"objprop\.weapon\[(\d+)\]\.weaponsid", lhs)
        if m and val is not None:
            stats.setdefault("weapons", {}).setdefault(int(m.group(1)), {})["weaponsid"] = val


_INT_VAR_DECL_RE = re.compile(
    r"\bvar\s+(\w+)\s*:\s*Integer\s*=\s*(-?\d+)\s*;"
)


def inline_int_var_decls(body: str) -> str:
    """Substitute trivial `var <name> : Integer = <int>;` declarations with their value
    throughout the body. The script's musketeer-line uses `var weapInd : Integer = 1;`
    to parameterize weapon-index args; without this inlining, SetObjBaseWeapon args like
    `weapInd` parse to None and weapon data is dropped. Last declaration wins per name —
    good enough since these helpers are scoped within a single branch."""
    decls = _INT_VAR_DECL_RE.findall(body)
    if not decls:
        return body
    bindings = {name: value for name, value in decls}
    result = body
    for name, val in bindings.items():
        result = re.sub(rf"\b{re.escape(name)}\b", val, result)
    return result


def parse_branch_body(body: str, base_stats: dict | None = None,
                      *, exclude_if_blocks: bool = True, debug_label: str = "") -> dict:
    """Parse a branch body (between ':' and end of branch) into a stats dict.

    If `base_stats` is given, start from that (deep copy — apply_* mutates nested dicts).
    If `exclude_if_blocks` is True (default), skip top-level `if (...) then ...`/
    `if (...) then begin ... end` blocks — those are conditional overrides and should
    be processed separately by the caller.
    """
    import os
    import copy
    stats = copy.deepcopy(base_stats) if base_stats else {}
    body_inner = body
    body_inner = re.sub(r"^\s*begin\b", "", body_inner)
    body_inner = re.sub(r"\bend\s*;?\s*$", "", body_inner)
    body_inner = inline_int_var_decls(body_inner)
    cleaned = remove_nested_cases(body_inner)
    if exclude_if_blocks:
        cleaned = remove_top_level_ifs(cleaned)
    if debug_label and os.environ.get("DEBUG_PARSE"):
        print(f"--- DEBUG {debug_label} cleaned ---", flush=True)
        print(cleaned[-1500:], flush=True)
        print(f"--- END {debug_label} ---", flush=True)
    for name, args in extract_calls(cleaned):
        apply_setobj_call(stats, name, args)
    for lhs, rhs in extract_assignments(cleaned):
        apply_assignment(stats, lhs, rhs)
    return stats


def remove_top_level_ifs(body: str) -> str:
    """Remove `if (...) then ...` and `if (...) then begin ... end[;]` blocks at top
    level (i.e., not inside another begin..end). Returns body without them.

    Strips the outer begin/end first so block_depth=0 means "directly inside the branch".
    """
    body = re.sub(r"^\s*begin\b", "", body)
    body = re.sub(r"\bend\s*;?\s*$", "", body)
    out: list[str] = []
    n = len(body)
    i = 0
    in_str = False
    block_depth = 0
    while i < n:
        c = body[i]
        if in_str:
            if c == "'":
                in_str = False
            out.append(c)
            i += 1
            continue
        if c == "'":
            in_str = True
            out.append(c)
            i += 1
            continue
        if body[i:i+2] == "//":
            nl = body.find("\n", i)
            seg = body[i:nl if nl != -1 else n]
            out.append(seg)
            i = nl if nl != -1 else n
            continue
        if c == "{":
            cl = body.find("}", i)
            out.append(body[i:cl + 1 if cl != -1 else n])
            i = cl + 1 if cl != -1 else n
            continue
        # detect 'if' at depth 0
        if body[i:i+2] == "if" and _is_word_boundary(body, i, 2) and block_depth == 0:
            # skip parens of condition
            j = i + 2
            # skip whitespace
            while j < n and body[j] in " \t\r\n":
                j += 1
            if j < n and body[j] == "(":
                paren = 1
                j += 1
                while j < n and paren > 0:
                    if body[j] == "(":
                        paren += 1
                    elif body[j] == ")":
                        paren -= 1
                    j += 1
            # skip 'then'
            while j < n and body[j] in " \t\r\n":
                j += 1
            if body[j:j+4] == "then" and _is_word_boundary(body, j, 4):
                j += 4
            # consume body of if
            body_if, new_j = consume_statement(body, j)
            # check if followed by 'else'
            k = new_j
            while k < n and body[k] in " \t\r\n":
                k += 1
            if body[k:k+4] == "else" and _is_word_boundary(body, k, 4):
                k += 4
                _, new_j = consume_statement(body, k)
            i = new_j
            out.append(" /*top-level-if*/ ")
            continue
        # track block depth
        opened = False
        for kw, kl in (("begin", 5), ("record", 6), ("try", 3)):
            if body[i:i+kl] == kw and _is_word_boundary(body, i, kl):
                block_depth += 1
                out.append(kw)
                i += kl
                opened = True
                break
        if opened:
            continue
        if body[i:i+3] == "end" and _is_word_boundary(body, i, 3):
            block_depth = max(0, block_depth - 1)
            out.append("end")
            i += 3
            continue
        out.append(c)
        i += 1
    return "".join(out)


def parse_top_level_ifs(body: str) -> list[tuple[str, str]]:
    """Find top-level `if (cond) then <stmt>` blocks and return [(cond, body_text)].
    Used for capturing nation-cluster overrides like `if (commontur) then begin … end;`.
    """
    out: list[tuple[str, str]] = []
    n = len(body)
    i = 0
    in_str = False
    block_depth = 0
    body_inner = re.sub(r"^\s*begin\b", "", body)
    body_inner = re.sub(r"\bend\s*;?\s*$", "", body_inner)
    body = body_inner
    n = len(body)
    while i < n:
        c = body[i]
        if in_str:
            if c == "'":
                in_str = False
            i += 1
            continue
        if c == "'":
            in_str = True
            i += 1
            continue
        if body[i:i+2] == "//":
            nl = body.find("\n", i)
            i = nl if nl != -1 else n
            continue
        if c == "{":
            cl = body.find("}", i)
            i = cl + 1 if cl != -1 else n
            continue
        if body[i:i+2] == "if" and _is_word_boundary(body, i, 2) and block_depth == 0:
            j = i + 2
            while j < n and body[j] in " \t\r\n":
                j += 1
            if j < n and body[j] != "(":
                i += 2
                continue
            cond_start = j + 1
            paren = 1
            j += 1
            while j < n and paren > 0:
                if body[j] == "(":
                    paren += 1
                elif body[j] == ")":
                    paren -= 1
                    if paren == 0:
                        break
                j += 1
            cond = body[cond_start:j].strip()
            j += 1  # consume )
            while j < n and body[j] in " \t\r\n":
                j += 1
            if body[j:j+4] == "then" and _is_word_boundary(body, j, 4):
                j += 4
            body_text, new_j = consume_statement(body, j)
            out.append((cond, body_text))
            i = new_j
            continue
        opened = False
        for kw, kl in (("begin", 5), ("record", 6), ("try", 3)):
            if body[i:i+kl] == kw and _is_word_boundary(body, i, kl):
                block_depth += 1
                i += kl
                opened = True
                break
        if opened:
            continue
        if body[i:i+3] == "end" and _is_word_boundary(body, i, 3):
            block_depth = max(0, block_depth - 1)
            i += 3
            continue
        i += 1
    return out


def remove_nested_cases(body: str) -> str:
    """Replace each top-level case…end block with a placeholder, so SetObj*/assignments
    inside cases don't get applied to the base."""
    # Walk and replace
    out = []
    n = len(body)
    i = 0
    in_str = False
    block_depth = 0
    case_starts: list[int] = []
    while i < n:
        c = body[i]
        if in_str:
            if c == "'":
                in_str = False
            out.append(c)
            i += 1
            continue
        if c == "'":
            in_str = True
            out.append(c)
            i += 1
            continue
        if body[i:i+2] == "//":
            nl = body.find("\n", i)
            seg = body[i:nl if nl != -1 else n]
            out.append(seg)
            i = nl if nl != -1 else n
            continue
        if body[i] == "{":
            cl = body.find("}", i)
            seg = body[i:cl + 1 if cl != -1 else n]
            out.append(seg)
            i = cl + 1 if cl != -1 else n
            continue
        # Detect 'case' at depth 0 — replace from 'case' through matching 'end'
        if body[i:i+4] == "case" and _is_word_boundary(body, i, 4) and block_depth == 0:
            # find matching end
            depth = 1
            j = i + 4
            in_str2 = False
            while j < n and depth > 0:
                if in_str2:
                    if body[j] == "'":
                        in_str2 = False
                    j += 1
                    continue
                if body[j] == "'":
                    in_str2 = True
                    j += 1
                    continue
                if body[j:j+2] == "//":
                    nl = body.find("\n", j)
                    j = nl if nl != -1 else n
                    continue
                if body[j] == "{":
                    cl = body.find("}", j)
                    j = cl + 1 if cl != -1 else n
                    continue
                opened = False
                for kw, kl in (("begin", 5), ("case", 4), ("record", 6), ("try", 3)):
                    if body[j:j+kl] == kw and _is_word_boundary(body, j, kl):
                        depth += 1
                        j += kl
                        opened = True
                        break
                if opened:
                    continue
                if body[j:j+3] == "end" and _is_word_boundary(body, j, 3):
                    depth -= 1
                    j += 3
                    continue
                j += 1
            out.append(" /*nested-case*/ ")
            i = j
            continue
        # Track begin/end depth for non-case blocks
        opened = False
        for kw, kl in (("begin", 5), ("record", 6), ("try", 3)):
            if body[i:i+kl] == kw and _is_word_boundary(body, i, kl):
                block_depth += 1
                out.append(kw)
                i += kl
                opened = True
                break
        if opened:
            continue
        if body[i:i+3] == "end" and _is_word_boundary(body, i, 3):
            block_depth = max(0, block_depth - 1)
            out.append("end")
            i += 3
            continue
        out.append(body[i])
        i += 1
    return "".join(out)


# ---------- Top-level driver ----------

def parse_unit_init_base(text: str) -> dict:
    """Parse `_unit_InitBase` and return:
    {
        'units':  { sid: {'base': stats, 'overrides': { nation: stats }} },
        'common_buildings': { suffix: {'base': stats, 'overrides_cluster': {cluster: stats}} },
        'nation_buildings': { suffix: {'base': stats, 'overrides_nation': {nation: stats}} },
    }
    """
    body = extract_proc_body(text, "_unit_InitBase")
    cases = find_top_cases(body)

    def _strip_leading_garbage(s: str) -> str:
        s = s.lstrip()
        while s.startswith("//") or s.startswith("{"):
            if s.startswith("//"):
                nl = s.find("\n")
                s = s[nl + 1:].lstrip() if nl != -1 else ""
            else:
                cl = s.find("}")
                s = s[cl + 1:].lstrip() if cl != -1 else ""
        return s

    units_case = None
    common_case = None
    nation_case = None
    units_case_size = -1
    for (cstart, of_end, end_pos, _depth) in cases:
        head = body[cstart:of_end]
        if "objprop.sid" not in head:
            continue
        inner = body[of_end:end_pos - 3]
        stripped = _strip_leading_garbage(inner)
        if not stripped:
            continue
        if stripped.startswith("commonsid"):
            if common_case is None:
                common_case = (of_end, end_pos - 3)
        elif stripped.startswith("csid"):
            if nation_case is None:
                nation_case = (of_end, end_pos - 3)
        elif stripped.startswith("'"):
            sz = end_pos - cstart
            if sz > units_case_size:
                units_case = (of_end, end_pos - 3)
                units_case_size = sz
    result: dict = {"units": {}, "common_buildings": {}, "nation_buildings": {}}
    if units_case:
        units_text = body[units_case[0]:units_case[1]]
        for label, body_text in split_case_branches(units_text):
            if label == "else":
                continue
            sids = parse_label_sids(label)
            if not sids:
                continue
            # Var-decls (e.g., `var weapInd : Integer = 1;`) live at outer-branch
            # scope. Inline here so nested per-sid override calls also see them.
            body_text_inlined = inline_int_var_decls(body_text)
            base = parse_branch_body(body_text_inlined)
            overrides = parse_nation_overrides(body_text_inlined)
            sid_overrides = parse_sid_overrides(body_text_inlined)
            for sid in sids:
                # Per-sid override stacks on top of the shared base; per-nation
                # override (if any) is still applied later at row-build time.
                if sid in sid_overrides:
                    sid_base = _merge_unit_stats(base, sid_overrides[sid])
                else:
                    sid_base = base
                result["units"][sid] = {"base": sid_base, "overrides": overrides}
    if common_case:
        cb_text = body[common_case[0]:common_case[1]]
        for label, body_text in split_case_branches(cb_text):
            if label == "else":
                continue
            suffixes = parse_label_commonsid_suffixes(label)
            if not suffixes:
                continue
            base = parse_branch_body(body_text)  # excludes if-blocks
            # Cluster overrides: `if (commonrus) then begin ... end;`, `if (commontur) ... end;`
            cluster_overrides: dict[str, dict] = {}
            for cond, if_body in parse_top_level_ifs(body_text):
                cluster = _commoncond_to_cluster(cond)
                if cluster:
                    cluster_overrides[cluster] = parse_branch_body(if_body, base, exclude_if_blocks=False)
            sub_overrides = parse_commonsid_subcase(body_text)
            for suf in suffixes:
                merged_base = dict(base)
                if suf in sub_overrides:
                    merged_base.update(sub_overrides[suf])
                result["common_buildings"][suf] = {
                    "base": merged_base,
                    "overrides_cluster": cluster_overrides,
                }
    if nation_case:
        nb_text = body[nation_case[0]:nation_case[1]]
        for label, body_text in split_case_branches(nb_text):
            if label == "else":
                continue
            suffixes = parse_label_csid_suffixes(label)
            if not suffixes:
                continue
            base = parse_branch_body(body_text)
            overrides = parse_nation_overrides_by_id(body_text)
            for suf in suffixes:
                result["nation_buildings"][suf] = {"base": base, "overrides_nation": overrides}
    return result


SID_LITERAL_RE = re.compile(r"'([^']+)'")


def parse_label_sids(label: str) -> list[str]:
    """Parse 'sid1', 'sid2', 'sid3' label list → list of sids."""
    return SID_LITERAL_RE.findall(label)


COMMONSID_RE = re.compile(r"commonsid\s*\+\s*'([^']+)'")


def parse_label_commonsid_suffixes(label: str) -> list[str]:
    return COMMONSID_RE.findall(label)


CSID_RE = re.compile(r"csid\s*\+\s*'([^']+)'")


def parse_label_csid_suffixes(label: str) -> list[str]:
    return CSID_RE.findall(label)


def _commoncond_to_cluster(cond: str) -> str | None:
    """Map a Pascal boolean expression like `commontur` or `(commontur) or (alg)` to a cluster.
    Returns one of 'eur','rus','tur','spa','ukr','por' or None if not parseable.
    """
    cs = cond.lower()
    # Direct cluster references
    for marker, cluster in (("commoneur", "eur"), ("commonrus", "rus"),
                            ("commontur", "tur"), ("commonspa", "spa"),
                            ("commonukr", "ukr"), ("commonpor", "por")):
        if marker in cs:
            return cluster
    # Sometimes: `if (ukr)` directly inside building branch (Ukraine-only override)
    for marker, cluster in (("ukr", "ukr"), ("rus", "rus"), ("tur", "tur"),
                            ("alg", "tur"), ("spa", "spa"), ("por", "por")):
        if re.search(rf"\b{marker}\b", cs):
            return cluster
    return None


def _merge_unit_stats(base: dict, override: dict) -> dict:
    """Deep-merge override into base (mirrors build_data._merge_stats but used during
    parse to produce per-sid effective bases). For nested dicts (weapons, cost, consume,
    produce) per-key merge; otherwise override wins."""
    import copy
    out = copy.deepcopy(base) if base else {}
    if not override:
        return out
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            for k2, v2 in v.items():
                if isinstance(v2, dict) and isinstance(out[k].get(k2), dict):
                    merged = dict(out[k][k2])
                    merged.update(v2)
                    out[k][k2] = merged
                else:
                    out[k][k2] = v2
        else:
            out[k] = v
    return out


def parse_sid_overrides(body: str) -> dict:
    """Find a nested `case objprop.sid of 'sidA':…; 'sidB':…; end;` block in body and
    return {sid: stats} for each branch. Used for unit families where the outer branch
    label lists multiple sids and an inner `case objprop.sid` carves per-sid overrides
    on top of the shared base (e.g., the musketeer-line: musketeerpol/musketeernet/
    pandur/chasseur/highlander/etc all live in one outer branch)."""
    out: dict[str, dict] = {}
    for m in re.finditer(r"\bcase\s+objprop\.sid\s+of\b", body):
        start = m.end()
        depth = 1
        i = start
        n = len(body)
        in_str = False
        while i < n and depth > 0:
            if in_str:
                if body[i] == "'":
                    in_str = False
                i += 1
                continue
            if body[i] == "'":
                in_str = True
                i += 1
                continue
            if body[i:i+2] == "//":
                nl = body.find("\n", i)
                i = nl if nl != -1 else n
                continue
            if body[i] == "{":
                cl = body.find("}", i)
                i = cl + 1 if cl != -1 else n
                continue
            opened = False
            for kw, kl in (("begin", 5), ("case", 4), ("record", 6), ("try", 3)):
                if body[i:i+kl] == kw and _is_word_boundary(body, i, kl):
                    depth += 1
                    i += kl
                    opened = True
                    break
            if opened:
                continue
            if body[i:i+3] == "end" and _is_word_boundary(body, i, 3):
                depth -= 1
                i += 3
                continue
            i += 1
        case_inner = body[start:i - 3]
        for label, branch_body in split_case_branches(case_inner):
            if label == "else":
                continue
            sids = parse_label_sids(label)
            stats = parse_branch_body(branch_body)
            for s in sids:
                out[s] = stats
        break
    return out


def parse_nation_overrides(body: str) -> dict:
    """Find a nested `case nation of 'pol':…; 'tur','alg':…; end;` block in body and
    return {nation: stats} for each branch."""
    out: dict[str, dict] = {}
    # Find first nested case beginning with `case nation`
    for m in re.finditer(r"\bcase\s+nation\s+of\b", body):
        # find matching end
        start = m.end()
        depth = 1
        i = start
        n = len(body)
        in_str = False
        while i < n and depth > 0:
            if in_str:
                if body[i] == "'":
                    in_str = False
                i += 1
                continue
            if body[i] == "'":
                in_str = True
                i += 1
                continue
            if body[i:i+2] == "//":
                nl = body.find("\n", i)
                i = nl if nl != -1 else n
                continue
            if body[i] == "{":
                cl = body.find("}", i)
                i = cl + 1 if cl != -1 else n
                continue
            opened = False
            for kw, kl in (("begin", 5), ("case", 4), ("record", 6), ("try", 3)):
                if body[i:i+kl] == kw and _is_word_boundary(body, i, kl):
                    depth += 1
                    i += kl
                    opened = True
                    break
            if opened:
                continue
            if body[i:i+3] == "end" and _is_word_boundary(body, i, 3):
                depth -= 1
                i += 3
                continue
            i += 1
        case_inner = body[start:i - 3]
        for label, branch_body in split_case_branches(case_inner):
            if label == "else":
                continue
            nations = parse_label_sids(label)  # nation codes like 'pol','tur','alg'
            stats = parse_branch_body(branch_body)
            for n_name in nations:
                out[n_name] = stats
        break  # only first nested case nation
    return out


# Map for `case i of aus: ... fra: ...`
NATION_ID_TO_SID_LOCAL = {
    "aus": "aus", "fra": "fra", "eng": "eng", "spa": "spa", "rus": "rus",
    "ukr": "ukr", "pol": "pol", "swe": "swe", "pru": "pru", "ven": "ven",
    "tur": "tur", "alg": "alg", "mis": "mis", "net": "net", "den": "den",
    "por": "por", "pie": "pie", "sax": "sax", "bav": "bav", "hun": "hun",
    "swi": "swi", "sco": "sco", "tat": "tat", "lit": "lit",
}


def parse_nation_overrides_by_id(body: str) -> dict:
    """Find `case i of aus: …; fra: …;` block — labels are bare nation identifiers."""
    out: dict[str, dict] = {}
    for m in re.finditer(r"\bcase\s+i\s+of\b", body):
        start = m.end()
        depth = 1
        i = start
        n = len(body)
        in_str = False
        while i < n and depth > 0:
            if in_str:
                if body[i] == "'":
                    in_str = False
                i += 1
                continue
            if body[i] == "'":
                in_str = True
                i += 1
                continue
            if body[i:i+2] == "//":
                nl = body.find("\n", i)
                i = nl if nl != -1 else n
                continue
            if body[i] == "{":
                cl = body.find("}", i)
                i = cl + 1 if cl != -1 else n
                continue
            opened = False
            for kw, kl in (("begin", 5), ("case", 4), ("record", 6), ("try", 3)):
                if body[i:i+kl] == kw and _is_word_boundary(body, i, kl):
                    depth += 1
                    i += kl
                    opened = True
                    break
            if opened:
                continue
            if body[i:i+3] == "end" and _is_word_boundary(body, i, 3):
                depth -= 1
                i += 3
                continue
            i += 1
        case_inner = body[start:i - 3]
        for label, branch_body in split_case_branches(case_inner):
            if label == "else":
                continue
            # labels are bare identifiers, comma-separated
            ids = [t.strip() for t in label.split(",")]
            stats = parse_branch_body(branch_body)
            for ident in ids:
                if ident in NATION_ID_TO_SID_LOCAL:
                    out[NATION_ID_TO_SID_LOCAL[ident]] = stats
        break
    return out


COMMONSID_SUB_RE = re.compile(r"\bcase\s+objprop\.sid\s+of\b")


def parse_commonsid_subcase(body: str) -> dict[str, dict]:
    """Find `case objprop.sid of commonsid+'gol':...; commonsid+'iro':...; commonsid+'coa':...; end;`
    inside a building branch and return {suffix: extra_stats}."""
    out: dict[str, dict] = {}
    m = COMMONSID_SUB_RE.search(body)
    if not m:
        return out
    start = m.end()
    depth = 1
    i = start
    n = len(body)
    in_str = False
    while i < n and depth > 0:
        if in_str:
            if body[i] == "'":
                in_str = False
            i += 1
            continue
        if body[i] == "'":
            in_str = True
            i += 1
            continue
        if body[i:i+2] == "//":
            nl = body.find("\n", i)
            i = nl if nl != -1 else n
            continue
        if body[i] == "{":
            cl = body.find("}", i)
            i = cl + 1 if cl != -1 else n
            continue
        opened = False
        for kw, kl in (("begin", 5), ("case", 4), ("record", 6), ("try", 3)):
            if body[i:i+kl] == kw and _is_word_boundary(body, i, kl):
                depth += 1
                i += kl
                opened = True
                break
        if opened:
            continue
        if body[i:i+3] == "end" and _is_word_boundary(body, i, 3):
            depth -= 1
            i += 3
            continue
        i += 1
    case_inner = body[start:i - 3]
    for label, branch_body in split_case_branches(case_inner):
        if label == "else":
            continue
        suffixes = parse_label_commonsid_suffixes(label)
        stats = parse_branch_body(branch_body)
        for suf in suffixes:
            out[suf] = stats
    return out


if __name__ == "__main__":
    import sys, json
    sys.stdout.reconfigure(encoding="utf-8")
    from config import UNIT_SCRIPT
    text = UNIT_SCRIPT.read_text(encoding="utf-8", errors="replace")
    data = parse_unit_init_base(text)
    print(f"Parsed: {len(data['units'])} unit groups, "
          f"{len(data['common_buildings'])} common buildings, "
          f"{len(data['nation_buildings'])} per-nation building suffixes")
    print()
    print("Sample units:")
    for sid in ["pikeman", "pikemanrus", "pikemanspa", "musketeer", "strelet", "jannisary"]:
        if sid in data["units"]:
            u = data["units"][sid]
            print(f"  {sid}: base={u['base']!r}")
            if u["overrides"]:
                print(f"    overrides: {list(u['overrides'].keys())}")
        else:
            print(f"  {sid}: NOT FOUND")
    print()
    print("Sample common buildings:")
    for suf in ["mil", "sto", "mar", "por", "tow", "gol", "iro", "coa", "swa", "sga"]:
        if suf in data["common_buildings"]:
            b = data["common_buildings"][suf]
            print(f"  {suf}: base={b['base']!r}")
        else:
            print(f"  {suf}: NOT FOUND")
    print()
    print("Sample per-nation buildings:")
    for suf in ["cen", "bar", "ba2", "aca", "bla", "sta", "tem", "art", "dip", "hou"]:
        if suf in data["nation_buildings"]:
            b = data["nation_buildings"][suf]
            print(f"  {suf}: base={b['base']!r}")
            if b["overrides_nation"]:
                print(f"    overrides_nation: {sorted(b['overrides_nation'].keys())}")
        else:
            print(f"  {suf}: NOT FOUND")
