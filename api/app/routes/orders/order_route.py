from flask import Blueprint,request

from app.controllers import OrderController

from app.routes.base_route import BaseRoute

order_bp = Blueprint("order",__name__)
order_controller = OrderController()

class OrderRoute(BaseRoute):
    def __init__(self):
        super().__init__(order_bp,order_controller)

    @order_bp.route("/",methods=["POST","OPTIONS"],strict_slashes=False)
    def route_add_order_with_addons():
        if request.method == "OPTIONS":
            return "",204
        return order_controller.controller_register_with_product_addons(request)
    
    @order_bp.route("/<int:id>",methods=["DELETE"],strict_slashes=False)
    def route_delete_order(id):
        return order_controller.controller_delete(id=id)