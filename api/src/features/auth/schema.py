from typing import Annotated

from pydantic import BaseModel, Field, field_validator
from pydantic_core.core_schema import ValidationInfo

from src.core import BaseResponseModelSchema
from src.utils.dates import create_timestampt

MIN_LEN_USERNAME = 3


class PayloadRegisterUser(BaseModel):
    username: str
    display_name: str
    password: str

    @field_validator("username", mode="before")
    @classmethod
    def validate_username(cls, username: str):
        if not len(username) > MIN_LEN_USERNAME:
            raise ValueError(f"Username must be more than {MIN_LEN_USERNAME} chars")

        return username

    @field_validator("password", mode="before")
    @classmethod
    def validate_password(cls, password: str):
        # More validations like password contains numbers and chars or etc, later on
        return password

    @field_validator("display_name", mode="before")
    def validate_display_name(cls, display_name: str, info: ValidationInfo):
        return display_name or info.data.get("username", "")


class PayloadValidateUser(BaseModel):
    username: str
    password: str


class PayloadCreateSession(BaseModel):
    id_user: int
    token: str
    expires_at: Annotated[int, Field(description="UTC unix timestamp")] = Field(
        default_factory=create_timestampt
    )


class PayloadToken(BaseModel):
    token: str


class PayloadSystemValue(BaseModel):
    value: str


# RESPONSES
class ResponseUser(BaseResponseModelSchema):
    username: str
    display_name: str
    auth_level: str


class ResponseUserForRelations(BaseResponseModelSchema):
    username: str
    display_name: str


class ResponseToken(BaseModel):
    token: str


class ResponseSession(BaseModel):
    expires_at: int
    user: ResponseUser
