# Recon notes

Глубокие исследования механик Cossacks 3 — то, что нельзя извлечь автоматическим парсером и что нужно переварить, чтобы понять цифры в [`docs/reference/`](../docs/reference/). Каждый файл — самостоятельный документ; перекрёстные ссылки размечены явно.

## Документы

### Логика мира

| Файл | Что внутри |
|---|---|
| [peasant_extraction.md](peasant_extraction.md) | Добыча ресурсов: цикл крестьянина, формулы, шахты (включая апгрейды до 95 absorber), поля (HP / regen / restart), efficiency-апгрейды, карта как вход (densities, гарантированные стартовые ресурсы), пеньки = бесконечный wood pool. |
| [building_mechanics.md](building_mechanics.md) | Здания: footprint mask (1 cell = 0.5 тайла), repair (бесплатно, +20 HP/удар), construction (delta = 0.359/buildtime per hit), builder slots, стены (2×2 на сегмент, 4-12 slots), гарнизон/башни, capture radius = 4 тайла. |
| [map_generation_pipeline.md](map_generation_pipeline.md) | Полный таймлайн `DoGenerate`: cCircle1/2/3 forbidden zones, `SetupStartingResources` (1× stoneforest + 2× stones + 3× forests в радиусе 5-22), Phase-1 / Phase-2 mines, FillOwnerMap, peacetime borders. Плюс seed space — что определяет уникальную карту (`(inputbitmap, randkey0, randkey1)`, ~230 базовых масок для 4pl Land). |
| [capture_mechanics.md](capture_mechanics.md) | Захват: чистая геометрия, не конвертер. Радиусы (`captureradius=4.013t Eucl²`, `protectionradius≈8t`). Кто захватывается (peasant + 5 типов артиллерии + почти все экономические здания). Кто НЕТ (башни, стены, академия, конюшня, верфь). Башни — только во время стройки. Священник = healer, не конвертер. |
| [victory_conditions.md](victory_conditions.md) | Условия победы/поражения: last-team-standing (`farmused=0` ⇒ defeat). Wonder отсутствует. Score копится только для статистики (kill +2×, capture +5×, build +1×). Surrender (`bleave=True`), first-leaver penalty −w ELO. Time-limit отсутствует. Game modes: skirmish / Historical Battle / Campaign / Scenario / Rated MP. |
| [ai_behavior.md](ai_behavior.md) | AI: тикает каждые 2.4 g-сек. Difficulty cheat = build/produce speed (easy 30%, normal 50%, hard 75%, veryhard 100%, impossible 125%). **Стартовых ресурсов не получает**. Build order rule-based, нация-зависимый. Aggressor wave = 5 squads. Diplomacy: команды статически из лобби, no alliance formation. |
| [pathfinding.md](pathfinding.md) | Pathfinding: алгоритм в нативном движке (A*-like через `TopologyGetPath`). Двухуровневый: high-level batched раз в 20мс + per-frame CollisionInertia (mass+radius). Collision grid = 0.5 t. Friendly push беззвучен; враг в 90° спереди → авто-атака. Formation = jittered per-unit, не squad-leader. |
| [mercenaries_diplomacy.md](mercenaries_diplomacy.md) | Diplomatic center (`<nat>dip`): 21 нация × 1 здание, 4500-6500 HP, prereq=academy. Каталог 8 наёмников (одинаковый у всех наций). Cost only gold + `consume.gold` upkeep, `bnohungry=True`. Cap масштабирования = 2× (vs 20000× у обычных юнитов). Pair-counter `archerdip ↔ archerturdip`. Rebellion 18.31% per tick на hard+. С 2026-04-30 data.json учитывает `if (bmercenary)` — все 168 dip-строк правильные. |
| [game_settings.md](game_settings.md) | Все опции лобби: `gen` (mapsize/terraintype/relieftype/resourcestart/resourcemines/season/randkey0/1) и `additional` (startingunits/balloon/cannons/peacetime/century18/capture/marketdip/teams/limit/gamespeed/adviserassistant). Полные таблицы значений + механика peacetime (`gbool_peacemode`, граница территории, `_unit_SearchEnemy` блок). Источник для машинного `docs/derived/game_settings.json` (генерируется `compute/compute_game_settings.py`). |

### Engine internals

Эта тройка идёт в комплекте — каждый документ ссылается на остальные. Без них невозможно объяснить, почему симуляция не воспроизводима даже на одном хосте.

| Файл | Что внутри |
|---|---|
| [ticks_and_subticks.md](ticks_and_subticks.md) | Модель времени: real / game / frames; главный progress-loop; sub-tick state-machine intervals (peasants 135 ms, units 100 ms); variable timestep + adaptive game speed; что нормализуется на Save/Load. |
| [determinism_audit.md](determinism_audit.md) | RNG audit: `random` vs `RandomExt` vs `SetRandomKey`, 7 RNG-сайтов в hot-path добычи, RNG в бою (5% headshot trigger), почему шахты воспроизводимы, импликации для модели и план мод-фикса. |
| [server_sync_architecture.md](server_sync_architecture.md) | Сетевая модель: C3 — server-authoritative, не lockstep. Net modes, паттерн `bProcess`, sync пакеты (per-event + periodic в **real-time**, mod-53 unit params, on-demand full sync). |

## Когда что читать

- **«Почему этот юнит добывает столько-то wood?»** → [peasant_extraction.md](peasant_extraction.md).
- **«Сколько крестьян могут одновременно строить здание X?»** → [building_mechanics.md](building_mechanics.md) §3.
- **«Сколько шахт у меня будет на старте?»** → [peasant_extraction.md §8.3](peasant_extraction.md) или [map_generation_pipeline.md §8](map_generation_pipeline.md).
- **«Почему один и тот же сейв даёт разную добычу при перезагрузке?»** → [determinism_audit.md](determinism_audit.md) §7.
- **«Почему `random` использован в одном месте и `RandomExt` в другом?»** → [server_sync_architecture.md](server_sync_architecture.md) §1.3 + [determinism_audit.md](determinism_audit.md) §1.
- **«Карта одна и та же — что это значит формально?»** → [map_generation_pipeline.md §12](map_generation_pipeline.md) (seed space).
- **«Когда AI меня атакует?»** → [ai_behavior.md](ai_behavior.md) §«Aggression / attack triggers».
- **«Можно ли захватить башню?»** → [capture_mechanics.md](capture_mechanics.md) §6.
- **«Как выиграть партию?»** → [victory_conditions.md](victory_conditions.md) §3.
- **«Как работают наёмники / Rebellion?»** → [mercenaries_diplomacy.md](mercenaries_diplomacy.md) §§3-4.
- **«Как ходят юниты в формации?»** → [pathfinding.md](pathfinding.md) §6.
- **«Какие опции есть в лобби и что они дают?»** → [game_settings.md](game_settings.md). Машинный JSON для editor — `../derived/game_settings.json`.

## Что НЕ в этой папке

- Готовые таблицы цен / HP / урона — в [`../reference/`](../reference/).
- Производные расчёты (DPS, EHP, scaling, tech tree, vision и т. п.) — в [`../reports/`](../reports/README.md).
- Выходы симулятора экономики — в [`../simulations/`](../simulations/README.md).
- Open empirical questions для in-game замеров — встроены в §9 каждого профильного документа.
