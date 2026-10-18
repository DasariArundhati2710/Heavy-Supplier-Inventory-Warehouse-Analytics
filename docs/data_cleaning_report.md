# Week 1 — Branch Dataset Inspection and Cleaning

## Dataset Overview
- Dataset: `branches.csv`
- Rows: 6
- Columns: 13
- Missing values: 0
- Duplicate rows: 0

## Data Quality Findings
- `warehouse_capacity` contained values such as `45230 sqft`, stored as text.
- `service_center_available` contained `Yes` and `No` values.
- No missing values or duplicate rows were found during inspection.

## Cleaning Performed
- Removed surrounding whitespace from column names.
- Converted `warehouse_capacity` into a numeric column by removing the `sqft` suffix.
- Standardised `service_center_available` text formatting.
- Saved the cleaned dataset as `data/cleaned/branches_cleaned.csv`.
- Preserved the original raw dataset.

## Initial Analysis
- Compared average monthly revenue with monthly operational costs.
- Calculated estimated monthly operating surplus/deficit and margin for each branch.
- Identified the highest- and lowest-revenue branches.

## Limitations
This dataset contains only six branch records. Findings are preliminary and should not be generalised without checking additional data. Revenue minus operational costs is an estimate, not confirmed accounting profit.

## Output Files
- `data/cleaned/branches_cleaned.csv`
- `data/cleaned/branch_performance_analysis.csv`
- `src/inspect_branches.py`
- `src/clean_branches.py`
- `src/analyze_branches.py`