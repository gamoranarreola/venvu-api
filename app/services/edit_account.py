from flask import Response
import json

from app.data.database import db_session
from app.data.schemas import account_schema
from app.services.common import api_edit_account
from app.model.accounts import EditAccountResponse
from app.repositories import AccountRepository


@api_edit_account("Edit Account API")
def edit_account(account_id: int) -> Response:

    account = AccountRepository(db_session).find_by_id(account_id)
    print(f"account: {account}")

    return EditAccountResponse(
        account=json.loads(account_schema.dumps(account))
    )
