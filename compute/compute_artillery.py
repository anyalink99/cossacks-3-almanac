"""Сводная таблица по сухопутной артиллерии: per-shot stats, стоимость выстрела,
лимит из artillery depot, экономика юнита.

Артиллерийские юниты в Cossacks 3 — те, у кого `objprop.bartillery = True`.
Парсер выставляет соответствующее поле в `data.json`. Это `cannon`, `howitzer`,
`mortar`, `multicannon` и `framegun` (последний — шотландский эксклюзив).
Внутри артиллерии есть подвид `bartprepare = True` (cannon, howitzer,
framegun) — для них активируется анимация подготовки выстрела перед каждым
залпом.

Лимит на парк артиллерии задан зданием Артиллерийское депо (`<nat>art`):
один депо добавляет к каждому из четырёх `gc_obj_artind_*`-счётчиков константу
из `objprop.artdepo[i]`. Базовая раздача: cannon +5, howitzer +5, mortar +10,
multicannon +3. Без депо лимит = 0, с N депо лимит = N × per-depo.

Output: docs/reports/combat/artillery.md.
"""
from __future__ import annotations
import sys
import json
from collections import defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "parser"))
from config import (DATA_JSON, PLAYABLE_NATIONS, REPORTS_COMBAT_DIR,
                    USAGE_RU, WEAPON_KIND_RU, nation_ru)
from citations import Citations

MD_PATH = REPORTS_COMBAT_DIR / "artillery.md"
FAST_SPEED_MULT = 1.4
RESOURCE_ABBR_RU = {
    "food": "ед.",
    "wood": "дер.",
    "stone": "кам.",
    "gold": "зол.",
    "iron": "жел.",
    "coal": "уг.",
}

# Per-depot artillery slots (`unit.script:2441-2444`, applies to `<nat>art`).
ARTDEPO_SLOTS = {
    "cannon":      5,   # gc_obj_artind_cannon = 0
    "howitzer":    5,   # gc_obj_artind_howitzer = 1
    "mortar":      10,  # gc_obj_artind_mortar = 2
    "multicannon": 3,   # gc_obj_artind_multicannon = 3
}


def primary_weapon(u: dict) -> dict | None:
    """Главное (по урону/паузе) оружие артиллерийского юнита. cannon имеет
    и cannonball-ствол (главный), и cannister (ближняя картечь); главным
    считаем cannonball."""
    weapons = u.get("weapons") or []
    if not weapons:
        return None
    main = [w for w in weapons if w.get("kind") in ("cannonball", "mortarball")]
    if main:
        return max(main, key=lambda w: (w.get("damage") or 0))
    return weapons[0]


def fmt_dispertion(w: dict | None) -> str:
    if not w:
        return "—"
    px = w.get("dispertion_px")
    t = w.get("dispertion_tiles")
    if px is None:
        return "—"
    return f"{px} пикс. · {t} клет."


def fmt_unit_cost(u: dict) -> str:
    parts = []
    for r in ("food", "wood", "stone", "gold", "iron", "coal"):
        v = u.get(r)
        if v:
            parts.append(f"{v} {RESOURCE_ABBR_RU[r]}")
    return " · ".join(parts) if parts else "—"


def collect_artillery(units: list[dict]) -> list[dict]:
    return [u for u in units if u.get("bartillery")]


def fmt_nations(nats: list[str]) -> str:
    if not nats:
        return "—"
    if len(nats) == len(PLAYABLE_NATIONS):
        return "все 21"
    if len(nats) > 6:
        return ", ".join(nation_ru(nat) for nat in nats[:5]) + f" … (+{len(nats) - 5})"
    return ", ".join(nation_ru(nat) for nat in nats)


def canonical_name(u: dict) -> str:
    """Reader-facing unit label with the technical identifier kept secondary."""
    name = u.get("name_ru") or u.get("name_en") or u.get("sid") or "—"
    sid = u.get("sid")
    return f"{name} (`{sid}`)" if sid else str(name)


def group_by_sid(art_units: list[dict]) -> dict[str, list[dict]]:
    by_sid: dict[str, list[dict]] = defaultdict(list)
    for u in art_units:
        by_sid[u["sid"]].append(u)
    return by_sid


