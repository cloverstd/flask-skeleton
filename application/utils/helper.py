# encoding: utf-8

# created by @cloverstd
# created at 2016-06-23 14:38

# import pkgutil
from flask.blueprints import Blueprint


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
