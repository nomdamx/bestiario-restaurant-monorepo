import time
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError

from src.core.custom_errors import ValidationError
from src.models import Order, OrderAddons, Ticket


def recalc_ticket_total(db: Session, *, id_ticket: int, retries:int = 3) -> None:
    for attempt in range(retries):
        try:
            db.flush()
            ticket = (
                db.query(Ticket)
                .filter(Ticket.id == id_ticket)
                .with_for_update()
                .first()
            )

            if not ticket:
                raise ValidationError(details="Ticket doesn't exist")

            new_total = (
                db.query(func.sum(Order.total))
                .filter(Order.id_ticket == id_ticket)
                .filter(Order.is_active)
                .scalar()
            ) or 0.0

            ticket.total = new_total
            return

        except OperationalError as e:
            db.rollback()
            if "deadlock" in str(e).lower() and attempt < retries - 1:
                time.sleep(0.1 * (attempt + 1))
                continue
            raise


def recalc_order_total(db: Session, *, id_order: int):
    order = db.query(Order).filter(Order.id == id_order).first()
    if not order:
        raise ValidationError(details="Order doesn't exist")

    addons_total = (
        db.query(func.sum(OrderAddons.unit_price * order.quantity))
        .filter(OrderAddons.id_order == id_order)
        .filter(OrderAddons.is_active)
        .scalar()
    ) or 0.0

    new_total = float(order.unit_price * order.quantity) + float(addons_total)
    order.total = new_total
    recalc_ticket_total(db, id_ticket=order.id_ticket)
