"""Orchestrator: assemble all parsers into a unified per-nation, per-sid dataset.

Output structure (written to data.json):
{
  "constants": { "gc_*": {raw, value} },
  "nations": [{"sid", "name", "members": [sids], "upgrades": [upgrade-ids]}],
  "buildings": [
     {"sid","name","nation","kind":"common"|"per-nation","hp","buildtime","costpercent",
      "food","wood","stone","gold","iron","coal","farm","capturable","trains","upgrades"}
  ],
  "units": [
     {"sid","name","nation","trained_in","hp","buildtime","cost":{...},"weapons":[...],
      "protection":{...},"speed_factor","vision","searchradius","upkeep":{...}}
  ],
  "upgrades": [
     {"sid","name","place","nations":[...],"food/wood/...","time","value","itype","prereqs"}
  ],
  "economy": {...},
  "known_facts": [...],
  "gaps": [...]
}
"""
from __future__ import annotations
import sys, json, copy, math, re
from pathlib import Path
from collections import defaultdict

sys.stdout.reconfigure(encoding="utf-8")

from config import (UNIT_SCRIPT, COUNTRY_SCRIPT, DM_GLOBAL, LOCALE,
                    PLAYABLE_NATIONS, NATION_TO_COMMON_CLUSTER, _commonname,
                    building_cluster, OUTPUT_DIR, RECON_DIR, DATA_JSON,
                    px_to_tiles, decode_upg_type, PIXELS_TO_TILE,
                    decode_usage, OBJ_SPEED_TABLE)
from extract_constants import parse_constants
from parse_locale import load_all as load_locale
from parse_country import (parse_country, collect_for_nation,
                           _commonname_storehouse, _commonname_market, _commonname_port,
                           safe_eval as _safe_eval, make_env as _make_env)
from parse_units import parse_unit_init_base
from simulate_upgrades import simulate as simulate_upgrades


PER_NATION_BUILDING_SUFFIXES = ["aca", "art", "bar", "ba2", "bla", "cen",
                                "dip", "hou", "sta", "tem"]
COMMON_BUILDING_SUFFIXES = ["coa", "gol", "iro", "mar", "mil", "sto",
                            "por", "sga", "swa", "tow", "wga", "wwa"]


def _merge_stats(base: dict, override: dict) -> dict:
    """Deep-merge override into base. For nested dicts (weapons, cost, consume, produce),
    do per-key merging. Returns a new dict."""
    out = copy.deepcopy(base) if base else {}
    if not override:
        return out
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            for k2, v2 in v.items():
                if isinstance(v2, dict) and isinstance(out[k].get(k2), dict):
                    merged = dict(out[k][k2])
                    merged.update(v2)
                    out[k][k2] = merged
                else:
                    out[k][k2] = v2
        elif isinstance(v, set) and isinstance(out.get(k), set):
            out[k] = out[k] | v
        else:
            out[k] = v
    return out


def _compute_effective_unit(unit_data: dict, nation: str, sid: str) -> dict:
    """Apply nation override to base, then merc override if sid is in BMERCENARY_SIDS.
    nation is sid suffix like 'rus'. The merc override is the body of the
    `if (bmercenary)` block from unit.script — applies only to the 8 dip-suffixed
    sids that pass the bmercenary check (unit.script:613)."""
    from parse_units import BMERCENARY_SIDS
    base = unit_data["base"]
    override = unit_data["overrides"].get(nation)
    stats = _merge_stats(base, override) if override else copy.deepcopy(base)
    if sid in BMERCENARY_SIDS:
        merc = unit_data.get("bmerc_override")
        if merc:
            stats = _merge_stats(stats, merc)
    return stats


def _compute_effective_common_building(b_data: dict, cluster: str) -> dict:
    """Apply matching cluster override to base."""
    base = b_data["base"]
    override = b_data["overrides_cluster"].get(cluster)
    return _merge_stats(base, override) if override else copy.deepcopy(base)


def _compute_effective_nation_building(b_data: dict, nation: str) -> dict:
    """Apply matching nation override to base."""
    base = b_data["base"]
    override = b_data["overrides_nation"].get(nation)
    return _merge_stats(base, override) if override else copy.deepcopy(base)


def _sid_nation_suffix(sid: str) -> str | None:
    """Heuristic: if sid ends with a 3-letter playable nation code, return it."""
    if len(sid) <= 3:
        return None
    suf = sid[-3:]
    if suf in PLAYABLE_NATIONS:
        return suf
    return None


