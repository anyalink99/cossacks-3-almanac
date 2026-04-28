"""Parse country.script — extract per-nation rosters and upgrade definitions.

Strategy:
1. Read the body of _country_Init.
2. Strip comments.
3. Tokenize into a recursive-descent friendly stream.
4. For each playable nation, evaluate boolean guards (if (aus) then ...) and
   collect the AddMember/AddUpgrade calls that are reachable.

The parser is simple but tolerant: it handles
  - `if (cond) then stmt;`
  - `if (cond) then begin ... end;`
  - `if (cond) then begin ... end else begin ... end;`
  - nested ifs and begins
and treats unrecognised statements as opaque (just skip).
"""
from __future__ import annotations
import re
from pathlib import Path
from dataclasses import dataclass, field
from typing import Any


# ---------- Tokenizer ----------

TOKEN_RE = re.compile(
    r"""
      \s+                                       # whitespace (skipped)
    | //[^\n]*                                  # line comment
    | \{[^}]*\}                                 # brace comment
    | '(?:[^'])*'                               # single-quoted string (Pascal — no escapes inside)
    | \b(?:if|then|else|begin|end|var|const|procedure|function|case|of|for|to|do|while|repeat|until|with|type|class|record|object|interface|try|except|finally|array)\b
    | _country_Add\w+                           # AddMember/AddUpgrade* etc.
    | _country_\w+                              # other helpers
    | [A-Za-z_][A-Za-z0-9_]*                    # identifier
    | \d+(?:\.\d+)?                             # number
    | [;,()\[\]:.+\-*/=<>]                      # punctuation
    """,
    re.VERBOSE,
)


def tokenize(text: str) -> list[tuple[str, str]]:
    """Return list of (kind, text) tokens. kind is 'KW', 'STR', 'NUM', 'ID', 'PUNCT', 'COMMENT'."""
    tokens: list[tuple[str, str]] = []
    KEYWORDS = {"if", "then", "else", "begin", "end", "var", "const", "procedure",
                "function", "case", "of", "for", "to", "do", "while", "repeat",
                "until", "with", "and", "or", "not", "true", "false", "div", "mod",
                "type", "class", "record", "object", "interface", "try", "except",
                "finally", "array"}
    for m in TOKEN_RE.finditer(text):
        s = m.group(0)
        if s.isspace():
            continue
        if s.startswith("//") or s.startswith("{"):
            continue
        if s.startswith("'"):
            tokens.append(("STR", s[1:-1]))
            continue
        if s[0].isdigit():
            tokens.append(("NUM", s))
            continue
        sl = s.lower()
        if sl in KEYWORDS:
            tokens.append(("KW", sl))
            continue
        if s and (s[0].isalpha() or s[0] == "_"):
            tokens.append(("ID", s))
            continue
        tokens.append(("PUNCT", s))
    return tokens


# ---------- Body extractor ----------

def _is_word_boundary(text: str, i: int, length: int) -> bool:
    n = len(text)
    left = (i == 0) or not (text[i-1].isalnum() or text[i-1] == "_")
    right = (i + length >= n) or not (text[i+length].isalnum() or text[i+length] == "_")
    return left and right


def extract_proc_body(text: str, name: str) -> str:
    """Extract text inside `procedure <name>(...) begin ... end;` (matching begin/end).

    Pascal `case` and `record` also use `end` without matching `begin`. We track them
    as open blocks too (they're opened by case/record and closed by end).
    """
    m = re.search(rf"procedure\s+{re.escape(name)}\b[^;]*?;", text)
    if not m:
        raise ValueError(f"procedure {name!r} not found")
    start = text.find("begin", m.end())
    if start == -1:
        raise ValueError(f"begin not found after procedure {name}")
    depth = 0
    i = start
    n = len(text)
    inside_string = False
    # Patterns that open a block closed by `end`:
    OPENERS = (("begin", 5), ("case", 4), ("record", 6), ("try", 3),
               ("class", 5), ("object", 6), ("interface", 9))
    while i < n:
        if inside_string:
            if text[i] == "'":
                inside_string = False
            i += 1
            continue
        if text[i] == "'":
            inside_string = True
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
        for kw, klen in OPENERS:
            if text[i:i+klen] == kw and _is_word_boundary(text, i, klen):
                depth += 1
                i += klen
                matched = True
                break
        if matched:
            continue
        if text[i:i+3] == "end" and _is_word_boundary(text, i, 3):
            depth -= 1
            i += 3
            if depth == 0:
                return text[start:i]
            continue
        i += 1
    raise ValueError(f"unterminated procedure {name}")


