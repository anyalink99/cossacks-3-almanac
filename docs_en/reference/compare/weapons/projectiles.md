<a id="каталог-оружия-projectile-level"></a>
<a id="оружие-и-снаряды"></a>
# Weapons and projectiles

[← Weapons and projectiles](README.md) · [← All comparisons](../README.md) · [← Quick reference](../../README.md)

This catalog lists each projectile or thrown-weapon type, its characteristics, and the units that use it. The same internal weapon ID may be shared by units with different damage or reload values, while the projectile type itself remains common.

Damage and reload columns show a range when the value differs between units.

| Internal weapon ID | Damage type | Damage | Reload (s) | Range (cells) | Shot cost | Units |
|---|---|---|---:|---:|---|---|
| `DIMMORT1` | Cannonball | 4000 | 18.75 | 26.25 | 100 Coal + 20 Iron | Howitzer (`howitzer`) |
| `DIMMORT2` | Explosive shell | 200 | 7.81 | 48.75 | 30 Coal + 20 Iron | Bombard (`mortar`) |
| `DIMMORT2KOR` | Explosive shell | 1000 | 1.56 | 58.13 | 9 Coal + 4 Iron | Galley (`galley`) |
| `NUCLGRE` | Grenade | 110..200 | 2.34..3.12 | 7.5..11.25 | — | Grenadier (`grenadier`), Grenadier (`grenadierbav`), Grenadier (`grenadierden`), Grenadier (mercenary) (`grenadierdip`), Grenadier (`grenadierhun`), Grenadier (`grenadierpru`) (+1) |
| `OSTRELA` | Incendiary arrow | 100..150 | 0.78..4.69 | 11.25..20.63 | 1 or 2 Wood | Archer (`archer`), Archer (mercenary) (`archerdip`), Bow Clansman (`archersco`), Turkish archer (`archertur`), Turkish archer (mercenary) (`archerturdip`), Tatar (`tatar`) |
| `PPOINTT` | Cannonball | 1800 | 10.94 | 40.5 | 40 Coal + 20 Iron | Cannon (`cannon`) |
| `PPOINTTFRAME` | Cannonball | 500 | 2.81 | 33.75 | 40 Coal + 30 Iron | Frame gun (`framegun`) |
| `PPOINTTKOR` | Cannonball | 0..1800 | 0.62..21.88 | 18.75..36.56 | 15 Coal + 5 Iron; 35 Coal + 25 Iron; or 9 Coal + 4 Iron | Ship of the Line (`battleship`), Chaika (`chaika`), Frigate (`frigate`), Galley (`galley`), Xebec (`xebec`), Yacht (`yacht`) (+1) |
| `PSMPOINTT` | Grapeshot | 500 | 1.88 | 13.13 | 30 Coal + 40 Iron | Multi-barrelled Cannon (`multicannon`) |
| `PSMPOINTTPUS` | Grapeshot | 0 | 10.94 | 8.44 | 21 Coal + 24 Iron | Cannon (`cannon`) |
| `SHOTMUSKET` | Bullet | 9..43 | 2.25..6.88 | 13.13..22.5 | 10 Coal + 6 Iron; 2 Coal + 1 Iron; 3 Coal + 1/2/3 Iron; 4 Coal + 2/3 Iron; 5 Coal + 2/3/4 Iron; 6 Coal + 3 Iron; 7 Coal + 3 Iron; 8 Coal + 4/5 Iron; or 9 Coal + 4 Iron | Chasseur (`chasseur`), Dragoon, 17th century (`dragoon`), Dragoon, 18th century (`dragoon18`), Dragoon, 18th century (mercenary) (`dragoon18dip`), Dragoon, 18th century (`dragoon18fra`), Dragoon, 18th century (`dragoon18net`) (+32) |
| `STRELA` | Arrow | 15..25 | 1.56..3.12 | 13.13..20.63 | 1 or 2 Wood | Archer (`archer`), Archer (mercenary) (`archerdip`), Bow Clansman (`archersco`), Turkish archer (`archertur`), Turkish archer (mercenary) (`archerturdip`), Tatar (`tatar`) |

<a id="заметки"></a>
## Notes

- **`SHOTMUSKET`** is the standard musket shot used by most Musketeers and Dragoons. The Strelets deals more damage with the same projectile.
- **`STRELA`** and **`OSTRELA`** are the standard and incendiary arrows. The incendiary arrow is an Archer's secondary weapon.
- **`PPOINTTKOR`** is the naval cannonball used by the Frigate, Xebec, Ship of the Line, Chaika, Galley, Yacht, and related ships.
- **`PPOINTT`** and **`PPOINTTFRAME`** are the Cannon and Frame gun projectiles.
- **`PSMPOINTTPUS`** and **`PSMPOINTT`** are Grapeshot projectiles for the Cannon and Multi-barrelled Cannon.
- **`DIMMORT1`**, **`DIMMORT2`**, and **`DIMMORT2KOR`** are projectiles used by the Howitzer, Bombard, and Galley's mortar.
- **`NUCLGRE`** is the Grenadier's grenade.
- **`PPOINTTTOW`** is the cannonball used by Towers and Shipyards; it is not included in the unit table.

Definitions come from `_weapon_AddWeapon` in `data/scripts/lib/weapon.script`. The same script also defines flight and visual-effect parameters.
