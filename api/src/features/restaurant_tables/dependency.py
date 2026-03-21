from typing import Annotated

from fastapi import Depends
from pydantic import Field

from src.core.dependency import BaseFilter


class FilterRestaurantTable(BaseFilter):
    number: int | None = Field(default=None)


FilterRestaurantTableDependency = Annotated[FilterRestaurantTable, Depends()]
