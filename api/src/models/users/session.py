from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base_model import BaseModel

if TYPE_CHECKING:
    from .user import User


class Session(BaseModel):
    __tablename__ = "session"

    session: Mapped[str] = mapped_column(unique=True)
    expires_at: Mapped[int]

    id_user: Mapped[UUID] = mapped_column(ForeignKey("user.id"), index=True)
    user: Mapped["User"] = relationship("User", back_populates="user_sessions")
