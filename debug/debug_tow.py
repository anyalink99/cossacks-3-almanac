import sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "parser"))
from config import UNIT_SCRIPT
from parse_units import (extract_proc_body, find_top_cases,
                         split_case_branches, parse_label_commonsid_suffixes,
                         remove_top_level_ifs, remove_nested_cases,
                         parse_top_level_ifs, parse_branch_body)

text = UNIT_SCRIPT.read_text(encoding="utf-8", errors="replace")
body = extract_proc_body(text, "_unit_InitBase")
cases = find_top_cases(body)

# Find common buildings case
for (cstart, of_end, end_pos, _) in cases:
    head = body[cstart:of_end]
    if "objprop.sid" not in head:
        continue
    inner = body[of_end:end_pos - 3].lstrip()
    while inner.startswith("//") or inner.startswith("{"):
        if inner.startswith("//"):
            nl = inner.find("\n")
            inner = inner[nl + 1:].lstrip() if nl != -1 else ""
        else:
            cl = inner.find("}")
            inner = inner[cl + 1:].lstrip() if cl != -1 else ""
    if inner.startswith("commonsid"):
        cb_text = body[of_end:end_pos - 3]
        for label, body_text in split_case_branches(cb_text):
            if label == "else":
                continue
            sufs = parse_label_commonsid_suffixes(label)
            if "tow" in sufs:
                print("=== tow branch body ===")
                print(body_text[:2500])
                print("=== end ===\n")

                cleaned = remove_nested_cases(body_text)
                print("=== after remove_nested_cases (last 1500 chars) ===")
                print(cleaned[-1500:])
                print()

                cleaned2 = remove_top_level_ifs(cleaned)
                print("=== after remove_top_level_ifs (last 1500 chars) ===")
                print(cleaned2[-1500:])
                print()

                ifs = parse_top_level_ifs(body_text)
                print(f"=== top-level ifs found: {len(ifs)} ===")
                for cond, body_if in ifs:
                    print(f"  cond={cond!r}")
                    print(f"  body[:200]={body_if[:200]!r}")
        break
