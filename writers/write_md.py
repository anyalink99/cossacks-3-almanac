"""Generate cossacks3_reference.md — comprehensive markdown reference."""
import sys, json
sys.stdout.reconfigure(encoding="utf-8")
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "parser"))
from config import OUTPUT_DIR, PLAYABLE_NATIONS, _commonname

from config import DATA_JSON
DATA_PATH = DATA_JSON
MD_PATH = OUTPUT_DIR / "cossacks3_reference.md"


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


def main():
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    out: list[str] = []
    A = out.append
    nation_name = {n["sid"]: (n["name_en"] or n["sid"]) for n in data["nations"]}
    nation_name_ru = {n["sid"]: (n["name_ru"] or n["sid"]) for n in data["nations"]}

    A("# Cossacks 3 — Полный справочник цифр (LEGACY)\n")
    A("> ⚠ **Этот файл — устаревшая монолитная версия.** Актуальная структурированная "
      "справка — в [`reference/`](reference/README.md) (главы 01-06, нации, сравнения), "
      "производные расчёты — в [`reports/`](reports/README.md). "
      "Файл сохраняется для обратной совместимости со старыми ссылками.\n")
    A("Извлечено напрямую из файлов игры в `C:\\Program Files (x86)\\Steam\\steamapps\\common\\Cossacks 3\\data\\scripts\\`. "
      "Скрипты парсера: `parser/`. "
      "Все цифры — немодифицированные значения из `unit.script`, `country.script`, `dmscript.global`.\n")
    A("**Версия игры:** актуальная на момент парсинга (Steam install).\n")

    A("## Содержание\n")
    A("- [1. Глобальная экономика](#1-глобальная-экономика)")
    A("- [2. Расхождения и автопроверки](#2-расхождения-и-автопроверки)")
    A("- [3. Нации (21)](#3-нации-21)")
    A("- [4. Здания по нациям](#4-здания-по-нациям)")
    A("    - [4.1 Per-nation постройки (`<nat><suffix>`)](#41-per-nation-постройки)")
    A("    - [4.2 Общие постройки (`<cluster><suffix>`)](#42-общие-постройки)")
    A("    - [4.3 Сводка по каждой нации](#43-сводка-по-каждой-нации)")
    A("- [5. Юниты](#5-юниты)")
    A("- [5b. Корабли](#5b-корабли)")
    A("- [5c. Шахты — апгрейды (gol/iro/coa)](#5c-шахты--апгрейды-goliroсoa)")
    A("- [6. Боевая математика](#6-боевая-математика)")
    A("    - [6a. Damage formula](#6a-damage-formula)")
    A("    - [6b. Скорости юнитов](#6b-скорости-юнитов)")
    A("    - [6c. Офицеры и формации](#6c-офицеры-и-формации)")
    A("- [6d. Рынок — обменные курсы](#6d-рынок--обменные-курсы)")
    A("- [7. Апгрейды](#7-апгрейды)")
    A("- [8. Дыры в данных и оговорки](#8-дыры-в-данных-и-оговорки)")
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
    A("## 4. Здания по нациям\n")
    A("Цены и времена постройки даны для **БАЗОВОГО** экземпляра. Каждое следующее здание того же типа "
      "стоит дороже на величину `costpercent` (200 = вторая постройка стоит ×2 от первой).\n")
    A("Время в секундах рассчитано как `buildtime / 32` (gc_time_to_frames=32).\n")

    A("### 4.1 Per-nation постройки\n")
    A("Каждая нация имеет свой набор; sid формируется как `<nat>+<3-letter>`. "
      "Например, для Австрии: `auscen` (Town Hall), `ausbar` (Barracks), `ausaca` (Academy).\n")
    PER_NAT_SUF_NAMES = {
        "cen": "Ratusha (Town Hall)", "bar": "Barracks 17в.", "ba2": "Barracks 18в.",
        "aca": "Academy", "bla": "Blacksmith", "sta": "Stable", "tem": "Cathedral",
        "art": "Artillery Depot", "dip": "Diplomatic Center", "hou": "Housing/Dwelling",
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
        A("| Нация | sid | Имя (EN) | HP | Время (сек) | costpercent | Цена | farm |")
        A("|---|---|---|---:|---:|---:|---|---:|")
        for b in rows:
            A(f"| {b['nation']} | `{b['sid']}` | {b['name_en'] or '—'} "
              f"| {fmt(b['hp'])} | {fmt(b['buildtime_sec'])} | {fmt(b['costpercent'])} "
              f"| {fmt_cost(b)} | {fmt(b['farm'])} |")
        A("")

    A("### 4.2 Общие постройки\n")
    A("Sid формируется как `<cluster>+<3-letter>`, где cluster зависит от нации и типа здания "
      "(см. функцию `building_cluster()` в `parser/config.py`).\n")
    COMMON_SUF_NAMES = {
        "mil": "Mill", "sto": "Storehouse", "mar": "Market", "por": "Shipyard",
        "tow": "Tower", "gol": "Gold Mine", "iro": "Iron Mine", "coa": "Coal Mine",
        "swa": "Stone Wall", "sga": "Stone Gate", "wga": "Wood Gate", "wwa": "Palisade",
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
            A(f"| `{b['sid']}` | {b['name_en'] or '—'} | {fmt(b['hp'])} "
              f"| {fmt(b['buildtime_sec'])} | {fmt(b['costpercent'])} "
              f"| {fmt(b['food'])} | {fmt(b['wood'])} | {fmt(b['stone'])} "
              f"| {fmt(b['gold'])} | {fmt(b['iron'])} | {fmt(b['coal'])} "
              f"| {fmt(b['farm'])} | {prod_str or '—'} |")
        A("")

    # ----- 5. Units -----
    A("## 5. Юниты\n")
    A("Группировка по нациям. Цена дана в food/wood/stone/gold/iron/coal. "
      "Защиты — числа в диапазоне 0..240+ (выше = меньше получаемого урона по правилам игры).\n")
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
            A(f"| `{u['sid']}` | {u['name_en'] or '—'} "
              f"| {u.get('usage_short') or '—'} | {train_str} "
              f"| {u.get('uniqueness') or '—'} "
              f"| {fmt(u['hp'])} | {fmt(u['buildtime_sec'])} "
              f"| {fmt(u['food'])} | {fmt(u['gold'])} | {fmt(u['iron'])} "
              f"| {fmt(w0.get('damage'))} | {fmt(w0.get('radiusmax_tiles'))} | {fmt(w0.get('pause_sec'))} "
              f"| {fmt(u['prot_pike'])} | {fmt(u['prot_sword'])} | {fmt(u['prot_bullet'])} "
              f"| {fmt(u['prot_cannister'])} | {fmt(u['prot_arrow'])} | {fmt(u['prot_cannonball'])} |")
        A("")

    # ----- 5b. Ships -----
    A("## 5b. Корабли\n")
    A("Морские юниты: рыбацкая лодка, военные суда (фрегат/ксебек/баттлшип/чайка), "
      "стрелковые яхты/галеи. У всех `transport` — пассажирская грузоподъёмность, "
      "`fishingmax` — ёмкость трюма для рыбы, `fishingspeed` — тиков на одну рыбу.\n")
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
        A(f"| `{u['sid']}` | {u['nation']} | {u['name_en'] or '—'} "
          f"| {', '.join(u.get('trained_in', []) or []) or '—'} "
          f"| {fmt(u['hp'])} | {fmt(u['wood'])} | {fmt(u['gold'])} | {fmt(u['iron'])} | {fmt(u['coal'])} "
          f"| {fmt(w0.get('damage'))} | {fmt(w0.get('radiusmax_tiles'))} | {fmt(w0.get('pause_sec'))} | {cost_str} "
          f"| {fmt(w1.get('damage'))} | {fmt(w1.get('radiusmax_tiles'))} "
          f"| {fmt(u.get('transport'))} | {fmt(u.get('fishingmax'))} | {fmt(u.get('fishingspeed'))} "
          f"| {fmt(consume.get('gold'))} |")
    A("")
    A("**Заметки:**")
    A("- Базовая `fishingmax=1000` у `fishboat`. Апгрейд `aca.5` (academy.5, "
      "**boat efficiency +100%**) удваивает грузоподъёмность лодки → 2000 рыбы за рейс.")
    A("- Апгрейд `aca.7` (`fishing boat cost -85%`) удешевляет постройку лодок.")
    A("- `transport` на торговых/транспортных судах = сколько юнитов поместится.")
    A("- `consume.gold` = золото в секунду игрового времени на upkeep (тратится при стрельбе).")
    A("")

    # ----- 5c. Mine upgrades -----
    A("## 5c. Шахты — апгрейды (gol/iro/coa)\n")
    A("Шахты сразу после постройки имеют `peasantabsorber=5` (5 крестьян). "
      "Каждый апгрейд `<cluster>{gol|iro|coa}.X` добавляет N крестьян. Все 6 апгрейдов "
      "**накапливаются** на каждой шахте отдельно (`bindividual=True`). "
      "Полная прокачка одной шахты: **5 + 5 + 8 + 10 + 12 + 15 + 40 = 95 крестьян**.\n")
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
    A("**Стоимость полной прокачки одной шахты** (eur cluster, без override): "
      "F1000+5250+12500+15800+19800+50200 = **104550 food**, "
      "G1250+4950+9250+18500+21050+25950 = **80950 gold**.\n")
    A("**Производительность шахты:** 1 крестьянин внутри → +13 add to "
      "`gPlayer.counter.resincome[restype]` (player.script). "
      "Реальная скорость = 13 × 32 / 250 ≈ **1.664 ресурса/игр-сек на крестьянина**. "
      "Полностью прокачанная шахта (95 крестьян) = **158/игр-сек** = **9460/игр-мин**.\n")

    # ----- 6. Combat math -----
    A("## 6. Боевая математика\n")

    # 6a. Damage formula
    A("### 6a. Damage formula\n")
    A("Расчёт реально нанесённого урона (`miscext2.script:_misc_DoDamage`):\n")
    A("```")
    A("damage = weapon.damage")
    A("if (target is fast cavalry on the move AND weapon kind in {arrow, bullet}):")
    A("    damage -= 5  # headshot bonus")
    A("if (target is fully built):")
    A("    damage -= target.shield")
    A("else:  # still under construction")
    A("    damage -= target.shield // 3")
    A("if (target in formation): damage -= squad.AddShield  (or AddShieldHold if hold-mode)")
    A("damage -= target.protection[weapon.kind]")
    A("damage = max(1, damage)  # minimum 1 damage per hit")
    A("target.hp -= damage")
    A("```")
    A("**Ключевые свойства:**")
    A("- `protection` и `shield` уменьшают урон **аддитивно** (не процентно).")
    A("- Минимум **1 хп** урона за попадание — нет нулевого урона, даже если protection > damage.")
    A("- Танки/слоны (высокий shield) безусловно лучше, чем тяжёлые protection — shield применяется ВСЕГДА.")
    A("- Pikeman vs cavalry: pike kind с damage 8-10 vs heavy cavalry protection_pike (типично 0-3) ≈ 5-10 хп/удар.")
    A("- Cavalry vs pikeman: sword/saber damage ≈ 5-7 vs pike protection (0-3) ≈ 2-7 хп/удар.")
    A("- Ranged attack: bullet/arrow damage 9-12 vs musketeer protection (default 0-4) ≈ 5-12 хп/удар; "
      "против тяжёлой пехоты с protection_bullet=6+ урон режется существенно.")
    A("")

    # 6b. Speed table
    A("### 6b. Скорости юнитов (абстрактные единицы)\n")
    A("Базовые `gc_obj_speed_*` из `dmscript.global:603-620`. Это **относительные** "
      "значения скорости, **не тайлы/сек**. Реальная скорость зависит от animation `walkInterval`, "
      "`walkintervalfactor` юнита и game speed. Для перевода в тайлы/сек нужен empirical test.\n")
    A("| Класс | Базовая скорость |")
    A("|---|---:|")
    speed_table = data["economy"].get("obj_speed_table_abstract_units", {})
    for k in ["default","peasant","hardhorse","fasthorse","cannon","mortar","howitzer",
              "multicannon","fishboat","ferry","yacht","yachttur","chaika","galley",
              "frigate","xebec","battleship"]:
        if k in speed_table:
            A(f"| {k} | {speed_table[k]} |")
    A("")
    A("Большие значения = быстрее. fasthorse (96) ≈ ×3 от cannon (20). Peasant (40) "
      "примерно посередине. Battleship/multicannon (16) — самые медленные.\n")

    # 6c. Officers
    A("### 6c. Офицеры и формации\n")
    A("Каждая нация имеет N групп офицеров. Один офицер ведёт строй из определённых юнитов "
      "(чаще пехота/кавалерия одного класса). Формации стандартные для всех: "
      "**LINE / SQUARE / KARE × 15 / 36 / 72 / 120 / 196 / 400 юнитов**. Чем больше формация, "
      "тем сильнее бонусы (атака, защита, дистанция, мораль). Источник: `country.script:_country_InitOfficerFormations`.\n")
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
    A("## 6d. Рынок — обменные курсы\n")
    A("Рынок (`mar` building) позволяет менять ресурсы. Формула обмена использует "
      "**buy** и **sell** цены каждого ресурса. После сделки цены **сдвигаются**: "
      "`buycost` растёт к `buycostmax`, `sellcost` падает к `sellcostmin`. "
      "Поэтому повторные продажи одного и того же ресурса дают всё меньше.\n")
    A("**Default ratio:** при стандартных ценах `selling X for Y → received_Y = sold_X * sellcost[X] / buycost[Y]`.\n")
    A("| Ресурс | buy_min | buy_def | buy_max | sell_min | sell_def | sell_max |")
    A("|---|---:|---:|---:|---:|---:|---:|")
    for res, vals in data.get("market_rates", {}).items():
        if res.startswith("_"): continue
        A(f"| {res} | {vals['buycostmin']} | {vals['buycostdef']:.2f} | {vals['buycostmax']} "
          f"| {vals['sellcostmin']:.2f} | {vals['sellcostdef']:.2f} | {vals['sellcostmax']:.2f} |")
    A("")
    A("**Пример обмена при default ценах:**")
    A("- Sell 100 food (sellcost ≈ 15.20) → получишь `100 * 15.20 / 50 = 30.4` wood.")
    A("- Sell 100 gold (sellcost = 110) → получишь `100 * 110 / 50 = 220` wood.")
    A("- Sell 100 iron (sellcost = 60) → получишь `100 * 60 / 25 = 240` food.")
    A("")
    A("Источник: `res.script:_res_InitEconomy` (строки 178-249), "
      "`res.script:_res_MarketTradeResources` (320-344). "
      "`gc_economy_exp = 0.00002` контролирует скорость деградации курса.\n")
    A("")

    # Original 6 — combat costs
    A("### Стоимость одного выстрела (только для юнитов/зданий с `weapon.cost`)\n")
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
    A("## 7. Апгрейды\n")
    A("Доступные апгрейды по нациям. Цена показана только для тех, что удалось извлечь из script (большинство — extracted из `_country_Init`/`_country_InitUnitsUpgrades`). "
      "Для апгрейдов из локали без cost/time в этой таблице — данные см. в самом скрипте.\n")

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
            A(f"| `{u['sid']}` | {u['name_en'] or '—'} | {fmt(u['level'])} | {fmt(u['value'])} "
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
    A("### Известные ограничения парсера\n")
    A("- **Per-unit blacksmith/stable/barracks апгрейды:** symbolic-симулятор в "
      "`parser/simulate_upgrades.py` теперь раскрывает их полностью — извлекает cost, "
      "time, value для каждого `<nat><place>.<unit>.<itype>.<level>`. См. лист "
      "`Upgrades` в xlsx или [секцию 7 этого md](#7-апгрейды) — ~4000 строк апгрейдов "
      "с полными данными.\n")
    A("- **Override-механика апгрейдов:** некоторые апгрейды нация-специфично патчатся "
      "через `_country_ModifyUpgrade(country, ind-1, …)`. Симулятор отслеживает "
      "последний emit и накладывает патч. Если значение неожиданно — проверяй "
      "соседние строки в скрипте.\n")
    A("- **AI-метаданные** (`aiforce`, `bstandground`, `bturnoff` и т.д.) опущены — это "
      "тюнинг для AI-бота, не игрового баланса.\n")
    A("- **State-machine скрипты** (в `data/scripts/units/*.inc`) не парсятся — они "
      "описывают анимации/триггеры, а не статы.\n")
    A("- **Странные значения `value`:** некоторые апгрейды имеют `value=-7500000` или "
      "`value=-30` — это сырые числа из `_country_AddUpgrade`, представляют разные шкалы "
      "(множители времени, проценты со знаком). Смотри `gc_upg_type_*` в "
      "`dmscript.global` для расшифровки шкалы.\n")

    A("---\n")
    A("Сгенерировано из файлов игры. Перепарсить можно, запустив:\n")
    A("```")
    A("python parser/build_data.py     # обновляет output/data.json")
    A("python writers/write_xlsx.py    # обновляет xlsx")
    A("python writers/write_md.py      # обновляет этот md")
    A("```")

    MD_PATH.write_text("\n".join(out), encoding="utf-8")
    print(f"Wrote {MD_PATH} ({MD_PATH.stat().st_size:,} bytes, {len(out):,} lines)")


if __name__ == "__main__":
    main()
