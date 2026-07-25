// Multi-section replay workbench renderer.

import { NATION_FROM_SID, NATION_BY_CID, NATION_LABEL_RU } from "./i18n.js";

const RESOURCE_NAMES_RU = [
  "?", "Еда", "Дерево", "Камень", "Золото", "Железо", "Уголь",
];
const EVENT_LABELS = {
  build: "Строительство",
  produce: "Производство",
  upgrade: "Улучшение",
  trade: "Рынок",
  order: "Приказ",
  abuse: "Двойная прокачка",
};
const MAP_PALETTE = [
  "#87a548", "#d49a4a", "#58a6a6", "#b77a55", "#8e74ba",
  "#c6b66c", "#6791bd", "#b86f84", "#8ca486", "#c47a42",
];

let GAME_SETTINGS = null;
let PATTERN_INVENTORY = {};
let PATTERN_TYPE_BY_NAME = new Map();
let workspaceSequence = 0;

export function setGameSettings(settings) {
  GAME_SETTINGS = settings;
}

export function setPatternData(types = {}, inventory = {}) {
  PATTERN_INVENTORY = inventory || {};
  PATTERN_TYPE_BY_NAME = new Map();
  for (const [type, names] of Object.entries(types || {})) {
    for (const name of names) {
      if (!PATTERN_TYPE_BY_NAME.has(name)) PATTERN_TYPE_BY_NAME.set(name, type);
    }
  }
}

function el(tag, attrs = {}, children = []) {
  const node = document.createElement(tag);
  for (const [key, value] of Object.entries(attrs)) {
    if (value == null || value === false) continue;
    if (key === "class") node.className = value;
    else if (key === "text") node.textContent = String(value);
    else if (key === "open" && value) node.open = true;
    else if (key.startsWith("on") && typeof value === "function") {
      node.addEventListener(key.slice(2).toLowerCase(), value);
    } else if (key === "dataset") {
      Object.assign(node.dataset, value);
    } else {
      node.setAttribute(key, value === true ? "" : String(value));
    }
  }
  for (const child of [].concat(children)) {
    if (child == null) continue;
    node.appendChild(
      typeof child === "string" || typeof child === "number"
        ? document.createTextNode(String(child))
        : child,
    );
  }
  return node;
}

function svgEl(tag, attrs = {}, children = []) {
  const node = document.createElementNS("http://www.w3.org/2000/svg", tag);
  for (const [key, value] of Object.entries(attrs)) {
    node.setAttribute(key, String(value));
  }
  for (const child of children) node.appendChild(child);
  return node;
}

function fmtTime(seconds) {
  const safe = Number.isFinite(Number(seconds)) ? Number(seconds) : 0;
  const hours = Math.floor(safe / 3600);
  const minutes = Math.floor((safe % 3600) / 60);
  const secs = Math.floor(safe % 60);
  return hours
    ? `${hours}:${String(minutes).padStart(2, "0")}:${String(secs).padStart(2, "0")}`
    : `${minutes}:${String(secs).padStart(2, "0")}`;
}

function fmtBytes(bytes) {
  if (!Number.isFinite(Number(bytes))) return "—";
  if (bytes < 1024) return `${bytes} Б`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(0)} КБ`;
  return `${(bytes / 1024 / 1024).toFixed(1)} МБ`;
}

function settingLabel(key, value) {
  if (value == null) return "—";
  const options = GAME_SETTINGS?.[key];
  if (!options) return String(value);
  const option = options.find((item) => item.value === value);
  return option?.label_ru || option?.label_en || String(value);
}

function playerByPid(result, pid) {
  return (result.players || []).find((player) => player.pid === Number(pid));
}

function playerName(result, pid) {
  return playerByPid(result, pid)?.name || `pid=${pid}`;
}

function colorVar(index) {
  const safe = Math.max(0, Math.min(12, Number(index) || 0));
  return `var(--color-${safe})`;
}

function inferNation(player, builds) {
  if (typeof player?.cid === "number" && NATION_BY_CID[player.cid]) {
    return NATION_BY_CID[player.cid];
  }
  const sid = builds?.[0]?.sid || "";
  for (const [prefix, nation] of Object.entries(NATION_FROM_SID)) {
    if (sid.startsWith(prefix)) return nation;
  }
  return sid.slice(0, 3) || null;
}

function swatch(player) {
  return el("span", {
    class: "color-swatch",
    style: `background:${colorVar(player?.color ?? player?.pid ?? 0)}`,
    "aria-hidden": "true",
  });
}

function notify(message) {
  const toast = document.querySelector("#toast");
  if (!toast) return;
  toast.textContent = message;
  toast.classList.add("visible");
  clearTimeout(notify.timer);
  notify.timer = setTimeout(() => toast.classList.remove("visible"), 2600);
}

function safeStem(filename) {
  return filename
    .replace(/\.(rep|map)$/i, "")
    .replace(/[<>:"/\\|?*\x00-\x1f]/g, "_")
    .slice(0, 120) || "replay";
}

function download(filename, content, type) {
  const blob = new Blob([content], { type });
  const url = URL.createObjectURL(blob);
  const link = el("a", { href: url, download: filename });
  document.body.appendChild(link);
  link.click();
  link.remove();
  setTimeout(() => URL.revokeObjectURL(url), 0);
  notify(`Сохранён ${filename}`);
}

function csvCell(value) {
  const text = value == null ? "" : String(value);
  return `"${text.replaceAll('"', '""')}"`;
}

function toCsv(rows) {
  return `\uFEFF${rows.map((row) => row.map(csvCell).join(";")).join("\r\n")}\r\n`;
}

function patternType(name) {
  return PATTERN_TYPE_BY_NAME.get(name) || "unknown";
}

function patternColor(type) {
  let hash = 0;
  for (const char of type) hash = ((hash << 5) - hash + char.charCodeAt(0)) | 0;
  return MAP_PALETTE[Math.abs(hash) % MAP_PALETTE.length];
}

