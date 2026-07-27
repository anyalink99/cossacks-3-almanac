<a id="recon-артиллерия"></a>
<a id="как-работает-артиллерия"></a>
# How Artillery Works

[← How the game works](../../README.md)

Artillery differs from ordinary ranged units in more than range and damage:
it occupies separate limit slots, can bombard coordinates, turns slowly, and
consumes iron and coal. The article begins with these player-facing rules;
fields and constants are collected near the end.

<a id="кратко"></a>
## TL;DR

- Land artillery consists of the Cannon, Howitzer, Bombard,
  Multi-barrelled Cannon, and Scotland's Frame gun [^1].
- Heavy artillery can **fire at a point**: the projectile flies toward fixed
  coordinates instead of following a particular unit. See
  [Target Selection and Attack-Move §5](target_selection.md).
- Visible **preparation for a shot** comes from turning, the attack animation,
  and reloading. Permission to fire at a point does not itself add a delay.
- Artillery Depots expand the limit for each artillery class [^2].
- **Friendly fire is possible** for grenades, cannonballs, and grapeshot:
  friendly units inside the blast radius can be hit.

---

<a id="как-применять-артиллерию"></a>
## How to Use Artillery

- **Watch the limit.** Each Artillery Depot adds capacity by gun class.
  Losing a depot does not destroy existing guns, but it may prevent new
  production until enough slots are free.
- **Bombard an area.** The Cannon, Howitzer, and Frame gun can fire at a
  selected point. The coordinate does not follow a unit and remains the
  target until a stop order or a new target is given.
- **Keep your distance.** Artillery has long maximum range but also a dead
  zone nearby. Dispersion increases with distance.
- **Keep friendly infantry away from the impact.** Area damage weakens toward
  the edge and has a target cap, but it can still hit allies.
- **Maintain supplies.** Most shots consume iron and coal; a gun cannot fire
  without the required stockpile.
- **Cover the firing cycle.** Turning, the preparation animation, and
  reloading leave heavy guns vulnerable to cavalry.

<a id="подробная-механика-и-техническое-приложение"></a>
## Detailed Mechanics and Technical Appendix

The sections below preserve exact limits, costs, formulas, and internal
flags. The practical rules are summarized above.

<a id="1-типы-артиллерии-gcobjartind"></a>
<a id="1-виды-артиллерии"></a>
### 1. Types of artillery

The game tracks a separate limit for each class [^1]:

| Class | Role |
|---|---|
| Cannon and Frame gun | Direct fire with cannonballs; both consume Cannon-class slots. |
| Howitzer | Heavy long-range fire. |
| Bombard | Indirect fire with area damage. |
| Multi-barrelled Cannon | Short-range canister salvos against groups. |

