// Bootstraps Pyodide and exposes runSimulation(buildOrder, data, tree, slots).
// Lives at repo-root/editor/js/, so simulator/ is two levels up.

let pyodide = null;
let simReady = false;

const SIM_PY_PATH = "../simulator/simulate_economy.py";
const CONFIG_PY_PATH = "../parser/config.py";

export async function initPyodide(onProgress = (s, cls) => {}) {
  if (pyodide && simReady) return pyodide;
  onProgress("Загрузка Pyodide…", "loading");
  pyodide = await window.loadPyodide({
    indexURL: "https://cdn.jsdelivr.net/pyodide/v0.26.4/full/",
  });
  onProgress("Загрузка симулятора…", "loading");
  const [simSrc, configSrc] = await Promise.all([
    fetch(SIM_PY_PATH).then(r => r.text()),
    fetch(CONFIG_PY_PATH).then(r => r.text()),
  ]);
  pyodide.FS.mkdirTree("/c3");
  pyodide.FS.writeFile("/c3/config.py", configSrc);
  pyodide.FS.writeFile("/c3/simulate_economy.py", simSrc);
  pyodide.runPython(`
import sys
sys.path.insert(0, "/c3")
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import simulate_economy
`);
  simReady = true;
  onProgress("Готов", "ready");
  return pyodide;
}

export async function runSimulation(buildOrder, data, tree, slots) {
  if (!simReady) throw new Error("Pyodide ещё грузится");
  pyodide.globals.set("__bo_json", JSON.stringify(buildOrder));
  pyodide.globals.set("__data_json", JSON.stringify(data));
  pyodide.globals.set("__tree_json", JSON.stringify(tree));
  pyodide.globals.set("__slots_json", JSON.stringify(slots));
  const resultJson = pyodide.runPython(`
import json
result = simulate_economy.simulate_in_memory(
    json.loads(__bo_json),
    json.loads(__data_json),
    json.loads(__tree_json),
    json.loads(__slots_json),
)
json.dumps(result, default=lambda o: list(o) if isinstance(o, set) else str(o))
`);
  return JSON.parse(resultJson);
}
