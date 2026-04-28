"""Symbolic simulator for `_country_InitUnitsUpgrades`.

Walks the procedure body as an AST and tracks string-var bindings + upgstruct state,
inlining the helper procedures `SetUpgStructFoodGold(/Iron/IronCoal)` and
`AddUpgradePack` so we can emit fully-resolved upgrade entries with cost/time/value.

Key technique: we re-use the tokenizer and parser from `parse_country.py`, but extend
parse_case to capture branches (so we can evaluate `case cid of _aus: …; _fra: …; end;`)
and add assignment-tracking + special-cased call handlers.

Output: list[dict] — one entry per emitted upgrade.
"""
from __future__ import annotations
import re
import copy
from pathlib import Path

from parse_country import (
    extract_proc_body, tokenize, ALL_NATIONS, _commonname_for,
    _commonname_storehouse, _commonname_market, _commonname_port,
    _is_word_boundary, Node,
)


# ---------- Constants from country.script:783-789 ----------

CTYPE_DAMAGE_PIKE = 0
CTYPE_DAMAGE_SWORD = 1
CTYPE_DAMAGE_BULLET = 2
CTYPE_PROTECTION = 3
CTYPE_PROTECTION_ONLY_PIKE_ARROW = 4
CTYPE_PROTECTION_ONLY_SWORD = 5
CTYPE_DAMAGE_ARROW = 6

CTYPE_BY_NAME = {
    "ctypeDamagePike": CTYPE_DAMAGE_PIKE,
    "ctypeDamageSword": CTYPE_DAMAGE_SWORD,
    "ctypeDamageBullet": CTYPE_DAMAGE_BULLET,
    "ctypeProtection": CTYPE_PROTECTION,
    "ctypeProtectionOnlyPikeArrow": CTYPE_PROTECTION_ONLY_PIKE_ARROW,
    "ctypeProtectionOnlySword": CTYPE_PROTECTION_ONLY_SWORD,
    "ctypeDamageArrow": CTYPE_DAMAGE_ARROW,
}

# Map per-nation literal names (`_aus`, `_fra`, etc.) to nation sid
NATION_LITERAL = {f"_{n}": n for n in ALL_NATIONS}


# ---------- Re-parser: extends parse_country.Parser to parse case branches ----------

