const STORAGE_KEY = "c3-almanac-language";

export function getLanguage() {
  const requested = new URLSearchParams(location.search).get("lang");
  if (requested === "ru" || requested === "en") {
    localStorage.setItem(STORAGE_KEY, requested);
    return requested;
  }
  return localStorage.getItem(STORAGE_KEY) === "en" ? "en" : "ru";
}

export function applyStaticLanguage(language = getLanguage()) {
  document.documentElement.lang = language;
  for (const element of document.querySelectorAll("[data-ru][data-en]")) {
    element.textContent = element.dataset[language];
  }
  for (const element of document.querySelectorAll("[data-href-ru][data-href-en]")) {
    element.setAttribute("href", element.dataset[`href${language === "en" ? "En" : "Ru"}`]);
  }
  for (const element of document.querySelectorAll("[data-title-ru][data-title-en]")) {
    element.setAttribute("title", element.dataset[`title${language === "en" ? "En" : "Ru"}`]);
  }
  return language;
}

export function bindLanguageSwitch(button, language = getLanguage()) {
  if (!button) return;
  const next = language === "ru" ? "en" : "ru";
  button.textContent = next.toUpperCase();
  button.setAttribute("aria-label", next === "en" ? "Switch to English" : "Переключить на русский");
  button.addEventListener("click", () => {
    localStorage.setItem(STORAGE_KEY, next);
    const url = new URL(location.href);
    url.searchParams.set("lang", next);
    location.href = url.toString();
  });
}
