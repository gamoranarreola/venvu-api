from typing import Any
import re

from app.data.database import Role
from app.data.schemas import company_profile_schema, account_schema


def required(field: str, value: Any):
    message = f"{field} field is required"
    if value is None:
        raise ValueError(message)


def string(field: str, value: Any):
    message = f"{field} should be a string"
    if type(value) != str:
        raise ValueError(message)


def email(field: str, value: Any):
    message = f"{field} should be a valid email address"

    if not re.match("^([a-zA-Z0-9_\\-\\.]+)@([a-zA-Z0-9_\\-\\.]+)\\.([a-zA-Z]{2,5})$", value):  # noqa: E501
        raise ValueError(message)


def sub(field: str, value: Any):
    message = f"{field} should be a valid Auth0 sub"

    if not re.match("^auth0\\|([a-zA-Z0-9]{24})$", value):
        raise ValueError(message)


def list_of_role_names(field: str, value: Any):
    message = f"{field} should be a list of role names"

    if type(value) is not list:
        raise ValueError(message)

    roles = [member.name for member in Role]

    for s in value:
        if s not in roles:
            raise ValueError(message)


def account(field: str, value: Any):
    message = f"{field} should be a Venvu account"
    validation_result = account_schema.validate(value)

    if len(validation_result) > 0:
        raise ValueError(f"{message} {validation_result}")


def company_profile(field: str, value: Any):
    message = f"{field} should be a Venvu company profile"
    validation_result = company_profile_schema.validate(value)

    if len(validation_result) > 0:
        raise ValueError(f"{message}: {validation_result}")