class SimParser:
    """Tiny recursive-descent parser tuned for the simulator's needs."""

    def __init__(self, tokens: list[tuple[str, str]]):
        self.tokens = tokens
        self.pos = 0

    def peek(self, off: int = 0):
        i = self.pos + off
        return self.tokens[i] if i < len(self.tokens) else None

    def at(self, kind: str, text: str) -> bool:
        t = self.peek()
        return t is not None and t[0] == kind and t[1] == text

    def at_kw(self, *names: str) -> bool:
        t = self.peek()
        return t is not None and t[0] == "KW" and t[1] in names

    def consume(self):
        t = self.tokens[self.pos]
        self.pos += 1
        return t

    def parse_block(self) -> Node:
        node = Node(kind="block")
        while self.pos < len(self.tokens):
            t = self.peek()
            if t is None:
                break
            if t[0] == "KW" and t[1] == "end":
                self.consume()
                return node
            before = self.pos
            stmt = self.parse_stmt()
            if stmt is not None:
                node.children.append(stmt)
            if self.pos == before:
                self.pos += 1
        return node

    def parse_stmt(self) -> Node | None:
        t = self.peek()
        if t is None:
            return None
        if t[0] == "PUNCT" and t[1] == ";":
            self.consume()
            return None
        if t[0] == "KW":
            kw = t[1]
            if kw == "begin":
                self.consume()
                return self.parse_block()
            if kw == "if":
                return self.parse_if()
            if kw == "case":
                return self.parse_case()
            if kw in ("for", "while"):
                return self.parse_loop()
            if kw == "with":
                return self.parse_with()
            if kw in ("var", "const"):
                self.skip_to_semicolon()
                return None
            if kw in ("procedure", "function"):
                # Nested procedure/function declaration: skip declaration line and the
                # following begin..end; block.
                self.skip_to_semicolon()  # past `procedure FOO(...);`
                # If immediately followed by `begin`, consume balanced begin..end;
                if self.at_kw("begin"):
                    self.consume()
                    self.parse_block()  # consumes matching end
                    if self.peek() == ("PUNCT", ";"):
                        self.consume()
                return None
            if kw == "type":
                # `type T = class … end; T2 = record … end;` etc. — skip until ';'
                # at depth 0 where depth tracks class/record/object/interface.
                self._skip_type_declaration()
                return None
            if kw == "else":
                return None
            if kw == "end":
                return None
        if t[0] == "ID":
            return self.parse_call_or_assign()
        self.consume()
        return None

    def _skip_type_declaration(self):
        """Skip a `type` block including any `class … end` / `record … end` definitions.
        We continue until we see a top-level `;` not inside class/record/object."""
        self.consume()  # 'type'
        depth = 0
        while self.pos < len(self.tokens):
            t = self.peek()
            if t is None:
                return
            if t[0] == "KW" and t[1] in ("class", "record", "object", "interface"):
                depth += 1
                self.consume()
                continue
            if t[0] == "KW" and t[1] == "end":
                if depth > 0:
                    depth -= 1
                    self.consume()
                    continue
                else:
                    # `end` at depth 0 — outside any nested type, stop without consuming
                    return
            if t[0] == "PUNCT" and t[1] == ";" and depth == 0:
                self.consume()
                # Could be more type declarations on the next "name = …;" lines.
                # Heuristic: stop if next is a keyword that ends the type block.
                nxt = self.peek()
                if nxt is None or (nxt[0] == "KW" and nxt[1] in
                                   ("var", "const", "begin", "procedure", "function",
                                    "type", "if", "case", "for", "while", "with", "end")):
                    return
                continue
            self.consume()

    def parse_if(self) -> Node:
        self.consume()  # if
        cond = self.parse_expr_until(("KW", "then"))
        if self.at_kw("then"):
            self.consume()
        body = self.parse_stmt_or_block()
        else_block = None
        if self.at_kw("else"):
            self.consume()
            else_block = self.parse_stmt_or_block()
        return Node(kind="if", cond=cond, children=[body], else_block=else_block)

    def parse_stmt_or_block(self) -> Node:
        if self.at_kw("begin"):
            self.consume()
            return self.parse_block()
        n = self.parse_stmt()
        return n if n is not None else Node(kind="opaque")

    def parse_case(self) -> Node:
        """Parse `case <expr> of <branches> [else <stmt>] end` into a Node tree.
        children[0] = expr-as-string, children[1..N] = branches (each kind='case_branch').
        """
        self.consume()  # 'case'
        expr = self.parse_expr_until(("KW", "of"))
        if self.at_kw("of"):
            self.consume()
        node = Node(kind="case", cond=expr)
        # parse branches until 'end'
        while self.pos < len(self.tokens) and not self.at_kw("end"):
            t = self.peek()
            if t is None:
                break
            if t[0] == "KW" and t[1] == "else":
                self.consume()
                else_body = self.parse_stmt_or_block()
                # consume optional ';'
                if self.peek() == ("PUNCT", ";"):
                    self.consume()
                node.children.append(Node(kind="case_else", children=[else_body]))
                continue
            # Parse label list until ':'
            label_tokens = []
            while self.pos < len(self.tokens):
                t = self.peek()
                if t is None:
                    break
                if t[0] == "PUNCT" and t[1] == ":":
                    break
                if t[0] == "KW" and t[1] in ("end", "else"):
                    break
                if t[0] == "PUNCT" and t[1] == ";":
                    self.consume()
                    continue
                label_tokens.append(self.consume())
            if not label_tokens:
                break
            if self.peek() == ("PUNCT", ":"):
                self.consume()
            body = self.parse_stmt_or_block()
            if self.peek() == ("PUNCT", ";"):
                self.consume()
            label_str = "".join(t[1] if t[0] != "STR" else f"'{t[1]}'" for t in label_tokens)
            node.children.append(Node(kind="case_branch", cond=label_str.strip(),
                                      children=[body]))
        if self.at_kw("end"):
            self.consume()
        return node

    def parse_loop(self) -> Node:
        """Parse `for <var> := <start> to <end> do <body>` capturing var/start/end."""
        kw = self.consume()  # for/while
        var_name = None
        start_expr = None
        end_expr = None
        if kw[1] == "for":
            # Expect: <var> := <start> to <end> do
            head_tokens = []
            while self.pos < len(self.tokens):
                t = self.peek()
                if t is None: break
                if t[0] == "KW" and t[1] == "do":
                    break
                head_tokens.append(self.consume())
            # Try to parse "var := start to end"
            head = head_tokens
            try:
                if len(head) > 0 and head[0][0] == "ID":
                    var_name = head[0][1]
                # Find := and to
                colon_idx = next((i for i, t in enumerate(head)
                                  if t == ("PUNCT", ":") and i + 1 < len(head) and head[i+1] == ("PUNCT", "=")), None)
                to_idx = next((i for i, t in enumerate(head)
                               if t[0] == "KW" and t[1] == "to"), None)
                if colon_idx is not None and to_idx is not None:
                    start_parts = head[colon_idx+2:to_idx]
                    end_parts = head[to_idx+1:]
                    start_expr = "".join(t[1] for t in start_parts).strip()
                    end_expr = "".join(t[1] for t in end_parts).strip()
            except Exception:
                pass
        else:
            # while: skip until do
            while self.pos < len(self.tokens):
                t = self.consume()
                if t[0] == "KW" and t[1] == "do":
                    break
        # Consume the 'do'
        if self.at_kw("do"):
            self.consume()
        body = self.parse_stmt_or_block()
        node = Node(kind="loop", children=[body])
        if var_name and start_expr and end_expr:
            node.cond = f"{var_name}|{start_expr}|{end_expr}"
        return node

    def parse_with(self) -> Node:
        self.consume()  # with
        while self.pos < len(self.tokens):
            t = self.consume()
            if t[0] == "KW" and t[1] == "do":
                break
        body = self.parse_stmt_or_block()
        return Node(kind="with", children=[body])

    def skip_to_semicolon(self):
        while self.pos < len(self.tokens):
            t = self.consume()
            if t[0] == "PUNCT" and t[1] == ";":
                return

    def parse_expr_until(self, stop) -> str:
        parts = []
        depth = 0
        while self.pos < len(self.tokens):
            t = self.peek()
            if t == stop and depth == 0:
                break
            self.consume()
            if t[0] == "PUNCT":
                if t[1] == "(":
                    depth += 1
                elif t[1] == ")":
                    depth -= 1
                parts.append(t[1])
            elif t[0] == "KW":
                kw = t[1]
                if kw == "and": parts.append(" and ")
                elif kw == "or": parts.append(" or ")
                elif kw == "not": parts.append(" not ")
                elif kw == "true": parts.append("True")
                elif kw == "false": parts.append("False")
                else: parts.append(" " + kw + " ")
            elif t[0] == "ID":
                parts.append(t[1])
            elif t[0] == "NUM":
                parts.append(t[1])
            elif t[0] == "STR":
                parts.append(repr(t[1]))
        return "".join(parts).strip()

    def parse_call_or_assign(self) -> Node:
        ident_tok = self.consume()
        ident = ident_tok[1]
        # Check for member access: ident.member or ident[idx].member
        # Pattern: collect all `.<ident>` and `[<expr>]` until we reach '(' or ':=' or ';'
        lhs_tokens = [ident]
        while self.pos < len(self.tokens):
            t = self.peek()
            if t == ("PUNCT", "."):
                lhs_tokens.append(self.consume()[1])  # consume '.'
                if self.peek() and self.peek()[0] == "ID":
                    lhs_tokens.append(self.consume()[1])
                continue
            if t == ("PUNCT", "["):
                lhs_tokens.append(self.consume()[1])
                # collect until matching ]
                depth = 1
                while self.pos < len(self.tokens) and depth > 0:
                    t2 = self.consume()
                    if t2 == ("PUNCT", "["):
                        depth += 1
                    elif t2 == ("PUNCT", "]"):
                        depth -= 1
                    lhs_tokens.append(t2[1])
                continue
            break
        lhs_full = "".join(lhs_tokens)
        # call?
        if self.peek() == ("PUNCT", "("):
            self.consume()
            args = self.parse_args()
            if self.peek() == ("PUNCT", ";"):
                self.consume()
            return Node(kind="call", name=lhs_full, args=args)
        # assign?
        if self.peek() == ("PUNCT", ":") and self.peek(1) == ("PUNCT", "="):
            self.consume(); self.consume()
            # collect rhs until ';' at depth 0
            rhs_parts = []
            paren = 0
            while self.pos < len(self.tokens):
                t = self.peek()
                if t == ("PUNCT", ";") and paren == 0:
                    self.consume()
                    break
                self.consume()
                if t[0] == "PUNCT":
                    if t[1] == "(":
                        paren += 1
                    elif t[1] == ")":
                        paren -= 1
                if t[0] == "STR":
                    rhs_parts.append(repr(t[1]))
                else:
                    rhs_parts.append(t[1])
            rhs = "".join(rhs_parts).strip()
            return Node(kind="assign", name=lhs_full, args=[rhs])
        # otherwise skip until ';'
        while self.pos < len(self.tokens):
            t = self.consume()
            if t[0] == "PUNCT" and t[1] == ";":
                return Node(kind="opaque")
        return Node(kind="opaque")

    def parse_args(self) -> list[str]:
        args = []
        cur = []
        depth = 0
        while self.pos < len(self.tokens):
            t = self.consume()
            if t[0] == "PUNCT" and t[1] == "(":
                depth += 1
                cur.append("(")
            elif t[0] == "PUNCT" and t[1] == ")":
                if depth == 0:
                    args.append("".join(cur).strip())
                    return args
                depth -= 1
                cur.append(")")
            elif t[0] == "PUNCT" and t[1] == "," and depth == 0:
                args.append("".join(cur).strip())
                cur = []
            elif t[0] == "STR":
                cur.append(repr(t[1]))
            elif t[0] == "KW":
                cur.append(t[1])
            else:
                cur.append(t[1])
        return args


