"""Cossacks 3 economy timeline simulator.

Reads `output/tech_tree.json` + `output/cossacks3_data.json`, takes a build
order JSON file, simulates game-time tick-by-tick, and outputs:
- CSV timeline (resources / population / buildings / units / upgrades over time)
- Markdown report with key milestones

Usage:
    python simulate_economy.py <build_order.json> [--output-prefix=<name>]

Build order JSON schema (`tests/build_order_*.json`):
    {
      "nation": "bav",
      "game_speed": "fast",      # slow|normal|fast (default fast)
      "map_config": {"walk_overhead": 0.30},  # 0..1, fraction of time wasted walking
      "starting_resources": {"food": 1000, "wood": 1000, "stone": 1000,
                              "gold": 1000, "iron": 0, "coal": 0},
      "starting_units": {"peaaus": 5},
      "starting_buildings": {"bavcen": 1},
      "max_time_sec": 600,        # game-time, not real-time
      "actions": [
        {"at": 0,  "do": "assign", "food": 3, "wood": 2},
        {"at": 30, "do": "build",  "sid": "bavhou", "builders": 2},
        {"at": 60, "do": "train",  "building_sid": "bavcen", "unit_sid": "peaaus", "amount": 5},
        {"at": 120, "do": "research", "upgrade_sid": "bavmil.1"}
      ]
    }

Mechanics modeled (simplified — see assumptions in §END):
- peasant idle/assigned to resource types: food/wood/stone/gold/iron/coal
- production rate (g-sec):
    * food/wood/stone: portion × eff / (hits × T_hit) × (1 - walk_overhead)
    * gold/iron/coal:  produce(13) × 32 / 250 × (1 - mine_overhead)
- buildings: time = buildtime_sec × 1.13 / N_builders, clamped at the per-building
  slot cap from derived/builder_slots.json (range 19..30).
- units: each building instance has its own queue; with N buildings of same sid →
  N units progress in parallel. Rate per building = 1/unit_buildtime.
- upkeep: per-unit food drain per g-sec = (consume.food + (bnohungry ? 0 : 30)) × 32 / 20000
  (the +30 = gc_obj_foodperunit, added in unit.script:3821 for every non-bnohungry,
   non-building unit; consume.food is the per-unit explicit value from unit.script)
- prereqs: action fails if any required building not built or upgrade not done
- farm cap: total farm = sum of building.farm (cen=100, bar=150, ba2=250, hou=25),
  CLAMPED at map_settings.limit (1..8 → 500..8000) and engine ceiling 32000.
- mine capacity: each mine accepts up to (5 + addpeasantabsorber) peasants inside;
  upgrades gol/iro/coa.1..6 add +5/+8/+10/+12/+15/+40 cumulatively (base→max 95).
- buildtimeperc upgrades: when researched, target sids (extracted via simulate_upgrades.py
  → upgrade.targets) get buildtime *= (1 + value/10_000_000). For value=-2_500_000
  this is -25% buildtime; for -7_500_000 it's -75% (effectively instant). Applied
  inside `advance_unit_production` via `buildtime_modifier(sid)`.
- field cycle (opt-in): if build_order includes `{"do":"plant_fields","count":49}`,
  food collection switches to field-aware mode:
    - Each plant_fields adds N fields in `growing` state (cost: N × 5 gold).
    - Growing → alive after 87.5 g-sec (FIELD_GROW_TIME_SEC); hp = 25000.
    - Alive → dead when hp ≤ 0; rest 21.875 g-sec; reborn → growing.
    - Per-tick auto-regen: alive fields with hp ≥ 13000 (visual_stage_0) get
      +1250 hp every 31.25 g-sec (mid-value of engine random 0..2500).
    - Harvest drains hp: peasants_food × resdec / T_HIT[food] per g-sec, distributed
      across alive fields. resdec = max(1, floor(100/(1+fieldlife/100))).
    - With fieldlife=0: 1 peasant on 1 field = -65 hp/g-sec (dies in ~6.5 min).
    - With fieldlife=300 (full upgrades): +44 hp/g-sec (field never dies).
    - Cap of 3 attackers/field (gc_gameplay_resource_maxattackers_food).
  Without plant_fields, food production is "infinite per peasant" (legacy).

What's NOT modeled (yet):
- Walking distances explicitly (uses static walk_overhead instead)
- Individual peasant fatigue / pathing
- Stone exhaustion (assumed infinite — stone HP=10M, effectively true)
- Production cancel (we just ignore failed/incomplete actions)
- Multiple barracks producing different units in parallel (modeled correctly!
  but action "train" assigns to ONE specific building_sid; user must build N barracks
  and queue N times)
- Tree depletion: wood pool is INFINITE through stumps anyway, so this is fine
- priceperc upgrades: target sids extracted but per-resource percentages stay
  in unparsed direct sarrparam2 assignments (parser gap; price_modifier returns 1.0)
"""
from __future__ import annotations
import csv
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "parser"))
from config import (OUTPUT_DIR, DATA_JSON, DERIVED_DIR,
                    ANIM_FRAMES_PER_GAMESEC, PEASANT_ANIM_SEC,
                    WALK_OVERHEAD_GUESS, MINE_OVERHEAD_GUESS,
                    GC_MAX_OBJ_COUNT, MAP_SETTINGS_LIMIT,
                    MINE_BASE_PEASANTABSORBER,
                    FIELD_MAX_HP, FIELD_GROW_TIME_SEC, FIELD_REST_TIME_SEC,
                    FIELD_REGEN_INTERVAL_SEC, FIELD_REGEN_PER_TICK_MAX,
                    FIELDS_PER_MILL, FIELD_GOLD_COST)
DATA_PATH = DATA_JSON
TREE_PATH = DERIVED_DIR / "tech_tree.json"
BUILDER_SLOTS_JSON = DERIVED_DIR / "builder_slots.json"

# ---------- Game constants ----------
GAMESPEED = {"slow": 0.7, "normal": 1.0, "fast": 1.4}
GC_TIME_TO_FRAMES = ANIM_FRAMES_PER_GAMESEC  # 32
# dmscript.global:808 — additive food upkeep contributed by every non-bnohungry,
# non-building unit (added to player's resconsume[food] in unit.script:3821).
GC_OBJ_FOODPERUNIT = 30

# Peasant work-cycle hits per resource (from country.script harvest formulas)
PORTION = {"food": 45, "wood": 28, "stone": 40}
HITS = {"food": 22, "wood": 14, "stone": 20}
# Time per hit = animation cycle length, from data/animations/aaf/peaaus.aaf
T_HIT = {"food":  PEASANT_ANIM_SEC["workfood"],
         "wood":  PEASANT_ANIM_SEC["workwood"],
         "stone": PEASANT_ANIM_SEC["workstone"]}

# Mine produce rate per peasant per g-sec — derived from gc_economy_time = 0.0001×32 = 0.0032 g-sec/tick,
# 250-tick mining cycle yielding 13 resource per peasant: 13 / (250 × 0.0032) = 16.25? No — see resource.script.
# Actual formula: rate = produce_per_cycle × gc_time_to_frames / cycle_frames = 13 × 32 / 250.
MINE_RATE_PER_PEASANT = 13 * 32 / 250  # 1.664 res/g-sec/peasant
MINE_TYPES = ("gold", "iron", "coal")

