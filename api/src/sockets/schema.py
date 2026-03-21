from pydantic import Field, field_validator, model_validator

from src.core import BaseResponseModelSchema
from src.features.auth.schema import ResponseUserForRelations
from src.features.order.schema import ResponseOrderRelationOrderAddon
from src.features.restaurant_tables.schema import ResponseRestaurantTable


class SocketTicket(BaseResponseModelSchema):
    uuid: str
    id_restaurant_table: int
    is_paid: bool
    comments: str | None = Field(default=None)
    client_name: str | None = Field(default=None)
    id_user: int
    ticket_number: int
    total: int
    restaurant_table: ResponseRestaurantTable
    user: ResponseUserForRelations
    orders: list[ResponseOrderRelationOrderAddon]
    print_for_pay: bool | None = None

    @model_validator(mode="before")
    @classmethod
    def extract_print_for_pay(cls, data):
        if hasattr(data, "print_list") and data.print_list:
            data.__dict__["print_for_pay"] = data.print_list.print_for_pay
        return data