# ---------- garr_* arrays (hardcoded, country.script:3395-3450) ----------
#
# These arrays are populated at TCountry-init time with nation-specific sids,
# then `_country_AddUpgradeSArrParam2MemberIfExists` calls in loops apply
# them as targets to the just-added upgrade. Our AST walker can't track the
# `garr_X[k] := Y` assignments (parser eats them as opaque), so we hardcode
# the array contents per-nation here. See country.script:3395-3450 for source.

def _garr_buildings_all(nation: str) -> list[str]:
    """garr_BuildingsAll for a nation. 17 sids (per-nat + cluster-prefix)."""
    com = _commonname_for(nation)
    sto = _commonname_storehouse(nation)
    mar = _commonname_market(nation)
    por = _commonname_port(nation)
    return [
        f"{nation}cen", f"{nation}hou", f"{nation}bla", f"{nation}sta",
        f"{nation}tem", f"{nation}aca", f"{nation}dip", f"{nation}bar",
        f"{nation}ba2", f"{nation}art",
        f"{com}mil", f"{sto}sto",
        "eurgol", "euriro", "eurcoa",
        f"{mar}mar", f"{por}por",
    ]


def _garr_buildings_tower_wall(nation: str) -> list[str]:
    """garr_BuildingsTowerWall — walls/gates/towers across all clusters."""
    return [
        "eurswa", "eursga", "russwa", "russga", "turswa", "tursga",
        "eurtow", "rustow", "tustow",
    ]


_GARR_RESOLVERS = {
    "garr_BuildingsAll":      _garr_buildings_all,
    "garr_BuildingsTowerWall": _garr_buildings_tower_wall,
}


# ---------- Pre-substitution (re-uses parse_country logic but per-call) ----------

def _presubstitute(body: str, nat: str) -> str:
    nat_lit = f"'{nat}'"
    com = _commonname_for(nat)
    com_lit = f"'{com}'"
    out = re.sub(r"\bcsid\b", nat_lit, body)
    out = re.sub(r"\bcommonName2\b", com_lit, out)
    out = re.sub(r"\bcommonNameStorehouse\b", f"'{_commonname_storehouse(nat)}'", out)
    out = re.sub(r"\bcommonNameMarket\b", f"'{_commonname_market(nat)}'", out)
    out = re.sub(r"\bcommonNamePort\b", f"'{_commonname_port(nat)}'", out)
    out = re.sub(r"\bcommonName\b", com_lit, out)
    out = re.sub(r"\bblacksmith\b", f"'{nat}bla'", out)
    out = re.sub(r"\bacademy\b", f"'{nat}aca'", out)
    out = re.sub(r"\bcentury18\b", f"'{nat}cen.1'", out)
    out = re.sub(r"\benablefrigate\b", f"'{nat}aca.6'", out)
    out = re.sub(r"\benablebattleship\b", f"'{nat}aca.29'", out)
    out = re.sub(r"\benablemulticannon\b", f"'{nat}aca.19'", out)
    # Local-var simplifications: see country.script:1000 — tmptype is always ctypeProtection
    out = re.sub(r"\btmptype\b", "ctypeProtection", out)
    return out


# ---------- Symbolic execution ----------

_GARR_RE = re.compile(r"\b(garr_BuildingsAll|garr_BuildingsTowerWall)\s*\[\s*([^\]]+)\s*\]")


def _eval_string_arg(arg: str, env: dict) -> str:
    """Resolve a single arg to a Python string (or '' on failure).

    Special-cases `garr_BuildingsAll[k]` / `garr_BuildingsTowerWall[k]` lookups
    by consulting hardcoded arrays (country.script:3395-3450). Returns '' for
    out-of-range indices so callers in unrolled loops over k=0..127 can skip.
    Nation is read from env["__nation"] when populating garr_* arrays.
    """
    s = arg.strip()
    # Replace IntToStr(n) → str(n)
    s = re.sub(r"\bIntToStr\(([^)]+)\)", r"str(\1)", s)
    # Resolve garr_*[k] before generic eval (eval doesn't know these arrays).
    nation = env.get("__nation")
    def _garr_repl(m: re.Match) -> str:
        if nation is None:
            return "''"
        arr_name = m.group(1)
        try:
            idx = int(eval(m.group(2), {"__builtins__": {}}, env))
        except Exception:
            return "''"
        arr = _GARR_RESOLVERS[arr_name](nation)
        return repr(arr[idx]) if 0 <= idx < len(arr) else "''"
    s = _GARR_RE.sub(_garr_repl, s)
    # Provide locals for member, upgplace, blacksmith, academy, century18 (already pre-subst.)
    locals_dict = dict(env)
    try:
        v = eval(s, {"__builtins__": {"str": str}}, locals_dict)
        if v is None:
            return ""
        return str(v)
    except Exception:
        return s  # return raw


