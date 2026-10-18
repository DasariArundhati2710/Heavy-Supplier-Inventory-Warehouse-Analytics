
from pathlib import Path
import pandas as pd

base = Path(__file__).resolve().parent.parent
data_dir = base / "data" / "cleaned"
output = base / "docs" / "data_quality_report.csv"

results = []

for file in sorted(data_dir.glob("*.csv")):
    df = pd.read_csv(file)
    results.append({
        "dataset": file.name,
        "row_count": len(df),
        "column_count": len(df.columns),
        "duplicate_rows": int(df.duplicated().sum()),
        "missing_cells": int(df.isna().sum().sum()),
        "duplicate_invoice_ids": (
            int(df["invoice_id"].duplicated().sum())
            if "invoice_id" in df.columns else "N/A"
        ),
        "duplicate_payment_ids": (
            int(df["payment_id"].duplicated().sum())
            if "payment_id" in df.columns else "N/A"
        )
    })

pd.DataFrame(results).to_csv(output, index=False)
print(f"Quality report saved to: {output}")
