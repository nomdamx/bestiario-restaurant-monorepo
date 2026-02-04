import time
from pydantic import BaseModel, Field, field_validator


class PrintBaseModel(BaseModel):
    id:int