def _eval_int_arg(arg: str, env: dict) -> int | None:
    s = arg.strip()
    s = re.sub(r"\{[^}]*\}", "", s)
    if s == "" or s.lower() == "default":
        return None
    s = _pascal_to_py(s)
    locals_dict = dict(env)
    try:
        v = eval(s, {"__builtins__": {"str": str, "int": int}}, locals_dict)
        if isinstance(v, bool):
            return int(v)
        if isinstance(v, (int, float)):
            return int(v)
    except Exception:
        pass
    return None


def _eval_bool_arg(arg: str, env: dict) -> bool | None:
    s = arg.strip().lower()
    if s == "true": return True
    if s == "false": return False
    s = _pascal_to_py(arg.strip())
    locals_dict = dict(env)
    try:
        v = eval(s, {"__builtins__": {}}, locals_dict)
        if isinstance(v, bool):
            return v
    except Exception:
        pass
    return None


def _pascal_to_py(expr: str) -> str:
    """Translate Pascal comparison operators to Python equivalents."""
    # `<>` → `!=` (must come before splitting `<` and `>`)
    expr = expr.replace("<>", "!=")
    # Pascal `=` (in expressions, NOT inside `:=` assignment context) → `==`. We've
    # already passed assignments separately, so any standalone `=` here is comparison.
    # But careful: `==` should stay as `==`. Use a regex to replace `=` not preceded
    # by `=`, `<`, `>`, `!`, `:`.
    expr = re.sub(r"(?<![=<>!:])=(?!=)", "==", expr)
    return expr


def _new_upgstruct() -> dict:
    return {
        "place": "", "member": "",
        "value": [0]*6, "food": [0]*6, "wood": [0]*6, "stone": [0]*6,
        "gold": [0]*6, "iron": [0]*6, "coal": [0]*6,
        "req": ["", ""],  # only first two used in setters; rest default
    }


def _set_upgstruct_food_gold(args: list[str], env: dict) -> dict:
    """SetUpgStructFoodGold(upgstruct, place, member,
        v0, f0, g0, b0, v1, f1, g1, b1, v2, f2, g2, b2, v3, f3, g3, b3, v4, f4, g4, b4,
        v5, f5, g5, req0, req1)"""
    s = _new_upgstruct()
    s["place"]  = _eval_string_arg(args[1], env) if len(args) > 1 else ""
    s["member"] = _eval_string_arg(args[2], env) if len(args) > 2 else ""
    # 6 levels: each block = (value, food, gold, bool[skipped on last])
    # Indices: v0=3,f0=4,g0=5,b0=6, v1=7,f1=8,g1=9,b1=10, v2=11..b2=14,
    #          v3=15..b3=18, v4=19..b4=22, v5=23,f5=24,g5=25, req0=26, req1=27
    layout = [(3,4,5), (7,8,9), (11,12,13), (15,16,17), (19,20,21), (23,24,25)]
    for j, (vi, fi, gi) in enumerate(layout):
        s["value"][j] = _eval_int_arg(args[vi], env) or 0 if vi < len(args) else 0
        s["food"][j]  = _eval_int_arg(args[fi], env) or 0 if fi < len(args) else 0
        s["gold"][j]  = _eval_int_arg(args[gi], env) or 0 if gi < len(args) else 0
    return s


def _set_upgstruct_food_gold_iron(args: list[str], env: dict) -> dict:
    """SetUpgStructFoodGoldIron: same as FoodGold but with iron0..iron5 inserted.
    Layout: (v, f, g, i, b) per level for j=0..4, and (v5,f5,g5,i5) for j=5, then req0,req1.
    Indices: v0=3,f0=4,g0=5,i0=6,b0=7; v1=8..i1=11,b1=12; ...; v5=28,f5=29,g5=30,i5=31, req0=32,req1=33
    """
    s = _new_upgstruct()
    s["place"]  = _eval_string_arg(args[1], env) if len(args) > 1 else ""
    s["member"] = _eval_string_arg(args[2], env) if len(args) > 2 else ""
    layout = [(3,4,5,6), (8,9,10,11), (13,14,15,16), (18,19,20,21), (23,24,25,26), (28,29,30,31)]
    for j, (vi, fi, gi, ii) in enumerate(layout):
        s["value"][j] = _eval_int_arg(args[vi], env) or 0 if vi < len(args) else 0
        s["food"][j]  = _eval_int_arg(args[fi], env) or 0 if fi < len(args) else 0
        s["gold"][j]  = _eval_int_arg(args[gi], env) or 0 if gi < len(args) else 0
        s["iron"][j]  = _eval_int_arg(args[ii], env) or 0 if ii < len(args) else 0
    return s


def _set_upgstruct_food_gold_iron_coal(args: list[str], env: dict) -> dict:
    """SetUpgStructFoodGoldIronCoal: + coal per level.
    Layout: (v,f,g,i,c,b) per level for j=0..4, then (v,f,g,i,c) for j=5.
    v0=3,f0=4,g0=5,i0=6,c0=7,b0=8; v1=9..c1=13,b1=14; ...; v5=33,f5=34,g5=35,i5=36,c5=37
    """
    s = _new_upgstruct()
    s["place"]  = _eval_string_arg(args[1], env) if len(args) > 1 else ""
    s["member"] = _eval_string_arg(args[2], env) if len(args) > 2 else ""
    layout = [(3,4,5,6,7), (9,10,11,12,13), (15,16,17,18,19),
              (21,22,23,24,25), (27,28,29,30,31), (33,34,35,36,37)]
    for j, (vi, fi, gi, ii, ci) in enumerate(layout):
        s["value"][j] = _eval_int_arg(args[vi], env) or 0 if vi < len(args) else 0
        s["food"][j]  = _eval_int_arg(args[fi], env) or 0 if fi < len(args) else 0
        s["gold"][j]  = _eval_int_arg(args[gi], env) or 0 if gi < len(args) else 0
        s["iron"][j]  = _eval_int_arg(args[ii], env) or 0 if ii < len(args) else 0
        s["coal"][j]  = _eval_int_arg(args[ci], env) or 0 if ci < len(args) else 0
    return s


