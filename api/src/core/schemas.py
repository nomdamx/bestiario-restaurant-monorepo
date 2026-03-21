import uuid
from datetime import datetime

from pydantic import BaseModel, field_validator


class BaseResponseModelSchema(BaseModel):
    id: int
    created_at: datetime
    deleted_at: datetime | None
    is_active: bool

    class Config:
        from_attributes = True
