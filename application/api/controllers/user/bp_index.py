# encoding: utf-8

# created by @cloverstd
# created at 2016-06-23 11:14

from flask import current_app as app

from ._base import api
from .._base import AuthResource
from application.tasks import say_hello
from application.utils.helper import SuccessOutput

@api.resource('/hello')
class Hello(AuthResource):

    def get(self):
        self.parser.add_argument('n', type=int, required=True, help="必填")
        args = self.parser.parse_args()

        res = say_hello.delay(args.n)
        app.logger.debug("task id: {}".format(res))
        return SuccessOutput({
            'task-id': str(res)
        }, message="success")