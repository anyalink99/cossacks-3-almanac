**Пример обмена при default-ценах:**

- Sell 100 food (sellcost ≈ 15.20) → получишь `100 × 15.20 / 50 = 30.4` wood.
- Sell 100 gold (sellcost = 110) → получишь `100 × 110 / 50 = 220` wood.
- Sell 100 iron (sellcost = 60) → получишь `100 × 60 / 25 = 240` food.

Источник: `res.script:_res_InitEconomy` (стр. 178-249), `res.script:_res_MarketTradeResources` (стр. 320-344). `gc_economy_exp = 0.00002` контролирует скорость деградации курса.
