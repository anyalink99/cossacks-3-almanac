<a id="recon-голод-и-бунт"></a>
<a id="голод-и-бунт-наёмников"></a>
# Famine and Mercenary Rebellion

[← How the game works](../../README.md)

An empty food stockpile gradually kills ordinary troops and peasants. An empty
gold stockpile combined with an unsustainable upkeep balance starts mercenary
rebellion checks. On Hard and above they can turn against their owner quickly;
on Easy and Normal this happens much more slowly. Famine and rebellion are
separate crises: food shortages threaten the regular army, while an
unsustainable gold balance threatens mercenaries.

<a id="коротко-о-главном"></a>
## In brief

- Famine begins after food is already gone and the next consumption payment
  cannot be made; a shortage of housing does not cause it.
- Famine ends as soon as some food is available or food consumption stops.
- Buildings and mercenaries do not die from famine. Peasants, infantry, and
  cavalry bear the main risk.
- Rebellion begins at zero gold only when gold expenditure exceeds income.
  Working gold mines may keep an army loyal even with an empty stockpile.
- Only mercenaries from the Diplomatic Center rebel. They move to a separate
  game-controlled side and then fight everyone.
- On high difficulty, rebellion unfolds rapidly; famine is much slower.

<a id="когда-начинается-и-заканчивается-кризис"></a>
## Starting and ending a crisis

| State | Starts when | Ends when |
|---|---|---|
| Famine | food is at zero and the next consumption payment cannot be met | food rises above zero or food consumption stops |
| Rebellion | gold is at zero and expenditure exceeds income | the stockpile reaches two gold or gold expenditure stops |

Gold depends on the current balance as well as the stockpile. If mines earn at
least as much as mercenary upkeep costs, rebellion does not begin even at zero
stored gold. Food has no equivalent protection: a shortfall at the next
payment immediately starts famine.

The state is recalculated with resources. Buying food or gold at the Market
can therefore end the crisis on the next calculation.

<a id="кого-убивает-голод"></a>
## Who can die from famine

Famine checks every food-consuming unit separately.

| Object type | Can die from famine |
|---|---|
| Peasant or Serf | Yes |
| Ordinary infantry and cavalry | Yes |
| Building | No |
| Mercenary from the Diplomatic Center | No |
| Certain elite units | Depends on their game data |

Peasants do not receive a special priority. Under equal conditions, they make
the same random check as every other vulnerable unit. They appear to die first
because players usually have more of them.

<a id="скорость-гибели-от-голода"></a>
## Famine death rate

| Mode and difficulty | Probability for one vulnerable unit per check |
|---|---:|
| Single-player, Easy | about 0.0153% |
| Single-player, Normal | about 0.0366% |
| Any mode, Hard, Very Hard, or Impossible | about 0.1526% |
| Network match, Easy | about 0.1678% |
| Network match, Normal | about 0.1892% |

Every unit receives an independent random result. A player with more
vulnerable inhabitants and troops is likely to see the first death sooner,
even though the chance for each unit is unchanged.

In single-player on Easy and Normal, and on high difficulty, that is one
death per roughly 6,554, 2,731, or 655 checks on average, respectively.
Online Easy and Normal average about 596 and 529 checks. In a large army, the
first loss occurs sooner because every unit receives an independent result.

<a id="как-считается-потребление-еды"></a>
## Food consumption

Each unit has a base consumption value. Ordinary units that are not immune to
famine also receive a common surcharge. The combined total for all units is
converted into consumption per game second.

| Canonical name | Food per game second |
|---|---:|
| Peasant of Austria, Poland, Spain, England, Ukraine, or Scotland | 0.0992 |
| Peasant of Turkey or Algeria | 0.0928 |
| Russian Serf | 0.0896 |
| Infantryman with no additional personal consumption | 0.0480 |

As a practical reference, 18 idle Austrian Peasants consume about 214 food
over two game minutes. The formula, source fields, and calculation are in the
[technical appendix](../../../../internals_en/scripts/hunger_and_rebellion_evidence.md).

<a id="что-происходит-при-бунте"></a>
## What rebellion does

Rebellion affects only mercenaries hired from the Diplomatic Center. Each one
checks independently whether to leave its owner.

| Difficulty | Transfer probability per check |
|---|---:|
| Easy | about 0.305% |
| Normal | about 0.610% |
| Hard, Very Hard, or Impossible | about 18.31% |

On high difficulty, one mercenary needs about 5.5 checks on average before
changing sides, so a large group can rapidly leave its owner. The process is
far slower on Easy and Normal.

Departing mercenaries do not become harmless neutral units. They move to a
separate game-controlled side that is hostile to every participant in the
match.

When a mercenary defects, three times that unit's base value is immediately
deducted from the former owner's score. At the same time, the new
game-controlled owner receives the unit's base value once; the unit's later
death is processed separately. These points affect final statistics, not
victory or rating.

Upkeep, income, and the Diplomatic Center are covered in more detail in the
[mercenary article](../../systems/mercenaries_diplomacy.md).

<a id="как-избежать-голода"></a>
## Preventing famine

- Keep a food reserve before training a large army or launching an attack.
- Place Storehouses near fields so that peasants deliver crops faster.
- Watch the total number of food-consuming units, not only peasants.
- During an emergency, buy food at the Market and restore field production as
  quickly as possible.

<a id="как-избежать-бунта"></a>
## Preventing rebellion

- Establish sustainable gold-mine income before hiring mercenaries in bulk.
- Compare gold income with upkeep rather than relying only on the stockpile.
- Use the Market as an emergency source of gold.
- Once rebellion starts on high difficulty, do not expect a long grace period:
  restore the balance immediately.

<a id="голод-и-предел-населения--разные-вещи"></a>
## Famine and the population limit are different

Running out of housing capacity does not start famine or kill existing units.
It only prevents new units from being created. Famine begins only when actual
food consumption cannot be paid.

Resource and population-related defeat conditions are covered separately in
[How Victory Is Decided](../../systems/victory_conditions.md).

<a id="технические-подробности-и-источники"></a>
## Technical details and sources

Internal state flags, exact random thresholds, the consumption formula, script
paths, and source excerpts are kept in the
[technical appendix](../../../../internals_en/scripts/hunger_and_rebellion_evidence.md).
