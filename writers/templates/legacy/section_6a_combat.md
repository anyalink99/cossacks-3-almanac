## 6. Боевая математика

### 6a. Damage formula

Расчёт реально нанесённого урона (`miscext2.script:_misc_DoDamage`):

```
damage = weapon.damage
if (target is fast cavalry on the move AND weapon kind in {arrow, bullet}):
    damage -= 5  # headshot bonus
if (target is fully built):
    damage -= target.shield
else:  # still under construction
    damage -= target.shield // 3
if (target in formation): damage -= squad.AddShield  (or AddShieldHold if hold-mode)
damage -= target.protection[weapon.kind]
damage = max(1, damage)  # minimum 1 damage per hit
target.hp -= damage
```

**Ключевые свойства:**

- `protection` и `shield` уменьшают урон **аддитивно** (не процентно).
- Минимум **1 хп** урона за попадание — нет нулевого урона, даже если protection > damage.
- Танки / слоны (высокий shield) безусловно лучше, чем тяжёлые protection — shield применяется ВСЕГДА.
- Pikeman vs cavalry: pike kind с damage 8-10 vs heavy cavalry protection_pike (типично 0-3) ≈ 5-10 хп / удар.
- Cavalry vs pikeman: sword / saber damage ≈ 5-7 vs pike protection (0-3) ≈ 2-7 хп / удар.
- Ranged attack: bullet / arrow damage 9-12 vs musketeer protection (default 0-4) ≈ 5-12 хп / удар; против тяжёлой пехоты с `protection_bullet ≥ 6` урон режется существенно.