# ---------- Market economy (gEconomy[restype], shared across players) -------
# Defaults from `res.script:_res_InitEconomy`. See docs/reference/06_market.
MARKET_DEFAULTS = {
    # res:    (buy_min, buy_def, buy_max, sell_min, sell_def, sell_max)
    "food":  (20,  25.00,  40,  10.64, 15.20, 19.76),
    "wood":  (40,  50.00,  60,  20.00, 30.00, 40.00),
    "stone": (40,  50.00,  60,  15.68, 20.90, 26.13),
    "gold":  (140, 190.00, 240, 80.00, 110.00, 140.00),
    "iron":  (100, 140.00, 180, 40.00, 60.00, 80.00),
    "coal":  (100, 140.00, 180, 40.00, 60.00, 80.00),
}
GC_ECONOMY_EXP = 0.00002       # weight scaler per traded unit
ECONOMY_REVERT_PER_GSEC = 0.025  # default returns ~2.5% per g-sec toward def

# Real per-building builder slot cap, from compute/compute_builder_slots.py
# (faithful sim of `_unit_CalcBuilderPoints` in unit.script:8702-9006).
def _load_builder_slots() -> dict[str, int]:
    if not BUILDER_SLOTS_JSON.exists():
        return {}
    raw = json.loads(BUILDER_SLOTS_JSON.read_text(encoding="utf-8"))
    return {sid: info["slots"] for sid, info in raw.items()}

BUILDER_SLOTS: dict[str, int] = _load_builder_slots()
GC_MAX_BUILDER_COUNT = 30  # engine ceiling, gc_MaxBuilderCount


def slot_cap_for(sid: str) -> int:
    """Builder slot cap for a building. Prefers the per-sid simulation,
    falls back to engine ceiling if sid is missing (rare; logs nothing
    so callers can detect by comparing against the ceiling)."""
    if sid in BUILDER_SLOTS:
        return BUILDER_SLOTS[sid]
    return GC_MAX_BUILDER_COUNT


def load_data():
    return (json.loads(DATA_PATH.read_text(encoding="utf-8")),
            json.loads(TREE_PATH.read_text(encoding="utf-8")))


# ---------- Simulator state ----------

PLACE_SUFFIXES = ("aca", "ba2", "bar", "bla", "sta", "mil", "art", "tem",
                   "cen", "dip", "tow", "swa", "wwa", "por", "hou",
                   "gol", "iro", "coa")
SHARED_PLACES = {"tow", "swa", "wwa", "por"}  # cluster-prefixed
MINE_PLACES = {"gol", "iro", "coa"}            # always eur*

def upgrade_place_building(upg_sid: str, nation: str, cluster: str) -> str | None:
    """Derive the building sid where this upgrade is researched, e.g.
    `bavbla.1` → `bavbla`, `eurgol.3` → `eurgol`, `eurtow.2` → `<cluster>tow`.
    Returns None if the suffix doesn't match any known place."""
    stem = upg_sid.split(".")[0]
    for p in (nation, cluster, "eur", "rus", "tur", "spa", "ukr", "por"):
        if not p or not stem.startswith(p):
            continue
        rest = stem[len(p):]
        if rest in PLACE_SUFFIXES:
            if rest in MINE_PLACES:
                return "eur" + rest
            if rest in SHARED_PLACES:
                return cluster + rest
            return nation + rest
    return None


