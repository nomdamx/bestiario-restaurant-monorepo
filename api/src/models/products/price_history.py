from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from src.models.base_model import BaseCreatedModel

if TYPE_CHECKING:
    from src.models import Product


class PriceHistory(BaseCreatedModel):
    __tablename__ = "price_history"

    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))

    old_price: Mapped[float] = mapped_column(nullable=False)
    new_price: Mapped[float] = mapped_column(nullable=False)

    changed_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )

    product: Mapped["Product"] = relationship("Product")
