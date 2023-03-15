from flask_restx import Model, Namespace
from marshmallow import fields

from app.model.fields import error_message_404, request_status_error


class NotFoundResponse:
    def __init__(self, message) -> None:
        self.message = message

    def encode(self):
        return {
            "status": "error",
            "message": self.message
        }

    @staticmethod
    def model(ns: Namespace) -> Model:
        return ns.model(
            "NotFoundResponse",
            {
                "status": fields.String(
                    **request_status_error,
                    required=True,
                ),
                "message": fields.String(
                    **error_message_404,
                    require=True,
                )
            }
        )
