// Editor v0.4 — timeline-based UI.
// Catalog (left) → Timeline (center) → Inspector (bottom).

import { loadAll } from "./data_loader.js";
import { initPyodide, runSimulation, importReplay, listReplayPlayers } from "./pyodide_runner.js";
import * as BO from "./build_order.js";
import * as Charts from "./ui/charts.js";
import { upgradesForNation } from "./ui/catalog.js";
import { Timeline } from "./ui/timeline.js";
import * as CatalogPanel from "./ui/catalog_panel.js";
import * as TimelineView from "./ui/timeline_view.js";
import * as Inspector from "./ui/inspector.js";
import { maxBuildersFor } from "./ui/catalog.js";
import {
  RES_ORDER, RES_INFO, RES_PRESETS, PEASANT_PRESETS,
  fmtName, fmtTime, DEFAULT_PEASANT,
} from "./ui/i18n.js";

const $ = (sel) => document.querySelector(sel);
const status = $("#status");
function setStatus(text, cls = "loading") {
  status.textContent = text;
  status.className = `pill ${cls}`;
}

let bundle = null;
let buildOrder = BO.load();
let currentTimeline = null;

function rebuildTimeline() {
  if (!bundle) return;
  currentTimeline = new Timeline(buildOrder, bundle.data);
}

function refreshAll() {
  rebuildTimeline();
  CatalogPanel.refresh(buildOrder, currentTimeline);
  TimelineView.render({ buildOrder, bundle, timeline: currentTimeline });
  Inspector.bind(buildOrder, currentTimeline);
  $("#actions_count").textContent = String(buildOrder.actions.length);
}

// ─── Add an action from the catalog with auto-snap time ────────────
function addFromCatalog(item) {
  const at = computeSnapTime(item);
  const action = buildActionFromCatalog(item, at);
  buildOrder.actions.push(action);
  buildOrder.actions.sort((a, b) => a.at - b.at);
  BO.save(buildOrder);
  refreshAll();
  TimelineView.setSelection(action);
  Inspector.select(action);
}

function computeSnapTime(item) {
  if (!currentTimeline) return 0;
  let t = isFinite(item.earliest) ? Math.round(item.earliest) : currentTimeline.suggestNextTime();
  // For build, also need at least 1 free peasant
  if (item.kind === "build") {
    const free = currentTimeline.earliestTimeFreePeasants(1, t);
    if (isFinite(free)) t = Math.max(t, Math.round(free));
  }
  return Math.max(0, t);
}

function buildActionFromCatalog(item, at) {
  const base = { at };
  if (item.kind === "build") {
    const max = maxBuildersFor(bundle.data, bundle.slots, item.payload.sid, currentTimeline, at);
    return { ...base, do: "build", sid: item.payload.sid, builders: max };
  }
  if (item.kind === "train") {
    if (item._mode === "infinite") {
      return { ...base, do: "train_infinite", building_sid: item.payload.building_sid, unit_sid: item.payload.unit_sid };
    }
    return { ...base, do: "train", building_sid: item.payload.building_sid, unit_sid: item.payload.unit_sid, amount: item.payload.amount };
  }
  if (item.kind === "research") return { ...base, do: "research", upgrade_sid: item.payload.upgrade_sid };
  if (item.kind === "assign")   return { ...base, do: "assign" };
  if (item.kind === "trade")    return { ...base, do: "trade", sell: item.payload.sell, buy: item.payload.buy, amount: item.payload.amount };
  return { ...base, do: item.kind };
}

// ─── Settings drawer ───────────────────────────────────────────────
function fillSelect(elId, list, currentValue, extraText = () => "") {
  const sel = $(`#${elId}`);
  if (!sel) return;
  sel.innerHTML = "";
  for (const item of list) {
    const opt = document.createElement("option");
    opt.value = String(item.value);
    const extra = extraText(item);
    opt.textContent = (item.label_ru || item.label_en || String(item.value)) + (extra ? ` ${extra}` : "");
    if (String(item.value) === String(currentValue)) opt.selected = true;
    sel.appendChild(opt);
  }
}