# ---------- Recursive-descent parser ----------

@dataclass
class Node:
    kind: str           # 'block' | 'if' | 'call' | 'opaque' | 'case' | 'for'
    children: list["Node"] = field(default_factory=list)
    cond: str | None = None     # for 'if' (Python-evaluable, with nation flag names)
    name: str | None = None     # for 'call'
    args: list[str] | None = None  # for 'call' (string literals as raw text)
    else_block: "Node | None" = None  # for 'if'


class Parser:
    def __init__(self, tokens: list[tuple[str, str]]):
        self.tokens = tokens
        self.pos = 0

    def peek(self, off: int = 0) -> tuple[str, str] | None:
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

    def expect(self, kind: str, text: str | None = None):
        t = self.consume()
        if t[0] != kind or (text is not None and t[1] != text):
            raise SyntaxError(f"expected {kind!r}/{text!r}, got {t!r} at pos {self.pos}")
        return t

    def parse_block(self) -> Node:
        """Parse until 'end' (consumes 'end' but not the trailing ';' or '.')."""
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
                # Defensive: parse_stmt didn't consume anything; force advance.
                self.pos += 1
        return node

    def parse_stmt(self) -> Node | None:
        t = self.peek()
        if t is None:
            return None
        # Skip stray semicolons
        if t[0] == "PUNCT" and t[1] == ";":
            self.consume()
            return None
        if t[0] == "KW":
            kw = t[1]
            if kw == "begin":
                self.consume()
                return self.parse_block()  # consumes matching end
            if kw == "if":
                return self.parse_if()
            if kw == "case":
                return self.parse_case()
            if kw in ("for", "while"):
                return self.parse_loop()
            if kw == "with":
                return self.parse_with()
            if kw in ("var", "const"):
                # skip declaration until ';'
                self.skip_to_semicolon()
                return None
            if kw == "else":
                # shouldn't happen at top-level
                return None
            if kw == "end":
                # caller handles
                return None
        if t[0] == "ID":
            return self.parse_call_or_assign()
        if t[0] == "PUNCT":
            self.consume()
            return None
        # default: skip
        self.consume()
        return None

    def parse_if(self) -> Node:
        self.expect("KW", "if")
        cond = self.parse_expr_until(("KW", "then"))
        self.expect("KW", "then")
        body = self.parse_stmt_or_block()
        else_block: Node | None = None
        # Allow optional ';' between then-body and else
        if self.peek() == ("PUNCT", ";"):
            # don't consume yet; check for else
            if self.peek(1) == ("KW", "else"):
                self.consume()
        if self.at_kw("else"):
            self.consume()
            else_block = self.parse_stmt_or_block()
        return Node(kind="if", cond=cond, children=[body], else_block=else_block)

    def parse_stmt_or_block(self) -> Node:
        if self.at_kw("begin"):
            self.consume()
            return self.parse_block()
        node = self.parse_stmt()
        return node if node is not None else Node(kind="opaque")

    def parse_case(self) -> Node:
        # We don't need to evaluate cases for nation rostering; opaque-skip.
        # But we need to skip matching 'end'.
        depth = 0
        # 'case' already at peek
        self.consume()  # case
        # Walk until matching 'end'
        while self.pos < len(self.tokens):
            t = self.consume()
            if t[0] == "KW" and t[1] in ("begin", "case"):
                depth += 1
            elif t[0] == "KW" and t[1] == "end":
                if depth == 0:
                    break
                depth -= 1
        return Node(kind="opaque")

    def parse_loop(self) -> Node:
        # for/while ... do <stmt-or-block>
        self.consume()  # consume 'for' or 'while'
        # Skip until 'do'
        while self.pos < len(self.tokens):
            t = self.consume()
            if t[0] == "KW" and t[1] == "do":
                break
        body = self.parse_stmt_or_block()
        return Node(kind="loop", children=[body])

    def parse_with(self) -> Node:
        self.consume()  # 'with'
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

    def parse_expr_until(self, stop: tuple[str, str]) -> str:
        """Collect tokens until stop into a Python-evaluable boolean expression."""
        parts: list[str] = []
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
                # Translate Pascal boolean ops to Python
                kw = t[1]
                if kw == "and":
                    parts.append(" and ")
                elif kw == "or":
                    parts.append(" or ")
                elif kw == "not":
                    parts.append(" not ")
                elif kw in ("true", "false"):
                    parts.append("True" if kw == "true" else "False")
                else:
                    parts.append(" " + kw + " ")
            elif t[0] == "ID":
                parts.append(t[1])
            elif t[0] == "NUM":
                parts.append(t[1])
            elif t[0] == "STR":
                # Shouldn't normally appear in nation conditions
                parts.append(repr(t[1]))
        return "".join(parts).strip()

    def parse_call_or_assign(self) -> Node:
        ident_tok = self.consume()
        ident = ident_tok[1]
        # Lookahead: '(' = call, otherwise it's an assignment / member access
        if self.peek() == ("PUNCT", "("):
            self.consume()
            args = self.parse_args()
            # consume ';'
            self.consume_semicolon_if_present()
            return Node(kind="call", name=ident, args=args)
        # member access or assignment — skip until ';'
        depth = 0
        while self.pos < len(self.tokens):
            t = self.consume()
            if t[0] == "PUNCT":
                if t[1] == "(":
                    depth += 1
                elif t[1] == ")":
                    depth -= 1
                elif t[1] == ";" and depth == 0:
                    return Node(kind="opaque")
        return Node(kind="opaque")

    def parse_args(self) -> list[str]:
        """Parse a comma-separated argument list, then expect ')'."""
        args: list[str] = []
        cur: list[str] = []
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

    def consume_semicolon_if_present(self):
        if self.peek() == ("PUNCT", ";"):
            self.consume()


