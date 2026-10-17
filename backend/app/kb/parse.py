"""Bounded, deterministic Unicode chunking; PDF chunks never cross page boundaries."""
from __future__ import annotations

import re
from io import BytesIO
from pathlib import Path

from pypdf import PdfReader

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
                text = page.extract_text() or ""
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
