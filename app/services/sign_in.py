from flask import Response
import json

from app.model.sign_in import SignInResponse
from app.data.database import Account, db_session
from app.data.schemas import account_schema
from app.repositories import AccountRepository
# from app.tasks import delete_user_from_auth0
from app.services.common import (
    api_sign_in
)


@api_sign_in(
    "Sign Up API"
)
def sign_in(email: str, sub: str) -> Response:
    # First check if there is an account under the provided email address.
    account = AccountRepository(db_session).find_by_email(email)

    if account is None:

        # Check if there is already an admin account under the provided email
        # domain.
        account = AccountRepository(db_session).find_by_account_admin(email)

        if account is None:

            account = Account(
                email=email,
                sub=sub
            )

            AccountRepository(db_session).save(account)
        else:
            pass
            # _ = delete_user_from_auth0.apply_async(args=[email])

    return SignInResponse(
        account=json.loads(account_schema.dumps(account))
    ), 200
