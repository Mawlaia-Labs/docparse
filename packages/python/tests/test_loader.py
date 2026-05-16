from docparse.loader import from_text, load


def test_from_text_single_page():
    layout = from_text("Hello world, this is a test document.")
    assert layout.page_count == 1
    assert "Hello world" in layout.pages[0].text
    assert "Hello world" in layout.total_text


def test_from_text_source():
    layout = from_text("content", source="my-doc")
    assert layout.source == "my-doc"


def test_from_text_default_source():
    layout = from_text("content")
    assert layout.source == "text"


def test_load_txt_file(tmp_path):
    p = tmp_path / "doc.txt"
    p.write_text("Invoice total: $1,500.00", encoding="utf-8")
    layout = load(str(p))
    assert "Invoice total" in layout.total_text


def test_load_md_file(tmp_path):
    p = tmp_path / "doc.md"
    p.write_text("# Contract\n\nParty: Acme Corp", encoding="utf-8")
    layout = load(str(p))
    assert "Acme Corp" in layout.total_text


def test_load_unsupported_raises(tmp_path):
    p = tmp_path / "doc.docx"
    p.write_text("content")
    try:
        load(str(p))
        assert False, "Should have raised"
    except ValueError as e:
        assert ".docx" in str(e)


def test_from_text_multiline():
    text = "Line 1\nLine 2\nLine 3"
    layout = from_text(text)
    assert layout.pages[0].text == text
