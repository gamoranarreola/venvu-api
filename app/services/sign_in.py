from flask import Response, request
import json

from app.model.sign_in import SignInResponse, SignInRequest
from app.data.database import Account, db_session
from app.data.schemas import account_schema
from app.repositories import AccountRepository
from app.services.common import error_409_response, error_400_response
# from app.tasks import delete_user_from_auth0


def sign_in() -> Response:

    try:
        body = request.get_json()
        req = SignInRequest.from_dict(body)
        req.validate()
    except ValueError as exc:
        return error_400_response(str(exc), exc)

    # First check if there is an account under the provided email address.
    account = AccountRepository(db_session).find_by_email(req.email)

    if account is None:

        # Check if there is already an admin account under the provided email
        # domain.
        account = AccountRepository(db_session).find_by_account_admin(req.email)  # noqa: E501

        if account is None:

            account = Account(
                email=req.email,
                sub=req.sub,
            )

            AccountRepository(db_session).save(account)

        else:
            # _ = delete_user_from_auth0.apply_async(args=[email])
            return error_409_response(
                f"An admin already exists for {req.email}"
            )

    return SignInResponse(
        account=json.loads(account_schema.dumps(account))
    ), 200
