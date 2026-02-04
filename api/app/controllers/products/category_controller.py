from app.controllers.base_controller import BaseController

from app.models import (
    Category,
)

from app.schemas import (
    CategorySchema,
)

class CategoryController(BaseController):
    def __init__(self):
        super().__init__(
            model=Category,
            schema=CategorySchema
        )
