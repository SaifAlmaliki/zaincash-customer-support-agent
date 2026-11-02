from __future__ import annotations

import re

from app.pipeline.contracts import NormalizedTicket, Ticket
from app.text import mask_cards, to_ascii_digits

_FOLD = str.maketrans({"أ": "ا", "إ": "ا", "آ": "ا", "ٱ": "ا", "ى": "ي", "ؤ": "و", "ئ": "ي"})
_DIACRITICS = re.compile(r"[\u064B-\u0652\u0670\u0640]")  # harakat, dagger alef, tatweel
_ARABIC = re.compile(r"[\u0600-\u06FF]")
_LATIN_WORD = re.compile(r"\b[0-9']*[A-Za-z][A-Za-z0-9']*\b")
_DIGIT_IN_WORD = re.compile(r"(?=.*[A-Za-z])(?=.*[235679])[A-Za-z0-9']+")
_ARABIZI_WORDS = frozenset({
    "shlon", "shlonak", "shlonich", "aku", "maku", "mako", "flos", "floos", "hawala",
    "hawalit", "rasid", "ams", "lyom", "alyom", "wallah", "wallahi", "shnu", "shno", "leish",
    "lesh", "ani", "inta", "inti", "ma", "da", "wsl", "wslat", "wislat", "alf", "dinar", "mal",
    "el", "w", "ywselni", "agdar", "akdar",
})


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
