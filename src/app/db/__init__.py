from flask_mongoengine import MongoEngine
from mongoengine.connection import connect


db = MongoEngine()

def initialize_db(app):
    db.init_app(app)
