from operator import itemgetter, or_

import pycountry
from flask import jsonify, request
from flask.wrappers import Response
from flask_restful import Resource
from sqlalchemy.sql.expression import and_, or_

from app.api.auth0 import requires_auth
from app.api.errors import (Auth0RequestError, BadRequestError,
                            InternalServerError)
from app.db.models import (Account, CompanyProfile, CompanyType,
                           EmployeeCountRange, Industry, Role,
                           YearlyRevenueRange)
from app.db.schemas import (account_schema, company_profile_schema,
                            industries_schema, industry_schema)
from app.tasks import assign_user_roles


class CompanyProfileListApi(Resource):
    @requires_auth
    def post(self) -> Response:

        response_obj = {"data": None, "error": None, "success": False}
        status_code = None

        try:

            """
            Query for an account with the
            provided email address.
            """
            req_data = request.get_json()
            account = Account.query.filter_by(email=req_data.get("email")).first()  # noqa: E501

            """
            Account not found.
            """
            if account is None:

                response_obj[
                    "error"
                ] = "An account with the email address {} does not exist.".format(req_data.get("email"))  # noqa: E501
                status_code = 404

            else:

                """
                Query for a company profile with the provided name.
                """
                company_profile = CompanyProfile.query.filter(
                    or_(
                        CompanyProfile.name == req_data.get("company_profile")["name"],  # noqa: E501
                        CompanyProfile.website
                        == req_data.get("company_profile")["website"],
                        and_(
                            CompanyProfile.state_tax_id
                            == req_data.get("company_profile")["state_tax_id"],
                            CompanyProfile.tax_id_state
                            == req_data.get("company_profile")["tax_id_state"],
                        ),
                    )
                ).first()

                """
                If no such company profile
                is found, create it.
                """
                if company_profile is None:

                    company_profile = CompanyProfile(**req_data.get("company_profile"))  # noqa: E501
                    company_profile.accounts.append(account)
                    company_profile.save()

                    account_data = {**req_data.get("account")}

                    for idx, role_name in enumerate(account_data["roles"]):
                        account_data["roles"][idx] = Role(role_name).name

                    _ = assign_user_roles.apply_async(
                        args=[account.sub, req_data.get("selectedRoleIds")]
                    )

                    try:
                        _.wait()
                    except Auth0RequestError:
                        raise Auth0RequestError

                    account.update(account_schema.load(data=account_data, partial=True))  # noqa: E501

                    response_obj["data"] = company_profile_schema.dump(company_profile)  # noqa: E501
                    response_obj["success"] = True
                    status_code = 200

                else:

                    response_obj["data"] = {}
                    response_obj["success"] = False

                    response_obj[
                        "error"
                    ] = "The company name and website must be unique as well as the tax ID within the provided state."  # noqa: E501

                    status_code = 400

            response = jsonify(response_obj)
            response.status_code = status_code

            return response

        except InternalServerError:
            raise InternalServerError

        except TypeError:
            raise BadRequestError


class CompanyProfileApi(Resource):
    @requires_auth
    def patch(self, company_profile_id) -> Response:

        response_obj = {"data": None, "error": None, "success": False}

        try:
            req_data = request.get_json()
            update_data = company_profile_schema.load(data=req_data, partial=True)  # noqa: E501
            company_profile = CompanyProfile.get_by_id(company_profile_id)
            company_profile.update(update_data)
            response_obj["data"] = company_profile_schema.dump(company_profile)
            response_obj["success"] = True
            response = jsonify(response_obj)
            response.status_code = 200

            return response

        except InternalServerError:
            raise InternalServerError

        except TypeError:
            raise BadRequestError


class CompanyTypeListApi(Resource):
    @requires_auth
    def get(self) -> Response:

        response_obj = {"data": None, "error": None, "success": False}

        try:
            response_obj["data"] = sorted(
                [{"code": d.name, "name": d.value} for d in CompanyType],
                key=itemgetter("name"),
            )
            response_obj["success"] = True
            response = jsonify(response_obj)
            response.status_code = 200

            return response

        except InternalServerError:
            raise InternalServerError


