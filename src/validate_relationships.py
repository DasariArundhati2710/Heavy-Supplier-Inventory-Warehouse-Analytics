
import pandas as pd
from pathlib import Path

DATA_DIR = Path("data/cleaned")

def load(name):
    return pd.read_csv(DATA_DIR / name)

checks = [
    ("purchase_orders_header.csv", "supplier_id",
     "suppliers.csv", "supplier_id"),
    ("purchase_orders_header.csv", "branch_id",
     "branches.csv", "branch_id"),
    ("purchase_orders_lines.csv", "po_id",
     "purchase_orders_header.csv", "po_id"),
    ("purchase_orders_lines.csv", "product_id",
     "products.csv", "product_id"),
    ("sales_orders_header.csv", "customer_id",
     "customers.csv", "customer_id"),
    ("sales_orders_header.csv", "branch_id",
     "branches.csv", "branch_id"),
    ("sales_orders_lines.csv", "so_id",
     "sales_orders_header.csv", "so_id"),
    ("sales_orders_lines.csv", "product_id",
     "products.csv", "product_id"),
    ("inventory_master.csv", "product_id",
     "products.csv", "product_id"),
    ("inventory_master.csv", "branch_id",
     "branches.csv", "branch_id"),
    ("invoices.csv", "so_id",
     "sales_orders_header.csv", "so_id"),
    ("invoices.csv", "customer_id",
     "customers.csv", "customer_id"),
    ("payments.csv", "invoice_id",
     "invoices.csv", "invoice_id"),
    ("stock_ledger.csv", "product_id",
     "products.csv", "product_id"),
    ("stock_ledger.csv", "branch_id",
     "branches.csv", "branch_id")
]

print("RELATIONSHIP VALIDATION")
print("=" * 65)

issues = 0

for child_file, child_col, parent_file, parent_col in checks:
    child = load(child_file)
    parent = load(parent_file)

    child_ids = set(child[child_col].dropna().astype(str).str.strip())
    parent_ids = set(parent[parent_col].dropna().astype(str).str.strip())

    unmatched = child_ids - parent_ids

    if unmatched:
        issues += 1
        print(f"\nCHECK: {child_file}.{child_col} -> "
              f"{parent_file}.{parent_col}")
        print("Unmatched unique IDs:", len(unmatched))
        print("Examples:", list(unmatched)[:10])

print("\n" + "=" * 65)

if issues == 0:
    print("All checked relationships passed.")
else:
    print("Relationships with unmatched IDs:", issues)

print("VALIDATION COMPLETE")
