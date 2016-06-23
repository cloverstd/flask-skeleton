# encoding: utf-8

# created by @cloverstd
# created at 2016-06-23 14:24

from flask import Blueprint
from application.tasks import say_hello

bp = Blueprint(
    'index',
    __name__,
    url_prefix="",
)


@bp.route('/hello')
def hello():
    say_hello.delay(10)
    return "api hello"
