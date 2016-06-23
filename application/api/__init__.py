# encoding: utf-8

# created by @cloverstd
# created at 2016-06-23 14:21

from .. import factory
from ..utils import helper


def create_app(settings_override=None):

    app = factory.create_app(__name__, settings_override)

    register_router(app)

    return app


def register_router(app):
    from . import controllers
    helper.register_router(app, controllers)