# ---------- Evaluator ----------

ALL_NATIONS = ["aus", "fra", "eng", "spa", "rus", "ukr", "pol", "swe", "pru",
               "ven", "tur", "alg", "mis", "net", "den", "por", "pie", "sax",
               "bav", "hun", "swi", "sco", "tat", "lit"]


def make_env(active: str) -> dict[str, bool | int]:
    env: dict[str, bool | int] = {n: (n == active) for n in ALL_NATIONS}
    # Common conveniences
    env["bAddIfNotExist"] = True
    env["bEarlyBird"] = True
    env["True"] = True
    env["False"] = False
    return env


def safe_eval(expr: str, env: dict) -> Any:
    expr = expr.strip()
    if not expr:
        return True
    try:
        return eval(expr, {"__builtins__": {}}, env)
    except Exception:
        # Conservative: assume reachable rather than dropping
        return True


def walk(node: Node, env: dict, sink: list, path_cond: list[str]):
    """Walk AST collecting AddMember/AddUpgrade* calls, gated by guards."""
    if node.kind == "block" or node.kind == "loop" or node.kind == "with":
        for c in node.children:
            walk(c, env, sink, path_cond)
    elif node.kind == "if":
        cond_val = safe_eval(node.cond or "True", env)
        if cond_val:
            walk(node.children[0], env, sink, path_cond + [node.cond or ""])
        elif node.else_block is not None:
            walk(node.else_block, env, sink, path_cond + ["not(" + (node.cond or "") + ")"])
    elif node.kind == "call":
        if node.name and node.name.startswith("_country_"):
            sink.append((node.name, node.args, list(path_cond)))
    elif node.kind == "opaque":
        pass


CALL_TO_INLINE_RE = re.compile(r"_country_InitUnitsUpgrades\s*\([^)]*\)\s*;")


def _inline_subprocs(text: str, body: str) -> str:
    """Replace `_country_InitUnitsUpgrades(...)` call inside body with that proc's body."""
    try:
        sub_body = extract_proc_body(text, "_country_InitUnitsUpgrades")
    except ValueError:
        return body
    # Strip leading 'begin' and trailing 'end' keywords
    sub_body = re.sub(r"^\s*begin\b", "", sub_body)
    sub_body = re.sub(r"\bend\s*$", "", sub_body)
    return CALL_TO_INLINE_RE.sub(lambda m: sub_body, body)


def _commonname_for(nat: str) -> str:
    if nat in ("rus", "ukr"):
        return "rus"
    if nat in ("tur", "alg"):
        return "tur"
    return "eur"


def _commonname_storehouse(nat: str) -> str:
    # Pol uses Russian storehouse; spa/por use Spanish; else common+'sto'
    if nat == "pol":
        return "russto"
    if nat in ("spa", "por"):
        return "spasto"
    return _commonname_for(nat) + "sto"


