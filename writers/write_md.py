"""Generate cossacks3_reference.md — legacy comprehensive markdown reference.

Static prose blocks (header, section intros, parser caveats, footer) live in
`writers/templates/legacy/*.md` so this file stays focused on assembly +
table generation. Computed tables (per-nation buildings/units/upgrades,
sanity checks, market rates) remain in code.
"""
import sys, json
sys.stdout.reconfigure(encoding="utf-8")
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "parser"))
from config import OUTPUT_DIR, PLAYABLE_NATIONS, _commonname

from config import DATA_JSON
DATA_PATH = DATA_JSON
MD_PATH = OUTPUT_DIR / "cossacks3_reference.md"
TEMPLATES_DIR = Path(__file__).parent / "templates"


def render_template(name: str, **subs: object) -> list[str]:
    """Load `writers/templates/<name>` (forward slashes for nested paths),
    apply `str.format(**subs)` if subs given, return as a list of lines."""
    text = (TEMPLATES_DIR / name).read_text(encoding="utf-8")
    if subs:
        text = text.format(**subs)
    return text.splitlines()


def fmt(v, default="—"):
    if v is None or v == "" or v == 0 and isinstance(v, int):
        if v == 0:
            return "0"
        return default
    return str(v)


def fmt_cost(row, keys=("food", "wood", "stone", "gold", "iron", "coal")):
    parts = []
    for k in keys:
        v = row.get(k)
        if v not in (None, 0):
            parts.append(f"{k[0].upper()}{v}")
    return " ".join(parts) if parts else "—"


def name_ru_or_en(item: dict) -> str:
    """Russian name from locale; falls back to English; then to em-dash."""
    ru = (item.get("name_ru") or "").strip()
    en = (item.get("name_en") or "").strip()
    return ru or en or "—"


