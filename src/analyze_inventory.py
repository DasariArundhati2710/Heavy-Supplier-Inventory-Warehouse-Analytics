
import pandas as pd
from pathlib import Path

DATA = Path("data/cleaned")

inventory = pd.read_csv(DATA / "inventory_master.csv")
products = pd.read_csv(DATA / "products.csv")

df = inventory.merge(
    products[["product_id", "product_name", "category"]],
    on="product_id",
    how="left",
    validate="many_to_one"
)

df["stock_status"] = "Normal"

df.loc[df["current_stock"] <= df["reorder_level"], "stock_status"] = "Reorder"
df.loc[df["current_stock"] <= df["safety_stock"], "stock_status"] = "Below Safety Stock"
df.loc[df["current_stock"] <= 0, "stock_status"] = "Stockout"
df.loc[df["current_stock"] > df["max_stock"], "stock_status"] = "Excess Stock"

df["reorder_quantity"] = (
    df["max_stock"] - df["current_stock"]
).clip(lower=0)

df.to_csv(DATA / "inventory_risk_analysis.csv", index=False)

print("INVENTORY RISK SUMMARY")
print("=" * 50)
print("Total product-branch records:", len(df))
print("\nRecords by stock status:")
print(df["stock_status"].value_counts().to_string())

print("\nTotal current stock:", df["current_stock"].sum())
print("Products below safety stock:",
      (df["current_stock"] <= df["safety_stock"]).sum())
print("Stockout records:", (df["current_stock"] <= 0).sum())
print("Excess stock records:", (df["current_stock"] > df["max_stock"]).sum())

print("\nMost urgent inventory records:")
urgent = df[df["stock_status"].isin(
    ["Stockout", "Below Safety Stock"]
)]

print(
    urgent[[
        "product_id", "product_name", "category", "branch_id",
        "current_stock", "safety_stock", "reorder_level", "stock_status"
    ]].head(15).to_string(index=False)
)

print("\nSaved: data/cleaned/inventory_risk_analysis.csv")
