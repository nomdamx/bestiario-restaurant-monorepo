from pydantic import BaseModel, Field, field_validator

class RestaurantTableSchema(BaseModel):
    number:int

class TicketSchema(BaseModel):
    id_restaurant_table:int
    is_paid:bool = False
    comments:str = ""
    client_name:str = None
    id_user:int
    
class OrderAddonsSchema(BaseModel):
    id_product_addons:int
    id_order:int

class OrderSchema(BaseModel):
    id_ticket:int
    id_product:int
    quantity:int
    finished_status:bool = Field(default=False)
    order_addons:list[int] = Field(default_factory=list)    

    @field_validator("quantity",mode="before")
    @classmethod
    def validate_quantity(cls,quantity):
        if not quantity:
            raise ValueError("Quantity must have a value")
        
        if not isinstance(quantity,int):
            raise TypeError(f"Expected int, got {type(quantity).__name__}")
        
        if quantity < 0:
            raise ValueError("Quantity can't be negative")
        
        return quantity
    
class PrintListTicketSchema(BaseModel):
    id_ticket:int
    printed:bool = False