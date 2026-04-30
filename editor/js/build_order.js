import { COMMON_NAME, DEFAULT_PEASANT } from "./ui/i18n.js";

const LS_KEY = "c3_editor_build_order_v4";

export function defaultBuildOrder(nation = "bav") {
  const cen = nation + "cen";
  const pea = DEFAULT_PEASANT[nation] || ("pea" + nation);
  return {
    nation,
    game_speed: "fast",
    map_config: {},  // walk_overhead removed — sim uses its built-in default
    // Game defaults: 1000 each (resourcestart=0, "Стандарт") + 18 крестьян
    // (CreateStartPointPeasants:1255). 1 town hall — заявка для билд-ордера, в игре
    // здания не размещаются изначально (только peasants + storehouse via map gen).
    starting_resources: { food: 1000, wood: 1000, stone: 1000, gold: 1000, iron: 1000, coal: 1000 },
    starting_units: { [pea]: 18 },
    starting_buildings: { [cen]: 1 },
    max_time_sec: 900,  // 15 minutes (game-time)
    actions: [],
  };
}

export function load() {
  try {
    const raw = localStorage.getItem(LS_KEY);
    if (!raw) return defaultBuildOrder();
    return JSON.parse(raw);
  } catch (e) { return defaultBuildOrder(); }
}

export function save(bo) {
  try { localStorage.setItem(LS_KEY, JSON.stringify(bo)); } catch (e) {}
}

export function exportToFile(bo) {
  const blob = new Blob([JSON.stringify(bo, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `bo_${bo.nation}_${Date.now()}.json`;
  document.body.appendChild(a); a.click(); document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

export async function importFromFile(file) {
  return JSON.parse(await file.text());
}

export function rebaseToNation(bo, newNation) {
  const newPea = DEFAULT_PEASANT[newNation];
  const newCen = newNation + "cen";
  const su = {};
  for (const [k, v] of Object.entries(bo.starting_units || {})) {
    if (k.startsWith("pea")) su[newPea] = v;
    else su[k] = v;
  }
  if (!Object.keys(su).length) su[newPea] = 18;
  const sb = {};
  for (const [k, v] of Object.entries(bo.starting_buildings || {})) {
    if (k.endsWith("cen")) sb[newCen] = v;
    else sb[k] = v;
  }
  if (!Object.keys(sb).length) sb[newCen] = 1;
  bo.starting_units = su;
  bo.starting_buildings = sb;
  bo.nation = newNation;
  // Clear actions — they reference the old nation's sids and would all be invalid.
  bo.actions = [];
  return bo;
}