class SimState:
    def __init__(self, nation: str, build_order: dict, data: dict, tree: dict):
        self.nation = nation
        self.data = data
        self.tree = tree
        self.nat_tree = tree["nations"][nation]
        # Cluster (eur/rus/ukr/tur) — common-buildings prefix per country.script.
        # data.json doesn't surface this field per-nation; mirror parser/config.py's
        # _commonname mapping here.
        if nation in ("rus", "ukr"):
            self.cluster = "rus"
        elif nation in ("tur", "alg"):
            self.cluster = "tur"
        else:
            self.cluster = "eur"
        self.bldgs_idx = {b["sid"]: b for b in data["buildings"] if b["nation"] == nation}
        self.units_idx = {u["sid"]: u for u in data["units"] if u["nation"] == nation}
        self.upg_idx = {u["sid"]: u for u in data["upgrades"] if u["nation"] == nation}

        self.t_g = 0.0  # current game-time in seconds
        self.dt = 1.0   # tick step in g-sec

        self.resources = dict(food=0, wood=0, stone=0, gold=0, iron=0, coal=0)
        self.resources.update(build_order.get("starting_resources", {}))

        self.buildings = defaultdict(int)  # sid -> count
        for sid, n in (build_order.get("starting_buildings") or {}).items():
            self.buildings[sid] += n

        self.units = defaultdict(int)  # sid -> count
        for sid, n in (build_order.get("starting_units") or {}).items():
            self.units[sid] += n

        self.upgrades_done: set[str] = set()

        # Construction in progress: list of (sid, finish_time_g, builders)
        self.construction = []
        # Unit production queues per building instance — simplified to per building_sid:
        # {sid: list of (unit_sid, progress)} where each entry is one queued unit
        self.unit_queues: dict[str, list[tuple[str, float]]] = defaultdict(list)
        # Upgrade research: list of (upgrade_sid, finish_time_g)
        self.upgrades_in_progress = []

        # Active "infinite train" orders. Each entry:
        #   {"building_sid": str, "unit_sid": str, "start_t": float}
        # Sim tops up the unit_queues so production never stops while orders
        # are active and resources hold out.
        self.infinite_orders: list[dict] = []

        # Market rates — shared across players, mutated by trade actions and
        # drifted back toward defaults every tick.
        self.market = {
            res: {
                "buy_min": vals[0], "buy": vals[1], "buy_max": vals[2],
                "sell_min": vals[3], "sell": vals[4], "sell_max": vals[5],
                "buy_def": vals[1], "sell_def": vals[4],
            }
            for res, vals in MARKET_DEFAULTS.items()
        }

        # Peasant assignments: {resource_type: count}
        self.assigned = defaultdict(int)
        # Resource type → set of mine sids the peasants are inside (optional refinement)
        self.mine_assignments: dict[str, int] = defaultdict(int)  # mine_sid -> peasants inside

        # Walking overhead (0..1) — empirical guess, see config.WALK_OVERHEAD_GUESS / MINE_OVERHEAD_GUESS.
        # Override per-run via build_order.map_config.{walk_overhead, mine_overhead, limit}.
        # `limit` (0..8) selects map-wide pop cap from gc_mapsettings_limit_*.
        self.build_order_map_config = build_order.get("map_config")
        self.walk_overhead = (self.build_order_map_config or {}).get("walk_overhead", WALK_OVERHEAD_GUESS)
        self.mine_overhead = (self.build_order_map_config or {}).get("mine_overhead", MINE_OVERHEAD_GUESS)

        # Efficiency per resource type (default 100, +upgrades)
        self.eff = {"food": 100, "wood": 100, "stone": 100, "gold": 100, "iron": 100, "coal": 100}
        # Field life (default 0). Drives resdec = max(1, floor(100/(1+fieldlife/100)))
        self.fieldlife = 0
        # Field cycle tracking. Each field is dict {state, hp, transition_time}.
        # state in {"growing", "alive", "dead"}.
        # If no fields planted (default), food rate falls back to "infinite per
        # peasant" model — preserves old build orders that don't model fields.
        self.fields: list[dict] = []
        # Last regen tick time (used for stage_0 +HP every FIELD_REGEN_INTERVAL_SEC).
        self.next_field_regen_t = FIELD_REGEN_INTERVAL_SEC

        # Deep-copy each action so deferral (mutating `at`) doesn't leak back
        # into the caller's build_order dict (the editor reuses it after sim).
        self.actions = sorted(
            ({**a} for a in build_order.get("actions", [])),
            key=lambda a: a["at"],
        )
        self.action_idx = 0

        self.events: list[str] = []  # log of milestones / errors
        self.snapshots: list[dict] = []
        self.snapshot_interval = 5.0  # snapshot every 5 g-sec

        # Game speed factor (only matters for converting g-sec ↔ real-sec at the end)
        self.gamespeed_name = build_order.get("game_speed", "fast")
        self.gamespeed_factor = GAMESPEED[self.gamespeed_name]
        self.max_time_g = build_order.get("max_time_sec", 600)

    # --- helpers ---

    def building_count(self, sid: str) -> int:
        return self.buildings[sid]

    def has_prereq(self, prereq: dict) -> bool:
        """Check if a prereq (kind/sid) is satisfied."""
        kind, sid = prereq["kind"], prereq["sid"]
        if kind == "building":
            return self.buildings[sid] > 0
        if kind == "unit":
            return self.units[sid] > 0
        if kind == "upgrade":
            return sid in self.upgrades_done
        return False

    def all_prereqs_met(self, prereqs: list[dict]) -> tuple[bool, list[dict]]:
        missing = [p for p in prereqs if not self.has_prereq(p)]
        return len(missing) == 0, missing

    def can_pay(self, cost: dict) -> bool:
        return all(self.resources.get(k, 0) >= v for k, v in cost.items() if v)

    def pay(self, cost: dict):
        for k, v in cost.items():
            if v:
                self.resources[k] -= v

    def farm_cap(self) -> int:
        """Effective population cap = min(sum of building.farm, map limit, engine ceiling)."""
        farm_sum = 0
        for sid, n in self.buildings.items():
            b = self.bldgs_idx.get(sid)
            if b and b.get("farm"):
                farm_sum += b["farm"] * n
        # Map setting cap (default = no override, falls back to engine ceiling)
        map_limit_idx = (self.build_order_map_config or {}).get("limit", 0)
        map_cap = MAP_SETTINGS_LIMIT.get(map_limit_idx, GC_MAX_OBJ_COUNT)
        return min(farm_sum, map_cap, GC_MAX_OBJ_COUNT)

    def mine_capacity(self, mine_sid: str) -> int:
        """How many peasants this specific mine can hold inside.

        Base = 5 (peasantabsorber). Plus sum of completed mine upgrades for
        the matching resource type (eurgol.1..6 etc.). The simulator currently
        treats upgrades as 'completed' — a real game tracks per-mine
        addpeasantabsorber, but we conservatively assume all built mines have
        all upgrades the player has researched.
        """
        cap = MINE_BASE_PEASANTABSORBER
        # Detect resource via b.produce field
        mine = self.bldgs_idx.get(mine_sid)
        if not mine or not mine.get("produce"):
            return cap
        res = next(iter(mine["produce"]))
        # Find matching upgrades like 'eurgol.1' through '.6' that are done
        # Resource → upgrade place suffix
        suffix = {"gold": "gol", "iron": "iro", "coal": "coa"}.get(res)
        if not suffix:
            return cap
        # Try cluster prefixes
        for prefix in ("eur", "rus", "ukr", "tur"):
            for n in range(1, 7):
                upg_sid = f"{prefix}{suffix}.{n}"
                if upg_sid in self.upgrades_done:
                    upg = next((u for u in self.data["upgrades"] if u["sid"] == upg_sid), None)
                    if upg and upg.get("value"):
                        cap += int(upg["value"])
        return cap

    def farm_used(self) -> int:
        # 1 per non-building unit
        used = 0
        for sid, n in self.units.items():
            u = self.units_idx.get(sid)
            if u and not (u.get("peasantabsorber") or 0):  # peasant counts as 1
                used += n
        return used

    def total_peasants(self) -> int:
        # All units with usage_short=='peasant' or sid starts with 'pea'
        return sum(n for sid, n in self.units.items() if sid.startswith("pea"))

    def idle_peasants(self) -> int:
        return self.total_peasants() - sum(self.assigned.values()) - sum(self.mine_assignments.values())

    # --- prereq ETA (for action deferral) ---

    def _eta_for_prereq(self, prereq: dict) -> float | None:
        """Earliest projected time when this single prereq will be satisfied.

        Returns None if no plan exists (action would have to skip outright).
        Looks at: current state, in-progress construction/research, and future
        actions in the build order.
        """
        kind, sid = prereq["kind"], prereq["sid"]
        if self.has_prereq(prereq):
            return self.t_g
        if kind == "building":
            finishes = [finish for s, finish, _b in self.construction if s == sid]
            if finishes:
                return min(finishes)
            b = self.bldgs_idx.get(sid)
            if not b:
                return None
            base_bt = b.get("buildtime_sec") or 1.0
            cap = slot_cap_for(sid)
            for fut in self.actions[self.action_idx + 1:]:
                if fut.get("do") == "build" and fut.get("sid") == sid:
                    builders = max(1, min(int(fut.get("builders", 1)), cap))
                    bt = base_bt * 1.13 / builders
                    return max(fut["at"], self.t_g) + bt
            return None
        if kind == "upgrade":
            finishes = [finish for s, finish in self.upgrades_in_progress if s == sid]
            if finishes:
                return min(finishes)
            ug = self.upg_idx.get(sid)
            time_sec = (ug.get("time_sec") or 0) if ug else 0
            for fut in self.actions[self.action_idx + 1:]:
                if fut.get("do") == "research" and fut.get("upgrade_sid") == sid:
                    return max(fut["at"], self.t_g) + time_sec
            return None
        # unit prereq: no good ETA (queues don't surface per-unit completion times)
        return None

    def _earliest_satisfaction_time(self, missing: list[dict]) -> float | None:
        eta = self.t_g
        for p in missing:
            e = self._eta_for_prereq(p)
            if e is None:
                return None
            if e > eta:
                eta = e
        # Tiny buffer so the prereq's completion has actually been applied to state
        return eta + max(self.dt, 0.05)

    def _bubble_deferred(self, act: dict, new_at: float) -> None:
        """Mutate `act["at"]` and re-sort the suffix so the action queue stays
        chronological. Does NOT advance action_idx — the slot is now occupied
        by whatever neighbour ended up there."""
        act["at"] = new_at
        i = self.action_idx
        while i + 1 < len(self.actions) and self.actions[i + 1]["at"] < self.actions[i]["at"]:
            self.actions[i], self.actions[i + 1] = self.actions[i + 1], self.actions[i]
            i += 1
        act["defer_count"] = act.get("defer_count", 0) + 1

    # --- core tick ---

    def step(self):
        # 1. Process queued actions whose time has arrived. An action may
        #    return a future timestamp to mean "defer me until that time".
        safety = 0
        while self.action_idx < len(self.actions) and self.actions[self.action_idx]["at"] <= self.t_g:
            act = self.actions[self.action_idx]
            defer_to = self.execute_action(act)
            if defer_to is not None and defer_to > self.t_g and act.get("defer_count", 0) < 20:
                self._bubble_deferred(act, defer_to)
            else:
                self.action_idx += 1
            safety += 1
            if safety > 1000:
                self.events.append(f"t={self.t_g:6.1f}g: SAFETY-BREAK in action loop")
                break

        # 2. Field state transitions (growing → alive → dead → reborn)
        self.advance_fields(self.dt)

        # 3. Income from peasants
        self.collect_income(self.dt)

        # 4. Upkeep (food/gold/iron/coal/etc.)
        self.consume_upkeep(self.dt)

        # 5. Construction progress
        self.advance_construction()

        # 6. Refill unit queues for active infinite-orders, then advance.
        self.maintain_infinite_orders()
        self.advance_unit_production(self.dt)

        # 7. Upgrade research progress
        self.advance_upgrades()

        # 7b. Market rates drift back toward defaults (~2.5% / g-sec)
        self.advance_market(self.dt)

        # 8. Snapshot
        if self.t_g % self.snapshot_interval == 0 or abs(self.t_g - self.max_time_g) < self.dt:
            self.snapshot()

        self.t_g += self.dt

    # --- field cycle ---

    def alive_field_count(self) -> int:
        return sum(1 for f in self.fields if f["state"] == "alive")

    def field_resdec(self) -> int:
        """HP cost per peasant work-cycle. fieldlife=0 → 100, fieldlife=300 → 25."""
        return max(1, math.floor(100 / (1 + self.fieldlife / 100)))

    def advance_fields(self, dt: float):
        """Tick field state machine. Called once per sim tick BEFORE income.

        Transitions:
          growing → alive  (after FIELD_GROW_TIME_SEC; hp = FIELD_MAX_HP)
          dead    → growing (after FIELD_REST_TIME_SEC; hp = 0)
          alive (regen): if hp >= 13000 (visual_stage_0) and t past next_regen_t,
                         add up to FIELD_REGEN_PER_TICK_MAX hp (deterministic 0.5 *
                         max for sim — engine uses random*0.1*MaxHP).

        Income/harvest itself is computed in collect_income; this only handles
        TIME-based transitions and regen ticks.
        """
        if not self.fields:
            return
        for f in self.fields:
            if f["state"] == "growing" and self.t_g >= f["transition_time"]:
                f["state"] = "alive"
                f["hp"] = FIELD_MAX_HP
            elif f["state"] == "dead" and self.t_g >= f["transition_time"]:
                f["state"] = "growing"
                f["hp"] = 0
                f["transition_time"] = self.t_g + FIELD_GROW_TIME_SEC
        # Regen tick — fires every FIELD_REGEN_INTERVAL_SEC g-sec
        if self.t_g >= self.next_field_regen_t:
            # Use mid-value (1250 HP) for deterministic sim — engine uses random×2500
            regen_amount = FIELD_REGEN_PER_TICK_MAX // 2
            for f in self.fields:
                if f["state"] == "alive" and f["hp"] >= 13000:
                    f["hp"] = min(FIELD_MAX_HP, f["hp"] + regen_amount)
            self.next_field_regen_t += FIELD_REGEN_INTERVAL_SEC

    def collect_income(self, dt: float):
        # Above-ground: food/wood/stone
        for res in ("food", "wood", "stone"):
            n = self.assigned.get(res, 0)
            if n == 0:
                continue
            # Field-aware food: if fields are tracked, peasants need ALIVE fields.
            # Each alive field accepts up to 3 attackers (gc_gameplay_resource_maxattackers_food).
            # Drain field hp by resdec/T_HIT per peasant per g-sec; dead fields get
            # transitioned to "dead" state for FIELD_REST_TIME_SEC then reborn.
            if res == "food" and self.fields:
                alive = [f for f in self.fields if f["state"] == "alive"]
                if not alive:
                    continue  # no alive fields → no food production
                # Cap effective peasants by 3 × alive fields
                n_eff = min(n, len(alive) * 3)
                rate_per_p = (PORTION[res] * self.eff[res] / 100) / (HITS[res] * T_HIT[res])
                rate_per_p *= (1 - self.walk_overhead)
                food_added = n_eff * rate_per_p * dt
                self.resources[res] += food_added
                # Drain HP: distribute peasants across alive fields evenly
                resdec = self.field_resdec()
                hp_drain_per_peasant_per_gsec = resdec / T_HIT[res]
                total_hp_drain = n_eff * hp_drain_per_peasant_per_gsec * dt
                hp_drain_per_field = total_hp_drain / len(alive)
                for f in alive:
                    f["hp"] -= hp_drain_per_field
                    if f["hp"] <= 0:
                        f["state"] = "dead"
                        f["transition_time"] = self.t_g + FIELD_REST_TIME_SEC
                continue
            # Wood/stone (and food without fields tracked): legacy infinite model
            rate_per_p = (PORTION[res] * self.eff[res] / 100) / (HITS[res] * T_HIT[res])
            rate_per_p *= (1 - self.walk_overhead)
            self.resources[res] += n * rate_per_p * dt
        # Mines: resource type comes from b.produce, not sid suffix
        for mine_sid, n in self.mine_assignments.items():
            if n == 0:
                continue
            mine = self.bldgs_idx.get(mine_sid)
            if not mine or not mine.get("produce"):
                continue
            res = next(iter(mine["produce"]))  # mines produce exactly one resource
            rate_per_p = MINE_RATE_PER_PEASANT * self.eff[res] / 100
            rate_per_p *= (1 - self.mine_overhead)
            self.resources[res] += n * rate_per_p * dt

    def consume_upkeep(self, dt: float):
        """Drain resources for unit upkeep (and tower upkeep through self.buildings).

        Real game formula (player.script:_player_ProcessResourceConsume + unit.script:3810,3821):
          For every unit/building of player, sum its consume[res] into player.resconsume[res]:
            food: consume.food + (gc_obj_foodperunit=30 if not bnohungry and not bbuilding)
            gold/iron/coal/wood/stone: just consume[res]
          Then drain per g-sec = resconsume × gc_time_to_frames / 20000.

        Sanity: 18 idle aus peasants (consume.food=32, bnohungry=False) ≈ 214 food / 120 g-sec
                (verified 2026-04-29). 1 battleship: 15000 gold/tick → 24 gold/g-sec.
        """
        # Aggregate resconsume across all owned units AND buildings (towers etc.)
        resconsume = {res: 0 for res in self.resources}
        for sid, n in self.units.items():
            u = self.units_idx.get(sid)
            if not u or n == 0:
                continue
            consume = u.get("consume") or {}
            if not isinstance(consume, dict):
                continue
            bnohungry = bool(u.get("bnohungry", False))
            bbuilding = False  # units are not buildings
            for res in resconsume:
                v = consume.get(res, 0) or 0
                if not isinstance(v, (int, float)):
                    continue
                resconsume[res] += n * v
            # +gc_obj_foodperunit for non-bnohungry, non-building units
            if not bnohungry and not bbuilding:
                resconsume["food"] += n * GC_OBJ_FOODPERUNIT
        # Buildings can also have consume (e.g. towers: consume.gold=500). They're
        # bbuilding=True so no +foodperunit. Look up each building in data.
        for sid, n in self.buildings.items():
            b = self.bldgs_idx.get(sid)
            if not b or n == 0:
                continue
            consume = b.get("consume") or {}
            if not isinstance(consume, dict):
                continue
            for res in resconsume:
                v = consume.get(res, 0) or 0
                if not isinstance(v, (int, float)):
                    continue
                resconsume[res] += n * v
        # Drain
        for res, total_per_tick_unit in resconsume.items():
            if total_per_tick_unit <= 0:
                continue
            self.resources[res] -= (total_per_tick_unit * GC_TIME_TO_FRAMES / 20000) * dt

    def maintain_infinite_orders(self):
        """Keep unit_queues topped up for active train_infinite orders.

        For each (building_sid, unit_sid) with N infinite orders, ensure the
        queue contains at least min(N, n_buildings) entries of that unit. This
        way each building instance always has work as long as an order targets
        it, and N orders for N buildings produce in parallel."""
        if not self.infinite_orders:
            return
        by_pair: dict[tuple[str, str], int] = defaultdict(int)
        for o in self.infinite_orders:
            if o["start_t"] > self.t_g:
                continue
            by_pair[(o["building_sid"], o["unit_sid"])] += 1
        for (bld_sid, unit_sid), n_orders in by_pair.items():
            n_inst = self.buildings.get(bld_sid, 0)
            if n_inst == 0:
                continue
            target = min(n_orders, n_inst)
            queue = self.unit_queues[bld_sid]
            cur = sum(1 for u, _p in queue if u == unit_sid)
            while cur < target:
                queue.append((unit_sid, 0.0))
                cur += 1

    def advance_construction(self):
        finished = []
        for i, (sid, finish_time, builders) in enumerate(self.construction):
            if self.t_g >= finish_time:
                finished.append(i)
        for i in reversed(finished):
            sid, finish_time, builders = self.construction.pop(i)
            self.buildings[sid] += 1
            # Mine auto-occupy: the peasants who built a mine walk straight in
            # as miners (engine behaviour — `peasantabsorber` slot on the
            # mine building). Capped by mine capacity × instance count.
            if any(sid.endswith(s) for s in ("gol", "iro", "coa")):
                cap_per_mine = self.mine_capacity(sid)
                total_cap = cap_per_mine * self.buildings[sid]
                already_in = self.mine_assignments.get(sid, 0)
                absorbed = max(0, min(builders, total_cap - already_in))
                if absorbed > 0:
                    self.mine_assignments[sid] = already_in + absorbed
                self.events.append(
                    f"t={finish_time:6.1f}g: BUILT {sid} (count={self.buildings[sid]}); "
                    f"{absorbed}/{builders} строителей вошли в шахту"
                )
            else:
                self.events.append(f"t={finish_time:6.1f}g: BUILT {sid} (count={self.buildings[sid]})")

    def advance_unit_production(self, dt: float):
        # For each building producing, each instance produces 1 unit per buildtime g-sec
        for bld_sid, queue in list(self.unit_queues.items()):
            if not queue or self.buildings[bld_sid] == 0:
                continue
            # All instances of this building share progress in our simplified model:
            # each instance independently produces at rate 1/buildtime.
            # We have N instances → up to N units progress in parallel.
            # Simplification: dispatch one (unit_sid, progress) entry per instance.
            n_instances = self.buildings[bld_sid]
            new_queue = []
            produced_this_tick = 0
            # Process up to n_instances first entries in queue
            instance_idx = 0
            for unit_sid, progress in queue:
                if instance_idx >= n_instances:
                    new_queue.append((unit_sid, progress))
                    continue
                u = self.units_idx.get(unit_sid)
                if not u or not u.get("buildtime_sec"):
                    continue
                bt = u["buildtime_sec"] * self.buildtime_modifier(unit_sid)
                # Check farm/cost when starting (progress=0)
                if progress == 0:
                    price_mult = self.price_modifier(unit_sid)
                    cost = {k: math.floor((u.get(k) or 0) * price_mult) for k in self.resources}
                    if not self.can_pay(cost):
                        new_queue.append((unit_sid, 0))  # stalled
                        instance_idx += 1
                        continue
                    if self.farm_used() + 1 > self.farm_cap():
                        new_queue.append((unit_sid, 0))  # farm cap
                        instance_idx += 1
                        continue
                    self.pay(cost)
                progress += dt / bt
                if progress >= 1.0:
                    self.units[unit_sid] += 1
                    produced_this_tick += 1
                    self.events.append(f"t={self.t_g:6.1f}g: TRAIN {unit_sid} (count={self.units[unit_sid]}) at {bld_sid}")
                    # progress wraps; if amount > 1, we'd queue another; here we just don't auto-requeue
                else:
                    new_queue.append((unit_sid, progress))
                instance_idx += 1
            self.unit_queues[bld_sid] = new_queue

    def advance_upgrades(self):
        finished = []
        for i, (upg_sid, finish_time) in enumerate(self.upgrades_in_progress):
            if self.t_g >= finish_time:
                finished.append(i)
        for i in reversed(finished):
            upg_sid, finish_time = self.upgrades_in_progress.pop(i)
            self.upgrades_done.add(upg_sid)
            self.events.append(f"t={finish_time:6.1f}g: RESEARCHED {upg_sid}")
            # Apply effect. Many upgrade types target specific units/buildings via
            # sarrparam2 (kept in upgrades_done set; consumers like slot_cap_for /
            # mine_capacity / get_modified_buildtime / get_modified_cost look it up).
            ug = self.upg_idx.get(upg_sid)
            if ug:
                v = ug.get("value") or 0
                itype = ug.get("itype") or ""
                if itype in ("gc_upg_type_effectfood", "gc_upg_type_effectfoodperc"):
                    self.eff["food"] += v
                elif itype in ("gc_upg_type_effectwood", "gc_upg_type_effectwoodperc"):
                    self.eff["wood"] += v
                elif itype in ("gc_upg_type_effectstone", "gc_upg_type_effectstoneperc"):
                    self.eff["stone"] += v
                elif itype == "gc_upg_type_fieldlifeperc":
                    self.fieldlife += v
                # buildtimeperc, priceperc, single_inside_mine, single_inside,
                # enableunit, lifeperc, damageperc, etc. — applied lazily by the
                # consumers that need them (see buildtime_modifier / price_modifier
                # below). Adding them eagerly here is wrong since they often target
                # specific sids via sarrparam2.

    def buildtime_modifier(self, sid: str) -> float:
        """Multiplier on buildtime for `sid`. Engine math (player.script:1848):
            buildtime *= (1 + value / (100 * 100000)) = (1 + value / 10_000_000)
        applied per upgrade. Order-independent because multiplication commutes —
        see docs/reference/05_upgrades/README.md «Математика применения». Typical
        values: -7500000 = -75% per upgrade. Clamp to 0.05 to avoid zero/negative.
        """
        factor = 1.0
        for done_sid in self.upgrades_done:
            ug = self.upg_idx.get(done_sid)
            if not ug or (ug.get("itype") or "") != "gc_upg_type_buildtimeperc":
                continue
            if sid not in (ug.get("targets") or []):
                continue
            v = ug.get("value")
            if v is not None:
                factor *= 1.0 + float(v) / 10_000_000.0
        return max(0.05, factor)

    # --- market ---

    def market_building_sid(self) -> str:
        # Market is sister-clustered: spa/por share "spamar"; everyone else
        # uses their common cluster (eur/rus/tur).
        if self.nation in ("spa", "por"):
            return "spamar"
        return self.cluster + "mar"

    def advance_market(self, dt: float):
        """Drift buy/sell rates toward their `def` values. Engine uses
        exponential return: cur ← cur + (def - cur) × dt × 0.025."""
        k = ECONOMY_REVERT_PER_GSEC * dt
        for state in self.market.values():
            state["buy"]  += (state["buy_def"]  - state["buy"])  * k
            state["sell"] += (state["sell_def"] - state["sell"]) * k

    def apply_trade(self, sell_res: str, buy_res: str, amount: int) -> int:
        """Execute one market trade. Returns units of buy_res received.
        Mutates self.market and self.resources."""
        sell_state = self.market[sell_res]
        buy_state  = self.market[buy_res]
        sellcost_x = sell_state["sell"]
        buycost_y  = buy_state["buy"]
        received = int(amount * sellcost_x / buycost_y)
        # Move resources
        self.resources[sell_res] -= amount
        self.resources[buy_res]  += received
        # Update rates per engine formula (res.script:_res_MarketTradeResources)
        w = amount * GC_ECONOMY_EXP
        # Selling X → both costs drift toward min
        sell_state["sell"] = (sell_state["sell"] + sell_state["sell_min"] * w) / (1 + w)
        sell_state["buy"]  = (sell_state["buy"]  + sell_state["buy_min"]  * w) / (1 + w)
        # Buying Y → both costs drift toward max
        buy_state["buy"]   = (buy_state["buy"]   + buy_state["buy_max"]   * w) / (1 + w)
        buy_state["sell"]  = (buy_state["sell"]  + buy_state["sell_max"]  * w) / (1 + w)
        return received

    def price_modifier(self, sid: str) -> float:
        """Multiplier on cost for `sid`. Engine math (player.script:1841):
            price[j] *= (1 + StrToInt(sarrparam2[...]) / 100)
        per resource. The per-resource percentages live in `sarrparam2` last 6
        slots and aren't extracted by simulate_upgrades.py yet (the direct
        `sarrparam2[X] := 'NN'` assignments are AST-opaque), so this returns 1.0
        unconditionally. When wired up, stacking is multiplicative per the engine
        (commutative — order doesn't matter). See docs/reference/05_upgrades/README.md
        «Математика применения».
        """
        return 1.0

    # --- actions ---

    def execute_action(self, act: dict):
        kind = act.get("do")
        if kind == "plant_fields":
            # Plant up to FIELDS_PER_MILL fields per mill click. Pays FIELD_GOLD_COST per field.
            # `count` arg defaults to 49 (= 7×7 grid in _unit_DoSeedWheat).
            n_mills = sum(n for sid, n in self.buildings.items() if sid.endswith("mil"))
            if n_mills == 0:
                self.events.append(f"t={self.t_g:6.1f}g: SKIP plant_fields — no mill")
                return
            requested = int(act.get("count", FIELDS_PER_MILL))
            cost_gold = requested * FIELD_GOLD_COST
            if self.resources.get("gold", 0) < cost_gold:
                affordable = self.resources.get("gold", 0) // FIELD_GOLD_COST
                self.events.append(
                    f"t={self.t_g:6.1f}g: PARTIAL plant_fields — wanted {requested} (need "
                    f"{cost_gold}G), got {int(affordable)} (have {int(self.resources['gold'])}G)"
                )
                requested = int(affordable)
            if requested <= 0:
                return
            self.resources["gold"] -= requested * FIELD_GOLD_COST
            for _ in range(requested):
                self.fields.append({
                    "state": "growing",
                    "hp": 0,
                    "transition_time": self.t_g + FIELD_GROW_TIME_SEC,
                })
            self.events.append(
                f"t={self.t_g:6.1f}g: PLANT {requested} fields (cost {requested * FIELD_GOLD_COST}G; "
                f"mature at t={self.t_g + FIELD_GROW_TIME_SEC:.1f}g)"
            )
            return
        if kind == "assign":
            for res in ("food", "wood", "stone"):
                if res in act:
                    self.assigned[res] = act[res]
            for mine_sid in list(act.keys()):
                if mine_sid not in ("do", "at", "food", "wood", "stone") and mine_sid in self.bldgs_idx:
                    requested = act[mine_sid]
                    cap_per_mine = self.mine_capacity(mine_sid)
                    n_mines = self.buildings.get(mine_sid, 0)
                    total_cap = cap_per_mine * n_mines
                    if requested > total_cap:
                        self.events.append(
                            f"t={self.t_g:6.1f}g: CLAMP {mine_sid} {requested}→{total_cap} "
                            f"(cap {cap_per_mine}/mine × {n_mines} mines)"
                        )
                        requested = total_cap
                    self.mine_assignments[mine_sid] = requested
            # validation
            assigned_total = sum(self.assigned.values()) + sum(self.mine_assignments.values())
            if assigned_total > self.total_peasants():
                self.events.append(f"t={self.t_g:6.1f}g: WARN assigned {assigned_total} peasants but have only {self.total_peasants()}")
        elif kind == "build":
            sid = act["sid"]
            builders = act.get("builders", 1)
            b = self.bldgs_idx.get(sid)
            if not b:
                self.events.append(f"t={self.t_g:6.1f}g: ERROR unknown building {sid}")
                return
            # Prereqs from tech tree
            prereqs = self.nat_tree["buildings"].get(sid, {}).get("prereqs", [])
            ok, missing = self.all_prereqs_met(prereqs)
            if not ok:
                eta = self._earliest_satisfaction_time(missing)
                if eta is not None:
                    self.events.append(
                        f"t={self.t_g:6.1f}g: DEFER build {sid} → t={eta:.1f}g "
                        f"(ждём {[p['sid'] for p in missing]})"
                    )
                    return eta
                self.events.append(f"t={self.t_g:6.1f}g: SKIP build {sid} — missing prereqs {[p['sid'] for p in missing]}")
                return
            # Cost (with costpercent scaling)
            count = self.buildings[sid]
            cp = b.get("costpercent") or 100
            mult = 1.0 if cp in (0, 100) else (cp / 100) ** count
            cost = {k: math.floor((b.get(k) or 0) * mult) for k in self.resources}
            if not self.can_pay(cost):
                self.events.append(f"t={self.t_g:6.1f}g: SKIP build {sid} — not enough resources (need {cost}, have {dict((k,int(v)) for k,v in self.resources.items())})")
                return
            self.pay(cost)
            # Construction time = buildtime × 1.13 / N_builders (capped by builder slot count).
            # Source: each builder makes 1 hit per construct anim cycle (~0.406 g-sec).
            # Each hit adds delta=0.359/buildtime progress. N builders accumulate N hits/cycle.
            # Total time = buildtime × (0.406/0.359) / N = buildtime × 1.13 / N.
            # See recon/building_mechanics.md §3.
            base_bt = b.get("buildtime_sec") or 1.0
            # Per-building slot cap from faithful sim of _unit_CalcBuilderPoints.
            cap = slot_cap_for(sid)
            # Clamp builders by physically free peasants right now: total alive
            # minus those already busy on other construction sites and those
            # standing at gathering/mine assignments.
            busy_in_construction = sum(b for _s, _f, b in self.construction)
            busy_at_resources = sum(self.assigned.values()) + sum(self.mine_assignments.values())
            free = max(0, self.total_peasants() - busy_in_construction - busy_at_resources)
            requested = builders
            n_builders = max(1, min(requested, cap, free if free > 0 else 1))
            if requested > n_builders:
                self.events.append(
                    f"t={self.t_g:6.1f}g: CLAMP build {sid} builders {requested} → {n_builders} "
                    f"(свободно {free}, cap {cap})"
                )
            bt = base_bt * 1.13 / n_builders
            finish = self.t_g + bt
            self.construction.append((sid, finish, n_builders))
            self.events.append(f"t={self.t_g:6.1f}g: START build {sid} (finish at t={finish:.1f}g, cost={cost})")
        elif kind == "train":
            bld_sid = act["building_sid"]
            unit_sid = act["unit_sid"]
            amount = act.get("amount", 1)
            if self.buildings[bld_sid] == 0:
                eta = self._earliest_satisfaction_time([{"kind": "building", "sid": bld_sid}])
                if eta is not None and eta > self.t_g:
                    self.events.append(
                        f"t={self.t_g:6.1f}g: DEFER train {unit_sid} в {bld_sid} → t={eta:.1f}g "
                        f"(ждём {bld_sid})"
                    )
                    return eta
                self.events.append(f"t={self.t_g:6.1f}g: SKIP train {unit_sid} at {bld_sid} — no such building")
                return
            u = self.units_idx.get(unit_sid)
            if not u:
                self.events.append(f"t={self.t_g:6.1f}g: ERROR unknown unit {unit_sid}")
                return
            # Prereqs
            prereqs = self.nat_tree["units"].get(unit_sid, {}).get("prereqs", [])
            ok, missing = self.all_prereqs_met(prereqs)
            if not ok:
                eta = self._earliest_satisfaction_time(missing)
                if eta is not None:
                    self.events.append(
                        f"t={self.t_g:6.1f}g: DEFER train {unit_sid} → t={eta:.1f}g "
                        f"(ждём {[p['sid'] for p in missing]})"
                    )
                    return eta
                self.events.append(f"t={self.t_g:6.1f}g: SKIP train {unit_sid} — missing {[p['sid'] for p in missing]}")
                return
            # Queue `amount` units at this building
            for _ in range(amount):
                self.unit_queues[bld_sid].append((unit_sid, 0.0))
            self.events.append(f"t={self.t_g:6.1f}g: QUEUE train {amount}× {unit_sid} at {bld_sid} (queue={len(self.unit_queues[bld_sid])})")
        elif kind == "train_infinite":
            bld_sid = act["building_sid"]
            unit_sid = act["unit_sid"]
            if self.buildings.get(bld_sid, 0) == 0:
                eta = self._earliest_satisfaction_time([{"kind": "building", "sid": bld_sid}])
                if eta is not None and eta > self.t_g:
                    self.events.append(
                        f"t={self.t_g:6.1f}g: DEFER ∞ {unit_sid} в {bld_sid} → t={eta:.1f}g"
                    )
                    return eta
                self.events.append(f"t={self.t_g:6.1f}g: SKIP ∞ {unit_sid} в {bld_sid} — нет такого здания")
                return
            u = self.units_idx.get(unit_sid)
            if not u:
                self.events.append(f"t={self.t_g:6.1f}g: ERROR unknown unit {unit_sid}")
                return
            prereqs = self.nat_tree["units"].get(unit_sid, {}).get("prereqs", [])
            ok, missing = self.all_prereqs_met(prereqs)
            if not ok:
                eta = self._earliest_satisfaction_time(missing)
                if eta is not None:
                    self.events.append(
                        f"t={self.t_g:6.1f}g: DEFER ∞ {unit_sid} → t={eta:.1f}g "
                        f"(ждём {[p['sid'] for p in missing]})"
                    )
                    return eta
                self.events.append(f"t={self.t_g:6.1f}g: SKIP ∞ {unit_sid} — нет пререквизитов")
                return
            self.infinite_orders.append({
                "building_sid": bld_sid, "unit_sid": unit_sid, "start_t": self.t_g,
            })
            self.events.append(
                f"t={self.t_g:6.1f}g: ∞ START production {unit_sid} в {bld_sid} (всего ∞-заказов: "
                f"{sum(1 for o in self.infinite_orders if o['building_sid'] == bld_sid and o['unit_sid'] == unit_sid)})"
            )
        elif kind == "research":
            upg_sid = act["upgrade_sid"]
            ug = self.upg_idx.get(upg_sid)
            if not ug:
                self.events.append(f"t={self.t_g:6.1f}g: ERROR unknown upgrade {upg_sid}")
                return
            if upg_sid in self.upgrades_done:
                self.events.append(f"t={self.t_g:6.1f}g: SKIP research {upg_sid} — already done")
                return
            # Implicit prereq: the building that hosts this upgrade must exist.
            # data.json doesn't currently surface `place_sid`, so derive it from
            # the sid convention (<nation><place>.N).
            place_bld = upgrade_place_building(upg_sid, self.nation, self.cluster)
            if place_bld and self.buildings.get(place_bld, 0) == 0:
                eta = self._earliest_satisfaction_time([{"kind": "building", "sid": place_bld}])
                if eta is not None and eta > self.t_g:
                    self.events.append(
                        f"t={self.t_g:6.1f}g: DEFER research {upg_sid} → t={eta:.1f}g "
                        f"(ждём {place_bld})"
                    )
                    return eta
                self.events.append(
                    f"t={self.t_g:6.1f}g: SKIP research {upg_sid} — здание {place_bld} не построено"
                )
                return
            prereqs = self.nat_tree["upgrades"].get(upg_sid, {}).get("prereqs", [])
            ok, missing = self.all_prereqs_met(prereqs)
            if not ok:
                eta = self._earliest_satisfaction_time(missing)
                if eta is not None:
                    self.events.append(
                        f"t={self.t_g:6.1f}g: DEFER research {upg_sid} → t={eta:.1f}g "
                        f"(ждём {[p['sid'] for p in missing]})"
                    )
                    return eta
                self.events.append(f"t={self.t_g:6.1f}g: SKIP research {upg_sid} — missing {[p['sid'] for p in missing]}")
                return
            cost = {k: ug.get(k) or 0 for k in self.resources}
            if not self.can_pay(cost):
                self.events.append(f"t={self.t_g:6.1f}g: SKIP research {upg_sid} — not enough resources")
                return
            self.pay(cost)
            time_sec = ug.get("time_sec") or 0
            finish = self.t_g + time_sec
            self.upgrades_in_progress.append((upg_sid, finish))
            self.events.append(f"t={self.t_g:6.1f}g: START research {upg_sid} (finish at t={finish:.1f}g)")
        elif kind == "trade":
            sell_res = act.get("sell")
            buy_res = act.get("buy")
            amount = int(act.get("amount") or 0)
            if sell_res not in self.market or buy_res not in self.market or sell_res == buy_res or amount <= 0:
                self.events.append(f"t={self.t_g:6.1f}g: ERROR invalid trade {sell_res}→{buy_res} ×{amount}")
                return
            mar_sid = self.market_building_sid()
            if self.buildings.get(mar_sid, 0) == 0:
                eta = self._earliest_satisfaction_time([{"kind": "building", "sid": mar_sid}])
                if eta is not None and eta > self.t_g:
                    self.events.append(
                        f"t={self.t_g:6.1f}g: DEFER trade {amount}×{sell_res}→{buy_res} → t={eta:.1f}g (ждём {mar_sid})"
                    )
                    return eta
                self.events.append(
                    f"t={self.t_g:6.1f}g: SKIP trade {amount}×{sell_res}→{buy_res} — рынок {mar_sid} не построен"
                )
                return
            if self.resources.get(sell_res, 0) < amount:
                self.events.append(
                    f"t={self.t_g:6.1f}g: SKIP trade {amount}×{sell_res}→{buy_res} — "
                    f"не хватает {sell_res} (есть {int(self.resources.get(sell_res, 0))})"
                )
                return
            received = self.apply_trade(sell_res, buy_res, amount)
            self.events.append(
                f"t={self.t_g:6.1f}g: TRADE {amount} {sell_res} → {received} {buy_res} "
                f"(курс sell={self.market[sell_res]['sell']:.2f}, buy={self.market[buy_res]['buy']:.2f})"
            )
        else:
            self.events.append(f"t={self.t_g:6.1f}g: WARN unknown action {kind}")

    # --- snapshot/output ---

    def snapshot(self):
        snap = {
            "t_g": round(self.t_g, 2),
            "t_real": round(self.t_g / self.gamespeed_factor, 2),
            **{f"res_{k}": int(v) for k, v in self.resources.items()},
            "farm_cap": self.farm_cap(),
            "farm_used": self.farm_used(),
            "peasants_total": self.total_peasants(),
            "peasants_idle": self.idle_peasants(),
            "buildings": dict(self.buildings),
            "units": dict(self.units),
            "upgrades_done": sorted(self.upgrades_done),
            "construction_in_progress": [(sid, round(finish, 1)) for sid, finish, _ in self.construction],
            "queues": {k: len(v) for k, v in self.unit_queues.items() if v},
        }
        if self.fields:
            snap["fields_alive"] = sum(1 for f in self.fields if f["state"] == "alive")
            snap["fields_growing"] = sum(1 for f in self.fields if f["state"] == "growing")
            snap["fields_dead"] = sum(1 for f in self.fields if f["state"] == "dead")
        self.snapshots.append(snap)


