from __future__ import annotations
from typing import Any, Literal
from pydantic import BaseModel, field_validator

FieldType = Literal["string", "number", "date", "boolean", "list"]


class FieldSpec(BaseModel):
    name:        str
    description: str
    type:        FieldType = "string"
    required:    bool      = False
    example:     str | None = None   # helps the LLM understand the expected format


class ExtractionSchema(BaseModel):
    name:   str
    fields: list[FieldSpec]

    def field_names(self) -> list[str]:
        return [f.name for f in self.fields]

    def prompt_lines(self) -> str:
        lines = []
        for f in self.fields:
            req  = " (REQUIRED)" if f.required else ""
            ex   = f' e.g. "{f.example}"' if f.example else ""
            lines.append(f"- {f.name} ({f.type}){req}: {f.description}{ex}")
        return "\n".join(lines)


class FieldValue(BaseModel):
    value:      Any
    confidence: float = 0.0
    raw:        str   = ""

    @field_validator("confidence")
    @classmethod
    def clamp(cls, v: float) -> float:
        return max(0.0, min(1.0, v))


class ExtractionResult(BaseModel):
    schema_name: str
    fields:      dict[str, FieldValue]
    page_count:  int = 1

    def get(self, field: str) -> Any:
        fv = self.fields.get(field)
        return fv.value if fv else None

    def confidence(self, field: str) -> float:
        fv = self.fields.get(field)
        return fv.confidence if fv else 0.0

    def missing_required(self, schema: ExtractionSchema) -> list[str]:
        return [
            f.name for f in schema.fields
            if f.required and (self.fields.get(f.name) is None or self.fields[f.name].value is None)
        ]


class TableCell(BaseModel):
    text:    str
    row:     int
    col:     int
    rowspan: int = 1
    colspan: int = 1


class PageContent(BaseModel):
    page_num: int
    text:     str
    tables:   list[list[list[str]]] = []  # tables[table_idx][row][col]
    width:    float = 0.0
    height:   float = 0.0


class DocumentLayout(BaseModel):
    source:     str = "unknown"
    pages:      list[PageContent]
    total_text: str = ""

    def __init__(self, **data):
        super().__init__(**data)
        if not self.total_text:
            self.total_text = "\n\n".join(p.text for p in self.pages)

    @property
    def page_count(self) -> int:
        return len(self.pages)

    def text_for_pages(self, start: int = 1, end: int | None = None) -> str:
        pages = [p for p in self.pages if start <= p.page_num <= (end or len(self.pages))]
        return "\n\n".join(p.text for p in pages)

    def all_tables(self) -> list[list[list[str]]]:
        return [t for p in self.pages for t in p.tables]
