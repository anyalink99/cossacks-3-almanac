<a id="бой-и-движение"></a>
# Combat and Movement

[← Quick reference](../README.md)

This chapter explains the rules that determine a battle’s outcome: how damage
is calculated, what armor protects against, why formations matter, and why a
listed weapon range does not guarantee a hit.

<a id="с-чего-начать"></a>
## Where to start

| Question | Read |
|---|---|
| Which unit attacks faster? | [Attack rates](../../reports/combat/attack_rates.md) |
| How do I compare unit health, damage, and protection? | [Combat statistics](../../reports/combat/combat_stats.md) |
| How do cannons, howitzers, and mortars work? | [Artillery](../../reports/combat/artillery.md) |
| How do similar units from different nations compare? | [Unit comparisons](../compare/units/README.md) |
| How does naval combat work? | [Navy](../07_naval/README.md) |

<a id="как-считается-урон"></a>
## Damage calculation

The target’s armor and protection against the relevant weapon type are
subtracted from the weapon’s base damage. Final damage cannot fall below one:

```text
final damage = max(1, base damage - armor - protection against weapon type)
```

Pikes, swords, bullets, arrows, grapeshot, and cannonballs use different
protection values. A unit that withstands musket fire well may still be
vulnerable to a pike or cannonball.

Formations, upgrades, distance, shot dispersion, and weapon-specific behavior
also affect the practical result. The complete sequence is documented in
[How damage is calculated](../../recon/world/combat/combat_damage_pipeline.md).

<a id="дальность-и-точность"></a>
## Range and accuracy

Range is the maximum distance at which a weapon can reach a target. For ranged
weapons it is not a hit probability: greater distance and dispersion make
bullets and arrows miss more often. A unit that has just moved also needs time
to stop before it can fire at full effectiveness.

See [Ranged-unit behavior](../../recon/world/combat/ranged_units_behavior.md)
and [Target selection](../../recon/world/combat/target_selection.md).

<a id="скорость-движения"></a>
## Movement speed

Speed values in the tables are relative engine units. They are useful for
in-game comparison but do not equal tiles per second. Light cavalry is usually
faster than heavy cavalry, peasants are faster than ordinary infantry, and
artillery and large ships are among the slowest units.

<a id="построения"></a>
## Formations

An Officer and a Drummer allow units to form a detachment. Line, column, and
square formations change unit placement and provide combat bonuses. Large
formations must retain their Officer, Drummer, and minimum troop count; if
too few members remain, the formation breaks.

See [Formations and their combat bonuses](../../recon/world/combat/formations.md)
for valid sizes and exact bonuses.

<a id="стоимость-стрельбы"></a>
## Cost of firing

Some ranged units, towers, artillery, and ships consume iron and coal with
each shot. This cost is separate from recruitment or construction. Exact
values are listed in [Combat statistics](../../reports/combat/combat_stats.md)
and [Artillery](../../reports/combat/artillery.md).

<a id="подробные-статьи"></a>
## Further reading

- [Unit orders](../../recon/world/combat/unit_commands.md)
- [Vision and fog of war](../../recon/world/combat/vision_and_fow.md)
- [Pathfinding and collisions](../../recon/world/combat/pathfinding.md)
- [Towers](../../recon/world/combat/towers.md)
- [Walls and gates](../../recon/world/combat/walls_and_gates.md)
- [Naval combat](../../recon/world/combat/naval_combat.md)
