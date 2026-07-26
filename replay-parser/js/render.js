// Multi-section replay workbench renderer.

import {
  NATION_FROM_SID,
  NATION_BY_CID,
  NATION_LABEL_RU,
  NATION_LABEL_EN,
} from "./i18n.js";
import { language, localizeTree, tr } from "../../assets/js/runtime-i18n.js";

const NUMBER_LOCALE = language === "en" ? "en-US" : "ru-RU";
const NATION_LABELS = language === "en" ? NATION_LABEL_EN : NATION_LABEL_RU;

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
const ORDER_LABELS_RU = {
  none: "Без приказа",
  move: "Перемещение",
  attackobj: "Атака объекта",
  gainres: "Добыча ресурсов",
  produce: "Производство юнита",
  patrol: "Патрулирование",
  attackpoint: "Огонь по точке",
  continueattackpoint: "Продолжение огня по точке",
  performupgrade: "Исследование улучшения",
  fishing: "Рыболовство",
  creategates: "Постройка ворот",
  buildwallcontinue: "Продолжение постройки стены",
  buildwall: "Постройка стены",
  gotomine: "Отправка в шахту",
  gototransport: "Посадка на транспорт",
  leavetransport: "Высадка из транспорта",
  leavebuilding: "Выход из здания",
  build: "Строительство здания",
  guard: "Охрана",
  repair: "Ремонт",
  exitunits: "Выход из гарнизона",
};
const HANDLER_LABELS_RU = {
  ReadConstruct: "Строительство",
  ReadNew: "Появление объектов",
  ReadNewP: "Создание объектов",
  ReadOrder: "Приказы юнитам",
  ReadRally: "Точки сбора",
  ReadApply: "Применение улучшений",
  ReadUpgrade: "Исследование улучшений",
  ReadSearch: "Поиск цели",
  ReadStand: "Остановка",
  ReadStop: "Отмена приказов",
  ReadProduce: "Производство юнитов",
  ReadPlayer: "Состояние игроков",
  ReadDeath: "Потери",
  ReadSyncUnitsParams: "Синхронизация параметров",
  ReadTrade: "Торговля",
  ReadTradeResources: "Обмен ресурсов",
  ReadLeave: "Выход из объекта",
  ReadGate: "Управление воротами",
  ReadLeaveOrder: "Отмена очереди",
  ReadFree: "Удаление объектов",
  ReadProjFree: "Удаление снарядов",
  ReadPeaceTime: "Время мира",
  ReadPackage: "Вложенные события",
  ReadProj: "Выстрелы",
  ReadFreeList: "Очистка списка объектов",
  ReadWall: "Строительство стен",
  ReadMove: "Перемещение",
  class_09_sync: "Синхронизация состояния",
  tiny_residue: "Служебные остаточные данные",
};
const PATTERN_TYPE_LABELS_RU = {
  unknown: "Прочие фрагменты",
  mng: "Золотые шахты",
  mni: "Железные шахты",
  mnc: "Угольные шахты",
  stoneforests: "Камни и лес",
  stones: "Каменные залежи",
  mountains: "Горы",
  plateau_big: "Большие плато",
  plain_huge: "Огромные равнины",
  plain_big: "Большие равнины",
  plain_medium: "Средние равнины",
  plain_small: "Малые равнины",
  hills_dark: "Тёмные холмы",
  swamp_small: "Малые болота",
};
const ENTITY_OVERRIDES_RU = {
  chaika: "Чайка",
  field: "Поле",
  unitbox: "Служебный объект",
};
const MAP_PALETTE = [
  "#87a548", "#d49a4a", "#58a6a6", "#b77a55", "#8e74ba",
  "#c6b66c", "#6791bd", "#b86f84", "#8ca486", "#c47a42",
];

let GAME_SETTINGS = null;
let CANONICAL_TERMS = {};
let PATTERN_INVENTORY = {};
let PATTERN_TYPE_BY_NAME = new Map();
let workspaceSequence = 0;

export function setGameSettings(settings) {
  GAME_SETTINGS = settings;
}

