# Known issues — архив исправленных проблем

Сюда переезжают записи из [`known_issues.md`](known_issues.md) после того, как
проблема исправлена в парсере или в данных. Сохраняется для истории — иногда
полезно знать, что именно правили в data.json и почему.

Формат: дата исправления → краткое описание → что было / что стало → ссылка на
коммит или PR (если есть).

## 2026-04-30

### `bmercenary` override не разрешался — 168 dip-юнитов в `../data.json` имели не-наёмничьи статы

**Было:** `parser/parse_units.py` не учитывал `if (bmercenary)` ветку в
`unit.script` для юнитов с суффиксом `dip` (8 sid × 21 нация = 168 строк).

**Фикс:** добавлены `BMERCENARY_SIDS` и `find_bmercenary_block_body()` в
[`parse_units.py`](../parser/parse_units.py); `_compute_effective_unit()` в
[`build_data.py`](../parser/build_data.py) применяет merc-override для sid'ов
из `BMERCENARY_SIDS`. Параллельно добавлен парсинг `objprop.costpercent := X;`
для unit-веток (3 не-merc юнита тоже его имели: 1867, 1889, 2018 в
unit.script).

**Подтверждено:** 8 dip-sid × 21 нация = 168 строк теперь имеют правильные
merc-статы — HP, gold, `consume.gold`, `bmercenary = True`, `bnohungry = True`,
`costpercent` (100 / 100.5 / 102) совпадают с
[`recon/systems/mercenaries_diplomacy.md`](recon/systems/mercenaries_diplomacy.md) §2.2. Стат
идентичен между нациями (nation-independent). 112 / 112 sanity checks PASS.

### Ценовые проценты `priceperc` апгрейдов не извлекались

**Было:** 291 priceperc-апгрейд в `../data.json` имел корректную базовую цену
исследования (food / wood / stone / gold / iron / coal), но **не имел**
`resource_pcts` — процентного снижения стоимости целевых юнитов и зданий. Эти
проценты выставляются в `country.script` через
`country.upgrade[ind-1].sarrparam2[gc_upgrade_maxarrparam2count - gc_ResCount + gc_resource_type_X - 1] := 'NN';`
после `_country_AddUpgrade*` вызова. Существующий `_attach_resource_pcts`
пытался re-resolve sid из текстовой позиции и не справлялся с per-nation
шаблонами (`csid + 'art.' + member + ...`).

**Фикс:** добавлен handler в `walk_sim`'s `assign` branch
([`simulate_upgrades.py:870-887`](../parser/simulate_upgrades.py)) —
`_SARR2_RES_LHS_RE` распознаёт LHS, парсит RHS как процент и присваивает
`state["last_upgrade"]["resource_pcts"][resource]`. AST уже трактовал эти
assigns правильно — handler их игнорировал.

**Подтверждено:** 291 / 291 priceperc-апгрейдов имеют `resource_pcts` (раньше
0 / 291). Числа совпадают с прямым чтением `country.script` (`artillery
.1.1-.1.6` = `wood / gold / iron −25%`, `aca.7` = `wood −85%`, `aca.32` = `gold
/ iron −50%`). Полное покрытие: 13–14 priceperc на нацию × 21 нация = 291.
`_attach_resource_pcts` оставлен как backstop для апгрейдов, чьи `if`-условия
вернули `False` в AST-walk.

## Прежние ошибки в самом репо (исправлены — но осторожно с форками)

Если читаешь старые версии файлов или внешние форки, проверь:

- **«Захват юнитов работает с 5%-шансом за тик»** — было неверно. Захват чисто
  **геометрический**, проверка раз в 1.9 игровых секунды (0.5 для
  артиллерии). См.
  [`docs/recon/world/economy/capture_mechanics.md`](recon/world/economy/capture_mechanics.md).
- **«Украинские/шотландские крестьяне иммунны к захвату»** — было неверно. Все
  8 sid'ов крестьян имеют `bcapture = True` (`unit.script:1199`); в стандартном
  Deathmatch / Historical Battle захват крестьян отключён картой через
  `capture_nopeasants`, но flag-уровневой иммунности у конкретных наций нет.
- **Названия зданий «Town Hall / Barracks 17c»** — оставались на английском в
  нескольких словарях writer'а до 2026-04-29. Канон — официальная
  локализация: «Городской центр», «Казарма 17 в.», «Собор», «Артиллерийское
  депо», «Дипломатический центр», «Порт», «Транспорт», «Гетьман», «козак».
