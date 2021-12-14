from flask_restful import HTTPException


class InternalServerError(HTTPException):
    pass


class InvalidQueryError(HTTPException):
    pass


class DuplicateResourceError(HTTPException):
    pass


class UnauthorizedRoleError(HTTPException):
    pass


class UnauthorizedError(HTTPException):
    pass


class BadRequestError(HTTPException):
    pass


errors = {
    'BadRequestError': {
        'message': '',
        'status': 400
    },
    'InternalServerError': {
        'message': '',
        'status': 500
    },
    'InvalidQueryError': {
        'message': '',
        'status': 500
    },
    'UnauthorizedRoleError': {
        'message': '',
        'status': 401
    },
    'UnauthorizedError': {
        'message': '',
        'status': 401
    },
    'DuplicateResourceError': {
        'message': '',
        'status': 409
    }
}