function buildTimeline(result) {
  const events = [];
  const addPerPlayer = (source, factory) => {
    for (const [pidText, items] of Object.entries(source || {})) {
      const pid = Number(pidText);
      for (const item of items || []) events.push(factory(item, pid));
    }
  };

  addPerPlayer(result.builds_per_pid, (item, pid) => ({
    ts: item.ts_g_sec,
    pid,
    type: "build",
    label: item.sid || "Неизвестная постройка",
    detail: `${item.builders ?? 0} строителей · x=${item.pos?.[0] ?? "?"}, y=${item.pos?.[1] ?? "?"}`,
  }));
  addPerPlayer(result.produces_per_pid, (item, pid) => ({
    ts: item.ts_g_sec,
    pid,
    type: "produce",
    label: item.unit_sid || `member #${item.proid}`,
    detail: `${item.start ? "заказ" : "отмена"} · ${item.infinite ? "∞" : item.amount} ед.`,
  }));
  addPerPlayer(result.upgrades_per_pid, (item, pid) => ({
    ts: item.ts_g_sec,
    pid,
    type: "upgrade",
    label: item.upgrade_name_ru || item.upgrade_name_en
      || item.upgrade_sid || `upgrade #${item.upgrade_id}`,
    detail: item.start ? "начато исследование" : "исследование отменено",
  }));
  addPerPlayer(result.trades_per_pid, (item, pid) => ({
    ts: item.ts_g_sec,
    pid,
    type: "trade",
    label: `${RESOURCE_NAMES_RU[item.sell] || item.sell} → ${RESOURCE_NAMES_RU[item.buy] || item.buy}`,
    detail: `${Number(item.amount || 0).toLocaleString("ru-RU")} ресурсов`,
  }));
  addPerPlayer(result.orders_timed_per_pid, (item, pid) => ({
    ts: item.ts_g_sec,
    pid,
    type: "order",
    label: item.ordtyp_name || `order #${item.ordtyp}`,
    detail: `${item.n_units ?? 0} юнитов${item.target_uid != null ? ` · цель ${item.target_uid}` : ""}`,
  }));
  for (const finding of result.abuses || []) {
    events.push({
      ts: finding.ts_g_sec_first,
      pid: finding.pid,
      type: "abuse",
      label: finding.details?.upgrade_name_ru
        || finding.details?.upgrade_name_en
        || finding.details?.upgrade_sid
        || "Повторная прокачка",
      detail: `${fmtTime(finding.ts_g_sec_first)} → ${fmtTime(finding.ts_g_sec_second)}`,
    });
  }
  return events.sort((a, b) => a.ts - b.ts || a.pid - b.pid);
}

function summaryText(filename, result) {
  const footer = result.footer || {};
  const lines = [
    `Cossacks 3 — отчёт по реплею`,
    `Файл: ${filename}`,
    `Сборка: ${result.replay?.build_version || "не определена"}`,
    `Длительность: ${fmtTime(result.duration_g_sec)} (${result.duration_g_sec} g-сек)`,
    `Игроков: ${(result.players || []).length}`,
    `Entry: ${result.n_entries || 0}`,
    `Sub-package: ${result.n_sub_packages || 0}`,
    `PatternList: ${(result.pattern_placements || []).length}`,
    `Карта: ${footer.map_file || "не определена"}${footer.map_width ? ` · ${footer.map_width}×${footer.map_height}` : ""}`,
    "",
    "Игроки:",
  ];
  for (const player of result.players || []) {
    const builds = result.builds_per_pid?.[player.pid] || [];
    const nation = inferNation(player, builds);
    lines.push(
      `- ${player.name || `pid=${player.pid}`} · ${NATION_LABEL_RU[nation] || nation || "нация не определена"} · team ${player.team}`,
    );
  }
  lines.push("", `Двойных прокачек: ${(result.abuses || []).length}`);
  for (const abuse of result.abuses || []) {
    const details = abuse.details || {};
    lines.push(
      `- ${playerName(result, abuse.pid)} · ${details.upgrade_name_ru || details.upgrade_sid || "неизвестное улучшение"} · ${fmtTime(abuse.ts_g_sec_first)}`,
    );
  }
  return `${lines.join("\n")}\n`;
}

function exportJson(filename, result) {
  download(
    `${safeStem(filename)}.json`,
    JSON.stringify(result, null, 2),
    "application/json;charset=utf-8",
  );
}

function exportTimeline(filename, result) {
  const rows = [[
    "time_g_sec", "time", "pid", "player", "type", "event", "details",
  ]];
  for (const event of buildTimeline(result)) {
    rows.push([
      event.ts,
      fmtTime(event.ts),
      event.pid,
      playerName(result, event.pid),
      event.type,
      event.label,
      event.detail,
    ]);
  }
  download(
    `${safeStem(filename)}-timeline.csv`,
    toCsv(rows),
    "text/csv;charset=utf-8",
  );
}

function exportPatterns(filename, result) {
  const rows = [[
    "name", "type", "x", "y", "offset", "pattern_width",
    "pattern_height", "object_count",
  ]];
  for (const placement of result.pattern_placements || []) {
    const inventory = PATTERN_INVENTORY[placement.name] || {};
    rows.push([
      placement.name,
      patternType(placement.name),
      placement.x,
      placement.y,
      placement.offset,
      inventory.width,
      inventory.height,
      inventory.object_count,
    ]);
  }
  download(
    `${safeStem(filename)}-patterns.csv`,
    toCsv(rows),
    "text/csv;charset=utf-8",
  );
}

function exportReport(filename, result) {
  download(
    `${safeStem(filename)}-report.txt`,
    summaryText(filename, result),
    "text/plain;charset=utf-8",
  );
}

