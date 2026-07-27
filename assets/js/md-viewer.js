// Markdown viewer used by docs/index.html and internals/index.html.
// Loads _manifest.json from the current directory, renders a sidebar
// tree, lets the user pick a file, fetches and renders it via marked.

import { marked } from "https://cdn.jsdelivr.net/npm/marked@13.0.3/+esm";
import markedFootnote from "https://cdn.jsdelivr.net/npm/marked-footnote@1.2.4/+esm";
import markedAlert from "https://cdn.jsdelivr.net/npm/marked-alert@2.1.2/+esm";
import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.esm.min.mjs";

const ENGLISH = /\/(?:docs_en|internals_en)(?:\/|$)/.test(location.pathname);
const DIRECTORY_LABELS = ENGLISH ? {
  reference: "Quick reference",
  recon: "How the game works",
  reports: "Tables and calculations",
  "01_economy": "Economy",
  "02_combat": "Combat and movement",
  "03_buildings": "Buildings",
  "04_units": "Units",
  "05_upgrades": "Upgrades",
  "06_market": "Market",
  "07_naval": "Navy",
  nations: "Nations",
  compare: "Comparisons",
  units: "Units",
  buildings: "Buildings",
  weapons: "Weapons and projectiles",
  world: "Game world",
  systems: "Game systems",
  combat: "Combat",
  economy: "Economy",
  map: "Map and match settings",
  tech: "Technology tree",
  data: "Data formats",
  engine: "Engine",
  scripts: "Scripts",
  project: "Project documentation",
} : {
  reference: "Краткий справочник",
  recon: "Как устроена игра",
  reports: "Таблицы и расчёты",
  "01_economy": "Экономика",
  "02_combat": "Бой и движение",
  "03_buildings": "Здания",
  "04_units": "Юниты",
  "05_upgrades": "Улучшения",
  "06_market": "Рынок",
  "07_naval": "Флот",
  nations: "Нации",
  compare: "Сравнения",
  units: "Юниты",
  buildings: "Здания",
  weapons: "Оружие и снаряды",
  world: "Игровой мир",
  systems: "Игровые системы",
  combat: "Бой",
  economy: "Экономика",
  map: "Карта и настройки матча",
  tech: "Дерево развития",
  data: "Форматы данных",
  engine: "Движок",
  scripts: "Скрипты",
  project: "Документация проекта",
};
const UI = ENGLISH ? {
  home: "Home",
  contents: "Contents",
  loading: (path) => `Loading ${path}…`,
  loadError: (path, message) => `Could not load ${path}: ${message}`,
  manifestError: (message) => `Could not load the manifest: ${message}`,
  mermaidError: (message) => `Could not render Mermaid: ${message}`,
  searchLabel: "Search",
  searchPlaceholder: "Search articles and objects…",
  searchLoading: "Loading the search index…",
  searchResults: (count) => `${count} result${count === 1 ? "" : "s"}`,
  searchShown: (count) => `${count} shown`,
  searchEmpty: (query) => `No matches for “${query}”`,
  searchError: (message) => `Search is unavailable: ${message}`,
  sectionOverview: "Section overview",
  closeContents: "Close",
  catalogLoading: "Loading the object card…",
  catalogError: (message) => `Could not load the object card: ${message}`,
} : {
  home: "На главную",
  contents: "Содержание",
  loading: (path) => `Загружаем ${path}…`,
  loadError: (path, message) => `Не удалось загрузить ${path}: ${message}`,
  manifestError: (message) => `Не удалось загрузить манифест: ${message}`,
  mermaidError: (message) => `Не удалось отрисовать mermaid: ${message}`,
  searchLabel: "Поиск",
  searchPlaceholder: "Поиск по статьям и объектам…",
  searchLoading: "Загружаем поисковый индекс…",
  searchResults: (count) => `${count} совпадени${count % 10 === 1 && count % 100 !== 11 ? "е" : "й"}`,
  searchShown: (count) => `показано ${count}`,
  searchEmpty: (query) => `По запросу «${query}» ничего не найдено`,
  searchError: (message) => `Поиск недоступен: ${message}`,
  sectionOverview: "Обзор раздела",
  closeContents: "Закрыть",
  catalogLoading: "Загружаем карточку объекта…",
  catalogError: (message) => `Не удалось загрузить карточку объекта: ${message}`,
};

const ENTITY_UI = ENGLISH ? {
  catalog: "Object catalog",
  kinds: { unit: "Unit", building: "Building", upgrade: "Upgrade" },
  technicalId: "Technical ID",
  available: "Available to",
  allNations: "all nations",
  allExcept: (nations) => `all nations except ${nations}`,
  variant: "Game values",
  baseValues: "Base values",
  differences: "Differences",
  cost: "Cost",
  health: "Health",
  trainingTime: "Training time",
  buildTime: "Construction time",
  researchTime: "Research time",
  gameSeconds: "game sec",
  speed: "Movement speed",
  vision: "Vision",
  capacity: "Capacity",
  housing: "Housing places",
  canBeCaptured: "Can be captured",
  yes: "yes",
  weapons: "Weapons",
  damage: "Damage",
  reload: "Reload",
  range: "Range",
  tiles: "tiles",
  protection: "Protection",
  trainedAt: "Trained at",
  produces: "Produces",
  researchedAt: "Researched at",
  affects: "Affects",
  prerequisites: "Requires",
  effect: "Effect",
  value: "Value",
  level: "Level",
  resources: {
    food: "food", wood: "wood", stone: "stone",
    gold: "gold", iron: "iron", coal: "coal",
  },
  weaponKinds: {
    pike: "pike", sword: "blade", bullet: "bullet",
    cannister: "canister", arrow: "arrow", cannonball: "cannonball",
    firearrow: "fire arrow",
  },
} : {
  catalog: "Каталог объектов",
  kinds: { unit: "Юнит", building: "Здание", upgrade: "Улучшение" },
  technicalId: "Технический код",
  available: "Доступно",
  allNations: "всем нациям",
  allExcept: (nations) => `всем нациям, кроме: ${nations}`,
  variant: "Игровые значения",
  baseValues: "Основные значения",
  differences: "Отличия",
  cost: "Стоимость",
  health: "Здоровье",
  trainingTime: "Время найма",
  buildTime: "Время строительства",
  researchTime: "Время изучения",
  gameSeconds: "игр. с",
  speed: "Скорость передвижения",
  vision: "Обзор",
  capacity: "Вместимость",
  housing: "Мест для жителей",
  canBeCaptured: "Можно захватить",
  yes: "да",
  weapons: "Оружие",
  damage: "Урон",
  reload: "Перезарядка",
  range: "Дальность",
  tiles: "клеток",
  protection: "Защита",
  trainedAt: "Нанимается в",
  produces: "Производит",
  researchedAt: "Изучается в",
  affects: "Действует на",
  prerequisites: "Требуется",
  effect: "Эффект",
  value: "Значение",
  level: "Уровень",
  resources: {
    food: "еда", wood: "дерево", stone: "камень",
    gold: "золото", iron: "железо", coal: "уголь",
  },
  weaponKinds: {
    pike: "пика", sword: "клинковое оружие", bullet: "пуля",
    cannister: "картечь", arrow: "стрела", cannonball: "ядро",
    firearrow: "огненная стрела",
  },
};

// --- Markdown configuration ----------------------------------------------
marked.setOptions({
  gfm: true,
  breaks: false,
  headerIds: true,
});
marked.use(markedFootnote());
marked.use(markedAlert());

