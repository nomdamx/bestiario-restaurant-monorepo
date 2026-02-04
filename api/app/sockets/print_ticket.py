from app import db, socketio

from datetime import datetime, date
from uuid import UUID
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask import Flask, request
import logging

PRINTERS_ROOM = "printers"

session = db.session
socket_logger = logging.getLogger("socket")

@socketio.on("connect")
def handle_connect():
    socket_logger.info(
        "[event:connect] "
        "[sid:%s] ",
        request.sid
    )

@socketio.on("disconnect")
def handle_disconnect():
    socket_logger.info(
        "[event:disconnect] "
        "[room:%s] "
        "[sid:%s] ",
        PRINTERS_ROOM,
        request.sid
    )
    leave_room(PRINTERS_ROOM)

@socketio.on("join")
def handle_join(data):
    join_room(PRINTERS_ROOM)
    tickets = get_pending_tickets()
    socket_logger.info(
        "[event:join] "
        "[room:%s] "
        "[sid:%s] ",
        PRINTERS_ROOM,
        request.sid
    )
    if tickets:
        emit(
            "pending_tickets",
            {"tickets_list": socket_safe(tickets)},
            room=PRINTERS_ROOM
        )

@socketio.on("resend")
def handle_resend():
    tickets = get_pending_tickets()
    socket_logger.info(
        "[event:resend] "
        "[room:%s] "
        "[sid:%s] ",
        PRINTERS_ROOM,
        request.sid
    )
    if tickets:
        socket_logger.info(
            "[event:resend] "
            "Pending tickets: %d",
            len(tickets)
        )
        emit(
            "pending_tickets",
            {"tickets_list": socket_safe(tickets)},
            room=PRINTERS_ROOM
        )

@socketio.on("ticket_printed")
def handle_printed_correctly(data):
    from app.models import PrintListTicket, Ticket

    ticket_id = data["ticket_id"]
    ticket_orders = data["orders"]

    try:
        ticket_print_list = (
            session.query(PrintListTicket)
            .filter_by(id_ticket=ticket_id)
            .first()
        )

        ticket = session.query(Ticket).filter_by(id=ticket_id).first()

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
            
        socket_logger.info(
            "[event:ticket_printed] "
            "[room:%s] "
            "[sid:%s] "
            "[ticket_id:%d] Correctly printed",
            PRINTERS_ROOM,
            request.sid,
            ticket.id
        )
        session.commit()

    except Exception as e:
        session.rollback()
        raise e
    
@socketio.on("ticket_print_error")
def handle_ticket_print_error(data):
    from app.models import PrintListTicket

    ticket_id = data["ticket_id"]

    p = (
        session.query(PrintListTicket)
        .filter_by(id_ticket=ticket_id)
        .first()
    )

    if not p:
        return

    p.is_active = False
    p.printed = False

    session.commit()
    socket_logger.info(
        "[event:ticket_print_error] "
        "[room:%s] "
        "[sid:%s] "
        "[ticket_id:%d] Printed Error",
        PRINTERS_ROOM,
        request.sid,
        p.ticket.id
    )


def ticket_watcher(app:Flask):
    socket_logger.info("Ticket watcher initialized")
    with app.app_context():
        while True:
            socketio.sleep(5)

            tickets = get_pending_tickets()
            if not tickets:
                socket_logger.debug(f"No pending Tickets")
                continue

            socket_logger.info(
                "[event:pending_tickets] "
                "Pending tickets: %d",
                len(tickets)
            )

            socketio.emit(
                "pending_tickets",
                {"tickets_list": socket_safe(tickets)},
                room=PRINTERS_ROOM
            )

def get_pending_tickets():
    from app.models import PrintListTicket, Order, Ticket
    from sqlalchemy import or_, and_

    tickets = (
        session.query(PrintListTicket)
        .join(PrintListTicket.ticket)
        .join(Ticket.orders)
        .filter(
            PrintListTicket.is_active == True,
            or_(
                and_(
                    PrintListTicket.print_for_pay == True,
                    PrintListTicket.printed == False,
                ),

                and_(
                    PrintListTicket.print_for_pay == False,
                    Order.printed == False
                )
            )
        )
        .distinct()
        .all()
    )

    return [t.ticket.get_json_for_print() for t in tickets]

def socket_safe(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()

    if isinstance(obj, UUID):
        return str(obj)

    if isinstance(obj, dict):
        return {k: socket_safe(v) for k, v in obj.items()}

    if isinstance(obj, list):
        return [socket_safe(v) for v in obj]

    return obj