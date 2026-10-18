
import pandas as pd
from pathlib import Path

DATA = Path("data/cleaned")

ledger = pd.read_csv(DATA / "stock_ledger.csv")
products = pd.read_csv(DATA / "products.csv")

ledger["movement_date"] = pd.to_datetime(
    ledger["movement_date"], errors="coerce"
)
ledger["quantity"] = pd.to_numeric(
    ledger["quantity"], errors="coerce"
)

print("MOVEMENT TYPES")
print(ledger["movement_type"].value_counts(dropna=False).to_string())

summary = ledger.groupby(
    ["branch_id", "product_id"], as_index=False
).agg(
    movement_count=("movement_id", "nunique"),
    total_quantity=("quantity", "sum"),
    latest_movement=("movement_date", "max")
)

summary = summary.merge(
    products[["product_id", "product_name", "category"]],
    on="product_id",
    how="left",
    validate="many_to_one"
)

summary = summary.sort_values("total_quantity")

summary.to_csv(
    DATA / "stock_movement_summary.csv",
    index=False
)

branch_summary = ledger.groupby("branch_id", as_index=False).agg(
    movement_count=("movement_id", "nunique"),
    net_quantity=("quantity", "sum")
)

branch_summary.to_csv(
    DATA / "branch_stock_movement_summary.csv",
    index=False
)

print("\nMOVEMENT RECORDS:", len(ledger))
print("Branch-product combinations:", len(summary))

print("\nBRANCH MOVEMENT SUMMARY")
print(branch_summary.to_string(index=False))

print("\nLOWEST NET QUANTITY COMBINATIONS")
print(
    summary[[
        "branch_id", "product_id", "product_name",
        "movement_count", "total_quantity"
    ]].head(10).to_string(index=False)
)

print("\nSaved stock movement reports in data/cleaned/")
