
from pathlib import Path
import pandas as pd

base = Path(__file__).resolve().parent.parent
data_dir = base / "data" / "cleaned"
output = base / "docs" / "data_dictionary.csv"

rows = []

for file in sorted(data_dir.glob("*.csv")):
    df = pd.read_csv(file, nrows=100)
    for col in df.columns:
        rows.append({
            "dataset": file.name,
            "column": col,
            "data_type": str(df[col].dtype),
            "non_null_samples": int(df[col].notna().sum()),
            "sample_value": str(df[col].dropna().iloc[0])
            if df[col].notna().any() else ""
        })

pd.DataFrame(rows).to_csv(output, index=False)
print(f"Data dictionary saved to: {output}")
