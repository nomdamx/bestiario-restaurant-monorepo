import uuid

from app.models import (
    BaseCreatedModel,
)

from datetime import datetime

from sqlalchemy.orm import (
    Session,
    Mapped,
    mapped_column,
    relationship
)

from sqlalchemy import (
    ForeignKey,
    event,
    func,
    UniqueConstraint
)

from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from app.models import (
        User,
        PrintListTicket,
        RestaurantTable,
        Order
    )

from app.utils import get_operational_date


class Ticket(BaseCreatedModel):
    __table_args__ = (
        UniqueConstraint(
            "operational_date",
            "ticket_number",
            name="uq_ticket_operational_day_number"
        ),
    )

    uuid:Mapped[Optional[str]] = mapped_column(default=None,unique=True)
    id_restaurant_table:Mapped[int] = mapped_column(ForeignKey("restaurant_table.id"))
    comments:Mapped[str] = mapped_column(default="")
    client_name:Mapped[str] = mapped_column(default=None,nullable=True)
    is_paid:Mapped[bool] = mapped_column(default=False)
    id_user:Mapped[int] = mapped_column(ForeignKey("user.id"))

    total:Mapped[Optional[float]] = mapped_column(default=0.0,nullable=True)

    ticket_number: Mapped[int] = mapped_column(nullable=False)
    operational_date: Mapped[datetime] = mapped_column(nullable=False)

    user:Mapped["User"] = relationship("User",back_populates="tickets")
    restaurant_table:Mapped["RestaurantTable"] = relationship("RestaurantTable",back_populates="tickets")
    orders:Mapped[list["Order"]] = relationship("Order",back_populates="ticket",cascade="all, delete-orphan",order_by="Order.id")
    print_list:Mapped["PrintListTicket"] = relationship("PrintListTicket",back_populates="ticket",cascade="all, delete-orphan")
    
    def get_json(self,include_relationships = None):
        return {
            "id":self.id,
            "is_active":self.is_active,
            "created_at":self.created_at,
            "deleted_at":self.deleted_at,
            "uuid":self.uuid,
            "ticket_number": self.ticket_number,
            "id_restaurant_table":self.id_restaurant_table,
            "comments":self.comments,
            "client_name":self.client_name,
            "is_paid":self.is_paid,
            "total":self.total,
            "id_user":self.id_user,
            "user":self.user.get_json(),
            "restaurant_table":self.restaurant_table.get_reference_json(),
            "orders":[order.get_reference_json() for order in self.orders if order.is_active]
        }

    def get_json_for_print(self,include_relationships = None):
        return {
            "id":self.id,
            "is_active":self.is_active,
            "created_at":self.created_at,
            "deleted_at":self.deleted_at,
            "uuid":self.uuid,
            "ticket_number": self.ticket_number,
            "id_restaurant_table":self.id_restaurant_table,
            "comments":self.comments,
            "client_name":self.client_name,
            "is_paid":self.is_paid,
            "total":self.total,
            "id_user":self.id_user,
            "user":self.user.get_json(),
            "restaurant_table":self.restaurant_table.get_reference_json(),
            "orders":[order.get_reference_json() for order in self.orders if order.is_active],
            "print_for_pay":self.print_list.print_for_pay if self.print_list else None
        }


@event.listens_for(Ticket, "before_insert")
def generate_uuid(mapper, connection, target:Ticket):

    session = Session(bind = connection)

    while True:
        generated_uuid = str(uuid.uuid4())

        exist = session.query(Ticket).filter_by(uuid = generated_uuid).first()

        if not exist:
            target.uuid = generated_uuid
            break
        
@event.listens_for(Ticket, "before_insert")
def assign_ticket_number(mapper, connection, target: Ticket):
    session = Session(bind=connection)

    op_date = get_operational_date()
    target.operational_date = op_date

    last_number = session.query(
        func.max(Ticket.ticket_number)
    ).filter(
        Ticket.operational_date == op_date
    ).scalar()

    target.ticket_number = (last_number or 0) + 1