# Recon notes — глубокие исследования механик

Это **handwritten** разбор того, чего нет в `data.json` и что не вытащит
автопарсер: поведение движка, скрытые формулы, edge cases, RNG-сайты,
сетевая модель. Все цифры в [`../reference/`](../reference/) опираются
на эти документы — здесь живёт «почему», а там «сколько».

Документы разложены по трём подпапкам в зависимости от того, **что
именно** разбирается. Каждый файл автономен; перекрёстные ссылки —
явно через markdown-линки. Пайплайн данных, в который встроены эти
документы, — в [`../architecture.md`](../architecture.md).

## Мир и карта (что видит игрок) — [`world/`](world/)

Подробные разборы того, что происходит в активной партии: добыча,
бой, движение, формации, захват, генерация карты, опции лобби.

### Экономика

| Файл | Что внутри |
|---|---|
| [world/economy/peasant_extraction.md](world/economy/peasant_extraction.md) | Добыча ресурсов: цикл крестьянина, формулы, шахты (до 95 absorber), поля, efficiency-апгрейды, гарантированные стартовые ресурсы, пеньки = бесконечный wood pool. |
| [world/economy/building_mechanics.md](world/economy/building_mechanics.md) | Здания: footprint mask, ремонт, постройка, builder slots, стены, гарнизон, captureradius. |
| [world/economy/capture_mechanics.md](world/economy/capture_mechanics.md) | Захват зданий и юнитов — чистая геометрия. Кто захватывается, кто нет. |
| [world/economy/upgrades_application.md](world/economy/upgrades_application.md) | Как применяется апгрейд: к существующим юнитам и будущим, аддитивная композиция `eff`, `priceperc` / `buildtimeperc`, прерывание исследования. |
| [world/economy/hunger_and_rebellion.md](world/economy/hunger_and_rebellion.md) | Голод (`bfamine`) и бунт (`brebellion`): когда поднимаются флаги, кто и в каком порядке умирает, защита. |
| [world/economy/production_queue.md](world/economy/production_queue.md) | Очередь производства: 12 слотов, infinite-режим, слитие ордеров через `costpercent`, refund при отмене и захвате, прерывание захватчиками. |
| (Рынок) | Подробный разбор механики и формулы обмена — пока только в [`../reference/06_market.md`](../reference/06_market.md). |

### Бой и команды

| Файл | Что внутри |
|---|---|
| [world/combat/combat_damage_pipeline.md](world/combat/combat_damage_pipeline.md) | Конвейер урона: 6 шагов формулы, хедшот, AoE, дружественный огонь, peace-mode, сценарная неуязвимость. |
| [world/combat/formations.md](world/combat/formations.md) | LINE / SQUARE / KARE: 149 формаций, бонусы строя, hold-mode, mask и symmetry. |
| [world/combat/target_selection.md](world/combat/target_selection.md) | Алгоритм выбора цели через scan-grid: 5 режимов, attack-move, конус 30°. |
| [world/combat/unit_commands.md](world/combat/unit_commands.md) | Очередь приказов, режимы (move, attack, attack-move, garrison, patrol, guard), hold-mode, hold-fire, rally point, STO/STP. |
| [world/combat/pathfinding.md](world/combat/pathfinding.md) | Pathfinding: A\*-like через `TopologyGetPath`, двухуровневый, collision grid, формации. |
| [world/combat/towers.md](world/combat/towers.md) | Башни: целеуказание, стоимость выстрела, апгрейды, захват только во время постройки. **Гарнизона в башне в C3 нет** — `peasantabsorber` ставится только у шахт. |
| [world/combat/walls_and_gates.md](world/combat/walls_and_gates.md) | Стены и ворота: сегменты, постройка крестьянами, builder slots по `wallvariation`, ворота как апгрейд `buildgate`, снос сегмента при попытке захвата. |
| [world/combat/artillery_specifics.md](world/combat/artillery_specifics.md) | Артиллерия: типы (`artind`), `bartprepare`, `attackpoint`, лимиты через арт-депо, AoE. |
| [world/combat/naval_combat.md](world/combat/naval_combat.md) | Морские юниты: порт, транспорт, линейный корабль, рыболов, морские формации, бой с берега. |
| [world/combat/vision_and_fow.md](world/combat/vision_and_fow.md) | Радиус обзора (`20 + 4 × vision`), туман войны, союзный обзор, `fogreveal`-снаряды. |
| [world/combat/ranged_units_behavior.md](world/combat/ranged_units_behavior.md) | Поведение стрелков: standground, bartprepare, RunAway, штраф к дальности, мульти-оружие, high ground. |

### Карта и генерация

| Файл | Что внутри |
|---|---|
| [world/map/map_generation_pipeline.md](world/map/map_generation_pipeline.md) | Таймлайн `DoGenerate`: forbidden zones, `SetupStartingResources`, mines phase-1/2, `FillOwnerMap`, peacetime границы, seed space. |
| [world/map/game_settings.md](world/map/game_settings.md) | Опции лобби: `gen.*` и `additional.*`, peace-time, century18, balloon. |