def _version_info() -> dict:
    """Capture extraction date + mtime of the most relevant game files.
    Used as a stamp so all derived files can show 'extracted on YYYY-MM-DD from
    game files modified YYYY-MM-DD'. After a game patch the mtime changes,
    making it easy to spot stale snapshots."""
    import datetime
    def ts(p):
        try:
            return datetime.datetime.fromtimestamp(p.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            return "unknown"
    return {
        "extracted_at_utc": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "extracted_at_local": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "game_files_mtime": {
            "unit.script": ts(UNIT_SCRIPT),
            "country.script": ts(COUNTRY_SCRIPT),
            "dmscript.global": ts(DM_GLOBAL),
        },
        "game_files_size": {
            "unit.script": UNIT_SCRIPT.stat().st_size if UNIT_SCRIPT.exists() else None,
            "country.script": COUNTRY_SCRIPT.stat().st_size if COUNTRY_SCRIPT.exists() else None,
            "dmscript.global": DM_GLOBAL.stat().st_size if DM_GLOBAL.exists() else None,
        },
    }


def assemble() -> dict:
    print("[1/5] Loading constants…", flush=True)
    constants = parse_constants(DM_GLOBAL)

    print("[2/5] Loading locale (en + ru)…", flush=True)
    loc_en = load_locale(LOCALE, "en")
    loc_ru = load_locale(LOCALE, "ru")

    print("[3/5] Parsing country.script…", flush=True)
    country = parse_country(COUNTRY_SCRIPT)
    country_text = COUNTRY_SCRIPT.read_text(encoding="utf-8", errors="replace")
    nation_data: dict[str, dict] = {}
    for nat in PLAYABLE_NATIONS:
        info = collect_for_nation(country["asts"][nat], nat)
        # _country_AddMember's 4th arg gates availability per nation
        # (e.g. lightcavalry passes `(hun)` — only Hungary). Evaluate it against
        # the per-nation env; if it cleanly evaluates to False, drop the member.
        nat_env = _make_env(nat)
        def _is_enabled(meta: dict) -> bool:
            arg = (meta.get("enabled_arg") or "").strip()
            if not arg:
                return True
            v = _safe_eval(arg, nat_env)
            return v is not False  # safe_eval returns True on parse failure (conservative)
        members = sorted(set(
            sid for sid, meta in info["members"]
            if sid and "+" not in sid and not sid.startswith("'")
            and _is_enabled(meta)
        ))
        upgrades_dict: dict[str, dict] = {}
        for uid, meta in info["upgrades"]:
            if not uid or uid == "null" or "+" in uid or uid.startswith("'"):
                # `null` is a placeholder no-op _country_AddUpgrade call in country.script
                continue
            upgrades_dict[uid] = meta
        # Now also pull simulated unit-upgrades from _country_InitUnitsUpgrades —
        # these have full cost/time/value/itype.
        sim_results = simulate_upgrades(country_text, nat)
        # `member` records (from _country_AddMember) carry the bare unit/building
        # sid but aren't upgrades — they belong to derived/country_members.json,
        # not data.json's upgrade list.
        sim_upgrades = [u for u in sim_results
                        if u.get("_kind") not in ("fixed_produce", "member")]
        sim_fixed = [u for u in sim_results if u.get("_kind") == "fixed_produce"]
        for u in sim_upgrades:
            upgrades_dict[u["sid"]] = u
        nation_data[nat] = {
            "members": members,
            "upgrades": upgrades_dict,
            "fixed_produces": info["fixed_produces"],
            "sim_fixed_produces": sim_fixed,
        }

    print("[4/5] Parsing unit.script…", flush=True)
    unit_text = UNIT_SCRIPT.read_text(encoding="utf-8", errors="replace")
    parsed_units = parse_unit_init_base(unit_text)

    print("[5/5] Assembling output…", flush=True)

    # ----- Build per-nation trained_in map (unit_sid → producer building sid) -----
    # _country_AddFixedProduce(country, fpind, producer, product, ...).
    # When producer is a peasant unit (peaXXX), product is a building that the peasant
    # constructs. When producer is a building, product is a unit it trains.
    trained_in: dict[tuple[str, str], set[str]] = {}
    constructs: dict[tuple[str, str], set[str]] = {}
    # Prereqs: for each (product, nation), list of req sids needed to enable production
    fp_prereqs: dict[tuple[str, str], set[str]] = {}
    BUILDING_SUFFIXES = {"cen","hou","bar","ba2","aca","bla","sta","dip","tem","art",
                          "mil","sto","mar","por","tow","gol","iro","coa","swa","sga","wga","wwa"}
    for nat in PLAYABLE_NATIONS:
        for fp in nation_data[nat].get("sim_fixed_produces", []):
            producer = fp.get("producer", "")
            product = fp.get("product", "")
            if not producer or not product:
                continue
            producer_is_building = (len(producer) >= 6 and producer[-3:] in BUILDING_SUFFIXES)
            if producer_is_building:
                trained_in.setdefault((product, nat), set()).add(producer)
            else:
                constructs.setdefault((producer, nat), set()).add(product)
            for r in fp.get("prereqs") or []:
                fp_prereqs.setdefault((product, nat), set()).add(r)

    # ----- Build building → produces mapping (inverse of trained_in) -----
    building_produces: dict[tuple[str, str], set[str]] = {}  # (building_sid, nation) → set of unit sids
    for (unit_sid, nat), buildings in trained_in.items():
        for b_sid in buildings:
            building_produces.setdefault((b_sid, nat), set()).add(unit_sid)

    # ----- Buildings -----
    buildings_rows: list[dict] = []
    for nat in PLAYABLE_NATIONS:
        nat_members = set(nation_data[nat]["members"])
        for suf in PER_NATION_BUILDING_SUFFIXES:
            sid = nat + suf
            if sid not in nat_members:
                continue
            b_data = parsed_units["nation_buildings"].get(suf)
            if not b_data:
                continue
            stats = _compute_effective_nation_building(b_data, nat)
            produces_list = list(building_produces.get((sid, nat), set()))
            row = _format_building_row(sid, nat, "per-nation", stats,
                                       loc_en, loc_ru, produces=produces_list)
            row["prereqs"] = sorted(fp_prereqs.get((sid, nat), set()))
            buildings_rows.append(row)
        for suf in COMMON_BUILDING_SUFFIXES:
            cluster = building_cluster(nat, suf)
            sid = cluster + suf
            if sid not in nat_members:
                continue
            b_data = parsed_units["common_buildings"].get(suf)
            if not b_data:
                continue
            # Sid prefix and override-cluster diverge for ukrwga/ukrwwa: every nation
            # builds the same `ukrwga` / `ukrwwa` sid, but the in-script `if (cluster)`
            # blocks key on the literal nation flag — `if (ukr)` is the only override
            # for these branches. So nation 'ukr' picks override 'ukr', everyone else
            # uses the base.
            override_cluster: str
            if suf in ("wga", "wwa"):
                override_cluster = "ukr" if nat == "ukr" else "__none__"
            else:
                override_cluster = cluster
            stats = _compute_effective_common_building(b_data, override_cluster)
            produces_list = list(building_produces.get((sid, nat), set()))
            row = _format_building_row(sid, nat, "common", stats,
                                       loc_en, loc_ru, cluster=cluster,
                                       produces=produces_list)
            row["prereqs"] = sorted(fp_prereqs.get((sid, nat), set()))
            buildings_rows.append(row)

    # ----- Units -----
    # `field` (wheat field) is an environment object, not a unit. It has no maxhp/weapons
    # and leaks into the units list otherwise.
    NON_UNIT_SIDS = {"field", "null"}
    unit_rows: list[dict] = []
    seen_unit_keys: set[tuple[str, str]] = set()
    for nat in PLAYABLE_NATIONS:
        nat_members = set(nation_data[nat]["members"])
        for sid in sorted(nat_members):
            # skip buildings (already emitted)
            if any(sid == nat + s for s in PER_NATION_BUILDING_SUFFIXES):
                continue
            if any(sid == _commonname(nat) + s for s in COMMON_BUILDING_SUFFIXES):
                continue
            if sid in (_commonname_storehouse(nat), _commonname_market(nat),
                       _commonname_port(nat)):
                continue
            if sid in NON_UNIT_SIDS:
                continue
            # Find unit data
            u_data = parsed_units["units"].get(sid)
            if not u_data:
                continue
            # Determine nation suffix for override
            nation_suf = _sid_nation_suffix(sid) or nat
            stats = _compute_effective_unit(u_data, nation_suf, sid)
            key = (sid, nat)
            if key in seen_unit_keys:
                continue
            seen_unit_keys.add(key)
            row = _format_unit_row(sid, nat, stats, loc_en, loc_ru)
            row["trained_in"] = sorted(trained_in.get((sid, nat), set()))
            row["prereqs"] = sorted(fp_prereqs.get((sid, nat), set()))
            unit_rows.append(row)

    # ----- Compute unique_to_nations: count distinct nations per unit sid -----
    sid_nation_count: dict[str, set[str]] = {}
    for r in unit_rows:
        sid_nation_count.setdefault(r["sid"], set()).add(r["nation"])
    for r in unit_rows:
        nat_count = len(sid_nation_count.get(r["sid"], set()))
        r["available_in_nations"] = nat_count
        if nat_count == 1:
            r["uniqueness"] = "unique"
        elif nat_count <= 3:
            r["uniqueness"] = f"semi-unique ({nat_count}n)"
        elif nat_count >= 18:
            r["uniqueness"] = "common"
        else:
            r["uniqueness"] = f"shared ({nat_count}n)"

    # ----- Upgrades -----
    # Combine: parsed upgrades from script (high-fidelity, has cost/time) + locale catalog
    # (lists every player-facing upgrade including ones we couldn't extract from script).
    upgrade_rows: list[dict] = []
    seen_upg: set[tuple[str, str]] = set()
    # First: parsed-from-script (have cost/time)
    for nat in PLAYABLE_NATIONS:
        for uid, meta in nation_data[nat]["upgrades"].items():
            key = (uid, nat)
            if key in seen_upg:
                continue
            seen_upg.add(key)
            upgrade_rows.append(_format_upgrade_row(uid, nat, meta, loc_en, loc_ru))
    # Second: locale-only — entries not found in script (cost/time unknown)
    for upg_key in loc_en.files["upgrades"].keys():
        # %nat% template — expand per nation
        if "%nat%" in upg_key:
            for nat in PLAYABLE_NATIONS:
                resolved_uid = upg_key.replace("%nat%", nat)
                key = (resolved_uid, nat)
                if key in seen_upg:
                    continue
                seen_upg.add(key)
                upgrade_rows.append(_format_locale_only_upgrade(resolved_uid, nat, upg_key, loc_en, loc_ru))
        else:
            # Try to detect nation from key prefix (e.g., 'algaca.6')
            nat_pref = upg_key[:3]
            if nat_pref in PLAYABLE_NATIONS:
                key = (upg_key, nat_pref)
                if key in seen_upg:
                    continue
                seen_upg.add(key)
                upgrade_rows.append(_format_locale_only_upgrade(upg_key, nat_pref, upg_key, loc_en, loc_ru))

    # ----- Economy / known facts -----
    economy = build_economy(constants)
    market_rates = build_market_rates()
    print("[5b/5] Extracting officer formations…", flush=True)
    officers = extract_officers(country_text)
    discrepancies = build_discrepancies(constants)
    gaps = collect_gaps(parsed_units, nation_data)

    result = {
        "version": _version_info(),
        "constants": {k: v for k, v in constants.items()},
        "nations": [
            {"sid": n, "name_en": loc_en.get("units", n), "name_ru": loc_ru.get("units", n),
             "members": nation_data[n]["members"],
             "upgrade_count": len(nation_data[n]["upgrades"])}
            for n in PLAYABLE_NATIONS
        ],
        "buildings": buildings_rows,
        "units": unit_rows,
        "upgrades": upgrade_rows,
        "economy": economy,
        "market_rates": market_rates,
        "officers": officers,
        "discrepancies": discrepancies,
        "gaps": gaps,
    }
    # Sanity checks need the assembled data; run last
    result["sanity_checks"] = build_sanity_checks(result, parsed_units, constants)
    return result


def _format_building_row(sid: str, nation: str, kind: str, stats: dict,
                         loc_en, loc_ru, cluster: str | None = None,
                         produces: list[str] | None = None) -> dict:
    com = sid[:3] if sid[:3] in {"eur", "rus", "tur", "spa", "ukr", "por"} else _commonname(nation)
    name_en = loc_en.lookup_unit_name(sid, nat=nation, com=com)
    name_ru = loc_ru.lookup_unit_name(sid, nat=nation, com=com)
    weapons = stats.get("weapons", {})
    return {
        "sid": sid,
        "nation": nation,
        "name_en": name_en,
        "name_ru": name_ru,
        "kind": kind,
        "cluster": cluster,
        "hp": stats.get("maxhp"),
        "buildtime_frames": stats.get("buildtime"),
        "buildtime_sec": _buildtime_to_sec(stats.get("buildtime")),
        "costpercent": stats.get("costpercent"),
        "food": stats.get("food", 0),
        "wood": stats.get("wood", 0),
        "stone": stats.get("stone", 0),
        "gold": stats.get("gold", 0),
        "iron": stats.get("iron", 0),
        "coal": stats.get("coal", 0),
        "farm": stats.get("farm", 0),
        "score": stats.get("score"),
        "usage": stats.get("usage"),
        "usage_short": decode_usage(stats.get("usage")),
        "produces": sorted(produces or []),
        "capturable": stats.get("bcapture"),
        "vision": stats.get("vision"),
        "weapon_damage": weapons.get(0, {}).get("damage") if weapons else None,
        "weapon_pause_frames": weapons.get(0, {}).get("pause") if weapons else None,
        "weapon_radiusmax": weapons.get(0, {}).get("radiusmax") if weapons else None,
        "weapon_kind": weapons.get(0, {}).get("kind") if weapons else None,
        "weapon_cost": weapons.get(0, {}).get("cost") if weapons else None,
        "consume": stats.get("consume"),
        "produce": stats.get("produce"),
        "peasantabsorber": stats.get("peasantabsorber"),
        "resourcebase": sorted(list(stats.get("resourcebase", set()))),
        "bnohungry": stats.get("bnohungry", False),
        "bbuilding": stats.get("bbuilding", True),
        "bgate": stats.get("bgate", False),
        "bwall": stats.get("bwall", False),
    }


def _resolve_speed(raw):
    """Convert raw `speed` (either int, None, or `'gc_obj_speed_<key>'` string) into
    a numeric value. Default to gc_obj_speed_default = 32 when not set, matching
    classes.script:3589 TObjBase.Create which seeds `speed := gc_obj_speed_default`."""
    if raw is None:
        return OBJ_SPEED_TABLE["default"]
    if isinstance(raw, (int, float)):
        return raw
    if isinstance(raw, str) and raw.startswith("gc_obj_speed_"):
        key = raw[len("gc_obj_speed_"):]
        if key in OBJ_SPEED_TABLE:
            return OBJ_SPEED_TABLE[key]
    return raw  # leave as-is for debugging if it's something unexpected


_FOODPERUNIT_RE = re.compile(r"^\s*floor\s*\(\s*gc_obj_foodperunit\s*\*\s*([\d.]+)\s*\)\s*$")


def _eval_consume_expr(value):
    """Evaluate `floor(gc_obj_foodperunit*K)` expressions to int. Pass-through
    integers / unknown forms unchanged. Used to flatten 7 unique expressions
    that script writers used in unit `consume` blocks (parse_units.py kept
    them as raw strings)."""
    if isinstance(value, int) or value is None:
        return value
    if isinstance(value, str):
        m = _FOODPERUNIT_RE.match(value)
        if m:
            return math.floor(30 * float(m.group(1)))  # gc_obj_foodperunit = 30
    return value


def _format_unit_row(sid: str, nation: str, stats: dict, loc_en, loc_ru) -> dict:
    com = _commonname(nation)
    name_en = loc_en.lookup_unit_name(sid, nat=nation, com=com)
    name_ru = loc_ru.lookup_unit_name(sid, nat=nation, com=com)
    # Evaluate any string-form consume expressions (e.g. floor(gc_obj_foodperunit*2) → 60)
    consume = stats.get("consume")
    if isinstance(consume, dict):
        consume = {k: _eval_consume_expr(v) for k, v in consume.items()}
    weapons = stats.get("weapons", {})
    weapon_list = []
    for idx in sorted(weapons.keys()):
        w = weapons[idx]
        weapon_list.append({
            "index": idx,
            "damage": w.get("damage"),
            "pause_frames": w.get("pause"),
            "pause_sec": _frames_to_sec(w.get("pause")),
            "radiusmin_px": w.get("radiusmin"),
            "radiusmin_tiles": px_to_tiles(w.get("radiusmin")),
            "radiusmax_px": w.get("radiusmax"),
            "radiusmax_tiles": px_to_tiles(w.get("radiusmax")),
            "dispertion_px": w.get("dispertion"),
            "dispertion_tiles": px_to_tiles(w.get("dispertion")),
            "kind": w.get("kind"),
            "weaponsid": w.get("weaponsid"),
            "cost": w.get("cost"),
        })
    return {
        "sid": sid,
        "nation": nation,
        "name_en": name_en,
        "name_ru": name_ru,
        "hp": stats.get("maxhp"),
        "buildtime_frames": stats.get("buildtime"),
        "buildtime_sec": _frames_to_sec(stats.get("buildtime")),
        "food": stats.get("food", 0),
        "wood": stats.get("wood", 0),
        "stone": stats.get("stone", 0),
        "gold": stats.get("gold", 0),
        "iron": stats.get("iron", 0),
        "coal": stats.get("coal", 0),
        "costpercent": stats.get("costpercent"),
        "score": stats.get("score"),
        "usage": stats.get("usage"),
        "usage_short": decode_usage(stats.get("usage")),
        "vision": stats.get("vision"),
        "searchradius_px": stats.get("searchradius"),
        "searchradius_tiles": px_to_tiles(stats.get("searchradius")),
        "transport": stats.get("transport"),
        "fishingmax": stats.get("fishingmax"),
        "fishingspeed": stats.get("fishingspeed"),
        "aiforce": stats.get("aiforce"),
        "walkintervalfactor": stats.get("walkintervalfactor"),
        "shield": stats.get("shield"),
        "speed": _resolve_speed(stats.get("speed")),
        "prot_pike": stats.get("prot_pike"),
        "prot_sword": stats.get("prot_sword"),
        "prot_bullet": stats.get("prot_bullet"),
        "prot_cannister": stats.get("prot_cannister"),
        "prot_arrow": stats.get("prot_arrow"),
        "prot_cannonball": stats.get("prot_cannonball"),
        "weapons": weapon_list,
        "consume": consume,
        "peasantabsorber": stats.get("peasantabsorber"),
        "bnohungry": stats.get("bnohungry", False),
        "bmercenary": stats.get("bmercenary", False),
        "bofficer": stats.get("bofficer", False),
        "bdrummer": stats.get("bdrummer", False),
        "bpriest": stats.get("bpriest", False),
        "bartillery": stats.get("bartillery", False),
        "bartprepare": stats.get("bartprepare", False),
    }


UPG_RE = re.compile(r"^(?P<place>[a-z]+)\.(?P<rest>.+)$")


def _format_upgrade_row(uid: str, nation: str, meta: dict, loc_en, loc_ru) -> dict:
    # Upgrade ID typically: "<place>.<member>.<itype>.<level>" e.g. "ausbla.pikeman.1.5"
    # Or "<nat><place>.<level>" e.g. "ausaca.1"
    name_en = loc_en.get("upgrades", uid)
    name_ru = loc_ru.get("upgrades", uid)
    if name_en is None:
        for nat in [nation]:
            templated = uid.replace(nat, "%nat%", 1)
            if templated != uid:
                v = loc_en.get("upgrades", templated)
                if v is not None:
                    name_en = v.replace("%nat%", nat)
                    break
    if name_ru is None:
        for nat in [nation]:
            templated = uid.replace(nat, "%nat%", 1)
            if templated != uid:
                v = loc_ru.get("upgrades", templated)
                if v is not None:
                    name_ru = v.replace("%nat%", nat)
                    break
    # Synthesize a name from sid for blacksmith/stable/barracks unit upgrades:
    # "<nat><place>.<member>.<itype>.<level>" → "<Place> <Member> +<value> (lvl X)"
    if name_en is None and meta.get("place") and meta.get("member"):
        place_suffix = meta["place"][3:]
        place_name = {
            "bla": "Blacksmith", "bar": "Barracks 17c", "ba2": "Barracks 18c",
            "sta": "Stable", "aca": "Academy", "art": "Artillery",
        }.get(place_suffix, place_suffix.upper())
        itype_name = {"damage": "damage", "protection": "protection"}.get(meta.get("itype"), meta.get("itype") or "")
        name_en = f"{place_name} {meta['member']} {itype_name} +{meta.get('value','?')} (lvl {meta.get('level','?')})"

    # Same synthesis for Russian when name_ru is missing.
    if not name_ru and meta.get("place") and meta.get("member"):
        place_suffix = meta["place"][3:]
        place_ru = {
            "bla": "Кузница", "bar": "Казарма 17 в.", "ba2": "Казарма 18 в.",
            "sta": "Конюшня", "aca": "Академия", "art": "Артиллерийское депо",
        }.get(place_suffix, place_suffix.upper())
        itype_ru = {"damage": "урон", "protection": "защита"}.get(meta.get("itype"), meta.get("itype") or "")
        name_ru = f"{place_ru} · {meta['member']} {itype_ru} +{meta.get('value','?')} (ур. {meta.get('level','?')})"

    # Clean locale noise: %color(XXX)%, %include(...)%, leftover %word%
    name_en_clean = (name_en or "").split("\n", 1)[0]
    name_ru_clean = (name_ru or "").split("\n", 1)[0]
    name_en_clean = re.sub(r"%color\([^)]+\)%", "", name_en_clean)
    name_ru_clean = re.sub(r"%color\([^)]+\)%", "", name_ru_clean)
    name_en_clean = re.sub(r"%include\([^)]+\)%", "", name_en_clean).strip()
    name_ru_clean = re.sub(r"%include\([^)]+\)%", "", name_ru_clean).strip()

    itype_short, itype_desc = decode_upg_type(meta.get("itype"))
    return {
        "sid": uid,
        "nation": nation,
        "name_en": name_en_clean,
        "name_ru": name_ru_clean,
        "level": _to_int(meta.get("level")),
        "value": _to_int(meta.get("value")),
        "itype": meta.get("itype"),
        "itype_short": itype_short,
        "itype_desc": itype_desc,
        "tooltiptype": meta.get("tooltiptype"),
        "time_frames": _to_int(meta.get("time")),
        "time_sec": _frames_to_sec(_to_int(meta.get("time"))),
        "food":  _to_int(meta.get("food")),
        "wood":  _to_int(meta.get("wood")),
        "stone": _to_int(meta.get("stone")),
        "gold":  _to_int(meta.get("gold")),
        "iron":  _to_int(meta.get("iron")),
        "coal":  _to_int(meta.get("coal")),
        "iarr1": meta.get("iarr1"),
        "sarr2": meta.get("sarr2"),
        "targets": meta.get("targets") or [],            # unit/building sids this upgrade modifies
        "resource_pcts": meta.get("resource_pcts") or {}, # priceperc only: {res: pct}
        "place": meta.get("place"),
        "member": meta.get("member"),
        "prereqs": meta.get("prereqs") or [],
        "_source": meta.get("_source") or "",
    }


def _format_locale_only_upgrade(uid: str, nation: str, locale_key: str, loc_en, loc_ru) -> dict:
    """Build an upgrade row when only the locale entry is known (cost/time unknown)."""
    name_en = loc_en.get("upgrades", locale_key) or ""
    name_ru = loc_ru.get("upgrades", locale_key) or ""
    name_en = name_en.replace("%nat%", nation).split("\n", 1)[0]
    name_ru = name_ru.replace("%nat%", nation).split("\n", 1)[0]
    # Strip locale noise: %color(...)%, %include(...)%, leftover %word% style markers.
    name_en = re.sub(r"%color\([^)]+\)%", "", name_en)
    name_ru = re.sub(r"%color\([^)]+\)%", "", name_ru)
    name_en = re.sub(r"%include\([^)]+\)%", "", name_en).strip()
    name_ru = re.sub(r"%include\([^)]+\)%", "", name_ru).strip()
    return {
        "sid": uid,
        "nation": nation,
        "name_en": name_en,
        "name_ru": name_ru,
        "level": None,
        "value": None,
        "itype": None,
        "tooltiptype": None,
        "time_frames": None,
        "time_sec": None,
        "food": None, "wood": None, "stone": None,
        "gold": None, "iron": None, "coal": None,
        "iarr1": None, "sarr2": None,
        "_source": "locale_only",
    }


def _to_int(s):
    if s is None:
        return None
    if isinstance(s, int):
        return s
    s = str(s).strip()
    if s == "" or s.lower() == "default":
        return None
    s = re.sub(r"\{[^}]*\}", "", s).strip()
    try:
        return int(s)
    except (ValueError, TypeError):
        try:
            return int(eval(s, {"__builtins__": {}}, {}))
        except Exception:
            return None


def _frames_to_sec(frames):
    """Convert raw 'frames' integer to game-time seconds for UNITS/upgrades/weapons.
    Uses _misc_FramesToTime: val × 1/32. See misc.script:470.
    """
    if frames is None:
        return None
    try:
        f = int(frames)
        return round(f / 32.0, 2)  # gc_time_to_frames = 32
    except (ValueError, TypeError):
        return None


def _buildtime_to_sec(frames):
    """Convert raw 'frames' integer to game-time seconds for BUILDINGS.
    Uses _misc_BuildtimeToTime: val × 1/32 × gc_buildtime_modifier(=10). See misc.script:478.
    Result is 10× larger than _frames_to_sec for the same input.
    Fixes a bug where buildings reported 10× too short buildtime.
    """
    if frames is None:
        return None
    try:
        f = int(frames)
        # gc_time_to_frames=32, gc_buildtime_modifier=10
        return round(f * 10.0 / 32.0, 2)
    except (ValueError, TypeError):
        return None


def build_economy(constants: dict) -> dict:
    return {
        "time_to_frames": constants.get("gc_time_to_frames", {}).get("value"),
        "pixels_to_tile": PIXELS_TO_TILE,
        "gamespeed_slow": constants.get("gc_settings_gamespeed_0", {}).get("value"),
        "gamespeed_normal": constants.get("gc_settings_gamespeed_1", {}).get("value"),
        "gamespeed_fast": constants.get("gc_settings_gamespeed_2", {}).get("value"),
        "max_obj_count": constants.get("gc_MaxObjCount", {}).get("value"),
        "max_player_count": constants.get("gc_MaxPlayerCount", {}).get("value"),
        "field_max_hp": constants.get("gc_FieldMaxHP", {}).get("value"),
        "resource_portion_food":  constants.get("gc_obj_resource_portion_food", {}).get("value"),
        "resource_portion_wood":  constants.get("gc_obj_resource_portion_wood", {}).get("value"),
        "resource_portion_stone": constants.get("gc_obj_resource_portion_stone", {}).get("value"),
        "resource_portion_others": 20,
        "hits_needed_food":  constants.get("gc_resource_hitsneeded_food", {}).get("value"),
        "hits_needed_wood":  constants.get("gc_resource_hitsneeded_wood", {}).get("value"),
        "hits_needed_stone": constants.get("gc_resource_hitsneeded_stone", {}).get("value"),
        "food_per_unit_upkeep": constants.get("gc_obj_foodperunit", {}).get("value"),
        "default_eff_percent": 100,
        "extraction_formula": "delivered = (base_portion * eff) / 100  (integer division). "
                              "eff defaults to 100; upgrades add to it additively.",
        "damage_formula": (
            "applied_damage = max(1, weapon_damage - target.shield - target.protection[weapon_kind] "
            "- squad_shield_bonus - misc_modifiers).  "
            "Headshot bonus: -5 damage to fast-cavalry on the move when hit by arrow/bullet. "
            "If target is still being built: shield is divided by 3.  "
            "Source: miscext2.script:_misc_DoDamage (lines 274-450)."
        ),
        "obj_speed_table_abstract_units": OBJ_SPEED_TABLE,
        "obj_speed_table_note": (
            "Values are abstract speed units (NOT tiles/sec). They scale movement relative "
            "to walkintervalfactor and game speed. Empirical testing required for absolute "
            "tiles/sec. Reference: dmscript.global:603-620, gc_obj_speed_*."
        ),
    }


def build_market_rates() -> dict:
    """Extract gEconomy[i] init values from res.script:178-249. Static representation.

    The food/stone formulas are copied verbatim from the script:
      food:  sellcostdef = 18.24095 * 0.8333; min = def * 0.7; max = def * 1.3
             (res.script:195-197)
      stone: sellcostdef = 19.29725 * 1.08306; min = def * 0.75; max = def * 1.25
    The constants 18.24095 / 19.29725 / 0.8333 / 1.08306 are unexplained in the
    script — preserved as-is so our values match the engine bit-for-bit.
    """
    return {
        "food":  {"buycostmin": 20,  "buycostdef": 25,  "buycostmax": 40,
                   "sellcostmin": 18.24095*0.8333*0.7,
                   "sellcostdef": 18.24095*0.8333,
                   "sellcostmax": 18.24095*0.8333*1.3},
        "wood":  {"buycostmin": 40,  "buycostdef": 50,  "buycostmax": 60,
                   "sellcostmin": 20, "sellcostdef": 30, "sellcostmax": 40},
        "stone": {"buycostmin": 40,  "buycostdef": 50,  "buycostmax": 60,
                   "sellcostmin": 19.29725*1.08306*0.75,
                   "sellcostdef": 19.29725*1.08306,
                   "sellcostmax": 19.29725*1.08306*1.25},
        "gold":  {"buycostmin": 140, "buycostdef": 190, "buycostmax": 240,
                   "sellcostmin": 80, "sellcostdef": 110, "sellcostmax": 140},
        "iron":  {"buycostmin": 100, "buycostdef": 140, "buycostmax": 180,
                   "sellcostmin": 40, "sellcostdef": 60,  "sellcostmax": 80},
        "coal":  {"buycostmin": 100, "buycostdef": 140, "buycostmax": 180,
                   "sellcostmin": 40, "sellcostdef": 60,  "sellcostmax": 80},
        "_note": (
            "Market exchange rates from res.script:_res_InitEconomy. Each resource has "
            "min/def/max for buy and sell. After each trade, prices SHIFT toward max (for "
            "buy) and min (for sell) — selling/buying same resource repeatedly degrades "
            "the rate. Formula uses gc_economy_exp/gc_economy_time as decay constants. "
            "Default exchange ratio: sell X to buy Y at ratio sellcost[X]/buycost[Y] (resources / unit). "
            "Example default: sell 1 food (sellcostdef≈15.2) → buy ~0.3 wood (buycostdef=50). "
            "Source: res.script:_res_InitEconomy (lines 178-249), _res_MarketTradeResources (320-344)."
        ),
    }


def extract_officers(country_text: str) -> list[dict]:
    """Extract officer formation data per nation. Each officer entry:
    {nation, officersid, drummersid, units: [...]}.

    Officer formations are universal (LINE/SQUARE/KARE × 15/36/72/120/196/400),
    so we don't repeat them per officer.
    """
    from simulate_upgrades import (extract_proc_body, _presubstitute, tokenize,
                                    SimParser, walk_sim, make_env)
    out: list[dict] = []
    body = extract_proc_body(country_text, "_country_InitOfficerFormations")
    for nat in PLAYABLE_NATIONS:
        body_nat = _presubstitute(body, nat)
        tokens = tokenize(body_nat)
        if tokens and tokens[0] == ("KW", "begin"):
            tokens = tokens[1:]
        parser = SimParser(tokens)
        root = parser.parse_block()

        # Custom walker just collecting AddOfficersFormationInf* call args
        sink = []
        env = make_env(nat)
        # We need _country_IsCountryMember to always return True so the
        # AddOfficersFormationInfExt body executes; in our walker, it appears as a call,
        # which we don't evaluate. We just pull the call args of AddOfficersFormation*.
        _walk_officers(root, env, sink, nat)
        for entry in sink:
            entry["nation"] = nat
            out.append(entry)
    return out


def _walk_officers(node, env, sink, nation):
    """Walk AST and collect AddOfficersFormationInfExt / NoOfficersExt calls."""
    if node is None:
        return
    k = node.kind
    if k in ("block", "with"):
        for c in node.children:
            _walk_officers(c, env, sink, nation)
    elif k == "loop":
        if node.cond and "|" in node.cond:
            var_name, start_expr, end_expr = node.cond.split("|", 2)
            try:
                start = int(eval(start_expr, {"__builtins__": {}}, env))
                end = int(eval(end_expr, {"__builtins__": {}}, env))
            except Exception:
                for c in node.children:
                    _walk_officers(c, env, sink, nation)
                return
            if end - start > 100:
                end = start + 100
            for i in range(start, end + 1):
                env[var_name] = i
                for c in node.children:
                    _walk_officers(c, env, sink, nation)
        else:
            for c in node.children:
                _walk_officers(c, env, sink, nation)
    elif k == "if":
        from simulate_upgrades import _pascal_to_py
        cond = _pascal_to_py(node.cond or "True")
        try:
            v = eval(cond, {"__builtins__": {}}, env)
        except Exception:
            v = True
        if v:
            _walk_officers(node.children[0], env, sink, nation)
        elif node.else_block is not None:
            _walk_officers(node.else_block, env, sink, nation)
    elif k == "case":
        from simulate_upgrades import _pascal_to_py, NATION_LITERAL
        cond = _pascal_to_py(node.cond.strip()) if node.cond else ""
        try:
            cond_val = eval(cond, {"__builtins__": {}}, env)
        except Exception:
            cond_val = None
        else_node = None
        matched = False
        for child in node.children:
            if child.kind == "case_else":
                else_node = child
                continue
            if child.kind != "case_branch":
                continue
            label = (child.cond or "").strip()
            if matched:
                continue
            label_parts = [p.strip() for p in label.split(",")]
            for part in label_parts:
                if part in NATION_LITERAL:
                    if NATION_LITERAL[part] == nation:
                        _walk_officers(child.children[0], env, sink, nation)
                        matched = True
                        break
                try:
                    pv = eval(_pascal_to_py(part), {"__builtins__": {}}, env)
                    if cond_val == pv:
                        _walk_officers(child.children[0], env, sink, nation)
                        matched = True
                        break
                except Exception:
                    pass
        if not matched and else_node is not None:
            _walk_officers(else_node.children[0], env, sink, nation)
    elif k == "assign":
        # Track string vars
        if "." not in node.name and "[" not in node.name:
            from simulate_upgrades import _eval_string_arg
            val = _eval_string_arg(node.args[0] if node.args else "", env)
            env[node.name] = val
    elif k == "call":
        name = node.name
        args = node.args or []
        if name in ("AddOfficersFormationInfExt", "AddOfficersFormationInfNoOfficersExt",
                     "AddOfficersFormationCavalryExt", "AddOfficersFormationGrenadierExt",
                     "AddOfficersFormationCannonExt", "AddOfficersFormationMortarExt"):
            from simulate_upgrades import _eval_string_arg
            entry: dict = {"call": name, "officersid": "", "drummersid": "", "units": []}
            if name == "AddOfficersFormationInfNoOfficersExt":
                # signature: (country, ind, u0)
                u0 = _eval_string_arg(args[2] if len(args) > 2 else "''", env)
                entry["officersid"] = u0
                entry["drummersid"] = u0
                entry["units"] = [u0] if u0 else []
            else:
                # signature: (country, ind, officersid, drummersid, u0..u18)
                if len(args) > 2:
                    entry["officersid"] = _eval_string_arg(args[2], env)
                if len(args) > 3:
                    entry["drummersid"] = _eval_string_arg(args[3], env)
                units = []
                for i in range(4, min(len(args), 24)):
                    u = _eval_string_arg(args[i], env)
                    if u:
                        units.append(u)
                entry["units"] = units
            if entry["officersid"]:
                sink.append(entry)


def build_discrepancies(constants: dict) -> list[dict]:
    """Real discrepancies between user's prompt-time notes and the source files.
    Only items where the file value differs from what was originally claimed.
    """
    items = []
    file_food_hits = constants.get("gc_resource_hitsneeded_food", {}).get("value")
    items.append({
        "fact": "hits_needed for food",
        "user_note": 30,
        "file_value": file_food_hits,
        "source": "dmscript.global:799 gc_resource_hitsneeded_food",
        "verdict": "Файл: 22, не 30. Доверяем файлу — крестьянин делает 22 удара мотыгой "
                    "до возврата к складу, не 30. Это укорачивает рейс и повышает фактический rate.",
    })
    items.append({
        "fact": "Field melioration (academy aca.4) cost",
        "user_note": "W1400 / G522",
        "file_value": "W1000 / G475 (any nation)",
        "source": "country.script:3490 _country_AddUpgrade('aca.4', ..., wood=1000, gold=475)",
        "verdict": "Файл: W1000/G475. Расхождение с промпт-заметками — возможно, цифры "
                    "из старой версии игры. Все 21 нация имеют одинаковую стоимость.",
    })
    items.append({
        "fact": "'Manufacture agricultural equipment' (blacksmith) cost",
        "user_note": "W400 / G100",
        "file_value": "не найден в blacksmith — этот апгрейд может быть из старого названия",
        "source": "country.script — нет blacksmith-апгрейда с такими параметрами",
        "verdict": "Текущий blacksmith содержит per-unit damage/protection апгрейды. "
                    "Возможно, в C1 был отдельный agricultural-equipment апгрейд, который "
                    "в C3 переименован в `aca.X` (academy). См. лист Upgrades с place=aca.",
    })
    return items


def build_sanity_checks(data: dict, parsed_units: dict, constants: dict) -> list[dict]:
    """Automated assertions about the data. Pass/fail rows that flag regressions
    after a game patch.

    Each check: {category, name, expected, actual, pass: bool}
    """
    checks: list[dict] = []

    def add(cat: str, name: str, expected, actual):
        ok = (expected == actual) if not isinstance(expected, str) else (expected == str(actual))
        checks.append({"category": cat, "name": name, "expected": expected,
                        "actual": actual, "pass": ok})

    def add_op(cat: str, name: str, op: str, expected, actual):
        if op == ">=":
            ok = actual is not None and actual >= expected
        elif op == "<=":
            ok = actual is not None and actual <= expected
        elif op == ">":
            ok = actual is not None and actual > expected
        else:
            ok = actual == expected
        checks.append({"category": cat, "name": name,
                        "expected": f"{op} {expected}", "actual": actual, "pass": ok})

    # Constants
    add("constants", "gc_time_to_frames",
        32, constants.get("gc_time_to_frames", {}).get("value"))
    add("constants", "gc_resource_hitsneeded_food",
        22, constants.get("gc_resource_hitsneeded_food", {}).get("value"))
    add("constants", "gc_resource_hitsneeded_wood",
        14, constants.get("gc_resource_hitsneeded_wood", {}).get("value"))
    add("constants", "gc_resource_hitsneeded_stone",
        20, constants.get("gc_resource_hitsneeded_stone", {}).get("value"))
    add("constants", "gc_obj_resource_portion_food",
        45, constants.get("gc_obj_resource_portion_food", {}).get("value"))
    add("constants", "gc_obj_resource_portion_wood",
        28, constants.get("gc_obj_resource_portion_wood", {}).get("value"))
    add("constants", "gc_obj_resource_portion_stone",
        40, constants.get("gc_obj_resource_portion_stone", {}).get("value"))
    add("constants", "gc_FieldMaxHP",
        25000, constants.get("gc_FieldMaxHP", {}).get("value"))
    add("constants", "gc_obj_foodperunit",
        30, constants.get("gc_obj_foodperunit", {}).get("value"))
    add("constants", "gc_MaxObjCount",
        32000, constants.get("gc_MaxObjCount", {}).get("value"))

    # Counts (regression guards)
    add("counts", "Playable nations", 21, len(data["nations"]))
    add_op("counts", "Building rows (sid×nation)", ">=", 410, len(data["buildings"]))
    add_op("counts", "Unit rows (sid×nation)", ">=", 700, len(data["units"]))
    add_op("counts", "Upgrade rows (sid×nation)", ">=", 4000, len(data["upgrades"]))
    add_op("counts", "Officer entries", ">=", 100, len(data.get("officers", [])))

    # Per-nation roster checks
    nation_buildings = {n["sid"]: 0 for n in data["nations"]}
    for b in data["buildings"]:
        nation_buildings[b["nation"]] = nation_buildings.get(b["nation"], 0) + 1
    for nat in PLAYABLE_NATIONS:
        cnt = nation_buildings.get(nat, 0)
        # Most nations have ~20 buildings (10 per-nation + ~10 common). Ukr has ~16 (no ba2/swa/sga/tow), tur has ~19.
        add_op("nations", f"{nat} building count", ">=", 15, cnt)

    # Critical building presence
    cen_in_nation: dict[str, bool] = {}
    bar_in_nation: dict[str, bool] = {}
    for b in data["buildings"]:
        if b["sid"] == b["nation"] + "cen":
            cen_in_nation[b["nation"]] = True
        if b["sid"] == b["nation"] + "bar":
            bar_in_nation[b["nation"]] = True
    for nat in PLAYABLE_NATIONS:
        add("buildings", f"у {nat} есть Городской центр ({nat}cen)", True, cen_in_nation.get(nat, False))
        add("buildings", f"у {nat} есть Казарма 17 в. ({nat}bar)", True, bar_in_nation.get(nat, False))

    # Building base values
    cen_data = parsed_units["nation_buildings"].get("cen", {}).get("base", {})
    bar_data = parsed_units["nation_buildings"].get("bar", {}).get("base", {})
    ba2_data = parsed_units["nation_buildings"].get("ba2", {}).get("base", {})
    add("buildings", "базовый HP Городского центра", 4000, cen_data.get("maxhp"))
    add("buildings", "базовое farm Городского центра", 100, cen_data.get("farm"))
    add("buildings", "базовый costpercent Городского центра", 300, cen_data.get("costpercent"))
    add("buildings", "базовое farm Казармы 17 в.", 150, bar_data.get("farm"))
    add("buildings", "базовое farm Казармы 18 в.", 250, ba2_data.get("farm"))

    # Mine semantics
    gol_data = parsed_units["common_buildings"].get("gol", {}).get("base", {})
    add("buildings", "Mine peasantabsorber base", 5, gol_data.get("peasantabsorber"))
    add("buildings", "Mine produce per peasant", 13,
        gol_data.get("produce", {}).get("gold"))

    # Mine upgrade chain (one nation as representative)
    mine_ups = sorted([u for u in data["upgrades"]
                       if u["sid"].startswith("eurgol.") and u["nation"] == "aus"],
                      key=lambda x: x["sid"])
    add("mine_upgrades", "Mine upgrades count (eurgol.*, aus)", 6, len(mine_ups))
    if len(mine_ups) == 6:
        total_workers = 5 + sum(u.get("value") or 0 for u in mine_ups)
        add("mine_upgrades", "Mine total workers (5 base + 6 upgrades)", 95, total_workers)
        total_food = sum(u.get("food") or 0 for u in mine_ups)
        total_gold = sum(u.get("gold") or 0 for u in mine_ups)
        add("mine_upgrades", "Mine full upgrade total food cost", 104550, total_food)
        add("mine_upgrades", "Mine full upgrade total gold cost", 80950, total_gold)

    # Specific unit existence + uniqueness
    units_by_sid: dict[str, list[dict]] = {}
    for u in data["units"]:
        units_by_sid.setdefault(u["sid"], []).append(u)
    add("units", "Strelet (rus) exists", True, "strelet" in units_by_sid)
    add("units", "Strelet is rus-unique", 1, len(units_by_sid.get("strelet", [])))
    add("units", "Janissary (tur) exists", True, "jannisary" in units_by_sid)
    add("units", "Janissary is tur-unique", 1, len(units_by_sid.get("jannisary", [])))
    add("units", "Vityaz (rus) exists", True, "vityaz" in units_by_sid)
    add("units", "Vityaz is rus-unique", 1, len(units_by_sid.get("vityaz", [])))
    add("units", "Fishboat (any nation) exists", True, "fishboat" in units_by_sid)
    add_op("units", "Fishboat available in nations", ">=", 21,
            len(units_by_sid.get("fishboat", [])))

    # Specific unit stats — values from the per-sid override block in
    # unit.script:931-938 (the inner `case objprop.sid of 'strelet':` branch).
    # Earlier the parser ignored those overrides and read the outer `'musketeerspa',
    # 'musketeeraus','strelet'` branch defaults; numbers below now match the override.
    strelet_rows = [u for u in data["units"] if u["sid"] == "strelet" and u["nation"] == "rus"]
    if strelet_rows:
        s = strelet_rows[0]
        add("units", "Strelet HP", 85, s.get("hp"))
        add("units", "Strelet food cost", 70, s.get("food"))
        if s.get("weapons"):
            w = s["weapons"][0]
            add("units", "Strelet weapon damage", 12, w.get("damage"))
            add("units", "Strelet weapon kind", "bullet", w.get("kind"))
            add("units", "Strelet weapon weaponsid", "SHOTMUSKET", w.get("weaponsid"))
            add("units", "Strelet weapon range_max (tiles)", 13.13, w.get("radiusmax_tiles"))

    # Fishboat fishingmax
    fb_rows = [u for u in data["units"] if u["sid"] == "fishboat"]
    if fb_rows:
        add("units", "Fishboat fishingmax (base)", 1000, fb_rows[0].get("fishingmax"))

    # Pixel-to-tile conversion
    add("conversions", "pixels_to_tile", 53.3333333, data["economy"].get("pixels_to_tile"))

    # Market rate sanity
    food_market = data.get("market_rates", {}).get("food", {})
    add("market", "food buy_default", 25, food_market.get("buycostdef"))
    add("market", "food buy_max", 40, food_market.get("buycostmax"))
    wood_market = data.get("market_rates", {}).get("wood", {})
    add("market", "wood sell_default", 30, wood_market.get("sellcostdef"))

    # Trained_in critical mappings
    def get_trained_in(sid: str, nation: str) -> set[str]:
        for u in data["units"]:
            if u["sid"] == sid and u["nation"] == nation:
                return set(u.get("trained_in", []))
        return set()
    add("trained_in", "Strelet trained at rusbar", True,
        "rusbar" in get_trained_in("strelet", "rus"))
    add("trained_in", "Reiter trained at aussta", True,
        "aussta" in get_trained_in("reiter", "aus"))
    add("trained_in", "Fishboat trained at eurpor", True,
        "eurpor" in get_trained_in("fishboat", "aus"))
    add("trained_in", "peaaus trained at auscen", True,
        "auscen" in get_trained_in("peaaus", "aus"))

    return checks


def _find_upgrade_cost(upgrade_rows: list[dict], sid: str) -> tuple[int | None, int | None]:
    for u in upgrade_rows:
        if u["sid"] == sid:
            return u.get("wood"), u.get("gold")
    return None, None


def collect_gaps(parsed_units: dict, nation_data: dict) -> list[dict]:
    gaps = []
    # Unparsed unit sids referenced in nations but not in parsed_units
    all_referenced = set()
    for nat, info in nation_data.items():
        for sid in info["members"]:
            all_referenced.add(sid)
    parsed_unit_sids = set(parsed_units["units"].keys())
    parsed_building_suffixes = set(parsed_units["common_buildings"].keys()) | set(parsed_units["nation_buildings"].keys())
    # Compute unmatched
    missing_units = []
    for sid in sorted(all_referenced):
        if sid in parsed_unit_sids:
            continue
        # Maybe it's a building?
        is_per_nation_building = any(sid.endswith(s) and sid[:-3] in PLAYABLE_NATIONS for s in PER_NATION_BUILDING_SUFFIXES)
        is_common_building = any(sid.endswith(s) and sid[:-3] in {"eur","rus","tur","spa","ukr","por"} for s in COMMON_BUILDING_SUFFIXES)
        if is_per_nation_building or is_common_building:
            continue
        # Maybe mission/null/special
        if sid in ("null", "field", "unitbox") or sid.startswith("mis"):
            continue
        missing_units.append(sid)
    gaps.append({
        "gap": "Unit sids referenced in nation rosters but not extracted from unit.script",
        "count": len(missing_units),
        "sample": missing_units[:30],
    })
    # New gap categorization after the simulator was added
    gaps.append({
        "gap": "Per-unit blacksmith/stable/barracks upgrades (resolved)",
        "count": 0,
        "sample": [],
    })
    return gaps


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    data = assemble()
    # Convert sets to lists for JSON serialization
    def default(o):
        if isinstance(o, set):
            return sorted(o)
        return str(o)
    out_path = DATA_JSON
    out_path.write_text(json.dumps(data, default=default, ensure_ascii=False, indent=2),
                         encoding="utf-8")
    print(f"\nWrote {out_path} ({out_path.stat().st_size:,} bytes)")
    print(f"  nations:   {len(data['nations'])}")
    print(f"  buildings: {len(data['buildings'])}  (rows; sid×nation)")
    print(f"  units:     {len(data['units'])}  (rows; sid×nation)")
    print(f"  upgrades:  {len(data['upgrades'])}  (rows; sid×nation)")
    print(f"  gaps:")
    for g in data["gaps"]:
        print(f"    - {g['gap']}: {g['count']} (sample={g['sample'][:8]})")
    print()
    print("Discrepancies (file vs prompt notes):")
    for d in data["discrepancies"]:
        print(f"  - {d['fact']}: user_note={d['user_note']} file={d['file_value']}")
    print()
    sanity = data["sanity_checks"]
    n_pass = sum(1 for c in sanity if c["pass"])
    n_fail = len(sanity) - n_pass
    print(f"Sanity checks: {n_pass}/{len(sanity)} passed, {n_fail} FAILED")
    if n_fail:
        print("FAILED:")
        for c in sanity:
            if not c["pass"]:
                print(f"  ! [{c['category']}] {c['name']}: expected {c['expected']!r}, "
                      f"got {c['actual']!r}")


if __name__ == "__main__":
    main()
