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
<a id="mapsize--размер-карты"></a>
<a id="размер-карты-mapsize"></a>
### Map size (`mapsize`)

| Internal value | Size, cells | Game label |
| :---: | --- | --- |
| 0 | 320 | Standard |
| 1 | 480 | Big |
| 2 | 640 | Huge |
| 3 | 256 | Tiny |

Every map is square; its dimensions are defined directly by the game [^1].

<a id="terraintype--тип-ландшафта-и-воды"></a>
<a id="тип-ландшафта-и-воды-terraintype"></a>
### Terrain and water (`terraintype`)

| Internal value | Game label |
| :---: | --- |
| 0 | Land |
| 1 | Mediterranean |
| 2 | Peninsulas |
| 3 | Islands |
| 4 | Several Continents |
| 5 | Single Continent |
| 6 | Lakes |
| 7 | Coast |
| 8 | Rivers |
| 9 | Without water |

Peninsulas, Islands, and Several Continents contain sea water, which requires
a Shipyard for access [^2].

<a id="relieftype--рельеф"></a>
<a id="рельеф-relieftype"></a>
### Relief (`relieftype`)

| Internal value | Game label |
| :---: | --- |
| 0 | Plain |
| 1 | Low Mountains |
| 2 | High Mountains |
| 3 | Highlands |
| 4 | Plateaus |
| 5 | Desert |

Default `relieftype = 3` (“Highlands”) [^3].

<a id="resourcestart--стартовые-ресурсы-у-игроков"></a>
<a id="стартовые-ресурсы-resourcestart"></a>
### Starting resources (`resourcestart`)

| Internal value | Each resource | Game label |
| :---: | --- | --- |
| 0 | 1000 | Normal |
| 1 | 4000 | Rich |
| 2 | 5000 | Thousands |
| 3 | 1000000 | Millions |

All six resources—food, wood, stone, gold, iron, and coal—receive the same
starting amount. The default is Thousands, or 5,000 of each [^4].

<a id="resourcemines--плотность-месторождений"></a>
<a id="количество-месторождений-resourcemines"></a>
### Resource deposits (`resourcemines`)

| Internal value | Game label |
| :---: | --- |
| 0 | Poor |
| 1 | Medium |
| 2 | Rich |

The default is Medium [^5]. Estimated deposit counts are available in
[map resources](map_resources.md), while the placement process is described
in [Random-map generation](../../recon/world/map/map_generation_pipeline.md).

<a id="season--сезон"></a>
<a id="сезон-season"></a>
### Season (`season`)

| Internal value | Game label |
| :---: | --- |
| 0 | Summer |
| 1 | Autumn |
| 2 | Winter |
| 3 | Desert |

The Desert option uses a separate set of desert forests and stone patterns
[^6].

<a id="правила-игры--gmapsettingsadditional"></a>
<a id="правила-партии"></a>
## Match rules

<a id="startingunits--стартовая-армия"></a>
<a id="стартовая-армия-startingunits"></a>
### Starting army (`startingunits`)
| Internal value | Game label |
| :---: | --- |
| 0 | Default |
| 1 | Army |
| 2 | Big Army |
| 3 | Huge Army |
| 4 | Army of Peasants |
| 5 | Different Nations |
| 6 | Towers |
| 7 | Cannons |
| 8 | Cannons and Howitzers |
| 9 | 18th Century Barracks |
| 10 | Barrack17 |
| 11 | Village |
| 12 | Logcabins |
| 13 | Union |

Each option's exact units and buildings are defined in
`data/game/var/startingsettings.cfg`.

> The **18 Peasants** in a 6×3 grid appear only with the Default option [^7].
> Special starting presets replace this group with their own formations from
> `startingsettings.cfg`.

<a id="balloon--монгольфьеры"></a>
<a id="монгольфьеры-balloon"></a>
### Balloons (`balloon`)

| Internal value | Game label |
| :---: | --- |
| 0 | Default |
| 1 | No Balloons |
| 2 | Balloons |

A hot-air balloon is a special unit that provides a wide area of vision.

<a id="cannons--пушки-башни-и-стены"></a>
<a id="пушки-башни-и-стены-cannons"></a>
### Cannons, towers, and walls (`cannons`)

| Internal value | Game label |
| :---: | --- |
| 0 | Default |
| 1 | No Cannons, Towers and Walls |
| 2 | Expensive Cannons |

Expensive Cannons raises artillery prices through a special upgrade.

<a id="peacetime--время-мира"></a>
<a id="время-мира-peacetime"></a>
### Peace time (`peacetime`)

| Internal value | Game minutes | Game seconds | Game label |
| :---: | --- | --- | --- |
| 0 | 0 | 0 | No Peace Time |
| 1 | 10 | 600 | 10 min |
| 2 | 20 | 1200 | 20 min |
| 3 | 30 | 1800 | 30 min |
| 4 | 45 | 2700 | 45 min |
| 5 | 60 | 3600 | 60 min |
| 6 | 90 | 5400 | 1.5 hours |
| 7 | 120 | 7200 | 2 hours |
| 8 | 180 | 10800 | 3 hours |
| 9 | 240 | 14400 | 4 hours |
| 11 | 15 | 900 | 15 min |

These are **game minutes**. At Fast speed, one game minute lasts about
42.9 real seconds, so ten minutes of peace time lasts roughly seven real
minutes.

