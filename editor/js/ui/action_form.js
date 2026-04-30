// Inline expanding form for adding actions.
// Filters dropdowns to only feasible options at the chosen time T.
// Builder count auto-suggests max.

import { fmtName, fmtCost, RES_ORDER, RES_INFO, KIND_INFO } from "./i18n.js";
import {
  buildingsAt, producersAt, unitsTrainedInAt, upgradesAt, maxBuildersFor,
} from "./catalog.js";
import { Timeline } from "./timeline.js";

const $ = (sel, root = document) => root.querySelector(sel);

let onAddCb = null;
let activeKind = null;
let _data = null, _slots = null, _bo = null, _timeline = null;

export function init(onAdd) {
  onAddCb = onAdd;
  document.querySelectorAll(".tab").forEach(btn => {
    btn.addEventListener("click", () => {
      const kind = btn.dataset.tab;
      if (activeKind === kind) {
        activeKind = null;
        btn.classList.remove("active");
        $("#action_form").classList.add("hidden");
        return;
      }
      document.querySelectorAll(".tab").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      activeKind = kind;
      renderForm(kind);
    });
  });
}

export function bindContext(data, slots, bo) {
  _data = data; _slots = slots; _bo = bo;
  _timeline = new Timeline(bo, data);
}

export function refresh() {
  // Rebuild timeline (state changed) and re-render form if open.
  if (_bo && _data) _timeline = new Timeline(_bo, _data);
  if (activeKind) renderForm(activeKind);
}

function renderForm(kind) {
  const root = $("#action_form");
  root.classList.remove("hidden");
  // Default time = "next available" (last action.at + 30, or 0).
  const defaultTime = _timeline ? _timeline.suggestNextTime() : 0;
  const renderers = { build: renderBuild, train: renderTrain, research: renderResearch, assign: renderAssign };
  const html = renderers[kind] ? renderers[kind](defaultTime) : "";
  root.innerHTML = html;
  wireForm(kind);
  // Recalc dropdowns on time change
  const timeInp = $("#f_at", root);
  if (timeInp) timeInp.addEventListener("input", () => onTimeChange(kind));
}

function timeFieldHtml(defaultAt) {
  return `<label class="field">
    <span>Время начала (g-сек)</span>
    <input type="number" id="f_at" value="${defaultAt}" min="0" max="3600" step="5" />
  </label>`;
}

function actionsRowHtml() {
  return `<div class="actions-row">
    <button class="btn btn-ghost" id="f_cancel">Отмена</button>
    <button class="btn btn-primary" id="f_submit">Добавить</button>
  </div>`;
}

function emptyHint(text) {
  return `<div class="hint-empty">${text}</div>`;
}

// ─── Build ─────────────────────────────────────────────────────────
function renderBuild(defaultTime) {
  const items = buildingsAt(_data, _bo.nation, _timeline, defaultTime);
  const available = items.filter(x => x.available);
  if (!available.length) {
    const msg = items.length
      ? "На это время ни одного здания построить нельзя — пререкизиты не выполнены. Подвинь время позже или построй базовые здания (Городской центр, Кузницу)."
      : "Нет зданий для этой нации.";
    return `
      <div class="row">${timeFieldHtml(defaultTime)}</div>
      ${emptyHint(msg)}
      ${actionsRowHtml()}
    `;
  }
  const opts = available.map(x =>
    `<option value="${x.building.sid}">${fmtName(x.building)} — ${fmtCost(x.building)}</option>`
  ).join("");
  const firstSid = available[0].building.sid;
  const maxB = maxBuildersFor(_data, _slots, firstSid, _timeline, defaultTime);
  return `
    <div class="row two">
      <label class="field">
        <span>Здание</span>
        <select id="f_sid">${opts}</select>
      </label>
      <label class="field">
        <span>Строителей <span class="muted small">(max ${maxB})</span></span>
        <input type="number" id="f_builders" value="${maxB}" min="1" max="30" />
      </label>
    </div>
    <div class="row">${timeFieldHtml(defaultTime)}</div>
    ${unavailableListHtml(items.filter(x => !x.available))}
    ${actionsRowHtml()}
  `;
}

function unavailableListHtml(unavailable) {
  if (!unavailable.length) return "";
  const top = unavailable.slice(0, 5).map(x =>
    `<li>${fmtName(x.building)} — нужно: ${x.prereqs.join(", ") || "?"}</li>`
  ).join("");
  return `<details class="locked-list">
    <summary>Недоступно сейчас (${unavailable.length})</summary>
    <ul>${top}${unavailable.length > 5 ? `<li class="muted">…и ещё ${unavailable.length - 5}</li>` : ""}</ul>
  </details>`;
}

// ─── Train ─────────────────────────────────────────────────────────
function renderTrain(defaultTime) {
  const producers = producersAt(_data, _bo.nation, _timeline, defaultTime);
  if (!producers.length) {
    return `
      <div class="row">${timeFieldHtml(defaultTime)}</div>
      ${emptyHint("Нет построенных зданий-производителей к этому времени. Сначала построй Городской центр / Казарму / Конюшню.")}
      ${actionsRowHtml()}
    `;
  }
  const prodOpts = producers.map(p => `<option value="${p.sid}">${fmtName(p)}</option>`).join("");
  const firstProd = producers[0].sid;
  const units = unitsTrainedInAt(_data, _bo.nation, firstProd, _timeline, defaultTime);
  const unitOpts = units.length
    ? units.map(u => `<option value="${u.sid}">${fmtName(u)} — ${fmtCost(u)}</option>`).join("")
    : `<option value="">— нет доступных юнитов —</option>`;
  return `
    <div class="row">
      <label class="field">
        <span>Здание-производитель</span>
        <select id="f_building">${prodOpts}</select>
      </label>
    </div>
    <div class="row two">
      <label class="field">
        <span>Юнит</span>
        <select id="f_unit">${unitOpts}</select>
      </label>
      <label class="field">
        <span>Кол-во</span>
        <input type="number" id="f_amount" value="5" min="1" max="500" />
      </label>
    </div>
    <div class="row">${timeFieldHtml(defaultTime)}</div>
    ${actionsRowHtml()}
  `;
}

