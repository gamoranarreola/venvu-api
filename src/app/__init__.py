import os

from flask import Flask, app
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from app.db import initialize_db
from app.api.routes import create_routes
from app.api.errors import errors


def create_app() -> app.Flask:
    # Create and configure app.
    flask_app = Flask(__name__)
    flask_app.config.from_object(os.environ['CONFIG_SETUP'])

    flask_app.config['MONGODB_SETTINGS'] = {
        'host': flask_app.config['MONGO_HOST'],
        'db': flask_app.config['MONGO_DB'],
        'username': flask_app.config['MONGO_USERNAME'],
        'password': flask_app.config['MONGO_PASSWORD'],
        'connect': False
    }

    CORS(flask_app, resources={
        r'/api/*': {
            'origins': [
                'http://localhost:4200'
            ]
        }
    })

    api = Api(app=flask_app, errors=errors)
    create_routes(api=api)

    # Initialize database.
    initialize_db(flask_app)

    # Initialize JWT Manager
    jwt = JWTManager(app=flask_app)

    return flask_app
