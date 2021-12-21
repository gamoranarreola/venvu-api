from flask import request, jsonify
from flask_restful import Resource
from flask.wrappers import Response

from app.api.errors import InternalServerError
from app.api.auth0 import requires_auth
from app.db import db
from app.db.models import Account
from app.db.schemas import account_schema


class AccountListApi(Resource):

    @requires_auth
    def post(self) -> Response:

        try:
            req_data = request.get_json()
            account = Account.query.filter_by(email=req_data.get('email')).first()

            if account is None:
                account = Account(**req_data)
                db.session.add(account)
                db.session.commit()

            response = jsonify({
                'data': account_schema.dump(account),
                'error': None,
                'success': True
            })

            response.status_code = 200

            return response

        except InternalServerError:
            raise InternalServerError


class AccountApi(Resource):

    @requires_auth
    def put(self, account_id) -> Response:

        try:
            req_data = request.get_json()
            update_data = account_schema.load(data=req_data, partial=True)
            account = Account.get_by_id(account_id)
            account.update(update_data)
            serialized_account = account_schema.dump(account)

            response = jsonify({
                'data': serialized_account,
                'error': None,
                'success': True
            })

            response.status_code = 200

            return response

        except InternalServerError:
            raise InternalServerError