// --- Mermaid configuration (Cossacks warm dark theme) --------------------
mermaid.initialize({
  startOnLoad: false,
  securityLevel: "loose",
  theme: "base",
  fontFamily: '"Inter", "Segoe UI", system-ui, sans-serif',
  themeVariables: {
    background:        "#15100a",
    mainBkg:           "#1f1810",
    primaryColor:      "#1f1810",
    primaryTextColor:  "#e6d4a8",
    primaryBorderColor:"#6a5128",
    secondaryColor:    "#251c14",
    secondaryTextColor:"#e6d4a8",
    secondaryBorderColor:"#4e3b1f",
    tertiaryColor:     "#0c0805",
    tertiaryTextColor: "#a59470",
    tertiaryBorderColor:"#4e3b1f",
    lineColor:         "#9a7836",
    textColor:         "#e6d4a8",
    nodeBorder:        "#6a5128",
    nodeTextColor:     "#e6d4a8",
    edgeLabelBackground:"#1f1810",
    clusterBkg:        "rgba(212, 130, 58, 0.05)",
    clusterBorder:     "#4e3b1f",
    titleColor:        "#e8c878",
    actorBkg:          "#1f1810",
    actorBorder:       "#6a5128",
    actorTextColor:    "#e6d4a8",
    actorLineColor:    "#9a7836",
    labelBoxBkgColor:  "#1f1810",
    labelBoxBorderColor:"#6a5128",
    labelTextColor:    "#e6d4a8",
    loopTextColor:     "#e6d4a8",
    fillType0:         "#251c14",
    fillType1:         "#322618",
    fillType2:         "#1f1810",
    fillType3:         "#4e3b1f",
  },
  flowchart: {
    htmlLabels: true,
    curve: "basis",
  },
});

