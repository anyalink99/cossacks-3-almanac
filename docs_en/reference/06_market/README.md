<a id="рынок"></a>
# Market

[← Quick reference](../README.md)

> **The essentials:**
>
> 1. **Rates are shared by everyone.** Every player sees the same prices.
> 2. **The first market gets the best opportunity.** Rates begin at their
>    standard values. A large early trade makes the following trade less
>    favorable. The deviation then recovers gradually—about 2.5% per game
>    second.
> 3. **Supply and demand.** A resource being bought becomes more expensive; a
>    resource being sold becomes cheaper. Untouched resources remain at their
>    standard rates.

<a id="курсы-обмена"></a>
## Exchange rates

Each resource has separate buying and selling rates. The table shows the
minimum, initial, and maximum values.

| Resource | Buy minimum | Buy initial | Buy maximum | Sell minimum | Sell initial | Sell maximum |
|---|---:|---:|---:|---:|---:|---:|
| Food | 20 | 25.00 | 40 | 10.64 | 15.20 | 19.76 |
| Wood | 40 | 50.00 | 60 | 20.00 | 30.00 | 40.00 |
| Stone | 40 | 50.00 | 60 | 15.68 | 20.90 | 26.13 |
| Gold | 140 | 190.00 | 240 | 80.00 | 110.00 | 140.00 |
| Iron | 100 | 140.00 | 180 | 40.00 | 60.00 | 80.00 |
| Coal | 100 | 140.00 | 180 | 40.00 | 60.00 | 80.00 |

<a id="формула-обмена"></a>
## Exchange formula

```text
amount received = amount sold × selling rate / buying rate
```

The result is rounded down. Food-to-gold trades usually return few units of
the new resource; selling gold or iron for food returns many units because
their initial rates differ greatly.

<a id="курсы--глобальные-их-видят-все-игроки"></a>
## Rates are global

A Market only gives its owner access to trading. It does not create separate
prices: all six resources use one shared set of rates for the entire match.

<a id="что-это-значит-на-практике"></a>
### Practical consequences

- **The first player to build a Market trades at the standard rate.**
- **A large first trade changes the rate for everyone.** If one player sells
  5,000 food for wood, later players receive less wood for the same food.
- **Rates recover.** About 2.5% of the deviation from the standard price
  disappears each game second. Half of the deviation is gone after roughly
  28 game seconds.
- **Small trades barely affect the price.** A noticeable shift requires
  thousands of resource units.

<a id="сколько-сдвигает-один-обмен"></a>
## How far one trade moves the rate

After each trade, prices are recalculated as follows:

```text
trade weight = amount × 0.00002
new rate = (current rate + limiting rate × trade weight) / (1 + trade weight)
```

The larger the trade, the closer the rate moves to its limit: upward for the
resource being bought and downward for the resource being sold.

> Selling 100–500 units changes the rate by only a fraction of a percent.
> A strong shift requires several thousand units in one trade.

<a id="примеры-обменов-на-начальном-курсе"></a>
### Examples at the initial rate

The following values apply to an unused Market:

| Sell | Receive | Calculation |
|---|---:|---|
| 100 food | **30 wood** | 100 × 15.20 / 50.00 |
| 100 food | **8 gold** | 100 × 15.20 / 190.00 |
| 100 gold | **220 wood** | 100 × 110.00 / 50.00 |
| 100 gold | **440 food** | 100 × 110.00 / 25.00 |
| 100 iron | **240 food** | 100 × 60.00 / 25.00 |
| 100 wood | **60 stone** | 100 × 30.00 / 50.00 |

<a id="численный-пример-сдвига-курса"></a>
### Example: one large trade

After one trade of **5,000 food for wood** at the initial rates:

- Wood received: **1,520**.
- Wood buying rate: 50.00 → **50.295** (+0.59%).
- Wood selling rate: 30.00 → **30.295**.
- Food selling rate: 15.20 → **14.786** (−2.73%); the next player receives
  less wood for food.
- Food buying rate: 25.00 → **24.545**; buying food becomes slightly cheaper.

About 2.5% of the deviation disappears per game second. Half is gone after
roughly 28 game seconds, or 20 real seconds at Fast speed. Frequent large
trades prevent full recovery.

<a id="практические-выводы-для-стратегии"></a>
## Strategic conclusions

- **Build a Market before your opponent if you plan a large trade.**
- **Split a large exchange and pause between parts.** In 30–60 game seconds,
  the Market partially recovers.
- **Gold is useful for buying food or wood.** The reverse direction is much
  less favorable.
- **Iron and coal** can also be sold when mines overproduce, but ships and
  towers consume them when firing.

<a id="источник"></a>
## Technical sources

- `res.script:_res_InitEconomy` (lines 178–249) — initial and limiting rates.
- `res.script:_res_MarketTradeResources` (lines 320–344) — trade and price
  recalculation.
- `res.script:_res_ProcessEconomy` (lines 270–309) — exponential recovery
  between trades.
- Trade weight is 0.00002 per unit; the effective recovery rate is about
  0.025 per game second.