def _add_upgrade_pack(args: list[str], state: dict, env: dict, sink: list, nation: str):
    """AddUpgradePack(country, upgstruct, upgradetype, tooltiptype, x, y, bEnabled, ind, linkind)
    Emits up to 6 upgrade entries based on state['upgstruct']."""
    import os
    upgstruct = state.get("upgstruct")
    if not upgstruct:
        if os.environ.get("DEBUG_SIM"):
            print(f"  AddUpgradePack: no upgstruct, args={args}", flush=True)
        return
    upgradetype_str = args[2].strip() if len(args) > 2 else ""
    upgradetype = CTYPE_BY_NAME.get(upgradetype_str)
    if upgradetype is None:
        # Try resolving as int via env (catches local ints like `tmptype`)
        try:
            upgradetype = eval(upgradetype_str, {"__builtins__": {}}, env)
            if isinstance(upgradetype, bool):
                upgradetype = int(upgradetype)
            if not isinstance(upgradetype, int):
                if os.environ.get("DEBUG_SIM"):
                    print(f"  AddUpgradePack: upgradetype_str={upgradetype_str!r} not int", flush=True)
                return
        except Exception:
            if os.environ.get("DEBUG_SIM"):
                print(f"  AddUpgradePack: cannot resolve upgradetype_str={upgradetype_str!r}", flush=True)
            return
    if os.environ.get("DEBUG_SIM"):
        print(f"  AddUpgradePack: upgradetype={upgradetype} ({upgradetype_str}) place={upgstruct['place']!r} member={upgstruct['member']!r} values={upgstruct['value']}", flush=True)
    tooltiptype = _eval_int_arg(args[3], env) if len(args) > 3 else None
    x = _eval_int_arg(args[4], env) if len(args) > 4 else None
    y = _eval_int_arg(args[5], env) if len(args) > 5 else None
    bEnabled = _eval_bool_arg(args[6], env) if len(args) > 6 else True
    # iupgtype2 from upgradetype
    if upgradetype in (CTYPE_DAMAGE_PIKE, CTYPE_DAMAGE_SWORD,
                       CTYPE_DAMAGE_BULLET, CTYPE_DAMAGE_ARROW):
        iupgtype2 = 1
        itype = "damage"
    else:
        iupgtype2 = 2
        itype = "protection"
    place = upgstruct["place"]
    member = upgstruct["member"]
    if not place or not member:
        return
    for j in range(6):
        if upgstruct["value"][j] == 0:
            continue
        sid = f"{place}.{member}.{iupgtype2}.{j+1}"
        sink.append({
            "sid": sid,
            "nation": nation,
            "level": j + 2,
            "value": upgstruct["value"][j],
            "itype": itype,
            "tooltiptype": tooltiptype,
            "time": 500,  # AddUpgradePack hardcodes time=500
            "food":  upgstruct["food"][j],
            "wood":  upgstruct["wood"][j],
            "stone": upgstruct["stone"][j],
            "gold":  upgstruct["gold"][j],
            "iron":  upgstruct["iron"][j],
            "coal":  upgstruct["coal"][j],
            "x": x, "y": y,
            "place": place,
            "member": member,
            "_source": "AddUpgradePack",
        })


def _add_upgrade_with_access(args: list[str], state: dict, env: dict, sink: list, nation: str):
    """_country_AddUpgradeWithAccessControl(country, upgid, level, tooltiptype, itype, value,
       enabled, time, x, y, ind, food, wood, stone, gold, iron, coal, bAddIfNotExist,
       iarr1p0..2, sarr2p0..9, bAccessControl, req0..7)"""
    if len(args) < 17:
        return
    upgid = _eval_string_arg(args[1], env)
    if not upgid or upgid == "null":
        # `null` is a Pascal nil literal that survives eval as a raw token; skip those rows.
        return
    # Prereqs for WithAccessControl: bAccessControl @ 31, then req0..req7 @ 32..39
    prereqs: list[str] = []
    for i in (32, 33, 34, 35, 36, 37, 38, 39):
        if i < len(args):
            r = _eval_string_arg(args[i], env)
            if r:
                prereqs.append(r)
    # Initial sarr2 (args 21..30) — first slots typically hold target sids,
    # last 6 hold per-resource percentage strings for `priceperc` upgrades.
    initial_sarr2: list[str] = []
    for i in range(21, min(31, len(args))):
        v = _eval_string_arg(args[i], env)
        initial_sarr2.append(v)
    # Split: ints (target sids) → targets, last 6 → resource_pcts (for priceperc)
    targets: list[str] = []
    resource_pcts: dict[str, int] = {}
    if len(initial_sarr2) >= 6:
        # Last 6 entries are food/wood/stone/gold/iron/coal pct strings
        res_keys = ("food", "wood", "stone", "gold", "iron", "coal")
        for k_idx, key in enumerate(res_keys):
            tail_pos = len(initial_sarr2) - 6 + k_idx
            if 0 <= tail_pos < len(initial_sarr2):
                tail_v = initial_sarr2[tail_pos]
                if tail_v:
                    try:
                        pct = int(tail_v.strip("'\""))
                        if pct != 0:
                            resource_pcts[key] = pct
                    except (ValueError, TypeError):
                        pass
        head = initial_sarr2[:-6]
    else:
        head = initial_sarr2
    for v in head:
        if v and v != "''" and v != "":
            targets.append(v)

    rec = {
        "sid": upgid,
        "nation": nation,
        "level": _eval_int_arg(args[2], env),
        "tooltiptype": _eval_int_arg(args[3], env),
        "itype": args[4].strip() if len(args) > 4 else None,
        "value": _eval_int_arg(args[5], env),
        "time": _eval_int_arg(args[7], env),
        "food":  _eval_int_arg(args[11], env),
        "wood":  _eval_int_arg(args[12], env),
        "stone": _eval_int_arg(args[13], env),
        "gold":  _eval_int_arg(args[14], env),
        "iron":  _eval_int_arg(args[15], env),
        "coal":  _eval_int_arg(args[16], env),
        "prereqs": prereqs,
        "targets": targets,           # sid list this upgrade targets (priceperc/buildtimeperc/etc.)
        "resource_pcts": resource_pcts,  # per-resource % for priceperc only
        "_source": "AddUpgradeWithAccessControl",
    }
    sink.append(rec)
    state["last_upgrade"] = rec  # for ModifyUpgrade and SArrParam2MemberIfExists


