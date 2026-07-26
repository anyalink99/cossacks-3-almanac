// Nation prefix → canonical sid; used as a fallback when the player's
// `cid` (from TMapPlayer in the .rep header) is missing or = -2 (random).

export const NATION_FROM_SID = {
  aus: "aus", alg: "alg", bav: "bav", den: "den", eng: "eng",
  fra: "fra", hun: "hun", net: "net", pie: "pie", pol: "pol",
  por: "por", pru: "pru", rus: "rus", sax: "sax", sco: "sco",
  spa: "spa", swe: "swe", swi: "swi", tur: "tur", ukr: "ukr",
  ven: "ven",
};

// Engine country index → nation sid. Mirrors parser/parse_replay_events.py
// NATION_BY_CID (lines 767-772). cid=24 = empty slot, cid=-2 = "random,
// not yet resolved".
export const NATION_BY_CID = {
   0: "aus",  1: "fra",  2: "eng",  3: "spa",  4: "rus",  5: "ukr",
   6: "pol",  7: "swe",  8: "pru",  9: "ven", 10: "tur", 11: "alg",
  12: "mis", 13: "net", 14: "den", 15: "por", 16: "pie", 17: "sax",
  18: "bav", 19: "hun", 20: "swi", 21: "sco", 22: "tat", 23: "lit",
};

export const NATION_LABEL_RU = {
  aus: "Австрия", alg: "Алжир", bav: "Бавария", den: "Дания",
  eng: "Англия", fra: "Франция", hun: "Венгрия", net: "Нидерланды",
  pie: "Пьемонт", pol: "Польша", por: "Португалия", pru: "Пруссия",
  rus: "Россия", sax: "Саксония", sco: "Шотландия", spa: "Испания",
  swe: "Швеция", swi: "Швейцария", tur: "Турция", ukr: "Украина",
  ven: "Венеция",
};

export const NATION_LABEL_EN = {
  aus: "Austria", alg: "Algeria", bav: "Bavaria", den: "Denmark",
  eng: "England", fra: "France", hun: "Hungary", net: "Netherlands",
  pie: "Piedmont", pol: "Poland", por: "Portugal", pru: "Prussia",
  rus: "Russia", sax: "Saxony", sco: "Scotland", spa: "Spain",
  swe: "Sweden", swi: "Switzerland", tur: "Turkey", ukr: "Ukraine",
  ven: "Venice",
};