# ---------- Top-level run + reporting ----------

def run_simulation(build_order_path: Path, output_prefix: Path):
    data, tree = load_data()
    bo = json.loads(build_order_path.read_text(encoding="utf-8"))
    nation = bo["nation"]
    sim = SimState(nation, bo, data, tree)
    while sim.t_g <= sim.max_time_g:
        sim.step()
    write_csv(sim, output_prefix.with_suffix(".csv"))
    write_md(sim, build_order_path, output_prefix.with_suffix(".md"))


def simulate_in_memory(build_order: dict, data: dict, tree: dict,
                       builder_slots: dict | None = None) -> dict:
    """Run a simulation without touching the filesystem. Used by the visual
    editor (browser/Pyodide) to drive the same engine without file IO.

    Returns a dict with:
    - `snapshots`: list of per-tick dicts (resources, units, buildings, …)
    - `events`: list of event log lines from sim
    - `final`: convenience copy of the last snapshot
    - `meta`: nation, gamespeed_name, gamespeed_factor, max_time_g, walk_overhead, mine_overhead
    """
    global BUILDER_SLOTS
    if builder_slots is not None:
        BUILDER_SLOTS = dict(builder_slots)
    nation = build_order["nation"]
    sim = SimState(nation, build_order, data, tree)
    while sim.t_g <= sim.max_time_g:
        sim.step()
    return {
        "snapshots": list(sim.snapshots),
        "events": list(sim.events),
        "final": dict(sim.snapshots[-1]) if sim.snapshots else {},
        "meta": {
            "nation": sim.nation,
            "gamespeed_name": sim.gamespeed_name,
            "gamespeed_factor": sim.gamespeed_factor,
            "max_time_g": sim.max_time_g,
            "walk_overhead": sim.walk_overhead,
            "mine_overhead": sim.mine_overhead,
        },
    }


