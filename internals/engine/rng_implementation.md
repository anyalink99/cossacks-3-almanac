# Реализация RNG в Cossacks 3

Что именно генерирует `random`, `RandomExt` и почему `SetRandomKey`
работает так, как работает.

> Сопровождает [`determinism_audit.md`](determinism_audit.md) (где
> RNG используется в горячем пути добычи и боя) и
> [`native_api.md` §2.4](native_api.md) (полный список четырёх
> RNG-потоков движка).

## 1. Общая картина

В скриптах C3 используются (по убыванию частоты):

| Функция | Вызовов в скриптах | Что |
|---|---:|---|
| `random` | 100 | Float ∈ [0, 1), глобальный поток |
| `RandomExt` | 60 | Float ∈ [0, 1), параллельный «расширенный» поток |
| `SetRandomKey(seed: Integer)` | 4 | Перезасев глобального потока |
| `SetRandomExtKey64(k0, k1)` | 0 | Перезасев расширенного 64-bit потока (в exe есть, скрипты не зовут) |

Каждая из них — **обёртка над стандартным Delphi `Random`/`RandSeed`**,
зарегистрированная DWS-движком. Об этом говорит сам факт, что DWS — это
Delphi-библиотека, а не самостоятельная VM, и она наследует RNG
от хоста.

## 2. Алгоритм Delphi `Random`

`System.Random` в Delphi — линейный конгруэнтный генератор (LCG):

```pascal
RandSeed := RandSeed * $08088405 + 1;
// $08088405 = 134775813
// аддент = 1
// модуль = 2^32 (естественное переполнение Cardinal)
```

Преобразование в float:

```pascal
function Random: Double;
begin
    Result := RandSeed / $FFFFFFFF;
end;
```

Свойства:
- **Период:** 2³² ≈ 4.29 × 10⁹ значений.
- **Семя:** 32-bit `Integer` через `SetRandomKey(seed)`.
- **Один глобальный `RandSeed`** на весь процесс (не per-thread).

Это **широко известная** константа Delphi (та же, что в Borland
Pascal с конца 80-х). Ничего эзотерического.

## 3. Реализация `RandomExt`

`RandomExt` имеет свой `Set/GetRandomExtKey64(k0, k1: Integer)`, то
есть **64-битное состояние** (две `Integer`-секции). Это говорит о
не-LCG генераторе. Кандидаты:

- **Xorshift64** — 64-bit состояние, период ≈ 2⁶⁴, простой код.
- **L'Ecuyer 64** — комбинированный генератор.
- **MT-mini** — неполный Mersenne Twister.

