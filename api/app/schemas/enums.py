from enum import Enum

    
class AuthLevelEnum(Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    WORKER = "worker"

class ProductAddonsEnum(Enum):
    OUTSIDE = "outside"

class ProductMenuSectionEnum(Enum):
    DRINKS = "drinks"
    BAR = "bar"
    GRILLED = "grilled"