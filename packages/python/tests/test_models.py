from docparse.models import (
    FieldSpec, ExtractionSchema, FieldValue, ExtractionResult, DocumentLayout, PageContent
)


def test_field_spec_defaults():
    f = FieldSpec(name="invoice_number", description="Invoice ID")
    assert f.type     == "string"
    assert f.required is False
    assert f.example  is None


def test_extraction_schema_field_names():
    schema = ExtractionSchema(name="test", fields=[
        FieldSpec(name="a", description="field a"),
        FieldSpec(name="b", description="field b"),
    ])
    assert schema.field_names() == ["a", "b"]


def test_extraction_schema_prompt_lines():
    schema = ExtractionSchema(name="test", fields=[
        FieldSpec(name="total", description="Total amount", type="number", required=True, example="100.00"),
    ])
    lines = schema.prompt_lines()
    assert "total" in lines
    assert "number" in lines
    assert "REQUIRED" in lines
    assert "100.00" in lines


def test_field_value_confidence_clamped():
    fv = FieldValue(value="x", confidence=1.5)
    assert fv.confidence == 1.0
    fv2 = FieldValue(value="x", confidence=-0.2)
    assert fv2.confidence == 0.0


def test_extraction_result_get():
    result = ExtractionResult(
        schema_name="invoice",
        fields={"total": FieldValue(value=1500.0, confidence=0.95)},
    )
    assert result.get("total") == 1500.0
    assert result.get("missing") is None


def test_extraction_result_confidence():
    result = ExtractionResult(
        schema_name="invoice",
        fields={"total": FieldValue(value=100.0, confidence=0.9)},
    )
    assert result.confidence("total") == 0.9
    assert result.confidence("missing") == 0.0


def test_extraction_result_missing_required():
    schema = ExtractionSchema(name="test", fields=[
        FieldSpec(name="required_field", description="must have", required=True),
        FieldSpec(name="optional_field", description="nice to have", required=False),
    ])
    result = ExtractionResult(
        schema_name="test",
        fields={
            "required_field": FieldValue(value=None, confidence=0.0),
            "optional_field": FieldValue(value="present", confidence=0.9),
        },
    )
    missing = result.missing_required(schema)
    assert "required_field" in missing
    assert "optional_field" not in missing


def test_document_layout_total_text():
    layout = DocumentLayout(pages=[
        PageContent(page_num=1, text="Page one content"),
        PageContent(page_num=2, text="Page two content"),
    ])
    assert "Page one content" in layout.total_text
    assert "Page two content" in layout.total_text
    assert layout.page_count == 2


def test_document_layout_text_for_pages():
    layout = DocumentLayout(pages=[
        PageContent(page_num=1, text="first"),
        PageContent(page_num=2, text="second"),
        PageContent(page_num=3, text="third"),
    ])
    assert "second" in layout.text_for_pages(2, 2)
    assert "first"  not in layout.text_for_pages(2, 2)


def test_document_layout_all_tables():
    layout = DocumentLayout(pages=[
        PageContent(page_num=1, text="", tables=[[["h1", "h2"], ["v1", "v2"]]]),
        PageContent(page_num=2, text="", tables=[[["a", "b"]]]),
    ])
    assert len(layout.all_tables()) == 2