// Mermaid flowchart labels do not understand `inline-code` (codespan).
// Rewrite backtick spans inside node labels to <code>…</code> before render
// so doc authors can keep writing `sid` naturally.
function preprocessMermaid(source) {
  return source.replace(/`([^`\r\n]+)`/g, "<code>$1</code>");
}

const tableScrollUpdaters = new WeakMap();
const tableScrollResizeObserver = typeof ResizeObserver === "undefined"
  ? null
  : new ResizeObserver((entries) => {
    for (const entry of entries) tableScrollUpdaters.get(entry.target)?.();
  });

// Marked emits raw <table>. Wide tables get two synchronized scroll surfaces:
// one above the header for immediate access and the conventional one below.
// The upper scrollbar stays hidden when the table fits the article column.
function wrapTablesInScrollContainers(container) {
  for (const table of container.querySelectorAll("table")) {
    if (table.parentElement?.classList.contains("md-table-scroll")) continue;

    const shell = document.createElement("div");
    shell.className = "md-table-shell";

    const topScroll = document.createElement("div");
    topScroll.className = "md-table-scroll-top";
    topScroll.setAttribute(
      "aria-label",
      ENGLISH ? "Scroll table horizontally" : "Горизонтальная прокрутка таблицы"
    );

    const topTrack = document.createElement("div");
    topTrack.className = "md-table-scroll-top-track";
    topScroll.appendChild(topTrack);

    const bottomScroll = document.createElement("div");
    bottomScroll.className = "md-table-scroll";

    table.replaceWith(shell);
    shell.append(topScroll, bottomScroll);
    bottomScroll.appendChild(table);

    let syncing = false;
    const syncScroll = (source, target) => {
      if (syncing || target.scrollLeft === source.scrollLeft) return;
      syncing = true;
      target.scrollLeft = source.scrollLeft;
      syncing = false;
    };
    topScroll.addEventListener(
      "scroll",
      () => syncScroll(topScroll, bottomScroll),
      { passive: true }
    );
    bottomScroll.addEventListener(
      "scroll",
      () => syncScroll(bottomScroll, topScroll),
      { passive: true }
    );

    const updateTopScrollbar = () => {
      const scrollWidth = bottomScroll.scrollWidth;
      const overflows = scrollWidth > bottomScroll.clientWidth + 1;
      topTrack.style.width = `${scrollWidth}px`;
      topScroll.hidden = !overflows;
      topScroll.tabIndex = overflows ? 0 : -1;
      if (!overflows) topScroll.scrollLeft = 0;
      else topScroll.scrollLeft = bottomScroll.scrollLeft;
    };

    tableScrollUpdaters.set(table, updateTopScrollbar);
    tableScrollUpdaters.set(bottomScroll, updateTopScrollbar);
    tableScrollResizeObserver?.observe(table);
    tableScrollResizeObserver?.observe(bottomScroll);
    requestAnimationFrame(updateTopScrollbar);
  }
}

function headingSlug(value) {
  return value
    .trim()
    .toLocaleLowerCase(ENGLISH ? "en" : "ru")
    .replace(/[^\p{L}\p{N}\s_-]/gu, "")
    // Match the GitHub-style fragments already used by generated tables:
    // punctuation is removed first, so spaces on both sides of an em dash
    // deliberately become two hyphens.
    .replace(/\s/g, "-");
}

function assignHeadingIds(container) {
  const used = new Set(
    [...container.querySelectorAll("[id]")].map((element) => element.id)
  );
  for (const heading of container.querySelectorAll("h1, h2, h3, h4, h5, h6")) {
    if (heading.id) continue;
    const base = headingSlug(heading.textContent);
    if (!base) continue;
    let candidate = base;
    let suffix = 1;
    while (used.has(candidate)) candidate = `${base}-${suffix++}`;
    heading.id = candidate;
    used.add(candidate);
  }
}

async function renderMermaidBlocks(container) {
  const blocks = container.querySelectorAll("pre > code.language-mermaid, pre > code.lang-mermaid");
  let idx = 0;
  for (const code of blocks) {
    const source = preprocessMermaid(code.textContent);
    const pre = code.parentElement;
    const target = document.createElement("div");
    target.className = "mermaid-render";
    pre.replaceWith(target);
    try {
      const { svg } = await mermaid.render(`mmd-${Date.now()}-${idx++}`, source);
      target.innerHTML = svg;
    } catch (e) {
      target.innerHTML = `<div class="md-error">${UI.mermaidError(e.message)}</div>` +
                         `<pre><code>${source.replace(/[<>&]/g, c => ({"<":"&lt;",">":"&gt;","&":"&amp;"}[c]))}</code></pre>`;
    }
  }
}

const $ = (sel) => document.querySelector(sel);

const params = new URLSearchParams(location.search);
let currentPath = params.get("p");
let currentEntity = params.get("entity");
let searchIndexPromise = null;
let searchElements = null;
let entityCatalogPromise = null;
let entityIndexPromise = null;
let closeMobileDrawer = () => {};

const LEGACY_REFERENCE_ROUTES = [
  {
    from: "reference/03_buildings/README.md",
    routes: {
      "town_hall.md": ["городской-центр-cen", "cen--городской-центр", "town-hall-cen"],
      "housing.md": ["дом-hou", "hou--дом", "housing-hou"],
      "barracks_17.md": ["казарма-17-в-bar", "bar--казарма-17-в", "barracks-17th-century-bar"],
      "barracks_18.md": ["казарма-18-в-ba2", "ba2--казарма-18-в", "barracks-18th-century-ba2"],
      "blacksmith.md": ["кузница-bla", "bla--кузница", "blacksmith-bla"],
      "stable.md": ["конюшня-sta", "sta--конюшня", "stable-sta"],
      "cathedral.md": ["собор-tem", "tem--собор", "cathedral-tem"],
      "academy.md": ["академия-aca", "aca--академия", "academy-aca"],
      "artillery_depot.md": ["артиллерийское-депо-art", "art--артиллерийское-депо", "artillery-depot-art"],
      "diplomatic_center.md": ["дипломатический-центр-dip", "dip--дипломатический-центр", "diplomatic-center-dip"],
      "mill.md": ["мельница-mil", "mil--мельница", "mill-mil"],
      "storehouse.md": ["склад-sto", "sto--склад", "storehouse-sto"],
      "market.md": ["рынок-mar", "mar--рынок", "mar--market", "market-mar"],
      "shipyard.md": ["порт-por", "por--порт", "shipyard-por"],
      "tower.md": ["башня-tow", "tow--башня", "tower-tow", "башня--кратко", "tower-summary"],
      "mines.md": [
        "золотая-шахта-gol", "gol--золотая-шахта", "gold-mine-gol",
        "железная-шахта-iro", "iro--железная-шахта", "iron-mine-iro",
        "угольная-шахта-coa", "coa--угольная-шахта", "coal-mine-coa",
        "улучшения-шахт", "шахты--апгрейды-golirocoa", "mines---upgrades-golirocoa",
      ],
      "walls_and_gates.md": [
        "каменная-стена-swa", "swa--каменная-стена", "stone-wall-swa",
        "каменные-ворота-sga", "sga--каменные-ворота", "stone-gate-sga",
        "деревянные-ворота-wga", "wga--деревянные-ворота", "wooden-gate-wga",
        "палисад-wwa", "wwa--палисад", "palisade-wwa",
      ],
    },
  },
  {
    from: "reference/05_upgrades/README.md",
    routes: {
      "mines.md": ["улучшения-шахт", "апгрейды-шахт-eurgoleurcoaeuriro", "mine-upgrades"],
      "academy.md": ["академия-исследования-aca", "aca--академия-исследования", "academy-aca"],
      "mill.md": ["мельница-эффективность-еды-mil", "mil--мельница-эффективность-еды", "mill-mil"],
      "blacksmith.md": [
        "кузница-по-юнитам--урон-и-защита-bla",
        "bla--кузница-по-юнитам--урон-и-защита",
        "blacksmith-bla--unit-damage-and-protection",
      ],
      "stable.md": [
        "конюшня-по-юнитам--кавалерия-sta",
        "sta--конюшня-по-юнитам--кавалерия",
        "stable-sta--cavalry",
      ],
      "barracks_17.md": [
        "казарма-17-в-по-юнитам-bar",
        "bar--казарма-17-в-по-юнитам",
        "barracks-17th-century-bar",
      ],
      "barracks_18.md": [
        "казарма-18-в-по-юнитам-ba2",
        "ba2--казарма-18-в-по-юнитам",
        "barracks-18th-century-ba2",
      ],
      "artillery_depot.md": [
        "артиллерийское-депо-апгрейды-пушек-art",
        "art--артиллерийское-депо-апгрейды-пушек",
        "artillery-depot-art--cannon-upgrades",
      ],
      "town_hall.md": [
        "городской-центр-переход-эпохи-cen",
        "cen--городской-центр-переход-эпохи",
        "town-hall-cen--advancing-to-the-18th-century",
      ],
      "tower.md": [
        "башня-скорость-перезарядки-tow",
        "tow--башня-скорость-перезарядки",
        "tower-tow--reload-speed",
      ],
      "walls_and_gates.md": [
        "каменная-стена-постройка-ворот-swa",
        "swa--каменная-стена-постройка-ворот",
        "stone-wall-swa--building-a-gate",
        "палисад-постройка-ворот-wwa",
        "wwa--палисад-постройка-ворот",
        "palisade-wwa--building-a-gate",
      ],
      "shipyard.md": [
        "порт-лечение-por", "por--порт-лечение", "shipyard-por--healing",
        "транспорт-вместимость-ferry", "ferry--транспорт-вместимость", "ferry-ferry--capacity",
      ],
    },
  },
];

function applyLegacyReferenceRoute() {
  if (!currentPath || !location.hash) return;
  let fragment;
  try {
    fragment = decodeURIComponent(location.hash.slice(1));
  } catch {
    fragment = location.hash.slice(1);
  }
  const reference = LEGACY_REFERENCE_ROUTES.find(({ from }) => from === currentPath);
  if (!reference) return;
  for (const [filename, fragments] of Object.entries(reference.routes)) {
    if (!fragments.includes(fragment)) continue;
    currentPath = `${currentPath.slice(0, currentPath.lastIndexOf("/") + 1)}${filename}`;
    const query = `?p=${encodeURIComponent(currentPath)}`;
    history.replaceState({}, "", query);
    return;
  }
}

function directoryLabel(segment) {
  return DIRECTORY_LABELS[segment] || segment.replaceAll("_", " ");
}

function readablePath(path, documentTitle = "") {
  const parts = path.split("/");
  const filename = parts.pop() || "";
  const labels = parts.map(directoryLabel);
  if (documentTitle && labels.at(-1)?.toLocaleLowerCase() !== documentTitle.toLocaleLowerCase()) {
    labels.push(documentTitle);
  }
  else if (filename !== "README.md") {
    labels.push(filename.replace(/\.md$/i, "").replaceAll("_", " "));
  }
  return labels.join(" › ");
}

async function loadManifest() {
  const r = await fetch("_manifest.json");
  if (!r.ok) throw new Error(`manifest HTTP ${r.status}`);
  return r.json();
}

async function loadSearchIndex() {
  if (!searchIndexPromise) {
    searchIndexPromise = fetch("_search.json").then((response) => {
      if (!response.ok) throw new Error(`search index HTTP ${response.status}`);
      return response.json();
    });
  }
  return searchIndexPromise;
}

async function loadEntityCatalog() {
  if (!entityCatalogPromise) {
    entityCatalogPromise = fetch("../assets/data/entity-catalog.json").then((response) => {
      if (!response.ok) throw new Error(`entity catalog HTTP ${response.status}`);
      return response.json();
    });
  }
  return entityCatalogPromise;
}

async function loadEntityIndex() {
  if (!entityIndexPromise) {
    const language = ENGLISH ? "en" : "ru";
    entityIndexPromise = fetch(`../assets/data/entity-index.${language}.json`).then((response) => {
      if (!response.ok) throw new Error(`entity index HTTP ${response.status}`);
      return response.json();
    });
  }
  return entityIndexPromise;
}

function normalizeSearch(value) {
  return value.toLocaleLowerCase(ENGLISH ? "en" : "ru").replaceAll("ё", "е");
}

function appendHighlightedText(container, value, terms) {
  const escaped = terms
    .filter(Boolean)
    .sort((a, b) => b.length - a.length)
    .map((term) => term.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"));
  if (!escaped.length) {
    container.textContent = value;
    return;
  }
  const pattern = new RegExp(`(${escaped.join("|")})`, "giu");
  let cursor = 0;
  for (const match of value.matchAll(pattern)) {
    if (match.index > cursor) {
      container.append(document.createTextNode(value.slice(cursor, match.index)));
    }
    const mark = document.createElement("mark");
    mark.textContent = match[0];
    container.append(mark);
    cursor = match.index + match[0].length;
  }
  if (cursor < value.length) {
    container.append(document.createTextNode(value.slice(cursor)));
  }
}

function searchSnippet(text, normalizedText, terms, normalizedQuery = "") {
  let first = normalizedQuery ? normalizedText.indexOf(normalizedQuery) : -1;
  if (first < 0) {
    for (const term of terms) {
      const at = normalizedText.indexOf(term);
      if (at >= 0 && (first < 0 || at < first)) first = at;
    }
  }
  if (first < 0) first = 0;
  let start = Math.max(0, first - 82);
  let end = Math.min(text.length, first + 190);
  if (start > 0) {
    const boundary = text.indexOf(" ", start);
    if (boundary >= 0 && boundary < first) start = boundary + 1;
  }
  if (end < text.length) {
    const boundary = text.lastIndexOf(" ", end);
    if (boundary > first) end = boundary;
  }
  return `${start > 0 ? "…" : ""}${text.slice(start, end)}${end < text.length ? "…" : ""}`;
}

function rankSearchEntries(entries, query) {
  const normalizedQuery = normalizeSearch(query).replace(/\s+/g, " ").trim();
  const terms = normalizedQuery.split(/\s+/).filter(Boolean);
  const ranked = [];
  for (const entry of entries) {
    const title = normalizeSearch(entry.title);
    const path = normalizeSearch(entry.path);
    const text = normalizeSearch(entry.text);
    const haystack = `${title} ${path} ${text}`;
    if (!terms.every((term) => haystack.includes(term))) continue;

    let score = 0;
    if (title === normalizedQuery) score += 700;
    else if (title.startsWith(normalizedQuery)) score += 420;
    else if (title.includes(normalizedQuery)) score += 260;
    if (text.includes(normalizedQuery)) score += 80;
    if (entry.entity) score += 35;
    else if (entry.kind === "section") score += 18;
    for (const term of terms) {
      if (title === term) score += 120;
      else if (title.startsWith(term)) score += 80;
      else if (title.includes(term)) score += 45;
      if (path.includes(term)) score += 22;
      let at = text.indexOf(term);
      let occurrences = 0;
      while (at >= 0 && occurrences < 12) {
        occurrences += 1;
        at = text.indexOf(term, at + term.length);
      }
      score += Math.min(occurrences, 12);
    }
    ranked.push({
      ...entry,
      score,
      snippet: searchSnippet(entry.text, text, terms, normalizedQuery),
    });
  }
  ranked.sort((a, b) => b.score - a.score
    || a.title.localeCompare(b.title, ENGLISH ? "en" : "ru")
    || a.path.localeCompare(b.path));
  return { terms, results: ranked.slice(0, 30), total: ranked.length };
}

function clearSearch() {
  if (!searchElements) return;
  searchElements.input.value = "";
  searchElements.input.removeAttribute("aria-busy");
  searchElements.results.hidden = true;
  searchElements.results.replaceChildren();
  searchElements.tree.hidden = false;
  searchElements.status.textContent = "";
}

function renderSearchResults(query, ranked) {
  const { input, results, status, tree } = searchElements;
  input.removeAttribute("aria-busy");
  results.replaceChildren();
  tree.hidden = true;
  results.hidden = false;

  if (!ranked.total) {
    status.textContent = UI.searchEmpty(query);
    return;
  }
  status.textContent = ranked.total > ranked.results.length
    ? `${UI.searchResults(ranked.total)} · ${UI.searchShown(ranked.results.length)}`
    : UI.searchResults(ranked.total);

  for (const result of ranked.results) {
    const link = document.createElement("a");
    link.className = "md-search-result";
    const fragment = result.fragment
      ? `#${encodeURIComponent(result.fragment)}`
      : "";
    link.href = result.entity
      ? `?entity=${encodeURIComponent(result.entity)}`
      : `?p=${encodeURIComponent(result.path)}${fragment}`;

    const title = document.createElement("strong");
    appendHighlightedText(title, result.title, ranked.terms);
    const path = document.createElement("span");
    path.className = "md-search-result-path";
    path.textContent = result.kindLabel
      || (result.kind === "section"
        ? `${readablePath(result.path, result.pageTitle)} › ${UI.sectionOverview}`
        : readablePath(result.path));
    const snippet = document.createElement("span");
    snippet.className = "md-search-result-snippet";
    appendHighlightedText(snippet, result.snippet, ranked.terms);
    link.append(title, path, snippet);
    link.addEventListener("click", (event) => {
      event.preventDefault();
      history.pushState({}, "", link.href);
      clearSearch();
      closeMobileDrawer();
      if (result.entity) openEntity(result.entity);
      else openFile(result.path);
    });

    const item = document.createElement("li");
    item.appendChild(link);
    results.appendChild(item);
  }
}