Each class has its own limit and its own Artillery Depot contribution. The
exact internal indexes are listed under
[Technical details](#technical-details).

---

<a id="2-лимиты-артиллерии"></a>
### 2. Artillery limits

The limit is **not static**: it grows as Artillery Depots are constructed.

<a id="21-арт-депо"></a>
<a id="21-артиллерийское-депо"></a>
#### 2.1. Artillery Depot

Completing an Artillery Depot adds its allowances to the owner's limits:
```
artlimit[artind] += building.artdepo[artind]
```
The change is applied when construction finishes [^2].
If the Artillery Depot is destroyed, the limit decreases again. If the player
has 20 Cannons and loses one of two depots that each add
10 slots, the limit falls to 10. The **20 existing cannons** do not
disappear; no more can be produced until losses reduce the count below
the limit.

<a id="22-использование-лимита"></a>
#### 2.2. Using the limit

When a new gun is ordered, the game compares the number already fielded with
the available limit. If no slot remains, the order is blocked. A destroyed
artillery unit frees its slot.

---

<a id="3-приказ-attackpoint--стрельба-по-точке"></a>
<a id="3-стрельба-по-точке"></a>
### 3. Firing at a point

Unlike an ordinary attack on a particular unit, heavy artillery can be
ordered to fire at selected coordinates [^3]. The differences are:

| Property | Attack a target | Fire at a point |
|---|---|---|
| Target | Specific unit or building | Map coordinates |
| If the target moves | The attacking unit follows it | The point remains fixed; artillery keeps firing into the area |
| AoE | Applies to one target | Applies to everyone within the burst radius |
| Ends | When the target dies | Only after an explicit stop or a new order |

Fire at a point is useful for:

- **Concentrated fire** — aim at the center of a group so that the blast
  catches several units.
- **Bombarding a building under construction** — fixed coordinates remain
  valid because the building cannot move out of the impact area.
- **Interdiction fire** — aim at a chokepoint and the artillery keeps
  shelling it instead of following an individual unit.

---

<a id="4-флаг-bartprepare-и-команда-attack-point"></a>
<a id="4-флаг-допуска-к-стрельбе-по-точке-bartprepare"></a>
<a id="4-кто-может-стрелять-по-точке"></a>
### 4. Which units can fire at a point

The Cannon, Howitzer, and Frame gun accept this order. Other selected units
ignore it; Towers and Shipyards, in particular, do not have this permission.

Importantly, the permission determines only whether the unit can **accept
the order**. It adds no delay and does not control the preparation animation.
The exact field and handler appear under
[Technical details](#technical-details).

<a id="41-что-выглядит-как-фаза-подготовки"></a>
#### 4.1. What looks like a preparation phase

The “preparation” visible in the game (the artillery is stationary, aimed, then
shoots) is a combination of other mechanics:

- **Attack animation** (`attack0`): the first shot plays the
  preparation segment up to the `OnAclAnimationReachedAttack` callback.
  The projectile is released on that exact frame (see
  [Animation system: timings, cycles, impact point](../../../../internals_en/engine/animation_system.md)).
  Heavy guns spend roughly 50–100 frames in preparation.
- **Turning** (`rotatespeed`): artillery slowly faces the target. The
  Bombard value `gc_obj_rotatespeed_mortar` is much lower than that of
  mobile infantry.
- **Pause between shots**: `objbase.weapon[0].pause`; for the Bombard it is
  250 frames (see `unit.script:1771`).

Together these factors make the shot feel slow. The
`bartprepare` flag is not directly involved, although it is usually set on
the same units.

<a id="42-тактическая-роль"></a>
#### 4.2. Tactical role

Heavy artillery is vulnerable while firing: it has a long pause,
turns slowly, and remains stationary during the preparation animation.
It needs infantry or walls for cover, or a cavalry raid may destroy it
before it reloads.

---

<a id="5-радиус-и-точность"></a>
### 5. Radius and accuracy

Artillery has a **large maximum range**, usually 15–25 cells versus 5–7 for
an 18th-century musket. Exact values are listed under
[Attack speed](../../../reports/combat/attack_rates.md).

Minimum range also matters: artillery **cannot fire at point-blank range**.
If an enemy moves inside that distance, the gun must move away or switch to
another available weapon.

<a id="51-рассеяние-снарядов"></a>
#### 5.1. Projectile dispersion

Artillery shells, especially cannonballs and mortar rounds, have
**dispersion**: the impact point may deviate from the selected coordinates.
See
[Target Selection and Attack-Move §9](target_selection.md#9-рассеяние-и-точность-выстрела).
The maximum deviation on each axis grows linearly with distance, but its
coefficient depends on the particular weapon's dispersion setting:
`maxdisp = distance × dispertion × 0.0267`. There is therefore no single
fraction of range that applies to every artillery weapon.

---

<a id="6-aoe-урон-от-артиллерии"></a>
<a id="6-урон-артиллерии-по-области"></a>
### 6. Area damage from artillery

Most artillery shells have a **blast radius**. On impact:

1. The game finds **all** objects within the radius.
2. Each receives `damage_at_d = damage × (1 − d / radius)` (see
   [How Damage Is Calculated §5](combat_damage_pipeline.md)).
3. **Friendly fire is possible** — if your own infantry is in the radius,
   it also takes damage.

The area-damage target cap limits how many objects one impact can damage.
This prevents one hit from affecting every unit in a dense group.

---

<a id="7-стоимость-выстрела"></a>
### 7. Shot cost

Many artillery units have `weapon_cost > 0`. Typical
costs per shot:

| Unit | Consumption |
|---|---|
| Cannon (`cannon`) | 20 iron + 40 coal |
| Frame gun (`framegun`) | 30 iron + 40 coal |
| Howitzer (`howitzer`) | 20 iron + 100 coal |
| Bombard (`mortar`) | 20 iron + 30 coal |
| Multi-barrelled Cannon (`multicannon`) | 40 iron + 30 coal per salvo |

If the player runs out of iron/coal, the artillery **does not fire**.
Therefore, during a long siege, it is critical to have stable mines.

The full list is in the [artillery report](../../../reports/combat/artillery.md),
generated from `data.json` (fields `consume` and `weapon[0].cost`).

---

<a id="8-перевозка-и-упаковка"></a>
### 8. Transport and deployment

Some artillery units have two states:

- **Deployed** (`deployed`) — can fire but moves slowly.
- **Packed** (`packed`) — moves faster but cannot fire.

Switching between states requires an animation of roughly 2–3 game seconds.
For horse artillery (`fasthorse + bartillery`), “packed” means that the gun
is horse-drawn and can move quickly.

---

<a id="технические-подробности"></a>
### Technical details

| Game concept | Internal representation |
|---|---|
| artillery flag | `bartillery` |
| artillery class | `artind`, constants `gc_obj_artind_*` |
| upper bound for class indexes | `gc_MaxArtilleryType` |
| current limit and deployed count | `gPlayer[pl].artlimit[artind]`, `artcount[artind]` |
| Artillery Depot allowances | `bartdepo`, `artdepo[artind]` |
| fire at coordinates | order `attackpoint(x, z)` |
| permission to accept that order | `bartprepare`; confirmed for `cannon`, `howitzer`, and `framegun`, checked by `_player_OrderUnitsToAttackPoint` |
| turning and reload | `rotatespeed`, `weapon[0].pause` |
| minimum and maximum range | `weapon_radiusmin`, `weapon_radiusmax` |
| shot cost | `weapon_cost`; fields `consume` and `weapon[0].cost` in the data |

<a id="источники"></a>
## Sources

[^1]: `data/scripts/dmscript.global` — constants `gc_obj_artind_*`
      and `gc_MaxArtilleryType`, which define the artillery classes.

[^2]: `data/scripts/lib/unit.script` — the Artillery Depot construction and
      destruction handlers. On completion, each allowance is added with
      `artlimit[artind] += building.artdepo[artind]`; destruction subtracts
      the same contribution.

[^3]: See [Target Selection and Attack-Move §5](target_selection.md) for the
      distinction between `move_mode_attack` (infantry) and `attackpoint`
      (artillery). Source:
      `data/scripts/lib/player.script:_player_OrderUnitsToAttackPoint`.
