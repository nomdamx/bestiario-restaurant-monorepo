from pydantic import BaseModel, Field, field_validator

from src.core import BaseResponseModelSchema
from src.models.products.product_addons import ProductAddonsEnum


class PayloadProductAddon(BaseModel):
    name: str
    price: float = Field(gt=0)
    type: ProductAddonsEnum = Field(default=ProductAddonsEnum.OUTSIDE)


class PayloadUpdateProductAddon(BaseModel):
    name: str
    type: ProductAddonsEnum = Field(default=ProductAddonsEnum.OUTSIDE)


class PayloadUpdatePriceProductAddon(BaseModel):
    price: float = Field(gt=0)


class ResponseProductAddon(BaseResponseModelSchema):
    name: str
    price: float
    type: ProductAddonsEnum
