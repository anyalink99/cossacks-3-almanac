// Renders one replay-result dict (returned from Python) into a card.

import { NATION_FROM_SID, NATION_BY_CID, NATION_LABEL_RU } from "./i18n.js";

const RESOURCE_NAMES_RU = ["?", "Еда", "Дерево", "Камень", "Золото", "Железо", "Уголь"];

// Canonical labels for every lobby/map enum. Populated at boot from
// derived/game_settings.json (which is itself extracted from game scripts +
// locale). Until that fetch lands we fall back to numeric values.
let GAME_SETTINGS = null;
export function setGameSettings(gs) { GAME_SETTINGS = gs; }

function settingLabel(key, value) {
  if (value == null) return "—";
  const opts = GAME_SETTINGS?.[key];
  if (!opts) return String(value);
  const opt = opts.find((o) => o.value === value);
  return opt?.label_ru || opt?.label_en || String(value);
}

const COLOR_VAR = (i) => `var(--color-${Math.max(0, Math.min(12, i))})`;

function el(tag, attrs = {}, children = []) {
  const e = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === "class") e.className = v;
    else if (k === "html") e.innerHTML = v;
    else if (k.startsWith("on") && typeof v === "function") e[k] = v;
    else e.setAttribute(k, v);
  }
  for (const c of [].concat(children)) {
    if (c == null) continue;
    e.appendChild(typeof c === "string" ? document.createTextNode(c) : c);
  }
  return e;
}

function fmtTime(g_sec) {
  const m = Math.floor(g_sec / 60);
  const s = Math.floor(g_sec % 60);
  return `${m}:${s.toString().padStart(2, "0")}`;
}

function inferNation(player, builds) {
  // Primary source: TMapPlayer.cid from the .rep header. cid 0..23 maps to
  // a real nation. cid 24 = empty slot, cid -2 = "random — pick at game
  // start" (we then fall back to the first ReadConstruct's cid / sid
  // prefix).
  const cid = player?.cid;
  if (typeof cid === "number" && NATION_BY_CID[cid]) {
    return NATION_BY_CID[cid];
  }
  if (!builds || !builds.length) return null;
  const sid = builds[0].sid || "";
  for (const [prefix, nation] of Object.entries(NATION_FROM_SID)) {
    if (sid.startsWith(prefix)) return nation;
  }
  return sid.slice(0, 3) || null;
}

function renderSettings(s) {
  const items = [
    ["Размер карты",       settingLabel("mapsize",       s.mapsize)],
    ["Ландшафт",           settingLabel("terraintype",   s.terraintype)],
    ["Рельеф",             settingLabel("relieftype",    s.relieftype)],
    ["Сезон",              settingLabel("season",        s.season)],
    ["Шахт на карте",      settingLabel("resourcemines", s.resourcemines)],
    ["Стартовые ресурсы",  settingLabel("resourcestart", s.resourcestart)],
    ["Скорость партии",    settingLabel("gamespeed",     s.gamespeed)],
    ["Стартовая армия",    settingLabel("startingunits", s.startingunits)],
    ["Время мира",         settingLabel("peacetime",     s.peacetime)],
    ["Переход в 18 век",   settingLabel("century18",     s.century18)],
    ["Захват",             settingLabel("capture",       s.capture)],
    ["Рынок и дипцентр",   settingLabel("marketdip",     s.marketdip)],
    ["Пушки/башни/стены",  settingLabel("cannons",       s.cannons)],
    ["Воздушные шары",     settingLabel("balloon",       s.balloon)],
    ["Лимит населения",    settingLabel("limit",         s.limit)],
    ["Команды",            s.teams ? "Включены" : "Выключены"],
    ["Маска генератора",   s.maskname],
    ["randkey0",           s.randkey0],
    ["randkey1",           s.randkey1],
    ["Рейтинговая",        s.brating === "true" ? "Да" : "Нет"],
    ["Битва (вспомог.)",   s.bbattle === "true" ? "Да" : "Нет"],
    ["DLC bitmask",        s.dlcs],
    ["Автосохранение",     s.autosave],
    ["Помощник советника", s.adviserassistant],
  ];
  const grid = el("div", { class: "setting-grid" },
    items.filter(([_, v]) => v != null && v !== "").map(([k, v]) =>
      el("div", { class: "setting-item" }, [
        el("div", { class: "k" }, String(k)),
        el("div", { class: "v" }, String(v)),
      ])
    )
  );
  return el("section", { class: "section" }, [
    el("h3", {}, "Настройки лобби"),
    grid,
  ]);
}

