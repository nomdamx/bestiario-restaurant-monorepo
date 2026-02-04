from app.models import (
    BaseCreatedModel
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from sqlalchemy import (
    ForeignKey,
    event,
    inspect
)

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models import (
        Order,
        ProductAddons,
        Category
    )


from datetime import datetime

class Product(BaseCreatedModel):
    name:Mapped[str] = mapped_column(default="")
    complete_name:Mapped[str] = mapped_column(default="")
    id_category:Mapped[int] = mapped_column(ForeignKey("category.id"))
    ingredient_description:Mapped[str] = mapped_column(default="")
    price:Mapped[float] = mapped_column(default=0.0)
    disponibility_status:Mapped[bool] = mapped_column(default=True)

    id_source_addon:Mapped[int] = mapped_column(ForeignKey("product_addons.id"),nullable=True,unique=True)

    category:Mapped["Category"] = relationship("Category",back_populates="products")
    orders:Mapped[list["Order"]] = relationship("Order",back_populates="product",cascade="all, delete-orphan")
    source_addon:Mapped["ProductAddons"] = relationship("ProductAddons",back_populates="mirror_product",cascade="all, delete-orphan",single_parent=True,uselist=True)

    def get_reference_json(self,include_relationships = None):
        return {
            "id":self.id,
            "is_active":self.is_active,
            "created_at":self.created_at,
            "deleted_at":self.deleted_at,
            "name":self.name,
            "complete_name":self.complete_name,
            "id_category":self.id_category,
            "ingredient_description":self.ingredient_description,
            "price":self.price,
            "disponibility_status":self.disponibility_status,
            "category":self.category.get_json()
        }
    
@event.listens_for(Product, "before_update")
def block_update_if_active_tickets(mapper, connection, target: "Product"):
    from app.models import Order, Ticket

    result = connection.execute(
        Order.__table__
        .join(Ticket.__table__, Order.__table__.c.id_ticket == Ticket.__table__.c.id)
        .select()
        .where(Order.__table__.c.id_product == target.id)
        .where(Ticket.__table__.c.is_paid == False)
        .where(Ticket.__table__.c.is_active == True)
        .limit(1)
    ).fetchone()

    if result:
        raise ValueError(
            "Can't be modified while there is active tickets"
        )
    
@event.listens_for(Product, "before_update")
def product_price_history(mapper, connection, target: Product):
    from app.models import PriceHistory
    if target.id_source_addon:
        return

    state = inspect(target)
    hist = state.attrs.price.history

    if not hist.has_changes():
        return

    old_price = hist.deleted[0] if hist.deleted else None
    new_price = hist.added[0] if hist.added else None

    if old_price is None or new_price is None:
        return

    connection.execute(
        PriceHistory.__table__.insert().values(
            product_id=target.id,
            old_price=float(old_price),
            new_price=float(new_price),
            changed_at=datetime.utcnow()
        )
    )

@event.listens_for(Product,"before_insert")
@event.listens_for(Product,"before_update")
def check_positive_price(mapper,connection,target:Product):
    if not target.price:
        raise ValueError("Price must have a value")
    
    if not isinstance(target.price,float):
        raise TypeError(f"Expected float, got {type(target.price).__name__}")
    
    if target.price < 0:
        raise ValueError("Price can't be negative")