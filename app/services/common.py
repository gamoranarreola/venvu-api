import functools

from flask import Response

from app.repositories.account_repository import AccountRepository
from app.data.database import db_session
from app.model import (
    BadRequestResponse,
    OKResponse,
    InternalServerErrorResponse,
    DuplicateAdminErrorResponse,
    NotFoundResponse,
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


def error_404_response(message: str = "Not Found") -> Response:
    response = NotFoundResponse(message)
    logger.debug(response)
    return response, 404


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


def account_not_found(account_id: int) -> Response:
    message = f"Account not found: {account_id}"
    return error_404_response(message)


def api_edit_account(api_name: str):
    def wrapper(func):

        @functools.wraps(func)
        def wrapped(account_id: int):

            logger.info(api_name)

            try:
                account = AccountRepository(db_session).find_by_id(account_id)

                if account is None:
                    return account_not_found(account_id)

                res = func(account)
                return res
            except Exception as exc:
                return error_500_response(exc)

        return wrapped
    return wrapper
