import flask_marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


db = SQLAlchemy()
ma = Marshmallow()

def init_marshmallow(app):
    ma.init_app(app)
