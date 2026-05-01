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

Семь документов про то, что происходит в активной партии: добыча,
постройка, захват, передвижение, выбор цели, генерация карты, опции
лобби.

| Файл | Что внутри |
|---|---|
| [world/peasant_extraction.md](world/peasant_extraction.md) | Добыча ресурсов: цикл крестьянина, формулы, шахты (включая апгрейды до 95 absorber), поля (HP / regen / restart), efficiency-апгрейды, карта как вход (densities, гарантированные стартовые ресурсы), пеньки = бесконечный wood pool. |
| [world/building_mechanics.md](world/building_mechanics.md) | Здания: footprint mask (1 cell = 0.5 тайла), ремонт (бесплатно, +20 HP за удар), постройка (delta = 0.359 / buildtime за удар), builder slots, стены (2×2 на сегмент, 4–12 slots), гарнизон / башни, captureradius = 4 тайла. |
| [world/capture_mechanics.md](world/capture_mechanics.md) | Захват: чистая геометрия, не конвертер. Радиусы (`captureradius = 4.013t` Eucl², `protectionradius ≈ 8t`). Кто захватывается (крестьянин + 5 типов артиллерии + почти все экономические здания). Кто НЕТ (башни, стены, академия, конюшня, верфь). Башни — только во время постройки. Священник = healer, не конвертер. |
| [world/pathfinding.md](world/pathfinding.md) | Pathfinding: алгоритм в нативном движке (A\*-like через `TopologyGetPath`). Двухуровневый: high-level batched раз в 20 мс + per-frame `CollisionInertia` (mass + radius). Collision grid = 0.5 t. Дружественный push беззвучен; враг в 90° спереди → авто-атака. Formation = jittered per-unit, не squad-leader. |
| [world/target_selection.md](world/target_selection.md) | Алгоритм выбора цели через scan-grid: `_unit_SearchEnemyInCell` (случайный стартовый индекс по списку в ячейке) + `_unit_SearchEnemyScanCells` (минимум по relativeDist с балансировкой нагрузки `×(1 + STO_count × 0.125)` для рукопашников). 5 режимов `scanmode` (default / priest / capture / capture-fallback / AI sabotage). Семантика attack-move: `move_mode_attack` для пехоты и кавалерии, `attackpoint` для артиллерии с `bartprepare`. Умный поиск ловит врагов только в 30°-конусе впереди. |
| [world/map_generation_pipeline.md](world/map_generation_pipeline.md) | Полный таймлайн `DoGenerate`: forbidden zones cCircle1/2/3, `SetupStartingResources` (1× stoneforest + 2× stones + 3× forests в радиусе 5–22), Phase-1 / Phase-2 mines, `FillOwnerMap`, peacetime-границы. Плюс seed space: что определяет уникальную карту (`(inputbitmap, randkey0, randkey1)`, ~230 базовых масок для 4pl Land). |
| [world/game_settings.md](world/game_settings.md) | Поведение движка по каждой опции лобби: `gen` (`mapsize`, `terraintype`, `relieftype`, `resourcestart`, `resourcemines`, `season`, `randkey0/1`) и `additional` (`startingunits`, `balloon`, `cannons`, `peacetime`, `century18`, `capture`, `marketdip`, `teams`, `limit`, `gamespeed`, `adviserassistant`). Глубокий разбор peacetime-механики (`gbool_peacemode`, ничейные ячейки, блок в `_unit_SearchEnemy`). Сами таблицы значений и каноничные русские названия — в [`../reports/map/lobby_settings.md`](../reports/map/lobby_settings.md), машинный JSON — в [`../derived/game_settings.json`](../derived/game_settings.json). |

## Игровые системы (правила, AI, наёмники) — [`systems/`](systems/)

Три документа про оверарх-механики: ИИ-противник, наёмничество, как
заканчивается партия.

| Файл | Что внутри |
|---|---|
| [systems/ai_behavior.md](systems/ai_behavior.md) | AI: тик каждые 2.4 g-сек. Difficulty cheat = скорость постройки и найма (easy 30%, normal 50%, hard 75%, veryhard 100%, impossible 125%). **Стартовых ресурсов не получает**. Build order rule-based, нация-зависимый. Aggressor wave = 5 отрядов. Diplomacy: команды статически из лобби, без альянсов в процессе партии. |
| [systems/mercenaries_diplomacy.md](systems/mercenaries_diplomacy.md) | Дипломатический центр (`<nat>dip`): 21 нация × 1 здание, 4500–6500 HP, пререквизит — академия. Каталог из 8 наёмников (одинаковый у всех наций). Стоимость — только золото; `consume.gold` upkeep; `bnohungry = True`. Лимит масштабирования = 2× (против 20 000× у обычных юнитов). Pair-counter `archerdip ↔ archerturdip`. Rebellion = 18.31% за тик на hard+. С 2026-04-30 `data.json` учитывает блок `if (bmercenary)` — все 168 dip-строк правильные. |
| [systems/victory_conditions.md](systems/victory_conditions.md) | Условия победы и поражения: last-team-standing (`farmused = 0` ⇒ defeat). Wonder отсутствует. Score копится только для статистики (kill +2×, capture +5×, build +1×). Surrender (`bleave = True`), first-leaver penalty −w ELO. Time-limit отсутствует. Игровые режимы: skirmish, Historical Battle, Campaign, Scenario, Rated MP. |

