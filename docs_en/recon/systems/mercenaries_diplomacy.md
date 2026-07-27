<a id="recon-дипломатические-центры-и-наёмники"></a>
<a id="наёмники-и-дипломатический-центр"></a>
# Mercenaries and the Diplomatic Center

[← How the game works](../README.md)

This article explains recruitment through the **Diplomatic Center**, gold
upkeep, price growth, and rebellion when the treasury is empty. Internal
identifiers and Pascal excerpts are collected under
[Technical details](#technical-details) and [Sources](#sources).

**Related documents:**

- [Peasant resource gathering](../world/economy/peasant_extraction.md)
  explains why mercenaries consume no food.
- [Construction and repair](../world/economy/building_mechanics.md)
  explains the Diplomatic Center's footprint and construction model.
- [Server architecture and network synchronization](../../../internals_en/engine/server_sync_architecture.md)
  explains why the server confirms owner changes during a rebellion.
- [Determinism audit](../../../internals_en/engine/determinism_audit.md)
  explains how the random selection of deserters stays synchronized.

<a id="кратко"></a>
## Key points

- The **Diplomatic Center** is a mid-game building available
  to all 21 nations. Its common variant costs 4,900 wood and 1,700 stone,
  has 4,500 health, and requires an Academy and Town Hall.
- It recruits **eight mercenaries**: six base units and two from the
  Early Bird DLC. Every nation uses the same roster and unit statistics.
- A mercenary costs **only gold**, consumes no food, and
  **continuously drains gold** as upkeep.
- When gold reaches zero while expenses exceed income, each mercenary can
  join an army hostile to every participant:
  - **Easy:** 0.305% per update;
  - **Normal:** 0.610% per update;
  - **Hard and above:** 18.31% per update.

---

<a id="1-дипломатические-здания-по-нациям"></a>
<a id="дипломатический-центр-у-разных-наций"></a>
## Diplomatic Centers by nation

Each of the 21 nations has one version of the building. Most European
nations share common statistics; Russia, Ukraine, Turkey, and Algeria have
their own values [^1] [^2].

| Building | Nations | Health | Build time | Wood | Stone | Gold | Capturable |
|---|---|---:|---:|---:|---:|---:|---|
| **Diplomatic Center** | Austria, France, England, Spain, Poland, Sweden, Prussia, Venice, Netherlands, Denmark, Portugal, Piedmont, Saxony, Bavaria, Hungary, Switzerland, Scotland | 4500 | 1000 frames | 4900 | 1700 | 0 | No |
| **Diplomatic Center** | Russia | 6500 | 1000 frames | 7900 | 3700 | 0 | No |
| **Diplomatic Center** | Ukraine | 5000 | 1000 frames | 3900 | 2700 | 0 | No |
| **Diplomatic Center** | Turkey, Algeria | 5500 | 1000 frames | 4600 | 2020 | 0 | No |

Construction requires an Academy. **The Diplomatic Center is not
capturable**, while its prerequisite Academy is. Localization also says
that a player may build only one Diplomatic Center; the code path enforcing
that limit has not yet been found.

---

<a id="2-каталог-наёмников"></a>
<a id="кого-можно-нанять"></a>
## Available mercenaries

Every nation receives the same eight mercenaries: **Light Infantryman**,
**Roundshier**, **Grenadier**, **Archer**, **Sich Cossack**,
**18th-century Dragoon**, and the Early Bird units **Turkish Archer** and
**Light Cavalry** [^5]. Recruitment requires a Town Hall, an Academy, and
the Diplomatic Center itself [^6].

<a id="21-детектирование-bmercenary"></a>
<a id="21-как-игра-распознаёт-наёмника"></a>
<a id="общие-правила"></a>
### Shared rules

Every nation receives the same roster with identical statistics. Mercenary
versions use their own price, health, weapons, and upkeep even when they are
derived from a similar regular unit [^7].

<a id="22-статы-каждого-наёмника"></a>
<a id="22-характеристики-наёмников"></a>
<a id="характеристики-наёмников"></a>
### Mercenary statistics

| Mercenary | Health | Recruit time, frames | Gold | Gold upkeep | Price growth, % | Weapon (damage/range/type) |
|---|---:|---:|---:|---:|---:|---|
| **Light Infantryman** | 50 | 40 | 4 | 4 | 100 | sword 16, range 50 px |
| **Roundshier** | 75 | 48 | 12 | 20 | 100 | sword 6, range 50 px |
| **Archer** | 20 | 40 | 15 | 16 | 100.5 | arrow 25 / firearm 100, range 700/750 |
| **Turkish Archer** | 20 | 40 | 15 | 16 | 100.5 | same |
| **Grenadier** | 30 | 48 | 25 | 60 | 100.5 | pike 30 / bullet 16 (range 800) / grenade 200 (range 400) |
| **Sich Cossack** | 150 | 80 | 60 | 150 | 100.5 | cavalry sabre 8, range 20 px |
| **18th-century Dragoon** | 100 | 64 | 120 | 120 | 102 | cavalry bullet 18, range 800 |
| **Light Cavalry** | 100 | 64 | 120 | 120 | 102 | same |

See [^8] for the exact `unit.script` branches that set `bnohungry` and
zero food, wood, stone, iron, and coal.

`bnohungry := True` is set in every mercenary branch, so mercenaries do not
pay food upkeep (see [hunger and army upkeep](../world/economy/hunger_and_rebellion.md)).

`SetObjBasePrice(objbase, 0, 0, 0, gold, 0, 0)` zeros every recruitment
resource except gold. **Mercenaries therefore cost only gold**.

<a id="23-масштабирование-цены-и-общий-счётчик"></a>
### 2.3 Price scaling and shared counters

Mercenary `costpercent` is 100, 100.5, or 102. Each subsequent copy costs
`floor(base × (costpercent/100)^N)` (see [price growth](../../reports/economy/scaling_prices.md)).
For mercenaries the limit is **lower than for regular units** [^9]:

- Paired units share a counter: **Archer** (`archerdip`) with
  **Turkish Archer** (`archerturdip`), and **Dragoon, 18th century**
  (`dragoon18dip`) with **Light Cavalry** (`lightcavalrydip`). The
  `case sid of` branch sums
  `gPlayer[plInd].counter.all[cid][tmpid]`.
- `costmodifier = pow(costpercent/100, count)` is capped by
  `if bmercenary and (costmodifier > 2) then costmodifier := 2`.
  Regular units instead use a ceiling of `20000`.

Two consequences:

1. **The Archer** (`archerdip`) **and Turkish Archer**
   (`archerturdip`) share one price counter. The same applies to the
   **Dragoon, 18th century** (`dragoon18dip`) and **Light Cavalry**
   (`lightcavalrydip`). Recruiting 100 Turkish Archers therefore raises
   the price of the ordinary Archer.
2. A mercenary's price can rise to at most **twice its base price**, not
   20,000 times. With `costpercent = 100.5`, the cap is reached after
   roughly `ln(2) / ln(1.005) ≈ 139` shared recruits; the price then
   remains flat.

---

<a id="3-механика-upkeep--потребление-золота"></a>
<a id="3-содержание-за-золото"></a>
## 3. Gold upkeep

Upkeep is consumed every frame in the same general cycle as food
(see [hunger and army upkeep](../world/economy/hunger_and_rebellion.md)).
The handler is `_player_ProcessResourceConsume`
in `player.script` [^10].

The cycle works as follows:

- For resource `i`, it reads
  `resconsume = gPlayer[plInd].counter.resconsume[i]`.
- Every frame it adds
  `resconsume × gc_time_to_frames × deltatime` to an accumulator, with
  `gc_time_to_frames = 32`.
- `value = floor(bank / 20000)` is the whole number of resource units
  due for payment.
- If the player can pay, `value` is deducted and the corresponding
  famine or rebellion flag is cleared.
- Otherwise, the remaining stock is deducted and the game raises
  `bfamine` for food or `brebellion` for gold.

<a id="скорость-утечки-золота"></a>
### Gold drain rate

Gold uses the same formula as food upkeep, in `consume.gold` units per
game second:
```
drain_per_g_sec = sum_over_units(consume.gold) × 32 / 20000
```
One **Dragoon, 18th century** (`dragoon18dip`) with
`consume.gold = 120` drains `120 × 32 / 20000 = 0.192` gold per game
second, or about **11.5 gold per game minute**. Fifty of them drain 9.6
gold per game second, or 576 per game minute—a cost that generally
requires a Market and Gold Mines.

<a id="bfamine-vs-brebellion--асимметрия"></a>
<a id="различие-голода-bfamine-и-бунта-brebellion"></a>
### `bfamine` versus `brebellion`: an asymmetry

Both flags are cleared when the player can pay and set when the relevant
resource is unavailable. **Gold has an additional safeguard:** rebellion
requires `resconsume[gold] > resincome[gold]` [^11]. If current gold
income covers upkeep, a momentary zero balance does not cause a rebellion.
The player must have both an empty reserve and an ongoing deficit.

`brebellion` is also cleared when `res[gold] >= 2` or
`resconsume[gold] <= 0` [^12]. Disbanding all mercenaries therefore ends
the rebellion immediately.

---

<a id="4-триггер-бунта"></a>
<a id="4-как-начинается-бунт"></a>
## 4. How rebellion begins

Desertion is handled by each unit's `Nothing` state in
`units/unit.inc/nothing.inc`, alongside random starvation deaths [^13].
It requires:

- `gPlayer[plInd].brebellion = True`,
- `objprop.bmercenary = True`,
- `plInd <> gc_player_mercenaryind` (not the mercenary slot itself),
- a playable unit (`bplayable`).

The game then calls `_misc_RandomInt`
(`floor(random × 32768)`, with `gc_c1rand_to_random = 32768`) [^14].
The threshold depends on the player's difficulty.

| Difficulty | Condition | Probability per `Nothing` update |
|---|---|---:|
| Easy (`0`) | 100 | 100/32768 ≈ **0.305%** |
| Normal (`1`) | 200 | 200/32768 ≈ **0.610%** |
| Hard, Very Hard, or Impossible (`>1`) | 6000 | 6000/32768 ≈ **18.31%** |

The handler runs during progress updates for idle and walking units.
On Hard and above, **a typical mercenary deserts within five or six
updates after `brebellion = True`**. A whole mercenary army can therefore
switch sides in a few game seconds.

On a successful random check, the unit is transferred to the NPC player via
`_misc_ChangePlayer(myHnd, plMercHnd, False, False, True)`. The mercenary
player occupies
`gc_player_mercenaryind = gc_MaxPlayerCount - 1` [^15]. Map
initialization makes this player hostile to every normal participant:
each real player's `enemyplmask` includes the NPC player's bit [^16].

Therefore, deserted mercenaries become hostile to **everyone**, including
their former owner. They remain alive.

The mercenary NPC starts with 20,000 gold and 10,000 of every other
resource [^17]. This lets deserted units pay their upkeep, although they
cannot desert again while already owned by the mercenary player.

<a id="реакция-ai"></a>
<a id="реакция-ии"></a>
### AI reaction

Rebellion also changes the AI's defense weighting [^18]:
`scoremodifier = 5` for captured units, `3` for its own mercenaries
during rebellion, and `2` for other owned units. The AI thus lowers the
priority of protecting mercenaries that are about to desert.

---

<a id="5-map-настройка-marketdip"></a>
<a id="5-настройка-лобби-рынок-и-дипломатический-центр-marketdip"></a>
## 5. “Market and Diplomatic Center” setting (`marketdip`)

`gMap.settings.additional.marketdip` controls the availability of Markets
and Diplomatic Centers in a match. All five values are listed under
[lobby settings](../../reports/map/lobby_settings.md#marketdip--рынок-и-дипцентр);
engine behavior is covered by
[match settings](../world/map/game_settings.md) §3.5.

Constants [^19]:

- `gc_mapsettings_marketdip_default = 0` — both are enabled,
- `gc_mapsettings_marketdip_nodip = 1` — Diplomatic Centers are disabled (`bproduceenabled := False`),
- `gc_mapsettings_marketdip_nomarket = 2` — Markets are disabled,
- `gc_mapsettings_marketdip_noboth = 3` — both are disabled,
- `gc_mapsettings_marketdip_expensivemercs = 4` — the price of each mercenary × 3.

The `expensivemercs` branch is in `player.script` [^20]. If
`objprop.bmercenary = True`, then for each resource
`TObjBase(pobjbase).price[res]` is multiplied by `gc_gameplay_expensivemercskoef = 3` [^21].
In the lobby with `expensivemercs`, the gold price of mercenaries is tripled
(4 → 12, 60 → 180, 120 → 360, 150 → 450, …). The multiplier is applied to
**all** slot prices, but since mercenaries only have non-zero
`price[gold]`, only the gold value is tripled.

---

<a id="6-нейтральные-дипцентры--точки-найма"></a>
<a id="6-есть-ли-нейтральные-точки-найма"></a>
## 6. Neutral recruitment points

**No.** Search in `data/scripts` for substrings `peasantdip`, `townhalldip`,
`tradehouse`, `gc_player_neutralind`, and `bneutral` finds no neutral
villages or pre-placed Diplomatic Centers on standard skirmish maps.
The only related neutral mechanisms are:

- `gPlayer.bneutral` [^22], which is changed only by scenarios. All
  normal players have `bneutral = False` in a skirmish;
- Mercenary owner slot `gc_player_mercenaryind` exists from initialization
  but owns *no buildings*. It exists only to receive deserters.

Therefore, on a standard random map, **the only way to recruit
mercenaries is to build a Diplomatic Center** (`<nat>dip`) with the
cost and prerequisites listed in §1.

Custom scenarios can place neutral Diplomatic Centers and call
`_misc_ChangePlayer`, but that is scenario content rather than a
standard random-map mechanic.

---

<a id="7-кросс-национальная-доступность"></a>
<a id="7-доступность-для-разных-наций"></a>
## 7. Availability across nations

Because `_country_AddMember` adds all eight mercenaries to **every**
nation and the production setup is shared, **any nation can recruit any
mercenary**. The six base units are **Roundshier** (`roundshierdip`),
**Light Infantryman** (`lightinfantrydip`), **Archer** (`archerdip`),
**Grenadier** (`grenadierdip`), **Sich Cossack** (`cossacksichdip`), and
**Dragoon, 18th century** (`dragoon18dip`). The **Light Cavalry**
(`lightcavalrydip`) and **Turkish Archer** (`archerturdip`) require the
Early Bird DLC (`bEarlyBird`) [^5].

Mercenary IDs have no nation suffix, unlike the **Spearman**
(`pikemanrus`) and **Covenanter Pikeman** (`pikemansco`). Unit
initialization sets `bmercenary` without filtering by nation [^7].

The apparent nation distinction in the paired IDs is purely a
**visual/model variant**. The Archer and Turkish Archer, as well as the
Dragoon and Light Cavalry, share statistics and a price counter (§2.3);
only their Western or Eastern appearance differs.

Formation rules differ slightly [^23]. **Roundshiers**
(`roundshierdip`) and **Grenadiers** (`grenadierdip`) can join standard
infantry formations with national Pikemen and Musketeers. **Archers**,
**Turkish Archers**, and **Light Infantrymen** use the
`…NoOfficersExtDip` registration and form formations without a national
Officer.

---

<a id="8-наёмник-vs-обычный-юнит--сравнение"></a>
<a id="8-сравнение-с-обычными-юнитами"></a>
## 8. Comparison with regular units

<a id="стоимость"></a>
### Cost

Mercenaries require **only gold and recruitment time**. Regular units may
also require food, iron, and coal, then consume food as upkeep. A heavy
mounted shooter illustrates the trade-off:

| Unit | Food | Iron | Coal | Gold | Shot cost | Health | Recruit time |
|---|---:|---:|---:|---:|---|---:|---:|
| **Dragoon, 18th century** (`dragoon18`, regular European) | 70 | 7 | 0 | 60 | 4 iron + 5 coal | 225 | 720 frames |
| **Dragoon, 18th century (mercenary)** (`dragoon18dip`) | 0 | 0 | 0 | 120 | 5 iron + 8 coal | **100** | **64 frames** |

The mercenary costs 60 more gold and no food, iron, or coal at
recruitment. It is **recruited eleven times faster**, but has only 44%
of the regular Dragoon's health, costs slightly more iron and coal per
shot, and continuously drains gold. The **Archer** follows a similar
pattern: the regular **Archer** (`archer`) has `btf = 32`, while the
mercenary Archer (`archerdip`) has `btf = 40`; the mercenary costs no
food and deals 25 rather than 15 damage.

<a id="содержание"></a>
### Upkeep

- Regular units consume food at
  `(consume.food + (bnohungry?0:30)) × 32/20000` per game second
  (see [hunger and army upkeep](../world/economy/hunger_and_rebellion.md)).
  Mercenaries have `bnohungry`, so they drain no food.
- Mercenaries consume gold at `consume.gold × 32/20000` per game second,
  based on
  `consume.gold` (4–150 per mercenary).
- Officers and Royal Musketeers also have `consume.gold` values of
  60–150, but are **not** `bmercenary` and cannot rebel.

<a id="когда-брать-наёмников-стратегический-профиль"></a>
### Strategic use

Mercenaries are essentially a **rapid-deployment army bought with gold**:

- **Early game.** Nations with an abundance of wood and poor access to iron/coal
  can exchange wood and stone for gold at the Market, then quickly recruit
  Roundshiers or Light Infantrymen.
- **Mid-game.** A gold surplus from allied trade or captured Gold Mines
  can become a Dragoon army without waiting for Coal Mines.
- **Low durability, fast deployment.** Mercenaries often have roughly half
  the health of comparable regular units, but the high-tier recruitment
  advantage is enormous: the mercenary Dragoon takes 64 frames versus
  720 for the regular unit, **11.25 times faster**.

**The main risk is an interruption to gold income.** If
`income[gold]` falls below upkeep and the reserve reaches zero, an entire
mercenary army can desert within seconds on Hard and above. Disbanding
mercenaries **before** the reserve is exhausted avoids this.

---

<a id="технические-подробности"></a>
## Technical details

The Diplomatic Center is registered as `<nat>dip` through
`_country_AddMember`; its AI role is `gc_ai_unit_dipcenter`, and its object
usage is `gc_obj_usage_dipcenter = 32` [^1] [^4]. The common variant is
used by `aus`, `fra`, `eng`, `spa`, `pol`, `swe`, `pru`, `ven`, `net`,
`den`, `por`, `pie`, `sax`, `bav`, `hun`, `swi`, and `sco`; separate
branches define `rusdip`, `ukrdip`, `turdip`, and `algdip` [^2].

`SetObjBuildingExtProperties` receives
`maxhp, buildtime, costpercent, bcapture, score, usage, food, wood, stone,
gold, iron, coal` [^3]. The Diplomatic Center has `bcapture=False` and
`costpercent=100`; the Academy has `bcapture=True`. The `0{1000}` comment
beside the zero gold price preserves the old value from the first Cossacks.

Mercenaries are recognized by eight internal identifiers:
`lightinfantrydip`, `roundshierdip`, `grenadierdip`, `archerdip`,
`cossacksichdip`, `dragoon18dip`, `archerturdip`, and
`lightcavalrydip`. Their `bmercenary` branch overrides health, weapons,
price, `consume.gold`, `bnohungry`, and `costpercent` [^7] [^8].

<a id="9-открытые-вопросы"></a>
## 9. Open questions

| # | Question | How to verify |
|---:|---|---|
| 1 | Localization says that each player can build only one Diplomatic Center, but no explicit `if count(dip) >= 1 then bproduceenabled := False` check was found. `costpercent = 100` does not enforce the limit either. | Inspect `gui.script` and production quotas. The AI's `_ai_GetUnitCount(..., gc_ai_unit_dipcenter) > 0` check does not constrain human players. |
| 2 | `bnoreputation` is never assigned in the inspected scripts. It may be a leftover from an earlier Cossacks game or an incorrectly identified field. | Search every `.script` and `.global` file. |
| 3 | The real-time frequency of rebellion checks remains uncertain. | Compare the `Nothing` update with [ticks and subticks](../../../internals_en/engine/ticks_and_subticks.md) §3. At 135 ms, a Hard mercenary typically defects in under a second; at 100 ms, in roughly half a second. |
| 4 | Twenty **Ship of the Line** (`battleship`) rows in `data.json` have `bmercenary = True`, although the `case 'battleship'` branch in `unit.script` does not set it. | Check for a separate Shipyard branch and rule out a parser artifact. |

---

<a id="источники"></a>
## Sources

All links are relative to `data/scripts/` in the Cossacks 3 installation.

[^1]: Registration of the Diplomatic Center in each nation's roster —
    `lib/country.script:2829`:
    ```pascal
    _country_AddMember(country, csid+'dip', ind, True,
                       gc_country_editorplace_category_buildings, 20,
                       gc_ai_unit_dipcenter);
    ```
[^2]: Selection of Diplomatic Center statistics by `csid+'dip'`, including
    national overrides —
    `lib/unit.script:2451-2459`:
    ```pascal
    csid+'dip' : begin
       SetObjBuildingExtProperties(objprop, objbase,
           4500, 1000, 100, False, 500,
           gc_obj_usage_dipcenter,
           0, 4900, 1700, 0{1000}, 0, 0);
       case i of
          rus : SetObjBuildingExtProperties(objprop, objbase,
                  6500, default, default, False, default, default,
                  0, 7900, 3700, 0{2500}, 0, 0);
          ukr : SetObjBuildingExtProperties(objprop, objbase,
                  5000, default, default, False, default, default,
                  0, 3900, 2700, 0{500}, 0, 0);
          tur : SetObjBuildingExtProperties(objprop, objbase,
                  5500, default, default, False, default, default,
                  0, 4600, 2020, 0{1300}, 0, 0);
          alg : SetObjBuildingExtProperties(objprop, objbase,
                  5500, default, default, False, default, default,
                  0, 4600, 2020, 0{1300}, 0, 0);
       end;
    end;
    ```
[^3]: Signature of `SetObjBuildingExtProperties` — `lib/unit.script:503`.
    Argument order:
    `maxhp, buildtime, costpercent, bcapture, score, usage, food, wood, stone, gold, iron, coal`.

[^4]: `gc_obj_usage_dipcenter = 32` - `dmscript.global:339`.

[^5]: Registration of eight mercenaries through `_country_AddMember` —
    `lib/country.script:2786-2793, 2900-2901`:
    ```pascal
    _country_AddMember(country, 'lightinfantrydip', ind, True, ...gc_ai_unit_light_dip);
    _country_AddMember(country, 'roundshierdip',    ind, True, ...gc_ai_unit_round_dip);
    _country_AddMember(country, 'grenadierdip',     ind, True, ...gc_ai_unit_grendip);
    _country_AddMember(country, 'archerdip',        ind, True, ...airole);
    _country_AddMember(country, 'cossacksichdip',   ind, True, ...gc_ai_unit_cossackdip);
    _country_AddMember(country, 'dragoon18dip',     ind, True, ...gc_ai_unit_dragundip);
    // "early-bird" extension (DLC):
    _country_AddMember(country, 'archerturdip',     ind, True, ..., gc_ai_unit_none);
    _country_AddMember(country, 'lightcavalrydip',  ind, True, ..., gc_ai_unit_none);
    ```
[^6]: Production setup for eight mercenaries —
    `lib/country.script:3010-3022`:
    ```pascal
    member := csid+'dip';
    fixedproduceind := _country_GetFixedProduceIndexBySID(cid, member, bAddIfNotExist);
    _country_AddFixedProduceWithAccessControl(country, fixedproduceind, member,
       'roundshierdip',    0, 0, ind, csid+'cen', csid+'aca', '');
    _country_AddFixedProduceWithAccessControl(country, ..., 'lightinfantrydip', 1, 0, ind, csid+'cen', csid+'aca', '');
    _country_AddFixedProduceWithAccessControl(country, ..., 'archerdip',        2, 0, ind, csid+'cen', csid+'aca', '');
    _country_AddFixedProduceWithAccessControl(country, ..., 'grenadierdip',     3, 0, ind, csid+'cen', csid+'aca', '');
    _country_AddFixedProduceWithAccessControl(country, ..., 'cossacksichdip',   4, 0, ind, csid+'cen', csid+'aca', '');
    _country_AddFixedProduceWithAccessControl(country, ..., 'dragoon18dip',     5, 0, ind, csid+'cen', csid+'aca', '');
    if (bEarlyBird) then
    begin
       _country_AddFixedProduceWithAccessControl(country, ..., 'lightcavalrydip', 5, 1, ind, csid+'cen', csid+'aca', '');
       _country_AddFixedProduceWithAccessControl(country, ..., 'archerturdip',    2, 1, ind, csid+'cen', csid+'aca', '');
    end;
    ```
[^7]: Detection of `bmercenary` from the internal unit ID (`sid`) —
    `lib/unit.script:611-614`:
    ```pascal
    var bmercenary : Boolean;
    if StrExists(sid, 'dip') and ((sid='roundshierdip') or (sid='lightinfantrydip')
       or (sid='archerdip') or (sid='grenadierdip') or (sid='cossacksichdip')
       or (sid='dragoon18dip') or (sid='archerturdip') or (sid='lightcavalrydip')) then
    bmercenary := True;
    ```
[^8]: `if (bmercenary) then begin ... end` blocks for each mercenary
    in `lib/unit.script`:

    - **Light Infantryman** (`lightinfantrydip`) — lines 712–734.
    - **Roundshier** (`roundshierdip`) — lines 735–770.
    - **Archer** (`archerdip`) and **Turkish Archer** (`archerturdip`)
      share the same `case` — lines 997–1061.
    - **Grenadier** (`grenadierdip`) — lines 1226–1318.
    - **Sich Cossack** (`cossacksichdip`) — lines 1320–1391.
    - **Dragoon, 18th century** (`dragoon18dip`) and **Light Cavalry**
      (`lightcavalrydip`) share the same `case` — lines 1544–1662.

    Resetting food/wood/stone/iron/coal — `SetObjBasePrice(objbase, 0, 0, 0, gold, 0, 0)`,
    for example: line 725 for **Light Infantryman** (`lightinfantry`),
    1048 for **Archer** (`archer`), 1382 for **Sich Cossack**
    (`cossacksich`), and 1651 for **Dragoon, 18th century** (`dragoon18`).

[^9]: Twofold price cap for mercenaries in `_unit_GetCostModifier` —
    `lib/unit.script:5660-5678`:
    ```pascal
    if (bmercenary) then
    begin
       var sid : String = gObjProp[cid][unitID].sid;
       var tmpsid : String;
       case sid of
          'archerdip'       : tmpsid := 'archerturdip';
          'archerturdip'    : tmpsid := 'archerdip';
          'dragoon18dip'    : tmpsid := 'lightcavalrydip';
          'lightcavalrydip' : tmpsid := 'dragoon18dip';
       end;
       var tmpid : Integer = _unit_ConvertObjSIDToID(cid, tmpsid);
       count := count+gPlayer[plInd].counter.all[cid][tmpid];
    end;
    costmodifier := pow(costpercent/100, count);
    if bmercenary and (costmodifier>2) then
    costmodifier := 2
    else
    if (costmodifier>20000) then
    costmodifier := 20000;
    ```

[^10]: `_player_ProcessResourceConsume` — `lib/player.script:268-322`:
    ```pascal
    procedure _player_ProcessResourceConsume(const plInd : Integer; const deltatime : Float);
    begin
       var i : Integer;
       for i:=0 to gc_ResCount-1 do
       begin
          var resconsume : Integer = gPlayer[plInd].counter.resconsume[i];
          if (resconsume>0) then
          begin
             const mult = 100;
             const speed = 20000;
             var resconsumerem : Float = gPlayer[plInd].counter.resconsumeremains[i]/mult;
             resconsume := resconsume*gc_time_to_frames;     // gc_time_to_frames = 32
             var bank : Float = resconsumerem+resconsume*deltatime;
             var realbank : Float = bank/speed;              // speed = 20000
             var value : Integer = floor(realbank);
             if (value<>0) then
             begin
                if (not gPlayer[plInd].res[i]>=value) then
                begin
                   _res_AddResToPlayerByIndex(plInd, i, -value);
                   case i of
                      gc_resource_type_food : gPlayer[plInd].bfamine := False;
                      gc_resource_type_gold : gPlayer[plInd].brebellion := False;
                   end;
                end
                else
                begin
                   _res_AddResToPlayerByIndex(plInd, i, -(not gPlayer[plInd].res[i]));
                   case i of
                      gc_resource_type_food : gPlayer[plInd].bfamine := True;
                      gc_resource_type_gold : begin
                         if (gPlayer[plInd].counter.resconsume[i]>gPlayer[plInd].counter.resincome[i]) then
                         gPlayer[plInd].brebellion := True
                         else
                         gPlayer[plInd].brebellion := False;
                      end;
                   end;
                end;
             end;
             bank := (realbank-value)*speed;
             gPlayer[plInd].counter.resconsumeremains[i] := floor(bank*mult);
          end;
       end;
       ...
    end;
    ```
[^11]: Condition for an ongoing gold deficit — `lib/player.script:306`:
    ```pascal
    if (gPlayer[plInd].counter.resconsume[i]>gPlayer[plInd].counter.resincome[i]) then
       gPlayer[plInd].brebellion := True
    else
       gPlayer[plInd].brebellion := False;
    ```
[^12]: Final reset of `brebellion` — `lib/player.script:318-320`:
    ```pascal
    if (gPlayer[plInd].brebellion) and ((not gPlayer[plInd].res[gc_resource_type_gold]>=2)
       or (gPlayer[plInd].counter.resconsume[gc_resource_type_gold]<=0)) then
    gPlayer[plInd].brebellion := False;
    ```
[^13]: Rebellion check in the unit's `Nothing` handler —
    `units/unit.inc/nothing.inc:487-506`:
    ```pascal
    if (gPlayer[plInd].brebellion) and (TObjProp(pobjprop).bmercenary)
       and (plInd<>gc_player_mercenaryind) and (bplayable) then
    begin
       if (gInterface.gamemode=gc_gamemode_game) or (gInterface.gamemode=gc_gamemode_spectator) then
       begin
          if ((gPlayer[plInd].difficulty>1) and (_misc_RandomInt<6000))
             or ((gPlayer[plInd].difficulty=0) and (_misc_RandomInt<100))
             or ((gPlayer[plInd].difficulty=1) and (_misc_RandomInt<200)) then
          begin
             var plMercHnd : Integer = GetPlayerHandleByIndex(gc_player_mercenaryind);
             _misc_ChangePlayer(myHnd, plMercHnd, False, False, True);
          end;
       end
       else
       if (plHnd=GetPlayerHandleInterfaceIO) then
       begin
          var s1 : String = 'Rebel, but in editor mode your units wont die';
          ...
       end;
    end;
    ```
[^14]: `_misc_RandomInt` returns `floor(random × 32768)` —
    `lib/misc.script:494-498`. Constant `gc_c1rand_to_random = 32768`.

[^15]: `gc_player_mercenaryind = gc_MaxPlayerCount-1` —
    `dmscript.global:776`.

[^16]: Hostility of the mercenary NPC slot toward every normal player —
    `common.inc/initmap.inc:48-49`:
    ```pascal
    if i<>gc_MaxPlayerCount-1 then
    gPlayer[i].enemyplmask:=1 shl (gc_MaxPlayerCount-1);
    ```
[^17]: Starting resources of the mercenary NPC player —
    `lib/player.script:89-99`:
    ```pascal
    if (id=gc_player_mercenaryind) then
    begin
       case i of
          gc_resource_type_food : _res_SetResToPlayerByIndex(id, i, 10000);
          gc_resource_type_gold : _res_SetResToPlayerByIndex(id, i, 20000);
          gc_resource_type_iron : _res_SetResToPlayerByIndex(id, i, 10000);
          gc_resource_type_coal : _res_SetResToPlayerByIndex(id, i, 10000);
          else
          _res_SetResToPlayerByIndex(id, i, 10000);
       end;
    end
    ```
[^18]: AI weighting for defending units — `lib/unit.script:3941-3946`:
    ```pascal
    if (bcaptured) then
       scoremodifier := 5
    else
    if (gPlayer[pl].brebellion) and (TObjProp(pobjprop).bmercenary) then
       scoremodifier := 3
    else
       scoremodifier := 2;
    ```
[^19]: Constants `gc_mapsettings_marketdip_*` - `dmscript.global:1077-1081`.

[^20]: Applying the Expensive Mercenaries setting (`expensivemercs`) —
    `lib/player.script:2741-2774`:
    ```pascal
    gc_mapsettings_marketdip_expensivemercs : begin
       if (TObjProp(pobjprop).bmercenary) then
       begin
          var res : Integer;
          for res:=0 to gc_ResCount-1 do
          TObjBase(pobjbase).price[res] := TObjBase(pobjbase).price[res]*gc_gameplay_expensivemercskoef;
       end;
    end;
    ```
[^21]: `gc_gameplay_expensivemercskoef = 3` - `dmscript.global:214`.

[^22]: The `gPlayer.bneutral` field is declared in
    `lib/classes.script:3698`. Scenario scripts set and clear it in
    `lib/scenario.script:2182-2238`.

[^23]: Formation registration for mercenaries —
    `lib/country.script:2515-2535`.
    **Roundshier** (`roundshierdip`) and **Grenadier** (`grenadierdip`)
    use standard infantry formations. **Archer** (`archerdip`),
    **Turkish Archer** (`archerturdip`), and **Light Infantryman**
    (`lightinfantrydip`) use `…NoOfficersExtDip`.
