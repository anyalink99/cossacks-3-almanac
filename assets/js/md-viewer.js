// Markdown viewer used by docs/index.html and internals/index.html.
// Loads _manifest.json from the current directory, renders a sidebar
// tree, lets the user pick a file, fetches and renders it via marked.

import { marked } from "https://cdn.jsdelivr.net/npm/marked@13.0.3/+esm";

// --- Markdown configuration ----------------------------------------------
marked.setOptions({
  gfm: true,
  breaks: false,
  headerIds: true,
});

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

function rewriteRelativeLinks(html, basePath) {
  // basePath = relative path of currently rendered file, e.g. "recon/world/map/foo.md"
  const baseDir = basePath.includes("/")
    ? basePath.substring(0, basePath.lastIndexOf("/"))
    : "";
  const div = document.createElement("div");
  div.innerHTML = html;
  for (const a of div.querySelectorAll("a[href]")) {
    const href = a.getAttribute("href");
    if (!href || href.startsWith("http") || href.startsWith("#") || href.startsWith("mailto:")) continue;
    // Resolve relative to baseDir
    const resolved = new URL(href, "file:///root/" + baseDir + "/").pathname.replace(/^\/root\//, "");
    if (resolved.endsWith(".md")) {
      a.setAttribute("href", `?p=${encodeURIComponent(resolved)}`);
      a.addEventListener("click", (ev) => {
        ev.preventDefault();
        history.pushState({}, "", a.href);
        openFile(resolved);
      });
    }
  }
  for (const img of div.querySelectorAll("img[src]")) {
    const src = img.getAttribute("src");
    if (!src || src.startsWith("http") || src.startsWith("data:")) continue;
    const resolved = new URL(src, "file:///root/" + baseDir + "/").pathname.replace(/^\/root\//, "");
    img.setAttribute("src", resolved);
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
