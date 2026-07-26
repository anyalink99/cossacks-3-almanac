<a id="recon-настройки-лобби--что-движок-делает-с-каждой-опцией"></a>
<a id="как-настройки-матча-влияют-на-игру"></a>
# How Match Settings Affect the Game

[← How the game works](../../README.md)

This document is **handwritten reverse-engineering** of how the Cossacks 3 engine works
reacts to the player's choice in the lobby. Values and labels are not included here - for
There are two truths to this:

- **[`docs/reports/map/lobby_settings.md`](../../../reports/map/lobby_settings.md)** —
  ready-made directory of all options (names from the locale, numeric values,
  default values).
- **[`derived/game_settings.json`](../../../../derived/game_settings.json)** - the same
  most in machine-readable form, for the editor and tools.

Here is only what cannot be seen in the table: which script functions read
these values, what flags are set, what game mechanics
turn on. All links to code and Pascal blocks are collected in the section
[Sources](#sources) at the end of the document.

<a id="1-структура-tmapsettings"></a>
## 1. Structure `TMapSettings`

The root structure contains two fields: `gen` and `additional` [^1]. `gen` decides
**how** the map is drawn (relief, size, resources, season), `additional` - **by
what rules** the game follows (peacetime, limit, speed, assistant). Contents
saved in save via `_misc_SaveLanRoomData` [^2].

`TMapSettingsGen` contains RNG keys (`randkey0` for arrangement, `randkey1`
for relief), `mapsize` (0..3), `terraintype` (0..9), `relieftype` (0..5),
`resourcestart` (0..3), `resourcemines` (0..2), `season` (0..3) [^3].

`TMapSettingsAdditional` contains `activeoption`, `startingunits`, `balloon`,
`cannons`, `peacetime`, `century18`, `capture`, `marketdip`, `teams`,
`autosave`, `limit`, `gamespeed`, `adviserassistant` [^4].

Numerical values and human names - in
[`reports/map/lobby_settings.md`](../../../reports/map/lobby_settings.md). Here - what
This is what the engine reads.

<a id="2-что-движок-делает-с-gen-параметрами"></a>
## 2. What the engine does with `gen` parameters

| Field | Where is it used | What does |
|---|---|---|
| `mapsize` | [^5] | Specifies `Width × Height` maps in tiles (square map). Affects the placement density and `prob*` modifiers [^6]. |
| `terraintype` | [^7] | Selects the mask table (`data/gen/terrainmasks/`) for the base map image. `terraintype ∈ {2,3,4}` (Peninsulas / Islands / Several Continents) includes “sea” waters - without `por` (port) they cannot be reached. |
| `relieftype` | [^8] | Selects the density of mountains/hills (`mnt`, `hgh`). On `relieftype = 3` (“Highlands”) the density of mountains is maximum - there are fewer flat areas for farms and warehouses. |
| `resourcestart` | [^9] | Cycle of 6 resources - each player is given a starting amount of **each** of 6 resources. Values according to `resourcestart`: 1000 / 4000 / 5000 / 1,000,000. |
| `resourcemines` | [^10] | Substituted in `minesdensity` - controls the mine placement phase. See [`map_generation_pipeline.md`](map_generation_pipeline.md) §8 (3 rounds × 3 types = 9 deposits per player for Tiny + Rich). |
| `season` | [^11] | `bDesert := (season = 3)`. This flag switches the set of pattern types (`forests_pinefir_*` → `desert_forests_*`, etc.). Other seasons only change textures. |
| `randkey0` / `randkey1` | [^12] | RNG keys. `randkey1` is used for relief (`SetRandomKey`), `randkey0` is used for placement. **The triple `(inputbitmap, randkey0, randkey1)` determines the map** - so replays reproduce the same map. More details - [`map_generation_pipeline.md` §12](map_generation_pipeline.md#12-seed-space). |

> **`foreststype` and Land.** The player selects `foreststype` in the lobby, but
> `terraintype = 0` (Land) the engine immediately rewrites it as `0` [^13].
> On non-Land maps the selection works.

<a id="3-что-движок-делает-с-additional-параметрами"></a>
## 3. What does the engine do with `additional` parameters
<a id="31-startingunits--стартовая-армия"></a>
### 3.1 `startingunits` - starting army

The specific set of units/buildings for each option is read from
`data/game/var/startingsettings.cfg`. Fields: `addresources` (additional resources),
`countries` (arrangement legend: `P` = peasant, `X` = infantryman, `B` =
drummer, `O` = officer, `Q`/`W` = mission buildings, etc.).

> **The base 18 peasants always appear.** Regardless of engine choice
> calls `CreateStartPointPeasants` and places **18 peasants** on the grid
> 6x3 around the starting point with a radius of 0.75 tiles [^14]. Even on "Po"
> by default” the player has 18 peasants at once.

<a id="32-peacetime--как-устроен-мир"></a>
### 3.2 `peacetime` - how the world works

Function `_misc_GetPeaceTime` decodes the index into game minutes and multiplies by
60 to get g-seconds [^15]:

| `ind` | Game minutes |
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

Minutes - **game**: at fast speed (`gamespeed = 2`) one game minute
≈ 42.9 real seconds, and a 10-minute world lasts ≈ 7 real minutes.

When generating the map [^16]:

- `gbool_peacemode := (peacetime <> 0)` - the flag is turned on if any
  non-zero preset.
- `gfloat_peacetime := _misc_GetPeaceTime(ind)` - specific value in
  game secondsah.
- `SetupBorderObjects` creates visual "boundaries" around each player.

While `gbool_peacemode = True`:

- **Searching for enemies is prohibited.** `_unit_SearchEnemy*` is checked for `bpeacetime`
  - if `True`, no unit finds enemies and attacks [^17].
- **Territory ownership grid.** `_misc_IsCorrectScanCellOwner` returns
  `True` only for drawn and own cells - enemies cannot enter
  your territory [^18].
- **Capture buildings are prohibited** on foreign territory.

Each Nothing-tick server checks for the end of the world [^19]: if
`gbool_peacemode = True` and `gametime > gfloat_peacetime`, and the batch is not
replay and not a client - the flag is reset, `ptborder` objects are deleted, and the batch
goes into military mode. The decision is made only by the server (host in MP,
single-player). In replays and clients, the state comes through a sync-event.

<a id="33-century18--переход-в-18-век"></a>
### 3.3 `century18` — advance to the 18th century

| Meaning | What does |
|---|---|
| 0 | Standard: upgrade `<nat>cen.1` available after aca + tem + art (with regular price). |
| 1 | Upgrade `cen.1` disabled - 18th century is not available in this batch. |
| 2 | The player starts in the 18th century - `cen.1` has already been researched. |

Nations without 18th century. (`ukr` Ukraine, `tur` Turkey, `alg` Algeria) option “Immediately”
useless - they do not have an upgrade from `cen.1` to `country.script`. See
[`reference/05_upgrades/README.md`](../../../reference/05_upgrades/README.md).

<a id="34-capture--правила-захвата"></a>
### 3.4 `capture` - capture rules

Capture geometry (radii, who is captured, who is not, towers, walls) - in
[`recon/world/economy/capture_mechanics.md`](../economy/capture_mechanics.md).

Option `capture` in the lobby only enables/disables target classes: `1` disables
capture of peasants, `2` also of City centers, `3` leaves only capture
artillery. The verification algorithm itself is the same.

<a id="35-marketdip--рынок-и-дипцентр"></a>
### 3.5 `marketdip` - market and deep center

`value = 4` (“Dear Mercenaries”) multiplies the hiring price by
`gc_gameplay_expensivemercskoef = 3`. Details about the economics of the diplomatic center are in
[`recon/systems/mercenaries_diplomacy.md`](../../systems/mercenaries_diplomacy.md).

<a id="36-gamespeed--скорость-партии"></a>
### 3.6 `gamespeed` — game speed

Constants `gc_settings_gamespeed_*` set the number of ticks per real second:
`slow = 7`, `normal = 10`, `fast = 14`; fourth value `20` (ultra-fast) in
code commented out [^20]. `gc_time_to_frames = 32` always (32 frames in one
game second); only the real-time factor changes.

| Speed | Ticks / real second | Multiplier | Real time per 1 game second |
|---:|---:|---:|---:|
| 0 (slow) | 7 | ×0.7 | 1.43 real seconds |
| 1 (normal) | 10 | ×1.0 | 1.00 real seconds |
| 2 (fast) | 14 | ×1.4 | 0.71 real seconds |

<a id="37-limit--лимит-населения"></a>
### 3.7 `limit` - population limit

This is the **global ceiling on top** of the local building limit:
```
pop_cap = cen × 100 + bar × 150 + ba2 × 250 + hou × 25
```
Global ceiling (`limit = 1..8` → 500 / 750 / 1000 / 1500 / 2200 / 3000 /
5000 / 8000) is never exceeded, even if the farm bonus allows more.

UI writes the value via `randommap.settings.limit.custom = "%value% units"` -
it is substituted by `_misc_GetLimitText`.

<a id="38-adviserassistant--помощник"></a>
### 3.8 `adviserassistant` - assistant

Contextual clues in the corner of the screen. Does not affect the simulation - only UI.

<a id="4-сложность-ии--gcplayerdifficulty"></a>
## 4. AI difficulty - `gc_player_difficulty_*`

The constants `gc_player_difficulty_*` from `-1` to `4` [^21] are listed:

| `difficulty` | Locale (gui) | What does | Speed Multiplier |
|---:|---|---|---:|
| -1 | (none) | No AI | — |
| 0 | difficulty.1 | Easy / Easy | 0.30 |
| 1 | difficulty.1 | Normal / Normal | 0.50 |
| 2 | difficulty.2 | Hard / Heavy | 0.75 |
| 3 | difficulty.3 | Very Hard / Very heavy | 1.00 |
| 4 | difficulty.4 | Impossible / Impossible | 1.25 |

The multiplier is applied via `_player_GetDifficultyKoef` to the speed
built/hired by AI. **AI does not receive starting resources** for any
complexity. More details - [`recon/systems/ai_behavior.md`](../../systems/ai_behavior.md).

See also [`recon/systems/mercenaries_diplomacy.md`](../../systems/mercenaries_diplomacy.md) §3 - on
hard+ with `brebellion = True` chance of mercenaries moving ≈ 18.31% per tick
(significantly).

<a id="5-глобальные-константы-партии"></a>
## 5. Global batch constants

These are not lobby options, but engine constants that determine the shape of all
settings [^22].

| Constant | Meaning | What does |
|---|---:|---|
| `gc_MaxPlayerCount` | 12 | Maximum players (including neutral and mercenary slot). |
| `gc_MaxObjCount` | 32000 | Hard cap of units on the map (all players together). |
| `gc_time_to_frames` | 32 | Frames in one game second. |
| `gc_buildtime_modifier` | 10 | Additional multiplier **buildings only**: real time in g-seconds = `frames × 10 / 32`. Units have no multiplier. |
| `gc_resource_hitsneeded_food` | 22 | Strikes with a hoe before handing over food. |
| `gc_resource_hitsneeded_wood` | 14 | Strikes with an ax until wood is delivered. |
| `gc_resource_hitsneeded_stone` | 20 | Strikes with a pickaxe until hitting the stone. |
| `gc_obj_resource_portion_food` | 45 | Food per flight at `eff = 100`. |
| `gc_obj_resource_portion_wood` | 28 | Trees per flight at `eff = 100`. |
| `gc_obj_resource_portion_stone` | 40 | Stone per flight at `eff = 100`. |
| `gc_obj_speed_peasant` | 40 | The declared speed of the peasant - but in the script the assignment is commented out [^23] (see [`recon/world/economy/peasant_extraction.md`](../economy/peasant_extraction.md) §9). |

<a id="6-победа-и-поражение"></a>
## 6. Victory and defeat

See separate document - [`recon/systems/victory_conditions.md`](../../systems/victory_conditions.md).
Briefly: victory = “only one team left”; `farmused = 0` ⇒ defeat,
but `farmused` does not fall to 0 while there is at least one peasant **or** Urban
center There are no Wonder victories in C3, the score is accumulated only for statistics.

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
