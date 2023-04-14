from __future__ import annotations
from typing import Dict
from flask_restx import Model, Namespace
from marshmallow import fields

import app.model.validator as V
from app.model.fields import company_profile


class EditCompanyProfileRequest:

    def __init__(
        self,
        *,
        company_profile: Dict
    ) -> None:
        self.company_profile = company_profile

    @classmethod
    def from_dict(cls, data: Dict) -> EditCompanyProfileRequest:
        return cls(
            company_profile=data,
        )

    def __validate_company_profile(self):
        field = "company_profile"
        value = self.company_profile
        V.required(field, value)
        V.company_profile(field, value)

    def validate(self):
        self.__validate_company_profile()

    @staticmethod
    def model(ns: Namespace) -> Model:
        return ns.model(
            "EditCompanyProfileRequest",
            {
                "company_profile": fields.Dict(
                    metadata=company_profile,
                    required=True,
                )
            }
        )