def write_csv(sim: SimState, path: Path):
    if not sim.snapshots:
        return
    fields = ["t_g", "t_real", "res_food", "res_wood", "res_stone", "res_gold",
              "res_iron", "res_coal", "farm_cap", "farm_used", "peasants_total",
              "peasants_idle"]
    # Add columns for any seen unit/building
    all_units = sorted({u for s in sim.snapshots for u in s["units"]})
    all_bldgs = sorted({b for s in sim.snapshots for b in s["buildings"]})
    fields += [f"bld_{b}" for b in all_bldgs]
    fields += [f"unit_{u}" for u in all_units]
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for s in sim.snapshots:
            row = {k: s.get(k, 0) for k in fields if not k.startswith(("bld_", "unit_"))}
            for b in all_bldgs:
                row[f"bld_{b}"] = s["buildings"].get(b, 0)
            for u in all_units:
                row[f"unit_{u}"] = s["units"].get(u, 0)
            w.writerow(row)
    print(f"Wrote {path}")


def write_md(sim: SimState, build_order_path: Path, path: Path):
    L = []
    L.append(f"# Отчёт симуляции: {build_order_path.stem}")
    L.append("")
    L.append(f"- Нация: **{sim.nation}**")
    L.append(f"- Скорость игры: **{sim.gamespeed_name}** (×{sim.gamespeed_factor})")
    L.append(f"- Макс. время: **{sim.max_time_g} g-sec** = {sim.max_time_g/sim.gamespeed_factor:.1f} real-sec")
    L.append(f"- Накладные расходы на ходьбу: {sim.walk_overhead*100:.0f}% (на поверхности), {sim.mine_overhead*100:.0f}% (в шахтах)")
    L.append("")
    L.append("## Итоговое состояние")
    if sim.snapshots:
        last = sim.snapshots[-1]
        L.append("")
        L.append(f"- Время: **{last['t_g']:.0f} g-sec / {last['t_real']:.0f} real-sec**")
        L.append(f"- Ресурсы: " + " / ".join(f"{k.replace('res_','').upper()}={v}" for k, v in last.items() if k.startswith("res_")))
        L.append(f"- Ферма: {last['farm_used']}/{last['farm_cap']}")
        L.append(f"- Крестьян всего: {last['peasants_total']} (без работы: {last['peasants_idle']})")
        L.append(f"- Здания: {dict(last['buildings'])}")
        L.append(f"- Юниты: {dict(last['units'])}")
        L.append(f"- Завершено апгрейдов ({len(last['upgrades_done'])}): {last['upgrades_done']}")
    L.append("")
    L.append("## Таймлайн (снимки каждые 5 g-sec)")
    L.append("")
    L.append("| t_g | t_real | F | W | S | G | I | C | ферма | крест. | здания |")
    L.append("|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---|")
    for s in sim.snapshots[::3]:  # every 15 g-sec for brevity
        farm_str = f"{s['farm_used']}/{s['farm_cap']}"
        b_str = ", ".join(f"{k}×{v}" for k, v in sorted(s["buildings"].items()) if v) or "—"
        L.append(f"| {s['t_g']:.0f} | {s['t_real']:.0f} | {s['res_food']} | {s['res_wood']} | {s['res_stone']} | "
                 f"{s['res_gold']} | {s['res_iron']} | {s['res_coal']} | {farm_str} | {s['peasants_total']} | {b_str[:50]} |")
    L.append("")
    L.append(f"## Журнал событий (всего {len(sim.events)})")
    L.append("")
    L.append("```")
    for ev in sim.events:
        L.append(ev)
    L.append("```")
    L.append("")
    L.append("---")
    L.append("")
    L.append("Сгенерировано скриптом `simulator/simulate_economy.py`. Билд-ордер: " + str(build_order_path))
    path.write_text("\n".join(L), encoding="utf-8")
    print(f"Wrote {path}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python simulate_economy.py <build_order.json> [output_prefix]")
        sys.exit(1)
    bo_path = Path(sys.argv[1])
    # Default output: current directory. The visual editor uses simulate_economy.py
    # via Pyodide and supplies its own output path; CLI users can override too.
    default_prefix = Path.cwd() / f"sim_{bo_path.stem}"
    out_prefix = Path(sys.argv[2]) if len(sys.argv) > 2 else default_prefix
    out_prefix.parent.mkdir(parents=True, exist_ok=True)
    run_simulation(bo_path, out_prefix)


if __name__ == "__main__":
    main()
