from ..models import ExtractionSchema, FieldSpec

LOAN_APPLICATION_SCHEMA = ExtractionSchema(
    name="loan_application",
    fields=[
        FieldSpec(name="borrower_name",       type="string",  required=True,  description="Full name of the primary borrower"),
        FieldSpec(name="co_borrower_name",    type="string",  required=False, description="Full name of the co-borrower if any"),
        FieldSpec(name="property_address",    type="string",  required=True,  description="Address of the property being financed"),
        FieldSpec(name="loan_amount",         type="number",  required=True,  description="Requested loan amount in dollars",   example="350000"),
        FieldSpec(name="loan_purpose",        type="string",  required=False, description="Purpose of the loan",               example="Purchase"),
        FieldSpec(name="property_type",       type="string",  required=False, description="Type of property",                  example="Single Family"),
        FieldSpec(name="annual_income",       type="number",  required=False, description="Borrower's annual income"),
        FieldSpec(name="employment_status",   type="string",  required=False, description="Employment status of borrower",     example="Employed"),
        FieldSpec(name="employer_name",       type="string",  required=False, description="Name of borrower's employer"),
        FieldSpec(name="credit_score",        type="number",  required=False, description="Credit score if stated"),
        FieldSpec(name="application_date",    type="date",    required=False, description="Date the application was submitted"),
        FieldSpec(name="ssn_last4",           type="string",  required=False, description="Last 4 digits of SSN if present"),
    ],
)

W2_SCHEMA = ExtractionSchema(
    name="w2",
    fields=[
        FieldSpec(name="employee_name",       type="string",  required=True,  description="Employee's full name"),
        FieldSpec(name="employer_name",       type="string",  required=True,  description="Employer's name"),
        FieldSpec(name="tax_year",            type="string",  required=True,  description="Tax year",                         example="2023"),
        FieldSpec(name="wages",               type="number",  required=True,  description="Box 1: Wages, tips, other comp"),
        FieldSpec(name="federal_tax_withheld",type="number",  required=False, description="Box 2: Federal income tax withheld"),
        FieldSpec(name="social_security_wages",type="number", required=False, description="Box 3: Social security wages"),
        FieldSpec(name="medicare_wages",      type="number",  required=False, description="Box 5: Medicare wages"),
        FieldSpec(name="state",               type="string",  required=False, description="State abbreviation",               example="CA"),
    ],
)
