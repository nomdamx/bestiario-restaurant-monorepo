from enum import StrEnum
from typing import TYPE_CHECKING

from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base_model import BaseCreatedModel


class ProductMenuSectionEnum(StrEnum):
    DRINKS = "drinks"
    BAR = "bar"
    GRILLED = "grilled"


if TYPE_CHECKING:
    from src.models import Product


class Category(BaseCreatedModel):
    __tablename__ = "category"

    name: Mapped[str] = mapped_column(default="")
    ingredient_description: Mapped[str] = mapped_column(default="")
    menu_section: Mapped[ProductMenuSectionEnum] = mapped_column(
        SAEnum(
            ProductMenuSectionEnum,
            name="menu_section_enum",
            values_callable=lambda x: [e.value for e in x],  # type: ignore
        ),
        nullable=False,
        default=ProductMenuSectionEnum.BAR,
    )

    products: Mapped[list["Product"]] = relationship(
        "Product", back_populates="category", cascade="all, delete-orphan"
    )
