// Catalog helpers — derive per-nation lists from data.json, with optional
// filtering by Timeline state at a given time T.

import { COMMON_NAME, fmtName } from "./i18n.js";

const NON_BUILDABLE = new Set(["ferry", "transport", "fishboat"]);

function _prereqsMet(prereqs, snapshot) {
  if (!prereqs || !prereqs.length) return true;
  for (const p of prereqs) {
    if (snapshot.buildings.has(p) && snapshot.buildings.get(p) > 0) continue;
    if (snapshot.upgrades.has(p)) continue;
    return false;
  }
  return true;
}

/**
 * All buildings the nation can construct (no time filter).
 */
export function buildingsForNation(data, nation) {
  const out = data.buildings.filter(b => {
    if (b.nation !== nation) return false;
    if (NON_BUILDABLE.has(b.sid)) return false;
    return true;
  });
  out.sort((a, b) => fmtName(a).localeCompare(fmtName(b), "ru"));
  return out;
}

/**
 * Buildings constructible at time T (their prereqs are met by then).
 * Returns array of {building, available, lockedBy} so caller can show greyed-out items.
 */
export function buildingsAt(data, nation, timeline, t) {
  const list = buildingsForNation(data, nation);
  const snap = timeline.snapshot(t);
  return list.map(b => ({
    building: b,
    available: _prereqsMet(b.prereqs, snap),
    prereqs: b.prereqs || [],
  }));
}

export function unitsForNation(data, nation) {
  return data.units.filter(u => u.nation === nation && u.trained_in && u.trained_in.length);
}

/**
 * Producer buildings for the nation that exist by time T.
 */
export function producersAt(data, nation, timeline, t) {
  const all = data.buildings.filter(b => b.nation === nation);
  const units = unitsForNation(data, nation);
  const producerSids = new Set();
  for (const u of units) for (const b of (u.trained_in || [])) producerSids.add(b);
  const snap = timeline.snapshot(t);
  const out = all.filter(b => producerSids.has(b.sid) && (snap.buildings.get(b.sid) || 0) > 0);
  out.sort((a, b) => fmtName(a).localeCompare(fmtName(b), "ru"));
  return out;
}

/**
 * Units producible in `building_sid` by time T (their prereqs met).
 */
export function unitsTrainedInAt(data, nation, building_sid, timeline, t) {
  const all = unitsForNation(data, nation).filter(u => (u.trained_in || []).includes(building_sid));
  const snap = timeline.snapshot(t);
  return all
    .filter(u => _prereqsMet(u.prereqs, snap))
    .sort((a, b) => fmtName(a).localeCompare(fmtName(b), "ru"));
}

/**
 * Upgrades with prereqs met at time T. Annotated with `__place_ru` for grouping.
 */
