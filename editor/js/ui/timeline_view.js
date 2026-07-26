// Timeline SVG view: renders the build-order as horizontal tracks.
// Tracks:
//   - Time axis (top)
//   - Постройки    — one row per active build, bar = construction span
//   - Юниты        — one row per producing building, bars = trained units
//   - Действия     — markers (research/assign/trade as discrete shapes)
// Click on any element → onSelect(actionRef).

import { fmtName } from "./i18n.js";
import { tr as translate } from "../../../assets/js/runtime-i18n.js";

const NS = "http://www.w3.org/2000/svg";

const LABEL_W = 130;   // left gutter for track labels
const AXIS_H  = 26;
const ROW_H   = 22;
const MIN_BAR_W = 4;
const PAD_X   = 6;

const TRACK_ORDER = [
  { id: "build",    label: "Постройки" },
  { id: "train",    label: "Юниты" },
  { id: "actions",  label: "Действия" },
];

let _svg = null;
let _state = {
  buildOrder: null,
  bundle: null,
  timeline: null,
  pxPerSec: 2,
  selected: null,
  onSelect: () => {},
  onChange: () => {},
};

export function init({ svg, onSelect, onChange }) {
  _svg = svg;
  _state.onSelect = onSelect || (() => {});
  _state.onChange = onChange || (() => {});
}

export function setZoom(px) {
  _state.pxPerSec = Math.max(0.5, Math.min(15, px));
  redraw();
}

export function getZoom() { return _state.pxPerSec; }

export function setSelection(action) {
  _state.selected = action;
  redraw();
}

export function render({ buildOrder, bundle, timeline }) {
  _state.buildOrder = buildOrder;
  _state.bundle = bundle;
  _state.timeline = timeline;
  redraw();
}

function redraw() {
  if (!_svg || !_state.buildOrder) return;
  const bo = _state.buildOrder;
  const maxT = bo.max_time_sec || 900;
  const width = LABEL_W + Math.ceil(maxT * _state.pxPerSec) + PAD_X * 2;

  // Build lane layout
  const lanes = computeLanes(bo, _state.bundle);
  let y = AXIS_H;
  const trackTops = {};
  const trackHeights = {};
  for (const tr of TRACK_ORDER) {
    trackTops[tr.id] = y;
    const rows = lanes[tr.id].length;
    trackHeights[tr.id] = Math.max(1, rows) * ROW_H + 6;
    y += trackHeights[tr.id];
  }
  const totalH = y + 12;
  _svg.setAttribute("width", width);
  _svg.setAttribute("height", totalH);
  _svg.setAttribute("viewBox", `0 0 ${width} ${totalH}`);
  while (_svg.firstChild) _svg.removeChild(_svg.firstChild);

  // Time axis
  drawTimeAxis(maxT, width);

  // Track backgrounds + labels
  for (let i = 0; i < TRACK_ORDER.length; i++) {
    const tr = TRACK_ORDER[i];
    const top = trackTops[tr.id];
    const h = trackHeights[tr.id];
    const bg = el("rect", {
      x: 0, y: top, width, height: h,
      class: i % 2 === 0 ? "track-bg" : "track-bg alt",
    });
    _svg.appendChild(bg);
    _svg.appendChild(el("text", {
      x: 10, y: top + 14, class: "track-label",
    }, [translate(tr.label).toUpperCase()]));
  }

  // Body content per track
  drawBuildBars(lanes.build, trackTops.build);
  drawUnitBars(lanes.train, trackTops.train);
  drawActionMarkers(lanes.actions, trackTops.actions);
}

function tx(t) {
  return LABEL_W + Math.round(t * _state.pxPerSec) + PAD_X;
}

function drawTimeAxis(maxT, width) {
  const bg = el("rect", { x: 0, y: 0, width, height: AXIS_H, class: "time-axis-bg" });
  _svg.appendChild(bg);
  _svg.appendChild(el("rect", { x: 0, y: 0, width: LABEL_W, height: AXIS_H, class: "time-axis-bg" }));
  _svg.appendChild(el("text", { x: 10, y: 16, class: "track-label" }, [translate("ВРЕМЯ (г-сек)")]));
  // Tick step: every 30g minor, 60g major (≈ 1 game-minute).
  const minor = 30, major = 60;
  for (let t = 0; t <= maxT; t += minor) {
    const x = tx(t);
    const isMajor = t % major === 0;
    _svg.appendChild(el("line", {
      x1: x, y1: AXIS_H - (isMajor ? 10 : 5), x2: x, y2: AXIS_H,
      class: isMajor ? "time-tick major" : "time-tick",
    }));
    if (isMajor) {
      _svg.appendChild(el("text", {
        x, y: AXIS_H - 12, class: "time-label", "text-anchor": "middle",
      }, [String(t)]));
    }
  }
}

