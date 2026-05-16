// Renders one replay-result dict (returned from Python) into a card.

import { NATION_FROM_SID, NATION_LABEL_RU } from "./i18n.js";

const RESOURCE_NAMES_RU = ["?", "Еда", "Дерево", "Камень", "Золото", "Железо", "Уголь"];
const GAMESPEED_LABEL = { 0: "Медленно", 1: "Нормально", 2: "Быстро" };
const MAPSIZE_LABEL = { 0: "Малая", 1: "Средняя", 2: "Большая", 3: "Огромная" };
const TERRAIN_LABEL = { 0: "Land", 1: "Mediterranean", 2: "Peninsulas",
                        5: "Continent", 7: "Lakes", 9: "Coastal" };
const RELIEF_LABEL = { 0: "Гладко", 1: "Лёгкий", 2: "Холмы", 3: "Highlands", 4: "Горы", 5: "Случайно" };
const SEASON_LABEL = { 0: "Лето", 1: "Зима", 2: "Осень", 3: "Пустыня" };
const RESOURCEMINES_LABEL = { 0: "Мало", 1: "Средне", 2: "Много" };

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

function inferNation(builds) {
  // First ReadConstruct sid tells us the player's nation prefix.
  if (!builds || !builds.length) return null;
  const sid = builds[0].sid;
  // Match by NATION_FROM_SID prefix table; otherwise return first 3 chars
  for (const [prefix, nation] of Object.entries(NATION_FROM_SID)) {
    if (sid.startsWith(prefix)) return nation;
  }
  return sid.slice(0, 3);
}

function renderSettings(s) {
  const items = [
    ["Размер карты", MAPSIZE_LABEL[s.mapsize] ?? s.mapsize],
    ["Ландшафт", TERRAIN_LABEL[s.terraintype] ?? s.terraintype],
    ["Рельеф", RELIEF_LABEL[s.relieftype] ?? s.relieftype],
    ["Шахты", RESOURCEMINES_LABEL[s.resourcemines] ?? s.resourcemines],
    ["Сезон", SEASON_LABEL[s.season] ?? s.season],
    ["Скорость", GAMESPEED_LABEL[s.gamespeed] ?? s.gamespeed],
    ["Лимит", s.limit],
    ["Маска", s.maskname],
    ["randkey0", s.randkey0],
    ["randkey1", s.randkey1],
    ["Команды", s.teams ? "Включены" : "Выключены"],
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
    const nation = inferNation(buildsPerPid[p.pid]);
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
    return el("div", { class: "abuses-clean" }, "Подозрительных действий не обнаружено.");
  }
  // Group by pid
  const byPid = new Map();
  for (const ab of abuses) {
    const list = byPid.get(ab.pid) || [];
    list.push(ab);
    byPid.set(ab.pid, list);
  }
  const playerName = (pid) => {
    const p = players.find((p) => p.pid === pid);
    return p ? p.name : `pid=${pid}`;
  };

  const children = [
    el("h3", {}, "Обнаружены подозрительные действия"),
  ];
  for (const [pid, list] of byPid) {
    children.push(el("div", { class: "abuse-item" }, [
      el("span", { class: "abuse-kind" }, list[0].kind),
      el("b", {}, playerName(pid)),
      ` — ${list.length} попадание(й). Первое: ${fmtTime(list[0].ts_g_sec_first)}, ` +
      `повтор: ${fmtTime(list[0].ts_g_sec_second)} (gap ${list[0].gap_ticks} ticks).`,
    ]));
  }
  return el("div", { class: "abuses-found" }, children);
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

function renderCombat(result, players) {
  const deaths = result.deaths_per_pid || {};
  const proj = result.proj_per_pid || {};
  const totalDeaths = Object.values(deaths).reduce((a, b) => a + b, 0);
  const totalProj = Object.values(proj).reduce((a, b) => a + b, 0);
  if (!totalDeaths && !totalProj) return null;
  const rows = players.map((p) => {
    const d = deaths[p.pid] || 0;
    const sh = proj[p.pid] || 0;
    return el("tr", {}, [
      el("td", {}, [
        el("span", { class: "color-swatch",
                     style: `background:${COLOR_VAR(p.color)};vertical-align:middle;margin-right:8px;` }),
        el("span", {}, p.name),
      ]),
      el("td", { class: "num" }, String(d)),
      el("td", { class: "num" }, String(sh)),
    ]);
  });
  return el("section", { class: "section" }, [
    el("h3", {}, "Боевая активность"),
    el("table", { class: "compact" }, [
      el("thead", {}, [el("tr", {}, [
        el("th", {}, "Игрок"), el("th", {}, "Потери"), el("th", {}, "Выстрелов"),
      ])]),
      el("tbody", {}, rows),
    ]),
  ]);
}

function renderOrdersSummary(ordersPerPid, players) {
  const rows = players.map((p) => {
    const orders = ordersPerPid[p.pid] || {};
    const total = Object.values(orders).reduce((a, b) => a + b, 0);
    if (!total) return null;
    const breakdown = Object.entries(orders)
      .sort((a, b) => b[1] - a[1])
      .map(([k, v]) => `${k}=${v}`)
      .join(" · ");
    return el("tr", {}, [
      el("td", {}, [
        el("span", { class: "color-swatch",
                     style: `background:${COLOR_VAR(p.color)};vertical-align:middle;margin-right:8px;` }),
        el("span", {}, p.name),
      ]),
      el("td", { class: "num" }, String(total)),
      el("td", {}, breakdown),
    ]);
  }).filter((x) => x);
  if (!rows.length) return null;
  return el("section", { class: "section" }, [
    el("h3", {}, "Приказы"),
    el("table", { class: "compact" }, [
      el("thead", {}, [el("tr", {}, [
        el("th", {}, "Игрок"), el("th", {}, "Всего"), el("th", {}, "Разбивка"),
      ])]),
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
      renderOrdersSummary(result.orders_per_pid || {}, players),
      renderCombat(result, players),
      renderTrades(result.trades_per_pid || {}, players),
    ]),
  ]);
  return card;
}