export function setCanonicalTerms(terms = {}) {
  CANONICAL_TERMS = terms || {};
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

function cleanCanonicalName(record) {
  const label = record?.[language] || record?.en || record?.ru || "";
  if (!label || label.startsWith("#") || label.includes("INCLUDES TEMPLATES")) {
    return null;
  }
  return label;
}

function canonicalUnitName(sid) {
  const key = String(sid || "").trim().toLowerCase();
  if (!key) return "Неизвестный юнит";
  return cleanCanonicalName(CANONICAL_TERMS.units?.[key])
    || ENTITY_OVERRIDES_RU[key]
    || "Неизвестный юнит";
}

function canonicalBuildingName(sid) {
  const key = String(sid || "").trim().toLowerCase();
  if (!key) return "Неизвестная постройка";

  // A few nation-specific building labels live in the locale's shared
  // object table and therefore appear under canonical `units`.
  const exact = cleanCanonicalName(CANONICAL_TERMS.units?.[key]);
  if (exact) return exact;

  const suffix = Object.keys(CANONICAL_TERMS.buildings || {})
    .sort((a, b) => b.length - a.length)
    .find((candidate) => key.endsWith(candidate));
  return cleanCanonicalName(CANONICAL_TERMS.buildings?.[suffix])
    || "Неизвестная постройка";
}

function canonicalEntityName(sid) {
  const key = String(sid || "").trim().toLowerCase();
  if (!key) return "Неизвестный объект";
  const unit = cleanCanonicalName(CANONICAL_TERMS.units?.[key]);
  if (unit) return unit;
  if (ENTITY_OVERRIDES_RU[key]) return ENTITY_OVERRIDES_RU[key];
  const building = canonicalBuildingName(key);
  return building === "Неизвестная постройка" ? "Неизвестный объект" : building;
}

function canonicalUpgradeName(item = {}) {
  if (language === "en" && item.upgrade_name_en) return item.upgrade_name_en;
  if (item.upgrade_name_ru) return item.upgrade_name_ru;

  const sid = String(item.upgrade_sid || "").trim().toLowerCase();
  if (sid) {
    const names = CANONICAL_TERMS.upgrade_names || {};
    const candidates = [
      sid,
      sid.length > 3 ? `%nat%${sid.slice(3)}` : null,
      sid.length > 3 ? `%com%${sid.slice(3)}` : null,
    ].filter(Boolean);
    for (const candidate of candidates) {
      const label = cleanCanonicalName(names[candidate]);
      if (label) return label;
    }
  }
  return item.upgrade_id != null
    ? `Улучшение №${item.upgrade_id}`
    : "Неизвестное улучшение";
}

function orderLabel(name, id = null) {
  const key = String(name || "").trim().toLowerCase();
  if (ORDER_LABELS_RU[key]) return ORDER_LABELS_RU[key];
  const unknown = key.match(/^unknown_(\d+)$/);
  const number = unknown?.[1] ?? id;
  return number != null ? `Неизвестный приказ №${number}` : "Неизвестный приказ";
}

function handlerLabel(name) {
  if (HANDLER_LABELS_RU[name]) return HANDLER_LABELS_RU[name];
  if (String(name).startsWith("engine_")) return "Внутренние события игры";
  if (String(name).startsWith("unknown_")) return "Неизвестные события";
  if (String(name).startsWith("decode_error_")) return "Ошибки чтения событий";
  return "Прочие события";
}

function patternTypeLabel(type) {
  const key = String(type || "unknown").toLowerCase();
  if (PATTERN_TYPE_LABELS_RU[key]) return PATTERN_TYPE_LABELS_RU[key];

  const size = key.includes("huge") ? "Огромные"
    : key.includes("big") ? "Большие"
      : key.includes("medium") || key.includes("_mid") ? "Средние"
        : key.includes("small") ? "Малые" : "";
  if (key.includes("forest") || key.includes("frt")) {
    const kind = key.includes("pinefir") ? "сосново-пихтовые леса"
      : key.includes("spruce") ? "еловые леса"
        : key.includes("pine") ? "сосновые леса" : "лесные массивы";
    return `${size} ${kind}`.trim();
  }
  if (key.includes("mountain") || key.includes("mnt")) return `${size} горы`.trim();
  if (key.includes("plateau") || key.includes("plt")) return `${size} плато`.trim();
  if (key.includes("plain")) return `${size} равнины`.trim();
  if (key.includes("hill")) return `${size} холмы`.trim();
  if (key.includes("swamp")) return `${size} болота`.trim();
  return "Прочие фрагменты";
}

function pluralRu(value, forms) {
  if (language === "en") {
    const english = {
      строитель: ["builder", "builders"],
      юнит: ["unit", "units"],
      игрок: ["player", "players"],
      событие: ["event", "events"],
      постройка: ["building", "buildings"],
      улучшение: ["upgrade", "upgrades"],
      точка: ["point", "points"],
      категория: ["category", "categories"],
      источник: ["source", "sources"],
    }[forms[0]] || [forms[0], `${forms[0]}s`];
    return Number(value) === 1 ? english[0] : english[1];
  }
  const number = Math.abs(Number(value)) % 100;
  const tail = number % 10;
  if (number > 10 && number < 20) return forms[2];
  if (tail === 1) return forms[0];
  if (tail >= 2 && tail <= 4) return forms[1];
  return forms[2];
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
  return option?.[`label_${language}`] || option?.label_en || option?.label_ru || String(value);
}

function playerByPid(result, pid) {
  return (result.players || []).find((player) => player.pid === Number(pid));
}

function playerName(result, pid) {
  return playerByPid(result, pid)?.name || `Игрок ${pid}`;
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
  if (language === "en" && (type.startsWith("text/") || type.includes("csv"))) {
    content = tr(content);
  }
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
    label: canonicalBuildingName(item.sid),
    detail: `${item.builders ?? 0} ${pluralRu(item.builders ?? 0, ["строитель", "строителя", "строителей"])} · координаты ${item.pos?.[0] ?? "?"}, ${item.pos?.[1] ?? "?"}`,
  }));
  addPerPlayer(result.produces_per_pid, (item, pid) => ({
    ts: item.ts_g_sec,
    pid,
    type: "produce",
    label: canonicalUnitName(item.unit_sid),
    detail: `${item.start ? "Заказано" : "Заказ отменён"} · ${item.infinite ? "∞" : `${item.amount} ед.`}`,
  }));
  addPerPlayer(result.upgrades_per_pid, (item, pid) => ({
    ts: item.ts_g_sec,
    pid,
    type: "upgrade",
    label: canonicalUpgradeName(item),
    detail: item.start ? "Исследование начато" : "Исследование отменено",
  }));
  addPerPlayer(result.trades_per_pid, (item, pid) => ({
    ts: item.ts_g_sec,
    pid,
    type: "trade",
    label: `${RESOURCE_NAMES_RU[item.sell] || item.sell} → ${RESOURCE_NAMES_RU[item.buy] || item.buy}`,
    detail: `${Number(item.amount || 0).toLocaleString(NUMBER_LOCALE)} ресурсов`,
  }));
  addPerPlayer(result.orders_timed_per_pid, (item, pid) => ({
    ts: item.ts_g_sec,
    pid,
    type: "order",
    label: orderLabel(item.ordtyp_name, item.ordtyp),
    detail: `${item.n_units ?? 0} ${pluralRu(item.n_units ?? 0, ["юнит", "юнита", "юнитов"])}${item.target_uid != null ? " · цель указана" : ""}`,
  }));
  for (const finding of result.abuses || []) {
    events.push({
      ts: finding.ts_g_sec_first,
      pid: finding.pid,
      type: "abuse",
      label: canonicalUpgradeName(finding.details),
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
    `Версия игры: ${result.replay?.build_version || "не определена"}`,
    `Длительность: ${fmtTime(result.duration_g_sec)} (${result.duration_g_sec} игровых сек.)`,
    `Игроков: ${(result.players || []).length}`,
    `Записей потока: ${result.n_entries || 0}`,
    `Распознано событий: ${result.n_sub_packages || 0}`,
    `Фрагментов генерации карты: ${(result.pattern_placements || []).length}`,
    `Карта: ${footer.map_file || "не определена"}${footer.map_width ? ` · ${footer.map_width}×${footer.map_height}` : ""}`,
    "",
    "Игроки:",
  ];
  for (const player of result.players || []) {
    const builds = result.builds_per_pid?.[player.pid] || [];
    const nation = inferNation(player, builds);
    lines.push(
      `- ${player.name || `Игрок ${player.pid}`} · ${NATION_LABELS[nation] || nation || "нация не определена"} · команда ${player.team}`,
    );
  }
  lines.push("", `Двойных прокачек: ${(result.abuses || []).length}`);
  for (const abuse of result.abuses || []) {
    const details = abuse.details || {};
    lines.push(
      `- ${playerName(result, abuse.pid)} · ${canonicalUpgradeName(details)} · ${fmtTime(abuse.ts_g_sec_first)}`,
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
    "время_игровые_секунды", "время", "id_игрока", "игрок", "тип", "событие", "подробности",
  ]];
  for (const event of buildTimeline(result)) {
    rows.push([
      event.ts,
      fmtTime(event.ts),
      event.pid,
      playerName(result, event.pid),
      EVENT_LABELS[event.type] || event.type,
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
    "имя_шаблона", "группа", "x", "y", "позиция_в_файле", "ширина_шаблона",
    "высота_шаблона", "число_объектов",
  ]];
  for (const placement of result.pattern_placements || []) {
    const inventory = PATTERN_INVENTORY[placement.name] || {};
    rows.push([
      placement.name,
      patternTypeLabel(patternType(placement.name)),
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
  const playerCount = (result.players || []).length;
  const facts = [
    ["Ход партии", fmtTime(result.duration_g_sec), `${result.duration_g_sec} игровых секунд`],
    ["Состав", `${playerCount} ${pluralRu(playerCount, ["игрок", "игрока", "игроков"])}`,
      language === "en"
        ? `${result.n_entries || 0} ${Number(result.n_entries) === 1 ? "stream record" : "stream records"}`
        : `${result.n_entries || 0} записей потока`],
    ["События", Number(result.n_sub_packages || 0).toLocaleString(NUMBER_LOCALE), "распознано в реплее"],
    ["Карта", footer.map_width ? `${footer.map_width}×${footer.map_height}` : "—", footer.map_file || "файл не указан"],
    ["Фрагменты карты", Number((result.pattern_placements || []).length).toLocaleString(NUMBER_LOCALE), "шаблонов генератора"],
    ["Разбор", `${parseMs} мс`, result.replay?.build_version ? `версия игры ${result.replay.build_version}` : "версия игры неизвестна"],
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
        el("span", {}, "Проверены команды исследования и применения улучшений."),
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
            el("b", {}, canonicalUpgradeName(details)),
            el("time", {}, fmtTime(first.ts_g_sec_first)),
          ]),
          ...group.map((finding) => el("div", { class: "evidence-row" }, [
            el("span", { class: `event-tag ${finding.kind === "double-apply" ? "abuse" : "order"}` },
              finding.kind === "double-apply" ? "применение" : "повторные клики"),
            el("span", {}, `${fmtTime(finding.ts_g_sec_first)} → ${fmtTime(finding.ts_g_sec_second)}`),
            el("span", { class: "muted" }, `интервал ${(finding.gap_ticks / 10).toFixed(1)} игров. сек.`),
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
        el("b", {}, player.name || `Игрок ${player.pid}`),
        el("span", {}, player.lanid || "Сетевой ID не записан"),
      ]),
      el("span", { class: "roster-nation" }, NATION_LABELS[nation] || nation || "—"),
      el("span", { class: "roster-team" }, `Команда ${player.team}`),
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
      el("span", {}, player?.name || `Игрок ${event.pid}`),
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
      el("option", { value: player.pid }, player.name || `Игрок ${player.pid}`)
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
    count.textContent = `${filtered.length.toLocaleString(NUMBER_LOCALE)} ${pluralRu(filtered.length, ["событие", "события", "событий"])}`;
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

function tallyNamedObject(object, labeler) {
  const named = new Map();
  for (const [key, value] of Object.entries(object || {})) {
    const label = labeler(key);
    named.set(label, (named.get(label) || 0) + Number(value || 0));
  }
  return [...named.entries()].sort((a, b) => b[1] - a[1]);
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
      el("span", {}, "Список игроков отсутствует или повреждён."),
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
    const upgradeCount = upgrades.filter((item) => item.start).length;

    return el("details", { class: "player-dossier", open: index === 0 }, [
      el("summary", {}, [
        swatch(player),
        el("div", { class: "dossier-title" }, [
          el("b", {}, player.name || `Игрок ${pid}`),
          el("span", {}, NATION_LABELS[nation] || nation || "Нация не определена"),
        ]),
        el("span", {}, `${builds.length} ${pluralRu(builds.length, ["постройка", "постройки", "построек"])}`),
        el("span", {}, `${unitTotal} ${pluralRu(unitTotal, ["юнит", "юнита", "юнитов"])}`),
        el("span", {}, `${upgradeCount} ${pluralRu(upgradeCount, ["улучшение", "улучшения", "улучшений"])}`),
      ]),
      el("div", { class: "dossier-body" }, [
        el("div", { class: "dossier-meta" }, [
          ["ID игрока", pid],
          ["Сетевой ID", player.lanid || "—"],
          ["Команда", player.team],
          ["Цвет в игре", player.color],
          ["Погибло", result.deaths_per_pid?.[pid] || 0],
          ["Сделок", trades.length],
        ].map(([label, value]) => el("div", {}, [
          el("span", {}, label),
          el("b", {}, value),
        ]))),
        el("div", { class: "dossier-columns" }, [
          el("section", {}, [
            el("h4", {}, "Порядок строительства"),
            miniList(builds.slice(0, 30).map((item) => ({
              time: item.ts_g_sec,
              label: canonicalBuildingName(item.sid),
              note: `${item.builders ?? 0} ${pluralRu(item.builders ?? 0, ["строитель", "строителя", "строителей"])}`,
            })), "Строительство не распознано."),
          ]),
          el("section", {}, [
            el("h4", {}, "Улучшения"),
            miniList(upgrades.filter((item) => item.start).slice(0, 30).map((item) => ({
              time: item.ts_g_sec,
              label: canonicalUpgradeName(item),
            })), "Улучшения не распознаны."),
          ]),
          el("section", {}, [
            el("h4", {}, "Произведено"),
            miniList(tallyNamedObject(spawns, canonicalEntityName).slice(0, 20).map(([label, value]) => ({
              label,
              note: `×${value}`,
            })), "Появления юнитов не распознаны."),
          ]),
          el("section", {}, [
            el("h4", {}, "Приказы"),
            miniList(tallyNamedObject(orders, orderLabel).slice(0, 20).map(([label, value]) => ({
              label,
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
  const pixelRatio = Math.min(window.devicePixelRatio || 1, 2);
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
  const canvas = el("canvas", {
    class: "pattern-map",
    role: "img",
    tabindex: 0,
    "aria-label": `Схема ${placements.length} размещённых фрагментов карты. Стрелки выбирают точку.`,
  });
  canvas.width = Math.round(width * pixelRatio);
  canvas.height = Math.round(height * pixelRatio);
  const context = canvas.getContext("2d");
  const radius = placements.length > 700 ? 3.1 : 4.3;
  const points = placements.map((placement) => ({
    placement,
    type: patternType(placement.name),
    x: mapX(Number(placement.x)),
    y: mapY(Number(placement.y)),
  }));
  let selectedIndex = -1;

  const paint = () => {
    context.setTransform(pixelRatio, 0, 0, pixelRatio, 0, 0);
    context.clearRect(0, 0, width, height);
    context.fillStyle = "#10120d";
    context.fillRect(0, 0, width, height);

    context.beginPath();
    for (let step = 0; step <= 8; step += 1) {
      const x = pad + (step / 8) * (width - pad * 2);
      const y = pad + (step / 8) * (height - pad * 2);
      context.moveTo(x, pad);
      context.lineTo(x, height - pad);
      context.moveTo(pad, y);
      context.lineTo(width - pad, y);
    }
    context.strokeStyle = "rgba(219, 194, 126, 0.105)";
    context.lineWidth = 1;
    context.stroke();

    context.strokeStyle = "rgba(219, 194, 126, 0.42)";
    context.strokeRect(pad, pad, width - pad * 2, height - pad * 2);

    context.fillStyle = "#8f805c";
    context.font = '10px "JetBrains Mono", Consolas, monospace';
    context.textAlign = "center";
    context.fillText(`${minX}`, pad, height - 18);
    context.fillText(`${maxX}`, width - pad, height - 18);
    context.fillText(`${minY}`, 18, height - pad);
    context.fillText(`${maxY}`, 18, pad + 5);

    for (const point of points) {
      context.beginPath();
      context.arc(point.x, point.y, radius, 0, Math.PI * 2);
      context.fillStyle = patternColor(point.type);
      context.globalAlpha = 0.84;
      context.fill();
      context.globalAlpha = 1;
      context.strokeStyle = "rgba(9, 8, 5, 0.8)";
      context.stroke();
    }
    if (selectedIndex >= 0) {
      const point = points[selectedIndex];
      context.beginPath();
      context.arc(point.x, point.y, radius + 3, 0, Math.PI * 2);
      context.strokeStyle = "#f6e6bc";
      context.lineWidth = 2;
      context.stroke();
    }
  };

  const choose = (index) => {
    if (index < 0 || index >= points.length) return;
    selectedIndex = index;
    const { placement, type } = points[index];
    const typeLabel = patternTypeLabel(type);
    const inventory = PATTERN_INVENTORY[placement.name] || {};
    selectedInfo.replaceChildren(
      el("div", { class: "selected-pattern-title" }, [
        el("span", {
          class: "legend-dot",
          style: `background:${patternColor(type)}`,
        }),
        el("b", {}, placement.name),
        el("span", {}, typeLabel),
      ]),
      el("dl", { class: "selected-pattern-data" }, [
        ["Координаты", `${placement.x}, ${placement.y}`],
        ["Размер шаблона", inventory.width && inventory.height
          ? `${inventory.width}×${inventory.height}` : "не определён"],
        ["Объектов", inventory.object_count ?? "не определено"],
        ["Позиция в файле", `0x${Number(placement.offset).toString(16)}`],
      ].map(([key, value]) => el("div", {}, [
        el("dt", {}, key),
        el("dd", {}, value),
      ]))),
    );
    canvas.setAttribute(
      "aria-label",
      `${placement.name}, ${typeLabel}, координаты ${placement.x}, ${placement.y}. Стрелки выбирают другую точку.`,
    );
    paint();
  };

  const nearestPoint = (event) => {
    const rect = canvas.getBoundingClientRect();
    const x = (event.clientX - rect.left) * (width / rect.width);
    const y = (event.clientY - rect.top) * (height / rect.height);
    let nearest = -1;
    let distanceSquared = 100;
    for (let index = 0; index < points.length; index += 1) {
      const dx = points[index].x - x;
      const dy = points[index].y - y;
      const candidate = dx * dx + dy * dy;
      if (candidate < distanceSquared) {
        distanceSquared = candidate;
        nearest = index;
      }
    }
    return nearest;
  };

  canvas.addEventListener("pointermove", (event) => {
    const index = nearestPoint(event);
    canvas.style.cursor = index >= 0 ? "pointer" : "crosshair";
    canvas.title = index >= 0
      ? `${points[index].placement.name} · ${patternTypeLabel(points[index].type)}`
      : "";
  }, { passive: true });
  canvas.addEventListener("click", (event) => choose(nearestPoint(event)));
  canvas.addEventListener("keydown", (event) => {
    if (!["ArrowRight", "ArrowDown", "ArrowLeft", "ArrowUp", "Home", "End"].includes(event.key)) {
      return;
    }
    event.preventDefault();
    if (event.key === "Home") selectedIndex = 0;
    else if (event.key === "End") selectedIndex = points.length - 1;
    else if (event.key === "ArrowRight" || event.key === "ArrowDown") {
      selectedIndex = (selectedIndex + 1 + points.length) % points.length;
    } else {
      selectedIndex = (selectedIndex - 1 + points.length) % points.length;
    }
    choose(selectedIndex);
  });
  paint();
  return canvas;
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
      el("span", {}, "Проверьте раздел «Диагностика»: блок генерации может отсутствовать или иметь другую версию формата."),
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
      el("option", { value: type }, `${patternTypeLabel(type)} · ${number}`)
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
    count.textContent = `${filtered.length.toLocaleString(NUMBER_LOCALE)} ${pluralRu(filtered.length, ["точка", "точки", "точек"])}`;
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
          el("span", {}, patternTypeLabel(type)),
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
      el("b", {}, patternTypeLabel(type)),
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
    el("dd", {}, Number(value).toLocaleString(NUMBER_LOCALE)),
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

function warningLabel(warning) {
  const labels = {
    "Не удалось прочитать OSWMap-заголовок.": "Не удалось прочитать заголовок файла.",
    "Поток entry-событий не найден.": "Поток игровых событий не найден.",
    "Футер GameMapBegin/GameMapEnd не найден.": "Служебная концовка файла не найдена.",
    "Футер найден, но завершающий GameMapEnd отсутствует.": "Концовка файла повреждена или записана не полностью.",
    "PatternList не содержит распознанных n/x/y-записей.": "Данные генерации карты не содержат распознанных координат.",
  };
  return labels[warning] || warning;
}

function streamSourceLabel(result, name) {
  const player = String(name).match(/^player_(\d+)$/);
  if (player) return playerName(result, Number(player[1]));
  const labels = {
    env: "Окружение",
    misc: "Служебные события",
    progress: "Ход симуляции",
    pool: "Пул объектов",
  };
  if (labels[name]) return labels[name];
  if (String(name).startsWith("unknown_")) return "Неизвестный источник";
  return "Системный источник";
}

function yesNo(value) {
  if (value == null || value === "") return "Не указано";
  return value === true || value === 1 || String(value).toLowerCase() === "true"
    ? "Да"
    : "Нет";
}

function renderDiagnostics(result) {
  const replay = result.replay || {};
  const footer = result.footer || {};
  const settings = result.settings || {};
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
            el("li", {}, warningLabel(warning))
          ))
        : el("div", { class: "diagnostic-ok" }, "Структурных предупреждений нет."),
    ]),
    el("section", { class: "diagnostic-card" }, [
      el("p", { class: "section-kicker" }, "Файл"),
      el("h3", {}, "OSWMap"),
      dataRows([
        ["Формат", replay.map_format_version ? `OSWMap${replay.map_format_version}` : "—"],
        ["Версия игры", replay.build_version || "—"],
        ["ID файла", replay.uid || "—"],
        ["Размер", fmtBytes(replay.file_size)],
        ["Записей потока", result.n_entries],
        ["Распознано событий", result.n_sub_packages],
      ]),
    ]),
    el("section", { class: "diagnostic-card" }, [
      el("p", { class: "section-kicker" }, "Служебные настройки"),
      el("h3", {}, "Генерация и тип матча"),
      dataRows([
        ["Маска генерации", settings.maskname || "—"],
        ["Путь к маске", settings.maskpath],
        ["Первый ключ генерации", settings.randkey0],
        ["Второй ключ генерации", settings.randkey1],
        ["Рейтинговая игра", yesNo(settings.brating)],
      ]),
    ]),
    el("section", { class: "diagnostic-card" }, [
      el("p", { class: "section-kicker" }, "Концовка файла"),
      el("h3", {}, footer.complete ? "Данные завершены корректно" : "Неполные данные"),
      dataRows([
        ["Файл карты", footer.map_file],
        ["Размер карты", footer.map_width ? `${footer.map_width}×${footer.map_height}` : null],
        ["Флаги карты", footer.map_flags],
        ["Проект", footer.project_path],
        ["Конфигурация меню", footer.menu_config],
        ["Состояние", footer.player_state],
        ["Служебный таймер", footer.elapsed_raw_s?.toFixed?.(6)],
        ["Позиция окончания записи", footer.record_end_offset != null
          ? `0x${footer.record_end_offset.toString(16)}` : null],
      ]),
      footer.elapsed_raw_s != null
        ? el("p", { class: "technical-note" },
            "Служебный таймер не равен времени партии; точное назначение этого значения пока не установлено.")
        : null,
    ]),
    el("section", { class: "diagnostic-card" }, [
      el("p", { class: "section-kicker" }, "Типы событий"),
      el("h3", {}, `${handlerRows.length} ${pluralRu(handlerRows.length, ["категория", "категории", "категорий"])}`),
      el("div", { class: "diagnostic-bars" }, handlerRows.slice(0, 30).map(([name, value]) =>
        el("div", {}, [
          el("span", {}, handlerLabel(name)),
          el("span", {}, Number(value).toLocaleString(NUMBER_LOCALE)),
        ])
      )),
    ]),
    el("section", { class: "diagnostic-card" }, [
      el("p", { class: "section-kicker" }, "Источники событий"),
      el("h3", {}, `${playerRows.length} ${pluralRu(playerRows.length, ["источник", "источника", "источников"])}`),
      el("div", { class: "diagnostic-bars" }, playerRows.map(([name, value]) =>
        el("div", {}, [
          el("span", {}, streamSourceLabel(result, name)),
          el("span", {}, Number(value).toLocaleString(NUMBER_LOCALE)),
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
      "Все разобранные поля без сокращений: игроки, события, концовка файла, генерация карты и диагностика.",
      `${fmtBytes(new Blob([JSON.stringify(result)]).size)} данных`,
      () => exportJson(filename, result),
      "Скачать JSON",
    ),
    exportCard(
      "Хронология CSV",
      "Плоская таблица строительства, производства, улучшений, рынка и приказов.",
      `${timelineCount.toLocaleString(NUMBER_LOCALE)} строк`,
      () => exportTimeline(filename, result),
      "Скачать CSV",
    ),
    exportCard(
      "Шаблоны карты CSV",
      "Все размещённые фрагменты карты: имя, группа, координаты, размеры и число объектов.",
      `${patternCount.toLocaleString(NUMBER_LOCALE)} строк`,
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
          await navigator.clipboard.writeText(language === "en" ? tr(report) : report);
          notify("Сводка скопирована");
        } catch {
          notify("Браузер запретил доступ к буферу обмена");
        }
      },
      "Копировать",
    ),
  ]);
}

function configureTabs(workspace, onActivate = () => {}) {
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
    onActivate(tab.dataset.section);
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
    "файл", "длительность_игровые_секунды", "игроки", "ширина_карты", "высота_карты",
    "фрагменты_карты", "постройки", "юниты", "улучшения", "сделки", "двойные_прокачки",
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
          ? `версия игры ${result.replay.build_version}` : "версия игры неизвестна"),
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
  const comparison = el("div", {}, [
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
  localizeTree(comparison);
  return comparison;
}

export function renderCard(filename, result, parseMs, options = {}) {
  const id = `replay-${++workspaceSequence}`;
  const playerCount = (result.players || []).length;
  const eventCount = Number(result.n_sub_packages || 0);
  const tabs = [
    ["overview", "Сводка", null],
    ["timeline", "Хронология", buildTimeline(result).length],
    ["players", "Игроки", (result.players || []).length],
    ["map", "Генерация карты", (result.pattern_placements || []).length],
    ["diagnostics", "Диагностика", (result.format_warnings || []).length || null],
    ["export", "Экспорт", null],
  ];
  const contentFactories = {
    overview: () => renderOverview(result, parseMs),
    timeline: () => renderTimeline(result, filename),
    players: () => renderPlayers(result),
    map: () => renderMap(result, filename),
    diagnostics: () => renderDiagnostics(result),
    export: () => renderExport(filename, result),
  };
  const workspace = el("article", { class: "replay-workspace card" }, [
    el("header", { class: "workspace-header" }, [
      el("div", { class: "workspace-title" }, [
        el("p", { class: "section-kicker" }, "Открытый реплей"),
        el("h2", {}, filename),
        el("p", {}, [
          `${fmtTime(result.duration_g_sec)} · `,
          `${playerCount} ${pluralRu(playerCount, ["игрок", "игрока", "игроков"])} · `,
          `${eventCount.toLocaleString(NUMBER_LOCALE)} ${pluralRu(eventCount, ["событие", "события", "событий"])}`,
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
        dataset: { section: key },
        "aria-controls": `${id}-panel-${key}`,
        "aria-selected": index === 0 ? "true" : "false",
        tabindex: index === 0 ? 0 : -1,
      }, [
        el("span", {}, label),
        badge != null ? el("small", {}, Number(badge).toLocaleString(NUMBER_LOCALE)) : null,
      ])
    )),
    ...tabs.map(([key]) =>
      el("section", {
        id: `${id}-panel-${key}`,
        class: `workspace-panel panel-${key}`,
        role: "tabpanel",
        dataset: { section: key },
        "aria-labelledby": `${id}-tab-${key}`,
      })
    ),
  ]);
  const initialized = new Set();
  configureTabs(workspace, (key) => {
    if (initialized.has(key)) return;
    const panel = workspace.querySelector(`[role="tabpanel"][data-section="${key}"]`);
    panel.replaceChildren(contentFactories[key]());
    initialized.add(key);
  });
  localizeTree(workspace);
  return workspace;
}
