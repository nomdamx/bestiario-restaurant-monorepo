from contextvars import ContextVar
from typing import Annotated

from fastapi import Depends
from pydantic import BaseModel, Field

_request_ctx: ContextVar["RequestContext"] = ContextVar("request_ctx", default=None)  # type: ignore


class RequestContext(BaseModel):
    user_token: str | None = Field(default=None)
    username: str | None = Field(default=None)
    version_app: str | None = Field(default=None)


def set_context(ctx: RequestContext):
    _request_ctx.set(ctx)


def get_context() -> RequestContext | None:
    return _request_ctx.get()


request_context_dependency = Annotated[RequestContext, Depends(get_context)]
