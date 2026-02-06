from app.models import (
    BaseModel,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

class SystemConfig(BaseModel):
    key:Mapped[str] = mapped_column(nullable=False)
    value:Mapped[str] = mapped_column(nullable=False)

    def check_bool(self) -> bool:
        return True if self.value.lower().replace(" ","") == "true" else False