function renderPlayers(players, buildsPerPid) {
  const rows = players.map((p) => {
    const nation = inferNation(p, buildsPerPid[p.pid]);
    const nationLabel = nation ? (NATION_LABEL_RU[nation] || nation) : "—";
    const swatch = el("span", { class: "color-swatch",
                                 style: `background:${COLOR_VAR(p.color)};` });
    const nick = el("span", { class: "player-nick" }, p.name || `pid=${p.pid}`);
    const nationEl = el("span", { class: "player-nation" }, nationLabel);
    const lanid = el("span", { class: "lanid" }, p.lanid || "—");
    const team = el("span", { class: "team-label" }, `team ${p.team}`);
    return el("div", { class: "player-row" }, [swatch, nationEl, nick, lanid, team]);
  });
  return el("section", { class: "section" }, [
    el("h3", {}, "Игроки"),
    ...rows,
  ]);
}

function renderAbuses(abuses, players) {
  if (!abuses || !abuses.length) {
    return el("div", { class: "abuses-clean" }, "Двойных прокачек не обнаружено.");
  }
  const playerName = (pid) => {
    const p = players.find((p) => p.pid === pid);
    return p ? p.name : `pid=${pid}`;
  };

  // Group by (pid, abuse_group_id). A real race-condition abuse produces
  // TWO findings — one `double-upgrade-start` (click pair) and one
  // `double-apply` (commit pair) — sharing the same abuse_group_id and
  // describing the same underlying incident. We collapse them into one
  // card so the UI doesn't show what looks like two abuses.
  const byPid = new Map();
  for (const ab of abuses) {
    const groups = byPid.get(ab.pid) || new Map();
    const gid = ab.abuse_group_id || `${ab.pid}-${ab.kind}-${ab.ts_g_sec_first}`;
    const list = groups.get(gid) || [];
    list.push(ab);
    groups.set(gid, list);
    byPid.set(ab.pid, groups);
  }

  // Order findings inside a group: start before apply (chronological).
  for (const groups of byPid.values()) {
    for (const list of groups.values()) {
      list.sort((a, b) => a.ts_g_sec_first - b.ts_g_sec_first);
    }
  }

  // Sort players: more groups first.
  const sortedPids = [...byPid.entries()]
    .sort((a, b) => b[1].size - a[1].size);

  const children = [el("h3", {}, "Обнаружена двойная прокачка")];
  for (const [pid, groups] of sortedPids) {
    // Sort each player's groups by the earliest timestamp.
    const sortedGroups = [...groups.values()]
      .sort((a, b) => a[0].ts_g_sec_first - b[0].ts_g_sec_first);

    children.push(el("div", { class: "abuse-item" }, [
      el("b", {}, playerName(pid)),
      ` — ${sortedGroups.length} прокачк${sortedGroups.length === 1 ? "а" : "и"}.`,
      el("ul", { class: "abuse-list" },
        sortedGroups.map((group) => renderAbuseGroup(group))),
    ]));
  }
  return el("div", { class: "abuses-found" }, children);
}

function renderAbuseGroup(group) {
  // `group` is an array of 1 or 2 findings sharing an abuse_group_id.
  // Pair (start + apply) is the normal real-abuse case; solo apply is
  // ground truth without a matching click pattern.
  const d = group[0].details || {};
  const name = d.upgrade_name_ru || d.upgrade_name_en || d.upgrade_sid || "";
  const nameNode = name
    ? el("b", { class: "abuse-upgname" }, name)
    : el("span", { class: "abuse-meta" },
                  `апгрейд id ${d.upgrade_id ?? d.ind ?? "?"}`);

  const lines = group.map((s) => {
    const kindLabel = s.kind === "double-upgrade-start" ? "клики" : "применения";
    const kindClass = s.kind === "double-upgrade-start" ? "abuse-tag-click" : "abuse-tag-apply";
    return el("div", { class: "abuse-row" }, [
      el("span", { class: `abuse-tag ${kindClass}` }, kindLabel),
      el("span", { class: "abuse-row-ts" },
        ` ${fmtTime(s.ts_g_sec_first)} → ${fmtTime(s.ts_g_sec_second)}`),
      el("span", { class: "abuse-meta" },
        ` · gap ${(s.gap_ticks / 10).toFixed(1)} g-сек`),
    ]);
  });

  const soloHint = group.length === 1 && group[0].kind === "double-apply"
    ? el("span", { class: "abuse-meta abuse-solo-hint" },
        " · только apply (клики не разделились в кластеры)")
    : null;

  return el("li", { class: "abuse-group" }, [
    nameNode,
    soloHint,
    el("div", { class: "abuse-rows" }, lines),
  ]);
}

