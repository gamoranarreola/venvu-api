from __future__ import annotations
from typing import Dict
from flask_restx import Model, Namespace
from marshmallow import fields

import app.model.validator as V
from app.model.fields import account


class EditAccountRequest:

    def __init__(
        self,
        *,
        account: Dict,
    ) -> None:
        self.account = account

    @classmethod
    def from_dict(cls, data: Dict) -> EditAccountRequest:
        return cls(
            account=data,
        )

    def __validate_account(self):
        field = "account"
        value = self.account
        V.required(field, value)
        V.account(self, value)

    def validate(self):
        self.__validate_account()

    @staticmethod
    def model(ns: Namespace) -> Model:
        return ns.model(
            "EditAccountRequest",
            {
                "account": fields.Dict(
                    metadata=account,
                    required=True
                )
            }
        )
