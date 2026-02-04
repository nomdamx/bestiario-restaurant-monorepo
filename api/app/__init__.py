from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import os
from flask_socketio import SocketIO
from dotenv import load_dotenv
from .error_handler import register_error_handlers

from hashlib import sha256

from flask_migrate import Migrate

if os.environ.get("DB_URL") is None:
    load_dotenv()

db = SQLAlchemy()
migrate = Migrate()

bcrypt = Bcrypt()
cors = CORS()
socketio = SocketIO(
    cors_allowed_origins="*",
    async_mode="eventlet",
    logger=True,
    engineio_logger=True
)

basedir = os.path.abspath(os.path.dirname(__file__))
upload_folder = os.path.abspath(os.path.join(basedir, 'static', 'uploads'))
    
app:Flask = Flask(__name__)

# app
def create_app():
    from .infra import ctx_middleware, setup_request_logger, log_request_end, log_request_start, setup_error_logger, setupt_socket_loggin
    
    register_error_handlers(app)
    setup_request_logger()
    setup_error_logger()
    setupt_socket_loggin()

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = upload_folder
    app.before_request(ctx_middleware)
    app.before_request(log_request_start)
    app.after_request(log_request_end)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True,automatic_options=True)
    socketio.init_app(app, cors_allowed_origins="*",async_mode="eventlet")
    
    from app.models import (
        BaseModel,
    )
    
    with app.app_context():
        db.create_all()

    define_routes(app)
    
    return app

def define_routes(app:Flask):
    # -------------------------------- Routes --------------------------------
    
    from app.routes import (
        AuthUserRoute,
    )
    
    #user & auth
    app.register_blueprint(AuthUserRoute().get_blueprint(),url_prefix="/api/auth/user")

    from app.routes import (
        CategoryRoute,
        ProductRoute,
        ProductAddonsRoute,
        RestaurantTableRoute,
        TicketRoute,
        OrderRoute,
        OrderAddonsRoute,
        PrintListTicketRoute
    )

    # routes
    app.register_blueprint(CategoryRoute().get_blueprint(),url_prefix="/api/category")
    app.register_blueprint(ProductRoute().get_blueprint(),url_prefix="/api/product")
    app.register_blueprint(ProductAddonsRoute().get_blueprint(),url_prefix="/api/product-addons")

    app.register_blueprint(RestaurantTableRoute().get_blueprint(),url_prefix="/api/restaurant-table")

    app.register_blueprint(TicketRoute().get_blueprint(),url_prefix="/api/ticket")
    app.register_blueprint(PrintListTicketRoute().get_blueprint(),url_prefix="/api/print-ticket")
    app.register_blueprint(OrderRoute().get_blueprint(),url_prefix="/api/order")
    app.register_blueprint(OrderAddonsRoute().get_blueprint(),url_prefix="/api/order-addons")


from app.models import User, Session

def get_user_by_token(token:str) -> tuple[User, Session]:
    session = db.session
    userSessionId = sha256(token.encode('utf-8'),usedforsecurity=True).hexdigest()
    user_session = session.query(Session).filter_by(session = userSessionId).first()
    user = session.query(User).filter_by(id=user_session.id_user).first()
    return (user, user_session)