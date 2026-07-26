<a id="recon-команды-юнитам"></a>
# Recon: commands to units

Deep analysis: what commands can be given to a unit, how they are stored
in the queue, how the attack and position holding modes work, where he lives
automatic response to impact. All links to the code are in
[Sources](#sources).

## TL;DR

- Each unit has an **queue of orders** up to 32 long (`TOrder` entries).
- Available orders: `move`, `attack`, `attack-move`, `garrison`,
  `ungarrison`, `patrol`, `guard`, `repair`, `build`, `extract`,
  `stop` (clears the queue).
- The queue is normally executed in order; holding Shift while
  clicks - adds to the queue, without Shift - replaces the queue.
- **Stand-mode** (`fHoldMode`) - squad mode “do not move without
  explicit order", gives complete `bonusdamagehold` / `bonusshieldhold`
  (See [`formations.md` §4](formations.md)).
- **Hold-fire** - a separate flag for the unit “do not open fire until
  explicit order." Useful for ambushes.
- **Auto-respond** — a squad in idle / hold automatically goes into
  “attack the one who hits” at the first hit to any unit
  squad.
- **Rally points** for buildings (`rallypoint`): new units,
  produced by the building go to the specified point.

---

<a id="1-структура-приказа"></a>
## 1. Order structure

`TOrder` (defined in `lib/classes.script`) - single entry
order [^1]. It has four fields: type `ord` (value from
`gc_order_*`), target handle `trg` (or `0`), position `x`, `z` (if
the order is attached to a point) and the Boolean flag `bMoveAttack` (enabled for
attack-move).

`gOrders[goHnd][0..31]` - queue of orders on the unit. Length - up to
`gc_order_maxcount = 32`. Queue management - via
`_unit_SetOrderTrg` (install), `_unit_ClearOrder` (uninstall),
`_unit_SortOrders` (arrange), `_unit_FullClearOrders`
(reset all) [^2].

<a id="11-типы-приказов"></a>
### 1.1. Types of orders

| `gc_order_*` | What | Arguments |
|---|---|---|
| `move` | Go to the point | x, z |
| `attack` | Attack a specific target | trg |
| `attack_move` | Go to the point, attack those you meet along the way | x, z + `bMoveAttack = True` |
| `garrison` | Enter the transport ship (see [`towers.md`](towers.md): other buildings do not accept infantry) | trg |
| `ungarrison` | Get out of transport | (no arguments) |
| `patrol` | Patrol between two points | x, z + second waypoint |
| `guard` | Protect the building/unit - don't go far | trg |
| `repair` | Repair the building | trg (for peasants) |
| `build` | Complete the building | trg |
| `extract` | Extract resource | trg (tree / stone / field / mine) |
| `stop` | Queue Clearing | (full reset `gOrders[goHnd]`) |

---

<a id="2-жизненный-цикл-приказа"></a>
## 2. Life cycle of an order

1. The player clicks “order”. The UI calls the `_control_*` function,
   which, through `_unit_SetOrderTrg`, writes an order to `gOrders`.
2. If **Shift is not held down**, the queue is first cleared through
   `_unit_FullClearOrders`, then the order is placed first.
3. If **Shift is held down**, the order is added to the end of the queue.
4. Each tick of the `_unit_DoTick` cycle looks at `gOrders[goHnd][0]`:
   if there is an order and is not fulfilled, it tries to take a step towards
   execution (moves, looks for a goal, starts work).
5. When the order is completed, it is deleted via `_unit_ClearOrder`,
   The queue is shifted via `_unit_OrdersOffset`.
6. If the queue is empty, the unit goes into idle and starts
   auto search for targets (see [`target_selection.md`](target_selection.md)).

---

## 3. Attack-move (`bMoveAttack`)

The most common "tactical" order. Behavior:

| Who | Implementation | Field in `TOrder` |
|---|---|---|
| Infantry | `move_mode_attack` - goes to the point, scans enemies along the way through `_unit_SearchEnemyScanCells` (see [`target_selection.md` §3](target_selection.md)). Found - attacks. | `ord = move`, `bMoveAttack = True` |
| Cavalry | Also - `move_mode_attack`. | Likewise. |
| Artillery | **Does not use** `move_mode_attack`. Instead `ord = attackpoint` with flag `bartprepare`. The artillery moves to the point, then prepares to fire (preparation animation, ~3-5 g-sec), then fires. | See [`artillery_specifics.md`](artillery_specifics.md). |

Important difference: infantry attack-move **interrupts** on anyone
encountered enemy; artillery - travels to a specific point and
fires from there. This gives the artillery a “range advantage” - it
is not distracted by infantry.

### 3.1. Cone search during attack-move

When attack-move, the unit searches for enemies **only in a 30° cone ahead**
(parameter `gc_search_attackmove_cone`, see
[`target_selection.md` §3.3](target_selection.md)). That is, a fighter
attack-move **will not stop** on an enemy from the side or behind is
"purposeful" movement.

For a unit to react to lateral threats, you need `guard` or
regular idle (no order). Idle units are searched in a full 360° radius.

---

## 4. Stand mode (`fHoldMode`) - stand to death

Enabled via UI or hotkey. Effect:

1. **Formation bonuses** switch to `fAddDamageHold` /
   `fAddShieldHold` (usually `+7`/`+7` vs `+2`/`+2` on the go).
   See [`formations.md` §4](formations.md).
2. **Units do not move voluntarily**: when auto-searching for a target, they
   won't give chase.
3. **Order `attack`** has been given - units will first **deploy to
   formation** at the current point (if not already in formation), and only then
   may start moving. In practice: it is better to **not use**
   hold for cavalry going on the attack.

Hold does not cancel automatic return fire on the one who hits -
There is a separate `fHoldFire` for this.

---

## 5. Hold-fire (`fHoldFire`) - do not open fire

Separate squad flag. When `fHoldFire = True`:

1. The unit **does not attack** even close enemies.
2. To the received blow - **replies** (or not - it depends on
   exact implementation, see §8).
3. Useful: ambushes, when the musketeers must not be given away prematurely
   shot before the enemy enters the salvo area.

Turned on by a separate UI button; usually used in conjunction with
hold-mode (ambush in a trench).

---

## 6. Patrol

`patrol(x1, z1, x2, z2)` - the unit walks between two points. Everyone
exit to the point - `move`-order + rescheduling for the next one
point. If along the way he sees an enemy in a cone, he attacks
(`move_mode_attack` behavior).

The patrol order **has no end** - it is closed. Resets
explicitly through `stop` or a new order.

---

## 7. Guard

`guard(trg)` - the unit is “tied” to the target. Behavior:

1. Stands next to the target (within a radius of ~2-3 tiles).
2. If an enemy appears nearby, he leaves his place, attacks, **returns**
   back to the target after the battle.
3. If the target has moved, it follows it, remaining within the radius.
4. If the target dies, the order is canceled and the unit goes into idle mode.

Key difference from patrol: guard **returns** to the point of protection,
and patrol simply follows a route. Guard is effective for protection
mines, warehouses, artillery in the rear.

---

## 8. Auto-respond (reaction to impact)

When any unit in the squad is hit (`_misc_DoDamage`), a separate
thread checks the status of the squad [^3]:

- If the squad is in **idle / hold / hold-fire** - all units of the squad
  switch to the “attack the one who beats me” mode.
- The reaction is transmitted via `gOrders[goHnd] := (attack, atkHnd)`.
- Effect: one salvo at the edge of the squad **wake up the entire** squad.
This behavior makes the units very “nervous” - you can’t be alone
sniper enemies one by one, they instantly respond in full formation.

See [`combat_damage_pipeline.md` §8](combat_damage_pipeline.md) for
exact location in the code.

---

## 9. Rally points

Buildings that produce units (barracks, academy, stable) have
**rally point** — rally point. Every new unit coming out of
building, receives the order `move(rally_x, rally_z)`.

Management:
- `gint_gui_setrallypointmode = True` - UI switches to
  “select rally point”, and the next click becomes the rally point.
- The point is stored in `objbase.rallypoint.x/z` for each building.
- If the rally point is inside a forest / obstacle, units will go to
  the nearest accessible point via pathfinding.

---

## 10. Garrison / Ungarrison

`garrison(building)`:
1. The unit goes to the building.
2. When reaching the radius (`captureradius = 4` tile) - `_unit_DoHideInside(goHnd, trgHnd)`.
3. The unit disappears from the map, its handle is added to `building.inside[]`.

In Cossacks 3 the only building that supports this order is for
**infantry**, is a **transport ship** (`btransport = True`).
Towers, houses and barracks do not accept infantry inside (see.
[`towers.md`](towers.md), quote at the beginning of the file). Mines -
special case: peasants enter there automatically through
`_unit_OrderExtractResources`, not via `garrison`.

`ungarrison()` - from the building UI. Units from `inside[]` appear
next to the building (from the entrance), their handles return to
`gPlayer[pl].objbase`.

The garrison **interrupts** other orders - the unit enters the building and
waiting. After exiting, the order queue **is not restored** (it
was reset at time `garrison`).

---

<a id="11-кеш-приказа-sto-и-stp"></a>
## 11. Order cache: `STO` and `STP`

Internal unit fields for optimization [^4]:

- **STO** (`Search Target Object`) — handle the target of the last search.
  Used to avoid recalculating the target every tick. Updated
  via `_unit_SetSTO_Normal`, `_unit_SetSTO`.
- **STP** (`Search Target Position`) — coordinates of the last
  “reference point” of the search: where we were going when we stumbled upon the enemy.
  Useful for returning to the route after a fight (for example, for guard).

These fields are not controlled by the player - they are an internal cache. But they
influence behavior: “the unit remembers” its target for a short
timeout even after loss of line of sight.

---

<a id="12-приказы-зданий"></a>
## 12. Building orders

Buildings also have orders, but a limited set:
- `produce(unit_sid)` — put the unit in the production queue.
- `cancel_produce(slot)` - cancel.
- `set_rally(x, z)` — set a collection point.
- `repair_self` - priority for repairs (when the peasants are free).

Buildings cannot “move” (except for siege buildings, such as artillery,
which is actually a unit) - therefore the order queue is shorter, and
processing is easier.

---

<a id="13-открытые-эмпирические-вопросы"></a>
## 13. Open empirical questions

1. **Exact behavior of `fHoldFire` when hit.** Does the unit attack in
   hold-fire in response to a hit received, or remains silent
   before an explicit order? Measure with a simple test.
2. ~~Order queue limit~~ — ✅ **Closed:**
   `gc_obj_MaxOrderCount = 12` (`dmscript.global`). This is common
   limit for all types of orders - `move`, `attack`, `produce`,
   `performupgrade`, `repair`, etc. See full list of 21 types
   `gc_obj_order_type_*` in [`production_queue.md` §1.1](../economy/production_queue.md).
3. **Resetting STO/STP when changing an order.** Is STO maintained between
   orders or reset? This affects the "continuing
   aggression" - how much the unit "remembers" the enemy after receiving
   new order.

---

<a id="источники"></a>
## Sources

[^1]: `data/scripts/lib/classes.script` - record definition
`TOrder` and related. `gOrders[goHnd][0..gc_order_maxcount-1]`
      — global queue of orders on the unit.

[^2]: `data/scripts/lib/unit.script:2649-2870` - procedures
      `_unit_ResetOrder`, `_unit_SetOrderTrg`, `_unit_ClearOrder`,
      `_unit_SortOrders`, `_unit_OrdersOffset`,
      `_unit_FullClearOrders` - queue management.

[^3]: `data/scripts/lib/miscext2.script:_misc_DoDamage` —
      auto-respond branch after decreasing hp; see also
      [`combat_damage_pipeline.md` §8](combat_damage_pipeline.md).

[^4]: `data/scripts/lib/unit.script:2894-3010` - operating procedures
      with STO (Search Target Object) and STP (Search Target Position):
      `_unit_SetClientSTO`, `_unit_SetSTO_Normal`, `_unit_SetSTO`,
      `_unit_SetSTP`.
