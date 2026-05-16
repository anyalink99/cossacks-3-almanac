// Bootstraps Pyodide, mounts the replay-parser Python modules into its
// virtual filesystem and exposes a single `parseReplay(bytes)` entry-point.

let pyodide = null;
let ready = false;

const FILES = [
  { url: "../parser/parse_replay.py",        target: "/c3/parse_replay.py" },
  { url: "../parser/parse_replay_events.py", target: "/c3/parse_replay_events.py" },
  { url: "../data.json",                     target: "/c3/data.json" },
  { url: "../derived/pattern_inventory.json", target: "/c3/output/derived/pattern_inventory.json", optional: true },
  { url: "../derived/pattern_types.json",     target: "/c3/output/derived/pattern_types.json", optional: true },
];

export async function initPyodide(onProgress = () => {}) {
  if (ready) return pyodide;
  onProgress("Загрузка Pyodide…", "loading");
  pyodide = await window.loadPyodide({
    indexURL: "https://cdn.jsdelivr.net/pyodide/v0.26.4/full/",
  });

  onProgress("Загрузка парсера…", "loading");
  pyodide.FS.mkdirTree("/c3");
  pyodide.FS.mkdirTree("/c3/output/derived");

  for (const f of FILES) {
    try {
      const src = await fetch(f.url).then(r => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.text();
      });
      // Make the directory before writing
      const dir = f.target.substring(0, f.target.lastIndexOf("/"));
      try { pyodide.FS.mkdirTree(dir); } catch (e) {}
      pyodide.FS.writeFile(f.target, src);
    } catch (e) {
      if (!f.optional) throw e;
      // Optional files (pattern data) — ignore if missing
    }
  }

  pyodide.runPython(`
import sys
sys.path.insert(0, "/c3")
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import parse_replay
import parse_replay_events
`);

  ready = true;
  onProgress("Готов — загрузите .rep", "ready");
  return pyodide;
}

export async function parseReplay(bytes) {
  if (!ready) throw new Error("Pyodide ещё не загрузился");
  pyodide.FS.writeFile("/c3/_current.rep", bytes);
  const resultJson = pyodide.runPython(`
import json
import parse_replay_events
with open("/c3/_current.rep", "rb") as f:
    data = f.read()
result = parse_replay_events.parse_replay_from_bytes(data)
json.dumps(result, ensure_ascii=False, default=str)
`);
  return JSON.parse(resultJson);
}
