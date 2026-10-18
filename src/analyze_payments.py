
import pandas as pd
from pathlib import Path

DATA = Path("data/cleaned")

invoices = pd.read_csv(DATA / "invoices.csv")
payments = pd.read_csv(DATA / "payments.csv")

for col in ["grand_total"]:
    invoices[col] = pd.to_numeric(invoices[col], errors="coerce")

payments["payment_amount"] = pd.to_numeric(
    payments["payment_amount"], errors="coerce"
)

# Report repeated invoice IDs; preserve all invoice rows
duplicate_ids = invoices[
    invoices["invoice_id"].duplicated(keep=False)
].sort_values("invoice_id")

duplicate_ids.to_csv(
    DATA / "duplicate_invoice_ids_review.csv", index=False
)

# Create a unique row key for this analysis
invoices = invoices.reset_index(drop=True)
invoices["invoice_row_id"] = invoices.index + 1

# Aggregate payments by invoice ID
payment_summary = payments.groupby("invoice_id", as_index=False).agg(
    total_paid=("payment_amount", "sum"),
    payment_count=("payment_id", "nunique")
)

# Because invoice IDs repeat, this merge may associate payments with
# multiple invoice rows. Flag those rows for review.
df = invoices.merge(
    payment_summary,
    on="invoice_id",
    how="left",
    validate="many_to_one",
    indicator=True
)

df["total_paid"] = df["total_paid"].fillna(0)
df["payment_count"] = df["payment_count"].fillna(0).astype(int)
df["outstanding_amount"] = df["grand_total"] - df["total_paid"]

df["balance_status"] = "Paid"
df.loc[df["outstanding_amount"] > 0.01, "balance_status"] = "Outstanding"
df.loc[df["outstanding_amount"] < -0.01, "balance_status"] = "Overpaid"

df["review_required"] = df["invoice_id"].isin(
    duplicate_ids["invoice_id"]
)

df.to_csv(DATA / "invoice_payment_analysis.csv", index=False)

print("PAYMENT ANALYSIS — PRELIMINARY")
print("=" * 50)
print("Invoice rows:", len(df))
print("Unique invoice IDs:", invoices["invoice_id"].nunique())
print("Rows with repeated invoice IDs:", len(duplicate_ids))
print("Rows requiring invoice-ID review:", int(df["review_required"].sum()))
print("Rows with no matching payment record:",
      int((df["_merge"] == "left_only").sum()))

print("\nInvoice row totals and payment totals are preliminary.")
print("Do not treat outstanding totals as final until repeated IDs are resolved.")
print("\nSaved:")
print("data/cleaned/invoice_payment_analysis.csv")
print("data/cleaned/duplicate_invoice_ids_review.csv")