function setupSearch() {
  const tree = $("#md-sidebar");
  const panel = document.createElement("div");
  panel.className = "md-search";

  const field = document.createElement("div");
  field.className = "md-search-field";
  const input = document.createElement("input");
  input.id = "md-search-input";
  input.type = "text";
  input.autocomplete = "off";
  input.spellcheck = false;
  input.placeholder = currentSection().startsWith("docs")
    ? UI.searchPlaceholder
    : (ENGLISH ? "Search documentation…" : "Поиск по документации…");
  input.setAttribute("aria-label", UI.searchLabel);
  input.setAttribute("aria-controls", "md-search-results");
  field.append(input);

  const status = document.createElement("div");
  status.className = "md-search-status";
  status.setAttribute("aria-live", "polite");
  const results = document.createElement("ol");
  results.id = "md-search-results";
  results.className = "md-search-results";
  results.hidden = true;

  panel.append(field, status, results);
  tree.before(panel);
  searchElements = { input, results, status, tree };

  let timer = 0;
  input.addEventListener("input", () => {
    window.clearTimeout(timer);
    const query = input.value.trim();
    if (query.length < 2) {
      input.removeAttribute("aria-busy");
      results.hidden = true;
      results.replaceChildren();
      tree.hidden = false;
      status.textContent = "";
      return;
    }
    input.setAttribute("aria-busy", "true");
    status.textContent = UI.searchLoading;
    timer = window.setTimeout(async () => {
      try {
        const index = await loadSearchIndex();
        if (input.value.trim() !== query) return;
        renderSearchResults(query, rankSearchEntries(index.entries, query));
      } catch (error) {
        input.removeAttribute("aria-busy");
        status.textContent = UI.searchError(error.message);
      }
    }, 140);
  });
  document.addEventListener("keydown", (event) => {
    const editing = /^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement?.tagName)
      || document.activeElement?.isContentEditable;
    if (event.key === "/" && !editing && !event.ctrlKey && !event.metaKey && !event.altKey) {
      event.preventDefault();
      input.focus();
      input.select();
    } else if (event.key === "Escape" && (document.activeElement === input || input.value)) {
      clearSearch();
      input.blur();
    }
  });
}

function pathToTree(entries) {
  const root = { children: new Map(), files: [], name: "" };
  for (const e of entries) {
    const parts = e.path.split("/");
    let node = root;
    for (let i = 0; i < parts.length - 1; i++) {
      const seg = parts[i];
      if (!node.children.has(seg)) {
        node.children.set(seg, { children: new Map(), files: [], name: seg });
      }
      node = node.children.get(seg);
    }
    node.files.push({ name: parts[parts.length - 1], entry: e });
  }
  return root;
}

function renderTree(node, depth = 0) {
  const container = document.createElement("ul");
  container.className = "md-tree";
  if (depth === 0) container.classList.add("md-tree-root");

  // Dirs first
  for (const [name, child] of [...node.children.entries()].sort()) {
    const li = document.createElement("li");
    li.className = "md-tree-dir";
    const head = document.createElement("div");
    head.className = "md-tree-dir-head";
    head.textContent = directoryLabel(name);
    head.dataset.segment = name;
    const sub = renderTree(child, depth + 1);
    sub.hidden = depth > 0;  // top-level expanded, deeper collapsed by default
    head.addEventListener("click", () => {
      sub.hidden = !sub.hidden;
      head.classList.toggle("md-tree-collapsed", sub.hidden);
    });
    if (sub.hidden) head.classList.add("md-tree-collapsed");
    li.appendChild(head);
    li.appendChild(sub);
    container.appendChild(li);
  }

  // Then files
  for (const f of node.files.sort((a, b) => a.name.localeCompare(b.name))) {
    if (depth === 0 && f.name === "README.md") continue;
    const li = document.createElement("li");
    li.className = "md-tree-file";
    const a = document.createElement("a");
    a.textContent = f.name === "README.md" ? UI.sectionOverview : f.entry.title;
    a.href = `?p=${encodeURIComponent(f.entry.path)}`;
    a.dataset.path = f.entry.path;
    a.addEventListener("click", (ev) => {
      ev.preventDefault();
      history.pushState({}, "", a.href);
      closeMobileDrawer();
      openFile(f.entry.path);
    });
    li.appendChild(a);
    container.appendChild(li);
  }

  return container;
}

function highlightActive() {
  for (const a of document.querySelectorAll(".md-tree-file a")) {
    a.classList.toggle("md-active", a.dataset.path === currentPath);
  }
}

