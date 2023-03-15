from flask import Flask
from flask_cors import CORS
from flask_restx import Api

from app.data import init_marshmallow
from app.data.cache import cache
from app.data.database import db_session
from app.routes.venvu_client import NSP
from app.utils.encoder import ModelEncoder


app = Flask(__name__)
app.config["RESTX_JSON"] = {"cls": ModelEncoder}
CORS(app)

cache.init_app(app)
init_marshmallow(app)

api = Api(
    app,
    title="Venvu API",
)

api.add_namespace(NSP, path="/api/v1")


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
