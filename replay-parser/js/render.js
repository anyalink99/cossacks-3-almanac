// Renders one replay-result dict (returned from Python) into a card.

import { NATION_FROM_SID, NATION_BY_CID, NATION_LABEL_RU } from "./i18n.js";

const RESOURCE_NAMES_RU = ["?", "Еда", "Дерево", "Камень", "Золото", "Железо", "Уголь"];
// All label tables mirror derived/game_settings.json — the canonical source
// extracted from game scripts + locale. Keep in sync with derived dump.
const GAMESPEED_LABEL = { 0: "Медленно", 1: "Нормально", 2: "Быстро" };
const MAPSIZE_LABEL = {
  0: "Нормальный (320×320)", 1: "Большой (480×480)",
  2: "Огромный (640×640)",   3: "Маленький (256×256)",
};
const TERRAIN_LABEL = { 0: "Land", 1: "Mediterranean", 2: "Peninsulas",
                        5: "Continent", 7: "Lakes", 9: "Coastal" };
const RELIEF_LABEL = { 0: "Гладко", 1: "Лёгкий", 2: "Холмы",
                       3: "Highlands", 4: "Горы", 5: "Случайно" };
const SEASON_LABEL = { 0: "Лето", 1: "Зима", 2: "Осень", 3: "Пустыня" };
const RESOURCEMINES_LABEL = { 0: "Мало", 1: "Средне", 2: "Много" };
const RESOURCESTART_LABEL = { 0: "Обычные (1 000)", 1: "Богатые (4 000)",
                              2: "Тысячи (5 000)", 3: "Миллионы (1 000 000)" };
const PEACETIME_LABEL = {
  0: "Без времени мира", 1: "10 мин", 2: "20 мин", 3: "30 мин",
  4: "45 мин", 5: "60 мин", 6: "90 мин", 7: "2 часа", 8: "3 часа",
  9: "4 часа", 11: "15 мин",
};
const CENTURY18_LABEL = { 0: "По умолчанию", 1: "Никогда", 2: "Сразу" };
const CAPTURE_LABEL = {
  0: "По умолчанию", 1: "Без захвата крестьян",
  2: "Без захвата крестьян и центров", 3: "Только пушки",
};
const MARKETDIP_LABEL = {
  0: "По умолчанию", 1: "Без дипцентра", 2: "Без рынка",
  3: "Не доступны", 4: "Дорогие наёмники",
};
const CANNONS_LABEL = {
  0: "По умолчанию", 1: "Без пушек, башен и стен", 2: "Дорогие пушки",
};
const BALLOON_LABEL = {
  0: "По умолчанию", 1: "Без монгольфьеров", 2: "Монгольфьеры",
};
const STARTINGUNITS_LABEL = {
  0: "По умолчанию", 1: "Армия", 2: "Большая армия", 3: "Огромная армия",
  4: "Множество крестьян", 5: "Разные нации", 6: "Башни",
  7: "Пушки", 8: "Пушки и гаубицы", 9: "Казармы 18 века",
  10: "Казарма 17 в.", 11: "Деревня", 12: "Срубы", 13: "Уния",
};
const LIMIT_LABEL = {
  0: "По умолчанию", 1: "500", 2: "1000", 3: "2000",
  4: "3000", 5: "4000", 6: "5000", 7: "6000", 8: "8000",
};

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
  const lookup = (table, k) => (s[k] != null && table[s[k]] != null) ? table[s[k]] : s[k];
  const items = [
    ["Размер карты",       lookup(MAPSIZE_LABEL, "mapsize")],
    ["Ландшафт",           lookup(TERRAIN_LABEL, "terraintype")],
    ["Рельеф",             lookup(RELIEF_LABEL, "relieftype")],
    ["Сезон",              lookup(SEASON_LABEL, "season")],
    ["Шахт на карте",      lookup(RESOURCEMINES_LABEL, "resourcemines")],
    ["Стартовые ресурсы",  lookup(RESOURCESTART_LABEL, "resourcestart")],
    ["Скорость партии",    lookup(GAMESPEED_LABEL, "gamespeed")],
    ["Стартовая армия",    lookup(STARTINGUNITS_LABEL, "startingunits")],
    ["Время мира",         lookup(PEACETIME_LABEL, "peacetime")],
    ["Переход в 18 век",   lookup(CENTURY18_LABEL, "century18")],
    ["Захват",             lookup(CAPTURE_LABEL, "capture")],
    ["Рынок и дипцентр",   lookup(MARKETDIP_LABEL, "marketdip")],
    ["Пушки/башни/стены",  lookup(CANNONS_LABEL, "cannons")],
    ["Воздушные шары",     lookup(BALLOON_LABEL, "balloon")],
    ["Лимит населения",    lookup(LIMIT_LABEL, "limit")],
    ["Команды",            s.teams ? "Включены" : "Выключены"],
    ["Маска генератора",   s.maskname],
    ["randkey0",           s.randkey0],
    ["randkey1",           s.randkey1],
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

  // Sort player groups: larger groups first
  const sorted = [...byPid.entries()].sort((a, b) => b[1].length - a[1].length);

  const children = [el("h3", {}, "Обнаружена двойная прокачка")];
  for (const [pid, list] of sorted) {
    const samples = list.slice(0, 5);
    children.push(el("div", { class: "abuse-item" }, [
      el("b", {}, playerName(pid)),
      ` — ${list.length} срабатывание(й).`,
      el("ul", { class: "abuse-list" },
        samples.map((s) => {
          const d = s.details || {};
          const name = d.upgrade_name_ru || d.upgrade_name_en || d.upgrade_sid || "";
          const label = name
            ? el("b", { class: "abuse-upgname" }, name)
            : el("span", { class: "abuse-meta" },
                          `апгрейд id ${d.upgrade_id ?? d.ind ?? "?"}`);
          return el("li", {}, [
            `${fmtTime(s.ts_g_sec_first)} → ${fmtTime(s.ts_g_sec_second)} · `,
            label,
            el("span", { class: "abuse-meta" },
              ` · gap ${(s.gap_ticks / 10).toFixed(1)} g-сек`),
          ]);
        })
      ),
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
