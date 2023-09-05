from flask_restx import Resource
from flask import request

from app.model import (
    BadRequestResponse,
    InternalServerErrorResponse,
    NotFoundResponse,
)
from app.routes.venvu_client import NSP
from app.services.create_company_profile import create_company_profile
from app.services.edit_company_profile import edit_company_profile
from app.services.company_profile_list_attributes import (
    get_employee_count_ranges,
    get_employee_count_range_by_name,
    get_yearly_revenue_ranges,
    get_yearly_revenue_range_by_name,
    get_countries,
    get_provinces,
)
from app.model import (
    CreateCompanyProfileRequest,
    CreateCompanyProfileResponse,
    EditCompanyProfileRequest,
    EditCompanyProfileResponse,
    CodeAndNameListResponse,
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


@NSP.route("/company-profiles/employee-count-ranges")
class EmployeeCountRanges(Resource):
    @NSP.response(200, "OK", CodeAndNameListResponse.model(NSP))
    @NSP.response(400, "Bad Request", BadRequestResponse.model(NSP))
    @NSP.response(500, "Internal Server Error", InternalServerErrorResponse.model(NSP))  # noqa: E501
    def get(self):
        return get_employee_count_ranges()


@NSP.route("/company-profiles/employee-count-ranges/<name>")
class EmployeeCountRange(Resource):
    def get(self, name):
        return get_employee_count_range_by_name(name)


@NSP.route("/company-profiles/yearly-revenue-ranges")
class YearlyRevenueRanges(Resource):
    def get(self):
        return get_yearly_revenue_ranges()


@NSP.route("/company-profiles/yearly-revenue-ranges/<name>")
class YearlyRevenueRange(Resource):
    def get(self, name):
        return get_yearly_revenue_range_by_name(name)


@NSP.route("/company-profiles/countries")
class Countries(Resource):
    def get(self):
        return get_countries()


@NSP.route("/company-profiles/provinces")
class Provinces(Resource):
    def get(self):
        return get_provinces(request.args['country_code'])
