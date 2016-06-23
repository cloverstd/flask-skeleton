# encoding: utf-8

# created by @cloverstd
# created at 2016-06-23 17:05

from ..core import ma
from flask_restful import abort
from ..utils.helper import ErrorOutput


class BaseModelSchema(ma.ModelSchema):

    def handle_error(self, exc, data):

        return abort(400, **ErrorOutput(code=self.err_code, message=exc.message).show())