from pydantic import BaseModel, Field, field_validator
from .enums import ProductAddonsEnum,ProductMenuSectionEnum

class CategorySchema(BaseModel):
    name:str
    ingredient_description:str
    menu_section:str = Field(default=ProductMenuSectionEnum.BAR.value)

class ProductAddonSchema(BaseModel):
    type:str = Field(default=ProductAddonsEnum.OUTSIDE.value)
    name:str
    price:float

    @field_validator("price",mode="before")
    @classmethod
    def validate_price(cls,price):
        if not price:
            raise ValueError("Price must have a value")
        
        if not isinstance(price,float):
            raise TypeError(f"Expected float, got {type(price).__name__}")
        
        if price < 0:
            raise ValueError("Price can't be negative")
        
        return price

class ProductSchema(BaseModel):
    id_category:int
    name:str
    complete_name:str | None = None
    ingredient_description:str
    price:float
    disponibility_status:bool = Field(default=True)
    id_source_addon:int | None = None

    @field_validator("complete_name", mode="before")
    def set_complete_name(cls, v, values):
        return v or values.get("name")

    @field_validator("price",mode="before")
    @classmethod
    def validate_price(cls,price):
        if not price:
            raise ValueError("Price must have a value")
        
        if not isinstance(price,float):
            raise TypeError(f"Expected float, got {type(price).__name__}")
        
        if price < 0:
            raise ValueError("Price can't be negative")
        
        return price