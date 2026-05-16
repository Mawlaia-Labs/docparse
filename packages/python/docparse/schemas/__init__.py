from .invoice  import INVOICE_SCHEMA
from .mortgage import LOAN_APPLICATION_SCHEMA, W2_SCHEMA
from .legal    import NDA_SCHEMA, CONTRACT_SCHEMA

REGISTRY: dict[str, object] = {
    "invoice":          INVOICE_SCHEMA,
    "loan_application": LOAN_APPLICATION_SCHEMA,
    "w2":               W2_SCHEMA,
    "nda":              NDA_SCHEMA,
    "contract":         CONTRACT_SCHEMA,
}

__all__ = [
    "INVOICE_SCHEMA", "LOAN_APPLICATION_SCHEMA", "W2_SCHEMA",
    "NDA_SCHEMA", "CONTRACT_SCHEMA", "REGISTRY",
]
