from ..models import ExtractionSchema, FieldSpec

NDA_SCHEMA = ExtractionSchema(
    name="nda",
    fields=[
        FieldSpec(name="party_1",            type="string",  required=True,  description="First party (disclosing party) full legal name"),
        FieldSpec(name="party_2",            type="string",  required=True,  description="Second party (receiving party) full legal name"),
        FieldSpec(name="effective_date",     type="date",    required=True,  description="Date the agreement becomes effective"),
        FieldSpec(name="expiry_date",        type="date",    required=False, description="Date the agreement expires if stated"),
        FieldSpec(name="confidential_info",  type="string",  required=False, description="Description of what constitutes confidential information"),
        FieldSpec(name="jurisdiction",       type="string",  required=False, description="Governing law / jurisdiction",     example="State of California"),
        FieldSpec(name="term_years",         type="number",  required=False, description="Duration of confidentiality obligation in years"),
        FieldSpec(name="mutual",             type="boolean", required=False, description="True if mutual NDA, False if one-way"),
    ],
)

CONTRACT_SCHEMA = ExtractionSchema(
    name="contract",
    fields=[
        FieldSpec(name="contract_title",     type="string",  required=False, description="Title or type of contract"),
        FieldSpec(name="party_1",            type="string",  required=True,  description="First party full legal name"),
        FieldSpec(name="party_2",            type="string",  required=True,  description="Second party full legal name"),
        FieldSpec(name="effective_date",     type="date",    required=False, description="Effective date of the contract"),
        FieldSpec(name="expiry_date",        type="date",    required=False, description="Expiry or end date if stated"),
        FieldSpec(name="contract_value",     type="number",  required=False, description="Total contract value if stated"),
        FieldSpec(name="payment_terms",      type="string",  required=False, description="Payment schedule or terms"),
        FieldSpec(name="jurisdiction",       type="string",  required=False, description="Governing law"),
        FieldSpec(name="termination_notice", type="string",  required=False, description="Required notice period for termination"),
    ],
)
