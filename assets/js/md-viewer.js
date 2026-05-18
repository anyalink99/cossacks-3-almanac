// Markdown viewer used by docs/index.html and internals/index.html.
// Loads _manifest.json from the current directory, renders a sidebar
// tree, lets the user pick a file, fetches and renders it via marked.

import { marked } from "https://cdn.jsdelivr.net/npm/marked@13.0.3/+esm";
import markedFootnote from "https://cdn.jsdelivr.net/npm/marked-footnote@1.2.4/+esm";
import markedAlert from "https://cdn.jsdelivr.net/npm/marked-alert@2.1.2/+esm";
import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.esm.min.mjs";

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
      target.innerHTML = `<div class="md-error">Не удалось отрисовать mermaid: ${e.message}</div>` +
                         `<pre><code>${source.replace(/[<>&]/g, c => ({"<":"&lt;",">":"&gt;","&":"&amp;"}[c]))}</code></pre>`;
    }
  }
}

const $ = (sel) => document.querySelector(sel);

const params = new URLSearchParams(location.search);
let currentPath = params.get("p");

async function loadManifest() {
  const r = await fetch("_manifest.json");
  if (!r.ok) throw new Error(`manifest HTTP ${r.status}`);
  return r.json();
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
  const m = location.pathname.match(/\/(docs|internals)(?=\/|$)/);
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

  let parts;
  if (href.startsWith("/")) {
    parts = href.replace(/^\/+/, "").split("/");
  } else {
    const dirParts = currentFile.includes("/")
      ? currentFile.split("/").slice(0, -1)
      : [];
    parts = dirParts.concat(href.split("/"));
  }
  parts = normalizePathParts(parts);

  const escapes = parts.filter(p => p === "..").length;
  const tail = parts.slice(escapes);

  if (escapes === 0) {
    return { kind: "section", section: currentSection(), path: tail.join("/") };
  }
  if (tail.length && (tail[0] === "docs" || tail[0] === "internals")) {
    return { kind: "section", section: tail[0], path: tail.slice(1).join("/") };
  }
  return { kind: "github", path: tail.join("/") };
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
      a.setAttribute("href", `${REPO_GITHUB_BLOB}/${resolved.path}`);
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
      const url = `?p=${encodeURIComponent(resolved.path)}`;
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
        `../${resolved.section}/?p=${encodeURIComponent(resolved.path)}`
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

async function openFile(path) {
  currentPath = path;
  const main = $("#md-content");
  const crumb = $("#md-crumbs");
  crumb.textContent = path;
  main.innerHTML = `<div class="md-loading">Загружаем ${path}…</div>`;
  try {
    const r = await fetch(path);
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    const text = await r.text();
    const html = marked.parse(text);
    main.innerHTML = rewriteRelativeLinks(html, path);
    wrapTablesInScrollContainers(main);
    await renderMermaidBlocks(main);
    main.scrollTop = 0;
    document.title = `${path.split("/").pop().replace(".md", "")} — ${currentRoot.title}`;
  } catch (e) {
    main.innerHTML = `<div class="md-error">Не удалось загрузить <code>${path}</code>: ${e.message}</div>`;
  }
  highlightActive();
  autoExpandFor(path);
}

let currentRoot = null;

async function init() {
  try {
    const manifest = await loadManifest();
    currentRoot = manifest;
    $("#md-root-title").textContent = manifest.title;
    document.title = manifest.title;

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
    });
  } catch (e) {
    $("#md-content").innerHTML = `<div class="md-error">Не удалось загрузить манифест: ${e.message}</div>`;
  }
}

init();
