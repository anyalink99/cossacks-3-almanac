import sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "parser"))
from config import COUNTRY_SCRIPT
from simulate_upgrades import (extract_proc_body, _presubstitute, tokenize, SimParser,
                               make_env, walk_sim)
from parse_country import Node

text = COUNTRY_SCRIPT.read_text(encoding="utf-8", errors="replace")
body = extract_proc_body(text, "_country_InitUnitsUpgrades")
print(f"Body length: {len(body)}")
body2 = _presubstitute(body, "rus")
print(f"After presubstitute: {len(body2)}")
tokens = tokenize(body2)
print(f"Tokens: {len(tokens)}")
print(f"First 5 tokens: {tokens[:5]}")
if tokens and tokens[0] == ("KW", "begin"):
    tokens = tokens[1:]
parser = SimParser(tokens)
root = parser.parse_block()
print(f"Root children: {len(root.children)}")
print(f"Parser pos: {parser.pos}/{len(tokens)}")

# Run the simulator on rus and dump rusbar.pikemanrus.1.1 entries
from simulate_upgrades import simulate
print("\n=== Tracing rusbar.pikemanrus.* ===")
upgrades = simulate(text, "rus")
matched = [u for u in upgrades if "rusbar.pikemanrus" in u["sid"]]
print(f"Found {len(matched)} entries:")
for i, u in enumerate(matched):
    print(f"  [{i}] sid={u['sid']} val={u['value']} F{u['food']}/G{u['gold']} src={u['_source']}")

# Recursively count node kinds
from collections import Counter
def count_kinds(node, c):
    c[node.kind] += 1
    for ch in node.children:
        count_kinds(ch, c)
    if node.else_block:
        count_kinds(node.else_block, c)
c = Counter()
count_kinds(root, c)
print(f"Node kinds: {dict(c)}")

# Find all call names
def find_calls(node, names):
    if node.kind == "call":
        names.append(node.name)
    for ch in node.children:
        find_calls(ch, names)
    if node.else_block:
        find_calls(node.else_block, names)
calls = []
find_calls(root, calls)
call_counter = Counter(calls)
print(f"Top calls:")
for name, cnt in call_counter.most_common(20):
    print(f"  {name}: {cnt}")
