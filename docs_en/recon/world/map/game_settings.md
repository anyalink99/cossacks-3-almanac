<a id="recon-настройки-лобби--что-движок-делает-с-каждой-опцией"></a>
<a id="как-настройки-матча-влияют-на-игру"></a>
# How Match Settings Affect the Game

[← How the game works](../../README.md)

This article explains what the pre-match options actually change: which ones
rebuild the map, which act only during play, and which restrictions are not
obvious from their lobby labels.

The numerical values and in-game labels are collected separately:

- **[lobby settings](../../../reports/map/lobby_settings.md)** —
  a reader-friendly reference for every option (localized names, numerical values,
  default values).
- **[`derived/game_settings.json`](../../../../derived/game_settings.json)** —
  the same data in machine-readable form, for the editor and tools.

This page covers what the table cannot show: the practical effect of each
choice. Exact fields, functions, and saved-record layout are collected under
[Technical details](#technical-details); script excerpts are in
[Sources](#sources).

<a id="1-структура-tmapsettings"></a>
<a id="1-как-хранятся-настройки-матча"></a>
<a id="быстрый-ориентир"></a>
## Quick guide

- **Map size, terrain type, relief, season, and deposits** affect the
  generated map and do not change after the match begins.
- **Starting army and resources** define the opening position, but the base
  eighteen Peasants always appear.
- **Peace time, capture, the 18th century, mercenaries, speed, and population
  limit** change rules during play.
- **Computer-player difficulty** primarily changes construction and
  recruitment speed; it does not grant extra starting resources.

<a id="2-что-движок-делает-с-gen-параметрами"></a>
<a id="2-настройки-генерации-карты"></a>
<a id="настройки-генерации-карты"></a>
## Map-generation settings

| Setting | Effect |
|---|---|
| Map size | Sets the width and height of the square map in cells and affects object-placement density [^5] [^6]. |
| Terrain type | Selects the map foundation. Peninsulas, Islands, and Continents contain sea water accessible to ships and a Port [^7]. |
| Relief | Controls mountain and hill density. Highlands leaves less flat ground for Farms and Storehouses [^8]. |
| Starting resources | Gives every player the selected amount of each of the six resources: 1,000, 4,000, 5,000, or 1,000,000 [^9]. |
| Mineral deposits | Changes how many placement passes are attempted. A Tiny Rich map can use three passes for each of three deposit types [^10]. See [How mineral deposits are placed](map_generation_pipeline.md#8-how-mineral-deposits-are-placed). |
| Season | Desert replaces normal environment sets with desert sets; other seasons mainly change textures [^11]. |
| Generation keys | Together with the base mask, uniquely determine terrain and object placement [^12]. |

> **Forest type.** The player selects a forest variant in the match room, but
> the shared generator immediately overwrites the choice with `0` for every
> terrain type [^13]. The option therefore does not affect the map: mixed
> conifer forests are used, with separate environment sets for Desert.

<a id="3-что-движок-делает-с-additional-параметрами"></a>
<a id="3-дополнительные-правила-партии"></a>
<a id="дополнительные-правила-партии"></a>
## Additional match rules
<a id="31-startingunits--стартовая-армия"></a>
<a id="31-стартовая-армия-startingunits"></a>
### 3.1 Starting army (`startingunits`)

The specific set of units/buildings for each option is read from
`data/game/var/startingsettings.cfg`. Fields: `addresources` (additional resources),
`countries` (arrangement legend: `P` = peasant, `X` = infantryman, `B` =
drummer, `O` = officer, `Q`/`W` = mission buildings, etc.).

> **The base 18 Peasants always appear.** With the Default option, the engine
> calls `CreateStartPointPeasants` and places **18 Peasants** in a 6 × 3 grid
> around the starting position, 0.75 cells apart [^14].

<a id="32-peacetime--как-устроен-мир"></a>
<a id="peacetime--как-устроен-мир"></a>
<a id="32-время-мира-peacetime"></a>
### 3.2 Peace time (`peacetime`)

Function `_misc_GetPeaceTime` decodes the index into game minutes and multiplies by
60 to obtain game seconds [^15]:

| Value (`ind`) | Game minutes |
|---:|---:|
| 0 | 0 (No peace time) |
| 1 | 10 |
| 2 | 20 |
| 3 | 30 |
| 4 | 45 |
| 5 | 60 |
| 6 | 90 |
| 7 | 120 |
| 8 | 180 |
| 9 | 240 |
| 11 | 15 |

These are **game minutes**. At Fast speed (`gamespeed = 2`), one game minute
lasts about 42.9 real seconds, so ten minutes of peace last about seven real
minutes.

When generating the map [^16]:

- `gbool_peacemode := (peacetime <> 0)` - the flag is turned on if any
  non-zero preset.
- `gfloat_peacetime := _misc_GetPeaceTime(ind)` stores the duration in game
  seconds.
- `SetupBorderObjects` creates visual "boundaries" around each player.

While `gbool_peacemode = True`:

- **Enemy searches are disabled.** `_unit_SearchEnemy*` checks `bpeacetime`;
  while it is `True`, units cannot acquire or attack enemies [^17].
- **Territory ownership grid.** `_misc_IsCorrectScanCellOwner` returns
  `True` only for neutral and owned cells; enemies cannot enter
  your territory [^18].
- **Capture buildings are prohibited** on foreign territory.

On every `Nothing` service tick, the server checks whether peace time has
expired [^19]. If it has, the flag is cleared, the `ptborder` objects are
removed, and combat begins. Only the authoritative side makes this decision:
the server in multiplayer or the game itself in single-player. Replays and
clients receive the change through a synchronization event.

<a id="33-century18--переход-в-18-век"></a>
<a id="33-переход-в-xviii-век-century18"></a>
### 3.3 Advance to the 18th century (`century18`)

| Value | Effect |
|---|---|
| 0 | Standard rules: the “Advance to the 18th Century” upgrade (`<nat>cen.1`) becomes available after an Academy (`aca`), Cathedral (`tem`), and Artillery Depot (`art`). |
| 1 | Upgrade `cen.1` is disabled; the 18th century is unavailable in this match. |
| 2 | The player starts in the 18th century - `cen.1` has already been researched. |

For Ukraine (`ukr`), Turkey (`tur`), and Algeria (`alg`), the “Immediately”
option has no effect: those nations have no `cen.1` upgrade in `country.script`. See
[upgrades](../../../reference/05_upgrades/README.md).

<a id="34-capture--правила-захвата"></a>
<a id="34-правила-захвата-capture"></a>
### 3.4 Capture rules (`capture`)

Capture geometry (radii, who is captured, who is not, towers, walls) - in
[building capture](../economy/capture_mechanics.md).

The `capture` option only enables or disables target classes: `1` prevents
Peasant capture, `2` also protects Town Halls, and `3` permits only artillery
capture. The underlying range and ownership checks remain unchanged.

<a id="35-marketdip--рынок-и-дипцентр"></a>
<a id="35-рынок-и-дипломатический-центр-marketdip"></a>
### 3.5 Market and Diplomatic Centre (`marketdip`)

`value = 4` (“Expensive Mercenaries”) multiplies the hiring price by
`gc_gameplay_expensivemercskoef = 3`. Details of Diplomatic Centre economics are in
[mercenaries and diplomacy](../../systems/mercenaries_diplomacy.md).

<a id="36-gamespeed--скорость-партии"></a>
<a id="36-скорость-партии-gamespeed"></a>
### 3.6 Game speed (`gamespeed`)

Constants `gc_settings_gamespeed_*` set the number of ticks per real second:
`slow = 7`, `normal = 10`, `fast = 14`. A fourth value of `20`
(`ultra-fast`) is commented out [^20]. `gc_time_to_frames` always remains 32;
only the relationship between game time and real time changes.

| Speed | Ticks / real second | Multiplier | Real time per 1 game second |
|---:|---:|---:|---:|
| 0 (slow) | 7 | ×0.7 | 1.43 real seconds |
| 1 (normal) | 10 | ×1.0 | 1.00 real seconds |
| 2 (fast) | 14 | ×1.4 | 0.71 real seconds |

<a id="37-limit--лимит-населения"></a>
<a id="37-лимит-населения-limit"></a>
### 3.7 Population limit (`limit`)

This is a **global ceiling applied after** the population provided by buildings:
```
pop_cap = cen × 100 + bar × 150 + ba2 × 250 + hou × 25
```
Global ceiling (`limit = 1..8` → 500 / 750 / 1000 / 1500 / 2200 / 3000 /
5000 / 8000) is never exceeded, even if the farm bonus allows more.

The interface displays it through
`randommap.settings.limit.custom = "%value% units"`; `_misc_GetLimitText`
substitutes the number.

<a id="38-adviserassistant--помощник"></a>
<a id="38-помощник-adviserassistant"></a>
### 3.8 Adviser (`adviserassistant`)

Contextual hints in the corner of the screen. They do not affect gameplay.

<a id="4-сложность-ии--gcplayerdifficulty"></a>
<a id="сложность-компьютерного-игрока"></a>
## Computer-player difficulty

The constants `gc_player_difficulty_*` from `-1` to `4` [^21] are listed:

| Value (`difficulty`) | Localization key | Difficulty | Speed multiplier |
|---:|---|---|---:|
| -1 | None | No AI | — |
| 0 | `difficulty.1` | Easy | 0.30 |
| 1 | `difficulty.1` | Normal | 0.50 |
| 2 | `difficulty.2` | Hard | 0.75 |
| 3 | `difficulty.3` | Very Hard | 1.00 |
| 4 | `difficulty.4` | Impossible | 1.25 |

`_player_GetDifficultyKoef` applies this multiplier to AI construction and
recruitment speed. **AI receives no extra starting resources** at any
difficulty. See [computer-player behavior](../../systems/ai_behavior.md).

See also [mercenaries and diplomacy](../../systems/mercenaries_diplomacy.md) §3 - on
Hard and above, when `brebellion = True`, mercenaries have an approximately
18.31% chance per tick to change sides.

<a id="технические-подробности"></a>
## Technical details

`TMapSettings` is split into map generation (`gen`) and match rules
(`additional`) [^1]. `_misc_SaveLanRoomData` writes the settings to a saved
game [^2].

| Reader-facing name | Internal field |
|---|---|
| Map size | `mapsize` |
| Terrain type | `terraintype` |
| Relief | `relieftype` |
| Starting resources | `resourcestart` |
| Deposit richness | `resourcemines` |
| Season | `season` |
| Terrain and placement keys | `randkey1`, `randkey0` |
| Starting army | `startingunits` |
| Peace time | `peacetime` |
| Advance to the 18th century | `century18` |
| Capture | `capture` |
| Market and Diplomatic Center | `marketdip` |
| Population limit | `limit` |
| Game speed | `gamespeed` |
| Adviser | `adviserassistant` |

<a id="5-глобальные-константы-партии"></a>
<a id="глобальные-константы-партии"></a>
### Global match constants

These are not lobby options, but engine constants that determine the shape of all
settings [^22].

| Constant | Value | Meaning |
|---|---:|---|
| `gc_MaxPlayerCount` | 12 | Maximum players (including neutral and mercenary slot). |
| `gc_MaxObjCount` | 32000 | Hard cap of units on the map (all players together). |
| `gc_time_to_frames` | 32 | Frames in one game second. |
| `gc_buildtime_modifier` | 10 | Additional multiplier **for buildings only**: game seconds = `frames × 10 / 32`. Units do not use it. |
| `gc_resource_hitsneeded_food` | 22 | Strikes with a hoe before handing over food. |
| `gc_resource_hitsneeded_wood` | 14 | Strikes with an ax until wood is delivered. |
| `gc_resource_hitsneeded_stone` | 20 | Strikes with a pickaxe until hitting the stone. |
| `gc_obj_resource_portion_food` | 45 | Food delivered per trip at `eff = 100`. |
| `gc_obj_resource_portion_wood` | 28 | Wood delivered per trip at `eff = 100`. |
| `gc_obj_resource_portion_stone` | 40 | Stone delivered per trip at `eff = 100`. |
| `gc_obj_speed_peasant` | 40 | The declared speed of the peasant - but in the script the assignment is commented out [^23] (see [peasant resource gathering](../economy/peasant_extraction.md) §9). |

<a id="6-победа-и-поражение"></a>
<a id="победа-и-поражение"></a>
## 6. Victory and defeat

See separate document - [Victory, Defeat, and the End of a Match](../../systems/victory_conditions.md).
In brief, victory means that only one team remains. `farmused = 0` means
defeat, but it cannot reach zero while the player still has at least one
Peasant or Town Hall. Cossacks 3 has no Wonder victory; score is used only for
statistics.

---

<a id="источники"></a>
## Sources

All references are relative to `data/scripts/` in the Cossacks 3 installation. Line numbers are
from the current installation files; After the game patch, recheck.

[^1]: Root structure `TMapSettings` - `lib/classes.script:85-88`:
    ```pascal
    type TMapSettings = class
       gen        : TMapSettingsGen;          // map-generator parameters
       additional : TMapSettingsAdditional;   // game rules
    end;
    ```
[^2]: Serialization of settings to save file - `_misc_SaveLanRoomData` in
    `lib/miscext2.script:2360-2380`.

[^3]: `TMapSettingsGen` — `lib/classes.script:74-83`:
    ```pascal
    type TMapSettingsGen = class
       randkey0      : Integer;   // RNG key for placement (mines / forests / stones)
       randkey1      : Integer;   // RNG key for relief / terrain
       mapsize       : Integer;   // 0..3 — size
       terraintype   : Integer;   // 0..9 — terrain / water type
       relieftype    : Integer;   // 0..5 — relief type
       resourcestart : Integer;   // 0..3 — starting resources
       resourcemines : Integer;   // 0..2 — mine density
       season        : Integer;   // 0..3 — season / decoration
    end;
    ```

[^4]: `TMapSettingsAdditional` — `lib/classes.script:58-72`:
    ```pascal
    type TMapSettingsAdditional = class
       activeoption     : Integer;
       startingunits    : Integer;   // starting unit / building set
       balloon          : Integer;   // balloons
       cannons          : Integer;   // cannons / walls / towers
       peacetime        : Integer;   // peace time
       century18        : Integer;   // advance to the 18th century
       capture           : Integer;  // capture rules
       marketdip        : Integer;   // Market / Diplomatic Center
       teams            : Integer;   // ally placement
       autosave         : Integer;
       limit            : Integer;   // population limit
       gamespeed        : Integer;   // game speed
       adviserassistant : Integer;   // adviser
    end;
    ```
[^5]: Application of `mapsize` - `common.inc/dogenerate.inc:1530-1545`.

[^6]: Density modifiers `prob*` depending on map size -
    `lib/misc.script:3929-3941`.

[^7]: Application `terraintype` - `common.inc/dogenerate.inc:1500-1530`;
    checking for the presence of the sea - `_misc_HasMaritime` to `lib/misc.script:5466`.

[^8]: Application of `relieftype` - `common.inc/dogenerate.inc:1640-1660`.

[^9]: Application `resourcestart` - `common.inc/initmapgen.inc:166-189`:
    ```pascal
    for j := 0 to gc_ResCount - 1 do
       _res_SetResToPlayerByIndex(i, j, ...);
    ```
[^10]: Application `resourcemines` - `common.inc/dogenerate.inc:1544`,
    is substituted in `minesdensity`.

[^11]: Application `season` - `common.inc/dogenerate.inc:4`:
    ```pascal
    bDesert := (season = 3);
    ```
[^12]: RNG keys `randkey0` / `randkey1` - `common.inc/generatemap.inc:142` and
    repeatedly in `common.inc/dogenerate.inc`.

[^13]: Overwriting `foreststype` on Land - `common.inc/dogenerate.inc:5-6`.

[^14]: Arrangement of starting peasants - `CreateStartPointPeasants` in
    `common.inc/dogenerate.inc:1231-1281`.

[^15]: Decoding `peacetime` to game seconds -
    `lib/misc.script:4262-4282`:
    ```pascal
    function _misc_GetPeaceTime(ind : Integer) : Float;
    begin
       case ind of
          0  : Result := 0;     // No peace time
          1  : Result := 10;    // 10 minutes
          2  : Result := 20;
          3  : Result := 30;
          4  : Result := 45;
          5  : Result := 60;
          6  : Result := 90;
          7  : Result := 120;
          8  : Result := 180;
          9  : Result := 240;
          11 : Result := 15;
       end;
       Result := Result * 60;   // convert to game seconds
    end;
    ```
[^16]: Peacetime initialization during generation - `common.inc/dogenerate.inc:2060`
    (`gbool_peacemode := (peacetime <> 0)`) and
    `common.inc/dogenerate.inc:2065` (`SetupBorderObjects`).

[^17]: Blocking the search for enemies in peacetime - `lib/unit.script:5516`,
    checking the flag `bpeacetime` in `_unit_SearchEnemy*`.

[^18]: Prohibition of foreign territory in peacetime - `_misc_IsCorrectScanCellOwner` in
    `lib/misc.script:2424`.

[^19]: End of peacetime on Nothing-tick -
    `progress/nothing.inc:658`:
    ```pascal
    if (gbool_peacemode) and (gametime > gfloat_peacetime)
       and (not _net_IsReplay) and (not _net_IsClient) then
    begin
       gbool_peacemode := false;
       // remove ptborder objects and enter wartime
    end;
    ```
[^20]: Batch rate constants - `dmscript.global:1025-1029`:
    ```pascal
    gc_settings_gamespeed_count   = 3;
    gc_settings_gamespeed_default = -1;
    gc_settings_gamespeed_0       = 7;     // slow   — 7 ticks / real second
    gc_settings_gamespeed_1       = 10;    // normal — 10 ticks / real second
    gc_settings_gamespeed_2       = 14;    // fast   — 14 ticks / real second
    //gc_settings_gamespeed_3 = 20;        // commented out; formerly ultra-fast
    ```
[^21]: AI difficulty constants - `dmscript.global:781-786`.

[^22]: Global batch constants - `dmscript.global` (constants section
    game time and frame scan, next to `gc_settings_gamespeed_*`).

[^23]: Commented out assignment `speed` to peasant -
    `lib/unit.script:1192`.
