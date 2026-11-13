"""Customer rows. A customer exists once any ticket or conversation uses the phone."""
from __future__ import annotations

from collections.abc import Iterable

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.db.models import CustomerRow


def ensure_customers(session: Session, phones: Iterable[str]) -> None:
    """Insert missing customers. Each phone must already be canonical."""
    rows = [{"phone": phone} for phone in sorted(set(phones))]
    if rows:
        session.execute(insert(CustomerRow).values(rows).on_conflict_do_nothing(index_elements=["phone"]))