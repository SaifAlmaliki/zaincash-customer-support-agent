"""Shared, length-preserving digit and sensitive-card normalization."""
from __future__ import annotations

import re

_DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹", "0123456789" * 2)
_CARD = re.compile(r"(?<![\w+])\d(?:[ -]?\d){12,18}(?!\w)")


def to_ascii_digits(text: str) -> str:
    """Arabic-Indic and Persian digits to ASCII. Length-preserving."""
    return text.translate(_DIGITS)


def mask_cards(text: str) -> str:
    """Replace all but the last 4 digits of card-like numbers with '*'. Length-preserving."""
    ascii_text = to_ascii_digits(text)
    chars = list(text)
    for match in _CARD.finditer(ascii_text):
        indexes = [i for i in range(match.start(), match.end()) if ascii_text[i].isdigit()]
        digits = "".join(ascii_text[i] for i in indexes)
        if digits.startswith(("964", "07")) and len(digits) <= 13:
            continue
        for index in indexes[:-4]:
            chars[index] = "*"
    return "".join(chars)
