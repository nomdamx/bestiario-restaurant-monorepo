from pydantic import BaseModel, Field, field_validator
import time
from app.schema.print_base_model import PrintBaseModel

class RestaurantTableSchema(PrintBaseModel):
    number:int

class Category(PrintBaseModel):
    name:str
    ingredient_description:str
    menu_section:str

class Product(PrintBaseModel):
    name:str
    price:float
    category:Category

class ProductAddons(PrintBaseModel):
    type:str
    name:str
    price:float

class OrderAddons(PrintBaseModel):
    id_product_addons:int
    id_order:int
    product_addons:ProductAddons

class Order(PrintBaseModel):
    id_ticket:int
    id_product:int
    quantity:int
    finished_status:bool
    printed:bool

    total:float
    product:Product
    order_addons:list[OrderAddons]

class User(PrintBaseModel):
    id:int
    username:str

class TicketSchema(PrintBaseModel):
    uuid:str
    ticket_number:int
    id_restaurant_table:int
    restaurant_table:RestaurantTableSchema
    is_paid:bool
    comments:str
    client_name:str | None
    total:float
    id_user:int
    print_for_pay:bool

    user:User
    orders:list[Order]