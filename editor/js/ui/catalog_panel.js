// Catalog: sidebar of all buildings / units / upgrades / "other" actions
// for the current nation. Click → ADD action with auto-snap time.

import { fmtName, fmtCost, RES_ORDER, RES_INFO, buildingClusterFor } from "./i18n.js";
import {
  buildingsAt, producersAt, unitsTrainedInAt, upgradesAt,
} from "./catalog.js";

let _data = null, _bo = null, _timeline = null, _onAdd = null;
let _activeCat = "build";
let _searchTerm = "";

export function init({ data, buildOrder, timeline, onAdd }) {
  _data = data; _bo = buildOrder; _timeline = timeline; _onAdd = onAdd;
  document.querySelectorAll(".cat-tab").forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".cat-tab").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      _activeCat = btn.dataset.cat;
      render();
    });
  });
  const search = document.querySelector("#catalog_search");
  search?.addEventListener("input", () => {
    _searchTerm = search.value.toLowerCase().trim();
    render();
  });
  render();
}

export function refresh(buildOrder, timeline) {
  _bo = buildOrder; _timeline = timeline;
  render();
}

function render() {
  const ul = document.querySelector("#catalog_list");
  if (!ul) return;
  ul.innerHTML = "";
  const items = collect(_activeCat).filter(itemMatchesSearch);
  for (const it of items) {
    const li = document.createElement("li");
    // Visually-locked only if there's NO path to make it available
    // (prereqs aren't planned and we can't reach it). Time-locked items
    // (prereqs already planned, just not done yet) look normal — clicking
    // them snaps the start-time to when they become valid.
    const reachable = it.available || (isFinite(it.earliest) && it.earliest >= 0);
    li.className = "cat-item" + (it.available ? " available" : (reachable ? " future" : " locked"));
    li.dataset.kind = it.kind;
    // For units: offer two buttons — +5 (finite) and ∞ (infinite).
    const extra = it.kind === "train"
      ? `<button class="cat-mini-btn" data-mode="finite" title="Обучить 5">+5</button>
         <button class="cat-mini-btn cat-inf" data-mode="infinite" title="Бесконечное производство">∞</button>`
      : "";
    li.innerHTML = `
      <span class="cat-icon">${iconFor(it.kind)}</span>
      <div class="cat-body">
        <div class="cat-name">${it.name}</div>
        <div class="cat-meta">${it.meta}</div>
      </div>
      ${it.tag ? `<span class="cat-tag">${it.tag}</span>` : ""}
      ${extra}
    `;
    if (it.kind === "train") {
      li.querySelector("[data-mode='finite']").addEventListener("click", (ev) => {
        ev.stopPropagation();
        _onAdd({ ...it, _mode: "finite" });
      });
      li.querySelector("[data-mode='infinite']").addEventListener("click", (ev) => {
        ev.stopPropagation();
        _onAdd({ ...it, _mode: "infinite" });
      });
      // Body click → also finite by default
      li.addEventListener("click", () => _onAdd({ ...it, _mode: "finite" }));
    } else {
      li.addEventListener("click", () => _onAdd(it));
    }
    ul.appendChild(li);
  }
  if (!items.length) {
    ul.innerHTML = `<div class="muted small" style="padding: 12px; text-align: center;">Ничего не найдено.</div>`;
  }
}

function itemMatchesSearch(it) {
  if (!_searchTerm) return true;
  return (it.name || "").toLowerCase().includes(_searchTerm)
      || (it.sid || "").toLowerCase().includes(_searchTerm);
}

function iconFor(kind) {
  return ({ build: "Стр", train: "Об", research: "Иc", assign: "Рк", trade: "Тор" })[kind] || "?";
}

function collect(cat) {
  if (!_data || !_bo || !_timeline) return [];
  const nat = _bo.nation;
  const out = [];

  if (cat === "build") {
    const list = buildingsAt(_data, nat, _timeline, 0);
    for (const x of list) {
      out.push({
        kind: "build",
        sid: x.building.sid,
        name: fmtName(x.building),
        meta: fmtCost(x.building),
        available: x.available,
        tag: x.available ? "" : tagForEarliest(x.earliest),
        earliest: x.earliest,
        payload: { sid: x.building.sid, builders: 1 },
      });
    }
  } else if (cat === "train") {
    const producers = producersAt(_data, nat, _timeline, 0);
    for (const p of producers) {
      const units = unitsTrainedInAt(_data, nat, p.sid, _timeline, 0);
      for (const u of units) {
        const available = p.available && u.available;
        // earliest = max(producer.earliest, unit.earliest from its prereqs)
        const earliest = Math.max(
          isFinite(p.earliest) ? p.earliest : 0,
          isFinite(u.earliest) ? u.earliest : 0,
        );
        out.push({
          kind: "train",
          sid: u.unit.sid,
          name: fmtName(u.unit),
          meta: `в ${fmtName(p)} · ${fmtCost(u.unit)}`,
          available,
          tag: available ? "" : tagForEarliest(earliest),
          earliest,
          payload: { building_sid: p.sid, unit_sid: u.unit.sid, amount: 5 },
        });
      }
    }
  } else if (cat === "research") {
    const ups = upgradesAt(_data, nat, _timeline, 0);
    for (const x of ups) {
      out.push({
        kind: "research",
        sid: x.upgrade.sid,
        name: fmtName(x.upgrade),
        meta: `${x.place_ru} · ${fmtCost(x.upgrade)}`,
        available: x.available,
        tag: x.available ? "" : tagForEarliest(x.earliest),
        earliest: x.earliest,
        payload: { upgrade_sid: x.upgrade.sid },
      });
    }
  } else if (cat === "other") {
    // Assign (always available)
    out.push({
      kind: "assign",
      sid: "assign",
      name: "Раскидать крестьян",
      meta: "распределение по ресурсам и шахтам",
      available: true,
      tag: "",
      earliest: 0,
      payload: {},
    });
    // Trade (gated on market built)
    const marketSid = buildingClusterFor(nat, "mar") + "mar";
    const marketEarliest = _timeline.earliestForOne(marketSid);
    const haveMarket = isFinite(marketEarliest);
    out.push({
      kind: "trade",
      sid: "trade",
      name: "Обмен на рынке",
      meta: "продать одно — купить другое",
      available: haveMarket && marketEarliest <= 0,
      tag: haveMarket ? (marketEarliest > 0 ? tagForEarliest(marketEarliest) : "") : "🔒 нужен рынок",
      earliest: isFinite(marketEarliest) ? marketEarliest : Infinity,
      payload: { sell: "food", buy: "wood", amount: 100 },
    });
  }
  return out;
}

function tagForEarliest(earliest) {
  if (!isFinite(earliest)) return "🔒 нет плана";
  if (earliest <= 0) return "";
  return `с t=${Math.round(earliest)}г`;
}
