from flask import Blueprint,request

from app.controllers import ProductController

from app.routes.base_route import BaseRoute


product_bp = Blueprint("product",__name__)
product_controller = ProductController()

class ProductRoute(BaseRoute):
    def __init__(self):
        super().__init__(product_bp,product_controller)

    @product_bp.route("/price",methods=["PUT"],strict_slashes=False)
    def route_update_price():
        return product_controller.controller_update_price(
            request=request
        )