export function upgradesAt(data, nation, timeline, t) {
  const cluster = COMMON_NAME[nation] || "eur";
  const out = data.upgrades.filter(u => {
    if (u.nation !== nation) return false;
    if (!u.sid || u.sid.includes("+")) return false;
    return true;
  });
  const PLACE_NAMES = {
    aca: "Академия", bla: "Кузница", bar: "Казарма 17в", ba2: "Казарма 18в",
    sta: "Конюшня", mil: "Мельница", art: "Арт. депо", tem: "Собор",
    cen: "Городской центр", dip: "Дипцентр", tow: "Башня", swa: "Стена",
    wwa: "Палисад", por: "Порт", ferry: "Транспорт",
    gol: "Шахта золота", iro: "Шахта железа", coa: "Шахта угля",
  };
  function classify(sid) {
    for (const m of ["gol", "coa", "iro"]) {
      if (sid.startsWith("eur" + m + ".") || sid === "eur" + m) return m;
    }
    const prefixes = [nation, cluster, "eur", "rus", "tur", "spa", "ukr", "por"];
    for (const p of prefixes) {
      if (sid.startsWith(p)) {
        const rest = sid.slice(p.length);
        for (const place of Object.keys(PLACE_NAMES)) {
          if (rest === place || rest.startsWith(place + ".")) return place;
        }
      }
    }
    return "?";
  }
  for (const u of out) {
    u.__place = classify(u.sid);
    u.__place_ru = PLACE_NAMES[u.__place] || u.__place;
  }
  // Filter by prereqs at T AND require that the place-building exists at T
  // (e.g. academy upgrades require academy to be built).
  const snap = timeline.snapshot(t);
  const placeBuildingSid = (place) => {
    if (place === "gol") return "eurgol";
    if (place === "coa") return "eurcoa";
    if (place === "iro") return "euriro";
    if (place === "tow") return cluster + "tow";
    if (place === "swa") return cluster + "swa";
    if (place === "wwa") return cluster + "wwa";
    if (place === "por") return cluster + "por";
    if (place === "ferry") return "ferry";
    return nation + place;
  };
  const filtered = out.filter(u => {
    const placeSid = placeBuildingSid(u.__place);
    if (!(snap.buildings.get(placeSid) || 0)) return false;
    return _prereqsMet(u.prereqs, snap);
  });
  // Filter out already-researched upgrades
  const result = filtered.filter(u => !snap.upgrades.has(u.sid));
  result.sort((a, b) => {
    const c = (a.__place_ru || "").localeCompare(b.__place_ru || "", "ru");
    return c || fmtName(a).localeCompare(fmtName(b), "ru");
  });
  return result;
}

/**
 * Maximum useful builder count for a build action at time T:
 * min(building's slot cap, total peasants by T).
 */
export function maxBuildersFor(data, slots, building_sid, timeline, t) {
  const slot_cap = slots[building_sid] || 30;
  const peasants = timeline.peasantsAt(t);
  return Math.max(1, Math.min(slot_cap, peasants));
}

// Legacy named exports (no time filter) — kept so old callers still work.
export function producersForNation(data, nation) {
  const units = unitsForNation(data, nation);
  const ids = new Set();
  for (const u of units) for (const b of (u.trained_in || [])) ids.add(b);
  return data.buildings.filter(b => b.nation === nation && ids.has(b.sid));
}
export function unitsTrainedIn(data, nation, buildingSid) {
  return unitsForNation(data, nation).filter(u => (u.trained_in || []).includes(buildingSid));
}
export function upgradesForNation(data, nation) {
  // Used in main.js for lookup-map building. Annotate but don't filter by time.
  const cluster = COMMON_NAME[nation] || "eur";
  const out = data.upgrades.filter(u => u.nation === nation && u.sid && !u.sid.includes("+"));
  const PLACE_NAMES = {
    aca: "Академия", bla: "Кузница", bar: "Казарма 17в", ba2: "Казарма 18в",
    sta: "Конюшня", mil: "Мельница", art: "Арт. депо", tem: "Собор",
    cen: "Городской центр", dip: "Дипцентр", tow: "Башня", swa: "Стена",
    wwa: "Палисад", por: "Порт", ferry: "Транспорт",
    gol: "Шахта золота", iro: "Шахта железа", coa: "Шахта угля",
  };
  function classify(sid) {
    for (const m of ["gol", "coa", "iro"]) {
      if (sid.startsWith("eur" + m + ".") || sid === "eur" + m) return m;
    }
    const prefixes = [nation, cluster, "eur", "rus", "tur", "spa", "ukr", "por"];
    for (const p of prefixes) {
      if (sid.startsWith(p)) {
        const rest = sid.slice(p.length);
        for (const place of Object.keys(PLACE_NAMES)) {
          if (rest === place || rest.startsWith(place + ".")) return place;
        }
      }
    }
    return "?";
  }
  for (const u of out) {
    u.__place = classify(u.sid);
    u.__place_ru = PLACE_NAMES[u.__place] || u.__place;
  }
  return out;
}