function renderControls() {
  const settings = bundle.settings;
  const ms = buildOrder.map_settings ||= {};

  const natSel = $("#nation");
  natSel.innerHTML = "";
  for (const n of bundle.data.nations) {
    const opt = document.createElement("option");
    opt.value = n.sid;
    opt.textContent = n.name_ru || n.name_en || n.sid;
    if (n.sid === buildOrder.nation) opt.selected = true;
    natSel.appendChild(opt);
  }
  $("#max_time").value = String(buildOrder.max_time_sec || 900);

  fillSelect("set_mapsize",       settings.mapsize,       ms.mapsize       ?? settings.defaults.gen.mapsize,
             (x) => `(${x.tiles}×${x.tiles})`);
  fillSelect("set_terraintype",   settings.terraintype,   ms.terraintype   ?? settings.defaults.gen.terraintype);
  fillSelect("set_relieftype",    settings.relieftype,    ms.relieftype    ?? settings.defaults.gen.relieftype);
  fillSelect("set_season",        settings.season,        ms.season        ?? settings.defaults.gen.season);
  fillSelect("set_resourcestart", settings.resourcestart, ms.resourcestart ?? settings.defaults.gen.resourcestart,
             (x) => `· ${x.amount.toLocaleString("ru-RU")} ед.`);
  fillSelect("set_resourcemines", settings.resourcemines, ms.resourcemines ?? settings.defaults.gen.resourcemines);

  fillSelect("set_gamespeed",     settings.gamespeed,     ms.gamespeed     ?? settings.defaults.additional.gamespeed,
             (x) => `(×${x.factor})`);
  fillSelect("set_startingunits", settings.startingunits, ms.startingunits ?? settings.defaults.additional.startingunits);
  fillSelect("set_peacetime",     settings.peacetime,     ms.peacetime     ?? settings.defaults.additional.peacetime,
             (x) => x.gsec ? `· ${x.gsec}g` : "");
  fillSelect("set_century18",     settings.century18,     ms.century18     ?? settings.defaults.additional.century18);
  fillSelect("set_capture",       settings.capture,       ms.capture       ?? settings.defaults.additional.capture);
  fillSelect("set_marketdip",     settings.marketdip,     ms.marketdip     ?? settings.defaults.additional.marketdip);
  fillSelect("set_cannons",       settings.cannons,       ms.cannons       ?? settings.defaults.additional.cannons);
  fillSelect("set_balloon",       settings.balloon,       ms.balloon       ?? settings.defaults.additional.balloon);
  fillSelect("set_limit",         settings.limit,         ms.limit         ?? settings.defaults.additional.limit,
             (x) => x.units ? `(${x.units})` : "");
  fillSelect("set_teams",         settings.teams,         ms.teams         ?? settings.defaults.additional.teams);
  fillSelect("set_difficulty",    settings.difficulty,    ms.difficulty    ?? 1,
             (x) => `(×${x.koef})`);

  const peaSel = $("#start_peasants");
  peaSel.innerHTML = "";
  const peaSid = DEFAULT_PEASANT[buildOrder.nation];
  const currentPea = (buildOrder.starting_units && buildOrder.starting_units[peaSid]) || 18;
  for (const p of PEASANT_PRESETS) {
    const opt = document.createElement("option");
    opt.value = String(p.value);
    opt.textContent = p.label;
    if (p.value === currentPea) opt.selected = true;
    peaSel.appendChild(opt);
  }

  const row = $("#starting_resources");
  row.innerHTML = "";
  for (const r of RES_ORDER) {
    const cell = document.createElement("div");
    cell.className = "resource-input";
    const val = (buildOrder.starting_resources?.[r]) ?? 0;
    const opts = RES_PRESETS.map(p =>
      `<option value="${p.value}" ${p.value === val ? "selected" : ""}>${p.label}</option>`
    ).join("");
    const customOpt = !RES_PRESETS.some(p => p.value === val)
      ? `<option value="${val}" selected>${val.toLocaleString("ru-RU")} (своё)</option>` : "";
    cell.innerHTML = `
      <span><span class="dot" style="background:${RES_INFO[r].color}"></span> ${RES_INFO[r].ru}</span>
      <select data-res="${r}">${customOpt}${opts}</select>
    `;
    row.appendChild(cell);
  }
}

