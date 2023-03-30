from typing import Any
import re


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
