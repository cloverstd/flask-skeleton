# encoding: utf-8

# created by @cloverstd
# created at 2016-06-23 15:42

from flask_restful import Api as restful_Api, abort
from flask_restful.utils import unpack
from flask_restful.reqparse import Argument
from werkzeug.wrappers import Response as ResponseBase
from functools import wraps
import six
from ..utils.helper import Output, ErrorOutput


class Api(restful_Api):

    def output(self, resource):
        @wraps(resource)
        def wrapper(*args, **kwargs):
            resp = resource(*args, **kwargs)
            if isinstance(resp, ResponseBase):  # There may be a better way to test
                return resp
            output, code, headers = unpack(resp)
            if isinstance(output, Output):
                data = output.show()
            else:
                data = output
            return self.make_response(data, code, headers=headers)

        return wrapper


class HackArgument(Argument):

    def __init__(self, *args, **kwargs):
        if 'err_code' not in kwargs:
            self.err_code = 400400

        super(HackArgument, self).__init__(*args, **kwargs)

    def handle_validation_error(self, error, bundle_errors):
        error_str = six.text_type(error)
        error_msg = self.help.format(error_msg=error_str) if self.help else error_str
        msg = {self.name: error_msg}

        return abort(400, **ErrorOutput(code=self.err_code, message=msg).show())
