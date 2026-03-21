from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base_model import BaseCreatedModel

if TYPE_CHECKING:
    from src.models import Ticket


class RestaurantTable(BaseCreatedModel):
    __tablename__ = "restaurant_table"

    number: Mapped[int] = mapped_column(unique=True)

    tickets: Mapped[list["Ticket"]] = relationship(
        "Ticket", back_populates="restaurant_table", cascade="all, delete-orphan"
    )