// Lay actions into per-track rows. Multiple sids share a row only if their
// time-spans don't overlap; otherwise we drop to a new row.
function computeLanes(bo, bundle) {
  const lanes = { build: [], train: [], actions: [] };
  const byBld = bundle && bundle.data
    ? new Map(bundle.data.buildings.filter(b => b.nation === bo.nation).map(b => [b.sid, b]))
    : new Map();
  const byUnit = bundle && bundle.data
    ? new Map(bundle.data.units.filter(u => u.nation === bo.nation).map(u => [u.sid, u]))
    : new Map();

  for (const action of bo.actions) {
    if (action.do === "build") {
      const b = byBld.get(action.sid);
      const buildtime = (b?.buildtime_sec) || 30;
      const builders = Math.max(1, +action.builders || 1);
      const span = (buildtime * 1.13) / builders;
      const start = +action.at || 0;
      const item = {
        action, start, end: start + span,
        title: b ? fmtName(b) : action.sid,
        meta: `строителей ${builders}`,
      };
      placeInLane(lanes.build, item);
    } else if (action.do === "train") {
      const u = byUnit.get(action.unit_sid);
      const buildtime = (u?.buildtime_sec) || 10;
      const amount = Math.max(1, +action.amount || 1);
      const start = +action.at || 0;
      const span = buildtime * amount;
      const item = {
        action, start, end: start + span,
        title: `${amount}× ${u ? fmtName(u) : action.unit_sid}`,
        meta: `в ${action.building_sid}`,
      };
      placeInLane(lanes.train, item);
    } else if (action.do === "train_infinite") {
      // Infinite production: shown as a stretching bar from `at` to maxT with
      // an ∞ glyph at the start. Sits on the Units track.
      const u = byUnit.get(action.unit_sid);
      const start = +action.at || 0;
      const item = {
        action, start, end: bo.max_time_sec || 900,
        title: `∞ ${u ? fmtName(u) : action.unit_sid}`,
        meta: `в ${action.building_sid}`,
        infinite: true,
      };
      placeInLane(lanes.train, item);
    } else {
      // research / assign / trade → single-point marker on Actions row.
      const start = +action.at || 0;
      const item = {
        action, start, end: start,
        title: shortTitle(action), meta: "",
      };
      placeInLane(lanes.actions, item, /*pointLike=*/ true);
    }
  }
  return lanes;
}

function placeInLane(lanes, item, pointLike = false) {
  for (const lane of lanes) {
    const overlap = lane.some(o => pointLike
      ? Math.abs(o.start - item.start) < 5
      : !(item.end <= o.start || item.start >= o.end));
    if (!overlap) { lane.push(item); return; }
  }
  lanes.push([item]);
}

function shortTitle(a) {
  if (a.do === "research") return `R ${a.upgrade_sid}`;
  if (a.do === "assign")   return "Раскидать";
  if (a.do === "trade")    return `${a.amount} ${a.sell}→${a.buy}`;
  return a.do || "?";
}

function drawBuildBars(lanes, top) {
  lanes.forEach((row, lane) => {
    const y = top + lane * ROW_H + 3;
    for (const it of row) {
      const x1 = tx(it.start);
      const x2 = tx(it.end);
      const w = Math.max(MIN_BAR_W, x2 - x1);
      const isSel = _state.selected === it.action;
      const bar = el("rect", {
        x: x1, y, width: w, height: ROW_H - 6,
        class: "build-bar" + (isSel ? " selected" : ""),
      });
      bar.appendChild(el("title", {}, [
        `${it.title}\n` +
        `Старт: t=${it.start}г · Готово: t=${Math.round(it.end)}г\n` +
        `${it.meta}\n— тяни мышкой чтобы изменить время —`
      ]));
      attachDraggable(bar, it.action);
      _svg.appendChild(bar);
      if (w > 60) {
        _svg.appendChild(el("text", {
          x: x1 + 6, y: y + ROW_H - 11, class: "bar-label",
        }, [`${it.title}`]));
      }
    }
  });
}

