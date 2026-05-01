# Формат сетевых пакетов C3 (через анализ скриптовых вызовов)

Bit-layout пакетов синхронизации, восстановленный **без декомпиляции
exe** — только через анализ вызовов нативного API в скриптах
`data/scripts/lib/`.

> Сопровождает [`server_sync_architecture.md`](server_sync_architecture.md)
> (общая модель) и [`native_api.md`](native_api.md) (полный список
> сериализационных примитивов в exe).

## 1. Двойная система сериализации

В C3 живут **две различные системы записи состояния**, использующие
разные нативные API:

| Система | API | Формат | Где используется |
|---|---|---|---|
| **Бинарь** | `RecordCustomWrite{Bit, Byte, Word, Int24, Integer, Float, PackedFloat, ShortString, String}` | bit-packed binary stream | Real-time sync экономики, малые delta-пакеты в multiplayer. |
| **Parser-текст** | `ParserSet{Int, Float, Bool, String}ValueByKeyByHandle` | плоский key=value текст в `.parser`-формате | Unit/squad state snapshots, save-файлы, отладочный sync. |

Это видно по факту: в скриптах `RecordCustomWrite*` вызывается **15
раз** (в `lib/miscext2.script`, в основном **закомментированно** —
старый код), а реально активные вызовы — только в
`lib/classes.script` для экономики. Большая часть unit-синхронизации
(29 ParserSet-вызовов в `AddUnitInfoToParser`) использует
parser-формат.

### Почему так

Бинарь даёт компактность (1–18 байт на пакет), parser-формат —
гибкость и debug-friendly (можно открыть пакет в текстовом редакторе).
C3 выбирает формат по критерию «как часто шлётся»: то, что идёт
**каждый game-tick** — бинарь; то, что шлётся **по событию** или для
save — parser-текст.

## 2. Бинарный пакет: `EconomyPackage`

Самый горячий sync-пакет в C3 — синхронизация экономических
показателей игрока. Источник:
`data/scripts/lib/classes.script` → `TLanSyncPlayerData.WriteEconomyPackage`.

### 2.1. Структура

Полный bit-layout (read top-to-bottom):

```
struct EconomyPackage {
    Byte   economyfieldstosync;   // битовая маска: какие поля
                                  // изменились с прошлого тика
    if (economyfieldstosync > 0) {
        Byte plind;               // индекс игрока (0..11)
        if (mask bit 0) Word idlepeasants;     // незанятые крестьяне
        if (mask bit 1) Word idlemines;        // пустые шахты
        if (mask bit 2) Word workers_food;     // на еде
        if (mask bit 3) Word workers_wood;     // на дереве
        if (mask bit 4) Word workers_stone;    // на камне
        if (mask bit 5) Word workers_gold;     // на золоте
        if (mask bit 6) Word workers_iron;     // на железе
        if (mask bit 7) Word workers_coal;     // на угле
    }
};
```

### 2.2. Размеры

| Сценарий | Размер пакета |
|---|---:|
| Никаких изменений | 1 байт (только маска `0x00`) |
| Поменялся 1 показатель | 1 + 1 + 2 = **4 байта** |
| Все 8 экономических полей | 1 + 1 + 8×2 = **18 байт** |

### 2.3. Воспроизведение

```pascal
// classes.script:
type TLanSyncPlayerData = class
    plind : Byte;
    idlepeasants : Word;
    idlemines : Word;
    workersonres : array [0..gc_ResCount-1] of Word;

    procedure WriteEconomyPackage(economyfieldstosync : Word);
    begin
        RecordCustomWriteByte(economyfieldstosync);
        if (economyfieldstosync > 0) then
        begin
            RecordCustomWriteByte(plind);
            if ((economyfieldstosync and (1 shl 0)) <> 0) then
                RecordCustomWriteWord(idlepeasants);
            // ... остальные 7 полей с похожей маской
        end;
    end;
end;
```

### 2.4. Полный пакет

В скриптах есть и охватывающий тип:

```pascal
type TLanSyncData = class
    playerstosync : Word;                                    // битмаска: какие игроки в пакете
    economyfieldstosync : array [0..11] of Byte;             // ... и какие поля у каждого
    netplayer : array [0..11] of TLanSyncPlayerData;
end;
```

То есть полный economy-snapshot = `Word`-маска игроков + 12 пакетов
`EconomyPackage`. Максимум — 2 + 12 × 18 = **218 байт** на 12-player
карту (всё со всем). Реально изменения редки, и пакет обычно
весит 5–30 байт.

## 3. Parser-формат: unit state snapshots

Источник: `data/scripts/lib/miscext2.script` →
`AddUnitInfoToParser(pSync, syncuid : Integer)`. Поля юнита
записываются как `key=value` в parser-handle:

### 3.1. Список полей (29 штук)

