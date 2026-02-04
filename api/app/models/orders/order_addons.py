from app.models import (
    BaseCreatedModel,
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

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models import (
        ProductAddons,
        Order
    )

from .recalc_totals import recalc_order_total

class OrderAddons(BaseCreatedModel):
    id_product_addons:Mapped[int] = mapped_column(ForeignKey("product_addons.id"))
    id_order:Mapped[int] = mapped_column(ForeignKey("order.id"))
    unit_price: Mapped[float] = mapped_column(nullable=False)

    order:Mapped["Order"] = relationship("Order",back_populates="order_addons")
    product_addons:Mapped["ProductAddons"] = relationship("ProductAddons",back_populates="order_addons")

    def get_reference_json(self,include_relationships = None):
        return {
            "id":self.id,
            "is_active":self.is_active,
            "created_at":self.created_at,
            "deleted_at":self.deleted_at,
            "id_product_addons":self.id_product_addons,
            "id_order":self.id_order,
            "product_addons":{
                "id":self.product_addons.id,
                "is_active":self.product_addons.is_active,
                "price":self.unit_price,
                "name":self.product_addons.name,
                "type":self.product_addons.type
            }
        }
    
    def soft_delete(self):
        ticket_id = self.order.id_ticket
        self.is_active = False
        self.deleted_at = datetime.now()
        session = object_session(self)

        if session:
            session.add(self)
            session.commit()

        from app.models.orders import recalc_ticket_total
        recalc_ticket_total(session.connection(), ticket_id)

@event.listens_for(OrderAddons, "before_insert")
def freeze_addon_price(mapper, connection, target: OrderAddons):
    from app.models import ProductAddons

    addon = connection.execute(
        ProductAddons.__table__.select()
        .where(ProductAddons.__table__.c.id == target.id_product_addons)
    ).fetchone()

    target.unit_price = float(addon.price)
    
@event.listens_for(OrderAddons,"after_insert")
@event.listens_for(OrderAddons,"after_update")
def calc_order_addons(mapper, connection, target:OrderAddons):
    recalc_order_total(
        connection = connection,
        order_id = target.id_order
    )