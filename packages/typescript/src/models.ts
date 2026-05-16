export type FieldType = "string" | "number" | "date" | "boolean" | "list";

export interface FieldSpec {
  name:        string;
  description: string;
  type:        FieldType;
  required:    boolean;
  example?:    string;
}

export function makeField(
  name:        string,
  description: string,
  opts: { type?: FieldType; required?: boolean; example?: string } = {},
): FieldSpec {
  return {
    name,
    description,
    type:     opts.type     ?? "string",
    required: opts.required ?? false,
    example:  opts.example,
  };
}

export interface ExtractionSchema {
  name:   string;
  fields: FieldSpec[];
}

export function fieldNames(schema: ExtractionSchema): string[] {
  return schema.fields.map((f) => f.name);
}

export function promptLines(schema: ExtractionSchema): string {
  return schema.fields
    .map((f) => {
      const req = f.required ? " (REQUIRED)" : "";
      const ex  = f.example  ? ` e.g. "${f.example}"` : "";
      return `- ${f.name} (${f.type})${req}: ${f.description}${ex}`;
    })
    .join("\n");
}

export interface FieldValue {
  value:      unknown;
  confidence: number;
  raw:        string;
}

export function clampedFieldValue(value: unknown, confidence: number, raw = ""): FieldValue {
  return { value, confidence: Math.max(0, Math.min(1, confidence)), raw };
}

export interface ExtractionResult {
  schemaName: string;
  fields:     Record<string, FieldValue>;
  pageCount:  number;
}

export function getValue(result: ExtractionResult, field: string): unknown {
  return result.fields[field]?.value ?? null;
}

export function getConfidence(result: ExtractionResult, field: string): number {
  return result.fields[field]?.confidence ?? 0;
}

export function missingRequired(result: ExtractionResult, schema: ExtractionSchema): string[] {
  return schema.fields
    .filter((f) => f.required)
    .filter((f) => {
      const fv = result.fields[f.name];
      return !fv || fv.value === null || fv.value === undefined;
    })
    .map((f) => f.name);
}

export interface PageContent {
  pageNum: number;
  text:    string;
  tables:  string[][][];
}

export interface DocumentLayout {
  source:    string;
  pages:     PageContent[];
  totalText: string;
}

export function makeLayout(pages: PageContent[], source = "unknown"): DocumentLayout {
  const totalText = pages.map((p) => p.text).join("\n\n");
  return { source, pages, totalText };
}

export function pageCount(layout: DocumentLayout): number {
  return layout.pages.length;
}

export function textForPages(layout: DocumentLayout, start: number, end?: number): string {
  const last = end ?? layout.pages.length;
  return layout.pages
    .filter((p) => p.pageNum >= start && p.pageNum <= last)
    .map((p) => p.text)
    .join("\n\n");
}

export function allTables(layout: DocumentLayout): string[][][] {
  return layout.pages.flatMap((p) => p.tables);
}
