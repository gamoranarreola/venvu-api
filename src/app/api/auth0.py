import os
import json
import http.client
from urllib.parse import urlencode

import six
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt

from app.api.errors import UnauthorizedError


vms_api_app = {
    'client_id': 'nl7qE0EZL2d0mBc7NAsnwhqarhEsTnTA',
    'client_secret': 'p2H_Z4w5LAJDcxH4CzEe0ewvt6COHCRf6WbJsyVN5PVvRttUnMo2coa_ElCVgUj8',
}

auth0_system_api = {
    'identifier': 'https://' + os.environ.get('AUTH0_DOMAIN') + '/api/v2/'
}


"""
From Auth0 sample.
"""
def get_token_auth_header():
    auth = request.headers.get('Authorization', None)

    if not auth:
        raise UnauthorizedError

    parts = auth.split()

    if parts[0] != 'Bearer' or len(parts) != 2:
        raise UnauthorizedError

    token = parts[1]

    return token


"""
From Auth0 sample.
"""
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_auth_header()
        jsonurl = six.moves.urllib.request.urlopen('https://' + os.environ.get('AUTH0_DOMAIN') + '/.well-known/jwks.json')
        jwks = json.loads(jsonurl.read())
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}

        for key in jwks['keys']:
            if key['kid'] == unverified_header['kid']:
                rsa_key = {
                    'kty': key['kty'],
                    'kid': key['kid'],
                    'use': key['use'],
                    'n': key['n'],
                    'e': key['e']
                }

        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=['RS256'],
                    audience=os.environ.get('API_AUDIENCE'),
                    issuer='https://' + os.environ.get('AUTH0_DOMAIN') + '/'
                )
            except Exception:
                raise UnauthorizedError

            _request_ctx_stack.top.current_user = payload

            return f(*args, **kwargs)

        raise UnauthorizedError

    return decorated


"""
Retrieves an auth token for the Auth0 Management API. The requestor
is the VMS API App.
"""
def auth0_get_mgmt_api_token():
    conn = http.client.HTTPSConnection(os.environ.get('AUTH0_DOMAIN'))

    data = {
        'client_id': vms_api_app.get('client_id'),
        'client_secret': vms_api_app.get('client_secret'),
        'audience': auth0_system_api.get('identifier'),
        'grant_type': "client_credentials"
    }

    conn.request(
        'POST',
        '/oauth/token',
        json.dumps(data),
        { 'content-type': 'application/json' }
    )

    return json.loads(conn.getresponse().read()).get('access_token')


def auth0_get_user_by_email(email):
    conn = http.client.HTTPSConnection(os.environ.get('AUTH0_DOMAIN'))

    conn.request(
        'GET',
        '/api/v2/users-by-email?' + urlencode({ 'email': email }),
        headers={
            'authorization': 'Bearer ' + auth0_get_mgmt_api_token(),
            'content-type': 'application/json'
        }
    )

    return json.loads(conn.getresponse().read())


def auth0_delete_user(id):
    conn = http.client.HTTPSConnection(os.environ.get('AUTH0_DOMAIN'))

    conn.request(
        'DELETE',
        '/api/v2/users/' + urlencode(id),
        headers={
            'authorization': 'Bearer ' + auth0_get_mgmt_api_token(),
            'content-type': 'application/json'
        }
    )

    return json.loads(conn.getresponse().read())
