<a id="настройки-лобби--справочник-значений"></a>
<a id="настройки-матча"></a>
# Match settings

[← Tables and calculations](../README.md)

Canonical names for every lobby setting, together with a short explanation of
what it changes. Internal values are included only to match settings against
replays and game files.

For the hidden behavior behind these options, see
[How Match Settings Affect the Game](../../recon/world/map/game_settings.md).

<a id="структура"></a>
<a id="карта-и-природные-ресурсы"></a>
## Map and natural resources

<a id="генератор-карты--gmapsettingsgen"></a>
<a id="правила-партии"></a>
<a id="mapsize--размер-карты"></a>
<a id="стартовая-армия-startingunits"></a>
<a id="размер-карты-mapsize"></a>
### Map size (`mapsize`)

| Meaning | Size, tiles | English label | Russian label |
| :---: | --- | --- | --- |
| 0 | 320 | Standard | Standard |
| 1 | 480 | Big | Big |
| 2 | 640 | Huge | Huge |
| 3 | 256 | Tiny | Little |

The map is square `tiles × tiles`. The game UI does not show labels (the values are protected by [^2]).

<a id="terraintype--тип-ландшафта-и-воды"></a>
<a id="монгольфьеры-balloon"></a>
<a id="тип-ландшафта-и-воды-terraintype"></a>
### Terrain and water (`terraintype`)

| Meaning | English label | Russian label |
| :---: | --- | --- |
| 0 | Land | Land |
| 1 | Mediterranean | Mediterranean |
| 2 | Peninsulas | Peninsulas |
| 3 | Islands | Islands |
| 4 | Several Continents | Several Continents |
| 5 | Single Continent | Single Continent |
| 6 | Lakes | Lakes |
| 7 | Coast | Coast |
| 8 | Rivers | Rivers |
| 9 | Without water | Without water |

Labels from `gui.txt @randommap.terraintype.*`. The values of `2..4` (`Peninsulas` / `Islands` / `Continents`) are checked by the engine in `_misc_HasMaritime` [^3] - these maps have “sea” waters, access to them requires a port.

<a id="relieftype--рельеф"></a>
<a id="пушки-башни-и-стены-cannons"></a>
<a id="рельеф-relieftype"></a>
### Relief (`relieftype`)

| Meaning | English label | Russian label |
| :---: | --- | --- |
| 0 | Plain | Plain |
| 1 | Low Mountains | Low Mountains |
| 2 | High Mountains | High Mountains |
| 3 | Highlands | Highlands |
| 4 | Plateaus | Plateaus |
| 5 | Desert | Desert |

Default `relieftype = 3` (“Highlands”) [^4].

<a id="resourcestart--стартовые-ресурсы-у-игроков"></a>
<a id="время-мира-peacetime"></a>
<a id="стартовые-ресурсы-resourcestart"></a>
### Starting resources (`resourcestart`)

| Meaning | For each resource | English label | Russian label |
| :---: | --- | --- | --- |
| 0 | 1000 | Normal | Normal |
| 1 | 4000 | Rich | Rich |
| 2 | 5000 | Thousands | Thousands |
| 3 | 1000000 | Millions | Millions |

All 6 resources (food / wood / stone / gold / iron / coal) receive the same starting amount. Default = 2 (“Thousands”, 5,000 each) [^5].

<a id="resourcemines--плотность-месторождений"></a>
<a id="переход-в-xviii-век-century18"></a>
<a id="количество-месторождений-resourcemines"></a>
### Resource deposits (`resourcemines`)

| Meaning | English label | Russian label |
| :---: | --- | --- |
| 0 | Poor | Poor |
| 1 | Medium | Medium |
| 2 | Rich | Rich |

Default `resourcemines = 1` (“Medium”) [^6]. The specific numbers of mines per level are in [map resource estimates](map_resources.md) and in [map generation](../../recon/world/map/map_generation_pipeline.md).

<a id="season--сезон"></a>
<a id="правила-захвата-capture"></a>
<a id="сезон-season"></a>
### Season (`season`)

| Meaning | English label | Russian label |
| :---: | --- | --- |
| 0 | Summer | Summer |
| 1 | Autumn | Autumn |
| 2 | Winter | Winter |
| 3 | Desert | Desert |

There are no labels in `gui.txt` - the UI is hardcoded. The only mechanical effect is `season = 3` (“Desert”) force `bDesert = True` [^7]; engine uses a different set of pattern types (`desert_*` instead of the usual forests and stones).

<a id="правила-игры--gmapsettingsadditional"></a>
<a id="сложность-компьютера"></a>
## Match rules

<a id="startingunits--стартовая-армия"></a>
<a id="сложность-difficulty"></a>
### Starting army (`startingunits`)
| Meaning | English label | Russian label |
| :---: | --- | --- |
| 0 | Default | Default |
| 1 | Army | Army |
| 2 | Big Army | Big Army |
| 3 | Huge Army | Huge Army |
| 4 | Army of Peasants | Army of Peasants |
| 5 | Different Nations | Different Nations |
| 6 | Towers | Towers |
| 7 | Cannons | Cannons |
| 8 | Cannons and Howitzers | Cannons and Howitzers |
| 9 | 18th Century Barracks | 18th Century Barracks |
| 10 | Barrack17 | Barracks 17th century. |
| 11 | Village | Village |
| 12 | Logcabins | Log houses |
| 13 | Union | Union |