## Игровые системы (правила, AI, наёмники, сценарии) — [`systems/`](systems/)

| Файл | Что внутри |
|---|---|
| [systems/ai_behavior.md](systems/ai_behavior.md) | AI: тик 2.4 g-сек, difficulty (от 30 % до 125 %), build order rule-based, агрессивные волны по 5 отрядов. |
| [systems/mercenaries_diplomacy.md](systems/mercenaries_diplomacy.md) | Дипцентр и наёмники: 21 нация, 8 типов наёмников, gold-upkeep, Rebellion 18.31 % на hard+. |
| [systems/victory_conditions.md](systems/victory_conditions.md) | Победа и поражение: last-team-standing, defeat по `farmused = 0`, score-табло для статистики. |
| [systems/scenarios_and_triggers.md](systems/scenarios_and_triggers.md) | Сценарии (`TScenarioTrigger` / `Condition` / `Action` / FSM) — кампания, Historical Battles, peace-mode для героя. |
| [systems/ui_input_and_feedback.md](systems/ui_input_and_feedback.md) | Интерфейс и ввод: селекция, mouse / keyboard / scroll, курсор, камера, listener для звука. **Звуки и FOW — независимые системы** (юнит во вражеском FOW слышен). Alarm-уведомления (`_misc_DoAlarm`) срабатывают только вне frustum камеры. |

## Engine internals — переехало

Документы про устройство движка (модель времени, RNG, сетевая
модель, нативный API DWS) — теперь в отдельной top-level папке
[`../../internals/engine/`](../../internals/engine/). Они слишком
технические для обычного читателя справочника. Если нужны:

- [`internals/engine/ticks_and_subticks.md`](../../internals/engine/ticks_and_subticks.md) — модель времени.
- [`internals/engine/determinism_audit.md`](../../internals/engine/determinism_audit.md) — RNG-аудит.
- [`internals/engine/server_sync_architecture.md`](../../internals/engine/server_sync_architecture.md) — server-authoritative.
- [`internals/engine/native_api.md`](../../internals/engine/native_api.md) — 4 856 native DWS-функций.

## Когда что читать

- **«Почему этот юнит добывает столько-то wood?»** → [world/economy/peasant_extraction.md](world/economy/peasant_extraction.md).
- **«Сколько крестьян могут одновременно строить здание X?»** → [world/economy/building_mechanics.md](world/economy/building_mechanics.md) §3.
- **«Сколько шахт у меня будет на старте?»** → [world/economy/peasant_extraction.md §8.3](world/economy/peasant_extraction.md) или [world/map/map_generation_pipeline.md §8](world/map/map_generation_pipeline.md).
- **«Почему один и тот же сейв даёт разную добычу при перезагрузке?»** → [internals/engine/determinism_audit.md](../../internals/engine/determinism_audit.md) §7.
- **«Почему `random` использован в одном месте и `RandomExt` в другом?»** → [internals/engine/server_sync_architecture.md](../../internals/engine/server_sync_architecture.md) §1.3 + [internals/engine/determinism_audit.md](../../internals/engine/determinism_audit.md) §1.
- **«Карта одна и та же — что это значит формально?»** → [world/map/map_generation_pipeline.md §12](world/map/map_generation_pipeline.md) (seed space).
- **«Когда AI меня атакует?»** → [systems/ai_behavior.md](systems/ai_behavior.md) §«Aggression / attack triggers».
- **«Можно ли захватить башню?»** → [world/economy/capture_mechanics.md](world/economy/capture_mechanics.md) §6.
- **«Как выиграть партию?»** → [systems/victory_conditions.md](systems/victory_conditions.md) §3.
- **«Как работают наёмники / Rebellion?»** → [systems/mercenaries_diplomacy.md](systems/mercenaries_diplomacy.md) §§3-4.
- **«Как ходят юниты в формации?»** → [world/combat/pathfinding.md](world/combat/pathfinding.md) §6.
- **«В кого выстрелит мой мушкетёр, если в радиусе три врага?»** → [world/combat/target_selection.md](world/combat/target_selection.md) §3.
- **«Чем `attack-move` отличается от обычного движения?»** → [world/combat/target_selection.md](world/combat/target_selection.md) §5.
- **«Какие опции есть в лобби и что они дают?»** → таблицы в [`../reports/map/lobby_settings.md`](../reports/map/lobby_settings.md), поведение движка — в [world/map/game_settings.md](world/map/game_settings.md). Машинный JSON для редакторов — [`../../derived/game_settings.json`](../../derived/game_settings.json).

## Что НЕ в этой папке

- Готовые таблицы цен / HP / урона — в [`../reference/`](../reference/).
- Производные расчёты (DPS, EHP, scaling, tech tree, vision и т. п.) — в [`../reports/`](../reports/README.md).
- Open empirical questions для in-game замеров — встроены в §9 каждого профильного документа.