function renderFacts(result, parseMs) {
  const footer = result.footer || {};
  const facts = [
    ["Ход партии", fmtTime(result.duration_g_sec), `${result.duration_g_sec} g-сек`],
    ["Состав", `${(result.players || []).length} игроков`, `${result.n_entries || 0} entry`],
    ["Команды", Number(result.n_sub_packages || 0).toLocaleString("ru-RU"), "sub-package"],
    ["Карта", footer.map_width ? `${footer.map_width}×${footer.map_height}` : "—", footer.map_file || "нет metadata"],
    ["Фрагменты карты", Number((result.pattern_placements || []).length).toLocaleString("ru-RU"), "шаблонов генератора"],
    ["Разбор", `${parseMs} мс`, result.replay?.build_version ? `build ${result.replay.build_version}` : "build неизвестен"],
  ];
  return el("dl", { class: "campaign-facts" }, facts.map(([label, value, note]) =>
    el("div", { class: "campaign-fact" }, [
      el("dt", {}, label),
      el("dd", {}, value),
      el("span", {}, note),
    ])
  ));
}

function renderSettings(settings) {
  const items = [
    ["Размер карты", settingLabel("mapsize", settings.mapsize)],
    ["Ландшафт", settingLabel("terraintype", settings.terraintype)],
    ["Рельеф", settingLabel("relieftype", settings.relieftype)],
    ["Сезон", settingLabel("season", settings.season)],
    ["Шахты", settingLabel("resourcemines", settings.resourcemines)],
    ["Стартовые ресурсы", settingLabel("resourcestart", settings.resourcestart)],
    ["Скорость", settingLabel("gamespeed", settings.gamespeed)],
    ["Стартовая армия", settingLabel("startingunits", settings.startingunits)],
    ["Время мира", settingLabel("peacetime", settings.peacetime)],
    ["XVIII век", settingLabel("century18", settings.century18)],
    ["Захват", settingLabel("capture", settings.capture)],
    ["Рынок и дипцентр", settingLabel("marketdip", settings.marketdip)],
    ["Пушки/башни/стены", settingLabel("cannons", settings.cannons)],
    ["Воздушные шары", settingLabel("balloon", settings.balloon)],
    ["Лимит", settingLabel("limit", settings.limit)],
    ["Маска", settings.maskname],
    ["randkey0", settings.randkey0],
    ["randkey1", settings.randkey1],
    ["Рейтинговая", settings.brating === "true" ? "Да" : "Нет"],
  ].filter(([, value]) => value != null && value !== "");

  return el("section", { class: "ledger-section" }, [
    el("div", { class: "section-heading" }, [
      el("p", { class: "section-kicker" }, "Условия"),
      el("h3", {}, "Настройки лобби"),
    ]),
    el("div", { class: "setting-grid" }, items.map(([label, value]) =>
      el("div", { class: "setting-item" }, [
        el("span", { class: "k" }, label),
        el("b", { class: "v" }, value),
      ])
    )),
  ]);
}

function groupAbuses(abuses) {
  const groups = new Map();
  for (const finding of abuses || []) {
    const id = finding.abuse_group_id
      || `${finding.pid}-${finding.details?.upgrade_id}-${finding.ts_g_sec_first}`;
    const group = groups.get(id) || [];
    group.push(finding);
    groups.set(id, group);
  }
  return [...groups.values()].sort(
    (a, b) => a[0].ts_g_sec_first - b[0].ts_g_sec_first,
  );
}

function renderAbuses(result) {
  const groups = groupAbuses(result.abuses);
  if (!groups.length) {
    return el("div", { class: "integrity-banner clean" }, [
      el("span", { class: "integrity-mark", "aria-hidden": "true" }, "✓"),
      el("div", {}, [
        el("b", {}, "Повторных прокачек не обнаружено"),
        el("span", {}, "Проверены ReadUpgrade и ReadApply в доступном потоке."),
      ]),
    ]);
  }

  return el("div", { class: "integrity-banner danger" }, [
    el("span", { class: "integrity-mark", "aria-hidden": "true" }, "!"),
    el("div", { class: "integrity-content" }, [
      el("b", {}, `Обнаружено эпизодов двойной прокачки: ${groups.length}`),
      el("span", {}, "Откройте строки, чтобы увидеть подтверждающие пакеты."),
      el("div", { class: "abuse-groups" }, groups.map((group) => {
        const first = group[0];
        const details = first.details || {};
        return el("details", { class: "abuse-evidence" }, [
          el("summary", {}, [
            el("span", {}, playerName(result, first.pid)),
            el("b", {}, details.upgrade_name_ru || details.upgrade_name_en
              || details.upgrade_sid || "Неизвестное улучшение"),
            el("time", {}, fmtTime(first.ts_g_sec_first)),
          ]),
          ...group.map((finding) => el("div", { class: "evidence-row" }, [
            el("span", { class: `event-tag ${finding.kind === "double-apply" ? "abuse" : "order"}` },
              finding.kind === "double-apply" ? "apply" : "клики"),
            el("span", {}, `${fmtTime(finding.ts_g_sec_first)} → ${fmtTime(finding.ts_g_sec_second)}`),
            el("span", { class: "muted" }, `gap ${(finding.gap_ticks / 10).toFixed(1)} g-сек`),
          ])),
        ]);
      })),
    ]),
  ]);
}

function renderPlayerRoster(result) {
  const rows = (result.players || []).map((player) => {
    const builds = result.builds_per_pid?.[player.pid] || [];
    const nation = inferNation(player, builds);
    return el("div", { class: "roster-row" }, [
      swatch(player),
      el("div", { class: "roster-name" }, [
        el("b", {}, player.name || `pid=${player.pid}`),
        el("span", {}, player.lanid || "LAN ID не записан"),
      ]),
      el("span", { class: "roster-nation" }, NATION_LABEL_RU[nation] || nation || "—"),
      el("span", { class: "roster-team" }, `team ${player.team}`),
    ]);
  });
  return el("section", { class: "ledger-section" }, [
    el("div", { class: "section-heading" }, [
      el("p", { class: "section-kicker" }, "Стороны"),
      el("h3", {}, "Игроки"),
    ]),
    el("div", { class: "roster" }, rows),
  ]);
}

