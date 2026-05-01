# Карта Delphi-классов движка (RTTI)

Структурированный обзор подсистем `cossacks.exe` через имена
классов, найденные в RTTI.

> **Откуда данные.** В Pascal ShortString-таблице `cossacks.exe`
> мы извлекли **1 779 имён Delphi-классов** (`T*` / `E*` / `I*` / `F*`).
> Из них около 266 — game-engine классы (префиксы `TX` и `TOSW`),
> остальные — стандартный Delphi VCL, Indy 10, FastMM4 и
> JPEG / DDS / OpenGL обвязка. Полный дамп — в
> [`../../derived/exe_strings.json`](../../derived/exe_strings.json),
> поле `delphi_class_names`. Извлекатель —
> [`../../parser/engine_recon/dump_exe_strings.py`](../../parser/engine_recon/dump_exe_strings.py).

## Ключевые префиксы

| Префикс | Кол-во | Что это |
|---|---:|---|
| `TX*` | 576 | Game engine: GameObject, AIRegion, Pattern, StateMachine, Path, Map, Scenario, Trigger, Lan и т. д. Классы, специфичные для движка Cossacks 3. |
| `TOSW*` | 263 | OpenSourceWorld engine — рендер, звук, частицы, атмосфера. Унаследовано от GLScene-подобной базы. |
| `EId*` | ~50 | Indy 10 — сетевой стек (Internet Direct). |
| `T*` стандартные Delphi | ~700 | VCL: TForm, TButton, TStringList, TBitmap, TPersistent и т. д. |
| `EAb*`, `EAccess*`, `EConvert*`, `EOut*` | ~150 | Стандартные исключения Delphi. |
| `TXAIX*` | 4 | Редактор `.aix`-формата (см. §10). |
| `T*OSW*Mod*` | 3 | Mod loader. |

## 1. Игровые объекты (`TXGameObject*`)

Корневой класс всех «штук на карте» — `TXGameObject`.

| Класс | Назначение |
|---|---|
| `TXGameObject` | Базовая единица — юнит, здание, ресурс, эффект. |
| `TXBrushGameObject` | Объекты-«кисти» (декорации, статичные элементы карты). |
| `TXEventGameObject` | Триггерные точки, спавнеры. |
| `TXGameObjectsGrid` | Spatial grid из всех объектов на карте. |
| `TXGridGameObjectMap` | Карта типа сетки → handle. |
| `TXPickedGameObjects` | Текущая выделенная группа (UI-state). |

Все 715 функций ECS-API (`Get*ByHandle` / `Set*ByHandle` — см.
[`native_api.md` §2.1](native_api.md)) работают с `TXGameObject`.

## 2. Behaviour-компоненты (`TXBehaviour*`, ~22 класса)

ECS-стиль: каждый GameObject может нести несколько Behaviour-объектов.

| Класс | Что делает |
|---|---|
| `TXBaseBehaviour`, `TXBehaviour`, `TXBehaviours` | Базовые / контейнер. |
| `TOSWBaseBehaviour`, `TOSWBehaviour`, `TOSWBehaviours` | Аналогичные на уровне OSW (рендер). |
| `TXConditionMachineBehaviour` | Поведение «по условиям» (FSM-подобное). |
| `TXDelayDestroyBehaviour`, `TXDelayDestroyListBehaviour` | Отложенное удаление. |
| `TXMiniMapPrimitiveBehaviour` | Отрисовка точки на миникарте. |
| `TXPhysicalFallBehaviour` | Падение под действием гравитации (труп после смерти). |
| `TXRollBehaviour`, `TXRotationBehaviour`, `TXTiltBehaviour`, `TXTurnObjectBehaviour` | Вращение / наклон. |
| `TXThrowBehaviour`, `TXThrowUpBehaviour` | Подбрасывание (граната, тело). |
| `TXMoveRotateWaveBehaviour` | Маятниковое движение. |
| `TXPoolBehaviour` | Объект из пула (для pooled-allocation). |
| `TXProgressChildrenBehaviour`, `TXProgressStateMachineBehaviour` | FSM-progress «дочерних» объектов. |
| `TXRayCastBehaviour`, `TXRayCastBehaviourAxis`, `TXRayCastBehaviourWheel` | Raycast (контакт с поверхностью / колесо повозки). |
| `TXTLFAnimationBehaviour`, `TXTLFAnimationChildrenBehaviour` | Top-Level Frame анимация. |
| `TXDecalChildrenBehaviour`, `TXDecalTransformBehaviour` | Декали (следы, кровь, тень). |

