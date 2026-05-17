// Main controller: file uploads + result rendering.

import { initPyodide, parseReplay } from "./pyodide_runner.js";
import { renderCard, setGameSettings } from "./render.js";

const $ = (sel) => document.querySelector(sel);
const status = $("#status");
const fileInput = $("#file_input");
const dropZone = $("#drop_zone");
const results = $("#results");
const clearBtn = $("#clear_btn");

function setStatus(text, cls = "loading") {
  status.textContent = text;
  status.className = `pill ${cls}`;
}

// Boot Pyodide + load canonical lobby-setting labels from derived/game_settings.json
// (extracted from game scripts/locale — single source of truth for option names).
initPyodide(setStatus).catch((e) => {
  setStatus(`Ошибка загрузки: ${e}`, "error");
  console.error(e);
});
fetch(`../derived/game_settings.json?v=${Date.now()}`)
  .then((r) => r.json())
  .then((gs) => setGameSettings(gs))
  .catch((e) => console.warn("game_settings.json load failed:", e));

// File picker
fileInput.addEventListener("change", async (ev) => {
  const files = Array.from(ev.target.files);
  await processFiles(files);
  fileInput.value = "";  // reset so re-uploading same file works
});

// Drag and drop
["dragenter", "dragover"].forEach((evt) => {
  dropZone.addEventListener(evt, (e) => {
    e.preventDefault();
    dropZone.classList.add("dragging");
  });
});
["dragleave", "drop"].forEach((evt) => {
  dropZone.addEventListener(evt, (e) => {
    e.preventDefault();
    dropZone.classList.remove("dragging");
  });
});
dropZone.addEventListener("drop", async (e) => {
  const files = Array.from(e.dataTransfer.files);
  await processFiles(files);
});

// Clear all
clearBtn.addEventListener("click", () => {
  results.innerHTML = "";
});

function fmtSize(bytes) {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(0)} KB`;
  return `${(bytes / 1024 / 1024).toFixed(1)} MB`;
}

function estimateSeconds(bytes) {
  // ~1.5 MB/s in Pyodide for the optimised single-pass decoder.
  return Math.max(1, Math.round(bytes / (1.5 * 1024 * 1024)));
}

async function processFiles(files) {
  const replays = files.filter((f) =>
    f.name.toLowerCase().endsWith(".rep") || f.name.toLowerCase().endsWith(".map")
  );
  if (!replays.length) return;

  for (const file of replays) {
    const placeholder = document.createElement("div");
    placeholder.className = "progress-row";
    const sizeStr = fmtSize(file.size);
    const eta = estimateSeconds(file.size);
    placeholder.textContent =
      `Парсим ${file.name} · ${sizeStr} · ожидайте ~${eta} сек…`;
    results.appendChild(placeholder);

    // Heartbeat — every second update the elapsed counter so the user
    // sees something is happening while Pyodide chews on a big replay.
    const tStart = performance.now();
    const heartbeat = setInterval(() => {
      const elapsed = Math.round((performance.now() - tStart) / 1000);
      placeholder.textContent =
        `Парсим ${file.name} · ${sizeStr} · ${elapsed} сек / ~${eta} сек`;
    }, 1000);

    try {
      const buf = new Uint8Array(await file.arrayBuffer());
      const result = await parseReplay(buf);
      clearInterval(heartbeat);
      const ms = Math.round(performance.now() - tStart);
      placeholder.replaceWith(renderCard(file.name, result, ms));
    } catch (e) {
      clearInterval(heartbeat);
      placeholder.className = "error-row";
      placeholder.textContent =
        `Ошибка при разборе ${file.name}: ${e.message || e}`;
      console.error(e);
    }
  }
}
