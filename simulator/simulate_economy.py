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
    * gold/iron/coal:  produce(13) × 32 / 250 × (1 - walk_overhead × 0.3)  [mines have less walking]
- buildings: 1 builder = nominal time; 2 builders = ×0.65; 3+ = ×0.5 (rough)
- units: building has 1-slot queue; rate = 1/unit_buildtime
- upkeep: food per unit per g-sec = consume.food / 32
- prereqs: action fails if any required building not built or upgrade not done
- farm cap: total farm = sum of building.farm; if farm_used >= cap, training stops.

What's NOT modeled (yet):
- Walking distances explicitly (uses static walk_overhead instead)
- Individual peasant fatigue / pathing
- Stone exhaustion (assumed infinite)
- Field regen + restart cycles (assumes infinite food per worker)
- Production cancel (we just ignore failed/incomplete actions)
- Multiple barracks producing different units in parallel (modeled correctly!
  but action "train" assigns to ONE specific building_sid; user must build N barracks
  and queue N times)
- Tree depletion: we don't reduce the global wood pool; assumed user-managed
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
from config import OUTPUT_DIR, DATA_JSON, STRATEGY_DIR
DATA_PATH = DATA_JSON
TREE_PATH = STRATEGY_DIR / "tech_tree.json"

# ---------- Game constants ----------
GAMESPEED = {"slow": 0.7, "normal": 1.0, "fast": 1.4}
GC_TIME_TO_FRAMES = 32
GC_FOOD_PER_UNIT = 32  # default consume.food per unit (most infantry)

PORTION = {"food": 45, "wood": 28, "stone": 40}
HITS = {"food": 22, "wood": 14, "stone": 20}
T_HIT = {"food": 22 / 32, "wood": 18 / 32, "stone": 18 / 32}  # game-seconds

# Mine produce rate per peasant per g-sec
MINE_RATE_PER_PEASANT = 13 * 32 / 250  # 1.664 res/g-sec/peasant
MINE_TYPES = ("gold", "iron", "coal")


def load_data():
    return (json.loads(DATA_PATH.read_text(encoding="utf-8")),
            json.loads(TREE_PATH.read_text(encoding="utf-8")))


# ---------- Simulator state ----------

