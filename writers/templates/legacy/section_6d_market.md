## 6d. Рынок — обменные курсы

Рынок (`mar` building) позволяет менять ресурсы. Формула обмена использует **buy** и **sell** цены каждого ресурса. После сделки цены **сдвигаются**: `buycost` растёт к `buycostmax`, `sellcost` падает к `sellcostmin`. Поэтому повторные продажи одного и того же ресурса дают всё меньше.

> **Полная статья по рынку:** [`reference/06_market.md`](reference/06_market.md) — global rates, first-mover advantage, формулы пересчёта, численные примеры.

**Default ratio:** при стандартных ценах `received_Y = sold_X × sellcost[X] / buycost[Y]`.
