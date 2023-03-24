import http.client
import json
import os
from functools import wraps
from urllib.parse import urlencode
from urllib.request import pathname2url

import six
from flask import _request_ctx_stack, request
from jose import jwt

from app.model.errors import UnauthorizedError


def get_token_auth_header():
    auth = request.headers.get("Authorization", None)

    if not auth:
        raise UnauthorizedError

    parts = auth.split()

    if parts[0] != "Bearer" or len(parts) != 2:
        raise UnauthorizedError

    token = parts[1]

    return token


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_auth_header()
        jsonurl = six.moves.urllib.request.urlopen(
            "https://"
            + os.environ.get("AUTH0_DOMAIN")
            + "/.well-known/jwks.json"  # noqa: E501
        )
        jwks = json.loads(jsonurl.read())
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}

        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"],
                }

        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=["RS256"],
                    audience=os.environ.get("API_AUDIENCE"),
                    issuer="https://" + os.environ.get("AUTH0_DOMAIN") + "/",
                )
            except Exception:
                raise UnauthorizedError

            _request_ctx_stack.top.current_user = payload

            return f(*args, **kwargs)

        raise UnauthorizedError

    return decorated


class Auth0:
    vms_api_app = {
        "client_id": "nl7qE0EZL2d0mBc7NAsnwhqarhEsTnTA",
        "client_secret": "p2H_Z4w5LAJDcxH4CzEe0ewvt6COHCRf6WbJsyVN5PVvRttUnMo2coa_ElCVgUj8",  # noqa: E501
    }

    auth0_system_api = {
        "identifier": "https://" + os.environ.get("AUTH0_DOMAIN") + "/api/v2/"
    }

    last_vms_admin_user_id = None
    last_vms_user_id = None

    @staticmethod
    def auth0_get_mgmt_api_token():
        """
        Retrieves an auth token for the Auth0 Management API. The requestor
        is the VMS API App.
        """
        conn = http.client.HTTPSConnection(os.environ.get("AUTH0_DOMAIN"))

        data = {
            "client_id": Auth0.vms_api_app.get("client_id"),
            "client_secret": Auth0.vms_api_app.get("client_secret"),
            "audience": Auth0.auth0_system_api.get("identifier"),
            "grant_type": "client_credentials",
        }

        conn.request(
            "POST",
            "/oauth/token",
            json.dumps(data),
            headers={"content-type": "application/json"},
        )

        return json.loads(conn.getresponse().read()).get("access_token")

    @staticmethod
    def auth0_create_user(email, password, is_admin=False):
        conn = http.client.HTTPSConnection(os.environ.get("AUTH0_DOMAIN"))

        data = {
            "email": email,
            "connection": "Username-Password-Authentication",
            "password": password,
        }

        conn.request(
            "POST", "/api/v2/users",
            json.dumps(data),
            headers=Auth0.get_headers()
        )

        user = json.loads(conn.getresponse().read())

        if is_admin:
            Auth0.last_vms_admin_user_id = user.get("user_id")
        else:
            Auth0.last_vms_user_id = user.get("user_id")

        return user

    @staticmethod
    def auth0_assign_user_roles(user_id, roles):
        conn = http.client.HTTPSConnection(os.environ.get("AUTH0_DOMAIN"))
        roles_string = "{\"roles\":["

        for idx, role in enumerate(roles):
            roles_string += f"\"{role}\""

            if idx < (len(roles) - 1):
                roles_string += ","

        roles_string += "]}"

        conn.request(
            "POST",
            "/api/v2/users/" + pathname2url(user_id) + "/roles",
            json.dumps(roles_string),
            headers=Auth0.get_headers(),
        )

        res = json.loads(conn.getresponse().read())
        print(res)
        return res

    @staticmethod
    def auth0_get_roles():
        conn = http.client.HTTPSConnection(os.environ.get("AUTH0_DOMAIN"))

        conn.request(
            "GET",
            "/api/v2/roles",
            headers=Auth0.get_headers(),
        )

        return json.loads(conn.getresponse().read())

    @staticmethod
    def auth0_get_role_permissions(role: str):
        conn = http.client.HTTPSConnection(os.environ.get("AUTH0_DOMAIN"))

        conn.request(
            "GET",
            f"/api/v2/roles/{role}/permissions",
            headers=Auth0.get_headers(),
        )

        return json.loads(conn.getresponse().read())

    @staticmethod
    def auth0_get_user_by_email(email):
        conn = http.client.HTTPSConnection(os.environ.get("AUTH0_DOMAIN"))

        conn.request(
            "GET",
            "/api/v2/users-by-email?" + urlencode({"email": email}),
            headers=Auth0.get_headers(),
        )

        return json.loads(conn.getresponse().read())

    @staticmethod
    def auth0_delete_user(id):
        conn = http.client.HTTPSConnection(os.environ.get("AUTH0_DOMAIN"))

        conn.request(
            "DELETE",
            "/api/v2/users/" + pathname2url(id),
            headers=Auth0.get_headers()
        )
        print("\n\nauth0_delete_user: " + id)
        return conn.getresponse().read()

    @staticmethod
    def get_headers():

        return {
            "authorization": "Bearer " + Auth0.auth0_get_mgmt_api_token(),
            "content-type": "application/json",
            "cache-control": "no-cache",
        }
