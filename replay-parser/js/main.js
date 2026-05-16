// Main controller: file uploads + result rendering.

import { initPyodide, parseReplay } from "./pyodide_runner.js";
import { renderCard } from "./render.js";

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

// Boot Pyodide
initPyodide(setStatus).catch((e) => {
  setStatus(`Ошибка загрузки: ${e}`, "error");
  console.error(e);
});

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

async function processFiles(files) {
  const replays = files.filter((f) =>
    f.name.toLowerCase().endsWith(".rep") || f.name.toLowerCase().endsWith(".map")
  );
  if (!replays.length) return;

  for (const file of replays) {
    const placeholder = document.createElement("div");
    placeholder.className = "progress-row";
    placeholder.textContent = `Парсим ${file.name}…`;
    results.appendChild(placeholder);

    try {
      const buf = new Uint8Array(await file.arrayBuffer());
      const t0 = performance.now();
      const result = await parseReplay(buf);
      const ms = Math.round(performance.now() - t0);
      placeholder.replaceWith(renderCard(file.name, result, ms));
    } catch (e) {
      placeholder.className = "error-row";
      placeholder.textContent = `Ошибка при разборе ${file.name}: ${e.message || e}`;
      console.error(e);
    }
  }
}
