from app.models import (
    BaseCreatedModel,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models import (
        Ticket
    )

class RestaurantTable(BaseCreatedModel):
    number:Mapped[int] = mapped_column(unique=True)

    tickets:Mapped[list["Ticket"]] = relationship("Ticket",back_populates="restaurant_table",cascade="all, delete-orphan")
    
    def get_reference_json(self,include_relationships = None):
        return {
            "id":self.id,
            "is_active":self.is_active,
            "created_at":self.created_at,
            "deleted_at":self.deleted_at,
            "number":self.number
        }