function renderOverview(result, parseMs) {
  return el("div", { class: "overview-grid" }, [
    renderFacts(result, parseMs),
    renderAbuses(result),
    el("div", { class: "overview-columns" }, [
      renderPlayerRoster(result),
      renderSettings(result.settings || {}),
    ]),
  ]);
}

function timelineRow(result, event) {
  const player = playerByPid(result, event.pid);
  return el("div", { class: "timeline-row" }, [
    el("time", { class: "timeline-time", datetime: `PT${Math.max(0, event.ts)}S` }, fmtTime(event.ts)),
    el("div", { class: "timeline-player" }, [
      swatch(player || { pid: event.pid }),
      el("span", {}, player?.name || `pid=${event.pid}`),
    ]),
    el("span", { class: `event-tag ${event.type}` }, EVENT_LABELS[event.type] || event.type),
    el("div", { class: "timeline-event" }, [
      el("b", {}, event.label),
      el("span", {}, event.detail),
    ]),
  ]);
}

function renderTimeline(result, filename) {
  const events = buildTimeline(result);
  const panel = el("div", { class: "timeline-workbench" });
  const controls = el("div", { class: "filter-bar" });
  const playerFilter = el("select", { "aria-label": "Фильтр по игроку" }, [
    el("option", { value: "all" }, "Все игроки"),
    ...(result.players || []).map((player) =>
      el("option", { value: player.pid }, player.name || `pid=${player.pid}`)
    ),
  ]);
  const typeFilter = el("select", { "aria-label": "Фильтр по типу события" }, [
    el("option", { value: "all" }, "Все события"),
    ...Object.entries(EVENT_LABELS).map(([value, label]) =>
      el("option", { value }, label)
    ),
  ]);
  const search = el("input", {
    type: "search",
    placeholder: "Поиск по названию…",
    "aria-label": "Поиск по хронологии",
  });
  const count = el("span", { class: "filter-count" });
  const list = el("div", { class: "timeline-list" });
  const more = el("button", { class: "btn btn-secondary load-more", type: "button" }, "Показать ещё");
  let limit = 250;

  const update = () => {
    const playerValue = playerFilter.value;
    const typeValue = typeFilter.value;
    const query = search.value.trim().toLowerCase();
    const filtered = events.filter((event) => (
      (playerValue === "all" || event.pid === Number(playerValue))
      && (typeValue === "all" || event.type === typeValue)
      && (!query || `${event.label} ${event.detail} ${playerName(result, event.pid)}`
        .toLowerCase().includes(query))
    ));
    list.replaceChildren(...filtered.slice(0, limit).map((event) => timelineRow(result, event)));
    count.textContent = `${filtered.length.toLocaleString("ru-RU")} событий`;
    more.hidden = filtered.length <= limit;
    if (!filtered.length) {
      list.replaceChildren(el("div", { class: "empty-state" }, [
        el("b", {}, "По этому фильтру событий нет"),
        el("span", {}, "Измените игрока, тип события или поисковую строку."),
      ]));
    }
  };
  for (const control of [playerFilter, typeFilter, search]) {
    control.addEventListener(control === search ? "input" : "change", () => {
      limit = 250;
      update();
    });
  }
  more.addEventListener("click", () => {
    limit += 500;
    update();
  });

  controls.append(
    playerFilter,
    typeFilter,
    search,
    count,
    el("button", {
      class: "btn btn-secondary compact-btn",
      type: "button",
      onclick: () => exportTimeline(filename, result),
    }, "CSV"),
  );
  panel.append(controls, list, more);
  update();
  return panel;
}

function tallyObject(object) {
  return Object.entries(object || {}).sort((a, b) => b[1] - a[1]);
}

function miniList(items, emptyText) {
  if (!items.length) return el("p", { class: "muted" }, emptyText);
  return el("ol", { class: "mini-timeline" }, items.map((item) =>
    el("li", {}, [
      item.time != null ? el("time", {}, fmtTime(item.time)) : null,
      el("span", {}, item.label),
      item.note ? el("small", {}, item.note) : null,
    ])
  ));
}

function renderPlayers(result) {
  if (!(result.players || []).length) {
    return el("div", { class: "empty-state" }, [
      el("b", {}, "Игроки не найдены"),
      el("span", {}, "TMapPlayer-блоки отсутствуют или повреждены."),
    ]);
  }
  const cards = result.players.map((player, index) => {
    const pid = player.pid;
    const builds = result.builds_per_pid?.[pid] || [];
    const upgrades = result.upgrades_per_pid?.[pid] || [];
    const trades = result.trades_per_pid?.[pid] || [];
    const productions = result.produces_per_pid?.[pid] || [];
    const spawns = result.spawns_per_pid?.[pid] || {};
    const orders = result.orders_per_pid?.[pid] || {};
    const nation = inferNation(player, builds);
    const unitTotal = Object.values(spawns).reduce((sum, value) => sum + value, 0);

    return el("details", { class: "player-dossier", open: index === 0 }, [
      el("summary", {}, [
        swatch(player),
        el("div", { class: "dossier-title" }, [
          el("b", {}, player.name || `pid=${pid}`),
          el("span", {}, NATION_LABEL_RU[nation] || nation || "Нация не определена"),
        ]),
        el("span", {}, `${builds.length} построек`),
        el("span", {}, `${unitTotal} юнитов`),
        el("span", {}, `${upgrades.filter((item) => item.start).length} улучшений`),
      ]),
      el("div", { class: "dossier-body" }, [
        el("div", { class: "dossier-meta" }, [
          ["PID", pid],
          ["LAN ID", player.lanid || "—"],
          ["Команда", player.team],
          ["Цвет", player.color],
          ["Погибло", result.deaths_per_pid?.[pid] || 0],
          ["Сделок", trades.length],
        ].map(([label, value]) => el("div", {}, [
          el("span", {}, label),
          el("b", {}, value),
        ]))),
        el("div", { class: "dossier-columns" }, [
          el("section", {}, [
            el("h4", {}, "Build order"),
            miniList(builds.slice(0, 30).map((item) => ({
              time: item.ts_g_sec,
              label: item.sid,
              note: `${item.builders} стр.`,
            })), "Строительство не распознано."),
          ]),
          el("section", {}, [
            el("h4", {}, "Улучшения"),
            miniList(upgrades.filter((item) => item.start).slice(0, 30).map((item) => ({
              time: item.ts_g_sec,
              label: item.upgrade_name_ru || item.upgrade_name_en
                || item.upgrade_sid || `upgrade #${item.upgrade_id}`,
            })), "Улучшения не распознаны."),
          ]),
          el("section", {}, [
            el("h4", {}, "Произведено"),
            miniList(tallyObject(spawns).slice(0, 20).map(([sid, value]) => ({
              label: sid || "unknown",
              note: `×${value}`,
            })), "Появления юнитов не распознаны."),
          ]),
          el("section", {}, [
            el("h4", {}, "Приказы"),
            miniList(tallyObject(orders).slice(0, 20).map(([name, value]) => ({
              label: name,
              note: `×${value}`,
            })), productions.length
              ? `${productions.length} производственных команд`
              : "Приказы не распознаны."),
          ]),
        ]),
      ]),
    ]);
  });
  return el("div", { class: "player-dossiers" }, cards);
}

