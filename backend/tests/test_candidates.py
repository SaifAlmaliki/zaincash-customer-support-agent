from app.pipeline.candidates import find_candidates, normalize_phone, parse_amount
from app.pipeline.normalize import to_ascii_digits


def _values(cands, field):
    return [c.value for c in cands.for_field(field)]


def test_arabic_indic_amount_not_confused_with_phone():
    text = to_ascii_digits("حولت ٥٠ الف لرقم 0770 123 4567 امس ورقم العملية ZC-2410000123")
    c = find_candidates(text)
    assert _values(c, "txn_ref") == ["ZC2410000123"]
    assert _values(c, "phone") == ["07701234567"]
    assert _values(c, "amount") == ["50 الف"]
    assert _values(c, "date") == ["امس"]
    for field in ("txn_ref", "phone", "amount", "date"):
        for cand in c.for_field(field):
            assert text[cand.start : cand.end] == cand.span


def test_small_bare_numbers_are_not_amounts():
    c = find_candidates("صارلي قبل 2 يوم انتظر")
    assert _values(c, "amount") == []
    assert _values(c, "date") == ["قبل 2 يوم"]


def test_amount_forms():
    c = find_candidates("دفعت 25k ومرة ثانية $20 والفاتورة 1,250,000 دينار")
    assert _values(c, "amount") == ["25k", "$20", "1,250,000 دينار"]


def test_parse_amount():
    assert parse_amount("50 الف") == (50000, "IQD")
    assert parse_amount("25k") == (25000, "IQD")
    assert parse_amount("$20") == (20, "USD")
    assert parse_amount("1,250,000 دينار") == (1250000, "IQD")
    assert parse_amount("1.5 مليون") == (1500000, "IQD")
    assert parse_amount("50.000") == (50000, "IQD")
    assert parse_amount("خمسين الف") is None


def test_dates_absolute_and_weekday():
    c = find_candidates("صار يوم الخميس وبعدها 2026-10-05 و 5/10")
    assert _values(c, "date") == ["2026-10-05", "5/10", "يوم الخميس"]


def test_normalize_phone():
    assert normalize_phone("+964 770 123 4567") == "07701234567"
    assert normalize_phone("0770-123-4567") == "07701234567"
    assert normalize_phone("12345") is None


def test_dedupes_repeated_values():
    c = find_candidates("ZC2410000123 و ZC 2410000123")
    assert _values(c, "txn_ref") == ["ZC2410000123"]