def render_header(cites: Citations) -> list[str]:
    L: list[str] = []
    A = L.append
    A("# Артиллерия")
    A("")
    A("[← Таблицы и расчёты](../README.md)")
    A("")
    A("Здесь собраны боевые характеристики сухопутной артиллерии, цена каждого "
      "выстрела, содержание орудий и лимиты Артиллерийского депо.")
    A("")
    bartillery_cite = cites.cite(
        "lib/unit.script:1725, 1757, 1788, 1815, 1847",
        label="`objprop.bartillery := True` для пяти артиллерийских юнитов",
    )
    A(f"Артиллерийское орудие в коде — это объект с признаком "
      f"`objprop.bartillery = True` "
      f"{bartillery_cite}. Подгруппа `bartprepare` включает анимацию подготовки "
      f"выстрела перед каждым залпом — это пушка (`cannon`), гаубица "
      f"(`howitzer`) и рибадекин (`framegun`). У мортиры (`mortar`) и "
      f"многоствольного орудия (`multicannon`) подготовки нет: они стреляют "
      f"непрерывно. "
      f"Поведение приказа `attackpoint` для артиллерии — в "
      f"[статье о выборе цели](../../recon/world/combat/target_selection.md), §5.2.")
    A("")
    A("Морская артиллерия — линейные корабли, галеры, фрегаты и другие суда — "
      "отдельная категория, см. [главу «Флот»](../../reference/07_naval/README.md). "
      "Гренадёр стреляет осколочным `mortarball`, но в `bartillery`-группу "
      "не входит и относится к пехоте — см. "
      "[сводные боевые характеристики](combat_stats.md).")
    A("")
    A("Содержание:")
    A("")
    A("- [§1. Орудия и боевые характеристики](#1-орудия-и-боевые-характеристики)")
    A("- [§2. Стоимость одного выстрела](#2-стоимость-одного-выстрела)")
    A("- [§3. Экономика юнита и национальные различия](#3-экономика-юнита-и-национальные-различия)")
    A("- [§4. Лимит парка от Артиллерийского депо](#4-лимит-парка-от-артиллерийского-депо)")
    A("- [§5. Важные особенности](#5-важные-особенности)")
    A("")
    return L


def render_section_1(art_units: list[dict], cites: Citations) -> list[str]:
    L: list[str] = []
    A = L.append
    A("## §1. Орудия и боевые характеристики")
    A("")
    A("Одна строка соответствует уникальному набору характеристик основного "
      "оружия. Если у нации характеристика отличается, она выносится в "
      "отдельную строку. Колонка **Подготовка** "
      "= `bartprepare`: задержка-анимация перед каждым выстрелом, фиксируется "
      "в скрипте, но точная длительность в `data.json` не извлечена и здесь "
      "не приводится. **Пауза** — холодная перезарядка после выстрела "
      "(`weapon.pause` в игровых секундах). **Точность** — "
      "`weapon.dispertion` в пикселях и клетках; меньше = точнее. Радиус — "
      "`weapon.radiusmax` в клетках; "
      "`radiusmin` показан, если у юнита есть мёртвая зона ближнего боя.")
    A("")
    A("| Орудие | Класс | Нации | Урон | Перезарядка, игр. с | Урон/с | Радиус | Разброс | Подготовка |")
    A("| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | :---: |")

    by_sid = group_by_sid(art_units)
    rows = []
    for sid, units in by_sid.items():
        sub: dict[tuple, list[dict]] = defaultdict(list)
        for u in units:
            w = primary_weapon(u) or {}
            key = (
                w.get("damage"),
                w.get("pause_sec"),
                w.get("radiusmin_tiles"),
                w.get("radiusmax_tiles"),
                w.get("dispertion_px"),
                w.get("dispertion_tiles"),
                w.get("kind"),
            )
            sub[key].append(u)
        for key, group in sub.items():
            rep = group[0]
            w = primary_weapon(rep) or {}
            d = w.get("damage") or 0
            p = w.get("pause_sec") or 0
            dps = round(d / p, 2) if p else None
            rmin = w.get("radiusmin_tiles") or 0
            rmax = w.get("radiusmax_tiles") or 0
            range_str = (
                f"{rmax} клет."
                if rmin <= 0
                else f"{rmin}–{rmax} клет."
            )
            disp = fmt_dispertion(w)
            prep = "✓" if rep.get("bartprepare") else "—"
            usage_ru = USAGE_RU.get(rep.get("usage_short"), rep.get("usage_short", "—"))
            nats = sorted({u["nation"] for u in group})
            rows.append((sid, canonical_name(rep), usage_ru, fmt_nations(nats), d, p,
                         dps, range_str, disp, prep, d))

    rows.sort(key=lambda r: (r[0], r[-1]))
    for sid, name, cls, nats, d, p, dps, rng, disp, prep, _ in rows:
        dps_str = f"{dps}" if dps is not None else "—"
        A(f"| {name} | {cls} | {nats} | {d} | {p} | {dps_str} | {rng} | {disp} | {prep} |")
    A("")
    A("Колонка **Урон/с** показывает урон за игровую секунду без учёта "
      "защиты цели и ограничения числа поражаемых взрывом юнитов. "
      "Реальный урон по толпе обычно ниже из-за ограничения "
      "`floor(1 + (r/0.35)²)` (см. [разбор расчёта урона, §6.5]"
      "(../../recon/world/combat/combat_damage_pipeline.md)).")
    A("")
    return L


