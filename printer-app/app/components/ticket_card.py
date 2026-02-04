import customtkinter as ctk
from app.schema import TicketSchema
from app.services import retry_ticket

class TicketCard(ctk.CTkFrame):
    def __init__(self,parent,ticket:TicketSchema,show_retry=False):
        super().__init__(
            parent,
            corner_radius=8,
            fg_color=("white", "#2a2a2a"),
        )

        self.ticket:TicketSchema = ticket
        self.show_retry = show_retry

        table_text = "Para Llevar" if ticket.restaurant_table.number == 0 else f"Mesa: #{ticket.restaurant_table.number}"
        row1 = ctk.CTkFrame(self, fg_color="transparent")
        row1.pack(fill="x", padx=12, pady=(8, 2))

        ctk.CTkLabel(row1, text=f"ID: {ticket.id}").pack(side="left")
        ctk.CTkLabel(row1, text=table_text).pack(side="right")

        row2 = ctk.CTkFrame(self, fg_color="transparent")
        row2.pack(fill="x", padx=12, pady=(0, 6))

        ctk.CTkLabel(row2, text=f"UUID: {ticket.uuid}").pack(side="left")
        ctk.CTkLabel(row2, text=f"${ticket.total}").pack(side="right")

        if show_retry:
            ctk.CTkButton(
                self,
                text="Reintentar",
                height=28,
                command=self._on_retry
            ).pack(padx=12, pady=(0, 8), anchor="e")

    def _on_retry(self):
        retry_ticket(self.ticket.id)