function drawPatternMap(placements, selectedInfo, boundsPlacements = placements) {
  const width = 960;
  const height = 560;
  const pad = 48;
  const xs = boundsPlacements.map((item) => Number(item.x));
  const ys = boundsPlacements.map((item) => Number(item.y));
  const minX = Math.min(...xs);
  const maxX = Math.max(...xs);
  const minY = Math.min(...ys);
  const maxY = Math.max(...ys);
  const rangeX = Math.max(1, maxX - minX);
  const rangeY = Math.max(1, maxY - minY);
  const mapX = (x) => pad + ((x - minX) / rangeX) * (width - pad * 2);
  const mapY = (y) => height - pad - ((y - minY) / rangeY) * (height - pad * 2);
  const svg = svgEl("svg", {
    class: "pattern-map",
    viewBox: `0 0 ${width} ${height}`,
    role: "img",
    "aria-label": `Карта ${placements.length} размещённых паттернов`,
  });
  svg.appendChild(svgEl("rect", {
    x: 0, y: 0, width, height, class: "map-ground",
  }));
  for (let step = 0; step <= 8; step += 1) {
    const x = pad + (step / 8) * (width - pad * 2);
    const y = pad + (step / 8) * (height - pad * 2);
    svg.append(
      svgEl("line", { x1: x, y1: pad, x2: x, y2: height - pad, class: "map-gridline" }),
      svgEl("line", { x1: pad, y1: y, x2: width - pad, y2: y, class: "map-gridline" }),
    );
  }
  svg.appendChild(svgEl("rect", {
    x: pad,
    y: pad,
    width: width - pad * 2,
    height: height - pad * 2,
    class: "map-frame",
  }));
  const axisLabels = [
    [pad, height - 18, `${minX}`],
    [width - pad, height - 18, `${maxX}`],
    [18, height - pad, `${minY}`],
    [18, pad + 5, `${maxY}`],
  ];
  for (const [x, y, label] of axisLabels) {
    const text = svgEl("text", { x, y, class: "map-axis-label" });
    text.textContent = label;
    svg.appendChild(text);
  }
  for (const placement of placements) {
    const type = patternType(placement.name);
    const circle = svgEl("circle", {
      cx: mapX(Number(placement.x)),
      cy: mapY(Number(placement.y)),
      r: placements.length > 700 ? 3.1 : 4.3,
      fill: patternColor(type),
      class: "map-point",
      tabindex: 0,
      role: "button",
      "aria-label": `${placement.name}, ${type}, x ${placement.x}, y ${placement.y}`,
    });
    const choose = () => {
      const inventory = PATTERN_INVENTORY[placement.name] || {};
      selectedInfo.replaceChildren(
        el("div", { class: "selected-pattern-title" }, [
          el("span", {
            class: "legend-dot",
            style: `background:${patternColor(type)}`,
          }),
          el("b", {}, placement.name),
          el("span", {}, type),
        ]),
        el("dl", { class: "selected-pattern-data" }, [
          ["Координаты", `${placement.x}, ${placement.y}`],
          ["Размер шаблона", inventory.width && inventory.height
            ? `${inventory.width}×${inventory.height}` : "не определён"],
          ["Объектов", inventory.object_count ?? "не определено"],
          ["Offset", `0x${Number(placement.offset).toString(16)}`],
        ].map(([key, value]) => el("div", {}, [
          el("dt", {}, key),
          el("dd", {}, value),
        ]))),
      );
    };
    circle.addEventListener("click", choose);
    circle.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        choose();
      }
    });
    const title = svgEl("title");
    title.textContent = `${placement.name} · ${type} · (${placement.x}, ${placement.y})`;
    circle.appendChild(title);
    svg.appendChild(circle);
  }
  return svg;
}

function placementStats(placements) {
  const stats = {
    forests: 0,
    stones: 0,
    gold: 0,
    iron: 0,
    coal: 0,
    objects: 0,
  };
  for (const placement of placements) {
    const type = patternType(placement.name).toLowerCase();
    if (type.includes("forest")) stats.forests += 1;
    if (type.includes("stone")) stats.stones += 1;
    if (type === "mng" || type.endsWith("_mng")) stats.gold += 1;
    if (type === "mni" || type.endsWith("_mni")) stats.iron += 1;
    if (type === "mnc" || type.endsWith("_mnc")) stats.coal += 1;
    stats.objects += Number(PATTERN_INVENTORY[placement.name]?.object_count || 0);
  }
  return stats;
}

