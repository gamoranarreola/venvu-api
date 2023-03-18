from __future__ import annotations
from typing import Dict

from flask_restx import Model, Namespace
from marshmallow import fields

from app.model.fields import request_status, account


class SignInResponse:
    def __init__(
        self,
        *,
        account: Dict,
    ) -> None:
        self.account = account

    def encode(self):
        return {
            "status": "ok",
            "account": self.account,
        }

    @staticmethod
    def model(ns: Namespace) -> Model:
        return ns.model(
            "SignInResponse",
            {
                "status": fields.String(
                    **request_status,
                    required=True,
                )
            },
            {
                "account": fields.Dict(
                    **account,
                    required=True,
                )
            }
        )
