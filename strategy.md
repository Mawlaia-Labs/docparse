# Document Understanding & Structured Extraction — Strategy & Development Plan

*Opportunity #8 from infrastructure_opportunities.md*
*"The LLM-powered back-office extraction API"*

---

## 1. Market Opportunity

### Problem
Every back-office process — insurance claims, loan underwriting, healthcare intake, legal review, accounting, customs clearance, KYC, government procurement — starts with a stack of unstructured documents. Traditional OCR + template engines were brittle, expensive, and required months of configuration per document type. LLMs unlock a clean, generic solution — but no developer-first API has captured this market yet.

### Market size
- Back-office document processing is a $40B+ TAM across verticals.
- Mortgage lending alone: ~$1.5 trillion in annual US originations, each requiring 200–500 pages of documents.
- Insurance: 1.5B+ claims globally per year, each starting with unstructured documents.
- Healthcare: 30B+ administrative transactions annually in the US alone.
- Realistic SOM at 3 years (developer-first wedge): 200–1000 paying companies × €500–10K/month = €1.2M–120M ARR.

### Forcing functions
- **LLMs make generic extraction viable for the first time** — no more brittle templates per document type
- **Digitization mandates** — EU Digital Single Market, US digital-first government requirements
- **Back-office cost pressure** — every ops team is under pressure to reduce headcount via automation
- **AI adoption maturity** — after 2 years of AI hype, companies are now asking "where does AI actually save us money?" — document processing is the clearest answer
- **Compliance documentation** — CSRD, SOX, AML all require structured data extracted from unstructured documents

### Buyer profile
- **Primary:** Head of Operations / COO at mid-market company in lending, insurance, healthcare, legal, accounting
- **Secondary:** CTO / Head of Engineering who needs to automate an internal document workflow
- **Tertiary:** Product Manager building a product that processes customer-submitted documents
- **Budget:** €500–5000/month self-serve; €20K–100K/year enterprise ops contracts
- **Sales motion:** top-down (ops buyer has budget) + bottoms-up (engineer prototypes with API)

---

## 2. Competition Landscape

| Player | Positioning | Gap |
|---|---|---|
| **Reducto** | Developer-first document API | Early, small team, limited vertical depth |
| **Unstructured.io** | Open-source document processing pipeline | Broad but not vertically specialized, limited hosted product |
| **LlamaParse (LlamaIndex)** | Developer-friendly PDF parser for RAG | Optimized for RAG chunking, not structured extraction |
| **Sensible** | Structured data from documents, good UI | Template-based, requires configuration per doc type, limited LLM integration |
| **Docupanda** | Very early stage | Limited ecosystem |
| **AWS Textract** | OCR + form extraction | No LLM intelligence, brittle templates, AWS lock-in |
| **Azure Document Intelligence** | OCR + structured extraction | Azure lock-in, complex pricing, limited customization |
| **Google Document AI** | OCR + classification | GCP lock-in, enterprise pricing |
| **Adobe Extract API** | PDF content extraction | No structured extraction, no LLM, limited to Adobe formats |
| **Hyperscience** | Enterprise intelligent document processing | Very expensive, enterprise-only, long implementation |

### Competitive gap
No product offers: **open-source layout parser + LLM-powered schema-based extraction + vertical packs with pre-built schemas + correction interface + data flywheel**, packaged as a developer-first API with per-page pricing. The market is split between "good OCR with no intelligence" (hyperscalers) and "good LLM integration with no verticals" (Reducto, LlamaParse).

### Defensibility
- **Correction flywheel:** customer corrections (human-in-the-loop) fine-tune extraction models → accuracy improves → switching cost builds
- **Vertical schemas:** pre-built extraction schemas for loan docs, ACORD forms, HCFA-1500 forms, legal contracts — months of domain work to replicate
- **Operations buyer lock-in:** once ops workflows are automated through your API, switching requires re-validation of every document type
- **Data moat:** aggregate extraction patterns across verticals improve accuracy for all customers