def _commonname_market(nat: str) -> str:
    if nat in ("spa", "por"):
        return "spamar"
    return _commonname_for(nat) + "mar"


def _commonname_port(nat: str) -> str:
    if nat == "por":
        return "porpor"
    if nat == "ukr":
        return "ukrpor"
    return _commonname_for(nat) + "por"


def _presubstitute(body: str, nat: str) -> str:
    """Pre-replace csid, commonName* and other per-nation string vars with literals."""
    nat_lit = f"'{nat}'"
    com_lit = f"'{_commonname_for(nat)}'"
    out = re.sub(r"\bcsid\b", nat_lit, body)
    # commonName2 (some places) treated same as commonName
    out = re.sub(r"\bcommonName2\b", com_lit, out)
    # Conditional storehouse/market/port — replace BEFORE commonName so we don't double-replace
    out = re.sub(r"\bcommonNameStorehouse\b", f"'{_commonname_storehouse(nat)}'", out)
    out = re.sub(r"\bcommonNameMarket\b", f"'{_commonname_market(nat)}'", out)
    out = re.sub(r"\bcommonNamePort\b", f"'{_commonname_port(nat)}'", out)
    out = re.sub(r"\bcommonName\b", com_lit, out)
    # blacksmith/academy/century18 are derived from csid in _country_InitUnitsUpgrades
    out = re.sub(r"\bblacksmith\b", f"'{nat}bla'", out)
    out = re.sub(r"\bacademy\b", f"'{nat}aca'", out)
    out = re.sub(r"\bcentury18\b", f"'{nat}cen.1'", out)
    out = re.sub(r"\benablefrigate\b", f"'{nat}aca.6'", out)
    out = re.sub(r"\benablebattleship\b", f"'{nat}aca.29'", out)
    out = re.sub(r"\benablemulticannon\b", f"'{nat}aca.19'", out)
    return out


def parse_country(path: Path) -> dict:
    """Parse country.script returning a per-nation AST dict.
    Returns {nat: AST root} so that subsequent walks evaluate guards per nation.
    """
    text = path.read_text(encoding="utf-8", errors="replace")
    body = extract_proc_body(text, "_country_Init")
    body = _inline_subprocs(text, body)
    asts: dict[str, Node] = {}
    for nat in ALL_NATIONS:
        body_nat = _presubstitute(body, nat)
        tokens = tokenize(body_nat)
        # Strip outer begin/end if they wrap everything
        if tokens and tokens[0] == ("KW", "begin"):
            tokens = tokens[1:]
        parser = Parser(tokens)
        root = parser.parse_block()
        asts[nat] = root
    return {"asts": asts, "raw_body": body}


def _resolve_string_arg(raw: str) -> str:
    """Resolve string-concat expressions like 'aus'+'cen.1' into 'auscen.1'.
    Returns '' if not a pure string expression.
    """
    s = raw.strip()
    # If already a quoted literal
    if (s.startswith("'") and s.endswith("'") and "+" not in s):
        return s[1:-1]
    if (s.startswith('"') and s.endswith('"') and "+" not in s):
        return s[1:-1]
    # Try to evaluate via Python
    # Translate Pascal '+' string concat (already same in Python). Allow IntToStr(n) -> str(n).
    py = re.sub(r"\bIntToStr\(([^)]+)\)", r"str(\1)", s)
    # Strip Pascal-style boolean/identifier safety: strip surrounding parens
    try:
        v = eval(py, {"__builtins__": {"str": str}}, {})
        if isinstance(v, str):
            return v
    except Exception:
        pass
    return s  # return raw on failure for debugging