function renderMap(result, filename) {
  const placements = result.pattern_placements || [];
  if (!placements.length) {
    return el("div", { class: "empty-state" }, [
      el("b", {}, "Данные генерации карты не найдены"),
      el("span", {}, "Проверьте раздел «Диагностика»: PatternList может отсутствовать или иметь другую версию формата."),
    ]);
  }

  const types = new Map();
  for (const placement of placements) {
    const type = patternType(placement.name);
    types.set(type, (types.get(type) || 0) + 1);
  }
  const sortedTypes = [...types.entries()].sort((a, b) => b[1] - a[1]);
  const typeFilter = el("select", { "aria-label": "Группа фрагмента карты" }, [
    el("option", { value: "all" }, "Все группы"),
    ...sortedTypes.map(([type, number]) =>
      el("option", { value: type }, `${type} · ${number}`)
    ),
  ]);
  const search = el("input", {
    type: "search",
    placeholder: "Имя шаблона…",
    "aria-label": "Поиск шаблона карты",
  });
  const count = el("span", { class: "filter-count" });
  const plot = el("div", { class: "map-canvas" });
  const table = el("div", { class: "pattern-table" });
  const selectedInfo = el("aside", { class: "selected-pattern" }, [
    el("b", {}, "Нажмите на точку"),
    el("span", {}, "Покажем имя шаблона, его размеры, координаты и положение внутри файла."),
  ]);

  const update = () => {
    const typeValue = typeFilter.value;
    const query = search.value.trim().toLowerCase();
    const filtered = placements.filter((placement) => (
      (typeValue === "all" || patternType(placement.name) === typeValue)
      && (!query || placement.name.toLowerCase().includes(query))
    ));
    count.textContent = `${filtered.length.toLocaleString("ru-RU")} точек`;
    if (filtered.length) {
      plot.replaceChildren(drawPatternMap(filtered, selectedInfo, placements));
    } else {
      plot.replaceChildren(el("div", { class: "empty-state" }, [
        el("b", {}, "Совпадений нет"),
        el("span", {}, "Сбросьте тип или строку поиска."),
      ]));
    }
    table.replaceChildren(
      ...filtered.slice(0, 200).map((placement) => {
        const type = patternType(placement.name);
        return el("div", { class: "pattern-row" }, [
          el("span", {
            class: "legend-dot",
            style: `background:${patternColor(type)}`,
          }),
          el("b", {}, placement.name),
          el("span", {}, type),
          el("code", {}, `${placement.x}, ${placement.y}`),
        ]);
      }),
      filtered.length > 200
        ? el("p", { class: "table-note" }, `Показаны первые 200 из ${filtered.length}. Полный список доступен в CSV.`)
        : null,
    );
  };
  typeFilter.addEventListener("change", update);
  search.addEventListener("input", update);

  const legend = el("div", { class: "map-legend" }, sortedTypes.slice(0, 12).map(([type, number]) =>
    el("span", {}, [
      el("i", { style: `background:${patternColor(type)}` }),
      el("b", {}, type),
      ` ${number}`,
    ])
  ));
  const stats = placementStats(placements);
  const statStrip = el("dl", { class: "map-stat-strip" }, [
    ["Лесные кластеры", stats.forests],
    ["Каменные кластеры", stats.stones],
    ["Залежи золота", stats.gold],
    ["Залежи железа", stats.iron],
    ["Залежи угля", stats.coal],
    ["Объектов внутри", stats.objects],
  ].map(([label, value]) => el("div", {}, [
    el("dt", {}, label),
    el("dd", {}, Number(value).toLocaleString("ru-RU")),
  ])));
  const root = el("div", { class: "map-workbench" }, [
    el("section", { class: "map-explainer" }, [
      el("span", { class: "map-explainer-mark", "aria-hidden": "true" }, "✥"),
      el("div", {}, [
        el("p", { class: "section-kicker" }, "Как читать схему"),
        el("h3", {}, "Каждая точка — готовый фрагмент случайной карты"),
        el("p", {},
          "При генерации игра раскладывает шаблоны окружения: группы деревьев и камней, залежи золота, железа и угля, элементы рельефа и декор. Цвет показывает группу шаблона, а положение точки — его координаты в системе генератора."),
        el("small", {},
          "Это не маршрут игроков и не карта отдельных юнитов или ресурсов."),
      ]),
    ]),
    el("div", { class: "filter-bar" }, [
      typeFilter,
      search,
      count,
      el("button", {
        class: "btn btn-secondary compact-btn",
        type: "button",
        onclick: () => exportPatterns(filename, result),
      }, "CSV"),
    ]),
    legend,
    statStrip,
    el("div", { class: "map-layout" }, [
      el("div", {}, [
        plot,
        el("p", { class: "map-note" },
          "Координаты относятся к целому шаблону окружения, а не к объектам внутри него."),
      ]),
      selectedInfo,
    ]),
    el("details", { class: "pattern-ledger" }, [
      el("summary", {}, "Реестр размещённых фрагментов"),
      table,
    ]),
  ]);
  update();
  return root;
}

function dataRows(rows) {
  return el("dl", { class: "diagnostic-data" }, rows
    .filter(([, value]) => value != null && value !== "")
    .map(([label, value]) => el("div", {}, [
      el("dt", {}, label),
      el("dd", {}, value),
    ])));
}

