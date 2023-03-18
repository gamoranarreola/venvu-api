from flask_restx import Model, Namespace
from marshmallow import fields

from app.model.fields import (
    request_status_error,
    error_message_duplicate_admin
)


class DuplicateAdminErrorResponse:
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
            "DuplicateAdminErrorResponse",
            {
                "status": fields.String(
                    **request_status_error,
                    required=True,
                ),
                "message": fields.String(
                    **error_message_duplicate_admin,
                    required=True
                )
            }
        )
