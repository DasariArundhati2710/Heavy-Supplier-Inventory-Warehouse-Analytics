
import pandas as pd

df = pd.read_csv("data/cleaned/branches_cleaned.csv")

df["estimated_monthly_profit"] = (
    df["avg_monthly_revenue"] - df["monthly_operational_cost"]
)

df["profit_margin_percent"] = (
    df["estimated_monthly_profit"] / df["avg_monthly_revenue"] * 100
).round(2)

print("BRANCH PERFORMANCE ANALYSIS")
print(df[[
    "branch_name",
    "city",
    "avg_monthly_revenue",
    "monthly_operational_cost",
    "estimated_monthly_profit",
    "profit_margin_percent"
]].to_string(index=False))

print("\nAVERAGE MONTHLY REVENUE:", round(df["avg_monthly_revenue"].mean(), 2))
print("AVERAGE MONTHLY OPERATIONAL COST:", round(df["monthly_operational_cost"].mean(), 2))
print("HIGHEST REVENUE BRANCH:", df.loc[df["avg_monthly_revenue"].idxmax(), "branch_name"])
print("LOWEST REVENUE BRANCH:", df.loc[df["avg_monthly_revenue"].idxmin(), "branch_name"])
from pathlib import Path

output_dir = Path("data/cleaned")
output_dir.mkdir(parents=True, exist_ok=True)

df.to_csv(output_dir / "branch_performance_analysis.csv", index=False)

print("\nAnalysis saved to data/cleaned/branch_performance_analysis.csv")