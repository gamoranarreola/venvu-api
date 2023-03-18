import functools
import re

from flask import Response

from app.model import (
    BadRequestResponse,
    OKResponse,
    InternalServerErrorResponse,
    DuplicateAdminErrorResponse,
)
from app.data.logger import logger


def success_response() -> Response:
    response = OKResponse()
    return response, 200


def error_400_response(
    message: str = "Bad Request",
    exc: Exception = None
) -> Response:
    response = BadRequestResponse(message)
    if exc is not None:
        logger.exception(exc)
    else:
        logger.debug(response)
    return response, 400


def error_500_response(exc: Exception) -> Response:
    response = InternalServerErrorResponse(message=str(exc))
    logger.exception(exc)
    return response, 500


def error_duplicate_admin_response(exc: Exception) -> Response:
    response = DuplicateAdminErrorResponse(message=str(exc))
    logger.exception(exc)
    return response, 500


def validate_email(email: str) -> None:
    if not re.match("^([a-zA-Z0-9_\\-\\.]+)@([a-zA-Z0-9_\\-\\.]+)\\.([a-zA-Z]{2,5})$", email):  # noqa: E501
        raise ValueError("Invalid email")


def invalid_email(email: str) -> None:
    message = f"Invalid email: {email}"
    return error_400_response(message)


def validate_sub(sub: str) -> None:
    if not re.match("^auth0\\|([a-zA-Z0-9]{24})$", sub):
        raise ValueError("Invalid sub")


def invalid_sub(sub: str) -> None:
    message = f"Invalid sub: {sub}"
    return error_400_response(message)


def api_sign_in(
    api_name: str,
):
    def wrapper(func):
        @functools.wraps(func)
        def wrapped(email: str, sub: str):
            logger.info(api_name)
            try:
                try:
                    validate_email(email)
                except ValueError:
                    return invalid_email(email)

                try:
                    validate_sub(sub)
                except ValueError:
                    return invalid_sub(sub)

                res = func(email, sub)
                return res
            except Exception as exc:
                return error_500_response(exc)
        return wrapped
    return wrapper
