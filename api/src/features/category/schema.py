from pydantic import BaseModel, Field, field_validator

from src.core import BaseResponseModelSchema
from src.features.product.schema import ResponseProduct
from src.models.products.category import ProductMenuSectionEnum


class PayloadCategory(BaseModel):
    name: str
    ingredient_description: str
    menu_section: ProductMenuSectionEnum = Field(default=ProductMenuSectionEnum.BAR)


class PayloadUpdateCategory(BaseModel):
    name: str | None = Field(default=None)
    ingredient_description: str | None = Field(default=None)
    menu_section: ProductMenuSectionEnum | None = Field(default=None)


class ResponseCategory(BaseResponseModelSchema):
    name: str
    ingredient_description: str
    menu_section: str


class ResponseMenuCategory(ResponseCategory):
    products: list[ResponseProduct]
