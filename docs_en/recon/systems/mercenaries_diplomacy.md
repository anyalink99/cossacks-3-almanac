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
- It recruits **six base mercenaries**; the Early Bird DLC adds **two more
  variants**. Every nation uses the same available roster and unit statistics.
- A mercenary costs **only gold**, consumes no food, and
  **continuously drains gold** as upkeep.
- When gold reaches zero while expenses exceed income, each mercenary can
  join an army hostile to every participant:
  - **Easy:** 0.305% per check;
  - **Normal:** 0.610% per check;
  - **Hard and above:** 18.31% per check.

---

<a id="1-дипломатические-здания-по-нациям"></a>
<a id="дипломатический-центр-у-разных-наций"></a>
## Diplomatic Centers by nation

Each of the 21 nations has one version of the building. Most European
nations share common statistics; Russia, Ukraine, Turkey, and Algeria have
their own values [^1] [^2].

| Building | Nations | Health | Build time | Wood | Stone | Gold | Capturable |
|---|---|---:|---:|---:|---:|---:|---|
| **Diplomatic Center** | Austria, France, England, Spain, Poland, Sweden, Prussia, Venice, Netherlands, Denmark, Portugal, Piedmont, Saxony, Bavaria, Hungary, Switzerland, Scotland | 4500 | 312.5 game seconds | 4900 | 1700 | 0 | No |
| **Diplomatic Center** | Russia | 6500 | 312.5 game seconds | 7900 | 3700 | 0 | No |
| **Diplomatic Center** | Ukraine | 5000 | 312.5 game seconds | 3900 | 2700 | 0 | No |
| **Diplomatic Center** | Turkey, Algeria | 5500 | 312.5 game seconds | 4600 | 2020 | 0 | No |

Construction requires an Academy. **The Diplomatic Center is not
capturable**, while its prerequisite Academy is.

---

<a id="2-каталог-наёмников"></a>
<a id="кого-можно-нанять"></a>
## Available mercenaries

Every nation receives the same six base mercenaries: **Light Infantryman**,
**Roundshier**, **Grenadier**, **Archer**, **Sich Cossack**, and
**Dragoon, 18th century**. The Early Bird DLC adds **Turkish Archer** and
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

| Mercenary | Availability | Health | Recruit time, game seconds | Gold | Gold upkeep | Price growth, % | Weapon: damage / range, cells |
|---|---|---:|---:|---:|---:|---:|---|
| **Light Infantryman** | Base game | 50 | 1.25 | 4 | 4 | 100 | sword: 16 / 0.94 |
| **Roundshier** | Base game | 75 | 1.5 | 12 | 20 | 100 | sword: 6 / 0.94 |
| **Archer** | Base game | 20 | 1.25 | 15 | 16 | 100.5 | arrow: 25 / 13.13; fire arrow: 100 / 14.06 |
| **Turkish Archer** | Early Bird | 20 | 1.25 | 15 | 16 | 100.5 | same as Archer |
| **Grenadier** | Base game | 30 | 1.5 | 25 | 60 | 100.5 | pike: 30; bullet: 16 / 15; grenade: 200 / 7.5 |
| **Sich Cossack** | Base game | 150 | 2.5 | 60 | 150 | 100.5 | cavalry sabre: 8 / 0.38 |
| **Dragoon, 18th century** | Base game | 100 | 2 | 120 | 120 | 102 | cavalry bullet: 18 / 15 |
| **Light Cavalry** | Early Bird | 100 | 2 | 120 | 120 | 102 | same as Dragoon, 18th century |

Every mercenary branch disables food upkeep and leaves only gold in the
recruitment price [^8]. **Mercenaries therefore cost only gold** and consume
no food (see [hunger and army upkeep](../world/economy/hunger_and_rebellion.md)).

<a id="23-масштабирование-цены-и-общий-счётчик"></a>
<a id="рост-цены-и-общие-счётчики"></a>
### Price growth and shared counters

The price-growth figure in the table is 100%, 100.5%, or 102%. The next
mercenary's price is calculated as follows [^9]:

**price = base price × (growth percentage / 100)<sup>N</sup>, rounded down**,

where N is the number of units previously recruited in the corresponding
group. Archer shares this counter with Turkish Archer, while Dragoon,
18th century shares one with Light Cavalry. Recruiting 100 Turkish Archers
therefore raises the regular Archer's price; the same rule applies to the
second pair.

A mercenary's price can rise to at most **twice its base price**. By
comparison, a regular unit can reach the technical ceiling of 20,000 times its
base price. At 100.5% growth, the 2× limit is reached after roughly
**ln(2) / ln(1.005) ≈ 139** shared recruits, after which the price remains
flat.

---

<a id="3-механика-upkeep--потребление-золота"></a>
<a id="3-содержание-за-золото"></a>
<a id="содержание-за-золото"></a>
## Gold upkeep