A specific set of units for each option is in `data/game/var/startingsettings.cfg` (`addresources`, `countries`).

> Regardless of the choice, the engine always calls `CreateStartPointPeasants` [^8] and places **18 peasants** in a 6x3 grid around the starting point. Even on `startingunits = 0` (“Default”) the player has 18 peasants at once.

<a id="balloon--монгольфьеры"></a>
### Balloons (`balloon`)

| Meaning | English label | Russian label |
| :---: | --- | --- |
| 0 | Default | Default |
| 1 | No Balloons | No Balloons |
| 2 | Balloons | Balloons |

A hot air balloon is a special unit that provides visibility at high altitudes.

<a id="cannons--пушки-башни-и-стены"></a>
### Cannons, towers, and walls (`cannons`)

| Meaning | English label | Russian label |
| :---: | --- | --- |
| 0 | Default | Default |
| 1 | No Cannons, Towers and Walls | No Cannons, Towers and Walls |
| 2 | Expensive Cannons | Expensive Cannons |

The option “Expensive Cannons” increases the prices of guns through an upgrade - read the exact multipliers in `country.script` (artillery upgrades section).

<a id="peacetime--время-мира"></a>
### Peace time (`peacetime`)

| Meaning | Minutes (game) | g-seconds | English label | Russian label |
| :---: | --- | --- | --- | --- |
| 0 | 0 | 0 | No Peace Time | No Peace Time |
| 1 | 10 | 600 | 10 min | 10 min |
| 2 | 20 | 1200 | 20 min | 20 min |
| 3 | 30 | 1800 | 30 min | 30 min |
| 4 | 45 | 2700 | 45 min | 45 min |
| 5 | 60 | 3600 | 60 min | 60 min |
| 6 | 90 | 5400 | 1.5 hours | 1.5 hours |
| 7 | 120 | 7200 | 2 hours | 2 hours |
| 8 | 180 | 10800 | 3 hours | 3 hours |
| 9 | 240 | 14400 | 4 hours | 4 hours |
| 11 | 15 | 900 | 15 min | 15 min |

Minutes are **game minutes**. At fast speed (`gamespeed = 2`, ×1.4) one game minute = 60 / 1.4 ≈ 42.9 real seconds: a 10-minute world lasts ≈ 7 real minutes. The value of `value = 11` (15 minut) lies between `1` and `2` - historical unevenness; movement to the end of the table.

