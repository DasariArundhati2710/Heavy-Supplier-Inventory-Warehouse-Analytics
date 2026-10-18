import pandas as pd
from pathlib import Path

data_folder = Path("data/raw")

for file_path in sorted(data_folder.glob("*.csv")):
    print("\n" + "=" * 50)
    print("DATASET:", file_path.name)

    df = pd.read_csv(file_path)

    print("Rows:", df.shape[0])
    print("Columns:", df.shape[1])
    print("Column names:", df.columns.tolist())
    print("Missing values:", df.isna().sum().sum())
    print("Duplicate rows:", df.duplicated().sum())
    print("\nData types:")
    print(df.dtypes.to_string())