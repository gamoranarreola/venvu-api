from operator import eq, or_
from unicodedata import name
from flask import request, jsonify
from flask_restful import Resource
from flask.wrappers import Response
from sqlalchemy.sql.expression import and_, or_

from app.api.errors import BadRequestError, InternalServerError
from app.api.auth0 import requires_auth
from app.db.models import Account, CompanyProfile, Role, AccountType
from app.db.schemas import company_profile_schema, account_schema


class CompanyProfileListApi(Resource):
    @requires_auth
    def post(self) -> Response:

        """
        A default response object.
        """
        response_obj = {"data": None, "error": None, "success": False}

        status_code = None

        try:

            """
            Query for an account with the
            provided email address.
            """
            req_data = request.get_json()
            account = Account.query.filter_by(email=req_data.get("email")).first()

            """
            Account not found.
            """
            if account is None:

                response_obj[
                    "error"
                ] = "An account with the email address {} does not exist.".format(
                    req_data.get("email")
                )
                status_code = 404

            else:

                """
                Query for a company profile with the provided name.
                """
                company_profile = CompanyProfile.query.filter(
                    or_(
                        CompanyProfile.name == req_data.get("company_profile")["name"],
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

                    company_profile = CompanyProfile(**req_data.get("company_profile"))
                    company_profile.accounts.append(account)
                    company_profile.save()

                    account_data = {**req_data.get("account")}
                    account_data["account_type"] = AccountType[
                        account_data["account_type"]
                    ]

                    if account_data["account_type"] == AccountType._CNS:
                        account_data["roles"] = [Role._CNS_ADM]
                    elif account_data["account_type"] == AccountType._VND:
                        account_data["roles"] = [Role._VND_ADM]

                    account.update(account_schema.load(data=account_data, partial=True))

                    response_obj["data"] = company_profile_schema.dump(company_profile)
                    response_obj["success"] = True
                    status_code = 200

                else:

                    response_obj["data"] = {}
                    response_obj["success"] = False
                    response_obj[
                        "error"
                    ] = "The company name and website must be unique as well as the tax ID within the provided state."
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
    def put(self, company_profile_id) -> Response:

        response_obj = {"data": None, "error": None, "success": False}

        try:
            req_data = request.get_json()
            update_data = company_profile_schema.load(data=req_data, partial=True)
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
