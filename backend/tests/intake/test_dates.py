from datetime import datetime
from zoneinfo import ZoneInfo


def test_yesterday_is_anchored_to_message_in_baghdad():
    from app.intake.dates import canonical_digits, normalize_reported_date
    sent = datetime(2026, 10, 18, 0, 5, tzinfo=ZoneInfo("Asia/Baghdad"))
    assert normalize_reported_date("yesterday", sent) == "2026-10-17"
    assert normalize_reported_date("أمس", sent) == "2026-10-17"
    assert canonical_digits("٥٠٠٠٠ / ۵۰۰۰۰") == "50000 / 50000"


def test_ambiguous_slash_date_is_not_fabricated():
    from app.intake.dates import normalize_reported_date
    sent = datetime(2026, 10, 18, 0, 5, tzinfo=ZoneInfo("Asia/Baghdad"))
    assert normalize_reported_date("10/11", sent) is None
    assert normalize_reported_date("2026-10-17", sent) == "2026-10-17"


def test_utc_instant_just_before_baghdad_midnight_stays_on_the_previous_day():
    from datetime import timedelta

    from app.intake.dates import normalize_reported_date
    # 21:30 UTC on the 17th is 00:30 on the 18th in Baghdad.
    sent = datetime(2026, 10, 17, 21, 30, tzinfo=ZoneInfo("UTC"))
    assert normalize_reported_date("today", sent) == "2026-10-18"
    assert normalize_reported_date("yesterday", sent) == "2026-10-17"
    assert timedelta(days=1).days == 1
