### 6b. Скорости юнитов (абстрактные единицы)

Базовые `gc_obj_speed_*` из `dmscript.global:603-620`. Это **относительные** значения скорости, **не тайлы / сек**. Реальная скорость зависит от animation `walkInterval`, `walkintervalfactor` юнита и game speed. Для перевода в тайлы / сек нужен empirical test.
