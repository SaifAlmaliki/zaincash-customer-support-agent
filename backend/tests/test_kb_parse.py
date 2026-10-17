from io import BytesIO

import pytest

from app.kb.parse import DocumentParseError, parse_document


def make_pdf(pages: list[str], *, password: str | None = None) -> bytes:
    """Generate real text/blank PDFs in memory without external fixtures or tools."""
    from pypdf import PdfWriter
    from pypdf.generic import DecodedStreamObject, DictionaryObject, NameObject

    writer = PdfWriter()
    for text in pages:
        page = writer.add_blank_page(width=612, height=792)
        if text:
            font = DictionaryObject({
                NameObject("/Type"): NameObject("/Font"),
                NameObject("/Subtype"): NameObject("/Type1"),
                NameObject("/BaseFont"): NameObject("/Helvetica"),
            })
            page[NameObject("/Resources")] = DictionaryObject({
                NameObject("/Font"): DictionaryObject({NameObject("/F1"): font}),
            })
            stream = DecodedStreamObject()
            stream.set_data(f"BT /F1 12 Tf 50 700 Td ({text}) Tj ET".encode("ascii"))
            page[NameObject("/Contents")] = stream
    if password is not None:
        writer.encrypt(password, algorithm="RC4-128")
    output = BytesIO()
    writer.write(output)
    return output.getvalue()


def test_arabic_text_and_bom_are_preserved():
    chunks = parse_document("policy.md", "\ufeff# سياسة تجريبية\nلا تشارك الرقم السري.".encode())
    assert chunks[0].index == 0
    assert "لا تشارك الرقم السري" in chunks[0].text
    assert chunks[0].text.startswith("# سياسة تجريبية")
    assert "\ufeff" not in chunks[0].text
    assert chunks[0].page_start is None and chunks[0].page_end is None


def test_only_the_initial_bom_is_removed():
    chunks = parse_document("policy.TXT", "\ufeffبداية\ufeffنهاية".encode())
    assert chunks[0].text == "بداية\ufeffنهاية"


@pytest.mark.parametrize("content", [b"", b" \n\t ", "\ufeff \n".encode()])
def test_empty_text_has_an_actionable_error(content):
    with pytest.raises(DocumentParseError, match="(?i)empty|no.*text"):
        parse_document("empty.txt", content)


def test_invalid_utf8_is_rejected_instead_of_replaced():
    with pytest.raises(DocumentParseError, match="UTF-8"):
        parse_document("policy.md", b"policy\xff")


def test_unsupported_file_is_rejected():
    with pytest.raises(DocumentParseError, match=r"(?i)unsupported|\.pdf"):
        parse_document("policy.docx", b"content")


def test_chunking_is_deterministic_bounded_and_overlapping():
    text = "".join(chr(0x0620 + i % 30) for i in range(3000))
    chunks = parse_document("long.txt", text.encode())
    assert chunks == parse_document("long.txt", text.encode())
    assert [chunk.index for chunk in chunks] == [0, 1, 2]
    assert [len(chunk.text) for chunk in chunks] == [1200, 1200, 960]
    assert chunks[0].text == text[:1200]
    assert chunks[1].text == text[1020:2220]
    assert chunks[2].text == text[2040:]
    assert chunks[0].text[-180:] == chunks[1].text[:180]
    assert chunks[2].text.endswith(text[-100:])


@pytest.mark.parametrize("separator", ["\n\n", "\r\n\r\n"])
def test_paragraph_boundary_is_preferred_without_losing_the_tail(separator):
    text = "a" * 800 + separator + "b" * 800
    chunks = parse_document("paragraphs.md", text.encode())
    assert chunks[0].text.rstrip() == "a" * 800
    assert len(chunks) == 2
    assert chunks[-1].text.endswith("b" * 800)
    assert all(len(chunk.text) <= 1200 for chunk in chunks)


@pytest.mark.parametrize("length, expected_count", [(1, 1), (179, 1), (180, 1),
                                                        (1200, 1), (1201, 2)])
def test_short_tail_and_overlap_always_terminate(length, expected_count):
    chunks = parse_document("tail.txt", b"x" * length)
    assert len(chunks) == expected_count
    assert chunks[-1].text == "x" * (length if length <= 1200 else 181)


