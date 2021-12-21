from flask_restful import HTTPException


class InternalServerError(HTTPException):
    pass


class InvalidQueryError(HTTPException):
    pass


class DuplicateResourceError(HTTPException):
    pass


class UnauthorizedError(HTTPException):
    pass


class BadRequestError(HTTPException):
    pass


errors = {
    'BadRequestError': {
        'message': 'Bad request',
        'status': 400
    },
    'InternalServerError': {
        'message': 'Internal server error',
        'status': 500
    },
    'InvalidQueryError': {
        'message': '',
        'status': 500
    },
    'UnauthorizedError': {
        'message': 'Unauthorized',
        'status': 401
    },
    'DuplicateResourceError': {
        'message': 'Duplicate resource',
        'status': 409
    }
}
