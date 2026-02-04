from app.models import (
    BaseCreatedModel
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from sqlalchemy import (
    event
)

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models import (
        Product,
        OrderAddons
    )

from sqlalchemy.dialects.postgresql import ENUM
from app.schemas import ProductAddonsEnum
from datetime import datetime

addon_type_enum = ENUM(*[addon_type.value for addon_type in ProductAddonsEnum], name="addon_type_enum",create_type=True)

class ProductAddons(BaseCreatedModel):
    type:Mapped[ProductAddonsEnum] = mapped_column(addon_type_enum,default=ProductAddonsEnum.OUTSIDE.value)
    name:Mapped[str] = mapped_column(default="")
    price:Mapped[float] = mapped_column(default=0.0)

    order_addons:Mapped[list["OrderAddons"]] = relationship("OrderAddons",back_populates="product_addons",cascade="all, delete-orphan")
    mirror_product:Mapped["Product"] = relationship("Product",back_populates="source_addon",uselist=False)

@event.listens_for(ProductAddons,"before_insert")
@event.listens_for(ProductAddons,"before_update")
def check_positive_price(mapper,connection,target:ProductAddons):
    if not target.price:
        raise ValueError("Price must have a value")
    
    if not isinstance(target.price,float):
        raise TypeError(f"Expected float, got {type(target.price).__name__}")
    
    if target.price < 0:
        raise ValueError("Price can't be negative")


@event.listens_for(ProductAddons, "before_update")
def block_addon_update_if_active_tickets(mapper, connection, target: "ProductAddons"):
    from app.models import OrderAddons, Order, Ticket

    result = connection.execute(
        OrderAddons.__table__
        .join(Order.__table__, OrderAddons.__table__.c.id_order == Order.__table__.c.id)
        .join(Ticket.__table__, Order.__table__.c.id_ticket == Ticket.__table__.c.id)
        .select()
        .where(OrderAddons.__table__.c.id_product_addons == target.id)
        .where(Ticket.__table__.c.is_paid == False)
        .where(Ticket.__table__.c.is_active == True)
        .limit(1)
    ).fetchone()

    if result:
        raise ValueError(
            "Can't be modified while there is active tickets"
        )
    

@event.listens_for(ProductAddons, "after_update")
def sync_price_and_history(mapper, connection, target: ProductAddons):
    from app.models import Product, PriceHistory

    if target.price is None:
        return

    product_table = Product.__table__

    product = connection.execute(
        product_table
        .select()
        .where(product_table.c.id_source_addon == target.id)
        .limit(1)
    ).fetchone()

    if not product:
        return

    old_price = float(product.price)
    new_price = float(target.price)

    if old_price == new_price:
        return

    connection.execute(
        product_table.update()
        .where(product_table.c.id == product.id)
        .values(price=new_price)
    )

    connection.execute(
        PriceHistory.__table__.insert().values(
            product_id=product.id,
            old_price=old_price,
            new_price=new_price,
            changed_at=datetime.utcnow()
        )
    )