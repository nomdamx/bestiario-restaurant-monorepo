from app.controllers.base_controller import BaseController

from app.models import (
    Category,
    Product,
    ProductAddons
)

from app.schemas import (
    ProductAddonSchema
)

from flask import Response,json,Request


class ProductAddonsController(BaseController):
    def __init__(self):
        super().__init__(
            model=ProductAddons,
            schema=ProductAddonSchema
        )

    def controller_register(self,request:Request):
        
        json_request = request.get_json()
        version = request.headers.get("Accept")
        json_request.pop("id",None)
            
        try:
            addon_data = ProductAddons(**json_request)
            self.session.add(addon_data)
            self.session.flush()

            extra_category = self.get_or_create_extra_category()

            product_data = Product(
                name=addon_data.name,
                price=addon_data.price,
                id_category=extra_category.id,
                id_source_addon=addon_data.id
            )

            self.session.add(product_data)
            self.session.commit()
            
        except Exception as e:
            self.session.rollback()
            raise e
        
        response = self.session.query(ProductAddons).filter_by(id = addon_data.id).first()
        return self.__return_json__(
            response = self.__parse_object__(response),
            version = version
        )


    def controller_delete(self,id):
        addon_query = self.session.query(ProductAddons).filter_by(id=id).first()
        product_query = self.session.query(Product).filter_by(id_source_addon=addon_query.id).first()
        
        try:
            addon_query.soft_delete()
            product_query.soft_delete()
            
        except Exception as e:
            self.session.rollback()
            raise e
        
        return Response(status=204)
    
    def get_or_create_extra_category(self):
        category = self.session.query(Category).filter_by(name="Extras").first()
        if not category:
            category = Category(
                name="Extras",
                ingredient_description="Extras para agregar por separado:",
            )
            self.session.add(category)
            self.session.commit()
        return category

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
        
        _query:ProductAddons = self.session.query(self._model).filter_by(id = _id).first()

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
    
    def sync_existing_addons_as_products(self):
        try:
            extra_category = self.get_or_create_extra_category()

            addons = self.session.query(ProductAddons).all()

            for addon in addons:
                exists = self.session.query(Product).filter_by(id_source_addon=addon.id).first()
                
                if exists:
                    continue

                product = Product(
                    name=addon.name,
                    price=addon.price,
                    id_category=extra_category.id,
                    id_source_addon=addon.id
                )
                self.session.add(product)

            self.session.commit()
            
        except Exception as e:
            self.session.rollback()
            raise e
        
        return Response(status=200)
    
