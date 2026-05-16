// Bottom-panel inspector: shows the currently-selected action's editable
// fields (time, builders/amount, etc.) and a delete button.

import { fmtName, fmtCost, RES_ORDER, RES_INFO, KIND_INFO, buildingClusterFor } from "./i18n.js";
import { maxBuildersFor } from "./catalog.js";

let _state = {
  data: null, slots: null, buildOrder: null, timeline: null,
  selected: null,
  onChange: () => {},
  onDelete: () => {},
};

export function init({ data, slots, buildOrder, timeline, onChange, onDelete }) {
  _state.data = data; _state.slots = slots;
  _state.buildOrder = buildOrder; _state.timeline = timeline;
  _state.onChange = onChange || (() => {});
  _state.onDelete = onDelete || (() => {});
}

export function bind(buildOrder, timeline) {
  _state.buildOrder = buildOrder; _state.timeline = timeline;
  render();
}

export function select(action) {
  _state.selected = action;
  render();
  // Auto-flip to inspector tab
  const tab = document.querySelector(".bp-tab[data-bp='inspector']");
  if (tab && !tab.classList.contains("active")) tab.click();
}

function render() {
  const root = document.querySelector("#bp_inspector");
  if (!root) return;
  const a = _state.selected;
  if (!a || !_state.buildOrder?.actions?.includes(a)) {
    _state.selected = null;
    root.innerHTML = `<div class="inspector-empty muted">Кликни по точке на таймлайне или добавь действие из левого каталога.</div>`;
    return;
  }
  root.innerHTML = bodyHtml(a);
  wire(root, a);
}

function bodyHtml(a) {
  const k = KIND_INFO[a.do] || { ru: a.do, short: "?", color: "#888" };
  const title = titleFor(a);
  return `
    <div class="inspector">
      <div class="inspector-head">
        <span class="kind-pill" style="background:${k.color}20;color:${k.color}">${k.ru}</span>
        <span class="title">${title}</span>
        <div class="actions">
          <button id="ins_delete" class="btn btn-ghost btn-sm">Удалить</button>
        </div>
      </div>
      <div class="inspector-fields">${fieldsHtml(a)}</div>
      ${warnHtml(a)}
    </div>
  `;
}

function titleFor(a) {
  if (a.do === "build") {
    const b = _state.data.buildings.find(x => x.sid === a.sid && x.nation === _state.buildOrder.nation);
    return b ? `Построить: ${fmtName(b)}` : `Построить: ${a.sid}`;
  }
  if (a.do === "train") {
    const u = _state.data.units.find(x => x.sid === a.unit_sid && x.nation === _state.buildOrder.nation);
    return `Обучить ${a.amount}× ${u ? fmtName(u) : a.unit_sid}`;
  }
  if (a.do === "train_infinite") {
    const u = _state.data.units.find(x => x.sid === a.unit_sid && x.nation === _state.buildOrder.nation);
    return `Беск. производство: ${u ? fmtName(u) : a.unit_sid}`;
  }
  if (a.do === "research") {
    const up = _state.data.upgrades.find(x => x.sid === a.upgrade_sid && x.nation === _state.buildOrder.nation);
    return `Исследовать: ${up ? fmtName(up) : a.upgrade_sid}`;
  }
  if (a.do === "assign") return "Раскидать крестьян";
  if (a.do === "trade") return `Обмен: ${a.amount} ${RES_INFO[a.sell]?.ru} → ${RES_INFO[a.buy]?.ru}`;
  return a.do;
}

function fieldsHtml(a) {
  const tField = `
    <label class="field">
      <span>Время начала (г-сек)</span>
      <input type="number" id="ins_at" value="${+a.at || 0}" min="0" max="3600" step="5" />
    </label>`;
  if (a.do === "build") {
    const max = maxBuildersFor(_state.data, _state.slots, a.sid, _state.timeline, +a.at || 0);
    return `
      ${tField}
      <label class="field">
        <span>Строителей <span class="hint">макс. ${max}</span></span>
        <input type="number" id="ins_builders" value="${+a.builders || 1}" min="1" max="30" />
      </label>
    `;
  }
  if (a.do === "train" || a.do === "train_infinite") {
    const isInf = a.do === "train_infinite";
    return `
      ${tField}
      <label class="field">
        <span>Количество</span>
        <input type="number" id="ins_amount" value="${+a.amount || 1}" min="1" max="500" ${isInf ? "disabled" : ""} />
      </label>
      <label class="field">
        <span>Режим</span>
        <label class="toggle-inline">
          <input type="checkbox" id="ins_infinite" ${isInf ? "checked" : ""} />
          <span>Бесконечно (∞)</span>
        </label>
      </label>
    `;
  }
  if (a.do === "research") {
    return tField;
  }
  if (a.do === "assign") {
    const total = _state.timeline.peasantsAt(+a.at || 0);
    const cells = RES_ORDER.map(r => `
      <label class="field">
        <span><span class="dot" style="background:${RES_INFO[r].color}"></span> ${RES_INFO[r].ru}</span>
        <input type="number" data-res="${r}" value="${+a[r] || 0}" min="0" max="500" />
      </label>
    `).join("");
    return `
      ${tField}
      ${cells}
      <div class="field hint" style="grid-column: 1 / -1;">К этому времени крестьян всего: ${total}</div>
    `;
  }
  if (a.do === "trade") {
    const resOpts = (sel) => RES_ORDER.map(r =>
      `<option value="${r}" ${sel === r ? "selected" : ""}>${RES_INFO[r].ru}</option>`
    ).join("");
    return `
      ${tField}
      <label class="field">
        <span>Продать</span>
        <select id="ins_sell">${resOpts(a.sell)}</select>
      </label>
      <label class="field">
        <span>Купить</span>
        <select id="ins_buy">${resOpts(a.buy)}</select>
      </label>
      <label class="field">
        <span>Кол-во</span>
        <input type="number" id="ins_amount" value="${+a.amount || 0}" min="1" max="1000000" step="10" />
      </label>
    `;
  }
  return tField;
}

function warnHtml(a) {
  const warns = [];
  // Build action: builders > free peasants at action's time
  if (a.do === "build") {
    const t = +a.at || 0;
    const free = _state.timeline.freePeasantsAt(t, a);
    const req = +a.builders || 1;
    if (req > free) {
      warns.push(`Запрошено ${req} строителей, на t=${t}г свободно ${free} крестьян. Симулятор автоматически снизит до ${Math.max(1, free)}.`);
    }
  }
  // Trade: market built?
  if (a.do === "trade") {
    const cluster = buildingClusterFor(_state.buildOrder.nation, "mar");
    const marketSid = cluster + "mar";
    const e = _state.timeline.earliestForOne(marketSid);
    const t = +a.at || 0;
    if (!isFinite(e) || e > t) {
      warns.push(`Рынок (${marketSid}) недоступен в t=${t}г. ` + (isFinite(e) ? `Действие отложится до t=${Math.round(e)}г.` : `Запланируй постройку рынка.`));
    }
  }
  if (!warns.length) return "";
  return warns.map(w => `<div class="inspector-warn">⚠ ${w}</div>`).join("");
}

function wire(root, action) {
  root.querySelector("#ins_delete")?.addEventListener("click", () => {
    _state.onDelete(action);
  });
  const atInp = root.querySelector("#ins_at");
  atInp?.addEventListener("change", () => {
    action.at = Math.max(0, +atInp.value || 0);
    _state.onChange(action);
  });
  const buildersInp = root.querySelector("#ins_builders");
  buildersInp?.addEventListener("change", () => {
    action.builders = Math.max(1, +buildersInp.value || 1);
    _state.onChange(action);
  });
  const amountInp = root.querySelector("#ins_amount");
  amountInp?.addEventListener("change", () => {
    action.amount = Math.max(1, +amountInp.value || 1);
    _state.onChange(action);
  });
  const infChk = root.querySelector("#ins_infinite");
  infChk?.addEventListener("change", () => {
    if (infChk.checked) {
      action.do = "train_infinite";
      delete action.amount;
    } else {
      action.do = "train";
      action.amount = 5;
    }
    _state.onChange(action);
  });
  root.querySelectorAll("input[data-res]").forEach(inp => {
    inp.addEventListener("change", () => {
      action[inp.dataset.res] = Math.max(0, +inp.value || 0);
      _state.onChange(action);
    });
  });
  const sellSel = root.querySelector("#ins_sell");
  sellSel?.addEventListener("change", () => {
    action.sell = sellSel.value;
    _state.onChange(action);
  });
  const buySel = root.querySelector("#ins_buy");
  buySel?.addEventListener("change", () => {
    action.buy = buySel.value;
    _state.onChange(action);
  });
}
