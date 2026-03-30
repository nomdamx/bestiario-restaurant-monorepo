import logging
from datetime import date, datetime
from uuid import UUID

import socketio
from sqlalchemy.orm import joinedload

from src.core.custom_errors import ValidationError

from . import schema

PRINTERS_ROOM = "printers"
socket_logger = logging.getLogger("socket")

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")


@sio.event
async def connect(sid, environ):
    socket_logger.info("[event:connect] [sid:%s]", sid)


@sio.event
async def disconnect(sid):
    socket_logger.info("[event:disconnect] [room:%s] [sid:%s]", PRINTERS_ROOM, sid)
    # await sio.leave_room(sid, PRINTERS_ROOM)


@sio.event
async def join(sid, data):
    await sio.enter_room(sid, PRINTERS_ROOM)
    socket_logger.info("[event:join] [room:%s] [sid:%s]", PRINTERS_ROOM, sid)
    tickets = get_pending_tickets()
    if tickets:
        await sio.emit(
            "pending_tickets",
            {"tickets_list": tickets},
            room=PRINTERS_ROOM,
        )


@sio.event
async def resend(sid):
    socket_logger.info("[event:resend] [room:%s] [sid:%s]", PRINTERS_ROOM, sid)
    tickets = get_pending_tickets()
    if tickets:
        socket_logger.info("[event:resend] Pending tickets: %d", len(tickets))
        await sio.emit(
            "pending_tickets",
            {"tickets_list": tickets},
            room=PRINTERS_ROOM,
        )


@sio.event
async def ticket_printed(sid, data):
    from src.db.session import db_context
    from src.models import PrintListTicket, Ticket

    ticket_id = data["ticket_id"]
    ticket_orders = data["orders"]

    with db_context() as session:
        ticket_print_list = (
            session.query(PrintListTicket).filter_by(id_ticket=ticket_id).first()
        )
        ticket = session.query(Ticket).filter_by(id=ticket_id).first()

        if ticket is None:
            raise ValidationError(details="Ticket doesn't exist")

        if ticket_print_list is None:
            raise ValidationError(details="Ticket Print List doesn't exist")

        if ticket.print_list.print_for_pay:
            ticket_print_list.is_active = False
            ticket_print_list.printed = True
            for order in ticket.orders:
                order.printed = True
        else:
            for order in ticket.orders:
                if order.id in ticket_orders:
                    order.printed = True
            ticket_print_list.is_active = False

        session.commit()


@sio.event
async def ticket_print_error(sid, data):
    from src.db.session import db_context
    from src.models import PrintListTicket

    ticket_id = data["ticket_id"]

    with db_context() as session:
        ticket_print_list = (
            session.query(PrintListTicket).filter_by(id_ticket=ticket_id).first()
        )

        if not ticket_print_list:
            return

        ticket_print_list.is_active = False
        ticket_print_list.printed = False

        socket_logger.info(
            "[event:ticket_print_error] [room:%s] [sid:%s] [ticket_id:%d] Printed Error",
            PRINTERS_ROOM,
            sid,
            ticket_print_list.ticket.id,
        )
        session.commit()


async def ticket_watcher():
    socket_logger.info("Ticket watcher initialized")
    last_count = 0

    while True:
        await sio.sleep(5)

        tickets = get_pending_tickets()
        count = len(tickets)

        if not tickets:
            if last_count != 0:
                socket_logger.debug("No pending tickets")
            last_count = 0
            continue

        if count != last_count:
            socket_logger.info("[Ticket Watcher] Pending tickets: %d", count)
            last_count = count

        await sio.emit(
            "pending_tickets",
            {"tickets_list": tickets},
            room=PRINTERS_ROOM,
        )


def get_pending_tickets():
    from sqlalchemy import and_, or_

    from src.db.session import db_context
    from src.models import Order, OrderAddons, PrintListTicket, Product, Ticket

    with db_context() as session:
        tickets = (
            session.query(PrintListTicket)
            .join(PrintListTicket.ticket)
            .join(Ticket.orders.and_(Order.is_active))
            .options(
                joinedload(PrintListTicket.ticket)
                .joinedload(Ticket.orders.and_(Order.is_active))
                .joinedload(Order.product)
                .joinedload(Product.category),
                joinedload(PrintListTicket.ticket)
                .joinedload(Ticket.orders.and_(Order.is_active))
                .joinedload(Order.order_addons)
                .joinedload(OrderAddons.product_addons),
                joinedload(PrintListTicket.ticket).joinedload(Ticket.restaurant_table),
                joinedload(PrintListTicket.ticket).joinedload(Ticket.user),
            )
            .filter(
                PrintListTicket.is_active,
                or_(
                    and_(
                        PrintListTicket.print_for_pay,
                        PrintListTicket.printed.is_(False),
                    ),
                    and_(
                        PrintListTicket.print_for_pay.is_(False),
                        Order.printed.is_(False),
                    ),
                ),
            )
            .distinct()
            .all()
        )
        return [
            schema.SocketTicket.model_validate(t.ticket).model_dump(mode="json")
            for t in tickets
        ]