Создаются через нативный `BehaviourCreate(gohnd, classname)` — см.
[`native_api.md` §2.5](native_api.md). Имя в `BehaviourCreate` — это
строковое имя класса (одно из перечисленных).

## 3. AI-регионы (`TXAIRegion*`, 5 классов)

Spatial-механика ИИ. Каждая зона интереса — отдельный объект.

| Класс | Что |
|---|---|
| `TXAIRegion` | Один регион. |
| `TXAIRegions` | Коллекция регионов. |
| `TXAIRegionManager` | Создаёт, обновляет, удаляет регионы. |
| `TXAIRegionScanMode` | Enum режимов сканирования (`scan` / `clear` / `update`). |
| `TXAIRegionViewer` | Визуализатор для редактора (раскраска зон в editor). |

Коды-обёртки скриптов — см. [`native_api.md` §2.6](native_api.md).
Этих 5 классов достаточно, чтобы построить spatial AI: ИИ
запрашивает у `TXAIRegionManager` обновление зоны интересов,
получает list объектов в ней и решает атаковать / отступить.

## 4. Pathfinding (`TXPath*`, `TOSWPath*`, `TPathData`, 6 классов)

Раскрывает то, что было «открыто» в `native_api.md §6.2`:

| Класс | Что |
|---|---|
| `TPathData` | Данные пути одного юнита (waypoints, текущий сегмент). |
| `TOSWMovementPath` | Один путь как последовательность ноду. |
| `TOSWMovementPaths` | Коллекция активных путей. |
| `TOSWPathNode` | Узел пути (точка с координатами + связи с соседями). |
| `TOSWPathNodes` | Граф нод. |
| `TXPathCellChangedArray` | Массив «изменившихся ячеек», для инвалидации кэша. |

**Вывод:** pathfinding в C3 использует **graph-based**
representation (узлы + связи) поверх grid'а, не чисто A* по grid'у.
Узлы (`TOSWPathNode`) живут в `TOSWPathNodes`-графе. Когда ячейка
карты меняется (стройка / снос здания), `TXPathCellChangedArray`
помечает её для пересчёта.

Управляется асинхронно через `PathDataThread*` (14 функций, см.
[`native_api.md` §2.3](native_api.md)) — отдельный thread pool с
приоритетами.

## 5. Топология (`TXTopology`, 1 класс)

В скриптах есть нативный примитив `TopologyGetPath` (упоминается в
[`docs/recon/world/combat/pathfinding.md`](../../docs/recon/world/combat/pathfinding.md)).
Класс `TXTopology` — это объект, инкапсулирующий проходимость карты
(коллизии, water-region, вода-суша). Он используется
pathfinding-движком для поиска от точки А до точки Б по нодам.

## 6. Сценарии и триггеры (`TXScenario*`, `TXTrigger*`, 8 классов)

Движковая основа сценарной системы (см. также recon-обзор:
[`scenarios_and_triggers.md`](../../docs/recon/systems/scenarios_and_triggers.md)).

| Класс | Что |
|---|---|
| `TXScenario` | Один сценарий (Historical Battle / миссия кампании). |
| `TXScenarioList` | Коллекция сценариев. |
| `TXTrigger` | Один триггер (условие → действие). |
| `TXTriggerEvent`, `TXTriggerEvents` | Событие, на которое срабатывает триггер. |
| `TXTriggerEventMode` | Режим обработки события (single-shot / repeating). |
| `TXTriggerEventType` | Тип события (UnitDied / ResourceReached / TimeElapsed / …). |
| `TXTriggerManager` | Управляет всеми активными триггерами. |

Это движковая часть. Скриптовая обёртка — `gScenario` и
`lib/scenario.script` (см.
[`internals/scripts/structure.md` §5](../scripts/structure.md)).

## 7. State Machines (`TXStateMachine*`, 9 классов)

| Класс | Что |
|---|---|
| `TXStateMachine` | Один FSM-экземпляр. |
| `TXStateMachineArgs` | Аргументы текущего состояния. |
| `TXStateMachineLibrary` | Загрузка готовых FSM из `.parser`-файлов. |
| `TXStateMachineProperty` | Свойство состояния. |
| `TXStateMachineStack`, `TXStateMachineStackItem` | Стек состояний (вложенные FSM). |
| `TXStateMachineProgressOption`, `TXStateMachineProgressChildrenOption` | Опции тика (как продолжать прогресс по дочерним FSM). |
| `TFormStateMachines` | Редактор FSM (UI-форма в editor.exe). |

