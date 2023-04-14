from flask_restx import Resource

from app.model import (
    BadRequestResponse,
    InternalServerErrorResponse,
    NotFoundResponse,
    EditAccountResponse,
    EditAccountRequest,
)
from app.routes.venvu_client import NSP
from app.services.edit_account import edit_account


@NSP.route("/accounts/<account_id>")
class Accounts(Resource):
    @NSP.response(200, "OK", EditAccountResponse.model(NSP))
    @NSP.response(400, "Bad Request", BadRequestResponse.model(NSP))
    @NSP.response(404, "Not Found", NotFoundResponse.model(NSP))
    @NSP.response(500, "Internal Server Error", InternalServerErrorResponse.model(NSP))  # noqa: E501
    @NSP.expect(EditAccountRequest.model(NSP))
    def put(self, account_id):
        return edit_account(account_id)
