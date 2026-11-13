import pytest

from app.customers.phone import InvalidPhone, customer_phone_or_none, normalize_customer_phone


@pytest.mark.parametrize("raw", [
    "07701234567",
    "0770 123 4567",
    "0770-123-4567",
    "(0770) 123-4567",
    "0770.123.4567",
    "+9647701234567",
    "+964 770 123 4567",
    "9647701234567",
    "00964 770 123 4567",
    "7701234567",
    "٠٧٧٠١٢٣٤٥٦٧",
    "+۹۶۴\u00a0۷۷۰-۱۲۳ ۴۵۶۷",
    "  07701234567  ",
    "\u202a+964 770 123 4567\u202c",
    "\u2066+964 770 123 4567\u2069",
    "\u200e07701234567",
    "\u061c07701234567",
    "\ufeff07701234567",
])
def test_accepted_formats_become_the_canonical_phone(raw):
    assert normalize_customer_phone(raw) == "07701234567"


@pytest.mark.parametrize("raw", [
    "", "   ", "0770123456", "077012345678", "07201234567", "96407701234567",
    "07701234567x", "0770123456\uff11", "0770123456\u0967", "+1 202 555 0100",
    "0770/123/4567", None, 7701234567,
], ids=["empty", "blank", "short", "long", "bad-prefix", "964-then-0", "letter", "fullwidth",
        "devanagari", "foreign", "slash", "none", "int"])
def test_invalid_input_is_rejected(raw):
    with pytest.raises(InvalidPhone, match="valid ZainCash phone number"):
        normalize_customer_phone(raw)


def test_optional_lookup_never_raises():
    assert customer_phone_or_none("+964 780 987 6543") == "07809876543"
    assert customer_phone_or_none("needle") is None
    assert customer_phone_or_none(None) is None