---

## 3. Customer Needs Map

### Jobs to be done
1. **"We process 500 loan applications/day — extract 40 fields from each manually"** — batch extraction with high accuracy
2. **"Our insurance claims intake team manually re-keys data from ACORD forms"** — structured extraction with confidence scores
3. **"We're building a KYC product that needs to extract data from passports + bank statements"** — identity document extraction
4. **"Our lawyers spend 4 hours per contract extracting key clauses"** — legal contract extraction
5. **"We need to import vendor invoices into our ERP automatically"** — invoice/PO extraction

### Document taxonomy by vertical

**Mortgage/Lending:**
- 1003 loan application, W-2, 1040 tax return, pay stubs, bank statements, appraisal reports

**Insurance:**
- ACORD forms (25, 125, 130, 140), claims forms, loss run reports, certificates of insurance

**Healthcare:**
- HCFA-1500 (medical claims), UB-04 (hospital claims), EOBs, referral letters, discharge summaries

**Legal:**
- Contracts (NDA, MSA, SOW), court filings, due diligence packages, regulatory submissions

**Accounting/Finance:**
- Invoices, purchase orders, receipts, bank statements, financial statements

### Integration points
- REST API: `POST /v1/extract` with document URL or base64, schema definition, returns JSON
- Webhook: async processing for large documents
- SDK: Python + TypeScript
- ERP connectors: NetSuite, QuickBooks, Sage (Phase 3)
- Storage: S3/GCS/Azure Blob input support

### Must-have on day one
- PDF, scanned image (JPEG/PNG/TIFF), multi-page support
- Schema-based extraction: define the fields you want, get structured JSON back
- Confidence scores per field
- Layout parsing: tables, multi-column, forms, checkboxes
- Free tier: first 100 pages/month free

---

## 4. Staged Development Plan

### Phase 0 — Open-source layout parser (weeks 1–4)
**Goal:** establish technical credibility, start design partner conversations

- [ ] Open-source `docparse` or similar — layout analysis library for PDFs and scanned images
- [ ] Capabilities: table detection + extraction, multi-column layout, form field detection, checkboxes
- [ ] Python library: `parse_document(path) → DocumentLayout` with pages, blocks, tables, forms
- [ ] Benchmark: accuracy on DocBank, PubLayNet, FUNSD datasets vs Unstructured.io
- [ ] Blog post: "Why existing PDF parsers fail for LLM extraction" + performance comparison
- [ ] Publish: GitHub, PyPI, HN Show HN

**Success metric:** 200+ GitHub stars, 5 design partner conversations started (mortgage lenders, insurance ops)

---

### Phase 1 — Extraction API + first vertical pack (months 1–3)
**Goal:** first paying customers in one vertical

- [ ] Hosted extraction API: `POST /v1/extract` → JSON with confidence scores
- [ ] Schema definition: Pydantic-style schema or JSON Schema input
- [ ] LLM extraction layer: GPT-4o-mini for standard docs, GPT-4o for complex layouts
- [ ] **Vertical Pack #1: Mortgage Loan Documents**
  - Pre-built schemas for: 1003 application, W-2, 1040 tax return, pay stubs, bank statements
  - Pre-tuned prompts for each document type
  - Accuracy benchmarks on public mortgage doc datasets
- [ ] Per-page pricing: €0.05/page for standard, €0.15/page for complex (tables, multi-column)
- [ ] Async API + webhook for batch processing
- [ ] Free tier: 100 pages/month
- [ ] Onboard 5–10 design partners from mortgage/lending space

**Success metric:** 5 paying customers, €2K–5K MRR (ops buyers pay per-page at volume)

---

### Phase 2 — Correction interface + second vertical (months 3–6)
**Goal:** build the data flywheel, expand TAM

