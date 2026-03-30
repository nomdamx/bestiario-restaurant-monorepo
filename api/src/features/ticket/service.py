from datetime import date

from sqlalchemy.orm import Query, Session, joinedload
from sqlalchemy.sql.elements import ColumnElement

from src.core.custom_errors import ValidationError
from src.models import Order, PrintListTicket, Ticket, User
from src.core.recalc_totals import recalc_ticket_total


from . import dependency, schema


def _query_ticket_(db: Session) -> Query[Ticket]:
    return db.query(Ticket)


def _query_filter_active(db: Session, is_active: bool = True) -> Query[Ticket]:
    return _query_ticket_(db).filter(Ticket.is_active == is_active)


def get_paginated(
    db: Session, *, filters: dependency.FilterTicket, limit: int, offset: int
) -> tuple[list[Ticket], int]:

    conditions: list[ColumnElement[bool]] = [
        Ticket.is_active.is_(filters.is_active),
        Ticket.is_paid.is_(filters.is_paid),
    ]

    if filters.uuid is not None:
        conditions.append(Ticket.uuid == filters.uuid)

    tickets = db.query(Ticket).filter(*conditions)

    total = tickets.count()

    if total <= 0:
        return tickets.all(), 1

    paginated = (
        tickets.order_by(Ticket.created_at.desc()).limit(limit).offset(offset).all()
    )

    return paginated, total


def get_by_id(db: Session, id_ticket: int) -> Ticket:
    ticket = _query_filter_active(db).filter(Ticket.id == id_ticket).first()

    if not ticket:
        raise ValidationError(details="This Ticket doesn't exist")

    return ticket


def get_by_uuid(db: Session, uuid: str) -> Ticket:
    ticket = _query_filter_active(db).filter(Ticket.uuid == uuid).first()

    if not ticket:
        raise ValidationError(details="This Ticket doesn't exist")

    return ticket


def register(db: Session, user: User, *, payload: schema.PayloadTicket) -> Ticket:
    op_date, ticket_number = operational_ticket_number(db)

    register_ticket = Ticket(
        id_restaurant_table=payload.id_restaurant_table,
        id_user=user.id,
        uuid=create_new_uuid(db),
        ticket_number=ticket_number,
        operational_date=op_date,
    )

    db.add(register_ticket)
    db.commit()
    return register_ticket


def get_ticket_with_orders(db: Session, *, uuid: str):
    ticket = (
        db.query(Ticket)
        .filter(Ticket.uuid == uuid)
        .filter(Ticket.is_active)
        .options(joinedload(Ticket.orders.and_(Order.is_active)))
        .first()
    )

    if not ticket:
        raise ValidationError(details="This Ticket doesn't exist")

    return ticket


def patch(
    db: Session, *, payload: schema.PayloadUpdateTicket, id_ticket: int
) -> Ticket:

    ticket = _query_filter_active(db).filter(Ticket.id == id_ticket).first()

    if not ticket:
        raise ValidationError(details="This Ticket doesn't exist")

    if payload.id_restaurant_table:
        ticket.id_restaurant_table = payload.id_restaurant_table

    if payload.comments is not None:
        ticket.comments = payload.comments

    if payload.client_name is not None:
        ticket.client_name = payload.client_name

    db.commit()
    return ticket


def soft_delete(db: Session, *, id_ticket: int) -> None:
    ticket = _query_filter_active(db).filter(Ticket.id == id_ticket).first()

    if not ticket:
        raise ValidationError(details="This Ticket doesn't exist")

    ticket.soft_delete()
    db.commit()


def print_ticket(
    db: Session, *, filter: dependency.FilterPrintPayment, uuid: str
) -> PrintListTicket:
    ticket = get_by_uuid(db, uuid=uuid)
    is_for_pay = filter.for_pay

    print_list_ticket = (
        db.query(PrintListTicket).filter(PrintListTicket.id_ticket == ticket.id).first()
    )

    if not print_list_ticket:
        print_list_ticket = PrintListTicket(
            id_ticket=ticket.id,
            print_for_pay=is_for_pay,
            is_active=True,
            printed=False,
        )
        db.add(print_list_ticket)

    else:
        print_list_ticket.is_active = True

        if is_for_pay:
            print_list_ticket.print_for_pay = True
            print_list_ticket.printed = False
        else:
            print_list_ticket.print_for_pay = False

    db.flush()
    recalc_ticket_total(db,id_ticket=ticket.id)
    db.flush()
    db.refresh(ticket)
    db.commit()
    return print_list_ticket


def patch_client(
    db: Session, *, payload: schema.PayloadUpdateClientTicket, uuid: str
) -> Ticket:
    ticket = get_by_uuid(db, uuid=uuid)
    ticket.client_name = payload.client_name
    db.commit()
    return ticket


def patch_comments(
    db: Session, *, payload: schema.PayloadUpdateCommentsTicket, uuid: str
) -> Ticket:
    ticket = get_by_uuid(db, uuid=uuid)
    ticket.comments = payload.comments
    db.commit()
    return ticket


def patch_paid_status(
    db: Session, *, payload: schema.PayloadUpdatePaidTicket, uuid: str
) -> Ticket:
    ticket = get_by_uuid(db, uuid=uuid)
    ticket.is_paid = payload.is_paid
    db.flush()
    recalc_ticket_total(db,id_ticket=ticket.id)
    db.flush()
    db.refresh(ticket)
    db.commit()
    return ticket


## EVENTS
def create_new_uuid(db: Session) -> str:
    from uuid import uuid4

    _query = db.query(Ticket)
    while True:
        generated_uuid = str(uuid4())

        exist = _query.filter(Ticket.uuid == generated_uuid).first()
        if not exist:
            return generated_uuid


def operational_ticket_number(db: Session) -> tuple[date, int]:
    from sqlalchemy import func

    from src.utils.dates import get_operational_date

    op_date = get_operational_date()

    last_number = (
        db.query(func.max(Ticket.ticket_number))
        .filter(Ticket.operational_date == op_date)
        .scalar()
    )

    ticket_number: int = (last_number or 0) + 1
    return op_date, ticket_number
