import {
  INVOICE_SCHEMA,
  LOAN_APPLICATION_SCHEMA,
  W2_SCHEMA,
  NDA_SCHEMA,
  CONTRACT_SCHEMA,
  REGISTRY,
} from "../src/schemas";
import { fieldNames, promptLines } from "../src/models";

const VALID_TYPES = new Set(["string", "number", "date", "boolean", "list"]);

describe("REGISTRY", () => {
  it("has all 5 keys", () => {
    expect(new Set(Object.keys(REGISTRY))).toEqual(
      new Set(["invoice", "loan_application", "w2", "nda", "contract"]),
    );
  });
});

describe("INVOICE_SCHEMA", () => {
  it("has at least 10 fields", () => {
    expect(INVOICE_SCHEMA.fields.length).toBeGreaterThanOrEqual(10);
  });

  it("includes line_items", () => {
    expect(fieldNames(INVOICE_SCHEMA)).toContain("line_items");
  });

  it("includes currency", () => {
    expect(fieldNames(INVOICE_SCHEMA)).toContain("currency");
  });

  it("has at least one required field", () => {
    const required = INVOICE_SCHEMA.fields.filter((f) => f.required);
    expect(required.length).toBeGreaterThan(0);
  });
});

describe("LOAN_APPLICATION_SCHEMA", () => {
  it("has at least 8 fields", () => {
    expect(LOAN_APPLICATION_SCHEMA.fields.length).toBeGreaterThanOrEqual(8);
  });

  it("includes borrower_name", () => {
    expect(fieldNames(LOAN_APPLICATION_SCHEMA)).toContain("borrower_name");
  });

  it("includes a loan amount field", () => {
    const names = fieldNames(LOAN_APPLICATION_SCHEMA);
    expect(names.some((n) => n.includes("loan") && n.includes("amount"))).toBe(true);
  });
});

describe("W2_SCHEMA", () => {
  it("has at least 6 fields", () => {
    expect(W2_SCHEMA.fields.length).toBeGreaterThanOrEqual(6);
  });

  it("includes a wages field", () => {
    const names = fieldNames(W2_SCHEMA);
    expect(names.some((n) => n.includes("wage") || n.includes("income"))).toBe(true);
  });

  it("includes an employer field", () => {
    const names = fieldNames(W2_SCHEMA);
    expect(names.some((n) => n.includes("employer"))).toBe(true);
  });
});

describe("NDA_SCHEMA", () => {
  it("has at least 6 fields", () => {
    expect(NDA_SCHEMA.fields.length).toBeGreaterThanOrEqual(6);
  });

  it("includes party fields", () => {
    const names = fieldNames(NDA_SCHEMA);
    expect(names.some((n) => n.includes("party") || n.includes("disclos"))).toBe(true);
  });
});

describe("CONTRACT_SCHEMA", () => {
  it("has at least 7 fields", () => {
    expect(CONTRACT_SCHEMA.fields.length).toBeGreaterThanOrEqual(7);
  });

  it("includes date fields", () => {
    const names = fieldNames(CONTRACT_SCHEMA);
    expect(names.some((n) => n.includes("date") || n.includes("effective"))).toBe(true);
  });
});

describe("all schemas", () => {
  Object.entries(REGISTRY).forEach(([key, schema]) => {
    it(`${key}: all fields have descriptions`, () => {
      schema.fields.forEach((f) => {
        expect(f.description).toBeTruthy();
      });
    });

    it(`${key}: all fields have valid types`, () => {
      schema.fields.forEach((f) => {
        expect(VALID_TYPES).toContain(f.type);
      });
    });

    it(`${key}: promptLines includes all field names`, () => {
      const lines = promptLines(schema);
      schema.fields.forEach((f) => {
        expect(lines).toContain(f.name);
      });
    });
  });
});
