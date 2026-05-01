# Recon notes — глубокие исследования механик

Это **handwritten** разбор того, чего нет в `data.json` и что не вытащит
автопарсер: поведение движка, скрытые формулы, edge cases, RNG-сайты,
сетевая модель. Все цифры в [`../reference/`](../reference/) опираются на
эти документы — здесь живёт «почему», а там «сколько».

Каждый файл автономен; перекрёстные ссылки — явно через markdown-линки.
Пайплайн данных, в который встроены эти документы, — в
[`../architecture.md`](../architecture.md).

## Мир и карта (что видит игрок)

Шесть документов про то, что происходит в активной партии: добыча, постройка,
захват, передвижение, генерация карты и опции лобби.

| Файл | Что внутри |
|---|---|
| [peasant_extraction.md](peasant_extraction.md) | Добыча ресурсов: цикл крестьянина, формулы, шахты (включая апгрейды до 95 absorber), поля (HP / regen / restart), efficiency-апгрейды, карта как вход (densities, гарантированные стартовые ресурсы), пеньки = бесконечный wood pool. |
| [building_mechanics.md](building_mechanics.md) | Здания: footprint mask (1 cell = 0.5 тайла), ремонт (бесплатно, +20 HP за удар), постройка (delta = 0.359 / buildtime за удар), builder slots, стены (2×2 на сегмент, 4–12 slots), гарнизон / башни, captureradius = 4 тайла. |
| [capture_mechanics.md](capture_mechanics.md) | Захват: чистая геометрия, не конвертер. Радиусы (`captureradius = 4.013t` Eucl², `protectionradius ≈ 8t`). Кто захватывается (крестьянин + 5 типов артиллерии + почти все экономические здания). Кто НЕТ (башни, стены, академия, конюшня, верфь). Башни — только во время постройки. Священник = healer, не конвертер. |
| [pathfinding.md](pathfinding.md) | Pathfinding: алгоритм в нативном движке (A\*-like через `TopologyGetPath`). Двухуровневый: high-level batched раз в 20 мс + per-frame `CollisionInertia` (mass + radius). Collision grid = 0.5 t. Дружественный push беззвучен; враг в 90° спереди → авто-атака. Formation = jittered per-unit, не squad-leader. |
| [map_generation_pipeline.md](map_generation_pipeline.md) | Полный таймлайн `DoGenerate`: forbidden zones cCircle1/2/3, `SetupStartingResources` (1× stoneforest + 2× stones + 3× forests в радиусе 5–22), Phase-1 / Phase-2 mines, `FillOwnerMap`, peacetime-границы. Плюс seed space: что определяет уникальную карту (`(inputbitmap, randkey0, randkey1)`, ~230 базовых масок для 4pl Land). |
| [game_settings.md](game_settings.md) | Поведение движка по каждой опции лобби: `gen` (`mapsize`, `terraintype`, `relieftype`, `resourcestart`, `resourcemines`, `season`, `randkey0/1`) и `additional` (`startingunits`, `balloon`, `cannons`, `peacetime`, `century18`, `capture`, `marketdip`, `teams`, `limit`, `gamespeed`, `adviserassistant`). Глубокий разбор peacetime-механики (`gbool_peacemode`, ничейные ячейки, блок в `_unit_SearchEnemy`). Сами таблицы значений и каноничные русские названия — в [`reports/map/lobby_settings.md`](../reports/map/lobby_settings.md), машинный JSON — в [`derived/game_settings.json`](../derived/game_settings.json). |

## Игровые системы (правила, AI, наёмники)

Четыре документа про оверарх-механики: ИИ-противник, наёмничество, как заканчивается партия, и как юниты выбирают, в кого стрелять.

