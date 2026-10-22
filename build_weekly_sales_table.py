#Build a one-row-per-product table from the store weekly sales export.

from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
RAW_PATH = BASE_DIR / "Store Weekly Sales History Export.csv"
OUTPUT_PATH = BASE_DIR / "product_table.csv"

# A product is sparse if it fails either condition below.
MIN_WEEKS_OBSERVED = 8
MIN_COVERAGE = 0.25

KEY_COLUMNS = ["store_id", "week_start_date", "product_id"]


def load_raw(path: Path = RAW_PATH) -> pd.DataFrame:
    """Read the raw CSV export with string identifiers."""
    return pd.read_csv(
        path,
        dtype={
            "store_id": "string",
            "product_id": "string",
            "product_name": "string",
            "category": "string",
            "week_start_date": "string",
        },
    )

#Parse dates, drop exact duplicate rows and check the weekly key is unique.
def clean_weekly(raw: pd.DataFrame) -> pd.DataFrame:
    weekly = raw.copy()
    weekly["week_start_date"] = pd.to_datetime(weekly["week_start_date"], format="%Y-%m-%d")

    exact_duplicates = weekly.duplicated().sum()
    weekly = weekly.drop_duplicates()
    print(f"Dropped {exact_duplicates} exact duplicate row(s)")

    conflicting = weekly.duplicated(subset=KEY_COLUMNS, keep=False)
    if conflicting.any():
        raise ValueError(
            "Conflicting rows share the same store, week and product:\n"
            f"{weekly.loc[conflicting]}"
        )
    return weekly


#Return every sparse condition the product trips, or an empty string.
def sparse_reason(row: pd.Series) -> str:
    reasons = []
    if row["weeks_observed"] < MIN_WEEKS_OBSERVED:
        reasons.append(f"weeks_observed {row['weeks_observed']} < {MIN_WEEKS_OBSERVED}")
    if row["coverage"] < MIN_COVERAGE:
        reasons.append(f"coverage {row['coverage']:.1%} < {MIN_COVERAGE:.0%}")
    return "; ".join(reasons)

#Summarise the weekly rows into one row per product_id.
def build_product_table(weekly: pd.DataFrame) -> pd.DataFrame:
    attributes_per_product = weekly.groupby("product_id")[["product_name", "category"]].nunique()
    if (attributes_per_product > 1).any().any():
        raise ValueError("product_name or category varies within a product_id")

    # Coverage is measured against the weeks that appear anywhere in the export.
    total_weeks = weekly["week_start_date"].nunique()

    table = (
        weekly.groupby("product_id")
        .agg(
            product_name=("product_name", "first"),
            category=("category", "first"),
            weeks_observed=("week_start_date", "nunique"),
            first_week=("week_start_date", "min"),
            last_week=("week_start_date", "max"),
            distinct_prices=("price", "nunique"),
            min_price=("price", "min"),
            max_price=("price", "max"),
            avg_price=("price", "mean"),
            total_units_sold=("units_sold", "sum"),
            avg_units_sold=("units_sold", "mean"),
        )
        .reset_index()
    )

    table["coverage"] = table["weeks_observed"] / total_weeks
    table["sparse_reason"] = table.apply(sparse_reason, axis=1)
    table["is_sparse"] = table["sparse_reason"] != ""
    table["is_single_price"] = table["distinct_prices"] == 1

    if not table["product_id"].is_unique:
        raise ValueError("product_id is not unique in the product table")

    return table[
        [
            "product_id",
            "product_name",
            "category",
            "weeks_observed",
            "coverage",
            "first_week",
            "last_week",
            "distinct_prices",
            "min_price",
            "max_price",
            "avg_price",
            "total_units_sold",
            "avg_units_sold",
            "is_sparse",
            "sparse_reason",
            "is_single_price",
        ]
    ]


def main() -> None:
    weekly = clean_weekly(load_raw())
    table = build_product_table(weekly)

    print(f"Products: {len(table)}")
    print(table.to_string(index=False))

    table.to_csv(OUTPUT_PATH, index=False)
    print(f"\nSaved table to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
