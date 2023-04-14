from flask_restx import Resource

from app.model import (
    BadRequestResponse,
    InternalServerErrorResponse,
    NotFoundResponse,
)
from app.routes.venvu_client import NSP
from app.services.create_company_profile import create_company_profile
from app.services.edit_company_profile import edit_company_profile
from app.model import (
    CreateCompanyProfileRequest,
    CreateCompanyProfileResponse,
    EditCompanyProfileRequest,
    EditCompanyProfileResponse,
)


@NSP.route("/company-profiles")
@NSP.route("/company-profiles/<company_profile_id>")
class CompanyProfiles(Resource):
    @NSP.response(200, "OK", CreateCompanyProfileResponse.model(NSP))
    @NSP.response(400, "Bad Request", BadRequestResponse.model(NSP))
    @NSP.response(404, "Not Found", NotFoundResponse.model(NSP))
    @NSP.response(500, "Internal Server Error", InternalServerErrorResponse.model(NSP))  # noqa: E501
    @NSP.expect(CreateCompanyProfileRequest.model(NSP))
    def post(self):
        return create_company_profile()

    @NSP.response(200, "OK", EditCompanyProfileResponse.model(NSP))
    @NSP.response(400, "Bad Request", BadRequestResponse.model(NSP))
    @NSP.response(404, "Not Found", NotFoundResponse.model(NSP))
    @NSP.response(500, "Internal Server Error", InternalServerErrorResponse.model(NSP))  # noqa: E501
    @NSP.expect(EditCompanyProfileRequest.model(NSP))
    def put(self, company_profile_id):
        return edit_company_profile(company_profile_id)
