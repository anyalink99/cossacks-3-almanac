<a id="recon-артиллерия"></a>
<a id="как-работает-артиллерия"></a>
# How Artillery Works

[← How the game works](../../README.md)

An in-depth look at how artillery differs from ordinary ranged units,
how the `attackpoint` order works, what the `bartprepare` flag actually
does, and how each player's artillery limits are calculated.

<a id="кратко"></a>
## TL;DR

- Artillery is a unit with `bartillery = True` and one of
  `artind` values (`gc_obj_artind_*`): Cannon, Bombard, Unicorn,
  rocket launcher [^1].
- Artillery uses **a separate order path**: instead of
  `move_mode_attack`, used by infantry, it receives `attackpoint`
  (shooting at a point), not `attack` (at a specific unit). See
  [Target Selection and Attack-Move §5](target_selection.md).
- **`bartprepare`**: artillery must **prepare** before
  firing: stop, turn, and deploy. Together these actions usually
  take about 3–5 game seconds for each new aim.
- The artillery limit is stored in `gPlayer[pl].artlimit[artind]`
  and increased by Artillery Depots (`bartdepo = True`, field
  `artdepo[gc_MaxArtilleryType]`) [^2].
- **Friendly fire is possible** for AoE projectiles (grenade,
  cannonballs, and grapeshot): friendly units inside the blast radius
  can be hit.

---

<a id="1-типы-артиллерии-gcobjartind"></a>
## 1. Types of artillery (`gc_obj_artind_*`)

`dmscript.global` defines several `artind` indexes [^1]:

| `artind` | Destination |
|---|---|
| `gc_obj_artind_none` | Not artillery. |
| `gc_obj_artind_cannon` | Cannon firing cannonballs. |
| `gc_obj_artind_mortar` | Bombard (indirect fire with area damage). |
| `gc_obj_artind_unicorn` | Unicorn (Russian howitzer). |
| `gc_obj_artind_rocket` | Rocket launcher (late 18th century). |
| `gc_obj_artind_multicannon` | Multi-barrelled Cannon / grapeshot weapon. |

`gc_MaxArtilleryType` defines the total number of types. Each type
has its own limit and its own Artillery Depot contribution.

---

<a id="2-лимиты-артиллерии"></a>
## 2. Artillery limits

`gPlayer[pl].artlimit[gc_MaxArtilleryType]` — array of current limits
for each type. The limit is **not static** - it grows as
Artillery Depots are constructed.

<a id="21-арт-депо"></a>
<a id="21-артиллерийское-депо"></a>
### 2.1. Artillery Depot

A building with `bartdepo = True` has an array `artdepo[gc_MaxArtilleryType]`,
which, when built, is added to the player’s `artlimit` [^2]:
```
artlimit[artind] += building.artdepo[artind]
```
If the art depot is destroyed, the limit is reduced back. If the player
the player has 20 cannons and loses one of two depots that each add
10 slots, the limit falls to 10. The **20 existing cannons** do not
disappear; no more can be produced until losses reduce the count below
the limit.

<a id="22-использование-лимита"></a>
### 2.2. Using the limit

When trying to order a new gun `gPlayer[pl].artcount[artind]` is compared
with `artlimit[artind]`. If `artcount >= artlimit`, the order is
blocked in the interface. Whenever an artillery unit dies,
`artcount` decreases.

---

<a id="3-приказ-attackpoint--стрельба-по-точке"></a>
## 3. Order `attackpoint` - shooting at a point

Unlike `attack(target_handle)` (attack a specific unit),
artillery uses **`attackpoint(x, z)`** [^3]. Differences:

| Parameter | `attack(handle)` | `attackpoint(x, z)` |
|---|---|---|
| Target | Specific unit or building | Map coordinates |
| If the target moves | The attacking unit follows it | The point remains fixed; artillery keeps firing into the area |
| AoE | Applies to one target | Applies to everyone within the burst radius |
| Ends | When the target dies | Only after an explicit stop or a new order |

`attackpoint` is ideal for:
- **Group Shooting** - aim at the center of the crowd, the AoE will hit everyone.
- **Shooting at a building under construction** - the dot does not move, but
  the building cannot be “escaped”.
- **Interdiction fire** - aim at a chokepoint and the artillery
  will hammer into it without being distracted.

---

<a id="4-флаг-bartprepare-и-команда-attack-point"></a>
<a id="4-флаг-допуска-к-стрельбе-по-точке-bartprepare"></a>
## 4. Permission to fire at a point (`bartprepare`)

`bartprepare` is the **permission flag** for
`gc_obj_order_type_attackpoint` (firing at a ground point). In the
scripts it is used in exactly one place:
[`_player_OrderUnitsToAttackPoint`](../../../../internals_en/engine/native_api.md):
the order only applies to units with `bartprepare =
True`; other units in the selection ignore it.

In other words, `bartprepare` determines whether a unit can receive
this order at all. The flag itself neither adds a delay nor controls
the preparation animation.

The flag is set for the Cannon (`cannon`), Multi-barrelled Cannon
(`multicannon`), Bombard (`mortar`), Howitzer (`howitzer`), and the
`*sga` grapeshot family: in practice, heavy artillery. Light horse
artillery and towers do not have it.

<a id="41-что-выглядит-как-фаза-подготовки"></a>
### 4.1. What looks like a preparation phase