class SimState:
    def __init__(self, nation: str, build_order: dict, data: dict, tree: dict):
        self.nation = nation
        self.data = data
        self.tree = tree
        self.nat_tree = tree["nations"][nation]
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

        # Peasant assignments: {resource_type: count}
        self.assigned = defaultdict(int)
        # Resource type → set of mine sids the peasants are inside (optional refinement)
        self.mine_assignments: dict[str, int] = defaultdict(int)  # mine_sid -> peasants inside

        # Walking overhead (0..1) for above-ground extraction
        self.walk_overhead = (build_order.get("map_config") or {}).get("walk_overhead", 0.30)
        self.mine_overhead = (build_order.get("map_config") or {}).get("mine_overhead", 0.05)

        # Efficiency per resource type (default 100, +upgrades)
        self.eff = {"food": 100, "wood": 100, "stone": 100, "gold": 100, "iron": 100, "coal": 100}
        # Field life (default 0)
        self.fieldlife = 0

        self.actions = sorted(build_order.get("actions", []), key=lambda a: a["at"])
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
        cap = 0
        for sid, n in self.buildings.items():
            b = self.bldgs_idx.get(sid)
            if b and b.get("farm"):
                cap += b["farm"] * n
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

    # --- core tick ---

    def step(self):
        # 1. Process queued actions whose time has arrived
        while self.action_idx < len(self.actions) and self.actions[self.action_idx]["at"] <= self.t_g:
            self.execute_action(self.actions[self.action_idx])
            self.action_idx += 1

        # 2. Income from peasants
        self.collect_income(self.dt)

        # 3. Upkeep (food)
        self.consume_upkeep(self.dt)

        # 4. Construction progress
        self.advance_construction()

        # 5. Unit production progress
        self.advance_unit_production(self.dt)

        # 6. Upgrade research progress
        self.advance_upgrades()

        # 7. Snapshot
        if self.t_g % self.snapshot_interval == 0 or abs(self.t_g - self.max_time_g) < self.dt:
            self.snapshot()

        self.t_g += self.dt

    def collect_income(self, dt: float):
        # Above-ground: food/wood/stone
        for res in ("food", "wood", "stone"):
            n = self.assigned.get(res, 0)
            if n == 0:
                continue
            rate_per_p = (PORTION[res] * self.eff[res] / 100) / (HITS[res] * T_HIT[res])
            rate_per_p *= (1 - self.walk_overhead)
            self.resources[res] += n * rate_per_p * dt
        # Mines
        for mine_sid, n in self.mine_assignments.items():
            if n == 0:
                continue
            # Determine resource from sid: <cluster>gol/iro/coa
            suf = mine_sid[-3:]
            res = {"gol": "gold", "iro": "iron", "coa": "coal"}.get(suf)
            if not res:
                continue
            rate_per_p = MINE_RATE_PER_PEASANT * self.eff[res] / 100
            rate_per_p *= (1 - self.mine_overhead)
            self.resources[res] += n * rate_per_p * dt

    def consume_upkeep(self, dt: float):
        # Real game formula (player.script:_player_ProcessResourceConsume):
        #   bank += consume × gc_time_to_frames × dt
        #   delivered = floor(bank / 20000)
        # Per-peasant food consumption per g-sec = consume × 32 / 20000
        # E.g. peasant with consume.food=32 → 32×32/20000 = 0.0512 food/g-sec
        # Over 300 g-sec ≈ 15.4 food per peasant.
        for sid, n in self.units.items():
            u = self.units_idx.get(sid)
            if not u:
                continue
            consume_food = (u.get("consume") or {}).get("food", 0) if isinstance(u.get("consume"), dict) else 0
            if not consume_food:
                continue
            self.resources["food"] -= n * (consume_food * GC_TIME_TO_FRAMES / 20000) * dt

    def advance_construction(self):
        finished = []
        for i, (sid, finish_time, _) in enumerate(self.construction):
            if self.t_g >= finish_time:
                finished.append(i)
        for i in reversed(finished):
            sid, finish_time, _ = self.construction.pop(i)
            self.buildings[sid] += 1
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
                bt = u["buildtime_sec"]
                # Check farm/cost when starting (progress=0)
                if progress == 0:
                    cost = {k: u.get(k) or 0 for k in self.resources}
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
            # Apply effect (efficiency / fieldlife)
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

    # --- actions ---

    def execute_action(self, act: dict):
        kind = act.get("do")
        if kind == "assign":
            for res in ("food", "wood", "stone"):
                if res in act:
                    self.assigned[res] = act[res]
            for mine_sid in list(act.keys()):
                if mine_sid not in ("do", "at", "food", "wood", "stone") and mine_sid in self.bldgs_idx:
                    self.mine_assignments[mine_sid] = act[mine_sid]
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
            # Estimate builder slot cap from collision mask perimeter (avg ~12 for typical buildings).
            # If user says builders=N > slot_cap, clamp.
            BUILDER_SLOT_CAP_DEFAULT = 12
            n_builders = max(1, min(builders, BUILDER_SLOT_CAP_DEFAULT))
            bt = base_bt * 1.13 / n_builders
            finish = self.t_g + bt
            self.construction.append((sid, finish, builders))
            self.events.append(f"t={self.t_g:6.1f}g: START build {sid} (finish at t={finish:.1f}g, cost={cost})")
        elif kind == "train":
            bld_sid = act["building_sid"]
            unit_sid = act["unit_sid"]
            amount = act.get("amount", 1)
            if self.buildings[bld_sid] == 0:
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
                self.events.append(f"t={self.t_g:6.1f}g: SKIP train {unit_sid} — missing {[p['sid'] for p in missing]}")
                return
            # Queue `amount` units at this building
            for _ in range(amount):
                self.unit_queues[bld_sid].append((unit_sid, 0.0))
            self.events.append(f"t={self.t_g:6.1f}g: QUEUE train {amount}× {unit_sid} at {bld_sid} (queue={len(self.unit_queues[bld_sid])})")
        elif kind == "research":
            upg_sid = act["upgrade_sid"]
            ug = self.upg_idx.get(upg_sid)
            if not ug:
                self.events.append(f"t={self.t_g:6.1f}g: ERROR unknown upgrade {upg_sid}")
                return
            if upg_sid in self.upgrades_done:
                self.events.append(f"t={self.t_g:6.1f}g: SKIP research {upg_sid} — already done")
                return
            prereqs = self.nat_tree["upgrades"].get(upg_sid, {}).get("prereqs", [])
            ok, missing = self.all_prereqs_met(prereqs)
            if not ok:
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
    L.append(f"# Simulation report: {build_order_path.stem}")
    L.append("")
    L.append(f"- Nation: **{sim.nation}**")
    L.append(f"- Game speed: **{sim.gamespeed_name}** (×{sim.gamespeed_factor})")
    L.append(f"- Max time: **{sim.max_time_g} g-sec** = {sim.max_time_g/sim.gamespeed_factor:.1f} real-sec")
    L.append(f"- Walking overhead: {sim.walk_overhead*100:.0f}% (above-ground), {sim.mine_overhead*100:.0f}% (mines)")
    L.append("")
    L.append("## Final state")
    if sim.snapshots:
        last = sim.snapshots[-1]
        L.append("")
        L.append(f"- Time: **{last['t_g']:.0f} g-sec / {last['t_real']:.0f} real-sec**")
        L.append(f"- Resources: " + " / ".join(f"{k.replace('res_','').upper()}={v}" for k, v in last.items() if k.startswith("res_")))
        L.append(f"- Farm: {last['farm_used']}/{last['farm_cap']}")
        L.append(f"- Peasants total: {last['peasants_total']} (idle: {last['peasants_idle']})")
        L.append(f"- Buildings: {dict(last['buildings'])}")
        L.append(f"- Units: {dict(last['units'])}")
        L.append(f"- Upgrades done ({len(last['upgrades_done'])}): {last['upgrades_done']}")
    L.append("")
    L.append("## Timeline (snapshots every 5 g-sec)")
    L.append("")
    L.append("| t_g | t_real | F | W | S | G | I | C | farm | peas | бараки |")
    L.append("|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---|")
    for s in sim.snapshots[::3]:  # every 15 g-sec for brevity
        farm_str = f"{s['farm_used']}/{s['farm_cap']}"
        b_str = ", ".join(f"{k}×{v}" for k, v in sorted(s["buildings"].items()) if v) or "—"
        L.append(f"| {s['t_g']:.0f} | {s['t_real']:.0f} | {s['res_food']} | {s['res_wood']} | {s['res_stone']} | "
                 f"{s['res_gold']} | {s['res_iron']} | {s['res_coal']} | {farm_str} | {s['peasants_total']} | {b_str[:50]} |")
    L.append("")
    L.append(f"## Events log ({len(sim.events)} total)")
    L.append("")
    L.append("```")
    for ev in sim.events:
        L.append(ev)
    L.append("```")
    L.append("")
    L.append("---")
    L.append("")
    L.append("Generated by `parser/simulate_economy.py`. Build order: " + str(build_order_path))
    path.write_text("\n".join(L), encoding="utf-8")
    print(f"Wrote {path}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python simulate_economy.py <build_order.json> [output_prefix]")
        sys.exit(1)
    bo_path = Path(sys.argv[1])
    sim_dir = STRATEGY_DIR / "sim"
    sim_dir.mkdir(parents=True, exist_ok=True)
    out_prefix = Path(sys.argv[2]) if len(sys.argv) > 2 else sim_dir / f"sim_{bo_path.stem}"
    run_simulation(bo_path, out_prefix)


if __name__ == "__main__":
    main()
