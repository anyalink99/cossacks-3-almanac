# Native primitives in cossacks.exe — DWS signatures (подробный список)

> **Аналитика и архитектурные выводы — в [native_api.md](native_api.md).**
> Здесь — машинно-генерируемая таблица для быстрого поиска примитивов.

Извлечено напрямую из `cossacks.exe`: каждый нативный DWS-примитив зарегистрирован как Delphi AnsiString вида `function NAME(args): ReturnType`. Скрипт ниже сканирует exe по сигнатуре заголовка AnsiString (`refcount=-1, length, chars, NUL`) и извлекает 100% этих строк.

**Всего сигнатур в exe:** 4856.  
**Из них вызывается из DMscript:** 884 (100.0% от 884 нативных вызовов в скриптах).  
**Только в exe (не используются скриптом):** 3972 — это либо мёртвые/legacy-примитивы, либо API для редактора/AI, либо примитивы, которые скрипт зовёт через class.method-синтаксис (не пойманный нашим извлекателем).

## Подсистемы (грубая классификация по префиксу)

| Подсистема | Сигнатур |
|---|---:|
| misc | 3675 |
| game_object | 715 |
| player | 185 |
| scripting | 85 |
| save_load | 38 |
| sound | 34 |
| behaviour_props | 28 |
| spawn | 25 |
| ui | 19 |
| path_command | 15 |
| geometry | 11 |
| ai | 10 |
| locale | 9 |
| rng | 5 |
| search | 2 |

## Топ-50 матчей (по числу вызовов из скриптов)

