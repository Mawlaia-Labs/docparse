# docparse

LLM-powered document extraction SDK. Extract structured data from PDFs, invoices, contracts, and any custom schema — in two lines of Python.

```python
from docparse import LLMExtractor, load, INVOICE_SCHEMA

layout = load("invoice.pdf")                        # or from_text("...")
result = LLMExtractor().extract(layout, INVOICE_SCHEMA)

print(result.get("total_amount"))        # 1500.0
print(result.confidence("vendor_name"))  # 0.97
```

## Installation

```bash
pip install docparse                # core (text files only)
pip install "docparse[pdf]"         # + PDF support via pdfplumber
pip install "docparse[openai]"      # + OpenAI provider
pip install "docparse[anthropic]"   # + Anthropic provider
pip install "docparse[all]"         # everything
```

## Quickstart

```python
from docparse import LLMExtractor, from_text, INVOICE_SCHEMA

layout = from_text("""
INVOICE #INV-2024-042
Vendor: Acme Corp
Date: 2024-03-15
Total: $1,500.00
""")

extractor = LLMExtractor(model="gpt-4o-mini", provider="openai")
result = extractor.extract(layout, INVOICE_SCHEMA)

for field_name in INVOICE_SCHEMA.field_names():
    value = result.get(field_name)
    conf  = result.confidence(field_name)
    if value is not None:
        print(f"{field_name}: {value}  (confidence: {conf:.0%})")
```

## Built-in schemas

| Schema constant           | Key                | Fields |
|---------------------------|--------------------|--------|
| `INVOICE_SCHEMA`          | `invoice`          | 12 fields — amounts, dates, vendor, line items |
| `LOAN_APPLICATION_SCHEMA` | `loan_application` | 12 fields — borrower, amounts, property |
| `W2_SCHEMA`               | `w2`               | 8 fields — employer, wages, withholdings |
| `NDA_SCHEMA`              | `nda`              | 8 fields — parties, term, jurisdiction |
| `CONTRACT_SCHEMA`         | `contract`         | 9 fields — parties, dates, obligations |

Access any by key: `from docparse import REGISTRY; schema = REGISTRY["invoice"]`

## Custom schemas

```python
from docparse import ExtractionSchema, FieldSpec, LLMExtractor, from_text

schema = ExtractionSchema(name="purchase_order", fields=[
    FieldSpec(name="po_number",     description="PO number",         required=True),
    FieldSpec(name="total",         description="Total amount",       type="number", required=True, example="4200.00"),
    FieldSpec(name="delivery_date", description="Expected delivery",  type="date"),
])

result = LLMExtractor().extract(from_text(po_text), schema)
missing = result.missing_required(schema)
```

## CLI

```bash
docparse extract invoice.pdf --schema invoice
docparse extract contract.txt --schema nda --json
docparse schemas          # list available schemas
```

## Providers

```python
# OpenAI (default)
LLMExtractor(model="gpt-4o-mini", provider="openai")

# Anthropic
LLMExtractor(model="claude-3-5-haiku-20241022", provider="anthropic")
```

## License

MIT © [Mawlaia](https://mawlaia.com)
