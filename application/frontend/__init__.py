# encoding: utf-8

# created by @cloverstd
# created at 2016-06-23 14:15

from .. import factory
from ..utils import helper
from flask import render_template


def create_app(settings_override=None):
    app = factory.create_app(__name__, settings_override)

    register_router(app)
    register_error_handler(app)

    return app


def register_router(app):
    from . import controllers
    helper.register_router(app, controllers)


def register_error_handler(app):
    if True:
        for e in [500, 404, 403]:
            app.errorhandler(e)(handle_error)


def handle_error(e):
    return render_template("error/{}.html".format(e.code)), e.code