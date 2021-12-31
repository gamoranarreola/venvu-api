from flask import Flask, app
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate

from app.api.routes import create_routes
from app.api.errors import errors
from app.db import db, init_marshmallow


migrate = Migrate()

def create_app(config_filename=None) -> app.Flask:
    flask_app = Flask(__name__, instance_relative_config=True)
    flask_app.config.from_pyfile(config_filename)

    CORS(flask_app, resources={
        r'/api/*': {
            'origins': [
                'http://localhost:4200'
            ]
        }
    })

    db.init_app(flask_app)
    init_marshmallow(flask_app)
    migrate.init_app(flask_app, db)
    api = Api(app=flask_app, errors=errors)
    create_routes(api=api)
    jwt = JWTManager(app=flask_app)

    return flask_app
