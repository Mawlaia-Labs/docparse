# docparse

> Document layout parser and structured extraction.

**docparse** extracts structured data from PDFs, scanned forms, and mixed-format documents — tables, multi-column layouts, checkboxes — ready to pipe into LLMs or your own pipelines.

```python
from docparse import parse_document, extract

doc = parse_document("loan_application.pdf")

# Use a schema to extract exactly the fields you need
data = extract(doc, schema={
    "applicant_name": "string",
    "annual_income": "number",
    "employment_status": "string",
    "loan_amount_requested": "number",
})

# {'applicant_name': 'Jane Doe', 'annual_income': 95000, ...}
```

## Status

🚧 **Early development.** Star to follow progress.

## What it does

- **Layout parsing** — tables, multi-column, forms, checkboxes from any PDF or scanned image
- **Schema-based extraction** — define the fields you want, get structured JSON back
- **Confidence scores** — per-field confidence, route low-confidence fields to human review
- **Async + webhooks** — batch processing for high-volume pipelines
- **Vertical packs** — pre-built schemas for mortgage docs, insurance forms, medical claims, invoices

## Roadmap

- [ ] Python library
- [ ] Table detection benchmark
- [ ] Schema-based extraction API
- [ ] Vertical pack: mortgage documents
- [ ] Vertical pack: insurance (ACORD forms)
- [ ] Hosted service ([mawlaia.com](https://mawlaia.com))
- [ ] HIPAA BAA

## License

MIT
