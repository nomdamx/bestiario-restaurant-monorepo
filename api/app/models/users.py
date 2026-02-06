from app.models import (
    BaseUser,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models import (
        Session,
        Ticket
    )

from sqlalchemy.dialects.postgresql import ENUM
from app.schemas import AuthLevelEnum

auth_level_enum = ENUM(*[level.value for level in AuthLevelEnum], name="auth_level_type",create_type=True)

class User(BaseUser):
    auth_level:Mapped[AuthLevelEnum] = mapped_column(auth_level_enum,default=AuthLevelEnum.WORKER.value)
    display_name:Mapped[str] = mapped_column(default="")

    user_sessions:Mapped[list["Session"]] = relationship("Session",back_populates="user",cascade="all, delete-orphan")
    tickets:Mapped[list["Ticket"]] = relationship("Ticket",back_populates="user",cascade="all, delete-orphan")

    def get_json(self,include_relationships = None):
        return {
            "id":self.id,
            "username":self.username,
            "auth_level":self.auth_level,
            "display_name":self.display_name,
            "is_active":self.is_active,
            "created_at":self.created_at,
            "deleted_at":self.deleted_at
        }

    def get_simplified_json(self):
        return {
            "username":self.username,
            "display_name":self.display_name,
            "auth_level":self.auth_level
        }

    def check_auth_level(self,levels):
        if self.auth_level.lower() == AuthLevelEnum.ADMIN:
            return True
        
        auth_level = self.auth_level.lower()

        if isinstance(levels,list):
            levels_lower = [level.lower() if isinstance(level, str) else level for level in levels]
            return auth_level in levels_lower
        elif isinstance(levels,str):
            return auth_level == levels.lower()
        
        return False