- [ ] Human-in-the-loop correction interface: review extracted fields, correct errors, validate
- [ ] Correction-to-fine-tuning pipeline: corrections feed back into prompt refinement
- [ ] Confidence threshold routing: high-confidence → auto-accept, low-confidence → human review queue
- [ ] **Vertical Pack #2: Insurance (ACORD Forms)**
  - Pre-built schemas for ACORD 25, 125, 130, 140
  - Certificate of insurance extraction
  - Loss run report parsing
- [ ] Batch processing dashboard: upload 500 docs, monitor progress, download results CSV
- [ ] SOC 2 Type I started
- [ ] Enterprise tier: €999+/month, dedicated model fine-tuning, SLA

**Success metric:** 30–80 paying customers, €10K–20K MRR

---

### Phase 3 — Healthcare vertical + HIPAA (months 6–12)
**Goal:** enter healthcare — highest willingness to pay

- [ ] HIPAA BAA available
- [ ] PHI handling: tokenize PHI before it leaves customer environment (integrate with PII Vault #2)
- [ ] **Vertical Pack #3: Healthcare (Medical Claims)**
  - HCFA-1500, UB-04, EOB, referral letters, prior authorization forms
  - ICD-10/CPT code extraction
  - Insurance coverage verification form parsing
- [ ] SOC 2 Type II
- [ ] Accuracy guarantee tier: SLA on per-field accuracy for specific document types (backed by human review fallback)
- [ ] ERP connectors: NetSuite invoice import, QuickBooks bill creation from invoices
- [ ] Seed raise: target €2–4M

**Success metric:** 100–200 paying customers, €30–60K MRR

---

### Phase 4 — Platform (months 12–24)
**Goal:** become the developer-grade document understanding platform

- [ ] **Vertical Pack #4: Legal contracts** — NDA/MSA clause extraction, obligation tracking, date extraction
- [ ] **Vertical Pack #5: Invoices/POs** — universal invoice parsing across formats
- [ ] Custom vertical builder: let customers define their own document types + schemas without code
- [ ] Model fine-tuning: train customer-specific models on their corrected extraction data
- [ ] On-premise deployment option (financial enterprise requirement)
- [ ] ISO 27001
- [ ] Series A raise

---

## 5. Zero-to-revenue path (bootstrap)

**Week 1–4:** open-source layout parser → GitHub traction → outreach to 20 mortgage lenders
**Month 2:** hosted API + mortgage pack live → 3–5 design partners at €0.05/page
**Month 3:** typical lender doing 500 loans/month × 20 pages = 10K pages → €500/month × 5 customers = €2.5K MRR
**Month 4–5:** 20 customers (mix mortgage + insurance), €8K MRR → insurance ACORD pack launched
**Month 6:** €15K MRR → SOC 2 started → healthcare conversations begin

**Infrastructure cost at €15K MRR:** ~€2K–4K/month (LLM API costs are the main variable — manage with caching and model routing)

**Key insight on unit economics:** LLM cost is the main cost driver. GPT-4o at $0.01/1K tokens processes ~1 page in ~1K tokens = $0.01/page cost. Sell at €0.05/page = 5x gross margin. Cache repeated document type schemas to reduce token usage.

---

## 6. Tech stack recommendation

- **Layout parsing:** PyMuPDF + custom table detection (or fine-tuned LayoutLM) for open-source layer
- **LLM extraction:** GPT-4o-mini (cost) → GPT-4o (accuracy) routing by confidence
- **Backend:** FastAPI + Postgres + S3
- **Queue:** Celery + Redis for async document processing
- **Frontend:** Next.js on Vercel
- **SDKs:** Python (primary — ops/engineering buyers use Python) + TypeScript
- **Inference cost management:** prompt caching (Anthropic/OpenAI), schema reuse, small model pre-filtering

### Synergy with #2 PII Vault
Documents often contain PII (patient data, financial data, personal information). Routing extracted values through PII Vault tokenization before storing gives customers HIPAA/GDPR compliance automatically. Natural bundle: Document Understanding for extraction + PII Vault for storage compliance.

---

*Last updated: 2026-05-15*