class CompanyTypeApi(Resource):
    @requires_auth
    def get(self, company_type_name) -> Response:

        response_obj = {"data": None, "error": None, "success": False}

        try:
            response_obj["data"] = CompanyType[company_type_name].value
            response_obj["success"] = True
            response = jsonify(response_obj)
            response.status_code = 200

            return response

        except InternalServerError:
            raise InternalServerError


class EmployeeCountRangeListApi(Resource):
    @requires_auth
    def get(self) -> Response:

        response_obj = {"data": None, "error": None, "success": False}

        try:
            response_obj["data"] = [
                {"code": d.name, "name": d.value} for d in EmployeeCountRange
            ]
            response_obj["success"] = True
            response = jsonify(response_obj)
            response.status_code = 200

            return response

        except InternalServerError:
            raise InternalServerError


class EmployeeCountRangeApi(Resource):
    @requires_auth
    def get(self, employee_count_range_name) -> Response:

        response_obj = {"data": None, "error": None, "success": False}

        try:
            response_obj["data"] = EmployeeCountRange[employee_count_range_name].value  # noqa: E501
            response_obj["success"] = True
            response = jsonify(response_obj)
            response.status_code = 200

            return response

        except InternalServerError:
            raise InternalServerError


class YearlyRevenueRangeListApi(Resource):
    @requires_auth
    def get(self) -> Response:

        response_obj = {"data": None, "error": None, "success": False}

        try:
            response_obj["data"] = [
                {"code": d.name, "name": d.value} for d in YearlyRevenueRange
            ]
            response_obj["success"] = True
            response = jsonify(response_obj)
            response.status_code = 200

            return response

        except InternalServerError:
            raise InternalServerError


class YearlyRevenueRangeApi(Resource):
    @requires_auth
    def get(self, yearly_revenue_range_name) -> Response:

        response_obj = {"data": None, "error": None, "success": False}

        try:
            response_obj["data"] = YearlyRevenueRange[yearly_revenue_range_name].value  # noqa: E501
            response_obj["success"] = True
            response = jsonify(response_obj)
            response.status_code = 200

            return response

        except InternalServerError:
            raise InternalServerError


class CountriesListApi(Resource):
    @requires_auth
    def get(self) -> Response:

        response_obj = {"data": None, "error": None, "success": False}

        try:
            response_obj["data"] = sorted(
                [
                    {"code": d.alpha_3, "country_code": d.alpha_2, "name": d.name}  # noqa: E501
                    for d in pycountry.countries
                ],
                key=itemgetter("name"),
            )
            response_obj["success"] = True
            response = jsonify(response_obj)
            response.status_code = 200

            return response

        except InternalServerError:
            raise InternalServerError


class ProvincesListApi(Resource):
    @requires_auth
    def get(self) -> Response:

        response_obj = {"data": None, "error": None, "success": False}
        args = request.args

        try:
            response_obj["data"] = sorted(
                [
                    {"code": d.code, "name": d.name}
                    for d in pycountry.subdivisions.get(
                        country_code=args["country_code"]
                    )
                ],
                key=itemgetter("name"),
            )
            response_obj["success"] = True
            response = jsonify(response_obj)
            response.status_code = 200

            return response

        except InternalServerError:
            raise InternalServerError


class IndustryListApi(Resource):
    @requires_auth
    def get(self) -> Response:

        response_obj = {"data": None, "error": None, "success": False}

        try:
            accounts = Industry.get_all()
            response_obj["data"] = industries_schema.dump(accounts)
            response_obj["success"] = True
            response = jsonify(response_obj)
            response.status_code = 200

            return response

        except InternalServerError:
            raise InternalServerError


class IndustryApi(Resource):
    @requires_auth
    def get(self, industry_id):

        response_obj = {"data": None, "error": None, "success": False}

        try:
            industry = Industry.get_by_id(industry_id)
            response_obj["data"] = industry_schema.dump(industry)
            response_obj["success"] = True
            response = jsonify(response_obj)
            response.status_code = 200

            return response

        except InternalServerError:
            raise InternalServerError
