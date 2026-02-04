from app.controllers.base_controller import BaseController

from app.models import (
    OrderAddons,
)

from app.schemas import (
    OrderAddonsSchema,
)

class OrderAddonsController(BaseController):
    def __init__(self):
        super().__init__(
            model=OrderAddons,
            schema=OrderAddonsSchema
        )