function autoExpandFor(path) {
  // Make sure every parent dir of the active file is expanded.
  const parts = (path || "").split("/");
  if (parts.length < 2) return;
  const dirs = document.querySelectorAll(".md-tree-dir");
  for (const li of dirs) {
    const head = li.querySelector(":scope > .md-tree-dir-head");
    if (head && parts.includes(head.dataset.segment)) {
      const sub = li.querySelector(":scope > ul");
      if (sub) sub.hidden = false;
      head.classList.remove("md-tree-collapsed");
    }
  }
}

const REPO_GITHUB_BLOB = "https://github.com/anyalink99/cossacks-3-almanac/blob/main";

function currentSection() {
  const m = location.pathname.match(/\/(docs_en|internals_en|docs|internals)(?=\/|$)/);
  return m ? m[1] : "docs";
}

function updateLanguageSwitchRoute() {
  const languageSwitch = document.querySelector("#language-switch");
  if (!languageSwitch) return;
  const section = currentSection();
  const counterpart = {
    docs: "docs_en",
    docs_en: "docs",
    internals: "internals_en",
    internals_en: "internals",
  }[section];
  languageSwitch.textContent = ENGLISH ? "RU" : "EN";
  const query = currentEntity
    ? `?entity=${encodeURIComponent(currentEntity)}`
    : (currentPath ? `?p=${encodeURIComponent(currentPath)}${location.hash}` : "");
  languageSwitch.href = `../${counterpart}/${query}`;
}

function normalizePathParts(parts) {
  const out = [];
  for (const p of parts) {
    if (p === "" || p === ".") continue;
    if (p === "..") {
      if (out.length && out[out.length - 1] !== "..") out.pop();
      else out.push("..");
    } else {
      out.push(p);
    }
  }
  return out;
}

// Resolve a markdown <a href="..."> against the file currently rendered.
//   currentFile : relative path within section (e.g. "engine/native_api.md")
//   href        : href as written in markdown
// Returns one of:
//   { kind: "section", section, path }  — viewable in our viewer
//   { kind: "github",  path }           — outside both sections, link to repo
//   { kind: "external", url }           — http(s) / mailto / anchor — keep as is
function resolveHref(currentFile, href) {
  if (!href) return { kind: "external", url: href };
  if (/^[a-z]+:/i.test(href) || href.startsWith("#") || href.startsWith("mailto:")) {
    return { kind: "external", url: href };
  }

  const hashAt = href.indexOf("#");
  const fragment = hashAt >= 0 ? href.slice(hashAt) : "";
  const hrefPath = hashAt >= 0 ? href.slice(0, hashAt) : href;
  let parts;
  if (hrefPath.startsWith("/")) {
    parts = hrefPath.replace(/^\/+/, "").split("/");
  } else {
    const dirParts = currentFile.includes("/")
      ? currentFile.split("/").slice(0, -1)
      : [];
    parts = dirParts.concat(hrefPath.split("/"));
  }
  parts = normalizePathParts(parts);

  const escapes = parts.filter(p => p === "..").length;
  const tail = parts.slice(escapes);

  if (escapes === 0) {
    return {
      kind: "section",
      section: currentSection(),
      path: tail.join("/"),
      fragment,
    };
  }
  if (tail.length && ["docs", "internals", "docs_en", "internals_en"].includes(tail[0])) {
    return {
      kind: "section",
      section: tail[0],
      path: tail.slice(1).join("/"),
      fragment,
    };
  }
  return { kind: "github", path: tail.join("/"), fragment };
}

function rewriteRelativeLinks(html, basePath) {
  const section = currentSection();
  const div = document.createElement("div");
  div.innerHTML = html;

  for (const a of div.querySelectorAll("a[href]")) {
    const href = a.getAttribute("href");
    const resolved = resolveHref(basePath, href);
    if (resolved.kind === "external") continue;

    if (resolved.kind === "github") {
      a.setAttribute("href", `${REPO_GITHUB_BLOB}/${resolved.path}${resolved.fragment}`);
      a.setAttribute("target", "_blank");
      a.setAttribute("rel", "noopener");
      continue;
    }

    // kind === "section"
    const isMd = resolved.path.endsWith(".md");
    if (!isMd) {
      // Non-.md assets inside a section (rare — e.g. images, JSON manifests).
      // Send those to GitHub too — Pages might serve them, but the user
      // asked for non-doc links to land on the repo.
      a.setAttribute(
        "href",
        `${REPO_GITHUB_BLOB}/${resolved.section}/${resolved.path}`
      );
      a.setAttribute("target", "_blank");
      a.setAttribute("rel", "noopener");
      continue;
    }

    if (resolved.section === section) {
      const url = `?p=${encodeURIComponent(resolved.path)}${resolved.fragment}`;
      a.setAttribute("href", url);
      a.addEventListener("click", (ev) => {
        ev.preventDefault();
        history.pushState({}, "", url);
        closeMobileDrawer();
        openFile(resolved.path);
      });
    } else {
      // Cross-section: hand off to sibling section's viewer page.
      a.setAttribute(
        "href",
        `../${resolved.section}/?p=${encodeURIComponent(resolved.path)}${resolved.fragment}`
      );
    }
  }

  for (const img of div.querySelectorAll("img[src]")) {
    const src = img.getAttribute("src");
    if (!src || /^[a-z]+:/i.test(src) || src.startsWith("data:")) continue;
    const r = resolveHref(basePath, src);
    if (r.kind === "section") {
      img.setAttribute("src", r.path);  // resolved within section's dir
    } else if (r.kind === "github") {
      img.setAttribute(
        "src",
        `https://raw.githubusercontent.com/anyalink99/cossacks-3-almanac/main/${r.path}`
      );
    }
  }
  return div.innerHTML;
}

function editDistance(a, b) {
  if (a === b) return 0;
  if (!a.length) return b.length;
  if (!b.length) return a.length;
  let previous = Array.from({ length: b.length + 1 }, (_, index) => index);
  for (let i = 1; i <= a.length; i += 1) {
    const current = [i];
    for (let j = 1; j <= b.length; j += 1) {
      current[j] = Math.min(
        current[j - 1] + 1,
        previous[j] + 1,
        previous[j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1),
      );
    }
    previous = current;
  }
  return previous[b.length];
}

function findHashTarget(id) {
  const direct = document.getElementById(id)
    || document.querySelector(`[name="${CSS.escape(id)}"]`);
  if (direct) return direct;

  // A translated TOC can temporarily retain an older source-language slug.
  // Its visible label still matches the translated heading, so use that
  // relationship as a safe fallback when both sides are unique.
  const matchingLinks = [...document.querySelectorAll('#md-content a[href*="#"]')]
    .filter((link) => {
      const href = link.getAttribute("href") || "";
      const fragment = href.split("#", 2)[1];
      if (!fragment) return false;
      try {
        return decodeURIComponent(fragment) === id;
      } catch {
        return fragment === id;
      }
    });
  if (matchingLinks.length === 1) {
    const labelSlug = headingSlug(matchingLinks[0].textContent);
    const matchingHeadings = [...document.querySelectorAll(
      "#md-content h1, #md-content h2, #md-content h3, " +
      "#md-content h4, #md-content h5, #md-content h6"
    )].filter((heading) => headingSlug(heading.textContent) === labelSlug);
    if (matchingHeadings.length === 1) return matchingHeadings[0];
  }

  // Old published links occasionally contain a one-character slug typo.
  // Resolve only a unique, very close match; never guess between headings.
  const candidates = [...document.querySelectorAll("#md-content [id]")]
    .map((element) => ({ element, distance: editDistance(id, element.id) }))
    .sort((a, b) => a.distance - b.distance);
  const threshold = id.length >= 12 ? 2 : 1;
  if (!candidates.length || candidates[0].distance > threshold) return null;
  if (candidates[1]?.distance === candidates[0].distance) return null;
  return candidates[0].element;
}