def main():
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    out: list[str] = []
    A = out.append
    nation_name = {n["sid"]: (n["name_en"] or n["sid"]) for n in data["nations"]}
    nation_name_ru = {n["sid"]: (n["name_ru"] or n["sid"]) for n in data["nations"]}

    out.extend(render_template("legacy/header_banner.md"))
    A("")

    # ----- 1. Economy -----
    A("## 1. Глобальная экономика\n")
    e = data["economy"]
    A("### Время")
    A("| Параметр | Значение | Что значит |")
    A("|---|---:|---|")
    A(f"| `gc_time_to_frames` | **{e['time_to_frames']}** | кадров в одной игровой секунде. `buildtime=144` = 4.5 сек. |")
    A(f"| game speed 0 (slow) | {e['gamespeed_slow']} | тиков/сек |")
    A(f"| game speed 1 (default) | {e['gamespeed_normal']} | тиков/сек |")
    A(f"| game speed 2 (fast) | {e['gamespeed_fast']} | тиков/сек |")
    A("")
    A("### Базовые порции (сколько крестьянин приносит за один рейс при eff=100)")
    A("| Ресурс | Базовая порция | hits_needed (циклов работы перед сдачей) |")
    A("|---|---:|---:|")
    A(f"| food (еда) | **{e['resource_portion_food']}** | {e['hits_needed_food']} |")
    A(f"| wood (дерево) | **{e['resource_portion_wood']}** | {e['hits_needed_wood']} |")
    A(f"| stone (камень) | **{e['resource_portion_stone']}** | {e['hits_needed_stone']} |")
    A(f"| gold/iron/coal/etc. | **{e['resource_portion_others']}** | (не задействован — шахты в режиме `produce`) |")
    A("")
    A("### Формула добычи\n")
    A("```")
    A(f"{e['extraction_formula']}")
    A("```\n")
    A(f"`eff` инициализируется = **{e['default_eff_percent']}** в `player.script:109`. "
      "Каждый апгрейд (mill, academy, blacksmith) добавляет своё значение к eff аддитивно. "
      "Например, +40% и +140% дают eff=280, и крестьянин приносит `45×280/100=126` еды за рейс.\n")
    A(f"### Прочее\n")
    A(f"- **Лимит юнитов на карте:** {e['max_obj_count']}\n"
      f"- **Лимит игроков:** {e['max_player_count']}\n"
      f"- **HP поля (для жатвы):** {e['field_max_hp']}\n"
      f"- **Upkeep юнита:** {e['food_per_unit_upkeep']} food / unit (для большинства).")
    A("")

    # ----- 2. Discrepancies + Sanity checks -----
    A("## 2. Расхождения и автопроверки\n")
    A("### 2a. Расхождения с промпт-заметками\n")
    A("Места, где значения в скриптах отличаются от исходных пользовательских заметок. "
      "Источник истины — файлы игры.\n")
    A("| Факт | В заметках | В файле | Источник | Вердикт |")
    A("|---|---|---|---|---|")
    for d in data.get("discrepancies", []):
        A(f"| {d['fact']} | {d['user_note']} | {d['file_value']} | {d['source']} | {d['verdict']} |")
    A("")
    A("### 2b. Sanity checks (автоматические утверждения)\n")
    sanity = data.get("sanity_checks", [])
    n_pass = sum(1 for c in sanity if c["pass"])
    n_fail = len(sanity) - n_pass
    A(f"**{n_pass}/{len(sanity)} проверок прошли.** Если после патча игры тут появятся `FAIL` — это "
      "сигнал, что цифры/структура поменялись и нужно проверить парсер.\n")
    if n_fail > 0:
        A(f"**❌ FAILED ({n_fail}):**\n")
        A("| Категория | Проверка | Ожидание | Получено |")
        A("|---|---|---|---|")
        for c in sanity:
            if not c["pass"]:
                A(f"| {c['category']} | {c['name']} | `{c['expected']}` | `{c['actual']}` |")
        A("")
    # Group passing checks by category for compact display
    A("**✅ PASSED (по категориям):**\n")
    by_cat = defaultdict(list)
    for c in sanity:
        if c["pass"]:
            by_cat[c["category"]].append(c)
    for cat in sorted(by_cat.keys()):
        items = by_cat[cat]
        A(f"- **{cat}** ({len(items)}): " +
          ", ".join(c["name"] for c in items[:6]) +
          (f" (+{len(items)-6})" if len(items) > 6 else ""))
    A("")

    # ----- 3. Nations -----
    A("## 3. Нации (21)\n")
    A("| ID | sid | Английское имя | Русское имя | Кластер `commonName` | Пехотный пеасант |")
    A("|---:|---|---|---|---|---|")
    cluster_peasant = {
        "aus": "peaaus", "fra": "peaeng", "eng": "peaeng", "spa": "peaspa", "rus": "pearus",
        "ukr": "peaukr", "pol": "peapol", "swe": "peaeng", "pru": "peaaus", "ven": "peaspa",
        "tur": "peatur", "alg": "peatur", "net": "peaeng", "den": "peaeng", "por": "peaspa",
        "pie": "peaspa", "sax": "peaaus", "bav": "peaaus", "hun": "peapol", "swi": "peaaus",
        "sco": "peasco",
    }
    for i, nat in enumerate(PLAYABLE_NATIONS):
        nation_obj = next((n for n in data["nations"] if n["sid"] == nat), None)
        en = nation_obj["name_en"] if nation_obj else ""
        ru = nation_obj["name_ru"] if nation_obj else ""
        A(f"| {i} | `{nat}` | {en or '—'} | {ru or '—'} | `{_commonname(nat)}` | `{cluster_peasant.get(nat, '?')}` |")
    A("")

    # ----- 4. Buildings -----
    out.extend(render_template("legacy/section_4_buildings_intro.md"))
    A("")
    PER_NAT_SUF_NAMES = {
        "cen": "Городской центр", "bar": "Казарма 17 в.", "ba2": "Казарма 18 в.",
        "aca": "Академия", "bla": "Кузница", "sta": "Конюшня", "tem": "Собор",
        "art": "Артиллерийское депо", "dip": "Дипломатический центр", "hou": "Дом",
    }
    by_suffix = defaultdict(list)
    for b in data["buildings"]:
        if b["kind"] != "per-nation":
            continue
        suf = b["sid"][len(b["nation"]):]
        by_suffix[suf].append(b)

    for suf in ["cen", "hou", "bar", "ba2", "bla", "sta", "tem", "aca", "art", "dip"]:
        rows = sorted(by_suffix.get(suf, []), key=lambda x: x["nation"])
        if not rows:
            continue
        A(f"#### {suf} — {PER_NAT_SUF_NAMES.get(suf, suf)}\n")
        A("| Нация | sid | Имя | HP | Время (сек) | costpercent | Цена | farm |")
        A("|---|---|---|---:|---:|---:|---|---:|")
        for b in rows:
            A(f"| {b['nation']} | `{b['sid']}` | {name_ru_or_en(b)} "
              f"| {fmt(b['hp'])} | {fmt(b['buildtime_sec'])} | {fmt(b['costpercent'])} "
              f"| {fmt_cost(b)} | {fmt(b['farm'])} |")
        A("")

    out.extend(render_template("legacy/section_4_2_common_intro.md"))
    A("")
    COMMON_SUF_NAMES = {
        "mil": "Мельница", "sto": "Склад", "mar": "Рынок", "por": "Порт",
        "tow": "Башня", "gol": "Золотая шахта", "iro": "Железная шахта", "coa": "Угольная шахта",
        "swa": "Каменная стена", "sga": "Каменные ворота",
        "wga": "Деревянные ворота", "wwa": "Палисад",
    }
    by_suffix = defaultdict(list)
    for b in data["buildings"]:
        if b["kind"] != "common":
            continue
        suf = b["sid"][3:]  # cluster prefix is always 3 letters
        by_suffix[suf].append(b)

    for suf in ["mil", "sto", "mar", "por", "tow", "gol", "iro", "coa", "swa", "sga", "wga", "wwa"]:
        rows = by_suffix.get(suf, [])
        if not rows:
            continue
        # Group by sid (so we don't repeat eurmil 15 times)
        by_sid = defaultdict(list)
        for b in rows:
            by_sid[b["sid"]].append(b)
        A(f"#### {suf} — {COMMON_SUF_NAMES.get(suf, suf)}\n")
        A("| sid (cluster) | Используют нации | HP | Время (сек) | costpercent | Цена | Доп. |")
        A("|---|---|---:|---:|---:|---|---|")
        for sid in sorted(by_sid.keys()):
            entries = by_sid[sid]
            nats = ", ".join(sorted(b["nation"] for b in entries))
            b = entries[0]  # representative
            extra_parts = []
            if b["weapon_damage"]:
                extra_parts.append(f"dmg {b['weapon_damage']}")
                if b["weapon_radiusmax"]:
                    extra_parts.append(f"range {b['weapon_radiusmax']}")
            if b["consume"]:
                extra_parts.append("upkeep " + json.dumps(b["consume"]))
            if b["produce"]:
                extra_parts.append("produce " + json.dumps(b["produce"]))
            if b["peasantabsorber"]:
                extra_parts.append(f"peasants {b['peasantabsorber']}")
            extra = "; ".join(extra_parts) if extra_parts else "—"
            A(f"| `{sid}` | {nats} | {fmt(b['hp'])} | {fmt(b['buildtime_sec'])} | "
              f"{fmt(b['costpercent'])} | {fmt_cost(b)} | {extra} |")
        A("")

    A("### 4.3 Сводка по каждой нации\n")
    A("Полный набор зданий + общая стоимость 1× каждого.\n")
    for nat in PLAYABLE_NATIONS:
        A(f"#### {nat} — {nation_name.get(nat, nat)}\n")
        bldgs = sorted([b for b in data["buildings"] if b["nation"] == nat],
                       key=lambda x: (x["kind"], x["sid"]))
        if not bldgs:
            A("(нет данных)\n")
            continue
        A("| sid | name | HP | Time (s) | cost% | F | W | S | G | I | C | farm | produces |")
        A("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|")
        for b in bldgs:
            produces = b.get("produces") or []
            prod_str = ", ".join(produces[:6]) + (f" (+{len(produces)-6})" if len(produces) > 6 else "")
            A(f"| `{b['sid']}` | {name_ru_or_en(b)} | {fmt(b['hp'])} "
              f"| {fmt(b['buildtime_sec'])} | {fmt(b['costpercent'])} "
              f"| {fmt(b['food'])} | {fmt(b['wood'])} | {fmt(b['stone'])} "
              f"| {fmt(b['gold'])} | {fmt(b['iron'])} | {fmt(b['coal'])} "
              f"| {fmt(b['farm'])} | {prod_str or '—'} |")
        A("")

    # ----- 5. Units -----
    out.extend(render_template("legacy/section_5_units_intro.md"))
    A("")
    units_by_nation = defaultdict(list)
    for u in data["units"]:
        units_by_nation[u["nation"]].append(u)

    for nat in PLAYABLE_NATIONS:
        units = sorted(units_by_nation.get(nat, []), key=lambda x: x["sid"])
        if not units:
            continue
        A(f"### {nat} — {nation_name.get(nat, nat)} ({len(units)} юнитов)\n")
        A("| sid | name | usage | trained_in | uniqueness | HP | Time | F | G | I | dmg | rng (t) | reload | пика | меч | пуля | картечь | стрела | ядро |")
        A("|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
        for u in units:
            w0 = (u["weapons"] or [{}])[0]
            train_str = ", ".join(u.get("trained_in", []) or []) or "—"
            A(f"| `{u['sid']}` | {name_ru_or_en(u)} "
              f"| {u.get('usage_short') or '—'} | {train_str} "
              f"| {u.get('uniqueness') or '—'} "
              f"| {fmt(u['hp'])} | {fmt(u['buildtime_sec'])} "
              f"| {fmt(u['food'])} | {fmt(u['gold'])} | {fmt(u['iron'])} "
              f"| {fmt(w0.get('damage'))} | {fmt(w0.get('radiusmax_tiles'))} | {fmt(w0.get('pause_sec'))} "
              f"| {fmt(u['prot_pike'])} | {fmt(u['prot_sword'])} | {fmt(u['prot_bullet'])} "
              f"| {fmt(u['prot_cannister'])} | {fmt(u['prot_arrow'])} | {fmt(u['prot_cannonball'])} |")
        A("")

    # ----- 5b. Ships -----
    out.extend(render_template("legacy/section_5b_ships.md"))
    A("")
    SHIP_SIDS = {"fishboat", "yacht", "yachttur", "galley", "frigate", "xebec",
                  "battleship", "chaika", "brigantine", "galleon"}
    SHIP_USAGES = {"gc_obj_usage_fisher", "gc_obj_usage_yacht", "gc_obj_usage_galley",
                    "gc_obj_usage_frigate", "gc_obj_usage_xebec", "gc_obj_usage_battleship"}
    ships_seen = {}
    for u in data["units"]:
        if u["sid"] not in SHIP_SIDS and u.get("usage") not in SHIP_USAGES:
            continue
        ships_seen.setdefault(u["sid"], u)  # one row per sid
    A("| sid | nation | name | trained_in | HP | wood | gold | iron | coal | "
      "weap0 dmg | range (t) | reload (s) | weap0 cost | "
      "weap1 dmg | weap1 range | transport | fishingmax | fishingspeed | gold upkeep |")
    A("|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|")
    for sid in sorted(ships_seen.keys()):
        u = ships_seen[sid]
        weapons = u["weapons"] or []
        w0 = weapons[0] if len(weapons) > 0 else {}
        w1 = weapons[1] if len(weapons) > 1 else {}
        consume = u.get("consume") or {}
        cost_str = json.dumps(w0.get("cost"), ensure_ascii=False) if w0.get("cost") else "—"
        A(f"| `{u['sid']}` | {u['nation']} | {name_ru_or_en(u)} "
          f"| {', '.join(u.get('trained_in', []) or []) or '—'} "
          f"| {fmt(u['hp'])} | {fmt(u['wood'])} | {fmt(u['gold'])} | {fmt(u['iron'])} | {fmt(u['coal'])} "
          f"| {fmt(w0.get('damage'))} | {fmt(w0.get('radiusmax_tiles'))} | {fmt(w0.get('pause_sec'))} | {cost_str} "
          f"| {fmt(w1.get('damage'))} | {fmt(w1.get('radiusmax_tiles'))} "
          f"| {fmt(u.get('transport'))} | {fmt(u.get('fishingmax'))} | {fmt(u.get('fishingspeed'))} "
          f"| {fmt(consume.get('gold'))} |")
    A("")
    out.extend(render_template("legacy/section_5b_ships_notes.md"))
    A("")

    # ----- 5c. Mine upgrades -----
    out.extend(render_template("legacy/section_5c_mines_intro.md"))
    A("")
    mine_ups = [u for u in data["upgrades"]
                if any(u["sid"].startswith(p) for p in ("eurgol.","euriro.","eurcoa.",
                                                          "rusgol.","ruseu.","tursola.")
                       )
                or u["sid"] in ("eurgol.1","eurgol.2","eurgol.3","eurgol.4","eurgol.5","eurgol.6")]
    # Just use one nation as representative (aus, since costs are uniform)
    rep_mines = [u for u in mine_ups if u["nation"] == "aus"]
    rep_mines.sort(key=lambda x: x["sid"])
    A("| sid | level | +workers | F | G | total workers (cumulative) |")
    A("|---|---:|---:|---:|---:|---:|")
    cumulative = 5
    last_kind = ""
    for u in rep_mines:
        kind = u["sid"][:6]  # eurgol etc.
        if kind != last_kind:
            cumulative = 5
            last_kind = kind
        cumulative += (u.get("value") or 0)
        A(f"| `{u['sid']}` | {fmt(u['level'])} | +{u.get('value','?')} | "
          f"{fmt(u['food'])} | {fmt(u['gold'])} | {cumulative} |")
    A("")
    out.extend(render_template("legacy/section_5c_mines_outro.md"))
    A("")

    # ----- 6. Combat math -----
    out.extend(render_template("legacy/section_6a_combat.md"))
    A("")

    # 6b. Speed table
    out.extend(render_template("legacy/section_6b_speed_intro.md"))
    A("")
    A("| Класс | Базовая скорость |")
    A("|---|---:|")
    speed_table = data["economy"].get("obj_speed_table_abstract_units", {})
    for k in ["default","peasant","hardhorse","fasthorse","cannon","mortar","howitzer",
              "multicannon","fishboat","ferry","yacht","yachttur","chaika","galley",
              "frigate","xebec","battleship"]:
        if k in speed_table:
            A(f"| {k} | {speed_table[k]} |")
    A("")
    out.extend(render_template("legacy/section_6b_speed_outro.md"))
    A("")

    # 6c. Officers
    out.extend(render_template("legacy/section_6c_officers_intro.md"))
    A("")
    officers = data.get("officers", [])
    by_nation = defaultdict(list)
    for o in officers:
        by_nation[o["nation"]].append(o)
    for nat in PLAYABLE_NATIONS:
        offs = by_nation.get(nat, [])
        if not offs:
            continue
        A(f"#### {nat} — {nation_name.get(nat, nat)} ({len(offs)} офицеров)\n")
        A("| officer | drummer | юниты в строю |")
        A("|---|---|---|")
        for o in offs:
            units = o.get("units", [])
            unit_str = ", ".join(units[:8]) + (f" (+{len(units)-8})" if len(units) > 8 else "")
            A(f"| `{o['officersid']}` | `{o['drummersid']}` | {unit_str or '—'} |")
        A("")

    # 6d. Market rates
    out.extend(render_template("legacy/section_6d_market.md"))
    A("")
    A("| Ресурс | buy_min | buy_def | buy_max | sell_min | sell_def | sell_max |")
    A("|---|---:|---:|---:|---:|---:|---:|")
    for res, vals in data.get("market_rates", {}).items():
        if res.startswith("_"): continue
        A(f"| {res} | {vals['buycostmin']} | {vals['buycostdef']:.2f} | {vals['buycostmax']} "
          f"| {vals['sellcostmin']:.2f} | {vals['sellcostdef']:.2f} | {vals['sellcostmax']:.2f} |")
    A("")
    out.extend(render_template("legacy/section_6d_market_examples.md"))
    A("")

    # Original 6 — combat costs
    out.extend(render_template("legacy/section_combat_costs_intro.md"))
    A("")
    A("| sid | nation | weapon | dmg | reload (s) | shots/min | iron/выстрел | coal/выстрел | gold/выстрел |")
    A("|---|---|---|---:|---:|---:|---:|---:|---:|")
    rows = []
    for u in data["units"]:
        for w in (u["weapons"] or []):
            cost = w.get("cost") or {}
            if cost:
                shots = round(60 / w["pause_sec"], 1) if w.get("pause_sec") else None
                rows.append((u["sid"], u["nation"], w["weaponsid"] or w["kind"] or "?",
                             w.get("damage"), w.get("pause_sec"), shots,
                             cost.get("iron"), cost.get("coal"), cost.get("gold")))
    for b in data["buildings"]:
        cost = b.get("weapon_cost") or {}
        if cost:
            pause_sec = (round(b["weapon_pause_frames"]/32, 2) if b["weapon_pause_frames"] else None)
            shots = (round(60 / pause_sec, 1) if pause_sec else None)
            rows.append((b["sid"], b["nation"], b["weapon_kind"] or "?",
                         b["weapon_damage"], pause_sec, shots,
                         cost.get("iron"), cost.get("coal"), cost.get("gold")))
    rows.sort()
    seen_combat = set()
    for r in rows:
        # dedupe by (sid, nation)
        if (r[0], r[1]) in seen_combat:
            continue
        seen_combat.add((r[0], r[1]))
        A(f"| `{r[0]}` | {r[1]} | `{r[2]}` | {fmt(r[3])} | {fmt(r[4])} | {fmt(r[5])} "
          f"| {fmt(r[6])} | {fmt(r[7])} | {fmt(r[8])} |")
    A("")

    # ----- 7. Upgrades -----
    out.extend(render_template("legacy/section_7_upgrades_intro.md"))
    A("")

    upgrades_by_nation = defaultdict(list)
    for u in data["upgrades"]:
        upgrades_by_nation[u["nation"]].append(u)
    for nat in PLAYABLE_NATIONS:
        upgs = sorted(upgrades_by_nation.get(nat, []), key=lambda x: x["sid"])
        if not upgs:
            continue
        A(f"### {nat} — {nation_name.get(nat, nat)}\n")
        A("| sid | имя (EN) | level | value | время (s) | F | W | S | G | I | C |")
        A("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
        for u in upgs:
            A(f"| `{u['sid']}` | {name_ru_or_en(u)} | {fmt(u['level'])} | {fmt(u['value'])} "
              f"| {fmt(u['time_sec'])} | {fmt(u['food'])} | {fmt(u['wood'])} | {fmt(u['stone'])} "
              f"| {fmt(u['gold'])} | {fmt(u['iron'])} | {fmt(u['coal'])} |")
        A("")

    # ----- 8. Gaps -----
    A("## 8. Дыры в данных и оговорки\n")
    for g in data["gaps"]:
        A(f"### {g['gap']}\n")
        A(f"- Кол-во: {g['count']}")
        if g["sample"]:
            A(f"- Пример: `{', '.join(g['sample'][:30])}`")
        A("")
    out.extend(render_template("legacy/section_8_gaps_outro.md"))
    A("")
    out.extend(render_template("legacy/footer.md"))

    MD_PATH.write_text("\n".join(out), encoding="utf-8")
    print(f"Wrote {MD_PATH} ({MD_PATH.stat().st_size:,} bytes, {len(out):,} lines)")


if __name__ == "__main__":
    main()
