<a id="артиллерия--сводный-справочник"></a>
# Artillery - summary reference book

**Derived** file (calculated, not extracted). Counted from [`data.json`](../../../data.json) as script [`compute/compute_artillery.py`](../../../compute/compute_artillery.py).

The artillery unit in the code is the one with `objprop.bartillery = True` [^1]. The `bartprepare` subgroup includes animation of preparing a shot before each salvo - these are `cannon`, `howitzer`, `framegun`. `mortar` and `multicannon` have no training: they shoot continuously. The behavior of the order `attackpoint` for artillery is in [`recon/world/combat/target_selection.md`](../../recon/world/combat/target_selection.md) §5.2.

Naval artillery (battleship, galley, frigate, etc.) is a separate category, see [`reference/07_naval/README.md`](../../reference/07_naval/README.md). The grenadier fires fragmentation `mortarball`, but is not included in the `bartillery` group and belongs to the infantry - see [`reports/combat/combat_stats.md`](combat_stats.md).

Contents:

- [§1. Catalog and combat stats](#1-каталог-и-боевые-статы)
- [§2. Cost of one shot](#2-стоимость-одного-выстрела)
- [§3. Unit economics and national differences](#3-экономика-юнита-и-национальные-различия)
- [§4. Park limit from the Artillery depot](#4-лимит-парка-от-артиллерийского-депо)
- [§5. Notes and cross-references](#5-заметки-и-cross-references)

<a id="1-каталог-и-боевые-статы"></a>
## §1. Catalog and combat stats

One line for a unique set of stats for the main weapon - if a nation has a different stat, it is placed in a separate line. Column **Preparation** = `bartprepare`: delay animation before each shot, fixed in the script, but the exact duration in `data.json` was not extracted and is not given here. **Pause** - cold reload after a shot (`weapon.pause` in g-sec). **Accuracy** — `weapon.dispertion` in pixels and tiles; less = more accurate. Radius - `weapon.radiusmax` (tiles); `radiusmin` is shown if the unit has a melee deadzone.

| `sid` | Class | Nations | dmg | pause | DPS, g-sec | Radius | Accuracy | Preparation |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | :---: |
| `cannon` | Cannon | all 21 | 1800 | 10.94 s | 164.53 | 10.31..40.5 t | 225 px · 4.22 t | ✓ |
| `framegun` | Cannon | sco | 500 | 2.81s | 177.94 | 3.75..33.75 t | 250 px · 4.69 t | ✓ |
| `howitzer` | Bombard | all 21 | 4000 | 18.75 s | 213.33 | 13.13..26.25 t | 300 px · 5.63 t | ✓ |
| `mortar` | Supermortar | all 21 | 200 | 7.81s | 25.61 | 23.44..48.75 t | 200 px · 3.75 t | — |
| `multicannon` | Richbarreled gun | aus, bav, den, eng, fra… (+12) | 500 | 1.88s | 265.96 | 0.19..13.13 t | — | — |

Column **DPS, g-sec** is `damage / pause`, excluding formation bonuses (artillery does not have its own formations), AoE cap and target protection. The real crowd output is usually lower due to `AoE damage cap = floor(1 + (r/0.35)²)` (see [`recon/world/combat/combat_damage_pipeline.md` §6.5](../../recon/world/combat/combat_damage_pipeline.md)).

<a id="2-стоимость-одного-выстрела"></a>
## §2. Cost of one shot

`weapon[i].cost[gc_resource_type_*]` - resources that are written off at the moment of the shot (and not for each pause interval). Zero means that a particular resource is not wasted; for mortars the coefficient `coal` is gunpowder, for cannons `iron + coal` is cannonball + gunpowder. `multicannon` (buckshot case) may not have a price, because its barrel is not assigned `weapon.cost` in the script.
**Price Efficient.** The `dmg / shot_cost_g` column is `damage` divided by the “gold equivalent of the shot.” The equivalent is calculated at the standard rate `mar.def` (`reference/06_market/README.md`): `iron × 140 + coal × 140 + wood × 50 + stone × 50 + food × 25 + gold × 1` - that is, we convert the consumption into conventional units of gold at default buy prices. This is a convenient rough measure to compare how much you "pay" per point of damage with different types of artillery. Does not take into account the purchase price of the gun itself, food upkeep and wear from return fire.

| `sid` | Nations | Projectile type | dmg | iron | coal | wood/stone/gold | shot_cost_g | dmg/shot_cost_g |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `cannon` | all 21 | cannonball | 1800 | 20 | 40 | — | 8400 | 0.21 |
| `framegun` | sco | cannonball | 500 | 30 | 40 | — | 9800 | 0.05 |
| `howitzer` | all 21 | cannonball | 4000 | 20 | 100 | — | 16800 | 0.24 |
| `mortar` | all 21 | mortarball | 200 | 20 | 30 | — | 7000 | 0.03 |
| `multicannon` | aus, bav, den, eng, fra… (+12) | canister | 500 | 40 | 30 | — | 9800 | 0.05 |

**Buckshot** (cannister) for `cannon` and `multicannon` is a separate weapon with its own `pause` and cost. For `cannon` `weapon[1].damage = 0`: buckshot for a conventional cannon is implemented not by direct entry into `damage`, but through the sub-projectile mechanism `_weapon_SyncWeapon` [^2]. Each shot of buckshot spawns several sub-shells; their damage is set at the time the weapon definition is created and is not directly reduced in `data.json`. `multicannon` `weapon[0]` already has the type `cannister`, and the whole characteristic sits there. It is therefore impossible to compare the DPS of buckshot and cannonballs directly using `data.json` without reading the weapon-script.

<a id="3-экономика-юнита-и-национальные-различия"></a>
## §3. Unit economics and national differences

Purchase price, construction time, HP, shield, speed and upkeep in gold. If a nation has the same values ​​- one line, the nations are grouped.

| `sid` | Nations | Price | bt, g-sec | HP | shield | speed | `consume[gold]` | gold/g-sec | score |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `cannon` | all 21 | 250 W · 400 G · 400 I | 75.0 | 9000 | 75 | 20 | 300 | 0.48 | 50 |
| `howitzer` | all 21 | 250 W · 350 G · 300 I | 94.0 | 3000 | 75 | 20 | 350 | 0.56 | 25 |
| `mortar` | all 21 | 100 W · 75 G · 200 I | 25.0 | 400 | 25 | 24 | 50 | 0.08 | 100 |
| `multicannon` | aus, bav, den, eng, fra… (+12) | 200 W · 400 G · 250 I | 50.0 | 2000 | 50 | 16 | 300 | 0.48 | 25 |
| `framegun` | sco | 200 W · 300 G · 150 I | 50.0 | 3000 | 50 | 20 | 300 | 0.48 | 50 |

`consume[gold]` - field `objprop.consume[gc_resource_type_gold]`. The actual consumption is calculated by the formula `consume × gc_time_to_frames / 20000` for each game second (since the `_player_ProcessResourceConsume` procedure uses `speed = 20000` in the divisor). Column `gold/game sec` already takes this formula into account. Artillery is the only class that has `consume.gold > 0` for all units: the cannon must be “maintained” even if it does not fire. For infantry and cavalry `consume.gold = 0`. More details in [`../../recon/world/economy/hunger_and_rebellion.md` §2.3](../../recon/world/economy/hunger_and_rebellion.md).

<a id="4-лимит-парка-от-артиллерийского-депо"></a>
## §4. Park limit from the Artillery depot

Building `<nat>art` (Artillery Depot). During construction, adds the constant `objprop.artdepo[i]` [^3] to `gPlayer[plInd].artlimit[i]`. The limit is linear in the number of depots - without a cap on top. Without a depot, the limit = 0 [^4], and any attempt to build artillery runs into `gc_result_checkaccesscontrolreq_artlimit` [^5].

Basic distribution from one depot [^6]:

| Index `artind` | Unit Index | Slots from one depot |
| --- | --- | ---: |
| 0 - `gc_obj_artind_cannon` | `cannon` | 5 |
| 1 - `gc_obj_artind_howitzer` | `howitzer` | 5 |
| 2 - `gc_obj_artind_mortar` | `mortar` | 10 |
| 3 - `gc_obj_artind_multicannon` | `multicannon` | 3 |

In other words, to roll out a full mortar battalion of 30 pieces, you need three Artillery depots (3 × 10 = 30 slots for `mortar`).

**Price and parameters of the Artillery Depot itself** by nation. Basic default value: `costpercent = 200`, `HP = 40000`, `score = 1400` [^7]. Nations that have this unit cheaper or more expensive are shown clearly - Ukraine and Turkey have `if (i = ukr/tur)`-override [^8].

| Nation | HP | Price (food/wood/stone/gold/iron/coal) | bt, g-sec | costpercent |
| --- | ---: | --- | ---: | ---: |
| alg, aus, bav, den, eng… (+14) | 40000 | 0 / 100 / 1000 / 0 / 0 / 1400 | 245.94 | 200 |
| ukr | 40000 | 0 / 4250 / 4400 / 100 / 0 / 1400 | 245.94 | 200 |
| tur | 40000 | 0 / 500 / 1200 / 0 / 0 / 1400 | 245.94 | 200 |

<a id="5-заметки-и-cross-references"></a>
## §5. Notes and cross-references

- **Preparation before shooting.** `bartprepare = True` means that a long animation is played before each shot. The behavior of the engine when issuing a shooting order is `_unit_TryAttackPoint` [^9]. The exact preparation duration is taken from the `.aaf` animation of the `attack0` unit; in `data.json` it is not extracted. For evaluation purposes, we use `weapon.pause` as a “cold reload” on top of any animation delays.

- **Accuracy drops while moving.** Shooter and artillery while moving (`standtime < 0.25 game sec`) lose up to `gc_obj_maxattackradiusdisp = 3` effective radius tiles [^10]. Additional dispersion `dispertion` remains the same. More details - [`recon/world/combat/ranged_units_behavior.md` §4](../../recon/world/combat/ranged_units_behavior.md#4-штраф-к-дальности-при-движении-standtime).

- **Accuracy is improved by Academy upgrades.** `aca.20` (Research new sighting devices for artillery) - -35% to dispersion. `aca.27` (Develop mathematics) - another −35%, accumulates with aca.20. After both, `0.65 × 0.65 ≈ 0.42` remains from the original, that is, the accuracy increases by approximately 2.4 times. Applies only to artillery; Musketeers and archers do not have a direct dispersion upgrade.

- **AoE cap catches the crowd.** When a shell explodes, only the first `count = floor(1 + (r/0.35)²)` units within the [^11] radius receive damage. For cannon (`r ≈ 1`) this is 9 units, for mortar (`r ≈ 2`) - 33. A stretched line suffers much more than a dense crowd.

- **AI targets for artillery.** The decision on where to shoot goes through `_unit_SearchEnemyLongRangeArtillery` [^12] - this is a separate branch, not the general `_unit_SearchVictimOnProgress`. AI artillery units aim precisely at a distance of `[radiusmin .. radiusmax]`, taking into account `bsearchmaxattradius`. This branch differs from the usual scan-cells and is described only indirectly - see [`recon/world/target_selection.md`](../../recon/world/combat/target_selection.md) §7 (open question No. 4).

- **`bartprepare` and `attack-move`.** Artillery with `bartprepare = True` receives the order `gc_obj_order_type_attackpoint` through `_player_OrderUnitsToAttackPoint` [^13] - this is shooting at a coordinate, not at a specific target. The behavior for non-artillery units is different - they move with `move_mode_attack`. Details - [`recon/world/target_selection.md`](../../recon/world/combat/target_selection.md) §5.


<a id="источники"></a>
## Sources

All links are relative to `data/scripts/` in the Cossacks 3 installation.

[^1]: `objprop.bartillery := True` for five artillery units - `lib/unit.script:1725, 1757, 1788, 1815, 1847`.

[^2]: sub-projectile mechanism of buckshot (`_weapon_SyncWeapon`) - `lib/weapon.script:529`.
[^3]: Sum `artdepo[i]` to `gPlayer[plInd].artlimit[i]` - `lib/unit.script:3826-3830`.

[^4]: initialization of `artlimit[k] := 0` at the start of the batch - `lib/player.script:3169-3171`.

[^5]: checking `artcount[i] >= artlimit[i]` → `gc_result_checkaccesscontrolreq_artlimit` - `lib/miscext2.script:114-116`.

[^6]: basic distribution `artdepo[0..3]` for `<nat>art` - `lib/unit.script:2441-2444`:
    ```pascal
    objprop.artdepo[0] := 5;
    objprop.artdepo[1] := 5;
    objprop.artdepo[2] := 10; // c1 = 30
    objprop.artdepo[3] := 3;
    objprop.bartdepo := True;
    ```
[^7]: the basic parameters of the Artillery Depot are `lib/unit.script:2440`.

[^8]: `if (i = ukr) ...` and `if (i = tur) ...` for the depot price - `lib/unit.script:2447-2448`.

[^9]: `_unit_TryAttackPoint` and related branches - `lib/unit.script:7512`.

[^10]: Radius penalty for moving shooter - `lib/unit.script:5151-5156`.

[^11]: `AoE damage cap = floor(1 + (r/0.35)²)` - `lib/miscext2.script:_misc_DoRoundDamage`.

[^12]: `_unit_SearchEnemyLongRangeArtillery` (separate branch for AI art) - `lib/unit.script:11184`.

[^13]: `_player_OrderUnitsToAttackPoint` (branch for `bartprepare = True`) - `lib/player.script:2447-2481`.
