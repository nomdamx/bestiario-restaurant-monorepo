from flask import Blueprint,request

from app.controllers import TicketController

from app.routes.base_route import BaseRoute


ticket_bp = Blueprint("ticket",__name__)
ticket_controller = TicketController()

class TicketRoute(BaseRoute):
    def __init__(self):
        super().__init__(ticket_bp,ticket_controller)

    @ticket_bp.route("/client",methods=["PUT"],strict_slashes=False)
    def route_update_client():
        return ticket_controller.controller_update_client(
            request=request
        )
    
    @ticket_bp.route("/comments",methods=["PUT"],strict_slashes=False)
    def route_update_comments():
        return ticket_controller.controller_update_comments(
            request=request
        )
    
    @ticket_bp.route("/pay",methods=["PUT"],strict_slashes=False)
    def route_update_paid_status():
        return ticket_controller.controller_update_paid_status(
            request=request
        )
    
    @ticket_bp.route("/<string:uuid>/print",methods=["POST"],strict_slashes=False)
    def route_print_ticket(uuid):
        return ticket_controller.controller_pending_ticket(
            uuid=uuid,
            request=request
        )