def render_section_2(art_units: list[dict], cites: Citations) -> list[str]:
    L: list[str] = []
    A = L.append
    A("## §2. Стоимость одного выстрела")
    A("")
    A("`weapon[i].cost[gc_resource_type_*]` — ресурсы, которые списываются "
      "в момент выстрела (а не за каждый интервал паузы). Ноль означает, что "
      "конкретный ресурс не тратится; у мортир коэффициент `coal` — порох, "
      "у пушек `iron + coal` — ядро + порох. У `multicannon` (картечница) "
      "цены может не быть, потому что её стволу не присваивается `weapon.cost` "
      "в скрипте.")
    A("")
    A("**Эффективность по цене.** Колонка `dmg / shot_cost_g` — это `damage`, "
      "делённый на «золотой эквивалент выстрела». Эквивалент считается по "
      "стандартному курсу `mar.def` (`reference/06_market/README.md`): "
      "`iron × 140 + coal × 140 + wood × 50 + stone × 50 + food × 25 + gold × 1` "
      "— то есть переводим расход в условные единицы золота по базовым ценам покупки. "
      "Это удобная грубая мера, чтобы сравнить, сколько ты «платишь» за единицу "
      "урона при разных типах артиллерии. Не учитывает закупочную цену самой "
      "пушки, расход еды на содержание и износ от ответного огня.")
    A("")

    DEF_BUY = {"food": 25, "wood": 50, "stone": 50, "gold": 1, "iron": 140, "coal": 140}

    A("| Орудие | Нации | Тип снаряда | Урон | Железо | Уголь | Прочие ресурсы | Цена в золотом эквиваленте | Урон на единицу цены |")
    A("| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |")

    rows = []
    for u in art_units:
        w = primary_weapon(u) or {}
        cost = w.get("cost") or {}
        d = w.get("damage") or 0
        kind = w.get("kind", "—")
        iron = cost.get("iron") or 0
        coal = cost.get("coal") or 0
        wood = cost.get("wood") or 0
        stone = cost.get("stone") or 0
        gold = cost.get("gold") or 0
        food = cost.get("food") or 0
        misc_parts = []
        if wood: misc_parts.append(f"{wood} {RESOURCE_ABBR_RU['wood']}")
        if stone: misc_parts.append(f"{stone} {RESOURCE_ABBR_RU['stone']}")
        if gold: misc_parts.append(f"{gold} {RESOURCE_ABBR_RU['gold']}")
        if food: misc_parts.append(f"{food} {RESOURCE_ABBR_RU['food']}")
        misc = " · ".join(misc_parts) or "—"
        gold_eq = sum((cost.get(r) or 0) * DEF_BUY[r] for r in DEF_BUY)
        eff = round(d / gold_eq, 2) if gold_eq else None
        rows.append((u["sid"], canonical_name(u), u["nation"],
                     WEAPON_KIND_RU.get(kind, kind), d, iron, coal, misc, gold_eq, eff))

    grouped: dict[tuple, list[str]] = defaultdict(list)
    for sid, name, nat, kind, d, iron, coal, misc, gold_eq, eff in rows:
        key = (sid, name, kind, d, iron, coal, misc, gold_eq, eff)
        grouped[key].append(nat)

    out_rows = sorted(grouped.items(), key=lambda kv: (kv[0][0], kv[0][4]))
    for key, nats in out_rows:
        sid, name, kind, d, iron, coal, misc, gold_eq, eff = key
        eff_str = f"{eff}" if eff is not None else "—"
        gold_eq_str = gold_eq if gold_eq else "—"
        A(f"| {name} | {fmt_nations(sorted(set(nats)))} | {kind} | "
          f"{d} | {iron} | {coal} | {misc} | {gold_eq_str} | {eff_str} |")
    A("")
    cannister_cite = cites.cite(
        "lib/weapon.script:529",
        label="механизм подснарядов картечи (`_weapon_SyncWeapon`)",
    )
    A(f"**Картечь** (`cannister`) у пушки (`cannon`) и многоствольного орудия "
      f"(`multicannon`) — отдельное оружие "
      f"со своей `pause` и стоимостью. У `cannon` `weapon[1].damage = 0`: "
      f"картечь у обычной пушки реализована не прямой записью в `damage`, "
      f"а через механизм подснарядов `_weapon_SyncWeapon` {cannister_cite}. "
      f"Каждый выстрел картечью порождает несколько подснарядов; их урон "
      f"выставлен при создании определения оружия и в `data.json` напрямую "
      f"не сводится. У `multicannon` `weapon[0]` уже типа `cannister`, и вся "
      f"характеристика там и хранится. Сравнивать урон в секунду картечи и ядра "
      f"напрямую по `data.json` поэтому нельзя без чтения сценария оружия.")
    A("")
    return L


