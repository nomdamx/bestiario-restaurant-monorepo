from enum import Enum, StrEnum
from typing import TYPE_CHECKING
from uuid import UUID

import bcrypt
from sqlalchemy import Enum as SAEnum
from sqlalchemy import ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base_model import BaseCreatedModel, BaseModel

if TYPE_CHECKING:
    from src.models import Ticket

    from .session import Session


class AuthLevelUserEnum(StrEnum):
    ADMIN = "admin"
    MANAGER = "manager"
    WORKER = "worker"


class User(BaseCreatedModel):
    __tablename__ = "user"
    __table_args__ = (
        Index(
            "uq_user_username_active_only",
            "username",
            unique=True,
            postgresql_where=("is_active = true"),
        ),
    )

    username: Mapped[str] = mapped_column(String(20))
    display_name: Mapped[str] = mapped_column(default="")
    password: Mapped[str]
    auth_level: Mapped[AuthLevelUserEnum] = mapped_column(
        SAEnum(
            AuthLevelUserEnum,
            name="auth_level_type",
            values_callable=lambda x: [e.value for e in x], # type: ignore
        ),
        nullable=False,
        default=AuthLevelUserEnum.WORKER,
    )

    user_sessions: Mapped[list["Session"]] = relationship(
        "Session", back_populates="user", cascade="all, delete-orphan"
    )
    tickets: Mapped[list["Ticket"]] = relationship(
        "Ticket", back_populates="user", cascade="all, delete-orphan"
    )

    def check_auth(self, auth_roles: list[AuthLevelUserEnum]) -> bool:
        for role in auth_roles:
            if role not in AuthLevelUserEnum:
                raise ValueError("Invalid Role")
            if role is self.auth_level:
                return True

        return False

    def set_password(self, password: str) -> None:
        self.password = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

    def validate_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), self.password.encode("utf-8"))
