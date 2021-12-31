import os
import json

import six
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt

from app.api.errors import UnauthorizedError


def get_token_auth_header():
    auth = request.headers.get('Authorization', None)

    if not auth:
        raise UnauthorizedError

    parts = auth.split()

    if parts[0] != 'Bearer' or len(parts) != 2:
        raise UnauthorizedError

    token = parts[1]

    return token


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
