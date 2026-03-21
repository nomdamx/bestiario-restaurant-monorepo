from pydantic import BaseModel, Field, field_validator

from src.core import BaseResponseModelSchema


class PayloadRestaurantTable(BaseModel):
    number: int


class PayloadUpdateRestaurantTable(BaseModel):
    number: int


class ResponseRestaurantTable(BaseResponseModelSchema):
    number: int
