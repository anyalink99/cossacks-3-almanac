<a id="tow--башня"></a>
<a id="башня-tow"></a>
<a id="башня"></a>
# Tower

[← All buildings](README.md)

The table lists the available national variants. Bold values differ from the most common version of the building.

| Building | Nations | Health | Construction time | Price growth | Food | Wood | Stone | Gold | Iron | Coal | Notes |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Tower** `eurtow` | Austria, Bavaria, Denmark, England, France, Hungary, Netherlands, Piedmont, Poland, Portugal, Prussia, Saxony, Scotland, Spain, Sweden, Switzerland, Venice | 20000 | 1230.31 | 120 | 0 | 100 | 100 | 150 | 0 | 0 | damage 1000; range 28.1t; gold upkeep 500 |
| **Tower** `rustow` | Russia | 21000 | 1476.56 | 125 | 0 | 100 | 100 | 150 | 0 | 0 | damage 1000; range 28.1t; gold upkeep 500 |
| **Tower** `turtow` | Algeria, Turkey | 22500 | 984.38 | 125 | 0 | 150 | 90 | 100 | 0 | 0 | damage 1200; range 30.0t; gold upkeep 500 |

<a id="башня--кратко"></a>
## Tower summary

A complete analysis of shooting, review, garrison and strategy - in
[tower and garrison mechanics](../../recon/world/combat/towers.md).
Brief parameters of the basic European tower (`eurtow`):

| Parameter | Meaning | Note |
|---|---:|---|
| HP | 20,000 | rus 21 000, tur 22 500 |
| `vision` | 3 → 32 FOW tiles | less than the average hussar |
| `searchradius` | 1400 px = 26.25 t | target auto-lock radius |
| Damage | 1000 | `cannonball` |
| `weapon_pause` | 400 frames = 12.5 g-sec | rus 9.4 g-sec, tur 15.6 g-sec |
| Shot range | 1500 px = 28.13 t | tur 30 t |
| Scatter | 100 px = 1.88 t | rus 125 |
| Shot cost | 10 iron + 30 coal | tur: 15 iron + 40 coal |
| Contents | `consume[gold] = 500` → **0.8 gold / g-sec** (≈ 67 / real-min @ fast) | formula `× 32 / 20000`, with `gold = 0` the turret silently stops firing |
| Capture | `bcapture = False` | the tower is **never** captured after construction |

5 upgrade levels `eurtow.1..5` reduce `weapon_pause` to
× 0.467 from base → fire frequency **× 2.14**. The full list is in
[Tower upgrades](../05_upgrades/tower.md).
