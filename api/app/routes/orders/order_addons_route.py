from flask import Blueprint

from app.controllers import OrderAddonsController
from app.routes.base_route import BaseRoute

order_addons_bp = Blueprint("order_addons",__name__)
order_addons_controller = OrderAddonsController()

class OrderAddonsRoute(BaseRoute):
    def __init__(self):
        super().__init__(order_addons_bp,order_addons_controller)