def render_section_3(art_units: list[dict], cites: Citations) -> list[str]:
    L: list[str] = []
    A = L.append
    A("## §3. Экономика юнита и национальные различия")
    A("")
    A("Цена покупки, время постройки, здоровье, защита, скорость и содержание в золоте. "
      "Если у нации те же значения — одна строка, нации сгруппированы.")
    A("")
    A("| Орудие | Нации | Цена | Время, игр. с | Здоровье | Щит | Скорость | Расход золота (служебное значение) | Золота/игр. с | Очки |")
    A("| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")

    by_sid = group_by_sid(art_units)
    for sid, units in by_sid.items():
        sub: dict[tuple, list[dict]] = defaultdict(list)
        for u in units:
            key = (
                u.get("food"), u.get("wood"), u.get("stone"),
                u.get("gold"), u.get("iron"), u.get("coal"),
                u.get("buildtime_sec"), u.get("hp"), u.get("shield"),
                u.get("speed"), (u.get("consume") or {}).get("gold"),
                u.get("score"),
            )
            sub[key].append(u)
        for key, group in sub.items():
            rep = group[0]
            nats = sorted({u["nation"] for u in group})
            cost = fmt_unit_cost(rep)
            bt = rep.get("buildtime_sec")
            hp = rep.get("hp")
            sh = rep.get("shield") if rep.get("shield") is not None else "—"
            sp = rep.get("speed")
            gpt = (rep.get("consume") or {}).get("gold") or "—"
            sc = rep.get("score") or "—"
            # Расход в gold/г-сек: consume × 32 / 20000
            try:
                gpg = round(int(gpt) * 32 / 20000, 3) if gpt not in ("—", None) else "—"
            except (ValueError, TypeError):
                gpg = "—"
            A(f"| {canonical_name(rep)} | {fmt_nations(nats)} | {cost} | {bt} | {hp} | "
              f"{sh} | {sp} | {gpt} | {gpg} | {sc} |")
    A("")
    A("`consume[gold]` — поле `objprop.consume[gc_resource_type_gold]`. "
      "Реальный расход считается формулой `consume × gc_time_to_frames / 20000` "
      "за каждую игровую секунду (так как процедура `_player_ProcessResourceConsume` "
      "использует `speed = 20000` в делителе). Колонка `gold/г-сек` уже учитывает "
      "эту формулу. Артиллерия — единственный класс, у которого `consume.gold > 0` "
      "для всех юнитов: пушку нужно «содержать», даже если она не стреляет. "
      "У пехоты и кавалерии `consume.gold = 0`. Подробнее — в "
      "[разбор голода и бунта, §2.3]"
      "(../../recon/world/economy/hunger_and_rebellion.md).")
    A("")
    return L


