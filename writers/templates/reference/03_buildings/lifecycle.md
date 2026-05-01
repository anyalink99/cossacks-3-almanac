## Жизненный цикл здания

Прежде чем переходить к таблицам, зафиксируем четыре механики, общие для **всех** зданий — стройка, ремонт, отмена, разрушение. Источник: [`recon/world/building_mechanics.md`](../recon/world/building_mechanics.md).

### Стройка

- **Прогресс:** на каждый «удар крестьянина» (анимация `construct`, 13 кадров) к `bbuilt_progress` прибавляется `delta = 0.359 / buildtime`. При `progress ≥ 1` здание получает `bbuilt = True`.
- **N строителей:** реальное время = `buildtime × 1.13 / N` (около 13% накладных расходов на координацию).
- **Лимит одновременной работы:** число строителей ограничено **builder slots** = `bbox_cols + bbox_rows` (Manhattan-периметр). Для большинства зданий 6–12, у складов используется специальный bbox для линейных «опор» (см. [`reports/economy/builder_slots.md`](../reports/economy/builder_slots.md)).
- **Уязвимость в стройке:** против любого урона действует `shield/3` вместо полного shield ([02_combat.md → Shield /3 при недостроенном здании](02_combat.md#shield-3-при-недостроенном-здании)). Недостроенное здание **захватывается** обычным capture-тиком независимо от типа — даже Башня.

### Ремонт

- **Бесплатно** — ремонт **не** тратит ресурсы (в `_misc_DoRepair` отсутствует `cost`).
- **+20 HP за один удар** крестьянина-ремонтника. Анимация ремонта — workfood (22 кадра, около 0.69 g-сек), значит один крестьянин восстанавливает **+29 HP / g-сек = +41 HP / real-сек @ fast**.
- **N ремонтников:** складываются аддитивно (штрафа 1.13× нет). 5 крестьян чинят со скоростью около 205 HP / real-сек.
- **Лимит одновременной работы:** тот же, что и при стройке.
- **Связь со стройкой:** ремонт в C3 формально — «стройка наоборот»: тот же тик, та же анимация, но прибавляет HP, а не прогресс bbuilt.

### Отмена постройки и заказа

- **Отмена недостроенного здания (Foundation).** GUI-обработчик `_misc_GUICancelBuilding` (`miscext2.script:3898-3953`) вызывает `GameObjectDestroyByHandle`, после чего здание идёт по обычной death-цепочке. Возвращаются 100% потраченных ресурсов (поведение в игре). Зеркального `_res_AddResToPlayerByIndex` к `_unit_ApplyCostByID` (`unit.script:5728-5762`) в скриптах не найдено — refund foundation cost, видимо, обрабатывается на стороне C++ (см. [`recon/world/building_mechanics.md §8`](../recon/world/building_mechanics.md#8-резюме-механик-быстрый-ответ-на-частые-вопросы)).
- **Отмена заказа юнита в очереди.** `_unit_CancelUnitProduction` (`unit.script:5891-5977`) возвращает `price[k] × costmodifier`, где `costmodifier = pow(costpercent/100, restype)` и `restype` — счётчик built-копий, сохранённый в `OrderInfo` в момент заказа (`unit.script:6017` поясняет: «restype stores amount of units, that we had at the moment of ordering produce»). На практике это 100% от того, что было реально списано в момент заказа, независимо от того, какая цена у этого юнита будет на текущий момент.
- **Отмена апгрейда.** `_unit_CancelUpgradePerform` (`unit.script:5837-5889`) возвращает базовую стоимость апгрейда из `_country_GetUpgradeCostBySID`. Костпроцентного масштабирования у апгрейдов в этой ветке нет, поэтому возврат равен списанному.
- **Захват.** При `_misc_ChangePlayer` все отменяемые производственные заказы прерываются и ресурсы возвращаются прежнему владельцу (см. [02_combat.md → Захват](02_combat.md#захват-зданий-и-юнитов), шаг 3).

### Разрушение

- При `hp ≤ 0` или `bDie := True` здание получает `essential_death`. State-машина (`units/building.inc/settagstates.inc:32-53`) ставит первый таймер `DelayExecuteState`:
  - если здание было `essential_birth` (отмена недостроенного) — сразу `DeathStage2` через `gc_building_deathtime_1 = 30` g-сек;
  - иначе — `DeathStage1` через `gc_building_deathtime_0 = 30` g-сек, далее `DeathStage1` (`deathstage1.inc:5-11`) меняет mesh на `<sid>_death1` и ставит `DeathStage2` ещё через 30 g-сек (`deathstage2.inc`). Для `usage = mine` обе паузы удваиваются (60 g-сек каждая).
- **Корпус** в этом промежутке остаётся на карте: визуально — mesh `<sid>_death1.mesh`, в состоянии `essential_death`, материал `'debris'` (`building.inc/ontagstates.inc:286`), коллизия — прежняя. Постройка нового здания на этих клетках невозможна, пока корпус не исчезнет.
- **Сброс клетки.** В `DeathStage2` (`deathstage2.inc:8-15`) для не-стен с `gc_collisiontag_terrain` вызывается `_unit_SetTerrainCollision(myHnd, gc_collisiontag_none)` + `_misc_UnitTopologyUpdate`, затем `GameObjectRequestToDestroyByHandle`. После этого клетка освобождается, и на ней можно ставить новое здание.
- **Гарнизон внутри** (если у здания `peasantabsorber > 0` или `transport > 0`). `_unit_DestroyObj` (`miscext2.script:4232-4242`) собирает `gc_argunit_inside` и вызывает `_unit_DoUnitsGoOutside(list, bDead=True, ...)`. Эта процедура (`unit.script:4559-4564`) ставит каждому юниту в списке `essential_death`, то есть содержимое умирает вместе со зданием.
- **Штраф к Score владельцу:** `−2× building.score` (или `−5×`, если здание ранее уже было захвачено — см. [02_combat.md → Score](02_combat.md#score-и-финальный-счёт)).
- **OnDeath-хук** (`building.inc/ondeath.inc:11-25`) до удаления прокручивает очередь заказов здания: `produce`-заказы прогоняются через `_unit_ProduceUnit(... bState=False, ...)` (`unit.script:10351`), что внутри ведёт к `_unit_CancelUnitProduction` и возврату ресурсов; `performupgrade`-заказы — через `_unit_CancelUpgradePerform`. То есть при сносе работающей казармы или академии ресурсы за уже оплаченные юниты/апгрейды возвращаются игроку, а не сгорают.