## Engine internals (тики, RNG, сетевая модель) — [`engine/`](engine/)

Тройка документов про устройство движка. Идут в комплекте — каждый
ссылается на остальные. Без них нельзя объяснить, почему симуляция
не воспроизводится даже на одном хосте.

| Файл | Что внутри |
|---|---|
| [engine/ticks_and_subticks.md](engine/ticks_and_subticks.md) | Модель времени: real / game / frames. Главный progress-loop. Sub-tick state-machine intervals (135 мс у крестьян, 100 мс у юнитов). Variable timestep + adaptive game speed. Что нормализуется на Save / Load. |
| [engine/determinism_audit.md](engine/determinism_audit.md) | RNG audit: `random` vs `RandomExt` vs `SetRandomKey`. 7 RNG-сайтов в hot-path добычи. RNG в бою (5% триггер хедшота). Почему шахты воспроизводимы. Импликации для симулятора и план мод-фикса. |
| [engine/server_sync_architecture.md](engine/server_sync_architecture.md) | Сетевая модель: C3 — server-authoritative, **не** lockstep. Net modes, паттерн `bProcess`, sync-пакеты (per-event + periodic в **real-time**, mod-53 unit params, on-demand full sync). |

## Когда что читать

- **«Почему этот юнит добывает столько-то wood?»** → [world/peasant_extraction.md](world/peasant_extraction.md).
- **«Сколько крестьян могут одновременно строить здание X?»** → [world/building_mechanics.md](world/building_mechanics.md) §3.
- **«Сколько шахт у меня будет на старте?»** → [world/peasant_extraction.md §8.3](world/peasant_extraction.md) или [world/map_generation_pipeline.md §8](world/map_generation_pipeline.md).
- **«Почему один и тот же сейв даёт разную добычу при перезагрузке?»** → [engine/determinism_audit.md](engine/determinism_audit.md) §7.
- **«Почему `random` использован в одном месте и `RandomExt` в другом?»** → [engine/server_sync_architecture.md](engine/server_sync_architecture.md) §1.3 + [engine/determinism_audit.md](engine/determinism_audit.md) §1.
- **«Карта одна и та же — что это значит формально?»** → [world/map_generation_pipeline.md §12](world/map_generation_pipeline.md) (seed space).
- **«Когда AI меня атакует?»** → [systems/ai_behavior.md](systems/ai_behavior.md) §«Aggression / attack triggers».
- **«Можно ли захватить башню?»** → [world/capture_mechanics.md](world/capture_mechanics.md) §6.
- **«Как выиграть партию?»** → [systems/victory_conditions.md](systems/victory_conditions.md) §3.
- **«Как работают наёмники / Rebellion?»** → [systems/mercenaries_diplomacy.md](systems/mercenaries_diplomacy.md) §§3-4.
- **«Как ходят юниты в формации?»** → [world/pathfinding.md](world/pathfinding.md) §6.
- **«В кого выстрелит мой мушкетёр, если в радиусе три врага?»** → [world/target_selection.md](world/target_selection.md) §3.
- **«Чем `attack-move` отличается от обычного движения?»** → [world/target_selection.md](world/target_selection.md) §5.
- **«Какие опции есть в лобби и что они дают?»** → таблицы в [`../reports/map/lobby_settings.md`](../reports/map/lobby_settings.md), поведение движка — в [world/game_settings.md](world/game_settings.md). Машинный JSON для редакторов — [`../derived/game_settings.json`](../derived/game_settings.json).

## Что НЕ в этой папке

- Готовые таблицы цен / HP / урона — в [`../reference/`](../reference/).
- Производные расчёты (DPS, EHP, scaling, tech tree, vision и т. п.) — в [`../reports/`](../reports/README.md).
- Выходы симулятора экономики — в [`../simulations/`](../simulations/README.md).
- Open empirical questions для in-game замеров — встроены в §9 каждого профильного документа.
