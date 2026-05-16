"""Convert a replay (.rep) into a build_order JSON the editor simulator
understands. Extracts the named player's actions in the first `window_g_sec`
seconds: builds, trains (finite + ∞), upgrades, market trades. Does NOT
extract peasant-assign moves — those are inferred from ReadOrder events
which the parser doesn't surface as economy-typed actions yet, so the user
adds assigns manually in the editor.
"""
from __future__ import annotations

import json
from pathlib import Path

from parse_replay_events import (
    parse_replay_from_bytes, _resolve_upgrade, NATION_BY_CID,
)

RES_BY_IND = {1: "food", 2: "wood", 3: "stone", 4: "gold", 5: "iron", 6: "coal"}
DEFAULT_WINDOW_G_SEC = 900.0  # 15 game-minutes

# Default peasant sid per nation — used as `starting_units` key.
# Mirrors editor/js/ui/i18n.js DEFAULT_PEASANT.
PEASANT_BY_NATION = {
    "aus": "peaaus", "fra": "peaeng", "eng": "peaeng", "spa": "peaspa",
    "rus": "pearus", "ukr": "peaukr", "pol": "peapol", "swe": "peaeng",
    "pru": "peaaus", "ven": "peaspa", "tur": "peatur", "alg": "peatur",
    "net": "peaeng", "den": "peaeng", "por": "peaspa", "pie": "peaspa",
    "sax": "peaaus", "bav": "peaaus", "hun": "peapol", "swi": "peaaus",
    "sco": "peasco",
}


MINE_SUFFIXES = ("gol", "iro", "coa")
MINE_SUFFIX_TO_RES = {"gol": "gold", "iro": "iron", "coa": "coal"}


