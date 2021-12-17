from flask import request, jsonify
from flask_restful import Resource
from flask.wrappers import Response

from app.api.errors import DuplicateResourceError, InternalServerError
from app.api.auth0 import requires_auth
from app.db.models import Account


class AccountListApi(Resource):

    @requires_auth
    def post(self) -> Response:
        try:
            # Get request data
            req_data = request.get_json()

            # Query for preexisting account
            if len(Account.objects(email=req_data.get('email'))) == 0:
                account = Account(**req_data)
                account.save()

                response = jsonify({
                    'data': account,
                    'error': None,
                    'success': True
                })

                response.status_code = 200

                return response
            else:
                raise DuplicateResourceError

        except InternalServerError:
            raise InternalServerError
