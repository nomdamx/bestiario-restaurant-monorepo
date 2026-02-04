# app/services/socket_client.py
import socketio
import time
import threading
from app.config import CONFIG
import json
import hashlib

from app.lib.queue_state import ticket_queue, queue_lock, TicketState
from app.lib.printer import PrinterTicket
from app.schema import TicketSchema
from app.lib.printer_logger import printer_logger


sio = socketio.Client(reconnection=True)
printer = PrinterTicket(socket=sio)

running = False
_worker_thread = None
url = CONFIG.API_URL

@sio.event
def connect():
    printer_logger.info("[SOCKET_CONNECTED] url=%s", url)
    sio.emit("join", {"user": "user_test"})

@sio.event
def disconnect():
    printer_logger.warning("[SOCKET_DISCONNECTED]")

@sio.on("pending_tickets")
def on_print_ticket(data):
    incoming = data["tickets_list"]

    printer_logger.info(
        "[TICKETS_RECEIVED] count=%s",
        len(incoming)
    )

    with queue_lock:
        for ticket in incoming:
            ticket_id = ticket["id"]
            sig = ticket_signature(ticket)

            if ticket_id in ticket_queue:
                existing = ticket_queue[ticket_id]

                existing["data"] = ticket

                if existing["state"] in (
                    TicketState.PENDING,
                    TicketState.PRINTING
                ):
                    printer_logger.info(
                        "[QUEUE_IGNORE_ACTIVE] ticket_id=%s state=%s",
                        ticket_id,
                        existing["state"].name
                    )
                    continue

                if existing["state"] == TicketState.SENT:
                    if existing["signature"] != sig:
                        printer_logger.info(
                            "[QUEUE_REPRINT_CHANGED] ticket_id=%s",
                            ticket_id
                        )
                        existing["state"] = TicketState.PENDING
                        existing["retries"] = 0
                        existing["signature"] = sig
                    else:
                        printer_logger.info(
                            "[QUEUE_IGNORE_SENT_SAME] ticket_id=%s",
                            ticket_id
                        )
                    continue

                if existing["state"] == TicketState.ERROR:
                    printer_logger.warning(
                        "[QUEUE_REACTIVATE_FROM_BACKEND] ticket_id=%s",
                        ticket_id
                    )
                    existing["state"] = TicketState.PENDING
                    existing["signature"] = sig
            else:
                printer_logger.info(
                    "[QUEUE_ADD] ticket_id=%s",
                    ticket_id
                )
                ticket_queue[ticket_id] = {
                    "state": TicketState.PENDING,
                    "data": ticket,
                    "signature": sig,
                    "retries": 0
                }

def _printer_worker():
    while running:
        with queue_lock:
            pending = [
                (tid, t)
                for tid, t in ticket_queue.items()
                if t["state"] == TicketState.PENDING
            ]

        for ticket_id, ticket in pending:
            printer_logger.info(
                "[PRINT_ATTEMPT] ticket_id=%s retry=%s",
                ticket_id,
                ticket["retries"]
            )
            with queue_lock:
                ticket["state"] = TicketState.PRINTING

            success = printer.print_ticket(
                TicketSchema(**ticket["data"])
            )

            with queue_lock:
                if success:
                    printer_logger.info(
                        "[PRINT_SUCCESS] ticket_id=%s",
                        ticket_id
                    )
                    ticket["state"] = TicketState.SENT
                else:
                    ticket["retries"] += 1
                    printer_logger.warning(
                        "[PRINT_RETRY] ticket_id=%s retry=%s",
                        ticket_id,
                        ticket["retries"]
                    )
                    if ticket["retries"] >= CONFIG.MAX_RETRIES:
                        ticket["state"] = TicketState.ERROR

                        printer_logger.error(
                            "[PRINT_BLOCKED] ticket_id=%s retries=%s",
                            ticket_id,
                            ticket["retries"]
                        )

                        sio.emit(
                            "ticket_print_error",
                            {"ticket_id": ticket_id}
                        )

                        print(f"[printer] Ticket {ticket_id} bloqueado por error")
                    else:
                        ticket["state"] = TicketState.PENDING

        time.sleep(1)

def ticket_signature(ticket: dict) -> str:
    relevant = {
        "orders": ticket["orders"],
        "print_for_pay": ticket.get("print_for_pay", False),
    }

    raw = json.dumps(relevant, sort_keys=True)
    sig = hashlib.md5(raw.encode()).hexdigest()

    printer_logger.debug(
        "[SIGNATURE] ticket_id=%s signature=%s",
        ticket.get("id"),
        sig
    )

    return sig

def retry_ticket(ticket_id: int):
    with queue_lock:
        ticket = ticket_queue.get(ticket_id)
        if not ticket:
            return False

        ticket["state"] = TicketState.PENDING
        ticket["retries"] = 0

    return True

def start_socket_client():
    global running, _worker_thread, url

    if running:
        printer_logger.warning("[SERVICE_ALREADY_RUNNING]")
        return

    running = True

    printer_logger.info("[SERVICE_START]")
    sio.connect(url, transports=["websocket"])

    _worker_thread = threading.Thread(
        target=_printer_worker,
        daemon=True
    )
    _worker_thread.start()

    print("[service] Socket client iniciado")

def stop_socket_client():
    global running

    printer_logger.info("[SERVICE_STOP]")
    running = False

    try:
        sio.disconnect()
    except Exception as e:
        printer_logger.error(
            "[SERVICE_STOP_ERROR] %s",
            str(e)
        )

    print("[service] Socket client detenido")
