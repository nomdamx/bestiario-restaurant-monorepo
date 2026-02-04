from app.controllers.base_controller import BaseController

from app.models import (
    RestaurantTable
)

from app.schemas import (
    RestaurantTableSchema
)

class RestaurantTableController(BaseController):
    def __init__(self):
        super().__init__(
            model=RestaurantTable,
            schema=RestaurantTableSchema
        )