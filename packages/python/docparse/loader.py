"""Document loader — PDF and raw text to DocumentLayout."""
from __future__ import annotations
from pathlib import Path
from .models import DocumentLayout, PageContent


def from_text(text: str, source: str = "text") -> DocumentLayout:
    """Wrap raw text as a single-page DocumentLayout (useful for testing)."""
    return DocumentLayout(
        source=source,
        pages=[PageContent(page_num=1, text=text)],
    )


def from_pdf(path: str | Path) -> DocumentLayout:
    """Parse a PDF file using pdfplumber."""
    try:
        import pdfplumber
    except ImportError:
        raise ImportError("PDF support requires pdfplumber: pip install docparse[pdf]")

    path   = Path(path)
    pages: list[PageContent] = []

    with pdfplumber.open(path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            text   = page.extract_text() or ""
            tables = []
            for table in page.extract_tables() or []:
                # Normalise None cells to empty string
                cleaned = [[cell or "" for cell in row] for row in table if row]
                if cleaned:
                    tables.append(cleaned)
            pages.append(PageContent(
                page_num=i,
                text=text,
                tables=tables,
                width=float(page.width),
                height=float(page.height),
            ))

    return DocumentLayout(source=str(path), pages=pages)


def load(path: str | Path) -> DocumentLayout:
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return from_pdf(path)
    if suffix in (".txt", ".md"):
        return from_text(path.read_text(encoding="utf-8"), source=str(path))
    raise ValueError(f"Unsupported file type: {suffix}. Use .pdf, .txt, or .md")
