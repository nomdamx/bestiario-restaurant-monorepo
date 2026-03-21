from pydantic import BaseModel, Field, field_validator

from src.core import BaseResponseModelSchema
from src.features.product.schema import ResponseProduct
from src.features.product_addons.schema import ResponseProductAddon
from src.models.products.category import ProductMenuSectionEnum


class PayloadOrderAddon(BaseModel):
    id_product_addons: int
    id_order: int


class PayloadUpdateOrderAddon(BaseModel):
    id_product_addons: int | None = Field(default=None)
    id_order: int | None = Field(default=None)


class ResponseOrderAddon(BaseResponseModelSchema):
    id_product_addons: int
    id_order: int
    unit_price: float
    product_addons: ResponseProductAddon
