from app.controllers.base_controller import BaseController

from app.models import (
    Order,
    OrderAddons,
)

from app.schemas import (
    OrderSchema,
)

from flask import Response,json,Request

class OrderController(BaseController):
    def __init__(self):
        super().__init__(
            model=Order,
            schema=OrderSchema
        )

    def controller_register_with_product_addons(self,request:Request):
        json_request = request.get_json()
        version = request.headers.get("Accept")
        json_request.pop("id",None)
        addons_ids = json_request.pop("order_addons",None)
            
        try:
            new_data:Order = self._model(**json_request)

            self.session.add(new_data)
            self.session.flush()

            for addon_id in addons_ids:
                addon_row = OrderAddons(
                    id_order = new_data.id,
                    id_product_addons = addon_id
                )
                new_data.order_addons.append(addon_row)

            self.session.commit()
            
        except Exception as e:
            self.session.rollback()
            raise e
        response = self.session.query(self._model).filter_by(id = new_data.id).first()
        return self.__return_json__(
            response = self.__parse_object__(response),
            version = version
        )

    def controller_update(self,id:int = None,request:Request = None):
        
        json_request = request.get_json()
        version = request.headers.get("Accept")
        json_request.pop("id",None)
        addons_ids = json_request.pop("order_addons",None)

        if id and isinstance(id,int):
            if "id" in json_request:
                return Response(response=json.dumps({"message":"id in data and url"}),status=400,mimetype="application/json")
            _id = id
            json_request["id"] = id

        else:
            if not "id" in json_request:
                return Response(response=json.dumps({"message":"Not id in data"}),status=400,mimetype="application/json")
            _id = json_request["id"]
        
        _query:Order = self.session.query(self._model).filter_by(id = _id).first()
        
        if not _query:
            return self.__return_json__(
                response = self.__parse_object__(_query),
                version = version
            )
        
        new_data = self._schema(**json_request).dict()

        try:
            for key,value in new_data.items():
                if hasattr(_query,key):
                    setattr(_query,key,value)
                    
            self.session.merge(_query)
            self.session.flush()

            for addon_id in addons_ids:
                addon_row = OrderAddons(
                    id_order = _id,
                    id_product_addons = addon_id
                )
                _query.order_addons.append(addon_row)


            self.session.commit()
            
        except Exception as e:
            self.session.rollback()
            raise e
        
        return self.__return_json__(
            response = self.__parse_object__(_query),
            version = version
        )

    def controller_delete(self,id):
        _query_order = self.session.query(Order).filter_by(id=id).first()
        
        try:
            _query_order.soft_delete()
            
        except Exception as e:
            self.session.rollback()
            raise e
        
        return Response(status=204)