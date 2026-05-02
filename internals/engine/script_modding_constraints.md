# Ограничения скриптинга при модинге: DoDamage и смерть юнита

Практические выводы, полученные при разработке мода Deterministic Cossacks.
Описывают поведение движка, которое не задокументировано в исходниках напрямую.

> **Связанные документы:**
> [`combat_damage_pipeline` (recon)](../../docs/recon/world/combat/combat_damage_pipeline.md)
> — формула урона; [`animation_system.md`](animation_system.md)
> — порядок вызовов при атаке.

---

## 1. Структура `_misc_DoDamage` (miscext2.script ~line 250)

Функция делится на два принципиально разных блока:

**Блок A — bookkeeping при убийстве** (`if TObj(pobj2).hp <= 0`, ~line 443):
- Начисление очков атакующему (`gPlayer[plInd].counter.scores`)
- Инкремент `TObj(pobj).kill`
- Перебор `gc_argunit_inside` (выгнать юнитов из транспорта/шахты)

**Блок B — death trigger** (`if bProcessLogic`, ~line 510):
```pascal
// для атакующего (pobj / goHnd):
if (not bSkipOnDeath) and (pobj<>nil) and (TObj(pobj).hp<=0) then begin
   if (not TObj(pobj).bdead) then
   GameObjectExecuteStateByHandle(goHnd, 'OnDeath');
   _unit_SetTagStates(goHnd, gc_statetag_essential_death);
end;

// для цели (pobj2 / trgHnd):
if (TObj(pobj2).hp<=0) then begin
   GameObjectExecuteStateByHandle(trgHnd, 'OnDeath');
   _unit_SetTagStates(trgHnd, gc_statetag_essential_death);
end;
```

Блок A и блок B **не связаны напрямую**: можно войти в блок A без попадания в B
(если `bProcessLogic = false`), и наоборот.

`bSkipOnDeath` выставляется только в peace-mode ветке (~line 308/318).
В обычном бою всегда `false`.

---

## 2. Нельзя убивать атакующего изнутри `_misc_DoDamage`

**Симптом:** `TObj(pobj).hp := 0` внутри kill block (блок A) → юнит зависает:
не умирает, не действует, нельзя выделить.

**Причина:** C++ вызывает `_misc_DoDamage` в середине attack sequence. После
возврата из скрипта движок продолжает обрабатывать атаку для `goHnd`. Если
скрипт успел выставить `hp = 0`, блок B той же функции вызывает
`_unit_SetTagStates(gc_statetag_essential_death)` — юнит получает death state,
но C++ attack sequence ещё не завершён. Результат — конфликт состояний.

**Вывод:** Любое изменение hp / состояния АТАКУЮЩЕГО (`goHnd/pobj`) изнутри
`_misc_DoDamage` ненадёжно. Цель (`trgHnd/pobj2`) убивать безопасно — движок
ожидает этого.

---

## 3. Рекурсивный вызов `_misc_DoDamage` вызывает двойную смерть

При попытке `_misc_DoDamage(goHnd, goHnd, 9999, weapind, weapkind)` из kill block:

1. Вложенный вызов: `TObj(pobj2).hp -= 9999` → блок B → `_unit_SetTagStates(essential_death)` **первый раз**
2. Вложенный вызов возвращается
3. Внешний вызов продолжает работу, доходит до блока B (~line 512): `TObj(pobj).hp <= 0` → `_unit_SetTagStates(essential_death)` **второй раз**

Двойной `_unit_SetTagStates(gc_statetag_essential_death)` ломает анимационный
конечный автомат — юнит застревает в вечной анимации атаки.

`GameObjectExecuteStateByHandle(goHnd, 'OnDeath')` защищён проверкой
`if (not TObj(pobj).bdead)`, но `_unit_SetTagStates(essential_death)` — нет.

---

## 4. `attackmaxdelay` нельзя использовать как флаг/sentinel

`attackmaxdelay` читается движком как максимальное время cooldown атаки.
Установка `attackmaxdelay := 9999` эффективно блокирует юнита на 9999 g-сек —
он перестаёт атаковать полностью. Поле не подходит для хранения произвольных
флагов.

Аналогично опасно злоупотреблять `attackdelay` значениями >> обычной паузы оружия.

---

## 5. Безопасное место для kill-trigger извне DoDamage

Функция `SearchEnemy` / retarget gate (unit.script ~line 8400) вызывается в
**регулярном update loop** юнита, вне attack sequence и вне `_misc_DoDamage`.
Установка `hp := 0` + `_unit_SetTagStates(gc_statetag_essential_death)` здесь
работает корректно.

Паттерн: после убийства `attackdelay` выставляется в ≥ 1.5 г-сек. Пока
`attackdelay > 0` retarget gate вызывается каждый тик. Это создаёт надёжное
окно для проверки пост-kill состояния атакующего без рекурсии.

```pascal
// unit.script retarget gate — безопасный kill trigger:
if (pobj<>nil) and (TObj(pobj).hp > 0) and (TObj(pobj).hp < 3)
and (TObj(pobj).attackdelay > 0) then begin
   TObj(pobj).hp := 0;
   _unit_SetTagStates(goHnd, gc_statetag_essential_death);
end
```

---

## 6. `_unit_DestroyObj` (miscext2.script:4205)

Полная cleanup-функция: убирает с миникарты, очищает orders, ставит
`bdead := True`, удаляет из счётчиков игрока. Никогда не вызывается из
скриптов (только определена). Вероятно, вызывается из C++ напрямую или
является dead code. Форвардная ссылка из начала miscext2.script теоретически
работает в DWS (двухпроходная компиляция), но практически не тестировалась.

---

## 7. `gc_argunit_stolist` — список атакующих юнита

```pascal
var psto : Pointer = _misc_GetObjectArgData(hnd, gc_argunit_stolist);
var n : Integer = TIntegerList(psto).GetCount;
```

`n` = количество юнитов, **сейчас атакующих** `hnd`. Доступно для любого
handle — как цели, так и атакующего. Обновляется движком в реальном времени.

---

## 8. Порядок вызовов при атаке юнита

На основе наблюдений (точный C++ порядок неизвестен):

1. Анимация атаки достигает swing point → C++ callback → `_misc_DoDamage`
2. Анимация завершается → C++ → `_unit_ApplyAttackPause` (выставляет `attackdelay`)
3. Юнит входит в idle/retarget → `SearchEnemy` / retarget gate

`_unit_ApplyAttackPause` вызывается **после** `_misc_DoDamage`, не до.
Поэтому sentinel, выставленный в DoDamage, виден в `_unit_ApplyAttackPause` —
но только если движок успевает вызвать её до следующего attack cycle.
На практике надёжнее использовать retarget gate (п. 5).
