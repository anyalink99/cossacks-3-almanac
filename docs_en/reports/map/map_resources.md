<a id="сколько-ресурсов-появляется-на-карте"></a>
# How Many Resources Appear on the Map

[← Tables and calculations](../README.md)

This page estimates the number of forests, stone deposits, and mineral
deposits produced by one commonly used set of match settings. Natural-object
counts are approximate: uneven terrain and occupied cells prevent some
objects from being placed.

<a id="настройки-расчёта"></a>
## Settings Used

| Setting | Selected value |
| --- | --- |
| Map size | **Tiny**, 256×256 cells |
| Relief | **Highlands** |
| Resource deposits | **Rich** |
| Terrain type | Land |

See [Match Settings](lobby_settings.md) for the other available values.

<a id="оценка-лесов-и-камней"></a>
## Estimated Forests and Stone Deposits

| Objects | Approximate number on the entire map |
| --- | ---: |
| Large forest areas | **25** |
| Medium forest areas | **17** |
| Small forest areas | **13** |
| Stone deposits | **19** |
| Individual trees | about **2,620** |
| Individual stones | about **779** |

The estimates for individual trees and stones are less reliable than the
counts of forest areas and stone deposits because they use the typical
contents of each map-generation pattern.

<a id="запасы-древесины-и-камня"></a>
## Wood and Stone Reserves

Under the current game logic, **wood is effectively unlimited**. When a tree
runs out of health, it turns into a stump, but Peasants can continue gathering
wood from it at the same rate. Stone deposits likewise have so much health
that they are effectively inexhaustible.

The practical limits are therefore the number of convenient gathering
points, the distance to a Storehouse, and how many Peasants can work nearby,
not the total amount of wood or stone on the map.

<a id="месторождения-у-каждого-игрока"></a>
## Mineral Deposits per Player

With the selected Resource Deposits setting, the generator makes **four
placement rounds**. In each round it tries to place one gold, one iron, and
one coal deposit for every player.

The maximum per player is therefore **4 gold + 4 iron + 4 coal = 12
deposits**. The actual number can be lower if the terrain offers no suitable
free cell.

| Round | Usual distance from the starting point, cells |
| ---: | ---: |
| 1 | 14–22 |
| 2 | 32–42 |
| 3 | 70–82 |
| 4 | 22–38 |

For the complete algorithm, see
[How a Random Map Is Created](../../recon/world/map/map_generation_pipeline.md).
Replay-based calibration of this estimate is documented in
[Map Prediction Validation](../../../internals_en/data/map_predictions_validation.md).
