import {
  makeField,
  fieldNames,
  promptLines,
  clampedFieldValue,
  getValue,
  getConfidence,
  missingRequired,
  makeLayout,
  pageCount,
  textForPages,
  allTables,
  ExtractionSchema,
  ExtractionResult,
} from "../src/models";

describe("makeField defaults", () => {
  it("sets type to string and required to false", () => {
    const f = makeField("foo", "bar");
    expect(f.type).toBe("string");
    expect(f.required).toBe(false);
    expect(f.example).toBeUndefined();
  });
});

describe("fieldNames", () => {
  it("returns names in order", () => {
    const schema: ExtractionSchema = {
      name: "test",
      fields: [makeField("a", "A"), makeField("b", "B")],
    };
    expect(fieldNames(schema)).toEqual(["a", "b"]);
  });
});

describe("promptLines", () => {
  it("includes name, type, REQUIRED, and example", () => {
    const schema: ExtractionSchema = {
      name: "test",
      fields: [makeField("total", "Total amount", { type: "number", required: true, example: "100.00" })],
    };
    const lines = promptLines(schema);
    expect(lines).toContain("total");
    expect(lines).toContain("number");
    expect(lines).toContain("REQUIRED");
    expect(lines).toContain("100.00");
  });
});

describe("clampedFieldValue", () => {
  it("clamps confidence above 1 to 1", () => {
    const fv = clampedFieldValue("x", 1.5);
    expect(fv.confidence).toBe(1);
  });

  it("clamps confidence below 0 to 0", () => {
    const fv = clampedFieldValue("x", -0.2);
    expect(fv.confidence).toBe(0);
  });
});

describe("getValue and getConfidence", () => {
  const result: ExtractionResult = {
    schemaName: "invoice",
    pageCount:  1,
    fields: {
      total: clampedFieldValue(1500, 0.95),
    },
  };

  it("getValue returns the value", () => {
    expect(getValue(result, "total")).toBe(1500);
  });

  it("getValue returns null for missing field", () => {
    expect(getValue(result, "missing")).toBeNull();
  });

  it("getConfidence returns the confidence", () => {
    expect(getConfidence(result, "total")).toBe(0.95);
  });

  it("getConfidence returns 0 for missing field", () => {
    expect(getConfidence(result, "missing")).toBe(0);
  });
});

describe("missingRequired", () => {
  const schema: ExtractionSchema = {
    name: "test",
    fields: [
      makeField("required_field", "must have", { required: true }),
      makeField("optional_field", "nice to have"),
    ],
  };

  it("detects missing required fields with null value", () => {
    const result: ExtractionResult = {
      schemaName: "test",
      pageCount:  1,
      fields: {
        required_field: clampedFieldValue(null, 0),
        optional_field: clampedFieldValue("present", 0.9),
      },
    };
    const missing = missingRequired(result, schema);
    expect(missing).toContain("required_field");
    expect(missing).not.toContain("optional_field");
  });
});

describe("makeLayout and helpers", () => {
  it("joins page text into totalText", () => {
    const layout = makeLayout([
      { pageNum: 1, text: "page one", tables: [] },
      { pageNum: 2, text: "page two", tables: [] },
    ]);
    expect(layout.totalText).toContain("page one");
    expect(layout.totalText).toContain("page two");
  });

  it("pageCount returns number of pages", () => {
    const layout = makeLayout([
      { pageNum: 1, text: "a", tables: [] },
      { pageNum: 2, text: "b", tables: [] },
    ]);
    expect(pageCount(layout)).toBe(2);
  });

  it("textForPages filters by page range", () => {
    const layout = makeLayout([
      { pageNum: 1, text: "first",  tables: [] },
      { pageNum: 2, text: "second", tables: [] },
      { pageNum: 3, text: "third",  tables: [] },
    ]);
    const text = textForPages(layout, 2, 2);
    expect(text).toContain("second");
    expect(text).not.toContain("first");
  });

  it("allTables flattens tables from all pages", () => {
    const layout = makeLayout([
      { pageNum: 1, text: "", tables: [[["h1", "h2"], ["v1", "v2"]]] },
      { pageNum: 2, text: "", tables: [[["a", "b"]]] },
    ]);
    expect(allTables(layout)).toHaveLength(2);
  });
});
