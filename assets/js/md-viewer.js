// Markdown viewer used by docs/index.html and internals/index.html.
// Loads _manifest.json from the current directory, renders a sidebar
// tree, lets the user pick a file, fetches and renders it via marked.

import { marked } from "https://cdn.jsdelivr.net/npm/marked@13.0.3/+esm";
import markedFootnote from "https://cdn.jsdelivr.net/npm/marked-footnote@1.2.4/+esm";
import markedAlert from "https://cdn.jsdelivr.net/npm/marked-alert@2.1.2/+esm";
import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.esm.min.mjs";

const ENGLISH = /\/(?:docs_en|internals_en)(?:\/|$)/.test(location.pathname);
const UI = ENGLISH ? {
  home: "Home",
  contents: "Contents",
  loading: (path) => `Loading ${path}…`,
  loadError: (path, message) => `Could not load ${path}: ${message}`,
  manifestError: (message) => `Could not load the manifest: ${message}`,
  mermaidError: (message) => `Could not render Mermaid: ${message}`,
  searchLabel: "Search",
  searchPlaceholder: "Search documentation…",
  searchLoading: "Loading the search index…",
  searchResults: (count) => `${count} result${count === 1 ? "" : "s"}`,
  searchShown: (count) => `${count} shown`,
  searchEmpty: (query) => `No matches for “${query}”`,
  searchError: (message) => `Search is unavailable: ${message}`,
} : {
  home: "На главную",
  contents: "Содержание",
  loading: (path) => `Загружаем ${path}…`,
  loadError: (path, message) => `Не удалось загрузить ${path}: ${message}`,
  manifestError: (message) => `Не удалось загрузить манифест: ${message}`,
  mermaidError: (message) => `Не удалось отрисовать mermaid: ${message}`,
  searchLabel: "Поиск",
  searchPlaceholder: "Поиск по документации…",
  searchLoading: "Загружаем поисковый индекс…",
  searchResults: (count) => `${count} совпадени${count % 10 === 1 && count % 100 !== 11 ? "е" : "й"}`,
  searchShown: (count) => `показано ${count}`,
  searchEmpty: (query) => `По запросу «${query}» ничего не найдено`,
  searchError: (message) => `Поиск недоступен: ${message}`,
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

// Marked emits raw <table>; if columns are wide the table overflows the
// article column without a scrollbar (unscrollable on touch + mouse).
// Wrap each table in a div with overflow-x: auto so wide tables become
// horizontally scrollable while narrow ones still look natural.
function wrapTablesInScrollContainers(container) {
  for (const table of container.querySelectorAll("table")) {
    if (table.parentElement?.classList.contains("md-table-scroll")) continue;
    const wrap = document.createElement("div");
    wrap.className = "md-table-scroll";
    table.replaceWith(wrap);
    wrap.appendChild(table);
  }
}

function headingSlug(value) {
  return value
    .trim()
    .toLocaleLowerCase(ENGLISH ? "en" : "ru")
    .replace(/[^\p{L}\p{N}\s_-]/gu, "")
    .replace(/\s+/g, "-");
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
let searchIndexPromise = null;
let searchElements = null;

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

function searchSnippet(text, normalizedText, terms) {
  let first = -1;
  for (const term of terms) {
    const at = normalizedText.indexOf(term);
    if (at >= 0 && (first < 0 || at < first)) first = at;
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
  const terms = normalizeSearch(query).split(/\s+/).filter(Boolean);
  const ranked = [];
  for (const entry of entries) {
    const title = normalizeSearch(entry.title);
    const path = normalizeSearch(entry.path);
    const text = normalizeSearch(entry.text);
    const haystack = `${title} ${path} ${text}`;
    if (!terms.every((term) => haystack.includes(term))) continue;

    let score = 0;
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
      snippet: searchSnippet(entry.text, text, terms),
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
    link.href = `?p=${encodeURIComponent(result.path)}`;

    const title = document.createElement("strong");
    appendHighlightedText(title, result.title, ranked.terms);
    const path = document.createElement("span");
    path.className = "md-search-result-path";
    path.textContent = result.path;
    const snippet = document.createElement("span");
    snippet.className = "md-search-result-snippet";
    appendHighlightedText(snippet, result.snippet, ranked.terms);
    link.append(title, path, snippet);
    link.addEventListener("click", (event) => {
      event.preventDefault();
      history.pushState({}, "", link.href);
      clearSearch();
      openFile(result.path);
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
  input.placeholder = UI.searchPlaceholder;
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
    head.textContent = name;
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
    const li = document.createElement("li");
    li.className = "md-tree-file";
    const a = document.createElement("a");
    a.textContent = f.entry.title;
    a.href = `?p=${encodeURIComponent(f.entry.path)}`;
    a.dataset.path = f.entry.path;
    a.addEventListener("click", (ev) => {
      ev.preventDefault();
      history.pushState({}, "", a.href);
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
    if (head && parts.includes(head.textContent)) {
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

async function openFile(path) {
  currentPath = path;
  const main = $("#md-content");
  const crumb = $("#md-crumbs");
  crumb.textContent = path;
  main.innerHTML = `<div class="md-loading">${UI.loading(path)}</div>`;
  try {
    const r = await fetch(path);
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    const text = await r.text();
    const html = marked.parse(text);
    main.innerHTML = rewriteRelativeLinks(html, path);
    assignHeadingIds(main);
    wrapTablesInScrollContainers(main);
    await renderMermaidBlocks(main);
    if (location.hash) scrollToCurrentHash();
    else window.scrollTo({ top: 0 });
    document.title = `${path.split("/").pop().replace(".md", "")} — ${currentRoot.title}`;
  } catch (e) {
    main.innerHTML = `<div class="md-error">${UI.loadError(`<code>${path}</code>`, e.message)}</div>`;
  }
  highlightActive();
  autoExpandFor(path);
}

let currentRoot = null;

async function init() {
  try {
    document.documentElement.lang = ENGLISH ? "en" : "ru";
    const home = document.querySelector(".topbar-actions .btn-secondary");
    const contents = document.querySelector(".md-sidebar h2");
    if (home) home.textContent = UI.home;
    if (contents) contents.textContent = UI.contents;
    const languageSwitch = document.querySelector("#language-switch");
    if (languageSwitch) {
      const section = currentSection();
      const counterpart = {
        docs: "docs_en",
        docs_en: "docs",
        internals: "internals_en",
        internals_en: "internals",
      }[section];
      languageSwitch.textContent = ENGLISH ? "RU" : "EN";
      const query = currentPath ? `?p=${encodeURIComponent(currentPath)}` : "";
      languageSwitch.href = `../${counterpart}/${query}`;
    }
    const manifest = await loadManifest();
    currentRoot = manifest;
    $("#md-root-title").textContent = manifest.title;
    document.title = manifest.title;

    setupSearch();
    const tree = pathToTree(manifest.entries);
    const treeEl = renderTree(tree);
    $("#md-sidebar").appendChild(treeEl);

    // Default to README.md if no path
    const initial = currentPath || manifest.entries.find((e) => e.path === "README.md")?.path
                                || manifest.entries[0]?.path;
    if (initial) {
      currentPath = initial;
      openFile(initial);
    }

    window.addEventListener("popstate", () => {
      const p = new URLSearchParams(location.search).get("p");
      if (p && p !== currentPath) openFile(p);
      else scrollToCurrentHash();
    });
    window.addEventListener("hashchange", scrollToCurrentHash);
  } catch (e) {
    $("#md-content").innerHTML = `<div class="md-error">${UI.manifestError(e.message)}</div>`;
  }
}

init();
