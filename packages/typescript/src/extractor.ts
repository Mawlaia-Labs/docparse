import {
  DocumentLayout,
  ExtractionSchema,
  ExtractionResult,
  clampedFieldValue,
  pageCount,
  promptLines,
} from "./models";

const EXTRACT_PROMPT = `\
You are an expert document extraction assistant. Extract structured data from the document text below.

DOCUMENT TEXT:
{text}

SCHEMA — extract these fields:
{fields}

Return ONLY valid JSON in exactly this format (no markdown, no explanation):
{
  "fields": {
    "<field_name>": {
      "value": <extracted_value_or_null>,
      "confidence": <float_0.0_to_1.0>,
      "raw": "<short_text_snippet_from_document>"
    }
  }
}

Rules:
- confidence 0.9–1.0: value clearly stated in document
- confidence 0.5–0.9: value inferred or partially stated
- confidence 0.0–0.5: value guessed or not found (set value to null)
- For missing fields, use null with confidence 0.0
- For dates, use ISO 8601 format (YYYY-MM-DD)
- For numbers, return numeric type (not string)
- For booleans, return true/false
`;

const JSON_RE = /\{[\s\S]*\}/;

export interface LLMExtractorOptions {
  model?:    string;
  provider?: "openai" | "anthropic";
  maxChars?: number;
}

export class LLMExtractor {
  readonly model:    string;
  readonly provider: "openai" | "anthropic";
  readonly maxChars: number;
  private  _client:  unknown = null;

  constructor(opts: LLMExtractorOptions = {}) {
    this.model    = opts.model    ?? "gpt-4o-mini";
    this.provider = opts.provider ?? "openai";
    this.maxChars = opts.maxChars ?? 12_000;
  }

  private async _getClient(): Promise<unknown> {
    if (this._client) return this._client;
    if (this.provider === "openai") {
      const { OpenAI } = await import("openai");
      this._client = new OpenAI();
    } else {
      const Anthropic = await import("@anthropic-ai/sdk");
      this._client = new Anthropic.default();
    }
    return this._client;
  }

  async _call(prompt: string): Promise<string> {
    const client = await this._getClient();
    if (this.provider === "openai") {
      const openai = client as import("openai").OpenAI;
      const resp   = await openai.chat.completions.create({
        model:           this.model,
        messages:        [{ role: "user", content: prompt }],
        temperature:     0,
        response_format: { type: "json_object" },
      });
      return resp.choices[0]?.message?.content ?? "";
    } else {
      const anthropic = client as import("@anthropic-ai/sdk").default;
      const resp      = await anthropic.messages.create({
        model:      this.model,
        max_tokens: 2048,
        messages:   [{ role: "user", content: prompt }],
      });
      const block = resp.content[0];
      return block && "text" in block ? block.text : "";
    }
  }

  async extract(layout: DocumentLayout, schema: ExtractionSchema): Promise<ExtractionResult> {
    const text   = layout.totalText.slice(0, this.maxChars);
    const prompt = EXTRACT_PROMPT
      .replace("{text}",   text)
      .replace("{fields}", promptLines(schema));
    const raw    = await this._call(prompt);
    return this._parseResponse(raw, schema, pageCount(layout));
  }

  _parseResponse(raw: string, schema: ExtractionSchema, pages = 1): ExtractionResult {
    let fields: Record<string, unknown> = {};
    try {
      const data = JSON.parse(raw) as Record<string, unknown>;
      fields     = (data["fields"] ?? {}) as Record<string, unknown>;
    } catch {
      const m = JSON_RE.exec(raw);
      if (m) {
        try {
          const data = JSON.parse(m[0]) as Record<string, unknown>;
          fields     = (data["fields"] ?? {}) as Record<string, unknown>;
        } catch {
          fields = {};
        }
      }
    }

    const fvMap: ExtractionResult["fields"] = {};
    for (const spec of schema.fields) {
      const entry = fields[spec.name];
      if (entry && typeof entry === "object" && !Array.isArray(entry)) {
        const e    = entry as Record<string, unknown>;
        fvMap[spec.name] = clampedFieldValue(
          e["value"] ?? null,
          typeof e["confidence"] === "number" ? e["confidence"] : 0,
          typeof e["raw"] === "string"         ? e["raw"]        : "",
        );
      } else {
        fvMap[spec.name] = clampedFieldValue(null, 0);
      }
    }

    return { schemaName: schema.name, fields: fvMap, pageCount: pages };
  }
}
