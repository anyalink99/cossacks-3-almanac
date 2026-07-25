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
  // Cache-bust query string forces fresh fetch after parser/catalog changes —
  // without it the browser pins the previous version forever.
  const v = `?v=${Date.now()}`;
  await Promise.all([
    loadFile("../../parser/parse_replay.py"               + v, "/c3/parse_replay.py"),
    loadFile("../../parser/parse_replay_events.py"        + v, "/c3/parse_replay_events.py"),
    loadFile("../../derived/replay_upgrades.json"         + v, "/c3/replay_upgrades.json"),
    loadFile("../../derived/country_members.json"         + v, "/c3/country_members.json"),
  ]);
  pyodide.runPython(`
import sys
sys.path.insert(0, "/c3")
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import parse_replay
import parse_replay_events
parse_replay_events._load_upgrade_names()
parse_replay_events._load_country_members()
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
    // A Uint8Array becomes a Pyodide JsBuffer. Converting it directly to
    // Python bytes copies the replay once; writing to MEMFS and reading it
    // back copied large files twice.
    pyodide.globals.set("_replay_bytes_js", bytes);
    const resultJson = pyodide.runPython(`
import json
import parse_replay_events
data = _replay_bytes_js.to_bytes()
result = parse_replay_events.parse_replay_from_bytes(data)
json.dumps(result, ensure_ascii=False, default=str)
`);
    postMessage({ id, ok: true, result: JSON.parse(resultJson) });
  } catch (e) {
    postMessage({ id, ok: false, error: String(e?.message || e) });
  } finally {
    pyodide?.globals.delete("_replay_bytes_js");
  }
};
