// Drives the Web Worker that holds Pyodide. The main thread is never
// blocked: parsing a 200 MB replay can chew seconds of CPU and we want
// the rest of the page (intro, drop-zone, status pill) to stay alive.

let worker = null;
let bootReady = false;
let waitingForReady = [];
let progressCb = () => {};
let nextId = 1;
const pending = new Map();

function ensureWorker() {
  if (worker) return worker;
  worker = new Worker(new URL("./worker.js", import.meta.url));
  worker.onmessage = (ev) => {
    const m = ev.data;
    if (m.kind === "progress") {
      progressCb(m.text, "loading");
      return;
    }
    if (m.kind === "ready") {
      bootReady = true;
      progressCb("Готов — загрузите .rep", "ready");
      while (waitingForReady.length) waitingForReady.shift()();
      return;
    }
    if (m.kind === "error") {
      progressCb(`Ошибка: ${m.text}`, "error");
      return;
    }
    if (m.id != null) {
      const p = pending.get(m.id);
      if (!p) return;
      pending.delete(m.id);
      if (m.ok) p.resolve(m.result);
      else p.reject(new Error(m.error));
    }
  };
  worker.onerror = (ev) => {
    progressCb(`Worker error: ${ev.message}`, "error");
  };
  return worker;
}

export async function initPyodide(onProgress = () => {}) {
  progressCb = onProgress;
  ensureWorker();
  if (bootReady) return;
  await new Promise((resolve) => waitingForReady.push(resolve));
}

export async function parseReplay(bytes) {
  ensureWorker();
  if (!bootReady) {
    await new Promise((resolve) => waitingForReady.push(resolve));
  }
  const id = nextId++;
  return new Promise((resolve, reject) => {
    pending.set(id, { resolve, reject });
    // Transfer the underlying buffer so we don't double the memory cost
    worker.postMessage({ id, bytes }, [bytes.buffer]);
  });
}
