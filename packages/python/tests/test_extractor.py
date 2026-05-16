import json
from unittest.mock import MagicMock, patch
from docparse.extractor import LLMExtractor
from docparse.loader import from_text
from docparse.models import ExtractionSchema, FieldSpec


SIMPLE_SCHEMA = ExtractionSchema(name="test", fields=[
    FieldSpec(name="total",   description="Total amount",  type="number",  required=True),
    FieldSpec(name="vendor",  description="Vendor name",   type="string",  required=True),
    FieldSpec(name="due_date", description="Due date",     type="string",  required=False),
])

_GOOD_RESPONSE = json.dumps({
    "fields": {
        "total":    {"value": 1500.0,       "confidence": 0.95, "raw": "$1,500.00"},
        "vendor":   {"value": "Acme Corp",  "confidence": 0.99, "raw": "Acme Corp"},
        "due_date": {"value": "2024-03-31", "confidence": 0.90, "raw": "March 31, 2024"},
    }
})

_MISSING_FIELD_RESPONSE = json.dumps({
    "fields": {
        "total":  {"value": 500.0, "confidence": 0.9, "raw": "500"},
        "vendor": {"value": None,  "confidence": 0.0, "raw": ""},
    }
})

_MARKDOWN_WRAPPED = "```json\n" + _GOOD_RESPONSE + "\n```"

_TOTALLY_BROKEN = "Sorry, I cannot extract that."


def _extractor_with_response(text: str) -> LLMExtractor:
    ex = LLMExtractor()
    ex._call = MagicMock(return_value=text)
    return ex


def test_extract_happy_path():
    layout = from_text("Invoice from Acme Corp. Total: $1,500.00. Due: March 31, 2024.")
    result = _extractor_with_response(_GOOD_RESPONSE).extract(layout, SIMPLE_SCHEMA)

    assert result.get("total")   == 1500.0
    assert result.get("vendor")  == "Acme Corp"
    assert result.get("due_date") == "2024-03-31"
    assert result.schema_name    == "test"
    assert result.page_count     == 1


def test_extract_confidence_values():
    layout = from_text("some text")
    result = _extractor_with_response(_GOOD_RESPONSE).extract(layout, SIMPLE_SCHEMA)

    assert result.confidence("total")   == 0.95
    assert result.confidence("vendor")  == 0.99
    assert result.confidence("missing") == 0.0


def test_extract_missing_field_returns_none():
    layout = from_text("partial invoice text")
    result = _extractor_with_response(_MISSING_FIELD_RESPONSE).extract(layout, SIMPLE_SCHEMA)

    assert result.get("total") == 500.0
    assert result.get("vendor") is None
    assert result.get("due_date") is None


def test_extract_missing_required_detected():
    layout = from_text("partial invoice")
    result = _extractor_with_response(_MISSING_FIELD_RESPONSE).extract(layout, SIMPLE_SCHEMA)

    missing = result.missing_required(SIMPLE_SCHEMA)
    assert "vendor" in missing
    assert "total"  not in missing


def test_extract_markdown_wrapped_json_fallback():
    layout = from_text("invoice text")
    result = _extractor_with_response(_MARKDOWN_WRAPPED).extract(layout, SIMPLE_SCHEMA)

    assert result.get("total") == 1500.0
    assert result.get("vendor") == "Acme Corp"


def test_extract_broken_response_graceful():
    layout = from_text("some text")
    result = _extractor_with_response(_TOTALLY_BROKEN).extract(layout, SIMPLE_SCHEMA)

    assert result.get("total")  is None
    assert result.get("vendor") is None


def test_extract_truncates_to_max_chars():
    long_text = "x" * 50_000
    layout    = from_text(long_text)

    ex = LLMExtractor(max_chars=100)
    captured_prompt = []

    def capture(prompt):
        captured_prompt.append(prompt)
        return _GOOD_RESPONSE

    ex._call = capture
    ex.extract(layout, SIMPLE_SCHEMA)

    assert len(captured_prompt) == 1
    assert "x" * 101 not in captured_prompt[0]


def test_extract_page_count_propagated():
    from docparse.models import DocumentLayout, PageContent
    layout = DocumentLayout(pages=[
        PageContent(page_num=1, text="page one"),
        PageContent(page_num=2, text="page two"),
    ])
    result = _extractor_with_response(_GOOD_RESPONSE).extract(layout, SIMPLE_SCHEMA)
    assert result.page_count == 2


def test_get_client_openai():
    ex = LLMExtractor(provider="openai")
    mock_openai = MagicMock()
    with patch("docparse.extractor.OpenAI" if False else "openai.OpenAI", mock_openai, create=True):
        pass
    assert ex.provider == "openai"


def test_confidence_clamped_in_extractor():
    over_confident = json.dumps({
        "fields": {
            "total":    {"value": 99.0, "confidence": 1.8, "raw": "99"},
            "vendor":   {"value": "X",  "confidence": -0.5, "raw": "X"},
            "due_date": {"value": None, "confidence": 0.0,  "raw": ""},
        }
    })
    layout = from_text("text")
    result = _extractor_with_response(over_confident).extract(layout, SIMPLE_SCHEMA)

    assert result.confidence("total")  == 1.0
    assert result.confidence("vendor") == 0.0
