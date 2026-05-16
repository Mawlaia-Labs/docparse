import * as fs from "fs";
import * as os from "os";
import * as path from "path";
import { fromText, load } from "../src/loader";

describe("fromText", () => {
  it("creates a single-page layout", () => {
    const layout = fromText("Hello world");
    expect(layout.pages).toHaveLength(1);
    expect(layout.pages[0].text).toBe("Hello world");
    expect(layout.totalText).toBe("Hello world");
  });

  it("sets source to 'text' by default", () => {
    const layout = fromText("content");
    expect(layout.source).toBe("text");
  });

  it("uses provided source name", () => {
    const layout = fromText("content", "my-doc");
    expect(layout.source).toBe("my-doc");
  });

  it("preserves multiline text", () => {
    const text = "Line 1\nLine 2\nLine 3";
    const layout = fromText(text);
    expect(layout.pages[0].text).toBe(text);
  });
});

describe("load", () => {
  const tmp = os.tmpdir();

  it("loads a .txt file", () => {
    const p = path.join(tmp, "test_docparse.txt");
    fs.writeFileSync(p, "Invoice total: $1,500.00", "utf-8");
    const layout = load(p);
    expect(layout.totalText).toContain("Invoice total");
    fs.unlinkSync(p);
  });

  it("loads a .md file", () => {
    const p = path.join(tmp, "test_docparse.md");
    fs.writeFileSync(p, "# Contract\n\nParty: Acme Corp", "utf-8");
    const layout = load(p);
    expect(layout.totalText).toContain("Acme Corp");
    fs.unlinkSync(p);
  });

  it("throws for unsupported extension", () => {
    const p = path.join(tmp, "test_docparse.docx");
    fs.writeFileSync(p, "content");
    expect(() => load(p)).toThrow(".docx");
    fs.unlinkSync(p);
  });

  it("throws a useful message for PDF without pdf-parse", () => {
    const p = path.join(tmp, "test_docparse.pdf");
    fs.writeFileSync(p, "%PDF-1.4");
    expect(() => load(p)).toThrow("pdf-parse");
    fs.unlinkSync(p);
  });
});
