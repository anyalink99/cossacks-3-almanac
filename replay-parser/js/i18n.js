// Nation prefix → canonical sid; used to infer player nation from
// the first ReadConstruct sid (e.g. "auscen" → "aus" → Австрия).

export const NATION_FROM_SID = {
  aus: "aus", alg: "alg", bav: "bav", den: "den", eng: "eng",
  fra: "fra", net: "net", pie: "pie", pol: "pol", por: "por",
  pru: "pru", rus: "rus", sax: "sax", sco: "sco", spa: "spa",
  swe: "swe", swi: "swi", tur: "tur", ukr: "ukr", ven: "ven",
};

export const NATION_LABEL_RU = {
  aus: "Австрия", alg: "Алжир", bav: "Бавария", den: "Дания",
  eng: "Англия", fra: "Франция", net: "Нидерланды", pie: "Пьемонт",
  pol: "Польша", por: "Португалия", pru: "Пруссия", rus: "Россия",
  sax: "Саксония", sco: "Шотландия", spa: "Испания", swe: "Швеция",
  swi: "Швейцария", tur: "Турция", ukr: "Украина", ven: "Венеция",
};
