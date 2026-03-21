from pydantic import BaseModel, Field, field_validator

from src.core import BaseResponseModelSchema
from src.features.auth.schema import ResponseUserForRelations
from src.features.order.schema import ResponseOrderRelationOrderAddon
from src.features.restaurant_tables.schema import ResponseRestaurantTable


class PayloadTicket(BaseModel):
    id_restaurant_table: int


class PayloadUpdateTicket(BaseModel):
    id_restaurant_table: int
    comments: str | None = Field(default=None)
    client_name: str | None = Field(default=None)


class PayloadUpdateCommentsTicket(BaseModel):
    comments: str


class PayloadUpdateClientTicket(BaseModel):
    client_name: str


class PayloadUpdatePaidTicket(BaseModel):
    is_paid: bool


class ResponseTicket(BaseResponseModelSchema):
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


class ResponseTicketRelations(ResponseTicket):
    orders: list[ResponseOrderRelationOrderAddon]
