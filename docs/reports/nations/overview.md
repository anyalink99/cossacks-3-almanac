# Cossacks 3 — Cross-nation overview

**Производный** отчёт. Считается из `docs/data.json` скриптом [`compute/compute_nations_overview.py`](../../compute/compute_nations_overview.py).

Side-by-side сравнение всех 21 наций. Для подробностей по конкретной нации — [`reference/nations/<nat>.md`](../reference/nations/README.md).

## §1. Размер ростера и эпохальный доступ

Сколько разных юнит-sid'ов доступно нации (`?` — мисс / тест-юниты, Drummer/Officer/Priest и т.п. отнесены отдельно). Колонка **18c** — есть ли у нации Barracks 18-в. (`<nat>ba2`); если нет — нация заперта в 17-в. эпохе.

| Nation | Total units | Combat | Shooters | Cavalry | Grenadiers | Ships | 18c access |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | :---: |
| **alg** Algeria | 25 | 18 | 2 | 2 | 1 | 5 | ❌ |
| **aus** Austria | 38 | 30 | 5 | 7 | 2 | 6 | ✅ |
| **bav** Bavaria | 35 | 27 | 4 | 6 | 2 | 6 | ✅ |
| **den** Denmark | 35 | 27 | 4 | 6 | 2 | 6 | ✅ |
| **eng** England | 36 | 28 | 5 | 6 | 2 | 6 | ✅ |
| **fra** France | 37 | 29 | 5 | 7 | 2 | 6 | ✅ |
| **hun** Hungary | 36 | 28 | 5 | 6 | 2 | 6 | ✅ |
| **net** Netherlands | 35 | 27 | 4 | 6 | 2 | 6 | ✅ |
| **pie** Piedmont | 35 | 27 | 4 | 6 | 2 | 6 | ✅ |
| **pol** Poland | 37 | 29 | 4 | 8 | 2 | 6 | ✅ |
| **por** Portugal | 36 | 28 | 5 | 6 | 2 | 6 | ✅ |
| **pru** Prussia | 36 | 28 | 4 | 6 | 3 | 6 | ✅ |
| **rus** Russia | 35 | 27 | 4 | 6 | 2 | 6 | ✅ |
| **sax** Saxony | 36 | 28 | 4 | 7 | 2 | 6 | ✅ |
| **sco** Scotland | 28 | 21 | 3 | 3 | 1 | 5 | ✅ |
| **spa** Spain | 36 | 28 | 4 | 6 | 2 | 6 | ✅ |
| **swe** Sweden | 36 | 28 | 4 | 7 | 2 | 6 | ✅ |
| **swi** Switzerland | 36 | 28 | 5 | 6 | 2 | 6 | ✅ |
| **tur** Turkey | 29 | 21 | 3 | 3 | 1 | 6 | ❌ |
| **ukr** Ukraine | 22 | 16 | 3 | 4 | 1 | 4 | ❌ |
| **ven** Venice | 35 | 27 | 4 | 6 | 2 | 6 | ✅ |

## §2. Покрытие стандартных построек

`✅` = нация имеет здание, `—` = у нации этого здания нет. Полный каталог зданий — [03_buildings.md](../reference/03_buildings.md).

| Нация | Городской центр | Дом | Мельница | Склад | Башня | Стена/ворота | Шахта | Порт | Дипломатический центр |
| --- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **alg** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **aus** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **bav** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **den** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **eng** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **fra** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **hun** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **net** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **pie** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **pol** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **por** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **pru** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **rus** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **sax** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **sco** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **spa** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **swe** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **swi** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **tur** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **ukr** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ | ✅ |
| **ven** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

**Заметные пропуски:**

- **ukr** — нет: Башня, Стена/ворота

## §3. Уникальные юниты по нациям

Юниты с `sid`, который встречается только у одной нации (после слияния `<unit>dip`-наёмников). Это «фишечные» отряды, с которыми нация ассоциируется. Мерсенарские sid (`<unit>dip`) показываются отдельно в §5.

