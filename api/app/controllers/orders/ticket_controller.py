from app.controllers.base_controller import BaseController

from app.models import (
    Ticket,
    PrintListTicket
)

from app.schemas import (
    TicketSchema,
)
from app import socketio

from flask import Response,json,Request

class TicketController(BaseController):
    def __init__(self):
        super().__init__(
            model=Ticket,
            schema=TicketSchema
        )

    def controller_pending_ticket(self, uuid: int, request: Request):
        try:
            ticket: Ticket = (
                self.session.query(Ticket)
                .filter_by(uuid=uuid)
                .first()
            )
            if not ticket:
                return Response(status=404)

            for_pay = self.__str_to_bool__(request.args.get("for_pay"))

            print_list = (
                self.session.query(PrintListTicket)
                .filter_by(id_ticket=ticket.id)
                .first()
            )

            if not print_list:
                print_list = PrintListTicket(
                    id_ticket=ticket.id,
                    print_for_pay=for_pay,
                    is_active=True,
                    printed=False
                )
                self.session.add(print_list)

            else:
                if print_list.is_active is False:
                    print_list.is_active = True

                if for_pay:
                    print_list.print_for_pay = True
                    print_list.printed = False
                else:
                    print_list.print_for_pay = False

            self.session.commit()

            from app.sockets import PRINTERS_ROOM, socket_safe 
            socketio.emit(
                "pending_tickets",
                {"tickets_list": socket_safe([print_list.ticket.get_json_for_print()])},
                room=PRINTERS_ROOM
            )

            return Response(status=200)

        except Exception:
            self.session.rollback()
            raise

    def controller_update_client(self, request:Request):
        json_request = request.get_json()
        version = request.headers.get("Accept")

        if id and isinstance(id,int):
            if "id" in json_request:
                return Response(response=json.dumps({"message":"id in data and url"}),status=400,mimetype="application/json")
            _id = id
            json_request["id"] = id

        else:
            if not "id" in json_request:
                return Response(response=json.dumps({"message":"Not id in data"}),status=400,mimetype="application/json")
            _id = json_request["id"]
        
        _query:Ticket = self.session.query(self._model).filter_by(id = _id).first()

        if not _query:
            return self.__return_json__(
                response = self.__parse_object__(_query),
                version = version
            )
        
        try:
            _query.client_name = json_request.get("client_name",None)

            self.session.commit()

        except Exception as e:
            self.session.rollback()
            raise e
        
        return self.__return_json__(
            response = self.__parse_object__(_query),
            version = version
        )
    
    def controller_update_comments(self, request:Request):
        json_request = request.get_json()
        version = request.headers.get("Accept")

        if id and isinstance(id,int):
            if "id" in json_request:
                return Response(response=json.dumps({"message":"id in data and url"}),status=400,mimetype="application/json")
            _id = id
            json_request["id"] = id

        else:
            if not "id" in json_request:
                return Response(response=json.dumps({"message":"Not id in data"}),status=400,mimetype="application/json")
            _id = json_request["id"]
        
        _query:Ticket = self.session.query(self._model).filter_by(id = _id).first()

        if not _query:
            return self.__return_json__(
                response = self.__parse_object__(_query),
                version = version
            )
        
        try:
            _query.comments = json_request.get("comments",None)

            self.session.commit()

        except Exception as e:
            self.session.rollback()
            raise e
        
        return self.__return_json__(
            response = self.__parse_object__(_query),
            version = version
        )
    
    def controller_update_paid_status(self, request:Request):
        json_request = request.get_json()
        version = request.headers.get("Accept")

        if id and isinstance(id,int):
            if "id" in json_request:
                return Response(response=json.dumps({"message":"id in data and url"}),status=400,mimetype="application/json")
            _id = id
            json_request["id"] = id

        else:
            if not "id" in json_request:
                return Response(response=json.dumps({"message":"Not id in data"}),status=400,mimetype="application/json")
            _id = json_request["id"]
        
        _query:Ticket = self.session.query(self._model).filter_by(id = _id).first()

        if not _query:
            return self.__return_json__(
                response = self.__parse_object__(_query),
                version = version
            )
        
        try:
            _query.is_paid = json_request.get("is_paid",None)

            self.session.commit()

        except Exception as e:
            self.session.rollback()
            raise e
        
        return self.__return_json__(
            response = self.__parse_object__(_query),
            version = version
        )
