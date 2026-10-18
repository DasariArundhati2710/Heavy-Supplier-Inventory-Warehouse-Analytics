
import pandas as pd
from pathlib import Path

DATA = Path("data/cleaned")

orders = pd.read_csv(DATA / "sales_orders_header.csv")
lines = pd.read_csv(DATA / "sales_orders_lines.csv")
products = pd.read_csv(DATA / "products.csv")
branches = pd.read_csv(DATA / "branches.csv")

orders["order_date"] = pd.to_datetime(orders["order_date"], errors="coerce")

orders["grand_total"] = pd.to_numeric(orders["grand_total"], errors="coerce")

lines["quantity"] = pd.to_numeric(lines["quantity"], errors="coerce")
lines["line_total"] = pd.to_numeric(lines["line_total"], errors="coerce")

monthly = orders.dropna(subset=["order_date"]).copy()
monthly["month"] = monthly["order_date"].dt.to_period("M").astype(str)

monthly_sales = monthly.groupby("month", as_index=False).agg(
    order_count=("so_id", "nunique"),
    sales_value=("grand_total", "sum")
)

branch_sales = orders.groupby("branch_id", as_index=False).agg(
    order_count=("so_id", "nunique"),
    sales_value=("grand_total", "sum")
).merge(
    branches[["branch_id", "branch_name"]],
    on="branch_id",
    how="left",
    validate="many_to_one"
)

product_sales = lines.groupby("product_id", as_index=False).agg(
    units_sold=("quantity", "sum"),
    sales_value=("line_total", "sum")
).merge(
    products[["product_id", "product_name", "category"]],
    on="product_id",
    how="left",
    validate="many_to_one"
).sort_values("sales_value", ascending=False)

monthly_sales.to_csv(DATA / "monthly_sales_analysis.csv", index=False)
branch_sales.to_csv(DATA / "branch_sales_analysis.csv", index=False)
product_sales.to_csv(DATA / "product_sales_analysis.csv", index=False)

print("MONTHLY SALES — first and last 10 months")
print(monthly_sales.head(10).to_string(index=False))
print("\nLatest months:")
print(monthly_sales.tail(10).to_string(index=False))

print("\nSALES BY BRANCH")
print(branch_sales.to_string(index=False))

print("\nTOP 10 PRODUCTS BY SALES VALUE")
print(product_sales.head(10).to_string(index=False))

print("\nSaved monthly, branch, and product sales reports in data/cleaned/")
