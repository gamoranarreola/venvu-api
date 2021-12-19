from flask import request, jsonify
from flask_restful import Resource
from flask.wrappers import Response

from app.api.errors import InternalServerError
from app.api.auth0 import requires_auth
from app.db.models import Account


class AccountListApi(Resource):

    @requires_auth
    def post(self) -> Response:
        try:
            req_data = request.get_json()
            query_result = Account.objects(email=req_data.get('email'))

            if len(query_result) == 0:
                account = Account(**req_data)
                account.save()
            else:
                account = query_result[0]

            response = jsonify({
                'data': account,
                'error': None,
                'success': True
            })

            response.status_code = 200

            return response

        except InternalServerError:
            raise InternalServerError
