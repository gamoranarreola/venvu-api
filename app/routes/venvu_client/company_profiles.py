from flask_restx import Resource

from app.model import (
    BadRequestResponse,
    InternalServerErrorResponse,
)
from app.routes.venvu_client import NSP
from app.services.create_company_profile import create_company_profile
from app.model import (
    CreateCompanyProfileRequest,
    CreateCompanyProfileResponse,
)


@NSP.route("/company-profiles")
class CompanyProfiles(Resource):
    @NSP.response(200, "OK", CreateCompanyProfileResponse.model(NSP))
    @NSP.response(400, "Bad Request", BadRequestResponse.model(NSP))
    @NSP.response(500, "Internal Server Error", InternalServerErrorResponse.model(NSP))  # noqa: E501
    @NSP.expect(CreateCompanyProfileRequest.model(NSP))
    def post(self):
        return create_company_profile()
