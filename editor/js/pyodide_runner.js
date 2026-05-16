// Bootstraps Pyodide and exposes:
//   - runSimulation(buildOrder, data, tree, slots)
//   - importReplay(bytes, pid?, windowGsec?) → build_order dict
// Lives at repo-root/editor/js/, so simulator/, parser/, derived/, data.json
// all sit two levels up.

let pyodide = null;
let ready = false;

const FILES_TO_LOAD = {
  "../simulator/simulate_economy.py":    "/c3/simulate_economy.py",
  "../parser/config.py":                 "/c3/config.py",
  "../parser/parse_replay.py":           "/c3/parse_replay.py",
  "../parser/parse_replay_events.py":    "/c3/parse_replay_events.py",
  "../parser/replay_to_build_order.py":  "/c3/replay_to_build_order.py",
  "../data.json":                        "/c3/data.json",
  "../derived/country_members.json":     "/c3/country_members.json",
};

export async function initPyodide(onProgress = (s, cls) => {}) {
  if (pyodide && ready) return pyodide;
  onProgress("Загрузка Pyodide…", "loading");
  pyodide = await window.loadPyodide({
    indexURL: "https://cdn.jsdelivr.net/pyodide/v0.26.4/full/",
  });
  onProgress("Загрузка симулятора и парсера…", "loading");
  pyodide.FS.mkdirTree("/c3");
  const loaded = await Promise.all(
    Object.entries(FILES_TO_LOAD).map(async ([url, target]) => {
      const r = await fetch(url);
      if (!r.ok) throw new Error(`HTTP ${r.status} for ${url}`);
      // data.json + country_members.json are JSON, others are .py source. fetch
      // .text() works for both — they're plain UTF-8.
      return [target, await r.text()];
    })
  );
  for (const [target, text] of loaded) {
    pyodide.FS.writeFile(target, text);
  }
  pyodide.runPython(`
import sys
sys.path.insert(0, "/c3")
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import simulate_economy
`);
  ready = true;
  onProgress("Готов", "ready");
  return pyodide;
}

export async function runSimulation(buildOrder, data, tree, slots) {
  if (!ready) throw new Error("Pyodide ещё грузится");
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

/**
 * Parse a .rep file and return a build_order dict.
 * @param {Uint8Array} bytes - raw replay bytes
 * @param {number|null} pid  - which player's actions to extract (null = autopick by build count)
 * @param {number} windowGsec - time window in game-seconds (default 900 = 15 g-min)
 */
export async function importReplay(bytes, pid = null, windowGsec = 900) {
  if (!ready) throw new Error("Pyodide ещё грузится");
  pyodide.FS.writeFile("/c3/_current.rep", bytes);
  pyodide.globals.set("__pid", pid === null ? -1 : pid);  // -1 sentinel
  pyodide.globals.set("__window", windowGsec);
  const resultJson = pyodide.runPython(`
import json
import replay_to_build_order as r2bo
with open("/c3/_current.rep", "rb") as f:
    rep_bytes = f.read()
with open("/c3/data.json", encoding="utf-8") as f:
    data = json.load(f)
pid_arg = None if __pid < 0 else int(__pid)
bo = r2bo.replay_to_build_order(rep_bytes, data, pid=pid_arg, window_g_sec=float(__window))
json.dumps(bo, ensure_ascii=False)
`);
  return JSON.parse(resultJson);
}

/**
 * List players in a replay so the user can pick one.
 * @returns {Array<{pid: number, name: string, nation: string, n_builds: number}>}
 */
export async function listReplayPlayers(bytes) {
  if (!ready) throw new Error("Pyodide ещё грузится");
  pyodide.FS.writeFile("/c3/_current.rep", bytes);
  const json_str = pyodide.runPython(`
import json
from parse_replay_events import parse_replay_from_bytes
with open("/c3/_current.rep", "rb") as f:
    data = f.read()
result = parse_replay_from_bytes(data)
players = []
for p in result.get("players", []):
    pid = p.get("pid")
    builds = result.get("builds_per_pid", {}).get(pid, [])
    nation = builds[0]["sid"][:3] if builds else "?"
    players.append({"pid": pid, "name": p.get("name", ""),
                    "nation": nation, "n_builds": len(builds)})
json.dumps(players)
`);
  return JSON.parse(json_str);
}
