from typing import Annotated

from fastapi import Depends
from pydantic import BaseModel, Field, field_validator


class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=100, ge=1, le=100)

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.limit


PaginationDependency = Annotated[PaginationParams, Depends()]


class BaseFilter(BaseModel):
    is_active: bool = Field(default=True)


BaseFilterDependency = Annotated[BaseFilter, Depends()]
