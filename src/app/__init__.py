import os

from celery import Celery
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_restful import Api

from app.api.errors import errors
from app.db import db, init_marshmallow
from config import Config

if os.environ.get("CONFIG_SETUP") == "development":
    from config import DevelopmentConfig as UseConfig
elif os.environ.get("CONFIG_SETUP") == "testing":
    from config import TestingConfig as UseConfig

mail = Mail()
migrate = Migrate()

celery = Celery(
    __name__, broker=Config.CELERY_BROKER_URL, result_backend=Config.RESULT_BACKEND  # noqa: E501
)

from app.api.routes import create_routes  # noqa: E402


def create_app():
    flask_app = Flask(__name__)
    flask_app.config.from_object(UseConfig)
    celery.conf.update(flask_app.config)

    CORS(
        flask_app,
        resources={r"/api/*": {"origins": ["http://localhost:4200"]}},
    )

    init_extensions(flask_app)
    create_routes(api=Api(app=flask_app, errors=errors))
    _ = JWTManager(app=flask_app)

    return flask_app


def init_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    init_marshmallow(app)