function renderDiagnostics(result) {
  const replay = result.replay || {};
  const footer = result.footer || {};
  const warnings = result.format_warnings || [];
  const handlerRows = Object.entries(result.by_handler || {})
    .sort((a, b) => b[1] - a[1]);
  const playerRows = Object.entries(result.by_pid || {})
    .sort((a, b) => b[1] - a[1]);

  return el("div", { class: "diagnostics-grid" }, [
    el("section", { class: "diagnostic-card wide" }, [
      el("p", { class: "section-kicker" }, "Совместимость"),
      warnings.length
        ? el("ul", { class: "warning-list" }, warnings.map((warning) =>
            el("li", {}, warning)
          ))
        : el("div", { class: "diagnostic-ok" }, "Структурных предупреждений нет."),
    ]),
    el("section", { class: "diagnostic-card" }, [
      el("p", { class: "section-kicker" }, "Файл"),
      el("h3", {}, "OSWMap"),
      dataRows([
        ["Формат", replay.map_format_version ? `OSWMap${replay.map_format_version}` : "—"],
        ["Сборка", replay.build_version || "—"],
        ["UID", replay.uid || "—"],
        ["Размер", fmtBytes(replay.file_size)],
        ["Entry", result.n_entries],
        ["Sub-package", result.n_sub_packages],
      ]),
    ]),
    el("section", { class: "diagnostic-card" }, [
      el("p", { class: "section-kicker" }, "Футер"),
      el("h3", {}, footer.complete ? "GameMapEnd найден" : "Неполные данные"),
      dataRows([
        ["Map-файл", footer.map_file],
        ["Размер карты", footer.map_width ? `${footer.map_width}×${footer.map_height}` : null],
        ["Map flags", footer.map_flags],
        ["Project", footer.project_path],
        ["Config", footer.menu_config],
        ["Состояние", footer.player_state],
        ["elapsed_raw_s", footer.elapsed_raw_s?.toFixed?.(6)],
        ["RecordEnd offset", footer.record_end_offset != null
          ? `0x${footer.record_end_offset.toString(16)}` : null],
      ]),
      footer.elapsed_raw_s != null
        ? el("p", { class: "technical-note" },
            "elapsed_raw_s не равен игровому времени; точная семантика часов пока не установлена.")
        : null,
    ]),
    el("section", { class: "diagnostic-card" }, [
      el("p", { class: "section-kicker" }, "Обработчики"),
      el("h3", {}, `${handlerRows.length} типов`),
      el("div", { class: "diagnostic-bars" }, handlerRows.slice(0, 30).map(([name, value]) =>
        el("div", {}, [
          el("code", {}, name),
          el("span", {}, Number(value).toLocaleString("ru-RU")),
        ])
      )),
    ]),
    el("section", { class: "diagnostic-card" }, [
      el("p", { class: "section-kicker" }, "Поток игроков"),
      el("h3", {}, `${playerRows.length} источников`),
      el("div", { class: "diagnostic-bars" }, playerRows.map(([name, value]) =>
        el("div", {}, [
          el("span", {}, name),
          el("span", {}, Number(value).toLocaleString("ru-RU")),
        ])
      )),
    ]),
  ]);
}

function exportCard(title, description, meta, action, label) {
  return el("article", { class: "export-card" }, [
    el("div", { class: "export-seal", "aria-hidden": "true" }, title.slice(0, 1)),
    el("div", {}, [
      el("h3", {}, title),
      el("p", {}, description),
      el("span", {}, meta),
    ]),
    el("button", {
      class: "btn btn-primary",
      type: "button",
      onclick: action,
    }, label),
  ]);
}

function renderExport(filename, result) {
  const timelineCount = buildTimeline(result).length;
  const patternCount = (result.pattern_placements || []).length;
  const report = summaryText(filename, result);
  return el("div", { class: "export-grid" }, [
    exportCard(
      "Полный JSON",
      "Все разобранные поля без сокращений: игроки, события, футер, PatternList и диагностика.",
      `${fmtBytes(new Blob([JSON.stringify(result)]).size)} данных`,
      () => exportJson(filename, result),
      "Скачать JSON",
    ),
    exportCard(
      "Хронология CSV",
      "Плоская таблица строительства, производства, улучшений, рынка и приказов.",
      `${timelineCount.toLocaleString("ru-RU")} строк`,
      () => exportTimeline(filename, result),
      "Скачать CSV",
    ),
    exportCard(
      "Шаблоны карты CSV",
      "Все размещённые фрагменты карты: имя, группа, координаты, размеры и число объектов.",
      `${patternCount.toLocaleString("ru-RU")} строк`,
      () => exportPatterns(filename, result),
      "Скачать CSV",
    ),
    exportCard(
      "Краткий отчёт",
      "Читаемая текстовая сводка для сообщения, заметки или архива партии.",
      `${report.split("\n").length} строк`,
      () => exportReport(filename, result),
      "Скачать TXT",
    ),
    exportCard(
      "Скопировать сводку",
      "Тот же краткий отчёт сразу попадёт в буфер обмена.",
      "UTF-8 · обычный текст",
      async () => {
        try {
          await navigator.clipboard.writeText(report);
          notify("Сводка скопирована");
        } catch {
          notify("Браузер запретил доступ к буферу обмена");
        }
      },
      "Копировать",
    ),
  ]);
}

function configureTabs(workspace) {
  const tabs = [...workspace.querySelectorAll('[role="tab"]')];
  const panels = [...workspace.querySelectorAll('[role="tabpanel"]')];
  const activate = (tab) => {
    for (const item of tabs) {
      const active = item === tab;
      item.setAttribute("aria-selected", active ? "true" : "false");
      item.tabIndex = active ? 0 : -1;
    }
    for (const panel of panels) {
      panel.hidden = panel.id !== tab.getAttribute("aria-controls");
    }
  };
  tabs.forEach((tab, index) => {
    tab.addEventListener("click", () => activate(tab));
    tab.addEventListener("keydown", (event) => {
      let target = null;
      if (event.key === "ArrowRight") target = tabs[(index + 1) % tabs.length];
      if (event.key === "ArrowLeft") target = tabs[(index - 1 + tabs.length) % tabs.length];
      if (event.key === "Home") target = tabs[0];
      if (event.key === "End") target = tabs[tabs.length - 1];
      if (target) {
        event.preventDefault();
        activate(target);
        target.focus();
      }
    });
  });
  activate(tabs[0]);
}

