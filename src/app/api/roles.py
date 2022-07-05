from operator import itemgetter
from flask.wrappers import Response
from flask_restful import Resource
from flask import jsonify, request
from pytest import Item

from app.api.errors import (
    BadRequestError,
    InternalServerError
)

from app.api.auth0 import Auth0, requires_auth


class RolesListApi(Resource):

    @requires_auth
    def get(self) -> Response:

        response_obj = {"data": None, "error": None, "success": False}

        try:
            response_obj["data"] = sorted([
                {
                    "id": r["id"],
                    "name": r["name"],
                    "permissions": sorted([
                        {
                            "permission_name": p["permission_name"],
                            "description": p["description"]
                        } for p in Auth0.auth0_get_role_permissions(r["id"])
                    ], key=itemgetter("permission_name"))
                } for r in Auth0.auth0_get_roles() if request.args["account_type"] in r["name"]
            ], key=itemgetter("name"))

            response_obj["success"] = True
            response = jsonify(response_obj)
            response.status_code = 200

            return response

        except InternalServerError:
            raise InternalServerError
        except TypeError:
            raise BadRequestError