def test_many_short_paragraphs_make_bounded_progress():
    text = "x\n\n" * 1000 + "THE END"
    chunks = parse_document("short.md", text.encode())
    assert 2 <= len(chunks) <= 5
    assert all(0 < len(chunk.text) <= 1200 for chunk in chunks)
    assert chunks[-1].text.endswith("THE END")


def test_extracted_text_limit_counts_unicode_characters_not_bytes():
    chunks = parse_document("max.txt", ("ع" * 1_000_000).encode())
    assert len(chunks) == 981
    assert chunks[-1].text.endswith("ع" * 100)
    with pytest.raises(DocumentParseError, match="1,000,000.*character"):
        parse_document("too-long.txt", b"x" * 1_000_001)


def test_chunk_limit_is_enforced():
    with pytest.raises(DocumentParseError, match="1,200.*chunk"):
        parse_document("many.md", ("x" * 600 + "\n\n").encode() * 1600)


def test_upload_limit_is_checked_before_pdf_processing(monkeypatch):
    def unexpected_reader(*args, **kwargs):
        pytest.fail("oversized uploads must not reach the PDF reader")

    monkeypatch.setattr("app.kb.parse.PdfReader", unexpected_reader)
    with pytest.raises(DocumentParseError, match="10 MB"):
        parse_document("too-large.pdf", b"x" * (10 * 1024 * 1024 + 1))


def test_blank_pdf_tells_operator_to_use_ocr():
    with pytest.raises(DocumentParseError, match="OCR"):
        parse_document("scan.pdf", make_pdf(["", ""]))


def test_encrypted_pdf_is_rejected_with_unlock_guidance():
    with pytest.raises(DocumentParseError, match="(?i)encrypted.*unlock|password"):
        parse_document("locked.pdf", make_pdf(["secret"], password="test-password"))


def test_malformed_pdf_has_a_bounded_public_error():
    with pytest.raises(DocumentParseError) as error:
        parse_document("broken.pdf", b"not a PDF: private document data")
    assert "PDF" in str(error.value)
    assert "private document data" not in str(error.value)
    assert len(str(error.value)) <= 250


def test_pdf_chunks_keep_original_one_based_pages_including_blank_pages():
    chunks = parse_document("policy.PDF", make_pdf(["a" * 1400, "", "Last page policy"]))
    assert [chunk.index for chunk in chunks] == [0, 1, 2]
    assert [(chunk.page_start, chunk.page_end) for chunk in chunks] == [(1, 1), (1, 1), (3, 3)]
    assert chunks[0].text == "a" * 1200
    assert chunks[1].text == "a" * 380
    assert chunks[2].text == "Last page policy"


def test_pdf_page_limit_is_checked_before_text_extraction(monkeypatch):
    def unexpected_extraction(*args, **kwargs):
        pytest.fail("page count must be checked before extracting any text")

    monkeypatch.setattr("pypdf.PageObject.extract_text", unexpected_extraction)
    with pytest.raises(DocumentParseError, match="300.*page"):
        parse_document("many-pages.pdf", make_pdf([""] * 301))


def test_pdf_page_limit_allows_exactly_300_pages():
    chunks = parse_document("300.pdf", make_pdf([""] * 299 + ["Last page"]))
    assert len(chunks) == 1
    assert chunks[0].page_start == chunks[0].page_end == 300


def test_pdf_extracted_limit_is_accumulated_and_stops_before_next_page(monkeypatch):
    from pypdf import PageObject

    real_extract = PageObject.extract_text
    extracted = []

    def tracked_extract(page, *args, **kwargs):
        if len(extracted) >= 2:
            pytest.fail("parser continued past the extracted-character limit")
        text = real_extract(page, *args, **kwargs)
        extracted.append(len(text))
        return text

    monkeypatch.setattr(PageObject, "extract_text", tracked_extract)
    with pytest.raises(DocumentParseError, match="1,000,000.*character"):
        parse_document("too-much.pdf", make_pdf(["a" * 600_000, "b" * 400_001, "tail"]))
    assert extracted == [600_000, 400_001]