def render_section_4(buildings: list[dict], cites: Citations) -> list[str]:
    L: list[str] = []
    A = L.append
    A("## §4. Лимит парка от Артиллерийского депо")
    A("")
    sum_cite = cites.cite("lib/unit.script:3826-3830",
                          label="суммирование `artdepo[i]` в `gPlayer[plInd].artlimit[i]`")
    init_cite = cites.cite("lib/player.script:3169-3171",
                           label="инициализация `artlimit[k] := 0` при старте партии")
    check_cite = cites.cite("lib/miscext2.script:114-116",
                            label="проверка `artcount[i] >= artlimit[i]` → "
                                  "`gc_result_checkaccesscontrolreq_artlimit`")
    A(f"Здание `<nat>art` (Артиллерийское депо). При постройке добавляет "
      f"к `gPlayer[plInd].artlimit[i]` константу `objprop.artdepo[i]` "
      f"{sum_cite}. Лимит линеен по числу депо — без капа сверху. Без депо "
      f"лимит = 0 {init_cite}, и любая попытка построить артиллерию упирается "
      f"в `gc_result_checkaccesscontrolreq_artlimit` {check_cite}.")
    A("")
    base_cite = cites.cite("lib/unit.script:2441-2444",
                           label="базовая раздача `artdepo[0..3]` для `<nat>art`",
                           code=("objprop.artdepo[0] := 5;\n"
                                 "objprop.artdepo[1] := 5;\n"
                                 "objprop.artdepo[2] := 10; // c1 = 30\n"
                                 "objprop.artdepo[3] := 3;\n"
                                 "objprop.bartdepo := True;"))
    A(f"Базовая раздача с одного депо {base_cite}:")
    A("")
    A("| Орудие | Технический индекс | Слотов с одного депо |")
    A("| --- | --- | ---: |")
    for sid, name, slots in [
        ("cannon", "Пушка", "0 — `gc_obj_artind_cannon`"),
        ("howitzer", "Гаубица", "1 — `gc_obj_artind_howitzer`"),
        ("mortar", "Мортира", "2 — `gc_obj_artind_mortar`"),
        ("multicannon", "Многоствольное орудие", "3 — `gc_obj_artind_multicannon`"),
    ]:
        A(f"| {name} (`{sid}`) | {slots} | {ARTDEPO_SLOTS[sid]} |")
    A("")
    A("Иначе говоря, чтобы выкатить полный мортирный батальон в 30 штук, "
      "нужно три Артиллерийских депо (3 × 10 = 30 слотов под `mortar`).")
    A("")

    depots = [b for b in buildings if b["sid"].endswith("art")
              and b["sid"][:-3] in PLAYABLE_NATIONS]
    if depots:
        defaults_cite = cites.cite(
            "lib/unit.script:2440",
            label="базовые параметры Артиллерийского депо",
        )
        overrides_cite = cites.cite(
            "lib/unit.script:2447-2448",
            label="`if (i = ukr) ...` и `if (i = tur) ...` для цены депо",
        )
        A(f"**Цена и параметры самого Артиллерийского депо** по нациям. "
          f"Обычный вариант имеет 40 000 здоровья, даёт 1 400 очков, а каждое "
          f"следующее депо стоит вдвое дороже предыдущего {defaults_cite}. "
          f"Отличия Украины и Турции показаны отдельными строками "
          f"{overrides_cite}.")
        A("")
        A("| Нация | Здоровье | Цена (еда/дерево/камень/золото/железо/уголь) | Время строительства, игр. с | Рост цены, % |")
        A("| --- | ---: | --- | ---: | ---: |")
        sub: dict[tuple, list[str]] = defaultdict(list)
        for b in depots:
            cost_tup = tuple(b.get(r) or 0 for r in
                             ("food", "wood", "stone", "gold", "iron", "coal"))
            sub[(b.get("hp"), cost_tup, b.get("buildtime_sec"),
                 b.get("costpercent"))].append(b["nation"])
        for (hp, cost_tup, bt, cp), nats in sorted(sub.items(), key=lambda kv: -len(kv[1])):
            cost_str = " / ".join(str(v) for v in cost_tup)
            A(f"| {fmt_nations(sorted(nats))} | {hp} | {cost_str} | {bt} | {cp} |")
        A("")
    return L