Группа | Ключ | Тип | Что |
|---|---|---|---|
| **identity** | `syncuid` | int | sync-UID юнита (стабильный) |
| | `bexists` | bool | жив или удалён |
| | `racename` | string | nation sid (`aus`, `fra`, ...) |
| | `basename` | string | unit sid (`musket18`, `cen`, ...) |
| | `cid` | int | country id (0..23) |
| | `id` | int | внутренний id |
| | `pl` | int | player handle |
| **position** | `posx`, `posz` | float | координаты на карте (тайлы) |
| | `scale` | float | масштаб модели |
| | `upx`, `upy`, `upz` | float | up-вектор (для ориентации) |
| | `dirx`, `diry`, `dirz` | float | direction-вектор |
| **state** | `statestag` | int | битовая маска FSM-состояния (см. `gc_statetag_*`) |
| | `sto` | int | sub-tick offset |
| | `stpx`, `stpz`, `sta` | float | start-position и start-angle (для лерпа) |
| **health** | `hp` | int | текущее HP |
| | `bbuilt` | bool | здание достроено (`True`) или строится |
| | `bdead` | bool | мёртв |
| | `buildprogress` | float | прогресс постройки |
| **rng** | `uniqrnd` | float | per-unit random seed `[0,1)` (для воспроизводимости хедшотов) |

(поле `angle` присутствует в коде, но **закомментированно** — то есть
угол не синхронизуется через этот канал.)

### 3.2. Формат на проводе

Пакет — это сериализованный parser-handle, который превращается в
плоский текст вида:

```
unit_<syncuid> begin
   syncuid = 12345
   bexists = true
   racename = aus
   basename = peaaus
   posx = 47.5
   posz = 122.3
   scale = 1.0
   upx = 0.0; upy = 1.0; upz = 0.0
   dirx = 0.7; diry = 0.0; dirz = 0.7
   statestag = 0x00000C20
   sto = 95
   hp = 5
   bbuilt = true
   bdead = false
   uniqrnd = 0.4827
end
```

(Точный синтаксис — формат `.parser` в C3, ровно тот же, что в
`dmscript.global` и других конфигах.)

Параллельно функция `LoadUnitInfoFromParser` в том же файле читает
обратно. Парный `Get*ValueByKeyByHandle` позволяет читать любое поле
без знания порядка — поэтому формат толерантен к версиям (новые
поля можно добавлять без поломки совместимости).

### 3.3. Размер

Один юнит ≈ **400–600 байт** в текстовом виде (плюс/минус, зависит
от длин имён). Для 200 юнитов на 4-player карте — ~100 КБ
state-snapshot.

Это **больше**, чем дал бы упакованный бинарь (там же ~80 байт на юнит
с использованием `Int24`+`PackedFloat`+bit-fields), но C3 предпочитает
текст: дельта между тиками маленькая (большинство юнитов не двигаются
каждый тик), а полный snapshot шлётся редко (только при подключении
нового клиента и при ON-DEMAND синке).

## 4. Что мы не нашли в скриптах

API в exe есть, но в скриптах **не вызывается**:

- `RecordCustomBeginGUI` / `RecordCustomBeginMap` /
  `RecordCustomBeginStateMachine` / `RecordCustomBeginTagObject` —
  ни одного вызова. Эти функции остались на стороне engine и
  используются движком напрямую для других каналов синка
  (например, GUI-state, FSM, map updates).
- `RecordSynch*` (40+ функций) — **полностью** не вызывается из
  скриптов. Это значит «delta-mark и stack-based sync» — это
  чисто внутренний механизм движка. На проводе мы видим только
  `RecordCustom*`-сериализованные результаты.
- `RecordCustomReadBit` / `RecordCustomBeginReadBitFields` /
  `RecordCustomReadInt24` / `RecordCustomReadPackedFloat` — есть в
  exe, но скрипты их не зовут. Опять же, движок может декодировать
  пакеты и без скрипта (если структура зашита).

## 5. Что это меняет в существующем `server_sync_architecture.md`

Документ
[`server_sync_architecture.md`](server_sync_architecture.md) описывал
паттерн `bProcess` как абстракцию, без указания конкретного формата.
Теперь мы знаем:

| `bProcess`-поток | Реальная реализация |
|---|---|
| Per-event mod-53 sync параметров юнита | Parser-формат, `AddUnitInfoToParser` (см. §3) |
| Periodic real-time sync экономики | Бинарный `EconomyPackage` (см. §2) |
| On-demand full state | Parser-снапшот всех юнитов (большой) |

Net I/O (сама отправка по сети) — Indy 10, недоступно скриптам.
Скрипты только подготавливают **payload** в одном из двух форматов.

## 6. Воспроизведение результатов

Все эти данные получены статически. Чтобы повторить:

```powershell
# Какие нативные функции синхронизации вообще доступны
python -c "import json; d=json.load(open('derived/dws_native_signatures.json',encoding='utf-8')); print('\n'.join(s['raw'] for s in d['signatures'] if 'record' in s['name'].lower() or 'serial' in s['name'].lower()))"

# Где и как они вызываются скриптами
grep -rn -E 'RecordCustom|ParserSet.*ValueByKey' "C:\Program Files (x86)\Steam\steamapps\common\Cossacks 3\data\scripts"
```

## 7. Что осталось закопанным

1. **Точная семантика `Word playerstosync`** — порядок битов: bit 0
   = player 0, или bit 0 = первый "имеется в пакете"? Без сниффа
   оригинального трафика не разрешить однозначно.
2. **Compression**. Возможно, движок сжимает текстовый
   parser-payload zlib'ом перед отправкой. В нативном API есть
   `ECompressionError` (Pascal class в exe) — намекает на zlib/gzip.
3. **MAC / signing**. Способ защиты от нечестных клиентов в exe
   точно есть (Steam-auth + Indy SSL?), но через скрипты не виден.
