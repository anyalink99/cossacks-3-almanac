## Формула добычи

```
delivered = (base_portion × eff) / 100   # integer division
```

Пример: с апгрейдами academy.1 (+40% food) и mill.1 (+140% food) → `eff = 100 + 40 + 140 = 280`. Крестьянин приносит `45 × 280 / 100 = 126` еды за рейс (вместо базовых 45).

Все апгрейды eff — в `player.script:1813-1828`. Список — в [05_upgrades.md](05_upgrades.md#economy-eff).
