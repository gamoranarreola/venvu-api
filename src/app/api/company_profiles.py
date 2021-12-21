from flask import request, jsonify
from flask_restful import Resource
from flask.wrappers import Response
from sqlalchemy.sql.elements import True_

from app.api.errors import BadRequestError, InternalServerError
from app.api.auth0 import requires_auth
from app.db import db
from app.db.models import CompanyProfile
from app.db.schemas import company_profile_schema


class CompanyProfileListApi(Resource):

    @requires_auth
    def post(self) -> Response:

        response_obj = {
            'data': None,
            'error': None,
            'success': False
        }

        try:
            req_data = request.get_json()
            company_profile = CompanyProfile.query.filter_by(name=req_data.get('name')).first()

            if company_profile is None:
                company_profile = CompanyProfile(**req_data)
                db.session.add(company_profile)
                db.session.commit()

            response_obj['data'] = company_profile_schema.dump(company_profile)
            response_obj['success'] = True
            response = jsonify(response_obj)
            response.status_code = 200

            return response

        except InternalServerError:
            raise InternalServerError

        except TypeError as e:
            print(f'{e}')
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