| Nation | Уникальные sid (usage · HP) |
| --- | --- |
| **alg** | `mameluke` _Mameluke_ (Heavy Cavalry, HP=280)<br>`archer` _Archer_ (Archer, HP=40) |
| **aus** | `croat` _Croat_ (Light Cavalry, HP=260)<br>`roundshier` _Roundshier_ (Light Infantry, HP=100)<br>`pandur` _Pandur_ (Shooter, HP=85)<br>`musketeeraus` _Musketeer, 17th century_ (Shooter, HP=55) |
| **bav** | `grenadierbav` _Grenadier_ (Grenadier, HP=125)<br>`musketeer18bav` _Musketeer, 18th century_ (Shooter, HP=100) |
| **den** | `grenadierden` _Grenadier_ (Grenadier, HP=125)<br>`musketeer18den` _Musketeer, 18th century_ (Shooter, HP=100) |
| **eng** | `highlander` _Highlander_ (Shooter, HP=130) |
| **fra** | `kingmusketeer` _King's Musketeer_ (Mounted Shooter, HP=280)<br>`dragoon18fra` _Dragoon, 18th century_ (Mounted Shooter, HP=140)<br>`chasseur` _Chasseur_ (Shooter, HP=75) |
| **hun** | `hussarhun` _Hussar_ (Light Cavalry, HP=250)<br>`lightcavalry` _Light cavalry_ (Mounted Shooter, HP=175)<br>`grenadierhun` _Grenadier_ (Grenadier, HP=125)<br>`pandurhun` _Szekely_ (Shooter, HP=75)<br>`gauduk` _Hajduk_ (Shooter, HP=60) |
| **net** | `dragoon18net` _Dragoon, 18th century_ (Mounted Shooter, HP=320)<br>`musketeernet` _Musketeer, 17th century_ (Shooter, HP=65) |
| **pie** | `dragoon18pie` _Dragoon, 18th century_ (Mounted Shooter, HP=200)<br>`padre` _Padre_ (Light Infantry, HP=100) |
| **pol** | `wingedhussar` _Winged Hussar_ (Light Cavalry, HP=225)<br>`reiterpol` _Light Reiter_ (Heavy Cavalry, HP=190)<br>`dragoonpol` _Pospolite ruszenie_ (Mounted Shooter, HP=185)<br>`pikemanpol` _Pikeman, 17th century_ (Light Infantry, HP=90)<br>`musketeerpol` _Musketeer, 17th century_ (Shooter, HP=70) |
| **por** | `pikemanpor` _Pikeman, 17th century_ (Light Infantry, HP=100)<br>`jagerpor` _Volunteer_ (Shooter, HP=50) |
| **pru** | `hussarpru` _Hussar_ (Light Cavalry, HP=240)<br>`grenadierpru` _Grenadier_ (Grenadier, HP=125)<br>`musketeer18pru` _Musketeer, 18th century_ (Shooter, HP=100) |
| **rus** | `vityaz` _Vityaz_ (Heavy Cavalry, HP=380)<br>`cossackdon` _Don Cossack_ (Heavy Cavalry, HP=220)<br>`officerrus` _Commander_ (Light Infantry, HP=125)<br>`drummerrus` _Drummer, 17th century_ (Light Infantry, HP=100)<br>`pikemanrus` _Spearman_ (Light Infantry, HP=85)<br>`strelet` _Strelets_ (Shooter, HP=85)<br>`pearus` _Serf_ (Peasant, HP=50) |
| **sax** | `guardcavalrysax` _Cavalry Guard_ (Heavy Cavalry, HP=320)<br>`grenadiersax` _Grenadier_ (Grenadier, HP=100)<br>`musketeer18sax` _Musketeer, 18th century_ (Shooter, HP=90) |
| **sco** | `framegun` _Frame gun_ (Cannon, HP=3000)<br>`lancersco` _Lancer_ (Heavy Cavalry, HP=320)<br>`raidersco` _Raider_ (Light Cavalry, HP=280)<br>`swordsmansco` _Sword Clansman_ (Light Infantry, HP=180)<br>`archersco` _Bow Clansman_ (Archer, HP=150)<br>`officersco` _Officer_ (Light Infantry, HP=150)<br>`pikemansco` _Covenanter pikeman_ (Light Infantry, HP=100)<br>`musketeersco` _Covenanter musketeer_ (Shooter, HP=90)<br>`peasco` _Peasant_ (Peasant, HP=60) |
| **spa** | `pikemanspa` _Coselete_ (Light Infantry, HP=100)<br>`musketeerspa` _Musketeer, 17th century_ (Shooter, HP=85) |
| **swe** | `reiterswe` _Swedish Reiter_ (Heavy Cavalry, HP=300)<br>`hackapell` _Hakkapeliitta_ (Light Cavalry, HP=245)<br>`pikeman18swe` _Pikeman, 18th century_ (Light Infantry, HP=110) |
| **swi** | `hussarswi` _Mounted Jaeger_ (Light Cavalry, HP=265)<br>`pikemanswi` _Pikeman, 17th century_ (Light Infantry, HP=90)<br>`jagerswi` _Jaeger_ (Shooter, HP=65) |
| **tur** | `yachttur` _Yacht_ (Yacht, HP=31000)<br>`sipahi` _Heavy Sipahi_ (Heavy Cavalry, HP=360)<br>`spakh` _Light Sipahi_ (Heavy Cavalry, HP=230)<br>`tatar` _Tatar_ (Archer, HP=185)<br>`archertur` _Turkish archer_ (Archer, HP=65)<br>`jannisary` _Janissary_ (Shooter, HP=65) |
| **ukr** | `chaika` _chaika_ (Yacht, HP=25000)<br>`hetman` _Hetman_ (Heavy Cavalry, HP=320)<br>`cossackregister` _Register Cossack_ (Heavy Cavalry, HP=250)<br>`cossacksich` _Sich Cossack_ (Light Cavalry, HP=250)<br>`serdiuk` _Serdiuk_ (Shooter, HP=85)<br>`peaukr` _Peasant_ (Peasant, HP=75) |

