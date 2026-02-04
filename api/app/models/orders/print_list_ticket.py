from app.models import (
    BaseCreatedModel,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from sqlalchemy import (
    ForeignKey
)

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models import (
        Ticket
    )

class PrintListTicket(BaseCreatedModel):
    id_ticket:Mapped[int] = mapped_column(ForeignKey("ticket.id"))
    printed:Mapped[bool] = mapped_column(default=False)
    print_for_pay:Mapped[bool] = mapped_column(default=False)

    ticket:Mapped["Ticket"] = relationship("Ticket",back_populates="print_list")

    def get_json(self,include_relationships = None):
        return {
            "id":self.id,
            "is_active":self.is_active,
            "created_at":self.created_at,
            "deleted_at":self.deleted_at,
            "id_ticket":self.id_ticket,
            "printed":self.printed,
            "print_for_pay":self.print_for_pay,
            "ticket":self.ticket.get_json()
        }