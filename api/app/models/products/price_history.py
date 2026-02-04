from app.models import (
    BaseCreatedModel
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from sqlalchemy import (
    ForeignKey,
    DateTime,
)

from datetime import datetime
from sqlalchemy.sql import func

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models import (
        Product
    )

class PriceHistory(BaseCreatedModel):
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))
    
    old_price: Mapped[float] = mapped_column(nullable=False)
    new_price: Mapped[float] = mapped_column(nullable=False)

    changed_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    product: Mapped["Product"] = relationship("Product")