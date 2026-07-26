<a id="шахты"></a>
# Mines

[← Building comparisons](README.md) · [← All comparisons](../README.md) · [← Quick reference](../../README.md)

The mines produce `coal` / `gold` / `iron`. The script accidentally uses `commonsid+'X'` for all clusters (eur/rus/tur/ukr/sco), but the stats are general: the surface parser only uses the `eur*` version, because all clusters inherit the same HP/price/rate. There are **no Cluster-specific mines** - this is a single model for all nations.

| Building | Cluster | Resource | HP | Time (g-sec) | W | S | G | rate (per beat) | Add. workers |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| **Mine** `eurcoa` | eur | coal | 2500 | 93.75 | 100 | 100 | 0 | 13 | 5 |
| **Mine** `eurgol` | eur | gold | 2500 | 93.75 | 100 | 100 | 0 | 13 | 5 |
| **Mine** `euriro` | eur | iron | 2500 | 93.75 | 100 | 100 | 0 | 13 | 5 |
