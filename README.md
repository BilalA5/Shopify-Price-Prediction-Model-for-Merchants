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

## Demand model

_Not started._

## Recommender spec

_Not started._

## Catalog audit

_Not started._

## Streamlit app

_Not started._
