
import pandas as pd
from pathlib import Path

input_file = Path("data/raw/branches.csv")
output_file = Path("data/cleaned/branches_cleaned.csv")

df = pd.read_csv(input_file)

df.columns = df.columns.str.strip()

df["warehouse_capacity"] = (
    df["warehouse_capacity"]
    .astype(str)
    .str.replace("sqft", "", regex=False)
    .str.strip()
)

df["warehouse_capacity"] = pd.to_numeric(
    df["warehouse_capacity"], errors="raise"
)

df["service_center_available"] = (
    df["service_center_available"].str.strip().str.title()
)

df.to_csv(output_file, index=False)

print("Cleaning completed!")
print("Rows and columns:", df.shape)
print("Missing values:", df.isna().sum().sum())
print("Duplicate rows:", df.duplicated().sum())
print("Warehouse capacity type:", df["warehouse_capacity"].dtype)
print("Saved to:", output_file)
