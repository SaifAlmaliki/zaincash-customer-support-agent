"""Bounded, deterministic Unicode chunking; PDF chunks never cross page boundaries."""
from __future__ import annotations

import re
import unicodedata
from io import BytesIO
from pathlib import Path

from pypdf import PdfReader
from pypdf._text_extraction import get_text_operands
from pypdf.generic._font import Font

from app.kb.contracts import TextChunk

CHUNK_SIZE = 1200
CHUNK_OVERLAP = 180
MAX_EXTRACTED_CHARS = 1_000_000
MAX_PDF_PAGES = 300
MAX_CHUNKS = 1200
MAX_UPLOAD_BYTES = 10 * 1024 * 1024
_PARAGRAPH_BREAK = re.compile(r"\r?\n\r?\n")


class DocumentParseError(ValueError):
    """An actionable, bounded message safe to show to the document's operator."""


def _append_chunks(text: str, chunks: list[TextChunk], *, page: int | None = None) -> None:
    start = 0
    while start < len(text):
        end = min(start + CHUNK_SIZE, len(text))
        if end < len(text):
            # Avoid tiny chunks when a paragraph break lies in the overlap itself.
            for boundary in _PARAGRAPH_BREAK.finditer(text, start + CHUNK_SIZE // 2, end):
                end = boundary.end()
        chunk_text = text[start:end].strip()
        if chunk_text:
            if len(chunks) >= MAX_CHUNKS:
                raise DocumentParseError("Document exceeds 1,200 chunks; split it into smaller files.")
            chunks.append(TextChunk(len(chunks), chunk_text, page, page))
        if end == len(text):
            break
        start = max(start + 1, end - CHUNK_OVERLAP)


def _check_extracted_size(size: int) -> None:
    if size > MAX_EXTRACTED_CHARS:
        raise DocumentParseError(
            "Document exceeds 1,000,000 extracted characters; split it into smaller files."
        )


def _is_rtl(char: str) -> bool:
    code = ord(char)
    return 0x0590 <= code <= 0x08FF or 0xFB50 <= code <= 0xFDFF or 0xFE70 <= code <= 0xFEFF


def _is_ltr(char: str) -> bool:
    return char.isascii() and (char.isalnum() or char == "_")


def _token_kind(token: str) -> str:
    if any(_is_rtl(char) for char in token):
        return "rtl"
    if any(_is_ltr(char) for char in token):
        return "ltr"
    return "neutral"


def _combining_only(token: str) -> bool:
    return bool(token) and all(unicodedata.combining(char) for char in token)


def _visual_tokens_to_logical(tokens: list[str]) -> str:
    """Undo a line drawn left-to-right in visual order.

    Arabic ligatures stay intact because each glyph is one token. Latin words are
    reversed back after the line reverse so embedded English keeps its spelling.
    """
    tokens = list(reversed(tokens))
    pieces: list[str] = []
    index = 0
    while index < len(tokens):
        if _token_kind(tokens[index]) != "ltr":
            pieces.append(tokens[index])
            index += 1
            continue
        end = index + 1
        while end < len(tokens):
            kind = _token_kind(tokens[end])
            if kind == "ltr":
                end += 1
                continue
            if kind == "rtl":
                break
            probe = end
            while probe < len(tokens) and _token_kind(tokens[probe]) == "neutral":
                probe += 1
            if probe < len(tokens) and _token_kind(tokens[probe]) == "ltr":
                end = probe + 1
                continue
            break
        pieces.extend(reversed(tokens[index:end]))
        index = end
    return "".join(pieces)


def _line_text(items: list[tuple[float, int, str]]) -> str:
    bases: list[tuple[float, int, str]] = []
    marks: list[tuple[float, str]] = []
    for x, order, text in sorted(items):
        if _combining_only(text):
            marks.append((x, text))
        else:
            bases.append((x, order, text))
    for x, text in marks:
        if not bases:
            continue
        nearest = min(range(len(bases)), key=lambda index: abs(bases[index][0] - x))
        base_x, base_order, base_text = bases[nearest]
        bases[nearest] = (base_x, base_order, base_text + text)
    tokens = [text for _x, _order, text in bases]
    if any(_is_rtl(char) for token in tokens for char in token):
        return _visual_tokens_to_logical(tokens)
    return "".join(tokens)


def _logical_page_text(page) -> str:
    """Read a page in logical order.

    These policy PDFs paint each glyph from left to right after bidi reordering,
    and pypdf then reorders the runs again. Collecting glyphs by position and
    restoring logical order keeps Arabic sentences and embedded English words intact.
    """
    resources = page.get("/Resources")
    font_resources = resources.get_object().get("/Font") if resources is not None else None
    if font_resources is None:
        return page.extract_text() or ""
    fonts = {
        name: Font.from_font_resource(font.get_object())
        for name, font in font_resources.get_object().items()
    }
    state: dict[str, Font | None] = {"font": None}
    glyphs: list[tuple[float, float, int, str]] = []
    sequence = 0

    def before(operator, operands, cm, tm):
        nonlocal sequence
        if operator == b"Tf" and operands:
            state["font"] = fonts.get(operands[0])
        font = state["font"]
        if operator != b"Tj" or not operands or font is None:
            return
        text_operands, is_string, _width = get_text_operands(
            operands, cm, tm, font, (0, 90, 180, 270),
        )
        decoded = text_operands if is_string else "".join(
            font.character_map.get(char, char) for char in text_operands
        )
        if decoded:
            glyphs.append((float(tm[5]), float(tm[4]), sequence, decoded))
            sequence += 1

    plain = page.extract_text(visitor_operand_before=before) or ""
    if not glyphs:
        return plain
    lines: list[tuple[float, list[tuple[float, int, str]]]] = []
    for y, x, order, text in glyphs:
        for baseline, items in lines:
            if abs(baseline - y) <= 2:
                items.append((x, order, text))
                break
        else:
            lines.append((y, [(x, order, text)]))
    logical = "\n".join(
        _line_text(items)
        for _baseline, items in sorted(lines, key=lambda item: item[0], reverse=True)
    ).strip()
    return logical or plain


def _parse_pdf(content: bytes) -> list[TextChunk]:
    chunks: list[TextChunk] = []
    try:
        with PdfReader(BytesIO(content)) as reader:
            if reader.is_encrypted:
                raise DocumentParseError("PDF is encrypted; unlock it and upload a password-free copy.")
            if len(reader.pages) > MAX_PDF_PAGES:
                raise DocumentParseError("PDF exceeds 300 pages; split it into smaller files.")
            extracted_chars = 0
            for page_number, page in enumerate(reader.pages, start=1):
                text = _logical_page_text(page)
                extracted_chars += len(text)
                _check_extracted_size(extracted_chars)
                _append_chunks(text, chunks, page=page_number)
    except DocumentParseError:
        raise
    except Exception:
        # Parser diagnostics can contain document data. Only expose static guidance.
        raise DocumentParseError(
            "Unable to read PDF; upload a valid text-based PDF or use OCR for a scanned document."
        ) from None
    if not chunks:
        raise DocumentParseError("PDF has no extractable text; use OCR and upload a text-based copy.")
    return chunks


def parse_document(filename: str, content: bytes) -> list[TextChunk]:
    """Parse .txt/.md UTF-8 or .pdf bytes; PDF page metadata is one-based.

    Raises DocumentParseError for unsupported, empty, unreadable or over-limit input.
    Only the initial UTF-8 BOM is removed. Overlap is up to 180 Unicode characters.
    """
    if len(content) > MAX_UPLOAD_BYTES:
        raise DocumentParseError("Document exceeds the 10 MB upload limit; upload a smaller file.")
    suffix = Path(filename).suffix.lower()
    if suffix == ".pdf":
        return _parse_pdf(content)
    if suffix not in {".txt", ".md"}:
        raise DocumentParseError("Unsupported document type; upload a .txt, .md or .pdf file.")
    try:
        text = content.decode("utf-8-sig")
    except UnicodeDecodeError:
        raise DocumentParseError("Text must be valid UTF-8; save it as UTF-8 and upload again.") from None
    _check_extracted_size(len(text))
    chunks: list[TextChunk] = []
    _append_chunks(text, chunks)
    if not chunks:
        raise DocumentParseError("Document is empty or has no text; upload a file containing text.")
    return chunks
