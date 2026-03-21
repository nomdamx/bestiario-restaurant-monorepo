from contextlib import asynccontextmanager

import socketio
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

import src.models
from src.config import get_config
from src.core.custom_errors import AppError
from src.core.error_handler import app_error_handler, request_validation_handler
from src.db.session import BASE, engine
from src.infra.loggin import (
    setup_error_logger,
    setup_request_logger,
    setup_socket_logger,
)
from src.infra.middleware import RequestContextMiddleware, RequestLoggingMiddleware
from src.sockets import sio, ticket_watcher

BASE.metadata.create_all(bind=engine)
config = get_config()
setup_request_logger()
setup_socket_logger()
setup_error_logger()


def register_routes(app: FastAPI):
    from src.features.auth.route import router as auth_router
    from src.features.category import router_categories
    from src.features.order import router_order
    from src.features.order_addons import router_order_addon
    from src.features.product import router_products
    from src.features.product_addons import router_product_addons
    from src.features.restaurant_tables import router_restaurant_table
    from src.features.ticket import router_ticket

    # AUTH
    app.include_router(auth_router, prefix="/api")

    # FEATURES
    app.include_router(router_categories, prefix="/api")
    app.include_router(router_products, prefix="/api")
    app.include_router(router_product_addons, prefix="/api")
    app.include_router(router_restaurant_table, prefix="/api")
    app.include_router(router_ticket, prefix="/api")
    app.include_router(router_order_addon, prefix="/api")
    app.include_router(router_order, prefix="/api")


@asynccontextmanager
async def lifespan(app: FastAPI):
    sio.start_background_task(ticket_watcher)
    yield


def create_app() -> FastAPI:
    app = FastAPI(title=config.APP_NAME, debug=config.DEBUG, lifespan=lifespan)

    return app


app = create_app()
register_routes(app)
app.add_exception_handler(AppError, app_error_handler)
app.add_exception_handler(RequestValidationError, request_validation_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(RequestContextMiddleware)


@app.get("/")
def index():
    return {"Index"}


socket_app = socketio.ASGIApp(sio, other_asgi_app=app)
