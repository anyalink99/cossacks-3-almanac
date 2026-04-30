// Russian labels and color-coded resource markers (no emoji — universal browser support).

export const RES_INFO = {
  food:  { ru: "Еда",     short: "F", color: "#d97766" },
  wood:  { ru: "Дерево",  short: "W", color: "#a06f3b" },
  stone: { ru: "Камень",  short: "S", color: "#9b8a6a" },
  gold:  { ru: "Золото",  short: "G", color: "#d4a857" },
  iron:  { ru: "Железо",  short: "I", color: "#6da5d4" },
  coal:  { ru: "Уголь",   short: "C", color: "#3d3024" },
};

export const RES_ORDER = ["food", "wood", "stone", "gold", "iron", "coal"];

export const KIND_INFO = {
  build:    { ru: "Построить",          short: "Стр", color: "#6da5d4" },
  train:    { ru: "Обучить",            short: "Об",  color: "#87b369" },
  research: { ru: "Исследовать",        short: "Исс", color: "#d4a857" },
  assign:   { ru: "Раскидать крестьян", short: "Расп", color: "#b87dd4" },
};

// Inline HTML for a small colored dot — used everywhere icons used to be.
export function dot(color, label = "") {
  return `<span class="dot" style="background:${color}" title="${label}"></span>`;
}

export function resTag(res) {
  const info = RES_INFO[res];
  return `<span class="res-tag" style="--c:${info.color}"><span class="dot"></span>${info.ru}</span>`;
}

// Resource preset options — exact game values from initmapgen.inc:166-189
// (driven by gMap.settings.gen.resourcestart). Locale labels from gui.txt
// `randommap.initialresources.{0..3}`.
export const RES_PRESETS = [
  { id: 0, label: "Стандарт (1 000)",   value: 1000 },
  { id: 1, label: "Богато (4 000)",     value: 4000 },
  { id: 2, label: "Тысячи (5 000)",     value: 5000 },
  { id: 3, label: "Миллионы (1 000 000)", value: 1000000 },
];

// Starting peasant count. Game default (dogenerate.inc:1255 CreateStartPointPeasants)
// is 18, in a 6×3 grid. Other counts are custom — game itself doesn't expose them as
// presets, but they're useful for testing build orders with smaller economies.
export const PEASANT_PRESETS = [
  { label: "5",  value: 5 },
  { label: "10", value: 10 },
  { label: "18 (как в игре)", value: 18 },
  { label: "25", value: 25 },
  { label: "50", value: 50 },
];

export function fmtTime(g_sec, gameSpeedFactor = 1.4) {
  const real = g_sec / gameSpeedFactor;
  const min = Math.floor(real / 60);
  const sec = Math.round(real % 60);
  return `${g_sec}g · ${min}:${String(sec).padStart(2, "0")}`;
}

export function fmtName(item) {
  return item?.name_ru || item?.name_en || item?.sid || "?";
}

export function fmtCost(item) {
  const parts = [];
  for (const k of RES_ORDER) {
    const v = item?.[k];
    if (v) parts.push(`${v}${RES_INFO[k].short}`);
  }
  return parts.join(" ") || "—";
}

export const COMMON_NAME = {
  aus: "eur", fra: "eur", eng: "eur", spa: "spa", rus: "rus", ukr: "ukr",
  pol: "eur", swe: "eur", pru: "eur", ven: "eur", tur: "tur", alg: "tur",
  net: "eur", den: "eur", por: "por", pie: "eur", sax: "eur", bav: "eur",
  hun: "eur", swi: "eur", sco: "eur",
};

export const DEFAULT_PEASANT = {
  aus: "peaaus", fra: "peaeng", eng: "peaeng", spa: "peaspa", rus: "pearus",
  ukr: "peaukr", pol: "peapol", swe: "peaeng", pru: "peaaus", ven: "peaspa",
  tur: "peatur", alg: "peatur", net: "peaeng", den: "peaeng", por: "peaspa",
  pie: "peaspa", sax: "peaaus", bav: "peaaus", hun: "peapol", swi: "peaaus",
  sco: "peasco",
};

// True if a sid looks like a peasant unit.
export function isPeasant(sid) {
  return typeof sid === "string" && sid.startsWith("pea");
}
