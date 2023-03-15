from flask import Response
import json

from app.model.sign_in import SignInResponse
from app.data.database import Account, db_session
from app.data.schemas import account_schema
from app.repositories import AccountRepository
from app.services.common import (
    api_sign_in
)


@api_sign_in(
    "Sign Up API"
)
def sign_in(email: str, sub: str) -> Response:
    account = AccountRepository(db_session).find_by_email(email)

    if account is None:
        admin_account = AccountRepository(db_session).find_by_account_admin(email)  # noqa: E501

        if admin_account is None:

            account = AccountRepository(db_session).save(Account(
                email=email,
                sub=sub
            ))

    return SignInResponse(status="ok", account=json.loads(account_schema.dumps(account))), 200  # noqa: E501
