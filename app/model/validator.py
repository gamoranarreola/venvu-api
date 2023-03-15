from typing import Any


def required(field: str, value: Any):
    message = f"{field} field is required"
    if value is None:
        raise ValueError(message)


def string(field: str, value: Any):
    message = f"{field} should be a string"
    if type(value) != str:
        raise ValueError(message)
