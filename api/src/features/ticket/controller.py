from math import ceil

from sqlalchemy.orm import Session

from src.core.api_response import Pagination
from src.core.custom_errors import ValidationError
from src.core.dependency import PaginationParams
from src.models import Ticket, User

from . import dependency, schema, service


def get_all(
    db: Session, *, pagination: PaginationParams, filters: dependency.FilterTicket
) -> tuple[list[Ticket], Pagination]:
    tickets, total = service.get_paginated(
        db, filters=filters, limit=pagination.limit, offset=pagination.offset
    )
    pages = ceil(total / pagination.limit)

    return tickets, Pagination(
        page=pagination.page, pages=pages, limit=pagination.limit, total=total
    )


def get_by_id(db: Session, *, id_ticket: int) -> Ticket:
    return service.get_by_id(db, id_ticket=id_ticket)


def get_by_uuid(db: Session, *, uuid: str) -> Ticket:
    return service.get_by_uuid(db, uuid=uuid)


def register(db: Session, user: User, *, payload: schema.PayloadTicket) -> Ticket:
    return service.register(db, user, payload=payload)


def get_ticket_with_orders(db: Session, *, uuid: str):
    return service.get_ticket_with_orders(db, uuid=uuid)


def patch(
    db: Session, *, payload: schema.PayloadUpdateTicket, id_ticket: int
) -> Ticket:
    return service.patch(db, payload=payload, id_ticket=id_ticket)


def delete(db: Session, *, id_ticket: int):
    service.soft_delete(db, id_ticket=id_ticket)


def print_ticket(db: Session, *, filter: dependency.FilterPrintPayment, uuid: str):
    service.print_ticket(db, filter=filter, uuid=uuid)
    # sockets para impresion
    # from app.sockets import PRINTERS_ROOM, socket_safe
    # socketio.emit(
    # "pending_tickets",
    # {"tickets_list": socket_safe([print_list.ticket.get_json_for_print()])},
    # room=PRINTERS_ROOM
    # )


def patch_client(db: Session, *, payload: schema.PayloadUpdateClientTicket, uuid: str):
    return service.patch_client(db, payload=payload, uuid=uuid)


def patch_comments(
    db: Session, *, payload: schema.PayloadUpdateCommentsTicket, uuid: str
):
    return service.patch_comments(db, payload=payload, uuid=uuid)


def patch_paid_status(
    db: Session, *, payload: schema.PayloadUpdatePaidTicket, uuid: str
):
    return service.patch_paid_status(db, payload=payload, uuid=uuid)
