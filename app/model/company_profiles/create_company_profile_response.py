from __future__ import annotations
from typing import Dict

from flask_restx import Model, Namespace
from marshmallow import fields

from app.model.fields import (
    request_status,
    company_profile,
)


class CreateCompanyProfileResponse:

    def __init__(
        self,
        *,
        company_profile: Dict
    ) -> None:
        self.company_profile = company_profile

    def encode(self):
        return {
            "status": "ok",
            "company_profile": self.company_profile
        }

    @staticmethod
    def model(ns: Namespace) -> Model:
        return ns.model(
            "CreateCompanyProfileResponse",
            {
                "status": fields.String(
                    metadata=request_status,
                    required=True,
                )
            },
            {
                "company_profile": fields.Dict(
                    metadata=company_profile,
                    required=True,
                )
            }
        )