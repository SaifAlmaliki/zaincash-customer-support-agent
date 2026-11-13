"""A customer is identified by the canonical ZainCash phone number 07XXXXXXXXX."""
from __future__ import annotations

import re

from app.text import to_ascii_digits

INVALID_PHONE_MESSAGE = "Enter a valid ZainCash phone number, for example 07701234567."
_ALLOWED = re.compile(r"[0-9\s+\-().]*")
# Invisible direction marks come from copy/paste in RTL apps and cannot alias another number.
_FORMAT_MARKS = re.compile("[\u200e\u200f\u061c\u202a-\u202e\u2066-\u2069\ufeff]")
_CANONICAL = re.compile(r"07[3-9][0-9]{8}")
_WITHOUT_ZERO = re.compile(r"7[3-9][0-9]{8}")


class InvalidPhone(ValueError):
    """The value is not a ZainCash customer phone number."""


def normalize_customer_phone(raw: object) -> str:
    # Unsupported characters reject the value; deleting them could turn
    # another value into a valid customer number.
    if not isinstance(raw, str):
        raise InvalidPhone(INVALID_PHONE_MESSAGE)
    text = _FORMAT_MARKS.sub("", to_ascii_digits(raw)).strip()
    if not _ALLOWED.fullmatch(text):
        raise InvalidPhone(INVALID_PHONE_MESSAGE)
    digits = re.sub(r"[^0-9]", "", text)
    if digits.startswith("00964"):
        digits = digits[2:]
    if digits.startswith("964"):
        digits = "0" + digits[3:]
    elif _WITHOUT_ZERO.fullmatch(digits):
        digits = "0" + digits
    if not _CANONICAL.fullmatch(digits):
        raise InvalidPhone(INVALID_PHONE_MESSAGE)
    return digits


def customer_phone_or_none(raw: object) -> str | None:
    try:
        return normalize_customer_phone(raw)
    except InvalidPhone:
        return None
