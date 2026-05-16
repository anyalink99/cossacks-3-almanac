// Pyodide worker — keeps the heavy replay-parse off the main thread.
// Receives postMessage({ id, bytes }), returns
// postMessage({ id, ok: true, result }) or { id, ok: false, error }.

importScripts("https://cdn.jsdelivr.net/pyodide/v0.26.4/full/pyodide.js");

let pyodide = null;
let ready = false;

async function loadFile(url, target) {
  const r = await fetch(url);
  if (!r.ok) throw new Error(`HTTP ${r.status} for ${url}`);
  const text = await r.text();
  const dir = target.substring(0, target.lastIndexOf("/"));
  try { pyodide.FS.mkdirTree(dir); } catch (e) {}
  pyodide.FS.writeFile(target, text);
}

async function boot() {
  postMessage({ kind: "progress", text: "Загрузка Pyodide…" });
  pyodide = await loadPyodide({
    indexURL: "https://cdn.jsdelivr.net/pyodide/v0.26.4/full/",
  });
  postMessage({ kind: "progress", text: "Загрузка парсера…" });
  pyodide.FS.mkdirTree("/c3");
  // Worker URL is replay-parser/js/worker.js, so "../../" climbs to repo root.
  await loadFile("../../parser/parse_replay.py",        "/c3/parse_replay.py");
  await loadFile("../../parser/parse_replay_events.py", "/c3/parse_replay_events.py");
  await loadFile("../../data.json",                     "/c3/data.json");
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
  postMessage({ kind: "ready" });
}

const bootPromise = boot().catch((e) => {
  postMessage({ kind: "error", text: String(e?.message || e) });
  throw e;
});

self.onmessage = async (ev) => {
  const { id, bytes } = ev.data || {};
  try {
    await bootPromise;
    pyodide.FS.writeFile("/c3/_current.rep", bytes);
    const resultJson = pyodide.runPython(`
import json
import parse_replay_events
with open("/c3/_current.rep", "rb") as f:
    data = f.read()
result = parse_replay_events.parse_replay_from_bytes(data)
json.dumps(result, ensure_ascii=False, default=str)
`);
    postMessage({ id, ok: true, result: JSON.parse(resultJson) });
  } catch (e) {
    postMessage({ id, ok: false, error: String(e?.message || e) });
  }
};
