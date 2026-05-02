## О чём эта глава

Сводные **таблицы** по бою и движению: типы оружия, скорости юнитов,
матрица контр-эффективности, перекрёстная таблица «апгрейды ×
характеристики», стоимость одного выстрела. Числа извлечены из
скриптов и сгенерированы автоматически из [`data.json`](../../data.json).

**Подробные разборы механик** — в `recon/world/combat/`:

- [combat_damage_pipeline.md](../recon/world/combat/combat_damage_pipeline.md)
  — конвейер урона: 6 шагов формулы, хедшот, AoE-кап, дружественный
  огонь, peace-mode, упрощения.
- [formations.md](../recon/world/combat/formations.md) — LINE /
  SQUARE / KARE: 149 формаций, бонусы строя, hold-mode FSM, порог
  расформирования.
- [ranged_units_behavior.md](../recon/world/combat/ranged_units_behavior.md)
  — поведение стрелков: standground, bartprepare, RunAway, штраф к
  дальности при движении, мульти-оружие, high ground.
- [target_selection.md](../recon/world/combat/target_selection.md)
  — алгоритм выбора цели через scan-grid, attack-move, лечение
  священниками, реакция отряда на удар, рассеяние выстрелов.
- [unit_commands.md](../recon/world/combat/unit_commands.md) —
  очередь приказов, режимы атаки, hold-fire, rally points.
- [vision_and_fow.md](../recon/world/combat/vision_and_fow.md) —
  туман войны и формула радиуса обзора `20 + 4 × vision`.
- [pathfinding.md](../recon/world/combat/pathfinding.md) —
  движение и push.
- [artillery_specifics.md](../recon/world/combat/artillery_specifics.md)
  — артиллерия: `bartprepare`, `attackpoint`, лимиты через арт-депо.
- [towers.md](../recon/world/combat/towers.md)
  — башни и гарнизон.
- [naval_combat.md](../recon/world/combat/naval_combat.md) —
  морской бой.
- [walls_and_gates.md](../recon/world/combat/walls_and_gates.md)
  — стены и ворота.

## Типы оружия (`gc_obj_weapon_kind_*`)

| Kind | Описание | Носители |
|---|---|---|
| `pike` | Длинное копьё / пика | Пикинёры 17 / 18 в. |
| `sword` | Меч / сабля | Лёгкая пехота, мечники, кавалерия в ближнем бою |
| `bullet` | Пуля огнестрела | Мушкетёр, стрелец, янычар, драгун и т.д. |
| `arrow` | Стрела / болт | Лучник (`SHOTLU`-боеприпас) |
| `cannonball` | Пушечное ядро | Пушка, башня, фрегат (одиночный выстрел) |
| `cannister` | Картечь | Пушка ближнего боя, многоствольная пушка |

Каждый `kind` имеет свою колонку `protection[kind]` у целей. См.
формулу урона в
[`recon/world/combat/combat_damage_pipeline.md` §2](../recon/world/combat/combat_damage_pipeline.md).

Детали — в
[`recon/world/combat/combat_damage_pipeline.md`](../recon/world/combat/combat_damage_pipeline.md)
и [`ranged_units_behavior.md`](../recon/world/combat/ranged_units_behavior.md).

## `uniqrnd` — индивидуальное случайное число юнита

При спавне каждый юнит получает `uniqrnd ∈ [0, 1)` — фиксированное
случайное число, остающееся неизменным до смерти (см.
[`internals/engine/rng_implementation.md`](../../internals/engine/rng_implementation.md)).
Используется в **четырёх** механиках одновременно:

| # | Где применяется | Эффект |
|---:|---|---|
| 1 | Бонус хедшота | `+floor(uniqrnd × 500)` дополнительного урона при крите |
| 2 | Эффективная max-range | `radiusmax −= uniqrnd × 3` тайла во время `standtime < 0.25` g-sec |
| 3 | Search timing | `nextSearch = now + uniqrnd × 0.15 + 0.3` сек — юниты не сканируют синхронно |
| 4 | Multiplayer sync seed | `SetRandomKey(floor(uniqrnd × MaxInt))` для синхронизации решений между клиентами |

Детали — в
[`recon/world/combat/combat_damage_pipeline.md`](../recon/world/combat/combat_damage_pipeline.md)
и [`ranged_units_behavior.md`](../recon/world/combat/ranged_units_behavior.md).
