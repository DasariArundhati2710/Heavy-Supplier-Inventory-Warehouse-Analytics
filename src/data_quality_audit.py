import pandas as pd
from pathlib import Path

input_folder = Path("data/raw")
output_folder = Path("docs")
output_folder.mkdir(parents=True, exist_ok=True)

missing_reports = []
summary_reports = []

for file_path in sorted(input_folder.glob("*.csv")):
    df = pd.read_csv(file_path)

    print("\n" + "=" * 50)
    print("DATASET:", file_path.name)
    print("Rows:", len(df), "| Columns:", len(df.columns))

    missing = df.isna().sum()
    missing = missing[missing > 0]

    if missing.empty:
        print("Missing values: None")
    else:
        print("Missing values by column:")
        print(missing.to_string())

        for column, count in missing.items():
            missing_reports.append({
                "dataset": file_path.name,
                "column": column,
                "missing_count": int(count),
                "missing_percent": round(count / len(df) * 100, 2)
            })

    print("Duplicate rows:", int(df.duplicated().sum()))

    summary_reports.append({
        "dataset": file_path.name,
        "rows": len(df),
        "columns": len(df.columns),
        "missing_cells": int(df.isna().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum())
    })

pd.DataFrame(summary_reports).to_csv(
    output_folder / "dataset_quality_summary.csv", index=False
)

pd.DataFrame(
    missing_reports,
    columns=["dataset", "column", "missing_count", "missing_percent"]
).to_csv(output_folder / "missing_values_report.csv", index=False)

print("\nAUDIT COMPLETE")
print("Reports saved in docs/")