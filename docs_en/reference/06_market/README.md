#06.Market

[← Index](README.md)

> **The main thing at the start:**
>
> 1. **Rates are global.** The game has one economy for everyone - all players see it at the same time. The building `mar` does not set its own “local” course, but opens access to this global one.
> 2. **Whoever built the market first skims the cream.** Starting rates are at standard values. Any first big deal will make them worse for the next ones. The recovery is gradual (~2.5% deviation per game second), so that those who are catching up will receive the already sagging rates.
> 3. **Demand and supply.** By buying X, you move both `buycost[X]` (more expensive to buy) and `sellcost[X]` (more profitable to sell) to their maximums. By selling X, you move both to their minimums. Untraded resources remain at standard values.

## Exchange rates

`buycost` is the price of the resource when you **buy it**. `sellcost` - compensation when you **sell it**. Each resource has a range of `[min ; max]` and a starting value of `def`.

| Resource | buy_min | buy_def | buy_max | sell_min | sell_def | sell_max |
|---|---:|---:|---:|---:|---:|---:|
| food | 20 | 25.00 | 40 | 10.64 | 15.20 | 19.76 |
| wood | 40 | 50.00 | 60 | 20.00 | 30.00 | 40.00 |
| stone | 40 | 50.00 | 60 | 15.68 | 20.90 | 26.13 |
| gold | 140 | 190.00 | 240 | 80.00 | 110.00 | 140.00 |
| iron | 100 | 140.00 | 180 | 40.00 | 60.00 | 80.00 |
| coal | 100 | 140.00 | 180 | 40.00 | 60.00 | 80.00 |

## Exchange formula
```
received_Y = floor(sold_X × sellcost[X] / buycost[Y])
```
`sellcost[X]` is the current sellcost of resource X, `buycost[Y]` is the current buycost of resource Y. You get the least for the “long-distance” exchange (food → gold) and the most for the “reverse” exchange (gold → food or iron → food), because gold/iron sellcost is already high, and food buycost is low.

## Courses are global. All players can see them

The array `gEconomy[restype]` (`res.script:_res_InitEconomy`) is indexed only by resource type - **not by players**. When you make an exchange through `_res_MarketTradeResources`, the script mutates exactly this global array - the same `buycost` / `sellcost`, which the opponent sees at the same moment in his market UI.

The `mar` (market) building is simply permission for the player to **participate** in an exchange. It does not create “its own” market and does not make the exchange rate more profitable for the one who created it. All six resources and their six values ​​`gEconomy[*].{buy,sell}cost` are common for the entire game.

### What does this mean in practice?

- **Whoever first built the market trades at the standard rate.** Before his transactions, prices are not shifted by anyone.
- **A large first trade shifts the rate for everyone.** If the first player immediately exchanges 5000 food → wood, the others will see `food.sellcost` already lower than the standard and `wood.buycost` higher. The catcher gets less wood for the same amount of food.
- **The rate is recovering.** In parallel with trading, `_res_ProcessEconomy(deltatime)` occurs: each tick the deviation from the standard value decreases exponentially with the coefficient `dt = deltatime × 0.025 × max(1, garr_res_dlt × 0.01)`. That is, per game second, the deviation from the standard price drops by approximately **2.5%** (faster if resources are actively changing in the world). Return half-period ≈ **28 game seconds**.
- **Cheap deals hardly move the rate.** The impact of one deal is scaled through `weight = amount × gc_economy_exp = amount × 0.00002`. To really get hooked on a course, you need thousands of units.

## How much does one exchange shift

After each transaction, the game recalculates prices like this:
```
# Покупка amount единиц Y:
weight = amount × 0.00002
buycost[Y]  ← (buycost[Y]  + buycostmax[Y]  × weight) / (1 + weight)
sellcost[Y] ← (sellcost[Y] + sellcostmax[Y] × weight) / (1 + weight)

# Продажа amount единиц X:
weight = amount × 0.00002
sellcost[X] ← (sellcost[X] + sellcostmin[X] × weight) / (1 + weight)
buycost[X]  ← (buycost[X]  + buycostmin[X]  × weight) / (1 + weight)
```
This is the “weighted average to limit” formula: the greater `amount × 0.00002`, the more the current price is drawn towards the limit (max when buying, min when selling).