function scrollToCurrentHash() {
  if (!location.hash) return;
  let id;
  try {
    id = decodeURIComponent(location.hash.slice(1));
  } catch {
    id = location.hash.slice(1);
  }
  window.requestAnimationFrame(() => {
    const target = findHashTarget(id);
    target?.scrollIntoView({ block: "start" });
  });
}

function makeElement(tag, className = "", text = "") {
  const element = document.createElement(tag);
  if (className) element.className = className;
  if (text !== "") element.textContent = text;
  return element;
}

function localized(value) {
  if (!value || typeof value !== "object") return String(value ?? "");
  return value[ENGLISH ? "en" : "ru"] || value.en || value.ru || "";
}

function entityRecord(catalog, entityKey) {
  const separator = entityKey.indexOf(":");
  if (separator < 1) return null;
  const kind = entityKey.slice(0, separator);
  const sid = entityKey.slice(separator + 1);
  return catalog.entities?.[kind]?.[sid] || null;
}

function removeRedundantLanguageRow(container, path) {
  if (path !== "README.md" || !currentSection().startsWith("docs")) return;
  const firstParagraph = container.querySelector("h1 + p");
  if (!firstParagraph) return;
  const label = firstParagraph.textContent.replace(/\s+/g, " ").trim();
  if (/^(?:English · Русский|Русский · English)$/.test(label)) {
    firstParagraph.remove();
  }
}

async function enrichEntityTables(container, path) {
  const tables = [...container.querySelectorAll("table")];
  if (!tables.length || !currentSection().startsWith("docs")) return;
  const index = await loadEntityIndex();
  if (currentPath !== path || !container.isConnected) return;

  for (const table of tables) {
    const rows = [...table.tBodies].flatMap((body) => [...body.rows]);
    const showIcons = rows.length <= 160;
    for (const row of rows) {
      const matches = [...row.querySelectorAll("code")]
        .filter((code) => !code.closest("a"))
        .map((code) => {
          const sid = code.textContent.trim();
          const entry = sid && index.entities?.[sid];
          return entry ? { code, sid, entry } : null;
        })
        .filter(Boolean);
      const uniqueMatches = new Map(
        matches.map((match) => [`${match.entry[0]}:${match.sid}`, match]),
      );
      if (uniqueMatches.size !== 1) continue;

      const [{ code: sidCode, sid, entry }] = uniqueMatches.values();
      const [kind, name, icon] = entry;
      const sidCell = sidCode.closest("td, th");
      if (!sidCell) continue;

      let cell = sidCell;
      const readerLabel = sidCell.textContent.replace(sid, "").trim();
      if (!readerLabel) {
        const normalizedName = normalizeSearch(name.trim());
        cell = [...row.cells].find((candidate) => {
          if (candidate === sidCell || candidate.querySelector("a, code")) return false;
          return normalizeSearch(candidate.textContent.trim()) === normalizedName;
        });
      }
      if (!cell || cell.querySelector("a")) continue;

      // Do not turn an unrelated label into a card link merely because the row
      // contains an entity SID in a statistics or relationship column.
      if (cell !== sidCell && normalizeSearch(cell.textContent.trim()) !== normalizeSearch(name)) {
        continue;
      }

      const key = `${kind}:${sid}`;
      const link = makeElement("a", "entity-table-link");
      link.href = `?entity=${encodeURIComponent(key)}`;
      link.dataset.entityKey = key;
      link.setAttribute(
        "aria-label",
        `${name} — ${ENTITY_UI.kinds[kind]}`
      );

      if (showIcons && icon) {
        const image = document.createElement("img");
        image.className = "entity-table-icon";
        image.src = icon;
        image.alt = "";
        image.width = 26;
        image.height = 26;
        image.loading = "lazy";
        image.decoding = "async";
        link.append(image);
      }

      const label = makeElement("span", "entity-table-label");
      const existing = [...cell.childNodes];
      const cellHasReaderLabel = cell.textContent.replace(sid, "").trim();
      if (cellHasReaderLabel) {
        label.append(...existing);
      } else {
        label.append(
          makeElement("strong", "", name),
          document.createTextNode(" "),
          ...existing,
        );
      }
      link.append(label);
      cell.replaceChildren(link);
    }
  }
}

function setupEntityNavigation() {
  $("#md-content").addEventListener("click", (event) => {
    const link = event.target.closest("a[data-entity-key]");
    if (!link) return;
    event.preventDefault();
    const key = link.dataset.entityKey;
    history.pushState({}, "", `?entity=${encodeURIComponent(key)}`);
    openEntity(key);
  });
}

function entityBySid(catalog, sid) {
  for (const kind of ["unit", "building", "upgrade"]) {
    if (catalog.entities?.[kind]?.[sid]) {
      return catalog.entities[kind][sid];
    }
  }
  return null;
}

function entityLink(entity, label = "") {
  const link = makeElement("a", "entity-related-link", label || localized(entity.name));
  const key = `${entity.kind}:${entity.sid}`;
  link.href = `?entity=${encodeURIComponent(key)}`;
  link.addEventListener("click", (event) => {
    event.preventDefault();
    history.pushState({}, "", link.href);
    openEntity(key);
  });
  return link;
}

function appendFact(container, label, value) {
  if (value === undefined || value === null || value === "") return;
  const item = makeElement("div", "entity-fact");
  item.append(makeElement("dt", "", label));
  const description = makeElement("dd");
  if (value instanceof Node) description.append(value);
  else description.textContent = value;
  item.append(description);
  container.append(item);
}

function resourceList(cost) {
  const container = makeElement("span", "entity-resource-list");
  for (const [resource, value] of Object.entries(cost || {})) {
    const chip = makeElement("span", `entity-resource entity-resource-${resource}`);
    chip.append(
      makeElement("span", "entity-resource-name", ENTITY_UI.resources[resource] || resource),
      makeElement("strong", "", String(value)),
    );
    container.append(chip);
  }
  return container;
}

function relatedList(values, catalog) {
  const container = makeElement("span", "entity-related-list");
  const groups = new Map();
  for (const sid of [...new Set(values || [])]) {
    const entity = entityBySid(catalog, sid);
    if (!entity) {
      groups.set(`raw:${sid}`, { label: sid, entities: [] });
      continue;
    }
    const label = localized(entity.name);
    const key = `${entity.kind}:${normalizeSearch(label)}`;
    const group = groups.get(key) || { label, entities: [] };
    group.entities.push(entity);
    groups.set(key, group);
  }
  for (const group of groups.values()) {
    if (group.entities.length === 1) {
      container.append(entityLink(group.entities[0], group.label));
    } else if (group.entities.length > 1) {
      // Nation-specific buildings and units often share one canonical name.
      // A single neutral label is more honest than linking to an arbitrary
      // national implementation.
      container.append(makeElement("span", "entity-related-label", group.label));
    } else {
      container.append(makeElement("code", "entity-related-plain", group.label));
    }
  }
  return container;
}

function nationsLabel(values, catalog) {
  const selected = new Set(values || []);
  const allNations = Object.keys(catalog.nations || {});
  if (selected.size === allNations.length) return ENTITY_UI.allNations;

  const labels = (sids) => sids
    .map((sid) => localized(catalog.nations?.[sid]) || sid.toUpperCase())
    .sort((a, b) => a.localeCompare(b, ENGLISH ? "en" : "ru"))
    .join(", ");
  const missing = allNations.filter((sid) => !selected.has(sid));
  if (missing.length && missing.length < selected.size) {
    return ENTITY_UI.allExcept(labels(missing));
  }
  return labels([...selected]);
}

const ENTITY_VARIANT_KEYS = {
  unit: [
    "hp", "buildtime_sec", "speed", "vision", "cost",
    "trained_in", "protection", "weapons",
  ],
  building: [
    "hp", "buildtime_sec", "vision", "farm", "peasantabsorber",
    "capturable", "cost", "produces",
  ],
  upgrade: [
    "effect", "value", "level", "time_sec", "cost",
    "place", "targets", "prereqs",
  ],
};

