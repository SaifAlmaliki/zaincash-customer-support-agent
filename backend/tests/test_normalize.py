from app.pipeline.normalize import (
    detect_arabizi,
    fold_arabic,
    has_latin_mix,
    mask_cards,
    normalize,
    sanitize_for_storage,
    to_ascii_digits,
)
from tests.helpers import make_ticket


def test_ascii_digits_is_length_preserving():
    assert to_ascii_digits("٥٠ الف ۱۲") == "50 الف 12"


def test_mask_card_keeps_last_four():
    assert mask_cards("رقم البطاقة 5123 4567 8901 2346") == "رقم البطاقة **** **** **** 2346"


def test_mask_card_in_arabic_indic_digits():
    assert mask_cards("٥١٢٣٤٥٦٧٨٩٠١٢٣٤٦") == "************٢٣٤٦"


def test_mask_leaves_phones_and_refs():
    for s in ["07701234567", "+9647701234567", "9647701234567", "ZC2410000123"]:
        assert mask_cards(s) == s


def test_fold_arabic():
    assert fold_arabic("أحمد إلى مستشفى") == "احمد الي مستشفي"
    assert fold_arabic("شُكْراً") == "شكرا"


def test_arabizi_detection():
    assert detect_arabizi("hawalit 25 alf w ma wslat")
    assert detect_arabizi("ma da ywselni el code mal ta2keed")
    assert not detect_arabizi("حولت 25 الف")
    assert not detect_arabizi("my app is not working")


def test_latin_mix():
    assert has_latin_mix("التطبيق ما يشتغل after update")
    assert not has_latin_mix("التطبيق ما يشتغل")


def test_normalize_keeps_spans_aligned():
    nt = normalize(make_ticket("حولت ٥٠ الف امس"))
    assert len(nt.match_text) == len(nt.ticket.text)
    assert "50" in nt.match_text
    assert not nt.is_arabizi


def test_sanitize_masks_cards():
    assert sanitize_for_storage(" بطاقتي 5123456789012346 ") == "بطاقتي ************2346"