> **Numerically (at the standard rate, we sell food):** `weight = 0.00002 × amount`. For `food.sellcost` to drop from 15.20 to, say, 12.0, you need many thousands of food sold in one go. On regular transactions of 100–500 units, the rate shifts by a fraction of a percent - noticeable only with a one-time large exchange (for example, converting a looted warehouse).

### Examples of exchanges at the default rate

How much Y will you get for 100 units of X on the fresh market. After a couple of trades, the numbers will shift to the worse.

| Selling | You get | What | According to the formula |
|---|---:|---|---|
| 100 food | **30** | wood | floor(100 × 15.20 / 50.00) |
| 100 food | **8** | gold | floor(100 × 15.20 / 190.00) |
| 100 gold | **220** | wood | floor(100 × 110.00 / 50.00) |
| 100 gold | **440** | food | floor(100 × 110.00 / 25.00) |
| 100 iron | **240** | food | floor(100 × 60.00 / 25.00) |
| 100 wood | **60** | stone | floor(100 × 30.00 / 50.00) |

### Numerical example of course shift

What will happen to the exchange rate after **one** exchange of 5000 food → wood at the fresh market (food.sellcost = 15.20, wood.buycost = 50.00):

- Received wood: `floor(5000 × 15.20 / 50.00) = 1520`.
- `wood.buycost`: 50.00 → **50.295** (shift by +0.59%, to buycostmax = 60).
- `wood.sellcost`: 30.00 → **30.295** (to sellcostmax = 40).
- `food.sellcost`: 15.20 → **14.786** (shift by -2.73%, to sellcostmin = 10.64). Those who catch up will receive less wood for their food.
- `food.buycost`: 25.00 → **24.545** (to buycostmin = 20). But buying food is now a little cheaper.

Prices return to standard values ​​at a rate of ≈ 2.5%/g-sec deviation in both directions. Half-cycle is about 28 g-seconds (≈ 20 real-seconds @ fast). In a minute or two, most of the shift will roll back - but if you trade often or in large quantities, the rate is chronically “sick”.

## Practical implications for strategy

- **Build the market before your opponent if you are planning large exchanges.** This is especially important at the start, when a single-trade for 1000+ food → wood easily shifts the rate by percentage, and the catcher gets the already shifted prices.
- **Split large transactions into several small ones with pauses.** In 30-60 g-seconds between them, the market will partially recover. It's more profitable in interest than doing it all at once.
- **“Unfavorable” exchange through gold.** Due to the high sellcost of gold and low buycost of food/wood, the `gold → food / wood` conversion gives a better rate than the other side. If a lot of gold is accumulated and there is a shortage of wood, it is more profitable to sell gold for wood than wood for gold.
- **Iron / coal:** their sell cost is the same as gold (60 def), and buy is cheaper than gold. Good reserve currencies for exchange when mines are overproducing.
- **Ships and towers spend iron / coal per shot** (see [02_combat/README.md → Cost of one shot](../02_combat/README.md#стоимость-одного-выстрела)). If warships are idle, sell excess iron/coal through the market, do not accumulate.

## Source

- `res.script:_res_InitEconomy` (pages 178-249) - starting `buy/sell × min/def/max` for each resource.
- `res.script:_res_MarketTradeResources` (pages 320-344) - exchange and recalculation of prices after the transaction.
- `res.script:_res_ProcessEconomy` (pages 270-309) - exponential recovery to standard rates between transactions.
- Constants: `gc_economy_exp = 0.00002` (weight of one trade), `gc_economy_time = 0.0001 × 32 = 0.0032` (obsolete; actual recovery rate ≈ 0.025 per game second - see formula above).