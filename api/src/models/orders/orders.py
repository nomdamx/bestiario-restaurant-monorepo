from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import (
    ForeignKey,
    event,
)
from sqlalchemy.orm import Mapped, mapped_column, object_session, relationship

from src.models.base_model import BaseCreatedModel

if TYPE_CHECKING:
    from src.models import OrderAddons, Product, Ticket


class Order(BaseCreatedModel):
    __tablename__ = "order"

    id_ticket: Mapped[int] = mapped_column(ForeignKey("ticket.id"))
    id_product: Mapped[int] = mapped_column(ForeignKey("product.id"))

    unit_price: Mapped[float] = mapped_column(nullable=False)
    quantity: Mapped[int] = mapped_column(default=1)
    total: Mapped[float | None] = mapped_column(default=0.0, nullable=True)

    finished_status: Mapped[bool] = mapped_column(default=False)
    printed: Mapped[bool] = mapped_column(default=False)

    ticket: Mapped["Ticket"] = relationship("Ticket", back_populates="orders")
    product: Mapped["Product"] = relationship("Product", back_populates="orders")
    order_addons: Mapped[list["OrderAddons"]] = relationship(
        "OrderAddons", back_populates="order", cascade="all, delete-orphan"
    )
