from flask import request, jsonify
from flask_restful import Resource
from flask.wrappers import Response

from app.api.errors import BadRequestError, InternalServerError
from app.api.auth0 import requires_auth
from app.db import db
from app.db.models import Account, CompanyProfile
from app.db.schemas import company_profile_schema


class CompanyProfileListApi(Resource):

    @requires_auth
    def post(self) -> Response:

        """
        A default response object.
        """
        response_obj = {
            'data': None,
            'error': None,
            'success': False
        }

        status_code = None

        try:

            """
            Query for an account with the
            provided email address.
            """
            req_data = request.get_json()
            account = Account.query.filter_by(email=req_data.get('email')).first()

            """
            Account not found.
            """
            if account is None:

                response_obj['error'] = 'An account with the email address {} does not exist.'.format(req_data.get('email'))
                status_code = 404

            else:

                """
                Query for a company profile with the provided name.
                """
                company_profile = CompanyProfile.query.filter_by(name=req_data.get('company_profile')['name']).first()

                """
                If no such company profile
                is found, create it.
                """
                if company_profile is None:
                    company_profile = CompanyProfile(**req_data)
                    db.session.add(company_profile)
                    db.session.commit()

                response_obj['data'] = company_profile_schema.dump(company_profile)

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

        response_obj = {
            'data': None,
            'error': None,
            'success': False
        }

        try:
            req_data = request.get_json()
            update_data = company_profile_schema.load(data=req_data, partial=True)
            company_profile = CompanyProfile.get_by_id(company_profile_id)
            company_profile.update(update_data)
            response_obj['data'] = company_profile_schema.dump(company_profile)
            response_obj['success'] = True
            response = jsonify(response_obj)
            response.status_code = 200

            return response

        except InternalServerError:
            raise InternalServerError

        except TypeError:
            raise BadRequestError
