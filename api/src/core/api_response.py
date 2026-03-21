from typing import Generic, TypeVar, cast

from pydantic import BaseModel, Field, field_validator
from pydantic.generics import GenericModel

T = TypeVar("T")


class Pagination(BaseModel):
    page: int = Field(default=1, ge=1)
    pages: int = Field(default=1, ge=1)
    limit: int = Field(default=1, ge=1, le=100)
    total: int = Field(default=0, ge=0)


class Metadata(BaseModel):
    response_type: str
    size: int
    pagination: Pagination


class APIResponse(GenericModel, Generic[T]):
    response: list[T]
    metadata: Metadata


def build_response[T](
    data: list[T] | T, *, response_type: str, pagination: Pagination | None = None
) -> APIResponse[T]:
    response_data: list[T] = normalize_to_list(data)
    if pagination is None:
        pagination = Pagination()
        pagination.total = len(response_data)

    return APIResponse[T](
        response=response_data,
        metadata=Metadata(
            response_type=response_type, size=len(response_data), pagination=pagination
        ),
    )


def normalize_to_list(data: T | list[T]) -> list[T]:
    if isinstance(data, list):
        return cast(list[T], data)
    return [data]
