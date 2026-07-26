# Recon: artillery

In-depth analysis: how artillery differs from ordinary shooters,
how does `bartprepare` (shot preparation phase) work?
yourself `attackpoint` (order to “shoot at the point”), as considered
artillery limits per player.

## TL;DR

- Artillery is a unit with `bartillery = True` and one of
  values `artind` (`gc_obj_artind_*`): gun, mortar, unicorn,
  rocket launcher [^1].
- Artillery uses **separate order line**: instead of
  `move_mode_attack` for infantry - they receive `attackpoint`
  (shooting at a point), not `attack` (at a specific unit). See
  [`target_selection.md` §5](target_selection.md).
- **`bartprepare`**: artillery must **prepare** before
  shot - stand up, turn around, unfold the installation. This
  takes ~3-5 g-sec for each pointing.
- Artillery limit - `gPlayer[pl].artlimit[artind]`, expanding
  through the art depot building (`bartdepo = True`, field
  `artdepo[gc_MaxArtilleryType]`) [^2].
- **Friendly fire is possible** for AoE projectiles (grenade,
  cannonball, buckshot) - hit your own within the gap radius.

---

## 1. Types of artillery (`gc_obj_artind_*`)

`dmscript.global` defines several `artind` indexes [^1]:

| `artind` | Destination |
|---|---|
| `gc_obj_artind_none` | Not artillery. |
| `gc_obj_artind_cannon` | Cannon with kernels. |
| `gc_obj_artind_mortar` | Mortara (mounted fire, AoE). |
| `gc_obj_artind_unicorn` | Unicorn (Russian howitzer). |
| `gc_obj_artind_rocket` | Rocket launcher (late 18th century). |
| `gc_obj_artind_multicannon` | Rich-barrel / buckshot. |

`gc_MaxArtilleryType` defines the total number of types. Each type
has its own limit and its own art depot.

---

## 2. Artillery limits

`gPlayer[pl].artlimit[gc_MaxArtilleryType]` — array of current limits
for each type. The limit is **not static** - it grows as
construction of special buildings.

### 2.1. Art depot

A building with `bartdepo = True` has an array `artdepo[gc_MaxArtilleryType]`,
which, when built, is added to the player’s `artlimit` [^2]:
```
artlimit[artind] += building.artdepo[artind]
```
If the art depot is destroyed, the limit is reduced back. If the player
20 guns, and one of the two art depots was demolished (gives +10 guns) - limit
will become 10, but **20 guns already fired** do not disappear; just
You cannot build new ones until the score decreases through losses.

### 2.2. Using the limit

When trying to order a new gun `gPlayer[pl].artcount[artind]` is compared
with `artlimit[artind]`. If `artcount >= artlimit` is an order
blocked in the UI. After each death of an artillery unit
`artcount` decreases.

---

## 3. Order `attackpoint` - shooting at a point

Unlike `attack(target_handle)` (attack a specific unit),
artillery uses **`attackpoint(x, z)`** [^3]. Differences:

| Parameter | `attack(handle)` | `attackpoint(x, z)` |
|---|---|---|
| What's the purpose | Specific Unit/Building | Coordinates on the map |
| If the target has moved | The pursuing unit follows her | The point does not move, artillery fires into the zone |
| AoE | Applies to one target | Applies to everyone within the burst radius |
| Cancel | When the target died | Explicit stop/reorientation only |

`attackpoint` is ideal for:
- **Group Shooting** - aim at the center of the crowd, the AoE will hit everyone.
- **Shooting at a building under construction** - the dot does not move, but
  the building cannot be “escaped”.
- **Defensive fire** - direct at the passage point, artillery
  will hammer into it without being distracted.

---

## 4. Flag `bartprepare` and attack-point command

`bartprepare` is the **gate flag** for the command
`gc_obj_order_type_attackpoint` (shooting at a ground point). B
in scripts the flag is used in exactly one place -
[`_player_OrderUnitsToAttackPoint`](../../../../internals_en/engine/native_api.md):
attack-point command only applies to units with `bartprepare=
True`; other units in the selection ignore it.

That is, `bartprepare` determines whether **the unit** can accept
shooting at a point (and not just at a specific target). On my own
The flag does not introduce delays or control preparation animations.

