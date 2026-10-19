"""Keep explicitly labelled receipt IDs while masking card-like numbers elsewhere."""
import re

from app.pipeline.stage1_normalize.normalize import mask_cards

_REFERENCE = re.compile(
    r"((?:\b(?:receipt|reference|transaction)(?:\s+(?:reference|number|id))?\b|رقم\s*(?:العملية|المرجع|الإيصال|الايصال))"
    r"\s*[:#-]?\s*\d{13,19}(?!\d))", re.I,
)


def sanitize_intake_text(text: str) -> str:
    pieces = _REFERENCE.split(text)
    return "".join(piece if index % 2 else mask_cards(piece) for index, piece in enumerate(pieces)).strip()
