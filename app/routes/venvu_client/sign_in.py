from flask_restx import Resource

from app.model import (
    SignInResponse,
    BadRequestResponse,
    DuplicateAdminErrorResponse,
    InternalServerErrorResponse,
)
from app.services.sign_in import sign_in
from app.routes.venvu_client import NSP


@NSP.route("/sign-in")
class SignIn(Resource):
    @NSP.response(200, "OK", SignInResponse.model(NSP))
    @NSP.response(400, "Bad Request", BadRequestResponse.model(NSP))
    @NSP.response(409, "Duplicate Admin", DuplicateAdminErrorResponse.model(NSP))  # noqa: E501
    @NSP.response(500, "Internal Server Error", InternalServerErrorResponse.model(NSP))  # noqa: E501
    def post(self):
        return sign_in()
