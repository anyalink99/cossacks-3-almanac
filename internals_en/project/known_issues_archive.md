<a id="known-issues--архив-исправленных-проблем"></a>
<a id="архив-исправленных-ограничений"></a>
# Known Issues: Resolved

**English** · [Русский](../../internals/project/known_issues_archive.md)

Entries move here from [`known_issues.md`](known_issues.md) after the parser or
dataset is corrected. The archive records what changed in `data.json` and why.

Format: correction date → brief description → previous and corrected behavior
→ commit or pull request, when available.

## 2026-04-30

<a id="bmercenary-override-не-разрешался--168-dip-юнитов-в-datajson-имели-не-наёмничьи-статы"></a>
<a id="переопределение-bmercenary-не-применялось-к-168-вариантам-наёмников-дипломатического-центра"></a>
### The `bmercenary` override was ignored for 168 Diplomatic Center units

**Before:** `parser/parse_units.py` ignored the `if (bmercenary)` branch in
`unit.script` for units whose SID ends in `dip`: 8 SIDs across 21 nations, or
168 records. Their entries in `data.json` therefore contained the ordinary
unit statistics rather than the mercenary variants.

**Fix:** [`parse_units.py`](../../parser/parse_units.py) now defines
`BMERCENARY_SIDS` and uses `find_bmercenary_block_body()`.
`_compute_effective_unit()` in
[`build_data.py`](../../parser/build_data.py) applies the override to those
SIDs. The same change added parsing for `objprop.costpercent := X;` in unit
branches; three non-mercenary units also use that field at lines 1867, 1889,
and 2018 of `unit.script`.

**Verified:** all 168 records now contain the correct mercenary statistics.
Health, gold cost and upkeep, `bmercenary = True`, `bnohungry = True`, and
`costpercent` values of 100, 100.5, or 102 agree with
[Mercenaries and the Diplomatic Center](../../docs_en/recon/systems/mercenaries_diplomacy.md)
§2.2. The statistics are identical across nations, as the scripts specify.
All 112 data sanity checks pass.

<a id="ценовые-проценты-priceperc-апгрейдов-не-извлекались"></a>
<a id="процентные-изменения-цены-улучшений-priceperc-не-извлекались"></a>
### Percentage-cost upgrades lacked `resource_pcts`

**Before:** the 291 `priceperc` upgrades in `data.json` had the correct base
research prices in food, wood, stone, gold, iron, and coal, but lacked
`resource_pcts`: the percentage reductions applied to the cost of affected
units and buildings. `country.script` writes these percentages through
`country.upgrade[ind-1].sarrparam2[gc_upgrade_maxarrparam2count - gc_ResCount + gc_resource_type_X - 1] := 'NN';`
after calling `_country_AddUpgrade*`. The old `_attach_resource_pcts`
implementation tried to recover the SID from the surrounding text and could
not handle nation-specific templates such as
`csid + 'art.' + member + ...`.

**Fix:** the `assign` branch in `walk_sim` now handles these statements
([`simulate_upgrades.py:870-887`](../../parser/simulate_upgrades.py)).
`_SARR2_RES_LHS_RE` recognizes the left-hand side, parses the right-hand side
as a percentage, and assigns it to
`state["last_upgrade"]["resource_pcts"][resource]`. The AST already represented
the assignments correctly; the simulation walker had simply ignored them.

**Verified:** all 291 `priceperc` upgrades now have `resource_pcts`, up from
none. The values match a direct reading of `country.script`: `artillery
.1.1-.1.6` reduces wood, gold, and iron costs by 25%; `aca.7` reduces wood by
85%; and `aca.32` reduces gold and iron by 50%. This covers 13 or 14 upgrades
per nation across all 21 nations. `_attach_resource_pcts` remains as a
fallback for upgrades skipped when an `if` condition evaluates to `False`
during the AST walk.

<a id="прежние-ошибки-в-самом-репо-исправлены--но-осторожно-с-форками"></a>
<a id="исправления-в-старых-версиях-и-внешних-ответвлениях"></a>
## Historical corrections

Old revisions and external forks may still contain these claims:

- Unit capture was once described as having a 5% chance per tick. Capture is
  geometric and deterministic; the game checks ordinary units every 1.9 game
  seconds and artillery every 0.5 game seconds. See
  [Capturing objects](../../docs_en/recon/world/economy/capture_mechanics.md).
- Ukrainian and Scottish Peasants were once described as immune to capture.
  All eight Peasant SIDs have `bcapture = True` (`unit.script:1199`). Standard
  Deathmatch and Historical Battle settings disable Peasant capture through
  `capture_nopeasants`; no nation-specific immunity flag exists.
- Until 2026-04-29, several dictionaries used by the Russian documentation
  retained English placeholder names such as “Town Hall” and “Barracks 17c”.
  They now use the official Russian localization: «Городской центр», «Казарма
  17 в.», «Собор», «Артиллерийское депо», «Дипломатический центр», «Порт»,
  «Транспорт», «Гетьман» and «козак».
