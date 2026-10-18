# Heavy Supplier, Inventory & Warehouse Analytics

## Project Overview
An individual data analytics project focused on analyzing supplier performance, purchasing operations, inventory risks, warehouse stock movements, and sales performance using Python, CSV datasets, and Power BI.

## Objectives
- Assess supplier delivery performance and purchase-order status.
- Identify inventory risks and potential overstocking.
- Analyze sales across products, branches, and months.
- Review data quality and validate dataset relationships.
- Build dashboards to support operational decision-making.

## Tools Used
- Python
- Pandas
- Power BI
- CSV datasets
- Git and GitHub

## Repository Structure
- `data/raw/` — Original source datasets
- `data/cleaned/` — Prepared datasets
- `docs/` — Reports, data dictionary, model, and sprint notes
- `notebooks/` — Data profiling notebook
- `src/` — Data cleaning, validation, and analysis scripts

## Sprint 1 Progress
- Reviewed 12 source datasets.
- Prepared cleaned datasets and ran data quality audits.
- Generated a data dictionary and quality reports.
- Validated the relationships checked by the validation script.
- Generated sales, supplier, inventory, and stock movement analysis outputs.
- Started the Power BI Sales Overview dashboard.

## Initial Findings
- Inventory quantities exceed maximum-stock levels across all 180 product-branch combinations and require investigation.
- Duplicate invoice IDs and payment IDs require further review.
- Missing received dates were identified for cancelled purchase orders.
- Purchase-order header totals reconcile with line-item totals within the checked tolerance.

## Current Limitations
Some data quality issues remain unresolved. Inventory and transaction-related findings should be treated cautiously until further validation is completed.

## Next Steps
- Investigate inventory and transaction discrepancies.
- Continue building Power BI dashboards.
- Refine the analysis and document verified findings.

## Project Type
Individual project