Gold upkeep is charged through the same continuous calculation as food
(see [hunger and army upkeep](../world/economy/hunger_and_rebellion.md)).
Fractional costs accumulate every frame, and whole units are periodically
deducted from the treasury [^10]. If the stockpile is insufficient, the game
spends the remainder and checks whether rebellion should begin.

<a id="скорость-утечки-золота"></a>
### Gold drain rate

The formula uses the values in the Gold upkeep column:

**gold per game second = total upkeep of all units × 32 / 20,000**.

One mercenary **Dragoon, 18th century** with an upkeep value of 120 drains
**120 × 32 / 20,000 = 0.192** gold per game second, or about
**11.5 gold per game minute**. Fifty of them drain 9.6 gold per game second,
or 576 per game minute—a cost that generally requires a Market and several
Gold Mines.

<a id="bfamine-vs-brebellion--асимметрия"></a>
<a id="различие-голода-bfamine-и-бунта-brebellion"></a>
<a id="почему-пустая-казна-не-всегда-вызывает-бунт"></a>
### Why an empty treasury does not always cause rebellion

Briefly reaching zero gold is not enough. Two conditions must hold at the
same time: the stockpile is empty and gold upkeep exceeds current income
[^11]. If Gold Mines fully cover upkeep, mercenaries remain loyal even with
an empty treasury.

Rebellion ends when the stockpile reaches at least two gold or mercenary
upkeep falls to zero [^12]. Disbanding every mercenary therefore ends the
crisis immediately.

---

<a id="4-триггер-бунта"></a>
<a id="4-как-начинается-бунт"></a>
<a id="как-начинается-бунт"></a>
## How rebellion begins

Once rebellion begins, every living mercenary makes a separate random check
while idle or moving [^13] [^14]:

| Difficulty | Successful outcomes out of 32,768 | Probability per background check |
|---|---:|---:|
| Easy | 100 | 100 / 32,768 ≈ **0.305%** |
| Normal | 200 | 200 / 32,768 ≈ **0.610%** |
| Hard, Very Hard, or Impossible | 6,000 | 6,000 / 32,768 ≈ **18.31%** |

On Hard and above, a typical mercenary needs about **five or six relevant
checks** before deserting. This is a per-check risk estimate, not a timer:
elapsed time also depends on the interval between unit-state updates.

After a successful check, the unit joins a game-controlled side that is
hostile to every normal participant [^15] [^16].

Therefore, deserted mercenaries become hostile to **everyone**, including
their former owner. They remain alive.

The game-controlled army starts with 20,000 gold and 10,000 of every other
resource [^17]. Deserters continue paying upkeep but cannot change sides
again.

<a id="реакция-ai"></a>
<a id="реакция-ии"></a>
<a id="штраф-к-очкам"></a>
### Score penalty

When a rebellious mercenary changes sides, **three times the unit's base
value** is immediately deducted from the former owner's score [^18]. The new
owner receives the unit's base value **once** during the same transfer.
This is a penalty for the **ownership transfer during rebellion**, not for
the unit's later death or loss.

For comparison, removing an ordinary object from the former owner's counters
uses twice its base value, while a previously captured object uses five times.
Score affects the final statistics, but it does not change computer-player
decisions or decide the match.

---

<a id="5-map-настройка-marketdip"></a>
<a id="5-настройка-лобби-рынок-и-дипломатический-центр-marketdip"></a>
<a id="настройка-лобби-рынок-и-дипломатический-центр"></a>
## “Market and Diplomatic Center” lobby setting

The setting has five options [^19]:

| Option | Result |
|---|---|
| Default | Markets and Diplomatic Centers are available |
| Without dip. center | Diplomatic Centers are unavailable |
| Without market | Markets are unavailable |
| Without both | Both buildings are unavailable |
| Expensive Mercenaries | Every mercenary's recruitment price is tripled |

