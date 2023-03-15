from flask_marshmallow import Marshmallow

ma = Marshmallow()


def init_marshmallow(app):
    ma.init_app(app)