function replayMetrics(result) {
  const sumLengths = (source) => Object.values(source || {})
    .reduce((sum, items) => sum + (items?.length || 0), 0);
  const unitCount = Object.values(result.spawns_per_pid || {})
    .reduce(
      (sum, tally) => sum + Object.values(tally || {})
        .reduce((inner, value) => inner + Number(value || 0), 0),
      0,
    );
  return {
    builds: sumLengths(result.builds_per_pid),
    units: unitCount,
    upgrades: Object.values(result.upgrades_per_pid || {})
      .reduce(
        (sum, items) => sum + (items || []).filter((item) => item.start).length,
        0,
      ),
    trades: sumLengths(result.trades_per_pid),
    abuses: groupAbuses(result.abuses).length,
  };
}

function exportComparison(replays) {
  const rows = [[
    "file", "duration_g_sec", "players", "map_width", "map_height",
    "patterns", "builds", "units", "upgrades", "trades", "abuses",
  ]];
  for (const replay of replays) {
    const result = replay.result;
    const footer = result.footer || {};
    const metrics = replayMetrics(result);
    rows.push([
      replay.filename,
      result.duration_g_sec,
      (result.players || []).length,
      footer.map_width,
      footer.map_height,
      (result.pattern_placements || []).length,
      metrics.builds,
      metrics.units,
      metrics.upgrades,
      metrics.trades,
      metrics.abuses,
    ]);
  }
  download(
    "replay-comparison.csv",
    toCsv(rows),
    "text/csv;charset=utf-8",
  );
}

export function renderComparison(replays) {
  const tableRows = replays.map((replay) => {
    const result = replay.result;
    const footer = result.footer || {};
    const metrics = replayMetrics(result);
    return el("tr", {}, [
      el("th", { scope: "row" }, [
        el("b", {}, replay.filename),
        el("span", {}, result.replay?.build_version
          ? `build ${result.replay.build_version}` : "build неизвестен"),
      ]),
      el("td", {}, fmtTime(result.duration_g_sec)),
      el("td", { class: "num" }, (result.players || []).length),
      el("td", {}, footer.map_width ? `${footer.map_width}×${footer.map_height}` : "—"),
      el("td", { class: "num" }, (result.pattern_placements || []).length),
      el("td", { class: "num" }, metrics.builds),
      el("td", { class: "num" }, metrics.units),
      el("td", { class: "num" }, metrics.upgrades),
      el("td", { class: "num" }, metrics.trades),
      el("td", { class: metrics.abuses ? "num danger-text" : "num" }, metrics.abuses),
    ]);
  });
  return el("div", {}, [
    el("header", { class: "comparison-header" }, [
      el("div", {}, [
        el("p", { class: "section-kicker" }, "Несколько партий"),
        el("h2", {}, "Сравнение открытых реплеев"),
        el("p", {}, "Сопоставление длительности, активности игроков и генерации карты."),
      ]),
      el("button", {
        class: "btn btn-secondary",
        type: "button",
        onclick: () => exportComparison(replays),
      }, "Скачать CSV"),
    ]),
    el("div", { class: "comparison-scroll" }, [
      el("table", { class: "comparison-table" }, [
        el("thead", {}, [
          el("tr", {}, [
            "Реплей", "Время", "Игроки", "Карта", "Фрагменты",
            "Постройки", "Юниты", "Улучшения", "Сделки", "Абуз",
          ].map((label) => el("th", { scope: "col" }, label))),
        ]),
        el("tbody", {}, tableRows),
      ]),
    ]),
  ]);
}

export function renderCard(filename, result, parseMs, options = {}) {
  const id = `replay-${++workspaceSequence}`;
  const tabs = [
    ["overview", "Сводка", null],
    ["timeline", "Хронология", buildTimeline(result).length],
    ["players", "Игроки", (result.players || []).length],
    ["map", "Генерация карты", (result.pattern_placements || []).length],
    ["diagnostics", "Диагностика", (result.format_warnings || []).length || null],
    ["export", "Экспорт", null],
  ];
  const contents = {
    overview: renderOverview(result, parseMs),
    timeline: renderTimeline(result, filename),
    players: renderPlayers(result),
    map: renderMap(result, filename),
    diagnostics: renderDiagnostics(result),
    export: renderExport(filename, result),
  };
  const workspace = el("article", { class: "replay-workspace card" }, [
    el("header", { class: "workspace-header" }, [
      el("div", { class: "workspace-title" }, [
        el("p", { class: "section-kicker" }, "Открытый реплей"),
        el("h2", {}, filename),
        el("p", {}, [
          `${fmtTime(result.duration_g_sec)} · `,
          `${(result.players || []).length} игроков · `,
          `${Number(result.n_sub_packages || 0).toLocaleString("ru-RU")} пакетов`,
        ]),
      ]),
      el("div", { class: "workspace-actions" }, [
        el("button", {
          class: "btn btn-secondary",
          type: "button",
          onclick: () => exportJson(filename, result),
        }, "JSON"),
        el("button", {
          class: "workspace-close",
          type: "button",
          title: "Закрыть реплей",
          "aria-label": `Закрыть ${filename}`,
          onclick: () => {
            workspace.remove();
            options.onClose?.();
          },
        }, "×"),
      ]),
    ]),
    el("nav", {
      class: "workspace-tabs",
      role: "tablist",
      "aria-label": `Разделы реплея ${filename}`,
    }, tabs.map(([key, label, badge], index) =>
      el("button", {
        id: `${id}-tab-${key}`,
        class: "workspace-tab",
        type: "button",
        role: "tab",
        "aria-controls": `${id}-panel-${key}`,
        "aria-selected": index === 0 ? "true" : "false",
        tabindex: index === 0 ? 0 : -1,
      }, [
        el("span", {}, label),
        badge != null ? el("small", {}, Number(badge).toLocaleString("ru-RU")) : null,
      ])
    )),
    ...tabs.map(([key]) =>
      el("section", {
        id: `${id}-panel-${key}`,
        class: `workspace-panel panel-${key}`,
        role: "tabpanel",
        "aria-labelledby": `${id}-tab-${key}`,
      }, contents[key])
    ),
  ]);
  configureTabs(workspace);
  return workspace;
}
