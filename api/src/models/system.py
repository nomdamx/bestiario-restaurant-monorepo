from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from .base_model import BaseModel


class SystemConfig(BaseModel):
    __tablename__ = "system_config"

    key: Mapped[str] = mapped_column(nullable=False)
    value: Mapped[str] = mapped_column(nullable=False)

    def check_bool(self) -> bool:
        return True if self.value.lower().replace(" ", "") == "true" else False
