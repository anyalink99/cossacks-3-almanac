# Recon notes

Глубокие исследования механик Cossacks 3 — то, что нельзя извлечь автоматическим парсером и что нужно переварить, чтобы понять цифры в [`output/reference/`](../output/reference/). Каждый файл — самостоятельный документ; перекрёстные ссылки размечены явно.

## Документы

### Логика мира

| Файл | Что внутри |
|---|---|
| [peasant_extraction.md](peasant_extraction.md) | Добыча ресурсов: цикл крестьянина, формулы, шахты (включая апгрейды до 95 absorber), поля (HP / regen / restart), efficiency-апгрейды, карта как вход (densities, гарантированные стартовые ресурсы), пеньки = бесконечный wood pool. |
| [building_mechanics.md](building_mechanics.md) | Здания: footprint mask (1 cell = 0.5 тайла), repair (бесплатно, +20 HP/удар), construction (delta = 0.359/buildtime per hit), builder slots, стены (2×2 на сегмент, 4-12 slots), гарнизон/башни, capture radius = 4 тайла. |
| [map_generation_pipeline.md](map_generation_pipeline.md) | Полный таймлайн `DoGenerate`: cCircle1/2/3 forbidden zones, `SetupStartingResources` (1× stoneforest + 2× stones + 3× forests в радиусе 5-22), Phase-1 / Phase-2 mines, FillOwnerMap, peacetime borders. Плюс seed space — что определяет уникальную карту (`(inputbitmap, randkey0, randkey1)`, ~230 базовых масок для 4pl Land). |

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

## Что НЕ в этой папке

- Готовые таблицы цен/ХП/урона — это [`output/reference/`](../output/reference/).
- Производные расчёты (DPS, EHP, scaling, tech tree) — [`output/reports/`](../output/reports/README.md).
- Выходы симулятора экономики — [`output/simulations/`](../output/simulations/README.md).
- Open empirical questions для in-game замеров — встроены в §9 каждого профильного документа.
