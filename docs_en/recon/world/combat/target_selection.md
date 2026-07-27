<a id="выбор-цели-и-атака-с-движением"></a>
# Target Selection and Attack-Move

[← How the Game Works](../../README.md)

Units do not share one automatic target across an entire formation. Each
soldier searches independently, and the rules differ for melee units,
ranged units, artillery, and healers. This allows a formation to spread
across the enemy line naturally, but it rarely concentrates fire without an
explicit order.

<a id="коротко"></a>
## At a Glance

- The game scans the area around a unit cell by cell and keeps eligible
  candidates.
- Within one cell, the scan begins at a random position, so nearby soldiers
  can choose different targets under otherwise similar conditions.
- Melee units account for allies already assigned to each enemy and avoid
  crowding the whole rank around one target.
- Ranged units usually choose the nearest valid target without that shared
  load balancing.
- Normal movement reacts mainly to enemies ahead; attack-move searches in
  every direction.
- Artillery ordered to fire at the ground attacks a coordinate rather than
  following a particular unit.

<a id="как-выбирается-цель"></a>
## How a Target Is Chosen

The process can be summarized as follows:

1. the game defines a search area around the unit;
2. cells without eligible enemies are skipped;
3. range, owner, state, and object type are checked in the remaining cells;
4. a ranged unit compares valid targets by distance;
5. a melee unit also considers how many allies have already selected each
   enemy.

The randomized starting point does not make targeting wholly random.
Unreachable, out-of-range, and unsuitable objects are still rejected. It
only separates the decisions of several units when the candidates are
otherwise almost equal.

<a id="почему-рукопашники-распределяются-по-фронту"></a>
## Why Melee Units Spread Across the Front

For melee targeting, an enemy is treated as 12.5% farther away for every
ally that has already selected it. If one opponent is surrounded, the next
Pikeman may prefer a neighboring enemy even when that enemy is physically
a little farther away.

This produces a natural front-line distribution:

- fewer soldiers crowd around one model;
- more of the formation begins fighting immediately;
- unattended enemies attract free attackers;
- an explicit attack order can still concentrate units on one target.

Ranged units do not use this adjustment. Without a manual order, each one
chooses its own nearest eligible target.

<a id="обычное-движение-и-атака-с-движением"></a>
## Normal Movement and Attack-Move

| Order | Enemy search |
|---|---|
| Normal movement | Reacts mainly to enemies within a forward cone of about 30°. |
| Attack-move | Repeatedly searches the full available radius. |
| Explicit unit attack | Prioritizes the selected target while it remains valid. |
| Artillery ground attack | Fires at the chosen coordinates even after the original enemy has moved. |

Immediately after starting to move, a ranged unit temporarily loses up to
three cells of effective detection range. The exact reduction varies
slightly between soldiers, so a rank may not open fire simultaneously.

<a id="пехота-и-кавалерия"></a>
### Infantry and Cavalry

During normal movement, a unit may switch to combat when an enemy appears
ahead. Enemies to the side or rear are more likely to be ignored.
Attack-move removes this directional restriction and is the safer order for
advancing through unknown or contested ground.

Normal movement is preferable when maintaining speed matters more than
engaging every minor target along the route.

<a id="артиллерия"></a>
### Artillery

Cannons, Howitzers, and Frame guns can be ordered to fire at a
point. The weapon remembers the coordinates and continues shelling them even
after the enemy previously standing there has moved away.

This can be used to:

- cover a narrow passage in advance;
- bombard a likely formation position;
- support a battle with area damage;
- suppress ground beyond the main line of troops.

To follow a moving enemy, attack the unit itself rather than the ground.

<a id="как-управлять-фокусом-огня"></a>
## How to Focus Fire

Automatic target selection does not coordinate a whole group. To
concentrate damage:

1. select the intended group;
2. issue an explicit attack order on one object;
3. choose the next high-value target after the first is destroyed.

This is especially useful against artillery, officers, healers, and
expensive cavalry. Without a direct order, ranged units spread their shots
among nearby eligible enemies.

<a id="лекари-и-раненые-союзники"></a>
## Healers and Wounded Allies

The Priest, Pope, Mullah, and Padre search only for allied units below
maximum health. Healing bypasses armor and protection: it restores health
directly, up to the target's maximum.

| Unit | Health restored | Range, cells | Distinction |
|---|---:|---:|---|
| Priest | 20 | 7.5 | Standard healer for most European nations. |
| Pope | 25 | 6.6 | Stronger healing at a shorter range. |
| Mullah | 15 | 9.4 | Longest healing range. |
| Padre | 30 | 7.5 | Most health restored per action. |

Several healers may assist the same target at once. They cannot convert
enemy units: religious units in Cossacks 3 are healers only.

<a id="реакция-отряда-на-полученный-урон"></a>
## How a Formation Reacts to Damage

A hit on one non-artillery soldier makes the entire formation more
aggressive. Its other members begin searching for enemies and responding to
the threat more actively.

This has several practical consequences:

- one shot can draw a whole enemy formation into action;
- a decoy can redirect an army's response;
- a covert raid should avoid touching guards too early;
- artillery formations handle the reaction differently and may continue
  their previous order.

<a id="9-рассеяние-и-точность-выстрела"></a>
<a id="рассеяние-и-точность"></a>
## Dispersion and Accuracy

Projectile deviation grows approximately in direct proportion to distance.
The farther the target and the greater the weapon's base dispersion, the
wider the possible impact area.

| Weapon | Deviation at a range of 15 cells |
|---|---:|
| Streltsy musket shot | about ±1.50 cells |
| Standard arrow | about ±1.31 cells |
| Fire arrow | about ±1.50 cells |
| Musketeer base shot | about ±1.88 cells |
| Cannonball | about ±1.88 cells |
| Tower shot | about ±0.75 cells |
| Yacht or Galley cannonball | about ±0.19 cells |

Listed damage is therefore not guaranteed damage per second against a small
target at long range: some shots miss. Two Academy upgrades reduce artillery
dispersion; Musketeers and Archers have no direct equivalent.

<a id="практические-выводы"></a>
## Practical Takeaways

- Use attack-move when entering unknown ground.
- Use normal movement when the group should ignore unimportant targets.
- Manually prioritize artillery, healers, and officers.
- Do not expect ranged units to focus fire automatically.
- When bombarding a point, account for enemy movement and projectile travel
  time.
- Keep healers behind the front line and protect them from flanking units.

<a id="техническое-приложение"></a>
## Technical Appendix

Exact search modes, cell traversal, internal target lists, dispersion
formulas, and script excerpts are available in the
[technical target-selection analysis](../../../../internals_en/scripts/target_selection_evidence.md).