| Имя | Сигнатура | Возвращает | Calls | Файлов |
|---|---|---|---:|---:|
| `ErrorLog` | `(const msg: String)` | `—` | 387 | 56 |
| `GetPlayerHandleByIndex` | `(playerindex: Integer)` | `Integer` | 270 | 43 |
| `GetGameObjectPositionZByHandle` | `(gohandle: Integer)` | `Float` | 263 | 34 |
| `GetGameObjectPositionXByHandle` | `(gohandle: Integer)` | `Float` | 263 | 34 |
| `Log` | `(const msg: String)` | `—` | 210 | 35 |
| `GetLocaleTableListItemByID` | `(const sid, skey: String)` | `String` | 197 | 6 |
| `SwitchTo` | `(const state: String)` | `—` | 146 | 145 |
| `VectorDistance` | `(x1, y1, z1: Float; x2, y2, z2: Float)` | `Float` | 137 | 24 |
| `SetBehaviourBoolProperty` | `(behaviour: Integer; const name: String; value: Boolean)` | `—` | 127 | 9 |
| `GetPlayerIndexByHandle` | `(plhandle: Integer)` | `Integer` | 120 | 44 |
| `ParserGetFloatValueByKeyByHandle` | `(aparser: Integer; const akey: String)` | `Float` | 115 | 10 |
| `RecordCustomWriteInteger` | `(const value: Integer)` | `Boolean` | 111 | 32 |
| `ReadInteger` | `(const fs: Integer; var val: Integer)` | `—` | 106 | 1 |
| `GetGameObjectUniqueIdByHandle` | `(gohandle: Integer)` | `Integer` | 95 | 47 |
| `GetGameObjectHandleByUniqueId` | `(uniqueid: Integer)` | `Integer` | 94 | 42 |
| `GetPlayerGameObjectsCountByHandle` | `(playerhandle: Integer)` | `Integer` | 89 | 31 |
| `WriteInteger` | `(const fs: Integer; const val: Integer)` | `—` | 87 | 1 |
| `StrExists` | `(const source: String; const substr: String)` | `Boolean` | 86 | 16 |
| `SetBehaviourFloatProperty` | `(behaviour: Integer; const name: String; value: Float)` | `—` | 84 | 9 |
| `GetGUITextureHeight` | `(const libmaterialname: String)` | `Integer` | 83 | 2 |
| `GetGUITextureWidth` | `(const libmaterialname: String)` | `Integer` | 78 | 2 |
| `ParserGetCountByHandle` | `(handle: Integer)` | `Integer` | 78 | 13 |
| `StrReplace` | `(const instr, whatstr, tostr: String)` | `String` | 76 | 10 |
| `MaxFloat` | `(const a, b: Float)` | `Float` | 73 | 12 |
| `VectorRotateY` | `(var x1, y1, z1: Float; angle: Float)` | `—` | 72 | 17 |
| `ParserGetIntValueByKeyByHandle` | `(aparser: Integer; const akey: String)` | `Integer` | 70 | 9 |
| `GetGameObjectStatesTagByHandle` | `(gohandle: Integer)` | `Integer` | 68 | 19 |
| `ParserSelectByHandleByKey` | `(const aparser: Integer; const akey: String)` | `Integer` | 68 | 15 |
| `ParserSetFloatValueByKeyByHandle` | `(aparser: Integer; const akey: String; const avalue: Float)` | `—` | 68 | 5 |
| `GetGameObjectPlayerHandleByHandle` | `(gohandle: Integer)` | `Integer` | 64 | 24 |
| `GetGameObjectHandleByIndex` | `(index: Integer; plhandle: Integer)` | `Integer` | 64 | 18 |
| `SeekInteger` | `(const fs: Integer)` | `—` | 59 | 1 |
| `SubStr` | `(const source: String; aindex, acount: Integer)` | `String` | 56 | 15 |
| `StateMachineGetArgDataByInd` | `(const smhnd, argind: Integer)` | `Pointer` | 56 | 15 |
| `GetMapCollisionTag` | `(x, y : Float; buselayers: Boolean)` | `Integer` | 55 | 16 |
| `GetGUIElementIndexByNameParent` | `(const elementname: String; parent: Integer)` | `Integer` | 50 | 7 |
| `PlayerExecuteStateByHandle` | `(plhandle: Integer; const state: String)` | `—` | 49 | 14 |
| `ParserSelectByHandleByIndex` | `(const aparser: Integer; index: Integer)` | `Integer` | 49 | 13 |
| `ParserGetValueByKeyByHandle` | `(aparser: Integer; const akey: String)` | `String` | 49 | 14 |
| `GetGameObjectSTOHandleByHandle` | `(gohandle: Integer)` | `Integer` | 47 | 15 |
| `ExecuteState` | `(const state: String)` | `—` | 46 | 32 |
| `FreeMem` | `(const p: Pointer)` | `—` | 46 | 4 |
| `SetGUIElementVisibleProperties` | `(index: Integer; const visprop, matname: String; const xoffset, yoffset, textxoffset, textyoffset, cursorind: Integer; const textcolorr, textcolorg, textcolorb, textcolora: Float)` | `—` | 45 | 1 |
| `IsFileExists` | `(const afile: String)` | `Boolean` | 44 | 9 |
| `MoveMem` | `(const source: Pointer; var dest: Pointer; count: Integer)` | `—` | 44 | 1 |
| `SetGameObjectVisibleByHandle` | `(gohandle: Integer; visible: Boolean)` | `—` | 43 | 22 |
| `MapDrawCollision` | `(x, y : Float; tag : Integer; radius : Float; round : Boolean)` | `—` | 43 | 7 |
| `ParserSetIntValueByKeyByHandle` | `(aparser: Integer; const akey: String; const avalue: Integer)` | `—` | 43 | 6 |
| `BoolToStr` | `(val: Boolean)` | `String` | 42 | 20 |
| `GameObjectAddNewChild` | `(const gohandle: integer; const racename: string; const basename: string)` | `Integer` | 42 | 4 |

## Примеры по подсистемам (10 первых из каждой)

### game_object (715)

- `procedure GetGameObjectAbsolutePositionByHandle(const gohnd: Integer; var x: Float; var y: Float; var z: Float)`  *(rva 0x00632364)*
- `procedure GetGameObjectAbsoluteScaleByHandle(const gohnd: Integer; var x: Float; var y: Float; var z: Float)`  *(rva 0x00632440)*
- `procedure GetGameObjectAbsoluteVectorTransformByHandle(gohnd: Integer; var x, y, z: Float)`  *(rva 0x00637a18)*
- `function GetGameObjectActiveWallCellHandleByHandle(const gohandle: Integer): Integer`  *(rva 0x0062f0e0)*
- `function GetGameObjectActorIndexByHandle(gohandle: Integer): Integer`  *(rva 0x00643704)*
- `function GetGameObjectAlignmentToFlagmanByHandle(gohandle: Integer): Boolean`  *(rva 0x00644d50)*
- `function GetGameObjectAllChildByCustomNameToArrayByHandle(gohandle: Integer; const scustom: String): Integer`  *(rva 0x0063dc10)*
- `function GetGameObjectAnimationControlerEnabledByHandle(gohandle: Integer): Boolean`  *(rva 0x0063698c)*
- `function GetGameObjectAnimationCycleCountFrameByHandle(const gohandle: Integer; const name: String): Integer`  *(rva 0x0062fc9c)*
- `function GetGameObjectAnimationCycleIndexByName(gohandle: Integer; const animname: String): Integer`  *(rva 0x00642080)*

