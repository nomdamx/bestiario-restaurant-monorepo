from contextvars import ContextVar
from pydantic import BaseModel, Field, model_validator

_request_ctx:ContextVar["RequestContext"] = ContextVar("request_ctx", default=None)

from app import get_user_by_token
from app.schemas import UserSchemaContext

class RequestContext(BaseModel):
    user_token: str | None = Field(default=None)
    version_api: str | None = Field(default=None)
    user:UserSchemaContext | None = Field(default=None)

    @model_validator(mode="after")
    def set_user(self):
        if self.user is None and self.user_token:
            try:
                self.user = get_user_by_token(self.user_token)[0]
            except Exception as e:
                self.user = None
        return self

def set_context(ctx: RequestContext):
    _request_ctx.set(ctx)

def get_context() -> RequestContext | None:
    return _request_ctx.get()