def replay_to_build_order(
    replay_bytes: bytes,
    data_json: dict,
    *,
    pid: int | None = None,
    window_g_sec: float = DEFAULT_WINDOW_G_SEC,
) -> dict:
    """Parse `replay_bytes` and return a build_order dict for `pid`.
    If `pid` is None, picks the *host* — player with most ReadOrder events
    (or falls back to most-builds if no one has ReadOrder)."""
    result = parse_replay_from_bytes(replay_bytes)

    orders_count = {p: sum(v.values()) for p, v in result.get("orders_per_pid", {}).items()}
    if pid is None:
        if orders_count and max(orders_count.values()) > 0:
            pid = max(orders_count, key=lambda p: orders_count[p])
        else:
            pid = max(result["builds_per_pid"].keys(),
                      key=lambda p: len(result["builds_per_pid"][p]))

    # Infer player's nation from the first ReadConstruct sid prefix
    builds = result["builds_per_pid"].get(pid, [])
    if not builds:
        raise ValueError(f"Player pid={pid} has no build actions in replay")
    nation = builds[0]["sid"][:3]
    cid = next((c for c, n in NATION_BY_CID.items() if n == nation), 0)
    is_host = orders_count.get(pid, 0) > 0

    # Build unit_sid → producer-building lookup from data.json
    unit_to_bld: dict[str, str] = {}
    for u in data_json.get("units", []):
        if u.get("nation") == nation and u.get("trained_in"):
            unit_to_bld[u["sid"]] = u["trained_in"][0]

    actions: list[dict] = []

    # — Builds —
    for b in builds:
        if b["ts_g_sec"] > window_g_sec:
            break
        sid = b["sid"]
        # Skip wall/gate slivers — they aren't single-clickable entities in the
        # editor catalog.
        if sid.startswith(("ukrwga", "ukrwwa")):
            continue
        actions.append({
            "at": round(b["ts_g_sec"], 1),
            "do": "build",
            "sid": sid,
            "builders": int(b.get("builders") or 1),
        })

    # — Trains (finite coalesced, ∞ separate) —
    prev_train: dict | None = None
    for p in result.get("produces_per_pid", {}).get(pid, []):
        if p["ts_g_sec"] > window_g_sec:
            break
        unit = p.get("unit_sid")
        if not unit or not p.get("start"):
            continue
        bld = unit_to_bld.get(unit)
        if not bld:
            continue
        at = round(p["ts_g_sec"], 1)
        if p["infinite"]:
            actions.append({
                "at": at, "do": "train_infinite",
                "building_sid": bld, "unit_sid": unit,
            })
            prev_train = None
        else:
            amount = int(p.get("amount") or 1)
            # Coalesce identical orders within 5 g-sec into one train action.
            if (prev_train is not None
                    and prev_train["unit_sid"] == unit
                    and prev_train["building_sid"] == bld
                    and at - prev_train["at"] < 5):
                prev_train["amount"] += amount
            else:
                prev_train = {
                    "at": at, "do": "train",
                    "building_sid": bld, "unit_sid": unit, "amount": amount,
                }
                actions.append(prev_train)

    # — Trades —
    for tr in result.get("trades_per_pid", {}).get(pid, []):
        if tr["ts_g_sec"] > window_g_sec:
            break
        sell = RES_BY_IND.get(tr.get("sell"))
        buy = RES_BY_IND.get(tr.get("buy"))
        if not sell or not buy:
            continue
        actions.append({
            "at": round(tr["ts_g_sec"], 1), "do": "trade",
            "sell": sell, "buy": buy, "amount": int(tr.get("amount") or 0),
        })

    # — Research —
    for u in result.get("upgrades_per_pid", {}).get(pid, []):
        if u["ts_g_sec"] > window_g_sec:
            break
        if not u.get("start"):
            continue
        upg = _resolve_upgrade(cid, u["upgrade_id"])
        if not upg or "+" in upg["sid"]:
            continue
        actions.append({
            "at": round(u["ts_g_sec"], 1), "do": "research",
            "upgrade_sid": upg["sid"],
        })

    # — Assigns (host only) —
    # gainres orders target tree/stone/food nodes — without map data we can't
    # tell the resource type from target_uid. Heuristic: split by game phase.
    # gotomine orders target mine buildings — we pick the most-recently-built
    # mine of the player (any type if multiple) as the destination.
    if is_host:
        actions.extend(_extract_assigns(
            result.get("orders_timed_per_pid", {}).get(pid, []),
            builds,
            window_g_sec,
        ))

    actions.sort(key=lambda a: (a["at"], 0 if a["do"] == "assign" else 1))

    settings = result.get("settings", {})
    starting_pea_sid = PEASANT_BY_NATION.get(nation, "peaaus")

    # Default to "standard" 1000-each resources unless replay carries an explicit
    # resourcestart preset (not always in settings).
    starting_resources = {r: 1000 for r in ("food", "wood", "stone", "gold", "iron", "coal")}

    # gamespeed enum 0=slow, 1=normal, 2=fast in the replay settings
    speed_str = {0: "slow", 1: "normal", 2: "fast"}.get(settings.get("gamespeed", 2), "fast")

    player_meta = next((p for p in result.get("players", []) if p.get("pid") == pid), {})
    player_name = player_meta.get("name", f"pid={pid}")

    host_tag = "хост — assigns извлечены" if is_host else "клиент — assigns НЕ извлекаются"
    return {
        "nation": nation,
        "game_speed": speed_str,
        "starting_resources": starting_resources,
        "starting_units": {starting_pea_sid: 18},
        "starting_buildings": {nation + "cen": 1},
        "max_time_sec": int(window_g_sec),
        "map_settings": {k: settings[k] for k in
                         ("mapsize", "terraintype", "relieftype",
                          "resourcemines", "season", "gamespeed")
                         if k in settings},
        "actions": actions,
        "_note": (f"Импорт из реплея (игрок: {player_name}, pid={pid}, {host_tag}, "
                  f"первые {int(window_g_sec)} г-сек). "
                  "Извлечены точно: build, train (finite+∞), trade, research. "
                  + ("Assigns эвристически: gainres → дерево/еда/камень по фазе игры (mill/sto), "
                     "gotomine → ближайшая по времени построенная шахта игрока. Проверь, поправь если что."
                     if is_host else
                     "У клиента в реплее нет ReadOrder-эвентов (всё уходит в state-sync, который мы не "
                     "декодируем), поэтому крестьян раскидываешь вручную через каталог.")),
    }