DWS source-tree содержит `dwsXPlatform.pas` и `dwsMathFunctions.pas`,
которые регистрируют расширенные RNG (см. open-source репозиторий
[github.com/EricGrange/DWScript](https://github.com/EricGrange/DWScript)).
Но C3 использует **свою регистрацию** (видно по тому, что в exe есть
`RandomExt` именно как именованный примитив, а в чистом DWS такой нет).
Скорее всего — Xorshift64 (самый частый выбор для расширенного RNG в
Delphi-проектах).

**Практический вывод:** разрядность 64 бит, период 2⁶⁴, **независим**
от глобального `RandSeed`. Используется там, где не должно быть
взаимодействия с gameplay-RNG (см. §5).

## 4. Семантика «глобальный RNG»

Из `determinism_audit.md` мы знали, что `random` — глобальный,
шарится между:

- gameplay-логикой (выбор цели, хедшоты, размещение пеньков),
- UI / GUI-эффектами (`gui.script` зовёт `random` для случайного
  материала combobox'а, например),
- ИИ-решениями.

Это означает: **GUI «крадёт» энтропию у gameplay**, и наоборот. Если
два клиента в сетевой игре проигрывают по-разному воспроизводимый
GUI, их глобальные `RandSeed` расходятся, и gameplay тоже разойдётся.

Этого избегают двумя способами:
- Для visual-only RNG (тучи, погода, GUI) — отдельные потоки
  (`AirWeatherRandom`, `RandomExt`).
- Для gameplay-критичных мест — **локальный пересев** (см. §5).

## 5. Главный паттерн детерминизма: пересев перед операцией

В скриптах `lib/unit.script` 4 вызова `SetRandomKey` — все
сделаны **специально для синхронизации**. Контекст из кода:

```pascal
// unit.script — перед формированием отряда
SetRandomKey(floor(random * gc_MaxInt));
// needed to sync multiplayer arg.frnd
arg.frnd := random;
```

```pascal
// unit.script — перед расчётом, зависящим от персонального юнита
SetRandomKey(floor(TObj(pobj).uniqrnd * gc_MaxInt));
// sync multiplayer
```

**Архитектурный паттерн:** перед операцией, требующей одинакового
результата на всех клиентах, скрипт **пересеивает глобальный RNG**
из источника, который **гарантированно одинаков на всех клиентах**:

| Источник пересева | Откуда детерминирован |
|---|---|
| `random` (предыдущее значение) | Если до этого синхронизация уже была — то одинакова. |
| `TObj(pobj).uniqrnd * gc_MaxInt` | `uniqrnd` юнита — фиксирован при спавне и **синхронно сохраняется** (см. поле `uniqrnd` в [`server_sync_packet_format.md` §3.1](server_sync_packet_format.md)). |

Это **не lockstep**, а **per-decision deterministic seed**. То же
самое решение, принятое на сервере и на клиенте (например, «какая
формация юнитов в отряде»), даст бит-в-бит одинаковый результат, не
требуя синхронизированного RNG-состояния.

## 6. Воспроизводимость значений

С учётом §2 (LCG) — задав `SetRandomKey(seed)`, можно полностью
воспроизвести следующие N значений `random`. Простая Python-модель:

```python
def delphi_random_stream(seed):
    s = seed & 0xFFFFFFFF
    while True:
        s = (s * 134775813 + 1) & 0xFFFFFFFF
        yield s / 0xFFFFFFFF

# Например, для seed=42:
g = delphi_random_stream(42)
print([next(g) for _ in range(5)])
# [0.5263867462985266, 0.4017018212098335, 0.7770079020410776, ...]
```

Это значит — **для каждого `uniqrnd` юнита можно заранее предсказать
любую RNG-зависимую величину** (хедшот, разлёт снаряда, выбор цели
из равных кандидатов). Симулятор может это использовать для
повторения боёв из save'ов.

## 7. Что насчёт MT-19937

Стандартный DWS (на GitHub) предоставляет **и LCG (`Random`), и
Mersenne Twister** (через `dwsRandomFunctions.pas`). Но в C3 имя
`Random` в exe регистрируется как **обычный 32-bit LCG**, потому что:

1. `SetRandomKey(seed: Integer)` принимает **только 32-битный `seed`**
   — для MT-19937 (624-сложного состояния) этого недостаточно.
2. Реакция `RandSeed` (Delphi standard global) на `SetRandomKey`
   — стандартное Delphi-поведение, MT не интегрирован в это.

Поэтому несмотря на то, что MT-19937 в DWS доступен, в C3 он **не
используется**. `RandomExt` — независимая функция, скорее всего
Xorshift64 (см. §3).

## 8. Связь с другими RNG-потоками

Все 4 потока [из `native_api.md` §2.4](native_api.md):

```
            ┌─ Random           (32-bit LCG, gameplay)
            ├─ RandomExt        (64-bit Xorshift?, AI/UI)
RNG потоки ─┼─ MapGenerator     (генератор карт, изолирован)
            └─ GlobalMapGenerator (campaign-level seed)
            (+ изолированный AirWeatherRandom для облаков/ветра)
```

`MapGenerator` принимает 2-key seed (`SetMapGeneratorRandomKey(k0,
k1)`) — то есть **тоже 64-битное состояние**, как у `RandomExt`. Это
объясняет, почему пара `(randkey0, randkey1)` для воспроизведения
карты — стандартное представление в save и lobby (см.
[`map_generation_pipeline.md`](../../docs/recon/world/map/map_generation_pipeline.md) §12).

## 9. Что это значит для симулятора

Для модели extraction (см.
[`docs/recon/world/peasant_extraction.md`](../../docs/recon/world/economy/peasant_extraction.md)),
если мы хотим **бит-точно** воспроизвести добычу с заданного save'а:

1. Считать `RandSeed` нельзя — он не сохраняется как отдельное поле.
2. Вместо этого считаем `uniqrnd` каждого крестьянина (есть в
   sync-снимке).
3. Для каждой RNG-зависимой операции в hot-loop'е (например, выбор
   точки на дереве) симулятор должен **знать пересевы** в скрипте и
   повторить их.
4. Реальная реализация — пройти `lib/unit.script` `_unit_DoExtract`
   и для каждого `random`-вызова определить, был ли там
   `SetRandomKey` непосредственно перед.

Это и есть план для симулятора Level C
[`project_level_c_simulator_plan.md`](../../docs/architecture.md)
(если симулятор когда-нибудь будет нацелен на bit-perfect
reproducibility, а не на статистическую точность).

## 10. Открытое

1. **Точная реализация `RandomExt`.** Скорее всего Xorshift64,
   но без репо C3 не докажешь. Можно валидировать
   in-game: засеять через `SetRandomExtKey64(0, 1)`, прочитать 100
   значений, сравнить с эталонами Xorshift64 / L'Ecuyer.
2. **Состояние `MapGenerator` и `GlobalMapGenerator`** — тоже 64-bit,
   но какой именно алгоритм — не знаем. Из RTTI видны классы
   `TXMapGenerator` и `TXGlobalMapGenerator` (см.
   [`rtti_class_map.md` §8](rtti_class_map.md)) — это namespacing,
   но не алгоритм. Не критично: оно ре-инициализируется один раз
   перед генерацией карты, после чего карта детерминирована при
   том же seed.
3. **`PlayerCubeRandomValue`.** Per-player детерминированный «куб
   случайности». Семантика неясна (см. [`native_api.md` §2.4](native_api.md))
   — кандидат на отдельную RE-сессию.
