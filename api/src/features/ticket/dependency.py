from typing import Annotated

from fastapi import Depends
from pydantic import BaseModel, Field, field_validator

from src.core.dependency import BaseFilter


class FilterTicket(BaseFilter):
    uuid: str | None = Field(default=None)
    is_paid: bool = Field(default=False)


class FilterPrintPayment(BaseFilter):
    for_pay: bool = Field(default=False)


FilterTicketDependency = Annotated[FilterTicket, Depends()]

FilterPrintPaymentDepndency = Annotated[FilterPrintPayment, Depends()]
