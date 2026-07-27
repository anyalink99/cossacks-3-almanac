<a id="стартовое-расположение-и-ресурсы"></a>
# Starting Positions and Resources

[← Tables and calculations](../README.md)

This page explains how the first Peasants are arranged and where the map
generator tries to place the nearest forests and stone clusters. The exact
layout varies from match to match because of terrain shape and the random
selection of valid positions.

<a id="первые-крестьяне"></a>
## The First Peasants

With the standard starting option, **18 Peasants** appear in a **6×3** grid
with 0.75 cells between them [^1]. The entire group occupies approximately
4.5×2.25 cells, and each Peasant's position receives a small random offset.

The generator does not place natural resources inside this small area, so
the Peasants do not start inside a forest or stone cluster.

<a id="ближайшие-леса-и-камни"></a>
## Nearby Forests and Stone

The generator uses three approximate zones around each starting point:

| Zone | Approximate distance | What appears there |
| --- | ---: | --- |
| Inner | Up to 5 cells | Clear space for the starting group |
| Middle | Roughly 5–12 cells | The nearest stone and parts of forests |
| Outer | Roughly 12–22 cells | Additional forests and stone |

The generator makes several attempts to place each object at a random angle
and distance. Terrain can block an attempt, so the final position may fall
outside the approximate range shown here. Gold, iron, and coal deposits use
a separate placement algorithm.

For more detail, see [Random-map generation](../../recon/world/map/map_generation_pipeline.md)
and [Estimated map resources](map_resources.md).

<a id="варианты-стартовых-ресурсов"></a>
## Starting Resource Presets

The lobby offers ready-made combinations of starting troops and resources.
The table lists the current entry for each option, using the names shown in
the English game localization.

| Preset | Food | Wood | Stone | Gold | Iron | Coal |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| (Template—not selectable) | 0 | 0 | 0 | 0 | 0 | 0 |
| Default | 0 | 0 | 0 | 0 | 0 | 0 |
| Army | 1000 | 0 | 0 | 0 | 0 | 0 |
| Big Army | 20000 | 0 | 0 | 0 | 0 | 0 |
| Huge Army | 20000 | 0 | 0 | 0 | 6000 | 9000 |
| Army of Peasants | 20000 | 0 | 0 | 0 | 6000 | 9000 |
| Different Nations | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 |
| Towers | 20000 | 0 | 0 | 0 | 6000 | 9000 |
| Cannons | 20000 | 0 | 0 | 1000 | 6000 | 9000 |
| Cannons and Howitzers | 20000 | 0 | 0 | 1000 | 6000 | 9000 |
| 18th Century Barracks | 65000 | 2000 | 2000 | 15000 | 6000 | 9000 |
| Barrack17 | 5000 | 1000 | 1000 | 2500 | 3000 | 3000 |
| Village | 1000 | 1000 | 1000 | 1000 | 2500 | 2500 |
| Logcabins | 0 | 0 | 0 | 0 | 2500 | 2500 |
| Union | 1000 | 0 | 0 | 0 | 0 | 0 |

Some presets also add buildings and troops. Their composition depends on
the selected nation; the complete list of option names is available in the
[match settings reference](lobby_settings.md).

<a id="источники"></a>
## Sources

All links are relative to `data/scripts/` in the Cossacks 3 installation.

[^1]: Starting Peasant placement —
      `common.inc/dogenerate.inc:1231-1281`.