def collect_for_nation(root: Node, nat: str) -> dict:
    env = make_env(nat)
    sink: list = []
    walk(root, env, sink, [])
    members: list[tuple[str, dict]] = []
    upgrades: list[tuple[str, dict]] = []
    fixed_produces: list[tuple[str, dict]] = []
    access_controls: list[tuple[str, dict]] = []
    other: list[tuple[str, list]] = []
    for name, args, path_cond in sink:
        if not args:
            continue
        if name == "_country_AddMember":
            # signature: (country, sid, ind, enabled, category, priority, airole)
            sid = _resolve_string_arg(args[1]) if len(args) > 1 else ""
            members.append((sid, {
                "enabled_arg": args[3] if len(args) > 3 else "",
                "category": args[4] if len(args) > 4 else "",
                "priority": args[5] if len(args) > 5 else "",
                "airole": args[6] if len(args) > 6 else "",
                "guards": path_cond,
            }))
        elif name in ("_country_AddUpgrade", "_country_AddUpgradeWithAccessControl"):
            # _country_AddUpgrade(country, upgid, level, tooltiptype, itype, value, enabled, time, x, y, ind,
            #                     food, wood, stone, gold, iron, coal, bAddIfNotExist, iarr1p0..p2, sarr2p0..p9)
            upgrades.append((_resolve_string_arg(args[1]) if len(args) > 1 else "", {
                "level": args[2] if len(args) > 2 else "",
                "tooltiptype": args[3] if len(args) > 3 else "",
                "itype": args[4] if len(args) > 4 else "",
                "value": args[5] if len(args) > 5 else "",
                "enabled": args[6] if len(args) > 6 else "",
                "time": args[7] if len(args) > 7 else "",
                "food":  args[11] if len(args) > 11 else "",
                "wood":  args[12] if len(args) > 12 else "",
                "stone": args[13] if len(args) > 13 else "",
                "gold":  args[14] if len(args) > 14 else "",
                "iron":  args[15] if len(args) > 15 else "",
                "coal":  args[16] if len(args) > 16 else "",
                "iarr1": [args[i] for i in (18, 19, 20) if i < len(args)],
                "sarr2": [strip_quotes(args[i]) for i in range(21, min(31, len(args)))],
                "name_signature": name,
                "guards": path_cond,
                "raw_args": args,
            }))
        elif name == "_country_AddFixedProduce" or name == "_country_AddFixedProduceWithAccessControl":
            fixed_produces.append((strip_quotes(args[2]) if len(args) > 2 else "", {
                "produced_by": strip_quotes(args[2]) if len(args) > 2 else "",
                "produces": strip_quotes(args[3]) if len(args) > 3 else "",
                "guards": path_cond,
            }))
        elif name == "_country_AddAccessControl":
            access_controls.append((strip_quotes(args[2]) if len(args) > 2 else "", {
                "guards": path_cond,
            }))
        else:
            other.append((name, args))
    return {
        "members": members,
        "upgrades": upgrades,
        "fixed_produces": fixed_produces,
        "access_controls": access_controls,
        "other": other,
    }


def strip_quotes(s: str) -> str:
    s = s.strip()
    if s.startswith("'") and s.endswith("'"):
        return s[1:-1]
    if s.startswith('"') and s.endswith('"'):
        return s[1:-1]
    # repr-form
    if (s.startswith('"') or s.startswith("'")) and "\\" not in s:
        return s[1:-1]
    if s and s[0] in "\"'" and s[-1] in "\"'":
        return s[1:-1]
    return s


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    from config import COUNTRY_SCRIPT, PLAYABLE_NATIONS
    parsed = parse_country(COUNTRY_SCRIPT)
    asts = parsed["asts"]
    print(f"Parsed per-nation ASTs: {len(asts)}")
    # Test playable nations
    for nat in ["aus", "rus", "ukr", "tur", "sco", "spa"]:
        info = collect_for_nation(asts[nat], nat)
        sids_unique = sorted(set(sid for sid, _ in info["members"] if sid and not sid.startswith("'") and "+" not in sid))
        upg_unique = sorted(set(uid for uid, _ in info["upgrades"] if uid))
        print(f"  {nat}: {len(sids_unique)} unique members, {len(upg_unique)} unique upgrades, "
              f"{len(info['fixed_produces'])} fixed_produces")
        # Show a few sids that look like buildings (3-letter suffix on nat)
        nat_sids = [s for s in sids_unique if s.startswith(nat) and len(s) == len(nat) + 3]
        print(f"     {nat}-prefixed buildings ({len(nat_sids)}): {nat_sids}")
        # Common buildings (start with eur/rus/tur/spa/ukr/por and 3-letter suffix)
        com = _commonname_for(nat)
        com_sids = [s for s in sids_unique if s.startswith(com) and len(s) == len(com) + 3]
        print(f"     {com}-prefixed buildings ({len(com_sids)}): {com_sids}")
        # Sample upgrades
        print(f"     sample upgrades: {upg_unique[:6]}")