def _extract_assigns(orders_timed: list[dict],
                     builds: list[dict],
                     window_g_sec: float) -> list[dict]:
    """Turn raw gainres/gotomine ReadOrder events into cumulative assign
    actions. Heuristics:
      - gainres before any mill is built  → wood (lumber stage)
      - gainres after mill, before storehouse  → wood + food (split 50/50)
      - gainres after storehouse  → food (mill+sto = pop+farming opener done)
      - gainres after stone walls/towers built → adds stone
      - gotomine → assign to the player's most-recently-built mine of any type
    These are rough buckets — meant to make the simulation not starve. The
    user adjusts in the editor.
    """
    # Index builds by time for phase lookups
    builds_sorted = sorted(builds, key=lambda b: b["ts_g_sec"])

    def first_built_t(suffix: str) -> float | None:
        """Earliest ts at which a building with `suffix` was ORDERED. Note:
        we use order time as an approximation (real completion is later, but
        the player issues gather orders after they SEE the build placed)."""
        for b in builds_sorted:
            sid = b["sid"]
            if sid.endswith(suffix):
                return b["ts_g_sec"]
        return None

    mill_t  = first_built_t("mil")
    sto_t   = first_built_t("sto")
    tow_t   = first_built_t("tow")
    swa_t   = first_built_t("swa")  # stone wall

    # Track cumulative N peasants assigned to each resource over time.
    # Each gainres / gotomine event adds N peasants to ONE resource; we
    # accumulate so each assign action reflects the player's *current*
    # gathering layout (assigns in C3 are SET, not ADD).
    cumulative: dict[str, int] = {"food": 0, "wood": 0, "stone": 0}
    cumulative_mine: dict[str, int] = {}  # mine_sid → N peasants

    def pick_gainres_res(ts: float) -> str:
        """Cheap phase classifier — see docstring."""
        if (swa_t is not None and ts >= swa_t) or (tow_t is not None and ts >= tow_t):
            # Stone walls or towers ordered — at least some peasants go to stone.
            # Slightly biased: keep wood/food going, add stone every 3rd order.
            return "stone"
        if sto_t is not None and ts >= sto_t:
            return "food"  # storehouse ordered → can drop food off
        if mill_t is not None and ts >= mill_t:
            # Even split: alternate by parity of how many events we've seen
            return "wood"
        return "wood"

    # Most-recently-built mine before time T
    def latest_mine_sid_before(t: float) -> str | None:
        latest = None
        for b in builds_sorted:
            if b["ts_g_sec"] > t:
                break
            sid = b["sid"]
            if any(sid.endswith(s) for s in MINE_SUFFIXES):
                latest = sid
        return latest

    out: list[dict] = []
    for ev in orders_timed:
        if ev["ts_g_sec"] > window_g_sec:
            break
        n = ev.get("n_units") or 0
        if n <= 0:
            continue
        ot = ev["ordtyp"]
        if ot == 3:  # gainres
            res = pick_gainres_res(ev["ts_g_sec"])
            cumulative[res] = max(cumulative.get(res, 0), n)
        elif ot == 13:  # gotomine
            mine_sid = latest_mine_sid_before(ev["ts_g_sec"])
            if not mine_sid:
                continue
            cumulative_mine[mine_sid] = max(cumulative_mine.get(mine_sid, 0), n)
        else:
            continue  # ignore fishing/build/repair for now

        # Emit a snapshot of current gathering layout.
        snap = {"at": round(ev["ts_g_sec"], 1), "do": "assign"}
        snap.update({k: v for k, v in cumulative.items() if v > 0})
        snap.update(cumulative_mine)
        out.append(snap)

    # Deduplicate consecutive identical assigns
    out2: list[dict] = []
    for a in out:
        if out2 and {k: v for k, v in a.items() if k not in ("at",)} == \
                    {k: v for k, v in out2[-1].items() if k not in ("at",)}:
            continue
        out2.append(a)
    return out2


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) < 2:
        print("Usage: python replay_to_build_order.py <replay.rep> [pid] [window_g_sec]")
        sys.exit(1)
    rep_path = Path(sys.argv[1])
    data_path = Path(__file__).resolve().parent.parent / "data.json"
    data = json.loads(data_path.read_text(encoding="utf-8"))
    pid_arg = int(sys.argv[2]) if len(sys.argv) > 2 else None
    window = float(sys.argv[3]) if len(sys.argv) > 3 else DEFAULT_WINDOW_G_SEC
    bo = replay_to_build_order(rep_path.read_bytes(), data, pid=pid_arg, window_g_sec=window)
    print(json.dumps(bo, ensure_ascii=False, indent=2))
