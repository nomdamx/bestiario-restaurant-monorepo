from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import uuid4

from sqlalchemy import ForeignKey, UniqueConstraint, event, func
from sqlalchemy.orm import Mapped, Session, mapped_column, relationship

from src.models.base_model import BaseCreatedModel

if TYPE_CHECKING:
    from src.models import Order, PrintListTicket, RestaurantTable, User

from src.utils.dates import get_operational_date


class Ticket(BaseCreatedModel):
    __tablename__ = "ticket"

    __table_args__ = (
        UniqueConstraint(
            "operational_date", "ticket_number", name="uq_ticket_operational_day_number"
        ),
    )

    uuid: Mapped[str | None] = mapped_column(default=None, unique=True)
    id_restaurant_table: Mapped[int] = mapped_column(ForeignKey("restaurant_table.id"))
    comments: Mapped[str] = mapped_column(default="")
    client_name: Mapped[str] = mapped_column(default=None, nullable=True)
    is_paid: Mapped[bool] = mapped_column(default=False)
    id_user: Mapped[int] = mapped_column(ForeignKey("user.id"))

    total: Mapped[float | None] = mapped_column(default=0.0, nullable=True)

    ticket_number: Mapped[int] = mapped_column(nullable=False)
    operational_date: Mapped[datetime] = mapped_column(nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="tickets")
    restaurant_table: Mapped["RestaurantTable"] = relationship(
        "RestaurantTable", back_populates="tickets"
    )
    orders: Mapped[list["Order"]] = relationship(
        "Order",
        back_populates="ticket",
        cascade="all, delete-orphan",
        order_by="Order.id",
    )
    print_list: Mapped["PrintListTicket"] = relationship(
        "PrintListTicket", back_populates="ticket", cascade="all, delete-orphan"
    )