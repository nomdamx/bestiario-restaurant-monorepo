from flask import Blueprint

from app.controllers import PrintListTicketController

from app.routes.base_route import BaseRoute

print_list_ticket_bp = Blueprint("print_list_ticket",__name__)
print_list_ticket_controller = PrintListTicketController()

class PrintListTicketRoute(BaseRoute):
    def __init__(self):
        super().__init__(print_list_ticket_bp, print_list_ticket_controller)