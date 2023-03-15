from flask_restx import Resource
from flask import request

from app.model import (
    SignInResponse,
    BadRequestResponse,
    NotFoundResponse,
    InternalServerErrorResponse,
)
from app.services.sign_in import sign_in
from app.routes.venvu_client import NSP


@NSP.route("/sign-in")
class SignIn(Resource):
    @NSP.response(200, "OK", SignInResponse.model(NSP))
    @NSP.response(400, "Bad Request", BadRequestResponse.model(NSP))
    @NSP.response(404, "Not Found", NotFoundResponse.model(NSP))
    @NSP.response(500, "Internal Server Error", InternalServerErrorResponse.model(NSP))  # noqa: E501
    def post(self):
        args = request.get_json()
        return sign_in(args.get("email"), args.get("sub"))
