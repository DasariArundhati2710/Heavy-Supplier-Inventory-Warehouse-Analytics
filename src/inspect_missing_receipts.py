
import pandas as pd

df = pd.read_csv("data/raw/purchase_orders_header.csv")

missing = df[df["received_date"].isna()]

print("Total purchase orders:", len(df))
print("Missing received dates:", len(missing))

print("\nPO status for missing received dates:")
print(missing["po_status"].value_counts(dropna=False))

print("\nMissing dates by status:")
print(
    pd.crosstab(
        df["po_status"],
        df["received_date"].isna(),
        margins=True
    )
)
