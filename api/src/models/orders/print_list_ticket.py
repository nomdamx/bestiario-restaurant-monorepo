from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base_model import BaseCreatedModel

if TYPE_CHECKING:
    from src.models import Ticket


class PrintListTicket(BaseCreatedModel):
    __tablename__ = "print_list_ticket"

    id_ticket: Mapped[int] = mapped_column(ForeignKey("ticket.id"))
    printed: Mapped[bool] = mapped_column(default=False)
    print_for_pay: Mapped[bool] = mapped_column(default=False)

    ticket: Mapped["Ticket"] = relationship("Ticket", back_populates="print_list")
