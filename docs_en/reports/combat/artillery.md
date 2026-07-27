<a id="артиллерия--сводный-справочник"></a>
<a id="артиллерия"></a>
# Artillery

[← Tables and calculations](../README.md)

This page covers land artillery: combat characteristics, the cost of each
shot, gun upkeep, and Artillery Depot limits.

In the game data, an artillery piece is an object marked
`objprop.bartillery = True` [^1]. Cannon (`cannon`), Howitzer (`howitzer`),
and Frame gun (`framegun`) also use a preparation animation before each
shot. Bombard (`mortar`) and Multi-barrelled Cannon (`multicannon`) do not.
See [target selection](../../recon/world/combat/target_selection.md), §5.2,
for the artillery firing order.

Ships with artillery are a separate category; see the
[Navy chapter](../../reference/07_naval/README.md). The Grenadier fires a
fragmentation projectile (`mortarball`) but remains an infantry unit; see
[combat characteristics](combat_stats.md).

Contents:

- [§1. Guns and combat characteristics](#1-орудия-и-боевые-характеристики)
- [§2. Cost of one shot](#2-стоимость-одного-выстрела)
- [§3. Unit economics and national differences](#3-экономика-юнита-и-национальные-различия)
- [§4. Artillery Depot limit](#4-лимит-парка-от-артиллерийского-депо)
- [§5. Important details](#5-важные-особенности)

<a id="1-каталог-и-боевые-статы"></a>
<a id="1-орудия-и-боевые-характеристики"></a>
## §1. Guns and combat characteristics

Each row represents a unique set of characteristics for the main weapon.
A nation with different values gets a separate row. **Preparation** is the
`bartprepare` animation before each shot; its exact duration has not yet been
extracted into `data.json`. **Reload** is `weapon.pause` in game seconds.
**Dispersion** is shown in pixels and map cells; lower is more accurate.
Range is `weapon.radiusmax`, with `radiusmin` included when a gun has a
close-range dead zone.

| Gun | Nations | Damage | Reload, game s | Damage/s | Range, cells | Dispersion, px · cells | Preparation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | :---: |
| Cannon (`cannon`) | all 21 | 1800 | 10.94 | 164.53 | 10.31–40.5 cells | 225 px · 4.22 cells | ✓ |
| Frame gun (`framegun`) | Scotland | 500 | 2.81 | 177.94 | 3.75–33.75 cells | 250 px · 4.69 cells | ✓ |
| Howitzer (`howitzer`) | all 21 | 4000 | 18.75 | 213.33 | 13.13–26.25 cells | 300 px · 5.63 cells | ✓ |
| Bombard (`mortar`) | all 21 | 200 | 7.81 | 25.61 | 23.44–48.75 cells | 200 px · 3.75 cells | — |
| Multi-barrelled Cannon (`multicannon`) | Austria, Bavaria, Denmark, England, France … (+12) | 500 | 1.88 | 265.96 | 0.19–13.13 cells | — | — |

**Damage/s** is damage per game second before target protection and the
limit on targets hit by an explosion. Actual damage against a crowd is
usually lower because of the `floor(1 + (r/0.35)²)` limit; see
[damage calculation, §6.5](../../recon/world/combat/combat_damage_pipeline.md).

<a id="2-стоимость-одного-выстрела"></a>
## §2. Cost of one shot

`weapon[i].cost[gc_resource_type_*]` stores the resources deducted when a
shot is fired. For a Bombard, `coal` represents gunpowder; for cannon-type
guns, `iron + coal` represents the ball and its powder charge.

**Cost efficiency.** The gold equivalent uses the default market prices:
`iron × 140 + coal × 140 + wood × 50 + stone × 50 + food × 25 + gold`.
Damage per unit of cost is a rough comparison only; it excludes the gun's
purchase price, upkeep, and losses to return fire.

| Gun | Nations | Projectile | Damage | Iron | Coal | Other resources | Gold equivalent | Damage per unit of cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Cannon (`cannon`) | all 21 | Cannonball | 1800 | 20 | 40 | — | 8400 | 0.21 |
| Frame gun (`framegun`) | Scotland | Cannonball | 500 | 30 | 40 | — | 9800 | 0.05 |
| Howitzer (`howitzer`) | all 21 | Cannonball | 4000 | 20 | 100 | — | 16800 | 0.24 |
| Bombard (`mortar`) | all 21 | Explosive shell | 200 | 20 | 30 | — | 7000 | 0.03 |
| Multi-barrelled Cannon (`multicannon`) | Austria, Bavaria, Denmark, England, France … (+12) | Grapeshot | 500 | 40 | 30 | — | 9800 | 0.05 |

**Canister shot** (`cannister`) is a separate weapon with its own reload and
cost. A Cannon has `weapon[1].damage = 0` because `_weapon_SyncWeapon`
creates several sub-projectiles and assigns their damage elsewhere [^2].
The Multi-barrelled Cannon instead stores its canister characteristics in
`weapon[0]`. A direct damage-per-second comparison therefore requires the
weapon script as well as `data.json`.

<a id="3-экономика-юнита-и-национальные-различия"></a>
## §3. Unit economics and national differences

Purchase price, construction time, health, shield, speed, and gold upkeep.
Nations with identical values are grouped into one row.

| Gun | Nations | Price | Build time, game s | Health | Shield | Speed | Gold upkeep (internal value) | Gold/game s | Score |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Cannon (`cannon`) | all 21 | 250 wood · 400 gold · 400 iron | 75.0 | 9000 | 75 | 20 | 300 | 0.48 | 50 |
| Howitzer (`howitzer`) | all 21 | 250 wood · 350 gold · 300 iron | 94.0 | 3000 | 75 | 20 | 350 | 0.56 | 25 |
| Bombard (`mortar`) | all 21 | 100 wood · 75 gold · 200 iron | 25.0 | 400 | 25 | 24 | 50 | 0.08 | 100 |
| Multi-barrelled Cannon (`multicannon`) | Austria, Bavaria, Denmark, England, France … (+12) | 200 wood · 400 gold · 250 iron | 50.0 | 2000 | 50 | 16 | 300 | 0.48 | 25 |
| Frame gun (`framegun`) | Scotland | 200 wood · 300 gold · 150 iron | 50.0 | 3000 | 50 | 20 | 300 | 0.48 | 50 |

The displayed gold rate already applies
`consume × gc_time_to_frames / 20000`. Artillery requires upkeep even while
idle; infantry and cavalry have no equivalent gold drain. See
[hunger and rebellion](../../recon/world/economy/hunger_and_rebellion.md).

<a id="4-лимит-парка-от-артиллерийского-депо"></a>
## §4. Artillery Depot limit

Each Artillery Depot (`<nat>art`) adds `objprop.artdepo[i]` slots to the
corresponding artillery limits [^3]. Limits grow linearly with the number of
depots. Without a depot, every artillery limit is zero [^4], and production
fails the `gc_result_checkaccesscontrolreq_artlimit` check [^5].

Basic distribution from one depot [^6]:

| Gun | Technical index | Slots from one depot |
| --- | --- | ---: |
| Cannon (`cannon`) | 0 — `gc_obj_artind_cannon` | 5 |
| Howitzer (`howitzer`) | 1 — `gc_obj_artind_howitzer` | 5 |
| Bombard (`mortar`) | 2 — `gc_obj_artind_mortar` | 10 |
| Multi-barrelled Cannon (`multicannon`) | 3 — `gc_obj_artind_multicannon` | 3 |

For example, a 30-gun Bombard force requires three Artillery Depots:
3 × 10 = 30 Bombard slots.

**Artillery Depot price and characteristics.** The ordinary version has
40,000 health and is worth 1,400 score points; every subsequent depot costs twice
as much [^7]. Ukraine and Turkey have separate base prices [^8].

| Nation | Health | Price (food/wood/stone/gold/iron/coal) | Build time, game s | Price growth, % |
| --- | ---: | --- | ---: | ---: |
| Algeria, Austria, Bavaria, Denmark, England … (+14) | 40000 | 0 / 100 / 1000 / 0 / 0 / 1400 | 245.94 | 200 |
| Ukraine | 40000 | 0 / 4250 / 4400 / 100 / 0 / 1400 | 245.94 | 200 |
| Turkey | 40000 | 0 / 500 / 1200 / 0 / 0 / 1400 | 245.94 | 200 |

<a id="5-заметки-и-cross-references"></a>
<a id="5-важные-особенности"></a>
## §5. Important details

- **Preparation before a shot.** Cannon, Howitzer, and some other guns play a
  separate long animation before every shot (`bartprepare`) [^9]. Its duration
  is stored in the `attack0` animation and has not yet been extracted into
  `data.json`; the table therefore shows only the weapon's reload interval.

- **Accuracy drops while moving.** A moving shooter
  (`standtime < 0.25 game seconds`) loses up to three cells of effective range
  [^10]. The separate dispersion value does not change. See
  [ranged-unit behavior](../../recon/world/combat/ranged_units_behavior.md#4-штраф-к-дальности-при-движении-standtime).

- **Academy research improves accuracy.** “Research new sighting devices for
  artillery” (`aca.20`) reduces dispersion by 35%. “Develop mathematics”
  (`aca.27`) reduces it by another 35%. Together they leave
  `0.65 × 0.65 ≈ 0.42` of the original dispersion, producing a spread about
  2.4 times tighter. These upgrades apply to artillery only.

- **An explosion hits a limited number of targets.** Only the first
  `count = floor(1 + (r/0.35)²)` units within the blast radius take damage
  [^11]. A Cannon at `r ≈ 1` can hit 9 units; a Bombard at `r ≈ 2` can hit 33.

- **Computer-player target selection.** Artillery uses the separate
  `_unit_SearchEnemyLongRangeArtillery` branch [^12] and considers targets
  within `[radiusmin .. radiusmax]`. See
  [target selection](../../recon/world/combat/target_selection.md), §7.

- **Preparation and attack-move.** Artillery marked `bartprepare = True`
  receives `gc_obj_order_type_attackpoint` through
  `_player_OrderUnitsToAttackPoint` [^13]: it fires at a coordinate rather than
  a specific object. See [target selection](../../recon/world/combat/target_selection.md),
  §5.


<a id="источники"></a>
## Sources

All links are relative to `data/scripts/` in the Cossacks 3 installation.

[^1]: `objprop.bartillery := True` for five artillery units —
      `lib/unit.script:1725, 1757, 1788, 1815, 1847`.

[^2]: Canister sub-projectile mechanism (`_weapon_SyncWeapon`) —
      `lib/weapon.script:529`.
[^3]: Adding `artdepo[i]` to `gPlayer[plInd].artlimit[i]` —
      `lib/unit.script:3826-3830`.

[^4]: Initializing `artlimit[k] := 0` at the start of the batch —
      `lib/player.script:3169-3171`.

[^5]: Check `artcount[i] >= artlimit[i]` →
      `gc_result_checkaccesscontrolreq_artlimit` —
      `lib/miscext2.script:114-116`.

[^6]: Base distribution `artdepo[0..3]` for `<nat>art` —
      `lib/unit.script:2441-2444`:
    ```pascal
    objprop.artdepo[0] := 5;
    objprop.artdepo[1] := 5;
    objprop.artdepo[2] := 10; // c1 = 30
    objprop.artdepo[3] := 3;
    objprop.bartdepo := True;
    ```
[^7]: Base Artillery Depot parameters — `lib/unit.script:2440`.

[^8]: `if (i = ukr) ...` and `if (i = tur) ...` for the depot price —
      `lib/unit.script:2447-2448`.

[^9]: `_unit_TryAttackPoint` and related branches —
      `lib/unit.script:7512`.

[^10]: Range penalty for a moving shooter — `lib/unit.script:5151-5156`.

[^11]: `AoE damage cap = floor(1 + (r/0.35)²)` —
       `lib/miscext2.script:_misc_DoRoundDamage`.

[^12]: `_unit_SearchEnemyLongRangeArtillery` (the computer player's
       long-range artillery branch) — `lib/unit.script:11184`.

[^13]: `_player_OrderUnitsToAttackPoint` (branch for `bartprepare = True`) —
       `lib/player.script:2447-2481`.