def _add_plain_upgrade(args: list[str], state: dict, env: dict, sink: list, nation: str):
    """_country_AddUpgrade — same as WithAccessControl but with a different signature:
    (country, upgid, level, tooltiptype, itype, value, enabled, time, x, y, ind,
     food, wood, stone, gold, iron, coal, bAddIfNotExist, iarr1p0..2, sarr2p0..9)"""
    _add_upgrade_with_access(args, state, env, sink, nation)


def _modify_upgrade(args: list[str], state: dict, env: dict, sink: list, nation: str):
    """_country_ModifyUpgrade(country, upgind, value, food, wood, stone, gold, iron, coal)
    Patches the last-added upgrade. Args of `default` (-1) mean don't change."""
    last = state.get("last_upgrade")
    if last is None:
        return
    field_map = [(2, "value"), (3, "food"), (4, "wood"), (5, "stone"),
                 (6, "gold"), (7, "iron"), (8, "coal")]
    for idx, name in field_map:
        if idx >= len(args):
            continue
        v = _eval_int_arg(args[idx], env)
        if v is not None and v != -1:
            last[name] = v


# ---------- Walker ----------

def walk_sim(node: Node, state: dict, env: dict, sink: list, nation: str):
    if node is None:
        return
    k = node.kind
    if k in ("block", "with"):
        for c in node.children:
            walk_sim(c, state, env, sink, nation)
    elif k == "loop":
        if node.cond and "|" in node.cond:
            var_name, start_expr, end_expr = node.cond.split("|", 2)
            try:
                start = int(eval(start_expr, {"__builtins__": {}}, env))
                end = int(eval(end_expr, {"__builtins__": {}}, env))
            except Exception:
                # Can't determine bounds — walk body once with var unbound
                for c in node.children:
                    walk_sim(c, state, env, sink, nation)
                return
            # Cap iterations defensively
            if end - start > 100:
                end = start + 100
            for i in range(start, end + 1):
                env[var_name] = i
                for c in node.children:
                    walk_sim(c, state, env, sink, nation)
        else:
            for c in node.children:
                walk_sim(c, state, env, sink, nation)
    elif k == "if":
        cond = _pascal_to_py(node.cond or "True")
        try:
            v = eval(cond, {"__builtins__": {}}, env)
        except Exception:
            v = True
        if v:
            walk_sim(node.children[0], state, env, sink, nation)
        elif node.else_block is not None:
            walk_sim(node.else_block, state, env, sink, nation)
    elif k == "case":
        # Evaluate guard for each branch
        cond = _pascal_to_py(node.cond.strip()) if node.cond else ""
        try:
            cond_val = eval(cond, {"__builtins__": {}}, env)
        except Exception:
            cond_val = None
        else_node = None
        matched = False
        for child in node.children:
            if child.kind == "case_else":
                else_node = child
                continue
            if child.kind != "case_branch":
                continue
            label = (child.cond or "").strip()
            if matched:
                continue
            label_parts = [p.strip() for p in label.split(",")]
            for part in label_parts:
                if part in NATION_LITERAL:
                    if NATION_LITERAL[part] == nation:
                        walk_sim(child.children[0], state, env, sink, nation)
                        matched = True
                        break
                try:
                    pv = eval(_pascal_to_py(part), {"__builtins__": {}}, env)
                    if cond_val == pv:
                        walk_sim(child.children[0], state, env, sink, nation)
                        matched = True
                        break
                except Exception:
                    pass
        if not matched and else_node is not None:
            walk_sim(else_node.children[0], state, env, sink, nation)
    elif k == "assign":
        lhs = node.name
        rhs = node.args[0] if node.args else ""
        # Track string variables AND simple int variables (member, upgplace, tmptype, etc.)
        if lhs in ("member", "upgplace"):
            v = _eval_string_arg(rhs, env)
            env[lhs] = v
        elif "." not in lhs and "[" not in lhs:
            # Try eval as int (for tmptype, bEnabled, etc.)
            try:
                v = eval(rhs, {"__builtins__": {}}, env)
                env[lhs] = v
            except Exception:
                pass
    elif k == "call":
        name = node.name
        args = node.args or []
        if name == "SetUpgStructFoodGold":
            state["upgstruct"] = _set_upgstruct_food_gold(args, env)
        elif name == "SetUpgStructFoodGoldIron":
            state["upgstruct"] = _set_upgstruct_food_gold_iron(args, env)
        elif name == "SetUpgStructFoodGoldIronCoal":
            state["upgstruct"] = _set_upgstruct_food_gold_iron_coal(args, env)
        elif name == "AddUpgradePack":
            _add_upgrade_pack(args, state, env, sink, nation)
        elif name == "_country_AddUpgradeWithAccessControl":
            _add_upgrade_with_access(args, state, env, sink, nation)
        elif name == "_country_AddUpgrade":
            _add_plain_upgrade(args, state, env, sink, nation)
        elif name == "_country_ModifyUpgrade":
            _modify_upgrade(args, state, env, sink, nation)
        elif name == "ResetUpgStruct":
            state["upgstruct"] = _new_upgstruct()
        elif name in ("_country_AddUpgradeLink", "_country_AddUpgradeLinkRange"):
            pass  # link metadata, ignore
        elif name == "_country_AddUpgradeSArrParam2MemberIfExists":
            # Signature: (country, upgind, sid). Append `sid` to the most recent
            # upgrade's `targets` list. `upgind` is `ind-1` so it always refers
            # to the just-added upgrade — we use state["last_upgrade"] for that.
            last = state.get("last_upgrade")
            if last is not None and len(args) >= 3:
                tgt = _eval_string_arg(args[2], env)
                # Skip empty (out-of-range garr_*[k]), duplicates, and unresolved
                # raw expressions (won't help simulator).
                if (tgt and tgt != "''" and tgt not in last.get("targets", [])
                        and not tgt.startswith(("garr_", "csid+", "commonName"))):
                    last.setdefault("targets", []).append(tgt)
        elif name in ("_country_AddFixedProduce", "_country_AddFixedProduceWithAccessControl"):
            # signature: (country, fpind, producer_sid, product_sid, x, y, ind, [req0, req1, req2])
            if len(args) >= 4:
                producer = _eval_string_arg(args[2], env)
                product = _eval_string_arg(args[3], env)
                if producer and product and "+" not in producer and "+" not in product:
                    # Extract prereqs (req0/req1/req2) for the WithAccessControl variant
                    reqs: list[str] = []
                    if name == "_country_AddFixedProduceWithAccessControl":
                        for i in (7, 8, 9):
                            if i < len(args):
                                r = _eval_string_arg(args[i], env)
                                if r:
                                    reqs.append(r)
                    sink.append({
                        "_kind": "fixed_produce",
                        "producer": producer,
                        "product": product,
                        "nation": nation,
                        "prereqs": reqs,
                        "_source": "AddFixedProduce",
                    })
        # other calls: ignore
    elif k == "opaque":
        pass


