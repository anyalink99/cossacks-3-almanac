<a id="recon-команды-юнитам"></a>
<a id="приказы-юнитам"></a>
# Unit Orders

[← How the game works](../../README.md)

This article explains the orders available to units, how order queuing works,
and how Attack-Move, Patrol, Guard, and Hold Position differ. Queue storage
and internal command names are collected under
[Technical Details](#technical-details).

<a id="кратко"></a>
## At a Glance

- Each unit has an **order queue**. A new order replaces it; holding `Shift`
  adds an order to the end.
- Units can move, attack, attack while moving, patrol, guard, repair, build,
  gather resources, enter and leave a transport, and stop.
- **Hold Position** prevents an idle squad from giving chase and enables the
  stronger formation bonuses.
- **Hold Fire** prevents firing without an explicit order. It is a separate
  mode useful for ambushes.
- The first hit on any member of an idle or holding squad can cause the
  entire squad to attack the aggressor.
- A building's **rally point** sends every newly produced unit to the chosen
  location.

<a id="3-атака-с-движением-bmoveattack"></a>
<a id="1-атака-с-движением"></a>
## 1. Attack-Move

| Unit type | Behavior |
|---|---|
| Infantry | Moves toward the destination, searches for enemies along the way, and attacks one it finds. |
| Cavalry | Behaves like infantry. |
| Artillery | Moves to the selected point, spends about 3–5 game seconds preparing, then begins firing. See [How Artillery Works](artillery_specifics.md). |

Infantry attack-move is interrupted by an encountered enemy. Artillery moves
to the selected firing point instead and is not distracted by infantry along
the way.

<a id="31-конусный-поиск-при-attack-move"></a>
<a id="31-конусный-поиск-при-атаке-с-движением"></a>
<a id="11-конусный-поиск-при-атаке-с-движением"></a>
<a id="11-поиск-во-всех-направлениях"></a>
### 1.1. Search in All Directions

An attack-moving unit repeatedly searches for enemies **throughout its
available radius**; see
[Target Selection and Attack-Move](target_selection.md#normal-movement-and-attack-move).
The 30° forward cone applies to ordinary movement, not Attack-Move.

<a id="4-stand-mode-fholdmode--стоять-насмерть"></a>
<a id="4-удержание-позиции-fholdmode"></a>
<a id="2-удержание-позиции"></a>
## 2. Hold Position

When enabled:

1. **Formation bonuses** switch to their stronger values—usually `+7/+7`
   instead of `+2/+2` while moving. See
   [Formations and Their Combat Bonuses §3](formations.md).
2. Units do not voluntarily give chase during automatic target acquisition.
3. After an attack order, the squad first assumes its formation at the
   current position and only then may move. Hold Position is therefore a
   poor fit for cavalry that must charge immediately.

Hold Position does not suppress automatic return fire; Hold Fire is a
separate mode.

<a id="5-hold-fire-fholdfire--не-открывать-огонь"></a>
<a id="5-запрет-огня-fholdfire"></a>
<a id="3-запрет-огня"></a>
## 3. Hold Fire

When enabled:

1. A unit does not attack even a nearby enemy.
2. If any member of its squad is hit, the squad can still retaliate as
   described in §6.
3. The mode can conceal an ambush by preventing Musketeers from firing before the
   enemy enters the intended volley area.

Hold Fire is commonly combined with Hold Position, but the two modes remain
independent.

<a id="6-патрулирование-patrol"></a>
<a id="4-патрулирование"></a>
## 4. Patrol

A unit moves between two points. On reaching one, it plans a route back to
the other. If it spots an enemy in the forward cone, it attacks.

Patrol has no natural end. Stop it explicitly or issue another order.

<a id="7-охрана-guard"></a>
<a id="5-охрана"></a>
## 5. Guard

A guard remains attached to its protected target:

1. it stays roughly 2–3 cells from the target;
2. it moves out to attack a nearby enemy and **returns** after the fight;
3. it follows a moving target while keeping nearby;
4. if the target dies, the order ends and the guard becomes idle.

Unlike a patrolling unit, a guard returns to the protected object. This is
useful around Mines, Storehouses, and rear-line artillery.

<a id="8-auto-respond-реакция-на-удар"></a>
<a id="8-автоматический-ответ-на-удар"></a>
<a id="6-автоматический-ответ-на-удар"></a>
## 6. Automatic Response to an Attack

When any member of a squad is hit, the game checks the state of the whole
squad [^3]:

- if the squad is idle, holding position, or holding fire, all its units
  switch to attacking the aggressor;
- consequently, one volley into the edge of a formation can **wake the
  entire squad**.

This makes it difficult to pick off members of a formation one at a time.
See [How Damage Is Calculated §8](combat_damage_pipeline.md).

<a id="9-точки-сбора"></a>
<a id="7-точки-сбора"></a>
## 7. Rally Points

Buildings that produce units—Barracks, Academy, Stable, and others—have a
**rally point**. Every newly produced unit immediately heads toward it.

- The next click after choosing the rally-point command sets its position.
- If the point lies inside a forest or obstacle, pathfinding sends units to
  the nearest reachable location.

<a id="10-вход-в-транспорт-и-выход-из-него"></a>
<a id="8-вход-в-транспорт-и-выход-из-него"></a>
## 8. Entering and Leaving a Transport

1. The unit approaches the transport.
2. At a distance of four cells, it goes inside.
3. It disappears from the map and is counted among the transport's
   passengers.

In Cossacks 3, the only ordinary object that accepts **infantry** this way is
the **Ferry**. Towers, Houses, and Barracks do not accept infantry;
see [How Towers Work](towers.md). Mines are a separate case: Peasants enter
them automatically as part of resource gathering.

On leaving, passengers appear beside the transport on its entrance side.
Entering a transport interrupts all other orders, and the old queue is not
restored after leaving.

<a id="12-приказы-зданий"></a>
<a id="9-приказы-зданиям"></a>
## 9. Building Orders

Buildings have a shorter set of orders: start or cancel production, set a
rally point, and request repairs. Ordinary buildings cannot move. Siege
weapons are units from the engine's point of view and use normal movement.

<a id="technical-details"></a>
<a id="технические-подробности"></a>
<a id="10-технические-подробности"></a>
## 10. Technical Details

<a id="1-структура-приказа"></a>
<a id="101-как-хранится-приказ"></a>
### 10.1. Order Storage

`TOrder` stores the type `ord`, a target handle `trg` or zero, coordinates
`x`, `z`, and the Attack-Move flag `bMoveAttack` [^1]. The queue
`gOrders[goHnd][0..31]` holds up to `gc_order_maxcount = 32` records.
`_unit_SetOrderTrg`, `_unit_ClearOrder`, `_unit_SortOrders`, and
`_unit_FullClearOrders` manage it [^2].

<a id="11-типы-приказов"></a>
| Player action | Internal type | Arguments |
|---|---|---|
| Move to a point | `move` | `x`, `z` |
| Attack a target | `attack` | `trg` |
| Attack-Move | `attack_move` | `x`, `z`, `bMoveAttack = True` |
| Enter a transport | `garrison` | `trg` |
| Leave a transport | `ungarrison` | none |
| Patrol | `patrol` | two route points |
| Guard an object | `guard` | `trg` |
| Repair | `repair` | `trg` |
| Continue construction | `build` | `trg` |
| Gather a resource | `extract` | `trg` |
| Stop | `stop` | clears the queue |

<a id="2-жизненный-цикл-приказа"></a>
Without `Shift`, the interface first calls `_unit_FullClearOrders`, then
writes the new order. With `Shift`, it appends the order. Every tick,
`_unit_DoTick` processes the first entry. `_unit_ClearOrder` removes a
completed order and `_unit_OrdersOffset` advances the queue. An empty queue
makes the unit idle and starts automatic target acquisition.

Infantry and cavalry implement Attack-Move as `ord = move`,
`bMoveAttack = True`, and `move_mode_attack`;
`_unit_SearchEnemyScanCells` performs the scan. Artillery uses
`ord = attackpoint` and `bartprepare`. The 30° forward-search restriction
belongs to ordinary movement.

The rally point is stored in `objbase.rallypoint.x/z`;
`gint_gui_setrallypointmode` enables its placement mode. At
`captureradius = 4`, `_unit_DoHideInside` places the unit handle in
`building.inside[]`. Leaving restores it to `gPlayer[pl].objbase`.

<a id="11-кеш-приказа-sto-и-stp"></a>
<a id="102-кеш-последней-цели-и-точки"></a>
### 10.2. Last-Target and Last-Position Cache

Two internal fields avoid repeating the same search every tick [^4]:

- `STO` (`Search Target Object`) stores the last target handle and is updated
  by `_unit_SetSTO_Normal` and `_unit_SetSTO`;
- `STP` (`Search Target Position`) stores the last reference point, allowing
  a unit to return to its route after combat.

These fields are not player-controlled, but they let a unit remember its
target briefly after losing direct vision.

<a id="103-внутренние-приказы-зданий"></a>
### 10.3. Internal Building Orders

- `produce(unit_sid)` adds a unit to production;
- `cancel_produce(slot)` cancels it;
- `set_rally(x, z)` sets the rally point;
- `repair_self` requests repair by available Peasants.

<a id="источники"></a>
## Sources

[^1]: `data/scripts/lib/classes.script` — the `TOrder` record and
      `gOrders[goHnd][0..gc_order_maxcount-1]`.

[^2]: `data/scripts/lib/unit.script:2649-2870` — `_unit_ResetOrder`,
      `_unit_SetOrderTrg`, `_unit_ClearOrder`, `_unit_SortOrders`,
      `_unit_OrdersOffset`, and `_unit_FullClearOrders`.

[^3]: `data/scripts/lib/miscext2.script:_misc_DoDamage` — the automatic
      response branch after health is reduced.

[^4]: `data/scripts/lib/unit.script:2894-3010` — `_unit_SetClientSTO`,
      `_unit_SetSTO_Normal`, `_unit_SetSTO`, and `_unit_SetSTP`.