The transition from peace to war is explained in
[How Match Settings Affect the Game](../../recon/world/map/game_settings.md#peacetime--как-устроен-мир).

<a id="century18--переход-в-18-век"></a>
<a id="переход-в-xviii-век-century18"></a>
### Advancing to the 18th century (`century18`)

| Internal value | Game label |
| :---: | --- |
| 0 | Default |
| 1 | Never |
| 2 | Immediately |

Immediately has no effect for Ukraine, Turkey, or Algeria because those
nations cannot advance to the 18th century.

<a id="capture--правила-захвата"></a>
<a id="правила-захвата-capture"></a>
### Capture rules (`capture`)

| Internal value | Game label |
| :---: | --- |
| 0 | Default |
| 1 | No Capturing Peasants |
| 2 | No Capturing Peasants or Centres |
| 3 | Artillery Only |

See [Building capture](../../recon/world/economy/capture_mechanics.md) for
capture radii and eligibility.

<a id="marketdip--рынок-и-дипцентр"></a>
<a id="рынок-и-дипломатический-центр-marketdip"></a>
### Market and Diplomatic Center (`marketdip`)

| Internal value | Game label |
| :---: | --- |
| 0 | Default |
| 1 | Without dip. center |
| 2 | Without market |
| 3 | Without both |
| 4 | Expensive Mercenaries |

Expensive Mercenaries triples the hiring price. See
[Mercenaries and diplomacy](../../recon/systems/mercenaries_diplomacy.md)
for details.

<a id="teams--расположение-союзников"></a>
<a id="расположение-союзников-teams"></a>
### Ally placement (`teams`)

| Internal value | Game label |
| :---: | --- |
| 0 | Default |
| 1 | Nearby |

With Nearby selected, allies start in neighboring positions rather than
being scattered across the map.

<a id="limit--лимит-населения"></a>
<a id="лимит-населения-limit"></a>
### Population limit (`limit`)

| Internal value | Unit limit | Game label |
| :---: | --- | --- |
| 0 | — | Without limitation |
| 1 | 500 | 500 units |
| 2 | 750 | 750 units |
| 3 | 1000 | 1000 units |
| 4 | 1500 | 1500 units |
| 5 | 2200 | 2200 units |
| 6 | 3000 | 3000 units |
| 7 | 5000 | 5000 units |
| 8 | 8000 | 8000 units |

This is a global ceiling on top of the population capacity supplied by
Town Halls, Barracks, and Houses. The selected limit is never exceeded even
when the buildings provide more capacity.

<a id="gamespeed--скорость-партии"></a>
<a id="скорость-партии-gamespeed"></a>
### Game speed (`gamespeed`)

| Internal value | Ticks per real second | Relative to Normal | Game label |
| :---: | --- | --- | --- |
| 0 | 7 | 0.7 | Slow |
| 1 | 10 | 1.0 | Normal |
| 2 | 14 | 1.4 | Fast |

Every game second contains 32 simulation frames; only its real-world
duration changes with the speed setting.

<a id="adviserassistant--помощник"></a>
<a id="помощник-adviserassistant"></a>
### Adviser assistant (`adviserassistant`)

| Internal value | Game label |
| :---: | --- |
| 0 | Default |
| 1 | Without adviser |

This setting controls the contextual hints in the corner of the screen. It
does not affect the simulation.

<a id="сложность-ии--gcplayerdifficulty"></a>
<a id="сложность-компьютера"></a>
## Computer opponent

<a id="difficulty--сложность"></a>
<a id="сложность-difficulty"></a>
### Difficulty (`difficulty`)

| Internal value | Speed multiplier | Game label |
| :---: | --- | --- |
| 0 | 0.3 | Easy |
| 1 | 0.5 | Normal |
| 2 | 0.75 | Hard |
| 3 | 1.0 | Very Hard |
| 4 | 1.25 | Impossible |

Difficulty changes the computer player's construction and production speed.
It does **not** grant additional starting resources. See
[Computer-player behavior](../../recon/systems/ai_behavior.md) for details.

---

**See also:**

- [How Match Settings Affect the Game](../../recon/world/map/game_settings.md)
  — the behavior behind each option.
- [`derived/game_settings.json`](../../../derived/game_settings.json) — the
  same values in machine-readable form.
- [Random-map generation](../../recon/world/map/map_generation_pipeline.md)
  — how the generator uses these settings.


<a id="источники"></a>
## Sources

All links are relative to `data/scripts/` in the Cossacks 3 installation.

[^1]: Map sizes in cells — `lib/miscext2.script:19-26`.

[^2]: `_misc_HasMaritime` — maritime terrain options —
      `lib/misc.script:5466`.

[^3]: Default `relieftype = 3` (Highlands) —
      `common.inc/initmap.inc:29`.

[^4]: Default `resourcestart = 2` (Thousands) —
      `common.inc/initmap.inc:30`.

[^5]: Default `resourcemines = 1` (Medium) —
      `common.inc/initmap.inc:31`.

[^6]: Desert pattern selection when `season = 3` —
      `common.inc/dogenerate.inc:4`.

[^7]: `CreateStartPointPeasants` — placement of 18 Peasants for the Default
      start — `common.inc/dogenerate.inc:1231-1281`.
