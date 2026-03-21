from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, event, inspect
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base_model import BaseCreatedModel

if TYPE_CHECKING:
    from src.models import Category, Order, ProductAddons


from datetime import datetime


class Product(BaseCreatedModel):
    __tablename__ = "product"

    name: Mapped[str] = mapped_column(default="")
    complete_name: Mapped[str] = mapped_column(default="")
    id_category: Mapped[int] = mapped_column(ForeignKey("category.id"))
    ingredient_description: Mapped[str] = mapped_column(default="")
    price: Mapped[float] = mapped_column(default=0.0)
    disponibility_status: Mapped[bool] = mapped_column(default=True)

    id_source_addon: Mapped[int] = mapped_column(
        ForeignKey("product_addons.id"), nullable=True, unique=True
    )

    category: Mapped["Category"] = relationship("Category", back_populates="products")
    orders: Mapped[list["Order"]] = relationship(
        "Order", back_populates="product", cascade="all, delete-orphan"
    )
    source_addon: Mapped["ProductAddons"] = relationship(
        "ProductAddons",
        back_populates="mirror_product",
        cascade="all, delete-orphan",
        single_parent=True,
        uselist=True,
    )