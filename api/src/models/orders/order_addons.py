from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    ForeignKey,
    event,
)
from sqlalchemy.orm import Mapped, mapped_column, object_session, relationship

from src.models.base_model import BaseCreatedModel

if TYPE_CHECKING:
    from src.models import Order, ProductAddons


class OrderAddons(BaseCreatedModel):
    __tablename__ = "order_addons"

    id_product_addons: Mapped[int] = mapped_column(ForeignKey("product_addons.id"))
    id_order: Mapped[int] = mapped_column(ForeignKey("order.id"))
    unit_price: Mapped[float] = mapped_column(nullable=False)

    order: Mapped["Order"] = relationship("Order", back_populates="order_addons")
    product_addons: Mapped["ProductAddons"] = relationship(
        "ProductAddons", back_populates="order_addons"
    )
