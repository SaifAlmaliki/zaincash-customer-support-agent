from __future__ import annotations

import re

from app.pipeline.contracts import NormalizedTicket, Ticket

_DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹", "0123456789" * 2)
_FOLD = str.maketrans({"أ": "ا", "إ": "ا", "آ": "ا", "ٱ": "ا", "ى": "ي", "ؤ": "و", "ئ": "ي"})
_DIACRITICS = re.compile(r"[\u064B-\u0652\u0670\u0640]")  # harakat, dagger alef, tatweel
_CARD = re.compile(r"(?<![\w+])\d(?:[ -]?\d){12,18}(?!\w)")
_ARABIC = re.compile(r"[\u0600-\u06FF]")
_LATIN_WORD = re.compile(r"\b[0-9']*[A-Za-z][A-Za-z0-9']*\b")
_DIGIT_IN_WORD = re.compile(r"(?=.*[A-Za-z])(?=.*[235679])[A-Za-z0-9']+")
_ARABIZI_WORDS = frozenset({
    "shlon", "shlonak", "shlonich", "aku", "maku", "mako", "flos", "floos", "hawala",
    "hawalit", "rasid", "ams", "lyom", "alyom", "wallah", "wallahi", "shnu", "shno", "leish",
    "lesh", "ani", "inta", "inti", "ma", "da", "wsl", "wslat", "wislat", "alf", "dinar", "mal",
    "el", "w", "ywselni", "agdar", "akdar",
})


def to_ascii_digits(text: str) -> str:
    """Arabic-Indic and Persian digits to ASCII. Length-preserving."""
    return text.translate(_DIGITS)


def mask_cards(text: str) -> str:
    """Replace all but the last 4 digits of card-like numbers with '*'. Length-preserving."""
    ascii_text = to_ascii_digits(text)
    chars = list(text)
    for m in _CARD.finditer(ascii_text):
        idx = [i for i in range(m.start(), m.end()) if ascii_text[i].isdigit()]
        digits = "".join(ascii_text[i] for i in idx)
        if digits.startswith(("964", "07")) and len(digits) <= 13:
            continue  # Iraqi phone number, not a card
        for i in idx[:-4]:
            chars[i] = "*"
    return "".join(chars)


def fold_arabic(text: str) -> str:
    return _DIACRITICS.sub("", text).translate(_FOLD)


def _latin_words(text: str) -> list[str]:
    return [w.lower() for w in _LATIN_WORD.findall(text)]


def detect_arabizi(text: str) -> bool:
    words = _latin_words(text)
    if len(words) < 2:
        return False
    hits = sum(1 for w in words if w in _ARABIZI_WORDS or _DIGIT_IN_WORD.fullmatch(w))
    return hits >= 2 or hits / len(words) >= 0.3


def has_latin_mix(text: str) -> bool:
    return bool(_ARABIC.search(text)) and len(_latin_words(text)) >= 2


def sanitize_for_storage(text: str) -> str:
    return mask_cards(text).strip()


def normalize(ticket: Ticket) -> NormalizedTicket:
    match_text = to_ascii_digits(ticket.text)
    return NormalizedTicket(
        ticket=ticket,
        match_text=match_text,
        normalized_text=fold_arabic(match_text),
        is_arabizi=detect_arabizi(ticket.text),
        has_latin_mix=has_latin_mix(ticket.text),
    )
