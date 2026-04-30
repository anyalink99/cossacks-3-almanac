// Lightweight timeline-state computer. Mirrors what the Python sim tracks but only
// for prereq-gating purposes (building/upgrade availability + peasant count over time).
// Used by action_form.js to filter dropdowns and gate validity.
//
// What it tracks:
// - At time T: which buildings have completed, which upgrades are done, total peasants.
// - For each known sid: earliest time it becomes "available" (built/researched).
//
// What it does NOT track (defer to actual sim):
// - Resource balance — sim's `events` log will report SKIP if not enough.
// - Producer queue contention — multiple `train` orders on the same building are serialized.
// - Builder slot enforcement — assumed observed by user / sim.

import { isPeasant, DEFAULT_PEASANT } from "./i18n.js";

export class Timeline {
  constructor(buildOrder, data) {
    this.bo = buildOrder;
    this.data = data;
    this.nation = buildOrder.nation;
    this.cluster = (data && data.nations && data.nations.find(n => n.sid === this.nation))?.cluster;
    this._buildEvents();
  }

  _buildEvents() {
    // Each event = { time, kind: "building"|"unit"|"upgrade", sid, count? }
    // We resolve completion times: build finishes at action.at + buildtime;
    // train finishes per-unit; research finishes at action.at + time.
    const ev = [];

    // Starting state — all at time 0.
    for (const [sid, count] of Object.entries(this.bo.starting_buildings || {})) {
      for (let i = 0; i < count; i++) ev.push({ time: 0, kind: "building", sid });
    }
    for (const [sid, count] of Object.entries(this.bo.starting_units || {})) {
      for (let i = 0; i < count; i++) ev.push({ time: 0, kind: "unit", sid });
    }

    // Sort actions by time; chain serially when actions hit the same producer.
    const acts = [...this.bo.actions].sort((a, b) => a.at - b.at);

    // Track per-building "next free time" so concurrent trains in the same
    // building queue serialize. (Crude approximation but good enough.)
    const buildingNextFree = new Map(); // building_sid → time when its queue is empty

    for (const a of acts) {
      const at = +a.at || 0;
      if (a.do === "build") {
        const b = this._findBuilding(a.sid);
        const buildtime = (b?.buildtime_sec) || 30;
        const builders = Math.max(1, +a.builders || 1);
        const realtime = (buildtime * 1.13) / builders;
        ev.push({ time: at + realtime, kind: "building", sid: a.sid });
      } else if (a.do === "train") {
        const u = this._findUnit(a.unit_sid);
        const buildtime = (u?.buildtime_sec) || 30;
        const amount = Math.max(1, +a.amount || 1);
        // Producer queue: production starts when producer is free OR at action.at, whichever later.
        let cursor = Math.max(at, buildingNextFree.get(a.building_sid) || 0);
        for (let i = 0; i < amount; i++) {
          cursor += buildtime;
          ev.push({ time: cursor, kind: "unit", sid: a.unit_sid });
        }
        buildingNextFree.set(a.building_sid, cursor);
      } else if (a.do === "research") {
        const upg = this._findUpgrade(a.upgrade_sid);
        const time = (upg?.time_sec) || 10;
        ev.push({ time: at + time, kind: "upgrade", sid: a.upgrade_sid });
      }
      // assign — no completion event; affects work distribution only.
    }

    ev.sort((x, y) => x.time - y.time);
    this.events = ev;
  }

  _findBuilding(sid) {
    return this.data.buildings.find(b => b.sid === sid && b.nation === this.nation);
  }
  _findUnit(sid) {
    return this.data.units.find(u => u.sid === sid && u.nation === this.nation);
  }
  _findUpgrade(sid) {
    return this.data.upgrades.find(u => u.sid === sid && u.nation === this.nation);
  }

  /** State accumulated through time T. */
  snapshot(t) {
    const buildings = new Map();
    const units = new Map();
    const upgrades = new Set();
    for (const e of this.events) {
      if (e.time > t) break;
      if (e.kind === "building") buildings.set(e.sid, (buildings.get(e.sid) || 0) + 1);
      else if (e.kind === "unit") units.set(e.sid, (units.get(e.sid) || 0) + 1);
      else if (e.kind === "upgrade") upgrades.add(e.sid);
    }
    return { buildings, units, upgrades };
  }

  /** Total peasants completed by time T. */
  peasantsAt(t) {
    const snap = this.snapshot(t);
    let total = 0;
    for (const [sid, n] of snap.units) if (isPeasant(sid)) total += n;
    return total;
  }

  /** Earliest time at which a single prereq sid is satisfied. Returns Infinity if never. */
  earliestForOne(sid) {
    for (const e of this.events) {
      if (e.sid === sid && (e.kind === "building" || e.kind === "upgrade")) return e.time;
    }
    return Infinity;
  }

  /** Earliest time at which ALL prereqs in the list are satisfied. */
  earliestForAll(prereqs) {
    if (!prereqs || !prereqs.length) return 0;
    let latest = 0;
    for (const p of prereqs) {
      const t = this.earliestForOne(p);
      if (!isFinite(t)) return Infinity;
      if (t > latest) latest = t;
    }
    return latest;
  }

  /** Suggested default time for a new action: 5 g-sec after the last action's start (rounded), or 0. */
  suggestNextTime() {
    const last = this.bo.actions.reduce((m, a) => Math.max(m, +a.at || 0), 0);
    return last === 0 ? 0 : last + 30;
  }
}
