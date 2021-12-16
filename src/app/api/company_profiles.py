from flask import request, jsonify
from flask_restful import Resource
from flask.wrappers import Response
from flask_cors import cross_origin

from app.api.errors import InternalServerError
from app.api.auth0 import requires_auth


class CompanyProfileListApi(Resource):

    @cross_origin(headers=['Content-Type', 'Authorization'])
    @requires_auth
    def post(self) -> Response:
        try:
            response = jsonify({
                'data': None,
                'error': None,
                'success': True
            })

            response.status_code = 200

            return response

        except InternalServerError:
            raise InternalServerError