function renderBuildSummary(buildsPerPid, players) {
  const rows = [];
  for (const [pidStr, builds] of Object.entries(buildsPerPid)) {
    if (!builds.length) continue;
    const pid = Number(pidStr);
    const player = players.find((p) => p.pid === pid);
    const name = player ? player.name : `pid=${pid}`;
    const colorBg = COLOR_VAR(player?.color ?? pid);
    // Top buildings
    const tally = new Map();
    for (const b of builds) tally.set(b.sid, (tally.get(b.sid) || 0) + 1);
    const topList = Array.from(tally.entries())
      .sort((a, b) => b[1] - a[1])
      .slice(0, 8)
      .map(([sid, c]) => `${sid} ×${c}`)
      .join(", ");
    const first3 = builds.slice(0, 3).map((b) => `${b.sid}@${fmtTime(b.ts_g_sec)}`).join(", ");
    rows.push(el("div", { class: "player-breakdown" }, [
      el("div", { class: "player-breakdown-head" }, [
        el("span", { class: "color-swatch", style: `background:${colorBg};` }),
        el("span", {}, name),
        el("span", { class: "lanid" }, `${builds.length} построек`),
      ]),
      el("div", { class: "player-breakdown-stats" }, [
        el("div", {}, [el("b", {}, "Топ: "), topList || "—"]),
        el("div", {}, [el("b", {}, "Первые: "), first3 || "—"]),
      ]),
    ]));
  }
  if (!rows.length) return null;
  return el("section", { class: "section" }, [
    el("h3", {}, "Строительство"),
    ...rows,
  ]);
}

function renderProductionSummary(spawnsPerPid, players) {
  const rows = [];
  for (const [pidStr, spawns] of Object.entries(spawnsPerPid)) {
    const pid = Number(pidStr);
    const player = players.find((p) => p.pid === pid);
    if (!player) continue;
    const total = Object.values(spawns).reduce((a, b) => a + b, 0);
    if (!total) continue;
    const colorBg = COLOR_VAR(player.color ?? pid);
    const topList = Object.entries(spawns)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 10)
      .map(([sid, c]) => `${sid} ×${c}`)
      .join(", ");
    rows.push(el("div", { class: "player-breakdown" }, [
      el("div", { class: "player-breakdown-head" }, [
        el("span", { class: "color-swatch", style: `background:${colorBg};` }),
        el("span", {}, player.name),
        el("span", { class: "lanid" }, `${total} юнитов`),
      ]),
      el("div", { class: "player-breakdown-stats" }, [
        el("div", {}, [el("b", {}, "Топ: "), topList]),
      ]),
    ]));
  }
  if (!rows.length) return null;
  return el("section", { class: "section" }, [
    el("h3", {}, "Производство юнитов"),
    ...rows,
  ]);
}

function renderTrades(tradesPerPid, players) {
  const all = [];
  for (const [pidStr, trades] of Object.entries(tradesPerPid)) {
    const pid = Number(pidStr);
    for (const t of trades) all.push({ pid, ...t });
  }
  if (!all.length) return null;
  // Aggregate sell→buy
  const pairs = new Map();
  for (const t of all) {
    const key = `${RESOURCE_NAMES_RU[t.sell] || t.sell}→${RESOURCE_NAMES_RU[t.buy] || t.buy}`;
    pairs.set(key, (pairs.get(key) || 0) + t.amount);
  }
  const rows = Array.from(pairs.entries())
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10)
    .map(([k, v]) => el("tr", {}, [
      el("td", {}, k),
      el("td", { class: "num" }, String(v.toLocaleString("ru-RU"))),
    ]));
  return el("section", { class: "section" }, [
    el("h3", {}, `Рынок (${all.length} сделок)`),
    el("table", { class: "compact" }, [
      el("thead", {}, [el("tr", {}, [el("th", {}, "Обмен"), el("th", {}, "Объём")])]),
      el("tbody", {}, rows),
    ]),
  ]);
}


export function renderCard(filename, result, parseMs) {
  const settings = result.settings || {};
  const players = result.players || [];
  const meta = [];
  meta.push(`${result.duration_g_sec.toFixed(0)} g-сек (${fmtTime(result.duration_g_sec)})`);
  meta.push(`${players.length} игр.`);
  meta.push(`${result.n_sub_packages.toLocaleString("ru-RU")} sub-pkg`);
  meta.push(`распарсено за ${parseMs} мс`);

  const card = el("div", { class: "replay-card" }, [
    el("div", { class: "card-header" }, [
      el("div", {}, [
        el("h2", { class: "card-title" }, filename),
        el("div", { class: "card-meta" }, meta.join(" · ")),
      ]),
    ]),
    el("div", { class: "card-body" }, [
      renderAbuses(result.abuses, players),
      renderPlayers(players, result.builds_per_pid || {}),
      renderSettings(settings),
      renderBuildSummary(result.builds_per_pid || {}, players),
      renderProductionSummary(result.spawns_per_pid || {}, players),
      renderTrades(result.trades_per_pid || {}, players),
    ]),
  ]);
  return card;
}