The flag is placed at `cannon`, `multicannon`, `mortar`, `howitzer`,
grapeshots `*sga`-clouds - that is, from heavy artillery. Light
horse artillery and towers without it.

### 4.1. What does the “preparation phase” look like?

The “preparation” visible in the game (the artillery is stationary, aimed, then
shoots) is a combination of other mechanics:

- **Animation attack0**: plays on the first shot
  prepare - part of the animation until the moment
  `OnAclAnimationReachedAttack`-callback - exactly in this frame
  a shot occurs (see
  [`internals/engine/animation_system.md`](../../../../internals_en/engine/animation_system.md)).
  The preparation time for heavy guns is about 50–100 frames.
- **Rotate** (`rotatespeed`): artillery turns slowly
  facing the target. For mortar `gc_obj_rotatespeed_mortar`
  significantly less than that of mobile infantry.
- **Pause between shots**: `objbase.weapon[0].pause` (for
  mortars - 250 frames, see unit.script:1771).

All three factors together create the impression of a "long shot"; flag
`bartprepare` is not directly included here, but is usually displayed on
the same units.

### 4.2. Tactical role

Heavy artillery is vulnerable at the moment of firing: long pause +
slow rotation + stillness during prepare animation. Needed
cover with infantry or walls - otherwise a cavalry raid will destroy
it before recharging.

---

## 5. Radius and accuracy

Artillery has **large `weapon_radiusmax`** (15-25 tiles
versus 5-7 for an 18th century musket). Specific numbers - in
[`reports/combat/attack_rates.md`](../../../reports/combat/attack_rates.md).

`weapon_radiusmin` is also significant: artillery **does not fire at
emphasis**. If the enemy comes closer than `radiusmin`, the unit cannot
attack - you need to move away.

<a id="51-рассеяние-снарядов"></a>
### 5.1. Projectile dispersion

Artillery shells (especially cannonballs and mortars) have **dispersion**
— displacement of the landing point from the declared one. Details - in
[`target_selection.md` §9](target_selection.md#9-рассеяние-и-точность-выстрела). Briefly:
the scattering radius is proportional to the range, something on the order of
`spread_pct ≈ distance × 0.05` tiles.

---

<a id="6-aoe-урон-от-артиллерии"></a>
## 6. AoE damage from artillery

Most artillery shells have an **AoE blast radius**
(`weapon_aoe_radius` or similar field). On hit:

1. The script finds **all** objects within a radius through
   native `GetGameObjectsInArea`.
2. Damage is applied according to the scheme `damage_at_d = damage × (1 − d / radius)`
   to each (see [`combat_damage_pipeline.md` §5](combat_damage_pipeline.md)).
3. **Friendly fire is possible** - if your own infantry is in the radius,
   she also takes damage.

AoE damage cap - total damage is limited `damage × cap`
(typically `cap = 3..5` equivalent units). This protects the heap
from instant destruction.

---

<a id="7-стоимость-выстрела"></a>
## 7. Shot cost

Many artillery units have `weapon_cost > 0`. Typical
costs per shot:

| Unit | Consumption |
|---|---|
| Cannon (cannon) | 1 iron + 1 coal |
| Mortara | 1 iron + 1 coal |
| Unicorn | 1 iron + 1 coal |
| Rocket Launcher | 1 iron + 1 coal (+ rare - 2+2) |
| Buckshot (multicannon) | 1 iron + 1 coal per salvo |

If the player runs out of iron/coal, the artillery **does not fire**.
Therefore, during a long siege, it is critical to have stable mines.

The full list is in [`reports/combat/artillery.md`](../../../reports/combat/artillery.md) (auto-gen from data.json: `consume`, `weapon[0].cost`).

---

<a id="8-перевозка-и-упаковка"></a>
## 8. Transportation and packaging

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
3. **AoE damage cap**. The exact value of `cap` is estimated to be 3-5, but
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
      `artlimit[artind] += building.artdepo[artind]`. Near death
      - `-=`.

[^3]: See [`target_selection.md` §5](target_selection.md) about
      differences between `move_mode_attack` (for infantry) and `attackpoint`
      (for artillery). Source:
      `data/scripts/lib/player.script:_player_OrderUnitsToAttackPoint`.
