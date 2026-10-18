
import pandas as pd
from pathlib import Path

DATA = Path("data/cleaned")
OUTPUT = Path("data/cleaned")
OUTPUT.mkdir(parents=True, exist_ok=True)

po = pd.read_csv(DATA / "purchase_orders_header.csv")
suppliers = pd.read_csv(DATA / "suppliers.csv")

for col in ["order_date", "expected_delivery_date", "received_date"]:
    po[col] = pd.to_datetime(po[col], errors="coerce")

po["delay_days"] = (
    po["received_date"] - po["expected_delivery_date"]
).dt.days

po["actual_lead_time_days"] = (
    po["received_date"] - po["order_date"]
).dt.days

po["received"] = po["received_date"].notna()
po["on_time"] = (
    po["received"] &
    (po["delay_days"] <= 0)
)

summary = po.groupby("supplier_id").agg(
    total_orders=("po_id", "nunique"),
    cancelled_orders=(
        "po_status",
        lambda s: s.astype(str).str.lower().eq("cancelled").sum()
    ),
    orders_with_receipt=("received", "sum"),
    on_time_orders=("on_time", "sum"),
    avg_actual_lead_time_days=("actual_lead_time_days", "mean"),
    avg_delay_days=("delay_days", "mean"),
    total_order_cost=("total_cost", "sum")
).reset_index()

summary["cancellation_rate_percent"] = (
    summary["cancelled_orders"] / summary["total_orders"] * 100
).round(2)

summary["on_time_rate_percent"] = (
    summary["on_time_orders"] / summary["orders_with_receipt"] * 100
).round(2)

summary["avg_actual_lead_time_days"] = (
    summary["avg_actual_lead_time_days"].round(2)
)

summary["avg_delay_days"] = summary["avg_delay_days"].round(2)

summary = summary.merge(
    suppliers[["supplier_id", "supplier_name", "reliability_score",
               "lead_time_days"]],
    on="supplier_id",
    how="left",
    validate="one_to_one"
)

summary = summary.sort_values(
    "on_time_rate_percent", ascending=False, na_position="last"
)

summary.to_csv(
    OUTPUT / "supplier_performance_analysis.csv",
    index=False
)

print("SUPPLIER PERFORMANCE ANALYSIS")
print("=" * 60)
print(summary.to_string(index=False))
print("\nSaved: data/cleaned/supplier_performance_analysis.csv")