### player (185)

- `function GetPlayerArmiesCalcNeededByHandle(plhandle: Integer; enemyarmies: Boolean): Boolean`  *(rva 0x006908cc)*
- `function GetPlayerArmiesCountByHandle(plhandle: Integer; enemyarmies: Boolean): Integer`  *(rva 0x0068fa04)*
- `function GetPlayerArmyDirectPathToArmy(plhandle: Integer; armyindex: Integer; toplhandle: Integer; toarmyindex: Integer): Boolean`  *(rva 0x006905fc)*
- `function GetPlayerArmyDirectPathToEnemyArmy(plhandle: Integer; armyindex: Integer; enemyarmyindex: Integer): Boolean`  *(rva 0x00690f6c)*
- `procedure GetPlayerArmyDirectionByHandle(plhandle: Integer; armyindex: Integer; enemyarmy: Boolean; var dirx: Float; var diry: Float)`  *(rva 0x0068fee0)*
- `procedure GetPlayerArmyDirectionToArmyByHandle(plhandle: Integer; armyindex: Integer; toplhandle: Integer; toarmyindex: Integer; var dirx: Float; var diry: Float; var angle: Float)`  *(rva 0x0068fbf4)*
- `procedure GetPlayerArmyDirectionToEnemyArmyByHandle(plhandle: Integer; armyindex: Integer; enemyarmyindex: Integer; var dirx: Float; var diry: Float; var angle: Float)`  *(rva 0x00690ebc)*
- `procedure GetPlayerArmyDirectionToGroupByHandle(plhandle: Integer; armyindex: Integer; togrhandle: Integer; enemyarmy: Boolean; var dirx: Float; var diry: Float; var angle: Float)`  *(rva 0x0068fcb4)*
- `procedure GetPlayerArmyDistAndDirToArmyByHandle(plhandle: Integer; armyindex: Integer; toplhandle: Integer; toarmyindex: Integer; var dist: Float; var dirx: Float; var diry: Float)`  *(rva 0x00690ce4)*
- `procedure GetPlayerArmyDistAndDirToEnemyArmyByHandle(plhandle: Integer; armyindex: Integer; enemyarmyindex: Integer; var dist: Float; var dirx: Float; var diry: Float)`  *(rva 0x00691130)*

### scripting (85)

- `function ParserAddChildByIndex(aparser: Integer; const achild: String): Integer`  *(rva 0x006e9b28)*
- `procedure ParserClearByHandle(const aparser: Integer)`  *(rva 0x006e82e4)*
- `function ParserCopyFromByHandle(const aparser: Integer): Boolean`  *(rva 0x006e8a28)*
- `function ParserCopyFromByKey(const aparser: String): Boolean`  *(rva 0x006e899c)*
- `function ParserCopyToByHandle(const aparser: Integer): Boolean`  *(rva 0x006e8a74)*
- `function ParserCopyToByKey(const aparser: String): Boolean`  *(rva 0x006e89e4)*
- `function ParserCreate(const aparser: String): Integer`  *(rva 0x006e82a4)*
- `function ParserCreateCurrentStateMachine(): Integer`  *(rva 0x006e8560)*
- `function ParserCreateGameObject(const gohandle: Integer): Integer`  *(rva 0x006e859c)*
- `function ParserCreateGroup(const grhandle: Integer): Integer`  *(rva 0x006e85e8)*

### save_load (38)