function drawUnitBars(lanes, top) {
  lanes.forEach((row, lane) => {
    const y = top + lane * ROW_H + 3;
    for (const it of row) {
      const x1 = tx(it.start);
      const x2 = tx(it.end);
      const w = Math.max(MIN_BAR_W, x2 - x1);
      const isSel = _state.selected === it.action;
      const cls = (it.infinite ? "unit-bar infinite" : "unit-bar") + (isSel ? " selected" : "");
      const bar = el("rect", {
        x: x1, y, width: w, height: ROW_H - 6, class: cls,
      });
      bar.appendChild(el("title", {}, [
        `${it.title}\n` +
        (it.infinite ? `Активно с t=${it.start}г, до конца` : `Готово: t=${Math.round(it.end)}г`) +
        `\n${it.meta}\n— тяни мышкой чтобы изменить время —`
      ]));
      attachDraggable(bar, it.action);
      _svg.appendChild(bar);
      if (w > 60) {
        _svg.appendChild(el("text", {
          x: x1 + 6, y: y + ROW_H - 11, class: "bar-label",
        }, [`${it.title}`]));
      }
    }
  });
}

function drawActionMarkers(lanes, top) {
  lanes.forEach((row, lane) => {
    const cy = top + lane * ROW_H + ROW_H / 2;
    for (const it of row) {
      const x = tx(it.start);
      const a = it.action;
      const isSel = _state.selected === a;
      let node;
      if (a.do === "research") {
        node = el("polygon", {
          points: `${x},${cy - 7} ${x + 7},${cy} ${x},${cy + 7} ${x - 7},${cy}`,
          class: "research-marker" + (isSel ? " selected" : ""),
        });
      } else if (a.do === "assign") {
        node = el("rect", {
          x: x - 6, y: cy - 6, width: 12, height: 12,
          class: "assign-marker" + (isSel ? " selected" : ""),
        });
      } else if (a.do === "trade") {
        node = el("circle", {
          cx: x, cy, r: 7,
          class: "trade-marker" + (isSel ? " selected" : ""),
        });
      } else {
        node = el("circle", { cx: x, cy, r: 5, fill: "#888" });
      }
      node.appendChild(el("title", {}, [
        `${it.title} @ t=${it.start}г\n— тяни мышкой чтобы изменить время —`
      ]));
      attachDraggable(node, a);
      _svg.appendChild(node);
      _svg.appendChild(el("text", {
        x: x + 10, y: cy + 4, class: "bar-label",
      }, [it.title]));
    }
  });
}

function el(tag, attrs = {}, children = []) {
  const node = document.createElementNS(NS, tag);
  for (const [k, v] of Object.entries(attrs)) {
    node.setAttribute(k, v);
  }
  for (const c of children) {
    if (typeof c === "string") node.appendChild(document.createTextNode(c));
    else node.appendChild(c);
  }
  return node;
}

// Combined click+drag handler. Click → select; drag (>3px) → move `at`.
const DRAG_TOLERANCE_PX = 3;
const DRAG_SNAP_G = 5;
function attachDraggable(node, action) {
  node.style.cursor = "grab";
  node.addEventListener("mousedown", (e) => {
    if (e.button !== 0) return;
    e.preventDefault();
    e.stopPropagation();
    const startX = e.clientX;
    const origAt = +action.at || 0;
    let moved = false;
    node.style.cursor = "grabbing";
    const onMove = (ev) => {
      const dx = ev.clientX - startX;
      if (!moved && Math.abs(dx) < DRAG_TOLERANCE_PX) return;
      moved = true;
      const dt = dx / _state.pxPerSec;
      const newAt = Math.max(0, Math.round((origAt + dt) / DRAG_SNAP_G) * DRAG_SNAP_G);
      if (newAt !== action.at) {
        action.at = newAt;
        _state.selected = action;
        redraw();
      }
    };
    const onUp = () => {
      document.removeEventListener("mousemove", onMove);
      document.removeEventListener("mouseup", onUp);
      node.style.cursor = "grab";
      if (moved) _state.onChange(action);
      else _state.onSelect(action);
    };
    document.addEventListener("mousemove", onMove);
    document.addEventListener("mouseup", onUp);
  });
}
