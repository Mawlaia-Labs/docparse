import { ExtractionSchema, makeField } from "../models";

export const INVOICE_SCHEMA: ExtractionSchema = {
  name: "invoice",
  fields: [
    makeField("invoice_number",  "Unique invoice identifier",                  { required: true,  example: "INV-2024-042" }),
    makeField("invoice_date",    "Date the invoice was issued",                 { type: "date",    required: true,  example: "2024-03-15" }),
    makeField("due_date",        "Payment due date",                            { type: "date",    example: "2024-04-15" }),
    makeField("vendor_name",     "Name of the vendor or seller",                { required: true }),
    makeField("vendor_address",  "Full address of the vendor"),
    makeField("client_name",     "Name of the client or buyer",                 { required: true }),
    makeField("subtotal",        "Subtotal before tax",                         { type: "number",  example: "1250.00" }),
    makeField("tax_amount",      "Tax amount",                                  { type: "number",  example: "250.00" }),
    makeField("total_amount",    "Total amount due including tax",              { type: "number",  required: true, example: "1500.00" }),
    makeField("currency",        "Currency code",                               { example: "USD" }),
    makeField("payment_terms",   "Payment terms or conditions",                 { example: "Net 30" }),
    makeField("line_items",      "List of line items as JSON array",            { type: "list" }),
  ],
};

export const LOAN_APPLICATION_SCHEMA: ExtractionSchema = {
  name: "loan_application",
  fields: [
    makeField("borrower_name",      "Full name of the primary borrower",        { required: true }),
    makeField("co_borrower_name",   "Full name of co-borrower if present"),
    makeField("loan_amount",        "Requested loan amount",                    { type: "number",  required: true, example: "350000" }),
    makeField("loan_purpose",       "Purpose of the loan",                      { example: "home purchase" }),
    makeField("property_address",   "Address of the property"),
    makeField("property_value",     "Estimated property value",                 { type: "number",  example: "425000" }),
    makeField("annual_income",      "Borrower annual income",                   { type: "number",  example: "95000" }),
    makeField("employment_status",  "Employment status of borrower"),
    makeField("credit_score",       "Borrower credit score",                    { type: "number",  example: "740" }),
    makeField("loan_term_years",    "Requested loan term in years",             { type: "number",  example: "30" }),
    makeField("interest_rate",      "Proposed or quoted interest rate",         { type: "number",  example: "6.75" }),
    makeField("application_date",   "Date the application was submitted",       { type: "date" }),
  ],
};

export const W2_SCHEMA: ExtractionSchema = {
  name: "w2",
  fields: [
    makeField("employer_name",       "Name of employer",                        { required: true }),
    makeField("employer_ein",        "Employer Identification Number",          { example: "12-3456789" }),
    makeField("employee_name",       "Name of employee",                        { required: true }),
    makeField("employee_ssn_last4",  "Last 4 digits of employee SSN",           { example: "1234" }),
    makeField("wages_tips",          "Total wages, tips and other compensation",{ type: "number", required: true, example: "85000.00" }),
    makeField("federal_tax_withheld","Federal income tax withheld",             { type: "number", example: "12750.00" }),
    makeField("social_security_wages","Social security wages",                  { type: "number", example: "85000.00" }),
    makeField("tax_year",            "Tax year for this W-2",                   { example: "2023" }),
  ],
};

export const NDA_SCHEMA: ExtractionSchema = {
  name: "nda",
  fields: [
    makeField("disclosing_party",    "Party disclosing confidential information", { required: true }),
    makeField("receiving_party",     "Party receiving confidential information",  { required: true }),
    makeField("effective_date",      "Date the NDA becomes effective",            { type: "date", required: true }),
    makeField("expiration_date",     "Date the NDA expires",                      { type: "date" }),
    makeField("term_years",          "Duration of confidentiality obligation in years", { type: "number", example: "2" }),
    makeField("jurisdiction",        "Governing law and jurisdiction",            { example: "State of California" }),
    makeField("purpose",             "Purpose of the disclosure"),
    makeField("exceptions",          "Exceptions to confidentiality obligations"),
  ],
};

export const CONTRACT_SCHEMA: ExtractionSchema = {
  name: "contract",
  fields: [
    makeField("party_a",             "First contracting party",                  { required: true }),
    makeField("party_b",             "Second contracting party",                 { required: true }),
    makeField("effective_date",      "Contract effective date",                  { type: "date", required: true }),
    makeField("expiration_date",     "Contract expiration date",                 { type: "date" }),
    makeField("contract_value",      "Total value or consideration",             { type: "number" }),
    makeField("payment_schedule",    "Payment schedule or milestones"),
    makeField("governing_law",       "Governing law and jurisdiction"),
    makeField("termination_clause",  "Conditions under which contract may be terminated"),
    makeField("renewal_terms",       "Auto-renewal or extension terms"),
  ],
};

export const REGISTRY: Record<string, ExtractionSchema> = {
  invoice:          INVOICE_SCHEMA,
  loan_application: LOAN_APPLICATION_SCHEMA,
  w2:               W2_SCHEMA,
  nda:              NDA_SCHEMA,
  contract:         CONTRACT_SCHEMA,
};
