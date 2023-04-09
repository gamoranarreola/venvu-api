from __future__ import annotations
from typing import Dict
from flask_restx import Model, Namespace
from marshmallow import fields

import app.model.validator as V
from app.model.fields import email, sub


class SignInRequest:

    def __init__(
        self,
        *,
        email: str,
        sub: str,
    ) -> None:
        self.email = email
        self.sub = sub

    @classmethod
    def from_dict(cls, data: Dict) -> SignInRequest:
        return cls(
            email=data.get("email"),
            sub=data.get("sub"),
        )

    def __validate_email(self):
        field = "email"
        value = self.email
        V.required(field, value)
        V.string(field, value)
        V.email(field, value)

    def __validate_sub(self):
        field = "sub"
        value = self.sub
        V.required(field, value)
        V.string(field, value)
        V.sub(field, value)

    def validate(self):
        self.__validate_email()
        self.__validate_sub()

    @staticmethod
    def model(ns: Namespace) -> Model:
        return ns.model(
            "SignInRequest",
            {
                "email": fields.String(
                    metadata=email,
                    required=True
                ),
                "sub": fields.String(
                    metadata=sub,
                    required=True
                )
            }
        )
