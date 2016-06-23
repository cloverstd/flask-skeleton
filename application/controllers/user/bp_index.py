# encoding: utf-8

# created by @cloverstd
# created at 2016-06-23 11:14

from flask import current_app as app

from ._base import bp
from application.tasks import say_hello


@bp.route('/hello', defaults={'n': 10})
@bp.route('/hello/<int:n>')
def hello(n=10):
    res = say_hello.delay(n)
    app.logger.debug("Task ID: {}".format(res))
    return "user hello"
