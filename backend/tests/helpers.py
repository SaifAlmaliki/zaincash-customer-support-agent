from datetime import datetime, timedelta, timezone

from app.pipeline.contracts import Ticket

BAGHDAD = timezone(timedelta(hours=3))
RECEIVED = datetime(2026, 10, 7, 9, 30, tzinfo=BAGHDAD)  # a Wednesday


def make_ticket(text: str, **kw) -> Ticket:
    return Ticket(
        external_id=kw.pop("external_id", "T-1"),
        text=text,
        received_at=kw.pop("received_at", RECEIVED),
        **kw,
    )
