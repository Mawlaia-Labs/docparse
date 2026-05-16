"""LLM-powered schema-based extraction."""
from __future__ import annotations
import json
import re
from .models import DocumentLayout, ExtractionSchema, ExtractionResult, FieldValue

_EXTRACT_PROMPT = """\
You are an expert document extraction assistant. Extract structured data from the document text below.

DOCUMENT TEXT:
{text}

SCHEMA — extract these fields:
{fields}

Return ONLY valid JSON in exactly this format (no markdown, no explanation):
{{
  "fields": {{
    "<field_name>": {{
      "value": <extracted_value_or_null>,
      "confidence": <float_0.0_to_1.0>,
      "raw": "<short_text_snippet_from_document>"
    }}
  }}
}}

Rules:
- confidence 0.9–1.0: value clearly stated in document
- confidence 0.5–0.9: value inferred or partially stated
- confidence 0.0–0.5: value guessed or not found (set value to null)
- For missing fields, use null with confidence 0.0
- For dates, use ISO 8601 format (YYYY-MM-DD)
- For numbers, return numeric type (not string)
- For booleans, return true/false
"""

_JSON_RE = re.compile(r"\{.*\}", re.DOTALL)


class LLMExtractor:
    def __init__(
        self,
        model:    str = "gpt-4o-mini",
        provider: str = "openai",
        max_chars: int = 12_000,  # ~3K tokens — keep cost low for Phase 0
    ):
        self.model     = model
        self.provider  = provider
        self.max_chars = max_chars
        self._client   = None

    def _get_client(self):
        if self._client:
            return self._client
        if self.provider == "openai":
            from openai import OpenAI
            self._client = OpenAI()
        else:
            from anthropic import Anthropic
            self._client = Anthropic()
        return self._client

    def _call(self, prompt: str) -> str:
        client = self._get_client()
        if self.provider == "openai":
            resp = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0,
                response_format={"type": "json_object"},
            )
            return resp.choices[0].message.content or ""
        else:
            resp = client.messages.create(
                model=self.model,
                max_tokens=2048,
                messages=[{"role": "user", "content": prompt}],
            )
            return resp.content[0].text if resp.content else ""

    def extract(self, layout: DocumentLayout, schema: ExtractionSchema) -> ExtractionResult:
        text   = layout.total_text[: self.max_chars]
        prompt = _EXTRACT_PROMPT.format(text=text, fields=schema.prompt_lines())
        raw    = self._call(prompt)
        return self._parse_response(raw, schema, layout.page_count)

    def _parse_response(self, raw: str, schema: ExtractionSchema, page_count: int = 1) -> ExtractionResult:
        try:
            data   = json.loads(raw)
            fields = data.get("fields", {})
        except json.JSONDecodeError:
            m = _JSON_RE.search(raw)
            if m:
                try:
                    data   = json.loads(m.group(0))
                    fields = data.get("fields", {})
                except json.JSONDecodeError:
                    fields = {}
            else:
                fields = {}

        fv_map: dict[str, FieldValue] = {}
        for spec in schema.fields:
            entry = fields.get(spec.name, {})
            if isinstance(entry, dict):
                fv_map[spec.name] = FieldValue(
                    value=entry.get("value"),
                    confidence=float(entry.get("confidence", 0.0)),
                    raw=str(entry.get("raw", "")),
                )
            else:
                fv_map[spec.name] = FieldValue(value=None, confidence=0.0)

        return ExtractionResult(
            schema_name=schema.name,
            fields=fv_map,
            page_count=page_count,
        )