The “preparation” visible in the game (the artillery is stationary, aimed, then
shoots) is a combination of other mechanics:

- **Attack animation** (`attack0`): the first shot plays the
  preparation part up to the `OnAclAnimationReachedAttack` callback.
  The shot is released on that exact frame
  a shot occurs (see
  [Animation system: timings, cycles, impact point](../../../../internals_en/engine/animation_system.md)).
  Heavy guns spend roughly 50–100 frames in preparation.
- **Rotate** (`rotatespeed`): artillery turns slowly
  facing the target. For mortar `gc_obj_rotatespeed_mortar`
  significantly less than that of mobile infantry.
- **Pause between shots**: `objbase.weapon[0].pause` (for
  mortars - 250 frames, see unit.script:1771).

Together these factors make the shot feel slow. The
`bartprepare` flag is not directly involved, although it is usually set on
the same units.

<a id="42-тактическая-роль"></a>
### 4.2. Tactical role

Heavy artillery is vulnerable while firing: it has a long pause,
turns slowly, and remains stationary during the preparation animation.
It needs infantry or walls for cover, or a cavalry raid may destroy it
before it reloads.

---

<a id="5-радиус-и-точность"></a>
## 5. Radius and accuracy

Artillery has **large `weapon_radiusmax`** (15-25 tiles
versus 5-7 for an 18th century musket). Specific numbers - in
[Attack speed](../../../reports/combat/attack_rates.md).

`weapon_radiusmin` is also significant: artillery **cannot fire at
point-blank range**. If the enemy comes closer than `radiusmin`, the unit cannot
attack - you need to move away.

<a id="51-рассеяние-снарядов"></a>
### 5.1. Projectile dispersion

Artillery shells (especially cannonballs and mortars) have **dispersion**
— displacement of the landing point from the declared one. Details - in
[Target Selection and Attack-Move §9](target_selection.md#9-рассеяние-и-точность-выстрела). Briefly:
the scattering radius is proportional to the range, something on the order of
`spread_pct ≈ distance × 0.05` tiles.

---

<a id="6-aoe-урон-от-артиллерии"></a>
<a id="6-урон-артиллерии-по-области"></a>
## 6. AoE damage from artillery

Most artillery shells have an **AoE blast radius**
(`weapon_aoe_radius` or similar field). On hit:

1. The script finds **all** objects within a radius through
   native `GetGameObjectsInArea`.
2. Damage is applied according to the scheme `damage_at_d = damage × (1 − d / radius)`
   to each (see [How Damage Is Calculated §5](combat_damage_pipeline.md)).
3. **Friendly fire is possible** - if your own infantry is in the radius,
   it also takes damage.

AoE damage cap - total damage is limited `damage × cap`
(typically `cap = 3..5` equivalent units). This prevents a dense group
from instant destruction.

---

<a id="7-стоимость-выстрела"></a>
## 7. Shot cost

Many artillery units have `weapon_cost > 0`. Typical
costs per shot:

| Unit | Consumption |
|---|---|
| Cannon (cannon) | 1 iron + 1 coal |
| Bombard (`mortar`) | 1 iron + 1 coal |
| Unicorn | 1 iron + 1 coal |
| Rocket Launcher | 1 iron + 1 coal (+ rare - 2+2) |
| Multi-barrelled Cannon (`multicannon`) | 1 iron + 1 coal per salvo |

If the player runs out of iron/coal, the artillery **does not fire**.
Therefore, during a long siege, it is critical to have stable mines.

The full list is in the [artillery report](../../../reports/combat/artillery.md),
generated from `data.json` (fields `consume` and `weapon[0].cost`).

---

<a id="8-перевозка-и-упаковка"></a>
## 8. Transport and deployment

Some artillery units have the following states:
- **Deployed** (`deployed`) - shoots, moves slowly.
- **Packed** (`packed`) - goes faster, doesn't shoot.

Switching between states requires animation (~2-3 g-sec).
For horse artillery (`fasthorse + bartillery`) condition
“packed” means towed by horses—high speed.

---

<a id="9-открытые-эмпирические-вопросы"></a>
## 9. Open empirical questions

1. **Exact radius_min** for each type. Some artillery
   `radiusmin` zero (you can shoot point-blank), others have 5+
   tiles. The list is in `data.json`, but interpretation requires
   measurements
2. **Scattering parameters**. Formula `spread = f(distance)` -
   incomplete. Measurements with different target distances and calculations
   standard deviation of hits.
3. **Area-damage cap**. The exact value of `cap` is estimated to be 3–5, but
   measurement needed: one salvo for 1, 5, 10, 30 units, count
   total damage.

---

<a id="источники"></a>
## Sources

[^1]: `data/scripts/dmscript.global` - constants `gc_obj_artind_*`
      and `gc_MaxArtilleryType`. Exact number of types and list -
      see the file itself.

[^2]: `data/scripts/lib/unit.script` - build handler and
      art depot destruction: when added to
      `gPlayer[pl].objbase` for `bartdepo`-buildings
      `artlimit[artind] += building.artdepo[artind]`. When it is
      destroyed, the contribution is subtracted with `-=`.

[^3]: See [Target Selection and Attack-Move §5](target_selection.md) about
      differences between `move_mode_attack` (for infantry) and `attackpoint`
      (for artillery). Source:
      `data/scripts/lib/player.script:_player_OrderUnitsToAttackPoint`.
