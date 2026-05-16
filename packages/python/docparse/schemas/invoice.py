from ..models import ExtractionSchema, FieldSpec

INVOICE_SCHEMA = ExtractionSchema(
    name="invoice",
    fields=[
        FieldSpec(name="invoice_number",   type="string",  required=True,  description="Invoice number or ID",             example="INV-2024-001"),
        FieldSpec(name="invoice_date",     type="date",    required=True,  description="Date the invoice was issued",       example="2024-03-15"),
        FieldSpec(name="due_date",         type="date",    required=False, description="Payment due date"),
        FieldSpec(name="vendor_name",      type="string",  required=True,  description="Name of the vendor or supplier"),
        FieldSpec(name="vendor_address",   type="string",  required=False, description="Full address of the vendor"),
        FieldSpec(name="client_name",      type="string",  required=False, description="Name of the billed client"),
        FieldSpec(name="subtotal",         type="number",  required=False, description="Subtotal before tax",               example="1250.00"),
        FieldSpec(name="tax_amount",       type="number",  required=False, description="Tax or VAT amount"),
        FieldSpec(name="total_amount",     type="number",  required=True,  description="Total amount due",                  example="1500.00"),
        FieldSpec(name="currency",         type="string",  required=False, description="Currency code",                     example="EUR"),
        FieldSpec(name="payment_terms",    type="string",  required=False, description="Payment terms",                     example="Net 30"),
        FieldSpec(name="line_items",       type="list",    required=False, description="List of line items as strings"),
    ],
)
