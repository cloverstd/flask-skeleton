#!/usr/bin/env python
# encoding: utf-8

import os.path

from flask import Flask, g
import time


def create_app(package_name=None, settings_override=None):

    app = Flask(package_name or __name__, instance_relative_config=True)

    app.config.from_object(settings_override)
    register_config(app)
    register_logger(app)
    register_error_handle(app)
    register_hooks(app)
    # if with_router:
    #     register_router(app)
    return app


def register_config(app):
    """
    register config to app
    :param app:
    :return:
    """
    from .config import load_config
    app.config.from_object(load_config())


def register_logger(app):
    """
    add stream log to app.logger
    :param app:
    :return:
    """
    import logging

    formatter = logging.Formatter(
        "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s"
    )
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(logging.DEBUG)
    if not app.debug:
        stream_handler.setLevel(logging.ERROR)
    app.logger.addHandler(stream_handler)


def register_error_handle(app):
    """

    :param app:
    :return:
    """
    if app.debug:
        return

    @app.errorhandler(403)
    def page_403(error):
        return "403", 403

    @app.errorhandler(404)
    def page_404(error):
        return "404", 404

    @app.errorhandler(500)
    def page_500(error):
        app.logger.error(error)
        return "500", 500


def register_db(app):
    """
    init SQLAlchemy
    :param app:
    :return:
    """
    from .core import db
    db.init_app(app)


def register_hooks(app):

    @app.before_request
    def before_request():
        g._before_request_time = time.time()

    @app.after_request
    def after_request(response):
        if hasattr(g, '_before_request_time'):
            delta = time.time() - g._before_request_time
            response.headers['X-Render-Time'] = delta * 1000
        return response


def register_router(app):
    from . import controllers
    from flask.blueprints import Blueprint

    for module in _import_submodules_from_package(controllers):
        if hasattr(module, 'bp'):
            bp = getattr(module, 'bp')
            if bp and isinstance(bp, Blueprint):
                app.register_blueprint(bp)


def _import_submodules_from_package(package):
    import pkgutil

    modules = []
    for importer, modname, ispkg in pkgutil.iter_modules(package.__path__,
                                                         prefix=package.__name__ + "."):
        modules.append(__import__(modname, fromlist="dummy"))
    return modules


def create_celery_app(app=None):
    from celery import Celery
    app = app or create_app('flask-skeleton')
    celery = Celery(__name__, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery
