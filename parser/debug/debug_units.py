import sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import UNIT_SCRIPT
from parse_units import (extract_proc_body, find_top_cases,
                         split_case_branches, parse_label_sids,
                         parse_label_commonsid_suffixes, parse_label_csid_suffixes)

text = UNIT_SCRIPT.read_text(encoding="utf-8", errors="replace")
body = extract_proc_body(text, "_unit_InitBase")
print(f"Body length: {len(body)}")
cases = find_top_cases(body)
print(f"Found {len(cases)} top-level case statements")
for n, (cstart, of_end, end_pos, depth) in enumerate(cases[:15]):
    head = body[cstart:of_end].replace("\n", " ").strip()[:80]
    inner = body[of_end:of_end + 80].lstrip().replace("\n", " ")[:80]
    print(f"  case#{n} depth={depth} head={head!r}")
    print(f"     inner-start: {inner!r}")
print()

# Show ALL objprop.sid cases with sizes
print("All objprop.sid cases:")
for n, (cstart, of_end, end_pos, _) in enumerate(cases):
    head = body[cstart:of_end]
    inner = body[of_end:end_pos - 3]
    inner_stripped = inner.lstrip()
    # strip leading comments
    while inner_stripped.startswith("//") or inner_stripped.startswith("{"):
        if inner_stripped.startswith("//"):
            nl = inner_stripped.find("\n")
            if nl < 0:
                break
            inner_stripped = inner_stripped[nl + 1:].lstrip()
        else:
            cl = inner_stripped.find("}")
            if cl < 0:
                break
            inner_stripped = inner_stripped[cl + 1:].lstrip()
    if "objprop.sid" in head:
        first_label_end = inner_stripped.find(":")
        first_label = inner_stripped[:first_label_end].strip() if first_label_end > 0 else inner_stripped[:60]
        print(f"  case#{n} cstart={cstart} of_end={of_end} end_pos={end_pos} size={end_pos - cstart} first_label={first_label[:60]!r}")

# Pick the LARGEST objprop.sid case starting with literal sid
unit_cands = []
for n, (cstart, of_end, end_pos, _) in enumerate(cases):
    head = body[cstart:of_end]
    inner = body[of_end:end_pos - 3]
    inner_stripped = inner.lstrip()
    while inner_stripped.startswith("//") or inner_stripped.startswith("{"):
        if inner_stripped.startswith("//"):
            nl = inner_stripped.find("\n")
            if nl < 0: break
            inner_stripped = inner_stripped[nl + 1:].lstrip()
        else:
            cl = inner_stripped.find("}")
            if cl < 0: break
            inner_stripped = inner_stripped[cl + 1:].lstrip()
    if "objprop.sid" in head and inner_stripped.startswith("'"):
        unit_cands.append((end_pos - cstart, of_end, end_pos))

unit_cands.sort(reverse=True)
if unit_cands:
    sz, of_end, end_pos = unit_cands[0]
    unit_case_inner = body[of_end:end_pos - 3]
    print(f"\nLargest unit-style case: {sz} chars")
    branches = split_case_branches(unit_case_inner)
    print(f"  -> {len(branches)} branches")
    for label, body_text in branches[:6]:
        sids = parse_label_sids(label)
        print(f"     label_first={label[:80]!r}  sids={sids[:4]}")
print()

# Check the nation building case
for (cstart, of_end, end_pos, _) in cases:
    head = body[cstart:of_end]
    inner = body[of_end:end_pos - 3].lstrip()
    if "objprop.sid" in head and inner.startswith("csid"):
        nation_case_inner = body[of_end:end_pos - 3]
        print(f"Nation building case: {len(nation_case_inner)} chars")
        branches = split_case_branches(nation_case_inner)
        print(f"  -> {len(branches)} branches")
        for label, body_text in branches[:8]:
            sufs = parse_label_csid_suffixes(label)
            print(f"     label={label[:80]!r}  suffixes={sufs}")
        break
