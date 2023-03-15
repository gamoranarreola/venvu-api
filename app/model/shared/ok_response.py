from flask_restx import Model, Namespace
from marshmallow import fields

from app.model.fields import request_status


class OKResponse:
    def encode(self):
        return {
            "status": "ok"
        }

    @staticmethod
    def model(ns: Namespace) -> Model:
        return ns.model(
            "OKResponse",
            {
                "status": fields.String(
                    **request_status,
                    required=True
                )
            }
        )
