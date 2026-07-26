# Weapon catalog (projectile-level)

[← weapons/](README.md) · [← compare/](../README.md) · [← Index](../../README.md)

All unique `weaponsid` (types of projectiles and throwing weapons) with their parameters and carrier units. One `weaponsid` can be used by different units with different stats (damage/pause vary), but **kind, dispersion, projectile-id are universal** - they are set in the weapon object itself (see `weapon.script`).

Column `dmg` shows the **range** of values ​​among carrier units (`min..max` if different, otherwise same number). The same for `reload (s)`.

| weaponsid | kind | dmg | reload(s) | range(t) | cost (per shot) | Carrier units |
|---|---|---|---:|---:|---|---|
| `DIMMORT1` | cannonball | 4000 | 18.75 | 26.25 | {"coal": 100, "iron": 20} | howitzer |
| `DIMMORT2` | mortarball | 200 | 7.81 | 48.75 | {"coal": 30, "iron": 20} | mortar |
| `DIMMORT2KOR` | mortarball | 1000 | 1.56 | 58.13 | {"coal": 9, "iron": 4} | galley |
| `NUCLGRE` | mortarball | 110..200 | 2.34..3.12 | 7.5..11.25 | — | grenadier, grenadierbav, grenadierden, grenadierdip, grenadierhun, grenadierpru (+1) |
| `OSTRELA` | firearrow | 100..150 | 0.78..4.69 | 11.25..20.63 | {"wood": 1}, {"wood": 2} | archer, archerdip, archersco, archertur, archerturdip, tatar |
| `PPOINTT` | cannonball | 1800 | 10.94 | 40.5 | {"coal": 40, "iron": 20} | cannon |
| `PPOINTTFRAME` | cannonball | 500 | 2.81 | 33.75 | {"coal": 40, "iron": 30} | framegun |
| `PPOINTTKOR` | cannonball | 0..1800 | 0.62..21.88 | 18.75..36.56 | {"coal": 15, "iron": 5}, {"coal": 35, "iron": 25}, {"coal": 9, "iron": 4} | battleship, chaika, frigate, galley, xebec, yacht (+1) |
| `PSMPOINTT` | canister | 500 | 1.88 | 13.13 | {"coal": 30, "iron": 40} | multicannon |
| `PSMPOINTTPUS` | canister | 0 | 10.94 | 8.44 | {"coal": 21, "iron": 24} | cannon |
| `SHOTMUSKET` | bullet | 9..43 | 2.25..6.88 | 13.13..22.5 | {"coal": 10, "iron": 6}, {"coal": 2, "iron": 1}, {"coal": 3, "iron": 1}, {"coal": 3, "iron": 2}, {"coal": 3, "iron": 3}, {"coal": 4, "iron": 2}, {"coal": 4, "iron": 3}, {"coal": 5, "iron": 2}, {"coal": 5, "iron": 3}, {"coal": 5, "iron": 4}, {"coal": 6, "iron": 3}, {"coal": 7, "iron": 3}, {"coal": 8, "iron": 4}, {"coal": 8, "iron": 5}, {"coal": 9, "iron": 4} | chasseur, dragoon, dragoon18, dragoon18dip, dragoon18fra, dragoon18net (+32) |
| `STRELA` | arrow | 15..25 | 1.56..3.12 | 13.13..20.63 | {"wood": 1}, {"wood": 2} | archer, archerdip, archersco, archertur, archerturdip, tatar |

## Notes

- **`SHOTMUSKET`** - standard musket shot. Used by most musketeers and dragoons. Strelets has more damage (9 vs. 8) with the same projectile.
- **`STRELA`** / **`OSTRELA`** - regular arrow and incendiary. Incendiary (OSTRELA, kind=`firearrow`) - the second weapon slot for archers.
- **`PPOINTTKOR`** - ship core (used by frigate, xebec, battleship, seagull, galley, yacht).
- **`PPOINTT`** vs **`PPOINTTFRAME`** - standard cannonball versus framegun core.
- **`PSMPOINTTPUS`** / **`PSMPOINTT`** - buckshot for cannon / multi-cannon.
- **`DIMMORT1`** / **`DIMMORT2`** / **`DIMMORT2KOR`** - mortar shells (1 = howitzer, 2 = mortar, 2KOR = galley ship mortar).
- **`NUCLGRE`** - granadier grenade.
- **`PPOINTTTOW`** - tower-port core (used by buildings `tow` and `por` with guns; not displayed in this table - see sheet `Buildings` in xlsx).
Definition source: `data/scripts/lib/weapon.script` (function `_weapon_AddWeapon`). Additional parameters (gravity, propagation, fxshot) are in the script, but are not uploaded to this sheet - see the source file if necessary.