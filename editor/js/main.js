import { loadAll } from "./data_loader.js";
import { initPyodide, runSimulation } from "./pyodide_runner.js";
import * as BO from "./build_order.js";
import * as Charts from "./ui/charts.js";
import * as ActionList from "./ui/action_list.js";
import * as ActionForm from "./ui/action_form.js";
import { upgradesForNation } from "./ui/catalog.js";
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
let lookupCtx = null;

function rebuildLookups() {
  if (!bundle) return;
  const nation = buildOrder.nation;
  const byBuildingSid = new Map(bundle.data.buildings.filter(b => b.nation === nation).map(b => [b.sid, b]));
  const byUnitSid = new Map(bundle.data.units.filter(u => u.nation === nation).map(u => [u.sid, u]));
  const ups = upgradesForNation(bundle.data, nation);
  const byUpgradeSid = new Map(ups.map(u => [u.sid, u]));
  lookupCtx = { byBuildingSid, byUnitSid, byUpgradeSid, gameSpeed: buildOrder.game_speed || "fast" };
  ActionForm.bindContext(bundle.data, bundle.slots, buildOrder);
}

// Populate a dropdown from a list of {value, label_ru, label_en, ...extras}
function fillSelect(elId, list, currentValue, extraText = (x) => "") {
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

  // Nation dropdown
  const natSel = $("#nation");
  natSel.innerHTML = "";
  for (const n of bundle.data.nations) {
    const opt = document.createElement("option");
    opt.value = n.sid;
    opt.textContent = `${(n.name_ru || n.name_en || n.sid)}`;
    if (n.sid === buildOrder.nation) opt.selected = true;
    natSel.appendChild(opt);
  }
  $("#max_time").value = String(buildOrder.max_time_sec || 900);

  // Map settings (gen.*) — directly from game_settings.json
  fillSelect("set_mapsize",       settings.mapsize,       ms.mapsize       ?? settings.defaults.gen.mapsize,
             (x) => `(${x.tiles}×${x.tiles})`);
  fillSelect("set_terraintype",   settings.terraintype,   ms.terraintype   ?? settings.defaults.gen.terraintype);
  fillSelect("set_relieftype",    settings.relieftype,    ms.relieftype    ?? settings.defaults.gen.relieftype);
  fillSelect("set_season",        settings.season,        ms.season        ?? settings.defaults.gen.season);
  fillSelect("set_resourcestart", settings.resourcestart, ms.resourcestart ?? settings.defaults.gen.resourcestart,
             (x) => `· ${x.amount.toLocaleString("ru-RU")} ед.`);
  fillSelect("set_resourcemines", settings.resourcemines, ms.resourcemines ?? settings.defaults.gen.resourcemines);

  // Additional (rules)
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

  // Peasants dropdown
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

  // Per-resource fine control (collapsed by default — most users use resourcestart preset)
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
      ? `<option value="${val}" selected>${val.toLocaleString("ru-RU")} (своё)</option>`
      : "";
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

  // Map / additional settings — store the enum values verbatim
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

  // Translate gamespeed enum (0/1/2) to legacy string for the simulator
  buildOrder.game_speed = ["slow", "normal", "fast"][ms.gamespeed] || "fast";

  // Translate resourcestart preset to actual numeric resources, if user hasn't customized
  const rsPreset = bundle.settings.resourcestart.find(x => x.value === ms.resourcestart);
  if (rsPreset && !buildOrder._resources_customized) {
    buildOrder.starting_resources = {
      food: rsPreset.amount, wood: rsPreset.amount, stone: rsPreset.amount,
      gold: rsPreset.amount, iron: rsPreset.amount, coal: rsPreset.amount,
    };
  } else {
    // Use per-resource overrides from the (collapsed) detail view
    const sr = buildOrder.starting_resources || {};
    document.querySelectorAll("#starting_resources select[data-res]").forEach(sel => {
      sr[sel.dataset.res] = +sel.value;
    });
    buildOrder.starting_resources = sr;
  }

  // Translate `limit` enum to map_config.limit (1..8) — simulator already supports it
  if (ms.limit > 0) (buildOrder.map_config ||= {}).limit = ms.limit;
  else delete (buildOrder.map_config || {}).limit;

  // Peasants
  const peaSid = DEFAULT_PEASANT[buildOrder.nation];
  const count = +$("#start_peasants").value;
  buildOrder.starting_units = { [peaSid]: count };
}

function renderActions() {
  ActionList.render(buildOrder.actions, lookupCtx, (i) => {
    buildOrder.actions.splice(i, 1);
    BO.save(buildOrder);
    renderActions();
    ActionForm.refresh();
  });
}

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
  const buildings = Object.entries(f.buildings || {}).filter(([k, v]) => v > 0).map(([k, v]) => `${k}×${v}`).join(", ") || "—";
  const meta_html = `
    <div class="summary-meta">
      <div class="pair">Время: <b>${fmtTime(f.t_g ?? 0, speed)}</b></div>
      <div class="pair">Крестьян: <b>${f.peasants_total ?? 0}</b></div>
      <div class="pair">Ферма: <b>${f.farm_used ?? 0} / ${f.farm_cap ?? 0}</b></div>
      <div class="pair">Здания: <b>${buildings}</b></div>
    </div>
  `;
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

async function init() {
  setStatus("Загрузка данных…", "loading");
  bundle = await loadAll();
  setStatus(`Данные · ${bundle.data.nations.length} наций · ${bundle.data.units.length} юнитов`, "ready");

  rebuildLookups();
  renderControls();
  renderActions();

  ActionForm.init((action) => {
    buildOrder.actions.push(action);
    buildOrder.actions.sort((a, b) => a.at - b.at);
    BO.save(buildOrder);
    renderActions();
    ActionForm.refresh();
  });

  const onChange = () => {
    readControls();
    rebuildLookups();
    renderActions();
    BO.save(buildOrder);
    ActionForm.refresh();
  };
  $("#nation").addEventListener("change", () => {
    onChange();
    renderControls();  // peasant dropdown depends on nation
    rebuildLookups();
    ActionForm.refresh();
  });
  $("#max_time").addEventListener("change", onChange);
  $("#start_peasants").addEventListener("change", onChange);

  // Wire all the map/rules settings dropdowns
  const settingIds = [
    "set_mapsize", "set_terraintype", "set_relieftype", "set_season",
    "set_resourcestart", "set_resourcemines", "set_gamespeed", "set_startingunits",
    "set_peacetime", "set_century18", "set_capture", "set_marketdip",
    "set_cannons", "set_balloon", "set_limit", "set_teams", "set_difficulty",
  ];
  for (const id of settingIds) {
    const el = $(`#${id}`);
    if (el) el.addEventListener("change", () => {
      // Changing resourcestart resets per-resource customization
      if (id === "set_resourcestart") buildOrder._resources_customized = false;
      onChange();
      // resourcestart change cascades into the visible per-resource fields
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
  $("#import_file").addEventListener("change", async (e) => {
    if (!e.target.files[0]) return;
    buildOrder = await BO.importFromFile(e.target.files[0]);
    BO.save(buildOrder);
    rebuildLookups();
    renderControls();
    renderActions();
    ActionForm.refresh();
  });
  $("#reset_btn").addEventListener("click", () => {
    if (!confirm("Сбросить билд-ордер до значений по умолчанию?")) return;
    buildOrder = BO.defaultBuildOrder(buildOrder.nation);
    BO.save(buildOrder);
    rebuildLookups();
    renderControls();
    renderActions();
    ActionForm.refresh();
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