| Файл | Что внутри |
|---|---|
| [ai_behavior.md](ai_behavior.md) | AI: тик каждые 2.4 g-сек. Difficulty cheat = скорость постройки и найма (easy 30%, normal 50%, hard 75%, veryhard 100%, impossible 125%). **Стартовых ресурсов не получает**. Build order rule-based, нация-зависимый. Aggressor wave = 5 отрядов. Diplomacy: команды статически из лобби, без альянсов в процессе партии. |
| [mercenaries_diplomacy.md](mercenaries_diplomacy.md) | Дипломатический центр (`<nat>dip`): 21 нация × 1 здание, 4500–6500 HP, пререквизит — академия. Каталог из 8 наёмников (одинаковый у всех наций). Стоимость — только золото; `consume.gold` upkeep; `bnohungry = True`. Лимит масштабирования = 2× (против 20 000× у обычных юнитов). Pair-counter `archerdip ↔ archerturdip`. Rebellion = 18.31% за тик на hard+. С 2026-04-30 `data.json` учитывает блок `if (bmercenary)` — все 168 dip-строк правильные. |
| [victory_conditions.md](victory_conditions.md) | Условия победы и поражения: last-team-standing (`farmused = 0` ⇒ defeat). Wonder отсутствует. Score копится только для статистики (kill +2×, capture +5×, build +1×). Surrender (`bleave = True`), first-leaver penalty −w ELO. Time-limit отсутствует. Игровые режимы: skirmish, Historical Battle, Campaign, Scenario, Rated MP. |
| [target_selection.md](target_selection.md) | Алгоритм выбора цели через scan-grid: `_unit_SearchEnemyInCell` (случайный стартовый индекс по списку в ячейке) + `_unit_SearchEnemyScanCells` (минимум по relativeDist с балансировкой нагрузки `×(1 + STO_count × 0.125)` для рукопашников). 5 режимов `scanmode` (default / priest / capture / capture-fallback / AI sabotage). Семантика attack-move: `move_mode_attack` для пехоты и кавалерии, `attackpoint` для артиллерии с `bartprepare`. Умный поиск ловит врагов только в 30°-конусе впереди. |

## Engine internals (тики, RNG, сетевая модель)

Тройка документов про устройство движка. Идут в комплекте — каждый ссылается
на остальные. Без них нельзя объяснить, почему симуляция не воспроизводится
даже на одном хосте.

| Файл | Что внутри |
|---|---|
| [ticks_and_subticks.md](ticks_and_subticks.md) | Модель времени: real / game / frames. Главный progress-loop. Sub-tick state-machine intervals (135 мс у крестьян, 100 мс у юнитов). Variable timestep + adaptive game speed. Что нормализуется на Save / Load. |
| [determinism_audit.md](determinism_audit.md) | RNG audit: `random` vs `RandomExt` vs `SetRandomKey`. 7 RNG-сайтов в hot-path добычи. RNG в бою (5% triger хедшота). Почему шахты воспроизводимы. Импликации для симулятора и план мод-фикса. |
| [server_sync_architecture.md](server_sync_architecture.md) | Сетевая модель: C3 — server-authoritative, **не** lockstep. Net modes, паттерн `bProcess`, sync-пакеты (per-event + periodic в **real-time**, mod-53 unit params, on-demand full sync). |

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
- **«В кого выстрелит мой мушкетёр, если в радиусе три врага?»** → [target_selection.md](target_selection.md) §3.
- **«Чем `attack-move` отличается от обычного движения?»** → [target_selection.md](target_selection.md) §5.
- **«Какие опции есть в лобби и что они дают?»** → таблицы в [`../reports/map/lobby_settings.md`](../reports/map/lobby_settings.md), поведение движка — в [game_settings.md](game_settings.md). Машинный JSON для редакторов — [`../derived/game_settings.json`](../derived/game_settings.json).

## Что НЕ в этой папке

- Готовые таблицы цен / HP / урона — в [`../reference/`](../reference/).
- Производные расчёты (DPS, EHP, scaling, tech tree, vision и т. п.) — в [`../reports/`](../reports/README.md).
- Выходы симулятора экономики — в [`../simulations/`](../simulations/README.md).
- Open empirical questions для in-game замеров — встроены в §9 каждого профильного документа.
