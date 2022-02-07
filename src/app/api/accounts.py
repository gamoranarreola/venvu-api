from flask import request, jsonify
from flask_restful import Resource
from flask.wrappers import Response
from sqlalchemy.sql.expression import and_

from app.api.errors import (
    BadRequestError,
    DuplicateAdminSignupError,
    InternalServerError
)
from app.api.auth0 import requires_auth
from app.db.models import Account, Roles
from app.db.schemas import account_schema
from app.tasks import delete_user_from_auth0


class AccountListApi(Resource):

    """
    This endpoint will always be called after a user logs on to the VMS through Auth0.
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

            # First check if an account exists for that email address.
            account = Account.query.filter_by(email=req_data.get('email')).first()

            # New user signup.
            if account is None:
                """
                Query the accounts table for an account that:
                1) Has an email address from the same company (based on the email domain)
                2) Has an admin role (vendor admin or consumer admin)
                """
                email_domain = req_data.get('email').split('@')[1]

                admin_account = Account.query.filter(
                    and_(
                        Account.email.contains(email_domain),
                        Account.roles.overlap([
                            Roles['_VND_ADM'].name,
                            Roles['_CNS_ADM'].name
                        ])
                    )
                ).first()

                if admin_account is None:
                    # Create the account and assign both types of admin roles temporarily
                    account = Account(**req_data)
                    account.roles = [Roles['_VND_ADM'].name, Roles['_CNS_ADM'].name]
                    account.save()

                else:
                    _ = delete_user_from_auth0.apply_async(args=[req_data.get('email')])
                    raise DuplicateAdminSignupError

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