const ENTITY_RELATION_FIELDS = new Set([
  "trained_in", "produces", "place", "targets", "prereqs",
]);

function stableValue(value) {
  if (Array.isArray(value)) return value.map(stableValue);
  if (value && typeof value === "object") {
    return Object.fromEntries(
      Object.keys(value).sort().map((key) => [key, stableValue(value[key])]),
    );
  }
  return value ?? null;
}

function relationValues(value) {
  if (value === undefined || value === null || value === "") return [];
  return Array.isArray(value) ? value : [value];
}

function variantFieldSignature(field, value, catalog) {
  if (!ENTITY_RELATION_FIELDS.has(field)) {
    return JSON.stringify(stableValue(value));
  }
  const semanticNames = relationValues(value).map((sid) => {
    const related = entityBySid(catalog, sid);
    return related
      ? `${related.kind}:${normalizeSearch(localized(related.name))}`
      : `raw:${sid}`;
  });
  return JSON.stringify([...new Set(semanticNames)].sort());
}

function displayVariantSignature(entity, variant, catalog) {
  return JSON.stringify(
    ENTITY_VARIANT_KEYS[entity.kind].map((field) => [
      field,
      variantFieldSignature(field, variant[field], catalog),
    ]),
  );
}

function mergeRelatedFields(target, source) {
  for (const field of ENTITY_RELATION_FIELDS) {
    const merged = [
      ...relationValues(target[field]),
      ...relationValues(source[field]),
    ];
    if (merged.length) target[field] = [...new Set(merged)].sort();
  }
}

function groupDisplayVariants(entity, catalog) {
  const groups = new Map();
  for (const source of entity.variants || []) {
    const signature = displayVariantSignature(entity, source, catalog);
    let group = groups.get(signature);
    if (!group) {
      group = JSON.parse(JSON.stringify(source));
      group.nations = [];
      groups.set(signature, group);
    }
    group.nations = [...new Set([
      ...(group.nations || []),
      ...(source.nations || []),
    ])].sort();
    mergeRelatedFields(group, source);
  }
  return [...groups.entries()]
    .sort((a, b) => b[1].nations.length - a[1].nations.length
      || a[0].localeCompare(b[0]))
    .map(([, variant]) => variant);
}

function variantDifferenceKeys(entity, variant, baseline, catalog) {
  return new Set(ENTITY_VARIANT_KEYS[entity.kind].filter(
    (field) => variantFieldSignature(field, variant[field], catalog)
      !== variantFieldSignature(field, baseline[field], catalog),
  ));
}

function protectionList(protection) {
  const container = makeElement("span", "entity-protection-list");
  for (const [key, value] of Object.entries(protection || {})) {
    const kind = key.replace(/^prot_/, "");
    const chip = makeElement("span", "entity-protection");
    chip.append(
      makeElement("span", "", ENTITY_UI.weaponKinds[kind] || kind),
      makeElement("strong", "", String(value)),
    );
    container.append(chip);
  }
  return container;
}

function renderWeapons(weapons) {
  const section = makeElement("section", "entity-detail-section");
  section.append(makeElement("h3", "", ENTITY_UI.weapons));
  const list = makeElement("div", "entity-weapons");
  for (const weapon of weapons) {
    const item = makeElement("div", "entity-weapon");
    item.append(makeElement(
      "strong",
      "entity-weapon-name",
      ENTITY_UI.weaponKinds[weapon.kind] || weapon.kind || ENTITY_UI.weapons,
    ));
    const facts = makeElement("dl", "entity-weapon-facts");
    appendFact(facts, ENTITY_UI.damage, weapon.damage);
    appendFact(
      facts,
      ENTITY_UI.reload,
      weapon.pause_sec != null ? `${weapon.pause_sec} ${ENTITY_UI.gameSeconds}` : null,
    );
    const min = weapon.radiusmin_tiles;
    const max = weapon.radiusmax_tiles;
    const range = max != null
      ? `${min != null ? `${min}–` : ""}${max} ${ENTITY_UI.tiles}`
      : null;
    appendFact(facts, ENTITY_UI.range, range);
    if (weapon.cost) appendFact(facts, ENTITY_UI.cost, resourceList(weapon.cost));
    item.append(facts);
    list.append(item);
  }
  section.append(list);
  return section;
}

function renderVariant(entity, variant, catalog, title, visibleKeys = null) {
  const section = makeElement("section", "entity-variant");
  const heading = makeElement("div", "entity-variant-heading");
  heading.append(
    makeElement("h2", "", title),
    makeElement("span", "entity-nations", nationsLabel(variant.nations, catalog)),
  );
  section.append(heading);

  const shows = (field) => !visibleKeys || visibleKeys.has(field);
  const facts = makeElement("dl", "entity-facts");
  if (entity.kind === "unit") {
    if (shows("hp")) appendFact(facts, ENTITY_UI.health, variant.hp);
    if (shows("buildtime_sec")) {
      appendFact(
        facts,
        ENTITY_UI.trainingTime,
        variant.buildtime_sec != null
          ? `${variant.buildtime_sec} ${ENTITY_UI.gameSeconds}`
          : null,
      );
    }
    if (shows("speed")) appendFact(facts, ENTITY_UI.speed, variant.speed);
    if (shows("vision")) appendFact(facts, ENTITY_UI.vision, variant.vision);
    if (shows("cost") && variant.cost) {
      appendFact(facts, ENTITY_UI.cost, resourceList(variant.cost));
    }
    if (shows("trained_in") && variant.trained_in) {
      appendFact(facts, ENTITY_UI.trainedAt, relatedList(variant.trained_in, catalog));
    }
    if (shows("protection") && variant.protection) {
      appendFact(facts, ENTITY_UI.protection, protectionList(variant.protection));
    }
  } else if (entity.kind === "building") {
    if (shows("hp")) appendFact(facts, ENTITY_UI.health, variant.hp);
    if (shows("buildtime_sec")) {
      appendFact(
        facts,
        ENTITY_UI.buildTime,
        variant.buildtime_sec != null
          ? `${variant.buildtime_sec} ${ENTITY_UI.gameSeconds}`
          : null,
      );
    }
    if (shows("vision")) appendFact(facts, ENTITY_UI.vision, variant.vision);
    if (shows("farm")) appendFact(facts, ENTITY_UI.housing, variant.farm);
    if (shows("peasantabsorber")) {
      appendFact(facts, ENTITY_UI.capacity, variant.peasantabsorber);
    }
    if (shows("capturable") && variant.capturable) {
      appendFact(facts, ENTITY_UI.canBeCaptured, ENTITY_UI.yes);
    }
    if (shows("cost") && variant.cost) {
      appendFact(facts, ENTITY_UI.cost, resourceList(variant.cost));
    }
    if (shows("produces") && variant.produces) {
      appendFact(facts, ENTITY_UI.produces, relatedList(variant.produces, catalog));
    }
  } else {
    if (shows("effect")) appendFact(facts, ENTITY_UI.effect, localized(variant.effect));
    if (shows("value")) appendFact(facts, ENTITY_UI.value, variant.value);
    if (shows("level")) appendFact(facts, ENTITY_UI.level, variant.level);
    if (shows("time_sec")) {
      appendFact(
        facts,
        ENTITY_UI.researchTime,
        variant.time_sec != null ? `${variant.time_sec} ${ENTITY_UI.gameSeconds}` : null,
      );
    }
    if (shows("cost") && variant.cost) {
      appendFact(facts, ENTITY_UI.cost, resourceList(variant.cost));
    }
    const place = relationValues(variant.place);
    if (shows("place") && place.length) {
      appendFact(facts, ENTITY_UI.researchedAt, relatedList(place, catalog));
    }
    if (shows("targets") && variant.targets?.length) {
      appendFact(facts, ENTITY_UI.affects, relatedList(variant.targets, catalog));
    }
    if (shows("prereqs") && variant.prereqs?.length) {
      appendFact(facts, ENTITY_UI.prerequisites, relatedList(variant.prereqs, catalog));
    }
  }
  if (facts.childElementCount) section.append(facts);
  if (entity.kind === "unit" && shows("weapons") && variant.weapons?.length) {
    section.append(renderWeapons(variant.weapons));
  }
  return section;
}