FSM в Cossacks 3 — это и **поведение юнита** (idle → walk → work
→ return → drop), и **логика триггеров сценариев** (см. §6).
Все state-машины загружаются из `.parser`-файлов через
`TXStateMachineLibrary`. Native-API `MachineLibrary*`-функции (см.
[`native_api.md` §2.5](native_api.md)) работают с этим классом.

## 8. Карты и генерация (7 классов)

| Класс | Что |
|---|---|
| `TXMap` | Базовая карта — terrain, объекты, размер. |
| `TXMapGenerator` | Процедурный генератор для skirmish. |
| `TXGlobalMapGenerator` | Кампанийный генератор (для глобальной карты кампании). |
| `TXTileMap`, `TXTileMapSchemesList` | Tile-сетка терреина (cluster по типам). |
| `TXHeightMap` | Высота terrain (heightmap). |
| `TXMiniMap` | Миникарта (рендер в углу UI). |
| `TXGridGameObjectMap` | См. §1. |

`TXMapGenerator` работает с `(randkey0, randkey1)`-парой, что
объясняет 64-bit состояние seed'а (см.
[`rng_implementation.md` §8](rng_implementation.md)).

## 9. Pattern (25 классов)

| Класс | Что |
|---|---|
| `TXPattern`, `TXPatternCollection` | Один шаблон-«штамп» / коллекция. |
| `TXPatternMask` | Маска размещения объектов. |
| `TXPatternObject` | Объект, который ставится по маске. |
| `TXPatternFreq`, `TXPatternFreqs` | Частоты повторения (для рандомизации). |
| `TXPatternCover`, `TXPatternCoverList` | Покрытие участка карты. |
| `TXPatternListCollection`, `TXPatternListItem` | Метаданные списка. |
| `TXBrushPatternPaint`, `TXEventPatternPaint` | Кисти редактора. |
| `TXPatternDecal` | Декали по pattern. |
| `TXPatternWater` | Pattern для воды. |
| `TXPatternLocalZone`, `TXPatternLocalZonesList` | Локальные зоны pattern. |
| `TXBridgePatternFreq`, `TXBridgePatternFreqs` | Pattern мостов. |
| `TXLightPattern`, `TXLightPatternItem`, `TXLightPattern[List|s]` | Pattern освещения. |
| `TXColorPatternsList` | Цветовые pattern. |
| `TXGlobalPatternList` | Глобальный список всех pattern. |
| `TPatternManager` | Главный manager-объект. |

Бинарный формат `.pattern`-файлов разобран в
[`../../parser/parse_patterns.py`](../../parser/parse_patterns.py).
Эти классы — runtime-обёртки.

## 10. Multiplayer / LAN (`TXLan*`, 8 классов)

Раскрывает sin-stack под `RecordSynch*` / `RecordCustom*`-API (см.
[`server_sync_packet_format.md`](server_sync_packet_format.md)):

| Класс | Что |
|---|---|
| `TXLan`, `TXLanManager` | Главный сетевой объект. |
| `TXLanClientInfo`, `TXLanClientInfoBase` | Состояние клиента. |
| `TXLanPublicServer`, `TXLanServerInfoBase` | Публичный сервер lobby. |
| `TXLanPublicServerClient`, `TXLanPublicServerSession` | Соединение с сервером. |

Транспорт — **Indy 10** (`EId*` exception classes в exe).
`TXLan*` — game-side обёртка над Indy.

`TXLanPublicServer` намекает что у Cossacks 3 был свой публичный
matchmaking-сервер (отдельно от Steam). Сейчас это, видимо, работает
через Steam wrapper (видно по `SteamwrapStartVoiceRecording` и
прочим Steamwrap-функциям в native API).

## 11. Mod loader (`TOSWMod*`, 3 класса)

| Класс | Что |
|---|---|
| `TOSWModDat` | Один `.dat`-файл мода. |
| `TOSWModLib`, `TOSWModLibrary` | Библиотека модов (контейнер). |

Используется внешним `modman.exe` (см. также
[`../scripts/structure.md` §1](../scripts/structure.md)).

## 12. Сериализация и сохранение

