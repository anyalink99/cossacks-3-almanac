<a id="recon-настройки-лобби--что-движок-делает-с-каждой-опцией"></a>
<a id="как-настройки-матча-влияют-на-игру"></a>
# How Match Settings Affect the Game

[← How the game works](../../README.md)

This article explains what the pre-match options actually change: which ones
rebuild the map, which act only during play, and which restrictions are not
obvious from their lobby labels.

Canonical labels, numeric values, and defaults are listed in the
[match-settings reference](../../../reports/map/lobby_settings.md). This
article explains the practical effects that are not obvious from the table.
Internal fields, functions, and the saved-record layout are kept under
[Technical details](#technical-details).

<a id="1-структура-tmapsettings"></a>
<a id="1-как-хранятся-настройки-матча"></a>
<a id="быстрый-ориентир"></a>
## Quick guide

- **Map size, terrain type, relief, season, and deposits** affect the
  generated map and do not change after the match begins.
- **Starting army and resources** define the opening position. The Default
  starting-army preset creates eighteen Peasants; other presets replace that
  default group with their own units and buildings.
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
| Terrain type | Selects the map foundation. Peninsulas, Islands, and Continents include navigable water, so ships and Ports are available [^7]. |
| Relief | Controls mountain and hill density. Highlands leave less flat ground for Farms and Storehouses [^8]. |
| Starting resources | Gives every player the selected amount of each of the six resources: 1,000, 4,000, 5,000, or 1,000,000 [^9]. |
| Mineral deposits | Changes how many placement passes are attempted. A Tiny Rich map can use three passes for each of three deposit types [^10]. See [How mineral deposits are placed](map_generation_pipeline.md#8-how-mineral-deposits-are-placed). |
| Season | Desert replaces normal environment sets with desert sets; other seasons mainly change textures [^11]. |
| Generation keys | Together with the base mask, uniquely determine terrain and object placement [^12]. |

> **Forest type.** On Land maps, the selected forest type has no effect [^13].
> The generator uses the mixed conifer set.

<a id="3-что-движок-делает-с-additional-параметрами"></a>
<a id="3-дополнительные-правила-партии"></a>
<a id="дополнительные-правила-партии"></a>
## Additional match rules
<a id="31-startingunits--стартовая-армия"></a>
<a id="31-starting-army"></a>
<a id="31-стартовая-армия-startingunits"></a>
<a id="31-стартовая-армия"></a>
<a id="стартовая-армия"></a>
### Starting army

The Default preset creates **18 Peasants** in a 6 × 3 grid around the starting
position, 0.75 cells apart [^14]. Other presets replace this group with their
own units and buildings. The full list is in the
[match-settings reference](../../../reports/map/lobby_settings.md#starting-army-startingunits).

<a id="32-peacetime--как-устроен-мир"></a>
<a id="32-peace-time"></a>
<a id="peacetime--как-устроен-мир"></a>
<a id="32-время-мира-peacetime"></a>
<a id="32-время-мира"></a>
<a id="время-мира"></a>
### Peace time

The lobby offers no peace time or durations of 10, 15, 20, 30, 45, 60, 90,
120, 180, and 240 game minutes [^15].

These are **game minutes**. At Fast speed, one game minute
lasts about 42.9 real seconds, so ten minutes of peace last about seven real
minutes.

While peace time is active:

- **units do not acquire or attack enemies** [^17];
- **foreign territory is closed**: troops can enter only neutral and owned
  cells [^18];
- **Buildings cannot be captured** on foreign territory.

Territory boundaries remain visible on the map. When the selected duration
expires, they disappear and normal combat begins [^16] [^19].

<a id="33-century18--переход-в-18-век"></a>
<a id="33-advance-to-the-18th-century"></a>
<a id="33-переход-в-xviii-век-century18"></a>
<a id="33-переход-в-xviii-век"></a>
<a id="переход-в-xviii-век"></a>
### Advance to the 18th century

| Lobby option | Effect |
|---|---|
| Default | **Progress to the 18th Century** becomes available after an Academy, Cathedral, and Artillery Depot have been built. |
| Never | Advancing to the 18th century is disabled. |
| Immediately | The player begins with the advance already completed. |

For Ukraine, Turkey, and Algeria, Immediately has no effect because those
nations do not advance to the 18th century. See
[upgrades](../../../reference/05_upgrades/README.md).

<a id="34-capture--правила-захвата"></a>
<a id="34-capture-rules"></a>
<a id="34-правила-захвата-capture"></a>
<a id="34-правила-захвата"></a>
<a id="правила-захвата"></a>
### Capture rules

For capture radii, eligible targets, towers, and walls, see
[building capture](../economy/capture_mechanics.md).

No Capturing Peasants, No Capturing Peasants or Centres, and Artillery Only
change only the eligible target classes. Capture distances and all other
checks remain unchanged.

<a id="35-marketdip--рынок-и-дипцентр"></a>
<a id="35-market-and-diplomatic-center"></a>
<a id="35-рынок-и-дипломатический-центр-marketdip"></a>
<a id="35-рынок-и-дипломатический-центр"></a>
<a id="рынок-и-дипломатический-центр"></a>
### Market and Diplomatic Center

Expensive Mercenaries triples recruitment prices. The lobby can also disable
the Market, the Diplomatic Center, or both. Details are in
[mercenaries and diplomacy](../../systems/mercenaries_diplomacy.md).

<a id="36-gamespeed--скорость-партии"></a>
<a id="36-game-speed"></a>
<a id="36-скорость-партии-gamespeed"></a>
<a id="36-скорость-партии"></a>
<a id="скорость-партии"></a>
### Game speed

Game speed changes the relationship between game time and real time, not the
internal duration of an action [^20].

| Speed | Multiplier | Real time per game second |
|---|---:|---:|
| Slow | ×0.7 | 1.43 real seconds |
| Normal | ×1.0 | 1.00 real second |
| Fast | ×1.4 | 0.71 real seconds |

<a id="37-limit--лимит-населения"></a>
<a id="37-population-limit"></a>
<a id="37-лимит-населения-limit"></a>
<a id="37-лимит-населения"></a>
<a id="лимит-населения"></a>
### Population limit

This is a **global ceiling applied after** the population provided by buildings:

**Town Halls × 100 + Barracks, 17th century × 150 + Barracks, 18th century ×
250 + Houses × 25.**

The selected lobby ceiling—500, 750, 1,000, 1,500, 2,200, 3,000, 5,000, or
8,000 units—cannot be exceeded even if the buildings provide more capacity.

<a id="38-adviserassistant--помощник"></a>
<a id="38-adviser"></a>
<a id="38-помощник-adviserassistant"></a>
<a id="38-помощник"></a>
<a id="помощник"></a>
### Adviser

Contextual hints in the corner of the screen. They do not affect gameplay.

<a id="4-сложность-ии--gcplayerdifficulty"></a>
<a id="сложность-компьютерного-игрока"></a>
## Computer-player difficulty

| Difficulty | Construction and recruitment speed multiplier |
|---|---:|
| Easy | 0.30 |
| Normal | 0.50 |
| Hard | 0.75 |
| Very Hard | 1.00 |
| Impossible | 1.25 |

**The computer player receives no extra starting resources** at any
difficulty. See [computer-player behavior](../../systems/ai_behavior.md).

<a id="6-победа-и-поражение"></a>
<a id="победа-и-поражение"></a>
## Victory and defeat

See
[Victory, Defeat, and the End of a Match](../../systems/victory_conditions.md).
In a standard match, the last surviving team wins. Cossacks 3 has no Wonder
victory, and score is used for statistics.

<a id="технические-подробности"></a>
## Technical details

`TMapSettings` is split into map generation (`gen`) and match rules
(`additional`) [^1]. `_misc_SaveLanRoomData` writes the settings to a saved
game [^2].

The machine-readable catalog is
[`derived/game_settings.json`](../../../../derived/game_settings.json).

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

<a id="реализация-отдельных-правил"></a>
### Implementation notes

- Starting-army presets are read from `data/game/var/startingsettings.cfg`.
  `CreateStartPointPeasants` creates the default group. In special layouts,
  `P` means Peasant, `X` infantryman, `B` Drummer, `O` Officer, and `Q` and
  `W` mission buildings [^14].
- `_misc_GetPeaceTime` converts the internal value to game minutes and seconds
  [^15]. `gbool_peacemode` and `gfloat_peacetime` store the state and end time,
  while `SetupBorderObjects` creates the boundaries [^16]. Enemy search checks
  `bpeacetime` [^17], and `_misc_IsCorrectScanCellOwner` restricts entry into
  foreign territory [^18]. The authoritative side confirms the end of peace
  time and synchronizes it with clients and replays [^19].
- For the 18th century, `century18 = 0/1/2` means Default, Never, and
  Immediately. The upgrade uses a nation-specific internal ID of the form
  `<nat>cen.1`.
- `capture = 1/2/3` disables Peasant capture, then Town Hall capture, or leaves
  only capturable artillery.
- `marketdip = 4` applies
  `gc_gameplay_expensivemercskoef = 3`.
- `slow`, `normal`, and `fast` run 7, 10, and 14 ticks per real second.
  `gc_time_to_frames = 32` remains unchanged [^20].
- Local population capacity is stored as
  `cen × 100 + bar × 150 + ba2 × 250 + hou × 25`; `limit = 1..8` applies the
  global ceilings from 500 to 8,000.
- `_player_GetDifficultyKoef` applies the
  `gc_player_difficulty_*` coefficients to computer-player construction and
  recruitment speed [^21].

<a id="5-глобальные-константы-партии"></a>
<a id="глобальные-константы-партии"></a>
### Global match constants

These are engine constants rather than lobby options. They define the common
framework within which the settings operate [^22].

| Constant | Value | Meaning |
|---|---:|---|
| `gc_MaxPlayerCount` | 12 | Maximum players (including neutral and mercenary slot). |
| `gc_MaxObjCount` | 32000 | Hard cap of units on the map (all players together). |
| `gc_time_to_frames` | 32 | Frames in one game second. |
| `gc_buildtime_modifier` | 10 | Additional multiplier **for buildings only**: game seconds = `frames × 10 / 32`. Units do not use it. |
| `gc_resource_hitsneeded_food` | 22 | Strikes with a hoe before handing over food. |
| `gc_resource_hitsneeded_wood` | 14 | Strikes with an ax until wood is delivered. |
| `gc_resource_hitsneeded_stone` | 20 | Pickaxe strikes before delivering stone. |
| `gc_obj_resource_portion_food` | 45 | Food delivered per trip at `eff = 100`. |
| `gc_obj_resource_portion_wood` | 28 | Wood delivered per trip at `eff = 100`. |
| `gc_obj_resource_portion_stone` | 40 | Stone delivered per trip at `eff = 100`. |
| `gc_obj_speed_peasant` | 40 | The declared Peasant speed, although the script assignment is commented out [^23] (see [peasant resource gathering](../economy/peasant_extraction.md) §9). |

<a id="источники"></a>
## Sources

All references are relative to `data/scripts/` in the Cossacks 3 installation.
Line numbers refer to the current installation and should be rechecked after a
game update.

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

[^7]: Applying `terraintype` — `common.inc/dogenerate.inc:1500-1530`;
    `_misc_HasMaritime` checks for sea access in `lib/misc.script:5466`.

[^8]: Application of `relieftype` - `common.inc/dogenerate.inc:1640-1660`.

[^9]: Application `resourcestart` - `common.inc/initmapgen.inc:166-189`:
    ```pascal
    for j := 0 to gc_ResCount - 1 do
       _res_SetResToPlayerByIndex(i, j, ...);
    ```
[^10]: Applying `resourcemines` — `common.inc/dogenerate.inc:1544`, where its
    value is assigned to `minesdensity`.

[^11]: Application `season` - `common.inc/dogenerate.inc:4`:
    ```pascal
    bDesert := (season = 3);
    ```
[^12]: RNG keys `randkey0` / `randkey1` - `common.inc/generatemap.inc:142` and
    repeatedly in `common.inc/dogenerate.inc`.

[^13]: Overwriting `foreststype` on Land — `common.inc/dogenerate.inc:5-6`.

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

[^17]: Blocking enemy searches during peace time — `lib/unit.script:5516`,
    where `_unit_SearchEnemy*` checks the `bpeacetime` flag.

[^18]: Restricting access to foreign territory during peace time —
    `_misc_IsCorrectScanCellOwner` in `lib/misc.script:2424`.

[^19]: Ending peace time during a `Nothing` tick —
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

[^23]: Commented-out assignment of `speed` to the Peasant —
    `lib/unit.script:1192`.
