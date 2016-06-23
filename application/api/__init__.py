# encoding: utf-8

# created by @cloverstd
# created at 2016-06-23 14:21

from .. import factory
from ..utils import helper


def create_app(settings_override=None):

    app = factory.create_app(__name__, settings_override)
    register_jwt(app)
    register_router(app)

    return app


def register_router(app):
    from . import controllers
    helper.register_router(app, controllers)


def register_jwt(app):
    from flask import make_response

    from .core import jwt
    from ..models.db_user import User
    from ..utils.helper import SuccessOutput, ErrorOutput

    @jwt.authentication_handler
    def authenticate(username, password):
        user = User.query.filter(User.username == username).scalar()
        if user.check_password(password):
            return user

    @jwt.identity_handler
    def identify(payload):
        return User.query.filter(User.id == payload['identity']).scalar()

    @jwt.jwt_error_handler
    def error_handler(e):
        app.logger.warning(e)
        response = make_response(ErrorOutput(40000, "auth failed").json)
        response.headers['Content-Type'] = 'application/json'
        response.status_code = 200
        return response

    @jwt.auth_response_handler
    def response_handler(access_token, identify):
        response = make_response(SuccessOutput(data=access_token.decode('utf-8')).json)
        response.headers['Content-Type'] = 'application/json'
        response.status_code = 200
        return response

    jwt.init_app(app)
