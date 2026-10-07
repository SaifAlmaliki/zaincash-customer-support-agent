from datetime import date

import pytest

from app.pipeline.dates import resolve_date
from tests.helpers import RECEIVED  # Wednesday 2026-10-07


@pytest.mark.parametrize(
    ("span", "expected"),
    [
        ("اليوم", date(2026, 10, 7)),
        ("امس", date(2026, 10, 6)),
        ("البارحة", date(2026, 10, 6)),
        ("yesterday", date(2026, 10, 6)),
        ("قبل يومين", date(2026, 10, 5)),
        ("قبل 3 ايام", date(2026, 10, 4)),
        ("الاسبوع الماضي", date(2026, 9, 30)),
        ("يوم الخميس", date(2026, 10, 1)),
        ("الاربعاء", date(2026, 10, 7)),
        ("2026-10-05", date(2026, 10, 5)),
        ("5/10", date(2026, 10, 5)),
        ("25/12", date(2025, 12, 25)),
        ("5/10/26", date(2026, 10, 5)),
    ],
)
def test_resolve(span, expected):
    assert resolve_date(span, RECEIVED) == expected


@pytest.mark.parametrize("span", ["32/13", "", "قريب"])
def test_unresolvable_is_none(span):
    assert resolve_date(span, RECEIVED) is None
