from flask import request, jsonify
from flask_restful import Resource
from flask.wrappers import Response

from app.api.errors import InternalServerError
from app.api.auth0 import requires_auth
from app.db import db
from app.db.models import Account, account_schema


class AccountListApi(Resource):

    @requires_auth
    def post(self) -> Response:
        try:
            req_data = request.get_json()
            query_result = Account.query.filter_by(email=req_data.get('email')).first()

            if query_result is None:
                account = Account(**req_data)
                db.session.add(account)
                db.session.commit()
            else:
                account = query_result

            response = jsonify({
                'data': account_schema.dump(account),
                'error': None,
                'success': True
            })

            response.status_code = 200

            return response

        except InternalServerError:
            raise InternalServerError