// ─── Research ──────────────────────────────────────────────────────
function renderResearch(defaultTime) {
  const ups = upgradesAt(_data, _bo.nation, _timeline, defaultTime);
  if (!ups.length) {
    return `
      <div class="row">${timeFieldHtml(defaultTime)}</div>
      ${emptyHint("Нет доступных апгрейдов к этому времени. Построй Академию / Кузницу / Шахты, чтобы открыть исследования.")}
      ${actionsRowHtml()}
    `;
  }
  const byPlace = new Map();
  for (const u of ups) {
    const k = u.__place_ru || "?";
    if (!byPlace.has(k)) byPlace.set(k, []);
    byPlace.get(k).push(u);
  }
  let opts = "";
  for (const [place, list] of byPlace) {
    opts += `<optgroup label="${place}">`;
    for (const u of list) {
      opts += `<option value="${u.sid}">${fmtName(u)} — ${fmtCost(u)}</option>`;
    }
    opts += `</optgroup>`;
  }
  return `
    <div class="row">
      <label class="field">
        <span>Апгрейд</span>
        <select id="f_upgrade">${opts}</select>
      </label>
    </div>
    <div class="row">${timeFieldHtml(defaultTime)}</div>
    ${actionsRowHtml()}
  `;
}

// ─── Assign ────────────────────────────────────────────────────────
function renderAssign(defaultTime) {
  const peasants = _timeline ? _timeline.peasantsAt(defaultTime) : 0;
  const cells = RES_ORDER.map(r => `
    <div class="assign-row">
      <label><span class="dot" style="background:${RES_INFO[r].color}"></span> ${RES_INFO[r].ru}</label>
      <input type="number" data-res="${r}" value="0" min="0" max="200" />
    </div>
  `).join("");
  return `
    <div class="muted small">Куда отправить крестьян. К этому моменту крестьян будет: <b>${peasants}</b>.</div>
    <div class="assign-grid">${cells}</div>
    <div class="row">${timeFieldHtml(defaultTime)}</div>
    ${actionsRowHtml()}
  `;
}

// ─── Wire-up ───────────────────────────────────────────────────────
function wireForm(kind) {
  const root = $("#action_form");
  $("#f_cancel", root)?.addEventListener("click", closeForm);
  $("#f_submit", root)?.addEventListener("click", () => submitForm(kind));

  if (kind === "build") {
    const sel = $("#f_sid", root);
    sel?.addEventListener("change", () => {
      const t = +$("#f_at", root).value;
      const max = maxBuildersFor(_data, _slots, sel.value, _timeline, t);
      const inp = $("#f_builders", root);
      inp.max = max;
      if (+inp.value > max) inp.value = max;
      const lbl = inp.previousElementSibling.querySelector(".muted");
      if (lbl) lbl.textContent = `(max ${max})`;
    });
  } else if (kind === "train") {
    const bld = $("#f_building", root);
    bld?.addEventListener("change", () => {
      const t = +$("#f_at", root).value;
      const units = unitsTrainedInAt(_data, _bo.nation, bld.value, _timeline, t);
      const sel = $("#f_unit", root);
      sel.innerHTML = units.length
        ? units.map(u => `<option value="${u.sid}">${fmtName(u)} — ${fmtCost(u)}</option>`).join("")
        : `<option value="">— нет доступных юнитов —</option>`;
    });
  }
}

function onTimeChange(kind) {
  // Re-render the form so dropdowns reflect new feasibility at the new time.
  renderForm(kind);
}

function closeForm() {
  document.querySelectorAll(".tab").forEach(b => b.classList.remove("active"));
  $("#action_form").classList.add("hidden");
  activeKind = null;
}

function submitForm(kind) {
  const root = $("#action_form");
  const at = +$("#f_at", root).value;
  let action = null;
  if (kind === "build") {
    const sid = $("#f_sid", root)?.value;
    const builders = +($("#f_builders", root)?.value || 1);
    if (!sid) return;
    action = { at, do: "build", sid, builders };
  } else if (kind === "train") {
    const building_sid = $("#f_building", root)?.value;
    const unit_sid = $("#f_unit", root)?.value;
    const amount = +($("#f_amount", root)?.value || 1);
    if (!building_sid || !unit_sid) return;
    action = { at, do: "train", building_sid, unit_sid, amount };
  } else if (kind === "research") {
    const upgrade_sid = $("#f_upgrade", root)?.value;
    if (!upgrade_sid) return;
    action = { at, do: "research", upgrade_sid };
  } else if (kind === "assign") {
    action = { at, do: "assign" };
    let total = 0;
    root.querySelectorAll("input[data-res]").forEach(inp => {
      const v = +inp.value;
      if (v > 0) { action[inp.dataset.res] = v; total += v; }
    });
    if (total === 0) return;
  }
  if (action) {
    onAddCb(action);
    closeForm();
  }
}
