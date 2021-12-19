import os

from flask import Flask, app
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.api.routes import create_routes
from app.api.errors import errors
from app.db import db


migrate = Migrate()

def create_app() -> app.Flask:
    flask_app = Flask(__name__)
    flask_app.config.from_object(os.environ['CONFIG_SETUP'])

    CORS(flask_app, resources={
        r'/api/*': {
            'origins': [
                'http://localhost:4200'
            ]
        }
    })

    db.init_app(flask_app)
    migrate.init_app(flask_app, db)
    api = Api(app=flask_app, errors=errors)
    create_routes(api=api)
    jwt = JWTManager(app=flask_app)

    return flask_app
