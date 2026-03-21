from pydantic import BaseModel, Field, field_validator

from src.core import BaseResponseModelSchema


# THIS IS BECAUSE OF CIRCULAR IMPORT, FIX LATER
class ResponseCategory(BaseResponseModelSchema):
    name: str
    ingredient_description: str
    menu_section: str


class PayloadProduct(BaseModel):
    name: str
    complete_name: str | None = Field(default=None)
    id_category: int
    ingredient_description: str
    price: float = Field(gt=0)
    disponibility_status: bool | None = Field(default=True)
    id_source_addon: int | None = Field(default=None)


class PayloadUpdateProduct(BaseModel):
    name: str | None = Field(default=None)
    complete_name: str | None = Field(default=None)
    id_category: int | None = Field(default=None)
    ingredient_description: str | None = Field(default=None)
    disponibility_status: bool | None = Field(default=None)


class PayloadUpdatePriceProduct(BaseModel):
    price: float = Field(gt=0)


class ResponseProduct(BaseResponseModelSchema):
    name: str
    complete_name: str
    id_category: int
    ingredient_description: str
    price: float = Field(gt=0)
    category: ResponseCategory