function readControls() {
  const newNation = $("#nation").value;
  if (newNation !== buildOrder.nation) {
    BO.rebaseToNation(buildOrder, newNation);
  }
  buildOrder.max_time_sec = +$("#max_time").value;
  delete (buildOrder.map_config || {}).walk_overhead;

  const ms = buildOrder.map_settings ||= {};
  const enums = {
    mapsize: "set_mapsize", terraintype: "set_terraintype", relieftype: "set_relieftype",
    season: "set_season", resourcestart: "set_resourcestart", resourcemines: "set_resourcemines",
    gamespeed: "set_gamespeed", startingunits: "set_startingunits", peacetime: "set_peacetime",
    century18: "set_century18", capture: "set_capture", marketdip: "set_marketdip",
    cannons: "set_cannons", balloon: "set_balloon", limit: "set_limit",
    teams: "set_teams", difficulty: "set_difficulty",
  };
  for (const [key, elId] of Object.entries(enums)) {
    const el = $(`#${elId}`);
    if (el) ms[key] = +el.value;
  }
  buildOrder.game_speed = ["slow", "normal", "fast"][ms.gamespeed] || "fast";

  const rsPreset = bundle.settings.resourcestart.find(x => x.value === ms.resourcestart);
  if (rsPreset && !buildOrder._resources_customized) {
    buildOrder.starting_resources = {
      food: rsPreset.amount, wood: rsPreset.amount, stone: rsPreset.amount,
      gold: rsPreset.amount, iron: rsPreset.amount, coal: rsPreset.amount,
    };
  } else {
    const sr = buildOrder.starting_resources || {};
    document.querySelectorAll("#starting_resources select[data-res]").forEach(sel => {
      sr[sel.dataset.res] = +sel.value;
    });
    buildOrder.starting_resources = sr;
  }

  if (ms.limit > 0) (buildOrder.map_config ||= {}).limit = ms.limit;
  else delete (buildOrder.map_config || {}).limit;

  const peaSid = DEFAULT_PEASANT[buildOrder.nation];
  const count = +$("#start_peasants").value;
  buildOrder.starting_units = { [peaSid]: count };
}

// ─── Run simulation ────────────────────────────────────────────────
async function runSim() {
  setStatus("Симулирую…", "busy");
  try {
    readControls();
    BO.save(buildOrder);
    const t0 = performance.now();
    const result = await runSimulation(buildOrder, bundle.data, bundle.tree, bundle.slots);
    const dt = performance.now() - t0;
    Charts.renderResources(result.snapshots);
    Charts.renderPop(result.snapshots);
    renderSummary(result);
    renderEvents(result.events);
    setStatus(`Готово · ${dt.toFixed(0)}мс · ${result.snapshots.length} снимков`, "ready");
  } catch (e) {
    console.error(e);
    setStatus(`Ошибка: ${e.message || e}`, "error");
  }
}

function renderSummary(result) {
  const f = result.final || {};
  const meta = result.meta || {};
  const speed = meta.gamespeed_factor || 1.4;
  const cells = RES_ORDER.map(r => {
    const v = f[`res_${r}`] ?? 0;
    return `<div class="summary-cell ${r === "gold" ? "gold" : ""} ${v < 0 ? "danger" : ""}">
      <div class="label"><span class="dot" style="background:${RES_INFO[r].color}"></span> ${RES_INFO[r].ru}</div>
      <div class="value">${v.toLocaleString("ru-RU")}</div>
    </div>`;
  }).join("");
  const buildings = Object.entries(f.buildings || {}).filter(([, v]) => v > 0).map(([k, v]) => `${k}×${v}`).join(", ") || "—";
  const meta_html = `
    <div class="summary-meta">
      <div class="pair">Время: <b>${fmtTime(f.t_g ?? 0, speed)}</b></div>
      <div class="pair">Крестьян: <b>${f.peasants_total ?? 0}</b></div>
      <div class="pair">Ферма: <b>${f.farm_used ?? 0} / ${f.farm_cap ?? 0}</b></div>
      <div class="pair">Здания: <b>${buildings}</b></div>
    </div>`;
  $("#summary").innerHTML = `<div class="summary-grid">${cells}</div>${meta_html}`;
}

