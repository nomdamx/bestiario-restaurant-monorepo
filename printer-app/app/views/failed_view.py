import customtkinter as ctk
from app.components import TicketCard
from app.lib import ticket_queue, queue_lock, TicketState
from app.schema import TicketSchema


class FailedView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True)
        self.cards = {}

        self.scroll = ctk.CTkScrollableFrame(
            self,
            corner_radius=0
        )
        self.scroll.pack(fill="both", expand=True, padx=10, pady=10)

        self._poll_queue()

    def _poll_queue(self):
        with queue_lock:
            snapshot = dict(ticket_queue)

        self._sync_cards(snapshot)
        self.after(1000, self._poll_queue)

    def _sync_cards(self, tickets):
        for ticket_id in list(self.cards.keys()):
            if (
                ticket_id not in tickets
                or tickets[ticket_id]["state"] != TicketState.ERROR
            ):
                self.cards[ticket_id].destroy()
                del self.cards[ticket_id]

        for ticket_id, ticket in tickets.items():
            if ticket["state"] != TicketState.ERROR:
                continue

            if ticket_id not in self.cards:
                card = TicketCard(
                    self.scroll,
                    TicketSchema(**ticket["data"]),
                    show_retry=True
                )
                card.pack(fill="x", padx=20, pady=8)
                self.cards[ticket_id] = card
