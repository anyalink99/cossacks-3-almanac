# Артиллерия — сводный справочник

**Производный** файл (расчётный, не извлечение). Считается из [`data.json`](../../../data.json) скриптом [`compute/compute_artillery.py`](../../../compute/compute_artillery.py).

Артиллерийский юнит в коде — это тот, у кого `objprop.bartillery = True` [^1]. Подгруппа `bartprepare` включает анимацию подготовки выстрела перед каждым залпом — это `cannon`, `howitzer`, `framegun`. У `mortar` и `multicannon` подготовки нет: они стреляют непрерывно. Поведение приказа `attackpoint` для артиллерии — в [`recon/world/combat/target_selection.md`](../../recon/world/combat/target_selection.md) §5.2.

Морская артиллерия (battleship, galley, frigate и т. п.) — отдельная категория, см. [`reference/07_naval/README.md`](../../reference/07_naval/README.md). Гренадёр стреляет осколочным `mortarball`, но в `bartillery`-группу не входит и относится к пехоте — см. [`reports/combat/combat_stats.md`](combat_stats.md).

Содержание:

- [§1. Каталог и боевые статы](#1-каталог-и-боевые-статы)
- [§2. Стоимость одного выстрела](#2-стоимость-одного-выстрела)
- [§3. Экономика юнита и национальные различия](#3-экономика-юнита-и-национальные-различия)
- [§4. Лимит парка от Артиллерийского депо](#4-лимит-парка-от-артиллерийского-депо)
- [§5. Заметки и cross-references](#5-заметки-и-cross-references)

## §1. Каталог и боевые статы

Одна строка на уникальный набор статов основного оружия — если у нации стат отличается, она выносится в отдельную строку. Колонка **Подготовка** = `bartprepare`: задержка-анимация перед каждым выстрелом, фиксируется в скрипте, но точная длительность в `data.json` не извлечена и здесь не приводится. **Пауза** — холодная перезарядка после выстрела (`weapon.pause` в g-сек). **Точность** — `weapon.dispertion` в пикселях и тайлах; меньше = точнее. Радиус — `weapon.radiusmax` (тайлы); `radiusmin` показан, если у юнита есть мёртвая зона ближнего боя.

| `sid` | Класс | Нации | dmg | пауза | DPS, g-сек | Радиус | Точность | Подготовка |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | :---: |
| `cannon` | Пушка | все 21 | 1800 | 10.94 s | 164.53 | 10.31..40.5 t | 225 px · 4.22 t | ✓ |
| `framegun` | Пушка | sco | 500 | 2.81 s | 177.94 | 3.75..33.75 t | 250 px · 4.69 t | ✓ |
| `howitzer` | Мортира | все 21 | 4000 | 18.75 s | 213.33 | 13.13..26.25 t | 300 px · 5.63 t | ✓ |
| `mortar` | Сверхмортира | все 21 | 200 | 7.81 s | 25.61 | 23.44..48.75 t | 200 px · 3.75 t | — |
| `multicannon` | Многоствольная пушка | aus, bav, den, eng, fra … (+12) | 500 | 1.88 s | 265.96 | 0.19..13.13 t | — | — |

Колонка **DPS, g-сек** — это `damage / pause`, без учёта формационных бонусов (у артиллерии своих формаций нет), AoE-капа и защиты цели. Реальный output по толпе обычно ниже из-за `AoE damage cap = floor(1 + (r/0.35)²)` (см. [`recon/world/combat/combat_damage_pipeline.md` §6.5](../../recon/world/combat/combat_damage_pipeline.md)).

## §2. Стоимость одного выстрела

`weapon[i].cost[gc_resource_type_*]` — ресурсы, которые списываются в момент выстрела (а не за каждый интервал паузы). Ноль означает, что конкретный ресурс не тратится; у мортир коэффициент `coal` — порох, у пушек `iron + coal` — ядро + порох. У `multicannon` (картечница) цены может не быть, потому что её стволу не присваивается `weapon.cost` в скрипте.

**Эффективность по цене.** Колонка `dmg / shot_cost_g` — это `damage`, делённый на «золотой эквивалент выстрела». Эквивалент считается по стандартному курсу `mar.def` (`reference/06_market/README.md`): `iron × 140 + coal × 140 + wood × 50 + stone × 50 + food × 25 + gold × 1` — то есть переводим расход в условные единицы золота по дефолтным buy-ценам. Это удобная грубая мера, чтобы сравнить, сколько ты «платишь» за единицу урона при разных типах артиллерии. Не учитывает закупочную цену самой пушки, food-апкип и износ от ответного огня.

| `sid` | Нации | Тип снаряда | dmg | iron | coal | wood/stone/gold | shot_cost_g | dmg / shot_cost_g |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `cannon` | все 21 | cannonball | 1800 | 20 | 40 | — | 8400 | 0.21 |
| `framegun` | sco | cannonball | 500 | 30 | 40 | — | 9800 | 0.05 |
| `howitzer` | все 21 | cannonball | 4000 | 20 | 100 | — | 16800 | 0.24 |
| `mortar` | все 21 | mortarball | 200 | 20 | 30 | — | 7000 | 0.03 |
| `multicannon` | aus, bav, den, eng, fra … (+12) | cannister | 500 | 40 | 30 | — | 9800 | 0.05 |

**Картечь** (cannister) у `cannon` и `multicannon` — отдельное оружие со своей `pause` и стоимостью. У `cannon` `weapon[1].damage = 0`: картечь у обычной пушки реализована не прямой записью в `damage`, а через sub-projectile-механизм `_weapon_SyncWeapon` [^2]. Каждый выстрел картечью порождает несколько подснарядов; их урон выставлен в момент создания weapon-определения и в `data.json` напрямую не сводится. У `multicannon` `weapon[0]` уже типа `cannister`, и вся характеристика там и сидит. Сравнивать DPS картечи и ядра напрямую по `data.json` поэтому нельзя без чтения weapon-script'а.

## §3. Экономика юнита и национальные различия

Цена покупки, время постройки, HP, щит, скорость и upkeep по золоту. Если у нации те же значения — одна строка, нации сгруппированы.

| `sid` | Нации | Цена | bt, g-сек | HP | shield | speed | `consume[gold]` | gold/г-сек | score |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `cannon` | все 21 | 250 W · 400 G · 400 I | 75.0 | 9000 | 75 | 20 | 300 | 0.48 | 50 |
| `howitzer` | все 21 | 250 W · 350 G · 300 I | 94.0 | 3000 | 75 | 20 | 350 | 0.56 | 25 |
| `mortar` | все 21 | 100 W · 75 G · 200 I | 25.0 | 400 | 25 | 24 | 50 | 0.08 | 100 |
| `multicannon` | aus, bav, den, eng, fra … (+12) | 200 W · 400 G · 250 I | 50.0 | 2000 | 50 | 16 | 300 | 0.48 | 25 |
| `framegun` | sco | 200 W · 300 G · 150 I | 50.0 | 3000 | 50 | 20 | 300 | 0.48 | 50 |

`consume[gold]` — поле `objprop.consume[gc_resource_type_gold]`. Реальный расход считается формулой `consume × gc_time_to_frames / 20000` за каждую игровую секунду (так как процедура `_player_ProcessResourceConsume` использует `speed = 20000` в делителе). Колонка `gold/г-сек` уже учитывает эту формулу. Артиллерия — единственный класс, у которого `consume.gold > 0` для всех юнитов: пушку нужно «содержать», даже если она не стреляет. У пехоты и кавалерии `consume.gold = 0`. Подробнее — в [`../../recon/world/economy/hunger_and_rebellion.md` §2.3](../../recon/world/economy/hunger_and_rebellion.md).

## §4. Лимит парка от Артиллерийского депо

Здание `<nat>art` (Артиллерийское депо). При постройке добавляет к `gPlayer[plInd].artlimit[i]` константу `objprop.artdepo[i]` [^3]. Лимит линеен по числу депо — без капа сверху. Без депо лимит = 0 [^4], и любая попытка построить артиллерию упирается в `gc_result_checkaccesscontrolreq_artlimit` [^5].

Базовая раздача с одного депо [^6]:

| Индекс `artind` | Юнит-индекс | Слотов с одного депо |
| --- | --- | ---: |
| 0 — `gc_obj_artind_cannon` | `cannon` | 5 |
| 1 — `gc_obj_artind_howitzer` | `howitzer` | 5 |
| 2 — `gc_obj_artind_mortar` | `mortar` | 10 |
| 3 — `gc_obj_artind_multicannon` | `multicannon` | 3 |

Иначе говоря, чтобы выкатить полный мортирный батальон в 30 штук, нужно три Артиллерийских депо (3 × 10 = 30 слотов под `mortar`).

**Цена и параметры самого Артиллерийского депо** по нациям. Базовое значение по умолчанию: `costpercent = 200`, `HP = 40000`, `score = 1400` [^7]. Нации, у которых этот юнит дешевле или дороже, показаны явно — у Украины и Турции есть `if (i = ukr/tur)`-override [^8].

| Нация | HP | Цена (food/wood/stone/gold/iron/coal) | bt, g-сек | costpercent |
| --- | ---: | --- | ---: | ---: |
| alg, aus, bav, den, eng … (+14) | 40000 | 0 / 100 / 1000 / 0 / 0 / 1400 | 245.94 | 200 |
| ukr | 40000 | 0 / 4250 / 4400 / 100 / 0 / 1400 | 245.94 | 200 |
| tur | 40000 | 0 / 500 / 1200 / 0 / 0 / 1400 | 245.94 | 200 |

## §5. Заметки и cross-references

- **Подготовка перед выстрелом.** `bartprepare = True` означает, что перед каждым выстрелом проигрывается длинная анимация. Поведение движка при отдаче ордера на стрельбу — `_unit_TryAttackPoint` [^9]. Точная длительность подготовки берётся из `.aaf`-анимации `attack0` юнита; в `data.json` она не извлечена. Для оценок используем `weapon.pause` как «холодную перезарядку» поверх любых анимационных задержек.

- **Точность падает в движении.** Стрелок и артиллерия в движении (`standtime < 0.25 g-сек`) теряют до `gc_obj_maxattackradiusdisp = 3` тайлов эффективного радиуса [^10]. Дополнительное рассеивание `dispertion` остаётся прежним. Подробнее — [`recon/world/combat/ranged_units_behavior.md` §4](../../recon/world/combat/ranged_units_behavior.md#4-штраф-к-дальности-при-движении-standtime).

- **Точность улучшается апгрейдами Академии.** `aca.20` (Research new sighting devices for artillery) — −35% к dispertion. `aca.27` (Develop mathematics) — ещё −35%, накапливается с aca.20. После обоих остаётся `0.65 × 0.65 ≈ 0.42` от исходного, то есть точность вырастает примерно в 2.4 раза. Применяется только к артиллерии; у мушкетеров и лучников прямого dispertion-апгрейда нет.

- **AoE-кап ловит толпу.** При взрыве снаряда урон получают только первые `count = floor(1 + (r/0.35)²)` юнитов в радиусе [^11]. Для cannon (`r ≈ 1`) это 9 юнитов, для mortar (`r ≈ 2`) — 33. Растянутая линия страдает гораздо больше, чем плотная толпа.

- **AI цели для артиллерии.** Решение, куда стрелять, идёт через `_unit_SearchEnemyLongRangeArtillery` [^12] — это отдельная ветка, не общий `_unit_SearchVictimOnProgress`. AI-юниты артиллерии целят прицельно по дистанции `[radiusmin .. radiusmax]`, учитывая `bsearchmaxattradius`. Эта ветка отличается от обычной scan-cells и описана только косвенно — см. [`recon/world/target_selection.md`](../../recon/world/combat/target_selection.md) §7 (open question № 4).

- **`bartprepare` и `attack-move`.** Артиллерия с `bartprepare = True` получает приказ `gc_obj_order_type_attackpoint` через `_player_OrderUnitsToAttackPoint` [^13] — это стрельба по координате, не по конкретной цели. Поведение для не-артиллерийских юнитов другое — они движутся с `move_mode_attack`. Подробности — [`recon/world/target_selection.md`](../../recon/world/combat/target_selection.md) §5.


## Источники

Все ссылки относительно `data/scripts/` в установке Cossacks 3.

[^1]: `objprop.bartillery := True` для пяти артиллерийских юнитов — `lib/unit.script:1725, 1757, 1788, 1815, 1847`.

[^2]: sub-projectile-механизм картечи (`_weapon_SyncWeapon`) — `lib/weapon.script:529`.

[^3]: суммирование `artdepo[i]` в `gPlayer[plInd].artlimit[i]` — `lib/unit.script:3826-3830`.

[^4]: инициализация `artlimit[k] := 0` при старте партии — `lib/player.script:3169-3171`.

[^5]: проверка `artcount[i] >= artlimit[i]` → `gc_result_checkaccesscontrolreq_artlimit` — `lib/miscext2.script:114-116`.

[^6]: базовая раздача `artdepo[0..3]` для `<nat>art` — `lib/unit.script:2441-2444`:

    ```pascal
    objprop.artdepo[0] := 5;
    objprop.artdepo[1] := 5;
    objprop.artdepo[2] := 10; // c1 = 30
    objprop.artdepo[3] := 3;
    objprop.bartdepo := True;
    ```

[^7]: базовые параметры Артиллерийского депо — `lib/unit.script:2440`.

[^8]: `if (i = ukr) ...` и `if (i = tur) ...` для цены депо — `lib/unit.script:2447-2448`.

[^9]: `_unit_TryAttackPoint` и связанные ветки — `lib/unit.script:7512`.

[^10]: штраф к радиусу для движущегося стрелка — `lib/unit.script:5151-5156`.

[^11]: `AoE damage cap = floor(1 + (r/0.35)²)` — `lib/miscext2.script:_misc_DoRoundDamage`.

[^12]: `_unit_SearchEnemyLongRangeArtillery` (отдельная ветка для AI-арты) — `lib/unit.script:11184`.

[^13]: `_player_OrderUnitsToAttackPoint` (ветка для `bartprepare = True`) — `lib/player.script:2447-2481`.
