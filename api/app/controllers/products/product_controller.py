from app.controllers.base_controller import BaseController

from app.models import (
    Product,
)

from app.schemas import (
    ProductSchema,
)

from flask import Response,json,Request

class ProductController(BaseController):
    def __init__(self):
        super().__init__(
            model=Product,
            schema=ProductSchema
        )

    def controller_update_price(self, request:Request):
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
        
        _query:Product = self.session.query(self._model).filter_by(id = _id).first()

        if not _query:
            return self.__return_json__(
                response = self.__parse_object__(_query),
                version = version
            )
        
        try:
            _query.price = json_request.get("price",None)

            self.session.commit()

        except Exception as e:
            self.session.rollback()
            raise e
        
        return self.__return_json__(
            response = self.__parse_object__(_query),
            version = version
        )