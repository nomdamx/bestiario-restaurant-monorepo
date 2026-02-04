from app.models import (
    BaseCreatedModel
)

from datetime import datetime

from sqlalchemy.orm import (
    object_session,
    Mapped,
    mapped_column,
    relationship
)

from sqlalchemy import (
    ForeignKey,
    event,
)

from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from app.models import (
        Product,
        OrderAddons,
        Ticket
    )

from .recalc_totals import recalc_order_total

class Order(BaseCreatedModel):
    id_ticket:Mapped[int] = mapped_column(ForeignKey("ticket.id"))
    id_product:Mapped[int] = mapped_column(ForeignKey("product.id"))

    unit_price: Mapped[float] = mapped_column(nullable=False)
    quantity:Mapped[int] = mapped_column(default=1)
    total:Mapped[Optional[float]] = mapped_column(default=0.0,nullable=True)


    finished_status:Mapped[bool] = mapped_column(default=False)
    printed:Mapped[bool] = mapped_column(default=False)


    ticket:Mapped["Ticket"] = relationship("Ticket",back_populates="orders")
    product:Mapped["Product"] = relationship("Product",back_populates="orders")
    order_addons:Mapped[list["OrderAddons"]] = relationship("OrderAddons",back_populates="order",cascade="all, delete-orphan")

    def get_total(self):
        addons_total = sum(
            a.unit_price for a in self.order_addons if a.is_active
        )
        return self.quantity * (self.unit_price + addons_total)
        
    def get_reference_json(self,include_relationshios = None):
        ticket = self.ticket.get_json() if include_relationshios else None
        return {
            "id":self.id,
            "is_active":self.is_active,
            "created_at":self.created_at,
            "deleted_at":self.deleted_at,
            "id_ticket":self.id_ticket,
            "id_product":self.id_product,
            "product":{
                "id":self.product.id,
                "is_active":self.product.is_active,
                "name":self.product.name,
                "id_category":self.product.id_category,
                "price":self.unit_price,
                "category":self.product.category.get_json()
            },
            "quantity":self.quantity,
            "finished_status":self.finished_status,
            "printed":self.printed,
            "total":self.total,
            "ticket":ticket,
            "order_addons":[addon.get_reference_json() for addon in self.order_addons]
        }
    
    def soft_delete(self):
        ticket_id = self.id_ticket
        print(ticket_id)
        self.is_active = False
        self.deleted_at = datetime.now()
        session = object_session(self)

        if session:
            session.add(self)
            session.commit()

        from app.models.orders import recalc_ticket_total
        recalc_ticket_total(session.connection(), ticket_id)


@event.listens_for(Order, "before_insert")
def freeze_product_price(mapper, connection, target: Order):
    from app.models import Product

    product = connection.execute(
        Product.__table__.select()
        .where(Product.__table__.c.id == target.id_product)
    ).fetchone()

    target.unit_price = float(product.price)

@event.listens_for(Order,"before_insert")
@event.listens_for(Order,"before_update")
def check_positive_quantity(mapper,connection,target:Order):
    if not target.quantity:
        raise ValueError("Quantity must have a value")
    
    if not isinstance(target.quantity,int):
        raise TypeError(f"Expected interger, got {type(target.quantity).__name__}")
    
    if target.quantity < 0:
        raise ValueError("Quantity can't be negative")
    

@event.listens_for(Order,"after_insert")
@event.listens_for(Order,"after_update")
def calc_order(mapper, connection, target:Order):
    recalc_order_total(
        connection = connection,
        order_id = target.id
    )