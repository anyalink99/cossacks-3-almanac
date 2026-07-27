<a id="recon-поведение-ии"></a>
<a id="как-играет-компьютер"></a>
# How the Computer Player Works

[← How the game works](../README.md)

This article explains how the computer player develops its economy, recruits
an army, and decides when to attack. Internal names and Pascal excerpts are
collected in the [technical source map](#technical-source-map) and
[Sources](#sources).

<a id="кратко"></a>
## Key points

- The computer revisits economic and military decisions once every
  **2.4 game seconds**.
- **Difficulty primarily changes construction and recruitment speed:**
  from 30% of the player's rate on Easy to 100% on Very Hard. The scenario-only
  Impossible level uses 125%. The AI receives **no extra starting resources**.
- **The build order is rule-based and nation-specific.** It uses neither
  machine learning nor a random plan; a sequence of conditions examines
  the current game state.
- **The first offensive wave** consists of five squads. Once assembled,
  they enter the normal offensive logic, which selects one of the enemies.
- **Diplomacy is static:** teams come from the lobby, and the AI neither
  forms nor breaks alliances during a match.

<a id="уровни-сложности"></a>
## Difficulty levels

The interface shows four levels: Easy, Normal, Hard, and Very Hard. A fifth
level, Impossible, is reserved for scenarios, including Historical Battles
[^4] [^5] [^6]. The full table of multipliers is in
[lobby settings](../../reports/map/lobby_settings.md#difficulty--сложность);
the corresponding engine behavior is covered under
[match settings](../world/map/game_settings.md) §4.

<a id="что-меняется-между-уровнями"></a>
### What changes between levels

<a id="1-скорость-постройки-и-найма--главный-чит"></a>
<a id="1-скорость-постройки-и-найма"></a>
#### 1. Construction and recruitment speed

The difficulty factor multiplies construction and recruitment progress [^10]:

- **Easy** — **30%** of player speed (3.33 times slower);
- **Normal** — 50% (twice as slow);
- **Hard** — 75%;
- **Very Hard** — equal to the player;
- **Impossible** — 125%, the only level with an advantage.

<a id="2-лимит-апгрейдов-башни"></a>
<a id="2-лимит-улучшений-башни"></a>
#### 2. Tower upgrade limit

Maximum tower upgrade level: Easy = 2, Normal = 3, Hard = 4,
Very Hard = 5, Impossible = 5 [^12].

<a id="3-размер-диверсионных-групп"></a>
<a id="3-подготовка-диверсий"></a>
#### 3. Preparing sabotage forces

Easy and Normal set no positive recruitment increment for saboteurs; Hard
uses 2, while Very Hard and Impossible use 4 [^13]. These values are **not
army counts**: they contribute to the recruitment target for **Sich Cossacks
(mercenaries)** intended for later raids. A separate military check permits
no more than **two active sabotage armies at once**.

<a id="4-лимит-апгрейдов-шахты"></a>
<a id="4-лимит-улучшений-шахты"></a>
#### 4. Mine upgrade limit

Easy is limited to level 0, Normal to level 2 or 3, and higher
difficulties to level 7 [^14].

<a id="5-базовые-ворота-через-if-difficulty--easy"></a>
<a id="5-ограничения-лёгкого-уровня"></a>
#### 5. Restrictions on Easy

Easy skips several economic and military upgrades and does not build
Howitzers or Bombards [^15]. The exact internal codes are listed in the
technical section.

<a id="6-дополнительные-проверки-на-hard"></a>
<a id="6-дополнительные-проверки-на-сложном-уровне-и-выше"></a>
#### 6. Additional checks on Hard and above

From Hard upward, the computer can recruit emergency **Dragoons, 18th century**
from the Diplomatic Center when gold is scarce [^16].

<a id="7-bricks1--только-veryhard-и-impossible"></a>
<a id="7-bricks1--только-на-очень-сложном-и-невозможном-уровнях"></a>
<a id="7-дополнительное-экономическое-улучшение"></a>
#### 7. Additional economic upgrade

Very Hard and Impossible allow the additional **Use new construction
materials (durability of buildings +85)** upgrade; the lower difficulty
levels skip it [^17].

<a id="8-поблажка-игроку-на-низких-уровнях"></a>
#### 8. Assistance for the player at low levels

On Easy and Normal, the player's ranged units are less readily forced into
their idle behavior, making them easier to control [^18]. This assists the
**player**, not the AI.

<a id="что-не-меняется-по-сложности"></a>
### What difficulty does not change

- **Starting resources.** Every player receives the same lobby-selected
  amount: 1,000, 4,000, 5,000, or 1,000,000 of each resource [^19].
  AI does not receive bonus resources at any level.
- **Income.** The computer gathers resources through the normal economy.
  Its resource-balance settings change gathering, production, and trade
  priorities; they do not grant free resources.
- **Game speed.** The selected speed is shared by every participant; the
  simulation is not accelerated separately for the AI.

<a id="порядок-строительства"></a>
## Build order

The economic AI is **adaptive but rule-based**. It repeatedly checks which
buildings already exist and how many Peasants and resources it has, then
selects the next available construction target.

The main phases are [^20]:

1. Starts with one or two **Town Halls**, a **Market**, and a **Mill**.
2. Algeria and Turkey may add **Housing** when they already have a
   Blacksmith, Storehouse, Market, and **Barracks, 17th century**.
3. Searches for available **Gold, Iron, and Coal Mines** [^21].
4. One **Blacksmith**.
5. **Barracks, 17th century**: target counts of 1 → 2 → 3 →
    6 or 8 depending on Town Hall count and whether the map is naval.
    Most nations aim for eight; Russia aims for six [^22].
6. After the second Town Hall, expands toward **five Town Halls**.
7. An **Academy** after at least two **Barracks, 17th century** and two
   Town Halls.
8. A **Stable**, **Artillery Depot**, **Diplomatic Center**, and **Cathedral** after the Academy.
9. **Barracks, 18th century** after advancing to the 18th century.
10. Up to three **Towers** after an Academy, once military AI is active
    above Easy: one per 75 Peasants, with a maximum of three [^23].

Build order varies substantially among the 21 playable nations. Ukraine
often skips the **Barracks, 17th century** and **Officer, 17th century**
chain in favor of mass **Musketeers, 17th century**. Algeria and Turkey
recruit **Archers** through the Academy. Russia limits itself to six
Barracks when the **Millions** starting-resources preset is selected.

Build order checkpoints (representative):

- two **Barracks, 17th century** and two Town Halls → Academy [^24];
- two **Barracks, 17th century** and four Town Halls → resource balance
  shifts toward gold [^25];
- at least five **Barracks, 18th century** → three more
   Barracks, 17th century and a sixth Town Hall [^26];
- 144 **Pikemen, 17th century** → recruit both Pikemen and
  **Musketeers, 17th century** [^27];
- 372 **Pikemen, 17th century** → recruit only Musketeers [^28].

Resource priorities adapt to the Peasant count. The food weight rises
through 12 → 21 → 27 → 36 → 45 at thresholds of 30, 45, 85, and
120 Peasants, with a ×1.3 multiplier while Pikemen remain unupgraded [^29].
Russia and Poland use 16 → 24 → 31 → 40 → 49 instead.

<a id="цели-по-производству"></a>
## Production goals

The computer does not set a final army size. It gives production buildings
the next set of targets instead. When a unit count falls below its target,
recruitment resumes during a later decision cycle [^30].

<a id="крестьяне"></a>
### Peasants

The production rule has two thresholds: **400 Peasants in total** across
all controlled nations and **30 Peasants for the current nation** [^31].
Recruitment continues until both thresholds have been reached. Therefore
400 is not an absolute total cap while one nation still has fewer than
30 Peasants, and 30 is not a per-nation cap while the total remains below
400. Each Town Hall adds two Peasants to the next replenishment request;
a separate check can then reduce the target [^32].

<a id="военные-цели"></a>
### Military targets

The main targets are [^33]:

- one Officer per 36 **Pikemen, 17th century**, with the first Officer
  requested after 28 Pikemen;
- two Reiters per Stable;
- two 18th-century infantrymen per **Barracks, 18th century**;
- two 17th-century infantrymen per **Barracks, 17th century**;
- six Cannons per Artillery Depot, clamped to a total of 6–30;
- two Howitzers per depot, clamped to 2–8;
- eight Bombards per depot, clamped to 8–40;
- **Dragoons, 18th century** and Pikemen depend on the nation and researched
  cavalry upgrades;
- Algeria and Scotland aim for roughly one Archer per three occupied
  population places, or one per five on a naval map.

These are **queue targets**, not hard limits. After 372 **Pikemen,
17th century**, the relevant queue switches to **Musketeers, 17th century**
only [^34]. Exact formulas and internal names are retained in the
[technical details](#exact-production-rules).

<a id="триггеры-агрессии-и-атаки"></a>
## When the AI attacks

The military logic gathers ready units into squads, chooses a target, and
periodically revisits that decision [^35] [^36].

- **First offensive wave:** the computer sends five mobile squads as soon
  as all five are ready. Later waves use the ordinary attack logic [^37].
- Before forming up, it can wait as long as 20 game seconds at Normal speed
  for a Drummer or Officer.
- **Retreat:** an army with more than 200 units or a force score above 3,800
  is treated as overwhelmingly strong and does not retreat. For smaller
  armies, the score may be multiplied by eight for a major advantage or by
  two for a minor advantage; retreat begins if the enemy is still stronger
  after that adjustment [^38].
- **Raid:** a nearby weaker force is attacked immediately; a more distant
  target can also trigger an advance within a wider search. The two internal
  radii are 30 and 400.
- **Wall attack:** nearby non-artillery squads switch to the wall.
  Artillery is excluded from this group order.
- **Peacetime** blocks every offensive and raid branch until it ends
  [^39] [^40].

Exact constants and the internal order-state list are retained in the
[technical details](#military-constants-and-order-states).

<a id="читы"></a>
<a id="преимущества-и-ограничения-по-сложности"></a>
## Difficulty advantages and handicaps

| Level | Effect | Construction and recruitment speed |
|---|---|---|
| Easy | Strong handicap | 30% of player speed |
| Normal | Handicap | 50% |
| Hard | Mild handicap | 75% |
| Very Hard | Parity | 100% |
| Impossible | Advantage | 125% |

In an ordinary match, these factors apply to all AI construction and
recruitment [^10]. A service mode that attaches AI logic to a
human-controlled player bypasses the slowdown and uses full speed regardless
of difficulty [^43].

**AI receives no extra starting resources.** Humans and AI receive the same
lobby-selected amount: 1,000 / 4,000 / 5,000 / 1,000,000 of each resource
[^19].

The computer gathers through the normal economy and discovers deposits only
after its own units reveal them. Its gameplay logic applies no separate
movement-speed multiplier [^44].

<a id="дипломатия"></a>
## Diplomacy

- Teams are set in the lobby. Players on different teams become enemies;
  “no team” also makes a player an enemy to everyone [^45].
- Computer players on the same team are friendly and do not attack one
  another; players on different teams are enemies [^46].
- **Teams remain fixed on random maps.** The computer continues to use the
  lobby assignments. Scenarios can change relationships during a mission,
  while ordinary random-map logic does not.
- AI treats all enemies **symmetrically**: it selects the next target at
  random [^47]. It does not prioritize
  weaker opponents or maintain a persistent “vendetta.”

<a id="исходные-файлы"></a>
<a id="техническая-карта-исходных-файлов"></a>
## Technical source map

The full cycle runs every 2.4 game seconds:
`gc_global_TimeProgressAI = 0.03 × 16 × 5` [^1]. The next update is offset
by `id × 0.25`, preventing all computer players from deciding on the same
tick [^2]. The dispatcher then runs the economic and military phases in
sequence [^3].

The internal levels are `easy`, `normal`, `hard`, `veryhard`, and
`impossible`; no AI is represented by `none = -1`. The choice is stored in
`gMap.players[i].aidifficulty` and copied to `gPlayer[i].difficulty`
[^7] [^8] [^9]. The multiplier applies to `deltabuildtime`;
`aiData.bhumanai` disables it [^10] [^11].

Easy skips `bricks1`, `fort`, `armor1`, `accurency1`, `artlife`, and
`horseswords` [^15]. A separate `bricks1` check enables it only on Very
Hard and Impossible [^17]. The sabotage-mercenary recruitment factor is
stored in `numdiver`, while `gc_ai_MaxDiverArmies` caps armies already in
the field [^13].

<a id="точные-производственные-правила"></a>
### Exact production rules

The starting-resource setting is stored in `resourcestart`, while global
game speed uses `gc_settings_gamespeed_*`. Build-order checks use
`centercount`, `ba17_count`, and `ba18_count`; the Tower target is
`numTowers = Min(3, peasants div 75)` [^23].

The `_ai_RequestUnitsProduction` dispatcher passes targets to `_ai_TryUnit`;
`_ai_DecreasePeasants` separately reduces the Peasant target [^30] [^32].
Exact military expressions are [^33]:

| Target | Internal expression |
|---|---|
| Officers | `numOfficers = pikemanCount div 36`; minimum 1 when `pikemanCount > 28` |
| Reiters | `numReiters = stable_count × 2` |
| 18th-century infantry | `numInf18 = ba18_count × 2` |
| 17th-century infantry | `bar_count = ba17_count × 2` |
| Cannons | `cannon_count = ClampInt(num_depo × 6, 6, 30)` |
| Howitzers | `howitzer_count = ClampInt(num_depo × 2, 2, 8)` |
| Bombards | `mortar_count = ClampInt(num_depo × 8, 8, 40)` |
| Archers for Algeria and Scotland | `_ai_GetUnitCount < farmused / 3`; `/ 5` on a naval map |

**Dragoons, 18th century** and Pikemen depend on nation and
`gc_ai_upg_horse`. The Musketeer-only transition uses
`36 × 7 + gc_ai_max_guards`, where `gc_ai_max_guards = 120`; the internal
Musketeer code is `musk17` [^28] [^34].

<a id="военные-константы-и-состояния-приказов"></a>
### Military constants and order states

| Name | Value | Purpose |
|---|---:|---|
| `gc_ai_AgressorsCount` | 5 | squads in the first offensive wave |
| `gc_ai_MaxDiverArmies` | 2 | internal cap on simultaneously active sabotage armies |
| `gc_ai_OfficerWaitTime` | 20 | wait for a Drummer or Officer at Normal speed |
| `gc_ai_GreArmyBattleDist` | 2 | local Grenadier search radius |
| `gc_ai_ArmyBattleDist` | 4 | ordinary local search radius |
| `gc_ai_BitvaInterval` | 8 | battle recheck interval |
| `gc_ai_CityDangerDist` | 20 | enemy-army proximity threshold around the city center when placing a merged army |
| `gc_ai_MergeArmyCityDist` | 25 | distance from the city center within which the merged army's position is adjusted |
| `gc_ai_MergeApproachDist` | 10 | distance by which a merged army is shifted towards the selected enemy when the city is not in danger |
| `gc_ai_MinStoreHouseDist` | 9 | minimum path distance from a suitable resource area to an existing Storehouse |

The `gc_ai_armyorder_*` enumeration contains `none`, `makebattle`, `bitva`,
`buildmine`, `sabotage`, `agressor`, `makewaterbattle`, `transport`, and
`attackwall` [^36]. The first wave uses `_ai_SendAgressors`; later waves use
`_ai_ArmyMakeBattleLink`. Retreat uses `_ai_GetArmyForce`, raids use the
`_ai_ArmyDiversia*` family, and wall attacks use
`_ai_ArmyCheckWallAttack` with `searchRadius` [^37] [^38]. Peacetime is
represented by `gbool_peacemode` [^39] [^40].

A player's team is stored in `gPlayer[i].team`. `_ai_IsTeamAI`,
`_ai_IsEnemiesExists`, and `_ai_GetRandomEnemy` respectively test for AI
inside a team, scan for enemies, and select a random target [^42] [^46]
[^47]. The scenario action
`gc_trigger_action_player_playerSetAsAlly = 19` can change relationships,
but random-map AI does not call it.

| Path | Size | Role |
|---|---:|---|
| `lib/ai.script` | 95.6 KB | Helper library: army queries (`_ai_GetArmyForce`, `_ai_GetArmyUnitsCount`), unit-role mappings (`_ai_FillUnitUpgradeList`), upgrade tables, deposit discovery, `_ai_IsTeamAI`, and `_ai_GetCommonNationName` (four groups: `rus`, `tur`, `mis`, `eur`). |
| `units/global.inc/progressai.inc` | 0.8 KB | **Dispatcher.** Each `gc_global_TimeProgressAI` tick calls `ProgressEconomicAI`, then `ProgressWarAI`. |
| `units/global.inc/progresseconomicai.inc` | 226 KB | Economic AI: build order, production goals, resource balance, choice of upgrades. |
| `units/global.inc/progresswarai.inc` | 223 KB | Military AI: army formation, attack/withdrawal decisions, sabotage groups, transport operations. |
| `misc/airegion.aix` | 3.0 KB | AI zone triggers for scenarios. Has nothing to do with the main AI. |

<a id="источники"></a>
## Sources

All links are relative to `data/scripts/` in the Cossacks 3 installation.

[^1]: `gc_global_TimeProgressAI = 0.03 × 16 × 5 = 2.4` — `dmscript.global:1486`.

[^2]: Shift `lastprogressaitime` by player-id — `player.script:140`:
    ```pascal
    lastprogressaitime := id * 0.25 + gc_global_TimeProgressAI;
    ```
[^3]: Dispatcher — `units/global.inc/progressai.inc`:
    ```pascal
    ExecuteState('ProgressEconomicAI');
    ExecuteState('ProgressWarAI');
    ```
[^4]: Listing difficulty levels - `dmscript.global:781-786`:
    ```pascal
    gc_player_difficulty_none       = -1;
    gc_player_difficulty_easy       =  0;
    gc_player_difficulty_normal     =  1;
    gc_player_difficulty_hard       =  2;
    gc_player_difficulty_veryhard   =  3;
    gc_player_difficulty_impossible =  4;
    ```
[^5]: `gc_MaxAIDifficultyCount = 4` - `dmscript.global:235`.

[^6]: Impossible for historical battles - `initmaphistoricalbattle.inc:121`.

[^7]: The `aidifficulty` field in the map-player record —
    `classes.script:105`.

[^8]: Copying to `gPlayer[i].difficulty` at startup - `initmapgen.inc:132`.

[^9]: Defaulted `easy` in the lobby - `map.script:244`, `player.script:118`.

[^10]: `deltabuildtime` multiplier on AI difficulty - `building.inc/doprogressorders.inc:222-230`:
    ```pascal
    if (gPlayer[plind].bai) and (not gPlayer[plInd].aiData.bhumanai) then
    case gPlayer[plind].difficulty of
       gc_player_difficulty_easy       : deltabuildtime *= 0.30;
       gc_player_difficulty_normal     : deltabuildtime *= 0.50;
       gc_player_difficulty_hard       : deltabuildtime *= 0.75;
       gc_player_difficulty_veryhard   : deltabuildtime *= 1.00;
       gc_player_difficulty_impossible : deltabuildtime *= 1.25;
    end;
    ```
[^11]: Default `aiData.bhumanai = False` - `classes.script:2688`.

[^12]: The tower upgrade limit is `progresseconomicai.inc:3653-3658`.

[^13]: Preparing sabotage forces — `progresseconomicai.inc:2321-2331`;
    active-army cap — `progresswarai.inc:2972-2980`:
    ```pascal
    case difficulty of
       gc_player_difficulty_normal     : numdiver := 0;
       gc_player_difficulty_hard       : numdiver := 2;
       gc_player_difficulty_veryhard   : numdiver := 4;
       gc_player_difficulty_impossible : numdiver := 4;
    end;
    numdiver := numdiver + _ai_GetDiverArmiesCount(plInd);
    _ai_TryUnit(plind, cid, gc_ai_unit_cossackdip, 10*numdiver, False);
    // Separately: aCount < gc_ai_MaxDiverArmies (= 2)
    ```
[^14]: The mine upgrade limit is `progresseconomicai.inc:2202-2212` and `~2396-2410`.

[^15]: The Easy difficulty disables Howitzers and Bombards —
    `progresseconomicai.inc:2349-2353`.

[^16]: Emergency hiring of mercenaries at `difficulty >= hard` - `progresseconomicai.inc:2306`.

[^17]: `bricks1` is restricted to Very Hard and Impossible —
    `progresseconomicai.inc:2452`.

[^18]: Relaxed ranged-unit control for the player at `<= normal` —
    `unit.script:7367`.

[^19]: The distribution of starting resources is the same for all players - `initmapgen.inc:166-189`.

[^20]: Main build-order phases — `progresseconomicai.inc:2700-2830`.

[^21]: Mine ranges - `dmscript.global:503-506` (`gc_ai_dist_mines_lvl1 = 30`, `lvl2 = 60`, `expansion = 85`).

[^22]: Target number of **Barracks, 17th century** (`ba17`) —
    `progresseconomicai.inc:2771`:
    ```pascal
    _ai_TryUnit(plind, cid, gc_ai_unit_ba17, 8, False)
    // 6 for Russia
    ```

[^23]: Towers — `progresseconomicai.inc:2926-2929`:
    ```pascal
    numTowers := Min(3, peasants div 75);
    ```
[^24]: Two **Barracks, 17th century** (`ba17`) and two Town Halls unlock the
    Academy — `progresseconomicai.inc:2796`.

[^25]: Two **Barracks, 17th century** and four Town Halls shift resource
    priorities toward gold — `progresseconomicai.inc:2036-2039`.

[^26]: At least five **Barracks, 18th century** (`ba18`) lead to three more
    **Barracks, 17th century** and a sixth Town Hall —
    `progresseconomicai.inc:2789-2793`.

[^27]: `pikemanCount ≥ 36 × 4` enables both **Pikemen, 17th century** and
    **Musketeers, 17th century** —
    `progresseconomicai.inc:2134`.

[^28]: `pikemanCount ≥ 36 × 7 + gc_ai_max_guards` switches production
    to **Musketeers, 17th century** (`musk17`) only —
    `progresseconomicai.inc:2152-2158`.

[^29]: Food balance by number of peasants - `progresseconomicai.inc:1999-2031`.

[^30]: `_ai_RequestUnitsProduction` - `progresseconomicai.inc:2085+`.

[^31]: Peasant cap — `progresseconomicai.inc:2088`:
    ```pascal
    var numpeasants : Integer = _ai_GetUnitCount(plind, cid, gc_ai_unit_center) * 2;
    if (peasants_total < 400) or (peasants_this_nation < 30) then
       if food < 700 then queue numpeasants
       else queue 1
    ```
[^32]: `_ai_DecreasePeasants` - `progresseconomicai.inc:3856`.

[^33]: Targets for military units - `progresseconomicai.inc:2103-2150` (and further `:2347`, `:2351`, `:2352` for guns, howitzers and mortars).

[^34]: `gc_ai_max_guards = 120` - `dmscript.global:500`.

[^35]: Aggression and attack constants - `dmscript.global:474-481`.

[^36]: Enumeration `gc_ai_armyorder_*` - `dmscript.global:430-438`.

[^37]: First aggressor wave - `progresswarai.inc:3560-3568` (`_ai_SendAgressors`):
    ```pascal
    if (not gbool_peacemode) and (agressorsSent = 0) and
       (agressors.GetCount >= gc_ai_AgressorsCount) then
    begin
       pArmy := _ai_CreateAgressorArmy(plInd, 5, agressors);
       _ai_ArmyMakeAgressorBattle(pArmy);
    end;
    ```
[^38]: Retreat logic - `progresswarai.inc:2398-2407`:
    ```pascal
    myForce := _ai_GetArmyForce(pArmy);
    if (uCount > 200) or (myForce > 3800) then
       myForce := 100000;
    // otherwise myForce *= 8 (heavy) or *= 2 (light)
    if (enForce > myForce) then ...retreat...
    ```
[^39]: Installation `gbool_peacemode` - `dogenerate.inc:2060-2064`.

[^40]: Early-exit aggression and sabotage during peacetime - `progresswarai.inc:2787` and `:3562`.

[^41]: Hostility by `team` - `initmapgen.inc:160`.

[^42]: `_ai_IsTeamAI` - `ai.script:527`.

[^43]: Field `bhumanai` - `classes.script:2611`.

[^44]: AI resource visibility is `ai.script:228` (`_ai_FillOreList` uses `GetGameObjectVisibleByHandle`).

[^45]: Initializing relationships by command - `initmapgen.inc:158-163`:
    ```pascal
    if (myteam <> histeam) or (histeam = 0) or (myteam = 0) then
       AddPlayerEnemyPlayerByHandle(...)
    else
       AddPlayerFriendPlayerByHandle(...);
    ```
[^46]: `_ai_IsEnemiesExists` - `ai.script:7-19`.

[^47]: `_ai_GetRandomEnemy` - `progresseconomicai.inc:67-94`.

[^48]: Condition `aidata.centerfound = True` - `ai.script:451`.
