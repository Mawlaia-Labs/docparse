import { LLMExtractor } from "../src/extractor";
import { fromText } from "../src/loader";
import { makeLayout, makeField, ExtractionSchema } from "../src/models";

const SIMPLE_SCHEMA: ExtractionSchema = {
  name: "test",
  fields: [
    makeField("total",    "Total amount",  { type: "number",  required: true }),
    makeField("vendor",   "Vendor name",   { required: true }),
    makeField("due_date", "Due date",      { type: "date" }),
  ],
};

const GOOD_RESPONSE = JSON.stringify({
  fields: {
    total:    { value: 1500.0,       confidence: 0.95, raw: "$1,500.00" },
    vendor:   { value: "Acme Corp",  confidence: 0.99, raw: "Acme Corp" },
    due_date: { value: "2024-03-31", confidence: 0.90, raw: "March 31, 2024" },
  },
});

const MISSING_FIELD_RESPONSE = JSON.stringify({
  fields: {
    total:  { value: 500.0, confidence: 0.9,  raw: "500" },
    vendor: { value: null,  confidence: 0.0,  raw: "" },
  },
});

const MARKDOWN_WRAPPED = "```json\n" + GOOD_RESPONSE + "\n```";
const TOTALLY_BROKEN   = "Sorry, I cannot extract that.";

function extractorWith(response: string): LLMExtractor {
  const ex = new LLMExtractor();
  jest.spyOn(ex, "_call").mockResolvedValue(response);
  return ex;
}

describe("LLMExtractor._parseResponse", () => {
  const ex = new LLMExtractor();

  it("parses clean JSON", () => {
    const result = ex._parseResponse(GOOD_RESPONSE, SIMPLE_SCHEMA);
    expect(result.fields["total"]?.value).toBe(1500.0);
    expect(result.fields["vendor"]?.value).toBe("Acme Corp");
    expect(result.fields["due_date"]?.value).toBe("2024-03-31");
  });

  it("falls back to regex for markdown-wrapped JSON", () => {
    const result = ex._parseResponse(MARKDOWN_WRAPPED, SIMPLE_SCHEMA);
    expect(result.fields["total"]?.value).toBe(1500.0);
    expect(result.fields["vendor"]?.value).toBe("Acme Corp");
  });

  it("returns null values on totally broken response", () => {
    const result = ex._parseResponse(TOTALLY_BROKEN, SIMPLE_SCHEMA);
    expect(result.fields["total"]?.value).toBeNull();
    expect(result.fields["vendor"]?.value).toBeNull();
  });

  it("clamps overconfident values to 1.0", () => {
    const over = JSON.stringify({
      fields: { total: { value: 99, confidence: 1.8, raw: "" }, vendor: { value: "X", confidence: -0.5, raw: "" } },
    });
    const result = ex._parseResponse(over, SIMPLE_SCHEMA);
    expect(result.fields["total"]?.confidence).toBe(1);
    expect(result.fields["vendor"]?.confidence).toBe(0);
  });

  it("propagates page count", () => {
    const result = ex._parseResponse(GOOD_RESPONSE, SIMPLE_SCHEMA, 3);
    expect(result.pageCount).toBe(3);
  });
});

describe("LLMExtractor.extract", () => {
  it("returns correct values on happy path", async () => {
    const layout = fromText("Invoice from Acme Corp. Total: $1,500.00. Due: March 31, 2024.");
    const result = await extractorWith(GOOD_RESPONSE).extract(layout, SIMPLE_SCHEMA);
    expect(result.fields["total"]?.value).toBe(1500.0);
    expect(result.fields["vendor"]?.value).toBe("Acme Corp");
    expect(result.schemaName).toBe("test");
    expect(result.pageCount).toBe(1);
  });

  it("returns null for missing field", async () => {
    const layout = fromText("partial invoice");
    const result = await extractorWith(MISSING_FIELD_RESPONSE).extract(layout, SIMPLE_SCHEMA);
    expect(result.fields["vendor"]?.value).toBeNull();
    expect(result.fields["due_date"]?.value).toBeNull();
  });

  it("truncates text to maxChars", async () => {
    const longText = "x".repeat(50_000);
    const layout   = fromText(longText);
    const ex       = new LLMExtractor({ maxChars: 100 });
    const captured: string[] = [];
    jest.spyOn(ex, "_call").mockImplementation(async (prompt) => {
      captured.push(prompt);
      return GOOD_RESPONSE;
    });
    await ex.extract(layout, SIMPLE_SCHEMA);
    expect(captured[0]).not.toContain("x".repeat(101));
  });

  it("propagates multi-page page count", async () => {
    const layout = makeLayout([
      { pageNum: 1, text: "page one",  tables: [] },
      { pageNum: 2, text: "page two",  tables: [] },
    ]);
    const result = await extractorWith(GOOD_RESPONSE).extract(layout, SIMPLE_SCHEMA);
    expect(result.pageCount).toBe(2);
  });
});
