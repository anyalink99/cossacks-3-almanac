const STORAGE_KEY = "c3-almanac-language";

export const language = (() => {
  const requested = new URLSearchParams(location.search).get("lang");
  if (requested === "ru" || requested === "en") {
    localStorage.setItem(STORAGE_KEY, requested);
    return requested;
  }
  return localStorage.getItem(STORAGE_KEY) === "en" ? "en" : "ru";
})();

let replacements = [];
let observer = null;

export function setTranslations(dictionary) {
  replacements = Object.entries(dictionary)
    .filter(([source, target]) => source && target && source !== target)
    .sort((left, right) => right[0].length - left[0].length);
}

export function tr(value) {
  if (language !== "en" || value == null) return value;
  let translated = String(value);
  for (const [source, target] of replacements) {
    if (translated.includes(source)) translated = translated.split(source).join(target);
  }
  return translated;
}

function translateAttributes(element) {
  for (const name of ["title", "placeholder", "aria-label"]) {
    if (element.hasAttribute?.(name)) {
      element.setAttribute(name, tr(element.getAttribute(name)));
    }
  }
}

export function localizeTree(root = document) {
  if (language !== "en" || !root) return;
  if (root.nodeType === Node.TEXT_NODE) {
    root.nodeValue = tr(root.nodeValue);
    return;
  }
  if (root.nodeType !== Node.ELEMENT_NODE && root.nodeType !== Node.DOCUMENT_NODE) return;
  if (root.nodeType === Node.ELEMENT_NODE) translateAttributes(root);
  const walker = document.createTreeWalker(
    root,
    NodeFilter.SHOW_ELEMENT | NodeFilter.SHOW_TEXT,
  );
  while (walker.nextNode()) {
    const node = walker.currentNode;
    if (node.nodeType === Node.TEXT_NODE) node.nodeValue = tr(node.nodeValue);
    else translateAttributes(node);
  }
}

export function startAutomaticLocalization(dictionary) {
  setTranslations(dictionary);
  document.documentElement.lang = language;
  if (language !== "en") return;
  document.title = tr(document.title);
  localizeTree(document.body);
  observer?.disconnect();
  observer = new MutationObserver((mutations) => {
    observer.disconnect();
    for (const mutation of mutations) {
      for (const node of mutation.addedNodes) localizeTree(node);
      if (mutation.type === "characterData") localizeTree(mutation.target);
    }
    observer.observe(document.body, { childList: true, subtree: true, characterData: true });
  });
  observer.observe(document.body, { childList: true, subtree: true, characterData: true });
}

export function bindToolLanguageSwitch(button) {
  if (!button) return;
  const next = language === "en" ? "ru" : "en";
  button.textContent = next.toUpperCase();
  button.setAttribute("aria-label", next === "en" ? "Switch to English" : "Переключить на русский");
  button.addEventListener("click", () => {
    localStorage.setItem(STORAGE_KEY, next);
    const url = new URL(location.href);
    url.searchParams.set("lang", next);
    location.href = url.toString();
  });
}