function renderEvents(events) {
  const ul = $("#events_list");
  ul.innerHTML = "";
  $("#events_count").textContent = events.length;
  for (const ev of events) {
    const li = document.createElement("li");
    let cls = "info";
    if (/SKIP/i.test(ev)) cls = "skip";
    else if (/ERROR|FAIL/i.test(ev)) cls = "error";
    else if (/DEFER/i.test(ev)) cls = "defer";
    li.className = cls;
    li.textContent = ev;
    ul.appendChild(li);
  }
}

// ─── Boot ───────────────────────────────────────────────────────────
async function init() {
  setStatus("Загрузка данных…", "loading");
  bundle = await loadAll();
  setStatus(`Данные · ${bundle.data.nations.length} наций · ${bundle.data.units.length} юнитов`, "ready");

  rebuildTimeline();
  renderControls();

  // Timeline view
  TimelineView.init({
    svg: $("#timeline_svg"),
    onSelect: (action) => {
      TimelineView.setSelection(action);
      Inspector.select(action);
    },
    onChange: (action) => {
      // Triggered after drag-to-reschedule completes.
      buildOrder.actions.sort((a, b) => a.at - b.at);
      BO.save(buildOrder);
      refreshAll();
      TimelineView.setSelection(action);
      Inspector.select(action);
    },
  });

  // Inspector
  Inspector.init({
    data: bundle.data, slots: bundle.slots,
    buildOrder, timeline: currentTimeline,
    onChange: (action) => {
      buildOrder.actions.sort((a, b) => a.at - b.at);
      BO.save(buildOrder);
      refreshAll();
      TimelineView.setSelection(action);
      Inspector.select(action);  // re-render to refresh warnings
    },
    onDelete: (action) => {
      const i = buildOrder.actions.indexOf(action);
      if (i >= 0) buildOrder.actions.splice(i, 1);
      BO.save(buildOrder);
      TimelineView.setSelection(null);
      refreshAll();
    },
  });

  // Catalog
  CatalogPanel.init({
    data: bundle.data, buildOrder, timeline: currentTimeline,
    onAdd: addFromCatalog,
  });

  refreshAll();

  // Settings drawer toggle
  $("#settings_btn").addEventListener("click", () => {
    $("#settings_drawer").classList.toggle("hidden");
  });

  // Bottom-panel tab switching
  document.querySelectorAll(".bp-tab").forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".bp-tab").forEach(b => b.classList.remove("active"));
      document.querySelectorAll(".bp-pane").forEach(p => p.classList.remove("active"));
      btn.classList.add("active");
      $(`#bp_${btn.dataset.bp}`).classList.add("active");
    });
  });

  // Zoom controls
  const zoomLabel = $("#zoom_label");
  const updateZoomLabel = () => zoomLabel.textContent = `${TimelineView.getZoom().toFixed(1)} px/г-сек`;
  $("#zoom_in").addEventListener("click", () => { TimelineView.setZoom(TimelineView.getZoom() * 1.4); updateZoomLabel(); });
  $("#zoom_out").addEventListener("click", () => { TimelineView.setZoom(TimelineView.getZoom() / 1.4); updateZoomLabel(); });
  updateZoomLabel();

  // Top-bar controls
  const onChange = () => {
    readControls();
    refreshAll();
    BO.save(buildOrder);
  };
  $("#nation").addEventListener("change", () => {
    onChange();
    renderControls();
    refreshAll();
  });
  $("#max_time").addEventListener("change", onChange);
  $("#start_peasants").addEventListener("change", onChange);
  const settingIds = [
    "set_mapsize", "set_terraintype", "set_relieftype", "set_season",
    "set_resourcestart", "set_resourcemines", "set_gamespeed", "set_startingunits",
    "set_peacetime", "set_century18", "set_capture", "set_marketdip",
    "set_cannons", "set_balloon", "set_limit", "set_teams", "set_difficulty",
  ];
  for (const id of settingIds) {
    const el = $(`#${id}`);
    if (el) el.addEventListener("change", () => {
      if (id === "set_resourcestart") buildOrder._resources_customized = false;
      onChange();
      if (id === "set_resourcestart") renderControls();
    });
  }
  document.querySelectorAll("#starting_resources select").forEach(sel => {
    sel.addEventListener("change", () => {
      buildOrder._resources_customized = true;
      onChange();
    });
  });

  $("#run_sim").addEventListener("click", runSim);
  $("#export_btn").addEventListener("click", () => BO.exportToFile(buildOrder));
  $("#import_btn").addEventListener("click", () => $("#import_file").click());

  // — Import from replay (.rep) —
  let pendingReplayBytes = null;
  let pendingReplayFilename = "";
  function updateHostHint() {
    const sel = $("#replay_pid_select");
    const opt = sel?.options[sel.selectedIndex];
    const isHost = opt?.dataset.host === "true";
    const hint = $("#replay_host_hint");
    if (!hint) return;
    if (isHost) {
      hint.innerHTML = "<b>Хост.</b> Извлекутся все действия + assigns эвристически (gainres→дерево/еда/камень по фазе игры, gotomine→ближайшая по времени шахта).";
      hint.className = "muted small host-ok";
    } else {
      hint.innerHTML = "<b>Клиент.</b> В реплее нет ReadOrder-эвентов этого игрока — assigns придётся раскидать вручную в редакторе. Build/train/research/trade всё равно извлечутся.";
      hint.className = "muted small host-warn";
    }
  }
  $("#import_replay_btn").addEventListener("click", () => $("#import_replay_file").click());
  $("#import_replay_file").addEventListener("change", async (e) => {
    const f = e.target.files[0];
    if (!f) return;
    setStatus(`Читаю реплей ${f.name}…`, "busy");
    try {
      pendingReplayBytes = new Uint8Array(await f.arrayBuffer());
      pendingReplayFilename = f.name;
      const players = await listReplayPlayers(pendingReplayBytes);
      // Sort hosts first (have ReadOrder events → assigns can be extracted),
      // then by build-count desc so the most-active player surfaces on top.
      players.sort((a, b) => (b.is_host - a.is_host) || (b.n_builds - a.n_builds));
      const sel = $("#replay_pid_select");
      sel.innerHTML = players.map(p => {
        const role = p.is_host ? "хост" : "клиент";
        return `<option value="${p.pid}" data-host="${p.is_host}">${p.name || ("pid=" + p.pid)} · ${p.nation} · ${p.n_builds} построек · ${role}</option>`;
      }).join("");
      $("#replay_modal_file").textContent = f.name;
      updateHostHint();
      sel.addEventListener("change", updateHostHint);
      $("#replay_modal").classList.remove("hidden");
      setStatus("Выбери игрока", "ready");
    } catch (err) {
      console.error(err);
      setStatus(`Ошибка чтения реплея: ${err.message || err}`, "error");
    }
    e.target.value = "";  // allow re-pick of same file
  });
  $("#replay_cancel_btn").addEventListener("click", () => {
    $("#replay_modal").classList.add("hidden");
    pendingReplayBytes = null;
  });
  $("#replay_confirm_btn").addEventListener("click", async () => {
    if (!pendingReplayBytes) return;
    const pid = +$("#replay_pid_select").value;
    const windowSec = +$("#replay_window_select").value;
    $("#replay_modal").classList.add("hidden");
    setStatus(`Извлекаю стратегию из ${pendingReplayFilename}…`, "busy");
    try {
      const imported = await importReplay(pendingReplayBytes, pid, windowSec);
      buildOrder = imported;
      BO.save(buildOrder);
      renderControls();
      refreshAll();
      setStatus(`Импортировано · ${buildOrder.actions.length} действий`, "ready");
    } catch (err) {
      console.error(err);
      setStatus(`Ошибка импорта: ${err.message || err}`, "error");
    }
    pendingReplayBytes = null;
  });

  $("#import_file").addEventListener("change", async (e) => {
    if (!e.target.files[0]) return;
    buildOrder = await BO.importFromFile(e.target.files[0]);
    BO.save(buildOrder);
    renderControls();
    refreshAll();
  });
  $("#reset_btn").addEventListener("click", () => {
    if (!confirm("Сбросить билд-ордер до значений по умолчанию?")) return;
    buildOrder = BO.defaultBuildOrder(buildOrder.nation);
    BO.save(buildOrder);
    renderControls();
    refreshAll();
  });

  setStatus("Загрузка Pyodide…", "loading");
  await initPyodide(setStatus);
  $("#run_sim").disabled = false;
  setStatus("Готов · нажми «Прогнать»", "ready");
}

init().catch(e => {
  console.error(e);
  setStatus(`Ошибка: ${e.message || e}`, "error");
});
