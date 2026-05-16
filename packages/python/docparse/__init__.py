"""docparse — LLM-powered document extraction."""

from .models    import (
    FieldSpec, ExtractionSchema, FieldValue, ExtractionResult,
    PageContent, DocumentLayout,
)
from .loader    import from_text, load
from .extractor import LLMExtractor
from .schemas   import REGISTRY, INVOICE_SCHEMA, LOAN_APPLICATION_SCHEMA, W2_SCHEMA, NDA_SCHEMA, CONTRACT_SCHEMA

__version__ = "0.1.0"

__all__ = [
    "FieldSpec", "ExtractionSchema", "FieldValue", "ExtractionResult",
    "PageContent", "DocumentLayout",
    "from_text", "load",
    "LLMExtractor",
    "REGISTRY", "INVOICE_SCHEMA", "LOAN_APPLICATION_SCHEMA",
    "W2_SCHEMA", "NDA_SCHEMA", "CONTRACT_SCHEMA",
]
