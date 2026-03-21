from pydantic import BaseModel, Field, field_validator

from src.core import BaseResponseModelSchema
from src.features.order_addons.schema import ResponseOrderAddon
from src.features.product.schema import ResponseProduct


class PayloadOrder(BaseModel):
    id_ticket: int
    id_product: int
    quantity: int = Field(gt=0)
    finished_status: bool = Field(default=False)


class PayloadOrderWithAddons(PayloadOrder):
    order_addons: list[int] = Field(default_factory=list[int])


class PayloadUpdateOrder(BaseModel):
    id_ticket: int | None = Field(default=None)
    id_product: int | None = Field(default=None)
    quantity: int | None = Field(default=None, gt=0)
    finished_status: bool = Field(default=False)


class PayloadUpdateOrderWithAddons(PayloadUpdateOrder):
    order_addons: list[int] = Field(default_factory=list[int])


class ResponseOrder(BaseResponseModelSchema):
    id_ticket: int
    id_product: int
    unit_price: float
    quantity: int
    total: float
    product: ResponseProduct
    order_addons: list[ResponseOrderAddon]
    finished_status: bool
    printed: bool


class ResponseOrderRelationOrderAddon(ResponseOrder):
    order_addons: list[ResponseOrderAddon]