| Класс | Что |
|---|---|
| `TPersistent`, `TPersistentClass` | Стандартная Delphi-база. |
| Имена с `Custom*Read*` / `Custom*Write*` (через RTTI методов) | Соответствуют native-API `RecordCustom*` (см. [`server_sync_packet_format.md`](server_sync_packet_format.md)). |

## 13. Звук (26 классов)

| Класс | Что |
|---|---|
| `TOSWSoundManager` | Главный звук-объект. |
| `TOSWSoundLibrary` | Библиотека звуков. |
| `TOSWSoundSample`, `TOSWSoundSamples` | Сэмплы. |
| `TOSWSoundEmitter`, `TOSWBSoundEmitter` | Источник звука на карте. |
| `TOSWSoundEmittersList` | Активные источники. |
| `TOSWSoundEnvironment` | Окружение (reverb, эффекты). |
| `TOSWSoundFile`, `TOSWSoundFileFormat`, `TOSWSoundFileFormatsList` | Формат `.ogg` / `.snd`. |
| `TOSWSoundSampling`, `TOSWSoundSource`, `TOSWSoundSourceChange*` | Sampling-rate и динамика. |
| `TOSWSoundVolumeGroup` | Микшер групп. |
| `TXSoundCollection`, `TXSoundInterface`, `TXSoundItem`, `TXSoundLibrary*`, `TXSoundManager`, `TXSoundProperty`, `TXSoundVolume*` | Game-side обёртки. |

## 14. Render (~25 классов) и шейдеры

| Класс | Что |
|---|---|
| `TXShader`, `TXShadowMap` | Шейдер, теневая карта. |
| `TXPHDRToneMapShader` | HDR-tonemap шейдер. |
| `TOSWCadencerMode`, `TOSWCameraInvarianceMode` | Опции движения камеры. |
| `TOSWAtmosphere*`, `TOSWAtmosphereException` | Небо, атмосфера, осадки. |
| Множество `T*` для рендера моделей, FBO, shadow casting. |

Не критично для gameplay — это 3D-стек.

## 15. Партиклы (27 классов)

`TXParticle*`, `TXSourcePFX*` — система частиц (огонь, дым, кровь,
взрывы). Не критично для gameplay-логики, но интересно для
визуального моддинга.

## 16. AIX-формат (`TAIX*`, 4 класса)

| Класс | Что |
|---|---|
| `TAIXEditor` | Редактор `.aix`-файлов. |
| `TAIXEditorState` | Состояние редактора. |
| `TAIXArgsEditor`, `TAIXVarsEditor` | Подмодули (аргументы / переменные). |

То есть редактор `.aix`-формата встроен в `editor.exe`. Это значит:
- `.aix`-формат **бинарный**, но **редактируемый** через UI.
- Структура хранится «полями» (`TAIXVarsEditor` — это про
  переменные, `TAIXArgsEditor` — про аргументы).
- Если когда-то понадобится разбор `.aix`, точка входа — RVA класса
  `TAIXEditorState` в exe (видны имена методов в RTTI).

## 17. UI-формы (25+)

`TForm*` классы — это окна редактора:

| Класс | Что |
|---|---|
| `TFormDWSDebugger` | Отладчик скриптов DWS. |
| `TFormScriptEvaluate` | Окно оценки выражений. |
| `TFormStateMachines` | Редактор FSM. |
| `TFormDbgCtrl` | Debug-контролы. |
| `TFormHelloScreen` | Стартовый экран игры. |
| Прочие `TForm*` | Editor / settings / mod manager UI. |

## Ограничения этого обзора

1. **Не все 1779 классов перечислены** — только подсистемы
   game-engine (`TX*`, `TOSW*`, AIX). Стандартная Delphi VCL и
   Indy 10 не разбираются — они open-source.
2. **Только имена классов** — не методы. Чтобы получить полный
   список published-методов каждого класса, нужно расширить
   `dump_exe_strings.py` walker'ом по VMT (см.
   [`native_api.md` §9](native_api.md)).
3. **Статика, не семантика.** Имя `TXAIRegion` намекает что это
   зона ИИ, но точный набор полей класса — не виден без
   декомпиляции.

Тем не менее имена дают **структурную карту**: понимаешь, какие
сущности живут в движке и в какой подсистеме.

## Воспроизведение

```powershell
cd c:\projects\other\cossacks
python parser\engine_recon\dump_exe_strings.py
# → derived/exe_strings.json (поле delphi_class_names)
```
