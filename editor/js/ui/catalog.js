// Catalog helpers — derive per-nation lists from data.json, with optional
// filtering by Timeline state at a given time T.

import { COMMON_NAME, fmtName } from "./i18n.js";

const NON_BUILDABLE = new Set(["ferry", "transport", "fishboat"]);

const PLACE_NAMES = {
  aca: "Академия", bla: "Кузница", bar: "Казарма 17в", ba2: "Казарма 18в",
  sta: "Конюшня", mil: "Мельница", art: "Арт. депо", tem: "Собор",
  cen: "Городской центр", dip: "Дипцентр", tow: "Башня", swa: "Стена",
  wwa: "Палисад", por: "Порт", ferry: "Транспорт",
  gol: "Шахта золота", iro: "Шахта железа", coa: "Шахта угля",
  mar: "Рынок", hou: "Дом", sto: "Склад",
};
const SHARED_PLACES = new Set(["tow", "swa", "wwa", "por"]);
const MINE_PLACES = new Set(["gol", "iro", "coa"]);

export function classifyUpgradePlace(sid, nation, cluster) {
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

export function placeBuildingSid(place, nation, cluster) {
  if (MINE_PLACES.has(place)) return "eur" + place;
  if (SHARED_PLACES.has(place)) return cluster + place;
  if (place === "ferry") return "ferry";
  return nation + place;
}

export { PLACE_NAMES };

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
 * Returns array of {building, available, earliest, prereqs}.
 * `earliest` is the smallest t at which all prereqs are satisfied (Infinity if never).
 */
export function buildingsAt(data, nation, timeline, t) {
  const list = buildingsForNation(data, nation);
  const snap = timeline.snapshot(t);
  return list
    .map(b => ({
      building: b,
      available: _prereqsMet(b.prereqs, snap),
      earliest: timeline.earliestForAll(b.prereqs || []),
      prereqs: b.prereqs || [],
    }))
    .sort((a, b) => (a.available !== b.available ? (a.available ? -1 : 1)
                                                  : a.earliest - b.earliest
                                                    || fmtName(a.building).localeCompare(fmtName(b.building), "ru")));
}

export function unitsForNation(data, nation) {
  return data.units.filter(u => u.nation === nation && u.trained_in && u.trained_in.length);
}

/**
 * All producer buildings for the nation, annotated with availability at T.
 */
export function producersAt(data, nation, timeline, t) {
  const all = data.buildings.filter(b => b.nation === nation);
  const units = unitsForNation(data, nation);
  const producerSids = new Set();
  for (const u of units) for (const b of (u.trained_in || [])) producerSids.add(b);
  const snap = timeline.snapshot(t);
  const out = all
    .filter(b => producerSids.has(b.sid))
    .map(b => ({
      sid: b.sid,
      name_ru: b.name_ru,
      name_en: b.name_en,
      available: (snap.buildings.get(b.sid) || 0) > 0,
      earliest: timeline.earliestForOne(b.sid),
    }));
  out.sort((a, b) => (a.available !== b.available ? (a.available ? -1 : 1)
                                                   : a.earliest - b.earliest));
  return out;
}

/**
 * Units producible in `building_sid`, annotated with availability at T.
 * `earliest` accounts for both unit-prereqs and the producer building's own ETA.
 */
export function unitsTrainedInAt(data, nation, building_sid, timeline, t) {
  const all = unitsForNation(data, nation).filter(u => (u.trained_in || []).includes(building_sid));
  const snap = timeline.snapshot(t);
  const producerEta = timeline.earliestForOne(building_sid);
  return all
    .map(u => {
      const own = timeline.earliestForAll(u.prereqs || []);
      const earliest = Math.max(producerEta, own);
      return {
        unit: u,
        available: (snap.buildings.get(building_sid) || 0) > 0 && _prereqsMet(u.prereqs, snap),
        earliest,
        prereqs: u.prereqs || [],
      };
    })
    .sort((a, b) => (a.available !== b.available ? (a.available ? -1 : 1)
                                                   : a.earliest - b.earliest
                                                     || fmtName(a.unit).localeCompare(fmtName(b.unit), "ru")));
}

/**
 * All upgrades for the nation, annotated with availability at T.
 * Each entry: {upgrade, available, earliest, place, place_ru, place_sid}.
 * `earliest` accounts for both upgrade-prereqs and the host building's ETA.
 */
export function upgradesAt(data, nation, timeline, t) {
  const cluster = COMMON_NAME[nation] || "eur";
  const ups = data.upgrades.filter(u => u.nation === nation && u.sid && !u.sid.includes("+"));
  for (const u of ups) {
    u.__place = classifyUpgradePlace(u.sid, nation, cluster);
    u.__place_ru = PLACE_NAMES[u.__place] || u.__place;
    u.__place_sid = placeBuildingSid(u.__place, nation, cluster);
  }
  const snap = timeline.snapshot(t);
  return ups
    .filter(u => !snap.upgrades.has(u.sid))
    .map(u => {
      const own = timeline.earliestForAll(u.prereqs || []);
      const placeEta = timeline.earliestForOne(u.__place_sid);
      const earliest = Math.max(own, placeEta);
      return {
        upgrade: u,
        available: (snap.buildings.get(u.__place_sid) || 0) > 0 && _prereqsMet(u.prereqs, snap),
        earliest,
        place: u.__place,
        place_ru: u.__place_ru,
        place_sid: u.__place_sid,
        prereqs: u.prereqs || [],
      };
    })
    .sort((a, b) => (a.available !== b.available ? (a.available ? -1 : 1)
                                                   : a.earliest - b.earliest
                                                     || fmtName(a.upgrade).localeCompare(fmtName(b.upgrade), "ru")));
}

/**
 * Maximum useful builder count for a build action at time T:
 * min(building's slot cap, peasants not already busy at T).
 */
export function maxBuildersFor(data, slots, building_sid, timeline, t) {
  const slot_cap = slots[building_sid] || 30;
  const free = timeline.freePeasantsAt(t);
  return Math.max(1, Math.min(slot_cap, free));
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
  for (const u of out) {
    u.__place = classifyUpgradePlace(u.sid, nation, cluster);
    u.__place_ru = PLACE_NAMES[u.__place] || u.__place;
  }
  return out;
}
