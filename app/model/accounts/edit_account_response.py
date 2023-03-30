from __future__ import annotations
from typing import Dict

from flask_restx import Model, Namespace
from marshmallow import fields

from app.model.fields import request_status, account


class EditAccountResponse:

    def __init__(
        self,
        *,
        account: Dict,
    ) -> None:
        self.account = account

    def encode(self):
        return {
            "status": "ok",
            "account": self.account
        }

    def model(ns: Namespace) -> Model:
        return ns.model(
            "EditAccountResponse",
            {
                "status": fields.String(
                    metadata=request_status,
                    required=True,
                )
            },
            {
                "account": fields.Dict(
                    metadata=account,
                    required=True,
                )
            }
        )