Details of the mechanics (how the engine blocks the search for enemies, unoccupied cells, the transition from peace to war) are in [match settings](../../recon/world/map/game_settings.md#peacetime--как-устроен-мир).

<a id="century18--переход-в-18-век"></a>
### Advancing to the 18th century (`century18`)

| Meaning | English label | Russian label |
| :---: | --- | --- |
| 0 | Default | Default |
| 1 | Never | Never |
| 2 | Immediately | Immediately |

On 17th century-only nations (Ukraine, Turkey, Algeria) the option “Immediately” is useless - they do not have the `<nat>cen.1` upgrade (“Transition to the 18th century”).

<a id="capture--правила-захвата"></a>
### Capture rules (`capture`)

| Meaning | English label | Russian label |
| :---: | --- | --- |
| 0 | Default | Default |
| 1 | No Capturing Peasants | No Capturing Peasants |
| 2 | No Capturing Peasants or Centers | No Capturing Peasants or Centres |
| 3 | Artillery Only | Artillery Only |

Capture geometry (radii, who is captured and who is not) - in [building capture](../../recon/world/economy/capture_mechanics.md).

<a id="marketdip--рынок-и-дипцентр"></a>
<a id="рынок-и-дипломатический-центр-marketdip"></a>
### Market and Diplomatic Center (`marketdip`)

| Meaning | English label | Russian label |
| :---: | --- | --- |
| 0 | Default | Default |
| 1 | Without dip. center | Without dip. center |
| 2 | Without market | Without market |
| 3 | Without both | Without both |
| 4 | Expensive Mercenaries | Dear mercenaries |

Option `value = 4` (“Dear Mercenaries”) multiplies the hiring price in the deep center by `gc_gameplay_expensivemercskoef = 3`. Details about mercenaries are in [mercenaries and diplomacy](../../recon/systems/mercenaries_diplomacy.md).

<a id="teams--расположение-союзников"></a>
<a id="расположение-союзников-teams"></a>
### Ally placement (`teams`)

| Meaning | English label | Russian label |
| :---: | --- | --- |
| 0 | Default | Default |
| 1 | Nearby | Nearby |

With `teams = 1`, the team starts in neighboring positions, and not scattered across the map.

<a id="limit--лимит-населения"></a>
<a id="лимит-населения-limit"></a>
### Population limit (`limit`)

| Meaning | Units | English label | Russian label |
| :---: | --- | --- | --- |
| 0 | — | Without limitation | Without limitation |
| 1 | 500 | 500 units | 500 units |
| 2 | 750 | 750 units | 750 units |
| 3 | 1000 | 1000 units | 1000 units |
| 4 | 1500 | 1500 units | 1500 units |
| 5 | 2200 | 2200 units | 2200 units |
| 6 | 3000 | 3000 units | 3000 units |
| 7 | 5000 | 5000 units | 5000 units |
| 8 | 8000 | 8000 units | 8000 units |

This is the **global ceiling on top of** the local building-by-building limit: `pop_cap = cen × 100 + bar × 150 + ba2 × 250 + hou × 25`. The global cap is never exceeded, even if the farm bonus allows more.

<a id="gamespeed--скорость-партии"></a>
<a id="скорость-партии-gamespeed"></a>
### Game speed (`gamespeed`)

| Meaning | Ticks/real second | Multiplier to norm | English label | Russian label |
| :---: | --- | --- | --- | --- |
| 0 | 7 | 0.7 | Slow | Slowly |
| 1 | 10 | 1.0 | Normal | Normal |
| 2 | 14 | 1.4 | Fast | quickly |

`gc_time_to_frames = 32` for all speeds (32 frames in one game second) - only the real-time factor changes. Slot `value = 3` (×2.0) existed, but is commented out in the current version.

<a id="adviserassistant--помощник"></a>
<a id="помощник-adviserassistant"></a>
### Adviser assistant (`adviserassistant`)

| Meaning | English label | Russian label |
| :---: | --- | --- |
| 0 | Default | Default |
| 1 | Without adviser | Without adviser |

Contextual clues in the corner of the screen. Does not affect the simulation - only UI.

<a id="сложность-ии--gcplayerdifficulty"></a>
## Computer opponent

<a id="difficulty--сложность"></a>
### Difficulty (`difficulty`)

| Meaning | Speed Multiplier | English label | Russian label |
| :---: | --- | --- | --- |
| 0 | 0.3 | Easy | Easy |
| 1 | 0.5 | Normal | Normal |
| 2 | 0.75 | Hard | Difficult |
| 3 | 1.0 | Very Hard | Very difficult |
| 4 | 1.25 | Impossible | Impossible |

AI players only. The “advantage” of difficulty is a multiplier to the speed of construction/hiring (`koef`), AI **does not receive** starting resources on any difficulty. AI behavior is discussed in [computer-player behavior](../../recon/systems/ai_behavior.md).

<a id="значения-по-умолчанию"></a>
## Default values

From [^9] (for `gen`) and general engine behavior (for `additional`):

| Field | Default |
| --- | --- |
| `settings.gen.mapsize` | `0` |
| `settings.gen.terraintype` | `0` |
| `settings.gen.relieftype` | `3` |
| `settings.gen.resourcestart` | `2` |
| `settings.gen.resourcemines` | `1` |
| `settings.gen.season` | `0` |
| `settings.additional.startingunits` | `0` |
| `settings.additional.balloon` | `0` |
| `settings.additional.cannons` | `0` |
| `settings.additional.peacetime` | `0` |
| `settings.additional.century18` | `0` |
| `settings.additional.capture` | `0` |
| `settings.additional.marketdip` | `0` |
| `settings.additional.teams` | `0` |
| `settings.additional.limit` | `0` |
| `settings.additional.gamespeed` | `2` |
| `settings.additional.adviserassistant` | `0` |

---

**Cm. also:**

- [match settings](../../recon/world/map/game_settings.md) - engine behavior for each option (peacetime, peace mode, captureradius, ...).
- [`derived/game_settings.json`](../../../derived/game_settings.json) - the same in machine-readable form.
- [map generation](../../recon/world/map/map_generation_pipeline.md) - what exactly does the map generator do with these values.


<a id="источники"></a>
## Sources

All links are relative to `data/scripts/` in the Cossacks 3 installation.

[^1]: definition of `TMapSettings` (`gMap.settings`) - `lib/classes.script:85-88`.

[^2]: hardcode of sizes `mapsize` in tiles - `lib/miscext2.script:19-26`.

[^3]: `_misc_HasMaritime` - checking terrain-sea options - `lib/misc.script:5466`.

[^4]: default `relieftype = 3` (Highlands) - `common.inc/initmap.inc:29`.

[^5]: default `resourcestart = 2` (Thousands) - `common.inc/initmap.inc:30`.

[^6]: default `resourcemines = 1` (Medium) - `common.inc/initmap.inc:31`.

[^7]: forcing `bDesert := True` when `season = 3` is `common.inc/dogenerate.inc:4`.

[^8]: `CreateStartPointPeasants` - arrangement of 18 peasants 6x3 - `common.inc/dogenerate.inc:1231-1281`.

[^9]: block defaults `gen` (relieftype, resourcestart, resourcemines) - `common.inc/initmap.inc:29-31`.
