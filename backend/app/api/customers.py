from fastapi import APIRouter, HTTPException
from sqlalchemy import func, select

from app.api.dependencies import SessionDep
from app.customers.phone import InvalidPhone, normalize_customer_phone
from app.db.models import CustomerRow, TicketResultRow, TicketRow
from app.services.workspace_queries import latest_results_query, result_view

router = APIRouter(prefix="/api/customers", tags=["Customers"])


@router.get("/{phone}")
def get_customer(phone: str, session: SessionDep):
    try:
        canonical = normalize_customer_phone(phone)
    except InvalidPhone as exc:
        raise HTTPException(422, str(exc)) from None
    customer = session.get(CustomerRow, canonical)
    if customer is None:
        raise HTTPException(404, "No customer with this phone number.")
    rows = session.scalars(
        latest_results_query()
        .join(TicketRow, TicketRow.id == TicketResultRow.ticket_id)
        .where(TicketRow.customer_phone == canonical)
        .order_by(TicketRow.received_at.desc(), TicketResultRow.id.desc())
    )
    ticket_count = session.scalar(
        select(func.count()).select_from(TicketRow).where(TicketRow.customer_phone == canonical)
    ) or 0
    return {
        "phone": canonical,
        "created_at": customer.created_at,
        "ticket_count": ticket_count,
        "results": [result_view(session, row) for row in rows],
    }
