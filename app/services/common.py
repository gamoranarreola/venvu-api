import functools
import re

from flask import Response, request

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


def error_409_response(
    message: str = "Duplicate Admin",
    exc: Exception = None
) -> Response:
    response = DuplicateAdminErrorResponse(message)

    if exc is not None:
        logger.exception(exc)
    else:
        logger.debug(response)

    return response, 409


def error_500_response(exc: Exception) -> Response:
    response = InternalServerErrorResponse(message=str(exc))
    logger.exception(exc)

    return response, 500


def api_edit_account(api_name: str):
    def wrapper(func):

        @functools.wraps(func)
        def wrapped(account_id: int):

            logger.info(api_name)

            try:
                try:
                    pass
                except ValueError:
                    pass

                res = func(account_id)
                return res
            except Exception as exc:
                return error_500_response(exc)

        return wrapped
    return wrapper