- `procedure ReadInteger(const fs: Integer; var val: Integer)`  *(rva 0x0060c8bc)*
- `function RecordCustomBegin(const state: String): Boolean`  *(rva 0x0068232c)*
- `function RecordCustomBeginGUI(const state: String): Boolean`  *(rva 0x00682438)*
- `function RecordCustomBeginMap(const state: String): Boolean`  *(rva 0x00682480)*
- `function RecordCustomBeginReadBitFields(): Boolean`  *(rva 0x00682900)*
- `function RecordCustomBeginStateMachine(const smhnd: Integer; const state: String): Boolean`  *(rva 0x006823d4)*
- `function RecordCustomBeginTagObject(const taghnd: Integer; const state: String): Boolean`  *(rva 0x00682370)*
- `procedure RecordCustomEnd()`  *(rva 0x006824c8)*
- `function RecordCustomEndReadBitFields(): Boolean`  *(rva 0x0068296c)*
- `function RecordCustomGetReadPackageSize(): Integer`  *(rva 0x00682c2c)*

### sound (34)

- `procedure PlayCurrentScenarioImmediately()`  *(rva 0x0069fe0c)*
- `function PlayerAddArmyByHandle(plhandle: Integer; enemyarmy: Boolean): integer`  *(rva 0x00690b88)*
- `function PlayerAddGroupToArmyByHandle(plhandle: Integer; armyindex: Integer; enemyarmy: Boolean; grouphandle: integer): integer`  *(rva 0x00690be0)*
- `function PlayerArmyCheckLinePointToPoint(plhandle: Integer; armyindex: Integer; enemyarmy: Boolean; x1,y1, x2,y2: Float): boolean`  *(rva 0x0069155c)*
- `function PlayerArmyCheckLineToEnemyArmy(plhandle: Integer; armyindex: Integer; enemyarmyindex: Integer): boolean`  *(rva 0x00691460)*
- `function PlayerArmyCheckLineToPoint(plhandle: Integer; armyindex: Integer; enemyarmy: Boolean; x,y: Float): boolean`  *(rva 0x006914dc)*
- `function PlayerArmyGroupSideLeftRight(plhandle: Integer; armyindex: Integer; enemyarmy: Boolean; groupindex: integer): integer`  *(rva 0x006916f8)*
- `procedure PlayerArmySetNameByHandle(plhandle: Integer; armyindex: Integer; enemyarmy: Boolean; name: string)`  *(rva 0x00690c6c)*
- `function PlayerArmyTestLineToEnemyArmy(plhandle: Integer; armyindex: Integer; enemyarmyindex: Integer; var resx, resy: Float): boolean`  *(rva 0x006915e8)*
- `function PlayerArmyTestLineToPoint(plhandle: Integer; armyindex: Integer; x, y: Float; var resx, resy: Float): boolean`  *(rva 0x00691678)*

### behaviour_props (28)

- `procedure GetBehaviourAffineVectorProperty(behaviour: Integer; const name: String; var x, y, z: Float)`  *(rva 0x006daa20)*
- `function GetBehaviourBaseObject(behaviour: Integer): Integer`  *(rva 0x006da300)*
- `function GetBehaviourBoolProperty(behaviour: Integer; const name: String): Boolean`  *(rva 0x006da840)*
- `function GetBehaviourByClassName(gohnd: Integer; const classname: String): Integer`  *(rva 0x006d97a8)*
- `function GetBehaviourByIndex(gohnd: Integer; const index: Integer): Integer`  *(rva 0x006d9854)*
- `function GetBehaviourByKey(gohnd: Integer; const key: String): Integer`  *(rva 0x006d9804)*
- `function GetBehaviourClassName(behaviour: Integer): String`  *(rva 0x006da238)*
- `function GetBehaviourCount(gohnd: Integer): Integer`  *(rva 0x006d98ac)*
- `function GetBehaviourFloatProperty(behaviour: Integer; const name: String): Float`  *(rva 0x006da8f8)*
- `function GetBehaviourIndex(behaviour: Integer): Integer`  *(rva 0x006da1b4)*

### spawn (25)

