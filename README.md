# Shopify-Price-Prediction-Model-for-Merchants

Price prediction model that recommends a Black Friday sale price for each product a merchant sells.

## Overview

The project is built in stages. Each stage has its own section below; sections marked _Not started_ are placeholders so the structure is set before the work lands.

| Stage | Status |
|---|---|
| Data: per-product table | Built (`build_weekly_sales_table.py`) |
| Demand model | Not started |
| Recommender spec | Not started |
| Catalog audit | Not started |
| Streamlit app | Not started |

## Data

Source: `Store Weekly Sales History Export.csv`, one row per store, product and week.

`build_weekly_sales_table.py` turns the export into `product_table.csv`, one row per `product_id`, with:

- `is_sparse` and `sparse_reason`: true when a product has fewer than 8 weeks of history, with the condition that triggered it.
- `is_single_price`: true when only one price was ever seen for the product.

Run it from the repo root with `python3 build_weekly_sales_table.py`. It requires `pandas`.

### Sparse cutoff

The cutoff is 8 weeks of history. It is a judgment call, but the data supports it: the seven products split cleanly into 4-6 weeks and 12-22 weeks, with none between 7 and 11, so any cutoff from 7 to 12 gives the same flags. 8 keeps a one-week margin above the sparse group and is short enough not to flag products with a normal run of data.

Coverage (weeks observed / 41 weeks in the export) is a second, separate rule in the script. It flags products below 25%, which is about 10 weeks, so it can flag products with 8-10 weeks that the weeks rule would not. No product falls in that range today, so the two rules agree on this export.

### Latest run output

Printed by `python3 build_weekly_sales_table.py` on the current export:

```
Dropped 1 exact duplicate row(s)
Products: 7
product_id                product_name    category  weeks_observed  coverage first_week  last_week  distinct_prices  min_price  max_price  avg_price  total_units_sold  avg_units_sold  is_sparse                              sparse_reason  is_single_price
    P-1001 Heavyweight Pullover Hoodie     Apparel              22  0.536585 2022-11-07 2024-10-14                5       64.0       89.0  81.436364              1011       45.954545      False                                                       False
    P-1002        Ribbed Merino Beanie     Apparel              17  0.414634 2022-11-07 2024-10-21                4       28.0       38.0  34.470588               616       36.235294      False                                                       False
    P-1003           Waxed Canvas Tote Accessories              14  0.341463 2022-11-14 2024-10-28                4       52.0       68.0  61.285714               224       16.000000      False                                                       False
    P-1004          Stoneware Camp Mug        Home              12  0.292683 2022-11-07 2024-10-21                3       22.0       28.0  26.000000               332       27.666667      False                                                       False
    P-1005    Cedar & Smoke Soy Candle        Home               6  0.146341 2024-09-16 2024-10-28                1       34.0       34.0  34.000000                81       13.500000       True weeks_observed 6 < 8; coverage 14.6% < 25%             True
    P-1006      Holiday Enamel Pin Set Accessories               4  0.097561 2023-11-06 2023-12-04                1       18.0       18.0  18.000000               214       53.500000       True  weeks_observed 4 < 8; coverage 9.8% < 25%             True
    P-1007             Leather Key Fob Accessories               4  0.097561 2024-06-10 2024-10-14                2       24.0       26.0  25.500000                25        6.250000       True  weeks_observed 4 < 8; coverage 9.8% < 25%            False
```

## Demand model

_Not started._

## Recommender spec

_Not started._

## Catalog audit

_Not started._

## Streamlit app

_Not started._