async function openEntity(entityKey) {
  currentEntity = entityKey;
  currentPath = null;
  updateLanguageSwitchRoute();
  const main = $("#md-content");
  const crumb = $("#md-crumbs");
  crumb.textContent = ENTITY_UI.catalog;
  main.replaceChildren(makeElement("div", "md-loading", UI.catalogLoading));
  try {
    const catalog = await loadEntityCatalog();
    const entity = entityRecord(catalog, entityKey);
    if (!entity) throw new Error(`unknown entity ${entityKey}`);

    const card = makeElement("article", "entity-card");
    const hero = makeElement("header", "entity-hero");
    if (entity.icon) {
      const frame = makeElement("div", "entity-icon-frame");
      const image = document.createElement("img");
      image.src = entity.icon;
      image.alt = "";
      image.width = 46;
      image.height = 46;
      frame.append(image);
      hero.append(frame);
    }
    const identity = makeElement("div", "entity-identity");
    identity.append(
      makeElement("span", `entity-kind entity-kind-${entity.kind}`, ENTITY_UI.kinds[entity.kind]),
      makeElement("h1", "", localized(entity.name)),
    );
    const sid = makeElement("div", "entity-sid");
    sid.append(
      makeElement("span", "", `${ENTITY_UI.technicalId}: `),
      makeElement("code", "", entity.sid),
    );
    identity.append(sid);
    hero.append(identity);
    card.append(hero);

    const displayVariants = groupDisplayVariants(entity, catalog);
    if (displayVariants.length === 1) {
      card.append(renderVariant(
        entity,
        displayVariants[0],
        catalog,
        ENTITY_UI.variant,
      ));
    } else {
      const baseline = displayVariants[0];
      card.append(renderVariant(
        entity,
        baseline,
        catalog,
        ENTITY_UI.baseValues,
      ));
      displayVariants.slice(1).forEach((variant, index) => {
        const title = displayVariants.length > 2
          ? `${ENTITY_UI.differences} ${index + 1}`
          : ENTITY_UI.differences;
        card.append(renderVariant(
          entity,
          variant,
          catalog,
          title,
          variantDifferenceKeys(entity, variant, baseline, catalog),
        ));
      });
    }
    main.replaceChildren(card);
    crumb.textContent = `${ENTITY_UI.catalog} › ${ENTITY_UI.kinds[entity.kind]} › ${localized(entity.name)}`;
    document.title = `${localized(entity.name)} — ${currentRoot.title}`;
    window.scrollTo({ top: 0 });
  } catch (error) {
    main.replaceChildren(makeElement("div", "md-error", UI.catalogError(error.message)));
  }
  highlightActive();
}

async function openFile(path) {
  currentEntity = null;
  currentPath = path;
  updateLanguageSwitchRoute();
  const main = $("#md-content");
  const crumb = $("#md-crumbs");
  crumb.textContent = readablePath(path);
  main.innerHTML = `<div class="md-loading">${UI.loading(path)}</div>`;
  try {
    const r = await fetch(path);
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    const text = await r.text();
    const html = marked.parse(text);
    main.innerHTML = rewriteRelativeLinks(html, path);
    removeRedundantLanguageRow(main, path);
    assignHeadingIds(main);
    wrapTablesInScrollContainers(main);
    enrichEntityTables(main, path).catch(() => {
      // Entity cards are an enhancement; a missing compact index must not
      // make the underlying reference table unreadable.
    });
    await renderMermaidBlocks(main);
    const pageTitle = main.querySelector("h1")?.textContent?.trim()
      || path.split("/").pop().replace(".md", "");
    crumb.textContent = readablePath(path, pageTitle);
    if (location.hash) scrollToCurrentHash();
    else window.scrollTo({ top: 0 });
    document.title = pageTitle === currentRoot.title
      ? pageTitle
      : `${pageTitle} — ${currentRoot.title}`;
  } catch (e) {
    main.innerHTML = `<div class="md-error">${UI.loadError(`<code>${path}</code>`, e.message)}</div>`;
  }
  highlightActive();
  autoExpandFor(path);
}

let currentRoot = null;

function setupMobileDrawer() {
  const topbar = document.querySelector(".topbar");
  const actions = document.querySelector(".topbar-actions");
  const sidebar = document.querySelector(".md-sidebar");
  if (!topbar || !actions || !sidebar) return;

  sidebar.id = "md-navigation";
  const toggle = makeElement("button", "btn btn-secondary md-drawer-toggle", UI.contents);
  toggle.type = "button";
  toggle.setAttribute("aria-controls", sidebar.id);
  toggle.setAttribute("aria-expanded", "false");
  actions.prepend(toggle);

  const backdrop = makeElement("div", "md-drawer-backdrop");
  backdrop.setAttribute("aria-hidden", "true");
  topbar.after(backdrop);

  const updateTopbarHeight = () => {
    document.documentElement.style.setProperty(
      "--md-topbar-height",
      `${Math.ceil(topbar.getBoundingClientRect().height)}px`,
    );
  };
  updateTopbarHeight();
  const observer = new ResizeObserver(updateTopbarHeight);
  observer.observe(topbar);

  const setOpen = (open) => {
    document.body.classList.toggle("md-drawer-open", open);
    toggle.setAttribute("aria-expanded", String(open));
    toggle.textContent = open ? UI.closeContents : UI.contents;
    backdrop.setAttribute("aria-hidden", String(!open));
  };
  closeMobileDrawer = () => setOpen(false);
  toggle.addEventListener("click", () => {
    setOpen(!document.body.classList.contains("md-drawer-open"));
  });
  backdrop.addEventListener("click", closeMobileDrawer);
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && document.body.classList.contains("md-drawer-open")) {
      closeMobileDrawer();
      toggle.focus();
    }
  });
  window.addEventListener("resize", () => {
    if (window.innerWidth > 900) closeMobileDrawer();
  });
}

async function init() {
  try {
    const section = currentSection();
    applyLegacyReferenceRoute();
    document.documentElement.lang = ENGLISH ? "en" : "ru";
    const home = document.querySelector(".topbar-actions .btn-secondary");
    const contents = document.querySelector(".md-sidebar h2");
    if (home) home.textContent = UI.home;
    if (contents) contents.textContent = UI.contents;
    updateLanguageSwitchRoute();
    const manifest = await loadManifest();
    currentRoot = manifest;
    $("#md-root-title").textContent = manifest.title;
    document.title = manifest.title;

    setupMobileDrawer();
    setupSearch();
    setupEntityNavigation();
    const tree = pathToTree(manifest.entries);
    const treeEl = renderTree(tree);
    $("#md-sidebar").appendChild(treeEl);

    // Default to README.md if no path
    const initial = currentPath || manifest.entries.find((e) => e.path === "README.md")?.path
                                || manifest.entries[0]?.path;
    if (currentEntity && section.startsWith("docs")) {
      openEntity(currentEntity);
    } else if (initial) {
      currentPath = initial;
      openFile(initial);
    }

    window.addEventListener("popstate", () => {
      const next = new URLSearchParams(location.search);
      const entity = next.get("entity");
      const p = next.get("p");
      if (entity && entity !== currentEntity && section.startsWith("docs")) openEntity(entity);
      else if (p && p !== currentPath) openFile(p);
      else if (!entity && !p && initial && (currentEntity || currentPath !== initial)) {
        openFile(initial);
      }
      else scrollToCurrentHash();
    });
    window.addEventListener("hashchange", scrollToCurrentHash);
  } catch (e) {
    $("#md-content").innerHTML = `<div class="md-error">${UI.manifestError(e.message)}</div>`;
  }
}

init();