- `function CreateAIRegion(const name: String): Integer`  *(rva 0x006a0eb8)*
- `function CreateBitmap(): Integer`  *(rva 0x0060cb90)*
- `function CreateBitmapTGA(): Integer`  *(rva 0x0060cbb8)*
- `function CreateFunction(const funcargsdesc: string; const addr: pointer): boolean`  *(rva 0x0060d5b8)*
- `function CreateGUIMiniMapPrimitive(const name: String): Integer`  *(rva 0x0066b684)*
- `function CreateGroup(const playername: String; const groupname: String): Integer`  *(rva 0x006591a0)*
- `function CreateGroupByPlHandle(const playerhandle: Integer; const groupname: String): Integer`  *(rva 0x006591fc)*
- `function CreatePlayer(const playername, racename, controlmode: String): Integer`  *(rva 0x0068da8c)*
- `function CreatePlayerFirst(const playername, racename, controlmode: String): Integer`  *(rva 0x0068dae8)*
- `function CreatePlayerGameObject(const playername: String; const racename: String; const basename: String; positionx: Float; positiony: Float; positionz: Float): String`  *(rva 0x0068d730)*

### ui (19)

- `function FormatColorTagCount(const val: String): Integer`  *(rva 0x0067331c)*
- `function FormatColorToHex3(c0, c1, c2: Float): String`  *(rva 0x006733f4)*
- `function FormatColorToHex4(c0, c1, c2, c3: Float): String`  *(rva 0x00673434)*
- `procedure FormatGetGUIElementTextPosData(index, pos: Integer; var x, y: Integer; var style: String; var r, g, b, a: Float)`  *(rva 0x00672e9c)*
- `function FormatGetGUIElementTextRefData(index, refind: Integer; var refpos: Integer; var refarg, refval: String; var x, y: Integer; var style: String; var r, g, b, a: Float): Boolean`  *(rva 0x00672fe4)*
- `function FormatGetGUIElementTextTagData(index, tagind: Integer; var tag: String; var tagpos, taglen: Integer; var tagarg: String; var x, y: Integer; var style: String; var r, g, b, a: Float): Boolean`  *(rva 0x0067313c)*
- `function FormatGetJustTextWithoutTags(const val: String; tag: String): String`  *(rva 0x00673360)*
- `procedure FormatHexToColor3(hex: String; var c0, c1, c2: Float)`  *(rva 0x00673478)*
- `procedure FormatHexToColor4(hex: String; var c0, c1, c2, c3: Float)`  *(rva 0x006734c0)*
- `function FormatIsHexString(hex: String): Boolean`  *(rva 0x006733b8)*

### path_command (15)

- `procedure MoveFileStream(const srcfilename, dstfilename: String)`  *(rva 0x0060c1a8)*
- `procedure MoveMem(const source: Pointer; var dest: Pointer; count: Integer)`  *(rva 0x006c17f8)*
- `function PathDataThreadCount(): Integer`  *(rva 0x00689358)*
- `procedure PathDataThreadDeltaPriority(const val : Integer)`  *(rva 0x0068917c)*
- `procedure PathDataThreadDynamicPriority(const val : Boolean)`  *(rva 0x006891c0)*
- `procedure PathDataThreadMaxPriority(const val : Integer)`  *(rva 0x00689290)*
- `procedure PathDataThreadMinPriority(const val : Integer)`  *(rva 0x0068924c)*
- `procedure PathDataThreadResume()`  *(rva 0x006890cc)*
- `procedure PathDataThreadSafeClean()`  *(rva 0x00689150)*
- `procedure PathDataThreadSleepLength(const val : Integer)`  *(rva 0x006892d4)*

### geometry (11)

- `function VectorAngle(x1, y1, z1: Float; x2, y2, z2: Float): Float`  *(rva 0x0060aa98)*
- `procedure VectorCross(x1, y1, z1: Float; x2, y2, z2: Float; var rx, ry, rz: Float)`  *(rva 0x0060ab30)*
- `function VectorDistance(x1, y1, z1: Float; x2, y2, z2: Float): Float`  *(rva 0x0060ab8c)*
- `function VectorDot(x1, y1, z1: Float; x2, y2, z2: Float): Float`  *(rva 0x0060aae4)*
- `function VectorLength(x1, y1, z1: Float): Float`  *(rva 0x0060abdc)*
- `procedure VectorNormalize(var x, y, z: Float)`  *(rva 0x0060ad54)*
- `procedure VectorReflect(var vx, vy, vz: Float; nx, ny, nz: Float)`  *(rva 0x0060ad8c)*
- `procedure VectorRotateAxis(var x, y, z: Float; axisx, axisy, axisz: Float; angle: Float)`  *(rva 0x0060acf0)*
- `procedure VectorRotateX(var x1, y1, z1: Float; angle: Float)`  *(rva 0x0060ac18)*
- `procedure VectorRotateY(var x1, y1, z1: Float; angle: Float)`  *(rva 0x0060ac60)*