def make_env(nat: str) -> dict:
    env = {n: (n == nat) for n in ALL_NATIONS}
    env["__nation"] = nat
    env["bAddIfNotExist"] = True
    env["cTrue"] = True
    env["True"] = True; env["False"] = False
    # Constants from country.script:783-789
    env["ctypeDamagePike"] = CTYPE_DAMAGE_PIKE
    env["ctypeDamageSword"] = CTYPE_DAMAGE_SWORD
    env["ctypeDamageBullet"] = CTYPE_DAMAGE_BULLET
    env["ctypeProtection"] = CTYPE_PROTECTION
    env["ctypeProtectionOnlyPikeArrow"] = CTYPE_PROTECTION_ONLY_PIKE_ARROW
    env["ctypeProtectionOnlySword"] = CTYPE_PROTECTION_ONLY_SWORD
    env["ctypeDamageArrow"] = CTYPE_DAMAGE_ARROW
    # Nation IDs
    for i, n in enumerate(ALL_NATIONS):
        env[f"_{n}"] = i
    env["cid"] = ALL_NATIONS.index(nat) if nat in ALL_NATIONS else -1
    # Initial empty member/upgplace
    env["member"] = ""
    env["upgplace"] = ""
    # Booleans for bhave18century etc.
    env["bhave18century"] = nat not in ("ukr", "tur", "alg")
    return env


def _simulate_proc(country_text: str, proc_name: str, nat: str, sink: list, env: dict | None = None):
    """Run the simulator on a single procedure and append emissions to sink."""
    body = extract_proc_body(country_text, proc_name)
    body = _presubstitute(body, nat)
    tokens = tokenize(body)
    if tokens and tokens[0] == ("KW", "begin"):
        tokens = tokens[1:]
    parser = SimParser(tokens)
    root = parser.parse_block()
    state = {"upgstruct": None, "last_upgrade": None}
    if env is None:
        env = make_env(nat)
    walk_sim(root, state, env, sink, nat)


# Pattern for `country.upgrade[ind-1].sarrparam2[...gc_resource_type_X-1] := 'NN';`
# Captures the resource name (food/wood/stone/gold/iron/coal) and signed pct.
_RES_PCT_RE = re.compile(
    r"country\.upgrade\[ind-1\]\.sarrparam2\["
    r"\s*gc_upgrade_maxarrparam2count\s*-\s*gc_ResCount\s*\+\s*"
    r"gc_resource_type_(\w+)\s*-\s*1\s*\]"
    r"\s*:=\s*'(-?\d+)'\s*;"
)
# Pattern matching an `_country_AddUpgrade*` call line (just to find positions).
_ADDUPG_RE = re.compile(
    r"_country_AddUpgrade(?:WithAccessControl)?\s*\(\s*country\s*,\s*([^,]+)"
)


