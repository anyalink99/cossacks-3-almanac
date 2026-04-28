"""Quick timing harness for parse_country."""
import sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
print("starting", flush=True)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "parser"))
from config import COUNTRY_SCRIPT
from parse_country import (extract_proc_body, _inline_subprocs, _presubstitute,
                           tokenize, Parser, walk, make_env)

t0 = time.time()
text = COUNTRY_SCRIPT.read_text(encoding="utf-8", errors="replace")
print(f"[{time.time()-t0:.2f}s] Read {len(text)} chars")

t0 = time.time()
body = extract_proc_body(text, "_country_Init")
print(f"[{time.time()-t0:.2f}s] extract_proc_body _country_Init -> {len(body)} chars")

t0 = time.time()
body2 = _inline_subprocs(text, body)
print(f"[{time.time()-t0:.2f}s] inline subprocs -> {len(body2)} chars")

t0 = time.time()
body_aus = _presubstitute(body2, "aus")
print(f"[{time.time()-t0:.2f}s] presubstitute aus -> {len(body_aus)} chars")

t0 = time.time()
tokens = tokenize(body_aus)
print(f"[{time.time()-t0:.2f}s] tokenize -> {len(tokens)} tokens")

import re
m = re.search(r"_country_InitUnitsUpgrades", body)
print(f"InitUnitsUpgrades call in body: at char {m.start() if m else 'NOT FOUND'}", flush=True)
m = re.search(r"_country_InitUnitsUpgrades\s*\([^)]*\)\s*;", body)
print(f"With regex: {m.group(0) if m else 'NO MATCH'}", flush=True)

t0 = time.time()
if tokens and tokens[0] == ("KW", "begin"):
    tokens = tokens[1:]
parser = Parser(tokens)
print(f"[{time.time()-t0:.2f}s] starting parse, {len(tokens)} tokens", flush=True)

# Add infinite-loop watchdog
last_pos = -1
import threading
done = [False]
def watchdog():
    import time
    while not done[0]:
        time.sleep(2)
        if not done[0]:
            print(f"  watchdog: pos={parser.pos}/{len(tokens)} stack-trace pending", flush=True)
t = threading.Thread(target=watchdog, daemon=True)
t.start()

root = parser.parse_block()
done[0] = True
print(f"[{time.time()-t0:.2f}s] parse -> root has {len(root.children)} children, parser.pos={parser.pos}/{len(tokens)}", flush=True)
