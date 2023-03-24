from flask_restx import Model, Namespace
from marshmallow import fields

from app.model.fields import error_message_400, request_status_error


class BadRequestResponse:
    def __init__(self, message: str) -> None:
        self.message = message

    def encode(self):
        return {
            "status": "error",
            "message": self.message
        }

    @staticmethod
    def model(ns: Namespace) -> Model:
        return ns.model(
            "BadRequestResponse",
            {
                "status": fields.String(
                    metadata=request_status_error,
                    required=True,
                ),
                "message": fields.String(
                    metadata=error_message_400,
                    required=True,
                )
            }
        )
