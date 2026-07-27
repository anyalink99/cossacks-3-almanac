<a id="known-issues--архив-исправленных-проблем"></a>
# Known Issues: Resolved

Entries move here from [`known_issues.md`](known_issues.md) after the parser or
dataset has been corrected. The archive records what changed in `data.json`
and why.

Format: correction date → brief description → previous and corrected behavior
→ commit or pull request, when available.

## 2026-04-30

<a id="bmercenary-override-не-разрешался--168-dip-юнитов-в-datajson-имели-не-наёмничьи-статы"></a>
### `bmercenary` override was not allowed - 168 dip units in `../data.json` had non-mercenary stats

**Was:** `parser/parse_units.py` did not take into account the `if (bmercenary)` branch in
`unit.script` for units with the suffix `dip` (8 sid × 21 nations = 168 lines).

**Fix:** added `BMERCENARY_SIDS` and `find_bmercenary_block_body()` to
[`parse_units.py`](../../parser/parse_units.py); `_compute_effective_unit()` in
[`build_data.py`](../../parser/build_data.py) applies merc-override to sids
from `BMERCENARY_SIDS`. At the same time, parsing `objprop.costpercent := X;` was added
for unit branches (3 non-merc units also had it: 1867, 1889, 2018
unit.script).

**Confirmed:** 8 dip-sid × 21 nations = 168 lines now have correct
merc stats - HP, gold, `consume.gold`, `bmercenary = True`, `bnohungry = True`,
`costpercent` (100 / 100.5 / 102) match
[`recon/systems/mercenaries_diplomacy.md`](../../docs_en/recon/systems/mercenaries_diplomacy.md) §2.2. Stat
identical between nations (nation-independent). 112 / 112 sanity checks PASS.

<a id="ценовые-проценты-priceperc-апгрейдов-не-извлекались"></a>
### Price percentages `priceperc` upgrades were not retrieved

**Was:** 291 priceperc upgrade in `../data.json` had the correct base price
research (food / wood / stone / gold / iron / coal), but **didn’t**
`resource_pcts` - percentage reduction in the cost of target units and buildings. These
interest is billed in `country.script` via
`country.upgrade[ind-1].sarrparam2[gc_upgrade_maxarrparam2count - gc_ResCount + gc_resource_type_X - 1] := 'NN';`
after `_country_AddUpgrade*` call. Existing `_attach_resource_pcts`
tried to re-resolve sid from text position and couldn't cope with per-nation
templates (`csid + 'art.' + member + ...`).

**Fix:** added handler to `walk_sim`'s `assign` branch
([`simulate_upgrades.py:870-887`](../../parser/simulate_upgrades.py)) —
`_SARR2_RES_LHS_RE` recognizes LHS, parses RHS as a percentage and assigns
`state["last_upgrade"]["resource_pcts"][resource]`. AST has already treated these
assigns are correct - the handler ignored them.

**Confirmed:** 291 / 291 priceperc upgrades have `resource_pcts` (previously
0 / 291). The numbers match the direct reading `country.script` (`artillery
.1.1-.1.6` = `wood / gold / iron −25%`, `aca.7` = `wood −85%`, `aca.32` = `gold
/ iron −50%`). Full coverage: 13–14 priceperc per nation × 21 nations = 291.
`_attach_resource_pcts` is left as a backstop for upgrades whose `if` conditions
returned `False` to AST-walk.

<a id="прежние-ошибки-в-самом-репо-исправлены--но-осторожно-с-форками"></a>
## Previous errors in the repo itself (fixed - but be careful with forks)

If you are reading old versions of files or external forks, check:

- **"Capture units work with a 5% chance per tick"** - was incorrect. Capture pure
  **geometric**, check every 1.9 game seconds (0.5 for
  artillery). See
  [`docs/recon/world/economy/capture_mechanics.md`](../../docs_en/recon/world/economy/capture_mechanics.md).
- **"Ukrainian/Scottish peasants are immune to capture"** - was incorrect. All
  8 peasant sids have `bcapture = True` (`unit.script:1199`); in standard
  Deathmatch / Historical Battle capture of peasants is disabled by the map via
  `capture_nopeasants`, but specific nations do not have flag-level immunity.
- **Building names “Town Hall / Barracks 17c”** - remained in English throughout
several writer's dictionaries until 2026-04-29. Canon - official
  localization: “Town Hall”, “Barracks 17th century”, “Cathedral”, “Artillery
  depot", "Diplomatic Center", "Shipyard", "Ferry", "Hetman", "kozak".
