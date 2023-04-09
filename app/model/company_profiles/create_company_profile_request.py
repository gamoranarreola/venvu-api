from __future__ import annotations
from typing import Dict, List
from flask_restx import Model, Namespace
from marshmallow import fields

import app.model.validator as V
from app.model.fields import (
    email,
    roles,
    company_profile,
)


class CreateCompanyProfileRequest:

    def __init__(
        self,
        *,
        email: str,
        roles: List[str],
        company_profile: Dict
    ) -> None:
        self.email = email
        self.roles = roles
        self.company_profile = company_profile

    @classmethod
    def from_dict(cls, data: Dict) -> CreateCompanyProfileRequest:
        return cls(
            email=data.get("email"),
            roles=data.get("roles"),
            company_profile=data.get("company_profile")
        )

    def __validate_email(self):
        field = "email"
        value = self.email
        V.required(field, value)
        V.string(field, value)
        V.email(field, value)

    def __validate_roles(self):
        field = "roles"
        value = self.roles
        V.required(field, value)
        V.list_of_role_names(field, value)

    def __validate_company_profile(self):
        field = "company_profile"
        value = self.company_profile
        V.required(field, value)
        V.company_profile(field, value)

    def validate(self):
        self.__validate_email()
        self.__validate_roles()
        self.__validate_company_profile()

    @staticmethod
    def model(ns: Namespace) -> Model:
        return ns.model(
            "CreateCompanyProfileRequest",
            {
                "email": fields.String(
                    metadata=email,
                    required=True
                ),
                "roles": fields.List(
                    cls_or_instance=fields.String,
                    metadata=roles,
                    required=True
                ),
                "company_profile": fields.Dict(
                    metadata=company_profile,
                    required=True
                )
            }
        )
