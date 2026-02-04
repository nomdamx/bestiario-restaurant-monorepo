from app.models import (
    BaseCreatedModel
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models import (
        Product
    )

from sqlalchemy.dialects.postgresql import ENUM
from app.schemas import ProductMenuSectionEnum

menu_section_enum = ENUM(*[menu_section.value for menu_section in ProductMenuSectionEnum], name="menu_section_enum",create_type=True)

class Category(BaseCreatedModel):
    name:Mapped[str] = mapped_column(default="")
    ingredient_description:Mapped[str] = mapped_column(default="")
    menu_section:Mapped[ProductMenuSectionEnum] = mapped_column(menu_section_enum,default=ProductMenuSectionEnum.BAR.value)

    products:Mapped[list["Product"]] = relationship("Product",back_populates="category",cascade="all, delete-orphan")