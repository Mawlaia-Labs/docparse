import * as fs from "fs";
import * as path from "path";
import { DocumentLayout, PageContent, makeLayout } from "./models";

export function fromText(text: string, source = "text"): DocumentLayout {
  const page: PageContent = { pageNum: 1, text, tables: [] };
  return makeLayout([page], source);
}

export function load(filePath: string): DocumentLayout {
  const ext  = path.extname(filePath).toLowerCase();
  const name = path.basename(filePath);

  if (ext === ".txt" || ext === ".md") {
    const text = fs.readFileSync(filePath, "utf-8");
    return fromText(text, name);
  }

  if (ext === ".pdf") {
    throw new Error(
      'PDF support requires the "pdf-parse" package. ' +
      'Install it: npm install pdf-parse\n' +
      'Then use loadPdf() from docparse/loader.',
    );
  }

  throw new Error(
    `Unsupported file type: ${ext}. Supported: .txt, .md (PDF support via loadPdf())`,
  );
}
