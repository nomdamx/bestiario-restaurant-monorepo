from app.controllers.base_controller import BaseController

from app.models import (
    PrintListTicket
)

from app.schemas import (
    PrintListTicketSchema
)

class PrintListTicketController(BaseController):
    def __init__(self):
        super().__init__(
            model=PrintListTicket,
            schema=PrintListTicketSchema
        )