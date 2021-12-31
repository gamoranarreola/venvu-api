from flask import request, jsonify
from flask_restful import Resource
from flask.wrappers import Response

from app.api.errors import BadRequestError, InternalServerError
from app.api.auth0 import requires_auth
from app.db import db
from app.db.models import Account
from app.db.schemas import account_schema


class AccountListApi(Resource):

    """
    This endpoint will always be called after a user logs on to the VMS through Auth0. If there is no account record
    in the VMS database with the provided email address, it will be created. If it does exist, it will come simply
    be retrieved and sent back in the response.
    """
    @requires_auth
    def post(self) -> Response:

        response_obj = {
            'data': None,
            'error': None,
            'success': False
        }

        try:
            req_data = request.get_json()
            account = Account.query.filter_by(email=req_data.get('email')).first()

            """
            This is a new account. We need to make sure this is not an attempt to create an admin account for a company
            that already has an admin account.
            """
            if account is None:
                account = Account(**req_data)
                db.session.add(account)
                db.session.commit()

            response_obj['data'] = account_schema.dump(account)
            response_obj['success'] = True
            response = jsonify(response_obj)
            response.status_code = 200

            return response

        except InternalServerError:
            raise InternalServerError

        except TypeError:
            raise BadRequestError


class AccountApi(Resource):

    @requires_auth
    def put(self, account_id) -> Response:

        response_obj = {
            'data': None,
            'error': None,
            'success': False
        }

        try:
            req_data = request.get_json()
            update_data = account_schema.load(data=req_data, partial=True)
            account = Account.get_by_id(account_id)
            account.update(update_data)
            response_obj['data'] = account_schema.dump(account)
            response_obj['success'] = True
            response = jsonify(response_obj)
            response.status_code = 200

            return response

        except InternalServerError:
            raise InternalServerError

        except TypeError:
            raise BadRequestError