### ai (10)

- `procedure AIRegionDoClearObjects(const name: String)`  *(rva 0x0069d790)*
- `procedure AIRegionDoClearObjectsByHandle(const reghnd: Integer)`  *(rva 0x006a1240)*
- `function AIRegionDoScanObjects(const name: String): Integer`  *(rva 0x0069d748)*
- `function AIRegionDoScanObjectsByHandle(const reghnd: Integer): Integer`  *(rva 0x006a111c)*
- `function AIRegionDoScanObjectsExtByHandle(const reghnd: Integer; const clear, notify: boolean): Integer`  *(rva 0x006a116c)*
- `procedure AIRegionDoUpdateObject(const reghnd, gohnd: Integer; const notify: boolean)`  *(rva 0x006a11e0)*
- `procedure AIRegionFromParserStruct(const parser: Integer)`  *(rva 0x006a1510)*
- `procedure AIRegionLoadFromTextFile(const filename: String)`  *(rva 0x006a14cc)*
- `procedure AIRegionSaveToTextFile(const filename: String)`  *(rva 0x006a1488)*
- `procedure AIRegionToParserStruct(const parser: Integer)`  *(rva 0x006a1554)*

### locale (9)

- `function GetLocaleTableFileName(): String`  *(rva 0x006a0580)*
- `function GetLocaleTableItem(const skey: String): String`  *(rva 0x006a0668)*
- `function GetLocaleTableListFileName(): String`  *(rva 0x006a05f0)*
- `function GetLocaleTableListItemByID(const sid, skey: String): String`  *(rva 0x006a070c)*
- `function GetLocaleTableListItemByIndex(const ind: Integer; const skey: String): String`  *(rva 0x006a06ac)*
- `function GetLocaleTableListUseTags(): Boolean`  *(rva 0x006a075c)*
- `procedure SetLocaleTableFileName(const val: String)`  *(rva 0x006a05b4)*
- `procedure SetLocaleTableListFileName(const val: String)`  *(rva 0x006a0628)*
- `procedure SetLocaleTableListUseTags(const val: Boolean)`  *(rva 0x006a0794)*

### rng (5)

- `function Random(): Float`  *(rva 0x0060af24)*
- `function RandomExt(): Float`  *(rva 0x0060a658)*
- `procedure RandomHeightTerrain(const x, y: Integer; const round: Boolean; const mb: Integer; const delta: Float)`  *(rva 0x006a3b68)*
- `procedure SetRandomExtKey64(const key0, key1: Integer)`  *(rva 0x0060a724)*
- `procedure SetRandomKey(key: Integer)`  *(rva 0x0060a6a8)*

### search (2)

- `function FindGameObjectByUniqId(const id: Integer): Integer`  *(rva 0x006a3efc)*
- `function FindUniqIdByGameObject(const gohnd: Integer): Integer`  *(rva 0x006a3eb4)*

## Где данные

- `docs/derived/dws_native_signatures.json` — полный машинно-читаемый список всех сигнатур.
- `docs/derived/engine_primitives.json` — нативные примитивы со стороны скрипта (970 имён + частоты).
- Генератор: `parser/engine_recon/extract_dws_signatures.py`.

## Как использовать дальше

1. **Поиск алгоритма примитива:** взять `rva` из JSON, открыть exe в Ghidra/IDA по этому адресу — рядом будет указатель на нативную функцию-обёртку (DWS callback). Декомпиляция показывает реальный алгоритм (например, BFS vs k-d tree для `findnearestresource`).
2. **Карта подсистем:** имена `Get*ByHandle/Set*ByHandle` выявляют ECS-style API движка. `RecordCustom*` — формат сейва. `SwitchTo` — корневой scheduler-примитив (146 файлов = почти весь скриптовый код).
3. **Документация без RE:** сигнатуры уже включают имена аргументов и типы — это де-факто публичный API DWS-движка C3.