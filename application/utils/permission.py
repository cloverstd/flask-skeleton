# encoding: utf-8

# created by @cloverstd
# created at 2016-06-24 10:27

from flask import g
from functools import wraps
from flask import abort
from ..models import db_user as U


def import_user():
    if hasattr(g, 'current_user'):
        return g.current_user
    else:
        return None


def user_is(role_flag, get_user=import_user, _abort=abort):
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            current_user = get_user()
            if not current_user:
                return _abort(403, "You do not have access")
            role = U.Role.get_by_flag(role_flag)
            if role in current_user.roles:
                return func(*args, **kwargs)
            return _abort(403, "You do not have access")
        return inner
    return wrapper


def user_has(permission_flag, methods=None, get_user=import_user, _abort=abort):
    def wrapper(func):
        @wraps(func)
        def inner(*ars, **kwargs):
            desired_permission = U.Permission.get_by_flag(permission_flag)
            all_methods = map(lambda x: x.method, desired_permission)
            for method in methods or ['GET']:
                if method.upper() not in all_methods:
                    return _abort(403, "You do not have access")

            user_permissions = []
            current_user = get_user()
            if not current_user:
                return _abort(403, "You do not have access")
            for role in current_user.roles:
                user_permissions += role.permissions
            if (set(desired_permission) & set(user_permissions)) != set(desired_permission):
                return _abort(403, "You do not have access")
            return func(*ars, **kwargs)
        return inner
    return wrapper
