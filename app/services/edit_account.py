import json
from flask import Response, request

from app.data.database import Account
from app.repositories.account_repository import AccountRepository
from app.data.database import db_session
from app.services.common import api_edit_account
from app.model.accounts import EditAccountResponse, EditAccountRequest
from app.services.common import error_400_response
from app.data.schemas import account_schema


@api_edit_account("Edit Account API")
def edit_account(account: Account) -> Response:

    try:
        body = request.get_json()
        req = EditAccountRequest.from_dict(body)
        req.validate()
    except ValueError as exc:
        return error_400_response(str(exc), exc)

    account = AccountRepository(db_session).update(account, body)
    AccountRepository(db_session).save(account)

    return EditAccountResponse(
        account=json.loads(account_schema.dumps(account))
    )
