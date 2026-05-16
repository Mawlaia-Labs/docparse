from docparse.schemas import (
    INVOICE_SCHEMA, LOAN_APPLICATION_SCHEMA, W2_SCHEMA,
    NDA_SCHEMA, CONTRACT_SCHEMA, REGISTRY,
)
from docparse.models import ExtractionSchema


def test_registry_keys():
    assert set(REGISTRY.keys()) == {"invoice", "loan_application", "w2", "nda", "contract"}


def test_registry_values_are_schemas():
    for key, schema in REGISTRY.items():
        assert isinstance(schema, ExtractionSchema), f"{key} is not ExtractionSchema"


def test_invoice_schema_field_count():
    assert len(INVOICE_SCHEMA.fields) >= 10


def test_invoice_schema_required_fields():
    required = {f.name for f in INVOICE_SCHEMA.fields if f.required}
    assert "total_amount" in required or "invoice_number" in required


def test_invoice_schema_has_line_items():
    names = INVOICE_SCHEMA.field_names()
    assert "line_items" in names


def test_invoice_schema_has_currency():
    assert "currency" in INVOICE_SCHEMA.field_names()


def test_loan_application_schema_field_count():
    assert len(LOAN_APPLICATION_SCHEMA.fields) >= 8


def test_loan_application_has_key_fields():
    names = LOAN_APPLICATION_SCHEMA.field_names()
    assert "loan_amount" in names or "requested_amount" in names
    assert "borrower_name" in names


def test_w2_schema_field_count():
    assert len(W2_SCHEMA.fields) >= 6


def test_w2_schema_has_wages():
    names = W2_SCHEMA.field_names()
    assert any("wage" in n or "income" in n for n in names)


def test_w2_schema_has_employer():
    names = W2_SCHEMA.field_names()
    assert any("employer" in n for n in names)


def test_nda_schema_field_count():
    assert len(NDA_SCHEMA.fields) >= 6


def test_nda_schema_has_parties():
    names = NDA_SCHEMA.field_names()
    assert any("party" in n or "disclos" in n for n in names)


def test_contract_schema_field_count():
    assert len(CONTRACT_SCHEMA.fields) >= 7


def test_contract_schema_has_dates():
    names = CONTRACT_SCHEMA.field_names()
    assert any("date" in n or "effective" in n for n in names)


def test_all_schemas_have_descriptions():
    for schema in REGISTRY.values():
        for field in schema.fields:
            assert field.description, f"{schema.name}.{field.name} has no description"


def test_all_schemas_have_valid_types():
    valid_types = {"string", "number", "date", "boolean", "list"}
    for schema in REGISTRY.values():
        for field in schema.fields:
            assert field.type in valid_types, (
                f"{schema.name}.{field.name} has invalid type: {field.type}"
            )


def test_prompt_lines_contains_all_fields():
    for schema in REGISTRY.values():
        lines = schema.prompt_lines()
        for field in schema.fields:
            assert field.name in lines, f"{field.name} missing from {schema.name} prompt_lines"
