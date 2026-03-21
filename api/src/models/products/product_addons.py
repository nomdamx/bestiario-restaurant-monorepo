from typing import TYPE_CHECKING

from sqlalchemy import event
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base_model import BaseCreatedModel

if TYPE_CHECKING:
    from src.models import OrderAddons, Product

from datetime import datetime
from enum import StrEnum

from sqlalchemy import Enum as SAEnum


class ProductAddonsEnum(StrEnum):
    OUTSIDE = "outside"


class ProductAddons(BaseCreatedModel):
    __tablename__ = "product_addons"

    type: Mapped[ProductAddonsEnum] = mapped_column(
        SAEnum(
            ProductAddonsEnum,
            name="addon_type_enum",
            values_callable=lambda x: [e.value for e in x],  # type: ignore
        ),
        nullable=False,
        default=ProductAddonsEnum.OUTSIDE,
    )
    name: Mapped[str] = mapped_column(default="")
    price: Mapped[float] = mapped_column(default=0.0)

    order_addons: Mapped[list["OrderAddons"]] = relationship(
        "OrderAddons", back_populates="product_addons", cascade="all, delete-orphan"
    )
    mirror_product: Mapped["Product"] = relationship(
        "Product", back_populates="source_addon", uselist=False
    )
