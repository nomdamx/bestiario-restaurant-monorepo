from flask import Blueprint

from app.controllers import RestaurantTableController

from app.routes.base_route import BaseRoute

restaurant_table_bp = Blueprint("restaurant_table",__name__)
restaurant_table_controller = RestaurantTableController()

class RestaurantTableRoute(BaseRoute):
    def __init__(self):
        super().__init__(restaurant_table_bp,restaurant_table_controller)