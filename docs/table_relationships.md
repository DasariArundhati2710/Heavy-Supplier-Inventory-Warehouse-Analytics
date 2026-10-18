
# Table Relationships

## Sales
- sales_orders_header connects to sales_orders_lines using sales_order_id.
- sales_orders_lines connects to products using product_id.
- sales_orders_header connects to customers using customer_id.
- sales_orders_header connects to branches using branch_id.

## Purchasing
- purchase_orders_header connects to purchase_orders_lines using po_id.
- purchase_orders_header connects to suppliers using supplier_id.
- purchase_orders_lines connects to products using product_id.

## Inventory
- inventory_master connects to products using product_id.
- inventory_master connects to branches using branch_id.
- stock_ledger connects to products using product_id.
- stock_ledger connects to branches using branch_id.

## Invoices and Payments
- invoices and payments may connect through invoice_id, subject to duplicate-ID and key validation.

## Validation Notes
Confirm the exact column names and key uniqueness in the source datasets before creating relationships in Power BI.
