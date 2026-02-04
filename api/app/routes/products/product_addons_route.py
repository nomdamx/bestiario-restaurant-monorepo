from flask import Blueprint,request

from app.controllers import ProductAddonsController

from app.routes.base_route import BaseRoute


product_addons_bp = Blueprint("product_addons",__name__)
product_addons_controller = ProductAddonsController()

class ProductAddonsRoute(BaseRoute):
    def __init__(self):
        super().__init__(product_addons_bp, product_addons_controller)

    @product_addons_bp.route("/sync-addons",methods=["POST","PUT"],strict_slashes=False)
    def route_sync_addons_in_menu():
        return product_addons_controller.sync_existing_addons_as_products()

    @product_addons_bp.route("/price",methods=["PUT"],strict_slashes=False)
    def route_update_price():
        return product_addons_controller.controller_update_price(
            request=request
        )