With Expensive Mercenaries, prices change from 4 to 12, 60 to 180, 120 to
360, 150 to 450, and so on [^20] [^21]. Mercenaries are bought only with
gold, so the player sees a tripled gold price. The complete list is in the
[lobby settings reference](../../reports/map/lobby_settings.md#marketdip--рынок-и-дипцентр).

---

<a id="6-нейтральные-дипцентры--точки-найма"></a>
<a id="6-есть-ли-нейтральные-точки-найма"></a>
<a id="6-где-нанимают-наёмников"></a>
<a id="где-нанимают-наёмников"></a>
## Where Mercenaries Are Recruited

On a standard random map, **mercenaries are recruited only from the
player's own Diplomatic Center**, with the prerequisites listed above. The
game-controlled army that receives deserters owns no recruitment buildings.

A scenario author can place a neutral Diplomatic Center in a mission, but
that is a rule of the scenario rather than a standard random-map mechanic.

---

<a id="7-кросс-национальная-доступность"></a>
<a id="7-доступность-для-разных-наций"></a>
<a id="доступность-для-разных-наций"></a>
## Availability across nations

**Any nation can recruit any mercenary.** Roundshier, Light Infantryman,
Archer, Grenadier, Sich Cossack, and Dragoon, 18th century are always
available. Light Cavalry and Turkish Archer require the Early Bird DLC [^5].

The apparent national distinction between the paired versions is purely a
**visual/model variant**. The Archer and Turkish Archer, as well as the
Dragoon and Light Cavalry, share statistics and a price counter
([see price growth](#price-growth-and-shared-counters));
only their Western or Eastern appearance differs.

Formation rules differ slightly [^23]. **Roundshiers** and **Grenadiers**
can join standard infantry formations with national Pikemen and Musketeers.
**Archers**, **Turkish Archers**, and **Light Infantrymen** form their own
formations without a national Officer.

---

<a id="8-наёмник-vs-обычный-юнит--сравнение"></a>
<a id="8-сравнение-с-обычными-юнитами"></a>
<a id="сравнение-с-обычными-юнитами"></a>
## Comparison with regular units

<a id="стоимость"></a>
### Cost

Mercenaries require **only gold and recruitment time**. Regular units may
also require food, iron, and coal, then consume food as upkeep. A heavy
mounted shooter illustrates the trade-off:

| Unit | Food | Iron | Coal | Gold | Shot cost | Health | Recruit time |
|---|---:|---:|---:|---:|---|---:|---:|
| **Dragoon, 18th century** (regular European) | 70 | 7 | 0 | 60 | 4 iron + 5 coal | 225 | 22.5 game seconds |
| **Dragoon, 18th century (mercenary)** | 0 | 0 | 0 | 120 | 5 iron + 8 coal | **100** | **2 game seconds** |

The mercenary costs 60 more gold and no food, iron, or coal at
recruitment. It is **recruited eleven times faster**, but has only 44%
of the regular Dragoon's health, costs slightly more iron and coal per
shot, and continuously drains gold. The **Archer** follows a similar
pattern: the mercenary version recruits slightly more slowly, costs no
food, and deals 25 rather than 15 damage.

<a id="содержание"></a>
### Upkeep

- An ordinary famine-vulnerable unit receives a common surcharge of 30 on top
  of its personal upkeep value. Food consumed per game second equals that
  total multiplied by 32 / 20,000 (see
  [hunger and army upkeep](../world/economy/hunger_and_rebellion.md)).
  Mercenaries drain no food.
- The Gold upkeep value in the table ranges from 4 to 150. The cost per game
  second is that value multiplied by 32 / 20,000.
- Officers and Royal Musketeers also consume gold, but they are not
  mercenaries and cannot rebel.

<a id="когда-брать-наёмников-стратегический-профиль"></a>
### Strategic use

Mercenaries are essentially a **rapid-deployment army bought with gold**:

- **Early game.** Nations with abundant wood and poor access to iron or coal
  can exchange wood and stone for gold at the Market, then quickly recruit
  Roundshiers or Light Infantrymen.
- **Mid-game.** A gold surplus from allied trade or captured Gold Mines
  can become a Dragoon army without waiting for Coal Mines.
- **Low durability, fast deployment.** Mercenaries often have roughly half
  the health of comparable regular units, but the high-tier recruitment
  advantage is enormous: the mercenary Dragoon takes 2 game seconds versus
  22.5 for the regular unit, **11.25 times faster**.

**The main risk is an interruption to gold income.** If gold income falls
below upkeep and the reserve reaches zero, mercenaries begin making frequent
desertion checks on Hard and above. Disbanding
mercenaries **before** the reserve is exhausted avoids this.

---

<a id="технические-подробности"></a>
## Technical details

Exact fields, handlers, and branches removed from the reader-facing sections
are grouped in the sources below: price calculation and paired identifiers in
[^9], upkeep accumulation and deficit conditions in [^10] [^11] [^12],
rebellion checks and the game-controlled owner in [^13] [^14] [^15] [^16]
[^17], score changes in [^18], and lobby-setting branches in [^19] [^20]
[^21].

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

On random maps, normal players have `bneutral = False`; scenario actions
change that field [^22]. The service owner `gc_player_mercenaryind` has no
buildings and exists only to receive deserters. Roundshier and Grenadier use
the standard officer-formation registration, while Archer, Turkish Archer,
and Light Infantryman use the `…NoOfficersExtDip` branch [^23].

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

[^5]: Registration of six base mercenaries and two Early Bird variants
      through `_country_AddMember` —
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
[^6]: Production setup for six base and two additional mercenaries —
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
[^18]: Former-owner score penalty on object loss —
       `lib/unit.script:3941-3947`:
    ```pascal
    if (bcaptured) then
       scoremodifier := 5
    else
    if (gPlayer[pl].brebellion) and (TObjProp(pobjprop).bmercenary) then
       scoremodifier := 3
    else
       scoremodifier := 2;
    ```

    The next statement performs
    `gPlayer[pl].counter.scores -= score * scoremodifier`.
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