def render_section_5(cites: Citations) -> list[str]:
    L: list[str] = []
    A = L.append
    A("## §5. Важные особенности")
    A("")

    try_attack_cite = cites.cite(
        "lib/unit.script:7512",
        label="`_unit_TryAttackPoint` и связанные ветки",
    )
    A(f"- **Подготовка перед выстрелом.** У пушки, гаубицы и некоторых других "
      f"орудий перед каждым выстрелом проигрывается отдельная длинная анимация "
      f"(внутренний флаг `bartprepare`) {try_attack_cite}. Её точная "
      f"длительность хранится в анимации атаки (`attack0`) и пока не извлечена "
      f"в `data.json`. Поэтому расчёт использует паузу оружия как чистую "
      f"перезарядку, без добавочной анимационной задержки.")
    A("")

    move_penalty_cite = cites.cite(
        "lib/unit.script:5151-5156",
        label="штраф к радиусу для движущегося стрелка",
    )
    A(f"- **Точность падает в движении.** Стрелок и артиллерия в движении "
      f"(`standtime < 0.25 g-сек`) теряют до `gc_obj_maxattackradiusdisp = 3` "
      f"тайлов эффективного радиуса {move_penalty_cite}. Дополнительное "
      f"рассеивание `dispertion` остаётся прежним. Подробнее — "
      f"[разбор поведения стрелков, §4]"
      f"(../../recon/world/combat/ranged_units_behavior.md#4-штраф-к-дальности-при-движении-standtime).")
    A("")

    A("- **Точность улучшают исследования Академии.** «Разработать новые "
      "прицельные системы для пушек» (`aca.20`) уменьшает рассеивание на 35%. "
      "«Развивать математику» (`aca.27`) уменьшает его ещё на 35%; эффекты "
      "складываются последовательно. После "
      "обоих остаётся `0.65 × 0.65 ≈ 0.42` от исходного, то есть точность "
      "вырастает примерно в 2.4 раза. Применяется только к артиллерии; "
      "у мушкетеров и лучников прямого улучшения рассеивания нет.")
    A("")

    aoe_cite = cites.cite(
        "lib/miscext2.script:_misc_DoRoundDamage",
        label="ограничение числа поражённых целей: `floor(1 + (r/0.35)²)`",
    )
    A(f"- **Взрыв поражает ограниченное число целей.** При взрыве снаряда "
      f"урон получают только "
      f"первые `count = floor(1 + (r/0.35)²)` юнитов в радиусе {aoe_cite}. "
      f"Для пушки (`r ≈ 1`) это 9 юнитов, для мортиры (`r ≈ 2`) — 33. "
      f"Растянутая линия страдает гораздо больше, чем плотная толпа.")
    A("")

    longrange_cite = cites.cite(
        "lib/unit.script:11184",
        label="`_unit_SearchEnemyLongRangeArtillery` (отдельная ветка для компьютерной артиллерии)",
    )
    A(f"- **Выбор цели компьютерным игроком.** Решение, куда стрелять, идёт через "
      f"`_unit_SearchEnemyLongRangeArtillery` {longrange_cite} — это отдельная "
      f"ветка, не общий `_unit_SearchVictimOnProgress`. Орудия "
      f"компьютерного игрока "
      f"выбирают цель по дистанции `[radiusmin .. radiusmax]`, учитывая "
      f"`bsearchmaxattradius`. Эта ветка отличается от обычного поиска по клеткам и "
      f"описана только косвенно — см. [статью о выборе цели]"
      f"(../../recon/world/combat/target_selection.md) §7 (нерешённый вопрос № 4).")
    A("")

    order_attackpoint_cite = cites.cite(
        "lib/player.script:2447-2481",
        label="`_player_OrderUnitsToAttackPoint` (ветка для `bartprepare = True`)",
    )
    A(f"- **`bartprepare` и `attack-move`.** Артиллерия с `bartprepare = True` "
      f"получает приказ `gc_obj_order_type_attackpoint` через "
      f"`_player_OrderUnitsToAttackPoint` {order_attackpoint_cite} — это "
      f"стрельба по координате, не по конкретной цели. Поведение для "
      f"не-артиллерийских юнитов другое — они движутся с `move_mode_attack`. "
      f"Подробности — в [статье о выборе цели]"
      f"(../../recon/world/combat/target_selection.md) §5.")
    A("")
    return L


def main() -> None:
    data = json.loads(DATA_JSON.read_text(encoding="utf-8"))
    units = data["units"]
    buildings = data["buildings"]
    art_units = collect_artillery(units)

    print(f"compute_artillery: art-юнит-нация-пар = {len(art_units)}, "
          f"уникальных sid = {len({u['sid'] for u in art_units})}")

    cites = Citations()
    L: list[str] = []
    L += render_header(cites)
    L += render_section_1(art_units, cites)
    L += render_section_2(art_units, cites)
    L += render_section_3(art_units, cites)
    L += render_section_4(buildings, cites)
    L += render_section_5(cites)
    L += cites.render()

    REPORTS_COMBAT_DIR.mkdir(parents=True, exist_ok=True)
    MD_PATH.write_text("\n".join(L), encoding="utf-8")
    print(f"saved -> {MD_PATH}")


if __name__ == "__main__":
    main()
