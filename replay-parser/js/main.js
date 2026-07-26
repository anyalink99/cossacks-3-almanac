// Main controller: file uploads + result rendering.

import { initPyodide, parseReplay } from "./pyodide_runner.js";
import translationsEn from "./translations.en.js";
import {
  bindToolLanguageSwitch,
  startAutomaticLocalization,
  tr,
} from "../../assets/js/runtime-i18n.js";
import {
  renderCard,
  renderComparison,
  setCanonicalTerms,
  setGameSettings,
  setPatternData,
} from "./render.js";

const $ = (sel) => document.querySelector(sel);
const status = $("#status");
const fileInput = $("#file_input");
const dropZone = $("#drop_zone");
const results = $("#results");
const comparison = $("#comparison");
const clearBtn = $("#clear_btn");
const openReplays = [];
let replayId = 0;

startAutomaticLocalization(translationsEn);
bindToolLanguageSwitch($("#language_switch"));

function setStatus(text, cls = "loading") {
  status.textContent = tr(text);
  status.className = `pill ${cls}`;
}

function updateComparison() {
  comparison.hidden = openReplays.length < 2;
  comparison.replaceChildren(
    ...(openReplays.length >= 2 ? [renderComparison(openReplays)] : []),
  );
}

// Boot Pyodide + load canonical labels and map-pattern metadata.
initPyodide(setStatus).catch((e) => {
  setStatus(`Ошибка загрузки: ${e}`, "error");
  console.error(e);
});
const metadataPromise = Promise.all([
  fetch(`../derived/game_settings.json?v=${Date.now()}`).then((r) => r.json()),
  fetch(`../derived/pattern_types.json?v=${Date.now()}`).then((r) => r.json()),
  fetch(`../derived/pattern_inventory.json?v=${Date.now()}`).then((r) => r.json()),
  fetch(`../derived/canonical_terms.json?v=${Date.now()}`).then((r) => r.json()),
])
  .then(([settings, types, inventory, canonicalTerms]) => {
    setGameSettings(settings);
    setPatternData(types, inventory);
    setCanonicalTerms(canonicalTerms);
  })
  .catch((e) => console.warn("replay metadata load failed:", e));

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
dropZone.addEventListener("click", () => fileInput.click());
dropZone.addEventListener("keydown", (event) => {
  if (event.key === "Enter" || event.key === " ") {
    event.preventDefault();
    fileInput.click();
  }
});

// Clear all
clearBtn.addEventListener("click", () => {
  results.innerHTML = "";
  openReplays.length = 0;
  updateComparison();
});

function fmtSize(bytes) {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(0)} KB`;
  return `${(bytes / 1024 / 1024).toFixed(1)} MB`;
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
    placeholder.textContent =
      `Разбираем ${file.name} · ${sizeStr}…`;
    results.appendChild(placeholder);
    setStatus(`Разбор: ${file.name}`, "loading");

    // Heartbeat — every second update the elapsed counter so the user
    // sees something is happening while Pyodide chews on a big replay.
    const tStart = performance.now();
    const heartbeat = setInterval(() => {
      const elapsed = Math.round((performance.now() - tStart) / 1000);
      placeholder.textContent =
        `Разбираем ${file.name} · ${sizeStr} · прошло ${elapsed} сек`;
    }, 1000);

    try {
      const buf = new Uint8Array(await file.arrayBuffer());
      const result = await parseReplay(buf);
      await metadataPromise;
      clearInterval(heartbeat);
      const ms = Math.round(performance.now() - tStart);
      const record = {
        id: ++replayId,
        filename: file.name,
        result,
      };
      openReplays.push(record);
      placeholder.replaceWith(renderCard(file.name, result, ms, {
        onClose: () => {
          const index = openReplays.findIndex((item) => item.id === record.id);
          if (index >= 0) openReplays.splice(index, 1);
          updateComparison();
        },
      }));
      updateComparison();
      setStatus("Готов — можно загрузить ещё", "ready");
    } catch (e) {
      clearInterval(heartbeat);
      placeholder.className = "error-row";
      placeholder.textContent =
        `Ошибка при разборе ${file.name}: ${e.message || e}`;
      setStatus("Ошибка разбора", "error");
      console.error(e);
    }
  }
}
