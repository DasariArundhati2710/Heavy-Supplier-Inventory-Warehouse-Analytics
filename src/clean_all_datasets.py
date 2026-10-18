
import pandas as pd
from pathlib import Path

RAW_DIR = Path("data/raw")
CLEAN_DIR = Path("data/cleaned")
CLEAN_DIR.mkdir(parents=True, exist_ok=True)

date_columns = {
    "branches.csv": [],
    "customers.csv": ["customer_since", "last_purchase_date"],
    "inventory_master.csv": [],
    "invoices.csv": ["invoice_date", "due_date"],
    "payments.csv": ["payment_date"],
    "products.csv": ["last_purchase_date"],
    "purchase_orders_header.csv": [
        "order_date", "expected_delivery_date", "received_date"
    ],
    "purchase_orders_lines.csv": [],
    "sales_orders_header.csv": ["order_date", "delivery_date"],
    "sales_orders_lines.csv": [],
    "stock_ledger.csv": ["movement_date"],
    "suppliers.csv": []
}

for file_path in sorted(RAW_DIR.glob("*.csv")):
    df = pd.read_csv(file_path)
    original_rows = len(df)

    # Standardize column names and text fields
    df.columns = df.columns.str.strip().str.lower()

    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].apply(
            lambda value: value.strip() if isinstance(value, str) else value
        )
        df[col] = df[col].replace("", pd.NA)

    # Convert known date columns without inventing dates
    for col in date_columns.get(file_path.name, []):
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    # Remove only exact duplicate rows
    duplicate_count = int(df.duplicated().sum())
    if duplicate_count:
        df = df.drop_duplicates()

    output_path = CLEAN_DIR / file_path.name
    df.to_csv(output_path, index=False, date_format="%Y-%m-%d")

    print(
        f"{file_path.name}: "
        f"{original_rows} input rows, "
        f"{len(df)} output rows, "
        f"{duplicate_count} duplicates removed, "
        f"{int(df.isna().sum().sum())} missing cells remaining"
    )

print("\nCLEANING COMPLETE")
print("Cleaned files saved in data/cleaned/")