def _attach_resource_pcts(country_text: str, nat: str, sink: list) -> None:
    """Walk the country.script body line by line. For each `AddUpgrade*(...)` call,
    capture `sarrparam2[...] := 'NN'` lines until the next AddUpgrade — these
    are the per-resource percentage modifiers for that upgrade. Match them to
    upgrade entries in `sink` by sid and attach to `resource_pcts`.

    The script doesn't include line numbers, but we can scan the textual order
    and use the upgrade sid (after pre-substitution for nation) as the key.
    """
    # Pre-substitute the body for this nation so 'csid+' / 'commonName+' resolve
    body = _presubstitute(country_text, nat)
    # Index sink by sid for quick lookup
    by_sid = {u["sid"]: u for u in sink if u.get("sid")}
    # Find all AddUpgrade* call positions and their first arg (the upgid expr)
    upg_positions: list[tuple[int, str]] = []
    for m in _ADDUPG_RE.finditer(body):
        # Resolve the upgid arg (first arg after `country,`)
        # Grab a window after the match start to find the second arg
        start = m.start()
        # Use _eval_string_arg with the env evaluated at this line
        # But env state is dynamic (member, place). We approximate by extracting
        # the literal upgid expr and evaluating with a minimal env. This is
        # imperfect — works for upgrades with literal sids in args.
        # Quick'n'dirty: search for the second arg (the sid) by finding the
        # comma after the function open paren.
        upg_positions.append((start, ""))
    # Scan: for each AddUpgrade position, find resource_pct assignments BEFORE
    # the next AddUpgrade and attach them to the most recent sink entry whose
    # source-text position matches. Since we don't track sink positions in the
    # script, fall back to ORDER: the i-th AddUpgrade match maps to the i-th
    # sink upgrade we processed for this nation. This works because the walker
    # appends in order.
    nat_sink = [u for u in sink if u.get("nation") == nat and u.get("itype") == "gc_upg_type_priceperc"]
    if not nat_sink:
        return
    # Walk the body and accumulate (start_pos, [(res, pct), ...]) per AddUpgrade
    pcts_by_pos: list[dict[str, int]] = [dict() for _ in upg_positions]
    for m in _RES_PCT_RE.finditer(body):
        # Find which AddUpgrade this assignment belongs to (the most recent one before it)
        pos = m.start()
        # Binary search would be faster; linear is fine for ~600 upgrades
        last_upg_idx = -1
        for i, (up_pos, _) in enumerate(upg_positions):
            if up_pos < pos:
                last_upg_idx = i
            else:
                break
        if last_upg_idx >= 0:
            res = m.group(1)
            try:
                pct = int(m.group(2))
                if pct != 0:
                    pcts_by_pos[last_upg_idx][res] = pct
            except ValueError:
                pass
    # Now we have pcts indexed by AddUpgrade position. We need to map from
    # AddUpgrade position → sink entry for THIS nation.
    # The walker visits all AddUpgrade calls but creates a sink entry only for
    # those reachable for `nat` (gated by `if (aus) then ...`). We can't trust
    # 1-to-1 ordering. Best-effort: for each priceperc sink entry, find the
    # AddUpgrade call whose upgid (after substitution) matches.
    upg_idx_by_substituted_sid: dict[str, int] = {}
    for i, m in enumerate(_ADDUPG_RE.finditer(body)):
        # Capture the upgid expression — it's the second arg in the args list,
        # extracted via a tighter regex starting at this match.
        rest = body[m.start():m.start() + 200]
        m2 = re.match(
            r"_country_AddUpgrade(?:WithAccessControl)?\s*\(\s*country\s*,\s*([^,]+),",
            rest,
        )
        if not m2:
            continue
        # Evaluate the upgid expression in a per-nation env to resolve concat'd strings
        sid_eval = _eval_string_arg(m2.group(1), {"__nation": nat})
        # The script wraps upgid as e.g. `upgplace+'.7'`; without `member`/`upgplace` in
        # env we can't fully resolve. Skip if it doesn't look like a simple sid.
        if not sid_eval or "+" in sid_eval or "upgplace" in sid_eval:
            continue
        upg_idx_by_substituted_sid[sid_eval] = i
    # Attach
    for u in nat_sink:
        if u["sid"] in upg_idx_by_substituted_sid:
            i = upg_idx_by_substituted_sid[u["sid"]]
            if i < len(pcts_by_pos) and pcts_by_pos[i]:
                u["resource_pcts"] = dict(pcts_by_pos[i])


def simulate(country_text: str, nat: str, *, dedup: bool = True) -> list[dict]:
    sink: list[dict] = []
    env = make_env(nat)
    # Process _country_InitUnitsUpgrades first (per-unit blacksmith/stable upgrades)
    _simulate_proc(country_text, "_country_InitUnitsUpgrades", nat, sink, env=env)
    # Then _country_Init (academy/mill/etc. upgrades + nation roster)
    _simulate_proc(country_text, "_country_Init", nat, sink, env=env)
    # Augment priceperc upgrades with resource percentages from direct assignments
    # of the form: `country.upgrade[ind-1].sarrparam2[...gc_resource_type_X-1] := 'NN'`
    # which the AST walker treats as opaque.
    _attach_resource_pcts(country_text, nat, sink)
    # Drop entries with unresolved sids (e.g., from inside the nested AddUpgradePack
    # proc declaration that may have leaked through). Keep fixed_produce events as-is.
    sink = [u for u in sink
            if u.get("_kind") == "fixed_produce" or
            (u.get("sid") and "+" not in u["sid"]
             and "upgstruct" not in u["sid"] and "csid" not in u["sid"])]
    if dedup:
        # Keep last-write-wins (mirrors real game: AddUpgrade with same id overwrites).
        last: dict[str, dict] = {}
        fp_seen: set[tuple[str, str]] = set()
        deduped = []
        for u in sink:
            if u.get("_kind") == "fixed_produce":
                key = (u["producer"], u["product"])
                if key in fp_seen:
                    continue
                fp_seen.add(key)
                deduped.append(u)
            else:
                last[u["sid"]] = u
        deduped.extend(last.values())
        sink = deduped
    return sink


if __name__ == "__main__":
    import sys, json
    sys.stdout.reconfigure(encoding="utf-8")
    from config import COUNTRY_SCRIPT, PLAYABLE_NATIONS
    text = COUNTRY_SCRIPT.read_text(encoding="utf-8", errors="replace")
    print("Simulating per-nation upgrades:")
    for nat in PLAYABLE_NATIONS:
        upgrades = simulate(text, nat)
        print(f"  {nat}: {len(upgrades)} upgrades emitted")
    # Show samples for Russia
    print("\nSample for rus (first 12):")
    upgrades = simulate(text, "rus")
    for u in upgrades[:12]:
        food = u.get('food') or 0
        gold = u.get('gold') or 0
        iron = u.get('iron') or 0
        coal = u.get('coal') or 0
        wood = u.get('wood') or 0
        stone = u.get('stone') or 0
        val = u.get('value')
        print(f"  {u['sid']:42s} lvl={u['level']} val={val} cost=F{food}/W{wood}/S{stone}/G{gold}/I{iron}/C{coal} src={u['_source']}")
    print(f"\nTotal for rus: {len(upgrades)}")
    # Sample blacksmith pikeman
    print("\nrusbla.pikemanrus.* (Russian blacksmith pikeman upgrades):")
    for u in upgrades:
        if "pikemanrus" in u["sid"]:
            food = u.get('food') or 0
            gold = u.get('gold') or 0
            iron = u.get('iron') or 0
            print(f"  {u['sid']:42s} lvl={u['level']} val={u['value']} cost=F{food}/G{gold}/I{iron}")
