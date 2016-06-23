# encoding: utf-8

# created by @cloverstd
# created at 2016-06-23 14:38

from flask.blueprints import Blueprint
from .tool import json_dumps


def register_router(app, controllers):

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


class Output(object):

    def __init__(self, data, code, message):
        self.data = data
        self.code = code
        self.message = message

    def show(self):
        return {
            'data': self.data,
            'meta': {
                'code': self.code,
                'message': self.message
            }
        }
    @property
    def json(self):
        return json_dumps(self.show())


class SuccessOutput(Output):

    def __init__(self, data=None, code=0, message=None):
        super(SuccessOutput, self).__init__(data=data, code=code, message=message)


class ErrorOutput(Output):
    def __init__(self, code, message=None, data=None):
        super(ErrorOutput, self).__init__(data=data, code=code, message=message)