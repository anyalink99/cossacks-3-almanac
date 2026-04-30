// Renders the list of actions as nice cards, no emojis.

import { KIND_INFO, RES_ORDER, RES_INFO, fmtName, fmtTime } from "./i18n.js";

export function render(actions, ctx, onDelete) {
  const ol = document.querySelector("#actions_list");
  ol.innerHTML = "";
  document.querySelector("#actions_count").textContent = actions.length;
  const speed = { slow: 0.7, normal: 1.0, fast: 1.4 }[ctx.gameSpeed || "fast"] || 1.4;
  actions.forEach((a, i) => {
    const li = document.createElement("li");
    li.className = "action-card";
    li.dataset.kind = a.do;
    const k = KIND_INFO[a.do] || { ru: a.do, short: "?", color: "#888" };
    const { title, sub } = describe(a, ctx);
    li.innerHTML = `
      <span class="kind-tag" style="--c:${k.color}">${k.short}</span>
      <div class="body">
        <div class="title">${title}</div>
        <div class="sub">${sub}</div>
      </div>
      <span class="time">${fmtTime(a.at, speed)}</span>
      <button class="del" data-i="${i}" title="Удалить">×</button>
    `;
    ol.appendChild(li);
  });
  ol.querySelectorAll(".del").forEach(btn => {
    btn.addEventListener("click", e => onDelete(+e.target.dataset.i));
  });
}

function describe(a, ctx) {
  const { byBuildingSid, byUnitSid, byUpgradeSid } = ctx;
  if (a.do === "build") {
    const b = byBuildingSid?.get(a.sid);
    const cost = b ? RES_ORDER.map(r => b[r] ? `${RES_INFO[r].short}${b[r]}` : null).filter(Boolean).join(" ") : "";
    return {
      title: `Построить: ${b ? fmtName(b) : a.sid}`,
      sub: `строителей ${a.builders ?? 1}` + (cost ? ` · ${cost}` : ""),
    };
  }
  if (a.do === "train") {
    const u = byUnitSid?.get(a.unit_sid);
    const b = byBuildingSid?.get(a.building_sid);
    return {
      title: `Обучить ${a.amount}× ${u ? fmtName(u) : a.unit_sid}`,
      sub: `в здании ${b ? fmtName(b) : a.building_sid}`,
    };
  }
  if (a.do === "research") {
    const u = byUpgradeSid?.get(a.upgrade_sid);
    return {
      title: `Исследовать: ${u ? fmtName(u) : a.upgrade_sid}`,
      sub: u && u.__place_ru ? `в ${u.__place_ru}` : a.upgrade_sid,
    };
  }
  if (a.do === "assign") {
    const parts = [];
    for (const r of RES_ORDER) {
      if (a[r]) parts.push(`<span class="res-tag" style="--c:${RES_INFO[r].color}"><span class="dot"></span>${a[r]}</span>`);
    }
    return {
      title: `Раскидать крестьян`,
      sub: parts.length ? parts.join(" ") : "(пусто)",
    };
  }
  return { title: a.do, sub: JSON.stringify(a) };
}