**Без уникальных не-наёмных юнитов:** ven — используют только общий ростер.

## §4. Стат-аномалии на «одинаковых» юнитах

Один и тот же `usage_short` у разных наций может иметь разные HP / damage / armor — это и есть скрытые балансовые отличия. Здесь — категории, где разброс HP между нациями ≥ 20%.

| Usage | Min HP (nation · sid) | Max HP (nation · sid) | Spread |
| --- | --- | --- | ---: |
| Archer | alg · `archer` (40) | tur · `tatar` (185) | +362% |
| Light Infantry | alg · `drummertur` (50) | sco · `swordsmansco` (180) | +260% |
| Cannon | sco · `framegun` (3000) | ven · `cannon` (9000) | +200% |
| Shooter | por · `jagerpor` (50) | eng · `highlander` (130) | +160% |
| Mounted Shooter | fra · `dragoon18fra` (140) | net · `dragoon18net` (320) | +129% |
| Heavy Cavalry | pol · `reiterpol` (190) | rus · `vityaz` (380) | +100% |
| Frigate | aus · `frigate` (50000) | tur · `xebec` (65000) | +30% |
| Grenadier | sax · `grenadiersax` (100) | pru · `grenadierpru` (125) | +25% |
| Light Cavalry | pol · `wingedhussar` (225) | sco · `raidersco` (280) | +24% |
| Yacht | ukr · `chaika` (25000) | ven · `yacht` (31000) | +24% |

## §5. Доступные наёмники (через дипломатический центр)

Юниты, обучаемые в `<nat>dip` (Дипломатический центр). Большинство из них имеет суффикс `dip` в `sid`. Платежи в gold, тренируются как обычные юниты, но не зависят от барачных prereq'ов. Юниты с явным флагом `bmercenary=True` (только `battleship` в текущем балансе) дополнительно потребляют gold-upkeep и при `gold=0` подвержены Rebellion (см. [`reference/01_economy.md`](../reference/01_economy.md#famine-голод-и-rebellion-восстание)).

| Sid | Usage | HP | max dmg | bmerc? | nations |
| --- | --- | ---: | ---: | :---: | --- |
| `archerdip` | Archer | 20 | 100 | ✅ | all |
| `archerturdip` | Archer | 20 | 100 | ✅ | all |
| `grenadierdip` | Grenadier | 30 | 200 | ✅ | all |
| `cossacksichdip` | Light Cavalry | 150 | 8 | ✅ | all |
| `lightinfantrydip` | Light Infantry | 50 | 16 | ✅ | all |
| `roundshierdip` | Light Infantry | 75 | 6 | ✅ | all |
| `dragoon18dip` | Shooter | 100 | 18 | ✅ | all |
| `lightcavalrydip` | Shooter | 100 | 18 | ✅ | all |

## §6. Вариант рынка

`mar` — общее здание (см. [03_buildings.md → mar](../reference/03_buildings.md#mar--market)). У наций — 4 разных вариантов здания (`eurmar`/`rusmar`/`spamar`/`turmar`), отличающихся HP, ценой и временем постройки. Это **только варианты здания** — курсы рынка глобальные и одни и те же для всех игроков в матче, независимо от того, какой `mar` они построили (см. [06_market.md](../reference/06_market.md#курсы--глобальные-их-видят-все-игроки)).

| Cluster | Nations |
| --- | --- |
| `eurmar` | aus, bav, den, eng, fra, hun, net, pie, pol, pru, sax, sco, swe, swi, ven |
| `rusmar` | rus, ukr |
| `spamar` | por, spa |
| `turmar` | alg, tur |

---

Перегенерация: `python compute/compute_nations_overview.py`